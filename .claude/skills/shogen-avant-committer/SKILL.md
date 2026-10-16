---
name: shogen-avant-committer
description: >-
  Garde-fous de Shōgen à appliquer à la réception d'un diff de worker, avant
  tout git commit et avant tout versement de pièces au dépôt : les commandes
  à passer (diff, sceau, commit, versement) et le moment où les passer.
---

# Avant de committer ou de verser

Erreurs visées : E1, E8, E9, E10, E13, E14, E16, E21, E28, LA-N04, LA-N05 (liste de l'orchestrateur, lot GARDE-FOUS-ORCH).

1. Diff reçu d'un worker, avant de lancer la G2 :
   `python3 -I -B scripts/controle/avant_acte.py diff --fichier <x.diff>` ; sortie 1 : le diff retourne au worker.
2. Message de commit : un fichier écrit après la dernière retouche de l'adjudication relue, avec une ligne
   `Source-Sha: <sha256>` par source (`sha256sum <source>`) et la ligne `Diff-Id: <id>`.
3. Vérification complète puis sceau, d'une seule commande :
   `<vérification> && python3 -I -B scripts/controle/avant_acte.py sceller`.
4. Commit : `git diff --cached --stat` (index relu, que le crochet GARDE-FAITS du dépôt exige avant tout commit),
   puis `python3 -I -B scripts/controle/avant_acte.py commit --message <m> --source <adjudication> --diff <d>
   --id <id> && git commit -q -F <m>`. Un décalage voulu d'un fichier cité s'écrit au message :
   `Décalage admis : <chemin>` (journalisé en contournement).
5. Versement, avant `xtask` : `SHA256SUMS` écrit depuis le dossier des pièces (`sha256sum <pièces>`), puis
   `python3 -I -B scripts/controle/avant_acte.py verser --pieces <dossier>` ; sortie 0 seulement. Un octet copié dans
   `biblio/` porte sa rangée d'INDEX et le compte remesuré dans le même diff (V6) ; rien ne se verse ni ne se copie
   dans `biblio/` pendant qu'une chaîne tourne (V7).
6. Un fichier seul, pour S-G5 : `python3 -I -B scripts/controle/presg5.py . <fichier.md>`.
