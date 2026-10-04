# -*- coding: utf-8 -*-
"""Glossaire du lot DOCS11-EN, fixé avant la traduction (2026-10-04T15:41:28Z, horloge lue par `date -u`).

Rattachement : brief du lot DOCS11-EN (sha256 cfe6c0d5…0e69), points 3, 4, 6 et 7 ; JOURNAL, entrée du 2026-10-04
15:16:03 UTC (lot DOCS11-EN lancé) ; G0 docs/adr-0029/G0-lots-S2BIS.md (ligne DOCS11-PUBLIC) ; annexe B.57 d'ADR-0028.

Source traduite : docs/publication/11-mesures-pilotes-public.md, sha256 c101998b…6561 (retouche E-19 du lot
DOCS11-PUBLIC ; version précédente 4de98654…7688). L'empreinte complète est épinglée plus bas (SOURCE_SHA256).

Ce module ne porte que des données ; le contrôle (controle_en.py) les lit. Toute retouche après la fixation est
déclarée au journal G1 avec son heure et son motif.

Amendement A-1 (2026-10-04, avant toute ligne traduite) : terme « recopié » précisé (copie verbatim des sorties,
citation traduite des documents), parce qu'une citation traduite n'est pas une copie à l'identique.

Amendements A-2 et A-3 (2026-10-04, pendant la traduction, avant toute exécution du contrôle sur elle) :
A-2 : « go exécution » est gardé en français avec glose (G-55), au lieu d'être traduit (ancien C-24), parce que la
source le dit « verbatim » : une traduction contredirait ce mot. A-3 : forme anglaise de P-02 « has the value »
(« vaut ») au lieu de « is », parce que la source porte aussi deux « est FAUX » (l.376, l.972) que « is » rend : le
compte du passage protégé resterait sinon faussé (1 dans la source, 3 dans la traduction).

Amendement A-4 (2026-10-04, après le deuxième contrôle de la traduction) : la note du terme « valider » ne cite plus
le qualificatif d'assurance interdit lui-même ; le registre anglais du contrôle l'y relevait.

Amendement A-5 (2026-10-04T16:48:57Z, après le relevé informatif de l'emploi des termes, explo/termes_survey.py) :
sens « contrôle d'horloge » du terme « écart » ajouté, rendu « offset », comme la source écrit elle-même
« offset médian » (l.1024) ; seule la ligne du glossaire final change, aucune ligne du corps traduit.

Amendement A-6 (2026-10-04T17:45:42Z) : corrections C-1, C-5 et C-6 de la relecture G2 bilingue
(g2/G2-DOCS11-EN.md, sha256 14e1d718…fe6cf), appliquées par g2/appliquer_corrections.py : phrase d'en-tête
adjugée (« the accepted report ») ; gloses G-47 (« guards cleared ») et G-48 (« conformant »).

Amendement A-7 (2026-10-04T17:47:27Z) : nouvelle source française (retouche E-19 : liste des pièces remises sur
demande, sous accord ; contrôle du sceau). Empreinte de la source épinglée (SOURCE_SHA256) ; P-30 suit le nouveau
texte ; P-31 à P-33 ajoutés, pour que le contrôle exige les passages retouchés dans la traduction.

Aucune barre oblique inverse n'est écrite dans ce fichier (SHOGEN-HARNAIS-ECHAPPEMENTS-1).
"""

# --- Source décrite par ce glossaire (amendement A-7) : toute autre source arrête le contrôle -------------------------

SOURCE_SHA256 = "c101998bb0bb9ea7107475f8c42b0f450f835ec6dfadfae8246ff86f15d16561"

# --- En-tête propre à la version anglaise (brief, point 6) ----------------------------------------------------------

ENTETE_BROUILLON = "**Draft — not published.**"
# Phrase du brief, point 6, à un mot près : « the validated report » devient « the accepted report », parce que
# la gate S-G4 (xtask/src/sg4.rs, LOCUTIONS_INTERDITES) refuse « validated » dans la prose de docs/**/*.md (doc 09,
# qualificatif d'assurance). Écart E-2, adjugé par l'orchestrateur le 2026-10-04 (brief de la relecture G2).
ENTETE_PHRASE = ("English translation of the accepted report; numbers, verdicts and sealed labels "
                 "are identical to the original; the sealed package and the original outputs prevail in case of "
                 "discrepancy.")
ENTETE_PHRASE_BRIEF = ("English translation of the validated report; numbers, verdicts and sealed labels are identical "
                       "to the original; the sealed package and the original outputs prevail in case of discrepancy.")
ENTETE_MENTION = "Report only: supporting documents are provided on request, under agreement."
ENTETE_CONVENTIONS = "*Translation conventions.*"

GLOSSAIRE_TITRE = "## Glossary (French → English)"
GLOSSAIRE_A = "### A. Passages kept in French (printed outputs, verdicts and sealed labels)"
GLOSSAIRE_B = "### B. Terms"

# --- Titres (fr → en), dans l'ordre du document --------------------------------------------------------------------

