# Contre-contrôle de DETTES-T3 (CONFORME en passe 2) (transcrit)

> Transcription par l'orchestrateur le 2026-10-09 18:07:35 UTC du fichier g2/cc/RAPPORT-CC.md ; contrôle FM-1.1 des transcripts du générateur-correcteur, du réviseur et du contre-contrôleur, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Contre-contrôle neuf du lot DETTES-T3 (série DT3-A, E, B, C, D, F sur 0cfbe3e)

- **Modèle** : `claude-opus-5-5`
- Gate 0 : modèle résolu `claude-opus-5-5` (identifiant exact donné par l'environnement), effort `max` demandé par le
  brief, non observable de l'intérieur. Heures lues par `date -u` : début 2026-10-09 16:34:23Z, rédaction 16:54:30Z.
- Contre-contrôleur neuf : je n'ai écrit ni les diffs ni la G2. Base : `/home/user/shogen` HEAD
  `0cfbe3ecaeac81cbb35f606b3c53ef3df856dff5`, égale à la tête du brief. Le dépôt réel n'a pas été modifié :
  `git status --porcelain` vide et HEAD inchangé à la fin.
- Pièces relues (sha256, 16 premiers caractères) : `ADJUDICATION-G1.md` `c4dccfe128dcab97` (sections de 15:51:56,
  16:06:10 et 16:22:00), `g2/RAPPORT-G2.md` `3cab489708cd1dc1`, `RAPPORT-GENERATEUR.md` `886c4a0b38bc278a` (dernière
  section 16:32:47). Diffs : A `b018c1f1`, E `3abe7e22`, B `6dfaff03`, C `eaa3c376`, D `49c469c1`, F `44adf11f`.
  Empreinte de la série (sha256 de la concaténation A, E, B, C, D, F) : `37e75eab7152f1a7a2d79cd802a683987c2e3a1a9d32b8bf6cf07014b16f8bce`.

## Verdict : CONFORME-AVEC-RÉSERVES (R-1 à R-4, liste fermée)

Les corrections C-1 à C-9 sont faites et répondent à la G2 et à l'adjudication. Seules restent deux précisions de
texte, des trous de test et deux heures. N-1 à N-6 sont tués par AssertionError. Toutes les gates donnent les comptes
attendus, et la série ne change aucun VERDICT de xtask. Six mutants neufs ont été essayés. Quatre survivent à la suite
du lot, et un cinquième n'est tué que par l'épingle sha256 (R-2). Toutes les réserves se corrigent dans le lot. Leur
forme est écrite et mesurée dans `corrections-CC.diff` (donnée, non diff à livrer ; sha256 `39e04edf42795f72…` ;
`git apply --check -p2` vert sur la série). Sur la copie corrigée : suite `scripts/controle` à Ran = 18, plancher
inchangé ; 12 mutants sur 12 tués, témoin vert. Aucun item n'est à former.

### Réserves

- **R-1 (DT3-F, docstring de `enforcement/journaux-modele.py`, C-5)**. Le texte dit : « le commit qui le modifie lui
  ajoute la ligne ». C'est faux pour les 16 journaux exemptés qui portent déjà la ligne en forme (recompte sans
  exemption : 16 conformes, 34 sans ligne, 2 hors forme). Mesure (`sorties/c5-procedure.txt`) : on suit la procédure
  sur `G1-lot-D8a.md` (une ligne de plus) → refus « 2 ligne(s) … une exigée ». La même retouche sans ligne ajoutée →
  conforme. Sur `G1-lot-CORR.md`, la ligne ajoutée → conforme. En plus, « par un lot (DT3-F) » se lit comme si DT3-F
  était le lot qui change ces sha256. Forme : « lui ajoute la ligne s'il n'en porte aucune (… ; 16 la portent déjà
  dans la forme : une seconde les ferait refuser) … par un lot (texte de DT3-F) ». Coût : +3 −2, dans F.
