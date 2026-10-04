# Sorties du lot PLAN-S2BIS (préparation de S2-bis)

Produites le 2026-10-04 de 16:59:04Z à 17:00:31Z par `bash scripts/plan-s2bis/lancer.sh` (code commis et épinglé au JOURNAL, entrée de
16:57:31 UTC, `SHA256SUMS` du code `65c26310…4398`), sur la copie de session des journaux scellés de S2 (sha256 égaux au bloc machine du
paquet de S2), avec le harnais extrait du commit d'analyse `f35a70c`. Chaque sortie porte en tête : « préparation de S2-bis ; ne change
pas le verdict de S2 (« R1 discrimine » = FAUX) ». Contrôle de cohérence : n, K et P̂_more par strate recomptés égaux au bloc 3 du rendu J28.

- `tau_sigma.txt` : τ et σ de BTC/USD par classe de source (ADR-0029 §2.6, amendement daté du 2026-10-04 16:20:56 UTC) ; le bloc
  `[VALEURS POUR LE PAQUET DE S2-BIS]` est destiné au paquet de pré-enregistrement de S2-bis, jamais re-réglé ensuite.
- `episodes.txt` : longueurs d'épisodes de panne et d'écart par unité et par strate ; courbe FIV_série(ℓ), pour SIM-BIS.
- `okx.txt` : contribution descriptive de la paire de flux OKX à K de S2 (SHOGEN-R1-HOTE-STRUCTUREL-1).
- `SHA256SUMS` : empreintes des trois sorties.
- `G1-lot-PLAN-S2BIS.md` (rapport du worker, phase 1 avant corrections) et `G2-lot-PLAN-S2BIS.md` (relecture G2 neuve).
