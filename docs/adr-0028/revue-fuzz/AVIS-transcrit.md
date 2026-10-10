# Avis de l'advisor sur Q-2 et Q-7 du lot FUZZ, précédé des questions (transcrit)

> Transcription par l'orchestrateur le 2026-10-10 03:36:30 UTC du fichier avis/QUESTIONS.md puis avis/AVIS.md ; contrôle FM-1.1 des transcripts du générateur-correcteur, de l'advisor, du réviseur G2 et du contre-contrôleur, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèles résolus : claude-opus-5-5 (générateur, G2, contre-contrôle), claude-fable-5-1 (advisor). Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Questions à l'advisor — lot FUZZ (seuil de distillation)

Contexte : `docs/adr-0028/ANNEXE-A-lots.md` l.59 (lot FUZZ : « 13 §7.3 : au moins 471/789 arêtes » ; gate de distillation) ; ADR-0011 seuil 7 et `fuzz/README.md` ; rapport du générateur `<scratchpad>/s2bis/fuzz/RAPPORT-GENERATEUR.md` (scratchpad = `<scratchpad>`) et son adjudication `ADJUDICATION.md`. But : Shōgen, standard institutionnel vendable, sans baisse de qualité ; règle « aucune dette ».

- **Q-2** : l'ancienne mesure (471 sur 789 arêtes apportées par le corpus dérivé) ne se rejoue plus sur le binaire courant. Le générateur a refait la base (afl-showmap d'AFL++ 4.40c, binaire de `c1122de` : E = 1 074 arêtes apportées par le dérivé) et transposé la fraction : seuil ⌈1074 × 471/789⌉ = 642 arêtes gagnées ; la famille distillée en gagne 745 (719 de E, 66,95 %). La transposition par fraction est-elle la bonne règle (plutôt qu'un seuil absolu, ou une autre base) ? Qui doit la ratifier (le registre parle d'une ratification du mainteneur) : faut-il un acte de l'investisseur, ou un avis d'advisor suffit-il (décision de l'investisseur du 2026-10-05 : accords rendus par un advisor) ?
- **Q-7** : à l'instrument de libFuzzer (compteurs 8 bits), la famille couvre environ 55,6 % de l'apport du dérivé, sous 471/789 ; le seuil n'est atteint qu'à afl-showmap, l'outil que fixe 13 §7. Faut-il exiger aussi un seuil à l'instrument de libFuzzer, ou écrire la différence comme observation ?

Rends ton avis dans `<scratchpad>/s2bis/fuzz/avis/AVIS.md` et par message, en français, court. Tu ne modifies rien d'autre. Interdits de lecture : `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/`, tout `*.jsonl`, toute pièce de D.2 ; aucune recherche récursive sur `docs/`, le dépôt ou le scratchpad.


---

# Avis de l'advisor — lot FUZZ, Q-2 et Q-7 (seuil de distillation)

**Gate 0** : modèle `claude-fable-5-1` (Fable 5.1), effort medium ; rôle advisor (CLAUDE.md §7). Date : 2026-10-09.

Pièces lues (plages) : `QUESTIONS.md` ; `RAPPORT-GENERATEUR.md` (entier) ; `ADJUDICATION.md` (entier) ; `docs/adr-0028/ANNEXE-A-lots.md` l.59 ; `docs/adr-0028/ANNEXE-B-items.md` l.28, l.1101, l.1167-1174 ; `docs/13-temoignage-e2e-design.md` l.185-195 ; `docs/12-fondations-ingenierie-design.md` l.99-114 (ADR-0011) ; `fuzz/README.md` et `crates/shogen-verifier/fuzz-corpus/README.md` (entiers) ; `JOURNAL.md` l.122, l.143, l.450 ; `docs/adr-0028/ANNEXE-D-preenregistrement.md` l.32-47 (liste D.2, pour l'appliquer) ; `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md` l.4-6 ; `docs/DECISIONS.md` l.24-35 (lignes de registre).
**Aucune pièce de D.2 ouverte ; aucun dossier interdit lu.** Écart déclaré : un `Glob *.md` lancé pour localiser ADR-0011 a listé des **noms** de fichiers de tout le dépôt (dont des noms sous `docs/rapports/` et `docs/pocket-report/`) ; aucun contenu n'a été ouvert ; aucune D.2 n'a été exposée (D.2 n° 5 vise la l.51 d'un fichier, pas son nom).

## Q-2 — la transposition par fraction, et qui ratifie

**Faits.** La règle écrite est « ≥ 471 des 789 arêtes au même outillage de mesure » (docs/13 l.195) ; 471 est l'apport du top-20 du glouton sur l'ancienne base, 789 l'apport total du dérivé. L'ancienne base n'est plus rejouable (JOURNAL l.122 : binaire de `20e1084`, `crates/` changé). Nouvelle base, même outil (afl-showmap AFL++ 4.40c, `fuzz/README.md` l.14) : E = 1 074 ; ⌈1074 × 471/789⌉ = 642 (505 854/789 = 641,13… ; recompte conforme à RAPPORT §2.1) ; famille distillée : 719 dans E (66,95 %), 745 gagnées, 0 arête de base perdue (RAPPORT §2.2) ; top-20 du glouton neuf : 624/1074 (58,1 %).

**Options.**
- (a) **Fraction transposée, 471/789 appliquée à E mesuré** → 642 (59,78 % ≥ 59,70 %). C'est la lecture littérale de docs/13 : le nombre « 471/789 » y est un rapport (« au moins 471 des 789 »), pas un compte abstrait ; la fraction est ce qui survit au changement de binaire.
- (b) **Sens d'origine, « au moins ce que le top-20 capturait »**, rejoué sur la base neuve → 624. Moins exigeant que (a) sur cette base ; dépend d'un paramètre (20) sans justification écrite.
- (c) **Seuil absolu 471** : sans sens — le dénominateur (3 024 → 3 904 arêtes du binaire, docs/13 l.195 et RAPPORT §2.2) et E ont changé ; 471/1074 = 43,9 %, ce serait une baisse de qualité silencieuse. À écarter.
- (d) **Autre base** (fraction de la carte totale, ou mesure à libFuzzer) : change l'objet mesuré ; non écrit dans 13 §7 ; relève d'un amendement de G0, non d'une transposition.

**Recommandation : (a)**, avec (b) écrit comme contrôle de cohérence (642 ≥ 624 : la transposition ne desserre pas le critère d'origine). Forme à écrire (FZ-e et README du corpus) : « seuil = ⌈E × 471/789⌉, E = arêtes apportées par le corpus dérivé versé, mesurées par afl-showmap sur le binaire courant ; référence datée : E = 1 074, seuil 642, binaire de `c1122de`, 2026-10-09 ».

**Risques et conditions.**
1. La gate FZ-c fige 1 074 et 471 (mutants C4, C5, RAPPORT §2.5) : avec la correction **C-2 de l'adjudication** (E recalculé en CI depuis le dérivé versé), le seuil doit être **calculé de E mesuré**, pas la constante 642 — sinon la gate compare une mesure courante à un seuil d'un autre binaire. 642 reste la valeur de référence écrite, le code dérive le seuil. Si le budget du job interdit C-2, garder 642 et la limite L-2/L-3 écrite (RAPPORT §6).
2. Règle L-3 adoptée par l'adjudication (jamais abaisser, redistiller) : indispensable, car une fraction de E recalculée est un seuil mobile ; elle n'est admissible que si la seule issue d'un rouge est une nouvelle distillation.
3. La gate CI compte 745 gagnées (sans intersection avec E) quand la mesure stricte est 719 ; les deux sont au-dessus de 642, mais le README doit nommer laquelle la gate compare (RAPPORT L-2 ; C-2 la rend stricte).

**Qui ratifie.** Le seuil d'origine fut lui-même une adjudication R-26 de l'orchestrateur sur avis d'advisor (docs/13 l.195 : « adjudication R-26 du 2026-08-13, option (d) de l'avis ADVISOR »). La consigne de l'investisseur du 2026-09-30 route les questions techniques, **Q-FUZZ-1 nommément**, vers les advisors (JOURNAL l.143) ; la décision du 2026-10-05 délègue aux advisors les accords de partie d'ADR-0029 et réserve à l'investisseur dépense, calendrier, déclaration publique et Pocket (JOURNAL l.450 ; annexe B l.1169) — la transposition d'un seuil de couverture ne touche à aucun de ces quatre domaines. **Un avis d'advisor suffit donc, l'orchestrateur adjuge et écrit** (docs/13 §7 par FZ-e, ligne datée de DECISIONS) ; aucun acte de l'investisseur n'est requis. Deux conditions : (i) la « ratification mainteneur due (C-10) » de JOURNAL l.122 est soldée par cette voie, en le disant explicitement dans l'adjudication (je n'ai pas lu le cp-1 qui porte C-10 ; si son texte exige une signature du mainteneur, l'orchestrateur consigne la substitution comme écart déclaré, appuyé sur JOURNAL l.143) ; (ii) une ligne d'information à l'investisseur dans le point d'étape (comme la réserve R-3 de B.72), sans attente.

## Q-7 — seuil à l'instrument de libFuzzer ?

**Faits.** À libFuzzer (compteurs 8 bits, binaire nightly avec assertions de débogage), la famille couvre ≈ 55,6 % de l'apport du dérivé (RAPPORT §2.2, O-1) ; docs/13 l.195 fixe « au même outillage de mesure », et l'outillage de la mesure d'origine est afl-showmap (JOURNAL l.122).

**Options.** (a) exiger la fraction aux deux instruments ; (b) écrire la différence comme observation, un seul instrument de référence ; (c) former un item nommé à déclencheur.

**Recommandation : (b), complétée par (c).** Motifs : la règle écrite n'a qu'un instrument ; un second critère serait une exigence nouvelle, hors du G0 du lot (annexe A l.59) — elle passerait par un amendement de docs/13 §7, pas par la revue d'un lot (G0, R-25) ; les deux instruments ne mesurent pas la même chose (arêtes AFL contre « features » arête × tranche de compteur, binaire et profil différents), donc 55,6 % et 66,95 % ne sont pas comparables terme à terme et « sous 471/789 » n'a pas de sens établi à cet instrument. Écrire O-1 avec ses chiffres et cette explication au README du corpus et dans FZ-e, pour qu'un lecteur ne lise pas 55,6 % comme un échec. Item (c) : « SHOGEN-FUZZ-DISTILLATION-LIBFUZZER-1 : distillation complémentaire à l'instrument de libFuzzer (`-merge=1` outillé, 378 arêtes neuves du dérivé, RAPPORT Q-7) ; déclencheur : amendement de docs/13 §7 posant un critère à deux instruments, ou libFuzzer devenant l'outil de référence ; propriétaire orch. » — ce n'est pas une dette (aucune exigence écrite n'est manquée), c'est une porte nommée, conforme à la règle « aucune dette ».

**Risque si (a) était retenu** : un lot de distillation de plus avant la G2, sans règle écrite pour le fonder, et un seuil à libFuzzer qui dépendrait de la nightly épinglée (`fuzz/README.md` l.13) — une seconde référence datée à entretenir.

## Résumé

- Q-2 : fraction 471/789 appliquée à E (= 642 sur la référence `c1122de`) ; seuil dérivé de E mesuré dès que C-2 est en place ; jamais abaissé (L-3) ; avis d'advisor + adjudication de l'orchestrateur suffisent (JOURNAL l.143, l.450), investisseur informé d'une ligne, C-10 soldé explicitement.
- Q-7 : pas de second seuil ; observation O-1 écrite avec ses chiffres et le motif de non-comparabilité ; item à déclencheur nommé.
