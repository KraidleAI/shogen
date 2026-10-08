# Rapport du worker — OUT2 (transcrit)

> Transcription par l'orchestrateur le 2026-10-08 12:11:04 UTC du rapport rendu par l'agent a1e9c50c94818cdbf (workflow wf_34ba9b2a-037) ; contrôle FM-1.1 : fragments_l51_l14 = 0 ; modèle résolu au transcript : claude-opus-5-5. Texte de l'agent ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Rapport du worker G1 — lot OUT-2 (outillage de preuve : RUNNER-REJEU-1, SUITE-MASQUE-UNITTEST-1, ENREG-ANCRE-1)

**Gate 0 : `claude-opus-5-5`** (identifiant exact lu dans le contexte système de la session). L'effort `max` vient de la fiche ; je ne peux pas le mesurer de l'intérieur.
**Horloge** (`date -u`) : début le 2026-10-08 à 10:14:05 UTC, fin à 11:16:18 UTC.
**Base** : HEAD e6657dcc3154bf2d35c69b84d9deae1385e702a7 sur `claude/compassionate-noether-szmdyj`, c'est la base du brief. Copie faite par `git archive`, avec les exclusions du brief passées en pathspec. Les 6 fichiers du contrat ont le sha256 des blobs. Le dépôt n'a pas bougé : statut vide, aucune écriture git.

## Verdict

- Les trois items sont fermés : deux par du code, le troisième par une règle écrite.
- La matrice 3.10 à 3.13 est verte, sauf S2 sous 3.10. C'est le rouge connu PY310-1, avec les mêmes 80 noms rouges que la base.
- Les leurres du contre-contrôle de R-1 donnent les mêmes verdicts, sauf D7, qui est maintenant refusé et nommé.
- Le contre-contrôle par un réviseur tiers reste à faire.

## Diffs

Série appliquée sur e6657dc ; `patch -p1 -F0` vérifié : base + OUT-2a = a, + OUT-2b = b, + OUT-2c = c.

| Diff | Item | Fichiers (lignes ajoutées) | + / − | sha256 |
|---|---|---|---|---|
| OUT-2a | RUNNER-REJEU-1 | runner (73) | 73 / 35 | 33a25a59…09e8 |
| OUT-2b | SUITE-MASQUE-UNITTEST-1 | runner 30, vérificateur 17, `oracle_record.py` 16, `test_oracle_record.py` 35 | 98 / 5 | ea802333…17de |
| OUT-2c | ENREG-ANCRE-1 | `s2-harness/tools/README.md` (31, fichier neuf), docstring de `oracle_record.py` (4) | 35 / 1 | 6ef56a8c…d20d |

- **Ordre** : d'abord le protocole à nonce, puis les cas M (même compte `CAS`, `PLANCHER` relevé), puis le texte, qui décrit l'état final.
- **Planchers exacts** : `CAS` du runner passe de 97 à 100 puis à 105 ; `PLANCHER` de S2 passe de 407 à 408. s2bis (255) et sim-bis (172) ne changent pas.
- `gates.yml` et le FORMAT sont inchangés. La suite s2bis ne change pas, donc il n'y a pas de section METRIQUES.

## Choix (Q-n)

**Q-1, RUNNER-REJEU-1 : un nonce par requête.**
- Le runner tire `secrets.token_hex(16)` avant chaque requête. Le serveur, qui est le code du runner, renvoie `[nonce, genre, valeur]`.
- Si le nonce de la réponse n'est pas celui de la requête, le runner s'arrête en sortie 1 avec le message « réponse sans le nonce de sa requête … : écrite avant elle, ou rejouée ».
- Je n'ai pas retenu le refus d'une réponse disponible avant sa requête, pour trois raisons :
  - il faut un `select` sur un tube, qui n'existe que sous POSIX ;
  - le résultat dépendrait du temps ;
  - `readline` lit en avance dans son tampon.
