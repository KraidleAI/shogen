# Relecture G2 de la partie 3 de S2 (réviseur neuf)

**Versement** : rapport du réviseur G2 neuf (`shogen-worker`, Gate 0 `claude-opus-5-5`), copié tel quel par l'orchestrateur le 2026-10-02 (fichier source sha256 `d8d70a092dd78b1a132afec3d87fc9d53beaadcaa1a433e52b7546af9ef59284`) ; adjudication : annexe B, bloc B.35.

Rédaction : 2026-10-02, de 18:16 UTC (`date -u`) ; relecture menée de 17:48:00Z à 18:15:59Z.

## 0. Gate 0 et cadre

- **Modèle résolu : `claude-opus-5-5`** (identifiant exact fourni par l'environnement de la session ; préfixe attendu
  `claude-opus-5-5` : conforme). Rôle : réviseur G2 (fiche `shogen-worker`, règle 6). Je n'ai généré aucun lot de cette
  partie.
- Brief : `scratchpad/g2-p3/BRIEF-G2-P3.md`, lu en entier avant tout travail.
- Dépôt `/home/user/shogen`, branche `partie-3-paquet`. **Périmètre : `git log 0711cc1..86a8a5b`** (28 commits) ; HEAD
  valait `86a8a5b` à l'ouverture (17:48:00Z, arbre propre). Le commit `6893fb5` (daté 18:01:34Z) est apparu pendant la
  relecture : il est hors du périmètre, et je ne lui ai appliqué que des contrôles mécaniques (constat 12).
- Aucune opération git en écriture. Je n'ai écrit que ce rapport et mes fichiers de travail, dans `scratchpad/g2-p3/`.
  Copies d'arbre : `git archive HEAD s2-harness scripts enforcement`, donc sans `biblio/` ni `docs/`, et sans aucun
  `*.jsonl` (`find … -name "*.jsonl"` : 0). Ces copies (`export/`, `export-t/`), le TMPDIR (`tmp/`) et le dossier de
  journaux vide ont été supprimés à 18:1xZ. Le paquet scellé n'a pas été modifié.

## 1. Attestation D.3

**Je n'ai vu aucun z, aucun K, aucun P̂_more ni aucun φ de campagne, et je n'en ai calculé aucun. Je n'ai lu aucun taux
d'écart ni de panne d'une source de la campagne. Je n'ai ouvert aucune pièce de la liste fermée D.2 : ni les points 1 à
11, ni le point 12 ajouté pendant ma relecture par `6893fb5`.** En détail :

- aucun journal scellé ni copie ;
- aucun `*.jsonl` (aucun n'est suivi par git : `git ls-files '*.jsonl'` = 0) ;
- rien sous `docs/adr-0025/`, et pas la cartographie du 2026-09-29 ;
- aucune transcription de session ;
- aucun accès au dépôt `KraidleAI/monark-governance` ;
- hors du dépôt, seulement mon dossier et le fichier de sommes de clôture, dont je n'ai lu que les empreintes.

`SHOGEN_S2_CAMPAGNE_CONTROL` n'a jamais été posée : chaque exécution Python passe par `env -u`.

Ce à quoi j'ai été exposé (classe M ou synthétique ; ces valeurs sont déjà portées par l'ADR, ses annexes ou le paquet) :

- comptes de D1 : Pyth, 0 `ok` sur 40 804 ;
- comptes de D5 : 5 313 `asn_attribution` dont 815 `resolve_failed` ; 483 `clock_check` ; `resolve_failed` à 15,3 % dans
  la plage contre 1,85 % hors plage (paquet l.50 ; santé du harnais DNS, annexe D.1 n° 8) ;
- comptes de fenêtres : 35 982 ; 2 618 ; 17 314 ; 9 261 ; 38 600 ;
- noms des pièces de D.2, lus dans le texte de l'annexe D ;
- dans l'ajout de `6893fb5` à l'annexe D : la description, sans valeur, de la lecture D.1 n° 16, et le motif FM-1.1 du
  point 12 de D.2 (une locution anglaise, sans chiffre) ;
- empreintes des trois journaux scellés ;
- résultats synthétiques de SIM-NIVEAU et de l'étape S.

## 2. Fichiers ouverts (niveau [lu], lecture seule)

- **Brief** : en entier.
- **`docs/adr-0028/ANNEXE-D-preenregistrement.md`** : en entier (l.1-188, à `86a8a5b`) ; plus les deux lignes ajoutées
  par `6893fb5` (`git show 6893fb5 -- <annexe D>`).
- **Plan, G0, annexes A et B** :
  - `docs/adr-0028/PLAN-PARTIE-3.md` et `docs/adr-0028/G0-partie-3.md`, en entier ;
  - `ANNEXE-A-lots.md` l.1-12 et l.110-130 ;
  - `ANNEXE-B-items.md` : titres, puis l.440-489 (B.30 à B.33). De B.34, seul le titre a été affiché (constat 12).
- **`JOURNAL.md`** :
  - l.234-258, en entier ;
  - `grep -n "2026-10-02"` coupé à 60 caractères, comme le brief le prescrit ;
  - écart déclaré au constat 13 : débuts de lignes de table (l.37-44, 28 caractères) et titres de section (80
    caractères) affichés hors de la plage permise.
