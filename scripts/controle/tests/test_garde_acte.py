"""Cas du crochet GARDE-FAITS du dépôt (.claude/hooks/garde_faits.py), lancé tel quel sur des journaux synthétiques
(nom en .txt), lot GARDE-FOUS-ORCH phase 2. LN-6 (SHOGEN-GARDE-CROCHET-ACTE-1) : l'acte est jugé, non le texte ; les
deux faux refus de la sonde du contre-contrôle (R3 puis R5 sur une commande qui écrit un journal synthétique par un
heredoc python portant un commit) passent ; les vrais refus restent ; R5 lit le fichier de git commit -F.
R7 (E18, E28) : sleep d'avant-plan ; pkill -f et pgrep -f à motif non ancré."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
GARDE = os.path.join(RACINE, ".claude", "hooks", "garde_faits.py")
NL = chr(10)
FICTIF = "9f8e7d6"          # identifiant fictif d'un journal synthétique, jamais affiché sauf où le cas le dit
SONDE = NL.join(["python3 - <<'EOF'", "import json", "e = {'type': 'assistant', 'message': {'content': [{'type':",
                 " 'tool_use', 'name': 'Bash', 'input': {'command': 'git commit -q -F m'}}]}}",
                 "open('journal-sonde.txt', 'w').write(json.dumps(e) + ' " + FICTIF + "')", "EOF"])


def appel(cmd, nom="Bash", resultat=""):
    """Deux entrées de journal : l'appel d'outil et son résultat affiché."""
    a = {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": nom, "input": {"command": cmd}}]}}
    return [a, {"type": "user", "message": {"content": [{"type": "tool_result", "content": resultat}]}}]


class Crochet(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.t = t.name
        self.notes = os.path.join(self.t, "NOTES.md")
        with open(self.notes, "w", encoding="utf-8") as f:
            f.write("note" + NL)

    def lancer(self, avant, cmd, garde=GARDE, entree=None):
        """Sortie et stderr du crochet sur l'appel Bash cmd après les entrées avant."""
        j = os.path.join(self.t, "journal.txt")
        with open(j, "w", encoding="utf-8") as f:
            f.writelines(json.dumps(e) + NL for e in avant)
        e = {"hook_event_name": "PreToolUse", "transcript_path": j, "cwd": self.t, "tool_name": "Bash",
             "tool_input": {"command": cmd}, **(entree or {})}
        p = subprocess.run([sys.executable, "-I", garde], input=json.dumps(e), capture_output=True, text=True,
                           timeout=60)
        return p.returncode, p.stderr

    def refus(self, avant, cmd, regle, **k):
        code, err = self.lancer(avant, cmd, **k)
        self.assertEqual((code, regle in err), (2, True), (cmd, err))

    def permis(self, avant, cmd, **k):
        code, err = self.lancer(avant, cmd, **k)
        self.assertEqual((code, err), (0, ""), cmd)


class ActeLu(Crochet):
    def test_ln6_sonde_du_contre_controle(self):
        """Cas réel (contre-contrôle, E-3 ; vécu de nouveau par le générateur de la phase 2) : la commande écrit un
        journal synthétique neuf par un heredoc python dont le texte porte un commit et un identifiant fictif ; ni
        commit ni écriture d'un fichier existant : permise sans lecture (refus R3), puis après git status (refus R5)."""
        self.permis(appel("ls"), SONDE)
        self.permis(appel("git status --short"), SONDE)

    def test_ln6_controle_d_une_poussee(self):
        """Point 3 de shogen-avant-pousser : contrôler une poussée (son texte en argument) n'est pas pousser."""
        controle = 'python3 -I -B scripts/controle/avant_acte.py pousser --acte "git push origin --delete b"'
        self.permis(appel("ls"), controle)
        self.permis(appel("ls"), 'echo "rm -rf clone ; git commit -m x" > neuf.txt')
        self.permis(appel("ls"), "cat > neuf2.txt <<'FIN'" + NL + "git push origin main" + NL + "FIN")

    def test_vrais_refus_restent(self):
        """Commit et poussée réels, sous toutes leurs formes lues (liste, bash -c, substitution, options globales),
        sans lecture : refus R3 ; un commit dans un heredoc donné à bash reste un commit."""
        for cmd in ("git commit -m x", "A=1 git commit -m x", "cd d && git -C . commit -qm x",
                    "bash -o pipefail -c 'git push origin b'", 'echo "$(git commit -m x)"',
                    "timeout 60 env A=1 git push", "bash <<'FIN'" + NL + "git push" + NL + "FIN", "eval 'git push'"):
            self.refus(appel("ls"), cmd, "R3")

    def test_r5_lit_le_message_et_le_fichier_de_f(self):
        """R5 sur le message d'un commit : -m et le fichier de -F (que le texte de la commande ne montre pas) ;
        identifiant affiché avant : permis."""
        with open(os.path.join(self.t, "msg.txt"), "w", encoding="utf-8") as f:
            f.write("reprend " + FICTIF + NL)
        lu = appel("git status")
        self.refus(lu, "git commit -q -F msg.txt", "R5")
        self.refus(lu, "git commit -am 'reprend " + FICTIF + "'", "R5")
        self.permis(lu + appel("git log -1", resultat=FICTIF + "a1 sujet"), "git commit -q -F msg.txt")

    def test_r2_ecriture_lue_sur_l_acte(self):
        """R2 : redirection, tee, sed -i, open en écriture d'un code python sur un fichier non lu : refus ; le même
        texte entre guillemets, ou une lecture (sed -n), n'écrit rien : permis."""
        n = self.notes
        for cmd in ("echo x >> " + n, "date | tee -a " + n, "sed -i -e s/a/b/ " + n, "sed -i.bak s/a/b/ " + n,
                    "python3 -c \"open('" + n + "', 'w')\"", "printf x 2>&1 > " + n):
            self.refus(appel("ls"), cmd, "R2")
        for cmd in ('echo "a > ' + n + '"', "sed -n 1p " + n, "grep -c x " + n + " > /dev/null"):
            self.permis(appel("ls"), cmd)

    def test_r1_effacement_lu_sur_l_acte(self):
        """R1 : rm récursif d'un clone (options où qu'elles soient) sans état lu : refus ; nommé dans un texte :
        permis."""
        os.makedirs(os.path.join(self.t, "clone", ".git"))
        for cmd in ("rm -rf clone", "rm clone -r -f", "cd . && rm -fR -- clone"):
            self.refus(appel("ls"), cmd, "R1")
        self.permis(appel("ls"), "echo 'rm -rf clone'")

    def test_commande_illisible_motifs(self):
        """Guillemet non fermé (shlex) ou module de lecture absent : les motifs d'avant jugent (sens sûr) ; module
        présent : lu, sans bytecode écrit à côté du crochet."""
        self.refus(appel("ls"), "echo \"x ; git commit -m y", "R3")
        seul = os.path.join(self.t, "seul")
        os.makedirs(seul)
        shutil.copy(GARDE, seul)
        self.refus(appel("ls"), SONDE, "R3", garde=os.path.join(seul, "garde_faits.py"))
        shutil.copy(os.path.join(os.path.dirname(GARDE), "acte_shell.py"), seul)
        self.permis(appel("ls"), SONDE, garde=os.path.join(seul, "garde_faits.py"))
        self.assertEqual(sorted(os.listdir(seul)), ["acte_shell.py", "garde_faits.py"])


