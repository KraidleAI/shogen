# Journal de provenance G1 — rédaction du rapport de S2 (`docs/11-mesures-pilotes.md`)

Rédacteur frais (fiche `shogen-worker`), instance neuve. Ouvert le 2026-10-04 (horloge lue : `date -u` →
`Sun Oct  4 02:32:47 UTC 2026`).

## Gate 0

Identifiant de modèle déclaré par l'environnement : `claude-opus-5-5`. L'effort n'est pas observable depuis
la session (déclaré `max` par la fiche ; non vérifiable de mon côté).

## Brief

- `/tmp/claude-0/-home-user-shogen/7ba84933-ba6d-5813-9ef4-ca3ac4febd16/scratchpad/rapport/BRIEF-RAPPORT.md`
  [lu, 86 lignes] ; sha256 recompté `8c83d0ca1988f6d64f92504d5b7788a9546a6b3dedcde82c81602535fc97d184`
  (égal à la valeur de l'orchestrateur).

## État du dépôt (lecture seule)

- `git rev-parse --abbrev-ref HEAD` → `partie-4-execution` ; `git rev-parse --short HEAD` → `81c5ad7` (égal au brief).
- `git status --short` → vide (arbre propre au départ).

## Sources lues (au fil de l'eau)

(voir « Lectures (ordre chronologique) » ci-dessous et la synthèse finale, avec les niveaux [lu] / [abs] / [2nd])

## Commandes et sorties

(consignées dans les entrées numérotées ci-dessous, au fil de l'eau)

### Lectures (ordre chronologique)

1. `docs/adr-0028/ANNEXE-D-preenregistrement.md` [lu, l.1-211, en entier] — liste fermée D.2 (12 points) repérée
   avant toute autre lecture ; aucune pièce de D.2 ouverte ; D.1 n° 16 l.28 ; D.4 b l.134-145 ; D.4 c l.147-167 ;
   D.5 l.169-190.
2. `docs/adr-0028/PAQUET-PREREG-S2.md` [lu, l.1-223, en entier] — §10.2 pts 1-11 l.114-133 ; §11 l.174-185 ;
   §12 pts 1-20 l.187-208 ; bloc machine l.214-223 ; révision datée A-8 l.8.
3. `docs/adr-0028/ADR-0028-decisions-sortie-S2.md` [lu, l.1-327, en entier] — D1 l.20-28 ; D2 l.29-42 ; D3 l.43-50 ;
   D4 l.51-56 ; D5 l.57-62 ; §1 bis.1 pts 1-11 l.93-110 ; clauses hors texte scellé l.112-114 ; D6 (v) l.199,
   (vi) l.200 ; D9 l.222-233 ; §3 tuyaux l.239-249 ; §4 l.251-285.
4. Rendus `docs/adr-0028/execution/rendu-2026-10-04/` : `wc -l` → 623 (suite), 209914 (j14-principal),
   112456 (j14-second), 435821 (j28), 18661 (recalcul-tiers), 1 (raw), 582 (json). sha256 recomptés :
   suite 4f223a22…aeb3a ; j14-principal 246ebeea…1498 ; j14-second d89db3a9…2b24 ; j28 26877549…65c0 ;
   recalcul-tiers a76ad448…1ac8 ; raw e996c634…97b8 ; json 355cf9bb…9c5c (valeurs complètes en §Commandes).
5. J28 (`…943.3-j28.out`) [lu] : repères `grep -n '^\[BLOC\|^\[SENS\|^\[ÉTIQ'` → l.1 ÉTIQUETTE, l.6 BLOC 1,
   l.3659 BLOC 2, l.435447 BLOC 3, l.435539 BLOC 4, l.435671 BLOC 5, l.435778 BLOC 6, l.435799 SENSIBILITÉ.
   Bloc 1 lu l.6-47 (clés) ; l.48-3657 = 3 610 lignes `controle_horloge` (compte par grep, non recopiées).
   Bloc 2 non lu (hors l.435440-435446, vues en bordure du bloc 3) et jamais recopié. Bloc 3 lu l.435447-435537.
   Bloc 4 lu l.435539-435669 (55 paires par strate, quatre comptes [n11 n10 n01 n00] et φ) ; bloc 5 lu
   l.435671-435776 ; bloc 6 lu l.435778-435797 ; [SENSIBILITÉ] lue l.435799-435820.
   Constat de lecture (à porter au rapport, étiqueté) : bloc 5 (d), l.435767, imprime « aucun cluster à ≥ 2 flux (1) »
   alors que le bloc 6, l.435785, nomme un cluster de 8 flux (AS13335). Libellé rapporté tel quel ; aucune
   interprétation par le code (le code n'est pas une source admise du brief).
6. Recherche des divergences ASN : `grep -c 'DIVERGENCE' *.out` → 0 dans j14-principal, j14-second, j28,
   recalcul-tiers, raw ; 1 dans suite (nom de test, l.379). `grep -n -i 'divergen'` → `"asn_divergences": []` aux
   l.4522, 8900, 13335, 18099 de recalcul-tiers ; ailleurs, seulement le résidu 4 du bloc 5 et des noms de tests.
7. `docs/adr-0028/ANNEXE-B-items.md` [lu, titres l.9-645 par grep ; B.38-B.45 l.542-664 en entier].
8. `docs/adr-0028/ANNEXE-A-lots.md` [lu par grep l.9-108, puis l.110-133] — ligne CORR l.126 ; G2-P4 l.127 ;
   PAQUET l.39 ; RENDU-1/2 l.37-38.
9. `JOURNAL.md` [lu, seulement les entrées datées 2026-10-03 et 2026-10-04 : `grep -n "^> \*\*2026-10-0[34]"` →
   l.300, 302, 304, 306, 308, 310, 312, 314, 316, 318 ; lues par `sed -n '300,318p'`]. La l.318 (2026-10-04
   02:33:28 UTC, directive de l'investisseur) est apparue pendant ma rédaction (fichier de 316 lignes à 02:33 UTC,
   318 ensuite). Aucun chiffre repris du JOURNAL quand un rendu le porte (les valeurs de la l.316 sont arrondies,
   donc de seconde main pour moi : non reprises).
10. J14 principal (`…943.1-j14-principal.out`) [lu] : repères l.1, 6, 1779, 209551, 209640, 209772, 209874 ;
    bloc 1 clés l.27-43 (hors `controle_horloge`) ; bloc 3 l.209551-209638 (lignes par source filtrées) ;
    bloc 5 (a) l.209772-209800 ; bloc 6 l.209874-209913.
11. J14 second (`…943.2-j14-second.out`) [lu] : repères l.1, 6, 972, 112108, 112197, 112329, 112436 ;
    bloc 1 clés l.31-43 ; bloc 3 l.112108-112195 ; bloc 5 (a) l.112329-112345 ; bloc 6 l.112436-112455.
12. Recalcul tiers (`…943.4-recalcul-tiers.out`) [lu par `python3 -B` (json.load), clés et valeurs] : entrées
    `j14-principal`, `j14-second`, `j28`, `j28-incluse` ; `avertissements` vide. Constat : l'entrée `j28-incluse`
    (étiquette « sensibilité « plage incluse » de la liste fermée (D2 pt 7), hors décision, biaisée vers le haut par
    construction ») porte un `drapeau_2` avec `"r1_discrimine": "VRAI"` (l.18045), `rejette` = calme, état `eteint`
    (l.17705) ; z_bloc calme de la variante incluse 2.508… (> 2,33). Hors décision ; à rapporter avec son étiquette.
13. Verdict brut (`…943.5-raw.out`, 1 ligne) [lu en entier] ; suite (`…943.0-suite.out`) [lu : tête, queue,
    `grep` des lignes skipped/Ran/OK] : l.621 `Ran 398 tests in 62.358s`, l.623 `OK (skipped=2)`, l.207 et l.209
    les deux tests sautés (variable absente).
14. Enregistrement (`…943.json`) [lu par `python3 -B` : toutes les clés ; `tree.sha256` compté, 436 fichiers].
15. `docs/adr-0028/sceau/README.md` [lu, 34 l.] ; `docs/adr-0028/sceau/premier-2026-10-02/README.md` [lu, en entier] ;
    manifestes `PAQUET.sha256` des deux sceaux [lus].
16. Contrôles du sceau rejoués par moi (lecture seule) :
    - `sha256sum` : paquet 4d2a8276…f528 ; manifeste 51942351…a3e9 ; jeton 9edb19b5…6b0e ; requête 887c5243…5ad7 ;
      cacert 2151b611…4438 ; tsa.crt 8bfb0305…3467 ; premier manifeste 680a95fd…4209 ; premier jeton 5f5ce535…0ee8.
    - `openssl ts -reply -in docs/adr-0028/sceau/paquet.tsr -text` (OpenSSL 3.0.13) → `Serial number: 0x08CFC8D5`,
      `Time stamp: Oct  3 01:04:10 2026 GMT` ; premier jeton → `0x08CC76D7`, `Oct  2 17:44:30 2026 GMT`.
    - `bash scripts/sceau/verify.sh` (script lu avant : aucune écriture) → `docs/adr-0028/PAQUET-PREREG-S2.md: OK`,
      `Verification: OK` deux fois, genTime ci-dessus, sortie 0 (avertissement OpenSSL “is not a CA cert” sur tsa.crt).
17. Garde (2) et script, rejoués (lecture seule) : `git diff --quiet f35a70c 27b0e30 -- s2-harness/shogen_s2
    s2-harness/tools` → 0 ; même contre HEAD `81c5ad7` → 0 ; `git show f35a70c:s2-harness/tools/rendu_unique.py |
    sha256sum` → 06d189cf…9050 (= `sha256_script`) ; `git merge-base --is-ancestor f35a70c 27b0e30` → 0 ; dates de
    commit : 27b0e30 2026-10-04T01:11:11Z ; 3be95be 2026-10-03T01:02:33Z ; 2d51940 2026-10-03T01:04:03Z ; b7a1b4a
    2026-10-03T01:05:55Z ; ed15613 2026-10-04T01:08:47Z ; d8074fa 2026-10-04T01:36:28Z. `git show 27b0e30:JOURNAL.md |
    grep -n -o <sha du paquet>` → l.304 (seul le sha affiché).
18. `docs/09-vocabulaire.md` [lu, l.1-63, en entier].
19. `docs/08-assumptions.md` [lu, l.1-76, en entier] — A(axis-coverage), A(window-stationarity), A(window-dependence),
    A(loss-non-informative), A(asn-attribution), A(host-integrity), A(harness-clock), A(prereg-blindness).
20. `docs/04-certificat-diversite.md` [lu : titres par grep ; §2 l.45-102 en entier].
21. `docs/10-mesures-pilotes-design.md` [lu : titres par grep ; l.1-49 (tête, §1) ; l.204-276 (§4.1) ;
    l.376-420 (§5.1) ; l.465-497 (§5.4) ; l.541-627 (§5.6, §6, §7, §8)].
22. `docs/adr-0028/AVIS-SEUIL-FLUX-QUASI-MORT.md` [lu : titres ; l.1-40 (§1 et début du §2)].
23. `docs/adr-0028/ANNEXE-B-items.md` [lu en plus : B.6 l.91-129 ; B.13 l.217-227 ; B.18 l.301-311] pour les items
    d'après l'exécution (DEP-FENETRES-2, R1-PLUGIN-1, HOST-DEGRADED-2, FLUX-QUASI-MORT-1, CENSURE-INFO-2,
    CONTENU-DEP-1, POOLEE-BLOC-1) et la précédence D-4 (Q-G2-2 ratifiée, l.311).
24. Incident de lecture (déclaré) : un `grep -i 'avertissement\|non fini\|NaN'` sur les rendus a apparié « nan » dans
    « binance » et affiché 7 lignes du bloc 2 du J28 (l.3662-3734 : prix de binance des premières fenêtres) ; rien
    n'en est recopié au rapport. Recherche refaite sensible à la casse.
25. Script `d3_lift.py` (SHOGEN-D3-LIFT-1) écrit dans `rapport/` ; entrée : le rendu J28 seul (bloc 4, l.435547-435601
    et l.435612-435666). Tests d'abord : `python3 -B d3_lift.py <J28> --mutant` → « auto-test … : ÉCHEC — identité
    fausse sur [2 1 1 6] », sortie 1 ; puis `python3 -B d3_lift.py <J28> | tee d3_lift.sortie.txt` → auto-test OK,
    110 tables lues, identité exacte 110/110, écart maximal |φ recalculé − φ imprimé| = 2.38E-50, six lifts des paires
    de singletons ; sortie 0. sha256 : `d3_lift.py` 8f91474c…9381 ; `d3_lift.sortie.txt` 77ae69ec…c73f.
26. Script `controles_r1.py` (recomptes de contrôle, hors décision) : entrée le rendu J28 seul (bloc 1 l.37 ; bloc 3
    l.435451-435537 ; [SENSIBILITÉ] l.435807-435812). Tests d'abord : `--mutant` (P̂₁ amputé d'un terme) →
    « auto-test … : ÉCHEC — 1/4 », sortie 1 ; normal → auto-test OK ; P̂₀, P̂₁, P̂_more recomptés exactement depuis
    les écarts entiers par flux ; z_s, γ̂₀, z_bloc (σ̂² imprimé), FIV et facteurs, cv, EMD_s et fraction, bornes de
    censure, écart de z de la sensibilité, z_pool : écart relatif maximal 4.21E-50 ; valeur de la règle recomptée
    égale à l'imprimée dans les deux strates ; identités entières (35982, 2618, grille 46468, 7795, T_fin) ; les
    cinq window_start du verdict brut dans la plage D5. Sortie 0. sha256 : `controles_r1.py` 11779f79…4c4f ;
    `controles_r1.sortie.txt` 0469a499…3e3e.
27. Script `comparer_recalcul.py` (comparaison de chaînes, aucun calcul) : JSON du run `recalcul-tiers` contre blocs 3
    et 6 des rendus J28, J14 principal, J14 second (n, K, P̂_more, garde, z, γ̂₀, σ̂², cv, FIV et facteurs, z_bloc,
    runs, décomposition de K, état du drapeau 2, « R1 discrimine »). `--mutant` (dernier chiffre de z calme du J28
    altéré en mémoire) → 125/126, la différence nommée, sortie 1 ; normal → 126/126 égales, sortie 0. sha256 :
    `comparer_recalcul.py` 4e61cea8…7585 ; `comparer_recalcul.sortie.txt` 8e6731f9…459e.
28. Recalcul tiers, structure R2 (lecture `python3 -B`) : `exact_copy_pairs` = [] dans les quatre entrées (l.1520, 6557,
    10991, 15421) ; J28 `cluster_correlations` : `"cluster_pairs": {}`, `"n_multi_clusters": 1` (l.10984-10988) :
    le « (1) » du libellé du bloc 5 (d) du J28 (l.435767) correspond à ce compte ; libellé rapporté tel quel.
29. Rédaction : `rapport/11-mesures-pilotes.md`, morceau 1 (en-tête, conventions, §1 résumé, §2 instrument et
    campagne) écrit à 02:5x UTC ; guillemets imbriqués des recopies rendus par “ ” (convention déclarée au texte).
30. Scripts `extraire_tables.py` (extraction verbatim des valeurs du bloc 3 du J28 en lignes de table ; aucune
    arithmétique ; sha256 dfa0ea59…c9b4, sortie 6f4b99e6…bf01) et `calc_divers.py` (racines, durée, sommes,
    rapports τ, z_pool recompté, gardes des J14 ; sha256 069791fe…5f62, sortie 2aebf1c5…a009), sortie 0 chacun.
    Morceau 2 du rapport (§3) écrit à 02:5x UTC, avec les lignes J28 l.435515-435522 et l.435503 recopiées par `sed`.
31. Script `extraire_d5.py` (extraction verbatim des lignes τ observé l.435526-435530 et censure l.435536-435537 ;
    sha256 e56b25ac…6c32, sortie 3d3b2105…ea6b), sortie 0. Morceaux 3 (§4) et 4 (§5) du rapport écrits à 02:55-02:56 UTC.
32. Script `table_lift.py` (mise en table de `d3_lift.sortie.txt`, aucune arithmétique ; sha256 04dbcca9…9e53, sortie
    7e2b2da3…11af). Morceau 5 (§6) du rapport écrit à 02:57 UTC.
33. Script `extraire_hd.py` (extraction verbatim J14p, J14s, [SENSIBILITÉ], z_pool, L&M, variante incluse du RT ; une
    erreur de syntaxe f-string corrigée avant toute sortie ; sha256 final 15f1e647…a9e5, sortie 23b8f6de…c667),
    sortie 0. Morceau 6 (§7) écrit à 02:59 UTC ; quatre défauts de découpage de tables (ligne z_pool vide, ligne hors
    table, ligne L&M manquante, en-tête de la table des flux du §3.5) corrigés par remplacement exact depuis les
    sorties d'extraction.
34. Morceau 7 (§8, contrôles) écrit à 03:01 UTC ; RAW l.1 recopiée par `cat` dans un bloc verbatim.
35. `calc_divers.py` étendu (sommes des écarts par type, bloc 3 : calme 1 451 = 1 443 pannes + 4 staleness + 4
    hors-enveloppe, égal à Σ mⱼ ; stress 693 = 691 + 2 + 0, égal à Σ mⱼ ; 3 non évaluables en stress) ; docstring mis
    à jour ; relancé, sortie 0 (hash final au §Commandes).
36. Morceaux 8 (§9 limites) et 9 (§10, §11, §12) écrits à 03:03-03:04 UTC. Relecture complète à suivre.
37. Relecture complète du rapport (03:05-03:10 UTC) : corrections — « résultat négatif » rattaché à doc 10 §7 (et non
    au pt 8, qui vise le cas hors discordance) ; résidu 4 « à chaque quorum » ; z_pool en liste ; raison JSON de la
    variante incluse déplacée en bloc verbatim (ligne contrôlée identique à RT l.18046 par comparaison de chaînes) ;
    §8.9 précisé (calc_divers sans mode mutant) ; D.1 n° 16 complété (« nature exacte du taux non établie sans
    lecture ») ; doubles lignes vides retirées.
38. Contrôle `cargo --locked xtask verify` sur copie de l'arbre (03:08-03:10 UTC), dans `rapport/arbre/` :
    - copie : `git -C /home/user/shogen archive HEAD | tar -x -C arbre --exclude=docs/rapports --exclude=docs/adr-0025
      --exclude=docs/adr-0028/monark-m009a --exclude=biblio` (tar sortie 0 ; les quatre chemins exclus absents de la
      copie, contrôlé par `test -e`) ; rapport copié en `arbre/docs/11-mesures-pilotes.md` (sha256 identique).
    - essai A (commande exacte du brief) : `cargo --locked xtask verify` → sortie 1, VERDICT GLOBAL ROUGE ; S-G1, S-G2,
      S-G3, S-G4 (107 fichiers examinés sur 107, 0 violation), S-G7a, S-G8, fmt, no_std, clippy VERTS ; S-G5 et S-G6
      ROUGES sur un seul incident chacun : « biblio/INDEX.md illisible », conséquence de `--exclude=biblio`, sans lien
      avec le rapport. Sortie : `verify-A.out`.
    - essai B (même copie, plus le seul fichier suivi de biblio/ : `git archive HEAD biblio/INDEX.md | tar -x`) :
      sortie 0, VERDICT GLOBAL VERT ; S-G5 en régime « CORPUS INCOMPLET » (0 artefact sur 128 déclarés, comme en CI),
      299 fragments contrôlés, 264 non contrôlés, dont 0 venant de `docs/11-mesures-pilotes.md`. Sortie : `verify-B.out`.
    - la copie `arbre/` (avec son `target/`) est retirée après l'essai ; les sorties sont gardées.
39. Incident de lecture (déclaré) : un `grep -n 'orchestrateur de la session cloud' JOURNAL.md`, lancé sans filtre de
    date pour contrôler la citation de la l.310, a affiché les numéros de trois lignes datées du 2026-10-02 (l.206,
    l.218, l.236), coupées à 20 caractères (« > **2026-10-02 0 » ou « 1 ») : aucun contenu de ces entrées n'a été lu.
    Contrôle refait sur la seule l.310 (`sed -n '310p' | grep -o`) : la phrase y figure. Écart à la consigne du brief
    (JOURNAL : entrées du 2026-10-03 et du 2026-10-04 seulement), sans effet sur le rapport.
40. §10.1 adouci : l'identité de l'orchestrateur exposé (D.1 n° 16) et de l'orchestrateur exécutant n'est plus
    affirmée ; le rapport cite « l'orchestrateur de la session cloud » (JOURNAL l.310).
41. Essais finaux `xtask verify` sur la version finale du rapport (03:12 UTC) : essai A (commande exacte du brief)
    sortie 1, rouge par les deux seuls incidents « biblio/INDEX.md illisible » (S-G5, S-G6) ; essai B (avec
    `biblio/INDEX.md`) sortie 0, VERDICT GLOBAL VERT, 0 fragment non contrôlé venant de `docs/11`. Sorties
    `verify-A-final.out` (sha256 01b0cbad…8d14) et `verify-B-final.out` (178adf51…f281) ; copie `arbre/` retirée ;
    sorties des premiers essais (`verify-A.out`, `verify-B.out`), supplantées, retirées.

---

# Synthèse G1 (consolidée en fin de passe)

## Sources lues, avec niveau

| source | portion lue | niveau |
|---|---|---|
| `rapport/BRIEF-RAPPORT.md` | en entier (86 l.) | [lu] |
| `docs/adr-0028/ANNEXE-D-preenregistrement.md` | en entier (l.1-211) | [lu] |
| `docs/adr-0028/PAQUET-PREREG-S2.md` | en entier (l.1-223) | [lu] |
| `docs/adr-0028/ADR-0028-decisions-sortie-S2.md` | en entier (l.1-327) | [lu] |
| rendu J28 | l.1-47 ; l.48-3657 comptées par grep (3 610 `controle_horloge`) ; l.435440-435821 ; bloc 2 non lu (sauf l.3662-3734 vues par incident, n° 24) | [lu] |
| rendu J14 principal | l.1 ; l.6-43 hors `controle_horloge` ; l.209551-209914 | [lu] |
| rendu J14 second | l.1 ; l.6-43 hors `controle_horloge` ; l.112108-112456 | [lu] |
| recalcul tiers (JSON) | par `json.load` (clés, entrées, valeurs citées) et lignes citées | [lu] |
| verdict brut | en entier (1 l.) | [lu] |
| suite | tête, queue, lignes de tests sautés et de divergence (grep) | [lu] |
| enregistrement (JSON) | en entier par `json.load` | [lu] |
| `docs/adr-0028/ANNEXE-A-lots.md` | grep des lignes CORR/PAQUET/RENDU ; l.110-133 | [lu] |
| `docs/adr-0028/ANNEXE-B-items.md` | titres ; B.6 l.91-129 ; B.13 l.217-227 ; B.18 l.301-311 ; B.38-B.45 l.542-664 | [lu] |
| `docs/04-certificat-diversite.md` | titres ; §2 l.45-102 | [lu] |
| `docs/08-assumptions.md` | en entier | [lu] |
| `docs/09-vocabulaire.md` | en entier | [lu] |
| `docs/10-mesures-pilotes-design.md` | titres ; l.1-49, 204-276, 376-420, 465-497, 541-627 | [lu] |
| `docs/adr-0028/sceau/README.md`, `premier-2026-10-02/README.md`, les deux `PAQUET.sha256` | en entier | [lu] |
| `docs/adr-0028/AVIS-SEUIL-FLUX-QUASI-MORT.md` | titres ; l.1-40 | [lu] |
| `JOURNAL.md` | l.300-318 seulement (entrées du 2026-10-03 et du 2026-10-04) ; incident n° 39 | [lu] |
| `scripts/sceau/verify.sh` | en entier (avant exécution) | [lu] |
| `xtask/src/sg4.rs`, `sg5.rs`, `documents.rs` (`prose_hors_citations` et suite), `rapport.rs` (verdict), `lib.rs` (`verifier_tout`), en-têtes de `sg1`, `sg3`, `sg6`, `sg7a`, `sg8` | outils des gates, lus pour que le rapport passe S-G4/S-G5 ; rien n'en est repris au rapport | [lu] |

Non ouverts : `docs/PASSATION-CLOUD.md` (écart volontaire, voir plus bas), `docs/rapports/`, `docs/adr-0025/`,
`docs/adr-0028/monark-m009a/`, tout `*.jsonl`, tout dépôt externe, toute pièce de la liste fermée D.2, le code de
`s2-harness/` (aucun module lu). `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée (aucun test du harnais lancé).

## Chiffres recomptés (aucun chiffre de seconde main au rapport)

- `controles_r1.py` : P̂₀, P̂₁, P̂_more exacts depuis les entiers ; z_s, γ̂₀, z_bloc, FIV et facteurs, cv, EMD_s et
  fraction, bornes de censure, écart de z de la sensibilité, z_pool ; écart relatif maximal 4.21E-50 ; valeur de la
  règle recomptée égale ; identités entières ; verdict brut contre la plage D5.
- `comparer_recalcul.py` : 126/126 valeurs du recalcul tiers égales aux rendus, à la chaîne près.
- `d3_lift.py` : six lifts exacts des paires de singletons ; identité exacte 110/110 ; φ à 2.38E-50 près.
- `calc_divers.py` : racines, durée (22 min 20 s), sommes (7 628 ; 167), rapports τ, z_pool, gardes des J14, sommes
  des écarts par type (1 451 = 1 443 + 4 + 4 ; 693 = 691 + 2 + 0).
- Les valeurs du JOURNAL (l.316, arrondies) ne sont reprises nulle part ; les valeurs citées depuis l'ADR, le paquet,
  le JOURNAL ou le README du sceau le sont avec leur ligne.

## Écarts et incidents

1. `docs/PASSATION-CLOUD.md` non lu, malgré la consigne de CLAUDE.md pour une nouvelle session : la liste des sources
   du brief est fermée (« seules admises ») et le rôle est celui d'un rédacteur frais ; question posée à l'orchestrateur.
2. Incident n° 24 : 7 lignes du bloc 2 du J28 affichées par un grep insensible à la casse (« nan » de « binance ») ;
   rien recopié.
3. Incident n° 39 : numéros de trois lignes du JOURNAL datées du 2026-10-02 affichés (20 caractères), sans contenu.
4. Commande du brief pour `xtask verify` : rouge par la seule absence de `biblio/INDEX.md` (exclu avec `biblio`) ;
   second essai avec ce seul fichier suivi : vert.
5. Queues binomiales exactes des J14 non recopiées (lecture prudente de « Aucune p-valeur ») : question posée.
6. Résumé plus long qu'une demi-page (recopie des options de D6 (vi), D9 et du pt 11) : choix de fidélité, déclaré.
7. Sources outils lues hors de la liste du brief (code des gates `xtask`, `verify.sh`) : nécessaires à la règle du brief
   sur `xtask verify` et au rejeu du sceau ; aucune ne fournit de contenu au rapport.

## Attestation d'exposition du rédacteur

J'ai lu les rendus de l'exécution unique, comme le rôle l'exige (valeurs de z, K, P̂_more, φ du J28 et des sorties hors
décision). Je n'ai ouvert aucune pièce de la liste fermée D.2, ni `docs/rapports/`, ni `docs/adr-0025/`, ni
`docs/adr-0028/monark-m009a/`, ni aucun `*.jsonl`, ni aucun dépôt externe ; je n'ai lu du JOURNAL que les entrées du
2026-10-03 et du 2026-10-04 (incident n° 39 mis à part). Aucune opération git en écriture ; écritures limitées au
dossier `rapport/`.

## Fichiers produits (dossier `rapport/`), sha256 à la remise

```text
a73097da9d22d1b83ff132e2af79384fe50e221f63790a874c3a385e957eecf0  11-mesures-pilotes.md
4d210cb65fb56fc5c0ef00ec31480bbe96426746191c5efa38a9e2def99a1c98  calc_divers.py
4e61cea803c902054e6fcbd2cc6a29f7c71ac1a2f8bfd824aefaa851ebef7585  comparer_recalcul.py
11779f798b948b155462c7b66460009a0a2c991bb27653c2ad344c6c83744c4f  controles_r1.py
8f91474cdded5694e733334fadf225b110d3378ddb560f1bee4066eca80f9381  d3_lift.py
e56b25ac5b1b8551b6e3e8f58937fa214e523a8407bcc56462833099479a6c32  extraire_d5.py
15f1e64769285de713766886fe0d8fca455774da1f4dbbbeb9720f22e581a9e5  extraire_hd.py
dfa0ea59d18b288b8b39e28309548e2a83b4820f680896b145ed6bd26cd5c9b4  extraire_tables.py
04dbcca9d8d2f8f8add0f1935e460bb25d3baf5475fb77d34cd8570b32c79e53  table_lift.py
de7bd825bba4e71aeac9437dfafa26eb3101d00c3d1ea0b992b103c33f4c52af  calc_divers.sortie.txt
8e6731f9f3c6f0a73ad2fb7938e66c215dafe1d0c13934f4d6f804d6dd57459e  comparer_recalcul.sortie.txt
0469a499233d66cd64031c7cf21e82bf01615658e3f14cc25d8221afe5581e3e  controles_r1.sortie.txt
77ae69ec8666065d0e7ec3a13588f982d87de7bf1789ffe3f91813ea028dc73f  d3_lift.sortie.txt
3d3b210524d0fdbb0c4dd5b97d2ad3d94ca6b696a518fb1f249ad4a6779bea6b  extraire_d5.sortie.txt
23b8f6de3e1de25c6ff3ee4276f7ed4ba0cfa84e6d6da5338f63f0477c5fc667  extraire_hd.sortie.txt
6f4b99e66b0e7acd1a88d6907a63e021f90e90fbdbe96262a4ea940c4dc2bf01  extraire_tables.sortie.txt
7e2b2da35088ed67fd6aef6dcdb8dff936f8a0b52419c272858993191e3d11af  table_lift.sortie.txt
01b0cbad924c8ca9732eb2eda53d90ad82bd61f685d770f4a406c70c36a18d14  verify-A-final.out
178adf516fb11e3e730fde40ffb610d066c2e3b695c5ca58a54b101f6358f281  verify-B-final.out
```

Le sha256 de ce journal G1 n'y figure pas (un fichier ne porte pas son propre sha) ; il est donné dans le rapport à l'orchestrateur.

## Addendum daté du 2026-10-04 03:1x UTC : entrées du JOURNAL apparues pendant la rédaction

42. `git log` (lecture seule) montre que la tête a avancé pendant ma rédaction (81c5ad7 → 14d06c0 02:43:56, 15311d5
    02:45:51, c1657c8, 82901cf, ab55f81, 25406c8 03:13:54) et que l'arbre de travail porte des modifications de
    `JOURNAL.md` et de `brand/` qui ne sont pas les miennes. Je n'ai rien écrit au dépôt.
43. Lecture des nouvelles entrées datées du 2026-10-04 (périmètre admis) : `grep -n "^> \*\*2026-10-0[34]"` → l.320 à
    l.332 ; lues : l.320 (avis produit après S2), l.322 (décisions de l'investisseur après S2), l.324 (consigne S2-bis)
    par `sed -n '320,324p'`. Les l.326-332 (recherche G4, charte graphique, avis G4, accroche) n'ont été vues que par
    leur titre tronqué à 140 caractères, sans effet sur le rapport.
44. Rapport mis à jour : §1 (décisions consignées l.322, recopiées ; titre « ce rapport n'en tranche aucune »), §2.7 et
    §9.3 pt 5 (collecte sur le poste de l'investisseur, consigne l.324 recopiée), §10.5 (décisions après J28, non des
    déviations). Citations contrôlées par `grep -o` sur les l.320-324 : les six chaînes recopiées y figurent.
45. Les essais `xtask verify` des n° 38 et 41 ont été faits sur des copies prises par `git archive HEAD` à 03:08 et
    03:12 UTC, donc sur la tête du moment (au plus ab55f81) ; seul mon fichier y était ajouté.
46. Essais finaux refaits sur le rapport mis à jour (copie prise à la tête 25406c8) : A, sortie 1, rouge par les deux seuls incidents « biblio/INDEX.md illisible » ; B, sortie 0, VERDICT GLOBAL VERT, 0 fragment non contrôlé venant de docs/11.

## Fichiers produits, sha256 à la remise (remplace la liste précédente)

```text
0a40a8b32be75f6f89bb69316d4003ea7368b9c9952ad252b64e91484f370e98  11-mesures-pilotes.md
4d210cb65fb56fc5c0ef00ec31480bbe96426746191c5efa38a9e2def99a1c98  calc_divers.py
4e61cea803c902054e6fcbd2cc6a29f7c71ac1a2f8bfd824aefaa851ebef7585  comparer_recalcul.py
11779f798b948b155462c7b66460009a0a2c991bb27653c2ad344c6c83744c4f  controles_r1.py
8f91474cdded5694e733334fadf225b110d3378ddb560f1bee4066eca80f9381  d3_lift.py
e56b25ac5b1b8551b6e3e8f58937fa214e523a8407bcc56462833099479a6c32  extraire_d5.py
15f1e64769285de713766886fe0d8fca455774da1f4dbbbeb9720f22e581a9e5  extraire_hd.py
dfa0ea59d18b288b8b39e28309548e2a83b4820f680896b145ed6bd26cd5c9b4  extraire_tables.py
04dbcca9d8d2f8f8add0f1935e460bb25d3baf5475fb77d34cd8570b32c79e53  table_lift.py
de7bd825bba4e71aeac9437dfafa26eb3101d00c3d1ea0b992b103c33f4c52af  calc_divers.sortie.txt
8e6731f9f3c6f0a73ad2fb7938e66c215dafe1d0c13934f4d6f804d6dd57459e  comparer_recalcul.sortie.txt
0469a499233d66cd64031c7cf21e82bf01615658e3f14cc25d8221afe5581e3e  controles_r1.sortie.txt
77ae69ec8666065d0e7ec3a13588f982d87de7bf1789ffe3f91813ea028dc73f  d3_lift.sortie.txt
3d3b210524d0fdbb0c4dd5b97d2ad3d94ca6b696a518fb1f249ad4a6779bea6b  extraire_d5.sortie.txt
23b8f6de3e1de25c6ff3ee4276f7ed4ba0cfa84e6d6da5338f63f0477c5fc667  extraire_hd.sortie.txt
6f4b99e66b0e7acd1a88d6907a63e021f90e90fbdbe96262a4ea940c4dc2bf01  extraire_tables.sortie.txt
7e2b2da35088ed67fd6aef6dcdb8dff936f8a0b52419c272858993191e3d11af  table_lift.sortie.txt
d797b6cd148f349cc62d61aed59ca2fc3bdfb39373eb1b8e64316408da284dd6  verify-A-final.out
b5e804421a98fb115637b9c8409533612075ee6d884d674bc42dc2e5d78e2a4d  verify-B-final.out
```
47. §8.2 corrigé (têtes 81c5ad7 et 25406c8 ; garde (2) rejouée contre 25406c8 : sortie 0). Essais finaux refaits (copie à la tête 25406c8) : A sortie 1 (incidents biblio/INDEX.md seuls), B sortie 0, VERT, 0 fragment non contrôlé de docs/11.

## Fichiers produits, sha256 à la remise (version finale ; remplace les listes précédentes)

```text
4604fff312eda48916691c778b0e755186e4538486499677e7d50fea9f0f6a2a  11-mesures-pilotes.md
4d210cb65fb56fc5c0ef00ec31480bbe96426746191c5efa38a9e2def99a1c98  calc_divers.py
4e61cea803c902054e6fcbd2cc6a29f7c71ac1a2f8bfd824aefaa851ebef7585  comparer_recalcul.py
11779f798b948b155462c7b66460009a0a2c991bb27653c2ad344c6c83744c4f  controles_r1.py
8f91474cdded5694e733334fadf225b110d3378ddb560f1bee4066eca80f9381  d3_lift.py
e56b25ac5b1b8551b6e3e8f58937fa214e523a8407bcc56462833099479a6c32  extraire_d5.py
15f1e64769285de713766886fe0d8fca455774da1f4dbbbeb9720f22e581a9e5  extraire_hd.py
dfa0ea59d18b288b8b39e28309548e2a83b4820f680896b145ed6bd26cd5c9b4  extraire_tables.py
04dbcca9d8d2f8f8add0f1935e460bb25d3baf5475fb77d34cd8570b32c79e53  table_lift.py
de7bd825bba4e71aeac9437dfafa26eb3101d00c3d1ea0b992b103c33f4c52af  calc_divers.sortie.txt
8e6731f9f3c6f0a73ad2fb7938e66c215dafe1d0c13934f4d6f804d6dd57459e  comparer_recalcul.sortie.txt
0469a499233d66cd64031c7cf21e82bf01615658e3f14cc25d8221afe5581e3e  controles_r1.sortie.txt
77ae69ec8666065d0e7ec3a13588f982d87de7bf1789ffe3f91813ea028dc73f  d3_lift.sortie.txt
3d3b210524d0fdbb0c4dd5b97d2ad3d94ca6b696a518fb1f249ad4a6779bea6b  extraire_d5.sortie.txt
23b8f6de3e1de25c6ff3ee4276f7ed4ba0cfa84e6d6da5338f63f0477c5fc667  extraire_hd.sortie.txt
6f4b99e66b0e7acd1a88d6907a63e021f90e90fbdbe96262a4ea940c4dc2bf01  extraire_tables.sortie.txt
7e2b2da35088ed67fd6aef6dcdb8dff936f8a0b52419c272858993191e3d11af  table_lift.sortie.txt
67ae399a7204962f0f2df0a21dbbc376f8cae5f6e6d376a1fbd3bdbd4e8bae1a  verify-A-final.out
b5e804421a98fb115637b9c8409533612075ee6d884d674bc42dc2e5d78e2a4d  verify-B-final.out
```
