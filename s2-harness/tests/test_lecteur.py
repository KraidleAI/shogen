"""Étape B de la partie 2, B1 (G0-partie-2.md §B) : lecteur de journal en octets, décodage ligne par ligne
(SHOGEN-TORN-LINE-UTF8-1, HS2-03) ; relevé asn_attribution sans ts compté à part au bloc 6, jamais KeyError
(SHOGEN-BLOC6-TS-1). Attendus écrits à la main. Chaque test nomme le mutant qui le rougit."""

from __future__ import annotations

import contextlib
import io
import os
import tempfile
import unittest

from shogen_s2 import r2, records, report
from tests.test_bloc3_bloc6 import DATE, DESCR, bloc
from tests.test_collector import BY_ID
from tests.test_critere import deux, journal
from tests.test_exclusion import PLAGE, build_fixture, poser

A = PLAGE[0]
SANS = "  relevés asn_attribution retenus sans ts (hôtes du pool, entrée malformée) = "
FIN = " — comptés à part, hors date de la partition (SHOGEN-BLOC6-TS-1)"


def fichier(octets: bytes) -> str:
    p = os.path.join(tempfile.mkdtemp(prefix="s2lect_"), "f.jsonl")
    with open(p, "wb") as f:
        f.write(octets)
    return p


class TestLecteurOctets(unittest.TestCase):
    def test_derniere_ligne_coupee_dans_un_caractere_multi_octets(self):
        """HS2-03 : dernière ligne coupée dans « é » (0xC3 seul) ; séparateurs CR, LF, CRLF ; ligne 2 blanche (espace
        insécable) : deux objets ; coupure consignée sur stderr, ligne nommée. Rougit si : fichier décodé d'un bloc
        (UnicodeDecodeError) ; ligne finale non décodable refusée ; découpe sur LF seul (CR séparateur en mode
        texte) ; ligne blanche jugée sur les octets (espace insécable non blanc)."""
        buf = io.StringIO()
        with contextlib.redirect_stderr(buf):
            lu = records.read_jsonl_tolerant(fichier(b'{"a": 1}\r\xc2\xa0\n{"b": "\xc3\xa9"}\r\n{"c": "\xc3'))
        self.assertEqual(lu, [{"a": 1}, {"b": "é"}])
        self.assertIn("dernière ligne tronquée ignorée", buf.getvalue())
        self.assertIn("(ligne 4, non décodable en UTF-8)", buf.getvalue())

    def test_ligne_non_decodable_non_finale_refusee(self):
        """Refus gardé et nommé : ligne 2 non décodable suivie d'une ligne valide. Rougit si : ligne non décodable
        tolérée hors de la dernière place, ou refus anonyme (UnicodeDecodeError du décodage d'un bloc)."""
        with self.assertRaisesRegex(ValueError, r"^ligne non décodable en UTF-8 NON finale .*\(ligne 2\)"):
            records.read_jsonl_tolerant(fichier(b'{"a": 1}\n{"b": "\xc3"}\n{"c": 3}\n'))

    def test_rendu_controle_coupe_dans_un_caractere(self):
        """Chemin de recalcul : control.jsonl terminé par une copie de run_params coupée dans « é » (crash
        mi-écriture) : rendu égal au rendu sans cette ligne. Rougit si : fichier décodé d'un bloc."""
        c, j = journal(10, 10, deux(5, 3))
        base = report.render_report(c, j)
        with open(c, "rb") as f:
            rp = f.readline()
        with open(c, "ab") as f:
            f.write(rp[:rp.index("é".encode()) + 1])
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(report.render_report(c, j), base)


class TestBloc6SansTs(unittest.TestCase):
    def setUp(self):
        d = tempfile.mkdtemp(prefix="s2b6ts_")
        self.c, self.j = build_fixture(d)
        poser(d, (A,))                                   # un relevé daté A par hôte du pool
        self.base = bloc(report.render_report(self.c, self.j), 6)
        self.h = self.malforme("coinbase")

    def malforme(self, flux: str) -> str:
        """Relevé de l'hôte de `flux` sans ts (entrée malformée), retenu : dernier de son hôte."""
        h = r2.build_flux_hosts([BY_ID[flux]])[flux]
        rec = records.asn_attribution_record(h, [flux], 0.0, [], {"status": "ok", "asn_ripestat": 7, "asn_cymru": 7})
        del rec["ts"]
        records.append_asn(self.c, rec)
        return h

    def test_releve_sans_ts_compte_a_part(self):
        """Bloc 6 rendu ; date sur les deux hôtes datés ; ligne « sans ts » = 1 et l'hôte ; sans entrée malformée,
        0 ; les trois hôtes sans ts : date « non mesurée » (aucun relevé retenu daté), 3. Rougit si : KeyError (ts
        indexé) ; relevé sans ts compté dans la date ; ligne absente ou compte faux ; « daté » omis."""
        iso, b6 = report._iso_utc(A), bloc(report.render_report(self.c, self.j), 6)
        self.assertIn(f"{DATE}relevé asn_attribution retenu (dernier par hôte, après filtre de lecture) : min "
                      f"{float(A)} = {iso} ; max {float(A)} = {iso} ; 2 / 3 hôtes du pool{DESCR}", b6)
        self.assertIn(f"{SANS}1 : {self.h}{FIN}", b6)
        self.assertIn(f"{SANS}0{FIN}", self.base)
        hs = sorted([self.h] + [self.malforme(f) for f in ("kraken", "bitstamp")])
        b6 = bloc(report.render_report(self.c, self.j), 6)
        self.assertIn(f"{DATE}non mesurée (aucun hôte du pool n'a de relevé asn_attribution retenu daté){DESCR}", b6)
        self.assertIn(f"{SANS}3 : {', '.join(hs)}{FIN}", b6)

    def test_releve_sans_ts_avec_filtre_refus_nomme(self):
        """Avec une plage, le relevé sans ts ne se place pas : refus nommé (ValueError), jamais KeyError. Rougit si :
        garde de filtre_horodatage retirée."""
        with self.assertRaisesRegex(ValueError, r"asn_attribution sans ts : placement .* indécidable"):
            report.render_report(self.c, self.j, exclude_ranges=[PLAGE])


if __name__ == "__main__":
    unittest.main()
