# SHOGEN-G2-HISTO-RECALCUL-1 : inventaire de la couverture G2 du chemin de recalcul

Rédaction : 2026-10-02, 21:2x UTC (`date -u` lu à 21:19:40 au départ, puis à 21:25:26). Lecteur : `shogen-lecteur`.
Dépôt `/home/user/shogen`, branche `partie-4-execution`. Analyse faite à `18cbfb6` ; HEAD est passé à `931854c` pendant la
lecture : `git diff --stat 18cbfb6 HEAD -- s2-harness` est vide, donc aucun module du chemin n'a changé.

## 0. Gate 0, attestation, commandes

**Gate 0.** Modèle résolu : `claude-sonnet-5-5` (identifiant exact fourni par l'environnement de la session ; préfixe
attendu des lecteurs, CLAUDE.md §7 : conforme). Effort : `high` (fiche).

**Attestation (forme D.3), avec exposition déclarée.**
- Aucune pièce de la liste D.2 ouverte : pas de `docs/rapports/`, rien sous `docs/adr-0025/`, aucun `*.jsonl`, rien hors du
  dépôt (donc aucun rapport `F:\tmp\shogen-lots\...`), aucune copie scellée, aucune transcription de session. Aucune
  recherche n'a parcouru `docs/rapports` ni `docs/adr-0025` (les `grep` visent des fichiers nommés ou ont écarté ces deux
  dossiers ; le `grep -rn "39f2b8dd"` a été lancé avec `--exclude-dir=rapports --exclude-dir=adr-0025`). **Une seule
  commande déroge** : `grep -rn -o -E "...(CRITERE|B-DEP-2|B0|DOCS-S2|B-DEP-1)[/\\]G2..." docs JOURNAL.md --include=*.md`, qui
  a parcouru `docs/rapports` et `docs/adr-0025` sans exclusion à la source ; sa sortie était filtrée par
  `grep -v "docs/rapports\|docs/adr-0025"` avant affichage, donc aucune ligne de ces dossiers n'est apparue dans ma
  transcription. Écart à la règle « exclure à la source », à consigner par l'orchestrateur (contrôle FM-1.1).
- Aucun z, K, P̂_more ni φ de campagne vu ni calculé.
- **L'attestation « aucun chiffre de campagne vu » ne tient pas telle quelle.** J'ai vu, dans des pièces que la fiche
  m'autorisait à lire, des valeurs de classe M déjà portées par le dépôt, que je ne recopie pas :
  1. `docs/G2-partie-3.md` l.38-41 : comptes de D1 et de D5, comptes de fenêtres, et **deux pourcentages de
     `resolve_failed` (dans la plage et hors plage)**, qui sont des taux de panne d'un composant de la campagne ;
  2. `JOURNAL.md` l.86, l.92, l.114, l.116, l.131 (lignes lues par `fold` ou par `grep` tronqué) : comptes de fenêtres de
     la campagne, répartis calme/stress, et une durée de stress en heures (l.86) ;
  3. `docs/G1-lot-adr0025-filtre.md` l.126-127 : borne de plage, comptes de fenêtres et durée de stress (erratum du lot A) ;
  4. `docs/adr-0022/G2-review.md` l.83 : un P99 global d'écart de la calibration ADR-0022 (journal de calibration, pas
     la campagne scellée) ;
  5. `docs/G2-partie-3.md` §3 (tableau des commandes) : résultats synthétiques de SIM-NIVEAU (étape S), sans donnée de
     campagne.
  Ces lignes ne contiennent ni z, ni K, ni P̂_more, ni φ. Les points 1 à 4 sont à compter dans la liste des expositions
  de l'annexe D.1 si l'orchestrateur le juge utile.
- Aucune opération git en écriture. Un seul fichier écrit dans le dépôt : aucun ; écrits : ce rapport et des fichiers de
  travail sous `.../scratchpad/p4/` (`hist.txt`, `r2.txt`, `r3.txt`, `blame_*.txt`).

**Commandes lancées** (toutes en lecture) :
- `date -u` ; `git rev-parse HEAD` ; `git status --short` ; `git log -1` ; `git log --format='%h %ad %s'` sans option
  d'écriture, avec et sans `--reverse`, sur `s2-harness/tools/{rendu_unique,oracle_record}.py`,
  `s2-harness/shogen_s2/{report,lm,r1,r2,records,window,model,journal}.py`, `enforcement/lint-model-pinning.sh`
  (sortie : `hist.txt`) ; `git log 18cbfb6..HEAD`, `git diff --stat 18cbfb6 HEAD -- s2-harness`.
- `git rev-list cefe134..6eabaa4` (41 commits) et `git rev-list 0711cc1..86a8a5b` (33 commits), `git rev-parse`,
  `git merge-base --is-ancestor`.
