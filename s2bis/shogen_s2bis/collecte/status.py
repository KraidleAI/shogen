"""Commande `status` (CB-17 ; E-C-38 ; ADR-0029 §2.3 et §2.9 l.244 ; AVIS du G0, Q-D-03, point 3) : la santé seule,
lue au journal du pool (enregistrements `sante` de CB-11 et marqueurs), sans rien écrire ni prendre le verrou de
l'écrivain. CB-17a : lecture et jugement. Une ligne `lecture` est reconnue à ses premiers octets, sa première clé en
forme canonique (FORMAT §1.2, §9.1), et n'est jamais décodée : aucun statut de source, aucune valeur, aucun prix
n'entre au jugement. Jugement par fenêtre aux seuils scellés (ADR-0029 §2.3 ; égaux au bloc `degradation` de
`config/analyse.json`, test croisé) : D-1 aucun marqueur, ou aucune `sante` ; D-2 lecture partie plus de 5 s après
son instant planifié, ou non partie (règle Q-C-02 de l'AVIS, FORMAT §11.6) ; D-4 au moins 2 témoins sans réponse
retenue ; D-5 au moins 2 noms témoins non résolus (sans réponse retenue, rcode non nul, ou sans réponse A). D-3 n'est
pas jugé : le format de la sortie de `chronyc` n'est pas lu sur pièce (SHOGEN-S2BIS-CHRONYC-FORMAT-1) ; seuls les
relevés absents ou en erreur sont comptés."""
import json
import os
import re

from shogen_s2bis.collecte.journal import LIMITE
from shogen_s2bis.collecte.lecture import S

LECTURE, W = b'{"adresse":', 60                      # première clé d'une `lecture` canonique ; largeur des fenêtres
D2, D4, D5 = 5 * S, 2, 2                             # retard (µs), témoins sans réponse, noms non résolus


class RefusStatus(ValueError):
    """Refus nommé (`code`) : STATUS/journal."""
    def __init__(self, code, detail):
        super().__init__(f"{code} : {detail}")
        self.code = code


def enregistrements(dossier, prefixe="pool"):
    """(enregistrement, ligne) hors `lecture`, fichiers dans l'ordre (jour, k entier) de la grammaire du FORMAT §6.1 ;
    un fichier s'arrête à sa première ligne coupée, illisible ou sans `type` ni `seq`."""
    motif = re.compile(re.escape(prefixe) + "-([0-9]{4}-[0-9]{2}-[0-9]{2})-(0|[1-9][0-9]*)[.]jsonl")
    fichiers = sorted((x[1], int(x[2]), n) for n in os.listdir(dossier) if (x := motif.fullmatch(n)))
    if not fichiers:
        raise RefusStatus("STATUS/journal", f"aucun fichier du journal « {prefixe} »")
    for _j, _k, n in fichiers:
        with open(os.path.join(dossier, n), "rb") as f:
            while (ligne := f.readline(LIMITE)).endswith(b"\n"):
                if ligne.startswith(LECTURE):
                    continue
                try:
                    e = json.loads(ligne)
                except (ValueError, RecursionError):
                    break
                if type(e) is not dict or type(e.get("type")) is not str or type(e.get("seq")) is not int:
                    break
                yield e, ligne


def _repond(v):
    return type(v) is dict and v.get("statut") == "reponse"


def _resolu(v):
    return _repond(v) and v.get("rcode") == 0 and any(type(r) is list and r[1:2] == [1] for r in v["reponses"] or ())


def juger(sante):
    """(codes, relevé D-3 absent ou en erreur) d'une fenêtre close dont `sante` est la santé (None : aucune) ; sans
    santé lisible : D-1."""
    try:
        d2, d3, codes = sante["d2"], sante["d3"], []
        if d2["non_parties"] or d2["retard_max"] is not None and d2["retard_max"] > D2:
            codes.append("D-2")
        codes += ["D-4"] * (sum(not _repond(v) for v in sante["d4"]) >= D4)
        codes += ["D-5"] * (sum(not _resolu(v) for v in sante["d5"]) >= D5)
        return codes, type(d3) is not dict or "erreur" in d3 or d3.get("code") != 0
    except (KeyError, TypeError, AttributeError):
        return ["D-1"], False
