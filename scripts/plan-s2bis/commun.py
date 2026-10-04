"""Commun du lot PLAN-S2BIS, préparation de S2-bis sur les journaux scellés de S2 (G0 docs/adr-0029/G0-lot-PLAN-S2BIS.md ;
ADR-0029 §2.6 et §6 lot 3 ; annexe B d'ADR-0028 : SHOGEN-TAU-REDERIV-1, SHOGEN-R1-HOTE-STRUCTUREL-1,
SHOGEN-POSTPREREG-PARAMS-SCEAU-1, SHOGEN-FICHE-WORKER-POSTEXEC-1). Harnais du commit d'analyse f35a70c importé d'une
extraction (--harnais) après contrôle du sha256 de chaque module chargé, jamais modifié ; lecture des journaux par les
appels de r1.recompute_from_journal (garde §5.3, filtre de lecture, segment J28 à n fixe, plage D5 exclue). Chaque sortie
porte ETIQUETTE en première ligne, sa provenance, puis le contrôle de cohérence (n, K, P̂_more par strate, chaîne pour
chaîne, contre parametres.json et contre le bloc 3 du rendu J28) ; en écart, aucune valeur d'analyse (code 1). Aucune
ligne de journal n'est imprimée. Aucune barre oblique inverse ici : saut de ligne par chr(10)."""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
import sys
from collections import Counter
from decimal import Decimal, localcontext

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(os.path.dirname(ICI))
PARAMETRES = os.path.join(ICI, "parametres.json")
ETIQUETTE = "préparation de S2-bis ; ne change pas le verdict de S2 (« R1 discrimine » = FAUX)"
NL = chr(10)
H: dict = {}                                    # modules du harnais chargés : r1, records, window


