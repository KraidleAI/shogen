"""Cas du modèle de chaîne gabarits/chaine.sh (lot GARDE-FOUS-ORCH, GF-9 ; erreurs E3, E8, LA-N04, LA-N05), lancé par
bash dans un dépôt git temporaire isolé (tests/aide_garde.py). La fonction verif, propre à chaque lot, est remplacée
par un faux réglé par ROUGE (id dont la vérification est rouge) ; le reste du modèle tourne tel quel.
Relecture G2, C-1 : VerifDuModele lance la fonction verif telle qu'écrite (cargo et portes factices) ; C-15 : cargo
à la cible par défaut même si l'environnement pose CARGO_TARGET_DIR.
Contre-contrôle : R-6 (étape écrite « - run: python3 … »).
Phase 2, L-4 : le modèle tourne avec une copie des outils dont gabarits/chaine.sh porte le faux (fonction verif
versionnée) ; une chaîne dont la verif diffère de la version des outils ne commet rien."""
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import avant_acte

from tests import aide_garde as ag

ICI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NL = chr(10)
FAUX = 'verif() { [ "$1" != "${ROUGE:-}" ]; }' + NL
UNSHARE = NL.join(["#!/bin/sh", '[ "$1" = -n ] || exit 9', "shift", "export ISOLE=1", 'exec "$@"', ""])  # forge sans droits


