# G1 — lot E1 d'ADR-0028 (modèle de menace, D10 ; F-DP-10 ; SHOGEN-E1-THREAT-MODEL-1), Shōgen — journal

- **Modèle** : `claude-opus-5-5` (déclaré par le harnais), effort max, contexte frais ; worker G1 (R-1 déclaré en tête de session). Aucun commit, aucun workflow déclenché (R-20). Aucune variable `GIT_DIR` ni `GIT_WORK_TREE` posée, aucun `--write-tree`. Écritures git limitées au worktree du lot : `git merge --ff-only aa0afdc` sur sa branche (§0), puis `git add -N .` pour produire le diff prescrit. Correction de la revue G2 (§15) : G1 de correction `claude-opus-5-5`, effort max, contexte frais, distinct du réviseur ; écritures git dans ce worktree seulement : `git merge --ff-only f5b8269` puis `cf696bd`, `git rm --cached` de la copie du G0, `git add -N .`.
- **Horloge** (`date -u`) : début 2026-09-30T05:11:25Z ; base basculée 05:18:26Z ; O-1 sur la base 05:20:03Z-05:21:40Z ; estimation R-25 écrite 05:24Z, avant tout texte du lot (§1) ; fiche éditeur et fiche CSRC lues 05:3xZ ; `verif_refs.py` écrit 05:3xZ-05:4xZ, avant docs/17 ; E1-a figé 05:53:21Z ; campagne O-3 n° 1 05:56Z-05:58Z ; E1-b écrit 06:0xZ ; relecture de fidélité et reprise de trois cellules, puis nouveau gel des deux sous-lots 06:12Z ; O-2 finals 06:12:57Z-06:13:29Z ; O-3 finals 06:13:35Z-06:18:29Z ; O-1 d'E1-a 06:18:46Z-06:19:58Z ; journal 06:21Z-06:4xZ ; O-1 finals et diffs au rapport G1.
- **Mandat** : commande de mission de l'orchestrateur Shōgen (`claude-fable-5-1`, 2026-09-30), lot E1 de l'annexe A, avec le G0 accepté (`F:/tmp/shogen-lots/E1/G0-lot-E1.md`, sha256 `1a4619caf55d82438d0b20e8fc8d6e209b6e0d2c5190ed53858bfcbac7d0a975`) et les corrections C-1 à C-7 du cp-1 complet (`F:/tmp/cp1-E1/CP1-E1.md`, sha256 `f87b0a45db92313af01fd059af0cb8d71803ea00b5b5b3b330f1635e5aa99606`, ACCEPTE-AVEC-CORRECTIONS).
- **Classification** : document. Le lot n'écrit aucun code ; il écrit une table fermée menaces x contrôles, dont chaque cellule se résout mécaniquement dans le gel (§4).
- **Résultat** : deux sous-lots empilés, E1-a (surface servie, transport, vérificateur, chaîne, méthode) et E1-b (chemin S2), chacun sous le seuil de 200 lignes : 118 et 41 lignes mesurées au G1, 116 et 41 après la correction de la revue G2, tout texte compté (§1). O-1 VERT ; O-2 sortie 0 sur chaque gel ; O-3 : 32 mutants tués sur 32 (E1-a), 34 sur 34 (E1-b), témoins à 0. Au G1, E1-b dépendait de C-6 (§0) ; depuis `f5b8269`, SHOGEN-E1-D2-COMPLETUDE-1 est défini par l'orchestrateur (annexe B.6) ; à la base rebasée `cf696bd`, O-2 d'E1-b sort 0 sans acte à poser (§15).

## 0. Préconditions mesurées avant texte

