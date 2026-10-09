"""Exécution du lot SIM-BIS (G0 docs/adr-0029/g0-sim/G0-SIM-BIS.md : PROPOSITION corrigée par AVIS, ajouts datés compris
; sous-lot SB-11 ; E-S-40 à E-S-48, E-S-52). SB-11a : taux d'une cellule (x sur R réplications, r̂ exact, erreur-type en
Decimal sous le contexte de r1, borne unilatérale à 95 % quand x = 0 ; E-S-40, E-S-43) ; fréquences des valeurs et des
causes de NON ÉVALUABLE, par cause et par combinaison (E-S-52). SB-11b : empreinte d'une suite d'enregistrements
(E-S-44) ; fichiers partiels de lot, un par (cellule, plage de i), relus à la condition que chaque i y soit une fois et
une seule (E-S-45, E-S-06). SB-11c : tâches dans l'ordre, en un ou plusieurs processus (E-S-42) ; plan de lots de 90 min
au plus sur le coût mesuré (adjudication 6 du G0). SB-11d : couche d'observateurs d'une cellule (grille
cellules.couches, O-5 ; perte sur le W de la cellule, L-2). SB-11e : cellules sous schéma fermé et refus nommés
(SHOGEN-SIM-BIS-SB11-IMPRESSIONS-1 ; O-1 de la G2 de la tranche 2) ; fond des sources d'une cellule. Entiers, rationnels
et Decimal seuls : aucun flottant, aucune puissance, aucune fonction de libm."""
import hashlib
import json
import multiprocessing
import os
import re
from decimal import Decimal
from fractions import Fraction

import calib_fiv
import commun
import observateurs
import regle
import sources

VALEURS = ("REJETTE", "NE REJETTE PAS", "NON ÉVALUABLE")
INSUFFISANTE = ("unites", "k_crit", "runs")         # information insuffisante (E-S-52) ; n_prime compté à part
NOM, SUFFIXE = re.compile("[A-Za-z0-9_-]+"), ".lot"  # nom de cellule sans « / » ni « . » (Q-T4-8) ; jamais .jsonl
BORNE = 90 * 60 * 1000000000                         # 90 min en ns : adjudication 6 du G0 (lots détachés)


def taux(x: int, R: int, k: dict) -> dict:
    """E-S-40 : x sur R réplications : r̂ = x/R exact ; SE = √(r̂(1 − r̂)/R) = √(x(R − x)/R³), une division puis une
    racine sous le contexte de r1 (calib_fiv.contexte de la section « calibration » : précision 50, ROUND_HALF_EVEN) ;
    borne unilatérale à 95 % 1 − 0,05^(1/R) quand x = 0, soit 1 − exp(ln(1/20)/R) par Decimal.ln et Decimal.exp sous
    le même contexte (aucune fonction de libm, E-S-43), None sinon. x, R entiers, 0 ≤ x ≤ R, R ≥ 1, sinon EXEC/taux."""
    if type(x) is not int or type(R) is not int or not 0 <= x <= R or R < 1:
        raise commun.Refus("EXEC/taux", f"x = {x!r}, R = {R!r} : entiers, 0 ≤ x ≤ R, R ≥ 1")
    ctx = calib_fiv.contexte(k)
    se = ctx.sqrt(ctx.divide(Decimal(x * (R - x)), Decimal(R * R * R)))
    borne = None
    if x == 0:
        ln = ctx.ln(ctx.divide(Decimal(1), Decimal(20)))
        borne = ctx.subtract(Decimal(1), ctx.exp(ctx.divide(ln, Decimal(R))))
    return {"x": x, "R": R, "r": Fraction(x, R), "SE": se, "borne": borne}


