"""Partie 2, C3 (G0 docs/adr-0028/G0-partie-2.md §C, décisions Q1 à Q8 et L3) : sorties de tools/rendu_unique.py,
commandes nommées de l'enregistreur. Fixtures seulement (D.4 a) : collecteur réel de tests/test_sensibilite.py, table
des sorties de fixture ; attendus écrits à la main (étiquettes, options, comptes) ou recalculés par les fonctions du
chemin de recalcul avec ces options ; un mutant par comportement (journal G1)."""
from __future__ import annotations

import argparse
import contextlib
import glob
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime
from decimal import Decimal, localcontext
from pathlib import Path
from unittest import mock

from shogen_s2 import lm, r1, r2, records, report
from tests.test_oracle_record import LINT, OUTIL as ENREGISTREUR, g
from tests import test_rendu_unique as tru
from tests.test_rendu_unique import (LOIN, OPENSSL, OUTIL, PAQUET, SCEAU, SCELLEMENT, epingler, h, monter, poser, ru,
                                     texte_bloc)
from tests.test_sensibilite import RA, fixture, t

TABLE = (("j14-principal", {"t0": t(7, 22), "t_fin": t(10, 2)}, (), "étiquette un"),        # table de fixture
         ("j14-second", {"t0": t(7, 22), "t_fin": t(8, 23)}, (), "étiquette deux"),
         ("j28", {"t0": t(7, 22), "n_fixe": 60}, (RA,), "étiquette trois"))
JETON = "SHOGEN_RENDU_PRODUCTION"       # C-1 du G2 : jeton de production (temporaire voisin), écrit à la main
ENVELOPPE = ("import ast, importlib.util, sys\ns = importlib.util.spec_from_file_location('ru', sys.argv[1])\n"
             "ru = importlib.util.module_from_spec(s)\ns.loader.exec_module(ru)\n"
             "ru.SORTIES = ast.literal_eval(sys.argv[2])\nraise SystemExit(ru.main(sys.argv[3:]))\n")


def produire(*args) -> tuple:
    """rendu_unique --produire en processus, jeton de production posé : (code, octets écrits sur la sortie standard)."""
    buf = io.BytesIO()
    with contextlib.redirect_stdout(io.TextIOWrapper(buf, encoding="utf-8")) as w, mock.patch.dict(
            os.environ, {JETON: tempfile.mkdtemp(prefix=".")}):
        code = ru.main(["--produire", *args])
        w.flush()
        return code, buf.getvalue()


def chaine(d) -> str:
    if isinstance(d, Decimal):
        return str(d)
    raise TypeError(f"{type(d).__name__} hors JSON")


def en_json(x):
    """Sortie de recompute_* telle qu'un JSON la relit (Decimal en chaîne, tuples en listes)."""
    with localcontext(r1.contexte_decimal()):
        return json.loads(json.dumps(x, default=chaine))


