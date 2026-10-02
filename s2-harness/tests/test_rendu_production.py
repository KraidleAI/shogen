"""Partie 2, C3 (G0 docs/adr-0028/G0-partie-2.md §C, décisions Q1 à Q8 et L3) : sorties de tools/rendu_unique.py,
commandes nommées de l'enregistreur. Fixtures seulement (D.4 a) : collecteur réel de tests/test_sensibilite.py, table
des sorties de fixture ; attendus écrits à la main (étiquettes, options, comptes) ou recalculés par les fonctions du
chemin de recalcul avec ces options ; un mutant par comportement (journal G1)."""
from __future__ import annotations

import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime
from decimal import Decimal, localcontext
from pathlib import Path
from unittest import mock

from shogen_s2 import lm, r1, r2, records, report
from tests.test_rendu_unique import OUTIL, ru
from tests.test_sensibilite import RA, fixture, t

TABLE = (("j14-principal", {"t0": t(7, 22), "t_fin": t(10, 2)}, (), "étiquette un"),        # table de fixture
         ("j14-second", {"t0": t(7, 22), "t_fin": t(8, 23)}, (), "étiquette deux"),
         ("j28", {"t0": t(7, 22), "n_fixe": 60}, (RA,), "étiquette trois"))


def produire(*args) -> tuple:
    """rendu_unique --produire en processus : (code, octets écrits sur la sortie standard)."""
    buf = io.BytesIO()
    with contextlib.redirect_stdout(io.TextIOWrapper(buf, encoding="utf-8")) as w:
        code = ru.main(["--produire", *args])
        w.flush()
        return code, buf.getvalue()


def chaine(d) -> str:
    if isinstance(d, Decimal):
        return str(d)
    raise TypeError(f"{type(d).__name__} hors JSON")


def en_json(x):
    """Sortie de recompute_* telle qu'un JSON la relit (Decimal en chaîne, tuples en listes)."""
    with localcontext(r1.CONTEXTE_DECIMAL):
        return json.loads(json.dumps(x, default=chaine))