def frequences(resultats: list) -> dict:
    """E-S-52 (et AVIS-SIM-T3, observation 3) : sur les résultats d'une classe dans une strate ({"valeur", "causes"}
    par réplication), comptes par valeur, par cause de NON ÉVALUABLE (non exclusives, ordre de regle.CAUSES),
    information insuffisante (au moins une cause parmi unites, k_crit, runs) et par combinaison de causes (jointes par
    « + » dans l'ordre de regle.CAUSES ; les combinaisons somment au compte de NON ÉVALUABLE). Valeur hors de VALEURS,
    causes hors de regle.CAUSES, dans le désordre ou en double, NON ÉVALUABLE sans cause, valeur évaluée avec une
    cause : EXEC/frequences."""
    out = {"valeurs": dict.fromkeys(VALEURS, 0), "causes": dict.fromkeys(regle.CAUSES, 0), "insuffisante": 0,
           "combinaisons": {}}
    for x in resultats:
        v, c = x.get("valeur"), x.get("causes")
        if (v not in VALEURS or type(c) is not list or c != [y for y in regle.CAUSES if y in c]
                or (v == VALEURS[2]) != bool(c)):
            raise commun.Refus("EXEC/frequences", f"valeur {v!r}, causes {c!r}")
        out["valeurs"][v] += 1
        for y in c:
            out["causes"][y] += 1
        if c:
            out["insuffisante"] += any(y in INSUFFISANTE for y in c)
            cle = "+".join(c)
            out["combinaisons"][cle] = out["combinaisons"].get(cle, 0) + 1
    return out


def jsonable(x):
    """Valeur pour commun.json_canonique : Fraction en « num/den » (str), Decimal en chaîne, tuple en liste, dict à
    clés textuelles (sinon EXEC/cle), le reste tel quel (un flottant y est refusé ensuite, SORTIE/flottant)."""
    if type(x) in (Fraction, Decimal):
        return str(x)
    if type(x) in (list, tuple):
        return [jsonable(y) for y in x]
    if type(x) is dict:
        if any(type(k) is not str for k in x):
            raise commun.Refus("EXEC/cle", f"clés {sorted(map(repr, x))!r} : textes attendus")
        return {k: jsonable(v) for k, v in x.items()}
    return x


def empreinte(enregistrements: list) -> str:
    """E-S-44 : sha256 de la suite ordonnée des enregistrements par réplication, chacun en JSON canonique d'une ligne
    (commun.json_canonique de jsonable, saut de ligne final)."""
    h = hashlib.sha256()
    for e in enregistrements:
        h.update(commun.json_canonique(jsonable(e)))
    return h.hexdigest()


def nom_lot(cellule: str, a: int, b: int) -> str:
    """« <cellule>.<a>-<b>.lot » (a et b sur six chiffres) : cellule de NOM, 0 ≤ a < b entiers, sinon LOT/nom."""
    if not (type(cellule) is str and NOM.fullmatch(cellule) and type(a) is int and type(b) is int and 0 <= a < b):
        raise commun.Refus("LOT/nom", f"{cellule!r}, [{a!r}, {b!r}) : lettres, chiffres, « - », « _ » ; 0 ≤ a < b")
    return f"{cellule}.{a:06d}-{b:06d}{SUFFIXE}"


def ecrire_lot(dossier: str, cellule: str, a: int, b: int, enregistrements: list, entete: list) -> tuple:
    """Fichier partiel du lot (cellule, [a, b)) (E-S-45, E-S-06) : l'étiquette (E-S-05), puis le JSON canonique de
    {cellule, debut, fin, entete, empreinte, enregistrements}, l'enregistrement k portant i = a + k (sinon
    LOT/indices) ; écrit par commun.ecrire (atomique, jamais par-dessus) ; rend (chemin, sha256 des octets, à consigner
    au journal d'exécution). Un lot perdu, refait, redonne les mêmes octets (graines par réplication)."""
    nom, recs = nom_lot(cellule, a, b), [jsonable(e) for e in enregistrements]
    if [type(e) is dict and e.get("i") for e in recs] != list(range(a, b)):
        raise commun.Refus("LOT/indices", f"{cellule} [{a}, {b}) : i des enregistrements différents de la plage")
    contenu = {"cellule": cellule, "debut": a, "fin": b, "entete": jsonable(entete), "empreinte": empreinte(recs),
               "enregistrements": recs}
    octets = (commun.ETIQUETTE + commun.NL).encode("utf-8") + commun.json_canonique(contenu)
    chemin = os.path.join(dossier, nom)
    commun.ecrire(chemin, octets)
    return chemin, hashlib.sha256(octets).hexdigest()