- Le nonce est tiré à chaque requête et non une fois par run. Sinon, un module qui lit la première requête pourrait écrire toutes les réponses d'avance (cas R-11, mutant A7).
- La docstring porte la garantie réelle : « sortie 0 = les CAS cas ont été joués et jugés sur le canal, chaque réponse écrite après sa requête par un code qui l'a lue », et non « les réponses viennent du code relu ».
- Elle porte aussi la limite : un vérificateur qui reconnaît `--serveur`, ou qui lit les requêtes, peut répondre juste au runner et mentir au job. La lecture humaine du diff du vérificateur reste nécessaire.

**Q-2, SUITE-MASQUE-UNITTEST-1 : refus nommé de tout nom de module standard posé à la racine.**
- Je n'ai retenu ni `unittest*` seul, ni `-I`.
- Mesure sans `-I`, sous 3.10 à 3.13 : 41 à 44 noms posés à la racine masquent la bibliothèque pour `-m unittest`. C'est `unittest`, plus 40 à 43 autres, dont `argparse`, `re`, `traceback`, et `runpy` sous 3.10. Tous sont dans `sys.stdlib_module_names`.
- Mesure de `-I` avec `-m` :
  - sous 3.10, le mode isolé n'ajoute pas le chemin 0 ;
  - sous 3.11 à 3.13, `-I` implique `-P` (`safe_path` vaut True) ;
  - aucun masquage avant la découverte sur les quatre versions.
- `-I` ne suffit pourtant pas :
  - il ne donne aucun refus nommé ;
  - la découverte (`-t .`) remet la racine en tête : un `json.py` importé par un test est pris à la racine, avec ou sans `-I` (mesuré) ;
  - `-I` implique `-E`, donc la suite ignorerait PYTHONHASHSEED, PYTHONDEVMODE et PYTHONWARNINGS.
- Règle retenue : refuser avant tout lancement toute entrée de la racine dont le nom, pris avant le premier point, est dans `sys.stdlib_module_names`. Aucune racine actuelle n'est touchée.
- Le refus est dans le vérificateur (`masques` et `main`, sortie 1, motif « … masque la bibliothèque standard … : suite non lancée »). Il couvre ainsi le job et les commandes de JOBS de l'enregistreur.
- Il est aussi dans l'enregistreur, pour la commande `suite`, la seule qu'il lance par `-m unittest` sans passer par le vérificateur.

**Q-3, ENREG-ANCRE-1 : un README de l'outil plutôt que le FORMAT.**
- Le FORMAT spécifie les journaux de l'observateur, il est scellé avec le collecteur et épinglé par `test_format.py`. L'enregistreur est un outil de preuve partagé par S2 et S2-bis.
- La règle est dans `s2-harness/tools/README.md`, avec un renvoi depuis la docstring :
  - la comparaison ne vaut que si l'outil tourne depuis un arbre dont le vérificateur a été relu, extrait à part du commit à enregistrer ;
  - lancée depuis l'arbre du commit enregistré, elle est triviale ;
  - la lecture (`--verifier`) suit la même règle ;
  - qui cite un enregistrement nomme l'arbre de l'outil et la revue qui a relu ce vérificateur.
- Garde mécanique proposée, sans l'imposer :
  - consigner un champ `outil` : sha256 de `VERIF`, `git rev-parse HEAD` du dépôt de l'outil, `VERIF` propre ou non ;
  - en option, refuser `outil.commit == tree.commit`.
  - Elle demande un schéma v2 et une décision.

**Q-4, enregistreur : la règle `masques` y est écrite en une ligne.**
- Mon premier dessin chargeait `VERIF` pour la commande `suite`. S2 a rougi : l'arbre de production de `test_nominal_bout_en_bout` n'a pas de vérificateur (écart E-1).
- J'ai donc écrit la règle deux fois. Chaque copie est épinglée à la même liste écrite à la main, M-05 côté vérificateur et le test neuf côté enregistreur.

## Cas neufs (rouge d'assertion montré)

