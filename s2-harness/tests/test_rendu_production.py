"""Partie 2, C3 (G0 docs/adr-0028/G0-partie-2.md §C, décisions Q1 à Q8 et L3) : sorties de tools/rendu_unique.py,
commandes nommées de l'enregistreur. Fixtures seulement (D.4 a) : collecteur réel de tests/test_sensibilite.py, table
des sorties de fixture ; attendus écrits à la main (étiquettes, options, comptes) ou recalculés par les fonctions du
chemin de recalcul avec ces options ; un mutant par comportement (journal G1)."""
from __future__ import annotations

import contextlib
import glob
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
from tests import test_rendu_unique as tru
from tests.test_rendu_unique import LOIN, OPENSSL, OUTIL, SCEAU, epingler, h, monter, ru
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


RUNS = ["suite", "j14-principal", "j14-second", "j28", "recalcul-tiers", "raw"]     # Q8 puis ordre de D.4 b


def lancer(f: dict, *plus: str) -> tuple:
    """main en processus, sans --gardes-seules, horloge en 2100 : (code, sortie standard, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = ru.main(["--depot", f["depot"], "--paquet", f["paquet"], "--journaux", f["journaux"], "--sommes",
                        f["sommes"], "--sortie", sortie(f), "--auteur", "claude-opus-5-5", *plus], maintenant=LOIN)
    return code, out.getvalue(), err.getvalue()


def sortie(f: dict) -> str:
    return os.path.join(os.path.dirname(f["depot"]), "sortie")


def faux_runs(echec=None, pendant=lambda nom: None) -> tuple:
    """Runs de l'enregistreur (commandes lancées par sys.executable) remplacés : sortie factice, code 1 au run echec,
    pendant(nom) appelé avant chaque run ; git et openssl passent au vrai subprocess.run. Rend (patch, runs lancés)."""
    vrai, lances = subprocess.run, []

    def faux(cmd, *a, **k):
        if cmd[0] != sys.executable:
            return vrai(cmd, *a, **k)
        lances.append("suite" if "unittest" in cmd else cmd[cmd.index("--produire") + 1])
        pendant(lances[-1])
        return subprocess.CompletedProcess(cmd, int(lances[-1] == echec), f"sortie factice {lances[-1]}\n".encode())
    return mock.patch.object(subprocess, "run", faux), lances


def affichage(cible: str, chemin: str) -> str:
    """Sortie standard attendue (voie (b), go du 2026-09-01) : chemins et sha256 lus dans l'enregistrement relu."""
    rec = json.loads(Path(chemin).read_text(encoding="utf-8"))
    return (f"gardes levées\nsorties : {cible} (voie b ; T0 2026-09-01T00:00:00Z ; genTime -)\n" + "".join(
        f"  {r['nom']} {r['sortie']['sha256']} {r['sortie']['chemin']}\n" for r in rec["runs"])
        + f"  enregistrement {h(Path(chemin).read_bytes())} {os.path.basename(chemin)}\n")


def fichiers(d: str) -> dict:
    return {n: h(Path(d, n).read_bytes()) for n in sorted(os.listdir(d))}


