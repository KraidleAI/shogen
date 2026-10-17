"""Cas du crochet GARDE-FAITS du dépôt (.claude/hooks/garde_faits.py), lancé tel quel sur des journaux synthétiques
(nom en .txt), lot GARDE-FOUS-ORCH phase 2. LN-6 (SHOGEN-GARDE-CROCHET-ACTE-1) : l'acte est jugé, non le texte ; les
deux faux refus de la sonde du contre-contrôle (R3 puis R5 sur une commande qui écrit un journal synthétique par un
heredoc python portant un commit) passent ; les vrais refus restent ; R5 lit le fichier de git commit -F.
R7 (E18, E28) : sleep d'avant-plan ; pkill -f et pgrep -f à motif non ancré. R8 (E20) : PR sans preuve que la forge
lance des jobs sur le dépôt. R9 (E27) : seuil de coût des workflows et des agents vivants, jeton de l'investisseur.
R10 (E26) : relevé des noms propres d'un message au JOURNAL (UserPromptSubmit), dossier nommé sans relevé (Stop).
R13 (lot CAUSES ; E37, E39, E40) : processus lourd pendant une chaîne ; chaîne lancée hors du modèle ; cause de refus
d'une gate nommée sans la ligne VIOLATION lue."""
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


def outil(nom, inp, resultat, i):
    """Appel d'outil et résultat appariés par l'identifiant d'appel, comme au journal de Claude Code."""
    a = {"type": "assistant", "message": {"content": [{"type": "tool_use", "id": f"t{i}", "name": nom, "input": inp}]}}
    r = {"type": "tool_result", "tool_use_id": f"t{i}", "content": resultat}
    return [a, {"type": "user", "message": {"content": [r]}}]


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

    def arbre(self, fichiers):
        """Copie du crochet (et de son voisin) dans un arbre temporaire, avec les fichiers {chemin: texte} ; rend son
        chemin."""
        a = os.path.join(self.t, "arbre")
        os.makedirs(os.path.join(a, ".claude", "hooks"), exist_ok=True)
        for x in ("garde_faits.py", "acte_shell.py"):
            shutil.copy(os.path.join(os.path.dirname(GARDE), x), os.path.join(a, ".claude", "hooks"))
        os.makedirs(os.path.join(a, "scripts", "controle", "garde"), exist_ok=True)
        for g in ("dossiers.txt", "motif-chaine.txt"):
            shutil.copy(os.path.join(RACINE, "scripts", "controle", "garde", g), os.path.join(a, "scripts", "controle", "garde"))
        for chemin, texte in fichiers.items():
            os.makedirs(os.path.dirname(os.path.join(a, chemin)), exist_ok=True)
            with open(os.path.join(a, chemin), "w", encoding="utf-8") as f:
                f.write(texte)
        return os.path.join(a, ".claude", "hooks", "garde_faits.py")

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

    def test_ln6_actes_non_litteraux(self):
        """G2, C-2 : commande portée par une variable (programme, eval) ou lancée par un code python (os.system,
        subprocess) : les motifs d'avant jugent aussi, refus R3 ou R1 ; la sonde et un code python qui ne lance rien
        passent toujours, une variable hors du programme ne change rien."""
        os.makedirs(os.path.join(self.t, "clone", ".git"))
        for cmd, regle in (("C='git commit -m x'; $C", "R3"), ("C='git commit -m x'; eval \"$C\"", "R3"),
                           ("python3 -c \"import os; os.system('git commit -m x')\"", "R3"),
                           (NL.join(["python3 - <<'EOF'", "import subprocess", "subprocess.run('git push', shell=1)",
                                     "EOF"]), "R3"), ("R='rm -rf clone'; $R", "R1")):
            self.refus(appel("ls"), cmd, regle)
        for cmd in ("F=neuf.txt; echo x > $F", "python3 -c \"print('git commit -m x')\"", SONDE):
            self.permis(appel("ls"), cmd)

    def test_r5_lit_le_message_et_le_fichier_de_f(self):
        """R5 sur le message d'un commit : -m et le fichier de -F (que le texte de la commande ne montre pas) ;
        identifiant affiché avant : permis."""
        with open(os.path.join(self.t, "msg.txt"), "w", encoding="utf-8") as f:
            f.write("reprend " + FICTIF + NL)
        lu = appel("git status")
        self.refus(lu, "git commit -q -F msg.txt", "R5")
        self.refus(lu, "git commit -am 'reprend " + FICTIF + "'", "R5")
        self.permis(lu + appel("git log -1", resultat=FICTIF + "a1 sujet"), "git commit -q -F msg.txt")
        # G2, C-8 (mutants G11, G12 vivants) : forme --message=, et texte d'une PR créée par gh
        self.refus(lu, "git commit --message='reprend " + FICTIF + "'", "R5")
        self.refus(appel("ls"), "gh pr create --title t --body 'reprend " + FICTIF + "'", "R5")

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

    def test_e18_boucle_a_condition_de_sortie(self):
        """G2, C-3 (L-3 adjugée par l'orchestrateur) : while ou until à condition de sortie, ou boucle à condition
        constante qui porte break (moniteur de l'orchestrateur) : permis ; condition constante sans sortie (while :,
        until false, leurs négations) ou boucle for : refus R7."""
        for cmd in ("while ! test -f fin; do sleep 5; done", "while kill -0 1 2>/dev/null; do sleep 10; done; echo f",
                    "while true; do test -f fin && break; sleep 5; done",
                    "while pgrep -f '^bash c.sh'; do sleep 9; done",
                    "until ! pgrep -f '^bash c.sh'; do sleep 9; done",
                    "until test -f f; do for i in 1 2; do sleep 1; done; done"):        # C-8 : boucle englobante
            self.permis(appel("ls"), cmd)
        for cmd in ("while :; do sleep 1; done", "until false; do sleep 5; done", "while ! false; do sleep 5; done",
                    "until ! true; do sleep 5; done", "for i in 1 2; do sleep 5; done"):
            self.refus(appel("ls"), cmd, "R7 (E18)")

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


