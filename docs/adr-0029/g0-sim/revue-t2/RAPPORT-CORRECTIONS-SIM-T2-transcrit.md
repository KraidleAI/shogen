# Rapport du worker — corrections G2 et avis de SIM-BIS tranche 2 (transcrit)

> Transcription par l'orchestrateur le 2026-10-05 03:48:53 UTC du rapport rendu par message par le worker (agent ad452789e9b545ead) ; contrôle FM-1.1 du transcript : fragments_l51_l14 = 0. Texte du worker ci-dessous, sans retouche.

# Rapport du worker : corrections G2 et avis de la tranche 2 de SIM-BIS (SB-4C à SB-4H)

**Gate 0** : je tourne sous `claude-opus-5-5` (identifiant exact), effort max.
**Dates** (`date -u`) : 2026-10-05, de 02:48:59 à 03:47:30 UTC.
**Opérations git** : aucune écriture dans `/home/user/shogen` (lectures seules : `rev-parse`, `status`, `log`, `show`, `archive`).
**Livraison** : `…/s2bis/sim2/corr/`
- `diffs/SB-4C.diff` à `SB-4H.diff` ;
- `etapes/` : e0 = rb4b, puis c4c à c4h ;
- `outils/` et `journal/` ;
- `SHA256SUMS` : 195 entrées, sha256 `60dd6f37d4b678de048b9f842aa11ad926d708476fb636deca28ab5adcf59a1f`, contrôle `sha256sum -c` sans écart.

## Base
- Copie `git archive` de **784ebd2**, la base du brief ; `git status` était vide au départ.
- Exclusions : celles du brief, plus `docs/adr-0028/execution` (pièce interdite par le brief).
- Les six diffs SB-3A à SB-4B passent `--check` et leur sha256 est conforme (121 sur 121). La série obtenue est égale à rb4b à l'octet (17 fichiers sur 17).
- **Écart de base** : pendant le lot, la tête a avancé à cause des commits COLLECTE-BIS parallèles (7058ecd à 122c670, de 02:58 à 03:41). J'ai gardé 784ebd2 comme base.
  - Vérifié : les 12 diffs s'appliquent aussi sur e761fd2 et sur **122c670**, et le job sim-bis y est vert (Ran 93).
  - Sur ces têtes, `gates.yml` ne diffère que par le plancher s2bis (49 → 106, puis 114).
  - Je n'ai rien avancé moi-même.

## Les diffs
Lignes de code ajoutées recomptées par `git apply --numstat` ; le plancher est égal à Ran à chaque étape.

| diff | contenu | code ajouté | plancher |
|---|---|---|---|
| SB-4C | C-1 | 109 | 85 |
| SB-4D | C-2, C-3 | 45 | 87 |
| SB-4E | C-4, C-5, O-2 | 46 | 88 |
| SB-4F | C-6 | 77 | 90 |
| SB-4G | C-7 | 47 | 91 |
| SB-4H | C-8 | 27 | 93 |

Total : 351 lignes de code ajoutées.

## Les corrections, une par une
- **C-1** : classe `TestCasG2` de 10 tests, écrits depuis les prototypes du réviseur ; (g) est neuf (panne initiale avec un horizon de 1 000 fenêtres).
  - Chaque cas est vert sur le code et rouge sous son mutant, R-01 à R-09, R-19, R-22 et R-25 : 12 sur 12 par assertion (`journal/rouges-c1-sous-mutant.txt`).
  - La première version de (c) rougissait R-03 par une ERROR ; je l'ai corrigée pour obtenir un rouge d'assertion.
- **C-2** : `regime_valide()` est appelé en tête de `union()` et dans `regime()`.
  - Avant le code : κ = 1/2 donnait `ALEAS/geometrique`, et à κ = 1, φ = 2 ou τ_D = 0 étaient admis sans refus.
  - Après : `SOURCES/regime` par `pannes()` comme par `etat()` (`constat-avant/apres-c2-c3.txt`).
- **C-3** : une unité faible hors du pool donne `SOURCES/faible`, par `faibles()` comme par `etat()`. Rouge avant le code : « Refus not raised ».
- **C-4** : `refus_puissance` voit désormais :
  - le nom `pow` pris comme valeur ;
  - les attributs `pow`, `ipow`, `__pow__`, `__rpow__` et `__ipow__` sur tout objet, alias compris ;
  - les imports `from operator import` de ces noms ou de `*`.
  - Rouge avant le code : `f = pow` n'était pas vu.
  - R-26 et R-27 sont tués. **R-28 est écrit comme limite** : getattr d'une chaîne calculée, dans les docstrings de `refus_puissance` et `refus_hasard` et dans le README.
