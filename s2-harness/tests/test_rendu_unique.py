"""SHOGEN-RENDU-UNIQUE-1 (G0 docs/adr-0028/G0-partie-2.md §C ; ADR-0028 annexe D.4 b) : tools/rendu_unique.py sur
dépôts git jetables (core.autocrlf=false ; fixtures seulement, D.4 a). Attendus indépendants de l'outil : sha256 des
octets écrits par le test, sha de git rev-parse, noms des gardes écrits à la main ; mutants par garde : journal G1."""
from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

from tests.test_oracle_record import GIT_ENV, HARNESS, g

OUTIL = os.path.join(HARNESS, "tools", "rendu_unique.py")
_SPEC = importlib.util.spec_from_file_location("rendu_unique", OUTIL)
ru = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(ru)
JOURNAUX = {"control.jsonl": b'{"type": "run_params"}\n', "journal.jsonl": b'{"v": 1}\n', "raw.jsonl": b'{"r": 2}\n'}
SOMMES = {**JOURNAUX, "campagne.log": b"x\n", "segments.json": b"{}\n"}     # cinq entrées au fichier de sommes
PAQUET, ORDRE = "docs/adr-0028/PAQUET-PREREG-S2.md", ["bloc", "(1)", "(2)", "(3)", "(4)", "(5)", "(6)"]
SANS_PREUVE = ["(5)", "(6)"]                    # fixture sans jeton ni go : (5) et (6) refusent (D.4 b (6))
SCEAU, DELAI, OPENSSL = "docs/adr-0028/sceau", timedelta(hours=24), shutil.which("openssl")
CNF = (b"[req]\ndistinguished_name = dn\n[dn]\n[tsa]\ndefault_tsa = t\n[t]\nserial = serial\nsigner_digest = sha256\n"
       b"default_policy = 1.2.3.4\ndigests = sha256\ness_cert_id_alg = sha256\n")     # configuration minimale de test
GO_OK, LOIN = "date: 2026-08-31T12:00:00Z\nordre: exécuter sans ancre\nsignataire: investisseur\n".encode(), datetime(
    2100, 1, 1, tzinfo=timezone.utc)                # go daté entre le scellement et son épinglage (C-3)
SCELLEMENT = "2026-08-31T00:00:00+00:00"        # date de commit du scellement des fixtures (C-3)


def h(octets: bytes) -> str:
    return hashlib.sha256(octets).hexdigest()


def attendus(*noms: str) -> list:
    return sorted(set(noms) | set(SANS_PREUVE), key=ORDRE.index)


def dater(depot: str, date, *args: str) -> None:
    """git commit sur le dépôt jetable, identité de fixture ; date : date de commit (GIT_COMMITTER_DATE), ou None."""
    subprocess.run(["git", "-C", depot, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "-c",
                    "commit.gpgsign=false", "commit", "-q", *args], check=True, capture_output=True,
                   env={**GIT_ENV, **({"GIT_COMMITTER_DATE": date} if date else {})})


def poser(racine: str, fichiers: dict, commit: bool = True, date=None):
    """Écrit les fichiers (octets) sous racine ; avec commit, les commite (dépôt jetable ; date : date de commit) et
    rend le sha de HEAD."""
    for rel, octets in fichiers.items():
        Path(racine, rel).parent.mkdir(parents=True, exist_ok=True)
        Path(racine, rel).write_bytes(octets)
    if commit:
        g(racine, "add", "-A"), dater(racine, date, "-m", "fixture")
        return g(racine, "rev-parse", "HEAD")


def lignes_bloc(c1: str, sommes: bytes) -> list:
    return [f"commit_analyse {c1}", f"sha256_script {h(Path(OUTIL).read_bytes())}",
            *(f"journal {n} {h(v)}" for n, v in JOURNAUX.items()), f"sommes {h(sommes)}",
            "cacert_sha256 " + "1" * 64, "tsa_crt_sha256 " + "2" * 64]


def texte_bloc(lignes: list) -> str:
    return "# Paquet de fixture\n\n```shogen-paquet-v1\n" + "\n".join(lignes) + "\n```\n"


def monter(d: str, bloc=lambda x: x, journal="- scellement du paquet : sha256 {}\n", texte=texte_bloc,
           sommes=lambda s: s, code=None) -> dict:
    """Fixture nominale dans d : dépôt jetable dont le commit c1 porte le code d'analyse (avec les octets de
    tools/rendu_unique.py et tools/oracle_record.py du harnais, C-2), puis paquet et JOURNAL.md ; journaux et fichier
    de sommes (format de sha256sum) hors dépôt. Variantes : bloc(lignes), journal (gabarit, {} = sha du paquet),
    texte(lignes) du paquet, sommes(texte) du fichier de sommes, code (fichiers de c1 remplacés)."""
    depot, jx = os.path.join(d, "depot"), os.path.join(d, "campagne")
    os.makedirs(depot), g(depot, "init", "-q"), g(depot, "config", "core.autocrlf", "false")
    outils = {f"s2-harness/tools/{n}": Path(HARNESS, "tools", n).read_bytes()
              for n in ("rendu_unique.py", "oracle_record.py")}
    c1 = poser(depot, {".gitignore": b"__pycache__/\n", "s2-harness/shogen_s2/m.py": b"x = 1\n",
                       "s2-harness/tools/t.py": b"y = 2\n", **outils, **(code or {})})
    sommes = sommes("".join(f"{h(v)}  {n}\n" for n, v in SOMMES.items())).encode()
    poser(jx, {**SOMMES, "SHA256SUMS.txt": sommes}, commit=False)
    paquet = texte(bloc(lignes_bloc(c1, sommes))).encode()
    poser(depot, {PAQUET: paquet, "JOURNAL.md": journal.format(h(paquet)).encode()}, date=SCELLEMENT)
    return {"depot": depot, "paquet": os.path.join(depot, PAQUET), "journaux": jx, "sha": h(paquet),
            "sommes": os.path.join(jx, "SHA256SUMS.txt"), "c1": c1}