TITRES = [
    ("# Les mesures pilotes S2 — rapport de la campagne (exécution unique du 2026-10-04)",
     "# The S2 pilot measurements — campaign report (single execution of 2026-10-04)"),
    ("## 1. Résumé", "## 1. Summary"),
    ("## Conventions de lecture et lexique", "## Reading conventions and lexicon"),
    ("## 2. Instrument et campagne", "## 2. Instrument and campaign"),
    ("### 2.1 Classe de fait, pool, flux et hôtes", "### 2.1 Fact class, pool, feeds and hosts"),
    ("### 2.2 Pool d'analyse (ADR-0028 D1)", "### 2.2 Analysis pool (ADR-0028 D1)"),
    ("### 2.3 Segment J28 (ADR-0028 D4, D2 pt 6)", "### 2.3 J28 segment (ADR-0028 D4, D2 pt 6)"),
    ("### 2.4 Exclusion D5", "### 2.4 D5 exclusion"),
    ("### 2.5 Strates et n par strate", "### 2.5 Strata and n per stratum"),
    ("### 2.6 Fenêtres sautées", "### 2.6 Skipped windows"),
    ("### 2.7 Hôte de collecte et limites de l'observateur", "### 2.7 Collection host and limitations of the observer"),
    ("## 3. Verdict confirmatoire (J28, règle SHOGEN-CRITERE-R1-1)",
     "## 3. Confirmatory verdict (J28, rule SHOGEN-CRITERE-R1-1)"),
    ("### 3.1 Entrées et valeur par strate (valeurs complètes)", "### 3.1 Inputs and value per stratum (complete values)"),
    ("### 3.2 Énoncés imprimés (pt 8), mot pour mot", "### 3.2 Printed statements (pt 8), word for word"),
    ("### 3.3 « R1 discrimine »", "### 3.3 « R1 discrimine »"),
    ("### 3.4 Famille de Bonferroni et prémisse de la borne (pt 7)",
     "### 3.4 Bonferroni family and premise of the bound (pt 7)"),
    ("### 3.5 Écarts par flux (bloc 3)", "### 3.5 Anomalies per feed (block 3)"),
    ("## 4. Drapeaux et R2 (blocs 5 et 6 du J28)", "## 4. Flags and R2 (blocks 5 and 6 of J28)"),
    ("### 4.1 Tête de certificat (bloc 6), recopiée", "### 4.1 Certificate head (block 6), copied"),
    ("### 4.2 R2 en résumé (bloc 5)", "### 4.2 R2 in summary (block 5)"),
    ("### 4.3 Divergences ASN pour des hôtes hors du pool (SHOGEN-ASN-DIVERGENCE-HORS-POOL-1, annexe B.44)",
     "### 4.3 ASN divergences for hosts outside the pool (SHOGEN-ASN-DIVERGENCE-HORS-POOL-1, annex B.44)"),
    ("### 4.4 Caveats du chemin de lecture (RPC)", "### 4.4 Caveats of the reading path (RPC)"),
    ("## 5. Descriptifs pré-enregistrés (annexe D.5, paquet §11), hors décision",
     "## 5. Pre-registered descriptives (annex D.5, package §11), hors décision"),
    ("### 5.1 τ observé contre τ committé (SHOGEN-TAU-REDERIV-1)",
     "### 5.1 Observed τ against committed τ (SHOGEN-TAU-REDERIV-1)"),
    ("### 5.2 Décomposition de K par lectures `panne_transport` (SHOGEN-HOST-DEGRADED-1)",
     "### 5.2 Decomposition of K by `panne_transport` readings (SHOGEN-HOST-DEGRADED-1)"),
    ("### 5.3 Censure : fenêtres sautées et bornes non extérieures (SHOGEN-CENSURE-INFO-1)",
     "### 5.3 Censoring: skipped windows and non-outer bounds (SHOGEN-CENSURE-INFO-1)"),
    ("### 5.4 Diagnostic de runs de I_t et FIV", "### 5.4 Diagnostic of runs of I_t and FIV"),
    ("## 6. Lift et identité φ de D3 (SHOGEN-D3-LIFT-1, annexe B.42)",
     "## 6. Lift and φ identity of D3 (SHOGEN-D3-LIFT-1, annex B.42)"),
    ("## 7. Sorties hors décision (paquet §10.2 pt 9)", "## 7. Outputs hors décision (package §10.2 pt 9)"),
    ("### 7.1 J14 principal", "### 7.1 Main J14"),
    ("### 7.2 J14 second (sensibilité « seconde coupe »)", "### 7.2 Second J14 (« seconde coupe » sensitivity)"),
    ("### 7.3 Strate poolée (exploratoire, hors famille, hors décision)",
     "### 7.3 Pooled stratum (exploratory, outside the family, hors décision)"),
    ("### 7.4 Sensibilité « plage incluse » (liste fermée, D2 pt 7)",
     "### 7.4 « plage incluse » sensitivity (closed list, D2 pt 7)"),
    ("### 7.5 L&M (bloc 4)", "### 7.5 L&M (block 4)"),
    ("### 7.6 Queues exactes", "### 7.6 Exact tails"),
    ("## 8. Contrôles de l'exécution", "## 8. Checks of the execution"),
    ("### 8.1 Sceau", "### 8.1 Seal"),
    ("### 8.2 Gardes (annexe D.4 b ; paquet §9)", "### 8.2 Guards (annex D.4 b; package §9)"),
    ("### 8.3 Journaux et sorties", "### 8.3 Journals and outputs"),
    ("### 8.4 Enregistrement d'oracle (D6 (viii))", "### 8.4 Oracle record (D6 (viii))"),
    ("### 8.5 Suite `s2-harness`", "### 8.5 `s2-harness` suite"),
    ("### 8.6 Oracle `recompute_*` (run `recalcul-tiers`) : ce qu'il établit et ce qu'il n'établit pas",
     "### 8.6 `recompute_*` oracle (run `recalcul-tiers`): what it establishes and what it does not establish"),
    ("### 8.7 Verdict du journal brut", "### 8.7 Verdict of the raw journal"),
    ("### 8.8 Durée", "### 8.8 Duration"),
    ("### 8.9 Recomptes du rédacteur [calc]", "### 8.9 Recounts by the drafter [calc]"),
    ("## 9. Limites", "## 9. Limitations"),
    ("### 9.1 Limites écrites avec la règle (paquet §10.2, pts 2, 7 et 11)",
     "### 9.1 Limitations written with the rule (package §10.2, pts 2, 7 and 11)"),
    ("### 9.2 Limites et procédures écrites au paquet (§12, points 1 à 20)",
     "### 9.2 Limitations and procedures written in the package (§12, points 1 to 20)"),
    ("### 9.3 Limites constatées d'après l'exécution", "### 9.3 Limitations observed from the execution"),
    ("## 10. Déviations et expositions déclarées", "## 10. Declared deviations and exposures"),
    ("### 10.1 Lecture D.1 n° 16 : exposition de l'orchestrateur de la session cloud",
     "### 10.1 Reading D.1 No. 16: exposure of the orchestrator of the cloud session"),
    ("### 10.2 Fermeture de MONARK-S2-M009A-EXPOSITION-1 (annexe B.38)",
     "### 10.2 Closure of MONARK-S2-M009A-EXPOSITION-1 (annex B.38)"),
    ("### 10.3 Remplacement du premier sceau (A-8 ; lot CORR)",
     "### 10.3 Replacement of the first seal (A-8; CORR work package)"),
    ("### 10.4 Précédence D-4 (SHOGEN-D4-PRECEDENCE-RAPPORT-1, annexe B.45)",
     "### 10.4 Precedence D-4 (SHOGEN-D4-PRECEDENCE-RAPPORT-1, annex B.45)"),
    ("### 10.5 Autres déviations", "### 10.5 Other deviations"),
    ("## 11. Analyses ajoutées après le pré-enregistrement : non faites à la date du rapport",
     "## 11. Analyses added after the pre-registration: not done at the date of the report"),
    ("### 11.1 Ajout daté du 2026-10-04 : analyses faites après le pré-enregistrement (lot POST-PREREG), hors décision",
     "### 11.1 Addition dated 2026-10-04: analyses done after the pre-registration (POST-PREREG work package), "
     "hors décision"),
    ("## 12. Reproduire", "## 12. Reproduce"),
]

