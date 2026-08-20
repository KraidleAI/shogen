# Runbook — lancement de la campagne S2 (calibration → mesures pilotes)

> **Statut : plan opérationnel — J0 FIXÉ AU VENDREDI 21 AOÛT 2026, 00:00 UTC** (décision
> investisseur du 2026-08-20 : le vendredi proche, pas le suivant). Régit le lancement du
> harnais S2, selon **ADR-0020** (params ex ante) et **ADR-0021** (σ/τ FIDÈLES : τ relatif, σ
> par classe, clôture P99). Le harnais (skeleton + M1b + M1c + **driver `run_campaign` +
> `closure`, adjugés et acceptés**, `a047814`) est sur `main`, recalculabilité prouvée
> bit-identique. Ce runbook décrit la procédure ; le déclenchement temps réel appartient à
> l'investisseur (commandes concrètes en **§9**).

## 0. Pré-conditions (état au 2026-08-20)

- ✅ **Code Phase A fermé** : `collect` (fenêtré UTC, fin-de-fenêtre), R1/L&M/queue
  exacte, R2 (ASN/contenu/méthode), k_eff par hôtes, drapeau 2, table §6 complète —
  recalculable (ADR-0003, 4033 chiffres bit-identiques adjugés).
- ✅ **ADR-0020 ratifié** : calibration 48h ; τ=0,5 % relatif ; σ par classe ;
  calendrier week-end=stress, J0/J14/J28.
- ✅ **ADR-0021 adjugée et ACCEPTÉE** (2026-08-20, `a047814`) : σ/τ FIDÈLES — τ relatif, σ par
  classe, calcul de clôture P99 (`closure.py`). Deux gates (oracle CONCORDANT bit-identique +
  G2 8/8 sans affaiblissement) + verdict G7 + checkpoint #2 validateur-humain. **Le CONSTAT M2
  est résolu** : l'instrument exécute enfin les σ/τ ratifiés (l'ancien harnais les trahissait —
  τ absolu, σ scalaire).
- ✅ **Driver `run_campaign` + `closure` construits et acceptés** : phases
  `demo`/`calibration`/`campagne` (campagne fail-close sans `--sigma-tau-file`), boucle
  restart-tolérante, DI complète, journaux hors dépôt.
- ✅ **Chaîne opérateur PROUVÉE LIVE sur la machine de campagne (2026-08-20)** : smoke 12/12 ;
  collecte demo 4/4 (σ/τ fidèles) ; table §6 rendue ; `closure` → σ/τ JSON valide (clause de
  révision τ vérifiée fail-closed) ; ASN DNS→RIPEstat→Cymru 11/11 concordant (M2/oracle).
- ✅ **PS-S2-01 résolu** : deviation Chainlink 0,5 % [lu] ; heartbeat ~1 h (3600 s)
  dérivé → **σ_chainlink = 5400 s** (plus de repli fail-closed).
- ✅ **§10.9 (débits) vert** : ~1 req/min/source, marge min **60×** ; CoinGecko 429 →
  panne (iii) par conception.
- ✅ **PS-S2-02** (rapport Kaiko primaire) — **réglé (2026-08-20)** : abonnement premium
  du mainteneur (le mur « Upgrade » est un bug d'affichage Kaiko signalé ; texte intégral
  dû). Strate *week-end=stress* désormais **[lu] primaire** — Kaiko « Crypto's Collateral
  Fragmentation Problem » (2026-04-07) : « weekday volumes consistently run 100% higher
  than weekend levels », et les deux escalades de stress 2026 tombées un week-end.
  **PS-S2-01 heartbeat** dérivé du countdown (exact 3600s = feed docs si précision voulue).

## 1. Machine et déploiement

- **Machine persistante** (la « machine de campagne ») — PAS une session éphémère.
  **Historique de coupures de courant** (memstack 2026-07-29) → la reprise (§5) est
  obligatoire, pas optionnelle.
- **Python ≥ 3.9, stdlib seule** (R-8 : aucune dépendance ; à re-vérifier :
  `pip list` doit être sans rapport avec le harnais).
