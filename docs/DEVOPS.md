# Shōgen — plan DevOps (v0, 2026-07-30)

> Statut : plan, rien n'est encore en place. Le principe directeur est une
> conséquence directe de la thèse du projet : **Shōgen vend de la provenance
> vérifiable ; sa propre chaîne de code doit être attestable au même
> standard**, sous peine d'auto-réfutation. Chaque choix ci-dessous en
> découle.

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
| S-G6 `index-sum` | l'en-tête d'`INDEX.md` en désaccord avec le contenu réel de `biblio/` | un compte d'artefacts déclaré est déjà parti en dérive une fois |
| S-G7 `deps` | version non exacte, licence non listée, advisory non traitée (`cargo-deny`) | R6 transposé |

CI sur **Windows + Linux** dès le début (la leçon plateforme-dans-la-trace),
sur chaque push, mêmes gates en local via `just verify` — une gate qui ne
tourne que quand on y pense ne vaut rien.

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
mainteneur. Modèle et effort conformes à la règle absolue du 2026-07-29
(Opus/Fable, effort max).

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

## Décisions qui vous appartiennent

- Nom/organisation GitHub du dépôt (`shogen` sous votre compte ? une org
  commune aux deux projets ?).
- La date du `git init` (recommandation : maintenant).
- Privé-jusqu'à-S3 vs public immédiat (recommandation argumentée : §1).
