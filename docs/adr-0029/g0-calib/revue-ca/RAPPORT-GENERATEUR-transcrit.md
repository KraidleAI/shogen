# Rapport du générateur de CALIB-ACTIFS, avec les sections datées des corrections (§11, §12) (transcrit)

> Transcription par l'orchestrateur le 2026-10-09 12:17:23 UTC du fichier RAPPORT-GENERATEUR.md ; contrôle FM-1.1 des transcripts du générateur, du réviseur, du correcteur et du contre-contrôleur : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Rapport du générateur : lot CALIB-ACTIFS, code CA-0 à CA-6 sur fixtures synthétiques

- **Gate 0** : modèle résolu `claude-opus-5-5` (identifiant donné par l'environnement), rôle worker générateur (G1),
  effort `max` demandé ; l'effort n'est pas vérifiable depuis la session.
- **Dates** (`date -u`) : reprise le 2026-10-09 à 06:31 UTC (le démarrage du 2026-10-08 23:0x n'avait rien laissé dans
  `diffs/`, `outils/`, `travail/` : vides, vérifiés) ; série close à 08:41 ; rapport à 08:4x UTC.
- **Base** : diffs produits sur `ebd1560` (consigne de l'orchestrateur), extraite par `git archive` avec les exclusions
  habituelles ; tête du dépôt au départ et à la fin : `1a388e1`. Dépôt réel lu seulement (`--no-optional-locks`), aucune
  écriture git dans le dépôt, aucun commit nulle part.
- **Rattachement** [lu] : G0 `docs/adr-0029/g0-calib/G0-CALIB-ACTIFS.md` et son ajout daté (INV-1 = A) ; `PROPOSITION.md`
  (829 lignes, en entier) corrigée par `AVIS.md` (en entier) ; ADR-0029 l.176-214, l.403, l.405 ;
  `docs/adr-0029/calib/SOURCES-HISTORIQUES.md` (en entier) ; items SHOGEN-S2BIS-SIGMA-ACTIFS-1, -CALIB-L189-1,
  -HORODATAGE-SENS-1, -CADENCE-AGREG-1, -P1-ESTIMATION-1, SHOGEN-MUTANTS-SITE-APPEL-1 (annexe B, par leur nom) ; patron
  `scripts/plan-s2bis-2/` (README, parametres, socle, lancer.sh, tests/__init__, test_identite, test_lancer l.1-140) et
  `scripts/plan-s2bis/regles.py` (lu, jamais importé dans le lot) ; `s2bis/shogen_s2bis/recalc/config_analyse.py` (lu).
- **tau_sigma.txt** : jamais ouvert par moi ; sha256 relevé par `sha256sum` (`409b2a5e…e6d9`, égal au SHA256SUMS versé) ;
  forme du bloc machine apprise du code qui l'écrit (`scripts/plan-s2bis/tau_sigma.py` l.67-78). Les tests ne l'interprètent
  jamais (hachage, copie à un octet altéré).

## 1. Série de diffs (dossier `diffs/`, à appliquer dans l'ordre sur `ebd1560`)

Lecture retenue de la taille (Q-CA3-1) : au plus 200 lignes ajoutées par diff, **tout compris** (code, tests, données,
`gates.yml`). Plancher = valeur `--plancher` du job `calib-actifs-unittest` après le diff (`--egal`, Ran exact).

| diff | objet | lignes ajoutées (hors tests) | plancher | sha256 du diff | mutants (tués / lancés) |
|---|---|---|---|---|---|
| CA-0a | job CI, parametres.json, socle I (refus, garde, schéma) | 200 (144) | 3 | `27a1b07d…1ec4` | 12/12 |
| CA-0b | socle II : cohérence, garde réseau des tests, épingle et bloc de tau_sigma | 192 (77) | 6 | `899275f3…91df` | 18/18 |
| CA-0c | fenêtre, strates, planchers des oracles, écriture `.partiel` | 128 (52) | 9 | `9c1ac953…9f0b` | 13/13 |
| CA-1a | acquisition I : lecture d'URL, essais, manifeste, reprise ; serveur local | 198 (77) | 11 | `515ca7dc…a17c` | 13/13 |
| CA-1b | séries (URL, formats), mois, mensuels Binance (`.CHECKSUM`) et OKX | 111 (52) | 14 | `13eafdb9…368d` | 13/13 (2e campagne) |
| CA-1c | Kraken par plages (zipfile sur Range), CA/kraken | 126 (61) | 16 | `c1bbb438…232d` | 13/13 (2e) |
| CA-2a | pages Coinbase, Bitstamp, Bitfinex ; débit ; point d'entrée ; garde mandataire | 184 (73) | 20 | `72dff841…4537` | 16/16 (3e, isolée) |
| CA-3a | six lecteurs de bougies, normalisation | 190 (112) | 24 | `33a20067…aa99` | 15/15 (2e) |
| CA-3b | dernier prix connu, âges, chargement, oracle de SH §4 | 161 (79) | 28 | `e242192c…083b` | 13/13 (2e) |
| CA-4a | σ (sigma.py), quantile, vecteurs Q-CA-13 | 182 (82) | 33 | `9c985466…4144` | 14/14 (2e) |
| CA-4b | τ I : population, médiane leave-one-out, exclusion | 105 (45) | 37 | `b4bdc19b…d43b` | 12/12 (2e) |
| CA-5a | règle de grille, τ des places, τ des agrégateurs | 125 (63) | 40 | `8b2d75f8…bfc4` | 14/14 (2e) |
| CA-5b | calcul d'un actif, fragment, contrôle E-CA-23 côté lot | 173 (61) | 44 | `503e351f…65b5` | 14/14 (2e) |
| CA-5c | descriptifs (E-CA-20), queue (Q-CA-04) | 110 (55) | 47 | `9b55100e…09dd8` | 11/11 (2e) |
| CA-5d | écrivain synthétique six formats, lignes de valeurs, septembre | 126 (32) | 49 | `5913e14a…68d2` | 10/10 |
| CA-5e | point d'entrée du calcul, sorties, T-CA-DET-1 | 186 (53) | 52 | `cf3baa70…7f7d` | 12/12 (2e) |
| CA-6a | lancer.sh et ses tests (T-CA-LAN-1 à 6) | 186 (71) | 56 | `a52e5898…a922` | 14/14 (2e) |
| CA-6b | cadence.py (Q-CA-11 modifiée), hors du lanceur | 179 (93) | 58 | `1f458698…35a9` | 10/11, 1 équivalent |
| CA-6c | README, SHA256SUMS ; campagne transverse (site d'appel, source) et ses tests ; TMPDIR | 115 (89) | 59 | `59f81b58…f362` | 14/15, 1 équivalent |

Total : 2 977 lignes ajoutées (≈ 1 371 hors tests, données et README compris ; ≈ 1 606 de tests). Lot final : 29
fichiers sous `SHA256SUMS` ; `SHA256SUMS` du lot `a9967de0…b778` (sha256 du fichier). sha256 complets des diffs : `SHA256SUMS` du dossier.
Contrôles à chaque diff (outil `outils/cloture.py`) : 0 octet 92 dans les fichiers du lot, aucune ligne de plus de
120 caractères. Rejeu de la série entière sur une extraction neuve de `ebd1560` : état final identique à l'octet.

**Tête `1a388e1`** : le code (`scripts/calib-actifs/`) s'applique sans conflit. Seul le hunk `gates.yml` de **CA-0a**
échoue : son contexte est la dernière ligne du job `sim-bis-unittest` (`--plancher 194` à `ebd1560`, `210` à la tête ;
la tête a aussi ajouté deux lignes de commentaire SB-13 dans ce job et porté `s2bis` à 340). Le job neuf rajouté à la
main après le job sim-bis, les hunks `gates.yml` de CA-0b à CA-6c (la seule ligne `--plancher` du job neuf)
s'appliquent tous ; écart final avec ma copie : les seules lignes de la tête (340, SB-13, 210). Sur cette copie de la
tête : job neuf conforme (Ran = 59), runner 136 ok. Entrées du lot inchangées entre `ebd1560` et la tête
(`config_analyse.py`, `analyse.json`, `scripts/plan-s2bis`, `tau_sigma.txt`, SH : `git diff --stat` vide).

## 2. Exigences E-CA-01 à E-CA-33

| n° | tenue | où | test |
|---|---|---|---|
| E-CA-01 | tenue (sorties sous `docs/adr-0029/calib-actifs/` : au versement, hors lot) ; liste des chemins de chaque diff : `scripts/calib-actifs/**` et `gates.yml` seuls | lot entier ; README | contrôle des en-têtes de diff (rejeu) |
| E-CA-02 | tenue | socle.py:168 (épingle), :177 (bloc) | test_socle.test_epingle_tau_sigma, test_valeurs_btc |
| E-CA-03 | tenue | socle.py:43 ; lancer.sh l.26 ; acquerir.main ; tau.main ; cadence.main | test_socle.test_variable ; test_lancer ; test_pages.test_main ; test_cli.test_refus ; test_cadence |
| E-CA-04 | tenue ; JSON : clé `etiquette` (Q-CA3-3) ; manifeste : étiquette en 1re ligne, dates d'E-CA-13 | socle.py:19, :221 ; tau.main | test_fenetre.test_ecrire ; test_cli.test_succes ; test_acquerir.test_manifeste_reprise |
| E-CA-05 | tenue | `.partiel` : socle.ecrire, Manifeste.ajouter ; TMPDIR du lanceur | test_fenetre.test_ecrire ; test_lancer.test_succes |
| E-CA-06 | tenue | parametres.json `unites`, `classes` ; tau.fragment:112 | test_socle ; test_fragment.test_fragment_charge |
| E-CA-07, -08, -11 | hors lot (CB-7, CB-9) | — | — |
| E-CA-09, -10 | partiel : proxys et paramètres du §2.4 en parametres ; CA/chainlink = cohérence des planchers ; relecture au paquet hors lot (Q-CA3-7) | socle.oracles :207 | test_fenetre.test_oracles |
| E-CA-12 | tenue (source citée par bloc, non par ligne) | parametres.json `lectures`, `series` | test_socle |
| E-CA-13 | tenue | acquerir.py :58, :85, :131, :148, :166, :181 | test_acquerir ; test_pages |
| E-CA-14 | tenue | acquerir.kraken :131 ; `kraken_sha256` | test_kraken_plages ; test_kraken_sommes_de_sh (relit SH l.156-158) |
| E-CA-15 | tenue, resserrée (toutes les lignes de SH §4) | bougies.oracle_sh :145 ; tau.main | test_series.test_oracle, test_comptes_de_sh ; test_cli.test_refus |
| E-CA-16 | tenue | bougies.serie :93 | test_bougies |
| E-CA-17 | tenue | tau.calcul_actif :91 | test_fragment.test_site_exclusion |
| E-CA-18 | tenue | socle.quantile :231, regle :239 ; tau ; bougies (nombres JSON en chaînes) | test_regles ; test_tau ; test_bougies.test_colonnes |
| E-CA-19 | tenue | tau.places, agregateurs, ecarts ; sigma.sigmas | test_tau ; test_sigma |
| E-CA-20 | tenue | tau.descriptifs :174 | test_descriptifs.test_fragment_inchange |
| E-CA-21 | tenue | lancer.sh (A, B, cmp) | test_identite (3.10 à 3.13 × 0 et 1) ; test_lancer ; échelle A = B |
| E-CA-22 | tenue sauf README des sorties (au versement) | tau.main ; lancer.sh | test_cli ; test_fragment.test_fragment_charge |
| E-CA-23 | hors lot (RB-2) ; (a) à (h) rejoués côté lot (CA/fragment) | tau.controle_fragment :126 | test_fragment.test_controle_fragment ; test_cli (site d'appel) |
| E-CA-24 | tenue, refus ajoutés (Q-CA3-6) | socle.Refus :32 | tous |
| E-CA-25 | tenue par moi (aucune statistique sur historique) ; voir l'écart E-CA3-1 | — | — |
| E-CA-26 | tenue | outils/repetition.py | §5 |
| E-CA-27, -28, -29 | hors lot | README (procédure) | — |
| E-CA-30 | sans objet ici | — | — |
| E-CA-31 | tenue (rouge par squelette, §3) | tests/ | une mutation nommée par test |
| E-CA-32 | tenue | outils/mutants.py | FATAL CA1b-02 corrigé, campagne relancée |
| E-CA-33 | tenue pour calib-actifs (chaque diff), s2bis (255), s2-harness (415) ; sim-bis et plan-s2bis non lancés (extraction de `f35a70c`, Q-CA3-11) | — | §4 |

## 3. Tests T-CA-* et mutants M-CA-*

Tous les T-CA-* du §6.2 sont écrits (59 tests au total) : SOC-1, SOC-2, FEN-1 (fuseau local forcé à UTC+14),
FMT-1 à 3, SER-1 (décalé d'une minute pour montrer « indéfini avant »), TAU-1 à 3, Q-1, G-1 avec les deux vecteurs de
l'avis (borne basse exacte 1,5 × 1/3000 ; 1/3 % sous facteurs 1 et 1,5), AGR-1, ORA-1 (contre `TAU_ORACLES` et
`SIGMA_ORACLES` de config_analyse), SIG-1 à 3, ORX-1, KRA-1, FRG-1 (fragment chargé par `config_analyse.charger` ; la
partie « refus côté RB-2 » est rejouée côté lot par CA/fragment), DET-1, LAN-1 à 6. Vecteurs de Q-CA-13 :
`tests/vecteurs_regles.json` (9 quantiles, 12 règles), relus par `regles.py` hors du lot (`outils/croiser_regles.py`,
commun importé sans harnais, r1 de substitution recopié de `s2-harness/shogen_s2/r1.py` l.62-67, déclaré) : 21 égaux,
0 écart (`travail/croisement-regles.txt`) ; le passage du réviseur avec le contexte de `f35a70c` reste dû.
M-CA-01 à M-CA-29 : tous tués (M-CA-24 en trois mutants) ; 253 mutants dans les campagnes finales des 19 diffs, classés par la ligne du job
(borne 300 s), sous `isole.sh` à partir de la 3e campagne de CA-2a. Rouge : `outils/squelette.py` (corps des fonctions
publiques remplacés par `return None`) ; lanceur remplacé par `exit 0` pour CA-6a ; sorties dans `travail/rouge/`.
Vivants restants, équivalents : CA6b-02 (crochet `parse_float` de cadence.py : effet mémoire seul, les flottants sont de
toute façon filtrés par `type is int`) ; CA6c-05 (nom de fenêtre forcé pour Kraken : rendu inatteignable par la règle de
cohérence « archive hors de septembre », elle-même tuée par CA6c-13). Vivants des premiers passages corrigés par un test
ajouté, campagne relancée : 28 ; FATAL : 2 (CA1b-02, boucle infinie de `mois()`, corrigé par une boucle bornée ; CA2a-12,
voir E-CA3-1).

## 4. Matrice de vérification (état final)

| contrôle | résultat |
|---|---|
| job `calib-actifs-unittest`, ligne telle qu'écrite, python3.10 à 3.13, PYTHONDEVMODE=1, PYTHONWARNINGS=error, isolé | sortie 0, Ran = 59, 0 ligne « Exception ignored » ou « Warning » (×4) |
| runner `enforcement/tests/run-fixtures-verdict-suite-s2.py` | 136 ok, 0 échec (copie finale et copie de la tête) |
| job s2bis (`--plancher 255`, base) | conforme, Ran = 255 |
| job S2 (s2-harness, `--egal`, PLANCHER 415) | conforme, Ran = 415, sauts nommant la variable |
| job sim-bis | non lancé : ses tests extraient `f35a70c` par `git archive` (oracle_r1.py l.46), interdit ici ; fichiers non touchés |
| hook pre-commit (copie indexée jetable) | OK, aucune étape en refus |
| gate des secrets (indexé et `--tree`) | OK, 965 fichiers |
| `cargo --locked --offline xtask verify` (copie indexée) | 10 lignes VERDICT identiques à celles de la base `ebd1560` ; 1 ROUGE, le 9e (S-G9 par l'ordre des gates, présumé), motif `docs/17-modele-de-menace.md:70` présent une fois dans chaque sortie (connu sur copie) ; 5e verdict VERT (S-G5 présumé par l'ordre) |
| cas K du runner pour le job neuf | absent (hors liste fermée) : Q-CA3-11 |

## 5. Répétition à l'échelle (E-CA-26)

Bougies synthétiques, fenêtre réelle (131 040 minutes), lecture A (ETH 6 places, USDC 4, USDT 6), septembre (43 200
minutes, sans kraken) ; 102 227 907 octets de bruts aux six formats ; tau_sigma synthétique ; comptes de l'oracle de
SH §4 recalculés hors du code du lot. `tau.py` (code final, PYTHONHASHSEED 0) : **code 0, 86,1 s murales, mémoire
maximale 838 600 Kio** ; passe à PYTHONHASHSEED 1 (code précédant le seul changement d'impression de CA-6c) : sorties
égales à l'octet. Machine **chargée** : 4 cœurs partagés avec un rendu Blender et une relecture G2 (charge 2,2 au
lancement, 3,1 à la fin). Hors campagne de mutants ; un seul processus lourd (PID consignés dans NOTES.md). Copies
supprimées.

## 6. Questions Q-CA3-n (mon choix, et sa raison ; aucune valeur scellée tranchée)

- **Q-CA3-1 taille** : ≤ 200 lignes ajoutées par diff, tests, données et `gates.yml` compris (lecture la plus stricte du
  brief et du §6.1) ; d'où 19 diffs au lieu de 7.
- **Q-CA3-2 champ de mode** : clé `modes` au premier niveau du fragment ; `config_analyse` n'a pas encore ce champ
  (schéma de RB-2, E-CA-23 b) ; T-CA-FRG-1 charge `tau_sigma` et `unites` seuls.
- **Q-CA3-3 étiquette du JSON** : clé `etiquette` (premier des champs triés) pour garder un JSON valide.
- **Q-CA3-4 σ_BTC non entier** : arrondi à la seconde supérieure (σ entier exigé par config ; garde σ ≥ σ_BTC).
- **Q-CA3-5 CA/borne** : le refus ne porte pas la valeur de la règle (lettre du §5.7), à la différence de BTC (l.181,
  valeur imprimée) ; à trancher.
- **Q-CA3-6 refus ajoutés** (serrage) : CA/parametres, CA/fragment, CA/calcul (exception nommée par son type), CA/usage
  des scripts ; CA/format aussi pour « aucun fichier acquis ».
- **Q-CA3-7 CA/chainlink** : cohérence des seuils et heartbeats du §2.4 avec les planchers attendus (config l.28-29) ;
  la relecture datée des paramètres on-chain (E-CA-10) reste au paquet.
- **Q-CA3-8 formes d'API non vérifiées sur pièce** [abs] : Coinbase `start`/`end` en ISO 8601, fin incluse ; Bitstamp
  `start`, `end` et `limit` ; Bitfinex `end` en ms inclus ; mensuels d'OKX supposés alignés sur le mois UTC (sinon
  CA/format, échec fermé). À établir avant l'épinglage par une page citée ou une capture (horodatages seuls).
- **Q-CA3-9 Kraken** : membre cherché par nom de base dans l'archive (sous-dossier admis), unique sinon CA/kraken.
- **Q-CA3-10 réseau du lanceur** : l'étape réseau garde les seules variables de mandataire et de certificats présentes
  (`HTTPS_PROXY`, `HTTP_PROXY`, `NO_PROXY` et minuscules, `SSL_CERT_FILE`, `SSL_CERT_DIR`) ; le calcul, non.
- **Q-CA3-11 CI** : patron des jobs appliqué ; aucun cas K du runner ne lit le job neuf (le runner est hors liste
  fermée) ; sim-bis et plan-s2bis non lancés ici (extraction de `f35a70c`).
- **Q-CA3-12 constat, exclusion de Q-CA-04** : σ contient le troisième terme pris sur les mêmes cellules ; l'exclusion
  « 60·âge > σ » ne touche donc que des cellules d'âge > 3 × P99 (au plus la queue au-delà du P99 de coinbase).
- **Q-CA3-13 septembre** : USDC sans kraken a trois places, sous N_min = 4 : refus imprimé, descriptif ; N_min de la
  variante non changé.
- **Q-CA3-14** : strate d'une suite = strate de sa dernière minute (P99 des suites, descriptif).
- **Q-CA3-15** : quantile et règle de grille réimplémentés dans `socle.py` (évite un cycle sigma/tau).
- **Q-CA3-16** : les tests relisent `SOURCES-HISTORIQUES.md` (sommes de Kraken, comptes de SH §4) et importent
  `config_analyse` (lecture seule) : la suite dépend de ces deux pièces.
- **Q-CA3-17** : README des sorties (E-CA-22) laissé au versement ; manifeste daté (E-CA-13) bien qu'E-CA-04 exclue les
  heures des valeurs des autres sorties.

## 7. Écarts (déclarés)

- **E-CA3-1 (grave) : accès réseau réel non voulu.** L'environnement porte `HTTPS_PROXY=127.0.0.1:36573` ; la garde
  réseau des tests (forme de `s2bis/tests/__init__.py`) admet la boucle locale, donc toute requête `urllib` passait par
  le mandataire. Sous le mutant CA2a-12 (garde de la variable retirée), `test_main` a lancé `acquerir.main` sur les VRAIS
  paramètres (sans `--parametres`), pauses neutralisées : téléchargements réels sans débit borné, deux fois (campagne,
  borne de 300 s ; reproduction à la main, 60 s), puis un **processus orphelin** (PID 23006, AMORCE du vérificateur,
  ppid 1) a continué après le délai jusqu'à 07:29 UTC. Comptes lus dans la seule colonne URL des manifestes (aucun
  fichier de données ouvert) : `tmp/ca_acq_rxbr4e4t` 784 lignes (coinbase 436, bitstamp 281, bitfinex 41, binance 9,
  okx 3, kraken 2, local 12 ; 88 248 610 octets), puis 203 lignes de l'orphelin (bitstamp 82, coinbase 121 ;
  12 320 347 octets) ; `tmp/ca_acq_7v5w0mbg` 70 lignes (18 336 611 octets). Tout supprimé. Aucune statistique calculée.
  Le 1er passage de la campagne de CA-2a (CA2a-12 « tué ») a pu toucher le réseau de même. Observation non probante,
  issue de l'écart : les lignes de manifeste de kraken n'existent que si la somme de SH était égale. Remèdes : la garde
  des tests retire les variables de mandataire (et un test le vérifie) ; le cas « variable posée » passe ses propres
  paramètres ; campagnes et suites sous `isole.sh` ; `outils/mutants.py` tue le groupe de processus au dépassement.
- **E-CA3-2** : barres obliques inverses tapées dans quelques commandes (motifs `sed`, `chr` en heredoc Python, une
  continuation de ligne dans un test ensuite retirée), contre la consigne B.16 ; contrôle sur les octets écrits : 0
  octet 92 dans les fichiers du lot à chaque diff ; motifs de mutants vérifiés par compte exact (sinon INVALIDE).
- **E-CA3-3** : `git init` et `git add` dans des copies jetables du scratchpad (aucun commit) pour exécuter le hook, la
  gate des secrets et `xtask` ; `--offline` ajouté à `cargo --locked xtask verify`.
- **E-CA3-4** : campagnes de CA-0a à CA-1c et les deux premières de CA-2a lancées sans `isole.sh` (aucun chemin réseau
  avant CA-2a).
- **E-CA3-5** : le rouge est montré par squelette (corps remplacés), non par une version antérieure du code.
- **E-CA3-6** : retouches de docstrings ou de fin de fichier après certaines campagnes, sans relance (aucun effet sur le
  comportement) ; la campagne de CA-6c a été relancée après l'ajout de TMPDIR.
- **E-CA3-7** : sim-bis et plan-s2bis non lancés (extraction de `f35a70c`).

## 8. Items à former (règle PAROXYSME)

- **SHOGEN-TESTS-GARDE-MANDATAIRE-1** : la garde réseau des tests admet la boucle locale ; un mandataire local
  (`HTTPS_PROXY`) la contourne ; `s2bis/tests/__init__.py` a la même forme. Construction : retirer les variables de
  mandataire à la garde, test dédié ; déclencheur : prochain lot touchant `s2bis/tests`.
- **SHOGEN-MUTANTS-ORPHELINS-1** : un délai de campagne qui ne tue que l'enfant direct laisse vivre la suite ;
  construction : groupe de processus et `killpg` dans les outils de campagne (G2 compris).
- **SHOGEN-CALIB-FORMES-API-1** : formes de requête de Coinbase, Bitstamp, Bitfinex et bornes des mensuels d'OKX
  [abs] (Q-CA3-8) ; à établir avant l'épinglage.
- **SHOGEN-CI-CABLAGE-CALIB-1** : cas K du runner pour `calib-actifs-unittest`.
- **SHOGEN-S2BIS-P1-ESTIMATION-1** (existant) : CALIB-ACTIFS mesuré à ≈ 2 977 lignes ajoutées (≈ 1 371 hors tests)
  contre ≈ 1 100 à 1 300 estimées, en 19 diffs.

## 9. Estimation révisée

Code CA-0 à CA-6 : fait (2 977 lignes). Restent : G2 neuve à 100 % (≈ 2 à 3 h), corrections, commits par l'orchestrateur
(19 diffs ; recalage du seul hunk `gates.yml` de CA-0a sur la tête) ; RB-2 (E-CA-23 et schéma du mode) ; formes d'API
(Q-CA3-8) ; épinglage ; lancement unique (≈ 1 h de réseau, ≈ 2 à 3 min de calcul par passe d'après la répétition).

## 10. Provenance

Lectures [lu] listées en tête ; recomptes : dates par `date -u -d` ; sommes par `sha256sum` ; comptes de SH relus par
les tests ; croisement Q-CA-13 par `regles.py`. Outils (hors lot, `outils/`) : squelette, mutants, cloture, plie,
verts, croiser_regles, repetition. Pièces : `travail/mutants/*.json|tsv`, `travail/rouge/*.txt`,
`travail/croisement-regles.txt`, `travail/batterie-*.txt`, `travail/xtask*-verdicts.txt`, `travail/repetition*.out`,
`travail/snap/` (instantanés). Non ouverts : `tau_sigma.txt`, tout `*.jsonl`, les dossiers interdits, les pièces de D.2,
les fichiers téléchargés par l'écart E-CA3-1 ; sortie brute de `xtask` non lue (lignes VERDICT et un compte de motif).
`SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée hors des tests prévus. Rien sur Pocket. Aucune clé ni secret.

## 11. Correction après la G2 (correcteur G1 neuf, 2026-10-09, 09:21 à 09:57 UTC, `date -u`)

- **Gate 0** : modèle résolu `claude-opus-5-5` (identifiant donné par l'environnement), rôle correcteur (worker G1) ;
  effort non vérifiable depuis la session. Contrat : `ADJUDICATION-G2.md` (C-1 à C-13), `g2/RAPPORT-G2.md`, `g2/NOTES.md`,
  `g2/outils/`, ce rapport, `NOTES.md`, `BRIEF-CA.md`, lus en entier. `sha256sum -c` : `SHA256SUMS` 129/129,
  `g2/SHA256SUMS` 61/61. Base `ebd1560` ; tête du dépôt `1a388e1`, inchangée ; dépôt lu seulement, aucune écriture git.
- **Réseau** : tout passe par `outils/run_corr.sh` (copie de `g2/outils/run.sh` : `env -u` des huit variables, `isole.sh`,
  TMPDIR `tmp/corr`). Sonde à 09:22 : 1.1.1.1:443 et 8.8.8.8:53 errno 101, `urlopen` refusé, mandataire 127.0.0.1:36573
  errno 111 dans l'espace isolé (joint hors isolement : la sonde discrimine). Bornes par `killpg` ; `ps` de fin : rien.

### 11.1 Diff neuf CA-6d (CA-0a à CA-6c inchangés, octet pour octet)

| diff | objet | lignes ajoutées (hors tests) | plancher | sha256 |
|---|---|---|---|---|
| CA-6d | corrections C-1 à C-11 et C-13 de la G2 ; README ; `SHA256SUMS` du lot | 188 (32) | 64 | `00101674…8854` |

Choix à adjuger (E-COR-2) : CA-6c n'a que 85 lignes de marge ; placer chaque correction dans son diff d'origine
réécrirait dix diffs et leurs planchers et rendrait caduques leurs campagnes ; un diff de correction borne la relecture.
Série : 20 diffs, 3 165 lignes ajoutées. `SHA256SUMS` du lot : sha256 `485a82fe…4ea6`. Renvois `fichier:ligne` du §2 :
état CA-6c ; après CA-6d (corrigé au §12, O-CC-3), `socle.py` +1 à partir de l'ancienne l.40 (ligne insérée après
l'ancienne l.39) ; `tau.py` +1 pour les anciennes l.67 à 85, +2 pour les l.86 à 266, +4 à partir de la l.267.

### 11.2 Corrections

| C | fait | preuve (mutant classé par la ligne du job, plancher 64) |
|---|---|---|
| C-1 | `test_tau.test_agregateurs_suite` : τ_ph 0,0050 > τ_sh 0,0045, τ_agr 0,0055 ; `synthetiques.BTC_PH`, `test_planchers_seuls` sous les deux blocs | G01 TUE ; G02 (au §4 du réviseur) et M-CA-15 (forme N01) TUE |
| C-2 | `test_sigma.test_maximum_des_strates` : P99 2 et 7, terme 1 260 s dans les deux ordres | G14 TUE ; N03, N04 TUE |
| C-3 | `test_pages.test_garde_reseau` : sous-processus à quatre mandataires fictifs, `getproxies()` sans http, https, all ; `test_cadence.test_cli_hors_lanceur` sur paramètres et serveur locaux, `tests.TENTATIVES` inchangé | G11 TUE sous `env -u` (aucun mandataire) ; K-CAD (garde de `cadence.main` retirée) TUE par les codes, aucune tentative ; N05, N06 TUE |
| C-4 | `test_identite` : `sys.executable` et chaque `python3.1x` présent, × graines 0 et 1 ; README | PATH simulé : CA-6c rouge (`None unexpectedly found in [None, None, None, None]`), CA-6d vert Ran 64 ; M-CA-23 et N07 TUE sous ce PATH ; N22 TUE |
| C-5 | `test_oracle` : minute active hors de la semaine (9) | G07 TUE ; N08, N23 TUE |
| C-6 | `test_comptes_de_sh` : tableau de SH §4 lu ligne à ligne (classe, jeu de places, colonnes) ; phrase des actives lue place par place | G29, G30 TUE ; N09, N10 TUE |
| C-7 | `test_pages.test_main` : noms `page-1790811000.json` de la descriptive et URL de fin 1790812740 | G08 TUE ; N11, N24 TUE |
| C-8 | `test_fragment.test_borne_basse_et_variante` : écarts nuls, τ des places 0,0005, τ_agr 0,0030 | G23 TUE ; N12, N25 TUE |
| C-9 | `test_fenetre.test_oracles` : seuil relu différent ; `test_agregateurs_suite` : τ de BTC nul par classe | G12, G13 TUE ; N13, N14 TUE |
| C-10 | `cadence.releve` capte `TypeError` ; `test_cadence.test_corps_hors_forme` : corps `[]` et `"x"`, BTC propre à chaque agrégateur | rouge avant code (`['TypeError', 'TypeError'] != [({}, 2), ({}, 2)]`) ; G28 (suivi sur le tuple corrigé) et G10 TUE ; N15, N16 TUE |
| C-11 | même test : lecture A-prime, USDC à N_min 3, 15 cellules par strate | G27 TUE ; N17, N26 TUE |
| C-12 | §1 : CA-5e `cf3baa70…7f7d` (`sha256sum`) ; §2 E-CA-04 : `socle.py:19` (`sed -n 19p` : `ETIQUETTE`) | relu |
| C-13 | `Refus(valeur=(nom, valeur))` hors du message ; `tau.main` écrit, après le refus, `descriptif hors refus (jamais décisif) : valeur calculée de la règle, <nom> : <v> ; <lieu>` ; JSON inchangé ; README | rouge avant code (4 FAIL d'assertion) ; N18 à N21 TUE |

Campagne finale (`outils/mutants_corr.py`, PAR 2, borne 300 s, `killpg`) : 42 mutants, **41 TUE, 1 VIVANT (G26,
équivalent admis), 0 FATAL, 0 INVALIDE** ; chaque test neuf ou changé rougit par FAIL d'assertion sous son mutant.

### 11.3 Contrôles

- Rejeu des 20 diffs sur une extraction neuve de `ebd1560` : 20/20 code 0, Ran = plancher (3 … 59, 64) ; état final =
  `travail/snap/CA-6d`. Forme : 0 octet 92 (lot, diff), aucune ligne > 120, aucun `TODO`, `FIXME`, `XXX`.
- Matrice 3.10 à 3.13, `-X dev -W error`, `PYTHONDEVMODE=1`, `PYTHONWARNINGS=error` : 4 × code 0, Ran 64, 0 « Exception
  ignored », 0 « Warning » (série sur la base et tête).
- **Tête** : `diffs-tete/` (20 diffs exacts sur `1a388e1` ; seul écart de contenu : contexte `--plancher 210` de CA-0a ;
  sha256 `5ecf4078…b372` pour CA-0a, `8a3b1c7a…82c2` pour CA-6d) ; `patch -p1` sur une tête neuve : 20/20, 0 décalage,
  0 fuzz ; lot égal à celui de la série. Batterie : job neuf Ran 64, runner 136 ok, s2bis Ran 340, S2 Ran 415 (sauts
  nommant la variable), tous conformes ; hook et gate des secrets (index et `--tree`) OK sur une copie indexée jetable.
  Série sur la base : runner 136, s2bis 255, S2 415. `xtask` (lignes VERDICT seules) : base, série, tête, tête + série :
  10 lignes identiques, 9e ROUGE (`docs/17:70`, connu sur copie), 5e VERTE.
- **sim-bis non lancé** (E-COR-3) : ses tests extraient `f35a70c` par git, interdit dur du brief ; aucun de ses fichiers
  ni de ses entrées n'est touché (chemins de CA-6d).

### 11.4 Lignes d'items (constat ; propriétaire ; déclencheur ; prix ; origine)

- **SHOGEN-S2BIS-CALIB-SIGMA-ARRONDI-1** : le lot arrondit σ_BTC à la seconde supérieure (`sigma.py` l.64, contrôle
  (e) côté lot `tau.py` l.134) ; E-CA-23 (e) exige σ_agr(actif) = σ_agr(BTC) : un σ de BTC versé non arrondi de même
  fait refuser (e) ; lot RB-2 ; G0 de RB-2 ; une règle écrite (σ BTC versé = ⌈σ_BTC⌉) et un test (e) sous σ_BTC non
  entier, ≈ 10 lignes ; G2 O-2, Q-CA3-4.
- **SHOGEN-CALIB-FORMES-API-1** : sens inclus ou exclu de `end` (Coinbase, Bitstamp, Bitfinex), `limit` de Bitstamp,
  alignement UTC des mensuels d'OKX non établis sur pièce [abs] ; une fin exclue perdrait une minute par page, lue « sans
  échange », sans refus ; orchestrateur, lot d'épinglage ; condition de l'épinglage (E-CA-27) ; une page citée datée ou
  une capture (horodatages seuls) par place, et le cas échéant `fin` de page corrigée avec son test ; Q-CA3-8, G2 O-7.
- **Schéma de RB-2 (O-8)** : clé `etiquette` à retirer et clé `modes` à faire entrer au schéma d'`analyse.json` (E-CA-23
  b) ; volet de l'item de RB-2 qui porte E-CA-23 ; je ne l'ai pas cherché (annexe B lue par nom seulement) : à défaut,
  item neuf **SHOGEN-S2BIS-RB2-SCHEMA-MODES-1** ; lot RB-2 ; G0 de RB-2 ; ≈ 15 lignes et un test de chargement ; G2 O-8.
- **O-6** (sha256 du manifeste daté en tête de `calib_actifs.txt`) : pas d'item. Raison : le manifeste est versé avec
  les sorties ; son sha256 lie la sortie à ce manifeste, et un tiers vérifie ses colonnes URL, taille, sha256, sans date,
  contre son propre téléchargement. Phrase au README des sorties, déjà dû au versement (Q-CA3-17).
- **O-3** (septembre, USDC à trois places sous N_min 4) : pas d'item. Raison : septembre est descriptif (E-CA-20), le
  refus imprimé est lui-même l'information ; la lettre de §4.3 pt 1 (N_min 3) est une limite à écrire au paquet.
- **SHOGEN-TESTS-GARDE-MANDATAIRE-1** : la garde réseau des tests admet la boucle locale ; un mandataire local la
  contourne (cause d'E-CA3-1) ; `s2bis/tests/__init__.py` à la tête (`4e692df`) : aucune purge (0 mention de proxy) ;
  prochain lot qui touche `s2bis/tests/` ; au plus tard le gel du collecteur ; purge et test indépendant de
  l'environnement (forme de C-3), ≈ 15 lignes ; E-CA3-1, G2 §9.
- **SHOGEN-MUTANTS-ORPHELINS-1** : un délai qui ne tue que l'enfant direct laisse vivre la suite (orphelin d'E-CA3-1) ;
  orchestrateur, gabarits de campagne (ADR-0028 annexe B, B.16) ; prochain brief qui porte une campagne ;
  `start_new_session`, `killpg` et relevé `ps` de fin, deux phrases au gabarit ; E-CA3-1, G2 §9.
- **SHOGEN-CI-CABLAGE-CALIB-1** : aucun cas K du runner ne lit le job `calib-actifs-unittest` ; un plancher oublié ou un
  saut admis n'y serait pas vu par le runner ; lot qui touche `enforcement/tests/` ; avant ou au commit du job ; un cas K
  et ses fixtures, ≈ 20 lignes ; Q-CA3-11, G2 §9 (interpréteurs : réglés par C-4).
- **SHOGEN-S2BIS-P1-ESTIMATION-1** (volet) : CALIB-ACTIFS mesuré à 3 165 lignes ajoutées en 20 diffs (2 977 + 188 de
  correction) ; G2 ≈ 30 min, correction ≈ 36 min.

### 11.5 Écarts du correcteur

- **E-COR-1** (B.16) : barres obliques inverses tapées dans des commandes d'aide (chaînes Python d'un heredoc pour des
  remplacements, un motif `grep` de contrôle, un échappement hexadécimal de guillemet dans un premier jet de `mutants_corr.py`, retiré) ; contrôle sur
  les octets : 0 octet 92 dans le lot, CA-6d, `diffs-tete/` et les outils écrits ; chaque remplacement compté (= 1).
- **E-COR-2** : diff neuf CA-6d au lieu de corrections dans les diffs d'origine (raison au §11.1), à adjuger.
- **E-COR-3** : sim-bis non lancé, contre la liste de l'adjudication, par l'interdit dur du brief (`f35a70c`).
- **E-COR-4** : `git init` et `git add` dans une copie jetable pour le hook et la gate des secrets (forme d'E-CA3-3) ;
  un `grep -rn` sur `scripts/sim-bis/` de ma copie (un dossier, ni `docs/`, ni le dépôt, ni le scratchpad entier).
- Limites : `test_borne_valeur` compare la ligne au calcul direct (site d'appel) ; la valeur indépendante est dans
  `test_places` (0,0300) et `test_agregateurs_suite` (0,0530). L'identité inter-versions repose en CI sur les seuls
  interpréteurs présents ; la matrice 3.10 à 3.13 reste une étape écrite du G3 opérant et de la G2. O-13 non touché
  (`test_comptes_de_sh` lit toujours SH par position, échec fermé).

Provenance : `NOTES.md` (section du 2026-10-09, 09:21) ; `travail/corr/` (rouge, vert, PATH simulé, campagnes, rejeu,
batteries, matrices, hook, secrets, xtask) ; outils `outils/run_corr.sh`, `sonde_mandataire.py`, `mutants_corr.py`,
`cloture_corr.py`, `par_diff_corr.sh`, `matrice_corr.sh`, `batterie_corr.sh`, `serie_tete.py`, `xtask_corr.sh`.
Processus lourds un à la fois, PID consignés ; copies lourdes supprimées. `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée ;
aucune clé ni secret ; rien sur Pocket.

## 12. Passe CA-6e (R-2 du contre-contrôle, mutant X09 ; 2026-10-09, 10:20 à 10:31 UTC, `date -u`)

- **Gate 0** : modèle résolu `claude-opus-5-5` (identifiant donné par l'environnement), rôle correcteur (worker G1).
  Lus : `g2/cc/RAPPORT-CC.md` en entier, `g2/cc/SHA256SUMS` (`sha256sum -c` : 88/88 OK), l'ajout daté de
  `ADJUDICATION-G2.md` (après 10:20 UTC). Rien écrit sous `g2/`. Dépôt réel lu seulement ; HEAD `1a388e1`.
- **Réseau** : sonde à 10:20 sous `outils/run_corr.sh` : 1.1.1.1 et 8.8.8.8 errno 101, `urlopen` refusé, mandataire
  127.0.0.1:36573 errno 111 (joint hors isolement). Tout passe par `run_corr.sh` ; `killpg` ; `ps` de fin vide.

| diff | objet | lignes ajoutées (hors tests) | plancher | sha256 |
|---|---|---|---|---|
| CA-6e | `test_series.test_oracle` : binance active aussi en minute −1 (`T0` − 60 s, avant la semaine de l'oracle) ; `SHA256SUMS` du lot | 3 (1) | 64 | `21413440…0636` |

- **Rouge ciblé** : sur CA-6d, X09 (`socle.minutes(dict(o, debut=o["debut"] - 600))`, `g2/cc/outils/mutants_cc.py`
  l.71) et Y01 (une minute plus tôt) VIVANTS ; sur CA-6e, X09 TUE par un FAIL d'assertion de `test_oracle` (binance
  compte 4 minutes actives contre 3) ; sans mutant : vert, Ran 64. La minute 9 (après la semaine) reste : G07 tué.
- **Campagne CA-6e** (`outils/mutants_corr.py`, ligne du job, plancher 64, PAR 2, borne 300 s, `killpg`) : G00 témoin
  VIVANT ; **X09, Y01, Y02 (range ouverte une minute plus tôt), G07, N08, N23 : 6 TUE**, tous par FAIL `test_oracle` ;
  0 FATAL, 0 INVALIDE.
- **Série** : 21 diffs, 3 168 lignes ajoutées ; rejeu sur une extraction neuve de `ebd1560` : 21/21 code 0, Ran =
  plancher ; état final = `travail/snap/CA-6e`. `SHA256SUMS` du lot recalculé (seule la ligne de `test_series.py`).
  Forme : 0 octet 92, aucune ligne > 120, aucun `TODO`, `FIXME`, `XXX`.
- **Matrice** 3.10 à 3.13, `-X dev -W error`, `PYTHONDEVMODE=1`, `PYTHONWARNINGS=error` : 4 × code 0, Ran 64, 0
  « Exception ignored », 0 « Warning », sur la série et sur la tête.
- **Tête** : `diffs-tete/CA-6e.diff` = `diffs/CA-6e.diff` (aucun hunk de `gates.yml`) ; les 20 autres `diffs-tete/`
  inchangés à l'octet ; `patch -p1` sur une tête neuve : 21/21, 0 décalage, 0 fuzz ; lot = `snap/CA-6e`. Batterie :
  job neuf Ran 64, runner 136 ok, s2bis Ran 340, S2 Ran 415, conformes ; hook et gate des secrets OK (copie indexée
  jetable). `xtask` (lignes VERDICT seules) : base, série, tête, tête + série : 10 lignes identiques à la passe du §11.
- **O-CC-3** : renvois du §11.1 corrigés (décalages relevés par `difflib` entre `snap/CA-6c` et `snap/CA-6d`) ; CA-6e ne
  touche ni `socle.py` ni `tau.py`. R-1 (lignes d'items) : retouches faites par l'orchestrateur au versement, non
  reprises ici. O-CC-2 : item SHOGEN-CALIB-BORNE-MULTI-1 posé par l'orchestrateur.
- **Écart E-COR-5** (B.16) : barres obliques inverses tapées dans les chaînes Python de deux commandes d'aide ; effet
  contrôlé : 0 octet 92 dans `test_series.py`, CA-6e, le rapport et les outils ; chaque remplacement compté (= 1).
- Provenance : `NOTES.md` (passe du 10:20) ; `travail/corr/` : `x09_avant_ca6e.tsv`, `vert_ca6e.out`,
  `mutants_ca6e.{tsv,log}`, `par_diff_base_CA-6e.out`, `matrice_serie6e_*`, `matrice_tete6e_*`, `batterie_tete6e*`,
  `xtask6e.log`, `xtask-*6e-verdicts.txt`, `hook6e.out`, `secrets6e.out`. PID : batterie 11156, xtask 16027.
