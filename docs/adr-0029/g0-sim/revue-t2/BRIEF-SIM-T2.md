# Brief — lot SIM-BIS, tranche 2 : sous-lots SB-3 et SB-4 (`sources.py`, couche des sources)

Worker `shogen-worker`, effort max. Dépôt `/home/user/shogen` (lecture seule ; **aucune opération git en écriture**). Lis `date -u`
avant toute date. Tu travailles dans `<scratchpad>/s2bis/sim2/` ;
`TMPDIR` dédié.

Base : copie de la tête (`git archive HEAD | tar -x …`, exclusions : `docs/rapports`, `docs/adr-0025`, `docs/adr-0028/monark-m009a`,
`docs/15-*`, `docs/16-*`, `docs/pocket-report`) + la tranche 1, **non encore commise et en relecture G2** : les neuf diffs
`…/s2bis/sim1/diffs/SB-0A.diff` … `SB-5B.diff` (ordre et noms exacts : ceux du dossier et de `…/sim1/SHA256SUMS`), appliqués en série.
Si la G2 change la tranche 1, je te ferai rejouer tes diffs après les siens. Rapport de la tranche 1 : `…/sim1/g2/RAPPORT-WORKER-SIM-T1-transcrit.md`.

Contrat : G0 `docs/adr-0029/g0-sim/G0-SIM-BIS.md` (contenu `PROPOSITION.md` corrigé par `AVIS.md`, qui prime) ; ADR-0029 et ses ajouts
datés. Sous-lots (proposition §6.1 ; la numérotation SB-0 à SB-14 de la proposition fait foi) : **SB-3** (`sources.py` I : processus par
hôte — régime, épisodes empiriques, pannes longues, dérives — sur la grille) et **SB-4** (`sources.py` II : classes jointes par hôte,
incidents cible, grille et ETH, unités faibles, triplets). Exigences E-S-nn rattachées par la proposition ; tests du §6.2.

Adjudications provisoires de l'orchestrateur sur les questions de la tranche 1 (sous réserve de la G2) : **Q-2 / I-1** : SB-3 emploie la
loi « tous épisodes » d'EP, avec une limite écrite (les épisodes censurés allongent la loi) et le constat porté à
SHOGEN-SIM-BIS-STRESS-EPISODES-1 ; PLAN-S2BIS-2 reste le recours prévu par le G0 (Q-S-03). **Q-3** : p = cellules/n_s exact en
`Fraction`. **Q-4** : indice de réplication à partir de 0 ; noms de composants des flux pré-déclarés dans `parametres.json`. **Q-5** :
`math.nextafter` admis (opération IEEE exacte), à confirmer par la G2. **Q-6** : pas de garde réseau dans les tests (frontière `ast`).
**I-3** : aucun `**` ni `pow` sur des flottants dans tes modules (relecture et test `ast` étendu si tu le peux dans le budget).
**I-4** : cache des tables géométriques.

Règles : tests d'abord (rouge avant, vert après) ; au moins dix mutants par sous-lot, **classés par la commande du job (suite entière)
avec borne de temps** (SHOGEN-S2BIS-MUT-COMMANDE-1 ; dépassement = FATAL) ; bibliothèque standard seule ; diffs en série, **chacun ≤ 200
lignes de code ajoutées**, plancher exact relevé ; identité bit à bit (graines, PYTHONHASHSEED, 3.10 à 3.13) ; aucune lecture de journal
de campagne ; R-13, R-8 ; aucune opération réseau ; `cargo --locked xtask verify` sur la copie (lignes de verdict seules ; S-G9
`docs/17:70` connu). Interdits : `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`,
`docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/`, tout `*.jsonl` réel, toute pièce de D.2 ; **aucune recherche récursive
(grep -r, git grep, du, find large) sur `docs/`, sur le dépôt entier ni sur le scratchpad entier**. Rapport par message si le harnais
refuse le fichier ; journal G1 ; SHA256SUMS. Gate 0 (identifiant exact en tête). Résumé court en français.
