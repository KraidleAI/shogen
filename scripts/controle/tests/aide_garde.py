"""Aide des tests du lot GARDE-FOUS-ORCH : dépôts git temporaires, isolés de la configuration de l'hôte (ni
configuration globale ni système, donc ni crochet ni signature), jamais le dépôt du projet."""
import os
import re
import subprocess

ICI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))     # scripts/controle


def variables_de_chaine():
    """Noms des variables que lisent les modèles de chaîne (`${NOM:` dans gabarits/*.sh, lus sur les fichiers, jamais
    recopiés) : un cas ne les hérite jamais de l'environnement ambiant (E39 : `DETACHE=1` posé au lancement d'une chaîne
    réelle faisait admettre à `test_e25_lancement_lie` un lancement lié qu'il doit refuser)."""
    dossier, noms = os.path.join(ICI, "gabarits"), set()
    for nom in sorted(os.listdir(dossier)):
        if nom.endswith(".sh"):
            with open(os.path.join(dossier, nom), encoding="utf-8") as f:
                noms.update(re.findall(r"\$\{([A-Z][A-Z0-9_]*):", f.read()))
    return frozenset(noms)


def env_git(dossier):
    """Environnement d'un git isolé : configuration vide écrite dans `dossier`, auteur fixe, HOME = `dossier` ; sans
    les variables des modèles de chaîne (`variables_de_chaine`, E39)."""
    vide = os.path.join(dossier, "gitconfig-vide")
    with open(vide, "a", encoding="utf-8"):
        pass
    chaine = variables_de_chaine()
    env = {k: v for k, v in os.environ.items()
           if not k.startswith("GIT_") and k != "SHOGEN_S2_CAMPAGNE_CONTROL" and k not in chaine}
    env.update(GIT_CONFIG_GLOBAL=vide, GIT_CONFIG_NOSYSTEM="1", HOME=dossier, GIT_AUTHOR_NAME="essai",
               GIT_AUTHOR_EMAIL="essai@exemple.invalid", GIT_COMMITTER_NAME="essai",
               GIT_COMMITTER_EMAIL="essai@exemple.invalid")
    return env


def git(depot, env, *args):
    return subprocess.run(["git", "-C", depot, *args], capture_output=True, text=True, check=True, env=env).stdout


def ecrire(depot, fichiers):
    for chemin, texte in fichiers.items():
        p = os.path.join(depot, chemin)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="") as f:
            f.write(texte)


def depot(dossier, fichiers):
    """Dépôt `dossier`/depot, un commit initial des `fichiers` {chemin: texte} ; rend (chemin, environnement)."""
    d, env = os.path.join(dossier, "depot"), env_git(dossier)
    os.makedirs(d)
    git(d, env, "init", "-q", "-b", "main")
    ecrire(d, fichiers)
    git(d, env, "add", "-A")
    git(d, env, "commit", "-q", "-m", "initial")
    return d, env
