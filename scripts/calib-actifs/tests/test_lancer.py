"""lancer.sh dans un dossier de lot jetable (T-CA-LAN-1 à 6 ; E-CA-03, E-CA-21, E-CA-24 ; forme des tests du lanceur de
PLAN-S2BIS-2) : faux acquerir.py et faux tau.py qui écrivent leurs sorties et lisent leur code dans la clé « faux » du
parametres.json du lot ; SHA256SUMS du lot et son sha256 en argument. Exception écrite (E-CA-03) : seul ce module pose
SHOGEN_S2_CAMPAGNE_CONTROL, à une valeur fictive, dans le seul sous-processus du lanceur. Chaque test nomme sa mutation.
"""
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import unittest

ICI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NL = chr(10)
TETE = ["import json, os, sys", "a = sys.argv",
        "f = json.load(open(os.path.join(os.path.dirname(os.path.abspath(a[0])), 'parametres.json'),"
        " encoding='utf-8'))['faux']"]
ACQ = NL.join(TETE + ["b = a[a.index('--bruts') + 1]", "os.makedirs(b, exist_ok=True)",
                      "open(os.path.join(b, 'manifeste.tsv'), 'w').write(' '.join(sorted(os.environ)))",
                      "sys.exit(f.get('acq', 0))", ""])
TAU = NL.join(TETE + ["s = a[a.index('--sortie') + 1]", "os.makedirs(s, exist_ok=True)",
                      "g = os.environ['PYTHONHASHSEED'] if f.get('graine') else ''",
                      "for n in ('calib_actifs.txt', 'fragment_analyse.json'):",
                      "    open(os.path.join(s, n), 'w').write(n + g + ' '.join(sorted(os.environ)) + ' bruts='"
                      " + a[a.index('--bruts') + 1])",
                      "sys.exit(f.get('tau', 0))", ""])


