"""Contrôles avant l'acte de l'orchestrateur (lot GARDE-FOUS-ORCH ; G0 docs/adr-0028/G0-lots-DETTES.md, ajout GF-0 ;
adjudication de l'orchestrateur du 2026-10-10). Bibliothèque standard seule (R-8), Python 3.10 à 3.13.
Usage : python3 -I -B scripts/controle/avant_acte.py [--depot D] <sous-commande> [options] ; sortie 0 conforme, 1 refus
(une ligne REFUS <code> : <raison> ; à faire : <geste> par faute), 3 erreur (argument, fichier absent, git en erreur,
chemin interdit jamais ouvert) ; jamais 0 sur une erreur. Chaque passage ajoute au journal <git-path
shogen-garde>/journal.tsv (non versionné) une ligne par refus, avertissement ou contournement, ou une ligne conforme :
heure lue par date -u, sous-commande, code, niveau, contourne (moyen du contournement, sinon -) ; il mesure les refus
et les faux refus (avis b.5 adopté).
GF-5 : sceller, derrière la vérification complète (verif && sceller) : sha256 de HEAD et de l'arbre de l'index (git
write-tree), ou de HEAD^{tree} avec --tete ; refusé si un chemin diffère hors de l'index ou n'est pas suivi (LA-N05 :
pièce retouchée après la vérification). Le sceau est exigé par commit (GF-5b)."""
import argparse
import hashlib
import importlib.util
import os
import subprocess
import sys


def _module(nom):
    """Module frère chargé par son chemin : sous -I, le dossier du script n'est pas dans sys.path."""
    spec = importlib.util.spec_from_file_location(nom, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                    nom + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


GC = _module("garde_commun")


class Erreur(Exception):
    """Erreur de l'outil : sortie 3, jamais un refus."""


def git(depot, *args):
    p = subprocess.run(["git", "-C", depot, "-c", "core.quotePath=false", *args], capture_output=True, text=True)
    if p.returncode:
        raise Erreur(f"git {args[0]} : sortie {p.returncode}")
    return p.stdout


def garde(depot, *sous):
    """Dossier non versionné de l'état local (sceaux, journal), créé au besoin."""
    d = os.path.join(depot, git(depot, "rev-parse", "--git-path", "shogen-garde").strip(), *sous)
    os.makedirs(d, exist_ok=True)
    return d


def cle(depot, tete=False):
    """Clé du sceau : sha256 de HEAD et de l'arbre de l'index (git write-tree), ou de HEAD^{tree} avec --tete."""
    h = git(depot, "rev-parse", "--verify", "HEAD").strip()
    arbre = git(depot, *(["rev-parse", "HEAD^{tree}"] if tete else ["write-tree"])).strip()
    return hashlib.sha256(f"{'tete' if tete else 'index'} {h} {arbre}".encode()).hexdigest()


def sceller(a, fautes):
    etat = [x for x in git(a.depot, "status", "--porcelain", "--untracked-files=all").split(chr(10)) if x]
    hors = [x for x in etat if x[1] != " " or (a.tete and x[0] != " ")]
    if hors:
        fautes.append(("refus", "S1", f"{len(hors)} chemin(s) hors de l'index ou non suivi(s) (--tete : non commis)",
                       "indexer ou retirer, relancer la vérification complète, puis sceller", "-"))
        return
    with open(os.path.join(garde(a.depot, "sceaux"), cle(a.depot, a.tete)), "w", encoding="utf-8") as f:
        f.write(GC.maintenant().strftime("%Y-%m-%dT%H:%M:%SZ") + chr(10))


COMMANDES = {"sceller": sceller}


def journal(a, fautes):
    try:
        d = garde(a.depot)
    except Erreur:
        return
    h = GC.maintenant().strftime("%Y-%m-%dT%H:%M:%SZ")
    lignes = [(code, niveau, c) for niveau, code, _r, _g, c in fautes] or [("-", "conforme", "-")]
    with open(os.path.join(d, "journal.tsv"), "a", encoding="utf-8") as f:
        f.writelines(chr(9).join([h, a.cmd, *x]) + chr(10) for x in lignes)


def main(argv=None):
    p = argparse.ArgumentParser(prog="avant_acte.py", description=__doc__.split(chr(10))[0])
    p.add_argument("--depot", default=".")
    sp = p.add_subparsers(dest="cmd", required=True)
    sp.add_parser("sceller").add_argument("--tete", action="store_true")
    try:
        a = p.parse_args(argv)
    except SystemExit as e:
        return 0 if e.code == 0 else 3
    fautes = []
    try:
        COMMANDES[a.cmd](a, fautes)
    except (Erreur, OSError, UnicodeDecodeError, ValueError) as e:
        print(f"ERREUR {a.cmd} : {e}", file=sys.stderr)
        return 3
    for niveau, code, raison, geste, _c in fautes:
        print(f"{niveau.upper()} {code} : {raison}" + (f" ; à faire : {geste}" if geste else ""))
    journal(a, fautes)
    return 1 if any(f[0] == "refus" for f in fautes) else 0


if __name__ == "__main__":
    sys.exit(main())