- **Code et tests (état final)** :
  - `scripts/sceau/make-tsq.sh` et `verify.sh` en entier ; `s2-harness/tests/test_sceau.py` en entier ;
  - `scripts/sim/sim_garde_niveau.py` et `sim_garde_niveau_oracle_r1.py` en entier ;
  - `s2-harness/tools/rendu_unique.py` : l.6-37, l.77-160, l.161-176, l.177-240, l.264-345, l.395-540 ;
  - `oracle_record.py` l.39-42, l.72-88 et l.136-137 ;
  - `report.py` : lignes de `ranges` (grep) ; `r2.py` : sites `localcontext` (grep) ;
  - `enforcement/lint-model-pinning.sh` l.33 ; `.gitattributes` l.65-67 ;
  - `s2-harness/tests/test_exclusion.py` l.43 et l.265-297 (grep).
- **Diffs** : `39f5cd2`, `b47ff24`, `a4e44d0` (`r1.py`, `test_contexte_decimal.py`), `ced5cb6`, `a6a99d8`, `d69c914`,
  `cc37c8c`, `8e8b174`, `86a8a5b`.
- **Journaux G1** :
  - `docs/G1-partie-3-S.md`, en entier (l.1-367) ;
  - `docs/G1-partie-3-P3.md` : l.112-120 et l.190-214, plus les lignes qui contiennent « 32 » ;
  - `docs/G1-partie-3-P3g.md`, en entier ;
  - `docs/G1-partie-3-R.md` : lu par script pour la recherche de la citation (g), non affiché.
- **Paquet `docs/adr-0028/PAQUET-PREREG-S2.md`** : l.1-108 et l.109-116 ; lignes 132, 136, 150, 165, 171 et 204 (grep) ;
  diff contre `baafb0c`.
- **`docs/adr-0028/CP1-PAQUET-2026-10-02.md`** : l.18-24, l.188-193, titres, et lignes 20, 21, 180, 191 (grep).
- **Sceau** :
  - `docs/adr-0028/sceau/README.md`, en entier ;
  - `PAQUET.sha256` (octets) ;
  - `paquet.tsq` et `paquet.tsr` (`openssl ts … -text`) ;
  - `chain/cacert.pem` et `chain/tsa.crt` (`openssl`).
- **`docs/adr-0028/sim-niveau/`** :
  - `SHA256SUMS`, en entier ;
  - enregistrements d'oracle, comparés en JSON trié ;
  - `garde_niveau.json`, lu par script ; `garde_niveau.txt`, comparé en octets.
- **`docs/DEVOPS.md`** : l.146-158.
- **Fichier de sommes de clôture** (`scratchpad/sceau/SHA256SUMS-cloture-2026-09-28.txt`) : analysé par script. Seuls
  les trois rapprochements de journaux et l'empreinte du fichier ont été imprimés.

## 3. Commandes et sorties (sorties dans `scratchpad/g2-p3/out/`)

| heure (Z) | commande | sortie |
|---|---|---|
| 17:48:00 | `git status` ; `git log 0711cc1..HEAD` ; `--numstat` | arbre propre ; 28 commits ; aucun ne touche `docs/rapports`, `docs/adr-0025` ou un `*.jsonl` |
| 17:51:59-17:52:44 | suite `s2-harness` à `86a8a5b` (`env -u … python3 -B -m unittest discover -s tests -t .`, TMPDIR sur mon dossier) | `Ran 383 tests`, `OK (skipped=2)`, rc 0 (`suite-HEAD.txt`, `f7e0091f…`) ; les deux sauts sont les tests nommés de D.4 a (`test_exclusion.py` l.270, l.297) ; arbre propre après |
| 17:53:19 | `rendu_unique.py --gardes-seules`, journaux = dossier vide, sommes = fichier de clôture, auteur `claude-opus-5-5` | rc 2 ; refus **(3)** (`FileNotFoundError` sur `control.jsonl` du dossier vide) et **(5)** (`T_now 2026-10-02T17:53:19Z < T0 + 24 h (T0 : 2026-10-02 17:44:30+00:00)`) **seuls** ; sortie standard vide (`gardes-seules.stderr`, `1634538e…`) |
| 17:5x | `bash scripts/sceau/verify.sh` | rc 0 ; `PAQUET-PREREG-S2.md: OK` ; `Verification: OK` deux fois ; `Serial number: 0x08CC76D7` ; `Time stamp: Oct  2 17:44:30 2026 GMT` ; manifeste `680a95fd…` (`verify.txt`, `c10da05d…`) |
| 17:5x | export `git archive HEAD s2-harness scripts enforcement` ; suite dans l'export | 383, OK (2 sauts) (`suite-export.txt`, `18af7606…`) |
| 17:5x | `mutants.py` (version finale `8807af03…` : M1 à M13, puis M14 et M4S ajoutés) : M1 à M13 sur l'export | voir §5 (`mutants.json`, `9397018b…`) ; export identique avant et après (empreinte d'arbre) |
| 17:5x | M14 (témoin) et M4 contre la suite entière | M14 tué ; M4 vivant, 383 OK (`mutants-2.json`, `695237b2…`) |
| 18:00:16-18:01:12 | `cargo --locked xtask verify` (code lu, puis compte de VIOLATION, avant affichage) | rc 0 ; 0 VIOLATION ; S-G1 à S-G8, fmt, no_std, clippy : VERT ; S-G6 « 128 = 128 » (`xtask.txt`, `4cbea9a8…`). État de l'arbre non contrôlé pendant cette exécution, car `6893fb5` est daté de 18:01:34Z ; voir le rejeu à `6893fb5` plus bas |
| 18:02:53-18:03:23 | S-b rejoué par moi (`python3.13 -B sim_garde_niveau_oracle_r1.py --r1 <export>/s2-harness --commit 86a8a5b… --json <garde_niveau.json versé> --processus 4`) | rc 0 ; T0 20 cas ; T1 260 + 160 invariants ; T2 7,25·10⁻⁴⁵ ; T3 **2 367** réplications, valeur égale à `r1.regle_critere`, P̂_more identique dans 378 ; écarts relatifs maximaux 3,9·10⁻⁴⁶ (P̂_more) et 4,1·10⁻⁴⁴ (z). Enregistrement (`f8690ff4…`) égal à `garde_niveau_oracle_r1-6564c0f.json` versé, au seul champ `commit_r1` près |
| 18:03:50-18:04:35 | S-a réduit (`--processus 4 --diviseur 20`, Python 3.13.14) | rc 0 ; JSON **`e105573a…`** et texte **`3b5a9104…`** : identiques à l'octet à l'exécution B du journal G1 S (§5) ; empreinte des R/20 premiers enregistrements de A (versée) égale à celle de mon rejeu dans les 20 cas |
| 18:0x | `recoupe_S.py` (`baf58101…`) : tables §6.1 et §6.2 du journal G1 S recalculées depuis les comptes du JSON | **280 cellules, 0 écart** ; chiffres de B.31 retrouvés |
| 18:0x | `texte()` de S-a appliqué au JSON versé ; JSON re-sérialisé | égal à `garde_niveau.txt` versé (67 lignes) ; JSON re-sérialisé égal au fichier |
| 18:07 | à la nouvelle tête `6893fb5` : `git diff --quiet 86a8a5b HEAD -- s2-harness scripts <paquet> docs/adr-0028/sceau` ; `verify.sh` ; `--gardes-seules` ; `xtask verify` | rc 0 (rien de changé sur ces chemins) ; `verify.sh` 0 ; refus (3) et (5) seuls (18:07:09Z) ; `xtask` rc 0, 0 VIOLATION, VERT (`xtask-6893fb5.txt`, `c040fb3d…`) ; arbre propre |
| 18:1x | test proposé (C-1) dans une seconde copie (`export-t`), puis M4 et M4b (`mutants_t.py`, `e0b3bb21…`) | vert sur le code de HEAD ; M4 et M4b tués ; suite entière : **384**, OK (2 sauts) (`suite-export-t.txt`, `ddd501f2…`) ; diff proposé `test_sceau-propose.diff` (`87ecfbde…`) |

