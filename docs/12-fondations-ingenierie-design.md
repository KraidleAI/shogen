# La passe S2.5 — fondations d'ingénierie (conception) (v0, 2026-08-12)

> Statut : **conception ratifiée**. Le mainteneur a ratifié le 2026-08-12 :
> (1) la règle des modèles (workers `claude-opus-5` épinglé — résout le
> conflit avec la règle projet du 2026-08-05, commit `de59708` ; orchestrateur
> Fable 5 ; effort `high` partout, second amendement du 2026-08-12) ; (2) le
> jalon dédié **S2.5** entre S2 et S3, conception dans ce document ; (3) le
> périmètre en **cinq ADR (0009–0013)**. Toute décision restante est déléguée
> sous la formule du 2026-08-12 — « toutes les autres décisions doivent être
> prises selon une rigueur académique » — même régime que la délégation
> d'ADR-0008 : tranchée sur pièce, jamais par préférence, révision mainteneur
> ouverte. **Les seuils chiffrés remontent en ratification** (§9).
>
> Rien ici n'est proven ni tested. Les identités bibliographiques du §4 sont
> des **candidates** — re-établies sur l'artefact détenu avant toute
> citation ; un DOI/ISBN candidat ne se cite pas. Les seuls énoncés
> d'observation de ce document sont les mesures de résolution du §6.2,
> datées du 2026-08-12, avec leur preuve rejouable.

## 1. Objet et non-objet