| Cas | Attendu | Rouge sur l'ancien mécanisme |
|---|---|---|
| R-09, capture puis rejeu du transcript (D7) | sortie 1, refus « nonce » | sortie 0 : D7 reproduit |
| R-10, réponse écrite avant toute requête | sortie 1, refus « nonce » | refus « illisible », non nommé |
| R-11, rejeu au nonce de la première requête | sortie 1, refus « nonce » | refus « illisible » |
| M-01, `unittest.py` qui forge le résumé | `main` = 1, refus nommé, leurre non importé | code 0, leurre importé |
| M-02, paquet `unittest/` | 1 | 0 |
| M-03, `argparse.py` | 1 | 0 |
| M-04, témoin `commun.py` | 0 | 0 |
| M-05, `masques` | `["json.py", "unittest.py"]` | écart |
| test neuf de l'enregistreur (S2, 408) | `suite` refusée sans rien écrire ; `suite-s2bis` en exit 1 avec refus nommé ; refus (exit) à la lecture | « ValueError not raised » |

Rien n'a été retiré : les 97 noms de cas de la base restent identiques, et les 13 tests de l'enregistreur sont intacts (AST égaux).

## Leurres

| Leurre | base | final |
|---|---|---|
| V0 / D1 / D2 / D3 / D4 | 0 / 3 / 1 / 1 / 1 | 0 / 3 / 1 / 1 / 1 |
| D5 | 1 | 1 (réponse illisible) |
| D6a / D6b / D-CAPTURE | 0 / 1 / 0 | 0 / 1 / 0 |
| **D7** | **0, non refusé** | **1, refusé et nommé (nonce)** |
| L0 à L3 de l'enregistreur (3.11, 3.12) | conforme, exit 1, refus, refus, exit 1 | identiques |
| **Leurre neuf** (`unittest.py`, `unittest/`, `argparse.py` à la racine de s2bis, ligne du job) | **0, « conforme Ran = 255 », × 3** | **1, refus nommé, × 3 formes × 4 versions** |

## Mutants

Classés par les commandes du job, dans l'ordre runner, s2bis, puis S2. Borne de 300 s, réseau isolé, campagne jouée sur les octets finaux.
- **OUT-2a : 9 tués sur 9.**
- **OUT-2b : 14 tués sur 14** (8 par le runner, 6 par S2).
- Aucun FATAL.
- OUT-2c n'a pas de code (écart E-7).

## Matrice

`-X dev -W error`, réseau isolé :

| Python | runner | s2bis | sim-bis | S2 | leurre neuf |
|---|---|---|---|---|---|
| 3.10 | 105 ok | 255 | 172 | rouge connu 77 FAIL + 3 ERROR, mêmes 80 noms que la base (sha256 6de48d41) ; test neuf ok | 1, refus nommé × 3 |
| 3.11 | 105 ok | 255 | 172 | 408 conforme | 1, refus nommé × 3 |
| 3.12 | 105 ok | 255 | 172 | 408 conforme | 1, refus nommé × 3 |
| 3.13 | 105 ok | 255 | 172 | 408 conforme | 1, refus nommé × 3 |

- Aucune ligne « Exception ignored » ni « Warning ».
- **xtask** : S-G1 à S-G8 verts, plus fmt, no_std et clippy. S-G9 est rouge sur sa seule violation connue, `docs/17-modele-de-menace.md:70`, qui pointe vers un fichier exclu de la copie.
- **Forme** : aucune ligne de plus de 120 caractères, aucun octet 92 ajouté, aucun marqueur R-13, bibliothèque standard seule (`secrets` ajouté).

## Écarts

