"""lancer.sh dans une arborescence jetable : faux paquet (bloc machine), faux journaux, faux scripts qui écrivent leurs
arguments, dépôt git temporaire dont l'arbre (git write-tree, aucun commit) tient lieu de commit d'analyse. Aucun
harnais ni journal réel. Chaque test nomme la mutation qui le rougit."""
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import unittest

ICI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NL = chr(10)
FAUX = ("import os, sys" + NL + "a = sys.argv" + NL + "with open(a[a.index('--sortie') + 1], 'w') as f:" + NL
        + "    f.write(' '.join(a[1:]))" + NL
        + "sys.exit(int(os.environ.get('FAUX_CODE_' + os.path.basename(a[0])[:-3], '0')))" + NL)
INTERDITS = ["docs/rapports/TEMOIN.md", "docs/adr-0025/TEMOIN.md", "docs/adr-0028/monark-m009a/TEMOIN.md",
             "docs/15-TEMOIN.md", "docs/16-TEMOIN.md", "docs/pocket-report/TEMOIN.md"]


def sha(b):
    return hashlib.sha256(b).hexdigest()


class TestLancer(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.mkdtemp(prefix="plan_lancer_")
        self.addCleanup(shutil.rmtree, self.t, True)
        self.depot, self.j = os.path.join(self.t, "depot"), os.path.join(self.t, "journaux")
        self.s, self.x = os.path.join(self.t, "sortie"), os.path.join(self.t, "travail")
        ici = os.path.join(self.depot, "scripts", "plan-s2bis")
        os.makedirs(ici)
        os.makedirs(self.j)
        shutil.copy(os.path.join(ICI, "lancer.sh"), ici)
        for s in ("tau_sigma", "episodes", "okx"):
            with open(os.path.join(ici, s + ".py"), "w") as f:
                f.write(FAUX)
        for x in ["s2-harness/shogen_s2/__init__.py", *INTERDITS]:           # faux harnais et témoins interdits
            os.makedirs(os.path.dirname(os.path.join(self.depot, x)), exist_ok=True)
            with open(os.path.join(self.depot, x), "w") as f:
                f.write("# témoin" + NL)
        g = ["git", "-c", "core.hooksPath=/dev/null", "-C", self.depot]
        subprocess.run(g[:1] + ["init", "-q", self.depot], check=True)
        subprocess.run(g + ["add", "s2-harness", *INTERDITS], check=True)
        self.arbre = subprocess.run(g + ["write-tree"], capture_output=True, text=True, check=True).stdout.strip()
        self.journaux = {n: (n + " faux" + NL).encode() for n in ("control.jsonl", "journal.jsonl", "raw.jsonl")}
        for n, b in self.journaux.items():
            with open(os.path.join(self.j, n), "wb") as f:
                f.write(b)
        self.bloc = (["commit_analyse " + self.arbre, "sha256_script " + "0" * 64]
                     + [f"journal {n} {sha(b)}" for n, b in self.journaux.items()] + ["sommes " + "0" * 64])
        self.ecrire()

    def ecrire(self, ouvertures=1, fermer=True, commit_prm=None):
        texte = "# faux paquet" + NL + ("```shogen-paquet-v1" + NL) * ouvertures + NL.join(self.bloc) + NL
        texte += ("```" + NL if fermer else "") + "fin" + NL
        os.makedirs(os.path.join(self.depot, "docs", "adr-0028"), exist_ok=True)
        with open(os.path.join(self.depot, "docs", "adr-0028", "PAQUET-PREREG-S2.md"), "w", encoding="utf-8") as f:
            f.write(texte)
        p = {"paquet_s2": {"chemin": "docs/adr-0028/PAQUET-PREREG-S2.md", "sha256": sha(texte.encode())},
             "commit_analyse": commit_prm or self.arbre}
        with open(os.path.join(self.depot, "scripts", "plan-s2bis", "parametres.json"), "w", encoding="utf-8") as f:
            json.dump(p, f)

    def lancer(self, *args, **env):
        e = {k: v for k, v in os.environ.items() if k != "SHOGEN_S2_CAMPAGNE_CONTROL"}
        e.update(env)
        a = list(args) or [self.j, self.s, self.x]
        return subprocess.run(["bash", os.path.join(self.depot, "scripts", "plan-s2bis", "lancer.sh"), *a],
                              capture_output=True, text=True, env=e)

    def assertRien(self, r, code):
        """Code attendu, aucun script lancé, aucune extraction."""
        self.assertEqual(r.returncode, code, r.stderr)
        self.assertFalse(os.path.exists(os.path.join(self.s, "okx.txt")) or os.path.exists(self.x))

    def test_lancement_complet(self):
        """Code 0 ; extraction de l'arbre ; trois sorties dont les arguments désignent l'extraction, les journaux et les
        paramètres ; stdout : noms, codes et sha256 seulement. Mutation ML-1 : --harnais pris au dépôt (s2-harness de la
        tête) au lieu de l'extraction."""
        r = self.lancer()
        self.assertEqual(r.returncode, 0, r.stderr)
        x = os.path.join(self.x, self.arbre[:7])
        self.assertTrue(os.path.isfile(os.path.join(x, "s2-harness", "shogen_s2", "__init__.py")))
        for s in ("tau_sigma", "episodes", "okx"):
            with open(os.path.join(self.s, s + ".txt")) as f:
                a = f.read().split(" ")
            self.assertEqual(a[a.index("--harnais") + 1], os.path.join(x, "s2-harness"))
            self.assertEqual((a[a.index("--journaux") + 1], a[a.index("--sortie") + 1]),
                             (self.j, os.path.join(self.s, s + ".txt")))
        for ligne in r.stdout.splitlines():
            hexa = len(ligne) > 66 and ligne[64:66] == "  " and set(ligne[:64]) <= set("0123456789abcdef")
            self.assertTrue(hexa or ligne.endswith((" : code 0", " : sha256 égal au bloc machine")), ligne)
        with open(os.path.join(self.s, "SHA256SUMS")) as f:
            self.assertEqual(len(f.read().splitlines()), 3)

    def test_dossiers_interdits_non_extraits(self):
        """Un témoin dans chacun des six dossiers interdits de l'arbre : code 0, aucun extrait. Prototype P-5 du réviseur.
        Mutation RV-15 : exclusions retirées de l'extraction."""
        r = self.lancer()
        x = os.path.join(self.x, self.arbre[:7])
        self.assertEqual((r.returncode, os.path.isdir(os.path.join(x, "s2-harness"))), (0, True), r.stderr)
        self.assertEqual([t for t in INTERDITS if os.path.exists(os.path.join(x, t))], [])

    def test_refus_sha_journal(self):
        """Mutation ML-2 : comparaison des sha256 des journaux retirée."""
        with open(os.path.join(self.j, "raw.jsonl"), "ab") as f:
            f.write(b"x")
        self.assertRien(self.lancer(), 3)

    def test_refus_paquet_non_epingle(self):
        """Mutation ML-3 : sha256 du paquet non contrôlé."""
        with open(os.path.join(self.depot, "docs", "adr-0028", "PAQUET-PREREG-S2.md"), "a") as f:
            f.write("ajout" + NL)
        self.assertRien(self.lancer(), 3)

    def test_refus_bloc_double_ou_non_ferme(self):
        """Mutation ML-4 : nombre d'ouvertures non contrôlé ; ML-5 : clôture non exigée."""
        self.ecrire(ouvertures=2)
        self.assertRien(self.lancer(), 3)
        self.ecrire(fermer=False)
        self.assertRien(self.lancer(), 3)

    def test_refus_commit_journal_variable_sortie_usage(self):
        """Commit du bloc différent de parametres.json, journal absent, variable posée, sortie non vide : 3 ; usage : 2.
        Exception écrite (adjudication A-3) : la variable est posée à une valeur fictive dans le seul sous-processus du
        lanceur, qui refuse à sa ligne 27 ; aucun test du harnais n'y tourne. Mutation ML-6 : commit du bloc non comparé."""
        self.ecrire(commit_prm="f" * 40)
        self.assertRien(self.lancer(), 3)
        self.ecrire()
        self.assertRien(self.lancer(SHOGEN_S2_CAMPAGNE_CONTROL="x"), 3)
        os.makedirs(self.s)
        with open(os.path.join(self.s, "vieux"), "w") as f:
            f.write("x")
        self.assertEqual(self.lancer().returncode, 3)
        shutil.rmtree(self.s)
        os.remove(os.path.join(self.j, "journal.jsonl"))
        self.assertRien(self.lancer(), 3)
        self.assertEqual(self.lancer(self.j, self.s).returncode, 2)

    def test_extraction_impossible_et_script_en_echec(self):
        """Arbre inconnu du dépôt (bloc et paramètres d'accord) : 4, aucun script ; un script à 1 : 5, les deux autres
        lancés. Mutation ML-7 : échec d'un script non reporté au code de sortie."""
        self.bloc[0] = "commit_analyse " + "e" * 40
        self.ecrire(commit_prm="e" * 40)
        r = self.lancer()
        self.assertEqual(r.returncode, 4, r.stderr)
        self.assertFalse(os.path.exists(os.path.join(self.s, "tau_sigma.txt")))
        self.bloc[0] = "commit_analyse " + self.arbre
        self.ecrire()
        shutil.rmtree(self.x)
        r = self.lancer(FAUX_CODE_episodes="1")
        self.assertEqual((r.returncode, sorted(os.listdir(self.s))),
                         (5, ["SHA256SUMS", "episodes.txt", "okx.txt", "tau_sigma.txt"]))


if __name__ == "__main__":
    unittest.main()
