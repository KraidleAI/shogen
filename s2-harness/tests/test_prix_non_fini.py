"""Lot CORR, CORR-2 (G0 docs/adr-0028/G0-lot-CORR.md ; ADR-0028 annexe B.43, SHOGEN-PRIX-NON-FINI-1, constat A-1 de la
relecture R-A) : un prix non fini de journal.jsonl est lu comme absent au point unique r1.parse_journal (None : panne au
sens de classify_ecart, non ok au sens du pool D1), compté par flux dans un avertissement du lecteur, jamais la valeur.
Fixtures seulement (D.4 a) : collecteur réel, cinq flux (N ≥ 4 répondantes : médiane de l'enveloppe atteinte), w =
60 s, deux strates ; attendus : la même fixture où ces prix sont null, le texte de l'avertissement et les comptes de
panne écrits à la main. Mutants : journal G1 du lot."""
from __future__ import annotations

import contextlib
import io
import json
import os
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from unittest import mock

from shogen_s2 import collector, r1, window
from shogen_s2.model import Reading, Status
from tests.test_collector import BY_ID, DELTA, TAU, FakeClock, _taumap, frozen_reading, sbc_huge
from tests.test_rendu_blocs import SAM
from tests.test_rendu_production import produire
from tests.test_rendu_unique import ru

W, FLUX = 60, ["coinbase", "kraken", "bitstamp", "bitfinex", "gemini"]
T0 = SAM - 50 * W                       # rangs 0-49 : calme ; 50-99 : stress (samedi 2026-08-08 00:00Z)
TABLE = (("j14-principal", {"t0": T0, "t_fin": T0 + 80 * W}, (), "étiquette un"),
         ("j28", {"t0": T0, "n_fixe": 90}, ((T0 + 20 * W, T0 + 24 * W),), "étiquette trois"))
NON_FINIS = {(10, "bitfinex"): "NaN", (60, "gemini"): "Infinity", (70, "bitfinex"): "NaN"}   # (rang, flux), lectures ok
AVERT = ("[s2-harness] AVERTISSEMENT : prix non fini(s) lu(s) comme absent(s) dans {}, fichier entier — par flux : {} "
         "(SHOGEN-PRIX-NON-FINI-1 : panne au sens de classify_ecart ; valeurs non reproduites).")


def journaux(d: str) -> None:
    """100 fenêtres, lectures gelées ; coinbase en panne aux rangs multiples de 3, kraken aux rangs impairs."""
    paths = [os.path.join(d, x) for x in ("control.jsonl", "journal.jsonl", "raw.jsonl")]

    def read_fn(s, ts):
        j = (int(ts) - T0) // W
        if s.flux_id == "coinbase" and j % 3 == 0 or s.flux_id == "kraken" and j % 2 == 1:
            return Reading(flux_id=s.flux_id, kind=s.kind, endpoint=s.endpoint, fetch_ts=ts, currency=s.currency,
                           status=Status.PANNE_HTTP, http_status=401)
        return frozen_reading(s.flux_id, ts)
    b = range(T0, T0 + 100 * W, W)
    collector.collect([BY_ID[f] for f in FLUX], *paths, n_windows=len(b), w=W, sigma_by_class=sbc_huge(),
                      tau_classe=_taumap(TAU), strate_spec=window.WEEKEND_STRATE_SPEC, sleep_fn=lambda s: None,
                      now_fn=FakeClock([float(T0)] + [x for ws in b for x in (ws + 1.0, ws + W - DELTA)]),
                      read_fn=read_fn)


