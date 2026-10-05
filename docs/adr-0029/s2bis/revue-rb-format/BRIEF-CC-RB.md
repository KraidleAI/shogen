# Brief — contre-contrôle bref des corrections de RB-1 (RB-1h..k) et RB-18 (RB-18a..i), et banc de concordance rejoué (critère C-13)

Réviseur `shogen-worker` (relecture, effort max), qui n'a écrit ni RB-1 ni RB-18. Dépôt en lecture seule (`git --no-optional-locks`), aucune écriture git. `date -u` avant toute date. Dossier : `<scratchpad>/s2bis/rb18/cc/` (scratchpad = `<scratchpad>`), TMPDIR dédié, NOTES.md tenu (reprise depuis lui, jamais depuis un `.jsonl`). **Budget de calcul presque épuisé : contrôle bref et ciblé, pas de nouvelle G2.**

## Base et diffs
- Tête **47b2177** ; série recalée commune dans `<scratchpad>/rebase-t5/diffs/` (SHA256SUMS 2d2c7852…), dans l'ordre : CB-19a..h (P1, contrôlée par un autre réviseur, à appliquer seulement), RB-1h..k (plancher +19), RB-18a..i (plancher +30) ; état final : suite s2bis Ran 254, runner 87 ok (mesuré par l'orchestrateur). Outil de recalage : `<scratchpad>/rebase-t5/rebaser_t5.py` (lignes +/- identiques aux originaux, plancher décalé).
- Rapports transcrits (FM-1.1 : 0) : `<scratchpad>/s2bis/rb1/corr2/RAPPORT-CORRECTIONS-RB1-FORMAT-transcrit.md`, `<scratchpad>/s2bis/rb18/corr/RAPPORT-CORRECTIONS-RB18-transcrit.md` ; preuves dans leurs dossiers.
- Lettre : FORMAT de la tête `docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md` ; adjudication `<scratchpad>/s2bis/rb18/g2/ADJUDICATION-FORMAT.md` ; relecture G2 de RB-18 et son banc : `<scratchpad>/s2bis/rb18/g2/` (G2-RB18-transcrit.md §4 et §6, `outils/banc_concordance.py`, `rejouer_banc.sh`, `aligner.py`).

## Adjudications de l'orchestrateur
- RB-1 Q-1 à Q-7 : choix du worker adoptés. RB-18 Q-R18-9 à Q-R18-15 : adoptés (C-6 : « non intègre », lettre du §7.1 d). Q-R18-17 : la borne de 200 porte sur les lignes de code ; RB-18b (199) tient.
- **Critère du banc (I-2 de RB-1)** : 0 discordance sur les verdicts et les sorties (flux des enregistrements intègres, positions, queues rendues, ruptures et leur type, queue finale, tête, refus) ; les **noms de cause** ne sont pas comparés, sauf par une table de correspondance que tu écris si elle est univoque.

## À contrôler
1. Pour chaque lettre C-1 à C-5 et chaque correction C-6 à C-15 : le comportement de RB-1 et de RB-18 suit la lettre (lecture des diffs, quelques sondes ciblées).
2. **Banc rejoué** (outils de la G2) sur l'état final, Python 3.10 et 3.12, familles **régénérées par l'écrivain de l'état final** (y compris CB-19c/d) : 0 discordance au critère ci-dessus ; donne les comptes par famille. Toute discordance : classée (lecteur en défaut, lettre muette) avec un cas minimal.
3. Mutants : rejoue un échantillon d'au moins 10 mutants de chaque worker par la commande du job s2bis (borne 300 s), plus 5 neufs à toi ; tous tués.
4. Indépendance : aucun import croisé (test de frontière vert) ; incidents déclarés des workers sans portée.
5. Forme : octets 92, R-13, ≤ 120 caractères ; xtask (lignes de verdict seules) sur l'état final ; isolement réseau (`<scratchpad>/s2bis/p1b/g2/travail/outils/isole.sh`).

## Interdits
`docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ; tout `*.jsonl` réel ; toute pièce de D.2 ; toute recherche récursive (grep -r, git grep, du, find large) sur `docs/`, sur le dépôt entier ou sur le scratchpad entier. PID réels consignés ; nettoyage des copies lourdes à la fin.

Verdict : CONFORME ou NON-CONFORME (liste fermée). Rapport par message, court, en français, Gate 0 en tête, journal G1 et SHA256SUMS de ton dossier.
