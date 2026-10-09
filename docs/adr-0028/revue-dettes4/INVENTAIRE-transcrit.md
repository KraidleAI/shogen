# Inventaire des SHA256SUMS de docs/ par le générateur de DETTES-T4 (transcrit)

> Transcription par l'orchestrateur le 2026-10-09 21:12:10 UTC du fichier INVENTAIRE.md ; contrôle FM-1.1 des transcripts du générateur-correcteur, du réviseur et du contre-contrôleur, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# INVENTAIRE des `SHA256SUMS` de `docs/` (lot DETTES-T4, item SHOGEN-DOCS-SHA256SUMS-GATE-1)

- **Modèle** : `claude-opus-5-5` (générateur G1 ; Gate 0 lu le 2026-10-09 18:08:01 UTC par `date -u`)
- Tête inventoriée : `963eba9e40d6f111d25a8dd2e74ed58651091ac9` (copie creuse `git clone --no-hardlinks` + sparse
  non-cone excluant `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`,
  `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/`, `*.jsonl`). Passages antérieurs : `6f8bfd8` (31 fichiers,
  281 lignes), `aff8c3b` (32, 285 : `766f0c2` ajoute `docs/adr-0028/revue-dettes3/SHA256SUMS`, 4 lignes OK) ;
  `963eba9` ajoute `docs/adr-0029/g0-sim/revue-nprime/SHA256SUMS` (5 lignes OK). Mêmes constats aux trois têtes.
- Recherche par nom (`find docs -name SHA256SUMS` dans la copie creuse, dossiers interdits absents) : **33 fichiers,
  290 lignes**. Deux mesures indépendantes : `outils/inventaire.py` (Python, lecture ligne à ligne) et
  `sha256sum -c --quiet` dans chaque dossier (coreutils) : 32 sorties 0, 1 sortie 1 (`sim-niveau`), concordantes.
- Aucun `SHA256SUMS` autorisé ne liste un chemin sous un dossier interdit, ni hors de son dossier, ni un `*.jsonl`
  (0 ligne dans ce cas) : aucun fichier interdit n'a eu à être écarté.
- Rien n'a été écrit dans `docs/`.
- Ajout du 2026-10-09 19:02:07 UTC : tête relue `6356a94` (fusion de la PR n° 9), arbre identique à `963eba9` : inventaire inchangé.

## Résultat par fichier (tête `963eba9`)

Colonnes : « non listés » = fichiers du dossier absents de son `SHA256SUMS`, hors des sous-dossiers qui portent leur
propre `SHA256SUMS` (dernière colonne : ces fichiers-là, couverts par le `SHA256SUMS` du sous-dossier).

