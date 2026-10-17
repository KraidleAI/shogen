"""Gabarit de script de versement (GARDE-FOUS phase 3, groupe A ; SHOGEN-GARDE-RECALAGE-CHECK-1 ; erreurs E32, E33,
E35), à copier par versement, ACTES rempli. Contrat : racine du dépôt lue dans SHOGEN_DEPOT (défaut /home/user/shogen),
que `avant_acte.py verser --blanc --script <copie>` pose sur une copie creuse avant le versement réel ; toutes les
cibles sont lues et vérifiées avant la première écriture (E32 : jamais écrire puis vérifier) ; chaque ajout va en fin
de fichier (aucune ligne citée par numéro ne bouge). Sorties : 0 versé, 1 refus avant toute écriture (lignes REFUS)."""
import importlib.util
import os
import sys

DEPOT = os.environ.get("SHOGEN_DEPOT", "/home/user/shogen")
ACTES = []      # [(chemin relatif au dépôt, texte ajouté en fin, saut de ligne final compris)], à remplir


def commun():
    """garde_commun.py du dépôt visé (compte des cellules lu par la même fonction que avant_acte.py verser V9)."""
    chemin = os.path.join(DEPOT, "scripts", "controle", "garde_commun.py")
    m = importlib.util.module_from_spec(importlib.util.spec_from_file_location("garde_commun", chemin))
    m.__spec__.loader.exec_module(m)
    return m


def fautes(actes):
    """Refus de chaque acte, lus sur la cible avant toute écriture : chemin hors du dépôt, ajout sans saut de ligne
    final, cible sans saut de ligne final, rangée de tableau dont le compte de cellules diffère de l'en-tête (E32)."""
    gc, out = commun(), []
    for chemin, ajout in actes:
        cible = os.path.realpath(os.path.join(DEPOT, chemin))
        if not cible.startswith(os.path.realpath(DEPOT) + os.sep):
            out.append(f"{chemin} : hors du dépôt")
            continue
        avant = ""
        if os.path.isfile(cible):
            with open(cible, encoding="utf-8") as f:
                avant = f.read()
        if not ajout.endswith(chr(10)) or avant[-1:] not in ("", chr(10)):
            out.append(f"{chemin} : ajout ou cible sans saut de ligne final")
        lignes, n = (avant + ajout).split(chr(10)), avant.count(chr(10))
        for k, nb, tete in gc.rangees_fautives(lignes, range(n + 1, n + ajout.count(chr(10)) + 1)):
            out.append(f"{chemin}:{k} : {nb} cellules, en-tête de {tete} (E32)")
    return out


if __name__ == "__main__":
    refus = fautes(ACTES)
    for x in refus:
        print("REFUS " + x)
    if refus:
        sys.exit(1)
    for chemin, ajout in ACTES:
        os.makedirs(os.path.dirname(os.path.join(DEPOT, chemin)) or DEPOT, exist_ok=True)
        with open(os.path.join(DEPOT, chemin), "a", encoding="utf-8") as f:
            f.write(ajout)
    print(f"versé : {len(ACTES)} acte(s)")
