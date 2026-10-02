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
