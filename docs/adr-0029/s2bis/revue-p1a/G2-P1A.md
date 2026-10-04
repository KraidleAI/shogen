# Relecture G2 de la partie P1 du collecteur de S2-bis, tranche A (CB-0a à CB-2c)

- **Réviseur** : `shogen-worker`, instance neuve ; n'a rien écrit du lot (règle 6). Reprise d'une première relecture
  interrompue avant son rapport : ses pièces (`g2/travail/`) n'ont servi que de point de départ, chacune vérifiée ou
  refaite (§12.4).
- **Gate 0** : modèle résolu **`claude-opus-5-5`** (identifiant exact déclaré par le harnais de la session) ; effort
  `max` déclaré par la commande, non observable de l'intérieur.
- **Horloge** (`date -u`) : début 2026-10-04 20:36:28 UTC ; rapport écrit à partir de 21:09:13 UTC (fin au §12).
- **Brief** : `scratchpad/s2bis/p1/g2/BRIEF-G2-P1A.md`, sha256 recalculé `37fa026c…48ae`. Rapport du worker
  `RAPPORT-WORKER-P1A.md` : `38417ad4…ca47`. Brief du worker `BRIEF-P1-A.md` : `842b70ac…8eaa`, égal à celui que
  le worker déclare.
- **Dépôt** : `/home/user/shogen`, branche `claude/compassionate-noether-szmdyj`, tête **`86c07ff`**
  (`86c07ffe5bc8…f070`), lecture seule ; aucune opération git en écriture.
  - `git status --porcelain` : vide à 20:36 et à 21:06 UTC.
  - À 21:12 UTC, 16 entrées « intent-to-add » apparaissent sous `docs/adr-0029/etude-marche/carto/`. Un autre agent les a
    posées pendant ma relecture : je ne les ai ni créées ni lues (noms vus par `git status` seulement).
  - La tête est inchangée. Mes copies viennent de `git archive HEAD`, que l'arbre de travail n'atteint pas.
  - Écritures dans `scratchpad/s2bis/p1/g2/` seulement (ce rapport, `reprise/`).
- **Contrat** : G0 `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md` ; PROPOSITION (contenu du G0) corrigée par
  l'AVIS ; ADR-0029 révision 3 avec son ajout daté du 2026-10-04 17:03:38 UTC.

## Résumé et verdict

**Verdict : ACCEPTE-AVEC-CORRECTIONS**, liste fermée **C-1 à C-6** (§9).

- **(1)** Les sept diffs s'appliquent en série sur la tête actuelle `86c07ff` (7 commits de documents après la base du
  worker `34a17d8`). Arbre obtenu égal aux 18 empreintes. Chaque diff a ≤ 200 lignes de code ajoutées (197, 160, 199,
  42, 64, 200, 136). Chaque état intermédiaire est vert à lui seul.
- **(2)** Conformes : E-C-01, E-C-02 (partiel déclaré), E-C-16, E-C-18, E-C-40, E-C-41 et §1 pt 6. Conformes avec
  réserves : E-C-19 et E-C-21. **Non conformes : E-C-22 et E-C-20**, sur deux défauts établis par sonde.
  - **C-1** : une fenêtre entamée sans marqueur est réadmise après un redémarrage dont l'horloge est en arrière des
    lignes déjà écrites. `window_start` se répète d'un démarrage au suivant. Un test du lot valide même ce cas : il
    ferme dans la seconde exécution une fenêtre ouverte par la première. Dans une même exécution, une fenêtre du jour J
    peut tomber dans le fichier de J+1, après la clôture de J.
  - **C-2** : après une erreur d'entrée-sortie, l'écrivain continue. Résultats : un marqueur en double après un `fsync`
    en échec ; une ligne collée au milieu d'un fichier, jamais déclarée ; une somme fausse (`sha256sum -c` en échec).
- **(3)** La chaîne, la forme canonique, le verrou, les six formes de queue testées et les sommes sont solides
  (références recalculées hors du code). Douze constats de sonde (§3), dont un défaut mineur : boucle infinie de
  `canonique` sur une structure cyclique (C-3).
- **(4)** Rouge puis vert rejoué sur les sept diffs (huit cas). Mutants :
  - 41 mutants à moi : 35 tués par le test visé, **6 vivants non équivalents**, 0 FATAL.
  - Les 32 mutants de la relecture interrompue, rejoués : 16 tués, **16 vivants** (bilan identique au sien).
  - Le score de 102 sur 102 du worker vaut pour son jeu à lui. Au total, 19 vivants distincts sont à tuer (C-4, C-5),
    plus 1 qui relève de Q-2.
- **(5)** Le comportement par défaut du vérificateur est inchangé (suite S2 : 405 tests, OK, skipped=2, conforme ;
  message identique). Mais la paramétrisation a ouvert un chemin non testé : un plancher par défaut ramené à 0 au point
  d'entrée (job S2) survit, et `if: false` sur un job passe K-01 et K-02 (C-4).
- **(7)** R-13 : aucun marqueur. R-8 : bibliothèque standard seule ; `fcntl` rend le paquet POSIX seulement. R-25 :
  tenu. `xtask` : S-G1 à S-G8 vertes ; S-G9 rouge sur une violation (`docs/17-modele-de-menace.md:70`), la même sans
  les diffs.
- **(6) et (8)** : avis motivés sur E-7 (a) à (f), Q-1 à Q-8 et I-1 à I-7. Six items neufs proposés (N-1 à N-6).

## 1. Contrôle (1) : application en série, tailles, empreintes

**Base.** La tête actuelle est `86c07ff`, soit 7 commits après `34a17d8` (`git rev-list --count`). Ces commits ne
touchent que `JOURNAL.md` et `docs/publication/envoi-preavis/` (deux fichiers `.md` et un PDF) : aucun chemin du lot.

**Copie.** `git archive HEAD` avec les exclusions du brief donne 679 fichiers. Pour chaque diff, dans l'ordre :
`git apply --check`, puis `git apply`. Résultat : 7 sur 7, puis 694 fichiers.
- 15 fichiers neufs : 12 sous `s2bis/` et 3 sous `docs/adr-0029/s2bis/`.
- 3 fichiers modifiés : `gates.yml`, `verdict-suite-s2.py`, `run-fixtures-verdict-suite-s2.py`.
- Rien d'autre ne change (`diff -rq` contre la base) ; `s2-harness/` est intact.

**Empreintes.**
- Diffs : 7 sur 7 égaux à `SHA256SUMS`.
- Fichiers finaux : 18 sur 18, contrôlés depuis la racine de l'arbre.
- Outils du worker : 8 sur 8.
- Défaut de forme (O-1) : `SHA256SUMS` mêle des chemins relatifs à `p1/` et à la racine de l'arbre. Lancé depuis
  `p1/`, `sha256sum -c` échoue sur les 18 fichiers finaux (« FAILED open or read »).

