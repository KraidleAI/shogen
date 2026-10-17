---
name: shogen-avant-lancer
description: >-
  Garde-fous de Shōgen à appliquer avant de lancer un agent, un workflow,
  une chaîne de commits ou une tâche longue : les commandes à passer et le
  moment où les passer. Les règles elles-mêmes vivent dans le bloc commun
  des fiches et dans scripts/controle/README.md.
---

# Avant de lancer

Erreurs visées : E3, E4, E6, E11, E18, E22, E23, E24, E25, E30, E31, E36 (liste de l'orchestrateur, lot GARDE-FOUS-ORCH).

1. Avant tout lancement : `python3 -I -B scripts/controle/avant_acte.py --depot <dépôt> disque` (système de
   fichiers du dépôt, et de TMPDIR s'il diffère ; jamais `/`, E4). Sortie 1 :
   `python3 -I -B scripts/controle/avant_acte.py disque --lister <dossier du scratchpad>`, supprimer les cibles
   cargo des lots clos, relancer le contrôle.
2. Chaîne de commits : copier `scripts/controle/gabarits/chaine.sh` ; une ligne de plan par commit ; rapport du
   contre-contrôle écrit sur `scripts/controle/gabarits/rapport-cc.md` (ligne `GROUPES :`). Puis
   `python3 -I -B scripts/controle/avant_acte.py chaine --plan <plan> --cc <rapport> --duree-pas <minutes>`, avec la
   durée mesurée d'un pas ; sortie 1 : regrouper les pas, ou lancer détaché comme le refus l'écrit. À blanc, avant
   le lancement : `python3 -I -B scripts/controle/avant_acte.py chaine --blanc --script <chaîne.sh> --plan <plan>
   --cc <rapport>` (chaîne sans plan : `--diffs <d1> <d2>…`, dans l'ordre) ; sortie 1 : corriger, ne pas lancer.
3. Lancement de la chaîne : `DETACHE=1 setsid nohup timeout <secondes> bash chaine.sh > chaine.log 2>&1 &`, PID et
   journal consignés ; attente dans un appel séparé, par la notification de fin ou par sondage du PID.
4. Toute autre tâche de fond : délai explicite dans l'appel ; au-delà de 100 min estimées, lancement détaché.
5. Brief d'un agent : l'écrire dans un fichier `BRIEF*.md`, puis
   `python3 -I -B scripts/controle/avant_acte.py brief --texte <brief> --fiche <fiche>` ; sortie 1 : corriger le brief
   (item fermé, constat sans fichier ni ligne, nom absent, règle git) ; le crochet GARDE-FAITS (R11) rejoue ce contrôle
   quand la consigne de l'agent nomme le fichier.