class TestSortiesNommees(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = tempfile.mkdtemp(prefix="s2prod_")
        cls.c, cls.j = fixture(cls.d)

    def test_table_reelle_constantes(self):
        """SHOGEN-RENDU-TABLE-REELLE-1 et décisions Q1 à Q4 : bornes recalculées ici depuis les dates d'ADR-0028 (D4,
        D2 pt 6, D5), étiquettes du G0 §C ; commandes nommées de l'enregistreur ; noms des journaux (L3). Rougit si une
        borne, une plage, une étiquette (J28 complétée : G2 C-7, décision Q-3), l'ordre ou une commande nommée
        diffère."""
        ep = lambda s: int(datetime.fromisoformat(s + "+00:00").timestamp())
        t0, hors = ep("2026-08-26T19:00:00"), " ; plage D5 non passée : hors du segment (D2 pt 6 l'applique au J28)"
        self.assertEqual(ru.SORTIES, (
            ("j14-principal", {"t0": t0, "t_fin": ep("2026-09-09T19:00:00")}, (),
             "hors décision, non confirmatoire (ADR-0028 D4, §1 bis.1 pt 9)" + hors),
            ("j14-second", {"t0": t0, "t_fin": ep("2026-09-04T00:00:00") + 60}, (),
             "sensibilité de la liste fermée (seconde coupe, décision 270), hors décision, non confirmatoire" + hors),
            ("j28", {"t0": t0, "n_fixe": 38600}, ((ep("2026-09-24T18:18:00"), ep("2026-09-26T15:08:00")),),
             "segment confirmatoire de la règle SHOGEN-CRITERE-R1-1 (D2 pt 6) ; la section [SENSIBILITÉ] (plage "
             "incluse) est hors décision, biaisée vers le haut par construction ; hors décision aussi (§1 bis.1 pt "
             "9) : L&M (bloc 4), queues exactes, strate poolée, diagnostic de runs et drapeau « run maximal ≥ ℓ »")))
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
        rendu J28 ; clé etiquette de chaque entrée (celle de la table ; texte écrit ici pour la variante incluse, G2
        C-7). Rougit si : un recompute manque, options autres, variante incluse absente ou sous plage, étiquette
        autre."""
        with mock.patch.object(ru, "SORTIES", TABLE):
            code, octets = produire("recalcul-tiers", "--journaux", self.d)
        out = json.loads(octets)
        incluse = ("sensibilité « plage incluse » de la liste fermée (D2 pt 7), hors décision, biaisée vers le haut "
                   "par construction")
        var = [(n, s, pl, e) for n, s, pl, e in TABLE] + [("j28-incluse", TABLE[2][1], (), incluse)]
        self.assertEqual((code, list(out), out["avertissements"]), (0, ["avertissements", *sorted(n for n, *_ in var)],
                                                                    []))
        for n, s, pl, e in var:
            attendu = en_json({"etiquette": e, "segment": s, "plages": [list(x) for x in pl], **{
                k: f(self.c, self.j, pl, s) for k, f in (
                    ("r1", r1.recompute_from_journal), ("d5", r1.recompute_d5_from_journal),
                    ("lm", lm.recompute_lm_from_journal), ("r2", r2.recompute_r2_from_journal))}})
            if n == "j28-incluse":              # SHOGEN-RT-ETIQUETTE-INCLUSE-1 (test suivant)
                attendu["r2"]["drapeau_2"]["etiquette"] = incluse
            with self.subTest(sortie=n):
                self.assertEqual(out[n], attendu)
        sens = report.render_report(self.c, self.j, exclude_ranges=[RA], segment=TABLE[2][1]).split("[SENSIBILITÉ]")[1]
        for st, b in out["j28-incluse"]["r1"]["strates"].items():
            self.assertIn(f"  {st:8} {'incluse (sensibilité)':22} : n = {b['n']} ; K = {b['K']} ; ", sens)

    def test_r1_discrimine_de_la_variante_incluse_etiquete(self):
        """SHOGEN-RT-ETIQUETTE-INCLUSE-1 (annexe B.46 ; docs/11 point 10) : dans le JSON du recalcul tiers, le drapeau
        2 de la variante incluse, qui porte « R1 discrimine », porte aussi l'étiquette de la variante (clé etiquette,
        comme la strate poolée) ; aucune autre entrée n'en reçoit ; valeur de r1_discrimine inchangée. Texte écrit
        ici. Rougit si : étiquette absente, autre, ou posée sur une entrée de la table ; valeur modifiée."""
        with mock.patch.object(ru, "SORTIES", TABLE):
            out = json.loads(produire("recalcul-tiers", "--journaux", self.d)[1])
        incluse = ("sensibilité « plage incluse » de la liste fermée (D2 pt 7), hors décision, biaisée vers le haut "
                   "par construction")
        d2 = {n: out[n]["r2"]["drapeau_2"] for n in ("j14-principal", "j14-second", "j28", "j28-incluse")}
        self.assertEqual({n: d.get("etiquette") for n, d in d2.items()},
                         {"j14-principal": None, "j14-second": None, "j28": None, "j28-incluse": incluse})
        self.assertEqual(d2["j28-incluse"]["r1_discrimine"],
                         r2.recompute_r2_from_journal(self.c, self.j, (), TABLE[2][1])["drapeau_2"]["r1_discrimine"])

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
        p = subprocess.run([sys.executable, "-B", OUTIL, "--produire", "raw", "--journaux", k], capture_output=True,
                           env={**os.environ, JETON: tempfile.mkdtemp(prefix=".")})
        self.assertEqual((p.returncode, p.stdout.decode("utf-8").startswith(f"{tete}refus — raw.jsonl, lecture ")),
                         (0, True), p.stderr)
        self.assertNotIn("conforme", p.stdout.decode("utf-8"))
        self.assertTrue(records.verifier_raw(os.path.join(self.d, "raw.jsonl"), self.j))

    def test_raw_refus_sans_chemin_des_journaux(self):
        """SHOGEN-RAW-CHEMIN-1 (B-1 de R-C) : raw.jsonl à ligne 2 coupée (non finale), mêmes journaux dans deux
        dossiers : code 0, verdict de refus identique à l'octet, journal nommé sans dossier. Rougit si le chemin des
        journaux reste dans le verdict (octets dépendants de l'hôte)."""
        sorties = []
        for d in (tempfile.mkdtemp(), tempfile.mkdtemp()):
            for n in ("control.jsonl", "journal.jsonl"):
                Path(d, n).write_bytes(Path(self.d, n).read_bytes())
            raw = Path(self.d, "raw.jsonl").read_bytes().split(b"\n")
            Path(d, "raw.jsonl").write_bytes(b"\n".join([raw[0], raw[1][:20], *raw[2:]]))
            sorties.append(produire("raw", "--journaux", d))
        self.assertEqual(sorties, [(0, "verdict raw.jsonl (records.verifier_raw ; SHOGEN-RAW-FIN-1) : refus — ligne "
                                   "JSON corrompue NON finale dans raw.jsonl (ligne 2) : recalcul impossible "
                                   "(fail-closed)\n".encode("utf-8"))] * 2)

    def test_produire_reserve_a_l_execution_unique(self):
        """C-1 (G2 de la partie 2) : --produire j14-principal, recalcul-tiers et raw en sous-processus (table de
        fixture) : sans SHOGEN_RENDU_PRODUCTION, vide, ou sur un répertoire dont le nom ne commence pas par un point,
        un chemin absent ou un fichier : code 2, sortie standard vide, motif sur stderr ; sur un répertoire existant
        dont le nom commence par un point : code 0. Rougit si le contrôle est retiré ou relâché."""
        point, sans = tempfile.mkdtemp(prefix="."), tempfile.mkdtemp()
        Path(sans, ".f").write_bytes(b"")
        env = {k: v for k, v in os.environ.items() if k != JETON}         # héritée dans la production : retirée
        for nom in ("j14-principal", "recalcul-tiers", "raw"):
            for v in (None, "", sans, os.path.join(sans, ".absent"), os.path.join(sans, ".f"), point):
                p = subprocess.run([sys.executable, "-B", "-c", ENVELOPPE, OUTIL, repr(TABLE), "--produire", nom,
                                    "--journaux", self.d], capture_output=True,
                                   env={**env, **({} if v is None else {JETON: v})})
                with self.subTest(nom=nom, valeur=v):
                    self.assertEqual((p.returncode, p.stdout == b"", "réservée à l'exécution unique" in p.stderr.decode(
                        "utf-8")), (0, False, False) if v == point else (2, True, True), p.stderr[-300:])

    def test_avertissements_du_lecteur_dans_les_sorties(self):
        """C-5 (G2) : dernière ligne de control.jsonl et de raw.jsonl tronquée, deux copies des journaux dans deux
        dossiers ; commandes lancées comme par l'enregistreur (stderr=STDOUT, jeton posé, table de fixture) : première
        ligne = étiquette (verdict pour raw), puis les lignes [AVERTISSEMENT DU LECTEUR] (nom du journal sans dossier),
        puis le rendu ; JSON de recalcul-tiers relisible, clé avertissements non vide ; sorties identiques à l'octet
        depuis les deux dossiers. Rougit si la capture ou la réécriture du préfixe du dossier sont retirées."""
        sorties, coupe, tete = [], b'{"record": "clock_check", "pha', "[AVERTISSEMENT DU LECTEUR] [s2-harness] "
        for d in (tempfile.mkdtemp(), tempfile.mkdtemp()):
            for n in ("control.jsonl", "journal.jsonl", "raw.jsonl"):
                Path(d, n).write_bytes(Path(self.d, n).read_bytes() + (coupe if n != "journal.jsonl" else b""))
            env = {**os.environ, JETON: tempfile.mkdtemp(prefix=".")}
            sorties.append({n: subprocess.run([sys.executable, "-B", "-c", ENVELOPPE, OUTIL, repr(TABLE), "--produire",
                                               n, "--journaux", d], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                              env=env).stdout.decode("utf-8") for n in [*(x[0] for x in TABLE),
                                                                                        "recalcul-tiers", "raw"]})
        self.assertEqual(sorties[0], sorties[1])
        for nom, *_x, etiq in TABLE:
            x = sorties[0][nom].split("\n")
            self.assertEqual((x[0], x[1].startswith(tete + "AVERTISSEMENT : dernière ligne tronquée ignorée dans "
                                                    "control.jsonl (ligne ")), (f"[ÉTIQUETTE] {nom} : {etiq}", True))
        self.assertTrue(json.loads(sorties[0]["recalcul-tiers"])["avertissements"])
        x = sorties[0]["raw"].split("\n")
        self.assertEqual((x[0].startswith("verdict raw.jsonl (records.verifier_raw ; SHOGEN-RAW-FIN-1) : conforme"),
                          x[1].startswith(tete) and " dans raw.jsonl (ligne " in x[1]), (True, True))

    def test_poolee_des_deux_variantes_du_j28_dans_le_recalcul_tiers(self):
        """SHOGEN-SENS-POOLEE-1 (annexe B.12, B.13 ; décision du lot DETTES-B1 : aucune ligne ajoutée à [SENSIBILITÉ]) :
        la strate poolée stratifiée des deux variantes du J28, plage exclue et plage incluse, est publiée par le JSON
        du recalcul tiers (clé r1.poolee de chaque entrée), étiquetée « exploratoire, hors famille, hors décision »,
        égale à celle de recompute_from_journal sous les options de la variante ; les deux diffèrent (n de la plage).
        Texte écrit ici. Rougit si : poolée absente d'une variante, étiquette autre, valeurs d'une autre variante."""
        with mock.patch.object(ru, "SORTIES", TABLE):
            out = json.loads(produire("recalcul-tiers", "--journaux", self.d)[1])
        po = {n: out[n]["r1"].get("poolee") for n in ("j28", "j28-incluse")}
        for n, pl in (("j28", (RA,)), ("j28-incluse", ())):
            with self.subTest(variante=n):
                self.assertEqual((po[n] or {}).get("etiquette"), "exploratoire, hors famille, hors décision")
                self.assertEqual(po[n], en_json(r1.recompute_from_journal(self.c, self.j, pl, TABLE[2][1])["poolee"]))
        self.assertNotEqual(po["j28"]["strates"], po["j28-incluse"]["strates"])


RUNS = ["suite", "j14-principal", "j14-second", "j28", "recalcul-tiers", "raw"]     # Q8 puis ordre de D.4 b


def lancer(f: dict, *plus: str) -> tuple:
    """main en processus (module f["ru"] si posé, C-2), sans --gardes-seules, horloge en 2100 : (code, sortie
    standard, stderr)."""
    m, out, err = f.get("ru", ru), io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = m.main(["--depot", f["depot"], "--paquet", f["paquet"], "--journaux", f["journaux"], "--sommes",
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


HARNAIS = os.path.dirname(os.path.dirname(OUTIL))
T_OK = b"import unittest\n\n\nclass T(unittest.TestCase):\n    def test_a(self):\n        pass\n"


def monter_prod(d: str) -> dict:
    """Dépôt jetable : commit c1 = shogen_s2/ et tools/ du harnais (seule la table des sorties de rendu_unique remplacée
    par TABLE), une suite triviale et le lint d'épinglage ; journaux du collecteur réel et sommes hors dépôt ; paquet,
    JOURNAL.md, go épinglé (voie (b), 2026-09-01) ; f["ru"] : module chargé depuis la copie du dépôt, dont le sha256
    est sha256_script (C-2)."""
    depot, jx = os.path.join(d, "depot"), os.path.join(d, "campagne")
    os.makedirs(depot), os.makedirs(jx), g(depot, "init", "-q"), g(depot, "config", "core.autocrlf", "false")
    src = Path(OUTIL).read_text(encoding="utf-8")
    for marque in ("# --- table des sorties", "# --- fin de la"):     # C-9 : une ligne de délimitation chacune
        if sum(x.startswith(marque) for x in src.split("\n")) != 1:
            raise AssertionError(f"délimiteur {marque!r} : une seule ligne exigée dans {OUTIL}")
    outil = src[:src.index("# --- table des sorties")] + f"SORTIES = {TABLE!r}\n" + src[src.index("# --- fin de la"):]
    code = ["tools/oracle_record.py"] + [f"shogen_s2/{n}" for n in os.listdir(os.path.join(HARNAIS, "shogen_s2"))
                                        if n.endswith(".py")]
    c1 = poser(depot, {".gitignore": b"__pycache__/\n", "s2-harness/tests/__init__.py": b"", "s2-harness/tests/"
                       "test_t.py": T_OK, "s2-harness/tools/rendu_unique.py": outil.encode(),
                       "enforcement/lint-model-pinning.sh": Path(LINT).read_bytes(),
                       **{f"s2-harness/{r}": Path(HARNAIS, r).read_bytes() for r in code}})
    fixture(jx)
    poser(jx, {"campagne.log": b"x\n", "segments.json": b"{}\n"}, commit=False)
    noms = ("control.jsonl", "journal.jsonl", "raw.jsonl", "campagne.log", "segments.json")
    sommes = "".join(f"{h(Path(jx, n).read_bytes())}  {n}\n" for n in noms).encode()
    poser(jx, {"SHA256SUMS.txt": sommes}, commit=False)
    paquet = texte_bloc([f"commit_analyse {c1}", f"sha256_script {h(outil.encode())}", *(
        f"journal {n} {h(Path(jx, n).read_bytes())}" for n in noms[:3]), f"sommes {h(sommes)}",
        "cacert_sha256 " + "1" * 64, "tsa_crt_sha256 " + "2" * 64]).encode()
    poser(depot, {PAQUET: paquet, "JOURNAL.md": f"- scellement du paquet : sha256 {h(paquet)}\n".encode()},
          date=SCELLEMENT)
    f = {"depot": depot, "paquet": os.path.join(depot, PAQUET), "journaux": jx, "sha": h(paquet), "c1": c1,
         "sommes": os.path.join(jx, "SHA256SUMS.txt")}
    epingler(f)
    s = importlib.util.spec_from_file_location("ru_depot", os.path.join(depot, "s2-harness/tools/rendu_unique.py"))
    f["ru"] = importlib.util.module_from_spec(s)
    with mock.patch.object(sys, "dont_write_bytecode", True):     # aucun __pycache__ dans le dépôt gardé
        s.loader.exec_module(f["ru"])
    return f


class TestProduction(unittest.TestCase):
    def test_echec_a_chaque_pas_rien_ne_reste(self):
        """Q8 : runs factices ; échec à chaque run, sortie altérée pendant le dernier run (relecture : refus sortie),
        .git/info/attributes posé pendant le dernier run (relecture : refus tree.sha256 ; C-11, R27), extraction ou
        renommage en échec : code 1, « gardes levées » seul sur la sortie standard, dossier parent inchangé, aucun run
        après l'échec, temporaire voisin de la sortie, heure et motif nommé sur stderr ; gardes refusées sans
        --gardes-seules : code 2, aucun run. Rougit si : temporaire ou sortie restés, arrêt absent, suite non première,
        relecture absente (ou sans --depot), temporaire hors du dossier parent, run en échec non nommé."""
        def pendant(nom):
            voisins.append(len(glob.glob(os.path.join(parent, ".sortie.*"))))
            if alterer and nom == "raw":
                alterer(f)
        nul, crlf = contextlib.nullcontext(), b"*.py eol=crlf\n"
        sortie_alteree = lambda f: [Path(x).write_bytes(b"altere") for x in glob.glob(os.path.join(
            os.path.dirname(f["depot"]), ".sortie.*", "*-j28.out"))]
        cas = [(n, n, None, nul) for n in RUNS] + [
            ("relecture", None, sortie_alteree, nul),
            ("attributs", None, lambda f: Path(f["depot"], ".git", "info", "attributes").write_bytes(crlf), nul),
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
                self.assertIn({"relecture": "refus (sortie)", "attributs": "refus (tree.sha256)",
                               "extraction": "factice", "renommage": "factice"}.get(
                    nom, f"run en échec : [('{nom}', 1)]"), err)
        f = monter(tempfile.mkdtemp())
        p, lances = faux_runs()
        with p:
            code, out, err = lancer(f)
        self.assertEqual((code, out, lances, os.path.exists(sortie(f))), (2, "", [], False))

    def test_cible_apparue_avant_le_renommage(self):
        """SHOGEN-RENDU-RENAME-POSIX-1 : répertoire vide posé à la place de --sortie pendant le dernier run, après le
        contrôle de destination et avant le renommage final : code 1, « gardes levées » seul sur la sortie standard,
        FileExistsError nommée sur stderr, tous les runs lancés, le répertoire posé reste vide, aucun temporaire
        voisin. Rougit si le renommage final remplace une cible apparue (os.rename seul, sous POSIX)."""
        f = monter(tempfile.mkdtemp())
        epingler(f)
        parent = os.path.dirname(f["depot"])
        avant = sorted(os.listdir(parent))
        p, lances = faux_runs(pendant=lambda nom: nom == "raw" and os.makedirs(sortie(f)))
        with p:
            code, out, err = lancer(f)
        self.assertEqual((code, out, lances, sorted(os.listdir(parent)), os.listdir(sortie(f))),
                         (1, "gardes levées\n", RUNS, sorted(avant + ["sortie"]), []))
        self.assertRegex(err, r"^rendu_unique : échec de production à \S+ : FileExistsError : ")

    def test_parent_de_la_sortie_absent(self):
        """SHOGEN-RENDU-MKDTEMP-1 (H-1 de R-C) : dossier parent de --sortie absent, gardes levées : « gardes levées »
        seul sur la sortie standard, « échec de production à <heure> : FileNotFoundError : … » sur stderr, code 1,
        aucun run, parent toujours absent. Rougit si le temporaire est créé hors du try (exception non rattrapée)."""
        f = monter(tempfile.mkdtemp())
        epingler(f)
        cible, (p, lances) = os.path.join(os.path.dirname(f["depot"]), "absent", "sortie"), faux_runs()
        out, err = io.StringIO(), io.StringIO()
        with p, contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = ru.main(["--depot", f["depot"], "--paquet", f["paquet"], "--journaux", f["journaux"], "--sommes",
                            f["sommes"], "--sortie", cible, "--auteur", "claude-opus-5-5"], maintenant=LOIN)
        self.assertEqual((code, out.getvalue(), lances, os.path.lexists(os.path.dirname(cible))),
                         (1, "gardes levées\n", [], False))
        self.assertRegex(err.getvalue(), r"^rendu_unique : échec de production à \S+ : FileNotFoundError : ")

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

    def test_script_hors_depot_enregistreur_voisin_modifie(self):
        """C-2 (sonde du réviseur) : copie du dépôt de rendu_unique.py lancée hors du dépôt, oracle_record.py voisin
        modifié (run suite retiré), lint d'épinglage copié : refus (4) seul, code 2, rien d'écrit. Rougit si
        l'enregistreur chargé n'est pas comparé à celui du commit gardé."""
        f, ailleurs, ancre = monter_prod(tempfile.mkdtemp()), tempfile.mkdtemp(), "    delai = DELAI_DEFAUT if "
        ru_, orc_ = "s2-harness/tools/rendu_unique.py", "s2-harness/tools/oracle_record.py"
        copie = {r: Path(f["depot"], r).read_bytes() for r in (ru_, orc_, "enforcement/lint-model-pinning.sh")}
        src, sans_suite = copie[orc_].decode("utf-8"), "    commandes = tuple(x for x in commandes if x != 'suite')\n"
        self.assertEqual(src.count(ancre), 1)
        copie[orc_] = src.replace(ancre, sans_suite + ancre).encode()
        poser(ailleurs, copie, commit=False)
        s = importlib.util.spec_from_file_location("ru_ailleurs", os.path.join(ailleurs, ru_))
        m = importlib.util.module_from_spec(s)
        s.loader.exec_module(m)
        avant = sorted(os.listdir(os.path.dirname(f["depot"])))
        code, out, err = lancer({**f, "ru": m})
        self.assertEqual((code, out, re.findall(r"^rendu_unique : refus (\S+) : ", err, re.M),
                          sorted(os.listdir(os.path.dirname(f["depot"])))), (2, "", ["(4)"], avant))

    def test_head_lu_une_fois_production_sur_le_commit_garde(self):
        """C-2 (sonde du réviseur) : gardes levées sur X ; un commit Y retire le sha du paquet de JOURNAL.md et change
        le code d'analyse ; production (runs factices) avec le contexte des gardes : code 0, tree.commit = X, jamais Y.
        Rougit si l'enregistreur ou la relecture relisent HEAD."""
        f = monter(tempfile.mkdtemp())
        epingler(f)
        refus, c = ru.evaluer_gardes(f["depot"], f["paquet"], f["journaux"], f["sommes"], LOIN)
        x = g(f["depot"], "rev-parse", "HEAD")
        y = poser(f["depot"], {"JOURNAL.md": b"- rien\n", "s2-harness/shogen_s2/m.py": b"x = 2\n"})
        a = argparse.Namespace(deviation=None, auteur="claude-opus-5-5", journaux=f["journaux"], sortie=sortie(f))
        p, _ = faux_runs()
        with p, contextlib.redirect_stdout(io.StringIO()):
            code = ru.produire_tout(c, a, sortie(f))
        self.assertEqual((refus, code, x != y), ([], 0, True))
        (chemin,) = glob.glob(os.path.join(sortie(f), "*.json"))
        self.assertEqual(json.loads(Path(chemin).read_text(encoding="utf-8"))["tree"]["commit"], x)

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

    def test_nominal_bout_en_bout(self):
        """Q5, Q8 : runs réels de l'enregistreur sur l'extraction d'un dépôt jetable qui porte le code d'analyse : code
        0, temporaire renommé (seul ajout au dossier parent), runs dans l'ordre RUNS, chaque sortie égale à son attendu,
        enregistrement conforme à oracle_record --verifier (rôle rendu, --depot), paquet.sha256, genTime nul (voie
        (b)), base = commit d'analyse ; sortie standard : chemins et sha256 seulement. Rougit si l'un diffère."""
        f = monter_prod(tempfile.mkdtemp())
        parent = os.path.dirname(f["depot"])
        avant = sorted(os.listdir(parent))
        code, out, err = lancer(f)
        self.assertEqual((code, sorted(os.listdir(parent))), (0, sorted(avant + ["sortie"])), err)
        (chemin,) = glob.glob(os.path.join(sortie(f), "*.json"))
        rec, sha = json.loads(Path(chemin).read_text(encoding="utf-8")), g(f["depot"], "rev-parse", "HEAD")
        self.assertEqual(([r["nom"] for r in rec["runs"]], rec["paquet"], rec["sceau"], rec["base"], rec["role"]),
                         (RUNS, {"sha256": f["sha"]}, {"genTime": None}, f["c1"], "rendu"))
        v = subprocess.run([sys.executable, "-B", ENREGISTREUR, "--verifier", chemin, "--role", "rendu", "--commit",
                            sha, "--depot", f["depot"]], capture_output=True, text=True)
        self.assertEqual(v.returncode, 0, v.stderr)
        lu = {r["nom"]: Path(sortie(f), r["sortie"]["chemin"]).read_bytes() for r in rec["runs"]}
        c, j = (os.path.join(f["journaux"], n) for n in ("control.jsonl", "journal.jsonl"))
        for nom, seg, pl, etiq in TABLE:
            txt = report.render_report(c, j, exclude_ranges=pl, segment=seg)
            self.assertEqual(lu[nom], f"[ÉTIQUETTE] {nom} : {etiq}\n{txt}\n".encode("utf-8"))
        self.assertIn(b"test_a (tests.test_t.T.test_a) ... ok", lu["suite"])
        incluse = en_json(r1.recompute_from_journal(c, j, (), TABLE[2][1]))
        self.assertEqual(json.loads(lu["recalcul-tiers"])["j28-incluse"]["r1"], incluse)
        self.assertTrue(lu["raw"].startswith("verdict raw.jsonl (records.verifier_raw ; SHOGEN-RAW-FIN-1) : "
                                             "conforme".encode("utf-8")))
        self.assertEqual(out, affichage(sortie(f), chemin))


if __name__ == "__main__":
    unittest.main()