- **E-1** : premier dessin de l'enregistreur rejeté (S2 rouge, voir Q-4). La campagne OUT-2b n° 1 est invalide pour B9 à B12 ; je l'ai versée sans la compter.
- **E-2** : l'outil d'édition a supprimé quatre espaces en fin de chaîne. Je les ai trouvées en relisant les diffs et corrigées, puis j'ai tout rejoué sur les octets finaux.
- **E-3** : M-01 lançait d'abord le vérificateur en ligne de commande. Les leurres D6a et D-CAPTURE passaient alors de 0 à 1, parce que l'enveloppe du réviseur neutralise `__main__`. M-01 passe maintenant par le canal, et la garde de capture devenue inutile est retirée.
- **E-4** : les mutants de l'enregistreur sont classés jusqu'à S2, comme l'E-3 de R-1.
- **E-5** : sim-bis tourne avec `GIT_DIR` pointé en lecture seule sur le dépôt, parce que la copie n'a pas d'historique.
- **E-6** : les lignes ResourceWarning viennent du script du réviseur lui-même, pas du code relu.
- **E-7** : OUT-2c n'a pas de code, donc pas de mutants. Point à adjuger.
- **E-8** : `$!` a rendu 7106 alors que le vrai PID était 7108.

## Items à former

1. **SHOGEN-S2BIS-SCRIPT-MASQUE-1** [mesuré sur la base] : les lignes du job tournent sans `-I`.
   - Un `enforcement/subprocess.py` donne « conforme » sans lancer la suite.
   - Un `enforcement/tests/json.py` fait rendre « 97 ok » au runner, avec la sortie 0.
   - Le serveur du runner et les commandes de production de l'enregistreur sont dans la même classe.
   - Prix [inféré] : passer ces lignes en `-I`, avec K-01 à K-03 et le motif de l'enregistreur. Déclencheur : avant la G2 de P2.
2. **SHOGEN-S2BIS-SUITE-RESUME-FORGE-1** [mesuré sur l'état final] : un test qui écrit un résumé forgé puis appelle `os._exit(0)` obtient « conforme (Ran = 255) », alors que la suite a 2 tests réels dont un en FAIL.
3. **SHOGEN-S2BIS-MASQUES-LECTURE-1** [inféré] : `verifier` ne contrôle pas le masquage dans `tree.sha256`.

**Limite** : `sys.stdlib_module_names` n'existe qu'à partir de 3.10. Sous 3.9, le refus deviendrait une AttributeError : l'échec reste fermé, mais il n'est pas nommé.

## Journal G1

- **Sources [lu]** : le brief ; G0 COLLECTE en entier ; ANNEXE-B l.1143-1186 ; ANNEXE-D l.32-48, lue pour éviter les pièces de D.2 ; `revue-r1` en entier ; runner, vérificateur, enregistreur et ses tests en entier ; `gates.yml` l.140-247 ; FORMAT l.1-45 ; `oracle_r1.py` l.25-80 ; `test_rendu_production.py` par plages ; NOTES et leurres de R-1 ; `isole.sh`.
- **Interdits respectés** : aucune pièce de D.2, aucun `*.jsonl`, aucune recherche récursive, et `SHOGEN_S2_CAMPAGNE_CONTROL` n'a jamais été posée.
- **Chiffres de base recomptés** : runner 97, s2bis 255, sim-bis 172, S2 407.
- **PID** : lignes 7108 et 9414 ; campagnes 26583, 27273, 6329, 28542, 16552 et 30106 ; passes finales 16550 et 30104 ; matrices 31333 à 31336, 2835/2836/2846/2847 et 16800 à 16803 ; leurres 26014/26015, 30996/30997, 14567/14568 et 30257/30258 ; xtask 28768 et 30614. Tous sont terminés.
- **Nettoyage** : copies, `mut/`, `cible/`, `tmp/` et `travail/` supprimés.

## Fichiers

Tous dans <scratchpad>/s2bis/outillage2/ :
- diffs/OUT-2a.diff
- diffs/OUT-2b.diff
- diffs/OUT-2c.diff
- SHA256SUMS : 142 entrées vérifiées, sha256 43116a77…1397
- NOTES.md
- RAPPORT-GENERATEUR.md
- livrables/ : sha256 des fichiers à chaque étape
- preuves/
- outils/
- leurres/
