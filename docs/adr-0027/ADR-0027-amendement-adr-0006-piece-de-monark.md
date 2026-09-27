# ADR-0027 — Amendement d'ADR-0006 : Shōgen est une pièce de MONARK, sans jeton propre ; la neutralité D11 s'applique à MONARK entier (décision investisseur 230)

- **Statut** : **G0 proposé** (rédigé par l'orchestrateur MONARK `claude-fable-5-1`, session « POKT X SHOGEN », 2026-09-27 01:3x UTC). Porte la **décision investisseur 230** (2026-09-26 15:4x UTC, verbatim : « shogen est une pièce dans monark, pas de jeton »). À approuver au checkpoint-1 (validateur-humain). Solde l'item **SHOGEN-ADR-0006-AMEND-1** (doc 15 §4 ligne 16 : contradiction ADR-0006 / registre MONARK).
- **Rattachement** : ADR-0006 (« Aucun token, jamais — sur ce projet comme sur ses frères », 2026-07-30, mainteneur) ; ADR-0019 D11 (neutralité : aucun revenu du mesuré) ; 05-roadmap l.250 (« Pas de token — jamais, sur ce projet comme sur ses frères ») ; 07-gtm §4 (moat = tiers neutre) ; README MONARK « single token, single ticker » [lu par le chercheur *shogen-interne*, SI-10/SI-11] ; doc 15 §1, §4 l.16, §9.6.

## Contexte — la contradiction consolidée

ADR-0006 pt 1 écrit « aucun token, jamais — sur ce projet comme sur ses **frères** ». Le registre MONARK déclare un jeton unique au niveau de la compagnie et présente Shōgen comme une pièce « built » de MONARK. Trois archives de l'étude Pocket (shogen-interne 7-3, juridique X-10, SI-10/SI-11) ont relevé la contradiction ; le doc 15 la porte en §4 ligne 16, tranchée par la décision 230 : **le proposant est MONARK ; Shōgen y est une pièce ; le seul jeton est MONARK**.

## Décision (proposée)

1. **ADR-0006 pt 1 est amendé** : « **Shōgen ne porte aucun jeton propre**, jamais. Shōgen est une pièce de MONARK ; l'unique jeton est celui de MONARK (niveau compagnie), décision investisseur 230. » La clause « sur ce projet comme sur ses frères » est **retirée** (elle prétendait lier des projets frères que cette ADR n'a pas autorité à lier ; la décision de la compagnie prime).
2. **ADR-0006 pt 2, pt 3, pt 4 sont inchangés** : aucun calcul on-chain ; ancrage = engagement, jamais affirmation ; « publier k_eff comme valeur à croire » reste interdit. Un jeton MONARK ne change rien à ces invariants : ce qui irait sur une chaîne resterait un engagement (hash), jamais une valeur.
3. **L'argument du moat est reformulé, pas abandonné** (ADR-0006 « Alternative considérée » ; 07-gtm §4) : la neutralité qui vaut n'est pas « aucun jeton nulle part », c'est **« aucun intérêt dans le résultat de la mesure »**. Elle se traduit par la règle **D11 étendue à MONARK entier** : aucun revenu venant d'un mesuré (Pocket ou autre) tant qu'une mesure de ce mesuré est publiée par une pièce de MONARK ; ni détention, ni stake, ni app stake, ni part « source owner » d'un réseau mesuré (doc 15 §7 P-3/P-4, S-8 ; §9.6). Un jeton MONARK n'est pas un jeton du mesuré : il n'entre pas dans D11, **sauf** si une pièce de MONARK venait à mesurer MONARK lui-même (auto-mesure interdite : hors périmètre, à écrire si le cas se présentait).
4. **Ce que Shōgen dit de lui-même** (09-vocabulaire, phrases publiques) : « Shōgen, la pièce d'attestation et de certificat de diversité de MONARK » ; **jamais** « le jeton Shōgen », « Shōgen DAO », « staker Shōgen ». Le nom Shōgen reste celui de la pièce (crates, docs, dépôt privé).
5. **Registres à porter** (même lot, après checkpoint-1) : DECISIONS.md (ligne d'index ADR-0006 : « amendée par ADR-0027 le … » ; bloc ADR-0006 : note d'amendement datée en tête, texte d'origine conservé) ; 05-roadmap l.250 ; 07-gtm §4 (une phrase : la neutralité se définit par D11, pas par l'absence de jeton) ; 08-assumptions si une hypothèse cite « pas de token » ; doc 15 §4 l.16 (renvoi à cette ADR).

## Alternatives écartées

- **Laisser ADR-0006 tel quel et n'amender que la roadmap** : la contradiction resterait dans le registre des décisions, qui fait foi ; trois lecteurs indépendants l'ont relevée.
- **Réécrire ADR-0006 en place** : interdit par la discipline du registre (une ADR acceptée ne se réécrit pas ; elle s'amende par ADR datée).

## Ce que la décision coûte

Rien en code. Une reformulation du moat dans le GTM ; l'obligation, désormais explicite, que D11 soit vérifiée au niveau **MONARK** (trésorerie, stakes, revenus) et non seulement au niveau de la pièce — ce qui relève de l'investisseur (entité non constituée, P-1) et n'est pas une pièce logicielle.

## Provenance

Décision 230 (CHANTIERS MONARK 2026-09-26 15:4x UTC, verbatim) ; ADR-0006 lu le 27/09 01:1x UTC (DECISIONS.md l.293-…) ; 05-roadmap l.250 ; doc 15 §1, §4 l.16, §7, §9.6 (sha `ae227cf8…` avant addendum). Advisor intégré indisponible dans la session de rédaction (consigné).
