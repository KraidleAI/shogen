"""Exécution du lot SIM-BIS (G0 docs/adr-0029/g0-sim/G0-SIM-BIS.md : PROPOSITION corrigée par AVIS, ajouts datés compris
; sous-lot SB-11 ; E-S-40 à E-S-48, E-S-52). SB-11a : taux d'une cellule (x sur R réplications, r̂ exact, erreur-type en
Decimal sous le contexte de r1, borne unilatérale à 95 % quand x = 0 ; E-S-40, E-S-43) ; fréquences des valeurs et des
causes de NON ÉVALUABLE, par cause et par combinaison (E-S-52). SB-11b : empreinte d'une suite d'enregistrements
(E-S-44) ; fichiers partiels de lot, un par (cellule, plage de i), relus à la condition que chaque i y soit une fois et
une seule (E-S-45, E-S-06). Entiers, rationnels et Decimal seuls : aucun flottant, aucune puissance, aucune fonction de
libm."""
import hashlib
import json
import os
import re
from decimal import Decimal
from fractions import Fraction

import calib_fiv
import commun
import regle

VALEURS = ("REJETTE", "NE REJETTE PAS", "NON ÉVALUABLE")
INSUFFISANTE = ("unites", "k_crit", "runs")         # information insuffisante (E-S-52) ; n_prime compté à part
NOM, SUFFIXE = re.compile("[A-Za-z0-9_-]+"), ".lot"  # nom de cellule sans « / » ni « . » (Q-T4-8) ; jamais .jsonl


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