- `git show --stat`, `git show -s --format=%B`, `git show <commit> -- <fichier>` sur `ed479c5`, `a6f3990`, `3ef3b25`,
  `093c076`, `cfc67f5`, `81b8a87`, `04553a7`, `15d831e`, `3a51b7c`, `4d49757`, `54e38ac:docs/G2-partie-2.md`.
- `git blame --line-porcelain HEAD -- <fichier>` sur les neuf modules (classement des lignes par dernier commit).
- `grep -nE` des imports sur `s2-harness/tools/*.py` et `s2-harness/shogen_s2/*.py` ; `grep -n` de `G2`, `rattrapage`,
  `HISTO-RECALCUL`, `G2-rapport`, `sha256` sur `JOURNAL.md`, `docs/G1-*.md`, `docs/G2-*.md`, `docs/adr-0022/*.md`,
  `docs/adr-0028/ANNEXE-A-lots.md`, `ANNEXE-B-items.md`, `ADR-0028-*.md`, `docs/journal-provenance.md`, `docs/DECISIONS.md`.
- `sha256sum` de `docs/G2-partie-2.md`, `docs/G2-partie-3.md`, `docs/adr-0022/G2-review.md`,
  `docs/G1-partie-2-corrections-G2.md`.
- `Read` : `s2-harness/tools/rendu_unique.py` et `oracle_record.py` en entier ; `docs/adr-0028/ANNEXE-D-preenregistrement.md`
  (liste D.2 et attestations seulement, par `sed -n` et `grep`) ; `docs/adr-0028/ANNEXE-B-items.md` l.40-70 ;
  `ANNEXE-A-lots.md` l.1-131 (colonnes tronquées) ; `docs/G2-partie-2.md` l.1-100, l.273-345, l.439-457 ;
  `docs/G2-partie-3.md` l.1-150 ; `docs/adr-0022/G2-review.md` l.1-148 ; `docs/adr-0028/PLAN-PARTIE-4.md` (grep P4).
- Deux petits scripts `python3` (bibliothèque standard) qui classent les lignes de `git blame` par commit et comparent
  aux plages lues par le G2 de la partie 3 ; aucune lecture de journal, aucun réseau.

## 1. Chemin de recalcul : liste exacte

Établie par lecture du code (niveau [lu]).

`rendu_unique.py` charge `tools/oracle_record.py` (`importlib`, l.55-57), puis, dans `produire` (l.389), importe
`from shogen_s2 import lm, r1, r2, records, report`. L'enregistreur lance dans l'extraction du commit, par liste fermée
`COMMANDES` (`oracle_record.py` l.32-34) : `suite` (`python -B -m unittest discover -s tests -t .`) et les cinq runs
`--produire` : `j14-principal`, `j14-second`, `j28` (→ `report.render_report`), `recalcul-tiers`
(→ `r1.recompute_from_journal`, `r1.recompute_d5_from_journal`, `lm.recompute_lm_from_journal`,
`r2.recompute_r2_from_journal`), `raw` (→ `records.verifier_raw`). Imports internes relus : `report` → `r2, records, lm,
r1, window` ; `r1` → `records, model, window` ; `r2` → `r1, records, window` (et `lm` en import paresseux, l.1038) ;
`lm` → `r1` (et `records`, `window` en import paresseux, l.209-210) ; `records` → aucun module du paquet (sauf `journal`
en import paresseux dans `append_asn`, l.278, **jamais appelé** par les commandes de lecture).

**Neuf modules** dans le chemin :

| # | module | rôle |
|---|---|---|
| 1 | `s2-harness/tools/rendu_unique.py` | exécution unique, gardes, `--produire` |
| 2 | `s2-harness/tools/oracle_record.py` | enregistreur, extraction `git archive`, liste fermée des commandes |
| 3 | `s2-harness/shogen_s2/report.py` | rendu des blocs 1 à 6 |
| 4 | `s2-harness/shogen_s2/lm.py` | estimateur L&M |
| 5 | `s2-harness/shogen_s2/r1.py` | R1, D5, règle, contexte décimal |
| 6 | `s2-harness/shogen_s2/r2.py` | R2, drapeau 2 |
| 7 | `s2-harness/shogen_s2/records.py` | lecteur tolérant, filtre, `verifier_raw` |
| 8 | `s2-harness/shogen_s2/window.py` | strates, fin de fenêtre, marqueurs (importé par `r1`, `r2`, `lm`, `report`) |
| 9 | `s2-harness/shogen_s2/model.py` | `Status` (importé par `r1`) |

