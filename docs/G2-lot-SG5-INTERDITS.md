# Revue G2 — lot SG5-INTERDITS (SHOGEN-SG5-NOTES-INTERDITS-1)

- **Gate 0** : modèle résolu `claude-opus-5-5` (effort max). Réviseur neuf : je n'ai rien écrit de ce lot.
- **Horloge** (`date -u`) : début 2026-10-04 13:47:43 UTC ; rapport écrit vers 14:07 UTC.
- **Brief** : `…/s2bis/sg5/g2/BRIEF-G2-SG5.md`, sha256 recalculé `364eaaf8357f8e0d12d131f13d2460b6115c8412b46cc235d62c62c07be34808` (conforme).
- **Base** : dépôt `/home/user/shogen`, branche `claude/compassionate-noether-szmdyj`, tête `2c2fbe9c57fa80976a7598fec841b54dd3c09030`,
  arbre de travail propre avant et après ma revue (`git status --short` : 0 ligne). Aucune opération git en écriture.
- **Contrat** : G0 `docs/adr-0029/G0-lots-S2BIS.md` l.12 (ligne SG5-INTERDITS) ; item SHOGEN-SG5-NOTES-INTERDITS-1,
  `docs/adr-0028/ANNEXE-B-items.md` l.828 (bloc B.51).

## 1. Verdict

**ACCEPTE-AVEC-CORRECTIONS** : trois corrections, liste fermée (§2). Le code de `sg5.rs` est juste : dans les deux régimes,
S-G5 n'imprime plus aucun texte de citation située en emplacement interdit, et verdict et comptes ne changent pas. Les
corrections portent sur deux trous du jeu de tests (cinq de mes treize mutants survivent) et sur une phrase de documentation
qui promet plus que ce que le lot garantit.

## 2. Corrections (liste fermée)

**C-1 — témoin des bornes incomplet (diff 01, +4 lignes).** Le témoin `temoin_sg5_interdits_voisins_gardent_le_texte` fixe la
borne de fin de `docs/15-` et de `docs/rapports/`, l'ancrage à la racine et la troncature de `monark-m009a`. Il ne fixe pas la
borne de fin des quatre autres entrées. Mes mutants G03 à G06 (borne sans tiret ou sans barre finale) survivent. Ils masquent
alors le texte d'un document légitime et faussent le compte (preuve : §3.5, fichier 15). Correction : ajouter au tableau
`voisins` quatre chemins : `docs/160-voisin.md`, `docs/pocket-reportage/voisin.md`, `docs/adr-00250/voisin.md`,
`docs/adr-0028/monark-m009ab/voisin.md`.

**C-2 — compte des masques non contraint (diff 01, +1 à +6 lignes).** Aucune fixture interdite ne porte de citation présente
au corpus. Le mutant G15 survit : il compte aussi les citations trouvées, donc la note « N fragment(s) introuvable(s) » devient
fausse. Correction : dans `mutant_sg5_interdits_complet_chemin_ligne_sans_texte`, ajouter à une fixture interdite (par
exemple `docs/rapports/factice.md`) une citation présente au corpus synthétique, par exemple
“this quotation is present in the corpus and it is checked by the gate”. Les assertions existantes restent telles quelles :
six violations, note « : 6 fragment(s) introuvable(s)… ».

**C-3 — sur-promesse dans la doc du module (diff 02, 0 ligne de plus).** Le paragraphe ajouté en tête de `sg5.rs` dit : « un
`verify` lancé sur l'arbre réel n'affiche pas de matière interdite à qui le lit ». C'est faux pour `verify` pris en entier.
J'ai mesuré que S-G4 imprime encore, en extrait, la ligne entière d'un fichier interdit (§3.7). Un lien symbolique fait aussi
imprimer le texte par S-G5. Correction : borner la phrase à S-G5 et nommer les limites mesurées. Formulation possible, en huit
lignes comme l'actuelle : « … jamais par son texte. Verdict et comptes n'en dépendent pas. Limites : le masque ne couvre que
S-G5 (S-G4 imprime encore la ligne en extrait) ; un emplacement absent de la liste, ou atteint par un lien symbolique, imprime
son texte. »