## 4. Constats numérotés

1. **Code P3a à P3g : conforme au G0 §P3 et aux items de B.30.** Point par point :
   - **P3a** (convention unique des chemins) :
     - `make-tsq.sh` l.12-14 : chemins relatifs à la racine ; refus des chemins absolus, des segments `..`, des lettres de
       lecteur et des barres inverses, avant l'écriture du manifeste et de la requête ;
     - `verify.sh` l.13 : relecture depuis la racine ;
     - `test_sceau.py` : TSA de test locale, aucun réseau.
   - **P3b** : `report.py` l.734 accorde les lignes de week-end au nombre de plages, sous `if ranges:` (l.682).
   - **P3c** (fabrique de contexte) :
     - `r1.contexte_decimal()` rend un contexte neuf à chaque appel, avec des valeurs identiques ;
     - 30 sites `localcontext(…contexte_decimal())` dans le code : r1 14, lm 3, r2 10, report 2, `rendu_unique` 1 ;
     - plus aucun `CONTEXTE_DECIMAL` dans `s2-harness`, hors du repli de S-b (`sim_garde_niveau_oracle_r1.py` l.36-38) ;
     - `closure.py` (quarantaine) reste hors champ.
   - **P3d** : `rendu_unique.py` l.443-445 et l.455-458 : création exclusive de la réserve sous POSIX, renommage sur la
     réserve, retrait de la réserve seulement si elle est vide.
   - **P3e** : l.169-171 : l'arbre de travail est jugé contre le commit résolu (`git diff --quiet <head résolu>`), et
     `git status` entier est gardé.
   - **P3f** : l.264-274 : candidats donnés par `git log -G`, chacun confirmé par `lignes_avec` sur
     `<commit>:JOURNAL.md` (sha entier sur une ligne).
   - **P3g** : `verify.sh` l.15 et l.17 : `-queryfile` et `-data`, écart en code 3, avant l'impression du genTime.
2. **Tests et mutants.**
   - La suite est verte : 383 tests, 2 sauts.
   - Sur 14 mutants tirés sur les changements de P3 (§5 : M1 à M13 et M4b), 12 sont tués par un test visé ; le témoin
     M14, hors P3, est tué lui aussi.
   - **M4** (l.15 de `verify.sh` retirée, `-data` seule) et **M4b** (écart de la l.15 ignoré) **survivent à la suite
     entière**. La liaison du jeton à la requête faite (nonce), que l'en-tête de `verify.sh` (l.6-7), le commentaire de
     la l.16 et le journal G1 de P3g (§3, l.49-52 : « les deux ») présentent comme nécessaire, n'est donc couverte par
     aucun test du script.
   - La sonde d'équivalence du G1 de P3g (§2, l.37-40) n'a pas été rendue reproductible, et ses mutants G1 à G5 ne
     retirent pas `-queryfile`.
   - La voie (a) de `rendu_unique.py` est, elle, couverte : le mutant symétrique M14 (l.229) est tué par
     `test_voie_a_refus` (« autre requête »). L'ouverture de l'exécution n'est donc pas exposée ; seul l'outil de
     vérification humain l'est. **Correction C-1.**
3. **R-25 et R-13.**
   - Lignes ajoutées et retirées par commit : P3a +84 −2, P3b +23 −7, P3c +66 −44, P3d +27 −3, P3e +13 −6, P3f +44 −10,
     P3g +33 −11, S-b +183, S-a +199. Toutes sont sous 200 lignes ajoutées.
   - Aucun `TODO` ni `FIXME` nu : la seule occurrence dans les lignes ajoutées de la partie est la mention « aucun
     `TODO` ni `FIXME` » du journal G1 S (l.114).
   - Aucun CR dans les fichiers ajoutés.