| # | SHA256SUMS | lignes | sha256sum -c (OK / échec / absent) | non listés (dossier propre) | fichiers de sous-dossiers à SHA256SUMS propre |
|---|---|---|---|---|---|
| 1 | `docs/adr-0028/lint-haiku/SHA256SUMS` | 11 | 11 / 0 / 0 | 0 | — |
| 2 | `docs/adr-0028/revue-dettes3/SHA256SUMS` | 4 | 4 / 0 / 0 | 0 | — |
| 3 | `docs/adr-0028/sim-dettes/SHA256SUMS` | 22 | 22 / 0 / 0 | 0 | — |
| 4 | `docs/adr-0028/sim-niveau/SHA256SUMS` | 23 | 12 / 0 / 11 (l.1, l.2, l.3, l.4, l.5, l.6, l.7, l.8, l.9, l.10, l.12) | 0 | — |
| 5 | `docs/adr-0029/etude-marche/carto/SHA256SUMS` | 15 | 15 / 0 / 0 | 0 | — |
| 6 | `docs/adr-0029/etude-marche/hylo/SHA256SUMS` | 15 | 15 / 0 / 0 | 0 | — |
| 7 | `docs/adr-0029/g0-calib/SHA256SUMS` | 7 | 7 / 0 / 0 | 0 | 6 |
| 8 | `docs/adr-0029/g0-calib/revue-ca/SHA256SUMS` | 5 | 5 / 0 / 0 | 0 | — |
| 9 | `docs/adr-0029/g0-plan2/SHA256SUMS` | 10 | 10 / 0 / 0 | 0 | — |
| 10 | `docs/adr-0029/g0-sim/SHA256SUMS` | 5 | 5 / 0 / 0 | 0 | 69 |
| 11 | `docs/adr-0029/g0-sim/revue-integ/SHA256SUMS` | 8 | 8 / 0 / 0 | 0 | — |
| 12 | `docs/adr-0029/g0-sim/revue-nprime/SHA256SUMS` | 5 | 5 / 0 / 0 | 0 | — |
| 13 | `docs/adr-0029/g0-sim/revue-sb11/SHA256SUMS` | 6 | 6 / 0 / 0 | 0 | — |
| 14 | `docs/adr-0029/g0-sim/revue-sb13/SHA256SUMS` | 6 | 6 / 0 / 0 | 0 | — |
| 15 | `docs/adr-0029/g0-sim/revue-t1/SHA256SUMS` | 6 | 6 / 0 / 0 | 0 | — |
| 16 | `docs/adr-0029/g0-sim/revue-t2/SHA256SUMS` | 9 | 9 / 0 / 0 | 0 | — |
| 17 | `docs/adr-0029/g0-sim/revue-t3/SHA256SUMS` | 11 | 11 / 0 / 0 | 0 | — |
| 18 | `docs/adr-0029/g0-sim/revue-t4/SHA256SUMS` | 10 | 10 / 0 / 0 | 0 | — |
| 19 | `docs/adr-0029/plan-s2bis-2/SHA256SUMS` | 3 | 3 / 0 / 0 | `README.md` | 10 |
| 20 | `docs/adr-0029/plan-s2bis-2/revue/SHA256SUMS` | 9 | 9 / 0 / 0 | 0 | — |
| 21 | `docs/adr-0029/plan-s2bis/SHA256SUMS` | 3 | 3 / 0 / 0 | `G1-lot-PLAN-S2BIS.md`, `G2-lot-PLAN-S2BIS.md`, `README.md` | — |
| 22 | `docs/adr-0029/s2bis/revue-dettes1/SHA256SUMS` | 4 | 4 / 0 / 0 | 0 | — |
| 23 | `docs/adr-0029/s2bis/revue-out2/SHA256SUMS` | 11 | 11 / 0 / 0 | 0 | — |
| 24 | `docs/adr-0029/s2bis/revue-p1-integ/SHA256SUMS` | 8 | 8 / 0 / 0 | 0 | — |
| 25 | `docs/adr-0029/s2bis/revue-p1a/SHA256SUMS` | 7 | 7 / 0 / 0 | 0 | — |
| 26 | `docs/adr-0029/s2bis/revue-p1b/SHA256SUMS` | 9 | 9 / 0 / 0 | 0 | — |
| 27 | `docs/adr-0029/s2bis/revue-p1c-fetch/SHA256SUMS` | 5 | 5 / 0 / 0 | 0 | — |
| 28 | `docs/adr-0029/s2bis/revue-p1c/SHA256SUMS` | 16 | 16 / 0 / 0 | 0 | — |
| 29 | `docs/adr-0029/s2bis/revue-p2a/SHA256SUMS` | 6 | 6 / 0 / 0 | 0 | — |
| 30 | `docs/adr-0029/s2bis/revue-p2b/SHA256SUMS` | 6 | 6 / 0 / 0 | 0 | — |
| 31 | `docs/adr-0029/s2bis/revue-r1/SHA256SUMS` | 3 | 3 / 0 / 0 | 0 | — |
| 32 | `docs/adr-0029/s2bis/revue-rb-format/SHA256SUMS` | 13 | 13 / 0 / 0 | 0 | — |
| 33 | `docs/adr-0029/s2bis/revue-rb1/SHA256SUMS` | 9 | 9 / 0 / 0 | 0 | — |

**Sommes en échec : 0.** Fichiers listés absents : 11 lignes, toutes dans `docs/adr-0028/sim-niveau/SHA256SUMS`.
Fichiers non listés (dossier propre) : 4, dans `plan-s2bis/` (3) et `plan-s2bis-2/` (1).

## Détail des 11 lignes absentes (`docs/adr-0028/sim-niveau/SHA256SUMS`)

