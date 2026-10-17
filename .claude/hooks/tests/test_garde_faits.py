"""Cas de la garde des faits : un cas « refusé » et un cas « autorisé » par règle, sur des journaux synthétiques.
Lancement : python3 -I .claude/hooks/tests/test_garde_faits.py -v (depuis la racine du dépôt)."""
import json
import os
import subprocess
import sys
import tempfile
import unittest

ICI = os.path.dirname(os.path.abspath(__file__))
GARDE = os.path.join(os.path.dirname(ICI), "garde_faits.py")
SHA = "9f8e7d6"           # identifiant fictif, jamais affiché sauf où le cas le dit
SHA2 = "abc1234"
os.environ["SHOGEN_GARDE_REFUS"] = os.devnull      # GARDE-FOUS phase 3 : jamais le journal des refus du dépôt (G2 ISOLE-ENV, C-2)


def entree_appel(nom, inp):
    return {"type": "assistant", "uuid": "u-" + nom, "message": {"role": "assistant", "content": [{"type": "tool_use", "name": nom, "input": inp}]}}


def entree_resultat(texte):
    return {"type": "user", "message": {"role": "user", "content": [{"type": "tool_result", "content": texte}]}}


def entree_texte(texte):
    return {"type": "assistant", "uuid": "u-texte-" + str(abs(hash(texte)) % 10**6), "message": {"role": "assistant", "content": [{"type": "text", "text": texte}]}}


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dossier = self.tmp.name
        self.journal = os.path.join(self.dossier, "session.jsonl")
        self.fichier = os.path.join(self.dossier, "NOTES.md")
        with open(self.fichier, "w", encoding="utf-8") as f:
            f.write("note\n")

    def tearDown(self):
        self.tmp.cleanup()

    def ecrire_journal(self, entrees, agent=None):
        chemin = self.journal
        if agent:
            os.makedirs(os.path.join(self.dossier, "session", "subagents"), exist_ok=True)
            chemin = os.path.join(self.dossier, "session", "subagents", f"agent-{agent}.jsonl")
        with open(chemin, "w", encoding="utf-8") as f:
            for e in entrees:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")

    def lancer(self, ev, tool_name=None, tool_input=None, agent=None):
        entree = {"hook_event_name": ev, "session_id": "s", "transcript_path": self.journal, "cwd": self.dossier}
        if tool_name:
            entree["tool_name"] = tool_name
            entree["tool_input"] = tool_input or {}
        if agent:
            entree["agent_id"] = agent
        p = subprocess.run([sys.executable, "-I", GARDE], input=json.dumps(entree), capture_output=True, text=True, timeout=30)
        return p.returncode, p.stderr

    def refuse(self, *a, **k):
        rc, err = self.lancer(*a, **k)
        self.assertEqual(rc, 2, err)
        self.assertIn("GARDE-FAITS : REFUS", err)
        return err

    def permet(self, *a, **k):
        rc, err = self.lancer(*a, **k)
        self.assertEqual(rc, 0, err)
        self.assertNotIn("REFUS", err)


class R1_EffacerArbre(Base):
    def setUp(self):
        super().setUp()
        self.arbre = os.path.join(self.dossier, "clone")
        os.makedirs(os.path.join(self.arbre, ".git"))

    def test_refuse_sans_status(self):
        self.ecrire_journal([entree_appel("Bash", {"command": "ls"})])
        err = self.refuse("PreToolUse", "Bash", {"command": f"rm -rf {self.arbre}"})
        self.assertIn("R1", err)

    def test_permis_apres_status_et_log(self):
        self.ecrire_journal([entree_appel("Bash", {"command": f"git -C {self.arbre} status --short"}), entree_resultat(""),
                             entree_appel("Bash", {"command": f"git -C {self.arbre} log origin/main..HEAD --oneline"}), entree_resultat("")])
        self.permet("PreToolUse", "Bash", {"command": f"rm -rf {self.arbre}"})


class R2_EcrireFichierExistant(Base):
    def test_refuse_sans_lecture(self):
        self.ecrire_journal([entree_appel("Bash", {"command": "ls"})])
        err = self.refuse("PreToolUse", "Bash", {"command": f"echo x >> {self.fichier}"})
        self.assertIn("R2", err)

    def test_refuse_sed_i(self):
        self.ecrire_journal([entree_appel("Bash", {"command": "ls"})])
        self.refuse("PreToolUse", "Bash", {"command": f"sed -i 's/a/b/' {self.fichier}"})

    def test_permis_apres_read(self):
        self.ecrire_journal([entree_appel("Read", {"file_path": self.fichier}), entree_resultat("note")])
        # G2, C-6 (L-7) : nom relatif au cwd du cas ; le chemin du TMPDIR (segment hexadécimal) reste hors du texte
        self.permet("PreToolUse", "Bash", {"command": "echo x >> NOTES.md"})

    def test_permis_apres_tail(self):
        self.ecrire_journal([entree_appel("Bash", {"command": f"tail -3 {self.fichier}"}), entree_resultat("note")])
        self.permet("PreToolUse", "Bash", {"command": "printf 'y\\n' >> NOTES.md"})

    def test_permis_fichier_neuf(self):
        self.ecrire_journal([entree_appel("Bash", {"command": "ls"})])
        self.permet("PreToolUse", "Bash", {"command": f"echo x > {self.dossier}/neuf.txt"})


