"""τ des places, des agrégateurs et des oracles (PROPOSITION §4.3 à §4.5 ; ADR-0029 l.187, l.189 et ajout daté l.403
(2) ; AVIS Q-CA-04, Q-CA-06). Population de τ des places : cellules (t, p) au dernier prix connu, au moins N_min
places définies en t ; cellules d'une place à horodatage de dernière transaction exclues quand 60·âge > σ (borne basse
de l'âge, déclarée), leur prix gardé dans la médiane des autres ; écart e = |c − m| / m à la médiane leave-one-out m
des autres places définies (moyenne des deux du milieu pour un nombre pair) ; m ≤ 0 : CA/mediane. Rationnels exacts
(Fraction), jamais de flottant (E-CA-18)."""
from __future__ import annotations

import json
import math
import os
import sys
from decimal import Context, Decimal, localcontext
from fractions import Fraction

import bougies
import sigma
import socle


def rationnels(c: list) -> list:
    """Clôtures (Decimal ou None) en Fraction, chaque valeur distincte convertie une fois."""
    vus = {}
    return [None if x is None else vus.setdefault(x, Fraction(x)) for x in c]


def mediane(valeurs: list) -> Fraction:
    v, m = sorted(valeurs), len(valeurs)
    return v[m // 2] if m % 2 else (v[m // 2 - 1] + v[m // 2]) / 2


def ecarts(actif: str, closes: dict, ages: dict, strates: list, n_min: int, exclusion: dict) -> dict:
    """{strate : (écarts, places, âges)} des cellules de la population (§4.3 pt 1 et 2 ; Q-CA-04) : closes et ages
    {place : liste sur la grille des minutes} ; exclusion {place : σ en secondes} des places à horodatage de
    dernière transaction."""
    places, out = sorted(closes), {st: ([], [], []) for st in ("calme", "stress")}
    for i, st in enumerate(strates):
        definies = [p for p in places if closes[p][i] is not None]
        if len(definies) < n_min:
            continue
        for p in definies:
            if p in exclusion and 60 * ages[p][i] > exclusion[p]:
                continue
            m = mediane([closes[q][i] for q in definies if q != p])
            if m <= 0:
                raise socle.Refus("CA/mediane", "médiane leave-one-out nulle ou négative", actif, strate=st, place=p)
            e, pl, ag = out[st]
            e.append(abs(closes[p][i] - m) / m)
            pl.append(p)
            ag.append(ages[p][i])
    return out


def places(prm: dict, actif: str, cel: dict) -> dict:
    """τ des places (§4.3 pt 3 ; ADR-0029 l.187) : P99,9 au rang ⌈999·N/1000⌉ par strate, maximum sur les strates, ×
    1,5, grid-ceil à 0,05 %, bornes ; P99 et maximum par strate imprimés ; strate sans cellule : CA/population ; règle à
    la borne haute ou au-delà : CA/borne (la valeur n'entre pas au refus, §5.7)."""
    t, par = prm["tau"], {}
    for st, (e, _pl, _ag) in cel.items():
        if not e:
            raise socle.Refus("CA/population", "aucune cellule à N_min places définies", actif, strate=st)
        par[st] = (len(e), socle.quantile(e, *t["rang"]), socle.quantile(e, 99, 100), max(e))
    p999 = max(v[1] for v in par.values())
    tau, drapeau, valeur = socle.regle(t["facteur"], p999, t["pas"], t["borne_basse"], t["borne_haute_exclue"])
    if tau is None:
        raise socle.Refus("CA/borne", "τ des places à la borne haute exclue ou au-delà", actif,
                          valeur=("τ des places", valeur))
    return {"tau": tau, "drapeau": drapeau, "regle": valeur, "p999": p999, "strates": par,
            "regle_au_maximum": socle.regle(t["facteur"], max(v[3] for v in par.values()), t["pas"], 0, 1)[2]}


def agregateurs(prm: dict, actif: str, tau_places, btc: dict) -> dict:
    """τ des agrégateurs (§4.4 ; ADR-0029 l.189, ajout daté l.403 (2)) : grid-ceil(τ_places × τ_agr_BTC /
    max(τ_BTC des deux classes de places), 0,05 %), bornes ; imprimés : la règle sous les autres dénominateurs
    (horodatée, sans horodatage, minimum), τ_agr_BTC tel quel, drapeau τ_agr < τ_places (Q-CA-06), jamais un refus.
    τ de BTC absent, refusé ou nul pour une classe lue : CA/btc."""
    cles = [("tau", c) for c in ("agregateur", "place_horodatee", "sans_horodatage")]
    if any(k not in btc or btc[k] <= 0 for k in cles):
        raise socle.Refus("CA/btc", "τ de BTC absent, refusé ou nul", actif, "agregateur")
    a, ph, sh, t = (*(Fraction(btc[k]) for k in cles), prm["tau"])

    def r(den):
        return socle.regle(1, Fraction(tau_places) * a / den, t["pas"], t["borne_basse"], t["borne_haute_exclue"])
    tau, drapeau, valeur = r(max(ph, sh))
    if tau is None:
        raise socle.Refus("CA/borne", "τ des agrégateurs à la borne haute exclue ou au-delà", actif, "agregateur",
                          valeur=("τ des agrégateurs", valeur))
    return {"tau": tau, "drapeau": drapeau, "regle": valeur, "sous_places": tau < tau_places,
            "autres": {"place_horodatee": r(ph)[2], "sans_horodatage": r(sh)[2], "minimum": r(min(ph, sh))[2],
                       "tel_quel": btc["tau", "agregateur"]}}


def calcul_actif(prm: dict, actif: str, series: dict, fen: dict, btc: dict) -> dict:
    """Un actif, dans l'ordre σ, τ des places, τ des agrégateurs, oracles (E-CA-17) : séries {place : série} de la
    lecture retenue sur la fenêtre ; mode « planchers seuls » : τ des places = 0,375 %, aucun troisième terme (§4.7)."""
    lec, closes, ages = socle.lecture(prm), {}, {}
    strates = [socle.strate(t, prm) for t in socle.minutes(fen)]
    for p, s in series.items():
        c, a = bougies.derniers(s, fen)
        closes[p], ages[p] = rationnels(c), a
    pop, mode = sigma.population(prm, actif), lec["modes"][actif]
    terme, detail = sigma.troisieme_terme(prm, {p: ages[p] for p in pop}, strates)
    sig, cel = sigma.sigmas(prm, actif, btc, terme, mode), None
    if mode == "planchers_seuls":
        tp = {"tau": Decimal(prm["tau"]["planchers_seuls"]), "drapeau": "planchers seuls (ADR-0029 l.191)"}
    else:
        cel = ecarts(actif, closes, ages, strates, lec["n_min"][actif], {p: sig["place_horodatee"] for p in pop})
        tp = places(prm, actif, cel)
    return {"mode": mode, "sigma": sig, "terme": terme, "detail_terme": detail, "places": tp, "cellules": cel,
            "agregateurs": agregateurs(prm, actif, tp["tau"], btc), "oracle": socle.oracles(prm)[actif],
            "closes": closes, "ages": ages, "strates": strates}


def fragment(prm: dict, res: dict) -> dict:
    """Fragment pour s2bis/config/analyse.json (E-CA-22) : tau_sigma et unites d'ETH, d'USDC et d'USDT (forme de
    config_analyse.py : τ en chaîne décimale, σ entier ou null), et le mode par actif (Q-CA-15 modifiée)."""
    ts = {}
    for a, r in res.items():
        tp, s = str(r["places"]["tau"]), r["sigma"]
        ts[a] = {"agregateur": {"sigma": s["agregateur"], "tau": str(r["agregateurs"]["tau"])},
                 "oracle_chainlink": {"sigma": r["oracle"][1], "tau": str(r["oracle"][0])},
                 "place_horodatee": {"sigma": s["place_horodatee"], "tau": tp},
                 "sans_horodatage": {"sigma": None, "tau": tp}}
    return {"modes": {a: r["mode"] for a, r in res.items()}, "tau_sigma": ts,
            "unites": {a: prm["unites"][a] for a in res}}


def controle_fragment(prm: dict, frag: dict, btc: dict) -> None:
    """Contrôles E-CA-23 (a) à (h), rejoués côté lot sur le fragment avant toute écriture (ils resserrent ; RB-2 les
    porte côté recalcul) : un écart, CA/fragment nommé par la règle et l'actif."""
    t, o = prm["tau"], socle.oracles(prm)
    pas = Decimal(t["pas"])
    for a, x in frag["tau_sigma"].items():
        tp, ag, mode = Decimal(x["place_horodatee"]["tau"]), Decimal(x["agregateur"]["tau"]), frag["modes"][a]
        attendu = agregateurs(prm, a, tp, btc)["tau"]
        sigma_agr = max(prm["sigma"]["planchers_s"]["agregateur"], math.ceil(Fraction(btc["sigma", "agregateur"])))
        seuls = mode == "planchers_seuls"
        regles = {"a": ag % pas == 0,
                  "b": (tp == Decimal(t["planchers_seuls"])) == seuls and (tp % pas == 0 or seuls),
                  "c": Decimal(x["oracle_chainlink"]["tau"]) == o[a][0], "d": ag == attendu,
                  "e": x["agregateur"]["sigma"] == sigma_agr, "f": x["oracle_chainlink"]["sigma"] == o[a][1],
                  "g": x["sans_horodatage"]["sigma"] is None,
                  "h": x["sans_horodatage"]["tau"] == x["place_horodatee"]["tau"]}
        for nom, ok in regles.items():
            if not ok:
                raise socle.Refus("CA/fragment", f"contrôle E-CA-23 ({nom}) du fragment en écart", a)


def affiche(x) -> str:
    """Rationnel ou décimal en chaîne décimale à 10⁻¹⁰ près (impression seule, contexte fixé : prec 50) ; None : « - ».
    """
    if x is None:
        return "-"
    with localcontext(Context(prec=50)):
        return str((Decimal(Fraction(x).numerator) / Decimal(Fraction(x).denominator)).quantize(Decimal("1E-10")))


def queue(prm: dict, cel: dict) -> dict:
    """{place : (cellules au-delà du P99,9 de leur strate, part de la queue, âge médian en minutes)} (§4.3 pt 5 ;
    AVIS Q-CA-04 : montre si τ vient de prix périmés)."""
    par = {}
    for e, pl, ag in cel.values():
        q = socle.quantile(e, *prm["tau"]["rang"])
        for x, p, a in zip(e, pl, ag):
            if q is not None and x > q:
                par.setdefault(p, []).append(a)
    n = sum(len(v) for v in par.values())
    return {p: (len(v), Fraction(len(v), n), socle.quantile(v, 50, 100)) for p, v in sorted(par.items())}


def actives_seules(r: dict) -> dict:
    """Clôtures des seules minutes actives (âge 0), None ailleurs : variante « minutes actives seules » (§4.3 pt 5)."""
    return {p: [c if a == 0 else None for c, a in zip(r["closes"][p], r["ages"][p])] for p in r["closes"]}


def descriptifs(prm: dict, actif: str, r: dict) -> list:
    """Lignes descriptives d'un actif, jamais décisives (E-CA-20) : troisième terme sur toutes les places horodatées
    (lettre de l.189) et P99 des suites ; variante « minutes actives seules » ; queue par place ; règle au maximum ;
    τ des agrégateurs sous les autres dénominateurs, τ_agr_BTC tel quel, drapeau τ_agr < τ_places. Ne modifie pas r."""
    lec, ag = socle.lecture(prm), r["agregateurs"]
    hor = [p for p in lec["places"][actif] if p in prm["classes"]["place_horodatee"]]
    terme, detail = sigma.troisieme_terme(prm, {p: r["ages"][p] for p in hor}, r["strates"])
    out = [f"[{actif}] descriptif : troisième terme sur toutes les places horodatées ({', '.join(hor)}) : "
           f"{terme if terme is not None else 'absent'} ; P99 des suites (population retenue) : "
           + " ; ".join(f"{st} {affiche(d[2])} min" for st, d in r["detail_terme"].items())]
    if r["cellules"] is not None:
        try:
            cel = ecarts(actif, actives_seules(r), r["ages"], r["strates"], lec["n_min"][actif], {})
            v = affiche(places(prm, actif, cel)["tau"])
        except socle.Refus as e:
            v = str(e)
        out += [f"[{actif}] descriptif : τ des places, variante minutes actives seules : {v}",
                f"[{actif}] descriptif : règle au maximum : {affiche(r['places']['regle_au_maximum'])}"]
        out += [f"[{actif}] descriptif : queue au-delà du P99,9, {p} : {n} cellules, part {affiche(f)}, âge médian "
                f"{a} min" for p, (n, f, a) in queue(prm, r["cellules"]).items()]
    out.append(f"[{actif}] descriptif : τ des agrégateurs sous les dénominateurs " + " ; ".join(
        f"{k} {affiche(v)}" for k, v in ag["autres"].items())
        + f" ; τ_agr < τ_places : {'oui' if ag['sous_places'] else 'non'}")
    return out


SORTIES = ("calib_actifs.txt", "fragment_analyse.json")


def corps(prm: dict, res: dict) -> list:
    """Valeurs décisives et leurs termes, par actif et par classe (E-CA-22)."""
    out = []
    for a, r in res.items():
        s, tp, ag, d = r["sigma"], r["places"], r["agregateurs"], r["detail_terme"]
        out += [f"[{a}] mode {r['mode']} ; places {', '.join(r['closes'])} ; N_min {socle.lecture(prm)['n_min'][a]}",
                f"[{a}] σ : place_horodatee {s['place_horodatee']} s (troisième terme "
                f"{'absent' if r['terme'] is None else str(r['terme']) + ' s'}, P99 des âges par strate "
                + " ; ".join(f"{st} N {n} P99 {'-' if p99 is None else p99} min" for st, (n, p99, _x) in d.items())
                + ") ; "
                f"sans_horodatage aucun ; agregateur {s['agregateur']} s ; oracle_chainlink {s['oracle_chainlink']} s",
                f"[{a}] τ des places {tp['tau']} ; drapeau {tp['drapeau'] or 'aucun'}" + "".join(
                    f" ; {st} N {n} P99,9 {affiche(q)} P99 {affiche(q99)}" for st, (n, q, q99, _m) in
                    tp.get("strates", {}).items()),
                f"[{a}] τ des agrégateurs {ag['tau']} (règle {ag['regle']}) ; drapeau {ag['drapeau'] or 'aucun'}",
                f"[{a}] τ des oracles {r['oracle'][0]}"]
    return out


def septembre(prm: dict, bruts: str, btc: dict) -> list:
    """Fenêtre descriptive (septembre 2026, sans ses places exclues), jamais décisive : τ, σ ou le refus, par actif."""
    out, fen = [], prm["fenetre_descriptive"]
    for a in socle.ACTIFS:
        try:
            pl = [p for p in socle.lecture(prm)["places"][a] if p not in fen["sans"]]
            r = calcul_actif(prm, a, {p: bougies.charger(prm, bruts, "descriptive", p, a, fen) for p in pl}, fen, btc)
            out.append(f"[{a}] septembre : τ des places {r['places']['tau']} ; σ des places horodatées "
                       f"{r['sigma']['place_horodatee']} s ; τ des agrégateurs {r['agregateurs']['tau']}")
        except socle.Refus as e:
            out.append(f"[{a}] septembre : {e}")
    return out


def main(argv=None, env=None) -> int:
    """python3 tau.py --bruts <dossier> --sortie <dossier> [--parametres <fichier>] : épingle de tau_sigma.txt,
    séries, oracle de SH §4, puis σ, τ et oracles par actif, fragment contrôlé ; sorties en .partiel puis renommées.
    Codes : 0 ; 1 refus nommé (dans les deux sorties) ; 2 usage. Aucune exception non nommée (type seul)."""
    a = list(sys.argv[1:] if argv is None else argv)
    if len(a) not in (4, 6) or a[0::2] != ["--bruts", "--sortie", "--parametres"][:len(a) // 2]:
        print("REFUS CA/usage : tau.py --bruts <dossier> --sortie <dossier> [--parametres <fichier>]", file=sys.stderr)
        return 2
    try:
        socle.garde(os.environ if env is None else env)
        prm = socle.lire(a[5] if len(a) == 6 else socle.PARAMETRES)
        ts = socle.tau_sigma(prm)
        btc, lec = socle.valeurs_btc(ts), socle.lecture(prm)
        series = {(x, p): bougies.charger(prm, a[1], "principale", p, x, prm["fenetre"])
                  for x in socle.ACTIFS for p in lec["places"][x]}
        oracle = bougies.oracle_sh(prm, series)
        res = {x: calcul_actif(prm, x, {p: series[x, p] for p in lec["places"][x]}, prm["fenetre"], btc)
               for x in socle.ACTIFS}
        frag = fragment(prm, res)
        controle_fragment(prm, frag, btc)
        fichiers = [__file__, socle.__file__, bougies.__file__, sigma.__file__,
                    a[5] if len(a) == 6 else socle.PARAMETRES, ts, os.path.join(a[1], "manifeste.tsv")]
        tete = ["sha256 : " + " ; ".join(f"{os.path.basename(f)} {socle.empreinte(f) if os.path.isfile(f) else '-'}"
                                         for f in fichiers),
                f"lecture {prm['lecture']} ; fenêtre {prm['fenetre']['debut']} à {prm['fenetre']['fin']} exclu",
                *oracle, "[VALEURS]", *corps(prm, res), "[DESCRIPTIFS]"]
        lignes = tete + [y for x in socle.ACTIFS for y in descriptifs(prm, x, res[x])] + septembre(prm, a[1], btc)
        sorties, code = {"calib_actifs.txt": lignes, "fragment_analyse.json": frag}, 0
    except Exception as e:                                          # jamais une trace : refus nommé, type seul
        r = e if isinstance(e, socle.Refus) else socle.Refus("CA/calcul", f"calcul en échec ({type(e).__name__})")
        hors = [] if r.valeur is None else [f"descriptif hors refus (jamais décisif) : valeur calculée de la règle, "
                                            f"{r.valeur[0]} : {r.valeur[1]} ; {r.lieu}"]      # C-13 : ligne à part
        sorties, code = {"calib_actifs.txt": [str(r), *hors], "fragment_analyse.json": {"refus": str(r)}}, 1
    os.makedirs(a[3], exist_ok=True)
    socle.ecrire(a[3], SORTIES[0], sorties[SORTIES[0]])
    socle.ecrire(a[3], SORTIES[1], [json.dumps({"etiquette": socle.ETIQUETTE} | sorties[SORTIES[1]], sort_keys=True,
                                               ensure_ascii=False, indent=1)], etiquette=False)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