| ligne | chemin écrit | somme écrite (début) | fichier au dépôt |
|---|---|---|---|
| l.1 | `execution-B/sim_niveau.json` | `d17c5121…` | jamais versé (0 commit, `git log --all`) ; même somme que `sim_niveau.json` versé (l.11) |
| l.2 | `execution-B/sim_niveau.log.txt` | `02e6fa72…` | jamais versé |
| l.3 | `execution-B/sim_niveau.txt` | `7173a9ce…` | jamais versé ; même somme que `sim_niveau.txt` (l.13) |
| l.4 | `oracle-1b/processus-1/sim_niveau.json` | `3a5b91ce…` | jamais versé |
| l.5 | `oracle-1b/processus-1/sim_niveau.log.txt` | `10325f43…` | jamais versé |
| l.6 | `oracle-1b/processus-1/sim_niveau.txt` | `c241cb15…` | jamais versé |
| l.7 | `oracle-1b/processus-12/sim_niveau.json` | `3a5b91ce…` | jamais versé |
| l.8 | `oracle-1b/processus-12/sim_niveau.log.txt` | `bcf42cac…` | jamais versé |
| l.9 | `oracle-1b/processus-12/sim_niveau.txt` | `c241cb15…` | jamais versé |
| l.10 | `oracle-4a-4b/oracle_4a_4b.json` | `bd3cc311…` | chemin inexact : versé à la racine (`oracle_4a_4b.json`, l.19, même somme) |
| l.12 | `sim_niveau.log.txt` | `058fb1f4…` | jamais versé (journal d'exécution, hors bit-identité) |

Origine : le `SHA256SUMS` du dossier `sortie\` du lot SIM-NIVEAU (13 fichiers, `docs/G1-lot-SIM-NIVEAU.md` l.210),
versé tel quel en `40b4cfb` avec 3 fichiers sur 13 ; constat SHOGEN-SIM-SOMMES-1 (annexe B l.461), clos en `04beacd`
par décision écrite (annexe B l.515) : « Lignes existantes non touchées (le paquet cite l.11, l.13, l.15-16) ». Dernier
commit sur ce `SHA256SUMS` : `972612a` (2026-10-03T00:49:18Z, 2 lignes ajoutées en fin). Réelle : sans objet (fichier
absent). Traitement proposé : Q-1 du rapport.

## Somme périmée citée par l'item (l.4 de `docs/adr-0029/g0-sim/SHA256SUMS`)

Conforme à la tête. Historique (lecture seule, `git show <commit>:…` et `sha256sum`) : OK à `435fa12` ; **en échec à
`784ebd2`** (écrite `eeaceb6b…`, réelle `d9cffc0a…` : `G0-SIM-BIS.md` modifié sans sa somme) ; remise à jour à
`3164348` (« empreinte du G0 remise à jour ») ; `12ce67f` et `2f32432` (SB-11z) touchent les deux, OK. Sur les 5
commits qui touchent l'un des deux fichiers, seul `784ebd2` a l.4 en échec ; le constat de l'item (annexe B l.1546,
« corrigée par SB-11z ») portait donc sur un état non commis [inféré]. Le contrôle DT4-a, lancé sur
`git archive 784ebd2 docs/adr-0029`, refuse cette ligne (sortie 1, motif `docs/adr-0029/g0-sim/SHA256SUMS l.4 :
G0-SIM-BIS.md : somme écrite eeaceb6b…, réelle d9cffc0a…` ; `sorties/retro-784ebd2.txt`).

## Hors de l'item (fichiers de sommes d'un autre nom)

| fichier | lignes | `sha256sum -c` |
|---|---|---|
| `docs/adr-0029/etude-marche/carto/SHA256SUMS.raw` | 37 | 37 fichiers listés absents (copies brutes `./raw/…` non versées) |
| `docs/adr-0029/etude-marche/hylo/SHA256SUMS.copies` | 193 | 193 fichiers listés absents (`pages/…` non versées) |
| `docs/adr-0029/calib/SHA256SUMS-ECHANTILLONS.txt` | 148 | 148 fichiers listés absents (`samples/…` non versés) |

L'item nomme `SHA256SUMS` ; ces manifestes de copies non versées ne sont pas contrôlables en CI. Rendus comme limite
(L-1 du rapport).
