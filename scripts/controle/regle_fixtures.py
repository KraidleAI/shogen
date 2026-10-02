"""Valeurs de la règle SHOGEN-CRITERE-R1-1 (r1.regle_critere) sur les fixtures de tests/test_critere.py, sur
l'arbre donné : table U1-U8, J1 (ℓ = 240 et 1), J2, J3 (ℓ = 1), J4 (fixture longue, ℓ = 240), deux(50, 40).
Écrit un JSON (Decimal en chaîne). Usage : python -B regle_fixtures.py <arbre> <sortie.json>"""
import json
import sys

arbre, sortie = sys.argv[1], sys.argv[2]
sys.path.insert(0, arbre)
from shogen_s2 import r1                                     # noqa: E402
from tests import test_critere as tc, test_rendu_blocs as trb  # noqa: E402

out = {"seuil": str(r1.SEUIL_Z), "ell": r1.ELL_BLOC}
for nom, (b, *_r) in tc.U.items():
    out[nom] = r1.regle_critere({"strates": {"a": b}})
for nom, fab, ell in (("J1", lambda: tc.journal(200, 200, tc.deux(25, 29)), 240),
                      ("J1-l1", lambda: tc.journal(200, 200, tc.deux(25, 29)), 1),
                      ("J2", lambda: tc.journal(200, 200, tc.deux(50, 37)), 240),
                      ("J3-l1", lambda: tc.journal(54, 10, tc.rotation), 1),
                      ("J5", lambda: tc.journal(200, 200, tc.deux(50, 40)), 240),
                      ("J4", lambda: tc.journal(7200, 60, trb.TestRenduBlocsLong.panne), 240)):
    out[nom] = tc.regle(*fab(), ell)[1]
with open(sortie, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1, default=str, sort_keys=True)
for k, v in out.items():
    if isinstance(v, dict):
        print(f"{k:6} {v['r1_discrimine']:14} m={v['m']} " + " ; ".join(
            f"{s}={e['valeur']}/{e['cas']}" for s, e in v["strates"].items()))
