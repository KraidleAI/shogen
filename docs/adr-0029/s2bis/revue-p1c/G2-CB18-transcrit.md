# Relecture G2 neuve — P1 tranche C (transcrit)

> Transcription par l'orchestrateur le 2026-10-05 08:46:06 UTC du rapport rendu par message par le réviseur G2 (agent a2fb4f197970d4d60) ; contrôle FM-1.1 du transcript : fragments_l51_l14 = 0. Texte du réviseur ci-dessous, sans retouche.

Gate 0 : claude-opus-5-5. C'est l'identifiant exact du modèle sous lequel je tourne. L'effort « max » demandé n'est pas observable de l'intérieur.

# Relecture G2 neuve : P1 du collecteur S2-bis, tranche C (CB-18a à CB-18f, ENREG-ROLE, SEGMENT-JOUR, ENTIER-ECRIVAIN)

**Verdict : ACCEPTE-AVEC-CORRECTIONS.** Liste fermée : C-1 à C-4, détaillées plus bas.

Début 07:48:25 UTC, fin 08:43 UTC (`date -u`). Aucune opération git en écriture dans /home/user/shogen : lectures en `--no-optional-locks` et `git archive` seulement. HEAD lu au début et à la fin : 31643485, égal à la base du brief.

## Résumé court
- **Série et jobs.** Les neuf diffs s'appliquent tels quels sur 3164348, sans décalage. Ils ajoutent tous au plus 200 lignes de code.
  - Chaque état est vert seul, par la commande du job (runner, puis la ligne de gates.yml de l'état), au plancher exact : Ran = 117, 122, 124, 126, 127, 129, 129, 131, 133.
  - Le job S2 donne Ran ≥ 405 avant ENREG-ROLE, puis Ran ≥ 406 après.
- **Items.** Les huit items sont fermés chacun par un test qui échoue sans le correctif (rouges rejoués). Les sondes de sommeil mural sont rejouées :
  - avant : −999 728 µs (sonde du worker) et −1 499 777 µs (sonde du réviseur) ;
  - après : +231 µs et +309 µs.
- **Écrivain après N-1 et I-1.**
  - Le banc RB a C5 mis à jour : ni collision ni ordre faux, sur 2 000 puis 20 000 graines. Sur e7 (avant N-1), le même banc donne collision 2 et ordre 1.
  - Mes scénarios donnent 7/7 sur l'état final, et ma propriété 0 écart sur 2 000 graines.
  - La borne de 640 chiffres ne dépend pas du réglage de l'interpréteur, mesuré sous 3.10 à 3.13.
- **Ce qui manque.**
  - La règle `budget` de CB-18c omet la tolérance de départ de 5 s du budget de l'ADR, que le FORMAT §14.1 dit pourtant appliquer (C-1).
  - Le test d'ENREG-ROLE ne tue pas une lecture hors du job (C-2).
  - Deux corrections documentaires (C-3, C-4).
  - Mon essai de contournement trompe l'enregistreur par une ligne leurre. Une des deux formes trompe aussi le cas K-02 du runner : à former en item.

## 1. Série
- **Pièces.** SHA256SUMS du worker : 232/232 OK ; son propre sha256 vaut 3641e431…, comme il l'annonce.
- **Application.** Copie `git archive 3164348`, exclusions du brief. `git apply` en série, sans décalage.
- **Lignes ajoutées**, recomptées par `git apply --numstat`, toutes égales au tableau du worker :

| diff | code | docs |
|---|---|---|
| CB-18a | 118 | 41 |
| CB-18b | 186 | 55 |
| CB-18c | 177 | 46 |
| CB-18d | 128 | 34 |
| CB-18e | 194 | 28 |
| CB-18f | 75 | 37 |
| ENREG-ROLE | 77 | 0 |
| SEGMENT-JOUR | 75 | 43 |
| ENTIER-ECRIVAIN | 52 | 30 |

- **Jobs**, par mon outil `jobg2.py` (étapes `run:` lues dans le gates.yml de chaque état, python3 = python3.12, `isole.sh` du réviseur P1-B, borne de 300 s) :
  - e0 à e9 : VIVANT ; verdicts « Ran = 114, 117, 122, 124, 126, 127, 129, 129, 131, 133 » ; runner 33 ok.
  - Job S2 : e6 « Ran ≥ 405 », e7 et e9 « Ran ≥ 406 », skipped=2 nommés.
  - sim-bis e9 : Ran = 93.
  - Job s2bis de e9 aussi sous python3.10, 3.11 et 3.13 : VIVANT, 133.
- **Comparaison au worker.** Mon arbre final est identique octet pour octet au mini-arbre e9 du worker sur 21 des 22 fichiers touchés. gates.yml ne diffère que par le plancher sim-bis (93 au lieu de 49), comme le worker le déclare.

## 2. Fermeture des items : rouge sans correctif, rejoué
| item | rouge observé | vert |
|---|---|---|
| ECRIVAIN-USAGE-1 | CB-18a : 3 FAIL (fil, refus nommés, `_terminal`) | OK |
| ECRIVAIN-USAGE-1, point d'entrée | 2 ERROR (`main` absent) ; rouge d'assertion par mes mutants MR-19 (`finally` retiré) et MR-20 (`except` restreint), TUÉS | OK |
| PLAN-CABLAGE-1 | `test_nom_du_plan…` FAIL (CB-18b) ; câblage : MR-21 et M-18c-15 TUÉS | OK |
| SONDES-ECHEANCE-1 | 2 FAIL (CB-18b) | OK |
| SOMMEIL-MURAL-1 | 2 sous-tests FAIL ; sondes détaillées sous le tableau | OK |
| FORMAT-RETOUCHES-1 et I-2 | `test_format` : 2 FAIL sur le texte de la base, 1 FAIL sur celui de e5 | OK sur e6 |
| SEGMENT-JOUR-1 | 3 FAIL | OK |
| ENTIER-ECRIVAIN-1 | 2 FAIL | OK |
| ENREG-ROLE-1 | 1 FAIL | OK |

- **Sondes de sommeil mural**, les deux sondes de P1-B lancées telles quelles, deux passages chacune :
  - sur e1 : −999 728 et −999 777 µs (worker) ; −1 499 777 et −1 499 786 µs (réviseur) ;
  - sur e9, où `boucle.py` est égal à celui de e2 : +231 et +249 µs ; +309 et +311 µs.
- **RFC 1035.** J'ai lu §7.3 (l.2526-2556) et §2.3.3 (l.478-487) de `biblio/rfc-1035…`, sha256 d14ae809…. Le texte du §12 est fidèle.
- **Test instable.** Dans le rouge de CB-18b, un 9e échec est apparu : `test_disque_et_empreinte_du_resolveur`.
  - Ce test vient de CB-11 et n'est pas touché par le lot.
  - Il compare deux lectures de `statvfs`, et l'espace libre a bougé de 4 096 octets entre les deux sous écritures concurrentes.
  - L'échec ne s'est pas reproduit en 30 passages : à former en item.

## 3. Conformité de CB-18 à la proposition
- **Conforme :**
  - point d'entrée `pool` (`python3 -m shogen_s2bis.collecte`), sorties 0/1/2, journal fermé dans `finally` ;
  - descripteur ;
  - `run_params` : commit, sha256 des trois fichiers lus, contenus, version de Python ;
  - configurations contrôlées (E-C-02), sous treize règles nommées ;
  - bout en bout : deux exécutions et une reprise. L'exécution A passe par `main`, la B par `__main__` avec le TLS par défaut. Les champs exacts sont contrôlés contre le FORMAT §2, §9, §11 à §14 ; je les ai recontrôlés champ par champ.
- **Écarts :**
  - C-1 (budget) ;
  - E-C-23 exige le **calendrier** dans `run_params`. Il est absent, et aucune configuration de calendrier n'existe au collecteur. Le worker l'a relevé sans le former : item.
  - Le FORMAT §11.5 (ordre de la fenêtre) ne place pas `run_params` en tête de la première fenêtre d'une exécution : observation.
  - Aucune règle ne contrôle `places` ≥ nombre de formes (ADR l.234 : pool « dimensionnée sur le nombre de lectures »), ni la forme de `hote` : item.

## 4. Écrivain après N-1 et I-1
- **Banc RB tel quel** (2e320fd1…) sur e9 : il s'arrête à C5 sur `JOURNAL/entier`, ce qui est attendu. Les cas C6 à C10 n'avaient pas été rejoués par le worker sur e9.
- **Ma copie, où seul C5 change** (765fc79d… ; 701, 641 et −641 chiffres refusés ; 640 chiffres écrits puis relus) :
  - sur e9 : 20/20 contrôles ok, différentiel de 3 000 altérations, 2 000 graines. Ni `collision_ecrivain` ni `ordre_noms_ecrivain` (1 764 journaux, 8 717 redémarrages).
  - 20 000 graines et 5 000 altérations : 0 écart (17 443 journaux, 86 473 redémarrages).
  - sur e7 : C5 en échec, collision 2, ordre 1, comme le réviseur RB.
- **Mes scénarios** (`scenarios_jour.py`) sur e9 : 7/7. Sur e7 : 3 `FileExistsError`. Scénarios :
  - jour futur vide ;
  - 12 segments d'un même jour ;
  - 50 redémarrages ;
  - horloge reculée de 4 jours ;
  - N-1 ;
  - saut de 3 jours puis retour ;
  - 12 fichiers vides du lendemain.
- **Ma propriété** (`propriete_jours.py`) : reculs de 1 à 5 jours, fichiers parasites de jour futur qui trient après tout fichier présent.
  - e9, 2 000 graines : 1 746 ok, 0 écart, 0 exception ; 17 085 redémarrages, segment maximal 11.
  - e7, 500 graines : 135 écarts et 82 `FileExistsError`.
  - Un fichier inséré au milieu de la chaîne n'est pas productible par l'écrivain. Le lecteur le signale, ce qui est le bon classement.
- **Borne de 640 chiffres**, sous 3.10.20, 3.11.15, 3.12.3 et 3.13.14 :
  - réglages essayés : limite par défaut (4 300), 640, 0, 100 000, et `-X int_max_str_digits=640` ;
  - 641, −641, 5 000 chiffres et la forme imbriquée sont refusés en `JOURNAL/entier` ; 640 chiffres sont écrits et relus intacts par `_lire` et par le lecteur RB ; le seuil vaut 640 partout.
  - Avant I-1 (e7) : `JOURNAL/type` à la limite 640 ; à la limite 0, 641 et 5 000 chiffres sont écrits puis vus en queue par le lecteur RB.
- **Limite I6 du worker confirmée.** Un fichier vide du 10-07 laissé au dossier fait écrire trois jours de fenêtres dans `…-10-07-1`. Au-delà de 9 segments, l'ordre affiché par `ls` n'est plus l'ordre de la chaîne.
- **Trou de couverture.** Mon mutant MR-26 (segments à deux chiffres invisibles) survit : la suite n'a aucun test à 10 segments ou plus.

## 5. ENREG-ROLE
- **Refus gardés.** Le diff n'ajoute que `JOBS`, `ligne_du_job` et les entrées de `COMMANDES`, et modifie deux lignes d'`enregistrer`. Aucun refus existant n'est touché.
  - test_oracle_record : 12 OK sous 3.11 à 3.13.
  - Le test neuf passe sous 3.10 et 3.13 en `-X dev -W error`.
  - Sous 3.10, l'échec de `test_enregistrement_champs_et_sha` existe déjà à e6 (format des noms de `-v`).
- **Lecture de la ligne.** Elle est lue au gates.yml de l'extraction du commit. Le commit « ko » du test le prouve.
- **Contournement** (`contournement_role.py`, avec le K-02 réel du runner en regard) :
  - C1, leurre dans un bloc `name: >` alors que la vraie étape lance `--plancher 0` sans `--egal` : l'enregistreur rend exit 0 sur la ligne leurre **et** K-02 passe. Les deux sont trompés.
  - C4, leurre dans une étape `if: false` : l'enregistreur est trompé, K-02 échoue.
  - `|| true`, ligne répétée, ligne commentée : refusés par les deux.
  - `set +e … exit 0` : l'enregistreur rend exit 1. Il n'est pas trompé, mais K-02 passe (limite de K-02, antérieure au lot).
  - Plancher faux : exit 1.

## 6. Rouge et vert
Six pas rejoués : CB-18a, CB-18b, CB-18d, ENREG-ROLE, SEGMENT-JOUR, ENTIER-ECRIVAIN, plus le texte de CB-18f. Les tests de l'état N sont lancés contre le code de l'état N−1, puis contre celui de l'état N. Preuves : `rouge-vert.txt` et `rouge-vert-format.txt`.

## 7. Mutants
Commande du job, borne de 300 s, FATAL au dépassement.

**Mes 25 mutants**, sur e9 : 19 TUÉS, 6 VIVANTS, 0 FATAL. Les survivants :
- MR-09 : tuple non parcouru. Équivalent en pratique, aucun tuple n'atteint l'écrivain en P1.
- MR-17 : budget refusé à l'égalité (traité par C-1).
- MR-18 : délai des sondes refusé à l'égalité.
- MR-22 : commit en majuscules admis.
- MR-24 : ligne cherchée au-delà du job (traité par C-2).
- MR-25 : `PLANCHER` S2 rendu à 405. Il survit parce que le job S2 n'a pas `--egal`.

**Mes deux mutants supplémentaires :**
- MR-12b est TUÉ. MR-12 l'avait été aussi, mais il retirait l'attente elle-même : je l'ai refait en MR-12b.
- MR-26 survit (§4).

**Échantillon du worker** : 27 mutants, 3 par jeu, tirés par `random.Random(18)`, rejoués sur e9. 27 TUÉS, chacun par son test visé, 0 FATAL.

**Journaux du worker recomptés** : 115/115 TUÉS par le test visé, 0 FATAL, témoins verts.

## 8. CI
- gates.yml : seul le plancher s2bis bouge (114 → 133). `PLANCHER` S2 passe de 405 à 406. Ce sont deux serrages ; aucune gate n'est affaiblie.
- **Avis sur `--egal` pour le job S2.** Son absence est conforme à l'adjudication Q-2 (B.60 ; G2-P1A l.298-304 : `--egal` réservé au job s2bis, couplage avec le test de comptes de B-SEG-1). Le lot a relevé `PLANCHER` au compte exact, le maximum que permet « ≥ ».
  - MR-25 montre la conséquence : un plancher S2 rendu à 405 passe.
  - Ce n'est pas un défaut du lot. Je recommande que l'orchestrateur tranche par écrit l'extension de `--egal` à S2 : la suite S2 évolue de nouveau (outillage), et la règle PLANCHER-SUIVI-1 n'y repose plus que sur la discipline. L'extension demande de retoucher la regex de K-01.

## 9. Interpréteurs et contrôles statiques
- **Matrice** `-X dev -W error` : s2bis 133 OK sous 3.10, 3.11, 3.12 et 3.13, 0 avertissement.
- **S2 sous 3.10** : 405 tests à e0, 406 à e9, failures=77, errors=3 dans les deux cas. Les 80 identifiants sont identiques.
- **R-13** : motif de la gate appliqué aux 21 fichiers de sa portée, 0 occurrence ; contrôle positif 1.
- **R-8** : imports ajoutés, tous de la bibliothèque standard.
- **Octets 92** : 0 dans les lignes ajoutées. Ceux qui restent dans les diffs sont des lignes de contexte.
- **Secrets** (dépôt jetable, 22 fichiers, modes index et `--tree`) : OK.
- **Crochets** : 54 ok.
- **xtask** (`cargo --locked xtask verify`, lignes de verdict seules), identique sur e9 et sur le témoin e0 :
  - S-G1 à S-G8 VERT ;
  - fmt, no_std et clippy VERT ;
  - S-G9 ROUGE, seule violation `docs/17-modele-de-menace.md:70`.

## 10. Avis sur les écarts et les items du worker
**Écarts**
- **E1 à E3 admis.**
  - La scission de CB-18c (259 lignes) donne 177 + 128.
  - Les campagnes refaites suivent les règles de témoin et de FATAL.
  - Les rouges d'erreur sont complétés par des mutants.
- **E4 admis** pour les tests. En revanche, METRIQUES reste faux d'une ligne (C-3).
- **E5 admis**, sans exposition. J'ai fait un écart de même nature (voir « Écarts du réviseur »).

**Items**
- **I1, SHOGEN-S2-PY310-1 : confirmé, antérieur au lot.** Causes : `hashlib.file_digest` (3.11 et plus) et le format des noms de `-v`.
  - Conséquence à trancher : le rendu de S2-bis sera calqué sur `rendu_unique`, qui demande `file_digest`. Il faut donc fixer le Python minimal du recalcul et de s2-harness.
  - La règle « 3.10 à 3.13 » ne tient aujourd'hui que pour s2bis.
- **I2, LIRE-BOOLEENS : confirmé** sur `_lire` comme sur le lecteur RB. Le risque est faible, car la ligne doit être canonique et chaînée. Recommandé : serrer des deux côtés avant le gel.
- **I3, CITATIONS-ADR-DECALEES-1 : confirmé.**
  - §2.9 commence l.229 à e16956b et eb518b3, puis l.231 dès b9ba2b4. Ce commit seul décale : 435fa12 ne décale pas §2.9, contrairement à ce que dit le worker.
  - Les citations suivent la convention du G0 (ADR à e16956b), mais le FORMAT, destiné au sceau, ne la dit pas. Recommandé : l'écrire dans son en-tête avant le gel.
- **I4 : confirmé**, voir C-4.
- **I5 : confirmé.** Le banc RB doit mettre C5 à jour ; ma copie montre la conduite neuve.
- **I6 : confirmé** (§4). La rétention de DB-4 ne doit pas se fonder sur le nom des fichiers. Option avant le gel : numéro de segment sur 3 chiffres.
- **I7 : confirmé.** Le e2e est stable sur 30 passages : 20 à charge 5,6 à 6,2 (autres agents), puis 10 sous 4 boucles de calcul à charge 6 à 11,2.
- **I8 : d'accord.** À former en priorité : le calendrier (E-C-23), et l'arrêt du processus sur un refus de l'écrivain. Ce dernier ferait une boucle de crash, avec un trou à chaque relance, si un décodeur de P2 rendait un flottant.

## Corrections (liste fermée)
- **C-1 (CB-18c : `entree.py`, FORMAT §14.1 et §14.4, `test_entree.py`).** La règle `budget` (`plus grand décalage + delai + marge ≤ delta`) n'inclut pas la tolérance de départ de D-2.
  - L'ADR fixe cette tolérance à 5 s : l.107 telle que reformulée par l'ajout daté (l.397) ; l.233-234 à e16956b, « la tolérance de départ, le délai et la marge tiennent dans δ (5 + 10 + 1 ≤ 20) » et « 5 + 4 + 10 + 1 = 20 ≤ 20 s ».
  - Le FORMAT §14.1 l'annonce pourtant comme « budget de l'ADR-0029 l.233-234 ».
  - Mesure (`sonde-budget.txt`) : cinq lectures espacées sur un hôte, avec un délai de 14 s puis de 15 s, sont **admises** ; l'ADR donne 24 et 25 > 20.
  - **À faire :** serrer la règle. Forme proposée : un champ scellé `tolerance` (µs) dans `formes.json`, 5 s en production, porté par `run_params`. Une constante de 5 s refuserait les configurations de test à w = 1 s. Une autre forme demande une adjudication écrite.
  - Mettre à jour le FORMAT, et ajouter un test à la borne : égalité admise, 1 µs de plus refusée. Ce test tue MR-17.
- **C-2 (ENREG-ROLE : `test_oracle_record.py`).** La docstring du test annonce « Rougit si … autre job … lu », mais MR-24 survit.
  - À faire : ajouter un cas où la ligne du vérificateur de s2bis ne figure que dans un job suivant (`sim-bis-unittest`). Refus attendu avant toute écriture ; montrer le rouge avec MR-24.
- **C-3 (METRIQUES-S2BIS.md, section CB-18b).** `shogen_s2bis/collecte/boucle.py` compte 132 lignes à e2 et à l'état final, non 131.
- **C-4 (biblio/INDEX.md, l.380, ligne de rfc-1035).** Ajouter §2.3.3 aux sections lues : le FORMAT §12 le cite depuis CB-18a. Lecteurs : le worker de CB-18 et moi, l.478-487, sha256 d14ae809…. À faire par l'orchestrateur au versement.

## Items à former (règle PAROXYSME)
Propriétaire : l'orchestrateur.
- **SHOGEN-S2BIS-RUNPARAMS-CALENDRIER-1** : calendrier exigé par E-C-23, absent de `run_params`. Déclencheur : gel du collecteur.
- **SHOGEN-S2BIS-LIGNE-JOB-LEURRE-1** : leurres C1 et C4 (§5). Remède :
  - ne lire la ligne que dans les blocs `run:`, avec un seul analyseur pour K-01 à K-03 et `ligne_du_job` ;
  - appliquer dans `ligne_du_job` les exclusions de K-02 (`if:`, `continue-on-error`) ;
  - en attendant, le G3 opérant lance le runner avec l'enregistreur.
  - Déclencheur : avant l'enregistrement de rôle de la G2 complète de P1.
- **SHOGEN-S2BIS-TEST-DISQUE-INSTABLE-1** : la double lecture de `statvfs` peut fausser le job et le classement des mutants. Remède : injecter `statvfs`, ou ne comparer que `total`.
- **SHOGEN-S2BIS-CONFIG-REGLES-1** : contrôler `places` ≥ nombre de formes, la forme de `hote` et celle de `chemin`. Ajouter les tests de borne qui tuent MR-18 et MR-22. Déclencheur : G0 de CB-6 à CB-9.
- **SHOGEN-S2BIS-SEGMENTS-10-1** : test à 10 segments ou plus dans la suite (tue MR-26), à joindre à I6.
- **SHOGEN-S2BIS-ECRIVAIN-REFUS-ARRET-1** (relevé du worker) : déclencheur, G0 de CB-6.
- **SIGTERM sans `finally`** : à traiter à DB-3 (`KillSignal` ou gestionnaire).
- **Décision `--egal` pour le job S2** (§8).

## Observations
- Le FORMAT §11.5 ne mentionne pas `run_params` dans l'ordre de la fenêtre.
- MR-09 : ajouter un cas tuple au test des 640 chiffres, qui annonce « à toute profondeur ».
- PROPOSITION §1.1 dit « rien ne change dans s2-harness/ » et §2.5 « s2-harness inchangée (405) ». ENREG-ROLE change les deux (406). L'écart est autorisé par B.60 et par le brief ; il reste à consigner au commit.

## Écarts du réviseur
- **E-1.** Deux `du -sh` sur mes copies (base, puis dossier de travail), pour une mesure de taille seulement. J'ai utilisé `df` ensuite.
- **E-2.** 20 passages du seul test disque sur e0 sans `unshare`. La garde réseau du paquet de tests était active, et le test ne fait aucun appel réseau.
- **E-3.** Gate des secrets lancée sans `unshare` (git local et grep).
- **E-4.** Le banc RB n'a pas été modifié en place : je l'ai lancé tel quel, puis une copie où seul C5 change (diff montré).
- **E-5.** `find travail -type f` sur mon propre dossier, pour SHA256SUMS.
- **E-6.** `ps` m'a montré les lignes de commande d'autres agents (rb1/corr, sim3/corr). Je n'ai arrêté que mes groupes de processus : PID 24325, 20082, 19073 et les boucles de charge 24792 à 24795.
- **Exposition.** Aucun `*.jsonl` réel (seulement des journaux synthétiques), aucune pièce D.2, aucun dossier exclu. `SHOGEN_S2_CAMPAGNE_CONTROL` n'a jamais été posée.

## Journal G1
**[lu]**
- Les briefs et le rapport : BRIEF-G2 7538795d, RAPPORT transcrit ea24dd5e, BRIEF-CB18 17e03a1a.
- G0 et AVIS en entier ; PROPOSITION l.1-460, 640-700 et 780-810.
- ADR-0029 :
  - à 3164348, l.225-250 et l.397 ;
  - à e16956b, l.106-108 et l.233-234 ;
  - position de §2.9 à six commits.
- ANNEXE-B : B.60 (l.992-1015) et B.63 (l.1045-1059) seulement.
- Pièces de revue : G2-P1A l.296-306 ; P1-B, lignes E-4 et sommeil.
- Pièces du recalcul : G2-RB-T1 (N-1, I-1, banc) ; RAPPORT-WORKER-RB l.142-143 ; banc_lecteur.py en entier ; lecteur RB l.1-142.
- FORMAT final en entier ; les 9 diffs en entier ; code de base et code final.
- RFC 1035, l.478-492 et 2526-2560 ; INDEX.md l.380.
- Sondes et outils de P1-B : 405c2d23, 848e4a9b, b532be4b, ebaa1c78.

**[abs]** : AVIS-RB-T1, B.64, les autres blocs de l'annexe B, D.2, DECISIONS-ARCHITECTURE et AQT.

**[2nd]** : aucun chiffre repris sans le recompter. Python 3.12.3 de l'image CI est [lu] dans un commentaire de gates.yml, et [inféré] pour le runner.

**Commandes** (mes outils, sorties intégrales dans `preuves/`) :
- `jobg2.py`, `serie.sh`, `rouge_vert.sh` ;
- `banc*.sh`, `scenarios_jour.py`, `propriete_jours.py` ;
- `sonde_640.py`, `sonde_budget.py`, `contournement_role.py` ;
- `campagne_g2.py`, `matrice.sh`, `flaky_e2e.sh`, `secrets.sh`, `xtask.sh` ;
- le runner des crochets.

## Fichiers
Les copies, la cible cargo et les fichiers temporaires sont supprimés : environ 263 Mio libérés, mesurés par `df`.
- <scratchpad>/s2bis/cb18/g2/SHA256SUMS-reviseur (98 lignes, sha256 20ca574a…, contrôle OK)
- <scratchpad>/s2bis/cb18/g2/travail/outils/
- <scratchpad>/s2bis/cb18/g2/travail/preuves/
- <scratchpad>/s2bis/cb18/g2/travail/NOTES.md
