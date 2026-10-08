"""lancer.sh dans une arborescence jetable (forme de PS2 tests/test_lancer.py l.1-76) : faux paquet (bloc machine), faux
journaux, fausses pièces de PLAN-S2BIS sous leurs épingles, faux scripts du lot qui écrivent leurs arguments, SHA256SUMS
du lot et son sha256 en argument, dépôt git temporaire dont l'arbre (git write-tree, aucun commit) tient lieu de commit
d'analyse. Aucun harnais ni journal réel. Chaque test nomme la mutation qui le rougit."""
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import unittest

import tests

ICI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NL = chr(10)
FAUX = NL.join(["import os, sys", "a = sys.argv", "i = a.index('--sortie')",
                "noms = {'masque_fiv': ['masque_j28.txt', 'fiv_unites.txt'], 'intervalles': ['intervalles.txt']}",
                "for n in noms[os.path.basename(a[0])[:-3]]:", "    with open(os.path.join(a[i + 1], n), 'w') as f:",
                "        g = os.environ.get('PYTHONHASHSEED', '') if 'FAUX_GRAINE' in os.environ else ''",
                "        f.write(' '.join(a[1:i]) + g)",
                "sys.exit(int(os.environ.get('FAUX_CODE_' + os.path.basename(a[0])[:-3], '0')))", ""])
INTERDITS = ["docs/rapports/TEMOIN.md", "docs/adr-0025/TEMOIN.md", "docs/adr-0028/monark-m009a/TEMOIN.md",
             "docs/15-TEMOIN.md", "docs/16-TEMOIN.md", "docs/pocket-report/TEMOIN.md",
             "docs/adr-0028/execution/TEMOIN.md"]                             # septième témoin (P-9)
PAQUET = "docs/adr-0028/PAQUET-PREREG-S2.md"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def ecrire(chemin, texte):
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(texte)


def sha_de(chemin):
    with open(chemin, "rb") as f:
        return sha(f.read())