class Forge(Crochet):
    """R8 (E20 ; SHOGEN-GARDE-OUTIL-E18-E20-1) : avant mcp__github__create_pull_request."""
    PR = {"tool_name": "mcp__github__create_pull_request",
          "tool_input": {"owner": "o", "repo": "r", "title": "t", "head": "b", "base": "main"}}
    LISTE = {"method": "list_workflow_runs", "owner": "o", "repo": "r"}

    def pgrep(self, code):
        """Faux pgrep en tête du PATH (R13 a) : sortie `code` (0 : une chaîne tourne ; 1 : aucune)."""
        faux = os.path.join(self.t, "faux-pgrep")
        os.makedirs(faux, exist_ok=True)
        with open(os.path.join(faux, "pgrep"), "w", encoding="utf-8") as f:
            f.write("#!/bin/sh" + NL + f"exit {code}" + NL)
        os.chmod(os.path.join(faux, "pgrep"), 0o755)
        ancien = os.environ["PATH"]
        os.environ["PATH"] = faux + os.pathsep + ancien
        self.addCleanup(os.environ.__setitem__, "PATH", ancien)

    def test_r13_processus_lourd_pendant_une_chaine(self):
        """R13 (E37) : une chaîne tourne (pgrep du motif de garde/motif-chaine.txt : 0) : cargo, xtask ou mutants.py
        refusés, une lecture permise ; aucune chaîne (pgrep : 1) : cargo permis ; motif absent : rien détecté."""
        garde = self.arbre({"scripts/controle/gabarits/chaine-modele.sh": "#!/usr/bin/env bash" + NL})
        self.pgrep(0)
        for cmd in ("cargo --locked xtask verify", "python3 -B scripts/controle/mutants.py c j m.json --sortie s",
                    "timeout 600 env -u X cargo test -p xtask", "bash -c 'cd d && cargo build'"):
            self.refus([], cmd, "R13 (E37)", garde=garde)
        self.permis(appel("ls"), "git status", garde=garde)
        for cmd in ("grep cargo x.txt", "echo cargo", "ls target/debug/xtask", "git log -1 --grep xtask"):
            self.permis(appel("ls"), cmd, garde=garde)          # G2 du lot CAUSES (C-2) : nommé, non lancé
        self.refus([], "python3 -X dev -B scripts/controle/mutants.py c j m.json --sortie s", "R13 (E37)", garde=garde)
        copie = os.path.join(self.t, "chaine_int3.sh")
        with open(copie, "w", encoding="utf-8") as f:
            f.write("#!/usr/bin/env bash" + NL)
        self.refus(appel("ls"), f"setsid nohup timeout 60 bash -c 'bash \"$1\"' _ {copie} > {self.t}/c.log 2>&1 &",
                   "R13 (E37)", garde=garde)                   # C-2 : une seconde chaîne pendant la première
        self.pgrep(1)
        self.permis(appel("ls"), "cargo --locked xtask verify", garde=garde)
        self.permis(appel("ls"), f"bash {copie}", garde=garde)
        sans = self.arbre({})
        os.remove(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(sans))), "scripts", "controle", "garde", "motif-chaine.txt"))
        self.pgrep(0)
        self.permis(appel("ls"), "cargo --locked xtask verify", garde=sans)

    def test_r13_chaine_lancee_hors_du_modele(self):
        """R13 (E39) : une chaîne lancée (chaine.sh, chaine_x.sh, aussi derrière setsid nohup timeout bash -c) doit être
        la copie à l'octet de gabarits/chaine-modele.sh : copie égale admise ; script différent, illisible ou modèle
        absent du dépôt : refus."""
        modele = "#!/usr/bin/env bash" + NL + "set -Eeuo pipefail" + NL + "echo FIN" + NL
        garde = self.arbre({"scripts/controle/gabarits/chaine-modele.sh": modele})
        self.pgrep(1)
        with open(os.path.join(self.t, "chaine_int3.sh"), "w", encoding="utf-8") as f:
            f.write(modele)
        with open(os.path.join(self.t, "chaine_main.sh"), "w", encoding="utf-8") as f:
            f.write(modele + "git commit -q -m x" + NL)
        egal, autre = os.path.join(self.t, "chaine_int3.sh"), os.path.join(self.t, "chaine_main.sh")
        self.permis(appel("ls"), f"DETACHE=1 setsid nohup timeout 13680 bash -c 'bash \"$1\"' _ {egal} > c.log 2>&1 &", garde=garde)
        self.permis(appel("ls"), f"bash {egal}", garde=garde)
        self.refus(appel("ls"), f"bash {autre}", "R13 (E39)", garde=garde)
        self.refus(appel("ls"), f"setsid nohup bash {os.path.join(self.t, 'chaine_absente.sh')} &", "R13 (E39)", garde=garde)
        self.assertIn("script différent du modèle", self.lancer(appel("ls"), f"bash {autre}", garde=garde)[1])
        for cmd in (f"cp {egal} {os.path.join(self.t, 'chaine_neuf.sh')}", f"cat {autre}", "grep -n chaine.sh notes.txt",
                    f"bash -c 'bash {egal}'"):
            self.permis(appel("ls"), cmd, garde=garde)          # G2 du lot CAUSES (C-2) : nommé, non lancé ; -c lu
        for cmd in (f"bash -e {autre}", f"source {autre}", f". {autre}"):
            self.refus(appel("ls"), cmd, "R13 (E39)", garde=garde)
        os.makedirs(os.path.join(self.t, "sous"))
        with open(os.path.join(self.t, "sous", "chaine_int3.sh"), "w", encoding="utf-8") as f:
            f.write(modele + "git commit -q -m x" + NL)
        self.refus(appel("ls"), f"cd {os.path.join(self.t, 'sous')} && bash chaine_int3.sh", "R13 (E39)", garde=garde)
        sans = self.arbre({})
        os.remove(os.path.join(self.t, "arbre", "scripts", "controle", "gabarits", "chaine-modele.sh"))
        self.refus(appel("ls"), f"bash {egal}", "R13 (E39)", garde=sans)
        self.assertIn("modèle scripts/controle/gabarits/chaine-modele.sh absent", self.lancer(appel("ls"), f"bash {egal}", garde=sans)[1])

    def test_r13_cause_de_refus_sans_la_ligne_de_la_gate(self):
        """R13 (E40) : une consigne (SendMessage, Agent) qui dit qu'une gate a rougi cite une ligne VIOLATION … ou
        REFUS … lue dans un résultat d'outil : citée telle quelle : permis ; cause déduite sans ligne : refus ; ligne
        citée mais absente du journal : refus ; consigne sans mot de rougeur : permis."""
        ligne = "VIOLATION docs/x.md:45 — « guaranteed » dans la voix du projet — qualificatif interdit (09)"
        vu = outil("Bash", {"command": "grep -n VIOLATION sortie.log"}, "  " + ligne, 1)
        def consigne(texte, nom="SendMessage"):
            cle = "message" if nom == "SendMessage" else "prompt"
            return {"tool_name": nom, "tool_input": {cle: texte}}
        self.permis(vu, "", entree=consigne("La vérification est ROUGE à la gate S-G4 : " + ligne + " ; mets le mot en code."))
        self.refus(vu, "", "R13 (E40)", entree=consigne("La vérification est ROUGE à la gate S-G4 : le mot garanti est en clair dans la table."))
        self.refus(vu, "", "R13 (E40)", entree=consigne("Refusé par la gate S-G4 : VIOLATION docs/y.md:3 — « verified » en clair.", "Agent"))
        self.permis(vu, "", entree=consigne("Contrôles rejoués : S-G5, presg5 : 0 fragment ; R-13 : 0 marqueur ; suite verte."))
        courte, guillemets = "VIOLATION docs/a.md:3 — « verified »", 'REFUS R-13 : marqueur "TODO" nu, docs/b.md:12'
        vu2 = vu + outil("Bash", {"command": "grep -n REFUS r.log"}, courte + NL + guillemets, 2)
        for juste in ("La gate S-G4 est rouge : " + courte + " ; mets le mot en code.", "Le job g5 est rouge : " + guillemets,
                      "Rouge avant, vert après : chaque cas rouge sans son correctif, puis vert.",
                      "Rejoue S-G4 sur les pièces : aucune violation attendue."):
            self.permis(vu2, "", entree=consigne(juste))        # G2 du lot CAUSES (C-3)
        for faux in ("La gate S-G4 a échoué sur le mot garanti.", "S-G4 failed: garanti in the table.",
                     "Le passage à blanc a donné REFUS K8 : test_e25 hérite de DETACHE.",
                     "S-G4 rouge : " + ligne + " ; et VIOLATION docs/y.md:9 — « garanti ».",
                     "La chaîne est bloquée par S-G4 : mot garanti."):
            self.refus(vu2, "", "R13 (E40)", entree=consigne(faux))

    def test_e20_forge_sans_job(self):
        """Cas réel E20 : dépôt privé, la forge ne lance aucun job (runner_id 0, échec en 2 s) : refus R8, avant
        tout comme après une lecture qui le montre ; run conclu success, ou job à runner_id non nul, lu pour ce
        dépôt (outil MCP ou gh run) : permis ; lu pour un autre dépôt : refus."""
        echec = '{"workflow_runs": [{"status": "completed", "conclusion": "failure", "runner_id": 0}]}'
        self.refus(appel("ls"), "", "R8 (E20)", entree=self.PR)
        self.refus(outil("mcp__github__actions_list", self.LISTE, echec, 1), "", "R8 (E20)", entree=self.PR)
        vu = outil("mcp__github__actions_list", self.LISTE, '{"jobs": [{"runner_id": 17, "status": "completed"}]}', 1)
        self.permis(vu, "", entree=self.PR)
        gh = outil("Bash", {"command": "gh run list -R o/r"}, "completed\tsuccess\tgates", 2)
        self.permis(gh, "", entree=self.PR)
        autre = dict(self.LISTE, repo="autre")
        self.refus(outil("mcp__github__actions_list", autre, '"conclusion": "success"', 1), "", "R8", entree=self.PR)
        # G2, C-8 (mutants G04, G05 vivants) : refus du crochet cité dans un résultat, gh run d'un autre dépôt
        refus = 'GARDE-FAITS : REFUS. "conclusion": "success"'
        self.refus(outil("mcp__github__actions_list", self.LISTE, refus, 1), "", "R8", entree=self.PR)
        self.refus(outil("Bash", {"command": "gh run list -R x/r"}, "completed\tsuccess\tgates", 2), "", "R8",
                   entree=self.PR)

    def test_e20_marqueur_du_jour(self):
        """Marqueur scripts/controle/garde/forge-actions.txt (G2, C-4) : ligne o/r du jour (date -u, fixée par un faux
        date) qui porte l'identifiant d'un run lu dans une preuve du même dépôt, au journal principal (PR créée par un
        sous-agent) ou d'un sous-agent de la session : permis ; ligne sans identifiant, d'un autre jour, d'un autre
        dépôt, identifiant absent des preuves ou lu dans un échec : refus."""
        faux = os.path.join(self.t, "faux")
        os.makedirs(faux)
        with open(os.path.join(faux, "date"), "w", encoding="utf-8") as f:
            f.write("#!/bin/sh" + NL + "echo 2026-10-15" + NL)
        os.chmod(os.path.join(faux, "date"), 0o755)
        chemin = os.path.join("scripts", "controle", "garde", "forge-actions.txt")
        ancien = os.environ["PATH"]
        os.environ["PATH"] = faux + os.pathsep + ancien
        self.addCleanup(os.environ.__setitem__, "PATH", ancien)
        sous = os.path.join(self.t, "agent-a1.txt")
        with open(sous, "w", encoding="utf-8") as f:
            f.write(json.dumps(appel("ls")[0]) + NL)
        pr = dict(self.PR, agent_id="a1", agent_transcript_path=sous)
        vu = outil("mcp__github__actions_list", self.LISTE,
                   '{"workflow_runs": [{"id": 4242, "conclusion": "success"}]}', 1)
        echec = outil("mcp__github__actions_list", self.LISTE, '{"workflow_runs": [{"id": 4343, "runner_id": 0}]}', 1)
        for avant, texte, code in ((vu, "# entête" + NL + "o/r 2026-10-15 4242" + NL, 0),
                                   (vu, "o/r 2026-10-15" + NL, 2),
                                   (vu, "o/r 2026-10-14 4242" + NL, 2), (vu, "x/r 2026-10-15 4242" + NL, 2),
                                   (vu, "o/r 2026-10-15 4243" + NL, 2), (echec, "o/r 2026-10-15 4343" + NL, 2),
                                   (appel("ls"), "o/r 2026-10-15 4242" + NL, 2)):
            self.assertEqual(self.lancer(avant, "", garde=self.arbre({chemin: texte}), entree=pr)[0], code, texte)
        os.makedirs(os.path.join(self.t, "subagents"))
        with open(os.path.join(self.t, "subagents", "agent-b.txt"), "w", encoding="utf-8") as f:
            f.writelines(json.dumps(e) + NL for e in vu)
        garde = self.arbre({chemin: "o/r 2026-10-15 4242" + NL})
        self.assertEqual(self.lancer(appel("ls"), "", garde=garde, entree=self.PR)[0], 0)


