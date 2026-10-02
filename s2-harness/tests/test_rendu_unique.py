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
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.test_oracle_record import HARNESS, g

OUTIL = os.path.join(HARNESS, "tools", "rendu_unique.py")
_SPEC = importlib.util.spec_from_file_location("rendu_unique", OUTIL)
ru = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(ru)
JOURNAUX = {"control.jsonl": b'{"type": "run_params"}\n', "journal.jsonl": b'{"v": 1}\n', "raw.jsonl": b'{"r": 2}\n'}
SOMMES = {**JOURNAUX, "campagne.log": b"x\n", "segments.json": b"{}\n"}     # cinq entrées au fichier de sommes
PAQUET, ORDRE = "docs/adr-0028/PAQUET-PREREG-S2.md", ["bloc", "(1)", "(2)", "(3)", "(4)", "(5)", "(6)"]
NON_CONSTRUITES = ["(5)", "(6)"]                                # sous-lot C1c


def h(octets: bytes) -> str:
    return hashlib.sha256(octets).hexdigest()


def attendus(*noms: str) -> list:
    return sorted(set(noms) | set(NON_CONSTRUITES), key=ORDRE.index)


def poser(racine: str, fichiers: dict, commit: bool = True):
    """Écrit les fichiers (octets) sous racine ; avec commit, les commite (dépôt jetable) et rend le sha de HEAD."""
    for rel, octets in fichiers.items():
        Path(racine, rel).parent.mkdir(parents=True, exist_ok=True)
        Path(racine, rel).write_bytes(octets)
    if commit:
        g(racine, "add", "-A"), g(racine, "commit", "-q", "-m", "fixture")
        return g(racine, "rev-parse", "HEAD")


def lignes_bloc(c1: str, sommes: bytes) -> list:
    return [f"commit_analyse {c1}", f"sha256_script {h(Path(OUTIL).read_bytes())}",
            *(f"journal {n} {h(v)}" for n, v in JOURNAUX.items()), f"sommes {h(sommes)}",
            "cacert_sha256 " + "1" * 64, "tsa_crt_sha256 " + "2" * 64]


def texte_bloc(lignes: list) -> str:
    return "# Paquet de fixture\n\n```shogen-paquet-v1\n" + "\n".join(lignes) + "\n```\n"


def monter(d: str, bloc=lambda x: x, journal="- scellement du paquet : sha256 {}\n", texte=texte_bloc,
           sommes=lambda s: s) -> dict:
    """Fixture nominale dans d : dépôt jetable dont le commit c1 porte le code d'analyse, puis paquet et JOURNAL.md ;
    journaux et fichier de sommes (format de sha256sum) hors dépôt. Variantes : bloc(lignes), journal (gabarit,
    {} = sha du paquet), texte(lignes) du paquet, sommes(texte) du fichier de sommes."""
    depot, jx = os.path.join(d, "depot"), os.path.join(d, "campagne")
    os.makedirs(depot), g(depot, "init", "-q"), g(depot, "config", "core.autocrlf", "false")
    c1 = poser(depot, {".gitignore": b"__pycache__/\n", "s2-harness/shogen_s2/m.py": b"x = 1\n",
                       "s2-harness/tools/t.py": b"y = 2\n"})
    sommes = sommes("".join(f"{h(v)}  {n}\n" for n, v in SOMMES.items())).encode()
    poser(jx, {**SOMMES, "SHA256SUMS.txt": sommes}, commit=False)
    paquet = texte(bloc(lignes_bloc(c1, sommes))).encode()
    poser(depot, {PAQUET: paquet, "JOURNAL.md": journal.format(h(paquet)).encode()})
    return {"depot": depot, "paquet": os.path.join(depot, PAQUET), "journaux": jx, "sha": h(paquet),
            "sommes": os.path.join(jx, "SHA256SUMS.txt"), "c1": c1}


def argv(f: dict) -> list:
    return ["--depot", f["depot"], "--paquet", f["paquet"], "--journaux", f["journaux"], "--sommes", f["sommes"],
            "--sortie", os.path.join(os.path.dirname(f["depot"]), "sortie")]


class TestRenduUnique(unittest.TestCase):
    def lancer(self, f: dict, **kw) -> tuple:
        """main() en processus : (code, gardes refusées lues sur stderr) ; rien d'écrit (répertoire de sortie absent,
        dossier parent inchangé) ; refus ⇔ code ≠ 0 ⇔ stdout vide, sinon « gardes levées »."""
        parent, err = os.path.dirname(f["depot"]), io.StringIO()
        avant = sorted(os.listdir(parent))
        with contextlib.redirect_stdout(io.StringIO()) as out, contextlib.redirect_stderr(err):
            code = ru.main(argv(f), **kw)
        noms = re.findall(r"^rendu_unique : refus (\S+) : ", err.getvalue(), re.M)
        self.assertEqual((sorted(os.listdir(parent)), code != 0, out.getvalue()),
                         (avant, bool(noms), "" if noms else "gardes levées\n"))
        return code, noms

    def test_nominal_et_cli(self):
        """Fixture nominale : seules refusent les gardes non construites, en processus et par la ligne de commande
        (code 2, stdout vide, rien d'écrit). Rougit si une garde construite refuse à tort, si une garde non construite
        cesse de refuser, si le refus ne s'imprime pas ou si son code se perd."""
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
        """(4) : sha256_script du bloc différent du sha256 des octets de l'outil (dernier chiffre changé) : refus (4),
        rien d'écrit. Rougit si la garde est neutralisée ou hache un autre fichier que l'outil."""
        f = monter(tempfile.mkdtemp(), bloc=lambda x: [x[0], x[1][:-1] + "01"[x[1][-1] == "0"], *x[2:]])
        self.assertEqual(self.lancer(f), (2, attendus("(4)")))

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


if __name__ == "__main__":
    unittest.main()