**Hors chemin de calcul, signalés pour mémoire (non inventoriés au tableau) :**
- `journal.py` : import paresseux non exécuté par les runs ; sa promesse « décodage recalculable » est lue par
  `records.verifier_raw` sans importer le module (l'item SHOGEN-FORMAT-JOURNAUX-1 le cite au commit `ed479c5`).
- `collector.py`, `closure.py`, `run_campaign.py`, `sources.py`, `smoke.py` : chargés seulement par le run `suite`
  (les tests les importent), pas par les runs de sortie. La suite est la première commande de l'exécution unique
  (`RUNS`, `rendu_unique.py` l.54) : leur couverture G2 n'est pas inventoriée ici.
- `enforcement/lint-model-pinning.sh` : donnée lue par `oracle_record.liste_blanche()` (liste blanche des auteurs, l.71-81).
  Historique : `de12b8b`, `84e0462`, `c833ae2`. G2 : D8a (sha `9e8b462f…561b`, `docs/G1-lot-D8a.md` l.325 [lu] la citation ;
  rapport hors dépôt [2nd]) pour les deux premiers ; D8c (`docs/G1-lot-D8c.md` l.445, rapport sans sha propre, diff
  `0dad2bae…6074`) pour le troisième. `G2-partie-3` en a lu la l.33 (`ALLOWED`).

## 2. Références G2 (clés du tableau)

Niveaux : **[lu]** = le rapport G2 est dans le dépôt et je l'ai lu ; **[2nd]** = le rapport est hors dépôt
(`F:\...`), je ne lis que la citation (qui, elle, est [lu] dans le dépôt, avec sa page ou sa ligne) ; **[abs]** = rien.

| clé | G2 | où | sha | niveau |
|---|---|---|---|---|
| **P2** | relecture G2 de la partie 2, périmètre `git diff cefe134 6eabaa4` (41 commits) ; lit `rendu_unique.py` et `oracle_record.py` **en entier** (`428f7dc5…`, `4eb3ed8b…`) et les diffs de `r1, lm, r2, records, report` (§13.1) ; suite rejouée sur chaque commit de code | `docs/G2-partie-2.md` (dépôt) | `0b45a458a53878f70b5826653eecc82615b980d7f57ce0317bee5c20391914d9`, **recalculé par moi sur le fichier du dépôt, égal au préfixe `0b45a458…` cité en JOURNAL l.228** | [lu] |
| **P3** | relecture G2 de la partie 3, périmètre `git log 0711cc1..86a8a5b` ; diffs de `b47ff24`, `a4e44d0`, `ced5cb6`, `a6a99d8`, `d69c914` ; lectures partielles de `rendu_unique.py` (l.6-37, 77-160, 161-176, 177-240, 264-345, 395-540) et de `oracle_record.py` (l.39-42, 72-88, 136-137) ; sites `localcontext` comptés par `grep` dans `r2`, `report` | `docs/G2-partie-3.md` (dépôt, versé tel quel) | fichier du dépôt `c6e3962a440c0a32be9eb332c3807da538e3e5c6cbf0430ec96f3474dc20c138` (mesuré) ; source citée `d8d70a09…` (en-tête l.3 et JOURNAL l.264) | [lu] |
| **A22** | revue G2 de la passe ADR-0022 (τ par classe), diff de `ed479c5` (13 fichiers : `r1`, `records`, `lm` 1 ligne) ; verdict : points 1-5 et 7 PASS, D1 (report de `closure` non déclaré) et D2 (documentation de `run_campaign.py`) ; **D1 corrigé** par l'amendement d'`ADR-0022.md` l.56 [lu] ; D2 est hors chemin (`run_campaign.py`) | `docs/adr-0022/G2-review.md` (dépôt) | aucun sha cité ; fichier du dépôt `9cc1a073f91a4016852c068cd17b7e8ee3348fe433b8379df351198069ce54f2` (mesuré) ; l'`oracle-post-d2.txt` est cité au journal de provenance l.29 | [lu] |
| **LA** | G2 du lot A (filtre d'exclusion ADR-0025, `742f1fc`) : ACCEPTE-AVEC-CORRECTIONS C-1..C-5, « code accepté tel quel », corrections = tests, erratum, provenance (zéro code) | `F:\tmp\shogen-g2-lotA\G2-lot-A-ADR-0025.md` ; cité `docs/G1-lot-adr0025-filtre.md` l.125-129, `docs/journal-provenance.md` l.30, JOURNAL l.92 | `39f2b8dd…` (tronqué, l.129) | [2nd] |
| **B0** | G2 du lot B0 (`0abc881`) : ACCEPTE-AVEC-CORRECTIONS C-1..C-6 ; corrections intégrées au même commit `0abc881` (texte proposé par le réviseur, un écart de date déclaré) | `F:\tmp\shogen-lots\B0\G2-rapport.md` ; cité `docs/G1-lot-B0-pool-analyse.md` l.218 et l.223 | `1c2d2b32…d892` (tronqué) | [2nd] |
| **BS1** | G2 de B-SEG-1 (`dc39cb8`, `83f86d8`) : C-1..C-6 ; corrections C-1..C-3 en tests seuls (B-SEG-1c, aucune ligne de `shogen_s2/`) | `F:/tmp/shogen-lots/B-SEG-1/G2-rapport.md` ; cité `docs/G1-lot-B-SEG-1-segment.md` l.205 et ANNEXE-B l.85 | `cc8f2b50dd33df44b70af460104ab796c0398e948fab25e8e6ea1c33fe1e9c5c` (complet) | [2nd] |
| **BS2** | G2 de B-SEG-2 (`c385d52`, `8878200`, `5e0c09b`) : C-1..C-9 ; C-1..C-5 « tel quel » = `5e0c09b` | `F:/tmp/shogen-lots/B-SEG-2/G2-rapport.md` ; cité `docs/G1-lot-B-SEG-2-bloc1.md` l.257, ANNEXE-B l.169 | `e778cef1b224436e925502f5502f68430bea4d01995d374373efeafb21d222de` | [2nd] |
| **B** | G2 du lot B (`082d457`, `e47a425`, `cf2a1ba`, `b923a71`) : C-1..C-10 ; `b923a71` = corrections C-1..C-5 « texte du réviseur tel quel » (message de commit [lu]) | `F:/tmp/shogen-lots/B/G2-rapport.md` ; cité `docs/G1-lot-B-sensibilite.md` l.231, ANNEXE-B l.205 | `473071596f0897c959cffab411bd9674f36ea95f28460d16c9279be04d62bef8` | [2nd] |
| **PO** | G2 de POOLEE (`57d1857`, `f70421b`) ; POOLEE-c = tests seuls | `F:/tmp/shogen-lots/POOLEE/G2-rapport.md` ; cité `docs/G1-lot-POOLEE-strate-poolee.md` l.224, ANNEXE-B l.219 | `d5d87ca9a2fbdd45dd3e1b63650b277d3b14a6b549cc6dbe637c8af52ca06ce7` | [2nd] |
| **BD1** | G2 de B-DEP-1 (`6c524a5`, `09c1a50`, `d0b9663`) : C-1..C-7 ; C-1..C-4 posées « tel quel » (`corrections-G2-B-DEP-1.diff`) | `F:/tmp/shogen-lots/B-DEP-1/G2-rapport.md` ; cité `docs/G1-lot-B-DEP-1-blocs.md` l.286 | `5cd2ff401bf041d86b027c73e1a07954753551a39a4a31ff4b2a7ead36c1f11e` | [2nd] |
| **BD2** | G2 de B-DEP-2 (`1775309`) : C-1..C-4 (JOURNAL l.189) ; la revue a rejoué le lot sur `c61ebc5` | `F:/tmp/shogen-lots/B-DEP-2/G2-rapport.md` ; cité `docs/G1-lot-B-DEP-2-bloc3.md` l.16 | **aucun sha cité** | [2nd] |
| **CR** | G2 du lot CRITERE (`d23706a`, `ca6011c`, `eb3453d`, `6c57039`, `3a51b7c`) : C-G2-1..6 ; Q-G2-1 option (a) recommandée par la revue (JOURNAL l.191), appliquée en `3a51b7c` | JOURNAL l.191 et message de `3a51b7c` seulement ; **aucun chemin ni sha cité dans le dépôt** | aucun | [2nd] |
| **DA** | G2 de D5-AMEND (`8de4062`, `8b9ec48`, `b323f03`) : C-1..C-3 | `F:/tmp/shogen-lots/D5-AMEND/G2-rapport.md` ; cité `docs/G1-lot-D5-AMEND-descriptifs.md` l.181, ANNEXE-B l.314 | `fd731fedbadcd275533ef3a6f64da6e7fb0492f2ef6965715726d9cc834efdf0` | [2nd] |
| **DS** | G2 de DOCS-S2 (sous-lot a, `4d49757` : commentaires et docstring de `r2.py`, 5 lignes) : C-1..C-10 (JOURNAL l.135) | rapport non nommé dans le dépôt (`docs/G1-lot-DOCS-S2.md` l.7 et l.89 le mentionnent) | aucun | [2nd] |
| **PA** | « oracle de recalcul + G2 à contexte frais » des incréments Phase A du 2026-08-20 (`f11bdca`, `432a0a5`, `0ca2b96`) ; « corrections C-A/C-B » pour `0ca2b96` | JOURNAL l.41 ; `docs/journal-provenance.md` l.25-27 (lignes de rattrapage reconstituées) ; **rapports non localisés** (ADR-0028 l.193 le déclare) | aucun | [2nd] déclaré, rapport [abs] |
| **A21** | passe ADR-0021, `8c58207` : « G2 (réviseur ≠ générateur, 8/8, aucun affaiblissement de test) » et oracle de recalcul | JOURNAL l.42 ; `docs/journal-provenance.md` l.23 ; **rapport non localisé** | aucun | [2nd] déclaré, rapport [abs] |
| **CORR2** | corrections G2 de la partie 2 (`3ef3b25`, `093c076`, `cfc67f5`, `81b8a87`, `04553a7`) : écrites par un correcteur après le G2 de la partie 2 (`docs/G1-partie-2-corrections-G2.md` l.3 : « liste fermée … appliquée telle quelle », mais le G2 §10 ne donne que la « construction attendue », pas le code) ; adjudication par l'orchestrateur (JOURNAL l.230, l.232), **pas de réviseur distinct** | `docs/G1-partie-2-corrections-G2.md` (sha `736516587f39…26e0`, mesuré, égal au préfixe `73651658…` de JOURNAL l.230) | — | [lu] pour la description, **aucun G2** |
| — | `a6f3990` (2026-08-05, `model.py`) : « tested », ADR-0008 acceptée ; aucune mention de G2 | message de commit [lu] ; aucune ligne de JOURNAL ni de provenance | — | [abs] |

## 3. Tableau : module | commits (ancien → récent) | G2 couvrant | lacune

Notation des commits : sha court. « P2 » etc. : clés de la section 2. Les corrections de lots (`0abc881` pour B0, `5e0c09b`,
`b923a71`, `d0b9663`, `3a51b7c`) sont couvertes au titre du G2 du lot (texte du réviseur appliqué), sans re-revue ; seuls
D8a et D8b ont eu une re-revue ciblée (rr1), hors chemin.

### 3.1 `s2-harness/tools/rendu_unique.py` (504 lignes)

| commits | G2 couvrant | niveau | lacune |
|---|---|---|---|
| `f939c05` `b25d394` `e52b216` `6e779e1` `a530dbd` `c2cdbc1` `4d42859` `3626c71` `397605c` (tous 2026-10-02, partie 2, étape C) | **P2** (fichier lu en entier à `6eabaa4`) | [lu] | aucune |
| `3ef3b25` (G2a) `093c076` (G2b) `cfc67f5` (G2c) `81b8a87` (G2d) `04553a7` (G2e) | **CORR2** ; hors des deux périmètres (voir §4, G-3) | [lu] (aucun G2) | **G-3** |
| `a4e44d0` (P3c) `ced5cb6` (P3d) `a6a99d8` (P3e) `d69c914` (P3f) | **P3** (diffs lus ; constats P3c à P3f) | [lu] | aucune |

Lignes de HEAD par dernier auteur (`git blame`) : 388 dans la plage P2, 31 dans la plage P3, 85 dans CORR2.

### 3.2 `s2-harness/tools/oracle_record.py` (274 lignes)

| commits | G2 couvrant | niveau | lacune |
|---|---|---|---|
| `0ad3655` `cbd3f7d` `ff4ce8c` `6fde16b` `e5d989b` `124e2e9` `c2cdbc1` `4d42859` (partie 2, étapes B et C) | **P2** (fichier lu en entier) | [lu] | aucune |
| `3ef3b25` (G2a : `verifier` exige les runs `suite` puis `PRODUCTION`, l.191-192, l.225-226) | **CORR2** ; P3 n'a lu que l.39-42, 72-88, 136-137 | [lu] (aucun G2) | **G-3** |

### 3.3 `s2-harness/shogen_s2/report.py` (786 lignes)

| commits | G2 couvrant | niveau | lacune |
|---|---|---|---|
| `f11bdca` `432a0a5` `0ca2b96` (2026-08-20) | **PA** | [2nd] | **G-1** |
| `8c58207` (2026-08-20) | **A21** | [2nd] | **G-1** |
| `742f1fc` (2026-09-28) | **LA** | [2nd] | sha tronqué (G-4) |
| `0abc881` (2026-09-30) | **B0** | [2nd] | sha tronqué (G-4) |
| `dc39cb8` `83f86d8` | **BS1** | [2nd] | aucune (sha complet) |
| `c385d52` `8878200` `5e0c09b` | **BS2** | [2nd] | aucune (sha complet) |
| `082d457` `e47a425` `cf2a1ba` `b923a71` | **B** | [2nd] | aucune (sha complet) |
| `f70421b` | **PO** | [2nd] | aucune (sha complet) |
| `1775309` | **BD2** | [2nd] | **G-4** (sha non cité) |
| `eb3453d` `6c57039` `3a51b7c` | **CR** | [2nd] | **G-4** (ni chemin ni sha) |
| `b323f03` | **DA** | [2nd] | aucune (sha complet) |
| `37db486` `1ed1c29` `270d09a` `1c35b49` `5cb791e` `24dd734` | **P2** | [lu] | aucune |
| `b47ff24` `a4e44d0` | **P3** (diffs lus ; `a4e44d0` sur `report.py` : comptage `grep` des sites) | [lu] | aucune |

Lignes de HEAD : 354 dont le dernier auteur est PA, 256 sous G2 hors dépôt à sha cité, 93 sous G2 sans sha, 77 P2, 6 P3.

### 3.4 `s2-harness/shogen_s2/lm.py` (239 lignes)

| commits | G2 couvrant | niveau | lacune |
|---|---|---|---|
| `432a0a5` `0ca2b96` | **PA** | [2nd] | **G-1** |
| `8c58207` | **A21** | [2nd] | **G-1** |
| `ed479c5` (1 ligne, passe-plat de `tau`) | **A22** | [lu] | aucune |
| `742f1fc` | **LA** | [2nd] | sha tronqué (G-4) |
| `0abc881` | **B0** | [2nd] | sha tronqué (G-4) |
| `dc39cb8` `83f86d8` | **BS1** | [2nd] | aucune |
| `270d09a` | **P2** | [lu] | aucune |
| `a4e44d0` | **P3** (comptage `grep` : « lm 3 » sites) | [lu] partiel | aucune |

Lignes de HEAD : 215 dont le dernier auteur est PA.

### 3.5 `s2-harness/shogen_s2/r1.py` (836 lignes)

| commits | G2 couvrant | niveau | lacune |
|---|---|---|---|
| `f11bdca` `432a0a5` `0ca2b96` | **PA** | [2nd] | **G-1** |
| `8c58207` | **A21** | [2nd] | **G-1** |
| `ed479c5` | **A22** | [lu] | aucune |
| `742f1fc` | **LA** | [2nd] | sha tronqué (G-4) |
| `0abc881` | **B0** | [2nd] | sha tronqué (G-4) |
| `dc39cb8` `83f86d8` | **BS1** | [2nd] | aucune |
| `57d1857` | **PO** | [2nd] | aucune |
| `6c524a5` `09c1a50` `d0b9663` | **BD1** | [2nd] | aucune |
| `d23706a` `ca6011c` | **CR** | [2nd] | **G-4** |
| `8de4062` `8b9ec48` | **DA** | [2nd] | aucune |
| `957525a` `270d09a` `5cb791e` `24dd734` `4d42859` | **P2** | [lu] | aucune |
| `a4e44d0` | **P3** (diff de `r1.py` lu) | [lu] | aucune |

Lignes de HEAD : 456 dont le dernier auteur est PA ou A21, 235 sous G2 hors dépôt à sha cité, 31 sans sha, 31 A22, 58 P2, 25 P3.

### 3.6 `s2-harness/shogen_s2/r2.py` (1 092 lignes)

| commits | G2 couvrant | niveau | lacune |
|---|---|---|---|
| `0ca2b96` (M1c : R2, k_eff, drapeau 2) | **PA** (« corrections C-A/C-B ») | [2nd] | **G-1** (1 016 lignes de HEAD) |
| `8c58207` | **A21** | [2nd] | **G-1** |
| `742f1fc` | **LA** | [2nd] | sha tronqué (G-4) |
| `0abc881` | **B0** | [2nd] | sha tronqué (G-4) |
| `dc39cb8` `83f86d8` | **BS1** | [2nd] | aucune |
| `4d49757` (commentaires, 5 lignes) | **DS** | [2nd] | **G-4** (sans effet de calcul) |
| `ca6011c` `3a51b7c` | **CR** | [2nd] | **G-4** |
| `270d09a` | **P2** | [lu] | aucune |
| `a4e44d0` | **P3** (comptage `grep` : « r2 10 » sites) | [lu] partiel | aucune |

Note : `r2.py` n'est pas touché par `ed479c5` ; A22 le cite seulement en lecture (passe-plat de `tau`, l.918 et l.1036 de l'époque).

### 3.7 `s2-harness/shogen_s2/records.py` (419 lignes)

| commits | G2 couvrant | niveau | lacune |
|---|---|---|---|
| `f11bdca` `432a0a5` `0ca2b96` | **PA** | [2nd] | **G-1** |
| `8c58207` | **A21** | [2nd] | **G-1** |
| `ed479c5` | **A22** | [lu] | aucune |
| `742f1fc` | **LA** | [2nd] | sha tronqué (G-4) |
| `dc39cb8` `83f86d8` | **BS1** | [2nd] | aucune |
| `8878200` | **BS2** | [2nd] | aucune |
| `1c35b49` `fd498a0` `24dd734` | **P2** | [lu] | aucune |
| `04553a7` (G2e, C-8 : refus nommé des `ts` non numériques, l.33, l.355-357, l.369-372) | **CORR2** | [lu] (aucun G2) | **G-3** |

### 3.8 `s2-harness/shogen_s2/window.py` (139 lignes)

| commits | G2 couvrant | niveau | lacune |
|---|---|---|---|
| `f11bdca` `432a0a5` (aucun commit depuis le 2026-08-20) | **PA** | [2nd] | **G-1** ; aucun G2 ultérieur ne le cite (grep sur `docs/G2-*.md`, `docs/adr-0022/G2-review.md`, journaux G1 : seule mention, `docs/G1-partie-2-etape-B-3.md` l.35, une lecture du G1, pas un G2) |

### 3.9 `s2-harness/shogen_s2/model.py` (70 lignes)

| commits | G2 couvrant | niveau | lacune |
|---|---|---|---|
| `a6f3990` (2026-08-05, incrément 1 « jetable ») | aucun G2 déclaré : le JOURNAL a été instancié le 2026-08-12 et la ligne de rattrapage du 2026-08-20 (l.41) commence à `f11bdca` ; `docs/journal-provenance.md` ne porte pas `a6f3990` | [abs] | **G-2** |

## 4. Liste fermée des lacunes et G2 de rattrapage proposés

Périmètre minimal : commit et fichier. Compte de lignes = lignes de `HEAD` dont le dernier auteur est le commit (`git
blame`), à titre d'indication ; un G2 de rattrapage relit les diffs des commits, pas seulement les lignes survivantes.

**G-1. Phase A et ADR-0021 : G2 déclarés, rapports non localisés** (JOURNAL l.41, l.42 ; ADR-0028 l.193 ; `journal-provenance.md`
l.23-27). Niveau [2nd] déclaré, rapport [abs]. C'est la plus grosse part du chemin.
- Commits : `f11bdca`, `432a0a5`, `0ca2b96` (2026-08-20), `8c58207` (2026-08-20).
- Fichiers et lignes de HEAD touchées en dernier par eux : `r2.py` (1 032), `r1.py` (456), `report.py` (354), `records.py`
  (245), `lm.py` (215), `window.py` (139).
- Proposition : **un G2 de rattrapage** par un réviseur neuf (≠ générateur, ≠ rédacteur de ce rapport), sur les diffs
  `git diff f11bdca^ 8c58207 -- s2-harness/shogen_s2/{r1,r2,lm,records,report,window}.py`, jugé contre l'état de `HEAD` pour
  ce qui a survécu ; `r2.py` et `r1.py` d'abord (plus gros). À fusionner avec G-2 (même nature : instrument jetable
  ancien). Condition de clôture de G-1 : ou bien un rapport versé dans le dépôt avec son sha256, ou bien la déclaration
  datée que les rapports du 2026-08-20 ne seront pas retrouvés et que ce G2 en tient lieu.

