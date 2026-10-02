# G0 du lot CORR (partie 4) — corrections avant un nouveau scellement (2026-10-02)

Rattachement : décision de l'investisseur du 2026-10-02 22:1x UTC (JOURNAL : « Corriger et resceller ») ; annexe B.42
(R-B, A-1) et B.43 (R-A, A-1) ; ADR-0028 D2, D.4 b, A-8 (un sceau remplacé avant l'exécution reste cité) ; paquet
scellé du 2026-10-02 (`494d770d…`), §9-§10.

## Objet (liste fermée)

1. **CORR-1 (R-B A-1, SHOGEN-RECALCUL-JSON-COPIE-1)** : le run `recalcul-tiers` doit sérialiser `content["exact_copy_pairs"]`
   (`frozenset` de deux noms de flux) : `_decimal` de `s2-harness/tools/rendu_unique.py` rend, pour un `set` ou un
   `frozenset`, la liste triée de ses éléments. Sérialisation seule : aucune valeur calculée ne change.
2. **CORR-2 (R-A A-1, SHOGEN-PRIX-NON-FINI-1)** : une lecture `ok` dont le prix n'est pas un nombre fini (`NaN`, `sNaN`,
   `Infinity`, sous toute casse ou forme admise par `Decimal`) ne doit plus faire échouer le rendu. Règle retenue par
   l'orchestrateur : **un prix non fini est traité comme un prix absent** (même effet qu'un `price` nul : panne au sens
   de `classify_ecart`, non `ok` au sens du pool D1 et du seuil SHOGEN-FLUX-QUASI-MORT-1), appliquée **en un seul point**,
   à la lecture des lectures (le point commun à R1, L&M, R2 et au rapport, à établir par le worker), avec un
   avertissement nommé du lecteur portant le **compte** de prix non finis par flux (jamais les valeurs), capturé dans
   les sorties comme les autres avertissements (`[AVERTISSEMENT DU LECTEUR]`). Motif : doc 10 §5 et paquet §10.2 ne
   définissent la panne que par l'absence de valeur ; une valeur non finie n'est pas une valeur ; pour tout prix fini,
   rien ne change.

## Contraintes

- Tests d'abord (fiche worker, règle 4) : un test qui échoue avant chaque correction (recalcul-tiers sur une fixture à
  copie exacte ; rendu et recalcul sur une fixture à prix `NaN`), puis vert ; une mutation par test.
- Non-régression obligatoire : JSON de la règle sur les 16 fixtures `ea3a2d94…` (`scripts/controle/regle_fixtures.py`),
  épingles `4e62fbb8…` et `d079dd9d…` (`scripts/controle/render_fixture.py`), suite entière verte ; aucun autre
  changement de valeur.
- R-25 : au plus 200 lignes ajoutées par commit ; R-13 ; aucune dépendance nouvelle.
- Pré-enregistrement : fixtures seulement (D.4 a) ; aucune pièce de D.2 ouverte ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais
  posée ; travail sur une copie, diff livré ; aucune opération git en écriture.

## Suite (orchestrateur)

Relecture G2 par un réviseur neuf ; commit ; nouveau commit d'analyse ; rejeux au gel (oracle (4), S-b) ; nouveau bloc
machine ; paquet révisé (texte inchangé hors bloc et une mention datée du premier sceau et de CORR-2), cp-1 bref d'un
validateur frais ; nouveau scellement, nouveau jeton FreeTSA, délai de 24 h depuis son genTime.

## Extension CORR-3 (ajout daté du 2026-10-02 22:2x UTC ; décision de l'investisseur, verbatim : « ok, continue, clors tout »)

Liste fermée des items de l'annexe B clos dans le même lot, avant le nouveau gel (le code est rouvert par la décision
de resceller ; chacun est sans effet sur les valeurs de la règle) :

| item | annexe B | construction |
|---|---|---|
| SHOGEN-SCEAU-VERIFY-REQUETE-1 | B.35 | test `test_verify_lie_le_jeton_a_la_requete` de la relecture G2 de la partie 3 (`docs/G2-partie-3.md` §6, C-1), tel quel |
| SHOGEN-RENDU-MKDTEMP-1 | B.41 | `mkdtemp` de `produire_tout` dans le `try` ; parent absent : ligne « échec de production », code 1 ; un test |
| SHOGEN-RAW-CHEMIN-1 | B.41 | verdict du run `raw` sans le chemin absolu des journaux (réécrit comme les avertissements du lecteur) ; un test |
| SHOGEN-TESTS-C8-SUITE-1 | B.41 | tests : contrôle de `window_start` et de `harness_ts` (C-8 de la partie 2), `suite` en tête des runs (mutants M29, M30, M24 de R-C) |
| SHOGEN-TESTS-HOTE-DEUX-FLUX-1 | B.42 | tests : hôte à deux flux (R2, k_eff), branche « VRAI, borne supérieure de k_eff < k nominal → éteint » (mutants M03b, M15, M06, M01 de R-B) |
| SHOGEN-TESTS-BORDS-R1-1 | B.43 | tests : staleness `>` contre `>=`, garde §5.4 `<` contre `<=` (mutants de R-A) |
| SHOGEN-R1-DOCSTRINGS-1 | B.32 | docstrings de `r1.block_long_run_variance` (Künsch 1989 versé et lu) et de `r1.regle_critere` (texte normatif : le paquet) |
| commentaires et libellés (C-3, C-5 de R-A ; C-4 de R-B) | B.42, B.43 | commentaires de `records.py` l.10 et l.41-42 ; docstring de `model.py` ; libellés périmés de `report.py` cités par R-B |
| SHOGEN-ASN-DIVERGENCE-ECHEC-1 | B.42 | un relevé `resolve_failed` ou à base muette n'est plus imprimé comme « DIVERGENCE ASN » ; un test ; k_eff et drapeau 2 inchangés |

Hors du lot, par construction : SHOGEN-D3-LIFT-1 (publié au rapport `docs/11`) ; analyses « ajoutées après le
pré-enregistrement » (FLUX-QUASI-MORT-1 sensibilité, -2, FLUX-DEVIANT-1, FLUX-FAIBLE-1, POOL-MIN-1, HOST-DEGRADED-2,
CENSURE-INFO-2, DEP-FENETRES-2, R1-PLUGIN-1, CONTENU-DEP-1, POOLEE-BLOC-1) ; ancre OpenTimestamps (investisseur).
Mêmes contraintes que CORR-1 et CORR-2 (tests d'abord, non-régression `ea3a2d94…`, `4e62fbb8…`, `d079dd9d…` ; un
rendu épinglé qui changerait par l'item ASN est ré-épinglé avec le diff textuel lu, seules les lignes de l'item
changeant) ; sous-lots R-25.
