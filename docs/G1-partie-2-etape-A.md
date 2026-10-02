# Journal G1 — partie 2 de S2, étape A (A1, A2, A3)

**Nature de ce journal** : transcription par l'orchestrateur (2026-10-02) du rapport rendu par le worker
`shogen-worker` (Gate 0 déclarée : `claude-opus-5-5`), travail du 2026-10-02 03:15 à 03:56 UTC. Le worker n'a
pas pu verser lui-même son rapport : la reprise qui le lui demandait a été interrompue par une erreur de l'API
(filtre de sécurité du fournisseur, sans lien avec le contenu technique). Les faits ci-dessous sont ceux du
rapport ; les contrôles de l'orchestrateur sont au §6. Contrat : `docs/adr-0028/G0-partie-2.md` §A.

## 1. Provenance

- Sources lues [lu] : G0 §A ; annexe B l.47, 107, 173, 175, 212, 213, 232, 297, 298, 306, 307, 325 ; annexe A
  l.63 ; `docs/G1-lot-DOCS-S2.md` l.60-95 et 110-130 ; passation et plan de la partie 2 ; annexe D l.30-43 (D.2)
  et l.107-150 (D.4) ; ADR-0028 l.99-111 ; `docs/09-vocabulaire.md` l.20-32 ; `r1.py`, `report.py`,
  `records.py` en entier ; `r2.py` l.305-375 ; `sources.py` l.296-340 ; `collector.py` l.186 et 209 ; tests du
  harnais concernés ; `scripts/sim/sim_niveau_oracle_r1.py` l.1-60. Aucune source [abs] ni [2nd].