- **C-5** :
  - `rattachement` porte `d9cffc0aec3634138f58ba33b9a9679484f2532460b3e5177c0c5ae194648034`, recalculé par `sha256sum` et `git show 784ebd2:…`. La valeur précédente `eeaceb6b…` (435fa12) y est citée comme « avant cet ajout ».
  - `sources.source` cite l'ajout daté du G0 du 2026-10-05 01:45:03, points 3 et 2.
  - Test `test_provenance_c_5`, rouge avant le changement.
- **O-2** : « ≈ » écrit dans la docstring d'`amincir`.
- **C-6** : `sources.indices_hotes` suit l'ordre de l'ADR-0029 l.168 : binance, coinbase, kraken, okx, bitstamp, gemini, bitfinex, coingecko, defillama, chainlink. EP l.8 confirme : aucun retrait.
  - Code : `rang()` ; `indice()` utilise `rang()` ; l'indice des unités faibles est `rang(prm, h)` ; refus `SOURCES/indice` pour un hôte absent ou une liste à doublon ; clé ajoutée au schéma.
  - Tests :
    - pool à rebours ou sans coinbase : état vrai des autres hôtes identique à l'octet, rang 1 inemployé ;
    - unité faible indexée par son rang quelle que soit sa place ;
    - refus.
  - `test_indice_et_longues` est mis à jour : 193 → 73 et 30 → 130.
  - Trois rouges d'assertion avant le code.
