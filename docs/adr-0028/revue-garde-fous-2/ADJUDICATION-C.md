# Adjudication — GARDE-FOUS phase 2, groupe C (orchestrateur, 2026-10-16 02:34:34 UTC, `date -u`)

## Contrôles
- Générateur : 419 champs `model` tous `claude-opus-5-5` ; FM-1.1 = 0 ; SHA256SUMS 51 OK ; P2C-1 à P2C-7 lus.
- G2 neuve (réviseur distinct, reprise après le redémarrage) : 178 champs `model` tous `claude-opus-5-5` ; FM-1.1 = 0 ; SHA256SUMS OK ; verdict **ACCEPTE-AVEC-CORRECTIONS, C-1 à C-4** (texte des ajouts du README seulement ; code, tests, outils à l'octet), série recalée sur `520bb2a` livrée.

## Décisions
1. **C-1 à C-4 adoptées** (planchers : +12 et non +11 ; portée du sceau bornée et forme `source` écrite ; relevé du registre à la tête ; procédure de changement de la vérification du modèle).
2. **Items formés au versement** : FM11-MOTIF-ATTRIBUTION-1, FM11-MOTIF-SORTIE-SCRATCHPAD-1 (faux négatif `scratchpad/../`), GARDE-ATTRIBUTION-PLAGE-LETTRES-1 (faux refus sur `DT15-a à DT15-m`), GARDE-VERIF-MODELE-CHANGE-1, GARDE-CHAINE-ORCH-MODELE-1 (les chaînes de l'orchestrateur n'appellent pas `avant_acte` : hors garde aujourd'hui ; isolement et variables de mandataire à porter au modèle par un diff relu), GARDE-DIFF-SANS-INDEX-1, GARDE-JOURNAL-LECTURE-SEULE-1, GARDE-DISQUE-DU-DEPOT-1 (le disque mesuré est `/`). L'heure sans date de l'annexe B l.1539 : histoire, non touchée.
3. M6-5 et M7-7 équivalents : admis.
4. **Ordre d'intégration des trois groupes : C, puis B, puis A** (D3 de P2A-7 refuserait les fonctions de C non nommées au README si A passait avant ; P2A-4 lit `cibles` que GFB-2 retire : A se recale sur B). Lot INTEGRATION-P2 : worker neuf.
