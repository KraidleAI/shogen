# Shōgen — doctrine DevOps (v1, 2026-08-12 ; plan v0 du 2026-07-30)

> Statut : **fondé et partiellement en place**. Ce qui était « plan, rien
> n'est encore en place » (v0) est depuis le 2026-08-12 adossé aux
> ADR-0009 à 0013 (S2.5, DECISIONS.md) et exécuté en phase C pour le
> squelette : workspace, toolchain épinglée, gates S-G1/S-G2/S-G3 + S-G7a
> avec mutants semés tués et committés, walking skeleton, CI écrite
> (non poussée). Le principe directeur est inchangé : **Shōgen vend de la
> provenance vérifiable ; sa propre chaîne de code doit être attestable au
> même standard**, sous peine d'auto-réfutation. Par section : §2 est la
> doctrine d'ADR-0010, §3 exécute ADR-0011/0013, §4 est gouverné par
> ADR-0012. Les citations d'autres documents visant « plan, rien n'est
> encore en place » décrivent l'état v0 à leur date — exact alors.

## 1. Le dépôt

- **Dépôt GitHub dédié `shogen`**, séparé de Kraidle. Les deux projets sont
  souverains (02-vision) ; un monorepo commun coulerait cette souveraineté
  dans l'outillage. Le point d'intégration (le stub `gather`, S4) vit côté
  Kraidle et consomme une interface versionnée, pas un chemin de fichier.
- **Visibilité : privé de S0 à S2, public à S3.** La raison est structurelle,
  pas défensive : l'artefact de confiance du projet est le **vérificateur**
  (« vérifiable offline sans confiance dans Shōgen ») — un vérificateur
  fermé contredit la vision, donc le passage en public est calé sur son
  existence (S3), pas sur un calendrier marketing. Avant S3, le dépôt privé
  protège la fenêtre R-1/S2 (antériorité académique via arXiv, pas via
  GitHub).
  - **Le passage public porte désormais une marque** (ADR-0019 D10,
    2026-08-20) : le nom **Shōgen** est validé et retenu, avec son propre site,
    sa propre plateforme, ses propres réseaux sociaux (D1). Le passage
    privé→public de S3 est donc aussi le lancement d'une marque publique.
    **Diligence PS-10 (non bloquante)** : recherche d'antériorité de marque
    (registres US/UE/FR/JP ; « 証言 » ; homonymes SaaS ; domaines) **avant**
    exposition — le choix est fait, il reste à dégager la marque (leçon
    Vernier/Seilkal).
- **`biblio/` ne va PAS dans le dépôt public.** Les artefacts détenus
  incluent des copies d'articles (IEEE TSE…) dont la redistribution
  publique est une violation de droits. Règle : `biblio/` locale (ou
  sous-module privé), **`biblio/INDEX.md` committé** avec, à terme, le hash
  SHA-256 de chaque artefact — le registre est public, les octets restent
  privés, et le hash rend le registre opposable.
- Historique local dès maintenant : `git init` + premier commit dès
  validation de ce plan — l'historique de commits est la provenance du
  projet lui-même, chaque jour sans lui est de la provenance perdue.

## 2. Structure cible du workspace

```
shogen/
  crates/
    shogen-core/        vocabulaire de faits, formes canoniques, k_eff.
                        AUCUN nom de transport (gate S-G1, analogue R2 Kraidle)
    shogen-verifier/    vérification offline des lots. Dépendances minimales,
                        no unwrap/panic (gate S-G3), build reproductible
    shogen-collector/   le harnais S2 (mesures R1/R2 sur sources réelles)
  adapters/
    transport-tlsn/     un adapter par transport (ADR-0001), testés jamais prouvés
    typer-price/        les typeurs (03-temoignage §3), identifiés et versionnés
  xtask/                les gates CI (voir §3)
  docs/                 la documentation actuelle
  biblio/               NON committée en public (voir §1) ; INDEX.md committé
  corpus/               classes d'attaque du certificat (04 §5), quand elles existent
```

Séparation des rôles dans les crates = la séparation des rôles du projet :
le vérificateur ne dépend jamais d'un adapter de transport (gate S-G2), le
cœur ne nomme aucun transport. La structure EST la doctrine, et les gates
la tiennent.

## 3. Les gates, dès le premier commit (doctrine gatewright héritée)

Chaque gate : sélection par rôle à chemins exacts, ligne de couverture avant
verdict, **mutant semé tué avant de croire le premier vert**, l'évasion
devient un test permanent.

