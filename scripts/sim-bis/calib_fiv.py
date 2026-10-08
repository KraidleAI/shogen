"""Calibration E1 du groupement (G0 docs/adr-0029/g0-sim/G0-SIM-BIS.md ; sous-lot SB-10 ; E-S-38, E-S-39) : SB-10a :
estimateur FIV_série(ℓ) de la forme de PLAN-S2BIS (r1.block_long_run_variance de f35a70c, forme de r1.bloc_strate ;
scripts/plan-s2bis/episodes.py, courbe) sur masques entiers : bit j = position j de la grille de la strate, présente
ou non ; une position absente ne forme aucune paire. Numérateur entier exact, valeurs publiées en Decimal sous le
contexte de r1 (précision calibration.precision, ROUND_HALF_EVEN, le reste du DefaultContext), FIV exact en Fraction.
SB-10b : portée du segment J28 lue sur EP l.6, calendrier de la grille, réplication du modèle d'E1 (unités
indépendantes vues d'un seul observateur, f = 1, régime caché d'E-S-12), moyenne des courbes d'un point. SB-10c :
grille, critère (logarithmes par Decimal.ln, correctement arrondi, sous le contexte de r1 : aucune fonction de libm),
choix de C2 et de C1. SB-15b (ajout daté du G0 du 2026-10-05 15:05:43 UTC, point (3)) : calendrier d'E1, positions
présentes = masque mesuré de J28 versé par PLAN-S2BIS-2. Entiers et rationnels
seuls, sauf les logarithmes du critère : aucun flottant, aucune puissance."""
import hashlib
import re
from decimal import ROUND_HALF_EVEN, Context, Decimal
from fractions import Fraction

import calendrier
import calibration
import commun
import regle
import sources

NOMBRE = re.compile("(?<![a-z])[0-9]+")         # nombres d'EP l.6 (« t0 » exclu) et des lignes du masque
SECTION_MASQUE = ("[MASQUE J28] positions j = (ws − t0)/w de la portée ; strate par jour UTC ; retenue = fenêtre "
                  "retenue de la strate")
CONTROLE_MASQUE = ("  contrôle : retenues = n du bloc 3 ; sautées = ADR-0029 l.31 ; strate de chaque retenue = "
                   "calendrier : égaux")


def _entree(pres, val, ells) -> None:
    """Masques entiers ≥ 0 (booléen refusé), I_t ⊂ positions présentes, ℓ liste non vide d'entiers ≥ 1, sinon
    FIV/entree."""
    if not (type(pres) is int and type(val) is int and pres >= 0 and val >= 0 and not val & ~pres):
        raise commun.Refus("FIV/entree", f"masques {pres!r}, {val!r} : entiers ≥ 0, série dans les positions présentes")
    if type(ells) is not list or not ells or any(type(e) is not int or e < 1 for e in ells):
        raise commun.Refus("FIV/entree", f"ℓ = {ells!r} : liste non vide d'entiers ≥ 1")


def courbe(pres: int, val: int, ells: list, k: dict) -> list:
    """Par ℓ de `ells` (dans leur ordre), sur la série I (val) des positions présentes (pres) : n, K, numérateur
    N = ℓ·n²·σ̂²_bloc = ℓ·n·K(n − K) + Σ_{j=1}^{ℓ−1} 2(ℓ − j)·A_j, A_j = n²·C_j − n·K·(S_g + S_d) + M_j·K² (paires de
    lag j : M_j présentes aux deux bouts, C_j à 1 aux deux bouts, S_g à 1 au début, S_d à 1 à la fin ; r1 de f35a70c,
    formule de block_long_run_variance), calculé par sommes préfixes des A_j jusqu'au plus grand ℓ ; γ̂₀ = (nK − K²)/n
    et σ̂²_bloc = N/(ℓn²) en Decimal (une division chacun), FIV_serie = σ̂²_bloc/γ̂₀ (division des deux valeurs
    publiées, forme d'episodes.courbe) ; fiv = N/(ℓ·n·K(n − K)) exact ; garde = n ≥ garde_blocs·ℓ (k : section
    « calibration » de parametres.json). n = 0 : γ̂₀, σ̂² et FIV à None ; γ̂₀ = 0 (K ∈ {0, n}) : FIV à None."""
    _entree(pres, val, ells)
    ctx = contexte(k)
    n, K, voulus = pres.bit_count(), val.bit_count(), set(ells)
    sommes, a, b = {1: (0, 0)}, 0, 0
    for j in range(1, max(ells)):
        pj, vj = pres >> j, val >> j
        aj = (n * n * (val & vj).bit_count() + (pres & pj).bit_count() * K * K
              - n * K * ((val & pj).bit_count() + (pres & vj).bit_count()))
        a, b = a + aj, b + j * aj
        if j + 1 in voulus:
            sommes[j + 1] = (a, b)
    out = []
    for ell in ells:
        num = ell * (n * K * (n - K) + 2 * sommes[ell][0]) - 2 * sommes[ell][1]
        g0 = ctx.divide(Decimal(n * K - K * K), Decimal(n)) if n else None
        s2 = ctx.divide(Decimal(num), Decimal(ell * n * n)) if n else None
        defini = n and 0 < K < n
        out.append({"ell": ell, "n": n, "K": K, "numerateur": num, "gamma0": g0, "sigma2_bloc": s2,
                    "FIV_serie": ctx.divide(s2, g0) if defini else None,
                    "fiv": Fraction(num, ell * n * K * (n - K)) if defini else None,
                    "garde": n >= k["garde_blocs"] * ell})
    return out


