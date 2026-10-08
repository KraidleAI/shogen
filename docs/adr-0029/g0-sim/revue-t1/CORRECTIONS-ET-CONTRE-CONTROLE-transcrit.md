# Corrections SB-5c et contre-contrôle — transcription par l'orchestrateur

Rapports rendus par message (le harnais interdit les fichiers de rapport).

## Corrections (worker neuf `claude-opus-5-5`, 2026-10-05 00:47 à 01:12 UTC)
Un diff `SB-5C.diff` (sha256 `8c5d47c6…e66d`) : 116 lignes de code ajoutées, 19 retirées ; plancher 37 → 49. C-1 (`test_garde_chemin_par_defaut`,
`mock.patch.object(commun.os, "environ", …)`), C-2 (`test_schema_controle_au_chargement`), C-3 (`refus_imports` refuse `oracle_r1` et
`oracle_recalc` même présents dans le lot ; `test_frontiere_refuse_les_adaptateurs`), C-4 (a) `test_flux_a_moitie_renseigne`, (b) `graine_flux`
exige composant et indice, `test_flux_exige_composant_et_indice`, C-5 (un cas écrit à la main par mutant : R-02, R-07, R-08, R-12, R-13),
C-6 (dates de `gates.yml` au 2026-10-05), O-1 (quantile sans rang → `CALIB/coherence`), O-2 (clés flottantes refusées). Rouge d'assertion
consigné avant le code (4 FAIL, 0 ERROR) ; vert sous Python 3.10 à 3.13 et trois PYTHONHASHSEED ; identité bit à bit inchangée (16/16,
`89505b96…24b15c`) ; mutants : réviseur 32/34 (R-10, R-11 équivalents), worker 137/137, neufs 6/6, 0 FATAL. Écarts déclarés E-1 à E-10
(dont R-34 reconstruit d'après le texte de la G2 ; huit mutants adaptés au plancher ; gates de balayage non lancées sur le dépôt entier,
secrets sur les fichiers du lot ; barres obliques inverses dans deux commandes, 0 octet 92 dans le lot ; une liste temporaire dans
`/dev/shm` supprimée). Items proposés : I-1 SHOGEN-S2BIS-MUT-HARNAIS-ORDRE-1 (un outil de mutants classé par la commande du job lance les
étapes dans l'ordre du job, runner d'abord) ; I-2 un réviseur verse tous les mutants qu'il cite ; I-3 mutants de second ordre des aides
de test non couverts.

## Contre-contrôle (réviseur de la G2, 2026-10-05 01:13 à 01:18 UTC) : CONFORME
Application sur `f24d97c` + neuf diffs + SB-5C : arbre = 14 empreintes ; 49 tests OK sous 3.10 à 3.13 et quatre PYTHONHASHSEED ; runner 33 ;
ligne du job conforme à Ran = 49. C-1 à C-6 tenues ; O-1, O-2 correctes. Mutants du réviseur rejoués avec son outil corrigé (ordre du job) :
32 tués, R-10 et R-11 équivalents ; R-34 reconstruit : mutation différente octet pour octet, même propriété, tué ; huit adaptés : sens gardé,
tués. Identité bit à bit : 16/16, fichier de sortie identique à celui de la G2. Diff lu en entier : rien d'autre que C-1 à C-6, O-1, O-2 et
trois lignes du README ; l'aide `refus` de `test_calibration` élargie, pas moins stricte.
