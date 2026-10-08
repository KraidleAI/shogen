# SB-8H : rapports du worker (transcrits)

> Transcription par l'orchestrateur le 2026-10-05 10:43:52 UTC des deux rendus du worker (agent adc50e03e87327a1c) ; contrôle FM-1.1 : fragments_l51_l14 = 0. Textes ci-dessous, sans retouche.

## Premier rendu

claude-opus-5-5

# SB-8H : correction CC-1 du contre-contrôle de SIM-BIS tranche 3, plus la retouche de `Couche`

Le diff est prêt : les trois points sont faits et tous les contrôles demandés passent. Il me reste une limite à former, détaillée plus bas.

- **Gate 0** : `claude-opus-5-5`, effort max.
- **Horloge** (`date -u`) : 2026-10-05, de 10:05:22 à 10:31:55 UTC.
- **Dépôt** : tête f5915a5 au début comme à la fin, `git status --short` vide. Aucune opération git en écriture.
- **Livrables** :
  - `<scratchpad>/s2bis/sim3/cc1/SB-8H.diff` : sha256 ef62621d…, 57 lignes, 0 octet 92.
  - `<scratchpad>/s2bis/sim3/cc1/SHA256SUMS` : sha256 2ed927f2…, 64 entrées, 64 OK (le diff, NOTES.txt, `outils/` et `journal/`).

## Base
- Copie f5915a5 par `git archive` avec les 7 exclusions : 770 fichiers.
- Les 13 diffs s'appliquent en série (`git apply --check`, puis `git apply`), 0 fichier `.orig` ou `.rej`.
- Sommes contrôlées avant application : `sim3/SHA256SUMS` (77f3268d…) 319 sur 319 OK ; `corr/SHA256SUMS` (48edd0ed…) 189 sur 189 OK.
- État SB-8G : runner 33 sur 33, Ran 128, conforme.
- **Écart de nom** : `rev/outils/proto_corrections_cc1.py`, nommé par le brief et par le contre-contrôle, n'existe pas. Le prototype présent est `rev/outils/proto_cc1.py` (e4cb24a9…, listé dans `rev/SHA256SUMS` c24296b0…, 121 sur 121 OK). X-01 vient de `rev/outils/mutants_cc.py` (7747e045…) ; ma copie lui est identique, comparaison faite par programme.

## Le diff : code +23 −4 (R-25 tenu)
1. **CC-1** : nouveau test `test_oracle_frontiere_c_s_t_reg_2` dans `TestModeComplet`, juste après T-REG-2 (+19 lignes).
   - Mock : `mock.patch.object(regle, "deux_modes", return_value=(a, f))`, R = 999, seuil 9, S suivie.
   - Assertion : `[code(9, 10), code(8, 9), code(10, 11), code(9, 9)] == ["REGLE/oracle", None, None, None]`.
   - **Ajout au prototype** : sans refus, `assertIs(rendu, a)` vérifie que l'oracle rend bien le résultat anticipé.
   - **Rouge sous X-01**, par assertion : `[None, 'REGLE/oracle', None, None] != [...]`. Ce sont les deux cas du réviseur : la faute 9 contre 10 n'est pas vue, et 8 contre 9 lève une fausse alerte.
   - **Vert sur le code.** Le prototype du réviseur, rejoué : 2 ECHEC sous X-01, 4 OK sur le code.
2. **Docstring de `Couche`** : lignes 111 à 113 renvoyées à la ligne, « indice i ≥ 0 » tient sur une ligne (+3 −3).
   - Octets avant et après le littéral identiques (positions 5528..6151 dans les deux versions).
   - Le littéral est le même une fois les blancs ôtés ; arbres `ast` égaux hors de cette docstring.
   - Aucune ligne de plus de 120 caractères.
3. **Plancher** : ligne 242 de `gates.yml`, `--plancher 128` devient `129`.
   - Avant le relèvement, le job refusait : « Ran 129 > plancher 128 (--egal) », sortie 1.
   - Après : conforme.

