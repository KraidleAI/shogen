"""Commun du lot POST-PREREG : analyses ajoutées après le pré-enregistrement, hors décision, sur les journaux scellés
(G0 `docs/adr-0028/G0-lots-DETTES.md`, ligne POST-PREREG ; items de l'annexe B d'ADR-0028, cités par chaque script).

Lecteurs du harnais réutilisés par import, sans modifier `s2-harness` : mêmes appels que `r1.recompute_from_journal`.
Chaque sortie porte ETIQUETTE en première ligne, puis sa provenance et le contrôle de cohérence contre le bloc 3 du
rendu J28 (n, K, P̂_more par strate, chaîne pour chaîne) ; en écart, aucune valeur d'analyse (fail-closed). Aucune
sortie ne remplace une valeur des rendus ; aucun contenu de journal n'est imprimé."""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
from decimal import Decimal, localcontext

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(os.path.dirname(ICI))
HARNAIS = os.path.join(RACINE, "s2-harness")
if HARNAIS not in sys.path:
    sys.path.insert(0, HARNAIS)
from shogen_s2 import r1, records, window  # noqa: E402

ETIQUETTE = ("ajoutée après le pré-enregistrement, hors décision ; ne change pas le verdict de la règle scellée "
             "(« R1 discrimine » = FAUX, docs/11 §3)")
T0, N_FIXE, PLAGE_D5 = 1787770800, 38600, (1790273880, 1790435280)   # rendu_unique.SORTIES « j28 » (D2 pt 6 ; D5)
SEGMENT = {"t0": T0, "n_fixe": N_FIXE}
RENDU_J28 = os.path.join(RACINE, "docs", "adr-0028", "execution", "rendu-2026-10-04",
                         "shogen-27b0e30-rendu-20261004T011129Z-943.3-j28.out")


def dec(x) -> str:
    """Decimal en chaîne sous le contexte nommé du harnais (forme des rendus) ; None : « - »."""
    with localcontext(r1.contexte_decimal()):
        return "-" if x is None else str(x)


def sha256(chemin: str) -> str:
    with open(chemin, "rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def lire_bloc3(chemin: str) -> dict:
    """{strate : (n, K, P̂_more en chaîne)} lus au bloc 3 d'un rendu : en-tête de strate, puis première ligne
    « P̂_more  = » (deux espaces) ; la ligne de strate poolée (« P̂_more = », un espace) n'est pas lue."""
    with open(chemin, encoding="utf-8") as f:
        b3 = f.read().split("\n[BLOC 3]", 1)[1].split("\n[BLOC 4]", 1)[0]
    out, st = {}, None
    for x in b3.split("\n"):
        if m := re.match(r"  ── strate « (\w+) » : n = (\d+) fenêtres complétées ; K = (\d+) ", x):
            st, out[m.group(1)] = m.group(1), [int(m.group(2)), int(m.group(3)), None]
        elif (m := re.fullmatch("    P̂_more  = (\\S+)", x)) and st and out[st][2] is None:
            out[st][2] = m.group(1)
    return {s: tuple(v) for s, v in out.items()}


def controle_j28(base: dict, chemin: str) -> tuple:
    """n, K, P̂_more de `base` (sortie de r1.compute_r1) contre le bloc 3 du rendu, chaîne pour chaîne : (égaux,
    lignes) ; une strate absente d'un côté est un écart ; rendu sans strate : écart."""
    attendu, lignes, ok = lire_bloc3(chemin), [], True
    for st in sorted(set(attendu) | set(base["strates"])):
        b = base["strates"].get(st)
        nous = None if b is None else (b["n"], b["K"], dec(b["P_more"]))
        ok &= nous == attendu.get(st)
        lignes.append(f"contrôle de cohérence (rendu, bloc 3) « {st} » : recompté (n, K, P̂_more) = {nous} ; rendu = "
                      f"{attendu.get(st)} : {'égaux' if nous == attendu.get(st) else 'ÉCART'}")
    return ok and bool(attendu), lignes
