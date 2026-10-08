"""lancer.sh dans une arborescence jetable (forme de PS2 tests/test_lancer.py l.1-76) : faux paquet (bloc machine), faux
journaux, fausses pièces de PLAN-S2BIS sous leurs épingles, faux scripts du lot qui écrivent leurs arguments, SHA256SUMS
du lot et son sha256 en argument, dépôt git temporaire dont l'arbre (git write-tree, aucun commit) tient lieu de commit
d'analyse. Aucun harnais ni journal réel. Les faux scripts importent un faux socle, qui charge commun de PLAN-S2BIS par
son chemin (forme de socle.charger_module), et lisent leur code de sortie et la dépendance à la graine dans la clé
« faux » du parametres.json du lot : l'environnement des scripts est une liste fermée (C-1 de la G2). Chaque test nomme
la mutation qui le rougit."""
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
FAUX = NL.join(["import os, sys", "import socle", "a, faux = sys.argv, socle.P['faux']",
                "nom, i = os.path.basename(a[0])[:-3], a.index('--sortie')",
                "noms = {'masque_fiv': ['masque_j28.txt', 'fiv_unites.txt'], 'intervalles': ['intervalles.txt']}",
                "for n in noms[nom] if faux.get('ecrire', True) else []:",
                "    with open(os.path.join(a[i + 1], n), 'w') as f:",
                "        f.write(' '.join(a[1:i]) + (os.environ['PYTHONHASHSEED'] if faux.get('graine') else ''))",
                "sys.exit(faux.get('code', {}).get(nom, 0))", ""])
SOCLE = NL.join(["import importlib.util, json, os", "ICI = os.path.dirname(os.path.abspath(__file__))",
                 "with open(os.path.join(ICI, 'parametres.json'), encoding='utf-8') as f:", "    P = json.load(f)",
                 "c = os.path.join(os.path.dirname(os.path.dirname(ICI)), P['plan_s2bis']['chemins']['commun'])",
                 "m = importlib.util.spec_from_file_location('commun', c)",
                 "m.loader.exec_module(importlib.util.module_from_spec(m))", ""])
FORGE = NL.join(["import importlib.util, marshal, os, sys", "src, marque = sys.argv[1:]",
                 "with open(src, encoding='utf-8') as f:", "    texte = f.read()",
                 "ajout = 'open(' + repr(marque) + ', ' + repr('a') + ').write(__name__ + chr(10))'",
                 "code = compile(texte + chr(10) + ajout + chr(10), src, 'exec')",
                 "st, cible = os.stat(src), importlib.util.cache_from_source(src)",
                 "os.makedirs(os.path.dirname(cible), exist_ok=True)", "with open(cible, 'wb') as f:",
                 "    f.write(importlib.util.MAGIC_NUMBER + bytes(4) + int(st.st_mtime).to_bytes(4, 'little')",
                 "            + st.st_size.to_bytes(4, 'little') + marshal.dumps(code))", ""])
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


def ombre(marque):
    """json.py d'ombre transparent : note son exécution dans marque, puis rend le vrai json."""
    return NL.join(["import os, sys", f"with open({marque!r}, 'a', encoding='utf-8') as f:",
                    "    f.write('ombre json' + chr(10))", "ici = os.path.dirname(os.path.abspath(__file__))",
                    "sys.path[:] = [x for x in sys.path if os.path.abspath(x or '.') != ici]",
                    "del sys.modules['json']", "import json", ""])


def vu(marque):
    """Marqueur d'exécution étrangère présent ; retiré après lecture."""
    if os.path.exists(marque):
        os.remove(marque)
        return True
    return False


def forger(src, marque):
    """Bytecode forgé de src (ajout : écrire __name__ dans marque), en-tête aux mtime et taille de src, dans le
    __pycache__ voisin, au format du python3 que le lanceur appelle."""
    subprocess.run(["python3", "-I", "-c", FORGE, src, marque], check=True)