# --- Passages gardés en français, avec leur glose à la première occurrence (brief, point 3) -------------------------
# (identifiant, forme exacte telle qu'écrite dans la traduction, glose anglaise, nature)
# Une forme entre « » est une citation gardée à l'identique (espaces normalisées) ; une forme nue est un libellé
# scellé ou une valeur imprimée ; une forme entre accents graves est un code en ligne recopié.

GLOSES = [
    ("G-01", "NE REJETTE PAS", "does not reject", "valeur de la règle (paquet §10.2 pt 5)"),
    ("G-02", "« R1 discrimine » = FAUX", "“R1 discriminates” = false", "verdict de la règle scellée"),
    ("G-03", "« le modèle binomial de doc 10 §5.1, à fenêtres indépendantes, est rejeté ; la cause n'est pas "
             "identifiée entre co-défaillance des sources et dépendance sérielle des fenêtres »",
     "the binomial model of doc 10 §5.1, with independent windows, is rejected; the cause is not identified between "
     "co-failure of the sources and serial dependence of the windows", "énoncé scellé de la discordance, imprimé"),
    ("G-04", "« R1 rejette (s) »", "R1 rejects (s)", "énoncé scellé"),
    ("G-05", "hors décision", "outside the decision", "étiquette scellée (paquet §10.2 pt 9)"),
    ("G-06", "VRAI", "true", "valeur scellée"),
    ("G-07", "« plage incluse »", "range included", "nom de la sensibilité (liste fermée, D2 pt 7)"),
    ("G-08", "[SENSIBILITÉ]", "SENSITIVITY", "nom de section imprimé"),
    ("G-09", "« rendu »", "rendering", "rôle de l'enregistrement d'oracle"),
    ("G-10", "REJETTE", "rejects", "valeur de la règle"),
    ("G-11", "« BTC/USD-stable, devise marquée par flux »", "BTC/USD-stable, currency marked per feed",
     "sortie imprimée"),
    ("G-12", "« pool configuré = 12 flux »", "configured pool = 12 feeds", "sortie imprimée"),
    ("G-13", "« k nominal = 10 (hôtes distincts du pool) »", "nominal k = 10 (distinct hosts of the pool)",
     "sortie imprimée"),
    ("G-14", "« ok = 0 / 24585 lectures, n = 24585 »", "ok = 0 / 24585 readings, n = 24585", "sortie imprimée"),
    ("G-15", "« 10 sources / 11 flux »", "10 sources / 11 feeds", "sortie imprimée (k nominal_s)"),
    ("G-16", "« ok = 0 / 11397 lectures, n = 11397 »", "ok = 0 / 11397 readings, n = 11397", "sortie imprimée"),
    ("G-17", "« fenêtres distinctes (window_close) calme 0, stress 0 ; asn_attribution 0 ; clock_check 0 »",
     "distinct windows (window_close) calm 0, stress 0; asn_attribution 0; clock_check 0", "sortie imprimée"),
    ("G-18", "« causalité non établie »", "causality not established", "sortie imprimée"),
    ("G-19", "« kind=weekend_utc stress = samedi+dimanche UTC »", "kind=weekend_utc stress = Saturday+Sunday UTC",
     "sortie imprimée"),
    ("G-20", "« harnais vivant »", "harness alive", "libellé imprimé"),
    ("G-21", "« le résidu est à son MAXIMUM, publié »", "the residual is at its MAXIMUM, published", "sortie imprimée"),
    ("G-22", "« le z confirmatoire inclut les modes communs de l'observateur (hôte, DNS, réseau) »",
     "the confirmatory z includes the common modes of the observer (host, DNS, network)", "sortie imprimée"),
    ("G-23", "« n'est pas rejeté »", "is not rejected", "énoncé scellé (paquet §10.2 pt 8)"),
    ("G-24", "« aucune strate ne rejette ; strate(s) testée(s) : calme, stress »",
     "no stratum rejects; stratum(s) tested: calm, stress", "sortie imprimée"),
    ("G-25", "« nonÉv »", "not evaluable", "colonne du bloc 3"),
    ("G-26", "(panne / stale / horsE / nonÉv)", "outage / stale / out-of-envelope / not evaluable",
     "colonnes du bloc 3"),
    ("G-27", "« côté livraison »", "delivery side", "sortie imprimée"),
    ("G-28", "« comparaison hétérogène déclarée »", "heterogeneous comparison declared", "sortie imprimée"),
    ("G-29", "« historique insuffisant »", "insufficient history", "libellé du drapeau 1"),
    ("G-30", "« co-défaillance observée non expliquée par les axes R2 »",
     "co-failure observed, not explained by the R2 axes", "libellé du drapeau 2"),
    ("G-31", "ÉTEINT", "off", "état du drapeau 2"),
    ("G-32", "« aucun cluster à ≥ 2 flux (1) → tout reste au φ par paire de flux (bloc 4) »",
     "no cluster with ≥ 2 feeds (1) → everything stays at the φ per pair of feeds (block 4)", "sortie imprimée"),
    ("G-33", "« chemin de LECTURE ≠ amont (§3.2) : l'ASN mesuré est celui du fournisseur RPC "
             "(ethereum-rpc.publicnode.com), une infrastructure de lecture, pas l'amont du feed »",
     "READING path ≠ upstream (§3.2): the measured ASN is that of the RPC provider (ethereum-rpc.publicnode.com), "
     "a reading infrastructure, not the upstream of the feed", "sortie imprimée"),
    ("G-34", "« bornes à P̂_more fixé, non extérieures ; verdict non identifié sous censure arbitraire des fenêtres "
             "sautées »",
     "bounds at fixed P̂_more, non-outer; verdict not identified under arbitrary censoring of the skipped windows",
     "sortie imprimée"),
    ("G-35", "« non extérieures »", "non-outer", "étiquette imprimée"),
    ("G-36", "« run maximal ≥ ℓ : σ̂²_bloc,s biaisé vers le bas ; SHOGEN-DEP-FENETRES-2 prioritaire avant G10 »",
     "maximal run ≥ ℓ: σ̂²_bloc,s biased downward; SHOGEN-DEP-FENETRES-2 a priority before G10",
     "drapeau scellé (pt 9)"),
    ("G-37", "« [inféré : dérivation de l'AVIS-advisor-defi Q1 (iv)] »",
     "[inferred: derivation from the AVIS-advisor-defi Q1 (iv)]", "marque imprimée"),
    ("G-38", "« seconde coupe »", "second cut", "nom de la sensibilité (liste fermée)"),
    ("G-39", "NON ÉVALUABLE : strate non testée, hors décision (§1 bis.1 pt 2)",
     "not evaluable: stratum not tested, outside the decision (§1 bis.1 pt 2)", "valeur de la règle"),
    ("G-40", "« k_eff ≤ 10 (BORNE SUPÉRIEURE) »", "k_eff ≤ 10 (UPPER BOUND)", "sortie imprimée"),
    ("G-41", "« ni levé ni éteint »", "neither raised nor off", "état du drapeau 2"),
    ("G-42", "« aucune strate testée »", "no stratum tested", "sortie imprimée"),
    ("G-43", "« strate poolée hors des entrées »", "pooled stratum outside the inputs", "sortie imprimée"),
    ("G-44", "« variante “exclue” = principale (blocs 1-6) ; variante “incluse” = sensibilité — biaisée vers le haut "
             "par construction ; documente l'exclusion D5 ; pas un estimateur alternatif »",
     "variant ‘excluded’ = main (blocks 1-6); variant ‘included’ = sensitivity — biased upward by construction; "
     "documents the D5 exclusion; not an alternative estimator", "sortie imprimée"),
    ("G-45", "« motif de l'exclusion (harnais dégradé, […]) : causalité non établie »",
     "reason for the exclusion (degraded harness, […]): causality not established", "sortie imprimée"),
    ("G-46", "`sensibilité « plage incluse » de la liste fermée (D2 pt 7), hors décision, biaisée vers le haut par "
             "construction`",
     "“range included” sensitivity of the closed list (D2 pt 7), outside the decision, biased upward by "
     "construction", "étiquette d'entrée imprimée (RT)"),
    ("G-47", "« gardes levées »", "guards cleared", "sortie imprimée"),
    ("G-48", "« conforme »", "conformant", "sortie imprimée"),
    ("G-49", "« vivant »", "alive", "libellé imprimé"),
    ("G-50", "« à son MAXIMUM, publié »", "at its MAXIMUM, published", "sortie imprimée"),
    ("G-51", "« aucun cluster à ≥ 2 flux (1) »", "no cluster with ≥ 2 feeds (1)", "sortie imprimée"),
    ("G-52", "« run_params divergents »", "diverging run_params", "refus imprimé"),
    ("G-53", "« ajoutée après le pré-enregistrement, hors décision »",
     "added after the pre-registration, outside the decision", "étiquette obligatoire (paquet §7, §11)"),
    ("G-54", "« ajoutée après le pré-enregistrement, hors décision ; ne change pas le verdict de la règle scellée "
             "(« R1 discrimine » = FAUX, docs/11 §3) »",
     "added after the pre-registration, outside the decision; does not change the verdict of the sealed rule "
     "(“R1 discriminates” = false, docs/11 §3)", "première ligne imprimée des sorties PP"),
    ("G-55", "« go exécution »", "go execution", "réponse verbatim de l'investisseur (JOURNAL l.310), amendement A-2"),
]

