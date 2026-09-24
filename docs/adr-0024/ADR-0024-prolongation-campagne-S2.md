# ADR-0024 — Prolongation de la campagne S2 jusqu'au lundi 28 septembre 2026 00:00 UTC (n_windows 37 440 → 38 600)

- **Statut** : accepté — décision investisseur « vas y, configure ça » (2026-09-24 18:13 UTC), sur reco de l'orchestrateur `claude-fable-5-1`. Aucun autre paramètre touché.
- **Rattachement** : RUNBOOK-campagne §3 (`run_params` ex ante : `duration 2246400` ⇒ `n_windows = 37 440`), §6 (« harnais-down ≠ source-en-panne »), critère strate week-end « 8 j ≥ 6,95 j » (§J28), ADR-0020 (fail-closed), ADR-0023 (Pyth absent, inchangé).

## Faits mesurés (journal `campagne/control.jsonl`, 2026-09-24 18:13 UTC)

- Fenêtres distinctes complétées : **33 920** ; dernière fenêtre 2026-09-24 18:09Z ; driver vivant (PID 7876/7880), relancé après la coupure de courant de 16:46Z.
- Fenêtres attendues sur le calendrier 26/08 19:00Z → 24/09 18:09Z : 41 710 ; manquantes : **7 790** (81 % de couverture). Trous ≥ 10 min : 29/08 19:00 → 31/08 13:32 (42,5 h) ; 14/09 10:46 → 16/09 11:23 (48,6 h) ; 22/09 20:46 → 23/09 20:10 (23,4 h) ; 18/09 18:06 → 20:33 (2,5 h) ; 14/09 09:13 → 10:36 (1,4 h) ; divers < 1 h. Tous = harnais-down (coupures, reboots, lignes déchirées SHOGEN-TORN-LINE-1), aucun = source-en-panne.
- Strate **stress** (week-end UTC) : 9 426 fenêtres = **157,1 h** ; critère = 6,95 j = **166,8 h** ⇒ **déficit 9,7 h**. Couverture par week-end : 29–30/08 40 % (1 140/2 880) ; 5–6/09 97 % ; 12–13/09 91 % ; 19–20/09 100 %.
- À 37 440 fenêtres, l'arrêt automatique tomberait le **dimanche 27/09 ~05:00Z** : le 5ᵉ week-end n'entrerait que ~5 h, critère non atteint.

## Décision

1. **`--duration 2246400` → `--duration 2316000`** dans `F:\shogen-campagne\run-campagne.bat` ⇒ `n_windows = ceil(2 316 000 / 60) = 38 600`. Si la collecte est continue, la 38 600ᵉ fenêtre tombe le **lundi 28/09 vers 00:09Z** ; le week-end 26–27/09 entre en entier (+2 880 fenêtres stress ⇒ ≈ 205 h > 166,8 h).
2. Aucun autre paramètre ne change : `w=60`, `sample_lead=10`, pool 11 sources / 12 flux, `sigma-tau.json`, strates, chunk. Le driver est restart-tolérant (dédup `window_start`, last-wins) : arrêt du driver courant puis relance avec la nouvelle durée ; coût ≤ 2 fenêtres.
3. **`run_params`** est réécrit par le driver à la relance et à chaque chunk : la prolongation est visible dans le journal (concordance fail-closed sur les autres champs). Le rapport J28 déclare la prolongation et son motif (coupures), et publie la couverture par week-end ci-dessus.
4. Si une nouvelle coupure repousse la 38 600ᵉ fenêtre au-delà du lundi 28/09 00:00Z, le driver continue jusqu'à 38 600 (aucun arrêt manuel) ; le rapport le dira.

## Conséquences

- Rapport J28 : date de fin réelle = atteinte de 38 600 fenêtres ; les deux strates au critère si aucune coupure ce week-end.
- Item **SHOGEN-TORN-LINE-1** inchangé (avant S3). Item nouveau **SHOGEN-UPS-1** : quatre coupures/reboots en 9 jours ; une alimentation sans interruption ou un hôte distant pour S3 (déclencheur : avant S3).
- Copie datée de `run-campagne.bat` avant modification : `run-campagne.bat.bak-20260924`.

## Alternatives écartées

- Laisser s'arrêter à 37 440 et rapporter la strate stress sous le critère : possible, mais le critère est celui du RUNBOOK et le manque vient du harnais, pas des sources.
- Relancer un segment séparé après l'arrêt : deux journaux à concaténer, complexité inutile face à un driver qui vise simplement n fenêtres.
