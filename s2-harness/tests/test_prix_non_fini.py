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
import traceback
import unittest
from decimal import Decimal
from pathlib import Path
from unittest import mock

from shogen_s2 import collector, r1, report, window
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
        cls.src = src = tempfile.mkdtemp(prefix="s2nf_")
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
        (chaîne, entier, flottant JSON) et null : inchangés, aucun avertissement ; prix illisible : refus nommé
        (SHOGEN-PRIX-ILLISIBLE-1, test suivant). Rougit si : chaînes seules ; libellés exacts ; NaN seul ; statut ok
        exigé ; fini touché."""
        nf = ('"NaN"', '"nan"', '"-NaN"', '"sNaN"', '"-sNaN"', '"NaN12"', '" nan "', '"Infinity"', '"-Infinity"',
              '"inf"', '"+INF"', "NaN", "Infinity", "-Infinity")
        cas = [(x, "ok", None, 1) for x in nf] + [('"NaN"', "panne_http", None, 1)] + [(x, "ok", v, 0) for x, v in (
            ('"64475.75"', "64475.75"), ('"-0"', "-0"), ('"1E+2"', "1E+2"), ("3", 3), ("1.5", Decimal("1.5")),
            ("null", None))]
        for brut, statut, prix, avert in cas:
            p = os.path.join(tempfile.mkdtemp(prefix="s2nf_"), "journal.jsonl")
            Path(p).write_text(f'{{"window_start": 0, "flux_id": "x", "status": "{statut}", "price": {brut}}}\n',
                               encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()) as err:
                (lu,) = r1.parse_journal(p)
            with self.subTest(prix=brut, statut=statut):
                self.assertEqual((lu["price"], err.getvalue()), (prix, AVERT.format(p, "x 1") + "\n" if avert else ""))

    def test_illisible_ou_hors_contexte_refus_nomme(self):
        """SHOGEN-PRIX-ILLISIBLE-1, SHOGEN-PRIX-HORS-CONTEXTE-1 (annexe B.44 ; L-1, L-2 du G1 du lot CORR) :
        r1.parse_journal sur une ligne, lecture ok ou en panne. Prix ni chaîne ni nombre JSON (liste, objet, booléen)
        ou chaîne que Decimal ne lit pas : PrixIllisible ; prix fini d'exposant ajusté au-delà d'Emax = 999999 du
        contexte nommé (chaîne ou jeton JSON) : PrixHorsContexte ; message : item, flux, window_start, jamais la valeur.
        Inchangés, sans avertissement : exposant ajusté 999999 (Emax), zéro d'exposant 2000000, 1E-1000000 (sous Emin :
        aucun dépassement). Rougit si : illisible inchangé ou lu comme absent ; booléen lu 0 ou 1 ; liste lue comme
        triplet Decimal ; borne « > Emax » devenue « ≥ » ; exposant brut au lieu de l'exposant ajusté (12E+999999 :
        ajusté 1000000, brut 999999) ; zéro refusé ; valeur dans le message."""
        refus = [(x, "PrixIllisible", "SHOGEN-PRIX-ILLISIBLE-1") for x in (
            '"abc"', '""', '"1,5"', "[1]", "[0, [1], 0]", "{}", "true", "false")] + [(x, "PrixHorsContexte",
            "SHOGEN-PRIX-HORS-CONTEXTE-1") for x in ('"1E+1000000"', '"-1E+1000000"', "1E+1000000",
                                                     '"12E+999999"')]
        for (brut, nom, item), statut in ((c, s) for c in refus for s in ("ok", "panne_http")):
            p = os.path.join(tempfile.mkdtemp(prefix="s2nf_"), "journal.jsonl")
            Path(p).write_text(f'{{"window_start": 7, "flux_id": "x", "status": "{statut}", "price": {brut}}}\n',
                               encoding="utf-8")
            with self.subTest(prix=brut, statut=statut):
                with self.assertRaises(ValueError) as cm:
                    r1.parse_journal(p)
                self.assertEqual(type(cm.exception).__name__, nom)
                self.assertIn(f"{item})", str(cm.exception))
                self.assertIn(f"{p} (flux 'x', window_start 7 ; valeur non reproduite)", str(cm.exception))
                if brut.strip('"'):              # chemin retiré : son suffixe aléatoire ne compte pas
                    self.assertNotIn(brut.strip('"'), str(cm.exception).replace(p, ""))
        for brut, prix in (('"1E+999999"', "1E+999999"), ('"-9.5E+999999"', "-9.5E+999999"), ('"0E+2000000"',
                           "0E+2000000"), ('"1E-1000000"', "1E-1000000"), ("1E+999999", Decimal("1E+999999"))):
            p = os.path.join(tempfile.mkdtemp(prefix="s2nf_"), "journal.jsonl")
            Path(p).write_text(f'{{"window_start": 7, "flux_id": "x", "status": "ok", "price": {brut}}}\n',
                               encoding="utf-8")
            with self.subTest(prix=brut), contextlib.redirect_stderr(io.StringIO()) as err:
                (lu,) = r1.parse_journal(p)
                self.assertEqual((lu["price"], err.getvalue()), (prix, ""))

    def test_recalcul_et_rendu_refus_nomme_au_lecteur(self):
        """Fixture de la classe, prix de la lecture ok (rang 10, bitfinex) : « abc » → PrixIllisible et « 1E+1000000 » →
        PrixHorsContexte, levées par r1.parse_journal depuis r1.recompute_from_journal et report.render_report, à la
        place de decimal.InvalidOperation (_classify_window) et decimal.Overflow (classify_ecart) de la base (sonde du
        journal G1). Rougit si : exception non nommée ; refus levé ailleurs qu'au lecteur."""
        for prix, nom in (("abc", "PrixIllisible"), ("1E+1000000", "PrixHorsContexte")):
            d = variante(self.src, {(10, "bitfinex"): prix})
            c, j = os.path.join(d, "control.jsonl"), os.path.join(d, "journal.jsonl")
            for f in (r1.recompute_from_journal, report.render_report):
                try:
                    f(c, j)
                    lu = None
                except Exception as e:      # pile lue ici : assertRaises la retire de l'exception qu'il garde
                    lu = (type(e).__name__, traceback.extract_tb(e.__traceback__)[-1].name)
                with self.subTest(prix=prix, f=f.__name__):
                    self.assertEqual(lu, (nom, "parse_journal"))

    def test_flux_de_l_avertissement_tries_par_nom(self):
        """G2 du lot CORR (mutant G03) : flux de l'avertissement triés par nom, non dans l'ordre du fichier (zeta y
        précède alpha)."""
        p = os.path.join(tempfile.mkdtemp(prefix="s2nf_"), "journal.jsonl")
        Path(p).write_text('{"flux_id": "zeta", "status": "ok", "price": "NaN"}\n'
                           '{"flux_id": "alpha", "status": "ok", "price": "NaN"}\n', encoding="utf-8")
        with contextlib.redirect_stderr(io.StringIO()) as err:
            r1.parse_journal(p)
        self.assertEqual(err.getvalue(), AVERT.format(p, "alpha 1, zeta 1") + "\n")


if __name__ == "__main__":
    unittest.main()