- **Base du G1** : `aa0afdc` (`main` au lancement, relevé 05:18:26Z). Le worktree du harnais était sur sa branche à `fa0ce5b`, ancêtre de `fb089dc` et de `aa0afdc`. La commande de mission nomme `fb089dc` ; le G0 (§1) fixe la base à la HEAD du lancement, au moins `6f3b9a7`. Motifs mesurés : à `fb089dc`, O-1 est ROUGE (S-G6, en-tête d'INDEX, G0 §10.1) et l'annexe B s'arrête à B.4, si bien qu'un bloc en fin d'annexe y prendrait le numéro de B.5 (SHOGEN-SEG-DEMARRAGE-1, ajouté à `6f3b9a7`). Acte du worker : `git merge --ff-only aa0afdc` sur la branche du worktree (l'avance passe par `fb089dc`). Le cp-1 a mesuré `git diff --stat 6f3b9a7 aa0afdc` = `JOURNAL.md` seul. E-1 (§9).
- **MONARK** : HEAD `4b4ec66e5e7c9e581961947597efa3a177b3cdad` au lancement (G0 : `b27e5e9`). `git diff --stat` entre les deux, sur `apps/harness/src`, `apps/site/data`, `packages/monark/src` et `fixtures` : vide ; les commits intermédiaires touchent `apps/dojo`, `docs` et `test` seulement. Règle du G0 §9 pt 5 (sha fixé au lancement du G1) : docs/17 cite `F:/Monark@4b4ec66e5e7c9e581961947597efa3a177b3cdad`. Lecture seule, `git -C F:/Monark show` et `git archive` vers `F:/tmp/shogen-lots/E1/work/monark/`.
- **C-6 non posée au lancement** : à `aa0afdc`, la ligne E1 de l'annexe A (l.32) porte encore l'ancien oracle et la taille de 150 à 250 lignes ; SHOGEN-E1-D2-COMPLETUDE-1 a 0 occurrence à l'annexe B, dans le commit comme dans l'arbre du dépôt principal (lu par chemin, sans git). Ce sont des actes de l'orchestrateur : ce G1 ne les écrit pas (précédent : `docs/G1-lot-B0-pool-analyse.md:13`). Leur texte, repris à l'octet du G0 (§12 et §8.1), est livré à part, hors du diff du lot (`F:/tmp/shogen-lots/E1/actes-orchestrateur-C6.diff`, construit par `oracles/actes_c6.py`). E1-a n'en dépend pas : docs/17 §1 à §6 cite le lot E1, présent à l'annexe A, jamais E1-a ni E1-b. **E1-b n'est consommable au G2 et au G7 qu'après la pose de C-6** ; O-2 sur E1-b est rejoué avec et sans ces actes (§4). *Correction du 2026-09-30 (revue G2, C-G2-1 iv)* : à `f5b8269`, l'orchestrateur a inscrit l'item à l'annexe B.6 ; la proposition d'item de ce diff est caduque, la moitié A-1 reste due (Q-G1-2).
- **O-1 sur la base** (copie `git archive aa0afdc`, `biblio/` recopié, garde réseau `oracles/cargo_env.sh`) : `cargo --locked xtask verify` sortie 0, VERDICT GLOBAL VERT ; S-G4 45 fichiers sur 45 ; S-G5 46 sur 46, INDEX + 125 artefacts locaux sur 125 déclarés ; S-G6 VERT. `F:/rust/rustup/downloads/` vide. Suite `s2-harness` : 206 tests, OK (skipped=2), les deux sauts nomment `SHOGEN_S2_CAMPAGNE_CONTROL` ; 0 entrée dans le TMP neuf, 0 `__pycache__`. CA-E1-1 tenu.
- **Variable `SHOGEN_S2_CAMPAGNE_CONTROL`** : jamais posée (`env`, compte 0, mesuré avant chaque suite).
- **Copie du G0** (mission) : le fichier accepté finit par un saut de ligne (66 797 octets, 362 sauts, 0 CR, 0 guillemet ASCII) ; sa copie verbatim sous `docs/adr-0028/` passe `cargo xtask gates` (S-G4 46 sur 46, S-G5 47 sur 47), mesuré avant tout texte. *Correction du 2026-09-30 (revue G2, C-G2-5, option (a))* : la copie est retirée du véhicule ; le G0 se cite hors dépôt, par chemin et sha256 (docs/17 l.4, annexe B.7) ; la copie et son §20 restent sous `F:/tmp/shogen-lots/E1/correction/avant/wt/docs/adr-0028/G0-lot-E1.md` (sha256 `f0191691f4bd1851c1c1bf9f6656739e23cd779c98dfacdc116819037d3e650d`).
- **Rebasage (revue G2, C-G2-1 ; 2026-09-30)** : `main` a avancé à `f5b8269` pendant la revue (amendement daté d'ADR-0028, commit de 06:48:19Z) ; `git apply --check` des diffs du G1 y sortait 1. Base du premier rebasage : `f5b8269`, relevée à 07:29:49Z. `main` a ensuite avancé à `cf696bd` (commit de 07:41:49Z, `JOURNAL.md` seul, deux lignes en fin, l.80 égale), relevé à 08:22:47Z : second `git merge --ff-only` à 08:23:46Z ; base du lot au gel : `cf696bd` (§15). `git diff --stat aa0afdc f5b8269` : huit fichiers, dont `docs/08` (en-tête déjà v4, deux entrées) et l'annexe B (bloc B.6 : décisions A-1 à A-12, procurements P-01 à P-14, SHOGEN-E1-D2-COMPLETUDE-1). Acte : `docs/08` et l'annexe B remis au contenu de `aa0afdc` par lecture `git show`, puis `git merge --ff-only f5b8269` sur la branche du worktree ; les sept entrées 08 reposées aux mêmes emplacements de table, sans le hunk d'en-tête ; les blocs du lot posés en B.7 et B.8, premier numéro libre ; la demande de procurement Shostack en P-15.

## 1. Coupe R-25

- **Estimation ascendante, écrite avant tout texte** (05:24Z ; reprise du G0 §11, corrigée de C-5) :

| fichier | E1-a | E1-b | base |
|---|---|---|---|
| `docs/17-modele-de-menace.md` (neuf) | 87 | 26 | G0 §11 |
| `docs/08-assumptions.md` | 6 | 2 | une ligne par entrée ; en-tête v4 |
| `docs/adr-0028/ANNEXE-B-items.md` | 27 | 8 | G0 §11 (19), plus la scission de SHOGEN-E1-METHODE-1 (1) et la demande de procurement formée (7), C-5 |
| `docs/AUDIT-ENTREE.md` | 0 | 3 | note datée |
| **total** | **120** | **39** | avec la marge x 1,3 du G1 de B0 : environ 156 et 51 |

- **Hors compte, mesurés et publiés** : la copie du G0 (mission ; 362 lignes verbatim, plus une section datée des corrections du cp-1, environ 20) et ce journal (cp-1 complet, CA-10). Q-G1-3.
- **Mesure** (lignes ajoutées ; `diff -ruN` entre instantanés, `wc -l` des fichiers neufs ; E1-b mesuré contre l'arbre E1-a figé) :

| sous-lot | docs/17 | docs/08 | annexe B | AUDIT-ENTREE | total (seuil 200) | hors compte |
|---|---|---|---|---|---|---|
| E1-a | 84 (neuf) | +6 −1 | +28 | 0 | **118** | copie du G0 : 374 (362 verbatim + 12, §20) |
| E1-b | +27 | +2 | +10 | +2 | **41** | ce journal (nombre au rapport G1) |

  Écart à l'estimation : E1-a 118 contre 120, E1-b 41 contre 39. Lot entier hors copie du G0 et hors journal : 159 lignes. Avec la copie du G0 : 533.
- **Correction de la revue G2 (C-G2-5, option (a) ; C-G2-1 ii et v)** : sous la règle de la mission, le texte de document G0 compte, et E1-a mesurait 492 lignes avec la copie du G0. La copie est retirée du véhicule (Q-G2-1, à ratifier). Estimation écrite avant tout édit (07:40:56Z, `correction/estimation-R25.txt`) : E1-a 116, E1-b 41. Mesure sur les instantanés rebasés (`git diff --no-index --numstat`, `wc -l` du fichier neuf) :

| sous-lot | docs/17 | docs/08 | annexe B | AUDIT-ENTREE | total (seuil 200, tout texte compté) |
|---|---|---|---|---|---|
| E1-a | 84 (neuf) | +5 | +27 | 0 | **116** |
| E1-b | +27 | +2 | +10 | +2 | **41** |

  Le hunk d'en-tête de docs/08 sort du lot (C-G2-1 ii) ; la demande de procurement passe de six lignes à cinq (C-G2-1 v). Lot entier hors journal : 157 lignes ; le journal reste hors compte (cp-1, CA-10).

## 2. Changements (worktree du lot ; G1 sur `aa0afdc`, correction sur `cf696bd`)

| fichier | E1-a | E1-b | sha256, 16 premiers chiffres : base, E1-a, E1-b |
|---|---|---|---|
| `docs/17-modele-de-menace.md` | neuf : en-tête, §1 à §6, S-01 à S-19 sauf S-08, T-01 à T-12 | §7 : S-08, S-20 à S-26, T-13 à T-18, note de complétude de D.2 | absent, `dfc56c66beceebd8`, `0010013cedfa8cbd` |
| `docs/08-assumptions.md` | A(root-store), A(freshness-above), A(designation-host-only), A(host-integrity), A(agent-conformance) ; en-tête v4 déjà à la base | A(harness-clock), A(prereg-blindness) | `c8ff538561acd524`, `7efe2ff105cf7fa8`, `c931cd711a217bf0` |
| `docs/adr-0028/ANNEXE-B-items.md` | bloc B.7 : treize items (SHOGEN-E1-METHODE-1 en deux sous-lignes), demande de procurement formée P-15 | bloc B.8 : EX-E1-1 à EX-E1-3, renvoi à SHOGEN-E1-D2-COMPLETUDE-1 (annexe B.6) | `d900804ffb2af648`, `102bc6f493c64773`, `6449e6a9e84713db` |
| `docs/AUDIT-ENTREE.md` | — | note datée en fin de fichier | `d508e04e1dc73eb2`, inchangé, `90bd113895f268f9` |
| `docs/adr-0028/G0-lot-E1.md` | retirée du véhicule par la correction (C-G2-5 a) ; au G1 : copie à l'octet du G0 accepté, plus §20 | — | absent aux trois états |
| `docs/G1-lot-E1-modele-de-menace.md` | — | neuf : ce journal | — |

- Sha des états du G1 (base `aa0afdc`) : rapport G1 et §2 de la version du G1 de ce journal (§15).
- **Intouchés** : tout le code, `s2-harness/` (suite identique à la base, §4), `xtask/`, les workflows, les annexes A, C, D et E, `biblio/INDEX.md`, et rien sous `F:/Monark` (CA-E1-16).

## 3. Corrections du cp-1 appliquées, et choix du G1

- **C-1** (T-06) : la cellule de contrôle cite la comparaison (`attestation-binding.ts` l.52-57, appartenance exacte), son appel par `gate.ts` (l.736-741) et la table (l.34-39) comme donnée ; le mot du fichier est employé (la couture déclare la cohérence, sans rien recalculer, l.4).
- **C-2** : chaque référence est écrite en chemin complet depuis la racine ; les neuf références courtes de la pré-carte ont été re-résolues au gel, ligne relue ; le contrôle (a) refuse une référence courte (mutant a5).
- **C-3** (T-11) : format de signature de `git log` désigné par ses mots ; aucun caractère pour-cent dans docs/17 (contrôle (f), mutant f2).
- **C-4** : consignes tenues (§14) ; les `error_origin` des deux incidents du G0 sont des actes de l'orchestrateur au JOURNAL.
- **C-5** : SHOGEN-E1-METHODE-1 en deux sous-lignes, (i) NIST SP 800-154 et (ii) Shostack ; demande de procurement formée sous la table du bloc du lot (B.6 au G1 ; B.7 et identifiant P-15 après la correction C-G2-1 ; identité, pages, tentatives, usage, coût du jour). Fiche Wiley et fiche CSRC lues [abs] le 2026-09-30 par `firecrawl_scrape` ; aucun téléchargement ; une copie PDF non autorisée, apparue dans une recherche, n'a pas été ouverte. Identifiant unique conservé : le cp-1 a compté treize items neufs (Q-G1-4).
- **C-6** : §0 ; texte proposé hors lot ; E1-b consommable après la pose.
- **C-7** : chemins, sha256 et nombres de lignes au §4 et au manifeste des oracles (Q-G1-7).
- **Choix du G1, déclarés** :
  - adversaires notés ADV-1 à ADV-7 (A-1 à A-7 au G0) : A-1 désigne aussi l'acte de l'orchestrateur du G0 §12, et la lettre A se confond avec les résidus A(...) ;
  - **T-04 étendu** d'un vecteur (iv) : `gate` accepte un `attested` porté par l'appelant, dont il déclare la cohérence sans recalcul (`gate.ts` l.732-741) et recopie les résidus (l.786-788). La pré-carte disait « aucune entrée appelant » sur le chemin servi, vrai pour `attest` seulement ; S-04 renvoie donc aussi à T-04 (Q-G1-5) ;
  - T-01 : le libellé démonstratif est cité à sa constante (`adapter-shogen.ts` l.41), la mention servie du témoin auto-notarisé est citée aux l.32-34 (description de l'outil) et l.67-73 (texte d'honnêteté du résultat MCP) d'`attest.ts`, et non plus au commentaire source des l.4-7 (revue G2, C-G2-3) ;
  - T-07 et A(root-store) : l'absence de consultation de révocation est marquée [inféré] (contrôle hors ligne), aucune pièce détenue ne l'énonçant ;
  - T-11 : la clé de signature est un fichier de l'hôte, relevé dans la configuration git du dépôt (chemin non recopié) ;
  - la couverture de l'oracle (e) est la base `aa0afdc` (plus `biblio/`), et non le gel du lot : aucun texte écrit par le lot ne peut valider sa propre citation (plus strict que le G0 §10.3 e ; le mode du G0 donne la même sortie, §4).

## 4. Oracles (G3) : chemins, sha256, lignes (C-7)

- **Correction de la revue G2** : `verif_refs.py` (C-G2-6) et `mutants_e1.py` (C-G2-3) sont corrigés en place ; les sha du tableau ci-dessous sont ceux des versions du G1, conservées sous `F:/tmp/shogen-lots/E1/correction/avant/` (`verif_refs-G1.py`, `mutants_e1-G1.py`). Versions corrigées : `verif_refs.py` sha256 `441bf47f85b2a219eb446b198b94e6af7193f90a9f5b791bd6ab8f5628025a94`, 546 lignes ; `mutants_e1.py` sha256 `aeb44781c4525cd17877e4c040b1452096d94c16feece87146ce31dd5a8d5f52`, 143 lignes. Gels, sorties et manifeste de la correction : §15.

Scripts (`F:/tmp/shogen-lots/E1/oracles/`, bibliothèque standard seule) :

| script | sha256 | lignes | rôle |
|---|---|---|---|
| `verif_refs.py` | `1af62186a75b30e1c32c41e028c06f235871026a828a5a2713be264b4f9fe8ba` | 515 | O-2, contrôles (a) à (h) du G0 §10.3, plus (i) entrées neuves de 08 et (j) items neufs de l'annexe B |
| `mutants_e1.py` | `17d184c58a959a7e2fd15bfa91e2a25ab3784e6b0b495a8bb1a4ab5066de3965` | 142 | O-3 |
| `run_o2.py` | `7fc266b252e7d2972fd4607a3c2ff4b1fa65fb201e42f5bf043104f5fad85f07` | 43 | rejeux O-2 |
| `geler.py` | `1af7ba71cecea029a7f56f142aafe7da618c75d2fd648539374610bb9a63268d` | 71 | instantanés et gels des sous-lots |
| `actes_c6.py` | `ab4152e465a9f2aa7139145f4e5fa8641629f724210cfff7b422e3cba760e0c6` | 56 | texte proposé des actes C-6 |
| `manifeste.py` | `62fec644700064b283cf07c453a65288c7059d0870e3ad0480fa3b62f85d66e3` | 32 | manifeste des pièces |
| `cargo_env.sh` | `8934586dfe54d5be28e7adeb1db5d7528895ce670a1d81beeb35713d96ca9fea` | 11 | garde réseau cargo (reprise du G0 et du G1 de B0) |

- **Gels** (`F:/tmp/shogen-lots/E1/work/`) : `gel-base` (`git archive aa0afdc`, `biblio/` recopié de `F:/Shogen/biblio`, 152 entrées) ; `gel-e1a` et `gel-e1b` (base + instantané) ; `gel-e1b-actes` (+ `actes-orchestrateur-C6.diff` appliqué par `patch -p1`, sortie 0). MONARK : `git archive 4b4ec66e…` des chemins cités.
- **O-1** : base, `o1-base-xtask.out` (`6f93f32558dd24b526692bdcc279f866ef65bc1b91acc1e8b643455853e9a06b`, 105 lignes), exit 0 ; E1-a, `o1-e1a-xtask.out` (`a678763556c9915fb30f90fe8a25278a562db170905aef6d59ed4650d02954ce`, 86 lignes), exit 0, VERDICT GLOBAL VERT, S-G4 47 sur 47, S-G5 48 sur 48, INDEX + 125 sur 125, S-G6 VERT. Suite `s2-harness` sur la base : `o1-base-unittest.out` (`f2be25a9348321cf4a027f159410944451735f970d4991178835de8fbf2a09b1`, 5 lignes) et `-v` (`35c608e3c095300befc6708aba6d4bf2eef2f19544d59816c7d64f889a211ffa`, 239 lignes). O-1 du gel final, journal compris, et suite sur ce gel : au rapport G1 (le journal fait partie de ce gel).
- **O-2** (`run_o2.log`, `185523b093fb35a734ba253684eb0213c54c18ea04240a709959a2e76cb7230f`, 10 lignes) :

| run | gel | exit | sortie, sha256 | lignes |
|---|---|---|---|---|
| `o2-e1a` | gel-e1a, couverture (e) = base | 0 | `297b453ea86cf021c3c609f4ec872a2826299568b2404b8e7453d3beec1dab60` | 28 |
| `o2-e1a-corpus-du-gel` | gel-e1a, couverture (e) = gel (mode du G0) | 0 | même sha | 28 |
| `o2-e1b-sans-actes-C6` | gel-e1b | **1** : (c) seul, SHOGEN-E1-D2-COMPLETUDE-1, docs/17 l.106 et l.111 | `c951f155bb7d5c79ca61df851ea1a032d03e0f22f140597d4f9bbb2debe029df` | 30 |
| `o2-e1b-avec-actes-C6` | gel-e1b-actes | 0 | `5f38f4489a652b6e5dbcbf8ab460736028f0825f5949b8a4592b8cc0a749a9a3` | 28 |
| `o2-e1b-avec-actes-C6-corpus-du-gel` | gel-e1b-actes, mode du G0 | 0 | même sha | 28 |

  Comptes du run E1-b avec actes : 78 références Shōgen et 19 MONARK résolues, 17 cellules de contrôle à référence (T-18 porte le jeton de contrôle absent et son motif), 25 identifiants au registre 08 et 39 résidus résolus, 35 items et 20 lots résolus, 12 PX trouvés au registre PAROXYSME (comptes seuls), 15 dates ISO, 26 lignes S et 18 lignes T ; (i) 7 entrées neuves de 08 à sept cellules non vides ; (j) 15 lignes d'items neufs à cinq cellules non vides.
- **O-3** : `o3-e1a.out` (`d04792eb24cf76ce60f13c7d22327f87e514b3d85f7ca83143c5df92dcb2d38c`, 34 lignes) : témoin 0, 32 mutants tués sur 32 ; `o3-e1b.out` (`327b8bb9a5b48d750e167f73b545f862531ee6dd98ea0263ee1f8a8f8e484300`, 36 lignes), sur gel-e1b-actes : témoin 0, 34 sur 34. Chaque mutant (`work/mut-e1a/`, `work/mut-e1b/`) et chaque sortie (`oracles/mutants-e1a/`, `oracles/mutants-e1b/`) : chemin, sha256 et lignes au manifeste `oracles/MANIFESTE-oracles.txt` (sha256 `a4b8c404faf0fdf07c330fde607653157cbbcd9c93cdf41e3ebff0b4fc4eb1df`, 158 lignes, 157 pièces). Les sorties de mutants sont produites sans `PYTHONIOENCODING` : la sortie de l'enfant, en cp1252, est décodée en UTF-8 avec remplacement, si bien que le jeton `[aucun contrôle]` y perd sa lettre accentuée ; leurs sha ne se reproduisent que dans ce même environnement, et le rejeu du cp-2 se fait sans la variable, ou compare les lignes de verdict (revue G2, C-G2-7 ; la correction garde cet environnement, §15).

## 5. Mutants (G0 §10.4) et trous d'oracle trouvés

- **Liste** (les deux sous-lots) : (a) plage au-delà de la fin, fichier inexistant, référence MONARK sans sha, cellule de contrôle sans référence ni motif, référence courte ; (b) résidu inventé ; (c) item inexistant, PX-Shogen-99, lot absent de l'annexe A, item mentionné mais non défini ; (d) date JJ/MM/AAAA, rejeu de mut1 du cp-1 bref, nom de mois ; (e) rejeu de mut5 du cp-1 bref (citation anglaise fabriquée en guillemets droits), fragment français introuvable, guillemet orphelin ; (f) chemin de D.2, pour-cent, valeur statistique, IPv4 et IPv6 de documentation, adresse électronique, graine et clé du constat insérées depuis le gel sans affichage, docs 16 ; (g) deux formes proscrites ; (h) ligne T retirée, S sans menace ni motif, cellule de résidu vide, jeton de chemin servi absent, marqueur entre guillemets au lieu du jeton. E1-b ajoute : T-17 retirée ; SHOGEN-E1-D2-COMPLETUDE-1 renommé.
- **Trou n° 1, tué par la campagne** : à la campagne n° 1 (05:56Z, `o3-e1a-campagne1.out`, sha256 `875078f477889988ef2e3814803c85b0eb0e1986de45ce0b983705ea78d4cf68`, 33 lignes), le mutant IPv4 a survécu : l'adresse suivie d'un point final échappait à l'expression. Corrigée, puis tuée. La version du script qui a produit cette sortie n'est pas conservée (corrigée en place) ; E-4.
- **Trou n° 2, trouvé par le rejeu différentiel avec et sans actes** : la première version de (c) acceptait un item dès qu'il était **mentionné** dans l'annexe B. Le renvoi du bloc B.7 du lot suffisait donc à valider SHOGEN-E1-D2-COMPLETUDE-1 sans l'acte de l'orchestrateur. (c) exige désormais une **définition** (première cellule d'une ligne de table, ou puce en gras de B.3) ; mutant c5 ajouté. E-4.
- **Trou n° 3, trouvé par la revue G2** (22 mutants hors de la liste du G0, `g2-work/mutants_g2.py` ; 11 survivants) : (a) acceptait sans la résoudre une référence sans extension, à chemin absolu, ou sortant du gel par un segment `..` ; (d) ignorait les dates numériques JJ.MM.AAAA, AAAA/MM/JJ et AAAA-M-J. Fermé par la correction C-G2-6 : (a) refuse le chemin absolu ou non canonique et toute sortie du gel, et résout dans le gel un chemin sans extension ; (d) refuse ces trois formes et deux voisines (AAAA.MM.JJ, JJ-MM-AAAA). La première version de la correction de (d) laissait survivre G08 et G09 : la date suivie d'un point final échappait à l'expression, comme au trou n° 1 ; corrigée avant le gel, sa version et sa sortie sont conservées (§15, E-7). Rejeu des 22 mutants : 17 tués, dont G01 à G03 et G08 à G10 ; les cinq survivants hors de la lettre du G0 (résidu en majuscules, citation entre apostrophes, décimal, pour-cent en toutes lettres, nom nu de D.2 n° 8) et la borne de (c) sur les lots MONARK sont nommés comme cas de test de SHOGEN-E1-XTASK-REFS-1 (annexe B.7).
- **Couverture non mécanisée** (FM-3.3) : `verif_refs.py` établit l'existence et la forme, jamais la fidélité ; la table de fidélité est la lecture du G2 (G0 §10.5).

## 6. Fidélité : ce que le G1 a relu

- Chaque ligne citée a été relue au gel avant d'écrire sa cellule (lectures de ce journal, §14). Trois cellules ont été reprises à la relecture finale : T-01 (libellé), T-07 (révocation, [inféré]), T-11 (clé de signature).
- Sidecars de `biblio/` (DECO l.109, l.110, l.1424 ; Knight et Leveson l.465) : non versionnés, présents dans le gel par copie de `biblio/` ; leur ligne se lit par `pdftotext` régénéré (`just sidecars`). Aucune citation entre guillemets n'en est faite ; les idées sont reformulées.

## 7. Tuyaux (CA-11)

- **Entrée** : surface servie MONARK à `4b4ec66e…` ; code Shōgen à `aa0afdc` au G1, à `cf696bd` après la correction (références re-résolues, lignes citées inchangées, §15) ; ADR-0015, 0016, 0028 ; docs 03, 04, 08, 13 ; cartographie (plages) ; dimensions `monark`, `rust` et `git-ci` (C-G2-4).
- **Sortie** : docs/17 (T-01 à T-18, S-01 à S-26) ; sept entrées 08 ; items et exigences des blocs B.7 et B.8 (B.6 et B.7 au G1) ; note d'AUDIT-ENTREE.
- **Consommateurs** : G0 des lots correctifs Shōgen et MONARK (transmission), cp-2 de clôture S2, registre PAROXYSME. **Tuyau partiel déclaré** vers les G0 aval (consommateurs futurs) ; composition docs/17 vers annexe B testée par (c).
- **État** : fichiers versionnés ; sha256 au JOURNAL au commit de chaque sous-lot (acte de l'orchestrateur).

## 8. Risques MAST nommés et contre-mesures

- **FM-1.1** : aucune pièce de D.2 ouverte ; aucune recherche récursive sur `F:/tmp/` ; cartographie lue par plages après repérage de sa l.51 par `shaline.py` ; ADR-0025 non ouverte (sa l.14 repérée de même) ; `PAROXYSME-Shogen.md` jamais affiché (sha256 recalculé, identifiants comptés par le script).
- **FM-2.4** : chaque résidu porte un item ou un lot à déclencheur (contrôles (c) et (h)).
- **FM-3.2, FM-3.3** : O-2 et O-3 ; deux trous de l'oracle trouvés et fermés (§5) ; fidélité laissée au G2.
- **FM-1.5** : ensembles fermés exacts (h) ; arrêt R-25 non déclenché.
- **FM-2.3** : aucun code, aucune décision de RENDU-1 ni du PAQUET (exigences seulement).

## 9. `error_origin` proposés (à assigner au G7)

- **E-1** : base nommée `fb089dc` par la commande de mission, alors que le G0 exige la HEAD du lancement ; worktree créé à `fa0ce5b`. Origine : commande de mission (modèle de base périmé) et harnais du workflow.
- **E-2** : préalables C-6 non posés au lancement. Origine : orchestrateur (séquence de lancement).
- **E-3** : pré-carte du G0 : « aucune entrée appelant » sur le chemin servi (vrai pour `attest`, faux pour `gate`) ; libellé cité à l'en-tête d'`attest.ts` ; révocation affirmée sans pièce. Origine : planificateur G0.
- **E-4** : deux trous de `verif_refs.py` (§5), fermés avant le gel final ; sortie de la campagne n° 1 conservée sans la version du script qui l'a produite. Origine : G1.
- **E-5** : égalité du registre de la fixture et de docs/08 (constat R-07) rompue par les sept entrées neuves, par construction : conséquence déclarée, pas une erreur (SHOGEN-E1-COPIES-GARDEES-1 porte l'invariant d'inclusion).
- **E-6** : base du G1 dépassée pendant la revue G2 (amendement `f5b8269`, commit de 06:48:19Z, la revue ayant commencé à 06:41:07Z) : diffs inapplicables, rebasage (C-G2-1). Origine : séquence des lots en parallèle ; aucune faute de rédaction.
- **E-7** : première version de la correction de (d) (`verif_refs.py` sha256 `a1bd76aefbfb332a38c05333cb208f6b8b07e5901c983dc5f4d18c7319f7ef28`) : G08 et G09 survivaient (point final après la date). Trouvé par le rejeu des mutants du G2 avant le gel, corrigé ; version et sortie conservées. Origine : G1 de correction.
- **E-8** : copie du G0 hors du véhicule du G0 §12 (Q-G1-8), retirée par C-G2-5 (a). Origine : commande de mission du G1.

## 10. Review Focus

1. T-04 (iv) et S-04 : le `attested` porté par l'appelant de `gate` est une entrée du chemin servi que rien ne recalcule, et ses résidus sont servis.
2. Registre publié : 18 identifiants à la base, 25 après le lot ; la copie `registre.txt` de la fixture en reste à 18 (inclusion, pas égalité).
3. Références à relire au gel du commit : `JOURNAL.md:80` (stable si le JOURNAL ne fait que croître) ; `s2-harness/tests/test_exclusion.py` l.242-244 et l.269-271, que la vague 2 peut déplacer ; le G2 rejoue `verif_refs.py` sur la HEAD du moment.
4. Numérotation des blocs du lot : B.7 et B.8 au gel, premier numéro libre à `cf696bd` (annexe B inchangée depuis `f5b8269`) ; tout bloc posé à l'annexe B avant le commit du lot les décale (`git apply --check`, CA-E1-14 ; revue G2, C-G2-1).
5. Sidecars de `biblio/` cités par ligne : le gel doit recopier `biblio/`.

## 11. Questions ouvertes Q-G1-n (pour l'orchestrateur)

- **Q-G1-1** : ratifier la base `aa0afdc` (§0) ; après la correction, la base est `f5b8269` (C-G2-1, Q-G2-2).
- **Q-G1-2** (amendée par la correction C-G2-1) : poser A-1 (annexe A : ligne E1, puis lignes E1-a et E1-b du G0 §12). L'item SHOGEN-E1-D2-COMPLETUDE-1 est inscrit à `f5b8269` (annexe B.6) : la proposition d'item d'`actes-orchestrateur-C6.diff` est caduque. Le diff de A-1 ne s'applique plus depuis `f5b8269` (revue G2, §9) : texte à re-dériver à la HEAD, avec les tailles mesurées (116 et 41, §1) et des véhicules sans la copie du G0 (E1-a) ni ce journal (E1-b).
- **Q-G1-3** : compter la copie du G0 (374 lignes) hors R-25, comme le journal (cp-1, CA-10) : copie à l'octet d'une pièce déjà revue, contrôlée par son sha. Sans objet après la correction C-G2-5 (a), qui retire la copie (Q-G2-1).
- **Q-G1-4** : SHOGEN-E1-METHODE-1 garde un identifiant et deux sous-lignes (le compte fermé de treize items tient).
- **Q-G1-5** : ratifier l'extension de T-04 et la notation ADV-n (§3).
- **Q-G1-6** : MONARK cité à `4b4ec66e…` plutôt qu'à `b27e5e9` (§0).
- **Q-G1-7** : forme de C-7 : les sha256 des scripts et des sorties au §4, ceux de chaque mutant et de chaque sortie de mutant au manifeste, dont le sha est ici. Rétention de `F:/tmp/shogen-lots/E1/oracles/`, de `F:/tmp/shogen-lots/E1/work/` et de `F:/tmp/shogen-lots/E1/correction/` (gels, mutants) jusqu'au cp-2 de clôture S2 : acte de l'orchestrateur au JOURNAL.
- **Q-G1-8** : la copie du G0 est hors du véhicule du G0 §12 (CA-E1-16) ; elle vient de la commande de mission. Retirée par la correction C-G2-5 (a).
- **Q-G1-9** : report de la demande de procurement à `WISHLIST.md`, registre des demandes du dépôt : acte hors lot.

## 12. Livrables (`F:/tmp/shogen-lots/E1/`)

- Après la correction de la revue G2 : `lot.diff` régénéré contre `cf696bd` (`git add -N .` puis `git diff HEAD`), `e1-a.diff` et `e1-b.diff` régénérés (`diff -ruN` entre instantanés rebasés), `correction-rapport.md` ; versions du G1 sous `correction/avant/` (`lot-G1.diff`, `e1-a-G1.diff`, `e1-b-G1.diff`).
- `lot.diff` (lot entier contre `aa0afdc`, `git add -N .` puis `git diff HEAD`), `e1-a.diff`, `e1-b.diff` (sur E1-a), `actes-orchestrateur-C6.diff` (hors lot) : sha et rejeu `patch -p1` au rapport G1.
- `G1-rapport.md` : ce journal, précédé des empreintes des livrables et des O-1 finals.
- `oracles/` : scripts, sorties, manifeste ; enregistrement d'oracle `shogen.oracle-record.v1` (rôle G1) sous `F:/tmp/oracle-results/`.

## 13. Incidents

- Aucun accès réseau par cargo ou rustup (`F:/rust/rustup/downloads/` vide après chaque run). Deux lectures réseau déclarées, par `firecrawl_scrape`, en lecture seule : fiche éditeur Wiley et fiche CSRC de NIST SP 800-154 (C-5). Aucun formulaire, aucun téléchargement.
- Le garde du harnais a refusé plusieurs formes de commandes (heredoc long, `source`, variables de chemin) : commandes scindées ou fichiers écrits par l'outil d'écriture ; aucun contournement du garde.

## 14. Attestation d'exposition (forme d'ADR-0028 D.3)

- **Pièces lues** : le G0 du lot (entier) ; le cp-1 complet (l.1-80) et la liste des mutants du cp-1 bref ; ADR-0028 (D6, D7, D9, D10, §3, §4.12), annexes A et B (entières), C (entière), D (D.2, D.3, D.4) ; docs 03 (l.1-112), 04 (l.120-204), 08 et 09 (entiers), 13 (l.97) ; DECISIONS (ADR-0015 pts 14, 16, 17 bis) ; AUDIT-ENTREE ; `docs/G1-lot-B0-pool-analyse.md` (l.1-240, tronquées) ; cartographie l.1-50 et l.52-112 ; `monark.md` l.1-133 et l.184-230 ; `rust.md` l.223-245 et l.301-323 ; code Shōgen et MONARK aux lignes citées ; JOURNAL l.80 (120 premiers caractères et comptes de jetons) ; INDEX (l.1-20, 81-86, 220, 231, 323-328) ; sidecars DECO (l.108-111, 1423-1425) et Knight et Leveson (l.464-466) ; `CLAUDE.md` ; `WISHLIST.md` (l.1-75).
- **Exposé à** : les comptes que porte la cartographie (fenêtres, couverture calendaire, doublons, n après l'exclusion, comptes de Pyth, coupes du J14, heures par strate et de référence) ; aucun n'est reproduit dans le lot.
- **Non ouverts** : les pièces de D.2 n° 1 à 9, toutes ; ADR-0025 ; `PAROXYSME-Shogen.md` ; docs 15 et 16 ; le rapport de divulgation ; les journaux de campagne et `F:/shogen-campagne/`.
- **Balayages mécaniques** (octets lus par un outil, rien d'interdit affiché) : `shaline.py` sur la cartographie et sur ADR-0025 (numéros de ligne seulement) ; `cargo xtask verify` et `gates` (S-G4, S-G5 lisent tout `docs/`) ; la couverture (e) de `verif_refs.py` lit tous les fichiers texte de la base, docs 15 et 16 compris, en mémoire, sans affichage ; le contrôle (c) compte les identifiants PX du registre PAROXYSME sans l'afficher ; la graine et la clé du constat sont lues par le script, jamais affichées.
- **Aucune statistique S2 calculée. Aucun z, aucun K, aucun P̂_more, aucun φ vu.**
- **Git et disque** : aucun `GIT_DIR`, aucun `GIT_WORK_TREE`, aucun `--write-tree`. Git écrivant : `merge --ff-only` et `add -N` dans ce worktree seulement. Rien écrit sur C: ; l'interpréteur Python de C: est lu, et c'est déclaré. `TMP`, `TEMP` et `TMPDIR` sous `F:/tmp/shogen-tests-tmp/e1-g1`, `CARGO_HOME` et `CARGO_TARGET_DIR` sur F:.

## 15. Corrections de la revue G2 (2026-09-30, ajout daté ; lignes précédentes amendées aux seuls endroits nommés ci-dessous)

- **Générateur** : `claude-opus-5-5` (R-1 déclaré en tête de session), effort max, contexte frais, G1 de correction, distinct du réviseur. Aucun commit, aucun workflow (R-20) ; aucun `GIT_DIR` ni `GIT_WORK_TREE`, aucun `--write-tree`. Horloge (`date -u`) : début 07:29:49Z ; sauvegardes 07:40:47Z ; estimation R-25 07:40:56Z, avant tout édit ; rebasage 07:41:15Z ; O-2 07:57:48Z-07:58:08Z ; O-3 07:58:14Z-08:04:17Z ; mutants du G2 rejoués 08:04:24Z-08:08:27Z ; O-1 de la base et d'E1-a 08:11:21Z-08:15:05Z, à `f5b8269` ; `main` relevé à `cf696bd` à 08:22:47Z, second rebasage 08:23:46Z, puis O-2, O-3, mutants et O-1 rejoués à `cf696bd` de 08:24:56Z à 08:39:36Z ; texte de docs/17 retouché à 08:56:42Z (l.8, virgule ; T-16, ancre (1) rattachée à l'annexe D.4 c), puis O-2, O-3, mutants et O-1 d'E1-a rejoués de 08:56:55Z à 09:08:44Z ; ce journal 09:1xZ.
- **Mandat** : commande de mission de l'orchestrateur Shōgen (`claude-fable-5-1`) ; liste fermée C-G2-1 à C-G2-7 de la revue G2 (`F:/tmp/shogen-lots/E1/G2-rapport.md`, sha256 `6d9cde594c64268fffafbe5a773d05363fc14172f1fea95dee8f99c20ebec96b`, ACCEPTE-AVEC-CORRECTIONS ; C-G2-1 bloquante avant le G7).
- **Amendements sur place** : en-tête (modèle, résultat), §0, §1, §2, §3 (C-5, T-01), §4, §5, §7, §9 (E-6 à E-8), §10 pt 4, §11 (Q-G1-1, -2, -3, -7, -8), §12. La version du G1 de ce journal est conservée : `F:/tmp/shogen-lots/E1/correction/avant/wt/docs/G1-lot-E1-modele-de-menace.md`, sha256 `1b52ad88f0d35702c9cb52e386ed9f27c3911d04347938c74460d48e8c87004a`.
- **C-G2-1** (rebasage, §0) : base `f5b8269`, puis `cf696bd` (`JOURNAL.md` seul entre les deux). docs/08 : sept entrées aux mêmes ancres, `git diff --numstat` 7 0, chaque ligne égale à l'octet à celle du G1 (`correction/scripts/reinserer_08.py`). Annexe B : blocs B.7 et B.8, demande de procurement P-15, aucune insertion de SHOGEN-E1-D2-COMPLETUDE-1 (`correction/scripts/construire_annexe_b.py`). docs/17 l.4 : base rebasée. Comptes : un titre `## B.7`, un titre `## B.8`, une ligne `| SHOGEN-E1-D2-COMPLETUDE-1 |`, une ligne `| P-15 |`. `git apply --check` des diffs régénérés sur `git archive` de la HEAD : au rapport de correction.
- **C-G2-2** : docs/17 l.88, gardes (1) à (6) ; T-16, gardes (5) et (6) de l'annexe D.4 b et ancre retenue en D.4 c, relues à `f5b8269` (annexe D l.116-149), sans décision ; annexe B.8, renvoi à l'annexe B.6.
- **C-G2-3** : T-01 cite `attest.ts` l.32-34 et l.67-73 à `4b4ec66e…`, lues : les deux plages portent la mention du témoin auto-notarisé et du vérificateur non exécuté à l'appel ; la cible du mutant a3 suit, a3 tué dans les deux campagnes.
- **C-G2-4** : docs/17 l.8 déclare la dimension `git-ci` et son sha256, recalculé égal ; GC-01 en l.221, lue par chemin explicite sous un garde de sha de ligne.
- **C-G2-5** : option (a), la seule applicable sans règle écrite de l'orchestrateur ; copie du G0 retirée du véhicule (`git rm --cached`, puis suppression du fichier, conservé au §0) ; E1-a mesure 116 lignes, tout texte compté (§1). Q-G2-1 reste à ratifier ; l'option (b) reste possible à partir de la copie conservée.
- **C-G2-6** : `verif_refs.py`, contrôles (a) et (d) (§5, trou n° 3) ; SHOGEN-E1-XTASK-REFS-1 nomme les cas de test hors de la lettre du G0 (annexe B.7).
- **C-G2-7** : §4, ligne O-3 ; les campagnes de la correction tournent aussi sans `PYTHONIOENCODING` (compte 0 dans l'environnement).
- **Oracles de la correction** (scripts sous `F:/tmp/shogen-lots/E1/correction/scripts/`, sorties sous `correction/sorties/`, gels sous `correction/work/` ; `gel-base` = `git archive cf696bd` et `biblio/` recopié, INDEX égal au blob du commit, 152 entrées, présent avant et après chaque run) :
  - O-1 : base `cf696bd` seule, VERT, S-G4 45 sur 45, S-G5 46 sur 46, INDEX + 125 sur 125 (`o1-base-cf696bd.out`, sha256 `68b2bf11a11915c697c77816b821343ff4a83d90e81e0f3fe65d8d86efb51d4b` ; même verdict à `f5b8269`, `f5b8269/o1-base-f5b8269.out`, `bb70d6b1cdb5830c745d51493f9af9d66cc7c3e1c8879e52db2c1bb86680155b`) : CA-E1-1 tenu à la nouvelle base ; E1-a, VERT, S-G4 46 sur 46, S-G5 47 sur 47 (`o1-e1a.out`, `5b07d4a5f3b41f31903434094276ab6765fed1528526d95de191d507d4ce3c03`) ; gel final, ce journal compris, et suite `s2-harness` : au rapport de correction.
  - O-2 (`run_o2_c.py`, `--items-neufs` = les treize items du lot, aucun acte à poser) : E1-a sortie 0 (`o2-e1a.out`, `f2ceafd4b5bd8ff011a5a397c1c389b4d009fb54988f7dd1ae97a06ad8d85cdd`) ; E1-b sortie 0 (`o2-e1b.out`, `40cb49ce1a07c78f85cd1a150efed0a13bdb026f59cb935b0f55520fc0d43efb`) ; mode de couverture du G0 et rejeu à `f5b8269` : mêmes sorties. Comptes d'E1-b : 78 références Shōgen et 20 MONARK, 17 cellules de contrôle à référence, 27 identifiants au registre et 39 résidus résolus, 35 items, 20 lots, 12 PX, 16 dates ISO, 26 lignes S et 18 lignes T, 7 entrées 08, 14 lignes d'items neufs.
  - O-3 (`mutants_e1.py`) : E1-a, témoin 0, 32 tués sur 32 (`o3-e1a.out`, `f9032a022c4ee44824dd4d64b66d30c95fd4302c8c8383aa75e04d94b4665a62`) ; E1-b, témoin 0, 34 sur 34 (`o3-e1b.out`, `9c16dbb8c71b35e642459b9bf5a9f3d4dc576fc2c208a72066176e0e63964a84`) ; mêmes verdicts qu'à `f5b8269`, les empreintes des mutants changeant avec la l.4 de docs/17, qui porte la base.
  - Mutants du G2, copie re-pathée (`mutants_g2_rejeu.py` ; sur le gel du G2, les 22 empreintes de mutants sont celles du G2) : sur le gel du G2 (`g2-actes`, lu seulement) et sur le gel final, témoin 0, 17 tués, 5 survivants nommés (`g2-mutants-rejeu-g2actes.out`, `99d4ba348249ae10ae6eb80768d1cf9b7967387e7b7e71cb647dcde40066d1fa` ; `g2-mutants-rejeu-gel-e1b.out`, `ee3ed1ff39a26bfe67ce20ad669de6c5c71734fb56ef0039fc98390735b75a47`). Première version (E-7) : `g2-mutants-rejeu-g2actes-v1.out` (`3ad91e012697fce0847cab8629ac4db8d301bc2c9ef32943b1be5006c1ed3c66`). Mutants de gel du G2, re-pathés : 4 tués sur 4, témoin 0 (`mutants-gel-rejeu.out`, `593dcefa91d1378390c3ac710a967dee3332b3cd7e73b8a054d5d3fc32cc8414`). Mutants et témoins ajoutés (`mutants_c1.py`) : quatre témoins en sortie 0 (référence sans extension résolue, numéro de version, numéros de section, document intact) et douze formes voisines tuées (`mutants-c1.out`, `f0d629710c8b262fc58ca5535f815d927e65f7e28224156a6e4e7a70a842a3bf`).
  - Références re-résolues au gel final : 74 uniques résolues, 0 introuvable, aucune ligne interdite affichée (`refs-show-gel-e1b.out`) ; entre `aa0afdc` et `cf696bd`, seul `JOURNAL.md` change parmi les fichiers cités (cinq lignes en fin, l.80 égale), `s2-harness/` compris.
  - Manifeste, rejeu des diffs et enregistrement d'oracle : au rapport de correction (`F:/tmp/shogen-lots/E1/correction-rapport.md`).
- **Attestation** (forme D.3) :
  - lu : la revue G2 (entière), le rapport G1, le G0 (§8.1, §11 à §14 et titres), l'annexe B à `f5b8269` (titres, l.83-128), le diff de docs/08 entre `aa0afdc` et `f5b8269`, l'annexe D à `f5b8269` (l.116-149), `attest.ts` à `4b4ec66e…` (l.1-74), `git-ci.md` l.221 ;
  - exposé à : des constantes de conception de l'amendement (portée de dépendance en fenêtres, borne de la famille R1, borne de dispersion par classe, dans les deux entrées 08 et le bloc B.6) et à une formule de condition de puissance avec son seuil de conception (annexe B.6) ; aucune valeur mesurée ;
  - non ouverts : les pièces de D.2 n° 1 à 9 ; `PAROXYSME-Shogen.md`, lu par le script, jamais affiché ; ADR-0025 ; docs 15 et 16 ;
  - `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée ; aucune statistique S2 calculée ; aucun z, K, P̂_more ni φ vu ;
  - git : lectures seules (`show`, `archive`, `diff`, `rev-parse`, `log`, `hash-object` sans écriture) ; écritures dans ce worktree seulement : `git merge --ff-only f5b8269` puis `cf696bd`, `git rm --cached docs/adr-0028/G0-lot-E1.md`, `git add -N .` ; rien écrit sur C: (`TMP` sous `F:/tmp/shogen-tests-tmp/e1-c1`) ; l'interpréteur Python de C: est lu.