def o(d: str, *args: str) -> None:
    """openssl dans d sous la configuration minimale CNF (rien de la configuration système) ; absent : échec du test."""
    subprocess.run([OPENSSL or "openssl", *args], cwd=d, check=True, capture_output=True,
                   env={**os.environ, "OPENSSL_CONF": os.path.join(d, "ac.cnf")})


def autorite(d: str) -> tuple:
    """Autorité RFC 3161 de test produite par openssl dans d (jamais FreeTSA, aucun réseau) : CA de test et certificat
    de TSA qu'elle signe, extension timeStamping critique ; rend les octets de cacert.pem et de tsa.crt."""
    os.makedirs(d)
    Path(d, "ac.cnf").write_bytes(CNF)
    k = ("-newkey", "ec", "-pkeyopt", "ec_paramgen_curve:prime256v1", "-nodes", "-days", "3")
    o(d, "req", "-x509", *k, "-keyout", "ca.key", "-subj", "/CN=CA de test", "-addext",
      "basicConstraints=critical,CA:TRUE", "-addext", "keyUsage=critical,keyCertSign", "-out", "cacert.pem")
    o(d, "req", "-x509", *k, "-keyout", "tsa.key", "-subj", "/CN=TSA de test", "-CA", "cacert.pem", "-CAkey",
      "ca.key", "-addext", "extendedKeyUsage=critical,timeStamping", "-out", "tsa.crt")
    return Path(d, "cacert.pem").read_bytes(), Path(d, "tsa.crt").read_bytes()


def jeton(d: str, donnees: bytes) -> dict:
    """Requête sur donnees (sha256, nonce, certificat demandé : scripts/sceau/make-tsq.sh) et réponse de la TSA de test
    de d ; rend paquet.tsq et paquet.tsr du dossier de sceau."""
    Path(d, "m").write_bytes(donnees)
    o(d, "ts", "-query", "-data", "m", "-sha256", "-cert", "-out", "q.tsq")
    o(d, "ts", "-reply", "-queryfile", "q.tsq", "-signer", "tsa.crt", "-inkey", "tsa.key", "-out", "r.tsr")
    return {f"{SCEAU}/paquet.tsq": Path(d, "q.tsq").read_bytes(), f"{SCEAU}/paquet.tsr": Path(d, "r.tsr").read_bytes()}


def epingler(f: dict, go: bytes = GO_OK, date="2026-09-01T00:00:00+00:00", ligne="- go : sha256 {}\n",
             ou=lambda j, x: j + x):
    """Voie (b) sur la fixture f : fichier de go posé (non commité), ligne qui porte son sha256 placée dans JOURNAL.md
    par ou(journal, ligne), commit daté (GIT_COMMITTER_DATE ; date None : pas de commit) ; rend la date du commit."""
    poser(f["depot"], {f"{SCEAU}/GO-sans-ancre.txt": go}, commit=False)
    j = Path(f["depot"], "JOURNAL.md")
    j.write_bytes(ou(j.read_bytes().decode(), ligne.format(h(go))).encode())
    if date:
        dater(f["depot"], date, "-am", "go")
        return datetime.fromisoformat(date)


def argv(f: dict) -> list:
    """Gardes seules (rien de produit, C3) ; auteur de la liste blanche du lint."""
    return ["--depot", f["depot"], "--paquet", f["paquet"], "--journaux", f["journaux"], "--sommes", f["sommes"],
            "--sortie", os.path.join(os.path.dirname(f["depot"]), "sortie"), "--auteur", "claude-opus-5-5",
            "--gardes-seules"]


