# Contrôles de registre R-8 — outillage

Registre de la **moitié humaine** de R-8, telle qu'ADR-0012 D5 la définit :
toute dépendance directe nouvelle entre par une PR qui porte son contrôle de
registre écrit — existence sur le registre officiel, ancienneté, mainteneurs,
téléchargements — **avant** installation, jamais après. La moitié mécanique est
`cargo-deny` (gate S-G7) et ne dispense pas de celle-ci.

Périmètre de ce fichier : les **outils** (installés par `cargo install`, hors
graphe de dépendances du workspace). Les dépendances qui entrent au graphe
portent leur contrôle au manifeste, à côté de la ligne qu'elles occupent —
c'est le cas de `proptest` dans `crates/shogen-core/Cargo.toml`.

Méthode, identique pour chaque ligne : interrogation de l'API publique de
crates.io (`/api/v1/crates/<nom>` et `/api/v1/crates/<nom>/owners`), champs
recopiés de la réponse. Aucun chiffre de seconde main.

## Outils contrôlés

| outil | version retenue | licence | mainteneurs (owners) | téléchargements cumulés | 1re publication | contrôle du | usage |
|---|---|---|---|---|---|---|---|
| `cargo-deny` | 0.20.2 (épinglée dans `squelette.yml` ; non yanked, 430 714 téléchargements de la version) | MIT OR Apache-2.0 | `embark-studios` (organisation) | 4 990 660 | 2019-05-13 | **2026-08-13 (trace reconstituée par l'orchestrateur, API crates.io — l'écart « déclaré au JOURNAL du 2026-08-12 sans trace au dépôt » reste consigné ci-dessous)** | gate S-G7 (licences, bans, sources, advisories) |
| `cargo-llvm-cov` | 0.8.7 (mesurée par `cargo llvm-cov --version` le 2026-08-13 ; non yanked, 1 090 683 téléchargements de la version) | Apache-2.0 OR MIT | `taiki-e` — propriétaire unique (même borne que `cargo-mutants` : version exacte, hors graphe livré, CI en lecture seule) | 7 148 919 | 2021-01-22 | **2026-08-13 (trace reconstituée par l'orchestrateur, API crates.io — même écart consigné)** | couverture par rôle (ADR-0011 seuil 1) |
| `cargo-mutants` | **27.1.0** | **MIT** | **`sourcefrog` (Martin Pool) — propriétaire unique** | **466 076** (dont 164 607 sur 90 jours) | **2021-10-25** | **2026-08-13 (S3 phase C)** | score de mutation du cœur (ADR-0011 seuils 3 et 4) |
| `cargo-fuzz` | **0.13.2** (non yanked, 665 687 téléchargements de la version, publiée le 2026-06-09 ; 40 versions publiées) | **MIT OR Apache-2.0** | **`frewsxcv`, `fitzgen`, `nagisa`, `Manishearth`, équipe `rust-fuzz:publishers`** | **4 050 192** | **2017-02-21** | **2026-08-13 (S3 phase C, chantier fuzz instrumenté — re-mesuré AVANT installation)** | pilote libFuzzer (job CI `cargo-fuzz`, nightly épinglée par date) |
| `cargo-afl` | **0.18.2** (non yanked, 22 771 téléchargements de la version, publiée le 2026-05-11 ; 45 versions publiées) | **Apache-2.0** (seule) | **`smoelius`, `anishnaik`, équipe `rust-fuzz:publishers`** | **195 418** (dont 26 713 récents) | **2023-03-27** | **2026-08-13 (S3 phase C, chantier fuzz instrumenté — AVANT installation)** | pilote AFL++ (job CI `cargo-afl`, stable du dépôt) |

**L'écart « trace non retrouvée », consigné puis comblé.** Le JOURNAL
du 2026-08-12 écrit « R-8 documenté pour proptest/cargo-deny/cargo-llvm-cov »,
et `docs/12` §5 écrit « R-8 documenté par outil ». La recherche au dépôt du
2026-08-13 (`grep -rn "R-8"` sur `docs/`, `*.toml`, `*.rs`, `*.yml`) ne trouve
le détail — existence, ancienneté, mainteneurs, téléchargements — que pour
**`proptest`**, en commentaire de `crates/shogen-core/Cargo.toml`. Les deux
autres étaient affirmés, pas écrits — un contrôle R-8 qu'on ne peut pas
relire n'est pas un contrôle R-8 (ADR-0012 D5, moitié humaine : « une PR qui
**porte** son contrôle de registre écrit »). Les deux traces ont été
**reconstituées le 2026-08-13 par l'orchestrateur** (interrogation API
crates.io, champs recopiés des réponses — lignes du tableau ci-dessus) ;
l'écart de déclaration du 2026-08-12, lui, reste un fait de la passe S2.5
et ne s'efface pas.