def _lot(chemin: str, cellule: str, entete: list) -> dict:
    """Contenu d'un fichier de lot contrôlé : étiquette, JSON canonique relu égal, cellule, plage, i, empreinte
    recalculée (LOT/forme) ; entête égale à `entete` (LOT/entete)."""
    with open(chemin, "rb") as f:
        tete, _nl, corps = f.read().partition(commun.NL.encode("utf-8"))
    try:
        c = json.loads(corps.decode("utf-8"))
        ok = (tete.decode("utf-8") == commun.ETIQUETTE and commun.json_canonique(c) == corps
              and os.path.basename(chemin) == nom_lot(c["cellule"], c["debut"], c["fin"]) and c["cellule"] == cellule
              and [e["i"] for e in c["enregistrements"]] == list(range(c["debut"], c["fin"]))
              and empreinte(c["enregistrements"]) == c["empreinte"])
    except (ValueError, TypeError, KeyError, commun.Refus):
        ok = False
    if not ok:
        raise commun.Refus("LOT/forme", os.path.basename(chemin))
    if c["entete"] != jsonable(entete):
        raise commun.Refus("LOT/entete", f"{os.path.basename(chemin)} : autres modules ou entrées")
    return c


def lire_lots(dossier: str, cellule: str, R_rep: int, entete: list) -> list:
    """Enregistrements des réplications 0 à R_rep − 1 de la cellule, dans l'ordre, depuis ses fichiers de lot
    (« <cellule>. », suffixe .lot ; _lot) : chaque i une fois et une seule (E-S-45) ; un i manquant : LOT/manquant
    (un lot interrompu n'a pas de fichier : il se refait, jamais compté) ; un i deux fois : LOT/double ; au-delà de
    R_rep : LOT/surplus."""
    noms = sorted(f for f in os.listdir(dossier) if f.startswith(cellule + ".") and f.endswith(SUFFIXE))
    lots, i = sorted((_lot(os.path.join(dossier, f), cellule, entete) for f in noms), key=lambda c: c["debut"]), 0
    for c in lots:
        if c["debut"] != i:
            code = "LOT/double" if c["debut"] < i else "LOT/manquant"
            raise commun.Refus(code, f"{cellule} : i = {min(i, c['debut'])}")
        i = c["fin"]
    if i != R_rep:
        raise commun.Refus("LOT/manquant" if i < R_rep else "LOT/surplus", f"{cellule} : {i} réplications pour {R_rep}")
    return [e for c in lots for e in c["enregistrements"]]


def appliquer(fonction, taches: list, processus: int) -> list:
    """[fonction(*t) pour t de taches], dans l'ordre des tâches (E-S-42) : en ce processus si processus = 1, sinon
    par `processus` processus neufs (méthode « spawn »), starmap ordonné : le résultat ne dépend ni du nombre de
    processus ni de l'ordre d'achèvement. processus entier ≥ 1, sinon EXEC/processus."""
    if type(processus) is not int or processus < 1:
        raise commun.Refus("EXEC/processus", f"{processus!r} : entier ≥ 1")
    if processus == 1:
        return [fonction(*t) for t in taches]
    with multiprocessing.get_context("spawn").Pool(processus) as p:
        out = p.starmap(fonction, taches, chunksize=1)
        p.close()
        p.join()
    return out