- **R-2 (tests, DT3-E et DT3-F)**. Les mutants neufs mesurés sur la suite du lot (`sorties/mutants-lot.json`) :
  CC-1 (fenêtres de `fm11.py` plafonnées au rang 40) n'est tué que par l'épingle et les sommes, jamais par `Temoin`.
  Aucun test ne voit les fenêtres 60 et suivantes d'une ligne de plus de 100 caractères. CC-2 (exemption accordée
  quand le nom est exempté et que le sha256 en est un autre de la liste), CC-3 (liste blanche réduite à opus), CC-4
  (`except` énuméré avec AttributeError : erreur de syntaxe ou import manquant de l'outil → sortie 1) et CC-5 (deux
  racines admises) sont **vivants**. C-4 nommait les trois chemins d'erreur, et le test n'en couvre qu'un, l'outil
  vide. Forme :
  - dans E : ajouter la longueur 121 à `test_queue_aux_longueurs_limites`, avec les extraits `(60,100,1)`,
    `(80,120,1)`, `(61,101,0)` et `(81,121,1)`, écrits à la main (fenêtres 0 à 80, queue [81,121)) ;
  - dans F (B est à +193) :
    - `test_nouveaux_conformes` reçoit `claude-sonnet-5-5`, `claude-fable-5-1` et `claude-haiku-5-5` ;
    - `test_exempte_puis_modifie` vérifie que les octets de `G1-lot-CORR.md` sous le nom `G1-lot-D8a.md` sont refusés ;
    - `test_racine_illisible` vérifie la sortie 3 pour l'outil vide, en erreur de syntaxe et à import manquant
      (sous-cas), et pour deux racines.

  Aucune méthode neuve : le plancher reste 18. Taille mesurée : E +55 −17, F +25 −4, toutes deux sous 200. Avec ces tests,
  CC-1 à CC-5 sont tués par AssertionError (`sorties/mutants-corr.json`). CC-1 l'est alors par
  `test_queue_aux_longueurs_limites`, et non plus par la seule épingle.
- **R-3 (DT3-C, consigne de `.claude/agents/shogen-worker.md`, C-7)**. La consigne est juste, sûre et applicable
  (voir point 1). Elle ne dit pas ce que l'enregistrement atteste quand les diffs ne sont pas commis. Mesure sur un
  dépôt jetable, avec la série non commise (`sorties/c7-*.txt`) :
  - la commande de la consigne sort en 0, et `--verifier` la juge conforme ;
  - son `tree` est la base seule : `fm11.py` à `886cc676…`, `journaux-modele.py` absent, suite lancée sur la base ;
  - une fois la série commise, `--verifier --commit <ce commit>` refuse (`tree.commit`).

  Un lecteur peut donc prendre l'enregistrement pour une preuve sur le code relu. Forme : une phrase après la
  dernière, « L'enregistrement atteste alors la base et la suite lancée sur elle, non les diffs : il se vérifie à
  `<commit relu>`, et seul le rapport G2 le relie aux diffs. », plus une assertion dans
  `test_consigne_au_bloc_de_gabarit` (constante `BASE`). Taille mesurée : C +74 −1.
- **R-4 (heures des ajouts datés, DT3-C et DT3-D)**. L'ajout de la fiche garde « 15:58:07 UTC » et celui de DT3-D
  « 15:58:38 UTC ». Pourtant leur texte a changé après la G2 : la phrase de C-7, et la citation de C-6 (avant : « B.55
  et B.61 », lu dans `travail/avant-g2/`). Les deux ajouts du README, eux, ont été re-datés à 16:23:29 (C-8). Forme :
  chaque ajout daté du lot porte l'heure `date -u` de sa dernière écriture, ou l'heure posée par l'orchestrateur au
  versement, comme Q-D1 l'annonçait. La règle est la même pour les trois fichiers. R-3 retouche la fiche : son heure
  suivra.

## 1. Corrections C-1 à C-9

