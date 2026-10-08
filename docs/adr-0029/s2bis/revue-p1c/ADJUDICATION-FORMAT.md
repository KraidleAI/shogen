# Adjudication de l'orchestrateur — lettres C-1 à C-5 au FORMAT des journaux de S2-bis (2026-10-05 10:01:36 UTC, heure lue)

Pièces de référence :
- G2 de RB-18 avec banc de concordance : `G2-RB18-transcrit.md` §4 et §6 ;
- avis de l'advisor : `AVIS-FORMAT.md`.

**L'avis est adopté en entier, lettres exactes comprises :**
- **C-1** : le fond est adopté et le code reste `JOURNAL/entier`.
- **C-2** : une seule définition d'« intègre » au §7.1, points (a) à (e) de l'avis. Tous les champs du §1.3 et du §2 sont typés ; un booléen n'est jamais un entier ; plus aucune « limite déclarée ». Le point `ws` null est vérifié type par type (R-2).
- **C-3** : adoptée, avec deux précisions :
  - la liste `queue` suit l'ordre croissant (jour, k) ; le FORMAT dit que l'écrivain l'écrit dans cet ordre, et un test de l'écrivain à deux queues le fixe (R-1) ;
  - une phrase est ajoutée à SHOGEN-S2BIS-RUPTURE-PORTEE-1.
- **C-4** : N = 64, avec la racine au niveau 1.
  - Le refus a lieu à l'écriture et dans `_lire`, sous le code `JOURNAL/imbrication`.
  - Les lecteurs comptent les niveaux eux-mêmes et ne se fient pas à `RecursionError`.
  - La profondeur réelle maximale M est mesurée au bout en bout et écrite.
- **C-5** :
  - le numéro k suit la grammaire `0|[1-9][0-9]*` ;
  - un nom du préfixe qui n'est pas conforme est un refus nommé chez les lecteurs, et `JOURNAL/nom` chez l'écrivain ;
  - un dossier vide est un refus nommé ;
  - **pas de numéros sur 3 chiffres** ; l'ordre des fichiers est (jour, k entier).

**Ordre** :
1. Le lot P1 tranche C, en correction, porte seul le FORMAT et l'écrivain. Il est commis d'abord.
2. RB-1 et RB-18 sont ensuite corrigés en parallèle sur la tête qui suit P1-C, d'après la lettre seule. RB-18 ne lit ni `lecteur.py` ni la contre-épreuve.
3. Le banc est rejoué en 3.10 et en 3.12, avec des familles régénérées par l'écrivain corrigé. Critère : 0 discordance.
4. Le banc est versé (N-3).
