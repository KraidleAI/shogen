"""Shōgen, lot DETTES-T5, DT5-8 (2026-10-09 ; adjudication C-2 : DT4-a avait rendu gates.yml illisible pour la
forge, un « : » dans un nom d'étape en scalaire simple, sans qu'aucune gate le voie) : chaque workflow (fichier
de .github/workflows dont le nom, plié en casse, finit par .yml ou .yaml, fichiers cachés compris, premier niveau
seul ; toute autre entrée nommée à la sortie, non lue : adjudication C-10) se charge avec PyYAML (paquet
python3-yaml de la distribution, contrôle R-8 dans docs/R-8-outillage.md) en un seul document qui est un mapping,
sans clé répétée à aucun niveau. Refus : erreur de lecture (ligne et colonne), clé répétée, document vide ou
autre qu'un mapping, octets hors UTF-8, aucun workflow ; et (relecture G2 du lot, C-8) tout libellé en -latest
(casse ignorée) dans la valeur lue de `runs-on` ou de `strategy.matrix` d'un job, ancres, alias, échappements et
clés explicites résolus : formes que runners-epingles.py, lecteur par lignes, ne voit pas. Refusées aussi
(contre-contrôle du lot) : toute étiquette explicite dont la valeur construite perd le texte du scalaire (`!!null`,
`!!bool`, `!!int`, `!!float`, `!!binary`, `!!timestamp`, `!!set`, `!!omap`, `!!pairs` : un libellé -latest y
deviendrait invisible), et toute clé de fusion `<<` (le lecteur construit chaque clé avant la fusion ; PyYAML n'a
pas de constructeur pour l'étiquette merge).
Limites : PyYAML lit le YAML 1.1, la forge son propre analyseur ; un fichier admis ici peut encore être refusé par elle
(L-5). Sur la forge, ce contrôle ne voit pas l'illisibilité de gates.yml lui-même, qui empêche le job g1 de démarrer :
elle ne paraît que comme un run du workflow gates en échec sans job, qui ne bloque la fusion que si les contrôles requis
de main nomment des jobs de gates.yml [inféré]. Le crochet pre-commit ne le lance pas (adjudication Q-4 : PyYAML n'est
pas exigé du poste) ; avant un commit, seule la chaîne de commits de l'orchestrateur le rejoue (procédure, non une
gate). Libellé posé par une variable, par une entrée (`with:` d'un workflow réutilisable, `inputs`) ou par une
expression `${{ }}`, matrice que pose une expression comprise : non lu (contre-contrôle du lot).
Usage : python3 -B workflows-yaml.py <racine> ; sortie 0 conforme, 1 refus (motifs sur stderr), 3 erreur (arguments,
racine sans .github/workflows, PyYAML absent, toute autre exception)."""
import os
import re
import sys

FLOTTANT = re.compile(r"-latest(?![A-Za-z0-9_.])", re.IGNORECASE)      # C-8 : forme de runners-epingles.py
PERTE = {"tag:yaml.org,2002:" + t for t in    # étiquettes explicites qui perdent le texte du scalaire
         ("null", "bool", "int", "float", "binary", "timestamp", "set", "omap", "pairs")}


def lecteur(yaml):
    """Chargeur sûr (SafeLoader) qui refuse toute clé répétée d'un mapping, à tout niveau, et toute étiquette
    explicite de PERTE (contre-contrôle du lot : la valeur construite, None, octets, ensemble ou paires, ne porterait
    plus le texte du libellé, qu'un alias cache aussi à runners-epingles.py)."""
    class Lecteur(yaml.SafeLoader):
        def compose_node(self, parent, index):
            e = self.peek_event()
            if getattr(e, "tag", None) in PERTE:
                raise yaml.composer.ComposerError(None, None, f"étiquette explicite refusée « {e.tag} »", e.start_mark)
            return super().compose_node(parent, index)

        def construct_mapping(self, noeud, deep=False):
            vues = set()
            for k, _v in noeud.value:
                cle = self.construct_object(k, deep=True)
                if cle in vues:
                    raise yaml.constructor.ConstructorError(None, None, f"clé répétée « {cle} »", k.start_mark)
                vues.add(cle)
            return super().construct_mapping(noeud, deep)
    return Lecteur


def chaines(x):
    """Chaînes d'une valeur lue (scalaire, éléments d'une liste, valeurs d'un mapping), à toute profondeur."""
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for v in x.values():
            yield from chaines(v)
    elif isinstance(x, list):
        for v in x:
            yield from chaines(v)


def flottants(doc: dict) -> list:
    """C-8 : libellés en -latest des valeurs lues de `runs-on` et de `strategy.matrix` de chaque job."""
    jobs = doc.get("jobs") if isinstance(doc.get("jobs"), dict) else {}
    vus = []
    for job in jobs.values():
        if isinstance(job, dict):
            strategie = job.get("strategy") if isinstance(job.get("strategy"), dict) else {}
            vus += [t for t in chaines([job.get("runs-on"), strategie.get("matrix")]) if FLOTTANT.search(t)]
    return vus


def refus(yaml, Lecteur, nom, octets):
    """Motif de refus du workflow `nom` (octets), None s'il est lisible et sans libellé flottant."""
    try:
        doc = yaml.load(octets.decode("utf-8"), Loader=Lecteur)
    except UnicodeDecodeError:
        return f"{nom} : octets hors UTF-8"
    except yaml.YAMLError as e:
        m = getattr(e, "problem_mark", None)
        ou = f"ligne {m.line + 1}, colonne {m.column + 1} : " if m else ""
        return f"{nom} : {ou}{getattr(e, 'problem', None) or e}"
    if not isinstance(doc, dict):
        return f"{nom} : document vide ou autre qu'un mapping"
    f = flottants(doc)
    return f"{nom} : image flottante (-latest) après lecture YAML : {', '.join(f)}" if f else None


def entrees(dossier: str) -> tuple:
    """Adjudication C-10 : (workflows lus, autres entrées) du dossier, noms triés : un fichier dont le nom, plié en
    casse, finit par .yml ou .yaml est lu, fichier caché compris ; toute autre entrée (fichier, dossier) est nommée,
    non lue."""
    lus, autres = [], []
    for x in sorted(os.listdir(dossier)):
        ok = os.path.isfile(os.path.join(dossier, x)) and x.casefold().endswith((".yml", ".yaml"))
        (lus if ok else autres).append(x)
    return lus, autres


def main(argv: list) -> int:
    try:
        dossier = os.path.join(argv[0], ".github", "workflows") if len(argv) == 1 else ""
        if not os.path.isdir(dossier):
            print(f"workflows-yaml : erreur : racine illisible {argv!r}", file=sys.stderr)
            return 3
        import yaml
        Lecteur, motifs = lecteur(yaml), []
        fichiers, autres = entrees(dossier)
        for nom in fichiers:
            with open(os.path.join(dossier, nom), "rb") as f:
                motifs.append(refus(yaml, Lecteur, nom, f.read()))
        motifs = [m for m in motifs if m] + ([] if fichiers else ["aucun workflow lu"])
    except Exception as e:
        print(f"workflows-yaml : erreur : {e!r}", file=sys.stderr)
        return 3
    for m in motifs:
        print(f"workflows-yaml : refus : {m}", file=sys.stderr)
    if not motifs:
        print(f"workflows-yaml : conforme ({len(fichiers)} workflow(s), PyYAML {yaml.__version__})")
    if autres:
        print(f"workflows-yaml : {len(autres)} autre(s) entrée(s) de .github/workflows non lue(s) : "
              f"{', '.join(autres)}")
    return 1 if motifs else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