| correction | constat | état |
|---|---|---|
| C-1 (E) | `test_queue_aux_longueurs_limites`, longueurs 39 à 61 | Fait. J'ai recalculé les 16 extraits à la main : tous justes. La sonde `outils/sonde_fm11.py` essaie **tous** les extraits [a, b) d'une ligne de n caractères distincts, pour n = 0, 1, 20, 39, 40, 41, 59, 60, 61, 79, 80, 81, 99, 100, 101, 120, 121, 141 et 200. Elle les compare à une référence écrite depuis la règle du README : fenêtres [20k, 20k+40) contenues dans la ligne, plus la queue. Résultat : 0 écart sur 77 787 extraits (`sorties/sonde-fm11.txt`). Plancher 9 dès E. Réserve R-2 (au-delà de 100). |
| C-2 (B) | trois formes refusées, mêmes octets sous un nom neuf | Fait. N-4 et N-5 sont tués. |
| C-3 (C) | `test_commande_passe_l_analyseur` | Fait. Le test passe par l'analyseur réel : pas de `usage:`, sortie 2, préfixe `oracle_record : `. N-6 et CC-6 sont tués. |
| C-4 (F) | `except Exception`, sortie 3 | Le code est fait. Le test ne couvre qu'un des trois chemins nommés : R-2. |
| C-5 (F) | procédure de retouche d'un journal exempté | Faite. Elle est fausse pour les 16 journaux déjà conformes : R-1. Le cas DETTES-B2 est dit, et mesuré (refus à 2 lignes). |
| C-6 (D) | « B.60 ; volets B.61 et B.85 » | Fait. B.60 : en-tête l.992, item l.1014. B.61 : l.1018. B.85 : en-tête l.1352, volet l.1367. Voir O-3. |
| C-7 (C) | décision de l'adjudication | Voir ci-dessous. Faite. R-3. |
| C-8 (E) | heures du README | Faites (16:23:29 UTC, deux ajouts). R-4 pour la fiche et D. |
| C-9 (E) | garantie de détection au README | Faite. La sonde vérifie la garantie (tout extrait d'au moins 60 caractères est détecté) à toutes les longueurs essayées. |

**C-7, vérifié moi-même.**
- Code : dans `s2-harness/tools/oracle_record.py`, `enregistrer` (l.253-256) lève ValueError (« paquet.sha256 (64 hex)
  exigé au rôle « rendu » ; paquet.sha256 et sceau.genTime nuls hors de ce rôle ») si le rôle n'est pas `rendu` et que
  `paquet_sha256` ou `sceau_gentime` est posé. Le contrôle passe avant le contrôle d'auteur et avant tout appel à git.
  `main` (l.435-437) rend cette erreur en sortie 2. La lecture (`verifier`, l.396-397) exige les mêmes champs nuls hors
  `rendu`. Le refus vaut donc pour G1, G2 et cp-2.
- Justesse : chaque proposition de la consigne est exacte. Le test l'exerce sur l'analyseur réel, et CC-6 (outil qui
  admet `--paquet-sha256` au rôle G2) est tué.
- Sûreté : la commande commence par `env -u SHOGEN_S2_CAMPAGNE_CONTROL`. L'outil se contente de consigner la variable
  (`consigne` lit `environ`). Dans mon enregistrement, `env.SHOGEN_S2_CAMPAGNE_CONTROL` vaut `null` et
  `tests_avec_variable` est vide. Rien dans la fiche ne pose la variable.
- Applicabilité : lancée à la lettre, depuis la racine de la copie, sur un dépôt jetable où la série n'est pas commise
  (`--commit` = la tête), la commande sort en 0. L'enregistrement est `shogen-fe26b01-G2-…json`, sha256
  `639d4249…`, avec 461 fichiers et la suite s2-harness OK (skipped=2). `--verifier --role G2 --commit <tête>
  --depot` le juge conforme. La copie doit être un dépôt git : une extraction `git archive` ne suffit pas, ce que dit
  déjà « tête de la copie ». Réserve de précision : R-3.

## 2. Force des tests

Le banc est `outils/mutants_cc.py`. Chaque mutant reçoit une copie neuve et un remplacement exact (une occurrence
exigée). La suite `scripts/controle` est lancée avec `start_new_session` et une borne de 300 s (`killpg`). Classement
selon SHOGEN-MUT-FATAL-1 : sortie 1 avec FAIL, sans ERROR et avec AssertionError → tué ; 0 → vivant ; tout autre cas
→ FATAL. Le témoin non muté est vert. Le relevé `ps` de fin, filtré sur `g2/cc/`, compte 0 processus. Aucun FATAL.

| mutant | suite du lot | suite corrigée (R-2, R-3) |
|---|---|---|
| N-1 à N-3 (`fm11.py`) | tués (`test_queue_aux_longueurs_limites` et épingle) | tués |
| N-4 (exemption par le sha256 seul) | tué (`test_exempte_puis_modifie`) | tué |
| N-5 (tout `[1m]` admis) | tué (`test_formes_refusees`) | tué |
| N-6 (l'outil exige `--base`) | tué (`test_commande_passe_l_analyseur`) | tué |
| CC-1 fenêtres plafonnées au rang 40 | tué par l'épingle seule ; **vivant pour `Temoin`** | tué par `test_queue_aux_longueurs_limites` |
| CC-2 nom exempté et sha256 exempté, sans les apparier | **vivant** | tué |
| CC-3 liste blanche réduite à opus | **vivant** | tué |
| CC-4 `except` énuméré (AttributeError) | **vivant** | tué (2 sous-cas) |
| CC-5 deux racines admises | **vivant** | tué |
| CC-6 `--paquet-sha256` admis au rôle G2 | tué | tué |

Pour fm11, la sonde a couvert les longueurs du brief : 0, 1, 20, 39, 40, 41, 80 et 81. Aux longueurs de 0 à 40, les
mutants de borne (`max(0, …)`, queue seulement à partir de 40) sont équivalents, car la queue `v[-40:]` vaut la ligne
entière. Je ne les compte pas. La longueur 0 est vue en O-2.

## 3. Gates (clones creux locaux, réseau coupé, sans la variable interdite)

| gate | tête `0cfbe3e` | tête + série |
|---|---|---|
| runner | 136 ok, 0 échec | 137 ok, 0 échec (K-04 ok) |
| s2-harness `--egal` | conforme, Ran = 415 | conforme, Ran = 415 |
| s2bis `--plancher 341` | conforme, Ran = 341 | conforme, Ran = 341 |
| sim-bis `--plancher 268` (clone git) | conforme, Ran = 268 | conforme, Ran = 268 |
| calib-actifs `--plancher 65` | conforme, Ran = 65 | conforme, Ran = 65 |
| controle-unittest `--egal --plancher 18` | n/a | conforme, Ran = 18 ; planchers 17 et 19 refusés (exactitude) |
| job g1 : cas du lint, lint R-1, `journaux-modele.py .` | 227 ok ; OK 7 fichiers ; n/a | 227 ok ; OK 7 fichiers ; conforme, 52 exemptés |
| hooks | 54 ok | 54 ok |
| G5, bloc du job lu dans `gates.yml` (identique sur les deux arbres) | OK, 0 marqueur | OK, 0 marqueur |
| G3 secrets, mode indexé, et cas | n/a | OK, 11 fichiers ; 147 ok |
| xtask, lignes VERDICT seules | 8 VERT, 1 ROUGE, global ROUGE | identiques (`cmp`) |

Pour G5, les chemins interdits sont exclus par pathspec, comme à la G2. `--tree` et `--history` de G3 ne sont pas
lancés, car ils liraient les blobs exclus.

## 4. Forme

- R-25 (`git apply --numstat`) : A +199 −4, E +54 −17, B +193 −1, C +69 −1, D +2 −0, F +13 −3. Tous sous 200, et
  encore sous 200 avec R-2 et R-3.
- Lignes ajoutées : aucun marqueur de dette nu (R-13), aucun octet 92, aucun CR (contrôle sur les octets des diffs). Pour mes
  propositions, la mesure est faite sur les octets écrits.
- Retouches :
  - DT3-D ajoute 2 lignes et n'en retire aucune.
  - La fiche reçoit 8 lignes, aucune retirée.
  - Au README, E retouche l'ajout daté de A, ce que C-8 adjuge (dans le diff qui touche le fichier en dernier). E
    retouche aussi la ligne `fm11.py` du tableau, une ligne versée avant ce lot (O-1).

## 5. Versement

Un journal G1 ou G2 de ce lot, versé sous `docs/G1-*.md` ou `docs/G2-*.md`, passe le contrôle à cinq conditions :
- son nom est neuf, hors de la liste figée ;
- il porte **exactement une** ligne qui commence par les caractères `- **Modèle** :` ;
- cette ligne a la forme : tiret, espace, `**Modèle**`, espace, deux-points, espace, accent grave, identifiant, accent
  grave, puis fin de ligne ou une espace suivie d'un texte libre ;
- l'identifiant est un des quatre de la ligne `ALLOWED=` du lint (`claude-opus-5-5`, `claude-sonnet-5-5`,
  `claude-fable-5-1`, `claude-haiku-5-5`), par égalité exacte, ou cet identifiant suivi exactement de `[1m]` ;
- les fins de ligne sont LF.

Pour ce lot, la ligne attendue est la ligne 3 du présent rapport. Essai (`sorties/versement.txt`) :
`RAPPORT-GENERATEUR.md` versé sous `G1-lot-DETTES-T3.md` et `g2/RAPPORT-G2.md` sous `G2-lot-DETTES-T3.md`, avec les 52
journaux de la tête → conforme, sortie 0. Le présent rapport, essayé dans le même arbre sous `G2-lot-DETTES-T3-contre-controle.md`, passe aussi : il ne
porte qu'une ligne de cette tête. Un journal qui citerait
cette ligne en début de ligne une seconde fois serait refusé.

## 6. Aucune dette

Chaque constat corrigeable est une réserve (R-1 à R-4), avec sa forme mesurée. Aucun item n'est formé. Aucun acte
extérieur n'est ouvert par ce contre-contrôle. O-1 de la G2 (information de l'investisseur) relève de l'orchestrateur,
et son adjudication du 16:22:00 l'y place.