4. **Étape S : sorties cohérentes avec `docs/G1-partie-3-S.md`.**
   - Empreintes égales au §9 : JSON `f421c419…`, texte `e1d79beb…`, enregistrements `9a689015…` et `0d44c76a…`.
   - Les tables §6.1 et §6.2 sont égales au recalcul (280 cellules, 0 écart).
   - Le texte versé est le rendu de `texte()` sur le JSON versé.
   - Bit-identité recontrôlée par mon propre rejeu R/20 (égal à B).
   - S-b rejoué à HEAD : mêmes nombres.
   - Les chiffres de B.31 et du pt 11 du paquet (0,01147, SE 0,00061 ; 0,01213, SE 0,00063 ; 0,00357, SE 0,00034 ;
     0 sur 6 000) sont recalculés.
   - Scripts : `sim_garde_niveau.py` `51902b0d…` et `sim_garde_niveau_oracle_r1.py` `7fbc82d3…`, égaux au journal ;
     `scripts/sim` est inchangé entre `8b14567` et HEAD.
   - G0 §S : cas fixés avant toute exécution (§1, 14:50Z), même modèle et même graine que SIM-NIVEAU, erreurs-types
     imprimées. La limite pré-déclarée est écrite au paquet (l.132 ; SHOGEN-GARDE-NIVEAU-ZSEUL-1), sans révision.
5. **SHOGEN-SIM-SOMMES-1 : contrôle de `docs/adr-0028/sim-niveau/SHA256SUMS`** (18 lignes ; `sha256sum -c` rc 1).
   - **7 lignes OK** : l.11, l.13 à l.18.
   - **11 lignes illisibles** :
     - 10 fichiers listés mais non versés : l.1-3 `execution-B/…`, l.4-9 `oracle-1b/…`, l.12 `sim_niveau.log.txt` ;
     - 1 chemin inexact : l.10 `oracle-4a-4b/oracle_4a_4b.json`, versé à la racine du dossier sous `oracle_4a_4b.json`,
       avec le même sha256 `bd3cc311…`.
   - **2 fichiers versés non listés** : `garde_niveau_oracle_r1-6564c0f.json` (`6a6d2db1…`) et `oracle4-6564c0f.json`
     (`818452ad…`), tous deux du commit `41f087e`.
   - Le libellé de B.31 (l.461), « 11 fichiers absents du dépôt et un chemin inexact », compte 12 : il faut lire « 10
     fichiers absents et un chemin inexact, 11 lignes illisibles ».
   - Le paquet scellé cite `SHA256SUMS` l.11, l.13 (paquet l.136) et l.15-16 (l.150) : toute correction doit donc être
     un ajout en fin de fichier.
   - **Correction C-2**, éprouvée sur une copie : trois lignes ajoutées, `tail -n 3 | sha256sum -c` OK, l.1-18
     inchangées.
6. **Bloc machine du paquet, recalculé par commande.** Les huit valeurs du bloc (l.214-221) sont égales :
   - `commit_analyse` `41f087ef3e0a621ddb04fa4f2af8733e5fd5a0f9` est le parent de `ddf8c54`, donc la tête au
     remplissage ; `git diff --quiet 41f087e HEAD -- s2-harness/shogen_s2 s2-harness/tools` rc 0 ; arbre et
     `git status --ignored` vides sur ces chemins ;
   - `sha256_script` `67b897a9…` = `rendu_unique.py` (fichier et blob) ;
   - `journal control.jsonl`, `journal.jsonl` et `raw.jsonl` : chacun égal à son unique ligne du fichier de sommes (mode
     `*`) ; `control.jsonl` = `SHA_CONTROL_SCELLE` (`test_exclusion.py` l.43) ;
   - `sommes` `70910984…` = sha256 du fichier (411 octets, ASCII, LF, 5 lignes) ;
   - `cacert_sha256` `2151b611…` et `tsa_crt_sha256` `8bfb0305…` = fichiers de `chain/`.

   Le paquet scellé est, à l'octet, le texte validé `baafb0c` (`1295e907…`) dont seules les l.214-221 sont substituées
   par celles de HEAD (reconstruction comparée octet à octet). La section 10.2 (texte de la règle) est identique à
   `8b9536b`, `baafb0c`, `ddf8c54` et HEAD. Le bloc est accepté par `lire_bloc` (garde « bloc » levée).
7. **Sceau.**
   - Manifeste `PAQUET.sha256` : 100 octets, UTF-8 sans BOM, un LF, aucun CR ; format `sha256sum -b` :
     `494d770d… *docs/adr-0028/PAQUET-PREREG-S2.md` ; `git check-attr text` : `unset` ; `git ls-files --eol` :
     `attr/-text` ; blob `85e31fd9…` = fichier.
   - Requête : empreinte `680a95fd…` = sha256 du manifeste ; nonce `0xE27D929D2F21D47F`.
   - Jeton (`5f5ce535…`, 4 644 octets) : `Granted`, même empreinte, même nonce, série `0x08CC76D7`, genTime
     `Oct  2 17:44:30 2026 GMT`.
   - Historique : requête et manifeste inchangés depuis `0743365`, jeton depuis `48797f1`.
   - Chaîne : `openssl verify` OK ; `tsa.crt` porte l'usage étendu Time Stamping (critique) ; échéances 2040-02-02
     (`tsa.crt`) et 2041-03-07 (racine) ; fichiers LF ; blobs égaux aux fichiers.
   - README (l.7-11, l.24-30) et JOURNAL (l.248, l.252-256) concordent sur le sha du paquet, le sha du manifeste, la
     série, le genTime et l'échéance (2026-10-03T17:44:30Z = genTime + 24 h).
   - Ordre : go (`5193f24`, 17:31:02Z) → scellement (`0743365`, 17:44:23Z) → jeton (17:44:30Z).
   - La correction `86a8a5b` ne change que les guillemets de la l.29 du README (et ajoute une parenthèse) ; le README
     est identique entre `48797f1` et `8e8b174`.
