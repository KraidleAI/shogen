# Journal de provenance — Shōgen

Exigence : P4/R-9 (référentiel doc 02) ; assise : NIST SSDF 800-218/218A,
AI Act, CRA. Une entrée par commit contenant du code généré. Un artefact
sans entrée ne s'intègre pas. *(Instancié le 2026-08-13 — fermeture de
l'écart G1 de l'audit d'entrée du 2026-08-12 ; les commits de code
antérieurs à l'instanciation sont reconstitués depuis JOURNAL.md et les
rapports de passe, qui portaient déjà ces faits en prose.)*

| Date | PR/commit | Modèle (identifiant épinglé exact) | Effort | Contexte fourni (résumé/lien) | Générateur (agent) | Réviseur | Verdict G2 |
|---|---|---|---|---|---|---|---|
| 2026-08-12 | `91c4524` | claude-opus-5 (variante de service `[1m]` constatée, 12 §6.2) | high | conception 12 §5 (walking skeleton), ADR-0009..0013 | worker `shogen-devops` | orchestrateur (Fable 5) — rejeu intégral, gates vues vertes, 13 mutants vus tués | approuvé |
| 2026-08-12 | `849ac4a` | claude-fable-5 (orchestrateur générateur — unité de son propre périmètre, 12 §10 item 2) | high | DEVOPS §3, ADR-0013, dette 12 §10 item 2 | orchestrateur | worker G2 via l'outil Agent, **tier nu `opus` — écart runtime consigné au verdict G7 du 2026-08-13** ; verdict « accepter avec corrections », bloquante + majeures 2-5 fermées le jour même | approuvé après corrections |
| 2026-08-13 | `f59083a` | claude-opus-5 | high | ADR-0012 D6, mission C2 (run `wf_8cace7eb-746`) | worker C2 (devops) | orchestrateur — lecture intégrale des 3 modules + rejeu double-build sur la cible ratifiée (VERT, empreintes identiques) | approuvé |
| 2026-08-13 | `fbe45fc` | claude-opus-5 (workers) + claude-fable-5 (corrections d'adjudication) | high | 03 §1, ADR-0016/0018/0005, missions C1 + reprise (run `wf_8cace7eb-746`) | workers C1 (mort en séance) + C1-reprise ; orchestrateur (corrections F1-F8) | worker G2 via Workflow, **claude-opus-5 épinglé** (run `wf_7ad25f82-267`) — « accepter avec corrections », R-5 cryptographique conforme (64/64 constantes contre la pièce FIPS, balayage indépendant 0..600) | approuvé après corrections (8/8 appliquées) |