class Chaine(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.tmp = t.name
        self.d, self.env = ag.depot(self.tmp, {"a.md": "un" + NL})
        with open(os.path.join(ICI, "gabarits", "chaine.sh"), encoding="utf-8") as f:
            modele = f.read()
        self.chaine = os.path.join(self.tmp, "chaine.sh")
        faux = modele[:modele.index("verif() {")] + FAUX + modele[modele.index("# --- fin"):]
        self.outils = os.path.join(self.tmp, "outils", "scripts", "controle")
        shutil.copytree(ICI, self.outils, ignore=shutil.ignore_patterns("tests", "sorties-fm11", "__pycache__"))
        os.makedirs(os.path.join(self.tmp, "outils", "enforcement"))
        shutil.copy(os.path.join(os.path.dirname(os.path.dirname(ICI)), "enforcement", "docs-sha256sums.py"),
                    os.path.join(self.tmp, "outils", "enforcement"))
        ag.ecrire(self.outils, {"gabarits/chaine.sh": faux})
        ag.ecrire(self.tmp, {"chaine.sh": faux, "ADJ.md": "Contre-contrôle CONFORME en deux passes." + NL})
        self.adj = os.path.join(self.tmp, "ADJ.md")
        copie = os.path.join(self.tmp, "copie")
        shutil.copytree(self.d, copie)
        plan = []
        for i, nom in ((1, "b.md"), (2, "c.md")):
            ag.ecrire(copie, {nom: nom + NL})
            ag.git(copie, self.env, "add", "-A")
            ag.ecrire(self.tmp, {f"d{i}.diff": ag.git(copie, self.env, "diff", "--cached", "HEAD", "--", nom)})
            plan.append(f"X-{i}|{self.tmp}/d{i}.diff|{self.tmp}/m{i}.txt|{self.adj}")
        ag.ecrire(self.tmp, {"plan": NL.join(plan) + NL + NL, "cc.md": "GROUPES : aucun" + NL})
        self.messages()

    def messages(self):
        """Messages écrits depuis la source du moment : Source-Sha et Diff-Id."""
        with open(self.adj, "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
        for i in (1, 2):
            ag.ecrire(self.tmp, {f"m{i}.txt": NL.join([f"X-{i} : CONFORME en deux passes", "", "Source-Sha: " + h,
                                                       f"Diff-Id: X-{i}", ""])})

    def lancer(self, **variables):
        """ROUGE, lue par le faux verif, posée vide sauf demande : jamais héritée (relecture G2 du lot ISOLE-ENV, C-3)."""
        env = dict(self.env, DEPOT=self.d, PLAN=os.path.join(self.tmp, "plan"), OUTILS=self.outils,
                   PYTHON=sys.executable, CC=os.path.join(self.tmp, "cc.md"), ROUGE="")
        env.update(variables)
        p = subprocess.run(["bash", self.chaine], env=env, capture_output=True, text=True, timeout=300)
        self.erreur, self.sortie = p.stderr, p.stdout
        return p.returncode, re.findall("(?m)^Diff-Id: (.+)$", ag.git(self.d, self.env, "log", "--format=%B"))

    def test_verte_puis_reprise(self):
        """Deux pas, vérification verte : deux commits, chacun avec son Diff-Id ; relance : aucun commit de plus."""
        self.assertEqual(self.lancer(), (0, ["X-2", "X-1"]))
        self.assertEqual(self.lancer(), (0, ["X-2", "X-1"]))

    def test_rouge_au_second_pas(self):
        """LA-N05 : vérification rouge au deuxième pas : un commit, arrêt nommé, et aucun sceau pour l'index du pas
        rouge (le sceau suit la vérification, jamais l'inverse)."""
        code, ids = self.lancer(ROUGE="X-2")
        self.assertEqual((code != 0, ids, "vérification rouge avant X-2" in self.erreur), (True, ["X-1"], True))
        with mock.patch.dict(os.environ, self.env, clear=True):
            sceau = os.path.join(self.d, ".git", "shogen-garde", "sceaux", avant_acte.cle(self.d))
        self.assertFalse(os.path.exists(sceau))

    def test_e8_message_perime(self):
        """E8 : source retouchée après l'écriture des messages (clôture) : aucun commit ; le pas arrêté retiré de
        l'index, messages réécrits depuis la source finale : admis."""
        ag.ecrire(self.tmp, {"ADJ.md": "Contre-contrôle CONFORME en deux passes. Clôture." + NL})
        code, ids = self.lancer()
        self.assertEqual((code != 0, ids, "refus du commit X-1" in self.erreur), (True, [], True))
        ag.git(self.d, self.env, "rm", "-q", "-f", "b.md")
        self.messages()
        self.assertEqual(self.lancer(), (0, ["X-2", "X-1"]))

    def test_e11_groupe(self):
        """E11 : le contre-contrôle groupe d1 et d2 ; le plan les commet en deux pas : arrêt avant tout pas."""
        ag.ecrire(self.tmp, {"cc.md": "GROUPES : d1+d2" + NL})
        code, ids = self.lancer()
        self.assertEqual((code != 0, ids), (True, []))

    def test_e25_lancement_lie(self):
        """E25 : durée estimée au-delà de 100 min (2 pas mesurés à 60 min) : lancement lié refusé avant tout pas ;
        DETACHE=1 (lancement détaché) : admis."""
        code, ids = self.lancer(DUREE_PAS="60")
        self.assertEqual((code != 0, ids), (True, []))
        self.assertEqual(self.lancer(DUREE_PAS="60", DETACHE="1"), (0, ["X-2", "X-1"]))

    def test_disque_et_arbre(self):
        """E4 : disque sous le seuil demandé : arrêt avant tout pas ; arbre non propre : arrêt avant d'appliquer."""
        code, ids = self.lancer(DISQUE_MIN_GO="1000000")
        self.assertEqual((code != 0, ids), (True, []))
        ag.ecrire(self.d, {"sale.md": "x"})
        code, ids = self.lancer()
        etat = ag.git(self.d, self.env, "status", "--porcelain")
        self.assertEqual((code != 0, ids, etat), (True, [], "?? sale.md" + NL))

    def test_ln1_disque_a_chaque_pas(self):
        """LN-1 (SHOGEN-GARDE-DISQUE-CHAINE-1) : disque passé sous le seuil en route (au second contrôle : PYTHON
        enveloppé qui serre --min-go à ce contrôle-là, outil réel) : ligne ROUGE disque avant X-2, X-1 seul commis,
        rien d'appliqué pour X-2 (arbre propre)."""
        compte = os.path.join(self.tmp, "compte")
        ag.ecrire(self.tmp, {"py.sh": NL.join([
            "#!/bin/sh", 'case " $* " in *" disque "*)', '  n=$(($(cat "$COMPTE" 2>/dev/null || echo 0) + 1))',
            '  echo "$n" > "$COMPTE"', '  [ "$n" -lt 2 ] || exec "$VRAI" "$@" --min-go 1000000 ;;', "esac",
            'exec "$VRAI" "$@"', ""])})
        os.chmod(os.path.join(self.tmp, "py.sh"), 0o755)
        code, ids = self.lancer(PYTHON=os.path.join(self.tmp, "py.sh"), VRAI=sys.executable, COMPTE=compte)
        etat = ag.git(self.d, self.env, "status", "--porcelain")
        self.assertEqual((code != 0, ids, "ROUGE disque avant X-2" in self.erreur, etat), (True, ["X-1"], True, ""))

    def test_l4_verif_versionnee(self):
        """L-4 (SHOGEN-GARDE-VERIF-VERSIONNEE-1) : le sceau porte le sha256 de declare -f verif de la chaîne qui a
        tourné ; chaîne dont la fonction verif n'est pas celle de gabarits/chaine.sh des outils (vérification
        affaiblie, toujours verte) : refus du commit, rien de commis ; chaîne à la verif versionnée : commise."""
        with open(self.chaine, encoding="utf-8") as f:
            texte = f.read()
        ag.ecrire(self.tmp, {"chaine.sh": texte.replace(FAUX, "verif() { true; }" + NL)})
        code, ids = self.lancer()
        self.assertEqual((code != 0, ids, "refus du commit X-1" in self.erreur), (True, [], True))
        ag.git(self.d, self.env, "rm", "-q", "-f", "b.md")
        ag.ecrire(self.tmp, {"chaine.sh": texte})
        self.assertEqual(self.lancer(), (0, ["X-2", "X-1"]))
        p = subprocess.run(["bash", "-c", FAUX + "declare -f verif"], capture_output=True, text=True, timeout=60)
        with mock.patch.dict(os.environ, self.env, clear=True):
            sceaux = os.path.join(self.d, ".git", "shogen-garde", "sceaux")
            lignes = set()
            for s in os.listdir(sceaux):
                with open(os.path.join(sceaux, s), encoding="utf-8") as f:
                    lignes |= set(f)
        self.assertIn("verif " + hashlib.sha256(p.stdout.encode()).hexdigest() + NL, lignes)

    def test_modele(self):
        """Le modèle se lit en bash ; sa vérification porte xtask, cargo test de xtask (règle I-1) et le lint R-1."""
        chemin = os.path.join(ICI, "gabarits", "chaine.sh")
        self.assertEqual(subprocess.run(["bash", "-n", chemin], capture_output=True, timeout=60).returncode, 0)
        with open(chemin, encoding="utf-8") as f:
            modele = f.read()
        for x in ("cargo --locked xtask verify", "cargo --locked test -p xtask", "lint-model-pinning.sh", "timeout",
                  "unshare -n bash", "-u HTTPS_PROXY", "-u all_proxy", "0x8914"):      # CHAINE-ORCH-MODELE
            self.assertIn(x, modele[modele.index("verif() {"):modele.index("# --- fin")])


class VerifDuModele(unittest.TestCase):
    PORTE = NL.join(["import os, sys", "if sys.argv[1] == 'mange':", "    sys.stdin.read()",
                     "isole = os.environ.get('ISOLE') == '1' or sys.argv[1] in ('cas', 'lint')",      # CHAINE-ORCH-MODELE
                     "sys.exit(1 if os.environ.get('ROUGE_A') == sys.argv[1] or 'HTTPS_PROXY' in os.environ or not isole "
                     "else 0)", ""])
    CARGO = NL.join(["#!/bin/sh", '[ -z "${CARGO_TARGET_DIR}${CARGO_BUILD_TARGET_DIR}" ] || exit 1', 'case "$*" in',
                     '  *"xtask verify"*) [ "$ROUGE_A" = xtask ] ||',
                     '    echo "=== VERDICT GLOBAL : VERT ===" ;;', '  *) [ "$ROUGE_A" != cargo ] ;;', "esac", ""])

    def fichiers(self):
        lancer = "exec python3 -B enforcement/porte.py "
        portes = "".join(f"        run: python3 -B enforcement/porte.py {x}" + NL for x in ("mange", "porte"))
        portes += "      - run: python3 -B enforcement/porte.py tiret" + NL      # forme en tiret (R-6)
        return {"a.md": "un" + NL, "enforcement/porte.py": self.PORTE, ".github/workflows/gates.yml": portes,
                "enforcement/tests/run-fixtures-model-pinning.sh": lancer + "cas" + NL,
                "enforcement/lint-model-pinning.sh": lancer + "lint" + NL}

    def test_c1_verif_reelle(self):
        """C-1 : appelée par verif && sceller, la fonction verif tourne hors de set -e ; un pas rouge, quel qu'il soit
        (verdict de xtask, cargo test, ligne de gates.yml, même après une ligne qui lit l'entrée standard, cas du lint,
        lint), arrête la chaîne avant le sceau et le commit (le pas arrêté est retiré de l'index avant la relance) ;
        tout vert : un commit. C-15 (E5, règle I-1) : CARGO_TARGET_DIR posé dans l'environnement ne déplace pas la
        cible de cargo (le cargo factice échoue s'il la voit). R-6 : étape de gates.yml écrite « - run: ».
        CHAINE-ORCH-MODELE : une porte Python lancée hors de unshare -n, ou qui voit HTTPS_PROXY, échoue."""
        with tempfile.TemporaryDirectory() as t:
            d, env = ag.depot(t, self.fichiers())
            ag.ecrire(t, {"bin/cargo": self.CARGO, "ADJ.md": "CONFORME en deux passes." + NL,
                          "cc.md": "GROUPES : aucun" + NL, "bin/unshare": UNSHARE})
            for x in ("cargo", "unshare"):
                os.chmod(os.path.join(t, "bin", x), 0o755)
            copie = os.path.join(t, "copie")
            shutil.copytree(d, copie)
            ag.ecrire(copie, {"b.md": "b" + NL})
            ag.git(copie, env, "add", "-A")
            with open(os.path.join(t, "ADJ.md"), "rb") as f:
                h = hashlib.sha256(f.read()).hexdigest()
            message = NL.join(["X-1 : CONFORME en deux passes", "", "Source-Sha: " + h, "Diff-Id: X-1", ""])
            ag.ecrire(t, {"d1.diff": ag.git(copie, env, "diff", "--cached", "HEAD"), "m1.txt": message,
                          "plan": f"X-1|{t}/d1.diff|{t}/m1.txt|{t}/ADJ.md" + NL})
            chemin = os.path.join(t, "bin") + os.pathsep + env["PATH"]
            for rouge in ("xtask", "cargo", "porte", "tiret", "cas", "lint", ""):
                variables = dict(env, DEPOT=d, PLAN=os.path.join(t, "plan"), CC=os.path.join(t, "cc.md"), OUTILS=ICI,
                                 PYTHON=sys.executable, ROUGE_A=rouge, PATH=chemin,
                                 CARGO_TARGET_DIR=os.path.join(t, "ailleurs"), HTTPS_PROXY="http://127.0.0.1:9")
                p = subprocess.run(["bash", os.path.join(ICI, "gabarits", "chaine.sh")], env=variables,
                                   capture_output=True, text=True, timeout=300)
                ids = re.findall("(?m)^Diff-Id: (.+)$", ag.git(d, env, "log", "--format=%B"))
                attendu = (True, [], True) if rouge else (False, ["X-1"], False)
                self.assertEqual((p.returncode != 0, ids, "vérification rouge avant X-1" in p.stderr), attendu, rouge)
                if rouge:
                    ag.git(d, env, "rm", "-q", "-f", "b.md")


class ChaineModele(Chaine):
    """SHOGEN-GARDE-CHAINE-ORCH-MODELE-1 : gabarits/chaine-modele.sh copié tel quel ; sa verif est tirée par source
    du modèle des outils (le faux de Chaine) ; chaine --blanc avant tout pas ; trap ERR (E36)."""
    def setUp(self):
        super().setUp()
        with open(os.path.join(ICI, "gabarits", "chaine-modele.sh"), encoding="utf-8") as f:
            ag.ecrire(self.tmp, {"chaine.sh": f.read()})
        os.makedirs(os.path.join(self.tmp, "outils", ".github", "workflows"))
        shutil.copy(os.path.join(os.path.dirname(os.path.dirname(ICI)), ".github", "workflows", "gates.yml"),
                    os.path.join(self.tmp, "outils", ".github", "workflows"))
        ag.ecrire(self.d, {"biblio/INDEX.md": "# index" + NL})
        ag.git(self.d, self.env, "add", "-A")
        ag.git(self.d, self.env, "commit", "-q", "-m", "biblio")

    def test_modele_a_blanc_avant_tout_pas(self):
        """E30 : second diff sans saut de ligne final : refus K5 avant le premier pas, rien de commis (le modèle
        d'avant commettait X-1 puis s'arrêtait) ; E36 : l'arrêt écrit sa ligne ROUGE ; diffs sains : deux commits."""
        with open(os.path.join(self.tmp, "d2.diff"), encoding="utf-8") as f:
            sain = f.read()
        ag.ecrire(self.tmp, {"d2.diff": sain[:-1]})
        code, ids = self.lancer()
        self.assertEqual((code != 0, ids, "REFUS K5 " in self.erreur + self.sortie, "ROUGE l." in self.erreur),
                         (True, [], True, True))
        ag.ecrire(self.tmp, {"d2.diff": sain})
        self.assertEqual(self.lancer(), (0, ["X-2", "X-1"]))

    def test_l4_verif_versionnee(self):
        """K7 : copie du modèle qui écrit sa propre verif (toujours verte) : refus avant tout pas, rien de commis."""
        with open(self.chaine, encoding="utf-8") as f:
            texte = f.read().replace("acte() {", "verif() {" + NL + "  true" + NL + "}" + NL + "acte() {")
        ag.ecrire(self.tmp, {"chaine.sh": texte})
        code, ids = self.lancer()
        self.assertEqual((code != 0, ids, "REFUS K7 " in self.sortie), (True, [], True))

    def test_modele(self):
        """Le modèle se lit en bash, n'écrit aucune verif, la tire par source du modèle des outils et porte set -E,
        trap ERR et chaine --blanc avant la boucle."""
        chemin = os.path.join(ICI, "gabarits", "chaine-modele.sh")
        self.assertEqual(subprocess.run(["bash", "-n", chemin], capture_output=True, timeout=60).returncode, 0)
        with open(chemin, encoding="utf-8") as f:
            modele = f.read()
        self.assertNotRegex(modele, "(?m)^ *(function +)?verif *[(][)]")
        for x in ("set -Eeuo pipefail", "' ERR", "fin de verif/p' " + chr(34) + "$OUTILS/gabarits/chaine.sh", "--blanc"):
            self.assertIn(x, modele[:modele.index("while IFS")])
