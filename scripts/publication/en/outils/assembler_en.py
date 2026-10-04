# -*- coding: utf-8 -*-
"""Assemblage de la traduction anglaise (lot DOCS11-EN) à partir des parties rédigées à la main.

Trois opérations mécaniques, et rien d'autre :
  1. concaténation des parties p1.md à p5.md, dans l'ordre ;
  2. chaque bloc « ```text / @@CODE@@ / ``` » est remplacé par le bloc de code de même rang de la source, recopié à
     l'octet (les sorties recopiées ne passent jamais par une saisie) ;
  3. les repères @@GLOSES@@ et @@TERMES@@ sont remplacés par les lignes des tables A et B, tirées du glossaire fixé
     (glossaire_en.py), pour que le glossaire final et les gloses du texte ne puissent pas diverger.

Aucune barre oblique inverse n'est écrite dans ce fichier.

Usage : python3 -B assembler_en.py SOURCE DOSSIER_DES_PARTIES SORTIE
"""
import importlib
import os
import sys

NL = chr(10)
REPERE_CODE = "```text" + NL + "@@CODE@@" + NL + "```"


def blocs_de_code(source):
    blocs, courant = [], None
    for ligne in source.split(NL):
        if ligne.startswith("```"):
            if courant is None:
                courant = [ligne]
            else:
                courant.append(ligne)
                blocs.append(NL.join(courant))
                courant = None
        elif courant is not None:
            courant.append(ligne)
    if courant is not None:
        raise SystemExit("bloc de code non fermé dans la source")
    return blocs


def main(argv):
    if len(argv) != 3:
        print("usage : assembler_en.py SOURCE DOSSIER_DES_PARTIES SORTIE")
        return 3
    source_chemin, parties, sortie = argv
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    g = importlib.import_module("glossaire_en")
    with open(source_chemin, encoding="utf-8") as f:
        source = f.read()
    texte = ""
    for nom in ("p1.md", "p2.md", "p3.md", "p4.md", "p5.md"):
        with open(os.path.join(parties, nom), encoding="utf-8") as f:
            texte += f.read()
    blocs = blocs_de_code(source)
    n = texte.count(REPERE_CODE)
    if n != len(blocs):
        print("repères de code : " + str(n) + ", blocs de la source : " + str(len(blocs)))
        return 1
    for bloc in blocs:
        texte = texte.replace(REPERE_CODE, bloc, 1)
    lignes_a = [("| " + forme + " | " + glose + " |") for _, forme, glose, _ in g.GLOSES]
    lignes_b = [("| " + fr + " | " + en + " | " + note + " |") for fr, en, note in g.TERMES]
    for repere, lignes in (("@@GLOSES@@", lignes_a), ("@@TERMES@@", lignes_b)):
        if texte.count(repere) != 1:
            print("repère " + repere + " absent ou répété")
            return 1
        texte = texte.replace(repere, NL.join(lignes))
    if "@@" in texte:
        print("repère non résolu")
        return 1
    with open(sortie, "w", encoding="utf-8") as f:
        f.write(texte)
    print("assemblé : " + sortie + " (" + str(len(blocs)) + " blocs de code recopiés, " + str(len(lignes_a))
          + " gloses, " + str(len(lignes_b)) + " termes)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
