"""Cas de la consigne G2 du chemin S2 dans .claude/agents/shogen-worker.md (lot DETTES-T3, DT3-C ;
SHOGEN-G2-ENREG-ROLE-1, adjudication Q-C1) : la commande d'enregistrement du rôle G2 est au bloc « Consignes de
gabarit », une fois, à la lettre ; ses options et son rôle sont ceux de l'aide de s2-harness/tools/oracle_record.py."""
import os
import subprocess
import sys
import tempfile
import unittest

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
FICHE = os.path.join(RACINE, ".claude", "agents", "shogen-worker.md")
OUTIL = os.path.join("s2-harness", "tools", "oracle_record.py")
COMMANDE = ("env -u SHOGEN_S2_CAMPAGNE_CONTROL PYTHONDONTWRITEBYTECODE=1 python3 -B " + OUTIL + " --role G2 --commit "
            "<commit relu> --auteur <modèle résolu> --depot <copie> --sortie <dossier G2>")
DIFFS = ("Sur des diffs non commis, `<commit relu>` est la tête de la copie (base où s'appliquent les diffs) et le "
         "rapport G2 écrit l'empreinte des diffs relus (sha256 de leur concaténation dans l'ordre de la série) : "
         "`oracle_record.py` refuse `--paquet-sha256` hors du rôle `rendu`.")
BASE = ("L'enregistrement atteste alors la base et la suite lancée sur elle, non les diffs : il se vérifie à "
        "`<commit relu>`, et seul le rapport G2 le relie aux diffs.")


def lancer(*plus):
    """Commande de la consigne, marqueurs remplacés par des valeurs factices (dépôt absent), options `plus` ajoutées."""
    with tempfile.TemporaryDirectory() as d:
        valeurs = {"<commit relu>": "0" * 40, "<modèle résolu>": "claude-opus-5-5",
                   "<copie>": os.path.join(d, "absent"), "<dossier G2>": os.path.join(d, "sortie")}
        args = COMMANDE.partition(" python3 -B ")[2]
        for k in valeurs:
            args = args.replace(k, k.replace(" ", "_"))          # un marqueur, un argument
        argv = [valeurs.get(x.replace("_", " "), x) for x in args.split()] + list(plus)
        env = {k: v for k, v in os.environ.items() if k != "SHOGEN_S2_CAMPAGNE_CONTROL"}
        return subprocess.run([sys.executable, "-B", *argv], cwd=RACINE, capture_output=True, text=True, timeout=60,
                              env=env)


class FicheWorker(unittest.TestCase):
    def test_consigne_au_bloc_de_gabarit(self):
        with open(FICHE, encoding="utf-8") as f:
            texte = f.read()
        bloc = texte.partition("## Consignes de gabarit")[2]
        self.assertEqual(bloc.count("`" + COMMANDE + "`"), 1)
        self.assertEqual(texte.count(COMMANDE), 1)
        self.assertEqual(" ".join(bloc.split()).count(DIFFS + " " + BASE), 1)      # C-12 : ce qui est attesté

    def test_options_de_l_aide(self):
        aide = subprocess.run([sys.executable, "-B", os.path.join(RACINE, OUTIL), "--help"], capture_output=True,
                              text=True, timeout=60).stdout
        self.assertIn("--role {G1,G2,cp-2,rendu}", aide)
        options = [x for x in COMMANDE.split() if x.startswith("--")]
        self.assertEqual(options, ["--role", "--commit", "--auteur", "--depot", "--sortie"])
        for o in options:
            self.assertIn(o + " ", aide)

    def test_commande_passe_l_analyseur(self):
        """C-3 de la G2 : l'analyseur réel admet la commande (aucun « usage: »), l'outil la refuse ensuite sur le dépôt
        absent (sortie 2) ; C-7 : `--paquet-sha256` est refusé au rôle G2, d'où l'empreinte écrite au rapport."""
        p = lancer()
        self.assertNotIn("usage:", p.stderr)
        self.assertEqual((p.returncode, p.stderr[:16]), (2, "oracle_record : "))
        p = lancer("--paquet-sha256", "0" * 64)
        self.assertEqual(p.returncode, 2)
        self.assertIn("paquet.sha256 et sceau.genTime nuls hors", p.stderr)
