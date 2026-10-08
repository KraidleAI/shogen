"""Partie 2 de S2, étape A, sous-lot A2 (docs/adr-0028/G0-partie-2.md, section A) : libellés et formes du rendu
des blocs 3 à 6 et de [SENSIBILITÉ]. SHOGEN-GARDE-LIBELLE-1 (seuil appliqué imprimé aux trois sites),
SHOGEN-RENDU-ZERO-1 (« 0 » pour un zéro Decimal exact), SHOGEN-AXES-ENONCE-1 (construction (b) : axes évaluables
de la strate et résidu nommé ; J1 et J2 : tests/test_critere.py, constante AX), SHOGEN-SENS-PLAGES-1 (titre
accordé au nombre de plages) et -2 (lignes de week-end, partie 3, lot P3). Attendus écrits à la main depuis la
conception des fixtures (collecteur réel, aucune donnée de campagne). Chaque test nomme la mutation qui le rougit."""

from __future__ import annotations

import json
import os
import re
import tempfile
import unittest

from shogen_s2 import report
from tests.test_d5_amend import rf
from tests.test_exclusion import PLAGE, build_fixture
from tests.test_rendu_blocs import couture, journal
from tests.test_sensibilite import RA, RB, fixture, t

SUITE = " — ADR-0025 déc. 4 ; ADR-0028 D2 pt 7 (liste fermée), §1 bis.1 pt 9 : hors décision"


def k_nul(f: str, st: bool, j: int) -> bool:
    """test_rendu_blocs, C-3 du G2 de B-DEP-2 : coinbase puis kraken, jamais ensemble (K = 0, garde > 0)."""
    a = 10 if st else 25
    return j < a if f == "coinbase" else f == "kraken" and a <= j < 2 * a


def z_nul(f: str, st: bool, j: int) -> bool:
    """test_rendu_blocs, C-2 du G2 de B-DEP-2 : une panne commune ; stress K = 1 = n·P̂_more (z_bloc = 0 à
    ℓ = 1)."""
    a = 10 if st else 25
    return j < a if f == "coinbase" else f == "kraken" and a - 1 <= j < 2 * a - 1