class TestLancer(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.mkdtemp(prefix="p2_lancer_")
        self.addCleanup(shutil.rmtree, self.t, True)
        self.depot, self.j, self.s, self.x = (os.path.join(self.t, n) for n in ("depot", "j", "sortie", "travail"))
        self.lot = os.path.join(self.depot, "scripts", "plan-s2bis-2")
        os.makedirs(self.lot)
        shutil.copy(os.path.join(ICI, "lancer.sh"), self.lot)
        for s, texte in (("masque_fiv", FAUX), ("intervalles", FAUX), ("socle", SOCLE)):
            ecrire(os.path.join(self.lot, s + ".py"), texte)
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

    def ecrire(self, ouvertures=1, fermer=True, commit_prm=None, faux=None, modif=None):
        """Faux paquet ; fausses pièces de PLAN-S2BIS (parametres.json : paquet et commit d'analyse ; les autres, des
        commentaires) ; parametres.json du lot (huit épingles, passes, faux, modif éventuel) ; SHA256SUMS du lot ;
        self.epingle = son sha256."""
        paquet = ("# faux paquet" + NL + ("```shogen-paquet-v1" + NL) * ouvertures + NL.join(self.bloc) + NL
                  + ("```" + NL if fermer else "") + "fin" + NL)
        ecrire(os.path.join(self.depot, PAQUET), paquet)
        c = dict(tests.PRM["plan_s2bis"]["chemins"])
        ps2 = {"paquet_s2": {"chemin": PAQUET, "sha256": sha(paquet.encode())},
               "commit_analyse": commit_prm or self.arbre}
        for k, rel in c.items():
            ecrire(os.path.join(self.depot, rel), json.dumps(ps2) if k == "parametres" else f"# pièce {k}" + NL)
        lot = {"plan_s2bis": {"chemins": c, "sha256": {k: sha_de(os.path.join(self.depot, r)) for k, r in c.items()}},
               "passes": {"variable": "PYTHONHASHSEED", "A": 0, "B": 1}, "faux": faux or {}}
        if modif:
            modif(lot)
        ecrire(os.path.join(self.lot, "parametres.json"), json.dumps(lot))
        sommes = "".join(f"{sha_de(os.path.join(self.lot, n))}  {n}" + NL
                         for n in ("intervalles.py", "lancer.sh", "masque_fiv.py", "parametres.json", "socle.py"))
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
        """T-P2-LAN-6 (fin). Commit du bloc différent du commit d'analyse : P2/commit ; extraction, ou cache de bytecode
        (pyc, C-1 b), déjà présents dans le dossier de travail : P2/sortie ; code 3. Mutation M-P2-27 : commit du bloc
        non comparé ; M-P2R4-6 : extraction déjà présente admise ; M-P2R6-9 : cache de bytecode déjà présent admis."""
        self.ecrire(commit_prm="f" * 40)
        self.assertRien(self.lancer(), 3, "P2/commit")
        self.ecrire()
        os.makedirs(os.path.join(self.x, self.arbre[:7]))
        r = self.lancer()
        self.assertEqual((r.returncode, r.stderr.split(" : ")[0], os.listdir(self.x)),
                         (3, "REFUS P2/sortie", [self.arbre[:7]]))
        os.rename(os.path.join(self.x, self.arbre[:7]), os.path.join(self.x, "pyc"))
        r = self.lancer()
        self.assertEqual((r.returncode, r.stderr.split(" : ")[0], os.listdir(self.x)), (3, "REFUS P2/sortie", ["pyc"]))

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
        self.ecrire(faux={"code": {"masque_fiv": 1}})
        shutil.rmtree(self.x)
        r = self.lancer()
        a, b = (os.path.join(self.x, n) for n in "AB")
        self.assertEqual((r.returncode, sorted(os.listdir(a)), os.path.exists(b), os.path.exists(self.s)),
                         (5, ["fiv_unites.txt", "masque_j28.txt"], False, False))

    def test_identite_a_b(self):
        """T-P2-LAN-8. Faux scripts dont la sortie dépend de PYTHONHASHSEED : P2/identite, code 5, sortie absente, les
        deux SHA256SUMS (six lignes de sha256) à l'écran. Mutation M-P2-30 : comparaison de A et B retirée ; M-P2R5-2 :
        même graine pour A et B."""
        self.ecrire(faux={"graine": True})
        r = self.lancer()
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

    def test_entree_hors_sommes(self):
        """T-P2-LAN-10 (C-1 c de la G2, vecteur S8). Entrée du dossier du lot absente de SHA256SUMS, dossiers à part :
        json.py d'ombre à côté des scripts ; fichier caché dans un sous-dossier : P2/epingle, code 3, rien d'exécuté.
        Mutation M-P2R6-1 : contrôle des entrées retiré ; M-P2R6-2 : sous-dossiers non parcourus ; M-P2R6-3 :
        entrées cachées ignorées."""
        marque = os.path.join(self.t, "marque")
        for i, rel in enumerate(("json.py", "sous/.cache")):
            ecrire(os.path.join(self.lot, rel), ombre(marque))
            r = self.lancer(self.j, self.s + str(i), self.x + str(i), self.epingle)
            os.remove(os.path.join(self.lot, rel))
            self.assertEqual((r.returncode, r.stderr.split(" : ")[0], vu(marque)), (3, "REFUS P2/epingle", False), rel)

    def test_ombre_pythonpath(self):
        """T-P2-LAN-11 (C-1 a et b de la G2, vecteur S9). json.py d'ombre dans un dossier passé par PYTHONPATH : jamais
        exécuté (parametres.json lus en python3 -I ; scripts sous env -i, liste fermée), code 0, quatre sorties.
        Mutation M-P2R6-4 : premier heredoc sans -I ; M-P2R6-5 : second heredoc sans -I ; M-P2R6-6 : environnement
        des scripts hérité."""
        marque, pp = os.path.join(self.t, "marque"), os.path.join(self.t, "pp")
        ecrire(os.path.join(pp, "json.py"), ombre(marque))
        r = self.lancer(PYTHONPATH=pp)
        self.assertEqual((r.returncode, os.path.exists(marque), len(os.listdir(self.s))), (0, False, 4), r.stderr)

    def test_bytecode(self):
        """T-P2-LAN-12 (C-1 b et c de la G2, vecteur S22). Bytecode forgé, en-tête aux mtime et taille de la source
        épinglée : dans scripts/plan-s2bis-2/__pycache__ (socle), P2/epingle, code 3 ; dans
        scripts/plan-s2bis/__pycache__ (commun), ignoré (PYTHONPYCACHEPREFIX vers <travail>/pyc), code 0 ; jamais
        exécuté. Mutation M-P2R6-7 : PYTHONPYCACHEPREFIX retiré ; M-P2R6-8 : __pycache__ hors du contrôle des
        entrées."""
        marque = os.path.join(self.t, "marque")
        ps2 = os.path.join(self.depot, tests.PRM["plan_s2bis"]["chemins"]["commun"])
        for i, (src, code, refus) in enumerate(((os.path.join(self.lot, "socle.py"), 3, "REFUS P2/epingle"),
                                                (ps2, 0, ""))):
            forger(src, marque)
            r = self.lancer(self.j, self.s + str(i), self.x + str(i), self.epingle)
            shutil.rmtree(os.path.join(os.path.dirname(src), "__pycache__"))
            self.assertEqual((r.returncode, r.stderr.split(" : ")[0], vu(marque)), (code, refus, False), r.stderr)

    def test_site_hostile(self):
        """T-P2-LAN-14 (Q-CORR-5 adjugée : python3 -S). Préfixe jetable : venv sous TMPDIR, dont le python3 précède
        celui du système dans PATH et dont le site-packages porte un .pth hostile (le site utilisateur passe par le
        même module site, qu'on n'écrit jamais dans le HOME réel) ; parametres.json lus en -I -S, scripts en -S :
        rien d'exécuté, code 0, quatre sorties. Mutation M-P2R6-18 : scripts sans -S ; M-P2R6-19 : premier heredoc
        sans -S ; M-P2R6-20 : second heredoc sans -S."""
        venv, marque = os.path.join(self.t, "venv"), os.path.join(self.t, "marque")
        subprocess.run(["python3", "-I", "-m", "venv", "--without-pip", venv], check=True)
        site = subprocess.run([os.path.join(venv, "bin", "python3"), "-I", "-c", "import sysconfig; print(sysconfig."
                               "get_path('purelib'))"], capture_output=True, text=True, check=True).stdout.strip()
        ecrire(os.path.join(site, "zz_hostile.pth"), f"import os; open({marque!r}, 'a').write('pth' + chr(10))" + NL)
        r = self.lancer(PATH=os.path.join(venv, "bin") + os.pathsep + os.environ["PATH"])
        self.assertEqual((r.returncode, vu(marque), len(os.listdir(self.s))), (0, False, 4), r.stderr)

    def test_sorties_nommees(self):
        """T-P2-LAN-13 (SHOGEN-PLAN-S2BIS-2-REFUS-NON-NOMMES-1, lanceur). Toute sortie hors 0 nommée, aucune trace
        Python ni de bash à l'écran : parametres.json du lot sans passes, ou sans la pièce parametres (épingle
        renommée) : P2/plan-s2bis seul ; dossier de travail qui est un fichier : extraction impossible, code 4 ;
        dossier de passe qui est un fichier, ou script en 0 sans sorties : code 5 ; sortie sous un fichier : copie
        impossible, code 5. Mutation M-P2R6-10 : erreurs des heredocs à l'écran ; M-P2R6-11 : création du travail non
        nommée ; M-P2R6-12 : dossier de passe non nommé ; M-P2R6-13 : sommes de passe non nommées ; M-P2R6-14 : copie
        non nommée ; M-P2R6-15 : pièce parametres non exigée (variable non liée, code 1)."""
        def renommer(p):
            for d in p["plan_s2bis"]["chemins"], p["plan_s2bis"]["sha256"]:
                d["autre"] = d.pop("parametres")
        for modif in (lambda p: p.pop("passes"), renommer):
            self.ecrire(modif=modif)
            r = self.lancer()
            self.assertEqual((r.returncode, r.stderr), (3, "REFUS P2/plan-s2bis : épingles de PLAN-S2BIS illisibles "
                                                           "dans parametres.json du lot" + NL))
        f, w = (os.path.join(self.t, n) for n in ("fichier", "w"))
        for n in (f, os.path.join(w, "A")):
            ecrire(n, "x")
        for t, s, faux, attendu in ((f, self.s, None, "extraction impossible : code 4"),
                                    (w, self.s, None, "passe A : dossier impossible : code 5"),
                                    (self.x, self.s, {"ecrire": False}, "passe A : SHA256SUMS impossible : code 5"),
                                    (w + "2", os.path.join(f, "s"), None, "copie de la passe A impossible : code 5")):
            self.ecrire(faux=faux)
            r = self.lancer(self.j, s, t, self.epingle)
            self.assertEqual((r.returncode, r.stderr), (int(attendu[-1]), attendu + NL))
