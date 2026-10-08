"""Tests du lot PLAN-S2BIS-2, sur fixtures seulement (annexe D.4 a ; aucun journal réel n'est lu), depuis
scripts/plan-s2bis-2, contre le harnais du commit d'analyse (README) : env -u SHOGEN_S2_CAMPAGNE_CONTROL
PLAN_S2BIS_HARNAIS=<extraction>/s2-harness PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -t .
Pièces de PLAN-S2BIS chargées par le socle sous leurs épingles (P-1) ; tests/fixtures.py de PLAN-S2BIS par chemin,
sous son sha256, sous le nom fixtures_ps2."""
import os

import socle

if not os.environ.get("PLAN_S2BIS_HARNAIS"):
    raise RuntimeError("PLAN_S2BIS_HARNAIS non posée : s2-harness d'une extraction du commit d'analyse (README)")
PRM = socle.lire()
CHEMINS, MODS, PS2, EP = socle.charger(PRM)
fx = socle.charger_module("fixtures_ps2", CHEMINS["fixtures"])