**L'objet** : convertir les présupposés d'ingénierie du dépôt — « ce sera du
Rust, avec ces crates et ces gates », épars dans `DEVOPS.md` (qui se déclare
lui-même « plan, rien n'est encore en place ») et implicites dans
ADR-0001/0002/0003 — en **choix instruits et tracés**, chacun adossé à une
source fondatrice détenue dans `biblio/` et lue à la section, comme la
statistique l'a fait avant lui ; puis exercer l'ossature de bout en bout
(tested) par un **walking skeleton** sans logique produit. La passe applique
la règle mainteneur du 2026-08-05 : **aucun code produit avant ces
fondations** — le walking skeleton est le critère d'entrée de S3.

**Les non-objets** :

1. Pas de logique produit : aucune statistique (K&L, L&M, k_eff, partition),
   aucun adapter de transport réel, aucune source réseau. Ce contenu est le
   remplissage de S3/S4, pas de S2.5.
2. `s2-harness/` est hors-champ : jetable (10 §1), il meurt après le rapport
   `11-mesures-pilotes.md` et n'est pas un ancêtre du produit. S2 continue en
   parallèle et n'est pas gaté par S2.5.
3. Pas de publication : le dépôt reste privé (DEVOPS §1) ; rien n'est poussé
   sans instruction explicite du mainteneur.

## 2. Le régime de décision

- **Délégation** : les ADR 0009–0013 sont rédigées au format maison
  (Contexte / Décision / Alternative considérée / La source qui tranche / Ce
  que la décision coûte / Registres touchés), adjugées par l'orchestrateur
  sur sources détenues, statut « acceptée (déléguée — révision mainteneur
  ouverte) » — le patron ADR-0008.
- **Les seuils chiffrés ne sont jamais adjugés seuls** : ils entrent en
  *candidats* (avec leur source et leur alternative), sont appliqués à titre
  provisoire par les gates dès le squelette (fail-closed : mieux vaut un
  seuil provisoire strict qu'aucun), et **remontent au mainteneur en
  ratification** (§9). Un seuil sans source est un défaut de passe.
- **Write-guard** : l'orchestrateur seul écrit sous `F:\Shogen`. Les workers
  acquièrent et transcrivent (scratchpad) ; la sélection des citations, le
  grep de contrôle et l'enregistrement à l'INDEX se font au bureau de
  l'orchestrateur, dans SA passe (frontière de passe : le rapport d'un
  worker est une piste, jamais une source).

## 3. Les cinq ADR

Chacune : la question, les options à instruire, la source-qui-tranche
candidate (§4), et ce qui remonte en ratification.

### ADR-0009 — Stack et toolchain du produit

- **Question** : le langage du produit (`shogen-core`, `shogen-verifier`,
  adapters) et la politique d'épinglage de la chaîne de compilation. Le
  harnais Python S2 est hors-champ (jetable).
- **Options à instruire** : Rust ; Go ; C/C++ contemporain ; Zig ; OCaml ou
  Haskell (pour le cœur pur). Critères : sûreté mémoire à fondation
  académique, aptitude `no_std`/dépendances minimales du vérificateur
  (ADR-0002/0003), déterminisme, écosystème CBOR/COSE, chaîne
  d'approvisionnement outillée (lockfile, audit).
- **Sources candidates** : RustBelt (POPL 2018) — la preuve de sûreté du
  fragment sûr ; « Safe Systems Programming in Rust » (CACM 2021) ; le
  dossier CISA/NSA 2023 sur les langages à sûreté mémoire (instruit
  l'alternative C/C++).
- **Remonte** : MSRV, edition, cible `no_std` du vérificateur (oui/à terme).

### ADR-0010 — Architecture : cœur pur, coquille impérative

- **Question** : la doctrine de dépendances — un noyau (typage des faits,
  formes canoniques, statistiques à terme) **pur, total, sans I/O, sans
  panique** ; le vérificateur ne dépend que du cœur ; les transports et
  typeurs sont des adapters au sens d'ADR-0001. Ratifie et fonde le §2 de
  DEVOPS.md et les gates S-G1/S-G2/S-G3.
- **Options à instruire** : décomposition par information hiding (Parnas)
  vs couches classiques vs monolithe modulaire ; totalité/fail-closed par
  contrats (Meyer) vs conventions.
- **Sources candidates** : Parnas 1972 (le critère de décomposition) ;
  Saltzer & Schroeder 1975 (*fail-safe defaults*, *least privilege* — la
  racine du fail-closed S-G3 et du moindre privilège de la CI) ; Meyer 1992
  (Design by Contract — l'article ; le livre OOSC2 en procurement).
- **Remonte** : rien de chiffré — les invariants deviennent des gates
  (direction de dépendance, zéro panique), pas des seuils.

### ADR-0011 — Stratégie de test et seuils (la pyramide)

- **Question** : la forme de la suite (pyramide unit/intégration/e2e),
  property-based sur le cœur pur, test de mutation comme validateur de la
  suite, couverture comme signal-candidat.
- **Options à instruire** : pyramide (Cohn) vs « testing trophy » (Dodds —
  l'alternative industrielle) ; example-based seul vs property-based
  (Claessen & Hughes) ; couverture-cible vs couverture-candidat — la
  littérature mesure que la couverture ne prédit pas fortement l'efficacité
  d'une suite (Inozemtseva & Holmes, à re-établir sur l'artefact) quand le
  score de mutation mesure, lui, la capacité de détection (DeMillo et al. ;
  Jia & Harman). Le « mutant semé » de la doctrine gatewright
  (`shogen-devops` §2) reçoit ici sa fondation académique.
- **Remonte** : plancher de couverture par rôle (cœur/vérificateur au-dessus
  des adapters), plancher de score de mutation sur le cœur pur — les deux en
  candidats sourcés.

### ADR-0012 — Politique d'environnement

- **Question** (le point nommé par le mainteneur au lancement) : **versions
  épinglées par lockfile committé**, toolchain épinglée
  (`rust-toolchain.toml` si 0009 retient Rust), politique de dépendances
  (`cargo-deny` : licences, advisories, sources), et cible de
  reproductibilité du binaire vérificateur. Ratifie et fonde le §4 de
  DEVOPS.md.
- **Options à instruire** : épinglage exact en manifeste vs plages semver +
  lockfile (le lockfile épingle transitoirement — qui fait foi et quand) ;
  vendoring vs registre ; reproductibilité bit-à-bit vs provenance attestée
  (les niveaux SLSA instruisent ce spectre).
- **Sources candidates** : Lamb & Zacchiroli 2022 (builds reproductibles) ;
  in-toto (USENIX Sec. 2019) ; Sigstore (CCS 2022) ; spec SLSA v1.0 (copies
  datées).
- **Remonte** : la politique d'épinglage retenue ; la cible de
  reproductibilité du vérificateur (bit-à-bit : oui/à terme, sur quelle
  plateforme d'abord).

### ADR-0013 — DevOps : gates et flux en doctrine ratifiée

- **Question** : élever DEVOPS.md §3/§5 au rang de décision fondée — les
  gates S-G1…S-G7 (sélection par rôle à chemins exacts, ligne de couverture
  avant verdict, mutant semé tué avant tout vert, l'évasion devient test),
  trunk-based avec `main` protégée, CI Windows+Linux sur chaque push,
  commits signés, actions épinglées par SHA, JOURNAL.md par unité de
  travail.
- **Options à instruire** : trunk-based vs git-flow ; gates bloquantes vs
  advisory (la doctrine du corpus doc 02 tranche : bloquantes,
  non-discrétionnaires — R-22).
- **Sources candidates** : Humble & Farley 2010 (le pipeline — procurement) ;
  Forsgren, Humble & Kim 2018, *Accelerate* (la base empirique DORA —
  procurement) ; l'anti-métrique du corpus (la vitesse de revue ne se
  maximise pas, DORA 2024).
- **Remonte** : rien de chiffré en propre (les seuils vivent en 0011/0012) ;
  la ratification des ADR emporte celle des gates.

**Couture** (rien n'est rouvert) : ADR-0002 (CBOR/COSE, `no_std` à terme) et
ADR-0003 (recalculable offline) **bornent** 0009/0010/0012 ; la séparation
des rôles de DEVOPS §2 est *la doctrine de 0010*, les gates de DEVOPS §3
sont *l'exécution de 0011/0013*.

## 4. Le corpus

### 4.1 Rang A — récupérables (phase A, en cours)

17 cibles, 4 packs, un worker par pack. Identités **candidates** — chaque
artefact est contrôlé par l'orchestrateur (page de titre ouverte, hash
recalculé) avant d'entrer dans `biblio/` et à l'INDEX ; les pages web
mutables entrent en copies datées (précédent : `tlsnotary-faq.html`).

| cle | identité candidate | ADR |
|---|---|---|
| rustbelt | Jung, Jourdan, Krebbers, Dreyer, « RustBelt… », PACMPL 2(POPL) 2018, DOI cand. 10.1145/3158154 | 0009 |
| safe-rust-cacm | Jung et al., « Safe Systems Programming in Rust », CACM 64(4) 2021, DOI cand. 10.1145/3418295 | 0009 |
| cisa-memory-safe | CISA/NSA/FBI et al., « The Case for Memory Safe Roadmaps », déc. 2023 | 0009 |
| parnas | Parnas, « On the Criteria… », CACM 15(12) 1972, DOI cand. 10.1145/361598.361623 | 0010 |
| saltzer-schroeder | Saltzer & Schroeder, « The Protection of Information… », Proc. IEEE 63(9) 1975, DOI cand. 10.1109/PROC.1975.9939 | 0010, 0012 |
| meyer-dbc | Meyer, « Applying "Design by Contract" », IEEE Computer 25(10) 1992, DOI cand. 10.1109/2.161279 | 0010 |
| cockburn-ws | Cockburn, page « Walking Skeleton » (mutable, copie datée) | §5 |
| quickcheck | Claessen & Hughes, « QuickCheck… », ICFP 2000, DOI cand. 10.1145/351240.351266 | 0011 |
| demillo | DeMillo, Lipton, Sayward, « Hints on Test Data Selection », IEEE Computer 11(4) 1978, DOI cand. 10.1109/C-M.1978.218136 — paywall probable | 0011 |
| jia-harman | Jia & Harman, « An Analysis and Survey… Mutation Testing », IEEE TSE 37(5) 2011, DOI cand. 10.1109/TSE.2010.62 | 0011 |
| inozemtseva | Inozemtseva & Holmes, « Coverage Is Not Strongly Correlated… », ICSE 2014, DOI cand. 10.1145/2568225.2568271 | 0011 |
| vocke | Vocke, « The Practical Test Pyramid », martinfowler.com 2018 (mutable, copie datée) | 0011 |
| dodds | Dodds, « The Testing Trophy… » (mutable, copie datée — l'alternative à instruire) | 0011 |
| lamb-zacchiroli | Lamb & Zacchiroli, « Reproducible Builds… », IEEE Software 39(2) 2022, arXiv cand. 2104.06020 | 0012 |
| intoto | Torres-Arias et al., « in-toto… », USENIX Security 2019 | 0012 |
| sigstore | Newman, Meyers, Torres-Arias, « Sigstore… », CCS 2022, DOI cand. 10.1145/3548606.3560596 | 0012 |
| slsa | Spec SLSA v1.0, page des niveaux (mutable, copies datées) | 0012, 0013 |

### 4.2 Rang B — ouvrages en procurement (le mainteneur procure)

Aucun n'est attendu en accès ouvert légitime ; les demandes **formées**
(identité complète, ISBN re-établi, tentatives d'acquisition constatées par
la phase A, usage prévu) sont déposées dans `WISHLIST.md` — le canal établi
depuis S0 — **à la clôture de la phase A**, jamais en « dû » nu.

| ouvrage | ISBN candidat | usage |
|---|---|---|
| Cohn, *Succeeding with Agile*, 2009 | 978-0321579362 | origine de la pyramide (0011) |
| Meyer, *Object-Oriented Software Construction* 2e, 1997 | 978-0136291558 | Design by Contract, totalité (0010) |
| Humble & Farley, *Continuous Delivery*, 2010 | 978-0321601919 | le pipeline (0013) |
| Forsgren, Humble, Kim, *Accelerate*, 2018 | 978-1942788331 | base empirique DORA (0013) |
| Cockburn, *Crystal Clear*, 2004 | 978-0201699470 | définition du walking skeleton (§5) |
| Freeman & Pryce, *Growing Object-Oriented Software, Guided by Tests*, 2009 | 978-0321503626 | walking skeleton opérationnalisé (§5) |

*Sweep du 2026-08-12 (run `wf_e63a0e8d-7e7`)* : **5 demandes formées
déposées** (WISHLIST §Priorité 3 — ISBN constatés sur fiche éditeur,
tentatives documentées ; Crystal Clear : papier épuisé, préférer l'eBook) ;
**OOSC2 réglé sans procurement** — texte intégral légal sur le site de
l'auteur avec permission Pearson, restriction de redistribution constatée
(pas de copie dans `biblio/`, citation par chapitre/page depuis l'URL —
WISHLIST §Réglé).

## 5. Le walking skeleton

Définition de travail (Cockburn — copie datée à détenir en phase A ;
opérationnalisée par Freeman & Pryce, en procurement) : la tranche de bout
en bout **la plus fine qui exerce l'architecture réelle et toute la chaîne
d'automatisation**, avant toute logique métier.

**Contenu exact pour Shōgen** : un témoignage **trivial** (données factices,
aucun transport réel) → sérialisé en CBOR canonique (ADR-0002) → **contrôlé
offline par un binaire séparé** (`shogen-verifier`) qui nomme un résidu et
échoue **fail-closed** sur un octet muté — en traversant les vraies crates
(cœur pur ↔ vérificateur, arête de dépendance dans le bon sens), les vraies
gates (S-G1/2/3, fmt, lints, tests, couverture, mutant semé tué), la vraie
CI (Windows ET Linux), la vraie chaîne d'approvisionnement (commit signé,
actions épinglées SHA, lockfile, audit de dépendances).

**Exclusions** : aucune statistique, aucun adapter réel, aucun réseau.

**Ce que le vert dit** : l'ossature est *tested* (avec compte d'exécutions
CI) — architecture, gates et provenance tiennent ensemble. Il ne dit rien
du produit, et le squelette ne devient jamais une excuse pour commencer S3
avant ratification des seuils.

## 6. Orchestration de la passe

### 6.1 Les phases

- **A — corpus** *(rang A fait le 2026-08-12)* : workflow
  `fondations-corpus-fetch` (run `wf_65513c15-e37`) — contrôle de
  résolution en tête (gate : aucun fetch si le modèle servi n'est pas
  conforme), puis 4 packs parallèles. Les workers téléchargent au
  scratchpad et transcrivent ; **rien n'entre dans `biblio/` sans contrôle
  de l'orchestrateur** (page de titre ouverte, hash recalculé, identité
  re-établie). Exécution : 3 rapports rendus ; le worker du pack
  architecture est mort au rendu (filtre de contenu sur sa sortie), ses
  fichiers ont été contrôlés directement, et la provenance de
  `parnas`/`meyer` re-établie par re-téléchargement à octets identiques.
  21 artefacts versés et enregistrés (INDEX, section S2.5) — dont SLSA
  v1.2 courante, fetch orchestrateur (la v1.0 du manifeste est « Retired »
  sur pièce). Reste de phase : les demandes de procurement rang B
  (§4.2), formées sur tentatives constatées.
- **B — ADR** *(faite le 2026-08-12)* : un worker par ADR (run
  `wf_e704a674-9da`, 5/5 drafts rendus) ; adjudication orchestrateur pièce
  à pièce — chaque citation re-établie au fichier détenu avant écriture
  (pages PDF relues par l'orchestrateur, HTML re-greppés, corpus doc 02 lu
  en entier) ; ADR-0009 à 0013 acceptées (déléguées — révision mainteneur
  ouverte) et apposées à DECISIONS.md par l'orchestrateur seul, seuils
  candidats inlinés. Corrections d'adjudication : citation tronquée
  complétée (0009), fausse citation corrigée (0013), mesure de toolchain
  re-exécutée (0009), ligne ADR-0008 manquante à la table réparée.
- **C — squelette** *(faite le 2026-08-12, adjugée verte sur rejeu
  intégral de l'orchestrateur)* : workspace Rust posé (`crates/shogen-core`
  pur/total/sans panique + CBOR canonique manuel zéro dépendance,
  `crates/shogen-verifier` fail-closed à résidu nommé, `xtask/`), gates
  S-G1/S-G2/S-G3/S-G7a avec 13 mutants + 1 témoin committés, 41 tests,
  couverture cœur 92,23 % (re-mesurée orchestrateur), CI Win+Linux écrite
  aux actions épinglées SHA (non poussée), R-8 documenté par outil. Fait
  de conception consigné : sur 87 octets du lot d'exemple, 50 mutations
  sont refusées fail-closed et 37 (la charge utile exacte) produisent un
  autre lot canonique, accepté à raison — la détection de cette classe
  exige la liaison au hash (ADR-0005), travail S3 ; un test assère
  l'égalité des deux ensembles.
- **D — docs** *(faite le 2026-08-12)* : DEVOPS v1 (statut « fondé et
  partiellement en place », ancres ADR par section, état d'instanciation) ;
  09-vocabulaire v2 (+9 interdits d'ingénierie) ; 08-assumptions v2
  (+A(toolchain-soundness), +A(verifier-binary), section « Résidus de
  méthode » : A(coupling-effect), A(gate-adequacy)) ; JOURNAL tenu.
- **E — ratification** : le paquet du §9 remonte au mainteneur.

### 6.2 Modèles — les faits mesurés du 2026-08-12

Règle ratifiée : workers `claude-opus-5` épinglé, orchestrateur Fable 5,
effort high partout. **Contrôle de résolution exécuté deux fois, deux
chemins** :

1. `agent()` de workflow, `model: 'claude-opus-5'` explicite → servi
   `claude-opus-5[1m]` (« Opus 5 (1M context) ») — run `wf_65513c15-e37`,
   verdict initial RESOLUTION_NON_CONFORME, aucun fetch lancé (le gate a
   fait son travail) ; preuve au journal du run.
2. Définition d'agent (`shogen-devops`, frontmatter `model:
   claude-opus-5`) → servi `claude-opus-5[1m]` — agent `a574eca240044dc12`,
   même jour.

**Adjudication** (déléguée, sur ces deux mesures) : l'identifiant exact
n'est pas servable dans ce harness ; la variante servie est le même modèle
Opus 5 en fenêtre 1M — ce n'est ni un tier nu, ni un héritage, ni une
descente de capacité, les trois choses que la règle existe pour empêcher.
La passe poursuit avec `claude-opus-5[1m]` **consigné**, le gate refusant
tout le reste. **Révision mainteneur ouverte** (§9) : si le mainteneur
refuse la variante 1M, les sorties de la passe restent adjugées par
l'orchestrateur pièce par pièce et la règle est resserrée pour la suite.

## 7. Le critère de sortie — binaire, ratifié

*Oui/non* : les cinq ADR 0009–0013 sont acceptées et **leurs seuils
ratifiés par le mainteneur** ; la source-qui-tranche de chacune est détenue
dans `biblio/` et lue à la section (ou une demande de procurement formée est
déposée) ; et le walking skeleton passe **vert toutes les gates applicables
sur Windows ET Linux**, en exerçant l'architecture réelle, avec **zéro
logique produit**. Atteint = S3 peut commencer.

## 8. Décisions de conception prises dans ce document

1. **Nommage S2.5** : index fractionnaire, pour ne pas renuméroter S3–S5,
   cités dans 02/03/04/05/08 et les ADR — le coût d'une renumérotation
   (références cassées en masse) excède le coût esthétique d'une fraction.
2. **Numéro de document : 12** (10 = conception S2 ; 11 = réservé au
   rapport des mesures pilotes, 05 §S2).
3. **JOURNAL.md instancié au lancement** : la règle « une ligne par unité de
   travail » est écrite depuis DEVOPS §5 — l'instancier est une exécution,
   pas une décision nouvelle.
4. **`biblio/` locale non committée** (DEVOPS §1, reconduit) : les nouveaux
   artefacts suivent le même régime — INDEX.md versionné, octets locaux.
5. **Réparation des définitions d'agents** (2026-08-12) : orchestrateur §1
   et §2 réécrits à la règle en vigueur (l'ancien texte prescrivait Opus
   4.8 par omission de champ — l'inverse exact de la règle ratifiée) ;
   parenthèse d'effort de la description corrigée (second amendement du
   jour) ; DEVOPS §6 mis à la règle. `shogen-devops` était déjà réparé.

## 9. Ce qui remonte au mainteneur — **ratifié le 2026-08-12 par délégation**

> **Procès-verbal de ratification (2026-08-12).** Le mainteneur a délégué
> à l'orchestrateur l'ensemble des décisions de cette section, avec une
> exigence : des réponses fondées sur une étude académique rigoureuse
> adéquate au projet. Exercice de la délégation :
> 1. **Les 14 seuils** (0009 : MSRV 1.97, edition 2024, `no_std` à S3,
>    zéro `unsafe` ; 0011 : les 7 seuils de test ; 0012 : épinglage par
>    rôle, bit-à-bit Linux d'abord, 6 variations, Build L2 à S3) sont
>    **ratifiés au statut exact que leurs sources autorisent** : les
>    régimes sont fondés sur artefacts détenus ; les valeurs numériques —
>    que les sources déclarent elles-mêmes non fondées (Inozemtseva &
>    Holmes : une cible fixe ne produit pas une suite efficace ;
>    Claessen & Hughes : « 100 is a rather arbitrary number ») — sont
>    ratifiées comme **budgets déclarés, fail-closed, révisables par ADR
>    seulement**. Les présenter comme fondées serait la surclamation que
>    09-vocabulaire interdit.
> 2. **La révision des cinq ADR** : close par la même délégation — les ADR
>    sont l'étude académique demandée (~176 citations re-établies).
> 3. **La variante `claude-opus-5[1m]`** : confirmée — deux mesures
>    concordantes (§6.2), même modèle, aucun chemin ne sert l'identifiant
>    nu ; le gate de résolution reste en place à chaque passe.
> 4. **La licence** : contractée par **ADR-0014** (dette
>    prudente-délibérée au sens Fowler/G5 du référentiel — le seul cas de
>    report licite —, propriétaire mainteneur, échéance S3, re-serrage
>    mécanique de la gate) ; `cargo deny check licenses` revu **vert** par
>    l'orchestrateur après application.
> 5. **Commit et push : autorisés** par le mainteneur dans le même acte.
>
> Section d'origine conservée ci-dessous pour la trace.

1. **Les seuils** : MSRV/edition/`no_std` (0009) ; planchers de couverture
   par rôle et de score de mutation du cœur (0011) ; politique d'épinglage
   et cible de reproductibilité (0012).
2. **La révision des cinq ADR déléguées** (patron ADR-0008).
3. **La variante de service `claude-opus-5[1m]`** (§6.2) — acceptée sur
   pièce par l'orchestrateur, à confirmer ou refuser.
4. **Les six demandes de procurement** (§4.2), déposées formées dans
   WISHLIST.md à la clôture de la phase A.
5. **Le commit des incréments de passe** — l'orchestrateur propose de
   committer par incrément comme aux passes précédentes ; aucun commit sans
   ton accord.

## 10. Dettes

Règle absolue du 2026-08-05 : aucune dette nue à la clôture — tout
non-résolu est une demande de procurement formée, une recherche documentée,
ou une unité de travail nommée avec propriétaire. **État au 2026-08-12
(phases A-D closes)** — rien de nu ; chaque point a sa voie :

| # | point | voie (propriétaire) |
|---|---|---|
| 1 | ~~Licence des trois crates~~ — **résolu le 2026-08-12 par ADR-0014** (report contracté à S3, gate re-cadrée, `licenses ok` revu vert par l'orchestrateur) | fermé |
| 2 | ~~S-G4/S-G5/S-G6/S-G8 non instanciées~~ — **résolu le 2026-08-12 (ouverture de S3)** : les quatre gates instanciées dans `xtask/` par l'orchestrateur, 8 mutants semés + témoin, verify complet vert ; trois prises réelles le premier jour (site « faits signés » de 02-vision, deux citations infidèles d'ADR corrigées — DEVOPS §3) | fermé |
| 3 | Double-build de reproductibilité (ADR-0012 D6, 6 variations) non écrit | unité dédiée, **orchestrateur + shogen-devops**, après ratification du seuil et de la cible Linux |
| 4 | ~~`cargo deny check advisories` jamais vu tourner localement~~ — **résolu le 2026-08-12** : étape « S-G7 — licences, bans, sources, advisories » verte au run CI `31645277610`, sur les deux plateformes | fermé |
| 5 | Score de mutation de programme (`cargo-mutants`, R-8 fait) et budgets de fuzz (seuil 7) | **S3** — le régime en deux temps d'ADR-0011 le prévoit ; en S2.5 le plancher binaire (mutant de gate tué) est tenu |
| 6 | ~~Walking skeleton vert **sur Linux**~~ — **résolu le 2026-08-12** : run CI `31645277610` vert sur ubuntu-latest ET windows-latest, zéro étape non-verte (toolchain épinglée, lockfile intact, build verrouillé, tests + mutants, gates, walking skeleton bout-en-bout, cargo-deny) | fermé |
| 7 | Documentation Zig (manque nommé, ADR-0009) — l'option ne se rouvre que par acquisition | fetch sur demande mainteneur, sinon reste un rejet « faute de pièce », honnête |
| 8 | Andrews et al. 2006 / Just et al. 2014 (planchers adossés plutôt qu'assumés, ADR-0011 coûts pt 7) | procurement conditionnel — ne devient demande formée que si le mainteneur exige un plancher adossé |

## 11. Clôture de passe — rapport (2026-08-12)

**Le critère de sortie du §7 est atteint**, chaque branche constatée :

1. Les ADR-0009 à 0013 (plus 0014, née de la passe) sont **acceptées et
   ratifiées** (délégation mainteneur du 2026-08-12, procès-verbal §9) ;
   les 14 seuils sont ratifiés au statut exact que leurs sources
   autorisent — régimes fondés, valeurs en budgets déclarés révisables
   par ADR.
2. La source-qui-tranche de chaque ADR est **détenue et lue à la section**
   (INDEX §S2.5, sha256 par entrée) ou couverte par une **demande de
   procurement formée** (WISHLIST §Priorité 3 — Humble & Farley et
   Accelerate, nommés « manques » par ADR-0013 qui ne les cite pas).
3. Le **walking skeleton est vert à travers toutes les gates applicables
   sur Windows ET Linux** : localement (rejeu intégral orchestrateur,
   phases C) puis au run CI `31645277610` du 2026-08-12 — deux jobs,
   zéro étape non-verte, avec zéro logique produit.

**Section dettes (G5)** : le tableau du §10 ne porte aucun dû nu — items
1, 4, 6 fermés ; items 2, 3, 5 assignés avec propriétaire (unités
nommées : gates documentaires S-G4/5/6/8, double-build D6, mutation de
programme et fuzz à S3) ; item 7 en fetch-sur-demande ; item 8 en
procurement conditionnel. Les 5 procurements de la WISHLIST restent à la
main du mainteneur.

**Provenance de la passe** (G1/R-9) : workers `claude-opus-5[1m]`
(résolution contrôlée, §6.2), orchestrateur Fable 5 ; runs
`wf_65513c15-e37` (corpus), `wf_e63a0e8d-7e7` (procurement),
`wf_e704a674-9da` (ADR), worker devops phase C ; chaque sortie de worker
adjugée avant consommation (P6/R-21) ; commits `d7a6709`, `20b3835`,
`91c4524`, `b38022b` (+ clôture), signés, poussés après autorisation
explicite du mainteneur.

**S3 peut commencer** — sur des fondations où chaque choix porte sa
source, ses seuils portent leur statut exact, et l'ossature est *tested*
avec compte, sur deux plateformes.
