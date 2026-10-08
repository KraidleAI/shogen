# Procédure de l'exécution unique de S2 (partie 4, étape P5 ; 2026-10-02)

Rattachement : ADR-0028 D2, annexe D.4 b-c ; paquet scellé `docs/adr-0028/PAQUET-PREREG-S2.md` (sha256 `494d770d…`), §9 ;
`docs/adr-0028/PLAN-PARTIE-4.md` (étape E) ; items SHOGEN-RENDU-PYCACHE-1, -RENDU-ECHEC-DIAG-1, -RENDU-COUT-1,
-RAW-MEMOIRE-1, -ENREG-VARIABLE-1, -CP2-RUNS-RENDU-1, -CI-S2-SAUT-1, -RENDU-CLI-REPORT-1 (annexe B). Hôte : la session
cloud (P1, JOURNAL du 2026-10-02 21:2x UTC). Toute heure écrite est lue par `date -u` juste avant.

## 0. Ouverture (acte de l'investisseur)

1. Après l'échéance **2026-10-03T17:44:30Z** (genTime du jeton + 24 h), l'investisseur écrit son go ; l'orchestrateur
   le recopie verbatim au JOURNAL, avec l'heure. Sans go, rien ne commence. Un veto avant ce point invalide le sceau
   (A-8 : nouveau paquet, nouveau sha, nouvelle ancre).
2. L'horloge seule n'ouvre rien : la garde (6) exige le jeton vérifié (voie a), la garde (5) l'échéance.

## 1. Préparation de l'hôte (aucune lecture de données)

- Branche `partie-4-execution` ; arbre propre (`git status --short` vide hors fichiers ignorés connus) ; tête notée
  `HEAD` ; `git diff --quiet 41f087ef3e0a621ddb04fa4f2af8733e5fd5a0f9 HEAD -- s2-harness/shogen_s2 s2-harness/tools`
  doit sortir 0 (garde (2)).
- SHOGEN-RENDU-PYCACHE-1 : `find s2-harness/shogen_s2 s2-harness/tools -name __pycache__` doit être vide (sinon :
  suppression, puis contrôle à nouveau) ; toutes les commandes Python sous `PYTHONDONTWRITEBYTECODE=1` et `-B` ;
  `SHOGEN_S2_CAMPAGNE_CONTROL` absente (`env -u`).
