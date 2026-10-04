# Corrections de la relecture G2 — lot DETTES-SIM (note du worker, 2026-10-04)

- **Gate 0** : modèle résolu **`claude-opus-5-5`** (identifiant exact déclaré par le harnais dans le contexte de la session), effort max ; worker générateur du lot (fiche `shogen-worker`), qui applique la liste fermée du réviseur. Aucune opération git en écriture, rien écrit dans le dépôt ; données synthétiques seulement ; aucune pièce de l'annexe D.2, aucun rendu d'exécution, aucun dossier interdit ouvert.
- **Rapport G2** : `scratchpad/dettes/G2-SIM/G2-DETTES-SIM.md`, sha256 `93b5881f4362b6a96a60559699044cb396c3794b74f4acfda17bcad594417c2b` (recalculé : égal) ; verdict ACCEPTE-AVEC-CORRECTIONS ; liste fermée C-1 à C-8 (§10 du rapport). Aucune correction hors de la liste ; aucun générateur ni aucune sortie de simulation touchés.
- **Base** : diffs refaits contre `dad3bc6`, tête nommée par l'orchestrateur (copie `git archive dad3bc6` sans `docs/rapports`, `docs/adr-0025`, `docs/adr-0028/monark-m009a` ni `biblio`, puis `biblio/INDEX.md` seul). **Écart de base relevé pendant la passe** (`git rev-parse HEAD`, lecture seule) : la tête du dépôt est passée à `5d45248` (relevée à 07:43Z : dix commits du lot POST-PREREG après `dad3bc6`, tous sous `scripts/post-s2/`, 17 fichiers neufs), puis à `27189d7` (relevée à 08:12Z : huit commits de plus, clôture de POST-PREREG et DETTES-B2, dont la gate des secrets), à `26c2c41` (08:16Z : versions des exécuteurs de `.github/workflows/`), à `1c2f0f2` (08:17Z : gate S-G9 de `xtask`), à `7c4861a` (08:22Z : contrôles de S-G9 complétés, annexe A, `docs/DEVOPS.md`), à `7bfff83` (08:29Z : clôture de DETTES-B2, S-G5 et S-G9 modifiés) et à `0419910` (08:31Z : révision 3 de l'ADR-0029, annexe B.52, `JOURNAL.md`). Aucun de ces commits ne touche un chemin du lot ni `r1.py`. Les dix diffs finaux ont été appliqués et vérifiés sur `dad3bc6` et sur les sept têtes (§6) ; les motifs de la gate des secrets ont été appliqués aux fichiers ajoutés (§6). Depuis `7c4861a`, S-G9 est rouge sur la copie, avec comme sans les diffs du lot (artefact de la copie, §8, O-a). Le worker n'avance aucune base.
- **Fenêtre** : 2026-10-04, de 07:05Z (lecture du rapport) à 08:33:50Z (génération de cette note, horloge lue par le programme).

## 1. Corrections, une par une

| n° | pièce | ce qui est fait | critère d'acceptation du G2 | état |
|---|---|---|---|---|
| C-1 | `DS-2a.diff` : `sim_bartlett_poolee_oracle.py` (193 lignes) | B1 recalcule aussi `E_centre_sur_P` = Σ_{\|k\|<ℓ} (1 − \|k\|/ℓ)(n − \|k\|)R(k) et `kunsch_premier_ordre` = −(n/ℓ)·Σ_{k=1}^{n−1} 2k·R(k), sur les R(k) de la convolution (`rk_conv`). Tolérance : égalité relative à 10⁻⁹ ; une référence nulle en théorie (\|x\| ≤ 10⁻⁹·Var(K) : terme de Künsch à L = 1) se compare à l'échelle de Var(K). L'état intermédiaire (écart rapporté à max(\|x\|, Var(K)) pour les cinq références) desserrait B1 : trouvé par le worker et corrigé avant livraison (§4 ; journal E-14) | B-kunsch et B-centre tués ; témoin vert ; oracle rejoué sur A et sur B (`--complet`), enregistrements reversés, `SHA256SUMS` mis à jour | **fait** : §2 (tués par B1), §4, §5 |
| C-2 | `DS-3a.diff` : `sim_dettes_oracle_r1.py` (193 lignes) | M0 compare `parametres.trou`, `alpha`, `hetero`, `mele` et les d0 de `lourd_d0_ED` de `modeles.json` à la table du pré-enregistrement recopiée dans l'oracle (`EXT`, `D0`) ; champ `M0_parametres_extensions` = 5 à l'enregistrement | B-hetero tué ; rejeux, reversement, `SHA256SUMS` | **fait** : §2 (tué par M0), §5 |
| C-3 | `DS-J` §7, ligne SHOGEN-SIM-REGEN-1 | portée élargie : forme de la queue de Lomax (C-geom), durée moyenne des trous (A-trou30), emploi des paramètres des extensions par les générateurs, ordre des tirages et alternance stricte (D3) ; construction : `serie` indépendante dans l'oracle ou contrôles de forme (survie des durées de run contre (d0/(d0 + j − 1))^1,5 ; trou moyen contre 60) ; déclencheur « avant toute réutilisation des générateurs étendus » | texte relu par l'orchestrateur | **fait** (journal §7) |
| C-4 | `DS-J` §7, ligne SHOGEN-FLUX-ABSORPTION-COLLECTIVE-1 (absorbe l'ex-QUASI-MORT-3) | « exact en c et en n, sous fenêtres iid, flux hors de la paire indépendants, dépendance confinée à la paire ; égalité exacte vérifiée par énumération au G2 » | idem | **fait** (journal §7) |
| C-5 | `DS-J` §4 | puce « Erreur-type de la bascule, sous aucun oracle » : mutant F-SE survivant, déclaré ; valeur publiée 0,0028034 (`flux.json`, `bascule.SE` = 0,0028033914559205753) ; vérifiée par le G2 (méthode delta 0,0028034 ; bootstrap apparié de 400 rééchantillonnages 0,00286 ; [2nd] : G2 §6 ter) | idem | **fait** (journal §4) |
| C-6 | `DS-J` §6 | erratum E-13 : E[D] exacts 5,000001711635 ; 20,000009348193 ; 60,000001285278 (recalculés par le worker par deux voies concordantes à 12 chiffres, `corrections-g2/c6/v_lomax_c6.py`) ; cause : signe du terme f(J)/2 de la queue d'Euler-Maclaurin dans `conception/calc_design.py` ; écart sans effet (b et la cible du run moyen déplacés d'au plus 3,0·10⁻⁸ en relatif) | idem | **fait** (journal §6) |
| C-7 | `DS-J` §5.1, §5.3, §5.4 | « À fenêtres iid (L = 1), un seul taux … dépasse 0,01 en estimation ponctuelle » (§5.1 et §5.3) ; « (L ≥ 5, sauf L = 5 à n = 2,5·10⁴ : 0,0086 ; correction C-7 du G2) » (§5.4) | idem | **fait** (journal §5) |
| C-8 | `DS-V.diff` | huit `.log.txt` retirés du versement et de son `SHA256SUMS` ; leurs sha256 gardés au journal (§4 bis) ; fichiers gardés au dossier de travail (`runs/A/…`) | `SHA256SUMS` à 22 lignes, `sha256sum -c` vert, aucun chemin `/tmp/claude-0` dans `docs/adr-0028/sim-dettes/` | **fait** (§5) |