| gate | ce qu'elle casse | pourquoi (leçon source) |
|---|---|---|
| S-G1 `forbidden-symbols` | un nom de transport (`tlsn`, `reclaim`, `tee`, `zkpass`…) dans `shogen-core` ou `shogen-verifier` | ADR-0001 : les transports sont des adapters ; analogue R2 Kraidle |
| S-G2 `verifier-isolation` | une arête de dépendance du vérificateur vers un adapter, ou une dépendance réseau/horloge dans le vérificateur | « offline, sans confiance dans Shōgen » doit être un fait de link-time, pas une intention |
| S-G3 `fail-closed` | `unwrap`/`expect`/`panic!`/arithmétique non vérifiée dans `shogen-verifier` et `shogen-core` | un vérificateur qui panique sur un lot malveillant est un déni qui ne dit pas son nom |
| S-G4 `vocabulary` | mots interdits (`verified`, `garanti`, `quorum de .* sources diverses` sans rangs…) dans `docs/` hors citations marquées | le vocabulaire de 02/04 devient mécanique — un audit humain récent a montré que la liste vit |
| S-G5 `citations` | une citation entre guillemets dans `docs/` introuvable dans les sidecars de `biblio/` | la règle une-citation-un-grep, mécanisée (précédent : G12 Kraidle, avec sa leçon de couverture) |
| S-G4 et S-G5 (ajout daté du 2026-10-02) | périmètre étendu : `docs/**/*.md` et `s2-harness/**/*.md` (lot P0, partie 2 de S2, SHOGEN-ORACLE-PERIMETRE-1 (i) ; ADR-0028 annexe A) ; les deux lignes qui précèdent sont inchangées | README et RUNBOOK du harnais étaient hors oracle (revue G2 de DOCS-S2, C-9) |
| S-G6 `index-sum` | l'en-tête d'`INDEX.md` en désaccord avec le contenu réel de `biblio/` | un compte d'artefacts déclaré est déjà parti en dérive une fois |
| S-G7 `deps` | version non exacte, licence non listée, advisory non traitée (`cargo-deny`) | R6 transposé |
| S-G9 `references` (ajout daté du 2026-10-04) | sur `docs/17-modele-de-menace.md` : référence `chemin:ligne` non résolue, résidu absent du registre 08, item absent de l'annexe B, lot absent de l'annexe A, date non ISO, guillemet droit ou citation entre apostrophes hors du code, citation française introuvable, pièce de D.2, pour-cent, décimal, statistique, adresse (lot DETTES-B2, SHOGEN-E1-XTASK-REFS-1 ; ADR-0028 annexe B.7) | l'oracle hors dépôt `verif_refs.py` du lot E1 : (a) à (f) mécanisés ; (g), (h) non, déclarés en note ; bornes imprimées : MONARK, `biblio/` sans octets, PX, lots MONARK |
| D6 `double-build` (hors numérotation S-Gn : elle ne vit pas dans `verify` — trop coûteuse par exécution ; `cargo xtask double-build`, CI `reproductibilite.yml` bloquante sur la cible ratifiée) | deux builds release de `shogen-verifier` sous 6 variations d'environnement dont les octets divergent | ADR-0012 D6 — la promesse offline tient au rebuild indépendant |
| gate `no_std` (dans `verify`, hors numérotation S-Gn, avec fmt et clippy ; instanciée 2026-08-13, phase C S3) | du `std` dans `shogen-core` ou la bibliothèque de `shogen-verifier` (construction `thumbv7em-none-eabi` rouge) | ADR-0009 pt 6, maintenue telle quelle par ADR-0015 pt 6 — le vérificateur vise les cibles contraintes |
| gate `mutation` (hors numérotation S-Gn : trop coûteuse par exécution ; `cargo xtask mutation`, CI `mutation.yml` — PR `--in-diff` ≤ 10 min, nightly complet ; instanciée 2026-08-13) | score du cœur < 80 %, ou un survivant hors de la ligne de base justifiée `crates/shogen-core/survivants.txt` | ADR-0011 seuil 3 — mesuré 94,2857 % à l'instanciation (417 mutants, 22 survivants tous justifiés) |
| gate `fuzz` (hors numérotation S-Gn ; `cargo xtask fuzz`, CI `fuzz.yml` — 15 min PR, 4 h nightly, corpus `crates/shogen-verifier/fuzz-corpus/` committé ; instanciée 2026-08-13) | une panique du vérificateur sur une suite d'octets | ADR-0011 seuil 7 — harnais en arbre (zéro dépendance) ; couche instrumentée en ratification R-26 |
| gate `fuzz-distillation` (ajout daté du 2026-10-09, lot FUZZ ; hors numérotation S-Gn ; `cargo xtask fuzz-distillation` sur deux cartes `afl-showmap`, CI `fuzz.yml`, job `cargo-afl`) | les graines `dirigee-distillee-*` gagnent moins de 642 arêtes hors du reste du corpus (⌈1074 × 471/789⌉), ou une arête de ce reste manque | 13 §7 dette 3 — le corpus dérivé des campagnes instrumentées, distillé en formes nommées régénérables, garde sa couverture |