- D.2 : ADR-0025 et la cartographie du 2026-09-29 non ouvertes ; deux recherches `grep -rl`/`grep -rn` sur
  `docs/` les ont balayées mécaniquement sans afficher de ligne (sorties : noms de fichiers seulement, ces deux
  pièces absentes des résultats). `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée.
- Oracles indépendants du code (scratchpad de la session, sha256 en préfixe) : `oracle_a1.py` (`775d7339…`,
  fractions et entiers, arrondi au pair à 50 chiffres) ; `render_fixture.py` (`4084c42b…`, méthode de DOCS-S2
  l.79) ; `render_autres.py` (`49078034…`, 11 fixtures) ; `regle_fixtures.py` (`5557fb56…`, règle sur U1-U8, J1,
  J1-ℓ1, J2, J3-ℓ1, J5, J4) ; `mutants_a1.py` (`627e7a28…`), `mutants_a2.py` (`5159da98…`), `mutants_a3.py`
  (`9afa048e…`) ; `faire_diff.py` (`e03caf95…`).

## 2. A1 — `r1.py` (DECIMAL-ARRONDI-1, PMORE-RESIDU-1) : +125 −18, suite 310 OK (2 sauts)

- `ctx.rounding = ROUND_HALF_EVEN` aux 14 `with localcontext()` (EMD de `regle_critere` compris) ;
  `poisson_binomial` : p̂ᵢ en a/b exacts (`as_integer_ratio`), D, N₀, N₁ en entiers, une division `Decimal` par
  valeur (P̂₀, P̂₁ et P̂_more).
- `tests/test_arrondi.py` : 13 sites sous `ROUND_DOWN` ambiant (attendus de l'oracle en fractions) ; règle J2 sous
  `ROUND_DOWN` ; p̂ = (0, 1/28, 0) ⇒ P̂_more == 0, garde 0, queue dégénérée. Avant correction : 15 échecs
  (P_more = `4E-51`, garde 1,12E-49). Mutants : 13/13 tués ; mutant du `localcontext` de `compute_r1` équivalent
  (comparaisons exactes seulement), déclaré ; mutant « 1 − P₀ − P₁ » tué.
- Rendus épinglés inchangés ; rendus non épinglés changés au 50e chiffre ou de forme (0.3750 → 0.375), valeurs
  égales à l'oracle exact dans 8 strates contrôlées (la base s'en écartait au dernier chiffre dans 3).

## 3. A2 — `report.py`, blocs 3 à 6 : +142 −20, suite 315 OK (2 sauts)

- REPORT-FISHER-1 (forme finale de DOCS-S2 l.77, `n_min` dynamique) ; GARDE-LIBELLE-1 (seuil appliqué, trois
  sites) ; BLOC3-RENVOI-TAU-1 ; RENDU-ZERO-1 (`_fmt_dec` rend « 0 ») ; AXES-ENONCE-1 construction (b) ;
  SENS-PLAGES-1 (« n PLAGES D'EXCLUSION INCLUSES » pour n ≥ 2).
- Tests : `test_v_ligne_nmin_suit_le_journal` refait (`content_n_min = 7`) ; `tests/test_rendu_libelles.py`
  neuf ; attendus figés mis à jour (`DEF` de `test_bloc3_bloc6`, préfixe de `test_sensibilite`, constante `AX` de
  `test_critere`). Avant correction : 8 rouges sur 12. Mutants 12/12 tués.
- Épingles : rendus « avant » = épingles en vigueur (`a7f5cbfd…`, `b0b4f3b7…`) ; deux lignes changées par rendu
  (renvoi τ, ligne N_min) ; nouvelles épingles `19865d4f…` et `c1fd5391…`.

## 4. A3 — `report.py`, bloc 1 et [SENSIBILITÉ] : +107 −19, suite 318 OK (2 sauts)

- BLOC1-RUNPARAMS-1 (ligne `run_params_non_porteurs`, 11 clés) ; ASN-STATUT-1 (ventilation par statut dans
  `_retires`, reportée en [SENSIBILITÉ]) ; SENS-PERTES-2 (par plage et par strate : fenêtres de grille sans
  marqueur, lectures absentes des fenêtres à marqueur). Imports `json` et `collections.Counter` (bibliothèque
  standard).
- Tests : attendus ASN de `test_bloc1` mis à jour ; deux tests neufs au bloc 1 ; `TestSensPertes`. Avant
  correction : 7 rouges sur 13. Mutants 8/8 tués. Attendu corrigé par le worker lui-même (`strate_defaut` : 2
  valeurs, démarrages un samedi, `collector.py:186`).
- Épingles : insertions seules ; nouvelles épingles `c4f45f47…` et `d0f785eb…`.

## 5. Écarts au G0, limites, questions (et réponses de l'orchestrateur)

- Écarts : 14 sites (le G0 en comptait 15, import compris) ; P̂₀ et P̂₁ aussi en entiers, entiers des p̂ᵢ publiés
  (API inchangée) ; SENS-PERTES-2 coupé au segment sous segment ; titre SENS-PLAGES-1 portant le nombre ;
  cas redondant `if dz else '0'` retiré (rendu identique) ; constante `AX` de `test_critere` modifiée (énoncé de
  la construction (b), décidée au B.18).
- Limites (items formés à l'annexe B.21) : arrondi ambiant hérité hors de `r1.py` (`lm.py` 3 sites, `r2.py` 10,
  `report.py` 1, `closure.py` 1 ; rendu J2 sous `ROUND_DOWN` : 4 lignes du bloc 4 changent encore) ; autres
  attributs du contexte (Emin : `_median([1E-75, 3E-75])` rend `0E-69` sous Emin −20) ; `axes_evaluables` marque
  « staleness » évaluable si σ de classe est None (sans effet en production) ; réplique SIM-NIVEAU ancrée à
  `f5b8269`, ne suit plus `r1` au 50e chiffre (valeurs de la règle inchangées).
- Réponses : Q1 coupe au segment gardée (assiette déclarée de [SENSIBILITÉ]) ; Q2 accord des lignes de week-end
  au nombre de plages : item SHOGEN-SENS-PLAGES-2 ; Q3 écart 2 et constante `AX` acceptés.

## 6. Contrôles de l'orchestrateur (adjudication, 2026-10-02 ≈ 04:0x UTC)

- Empreintes des diffs = rapport (A1 `d082dff0…`, A2 `5441180f…`, A3 `a6e529f7…`, complet `1176508e…`) ;
  chaîne A1 → A2 → A3 rejouée sur un export de `d295ed2` : suite verte à chaque pas, arbre identique au livré.
- Rendu de la fixture épinglée sur l'arbre d'avant et l'arbre d'après : sha = anciennes et nouvelles épingles ;
  diff textuel lu : seules les lignes des items changent.
- Règle scellée : JSON des sorties de `regle_critere` sur les 16 fixtures identique à l'octet avant et après
  (`ea3a2d94…`).
- Mutants de l'orchestrateur : dernier `ctx.rounding` de `r1.py` retiré ⇒ 1 échec ; N_min codé en dur ⇒
  `test_v_ligne_nmin_suit_le_journal` échoue.
- Commits : `957525a` (A1), `37db486` (A2), `1ed1c29` (A3) ; suite finale 318, OK (2 sauts).
