"""Lot PRODUIT-R2, R2-c (ADR-0028 §4 pt 7, D9 ; AVIS-PRODUIT-APRES-S2 §3) : contrôle d'un rapport écrit depuis un
gabarit de docs/publication/gabarits/ (champ <type.nom>). Refuse : (1) une locution de doc 09 dans tout le texte (MOTS,
ancrées à leur ligne de doc 09, relue à chaque lancement : ancre absente, erreur 3) ; (2) un texte fixe changé, des
champs ni tous vides ni tous remplis, un champ à deux valeurs ; (3) un nombre sans empreinte : sha256, commit, date,
version de forme fausse ; <p.nom> avec un champ sha256.p : nombres attribués à cette empreinte ; autre champ : toute
ligne à chiffre cite [sha256.x] ou [sha256.x l.N] d'un champ du gabarit ; (4) R1 dans un champ libre. Non mécanisés :
doc 09 l.41, le contexte, l'égalité d'une valeur à sa pièce. Usage : <gabarit> <rapport> [--doc09 D] ; 0, 1 refus, 3."""
import os               # garde en tête (SHOGEN-S2BIS-GARDE-EN-TETE-1) : le dossier du script quitte sys.path
import sys
if sys.path and os.path.realpath(sys.path[0]) == os.path.dirname(os.path.realpath(__file__)):
    del sys.path[0]
if "SHOGEN_S2_CAMPAGNE_CONTROL" in os.environ:
    sys.stderr.write("variable scellée posée : refus (annexe D.4 a)\n")
    sys.exit(3)
import pathlib
import re

DOC09 = str(pathlib.Path(__file__).resolve().parents[2] / "docs" / "09-vocabulaire.md")
CHAMP = re.compile(r"<([a-z][a-z0-9-]*)\.([a-z0-9-]+)>")
REF = re.compile(r"\[sha256\.([a-z0-9-]+)(?: l\.\d+(?:-\d+)?)?\]")
FORMES = {"sha256": "[0-9a-f]{64}", "commit": "[0-9a-f]{40}", "date": r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ",
          "version": r"\d+\.\d+\.\d+"}
MOTS = (    # (ligne de doc 09, ancre lue à cette ligne, motif cherché sans casse, borné par des non-mots)
    (11, "*verified, validated", r"verified|validated|guaranteed|ensures?|safe|validée?s?"),
    (14, "« donnée vérifiée »", r"vérifiée?s?"), (20, "**diverses**", r"diverses?"),
    (21, "**indépendantes**", r"indépendante?s?|independent"),
    (22, "**garantit**", r"garanti(?:e|es|s|t|ssent)?|guarantees?"),
    (23, "**fait signé**", r"faits? signés?|signed facts?"),
    (24, "donnée **vraie**", r"donnée?s? vraies?|prix corrects?|dit vrai|true (?:price|data)|correct price"),
    (25, "sécurité du lot", r"niveau de sécurité|security level"), (26, "« k sources »", r"(?:k|\d+) sources"),
    (27, "**prouve** l'absence", r"prouve(?:nt)?|proves?"),
    (28, "ne mesure", r"personne ne mesure|(?:nobody|no one) measures"),
    (29, "**imposée**", r"diversité imposée|(?:imposed|enforced) diversity"),
    (30, "sont bonnes", r"qualité d'une source|nos sources sont bonnes|quality of a source|our sources are"),
    (31, "décentralisé", r"décentralisée?s?|decentrali[sz]ed"), (37, "est **sûr** parce", r"sûre?s?"),
    (38, "paniquer", r"ne peut pas paniquer|cannot panic"), (39, "élevée", r"couverture élevée|high coverage"),
    (42, "build **reproductible**", r"reproductibles?|reproducible"), (43, "**sécurisée**", r"sécurisée?s?|secured?"),
    (44, "SLSA niveau", r"SLSA (?:niveau|level)"), (45, "verte **donc**", r"verte donc|green,? (?:so|therefore|hence)"),
    (51, "publiquement", r"publiquement vérifiable|publicly verifiable"),
    (53, "trustless", r"trustless|transport sans confiance"), (54, "normalisé", r"subject normalisé|normalise l'URL"),
    (55, "deux ressources", r"donc deux ressources"),
)


