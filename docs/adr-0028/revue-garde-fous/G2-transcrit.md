# Relecture G2 neuve de GARDE-FOUS-ORCH phase 1 (C-1 à C-18) (transcrit)

> Transcription par l'orchestrateur le 2026-10-15 20:10:04 UTC du fichier garde-fous/gf1/g2/RAPPORT-G2.md ; contrôle FM-1.1 des transcripts du générateur, du réviseur G2 et du contre-contrôleur, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Relecture G2 du lot GARDE-FOUS-ORCH, phase 1 (réviseur neuf)

Écrit le 2026-10-15 à partir de 10:49 UTC (`date -u`). Worker `shogen-worker`, réviseur G2 neuf : je n'ai ni écrit ni
relu ce lot. **Gate 0 : modèle résolu `claude-opus-5-5`** (identifiant exact déclaré par l'environnement), effort max.
Ouverture le 2026-10-10 à 08:14 UTC ; arrêt à 09:32 sur demande de l'investisseur ; reprise le 2026-10-15 à 09:38.

Brief `g2/BRIEF-G2.md` (sha256 `2f723718…7e0505`). Pièces (sha256, huit premiers caractères) : `ADJUDICATION.md` lue
à l'ouverture en `3546189b`, aujourd'hui `8257fb4c` (ajouts datés du 2026-10-10 à 08:19:22 et 14:09:16, §0) ;
`ERREURS-ORCHESTRATEUR.md` lue en `cb941153` (E1 à E25), aujourd'hui `216ce860` (E26 et E27 ajoutées) ;
`PROPOSITION.md` `eb4054d8` ; `AVIS.md` `8335b4ce` ; `gf1/BRIEF-GF1.md` `12c3673e` ; `gf1/RAPPORT-GENERATEUR.md`
`1c511b88` ; `gf1/bloc-commun-brouillon.md` `ff3c02b7` ; `gf1/SHA256SUMS` `f49f733b`, rejoué : 21 lignes OK. Série :
18 diffs, 2 309 lignes ajoutées (recomptées), concaténation dans l'ordre de la chaîne `527aa61c…36ffe`.

Copies, toutes dans des dépôts jetables à moi (`git archive` avec les exclusions des interdits et de `*.jsonl`, un
commit de base, un commit et une étiquette par diff) : ouverture sur `1b8a44d` ; reprise sur `d6ef3e9` ; **copie
finale sur `c9b5c1a`** (tête de 10:22), série puis C-1 à C-12 et C-14 à C-18 (36 commits), effacée à la fin avec
les autres copies (aucune n'avait de dépôt distant ni d'état non lu). Dernière tête relue : §8.
Aucune écriture dans le dépôt du projet, aucun réseau (outils sous `isole.sh`, sans variables de mandataire),
`SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée, aucun emplacement interdit ouvert ni listé.

## 0. Pièces changées depuis l'ouverture

- Adjudication, ajout de 08:19:22 : une ligne de plus pour GF-20 (les passes d'agents ne lancent ni g3 `--history`
  ni g3 `--tree`). Absente du brouillon : ajoutée par C-13 (§11). Lue aujourd'hui à 10:45, après trois passages de
  g3 `--tree` sur mes copies (écart E-10).
- Adjudication, ajout de 14:09:16 (décision de l'investisseur) : les erreurs sans contrôle mécanique en phase 1 (E6,
  E7, E12, E13, E18, E20, E22, E23, E26, E27) entrent dans le lot, et les outils se branchent par des crochets du
  harnais. Aucun diff de la série ne les porte : ce ne sont pas des corrections C-n de cette relecture mais le travail
  que la décision ouvre après elle. L'ordre écrit nomme « C-1 à C-17 » : la liste fermée compte désormais C-18 (§9),
  et C-13 a reçu un complément (§11).

## Verdict

**ACCEPTE-AVEC-CORRECTIONS**, liste fermée **C-1 à C-18** (§9 ; `corrections/C-n.diff`). Chaque correction de code :
rouge d'assertion montré sur l'état d'avant, vert après ; ligne exacte du job `controle-unittest` à chaque état
(plancher 90 → 107, `Ran` égal au plancher) ; `avant_acte.py diff` de l'outil corrigé en sortie 0 sur les 35 diffs
(série et corrections), à `c9b5c1a`, `2b8fb59` et `8d19a0e`. Les dix-huit diffs s'appliquent et chacun est vert seul au
plancher exact (19 états, `Ran` = plancher : 37, 37, 43, 48, 49, 53, 56, 57, 60, 63, 67, 70, 72, 75, 77, 82, 86, 88,
89) ; sommes et comptes de chaque ajout daté du README justes ; les contrôles du §3 du rapport du générateur refusent
les cas réels (33 mutants à moi sur la série : 32 tués, le vivant donne C-1). Défauts qui exigent les corrections
avant la chaîne :

1. **C-1 (grave, LA-N05)** : `verif` du modèle `gabarits/chaine.sh` est appelée par `verif "$id" && acte sceller` ;
   bash y ignore `set -e`, et la fonction rend le code de sa seule dernière commande (le lint). Essai de bout en bout
   (`outils/essai_verif.sh`) : `xtask` ROUGE, `cargo test` rouge, une ligne de `gates.yml` rouge, lint vert : la
   chaîne a scellé et commis le pas (sortie 0). C-15 complète (E5) : cargo sans `CARGO_TARGET_DIR` hérité.
2. **C-3 (faux refus réels, E9 ; E21)** : `diff` jugeait citations et corpus de `presg5` sur HEAD, avant le diff :
   DT14-a et DT14-b, commis, sortaient en 1 (65 lignes `REFUS G5` sur des citations que le même diff inscrit à
   `biblio/INDEX.md`) ; un diff hors format de git (`diff -u`, préfixes de `diff.mnemonicPrefix`) passait sans
   contrôle.
3. **C-16 (faux refus réel, E8)** : C3 ne lisait que la forme `N passes` ; l'adjudication de DETTES-T6 n'écrit que
   `passe 2` et `sans passe 3` : le message réel de DT6-d (`en deux passes`, juste) était refusé. Celui de DT5-22
   (`en trois passes`, l'erreur E8) reste refusé.
4. **C-17 (LA-N04, E11)** : la reprise du modèle saute tout pas dont la ligne `Diff-Id` est déjà dans l'historique
   (`chaine.sh` l.44) ; un nom courant (`C-1`) porté par le commit d'un autre lot faisait sauter le pas sans rien
   dire. `chaine` G4 le refuse désormais ; même message (reprise après un arrêt) : admis.
5. **C-18 (contrat GF-10b)** : hors des sous-commandes, la sortie n'était pas 3 ; mesuré (rouge du test) : module
   frère illisible, 1 (se lit refus) ; `presg5` copié sans `enforcement/` ou avec un `docs-sha256sums.py` sans
   `INTERDITS`, 1 (se lit fragment introuvable) ; sortie standard fermée (tube sans lecteur), 120, hors contrat.
6. **C-2, C-4** : `pousser --branche b` jugeait HEAD seule (une branche b en avance, porteuse d'un `docs/15-*`,
   passait) ; la suppression de branche que B.92 constate (écriture de l'API) passait `--acte` (Q-4, §5).

## 1. Erreur par erreur : contrôle, rouge rejoué, forme voisine

Rouge rejoué : mutant à moi qui retire le contrôle (`mutants/serie.log`) ou cas réel rejoué. Forme voisine : éprouvée
par les sondes `outils/sonde_*` ; une forme qui passe est fermée par une correction, sinon écrite en limite (§10).

| erreur | contrôle (§3 du rapport) | rouge rejoué | forme voisine éprouvée | issue |
|---|---|---|---|---|
| E1 | C8 (`workflows-yaml.py`) | R-19 tué | workflow d'un diff hors format de git : non lu | C-3 |
| E2 | `publier` (parties vérifiables) | R-01 tué | cause fausse : non vue | L-10 |
| E3, E25 | modèle détaché, G3 | R-21, R-24 tués | délai fixe `timeout 6600` de l'en-tête du modèle (110 min) : tue une chaîne plus longue ; `DETACHE=1` en lancement lié, durée de pas sous-déclarée : passent | C-1 ; L-11 |
| E4 | `etat_disque`, `disque` | R-09 tué | — | — |
| E5 | `verif` : `cargo test -p xtask` à la cible par défaut | R-22 VIVANT | `verif` rouge non vue ; `CARGO_TARGET_DIR` hérité déplace la cible | C-1, C-15 |
| E8, LA-N03 | C2 `Source-Sha`, C3 | R-14, R-15 tués ; DT5-22 réel refusé | `passe 2` des sources non lue (faux refus réel de DT6-d) ; `passe 3`, `troisième passe`, verdict accentué ou en minuscules, sha court d'un autre commit : non vus | C-16 ; L-3 |
| E9 | `presg5` (0, 1, 3), G5 | DT14-a réel | citation que le diff inscrit à `biblio/INDEX.md` : faux refus | C-3 |
| E10 | V2 | R-28 tué | copie retouchée d'un mot, copie partielle, copie en `.txt` : admises | L-14 |
| E11 | `GROUPES :`, G1, G2 | R-20 tué | noms écrits autrement qu'au plan (casse, `.diff`, `.patch`, préfixe) : groupe ignoré ; gabarit à `aucun` par défaut | C-7 |
| E14 | `horodatages_fautifs` | R-01 tué | seconde heure d'une plage, `19:5X` : non vues ; heure avant la date, sans date, `04 h 22`, date en lettres, lendemain : non vus | C-11 ; L-1 |
| E15 | `existe` | R-33 tué | autre casse, nom de dossier : absence fausse (X1) ; fichier ignoré par git : X1 | C-6 ; L-17 |
| E16, LA-N08 | citations, forme stricte | R-10, R-11, R-12 tués | référence en code (`chemin:N` entre accents graves) : ni refus ni avertissement ; crochets, référence avant la citation, `ligne N` : non vus | C-5 ; L-2 |
| E17 | `pousser --acte` | R-26 tué | suppression constatée (API, B.92 l.1568), `-d`, `:branche`, méthode après le chemin, `-XPUT`, `--method=PUT`, `gh repo edit` : passaient | C-4 ; L-7 |
| E19, E24 | interdits, racines | R-05 à R-08 tués | 23 formes de chemin : justes ; `verser --pieces /` lancé (parcours de `/`, sur témoin) ; dossiers interdits parcourus par `verser` ; racine interdite de `presg5` lue et nommée | C-8, C-10 |
| E21 | C7 | R-17 tué ; DT14-e et DT14-g d'origine refusés | `diff -u`, préfixes `i/` et `w/` : insertion admise ; permutation à nombre égal : refusée ; remplacement à nombre égal : admis | C-3 ; L-13 |
| LA-N01, LA-N05 | P2, P1, `sceller`, C1 | R-13, R-23, R-25, R-27 tués | branche poussée autre que HEAD : admise ; `verif` rouge scellée | C-2, C-1 |
| LA-N04 | C6 | R-16 tué | pas dont le `Diff-Id` est déjà porté par le commit d'un autre lot : sauté par la reprise | C-17 |
| GF-10b | toute exception en 3 | — | exception du journal : 1 ; module frère ou interdits illisibles : 1 ; sortie fermée : 120 | C-9, C-18 ; L-16 |
| lot lui-même | GF-0 | — | GF-0 écrit `E1 à E21` ; la liste versée porte E22 à E25 | C-14 |

## 2. Sûreté des outils (point 2)

- Interdits (GF-4) lus dans le code : `INTERDITS` de `enforcement/docs-sha256sums.py` et `motifs` de `fm11.py` par
  `ast`, sans exécuter `fm11.py` ni afficher un motif. Éprouvés : 23 formes de chemin (`./`, `//`, `..`, casse,
  barre finale, liens, `*.JSONL`, composants voisins) jugées justement ; aucun des 200 000 noms de dossiers
  temporaires tirés n'est jugé interdit par les 21 motifs de D.2 (sonde rejouée le 2026-10-15). Rien d'affiché que
  des comptes.