**Budget mesuré** sur un prototype de C-1 et C-2 (forme longue de C-2, six lignes ; copie séparée `g2/proto`, preuve seulement,
pas un livrable) : diff 01 = 146 lignes ajoutées, diff 02 = 52, soit **198 ≤ 200**. Sur ce prototype : `cargo fmt --check`
vert, `cargo clippy -p xtask --all-targets -D warnings` vert, suite `xtask` verte (80 + 9), **mes 13 mutants tués**.

**Contrôle de clôture proposé** : rejouer `g2/outils/mutants_g2.py` sur la copie corrigée (13 tués, 0 FATAL). Puis rejouer
la suite `xtask`, `verify` sur une copie sans dossiers interdits, et recompter les lignes ajoutées.

## 3. Contrôles demandés

### 3.1 Application et taille (contrôle 1)
- Les 53 empreintes de `sortie/SHA256SUMS` sont conformes, vérifiées depuis `sg5/` : les chemins y sont relatifs à `sg5/`, pas
  à `sortie/`.
- `git apply --check --whitespace=error` sur la tête : code 0 pour les deux diffs. Application réelle sur ma copie : propre.
  Les fichiers obtenus ont exactement les sha256 du worker (`sg5.rs` 57c4c71c…, `mutants.rs` 8c223c80…). `orig/` du worker
  est identique à la tête.
- Lignes ajoutées : diff 01 = **136**, diff 02 = **52** (7 retirées), total **188 ≤ 200**. Fichiers touchés : `xtask/src/sg5.rs`
  et `xtask/tests/mutants.rs` seulement.

### 3.2 Conformité à l'item (contrôle 2)
J'ai écrit mes propres fixtures, plus riches que celles du worker (`g2/outils/fixtures_g2.py`) :
- formes « dossier » et « fichier » ;
- imbrication profonde ;
- une citation sur deux lignes ;
- une citation élidée (deux fragments sur la même ligne) ;
- une citation trouvée au corpus, un fragment court et un fragment français (écartés) ;
- huit voisins hors liste, dont `s2-harness/docs/rapports/` et `docs/Rapports/`.