def portee(texte: str, cal: dict) -> dict:
    """Portée du segment J28 de S2, lue sur EP l.6 (E-S-38 : « calendrier du segment J28 de S2, portée et plage D5
    d'EP l.6 ») : segment [t0 ; t_fin), n fixe, plages exclues [(a, b)]. Forme exigée : la ligne, réécrite depuis ses
    nombres sous la forme de scripts/plan-s2bis/commun.py (executer), lui est identique ; t0 répété, instants multiples
    du pas w, t0 < t_fin, a ≤ b ; sinon CALIB/forme."""
    lignes = texte.split(commun.NL)
    ligne = lignes[5] if len(lignes) > 5 else ""
    x = [int(y) for y in NOMBRE.findall(ligne)]
    plages, ok = list(zip(x[4::2], x[5::2])), len(x) >= 4 and len(x) % 2 == 0
    canon = ok and (f"portée : segment [{x[0]} ; {x[1]}) (t0 = {x[2]}, n fixe = {x[3]}), plages exclues ["
                    + ", ".join(f"({a}, {b})" for a, b in plages) + "]")
    if not (ok and ligne == canon and x[0] == x[2] < x[1] and all(a <= b for a, b in plages)
            and all(y % cal["w"] == 0 for y in x[:2] + x[4:])):
        raise commun.Refus("CALIB/forme", "EP l.6 : portée du segment J28 illisible")
    return {"t0": x[0], "t_fin": x[1], "n_fixe": x[3], "plages": plages}