- Écritures : `.git/shogen-garde/` (sceaux, journal) et objets git du dépôt cible (`apply --cached`, `write-tree`) ;
  index et fichiers temporaires sous `TMPDIR`, effacés ; le modèle de chaîne écrit ses journaux près du plan.
- Aucun appel réseau dans les outils ; `pousser` et `publier` ne poussent ni ne publient : contrôles seuls.
  Sous-commandes git : `apply`, `cat-file`, `checkout-index` (vers un temporaire), `diff`, `hash-object` (sans
  `-w`), `ls-files`, `log`, `read-tree` (index temporaire), `rev-parse`, `status`, `write-tree` ; `commit` dans le
  modèle de chaîne seul.
- Contrat 0, 1, 3 : une exception d'une sous-commande sort en 3 ; celle du journal sortait en 1 (C-9) ; le chargement
  d'un module frère, les interdits illisibles de `presg5`, l'écriture et le vidage final de la sortie sortaient en 1
  ou en 120 (C-18, rouge montré sur C-17 : quatre cas de `presg5`, deux d'`avant_acte`). Reste une erreur de syntaxe
  de l'outil lui-même : l'interpréteur sort en 1 avant toute ligne de l'outil (L-16).
- Parcours : `disque --lister` refuse `/`, le dépôt, ses ancêtres, `docs`, les interdits ; `verser` n'avait aucune
  borne (C-8). Mes mutants sont bornés : racines temporaires, parcours de `verser` sur témoin, aucun mutant ne retire
  un contrôle d'interdit pour l'éprouver sur un vrai chemin.

## 3. Faux refus : rejeux réels (point 3)

`avant_acte.py diff` sur un dépôt jetable dont la tête est la base de chaque diff (`outils/rejeu.sh`) :

| série | outil de la série (GF-10b) | outil corrigé | juste ? |
|---|---|---|---|
| DT14-c sur `04f242d` | 0 | 0 | oui |
| DT6-d sur `a59eaa2` | 0 | 0 | oui |
| DT5-24 sur `57330fa` | 0 | 0 | oui |
| DT14 a à m, commis (version C-3), sur `dda4bbc` | DT14-a et DT14-b : 1 (65 `REFUS G5`), les autres 0 | 0 partout | refus faux (C-3) |
| DT14 a à g d'origine | DT14-a, b : 1 (G5, faux) ; DT14-e, g : 1 (C7) | DT14-e, g : 1 (C7) | C7 juste : E21 réel |
| série GF et corrections, sur `c9b5c1a`, `2b8fb59`, `8d19a0e` | série : 0 partout | C-18 : 0 sur les 35 diffs | oui |

`commit` sur un commit réel, dans un dépôt jetable à son parent (`outils/rejeu_commit.sh` : diff appliqué, `sceller`,
message réel, `Source-Sha` de l'adjudication du lot) : DT14-c (`953270e`) 0 ; DT5-24 (`d49df1b`) 0 ; DT6-d (`8575186`)
1, `REFUS C3 : nombre de passes du message absent des sources : 2` : faux (C-16), puis 0 ; DT5-22 (`0838597`, message
`en trois passes`) 1 avec les deux outils : juste (E8 réel).

## 4. Skills (point 4)

En-têtes lus par PyYAML : `name` égal au dossier, `description` de 216 à 263 caractères, sans `<` ni `>`, clés `name`
et `description` seules : chargeables. Chaque commande des quatre skills lancée telle qu'écrite depuis la racine d'un
dépôt jetable (`outils/skills_smoke.sh`, sur GF-10b puis sur l'état corrigé) : `diff --fichier`, `sceller`,
`commit … && git commit -q -F`, `verser --pieces`, `presg5.py .`, `date -u`, `existe`, `publier --texte`, `df -h /`,
`disque`, `disque --lister`, `chaine --plan --cc --duree-pas`, `bash -n` du modèle, `sceller --tete`, `pousser
--distant --branche`, `pousser --acte` : sorties attendues (0 ; 1 pour l'acte refusé). Une répétition : le point 4 de
`shogen-avant-lancer` redit la ligne « Tâche de fond » du bloc commun, sans commande : à retirer au diff GF-20 (C-13).

## 5. Q-4 et Q-10

**Q-4, forme exacte** (C-4) : l.8 à 10 de `garde/hors-distant.txt`, récrites à nombre égal :

```
# Écritures sur la forge refusées par le mandataire réseau (HTTP 403 ; la lecture est admise) : protection de branche
# et réglages du dépôt, le 2026-10-10 (annexe B, B.95 ; docs/adr-0028/forge-pr11/refus-mandataire.txt) ; suppression
# de branche par l'API, le 2026-10-10 (annexe B, B.92 : source exacte en fin de fichier). Motifs fnmatch de l'acte.
```

puis, en fin de fichier, la source et les motifs de la requête constatée :

```
# Relecture G2 du lot (C-4, Q-4) : la suppression refusée est celle de la branche jetable essai/analyseur-residus, par
# une écriture de l'API (réponse 403 du mandataire), docs/adr-0028/ANNEXE-B-items.md l.1568 (B.92) ; sha256 de la
# ligne entière, saut de ligne compris : 0c3a9bfc1a2dc935fb255d980882722799bbdd1ab59a51963558366cc4282196 ; et non E17
# [2nd]. Même requête écrite autrement : méthode après le chemin, -XPUT, --method=PUT (ramenés à -X PUT par l'outil),
# gh repo edit (réglages) ; suppression d'une branche par le protocole git (-d, :branche) : refus conservateur, non
# constaté.
acte *-X DELETE *git/refs/*
acte *git/refs/*-X DELETE*
acte *protection*-X PUT*
acte *repos/*-X PATCH*
acte gh repo edit*
acte git push* -d *
acte git push* :*
```

La l.1568 a le même sha256 à `1b8a44d`, `d6ef3e9`, `c9b5c1a` et à la tête de 10:47 ; la l.293 de l'ADR-0028
(`16e208a9…`) aussi. Le test `test_c4_actes_voisins_et_sources` rejoue les deux lignes sources.

**Q-10**, entrée par entrée (preuve : renvoi par numéro lu dans un fichier nommé) :

| entrée | jugement |
|---|---|
| `ADR-0028-decisions-sortie-S2.md` | juste : l.293 citée (`hors-distant.txt`) ; E21 |
| `ANNEXE-B-items.md` | juste : l.1568 (Q-4) ; `docs/17` cite l.147 |
| `CP2-S2.md` | juste : la fiche worker cite l.36-37 |
| `G0-lots-DETTES.md` | admissible : aucun renvoi par numéro trouvé (renvois par section) ; ajout en fin par usage |
| `docs/17-*` | juste : E21 ; S-G9 lit ses renvois |
| `JOURNAL.md` | juste : `docs/17` cite l.80 ; E16 |
| `scripts/controle/README.md` | juste : la proposition cite l.1-7, l.11, l.55-59 |
| `scripts/controle/garde/*` | admissible, sans preuve de renvoi ; ajout en fin des données (C-4 s'y tient) |
| `.claude/agents/*.md` | juste : la proposition cite `shogen-orchestrator.md:83-86` et `:14` |

Ce qui manquait : les documents que `docs/17-modele-de-menace.md` cite par numéro, `docs/AUDIT-ENTREE.md` (l.13, 20,
41), docs 03, 04 (l.143-146, 166-172), 09, 13, `docs/G1-lot-B0-pool-analyse.md`, `CLAUDE.md` (l.20-32) : ajoutés par
C-12, avec un test qui exige que tout `.md` cité par numéro dans `docs/17` suive un motif. `biblio/INDEX.md`
(l.18, 19, 325-327) et les workflows (`gates.yml` l.35, 54-92, 144-192 ; `squelette.yml`, `compagnon.yml`,
`temoignage.yml`), cités aussi, restent dehors : DT14-a, commis, serait refusé si `biblio/INDEX.md` y était, et `diff`
n'a pas de voie d'admission ; `docs/17` dit lui-même périmés deux renvois à `gates.yml` (L-15).

## 6. Mutants (point 6)

Banc `outils/banc.py` : remplacement exact (une occurrence), base verte exigée, ligne exacte du job lue dans
`gates.yml` de la copie, sous `isole.sh`, sans mandataire, `TMPDIR` de mon dossier, groupe de processus tué au délai,
fichier relu par sha256 après restauration ; 1 tué, 0 vivant, toute autre sortie FATAL ; relevé `ps` à la fin.

| campagne | état, plancher | mutants | tués | vivants | FATAL |
|---|---|---|---|---|---|
| série (`mutants_g2.py`, `serie.log`) : horloge 4, interdits et disque 5, citations 3, commit 7, chaîne 5, pousser 3, verser 3, `presg5` 1, journal 1, `existe` 1 | GF-10b, 89 | 33 | 32 | 1 (R-22 : C-1) | 0 |
| corrections (`mutants_corr.py`, `corrections.log`) : les 33, dont 5 adaptés au texte corrigé, et K-01 à K-25 | C-12, 103 | 58 | 57 | 1 (R-30' : test de C-8 renforcé, puis tué) | 0 |
| finale du 2026-10-10 (`final.log`) : K-26, K-27 (C-15) | C-17, 105 | 2 | 2 | 0 | 0 |
| C-18 (`mutants_c18.py`, `c18.log`) : K-31 à K-38 | C-18, 107 | 8 | 8 | 0 | 0 |

R-30' : V0 retiré au niveau du fichier, non couvert depuis que C-8 écarte les dossiers interdits ; le test de C-8 a
reçu un fichier `*.jsonl` parmi les pièces, et R-30' a été tué au rejeu (NOTES, 2026-10-10). La campagne finale a été
coupée par l'arrêt de 09:32 : K-28, K-29 (C-16), K-30 (C-17) et R-30' relancé n'ont pas été joués, et la reprise ne les
nommait pas (écart E-8) ; les contrôles de C-16 et C-17 ont leur test rouge montré sur l'état d'avant (contrôle
absent), pas de mutant partiel. Aucun mutant équivalent parmi ceux joués ; défense en profondeur non mutée : la lecture
des chemins par `git apply --numstat` avant l'application (C-3) double le refus D1 d'après l'application.

## 7. Gates (point 7)

Copie finale (`c9b5c1a`, série, C-1 à C-12, C-14 à C-18), sous `isole.sh`, sans variables de mandataire ni
`SHOGEN_S2_CAMPAGNE_CONTROL` (`outils/gates.sh`, `tmp/gates-tete-c18.txt`) : toutes les étapes `run:` de `gates.yml`
(g3 `--history` excepté) en sortie 0 : hooks 57 ok ; aucun marqueur de dette nu ; runners épinglés (7 workflows,
22 clés) ; workflows-yaml 16 cas, conforme (PyYAML 6.0.1) ; model-pinning 227 cas, lint R-1 sur 12 fichiers ;
journaux-modele conforme ; docs-sha256sums conforme (42 fichiers SHA256SUMS, 324 lignes) ; secrets 147 cas, `--tree`
1244 fichiers ; runner verdict-suite 137 ok ; S2 `Ran = 419` ; s2bis 358 ; sim-bis 279 ; calib-actifs 76 ;
controle 107. Mêmes étapes vertes à l'état C-17, sur `d6ef3e9` (`tmp/gates-final.txt`) et sur `c9b5c1a`
(`tmp/gates-tete.txt`).

Matrice `scripts/controle` en `-X dev -W error -B` (`tmp/matrice-tete-c18.txt`) : Python 3.10, 3.11, 3.12, 3.13 :
`Ran 107`, OK ; aucun fichier compilé laissé.

Cargo, à la cible par défaut de la copie de `d6ef3e9` (état C-17 ; I-1) : `cargo --locked test -p xtask`, sortie 0,
100 tests passés, 0 échec ; forme de la CI `cargo test --locked --workspace`, sortie 0, 269 passés, 0 échec, 0 ignoré ;
`cargo --locked xtask verify` (lignes VERDICT seules, `outils/verdicts.py`) : huit VERT, un ROUGE (S-G9, une
violation, `docs/17-modele-de-menace.md:70`, qui cite un fichier d'un emplacement exclu, absent de la copie creuse :
attendu), verdict global ROUGE attendu. Entre `d6ef3e9` et `c9b5c1a`, aucun changement dans `crates`, `xtask`,
`Cargo.toml`, `Cargo.lock`, `rust-toolchain.toml`, `docs/17-modele-de-menace.md` (diff limité à ces chemins) ; la
série et les corrections ne touchent ni le Rust ni `docs/17`.

## 8. Tête du moment

Têtes relevées : `1b8a44d` (ouverture), `57b40a8`, `6f77aca`, `750ed24`, `73894cc` (le 2026-10-10) ; `a45f363`
(crochets `.claude/hooks/`), `d6ef3e9` (reprise), `41e69bd`, `9c75ef5`, `c9b5c1a`, `2b8fb59`, `29d945d`, `8d19a0e`
(le 2026-10-15, chaîne DETTES-T2). Dans les chemins de la série, l'amont n'a touché que `gates.yml`, hors des blocs de
la série (planchers d'autres jobs). **La série s'applique sur la tête du moment** : sur `2b8fb59` (10:44) puis sur
`8d19a0e` (10:54), série et corrections appliquées dans l'ordre (36 commits) ; ligne du job `Ran = 89` à GF-10b et
`Ran = 107` à C-18 ; `avant_acte.py diff` : outil de la série, 18 diffs sur 18 en sortie 0 ; outil C-18, 35 sur 35
(`outils/tete_fin2.sh`, `tmp/tete-fin2.txt`, `tmp/tete-fin3.txt`).

## 9. Corrections (liste fermée)

`corrections/C-n.diff` est le diff de l'état C-(n-1) à C-n (C-1 depuis GF-10b ; C-18 depuis C-17) ; C-13 porte sur
`gf1/bloc-commun-brouillon.md` (texte de GF-20, non posé) et s'applique à la pièce telle que versée. Une correction de
code porte son ajout daté en fin de `scripts/controle/README.md` (sha256 des fichiers, heure de `date -u` lue par le
script d'écriture, `ecrire/`).

| C-n | objet | fichiers | lignes ajoutées | plancher | sha256 |
|---|---|---|---|---|---|
| C-1 | `verif` du modèle : chaque pas sort en 1 à son échec ; lignes de `gates.yml` lancées ; délai du lancement détaché calculé, non plus 6600 fixe ; test sur la vraie `verif` | `chaine.sh`, test, README, `gates.yml` | 69 | 90 | `5523e490` |
| C-2 | `pousser` P3 : la branche poussée est HEAD | `avant_acte.py`, test, README, `gates.yml` | 37 | 91 | `97494374` |
| C-3 | `diff` lu comme git l'applique (D1 sur `git apply --numstat`, analyse de l'index temporaire) ; C5 et G5 sur l'état d'après le diff ; préfixes a/ b/ forcés | `avant_acte.py`, `garde_commun.py`, test, README, `gates.yml` | 115 | 94 | `26bd2e0c` |
| C-4 | Q-4 : source de la suppression de branche (B.92 l.1568) ; motifs de la requête constatée et de ses formes voisines | `hors-distant.txt`, `avant_acte.py`, test, README, `gates.yml` | 62 | 95 | `b43ac021` |
| C-5 | forme stricte de citation à référence en code | `garde_commun.py`, test, README, `gates.yml` | 22 | 96 | `07b9553f` |
| C-6 | `existe` : toute casse, fichiers et dossiers ; X1 nomme ce qui n'est pas cherché | `avant_acte.py`, test, README, `gates.yml` | 35 | 97 | `4a62b0d7` |
| C-7 | `chaine` G1 : noms de `GROUPES :` pris au plan ; gabarit à remplir | `avant_acte.py`, `rapport-cc.md`, test, README, `gates.yml` | 37 | 98 | `c1759b14` |
| C-8 | `verser` : `/`, dépôt et ancêtres refusés avant tout parcours ; interdit jamais parcouru (V0) ; fichier non ordinaire jamais ouvert (V5) | `avant_acte.py`, test, README, `gates.yml` | 54 | 99 | `55aa18f3` |
| C-9 | exception du journal : sortie 3 | `avant_acte.py`, test, README, `gates.yml` | 34 | 100 | `a72c35cc` |
| C-10 | `presg5` : racine jugée par les interdits | `presg5.py`, test, README, `gates.yml` | 19 | 101 | `667fab81` |
| C-11 | heures : toute heure dans les 25 caractères après une date du jour (plages) ; `19:5X` | `garde_commun.py`, test, README, `gates.yml` | 33 | 102 | `3e99c59b` |
| C-12 | Q-10 : documents cités par numéro dans `docs/17`, ajoutés en fin ; test de couverture | `lignes-citees.txt`, test, README, `gates.yml` | 34 | 103 | `66b4754d` |
| C-13 | GF-20 : phrase verbatim, mutants bornés, `git archive` avec exclusions, ligne g3 adjugée, taille estimée, point 4 du skill à retirer | `gf1/bloc-commun-brouillon.md` | 16 | — | `c56b275f` |
| C-14 | GF-0 : `E1 à E25`, heure relue | `docs/adr-0028/G0-lots-DETTES.md` | 2 | 103 | `ff354a6e` |
| C-15 | `verif` : cargo sans `CARGO_TARGET_DIR` ni `CARGO_BUILD_TARGET_DIR` (E5) | `chaine.sh`, test, README | 20 | 103 | `eaab727a` |
| C-16 | C3 : `passe N` des sources, hors négation | `avant_acte.py`, test, README, `gates.yml` | 35 | 104 | `d1c6cdbf` |
| C-17 | `chaine` G4 : `Diff-Id` du plan déjà porté par un commit d'un autre message | `avant_acte.py`, test, README, `gates.yml` | 37 | 105 | `88f8b1e8` |
| C-18 | contrat 0, 1, 3 hors des sous-commandes : chargement, interdits illisibles de `presg5`, écriture et vidage de la sortie | `avant_acte.py`, `presg5.py`, deux tests, README, `gates.yml` | 109 | 107 | `ba1b1b02` |

Total : 770 lignes ajoutées, chaque diff sous 200 (R-25) ; aucune ligne de code ni de README de plus de 120
caractères. Ordre de la chaîne : après GF-10b, C-1 à C-12, C-14 à C-18 ; C-13 se joint au diff GF-20. État final :
`test_avant_acte.py` 36 tests, `test_garde_commun.py` 17, `test_gabarit_chaine.py` 8, `test_presg5.py` 7,
`test_skills.py` 2.

## 10. Limites L-1 à L-13, et limites nouvelles

| limite | jugement | déclencheur |
|---|---|---|
| L-1 | juste, amendée : la seconde heure d'une plage et `19:5X` sont fermées (C-11) ; restent une heure avant sa date, sans date, en d'autres écritures, après plus de 25 caractères, un lendemain, deux lignes, une heure passée fausse | refus manqué relevé au journal ; phase 3 |
| L-2 | juste, amendée : la référence en code est fermée (C-5) ; crochets, référence avant la citation, `ligne N`, guillemets droits : ni refus ni avertissement | lecture du journal (avis c.4 : durcir après mesure) |
| L-3 | juste, amendée : présence, non sens ; `passe 3`, `troisième passe`, verdict en minuscules ou accentué : non lus ; un sha court d'un autre commit passe ; négation lue dans les sources seules (C-16) | E8 récidive au journal |
| L-4 | juste ; la `verif` du modèle ne s'ouvre plus à un pas rouge (C-1, C-15) | fonction `verif` versionnée (SHOGEN-GARDE-VERIF-VERSIONNEE-1) |
| L-5 | juste ; `verser` ne parcourt plus un interdit (C-8) ; `sceller` et `existe` lisent des noms en mémoire | crochet de la phase 2 |
| L-6 | juste ; la branche poussée est HEAD (C-2) | acte réseau |
| L-7 | juste, réduite par C-4 : autres outils (`curl`, outils MCP), alias, variables | refus nouveau du mandataire |
| L-8 | juste ; le corpus d'après le diff est fermé (C-3) ; `WISHLIST.md` hors du corpus de `presg5` | `xtask` reste le juge |
| L-9 | juste : un retrait automatique du pas dans l'arbre du projet serait un geste d'écriture risqué | chaîne relancée sur un index sale |
| L-10 | juste (phase 3, Q-11) | décision de phase 3 |
| L-11 | juste : `DETACHE` et la durée d'un pas sont déclarés ; le délai réel du lancement détaché n'est pas vu | chaîne tuée à la borne |
| L-12 | juste ; en lecture seule, l'échec d'écriture des objets se lit D2 (refus) au `diff` | SHOGEN-GARDE-LECTURE-SEULE-1 |
| L-13 | juste : une permutation est vue (C7) ; refuser tout remplacement refuserait DT14-m et les errata à nombre égal | contrôle par ligne (Q-9, SHOGEN-REFS-LIGNE-CONTENU-1) |
| L-14 (nouvelle) | V2 ne voit qu'une copie entière d'un `.md` dans un `.md` ; une fenêtre partagée refuserait les citations longues | E10 récidive |
| L-15 (nouvelle) | `biblio/INDEX.md` et les workflows, cités par numéro dans `docs/17`, hors de C7 (§5) ; renvois périmés de `docs/17` (`CLAUDE.md:20-32`, `gates.yml`) : à un lot de `docs/17`, non à celui-ci | Q-9 ; SHOGEN-REFS-LIGNE-CONTENU-1 |
| L-16 (nouvelle, réduite par C-18) | une erreur de syntaxe de l'outil lui-même sort en 1 : l'interpréteur échoue avant toute ligne de l'outil | installation abîmée ; la ligne du job la voit |
| L-17 (nouvelle) | `existe` ne cherche pas les fichiers ignorés par git (X1 le dit depuis C-6) : les chercher parcourrait des arbres ignorés, emplacements locaux compris | absence affirmée d'un fichier ignoré |

## 11. GF-20 (brouillon du bloc commun, jugé comme texte)

Le bloc porte les règles adjugées (non-décalage, liste explicite de chemins, lancement détaché, `avant_acte.py diff`,
base de la copie) et ne répète pas DETTES-T7 (Q-6). C-13 : la phrase de la fiche orchestrateur §4 verbatim, minuscule
initiale comprise ; aucun mutant ne parcourt `/` ni un interdit (écart E-8 du générateur) ; `git archive` toujours
avec les exclusions, même vers un tube (écart E-1 du générateur) ; la ligne adjugée le 2026-10-10 à 08:19:22 (g3
`--history` et `--tree` hors des passes d'agents ; la CI de la forge les porte), avec sa source au tableau ; la taille
estimée du diff GF-20 relevée à 6 × 27 lignes, environ 200 lignes, à couper en deux diffs au-delà de 200 (R-25) ; le
point 4 de `shogen-avant-lancer` retiré dans le même diff. `git apply` de C-13 sur la pièce rend le brouillon corrigé.

## 12. Écarts

- E-1 Les premières passes du 2026-10-10 (états de la série, sondes, rejeux, jusqu'à 08:39) ont tourné avec le
  `TMPDIR` du système (temporaires créés et effacés sous `/tmp`) ; `TMPDIR` de mon dossier ensuite.
- E-2 Une sortie de `grep` ciblé sur `docs/17-modele-de-menace.md` a affiché, parmi ses renvois, le nom d'un fichier
  d'un dossier interdit (nom déjà écrit au §8 de `CLAUDE.md`) ; aucun fichier interdit ouvert ni listé. Le 2026-10-15,
  la ligne 70 de `docs/17` a été lue par un script qui n'affiche pas le chemin exclu.
- E-3 J'ai relevé le nombre (21) et les longueurs extrêmes des motifs de D.2, jamais un motif.
- E-4 L'en-tête de l'ajout daté de C-2 a été raccourci une minute après l'heure lue (faits inchangés) ; celui de C-16
  a été relu par `date -u` après une retouche.
- E-5 Commits, étiquettes, `git reset --hard`, `commit --amend` et `tag -f` dans mes dépôts jetables, jamais dans le
  dépôt du projet.
- E-6 Copies finales : `objects/info/alternates` vers les objets du dépôt du projet, en lecture, pour le job sim-bis
  (historique de `f35a70c` et `f458980`), comme l'écart E-7 du générateur.
- E-7 `pwd` en erreur après l'effacement d'un dossier où le shell se trouvait ; sans effet.
- E-8 Arrêt du 2026-10-10 à 09:32 : la campagne finale a joué la base et K-26, K-27 puis s'est arrêtée ; deux
  temporaires laissés sous mon `TMPDIR`, effacés à la reprise ; la copie de campagne effacée à la reprise. K-28 à
  K-30 et R-30' relancé non joués (§6). Mon contexte a été compacté pendant la reprise : je n'ai pas relu mon journal
  (`*.jsonl`, interdit) ; les faits viennent de `NOTES.md`, de mes fichiers et des relevés du 2026-10-15.
- E-9 Lecture du journal de `cargo test` : mon filtre de lignes `error` a affiché trois lignes d'un cas semé du
  harnais `xtask` (crate jouet compilée en échec exprès) ; la sortie de `xtask verify` n'a été lue que par ses lignes
  VERDICT et l'emplacement de S-G9. Journaux bruts de cargo et de `xtask` effacés après extraction (ils portent des
  jetons `chemin:ligne` non lus) : bilans et lignes VERDICT gardés dans `tmp/affiche-1015.txt`.
- E-10 g3 `--tree` lancé trois fois aujourd'hui sur mes copies (point 7 du brief) avant que je lise l'ajout de 08:19:22
  qui l'exclut des passes d'agents : copies tirées par `git archive` avec les exclusions, donc sans les dossiers
  interdits ni `*.jsonl` ; une pièce de D.2 hors de ces dossiers, s'il en est, a pu être lue par la gate dans un
  temporaire, rien n'en a été affiché (dernière ligne seule). Cause : pièces non ré-empreintées à la reprise. Les
  étapes `g5-todo` (`git grep`) et `g3-cas` ont aussi cherché dans mes copies, comme le point 7 le demande.
- E-11 Cargo lancé sur la copie de `d6ef3e9`, non sur celle de `c9b5c1a` : aucun changement entre les deux dans les
  chemins que cargo et S-G9 lisent (§7).
- E-12 C-18 et le complément de C-13 trouvés à la reprise (L-16 relue sous la règle « aucune dette » ; ajout de
  08:19:22), après la liste de reprise, qui ne les nommait pas.
- E-13 Le crochet R5 du dépôt a refusé deux écritures de ce rapport (identifiant affiché seulement dans une sortie qui
  portait la marque du crochet, écartée par lui) ; rapport écrit après un relevé par outil de chaque identifiant et
  nombre (`outils/releve_final.sh`, `tmp/releve-final.txt`) et contrôlé par `outils/controle_nombres.py`.
- E-14 La tête avance pendant l'écriture (chaîne DETTES-T2) : les gates complètes sont sur `c9b5c1a` ; le dernier
  rejeu (application, ligne du job, `diff`) est sur `8d19a0e`, tête du moment à 10:54.
- E-15 En écrivant `SHA256SUMS`, une commande a créé puis effacé dans la même ligne une liste temporaire de mes noms
  de fichiers sous `/dev/shm`, hors de mon dossier (reste d'une première forme de la commande) ; vérifié absent ensuite.
  Avant la somme, mes brouillons périmés (gabarit du rapport, tables de travail) et les doublons à l'octet des diffs
  de correction et des journaux de mutants ont été effacés de mon dossier.

## 13. Journal de provenance

Sources lues, niveau [lu] : le brief ; les sept pièces (empreintes en tête), dont les ajouts de l'adjudication de
08:19:22 et 14:09:16 et les lignes E22 à E27 des erreurs, lus le 2026-10-15 ; les dix-huit diffs en entier ;
`gf1/NOTES.md` ; `s2bis/p1b/g2/travail/outils/isole.sh`, `lo_up.py` ; dans la copie : `.github/workflows/gates.yml`,
`enforcement/verdict-suite-s2.py`, `enforcement/docs-sha256sums.py`, les outils et tests de `scripts/controle`,
`docs/adr-0028/ANNEXE-B-items.md` l.1568, `docs/adr-0028/forge-pr11/refus-mandataire.txt`,
`.claude/agents/shogen-orchestrator.md` (§4), `CLAUDE.md` ; renvois par numéro relevés par recherche ciblée dans des
fichiers nommés ; `.claude/hooks/garde_faits.py` et `.claude/settings.json` (crochets de la reprise) ; diffs réels
(DT14 a à m, DT6-d, DT5-22, DT5-24) lus par les outils ; messages des commits `953270e`, `8575186`, `d49df1b`,
`0838597`. Aucun chiffre de seconde main : lignes, sommes, comptes de tests, planchers, bilans de mutants et de gates
recomptés par script (`tmp/releve-final.txt`, journaux de `mutants/`, `tmp/*.txt`). Aucune variable de clé lue, rien
sur Pocket, aucune commande git d'écriture sur le dépôt du projet ; commandes git de lecture limitées à des listes de
chemins explicites ; `git archive` avec les exclusions. Commandes, heures et sorties : `g2/NOTES.md` ; scripts :
`g2/outils/`, `g2/ecrire/` ; mutants : `g2/mutants/`.
