"""Étape B de la partie 2, B1 (G0-partie-2.md §B) : lecteur de journal en octets, décodage ligne par ligne
(SHOGEN-TORN-LINE-UTF8-1, HS2-03) ; relevé asn_attribution sans ts compté à part au bloc 6, jamais KeyError
(SHOGEN-BLOC6-TS-1). B2 : lecteur et oracle de raw.jsonl (SHOGEN-RAW-LECTEUR-1). Attendus écrits à la main. Chaque
test nomme le mutant qui le rougit."""

from __future__ import annotations

import contextlib
import io
import json
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


class TestTsNumerique(unittest.TestCase):
    def test_ts_non_numerique_ou_non_fini_refus_nomme(self):
        """SHOGEN-BLOC6-TS-NUM-1 (G2, C-8) : relevé asn_attribution sous segment, ts lu par json.loads : true, NaN,
        Infinity, "abc", "1787770900" : refus nommé (ValueError) ; entier ou flottant fini : retenu. Rougit si le
        contrôle est retiré (écarté en silence, ou TypeError anonyme)."""
        seg = (1787770800, 1788980400)
        for brut, refus in (("true", 1), ("NaN", 1), ("Infinity", 1), ('"abc"', 1), ('"1787770900"', 1),
                            ("1787770900", 0), ("1787770900.5", 0)):
            rec = json.loads('{"record": "asn_attribution", "host": "h", "ts": ' + brut + "}")
            with self.subTest(ts=brut):
                if refus:
                    with self.assertRaisesRegex(ValueError, r"non numérique ou non fini .*SHOGEN-BLOC6-TS-NUM-1"):
                        records.filtre_horodatage([rec], (), 60, seg)
                else:
                    self.assertEqual(records.filtre_horodatage([rec], (), 60, seg), [rec])

    def test_trois_champs_sous_segment_ou_plage_seule(self):
        """C-2 de R-C (SHOGEN-TESTS-C8-SUITE-1) : même refus nommé pour window_start (window_close), harness_ts
        (clock_check) et ts (asn_attribution), sous segment comme sous une plage seule. Rougit si le contrôle ne vaut
        que pour ts (M30 de R-C) ou que sous segment (M29)."""
        seg, pl = (1787770800, 1788980400), [(1787770860, 1787770920)]
        for rec, champ in (("window_close", "window_start"), ("clock_check", "harness_ts"), ("asn_attribution", "ts")):
            for brut in ("true", "NaN", '"1787770900"'):
                r = json.loads(f'{{"record": "{rec}", "{champ}": {brut}}}')
                for plages, segment in (((), seg), (pl, None)):
                    with self.subTest(champ=champ, brut=brut, plages=plages), self.assertRaisesRegex(
                            ValueError, r"non numérique ou non fini .*SHOGEN-BLOC6-TS-NUM-1"):
                        records.filtre_horodatage([r], plages, 60, segment)



class TestRawLecteur(unittest.TestCase):
    """SHOGEN-RAW-LECTEUR-1 sur la fixture d'exclusion (9 fenêtres × 3 flux, octets gelés) ; une altération par cas,
    sur une copie réécrite objet par objet."""

    @classmethod
    def setUpClass(cls):
        cls.d = tempfile.mkdtemp(prefix="s2raw_")
        build_fixture(cls.d)

    def copie(self, nom: str, f) -> tuple:
        """Copie raw.jsonl et journal.jsonl ; dans `nom`, f(rang, objet) rend l'objet, ou None (ligne retirée)."""
        d = tempfile.mkdtemp(prefix="s2raw_")
        for n in ("raw.jsonl", "journal.jsonl"):
            with open(os.path.join(self.d, n), encoding="utf-8") as fe:
                objs = [json.loads(x) for x in fe]
            with open(os.path.join(d, n), "w", encoding="utf-8") as fs:
                fs.writelines(json.dumps(o, ensure_ascii=False) + "\n" for o in (
                    (f(i, o) for i, o in enumerate(objs)) if n == nom else objs) if o is not None)
        return os.path.join(d, "raw.jsonl"), os.path.join(d, "journal.jsonl")

    def test_conforme(self):
        """27 lectures, toutes à octets. Rougit si : sha256 pris sur le texte base64 ; compte faux."""
        att = {"lectures": 27, "avec_octets": 27}
        self.assertEqual(records.verifier_raw(*(os.path.join(self.d, n) for n in ("raw.jsonl", "journal.jsonl"))), att)

    def test_ecarts_refus_nommes(self):
        """b64 altéré (valide, autres octets), b64 invalide, sha de la ligne altéré, sha de journal.jsonl altéré,
        lecture absente de chaque côté, fetch_ts altéré : refus nommé. Rougit si : base64 non strict (« ! » ignoré) ;
        contrôle du sha de la ligne retiré ; correspondance avec journal.jsonl retirée ou sans fetch_ts ; écart mal
        nommé."""
        def un(**k):                                    # altère la première lecture seulement
            return lambda i, o: {**o, **{c: v(o) for c, v in k.items()}} if i == 0 else o
        rl, ab = r"^raw\.jsonl, lecture .* : ", r"^lecture\(s\) de {}\.jsonl absente\(s\) de {}"
        cas = (("raw.jsonl", un(raw_b64=lambda o: "AB"[o["raw_b64"][0] == "A"] + o["raw_b64"][1:]),
                rl + r"sha256 recalculé \w+ ≠ sha256_raw de la ligne"),
               ("raw.jsonl", un(raw_b64=lambda o: o["raw_b64"] + "!"), rl + "raw_b64 non décodable"),
               ("raw.jsonl", un(sha256_raw=lambda o: "0" * 64), rl + "sha256 recalculé .* de la ligne 0{64}"),
               ("journal.jsonl", un(sha256_raw=lambda o: "0" * 64), r"^sha256 des octets ≠ sha256_raw de journal"),
               ("raw.jsonl", lambda i, o: o if i else None, ab.format("journal", "raw")),
               ("journal.jsonl", lambda i, o: o if i else None, ab.format("raw", "journal")),
               ("raw.jsonl", un(fetch_ts=lambda o: o["fetch_ts"] + 1), ab.format("raw", "journal")))
        for k, (nom, f, motif) in enumerate(cas):
            with self.subTest(cas=k, nom=nom):
                with self.assertRaisesRegex(ValueError, motif):
                    records.verifier_raw(*self.copie(nom, f))


if __name__ == "__main__":
    unittest.main()
