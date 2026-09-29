# Shogen — instructions Claude

## Référentiel qualité (obligatoire, non discrétionnaire — 2026-08-12)
Ce dépôt est régi par le corpus « Compliance et ingénierie logicielle et architecturale »
(C:\Users\KACIMI\compiliance et ingénierie locielle et architecturale\docs\) :
- doc 02 : gates **G0–G7 bloquants** et règles R-1..R-26 (R-26 advisor,
  ajoutée le 2026-08-12 — ligne mise au courant le 2026-08-13, ordre de
  conformité mainteneur ; la mention équivalente du CLAUDE.md global
  appartient au mainteneur) ;
- doc 03 : méthodologie de passe (sources avant travail, niveaux [lu]/[abs]/[2nd], clôture zéro dette).

Conséquences opérationnelles :
1. Aucun code sans spec/ADR de rattachement (G0).
2. Artefacts générés : journal de provenance (G1) ; revue 100 % avec la checklist G2 du corpus,
   réviseur ≠ générateur (G2).
3. CI à instancier depuis templates/ci-gates.yml du corpus : jobs bloquants (G3/G4/G6).
4. PR petites et unitaires (R-25). TODO/FIXME nus interdits (R-13).
5. Dépendance nouvelle : vérification registre AVANT installation (R-8).
6. Clôture de passe : rapport-de-passe du corpus, section dettes vide ou en PR-x/recherches (G5).
7. Roster (mainteneur 2026-08-14, ADR-0019 ; réversion des efforts 2026-09-16 ; **décision investisseur
   2026-09-22, décision 133 MONARK : workers, chercheurs et lecteurs sous Opus 5.5**) : workers
   **`claude-opus-5-5` épinglés, effort `max` EXPLICITE** (effort par défaut du modèle = medium) ;
   chercheurs/lecteurs **`claude-sonnet-5-5`, effort `high`** (décisions 267/280, 2026-09-28 ; `claude-opus-5-5`
   admis en lecture quand la synthèse exige du jugement) ; orchestrateur/planificateur
   **`claude-fable-5-1`, effort `high`** ; advisors Fable 5.1 effort `medium` (amendement 2026-09-18) ;
   validateur-humain Fable 5.1 effort `high`. Frontmatters `.claude/agents/shogen-devops.md`
   (`claude-opus-5-5`, max) et `shogen-orchestrator.md` (`claude-fable-5-1`, high) alignés le 2026-09-26 ;
   prise d'effet au redémarrage de session. **`claude-opus-5` est banni** ; jamais un tier `opus` ou
   `fable` nu dans le champ `model`. Connecteur Firecrawl : UUID `1e993196-5288-40f1-bf6f-0cb66830757d` (2026-09-28)
   (vérifier par `ToolSearch firecrawl` avant tout lancement, il change à chaque bascule de compte).
   Gate 0 (contrôle du modèle résolu, préfixe `claude-opus-5-5`) au premier worker de chaque passe.
   Seul l'orchestrateur committe (R-19/R-20).
8. Audit d'entrée : fait le 2026-08-12 (docs/AUDIT-ENTREE.md, commit 10e5557) ; son rafraîchissement
   (état S2/S3 réel) est porté par la cartographie du 2026-09-29 (docs/rapports/cartographie-2026-09-29.md).