class Cout(Crochet):
    """R9 (E27 ; SHOGEN-GARDE-OUTIL-E26-E27-E28-1) : avant Agent et Workflow."""
    DIX = {"script": " ".join(f"agent({{prompt: 'point {k}', model: 'claude-opus-5-5'}});" for k in range(10))}

    def humain(self, texte):
        return {"type": "user", "message": {"role": "user", "content": texte}}

    def vivants(self, n, age=0):
        d = os.path.join(self.t, "subagents")
        os.makedirs(d, exist_ok=True)
        for k in range(n):
            x = os.path.join(d, f"agent-a{k}.txt")
            with open(x, "w", encoding="utf-8") as f:
                f.write("x")
            os.utime(x, (os.path.getmtime(x) - age,) * 2)

    def test_e27_workflow_de_dix_agents(self):
        """Cas réel E27 : workflow de 10 agents lancé sans estimer le coût : refus R9 ; boucle qui multiplie les
        agents (nombre illisible) : refus ; trois agents : permis ; jeton FANOUT-AUTORISE, ou les mots fan out, dans
        le dernier message de l'humain : permis ; jeton dans un message plus ancien ou un résultat d'outil : refus."""
        wf = lambda inp: {"tool_name": "Workflow", "tool_input": inp}
        boucle = {"script": "for (const p of points) { await agent({prompt: p}) }"}
        trois = {"script": "agent({prompt: 'a'}); agent({prompt: 'b'}); agent({prompt: 'c'})"}
        for inp in (self.DIX, boucle):
            self.refus([self.humain("vérifie ces quatre points")], "", "R9 (E27)", entree=wf(inp))
        self.permis([self.humain("vérifie")], "", entree=wf(trois))
        quatre = {"script": trois["script"] + " agent({prompt: 'd'})"}
        self.refus([self.humain("vérifie")], "", "R9 (E27)", entree=wf(quatre))
        for texte in ("vas-y, FANOUT-AUTORISE", "on peut fan out sur les dix"):
            self.permis([self.humain(texte)], "", entree=wf(self.DIX))
        ancien = [self.humain("FANOUT-AUTORISE"), self.humain("autre chose")]
        self.refus(ancien + appel("ls", resultat="FANOUT-AUTORISE"), "", "R9", entree=wf(self.DIX))
        meta = {"type": "user", "isMeta": True, "message": {"role": "user", "content": "FANOUT-AUTORISE"}}
        self.refus([self.humain("vérifie"), meta], "", "R9", entree=wf(self.DIX))     # G2, C-8 (G06 vivant)

    def test_e27_fan_out_dans_une_phrase_niee(self):
        """G2, C-7 : les mots fan out dans une phrase niée ne valent pas jeton (refus R9) ; FANOUT-AUTORISE vaut
        toujours, et une négation d'une autre phrase ne retire pas le jeton."""
        wf = {"tool_name": "Workflow", "tool_input": self.DIX}
        for texte in ("non, pas de fan out, fais en direct", "fan-out interdit ici", "no fan out please"):
            self.refus([self.humain(texte)], "", "R9 (E27)", entree=wf)
        for texte in ("pas de souci, FANOUT-AUTORISE", "Pas de souci. Fan out sur les dix."):
            self.permis([self.humain(texte)], "", entree=wf)

    def test_e27_jeton_lu_au_journal_de_la_session(self):
        """Pour un sous-agent, le jeton se lit au dernier message de l'humain du journal de la session, jamais au
        brief que le sous-agent a reçu."""
        sous = os.path.join(self.t, "agent-a9.txt")

        def lancer_sous(brief, humain):
            with open(sous, "w", encoding="utf-8") as f:
                f.write(json.dumps(self.humain(brief)) + NL)
            plus = {"tool_name": "Workflow", "tool_input": self.DIX, "agent_id": "a9", "agent_transcript_path": sous}
            return self.lancer([self.humain(humain)], "", entree=plus)[0]
        self.assertEqual([lancer_sous("vas-y, FANOUT-AUTORISE", "vérifie"), lancer_sous("vérifie", "FANOUT-AUTORISE")],
                         [2, 0])

    def test_e27_agents_vivants(self):
        """Quatre sous-agents vivants (journal touché depuis moins de 300 s) : un cinquième refusé ; trois vivants, ou
        quatre journaux vieux de plus de 300 s : permis."""
        agent = {"tool_name": "Agent", "tool_input": {"prompt": "relis la note", "subagent_type": "shogen-worker"}}
        self.vivants(4)
        self.refus([self.humain("relis")], "", "R9 (E27)", entree=agent)
        shutil.rmtree(os.path.join(self.t, "subagents"))
        self.vivants(3)
        self.permis([self.humain("relis")], "", entree=agent)
        self.vivants(4, age=1000)
        self.permis([self.humain("relis")], "", entree=agent)
        for k in range(4):                  # G2, C-8 (G07 vivant) : un fichier qui n'est pas agent-* ne compte pas
            with open(os.path.join(self.t, "subagents", f"autre-{k}.txt"), "w", encoding="utf-8") as f:
                f.write("x")
        self.permis([self.humain("relis")], "", entree=agent)


