# Partie 2 de S2 — G0 courts par étape (orchestrateur de la session cloud)

Rattachement : `docs/adr-0028/PLAN-PARTIE-2.md` ; ADR-0028 annexes A, B, D ; méthode `docs/METHODE-PARTIES.md`
(un G0 court par lot : fichiers, tests, risques). Chaque section est datée ; une section écrite ne se réécrit pas.

## P0 — SHOGEN-ORACLE-PERIMETRE-1 (i) : S-G4 et S-G5 sur `s2-harness/**/*.md` (2026-10-02 02:5x UTC)

- **Source** : annexe B l.188 (item, échéance « (i) avant le G0 du lot RENDU-1 ») ; origine C-1 et C-9 b du G2 de
  DOCS-S2 (`docs/G1-lot-DOCS-S2.md` l.90 : S-G4/S-G5 ne lisent que `docs/**/*.md`) ; doctrine des gates ADR-0013
  (une gate imprime sa couverture ; aucun vert sans mutant semé) ; `.claude/agents/shogen-devops.md` §2.
- **Fichiers** : `xtask/src/sg4.rs`, `xtask/src/sg5.rs` (périmètre : `docs/**/*.md` puis `s2-harness/**/*.md`,
  couverture imprimée pour les deux) ; `xtask/tests/mutants.rs` (arbres de fixture, mutants neufs) ; au besoin
  `s2-harness/README.md` et `RUNBOOK-campagne.md` si la gate étendue y trouve une violation (correction du texte,
  jamais de la gate).
- **Tests** : (1) mutant S-G4 : locution interdite dans un `.md` de `s2-harness/` ⇒ S-G4 ROUGE ; (2) mutant S-G5 :
  citation anglaise hors corpus dans un `.md` de `s2-harness/` ⇒ S-G5 ROUGE ; (3) les témoins verts existants
  restent verts ; (4) `cargo --locked xtask verify` VERT sur l'arbre réel, couverture S-G4/S-G5 = fichiers de
  `docs/` + 2 fichiers de `s2-harness/`.
- **Risques** : (a) `fichiers_par_extension` refuse de conclure sur un répertoire absent ou vide : les arbres de
  fixture des mutants documentaires n'ont que `docs/` ; ils doivent recevoir un `s2-harness/` synthétique, sans
  affaiblir le refus ; (b) la recherche est récursive sur le disque, pas sur l'index git : un `.md` non suivi sous
  `s2-harness/` (environnement virtuel, cache) entrerait au périmètre, à constater et à déclarer, jamais à
  exclure par nom choisi par le fichier ; (c) S-G5 en régime partiel en session cloud (biblio absente) : les
  citations de `s2-harness/` sont listées « non contrôlées » ; le rejeu en corpus complet relève de (ii) ;
  (d) S-G4 exempte seulement `docs/09-vocabulaire.md` ; aucune exemption neuve.
- **Taille** : ≈ 15 lignes de code, ≈ 60 de tests [inféré]. Un commit (R-25).
- **G1** : worker `shogen-worker` (`claude-opus-5-5`, effort `max`). Gate 0 : modèle résolu déclaré par le worker.
