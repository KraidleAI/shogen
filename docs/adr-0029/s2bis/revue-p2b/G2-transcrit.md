# Relecture G2 de P2B (transcrit)

> Transcription par l'orchestrateur le 2026-10-09 06:28:34 UTC du fichier g2/RAPPORT-G2.md ; contrôle FM-1.1 des quatorze transcripts d'agents qui ont touché `s2bis/p2a` ou `s2bis/p2b` : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Relecture G2 neuve de P2B : CB-15 (têtes, export, RFC 3161) et CB-17 (commande `status`)

**Gate 0 : `claude-opus-5-5`** (réviseur G2 neuf, fiche `shogen-worker`, effort max). Je n'ai écrit aucun des diffs relus.

## Verdict : ACCEPTE-AVEC-CORRECTIONS

Liste fermée : **C-1 à C-4** (détail au §7).

| n° | où | défaut |
|---|---|---|
| C-1 | `tetes.py:235-238` | un `.tsr` d'une autre requête est gardé « émis », puis le jour n'est jamais redemandé |
| C-2 | `tetes.py:225`, borne `:211` | la tête propre peut tomber hors des 16 têtes lues : le jeton est alors refusé |
| C-3 | `status.py:98-99` | la grille dépend de valeurs lues sans contrôle : un chiffre faux fait allouer 1,5 Gio puis échouer |
| C-4 | voir §7 | cinq mutants du réviseur restent vivants sous la commande du job |

Le reste du lot est tenu, preuves au §1 :
- la requête RFC 3161 est égale à l'octet à celle d'OpenSSL ;
- les têtes sont exportées et consignées ;
- `status` n'imprime que la santé, ne décode aucune lecture et n'écrit rien ;
- les 11 états de la série sont conformes à leur plancher exact ;
- la matrice 3.10 à 3.13 est verte, ainsi que S2, sim-bis et le runner ;
- xtask rend les mêmes lignes que le témoin.

## 0. Base, horloge, pièces

- **Horloge** : relecture ouverte le 2026-10-08 à 21:02:36 UTC, rapport écrit à partir de 21:59 UTC.
- **Pièces du générateur** :
  - `p2b/SHA256SUMS` : 201 lignes, `sha256sum -c` sans aucun écart ;
  - sha256 du fichier SHA256SUMS : `201702ce…eb782` ;
  - diffs copiés dans `g2/diffs-copie/`, empreintes égales à celles de SHA256SUMS.
- **Base 5cfe746** :
  - deux extractions neuves par `git --no-optional-locks archive` : sept exclusions par pathspec, et les mêmes par `tar --exclude` ;
  - les dossiers exclus sont absents des extractions ;
  - les 10 diffs passent `git apply --check` puis `git apply` sur la première, `patch -p1 --dry-run` puis `patch` sur la seconde, sans aucun rejet ;
  - les 9 fichiers touchés ont le même sha256 dans les deux arbres.
- **La tête du dépôt a avancé pendant la relecture** : 5e386c4 à l'ouverture, c58b997 à 21:56 (PR #1 à #4, README).
  - De 5cfe746 à c58b997, sur `s2bis/`, `enforcement/`, `.github/` et `docs/adr-0029/s2bis/`, seul `gates.yml` change (ligne sim-bis : plancher 172 → 194).
  - Les 10 diffs passent `git apply` sur 5e386c4 et sur c58b997, sur une extraction des seuls chemins touchés.
  - Les 8 fichiers obtenus sont égaux à ceux de l'arbre final. Seule la ligne sim-bis diffère.
- **Contrat lu** : brief ; G0 et ses ajouts datés ; PROPOSITION §2.2, §2.4, §2.6, §4.2 et Q-D-03 ; AVIS en entier (il prime, Q-D-03 points 1 à 3) ; ADR-0029 aux lignes et ajouts datés utiles ; FORMAT ; RFC 3161 du registre ; scripts du sceau. Le détail est au §12.
- **Annexe B** : recherche de « CB-15 » et « CB-17 » dans ce seul fichier. Un seul item a l'un d'eux pour déclencheur : SHOGEN-S2BIS-CHRONYC-FORMAT-1 (l.1051).

## 1. Exigences et items : tenue, code et test qui la fige (contrôle 1)

Les numéros de ligne renvoient à l'arbre final, base plus les 10 diffs.