def calendrier_j28(seg: dict, cal: dict) -> dict:
    """Grille de pas w sur [t0 ; t_fin) : position j = instant t0 + j·w ; strate de chaque journée UTC
    (calendrier.strate, réplique de window de f35a70c), jours partiels compris ; les positions des plages exclues,
    bornes incluses (forme de records.filtre_horodatage de f35a70c), ne sont dans aucune strate ; les fenêtres de S2
    non évaluables, inconnues d'EP, restent des positions (Q-T4-5 : limite écrite). Rend {"masques" : {strate :
    masque}, "horizon" : nombre de positions}."""
    w, t0, tf = cal["w"], seg["t0"], seg["t_fin"]
    out, t = {"calme": 0, "stress": 0}, t0
    while t < tf:
        b = min(tf, (t // 86400 + 1) * 86400)
        out[calendrier.strate(t, cal)] |= ((1 << ((b - t) // w)) - 1) << ((t - t0) // w)
        t = b
    for a, b in seg["plages"]:
        ja, jb = max(0, -(-(a - t0) // w)), min((tf - t0) // w - 1, (b - t0) // w)
        trou = ((1 << (jb - ja + 1)) - 1) << ja if ja <= jb else 0
        out = {s: x & ~trou for s, x in out.items()}
    return {"masques": out, "horizon": (tf - t0) // w}


def masque_j28(texte: str, seg: dict, cal: dict) -> dict:
    """Positions présentes d'E1 (point (3)) : masque des fenêtres évaluables de J28 versé par PLAN-S2BIS-2, section
    [MASQUE J28] de masque_j28.txt (forme de scripts/plan-s2bis-2/masque_fiv.py, lignes_masque), sur la grille de la
    portée `seg` d'EP l.6 : position non retenue ⇔ dans une lacune (suites maximales en ordre croissant, D5 comprise) ;
    strate de chaque position par le calendrier (calendrier_j28 sans plage). La section, réécrite depuis la portée, le
    calendrier et les bornes des lacunes, doit lui être identique jusqu'au saut de ligne final, empreinte comprise
    (sha256 de la chaîne c/s/- reconstruite) ; aucune retenue dans une plage exclue ; sinon E1/masque. Rend {strate :
    masque des positions présentes}."""
    lignes, w, t0 = texte.split(commun.NL), cal["w"], seg["t0"]
    plein, hors = calendrier_j28(dict(seg, plages=[]), cal), calendrier_j28(seg, cal)["masques"]
    n, m = plein["horizon"], plein["masques"]
    if lignes[0] != calibration.ETIQUETTE_EP or lignes.count(SECTION_MASQUE) != 1:
        raise commun.Refus("E1/masque", "masque_j28.txt : étiquette d'EP ou section [MASQUE J28] unique attendue")
    i = lignes.index(SECTION_MASQUE)
    lac = [[int(y) for y in NOMBRE.findall(x)][:2] for x in lignes[i + 5 + len(m):-1]]
    if not all(len(x) == 2 and x[0] <= x[1] < n for x in lac) or any(a[1] + 1 >= b[0] for a, b in zip(lac, lac[1:])):
        raise commun.Refus("E1/masque", "lacunes hors de la grille, chevauchantes, contiguës ou désordonnées")
    trou = sum(((1 << (b - a + 1)) - 1) << a for a, b in lac)
    pres = {s: x & ~trou for s, x in m.items()}
    bits = {s: format(x, "b")[::-1].ljust(n, "0") for s, x in pres.items()}
    chaine = "".join(next((s[0] for s in pres if bits[s][j] == "1"), "-") for j in range(n))
    jp = [(max(0, -(-(a - t0) // w)), min(n - 1, (b - t0) // w)) for a, b in seg["plages"]]
    d5 = " ; ".join(f"j = {a} à {b} ({b - a + 1} positions)" if a <= b else "aucune position" for a, b in jp)
    canon = [SECTION_MASQUE, f"  portée : t0 = {t0} ; t_fin = {seg['t_fin']} ; positions = {n} ; plage D5 : "
             + (d5 or "aucune")]
    canon += [f"  « {s} » : calendrier hors D5 = {hors[s].bit_count()} ; retenues = {x.bit_count()} ; sautées hors "
              f"D5 = {hors[s].bit_count() - x.bit_count()}" for s, x in pres.items()]
    canon += [CONTROLE_MASQUE, f"  empreinte : sha256 de la chaîne de {n} caractères (c calme retenue, s stress "
              f"retenue, - non retenue) = {hashlib.sha256(chaine.encode('ascii')).hexdigest()}", f"  lacunes : "
              f"{len(lac)} suites maximales de positions non retenues, plage D5 comprise, en ordre croissant"]
    canon += [f"  lacune j = {a} à {b} : {b - a + 1} positions ("
              + ", ".join(f"{s} {(x >> a & ((1 << (b - a + 1)) - 1)).bit_count()}" for s, x in m.items()) + ")"
              for a, b in lac]
    if lignes[i:] != canon + [""] or any(x & ~hors[s] for s, x in pres.items()):
        raise commun.Refus("E1/masque", "section [MASQUE J28] différente de sa réécriture, ou retenue dans une plage "
                                        "exclue")
    return pres


def calendrier_e1(prm: dict, lus=None, environ=None) -> dict:
    """Calendrier d'E1 pour C0, C1 et C2 (point (3)) : génération sur la grille de la portée d'EP l.6 hors D5
    (calendrier_j28) ; positions présentes : masque mesuré (masque_j28), lu sous ses deux épingles (parametres.json,
    puis le SHA256SUMS de PLAN-S2BIS-2, sommes_plan2). Rend {"masques", "horizon", "presentes"}."""
    seg = portee(commun.lire_entree(prm, "episodes", lus, environ).decode("utf-8"), prm["calendrier"])
    texte = commun.lire_entree(prm, "masque_j28", lus, environ, sommes="sommes_plan2").decode("utf-8")
    return dict(calendrier_j28(seg, prm["calendrier"]), presentes=masque_j28(texte, seg, prm["calendrier"]))


def replication(prm: dict, ep: dict, cal: dict, point, cellule: str, i: int) -> dict:
    """Une réplication d'E1 (E-S-38) : unités indépendantes vues d'un seul observateur (aucun observateur simulé),
    régime `point` = (φ, κ, τ_D), ou None (C0), dans chaque strate ; composition du fond lue dans la section e1.fond de
    parametres.json (C-1 de la G2 de la tranche 4 ; Q-T4-13 : f = 1, ni pannes longues, ni hors-enveloppe, classe BTC) :
    f, part des pannes longues, multiplicateur hors de BTC, part hors-enveloppe, classe ; ni dérive, ni incident, ni
    unité faible (clés absentes du fond de sources.Replication ; flux de la cellule `cellule`, réplication i) ; classe
    hors de sources.classes : E1/classe ; état D*(u) = H(u) ∪ F(u, classe) de chaque hôte du pool de la classe (BTC :
    pool D1-bis, calibration.unites) ; I_t = 1 si au moins deux hôtes sont en écart (regle.deux), sur les positions de
    chaque strate. Rend {"strates" : {s : (positions, I)}, "etats" : {hôte : D*}}."""
    e, cl = prm["e1"]["fond"], sources.classes(prm)
    if e["classe"] not in [x for x, _p in cl]:
        raise commun.Refus("E1/classe", f"{e['classe']!r} : classe de sources.classes attendue")
    c = [x for x, _p in cl].index(e["classe"])
    fond = {"f": Fraction(*e["f"]), "regime": {s: point for s in cal["masques"]}, "longues": Fraction(*e["longues"]),
            "autres": Fraction(*e["autres"]), "hors_enveloppe": Fraction(*e["hors_enveloppe"])}
    rep = sources.Replication(prm, ep, fond, cellule, i, cal["masques"], cal["horizon"])
    etats = {h: rep.pannes(h) | rep.ecarts(h, c) for h in cl[c][1]}
    i_t = regle.deux(list(etats.values()))
    return {"strates": {s: (m, i_t & m) for s, m in cal["masques"].items()}, "etats": etats}


def moyenne(courbes: list) -> dict:
    """Courbe d'un point d'E1 sur ses réplications (courbes de courbe(), mêmes ℓ) : par ℓ, moyenne exacte des FIV
    définis ; une réplication à FIV indéfini (K ∈ {0, n}, indéfini à tout ℓ) est comptée à part (Q-T4-6) ; aucune
    définie : None ; liste vide : FIV/entree."""
    if not courbes:
        raise commun.Refus("FIV/entree", "aucune courbe")
    definies = [c for c in courbes if c[0]["fiv"] is not None]
    nb = len(definies)
    fiv = [sum((c[j]["fiv"] for c in definies), Fraction(0)) / nb if nb else None for j in range(len(courbes[0]))]
    return {"fiv": fiv, "definies": nb, "indefinies": len(courbes) - nb}


def contexte(k: dict) -> Context:
    """Contexte décimal de r1 de f35a70c : précision calibration.precision, ROUND_HALF_EVEN, le reste du
    DefaultContext."""
    return Context(prec=k["precision"], rounding=ROUND_HALF_EVEN)


def grille(prm: dict) -> list:
    """Points (φ, κ, τ_D) de la grille d'E1 (E-S-38, section « e1 »), dans l'ordre φ, puis κ, puis τ_D."""
    e = prm["e1"]
    return [(Fraction(*f), Fraction(k), t) for f in e["phi"] for k in e["kappa"] for t in e["tau_D"]]


def cellule(prm: dict, point) -> str:
    """Nom de cellule des flux d'une réplication d'E1 (Q-T4-8, forme modifiée par l'avis : aucun « / », le nom
    nommant aussi les fichiers partiels de calcul, E-S-45) : « <préfixe>-C0-v2 » (C0 renommée avant E0, nom jamais
    employé : E-4, valeurs de E1-C0 possiblement vues en mise au point), ou « <préfixe>-<num>_<den>-<κ>-<τ_D> »,
    φ = num/den en fraction irréductible."""
    if point is None:
        return f"{prm['e1']['cellule']}-C0-v2"
    return f"{prm['e1']['cellule']}-{point[0].numerator}_{point[0].denominator}-{point[1]}-{point[2]}"


def _ln(x, ctx) -> Decimal:
    """ln x, x rationnel > 0 : quotient décimal puis Decimal.ln, tous deux sous le contexte (Q-T4-7)."""
    x = Fraction(x)
    return ctx.divide(Decimal(x.numerator), Decimal(x.denominator)).ln(ctx)


def critere(modele: list, cible: list, ells: list, ctx):
    """Critère d'E1 (E-S-38) : Σ (ln F_modèle(ℓ) − ln F_EP(ℓ))² aux ℓ dont la garde d'EP est tenue ; ℓ de la cible
    (points d'EP) égaux à `ells` dans l'ordre et autant de valeurs du modèle, sinon E1/cible ; FIV du modèle
    indéfini à un ℓ gardé : None (point écarté, Q-T4-10)."""
    if [c["ell"] for c in cible] != ells or len(modele) != len(ells):
        raise commun.Refus("E1/cible", f"ℓ de la cible {[c['ell'] for c in cible]}, attendus {ells}")
    s = Decimal(0)
    for x, c in zip(modele, cible):
        if c["garde"] and x is None:
            return None
        if c["garde"]:
            d = ctx.subtract(_ln(x, ctx), _ln(c["fiv"], ctx))
            s = ctx.add(s, ctx.multiply(d, d))
    return s


def _rang(item) -> tuple:
    """Ordre de choix : valeur, puis plus petit κ, puis plus petit τ_D (E-S-38), puis plus petit φ (Q-T4-9)."""
    v, (phi, kappa, tau) = item
    return v, kappa, tau, phi


def selection(prm: dict, cible: dict, moyennes: dict) -> dict:
    """C2 et C1 de chaque strate (E-S-38) : cible = {strate : points d'EP du pool e1.pool} ; moyennes = {point de la
    grille, ou None pour C0 : {strate : moyenne()}}. C2 = point de critère minimal ; C1 = point de la grille dont
    ln FIV(ell_c1) est le plus proche de la moyenne des ln FIV(ell_c1) de C0 et de C2, C2 compris (lettre d'E-S-38) ;
    égalités : _rang. Rend {strate : {"C2", "C1", "criteres" : {point : critère}, "residus" : ln F_C2(ℓ) − ln F_EP(ℓ)
    aux ℓ gardés}}. ell_c1 absent de calibration.ell : E1/ell ; point absent, C0 compris : E1/point ; strate de la cible
    sans courbe pour un point ou pour C0 : E1/strate (O-7 de la G2 de la tranche 4) ; aucun critère défini, ou
    FIV(ell_c1) de C0 ou de C2 indéfini : E1/indefini."""
    ctx, ells, pts = contexte(prm["calibration"]), prm["calibration"]["ell"], grille(prm)
    if prm["e1"]["ell_c1"] not in ells:
        raise commun.Refus("E1/ell", f"ell_c1 = {prm['e1']['ell_c1']!r} absent de calibration.ell")
    j, out = ells.index(prm["e1"]["ell_c1"]), {}
    if any(p not in moyennes for p in [None] + pts):
        raise commun.Refus("E1/point", "point de la grille ou C0 sans courbe")
    if any(s not in moyennes[p] for p in [None] + pts for s in cible):
        raise commun.Refus("E1/strate", "strate de la cible sans courbe pour un point de la grille ou pour C0")
    for s, cs in cible.items():
        crit = {p: critere(moyennes[p][s]["fiv"], cs, ells, ctx) for p in pts}
        defs = [(v, p) for p, v in crit.items() if v is not None]
        c2 = min(defs, key=_rang)[1] if defs else None
        f0, f2 = moyennes[None][s]["fiv"][j], None if c2 is None else moyennes[c2][s]["fiv"][j]
        if f0 is None or f2 is None:
            raise commun.Refus("E1/indefini", f"strate {s} : critère ou FIV({ells[j]}) indéfini")
        mil = ctx.divide(ctx.add(_ln(f0, ctx), _ln(f2, ctx)), 2)
        dist = [(ctx.subtract(_ln(moyennes[p][s]["fiv"][j], ctx), mil).copy_abs(), p) for p in pts
                if moyennes[p][s]["fiv"][j] is not None]
        out[s] = {"C2": c2, "C1": min(dist, key=_rang)[1], "criteres": crit,
                  "residus": [ctx.subtract(_ln(x, ctx), _ln(c["fiv"], ctx))
                              for x, c in zip(moyennes[c2][s]["fiv"], cs) if c["garde"]]}
    return out