**Décisions de l'orchestrateur, reportées au journal** : sorties sous `docs/adr-0028/sim-dettes/`, journal `docs/G1-lot-DETTES-SIM.md`, versement (`DS-V`, `DS-J`) en un commit sans code après les huit commits de code (§9, E-8) ; SIM-NIVEAU-P-1 fermé avec sa déviation déclarée (§5.7, §9) ; choc commun admis comme alternative (§9) ; items du §7 formés avec les ajustements du G2 : QUASI-MORT-3 fusionné dans ABSORPTION-COLLECTIVE-1, SERIEL-1 élargi (co-défaillance d'ordre ≥ 3 ou impliquant le flux faible), ZSEUL-2 doté de la construction du G2 (R = 10⁵ sur les quatre cellules L = 1 des deux plus petits p, pré-enregistrée, exploratoire), SIM-PLATEFORME-2 rattaché à la limite L-7 de l'étape S, sans item neuf (§7).

## 2. Mutants du réviseur : rouge avant, vert après (table extraite de `avant/banc.out`, `avant/banc-7.out` et `apres/banc.out`)

| id | fichier muté | mutation (G2) | disposition du G2 | avant correction (`sim-avant`) | après correction (`sim-apres`) |
|---|---|---|---|---|---|
| R1 | `r1:shogen_s2/r1.py` | `"rejet_non_qualifiable" if zb is None else "rejette"` → `"rejette" if zb is None else "rejette"` | déjà tué | tué, oracle (rc 1) : ECHEC (T3) : valeur NON ÉVALUABLE (rejet non qualifiable) contre r1.regle_critere rejette, p=0.01006 L=1 n=2880 r=45 | tué, oracle (rc 1) : ECHEC (T3) : valeur NON ÉVALUABLE (rejet non qualifiable) contre r1.regle_critere rejette, p=0.01006 L=1 n=2880 r=45 |
| C-geom | `sim_dettes_calc.py` | `int(d0 * ((1.0 - rnd()) ** (-1 / ALPHA) - 1))` → `int(__import__('math').log(1.0 - rnd()) / __import__('math')` | à déclarer (C-3, SIM-REGEN-1) | survit (rc 0 à toutes les étapes) | survit (rc 0 à toutes les étapes) |
| A-trou30 | `sim_dettes_calc.py` | `absente = rnd() < ((1 - 1 / G) if absente else f / (G * (1 -` → `absente = rnd() < ((1 - 2 / G) if absente else 2 * f / (G * ` | à déclarer (C-3, SIM-REGEN-1) | survit (rc 0 à toutes les étapes) | survit (rc 0 à toutes les étapes) |
| B-kunsch | `sim_bartlett_poolee.py` | `-n / ELL * math.fsum(2 * k * R[k] for k in range(1, n))` → `-n / ELL * math.fsum(k * R[k] for k in range(1, n))` | à tuer (C-1) | survit (rc 0 à toutes les étapes) | tué, oracle (rc 1) : ECHEC (B1) : kunsch_premier_ordre : sortie -6.9702713170993835, oracle -13.940542633541648, L=5 n=10000 |
| B-centre | `sim_bartlett_poolee.py` | `2 * (1 - k / ELL) * (n - k) * R[k] for k in range(1, ELL)` → `2 * (1 - k / ELL) * n * R[k] for k in range(1, ELL)` | à tuer (C-1) | survit (rc 0 à toutes les étapes) | tué, oracle (rc 1) : ECHEC (B1) : E_centre_sur_P : sortie 1049.1821630286613, oracle 1048.8578694649611, L=5 n=10000 |
| A-Mk | `sim_dettes_calc.py` | `(Pm & Pk).bit_count() * K * K` → `(T - k) * K * K` | déjà tué | tué, oracle (rc 1) : ECHEC (M3) : n, K, e ou N, ['a', 1, 11112] r=0 | tué, oracle (rc 1) : ECHEC (M3) : n, K, e ou N, ['a', 1, 11112] r=0 |
| F-SE | `sim_flux.py` | `g2 * g2 * v2 + 2 * g1 * g2 * c12` → `g2 * g2 * v2 - 2 * g1 * g2 * c12` | à déclarer (C-5) | survit (rc 0 à toutes les étapes) | survit (rc 0 à toutes les étapes) |
| B-tronc | `sim_bartlett_poolee.py` | `if k and g < 1e-20:` → `if k and g < 1e-3:` | déjà tué | tué, oracle (rc 1) : ECHEC (B1) : var_K_exacte : sortie 1062.292974567418, oracle 1062.78813263823, L=5 n=10000 | tué, oracle (rc 1) : ECHEC (B1) : var_K_exacte : sortie 1062.292974567418, oracle 1062.78813263823, L=5 n=10000 |
| F-profil | `sim_flux.py` | `[P if (k == 0 or j >= k) else w for j in range(9)]` → `[P if (k == 0 or j > k) else w for j in range(9)]` | déjà tué | tué, oracle (rc 1) : ECHEC (M2) : P_more_marges : oracle 0.016177640686423134, sortie 0.013114893805128704, profil (1, 0.0, False) | tué, oracle (rc 1) : ECHEC (M2) : P_more_marges : oracle 0.016177640686423134, sortie 0.013114893805128704, profil (1, 0.0, False) |
| B-hetero | `sim_dettes_calc.py` | `HETERO, MELE = (0.01,) * 6 + (0.04,) * 5,` → `HETERO, MELE = (0.01,) * 5 + (0.04,) * 6,` | à tuer (C-2) | survit (rc 0 à toutes les étapes) | tué, oracle (rc 1) : ECHEC (M0) : paramètres des extensions de sim_modeles différents du pré-enregistrement |

