"""Cas de scripts/controle/mutants.py (lot DETTES-T7, SHOGEN-S2BIS-MUT-COMMANDE-1) : copie jetable, job de son
gates.yml, mutants d'une fixture ; attendus écrits à la main ; variable scellée jamais posée ; bash et ps (POSIX)."""
import contextlib
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import unittest

OUTIL = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "mutants.py")
NL, CIBLE = chr(10), chr(10).join(["import sys", "sys.exit(0)", ""])
GATES = ["jobs:", "  essai:", "    steps:",                 # checkout du gabarit K, écrit à la main (réserve R-1)
         "      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # tag v7.0.1", "        with:",
         "          persist-credentials: false", "      - name: a",
         "        shell: bash", "        run: echo premier", "      - name: b", "        shell: bash", "        run: |",
         "          python3 -B cible.py", "          echo fin"]


def lancer(d: str, mutants: list, *plus, gates=GATES, job="essai") -> tuple:
    """Copie jetable sous d (gates.yml, cible.py), campagne des mutants : (code, lignes JSON, stderr, copie)."""
    c = os.path.join(d, "copie")
    os.makedirs(os.path.join(c, ".github", "workflows"), exist_ok=True)
    for chemin, texte in ((os.path.join(c, ".github", "workflows", "gates.yml"), NL.join(gates) + NL),
                          (os.path.join(c, "cible.py"), CIBLE), (os.path.join(d, "m.json"), json.dumps(mutants))):
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(texte)
    env = {k: v for k, v in os.environ.items() if k != "SHOGEN_S2_CAMPAGNE_CONTROL"}
    p = subprocess.run([sys.executable, "-B", OUTIL, c, job, os.path.join(d, "m.json"), "--sortie", os.path.join(
        d, "s"), *plus], capture_output=True, text=True, timeout=120, env=env)
    return p.returncode, [json.loads(x) for x in p.stdout.splitlines()], p.stderr, c


def vit(chemin: str) -> bool:
    """Processus dont le numéro est écrit dans `chemin` encore vivant (zombie : mort ; fichier absent : False ; ps
    POSIX) ; réserve R-2."""
    try:
        with open(chemin, encoding="utf-8") as f:
            pid = f.read()
    except OSError:
        return False
    etat = subprocess.run(["ps", "-o", "stat=", "-p", pid], capture_output=True, text=True).stdout.strip()
    return bool(etat) and not etat.startswith("Z")


def tuer(chemin: str) -> None:
    """Descendant détaché du cas M7 (numéro écrit dans `chemin`) arrêté s'il vit encore (G2 du lot DETTES-T7)."""
    with contextlib.suppress(OSError, ValueError):
        with open(chemin, encoding="utf-8") as f:
            os.kill(int(f.read()), signal.SIGKILL)


