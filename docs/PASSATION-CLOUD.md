# Passation Shōgen → session cloud

Rédigé par l'orchestrateur local (2026-10-02), à la demande de l'investisseur : « il faut que le claude qui
va continuer [...] va savoir exactement où reprendre ». **Lis ce fichier en entier avant tout acte.** Il est
autosuffisant : une session cloud n'a ni le disque `F:` de l'investisseur, ni la mémoire `memstack`, ni la
configuration globale `F:\claude-config`. Tout ce qui t'est nécessaire et transmissible est ici ou dans le dépôt.

---

## 0. En une minute

- **Projet** : Shōgen, campagne **S2**, sortie régie par **ADR-0028** (`docs/adr-0028/`).
- **Où on en est** : la **partie 1 (moteur)** est **finie et fusionnée dans `main`** (commit de fusion
  `eb1b13d`). Suite `s2-harness` : **307 tests, OK (2 sauts)**.
- **Où reprendre** : **la partie 2** (intégration et gardes) : DOCS-S2-b, RENDU-1, RENDU-2. Voir §3.
- **Méthode** : par parties (`docs/METHODE-PARTIES.md`), découpage fixé dans `docs/adr-0028/PARTIES-S2.md`.
- **Journal** : `JOURNAL.md` (racine), une ligne datée par décision ; les décisions de l'investisseur y sont
  citées **mot pour mot**. Lis ses 15 dernières entrées.

---

> **Ajout daté du 2026-10-02 12:52 UTC (session cloud) — état à jour** : **partie 2 FAITE et fusionnée** (commit de fusion `0cc5a92`) sur la branche **`claude/compassionate-noether-szmdyj`**, qui tient lieu de `main` locale (passation + partie 1 + partie 2) tant que KraidleAI/shogen#1 n'est pas fusionnée ; branche de partie `partie-2-rendu` conservée. Suite 376 OK (2 sauts) ; xtask VERT en corpus complet ; Rust 209. **Reprendre à la partie 3** (PAQUET, sceau) après l'accord de l'investisseur ; items dus au G0 du PAQUET : annexe B, blocs B.20 à B.29 (déclencheur « G0 du PAQUET »). Le tableau ci-dessous est l'état du 2026-10-02 matin, gardé tel quel.

