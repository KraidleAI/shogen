# Contrôles de l'orchestrateur — lot GEL-COLLECTEUR-1 (2026-10-18 03:27:51 UTC, `date -u`)

| agent | rôle | Gate 0 (champ model, grep -o sur le transcript) | FM-1.1 (fm11.py versé) |
|---|---|---|---|
| générateur (worker) | GEL-1 à GEL-9, corrections C-1, C-2 | claude-opus-5-5, 437 occurrences, aucune autre | fragments_l51_l14 : resultats 0, entrees 0 ; 950 événements |
| lecteur DNS | noms témoins de D-5 | claude-sonnet-5-5, 45 occurrences, aucune autre | fragments_l51_l14 : resultats 0, entrees 0 ; 108 événements |
| advisor | Q-A, Q-B, Q-C | claude-fable-5-1, 37 occurrences, aucune autre | fragments_l51_l14 : resultats 0, entrees 0 ; 78 événements |

SHA256SUMS du générateur : vérifié (`sha256sum -c`, toutes les lignes OK). Aucun diff ne nomme FreeTSA (grep -ci : 0 pour les neuf). Réviseur G2 : en cours (contrôles ajoutés à son rendu).

| réviseur G2 | relecture des neuf diffs, C-3, C-4 | claude-opus-5-5, 306 occurrences, aucune autre | fragments_l51_l14 : resultats 0, entrees 0 ; 651 événements |

SHA256SUMS de la G2 : 79 lignes OK, 0 écart. Adjudication de la G2 (2026-10-18 05:14:09 UTC) : C-3 et C-4 adoptés tels quels ; I-1 → correction C-5 (boucle, avant le gel) ; I-2 → correction C-6 (remplaçants de Binance à la carte) ; Q-1 → texte du paquet ; Q-2 ratifié ; I-3 → texte d'item TSA-CERTIGNA-1 au versement ; E-7 (oracle_record) : non applicable à S2-bis (chemin cp-2 de S2). Brief : BRIEF-GEL-CORR2.md.
`06:19:45`Z preflight : serie de 13 diffs appliquee sur 1d7e5d4, runner 153 ok, s2bis conforme Ran = 443

2026-10-18 07:14:46 UTC — Relecture G2 de C-5 et C-6 : ACCEPTE-AVEC-CORRECTIONS (C-7, adopté tel quel) ; SHA256SUMS de la G2 : 0 écart. I-4 (éviction par un observateur de la liste posant des journaux inventés) → correction C-8 (liste fermée des journaux pool, secondaire), brief BRIEF-GEL-CORR3.md ; I-5 → item SHOGEN-S2BIS-CARTE-REMPLACANTS-RECALC-1 formé au versement (déclencheur G0 de RB-2) ; E-8 de la G2 (git diff --name-only sur dossiers nommés) : noté, sans effet.

2026-10-18 08:45:47 UTC — Relecture G2 de C-8 : ACCEPTE-AVEC-CORRECTIONS (C-9, adopté tel quel) ; espion de `lier` admis par la G2 (liaison réelle prouvée ailleurs, mutants T-03, T-04 tués) ; SHA256SUMS de la G2 : 0 écart. I-6 → C-10 (tête du journal secondaire exportée, ferme SHOGEN-S2BIS-TETE-SECONDAIRE-1) ; I-7 → C-11 (test déterministe) ; brief BRIEF-GEL-CORR4.md. Série prévue : dix-huit pas.
2026-10-18 11:10:18 UTC — incident : conteneur redémarré vers `11:08` UTC (uptime 103 s à `11:09:43`), chaîne lancée à `10:41:08` UTC tuée pendant le pas GEL-1 (journal : ligne PID seule, aucun commit) ; arbre restauré (git restore --staged --worktree, 0 ligne, aucun fichier non suivi) ; relance de la chaîne après rejeu du contrôle préalable.
2026-10-18 11:47:53 UTC — incident 2 : conteneur redémarré de nouveau vers `11:46:50` UTC (uptime 33 s à `11:47:26`), au réveil du point de contrôle programmé ; la chaîne relancée à `11:16:12` est morte pendant GEL-1 sans commit ; arbre restauré. Cause retenue : le conteneur est récupéré quand la session est inactive ; la chaîne doit tourner pendant que la session reste active (surveillance en premier plan, aucun arrêt de tour avant la fin de la chaîne).
2026-10-18 13:27:20 UTC — chaîne arrêtée à GEL-9 par la gate C4 (heure sans date « 00:00 » au FORMAT l.785, E14) après six commits (GEL-1 à GEL-6, GEL-7, GEL-8 : huit pas commis a30e25c..6844047) ; retouches de l'orchestrateur (E35) sur les diffs non commis : GEL-9 et C-6 « à 00:00 UTC » → « à minuit UTC » (FORMAT et commentaire de carte.json de test), C-10 docstring « 22:59 » mis en code, C-12 contexte aligné ; contrôle C4 des ajouts de tous les diffs : aucune faute ; préflight sur clone : série appliquée et job s2bis rejoué.