class Mutants(unittest.TestCase):
    def test_classement_par_la_commande_du_job(self):
        """Témoin vivant ; tué ; vivant ; FATAL : borne (petit-enfant arrêté avec le groupe, marque jamais posée),
        sortie 3, texte avant absent ; --tue 3 : tué ; copie rendue ; diff et sortie versés ; relevé ps vide.
        G2 du lot DETTES-T7 (C-1) : à la borne, petit-enfant parti dans sa propre session, comme la suite que lance le
        vérificateur (M6), arrêté avec son groupe ; descendant détaché qui garde le tuyau (M7) attendu RELIQUAT s au
        plus ; mutant de gates.yml (M8) classé par la ligne qu'il écrit, étapes relues sur la copie mutée.
        Réserve R-2 du contre-contrôle (Linux, moissonneur) : enfant d'une autre session resté après une sortie
        normale (M9) et descendant détaché, parent sorti, à la borne (M10) : arrêtés avant la fin de la campagne."""
        p = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, p, True)
        for n in ("pid", "pid9", "pid10"):
            self.addCleanup(tuer, os.path.join(p, n))
        with tempfile.TemporaryDirectory() as d:
            marque, marque2 = os.path.join(d, "marque"), os.path.join(d, "marque2")
            enfant = repr(f"import pathlib, time; time.sleep(3); pathlib.Path({marque!r}).touch()")
            dort = f"import subprocess, time; subprocess.Popen([sys.executable, '-c', {enfant}]); time.sleep(60)"
            seul = repr(f"import pathlib, time; time.sleep(3); pathlib.Path({marque2!r}).touch()")
            session = (f"import subprocess, time; subprocess.Popen([sys.executable, '-c', {seul}], "
                       "start_new_session=True); time.sleep(60)")
            detache = NL.join(["import os, time", "if os.fork() == 0:", "    os.setsid()", "    if os.fork() == 0:",
                               f"        open({os.path.join(p, 'pid')!r}, 'w').write(str(os.getpid()))",
                               "        time.sleep(90)", "    os._exit(0)", "sys.exit(0)"])
            dort30 = ("subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(30)'], "
                      "stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL{})")
            p9, p10 = os.path.join(p, "pid9"), os.path.join(p, "pid10")
            reste = NL.join(["import subprocess", "q = " + dort30.format(", start_new_session=True"),
                             f"with open({p9!r}, 'w') as w:", "    w.write(str(q.pid))", "sys.exit(0)"])
            orphelin = NL.join(["import os, subprocess, time", "f = os.fork()", "if f == 0:", "    os.setsid()",
                                "    q = " + dort30.format(""), f"    with open({p10!r}, 'w') as w:",
                                "        w.write(str(q.pid))", "    os._exit(0)", "os.waitpid(f, 0)", "time.sleep(60)"])
            m = [{"id": "M1", "fichier": "cible.py", "avant": "sys.exit(0)", "apres": "sys.exit(1)"},
                 {"id": "M2", "fichier": "cible.py", "avant": "import sys", "apres": "import sys  # neutre"},
                 {"id": "M3", "fichier": "cible.py", "avant": "sys.exit(0)", "apres": dort},
                 {"id": "M4", "fichier": "cible.py", "avant": "sys.exit(0)", "apres": "sys.exit(3)"},
                 {"id": "M5", "fichier": "cible.py", "avant": "sys.exit(9)", "apres": "sys.exit(1)"},
                 {"id": "M6", "fichier": "cible.py", "avant": "sys.exit(0)", "apres": session},
                 {"id": "M7", "fichier": "cible.py", "avant": "sys.exit(0)", "apres": detache},
                 {"id": "M8", "fichier": ".github/workflows/gates.yml", "avant": "run: echo premier",
                  "apres": "run: exit 1"},
                 {"id": "M9", "fichier": "cible.py", "avant": "sys.exit(0)", "apres": reste},
                 {"id": "M10", "fichier": "cible.py", "avant": "sys.exit(0)", "apres": orphelin}]
            debut = time.monotonic()
            code, lignes, err, c = lancer(d, m, "--borne", "2")
            self.assertEqual((code, time.monotonic() - debut < 40, [(x["id"], x["classement"], len(x["etapes"])) for x
                                                                     in lignes]), (0, True, [
                ("témoin", "vivant", 2), ("M1", "tué", 2), ("M2", "vivant", 2), ("M3", "FATAL", 2), ("M4", "FATAL", 2),
                ("M5", "FATAL", 0), ("M6", "FATAL", 2), ("M7", "FATAL", 2), ("M8", "tué", 1), ("M9", "vivant", 2),
                ("M10", "FATAL", 2)]), err)
            if sys.platform.startswith("linux"):        # R-2 : moissonneur ; ailleurs, limite écrite au README
                self.assertEqual([(os.path.exists(n), vit(n)) for n in (p9, p10)], [(True, False), (True, False)],
                                 "orphelin d'une étape vivant après la campagne")
            self.assertEqual([x["etapes"][1][0] for x in lignes[:5]], [0, 1, 0, None, 3])
            for nom, attendu in (("M1.diff", NL.join(["-sys.exit(0)", "+sys.exit(1)", ""])), ("M2.out", NL.join([
                    "premier", "fin", ""]))):
                with open(os.path.join(d, "s", nom), encoding="utf-8") as f:
                    self.assertIn(attendu, f.read())
            with open(os.path.join(c, "cible.py"), encoding="utf-8") as f:
                self.assertEqual((f.read(), "aucun processus" in err), (CIBLE, True))
            time.sleep(max(0.0, debut + 6 - time.monotonic()))
            self.assertFalse(os.path.exists(marque), "petit-enfant vivant après la borne")
            self.assertFalse(os.path.exists(marque2), "petit-enfant d'une autre session vivant après la borne")
            code, lignes, err, c = lancer(d, m[3:4], "--tue", "1", "--tue", "3",       # FETCH admis (R-1)
                                          gates=GATES[:6] + ["          fetch-depth: 0"] + GATES[6:])
            self.assertEqual((code, lignes[1]["classement"]), (0, "tué"), err)

    def test_refus_avant_tout_mutant(self):
        """Témoin non vivant, étape non admise (if:), job absent, première étape autre que le checkout (G2 du lot
        DETTES-T7, C-1) : sortie 3, refus nommé, aucun mutant lancé. Réserve R-1 du contre-contrôle : première étape
        non admise autre que le checkout épinglé (étape `if:` qui échouerait, autre action, `with:` autre)."""
        m = [{"id": "M1", "fichier": "cible.py", "avant": "sys.exit(0)", "apres": "sys.exit(1)"}]
        for nom, gates, job, motif in (("rouge", GATES[:-2] + ["          exit 1"], "essai", "témoin non vivant"),
                                       ("if", GATES[:7] + ["        if: false"] + GATES[7:], "essai", "job essai : "),
                                       ("absent", GATES, "x", "job x : "),
                                       ("tete", GATES[:3] + GATES[6:], "essai", "job essai : "),
                                       ("tete-if", GATES[:3] + ["      - name: avant", "        if: always()",
                                                                "        shell: bash", "        run: exit 1"]
                                        + GATES[6:], "essai", "job essai : "),
                                       ("tete-action", GATES[:3] + ["      - uses: actions/setup-python@0"] + GATES[6:],
                                        "essai", "job essai : "),
                                       ("tete-with", GATES[:6] + ["          path: sous"] + GATES[6:], "essai",
                                        "job essai : ")):
            with self.subTest(cas=nom), tempfile.TemporaryDirectory() as d:
                code, lignes, err, _c = lancer(d, m, gates=gates, job=job)
                self.assertEqual((code, [x["id"] for x in lignes if x["id"] != "témoin"], f"mutants : erreur : {motif}"
                                  in err), (3, [], True), err)
