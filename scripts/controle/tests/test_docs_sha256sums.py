"""Cas de enforcement/docs-sha256sums.py (lot DETTES-T4, DT4-a ; SHOGEN-DOCS-SHA256SUMS-GATE-1). Sommes publiées,
non recalculées : SHA-256 de « abc » (FIPS 180-2, annexe B.1) et du vide. Arbres temporaires, sauf le dernier cas."""
import contextlib
import io
import os
import re
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SCRIPT = os.path.join(RACINE, "enforcement", "docs-sha256sums.py")
ABC, VIDE = ("ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
             "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
NL, NIVEAU = chr(10), "docs/adr-0028/sim-niveau/SHA256SUMS"


def controler(*racines):
    p = subprocess.run([sys.executable, "-B", SCRIPT, *racines], capture_output=True, text=True, timeout=120)
    return p.returncode, p.stdout, p.stderr


class DocsSha256sums(unittest.TestCase):
    def arbre(self, fichiers, d=None):
        if d is None:
            d = tempfile.mkdtemp()
            self.addCleanup(shutil.rmtree, d)
            os.makedirs(os.path.join(d, "docs"))
        for nom, texte in fichiers.items():
            os.makedirs(os.path.dirname(os.path.join(d, nom)), exist_ok=True)
            with open(os.path.join(d, nom), "w", encoding="utf-8", newline="") as f:
                f.write(texte)
        return d

    def refuse(self, fichiers, *attendus):
        code, _, err = controler(self.arbre(fichiers) if isinstance(fichiers, dict) else fichiers)
        self.assertEqual(code, 1, err)
        self.assertTrue(all(a in err for a in attendus), err)

    def test_conforme(self):
        """Deux modes (espace, *), sous-dossier listé, fichier non listé (compté, non refusé) : conforme."""
        code, out, err = controler(self.arbre({"docs/a/SHA256SUMS": ABC + "  x.md" + NL + VIDE + " *s/v.txt" + NL,
                                               "docs/a/x.md": "abc", "docs/a/s/v.txt": "", "docs/a/R.md": "n",
                                               "docs/c/SHA256SUMS.raw": VIDE + "  absent.md" + NL}))  # L-1 : hors nom
        self.assertTrue(code == 0 and "1 SHA256SUMS, 2 ligne" in out and "1 fichier(s) non listé(s)" in out, err + out)
        self.refuse({"docs/a/SHA256SUMS": VIDE + "  x.md" + NL, "docs/a/x.md": "abc"}, "SHA256SUMS l.1", VIDE, ABC)

    def test_absent_refuse(self):
        """Exemption de sim-niveau : ses 11 lignes exactes, à leurs numéros, dans leur fichier, fichier absent."""
        d = self.arbre({})
        shutil.copytree(os.path.join(RACINE, os.path.dirname(NIVEAU)), os.path.join(d, os.path.dirname(NIVEAU)))
        self.assertEqual(controler(d)[0], 0)
        with open(os.path.join(d, NIVEAU), encoding="utf-8") as f:
            lignes = f.read().split(NL)
        self.refuse(self.arbre({os.path.dirname(NIVEAU) + "/sim_niveau.log.txt": "abc"}, d), "l.12")  # présent
        os.remove(os.path.join(d, os.path.dirname(NIVEAU), "sim_niveau.log.txt"))
        for nom, texte in ((NIVEAU, lignes[1:2] + lignes[:1] + lignes[2:]),     # dans la copie : seules ces lignes
                           (NIVEAU, [lignes[0].replace("execution-B", "execution-C")] + lignes[1:]),
                           ("docs/a/SHA256SUMS", [ABC + "  x.md"]), ("docs/a/SHA256SUMS", lignes)):
            with self.subTest(nom=nom, texte=texte[:2]):
                self.refuse(self.arbre({nom: NL.join(texte)}, d), "l.1 ", "absent")

    def test_formes_refusees(self):
        for texte in ("", NL, ABC.upper() + "  x.md" + NL, ABC + " x.md" + NL, ABC[1:] + "  x.md" + NL,
                      "SHA256 (x.md) = " + ABC + NL, ABC + "  /etc/hostname" + NL, ABC + "  ../b/x.md" + NL,
                      ABC + "  ./x.md" + NL, ABC + "  x.md" + NL + NL, ABC + "  x.md" + chr(13) + NL,
                      ABC + "  x" + chr(92) + "y.md" + NL):     # C-7 (DT4-e) : barre oblique inverse
            with self.subTest(texte=texte):
                self.refuse({"docs/a/SHA256SUMS": texte, "docs/a/x.md": "abc", "docs/b/x.md": "abc"}, "a/SHA256SUMS",
                            "hors forme")     # C-7 : le motif, pas seulement le refus

    def test_interdits(self):
        """SHA256SUMS interdit : jamais lu ; chemin vers un interdit, un *.jsonl ou hors du dossier : refusé. C-5, C-8
        (DT4-e) : tout composant en *.jsonl ; comparaison aussi en casse pliée (système insensible à la casse)."""
        faux = VIDE + "  x.md" + NL
        code, out, err = controler(self.arbre({f"docs/{x}/SHA256SUMS": faux for x in (
            "rapports", "15-x", "16-y.d", "adr-0028/execution", "adr-0028/monark-m009a", "adr-0025", "pocket-report",
            "b/z.jsonl", "Rapports", "adr-0028/EXECUTION", "ADR-0025", "b/Z.Jsonl", "rapport" + chr(0x17F))}))  # s long
        self.assertEqual((code, "0 SHA256SUMS" in out), (0, True), err)
        for chemin in ("monark-m009a/x.md", "execution/x.md", "a/x.jsonl", "z.jsonl/x.md", "Monark-M009A/x.md",
                       "Execution/x.md", "a/x.JSONL", "Z.jsonL/x.md"):
            self.refuse({"docs/adr-0028/SHA256SUMS": f"{ABC}  {chemin}", f"docs/adr-0028/{chemin}": "abc"}, "interdit")
        d = self.arbre({"docs/a/SHA256SUMS": ABC + "  l.md" + NL, "docs/ab/x.md": "abc"})    # C-6 : voisin de préfixe
        os.symlink(os.path.join(d, "docs", "ab", "x.md"), os.path.join(d, "docs", "a", "l.md"))
        self.refuse(d, "docs/a/SHA256SUMS l.1", "lien")
        e = self.arbre({"docs/rapports/SHA256SUMS": ABC + "  x.md" + NL, "docs/a/x.md": "abc"})   # SHA256SUMS lien
        os.symlink(os.path.join(e, "docs", "rapports", "SHA256SUMS"), os.path.join(e, "docs", "a", "SHA256SUMS"))
        self.refuse(e, "docs/a/SHA256SUMS : lien")
        g = self.arbre({"docs/ab/S": ABC + "  x.md" + NL, "docs/a/x.md": "abc"})     # hors du dossier, voisin (C-6)
        os.symlink(os.path.join(g, "docs", "ab", "S"), os.path.join(g, "docs", "a", "SHA256SUMS"))
        self.refuse(g, "docs/a/SHA256SUMS : lien")
        for cible in ("execution/x.md", "a.jsonl"):     # lien vers un interdit sans sortir du dossier (DT4-d, C-1, C-2)
            f = self.arbre({"docs/adr-0028/SHA256SUMS": ABC + "  l.md" + NL, f"docs/adr-0028/{cible}": "abc"})
            os.symlink(cible, os.path.join(f, "docs", "adr-0028", "l.md"))
            self.refuse(f, "l.1 : l.md sous un emplacement interdit")
            os.replace(os.path.join(f, "docs", "adr-0028", "l.md"), os.path.join(f, "docs", "adr-0028", "SHA256SUMS"))
            code, _, err = controler(f)     # SHA256SUMS lien vers l'interdit : refusé, son contenu jamais imprimé
            self.assertEqual((code, "docs/adr-0028/SHA256SUMS : lien" in err, "'abc'" in err), (1, True, False), err)

    def test_liste_egale_sg5(self):     # emplacements interdits de S-G5 (xtask/src/sg5.rs) = liste du contrôle (DT4-b)
        self.assertTrue(os.path.isfile(SCRIPT), SCRIPT)
        interdits = runpy.run_path(SCRIPT)["INTERDITS"]
        with open(os.path.join(RACINE, "xtask", "src", "sg5.rs"), encoding="utf-8") as f:
            sg5 = re.findall('"([^"]+)"', f.read().split("EMPLACEMENTS_INTERDITS: &[&str] = &[", 1)[1].split("];")[0])
        self.assertEqual(sorted(sg5), sorted(interdits))

    def test_erreur(self):
        """Deux racines, racine sans docs/, SHA256SUMS illisible (lien cassé dans son dossier) : sortie 3, jamais 1."""
        d = self.arbre({"docs/a/x.md": "abc"})
        os.symlink(os.path.join(d, "docs", "a", "absent"), os.path.join(d, "docs", "a", "SHA256SUMS"))
        self.assertEqual([controler(d, d)[0], controler(os.path.join(d, "docs"))[0], controler(d)[0]], [3, 3, 3])

    def test_dossier_illisible(self):     # C-4 (DT4-d) : dossier que os.walk ne lit pas : sortie 3, jamais un vert
        d = self.arbre({"docs/a/SHA256SUMS": ABC + "  x.md" + NL, "docs/a/x.md": "abc", "docs/b/c/y.md": ""})
        vrai, bloque = os.scandir, os.path.join(d, "docs", "b")

        def doublure(chemin="."):       # doublure de os.scandir : PermissionError sur docs/b seul
            if os.fspath(chemin) == bloque:
                raise PermissionError(13, "doublure : lecture refusée", chemin)
            return vrai(chemin)
        principal = runpy.run_path(SCRIPT)["main"]
        with mock.patch("os.scandir", doublure), contextlib.redirect_stderr(io.StringIO()) as err:
            self.assertEqual(principal([d]), 3, err.getvalue())

    def test_arbre_du_depot(self):     # une somme périmée ou un fichier listé absent du dépôt fait rougir ce cas
        code, _, err = controler(RACINE)
        self.assertEqual(code, 0, err)