- `bash scripts/sceau/verify.sh` : sortie 0.
- *Ajout daté du 2026-10-02 21:5x UTC (constat H-1 de R-C, annexe B.41)* : le dossier parent de `--sortie`,
  `docs/adr-0028/execution/`, doit exister (il est suivi par son `README.md`) ; `--sortie` s'écrit sans barre finale
  (constat C-1 de R-C : avec une barre finale, les débris d'une tentative interrompue ne sont pas vus).

## 2. Journaux scellés (après le go seulement)

- Dossier de travail **hors du dépôt** : `$J` = `<scratchpad>/execution/journaux/` ; fichier de sommes `$S` =
  `<scratchpad>/sceau/SHA256SUMS-cloture-2026-09-28.txt` (sha256 `70910984076474987239d8c7a9da786acc95c38b375ad572d78afa297bf8caf4`,
  re-téléchargé depuis Drive s'il manque, id `1bA3bmuUZn0XCljRH7GIE54RjMsRI5q9Q`).
- Téléchargement des trois fichiers du dossier Drive `1TwP2Jtc0-_gAYjDOHHpvfh3XxnR6jtR6` (ids notés au JOURNAL du
  2026-10-02 21:2x UTC) par `curl -L 'https://drive.usercontent.google.com/download?id=<id>&export=download&confirm=t'`,
  dans `$J`, sous leurs noms exacts. **Aucun affichage de contenu** : ni `cat`, ni `head`, ni lecture par un outil.
- SHOGEN-RAW-MEMOIRE-1, SHOGEN-RENDU-COUT-1 : tailles lues (attendues : 41 676 139, 148 930 880, 204 107 558 o) ;
  mémoire libre lue (`free -g`) ; aucune mesure de durée avant l'exécution.
- `sha256sum` des trois fichiers : égaux aux lignes `journal …` du bloc machine et à celles de `$S` ; consigné au
  JOURNAL (sha seulement). Un écart : arrêt, ligne de JOURNAL, question à l'investisseur.
- *Ajout daté du 2026-10-02 21:5x UTC (constat B-1 de R-C)* : si `raw.jsonl` porte une ligne corrompue autre que la
  dernière, le verdict du run `raw` cite le chemin absolu de `$J` : ses octets et son sha256 dépendent alors de ce
  chemin. Le chemin exact de `$J` est écrit au JOURNAL avant l'exécution, pour qu'un tiers rejoue à l'octet.

## 3. Gardes seules, puis production

- `python3 -B s2-harness/tools/rendu_unique.py --depot . --paquet docs/adr-0028/PAQUET-PREREG-S2.md --journaux $J
  --sommes $S --sortie docs/adr-0028/execution/rendu-<date> --auteur claude-opus-5-5 --gardes-seules` : attendu
  « gardes levées », sortie 0. Un refus n'est pas une exécution : ligne de JOURNAL (heure, gardes refusées, motif),
  correction de la cause hors code gardé, puis nouvelle tentative.
- Même commande **sans** `--gardes-seules`, lancée en tâche de fond (délai par commande : 3 600 s, `DELAI_DEFAUT`).
  La sortie standard ne porte que des chemins et des sha256 ; aucun contenu n'est lu à ce stade.
- Échec (SHOGEN-RENDU-ECHEC-DIAG-1) : rien ne reste ; seuls l'heure, le run en échec et son code sortent sur stderr ;
  ligne de JOURNAL ; ce n'est pas une seconde exécution. Débris `.rendu-<date>.*` : consignés, puis retirés à la main
  avant toute nouvelle tentative.

## 4. Contrôles d'après production (avant toute lecture des rendus)

- Sha256 de chaque sortie et de l'enregistrement, tels qu'imprimés : au JOURNAL (= consignation de l'exécution, D.4 b).
- `python3 -B s2-harness/tools/oracle_record.py --verifier <enregistrement> --role rendu --commit <HEAD> --depot .` :
  « conforme » (SHOGEN-CP2-RUNS-RENDU-1 : runs `suite`, `j14-principal`, `j14-second`, `j28`, `recalcul-tiers`,
  `raw`, dans cet ordre, sortie 0 chacun).
- SHOGEN-CI-S2-SAUT-1 : la sortie du run `suite` doit finir par `Ran 383 tests` et `OK (skipped=2)` (les deux tests
  nommés de D.4 a sautés, variable absente) ; tout autre compte : constat au JOURNAL, examiné avant toute lecture des
  rendus. SHOGEN-ENREG-VARIABLE-1 : `tests_avec_variable` vide dans l'enregistrement.

## 5. Lecture et suite

- Les rendus se lisent dans `docs/adr-0028/execution/rendu-<date>/` ; ils sont versés au dépôt tels quels (les
  journaux, jamais).
- SHOGEN-RENDU-CLI-REPORT-1 : aucun rendu des journaux hors de `rendu_unique.py` (ni `python -m shogen_s2.report`, ni
  lecture directe des journaux) ; contrôle FM-1.1 de la transcription de l'exécution par l'orchestrateur, consigné.
- Le verdict est celui de la règle scellée (paquet §10.2) tel que rendu ; toute question non prévue est une déviation
  déclarée, jamais une réécriture (pt 11). Rapport `docs/11` : étape R du plan.

> *Ajout daté du 2026-10-03 01:04:33 UTC (second sceau, A-8)* : le paquet a été révisé et rescellé (sha256 `4d2a8276…`, genTime 2026-10-03T01:04:10Z) ; **l'échéance est désormais 2026-10-04T01:04:10Z** et le commit d'analyse `f35a70c19ba8269f1f7e2bcd31775e4fc513da20` (la commande de garde (2) du §1 se lit avec ce commit à la place de `41f087e…`). Lignes ci-dessus conservées. Le constat B-1 de R-C (chemin de `$J` dans un verdict `raw` de refus) est corrigé dans le code (SHOGEN-RAW-CHEMIN-1, lot CORR) ; écrire le chemin de `$J` au JOURNAL reste fait.

> *Ajout daté du 2026-10-03 01:43:15 UTC (relecture G2 de la partie 4, `docs/G2-partie-4.md`, K-1 ; B-1)* : au §4, le run `suite` doit finir par `Ran 398 tests` et `OK (skipped=2)` (suite du commit d'analyse `f35a70c` : 396 tests verts, les deux tests nommés de D.4 a sautés, variable absente ; mesuré le 2026-10-03 sur une extraction de `b7a1b4a`, avec et sans `SHOGEN_RENDU_PRODUCTION` posée) ; `383` était le compte de `931854c`. Tout autre compte reste un constat au JOURNAL, examiné avant toute lecture des rendus.

> *Ajout daté du 2026-10-03 01:43:15 UTC (relecture G2 de la partie 4, `docs/G2-partie-4.md`, K-2 ; B-2)* : au §3, la production n'est lancée ni au premier plan de l'outil de commandes (borne de 10 min) ni en tâche de fond à son délai par défaut (30 min) : soit détachée (`setsid nohup env -u SHOGEN_S2_CAMPAGNE_CONTROL PYTHONDONTWRITEBYTECODE=1 python3 -B s2-harness/tools/rendu_unique.py … > <scratchpad>/execution/production.log 2>&1 &`, PID et heure écrits au JOURNAL, fin attendue en sondant le PID et ce fichier), soit en tâche de fond avec un délai explicite de 7 200 000 ms. Durée attendue d'après R-B §5 (synthétique, même hôte) : 13 à 15 min. Après toute interruption (borne atteinte, redémarrage de la machine), consigner puis retirer à la main les débris `.rendu-<date>.*` et, s'il existe et est vide, le répertoire `rendu-<date>` (réserve de `rendu_unique.py` l.447) ; ce n'est pas une seconde exécution.

> *Ajout daté du 2026-10-03 01:43:15 UTC (relecture G2 de la partie 4, `docs/G2-partie-4.md`, K-3 ; B-3)* : au §2, (i) le moyen de téléchargement a été éprouvé le 2026-10-03 à 01:42:36 UTC sur le seul fichier de sommes (id `1bA3bmuUZn0XCljRH7GIE54RjMsRI5q9Q`, écrit hors du dépôt) : `curl --fail -L`, HTTP 200, 411 octets, sha256 `70910984076474987239d8c7a9da786acc95c38b375ad572d78afa297bf8caf4` (égal à la clé `sommes`) ; aucun journal téléchargé ; (ii) identifiants Drive des trois journaux : `control.jsonl` `11WjwNZKgo8gW_OnmgAsFbD2b4E2ECrWZ`, `journal.jsonl` `1otC_ZKhiPEVHrqQpTCOlepnBNRjIbSP3`, `raw.jsonl` `1rVmzpisoCrrr-4Ju6-ghVp7XpLh7PERm` (dossier `1TwP2Jtc0-_gAYjDOHHpvfh3XxnR6jtR6` ; les entrées de JOURNAL de 21:2x n'en portent pas) ; (iii) chaque fichier est téléchargé avec `curl --fail -L` ; sa taille est comparée d'abord : une taille différente est un transfert incomplet, refait et consigné ; seul un sha256 différent à taille égale est l'écart qui arrête l'exécution et va à l'investisseur.

> *Ajout daté du 2026-10-03 01:43:15 UTC (relecture G2 de la partie 4, `docs/G2-partie-4.md`, K-4 ; C-2, C-3)* : au §4, `--commit` reçoit le sha complet (40 caractères) de la tête notée au §1, celle que porte `tree.commit` de l'enregistrement, jamais `HEAD` littéral ni une tête postérieure aux commits de JOURNAL du §4 ; au §3, `--auteur` reçoit l'identifiant exact du modèle de l'orchestrateur qui exécute (Gate 0 de sa session), pris dans la liste blanche du lint (`enforcement/lint-model-pinning.sh` l.33).

> *Ajout daté du 2026-10-04 06:52:35 UTC (relecture G2 du lot DETTES-B1, C-3 ; garde (2) du §1, lue contre `HEAD`)* : à partir du commit `0221a74` (lot DETTES-B1, B1-1 ; `rendu_unique.py` à partir de `0789d96`, B1-4), `s2-harness/shogen_s2` et `s2-harness/tools` diffèrent du commit d'analyse `f35a70c` (sha256 de `rendu_unique.py` à la tête `5ee95dbf…` ≠ `sha256_script` `06d189cf…`) : les gardes (2) et (4) refusent à la tête ; tout rejeu (`recompute_*`) ou ré-exécution du rendu de S2 se fait sur une extraction de `f35a70c` ; à la tête, les sorties diffèrent par construction (bloc 5 (d), note k_eff, clé `etiquette` du drapeau 2 de `j28-incluse`, divergences ASN de relevés partiels). La procédure ne se rejoue donc qu'à `f35a70c`.