class TestSortiesNommees(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = tempfile.mkdtemp(prefix="s2prod_")
        cls.c, cls.j = fixture(cls.d)

    def test_table_reelle_constantes(self):
        """SHOGEN-RENDU-TABLE-REELLE-1 et décisions Q1 à Q4 : bornes recalculées ici depuis les dates d'ADR-0028 (D4,
        D2 pt 6, D5), étiquettes du G0 §C ; commandes nommées de l'enregistreur ; noms des journaux (L3). Rougit si une
        borne, une plage, une étiquette, l'ordre ou une commande nommée diffère."""
        ep = lambda s: int(datetime.fromisoformat(s + "+00:00").timestamp())
        t0, hors = ep("2026-08-26T19:00:00"), " ; plage D5 non passée : hors du segment (D2 pt 6 l'applique au J28)"
        self.assertEqual(ru.SORTIES, (
            ("j14-principal", {"t0": t0, "t_fin": ep("2026-09-09T19:00:00")}, (),
             "hors décision, non confirmatoire (ADR-0028 D4, §1 bis.1 pt 9)" + hors),
            ("j14-second", {"t0": t0, "t_fin": ep("2026-09-04T00:00:00") + 60}, (),
             "sensibilité de la liste fermée (seconde coupe, décision 270), hors décision, non confirmatoire" + hors),
            ("j28", {"t0": t0, "n_fixe": 38600}, ((ep("2026-09-24T18:18:00"), ep("2026-09-26T15:08:00")),),
             "segment confirmatoire de la règle SHOGEN-CRITERE-R1-1 (D2 pt 6) ; la section [SENSIBILITÉ] (plage "
             "incluse) est hors décision, biaisée vers le haut par construction")))
        self.assertEqual(ru.NOMS_JOURNAUX, ("control.jsonl", "journal.jsonl", "raw.jsonl"))
        for n in ("j14-principal", "j14-second", "j28", "recalcul-tiers", "raw"):
            self.assertEqual(ru.orc.COMMANDES[n], ("s2-harness", ["-B", "tools/rendu_unique.py", "--produire", n,
                                                                   "--journaux", ru.orc.JOURNAUX]))

    def test_sortie_etiquette_puis_rendu(self):
        """Q1, Q2, Q4 : chaque sortie de la table = « [ÉTIQUETTE] <nom> : <étiquette> », puis render_report avec ses
        seules options (plage au J28 seul : section [SENSIBILITÉ] présente là seulement). Rougit si : étiquette absente
        ou autre, segment ou plages non transmis, plage passée aux J14."""
        with mock.patch.object(ru, "SORTIES", TABLE):
            for nom, seg, pl, etiq in TABLE:
                txt = report.render_report(self.c, self.j, exclude_ranges=pl, segment=seg)
                with self.subTest(sortie=nom):
                    self.assertEqual(produire(nom, "--journaux", self.d),
                                     (0, f"[ÉTIQUETTE] {nom} : {etiq}\n{txt}\n".encode("utf-8")))
                    self.assertEqual("[SENSIBILITÉ]" in txt, bool(pl))

    def test_recalcul_tiers_quatre_recompute_et_variante_incluse(self):
        """Q6 : JSON des quatre recompute_* (r1, d5 avec la ventilation de B5, lm, r2) par sortie, mêmes options,
        plus la variante sans plage du J28 ; ses n et K égaux aux lignes « incluse » de la section [SENSIBILITÉ] du
        rendu J28. Rougit si : un recompute manque, options autres, variante incluse absente ou sous plage."""
        with mock.patch.object(ru, "SORTIES", TABLE):
            code, octets = produire("recalcul-tiers", "--journaux", self.d)
        out = json.loads(octets)
        var = [(n, s, pl) for n, s, pl, _ in TABLE] + [("j28-incluse", TABLE[2][1], ())]
        self.assertEqual((code, list(out)), (0, sorted(n for n, *_ in var)))
        for n, s, pl in var:
            with self.subTest(sortie=n):
                self.assertEqual(out[n], en_json({"segment": s, "plages": [list(x) for x in pl], **{
                    k: f(self.c, self.j, pl, s) for k, f in (
                        ("r1", r1.recompute_from_journal), ("d5", r1.recompute_d5_from_journal),
                        ("lm", lm.recompute_lm_from_journal), ("r2", r2.recompute_r2_from_journal))}}))
        sens = report.render_report(self.c, self.j, exclude_ranges=[RA], segment=TABLE[2][1]).split("[SENSIBILITÉ]")[1]
        for st, b in out["j28-incluse"]["r1"]["strates"].items():
            self.assertIn(f"  {st:8} {'incluse (sensibilité)':22} : n = {b['n']} ; K = {b['K']} ; ", sens)

    def test_raw_verdict_et_exit_0(self):
        """Q7, SHOGEN-RAW-FIN-1 : verdict de records.verifier_raw écrit sur la sortie, code 0 conforme comme en refus
        (sha256 d'une lecture altéré dans une copie) ; comptes recomptés ici dans raw.jsonl. Rougit si : refus en code
        non nul, verdict ou comptes absents."""
        lignes = [json.loads(x) for x in Path(self.d, "raw.jsonl").read_text(encoding="utf-8").splitlines()]
        tete = "verdict raw.jsonl (records.verifier_raw ; SHOGEN-RAW-FIN-1) : "
        self.assertEqual(produire("raw", "--journaux", self.d), (0, (
            f"{tete}conforme — lectures {len(lignes)} ; avec octets "
            f"{sum(x.get('raw_b64') is not None for x in lignes)}\n").encode("utf-8")))
        k = tempfile.mkdtemp(dir=self.d)
        for n in ("control.jsonl", "journal.jsonl"):
            Path(k, n).write_bytes(Path(self.d, n).read_bytes())
        x = next(i for i, y in enumerate(lignes) if y.get("raw_b64") is not None)
        lignes[x]["sha256_raw"] = "0" * 64
        Path(k, "raw.jsonl").write_text("".join(json.dumps(y) + "\n" for y in lignes), encoding="utf-8")
        p = subprocess.run([sys.executable, "-B", OUTIL, "--produire", "raw", "--journaux", k], capture_output=True)
        self.assertEqual((p.returncode, p.stdout.decode("utf-8").startswith(f"{tete}refus — raw.jsonl, lecture ")),
                         (0, True), p.stderr)
        self.assertNotIn("conforme", p.stdout.decode("utf-8"))
        self.assertTrue(records.verifier_raw(os.path.join(self.d, "raw.jsonl"), self.j))


if __name__ == "__main__":
    unittest.main()