- **Code** : `git clone`/`pull` de `origin/main` (révision épinglée committée au
  journal de la campagne, pour la reproductibilité du binaire d'analyse).
- **Horloge** : NTP actif ; le contrôle d'horloge du harnais (§4 exigence 2) journalise
  l'offset au démarrage et à chaque reprise — non bloquant, mais tracé.
- **Réseau sortant** vers les 11 endpoints (`docs/10` §3.1) + DNS/RIPEstat/Cymru pour
  l'axe ASN. Aucune clé, aucun token, aucun cookie (« strictement sans clé »).
- **Auto-restart au boot (option A — historique de coupures)** : le driver REPREND après une
  coupure (dédup marqueurs + last-wins, testé), mais il faut le relancer. Tâche « au démarrage »
  rejouant la commande du segment ACTIF via un wrapper qui boucle sur crash —
  `F:\shogen-campagne\run-seg.bat` :

  ```
  :loop
  cd /d F:\Shogen\s2-harness
  python -m shogen_s2.run_campaign --phase calibration --journal-dir F:\shogen-campagne\calibration --duration 172800 --w 60 --sample-lead 10
  if errorlevel 1 ( timeout /t 30 & goto loop )
  ```

  Enregistrement : `schtasks /create /tn shogen-campagne /tr F:\shogen-campagne\run-seg.bat /sc onstart /ru <user>`.
  À J0+48h, remplacer la ligne `python …` par la commande `campagne` (§9d). Driver terminé
  (n fenêtres atteintes) → sort 0, la boucle s'arrête ; un reboot ultérieur le relance, il voit
  n fait et sort aussitôt (idempotent, sans risque).

## 2. Le driver de lancement — spécification (mission code M2, à adjuger avant J0)

Le harnais expose déjà `collector.collect(...)` (read path) et `collector.collect_asn(...)`
(axe ASN). Le driver est une **glu opératoire mince** (jetable, R-22) qui :

1. **Fixe le `run_params`** committé ex ante : `pool` = 11 sources (§3.1), `w=60`,
   `strate_calendar` = week-end UTC (spec `WEEKEND_STRATE_SPEC`), `decimal_prec=50`,
   `seuil_historique_valeur=10`, `n_min_hors_enveloppe=4`. **σ/τ : voir §3** (fixés à
   la clôture de calibration, pas au lancement).
2. **Câble le read path réel** : `read_fn = sources.read` (les 12 décodeurs, déjà
   *tested* + smoke live 12/12).
3. **Câble l'axe ASN réel** : `resolve_fn = r2.resolve_host_real` (**non exercé en
   réseau à ce jour — M1c frontière 1** : à smoke-tester en §4 AVANT J0).
4. **Boucle de collecte restart-tolérante** : `now_fn = time.time`, `sleep_fn =
   time.sleep` ; journal **append-only** ; à chaque reprise, ré-écrit `run_params`
   (concordance fail-closed vérifiée) + contrôle d'horloge ; fenêtres UTC-alignées
   (personne ne choisit ses bords) ; last-wins + dédup marqueurs (reprise idempotente,
   testée).
5. **Cadence ASN** : re-mesure de l'axe ASN à intervalle (au moins une fois par
   fenêtre de rapport ; l'attribution est un instantané daté, §4.1 résidu 4/7).

**M2 (code) est une mission worker adjugée** (oracle de recalcul + G2 sur le driver +
la vérification live), comme le skeleton/M1b/M1c — le driver ne se promeut pas sans
G0–G7.

## 3. Les seuils σ/τ — fixés à la CLÔTURE de calibration, pas au lancement

Rappel du reframe (ADR-0020) : le **journal brut est sans seuil à la capture** ; σ/τ
n'affectent que les **statuts d'écart dérivés** (recalculés au rapport, ADR-0003).
Donc :

- **J0** : la collecte démarre avec les valeurs **proposées** d'ADR-0020 (τ=0,5 % ;
  σ = {places 30 s, agrégateurs 300 s, sans-horodatage « non évaluable »,
  Chainlink 5400 s, Pyth 30 s}) écrites au `run_params`.