class TestRenduLibelles(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        d = rf()                     # fixture RF de D5-AMEND : six flux, hors-enveloppe évaluable (N ≥ 4)
        cls.rf = report.render_report(*(os.path.join(d, x) for x in ("control.jsonl", "journal.jsonl")))

    def test_garde_seuil_applique_aux_trois_sites(self):
        """GARDE-LIBELLE-1 : seuil_historique_valeur = 12 réécrit dans chaque démarrage (fixture du lot A, K = 0,
        garde levée), plage [w2 ; w4] : bloc 3 (2 strates), [SENSIBILITÉ] (2 strates × 2 variantes), règle (2
        strates) impriment « < 12 », jamais « < 10 ». Rougit si : « 10 » codé en dur à l'un des trois sites."""
        c, j = build_fixture(tempfile.mkdtemp(prefix="s2a2g_"))
        with open(c, encoding="utf-8") as f:
            objs = [dict(o, seuil_historique_valeur=12) if o["record"] == "run_params" else o
                    for o in map(json.loads, f)]
        with open(c, "w", encoding="utf-8") as f:
            f.writelines(json.dumps(o, ensure_ascii=False) + "\n" for o in objs)
        txt = report.render_report(c, j, exclude_ranges=[PLAGE])
        self.assertEqual((txt.count("(garde §5.4 : n·P̂_more·(1−P̂_more) < 12)"),
                          txt.count("(garde §5.4 : n·P̂_more·(1 − P̂_more) < 12)"), txt.count("< 10)")), (6, 2, 0))

    def test_zero_exact_forme_unique_trois_fixtures(self):
        """RENDU-ZERO-1 : FIV et R_centrage nuls (K = 0), z_bloc nul publié (couture ℓ = 1), φ nul au bloc 4
        (fixture RF) : « 0 » ; aucune forme 0E±k dans les trois rendus. Rougit si : _fmt_dec rend str(Decimal)
        d'un zéro."""
        k0 = report.render_report(*journal(250, 100, k_nul))
        with couture(1):
            z0 = report.render_report(*journal(250, 100, z_nul))
        for st in ("calme", "stress"):
            self.assertIn(f"\n    « {st} » : FIV = 0 ; R_centrage = 0 ; γ̂₀ = 0 (K ∈ {{0, n}}) : FIV_serie "
                          "indéfini\n", k0)
        self.assertIn("\n    « stress » : z_bloc = 0\n", z0)
        self.assertIn("\n      bitstamp×kraken            [20 20 40 40] φ=0 (0)\n", self.rf)
        zeros = [re.findall(r"(?<![\w.])-?0E[+-]\d+", x) for x in (k0, z0, self.rf)]
        self.assertEqual(zeros, [[], [], []])

    def test_enonce_axes_evaluables_et_residu(self):
        """AXES-ENONCE-1 (b), fixture RF : hors-enveloppe évaluable (aucune cellule non évaluable), staleness
        fail-open sur kraken et binance (sans horodatage porté). Rougit si : axes codés en dur ; résidu tu."""
        for st, n in (("calme", 120), ("stress", 140)):
            self.assertIn(f"\n    « {st} » : « le modèle d'indépendance n'est pas rejeté sur {n} fenêtres, axes "
                          "panne / staleness / hors-enveloppe (résidu : staleness fail-open : kraken, binance) » "
                          "; un résultat négatif est un résultat\n", self.rf)

    def test_titre_sensibilite_accorde_au_nombre_de_plages(self):
        """SENS-PLAGES-1 : une, deux puis trois plages (la troisième hors campagne) : titre au singulier, puis au
        pluriel avec le nombre. Rougit si : titre au singulier sous plusieurs plages ; nombre codé en dur."""
        c, j = fixture(tempfile.mkdtemp(prefix="s2a2p_"))
        for rg, titre in (([RA], "PLAGE D'EXCLUSION INCLUSE"), ([RA, RB], "2 PLAGES D'EXCLUSION INCLUSES"),
                          ([RA, RB, (t(1, 0), t(1, 5))], "3 PLAGES D'EXCLUSION INCLUSES")):
            lignes = report.render_report(c, j, exclude_ranges=rg).splitlines()
            self.assertEqual([x for x in lignes if x.startswith("[SENSIBILITÉ]")],
                             [f"[SENSIBILITÉ] {titre}{SUITE}"])

    def test_lignes_week_end_accordees_au_nombre_de_plages(self):
        """SENS-PLAGES-2 : une, deux puis trois plages (la troisième hors campagne) : chaque ligne de week-end finit
        par « retirées par la plage <n> », puis « retirées par les <k> plages <n> » ; ligne des totaux : « retirés en
        totalité par la plage : », puis « … par les <k> plages : ». Rougit si : singulier sous plusieurs plages ;
        nombre codé en dur ; pluriel sans le nombre."""
        c, j = fixture(tempfile.mkdtemp(prefix="s2p3b_"))
        for rg, par in (([RA], "la plage"), ([RA, RB], "les 2 plages"), ([RA, RB, (t(1, 0), t(1, 5))], "les 3 plages")):
            lignes = report.render_report(c, j, exclude_ranges=rg).splitlines()
            we = [re.sub(r" \d+$", "", x.split(" ; ")[-1]) for x in lignes if x.startswith("    week-end ")]
            tot = [x.split(" ; ")[-1].rsplit(" : ", 1)[0] for x in lignes if x.startswith("    en totalité : ")]
            with self.subTest(plages=len(rg)):
                self.assertEqual((we, tot), ([f"retirées par {par}"] * 3, [f"retirés en totalité par {par}"]))


if __name__ == "__main__":
    unittest.main()
