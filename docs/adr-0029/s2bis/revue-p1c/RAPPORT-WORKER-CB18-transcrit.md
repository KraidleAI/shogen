# Rapport du worker — P1 tranche C : CB-18, ENREG-ROLE, SEGMENT-JOUR, ENTIER-ECRIVAIN (transcrit)

> Transcription par l'orchestrateur le 2026-10-05 07:47:30 UTC du rapport rendu par message par le worker (agent a5c5e841f344d2c69) ; contrôle FM-1.1 du transcript : fragments_l51_l14 = 0. Texte du worker ci-dessous, sans retouche.

Gate 0 : claude-opus-5-5 (identifiant exact du modèle sous lequel je tourne ; l'effort « max » demandé n'est pas observable de l'intérieur)

Rapport du worker : sous-lot CB-18 (P1, tranche C), SHOGEN-S2BIS-ENREG-ROLE-1, puis les ajouts de l'orchestrateur reçus en cours de lot (N-1, I-1, I-2). Fin : 2026-10-05 07:45 UTC. Aucune opération git en écriture dans /home/user/shogen : lectures en `--no-optional-locks`, `git archive` vers mes copies, `git apply` dans mes copies seulement. Rapport rendu par ce message.

## Résumé
- **Neuf diffs en série**, chacun ≤ 200 lignes de code ajoutées. Ils sont produits sur une copie de 122c670 et s'appliquent tels quels sur la tête actuelle 3164348. La seule différence avec la tête est le plancher sim-bis (93 au lieu de 49), qui vient d'un autre lot.
- **Items fermés, chacun par un test nommé** : ECRIVAIN-USAGE-1, PLAN-CABLAGE-1, SONDES-ECHEANCE-1, SOMMEIL-MURAL-1, FORMAT-RETOUCHES-1 (étendu par I-2), SEGMENT-JOUR-1 (N-1) et ENTIER-ECRIVAIN-1 (I-1). ENREG-ROLE-1 est livré.
- **Mutants** : 115 au total, tous tués sur l'état final de leur diff par la commande du job, presque tous par leur test visé. Aucun vivant, aucun FATAL.
- **Suites** : s2bis passe de 114 à 133 tests (matrice 3.10 à 3.13 en `-X dev -W error` : OK, 0 avertissement). La suite S2 passe de 405 à 406 tests.
- **xtask** : seul S-G9 est rouge (`docs/17-modele-de-menace.md:70`), comme sur le témoin de base.
- **Défaut trouvé en route et corrigé** : le test de bout en bout CB-18e échouait sous charge. La sonde D-3 lançait `python3 -c` avec un délai de 0,1 s. Il passe maintenant par `/bin/echo` avec un délai de 0,2 s, et le test exige au moins une requête D-4 ou D-5 relevée. Toutes les campagnes concernées ont été rejouées.

## Diffs (dossier `…/cb18/diffs/`)

| diff | objet | code +/− | docs +/− | plancher | rouge montré | mutants |
|---|---|---|---|---|---|---|
| CB-18a | écrivain : un seul fil, refus nommés, `_terminal` ; FORMAT §5 et §12 | 118/36 | 41/5 | s2bis 117 | 3 FAIL | 12/12 |
| CB-18b | attentes murales par pas ≤ 1 s, départ monotone porté dans le suivi, plan câblé (BOUCLE/plan, BOUCLE/hote), règle `fin` > E appliquée aux sondes | 186/38 | 55/8 | 122 | 8 FAIL | 13/13 (2e passage) |
| CB-18c | configurations scellées, descripteur, câblage | 177/1 | 46/1 | 124 | squelette : 13 FAIL + 2 ERROR | 15/15 |
| CB-18d | point d'entrée `pool`, `__main__`, `run_params`, fermeture | 128/9 | 34/2 | 126 | squelette : 1 FAIL + 3 ERROR | 11/11 |
| CB-18e | test de bout en bout, conformité au FORMAT | 194/1 | 28/2 | 127 | par mutation (champ omis) | 11/11 |
| CB-18f | tests nommés de FORMAT-RETOUCHES-1, avec I-2 (§7.1) | 75/1 | 37/8 | 129 | 2 FAIL (texte de base), 1 FAIL (texte de e5) | 20/20 |
| ENREG-ROLE | `oracle_record` : suites `suite-s2bis` et `suite-sim-bis`, ligne du job lue au gates.yml du commit, refus gardés | 77/6 | 0/0 | S2 `PLANCHER` 406 | 1 FAIL | 11/11 (job S2) |
| SEGMENT-JOUR | jour et numéro des fichiers neufs (N-1) ; FORMAT §6.1, §6.2, §7.2, §7.3 | 75/12 | 43/10 | 131 | 3 FAIL | 11/11 |
| ENTIER-ECRIVAIN | entiers de 640 chiffres au plus (I-1) ; FORMAT §1.2 et §2 | 52/4 | 30/4 | 133 | 2 FAIL | 11/11 |

Chaque plancher est exact (`--egal`). Les jobs passent sur chaque état seul : e1 à e9 donnent Ran 117, 122, 124, 126, 127, 129, 129, 131, 133, tous VIVANT.

## Items fermés et tests nommés
- **ECRIVAIN-USAGE-1**
  - Écrivain : `test_garde_d_un_seul_fil`, `test_refus_nommes_ecrivain_neuf_ferme_ou_deja_ouvert`, `test_terminal_sur_toute_methode_publique_d_ecriture`.
  - Boucle qui sort sur OSError ou JOURNAL/casse, et journal fermé par le point d'entrée : `test_run_params_et_fermeture_sur_erreur_du_journal` (sortie 1, verrou rendu, reprise).
- **PLAN-CABLAGE-1** : `test_nom_du_plan_sans_lecture_refuse_a_la_construction` et `test_cablage_des_sondes_et_de_la_boucle`.
- **SONDES-ECHEANCE-1** : `test_sonde_rendue_apres_l_echeance_avant_le_releve_vaut_null` et `test_disque_et_empreinte_releves_apres_l_etat_des_futurs`.
- **SOMMEIL-MURAL-1**
  - Tests : `test_sommeil_jusqu_a_l_instant_mural_malgre_un_saut`, `test_depart_monotone_porte_dans_le_suivi`, `test_depart_pose_par_la_boucle_et_suivi`.
  - Mesures rejouées (`sommeil-mural-rejoue.txt`) : sonde du worker −999 850 µs avant le correctif, +198 µs après ; sonde du réviseur −1 498 115 µs avant, +173 µs après.
- **FORMAT-RETOUCHES-1 et I-2** : `test_retouches_du_paragraphe_12_et_de_l_en_tete` et `test_paragraphe_7_1_dit_les_controles_de_type_de_lire`. Le second vérifie aussi que `_lire` fait les contrôles que le texte décrit.
- **SEGMENT-JOUR-1** : `test_horloge_avant_le_jour_d_un_fichier_sans_ligne_integre` et `test_bascule_vers_un_jour_deja_present_segment_suivant`.
- **ENTIER-ECRIVAIN-1** : `test_entiers_de_640_chiffres_au_plus` et `test_queue_entier_de_641_chiffres`.
- **ENREG-ROLE-1** : `test_suites_s2bis_et_sim_bis_par_la_ligne_du_job`.

## Ajouts de l'orchestrateur

### N-1 (SEGMENT-JOUR-1)
- **Reproduction** : déterministe. Fichier du lendemain vide ou coupé à 8 octets, horloge revenue à la veille. Avant le correctif, le segment 2026-10-04-1 est nommé avant le fichier 2026-10-05-0 qu'il déclare, puis la bascule suivante lève FileExistsError.
- **Remède** (celui du réviseur) :
  - jour du segment neuf = max(jour de l'horloge, dernier jour présent au dossier) ;
  - numéro = 1 + le plus grand numéro de ce jour, à la reprise comme à la bascule.
- **Test existant réécrit** : l'ancien test C-2 `test_bascule_en_echec_puis_fermer` provoquait l'échec avec un fichier du lendemain déjà présent, ce qui réussit maintenant. Il injecte désormais un ENOSPC à la création exclusive, et attrape toujours la double fermeture (M-SJ-10 tué).

### Banc du réviseur rejoué
- `banc_lecteur.py`, sha256 2e320fd1…, lancé sans modification, 2000 graines, avec le lecteur des diffs RB (`recalc/` et `config/` seuls).
- Avant mes correctifs (e7) : `collision_ecrivain` 2 et `ordre_noms_ecrivain` 1, les mêmes chiffres que le réviseur.
- Après (e9) : aucun des deux sur 2000 graines ; différentiel de 3000 altérations sans écart.
- Le cas C5 du banc, qui attendait la divergence I-1, n'a plus d'objet : l'écrivain refuse désormais l'entier et le banc s'arrête sur JOURNAL/entier.

### I-1 (ENTIER-ECRIVAIN-1)
- L'écrivain refuse tout entier de plus de 640 chiffres (`JOURNAL/entier`) avant le sérialiseur, à toute profondeur.
- Le parcours ne voit chaque conteneur qu'une fois, donc il se termine aussi sur un cycle.
- Le refus ne dépend pas du réglage de l'interpréteur : testé avec la limite abaissée à 640 et levée à 0.
- 640 est `sys.int_info.str_digits_check_threshold`, mesuré sous 3.10 à 3.13.
- `_lire` passant par la même fonction, une ligne portant un tel entier devient une queue.

### I-2
- Placé dans CB-18f : il étend FORMAT-RETOUCHES-1 et ce diff n'était pas encore figé.
- Le texte du §7.1 a été écrit d'après une sonde sur `_lire` (`sonde-lire-types.txt`).
- Limites déclarées au §7.1 :
  - un booléen JSON passe dans `a` et, hors première ligne, dans `seq` ;
  - `de`, le `ws` de `point` et de `reprise`, et `jour` ne sont pas contrôlés.
- Si tu préfères un diff distinct pour I-2, CB-18f se scinde en deux.

## Vérifications sur l'état final (e9 et arbre complet)
- **Jobs s2bis** : python 3.10 à 3.13, tous VIVANT.
- **Matrice `-X dev -W error`** : 133 OK sur chaque version, 0 avertissement.
- **Job S2** : VIVANT, Ran 406, 80,8 s.
- **Crochets** : 54 ok. **Runner** : 33 ok.
- **xtask** : S-G1 à S-G8 VERT ; fmt, no_std et clippy VERT ; S-G9 ROUGE avec la seule violation `docs/17-modele-de-menace.md:70`. Verdicts identiques au témoin de base.
- **R-13** : 22 fichiers touchés, 0 occurrence ; contrôle positif 2/2.
- **Secrets** : 22 fichiers OK, en mode index et en mode `--tree`, dans un dépôt jetable sans commit.
- **R-8** : bibliothèque standard seule.
- **Série** : e0 + les neuf diffs = e9 ; la série s'applique aussi sur 3164348.

## Écarts
1. **CB-18c scindé** en CB-18c et CB-18d : le diff unique faisait 259 lignes de code.
2. **Campagnes refaites** (passages non valides archivés, jamais comptés) :
   - CB-18a : témoin d'abord tué (plancher 114, Ran 117), plancher relevé à 117.
   - CB-18b : M-18b-10 vivant au 1er passage, test réécrit, 13/13 au 2e.
   - CB-18c avant scission : M-18c-11 FATAL à 300 s (non compté), puis 17/18, puis 18/18.
   - CB-18d : campagne rejouée après le passage à `pathlib` (ResourceWarning).
   - CB-18e : 10/11 à des délais de 0,4 s (M-18e-09 vivant), d'où l'assertion ajoutée ; 11/11 ensuite.
   - CB-18f : 11/11 avant I-2, puis 20/20 sur l'état final.
   - SEGMENT-JOUR et ENTIER-ECRIVAIN : passés d'abord sur brouillon, puis rejoués sur e8 et e9.
3. **Nature des rouges** :
   - Deux tests ont donné ERROR, non FAIL, sur le squelette (câblage, `run_params`). Leur rouge d'assertion est montré par mutant dans `nature-rouge-*.txt`.
   - Le rouge de CB-18e est montré par mutation : il n'y a pas de code de production.
   - Le test de CB-18f vient après la retouche de CB-18a ; son rouge est montré sur le texte de la base.
4. **Retouches de texte après campagne** (FORMAT, docstrings de `boucle`) : sans effet sur les tests.
5. **Méthode et périmètre de l'interdit de recherche récursive** : j'ai utilisé `diff -r`, `git diff --no-index`, `find -name __pycache__` et `rm -rf` sur mes mini-arbres, qui contiennent une copie de `docs/adr-0029/s2bis`, et `du -s` une fois sur des sous-dossiers non-docs. Comparaison et nettoyage seulement, aucune recherche de contenu. Pour situer B.60 et B.63, j'ai affiché les titres des blocs de l'annexe B ; aucun autre bloc n'a été lu, et B.64 n'est pas lu.

## Items à former (PAROXYSME)
1. **SHOGEN-S2-PY310-1** (proposé) : la suite s2-harness est rouge sous Python 3.10, avec 77 échecs et 3 erreurs, ensembles identiques à la base et à l'état final. Causes : `hashlib.file_digest` (3.11+) et le format des noms de `unittest -v`. Le CI tourne en 3.12.3, mais la règle « 3.10 à 3.13 » du brief n'est tenue que pour s2bis et pour le test neuf d'ENREG-ROLE.
2. **SHOGEN-S2BIS-LIRE-BOOLEENS-1** (proposé) : les limites de type de `_lire` déclarées au §7.1. À trancher avec le lecteur RB-1 : serrer des deux côtés, ou garder.
3. **SHOGEN-S2BIS-CITATIONS-ADR-DECALEES-1** (proposé) : les citations « ADR-0029 l.N » du FORMAT, du code et de mes tests suivent l'ADR au commit eb518b3. Les ajouts datés b9ba2b4 et 435fa12 ont décalé §2.9 de +2 : le budget passe de l.233 à l.235.
4. **Registre biblio** : la ligne de rfc-1035 dans `biblio/INDEX.md` (l.380) ne liste pas §2.3.3, que le FORMAT §12 cite (je l'ai lu, l.478-482, sha256 identique).
5. **Banc du réviseur RB** : son cas C5 est à mettre à jour, il n'a plus d'objet après ENTIER-ECRIVAIN.
6. **Limite de SEGMENT-JOUR** : un fichier d'un jour futur laissé au dossier par erreur fixerait les segments neufs à ce jour. Ce n'est pas détecté. Par ailleurs, au-delà du segment 9, l'ordre des noms affiché par `ls` n'est plus l'ordre numérique.
7. **Dépendance nouvelle de la suite s2bis** : `test_format` lit le FORMAT à côté du paquet. Le e2e suppose `/bin/echo` (Linux). Sous une charge extrême, toutes les requêtes D-4 et D-5 pourraient rester nulles.
8. **Relevés pendant le lot (avant la reprise de contexte)** :
   - commit non vérifié sur l'observateur (DB-2) ;
   - calendrier absent de `run_params` ;
   - un refus de l'écrivain arrête le processus (à revoir avec les décodeurs de P2) ;
   - fichiers de configuration scellés réels absents ;
   - SIGTERM sans `finally` (DB-3) ;
   - `retard_max` ≥ 0 du e2e dépend de l'horloge de l'hôte ;
   - le job S2 n'a pas `--egal`, donc un retour de `PLANCHER` à 405 passerait ;
   - chemin TLS réussi testé par couche injectée seulement (TLS-REUSSI-1 reste ouvert) ;
   - limite des sondes faussée par un saut mural entre E et le relevé ;
   - format d'hôte non contrôlé au chargement ;
   - retour anticipé d'`attendre` inchangé.

## Estimation révisée (recomptée par numstat, [inféré] pour le futur)
- **P1 mesuré** : 4 068 lignes de code, dont tranche A 1 323, tranche B 1 740, tranche C 878 et N-1 + I-1 127, contre 1 620 au G0, soit ×2,51. Le premier jet seul fait 3 047 lignes, soit ×1,88.
- **Reste de P1** : corrections de la G2 complète, environ 300 à 450 lignes, en 2 à 3 diffs.
- **P2** (CB-6 à 9, 12, 13, 15, 16, 17 ; 1 510 lignes au G0) : 2 900 à 3 800 lignes. CB-14.k ajoute 660 à 1 760 lignes. Soit environ 20 à 30 diffs.
- **CB-19** : environ 400 lignes, 2 diffs.

## Journal G1

### Sources [lu]
- Le brief et ton message d'ajout.
- Le G0 COLLECTE : G0-COLLECTE-RECALC-DEPLOI.md, avec son ajout daté de 3164348 ; PROPOSITION.md l.204-232 (table, dont CB-18 à la l.226) ; AVIS.md.
- ADR-0029 l.231-242 : aux commits 122c670, eb518b3 et 3164348.
- ANNEXE-B : B.60 (l.992-1015) et B.63 (l.1045-1058) seulement.
- FORMAT et METRIQUES ; la liste des pièces `revue-p1a` et `revue-p1b`.
- Le code et les tests du collecteur, `verdict-suite-s2.py`, l'en-tête de `gate-secrets.sh`, gates.yml, `oracle_record.py` et ses tests, `xtask/src/sg5.rs` l.1-70.
- RFC 1035 (`biblio/rfc-1035-dns-implementation-2026-10-05.txt`, sha256 d14ae809…) : l.478-482, 1401, 1530 et 2526-2556 ; INDEX.md l.380.
- Pièces du scratchpad :

| pièce | sha256 |
|---|---|
| `lo_up.py` | b532be4b… |
| `isole.sh` du réviseur | ebaa1c78… |
| `sonde_sommeil_mural_2.py` | 405c2d23… |
| `sonde_sommeil_mural_cc.py` | 848e4a9b… |
| `rb1/g2/outils/banc_lecteur.py` (l.1-150 et 355-375 lus, lancé tel quel) | 2e320fd1… |
| `banc_lecteur_py312.txt` | 0363060d… |
| `banc_lecteur_python3.10.txt` / `banc_lecteur_python3.13.txt` | 797608de… |
| `survivants-non-equivalents.txt` | f4979f33… |
| diffs RB-0a à RB-6b (sommes listées en preuve) | — |

### [2nd]
- La description de N-1, I-1 et I-2 dans ton message. Je l'ai vérifiée par mes rouges et par le banc.

### [abs]
- B.64 ; G2-RB-T1, AVIS-RB-T1 ; toute doc Python en ligne (réseau coupé, comportement mesuré localement).

### Commandes principales
Toutes lancées sous `isole.sh` : `unshare -n`, `lo` allumée, variable scellée retirée.
- `job.py` (runner, puis ligne de gates.yml, borne de 300 s) ; `campagne.py` ; `etats*.sh`, `verif_finale*.sh`, `matrice_s2.sh`, `banc_rejoue.sh`, `banc_propriete.py`, `nature_rouge.py`, `sonde_lire_types.py`.
- `cargo --locked xtask verify` ; `gate-secrets.sh` (index et `--tree`) ; grep R-13 (motif sha a1a6e684…).
- Sorties intégrales dans `preuves/` (190 fichiers).

### Chiffres recomptés
- Lignes : `git apply --numstat`.
- P1 : `git show --numstat` sur les 23 commits de P1.
- Tests : `Ran` dans les sorties des jobs.

## Exposition
- Copies extraites sans `docs/15-*`, `docs/16-*`, `docs/pocket-report`, `docs/rapports`, `docs/adr-0025`, `docs/adr-0028/monark-m009a` ni `docs/adr-0028/execution` ; aucun de ces chemins ouvert.
- Aucun `*.jsonl` réel ouvert : seulement des journaux synthétiques de tests ou du banc dans mon TMPDIR. Je n'ai pas non plus ouvert le transcript de session.
- Aucune pièce D.2 ouverte. `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée.
- Un `ps` antérieur m'a montré des lignes de commande d'autres workers.
- Je n'ai arrêté que mes propres groupes de processus.

## Livrables
Dossier : `<scratchpad>/s2bis/cb18/`
- `diffs/` (9 fichiers, dans l'ordre d'application) :
  1. CB-18a.diff
  2. CB-18b.diff
  3. CB-18c.diff
  4. CB-18d.diff
  5. CB-18e.diff
  6. CB-18f.diff
  7. ENREG-ROLE.diff
  8. SEGMENT-JOUR.diff
  9. ENTIER-ECRIVAIN.diff
- `mutants/` (10 jeux).
- `outils/`.
- `preuves/` (190 fichiers).
- `etapes/e0` à `etapes/e9` (mini-arbres légers).
- `SHA256SUMS` : 232 lignes, contrôle OK ; son propre sha256 : 3641e4318ba9f09fd91a0f5d2b0275b18350be266b5d67aba2b23e28cc180da7.

Copies lourdes nettoyées (base, copies de travail, cible cargo, brouillons) : 177 Mio puis 188 Mio libérés, mesurés par `df`.