**Lignes ajoutées** (`git apply --numstat` ; un chemin sous `docs/` compte comme document) :

| diff | code | documents | retirées | fichiers |
|---|---|---|---|---|
| CB-0a | 197 | 33 | 0 | 7 |
| CB-0b | 160 | 40 | 15 | 5 |
| CB-1a | 199 | 60 | 1 | 5 |
| CB-1b | 42 | 17 | 9 | 5 |
| CB-2a | 64 | 24 | 9 | 5 |
| CB-2b | **200** | 36 | 14 | 5 |
| CB-2c | 136 | 28 | 13 | 6 |

Total : 998 lignes de code et 238 de documents, égal au tableau du worker.

**Chaque état intermédiaire est vert à lui seul.** t_k désigne `86c07ff` plus les diffs 1 à k. Mesures avec
`python3.12` :
- la suite s2bis, jugée par le vérificateur avec le plancher du `gates.yml` de l'étape, est conforme à chaque étape :
  t1 6 tests (sans job), t2 10, t3 14, t4 15, t5 16, t6 25, t7 34 ;
- le runner du vérificateur sort en 0 : 20 cas à t1, puis 27.

Le compte découvert est égal au plancher committé à chaque étape (SHOGEN-CI-PLANCHER-SUIVI-1 tenu).

**Verdict (1) : conforme.**

## 2. Contrôle (2) : conformité exigence par exigence