## Observations (O-n, sans correction)

- **O-1** : E retouche la ligne `fm11.py` du tableau du README : nouveau sha256, avec « avant : `886cc676…` ». C'est
  une table de référence, non une prose adjugée. Laisser l'ancien sha256 la rendrait fausse. La retouche est tracée par
  l'ajout daté de E et suit L-1. Il appartient à l'orchestrateur de la confirmer.
- **O-2** : à n = 0, le fragment vide est contenu dans tout texte, et tout est détecté (sûr par défaut). Le cas est
  impossible : SHA51 et SHA14 diffèrent du sha256 d'un saut de ligne seul (`01ba4719…`).
- **O-3** : SHOGEN-S2BIS-P1-ESTIMATION-1 est aussi précisé en B.63 (l.1047), B.65 (l.1074, « étendu à P3 »), B.69
  (l.1135) et B.71 (l.1165). La forme adjugée de C-6 n'est pas fausse, elle n'est pas exhaustive.
- **O-4** : `except Exception` ne couvre pas SystemExit. L'import de l'outil ne peut pas en lever : la garde
  `__main__` est là, et le module est chargé sous le nom `oracle_record`.
- **O-5** : xtask est ROUGE à l'identique sur la tête et sur la série, comme à la G2 (O-6). Le VERT avant commit reste
  celui de l'orchestrateur sur le dépôt entier.

