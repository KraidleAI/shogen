---
name: shogen-avant-pousser
description: >-
  Garde-fous de Shōgen à appliquer avant tout git push, toute PR, tout
  commentaire public, toute page pour l'investisseur et tout acte sur la
  forge (branche, protection, réglages) : les commandes à passer et le moment.
---

# Avant de pousser ou de publier

Erreurs visées : E1, E2, E14, E17, E20, LA-N01, LA-N05 (liste de l'orchestrateur, lot GARDE-FOUS-ORCH).

1. Tête vérifiée puis scellée : `<vérification de la tête> && python3 -I -B scripts/controle/avant_acte.py sceller
   --tete`.
2. Poussée : `git log --oneline origin/<b>..HEAD` (ce qui part, lu, que le crochet GARDE-FAITS exige ; branche
   neuve : `git status --short`), puis `python3 -I -B scripts/controle/avant_acte.py pousser --distant origin
   --branche <b> && git push origin <b>`. Les chemins qui ne partent jamais et les actes déjà refusés par le
   mandataire sont dans `scripts/controle/garde/hors-distant.txt`.
3. Tout autre acte sur la forge, avant de le tenter : `git status --short` (le crochet prend le texte d'un acte
   `git push` pour une poussée), puis `python3 -I -B scripts/controle/avant_acte.py pousser --acte "<commande>"` ;
   sortie 1 : l'acte passe à l'investisseur, décrit pas à pas.
4. Texte publié : écrit dans un fichier, puis `python3 -I -B scripts/controle/avant_acte.py publier --texte <f>` ;
   publication sur une sortie 0 seulement.
