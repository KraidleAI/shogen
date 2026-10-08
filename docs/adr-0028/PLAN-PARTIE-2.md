# Partie 2 de S2 — intégration et gardes : plan (préparé le 2026-10-02 ; accord de l'investisseur donné le 2026-10-02, lancement après la cartographie du même jour)

Rattachement : ADR-0028, annexe A (lignes DOCS-S2-b, RENDU-1, RENDU-2), annexe D.4 a et D.4 b, annexe B (items
nommés ci-dessous) ; découpage `docs/adr-0028/PARTIES-S2.md` ; méthode `docs/METHODE-PARTIES.md` ; reprise
`docs/PASSATION-CLOUD.md` §3. Plan court de l'orchestrateur de la session cloud (fichiers, tests, risques).
Accord de l'investisseur (verbatim, 2026-10-02) : « oui, lance la partie 2 », suivi de « avant de lancer quoi que ce
soit, cartographie générale » (`docs/rapports/cartographie-2026-10-02.md`).

## 1. Base et branche

- `partie-2-rendu` part de la tête de `passation-cloud-2026-10-02` (`d73327f`), qui porte la fusion de la partie 1
  (`eb1b13d`) et la passation : c'est la `main` locale de la session précédente. La `main` de GitHub (`afc7756`) ne
  la porte pas tant que KraidleAI/shogen#1 n'est pas fusionnée ; à sa fusion, `partie-2-rendu` se met à jour par
  fusion de `main`, jamais par rebase.

## 2. Ordre des étapes (choix de l'orchestrateur)

L'annexe A fixe DOCS-S2-b avant RENDU ; l'ordre entre RENDU-1 et RENDU-2 est libre. Retenu : rendu d'abord,
enregistreur ensuite, script d'exécution en dernier.

| étape | contenu | fichiers | raison de la place |
|---|---|---|---|
| **A — rendu du rapport** | DOCS-S2-b : SHOGEN-REPORT-FISHER-1 (ligne imprimée, `n_min` dynamique, source de B.6) ; SHOGEN-GARDE-LIBELLE-1 (seuil appliqué imprimé, trois sites) ; et les items de rendu adressés au G0 de RENDU-1 : SHOGEN-RENDU-ZERO-1 (`_fmt_dec`), SHOGEN-AXES-ENONCE-1 (construction (b) décidée), SHOGEN-SENS-PERTES-2, SHOGEN-DECIMAL-ARRONDI-1 (`ROUND_HALF_EVEN` dans chaque `localcontext` de `r1.py`, EMD compris), SHOGEN-PMORE-RESIDU-1 ; ajoutés le 2026-10-02 (cartographie) : SHOGEN-BLOC3-RENVOI-TAU-1, SHOGEN-BLOC1-RUNPARAMS-1, SHOGEN-SENS-PLAGES-1, SHOGEN-ASN-STATUT-1 | `s2-harness/shogen_s2/report.py`, `r1.py`, `tests/test_exclusion.py`, `tests/test_pool_analyse.py`, tests neufs | ces items changent le rendu ; ils passent avant le script, qui fige le rendu. Le `lot-b.diff` ancien est périmé : refait, jamais réappliqué |
| **B — RENDU-2** | SHOGEN-ORACLE-ENREG-1 : enregistreur `shogen.oracle-record.v1` (schéma ratifié A-12 ; champs `paquet.sha256` et `sceau.genTime`) ; SHOGEN-TORN-LINE-UTF8-1 ; SHOGEN-RAW-LECTEUR-1 (décision au G0 : lecteur et oracle `sha256_raw`, ou limite déclarée au bloc 1 avec item PAROXYSME) ; ajoutés le 2026-10-02 : SHOGEN-BLOC6-TS-1, SHOGEN-D5-RECALCUL-TIERS-1, SHOGEN-CENSURE-CAUSES-1 | `s2-harness/tools/` (neuf), `records.py` | l'exécution unique produit l'enregistrement (D.4 b) : l'enregistreur existe avant le script qui le consomme (règle Branchement), sans bouchon |
| **C — RENDU-1** | script d'exécution unique en refus par défaut : gardes (1) à (6) de D.4 b ; EX-E1-1 (sha256 complets des journaux comparés à ceux du paquet scellé, pas au seul fichier de sommes) ; chemin et format du fichier de go fixés au G0 ; ordre des sorties de D.4 b ; ajouté le 2026-10-02 : SHOGEN-HOOK-SUITE-S2-1 (suite `s2-harness` dans le hook ou non, décision au G0) | `s2-harness/tools/` | dernier : il consomme le rendu figé (A) et l'enregistreur (B) |

