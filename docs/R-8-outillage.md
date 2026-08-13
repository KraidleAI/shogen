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

## Outillage de fuzz — instruit, non installé

ADR-0011 seuil 7 exige un fuzz du vérificateur. Les candidats ont été contrôlés
sur registre **avant** toute installation, et **aucun n'a été installé** : le
choix engage la doctrine de toolchain (ADR-0009 point 3) et fait l'objet d'une
demande de consultation formée (R-26) déposée le 2026-08-13. Les faits qui
alimentent cette demande, mesurés le même jour :

| crate | version | licence | mainteneurs (owners) | téléchargements cumulés | 1re publication | contrainte |
|---|---|---|---|---|---|---|
| `cargo-fuzz` | 0.13.2 | MIT OR Apache-2.0 | `frewsxcv`, `fitzgen`, `nagisa`, `Manishearth`, équipe `rust-fuzz:publishers` | 4 044 015 | 2017-02-21 | pilote libFuzzer ; exige une toolchain **nightly** |
| `libfuzzer-sys` | 0.4.13 | **(MIT OR Apache-2.0) AND NCSA** | `frewsxcv`, `fitzgen`, `nagisa`, `Manishearth`, `gedigi` | 56 977 318 | 2019-09-10 | entrerait au graphe de la cible fuzz ; **NCSA absente de la liste blanche de `deny.toml`** |
| `arbitrary` | 1.4.2 | MIT OR Apache-2.0 | `nagisa`, équipe `rust-fuzz:publishers` | 142 350 058 | 2017-05-08 | facultative — la cible du vérificateur consomme des octets bruts, elle n'a pas besoin de types structurés |
| `afl` | 0.18.2 | **Apache-2.0** (seule) | `frewsxcv`, `smoelius`, `anishnaik`, équipe `rust-fuzz:publishers` | 2 096 591 | 2016-01-31 | tourne sur toolchain **stable** ; construit AFL++ depuis les sources, chaîne C requise, **pas de cible Windows** |

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

En attendant, ce qui tourne est le harnais en arbre (`xtask/src/fuzz.rs`) :
**zéro dépendance, zéro outil, zéro toolchain nouvelle**, sur les deux
plateformes. Il tient le seuil binaire, le corpus committé croissant et les
budgets ; il ne tient pas la partie guidée par la couverture, et le dit à
chaque exécution.

## Ce que ce registre ne dit pas

Qu'un outil contrôlé est sûr. R-8 mesure ce qu'un registre publie — existence,
ancienneté, mainteneurs, téléchargements — et rien de plus. Un compte
mainteneur peut être repris, un paquet peut être remplacé à version égale sur
un registre qui l'autoriserait. C'est pourquoi la version est **exacte** et
`--locked` partout, et pourquoi la moitié mécanique (S-G7) existe à côté :
aucune des deux ne dispense de l'autre.
