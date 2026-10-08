# Brief — cp-1 bref : lettre de l'ajout daté au G0 de SIM-BIS (lot PLAN-S2BIS-2)

Tu es le validateur-humain (`shogen-validateur`, effort high) pour un checkpoint **cp-1 bref**. Il porte sur un seul texte. Tu ne modifies rien : tu écris seulement `<scratchpad>/s2bis/plan2/CP1-AJOUT.md`, et tu rends aussi ton verdict par message.

**Texte à valider** : `…/plan2/LETTRE-AJOUT-G0-SIM.md` (sha256 `01ce4551…`). Cet ajout daté sera inscrit au G0 de SIM-BIS (`docs/adr-0029/g0-sim/G0-SIM-BIS.md`) avant l'inscription au JOURNAL du sha256 du code de PLAN-S2BIS-2. Aucune valeur de FIV_u n'existe encore.

**Rattachements** :
- avis de l'advisor `…/plan2/AVIS-PLAN2.md` (§2 Q-P2-05, 06, 07 ; §3.1 à 3.3), adopté en entier par l'orchestrateur ;
- proposition `…/plan2/PROPOSITION-PLAN2.md` §3.2 ;
- G2 de la tranche 4 de SIM-BIS `…/s2bis/sim4/g2/G2-SIM-T4-transcrit.md` (constat du point 9, point 4) ;
- G0 de SIM-BIS et son AVIS ;
- ADR-0029 l.395-400 ;
- annexe B, bloc B.61 seulement.

**À juger** :
1. Fidélité. Le texte dit-il exactement ce que l'avis adopté demande, sans rien ajouter ni retirer ? Point (5), option (b) modifiée. Point (8), critère de bord mot pour mot. Point (9), filet.
2. Clarté pour un tiers. Chaque règle est-elle constatable par un script, sans lecture humaine ?
3. Cohérence avec la lettre restante du G0 de SIM-BIS et d'E-S-38. Signale toute contradiction.
4. Cas limite que le rédacteur demande de confirmer : si W*(C0) > 16 ≥ W*(C1), on retient 16 semaines, et A-2 est-il posé « sans détour » (AVIS l.60, iv) ?
5. Une décision de valeur se cache-t-elle dans ce texte ? Elle relèverait de l'investisseur : dépense, calendrier annoncé, déclaration publique.

**Verdict** : ACCEPTE, ACCEPTE-AVEC-CORRECTIONS (liste fermée, lettres exactes) ou REFUSE, ou ESCALADE-INVESTISSEUR sur une décision de valeur.

**Interdits** :
- `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ;
- tout `*.jsonl` ;
- toute pièce de D.2 ;
- toute recherche récursive.

Gate 0 : l'identifiant exact du modèle en tête.
