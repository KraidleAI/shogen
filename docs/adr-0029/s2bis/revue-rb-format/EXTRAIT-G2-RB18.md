# Extrait de la relecture G2 de RB-18 (§6, partie RB-18), remis au worker des corrections de RB-18

> Extrait par l'orchestrateur ; lignes 203 à 223 de `s2bis/rb18/g2/G2-RB18-transcrit.md`, sans retouche. Les lettres C-1 à C-5 du FORMAT sont commises à la tête (P1 tranche C) : la source est le FORMAT de la tête, non le texte de la relecture.

### RB-18

Corrections à écrire d'après la lettre seule, sans lire `lecteur.py` ni ma contre-épreuve, en diffs RB-18e et suivants sur `f5915a5`.
- **C-6** : défaut E11 ; `queue` qui n'est ni une liste ni null → déclaration fausse.
- **C-7** : C-1 ; entier long → ligne non intègre.
- **C-8** : C-5 ; grammaire des noms ; refus quand il n'y a aucun fichier.
- **C-9** : C-2 ; champs propres typés.
- **C-10** : C-3 ; déclaration exacte, toutes les queues rendues avec la rupture.
- **C-11** : C-4 ; borne d'imbrication.
- **C-12** : tests, chacun avec son rouge montré :
  - G-07 : reprise en tête de segment au lien faux ;
  - G-08 : une reprise qui déclare deux queues, après deux pannes de l'écrivain réel ;
  - G-13 : sortie avec un caractère hors ASCII ;
  - G-14 : trois arguments → code 2 ;
  - les comportements de C-6 à C-11 ;
  - un test tracemalloc de `Lecture` sur des tailles 1 et 4 ;
  - le G1 corrigé : 392 lignes.
- **C-13** : recalage.
  - Ne plus créer `recalc/__init__.py` et ne plus toucher `REGLES` (règle déjà en tête, identique en contenu).
  - Plancher re-mesuré par `--egal` : 188 aujourd'hui, à refaire après C-6 à C-12.
  - Critère de sortie : le banc rejoué donne 0 discordance avec RB-1 corrigé (PROPOSITION l.551).

Tests vivants à fermer (§5 de la relecture) : G-07, G-08, G-13, G-14, comme listés en C-12.