Le même écart existe sur `cargo-mutants` en sens inverse : `docs/12` ligne 386
et `docs/13` ligne 96 écrivent tous deux « R-8 fait » **au passé**, alors
qu'aucune trace n'existait au dépôt avant ce fichier. Le contrôle a donc été
fait le 2026-08-13, avant installation, et c'est cette ligne-ci qui le porte.

Compléments mesurés sur `cargo-mutants` le 2026-08-13 : 71 versions publiées ;
`rust_version` déclarée par la version retenue = 1.88, satisfaite par la
toolchain épinglée du dépôt (1.97.1, `rust-toolchain.toml`) ; dépôt déclaré
`https://github.com/sourcefrog/cargo-mutants`.

**Point de vigilance nommé, pas dissimulé** : `cargo-mutants` a un
**propriétaire unique**. C'est le facteur de risque de chaîne
d'approvisionnement le plus visible de cette ligne. Ce qui le borne ici : (i)
l'outil est installé à **version exacte** et `--locked`, donc une reprise
malveillante du compte ne change rien tant que la version n'est pas remontée
par un acte de revue ; (ii) il ne fait **pas** partie du graphe du vérificateur
ni du cœur — il n'entre dans aucun artefact livré ; (iii) il ne tourne que dans
un job CI sans droit d'écriture (`permissions: contents: read`).

## Outillage de fuzz — instruit le 2026-08-13, RATIFIÉ le même jour, installé ensuite

ADR-0011 seuil 7 exige un fuzz du vérificateur. Les candidats ont d'abord été
contrôlés sur registre **avant** toute installation, alors qu'aucun n'était
installé : le choix engageait la doctrine de toolchain (ADR-0009 point 3) et a
fait l'objet d'une demande de consultation formée (R-26) déposée le 2026-08-13.
**Le mainteneur a tranché le même jour : les DEUX moteurs sont retenus** —
`cargo-fuzz` sur une nightly épinglée par date réservée à son job, et
`cargo-afl` sur la stable du dépôt, le harnais en arbre restant en complément
multi-plateforme (clarification ADR-0009 point 3, 2026-08-13). Les deux
**outils** ont donc leur ligne dans le tableau ci-dessus — c'est ce que
`cargo install` va chercher — et les **dépendances** qui entrent au graphe de
la cible fuzz gardent leur tableau ci-dessous. Ce tableau-ci garde aussi sa
ligne `cargo-fuzz`, qui est un outil : elle date de l'instruction du matin,
elle est le document de la demande de consultation, et l'effacer réécrirait
l'histoire de la décision. La ligne d'outil qui fait foi pour l'installation
est celle du tableau du haut, re-mesurée avant `cargo install`. Les faits,
mesurés le 2026-08-13 :