| exigence | tenue | code | test qui la fige ; preuve du réviseur |
|---|---|---|---|
| E-C-35 : tête exportée à chaque point de contrôle | oui | `boucle.py:120-128` ; `tetes.py:177-185`, `106-124` | `test_tetes.py:232`, `:149`, `:162`, `:435` ; S-4 : tête recalculée sur les octets du point, égale |
| E-C-35 : têtes des autres consignées dès leur lecture | oui | `boucle.py:122` (`tetes` avant `sante`) ; `tetes.py:148-214` | `test_tetes.py:181`, `:202`, `:232`, `:251` ; S-4, S-6 |
| E-C-36 : requête construite en bibliothèque standard | oui | `tetes.py:44-63` | `test_tetes.py:64` (octets d'`openssl ts -query -no_nonce`), `:71`, `:74`, `:81` ; S-1 : 24 sur 24 |
| PROPOSITION §2.4 « Jeton » : mutants certReq absent et algorithme faux | oui | `tetes.py:56-63` | mutants M-15a du générateur ; G-11, G-12 tués |
| E-C-36 : `.tsr` conservé, sha256 journalisé | oui, mais **C-1** (liaison non contrôlée) | `tetes.py:217-238` ; `:187-203` (`jeton` au `tetes`) | `test_tetes.py:298`, `:316` |
| E-C-36 : envoi armé par un paramètre que seul le go autorise | oui (Q-7) | `entree.py:128` (`--envoi`) ; `tetes.py:241-260` | `test_tetes.py:357`, `:329` ; **C-4** pour le contexte TLS (G-17) |
| AVIS Q-D-03 (1) : sa tête chaque jour, celles des autres en plus | **partiel, C-2** | `tetes.py:225-227` | `test_tetes.py:298` ; KO-1 de S-5 |
| AVIS Q-D-03 (2) : résumé par fenêtre, liste blanche, projection du journal | oui | `status.py:111-118` ; `entree.py:152-154` | `test_status.py:247`, `:342` |
| AVIS Q-D-03 (3) : compte local toujours, compte à quorum avec l'âge des résumés | oui (robustesse : **C-3**) | `status.py:144-192` | `test_status.py:265`, `:285`, `:311`, `:319`, `:327` ; S-8 bis (quorum calculé à la main) |
| E-C-38, ADR l.244 et l.246 : santé seule (D-1 à D-5, dernier marqueur, tête, disque) et compte par strate | oui, **D-3 non jugé** (item CHRONYC) | `status.py:42-108`, `172-192` | `test_status.py:110`, `:183`, `:195` ; S-7 |
| PROPOSITION §2.4 « Status » : même sortie avec et sans lectures | oui | `status.py:52-53` | `test_status.py:201`, `:81` ; G-29 tué ; S-7 (chaîne canari jamais imprimée) |
| Brief CB-17 : `status` n'écrit rien | oui | `status.py` sans écriture ; `entree.py:149-151` | `test_status.py:209` ; S-8 et S-8 bis (voir la note) |
| E-C-26, E-R-05, E-R-06 : jugement aux seuils scellés, M_j ≥ 2 | oui pour D-2, D-4 et D-5 | `status.py:30`, `71-82`, `165` | `test_status.py:110`, `:125` (égalité à `analyse.json`) ; G-20, G-21, G-27 tués |
| Strates par le calendrier du week-end UTC | oui | `status.py:107-108` | `test_status.py:195` ; G-25 tué |
| SHOGEN-S2BIS-ECRIVAIN-REFUS-ARRET-1 : un dépôt hostile ne fait jamais refuser `tetes` | oui | `tetes.py:148-203` | `test_tetes.py:202` |
| Aucune requête réseau ; fixtures seules | oui | — | garde réseau des tests ; toutes mes exécutions sous `unshare -n` |
| SHOGEN-S2BIS-CHRONYC-FORMAT-1 (l.1051) | **non fermé, rendu en limite I-1** | « D-3 non jugé » (`status.py:188-189`) | `test_status.py:110` ; sources absentes, vérifié (§9) |

Note sur S-8 et S-8 bis : sont relevés les noms, tailles, mtime, modes et inodes du journal et du dépôt. Aucun `.verrou` n'est créé. `status` rend en 0,08 s quand un autre processus tient le verrou. Dossiers en 0555, fichiers en 0444, sans capacité (`unshare -U`) : sortie 0.

## 2. Sonde du réviseur, écrite d'après le contrat seul (contrôle 2)

Les attentes ont été écrites dans NOTES à 21:07, avant toute lecture du code. Seules les lignes `def` et `add_parser` étaient relevées.

| sonde | attendu (source) | résultat |
|---|---|---|
| S-1 requête | DER de RFC 3161 §2.4.1, entiers minimaux ; égal à `openssl -no_nonce` | **24/24** : égalité avec mon encodeur et avec openssl ; nonces 0, 0x7f, 0x80, 0xff, 2^63 et 2^64−1 relus par openssl ; −1, 2^64, booléen et empreinte fausse refusés |
| S-2 réponse | rejet de toute réponse qui n'est pas celle de la requête (RFC 3161 §2.2, §2.4.1) | `statut` rend 0 pour un `.tsr` d'une **autre empreinte**, d'un **autre nonce** et d'un **genTime forgé en 2001** ; `openssl ts -verify` les refuse tous les trois. Les cas mal formés donnent un refus nommé `JETON/reponse`. Voir C-1 |
| S-3 armement | sans armement, rien ne part | tenu (`entree.py:128`) |
| S-4 export | tête = (seq, sha256 de la ligne du `point`) | tenu, recalculé sur les octets |
| S-5 jeton | sa tête toujours au manifeste | **KO** : 16 têtes de noms antérieurs, puis `JETON/tete` (C-2) |
| S-6 dépôt hostile | aucun blocage, rien hors du dépôt, jamais la tête d'un autre prise pour la sienne | tenu, avec deux constats (§3) |
| S-7 lectures | aucune lecture lue ; même sortie avec et sans | tenu |
| S-8 écriture | aucun effet d'écriture | tenu |
| S-9 seuils | 5 s pile valide, 5 s + 1 µs D-2 ; 1 témoin muet valide, 2 D-4 ; 1 nom en échec valide, 2 D-5 | tenu (codes écrits à la main) |
| S-10 quorum | M_j ≥ 2, âge imprimé | tenu |
| S-11 journal dégradé | jamais de trace Python ni de blocage | **KO** : un chiffre corrompu fait échouer `status` (C-3) ; un tube nommé dans le journal le bloque (constat O-4) |

## 3. Leurres du réviseur (contrôle 3)

**Têtes, export et jeton** (`sonde_tetes.py`, `sonde_tsr.py`) :

| leurre | résultat |
|---|---|
| tube nommé, socket UNIX, lien vers `/dev/zero` au nom d'une tête | `TETES/lecture`, sans blocage (0,000 s) |
| fichier creux de 8 Gio | `TETES/taille` |
| tête propre usurpée au dépôt | jamais relue |
| nom en O cyrillique | ignoré |
| lien vers un fichier hors du dépôt contenant une tête valide | suivi et lu (O-1) |
| « o2 » et « O2 » | comptés comme deux observateurs (O-2) |
| manifeste et ordre | triés par (observateur, journal) quel que soit l'ordre lu (G-10 tué) |
| 16 têtes de noms antérieurs | **la sienne n'est pas lue** (C-2) |
| `.tsr` d'une autre empreinte, `.tsr` rejoué (autre nonce) | gardés « émis », puis « déjà émis » ; openssl : ÉCHEC (C-1) |
| genTime hors du jour | admis : constat (le nonce suffit à la fraîcheur, RFC 3161 §2.2) |
| `.tsr` tronqué, vide, octet en trop, statut 3 avec jeton | `JETON/reponse` (openssl, lui, admet l'octet en trop) |
| lien posé au nom du fichier temporaire | cible intacte (test `:435`, CB-15f) |

**`status`** (`sonde_status.py`, `sonde_status_memoire.py`, `sonde_status_depot.py`) :

| leurre | résultat |
|---|---|
| dernière ligne déchirée | même rapport, hors tête |
| santé incohérente (`d4` null, `retard_max` en texte, `d5` absente) | jamais valide (D-1) |
| fichier du journal illisible (0000, sans capacité) | refus nommé, sortie 1 |
| dossiers en lecture seule, verrou de l'écrivain tenu ailleurs | sortie 0, rien d'écrit |
| `ws` d'un marqueur corrompu (2 → 9), JSON valide | **MemoryError en 9,0 s à 1 519 Mio** (borne de 1,5 Gio ; délai de 30 s dépassé sans borne) (C-3) |
| `suivante` ramenée à 2001, même longueur | **MemoryError en 9,8 s à 1 516 Mio** (C-3) |
| témoin sain | 0,1 s, 21 Mio |
| première ligne d'un fichier illisible | le fichier entier est ignoré sans le dire (O-3) |
| tube nommé au nom d'un fichier du journal | bloque, comme l'écrivain de P1 (O-4) |

## 4. Mutants (contrôle 4)

**Campagne du réviseur** :
- outil `travail/outils/campagne.py`, écrit par moi ;
- commande exacte du job, lue au `gates.yml` de chaque copie : `python3.12 -B enforcement/tests/run-fixtures-verdict-suite-s2.py`, puis `python3.12 -B enforcement/verdict-suite-s2.py s2bis --aucun-saut --egal --plancher 294` ;
- borne de 300 s par étape, réseau isolé ; témoin VIVANT (Ran 294) ; de 21:26:38 à 21:45:49.

| bilan | mutants |
|---|---|
| **30 mutants** : 25 TUÉS, tous par la ligne s2bis (runner à 0), chacun par son test visé quand il en a un | G-01 à G-30 |
| **5 VIVANTS**, **0 FATAL** | G-01, G-03, G-04, G-16, G-17 |

Détail des cinq vivants :

| mutant | où | mutation |
|---|---|---|
| G-01 | `tetes.py:235` | statut 1 refusé |
| G-03 | `tetes.py:248` | envoi http sans délai |
| G-04 | `tetes.py:253` | `r.read()` sans borne |
| G-16 | `entree.py:130` | nonce constant |
| G-17 | `entree.py:128` | contexte TLS non transmis : https refusé, http admis en production |

Ils donnent C-4.

**Campagne du générateur** : 150 tués sur 150 dans ses fichiers, 0 vivant, 0 FATAL, témoin VIVANT à chaque campagne.
- Son outil ajoute `-X dev -W error` au runner et au vérificateur. Ces options ne passent pas au sous-processus de la suite.
- J'ai reclassé par la commande exacte sept de ses mutants qui touchent fermetures, fsync ou lectures de fichiers : M-15b-02 et M-15b-03 (état CB-15b) ; M-15f-02, -05, -08, -10 et -13 (état final).
- Résultat : **7 sur 7 tués** par leur test visé. Son classement tient.

## 5. Gates (contrôle 5)

| contrôle | résultat |
|---|---|
| ligne s2bis de chaque état, `--egal`, python3.12 | e0 à e10 : 255, 262, 266, 270, 272, 274, 279, 284, 286, 289, 294 : **11 conformes** |
| matrice 3.10, 3.11, 3.12, 3.13, `-X dev -W error`, `unittest discover` | 294 OK sous les quatre ; « Warning » 0 ; « Exception ignored » 0 |
| ligne du job sous les quatre interpréteurs, `-X dev -W error` | conforme, Ran = 294 |
| runner | 136 ok, 0 échec |
| S2 (`--egal`) | Ran 415, conforme ; deux sauts nommant `SHOGEN_S2_CAMPAGNE_CONTROL`, jamais posée |
| sim-bis (plancher 172 à 5cfe746) | Ran 172, conforme. Objets git du dépôt réel lus par `GIT_DIR`, en lecture seule, `GIT_OPTIONAL_LOCKS=0`. `git status` du dépôt resté vide |
| `__pycache__` sous `s2bis/` | 0 |
| `cargo --locked xtask verify`, série et témoin t0, réseau isolé | lignes de verdict identiques : S-G1 à S-G8, fmt, no_std et clippy VERTS ; **S-G9 ROUGE seule, `docs/17-modele-de-menace.md:70`** (connue sur les copies) |
| rouges rejoués | CB-15a : squelette du générateur et test livré, 7 FAIL, 0 ERROR, puis 7 OK. CB-17a : 5 FAIL, puis 5 OK. CB-15f : code de l'état CB-17d avec les tests livrés, 5 FAIL, 0 ERROR, puis 39 OK |

## 6. Forme (contrôle 6)

- **R-25** : lignes de code et de tests ajoutées par diff : 178, 197, 96, 114, 119, 191, 182, 94, 139, 140, plus 1 ligne de CI chacun. Tous sont sous 200, et ces nombres sont égaux à ceux du générateur. Les documents sont hors compte.
- **METRIQUES** : la forme est celle de P1 (objet, rouge, tableau, mutants, suite et plancher). Lignes et nombre de tests sont égaux à mes relevés, état par état.
- **R-13** : aucun `TODO`, `FIXME` ni `XXX` ajouté.
- **R-8** : imports neufs de la bibliothèque standard seulement (`contextlib`, `hashlib`, `http.client`, `urllib.parse`, `stat`, `secrets`, `calendar`, `time`, `json`, `os`, `re` ; en test, `signal`, `http.server`, `threading`). `test_fitness` est vert.
- **Octet 92** : seulement dans des littéraux `\n` et `\xff` (`tetes.py:63` : certReq), contrôlés sur les octets par S-1.
- **120 caractères** : aucune ligne ajoutée au-delà.
- **xtask** : voir §5.

## 7. Corrections (liste fermée)

**C-1 : le jeton n'est pas lié à la requête** (`tetes.py:235-238`, `jeton` ; FORMAT §15.2 l.562-567 et §15.7 l.593-600).

- **Preuve.**
  - Une réponse accordée, produite par une TSA locale du réviseur pour une autre empreinte, ou pour le même manifeste avec un autre nonce, est gardée en `.tsr` sous l'état « émis » (`sonde_tetes.py`, KO-2 et KO-3).
  - L'appel suivant rend « déjà émis » (`tetes.py:223-224`) : le jour n'est jamais réhorodaté.
  - `openssl ts -verify -queryfile` refuse les deux réponses ; `statut` rend 0 (`sonde_tsr.py`).
- **Norme.** RFC 3161 du registre (`39fd1764…8240`) :
  - §2.2, l.157-183 : « the requesting entity SHALL verify … the correct data imprint … the nonce … If any of the verifications above fails, the TimeStampToken SHALL be rejected » ;
  - §2.4.1, l.267-272 : sur le nonce, « otherwise the response shall be rejected » ;
  - E-C-36 demande un jeton **sur le manifeste**. Le générateur a lu §2.4.1, §2.4.2 et §3.4, mais pas §2.2.
- **Remède.**
  - Avant `ecrire(.tsr)`, lire au TSTInfo l'algorithme (SHA-256), l'empreinte (sha256 du manifeste) et le nonce (celui de la requête), pour un statut de 0 ou de 1.
  - Tout écart, ou tout chemin DER illisible, donne un refus nommé, et rien n'est conservé. La signature reste vérifiée hors ligne (limite déclarée).
  - Tests sur des réponses d'`openssl ts -reply` d'une TSA jetable : réponse juste, autre empreinte, autre nonce, sans nonce.
  - Réécrire FORMAT §15.2 et §15.7.
  - Mutants : contrôle d'empreinte retiré, contrôle de nonce retiré.
  - Faisabilité vérifiée : prototype de 15 lignes avec `_element` du lot (`sondes/prototype_c1.py`) : réponse juste gardée, autre empreinte refusée, autre nonce refusé.

**C-2 : l'ancrage propre dépend des fichiers des autres** (`tetes.py:225`, `lues = lire_tetes(dossier)[0]`, avec la borne `NOMBRE` de `tetes.py:211`).

- **Preuve.** Seize fichiers `A00-pool.tete` à `A15-pool.tete`, puis `O1-pool.tete` : `jeton(…, "O1", …)` rend `JETON/tete` (KO-1).
- **Contrat.** L'AVIS Q-D-03 (1), qui prime, dit que la tête propre est « ancrée quoi qu'il arrive à la lecture croisée ».
- **Remède.**
  - Lire d'abord les fichiers de tête de l'observateur, hors borne, puis au plus 16 têtes des autres.
  - Test : 16 têtes de noms antérieurs et la sienne ; la sienne est au manifeste.
  - Mutant : borne appliquée à ses têtes.
  - Ferme la limite I-8 du générateur.

**C-3 : la grille de `status` n'est pas bornée** (`status.py:98-99`, `etat`, et donc `resumes`, `status.py:111-118`, et la commande `resume`).

- **Preuve.**
  - Un `ws` de marqueur ou une `suivante` corrompus d'un chiffre, en JSON valide, font allouer `range(debut, max(juges) + W, W)`.
  - Sous une borne de 1,5 Gio : MemoryError en 9,0 s et en 9,8 s, à 1 519 et 1 516 Mio de pic. Le témoin sain prend 0,1 s et 21 Mio. Sans borne, l'appel dépasse le délai de 30 s.
  - `status`, outil de l'investisseur, échoue alors sur l'observateur même où tourne le collecteur. Seul le processus secondaire a un `MemoryMax` (E-D-09).
- **Remède.**
  - Borner la grille par les noms de fichiers. FORMAT §6.1 : aucune fenêtre n'est d'un jour postérieur à celui de son fichier. Un `ws` ou une `suivante` au-delà de la fin du jour du fichier est une ligne illisible, et le fichier s'arrête.
  - Ne jamais commencer avant le jour du premier fichier présent, moins un jour pour un segment de reprise.
  - Tests : les deux journaux corrompus de `sonde_status_memoire.py` ; sortie 0 en moins de 2 s ; rapport borné.
  - Mutant : borne retirée.
  - Ferme la part « gonfler la grille » de la limite I-3 du générateur.

**C-4 : tests manquants, cinq mutants du réviseur vivants sous la commande du job.** Chaque mutant doit être tué par un test nommé, puis rejoué par la commande du job.

| mutant | test à ajouter |
|---|---|
| G-01 (`tetes.py:235`) | une réponse au statut 1 est conservée (FORMAT §15.7 le dit) |
| G-03 (`tetes.py:248`) | une TSA de boucle locale qui accepte et ne répond pas, avec un `delai` court : erreur en temps borné (le rapport, I-6, dit « envoyer borne connexion et lecture (10 s) ») |
| G-04 (`tetes.py:253`) | une réponse annoncée à 10^9 octets, 65 537 envoyés puis silence : `JETON/http` immédiat |
| G-16 (`entree.py:130`) | deux `jeton` non armés : nonces différents dans les `.tsq` (Q-5) |
| G-17 (`entree.py:128`) | `main` sans `tls=` transmet un `ssl.SSLContext` à `envoyer`, et `--envoi http://…` sort en 1 avec `JETON/url` |

## 8. Avis sur les questions du générateur (contrôle 7)

- **Q-1 Place de `tetes`** : d'accord. Un enregistrement de fenêtre garde les invariants de l'écrivain (ws non décroissant, avant le marqueur), et l'export après le point exporte la tête du point. Un type hors fenêtre demanderait un type réservé neuf.
- **Q-2 E/S du dépôt dans la boucle** : d'accord avec sa recommandation.
  - Écrire au FORMAT §15 que le dépôt passé à `pool --depot` est un dossier **local**, synchronisé par une unité séparée (DB-4).
  - Motif : E-C-15 interdit une tâche bloquante sur le fil de la boucle, et un montage réseau pendu bloquerait `listdir` et `open` malgré `O_NONBLOCK`.
- **Q-3 Forme du dépôt** : dossier plat, à confirmer à DB-0 avec la lecture croisée de la Storage Box. La synchronisation peut aplatir des sous-comptes. Sans objection.
- **Q-4 Manifeste** : d'accord (toutes les têtes valides, triées), sous C-2 : les siennes toujours.
- **Q-5 Nonce** : 64 bits, conforme à l'exemple de RFC 3161 §2.4.1.
  - Le figer par test (G-16).
  - Journaliser aussi les sha256 du `.tsq` et du `.manifeste` au `tetes`, pour que la chaîne ancre la requête faite (O-7).
- **Q-6 Contrôle de la réponse** : **pas d'accord** pour l'empreinte et le nonce (C-1). D'accord pour la signature hors ligne (aucune vérification RSA ou ECDSA en bibliothèque standard), en limite déclarée.
- **Q-7 Armement** : `--envoi` est simple et testé. Je recommande que l'URL vive dans une configuration scellée, et que l'état d'armement se lise au dépôt ou au journal (auditable). Choix de déploiement, à l'orchestrateur.
- **Q-8 Nom d'observateur** : resserrement admis avant le gel. Je recommande `[a-z0-9]{1,16}` ou une liste fermée des quatre noms dans la configuration scellée, contre les jumeaux de casse (O-2) et les résumés étrangers (O-8).
- **Q-9 D-3 non jugé** :
  - affichage admis tant que l'item CHRONYC est ouvert, avec la mention « hors D-3 » sur les lignes « fenêtres valides » et « quorum » (O-6) ;
  - le gel du collecteur ne doit pas précéder la fermeture de l'item, dont le déclencheur dit « avant le gel ».
- **Q-10 Définitions de D-4 et D-5** : d'accord. RB-3 doit importer ces définitions ou les recouper par un test croisé, comme les seuils (`test_status.py:125`).
- **Q-11 Lecture reconnue à ses premiers octets** : admis. Le test `test_status.py:81` construit les lignes par `Lecture.enregistrement()` réel, si bien qu'une clé future triée avant `adresse` le ferait échouer.
- **Q-12 Fréquence des résumés** : au déploiement. Je recommande l'heure, après le point, alignée sur l'export de la tête.

## 9. Limites, écarts et item du générateur

**Limites rendues** :
- **I-1 CHRONYC-FORMAT-1** : rendu légitime. Chrony est absent de l'hôte, je n'en ai trouvé aucune documentation locale (`which`, `/usr/share/doc`, `dpkg`), et le réseau est interdit. L'item reste ouvert et son déclencheur « avant le gel » tient. À DB-0 : lecture sur pièce et sortie gelée.
- **I-2 Rétention** : d'accord ; les résumés publiés peuvent servir de mémoire.
- **I-3 Journal hors FORMAT** : pour partie dans C-3 ; le reste (types par enregistrement) en item.
- **I-4 Tête du secondaire** et **I-5 Bout en bout avec dépôt** : items d'intégration, d'accord.
- **I-6 DNS de l'envoi** : d'accord. Ajouter que le délai est compté par opération et non au total : une TSA au goutte-à-goutte tient la commande (O-5).
- **I-7 Un écrivain par nom** : d'accord ; C-1 ferait refuser un `.tsr` croisé.
- **I-8** : devient C-2.

**Écarts déclarés** :
- E-1 à E-5 sont déclarés et sans effet sur les livrables.
- E-1 et E-3 sont contraires à la lettre « même sur tes copies », mais aucune liste n'a été affichée ni aucune recherche faite.
- Non déclaré, et sans effet : `-X dev -W error` ajoutés à la commande des campagnes. Voir §4 : le classement tient sur les sept mutants reclassés.

## 10. Items à former (proposés par le réviseur, règle PAROXYSME)

- **O-1 SHOGEN-S2BIS-DEPOT-LIENS-1** : les lectures du dépôt suivent les liens symboliques. La lecture est bornée et seul un contenu à forme de tête est retenu. Envisager `O_NOFOLLOW` si le dépôt n'est pas strictement local.
- **O-2 et O-8 SHOGEN-S2BIS-OBSERVATEURS-LISTE-1** : noms sensibles à la casse ; le quorum compte tout nom d'observateur trouvé dans un résumé. Liste fermée des observateurs dans la configuration scellée.
- **O-3 SHOGEN-S2BIS-STATUS-QUEUES-1** : `status` arrête un fichier à sa première ligne illisible sans le dire, et les fenêtres disparaissent du rapport. Imprimer le nombre de fichiers arrêtés avant leur fin.
- **O-4 SHOGEN-S2BIS-JOURNAL-FICHIER-SPECIAL-1** : un tube nommé au nom d'un fichier du journal bloque `status`, comme il bloquerait la reprise de l'écrivain de P1.
- **O-5, avec I-6, SHOGEN-S2BIS-ENVOI-ECHEANCE-1** : échéance totale de l'envoi (DNS compris), dans le code ou dans l'unité systemd de `jeton`.
- **O-6** : mention « hors D-3 » sur les lignes de compte (Q-9).
- **O-7** : sha256 du `.tsq` et du `.manifeste` au `tetes` (Q-5).
- **Q-2** : le dépôt local écrit au FORMAT et à DB-4.

## 11. Écarts du réviseur

- **E-R1** : un `find <copie serie> -maxdepth 4 -name '*.orig' -o -name '*.rej'` sur ma copie entière. Noms seulement, sortie vide. Non refait.
- **E-R2** : `cp -a` de `docs/adr-0029/s2bis` dans mes mini-arbres d'états, et `find s2bis -name __pycache__` sur ma copie. Ce sont des copies et un compte, sans recherche dans `docs/`.
- **E-R3** : `GIT_DIR` du dépôt réel, en lecture seule, pour l'oracle de sim-bis (`git archive`, sans verrou), comme le générateur.
- **E-R4** : une commande a été bloquée par un contrôle de sûreté du harnais (script `sh -c`), et je l'ai réécrite sans `sh -c` (outils `isole.sh` et `apres_lo.sh`).
- **E-R5** : trois heures de NOTES écrites d'abord par estimation, puis corrigées sur l'horloge et les mtime des preuves.
- Aucune pièce de D.2 ouverte, aucun `*.jsonl` réel, `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée, aucun appel réseau réel (tout sous `unshare -n`), aucune écriture git ni sous `.claude/` du dépôt.

## 12. Journal de provenance (G1)

| niveau | source | sha256 | lu |
|---|---|---|---|
| [lu] | brief `p2b/BRIEF-P2B.md` | `0cc6ffe1…b565cd27` | en entier |
| [lu] | G0 `G0-COLLECTE-RECALC-DEPLOI.md` | `0e9001f3…e8352a90` | en entier |
| [lu] | PROPOSITION | `0cdf84c2…865fbfd0` | en entier (§2.2, §2.4, §2.6, §4, Q-D-03) |
| [lu] | AVIS | `a919b307…421616ce` | en entier |
| [lu] | ADR-0029 | `35563d8f…2f659eb8` | l.158, l.194-198, l.218-246, l.397 ; liste des ajouts datés |
| [lu] | FORMAT (5cfe746) | `178041f2…2c4e6dc8` | en entier ; FORMAT final §15 et §16 par les diffs |
| [lu] | METRIQUES (5cfe746) | `f1761ea4…2ebc4ca9` | sections de forme (RB-18i, RB-1l) |
| [lu] | annexe B | `3f738722…d7a5d0d2` | recherche dans ce seul fichier ; l.120-127, l.519, l.1051 |
| [lu] | annexe D | `deb64179…b5690eaf` | l.32-47 (liste D.2), sans ouvrir aucune pièce |
| [lu] | `scripts/sceau/make-tsq.sh`, `verify.sh` | `ef66fe83…6e18d3c5`, `b6f7b66a…1962d166` | en entier |
| [lu] | RFC 3161 (`biblio/` du dépôt réel, hors suivi git) | `39fd1764…3eb98240` (égal à INDEX l.356) | l.150-183 (§2.2), l.213-382, l.560-580 |
| [lu] | `biblio/INDEX.md` | `593b96de…df15c3d6` | l.1-12, l.356 |
| [lu] | `s2bis/config/analyse.json` | `e9243c79…233a1d00` | bloc `degradation` |
| [lu] | code de P1 : `journal.py`, `entree.py`, `sante.py`, `boucle.py` ; aides de tests | `a39ab0dc…`, `403987d4…`, `2afee71a…`, `daf4b1c1…` | en entier ; aides `Temps`, `borne`, `chaine` |
| [lu] | diffs 01 à 10, en entier ; `tetes.py` et `status.py` finals | sha256 de SHA256SUMS | à 100 % |
| [lu] | rapport et NOTES du générateur | `793f3184…7f7b3528` | après ma lecture propre, puis confrontés |
| [abs] | X.690 | — | règles DER appliquées de mémoire ; contrôlées par openssl (S-1) |
| [abs] | documentation et sortie de `chronyc` | — | absentes de l'hôte |

**Commandes et sorties** (complètes dans `g2/preuves/`) :

| commande | preuve |
|---|---|
| sondes S-1 à S-11, S-8 bis, prototype de C-1 | `sonde_*.txt`, `prototype_c1.txt` |
| états e0 à e10 | `etats-bilan.txt`, `etat-e*.txt` |
| campagnes | `campagne-g2.txt`, `reclasse-*.txt` |
| matrice, S2, sim-bis, runner | `serie-*.txt`, `gates-serie.txt` |
| xtask | `xtask-*.txt` |
| rouges rejoués | `rouge-rejoue-*.txt`, `vert-rejoue-*.txt` |

Chiffres recomptés par moi : lignes par diff, `wc -l`, `def test_`, `Ran`, mutants, mémoire et durées ; aucun chiffre de seconde main.

## 13. Fichiers produits

Dossier `…/s2bis/p2b/g2/` :
- `RAPPORT-G2.md`, `NOTES.md` ;
- `diffs-copie/` (les 10 diffs relus) ;
- `sondes/` (7 sondes et la TSA de test ; clés privées détruites en fin de relecture) ;
- `travail/outils/` (isolement, états, campagne, mutants, reclassement, gates, xtask) ;
- `preuves/` (49 fichiers) ;
- `etats/` (mini-arbres e0 à e10 et e2full).

Copies lourdes supprimées en fin de relecture : `travail/t0`, `travail/serie`, `travail/serie-ga`, `cible-cargo`, `tmp`.

Les numéros de ligne de ce rapport renvoient à l'arbre final. Son `s2bis/` est gardé à l'identique dans `etats/e10/` (contrôlé par `cmp` sur les six fichiers touchés). Les diffs se rejouent sur 5cfe746 par `git apply`.

Empreintes : `g2/SHA256SUMS` (contrôle : `sha256sum -c SHA256SUMS` depuis `g2/`).