## Écarts (E-CC-n)

- **E-CC-1** : pour C-7, j'ai créé trois dépôts jetables sous `g2/cc/tmp/` (`git init`, puis commits de fixture avec
  `core.hooksPath=/dev/null`, auteur `contre-controle`). Aucun commit n'a été fait dans le dépôt du projet. Les deux
  premiers manquaient de `docs/adr-0028/sceau` et `scripts/sceau` : suite en exit 1, enregistrements écartés. Le
  troisième fait foi.
- **E-CC-2** : un premier lancement détaché (`setsid nohup sh -c …`) a été refusé par la garde du harnais. Je l'ai
  relancé par la tâche de fond de l'outil, sans effet sur les résultats.
- **E-CC-3** : `git add -A` dans l'index du clone `w/serie` seul, pour G3 indexé et xtask.
- **E-CC-4** : lectures ciblées hors des pièces du brief, toutes dans des chemins permis :
  - `oracle_record.py` l.1-20, 100-135, 205-322 et 336-443 ;
  - `CP2-S2.md` l.20-50 et `grep G2` ;
  - `ANNEXE-B-items.md` : en-têtes l.980-1400 et lignes qui portent `ESTIMATION`, extraits ;
  - ligne `ALLOWED=` du lint ;
  - `fm11.py` l.1-14 coupé à 60 caractères : noms et sha256, aucun contenu de D.2.

  Aucune pièce de D.2 ouverte, aucun `*.jsonl` lu ou écrit, aucune recherche récursive sur `docs/` ni sur le dépôt.

## Journal de provenance (G1)