J'ai lancé `xtask gates` du binaire de la tête et du binaire corrigé, dans les deux régimes :
- **Corpus complet** : 19 contrôlés, 3 écartés, 16 violations, ROUGE, identiques dans les deux binaires. Marques interdites
  imprimées : 8 par la tête, **0** par le corrigé. Les 8 voisins gardent leur texte. La note de masque compte 8 (la citation
  trouvée n'est pas comptée).
- **Corpus incomplet** : 19 contrôlés, 3 écartés, 19 non contrôlés, VERT, identiques. Marques interdites : 8 par la tête,
  **0** par le corrigé. La note de masque compte 9 : la citation « trouvée » ne l'est pas sans octets, c'est correct.
- Les lignes de verdict et toutes les lignes des autres gates sont identiques entre les deux binaires (fichier 12).

`verify` sur mes copies sans dossiers interdits, à la tête puis avec les diffs (sortie redirigée, verdicts lus par script) :
- code 1 dans les deux cas ;
- huit gates VERT ; S-G9 ROUGE avec 1 violation, située en `docs/17-modele-de-menace.md:70` (rouge connu,
  SHOGEN-SG9-COPIE-INTERDITS-1) ;
- fmt, no_std et clippy VERT ;
- S-G5 : 310 contrôlés, 6694 écartés, 267 non contrôlés, à l'identique ;
- seule différence : la nouvelle note de masque (compte 0 sur la copie).

### 3.3 Le choix « masquer les emplacements interdits seulement » (contrôle 3)
**Juste.**
- Il suit la lettre du G0 (« n'imprime plus que `chemin:ligne` pour les dossiers interdits »).
- Il garde une exigence G2 antérieure : chaque fragment non contrôlé est nommé (témoin
  `temoin_sg5_corpus_incomplet_dit_partiel_et_liste_les_non_controles`, revue G2 du 2026-08-13, majeure 4). Le mutant M09 du
  worker, « masque partout », est tué par ce témoin.
- Il garde la valeur de diagnostic de S-G5 : 267 fragments non contrôlés sur une copie cloud, à trier sans ouvrir 267 endroits.
- Son coût est la dépendance à une liste tenue à la main, et aux liens symboliques. Le code nomme la première limite ; les deux
  sont à couvrir par les items I-2 et I-3 (§5).

Je n'ai pas eu le texte des motifs du worker (§3 de son rapport) ; mon avis s'appuie sur le code, le G0 et l'item.

### 3.4 Rouge avant, vert après, rejoués (contrôle 4)
Chaque copie a sa propre cible cargo et son propre `TMPDIR` (voir l'incident O-6) :
- **Tête** : 77 + 9 verts.
- **Tête + diff 01** : 78 verts, **2 rouges** (`mutant_sg5_interdits_complet…` et `mutant_sg5_interdits_incomplet…`). Les deux
  échouent sur l'assertion « texte d'une citation en emplacement interdit imprimé » (`mutants.rs:799`). Les assertions de
  verdict et de comptes passent déjà sur la tête : le verdict inchangé est donc bien fixé. Le témoin des voisins passe avant
  comme après.
- **Tête + diffs 01 et 02** : 80 + 9 verts.
- Suite `s2-harness` sur la copie corrigée : 405 tests, OK (2 sautés).

### 3.5 Mutants du réviseur (contrôle 5)
Treize mutants, tous dans `sg5.rs` corrigé (`g2/outils/mutants_g2.py`). Classement :
- construction en échec : FATAL ;
- binaire identique à la référence : FATAL (garde de fraîcheur) ;
- sortie 0 : vivant ;
- sortie 101 avec un test en échec : tué.

| id | famille | mutation | lot livré | avec C-1 et C-2 |
|---|---|---|---|---|
| G01 | liste | `docs/pocket-reports/` (faute de frappe) | tué | tué |
| G02 | liste | `docs/adr-0026/` au lieu de `docs/adr-0025/` | tué | tué |
| G03 | borne | `docs/16` sans tiret | **vivant** | tué |
| G04 | borne | `docs/pocket-report` sans barre | **vivant** | tué |
| G05 | borne | `docs/adr-0025` sans barre | **vivant** | tué |
| G06 | borne | `…/monark-m009a` sans barre | **vivant** | tué |
| G07 | borne | prédicat évalué sur le chemin absolu | tué | tué |
| G09 | binaire | texte passé par le champ `extrait` (ligne `      \| …`) | tué (test binaire seul) | tué |
| G10 | binaire | texte imprimé sur stderr | tué | tué |
| G11 | binaire | texte poussé dans une note annexe | tué | tué |
| G14 | verdict | ligne décalée de un en emplacement interdit | tué | tué |
| G15 | compte | compteur déplacé avant la recherche au corpus | **vivant** | tué |
| G16 | verdict | régime incomplet : chemin remplacé par une étiquette | tué | tué |

Lot livré : **8 tués, 5 vivants, 0 FATAL**. Les cinq vivants ont été construits (binaire changé) puis testés (80 verts). Ils
ne sont pas équivalents : sur mes fixtures, chacun change la sortie (fichier 15). Avec C-1 et C-2 : **13 tués**.

G09 montre l'intérêt du contrôle sur la sortie réelle du binaire : l'aide `motifs()` du fichier de tests ne lit pas le champ
`extrait`, et seul le test binaire attrape cette fuite. Les 21 mutants du worker (tous tués, `journal/04-mutants-bilan.txt`)
sont distincts des miens.

### 3.6 R-13, R-8, tests, verify (contrôle 6)
- R-13 : aucun `TODO`, `FIXME`, `XXX` ni `HACK` dans les lignes ajoutées.
- R-8 : aucune dépendance (ni `Cargo.toml` ni `Cargo.lock` touchés) ; `xtask` reste sans dépendance tierce.
- Aucun `unsafe`, `unwrap`, `expect`, `panic!` ni indexation dans le code ajouté.
- Suite `xtask` et `verify` : §3.2 et §3.4.

### 3.7 Les trois items proposés (contrôle 7) : à former tous les trois
- **S-G4 extrait** : à former, priorité moyenne à haute. Mesuré avec le binaire corrigé, sur fixture : une locution du
  registre dans `docs/rapports/r.md` fait imprimer par S-G4 la ligne entière (`      | Cette d[…]e v[…]e QXS4 fonde le
  verdict.`). La fuite est latente sur l'arbre réel : S-G4 y était vert au versement de DETTES-B2 (annexe B l.816-817,
  « VERDICT GLOBAL VERT ») et l'est sur ma copie. Mais tout ajout au registre 09 mécanisé, qui est un resserrement licite,
  peut la déclencher d'un coup. Proposition : SHOGEN-SG4-EXTRAIT-INTERDITS-1, voir §5.
- **Liste unique** : à former, priorité moyenne. La liste vit dans `sg5.rs`, dans les briefs (non versionnés) et dans les
  outils hors dépôt. Les énumérations versionnées divergent :
  - six entrées dans `docs/adr-0028/DOSSIER-G7-S2.md` l.15-16 ;
  - les six plus `docs/adr-0028/execution/` dans `docs/adr-0029/AVIS-QUESTIONS-TECHNIQUES-V3.md` l.5 ;
  - les six plus `apres-execution/` dans `docs/G2-lot-DETTES-B2.md` l.310.

  S-G5 lit les trois `.md` de `docs/adr-0028/execution/`, mais aucune ligne S-G5 ne les vise aujourd'hui (compté : 0). Cet item
  rejoint SHOGEN-SG9-CORPUS-1, qui réclame lui aussi une liste d'exclusion.
- **Liens symboliques** : à former, priorité basse. Mesuré sur fixture avec le binaire corrigé : `docs/lien-dossier ->
  pocket-report` et `docs/lien-fichier.md -> adr-0025/x.md` font imprimer par S-G5 trois textes interdits, sous des chemins non
  interdits. Cause : `roles.rs::parcourir` suit les liens (`is_dir()`). Aucun lien n'est versionné aujourd'hui (mode 120000 :
  0).

### 3.8 L'écart E-7, noms fixes (contrôle 8)
Je n'ai pas eu le texte de E-7. Je le lis comme : les nouveaux tests suivent la convention des noms fixes sous `temp_dir()`
(SHOGEN-XTASK-TMP-NOMS-FIXES-1, annexe B l.832).

Le déclencheur de cet item, « prochain lot qui touche `xtask/tests` », est **atteint** par ce lot. **Avis : ne pas le traiter
ici.**
- Le G0 borne le lot à S-G5.
- R-25 demande des PR petites et unitaires.
- Le budget est de 198 sur 200 après C-1 à C-3.
- Un vrai remède (noms uniques) demande un nettoyage des arbres en fin de test [inféré] : c'est un lot à part.

Les trois tests ajoutent trois noms de la même forme (`shogen-mutant-doc-sg5-interdits-*`), sans créer de classe nouvelle.
**Action due par l'orchestrateur** : consigner en annexe B que le déclencheur a été atteint par SG5-INTERDITS et reporté, avec
un nouveau déclencheur (par exemple : lot dédié, avant le prochain lot qui ajoute des tests à `xtask/tests`). La consigne
« `TMPDIR` dédié par copie » reste en vigueur.

## 4. Observations (hors corrections)

- **O-1** : le rapport rédigé du worker (lectures avec niveau, §3, écarts E-n) ne figure pas parmi les pièces reçues ; seuls
  le journal de commandes et les outils y sont. La G1 versée doit le porter.
- **O-2** : le G0 de vague exige « un G0 de lot … avant tout code (périmètre exact, tests attendus, sortie) ». Pour ce lot, le
  brief du worker en tient lieu, mais il n'est pas versionné : à verser ou à citer au commit.
- **O-3** : l'outil du worker `outils/controle_sortie_verify.py` cherche les préfixes sans ancrage. Il compte comme fuite
  `s2-harness/docs/rapports/ok.md:3 — « … »` (faux positif, dans le sens prudent). Il ne voit pas non plus les fuites par lien
  symbolique. Sans effet sur ses mesures : ses arbres de contrôle 07 ne contiennent pas ce cas. À ancrer s'il est réutilisé
  sur l'arbre réel.
- **O-4** : le compte des écartés diffère (6669 chez le worker, 6694 chez moi). C'est réconcilié : 6669 sur sa base
  `75bf258`, 6694 sur son rejeu à `2c2fbe9`, égal au mien. Le commit CALIB a ajouté des citations.
- **O-5** : la sortie S-G5 garde le nom des fichiers interdits (`chemin:ligne`), comme l'autorise l'item.
- **O-6, incident de ma procédure** : ma première passe « vert après » partageait une cible cargo avec la copie « rouge ».
  Cargo n'a rien recompilé (« Finished in 0.01s ») et a rejoué les tests de l'autre copie (deux échecs fantômes). Ce passage
  est invalide et non compté (`journal/03-INVALIDE-…`) ; tout a été refait avec une cible par copie. Cause probable [inféré] :
  cargo identifie les membres du workspace indépendamment de leur emplacement et juge la fraîcheur à la date des fichiers, or
  `git archive` pose la date du commit. Les journaux du worker montrent une recompilation à chaque passage (non affecté).
  Item I-4 au §5.
- **O-7** : l'ancien dossier `g2/cible` (cible partagée) reste en place. Sa suppression (`rm -rf`) a été refusée par un
  contrôle de sécurité de l'outil ; je ne l'ai pas contournée. Le dossier est sans effet ; à supprimer par l'orchestrateur ou
  par l'utilisateur s'il le souhaite.

## 5. Items à former (règle PAROXYSME)

| item proposé | constat | déclencheur | prix [inféré] |
|---|---|---|---|
| SHOGEN-SG4-EXTRAIT-INTERDITS-1 | S-G4 imprime en extrait la ligne entière d'un fichier interdit qui porte une locution du registre (mesuré sur fixture, binaire corrigé) ; latent sur l'arbre réel | prochain lot qui touche `sg4.rs` ou `rapport.rs`, et au plus tard avant tout ajout au registre 09 mécanisé | extrait vide pour un chemin sous `crate::sg5::emplacement_interdit` (déjà `pub(crate)`) et un test sur la sortie du binaire comme ceux de ce lot |
| SHOGEN-INTERDITS-LISTE-UNIQUE-1 | liste codée dans `sg5.rs`, recopiée dans les briefs et les outils ; énumérations versionnées divergentes (6 entrées, ou plus `execution/`, ou plus `apres-execution/`) | avec SHOGEN-SG9-CORPUS-1, ou au premier ajout d'un emplacement interdit | une liste versionnée lue par `xtask`, d'où se copient les exclusions des briefs, et un test d'égalité ; décider si `docs/adr-0028/execution/` en fait partie |
| SHOGEN-GATES-LIENS-SYMBOLIQUES-1 | `parcourir` suit les liens : un lien hors liste vers un emplacement interdit fait imprimer son texte par S-G5 (mesuré sur fixture) ; 0 lien versionné | prochain lot qui touche `roles.rs` ou `documents.rs`, ou premier lien versionné | refuser un lien dans le périmètre (incident, refus de conclure), ou tester le préfixe sur le chemin résolu ; refus du mode 120000 par le hook |
| SHOGEN-HARNAIS-CIBLE-PARTAGEE-1 | deux copies `git archive` de la même tête, avec un `CARGO_TARGET_DIR` commun : pas de recompilation, les tests d'une copie tournent sur le code de l'autre (mesuré, O-6) | gabarit des briefs, dès maintenant | une cible par copie, ou une garde de fraîcheur (sha256 du binaire construit) dans les scripts de mutants |
| suivi de SHOGEN-XTASK-TMP-NOMS-FIXES-1 | déclencheur atteint par SG5-INTERDITS, non traité (§3.8) | à redater par l'orchestrateur | inchangé |

## 6. Journal de provenance (G1)

**Lectures** (toutes [lu] ; aucune source [abs] ni [2nd]) :
- les deux briefs ;
- `docs/adr-0029/G0-lots-S2BIS.md` (entier) ;
- `ANNEXE-B-items.md` l.804-835 (dont l.816-817) et la liste des titres B.50-B.55 ;
- `ANNEXE-D-preenregistrement.md` l.32-48 (liste D.2) ;
- dans `xtask/src` : `sg5.rs` (entier, à la tête), `rapport.rs` (entier), `lib.rs` (entier), `roles.rs` l.1-138,
  `documents.rs` l.1-140 et ses messages d'incident, `main.rs` l.1-140, `sg4.rs` l.95-160, `sg6.rs` l.60-143,
  `sg8.rs` l.1-60 ;
- `xtask/tests/mutants.rs` l.1-140, l.380-540, l.636-740 ;
- `xtask/Cargo.toml`, `Cargo.toml` l.1-40, `.cargo/config.toml`, `.gitattributes` l.72 ;
- `JOURNAL.md` l.380-392 ;
- `DOSSIER-G7-S2.md` l.15-16, `G2-lot-DETTES-B2.md` l.310-311, `AVIS-QUESTIONS-TECHNIQUES-V3.md` l.5 (ligne trouvée par
  recherche) ;
- côté worker : les deux diffs, `SHA256SUMS`, ses trois outils (entiers) ; dans son journal, `04-mutants-bilan.txt` (entier),
  les en-têtes et lignes de verdict de ses `verify`, les sections S-G4 et S-G5 de `07-controle-corrige-demo-sg4.txt`, les
  lignes « test result » de ses passages.

Une seule inférence, marquée [inféré] : le mécanisme de cargo de O-6.

**Non ouvert** : `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`,
`docs/adr-0028/monark-m009a/` ; tout `*.jsonl` ; toute pièce de D.2 ; le corps des sorties `verify` (verdicts et comptes
seulement, par script) ; les `.md` de `docs/adr-0028/execution/` (noms seulement). Les recherches dans le dépôt ont porté sur
`git ls-files` privé des dossiers interdits (617 fichiers sur 633). `SHOGEN_S2_CAMPAGNE_CONTROL` n'a jamais été posé (retiré de
l'environnement de chaque commande cargo).

**Commandes et sorties** (outils, rustc et cargo 1.97.1) :

| commande | sortie |
|---|---|
| `sha256sum -c sortie/SHA256SUMS`, depuis `sg5/` | 53 OK |
| `git apply --check --whitespace=error`, deux diffs, sur la tête | code 0 et 0 |
| `git archive 2c2fbe9 \| tar -x` avec les six exclusions | copies `base`, `rouge`, `corrige`, `mutants`, `proto` ; 0 dossier interdit, 0 `*.jsonl` |
| `cargo test --locked -p xtask`, une cible par copie | base 77 + 9 OK ; rouge 78 OK et 2 FAILED (`mutants.rs:799`) ; corrigé 80 + 9 OK |
| `python3 -B -m unittest discover -s tests -t .` (`s2-harness`, copie corrigée) | 405 tests, OK (2 sautés) |
| `python3 -B outils/fixtures_g2.py` | code 0 ; CONFORME dans les deux régimes |
| `cargo --locked xtask verify` (base, puis corrigée), puis `outils/verdicts_verify.py` | code 1 et 1 ; 8 VERT, S-G9 ROUGE (1, en `docs/17:70`) ; S-G5 310/6694/267 |
| `python3 -B outils/mutants_g2.py` (lot livré) | 8 TUÉ, 5 VIVANT, 0 FATAL ; `sg5.rs` restauré (sha conforme) |
| `python3 -B outils/vivants_g2.py` | les 5 vivants changent la sortie S-G5 sur les fixtures |
| `xtask gates` corrigé, sur fixture avec liens et locution S-G4 | fuite S-G4 : 1 ligne ; fuites S-G5 par lien : 3 lignes |
| prototype C-1 et C-2 : fmt, clippy `-D warnings`, tests, `mutants_g2.py` | 0, 0, 0 ; 13 TUÉ |
| décompte des lignes ajoutées | livré 136 + 52 = 188 ; prototype 146 + 52 = 198 |

**Pièces produites** (`…/s2bis/sg5/g2/`) : ce rapport ; `outils/` (`fixtures_g2.py` `cd7f6622…`, `mutants_g2.py`
`e3c233ad…`, `vivants_g2.py` `19811492…`, `verdicts_verify.py` `69d67f06…`) ; `journal/` (bilans 14 `67798b8c…` et 17
`63e31d3d…`, non-équivalence 15 `d01514f4…`, fixtures 12 `a07dcfb1…`, items 16 `86009664…`, verify 13, tests 10) ;
`SHA256SUMS-G2.txt` (54 empreintes, ce rapport non compris). Copies et cibles : `base`, `rouge`, `corrige`, `mutants`, `proto`,
`cible-*`, `tmp-*`, `fixtures`.

> *Retouche de l'orchestrateur au versement (2026-10-04 14:14:11 UTC, `date -u`)* : l.31, la citation d'une chaîne de fixture passe de « » à “ ” (S-G5 : chaîne de test, non détenue au registre) ; l.145, la ligne de fixture recopiée, qui porte une formule interdite par le registre doc 09 (construite exprès pour démontrer la fuite de S-G4), est élidée par « […] » (S-G4) ; aucun autre octet changé.