**G-2. `model.py` : aucun G2 déclaré** (`a6f3990`, 2026-08-05, 70 lignes ; seul module du chemin dans ce cas).
- Proposition : relecture de `s2-harness/shogen_s2/model.py` en entier, avec l'usage de `Status.PANNE_TRANSPORT` par
  `r1.py` (l.55 et l.76). Périmètre minimal : un fichier, un commit.

**G-3. Corrections G2 de la partie 2 : ni dans le périmètre de P2 ni dans celui de P3.** `docs/G2-partie-2.md` s'arrête à
`6eabaa4` ; `docs/G2-partie-3.md` part de `0711cc1`, postérieur à ces cinq commits (`git rev-list 0711cc1..6eabaa4` est vide ;
`6eabaa4` est ancêtre de `0711cc1`). Les cinq commits ont été écrits par un correcteur et adjugés par l'orchestrateur
(JOURNAL l.230, l.232), sans réviseur distinct. P3 a lu l'état final de `rendu_unique.py` par plages seulement. Lignes de HEAD
**non lues** par P3 et dernières écrites par ces commits :
- `rendu_unique.py` : l.346-350, l.375-377, l.391-394 (`81b8a87`, G2d : temporaire interrompu, séparation de stderr) ;
  l.374, l.378-382 (`3ef3b25`, G2a : jeton de production) ; l.250, l.255-263 (`cfc67f5`, G2c : ordre du scellement et du go)
  ; l.48-49, l.52-53 (`04553a7`, G2e : étiquettes) ;