class R3_CommitPush(Base):
    def test_commit_refuse_sans_diff(self):
        self.ecrire_journal([entree_appel("Bash", {"command": "ls"})])
        err = self.refuse("PreToolUse", "Bash", {"command": "git commit -m 'x'"})
        self.assertIn("R3", err)

    def test_commit_permis_apres_status(self):
        self.ecrire_journal([entree_appel("Bash", {"command": "git status --short"}), entree_resultat("M a")])
        self.permet("PreToolUse", "Bash", {"command": "git commit -m 'x'"})

    def test_push_refuse_sans_lecture(self):
        self.ecrire_journal([entree_appel("Bash", {"command": "git commit -m x"})])
        self.refuse("PreToolUse", "Bash", {"command": "git push -u origin b"})

    def test_push_permis_apres_log_origin(self):
        self.ecrire_journal([entree_appel("Bash", {"command": "git log --oneline origin/b..HEAD"}), entree_resultat(SHA2 + " x")])
        self.permet("PreToolUse", "Bash", {"command": "git push -u origin b"})


class R4_SousAgent(Base):
    def test_refuse_sans_etat(self):
        self.ecrire_journal([entree_appel("Bash", {"command": "ls"})])
        err = self.refuse("PreToolUse", "Agent", {"prompt": "Travaille sur le dépôt /home/user/shogen"})
        self.assertIn("R4", err)

    def test_permis_apres_status(self):
        self.ecrire_journal([entree_appel("Bash", {"command": "git status --short"}), entree_resultat("")])
        self.permet("PreToolUse", "Agent", {"prompt": "Travaille sur le dépôt /home/user/shogen"})


class R5_Identifiants(Base):
    def test_refuse_sha_jamais_affiche(self):
        self.ecrire_journal([entree_appel("Bash", {"command": "git status"}), entree_resultat("clean"),
                             entree_texte("le commit est " + SHA)])      # tapé par l'agent : ne compte pas
        err = self.refuse("PreToolUse", "Edit", {"file_path": self.fichier, "old_string": "note", "new_string": "commit `" + SHA + "`"})
        self.assertIn("R5", err)

    def test_refuse_sha_cite_par_un_refus(self):
        self.ecrire_journal([entree_resultat("GARDE-FAITS : REFUS. R5 : l'identifiant « " + SHA + " » …")])
        self.refuse("PreToolUse", "Edit", {"file_path": self.fichier, "old_string": "note", "new_string": "commit " + SHA})

    def test_permis_sha_affiche(self):
        self.ecrire_journal([entree_appel("Bash", {"command": "git log -n 1"}), entree_resultat(SHA + "a1 sujet")])
        self.permet("PreToolUse", "Edit", {"file_path": self.fichier, "old_string": "note", "new_string": "commit `" + SHA + "`"})

    def test_refuse_pr_jamais_affichee(self):
        self.ecrire_journal([entree_appel("Bash", {"command": "git status"}), entree_resultat("clean")])
        self.refuse("PreToolUse", "Bash", {"command": "git commit -m 'ferme la PR n° 42'"})

    def test_permis_pr_affichee(self):
        self.ecrire_journal([entree_appel("Bash", {"command": "git status"}), entree_resultat("pull/42 ouverte")])
        self.permet("PreToolUse", "Bash", {"command": "git commit -m 'ferme la PR n° 42'"})

    def test_permis_sha_affiche_dans_journal_du_sous_agent(self):
        self.ecrire_journal([entree_appel("Bash", {"command": "git status"}), entree_resultat(SHA2 + " vu par le sous-agent")], agent="a1")
        self.journal = os.path.join(self.dossier, "session.jsonl")
        self.permet("PreToolUse", "Bash", {"command": "git commit -m 'reprend " + SHA2 + "'"}, agent="a1")


class R6_Stop(Base):
    def test_refuse_nombre_non_affiche_puis_passe_au_second_arret(self):
        self.ecrire_journal([entree_resultat("Ran 38"), entree_texte("Résultat : 1 715 fenêtres et 0,901.")])
        err = self.refuse("Stop")
        self.assertIn("R6", err)
        self.permet("Stop")        # second arrêt du même tour : passage consigné
        with open(os.path.join(self.dossier, "garde-faits.log"), encoding="utf-8") as f:
            self.assertIn("PASSAGE", f.read())

    def test_refuse_duree_de_memoire_E29(self):
        self.ecrire_journal([entree_resultat("git status : propre"), entree_texte("Pendant les 28 jours de collecte, le travail continue.")])
        err = self.refuse("Stop")
        self.assertIn("28", err)

    def test_permis_duree_lue_E29(self):
        self.ecrire_journal([entree_resultat("(e) ... 16 semaines donnent 0,91"), entree_texte("La collecte dure 16 semaines.")])
        self.permet("Stop")

    def test_permis_petit_nombre_sans_unite(self):
        self.ecrire_journal([entree_resultat("ok"), entree_texte("Point 3 de la liste, pas 7 de la chaîne DT7-l, section 2 du plan.")])
        self.permet("Stop")

    def test_permis_nombres_affiches(self):
        self.ecrire_journal([entree_resultat("n = 1715 ; phi = 0.901"), entree_texte("Résultat : 1 715 fenêtres et 0,901.")])
        self.permet("Stop")

    def test_permis_veille_attachment(self):
        self.ecrire_journal([{"type": "attachment", "attachment": {"type": "queued_command", "prompt": "commit " + SHA2 + " Ran = 419"}},
                             entree_texte("La suite compte 419 cas.")])
        self.permet("Stop")

    def test_sous_agent(self):
        self.ecrire_journal([entree_texte("Il reste 4093 démarrages.")], agent="a2")
        rc, err = self.lancer("SubagentStop", agent="a2")
        self.assertEqual(rc, 2)


if __name__ == "__main__":
    unittest.main()
