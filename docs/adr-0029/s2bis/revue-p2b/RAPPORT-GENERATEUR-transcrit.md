# Rapport du générateur de P2B, avec la section datée des corrections (transcrit)

> Transcription par l'orchestrateur le 2026-10-09 06:28:34 UTC du fichier RAPPORT-GENERATEUR.md ; contrôle FM-1.1 des quatorze transcripts d'agents qui ont touché `s2bis/p2a` ou `s2bis/p2b` : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Rapport du générateur — lot P2B (CB-15 têtes, export, RFC 3161 ; CB-17 commande `status`)

**Gate 0 : `claude-opus-5-5`** (identifiant exact du modèle qui tourne), effort max, worker G1.

> Ajout du 2026-10-09 (03:36 UTC) : les §1 à §9 rendent la phase 1 (base 5cfe746) ; ses diffs sont désormais dans
> `p2b/diffs-v1-5cfe746/`. La correction de la G2 (base c58b997, `p2b/diffs/`) et la variante sur P2A
> (`p2b/diffs-apres-p2a/`) sont au §10.

- Horloge (`date -u`) : ouverture 2026-10-08 18:45:30 UTC ; rapport écrit à 21:01:52 UTC.
- Brief : `<scratchpad>/s2bis/p2b/BRIEF-P2B.md`, sha256
  `0cc6ffe1a824e501dbafa90990bac59207a4b0fe6e28764c00fe4015b565cd27`.
- Base des diffs : `5cfe74680822e5eb0f71c41aabbeb3f6870e0df9` (= 5cfe746 du brief), tête du dépôt réel à l'ouverture
  et à 20:08:56 UTC ; copie par `git archive 5cfe746` avec les sept exclusions du brief (vérifiées absentes). Aucune
  opération git en écriture, aucun verrou. **La tête a avancé pendant le lot** (commits de l'orchestrateur, comme le
  brief l'annonçait) : à 20:59:30 UTC, `5e386c40da8e9d2dc16823be94805e1222c9c1d5` (8 commits SIM-BIS SB-15A à G et
  SIM-INTEG), arbre propre. Parmi mes fichiers, ces commits ne touchent que la ligne sim-bis de `gates.yml`
  (plancher 172 → 194) ; `s2bis/` et `enforcement/` inchangés. Les dix diffs s'appliquent aussi sur `5e386c4`
  (`git apply --whitespace=error-all`, 0 rejet ; fichiers obtenus identiques à l'état final, hors cette ligne).
- Rattachement (G0) : G0 `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md` (PROPOSITION corrigée par l'AVIS,
  qui prime) ; PROPOSITION l.223 (CB-15), l.225 (CB-17) ; E-C-35, E-C-36, E-C-38 (et E-C-26 : jugement dans
  `status`) ; AVIS Q-D-03, points 1 à 3 ; ADR-0029 l.218, l.240, l.244, §2.3.

## 1. Livrables

Dossier : `<scratchpad>/s2bis/p2b/diffs/`, dix diffs à appliquer **dans l'ordre des numéros** sur 5cfe746 (`patch -p1`
ou `git apply`), vérifiés en série par `travail/outils/serie.sh` (deux extractions neuves de la base : `patch -p1 -F0`
et `git apply --whitespace=error-all`, état comparé fichier par fichier après chaque diff : 0 écart).

| # | diff | objet | code | docs | retirées | plancher | sha256 |
|---|---|---|---|---|---|---|---|
| 1 | `01-CB-15a.diff` | requête RFC 3161, statut d'une réponse, manifeste | 179 | 47 | 1 | 262 | `f46f85e992abe014…` |
| 2 | `02-CB-15b.diff` | fichiers de tête, export atomique, lecture stricte du dépôt | 198 | 38 | 4 | 266 | `46d5155ebd59f4a6…` |
| 3 | `03-CB-15c.diff` | enregistrement `tetes` et export dans la boucle, `--depot`, nom d'observateur | 97 | 36 | 20 | 270 | `af96ab4d93d4ca46…` |
| 4 | `04-CB-15d.diff` | jeton du jour, `.tsr` conservé et journalisé | 115 | 32 | 19 | 272 | `4cb588cefb8ea7bf…` |
| 5 | `05-CB-15e.diff` | envoi HTTPS armé par `--envoi`, commande `jeton` | 120 | 31 | 7 | 274 | `5b0089e4dcc1f4d9…` |
| 6 | `06-CB-17a.diff` | `status` : lecture du journal, jugement d'une santé | 192 | 44 | 1 | 279 | `397851ca28f7c5de…` |
| 7 | `07-CB-17b.diff` | `status` : état par fenêtre, rapport, strates, commande | 183 | 37 | 6 | 284 | `04d95d4941f778a0…` |
| 8 | `08-CB-17c.diff` | résumés par jour, liste blanche, commande `resume` | 95 | 29 | 13 | 286 | `50f8bab37168bfcf…` |
| 9 | `09-CB-17d.diff` | compte à quorum sur les résumés des autres | 140 | 36 | 16 | 289 | `81146d0ed3978e8c…` |
| 10 | `10-CB-15f.diff` | dépôt : fichiers ordinaires seuls sans attente, aucun lien suivi, dépôt illisible | 141 | 45 | 19 | 294 | `66acdec842e5df6e…` |

« code » : lignes ajoutées hors `docs/` (code et tests, R-25 ≤ 200) ; « docs » : FORMAT et METRIQUES. Plancher : ligne
s2bis de `gates.yml`, `--egal`, relevé au compte mesuré de chaque état. Fichiers touchés :
`s2bis/shogen_s2bis/collecte/tetes.py` (neuf), `status.py` (neuf), `boucle.py`, `entree.py` ;
`s2bis/tests/test_tetes.py`, `test_status.py` (neufs) ; `.github/workflows/gates.yml` (plancher seul) ;
`docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md` (§2, §11.5, §14.1, §14.3, §15 neuf, §16 neuf) ;
`docs/adr-0029/s2bis/METRIQUES-S2BIS.md` (une section par diff, forme de P1).