# Expressions régulières de recherche des libellés nus (bornes de mot ; REJETTE hors de NE REJETTE PAS).
LETTRE = "A-Za-zÀ-ÖØ-öø-ÿ_"
REGEX_LIBELLES = {
    "G-01": "(?<![" + LETTRE + "])NE REJETTE PAS(?![" + LETTRE + "])",
    "G-05": "(?<![" + LETTRE + "])hors décision(?![" + LETTRE + "])",
    "G-06": "(?<![" + LETTRE + "])VRAI(?![" + LETTRE + "])",
    "G-10": "(?<![" + LETTRE + "])(?<!NE )REJETTE(?! PAS)(?![" + LETTRE + "])",
    "G-31": "(?<![" + LETTRE + "])ÉTEINT(?![" + LETTRE + "])",
}

# Citations gardées sans glose : contenu sans mot français, ou terme anglais tel qu'imprimé.
NEUTRES = [
    ("fail-open", "terme anglais, imprimé tel quel"),
    ("DUE", "même graphie et même sens en anglais"),
    ("≥", "symbole"),
    ("concordant", "même mot en anglais"),
    ("≤ 2026-09-04T00:00Z", "symbole et date ISO"),
    ("Cov<0 possible", "même graphie et même sens en anglais"),
    ("staleness", "terme anglais du paquet"),
    ("(Fisher)", "nom propre"),
    ("ok", "statut imprimé"),
]

