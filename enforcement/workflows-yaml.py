"""Shōgen, lot DETTES-T5, DT5-8 (2026-10-09 ; adjudication C-2 : DT4-a avait rendu gates.yml illisible pour la forge, un
« : » dans un nom d'étape en scalaire simple, sans qu'aucune gate le voie) : chaque workflow (.github/workflows/*.yml et
*.yaml, premier niveau seul, comme la forge) se charge avec PyYAML (paquet python3-yaml de la distribution, contrôle
R-8 dans docs/R-8-outillage.md) en un seul document qui est un mapping, sans clé répétée à aucun niveau. Refus : erreur
de lecture (ligne et colonne), clé répétée, document vide ou autre qu'un mapping, octets hors UTF-8, aucun workflow.
Limite : PyYAML lit le YAML 1.1, la forge son propre analyseur ; un fichier admis ici peut encore être refusé par elle.
Usage : python3 -B workflows-yaml.py <racine> ; sortie 0 conforme, 1 refus (motifs sur stderr), 3 erreur (arguments,
racine sans .github/workflows, PyYAML absent, toute autre exception)."""
import glob
import os
import sys


def lecteur(yaml):
    """Chargeur sûr (SafeLoader) qui refuse toute clé répétée d'un mapping, à tout niveau."""
    class Lecteur(yaml.SafeLoader):
        def construct_mapping(self, noeud, deep=False):
            vues = set()
            for k, _v in noeud.value:
                cle = self.construct_object(k, deep=True)
                if cle in vues:
                    raise yaml.constructor.ConstructorError(None, None, f"clé répétée « {cle} »", k.start_mark)
                vues.add(cle)
            return super().construct_mapping(noeud, deep)
    return Lecteur


def refus(yaml, Lecteur, nom, octets):
    """Motif de refus du workflow `nom` (octets), None s'il est lisible."""
    try:
        doc = yaml.load(octets.decode("utf-8"), Loader=Lecteur)
    except UnicodeDecodeError:
        return f"{nom} : octets hors UTF-8"
    except yaml.YAMLError as e:
        m = getattr(e, "problem_mark", None)
        ou = f"ligne {m.line + 1}, colonne {m.column + 1} : " if m else ""
        return f"{nom} : {ou}{getattr(e, 'problem', None) or e}"
    return None if isinstance(doc, dict) else f"{nom} : document vide ou autre qu'un mapping"


def main(argv: list) -> int:
    try:
        dossier = os.path.join(argv[0], ".github", "workflows") if len(argv) == 1 else ""
        if not os.path.isdir(dossier):
            print(f"workflows-yaml : erreur : racine illisible {argv!r}", file=sys.stderr)
            return 3
        import yaml
        Lecteur, motifs = lecteur(yaml), []
        fichiers = sorted(glob.glob(os.path.join(dossier, "*.yml")) + glob.glob(os.path.join(dossier, "*.yaml")))
        for chemin in fichiers:
            with open(chemin, "rb") as f:
                motifs.append(refus(yaml, Lecteur, os.path.basename(chemin), f.read()))
        motifs = [m for m in motifs if m] + ([] if fichiers else ["aucun workflow lu"])
    except Exception as e:
        print(f"workflows-yaml : erreur : {e!r}", file=sys.stderr)
        return 3
    for m in motifs:
        print(f"workflows-yaml : refus : {m}", file=sys.stderr)
    if not motifs:
        print(f"workflows-yaml : conforme ({len(fichiers)} workflow(s), PyYAML {yaml.__version__})")
    return 1 if motifs else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