- **J0+48h (clôture calibration)** : depuis les **fenêtres de calibration seules**
  (exclues à jamais de l'inférence), calculer `P99(|écart LOO relatif| honnête)` et
  `P99(staleness honnête par classe)`. **Réviser par ADR** avant la campagne SI :
  `P99(concordance) > 0,25 %` (⇒ τ) ou `σ_floor < 3·P99(staleness_s)` (⇒ σ_s remonté).
  Sinon les valeurs proposées tiennent. **Committer (git) les σ/τ finaux** avant la
  première fenêtre scorée.
- **Fail-closed run_params** : la calibration et la campagne portent des `run_params`
  potentiellement différents (σ/τ) → **deux segments de journal** (calibration /
  campagne), la calibration marquée exclue. L'archive brute est continue depuis J0 ;
  l'**inférence** ne consomme que le segment campagne.

## 4. Vérification live AVANT J0 (dé-risquage, quelques fenêtres) — ✅ FAIT le 2026-08-20

Ne PAS lancer 48h à l'aveugle. Smoke live court (minutes) — **exécuté sur la machine de campagne
le 2026-08-20, tout vert** (§0) ; procédure reproductible :

1. `python -m shogen_s2.smoke` → 12/12 (read path — déjà vert).
2. **`collect_asn` en réseau réel sur 2-3 hôtes** (le trou de M1c frontière 1) : la
   chaîne DNS→RIPEstat→Cymru répond-elle ? l'attribution croisée concorde-t-elle
   (≥ 2 bases) ? Consigner le résultat ; si RIPEstat/Cymru rate, l'axe ASN dégrade en
   « non évaluable » (fail-closed) et k_eff porte « borne supérieure » (C-A) — pas un
   casseur, mais à savoir avant J0.
3. Un run de collecte de ~10 fenêtres (10 min) → la table §6 se rend de bout en bout,
   recalculable ; contrôle d'horloge journalisé.

## 5. Calendrier de la campagne (ADR-0020)

| jalon | date | action | livrable |
|---|---|---|---|
| **J0** | **vendredi 21 août, 00:00 UTC** | lancement de la collecte (l'**archive** démarre — l'actif non copiable) ; les 48 premières h = **calibration** | journal brut append-only |
| J0+48h | **dimanche 23 août, 00:00 UTC** | clôture calibration → **commit σ/τ** (§3, §9c) ; début du segment campagne | `sigma-tau.json` scellé, git |
| **J14** | **jeudi 4 sept** | **rapport intermédiaire** : z calme probablement publiable ; z stress « historique insuffisant » + queue exacte — **premier chiffre opposable** | `11-mesures-pilotes.md` v1 (recalculé par l'oracle) |
| **J28** | **jeudi 18 sept** (**date fixe**) | **rapport final** : les deux strates au critère (week-end : 8 j ≥ 6,95 j) | `11-mesures-pilotes.md` final |

- **Fin à DATE FIXE, jamais « quand z croise 2,33 »** (l'arrêt optionnel gonfle
  l'erreur type-I, 04 §5).
- **Trois z toujours publiés** (calme, stress, poolé) — lecture asymétrique du poolé
  écrite d'avance (§5.5) ; risque famille ~3 % publié.
- Si `P̂_more` réel s'écarte d'un ordre de grandeur de l'illustration 10⁻³, J14/J28
  se recalculent depuis l'estimée de calibration **avant** que les dates ne soient
  promises publiquement.

## 6. Monitoring et reprise

- **Journal append-only, fenêtres UTC-alignées** → reprise idempotente (dédup marqueurs
  + last-wins, testé). Redémarrage après coupure : relancer le driver, il reprend.
- **Contrôle d'horloge** au démarrage/reprise (offset NTP ou plausibilité croisée des
  `source_ts`) — journalisé, non bloquant ; une dérive silencieuse corromprait n.
- **Harnais-down ≠ source-en-panne** (déjà codé) : une fenêtre non tentée n'entre ni
  dans n ni en panne — le monitoring distingue « harnais tombé » de « source tombée ».
- **Surveiller** : uptime de collecte, taux de 429 (CoinGecko attendu → panne (iii)),
  bans (Bitfinex — mais 10× sous le seuil), échecs de résolution ASN, événements de
  reprise. Aucun de ces états ne se « corrige » en silence : ils se journalisent.

## 7. Procurements et dettes ouverts (non bloquants pour J0, dus avant claim public)

- **PS-S2-02** — rapport Kaiko primaire (volume week-end BTC post-ETF) : **réglé** —
  *week-end=stress* fondé **[lu]** sur Kaiko primaire (débrief 2026-04-07 : « weekday
  volumes consistently run 100% higher than weekend levels » ; abonnement premium
  mainteneur). Reste **optionnel** : le chiffre historique ~28 %→16-17 % (The Block 2024,
  [2nd]) si une antériorité chiffrée précise devient porteuse — paginer l'archive Kaiko 2024.
- **Vérifs d'endpoints ASN octet-exact** (M1c frontière 3, dette 10 §10.4) : les 3
  pages (DoH/RIPEstat/Cymru) lues via résumeur = rang (b) ; ré-établir octet-exact
  avant un claim sur l'axe ASN.
- **Heartbeat Chainlink exact** (3600 s) : dérivé du countdown ; confirmer aux feed
  docs si une précision au-delà de « ~1 h » devient porteuse.
- **Multi-résolveurs / multi-vantage ASN** (§4.1) : v0 = 1 résolveur ; résidu publié,
  dû à la campagne mûre.

## 8. Ce que la campagne NE fait PAS

- **Ne publie rien.** D6 = « publiable », pas « publié » : l'acte de publier
  `11-mesures-pilotes.md` (et l'exposition du benchmark) est une **décision
  investisseur** (percute DEVOPS §1 dépôt privé jusqu'à S3, S5 antériorité arXiv,
  D10/PS-10 marque). Les rapports J14/J28 sont produits et vérifiés ; leur diffusion
  attend.
- **Ne promeut pas le harnais** (R-22 : jetable, mort après le rapport).
- **Ne consomme pas les fenêtres de calibration dans l'inférence.**
- **Ne s'arrête pas à un z favorable** (date fixe).

## 9. Séquence de déclenchement — COMMANDES CONCRÈTES (J0 = vendredi 21 août 2026)

Toutes depuis `F:\Shogen\s2-harness` (`Set-Location F:\Shogen\s2-harness`), Python ≥ 3.9
stdlib seule. Journaux sur **`F:`** (jamais `C:`, à l'étroit). `git pull origin main`
d'abord ; noter le SHA (`a047814` ou plus récent) au journal de campagne.

**a) Avant J0 — dé-risquage** *(fait le 2026-08-20 sur cette machine : smoke 12/12 +
collecte demo + ASN 11/11 concordant)* :

```
python -m shogen_s2.smoke
```

**b) J0 — vendredi 21 août 00:00 UTC — lancer la CALIBRATION (48 h) :**

```
python -m shogen_s2.run_campaign --phase calibration --journal-dir F:\shogen-campagne\calibration --duration 172800 --w 60 --sample-lead 10
```

`--duration 172800` = 48 h (2880 fenêtres). σ/τ = planchers ADR-0020 PROVISOIRES par classe
(la capture est SANS SEUIL — la valeur provisoire n'altère pas l'archive, §3). L'**archive
démarre ICI** (l'actif non copiable). Sous auto-restart (§1).

**c) J0+48h — dimanche 23 août 00:00 UTC — CLÔTURE de calibration (fixe les σ/τ finaux) :**

```
python -m shogen_s2.closure F:\shogen-campagne\calibration > F:\shogen-campagne\sigma-tau.json
type F:\shogen-campagne\sigma-tau.json
```

LIRE le JSON : si `tau_revision_needed` = true (P99 écart relatif > 0,25 %) ou un `sigma_classe`
remonté surprend → **révision par ADR AVANT la campagne** (fail-closed : `tau_classe` = null
bloque la campagne). Sinon **committer `sigma-tau.json`** (git) — σ/τ scellés, reproductibles.

**d) J0+48h → J28 — lancer la CAMPAGNE (segment scoré DISTINCT) :**

```
python -m shogen_s2.run_campaign --phase campagne --journal-dir F:\shogen-campagne\campagne --sigma-tau-file F:\shogen-campagne\sigma-tau.json --duration 2246400 --w 60 --sample-lead 10
```

`--duration 2246400` ≈ 26 j (dim. 23 août → jeu. 18 sept = **J28, date fixe**). Sans
`--sigma-tau-file`, la campagne **fail-close** (rc=3). Dossier de segment **distinct** de la
calibration (§3 : l'inférence ne consomme que ce segment).

**e) J14 (~4 sept) / J28 (18 sept) — rapports** (recalculés, NON publiés sans décision
investisseur, §8) :

```
python -m shogen_s2.report F:\shogen-campagne\campagne
```

**f) Clôture** : rapport de passe (zéro dette), critère de sortie S2 (les axes R2
discriminent-ils ? — n, K, z, partition, k_eff vs k nominal).