Avant le G0 de RENDU-1 (ajouté le 2026-10-02, cartographie §3) : SHOGEN-ORACLE-PERIMETRE-1 (i), S-G4 et S-G5 étendues à
`s2-harness/**/*.md` avec leurs mutants de gate (`xtask/`) ; premier commit de la partie : correction datée du statut
d'ADR-0028 (cartographie §4, point 1).

Re-capture des épingles `SHA_BASE_*` : à chaque commit qui change le rendu, par diff textuel du rendu avant et
après (C-6, FM-3.3), jamais en aveugle.

## 3. Tests (D.4 a : fixtures seulement)

- Tests d'abord, valeurs de référence indépendantes du code, échec montré avant correction, une mutation par test.
- RENDU-1 : pour chaque garde, une fixture qui la déclenche donne une sortie différente de 0 et aucune sortie
  écrite, avec son mutant ; le cas nominal sort 0. Fixtures : dépôt git jetable, faux paquet, jeton RFC 3161
  produit par une autorité de test locale (`openssl ts`) ; jamais FreeTSA, jamais de donnée de campagne.
- RENDU-2 : enregistrement produit sur fixture, relu et vérifié (champs, sha, code de sortie) ; fixture de ligne
  finale coupée dans un caractère multi-octets (HS2-03).
- Chaque commit garde la suite `s2-harness` verte (307 au départ, 2 sauts) ; plafond de 200 lignes de code par
  commit (R-25), documents hors compte.

## 4. Circuit

- Par étape : un G0 court (fichiers, tests, risques), puis G1 par un worker `claude-opus-5-5` en effort `max`
  explicite ; commits de l'orchestrateur seul (R-19/R-20), messages écrits après lecture de la ligne d'annexe.
- **Une** relecture G2 par une instance neuve sur toute la partie ; **une** revue de partie par l'orchestrateur,
  oracles du §6 de la passation rejoués sur la tête de branche, dont `run-fixtures-hooks.sh` et
  `install-pre-commit.sh --verifier` avant la fusion (SHOGEN-HOOK-COUVERTURE-1).
- Fusion `--no-ff` en local, poussée sur une branche ; `main` de GitHub seulement après la fusion de
  KraidleAI/shogen#1.

## 5. Risques et limites déclarés (chaque limite reçoit un item formé au G0 de l'étape qui la rencontre)

1. **Tests nommés sur copie scellée** : la copie vit sur le poste local ; en cloud ils sautent (`skipped=2`, état
   normal). Leur rejeu sur la tête de la partie 2 se fait sur le poste local, avant l'exécution unique.
2. **OpenSSL** : 3.0.13 dans la session cloud, 3.5.7 sur l'hôte (D.4 c). Les jetons de fixture sont produits et
   vérifiés par la même version ; la vérification réelle (partie 4) tourne sur l'hôte.
3. **Effort `max` explicite des workers** (roster) : en cloud, il passe par une fiche d'agent projet
   `.claude/agents/shogen-worker.md` (`claude-opus-5-5`, `effort: max`), commise le 2026-10-02 avec la
   cartographie ; elle prend effet au démarrage de la session suivante. Gate 0 (modèle résolu, préfixe `claude-opus-5-5`) au premier worker.
4. **Siège de l'orchestrateur** : le roster le met sous `claude-fable-5-1` ; la session cloud tourne sous
   `claude-opus-5-5` (écart consigné au JOURNAL, comme la dérogation de la session locale).
5. **Connecteur Firecrawl** : en cloud ses outils s'appellent `mcp__Firecrawl__*`, pas l'UUID de CLAUDE.md ; aucune
   recherche web n'est prévue en partie 2.
6. **Biblio** : requise par la partie 2 pour le rejeu en corpus complet de la gate des citations sur tout document
   touché (SHOGEN-ORACLE-PERIMETRE-1 (ii), échéance « immédiat » ; corrigé le 2026-10-02, cartographie §4), et par la
   partie 3 (lectures de Künsch 1989 et Fisher 1921).