- **C-7** : chaque valeur porte sa source (lignes de l'AVIS et de la PROPOSITION).
  - `poids_longues [1, 1, 1]` est branché dans `loi_longues`, avec `SOURCES/loi` si les longueurs diffèrent.
  - `derive.tendance_par_semaine` vaut 10080. Les cinq valeurs Q-T2-6 sont sourcées, avec la mention « rapport 19, même enveloppe que la tendance ».
  - `sources.absorption` contient : population `as13335`, `k_faibles [1, 2, 4]`, `k_bascule 1`. Le partenaire et l'imposé uniforme sont écrits et vérifiés par `touches`.
  - Le test vérifie la présence et la forme sous le schéma ; il est rouge avant le code sur le branchement des poids.
  - DERIVE-AMPLITUDE-1 et ABS-POPULATIONS-1 sont closables.
- **C-8** : deux oracles, tendance et saut. L'écart (part en panne − p·Σm(t)/T), avec m(t) refait à la main, est centré à 5 erreurs-types **dans chaque sens**.
  - z mesurés : −0,48 / −1,35 (tendance) et +1,05 / −0,75 (saut).
  - La version groupée laissait vivre M-C8-03 : les erreurs de signes opposés se compensaient. Je l'ai séparée par sens.
  - Les mutants M-C8-01 à 04 sont rouges par assertion.

## Rejeu par la commande du job
Runner d'abord, puis la ligne de `gates.yml`, borne de 300 s ; campagne finale v3, sur c4h.
- **28 mutants du réviseur** : 27 tués, chacun par son test nommé ; **R-28 vivant** (la limite écrite). R-01 a été adapté en R-01a, parce que la ligne qu'il visait a été réécrite par C-6.
- **80 mutants du worker** : 80 tués par leur test nommé.
  - 4 adaptés par le réviseur : W-3C-05a, W-GEN-3a, W-4A-02a, W-4A-03a.
  - 4 adaptés par moi : M-3C-01b et M-3C-10b (C-6), M-3C-09b (C-7), M-3C-14b (C-2).
- **16 mutants neufs** : M-C6-01 à 06, M-C7-01 à 06, M-C8-01 à 04 ; 16 tués.
- **6 compléments** : M-C2-01, M-C3-01, M-C4-01 à 03, M-C5-01 ; 6 tués.
- **Aucun FATAL.**

## Identité bit à bit
- Inchangée de e0 à c4e : 85c7fbdd… pour la sonde du worker, 9e288226… pour celle du réviseur.
- **Nouvelle empreinte à partir de C-6**, sur 3.10.20, 3.11.15, 3.12.3 et 3.13.14, avec PYTHONHASHSEED 0, 1, 4242 et aléatoire :
  - sonde du worker : `a424e5e84d5fd843d19f1dbddd280ce543a949c259db74c724f4a39ed89c8fc0`, 16 sur 16 ;
  - sonde du réviseur : `a78a9c33a9a86366cbb40b34682458b46413a1d98cb8592bc3a94952846c03c3`, 16 sur 16.
- C-7 ne change aucun tirage.

## Portes, sur la série finale
- Runner : 33 ok. Jobs : sim-bis Ran 93, s2bis 49, s2-harness 405 (skipped=2).
- Hooks 54, model-pinning 95, lint OK, secrets 147 et `--tree` sur un dépôt jetable.
- `cargo --locked xtask verify` sous `unshare -n` (lignes de verdict seules) :
  - S-G1 à S-G8 VERT ; fmt, no_std et clippy VERT ;
  - S-G9 ROUGE sur docs/17:70, déjà connu, identique sur le témoin.
- Toutes les étapes sont vertes à leur plancher exact. c4h passe sous 3.10 à 3.13 avec `-W error`.
- R-13 : aucun marqueur. R-8 : bibliothèque standard seule. Aucun octet 92 dans les fichiers du lot ni dans les diffs.

## Points à former ou à porter (règle PAROXYSME)
1. **Indices et identifiants (Q-S-07 (b))** : `indices_hotes` est écrite en noms courts. À la finale, il faudra une correspondance scellée avec les identifiants DNS ; sans elle, `SOURCES/indice` refuse (le défaut est sûr).
2. **Erratum O-4 du G0** : il changera l'empreinte du G0. Il faudra mettre à jour `rattachement` et la valeur épinglée dans `test_provenance_c_5` dans le même commit. Par ailleurs, `docs/adr-0029/g0-sim/SHA256SUMS` épingle encore `eeaceb6b…` pour le G0.
3. **Surcharge de `longues`** : tout appelant qui surcharge `longues` (SB-11) doit aussi surcharger `poids_longues`.
4. **Durée de la suite** : 5,2 s → 7,6 s.
5. **Restent sans code, comme adjugé** : O-1, O-3, O-5, O-6, Q-T2-2 et les impressions demandées par l'avis.

## Mes écarts
- **E-1** : repli des lignes de plus de 120 caractères, puis docstrings complétées par les mutants, faits après les instantanés. Je l'ai fait par script sur c4c à c4h (texte seul). Rejoué ensuite : jobs, rouges et campagne v3. Les sorties v1 et v2 sont gardées ; la v2 a été arrêtée par moi après le groupe du réviseur.
- **E-2** : des barres obliques inverses dans des commandes :
  - `sed s/…\/…/`, une fois ;
  - des heredocs Python avec `\n` ;
  - `docstrings.py`, qui contient 42 octets 92 ;
  - `tr '\n'` et `\(secrets\)` dans `etapes.sh` et `portes.sh` ;
  - `xargs -d '\n'`.
  Tout a été contrôlé sur les octets écrits.
- **E-3** : `find | wc -l`, `du` et `find -name __pycache__` sur mes **copies** du dépôt (comptes seulement), et `ls` des noms de `docs/` dans la copie. C'est contraire à la lettre de l'interdit si une copie compte comme le dépôt.
- **E-4** : le premier PID consigné, 5239, était le sous-shell parent ; le vrai est 5241.
- **E-5** : une boucle de sondage a été passée en tâche de fond par le harnais, sans effet.
- **E-6** : `test_provenance_c_5` épingle les empreintes à la main, sans lire le G0.
- **E-7** : exposition, toute permise : ADR l.166-170, EP l.1-12 et ses lignes binance, gemini et kraken, PROPOSITION l.130-215 et l.498-516, sujets des commits parallèles. Aucune pièce de D.2, aucun `*.jsonl`, aucun JOURNAL.

## Journal de provenance (G1)
**Lu [lu]** :
- en entier : brief (`c66678cf…`), G2 transcrite (`1a024a3a…`), AVIS-SIM-T2 (`30950295…`), rapport précédent (`f3527a9e…`), G0 (33 lignes, `d9cffc0a…`) ;
- par extraits, comme dit en E-7 : PROPOSITION (`0e78afab…`), ADR (`b908842d…`), EP (`c0371ca5…`), `gates.yml` l.1-20 et l.215-245 ;
- le code du lot ;
- les outils et sorties du réviseur (`rev/`) et du worker (`outils/`, `journal/`) ;
- `revue-t1/SHA256SUMS`.

**Seconde main [2nd]** : aucun chiffre.

**Commandes** : dans `outils/` ; leurs sorties dans `journal/` :
- `rouges-avant-code.txt`, `rouges-c1-sous-mutant.txt`, `rouges-c8-sous-mutant.txt` ;
- `mutants-*.txt` ;
- `identite.txt` ;
- `etapes.txt` ;
- `portes.txt` et `xtask-verdicts-*.txt` ;
- `serie.txt` et `application-tete-*.txt` ;
- `tailles-diffs.txt` ;
- `base-tete.txt`.

**Chiffres** : tous recomptés par mes propres commandes.

Copies lourdes supprimées (base, série, travail, cible, tmp) ; disque : 9,7 Go libres.

