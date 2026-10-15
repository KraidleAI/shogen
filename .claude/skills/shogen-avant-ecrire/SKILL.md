---
name: shogen-avant-ecrire
description: >-
  Garde-fous de Shōgen à appliquer avant d'écrire une heure, une citation,
  une absence de fichier ou un renvoi par numéro de ligne, dans un document,
  un brief, un message de commit ou une réponse : les commandes à passer.
---

# Avant d'écrire une date ou un fait

Erreurs visées : E7, E14, E15, E16, E21 (liste de l'orchestrateur, lot GARDE-FOUS-ORCH).

1. Heure : `date -u` juste avant de l'écrire ; un script qui écrit une heure la lit lui-même par `date -u`.
2. Absence d'un fichier : `python3 -I -B scripts/controle/avant_acte.py existe <nom>` ; sortie 1 seulement : absent.
3. Document écrit à la main, avant de le rendre ou de le verser :
   `python3 -I -B scripts/controle/avant_acte.py publier --texte <f>` (heures, citations, secrets, chemins).
4. Citation contrôlable : forme `« … » (chemin:N)`, chemin depuis la racine du dépôt, ligne relue.
5. Fichier cité par numéro de ligne : la liste est `scripts/controle/garde/lignes-citees.txt` ; `diff` et `commit`
   de `scripts/controle/avant_acte.py` refusent un bloc qui en décale une ligne.