> **Ajout daté du 2026-10-02 18:2x UTC (session cloud) — état à jour** : **partie 3 FAITE et fusionnée** (commit de fusion `fdc7252`) sur **`claude/compassionate-noether-szmdyj`** ; branche de partie `partie-3-paquet` conservée. **Paquet de pré-enregistrement SCELLÉ** : `docs/adr-0028/PAQUET-PREREG-S2.md`, sha256 `494d770d…` ; manifeste `docs/adr-0028/sceau/PAQUET.sha256` `680a95fd…` ; jeton FreeTSA `paquet.tsr`, **genTime 2026-10-02T17:44:30Z**, **échéance du délai 2026-10-03T17:44:30Z** (`docs/adr-0028/sceau/README.md`, JOURNAL). **Reprendre à la partie 4** (exécution unique, `docs/11`, cp-2) : rien avant l'échéance ; puis acte distinct de l'investisseur. Données hors dépôt, déposées par l'investisseur sur Drive : fichier de sommes de clôture (id `1bA3bmuUZn0XCljRH7GIE54RjMsRI5q9Q`, sha256 `70910984…`) ; **journaux scellés** dans le dossier Drive `1TwP2Jtc0-_gAYjDOHHpvfh3XxnR6jtR6` (`control.jsonl`, `journal.jsonl`, `raw.jsonl`) — **jamais ouverts avant l'échéance et le go** (D.2 n° 7) ; leurs sha256 sont ceux du bloc machine. Ouvert : MONARK-S2-M009A-EXPOSITION-1 (annexe B.34 : attestation de l'investisseur et balayage des transcriptions du poste local, avant l'exécution) ; items B.35 (FM11-VERIFIABLE-1 et REGLE-EMPREINTE-OUTIL-1 avant le cp-2 ; SCEAU-VERIFY-REQUETE-1 et R1-DOCSTRINGS-1 après l'exécution). **Outils de contrôle non versés** (scratchpad de la session, perdus si le conteneur est repris) : `fm11.py` (`886cc676…`, contrôle FM-1.1 décrit en B.32), `regle_fixtures.py` (empreinte `ea3a2d94…`), `render_fixture.py` (épingles) : à reconstruire depuis leur description si besoin, puis verser (items de B.35). Exposition de l'orchestrateur cloud : annexe D.1 n° 15 et n° 16.

## 1. État exact au moment de la passation

| objet | valeur |
|---|---|
| branche de travail | `main` |
| dernier commit de fusion | `eb1b13d` (partie 1 dans `main`) |
| poussé sur GitHub | **branche `passation-cloud-2026-10-02`** (tout le travail, partie 1 comprise). La `main` de GitHub reste à `afc7756` : sa protection a refusé le push (§7). **Clone cette branche.** |
| branche de partie close | `partie-1-moteur` (fusionnée ; conservée, ne pas supprimer sans accord) |
| suite Python | `cd s2-harness && python -B -m unittest discover -s tests -t .` → `Ran 307 tests … OK (skipped=2)` |
| gates Rust | `cargo --locked xtask verify` → `VERDICT GLOBAL : VERT` |
| hook pre-commit | versionné (`enforcement/hooks/pre-commit`) ; **à installer dans ta session** (§6) |

**Lots d'ADR-0028 commis** (annexe A, `docs/adr-0028/ANNEXE-A-lots.md`, une ligne datée par sous-lot) :
B0, B-SEG-1, B-SEG-2, B, POOLEE, E1, DOCS-S2-a, SIM-NIVEAU, D8a, D8b, D8c, **B-DEP-1, B-DEP-2, CRITERE,
D5-AMEND** (ces quatre = partie 1). Le hook versionné de D8c est installé sur le poste local.

**Règle scellée** (ADR-0028 §1 bis) : SHOGEN-CRITERE-R1-1 = « R1 rejette (s) ⇔ z_s ≥ 2,33 ∧ z_bloc,s ≥ 2,33 »,
z_bloc = plancher d'erreur-type (Künsch 1989, noyau de Bartlett, ℓ = 240), trois valeurs REJETTE / NE REJETTE
PAS / NON ÉVALUABLE. Codée par CRITERE (`r1.regle_critere`). **Ne change ni ℓ, ni le seuil, ni la règle** :
SIM-NIVEAU a mesuré que la règle tient son niveau (`docs/adr-0028/sim-niveau/`).

---

## 2. Le plan restant (fin de S2)

| partie | contenu | état |
|---|---|---|
| 1 — moteur | B-DEP-1, B-DEP-2, CRITERE, D5-AMEND | **FAIT, fusionné** |
| **2 — intégration et gardes** | **DOCS-S2-b, RENDU-1, RENDU-2** | **À FAIRE — reprends ici** |
| 3 — texte scellé | PAQUET (pré-enregistrement), sceau RFC 3161 préparé | à faire après 2 |
| 4 — données | ancre (acte investisseur), 24 h, exécution unique, `docs/11`, clôture S2 | à faire après 3 |

---

## 3. Reprendre : la partie 2, pas à pas

1. **Accord de l'investisseur pour la partie 2** : une seule question, en langage clair, sans technique.
   (Méthode, règle 4 : un accord par partie, pas à chaque push.)
2. **Créer la branche** `partie-2-rendu` depuis `main`.
3. **Pour chaque lot**, un G0 court (fichiers, tests, risques), puis G1 (implémentation, tests d'abord), puis
   commit sur la branche. **Les items à traiter au G0 de RENDU-1** (annexe B) :
   - SHOGEN-DECIMAL-ARRONDI-1 (B.14 ; portée étendue à l'EMD de la règle, B.18) : fixer
     `ctx.rounding = ROUND_HALF_EVEN` dans chaque `localcontext` de `r1.py`, test sous `ROUND_DOWN` ;
   - SHOGEN-RENDU-ZERO-1 (B.17) : forme unique d'un zéro exact au rendu (`_fmt_dec`) ;
   - SHOGEN-PMORE-RESIDU-1 (B.17) : P_more sans annulation (sans effet sur la règle) ;
   - SHOGEN-AXES-ENONCE-1 (B.18) : **construction (b) décidée** — imprimer les axes évaluables ;
   - SHOGEN-SENS-PERTES-2 (B.19) : fenêtres sans marqueur et lectures absentes dans [SENSIBILITÉ] ;
   - **au G0 de DOCS-S2-b** : SHOGEN-GARDE-LIBELLE-1 (B.18) — imprimer le seuil appliqué.
   - DOCS-S2-b : la ligne imprimée `report.py` (SHOGEN-REPORT-FISHER-1) **et le ré-épinglage** des dorés
     `SHA_BASE_*`. L'ancien `lot-b.diff` est **périmé** (les épingles ont changé avec B, POOLEE, B-DEP-2,
     CRITERE, D5-AMEND) : **refais-le**, ne le réapplique pas.
4. **UNE relecture G2** par une instance neuve, sur toute la partie.
5. **UNE revue de partie** par l'orchestrateur (oracles rejoués sur la tête de branche, §6).
6. **Fusion** dans `main` par `git merge --no-ff partie-2-rendu` (jamais de rebase, de push forcé ni de
   réécriture d'historique). **Attention** : la `main` de GitHub refuse aujourd'hui les commits de fusion et
   non signés (§7) ; tant que l'investisseur n'a pas tranché, fusionne en local et pousse sur une branche
   (pas sur `main`). Une fusion sans conflit ne lance pas le hook : rejoue
   `bash enforcement/tests/run-fixtures-hooks.sh` et `bash enforcement/hooks/install-pre-commit.sh --verifier`
   **avant** (item SHOGEN-HOOK-COUVERTURE-1).

**RENDU-1** = le script d'exécution unique, **en refus par défaut** (gardes d'ADR-0028 annexe D.4 b, dont la
garde (6) : aucune exécution sans jeton `.tsr` vérifié ou fichier de go daté de l'investisseur). **RENDU-2** =
l'enregistreur d'oracle `shogen.oracle-record.v1`. Les deux se testent **sur fixtures seulement** (D.4 a).

**Partie 3 (PAQUET)**, items à porter (annexe B) : SHOGEN-CRITERE-PT10-CLAUSE-1 (lecture (a) du pt 10 au texte
scellé), SHOGEN-CRITERE-GARDE-NIVEAU-1, clause C-6 « Mantel-Haenszel » (choix par l'état de `biblio/` au
scellement), lecture de Künsch 1989 et Fisher 1921 (voir §5), rédacteurs **frais** (D.2), contrôle FM-1.1 des
transcriptions. Scripts du sceau prêts : `scripts/sceau/make-tsq.sh` et `verify.sh` (ADR §1 bis.10).

---

## 4. Règles (autosuffisantes ; elles s'appliquent sans exception)

**Méthode par parties** (`docs/METHODE-PARTIES.md` ; section 5 « messagerie » exclue pour Shōgen) :
un chantier = une ADR + 3-4 parties ; une partie = un plan, une relecture G2, une revue ; accord investisseur
une fois par partie ; PR/commits remplis jusqu'au plafond (200 lignes de code par commit, R-25), documents hors
compte ; fusion par commit de fusion quand la « CI » est verte ; **jamais de réécriture d'historique**.

**Git** : seul l'orchestrateur committe (R-19/R-20) ; un worker ne committe jamais. Une branche en retard se met
à jour **par fusion de `main`**, jamais par rebase. Pousse `main` seul, jamais une branche de worktree.

**Vérifier avant d'agir** (règle n° 1 de l'investisseur) : lire la ligne avant de la modifier, **lire
l'horloge (`date -u`) avant d'écrire une date**, recompter avant de reprendre un chiffre, lancer le test avant
de committer. **Lire la ligne d'annexe avant d'écrire un message de commit** (trois erreurs consignées le
2026-09-30/10-01 faute de l'avoir fait).

**Roster** (modèles, toujours épinglés par ID complet, jamais un tier nu `opus`/`fable`) :
orchestrateur et advisors et validateur : `claude-fable-5-1` ; workers (G1, G2, corrections) :
`claude-opus-5-5`, **effort `max` explicite** ; tâches mécaniques à brief complet, re-revues ciblées,
lecteurs/chercheurs : `claude-sonnet-5-5`, effort `high`. **`claude-opus-5` est BANNI.** Jamais haiku.
(La session locale tournait sous `claude-opus-5-5` puis l'attribution `Opus 4.8`/`Opus 5.5` par décision de
l'investisseur : dérogation de session, consignée ; en cloud, suis le roster.)

**Gates G0-G7** (corpus qualité, doc 02) : G0 cadrage/ADR avant tout code ; G1 génération tracée (journal de
provenance) ; G2 revue 100 %, réviseur ≠ générateur ; G3 vérification automatique (oracles non-LLM) ; G7
verdict de l'orchestrateur. Niveaux de preuve **[lu] / [abs] / [2nd]** ; **aucun chiffre de seconde main**.

**Zéro dette** : tout point non résolu à la clôture devient une **demande de procurement formée** (papier
introuvable) ou une **recherche de solutions documentée** (choix/blocage) — jamais un « dû » nu.
**Branchement** : une pièce n'est « built » que si sa sortie est consommée par un chemin servi testé.
**PAROXYSME** : toute limite déclarée (« hors théorie », « non couvert ») déclenche un item de recherche formé ;
**rappelle l'état du registre PAROXYSME à l'investisseur à chaque point d'étape.**

**Pré-enregistrement (à ne jamais casser)** :
- **D.2** (annexe D) : pièces **interdites** aux rédacteurs et validateurs frais du PAQUET (dont ADR-0025 l.14
  et la cartographie l.51, repérées par sha256, **jamais affichées**). Toute commande qui dit « Lis ADR-0025 »
  repère d'abord la l.14 par son sha256 `0fe88f1a…` (D.2 n° 6). Lectures déjà faites : inventaire **D.1**.
- **D.3** : attestations d'exposition.
- **D.4 a** : les lots RENDU/B-DEP/CRITERE/D5-AMEND se testent **sur fixtures seulement** ; la variable
  `SHOGEN_S2_CAMPAGNE_CONTROL` (copie scellée) n'est posée **que par l'orchestrateur**, pour les deux tests
  nommés, jamais par un G1/G2. **Sans elle, les deux tests nommés sautent : c'est l'état normal** (`skipped=2`).
- **D.4 b** : aucune exécution sans l'ancre RFC 3161 vérifiée + 24 h (ou go écrit daté de l'investisseur).

---

## 5. Ce que la session cloud N'A PAS (local seulement) et comment faire

| manque | où il vit (poste local) | conséquence en cloud | quoi faire |
|---|---|---|---|
| **Copie scellée de la campagne** (`control.jsonl`, sha256 `351f51b2…`) | `F:/tmp/shogen-scelle-copie/` | les 2 tests nommés **sautent** (normal) ; **exécution unique impossible** | parties 2 et 3 : rien à faire (fixtures seulement). Partie 4 : **reste locale**, avec l'investisseur |
| **Papiers de la biblio** (`biblio/*.pdf` etc.) | `F:/Shogen/biblio/`, `F:/Shogen/scratch/biblio-a-verser/` | seul `biblio/INDEX.md` est versionné ; S-G5 tourne en « régime partiel » et reste **VERT** | **copie sur le Google Drive de l'investisseur** : voir §5 bis ; jamais dans git |
| **Corpus qualité** (doc 02 gates, doc 03 méthode, doc 06 AgileGates, templates) | `C:\Users\KACIMI\compiliance et ingénierie locielle et architecturale\` | non disponible | §4 en donne l'essentiel ; demande la copie à l'investisseur si un détail manque |
| **Config globale** (CLAUDE.md global, agents `worker`, `lecteur`, `advisor`, `validateur-humain`…) | `F:\claude-config\` | agents globaux absents | utilise `agent(..., {model, effort})` avec les ID du §4 ; agents projet dans `.claude/agents/` |
| **Mémoire `memstack`** | serveur local | absente | ce fichier et `JOURNAL.md` la remplacent |
| **Étude Pocket — copie isolée** | `F:/etudes-locales/pocket-network/` | — | §8 |

---

## 5 bis. La biblio sur Google Drive (décision de l'investisseur, 2026-10-02)

Les papiers ne vont **pas** dans git : le versement dans le dépôt a été refusé (droit d'auteur, §8).
L'investisseur les dépose sur **son Google Drive**, dans un dossier **privé** (ni lien public, ni partage) :

| dossier local (source) | contenu | dossier Drive |
|---|---|---|
| `F:\Shogen\biblio\` | 152 fichiers, ≈ 44 Mo : les 125 artefacts indexés, `INDEX.md`, les extractions texte `*.sidecar` | `Shogen-biblio/biblio/` |
| `F:\Shogen\scratch\biblio-a-verser\` | 56 fichiers, ≈ 54 Mo : papiers reçus, pas encore indexés, dont **Künsch 1989** et **Fisher 1921** (sous-dossier `2026-09-30/`, avec `PROVENANCE-2026-09-30.md`) | `Shogen-biblio/biblio-a-verser/` |

**Lien du dossier Drive** : à demander à l'investisseur au début de la session cloud, puis à inscrire ici par un
commit daté.

> **Ajout daté du 2026-10-02 03:0x UTC (session cloud)** : emplacement réel constaté par le connecteur Google Drive
> (lecture accordée par l'investisseur vers 02:5x UTC) : pas de dossier parent `Shogen-biblio/` ; deux dossiers à la
> racine du Drive, privés, créés le 2026-10-02 02:27 UTC : `biblio` (id `10e0eif32lMlwsc0HP1AZsSd6eHX58zHj`) et
> `biblio-a-verser` (id `1Z3QzHd5JKAqN4NhGoPorhPJJsUTliFiL`) ; Künsch 1989, Fisher 1921 et
> `PROVENANCE-2026-09-30.md` sont dans un sous-dossier de `biblio-a-verser` ; une transcription
> `kunsch1989.ocr.txt` (datée du 2026-09-29) existe dans un autre dossier, provenance à établir au lot de lecture.
> **Conduite corrigée** : la recopie complète (point 2 ci-dessous) est impraticable par le connecteur (chaque
> fichier transite encodé par le contexte de la session ; ≈ 98 Mo) ; la recherche plein texte du Drive cherche des
> mots, pas une phrase exacte : elle ne remplace pas S-G5. Donc : lectures ciblées par le connecteur (parties 2 et
> 3) ; rejeu mécanisé de S-G5 en corpus complet (SHOGEN-ORACLE-PERIMETRE-1 (ii)) sur le poste local, où sont les
> octets, avant l'entrée de la partie 2 dans `main`.
>
> **Ajout daté du 2026-10-02 04:21 UTC (remplace la conduite corrigée ci-dessus)** : recopie complète faite en cloud, sans poste local. Procédé : l'investisseur ouvre le dossier `biblio` du Drive en partage par lien ; la session lit la liste par `https://drive.google.com/embeddedfolderview?id=<id du dossier>` puis télécharge chaque fichier par `https://drive.usercontent.google.com/download?id=<id>&export=download&confirm=t` dans `biblio/` (jamais `INDEX.md` par-dessus celui du dépôt : le comparer) ; contrôles : 152 fichiers, aucun PDF remplacé par une page de connexion, `xtask verify` en corpus complet (S-G6 = 125) ; puis l'investisseur referme le partage. Le conteneur est éphémère : refaire à chaque session neuve qui a besoin du corpus complet.

**Conduite en cloud** :
1. Lire le Drive par le connecteur Google Drive de claude.ai (à autoriser par l'investisseur s'il ne l'est pas).
2. Recopier `Shogen-biblio/biblio/` dans `biblio/` du clone, et `Shogen-biblio/biblio-a-verser/` dans
   `scratch/biblio-a-verser/`. Ces deux chemins sont **ignorés par git** : **ne jamais les committer**.
3. Avec les octets en place, la gate S-G5 passe en régime complet, comme sur le poste local ; vérifier
   `cargo --locked xtask verify` (S-G6 doit compter 125 artefacts).
4. Lectures du PAQUET (Künsch, Fisher) : `pdftotext` d'abord (doc 03 §6) ; Künsch est un scan JSTOR sans
   couche de texte, une OCR est nécessaire. Citations de 25 mots au plus.

---

## 6. Mise en route en cloud (à faire une fois)

```bash
# 1. installer le hook versionné (refuse si core.hooksPath est posé ou depuis un worktree lié)
bash enforcement/hooks/install-pre-commit.sh
bash enforcement/hooks/install-pre-commit.sh --verifier     # doit rendre 0

# 2. oracles locaux = « CI » entre deux fenêtres GitHub
( cd s2-harness && python -B -m unittest discover -s tests -t . )   # 307 OK, skipped=2
cargo --locked xtask verify                                         # VERDICT GLOBAL : VERT
bash enforcement/tests/run-fixtures-hooks.sh                        # hooks : 51 ok
bash enforcement/tests/run-fixtures-model-pinning.sh                # model-pinning : 95 ok
bash enforcement/tests/run-fixtures-secrets.sh                      # secrets : 113 ok
bash enforcement/gate-secrets.sh --tree && bash enforcement/gate-secrets.sh --history
```

Le hook refuse un commit si le lint d'épinglage, la gate des secrets ou l'image du job g5 sont en refus. Une
dette `TODO`/`FIXME` nue est refusée (R-13).

---

## 7. CI GitHub et push (protocole de l'investisseur)

- Dépôt `KraidleAI/shogen` (à renommer `shogen-gouvernance` par l'investisseur ; le renommage n'avait pas pris le
  2026-10-01). Il est **privé**. La carte de l'investisseur est refusée : les Actions ne tournent pas en privé.
- **Protocole** : l'investisseur ouvre une **fenêtre publique** le temps des CI, tu pousses `main`, il referme.
  **Tu ne bascules jamais la visibilité toi-même.** Entre deux fenêtres, les oracles du §6 font foi.
- Pousser sur un dépôt privé ne demande pas de fenêtre (seules les CI en demandent une).
- **Protection de `main` sur GitHub** (lue le 2026-10-02, `gh api …/branches/main/protection`) :
  `required_signatures` (commits signés exigés), `required_linear_history` (**aucun commit de fusion**),
  `enforce_admins`, push forcé interdit. Le push de `main` du 2026-10-02 a été **refusé** (`protected branch
  hook declined`) : les commits ne sont pas signés et la partie 1 a été fusionnée par commits de fusion.
  **Conflit à trancher par l'investisseur** : la méthode (règle 4) impose des commits de fusion, la protection
  les interdit. Ne réécris pas l'historique pour passer (signer après coup ou linéariser = réécriture,
  interdite par la méthode). Le travail est poussé sur la branche non protégée `passation-cloud-2026-10-02`.
  Voies : (A) l'investisseur retire « Require linear history » (et, s'il le veut, « Require signed commits »)
  de `main`, puis `main` reçoit la branche par avance rapide ; (B) l'investisseur garde la protection et la
  méthode change : chaque partie entre dans `main` par une PR fusionnée en « Squash and merge » dans
  l'interface de GitHub (commit signé par GitHub, historique linéaire) ; l'historique détaillé reste sur la
  branche de partie.
- **État constaté le 2026-10-02 02:22 UTC** : l'investisseur a retiré `required_signatures` et `required_linear_history`, mais la règle exige désormais une **PR approuvée par une personne** (`required_approving_review_count: 1`, administrateurs compris). Push direct refusé (« Changes must be made through a pull request »). **PR ouverte : `KraidleAI/shogen#1`** (branche `passation-cloud-2026-10-02` vers `main`, fusionnable, bloquée par l'approbation). L'auteur de la PR ne peut pas l'approuver lui-même. Réglage de sécurité : acte de l'investisseur ; ne contourne jamais l'approbation, et n'approuve pas avec un second compte.
- **Décision de l'investisseur (2026-10-02) : voie (A).** Le retrait de la protection est un réglage de sécurité
  du dépôt : **acte de l'investisseur**, jamais de l'orchestrateur. Vérifie qu'il est fait
  (`gh api repos/KraidleAI/shogen/branches/main/protection`) avant de pousser `main` ; la branche
  `passation-cloud-2026-10-02` entre alors dans `main` par avance rapide.

---

## 8. Décisions et actes en attente de l'investisseur

- **Accord de la partie 2** (§3, étape 1).
- **Protection de `main`** (§7) : voie (A) décidée ; le retrait est un acte de l'investisseur. Tant qu'il n'est
  pas constaté, travaille sur des branches et ne pousse pas `main` sur GitHub.
- **Biblio** : le versement dans le dépôt a été **refusé par le contrôle de permissions** de la session locale
  (droit d'auteur : un manuel Wiley, des articles IMS, dépôt public pendant les fenêtres) ; **non contourné**.
  Décision de l'investisseur ensuite : **copie sur son Google Drive** (§5 bis) ; lien à obtenir de lui.
- **Ancre du sceau** (partie 4) : une commande `curl` vers FreeTSA, acte de l'investisseur.
- **Renommage** du dépôt en `shogen-gouvernance`.
- **Pocket** : réponse reçue le 2026-10-01 (F1/F4 confirmés, sévérité medium, **fenêtre de divulgation
  coordonnée de 90 jours acceptée**, CVE et crédit à coordonner). **Aucune déclaration publique avant la date
  convenue.** Correction due au §5 du rapport (Pocket a mesuré ≈ 1,0× à p = 0,25, déficit confiné sous ~5 % ;
  la conclusion sous-% tient) : à faire, sans réécrire l'historique. Réponse et suivi : copie locale isolée.

**Registre PAROXYSME (rappel)** : procurements P-01 Künsch et P-03 Fisher **reçus** (à lire et verser) ;
P-15 Shostack et SHOGEN-POOLEE-SOURCE-1 (Mantel-Haenszel 1959, Cochran 1954, Agresti 2013) en attente ;
FUZZ reporté après S2 ; aucune limite connue sans item (annexe B, blocs B.1 à B.19).

---

## 9. Où trouver quoi

| sujet | fichier |
|---|---|
| décisions de sortie S2 | `docs/adr-0028/ADR-0028-decisions-sortie-S2.md` (§1 bis = amendement, règle scellée) |
| lots et ordre | `docs/adr-0028/ANNEXE-A-lots.md` |
| items (dettes, PAROXYSME) | `docs/adr-0028/ANNEXE-B-items.md` (blocs B.1 à B.19) |
| pré-enregistrement | `docs/adr-0028/ANNEXE-D-preenregistrement.md` (D.1 à D.5) |
| parties | `docs/adr-0028/PARTIES-S2.md`, `docs/METHODE-PARTIES.md` |
| journaux de lot (G1) | `docs/G1-lot-*.md` |
| registre des décisions | `docs/DECISIONS.md` |
| hypothèses | `docs/08-assumptions.md` ; vocabulaire `docs/09-vocabulaire.md` |
| modèle de menace | `docs/17-modele-de-menace.md` |
| code de l'analyse | `s2-harness/shogen_s2/` (`r1.py` règle et blocs, `r2.py`, `report.py`) |
| simulation de niveau | `scripts/sim/`, `docs/adr-0028/sim-niveau/` |
| sceau | `scripts/sceau/make-tsq.sh`, `verify.sh` |
| gates | `enforcement/`, `xtask/`, `.github/workflows/gates.yml` |
