"""Tests du lot PLAN-S2BIS, sur fixtures seulement (annexe D.4 a ; aucun journal réel n'est lu), lancés depuis
`scripts/plan-s2bis` contre le harnais du commit d'analyse (README) :
`env -u SHOGEN_S2_CAMPAGNE_CONTROL PLAN_S2BIS_HARNAIS=<extraction>/s2-harness PYTHONDONTWRITEBYTECODE=1
python3 -B -m unittest discover -s tests -t .`"""