# Citations gardées couvertes par la glose d'une forme composée qui les contient à leur première occurrence.
COUVERTS = [
    ("R1 discrimine", "G-02", "première occurrence dans « R1 discrimine » = FAUX, glosé en bloc"),
]

# Citations d'autres documents du projet, traduites entre “ ” (le texte original fait foi).
# (identifiant, contenu français à espaces normalisées, contenu anglais, document cité)
CITATIONS_TRADUITES = [
    ("C-01", "Reproduire", "Reproduce", "ce rapport, titre du §12"),
    ("C-02", "Ce qui n'est pas public", "What is not public", "ce rapport, §12"),
    ("C-03", "les axes R2 sont-ils observables en pratique, et le test R1 discrimine-t-il quelque chose sur données "
             "réelles ?",
     "are the R2 axes observable in practice, and does the R1 test discriminate anything on real data?", "doc 10 §1"),
    ("C-04", "n fenêtres, K, z du pool, la partition R2 constatée, k_eff vs k nominal ; résultat négatif = résultat",
     "n windows, K, z of the pool, the observed R2 partition, k_eff vs nominal k; negative result = result",
     "doc 10 §7"),
    ("C-05", "Clause datée après J28 : décision de l'investisseur (§4.10 b), sur la règle écrite au paquet "
             "(SHOGEN-CRITERE-R1-1). Si R1 discrimine : lot “benchmark continu” par un G0 neuf (réimplémentation "
             "dans le cœur, ou promotion G0-G7 de la collecte). Sinon, la collecte meurt comme prévu.",
     "Clause dated after J28: decision of the investor (§4.10 b), on the rule written in the package "
     "(SHOGEN-CRITERE-R1-1). If R1 discrimine: ‘continuous benchmark’ work package through a new G0 "
     "(reimplementation in the core, or G0-G7 promotion of the collection). Otherwise, the collection dies as "
     "planned.", "ADR-0028 D6 (vi)"),
    ("C-06", "“R1 discrimine” := VRAI de la règle SHOGEN-CRITERE-R1-1 ; “la collecte meurt” reste une décision de "
             "l'investisseur",
     "‘R1 discrimine’ := VRAI of rule SHOGEN-CRITERE-R1-1; ‘the collection dies’ remains a decision of the investor",
     "ADR-0028 D6 (vi), erratum"),
    ("C-07", "Après J28 : bifurcation = décision de l'investisseur (§4.10 b)",
     "After J28: bifurcation = decision of the investor (§4.10 b)", "ADR-0028 D9"),
    ("C-08", "Si (i) est faux : priorité à G4 et révision de 04 (doc 10 l.35-36 ; 05-roadmap l.126-127).",
     "If (i) is false: priority to G4 and revision of 04 (doc 10 l.35-36; 05-roadmap l.126-127).", "ADR-0028 D9"),
    ("C-09", "FAUX → priorité à G4 et révision de 04, avec les EMD_s",
     "FAUX → priority to G4 and revision of 04, with the EMD_s", "paquet §10.2 pt 11"),
    ("C-10", "“La collecte meurt” reste une décision de l'investisseur (D6 vi), jamais une conséquence mécanique.",
     "‘The collection dies’ remains a decision of the investor (D6 vi), never a mechanical consequence.",
     "paquet §10.2 pt 11"),
    ("C-11", "L'arrêter (Recommandé)", "Stop it (Recommended)", "JOURNAL l.322, réponse de l'investisseur"),
    ("C-12", "Oui, préparer S2-bis (Recommandé)", "Yes, prepare S2-bis (Recommended)",
     "JOURNAL l.322, réponse de l'investisseur"),
    ("C-13", "Oui, en principe (Recommandé)", "Yes, in principle (Recommended)",
     "JOURNAL l.322, réponse de l'investisseur"),
    ("C-14", "(i) faux", "(i) false", "JOURNAL l.322"),
    ("C-15", "J28 l.435516", "J28 l.435516", "ce rapport, notation"),
    ("C-16", "≈", "≈", "ce rapport, notation"),
    ("C-17", "établie", "established", "doc 09, registre"),
    ("C-18", "0 `ok` sur 40 804 lectures, HTTP 401 dès 2026-08-26T19:00Z",
     "0 `ok` out of 40,804 readings, HTTP 401 from 2026-08-26T19:00Z", "ADR-0028 l.25"),
    ("C-19", "un seul test", "single test", "paquet §10.1"),
    ("C-20", "La borne vaut sous le modèle nul joint : le modèle d'indépendance du pool de doc 10 §5.1, avec une "
             "dépendance sérielle des fenêtres de portée < ℓ (A(window-dependence), doc 08). Le niveau est "
             "asymptotique […]. Il est conservateur sous fenêtres iid (plug-in de P̂_more). Il n'est pas démontré "
             "≤ 0,01 en échantillon fini",
     "The bound holds under the joint null model: the independence model of the pool of doc 10 §5.1, with a serial "
     "dependence of the windows of range < ℓ (A(window-dependence), doc 08). The level is asymptotic […]. It is "
     "conservative under iid windows (plug-in of P̂_more). It is not demonstrated ≤ 0.01 in finite samples",
     "paquet §10.2 pt 7"),
    ("C-21", "Aucune significativité par paire : c'est du descriptif", "No significance per pair: this is descriptive",
     "paquet §5 (D3)"),
    ("C-22", "qui rend exacte la mention “proxy bruité”", "which makes the mention ‘noisy proxy’ exact",
     "paquet §5 (D3)"),
    ("C-23", "proxy bruité", "noisy proxy", "paquet §5 (D3)"),
    ("C-25", "le premier sha reste cité", "the first sha remains cited", "ADR-0028 §1 bis.8"),
    ("C-26", "L'oracle `recompute_*`, rejoué dans l'exécution unique, est un contrôle interne : ce n'est pas le test "
             "de composition",
     "The `recompute_*` oracle, replayed in the single execution, is an internal check: it is not the composition "
     "test", "ADR-0028 §3"),
    ("C-27", "L'exécution unique imprime et enregistre ce verdict sans qu'il la ferme (run nommé qui sort 0 quel que "
             "soit le verdict […] ; la liste des gardes de D.4 b est fermée)",
     "The single execution prints and records this verdict without the verdict closing it (named run that exits 0 "
     "whatever the verdict […]; the list of guards of D.4 b is closed)", "paquet §12 pt 1"),
    ("C-28", "Aucun auteur de la règle n'a vu z, K, P̂_more ni φ (annexe D.3)",
     "No author of the rule has seen z, K, P̂_more or φ (annex D.3)", "paquet §10.2 pt 11"),
    ("C-29", "≈ ±0,11", "≈ ±0.11", "doc 10"),
    ("C-30", "compte 16 lectures en D.1 (la n° 16, exposition de l'orchestrateur de la session cloud, est datée du "
             "2026-10-02 après le premier sceau et avant celui-ci)",
     "counts 16 readings in D.1 (No. 16, exposure of the orchestrator of the cloud session, is dated 2026-10-02, "
     "after the first seal and before this one)", "paquet l.8"),
    ("C-31", "l'orchestrateur de la session cloud", "the orchestrator of the cloud session", "JOURNAL l.310"),
    ("C-32", "repris au rapport de l'exécution", "taken up in the report of the execution", "annexe B.38"),
    ("C-33", "avant scellement", "before sealing", "annexe B.38"),
    ("C-34", "non", "no", "annexe D.3 (i), attestation de l'investisseur"),
    ("C-35", "Corriger et resceller", "Correct and reseal", "décision de l'investisseur du 2026-10-02"),
    ("C-36", "quasi morts", "quasi-dead", "annexe B.39"),
    ("C-37", "fenêtres à diagnostic d'hôte dégradé retirées", "windows with a degraded-host diagnostic removed",
     "annexe B.6"),
    ("C-38", "identifié", "identified", "annexe B.6"),
    ("C-39", "non identifié sous censure arbitraire", "not identified under arbitrary censoring", "annexe B.6"),
    ("C-40", "de type Manski", "Manski-type", "annexe B.6"),
    ("C-41", "Code", "Code", "ce rapport, §12"),
    ("C-42", "Rejeu", "Replay", "ce rapport, §12"),
]

