# G0 du lot PLAN-S2BIS (données de S2 pour la préparation de S2-bis)

Écrit par l'orchestrateur le 2026-10-04 à 14:55:41 UTC (`date -u`). Rattachement : ADR-0029 révision 3, acceptée (§2.6 TAU-SIGMA-S2BIS ;
§6 lot 3) ; G0 de vague `docs/adr-0029/G0-lots-S2BIS.md` ; annexe B d'ADR-0028 (items SHOGEN-TAU-REDERIV-1, SHOGEN-R1-HOTE-STRUCTUREL-1,
SHOGEN-POSTPREREG-PARAMS-SCEAU-1, SHOGEN-FICHE-WORKER-POSTEXEC-1).

**Objet** : trois sorties calculées sur les journaux scellés de S2 (segment J28, exclusion D5), **toutes sur une extraction du commit
d'analyse `f35a70c`** (conséquence E-8), qui réutilisent les lecteurs du harnais en import, sans modifier `s2-harness` :
1. **TAU-SIGMA-S2BIS** (BTC/USD seul) : τ_c et σ_c par classe de source, selon la règle écrite à l'ADR-0029 §2.6 (population : cellules
   arrivées à l'axe (i) sous le σ de S2, recalculées sur le pool D1-bis de 10 hôtes, sans `okx_index`, Pyth exclu ; τ_c =
   grid-ceil(1,5 × max_s P99,9_{c,s}, 0,05 %), borné par 0,05 % ≤ τ_c < 2,85 % ; σ_c = max(plancher, 3 × P99 staleness), planchers
   d'ADR-0020). Valeurs **destinées au paquet de S2-bis**, jamais re-réglées ensuite.
2. **Épisodes** : distributions des longueurs d'épisodes de panne et d'écart par source, et courbe FIV_série(ℓ), pour calibrer
   SIM-NIVEAU-BIS et SIM-PUISSANCE-BIS.
3. **OKX** : mesure descriptive de la contribution de la paire de flux OKX à K de S2 (SHOGEN-R1-HOTE-STRUCTUREL-1).

**Règles** (reprises du lot POST-PREREG et des items B.50) :
- exception à la consigne « fixtures seulement » de la fiche worker, accordée par ce G0 : les **scripts du lot**, et eux seuls, lisent
  les journaux scellés de la session ; personne n'affiche un journal ; sha256 des journaux contrôlés contre le bloc machine du paquet
  de S2 avant usage ;
- **paramètres et code épinglés avant l'exécution** (SHOGEN-POSTPREREG-PARAMS-SCEAU-1) : le worker remet à l'orchestrateur le sha256 de
  ses scripts et de ses paramètres ; l'orchestrateur l'inscrit au JOURNAL ; **alors seulement** les scripts tournent sur les journaux ;
- tests sur fixtures d'abord (rouge avant, vert après), mutants ; contrôle de cohérence : n, K et P̂_more par strate recomptés égaux au
  bloc 3 du rendu J28 ;
- chaque sortie porte en tête : « préparation de S2-bis ; ne change pas le verdict de S2 (« R1 discrimine » = FAUX) » ;
- G1 journal de provenance ; G2 relecture neuve ; R-25, R-13, R-8 ; seul l'orchestrateur committe.

**Sorties** : `scripts/plan-s2bis/` (code et tests), `docs/adr-0029/plan-s2bis/` (sorties et README), journal G1.
