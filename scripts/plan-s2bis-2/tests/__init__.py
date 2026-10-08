"""Tests du lot PLAN-S2BIS-2, sur fixtures seulement (annexe D.4 a ; aucun journal réel n'est lu), depuis
scripts/plan-s2bis-2, contre le harnais du commit d'analyse (README) : env -u SHOGEN_S2_CAMPAGNE_CONTROL
PLAN_S2BIS_HARNAIS=<extraction>/s2-harness PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -t .
Pièces de PLAN-S2BIS chargées par le socle sous leurs épingles (P-1) ; tests/fixtures.py de PLAN-S2BIS par chemin,
sous son sha256, sous le nom fixtures_ps2."""
import json
import os

import socle

if not os.environ.get("PLAN_S2BIS_HARNAIS"):
    raise RuntimeError("PLAN_S2BIS_HARNAIS non posée : s2-harness d'une extraction du commit d'analyse (README)")
PRM = socle.lire()
CHEMINS, MODS, PS2, EP = socle.charger(PRM)
fx = socle.charger_module("fixtures_ps2", CHEMINS["fixtures"])


def banc(test, ws, motif, unites, pool=None, plages=(), masque=None, sigma=None, modif=None, **sur):
    """Fixture complète dans un dossier jetable : journaux de fixtures_ps2 (pool S2 : pool, ou les unités), bloc 3
    recompté par r1, faux rendu, parametres.json de PLAN-S2BIS (prm_fixture, ℓ = 1, 2, 3, puis sur), EP produit par
    episodes.main épinglé, modif(parametres) éventuelle, parametres.json du lot qui épingle ces pièces (masque : comptes
    attendus). Rend les arguments de la CLI des scripts, sorties dans <dossier>/s."""
    d = fx.dossier(test, "p2_banc_")
    fx.journaux(d, ws, motif, pool or unites, sigma=sigma)
    c, j = (os.path.join(d, n) for n in ("control.jsonl", "journal.jsonl"))
    b = fx.r1.recompute_from_journal(c, j, list(plages), {"t0": ws[0], "n_fixe": len(ws)})["strates"]
    b3 = {s: (v["n"], v["K"], MODS["commun"].dec(v["P_more"])) for s, v in b.items()}
    r = fx.rendu(os.path.join(d, "r.out"), b3)
    p = fx.prm_fixture(unites, b3, socle.empreinte(r), ws[0], len(ws), plages, fiv={"ell": [1, 2, 3]}, **sur)
    a, ep = ["--journaux", d, "--harnais", fx.HARNAIS, "--rendu", r], os.path.join(d, "episodes.txt")
    MODS["episodes"].main(a + ["--sortie", ep, "--parametres", fx.ecrire_prm(os.path.join(d, "ps2.json"), p)])
    if modif:
        modif(p)
    lot = json.loads(json.dumps(PRM))
    for cle, chemin in (("parametres", fx.ecrire_prm(os.path.join(d, "ps2b.json"), p)), ("ep", ep)):
        lot["plan_s2bis"]["chemins"][cle], lot["plan_s2bis"]["sha256"][cle] = chemin, socle.empreinte(chemin)
    lot["masque"].update(masque or {})
    return a + ["--sortie", os.path.join(d, "s"), "--parametres", fx.ecrire_prm(os.path.join(d, "lot.json"), lot)]