| crate | version | licence | mainteneurs (owners) | téléchargements cumulés | 1re publication | contrainte |
|---|---|---|---|---|---|---|
| `cargo-fuzz` | 0.13.2 | MIT OR Apache-2.0 | `frewsxcv`, `fitzgen`, `nagisa`, `Manishearth`, équipe `rust-fuzz:publishers` | 4 044 015 | 2017-02-21 | pilote libFuzzer ; exige une toolchain **nightly** |
| `libfuzzer-sys` | 0.4.13 | **(MIT OR Apache-2.0) AND NCSA** | `frewsxcv`, `fitzgen`, `nagisa`, `Manishearth`, `gedigi` | 56 977 318 (mesure du matin de l'instruction — même arbitrage que la note `cargo-fuzz` : la ligne date de la demande de consultation et ne se réécrit pas) | 2019-09-10 | entrerait au graphe de la cible fuzz ; **NCSA absente de la liste blanche de `deny.toml`** |
| `arbitrary` | 1.4.2 | MIT OR Apache-2.0 | `nagisa`, équipe `rust-fuzz:publishers` | 142 350 058 | 2017-05-08 | facultative — la cible du vérificateur consomme des octets bruts, elle n'a pas besoin de types structurés |
| `afl` | 0.18.2 | **Apache-2.0** (seule) | `frewsxcv`, `smoelius`, `anishnaik`, équipe `rust-fuzz:publishers` | 2 096 591 (mesure du matin de l'instruction, idem) | 2016-01-31 | tourne sur toolchain **stable** ; construit AFL++ depuis les sources, chaîne C requise, **pas de cible Windows** |

Trois faits qui pèsent sur la décision et qu'aucun des quatre contrôles ne
lève :

1. **`cargo-fuzz` impose une toolchain nightly.** Le dépôt épingle `1.97.1` par
   fichier versionné et la CI **vérifie** la toolchain servie au lieu de
   l'espérer (`squelette.yml`). Une nightly serait donc une **seconde**
   toolchain, épinglée par date, réservée au job fuzz — pas un remplacement.
   La forme exacte de cet épinglage est ce qui est soumis à consultation.
2. **`afl` tourne sur stable mais pas sur Windows.** Le critère de clôture du
   dépôt exige un vert sur Windows **et** Linux (S2.5, run `31645277610`).
   Un fuzz Linux seul est défendable — le double-build D6 l'est déjà, avec son
   asymétrie publiée — mais c'est une asymétrie de plus, à décider, pas à
   subir.
3. **`libfuzzer-sys` porte `AND NCSA`.** `cargo deny check licenses` lit le
   manifeste : la licence NCSA devrait entrer dans la liste blanche de
   `deny.toml`, c'est-à-dire un élargissement de gate porté par ADR. Le dépôt a
   déjà refusé un tel élargissement une fois, pour un confort d'architecture
   (ADR-0015, alternative (a), motif 3). Le motif serait ici différent — un
   outil de test, hors artefact livré — mais la décision reste une décision.

Ce qui a été **complété le 2026-08-13**, après ratification et **avant
installation** :

* **L'outil AFL n'est PAS la crate `afl`.** `cargo install` va chercher
  **`cargo-afl`**, crate distincte depuis la scission du paquet ; la ligne du
  tableau d'outils ci-dessus la porte, avec ses propres mainteneurs
  (`smoelius`, `anishnaik`, équipe `rust-fuzz:publishers` — `frewsxcv`
  n'y figure pas, à la différence de la crate `afl`). La version retenue,
  **0.18.2**, est celle qui apparie exactement la version de la bibliothèque
  `afl` 0.18.2 que la cible consomme : outil et runtime au même numéro, aucun
  appariement à deviner.
* **`arbitrary` n'est pas une dépendance DIRECTE — mais elle entre au graphe,
  et c'est une mesure, pas une déduction.** La cible fuzz est
  [`shogen_verifier::eprouver`], dont la signature est `fn eprouver(octets:
  &[u8])` : elle consomme des **octets bruts**. `arbitrary` ne sert qu'à
  dériver des *types structurés* depuis un flux d'octets — le harnais n'a rien
  à dériver, il transmet la tranche telle quelle, et aucun manifeste de
  `fuzz/` ne la nomme. **Elle arrive quand même**, parce que `libfuzzer-sys`
  en dépend inconditionnellement. Mesuré le 2026-08-13,
  `cargo tree -p shogen-fuzz-libfuzzer -e normal` dans `fuzz/` :

  ```
  shogen-fuzz-libfuzzer v0.0.0 (/mnt/f/Shogen/fuzz/libfuzzer)
  ├── libfuzzer-sys v0.4.13
  │   └── arbitrary v1.4.2
  └── shogen-verifier v0.0.0 (/mnt/f/Shogen/crates/shogen-verifier)
      └── shogen-core v0.0.0 (/mnt/f/Shogen/crates/shogen-core)
  ```

  La conclusion utile n'est donc PAS « un acteur de chaîne
  d'approvisionnement de moins » — ce qui aurait été faux — mais : **son
  contrôle de registre était dû de toute façon**, il est fait (ligne du
  tableau ci-dessous), et son périmètre est celui du workspace `fuzz/`, hors
  artefact livré. La formule initiale de ce fichier (« facultative ») décrivait
  l'usage direct ; le graphe, lui, se mesure.
* **`libfuzzer-sys` n'entre que dans le workspace `fuzz/`**, jamais au graphe
  du vérificateur ni du cœur : `fuzz/` est un workspace INDÉPENDANT (son propre
  `Cargo.lock`), et l'arête va de la cible fuzz **vers** le vérificateur.
  Contrôle mécanique conservé : `cargo tree -p shogen-verifier -e normal` au
  dépôt racine reste à **2 lignes**.

Le harnais en arbre (`xtask/src/fuzz.rs`) **reste** : **zéro dépendance, zéro
outil, zéro toolchain nouvelle**, sur les deux plateformes. Il tient le seuil
binaire, le corpus committé croissant et les budgets ; il ne tient pas la
partie guidée par la couverture — c'est ce que les deux moteurs instrumentés
ajoutent, sur Linux seulement (asymétrie mesurée, cf. `.github/workflows/fuzz.yml`).

## Outillage de lecture (OCR) — contrôlé le 2026-10-02 14:26 UTC, avant installation (session cloud, partie 3 de S2)

Usage : OCR mécanique des scans Künsch 1989 et Fisher 1921 (sans couche de texte : `pdftotext` rend 20 et 5 mots), pour des extractions `*.sidecar` indépendantes du lecteur (gate S-G5) ; hors graphe du workspace, hors CI, rien de livré. Registre officiel : archive Ubuntu 24.04 (noble), champs recopiés de `apt-cache show` et du paquet téléchargé sans installation (`apt-get download`, `dpkg-deb --fsys-tarfile`).

| outil | version retenue | licence | mainteneurs | origine | contrôle du | usage |
|---|---|---|---|---|---|---|
| `tesseract-ocr` | 5.3.4-1build5 (`pool/universe/t/tesseract/tesseract-ocr_5.3.4-1build5_amd64.deb`, SHA256 de l'index `2dfac382d77215aee0c3de4a2a2205505d5f2195e72e79b54ad32154fc08da77` = sha256 du paquet téléchargé) | Apache-2.0 (fichier `copyright` du paquet ; `Upstream-Name: tesseract-ocr`, `Source: https://github.com/tesseract-ocr/`) | Ubuntu Developers ; mainteneur d'origine Alexander Pozdnyakov | Ubuntu, section universe/graphics | 2026-10-02 14:26 UTC | OCR des scans de la biblio (partie 3) |
| `tesseract-ocr-eng` (dépendance du précédent) | 1:4.1.0-2 (SHA256 de l'index `b1996b3113c78663f4dd16cf18aa1f288b07e9624f8d4a0ddbd7d9b52a234ba7`) | (paquet `tesseract-lang`) | Ubuntu Developers | Ubuntu, universe | 2026-10-02 14:26 UTC | données de langue anglaise |

Limite déclarée : pas de compte de téléchargements ni d'ancienneté pour un paquet d'archive Ubuntu (champs absents du registre) ; l'outil s'installe dans le conteneur éphémère de la session, pas sur le poste de l'investisseur.

## Lecture YAML des workflows (PyYAML de la distribution) — contrôlé le 2026-10-09 21:29 UTC, avant emploi au dépôt (lot DETTES-T5, DT5-8)

Usage : `enforcement/workflows-yaml.py` charge chaque workflow de `.github/workflows/` et refuse tout fichier illisible
(adjudication C-2 du lot DETTES-T5 : un nom d'étape hors forme YAML avait rendu `gates.yml` illisible pour la forge sans
qu'aucune gate le voie). Forme retenue : le paquet de la distribution, jamais `pip` ; dans le job g1, installé à version
exacte par `apt-get` si l'image ne l'a pas à cette version, version relue après l'installation et imprimée au journal,
module importé rattaché au paquet par `dpkg -S` (relecture G2 du lot, C-2) ; interpréteur du système
(`/usr/bin/python3`).
Registre officiel : archive Ubuntu 24.04 (noble), champs recopiés de `apt-cache show python3-yaml` et du fichier
`copyright` du paquet (session cloud, conteneur où le paquet était déjà installé).

| paquet | version retenue | licence | mainteneurs | origine | contrôle du | usage |
|---|---|---|---|---|---|---|
| `python3-yaml` (source `pyyaml`) | 6.0.1-2build2 (`pool/main/p/pyyaml/python3-yaml_6.0.1-2build2_amd64.deb`, SHA256 de l'index `315e59500af855f23ee4e95525b99009bd798c4d2658af8eb4b2d66a8a91ec23` ; priorité `important` ; dépend de `libyaml-0-2`) | MIT (texte du fichier `copyright` ; Copyright (c) 2017-2019 Ingy döt Net, 2006-2016 Kirill Simonov) | Ubuntu Developers ; mainteneur d'origine Debian Python Team | Ubuntu, `noble/main` ; amont `https://github.com/yaml/pyyaml` | 2026-10-09 21:29 UTC | lecture YAML des workflows (job g1) |

Limites déclarées : pas de compte de téléchargements ni d'ancienneté pour un paquet d'archive (champs absents du
registre) ; PyYAML lit le YAML 1.1, la forge son propre analyseur : un fichier accepté ici peut encore être refusé
par la forge (le contrôle refuse en plus les clés répétées et les documents multiples, qu'elle refuse aussi
[inféré]) ; présence du paquet sur l'image `ubuntu-24.04` non lue (d'où l'installation conditionnelle). Écart :
`yaml.safe_load` de ce paquet a servi d'outil de mesure hors dépôt aux phases 1 et 2 du lot, avant cette ligne
(E-12 du journal G1 du lot).

## Ce que ce registre ne dit pas

Qu'un outil contrôlé est sûr. R-8 mesure ce qu'un registre publie — existence,
ancienneté, mainteneurs, téléchargements — et rien de plus. Un compte
mainteneur peut être repris, un paquet peut être remplacé à version égale sur
un registre qui l'autoriserait. C'est pourquoi la version est **exacte** et
`--locked` partout où l'outil l'accepte — `cargo fuzz`, qui ne l'accepte pas,
est gardé autrement : contrôle `cargo metadata --locked` avant campagne et
`git diff --exit-code -- fuzz/Cargo.lock` après (revue G2 du chantier fuzz,
2026-08-13) — et pourquoi la moitié mécanique (S-G7) existe à côté :
aucune des deux ne dispense de l'autre.