class TestRenduUnique(unittest.TestCase):
    def lancer(self, f: dict, *plus: str, **kw) -> tuple:
        """main() en processus : (code, gardes refusées lues sur stderr) ; rien d'écrit (répertoire de sortie absent,
        dossier parent inchangé) ; refus ⇔ code ≠ 0 ⇔ stdout vide, sinon « gardes levées »."""
        parent, err = os.path.dirname(f["depot"]), io.StringIO()
        avant = sorted(os.listdir(parent))
        with contextlib.redirect_stdout(io.StringIO()) as out, contextlib.redirect_stderr(err):
            code = ru.main(argv(f) + list(plus), **kw)
        noms = re.findall(r"^rendu_unique : refus (\S+) : ", err.getvalue(), re.M)
        self.assertEqual((sorted(os.listdir(parent)), code != 0, out.getvalue()),
                         (avant, bool(noms), "" if noms else "gardes levées\n"))
        return code, noms

    def voie_a(self, d: str, ca=lambda s: s, tsa=lambda s: s) -> tuple:
        """Fixture de la voie (a) dans d : autorité de test, bloc aux sha256 de sa chaîne (ca, tsa : variantes), dossier
        de sceau (PAQUET.sha256 qui liste le paquet, jeton sur ses octets, chain/) ; rend (fixture, dossier de
        l'autorité, horloge lue avant la requête à la seconde, préfixes de la chaîne de test)."""
        a, c = autorite(os.path.join(d, "ac"))
        f = monter(d, bloc=lambda x: x[:-2] + [f"cacert_sha256 {ca(h(a))}", f"tsa_crt_sha256 {tsa(h(c))}"])
        t, m = datetime.now(timezone.utc).replace(microsecond=0), f"{f['sha']} *{PAQUET}\n".encode()
        poser(f["depot"], {f"{SCEAU}/PAQUET.sha256": m, **jeton(os.path.join(d, "ac"), m),
                           f"{SCEAU}/chain/cacert.pem": a, f"{SCEAU}/chain/tsa.crt": c}, commit=False)
        return f, os.path.join(d, "ac"), t, {"cacert_sha256": h(a)[:8], "tsa_crt_sha256": h(c)[:8]}

    def test_nominal_et_cli(self):
        """Fixture sans jeton ni go : seules refusent (5) et (6), en processus et par la ligne de commande (code 2,
        stdout vide, rien d'écrit). Rougit si une autre garde refuse à tort, si (5) ou (6) cesse de refuser, si le refus
        ne s'imprime pas ou si son code se perd."""
        f = monter(tempfile.mkdtemp())
        self.assertEqual(self.lancer(f), (2, attendus()))
        p = subprocess.run([sys.executable, "-B", OUTIL, *argv(f)], capture_output=True, text=True)
        self.assertEqual((p.returncode, p.stdout, re.findall(r"^rendu_unique : refus (\S+) : ", p.stderr, re.M)),
                         (2, "", attendus()))

    def test_bloc_absent_duplique_malforme(self):
        """Bloc machine (G0 §C) : paquet sans bloc : refus (bloc ; (2) à (4) non évaluées), rien d'écrit ; lecteur
        seul : forme nominale lue à l'identique ; chaque variante absente, dupliquée ou malformée lève ValueError.
        Rougit si : bloc non lu ou refus avalé ; clé dupliquée admise (même valeur), clé ou journal absent, quatrième
        journal, majuscules, sha tronqué, champ en trop, clé inconnue, nom hors forme ; second bloc ou ouverture
        voisine ignorés ; fermeture non exigée."""
        f = monter(tempfile.mkdtemp(), texte=lambda x: "# Paquet sans bloc\n")
        self.assertEqual(self.lancer(f), (2, attendus("bloc", "(2)", "(3)", "(4)")))
        x = lignes_bloc("a" * 40, b"s")
        self.assertEqual(ru.lire_bloc(texte_bloc(x)), {
            "commit_analyse": "a" * 40, "sha256_script": h(Path(OUTIL).read_bytes()), "sommes": h(b"s"),
            "cacert_sha256": "1" * 64, "tsa_crt_sha256": "2" * 64, "journal": {n: h(v) for n, v in JOURNAUX.items()}})
        for nom, lignes in (("clé absente", x[:5] + x[6:]), ("journal absent", x[:4] + x[5:]),
                            ("quatre journaux", x + ["journal autre.jsonl " + "3" * 64]), ("clé dupliquée", x + [x[1]]),
                            ("journal dupliqué", x[:5] + [x[2]] + x[5:]),
                            ("majuscules", [x[0], x[1][:14] + x[1][14:].upper(), *x[2:]]),
                            ("sha tronqué", [x[0], x[1][:-1], *x[2:]]), ("commit court", [x[0][:-1], *x[1:]]),
                            ("champ en trop", [x[0], x[1] + " x", *x[2:]]), ("clé inconnue", x + ["autre " + "4" * 64]),
                            ("tabulation", [x[0].replace(" ", "\t"), *x[1:]]), ("ligne vide", x + [""]),
                            ("retour chariot", [x[0] + "\r", *x[1:]]),
                            ("nom hors forme", [*x[:2], "journal ../c " + "5" * 64, *x[3:]])):
            with self.subTest(variante=nom), self.assertRaises(ValueError):
                ru.lire_bloc(texte_bloc(lignes))
        t = texte_bloc(x)
        for nom, texte in (("aucun bloc", "# Paquet\n"), ("deux blocs", t + t), ("non fermé", t[:-4]),
                           ("ouverture voisine", t + "\n~~~ shogen-paquet-v1\n~~~\n"),
                           ("ouverture tilde", t.replace("```shogen", "~~~shogen").replace("\n```\n", "\n~~~\n"))):
            with self.subTest(variante=nom), self.assertRaisesRegex(ValueError, "ouverture"):
                ru.lire_bloc(texte)

    def test_garde_1_sha_du_paquet_a_head(self):
        """(1) : sha256 complet du paquet absent de JOURNAL.md à HEAD : présent seulement sur le disque (non commité),
        en préfixe de huit chiffres, ou pris dans une suite hexadécimale plus longue : refus (1), rien d'écrit. Rougit
        si : JOURNAL.md lu sur le disque ; préfixe ou sous-chaîne admis ; garde neutralisée."""
        for journal in ("- paquet {:.8}…\n", "- {}0\n", "- f{}\n", "- rien\n"):
            with self.subTest(journal=journal):
                self.assertEqual(self.lancer(monter(tempfile.mkdtemp(), journal=journal)), (2, attendus("(1)")))
        f = monter(tempfile.mkdtemp(), journal="- rien\n")
        poser(f["depot"], {"JOURNAL.md": f"- scellement du paquet : sha256 {f['sha']}\n".encode()}, commit=False)
        self.assertEqual(self.lancer(f), (2, attendus("(1)")))

    def test_garde_4_sha_du_script(self):
        """(4) : sha256_script du bloc différent du sha256 des octets de l'outil (dernier chiffre changé) ; outil ou
        enregistreur du commit gardé autres que ceux qui tournent ((2) levée : mêmes octets à c1 ; C-2) : refus (4),
        rien d'écrit. Rougit si la garde est neutralisée, hache un autre fichier, ou ne lit pas le commit gardé."""
        f = monter(tempfile.mkdtemp(), bloc=lambda x: [x[0], x[1][:-1] + "01"[x[1][-1] == "0"], *x[2:]])
        self.assertEqual(self.lancer(f), (2, attendus("(4)")))
        for nom in ("rendu_unique.py", "oracle_record.py"):
            with self.subTest(commit_garde=nom):
                f = monter(tempfile.mkdtemp(), code={f"s2-harness/tools/{nom}": b"# autre\n"})
                self.assertEqual(self.lancer(f), (2, attendus("(4)")))

    def test_gardes_lisent_le_head_resolu_une_fois(self):
        """C-2 (i) et RENDU-STATUS-HEAD-1 : HEAD déplacé sur Y (commit sans parent : sha du paquet et go absents de
        JOURNAL.md, code d'analyse et outil changés), arbre de travail propre sur Y ; la résolution unique de HEAD rend
        X (enveloppe de git) : contexte head = X ; seule (2) refuse, l'arbre de travail étant jugé contre X (git status
        le juge contre HEAD et n'y voit rien). Rougit si (1), (4) ou la voie (b) relisent HEAD au lieu du commit
        résolu, ou si l'arbre de travail n'est pas jugé contre X."""
        f = monter(tempfile.mkdtemp())
        epingler(f)
        x, vrai = g(f["depot"], "rev-parse", "HEAD"), ru.git
        g(f["depot"], "checkout", "-q", "--orphan", "y")
        poser(f["depot"], {"JOURNAL.md": b"- rien\n", "s2-harness/shogen_s2/m.py": b"x = 2\n",
                           "s2-harness/tools/rendu_unique.py": b"# y\n"})
        resolu = lambda r, *a: subprocess.CompletedProcess(a, 0, f"{x}\n".encode(), b"") if a == (
            "rev-parse", "--verify", "HEAD^{commit}") else vrai(r, *a)
        with mock.patch.object(ru, "git", resolu):
            refus, c = ru.evaluer_gardes(f["depot"], f["paquet"], f["journaux"], f["sommes"], LOIN)
        self.assertEqual(([n for n, _ in refus], c.get("head")), (["(2)"], x))
        self.assertTrue(refus[0][1].startswith(f"arbre de travail ≠ commit gardé {x} "), refus)

    def test_garde_2_code_d_analyse(self):
        """(2) : code d'analyse différent du commit du bloc (commit qui change tools), commit du bloc absent du dépôt,
        arbre de travail modifié sur les chemins (fichier suivi modifié, indexé ou non ; non suivi ; ignoré) : refus
        (2), rien d'écrit ; de même avec --depot sur un sous-dossier ; commit hors des chemins : levée. Rougit si : git
        diff ou git status retirés, erreur de git diff admise, non suivis ou ignorés admis, racine non résolue."""
        sale = {"s2-harness/shogen_s2/m.py": b"x = 2\n"}
        for nom, faire in (("commit", lambda d: poser(d, {"s2-harness/tools/t.py": b"y = 3\n"})),
                           ("modifié", lambda d: poser(d, sale, commit=False)),
                           ("indexé", lambda d: (poser(d, sale, commit=False), g(d, "add", "-A"))),
                           ("non suivi", lambda d: poser(d, {"s2-harness/shogen_s2/n.py": b""}, commit=False)),
                           ("ignoré", lambda d: poser(d, {"s2-harness/tools/__pycache__/t.pyc": b"\0"}, False))):
            f = monter(tempfile.mkdtemp())
            faire(f["depot"])
            with self.subTest(variante=nom):
                self.assertEqual(self.lancer(f), (2, attendus("(2)")))
                self.assertEqual(self.lancer({**f, "depot": os.path.join(f["depot"], "s2-harness")}),
                                 (2, attendus("(2)")))
        f = monter(tempfile.mkdtemp(), bloc=lambda x: ["commit_analyse " + "0" * 40, *x[1:]])
        self.assertEqual(self.lancer(f), (2, attendus("(2)")))
        f = monter(tempfile.mkdtemp())
        poser(f["depot"], {"LISEZ-MOI": b"hors des chemins\n"})
        self.assertEqual(self.lancer(f), (2, attendus()))

    def test_garde_3_journaux_bloc_et_sommes(self):
        """(3) et EX-E1-1 : journal modifié ; sommes qui diffèrent du fichier et du bloc (sha des sommes au bloc mis à
        jour) ; bloc qui diffère du fichier et des sommes ; sommes modifiées hors de leurs entrées ; journal absent des
        sommes ou du dossier ; nom répété ou ligne non conforme aux sommes : refus (3), rien d'écrit ; sommes en CRLF,
        marque binaire et majuscules : levée. Rougit si : comparaison au bloc ou aux sommes retirée, sha du fichier de
        sommes non contrôlé, nom répété ou ligne non conforme admis, CRLF, « * » ou majuscules refusés."""
        j, r = h(JOURNAUX["journal.jsonl"]), h(JOURNAUX["raw.jsonl"])
        for nom, kw in (("sommes ≠ fichier", {"sommes": lambda s: s.replace(j, "f" * 64)}),
                        ("bloc ≠ fichier", {"bloc": lambda x: [*x[:3], "journal journal.jsonl " + "e" * 64, *x[4:]]}),
                        ("absent des sommes", {"sommes": lambda s: s.replace(f"{r}  raw.jsonl\n", "")}),
                        ("nom répété", {"sommes": lambda s: "f" * 64 + "  control.jsonl\n" + s}),
                        ("ligne non conforme", {"sommes": lambda s: "n'importe quoi\n" + s})):
            with self.subTest(variante=nom):
                self.assertEqual(self.lancer(monter(tempfile.mkdtemp(), **kw)), (2, attendus("(3)")))
        for nom, faire in (("journal modifié", lambda jx: poser(jx, {"raw.jsonl": b"{}\n"}, commit=False)),
                           ("sommes hors entrées", lambda jx: poser(jx, {"SHA256SUMS.txt": Path(
                               jx, "SHA256SUMS.txt").read_bytes() + b"\n"}, commit=False)),
                           ("absent du dossier", lambda jx: os.remove(os.path.join(jx, "control.jsonl")))):
            f = monter(tempfile.mkdtemp())
            faire(f["journaux"])
            with self.subTest(variante=nom):
                self.assertEqual(self.lancer(f), (2, attendus("(3)")))
        crlf = lambda s: re.sub(r"^([0-9a-f]{64})  ", lambda m: m.group(1).upper() + " *", s, flags=re.M)
        self.assertEqual(self.lancer(monter(tempfile.mkdtemp(), sommes=lambda s: crlf(s).replace("\n", "\r\n"))),
                         (2, attendus()))


    def test_voie_a_jeton_verifie_et_garde_5(self):
        """(5) et (6), voie (a), préfixes de D.4 c remplacés par ceux de la chaîne de test : horloge à genTime + 24 h
        (borne haute) : gardes levées, code 0, « gardes levées », rien d'écrit ; une seconde avant genTime + 24 h (borne
        basse) : refus (5) seul ; préfixes réels de D.4 c : refus (5) et (6). Rougit si : délai retiré ou raccourci,
        genTime mal lu, préfixes non contrôlés, jeton refusé à tort."""
        self.assertTrue(OPENSSL, "openssl absent : le test échoue, il ne saute pas (G0 §C, risque (a))")
        f, _, t, pref = self.voie_a(tempfile.mkdtemp())
        haut = datetime.now(timezone.utc).replace(microsecond=0) + timedelta(seconds=1)
        with mock.patch.dict(ru.PREFIXES, pref):
            self.assertEqual(self.lancer(f, maintenant=haut + DELAI), (0, []))
            self.assertEqual(self.lancer(f, maintenant=t + DELAI - timedelta(seconds=1)), (2, ["(5)"]))
        self.assertEqual(self.lancer(f, maintenant=haut + DELAI), (2, ["(5)", "(6)"]))

    def test_voie_a_refus(self):
        """(6), voie (a), horloge à genTime + 48 h : bloc d'une autre chaîne que cacert.pem ou tsa.crt (même préfixe) ;
        requête qui n'est pas celle du jeton (autre nonce) ; jeton sur d'autres octets que PAQUET.sha256 ; manifeste qui
        ne liste pas le sha du paquet (jeton sur ce manifeste), ou le liste au format BSD (C-11, R04) ; jeton d'une
        autre autorité : refus (5) et (6), rien d'écrit. Rougit si l'un des contrôles de la voie (a) est retiré ou si
        le code d'openssl est ignoré."""
        self.assertTrue(OPENSSL, "openssl absent : le test échoue, il ne saute pas (G0 §C, risque (a))")
        m = lambda f: Path(f["depot"], SCEAU, "PAQUET.sha256").read_bytes()
        autre = lambda f, ac: (autorite(ac + "2"), poser(f["depot"], jeton(ac + "2", m(f)), commit=False))
        sans, bsd = ("0" * 64 + " *x\n").encode(), lambda f: f"SHA256 ({PAQUET}) = {f['sha']}\n".encode()
        for nom, kw, faire in (
                ("bloc ≠ cacert.pem", {"ca": lambda s: s[:8] + "0" * 56}, None),
                ("bloc ≠ tsa.crt", {"tsa": lambda s: s[:8] + "0" * 56}, None),
                ("autre requête", {}, lambda f, ac: poser(f["depot"], {f"{SCEAU}/paquet.tsq": jeton(ac, m(f))[
                    f"{SCEAU}/paquet.tsq"]}, commit=False)),
                ("jeton sur d'autres octets", {}, lambda f, ac: poser(f["depot"], jeton(ac, b"autre\n"), commit=False)),
                ("manifeste sans le paquet", {}, lambda f, ac: poser(f["depot"], {f"{SCEAU}/PAQUET.sha256": sans,
                                                                                  **jeton(ac, sans)}, commit=False)),
                ("manifeste BSD", {}, lambda f, ac: poser(f["depot"], {f"{SCEAU}/PAQUET.sha256": bsd(f),
                                                                       **jeton(ac, bsd(f))}, commit=False)),
                ("autre autorité", {}, autre)):
            f, ac, t, pref = self.voie_a(tempfile.mkdtemp(), **kw)
            faire and faire(f, ac)
            with self.subTest(variante=nom), mock.patch.dict(ru.PREFIXES, pref):
                self.assertEqual(self.lancer(f, maintenant=t + 2 * DELAI), (2, ["(5)", "(6)"]))

    def test_ni_jeton_ni_go_horloge_seule(self):
        """D.4 b (6) : ni jeton vérifié ni go épinglé (pas de dossier de sceau, puis dossier vide) : refus (5) et (6),
        même horloge en 2100, rien d'écrit ; ligne de commande : même refus, et l'horloge n'y est pas une option.
        Rougit si (5) ou (6) est neutralisée, si T0 indéterminé est admis, ou si l'horloge devient une option."""
        f, loin = monter(tempfile.mkdtemp()), datetime(2100, 1, 1, tzinfo=timezone.utc)
        self.assertEqual(self.lancer(f, maintenant=loin), (2, ["(5)", "(6)"]))
        os.makedirs(os.path.join(f["depot"], SCEAU, "chain"))
        self.assertEqual(self.lancer(f, maintenant=loin), (2, ["(5)", "(6)"]))
        p = subprocess.run([sys.executable, "-B", OUTIL, *argv(f), "--maintenant", "2100-01-01T00:00:00Z"],
                           capture_output=True, text=True)
        self.assertEqual((p.returncode, p.stdout, "unrecognized arguments: --maintenant" in p.stderr), (2, "", True))

    def test_voie_b_go_epingle_et_garde_5(self):
        """(5) et (6), voie (b), textconv hostile posé sur JOURNAL.md : horloge à T0 + 24 h exactement (T0 = date du
        commit qui épingle le go) : levées, code 0 ; une seconde avant : refus (5) seul ; le go cité de nouveau dix
        jours plus tard : T0 reste le premier commit ; ligne de commande (heure système) : go épinglé trois jours plus
        tôt, code 0 et « gardes levées » ; go épinglé maintenant : refus (5). Rougit si : borne exclue, dernier commit
        pris pour T0, textconv appliqué, voie (b) absente, horloge système non lue."""
        f = monter(tempfile.mkdtemp())
        Path(f["depot"], ".git", "info", "attributes").write_bytes(b"JOURNAL.md diff=maj\n")
        g(f["depot"], "config", "diff.maj.textconv", "tr a-f A-F <")
        t0 = epingler(f)
        epingler(f, ligne="- rappel du go : {}\n", date="2026-09-11T00:00:00+00:00")
        self.assertEqual(self.lancer(f, maintenant=t0 + DELAI), (0, []))
        self.assertEqual(self.lancer(f, maintenant=t0 + DELAI - timedelta(seconds=1)), (2, ["(5)"]))
        for recul, code, sortie, noms in ((3 * DELAI, 0, "gardes levées\n", []), (timedelta(0), 2, "", ["(5)"])):
            f = monter(tempfile.mkdtemp())
            epingler(f, date=(datetime.now(timezone.utc) - recul).isoformat())
            p = subprocess.run([sys.executable, "-B", OUTIL, *argv(f)], capture_output=True, text=True)
            self.assertEqual((p.returncode, p.stdout, re.findall(r"^rendu_unique : refus (\S+) : ", p.stderr, re.M)),
                             (code, sortie, noms))

    def test_voie_b_refus(self):
        """(6), voie (b), horloge en 2100 : go avec BOM, en CRLF, sans LF final, avec une ligne de plus, sans accent,
        date hors ISO 8601, hors calendrier, sans fuseau ou à +01:00 (même instant UTC), encodé en Latin-1 ; sha du go
        absent de JOURNAL.md, en préfixe seulement, sur le disque seulement, avant la ligne du scellement (seul, ou cité
        avant puis après), ou sur cette ligne ; C-3 (SHOGEN-GO-ORDRE-1) : go daté après son commit d'épinglage ou
        avant le commit du scellement ; commit d'épinglage daté avant le scellement, au même instant, ou hors de sa
        descendance ; scellement et go dans le même commit : refus (5) et (6), rien d'écrit. Rougit si l'un des
        contrôles de la voie (b) est retiré ou relâché."""
        u, date = GO_OK.decode(), lambda x: GO_OK.decode().replace("2026-08-31T12:00:00Z", x).encode()
        for nom, kw in (("BOM", {"go": b"\xef\xbb\xbf" + GO_OK}), ("CRLF", {"go": GO_OK.replace(b"\n", b"\r\n")}),
                        ("sans LF final", {"go": GO_OK[:-1]}), ("ligne de plus", {"go": GO_OK + b"x\n"}),
                        ("sans accent", {"go": u.replace("é", "e").encode()}), ("Latin-1", {"go": u.encode("latin-1")}),
                        ("date hors ISO", {"go": date("31/08/2026")}),
                        ("hors calendrier", {"go": date("2026-13-31T12:00:00Z")}),
                        ("sans fuseau", {"go": u.replace(":00Z", ":00").encode()}),
                        ("+01:00", {"go": date("2026-08-31T13:00:00+01:00")}),
                        ("sha absent", {"ligne": "- go de l'investisseur\n"}), ("préfixe", {"ligne": "- go {:.8}…\n"}),
                        ("disque seulement", {"date": None}), ("avant le scellement", {"ou": lambda j, x: x + j}),
                        ("cité avant puis après", {"ou": lambda j, x: x + j + x}),
                        ("même ligne", {"ou": lambda j, x: j.rstrip("\n") + " " + x}),
                        ("go après son épinglage", {"go": date("2026-09-01T00:00:01Z")}),
                        ("go avant le scellement", {"go": date("2026-08-30T23:59:59Z")}),
                        ("épinglage avant le scellement", {"date": "2026-08-30T00:00:00+00:00"}),
                        ("épinglage au même instant", {"go": date("2026-08-31T00:00:00Z"), "date": SCELLEMENT})):
            f = monter(tempfile.mkdtemp())
            epingler(f, **kw)
            with self.subTest(variante=nom):
                self.assertEqual(self.lancer(f, maintenant=LOIN), (2, ["(5)", "(6)"]))
        go = date("2026-08-31T00:00:00Z")
        f = monter(tempfile.mkdtemp(), journal="- scellement du paquet : sha256 {}\n" + f"- go : sha256 {h(go)}\n")
        poser(f["depot"], {f"{SCEAU}/GO-sans-ancre.txt": go}, commit=False)
        with self.subTest(variante="même commit"):
            self.assertEqual(self.lancer(f, maintenant=LOIN), (2, ["(5)", "(6)"]))
        f = monter(tempfile.mkdtemp())                  # go épinglé sur une branche partie de c1, puis fusionnée
        g(f["depot"], "checkout", "-q", "-b", "parallele", f["c1"])
        poser(f["depot"], {"JOURNAL.md": f"- go : sha256 {h(GO_OK)}\n".encode()}, date="2026-08-31T18:00:00+00:00")
        g(f["depot"], "checkout", "-q", "-"), g(f["depot"], "merge", "-q", "--no-commit", "-s", "ours", "parallele")
        epingler(f, date="2026-08-31T20:00:00+00:00")
        with self.subTest(variante="hors de la descendance du scellement"):
            self.assertEqual(self.lancer(f, maintenant=LOIN), (2, ["(5)", "(6)"]))

    def test_voie_b_premiere_ligne_entiere_pas_une_sous_chaine(self):
        """GO-PICKAXE-1 : S et Gc = premiers commits dont JOURNAL.md porte une ligne qui contient le sha entier (comme
        (1)). Go cité d'abord en « f<sha> » (08-31 13:00, après la date du go), puis sur sa ligne (09-01) : T0 =
        09-01T00:00Z, refus (5) à 09-01 14:00 ; paquet cité d'abord en « f<sha> » (00:00), puis sur sa ligne (06:00) :
        go daté de 03:00 refusé, de 12:00 levé ; « f<sha> » réécrit en ligne entière (même nombre d'occurrences, 09-01)
        : T0 = 09-01T00:00Z. Rougit si : sous-chaîne prise pour S ou Gc (git log -S) ; candidat non confirmé sur sa
        ligne ; remplacement à compte égal manqué."""
        j = lambda f: Path(f["depot"], "JOURNAL.md").read_bytes()
        f = monter(tempfile.mkdtemp())
        poser(f["depot"], {"JOURNAL.md": j(f) + f"- brouillon f{h(GO_OK)}\n".encode()}, date="2026-08-31T13:00:00Z")
        epingler(f)
        r = ru.evaluer_gardes(f["depot"], f["paquet"], f["journaux"], f["sommes"], LOIN)
        with self.subTest(cas="go en sous-chaîne d'abord"):
            self.assertEqual((r[0], ru.ouverture(r[1])["T0"]), ([], "2026-09-01T00:00:00Z"))
            self.assertEqual(self.lancer(f, maintenant=datetime(2026, 9, 1, 14, tzinfo=timezone.utc)), (2, ["(5)"]))
        for heure, attendu in (("03", (2, ["(5)", "(6)"])), ("12", (0, []))):
            f = monter(tempfile.mkdtemp(), journal="- brouillon f{}\n")
            poser(f["depot"], {"JOURNAL.md": j(f) + f"- scellement : sha256 {f['sha']}\n".encode()},
                  date="2026-08-31T06:00:00Z")
            epingler(f, go=GO_OK.replace(b"T12:", f"T{heure}:".encode()))
            with self.subTest(go=heure):
                self.assertEqual(self.lancer(f, maintenant=LOIN), attendu)
        f = monter(tempfile.mkdtemp())
        x = j(f)
        poser(f["depot"], {"JOURNAL.md": x + f"- go : sha256 f{h(GO_OK)}\n".encode()}, date="2026-08-31T13:00:00Z")
        poser(f["depot"], {"JOURNAL.md": x + f"- go : sha256 {h(GO_OK)}\n".encode()}, date="2026-09-01T00:00:00Z")
        poser(f["depot"], {f"{SCEAU}/GO-sans-ancre.txt": GO_OK}, commit=False)
        r = ru.evaluer_gardes(f["depot"], f["paquet"], f["journaux"], f["sommes"], LOIN)
        with self.subTest(cas="remplacement à compte égal"):
            self.assertEqual((r[0], ru.ouverture(r[1]).get("T0") if not r[0] else None), ([], "2026-09-01T00:00:00Z"))

    def test_deux_voies_t0_le_plus_tardif(self):
        """(5), les deux voies établies : go épinglé trois jours avant le jeton ; horloge à T0 du go + 25 h, avant
        genTime + 24 h : refus (5) ; à genTime + 24 h (borne haute) : levées. Rougit si T0 est le plus ancien."""
        self.assertTrue(OPENSSL, "openssl absent : le test échoue, il ne saute pas (G0 §C, risque (a))")
        f, _, t, pref = self.voie_a(tempfile.mkdtemp())
        haut = datetime.now(timezone.utc).replace(microsecond=0) + timedelta(seconds=1)
        t0 = epingler(f, date=(t - 3 * DELAI).isoformat())
        with mock.patch.dict(ru.PREFIXES, pref):
            self.assertEqual(self.lancer(f, maintenant=t0 + DELAI + timedelta(hours=1)), (2, ["(5)"]))
            self.assertEqual(self.lancer(f, maintenant=haut + DELAI), (0, []))

    def test_gentime_formes(self):
        """genTime de openssl ts -reply -text : forme d'OpenSSL et ISO 8601, fin de ligne CRLF, fraction de seconde
        portée à la seconde suivante (T0 jamais avancé) ; ligne absente ou répétée, autre décalage : ValueError. Rougit
        si : CRLF, forme ISO ou fraction mal lus."""
        u = lambda *a: datetime(*a, tzinfo=timezone.utc)
        for texte, attendu in (("Time stamp: Oct  2 07:32:34 2026 GMT\n", u(2026, 10, 2, 7, 32, 34)),
                               ("x\r\nTime stamp: Dec 31 23:59:59.5 2026 GMT\r\n", u(2027, 1, 1)),
                               ("Time stamp: 2026-10-02 07:32:34.000Z\n", u(2026, 10, 2, 7, 32, 34))):
            self.assertEqual(ru.gentime(texte), attendu)
        for texte in ("", "Time stamp: Oct  2 07:32:34 2026 GMT\n" * 2, "Time stamp: 2026-10-02T07:32:34+01:00\n"):
            with self.subTest(texte=texte), self.assertRaises(ValueError):
                ru.gentime(texte)


    def test_ouverture_voie_t0_gentime(self):
        """SHOGEN-RENDU-T0-1 : evaluer_gardes rend les refus et le contexte ; ouverture() en tire la voie, T0 (le plus
        tardif, celui de la garde (5)) et genTime (voie (a) seule), en ISO 8601 UTC. Voie (b) : T0 = date du commit qui
        épingle le go, genTime nul ; voie (a) : T0 = genTime, lu ici dans openssl ts -reply -text ; deux voies (go
        épinglé un jour après genTime) : T0 = le go, genTime du jeton. Rougit si : voie, T0 ou genTime faux."""
        self.assertTrue(OPENSSL, "openssl absent : le test échoue, il ne saute pas (G0 §C, risque (a))")
        f = monter(tempfile.mkdtemp())
        epingler(f)
        r = ru.evaluer_gardes(f["depot"], f["paquet"], f["journaux"], f["sommes"], LOIN)
        self.assertEqual((r[0], ru.ouverture(r[1])), ([], {"voie": "b", "T0": "2026-09-01T00:00:00Z", "genTime": None}))
        f, _, _, pref = self.voie_a(tempfile.mkdtemp())
        x = subprocess.run([OPENSSL, "ts", "-reply", "-in", os.path.join(f["depot"], SCEAU, "paquet.tsr"), "-text"],
                           capture_output=True, text=True).stdout.split("Time stamp: ")[1].split("\n")[0]
        g = datetime.strptime(x, "%b %d %H:%M:%S %Y GMT").replace(tzinfo=timezone.utc)
        iso = lambda d: d.strftime("%Y-%m-%dT%H:%M:%SZ")
        with mock.patch.dict(ru.PREFIXES, pref):
            r = ru.evaluer_gardes(f["depot"], f["paquet"], f["journaux"], f["sommes"], LOIN)
            self.assertEqual((r[0], ru.ouverture(r[1])), ([], {"voie": "a", "T0": iso(g), "genTime": iso(g)}))
            go = epingler(f, date=(g + DELAI).isoformat())
            r = ru.evaluer_gardes(f["depot"], f["paquet"], f["journaux"], f["sommes"], LOIN)
            self.assertEqual((r[0], ru.ouverture(r[1])), ([], {"voie": "a+b", "T0": iso(go), "genTime": iso(g)}))

    def test_refus_auteur_sortie_deviation_noms(self):
        """Avant toute garde : auteur hors de la liste blanche du lint (refus auteur) ; --sortie présent sans
        --deviation, lien symbolique pendant à la place de --sortie (C-11, R05), --deviation sans première exécution,
        à motif vide ou sur deux lignes (refus sortie). Gardes levées (go épinglé, horloge en 2100) : noms des journaux
        du bloc autres que control.jsonl, journal.jsonl, raw.jsonl (refus noms, L3). Code 2, rien d'écrit ; répertoire
        de déviation : premier suffixe libre. Rougit si un refus manque ou si un suffixe existant est repris."""
        f = monter(tempfile.mkdtemp())
        epingler(f)
        sortie = os.path.join(os.path.dirname(f["depot"]), "sortie")
        self.assertEqual(self.lancer(f, maintenant=LOIN), (0, []))
        self.assertEqual(self.lancer(f, "--auteur", "claude-opus-" + "5", maintenant=LOIN), (2, ["auteur"]))
        for plus in (["--deviation", "relance"], ["--deviation", " "]):
            self.assertEqual(self.lancer(f, *plus, maintenant=LOIN), (2, ["sortie"]))
        os.symlink(os.path.join(os.path.dirname(sortie), "absent"), sortie)       # lien pendant (C-11, R05)
        self.assertEqual(self.lancer(f, maintenant=LOIN), (2, ["sortie"]))
        os.remove(sortie)
        os.makedirs(sortie)
        for plus in ([], ["--deviation", ""], ["--deviation", "deux\nlignes"]):
            self.assertEqual(self.lancer(f, *plus, maintenant=LOIN), (2, ["sortie"]))
        self.assertEqual(self.lancer(f, "--deviation", "relance déclarée", maintenant=LOIN), (0, []))
        self.assertEqual(ru.destination(sortie, "motif"), sortie + ".deviation-1")
        os.makedirs(sortie + ".deviation-1")
        self.assertEqual(ru.destination(sortie, "motif"), sortie + ".deviation-2")
        noms = {"control.jsonl": JOURNAUX["control.jsonl"], "journal.jsonl": JOURNAUX["journal.jsonl"],
                "brut.jsonl": JOURNAUX["raw.jsonl"]}
        cinq = {**noms, "campagne.log": b"x\n", "segments.json": b"{}\n"}
        with mock.patch.dict(JOURNAUX, noms, clear=True), mock.patch.dict(SOMMES, cinq, clear=True):
            f = monter(tempfile.mkdtemp())
        epingler(f)
        self.assertEqual(self.lancer(f, maintenant=LOIN), (2, ["noms"]))

    def test_refus_debris_d_une_tentative_interrompue(self):
        """C-4 (G2) : dossier .sortie.abcd (débris d'une tentative interrompue) à côté de --sortie : refus sortie, rien
        d'écrit, sans --deviation (sortie absente) et avec (première exécution présente) ; motif nommant le chemin.
        Rougit si le contrôle est retiré."""
        f = monter(tempfile.mkdtemp())
        epingler(f)
        sortie, debris = (os.path.join(os.path.dirname(f["depot"]), x) for x in ("sortie", ".sortie.abcd"))
        os.makedirs(debris)
        self.assertEqual(self.lancer(f, maintenant=LOIN), (2, ["sortie"]))
        os.makedirs(sortie)
        self.assertEqual(self.lancer(f, "--deviation", "relance déclarée", maintenant=LOIN), (2, ["sortie"]))
        with self.assertRaisesRegex(ValueError, re.escape(debris)):
            ru.destination(sortie, None)


if __name__ == "__main__":
    unittest.main()