def variante(src: str, prix: dict) -> str:
    """Copie de src : dans journal.jsonl, prix[(rang, flux)] à la place du prix de ces lectures ok ; reste à l'octet."""
    d, lignes = tempfile.mkdtemp(prefix="s2nf_"), []
    for n in ("control.jsonl", "raw.jsonl"):
        Path(d, n).write_bytes(Path(src, n).read_bytes())
    for x in Path(src, "journal.jsonl").read_text(encoding="utf-8").splitlines():
        o = json.loads(x)
        k = ((o["window_start"] - T0) // W, o["flux_id"])
        if k in prix:
            if o["status"] != "ok":
                raise AssertionError(f"fixture : lecture {k} non ok")
            x = json.dumps({**o, "price": prix[k]}, ensure_ascii=False)
        lignes.append(x + "\n")
    Path(d, "journal.jsonl").write_text("".join(lignes), encoding="utf-8")
    return d


class TestPrixNonFini(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        src = tempfile.mkdtemp(prefix="s2nf_")
        journaux(src)
        cls.a, cls.b = variante(src, NON_FINIS), variante(src, dict.fromkeys(NON_FINIS))

    def test_rendu_et_recalcul_comme_prix_null(self):
        """Sorties j14-principal, j28 (plage exclue) et recalcul-tiers sur la fixture à prix NaN et Infinity (lectures
        ok, N ≥ 4) : code 0, égales à celles de la fixture où ces prix sont null, à l'avertissement près : une ligne
        [AVERTISSEMENT DU LECTEUR] après l'étiquette (bitfinex 2, gemini 1 ; journal nommé sans dossier), douze au JSON
        (r1, d5, lm, r2 : quatre lectures par variante, trois variantes), aucune sur la fixture null ; ces lectures en
        panne au bloc R1 du J28. Rougit si : exception (InvalidOperation de la médiane ou du logarithme : constat A-1) ;
        prix non fini lu autrement qu'absent ; avertissement absent, sans compte par flux, ou qui porte une valeur."""
        ligne = AVERT.format("journal.jsonl", "bitfinex 2, gemini 1")
        with mock.patch.object(ru, "SORTIES", TABLE):
            for nom, *_x, etiq in TABLE:
                (ca, a), (cb, b) = (produire(nom, "--journaux", d) for d in (self.a, self.b))
                tete, *corps = b.decode("utf-8").split("\n")
                with self.subTest(sortie=nom):
                    self.assertEqual((ca, cb, tete), (0, 0, f"[ÉTIQUETTE] {nom} : {etiq}"))
                    self.assertEqual(a.decode("utf-8"), "\n".join([tete, "[AVERTISSEMENT DU LECTEUR] " + ligne,
                                                                   *corps]))
            (ca, a), (cb, b) = (produire("recalcul-tiers", "--journaux", d) for d in (self.a, self.b))
        a, b = json.loads(a), json.loads(b)
        self.assertEqual((ca, cb, a.pop("avertissements"), b.pop("avertissements")), (0, 0, [ligne] * 12, []))
        self.assertEqual(a, b)
        st = a["j28"]["r1"]["strates"]
        self.assertEqual([st[s]["per_source"][f]["panne"] for s, f in (("calme", "bitfinex"), ("stress", "bitfinex"),
                                                                        ("stress", "gemini"))], [1, 1, 1])

    def test_formes_lues_comme_absentes_ou_inchangees(self):
        """r1.parse_journal sur une ligne : toute forme non finie que Decimal admet (casse, signe, sNaN, charge utile,
        espaces, jetons JSON NaN et Infinity), lecture en panne comprise : prix None, avertissement « x 1 » ; prix fini
        (chaîne, entier, flottant JSON), null et prix illisible par Decimal : inchangés, aucun avertissement. Rougit
        si : chaînes seules ; libellés exacts ; NaN seul ; statut ok exigé ; illisible lu comme absent ; fini touché."""
        nf = ('"NaN"', '"nan"', '"-NaN"', '"sNaN"', '"-sNaN"', '"NaN12"', '" nan "', '"Infinity"', '"-Infinity"',
              '"inf"', '"+INF"', "NaN", "Infinity", "-Infinity")
        cas = [(x, "ok", None, 1) for x in nf] + [('"NaN"', "panne_http", None, 1)] + [(x, "ok", v, 0) for x, v in (
            ('"64475.75"', "64475.75"), ('"-0"', "-0"), ('"1E+2"', "1E+2"), ("3", 3), ("1.5", Decimal("1.5")),
            ("null", None), ('"abc"', "abc"), ("[1]", [1]))]
        for brut, statut, prix, avert in cas:
            p = os.path.join(tempfile.mkdtemp(prefix="s2nf_"), "journal.jsonl")
            Path(p).write_text(f'{{"window_start": 0, "flux_id": "x", "status": "{statut}", "price": {brut}}}\n',
                               encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()) as err:
                (lu,) = r1.parse_journal(p)
            with self.subTest(prix=brut, statut=statut):
                self.assertEqual((lu["price"], err.getvalue()), (prix, AVERT.format(p, "x 1") + "\n" if avert else ""))


if __name__ == "__main__":
    unittest.main()