# --- Passages protégés (lot DOCS11-PUBLIC, contrôle 4) et leur forme anglaise ---------------------------------------
# (identifiant, forme française dans la source, forme attendue dans la traduction). Comptes égaux exigés, espaces
# normalisées. Les formes identiques sont gardées à l'octet (sorties, empreintes, verdicts).

PROTEGES = [
    ("P-01", "**« R1 discrimine » = FAUX**", "**« R1 discrimine » = FAUX**"),
    ("P-02", "« R1 discrimine » vaut FAUX", "« R1 discrimine » has the value FAUX"),
    ("P-03", "la règle rend dans chacune des deux strates la valeur **NE REJETTE PAS, au titre de",
     "the rule returns, in each of the two strata, the value **NE REJETTE PAS [*does not reject*], on account of"),
    ("P-04", "la cause n'est pas identifiée entre co-défaillance des sources et dépendance sérielle des fenêtres",
     "la cause n'est pas identifiée entre co-défaillance des sources et dépendance sérielle des fenêtres"),
    ("P-05", "« R1 discrimine » (§1 bis.1 pt 6 ; déclencheur de D6 (vi) et D9) = FAUX : aucune strate ne rejette ; "
             "strate(s) testée(s) : calme, stress",
     "« R1 discrimine » (§1 bis.1 pt 6 ; déclencheur de D6 (vi) et D9) = FAUX : aucune strate ne rejette ; "
     "strate(s) testée(s) : calme, stress"),
    ("P-06", "Il n'établit ni n'exclut une co-défaillance des sources",
     "It neither establishes nor excludes a co-failure of the sources"),
    ("P-07", "Il n'établit pas l'indépendance des sources (doc 09).",
     "It does not establish the independence of the sources (doc 09)."),
    ("P-08", "« ajoutée après le pré-enregistrement, hors décision ; ne change pas le verdict",
     "« ajoutée après le pré-enregistrement, hors décision ; ne change pas le verdict"),
    ("P-09", "hors décision", "hors décision"),
    ("P-10", "Hors décision", "Hors décision"),
    ("P-11", "NE REJETTE PAS", "NE REJETTE PAS"),
    ("P-12", "4d2a8276316b1c66a08aabb15ff3b39be812978e93dafc01a4e627f20d0af528",
     "4d2a8276316b1c66a08aabb15ff3b39be812978e93dafc01a4e627f20d0af528"),
    ("P-13", "519423510b21ecbebda895d6e225ab0748fb0fe5a2b257a36c9301e36bfaa3e9",
     "519423510b21ecbebda895d6e225ab0748fb0fe5a2b257a36c9301e36bfaa3e9"),
    ("P-14", "9edb19b53379f370e291c5da01d4df3bc269b67a44feddb589d1211ec5ec6b0e",
     "9edb19b53379f370e291c5da01d4df3bc269b67a44feddb589d1211ec5ec6b0e"),
    ("P-15", "série `0x08CFC8D5`, **genTime 2026-10-03T01:04:10Z**, horloge de FreeTSA",
     "serial `0x08CFC8D5`, **genTime 2026-10-03T01:04:10Z**, FreeTSA's clock"),
    ("P-16", "494d770d704dc7c342f0c6deec269e5642b3621bf451922f991e4ca1fb968097",
     "494d770d704dc7c342f0c6deec269e5642b3621bf451922f991e4ca1fb968097"),
    ("P-17", "680a95fdf50908cea797ae4fe9f0b42c43b5a99fcad755cb410e26fa6e794209",
     "680a95fdf50908cea797ae4fe9f0b42c43b5a99fcad755cb410e26fa6e794209"),
    ("P-18", "genTime 2026-10-02T17:44:30Z", "genTime 2026-10-02T17:44:30Z"),
    ("P-19", "f35a70c19ba8269f1f7e2bcd31775e4fc513da20", "f35a70c19ba8269f1f7e2bcd31775e4fc513da20"),
    ("P-20", "06d189cf84e7dca97bdfc0e1b695fc827a09473779505c7a8f1af1e7c26e9050",
     "06d189cf84e7dca97bdfc0e1b695fc827a09473779505c7a8f1af1e7c26e9050"),
    ("P-21", "Python 3.11.15", "Python 3.11.15"),
    ("P-22", "`bash scripts/sceau/verify.sh`", "`bash scripts/sceau/verify.sh`"),
    ("P-23", "351f51b2e4b7421b4ee286c27465cde239124d6edd70c0e550741d22f83366ff",
     "351f51b2e4b7421b4ee286c27465cde239124d6edd70c0e550741d22f83366ff"),
    ("P-24", "98c5793ec460e3c009b7f743796800ae7259f71c65a4063a3c315e8eea595d74",
     "98c5793ec460e3c009b7f743796800ae7259f71c65a4063a3c315e8eea595d74"),
    ("P-25", "39ffb13fb0e5939ff88285ce256fbd416b0665c20ee6394c512eed7d2175c15d",
     "39ffb13fb0e5939ff88285ce256fbd416b0665c20ee6394c512eed7d2175c15d"),
    ("P-26", "70910984076474987239d8c7a9da786acc95c38b375ad572d78afa297bf8caf4",
     "70910984076474987239d8c7a9da786acc95c38b375ad572d78afa297bf8caf4"),
    ("P-27", "41 676 139, 148 930 880 et 204 107 558 octets", "41,676,139, 148,930,880 and 204,107,558 bytes"),
    ("P-28", "Une nouvelle production par `rendu_unique.py` serait une seconde exécution, déviation déclarée "
             "(annexe D.4 b).",
     "A new production by `rendu_unique.py` would be a second execution, a declared deviation (annex D.4 b)."),
    ("P-29", "tout rejeu (`recompute_*`) ou ré-exécution du rendu de S2 se fait sur une extraction de `f35a70c`",
     "any replay (`recompute_*`) or re-execution of the S2 rendering is done on an extraction of `f35a70c`"),
    ("P-30", "un tiers à qui l'on remet le paquet scellé, le sceau et les rendus sans",
     "a third party who is given the sealed package, the seal and the renderings without"),
    ("P-31", "Le contrôle du sceau exige le paquet scellé, remis avec le sceau sur demande",
     "Checking the seal requires the sealed package, which is provided together with the seal on request"),
    ("P-32", "le paquet scellé, le sceau, les rendus, les enregistrements et les scripts sont remis sur demande, "
             "sous accord",
     "the sealed package, the seal, the renderings, the records and the scripts are provided on request, "
     "under agreement"),
    ("P-33", "Le paquet scellé, le sceau, les rendus, les enregistrements et les scripts sont au même dépôt privé",
     "The sealed package, the seal, the renderings, the records and the scripts are in the same private "
     "repository"),
]

