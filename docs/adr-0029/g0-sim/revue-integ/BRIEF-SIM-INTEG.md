# Brief — SIM-BIS, diff d'intégration des sorties de PLAN-S2BIS-2 (C1 mesurée, masque de J28, retrait de `e1.ell_c1`, bord de la grille)

Worker `shogen-worker`, effort max. Dépôt `/home/user/shogen` en lecture seule (`git --no-optional-locks`), **aucune écriture git**. `date -u` avant toute date. Dossier : `<scratchpad>/s2bis/sim5/` (scratchpad = `<scratchpad>`), `TMPDIR` dédié, `NOTES.md` tenu (reprise depuis lui, jamais depuis un `.jsonl`).

## Contrat (lis-le d'abord)
- **Ta spécification : l'ajout daté du 2026-10-05 15:05:43 UTC à la fin de `docs/adr-0029/g0-sim/G0-SIM-BIS.md`** (points (1) à (9), précision d'adjudication à (8) comprise), et le G0 `docs/adr-0029/g0-plan2/G0-PLAN-S2BIS-2.md`, adjudication 5 (« diff d'intégration côté SIM-BIS : nouvelle règle de C1, masque mesuré, retrait de `e1.ell_c1` ; sa relecture G2 ; E0 attend »).
- Le reste du G0 de SIM-BIS, sa `PROPOSITION.md` (E-S-37, E-S-38, §3) et son `AVIS.md`, en lecture ciblée ; ADR-0029 et ses ajouts datés, en lecture ciblée.
- **Entrées versées, à lire par empreinte contrôlée** : `docs/adr-0029/plan-s2bis-2/` (`fiv_unites.txt`, `masque_j28.txt`, `intervalles.txt`, `SHA256SUMS`, `README.md`) et EP `docs/adr-0029/plan-s2bis/`.
- Code : `scripts/sim-bis/` (lis ce que tu touches en entier) ; la suite `scripts/sim-bis/tests/` et la ligne du job `sim-bis-unittest` de `.github/workflows/gates.yml` (plancher actuel 172).
- Items à lire dans `docs/adr-0028/ANNEXE-B-items.md`, par leur nom seulement : SHOGEN-SIM-BIS-FIV-IDENTIF-1, SHOGEN-SIM-BIS-REGIME-FAISABILITE-1, SHOGEN-SIM-BIS-SB11-BRIEF-1, SHOGEN-SIM-BIS-SB11-IMPRESSIONS-1.

## Base
Tête **b46672b** de `claude/compassionate-noether-szmdyj` (`git archive`, exclusions habituelles : `docs/rapports`, `docs/adr-0025`, `docs/adr-0028/monark-m009a`, `docs/adr-0028/execution`, `docs/15-*`, `docs/16-*`, `docs/pocket-report`).

## Périmètre (liste fermée)
1. **C1 selon (1)** : sélection, dans chaque strate, du point de la grille d'E1 qui minimise Q₁, aux hôtes et aux ℓ que (1) définit, F_u(ℓ) lu dans `fiv_unites.txt` en rationnel exact, F̄_u,p(ℓ) exact sur les réplications définies parmi les 200 de C2, logarithmes par `Decimal.ln` sous le contexte de r1, égalités départagées comme écrit, point à F̄ indéfini écarté. La convention « milieu des logs de C0 et de C2 à ℓ = 240 » est retirée.
2. **Calendrier d'E1 selon (3)** : masque de `masque_j28.txt`, empreinte contrôlée, appliqué après génération, pour C0, C1 et C2 ; E2 et E3 inchangés.
3. **Retrait de `e1.ell_c1`** de `scripts/sim-bis/parametres.json` (7), et de toute lecture de cette clé.
4. **Bord de la grille selon (8)** : constat par le script, ligne nommée par strate (nombre d'hôtes qui satisfont la condition, liste des ℓ retenus ≥ 60, coordonnée extrême le cas échéant) ; aucune seconde sélection.
5. Hors périmètre, à ne pas écrire ici : les impressions de (6) qui relèvent de SB-11 (sauf ce que (8)(iv) exige), l'exécution d'E0, toute valeur de durée. Si une ligne de SHOGEN-SIM-BIS-SB11-BRIEF-1 est indispensable au câblage, dis-le en question.
6. Si le contrat est muet, ou contredit le code : question Q-SI-n, avec ton choix et sa raison ; tu ne tranches aucune valeur.

## Règles
- **Tests d'abord**, rouge d'assertion montré ; fixtures synthétiques pour E1 (aucun calcul à l'échelle réelle n'est demandé) ; un test qui fige la lecture des trois sorties de PLAN-S2BIS-2 par leur empreinte.
- Diffs en série **SB-15a, SB-15b…**, chacun ≤ 200 lignes de code ajoutées ; plancher de la suite sim-bis recalé exactement dans `gates.yml` (`--plancher`), METRIQUES par diff si la forme du dépôt l'exige.
- Au moins 10 mutants par diff, classés par la commande du job sim-bis (borne 300 s, dépassement FATAL).
- Bibliothèque standard seule ; Python 3.11 à 3.13 en `-X dev -W error` (3.10 : dis ce qui se passe) ; critère de vert : code 0 et aucune ligne « Exception ignored » ni « Warning ».
- R-13, R-8, octets 92 comptés juste, lignes ≤ 120 caractères. Réseau isolé (`<scratchpad>/s2bis/p1b/g2/travail/outils/isole.sh`). Avant livraison : runner, jobs s2bis, S2 et sim-bis aux planchers exacts, `cargo --locked xtask verify` sur la copie (lignes de verdict seules ; S-G9 `docs/17:70` connu sur copie).

## Interdits (durs)
Aucun journal réel de S2 ni de S2-bis ; ne jamais poser `SHOGEN_S2_CAMPAGNE_CONTROL` ; `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ; tout `*.jsonl` ; toute pièce de D.2 ; toute recherche ou énumération récursive (grep -r, git grep, git ls-tree -r, du, find large) sur `docs/`, le dépôt entier ou le scratchpad entier ; aucun fichier sous un `.claude/` du dépôt réel ; rien sur Pocket.

## Rendu
Rapport final par message (ta valeur de retour), en français, Gate 0 (identifiant exact du modèle) en tête : diffs (sha256, lignes ajoutées), tableau des points (1), (3), (7), (8) avec fichier:ligne et test, mutants, matrice, planchers, questions Q-SI-n, écarts, items à former. Écris-le aussi dans `<scratchpad>/s2bis/sim5/RAPPORT-GENERATEUR.md`, couvert par ton `SHA256SUMS`.