8. **`--gardes-seules`** : seuls les refus (3) et (5) sont levés, à `86a8a5b` comme à `6893fb5`. Les gardes « bloc »,
   (1), (2), (4) et (6) (voie a) sont levées.
9. **Traçabilité.** Sont tracés :
   - P3a-P3g, S-a, S-b, R et V par l'annexe A (l.118-128) ;
   - les commits Sc, P1, P et les versements par leur propre entrée JOURNAL ou une entrée qui les cite (l.234-258) ;
   - les trois G0 (`32044eb`, `3414e0f`, `8ec45b8`) par les lignes d'annexe A qui citent leurs sections.

   **`c32c285`** (`biblio/INDEX.md`, trois artefacts, compte 125 → 128) n'a ni ligne d'annexe A ni entrée JOURNAL qui le
   nomme. L'étape L a ses entrées (15:23 et 15:35), mais le versement à l'INDEX n'y figure pas (B.30 l.453 : « versement
   à `biblio/` en cours »). **Correction C-3.**
10. **Attestation D.3 (h)** (annexe D l.118 à `86a8a5b`, l.120 à `6893fb5`, « §1 et §7, recopié »).
    - La citation n'est pas littérale : « …et n'en ai calculé aucun ; aucun taux d'une source réelle. Je n'ai ouvert
      aucune pièce de D.2 (points 1 à 11) » ne se trouve ni au §1 (l.20-21) ni au §7 (l.191) du rapport du cp-1.
    - Le fragment « aucun taux d'une source réelle » n'y figure nulle part. C'est une condensation fidèle sur le fond,
      présentée comme une recopie.
    - La citation (g) est, elle, littérale dans `docs/G1-partie-3-R.md` (espaces normalisés).
    - **Correction C-4**, sous forme d'erratum daté, en ajout.
11. **Errata et items.**
    - L'erratum de B.32 (nom d'item de B.31) est déclaré.
    - L'erratum « gate rouge commise » (JOURNAL l.258 : `48797f1` et `8e8b174` commis sans verdict de `xtask`) est
      déclaré et corrigé par `86a8a5b` ; je n'ai pas reproduit le rouge (limite L-3).
    - SHOGEN-DOC-ERRATA-P3-1 est exécuté par `8e8b174` : ajouts datés, lignes antérieures inchangées. L'insertion dans
      doc 10 après la l.298 décale de +2 les lignes de doc 10 que cite le paquet (l.379-380, 386, 392-395, 519-522,
      555-579 ; contenu identique, vérifié par empreinte de ligne). Le paquet ancre ses renvois à `8b14567` (en-tête
      l.5) : ce n'est pas un défaut.
    - Les items dus au paquet par B.30 à B.32 y figurent (`grep -c` ≥ 1 chacun). SHOGEN-SIM-REJEU-GEL-1 a été rejoué à
      `6564c0f` : le code est identique à `41f087e` (rc 0), ce que déclare JOURNAL l.254.
12. **Commit `6893fb5`, apparu pendant la relecture** (hors périmètre).
    - Il touche seulement `JOURNAL.md` (+2), l'annexe B (+14, B.34) et l'annexe D (+2 : D.1 n° 16, D.2 n° 12).
    - Il ne change ni le code, ni les scripts, ni le paquet, ni le sceau. `verify.sh`, `--gardes-seules` et
      `xtask verify` sont inchangés à cette tête.
    - Il ajoute à D.2 un point 12 (dépôt `KraidleAI/monark-governance` : pièces de D.2 n° 2 et sujet du commit
      `aa04924`). Mon attestation couvre ce point.
    - Il inscrit en D.1 n° 16 une exposition de l'orchestrateur de la session cloud, postérieure au scellement, de classe
      **R présumée**.
    - Je n'en ai pas examiné le fond (B.34 et l'entrée JOURNAL n'ont pas été lus). Je signale à l'orchestrateur que les
      conditions de D2 pt 4 (paquet l.55 : attestations des décideurs) sont à rapprocher de cette ligne ; c'est la
      déviation déclarée de D2 pt 8 (paquet l.90), hors de ma relecture.
13. **Écart du réviseur, déclaré.** Pour situer la table d'unités contrôlée par S-G8, j'ai affiché, hors de la plage du
    JOURNAL permise par le brief, les débuts de lignes de table (l.37-44, coupés à 28 caractères) et les titres de
    section (coupés à 80 caractères). Je n'y ai vu que des dates et des débuts de titres, aucun chiffre de résultat. Je
    n'ai rien lu d'autre de ces lignes.
14. **Gates.** `cargo --locked xtask verify` : rc 0, 0 ligne VIOLATION, VERDICT GLOBAL VERT, à `86a8a5b` comme à
    `6893fb5`.

**Observations, sans correction :**

- **O-1.** L'annexe A l.120 et le sujet de `a4e44d0` parlent de « 32 sites ». Il s'agit de 32 usages : 30 sites de code
  et 2 usages de test (journal G1 P3 l.198-199, exact).
- **O-2.** Le commentaire de `make-tsq.sh` l.13 dit « contrôlée avant toute écriture », alors que `mkdir -p "$D/chain"`
  (l.10) précède le contrôle. Le test fige `["chain"]` comme état après refus ; le manifeste et la requête ne sont jamais
  écrits.