class AttenteEtMotif(Crochet):
    """R7 (E18, E28 ; SHOGEN-GARDE-OUTIL-E18-E20-1, SHOGEN-GARDE-OUTIL-E26-E27-E28-1)."""

    def test_e18_sleep_d_avant_plan(self):
        """Cas réel E18 : sleep 60 en commande d'avant-plan, et ses formes (liste, enveloppe, bash -c, boucle while) :
        refus R7 ; boucle until, arrière-plan (&, groupe, liste, run_in_background), texte cité : permis."""
        for cmd in ("sleep 60", "ls" + NL + "sleep 60", "sleep 5 && git log -1", "timeout 30 sleep 20",
                    "bash -c 'sleep 4'", "while true; do sleep 5; done", "cmd & sleep 3"):
            self.refus(appel("ls"), cmd, "R7 (E18)")
        for cmd in ("until test -f fin; do sleep 5; done", "sleep 30 &", "(sleep 10; kill 1) &", "sleep 3 && cmd &",
                    "setsid nohup bash -c 'sleep 4' > log 2>&1 &", 'echo "sleep 60"', "sleep 2 && (kill 1) &",
                    "until test -f fin; do bash -c 'sleep 5'; done"):
            self.permis(appel("ls"), cmd)
        self.permis(appel("ls"), "sleep 60", entree={"tool_input": {"command": "sleep 60", "run_in_background": True}})
        self.refus(appel("ls"), 'echo "x ; sleep 60', "R7 (E18)")          # illisible par shlex : motifs

    def test_e28_motif_non_ancre_se_reconnait(self):
        """Cas réel E28 : le moniteur pgrep -f chaine_gf.sh se reconnaissait (le shell qui le lance porte le motif ;
        preuve sur l'hôte : trouvé sans aucune chaîne, rien trouvé une fois ancré) ; refus R7 de pkill -f et pgrep -f
        non ancrés, sous leurs formes ; motif ancré, ou sans -f : permis."""
        essai = "pgrep -f chaine_zz_" + str(os.getpid()) + ".sh"
        ancre = essai.replace("-f ", "-f '^bash ") + "'"
        lances = [subprocess.run(["bash", "-c", c + " > /dev/null; echo $?"], capture_output=True, text=True,
                                 timeout=30).stdout.split()[-1] for c in (essai, ancre)]
        self.assertEqual(lances, ["0", "1"])         # moniteur à deux commandes : le shell reste, porteur du motif
        for cmd in ("pgrep -f chaine_gf.sh", "pkill -9 -f chaine_gf.sh", "pgrep -af chaine", "x=$(pgrep -f chaine_gf)",
                    "pkill --signal TERM --full chaine", "pgrep -u 0 -f chaine", "pkill -HUP -f chaine"):
            self.refus(appel("ls"), cmd, "R7 (E28)")
        for cmd in ("pgrep -f '^bash chaine_gf.sh'", "pgrep chaine_gf", "pkill -f -- '^bash x'", "pgrep -fu0 '^x'",
                    "pgrep -f 2>/dev/null '^bash x'"):
            self.permis(appel("ls"), cmd)


if __name__ == "__main__":
    unittest.main()