CI sur **Windows + Linux** dès le début (la leçon plateforme-dans-la-trace),
sur chaque push, mêmes gates en local via `just verify` — une gate qui ne
tourne que quand on y pense ne vaut rien.

**État d'instanciation (2026-08-12, phase C S2.5, adjugé par
l'orchestrateur — gates vues vertes, mutants vus tués)** :
S-G1, S-G2, S-G3 instanciées dans `xtask/` (+ **S-G7a**, le volet
« version exacte » de S-G7 porté par rôle, ADR-0012 D3), chacune avec
sélection par chemins exacts, ligne de couverture avant verdict, et ses
mutants permanents (`xtask/tests/mutants.rs` — au 2026-08-13 phase C
vague 1 : 28 tests re-mesurés par `grep -c '#[test]'`, soit 24 mutants +
4 témoins ; le 28ᵉ est le mutant S-G3 « seconde racine de compilation »
semé quand la scission no_std a donné deux racines à `shogen-verifier` —
le champ `fichier_racine` de S-G3 est devenu la liste `fichiers_racines`).
Entrée unique : `cargo xtask verify`. Le reste de S-G7 (licences, bans,
sources, advisories) est tenu par `cargo deny --locked check`. **S-G4,
S-G5, S-G6 et S-G8 instanciées le 2026-08-12 (ouverture de S3, unité
orchestrateur — dette 12 §10 item 2 fermée)** : vocabulaire (sous-ensemble
non ambigu du registre 09, citations marquées exclues), citations
(une-citation-un-grep contre INDEX + octets locaux + sidecars `*.sidecar`
générés par `just sidecars` ; en CI sans octets le contrôle partiel se dit
partiel), index (compte d'en-tête + chaque octet versé nommé au registre),
journal (3 cellules, date ISO, ordre chronologique). 10 mutants semés + 3
témoins sur arbre synthétique (`xtask/tests/mutants.rs`), dont les témoins
du régime « corpus partiel » exigés par la revue G2 du 2026-08-13
(verdict : accepter avec corrections — bloquante `.gitignore` et majeures
2-5 toutes fermées le jour même). Premières prises
le jour de l'instanciation : un site « faits signés » survivant de l'audit
S1 (02-vision), deux citations infidèles dans des ADR ratifiées (RustBelt
« type system itself » cité « language itself » ; sigstore « secure but
accessible » inversé en « and » par l'adjudication S2.5) — corrigées en
classe, trace aux sites.

## 4. Chaîne d'approvisionnement — le standard auto-imposé

Le projet qui dit « une attestation est liée à sa source » signe et atteste
sa propre chaîne :

- **Commits signés** (sigstore/gitsign ou clé SSH signée) — obligatoire par
  branch protection, dès le premier commit.
- **Actions GitHub épinglées par SHA de commit**, jamais par tag mutable —
  la version taguée d'une action est une page mutable, exactement ce que
  la forme canonique de témoignage refuse.
- **Provenance de build** : attestations GitHub (SLSA) sur le binaire
  `shogen-verifier` publié ; build reproductible visé pour ce binaire
  (c'est LE binaire qu'un tiers doit pouvoir reconstruire — la promesse
  offline tient à ça).
- **`cargo-deny` + lockfile committé + toolchain épinglée**
  (`rust-toolchain.toml`) ; audit des nouvelles dépendances dans la PR qui
  les introduit, justification à l'appui (R6 Kraidle).
- **Zéro secret dans le dépôt et zéro autorité ambiante en CI** (R4
  transposé) : tokens OIDC éphémères de portée minimale, jamais de PAT
  longue durée ; le job de release est le seul à porter le droit de
  publier, et il ne tourne que sur tag protégé.

## 5. Règles de flux

- **Trunk-based** : `main` protégée — PR obligatoire, gates requises au
  vert, pas de force-push, tags protégés. Revue humaine : au moins le
  mainteneur (c'est un projet solo aujourd'hui ; la protection vaut
  surtout contre l'agent et contre soi-même à 2 h du matin).
- Les commits mécaniques (fmt, renommages) séparés des commits de fond,
  diff relu avant commit (leçon des 1476 lignes CRLF de Kraidle).
- `.gitattributes` dès le premier commit : `* text=auto eol=lf`, les PDFs
  en binaire — la leçon cp1252/CRLF de ce même environnement Windows.
- Une ligne de `JOURNAL.md` par unité de travail, ADR pour tout choix
  structurant — même registre de discipline que la doc actuelle.

## 6. L'agent DevOps (`.claude/agents/shogen-devops.md`)

Défini dans le fichier d'agent à côté de ce plan. Sa charte en trois
lignes : il **propose et outille, ne relâche jamais** — il peut ajouter une
gate, jamais l'affaiblir sans ADR ; il sème le mutant avant de rapporter un
vert ; il ne pousse rien vers GitHub sans instruction explicite du
mainteneur. Modèle et effort conformes à la règle mainteneur en vigueur
(CLAUDE.md global, 2026-08-05, effort amendé le 2026-08-12 — ratifiée pour
Shōgen le 2026-08-12) : workers `claude-opus-5` épinglé, orchestrateur
Fable 5, effort high partout.

## 7. Séquence de mise en place (à valider avant exécution)

1. `git init` local, `.gitattributes`, `.gitignore` (biblio/*.pdf,
   biblio/*.html exclus du futur remote public), premier commit signé.
2. Squelette workspace (crates vides + xtask) — un commit.
3. S-G6 et S-G4 d'abord (elles gardent ce qui existe déjà : les docs et
   l'INDEX), mutants semés, puis S-G1/S-G2/S-G3 quand les crates naissent.
4. Création du dépôt GitHub **privé** + branch protection + push — sur
   votre instruction explicite (compte, nom d'organisation : à vous).
5. CI GitHub Actions (Windows+Linux, gates, cargo-deny), actions épinglées
   SHA.
6. À S3 : passage public + attestations de build sur le vérificateur.

## État d'exécution (2026-07-30)

- `git init` fait, branche `main` ; premier commit **signé et vérifié**
  (clé SSH ed25519 dédiée `~/.ssh/shogen_signing`, config locale au dépôt,
  allowed-signers local en place).
- Dépôt GitHub **privé** créé, poussé, transféré vers le compte `Kraidle`
  (accepté), puis — décision du mainteneur du 2026-07-30 — **transféré
  vers l'organisation `KraidleAI`** (plan Team, owner : `Kraidle`) :
  **`KraidleAI/shogen`**, la forme org recommandée (continuité de
  propriété, gouvernance, deux produits sous une maison). Le remote local
  pointe sur `https://github.com/KraidleAI/shogen.git` ; `gh` est
  authentifié avec le compte `Kraidle` (owner) ; le collaborateur
  résiduel `phoenixgoku00-cell` a été retiré (l'org n'avait pas de siège
  pour lui — seats 1/1). La signature des commits reste vérifiée après
  transfert (clé sur le compte utilisateur `Kraidle`, email noreply
  inchangé — `verified: true` re-contrôlé par l'API sur `dcbb493`).
- ~~Dette : protection de branche~~ — **fermée le 2026-07-30** par le
  transfert vers l'org Team : protection active sur `main` et vérifiée
  par l'API — force-push interdit, suppression interdite, historique
  linéaire requis, admins inclus, **et signatures de commit requises**.
- ~~Action mainteneur : clé de signature~~ — **fait le 2026-07-30** : clé
  `shogen-signing` posée sur le compte Kraidle (via Chrome, autorisation
  explicite du mainteneur), et **identité git du dépôt basculée** sur
  `Kraidle <309500047+Kraidle@users.noreply.github.com>` (GitHub rattache
  la vérification à l'email du commit — l'email personnel appartient à
  l'autre compte, d'où un premier `unknown_key`). Commit fondateur amendé,
  re-signé, re-poussé : **`3d54450`, `verified: true — reason: valid`**
  confirmé par l'API. L'ancien hash `43e7f9f` n'existe plus (forced update
  avant toute autre histoire).

## Décisions qui vous appartiennent

- Nom/organisation GitHub du dépôt (`shogen` sous votre compte ? une org
  commune aux deux projets ?).
- La date du `git init` (recommandation : maintenant).
- Privé-jusqu'à-S3 vs public immédiat (recommandation argumentée : §1).