- **O-3.** `paquet.tsq` et `paquet.tsr` relèvent de `text=auto eol=lf`, détectés binaires par git (`i/-text`), donc sans
  conversion aujourd'hui. Un `-text` explicite serait plus strict ; D.4 c ne l'exige que pour le manifeste.
- **O-4.** Dans le journal G1 S §10, E-10 est placé entre E-8 et E-9 (forme).

## 5. Mutants (une substitution textuelle par mutant, occurrence unique exigée, copie de l'export, fichier restauré et relu)

| # | lot | mutation | résultat | test qui tue |
|---|---|---|---|---|
| M1 | P3a | motif `*/../*` retiré du contrôle de `make-tsq.sh` | tué | `test_make_tsq_refuse_un_chemin_hors_convention` (« segment .. ») |
| M2 | P3a | manifeste relu depuis le dossier de sceau (ancienne l.13) | tué | `test_make_tsq_puis_verify_depuis_la_racine` |
| M3 | P3g | écart `-data` ignoré (`\|\| true`) | tué | `test_verify_lie_le_jeton_au_manifeste` |
| **M4** | P3g | ligne `-queryfile` (l.15) retirée, `-data` seule | **vivant** (suite entière : 383 OK) | test proposé en C-1 |
| **M4b** | P3g | écart `-queryfile` ignoré (`\|\| true`) | **vivant** | test proposé en C-1 |
| M5 | P3b | singulier gardé pour deux plages (`<= 2`) | tué | `test_lignes_week_end_accordees_au_nombre_de_plages` (2 plages), et deux tests de `test_sensibilite` |
| M6 | P3c | `Emax` de la fabrique à 99999 | tué | `test_contexte_nomme_complet` |
| M7 | P3c | site `_quantize` de r2 rendu au contexte appelant | tué | `test_sites_sous_contexte_hostile` (r2 `_quantize`) |
| M8 | P3d | réserve non exclusive (`makedirs(…, exist_ok=True)`) | tué | `test_cible_apparue_avant_le_renommage` |
| M9 | P3d | réserve vide laissée après un échec | tué | `test_echec_a_chaque_pas_rien_ne_reste` (« renommage ») |
| M10 | P3e | arbre jugé contre `HEAD` courant | tué | `test_gardes_lisent_le_head_resolu_une_fois` |
| M11 | P3f | `-S` au lieu de `-G` | tué | `test_voie_b_premiere_ligne_entiere_pas_une_sous_chaine` (« remplacement à compte égal ») |
| M12 | P3f | candidat non confirmé sur sa ligne | tué | même test (trois sous-cas) |
| M13 | P3f | `--reverse` retiré (dernier candidat) | tué | `test_voie_b_go_epingle_et_garde_5` |
| M14 | témoin hors P3 | voie (a) de `rendu_unique.py` sans `-queryfile` | tué | `test_voie_a_refus` (« autre requête ») |

Bilan : 12 mutants de P3 tués sur 14, plus le témoin M14 (hors P3), tué. Les deux vivants (M4, M4b) relèvent d'un même
manque, et ils sont tués par le test de C-1.

## 6. Verdict : **ACCEPTE-AVEC-CORRECTIONS**

Liste fermée. Aucune correction ne touche les octets scellés (paquet, manifeste, requête, jeton), ni les chemins de la
garde (2), ni le bloc.

- **C-1** : `s2-harness/tests/test_sceau.py`, après la l.93 (fin de la classe `TestSceauScripts`).
  - **Texte actuel** : l.93 `                                 p.stdout + p.stderr)`, puis deux lignes vides et
    `if __name__ == "__main__":` (aucune méthode).
  - **Texte proposé**, inséré après la l.93 (13 lignes, diff `test_sceau-propose.diff`, `87ecfbde…`) :

    ```python

        def test_verify_lie_le_jeton_a_la_requete(self):
            """SHOGEN-SCEAU-VERIFY-DATA-1, autre moitié (sonde d'équivalence du G1 de P3g, §2) : après le jeton, requête
            refaite par make-tsq.sh sur le même manifeste (autre nonce) : étape (1) passe, étape (2) refuse, code 3,
            dernière ligne « JETON : ÉCART », étape (3) jamais atteinte. Rougit si le jeton n'est vérifié que contre les
            octets du manifeste (-data seul)."""
            d = self.sceller()
            q = Path(d, SCEAU, "paquet.tsq").read_bytes()
            p = script("make-tsq.sh", d, SCEAU, PAQUET)
            self.assertEqual((p.returncode, Path(d, SCEAU, "paquet.tsq").read_bytes() == q), (0, False), p.stderr)
            p = script("verify.sh", d)
            self.assertEqual((p.returncode, f"{PAQUET}: OK" in p.stdout, p.stdout.splitlines()[-1], "== (3)" in p.stdout),
                             (3, True, "JETON : ÉCART", False), p.stdout + p.stderr)
    ```

  - Éprouvé : vert sur le code de HEAD ; M4 et M4b rouges ; suite entière 384, OK (2 sauts) ; style du fichier inchangé
    (longueur maximale 129).
  - `s2-harness/tests` est hors des chemins de la garde (2) (`rendu_unique.py` l.29) : `commit_analyse`,
    `sha256_script` et le bloc restent valides.
  - **Si l'orchestrateur juge que « aucun code après le gel du commit d'analyse »** (paquet l.204) couvre aussi les
    tests, C-1 prend sa forme de repli : une ligne datée de l'annexe B, dans le bloc de l'adjudication de cette relecture
    (après B.34), dont le texte proposé est :

    `| SHOGEN-SCEAU-VERIFY-REQUETE-1 | `scripts/sceau/verify.sh` l.15 : la vérification `-queryfile` (liaison du jeton à la requête faite, nonce) n'est couverte par aucun test ; mutants M4 (ligne retirée) et M4b (écart ignoré) de la relecture G2 de la partie 3 vivants contre la suite entière (383, OK) ; la voie (a) de `rendu_unique.py` est couverte (`test_voie_a_refus`, « autre requête ») ; construction : test `test_verify_lie_le_jeton_a_la_requete` (rapport G2 de la partie 3, C-1 ; vert sur `86a8a5b`, rouge sous M4 et M4b) | orch. | après l'exécution unique (aucun code après le gel) | 13 lignes de test [mesuré] | G2 partie 3, C-1 |`