Ce que fait le code (détail : FORMAT §15 et §16) :
- **CB-15a** : requête RFC 3161 (`TimeStampReq`, DER, bibliothèque standard) égale aux octets d'`openssl ts -query
  -sha256 -cert -no_nonce` et, avec nonce, aux octets d'OpenSSL pour son nonce ; statut d'une réponse (PKIStatus,
  jeton présent si et seulement si 0 ou 1, longueurs DER minimales) ; manifeste canonique des têtes.
- **CB-15b** : fichier de tête `<observateur>-<journal>.tete`, export atomique qui ne lève jamais (échec noté) ;
  lecture stricte du dépôt (16 têtes, 1 024 octets au plus, refus `TETES/…`), toute valeur admise par l'écrivain.
- **CB-15c** : enregistrement `tetes` dans la fenêtre qui clôt l'heure (avant `sante`), export de la tête du point
  après le marqueur ; `pool --depot` ; nom d'observateur `[A-Za-z0-9]{1,16}`.
- **CB-15d** : jeton du jour (AVIS Q-D-03 pt 1) : manifeste (au moins une tête propre) et requête écrits au dépôt ;
  envoi seulement par une fonction donnée ; réponse accordée conservée en `.tsr`, jamais redemandée ; sha256 du
  dernier `.tsr` au `tetes` suivant.
- **CB-15e** : envoi HTTPS (POST `application/timestamp-query`, RFC 3161 §3.4, aucune redirection, 65 536 octets au
  plus), commande `jeton`, armée par `--envoi` seulement. Aucune requête réseau réelle (serveur de boucle locale).
- **CB-17a** : `status` lit le journal sans écrire ni verrou ; une `lecture` reconnue à ses premiers octets, jamais
  décodée ; jugement d'une `sante` aux seuils de l'ADR-0029 §2.3 égaux à `analyse.json` (test croisé) ; D-3 non jugé.
- **CB-17b** : état par fenêtre, rapport (santé seule, aucun nombre à virgule, même sortie avec ou sans lectures),
  strates, `status --journal`.
- **CB-17c** : résumé par jour (`[ws, codes]`, liste blanche des clés), commande `resume` (AVIS Q-D-03 pt 2).
- **CB-17d** : compte à quorum M_j ≥ 2 sur les résumés des autres, lus strictement (`RESUME/…`), avec leur âge
  (AVIS Q-D-03 pt 3).
- **CB-15f** (relecture du générateur, dixième diff) : au dépôt, fichiers ordinaires seuls, ouverts sans attente,
  sans descripteur perdu ; écriture sans lien suivi ; dépôt illisible : le compte local de `status` reste.

## 2. Tests d'abord, mutants, gates

**Rouges** (squelettes d'interface ou code de l'état précédent ; `preuves/rouge-*.txt`) : tous en échec d'assertion,
0 ERROR : CB-15a 7, CB-15b 4, CB-15c 3 (+1 vert par construction : non-régression sans dépôt), CB-15d 5, CB-15e 2,
CB-17a 5, CB-17b 4 (+1 vert par construction : invariance), CB-17c 2, CB-17d 3 + 1 (complément : codes non
textes), CB-15f 4 + 1 (dépôt illisible) + 1 (descripteur perdu, assertion ajoutée à un test existant).

**Mutants** (`travail/outils/campagne.py` ; commande du job : runner puis ligne s2bis lue dans le `gates.yml` de la
copie mutée, python3.12 `-X dev -W error`, réseau isolé, borne 300 s, témoin VIVANT exigé ; SHOGEN-S2BIS-MUT-COMMANDE-1,
SHOGEN-MUT-FATAL-1) ; définitions versées dans `travail/mutants/mutants_<état>.py`, résultats
`travail/preuves/mutants-<état>.txt` :

| sous-lot | mutants | tués | par le test visé | par un autre test | par la ligne du job (plancher) | vivants | FATAL | témoin |
|---|---|---|---|---|---|---|---|---|
| CB-15a | 19 | 19 | 18 | 0 | 1 | 0 | 0 | VIVANT |
| CB-15b | 19 | 19 | 18 | 0 | 1 | 0 | 0 | VIVANT |
| CB-15c | 13 | 13 | 12 | 0 | 1 | 0 | 0 | VIVANT |
| CB-15d | 12 | 12 | 11 | 0 | 1 | 0 | 0 | VIVANT |
| CB-15e | 11 | 11 | 10 | 0 | 1 | 0 | 0 | VIVANT |
| CB-17a | 17 | 17 | 16 | 0 | 1 | 0 | 0 | VIVANT |
| CB-17b | 15 | 15 | 14 | 0 | 1 | 0 | 0 | VIVANT |
| CB-17c | 12 | 12 | 11 | 0 | 1 | 0 | 0 | VIVANT |
| CB-17d | 18 | 18 | 17 | 0 | 1 | 0 | 0 | VIVANT |
| CB-15f | 14 | 14 | 13 | 0 | 1 | 0 | 0 | VIVANT |
| total | 150 | 150 | | | | | | |

**Gates de l'arbre final** (copie de 5cfe746 + série ; `travail/preuves/`) :
- runner `enforcement/tests/run-fixtures-verdict-suite-s2.py` : 136 ok, 0 échec ;
- ligne s2bis du job (`--aucun-saut --egal --plancher 294`) : Ran 294, conforme ;
- S2 (`--egal`) : Ran 415, conforme (2 sauts nommant `SHOGEN_S2_CAMPAGNE_CONTROL`, jamais posée) ;
- sim-bis (`--plancher 172`) : Ran 172, conforme (objets git du dépôt réel lus par `GIT_DIR`, lecture seule) ;
- matrice Python 3.10, 3.11, 3.12, 3.13 en `-X dev -W error` : 294 OK sous les quatre, « Warning » 0,
  « Exception ignored » 0, ligne du job conforme sous les quatre ; aucun `__pycache__` laissé (`preuves/fin3.out`,
  `preuves/final3-*.txt`) ;
- `cargo --locked xtask verify` (réseau isolé, cible cargo dédiée) : lignes de verdict identiques à celles du témoin
  (copie de 5cfe746) : S-G1 à S-G8 VERT, fmt, no_std, clippy VERT ; seule S-G9 ROUGE,
  `docs/17-modele-de-menace.md:70` (connue sur les copies) ; verdict global ROUGE par elle seule
  (`preuves/xtask-final3-verdicts.txt`, `xtask-t0-verdicts.txt`) ;
- base t0 (copie de 5cfe746) : runner 136, s2bis 255, S2 415, sim-bis 172, tous conformes (sim-bis au second essai,
  §8).

**Règles communes** : bibliothèque standard seule (R-8 ; imports neufs : `hashlib`, `http.client`, `json`, `os`, `re`,
`stat`, `contextlib`, `urllib.parse`, `calendar`, `time`, `secrets` ; `test_fitness`, frontière d'imports, vert) ;
aucun `TODO`/`FIXME` dans les fichiers touchés (R-13, recherche : 0) ; écrivain (SHOGEN-S2BIS-ECRIVAIN-REFUS-ARRET-1,
annexe B l.1110, lu) : le seul enregistrement neuf, `tetes`, ne porte que des entiers bornés, des textes contrôlés et
null, aucun flottant, et s'écrit sans refus depuis un dépôt hostile
(`test_seize_tetes_au_plus_et_enregistrement_admis_par_l_ecrivain`) ; `status` et `resume` n'écrivent rien au
journal ; aucune requête réseau (`unshare -n`, `lo` seule ; envoi testé contre un serveur de boucle locale).

## 3. Item de l'annexe B (recherche de « CB-15 », « CB-17 » dans `docs/adr-0028/ANNEXE-B-items.md` seul)

Un seul déclencheur : **SHOGEN-S2BIS-CHRONYC-FORMAT-1** (l.1051 ; « G0 de CB-17 et de la règle de validité RB, avant le
gel » ; prix « une lecture sur pièce et une borne »). **Non fermé, rendu (limite)** : aucune source du format de la
sortie de `chronyc` n'est détenue (chrony absent de l'hôte, aucune documentation dans `biblio/`, réseau interdit) ; le
fermer sans pièce serait supposer un format. Dans le lot : `status` et les résumés ne jugent pas D-3 (« D-3 non jugé »,
FORMAT §16.2) et comptent à part les relevés D-3 absents, en erreur ou de code non nul (test
`test_codes_d_une_sante`, mutant M-17a-15). Proposition : lecture sur pièce de la documentation de `chronyc tracking`
et d'une sortie gelée capturée à DB-0, puis une règle D-3 commune à `status` et à RB-3 (test croisé), et la borne de
la capture d'erreur de `sante.py` (O-3).

## 4. Questions rendues (décisions de valeur)

Choix faits dans le code, à confirmer ou à changer par l'orchestrateur (chacun localisé au FORMAT) :
- **Q-1 Place de `tetes`** : dans la fenêtre qui clôt l'heure, après ses `lecture` et avant sa `sante` ; l'export
  de la tête suit le marqueur et le point (FORMAT §15.6). Autre forme possible : un enregistrement hors fenêtre.
- **Q-2 E/S du dépôt dans la boucle** : lecture du dépôt et export faits par la boucle du pool, à l'heure ; jamais
  d'exception (échec noté au champ `export`), jamais d'attente sur un fichier spécial (CB-15f), mais une E/S lente
  (montage réseau de l'espace de sauvegarde) retarderait la boucle. Recommandé : un dépôt **local**, synchronisé par
  un processus séparé (DB) ; sinon sortir ces E/S de la boucle.
- **Q-3 Forme du dépôt** : un dossier plat, fichiers préfixés par l'observateur (`O1-pool.tete`, `O1-<jour>.tsr`,
  `O1-<jour>.resume`) ; le nom fait autorité. Avec un dossier par sous-compte (Storage Box), la lecture changerait
  (l'observateur serait celui du dossier). À fixer avec la lecture croisée « à établir à DB-0 » (AVIS Q-D-03).
- **Q-4 Manifeste** : toutes les têtes valides du dépôt (les siennes et celles des autres), triées ; sans tête
  propre, refus `JETON/tete` (AVIS pt 1 : sa propre tête chaque jour, les autres en plus quand elles sont lisibles).
- **Q-5 Nonce** : 64 bits tirés par `secrets` à chaque requête ; il est dans le `.tsq` conservé au dépôt, pas au
  journal (le `tetes` porte le sha256 du `.tsr`).
- **Q-6 Contrôle de la réponse** : statut et présence du jeton seuls ; signature, empreinte et nonce se vérifient
  hors ligne (`openssl ts -verify`, comme `scripts/sceau/verify.sh`) ; un rejet n'est pas conservé (sortie 1).
- **Q-7 Armement** : `jeton --envoi URL` (https) arme l'envoi ; sans lui, « non armé », rien ne part (E-C-36 :
  « un paramètre que seul le go écrit de l'investisseur autorise »). Paramètre de commande ou configuration scellée ?
- **Q-8 Nom d'observateur** : règle `[A-Za-z0-9]{1,16}` ajoutée au descripteur (refus `CONFIG/incoherent :
  observateur-nom`) : elle resserre un schéma de P1 (le nom nomme les fichiers au dépôt).
- **Q-9 D-3 non jugé** : tant que l'item CHRONYC est ouvert, les comptes de `status` et les résumés sont optimistes
  (une fenêtre dégradée par D-3 seul compte valide). Accepter l'affichage « D-3 non jugé », ou retenir `status` et
  `resume` jusqu'à la lecture sur pièce ?
- **Q-10 Définitions D-4, D-5 communes avec RB-3** : `status` compte en échec un témoin dont le résultat n'est pas
  une réponse retenue (le délai de 2 s de CB-11 compris), et un nom sans réponse retenue, de rcode non nul ou sans
  réponse A ; seuils égaux à `analyse.json` (test croisé). E-R-05 (PROPOSITION l.431) dit « au moins 2 témoins sur
  3 sans réponse en 2 s ; 2 noms sur 2 en échec » : RB-3 doit prendre les mêmes définitions (code commun ou test
  croisé), sinon `status`, les résumés et le recalcul divergent.
- **Q-11 Lecture reconnue à ses premiers octets** (`{"adresse":`, première clé de toute `lecture` canonique) : c'est
  ce qui permet « aucune lecture décodée » (test « Status » de la PROPOSITION) ; sûr tant que la forme canonique trie
  les clés et qu'aucun autre type n'a `adresse` pour première clé (FORMAT §1.2, §9.1).
- **Q-12 Publication des résumés** : `resume` réécrit le résumé de chaque jour présent au journal ; sa fréquence
  (minuterie) est laissée au déploiement.

## 5. Limites rendues (items à former, règle PAROXYSME)

- **I-1 SHOGEN-S2BIS-CHRONYC-FORMAT-1** : voir §3 (rendu, non fermé).
- **I-2 Rétention et comptes** : `status` et les résumés ne voient que les fichiers présents (rétention locale de
  7 jours, ajout daté du 2026-10-04 à l'ADR-0029) ; un compte cumulé sur la campagne demande un état persistant, ou
  les résumés publiés comme mémoire. [à former : SHOGEN-S2BIS-STATUS-RETENTION]
- **I-3 Journal hors FORMAT** : `status` suppose un journal de l'écrivain ; une ligne JSON valide mais hors FORMAT
  (`ws` non entier dans une `sante`, `ws` hors calendrier, `disque` partiel) peut le faire échouer ou gonfler la
  grille. Remède proposé : contrôle de forme par type d'enregistrement commun avec le lecteur du recalcul (RB-18).
- **I-4 Tête du journal secondaire** : l'export de la tête du journal de la carte (CB-13, tranche P2A) et le
  `tetes` du secondaire restent à câbler à l'intégration (`tetes.Depot(dossier, observateur, "carte")` existe).
- **I-5 Bout en bout** : le test de bout en bout de P1 (CB-18) tourne sans dépôt ; un test de conformité au FORMAT
  avec `--depot` (enregistrement `tetes`) est à ajouter à l'intégration.
- **I-6 DNS de l'envoi** : `envoyer` borne connexion et lecture (10 s) mais pas la résolution du nom de la TSA
  (`getaddrinfo`) ; à borner au déploiement (minuterie de la commande, DB-3) ou par une adresse résolue au client DNS.
- **I-7 Un écrivain par nom** : deux `resume` (ou deux `jeton`) simultanés partagent le nom du temporaire ; un
  fichier partiel peut alors être publié. Une exécution unique (minuterie sans recouvrement, ou verrou) est à poser
  au déploiement.
- **I-8 Seize têtes au plus** : au-delà de 16 fichiers de tête au dépôt, sa propre tête peut tomber hors de la
  lecture (refus `JETON/tete`) ; 4 observateurs × 2 journaux = 8 : borne à revoir si le dépôt en garde davantage.

## 6. Écarts

- **E-1** (20:02 UTC) : un `diff -rq copie final` sur deux copies entières du dépôt (comparaison récursive, contre la
  lettre « même sur tes copies ») ; sortie : 8 noms, tous mes fichiers ; les copies n'ont aucun dossier interdit
  (exclus à l'archive). Plus aucune comparaison récursive de copies entières ensuite.
- **E-2** : diffs de CB-15d et de CB-17 d'abord trop longs (224, 297, 210 lignes) : redécoupés en CB-15d/CB-15e et
  CB-17a à CB-17d ; campagnes lancées sur les anciens états arrêtées, journaux vides versés à
  `travail/preuves/invalides/`, campagnes refaites sur les états définitifs.
- **E-3** : mini-arbres de travail (`mini.sh` : `cp -a`, `chmod -R` de `docs/adr-0029/s2bis`), copies des campagnes
  (`copytree` de `docs/`) et diffs préliminaires (`git diff --no-index` des mini-arbres entiers) : opérations
  récursives sur un sous-arbre de `docs/` de mes copies (aucune liste affichée, aucune recherche). Les diffs livrés et
  le contrôle de série ne descendent plus sous `docs/` (`faire_diff2.sh`, `serie.sh` : les deux fichiers touchés
  seuls) ; l'état CB-15f est fait sans récursion sous `docs/`.
- **E-4** : relecture du générateur après la série verte : trois défauts trouvés et corrigés, tests d'abord :
  (a) CB-17d, un résumé aux codes non textes faisait lever `status` (TypeError) : complément dans CB-17d, rouge
  `preuves/rouge-cb17d-complement.txt`, mutant M-17d-17 ; (b) tubes nommés et liens au dépôt : dixième diff CB-15f
  (rouge `preuves/rouge-cb15f.txt`, la cible du lien écrasée par la tête), plus le dépôt illisible
  (`preuves/rouge-cb15f-depot.txt`) ; (c) dans CB-15f même, la première forme de `lire_borne` perdait un
  descripteur par dossier lu (`open` d'un descripteur de dossier lève sans le fermer ; fuite mesurée, 5 sur 5) :
  assertion ajoutée, rouge `preuves/rouge-cb15f-descripteurs.txt`, forme `try`/`finally`, mutant M-15f-13. Les
  campagnes de CB-17d et de CB-15f tournent sur les octets corrigés ; l'arbre final est recontrôlé (final3).
- **E-5** : un premier contrôle de l'arbre final après CB-15f, lancé au plancher 293, arrêté et refait au plancher
  294 (`preuves/invalides/fin2-sur-293.out`) ; les campagnes ont tourné avant l'écriture des sections METRIQUES
  (documents seuls : aucun test ni gate ne lit METRIQUES, vérifié par recherche dans `s2bis/tests`, `enforcement`,
  `gates.yml`).

## 7. Estimation révisée des sous-lots restants de P2

Mesuré ici [mesuré, `travail/outils/compte.py`] : CB-15 et CB-17, chiffrés ≈ 180 + ≈ 160 = 340 lignes au G0
(PROPOSITION l.223, l.225), font 1460 lignes ajoutées de code et de tests en dix diffs, soit ×4,3 ;
hors des ajouts de l'AVIS (résumés et quorum : CB-17c, CB-17d) et de la relecture (CB-15f), ×3,2. Les
tests font environ 58 % des lignes.

Restent dans P2 hors des deux tranches en cours (P2A : CB-6, CB-12, CB-13 ; P2B : ce lot) : CB-7 (≈ 180), CB-8
(≈ 170), CB-9 (≈ 180), CB-14.k (≈ 175 chacun, k = 2 à 4), CB-16 (≈ 140), et CB-19 en option (≈ 160) : 1 020 à 1 370
lignes au G0 sans CB-19. Avec un facteur de ×2 (décodeurs surtout faits de fixtures) à ×3,2 (le facteur mesuré ici
hors ajouts), **≈ 2 000 à 4 400 lignes, soit ≈ 14 à 30 diffs à la taille moyenne mesurée ici (146 lignes de code
par diff), 11 à 22 au plus serré (200)** [inféré], plus l'intégration des sorties de ce lot (I-4, I-5 : ≈ 1 à 2
diffs) et CB-19 s'il reste dans P2 (≈ 2 diffs). Les entrées attendues
(paires servies avant CB-7 et CB-8, adresses du témoin avant CB-9, licences avant le gel) bornent l'ordre plus que la
taille.

## 8. Journal de provenance (G1)

**Sources** (sha256 relevés entre 20:09 et 20:12 UTC sur le dépôt réel, lecture seule) :

| niveau | source | sha256 | lu |
|---|---|---|---|
| [lu] | brief `p2b/BRIEF-P2B.md` | `0cc6ffe1…cd27` | en entier (deux fois) |
| [lu] | G0 `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md` | `0e9001f3…2a90` | en entier (25 l.) |
| [lu] | `docs/adr-0029/g0-collecte/PROPOSITION.md` | `0cdf84c2…bfd0` | l.1-375 (§2.2, §2.4, §2.6 compris), l.616-916 ; l.427-435 (E-R-01 à E-R-09) et l.783-811 (§5) relues |
| [lu] | `docs/adr-0029/g0-collecte/AVIS.md` | `a919b307…16ce` | en entier ; Q-D-03 (l.36-47) relu |
| [lu] | `docs/adr-0029/ADR-0029-campagne-S2-bis.md` | `35563d8f…9eb8` | l.76-141, l.210-260, l.395-401 (ajouts datés) |
| [lu] | FORMAT `docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md` (5cfe746) | `178041f2…6dc8` | en entier |
| [lu] | METRIQUES `docs/adr-0029/s2bis/METRIQUES-S2BIS.md` (5cfe746) | `f1761ea4…4ca9` | en-tête ; CB-19a à CB-19h, RB-1l (forme) |
| [lu] | `docs/adr-0028/ANNEXE-B-items.md` | `3f738722…d0d2` | recherche « CB-15 », « CB-17 » dans ce seul fichier ; l.1042, l.1051, l.1110 |
| [lu] | `scripts/sceau/make-tsq.sh`, `verify.sh` | `ef66fe83…d3c5`, `b6f7b66a…d166` | en entier |
| [lu] | `biblio/INDEX.md` | `593b96de…c3d6` | l.356 (entrée RFC 3161) |
| [lu] | RFC 3161, `biblio/ietf-rfc3161-time-stamp-protocol-2026-10-04.txt` | `39fd1764…8240` (= INDEX) | §2.4.1, §2.4.2 (l.213-470), §3.4 (l.735-757), en-tête de l'annexe C |
| [lu] | `s2bis/config/analyse.json` | `e9243c79…1d00` | bloc `degradation` |
| [lu] | code de P1 (5cfe746) : `journal.py`, `boucle.py`, `entree.py`, `sante.py`, `config.py`, `lecture.py`, `http.py` | `a39ab0dc…`, `daf4b1c1…`, `403987d4…`, `2afee71a…`, `92e86e62…` | lus (interfaces et parties touchées) ; tests : `test_garde`, `test_fitness`, `test_format`, `test_bout_en_bout`, en-têtes de `test_entree`, `test_journal`, `test_boucle` |
| [lu] | pièces de revue de P1 (forme) : `revue-p1a` (brief, rapport), `revue-p1b` (G2), `revue-out2` (brief, rapport) | — | lues pour la forme des diffs et des tests |
| [abs] | X.690 (règles DER) | — | non détenue : octets de référence produits par OpenSSL 3.0.13 [mesuré] |
| [abs] | identifiant de SHA-256 (2.16.840.1.101.3.4.2.1) | — | non détenu en texte : octets d'OpenSSL [mesuré] |
| [abs] | documentation et sortie de `chronyc` | — | absentes (chrony non installé, rien dans `biblio/`) : item §3 |
| [abs] | lecture croisée des sous-comptes de l'espace de sauvegarde | — | « à établir à DB-0 » (AVIS) : Q-3 |
| [2nd] | champs de D-3 (« décalage, délai et dispersion racine, statut, âge ») | — | cités par E-C-25 (PROPOSITION l.186), non lus sur pièce : aucun format supposé |

**Commandes et sorties** (complètes dans `travail/preuves/`) :
- `git --no-optional-locks rev-parse HEAD` : `5cfe746…` à 18:45 et à 20:08, `5e386c4…` à 20:59 ; `status --short` :
  vide ; `log --oneline 5cfe746..HEAD` : 8 commits ; `diff --stat 5cfe746 HEAD` sur mes fichiers, `s2bis`,
  `enforcement` : `gates.yml` seul (1 ligne).
- Références RFC 3161 (`travail/ref/`, OpenSSL 3.0.13, clés des TSA jetables détruites) : `openssl ts -query -data
  donnees.txt -sha256 -cert -no_nonce` (59 octets, sha256 `ac28004e…b2ce`), 12 requêtes avec nonce, entiers DER par
  `openssl asn1parse` ; réponses : accordée (`tsa/reponse-n1.tsr`, 2 413 octets), rejet badAlg (`tsa/reponse-rejet.tsr`,
  57 octets) ; la requête produite par le code (`requete-code.tsq`) servie par une seconde TSA jetable : `openssl ts
  -verify -queryfile requete-code.tsq -in reponse-code.tsr` → `Verification: OK`, et `-data manifeste-code.txt` →
  `Verification: OK` (relancées à 20:30 UTC).
- Base t0 (19:02-19:04) : runner 136 ok ; s2bis 255 conforme ; S2 415 conforme ; sim-bis 172 conforme (second essai,
  `GIT_DIR` du dépôt réel en lecture seule ; le premier, sans historique, refusait `ORACLE/extraction`).
- États : `travail/outils/gates.sh` (`RAPIDE=1` : runner et ligne s2bis) à chaque état ; arbre final : voir §2.
- Campagnes : `travail/outils/campagne.py ETAT MUTANTS SORTIE`, en série par `chaine.sh` (processus détachés, fin
  constatée au PID) ; classées par la sortie des commandes (0 vivant, 1 tué, autre ou borne : FATAL).
- Série : `travail/outils/serie.sh diffs` → `travail/preuves/serie.txt` ; comptes : `travail/outils/compte.py`.

**Chiffres recomptés** : lignes par `wc -l`, tests par `grep -c "def test_"` et par la ligne `Ran` des suites,
planchers lus dans `gates.yml`, lignes ajoutées par `compte.py` sur les diffs livrés ; aucun chiffre de seconde main.

## 9. Nettoyage

Supprimés à 21:00:56 UTC : `p2b/copie/` et `p2b/final/` (copies entières du dépôt), `p2b/cargo-target/`, le contenu de
`p2b/tmp/`, les états périmés `travail/etats/old-*` ; place libre sur `/` : 6 698 → 6 876 Mo (`df`, disque partagé).
Gardés, légers, pour la relecture : `diffs/` ; `travail/etats/` (t0 et les dix états : mini-arbres `s2bis`,
`enforcement`, `.github`, `docs/adr-0029/s2bis`, que `serie.sh` compare) ; `travail/rouge/` (squelettes des rouges) ;
`travail/ref/` (références OpenSSL, sans clé) ; `travail/preuves/`, `travail/mutants/`, `travail/outils/`. Aucun
processus du lot ne reste. `p2b/SHA256SUMS` couvre ce rapport, `NOTES.md`, le brief, les diffs, les outils, les
mutants, les preuves et les références (`sha256sum -c SHA256SUMS` depuis `p2b/`).

## 10. Correction de la G2 (phase 2, 2026-10-08 22:08 UTC à 2026-10-09 03:36 UTC)

**Gate 0 : `claude-opus-5-5`** (identifiant exact du modèle qui tourne), effort max, worker G1 ; quatre agents successifs
du même rôle (ouverture à 22:08:43, reprises à 23:04:43, 23:46:55 et 02:02:26 UTC, chacune depuis `NOTES.md` seul).

- Pièces d'entrée : `ADJUDICATION-G2.md` (sha256 `d98f8639…e74f`, liste fermée C-1 à C-7, note Certigna), `g2/RAPPORT-G2.md`
  (sha256 `b253aa11…f4ef`, lu en entier), `BRIEF-P2B.md` (`0cc6ffe1…cd27`, toujours en vigueur).
- Base des diffs : **c58b997** (`c58b997cd4f6e76f1289d59d389214afc043e7e7`). Tête du dépôt réel à la clôture :
  `b07147d` (fusion PR #5, SB-13) ; dépôt en lecture seule, aucune opération git en écriture, aucun verrou.
- Horloge : `date -u` avant chaque heure écrite ; reprise de cette dernière phase à 02:02:26 UTC.

### 10.1 Diffs livrés (`p2b/diffs/`, dans l'ordre des numéros, sur c58b997)

Contrôle de série `travail2/outils/serie2.sh` : deux extractions neuves de c58b997 (`git archive`, chemins touchés
seuls), `patch -p1 -F0` puis `git apply --whitespace=error-all`, état comparé fichier par fichier après chaque diff :
**0 écart aux dix diffs** (`travail2/preuves/serie.txt`). Les diffs de la phase 1 (base 5cfe746) sont gardés dans
`p2b/diffs-v1-5cfe746/`.

| # | diff | code et tests ajoutés | docs | plancher (`--egal`) | corrections portées | sha256 |
|---|---|---|---|---|---|---|
| 1 | `01-CB-15a.diff` | 178 | 49 | 262 | aucune (rejoué) | `f8bb0a6e920222f5…` |
| 2 | `02-CB-15b.diff` | 198 | 48 | 266 | C-6 (noms du dépôt), C-7 (FORMAT : dépôt local) | `941774fd593a17be…` |
| 3 | `03-CB-15c.diff` | 98 | 42 | 270 | C-6 (descripteur), test de G-18 | `557995302ac7f4bc…` |
| 4 | `04-CB-15d.diff` | 194 | 65 | 274 | C-1, C-2, C-4 (G-01) | `1b754098b0b78223…` |
| 5 | `05-CB-15e.diff` | 190 | 49 | 277 | C-4 (G-03, G-04, G-16, G-17), C-5 (nonce) | `4d6f66f7308c58ce…` |
| 6 | `06-CB-17a.diff` | 192 | 46 | 282 | aucune (rejoué) | `2fc9c0094c4f7174…` |
| 7 | `07-CB-17b.diff` | 183 | 41 | 287 | C-7 (compte local) | `ccfbb7732846b88f…` |
| 8 | `08-CB-17c.diff` | 155 | 51 | 290 | C-3, test de G-18 | `2f75bc473cfb230e…` |
| 9 | `09-CB-17d.diff` | 142 | 41 | 293 | C-6 (résumés), C-7 (quorum) | `576b3abff524138f…` |
| 10 | `10-CB-15f.diff` | 166 | 57 | 298 | C-5 (`tetes` : manifeste, requête) | `4bef25d4aa4984e2…` |

Code ajouté : `travail/outils/compte.py` (`travail2/preuves/compte-diffs.txt`) ; tous ≤ 200 (R-25). Forme
(`travail2/preuves/forme-diffs.txt`) : R-13 : 0 ; ligne de plus de 120 colonnes : 0 ; octet 92 seulement dans des
littéraux `\n`, `\r`, `\xff`, `\x01`, `\x05` ; imports des lignes ajoutées : bibliothèque standard et modules du
projet seuls (liste par diff au même fichier ; neufs depuis la phase 1, en test : `base64`, `secrets`, `socket`,
`subprocess`, `sys`, `time`) ; R-8 sans objet (aucune dépendance). METRIQUES : une section par diff, refaite
(`travail2/edits/metriques.py`) : objet, rouge, tableau, mutants de la campagne refaite, suite et plancher.

### 10.2 Corrections C-1 à C-7

| n° | correction | code (arbre final) | test nommé | rouge d'assertion | mutants neufs (tous tués) | FORMAT |
|---|---|---|---|---|---|---|
| C-1 | avant d'écrire le `.tsr`, `lier` lit le jeton (ContentInfo id-signedData, SignedData, eContent id-ct-TSTInfo) et compare au TSTInfo l'algorithme (SHA-256, paramètres NULL), l'empreinte (sha256 du manifeste) et le nonce (celui de la requête ; absent si elle n'en a pas) ; écart : `JETON/liaison` ; chemin DER illisible : `JETON/reponse` ; rien de conservé, le jour reste à demander ; signature et certificat hors ligne (limite déclarée) | `tetes.py:114-134`, appel `:292` | `test_tetes.Jeton.test_jeton_lie_a_la_requete` : réponses d'`openssl ts -reply` d'une TSA jetable (clé détruite) : juste, autre empreinte, autre nonce, sans nonce ; plus autre algorithme, jeton factice, autre type de contenu ; statut 1 conservé (G-01) ; fixtures égales octet pour octet à `travail2/ref/c1/*.tsr`, dont `openssl ts -verify -queryfile` rend OK pour la juste, FAILED pour les trois autres (`ref/c1/verification.txt`) | R-C1 (CB-15d) : FAIL 1, ERROR 0 | N-C1-1 à N-C1-6 (empreinte, nonce, algorithme, types de contenu, nonce absent, code de l'écart) | §15.2 (liaison), §15.7 |
| C-2 | les fichiers de tête de l'observateur sont lus d'abord, 16 au plus, hors de la borne des 16 autres ; `ignores` compte les deux bornes | `tetes.py:257-268`, `:280` ; `Depot.lire` `:241` | `test_tetes.Jeton.test_sa_tete_toujours_au_manifeste` (17 têtes de noms antérieurs, la sienne au manifeste, `ignores` = 3) | R-C2 (CB-15d, boucle d'avant `noms[:NOMBRE]`) : FAIL 1, ERROR 0 | N-C2-1 à N-C2-3 | §15.5, §15.7 ; ferme I-8 |
| C-3 | `ws` à la fin du jour de son fichier ou au-delà, ou `suivante` au-delà : ligne illisible, le fichier s'arrête ; un nom de fichier hors calendrier (30 février) n'est pas lu ; la grille commence au plus tôt au jour du premier fichier présent moins un jour | `status.py:42-60`, `:75-77`, `:106`, `:117` | `test_status.Etat.test_grille_bornee_par_le_jour_des_fichiers` : les deux journaux corrompus de la G2 (`ws` et `suivante` portés en 2280 ; `suivante` ramenée en 2001) ; `status` en sous-processus, espace d'adressage borné à 512 Mio : sortie 0 en moins de 2 s, rapport borné (2 876 fenêtres, comptées à la main) | R-C3 (contrôle du jour retiré) et R-C3b (plancher retiré) (CB-17c) : FAIL 1, ERROR 0 chacun | N-C3-1 à N-C3-5 | §16.1, §16.3 (§6.1 cité) |
| C-4 | un test nommé par mutant vivant de la G2 | — | G-01 : `test_jeton_lie_a_la_requete` ; G-03 et G-04 : `test_envoi_borne_en_temps_et_en_octets` (TSA de boucle locale muette : `TimeoutError` sous 2 s ; réponse annoncée à 10^9 octets, 65 537 envoyés : `JETON/http`) ; G-16 et G-17 : `test_commande_jeton` (deux nonces tirés différents ; sans `tls=`, `http.CONTEXTE` transmis, `--envoi http://…` sort en 1, `JETON/url`) | R-G01 (CB-15d), R-G03, R-G04, R-G16, R-G17 (CB-15e) : FAIL 1, ERROR 0 chacun | N-C4-1, N-C4-3 ; **G-01, G-03, G-04, G-16, G-17 rejoués : tués par leurs tests nommés** | §15.8 |
| C-5 | nonce de 64 bits figé par le test de la commande (`secrets.randbits(64)`, deux appels) ; au `tetes`, champ `jeton` = `{fichier, sha256, manifeste, tsq}` (sha256 du `.tsr`, du `.manifeste` et du `.tsq` du même jour ; null pour un fichier illisible) | `entree.py:130` ; `tetes.py:187-192`, `:247-253` | `test_tetes.Jeton.test_commande_jeton` (`mock.call(64)` × 2) ; `test_jeton_du_jour_non_arme_puis_emis_une_fois`, `FichiersDuDepot.test_lecture_sans_attente_fichiers_ordinaires_seuls` | R-C5 (CB-15f) : FAIL 2, ERROR 0 ; R-G16 | N-C4-2 (63 bits), N-C5-1 à N-C5-3 | §15.5, §15.8 |
| C-6 | nom d'observateur `[a-z0-9]{1,16}` au descripteur (`CONFIG/incoherent : observateur-nom`, sortie 2), au dépôt (têtes) et aux résumés : un jumeau de casse est ignoré | `entree.py:79` ; `tetes.py:32` ; `status.py:32` | `test_tetes.Depot.test_lecture_du_depot_et_refus_nommes`, `Branchement.test_point_d_entree_depot_et_nom_d_observateur`, `test_status.Resumes.test_resumes_hostiles_refuses` ; « o-1 » refusé aux trois points d'entrée (`jeton`, pool, `resume`) | R-C6a (CB-15b), R-C6b (CB-15c), R-C6c (CB-17d) ; R-G18a, R-G18b, R-G18c | N-C6-1 à N-C6-3 ; G-18 tué | §15.4, §14.1 (renvoi) |
| C-7 | « hors D-3 » sur les lignes de compte de `status` (compte local et quorum) ; FORMAT : le dépôt est un dossier **local**, synchronisé par une unité séparée (DB-4) | `status.py:185`, `:211` | `test_status.Rapport.test_sante_seule_jugee_et_comptee_par_strate`, `Resumes.test_compte_a_quorum_ages_et_refus` | R-C7a (CB-17b), R-C7b (CB-17d) : FAIL 1, ERROR 0 | N-C7-1, N-C7-2 | §15 (paragraphe d'entrée), §16.4, §16.6 |

Rouges (`travail2/outils/rouges.py`, `travail2/preuves/rouges-final3.txt`, 18 cas) : pour chaque cas, la correction
retirée du code (texte remis à l'identique de l'état d'avant), le test gardé, python3.12 `-X dev -W error`, réseau
isolé : sortie 1, au moins un FAIL, **aucun ERROR** ; puis vert sur l'état non retouché. Les numéros de ligne
renvoient à l'arbre final (c58b997 plus les dix diffs).

### 10.3 Mutants

Campagne unique (`travail2/outils/campagne2.py`, en série par `chaine2.sh`) classée par la **commande exacte du job**
(runner, puis la ligne s2bis lue au `gates.yml` de la copie mutée, python3.12, **sans** `-X dev` : écart relevé au §4
de la G2, corrigé), borne de 300 s par mutant, réseau isolé, copie fraîche par mutant, témoin non muté VIVANT exigé à
chaque liste ; contrat SHOGEN-MUT-FATAL-1 (sortie 1 tué, 0 vivant, autre ou borne FATAL).

| liste | état | mutants | tués | par le test visé | sans test visé | vivants | FATAL | fenêtre (UTC) |
|---|---|---|---|---|---|---|---|---|
| g2 | cb15f | 30 | 30 | 24 | 6 | 0 | 0 | 00:00:10-00:18:49 |
| cb15a | cb15a | 19 | 19 | 18 | 1 | 0 | 0 | 00:18:49-00:29:54 |
| cb15b | cb15b | 20 | 20 | 19 | 1 | 0 | 0 | 00:29:54-00:43:01 |
| cb15c | cb15c | 14 | 14 | 13 | 1 | 0 | 0 | 00:43:01-00:51:51 |
| cb15d | cb15d | 18 | 18 | 17 | 1 | 0 | 0 | 00:51:51-01:04:01 |
| cb15e | cb15e | 17 | 17 | 16 | 1 | 0 | 0 | 01:04:01-01:16:21 |
| cb17a | cb17a | 17 | 17 | 16 | 1 | 0 | 0 | 01:16:21-01:27:45 |
| cb17b | cb17b | 16 | 16 | 15 | 1 | 0 | 0 | 01:27:45-01:39:51 |
| cb17c | cb17c | 17 | 17 | 16 | 1 | 0 | 0 | 01:39:51-01:52:20 |
| cb17d | cb17d | 20 | 20 | 19 | 1 | 0 | 0 | 02:03:46-02:19:03 |
| cb15f | cb15f | 17 | 17 | 16 | 1 | 0 | 0 | 02:19:03-02:31:43 |
| **total** | | **205** | **205** | **189** | **16** | **0** | **0** | |

- Les 150 mutants de la phase 1 rejoués (18 textes `avant` remis à jour sur le code corrigé ; M-15d-08 à M-15d-10
  devenus M-15e-12 à M-15e-14, leur code ayant migré), 25 neufs (C-1 : 6, C-2 : 3, C-3 : 5, C-4 : 2, C-5 : 4, C-6 :
  3, C-7 : 2 ; au moins deux par correction), les 30 de la G2 (G-01 à G-30) rejoués sur l'état final.
- Sans test visé : 10 mutants de plancher (`gates.yml`, tués par la ligne du job) et 6 de la G2 dont la liste ne
  nomme pas de test ; G-01, G-03, G-04, G-16 et G-17, les cinq vivants de la G2, sont tués, chacun par le test nommé de
  C-4 (échecs relevés : voir `travail2/preuves/mutants-g2.txt`).
- Aucun « visé NON en échec ». Définitions : `travail2/mutants/mutants_<liste>.py` ; résultats :
  `travail2/preuves/mutants-<liste>.txt` ; journaux : `chaine.log` (campagne 4, coupée), `chaine-reprise.log`.

### 10.4 Gates et matrice (arbre final complet : extraction de c58b997, exclusions du brief, plus les dix diffs)

| contrôle | résultat |
|---|---|
| ligne du job s2bis de chaque état (`--egal`, python3.12) | 262, 266, 270, 274, 277, 282, 287, 290, 293, 298 : **10 conformes** ; runner 136 ok à chaque état (`travail2/preuves/j2.log`) |
| runner | 136 ok, 0 échec |
| s2bis (`--aucun-saut --egal --plancher 298`) | Ran 298, conforme |
| S2 (`--egal`) | Ran 415, conforme ; deux sauts nommant `SHOGEN_S2_CAMPAGNE_CONTROL`, jamais posée |
| sim-bis (plancher 194 de c58b997) | Ran 194, conforme (objets git du dépôt réel par `GIT_DIR`, lecture seule) |
| matrice 3.10, 3.11, 3.12, 3.13, `-X dev -W error`, `unittest discover` | 298 OK sous les quatre ; « Warning » 0 ; « Exception ignored » 0 ; ligne du job conforme sous les quatre |
| `__pycache__` sous les racines de suites | 0 |
| `cargo --locked xtask verify` (arbre final et témoin c58b997, réseau isolé) | 22 lignes de verdict **identiques** (`cmp`) : S-G1 à S-G8, fmt, no_std, clippy VERTS ; S-G9 ROUGE (1 violation) des deux côtés, connue sur les copies (sortie brute non lue) |

Sorties : `travail2/preuves/final2.log`, `final-*.txt`, `xtask-{final,temoin}-verdicts.txt`.

### 10.5 Items (lignes pour l'annexe B ; règle PAROXYSME)

| item | constat | propriétaire | déclencheur | prix | origine |
|---|---|---|---|---|---|
| SHOGEN-S2BIS-TSA-CERTIGNA-1 | l'horodatage du projet se fera chez Certigna (horodatage qualifié eIDAS, RFC 3161, avec compte et authentification ; note de l'investisseur du 2026-10-08), non chez FreeTSA ni par OpenTimestamps ; le code de P2B n'en change pas : `jeton` envoie la requête sans authentification (POST `application/timestamp-query`, URL donnée par `--envoi`), sans politique (`reqPolicy` absent, FORMAT §15.1), et la signature se vérifie hors ligne sans chaîne de confiance fixée ; restent à lire sur pièce (documentation du service non détenue [abs]) et à fixer : l'URL https du service ; la forme de l'authentification de la requête (en-tête HTTP, certificat client ou autre) et le lieu de ses secrets (configuration scellée, jamais journalisés ni commités) ; les identifiants des observateurs (un compte par observateur ou un compte commun, et leur lien avec le nom `[a-z0-9]{1,16}` du descripteur) ; la politique d'horodatage exigée (OID de `reqPolicy`) ; le certificat de la TSA et sa chaîne pour `openssl ts -verify` (statut qualifié lu à la liste de confiance de l'UE) | orch. ; requis : investisseur (compte Certigna) | lot 7 | une lecture sur pièce, l'authentification ajoutée à `envoyer`, une configuration scellée et des tests sur fixtures [inféré] | adjudication de la G2 de P2B (note de l'investisseur, 2026-10-08) |
| SHOGEN-S2BIS-DEPOT-LIENS-1 | les lectures du dépôt (têtes, `.tsr`, résumés) suivent les liens symboliques : un lien vers un fichier hors du dépôt qui porte une tête valide est lu et retenu (la lecture est bornée et seule une forme de tête est retenue) | orch. | G0 de DB-4 (synchronisation du dépôt) | `O_NOFOLLOW` à la lecture si le dépôt n'est pas strictement local, et un test [inféré] | G2 de P2B, O-1 |
| SHOGEN-S2BIS-OBSERVATEURS-LISTE-1 | volet restant après C-6 (noms `[a-z0-9]{1,16}`, jumeaux de casse écartés au dépôt et au descripteur) : `status` compte au quorum tout nom d'observateur d'un résumé lisible du dépôt, et `jeton` met au manifeste toute tête d'un nom de la grammaire ; aucune liste fermée des quatre observateurs | orch. | gel du collecteur (configuration scellée, avec SHOGEN-S2BIS-CONFIG-PRODUCTION-1) | une liste fermée en configuration scellée, lue par `status`, `resume` et `jeton`, et des tests [inféré] | G2 de P2B, O-2 et O-8 |
| SHOGEN-S2BIS-STATUS-QUEUES-1 | `status` arrête un fichier du journal à sa première ligne illisible, ou d'un jour postérieur au sien (C-3), sans le dire : les fenêtres qui suivent disparaissent du rapport ; résiduel de C-3 : la borne haute de la grille est le jour du dernier fichier présent, si bien qu'un fichier au nom d'un jour lointain et aux `ws` de ce jour l'étend encore [mesuré : un journal sain d'une ligne et `pool-2999-01-01-0.jsonl` portant un marqueur de ce jour : `status` sort en 1 sur MemoryError en 3,0 s, espace d'adressage borné à 512 Mio ; `travail2/preuves/sonde-grille-jour-lointain.txt`] | orch. | G0 de RB-18 (lecteur commun du recalcul) ou gel du collecteur | une ligne du rapport (fichiers arrêtés avant leur fin), les noms de fichiers d'un jour postérieur au lendemain de l'horloge écartés, et des tests [inféré] | G2 de P2B, O-3 ; correction C-3 (résiduel du générateur) |
| SHOGEN-S2BIS-JOURNAL-FICHIER-SPECIAL-1 | un tube nommé au nom d'un fichier du journal bloque `status` (ouverture sans `O_NONBLOCK`), comme il bloquerait la reprise de l'écrivain de P1 | orch. | avant le gel du collecteur (lecteurs du journal : `status`, reprise de l'écrivain) | ouverture sans attente et fichier ordinaire exigé, comme au dépôt (FORMAT §15.9), et un test [inféré] | G2 de P2B, O-4 |
| SHOGEN-S2BIS-ENVOI-ECHEANCE-1 | `envoyer` borne chaque opération (connexion, lecture : `delai`, 10 s) mais ni la résolution du nom de la TSA (`getaddrinfo`) ni la durée totale : une TSA au goutte-à-goutte tient la commande `jeton` | orch. | G0 de DB-3 (minuterie de `jeton`), au plus tard lot 7 (avec SHOGEN-S2BIS-TSA-CERTIGNA-1) | une échéance totale, dans le code ou dans l'unité systemd (`TimeoutStartSec`), et un test [inféré] | G2 de P2B, O-5 ; I-6 du générateur |
| SHOGEN-S2BIS-RB3-DEGRADATIONS-1 | le jugement d'une fenêtre par `status` (D-1, D-2, D-4, D-5 ; FORMAT §16.2, CB-17a) est écrit dans le collecteur ; la règle de validité du recalcul (RB-3) doit juger les mêmes fenêtres de la même façon, D-4 et D-5 compris | orch. | G0 de RB-3 | import des définitions de `status`, ou test croisé sur un même journal (comme celui des seuils, égalité à `analyse.json` dans `test_status`) [inféré] | G2 de P2B, Q-10 |

Volets ajoutés à des items existants (décisions de l'adjudication) :
- **SHOGEN-S2BIS-CONFIG-PRODUCTION-1** (Q-7) : URL de la TSA dans la configuration scellée et état d'armement de
  `jeton` lisible au dépôt ou au journal (auditable) ; `--envoi` reste le seul armement du code.
- **SHOGEN-S2BIS-CHRONYC-FORMAT-1** (Q-9) : toujours ouvert, rendu en limite (aucune pièce du format de `chronyc`
  détenue) ; le gel du collecteur ne précède pas sa fermeture ; `status` dit « hors D-3 » d'ici là (C-7).
- Q-3 (forme du dépôt, dossier plat) : à DB-0, avec la lecture croisée des sous-comptes ; Q-12 (fréquence des
  résumés) : au déploiement ; Q-1, Q-4, Q-11 adoptées (rien à changer).

### 10.6 Écarts de la phase 2

- **E-6 (interruption)** : la campagne 4 (une seule chaîne, PID 7118, lancée le 2026-10-09 à 00:00:12) a été coupée
  par le redémarrage du conteneur vers 02:00 UTC, pendant la liste cb17d (commencée à 01:52:20 ; 9 mutants classés au
  journal partiel) ; cb15f n'était pas commencée. Les neuf listes finies (g2, cb15a … cb15e, cb17a … cb17c : 168
  mutants) avaient chacune leur fichier de résultat complet (témoin VIVANT, bilan égal à la taille de la liste) et les
  états n'avaient pas bougé (620 fichiers recontrôlés contre `empreintes-etats-campagne4.txt`, 0 écart ; listes de
  mutants inchangées depuis 23:42:21) : gardées. cb17d (20) et cb15f (17) refaites en entier de 02:03:46 à 02:31:43
  (chaîne PID 910) ; le journal partiel est versé, non compté, à `travail2/preuves/invalides/campagne-4-interrompue/`.
- **E-7 (campagnes invalides, non comptées)** : campagne 1 (23:34) arrêtée : un rouge de C-2 rendait ERROR, test
  retouché ; campagne 2 (23:42) : trois chaînes en parallèle, contraire à « un seul processus lourd à la fois » (charge
  7,4 sur 4 cœurs), deux arrêtées puis la troisième ; campagne 3 (23:51) arrêtée sur G-18 VIVANT (mutation devenue
  équivalente pour les tests après C-6 : « O-1 » était refusé par la majuscule), tests retouchés (« o-1 ») avant la
  campagne 4. Journaux sous `travail2/preuves/invalides/campagne-{1,2-paralleles,3-g18}/`.
- **E-8** : trois reprises par des agents neufs (redémarrages du conteneur) ; chaque reprise a recontrôlé l'état réel
  des fichiers avant de se fier aux NOTES (empreintes des états, résultats complets).
- **E-9** : les mini-arbres d'états (`travail2/etats`, `etats-v1`) se copient par `cp -a`, ce qui recopie le sous-arbre
  `docs/adr-0029/s2bis` de mes copies (comme E-3) ; aucune recherche ni liste sous `docs/`.
- **E-10 (variante)** : un premier passage des planchers de la variante (02:47-02:50) est invalide, non compté
  (`travail2/preuves/invalides/jv-sans-s2harness/`) : `test_decodeurs` de P2A lit `s2-harness/tests/fixtures/` et
  `expected.json`, absents de mes mini-arbres (12 ERROR, sur la base P2A seule aussi : artefact de l'arbre, non de la
  série) ; ces fichiers de c58b997 ont été ajoutés à la base de la variante, puis tout refait.
- Aucune pièce de D.2 ouverte, aucun `*.jsonl` réel, `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée, aucun appel réseau
  réel (tout sous `unshare -n`), aucune écriture git ni sous `.claude/`, aucun secret lu ni écrit.

### 10.7 Variante sur la série P2A corrigée (`p2b/diffs-apres-p2a/`)

Demandée par l'orchestrateur (message reçu le 2026-10-09 vers 00:10 UTC), faite **après** les corrections prouvées sur
c58b997. Base : c58b997 plus les huit diffs de P2A corrigés, dans l'ordre CB-6a, CB-6b, CB-6c, CB-6d, CB-12a, CB-12b,
CB-13a, CB-13b (`s2bis/p2a/diffs/` ; `p2a/SHA256SUMS`, sha256 `26548156…17f4`, `sha256sum -c` : 289 lignes OK, 0
écart, recontrôlé à 02:10 UTC) ; plancher s2bis de P2A : 297, mesuré conforme sur cette base (Ran 297).

Construction (`travail2/outils/variante.py`, déterministe) : pour chaque état k de la série corrigée, les fichiers que
P2B change par rapport à c58b997 sont repris sur la base P2A ; fichiers neufs de P2B (`tetes.py`, `status.py`,
`test_tetes.py`, `test_status.py`) copiés, renvois renumérotés ; fichiers touchés des deux côtés fusionnés à trois
(`git merge-file`, base c58b997) : `boucle.py` (conflit de docstring résolu par règle écrite : les deux textes gardés),
`entree.py` (docstring, import, sous-commandes : `--depot` au seul pool, puis `jeton`, `status`, `resume` à côté de
`secondaire`, aiguillage avant celui de P2A ; construction : `construire(*args, a.depot) if pool else
construire_secondaire(*args)`), `test_entree.py` (sans conflit) ; tout conflit hors règle arrête la construction
(aucun). FORMAT : tête fusionnée à trois, puis le §15 de P2A (processus secondaire), puis **les §15 et §16 de P2B
devenus §16 et §17**, renvois compris (`§16` → `§17`, puis `§15` → `§16`, dans les seuls textes de P2B ; la base
c58b997 ne porte aucun `§15` ni `§16`, contrôlé). METRIQUES : celui de P2A, puis les sections de P2B renumérotées, avec
une note de variante. Contrôlé : `tetes.py`, `status.py`, `test_tetes.py` et `test_status.py` de la variante sont
égaux à ceux de la série corrigée à la renumérotation près ; seuls `boucle.py`, `entree.py` et `test_entree.py`
diffèrent (fusion) (`travail2/preuves/variante-ecarts-fichiers.txt`). Pour les tests de P2A, la base de la variante
porte aussi `s2-harness/tests/expected.json` et `s2-harness/tests/fixtures/` de c58b997 (lus par `test_decodeurs` de
P2A ; fichiers non touchés).

| # | diff | code et tests ajoutés | docs | plancher (`--egal`) | sha256 |
|---|---|---|---|---|---|
| 1 | `01-CB-15a.diff` | 178 | 53 | 304 | `3e3ff2f268a90dd0…` |
| 2 | `02-CB-15b.diff` | 198 | 52 | 308 | `626a632baa80a5c4…` |
| 3 | `03-CB-15c.diff` | 101 | 46 | 312 | `3f24c16dc843b510…` |
| 4 | `04-CB-15d.diff` | 194 | 69 | 316 | `67490b186dff62c5…` |
| 5 | `05-CB-15e.diff` | 187 | 53 | 319 | `fa784b9318229e18…` |
| 6 | `06-CB-17a.diff` | 192 | 50 | 324 | `94a1c010cd440721…` |
| 7 | `07-CB-17b.diff` | 184 | 45 | 329 | `9482f73fb764f389…` |
| 8 | `08-CB-17c.diff` | 155 | 55 | 332 | `b669908854d2d3e0…` |
| 9 | `09-CB-17d.diff` | 142 | 45 | 335 | `7e92491bff963aaf…` |
| 10 | `10-CB-15f.diff` | 166 | 61 | 340 | `79e91fbcb9006edd…` |

Contrôles de la variante :

| contrôle | résultat |
|---|---|
| série (`travail2/outils/serie_variante.sh`) | deux extractions neuves de c58b997 ; les 8 diffs de P2A, puis les 10 de la variante, par `patch -p1 -F0` et par `git apply` : **0 écart** après P2A et après chacun des dix diffs (`travail2/preuves/serie-variante.txt`) |
| R-25 et forme | code ajouté de 101 à 198 par diff (tous ≤ 200) ; R-13 0 ; > 120 colonnes 0 ; octet 92 seulement en littéraux (`travail2/preuves/forme-diffs-variante.txt`) |
| ligne du job de chaque état (`--egal`) | t0 (P2A) 297 ; puis 304, 308, 312, 316, 319, 324, 329, 332, 335, 340 : **11 conformes** ; runner 136 ok à chaque état (`travail2/preuves/jv.log`) |
| arbre complet de la variante (`final-variante` : extraction de c58b997, exclusions du brief, plus P2A et la variante ; `travail2/outils/final_variante.sh`) | runner 136 ok ; s2bis Ran 340 conforme ; S2 Ran 415 conforme (deux sauts nommant `SHOGEN_S2_CAMPAGNE_CONTROL`, jamais posée) ; sim-bis Ran 194 conforme (`travail2/preuves/final-variante.log`) |
| matrice 3.10 à 3.13, `-X dev -W error`, `unittest discover` | 340 OK sous les quatre ; « Warning » 0 ; « Exception ignored » 0 ; ligne du job conforme sous les quatre |
| `cargo --locked xtask verify` | 22 lignes de verdict identiques à celles du témoin c58b997 (`cmp`) ; S-G9 ROUGE seule, des deux côtés |
| mutants des fichiers fusionnés (`travail2/outils/mutants_variante.py`, `campagne2v.py`, commande exacte du job, plancher 340 à l'état final) | 31 mutants de la série qui mutent `boucle.py` ou `entree.py` (dont G-14 à G-18 ; M-15c-12 réécrit sur la ligne fusionnée), rejoués sur les états de la variante : **31 tués** (29 par leur test visé, G-16 et G-17 par `test_commande_jeton`), 0 vivant, 0 FATAL, témoin VIVANT aux six listes (`travail2/preuves/variante-mutants-*.txt`, `chaine-variante.log`, de 03:08:08 à 03:33:30). Des 174 autres, 164 mutent `tetes.py` (90) ou `status.py` (74), égaux à la renumérotation près à ceux de la série sur c58b997, et 10 sont des mutants de plancher de `gates.yml` (planchers de la variante mesurés à chaque état, ligne précédente) : non rejoués |

Limites de la variante : la tête du journal secondaire (`carte`, P2A) n'est ni exportée ni consignée au `tetes` (I-4
de la phase 1, toujours ouvert : `tetes.Depot(dossier, observateur, "carte")` existe, rien ne l'appelle) ; à câbler à
l'intégration.

### 10.7 bis Estimation révisée

La série corrigée fait 1 696 lignes ajoutées de code et de tests en dix diffs (contre 1 460 en phase 1, +16 % pour
les sept corrections) [mesuré, `compte.py`] ; l'estimation des sous-lots restants de P2 (§7) est inchangée, avec cette
marge de correction de G2 à ajouter (≈ +15 %) [inféré].

### 10.8 Journal de provenance de la phase 2 (G1)

| niveau | source | sha256 | lu |
|---|---|---|---|
| [lu] | `ADJUDICATION-G2.md` | `d98f8639…e74f` | en entier (deux fois) |
| [lu] | `g2/RAPPORT-G2.md` | `b253aa11…f4ef` | en entier |
| [lu] | `BRIEF-P2B.md` | `0cc6ffe1…cd27` | en entier |
| [lu] | RFC 3161 du registre (`biblio/ietf-rfc3161-time-stamp-protocol-2026-10-04.txt`, hors suivi git) | `39fd1764…8240` (recalculé) | §2.2, l.150-183, relue à 03:36 UTC : vérifier l'empreinte, l'OID de l'algorithme, le nonce (ou l'heure), le certificat de la TSA et la signature, « If any of the verifications above fails, the TimeStampToken SHALL be rejected » ; les trois premiers sont contrôlés par `lier`, les deux derniers hors ligne (limite déclarée, FORMAT §15.2) ; §2.4.1, §2.4.2 lus en phase 1 |
| [lu] | `docs/adr-0028/ANNEXE-B-items.md` (dépôt réel) | — | forme des lignes (l.1051, l.1152) ; recherche des items cités dans ce seul fichier |
| [lu] | série P2A corrigée (`s2bis/p2a/diffs/`, `SHA256SUMS` `26548156…17f4`, `sha256sum -c` : 289 OK, 0 écart) | — | huit diffs appliqués ; tableau de la série dans `p2a/RAPPORT-GENERATEUR.md` (l.95-107) |
| [abs] | documentation du service d'horodatage de Certigna | — | non détenue, non lue (réseau interdit) : item SHOGEN-S2BIS-TSA-CERTIGNA-1 |
| [abs] | X.690 (DER), sortie de `chronyc` | — | comme en phase 1 |
| [lu] | sonde mémoire de la G2 (`g2/sondes/sonde_status_memoire.py`) | — | en tête (l.1-30) ; rejouée sur l'état final, cas 0 à 2 : code 0, 0,1 s, 23 Mio (avant : MemoryError en 9 s) (`travail2/preuves/sonde-memoire-g2-rejouee.txt`) |
| [mesuré] | réponses de TSA jetable (`openssl ts -reply`, OpenSSL 3.0.13, clé détruite) | `travail2/ref/c1/` | quatre `.tsr`, vérifiés par `openssl ts -verify` |

Commandes (sorties dans `travail2/preuves/`) : `rouges.py` (rouges) ; `campagne2.py` par `chaine2.sh` (mutants) ;
`job_etats.sh j2` (planchers) ; `final2.sh` (gates, matrice) ; `xtask2.sh` ; `finir2.sh` (diffs, série) ;
`variante.py`, `job_etats_variante.sh`, `final_variante.sh`, `campagne2v.py` par `chaine2v.sh` sur `mutants/variante/`,
`serie_variante.sh` (variante) ; `sonde_grille.py` (résiduel de C-3 ; corps égal au script lancé, en-tête ajouté
ensuite). Chiffres recomptés : lignes par `compte.py`, tests par la ligne `Ran`, planchers lus au
`gates.yml`, mutants comptés aux fichiers de résultat ; aucun chiffre de seconde main.

### 10.9 Nettoyage

Supprimés à 03:34:26 UTC : `p2b/final-variante/` (arbre complet, ex-`final-c58`), `p2b/temoin-c58/` (arbre complet du
témoin), `p2b/cargo-target/`, le contenu de `p2b/tmp/` et de `travail2/tmp/` ; place libre sur `/` : 4 897 → 5 099 Mo
(`df -m`, disque partagé). Aucun processus du lot ne reste (contrôlé par `ps`). Gardés, légers, pour la relecture :
`diffs/`, `diffs-apres-p2a/`, `diffs-v1-5cfe746/` ; `travail2/etats/` (t0 et les dix états de la série corrigée),
`travail2/etats-v1/` (série de la phase 1 sur c58b997), `travail2/variante/` (base P2A et états de la variante) :
mini-arbres `s2bis`, `enforcement`, `.github`, `docs/adr-0029/s2bis` ; `travail2/edits/`, `outils/`, `mutants/`,
`preuves/`, `ref/` (réponses de la TSA jetable, sans clé) ; `travail/` de la phase 1. `p2b/SHA256SUMS`, recalculé,
couvre ce rapport, `NOTES.md`, le brief, l'adjudication, les trois dossiers de diffs, `travail/` (outils, mutants,
preuves, références) et `travail2/` (éditions, outils, mutants, preuves, références, brouillons) ; contrôle :
`sha256sum -c SHA256SUMS` depuis `p2b/`.
