"""Shōgen, lot DETTES-T5 (2026-10-09 ; SHOGEN-CI-RUNNERS-1, ADR-0028 annexe B l.80 et l.822-824 ; adjudication Q-2 du
2026-10-09) : aucune image de runner flottante. Dans chaque workflow (.github/workflows/*.yml et *.yaml, premier niveau
seul, comme la forge), toute valeur d'une clé `runs-on` ou `os` (matrice, `include`, entrée d'action), ou d'une clé de
matrice qu'une valeur `runs-on` nomme (`${{ matrix.<clé> }}`), qui porte un libellé en `-latest` (casse ignorée) est
refusée : forme en ligne, entre guillemets, en liste ou en mapping de flux (clé JSON collée à sa valeur comprise), ou
sur les lignes plus indentées qui suivent une clé sans valeur, une ancre ou une étiquette seule, un en-tête de scalaire
de bloc (`|`, `>`) ou un flux ouvert ; après une clé sans valeur, aussi la suite `-` écrite au retrait de la clé
(relecture G2 du lot, C-1). Les commentaires (`#` en tête ou après une espace, hors guillemets) ne comptent pas.
Lecture par lignes, bibliothèque standard seule (R-8), sans analyseur YAML : refus en plus possibles (une ligne
`os: …-latest` dans un bloc `run:` qui suit une clé lue), jamais un refus en moins sur ces formes. Limites : ancre et
alias, clé de fusion `<<` ; échappement dans un scalaire entre guillemets doubles (hexadécimal, unicode, fin de ligne
échappée) ; clé explicite (`? runs-on`) ; suite d'un flux moins indentée que sa clé (refusée par YAML 1.2) ; libellé
posé par une variable ou par une expression `${{ }}` autre que `matrix.<clé>`.
Usage : python3 -B runners-epingles.py <racine> ; sortie 0 conforme, 1 refus (motifs sur stderr), 3 erreur, toute
exception comprise (une erreur n'est jamais un refus)."""
import glob
import os
import re
import sys

FLOTTANT = re.compile(r"[A-Za-z0-9_.-]*-latest(?![A-Za-z0-9_.])[A-Za-z0-9_.-]*", re.IGNORECASE)
MATRICE = re.compile(r"matrix\s*\.\s*([A-Za-z_][A-Za-z0-9_-]*)", re.IGNORECASE)   # ${{ matrix.<clé> }} d'un runs-on
VIDE = re.compile(r"\s*(?:[&!]\S*\s*)*")                    # valeur absente, ou ancre et étiquette seules
BLOC = re.compile(r"\s*(?:[&!]\S*\s*)*[|>][-+0-9]*\s*")     # en-tête de scalaire de bloc


def cle(noms) -> re.Pattern:
    """Clé de `noms` (casse ignorée), entre guillemets ou non, suivie de « : », collé à sa valeur compris (clé JSON)."""
    return re.compile(r"""(?:^|[\s{,\[])["']?(""" + "|".join(sorted(map(re.escape, noms))) + r""")["']?[ \t]*:""",
                      re.IGNORECASE)


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


def retrait(ligne: str) -> int:
    return len(ligne) - len(ligne.lstrip(" "))


def valeurs(lignes: list, motif: re.Pattern):
    """Pour chaque clé lue : [(indice de ligne, texte)] de sa valeur, sur la ligne de la clé, puis, si elle est sans
    valeur, ancre ou étiquette seule, en-tête de scalaire de bloc ou flux ouvert, sur les lignes plus indentées que la
    ligne de la clé qui la suivent et, après une clé sans valeur, sur les lignes `-` écrites à son retrait."""
    for i, ligne in enumerate(lignes):
        for m in motif.finditer(ligne):
            valeur, r = ligne[m.end():], retrait(ligne)
            vide = VIDE.fullmatch(valeur) is not None
            ouvert = valeur.count("[") + valeur.count("{") - valeur.count("]") - valeur.count("}") > 0
            pieces = [(i, valeur)]
            if vide or ouvert or BLOC.fullmatch(valeur):
                for j in range(i + 1, len(lignes)):
                    s = lignes[j]
                    if s.strip() and (retrait(s) < r or retrait(s) == r and not (
                            vide and s.lstrip(" ").startswith("-"))):
                        break
                    pieces.append((j, s))
            yield pieces


def refus(texte: str) -> tuple:
    """(motifs « ligne : jeton », nombre de clés lues) pour le texte d'un workflow : clés runs-on et os, et clés de
    matrice qu'une valeur runs-on nomme."""
    lignes = [code(x) for x in texte.split(chr(10))]
    noms = {"runs-on", "os"} | {k for v in valeurs(lignes, cle({"runs-on"})) for _i, t in v for k in MATRICE.findall(t)}
    motifs, n = [], 0
    for v in valeurs(lignes, cle(noms)):
        n += 1
        motifs += [f"{i + 1} : {t}" for i, s in v for t in FLOTTANT.findall(s)]
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
