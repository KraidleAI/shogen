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
             "docs/15-TEMOIN.md", "docs/16-TEMOIN.md", "docs/pocket-report/TEMOIN.md"]
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