class TestLancer(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.mkdtemp(prefix="p2_lancer_")
        self.addCleanup(shutil.rmtree, self.t, True)
        self.depot, self.j, self.s, self.x = (os.path.join(self.t, n) for n in ("depot", "j", "sortie", "travail"))
        self.lot = os.path.join(self.depot, "scripts", "plan-s2bis-2")
        os.makedirs(self.lot)
        shutil.copy(os.path.join(ICI, "lancer.sh"), self.lot)
        for s in ("masque_fiv", "intervalles"):
            ecrire(os.path.join(self.lot, s + ".py"), FAUX)
        for x in ["s2-harness/shogen_s2/__init__.py", *INTERDITS]:          # faux harnais et témoins interdits
            ecrire(os.path.join(self.depot, x), "# témoin" + NL)
        g = ["git", "-c", "core.hooksPath=/dev/null", "-C", self.depot]
        subprocess.run(g[:1] + ["init", "-q", self.depot], check=True)
        subprocess.run(g + ["add", "s2-harness", *INTERDITS], check=True)
        self.arbre = subprocess.run(g + ["write-tree"], capture_output=True, text=True, check=True).stdout.strip()
        self.journaux = {n: (n + " faux" + NL).encode() for n in ("control.jsonl", "journal.jsonl", "raw.jsonl")}
        os.makedirs(self.j)
        for n, b in self.journaux.items():
            with open(os.path.join(self.j, n), "wb") as f:
                f.write(b)
        self.bloc = (["commit_analyse " + self.arbre, "sha256_script " + "0" * 64]
                     + [f"journal {n} {sha(b)}" for n, b in self.journaux.items()] + ["sommes " + "0" * 64])
        self.ecrire()

    def ecrire(self, ouvertures=1, fermer=True, commit_prm=None):
        """Faux paquet ; fausses pièces de PLAN-S2BIS (parametres.json : paquet et commit d'analyse) ; parametres.json
        du lot (huit épingles, passes) ; SHA256SUMS du lot ; self.epingle = son sha256."""
        paquet = ("# faux paquet" + NL + ("```shogen-paquet-v1" + NL) * ouvertures + NL.join(self.bloc) + NL
                  + ("```" + NL if fermer else "") + "fin" + NL)
        ecrire(os.path.join(self.depot, PAQUET), paquet)
        c = tests.PRM["plan_s2bis"]["chemins"]
        ps2 = {"paquet_s2": {"chemin": PAQUET, "sha256": sha(paquet.encode())},
               "commit_analyse": commit_prm or self.arbre}
        for k, rel in c.items():
            ecrire(os.path.join(self.depot, rel), json.dumps(ps2) if k == "parametres" else f"pièce {k}" + NL)
        lot = {"plan_s2bis": {"chemins": c, "sha256": {k: sha_de(os.path.join(self.depot, r)) for k, r in c.items()}},
               "passes": {"variable": "PYTHONHASHSEED", "A": 0, "B": 1}}
        ecrire(os.path.join(self.lot, "parametres.json"), json.dumps(lot))
        sommes = "".join(f"{sha_de(os.path.join(self.lot, n))}  {n}" + NL
                         for n in ("intervalles.py", "lancer.sh", "masque_fiv.py", "parametres.json"))
        ecrire(os.path.join(self.lot, "SHA256SUMS"), sommes)
        self.epingle = sha(sommes.encode())

    def lancer(self, *args, **env):
        e = {k: v for k, v in os.environ.items() if k != "SHOGEN_S2_CAMPAGNE_CONTROL"}
        e.update(env)
        a = list(args) or [self.j, self.s, self.x, self.epingle]
        return subprocess.run(["bash", os.path.join(self.lot, "lancer.sh"), *a], capture_output=True, text=True, env=e)

    def assertRien(self, r, code, refus):
        """Code et refus nommé attendus ; aucun script lancé, aucune extraction (dossier de travail absent)."""
        self.assertEqual((r.returncode, r.stderr.split(" : ")[0]), (code, "REFUS " + refus), r.stderr)
        self.assertFalse(os.path.exists(self.x) or os.path.exists(os.path.join(self.s, "masque_j28.txt")))

    def test_epingle(self):
        """T-P2-LAN-3. Argument différent du sha256 du SHA256SUMS du lot ; fichier du lot altéré après l'épingle
        (sha256sum -c en échec) : P2/epingle ; parametres.json de PLAN-S2BIS altéré après son épingle : P2/plan-s2bis ;
        code 3. Mutation M-P2-23 : épingle non comparée à l'argument ; M-P2R4-1 : sha256sum -c omis ; M-P2R4-2 : épingle
        du parametres.json de PLAN-S2BIS non contrôlée."""
        self.assertRien(self.lancer(self.j, self.s, self.x, "0" * 64), 3, "P2/epingle")
        with open(os.path.join(self.lot, "masque_fiv.py"), "a", encoding="utf-8") as f:
            f.write("# altéré" + NL)
        self.assertRien(self.lancer(), 3, "P2/epingle")
        self.ecrire()
        with open(os.path.join(self.depot, tests.PRM["plan_s2bis"]["chemins"]["parametres"]), "a") as f:
            f.write(" ")
        self.assertRien(self.lancer(), 3, "P2/plan-s2bis")

    def test_variable_journaux_sortie_usage(self):
        """T-P2-LAN-6 (début). Variable posée à une valeur fictive dans le seul sous-processus du lanceur (exception
        A-3, E-P2-05) : P2/variable ; dossier des journaux absent : P2/journal ; sortie non vide, ou ne contenant qu'une
        entrée cachée : P2/sortie ; code 3 ; trois arguments : P2/usage, code 2. Mutation M-P2-21 : garde de la
        variable retirée ; M-P2-22 : sortie non vide admise ; M-P2R4-3 : dossier des journaux non contrôlé ; G-23 (G2) :
        entrées cachées ignorées (ls) ; M-P2R4-9 : idem (find) ; M-P2R4-10 : idem (filtre des noms en point)."""
        self.assertRien(self.lancer(SHOGEN_S2_CAMPAGNE_CONTROL="x"), 3, "P2/variable")
        r = self.lancer(self.j + "-absent", self.s, self.x, self.epingle)
        self.assertEqual((r.returncode, r.stderr), (3, "REFUS P2/journal : dossier des journaux absent" + NL))
        for n in ("vieux", ".cache"):
            shutil.rmtree(self.s, True)
            ecrire(os.path.join(self.s, n), "x")
            r = self.lancer()
            self.assertEqual((r.returncode, r.stderr.split(" : ")[0], os.path.exists(self.x)),
                             (3, "REFUS P2/sortie", False))
        shutil.rmtree(self.s)
        self.assertRien(self.lancer(self.j, self.s, self.x), 2, "P2/usage")

    def test_paquet_et_bloc(self):
        """T-P2-LAN-4. Paquet altéré après son épingle ; bloc machine ouvert deux fois ; bloc non fermé : P2/paquet,
        code 3. Mutation M-P2-24 : sha256 du paquet non contrôlé ; M-P2-25 : ouverture multiple admise ; M-P2R4-4 :
        clôture non exigée."""
        with open(os.path.join(self.depot, PAQUET), "a", encoding="utf-8") as f:
            f.write("ajout" + NL)
        self.assertRien(self.lancer(), 3, "P2/paquet")
        for cas in ({"ouvertures": 2}, {"fermer": False}):
            self.ecrire(**cas)
            self.assertRien(self.lancer(), 3, "P2/paquet")

    def test_journal(self):
        """T-P2-LAN-5. sha256 d'un journal différent du bloc ; ligne « journal » malformée au bloc ; journal nommé au
        bloc par un nom commençant par « . » (présent, de sha256 égal) ; journal nommé absent ; control.jsonl non nommé
        au bloc : P2/journal, code 3. Mutation M-P2-26 : sha256 des journaux non comparés ; M-P2R4-5 : journal absent
        admis ; M-P2R4-7 : control.jsonl et journal.jsonl non exigés au bloc ; M-P2R4-8 : ligne malformée admise ; G-26
        (G2) : nom en point admis ; M-P2R4-11 : seuls les noms en « .. » refusés ; M-P2R4-12 : seul « . » refusé."""
        with open(os.path.join(self.j, "raw.jsonl"), "ab") as f:
            f.write(b"x")
        self.assertRien(self.lancer(), 3, "P2/journal")
        with open(os.path.join(self.j, "raw.jsonl"), "wb") as f:
            f.write(self.journaux["raw.jsonl"])
        self.bloc.append("journal autre.jsonl " + "0" * 63)
        self.ecrire()
        r = self.lancer()
        self.assertEqual((r.returncode, r.stderr),
                         (3, "REFUS P2/journal : ligne journal malformée au bloc machine" + NL))
        self.bloc.pop()
        with open(os.path.join(self.j, ".cache.jsonl"), "wb") as f:
            f.write(b"x")
        self.bloc.append("journal .cache.jsonl " + sha(b"x"))
        self.ecrire()
        r = self.lancer()
        self.assertEqual((r.returncode, r.stderr), (3, "REFUS P2/journal : nom de journal refusé" + NL))
        self.bloc.pop()
        self.bloc = [x for x in self.bloc if not x.startswith("journal control.jsonl ")]
        self.ecrire()
        self.assertRien(self.lancer(), 3, "P2/journal")
        os.remove(os.path.join(self.j, "journal.jsonl"))
        r = self.lancer()
        self.assertEqual((r.returncode, r.stderr), (3, "REFUS P2/journal : journal absent : journal.jsonl" + NL))

    def test_commit_extraction(self):
        """T-P2-LAN-6 (fin). Commit du bloc différent du commit d'analyse : P2/commit ; extraction déjà présente dans
        le dossier de travail : P2/sortie ; code 3. Mutation M-P2-27 : commit du bloc non comparé ; M-P2R4-6 :
        extraction déjà présente admise."""
        self.ecrire(commit_prm="f" * 40)
        self.assertRien(self.lancer(), 3, "P2/commit")
        self.ecrire()
        os.makedirs(os.path.join(self.x, self.arbre[:7]))
        r = self.lancer()
        self.assertEqual((r.returncode, r.stderr.split(" : ")[0], os.listdir(self.x)),
                         (3, "REFUS P2/sortie", [self.arbre[:7]]))

    def test_lancement_complet(self):
        """T-P2-LAN-1 et T-P2-LAN-2. Code 0 ; sortie = passe A (trois sorties et SHA256SUMS, octet pour octet) ;
        arguments des scripts : --harnais de l'extraction du dossier de travail, journaux, parametres.json du lot ;
        écran fait de noms, de codes et de sha256 seuls ; aucun des sept témoins des dossiers interdits extrait.
        Mutation M-P2-38 : harnais pris au dépôt ; M-P2-28 : exclusions retirées ; M-P2R5-1 : docs/adr-0028/execution
        non exclu (P-9)."""
        r = self.lancer()
        self.assertEqual(r.returncode, 0, r.stderr)
        x = os.path.join(self.x, self.arbre[:7])
        self.assertEqual(sorted(os.listdir(self.s)), ["SHA256SUMS", "fiv_unites.txt", "intervalles.txt",
                                                      "masque_j28.txt"])
        for n in os.listdir(self.s):
            self.assertEqual(sha_de(os.path.join(self.s, n)), sha_de(os.path.join(self.x, "A", n)), n)
        with open(os.path.join(self.s, "masque_j28.txt"), encoding="utf-8") as f:
            a = f.read().split(" ")
        self.assertEqual([a[a.index(o) + 1] for o in ("--journaux", "--harnais", "--parametres")],
                         [self.j, os.path.join(x, "s2-harness"), os.path.join(self.lot, "parametres.json")])
        for ligne in r.stdout.splitlines():
            hexa = len(ligne) > 66 and ligne[64:66] == "  " and set(ligne[:64]) <= set("0123456789abcdef")
            self.assertTrue(hexa or ligne.endswith((" : code 0", " : sha256 égal au bloc machine")), ligne)
        self.assertEqual(([t for t in INTERDITS if os.path.exists(os.path.join(x, t))], os.path.isdir(
            os.path.join(x, "s2-harness"))), ([], True))

    def test_extraction_impossible_script_en_echec(self):
        """T-P2-LAN-7. Arbre inconnu du dépôt (bloc et paramètres d'accord) : code 4, aucun script ; masque_fiv à 1 dans
        la passe A : code 5, rien dans la sortie, intervalles non lancé, passe B non commencée (P-7). Mutation
        M-P2-29 : échec d'un script non reporté."""
        self.bloc[0] = "commit_analyse " + "e" * 40
        self.ecrire(commit_prm="e" * 40)
        r = self.lancer()
        self.assertEqual((r.returncode, os.path.exists(os.path.join(self.x, "A"))), (4, False), r.stderr)
        self.bloc[0] = "commit_analyse " + self.arbre
        self.ecrire()
        shutil.rmtree(self.x)
        r = self.lancer(FAUX_CODE_masque_fiv="1")
        a, b = (os.path.join(self.x, n) for n in "AB")
        self.assertEqual((r.returncode, sorted(os.listdir(a)), os.path.exists(b), os.path.exists(self.s)),
                         (5, ["fiv_unites.txt", "masque_j28.txt"], False, False))

    def test_identite_a_b(self):
        """T-P2-LAN-8. Faux scripts dont la sortie dépend de PYTHONHASHSEED : P2/identite, code 5, sortie absente, les
        deux SHA256SUMS (six lignes de sha256) à l'écran. Mutation M-P2-30 : comparaison de A et B retirée ; M-P2R5-2 :
        même graine pour A et B."""
        r = self.lancer(FAUX_GRAINE="1")
        hexa = [x for x in r.stdout.splitlines() if x[64:66] == "  " and set(x[:64]) <= set("0123456789abcdef")]
        self.assertEqual((r.returncode, r.stderr.split(" : ")[0], len(hexa), os.path.exists(self.s)),
                         (5, "REFUS P2/identite", 6, False))

    def test_epingles_plan_s2bis(self):
        """T-P2-LAN-9. Copie altérée de chacune des sept autres pièces épinglées de PLAN-S2BIS : P2/plan-s2bis, code 3.
        Mutation M-P2-39 : épingles de PLAN-S2BIS non contrôlées au lanceur."""
        for k, rel in tests.PRM["plan_s2bis"]["chemins"].items():
            if k != "parametres":
                self.ecrire()
                with open(os.path.join(self.depot, rel), "a", encoding="utf-8") as f:
                    f.write(" ")
                self.assertRien(self.lancer(), 3, "P2/plan-s2bis")