| exigence | constat | verdict |
|---|---|---|
| **E-C-01** (CB-0b) | Imports lus par `ast`. Admis : la bibliothèque standard et le sous-paquet. Refusés : `shogen_s2`, l'import relatif sortant, `importlib`/`__import__`, le sous-paquet sans règle. Rouge montré (`import shogen_s2` ajouté donne FAIL). | conforme ; limite : `exec`, `eval` et `getattr(builtins…)` ne sont pas vus (O-10) |
| **E-C-02** partiel (CB-0a) | Octets lus une fois ; sha256 de ces octets. Refus nommés `CONFIG/…` : champs exacts, types (`true` n'est pas un entier), bornes incluses, liste vide, clé double, flottant, NaN, entier de plus de 30 caractères, UTF-8, imbrication. `SHA_VALIDE` recalculé hors du code (`printf … \| sha256sum` donne `2485d525…2fa2`). | conforme ; `run_params` relève de CB-18 (déclaré) |
| **E-C-16** (CB-1b) | `flock` exclusif sans attente sur `<préfixe>.verrou`, pris avant toute lecture. Une seconde instance lève `JournalOccupe` sans rien écrire. Libération à `fermer`. | conforme ; O-2 : verrou gardé après un refus d'`ouvrir` |
| **E-C-18** (CB-1a) | `seq` ; `prec` = sha256 de la ligne, saut compris ; genèse de 64 zéros ; forme canonique. H1, H2, H3 et TETE recalculés hors du code (`printf` puis `sha256sum` ; « é » contrôlé par `od -c` : `303 251`) : égaux. | conforme |
| **E-C-19** (CB-1a) | `fsync` au marqueur seulement (espion par inode). Le point suit la fenêtre qui clôt l'heure. | conforme avec réserves : ordre `fsync`/point non testé (M-07 vivant, C-5) ; marqueur en double après un `fsync` en échec (C-2) ; aucun point quand la fenêtre de fin d'heure n'a pas de marqueur (O-4) |
| **E-C-20** (CB-2a, CB-2c) | Fichiers quotidiens, `cloture`, sommes au format de `sha256sum` : contrôlé par `sha256sum -c` sur un journal de 1 500 fenêtres avec reprise sur queue, 2 fichiers OK. La chaîne continue d'un fichier au suivant. | **non conforme sur deux points** : une fenêtre de J peut s'écrire dans le fichier de J+1 après la clôture de J (S-4, C-1) ; somme fausse après une écriture partielle (S-6, C-2) |
| **E-C-21** (CB-2b, CB-2c) | Reprise au dernier enregistrement intègre. Six formes de queue testées (ligne coupée, NUL, non canonique, mal chaînée, trop longue, imbrication). Queue jamais réécrite ; segment neuf ; repli sur le précédent. | conforme pour ces formes ; **non conforme** pour une queue née d'une erreur d'écriture en cours d'exécution, enfouie au milieu du fichier et jamais déclarée (S-6, C-2) ; chemins non testés (C-5) |
| **E-C-22** (CB-2c) | `trou` au marqueur qui suit, causes `arret`, `horloge_reculee` et `saut`. Fenêtre du redémarrage et fenêtres closes refusées. | **non conforme** : `window_start` répété d'un démarrage au suivant pour une fenêtre entamée sans marqueur (S-1, S-2), et un test du lot valide ce cas (C-1). La lecture « trou au marqueur suivant » plutôt qu'« à la reprise » est acceptable (O-8). |
| **E-C-40** (CB-0a) | Garde posée à l'import du paquet de tests ; `ReseauInterdit` dérive de `BaseException` ; boucle locale permise. | conforme ; `connect_ex` non testé (M-26 vivant, C-5) ; `sendmsg` non gardé (O-7) ; `_socket` (I-4) |
| **E-C-41** (CB-0b) | Fitness : frontière, réseau, déterminisme sous cinq graines, compilation avec avertissements en erreur. Baseline `METRIQUES-S2BIS.md` : lignes et tests par fichier recomptés, égaux à chaque étape. | conforme ; déterminisme limité à `config` (O-9) |
| **§1 pt 6** | Voir le détail sous le tableau. | conforme, sauf la protection par test des planchers et le refus de `if:` (C-4) |
| **§2.4** (familles « Chaîne » et « Fitness ») | Chaîne recalculée par un code indépendant ; espion de `fsync` ; seconde instance refusée ; queue conservée à l'octet ; bascule de 00:00 : tous présents. « Horloge reculée : aucun `window_start` répété » : **partiel**, le cas de la fenêtre entamée manque (C-1). Fitness `import shogen_s2` et vraie socket : présents. Format (CB-18) : hors tranche. | partiel (C-1) |

**Détail du §1 pt 6.**
- Job neuf `s2bis-unittest` sur `ubuntu-24.04`, checkout épinglé par SHA ; résumé final exigé ; aucun saut admis ;
  plancher relevé à chaque diff ; K-01 et K-02 lisent les étapes des deux jobs.
- Suite S2 inchangée (405 tests, OK, skipped=2) ; hook : 54 cas ; gate des secrets : 685 fichiers.
- `xtask` : voir le §7.

## 3. Contrôle (3) : robustesse du journal chaîné

Sondes à moi : `reprise/outils/sondes_g2.py` (`65fb54ef…c7b1`), sorties dans `preuves/sondes-g2.txt` (`1b4cfc8b…d632`).

Instants : WS = 2026-10-04 22:58 UTC ; m(n) = WS + n minutes. « Journal type » : marqueurs de m1 à m3, puis une lecture
m4 écrite sans marqueur (arrêt).

| n° | cas | constat | suite |
|---|---|---|---|
| S-1 | journal type, redémarrage horloge à m(−8), puis `ecrire("lecture", m4)` et `marqueur(m4)` | **admis** : fenêtres écrites lecture 4, lecture 4, marqueur 4 | C-1 |
| S-2 | journal type, redémarrage à m3 (fenêtre du dernier marqueur), puis `ecrire(m4)` | **admis**. Le test `test_cause_remise_a_saut_par_un_marqueur_sans_trou` encode ce cas : séquence relue lecture m4 (1ʳᵉ exécution), `reprise`, marqueur m4 (2ᵉ exécution) | C-1 |
| S-3 | même exécution : lecture m3, puis lecture m1 | **admis** (`ws` non monotone) | C-1 |
| S-4 | lecture de 00:00 (J+1), puis marqueur de 23:59 (J) | le marqueur de J est écrit dans `pool-2026-10-05-0.jsonl`, après la `cloture` de J | C-1 |
| S-5 | `fsync` injecté en échec au marqueur m2, l'appelant réessaie | marqueurs écrits : m1, m2, **m2** | C-2 |
| S-6 | écriture partielle (RLIMIT_FSIZE, sous-processus : 40 octets écrits sur 164), l'appelant continue, bascule | ligne illisible au milieu du fichier de J ; `sha256sum -c pool.sha256` : **FAILED** ; la reprise suivante déclare `queue: null` | C-2 |
| S-7 | `canonique` d'une liste qui se contient | **boucle sans fin** (arrêt par `timeout` à 10 s, sortie 124) | C-3 |
| S-8 | `ouvrir` hors grille, puis seconde ouverture dans le même processus | `JOURNAL/fenetre`, puis `JOURNAL/occupe` : verrou non rendu | O-2 |
| S-9 | coupure juste après la création du fichier de J+1 (vide), redémarrage horloge à 23:53 de J, marqueur de 00:00 | `FileExistsError`, exception non nommée (double défaut ; un redémarrage la résout) | O-3 |
| S-10 | ligne avec `"seq": true` à la place de 1 | prise pour intègre (`seq` de la reprise = 2) | I-3, confirmé |
| S-11 | premier enregistrement d'un jour neuf refusé (flottant) | `JOURNAL/type`, mais la bascule a eu lieu (fichier de J+1 et sommes créés) : la docstring « Tout refus … n'écrit rien » est fausse | C-6 |
| S-12 | fenêtre de 23:59 sans marqueur | aucun `point` pour cette heure | O-4 |

Contrôles positifs :
- Fichier de sommes en marche normale (1 500 fenêtres, deux bascules, reprise sur queue) : `sha256sum -c` OK sur les
  deux fichiers clos.
- Les sondes de la relecture interrompue (`sondes_prec.py`, copiées sans changement, `b276c0b9…fa47`) donnent sur mon
  arbre les mêmes constats (S-4 à S-8 ; reprise un jour plus tard ; fichier vide) ; sorties dans ma transcription.

Cas que l'arbre ne teste pas : voir les mutants vivants du §4.
- Sur le reste, la conception tient :
  - une ligne sans saut final n'est jamais prise pour intègre ;
  - les octets invalides et les fins de ligne CRLF donnent une queue ;
  - les fichiers achevés sont sommés à la reprise, une ligne de sommes coupée est close.
- Un recul d'horloge pendant l'exécution, sans redémarrage, rend toute écriture impossible (santé comprise) : item N-3.

## 4. Contrôle (4) : rouge avant, vert après ; mutants

**Rouge puis vert**, sur mes arbres t0 à t7 (rouge : code de t_{k−1} avec les tests de t_k ; réseau isolé par
`unshare -n`). Script `outils/rouge_vert.sh` (`55489933…cb70`) ; sortie `preuves/rouge-vert.txt` (`f1bc597d…83ed7`).

| cas | rouge | vert |
|---|---|---|
| CB-0a (tests sans paquet ni garde) | FAILED (errors=2) : import de `config`, `test_sorties_refusees_et_inscrites` | 6, OK |
| CB-0b runner | `TypeError: verdict() got an unexpected keyword argument 'variable'` ; puis, avec le vérificateur de t2 et le `gates.yml` de t1 : K-02 en échec (26 ok, 1 échec) | 27 ok |
| CB-0b fitness | `import shogen_s2` ajouté : FAIL (frontière et cinq graines) ; échappement invalide écrit par `printf '\134d'` et contrôlé par `od -c` : ERROR (compilation) | 4, OK |
| CB-1a | ImportError (`journal` absent) | 4, OK |
| CB-1b | FAIL `test_seconde_instance_refusee_sans_ecriture` | 5, OK |
| CB-2a | ERROR `test_bascules_cloture_sommes_et_chaine_continue` | 1, OK |
| CB-2b | 9 errors | 9, OK |
| CB-2c | 4 FAIL de `test_trous` et 8 ERROR de `test_reprise` (sommes rattrapées) | 18, OK |

Pour CB-2c, le worker déclare « 5 tests de trous en échec » ; je mesure 4 échecs dans `test_trous`, plus 8 erreurs dans
`test_reprise`. L'écart est sans effet : le rouge est montré.

**Mes mutants.** Lanceur `outils/campagne.py` (`2fe26a22…a3c9`) :
- contrat : sortie 1 = tué, 0 = vivant, toute autre sortie ou mutant inapplicable = FATAL ;
- témoin vert par cible ;
- copie fraîche pour chaque mutant ;
- espace réseau isolé (`unshare -n`, boucle locale allumée par `lo_up.py`, `03d91b36…d696`).

Mutants dans `outils/mutants_g2.py` (`782b7ac8…7699`) ; sortie `preuves/mutants-g2.txt` (`dd5e318f…c44fd`).

**41 mutants : 35 tués**, chacun par le test visé, **6 vivants, 0 FATAL**.
- Tués : `prec` sans saut de ligne ; `seq` initial ; clés non triées ; canonicité et `prec` non contrôlés à la
  relecture ; première ligne de tout type ; clôture et sommes sans `fsync` ; fenêtre du redémarrage admise ; borne du
  recul ; sha256 et position de la queue ; ligne de sommes non close ; relecture sans borne ; sommes non rattrapées ;
  trou avant une lecture ; borne « a » ; type réservé ; borne d'écriture ; fenêtre close admise ; cause non remise ;
  verrou partagé ; `fermer` sans libération ; clé double ; booléen pour un entier ; sha256 des octets réduits ;
  `RecursionError` non capturée ; liste vide ; garde neutralisée ; `ReseauInterdit` sous `Exception` ; `--aucun-saut`
  sans effet ; job s2bis ramené à la suite nue ; job s2bis sans `--aucun-saut` ; job S2 avec `--plancher 1` ; job
  s2bis sans l'étape du runner.
- **Vivants, tous non équivalents** :
  - **M-07** : `fsync` avant le point ; l'espion compte les appels, pas l'ordre.
  - **M-18** : reprise un jour plus tard sur un fichier propre, écrite dans le fichier de la veille.
  - **M-26** : `connect_ex` non gardé, aucun test ne l'appelle.
  - **M-28** : plancher par défaut du point d'entrée à 0. Le cas C-01 tombe exactement au plancher.
  - **M-29** : `--plancher N` lu puis mis à 0. C-04 tombe au plancher.
  - **M-32** : `if: false` sur le job s2bis ; K-02 ne lit pas les `if:`.

**Mutants de la relecture interrompue, rejoués** par mon lanceur. Source : `mutants_prec.py`, copie sans changement
(`50148ac8…ae8a`), adaptée par `mutants_prec_adapte.py`. Sortie `preuves/mutants-prec-rejoues.txt` (`f48d515f…bb6b`).

**32 mutants : 16 tués, 16 vivants**, bilan identique au sien. Les vivants :
- **G-01** : reprise un jour plus tard sans `cloture`.
- **G-02** : fichier clos rouvert.
- **G-03** : grille non contrôlée.
- **G-04** : `ws` d'ouverture hors grille.
- **G-05** : `JOURNAL/illisible` mal nommé ; aucun test ne nomme ce refus, que FORMAT §7.6 promet.
- **G-06** : `fsync` de la reprise retiré.
- **G-07** : type de `seq` non contrôlé en première ligne.
- **G-08** : queues dans l'ordre inverse.
- **G-10**, **G-11** : bornes d'écriture et de lecture décalées d'un octet.
- **G-13** : champ `prec` admis en silence.
- **G-19** : descripteur de la seconde instance non fermé.
- **G-20** : borne des entiers de configuration.
- **G-26** : plancher s2bis abaissé à 1 (relève de Q-2).
- **G-27** : identique à M-32.
- **G-29** : identique à M-28.

**Bilan.** Aucun vivant n'est équivalent. 19 vivants distincts sont à tuer (C-4, C-5) ; G-26 relève de Q-2. Règle de
METHODE-PARTIES §2 : « une mutation qui survit = test à renforcer, jamais à retirer ».

**Mutants obligatoires du §2.4.** Le jeu du worker les contient tous, tués par leur test nommé (ses `journal/final-*` ;
totaux 19 + 20 + 19 + 4 + 11 + 15 + 14 = 102). Son « doublon admis » (`suivante = ws + w`) ne couvre pas le doublon
réel de S-1 et S-2.

## 5. Contrôle (5) : la CI

**Job `s2bis-unittest`.**
- Image `ubuntu-24.04` ; checkout épinglé `3d3c42e5…` (v7.0.1), `persist-credentials: false` ; `timeout-minutes: 10`.
- Pas de `setup-python` (R-8).
- Étapes : le runner du vérificateur, puis `python3 -B enforcement/verdict-suite-s2.py s2bis --aucun-saut --plancher 34`.
- Aucune `continue-on-error`. Commentaire d'en-tête mis à jour.

**Vérificateur paramétré : comportement par défaut inchangé.**
- Sans option, `main` garde `PLANCHER` = 405 et `VARIABLE`.
- Suite S2 rejouée en réseau isolé (`python3.12`) : `Ran 405 tests`, `OK (skipped=2)`, sortie 0. Message « conforme
  (code 0, résumé final, sauts nommant SHOGEN_S2_CAMPAGNE_CONTROL, Ran ≥ 405) » : texte identique à l'ancien.
- Runner : 27 cas sur 27, sous 3.11 et 3.12.
- Analyse des arguments plus stricte : argument en trop ou commençant par « - » donne 3 ; option répétée ou plancher
  illisible aussi.
- Aucun autre appelant ne passe d'argument au vérificateur (recherche au §12, écart E-R1).

**Gates.** Aucune n'est affaiblie dans son comportement. Mais **une protection par test a reculé** :
- avant le lot, `main` appelait `verdict(err, code)`, et le plancher par défaut était celui de `verdict`, tenu par V-03 ;
- maintenant `main` porte son propre défaut, qu'aucun cas n'exerce (M-28 vivant) ;
- de même, l'option `--plancher` mise à 0 survit (M-29) ;
- K-01 et K-02 refusent `continue-on-error` et `-m unittest`, mais pas `if:` (M-32 vivant).

C-4 referme ces trois points. K-01 tue le retour à la suite nue (G-25) et un plancher abaissé par option sur le job S2
(M-41).

## 6. Contrôle (6) : choix E-7 et questions Q-1 à Q-8

**E-7 (a) Vérificateur paramétré plutôt que neuf : d'accord.**
- La PROPOSITION (l.139) laisse le choix ; le paramétrage réutilise les motifs déjà éprouvés (`FIN`, `SAUT`).
- Condition : C-4 (cas du point d'entrée).

**(b) Plancher dans `gates.yml`, relevé à chaque diff : d'accord.**
- La constante `PLANCHER` de S2 reste intacte.
- Égalité avec le compte non mécanisée : voir Q-2.

**(c) Avertissements en erreur à la compilation seulement : conforme à la lettre de Q-G-05.**
- Voir Q-3 pour la recommandation de serrer.

**(d) Configuration : d'accord.**
- Flottants refusés (valeurs exactes en chaîne, cohérent avec τ et σ en `Decimal` côté RB-0).
- Entiers de plus de 30 caractères refusés : borne large et nommée.
- Listes vides refusées : une liste scellée vide est presque toujours une erreur ; un schéma pourra l'admettre
  explicitement plus tard.

**(e) Format : d'accord sur le fond, avec trois compléments.**
- D'accord sur :
  - aucun flottant ; UTF-8 sans échappement ;
  - `prec` qui hache la ligne saut compris, recalculable ligne à ligne par `sha256sum` ;
  - les noms des fichiers ;
  - la borne de 4 Mio ;
  - `JOURNAL/illisible` sans seconde chaîne, échec fermé.
- Point qui ne porte que `ws`, sa tête étant son `prec` : acceptable au regard d'E-C-19. Mais l'heure dont la dernière
  fenêtre manque n'a pas de point (O-4).
- Compléments :
  1. la règle « `ws` non décroissant » (C-1) ;
  2. l'arrêt après erreur d'entrée-sortie (C-2) ;
  3. la borne de 4 Mio exige que CB-3 borne le corps des réponses sous LIMITE, base64 compris (N-4).
- « Trou au marqueur suivant » : la reprise porte le début (`suivante`) et le marqueur suivant fixe la fin. Acceptable,
  à consigner comme lecture d'E-C-22 (O-8).

**(f) Garde : d'accord.**
- `BaseException` : un attrape-tout du code testé ne la masque pas.
- Boucle locale permise.
- Compléments : `connect_ex` à tester (C-5) ; `sendmsg` non gardé (O-7) ; campagnes de mutants en `unshare -n`
  (O-6 : l'E-6 du worker a envoyé une vraie requête DNS au résolveur de l'hôte).

**Q-1 (découpage en sept diffs, un commit par diff) : oui.**
- METHODE-PARTIES §3 : une partie qui dépasse le plafond part en PR consécutives.
- L'adjudication 5 du G0 (≤ 200 lignes par sous-lot) est tenue en lisant « sous-lot » comme « diff ». Numérotation à
  porter à l'annexe A, une ligne par diff.
- Chaque état intermédiaire est vert (§1).
- Les corrections C-1 à C-6 forment un diff de plus après CB-2c (≤ 200 lignes de code).

**Q-2 (mécaniser plancher = compte) : recommandé, non exigé.**
- Le G0 ne l'impose pas. Mais un plancher abaissé survit aujourd'hui (G-26).
- Forme la moins coûteuse : une option `--egal` du vérificateur (Ran = plancher) pour le seul job s2bis. Cela tue G-26
  et met en œuvre mécaniquement SHOGEN-CI-PLANCHER-SUIVI-1.
- Le conflit sur la ligne `--plancher` est d'une ligne par lot, sous un seul orchestrateur.
- Le motif « sans égalité figée » de S2 (couplage avec le test de comptes de B-SEG-1) ne vaut pas pour s2bis.
- Décision de l'orchestrateur (serrer).

**Q-3 (`PYTHONWARNINGS=error` sur toute la suite) : oui, à coût nul aujourd'hui.**
- La suite passe sous `-X dev -W error` avec 3.10, 3.11, 3.12 et 3.13 : 34 tests, 0 avertissement.
- Le collecteur tourne des mois : un descripteur oublié ou une dépréciation y comptent.
- Mise en œuvre : `PYTHONDEVMODE=1` et `PYTHONWARNINGS=error` dans l'environnement de l'étape. Le vérificateur transmet
  l'environnement à la suite.

**Q-4 (fenêtre du redémarrage) : la garder refusée, et sceller ce choix.**
- Coût : une fenêtre par redémarrage, déclarée `arret`.
- Une fenêtre en cours au redémarrage a un état incertain (lignes de l'exécution précédente, cf. C-1).
- L'admettre « si elle n'a encore aucune ligne » ne serait sûr qu'avec la règle de C-1 et le critère D-2.

**Q-5 (sceller E-7 (e) tel quel) : oui, après C-1, C-2 et C-6.**
- Ajouter au format : la règle de monotonie, l'arrêt sur erreur, la règle du point horaire (O-4) et la borne de corps
  (N-4).
- Le scellement se fait au gel, avec le test de conformité de CB-18.

**Q-6 (SHOGEN-CI-S2-CABLAGE-1) : fermable par ce lot, après C-4 (c).**
- Le déclencheur « prochain lot qui touche `gates.yml` » est atteint.
- K-01 est le cas de la forme de H-20 qu'attend l'item, et il tue le retour à la suite nue.
- Il reste à refuser `if:`. La fermeture est un acte de l'orchestrateur.

**Q-7 (SHOGEN-ENTRELACEMENT-D5-1) : oui pour S2-bis, mécanisme en place et testé.**
- Mécanisme : verrou, plus la chaîne qui rend visible tout entrelacement.
- À prononcer après C-2 : l'arrêt sur erreur touche l'intégrité de la chaîne.
- Réserve à écrire au G0 de DB-4 : ne jamais supprimer ni recréer `<préfixe>.verrou`, sinon le verrou est contourné
  (N-5).
- La qualification sur S2 (lot à `f35a70c`) reste à re-dater, selon l'AVIS Q-C-11.

**Q-8 (rejouer `xtask` sur le dépôt réel) : oui, par l'orchestrateur ; je ne le peux pas (dossiers interdits).**
- Sur ma copie, la seule violation S-G9 est la même avec et sans les diffs : le lot n'en ajoute aucune.

## 7. Contrôle (7) : R-13, R-8, R-25, `xtask`

**R-13.**
- Motif exact du job g5 (`git grep` sur un index jetable de l'arbre en série) : sortie 1, 0 ligne.
- Recherche large (todo, fixme, xxx, hack ; insensible à la casse) sur les fichiers du lot : rien.

**R-8.**
- Mon balayage `ast` des 14 fichiers Python du lot ne trouve que la bibliothèque standard : `ast`, `contextlib`,
  `fcntl`, `hashlib`, `importlib`, `io`, `ipaddress`, `json`, `os`, `re`, `shutil`, `socket`, `subprocess`, `sys`,
  `tempfile`, `threading`, `time`, `unittest`, `warnings`, plus le paquet et `tests`.
- `fcntl` restreint le paquet à POSIX : à écrire dans la pièce G6 (C-6).
- PyYAML, utilisé en local par le worker (E-8) : aucun ajout au dépôt, rien à objecter.

**R-25** : tenu (§1).

**`cargo --locked xtask verify`.**
- Copies : la série et la base, même tête `86c07ff`, exclusions du brief.
- `TMPDIR` et `CARGO_TARGET_DIR` dédiés ; sorties redirigées ; seules les lignes de verdict ont été lues ; aucun accès
  réseau de `cargo`, vérifié sur les journaux.
- Résultats :

| gate | série | base |
|---|---|---|
| S-G1 à S-G8 (dont S-G5, corrigée par `86c07ff`) | VERT (0) | VERT (0) |
| S-G9 | ROUGE, 1 violation | ROUGE, 1 violation |
| `cargo fmt --check`, `no_std`, `clippy -D warnings` | VERT | VERT |

- La violation S-G9 est `docs/17-modele-de-menace.md:70` dans les deux cas : un renvoi vers un dossier exclu, connu du
  brief.
- Verdict global ROUGE par S-G9 seule. Les sections S-G9 ne diffèrent que par les journaux de compilation de `cargo`.

## 8. Contrôle (8) : items I-1 à I-7 et items neufs

**Items du worker.**
- **I-1** (aucun `fsync` du dossier) : d'accord.
  - Concerne la création d'un fichier journal et du fichier de sommes.
  - Déclencheur proposé : avant le gel du collecteur, au plus tard CB-18.
  - Coût : trois lignes ; peut entrer dans le diff de corrections.
- **I-2** (aucune SAST) : d'accord. Étendre SHOGEN-SAST-PYTHON-RECALCUL-1 à `s2bis/` plutôt que former un item neuf :
  même décision d'outil (R-8). Déclencheur : avant le gel du collecteur, code scellé qui tourne des mois.
- **I-3** (lien entre fichiers ; `seq` comparé par valeur) : confirmé par S-10.
  - À écrire aux G0 de RB-1 et RB-18 : entier strict, non booléen ; première ligne chaînée à la dernière intègre du
    fichier précédent, ou `reprise` qui déclare la queue.
  - L'écrivain peut aussi exiger `type(seq) is int` à toute ligne (facultatif).
- **I-4** (`_socket`) : d'accord. Élargir à `sendmsg` (O-7) et aux sous-processus qui n'importent pas `tests`.
- **I-5** (`JOURNAL/illisible` arrête l'observateur jusqu'à N3) : d'accord.
  - Ajouter le cas de la mise en service : premier démarrage coupé entre la création du fichier et sa première ligne,
    fichier vide unique (sonde de la relecture interrompue, rejouée : `JOURNAL/illisible`).
  - À écrire au DB-6 et aux exercices A-7.
- **I-6** (écrivain non partagé entre fils) : d'accord. Recommandation : une garde mécanique (fil propriétaire noté à
  `ouvrir`, refus nommé sinon) plutôt qu'une consigne écrite seule (N-6). Déclencheur : CB-4.
- **I-7** (réestimer P1) : d'accord, et à dire au calendrier.
  - Mesuré : 998 lignes de code pour CB-0 à CB-2, contre environ 560 estimées (190 + 180 + 190), soit ×1,78 [calc].
  - Avec les corrections, environ ×2 ; P1 (≈ 1 620 estimées) se rapprocherait de 2 900 à 3 200 lignes [calc, inféré].
  - À porter à l'information de l'investisseur (Q-G-04, A-1).

**Items neufs proposés à l'orchestrateur (PAROXYSME).**
- **N-1** : l'enregistreur `s2-harness/tools/oracle_record.py` ne couvre pas `s2bis` : liste fermée de commandes, et un
  commit est exigé. SHOGEN-G2-ENREG-ROLE-1 ne se tient donc pas mécaniquement pour S2-bis. Déclencheur : avant la G2
  complète de P1.
- **N-2** : la checklist G2 du corpus est absente en session cloud. SHOGEN-G2-CHECKLIST-CORPUS-1 reste ouvert ; rappel,
  pas d'item neuf.
- **N-3** : un recul d'horloge pendant l'exécution, sans redémarrage, fait refuser tout enregistrement (fenêtre
  inférieure à `suivante`), santé comprise : rien ne le journalise. Déclencheur : G0 de CB-4 et CB-11.
- **N-4** : corps des réponses à borner sous LIMITE, base64 compris (E-C-17), faute de quoi `JOURNAL/taille` fait perdre
  la lecture. Déclencheur : G0 de CB-3.
- **N-5** : la rétention (DB-4) ne doit jamais :
  - supprimer ou recréer `<préfixe>.verrou` ;
  - réécrire `<préfixe>.sha256` ;
  - supprimer le fichier du jour.
  Elle doit aussi tolérer une dernière ligne de sommes incomplète, et traiter « clos » comme « inscrit aux sommes » (un
  fichier à queue n'a pas de `cloture`). Déclencheur : G0 de DB-4.
- **N-6** : garde mécanique d'un seul fil (voir I-6). Déclencheur : CB-4.

## 9. Liste fermée des corrections (C-1 à C-6)

**Conditions communes :**
- un diff de plus après CB-2c, d'au plus 200 lignes de code ;
- tests d'abord, rouge montré ;
- plancher relevé ;
- FORMAT et METRIQUES mis à jour ;
- mes deux jeux de mutants (`reprise/outils/mutants_g2.py`, `mutants_prec.py`) rejoués : chaque mutant cité ci-dessous
  tué, les autres toujours tués ;
- revue par l'orchestrateur, ou G2 ciblée sur ce diff.

**C-1 : `window_start` non décroissant (E-C-22, E-C-20 ; FORMAT §3.2, §6.1 et §7.5).**
- (a) Refuser nommément (`JOURNAL/fenetre`) tout enregistrement de fenêtre (`ecrire`, `marqueur`) dont `ws` est
  inférieur à la dernière fenêtre écrite.
- (b) À la reprise, restaurer cette dernière fenêtre depuis le journal (types autres que `ouverture`, `point`,
  `cloture`, `reprise` et `trou`) et poser `suivante = max(attendu, dernière + w, ws + w)`.
- (c) Tests :
  - S-1 et S-2 refusés, octets du journal inchangés ;
  - S-4 refusé, aucun enregistrement de J dans le fichier de J+1 ;
  - S-3 refusé ;
  - réécrire la prémisse de `test_cause_remise_a_saut_par_un_marqueur_sans_trou`, qui ferme aujourd'hui en seconde
    exécution une fenêtre ouverte par la première.
- (d) Mutants tués : « dernière fenêtre non restaurée à la reprise » ; « contrôle de monotonie retiré ».

**C-2 : arrêt après erreur d'entrée-sortie (E-C-19, E-C-20, E-C-21 ; FORMAT §4).**
- Règle : toute `OSError` levée par une écriture, un `fsync` ou une fermeture de l'écrivain le laisse inutilisable.
  - Concerne `ecrire`, `marqueur`, la bascule, les sommes, la reprise.
  - Tout appel ultérieur lève un refus nommé (par exemple `JOURNAL/casse`), sans rien écrire.
  - `fermer` libère toujours le verrou.
  - L'instance suivante déclare la queue déchirée par `reprise`.
- Tests :
  - S-5 : le marqueur réessayé est refusé, aucun doublon ;
  - S-6 : écriture partielle injectée (fonction d'écriture injectable, ou RLIMIT_FSIZE en sous-processus) ; écritures
    suivantes refusées ; à la réouverture, `reprise.queue` déclare la queue ; toute ligne de sommes égale au sha256 des
    octets de son fichier.

**C-3 : `canonique` sur une structure cyclique.**
- Refus nommé `JOURNAL/type` en temps borné.
- Les sous-structures partagées non cycliques restent admises.
- Test sous délai (fil avec `join`, ou sous-processus).

**C-4 : runner du vérificateur.**
- (a) Cas « point d'entrée sans option, PLANCHER − 1 tests sans saut : sortie 1 » ; tue M-28 et G-29.
- (b) Cas « `--aucun-saut --plancher 4`, trois tests : sortie 1 » ; tue M-29.
- (c) K-01 et K-02 refusent toute ligne `if:` dans le job ; tue M-32 et G-27.

**C-5 : tuer les mutants vivants non équivalents**, par des tests à valeurs attendues écrites à la main.

| mutant(s) | test à écrire |
|---|---|
| G-01, M-18 | reprise un jour plus tard sur un fichier propre : `cloture` à la veille, `reprise` dans le fichier du jour |
| G-02 | dernier enregistrement = `cloture` : fichier clos intact, fichier neuf |
| G-03 | w qui ne divise pas 3 600 : `JOURNAL/grille` |
| G-04 | `ouvrir` hors grille : `JOURNAL/fenetre` |
| G-05 | journal sans enregistrement intègre : `JOURNAL/illisible` |
| G-06 | `fsync` après la `reprise` |
| G-07 | première ligne à `seq` non entier : queue |
| G-08 | deux queues déclarées dans l'ordre |
| G-10, G-11 | ligne d'exactement LIMITE octets écrite et relue ; LIMITE + 1 refusée à l'écriture, prise pour queue à la lecture |
| G-13 | champ `prec` refusé |
| G-19 | la seconde instance ferme son descripteur |
| G-20 | entier de 30 caractères admis, 31 refusé |
| M-07 | l'espion relève la taille du fichier au `fsync` : égale à la taille après le point |
| M-26 | `connect_ex` vers 192.0.2.1 : `ReseauInterdit` |

**C-6 : documents.**
- (a) Docstring de `journal.py` l.6-7, « Tout refus est nommé (ErreurJournal) et n'écrit rien » : fausse aujourd'hui
  (S-11 ; trou écrit avant un marqueur refusé). Rendre le code conforme (contrôler l'enregistrement avant toute bascule
  ou tout trou), ou corriger le texte.
- (b) FORMAT §3.2 : « tout type sauf `ouverture` et `point` » englobe `reprise` (son `ws` peut être inférieur à
  `suivante`) et `cloture` et `trou` (sans `ws`). Écrire « enregistrements écrits par `ecrire` et `marqueur` » et ajouter
  la règle de C-1 ; l'affirmation du §7.5 devient alors vraie.
- (c) FORMAT §4 : la règle de C-2.
- (d) METRIQUES : résultats des campagnes du réviseur après corrections.
- (e) Pièce G6 : plate-forme POSIX (`fcntl`).

## 10. Observations (non bloquantes)

- **O-1** : `SHA256SUMS` du worker : chemins de deux origines (§1). Pièce de transport non versée.
- **O-2** : verrou gardé après un refus d'`ouvrir` (`JOURNAL/fenetre`, `JOURNAL/illisible`) jusqu'à `fermer()` ou la
  sortie du processus (S-8). Recommandation : `fermer()` dans ces chemins.
- **O-3** : bascule vers un segment 0 qui existe déjà : `FileExistsError` (S-9, double défaut, résolu par un
  redémarrage). Recommandation : numéroter le segment du jour neuf comme le fait la reprise.
- **O-4** : aucun `point` pour une heure dont la dernière fenêtre n'a pas de marqueur (S-12). À trancher à CB-15
  (cadence d'export des têtes, E-C-35).
- **O-5** : `ecrire(…, type=…)` : le champ `type` est écrasé en silence. Recommandation : le refuser comme `seq` et
  `prec`.
- **O-6** : les campagnes de mutants qui retirent la garde se lancent en `unshare -n`. L'E-6 du worker a envoyé une
  requête DNS réelle au résolveur de l'hôte.
- **O-7** : `socket.sendmsg` n'est pas gardé.
- **O-8** : E-C-22 dit « trou à la reprise ». Le lot l'écrit au marqueur suivant, le début étant porté par la reprise.
  Lecture à consigner à l'adjudication.
- **O-9** : la fitness « mêmes octets » ne porte que sur `config`. Les octets du journal sont fixés par le test écrit à
  la main, sous une seule graine.
- **O-10** : la frontière syntaxique ne voit ni `exec`, ni `eval`, ni `getattr(builtins, …)`. Limite à écrire à la pièce
  G6 ou à METRIQUES.
- **O-11** : `prefixe` n'est pas validé (séparateur de chemin possible). Recommandation : un motif fermé.
- **O-12** : le premier commit (CB-0a) porte six tests sans job CI ; le job arrive avec CB-0b. Sans effet tant que la
  forge ne démarre pas les jobs (GC-01).

## 11. Checklist G2 du corpus et enregistrement de rôle

- **Checklist du corpus** (`templates/checklist-revue-G2.md`) : **[abs]**, non disponible en session cloud
  (PASSATION-CLOUD l.151). J'ai appliqué les huit contrôles du brief et les points de G2 de doc 02 que reporte la
  PASSATION (l.123-125) :
  - revue à 100 % : les 18 fichiers à l'état final lus en entier, ainsi que les diffs des 3 fichiers modifiés ;
  - réviseur distinct du générateur ;
  - niveaux de preuve.
  SHOGEN-G2-CHECKLIST-CORPUS-1 reste ouvert (N-2).
- **Enregistrement de rôle** au schéma `shogen.oracle-record.v1`, produit par mes propres commandes (N-1 : l'outil du
  dépôt ne s'applique pas) :
  - fichier : `reprise/oracle/shogen-86c07ff-G2-20261004T210156Z-27898.json`, sha256 `6105955a…192f` ;
  - contenu : rôle G2, auteur `claude-opus-5-5`, `static_only` false, `served_from` null ;
  - arbre : `tree.commit` = `86c07ff`, extraction décrite (`git archive` puis les sept diffs), 694 fichiers hachés ;
  - exécutions : suite s2bis par le vérificateur, runner, suite S2 par le vérificateur, toutes en sortie 0 ;
  - `exit` 0 ; variable scellée non posée.
  - Enregistreur : `outils/enregistrement_role.py` (`96a64740…310b`).

## 12. Journal de provenance (G1 du réviseur)

### 12.1 Lectures

- **[lu]**, contrat et règles :
  - le brief ; le rapport du worker (entier) ; le brief du worker ;
  - le G0 (entier) ; l'AVIS (entier) ;
  - la PROPOSITION l.1-379 et l.780-926, les l.380-779 (RECALC, DEPLOI) n'étant lues que par des recherches de
    mots-clés de la tranche ;
  - ADR-0029 : titres ; l.100-117 ; l.214-253 ; l.375-434, dont l'ajout daté de la l.395 ;
  - annexe D d'ADR-0028 l.32-48 (liste D.2, aucune pièce ouverte) ;
  - annexe B d'ADR-0028 : l.42, 45, 55, 79, 80, 685, 760, 764, 798, 892, 893, 894, 896 et 916 (1 500 premiers caractères
    de chacune) ;
  - ADR-0028 l.195-215, D6 (viii) ;
  - `docs/METHODE-PARTIES.md` (entier) ;
  - `docs/PASSATION-CLOUD.md` l.120-146 et des lignes trouvées par recherche ;
  - `docs/G2-lot-DETTES-SIM.md` l.1-60 (forme) ;
  - `s2-harness/tools/oracle_record.py` : l.1-72, l.117-175 et des lignes trouvées par recherche.
- **[lu]**, le lot : les 18 fichiers à l'état final, en entier ; les diffs de `gates.yml`, du vérificateur et du runner
  contre la base ; la tête de `gates.yml` en entier.
- **[abs]** : la checklist G2 du corpus.
- **Jamais ouverts** :
  - `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/` (voir E-R2), `docs/15-*`, `docs/16-*`,
    `docs/pocket-report/` ;
  - aucun `*.jsonl` réel, aucune pièce de D.2.
- `SHOGEN_S2_CAMPAGNE_CONTROL` n'a jamais été posée. Mes scripts la retirent (`unset` ou filtre d'environnement), et le
  vérificateur aussi.

### 12.2 Commandes et sorties

Les sorties sont sous `reprise/preuves/`.

| contrôle | commande | sortie |
|---|---|---|
| base | `git rev-parse HEAD` ; `git rev-list --count 34a17d8..HEAD` | `86c07ff…` ; 7 commits, documents seulement |
| (1) | `git archive` puis `git apply --check` et `git apply` ×7 ; `sha256sum -c` ; `diff -rq` ; `git apply --numstat` | §1 |
| état par étape | vérificateur (plancher de l'étape) et runner, t1 à t7 | §1 |
| suite s2bis | `unshare -n … pythonX -B enforcement/verdict-suite-s2.py s2bis --aucun-saut --plancher 34` | conforme, 34 tests, 3.10 à 3.13 (`verdict-s2bis-python3.1*.txt`) |
| suite s2bis sous `-X dev -W error` | 3.10 à 3.13 | 34 tests, OK, 0 avertissement |
| suite S2 | `unshare -n … python3.12 -B enforcement/verdict-suite-s2.py` | 405 tests, OK (skipped=2), conforme ; 20:49:16 à 20:50:03 UTC (`verdict-s2-defaut.txt`, `13d4d328…24de1b`) |
| runner | `python3.1x -B enforcement/tests/run-fixtures-verdict-suite-s2.py` | 27 ok, 0 échec (`runner-python3.12.txt`, `9deaacf1…494e`) |
| hook | `bash enforcement/tests/run-fixtures-hooks.sh` | 54 ok, 0 échec, en 5 s (`hooks-complet.txt`) |
| secrets | `bash enforcement/gate-secrets.sh --tree`, sur un index jetable | OK, 685 fichiers (`secrets-tree.txt`) |
| R-13 | motif exact du job g5, sur l'index jetable | sortie 1, 0 ligne |
| xtask | `outils/xtask.sh`, détaché ; fin constatée par sondage | §7 (`xtask-serie.txt` `33eecb2e…`, `xtask-base.txt` `d4b9e5fc…`) |
| sondes | `outils/sondes_g2.py` ; `sondes_prec.py` | §3 |
| rouge et vert | `outils/rouge_vert.sh` | §4 |
| mutants | `outils/campagne.py` sur `mutants_g2.py` et `mutants_prec_adapte.py` | §4 |
| rôle | `outils/enregistrement_role.py` | §11 |

### 12.3 Chiffres recomptés

- Fichiers : 679 et 694.
- Lignes ajoutées par diff : `git apply --numstat`.
- Tests par étape : `TestLoader().discover`.
- Planchers.
- Lignes par fichier : `wc -l`.
- Tests par module : décompte des `def test_`.
- Empreintes de référence (`SHA_VALIDE`, H1, H2, H3, TETE) : `printf` puis `sha256sum`.
- Comptes des campagnes.
- Rapport ×1,78 [calc] : 998 / 560.

Aucun chiffre de seconde main. Les chiffres du worker qui ne sont pas rejoués sont attribués (ses 102 mutants : lus dans
ses fichiers `journal/final-*`).

### 12.4 Pièces de la relecture interrompue

- **Utilisées**, après lecture et empreinte :
  - ses sondes (`sondes_prec.py`), rejouées sur mon arbre ;
  - ses 32 mutants (`mutants_prec.py`), rejoués par mon lanceur ;
  - son utilitaire `lo_up.py`, lu (huit lignes d'`ioctl`) et copié.
- **Refaits sur la tête actuelle**, sans m'y fier : ses rouge et vert, ses verdicts, ses lancements de `xtask`, ses
  contrôles du hook et des secrets.

### 12.5 Écarts du réviseur

- **E-R1** : pour trouver les appelants du vérificateur, j'ai lancé `git grep -n 'verdict-suite-s2'` sur tout le dépôt.
  - Exclusions : les six dossiers interdits et `*.jsonl`. La recherche a donc parcouru `docs/`, contre la consigne
    « aucune recherche récursive sur tout `docs/` ».
  - Sortie : lignes coupées à 200 caractères, dont `JOURNAL.md:374` et des lignes de `docs/adr-0028/` (ADR, annexe A,
    CP2, DOSSIER-G7) et de la PROPOSITION.
  - Aucune pièce de D.2, aucun dossier interdit.
- **E-R2** : `grep -rl 'oracle-record' --include=*.md docs/adr-0028 …` a parcouru récursivement `docs/adr-0028`, donc la
  liste du dossier interdit `monark-m009a`.
  - Ce dossier compte 6 fichiers suivis, dont 0 `.md` (comptes seuls, par `git ls-files` et `find`) : `grep` n'y a lu
    aucun fichier.
  - Sortie : noms de fichiers seulement, aucun de ce dossier.

### 12.6 Exposition, à l'usage du contrôle FM-1.1

- Le chemin du scratchpad contient le motif de session de la liste FM-1.1 (retouche de versement).
- Les noms des dossiers interdits figurent dans mes exclusions.
- La lecture de la liste D.2 (annexe D l.32-48) porte dans ma transcription les noms des pièces et les motifs FM-1.1 de
  D.2 n° 10 et n° 12. L'identifiant de session de D.2 n° 11 figure aussi dans mon contexte, par la ligne d'attribution du
  harnais.
- Les noms `control.jsonl`, `journal.jsonl` et `raw.jsonl` apparaissent par la lecture de `gates.yml` et des
  docstrings du vérificateur.
- Journaux `*.jsonl` **synthétiques**, fabriqués par l'écrivain sous test dans mon `TMPDIR` (fixtures, D.4-bis) ;
  aucun réel.
- Aucune opération réseau :
  - suites, mutants et sondes en `unshare -n` (seule l'interface `lo` existe) ;
  - runner, hook et secrets : processus locaux ;
  - `cargo` sans téléchargement (vérifié sur ses journaux).

Fin de rédaction : 2026-10-04 21:12:26 UTC (`date -u`).