- `oracle_record.py` : l.191-192, l.225-226 (`3ef3b25`, vérification des runs au rôle « rendu ») ;
- `records.py` : l.33, l.355-357, l.369-372 (`04553a7`, refus nommé des `ts` non numériques).
`093c076` (G2b, 25 lignes) tombe entièrement dans des plages que P3 a lues, mais comme état final, sans verdict sur C-2.
- Proposition : **G2 de rattrapage borné** sur `git diff 6eabaa4 0711cc1 -- s2-harness/tools/rendu_unique.py
  s2-harness/tools/oracle_record.py s2-harness/shogen_s2/records.py` (commits `3ef3b25`, `093c076`, `cfc67f5`, `81b8a87`,
  `04553a7` ; `15d831e` est tests seuls et n'est pas un module du chemin). Mutants du réviseur de P2 (`liste_g2.py`) à
  rejouer sur ces trois fichiers. C'est le plus petit et le plus urgent : ce code est dans le script scellé
  (`sha256_script`) et dans le code d'analyse (garde (2)).

**G-4. G2 de lot hors dépôt dont le sha n'est pas cité en entier, ou n'est pas cité** (item : « rapport et sha »). Niveau [2nd]
partout : les rapports sont sur `F:\`, que je n'ai pas le droit d'ouvrir.
- sha tronqué : lot A (`742f1fc` ; `39f2b8dd…`, `docs/G1-lot-adr0025-filtre.md` l.129), B0 (`0abc881` ; `1c2d2b32…d892`,
  `docs/G1-lot-B0-pool-analyse.md` l.218) ;
- chemin cité, sha non cité : B-DEP-2 (`1775309`, `report.py` ; `docs/G1-lot-B-DEP-2-bloc3.md` l.16) ;
- ni chemin ni sha dans le dépôt : CRITERE (`d23706a`, `ca6011c`, `eb3453d`, `6c57039`, `3a51b7c` ; `r1.py`, `r2.py`,
  `report.py`), DOCS-S2-a (`4d49757` ; `r2.py` : 5 lignes de commentaires et de docstring, sans effet de calcul).
- Proposition : ce n'est pas un G2 de rattrapage de plein droit. **Première action : relever sur le poste local le sha256
  complet de chaque `G2-rapport.md`** (lot A, B0, B-DEP-2, CRITERE, DOCS-S2) et le consigner à l'annexe A ou au JOURNAL.
  **Si un rapport est introuvable**, G2 de rattrapage borné, dans cet ordre : CRITERE (`d23706a..3a51b7c` sur `r1.py`,
  `r2.py`, `report.py`, car la règle scellée y est écrite), puis B-DEP-2 (`1775309`, `report.py`). `4d49757` ne justifie aucun
  rattrapage (commentaires).

## 5. Remarques sans lacune

- **Aucun G2 de lot n'est lisible dans le dépôt**, sauf P2, P3 et A22 : les neuf G2 de lots (LA, B0, BS1, BS2, B, PO, BD1,
  DA, plus BD2, CR, DS) sont [2nd]. Pour LA, BS1, BS2, B, PO, BD1, DA, la citation avec sha complet est dans le dépôt (sauf LA
  et B0, tronqués) : « référence et sha » est satisfait, la relecture du contenu ne l'est que par ces citations.
- **A22 a rendu un verdict de réserve** (« pas de PASS propre tant que D1 et D2 ne sont pas corrigés ») ; D1 est corrigé
  dans l'ADR (l.56), D2 porte sur `run_campaign.py` (hors chemin) ; je n'ai pas vérifié D2 sur le fichier.
- **Écart de compte** : `docs/G2-partie-3.md` §0 annonce 28 commits pour `0711cc1..86a8a5b` ; `git rev-list` en donne 33 dans
  le dépôt actuel (0 commit de merge). Je n'explique pas l'écart (non investigué : il aurait fallu lire le brief de P3, hors
  périmètre). Dans cette plage, `git log -- s2-harness/shogen_s2 s2-harness/tools` ne retient que `d69c914`, `a6a99d8`, `ced5cb6`,
  `a4e44d0`, `b47ff24` : tous diffés par P3. À signaler à l'orchestrateur, sans conséquence sur le tableau.
- **Désaccord apparent des comptes de corrections** : le JOURNAL annonce C-1..C-10 pour B et POOLEE ; l'annexe A ne porte
  que C-1..C-5 (B-c) et C-1..C-3 (POOLEE-c) comme lignes de code ou de tests (les autres sont des items ou de la
  provenance). Non vérifié sur les rapports ([2nd]).
- **P3 sur `a4e44d0`** : seul le diff de `r1.py` a été lu ; les hunks de `lm`, `r2`, `report`, `rendu_unique` ont été comptés
  par `grep` (30 sites). Je le classe « lu partiel », sans lacune, la modification étant mécanique (fabrique de contexte).
- Mon classement par `git blame` est un indicateur de masse (lignes survivantes), pas une preuve de couverture : un G2
  couvre des diffs, et une ligne peut avoir été relue avant d'être réécrite.