class TestProduction(unittest.TestCase):
    def test_echec_a_chaque_pas_rien_ne_reste(self):
        """Q8 : runs factices ; échec à chaque run, sortie altérée pendant le dernier run (relecture : refus sortie),
        extraction ou renommage en échec : code 1, « gardes levées » seul sur la sortie standard, dossier parent
        inchangé, aucun run après l'échec, temporaire voisin de la sortie, heure et motif nommé sur stderr ; gardes
        refusées sans --gardes-seules : code 2, aucun run. Rougit si : temporaire ou sortie restés, arrêt absent, suite
        non première, relecture absente, temporaire hors du dossier parent, run en échec non nommé."""
        def pendant(nom):
            voisins.append(len(glob.glob(os.path.join(parent, ".sortie.*"))))
            for x in glob.glob(os.path.join(parent, ".sortie.*", "*-j28.out")) if alterer and nom == "raw" else ():
                Path(x).write_bytes(b"altere")
        nul = contextlib.nullcontext()
        cas = [(n, n, False, nul) for n in RUNS] + [
            ("relecture", None, True, nul),
            ("extraction", None, False, mock.patch.object(ru.orc, "extraire", side_effect=ValueError("factice"))),
            ("renommage", None, False, mock.patch.object(ru.os, "rename", side_effect=OSError("factice")))]
        for nom, echec, alterer, autre in cas:
            f, voisins = monter(tempfile.mkdtemp()), []
            epingler(f)
            parent = os.path.dirname(f["depot"])
            avant = sorted(os.listdir(parent))
            p, lances = faux_runs(echec, pendant)
            with p, autre:
                code, out, err = lancer(f)
            runs = [] if nom == "extraction" else RUNS[:RUNS.index(echec) + 1] if echec else RUNS
            with self.subTest(cas=nom):
                self.assertEqual((code, out, sorted(os.listdir(parent)), lances, set(voisins) <= {1}),
                                 (1, "gardes levées\n", avant, runs, True))
                self.assertRegex(err, r"^rendu_unique : échec de production à \d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ : ")
                self.assertIn({"relecture": "refus (sortie)", "extraction": "factice", "renommage": "factice"}.get(
                    nom, f"run en échec : [('{nom}', 1)]"), err)
        f = monter(tempfile.mkdtemp())
        p, lances = faux_runs()
        with p:
            code, out, err = lancer(f)
        self.assertEqual((code, out, lances, os.path.exists(sortie(f))), (2, "", [], False))

    def test_deviation_seconde_sortie_premiere_intacte(self):
        """D.4 b, G0 §C : première exécution (runs factices) écrite ; relance sans --deviation : refus sortie, rien
        d'écrit ; avec --deviation : <sortie>.deviation-1, avec DEVIATION.txt (motif, première sortie), première sortie
        intacte octet pour octet ; sortie standard : chemins et sha256 de l'enregistrement relu, aucun contenu. Rougit
        si : écrasement, motif non écrit, autre répertoire, contenu imprimé."""
        f = monter(tempfile.mkdtemp())
        epingler(f)
        p, _ = faux_runs()
        with p:
            self.assertEqual(lancer(f)[0], 0)
            premiere = fichiers(sortie(f))
            self.assertEqual(lancer(f)[:2], (2, ""))
            code, out, err = lancer(f, "--deviation", "relance déclarée")
        dev = sortie(f) + ".deviation-1"
        self.assertEqual((code, fichiers(sortie(f)), out), (0, premiere, affichage(dev, *glob.glob(f"{dev}/*.json"))))
        self.assertEqual(Path(dev, "DEVIATION.txt").read_text(encoding="utf-8"), "seconde exécution déclarée (ADR-0028 "
                         f"annexe D.4 b) ; première : {sortie(f)} ; motif : relance déclarée\n")

    def test_gentime_du_jeton_dans_l_enregistrement(self):
        """SHOGEN-RENDU-T0-1 : voie (a) (autorité de test d'openssl), runs factices : sceau.genTime = genTime du jeton,
        lu ici dans openssl ts -reply -text ; paquet.sha256 = sha du paquet ; base = commit d'analyse. Rougit si genTime
        manque ou diffère."""
        self.assertTrue(OPENSSL, "openssl absent : le test échoue, il ne saute pas (G0 §C, risque (a))")
        f, _, _, pref = tru.TestRenduUnique.voie_a(None, tempfile.mkdtemp())     # fixture de la voie (a), sans self
        x = subprocess.run([OPENSSL, "ts", "-reply", "-in", os.path.join(f["depot"], SCEAU, "paquet.tsr"), "-text"],
                           capture_output=True, text=True).stdout.split("Time stamp: ")[1].split("\n")[0]
        jeton = datetime.strptime(x, "%b %d %H:%M:%S %Y GMT").strftime("%Y-%m-%dT%H:%M:%SZ")
        p, _ = faux_runs()
        with p, mock.patch.dict(ru.PREFIXES, pref):
            self.assertEqual(lancer(f)[0], 0)
        (chemin,) = glob.glob(os.path.join(sortie(f), "*.json"))
        rec = json.loads(Path(chemin).read_text(encoding="utf-8"))
        self.assertEqual((rec["sceau"], rec["paquet"], rec["base"]),
                         ({"genTime": jeton}, {"sha256": f["sha"]}, f["c1"]))



if __name__ == "__main__":
    unittest.main()