def plan(R_rep: int, ns: int, processus: int, borne: int = BORNE) -> list:
    """Plages [(a, b)] de [0, R_rep), dans l'ordre, de T = borne·processus // ns réplications (la dernière au plus) :
    durée d'un lot (b − a)·ns/processus ≤ borne, sur le coût mesuré ns par réplication (en ns ; adjudication 6 du G0,
    90 min ; SHOGEN-SIM-BIS-C1-COUT-1) ; une réplication plus longue que la borne : EXEC/plan."""
    if not all(type(v) is int and v >= 1 for v in (R_rep, ns, processus, borne)) or ns > borne:
        raise commun.Refus("EXEC/plan", f"R = {R_rep!r}, {ns!r} ns par réplication, borne {borne!r} ns")
    t = borne * processus // ns
    return [(a, min(a + t, R_rep)) for a in range(0, R_rep, t)]


CLES = ("nom", "niveau", "f", "longues", "autres", "hors_enveloppe", "derive", "incidents", "faibles", "couche",
        "regle", "surcharges")
COUCHE = ("grille", "repli", "chemin", "local", "artefacts", "regionale", "manque")
REGLE = ("R", "classes", "S", "variante", "evenements", "absorption")
INCIDENT = {"chacun": ("rho", "duree", "geometrique", "mode", "population", "p"),
            "parmi": ("rho", "duree", "geometrique", "mode", "population", "k", "imposes")}


def _q(v, haut=1, ouvert=False):
    """Fraction de [num, den] entiers (den > 0, booléens refusés), de valeur dans [0, haut] (haut exclu si ouvert ;
    haut None : sans borne), sinon None."""
    if not (type(v) is list and len(v) == 2 and all(type(x) is int for x in v) and v[1] > 0):
        return None
    x = Fraction(*v)
    return x if 0 <= x and (haut is None or (x < haut if ouvert else x <= haut)) else None


def _population(prm: dict, nom: str) -> list:
    """« pool » : les hôtes du pool BTC D1-bis (calibration.unites) ; « as13335 » : sources.as13335."""
    return [h for h, _f in prm["calibration"]["unites"]] if nom == "pool" else list(prm["sources"]["as13335"])


def _schema(prm: dict, c: dict) -> bool:
    """Clés exactes, types et domaines d'une cellule (CELLULE/schema) ; toute entrée malformée rend False."""
    try:
        co, rg, fa, inc, sur = c["couche"], c["regle"], c["faibles"], c["incidents"], c["surcharges"]
        v, cl = prm["variante"], rg["classes"]
        return bool(sorted(c) == sorted(CLES) and NOM.fullmatch(c["nom"]) and c["niveau"] in ("C0", "C1", "C2")
                    and _q(c["f"]) and _q(c["longues"], 1, True) is not None and _q(c["autres"], None) is not None
                    and _q(c["hors_enveloppe"], 1, True) is not None and type(sur) is dict
                    and (c["derive"] is None or type(c["derive"]) is list and set(c["derive"]) <= set(sources.GENRES))
                    and sorted(co) == sorted(COUCHE) and sorted(rg) == sorted(REGLE)
                    and rg["R"] in (prm["regle"]["R"], prm["regle"]["R_approche"]) and type(cl) is list
                    and cl == [x for x in sources.CLASSES if x in cl] and cl[0] == "BTC"
                    and type(rg["S"]) is bool and type(rg["absorption"]) is bool and commun.naturel(rg["evenements"])
                    and type(rg["variante"]) is list and set(rg["variante"]) <= {v["diviseur"], v["sensibilite"]}
                    and (fa is None or sorted(fa) == ["L", "k", "p", "type"] and fa["type"] in ("panne", "ecart"))
                    and (inc is None or type(inc) is dict))
    except (TypeError, KeyError, AttributeError, IndexError):
        return False


