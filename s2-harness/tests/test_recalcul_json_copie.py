"""Lot CORR, CORR-1 (G0 docs/adr-0028/G0-lot-CORR.md ; ADR-0028 annexe B.42, SHOGEN-RECALCUL-JSON-COPIE-1, constat A-1
de la relecture R-B) : le run recalcul-tiers sérialise content["exact_copy_pairs"] (frozenset de deux noms de flux) en
liste triée ; sérialisation seule. Fixtures seulement (D.4 a) : collecteur réel, w = 60 s, 330 fenêtres ; defillama
recopie à chaque fenêtre le prix de coingecko, série non constante (copie exacte de r2.tick_identity sur au moins
content_n_min = 300 fenêtres communes). Attendus écrits à la main ; mutants : journal G1 du lot."""
from __future__ import annotations

import json
import os
import tempfile
import unittest
from decimal import Decimal, localcontext
from unittest import mock

from shogen_s2 import collector, lm, r1, r2
from shogen_s2.model import Reading, Status
from tests.test_collector import BY_ID, DELTA, TAU, FakeClock, _taumap, sbc_huge
from tests.test_rendu_production import produire
from tests.test_rendu_unique import ru

W, T0 = 60, 1787770800                  # T0 de la table réelle (2026-08-26T19:00:00Z), une seule strate (calme)
TABLE = (("j14-principal", {"t0": T0, "t_fin": T0 + 320 * W}, (), "étiquette un"),          # 320 fenêtres communes
         ("j28", {"t0": T0, "n_fixe": 320}, ((T0 + 100 * W, T0 + 109 * W),), "étiquette trois"))   # 310, plage exclue


def copie(d: str) -> tuple:
    """Fenêtre j (330) : coingecko et defillama au prix 64000 + j/100, coinbase à ce prix + 7 ; lectures toutes ok."""
    paths = [os.path.join(d, x) for x in ("control.jsonl", "journal.jsonl", "raw.jsonl")]

    def read_fn(s, ts):
        prix = Decimal(6400000 + (int(ts) - T0) // W + 700 * (s.flux_id == "coinbase")) / 100
        return Reading(flux_id=s.flux_id, kind=s.kind, endpoint=s.endpoint, fetch_ts=ts, status=Status.OK,
                       http_status=200, price=prix, currency=s.currency)
    b = range(T0, T0 + 330 * W, W)
    collector.collect([BY_ID[f] for f in ("coinbase", "coingecko", "defillama")], *paths, n_windows=len(b), w=W,
                      sigma_by_class=sbc_huge(), tau_classe=_taumap(TAU), sleep_fn=lambda s: None, read_fn=read_fn,
                      now_fn=FakeClock([float(T0)] + [x for ws in b for x in (ws + 1.0, ws + W - DELTA)]))
    return paths[0], paths[1]


def relu(x):
    """Sortie de recompute_* telle que le JSON du recalcul tiers doit la porter, écrite ici : Decimal en chaîne,
    ensemble en liste triée (G0, CORR-1), tuples en listes."""
    def ecrire(v):
        if isinstance(v, Decimal):
            return str(v)
        if isinstance(v, (set, frozenset)):
            return sorted(v)
        raise TypeError(type(v).__name__)
    with localcontext(r1.contexte_decimal()):
        return json.loads(json.dumps(x, default=ecrire))


class TestRecalculCopieExacte(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = tempfile.mkdtemp(prefix="s2copie_")
        cls.c, cls.j = copie(cls.d)

    def test_recalcul_tiers_paire_copie_en_liste_triee(self):
        """recalcul-tiers, table de fixture : code 0, JSON relisible, aucun avertissement ; dans chaque variante
        (j14-principal ; j28, plage exclue ; j28-incluse), exact_copy_pairs = [["coingecko", "defillama"]] et les
        quatre recompute_* égaux à leur sortie relue ici (sérialisation seule). Rougit si : frozenset hors du JSON
        (TypeError, aucune sortie : constat A-1) ; paire non triée ; une valeur du recalcul change."""
        with mock.patch.object(ru, "SORTIES", TABLE):
            code, octets = produire("recalcul-tiers", "--journaux", self.d)
        out = json.loads(octets)
        self.assertEqual((code, sorted(out), out["avertissements"]),
                         (0, ["avertissements", "j14-principal", "j28", "j28-incluse"], []))
        for n, seg, pl in [x[:3] for x in TABLE] + [("j28-incluse", TABLE[1][1], ())]:
            with self.subTest(sortie=n):
                self.assertEqual(out[n]["r2"]["content"]["exact_copy_pairs"], [["coingecko", "defillama"]])
                self.assertEqual({k: out[n][k] for k in ("r1", "d5", "lm", "r2")}, relu({k: f(
                    self.c, self.j, pl, seg) for k, f in (("r1", r1.recompute_from_journal), ("d5",
                    r1.recompute_d5_from_journal), ("lm", lm.recompute_lm_from_journal), ("r2",
                    r2.recompute_r2_from_journal))}))

    def test_decimal_ensembles_en_listes_triees(self):
        """_decimal (default de json.dumps) : frozenset et set en liste triée ({8, 1} s'itère 8 puis 1 sous CPython :
        list() à la place de sorted() rougit), Decimal en chaîne ; tout autre type : TypeError nommé, comme avant.
        Rougit si : ensemble refusé ; list() au lieu de sorted() ; set oublié ; refus des autres types retiré."""
        self.assertEqual(ru._decimal(frozenset({"defillama", "coingecko"})), ["coingecko", "defillama"])
        self.assertEqual(ru._decimal({8, 1}), [1, 8])
        self.assertEqual(ru._decimal(Decimal("1.50")), "1.50")
        for x in (object(), b"x", 1j):
            with self.subTest(x=x), self.assertRaisesRegex(TypeError, "hors du JSON du recalcul tiers$"):
                ru._decimal(x)


if __name__ == "__main__":
    unittest.main()