## Contrôles sur l'état final
- **Commande du job** : runner 33 ok, 0 échec ; ligne `--aucun-saut --egal --plancher 129` : sortie 0, Ran 129, conforme.
- **Mode strict** `-X dev -W error` : Python 3.10.20, 3.11.15, 3.12.3, 3.13.14 × PYTHONHASHSEED 0 et 7 : 8 sur 8 OK, Ran 129.
- **R-13** : motif lu dans `gates.yml` (67 octets).
  - 0 constat sur les 19 fichiers de `scripts/sim-bis` et sur les lignes ajoutées.
  - Témoin positif : le motif voit bien un marqueur posé exprès.
- **Octets 92** : 0 dans le diff ; 0 dans les 64 fichiers de `cc1`.
- **Mutants**, classés par la commande du job (borne 300 s) :

| mutant | sur SB-8H | sur SB-8G (pour information) |
|---|---|---|
| X-01 | tué | vivant (CC-1 confirmé) |
| M-8H-01 « ≤ seuil + 1 » | tué | déjà tué |
| M-8H-02 seuil du R de `parametres.json` | tué | déjà tué |
| M-8H-03 C_S de l'anticipé lu des deux côtés | tué | déjà tué |
| M-8H-04 « == » au lieu de « ≤ » | tué | déjà tué |
| M-8H-05 résultat complet rendu | tué | déjà tué |

  - Sur SB-8H : 6 tués, 0 FATAL, 26,4 s au plus.
  - Le nouveau test, lancé seul, est rouge par assertion sous chacun des six.
  - Le cas n'ajoute à la suite que la mort de X-01. Les cinq mutants neufs étaient déjà tués par la suite existante ; le cas les tue aussi seul.
- **s2-harness** (règle 4), sous `isole.sh` (`unshare -n`, `lo` allumée) : Ran 405, OK (2 sauts qui nomment la variable), conforme.
- **xtask** (lignes de verdict seules) :
  - S-G1 à S-G8 VERT ; fmt, no_std et clippy VERT.
  - S-G9 ROUGE, 1 violation ; verdict global ROUGE.
  - Lignes identiques sur le témoin (f5915a5 sans diff). Une ligne de sortie cite `docs/17-modele-de-menace.md:70` des deux côtés ; je l'ai comptée sans l'afficher.
- **Diff vérifié** : appliqué sur une copie neuve de SB-8G, l'arbre obtenu est identique à l'arbre de travail (`diff -r`). Les lignes `index` correspondent aux blobs (cd9b3e6, 61ab115, 58b878b).
- **Nettoyage** : copies, cible cargo, dossier d'étapes et TMPDIR supprimés ; il reste 748 Ko.