Sources [lu] :
- `CLAUDE.md` ;
- `ADJUDICATION-G1.md`, `g2/RAPPORT-G2.md` et `RAPPORT-GENERATEUR.md`, en entier ;
- les 6 diffs, en entier, et `travail/avant-g2/DT3-C.diff` et `DT3-D.diff` (lignes datées) ;
- `g2/outils/mutants_g2.py` (formes de N-1 à N-6), `iso.sh`, `gates.sh` et `xtask.sh` ;
- `outils/mutants2.py` du générateur (M-F1, M-F2) ;
- `fm11.py` de la série, l.15-47 ;
- les extraits listés en E-CC-4.

[abs] : aucune procédure écrite du cp-2 qui relie un enregistrement G2 de base aux diffs (motif de R-3).

Commandes (sorties sous `g2/cc/sorties/`) :
- clones `git clone --no-checkout --no-hardlinks` avec `sparse-checkout` (exclusions du brief ; 0 `*.jsonl`) ;
- série appliquée par `git apply --check` puis `git apply` ;
- `outils/gates.sh` sur les deux arbres (`serie-*`, `tete-*`, codes tous à 0) ;
- `outils/xtask.sh` (`xtask-*-VERDICT.txt`) ;
- `g5-*.txt`, `g3-*.txt`, `controle-exact.txt` ;
- `outils/compte_journaux.py` (16, 34 et 2) ;
- `outils/sonde_fm11.py` (rejouée pour `sorties/sonde-fm11.txt`) ;
- `outils/mutants_cc.py` : `mutants-lot.json`, `mutants-avec-cc.json` (tests de `outils/tests_cc/`) et
  `mutants-corr.json` ;
- `c5-procedure.txt` et `c7-*.txt` ;
- `versement.txt` ;
- `outils/corrections_cc.py` → `corrections-CC.diff`.

Chiffres recomptés :
- +199/−4, +54/−17, +193/−1, +69/−1, +2/−0, +13/−3 ;
- 71 sommes OK, 68 sorties ;
- sha256 de `fm11.py` `4a0b8abc…` ;
- 52 exemptés, 16/34/2 ;
- 137/136, 415, 341, 268, 65, 18, 227, 54, 147, 11 ;
- 9 lignes VERDICT plus la ligne globale ;
- 77 787 extraits de la sonde ;
- quatre campagnes de 13 runs (témoin compris) ; la copie corrigée a été passée deux fois, la seconde fait foi ;
- tailles corrigées E +55 −17, C +74 −1, F +25 −4, mesurées par `git diff --no-index --numstat`.

## Passe 2 (section datée du 2026-10-09 17:29:15 UTC, `date -u`) : vérification de C-10 à C-13

Pièces lues : l'ajout daté de `ADJUDICATION-G1.md` (16:57:58 UTC) et la section de `RAPPORT-GENERATEUR.md` datée de
17:07:04 UTC. La série est A, E, B, C, D, F, sur `0cfbe3e`. Sha256 des diffs (16 premiers caractères) :
- A `b018c1f1a7255502` ;
- E `e79bb09df37f9e65` ;
- B `6dfaff03946c3137` ;
- C `a4f4100e4e38b2b0` ;
- D `2adc9a49bb9c4e33` ;
- F `5fd1703821ecc891`.

Empreinte de la série : `02449039cbe2ffb4e0061c765a6de08c76c9b1ede888425a6f8ae97add43af44`. J'ai comparé chaque diff à
sa version de `travail/avant-cc/` (`diff`) : seuls changent les hunks visés par C-10 à C-13. A et B sont identiques à
l'octet près. Le README de E est inchangé.

### Verdict passe 2 : CONFORME

R-1 à R-4 sont levées en entier. Aucune réserve nouvelle, aucun item.