Témoins non mutés, après correction (`apres/temoins.out`) : temoin-gn : aucune (rc 0) ; temoin-bp : aucune (rc 0) ; temoin-d3 : aucune (rc 0).

Bilan : avant correction, **4 tués et 6 survivants** (dont B-kunsch, B-centre et B-hetero), comme au rapport G2 §6 ; après correction, **7 tués et 3 survivants**, tous déclarés (C-geom et A-trou30 : SIM-REGEN-1 élargi, C-3 ; F-SE : C-5). Chaque mutant tué l'est par le message `ECHEC` du contrôle visé (rc 1, aucune trace d'exception). État intermédiaire (`apres-v1/banc.out`, oracle B1 à l'échelle max(|x|, Var(K)), E-14) : mêmes issues et mêmes étapes pour les dix mutants.

## 3. Non-régression : banc du worker rejoué sur l'état final (jeux BARTLETT/POOLEE et MODELES/FLUX)

`banc_worker_copie.py` (copie de `mutants/banc.py` : seuls SRC, R1, l'étiquette de commit et les dossiers de sortie changent) : témoins temoin-bp conforme, temoin-d3 conforme ; **14 mutants tués sur 15**, chacun par le contrôle attendu au banc d'origine ; survivant(s) : D3 (attendu : D3 seul, mutant de spécification déclaré au journal §4, qui survit comme à la première passe) (`banc-worker/sortie.txt`).

## 4. Resserrage de la tolérance de B1 (écart E-14 du journal) : rouge avant, vert après

| id | mutation | état | issue |
|---|---|---|---|
| B-tol | `* (1 + 5e-9)` ajouté à `kunsch_premier_ordre` | intermédiaire (`sim-apres-v1`) | survit (rc 0 à toutes les étapes) |
| B-tol0 | `+ 1e-6` ajouté à `kunsch_premier_ordre` | intermédiaire (`sim-apres-v1`) | tué, oracle (rc 1) : ECHEC (B1) : kunsch_premier_ordre : sortie 1e-06, oracle 1.4240453434510856e-11, L=1 n=10000 |
| B-tol | `* (1 + 5e-9)` ajouté à `kunsch_premier_ordre` | final (`sim-apres`) | tué, oracle (rc 1) : ECHEC (B1) : kunsch_premier_ordre : sortie -13.94054270390148, oracle -13.940542633541648, L=5 n=10000 |
| B-tol0 | `+ 1e-6` ajouté à `kunsch_premier_ordre` | final (`sim-apres`) | tué, oracle (rc 1) : ECHEC (B1) : kunsch_premier_ordre : sortie 1e-06, oracle 1.4240453434510856e-11, L=1 n=10000 |

## 5. Rejeux des oracles finaux et reversement (extraits de `oracles/rejeux.out` et des enregistrements versés)

Rejeux (`corrections-g2/sim-apres`, r1 de `dad3bc6`) : 07:52:50Z ; bp A rc=0 ; d3 A rc=0 ; bp B complet rc=0 ; d3 B complet rc=0 ; 07:56:40Z.

| enregistrement versé (`sim-dettes/`) | sha256 | contrôles (champs de l'enregistrement) |
|---|---|---|
| `garde_n_oracle_r1-A.json` | `e3705936491911dd647c45a3ed59cd97e8db8e80ada3a0879c14490a6475229e` | commit r1 `5afbdd2` ; T0_cas = 20, T1_invariants = 260, T1_invariants_4b_ii = 416, T2_ecart_relatif_max = 1.811834508451762e-45, T3_replications = 12381, T3_P_more_egaux_a_l_identique = 349, T3_ecart_relatif_max = {'P_more': '2.815817142857143e-46', 'garde': '2.8157426905951383e-46', 'z': '1.1144594001524396e-45', 'z_bloc': '6.160391562984183e-46'}, T4_cas = 20 |
| `bartlett_poolee_oracle-A.json` | `4b78e8e41b1d7fb0b6f25e2ef00293520ef30473f104ae6826d0d809ee073404` | commit r1 `dad3bc6` ; B1_references = 40, B1_ecart_relatif_max = 5.2665231195968436e-11, B2_taux = 52, B3_replications = 80, B3_ecart_relatif_max = 9.978349127167886e-47, B4_replications_recomptees = 0 |
| `bartlett_poolee_oracle-B-complet.json` | `728d971d0c29b81bbc7c4c9eea8403b5cc27ba2daa4b7ebfbe1c735a80aededc` | commit r1 `dad3bc6` ; B1_references = 40, B1_ecart_relatif_max = 5.2665231195968436e-11, B2_taux = 52, B3_replications = 80, B3_ecart_relatif_max = 9.978349127167886e-47, B4_replications_recomptees = 1000 |
| `dettes_oracle_r1-A.json` | `958c6c832449c4b4cd5349028c0dea3b7ce20549fc10a2a9e22a63bdb07580c5` | commit r1 `dad3bc6` ; M0_cas = 18, M0_profils = 40, M0_parametres_extensions = 5, M1_invariants_4b_ii = 464, M2_ecart_relatif_max = 8.551832729851518e-17, M3_replications = 300, M3_ecart_relatif_max = 2.892398121876283e-45, M4_replications_recomptees = 0 |
| `dettes_oracle_r1-B-complet.json` | `8e4f02b400ea6a909324a1d64ea42e84187858fda3c9c63e949e4596a761fcd2` | commit r1 `dad3bc6` ; M0_cas = 18, M0_profils = 40, M0_parametres_extensions = 5, M1_invariants_4b_ii = 464, M2_ecart_relatif_max = 8.551832729851518e-17, M3_replications = 300, M3_ecart_relatif_max = 2.892398121876283e-45, M4_replications_recomptees = 3800 |

`sim-dettes/SHA256SUMS` : 22 lignes, sha256 `54c8c52dade89f315c75742d8e9d86b76455671456b0b6c201918bdbb926a7c4` ; recontrôle de chaque ligne : égal ; fichiers du dossier : 23 (dont `SHA256SUMS`) ; `.log.txt` : 0 ; occurrences de `/tmp/claude-0` : 0.

## 6. Vérifications finales (`corrections-g2/verifier.sh`, sorties `corrections-g2/verif/<base>/verif.txt`)

Têtes vérifiées, dans l'ordre des vérifications : `1c2f0f2`, `dad3bc6`, `5d45248`, `27189d7`, `26c2c41`, `7c4861a`, `7c4861a-sans-diffs`, `7bfff83`, `7bfff83-sans-diffs`, `0419910`.

Base `1c2f0f2` :

```
base 1c2f0f2 : 1c2f0f2d66c7c5524a48858c12c216ec405ea233
08:17:52Z
apply DS-0 rc=0
apply DS-1 rc=0
apply DS-2a rc=0
apply DS-2b rc=0
apply DS-3a rc=0
apply DS-3b rc=0
apply DS-3c rc=0
apply DS-3d rc=0
apply DS-V rc=0
apply DS-J rc=0
egal a patche2 : scripts/sim rc=0
egal a patche2 : docs/adr-0028/sim-dettes rc=0
egal a patche2 : docs/G1-lot-DETTES-SIM.md rc=0
r1.py egal a celui de dad3bc6 rc=0
sha256sum -c sim-dettes rc=0 lignes=22
xtask rc=0
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
cargo fmt --check : VERT
no_std du vérificateur (construction pour une cible sans bi
cargo clippy -D warnings : VERT
=== VERDICT GLOBAL : VERT ===
  couverture : 138 fichier(s) examiné(s) sur 138 présent(s)
  couverture : 139 fichier(s) examiné(s) sur 139 présent(s)
harnais rc=0
Ran 405 tests in 69.207s
OK (skipped=2)
__pycache__ : 0
08:19:22Z
```

Base `dad3bc6` :

```
base dad3bc6 : dad3bc6f6c35537d7bb5f8510bbdb354afa966f5
08:19:29Z
apply DS-0 rc=0
apply DS-1 rc=0
apply DS-2a rc=0
apply DS-2b rc=0
apply DS-3a rc=0
apply DS-3b rc=0
apply DS-3c rc=0
apply DS-3d rc=0
apply DS-V rc=0
apply DS-J rc=0
egal a patche2 : scripts/sim rc=0
egal a patche2 : docs/adr-0028/sim-dettes rc=0
egal a patche2 : docs/G1-lot-DETTES-SIM.md rc=0
arbre entier egal a patche2 rc=0
r1.py egal a celui de dad3bc6 rc=0
sha256sum -c sim-dettes rc=0 lignes=22
xtask rc=0
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
cargo fmt --check : VERT
no_std du vérificateur (construction pour une cible sans bi
cargo clippy -D warnings : VERT
=== VERDICT GLOBAL : VERT ===
  couverture : 134 fichier(s) examiné(s) sur 134 présent(s)
  couverture : 135 fichier(s) examiné(s) sur 135 présent(s)
harnais rc=0
Ran 405 tests in 70.542s
OK (skipped=2)
__pycache__ : 0
08:21:01Z
```

Base `5d45248` :

```
base 5d45248 : 5d452485f83114f0612f03f57e84a7ff9098877e
08:21:02Z
apply DS-0 rc=0
apply DS-1 rc=0
apply DS-2a rc=0
apply DS-2b rc=0
apply DS-3a rc=0
apply DS-3b rc=0
apply DS-3c rc=0
apply DS-3d rc=0
apply DS-V rc=0
apply DS-J rc=0
egal a patche2 : scripts/sim rc=0
egal a patche2 : docs/adr-0028/sim-dettes rc=0
egal a patche2 : docs/G1-lot-DETTES-SIM.md rc=0
r1.py egal a celui de dad3bc6 rc=0
sha256sum -c sim-dettes rc=0 lignes=22
xtask rc=0
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
cargo fmt --check : VERT
no_std du vérificateur (construction pour une cible sans bi
cargo clippy -D warnings : VERT
=== VERDICT GLOBAL : VERT ===
  couverture : 134 fichier(s) examiné(s) sur 134 présent(s)
  couverture : 135 fichier(s) examiné(s) sur 135 présent(s)
harnais rc=0
Ran 405 tests in 69.056s
OK (skipped=2)
__pycache__ : 0
08:22:32Z
```

Base `27189d7` :

```
base 27189d7 : 27189d7081cee8244be231cc3fc005f990c2ef86
08:22:38Z
apply DS-0 rc=0
apply DS-1 rc=0
apply DS-2a rc=0
apply DS-2b rc=0
apply DS-3a rc=0
apply DS-3b rc=0
apply DS-3c rc=0
apply DS-3d rc=0
apply DS-V rc=0
apply DS-J rc=0
egal a patche2 : scripts/sim rc=0
egal a patche2 : docs/adr-0028/sim-dettes rc=0
egal a patche2 : docs/G1-lot-DETTES-SIM.md rc=0
r1.py egal a celui de dad3bc6 rc=0
sha256sum -c sim-dettes rc=0 lignes=22
xtask rc=0
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
cargo fmt --check : VERT
no_std du vérificateur (construction pour une cible sans bi
cargo clippy -D warnings : VERT
=== VERDICT GLOBAL : VERT ===
  couverture : 138 fichier(s) examiné(s) sur 138 présent(s)
  couverture : 139 fichier(s) examiné(s) sur 139 présent(s)
harnais rc=0
Ran 405 tests in 70.006s
OK (skipped=2)
__pycache__ : 0
08:24:08Z
```

Base `26c2c41` :

```
base 26c2c41 : 26c2c419063bd17fbc5d81830f006f196447e9b6
08:24:08Z
apply DS-0 rc=0
apply DS-1 rc=0
apply DS-2a rc=0
apply DS-2b rc=0
apply DS-3a rc=0
apply DS-3b rc=0
apply DS-3c rc=0
apply DS-3d rc=0
apply DS-V rc=0
apply DS-J rc=0
egal a patche2 : scripts/sim rc=0
egal a patche2 : docs/adr-0028/sim-dettes rc=0
egal a patche2 : docs/G1-lot-DETTES-SIM.md rc=0
r1.py egal a celui de dad3bc6 rc=0
sha256sum -c sim-dettes rc=0 lignes=22
xtask rc=0
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
cargo fmt --check : VERT
no_std du vérificateur (construction pour une cible sans bi
cargo clippy -D warnings : VERT
=== VERDICT GLOBAL : VERT ===
  couverture : 138 fichier(s) examiné(s) sur 138 présent(s)
  couverture : 139 fichier(s) examiné(s) sur 139 présent(s)
harnais rc=0
Ran 405 tests in 70.967s
OK (skipped=2)
__pycache__ : 0
08:25:40Z
```

Base `7c4861a` :

```
base 7c4861a : 7c4861a6f4c3a6732facf0b9d4bc13cd8ad57a2b
08:25:40Z
apply DS-0 rc=0
apply DS-1 rc=0
apply DS-2a rc=0
apply DS-2b rc=0
apply DS-3a rc=0
apply DS-3b rc=0
apply DS-3c rc=0
apply DS-3d rc=0
apply DS-V rc=0
apply DS-J rc=0
egal a patche2 : scripts/sim rc=0
egal a patche2 : docs/adr-0028/sim-dettes rc=0
egal a patche2 : docs/G1-lot-DETTES-SIM.md rc=0
r1.py egal a celui de dad3bc6 rc=0
sha256sum -c sim-dettes rc=0 lignes=22
xtask rc=1
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : ROUGE (1 violation(s))
cargo fmt --check : VERT
no_std du vérificateur (construction pour une cible sans bi
cargo clippy -D warnings : VERT
=== VERDICT GLOBAL : ROUGE — l'intégration s'arrête (ADR
  couverture : 138 fichier(s) examiné(s) sur 138 présent(s)
  couverture : 139 fichier(s) examiné(s) sur 139 présent(s)
harnais rc=0
Ran 405 tests in 69.292s
OK (skipped=2)
__pycache__ : 0
08:27:10Z
```

Base `7c4861a-sans-diffs` :

```
base 7c4861a, copie vierge SANS les dix diffs (même extraction et mêmes exclusions) : 7c4861a6f4c3a6732facf0b9d4bc13cd8ad57a2b
08:27:31Z
xtask (sans les diffs) rc=1
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : ROUGE (1 violation(s))
=== VERDICT GLOBAL : ROUGE — l'intégration s'arrête (ADR-0013, point 1) ===
S-G9, constat unique, jetons de chemin seuls (aucun texte de document lu) : docs/17-modele-de-menace.md:70 docs/rapports/cartographie-2026-09-29.md:21 
même constat, mêmes jetons, avec les dix diffs (verif/7c4861a) : docs/17-modele-de-menace.md:70 docs/rapports/cartographie-2026-09-29.md:21 
portée de S-G9 : docs/17-modele-de-menace.md docs/08-assumptions.md docs/adr-0028/ANNEXE-A-lots.md docs/adr-0028/ANNEXE-B-items.md 
08:27:49Z
```

Base `7bfff83` :

```
base 7bfff83 : 7bfff83bf3aa7d60739cb8124941dfc9f8eeb8f1
08:29:23Z
apply DS-0 rc=0
apply DS-1 rc=0
apply DS-2a rc=0
apply DS-2b rc=0
apply DS-3a rc=0
apply DS-3b rc=0
apply DS-3c rc=0
apply DS-3d rc=0
apply DS-V rc=0
apply DS-J rc=0
egal a patche2 : scripts/sim rc=0
egal a patche2 : docs/adr-0028/sim-dettes rc=0
egal a patche2 : docs/G1-lot-DETTES-SIM.md rc=0
r1.py egal a celui de dad3bc6 rc=0
sha256sum -c sim-dettes rc=0 lignes=22
xtask rc=1
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : ROUGE (1 violation(s))
cargo fmt --check : VERT
no_std du vérificateur (construction pour une cible sans bi
cargo clippy -D warnings : VERT
=== VERDICT GLOBAL : ROUGE — l'intégration s'arrête (ADR
  couverture : 141 fichier(s) examiné(s) sur 141 présent(s)
  couverture : 142 fichier(s) examiné(s) sur 142 présent(s)
harnais rc=0
Ran 405 tests in 68.064s
OK (skipped=2)
__pycache__ : 0
08:30:52Z
```

Base `7bfff83-sans-diffs` :

```
base 7bfff83, copie vierge SANS les dix diffs (même extraction et mêmes exclusions) : 7bfff83bf3aa7d60739cb8124941dfc9f8eeb8f1
08:31:02Z
xtask (sans les diffs) rc=1
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : ROUGE (1 violation(s))
=== VERDICT GLOBAL : ROUGE — l'intégration s'arrête (ADR-0013, point 1) ===
S-G9, constat unique, jetons de chemin seuls (aucun texte de document lu) : docs/17-modele-de-menace.md:70 docs/rapports/cartographie-2026-09-29.md:21 
même constat avec les dix diffs (verif/7bfff83) : docs/17-modele-de-menace.md:70 docs/rapports/cartographie-2026-09-29.md:21 
portée de S-G9 : docs/17-modele-de-menace.md docs/08-assumptions.md docs/adr-0028/ANNEXE-A-lots.md docs/adr-0028/ANNEXE-B-items.md 
08:31:19Z
```

Base `0419910` :

```
base 0419910 : 0419910731cad30b88913b5184fbe8b3afcb3fb5
08:31:47Z
apply DS-0 rc=0
apply DS-1 rc=0
apply DS-2a rc=0
apply DS-2b rc=0
apply DS-3a rc=0
apply DS-3b rc=0
apply DS-3c rc=0
apply DS-3d rc=0
apply DS-V rc=0
apply DS-J rc=0
egal a patche2 : scripts/sim rc=0
egal a patche2 : docs/adr-0028/sim-dettes rc=0
egal a patche2 : docs/G1-lot-DETTES-SIM.md rc=0
r1.py egal a celui de dad3bc6 rc=0
sha256sum -c sim-dettes rc=0 lignes=22
xtask rc=1
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : VERT (0 violation(s))
VERDICT : ROUGE (1 violation(s))
cargo fmt --check : VERT
no_std du vérificateur (construction pour une cible sans bi
cargo clippy -D warnings : VERT
=== VERDICT GLOBAL : ROUGE — l'intégration s'arrête (ADR
  couverture : 144 fichier(s) examiné(s) sur 144 présent(s)
  couverture : 145 fichier(s) examiné(s) sur 145 présent(s)
harnais rc=0
Ran 405 tests in 69.294s
OK (skipped=2)
__pycache__ : 0
08:33:16Z
```

Motifs de la gate des secrets de `27189d7` (`enforcement/gate-secrets.sh` l.62-63, extraits par `sed` dans `secrets/motifs-27189d7.sh`), appliqués aux fichiers ajoutés par les dix diffs et à leurs noms de chemin (`secrets/chemins-ajoutes.txt`), drapeaux de la gate : fichiers balayés : 33 ; lignes de contenu en constat : 0 ; noms de chemin en constat : vendor=0 generic=0 ; témoin positif (doit trouver 1) : 1 ; motifs identiques à 7c4861a : oui.

## 7. Livrables (`livrables-g2/`, diffs contre `dad3bc6`)

| fichier | sha256 | lignes ajoutées | identique à la première passe (`livrables/`) |
|---|---|---|---|
| `DS-0.diff` | `6a090bee1f7df4ddd2eff911717ec12498e45c15bd2370ca918ef3942efd3750` | 53 | oui |
| `DS-1.diff` | `d01fcd7a050f61da5e3e9ef345d3727109f474297a23d6648fbaf7b38d7a5009` | 199 | oui |
| `DS-2a.diff` | `da896198d1682abd4c03f01686f772e52d13220e51d5115e6105a2878ef595b9` | 193 | non |
| `DS-2b.diff` | `717865ae69bf51ce9b5588e8a4d3c9b752c5adfa0dd14b98a8c7417df2635b91` | 190 | oui |
| `DS-3a.diff` | `bcffe95843c4a34ade9d97d7c03b1bfa79f0a8793c908c5adb0715c4eb0cb327` | 193 | non |
| `DS-3b.diff` | `4ae145f978a4c51d83b233383d571f923bd5dea185d4138a607386261be8b774` | 162 | oui |
| `DS-3c.diff` | `f932036e1da456f9f7d8a671369beb9763ad8a5d59b2dbf192e643fa0a21cadb` | 148 | oui |
| `DS-3d.diff` | `d1343a28d6fece26cb2125784dbdcdf30cf3c20a61f8791ee1af1d478a0cf2e3` | 150 | oui |
| `DS-V.diff` | `a1a0e3150a60d0e0b995a5ab4ab291a3c74de0002cd703e04b8d28a78a98d1d8` | 33818 | non |
| `DS-J.diff` | `bf67278c8a5608e526624aa8790a404b084e17a43ced8595fdf0495a873ddd72` | 477 | non |
| `G1-lot-DETTES-SIM.md` | `94a0b02f54f39e6df6ef3dbb8d953648dd6662215125e14841b48d1eac580f62` | 477 (lignes du fichier) | non |

## 8. Observations rendues à l'orchestrateur (rien de tu)

- **O-a Base** : le message de l'orchestrateur nomme `dad3bc6` ; la tête du dépôt a avancé sept fois pendant la passe, de `5d45248` à `0419910` (POST-PREREG, DETTES-B2, puis ADR-0029). Les dix diffs s'appliquent sans conflit sur les huit têtes ; la suite `s2-harness` est verte partout (405 tests) ; `xtask verify` est vert sur `dad3bc6`, `5d45248`, `27189d7`, `26c2c41` et `1c2f0f2`, et S-G5, qui balaie le journal, est vert partout. **À `7c4861a`, `7bfff83` et `0419910`, S-G9 est rouge sur la copie (1 constat, le même aux trois têtes ; rouge aussi sans les dix diffs, sur les copies vierges de `7c4861a` et de `7bfff83`)** : le constat unique va de `docs/17-modele-de-menace.md:70` vers `docs/rapports/cartographie-2026-09-29.md:21`, dossier exclu de la copie par le mandat. Le worker n'a extrait de la sortie que ces deux jetons de chemin, sans rien lire de `docs/rapports/`. S-G9 ne porte que sur `docs/17`, `docs/08` et les annexes A et B, aucun fichier du lot (`verif/7c4861a-sans-diffs/verif.txt`, `verif/7bfff83-sans-diffs/verif.txt`). Ce rouge n'est donc pas imputable au lot ; il reste à constater vert sur l'arbre réel au commit. La gate des secrets a changé à `27189d7` ; ses motifs ne trouvent rien dans les fichiers ajoutés, contenu et noms de chemin. La gate elle-même exige un dépôt git et n'a pas été lancée ; elle tournera au commit. Si la tête avance encore avant le commit, il suffit de rejouer `corrections-g2/verifier.sh <tête>`. Aucune base n'a été avancée par le worker.
- **O-b Déclencheur atteint de SHOGEN-POOLEE-NIVEAU-1** : son déclencheur, « lot POST-PREREG (POOLEE-BLOC-1 (a)) », est atteint, puisque PP-c (`ff919a5`, « z poolee par blocs, part (a) ») est au dépôt depuis `dad3bc6`. Le worker n'a lu de PP-c que la ligne de sujet du commit (`git log --oneline`, lecture seule). À la formation de l'item, l'orchestrateur vérifiera si la limite « z_pool sans niveau sous dépendance sérielle synthétique (8,3 % à 33,1 %) » est écrite à côté de la poolée (paquet §4, rapport), ou bien datera le déclencheur.
- **O-c État intermédiaire de C-1 (E-14)** : le worker l'a trouvé et corrigé avant toute livraison ; aucune pièce de cet état n'a quitté le dossier de travail. Les sorties de cet état sont gardées comme historique (`apres-v1/`, `banc-worker-v1/`, `oracles-v1/`, `sim-apres-v1/`), avec leurs sha256 en annexe.
- **O-d Observation O-2 du G2** : `livrables-g2/SHA256SUMS` porte des chemins relatifs à `livrables-g2/` (`sha256sum -c` lancé depuis ce dossier) ; le journal, ses diffs et cette note y figurent.
- **O-e Classement des mutants** : chaque mutant tué l'est avec rc 1 et le message `ECHEC` du contrôle visé ; aucun run n'est sorti hors du contrat {0, 1}, il n'y a donc pas de run FATAL. Les survivants déclarés restent C-geom et A-trou30 (SIM-REGEN-1 élargi, C-3), F-SE (C-5) et D3 (mutant de spécification du worker, journal §4). Hors E-14, aucune limite nouvelle n'est apparue pendant cette passe.

## 9. Provenance de la passe (G1)

- **Lu [lu]** : le rapport G2 en entier, sha256 recalculé ; les brouillons du journal et le pré-enregistrement gelé (`conception/PREENREGISTREMENT-gel-0417.md`, sha256 `d046cf01…8888`) ; `docs/G1-partie-3-S.md` l.355 (L-7) et l'annexe B l.464, pour le rattachement de SIM-PLATEFORME-2 ; les sorties synthétiques du lot (`runs/A`, `runs/B`) et les enregistrements d'oracle. Sur le dépôt, lecture seule : `git rev-parse`, `git log --oneline dad3bc6..5d45248` et `5d45248..27189d7`, `git diff --stat` et `--name-only`, `git archive`, `git show 27189d7:enforcement/gate-secrets.sh` (en-tête l.1-60, motifs l.62-63, lignes d'appel de `grep`).
- **De seconde main [2nd]** : les valeurs que seul le G2 a calculées sont citées comme telles : bootstrap apparié 0,00286 ; taux poolés lot et rejeu, 0,0103 ± 0,0008 et 0,0110 ± 0,0006 ; durée estimée de la mesure ciblée de ZSEUL-2, ≈ 2,1 h.
- **Recompté par le worker** : E[D] de Lomax (`c6/v_lomax_c6.py`) ; écart maximal de B1 par référence sous la règle finale (sur `runs/A`) : `kunsch_premier_ordre` 5,3·10⁻¹¹ (L = 20), `var_K_exacte` 1,8·10⁻¹², `n_sigma2_inf` 1,5·10⁻¹², `E_sigma2_bloc_exacte` 7,2·10⁻¹³, `E_centre_sur_P` 7,3·10⁻¹³ ; rapports |x|/Var(K) des références (`E_sigma2_bloc_exacte` 0,80 à 0,99 ; Künsch 0,0131 à 0,179, nul à L = 1) ; lignes ajoutées des diffs ; lignes et sha256 des `SHA256SUMS`.
- **Commandes** (préfixe `env -u SHOGEN_S2_CAMPAGNE_CONTROL PYTHONDONTWRITEBYTECODE=1`) :
  - bancs : banc du réviseur (copie `banc_g2_copie.py`) sur `sim-avant`, puis sur `sim-apres` avec les témoins ; banc du worker (copie `banc_worker_copie.py`, jeux bp et d3) ; `tol/banc_tol.py` sur `sim-apres-v1` et sur `sim-apres` ;
  - `relance-v2.sh` : lancé détaché (`setsid nohup`), processus 31622, fin constatée par sondage et par le fichier `relance-v2.fin` ; il refait le banc du réviseur, ses témoins, le banc du worker et les quatre rejeux d'oracle ;
  - mise en forme : `faire_diffs.py` (`ARBRE=patche2`), `faire_j10.py`, `maj_j3_j4bis.py`, `assembler.py` (journal), `verifier.sh dad3bc6 5d45248 27189d7`, balayage des motifs de la gate des secrets (boucle `grep` dans le shell courant, sortie `secrets/balayage.out`), `faire_note.py` (cette note).

## Annexe : sha256 des sorties et de l'outillage de la passe (dossier de travail, hors dépôt)

| fichier (`corrections-g2/`) | sha256 |
|---|---|
| `avant/banc.out` | `6225d7c439f25ba343e312228410e2e7ce83cb4268080c28843f9b00713fd45b` |
| `avant/banc-7.out` | `630d1dc83635cf591b387e5b58b8848d294153207e1813ac77687e2c98376db8` |
| `apres-v1/banc.out` | `5061dcd6c9110aeb59bbc65184b79ef542dcb74dc1cdc55f1e3d8de05a6e2b84` |
| `apres-v1/temoins.out` | `550d7782714ce2fff1c22a327fa6067705af49d0487af5bf891687dd46c9bbe3` |
| `apres/banc.out` | `e953931bef46ea92f7625b5728f9b9eec46e55e2c58d9da5abfc4cff9e40c7ab` |
| `apres/temoins.out` | `273c00b08a5e5b0964f94e14a8d530a3bf62c0051718051fe4252813af79017d` |
| `banc-worker-v1/sortie.txt` | `c22b9d3081eec74cfaa48b77254425b9019defc43f945cd0fe781159723392d9` |
| `banc-worker/sortie.txt` | `4b00a61b62b7e400f0ef9ed3a1e2cae1d1f3cc3abc5de96f3478395db06ff7aa` |
| `tol/v1-essai-1.out` | `9e0f9966416b0931b2c0df1076d4a46785c7ff31260e28ab3c4f8c76cc654bd8` |
| `tol/v1.out` | `d59ee17b13745f898be005fdef42bd830d8e5361ca9552aa815f7587cfc54653` |
| `tol/v2-essai-egalite-exacte.out` | `633944165d23f4c7eaa267c2b16618bc9642b67ae43a3daa7994a8c4015f6b96` |
| `tol/v2.out` | `56aba73a71b3dc585f2a23834125cbddaaba049a1ee94d6b20589fa9f3b3535a` |
| `oracles-v1/rejeux.out` | `16a549522e347d24e94a3c3af7dd4655682d64b02d2fca4320054f300a781bd9` |
| `oracles/rejeux.out` | `6bfd52b4757339abc4d32f3e3b0c34956637f6f2254abdf09bbdc87d55944ba6` |
| `secrets/motifs-27189d7.sh` | `3583b7ecb5eebff3287c5bcd77c543d79426c17d3bc07fe16278ccf20cbdd6bd` |
| `secrets/chemins-ajoutes.txt` | `6ceb9b77b362ade6e833293318299e5a6c85e78cc1ff738af7cede4a5651ad62` |
| `secrets/balayage.out` | `6355c4c1c6d197f88505113cff1d3f53018f7ab55b3af21e2b873a269921fbe3` |
| `banc_g2_copie.py` | `6e88c10f608035f00de0b0fbdb1f637fd2f60129018742cd1daaa2f2ad1593f0` |
| `temoins_g2_copie.py` | `dfa8e34ac8ae856ad927a2b0aaa59c9434959adc7e04a99c545addb9fc067013` |
| `banc_worker_copie.py` | `9d2503b2ef61459f6fbb611371672722b1e98a08a46cd424996445f70f696e1e` |
| `tol/banc_tol.py` | `ecfe7848f4ebb617b14725649094a90d153874ea417da9c5baea1b8e1be52e16` |
| `relance-v2.sh` | `42c74f1a2851cf834b5e54fd54ae2830957ab7f56e5d157af29fd63e0acd9fb0` |
| `verifier.sh` | `f62df7b45f46f59bd346a2ed9c2f0ec25189b23f0b34cdfe2352e5ac0ac2f3f9` |
| `faire_diffs.py` | `a042f1173a760df2704536addd9b897a7b259846f2f2a1e331335484d123b134` |
| `faire_note.py` | `f0e250f59db8f1ad40c8f6343878faa8d1cf285c88ff68692fbbbb14e464d786` |
| `note-texte.md` | `68d8afeb9822358e30cff601b4899315aa40b184f91cc6f32b20a3da2aaeae29` |
| `note-fin.md` | `6d4682b152eceda5075ef41f9d5596df0396de662331b4f87c9ae9b82d3a6a7a` |
| `c6/v_lomax_c6.py` | `eaa99d581cd44fa48740c6804766f739211a1c9fb865616835ddaadfc98fbc82` |
| `c6/v_lomax_c6.out` | `33fdb81d53b6e9fdb29016d9be564045ba2a457553a9bd37354233313d6e00d5` |
| `verif/1c2f0f2/verif.txt` | `45c4f1d360c9d22fa44ea3fb59af5805025434cfc096079919e49d5714ead767` |
| `verif/dad3bc6/verif.txt` | `f03e6889c821bf08c2ae7a6dbbf047d905c88ad3af0328cf6dc717ff3329885a` |
| `verif/5d45248/verif.txt` | `d8152205ccdb76730b3f035198cb0911f833960075dbe6d18187ff49dd98b492` |
| `verif/27189d7/verif.txt` | `fc10fe1548a8034dad378dd2a39f698971090d82ff58bb8d7d446f261d25910f` |
| `verif/26c2c41/verif.txt` | `62016c0cfe1fa4558b795e965220aa4e9e4a2686e49b38c8440d2e911a5a37f0` |
| `verif/7c4861a/verif.txt` | `a42b3f098674e342e83f1d286d052b4af053303335718e0712f6f268941f5ac7` |
| `verif/7c4861a-sans-diffs/verif.txt` | `c78d4a51af764a3f455a16a5faff863f279b573dc45df5dde2346bc8850055dd` |
| `verif/7bfff83/verif.txt` | `67d2ceaaead39741e0de2f22c6a5f56085e448bed2d2de3d1ca7de52385bfe63` |
| `verif/7bfff83-sans-diffs/verif.txt` | `d07c790e84c7d840c03df04b6c82c6dd7516f4a4a69a0c3ff1d32696c8e96b2f` |
| `verif/0419910/verif.txt` | `7a9a72a708598a38012e14b5bc4526c482feb5b7657bca7f8d94d391727e03ca` |