class TestLancer(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.mkdtemp(prefix="ca_lan_")
        self.addCleanup(shutil.rmtree, self.t, True)
        self.lot, self.b, self.s, self.x = (os.path.join(self.t, n) for n in ("lot", "b", "s", "x"))
        os.makedirs(self.lot)
        shutil.copy(os.path.join(ICI, "lancer.sh"), self.lot)
        self.ecrire()

    def ecrire(self, faux=None):
        for nom, texte in (("acquerir.py", ACQ), ("tau.py", TAU),
                           ("parametres.json", json.dumps({"passes": {"A": 0, "B": 1}, "faux": faux or {}}))):
            with open(os.path.join(self.lot, nom), "w", encoding="utf-8") as f:
                f.write(texte)
        sommes = ""
        for n in ("acquerir.py", "lancer.sh", "parametres.json", "tau.py"):
            with open(os.path.join(self.lot, n), "rb") as f:
                sommes += f"{hashlib.sha256(f.read()).hexdigest()}  {n}" + NL
        with open(os.path.join(self.lot, "SHA256SUMS"), "w", encoding="utf-8") as f:
            f.write(sommes)
        self.epingle = hashlib.sha256(sommes.encode()).hexdigest()

    def lancer(self, *args, **env):
        e = {k: v for k, v in os.environ.items() if k != "SHOGEN_S2_CAMPAGNE_CONTROL"} | env
        a = list(args) or [self.b, self.s, self.x, self.epingle]
        return subprocess.run(["bash", os.path.join(self.lot, "lancer.sh"), *a], capture_output=True, text=True, env=e)

    def assertRefus(self, r, code, refus):
        self.assertEqual((r.returncode, r.stderr.split(" : ")[0]), (code, "REFUS " + refus), r.stderr)

    def test_succes(self):
        """Code 0 : sortie = sorties de A, manifeste et SHA256SUMS ; environnement des scripts réduit (aucune variable
        hors de la liste fermée ; mandataire à l'étape réseau seule ; PYTHONHASHSEED au calcul). Mutations : env -i
        retiré ; mandataire passé au calcul ; mandataire retiré de l'étape réseau."""
        r = self.lancer(HTTPS_PROXY="http://127.0.0.1:9", AUTRE="x")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(sorted(os.listdir(self.s)), ["SHA256SUMS", "calib_actifs.txt", "fragment_analyse.json",
                                                      "manifeste.tsv"])
        with open(os.path.join(self.s, "calib_actifs.txt"), encoding="utf-8") as f:
            env = f.read().split(" ")
        with open(os.path.join(self.s, "manifeste.tsv"), encoding="utf-8") as f:
            reseau = f.read().split(" ")
        self.assertEqual((env[0], "AUTRE" in env, "HTTPS_PROXY" in env, "PYTHONHASHSEED" in env, "TMPDIR" in env,
                          env[-1]), ("calib_actifs.txtLC_ALL", False, False, True, True, "bruts=" + self.b))
        self.assertEqual(("AUTRE" in reseau, "HTTPS_PROXY" in reseau, "PYTHONHASHSEED" in reseau), (False, True, False))

    def test_epingle(self):
        """T-CA-LAN-1 : sha256 en argument faux ; fichier du lot altéré (sha256sum -c) ; entrée hors de SHA256SUMS :
        CA/epingle, code 3, aucun script lancé. Mutations M-CA-24 : chacun des trois contrôles retiré."""
        self.assertRefus(self.lancer(self.b, self.s, self.x, "0" * 64), 3, "CA/epingle")
        with open(os.path.join(self.lot, "intrus.py"), "w", encoding="utf-8") as f:
            f.write("#")
        self.assertRefus(self.lancer(), 3, "CA/epingle")
        os.remove(f.name)
        with open(os.path.join(self.lot, "tau.py"), "a", encoding="utf-8") as f:
            f.write("#")
        self.assertRefus(self.lancer(), 3, "CA/epingle")
        self.assertFalse(os.path.exists(self.b))

    def test_sortie_variable_usage(self):
        """T-CA-LAN-2 : sortie ou travail non vide, CA/sortie (3) ; T-CA-LAN-3 : variable posée (valeur fictive, ce seul
        sous-processus), CA/variable (3) ; T-CA-LAN-6 : trois arguments, CA/usage (2). Mutations M-CA-25, M-CA-26,
        M-CA-29 : contrôle retiré."""
        os.makedirs(self.s)
        with open(os.path.join(self.s, "x"), "w", encoding="utf-8") as f:
            f.write("x")
        self.assertRefus(self.lancer(), 3, "CA/sortie")
        shutil.move(self.s, self.x)                         # travail non vide : même refus
        self.assertRefus(self.lancer(), 3, "CA/sortie")
        shutil.rmtree(self.x)
        self.assertRefus(self.lancer(SHOGEN_S2_CAMPAGNE_CONTROL="fictive"), 3, "CA/variable")
        self.assertRefus(self.lancer(self.b, self.s, self.x), 2, "CA/usage")

    def test_acquisition_et_identite(self):
        """T-CA-LAN-4 : acquisition en code 4 : CA/acquisition, code 4, aucune passe ; T-CA-LAN-5 : sorties dépendant de
        la graine : CA/identite, code 5, sortie vide ; calcul en code 1 : code 5. Mutations M-CA-27, M-CA-28."""
        for faux, code, refus in (({"acq": 4}, 4, "CA/acquisition"), ({"graine": True}, 5, "CA/identite")):
            self.ecrire(faux)
            self.assertRefus(self.lancer(), code, refus)
            self.assertEqual((os.path.exists(os.path.join(self.x, "A")), os.path.exists(self.s)), (code == 5, False))
            shutil.rmtree(self.x)
        self.ecrire({"tau": 1})
        self.assertEqual(self.lancer().returncode, 5)


if __name__ == "__main__":
    unittest.main()