- **C-2** (SHOGEN-SIM-SOMMES-1), en deux parties.
  - **(a) `docs/adr-0028/sim-niveau/SHA256SUMS`, après la l.18** (dernière ligne).
    - **Texte actuel** : l.18 `0d44c76afa251c85f80723fa55751ce822036308ad623b971ad2f73eb8ef4ad5 *oracle4-3414e0f.json`,
      fin de fichier.
    - **Texte proposé** : trois lignes ajoutées, format `sha256sum -b`, LF :

      ```
      bd3cc31125ec83ad349f1a130574ff563d9f32f1aeb7dfbdc912d8fcacf63e5e *oracle_4a_4b.json
      6a6d2db1d048b8177477c677b9701b862120383168a929d0df627eaa98665b96 *garde_niveau_oracle_r1-6564c0f.json
      818452adedbc4c24b0025eb38be363312fa90023d8dc2cbeea64180e65491532 *oracle4-6564c0f.json
      ```

    - Les l.1-18 restent inchangées, y compris l.11, l.13 et l.15-16, citées par le paquet. Fichier obtenu :
      `526d6447…` (`out/SHA256SUMS-propose`). Le journal G1 S (§9, l.329) garde l'empreinte de l'état à `8b14567`
      (`47b22361…`), seule citation de cette empreinte.
  - **(b) Annexe B, bloc de l'adjudication de cette relecture (après B.34), ligne datée** (texte proposé) :

    *« SHOGEN-SIM-SOMMES-1, clos (relecture G2 de la partie 3, 2026-10-02 18:1x UTC, `sha256sum -c` dans `docs/adr-0028/sim-niveau/` à `86a8a5b`) : `SHA256SUMS` (`47b22361…`, 18 lignes) : 7 lignes OK (l.11, l.13 à l.18) ; 11 lignes illisibles, soit 10 fichiers listés non versés (l.1-3 `execution-B/…`, l.4-9 `oracle-1b/…`, l.12 `sim_niveau.log.txt`) et 1 chemin inexact (l.10 `oracle-4a-4b/oracle_4a_4b.json`, versé à la racine sous `oracle_4a_4b.json`, même sha256 `bd3cc311…`) ; 2 fichiers versés non listés (`garde_niveau_oracle_r1-6564c0f.json`, `oracle4-6564c0f.json`, commit `41f087e`). Lignes existantes non touchées (le paquet cite l.11, l.13, l.15-16) ; trois lignes ajoutées en fin de fichier aux chemins exacts. Le libellé de B.31 « 11 fichiers absents du dépôt et un chemin inexact » se lit « 10 fichiers absents et un chemin inexact (11 lignes illisibles) » ; la ligne de B.31 est conservée. »*

- **C-3** : `JOURNAL.md`, en ajout après la dernière ligne (l.260 à `6893fb5`).
  - **Texte actuel** : aucune entrée ne nomme `c32c285`.
  - **Texte proposé** :

    `> **2026-10-02 18:xx UTC — Traçabilité (relecture G2 de la partie 3, C-3)** : le commit `c32c285` (`biblio/INDEX.md` : trois artefacts versés à la partie 3, Künsch 1989, Fisher 1921 et Agresti 2013 partielle pp. 240-252 ; scans et sidecars OCR ; compte 125 → 128) relève de l'étape L (entrées de 15:23 et 15:35 UTC) ; S-G6 : 128 = 128 (`xtask verify` VERT à `86a8a5b`).`

- **C-4** : `docs/adr-0028/ANNEXE-D-preenregistrement.md`, en ajout en fin de fichier (après la l.190 à `6893fb5`, pour
  ne décaler aucune ligne citée).
  - **Texte actuel** : l.120 (à `6893fb5`), citation de (h) donnée comme « recopiée ».
  - **Texte proposé** :

    `*Erratum daté du 2026-10-02 18:xx UTC (relecture G2 de la partie 3, C-4 ; la citation de D.3 (h) est inchangée)* : la citation de (h) n'est pas une recopie littérale ; elle condense le rapport `docs/adr-0028/CP1-PAQUET-2026-10-02.md` sans en changer le sens. Texte littéral du §1, l.20-21 : « Je n'ai vu aucun z, aucun K, aucun P̂_more ni aucun φ de campagne, et je n'en ai calculé aucun. Je n'ai lu aucun taux d'écart ni de panne d'une source de la campagne. Je n'ai ouvert aucune pièce de la liste fermée D.2 (points 1 à 11) » ; du §7, l.191 : « je n'ai vu aucun z, aucun K, aucun P̂_more ni aucun φ de campagne, et n'en ai calculé aucun ; aucune pièce de D.2 ouverte ». Ajout de (h) : commit `0ca1f4c`.`

## 7. Limites rencontrées : items proposés (règle PAROXYSME)