class Releve(Crochet):
    """R10 (E26 ; SHOGEN-GARDE-OUTIL-E26-E27-E28-1) : UserPromptSubmit et Stop."""
    COURRIEL = ("Hi Shogen team," + NL + "Thanks for the heads-up about your report." + NL + "Regarding the outage "
                "wording, we checked it at 10:00 UTC." + NL + "Best, Jane Doe, CoinGecko (jane@coingecko.com)")
    JOURNAL = {"JOURNAL.md": "# Journal" + NL + "Préavis privés envoyés, CoinGecko par formulaire." + NL,
               os.path.join("docs", "publication", "envoi-preavis", "REPONSE.md"): "Réponse de CoinGecko." + NL}

    def evenement(self, garde, ev, avant, **plus):
        j = os.path.join(self.t, "journal.txt")
        with open(j, "w", encoding="utf-8") as f:
            f.writelines(json.dumps(e) + NL for e in avant)
        e = {"hook_event_name": ev, "transcript_path": j, "cwd": self.t, **plus}
        p = subprocess.run([sys.executable, "-I", garde], input=json.dumps(e), capture_output=True, text=True,
                           timeout=60)
        return p.returncode, p.stdout, p.stderr

    def tour(self, reponse, *outils):
        humain = {"type": "user", "message": {"role": "user", "content": self.COURRIEL}}
        texte = {"type": "assistant", "uuid": "u1", "message": {"content": [{"type": "text", "text": reponse}]}}
        return [humain, *[e for x in outils for e in x], texte]

    def test_e26_courriel_rattache_sans_releve(self):
        """Cas réel E26 : courriel de CoinGecko rattaché à Pocket sans recherche au JOURNAL : refus R10 au Stop ;
        second arrêt (stop_hook_active) : passage consigné ; arrêt d'un sous-agent : non jugé."""
        garde = self.arbre(self.JOURNAL)
        code, _o, err = self.evenement(garde, "Stop", self.tour("C'est la réponse au rapport de Pocket."))
        self.assertEqual((code, "R10 (E26)" in err, "Pocket" in err), (2, True, True), err)
        self.assertEqual(self.evenement(garde, "Stop", self.tour("Rattaché à Pocket."), stop_hook_active=True)[0], 0)
        ancien = outil("Bash", {"command": "grep -n Pocket JOURNAL.md"}, "55:## Session POKT (Pocket)", 1)
        self.assertEqual(self.evenement(garde, "Stop", ancien + self.tour("Rattaché à Pocket."))[0], 2)  # tour d'avant
        self.assertEqual(self.evenement(garde, "SubagentStop", self.tour("Rattaché à Pocket."), agent_id="a")[0], 0)
        codes = [self.evenement(garde, "Stop", self.tour(x))[0] for x in ("Rattaché à pocket.", "Un Pocketbook.")]
        self.assertEqual(codes, [2, 0])     # G2, C-8 (G10 vivant) : casse ignorée, mot entier
        nomme = [{"type": "user", "message": {"content": "Jane de CoinGecko demande où en est Pocket."}},
                 {"type": "assistant", "message": {"content": [{"type": "text", "text": "Pocket attend."}]}}]
        self.assertEqual(self.evenement(garde, "Stop", nomme)[0], 0)          # le message nomme lui-même le dossier

    def test_e26_releve_puis_rattachement(self):
        """UserPromptSubmit : noms propres relevés (pas les mots de début de phrase ni les mots courants), lignes du
        JOURNAL et de docs/publication/ affichées en contexte ; la réponse qui rattache au préavis (lu au relevé) passe,
        celle qui rattache à Pocket (absent du relevé) reste refusée ; un grep -n du tour qui affiche Pocket suffit ;
        message sans nom propre : rien relevé, réponse non jugée."""
        garde = self.arbre(self.JOURNAL)
        code, sortie, _e = self.evenement(garde, "UserPromptSubmit", [], prompt=self.COURRIEL)
        self.assertEqual((code, sortie.split(NL)[0][:99]), (0, "RELEVÉ (crochet du dépôt, E26) : noms propres du "
                         "message : Shogen, Jane, Doe, CoinGecko, coingecko."))
        self.assertIn("JOURNAL.md:2: Préavis privés envoyés, CoinGecko", sortie)
        self.assertIn(os.path.join("docs", "publication", "envoi-preavis", "REPONSE.md") + ":1:", sortie)
        self.assertEqual(self.evenement(garde, "Stop", self.tour("Réponse au préavis de S2."))[0], 0)
        self.assertEqual(self.evenement(garde, "Stop", self.tour("Réponse au rapport Pocket."))[0], 2)
        grep = outil("Bash", {"command": "grep -n Pocket JOURNAL.md"}, "55:## Session POKT (Pocket)", 1)
        self.assertEqual(self.evenement(garde, "Stop", self.tour("Réponse au rapport Pocket.", grep))[0], 0)
        self.assertEqual(self.evenement(garde, "UserPromptSubmit", [], prompt="où en est la suite ?")[:2], (0, ""))
        autre = [{"type": "user", "message": {"content": "Note de Paul Martin sur la suite."}},
                 {"type": "assistant", "message": {"content": [{"type": "text", "text": "Réponse au préavis."}]}}]
        self.assertEqual(self.evenement(garde, "Stop", autre)[0], 2)          # relevé d'un autre message : sans effet

    def test_e26_dossiers_lus_au_fichier(self):
        """G2, C-5 : la liste des dossiers se lit dans scripts/controle/garde/dossiers.txt (versé, un nom par ligne) :
        un dossier ajouté au fichier est refusé sans relevé, un dossier qui n'y est plus ne l'est plus."""
        chemin = os.path.join("scripts", "controle", "garde", "dossiers.txt")
        garde = self.arbre(dict(self.JOURNAL, **{chemin: "# liste" + NL + "Zorglub" + NL}))
        codes = [self.evenement(garde, "Stop", self.tour(f"Rattaché à {d}."))[0] for d in ("Zorglub", "Pocket")]
        self.assertEqual(codes, [2, 0])

    def test_e26_crochet_branche(self):
        """.claude/settings.json branche le crochet du dépôt sur UserPromptSubmit."""
        with open(os.path.join(RACINE, ".claude", "settings.json"), encoding="utf-8") as f:
            reglages = json.load(f)
        commandes = [h["command"] for x in reglages["hooks"]["UserPromptSubmit"] for h in x["hooks"]]
        self.assertEqual(commandes, ['python3 -I "$CLAUDE_PROJECT_DIR/.claude/hooks/garde_faits.py"'])


class Serie(Crochet):
    """Lot INTEGRATION-P2 : la règle E7 du groupe A (P2A-4, comptes d'un brief écrit par le shell) lit les fichiers
    écrits sur l'acte de LN-6 (fc["ecrit"], GFB-2) ; posée sur l'ancienne variable cibles, que GFB-2 retire, toute
    commande Bash sortait en erreur interne du crochet, acte permis sans contrôle (adjudication du groupe B, point 3)."""
    def test_bash_juge_apres_la_serie(self):
        """Après la série : une commande Bash interdite reste refusée (R3, commit sans état lu ; E7, compte d'un brief
        écrit par le shell et jamais affiché) ; affiché, le compte passe ; une commande sans acte jugé passe sans
        erreur interne."""
        self.refus([], "git commit -q -m x", "R3")
        self.refus([], "printf '5 mutants' > BRIEF-x.md", "E7")
        self.permis(appel("true", resultat="5 mutants"), "printf '5 mutants' > BRIEF-x.md")
        self.permis([], "ls")


if __name__ == "__main__":
    unittest.main()
