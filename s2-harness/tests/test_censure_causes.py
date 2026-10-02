"""SHOGEN-CENSURE-CAUSES-1, option (a) (ADR-0028 annexe B.23 ; docs/adr-0028/G0-partie-2.md §B, troisième ajout) : au
bloc 1, deux lignes par strate, fenêtres sautées entre deux marqueurs d'un même démarrage (harnais vivant), puis toutes
les autres (arrêt ou passage entre démarrages, cause non attribuée par le journal) ; aucun seuil de temps ; somme des
deux = s de fenetres_sautees. Collecteur réel, horloge factice, aucune donnée de campagne (D.4 a) ; attendus écrits à la
main depuis la géométrie des fixtures, jamais lus dans une sortie du code ; chaque test nomme la mutation qui le
rougit."""
from __future__ import annotations

import json
import os
import re
import tempfile
import unittest

from shogen_s2 import collector, records, report, window
from tests.test_collector import BY_ID, DELTA, SKELETON, TAU, FakeClock, _taumap, frozen_read_fn, sbc_huge
from tests.test_d5_amend import rang
from tests.test_exclusion import PLAGE, build_fixture
from tests.test_sensibilite import H, fixture as fixture_h, t as heure

# Démarrages (départ, rangs collectés), dans l'ordre du journal ; rang 0 = ven. 22:00Z, stress dès le rang 120 (sam.
# 00:00Z). Le 3e perd sa ligne run_params, le 4e sa ligne clock_check « startup » (excisions) ; le 5e revient sur 120 et
# 122, dans la portée du 1er (horloge qui recule : portées chevauchantes).
DEM = ((rang(100), [k for k in range(100, 125) if k not in (110, 121, 123)]),
       (rang(127) + 30, [129, 130, 131, 133, 134, 135]), (rang(140), [141, 142, 143]), (rang(150), [152, 154]),
       (rang(120), [120, 122]))
VIV = ("  {:24} = « {} » : {} sur s = {} — sautées entre deux marqueurs window_close d'un même démarrage (run_params "
       "ou clock_check « startup », ordre du journal) : harnais vivant — SHOGEN-CENSURE-CAUSES-1")
AUT = ("  {:24} = « {} » : {} sur s = {} — arrêt ou passage entre démarrages, cause non attribuée par le journal "
       "(fenêtres entre started_epoch et le premier marqueur d'un démarrage comprises) — SHOGEN-CENSURE-CAUSES-1")
KW = ({}, {"exclude_ranges": [(rang(110), rang(110)), (rang(122), rang(124)), (rang(154), rang(154))]},
      {"segment": {"t0": rang(105), "t_fin": rang(128)}})


def fixture(avant=()) -> tuple:
    """Un appel de collector.collect par démarrage ; excisions ; clock_check d'une autre phase posé après le marqueur
    109 ; `avant` : marqueurs window_close (calme) écrits en tête, avant toute ligne de démarrage. Rend (c, j)."""
    d = tempfile.mkdtemp(prefix="s2causes_")
    c, j, raw = (os.path.join(d, x) for x in ("control.jsonl", "journal.jsonl", "raw.jsonl"))
    for debut, rangs in DEM:
        clock = [float(debut)] + [x for k in rangs for x in (rang(k) + 1.0, rang(k) + 60 - DELTA)]
        collector.collect([BY_ID[f] for f in SKELETON], c, j, raw, n_windows=len(rangs), sigma_by_class=sbc_huge(),
                          tau_classe=_taumap(TAU), strate_spec=window.WEEKEND_STRATE_SPEC, now_fn=FakeClock(clock),
                          sleep_fn=lambda s: None, read_fn=frozen_read_fn)
    sans = (("run_params", "started_epoch", rang(140)), ("clock_check", "harness_ts", rang(150)))
    with open(c, encoding="utf-8") as f:
        tous = [json.loads(ln) for ln in f]
    objs = [o for o in tous if not any(o["record"] == r and o.get(k) == v for r, k, v in sans)]
    assert len(objs) == len(tous) - 2
    i = next(k for k, o in enumerate(objs) if o.get("window_start") == rang(109)) + 1
    objs[i:i] = [records.clock_check_record(rang(109) + 56.0, "controle", {}, {}, None, "phase autre que startup")]
    with open(c, "w", encoding="utf-8") as f:
        f.writelines(json.dumps(o, ensure_ascii=False) + "\n" for o in [
            records.window_close_record(ws, "calme", ws + 55.0) for ws in avant] + objs)
    return c, j


def lu(txt: str) -> tuple:
    """Bloc 1 : (s par strate, lu sur la ligne fenetres_sautees ; les 2 × (nombre de strates) lignes qui la suivent)."""
    b1 = txt.split("[BLOC 2]")[0].splitlines()
    i = next(k for k, ln in enumerate(b1) if ln.startswith(f"  {'fenetres_sautees':24} = "))
    s = {st: int(n) for st, n in re.findall(r"(\w+) (\d+)", b1[i].split("hors plages D5 : ")[1].split(" — ")[0])}
    return s, b1[i + 1:i + 1 + 2 * len(s)]


