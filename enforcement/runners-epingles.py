"""Shōgen, lot DETTES-T5 (2026-10-09 ; SHOGEN-CI-RUNNERS-1, ADR-0028 annexe B l.80 et l.822-824 ; adjudication Q-2 du
2026-10-09) : aucune image de runner flottante. Dans chaque workflow (.github/workflows/*.yml et *.yaml, premier niveau
seul, comme la forge), toute valeur d'une clé `runs-on` ou `os` (matrice, `include`, entrée d'action) qui porte un
libellé en `-latest` est refusée : forme en ligne, entre guillemets, en liste ou en mapping de flux, ou en bloc (lignes
plus indentées qui suivent la clé, et suite d'un flux ouvert). Les commentaires (`#` en tête ou après une espace, hors
guillemets) ne comptent pas. Lecture par lignes, bibliothèque standard seule (R-8), sans analyseur YAML : refus en plus
possibles (une ligne `os: …-latest` dans un bloc `run:` qui suit une clé lue), jamais un refus en moins sur ces formes.
Limites : ancre et alias YAML, libellé posé par une variable ou une expression `${{ }}` autre que la matrice.
Usage : python3 -B runners-epingles.py <racine> ; sortie 0 conforme, 1 refus (motifs sur stderr), 3 erreur, toute
exception comprise (une erreur n'est jamais un refus)."""
import glob
import os
import re
import sys

CLE = re.compile(r"""(?:^|[\s{,\[])["']?(runs-on|os)["']?[ \t]*:(?=\s|$)""")
FLOTTANT = re.compile(r"[A-Za-z0-9_.-]*-latest(?![A-Za-z0-9_.])[A-Za-z0-9_.-]*")


def code(ligne: str) -> str:
    """La ligne sans son commentaire : `#` en tête ou après une espace, hors guillemets."""
    q = ""
    for i, c in enumerate(ligne):
        if q:
            q = "" if c == q else q
        elif c in "'\"":
            q = c
        elif c == "#" and (i == 0 or ligne[i - 1] in " \t"):
            return ligne[:i]
    return ligne


def refus(texte: str) -> tuple:
    """(motifs « ligne : jeton », nombre de clés lues) pour le texte d'un workflow."""
    lignes = [code(x) for x in texte.split(chr(10))]
    motifs, n = [], 0
    for i, ligne in enumerate(lignes):
        for m in CLE.finditer(ligne):
            n += 1
            valeur = ligne[m.end():]
            motifs += [f"{i + 1} : {t}" for t in FLOTTANT.findall(valeur)]
            ouvert = valeur.count("[") + valeur.count("{") - valeur.count("]") - valeur.count("}")
            if valeur.strip() and ouvert <= 0:
                continue
            retrait = len(ligne) - len(ligne.lstrip(" "))
            for j in range(i + 1, len(lignes)):
                suite = lignes[j]
                if suite.strip() and len(suite) - len(suite.lstrip(" ")) <= retrait:
                    break
                motifs += [f"{j + 1} : {t}" for t in FLOTTANT.findall(suite)]
    return list(dict.fromkeys(motifs)), n          # une ligne lue deux fois (clé dans un bloc) n'est dite qu'une fois


def main(argv: list) -> int:
    try:
        if len(argv) != 1 or not os.path.isdir(os.path.join(argv[0], ".github", "workflows")):
            print(f"runners-epingles : erreur : racine illisible {argv!r}", file=sys.stderr)
            return 3
        dossier = os.path.join(argv[0], ".github", "workflows")
        fichiers = sorted(glob.glob(os.path.join(dossier, "*.yml")) + glob.glob(os.path.join(dossier, "*.yaml")))
        motifs, cles = [], 0
        for chemin in fichiers:
            with open(chemin, encoding="utf-8") as f:
                m, n = refus(f.read())
            motifs += [f".github/workflows/{os.path.basename(chemin)}:{x}" for x in m]
            cles += n
    except Exception as e:
        print(f"runners-epingles : erreur : {e}", file=sys.stderr)
        return 3
    for m in motifs:
        print(f"runners-epingles : refus : image flottante (-latest) : {m}", file=sys.stderr)
    if not motifs:
        print(f"runners-epingles : conforme ({len(fichiers)} workflow(s), {cles} clé(s) runs-on/os lues)")
    return 1 if motifs else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