# Libellés de verdict comptés : même nombre d'occurrences bornées dans la source et dans la traduction (glossaire
# final exclu).
LIBELLES_COMPTES = {
    "FAUX": "(?<![" + LETTRE + "])FAUX(?![" + LETTRE + "])",
    "VRAI": "(?<![" + LETTRE + "])VRAI(?![" + LETTRE + "])",
    "REJETTE (nu)": "(?<![" + LETTRE + "])(?<!NE )REJETTE(?! PAS)(?![" + LETTRE + "])",
    "NE REJETTE PAS": "NE REJETTE PAS",
    "NON ÉVALUABLE": "NON ÉVALUABLE",
    "R1 discrimine": "R1 discrimine(?![" + LETTRE + "-])",
    "ÉTEINT / ETEINT": "[ÉE]TEINT",
}

# --- Termes (fr → en), appliqués partout (brief, point 7) ------------------------------------------------------------

TERMES = [
    ("k_eff ; k nominal ; k nominal_s", "k_eff ; nominal k ; nominal k_s",
     "k_eff: number of classes of the measured R2 partition; never an independence count"),
    ("enveloppe ; hors-enveloppe", "envelope ; out-of-envelope", ""),
    ("fenêtre ; fenêtres sautées", "window ; skipped windows", "one minute of the UTC grid"),
    ("strate ; strate calme ; strate de stress ; strate poolée", "stratum (pl. strata) ; calm stratum ; stress "
     "stratum ; pooled stratum", "printed stratum names: calme, stress"),
    ("flux", "feed", "a reading of the BTC/USD (or BTC/USDT) price served by a source"),
    ("source ; place (d'échange) ; agrégateur ; oracle", "source ; exchange ; aggregator ; oracle", ""),
    ("hôte ; hôte de collecte", "host ; collection host", ""),
    ("panne", "outage", "status panne_transport kept as printed"),
    ("écart (doc 10 §5.2) ; en écart ; co-écart ; taux d'écart",
     "anomaly ; anomalous ; co-anomaly ; anomaly rate",
     "a feed is anomalous in a window if in outage, stale or out of envelope"),
    ("écart (sens courant) ; écart déclaré (à un texte) ; écart (contrôle d'horloge)",
     "difference, gap ; declared departure ; offset",
     "offset: clock-check sense (§9.2 pt 17), as in the median offset of §11.1"),
    ("déviation (déclarée)", "(declared) deviation", "departure from the pre-registered plan"),
    ("co-défaillance", "co-failure", ""),
    ("discordance", "discordance", "rule case: z_s ≥ 2.33 and published z_bloc,s < 2.33"),
    ("sceau ; sceller ; scellé ; scellement", "seal ; to seal ; sealed ; sealing", ""),
    ("paquet (de pré-enregistrement) ; paquet scellé", "(pre-registration) package ; sealed package", ""),
    ("rendu (nom)", "rendering", "an output file of the single execution (SUITE, J14p, J14s, J28, RT, RAW)"),
    ("exécution unique", "single execution", ""),
    ("sortie ; sortir 0", "output ; exit 0", ""),
    ("journal ; journaux scellés ; journal brut", "journal ; sealed journals ; raw journal",
     "JOURNAL: the project journal"),
    ("relevé", "probe record", "diagnostic record of the harness (asn_attribution, clock_check)"),
    ("enregistrement (d'oracle)", "(oracle) record", ""),
    ("lecture", "reading", "a data reading; also an interpretation; also an access listed in annex D.1"),
    ("rédacteur (frais) ; auteur ; validateur ; relecture", "(fresh) drafter ; author ; validator ; review", ""),
    ("valider", "accept (at review)", "the assurance qualifier listed in doc 09 is not used (gate S-G4)"),
    ("orchestrateur ; investisseur ; sous-agent", "orchestrator ; investor ; sub-agent", ""),
    ("feu vert ; brouillon", "go-ahead ; draft", ""),
    ("dépôt (privé) ; versé", "(private) repository ; filed", ""),
    ("harnais ; démarrage", "harness ; start", ""),
    ("garde ; déclencheur", "guard ; trigger", ""),
    ("drapeau ; levé ; éteint", "flag ; raised ; off", "printed state kept: ÉTEINT, ETEINT"),
    ("seuil ; puissance", "threshold ; power", ""),
    ("erreur-type ; erreur-type par blocs ; plancher d'erreur-type par blocs",
     "standard error ; block standard error ; block standard-error floor", ""),
    ("excès minimal détectable", "minimum detectable excess", "EMD_s"),
    ("statistique confirmatoire", "confirmatory statistic", ""),
    ("censure ; bornes (non) extérieures", "censoring ; (non-)outer bounds", ""),
    ("plage (D5) ; segment ; coupe", "(D5) range ; segment ; cut", ""),
    ("variante exclue ; variante incluse", "excluded variant ; included variant", ""),
    ("sensibilité ; descriptif", "sensitivity ; descriptive", ""),
    ("bloc ; bloc machine", "block ; machine block", ""),
    ("jeton ; manifeste ; horodatage ; autorité d'horodatage",
     "token ; manifest ; timestamp ; timestamping authority", ""),
    ("délai de rétractation ; tête gardée ; voie (a)", "withdrawal period ; guarded head ; route (a)", ""),
    ("recalcul tiers ; chemin de recalcul ; rejeu", "third-party recomputation ; recomputation path ; replay", ""),
    ("commit d'analyse ; commit de collecte", "analysis commit ; collection commit", ""),
    ("amont ; amont déclaré", "upstream ; declared upstream", ""),
    ("résidu ; chemin de lecture ; chemin de mesure", "residual ; reading path ; measurement path", ""),
    ("mono-vantage ; sonde multi-résolveurs", "single-vantage ; multi-resolver probe", ""),
    ("constat ; [constat du rapport] ; inféré", "finding ; [report finding] ; inferred", "[calc]: drafter's "
     "computation"),
    ("recopié ; imprimé ; étiquette", "copied (verbatim outputs) or quoted (translated quotations) ; printed ; "
     "label", "a translated quotation is not a verbatim copy; the original prevails"),
    ("limite ; lot ; annexe", "limitation ; work package ; annex", ""),
    ("pt, pts ; n° ; l.", "pt, pts ; No. ; l.", "point(s) ; number ; line"),
    ("exposition ; poste local ; session cloud", "exposure ; local workstation ; cloud session", ""),
    ("fonction de difficulté", "difficulty function", "Littlewood and Miller (L&M)"),
    ("témoignage attesté", "attested statement", "doc 09"),
    ("J14 principal ; J14 second", "main J14 ; second J14", "run names kept: j14-principal, j14-second"),
]

# --- Registre (doc 09) transposé en anglais : exceptions motivées --------------------------------------------------
# (motif régulier du registre, glose ou texte qui porte l'occurrence admise, motif de l'admission)
EXCEPTIONS_REGISTRE = [
    ("k sources", "10 sources / 11 feeds",
     "glose d'une sortie imprimée recopiée (J28 l.44, l.45), colonne « k nominal_s » : k nominal nommé par la "
     "colonne (même exception que le lot DOCS11-PUBLIC)"),
]