- **L-1** (forme de repli de C-1 seulement) : SHOGEN-SCEAU-VERIFY-REQUETE-1, texte au §6.
- **L-2. Le contrôle FM-1.1 des blocs B.32 et B.33 n'est pas rejouable par un réviseur G2.**
  - `fm11.py` (`886cc676…`) et ses sorties sont dans le scratchpad de la session, hors du périmètre admis du réviseur.
  - Les transcriptions sont soit la pièce de D.2 n° 11, soit des transcriptions de sous-agents.
  - Je n'ai pu ni vérifier les « 0 fragment » ni les empreintes `796ece54…`, `a4ab03ce…`, `03e57a35…`.
  - Item proposé : **SHOGEN-FM11-VERIFIABLE-1**. Construction : verser au dépôt `fm11.py` et ses sorties JSON, sans
    transcription, avec leurs sha256, pour qu'un tiers recoupe au moins les empreintes et la logique du script.
    Propriétaire : orchestrateur ; avant le cp-2.
- **L-3. Deux points non reproduits.**
  - L'empreinte de la « règle scellée » `ea3a2d94…` (G0 §P3, journal G1 P3 l.115-116) vient d'un outil du worker
    (`regle_fixtures.py`) absent du dépôt. Elle est couverte indirectement : S-b à HEAD donne 2 367 égalités avec
    `r1.regle_critere`, et la suite est verte.
  - Le rouge de S-G5 à `48797f1` et `8e8b174` aurait exigé une copie de l'arbre avec `biblio/`, ou une modification de
    l'arbre de travail, deux choses exclues par le brief.
  - Item proposé, au choix de l'orchestrateur : **SHOGEN-REGLE-EMPREINTE-OUTIL-1** (verser `regle_fixtures.py` sous
    `scripts/`, pour que l'empreinte de la règle soit recalculable par tout réviseur).
- **L-4. Exposition de classe R présumée de l'orchestrateur après le scellement** (D.1 n° 16, `6893fb5`).
  - C'est hors de ma relecture, mais elle touche les conditions de D2 pt 4 (attestations des décideurs).
  - Elle est rendue à l'orchestrateur et à l'investisseur, sans proposition de ma part.

## 8. Déclaration pour le contrôle FM-1.1 de ma transcription

Occurrences de chemins ou de noms de pièces de D.2 **dans mes entrées d'outils** :

- `':(exclude)docs/rapports' ':(exclude)docs/adr-0025' ':(exclude)biblio'`, dans deux `git diff 0711cc1 HEAD` (compte
  R-13, puis localisation) : exclusion à la source, prescrite par le brief ;
- `--exclude-dir=rapports --exclude-dir=adr-0025 --exclude-dir=biblio`, dans un `grep -rl "47b22361"` (noms de fichiers
  seulement ; résultat : `docs/G1-partie-3-S.md`) ;
- motifs `rapports\|adr-0025\|jsonl`, dans un `grep -c` sur ma propre sortie de `xtask` (compte : 0, avant affichage) ;
- `git ls-files '*.jsonl'` et `find <export> -name "*.jsonl"` (comptes : 0 et 0) ;
- noms nus `control.jsonl`, `journal.jsonl`, `raw.jsonl`, comme clés de rapprochement dans mon script de lecture du
  fichier de sommes (empreintes seulement) ; `--journaux <mon dossier>/journaux-vide` pour `--gardes-seules`
  (`rendu_unique` a tenté `journaux-vide/control.jsonl`, inexistant) ;
- chemin du fichier de sommes `scratchpad/sceau/SHA256SUMS-cloture-2026-09-28.txt`, admis par le brief et par D.2 n° 7
  et n° 8 ;
- `git show 6893fb5 -- docs/adr-0028/ANNEXE-D-preenregistrement.md` : annexe D, non interdite ; sa sortie porte des
  noms de pièces de D.2 n° 2, le nom du dépôt `KraidleAI/monark-governance` et le motif FM-1.1 du point 12.

**Dans les résultats d'outils**, on trouve des noms de pièces de D.2 lus dans le texte de l'annexe D, du plan, du G0, du
JOURNAL (l.234-258), du paquet, du rapport du cp-1 et du sujet du commit `6893fb5`. On trouve aussi l'identifiant de
session de D.2 n° 11, dans les lignes `Claude-Session:` des messages de commit affichés par `git show` : la transcription
n'a jamais été ouverte. Aucun fichier ouvert par `Read` ou `cat` n'est une pièce de D.2.

## 9. Fichiers de travail (dossier `scratchpad/g2-p3/`)

- Scripts :
  - `mutants.py` `8807af03…` ;
  - `mutants_t.py` `e0b3bb21…` ;
  - `recoupe_S.py` `baf58101…`.
- `out/` :
  - suites : `suite-HEAD.txt` `f7e0091f…`, `suite-export.txt` `18af7606…`, `suite-export-t.txt` `ddd501f2…` ;
  - sceau et gardes : `verify.txt` `c10da05d…`, `gardes-seules.stderr` `1634538e…` ;
  - gates : `xtask.txt` `4cbea9a8…`, `xtask-6893fb5.txt` `c040fb3d…` ;
  - mutants : `mutants.json` `9397018b…`, `mutants-2.json` `695237b2…` ;
  - étape S : `garde_niveau_oracle_r1-G2.json` `f8690ff4…`, `sa-R20/garde_niveau.json` `e105573a…`,
    `sa-R20/garde_niveau.txt` `3b5a9104…` ;
  - propositions : `SHA256SUMS-propose` `526d6447…`, `test_sceau-propose.diff` `87ecfbde…`.
- Supprimés : `export/`, `export-t/`, `tmp/`, `journaux-vide/`.