def attendu(**par_strate) -> tuple:
    """strate = (vivant, non attribuées, s), écrits à la main ; deux lignes par strate, strates triées."""
    return ({st: s for st, (_v, _a, s) in par_strate.items()},
            [x for st, (v, a, s) in sorted(par_strate.items()) for x in (
                VIV.format("sautees_harnais_vivant", st, v, s), AUT.format("sautees_non_attribuees", st, a, s))])


class TestCensureCauses(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c, cls.j = fixture()

    def test_vivant_entre_deux_marqueurs_reste_non_attribue(self):
        """Sans option : 110 (calme) ; 121, 123, 132 et 153 (stress) entre deux marqueurs d'un même démarrage ; non
        attribuées : 125-128 (du dernier marqueur du 1er démarrage à started_epoch du 2e, puis jusqu'à son premier
        marqueur), 136-140 et 144-151 (le 3e démarrage s'ouvre à son clock_check, le 4e à son run_params). Rougit si :
        démarrage ouvert par run_params seul, par clock_check seul ou par un clock_check d'une autre phase ; journal
        entier tenu pour un démarrage ; portées chevauchantes comptées deux fois, ou union arrêtée à la fin de la
        portée incluse ; marqueur de fin de portée compté sauté ; ligne à 0 omise ; valeurs permutées."""
        self.assertEqual(lu(report.render_report(self.c, self.j)), attendu(calme=(1, 0, 1), stress=(4, 17, 21)))

    def test_plages_et_segment(self):
        """Plages [110 ; 110], [122 ; 124] et [154 ; 154] : 110 et 123 exclues, plus sautées ; 121 et 153 restent
        vivantes (portées lues sur tous les marqueurs, exclus compris). Segment [105 ; 128) : 132 et 153 hors portée.
        Rougit si : part vivante sans les plages, sur les marqueurs filtrés, ou hors de la portée du segment."""
        for kw, att in zip(KW[1:], (attendu(calme=(0, 0, 0), stress=(3, 17, 20)),
                                    attendu(calme=(1, 0, 1), stress=(2, 3, 5)))):
            with self.subTest(kw=kw):
                self.assertEqual(lu(report.render_report(self.c, self.j, **kw)), att)

    def test_marqueurs_avant_tout_demarrage_et_week_end_sans_marqueur(self):
        """Marqueurs 96 et 98 écrits avant toute ligne de démarrage : 97 et 99 non attribuées. Fixture de
        test_sensibilite (w = 3 600, deux démarrages d'une fenêtre, week-end entier sauté, strate stress sans
        marqueur) : tout non attribué. Épingles (fixture de l'exclusion, sans et avec PLAGE) : quatre lignes à 0.
        Rougit si : marqueurs antérieurs au premier démarrage tenus pour un démarrage ; strate sans marqueur omise."""
        we = fixture_h(tempfile.mkdtemp(prefix="s2causes_we_"), blocs=[range(heure(7, 10), heure(7, 11), H),
                                                                          range(heure(10, 10), heure(10, 11), H)])
        c0, j0 = build_fixture(tempfile.mkdtemp(prefix="s2causes_ep_"))
        for cj, kw, att in ((fixture(avant=(rang(96), rang(98))), {}, attendu(calme=(1, 2, 3), stress=(4, 17, 21))),
                            (we, {}, attendu(calme=(0, 23, 23), stress=(0, 48, 48))),
                            ((c0, j0), {}, attendu(calme=(0, 0, 0), stress=(0, 0, 0))),
                            ((c0, j0), {"exclude_ranges": [PLAGE]}, attendu(calme=(0, 0, 0), stress=(0, 0, 0)))):
            with self.subTest(c=cj[0], kw=kw):
                self.assertEqual(lu(report.render_report(*cj, **kw)), att)

    def test_somme_des_deux_lignes_egale_s(self):
        """Valeurs lues dans le rendu, sans option, sous plages et sous segment : part vivante + non attribuées = s de
        fenetres_sautees, par strate, et « sur s » = s. Rougit si : reste ≠ s − part vivante."""
        for kw in KW:
            s, lignes = lu(report.render_report(self.c, self.j, **kw))
            for st, viv, aut in zip(sorted(s), lignes[::2], lignes[1::2]):
                (v, sv), (a, sa) = (map(int, re.search(rf"« {st} » : (\d+) sur s = (\d+) — ", x).groups())
                                    for x in (viv, aut))
                self.assertEqual((v + a, sv, sa), (s[st],) * 3, (kw, st))


if __name__ == "__main__":
    unittest.main()
