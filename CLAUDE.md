# Shogen — instructions Claude

> **SESSION CLOUD OU NOUVELLE SESSION : lis d'abord `docs/PASSATION-CLOUD.md`** (passation du 2026-10-02 :
> état exact, où reprendre — la partie 2 de S2 —, règles autosuffisantes, ce qui n'existe que sur le poste local).

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
   **Haiku 5.5** (décision du fondateur transmise par MONARK le 2026-10-08 : « oui, on adopte, pour tous les
   claudes, recherches et paroxysme compris ») : `claude-haiku-5-5`, effort `high` toujours écrit (défaut du
   modèle = medium), **rôles de signal seulement** : extracteur (ce qu'une pièce demande, ses verdicts, ses
   constats), trieur de veille (annote, ne retire jamais), relevé ciblé (une ligne ou un chiffre dans un document
   déjà identifié), greffier (premier jet d'une ligne de journal ou de tableau). Sa sortie est un signal, jamais
   une preuve : chaque citation contrôlée par script, mot pour mot et dans le bon fichier ; la source relue avant
   tout acte ; un « rien trouvé » ne prouve pas une absence. **Jamais** en G2, G7, validation, prover, red team,
   advisor, lecture qui fait preuve, ni décision ; pas de rôle mémoire. Doctrine Knight et Leveson : Haiku est de
   la même famille que Sonnet, Opus et Fable, il ne compte jamais comme version indépendante d'un autre Claude
   (quorum, diversité, réviseur ≠ générateur). Fiche `shogen-extracteur` posée par le lot LINT-HAIKU (la liste
   blanche du lint R-1, `enforcement/lint-model-pinning.sh`, se change par un lot) ; appels directs à
   l'API par la clé `SHOGEN_ANTHROPIC_API_KEY` de l'environnement cloud (organisation Console du fondateur), jamais
   affichée, écrite ni commitée ; Gate 0 sur le champ `model` de la réponse (premier appel le 2026-10-08 :
   `claude-haiku-5-5`).
   Seul l'orchestrateur committe (R-19/R-20).
8. Audit d'entrée : fait le 2026-08-12 (docs/AUDIT-ENTREE.md, commit 10e5557) ; son rafraîchissement
   (état S2/S3 réel) est porté par la cartographie du 2026-09-29 (docs/rapports/cartographie-2026-09-29.md).