| réserve | correction | constat |
|---|---|---|
| R-1 | C-10 (F) | La docstring reprend la forme de `corrections-CC.diff` : « s'il n'en porte aucune », « 16 la portent déjà dans la forme : une seconde les ferait refuser », « (texte de DT3-F) ». Le décompte 16 / 34 / 2 a été mesuré à la passe 1, sur les mêmes journaux. |
| R-2 | C-11 (E, F) | Longueur 121, avec les extraits `(60,100,1)`, `(80,120,1)`, `(61,101,0)` et `(81,121,1)`. Trois autres identifiants de la liste blanche sont admis. Les octets de `G1-lot-CORR.md` sous le nom `G1-lot-D8a.md` sont refusés. La sortie 3 est vérifiée pour deux racines et pour un outil vide, en erreur de syntaxe ou à import manquant. Plancher toujours à 18. La sonde fm11, rejouée pour n = 0, 1, 20, 39, 40, 41, 80, 81, 121 et 200, donne 0 écart (`sorties/p2/sonde-fm11.txt`). |
| R-3 | C-12 (C) | La phrase est dans le bloc. Le test exige la suite `DIFFS + " " + BASE` en une seule assertion, qui remplace l'assertion `DIFFS` seule : la portée est la même et C passe à +73, au lieu de +74. P2-3 (phrase retirée) est tué. |
| R-4 | C-13 | Ajouts datés de l'arbre final : README 16:23:29 et 16:23:29, fiche 16:58:59, DT3-D 16:59:08. Pour la fiche et DT3-D, l'heure suit la dernière écriture : les fichiers datent de 16:59:01 et 16:59:08. Les hunks du README n'ont pas changé depuis le DT3-E de 16:23 (mtime relevé à la passe 1). Son heure, 16:23:29, est donc bien celle de sa dernière écriture. La règle tient pour les quatre ajouts. |

**Mutants** (`outils/mutants_p2.py`, `sorties/p2/mutants-p2.json`) : 15 sur 15 tués, témoin vert, aucun FATAL. Chaque
run a sa copie neuve, `start_new_session`, une borne de 300 s avec `killpg`. Le relevé `ps` de fin compte 0 processus.
- N-1 à N-6 : tués.
- CC-1 à CC-6 : tués par un test de comportement, par AssertionError :
  - CC-1 par `test_queue_aux_longueurs_limites` (et pas seulement par l'épingle) ;
  - CC-2 par `test_exempte_puis_modifie` ;
  - CC-3 par `test_nouveaux_conformes` ;
  - CC-4 et CC-5 par `test_racine_illisible` ;
  - CC-6 par `test_commande_passe_l_analyseur`.
- Neufs, sur les ajouts :
  - P2-1 (fenêtres plafonnées au rang 60) : tué par `test_queue_aux_longueurs_limites` (longueur 121) ;
  - P2-2 (`except` énuméré sans ImportError) : tué par `test_racine_illisible` (sous-cas import manquant) ;
  - P2-3 (phrase de C-12 retirée de la fiche) : tué par `test_consigne_au_bloc_de_gabarit`.

**Gates** (clones creux, réseau coupé, sans la variable interdite ; `sorties/p2/`) :

| gate | tête seule | tête + série |
|---|---|---|
| runner | 136 | 137 (K-04 ok) |
| s2-harness | 415 | 415 |
| s2bis | 341 | 341 |
| sim-bis (clone git) | 268 | 268 |
| calib-actifs | 65 | 65 |
| controle-unittest | — | Ran = 18, `--egal --plancher 18` conforme ; 17 et 19 refusés |
| job g1 | 227 cas, lint OK | 227 cas, lint OK, `journaux-modele` conforme (52 exemptés) |
| hooks | 54 | 54 |
| G5 (bloc du job identique sur les deux arbres) | 0 marqueur | 0 marqueur |
| G3 indexé et cas | — | OK, 11 fichiers ; 147 ok |
| xtask, lignes VERDICT seules | 8 VERT, 1 ROUGE | identiques à la tête (`cmp`) et à la passe 1 |

**Forme** : A +199 −4, E +55 −17, B +193 −1, C +73 −1, D +2 −0, F +25 −4, tous sous 200. Lignes ajoutées : aucun
marqueur nu, aucun octet 92, aucun CR.

**Provenance** :
- clones `--no-checkout --no-hardlinks` avec `sparse-checkout` (exclusions du brief, 0 `*.jsonl`) ;
- `git apply --check` puis `git apply` en série ;
- `outils/deux-p2.sh`, `outils/xtask-p2.sh`, `g5-p2-*.sh`, `outils/mutants_p2.py` (dérivé de `mutants_cc.py` : trois
  mutants ajoutés, préfixe `mutp2_`) et `outils/sonde_fm11.py` ;
- `git add -A` dans l'index du clone seul, pour G3 indexé ;
- aucune pièce de D.2 ouverte ;
- dépôt réel : `git status` vide, HEAD `0cfbe3e` ;
- copies supprimées à la fin (`w/`, `tmp/`, `cible-*`).