## Limite à former (règle PAROXYSME)
- **Constat** : la sonde S-8H-01, hors compte, reste vivante sur SB-8G comme sur SB-8H. Elle calcule le seuil de `oracle()` sur `R_approche`, donc 9 quel que soit R ; la sortie du job vaut 0 et le test seul passe.
- **Cause** : le cas de frontière fixe la borne à R = 999 seulement. Aucun test ne la fixe à R = 9 999, le R de l'oracle sur les 200 premières réplications (E-S-29).
- **Effet si la faute existait** : à R = 9 999, l'oracle comparerait « C_S ≤ 9 » au lieu de « C_S ≤ 99 ». Il manquerait une faute d'arrêt avec C_S entre 10 et 99.
- **Remède proposé, non appliqué** (hors de CC-1 tel qu'adjugé) : les mêmes quatre cas à R = 9 999, seuil 99, soit 99/100 refusé et 98/99, 100/101, 99/99 sans refus. Environ +1 ligne. À trancher par toi.

## Mes écarts
- **E-1, barres obliques inverses** :
  - tapées dans un `grep` de lecture vers 10:13, pour vérifier l'unicité d'une ancre ; aucun fichier écrit ;
  - deux outils (`mutants_8h.py`, `portes.sh`) écrits d'abord avec des guillemets échappés, réécrits avant tout usage. Le compte final est de 0.
- **E-2, PID** :
  - un `pgrep -f` sur un motif étroit pour la première campagne (PID 22479) ; il a aussi listé les coquilles ;
  - `$!` après `setsid nohup` rendait le PID du parent, qui forke. Les PID réels (28110, 28111) ont été lus dans `/proc`, avec `cmdline.py` et `trouver.py`.
- **E-3, lectures de taille sur mes copies** : `du -sh`, des `find` (compte de fichiers, `__pycache__`, fichiers récents) et des `diff -rq`. Seuls des tailles, des comptes et des noms de fichiers différents ont été affichés, jamais de contenu.

## Journal G1
- **[lu]**
  - Le brief et CLAUDE.md.
  - Le CONTRE-CONTROLE transcrit (875f71ae…), en entier.
  - Côté réviseur : `rev/notes-cc.txt` (2c564aa4…) ; `proto_cc1.py`, `mutants_cc.py`, `strict.sh`, `xtask.sh`.
  - Les briefs : BRIEF-SIM-T3 (eaeb1937…) et BRIEF-CORRECTIONS (fa243d23…).
  - Côté worker des corrections : `corr/outils` base.sh, job.sh, faire_diffs.py, etape.sh ; de `mutants_rejeu.py` et `mutants_corr.py`, les imports seulement, chargés par `runpy` ; `corr/journal` portes.txt et xtask-verdicts.
  - Les diffs : SB-8F l.25-50 ; « indice i » cherché dans les 13 diffs.
  - `p1b/g2/travail/outils/isole.sh` et `lo_up.py`.
  - Dépôt à f5915a5 :
    - ANNEXE-D l.32-48 (D.2) ;
    - G0-SIM-BIS en entier (d9cffc0a…) ;
    - PROPOSITION (0e78afab…) l.183 (E-S-29), 360-361 (SB-8), 388-410 (T-REG-2) ;
    - AVIS (aaf70a4f…), lignes trouvées par grep ;
    - ADR-0029 (b908842d…) l.197-204, lignes tronquées à 700 caractères ;
    - `gates.yml` (a92a750e…) l.220-242, et les lignes R-13 trouvées par grep.
  - Sur la copie : `regle.py` et `test_regle.py` en entier ; `observateurs.py` l.107-147 ; `verdict-suite-s2.py` ; l'en-tête du runner.
- **[abs]** : AVIS-SIM-T3, G2-SIM-T3, RAPPORT-CORRECTIONS, PASSATION-CLOUD, le corpus (poste local), le reste d'ADR-0029.
- **[2nd]** : aucun ; chaque chiffre ci-dessus est recompté par mes commandes (`journal/`).
- **Interdits respectés** : aucune pièce de D.2, aucun `*.jsonl`, aucun dossier exclu, aucune opération réseau ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée.

## Second rendu

claude-opus-5-5

# SB-8H, second rendu : la limite S-8H-01 est fermée dans SB-8H

Le diff est régénéré et tout ce que tu as demandé de rejouer est vert : X-01 et les six mutants sont tués, S-8H-01 compris.

- **Gate 0** : `claude-opus-5-5`, effort max.
- **Horloge** (`date -u`) : 2026-10-05, de 10:34:18 à 10:43:18 UTC.
- **Dépôt** : tête f5915a5, `git status --short` vide. Aucune opération git en écriture.
- **Livrables** :
  - `<scratchpad>/s2bis/sim3/cc1/SB-8H.diff` : sha256 **016a7ccd…** (remplace ef62621d…), 61 lignes, 3 fichiers.
  - `<scratchpad>/s2bis/sim3/cc1/SHA256SUMS` : sha256 **52cdb92f…**, 95 entrées, 95 OK. L'ancienne liste est gardée dans `journal/SHA256SUMS-v1.txt`.

## Base reconstruite
- Copie f5915a5 avec les 7 exclusions : 770 fichiers.
- Les 13 diffs : sommes contrôlées, application en série sans fichier `.orig` ni `.rej`.
- Puis SB-8H dans sa première version : les blobs obtenus égalent ceux du premier rendu (44c1052, e20133d, aa540dc).

## Modification : le même test, aucune nouvelle méthode
- Dans `test_oracle_frontiere_c_s_t_reg_2`, `code()` prend maintenant R en argument. Le test parcourt deux jeux de cas écrits à la main :
  `cas = {999: ((9, 10), (8, 9), (10, 11), (9, 9)), 9999: ((99, 100), (98, 99), (100, 101), (99, 99))}`
- Pour chaque R, la liste attendue est `["REGLE/oracle", None, None, None]`. Le seuil 99 se calcule à la main : α·(R + 1) − 1.
- La docstring est complétée et nomme S-8H-01.
- Le plancher reste 129 : aucun test ajouté.
- **Rouge sous S-8H-01**, par assertion à R = 9 999 : `[None, None, None, None] != ['REGLE/oracle', None, None, None] : 9999`. La faute 99 contre 100 n'est pas vue.
- **Vert sur le code.** Le prototype du réviseur, rejoué en non-régression à R = 999 : 4 OK.
- Diff total : code +27 −4. Le test fait +23 lignes, `observateurs.py` reste à +3 −3 (contrôle de la docstring identique, 9 sur 9) et `gates.yml` à +1 −1.

## Rejeu sur l'état final

**Mutants**, classés par la commande du job (borne 300 s) : 7 tués sur 7, 0 FATAL, 28,2 s au plus.

| mutant | job | test seul : rouge par assertion |
|---|---|---|
| X-01 | tué | `[None, 'REGLE/oracle', None, None]` |
| M-8H-01 | tué | `[None, None, 'REGLE/oracle', None]` |
| M-8H-02 | tué | `[None, None, None, None]` |
| M-8H-03 | tué | `[None, None, None, None]` |
| M-8H-04 | tué | `['REGLE/oracle', 'REGLE/oracle', None, None]` |
| M-8H-05 | tué | `assertIs` en échec, résultat complet rendu |
| S-8H-01 | tué | `[None, None, None, None]` à R = 9 999 |

- **Commande du job** : runner 33 ok, 0 échec ; ligne `--egal --plancher 129` : sortie 0, Ran 129, conforme.
- **Mode strict** `-X dev -W error` : Python 3.10.20, 3.11.15, 3.12.3, 3.13.14 × PYTHONHASHSEED 0 et 7 : 8 sur 8 OK, Ran 129.
- **R-13** (motif lu dans `gates.yml`) : 0 constat sur les 19 fichiers de `scripts/sim-bis` et sur les lignes ajoutées ; le témoin positif est bien vu.
- **Octets 92** : 0 dans le diff ; 0 dans les 96 fichiers de `cc1`.
- **Rejoués aussi, hors de ta liste** :
  - xtask : lignes de verdict identiques au premier rendu et au témoin. S-G1 à S-G8 VERT, S-G9 ROUGE (1 violation, la ligne connue `17:70`, comptée sans l'afficher).
  - s2-harness sous `isole.sh` : 405, OK (2 sauts), conforme.
- **Diff vérifié** : appliqué sur une copie neuve de SB-8G, l'arbre obtenu est identique à l'arbre de travail ; lignes `index` 58b878b..138db43 pour le test.
- **Nettoyage** : copies, cible cargo et TMPDIR supprimés ; il reste 1,2 Mo.

## Écarts
- **E-4, barres obliques inverses** : guillemets échappés tapés dans le heredoc Python qui a mis S-8H-01 dans la liste des mutants (`outils/mutants_8h.py`). Le fichier écrit a été contrôlé : 0 octet 92, les sept ancres trouvées une fois chacune, X-01 toujours identique à celui du réviseur.
- **E-3 reconduit** : `diff -rq`, `find` (`__pycache__`) et `du` sur mes seules copies ; seuls des comptes et des noms de fichiers ont été affichés.
- **Outils** : `mutants_8h.py` modifié (S-8H-01 passe dans les mutants, les chaînes ne changent pas). Les nouveaux outils `rouge_vert_2.sh` et `portes_2.sh` écrivent des sorties suffixées `-v2` ; les sorties du premier rendu sont conservées.

## Journal G1 (complément)
- **[lu]** : ton message, et mes propres outils et sorties du premier rendu.
- **Commandes et chiffres** : tout est recompté par mes commandes, dans `journal/` : `rouge-vert-S-8H-01.txt`, `job-travail-8H-v2.txt`, `campagne-8H2.txt` et `mut-8H2-*`, `portes-v2.txt`, `xtask-verdicts-*-v2.txt`, `s2-harness-travail-v2.txt`, `tailles-SB-8H-v2.txt`, `verif-diff-SB-8H-v2.txt`.
- **[2nd]** : aucun.
- **Interdits respectés** : aucune pièce de D.2, aucun `*.jsonl`, aucun dossier exclu, aucune opération réseau ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée.