def mots(texte: str, doc09: str) -> list:
    registre = pathlib.Path(doc09).read_bytes().decode("utf-8").split("\n")
    for ligne, ancre, _ in MOTS:
        if ligne > len(registre) or ancre not in registre[ligne - 1]:
            raise ValueError(f"doc 09 l.{ligne} ne porte plus {ancre!r} : liste MOTS à relire")
    return [f"l.{i} : locution (doc 09 l.{ligne}) : {m.group(0)!r}" for i, x in enumerate(texte.split("\n"), 1)
            for ligne, _, motif in MOTS for m in [re.search(rf"(?<!\w)(?:{motif})(?!\w)", x, re.I)] if m]


def valeurs(gabarit: str, rapport: str):
    p = CHAMP.split(gabarit)
    lits, noms = p[0::3], [f"{a}.{b}" for a, b in zip(p[1::3], p[2::3])]
    if not noms or "" in lits[1:-1]:
        raise ValueError("gabarit sans champ, ou deux champs contigus")
    if not rapport.startswith(lits[0]):
        return "texte fixe changé avant le premier champ"
    pos, vals = len(lits[0]), []
    for nom, lit in zip(noms, lits[1:]):
        j = rapport.find(lit, pos) if lit else len(rapport)
        if j < 0:
            return f"texte fixe changé ou absent après <{nom}>"
        vals, pos = vals + [(nom, rapport[pos:j])], j + len(lit)
    return vals if pos == len(rapport) else "texte en trop en fin de rapport"


def controler(gabarit: str, rapport: str, doc09: str = DOC09) -> list:
    motifs, vals = mots(rapport, doc09), valeurs(gabarit, rapport)
    if isinstance(vals, str):
        return motifs + [vals]
    vides, pleins = sorted({n for n, v in vals if v == f"<{n}>"}), [n for n, v in vals if v != f"<{n}>"]
    if vides:      # occurrences, non noms : un champ répété rempli une seule fois n'est pas vide (G2, C-1)
        return motifs + ([] if not pleins else [f"champs ni tous remplis ni tous vides ; vides : {vides}"])
    empreintes, d = {n.split(".", 1)[1] for n, _ in vals if n.startswith("sha256.")}, {}
    for n, v in vals:
        genre = n.split(".", 1)[0]
        if d.setdefault(n, v) != v:
            motifs.append(f"<{n}> : deux valeurs")
        if not v.strip():
            motifs.append(f"<{n}> : valeur vide")
        if genre == "libre" and re.search(r"(?<!\w)R1(?!\w)", v):
            motifs.append(f"<{n}> : prétention R1 (aucune avant le rendu de S2-bis)")
        if genre in FORMES and not re.fullmatch(FORMES[genre], v):
            motifs.append(f"<{n}> : forme {genre} attendue")
        elif genre not in FORMES and genre not in empreintes:
            motifs += [f"<{n}> : nombre sans empreinte : {x.strip()[:80]!r}" for x in v.split("\n")
                       if re.search(r"\d", x) and not set(REF.findall(x)) & empreintes]
            motifs += [f"<{n}> : empreinte inconnue [sha256.{r}]" for r in REF.findall(v) if r not in empreintes]
    return motifs


def main(argv: list) -> int:
    try:
        if len(argv) not in (2, 4) or argv[2:3] not in ([], ["--doc09"]):
            raise ValueError("usage : gabarit_controle.py <gabarit> <rapport> [--doc09 D]")
        motifs = controler(*(pathlib.Path(c).read_bytes().decode("utf-8") for c in argv[:2]), *argv[3:])
    except (OSError, UnicodeDecodeError, ValueError) as e:
        sys.stderr.write(f"erreur : {e}\n")
        return 3
    sys.stderr.write("".join(m + "\n" for m in motifs))
    print("refus" if motifs else "conforme")
    return 1 if motifs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