def sha256(chemin: str) -> str:
    with open(chemin, "rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def lire_parametres(chemin: str = PARAMETRES) -> dict:
    with open(chemin, encoding="utf-8") as f:
        return json.load(f)


def importer_harnais(harnais: str, epingles: dict) -> dict:
    """shogen_s2 du dossier `harnais` (s2-harness d'une extraction du commit d'analyse) : sha256 de chaque module épinglé
    contrôlé avant l'import ; après, tout module chargé de shogen_s2 doit être un fichier épinglé de ce dossier. Sinon
    ValueError (fail-closed). Rend {"r1", "records", "window"}."""
    racine = os.path.realpath(harnais)
    for rel, sha in sorted(epingles.items()):
        p = os.path.join(racine, rel)
        if not os.path.isfile(p) or sha256(p) != sha:
            raise ValueError(f"harnais : {rel} absent ou de sha256 différent de l'épingle — fail-closed")
    if sys.path[:1] != [racine]:
        sys.path.insert(0, racine)
    mods = {n: importlib.import_module(f"shogen_s2.{n}") for n in ("r1", "records", "window")}
    charges = {os.path.realpath(m.__file__) for n, m in list(sys.modules.items()) if n.split(".")[0] == "shogen_s2"}
    hors = charges - {os.path.join(racine, rel) for rel in epingles}
    if hors:
        raise ValueError(f"module(s) de shogen_s2 chargé(s) hors des fichiers épinglés : {sorted(hors)} — fail-closed")
    H.update(mods)
    return mods


def dec(x) -> str:
    """Decimal en chaîne sous le contexte nommé du harnais (forme des rendus) ; None : « - »."""
    with localcontext(H["r1"].contexte_decimal()):
        return "-" if x is None else str(x)


def charger(journaux: str, prm: dict) -> dict:
    """Journaux lus comme par r1.recompute_from_journal (garde §5.3, filtre de lecture, segment et plages de prm) ; pool
    S2 (D1, r1.analysis_pools), sortie « base » de r1.compute_r1 sur ce pool (contrôle de cohérence), pool D1-bis."""
    r1, records, window = H["r1"], H["records"], H["window"]
    c, j = (os.path.join(journaux, n) for n in ("control.jsonl", "journal.jsonl"))
    plist, _clock, tous = records.parse_control(c)
    p = records.effective_run_params(plist)
    if window.verify_markers_against_spec(tous, p["strate_calendar"]):
        raise ValueError("strates journalées incohérentes avec le calendrier committé (fail-closed, §5.3)")
    plages = [tuple(x) for x in prm["segment"]["plages_exclues"]]
    m, _c, _a, bornes = records.filtre_lecture(p, tous, ranges=plages, segment={
        "t0": prm["segment"]["t0"], "n_fixe": prm["segment"]["n_fixe"]})
    lus = r1.parse_journal(j)
    sbc, scf, tau = records.sigma_tau_from_params(p)
    d = {"control": c, "journal": j, "params": p, "bornes": bornes, "plages": plages, "rmap": r1.build_reading_map(lus),
         "ws": r1.build_window_strate(m), "w": int(p["w"]), "sbc": sbc, "scf": scf, "tau": tau,
         "n_min": int(p["n_min_hors_enveloppe"])}
    if set(d["ws"].values()) - set(prm["strates"]):
        raise ValueError(f"strate(s) hors de parametres.json : {sorted(set(d['ws'].values()) - set(prm['strates']))}")
    d["pools_s2"], pool, d["retraits_s2"] = r1.analysis_pools(m, lus, list(p["pool"]))
    d["base"] = r1.compute_r1(m, lus, pool, d["w"], sbc, scf, tau, Decimal(str(p["seuil_historique_valeur"])),
                              d["n_min"], pool_by_strate=d["pools_s2"])
    d["pools_bis"], d["retraits_bis"] = pool_d1bis(d, prm)
    return d


def pool_d1bis(d: dict, prm: dict) -> tuple:
    """Pool D1-bis par strate (ADR-0029 §2.5 ; seuil d'annexe B.39) : unités = hôtes de prm (un flux par hôte), classe
    journalisée égale à celle de prm, sinon ValueError ; ok(u, s) = fenêtres retenues de s dont la lecture last-wins a
    statut ok et un prix ; u retiré de s si ok(u, s) = 0 (D1 a, b) ou, seuil posé, si 2·ok(u, s) < n_s (égalité : u
    reste). Rend ({strate : [flux]}, [(strate, hôte, flux, ok, n_s, motif)])."""
    unites, seuil = prm["pool_d1bis"]["unites"], prm["pool_d1bis"]["seuil_presque_mort"]
    faux = [f for f in unites.values() if f not in d["params"]["pool"] or d["scf"].get(f) != prm["classes"].get(f)]
    if faux:
        raise ValueError(f"unité(s) D1-bis hors du pool journalisé ou de classe divergente : {faux} — fail-closed")
    n, ok = Counter(d["ws"].values()), Counter()
    for (ws, f), rd in d["rmap"].items():
        if ws in d["ws"] and rd.get("status") == "ok" and rd.get("price") is not None:
            ok[d["ws"][ws], f] += 1
    pools, retraits = {}, []
    for st in sorted(n):
        pools[st] = []
        for h, f in unites.items():
            motif = ("aucune lecture ok (D1 a, b)" if not ok[st, f] else
                     "2·ok < n_s (seuil de flux presque mort, B.39)" if seuil and 2 * ok[st, f] < n[st] else None)
            (retraits.append((st, h, f, ok[st, f], n[st], motif)) if motif else pools[st].append(f))
    return pools, retraits


def classer(d: dict, pools: dict) -> dict:
    """{strate : [(ws, {flux : Ecart}, {flux répondant : prix})]}, fenêtres retenues en ordre croissant, par
    r1._classify_window (σ et τ committés de S2, run_params) sur le pool de chaque strate : l'appel de compute_r1."""
    r1, rm, out = H["r1"], d["rmap"], {}
    for ws, st in sorted(d["ws"].items()):
        ps = pools[st]
        cls = r1._classify_window(ws, rm, ps, d["w"], d["sbc"], d["scf"], d["tau"], d["n_min"])
        rep = {f: Decimal(rm[ws, f]["price"]) for f in ps
               if (ws, f) in rm and rm[ws, f].get("status") == "ok" and rm[ws, f].get("price") is not None}
        out.setdefault(st, []).append((ws, cls, rep))
    return out


def lire_bloc3(chemin: str) -> dict:
    """{strate : (n, K, P̂_more en chaîne)} du premier bloc 3 d'un rendu (jusqu'à la ligne « [BLOC » suivante) : en-tête
    de strate, puis première ligne « P̂_more  = » (deux espaces) de la strate ; ligne de strate poolée non lue."""
    tete, pm, out, st, dedans = "  ── strate « ", "    P̂_more  = ", {}, None, False
    with open(chemin, encoding="utf-8") as f:
        for x in f.read().split(NL):
            if x.startswith("[BLOC "):
                if dedans:
                    break
                dedans = x.startswith("[BLOC 3]")
            elif dedans and x.startswith(tete) and " : n = " in x and " ; K = " in x:
                st, n_s = x[len(tete):].split(" »", 1)[0], int(x.split(" : n = ", 1)[1].split(" ", 1)[0])
                out[st] = [n_s, int(x.split(" ; K = ", 1)[1].split(" ", 1)[0]), None]
            elif dedans and x.startswith(pm) and st is not None and out[st][2] is None:
                out[st][2] = x[len(pm):]
    return {s: tuple(v) for s, v in out.items()}


def controle(d: dict, prm: dict, rendu: str) -> tuple:
    """(égal, lignes) : (n, K, P̂_more) recomptés par strate contre l'épingle du bloc 3 de prm, chaîne pour chaîne, puis
    le bloc 3 relu dans le rendu de sha256 épinglé. Strate absente d'un côté, sha ou bloc 3 différents : écart."""
    epingle = {s: tuple(v) for s, v in prm["rendu_j28"]["bloc3"].items()}
    sha_ok = sha256(rendu) == prm["rendu_j28"]["sha256"]
    relu = lire_bloc3(rendu) if sha_ok else None
    ok = sha_ok and relu == epingle and bool(epingle)
    etat = "non relu" if relu is None else "relu égal" if relu == epingle else "relu DIFFÉRENT"
    lignes = [f"rendu de contrôle {os.path.basename(rendu)} : sha256 {'égal à' if sha_ok else 'DIFFÉRENT de'} l'épingle ; "
              f"bloc 3 {etat} aux valeurs épinglées"]
    for st in sorted(set(epingle) | set(d["base"]["strates"])):
        b = d["base"]["strates"].get(st)
        nous = None if b is None else (b["n"], b["K"], dec(b["P_more"]))
        ok = ok and nous == epingle.get(st)
        lignes.append(f"contrôle de cohérence (bloc 3 du rendu J28) « {st} » : recompté (n, K, P̂_more) = {nous} ; épinglé "
                      f"= {epingle.get(st)} : {'égaux' if nous == epingle.get(st) else 'ÉCART'}")
    return ok, lignes


def executer(nom: str, items: str, analyse, argv=None) -> int:
    """CLI commune : --journaux, --harnais, --sortie (obligatoires), --parametres, --rendu (défaut : chemin de prm sous
    la racine du dépôt). Épingles du harnais, lecture, contrôle, puis analyse(d, prm) si égal (code 0), sinon une ligne
    de refus (code 1). Fichier écrit en entier ou pas du tout (voisin « .partiel », puis renommage)."""
    a = argparse.ArgumentParser(prog=nom)
    for o in ("--journaux", "--harnais", "--sortie"):
        a.add_argument(o, required=True)
    a.add_argument("--parametres", default=PARAMETRES)
    a.add_argument("--rendu")
    x = a.parse_args(argv)
    prm = lire_parametres(x.parametres)
    rendu = x.rendu or os.path.join(RACINE, prm["rendu_j28"]["chemin"])
    importer_harnais(x.harnais, prm["harnais_sha256"])
    d = charger(x.journaux, prm)
    ok, ctrl = controle(d, prm, rendu)
    script = sys.modules[analyse.__module__].__file__
    charges = [m.__file__ for m in list(sys.modules.values()) if getattr(m, "__file__", None)]
    lot = sorted({os.path.realpath(q) for q in charges if os.path.dirname(os.path.realpath(q)) == os.path.realpath(ICI)})
    tete = [f"{nom} — {items}",
            f"script {os.path.basename(script)} ; modules du lot chargés : " + " ; ".join(f"{os.path.basename(q)} sha256 "
            f"{sha256(q)}" for q in lot) + f" ; parametres.json sha256 {sha256(x.parametres)}",
            f"harnais : extraction du commit d'analyse {prm['commit_analyse']} ; modules épinglés : "
            + " ; ".join(f"{os.path.basename(k)} {v}" for k, v in prm["harnais_sha256"].items()),
            f"journaux : control.jsonl sha256 {sha256(d['control'])} ; journal.jsonl sha256 {sha256(d['journal'])}",
            f"portée : segment [{d['bornes'][0]} ; {d['bornes'][1]}) (t0 = {prm['segment']['t0']}, n fixe = "
            f"{prm['segment']['n_fixe']}), plages exclues {d['plages']}",
            "pool S2 (D1) : " + " ; ".join(f"« {s} » {len(v)} flux" for s, v in d["pools_s2"].items())
            + " ; retraits : " + (" ; ".join(f"« {s} » {f} (ok {k} sur {t} lectures)" for s, f, k, t, _n in d["retraits_s2"])
                                  or "aucun"),
            "pool D1-bis : " + " ; ".join(f"« {s} » {len(v)} hôtes" for s, v in d["pools_bis"].items()) + " ; retraits : "
            + (" ; ".join(f"« {s} » {h} ({f}, ok {k} sur n = {n}, {m})" for s, h, f, k, n, m in d["retraits_bis"])
               or "aucun")]
    corps = analyse(d, prm) if ok else ["contrôle de cohérence en ÉCART : aucune valeur d'analyse imprimée (fail-closed)"]
    with open(x.sortie + ".partiel", "w", encoding="utf-8", newline=NL) as f:
        f.write(NL.join([ETIQUETTE, *tete, *ctrl, *corps]) + NL)
    os.replace(x.sortie + ".partiel", x.sortie)
    return 0 if ok else 1
