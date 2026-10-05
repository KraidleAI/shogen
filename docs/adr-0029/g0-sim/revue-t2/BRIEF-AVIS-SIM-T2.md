# Brief — avis de l'advisor sur les douze questions de conception de la couche des sources (SIM-BIS, tranche 2)

Advisor `shogen-advisor` (Fable 5.1, effort medium). Tu n'agis pas, tu ne modifies rien hors de ta sortie. Tu écris seulement
`<scratchpad>/s2bis/sim2/g2/AVIS-SIM-T2.md`.

Pièce : `…/sim2/g2/RAPPORT-WORKER-SIM-T2-transcrit.md` (questions Q-T2-1 à Q-T2-12 et items proposés). Rattachements :
`docs/adr-0029/g0-sim/G0-SIM-BIS.md` (avec ses ajouts datés), `PROPOSITION.md` (§2.2 à §2.4, §5), `AVIS.md` (ton avis précédent) ;
ADR-0029 §2.4 et §2.7 ; `docs/adr-0029/AVIS-STATS.md` ; `docs/adr-0029/plan-s2bis/episodes.txt` (EP). Tu peux lire le code livré
(`…/sim2/etapes-784ebd2/rb4b/scripts/sim-bis/sources.py`) pour juger une question.

Pour chaque question : adopter le choix du worker, le modifier (comment, pourquoi) ou le rejeter ; marque **[G0]** ce qui change la
lettre du G0 et **[E0]** ce qui doit être scellé avant E0. Points d'attention : Q-T2-1 (indépendance par strate : effet sur le niveau
et la puissance, en particulier sur la statistique K et les runs), Q-T2-2 (E′ indépendante fenêtre par fenêtre contre le groupement
FIV mesuré sur S2 : la calibration C0/C1/C2 garde-t-elle son sens ?), Q-T2-4 (classes de même taux que BTC, réalisation indépendante),
Q-T2-6 (valeurs non fixées par le G0 : propose des valeurs et leur source), Q-T2-11 (indice de flux positionnel ou par nom), Q-T2-12
(budget de calcul). Puis les items proposés et trois risques. Vocabulaire du registre 09. Interdits : `docs/15-*`, `docs/16-*`,
`docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/`, tout `*.jsonl`,
toute pièce de D.2. Gate 0 (identifiant exact et effort en tête). Résumé court en français.