def _valider(prm: dict, c: dict) -> None:
    """Schéma fermé d'une cellule, puis refus nommés (voir cellule)."""
    def non(code):
        raise commun.Refus(code, f"cellule {c.get('nom') if type(c) is dict else c!r}")
    if not _schema(prm, c):
        non("CELLULE/schema")
    co, fa, inc, sur = c["couche"], c["faibles"], c["incidents"], c["surcharges"]
    ch, cle = co["chemin"], {"reference": "facteur", "fixe": "epsilon"}
    if (co["grille"] not in prm["cellules"]["couches"] or type(co["repli"]) is not bool or type(ch) is not dict
            or sorted(ch) != sorted(["mode", cle.get(ch.get("mode"), "mode")]) or _q(ch[cle[ch["mode"]]]) is None
            or any(co[k] is not None and _q(co[k]) is None for k in ("local", "artefacts"))
            or _q(co["regionale"]) is None or _q(co["manque"]) is None):
        non("CELLULE/couche")
    pop = prm["sources"][prm["sources"]["absorption"]["population"]]
    if fa is not None:
        if _q(fa["p"], 1, True) is None:
            non("CELLULE/faible-p")
        if type(fa["L"]) is not int or fa["L"] < 1:
            non("CELLULE/faible-L")
        if type(fa["k"]) is not int or not 1 <= fa["k"] <= len(pop):
            non("CELLULE/faible-k")
    if inc is not None:
        if inc.get("mode") not in INCIDENT:
            non("CELLULE/incident-mode")
        if not _q(inc.get("rho"), None):
            non("CELLULE/rho")
        if type(inc.get("duree")) is not int or inc["duree"] < 1:
            non("CELLULE/incident-duree")
        if (sorted(inc) != sorted(INCIDENT[inc["mode"]]) or type(inc["geometrique"]) is not bool
                or inc["population"] not in ("pool", "as13335") or (inc["mode"] == "chacun" and _q(inc["p"]) is None)
                or (inc["mode"] == "parmi" and not (type(inc["k"]) is int and 1 <= inc["k"] <= len(_population(
                    prm, inc["population"])) and inc["imposes"] in ("aucun", "faibles" if fa else "aucun")))):
            non("CELLULE/schema")
    if sur and not (sorted(sur) == ["longues", "poids_longues"] and len(sur["longues"]) == len(sur["poids_longues"])
                    and all(commun.positif(x) for x in sur["longues"] + sur["poids_longues"])):
        non("CELLULE/longues")


def fond(prm: dict, cel: dict, points: dict, W: int) -> dict:
    """Fond de sources.Replication d'une cellule validée : f ; régime de chaque strate au niveau de la cellule (C0 :
    aucun ; C1, C2 : point d'E1 de la strate, points = {niveau : {strate : (φ, κ, τ_D)}}, sinon CELLULE/niveau) ; part
    des pannes longues, autres, hors-enveloppe ; dérive sur la durée nominale W·tendance_par_semaine (E-S-13 ; W entier
    ≥ 1, sinon CELLULE/duree, durée nulle) ; incidents, hôtes au mode de sources.touches (E-S-15) ; unités faibles :
    les k premiers hôtes de sources.absorption.population (E-S-16, Q-T2-10), partenaire imposé parmi elles."""
    if type(W) is not int or W < 1:
        raise commun.Refus("CELLULE/duree", f"W = {W!r} : entier ≥ 1")
    st, n, fa, inc = prm["calibration"]["strates"], cel["niveau"], cel["faibles"], cel["incidents"]
    if n != "C0" and sorted(points.get(n, {})) != sorted(st):
        raise commun.Refus("CELLULE/niveau", f"{cel['nom']} : {n} sans point d'E1 pour chaque strate")
    hf = fa and prm["sources"][prm["sources"]["absorption"]["population"]][:fa["k"]]
    out = {"f": Fraction(*cel["f"]), "regime": {s: None if n == "C0" else points[n][s] for s in st},
           "longues": Fraction(*cel["longues"]), "autres": Fraction(*cel["autres"]),
           "hors_enveloppe": Fraction(*cel["hors_enveloppe"]), "incidents": None,
           "derive": cel["derive"] and {"genres": list(cel["derive"]),
                                        "duree": W * prm["sources"]["derive"]["tendance_par_semaine"]},
           "faibles": fa and {"hotes": hf, "p": Fraction(*fa["p"]), "L": fa["L"], "type": fa["type"]}}
    if inc is not None:
        p = _population(prm, inc["population"])
        h = (("chacun", p, Fraction(*inc["p"])) if inc["mode"] == "chacun"
             else ("parmi", p, inc["k"], hf if inc["imposes"] == "faibles" else []))
        out["incidents"] = {"rho": Fraction(*inc["rho"]), "duree": inc["duree"], "geometrique": inc["geometrique"],
                            "hotes": h}
    return out


