# Correction finale d'OUT-2j (C-1 de la revue de la vague 3) (transcrit)

> Transcription par l'orchestrateur le 2026-10-08 18:42:05 UTC du texte écrit par l'agent a3a8586c8cc52a289 dans `<scratchpad>/s2bis/outillage2/corr3/RAPPORT-CORRECTIONS.md` (sha256 43119ffe…) ; contrôle FM-1.1 de son transcript : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte de l'agent ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

## Correction finale du 2026-10-08 17:53 UTC (heure lue par `date -u`) : C-1 de la revue de la vague 3

**Gate 0 : `claude-opus-5-5`** (contexte système ; effort `max` selon la fiche, non mesurable de l'intérieur).
Horloge : de 17:40:02 à 17:54 UTC. Sources [lu] : `REVUE-transcrit.md` en entier ; `revue/remede/remede-J09.diff`
(`32eb0005…`) lu comme donnée ; `revue/mutants/spec_j.py`, pour reprendre la forme exacte de J09.

**Ce qui change (tests seuls)** : `test_drapeaux_de_l_environnement_rendus_aux_enfants_isoles` gagne le sous-test
`{"PYTHONDEVMODE": "0", "PYTHONWARNINGS": ""}` → `["-X", "dev"]`, et son « Rougit si » nomme « PYTHONDEVMODE non vide
autre que « 1 » (« 0 », que CPython lit comme posé) pris pour absent ». `PLANCHER` reste à 415. Le code est inchangé.

- **Référence indépendante** (`preuves/mesure-pythondevmode-0.txt`) : sous 3.10 à 3.13, PYTHONDEVMODE « 1 » et « 0 »
  donnent `True ['default']`, « » donne `False []`.
- **OUT-2j corrigé** (même nom, même place) : sha256 `3f5ed4dc2636732ee80c18775a9084197c15489af928037c540ac89f3a52a66f`,
  49 lignes ajoutées et 10 retirées (contre 48 et 10), aucune de plus de 120 caractères, aucun marqueur R-13, octets 92
  inchangés par fichier. L'ancien OUT-2j (`9b41f9d1…`) est gardé sous `livrables/avant-C1/`.

**Rouge puis vert (3.12, `-X dev -W error`)**
- J09 sur l'ancien OUT-2j (anciens tests) : 21 OK, il survit.
- J09 sur OUT-2j corrigé : 1 FAIL (le sous-test PYTHONDEVMODE « 0 », « Tuples differ »), 0 ERROR.
- OUT-2j corrigé, sans mutant : 21 OK.

**Mutants OUT-2j** (sur l'état corrigé, borne 300 s, runner puis s2bis, S2, sim-bis) : 11 sur 11 tués par S2, 0 FATAL.
J11 est le J09 de la revue ; il est tué par S2.

**Série et lignes du job**
- La série OUT-2a à OUT-2j est rejouée sans retouche par `patch -p1 -F0`, sans aucun avertissement :
  - sur `e6657dc`, elle donne l'arbre final entier ;
  - sur `b46672b`, les 9 fichiers du contrat sont identiques, et les mêmes 7 fichiers sont touchés.
- Lignes du job sur l'état final :

| Python | runner | s2bis | sim-bis | S2 |
|---|---|---|---|---|
| 3.10 | 136 ok | 255 | 172 | rouge connu PY310-1 (80 noms identiques à la base ; sous-test neuf « ok ») |
| 3.11, 3.12, 3.13 | 136 ok | 255 | 172 | Ran = 415, conforme |
| 3.12, série sur `b46672b` | 136 ok | 255 | 172 | Ran = 415, conforme |

Aucune ligne « Exception ignored » ni « Warning ». Rien retiré : 123 → 136 cas, 413 → 415 tests.

**Écart E-9** : mon premier J09 était écrit sans parenthèses (`2 * environ.get(...) == "1"`). Par précédence, c'est un
autre mutant (jamais `-X dev`). Ses sorties sont versées sous `preuves/rouge/invalide/` et ne comptent pas ; je l'ai
refait à la forme de la revue. Dépôt : tête `b46672b`, statut vide, `.git/HEAD` et `.git/index` inchangés depuis la
vague 3 ; aucune écriture git. Copies lourdes supprimées ; aucun processus ne reste.

**SHA256SUMS** : il couvre désormais tout le dossier `corr3/` sauf lui-même, y compris ce rapport, `revue/` et les deux
transcrits posés par l'orchestrateur.