def couche(prm: dict, ep: dict, cel: dict, W: int) -> dict:
    """Couche d'observateurs.Couche d'une cellule validée : grille cellules.couches[grille] de parametres.json (O-5) ;
    perte tirée sur la durée nominale W de la cellule, celle passée à calendrier.echelle, jamais sur T_max (L-2 ;
    Q-T3-7) ; chemin : référence (1 − f)·p̂ (observateurs.chemin_reference, Q-S-12) × facteur, ou ε fixe ; repli,
    pannes régionales et manques de la cellule ; défaut local et artefacts : ceux de la cellule, ou, à None, ceux de
    la grille."""
    c, g, unites = cel["couche"], prm["cellules"]["couches"][cel["couche"]["grille"]], prm["calibration"]["unites"]
    if c["chemin"]["mode"] == "fixe":
        eps = {(h, s): Fraction(*c["chemin"]["epsilon"]) for h, _f in unites for s in prm["calibration"]["strates"]}
    else:
        ref = observateurs.chemin_reference(prm, ep, Fraction(*cel["f"]))
        eps = {k: x * Fraction(*c["chemin"]["facteur"]) for k, x in ref.items()}
    return {"absences": Fraction(*g["absences"]), "degradations": Fraction(*g["degradations"]),
            "paires": Fraction(*g["paires"]), "perte": W if g["perte"] else None, "repli": c["repli"], "chemin": eps,
            "local": Fraction(*(c["local"] or g["local"])), "artefacts": Fraction(*(c["artefacts"] or g["artefacts"])),
            "regionale": Fraction(*c["regionale"]), "manque": Fraction(*c["manque"])}


def cellule(prm: dict, ep: dict, cel: dict, points: dict, W: int) -> dict:
    """Cellule sous schéma fermé (SHOGEN-SIM-BIS-SB11-IMPRESSIONS-1 ; O-1 de la G2 de la tranche 2), puis ses entrées :
    {"nom", "prm" (surcharges de sources.longues et sources.poids_longues appliquées à une copie), "fond", "couche",
    "regle"}. Refus nommés : clés, types et domaines (CELLULE/schema) ; grille, chemin et taux de la couche
    (CELLULE/couche) ; unité faible à p ≥ 1 (CELLULE/faible-p), à L < 1 (CELLULE/faible-L), à k hors de 1..|population|
    (CELLULE/faible-k) ; incident de mode inconnu (CELLULE/incident-mode), à ρ nul (CELLULE/rho), de durée nulle
    (CELLULE/incident-duree) ; surcharge de longues sans poids_longues, ou l'inverse (CELLULE/longues) ; W nul
    (CELLULE/duree) ; niveau sans point d'E1 (CELLULE/niveau)."""
    _valider(prm, cel)
    p = dict(prm, sources=dict(prm["sources"], **cel["surcharges"]))
    return {"nom": cel["nom"], "prm": p, "fond": fond(p, cel, points, W), "couche": couche(p, ep, cel, W),
            "regle": cel["regle"]}
