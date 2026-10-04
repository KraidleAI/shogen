# The S2 pilot measurements — campaign report (single execution of 2026-10-04)

> **Draft — not published.** English translation of the accepted report; numbers, verdicts and sealed labels are identical to the original; the sealed package and the original outputs prevail in case of discrepancy. Report only: supporting documents are provided on request, under agreement.
>
> *Translation conventions.* Printed outputs, verdicts and sealed labels are kept in French, unchanged: in code blocks, between French guillemets, or as bare labels in the running text. At its first occurrence in the running text, each such passage carries an English gloss, in italics between square brackets, unless it is already legible in English (symbols, English terms); code blocks are not glossed; the glossary at the end of this document lists the glosses. Quotations from other French-language documents of the project (design document, ADR and annexes, sealed package, project journal, recorded answers of the investor) are given in English translation between English quotation marks; the French original prevails. Numbers follow English usage (decimal point, comma as thousands separator), except in identifiers, hashes, ISO dates and copied outputs.

> **Filtered public version, in draft form: not published.** Its publication is a decision of the investor (ADR-0028 §4, pt 4; D9), which awaits the investor's written go-ahead, given after reading. Compared with the source report, the local-workstation paths, the names of private repositories, the session or agent identifiers, the references to documents or folders excluded from any distribution and mentions of internal governance that are of no relevance to an outside reader are removed or replaced by a neutral sentence; one wording is brought into line with the project's vocabulary register. By decision of the investor, the finding on Pyth and an instruction of the investor are reworded in factual and neutral terms. The publication covers this report only: the other documents cited (project journal, ADRs and annexes, sealed package, renderings, seal, records, scripts) are in the project's private repository and are not published; the sealed package, the seal, the renderings, the records and the scripts are provided on request, under agreement (section “Reproduce”, “What is not public”). The verdict, the values, the limitations, the declared deviations, the pre-registration, the seal and the reproduction procedure are retained; no number is changed or added.
>
> **Status**: report drafted on 2026-10-04 (UTC) by a fresh drafter (model `claude-opus-5-5`), who wrote neither the analysis code, nor the pre-registration package, nor the renderings. It reports what the renderings of the single execution print, without reinterpreting the rule: the sealed text is authoritative (package §10.2, pts 1 to 11; pt 11: an unforeseen case is a declared deviation, never a rewrite).
>
> **Basis**: ADR-0028 D6 (v) (output wired to `docs/11-mesures-pilotes.md`), D6 (vi) and D9; exit criterion of `docs/10-mesures-pilotes-design.md` §7; sealed package `docs/adr-0028/PAQUET-PREREG-S2.md` (sha256 `4d2a8276316b1c66a08aabb15ff3b39be812978e93dafc01a4e627f20d0af528`); renderings filed byte for byte in `docs/adr-0028/execution/rendu-2026-10-04/`.
>
> **Provenance**: G1 journal of the drafter; it lists each reading, each command and its output. Each number in this report is either copied from a rendering (file and line cited) or computed by a script of the drafter (mark [calc], output cited). A computation by the drafter never replaces a printed value.

## 1. Summary

Reading conventions and lexicon: next section.

**Question.** S2 was to settle the question posed by the roadmap: “are the R2 axes observable in practice, and does the R1 test discriminate anything on real data?” (doc 10 §1). The exit criterion sets the deliverable: “n windows, K, z of the pool, the observed R2 partition, k_eff vs nominal k; negative result = result” (doc 10 §7). The decision rule is the sealed rule SHOGEN-CRITERE-R1-1 (package §10.2), evaluated only once on the J28 segment.

**Verdict of the rule.** On J28 (35,982 one-minute windows after the D5 exclusion; analysis pool of 11 feeds and 10 hosts after the removal of Pyth), the rule returns, in each of the two strata, the value **NE REJETTE PAS [*does not reject*], on account of the discordance**: the confirmatory statistic z_s exceeds 2.33 (≈ 20.8 in calm, ≈ 28.5 in stress), but the block standard-error floor brings it back below the threshold (z_bloc,s ≈ 1.95 and ≈ 1.74). **« R1 discrimine » = FAUX** [*“R1 discriminates” = false*] (J28 l.435522). For each stratum, the rendering prints the sealed statement of the discordance case: « le modèle binomial de doc 10 §5.1, à fenêtres indépendantes, est rejeté ; la cause n'est pas identifiée entre co-défaillance des sources et dépendance sérielle des fenêtres » [*the binomial model of doc 10 §5.1, with independent windows, is rejected; the cause is not identified between co-failure of the sources and serial dependence of the windows*] (J28 l.435517, l.435520), with a minimum detectable excess EMD_s ≈ 196 windows in calm and ≈ 211 in stress. On the R2 side, the ASN axis was observed: the observed partition counts k_eff = 4 classes for nominal k = 10 hosts (J28 l.435779-435780); flag 1 is false in both strata and flag 2 is off (J28 l.435794-435795).

**What this verdict allows one to say.** On 24,585 calm windows and 11,397 weekend windows, outage, staleness and out-of-envelope axes, as observed by this instrument (host, DNS and network of the harness included): the binomial model with independent windows is rejected in both strata (sealed statement of the discordance); the pre-registered rule, which also requires z_bloc,s ≥ 2.33, returns NE REJETTE PAS in both strata, so that « R1 rejette (s) » [*R1 rejects (s)*] is stated for no stratum. A negative result is a result (doc 10 §7). The ASN axis is observable: 7 of the 10 hosts of the pool share AS13335 (Cloudflare), on the delivery side (J28 l.435691).

**What it does not allow one to say.** It neither establishes nor excludes a co-failure of the sources: the cause of the discordance is not identified (sealed statement). It establishes no pair dependence (ADR-0028 D3: descriptive). It does not establish the independence of the sources (doc 09). The pre-registered descriptives (§5), including the decomposition of K by `panne_transport` readings, are hors décision [*outside the decision*] and identify no cause. The hors décision outputs that print « R1 discrimine » VRAI [*true*] (main J14; « plage incluse » [*range included*] variant of the third-party recomputation) do not change the verdict (§7). Nothing is said about the accuracy of a price, nor outside the measured axes (A(axis-coverage), doc 08).

**Decisions of the investor (stated; this report settles none of them).** Pre-registered options:

- ADR-0028 D6 (vi), quoted (inner quotation marks rendered as ‘ ’): “Clause dated after J28: decision of the investor (§4.10 b), on the rule written in the package (SHOGEN-CRITERE-R1-1). If R1 discrimine: ‘continuous benchmark’ work package through a new G0 (reimplementation in the core, or G0-G7 promotion of the collection). Otherwise, the collection dies as planned.” Dated erratum of the same paragraph: “‘R1 discrimine’ := VRAI of rule SHOGEN-CRITERE-R1-1; ‘the collection dies’ remains a decision of the investor”.
- ADR-0028 D9, quoted: “After J28: bifurcation = decision of the investor (§4.10 b)”, with, for the branch observed here: “If (i) is false: priority to G4 and revision of 04 (doc 10 l.35-36; 05-roadmap l.126-127).”
- Package §10.2 pt 11, quoted: “FAUX → priority to G4 and revision of 04, with the EMD_s”; “‘The collection dies’ remains a decision of the investor (D6 vi), never a mechanical consequence.”
- Publication of J14 and of J28, and of this report (ADR-0028 §4 pt 4; D4: J14 is not published without a decision of the investor).

Decisions recorded since, after the execution and before this report (JOURNAL l.322, 2026-10-04 02:42:19 UTC; answers of the investor quoted): S2 collection, “Stop it (Recommended)”; S2-bis, “Yes, prepare S2-bis (Recommended)”; publication, “Yes, in principle (Recommended)”, the final go-ahead remaining with the investor after reading the report; one answer on commercial strategy is not reproduced. The JOURNAL notes there that the D9 bifurcation follows the branch “(i) false” (G4, revision of doc 04), plus an ADR-S2-BIS work package.

## Reading conventions and lexicon

The renderings are cited by abbreviation and line number (“J28 l.435516” = line 435516 of the J28 rendering). All are in `docs/adr-0028/execution/rendu-2026-10-04/`, under the prefix `shogen-27b0e30-rendu-20261004T011129Z-943.`:

| abbreviation | file | content | sha256 |
|---|---|---|---|
| SUITE | `0-suite.out` | `s2-harness` suite (run `suite`) | `4f223a22950778c799b39b1856a400c965ac18b4b57625bfef3136c04daaeb3a` |
| J14p | `1-j14-principal.out` | main J14, hors décision | `246ebeea132392de15f34ccefff808e4e44b157498c3fdc1009282cc7e1e1498` |
| J14s | `2-j14-second.out` | second J14, hors décision | `d89db3a94da67f48c00f3bbc7ce7710a092fc3ad14f935e874e8c905f0172b24` |
| J28 | `3-j28.out` | confirmatory segment: blocks 1 to 6 and [SENSIBILITÉ] [*SENSITIVITY*] | `26877549658b7271f766b433e941c79a35169398238755fa4bbf77a4911d65c0` |
| RT | `4-recalcul-tiers.out` | third-party recomputation (`recompute_*`), JSON | `a76ad44832d28751e68c56d6844be0c0ebd83f1b79b89bd7a16611779d891ac8` |
| RAW | `5-raw.out` | verdict of the raw journal | `e996c6343bbed572221b6a3eb7679286167b46b3452431136f3d622254ae97b8` |
| ENR | `json` | oracle record of role « rendu » [*rendering*] | `355cf9bb43609c1c4b0f3ffebcd32d9d987e5e12e63277d9e4acbd467eb0fb5c` |

Other documents: PAQ = sealed package; ADR = `docs/adr-0028/ADR-0028-decisions-sortie-S2.md`; annexes A, B, D of the same folder; doc 04, doc 08, doc 09, doc 10 = `docs/04-certificat-diversite.md`, `docs/08-assumptions.md`, `docs/09-vocabulaire.md`, `docs/10-mesures-pilotes-design.md`.

- **Complete values**: `Decimal` strings (precision 50) copied as printed, between backquotes.
- **Reading roundings**: in the running text only, flagged by “≈”, to 3 significant figures; the complete value is in a table, with its line.
- **[calc]**: computation by the drafter (scripts `d3_lift.py`, `controles_r1.py`, `comparer_recalcul.py`, `calc_divers.py`, Python standard library, exact arithmetic or `decimal`; outputs cited in §8.9 and §6).
- **No p-value** is given or read (package §10.2 pt 4). The exact binomial tails that the J14 renderings print hors décision under the §5.4 guard are not copied here; they remain readable at the lines cited (§7.1, §7.2).
- **Vocabulary**: register of doc 09. The independence of sources is never “established”: an independence model is rejected or not rejected, on n windows, on named axes, as observed by this instrument.

**Lexicon**, for an outside reader (definitions of doc 10 and of the package, summarized):

- **Feed, source, host**: a feed is a reading of the BTC/USD (or BTC/USDT) price served by a source (exchange, aggregator or oracle); two feeds can share a host (`www.okx.com`). The configured pool counts 12 feeds.
- **Window**: a minute of the UTC grid (w = 60 s); in each window, each feed counts as one reading.
- **Anomaly** (doc 10 §5.2): a feed is anomalous in a window if it is in outage (reading absent, status not `ok` or price absent), stale (carried timestamp older than σ_classe) or out of envelope (relative difference from the median of the other feeds beyond τ_classe, with at least four respondents).
- **n, K**: number of analysed windows of a stratum; number of those windows in which at least two feeds are anomalous.
- **P̂_more**: probability of at least two anomalies in a window if the feeds were unrelated to one another, estimated from the anomaly rate of each feed (Knight and Leveson model, doc 10 §5.1).
- **z_s, z_bloc,s**: difference between K and n·P̂_more, scaled by the binomial standard error with independent windows (z_s) or by a block standard error that allows a serial dependence of the windows of range below ℓ = 240 windows, i.e. 4 h (z_bloc,s).
- **Rule SHOGEN-CRITERE-R1-1**: a tested stratum (guard n·P̂_more(1 − P̂_more) ≥ 10 met) REJETTE [*rejects*] if z_s ≥ 2.33 and z_bloc,s ≥ 2.33; « R1 discrimine » has the value VRAI if at least one stratum rejects.
- **Strata**: stress = Saturday and Sunday UTC; calm = the other days; calendar fixed before the campaign.
- **EMD_s**: minimum detectable excess of K, in windows, at power 0.8 (design choice).
- **R2, k_eff, nominal k**: diversity observables; here the ASN axis, the network that announces the address of each host; k_eff = number of classes after merging the hosts that share a measured ASN; nominal k = number of hosts.
- **J28, J14**: J28 is the confirmatory segment (38,600 distinct windows at fixed n, then D5 exclusion); the two J14 segments are cuts of the start of the campaign (fourteen days for the main one, up to 2026-09-04 for the second), hors décision.
- **D1, D5**: removal of the feeds without any `ok` reading (here Pyth); exclusion of a range of degraded harness, from 24 to 26 September 2026.
- **Hors décision**: printed and labelled output, which cannot change the verdict (package §10.2 pt 9).

## 2. Instrument and campaign

### 2.1 Fact class, pool, feeds and hosts

- Class: « BTC/USD-stable, devise marquée par flux » [*BTC/USD-stable, currency marked per feed*]; « pool configuré = 12 flux » [*configured pool = 12 feeds*]: binance, coinbase, kraken, okx_ticker, okx_index, bitstamp, gemini, bitfinex, coingecko, defillama, pyth, chainlink (J28 l.8-9); currency composition of the analysis pool: 9 USD / 2 USDT (l.46).
- Window w = 60 s (l.10); `Decimal` decimals to 50 digits (l.19); threshold z = 2.33 (l.21); guard n·P̂_more·(1−P̂_more) ≥ 10 (l.16, l.20); n_min = 4 respondents for the out-of-envelope axis (l.17).
- Thresholds per class, committed before the campaign (J28 l.12-14):

| class (σ/τ) | feeds | σ_classe (s) | τ_classe |
|---|---|---|---|
| `place_horodatee` | coinbase, okx_ticker, okx_index, bitstamp, gemini | `180.0` | `0.0045` |
| `sans_horodatage` | binance, kraken, bitfinex | `None` (staleness not evaluated) | `0.0045` |
| `agregateur` | coingecko, defillama | `1140.0` | `0.026` |
| `oracle_chainlink` | chainlink | `10695.0` | `0.0165` |
| `oracle_pyth` | pyth | `33.0` | `0.0015` |

- Printed anomaly definition (J28 l.435448): per window and per feed of the analysis pool, precedence outage > staleness > out-of-envelope; K = windows with at least two anomalies. Printed residual: staleness « fail-open » for binance, kraken and bitfinex, which carry no timestamp (l.435464).
- Hosts: the 11 feeds of the analysis pool are served by 10 distinct hosts (« k nominal = 10 (hôtes distincts du pool) » [*nominal k = 10 (distinct hosts of the pool)*], J28 l.435779); okx_index and okx_ticker share `www.okx.com` (l.435688); chainlink is read through the public RPC `ethereum-rpc.publicnode.com` (l.435685).

### 2.2 Analysis pool (ADR-0028 D1)

| stratum | removal (case) | printed counts | nominal k_s | source |
|---|---|---|---|---|
| calm | pyth, case (a) | « ok = 0 / 24585 lectures, n = 24585 » [*ok = 0 / 24585 readings, n = 24585*] | « 10 sources / 11 flux » [*10 sources / 11 feeds*] | J28 l.42, l.44 |
| stress | pyth, case (a) | « ok = 0 / 11397 lectures, n = 11397 » [*ok = 0 / 11397 readings, n = 11397*] | « 10 sources / 11 flux » | J28 l.43, l.45 |

Pyth is removed from R1, from L&M and from R2 in both strata (case (a): no `ok` reading in any stratum). The ADR carries the count over the whole journal: “0 `ok` out of 40,804 readings, HTTP 401 from 2026-08-26T19:00Z” (ADR l.25). No removal under case (b) is printed.

### 2.3 J28 segment (ADR-0028 D4, D2 pt 6)

- Segment: `[1787770800 ; 1790558880) = [2026-08-26T19:00:00+00:00 ; 2026-09-28T01:28:00+00:00)`, half-open, same bound on `window_start`, `ts` and `harness_ts`, fixed n = 38,600 (J28 l.31).
- The journal counts 38,600 distinct windows: first `1787770800` (2026-08-26T19:00:00Z), last `window_start` `1790558820` (2026-09-28T01:27:00Z) (l.28); T_fin = 1790558820 + 60 = 1790558880 [calc].
- The segment removes nothing: « fenêtres distinctes (window_close) calme 0, stress 0 ; asn_attribution 0 ; clock_check 0 » [*distinct windows (window_close) calm 0, stress 0; asn_attribution 0; clock_check 0*] (l.32).

### 2.4 D5 exclusion

- Bounds: `window_start` in `[1790273880 ; 1790435280]` (closed; 2026-09-24T18:18:00Z to 2026-09-26T15:08:00Z, J28 l.33); `ts` and `harness_ts` in `[1790273880 ; 1790435340)` (l.34).
- Removed by the range (l.35-36): 1,709 calm windows and 909 stress windows; 5,313 `asn_attribution` probe records (4,498 `ok`, 815 `resolve_failed`); 483 `clock_check` probe records.
- Reason (ADR l.60): `resolve_failed` 15.3% in the range against 1.85% outside the range, health of the DNS harness, not a source statistic; « causalité non établie » [*causality not established*] (recalled by the rendering, J28 l.435801).
- Check [calc]: 1,709 + 909 = 2,618; 38,600 − 2,618 = 35,982 = 24,585 + 11,397.

### 2.5 Strata and n per stratum

- Ex ante calendar: « kind=weekend_utc stress = samedi+dimanche UTC » [*kind=weekend_utc stress = Saturday+Sunday UTC*], operator decision committed before the launch, never inferred from the data (J28 l.27).
- n_calme = 24,585 completed windows (J28 l.435451); n_stress = 11,397 (l.435471).
- Coverage of the five weekends (J28 l.435814-435818): 2026-08-29, 1,140 windows out of 2,880 (19 h 00 min); 2026-09-05, 2,801; 2026-09-12, 2,611; 2026-09-19, 2,874; 2026-09-26, 1,971 in the excluded variant (32 h 51 min), 909 windows removed by the D5 range.

### 2.6 Skipped windows

- Grid with a 60 s step over the segment, without a `window_close` marker, outside the D5 range: 5,701 in calm, 2,094 in stress, all causes combined, under the assumption H_perte (A(loss-non-informative), doc 08) (J28 l.37).
- Breakdown (l.38-41): « harnais vivant » [*harness alive*] (skipped between two markers of the same start) 17 in calm, 150 in stress; cause not attributed by the journal (stop or transition between starts) 5,684 in calm, 1,944 in stress.
- Check [calc]: the grid of the segment counts (1790558880 − 1787770800)/60 = 46,468 windows; 46,468 − 38,600 (markers) − 73 (windows of the range without a marker, J28 l.435806) = 7,795 = 5,701 + 2,094.
- The harness started 4,093 times over the campaign, with `run_params` concordant on the load-bearing fields (J28 l.26).

### 2.7 Collection host and limitations of the observer

- The S2 collection is a bare HTTPS reading by a harness (doc 10 §1, non-goal 1); the only interaction with a chain is an `eth_call` reading through public RPC (doc 10 §1, non-goal 4).
- The renderings carry the trace of a Windows collection host: path with a drive letter (J28 l.7); socket errors `WinError 10013` in the ASN probe records at the end of the main J14 (J14p l.209885). The JOURNAL places this collection on the personal workstation of the investor, who asks for a collection on a virtual private server for S2-bis (JOURNAL l.324).
- A single observation point and a single resolver per ASN probe record, `cloudflare-dns.com` (J28 l.435676-435688); the rendering itself publishes residuals 3 (single-vantage; multi-resolver probe « DUE », J28 l.435772) and 5 (the measurement path belongs to the measured class, « le résidu est à son MAXIMUM, publié » [*the residual is at its MAXIMUM, published*], l.435774).
- The assignment of windows to strata and segments rests on the host's clock, A(harness-clock) (doc 08; package §12 pt 17). Block 1 of J28 prints 3,610 start-up `controle_horloge` probe records (l.48-3657; count [calc] by line search); their range is not computed by the rendering (package §12 pt 17) nor by this report.
- The label of the annex D.5 descriptive recalls it: « le z confirmatoire inclut les modes communs de l'observateur (hôte, DNS, réseau) » [*the confirmatory z includes the common modes of the observer (host, DNS, network)*] (J28 l.435531).

## 3. Confirmatory verdict (J28, rule SHOGEN-CRITERE-R1-1)

The rule is evaluated mechanically by the single-execution script on the J28 segment, D1 analysis pool per stratum, D5 exclusion, in each confirmatory stratum (package §10.2 pt 1). The comparisons bear on the unrounded `Decimal` values, against the constant `Decimal("2.33")`, with the inequality « ≥ » (pt 4; printed reminder, J28 l.435515).

### 3.1 Inputs and value per stratum (complete values)

| input (pt 1) | calm | stress | J28 |
|---|---|---|---|
| n_s (completed windows) | `24585` | `11397` | l.435451; l.435471 |
| K_s (windows with ≥ 2 anomalies) | `154` | `133` | l.435451; l.435471 |
| P̂₀ | `0.94236061369788154146024296580093086828513938470018` | `0.94068072247707197570660265774160717593176388308751` | l.435465; l.435485 |
| P̂₁ | `0.056276435879320695626255997808433611118939114709424` | `0.057852878561437609992981152213024246102249979400096` | l.435466; l.435486 |
| P̂_more,s | `0.0013629504227977629135010363906355205959215005903986` | `0.0014663989614904143004161900453685779659861375123928` | l.435467; l.435487 |
| guard n_s·P̂_more,s(1−P̂_more,s) (threshold 10) | `33.462466216157713120610261901717310599417168320476` | `16.688041699661428674928415017858500902580981925520` | l.435468; l.435488 |
| z_s | `20.829495417808173515660354538360738280133057485734` | `28.466243694685921454102240881955034913016073716310` | l.435469; l.435489 |
| ℓ | `240` | `240` | l.435494; l.435498 |
| γ̂₀,s | `153.03534675615212527964205816554809843400447427293` | `131.44792489251557427393173642186540317627445819075` | l.435494; l.435498 |
| σ̂²_bloc,s | `3837.3644239148386709307388556071047850697416032311` | `4444.2268779663177986090438425985366511755710614584` | l.435494; l.435498 |
| FIV_s | `114.67667682132543551816351669459307932477895917439` | `266.31206692493364443057277635430175333060222847741` | l.435495; l.435499 |
| R_centrage,s | `4.5733433324247139833425606396397303313682246279750` | `7.8767735159232268649296718039283324323387017357003` | l.435495; l.435499 |
| FIV_série,s | `25.075020282924108215938185508697612502356118056163` | `33.809791075822184156289564915103491737231918165960` | l.435495; l.435499 |
| z_bloc,s | `1.9450967130759827973431520036612640074344098711768` | `1.7443544612798118150330419847751992092506597257981` | l.435496; l.435500 |
| maximal run of I_t | `6` | `2` | l.435497; l.435501 |
| EMD_s (windows) | `196.46940578076511214605312297686775770638678422511` | `211.43482468284790300599634573463971654187425170170` | l.435518; l.435521 |
| fraction EMD_s/n_s | `0.0079914340362320566258309181605396688105099363117799` | `0.018551796497573738966920798958904950122126371124129` | l.435518; l.435521 |
| rule value (pt 5) | NE REJETTE PAS (discordance) | NE REJETTE PAS (discordance) | l.435516; l.435519 |

Reading (roundings flagged): in calm, n = 24,585, K = 154, P̂_more ≈ 0.00136, guard ≈ 33.5 (met), z_s ≈ 20.8 ≥ 2.33 and z_bloc ≈ 1.95 < 2.33; in stress, n = 11,397, K = 133, P̂_more ≈ 0.00147, guard ≈ 16.7 (met), z_s ≈ 28.5 ≥ 2.33 and z_bloc ≈ 1.74 < 2.33. Both strata are tested: §5.4 guard met, σ̂²_bloc,s > 0 and n_s ≥ 30·ℓ = 7,200, hence z_bloc,s published (pts 2, 3 and 5).

[calc] By construction (same numerator K_s − n_s·P̂_more,s, package pt 3), z_bloc,s = z_s/√FIV_s: the difference between the two statistics is carried entirely by FIV_s ≈ 115 in calm and ≈ 266 in stress, product of R_centrage,s (≈ 4.57; ≈ 7.88) and of FIV_série,s (≈ 25.1; ≈ 33.8). The report draws no cause from it (pt 8).

### 3.2 Printed statements (pt 8), word for word

Lines J28 l.435515 to l.435522, copied by extraction (`sed -n '435515,435522p'`):

```text
  ── règle SHOGEN-CRITERE-R1-1 (ADR-0028 §1 bis.1 pts 1-11 ; forme scellée) : valeur par strate ; comparaisons sur les Decimal publiées, non arrondies, au seuil 2.33, « ≥ » ; aucune p-valeur
    « calme » : z_s = 20.829495417808173515660354538360738280133057485734 ≥ 2,33 ; z_bloc = 1.9450967130759827973431520036612640074344098711768 < 2,33 → NE REJETTE PAS (discordance)
    « calme » : « le modèle binomial de doc 10 §5.1, à fenêtres indépendantes, est rejeté ; la cause n'est pas identifiée entre co-défaillance des sources et dépendance sérielle des fenêtres »
    « calme » : EMD_s = (2,33 + 0,8416)·max(√(n_s·P̂_more,s·(1 − P̂_more,s)), σ̂_bloc,s) = 196.46940578076511214605312297686775770638678422511 fenêtres ; fraction de n_s = 0.0079914340362320566258309181605396688105099363117799 (puissance 0,8 : choix de conception ; aucun seuil sur l'EMD)
    « stress » : z_s = 28.466243694685921454102240881955034913016073716310 ≥ 2,33 ; z_bloc = 1.7443544612798118150330419847751992092506597257981 < 2,33 → NE REJETTE PAS (discordance)
    « stress » : « le modèle binomial de doc 10 §5.1, à fenêtres indépendantes, est rejeté ; la cause n'est pas identifiée entre co-défaillance des sources et dépendance sérielle des fenêtres »
    « stress » : EMD_s = (2,33 + 0,8416)·max(√(n_s·P̂_more,s·(1 − P̂_more,s)), σ̂_bloc,s) = 211.43482468284790300599634573463971654187425170170 fenêtres ; fraction de n_s = 0.018551796497573738966920798958904950122126371124129 (puissance 0,8 : choix de conception ; aucun seuil sur l'EMD)
  « R1 discrimine » (§1 bis.1 pt 6 ; déclencheur de D6 (vi) et D9) = FAUX : aucune strate ne rejette ; strate(s) testée(s) : calme, stress
```

The discordance case (guard met, z_s ≥ 2.33, published z_bloc,s < 2.33) has the value NE REJETTE PAS; the stratum prints the discordance statement and EMD_s, and not the statement « n'est pas rejeté » [*is not rejected*]; this case is never a VRAI (package §10.2 pts 5 and 8). This “single test” reading of the discordance was ratified by the orchestrator on 2026-09-30, subject to veto, before the sealing (package §10.1). EMD_s = (2.33 + 0.8416)·max(√(n_s·P̂_more,s(1−P̂_more,s)), σ̂_bloc,s): the power 0.8 is a design choice, without any threshold on the EMD (pt 8). Here the maximum is σ̂_bloc,s in both strata [calc: √σ̂²_bloc,s ≈ 61.9 and ≈ 66.7 against √guard ≈ 5.78 and ≈ 4.09].

### 3.3 « R1 discrimine »

« R1 discrimine » has the value FAUX: « aucune strate ne rejette ; strate(s) testée(s) : calme, stress » [*no stratum rejects; stratum(s) tested: calm, stress*] (J28 l.435522). By pt 6, FAUX means that no stratum REJETTE, that at least one NE REJETTE PAS and that none is in a non-qualifiable rejection. It is the trigger of D6 (vi) and of D9 (§1, decisions of the investor).

### 3.4 Bonferroni family and premise of the bound (pt 7)

Printed line (J28 l.435503):

```text
  famille de Bonferroni pré-enregistrée (ADR-0028 D2 pt 4) : m = 2 (strates testées : calme, stress ; m ≤ 2 ; §1 bis.1 pt 6), tests unilatéraux au seuil 2,33 ; borne P(au moins un rejet à tort) ≤ 2 × 0,01 = 0,02 sous le modèle nul joint (§1 bis.1 pt 7) : modèle d'indépendance du pool de doc 10 §5.1 et dépendance sérielle des fenêtres de portée < ℓ = 240 (A(window-dependence), registre 08) ; niveau asymptotique, non démontré ≤ 0,01 en échantillon fini (SHOGEN-SIM-NIVEAU-1)
```

Premise, quoted from package §10.2 pt 7: “The bound holds under the joint null model: the independence model of the pool of doc 10 §5.1, with a serial dependence of the windows of range < ℓ (A(window-dependence), doc 08). The level is asymptotic […]. It is conservative under iid windows (plug-in of P̂_more). It is not demonstrated ≤ 0.01 in finite samples”. The measurements of SIM-NIVEAU and of step S, made before the sealing on synthetic data only (package §10.3), say nothing about the real sources: under the simulated null model, the false-rejection rate of the rule ranges from 0.001590 (SE 0.000126) to 0.001810 (SE 0.000134) with independent windows, and stays at most 0.00357 (SE 0.00034) near the guard; that of z_s alone reaches 0.337300 (SE 0.001495) under serial dependence (mean runs of 60 windows) (package §10.3, tables l.139-148 and l.153-162). By pre-declared consequence, these outputs modify neither ℓ, nor the threshold, nor the rule (pt 7).

### 3.5 Anomalies per feed (block 3)

p̂ᵢ = anomalies of the feed / n_s; the complete values of p̂ᵢ are at the lines cited. « nonÉv » [*not evaluable*] counts the cells not evaluable on the out-of-envelope axis, which are not anomalies (J28 l.435448).

| feed | class | calm: anomalies (panne / stale / horsE / nonÉv) [*outage / stale / out-of-envelope / not evaluable*] | stress: anomalies (panne / stale / horsE / nonÉv) | J28 |
|---|---|---|---|---|
| binance | `sans_horodatage` | 372 (372 / 0 / 0 / 0) | 46 (46 / 0 / 0 / 0) | l.435453; l.435473 |
| coinbase | `place_horodatee` | 56 (56 / 0 / 0 / 0) | 11 (11 / 0 / 0 / 0) | l.435454; l.435474 |
| kraken | `sans_horodatage` | 34 (34 / 0 / 0 / 0) | 46 (46 / 0 / 0 / 0) | l.435455; l.435475 |
| okx_ticker | `place_horodatee` | 64 (64 / 0 / 0 / 0) | 6 (6 / 0 / 0 / 1) | l.435456; l.435476 |
| okx_index | `place_horodatee` | 64 (64 / 0 / 0 / 0) | 7 (7 / 0 / 0 / 1) | l.435457; l.435477 |
| bitstamp | `place_horodatee` | 475 (475 / 0 / 0 / 0) | 39 (39 / 0 / 0 / 0) | l.435458; l.435478 |
| gemini | `place_horodatee` | 68 (65 / 3 / 0 / 0) | 21 (19 / 2 / 0 / 0) | l.435459; l.435479 |
| bitfinex | `sans_horodatage` | 32 (30 / 0 / 2 / 0) | 51 (51 / 0 / 0 / 0) | l.435460; l.435480 |
| coingecko | `agregateur` | 56 (56 / 0 / 0 / 0) | 127 (127 / 0 / 0 / 1) | l.435461; l.435481 |
| defillama | `agregateur` | 159 (158 / 1 / 0 / 0) | 226 (226 / 0 / 0 / 0) | l.435462; l.435482 |
| chainlink | `oracle_chainlink` | 71 (69 / 0 / 2 / 0) | 113 (113 / 0 / 0 / 0) | l.435463; l.435483 |

## 4. Flags and R2 (blocks 5 and 6 of J28)

### 4.1 Certificate head (block 6), copied

Lines J28 l.435779 to l.435797, copied by extraction (`sed -n '435779,435797p'`):

```text
  k nominal = 10 (hôtes distincts du pool)
  k_eff     = 4  — k_eff = nombre de classes de la partition R2 measured (§5.6)
  date de la partition, axe ASN (ADR-0026 déc. 1 ; HS2-07) = relevé asn_attribution retenu (dernier par hôte, après filtre de lecture) : min 1790558275.4337332 = 2026-09-28T01:17:55.433733+00:00 ; max 1790558282.5194278 = 2026-09-28T01:18:02.519428+00:00 ; 10 / 10 hôtes du pool — descriptif seulement (ADR-0028 annexe D.5)
  relevés asn_attribution retenus sans ts (hôtes du pool, entrée malformée) = 0 — comptés à part, hors date de la partition (SHOGEN-BLOC6-TS-1)
  R3 (déclaration : entité légale, juridiction, méthodologie annoncée) ne modifie JAMAIS k_eff (§5.6 / 04 §3) — seuls les recouvrements R2 measured partitionnent.
  PARTITION NOMMÉE (ADR-0007 : nomme l'amont, jamais un compte anonyme) :
    cluster = {api-pub.bitfinex.com, api.coingecko.com, api.exchange.coinbase.com, api.kraken.com, coins.llama.fi, ethereum-rpc.publicnode.com, www.okx.com} via AS13335 CLOUDFLARENET - Cloudflare, Inc. [fusion ASN partagé AS13335 CLOUDFLARENET - Cloudflare, Inc. — côté livraison (§4.1, résidu 1)] ; flux = ['bitfinex', 'chainlink', 'coinbase', 'coingecko', 'defillama', 'kraken', 'okx_index', 'okx_ticker']
        amont déclaré (basis:doc, ne fusionne pas) : binance → coingecko (coingecko.com/en/exchanges/binance)
        amont déclaré (basis:doc, ne fusionne pas) : coinbase → pyth (pyth.network/publishers)
        amont déclaré (basis:doc, ne fusionne pas) : coingecko → defillama (docs.llama.fi/llms-full.txt)
        caveat : chemin de LECTURE ≠ amont (§3.2) : l'ASN mesuré est celui du fournisseur RPC (ethereum-rpc.publicnode.com), une infrastructure de lecture, pas l'amont du feed
    cluster = {api.binance.com} via AS16509 AMAZON-02 - Amazon.com, Inc. ; flux = ['binance']
        amont déclaré (basis:doc, ne fusionne pas) : binance → coingecko (coingecko.com/en/exchanges/binance)
    cluster = {api.gemini.com} via AS14618 AMAZON-AES - Amazon.com, Inc. ; flux = ['gemini']
    cluster = {www.bitstamp.net} via AS19551 INCAPSULA - Incapsula Inc ; flux = ['bitstamp']
  DRAPEAU 1 « historique insuffisant » (§5.4) par strate : {'calme': False, 'stress': False}
  DRAPEAU 2 « co-défaillance observée non expliquée par les axes R2 » (§5.6) : état = ETEINT
      « R1 discrimine » FAUX : le modèle d'indépendance n'est rejeté dans aucune strate testée (bloc 3)
      entrées (ADR-0028 §1 bis.1 pt 10) : « R1 discrimine » = FAUX (bloc 3) ; k_eff = 4 ; k nominal du segment (hôtes) = 10 ; k nominal_s (flux du pool de la strate) : « calme » = 11, « stress » = 11 — comparaison hétérogène déclarée ; strate poolée hors des entrées
```

- **Named and dated partition**: four classes on the ASN axis, including a cluster of seven hosts and eight feeds merged on AS13335 (Cloudflare), « côté livraison » [*delivery side*] (residual 1 of doc 10 §4.1), and three singletons: `api.binance.com` (AS16509), `api.gemini.com` (AS14618), `www.bitstamp.net` (AS19551). Date: retained `asn_attribution` probe records, last per host, between 2026-09-28T01:17:55Z and 01:18:02Z, 10 hosts out of 10 (l.435781). The `basis:doc` edges (binance → coingecko, coinbase → pyth, coingecko → defillama) are declared upstreams: they do not merge (ADR-0008, recalled at l.435786-435788).
- **k_eff = 4, nominal k = 10** (distinct hosts of the pool, l.435779-435780); nominal k_s = 11 feeds in each stratum, « comparaison hétérogène déclarée » [*heterogeneous comparison declared*] (l.435797). k_eff is not an independence count: it is the number of classes of the observed R2 partition (doc 10 §5.6); z is never composed into k_eff.
- **Flag 1** « historique insuffisant » [*insufficient history*]: false in both strata (l.435794).
- **Flag 2** « co-défaillance observée non expliquée par les axes R2 » [*co-failure observed, not explained by the R2 axes*]: **ÉTEINT** [*off*] (l.435795). By pt 10, the flag is off as soon as « R1 discrimine » is FAUX; its inputs are printed (l.435797), pooled stratum excluded. The flag is a signal on A(axis-coverage), never the rule (pt 10).

### 4.2 R2 in summary (block 5)

- **(a) ASN axis** (l.435673-435691): 10 hosts, one retained probe record each, the last one (2026-09-28T01:17:55Z to 01:18:02Z), resolver `cloudflare-dns.com`, cross attribution RIPEstat and Team Cymru « concordant » for the 10. One measured overlap: AS13335 shared by `api-pub.bitfinex.com`, `api.coingecko.com`, `api.exchange.coinbase.com`, `api.kraken.com`, `coins.llama.fi`, `ethereum-rpc.publicnode.com` and `www.okx.com` (l.435691). Printed CNAME chains: binance to CloudFront, gemini to an AWS load balancer, bitstamp to Incapsula, okx to Cloudflare's CDN (l.435678, l.435682, l.435687, l.435689).
- **(b) Content axis** (l.435693-435752): 35,982 windows; N_min = 300 common windows per pair (design choice); sole merging criterion v0: exact identity (T = 1) on at least N_min common windows (l.435695). No pair is merged on this axis: the list of exact copies of the third-party recomputation is empty (RT l.10991). The per-pair statistics (ρ_raw, ρ_resid, T, T_Δ, co-aberrance, lag) are descriptive; the USDT/USD peg gap is carried by ρ_resid (J28 l.47). The serial dependence on this axis is out of scope (SHOGEN-CONTENU-DEP-1, §11).
- **(c) Method axis** (l.435754-435764): five `basis:doc` entries (three upstream edges: binance → coingecko, coinbase → pyth, coingecko → defillama; two estimator declarations: coingecko, pyth), which trigger (b) and do not partition.
- **(d) Correlations between clusters**: the rendering prints « aucun cluster à ≥ 2 flux (1) → tout reste au φ par paire de flux (bloc 4) » [*no cluster with ≥ 2 feeds (1) → everything stays at the φ per pair of feeds (block 4)*] (l.435767). The JSON of the third-party recomputation carries, for J28, `"cluster_pairs": {}` and `"n_multi_clusters": 1` (RT l.10985-10987). [report finding] The label reads poorly next to block 6, which names a cluster of eight feeds: the partition counts a single cluster of at least two members, hence no pair of such clusters, and the main D3 estimator between clusters (correlation of the Θ̂ series, analogue of eq. 35 of L&M) has no object on J28.
- **(e) The seven residuals of the ASN axis** are printed with the table (l.435769-435776), notably: fronting (k_eff counted on the delivery side), single-vantage, instantaneity (dated attribution, re-measured at each quorum), and the measurement path that belongs to the measured class.

### 4.3 ASN divergences for hosts outside the pool (SHOGEN-ASN-DIVERGENCE-HORS-POOL-1, annex B.44)

No ASN divergence appears in the renderings. A search for the string `DIVERGENCE` gives 0 lines in J14p, J14s, J28, RT and RAW, and a single one in SUITE, which is a test name (SUITE l.379); the JSON of the third-party recomputation carries `"asn_divergences": []` in its four entries (RT l.4522, l.8900, l.13335, l.18099). There is therefore no line to label or to remove: the case that the item anticipated (probe records of hosts removed by D1 case (a), that is, of Pyth) does not arise in these renderings.

### 4.4 Caveats of the reading path (RPC)

- Chainlink is read by `eth_call` on the public RPC `ethereum-rpc.publicnode.com` (doc 10 §1, non-goal 4; J28 l.435685). The rendering says so: « chemin de LECTURE ≠ amont (§3.2) : l'ASN mesuré est celui du fournisseur RPC (ethereum-rpc.publicnode.com), une infrastructure de lecture, pas l'amont du feed » [*READING path ≠ upstream (§3.2): the measured ASN is that of the RPC provider (ethereum-rpc.publicnode.com), a reading infrastructure, not the upstream of the feed*] (l.435789). The classification of chainlink in the AS13335 cluster therefore bears on the reading infrastructure.
- Same rule for any host served behind a CDN: the observed IP is the delivery layer, not the origin (residual 1, l.435770).
- Pyth, read through an HTTP service that answered 401 from the first day (ADR l.25), is outside the analysis pool (§2.2): no measurement of this report bears on it.

## 5. Pre-registered descriptives (annex D.5, package §11), hors décision

These treatments are descriptive, hors décision and without parameters; none enters the rule or the closed list of sensitivities (package §11; printed label, J28 l.435524).

### 5.1 Observed τ against committed τ (SHOGEN-TAU-REDERIV-1)

The τ committed before the campaign serves all the confirmatory tests; the observed τ is defined in advance: P99 and maximum of |p − médiane_LOO|/médiane_LOO of the (window, feed) cells that reached the out-of-envelope axis, per class, over the segment, without re-estimation (J28 l.435525; package §11).

| class | τ_classe (committed) | N cells | observed P99 | observed maximum | J28 |
|---|---|---|---|---|---|
| `agregateur` | `0.026` | 71395 | `0.0029870446819581321147177994146356252452815395638463` | `0.017649908208186827670019929236496737002324764533848` | l.435526 |
| `oracle_chainlink` | `0.0165` | 35800 | `0.0045133817598667881395689083527158792588820593853894` | `0.017842859661860400175061719273882056236385914669308` | l.435527 |
| `oracle_pyth` | `0.0015` | 0 | not defined | not defined | l.435528 |
| `place_horodatee` | `0.0045` | 179097 | `0.00084986241659292805372128990214331880618269790009557` | `0.0031005971796576586758169290273558058198265570013814` | l.435529 |
| `sans_horodatage` | `0.0045` | 107367 | `0.0016680227037502354455795456531406013037374194387754` | `0.0084293722922191923975621436933888192128120065521140` | l.435530 |

[calc] The observed P99 is below τ_classe in the four defined classes (P99/τ ratios ≈ 0.115; 0.274; 0.189; 0.371). The observed maximum exceeds τ_classe for `oracle_chainlink` (≈ 1.08 τ) and `sans_horodatage` (≈ 1.87 τ), which is consistent with the out-of-envelope cells counted in block 3 (chainlink and bitfinex, 2 each in calm, §3.5). A divergence between observed τ and projected τ is a finding, not a silent re-tune (ADR-0022 pt 3, cited by package §12 pt 13); the re-derivation is PX-Shogen-13, after the rendering, never applied to the confirmatory z. Reservation already written (annex B.45, note to PX-Shogen-13): the observed τ (out-of-envelope axis reached) and the calibration P99 (all evaluable cells) do not bear on the same population.

### 5.2 Decomposition of K by `panne_transport` readings (SHOGEN-HOST-DEGRADED-1)

Lines J28 l.435531 to l.435533, copied by extraction:

```text
    décomposition de K (SHOGEN-HOST-DEGRADED-1) par nombre de lectures présentes au statut panne_transport (model.Status) des flux du pool D1 de la strate ; c_s = fenêtres où chaque flux du pool porte une lecture panne_transport ; le z confirmatoire inclut les modes communs de l'observateur (hôte, DNS, réseau)
    « calme » : K = 154 = K[≥ 2 panne_transport] 153 + K[1] 1 + K[0] 0 ; K[tous les écarts hors_enveloppe] = 0 ; c_s = 9
    « stress » : K = 133 = K[≥ 2 panne_transport] 133 + K[1] 0 + K[0] 0 ; K[tous les écarts hors_enveloppe] = 0 ; c_s = 0
```

In calm, 153 of the 154 windows counted in K carry at least two readings with status `panne_transport` among the feeds of the stratum's pool, one carries one, none carries zero; in stress, the 133 carry at least two. No window of K has all its anomalies on the out-of-envelope axis. c_s, the number of windows in which each feed of the pool carries a `panne_transport` reading, is 9 in calm and 0 in stress. This descriptive identifies no cause: it describes the composition of K, which the rule does not read. The sensitivity that removes the windows with a degraded-host diagnostic is a post-execution item, not done at the date of the report (SHOGEN-HOST-DEGRADED-2, §11).

### 5.3 Censoring: skipped windows and non-outer bounds (SHOGEN-CENSURE-INFO-1)

The skipped windows are counted in §2.6 (J28 l.37-41). Under the assumption H_perte (A(loss-non-informative): tooling losses are non-informative), the rendering prints bounds at fixed P̂_more, with s = skipped windows of the stratum: z_bas = (K − (n+s)·P̂)/√((n+s)·P̂(1−P̂)) and z_haut = (K + s − (n+s)·P̂)/√((n+s)·P̂(1−P̂)), then the same with σ̂_bloc,s in the denominator (J28 l.435535). Printed header line: « bornes à P̂_more fixé, non extérieures ; verdict non identifié sous censure arbitraire des fenêtres sautées » [*bounds at fixed P̂_more, non-outer; verdict not identified under arbitrary censoring of the skipped windows*] (l.435534).

| stratum | s (skipped windows) | z_bas | z_haut | z_bas with σ̂_bloc | z_haut with σ̂_bloc | J28 |
|---|---|---|---|---|---|---|
| calm | 5701 | `17.556689997555283653681146237762934756839540547496` | `905.50199539544630203447432173216643843074844907832` | `1.8196629136861220471711460494461585204157608817430` | `93.850742908789397830496314603025603356370670497401` | l.435536 |
| stress | 2094 | `25.473078564141066684303998709584385344769540455886` | `496.61005684969625124835679931557781942595489865145` | `1.6982937424929091779945784909896792520918497568624` | `33.109062569066257260750656346574928093519208266497` | l.435537 |

These bounds are labelled « non extérieures » [*non-outer*] and carry no identification reading (annex D.5; CV2-24): imputing an anomaly to a censored window also raises P̂_more, so that the lower bound is not outer. The loss counts measure the extent of the censoring, not its non-informative character (package §12 pt 14). The outer bounds are item SHOGEN-CENSURE-INFO-2, after the execution (§11).

### 5.4 Diagnostic of runs of I_t and FIV

- Runs of I_t = 1{m_t ≥ 2} (hors décision; J28 l.435497, l.435501): in calm, 119 runs, mean length `1.2941176470588235294117647058823529411764705882353`, maximal run 6; in stress, 130 runs, mean length `1.0230769230769230769230769230769230769230769230769`, maximal run 2. [calc] The mean length is K_s divided by the number of runs (154/119 and 133/130).
- The maximal run stays below ℓ = 240 in both strata: the flag « run maximal ≥ ℓ : σ̂²_bloc,s biaisé vers le bas ; SHOGEN-DEP-FENETRES-2 prioritaire avant G10 » [*maximal run ≥ ℓ: σ̂²_bloc,s biased downward; SHOGEN-DEP-FENETRES-2 a priority before G10*] (pt 9) is not printed; in J28, the phrase appears only in the head label (l.1).
- FIV_s and its two factors are in §3.1 (l.435495, l.435499); the theoretical coefficient of variation of σ̂²_bloc,s, √(4ℓ/(3n)), is `0.11408797792643129814123654880491384644099142081780` in calm and `0.16756361261114975367661284639462247100481161298594` in stress (l.435494, l.435498), marked « [inféré : dérivation de l'AVIS-advisor-defi Q1 (iv)] » [*[inferred: derivation from the AVIS-advisor-defi Q1 (iv)]*] by the rendering (l.435493).

## 6. Lift and φ identity of D3 (SHOGEN-D3-LIFT-1, annex B.42)

D3 (package §5, quoted in substance): between singletons of the R2 partition, φ of the anomaly indicators remains the main estimator; for the pairs of singletons (2×2 tables), the lift (left-hand side of eq. 28 of L&M) is a declared secondary; “No significance per pair: this is descriptive”; the identity φ = (lift−1)·√(p_A p_B / ((1−p_A)(1−p_B))) must be published, “which makes the mention ‘noisy proxy’ exact”, and the four counts per pair. The renderings do not compute the lift (finding B-2 of review R-B, annex B.42): it is recomputed here by the drafter, in exact arithmetic, from the four counts printed in block 4 of J28 alone.

- **Pairs concerned**: the J28 partition counts three singletons, {binance}, {gemini} and {bitstamp} (J28 l.435790, l.435792, l.435793), hence three pairs of singletons per stratum.
- **Definitions**: n = n11 + n10 + n01 + n00; p_A = (n11 + n10)/n; p_B = (n11 + n01)/n; lift = p_AB/(p_A·p_B) = n11·n/((n11 + n10)(n11 + n01)); φ = (n11·n00 − n10·n01)/√((n11 + n10)(n01 + n00)(n11 + n01)(n10 + n00)).
- **Method**: script `d3_lift.py` (standard library, `fractions` and `decimal` to 80 digits), filed in the project repository with this report (sha256 `8f91474cdded5694e733334fadf225b110d3378ddb560f1bee4066eca80f9381`; output `d3_lift.sortie.txt`, sha256 `77ae69ec8666065d0e7ec3a13588f982d87de7bf1789ffe3f91813ea028dc73f`). The identity is checked exactly: φ² and (lift − 1)²·p_A·p_B/((1 − p_A)(1 − p_B)) are two equal rationals, and φ has the sign of lift − 1. Self-test on two tables computed by hand ([2 1 1 6]: lift = 20/9, φ = 11/21; [0 5 5 90]: lift = 0, φ = −1/19), which fails under a mutated identity.

[calc] Output of the script, put in a table (`table_lift.py`, string rewriting); the exact lift is an irreducible fraction, its decimals are rounded to 12 significant figures:

| stratum | pair | [n11 n10 n01 n00] (J28) | p_A; p_B | lift (exact) | lift ≈ | √(p_A·p_B/((1−p_A)(1−p_B))) ≈ | (lift − 1)·√(…) ≈ | printed φ (block 4) | exact identity |
|---|---|---|---|---|---|---|---|---|---|
| calm | binance×bitstamp | [52 320 423 23790] (l.435547) | 124/8195; 95/4917 | 21307/2945 | 7.23497453311 | 0.0173978414435 | 0.108475098331 | `0.10847509833108362918259591106802162184159185904700` | yes |
| calm | bitstamp×gemini | [21 454 47 24063] (l.435551) | 95/4917; 68/24585 | 103257/6460 | 15.9840557276 | 0.00739211972867 | 0.110763933959 | `0.11076393395917706370581636186843800964431146805970` | yes |
| calm | binance×gemini | [20 352 48 24165] (l.435552) | 124/8195; 68/24585 | 40975/2108 | 19.4378557875 | 0.00652781686160 | 0.120358945901 | `0.12035894590128557980983967111642447373272429106910` | yes |
| stress | binance×bitstamp | [4 42 35 11316] (l.435622) | 46/11397; 13/3799 | 7598/299 | 25.4113712375 | 0.00373029540546 | 0.0910616259682 | `0.091061625968168214579556752802535961836177686365615` | yes |
| stress | binance×gemini | [3 43 18 11333] (l.435624) | 46/11397; 7/3799 | 11397/322 | 35.3944099379 | 0.00273512204339 | 0.0940729087904 | `0.094072908790429061895721354843595547904877588394058` | yes |
| stress | bitstamp×gemini | [3 36 18 11340] (l.435627) | 13/3799; 7/3799 | 3799/91 | 41.7472527473 | 0.00251765505523 | 0.102587526866 | `0.10258752686577574340266708561888701645711988440463` | yes |

In rounded reading [calc]: lift ≈ 7.23; 16.0; 19.4 in calm and ≈ 25.4; 35.4; 41.7 in stress, for printed φ from ≈ 0.108 to ≈ 0.120 in calm and from ≈ 0.0911 to ≈ 0.103 in stress. The factor √(p_A·p_B/((1−p_A)(1−p_B))) is small at low margins (from ≈ 0.00252 to ≈ 0.0174 here), and lift − 1 equals φ divided by this factor: this is the relation that the package publishes to make the mention “noisy proxy” exact. No decision reading is drawn from it, no per-pair significance is computed, and the conditional odds ratio, exploratory and without a method fixed at the sealing, is not computed (package §5).

Check of the 110 tables of block 4 [calc]: the identity is exact on 110 tables out of 110 (55 per stratum), and the recomputed φ differs from the printed φ by at most 2.38·10⁻⁵⁰ in absolute value (output `d3_lift.sortie.txt`, l.2-3). The lift is published only for the pairs of singletons, the only ones targeted by D3.

## 7. Outputs hors décision (package §10.2 pt 9)

Pt 9 lists them: main and second J14 (non-confirmatory), pooled stratum (exploratory), sensitivities « plage incluse » (biased upward by construction) and « seconde coupe » [*second cut*], L&M (block 4), exact tails, run diagnostic. **None changes the verdict**: the rule is evaluated on J28 alone, D5 range excluded (pt 1), and « R1 discrimine » there has the value FAUX (§3.3). Each output is reproduced with the label that the rendering prints at its head.

### 7.1 Main J14

Label (J14p l.1):

```text
[ÉTIQUETTE] j14-principal : hors décision, non confirmatoire (ADR-0028 D4, §1 bis.1 pt 9) ; plage D5 non passée : hors du segment (D2 pt 6 l'applique au J28)
```

Segment `[1787770800 ; 1788980400) = [2026-08-26T19:00:00+00:00 ; 2026-09-09T19:00:00+00:00)` (J14p l.31), ex ante rule of ADR-0022 pt 5 (D4); Pyth removed from both strata, case (a): 0 `ok` readings out of 13,373 and out of 3,941 (l.38-39); skipped windows 1,027 and 1,819 (l.33).

| J14p: quantity | calm | stress | J14p |
|---|---|---|---|
| n_s | `13373` | `3941` | l.209555; l.209575 |
| K_s | `50` | `8` | l.209555; l.209575 |
| P̂_more,s | `0.0013938968610775433013870221315659599986142913741574` | `0.00035260783541832319883608669380651774613270860280165` | l.209571; l.209591 |
| guard (threshold 10) | `18.614599673443475762938726299057869492601437469783` | `1.3891374858460684507352497516803467029217226329697` | l.209572; l.209592 |
| z_s | `7.2684387263613165124682538101673599947301495076272` | not published (guard §5.4) | l.209573; l.209593 |
| z_bloc,s | `2.6455172861617278377464936516549168389991781470697` | not published (block guard, n_s < 7200) | l.209601; l.209605 |
| rule value (hors décision) | REJETTE | NON ÉVALUABLE : strate non testée, hors décision (§1 bis.1 pt 2) [*not evaluable: stratum not tested, outside the decision (§1 bis.1 pt 2)*] | l.209620; l.209622 |

Lines of the rule (J14p l.209619 to l.209623), copied by extraction:

```text
  ── règle SHOGEN-CRITERE-R1-1 (ADR-0028 §1 bis.1 pts 1-11 ; forme scellée) : valeur par strate ; comparaisons sur les Decimal publiées, non arrondies, au seuil 2.33, « ≥ » ; aucune p-valeur
    « calme » : z_s = 7.2684387263613165124682538101673599947301495076272 ≥ 2,33 ; z_bloc = 2.6455172861617278377464936516549168389991781470697 ≥ 2,33 → REJETTE
    « calme » : « le modèle d'indépendance du pool (k nominal_s = 11 flux du pool de la strate, bloc 1 ; k_eff mesuré ≤ 10 (borne supérieure), bloc 6) est rejeté dans la strate calme sur 13373 fenêtres, axes panne / staleness / hors-enveloppe (résidu : staleness fail-open : binance, kraken, bitfinex), tel qu'observé par cet instrument (hôte, DNS et réseau du harnais compris) ; aucune dépendance de paire n'est établie »
    « stress » : z_s non publié (garde §5.4 : n·P̂_more·(1 − P̂_more) < 10) → NON ÉVALUABLE : strate non testée, hors décision (§1 bis.1 pt 2)
  « R1 discrimine » (§1 bis.1 pt 6 ; déclencheur de D6 (vi) et D9) = VRAI : strate(s) qui rejettent : calme
```

The family counts m = 1 (l.209608); the pooled stratum is not published, the stress stratum being under the guard (l.209614). In block 6, the ten ASN probe records retained at the end of the segment (2026-09-09T18:49Z to 18:51Z) are all `resolve_failed` (J14p l.209777-209786): k_eff is known only as an upper bound, « k_eff ≤ 10 (BORNE SUPÉRIEURE) » [*k_eff ≤ 10 (UPPER BOUND)*] (l.209876); flag 1 true in stress only (l.209907); flag 2 not evaluable, « ni levé ni éteint » [*neither raised nor off*] (l.209908-209909), by reading (a) of pt 10. J14 is non-confirmatory and its publication is a decision of the investor (D4; decision 270). **This « R1 discrimine » VRAI is hors décision and does not change the verdict** (pts 1 and 9).

### 7.2 Second J14 (« seconde coupe » sensitivity)

Label (J14s l.1):

```text
[ÉTIQUETTE] j14-second : sensibilité de la liste fermée (seconde coupe, décision 270), hors décision, non confirmatoire ; plage D5 non passée : hors du segment (D2 pt 6 l'applique au J28)
```

Segment `[1787770800 ; 1788480060) = [2026-08-26T19:00:00+00:00 ; 2026-09-04T00:01:00+00:00)` (J14s l.31), cut « ≤ 2026-09-04T00:00Z » of decision 270 (D4); Pyth removed from both strata, case (a) (l.38-39).

| J14s: quantity | calm | stress | J14s |
|---|---|---|---|
| n_s | `8121` | `1140` | l.112112; l.112133 |
| K_s | `5` | `1` | l.112112; l.112133 |
| P̂_more,s | `0.000014316253783038939038177418104725077784697432524987` | `0.000021469618207937163532218656623490189731153357463892` | l.112128; l.112149 |
| guard (threshold 10) | `0.11626063253151037288958691789311493515448564399261` | `0.024474839280311532597570565581073686929332258857146` | l.112129; l.112150 |
| z_s | not published (guard §5.4) | not published (guard §5.4) | l.112130; l.112151 |
| z_bloc,s | `2.0943484839416630978298953875433710863142063001875` | not published (block guard, n_s < 7200) | l.112159; l.112163 |
| rule value (hors décision) | NON ÉVALUABLE : strate non testée, hors décision (§1 bis.1 pt 2) | NON ÉVALUABLE : strate non testée, hors décision (§1 bis.1 pt 2) | l.112178; l.112179 |

Both strata are under the §5.4 guard, hence not tested: « R1 discrimine » = NON ÉVALUABLE, « aucune strate testée » [*no stratum tested*] (J14s l.112180); m = 0 (l.112166). In calm, z_bloc is printed (block guard met, n_s ≥ 7,200), but the value of the stratum remains NON ÉVALUABLE, the §5.4 guard taking precedence (pt 5). Block 6: k_eff = 4 for nominal k = 10 (l.112437-112438), partition dated from 2026-09-03T23:56:54Z to 23:57:06Z (l.112439); flags 1 true in both strata (l.112452); flag 2 not evaluable (l.112453-112454). **Hors décision; does not change the verdict.**

### 7.3 Pooled stratum (exploratory, outside the family, hors décision)

On J28, stratified form of D2 pt 4, each stratum on its D1 pool (J28 l.435505-435510):

- z_pool = `33.435366780260737654814166344529336014557255168635` (l.435510);
- Σ_s (K_s − n_s·P̂_more,s) = `236.77931489141074698973370238916004307092589875631` and Σ_s n_s·P̂_more,s(1 − P̂_more,s) = `50.150507915819141795538676919575811501998150245996` (l.435509).

Reading: z_pool ≈ 33.4 ([calc] recounted at 33.4353667803 from the two printed sums). The pooled stratum is never among the inputs of the rule nor among those of flag 2 (pt 9; « strate poolée hors des entrées » [*pooled stratum outside the inputs*], l.435797). Its normal approximation is not measured (SHOGEN-POOLEE-BLOC-1, §11). It is published in neither of the two J14 renderings (strata under the guard, J14p l.209614, J14s l.112172). **Hors décision; does not change the verdict.**

### 7.4 « plage incluse » sensitivity (closed list, D2 pt 7)

[SENSIBILITÉ] section of J28 (l.435799-435820). Printed label: « variante “exclue” = principale (blocs 1-6) ; variante “incluse” = sensibilité — biaisée vers le haut par construction ; documente l'exclusion D5 ; pas un estimateur alternatif » [*variant ‘excluded’ = main (blocks 1-6); variant ‘included’ = sensitivity — biased upward by construction; documents the D5 exclusion; not an alternative estimator*] (l.435800, inner quotation marks rendered as “ ”); « motif de l'exclusion (harnais dégradé, […]) : causalité non établie » [*reason for the exclusion (degraded harness, […]): causality not established*] (l.435801). R1 alone per variant, neither L&M nor R2 (l.435802).

| stratum | variant | n | K | P̂_more | z | flag 1 | J28 |
|---|---|---|---|---|---|---|---|
| calm | excluded (main) | 24585 | 154 | `0.0013629504227977629135010363906355205959215005903986` | `20.829495417808173515660354538360738280133057485734` | False | l.435807 |
| calm | included (sensitivity) | 26294 | 408 | `0.0039561837661865178605964292161309130218132671860844` | `29.863015876556250088619968054838673686543339634366` | False | l.435808 |
| stress | excluded (main) | 11397 | 133 | `0.0014663989614904143004161900453685779659861375123928` | `28.466243694685921454102240881955034913016073716310` | False | l.435810 |
| stress | included (sensitivity) | 12306 | 133 | `0.0013272367906723694408097789913642102856351014485357` | `28.887094091051972755366700337792595909958417732478` | False | l.435811 |

- Difference in z (included − excluded): `9.033520458748076572959613516477935406410282148632` in calm (l.435809), `0.420850396366051301264459455837560996942344016168` in stress (l.435812).
- Losses by type removed by the range (SHOGEN-DP-JOURNAL-LOSS-1, l.435803-435806): those of §2.4, plus, within the range, 73 grid windows without a marker in calm and 0 in stress, and no reading absent from the windows with a marker (D1 pool of the included variant).
- Coverage per weekend: §2.5 (l.435813-435820).
- The third-party recomputation also returns the included variant of J28, under the entry label `sensibilité « plage incluse » de la liste fermée (D2 pt 7), hors décision, biaisée vers le haut par construction` [*“range included” sensitivity of the closed list (D2 pt 7), outside the decision, biased upward by construction*] (RT l.13924). There it prints z_bloc `2.5084623121105959997807452114411311466491022293836` in calm (RT l.14934) and `1.7478959678777101321272619734145717678436022586316` in stress (RT l.15167), and, in flag 2 of the variant, `"r1_discrimine": "VRAI"` (RT l.18045), `"rejette": ["calme"]` (l.18047-18049) and the state `eteint` (l.17705), with the reason printed at l.18046 (copied below). [report finding] Package §7 avoided a complete rendering of this variant, which would print « R1 discrimine » without a label (against pt 9); the JSON of the third-party recomputation carries this key for the variant, labelled at the entry level only. **Hors décision, biased upward by construction; does not change the verdict.**

```text
    "raison": "« R1 discrimine » VRAI (strate(s) : calme) mais k_eff = 4 < k nominal du segment = 10 : recouvrement R2 mesuré explique au moins en partie la co-défaillance",
```

### 7.5 L&M (block 4)

Difficulty function Θ over N = 11 feeds, D1 analysis pool (J28 l.435539); signed φ correlations per pair of feeds, complete co-anomaly matrix, « Cov<0 possible » (l.435544, l.435546).

| L&M (block 4) | calm | stress | J28 |
|---|---|---|---|
| Σ mⱼ | 1451 | 693 | l.435541; l.435606 |
| Ê(Θ) | `0.0053654297705548468208626841939837668940780594227818` | `0.0055277704659120821268754935509344564359041853119242` | l.435542; l.435607 |
| Ê(Θ²) | `0.00058498345258564904690591084733854715550871743672239` | `0.0011262932031555353482176330294256064195521947561954` | l.435543; l.435608 |
| Var̂(Θ) | `0.00055619561596289281070470998663090781236412718685660` | `0.0010957369568317254707066076636531337727625164483380` | l.435544; l.435609 |
| φ defined / 55 | 55 | 55 | l.435545; l.435610 |
| pairs with a co-anomaly (n11 > 0) | 55 | 50 | l.435545; l.435610 |

The highest φ are, in calm, kraken×bitfinex and okx_ticker×okx_index (≈ 0.454 and ≈ 0.452; l.435563, l.435548); in stress, coingecko×chainlink (≈ 0.901; l.435614), kraken×bitfinex (≈ 0.763; l.435621), defillama×chainlink (≈ 0.691; l.435613) and coingecko×defillama (≈ 0.686; l.435612). Five φ are negative in stress, none in calm (l.435662-435666). These are descriptives: no per-pair significance (D3), no pair dependence established. **Hors décision; does not change the verdict.**

### 7.6 Exact tails

Under the §5.4 guard, the renderings print the exact binomial tail hors décision (J14p l.209594; J14s l.112131, l.112152); no stratum of J28 is under the guard, and no tail is printed there. These values are not copied here (reading conventions). **Hors décision; they do not change the verdict.**

## 8. Checks of the execution

### 8.1 Seal

- **Package** `docs/adr-0028/PAQUET-PREREG-S2.md`, commit `3be95be`, sha256 `4d2a8276316b1c66a08aabb15ff3b39be812978e93dafc01a4e627f20d0af528`, written to the JOURNAL on 2026-10-03 at 01:02:51 UTC (JOURNAL l.304; `docs/adr-0028/sceau/README.md`). [calc] sha256 recounted equal on 2026-10-04.
- Timestamped **manifest** `docs/adr-0028/sceau/PAQUET.sha256`, sha256 `519423510b21ecbebda895d6e225ab0748fb0fe5a2b257a36c9301e36bfaa3e9` (recounted equal).
- **FreeTSA RFC 3161 token** `paquet.tsr`, sha256 `9edb19b53379f370e291c5da01d4df3bc269b67a44feddb589d1211ec5ec6b0e`, serial `0x08CFC8D5`, **genTime 2026-10-03T01:04:10Z**, FreeTSA's clock (README of the seal; JOURNAL l.306). Replayed by the drafter on 2026-10-04: `openssl ts -reply -in docs/adr-0028/sceau/paquet.tsr -text` prints `Time stamp: Oct  3 01:04:10 2026 GMT`; `bash scripts/sceau/verify.sh` exits 0, with `docs/adr-0028/PAQUET-PREREG-S2.md: OK` (the manifest rechecks the bytes of the package) and `Verification: OK` twice (the token against the request, then against the bytes of the manifest and the FreeTSA chain). OpenSSL's warning “is not a CA cert” bears on `tsa.crt`, passed as signing certificate and not as authority.
- **Withdrawal period** (A-7): 24 h from genTime, deadline 2026-10-04T01:04:10Z (README of the seal).
- **Opening**: go of the investor, verbatim « go exécution » [*go execution*], recorded on 2026-10-04 at 01:06:36 UTC, after the deadline (JOURNAL l.310); route (a) (token), T0 = genTime (JOURNAL l.314).
- **First seal, cited**: package `494d770d704dc7c342f0c6deec269e5642b3621bf451922f991e4ca1fb968097` (commit `ddf8c54`), manifest `680a95fdf50908cea797ae4fe9f0b42c43b5a99fcad755cb410e26fa6e794209`, token serial `0x08CC76D7`, genTime 2026-10-02T17:44:30Z (`docs/adr-0028/sceau/premier-2026-10-02/README.md`; [calc] sha256 of the manifest and genTime reread equal). It is cited because rule A-8 requires it: a seal replaced before the execution remains cited (“the first sha remains cited”, ADR §1 bis.8; package §9). It was replaced before any execution (§10.3) and no longer opens any execution (README of the first seal, addition dated 2026-10-03).
- **What the seal does not attest**: the token attests the existence of the bytes of the manifest at the latest at genTime, nothing more, and nothing about earlier readings of the data (annexes D.1, D.3); it is checked under trust in FreeTSA, an individual operator, with no service-level agreement read; the OpenTimestamps durability anchor is not done (README of the seal; package §12 pt 16).

### 8.2 Guards (annex D.4 b; package §9)

- `--gardes-seules` on the real journals at 01:11:19 UTC: « gardes levées » [*guards cleared*], exit 0; production launched at 01:11:27 UTC, process 943, author `claude-opus-5-5`, guarded head `27b0e303f196699959bddc2607db6a1d808ce0db`, route (a) (JOURNAL l.314).
- Read-only replays by the drafter, on 2026-10-04: guard (1), the sha256 of the package appears in the JOURNAL of the guarded head, l.304 (`git show 27b0e30:JOURNAL.md`, sha alone displayed); guard (2), `git diff --quiet f35a70c 27b0e30 -- s2-harness/shogen_s2 s2-harness/tools` exits 0 (likewise against heads `81c5ad7` and `25406c8` of the branch during the drafting of the report), and `f35a70c` is an ancestor of `27b0e30`; guard (4), the sha256 of `s2-harness/tools/rendu_unique.py` at commit `f35a70c` is `06d189cf84e7dca97bdfc0e1b695fc827a09473779505c7a8f1af1e7c26e9050`, equal to the key `sha256_script` of the machine block (package l.216). Guard (4) is a guard against accidental editing, not a proof (package §9).
- Guard (3): sha256 of the downloaded journals equal to the machine block and to the sums file (JOURNAL l.312; §8.3).

### 8.3 Journals and outputs

- Sealed journals (machine block, package l.217-219; JOURNAL l.312): `control.jsonl` `351f51b2e4b7421b4ee286c27465cde239124d6edd70c0e550741d22f83366ff`; `journal.jsonl` `98c5793ec460e3c009b7f743796800ae7259f71c65a4063a3c315e8eea595d74`; `raw.jsonl` `39ffb13fb0e5939ff88285ce256fbd416b0665c20ee6394c512eed7d2175c15d`; closing sums file `70910984076474987239d8c7a9da786acc95c38b375ad572d78afa297bf8caf4` (package l.220). Downloaded from a private storage without any display of content, sizes 41,676,139, 148,930,880 and 204,107,558 bytes equal to the expected ones, sha256 equal (JOURNAL l.312).
- Outputs: the seven sha256 of the conventions table, recounted by the drafter, are equal to those that the JOURNAL records (l.314) and to those of the runs of the record (ENR l.31-132).

### 8.4 Oracle record (D6 (viii))

ENR, schema `shogen.oracle-record.v1` (l.138), role `rendu` (l.15), author `claude-opus-5-5` (l.2), base `f35a70c19ba8269f1f7e2bcd31775e4fc513da20` (l.3), `ecrit` `2026-10-04T01:11:29Z` (l.4), variable `SHOGEN_S2_CAMPAGNE_CONTROL` at `null` (l.8), `exit` 0 (l.10), `paquet.sha256` equal to the sha of the package (l.12), Python `3.11.15` (l.14), `sceau.genTime` `2026-10-03T01:04:10Z` (l.136), `served_from` `null` (l.139), `static_only` `false` (l.140), `tree.commit` `27b0e303f196699959bddc2607db6a1d808ce0db` extracted by `git archive`, 436 files hashed (l.142; [calc] count of the entries). Six runs, in the order `suite`, `j14-principal`, `j14-second`, `j28`, `recalcul-tiers`, `raw`, each with exit 0 and without any test launched with the variable (`tests_avec_variable` empty) (l.31-132). Reread by `oracle_record.py --verifier … --role rendu --commit 27b0e303…`: « conforme » [*conformant*] (JOURNAL l.314).

### 8.5 `s2-harness` suite

`Ran 398 tests in 62.358s` (SUITE l.621) and `OK (skipped=2)` (l.623). The two skipped tests are the count tests that would read a sealed copy through `SHOGEN_S2_CAMPAGNE_CONTROL` (SUITE l.207, l.209): the variable was not set (ENR l.8; annex D.4 a).

### 8.6 `recompute_*` oracle (run `recalcul-tiers`): what it establishes and what it does not establish

- **Object**: the JSON of the `recompute_*` entry points of the recomputation path (ADR-0028 D6 (i); third-party oracle of ADR-0003) for the main J14, the second J14, J28 and the included variant of J28 (RT l.3, l.5048, l.9462, l.13897), each with its label (RT l.23, l.5060, l.9489, l.13924); no warning from the reader (`"avertissements": []`, RT l.2).
- **What it establishes** [calc]: the 126 compared values (n, K, P̂_more, guard, z, γ̂₀, σ̂²_bloc, cv, FIV and its factors, z_bloc, runs, decomposition of K, state of flag 2 and « R1 discrimine », for J28, the main J14 and the second J14) are equal, string for string, to those of the renderings (`comparer_recalcul.py`, §8.9). In this execution, the recomputation path and the report path therefore return the same values from the journal alone.
- **What it does not establish**: an independent implementation. The two paths call the same frozen modules (`r1`, `lm`, `r2`, `records`), under the same Python, on the same host, in the same execution: it is a consistency check between two entry points, not a recomputation by third-party code. The independent oracle in exact arithmetic, written from the sealed text, was compared with `r1` on 585 synthetic journals before the seal, with 0 differences (annex B.43), and not on the real journals. Nor is it the composition test SHOGEN-S2-TUYAU-MONARK-1: “The `recompute_*` oracle, replayed in the single execution, is an internal check: it is not the composition test” (ADR §3). It says nothing about the fidelity of the journals to the sources (A(history-integrity), doc 08).

### 8.7 Verdict of the raw journal

RAW l.1, copied by extraction:

```text
verdict raw.jsonl (records.verifier_raw ; SHOGEN-RAW-FIN-1) : refus — lecture(s) de raw.jsonl absente(s) de journal.jsonl : [(1790275920, 'binance', Decimal('1790275970.0000675')), (1790277780, 'binance', Decimal('1790277830.0003345')), (1790283600, 'binance', Decimal('1790283650.0009525')), (1790283840, 'okx_ticker', Decimal('1790283890.0004282')), (1790285940, 'binance', Decimal('1790285990.0001917'))] — refus (SHOGEN-RAW-LECTEUR-1)
```

- The raw-journal verifier refuses (SHOGEN-RAW-LECTEUR-1): five readings of `raw.jsonl` are absent from `journal.jsonl`, four from binance and one from okx_ticker. [calc] Their `window_start` values are 2026-09-24T18:52Z, 19:23Z, 21:00Z, 21:04Z and 21:39Z: all within the D5 range `[1790273880 ; 1790435280]` (`controles_r1.py`), hence outside n, K and P̂_more of J28 (§2.4), and outside the two J14 segments, which end on 2026-09-09 and 2026-09-04.
- This verdict does not close the execution, by a construction written before the seal (package §12 pt 1, SHOGEN-RAW-FIN-1): “The single execution prints and records this verdict without the verdict closing it (named run that exits 0 whatever the verdict […]; the list of guards of D.4 b is closed)”. The `raw` run exited 0 (ENR l.126-127).

### 8.8 Duration

Production launched at 01:11:27 UTC, ended at 01:33:47 UTC, exit 0 (JOURNAL l.314), i.e. 22 min 20 s [calc]; the suite ran in 62.358 s (SUITE l.621). A single execution, no failed attempt (JOURNAL l.314).

### 8.9 Recounts by the drafter [calc]

Scripts of the drafter, Python standard library, filed in the project repository with this report. The first three were initially run under a mutation that must make them fail, then normally (G1 journal); `calc_divers.py` has no mutant mode: it performs elementary operations on copied values, cited line by line in its code.

| script | object | result | sha256 of the script; of the output |
|---|---|---|---|
| `controles_r1.py` | from the printed integers (anomalies per feed, n, K, s): exact P̂₀, P̂₁, P̂_more; z_s, γ̂₀, z_bloc (printed σ̂²), FIV and factors, cv, EMD_s, censoring bounds, z difference of the sensitivity, z_pool; rule value; integer identities; raw verdict against the D5 range | maximum relative difference from the printed values 4.21·10⁻⁵⁰ (last digit of precision 50); recounted rule value equal to the printed one in both strata | `11779f798b948b155462c7b66460009a0a2c991bb27653c2ad344c6c83744c4f`; `0469a499233d66cd64031c7cf21e82bf01615658e3f14cc25d8221afe5581e3e` |
| `comparer_recalcul.py` | JSON of the third-party recomputation against blocks 3 and 6 of the renderings | 126 values out of 126 equal as strings | `4e61cea803c902054e6fcbd2cc6a29f7c71ac1a2f8bfd824aefaa851ebef7585`; `8e6731f9f3c6f0a73ad2fb7938e66c215dafe1d0c13934f4d6f804d6dd57459e` |
| `d3_lift.py` | lift and φ identity of D3 (§6) | exact identity on 110 tables out of 110; difference from printed φ ≤ 2.38·10⁻⁵⁰ | `8f91474cdded5694e733334fadf225b110d3378ddb560f1bee4066eca80f9381`; `77ae69ec8666065d0e7ec3a13588f982d87de7bf1789ffe3f91813ea028dc73f` |
| `calc_divers.py` | roots, duration, sums, τ ratios, z_pool, guards of the J14 segments, sums of the anomalies per type | values cited [calc] in the text | `4d210cb65fb56fc5c0ef00ec31480bbe96426746191c5efa38a9e2def99a1c98`; `de7bd825bba4e71aeac9437dfafa26eb3101d00c3d1ea0b992b103c33f4c52af` |

σ̂²_bloc,s cannot be recomputed without the I_t series, hence without reading the journal: it is taken as printed, and the recount of z_bloc,s checks only the division by its root. The tables of this report were extracted from the renderings by scripts (`extraire_tables.py`, `extraire_d5.py`, `extraire_hd.py`, `table_lift.py`), without copying by hand.

## 9. Limitations

### 9.1 Limitations written with the rule (package §10.2, pts 2, 7 and 11)

1. Serial dependence of range ≥ ℓ not corrected: σ̂²_bloc,s is biased downward there (pt 11).
2. Even under a range < ℓ, bias of the triangular-weight estimator of the order of −ℓ⁻¹·Σ_k |k|·R(k): under positive autocorrelations, σ̂²_bloc,s underestimates and z_bloc,s overestimates (pt 11, SHOGEN-BARTLETT-BIAIS-1).
3. z_s and z_bloc,s are conservative through the plug-in of P̂_more; a non-rejection is thereby less probative (pt 11; SHOGEN-R1-PLUGIN-1).
4. Reduced, even negative, power against a common mode that affects all the sources, as soon as Σ_i (∂P_more/∂p_i)(1 − p_i) > 1 − P_more (pt 11; SHOGEN-R1-PLUGIN-1).
5. Normal approximation at the guard; near the guard, with iid windows, the level of z_s alone is measured above 0.01 on synthetic data, whereas the rule holds (pt 11, SHOGEN-GARDE-NIVEAU-ZSEUL-1; §3.4).
6. Asymptotic level, not demonstrated ≤ 0.01 in finite samples; the bound 0.02 holds under the joint null model (pt 7).
7. Under the §5.4 guard, declared departure from doc 10 §5.4: the stratum is not tested, its exact tail is hors décision (pt 2).
8. “No author of the rule has seen z, K, P̂_more or φ (annex D.3)” (pt 11), under the limitations of the D.1 inventory and of the measurements of annex B.37 (§10).

### 9.2 Limitations and procedures written in the package (§12, points 1 to 20)

1. SHOGEN-RAW-FIN-1: the raw-journal oracle remains strict; its verdict is printed without closing the execution (§8.7).
2. SHOGEN-ENREG-G1-1: the recorder extracts only a commit; a G1 record of uncommitted work cannot be produced.
3. SHOGEN-ENREG-DELAI-CHAMP-1: the timeout (3,600 s per command) is not a field of the record; it kills only the direct child.
4. SHOGEN-CENSURE-VIVANT-PORTEE-1: « harnais vivant » means the same start before and after the skipped window; a sleep during a start is counted « vivant » [*alive*].
5. SHOGEN-RENDU-TABLE-REELLE-1: the real output table never ran end to end on a fixture; the single execution is its first complete execution.
6. SHOGEN-RENDU-CLI-REPORT-1: `python -m shogen_s2.report` renders journals without a guard; procedure: no rendering of the sealed journals outside `rendu_unique.py`.
7. SHOGEN-RENDU-JETON-MAIN-1: the token `SHOGEN_RENDU_PRODUCTION` blocks the accidental call of `--produire`, not the deliberate call.
8. SHOGEN-RENDU-ORC-OCTETS-1: guard (4) hashes the files on disk, not the bytes loaded in memory.
9. SHOGEN-RENDU-RENAME-FENETRE-1: under POSIX, a window remains between the exclusive creation of the target and the renaming.
10. SHOGEN-GO-PICKAXE-FUSION-1: `git log -G` does not read merge commits; effect in refusal only.
11. SHOGEN-AXES-SIGMA-NUL-1: `axes_evaluables` marks « staleness » evaluable for a class σ of `None`; without effect in production.
12. SHOGEN-PAQUET-ERRATUM-FISHER-1: the « (Fisher) » of doc 10 designates the transformation z′ = artanh(r); the interval “≈ ±0.11” holds on the z′ scale; SE = 1/√(N−3) assumes independent pairs; N_min = 300 is a design choice.
13. SHOGEN-TAU-REDERIV-1: τ is not re-derived; the committed τ serves all the confirmatory tests (§5.1).
14. SHOGEN-CENSURE-INFO-1: informative censoring is not modelled; the verdict is not identified under arbitrary censoring of the skipped windows (§5.3).
15. SHOGEN-SEG-DEMARRAGE-1: a record belongs to the segment by its own timestamp; a segment without a retained `asn_attribution` makes k_eff not evaluable.
16. Private seal: with anchor (1), the token attests the existence of the bytes at the latest at genTime, nothing about earlier readings, under trust in FreeTSA; in the cloud session, the commits are signed by the key of the session and no offline bundle is made (§8.1).
17. Harness clock (T-17): the assignment of windows to strata and segments rests on the host's clock, A(harness-clock); the range of the median offsets of the clock check does not enter block 1 (§2.7).
18. SHOGEN-COLLECT-PREVWS-1: item not qualifiable in the cloud session, outside the rule; requalification after S2.
19. SHOGEN-ATTEST-ADVISOR-1: attestations of advisors missing; class R is excluded by the D.1 inventory, not by attestation.
20. Values of the machine block: the sha256 of the journals were only on the local workstation; the package validator accepted their text and format, not the values. At the execution, the downloaded journals are equal to them (§8.3).

### 9.3 Limitations observed from the execution

1. [report finding] The verdict is decided entirely on the standard-error floor: z_s ≈ 20.8 and ≈ 28.5, but FIV_s ≈ 115 and ≈ 266 bring z_bloc,s back below 2.33 (§3.1). The rule does not separate co-failure of the sources from serial dependence of the windows: this is the sealed statement of the discordance.
2. [report finding] The counted anomalies are almost all outages: in calm, 1,443 of the 1,451 anomalies (4 of staleness, 4 out-of-envelope); in stress, 691 of the 693 (2 of staleness, none out-of-envelope) [calc, sums of block 3, equal to Σ mⱼ of block 4]. K is formed, to within one window, of windows with at least two `panne_transport` readings (§5.2). These counts describe; they identify no cause.
3. [report finding] The censoring is large relative to n: 7,795 grid windows skipped outside the D5 range, of which 7,628 without a cause attributed by the journal, for 35,982 analysed windows, and 4,093 starts of the harness (§2.6); with σ̂_bloc,s, the non-outer bounds range from ≈ 1.82 to ≈ 93.9 in calm and from ≈ 1.70 to ≈ 33.1 in stress (§5.3). H_perte is an assumption, not tested.
4. [report finding] The R2 partition is a snapshot: one probe record per host, the last one, taken between 2026-09-28T01:17:55Z and 01:18:02Z (J28 l.435781). It does not describe the ASN axis over the 33 days. On the main J14, the ten probe records retained at the end of the segment failed and k_eff there is only an upper bound (§7.1).
5. [report finding] A single observer: one collection host (Windows traces in the renderings; the investor's workstation, JOURNAL l.324), one DNS resolver (Cloudflare DoH) per probe record; the multi-resolver and multi-vantage probe is « DUE » and residual 5 is « à son MAXIMUM, publié » [*at its MAXIMUM, published*] (J28 l.435772, l.435774). The anomalies of R1 and the ASN axis of R2 depend on the same observer.
6. [report finding] The staleness axis is not evaluable for binance, kraken and bitfinex, which carry no timestamp (J28 l.435464): it covers 8 of the 11 feeds of the pool.
7. [report finding] Uneven coverage of the stress stratum: the weekend of 2026-08-29 is covered over only 19 h of the 48 h, and that of 2026-09-26 over 32 h 51 min in the main variant, because of the D5 range (§2.5).
8. [report finding] No price data was received from Pyth over the whole campaign: access to the queried service was refused (HTTP 401) from the first day (ADR l.25), and nothing shows an outage of Pyth; the pool loses one of the two oracle-class feeds, and chainlink is observed only through a public RPC (§4.4).
9. [report finding] The label of block 5 (d) of J28, « aucun cluster à ≥ 2 flux (1) » [*no cluster with ≥ 2 feeds (1)*], reads poorly next to the partition of block 6; the main D3 estimator between clusters has no object on J28 (§4.2).
10. [report finding] The JSON of the third-party recomputation carries `"r1_discrimine": "VRAI"` for the « plage incluse » variant, labelled only at the entry level (§7.4); a reading of the line alone would isolate it from its label.
11. [report finding] Two hors décision outputs cross the threshold where J28 does not cross it: the main J14 REJETTE in calm (z_bloc ≈ 2.65) and the included variant gives z_bloc ≈ 2.51 in calm (§7.1, §7.4). Pt 9 excludes them from the decision; this report draws no reading from them.
12. [report finding] The third-party recomputation is not an independent implementation (§8.6); σ̂²_bloc,s is recounted by no distinct code on the real journals.
13. [report finding] The observed τ exceeds τ_classe at the maximum for two classes (§5.1): descriptive finding, without re-tune; the re-derivation is PX-Shogen-13 (§11).
14. [report finding] The byte-for-byte equality of a replay of the renderings on another host or another Python version is not measured (§12).

## 10. Declared deviations and exposures

### 10.1 Reading D.1 No. 16: exposure of the orchestrator of the cloud session

- **What is declared** (annex D, D.1 No. 16, addition dated 2026-10-02 17:5x UTC, declared deviation under D2 pt 8): while measuring the item MONARK-S2-M009A-EXPOSITION-1, the orchestrator of the cloud session displayed the subjects of the commits of a private repository of the MONARK project that touch documents forbidden to fresh drafters and validators (annex D); the subject of one of these commits carries a rate estimated on the S2 traces, whose value is copied nowhere; the content of the files was not downloaded (clone without blobs). Date: 2026-10-02 around 17:57Z; class R presumed (same measurement as reading No. 2, MONARK reimplementation of `r1.classify_ecart` on a snapshot of 18/09; exact nature of the rate not established without reading).
- **Position in the chronology**: after the first seal (genTime 2026-10-02T17:44:30Z) and before the second (2026-10-03T01:04:10Z). The revised package lists it: annex D “counts 16 readings in D.1 (No. 16, exposure of the orchestrator of the cloud session, is dated 2026-10-02, after the first seal and before this one)” (package l.8, (v)). The text of the rule (§10.2) was already sealed by the first package and it is identical byte for byte in the second (package l.8; JOURNAL l.304). The single execution was conducted by “the orchestrator of the cloud session” (JOURNAL l.310); it is the mechanical execution of a sealed script, under the guards of §8.
- The item SHOGEN-MONARK-SUJET-COMMIT-1, which measured the sessions that had displayed this commit subject, is closed (annex B.38).

### 10.2 Closure of MONARK-S2-M009A-EXPOSITION-1 (annex B.38)

Annex B.38 asks that this result be “taken up in the report of the execution”; it is taken up here, in substance. The item is closed after the sealing (trigger “before sealing” passed, departure recorded in package §8 and in the JOURNAL). The readers of the figure of reading D.1 No. 2 are the MONARK sessions of the M009 work packages, the orchestrator of the local workstation and its sub-agents, and a mapping sub-agent (commit subject only, not transmitted); no author of rule SHOGEN-CRITERE-R1-1 and no decision-maker, under the limitations of annex B.37 (search by exact tokens, window of 300 characters, text files); plus the cloud orchestrator after the first sealing (D.1 No. 16, §10.1). Attestation of the investor, decision-maker of the rule, to the question of whether the investor saw this figure: “no” (annex D.3 (i)). The revised package notes that this closure lifts the limitation written in its §8 (package l.8, (v)), whose text has remained unchanged.

### 10.3 Replacement of the first seal (A-8; CORR work package)

- First package: commit `ddf8c54`, sha256 `494d770d704dc7c342f0c6deec269e5642b3621bf451922f991e4ca1fb968097`, FreeTSA token of genTime 2026-10-02T17:44:30Z; replaced before any execution; it remains cited and no longer opens any execution (package l.8; §8.1).
- Reason: two class A findings of the catch-up G2 reviews, each capable of leaving the single execution without any output, without producing a false value (annex B.42, A-1: a `frozenset` of pairs of exact copies that the third-party recomputation did not serialize; annex B.43, A-1: a non-finite `ok` price that raised a `decimal` exception).
- Decision of the investor of 2026-10-02: “Correct and reseal”. CORR work package, commits `02f9c00`, `4002239`, `35cd2e2`, `4c831b8`, `e4bc2f1`, `a5a9de9`, `f35a70c`, suite 398 OK, rule and pins unchanged at each commit (annex A, CORR line; annex B.44).
- Effect on the sealed text: sections 1 to 12 unchanged, section 10.2 identical byte for byte; no value, no threshold, no inequality of the rule changes; new machine block (analysis commit `f35a70c`) (package l.8; JOURNAL l.304).
- In this execution, neither of the two corrected cases arose: the list of exact copies is empty in the four entries of the third-party recomputation (RT l.1520, l.6557, l.10991, l.15421), and no warning from the reader is printed (RT l.2), whereas clarification (i) of the package provides for one, counted per feed, for any non-finite price.

### 10.4 Precedence D-4 (SHOGEN-D4-PRECEDENCE-RAPPORT-1, annex B.45)

The D-4 precedence (FAUX case with k_eff not evaluable, returned NON ÉVALUABLE for flag 2) is not written in the package; it is ratified (annex B.18) and must be cited in the report if the case arises. **The case does not arise on J28**: « R1 discrimine » is FAUX and k_eff = 4 is evaluable (J28 l.435780); flag 2 is off by pt 10 itself (l.435795). Nor does it arise in the hors décision outputs: on the main J14, « R1 discrimine » is VRAI with a k_eff upper bound, hence a flag not evaluable by reading (a) of pt 10 (§7.1); on the second J14, « R1 discrimine » is NON ÉVALUABLE, hence a flag not evaluable by pt 10 (§7.2).

### 10.5 Other deviations

No other deviation is known to the orchestrator at the date of the brief of this report (2026-10-04). The JOURNAL records a single execution, with no failed attempt and no second execution (l.314). The refusal « run_params divergents » [*diverging run_params*] that item SHOGEN-R2-RUNPARAMS-CONCORDANCE-1 feared did not occur: the execution wrote its seven outputs (annex B.45; §8.4). The decisions of the investor recorded after the execution (JOURNAL l.322; §1) are those that D6 (vi) and D9 reserve to the investor after J28, plus an S2-bis work package; to the drafter's knowledge, none changes a decision prior to the seal (ADR §1 bis.8 would make it a declared deviation).

## 11. Analyses added after the pre-registration: not done at the date of the report

Each will carry the mandatory label « ajoutée après le pré-enregistrement, hors décision » [*added after the pre-registration, outside the decision*]; none is computed here, none enters the rule or can change the verdict (package §7, §11).

| item | what it will measure | source |
|---|---|---|
| SHOGEN-FLUX-QUASI-MORT-1 | the sealed rule recomputed per stratum after removal of the “quasi-dead” feeds, 2·ok(f, s) < n_s, threshold fixed in advance by an author without exposure to the presence rates; construction constraint SHOGEN-QUASI-MORT-PREDICAT-1: count « ok » by the predicate of `r1.analysis_pools` on the list of `r1.parse_journal` | `docs/adr-0028/AVIS-SEUIL-FLUX-QUASI-MORT.md` §1; annex B.39, B.44 |
| SHOGEN-HOST-DEGRADED-2 | the sensitivity “windows with a degraded-host diagnostic removed”, criterion defined on the diagnostic records of the harness alone (`asn_attribution.resolve_failed`, `clock_check`), never on a source status | annex B.6; annex D.5 |
| SHOGEN-CENSURE-INFO-2 | the outer bounds of z under arbitrary censoring of the skipped windows (arbitrary imputations, Manski-type bounds), with the reading “identified” or “not identified under arbitrary censoring” | annex B.6 (P-08); annex D.5 |
| SHOGEN-DEP-FENETRES-2 | the serial dependence of range ≥ ℓ (fixed-b asymptotics, linearized version of Künsch, event statistic), discharge of A(window-dependence); priority before G10 if the maximal run is ≥ ℓ, which is not the case on J28 (6 and 2, §5.4) | annex B.6 |
| SHOGEN-R1-PLUGIN-1 | the limitations of the transposed z: variance of the influence function (conservativeness of the plug-in), test of the complete distribution of m_t against its Poisson-binomial distribution (absorption of a broad common mode) | annex B.6 |
| SHOGEN-CONTENU-DEP-1 | the serial dependence on the content axis (effective N < N for N_min = 300 and the Fisher SE), by a block variance of ρ̂ | annex B.6; package §12 pt 12 |
| SHOGEN-POOLEE-BLOC-1 | a block standard-error floor for the pooled stratum and the level of z_pool under the null model, by simulation | annex B.13, B.18 |
| PX-Shogen-13 | the re-derivation of τ after the rendering, never applied to the confirmatory z; reservation: observed τ and calibration P99 do not bear on the same population | annex D.5; package §12 pt 13; annex B.45 |

### 11.1 Addition dated 2026-10-04: analyses done after the pre-registration (POST-PREREG work package), hors décision

Each output carries on its first line: « ajoutée après le pré-enregistrement, hors décision ; ne change pas le verdict de la règle scellée (« R1 discrimine » = FAUX, docs/11 §3) » [*added after the pre-registration, outside the decision; does not change the verdict of the sealed rule (“R1 discriminates” = false, docs/11 §3)*]. None enters the rule or replaces a value of a rendering; the verdict remains that of §3. Code: `scripts/post-s2/`, which reuses the readers of the harness without modifying `s2-harness`; outputs: `docs/adr-0028/execution/post-prereg-2026-10-04/` (abbreviated PP/ below; sha256 in `SHA256SUMS`); G1 journal of the worker (`docs/G1-lot-POST-PREREG.md`), where the parameters are written on 2026-10-04 at 04:18:36 UTC, before any execution on the journals. Exposure declared at the time of fixing them: block 3 of the J28 rendering and this report. The threshold of FLUX-QUASI-MORT-1 comes from the advice of an author without exposure (annex B.39); that of FLUX-DEVIANT-1 (p̂_f > 1/2) is the value of variant V2 of the same advice, applied by the worker. The constructions come from annex B, written before the execution, except the form of the criterion of HOST-DEGRADED-2 (ASN probe of the start, last marker, `clock_check` outside the criterion), a choice of the worker not written in the annex. These choices of the worker are fixed before the execution, after the exposure declared above, and named in the G1 journal. Consistency check: each output recounts n, K and P̂_more per stratum and finds them equal, string for string, to block 3 of J28 (PP/*.txt l.7-8). Roundings “≈” to 3 significant figures; complete values at the lines cited.

| item | what is computed | result | output |
|---|---|---|---|
| SHOGEN-FLUX-QUASI-MORT-1 (with QUASI-MORT-PREDICAT-1 and POOL-MIN-1) | sealed rule recomputed per stratum without the feeds with 2·ok(f, s) < n_s, ok counted by the predicate of `r1.analysis_pools` | no feed removed (minimum `ok` rate ≈ 0.981 in calm, bitstamp; ≈ 0.980 in stress, defillama [calc]); recomputed rule identical to the sealed rule; recomputed « R1 discrimine » = FAUX | PP/quasi-mort.txt l.10-16 |
| SHOGEN-FLUX-DEVIANT-1 (exploratory, conditioned on p̂_f) | same recomputation without the feeds with p̂_f > 1/2 | no feed removed (maximum p̂_f ≈ 0.0193 in calm, ≈ 0.0198 in stress [calc]); identical; FAUX | PP/deviant.txt l.10-16 |
| SHOGEN-POOLEE-BLOC-1 (a) | z_pool,bloc = Σ_s (K_s − n_s·P̂_more,s)/√(Σ_s σ̂²_bloc,s) | ≈ 2.60 (binomial z_pool ≈ 33.4); exploratory, outside the family; level not measured (POOLEE-BLOC-1 (b), DETTES-SIM work package) | PP/poolee-bloc.txt l.12-13 |
| SHOGEN-HOST-DEGRADED-2 | rule recomputed without the windows of the starts whose ASN probe carries a `resolve_failed` | 631 starts out of 4,172; windows removed 3,341 in calm and 720 in stress; K goes from 154 to 70 and from 133 to 59; calm: z_s ≈ 18.1, z_bloc ≈ 1.80, NE REJETTE PAS (discordance), EMD_s ≈ 104; stress: guard ≈ 6.03 < 10, NON ÉVALUABLE; FAUX | PP/hote-degrade.txt l.10-18 |
| SHOGEN-HORLOGE-ETENDUE-1 | median offset of the 3,610 retained `clock_check` | none non-evaluable; minimum ≈ −52.2 s, median ≈ 1.42 s, maximum ≈ 96.3 s, range ≈ 148 s | PP/horloge-etendue.txt l.10-11 |
| SHOGEN-CENSURE-INFO-2 | outer bounds of z_s under arbitrary censoring of the skipped windows; rule value under two witness imputations | calm: z_s ∈ [≈ −169; ≈ 121]; stress: [≈ −88.6; ≈ 81.5], bounds attained; all skipped windows clean: FAUX; 19 skipped windows in calm (42 in stress) imputed with two anomalies: REJETTE, hence « R1 discrimine » VRAI under this imputation; reading: **not identified under arbitrary censoring** | PP/censure.txt l.10-21 |
| SHOGEN-SIGMA-BLOC-INDEP-1 | classification, I_t series and σ̂²_bloc by a code independent of `r1` | 0 disagreements out of 270,435 cells in calm and 125,367 in stress; γ̂₀ and σ̂²_bloc equal, string for string, to block 3 | PP/sigma-indep.txt l.9-13 |
| SHOGEN-DEP-FENETRES-2 (b), which is SHOGEN-R1-PLUGIN-1 (a) | block variance of the influence function of K/n − P_more(p̂) (Künsch 1989, Ex. 2.2 and (2.14)) | σ̂²_IF,bloc ≈ 0.672·σ̂²_bloc in calm, ≈ 0.677 in stress; z_IF,bloc ≈ 2.37 in calm, ≈ 2.12 in stress; exploratory, level not measured | PP/influence.txt l.10-11 |
| SHOGEN-DEP-FENETRES-2 (c) | runs of I_t taken as units, iid null distribution at P̂_more | R = 119 against E[R] ≈ 33.5 in calm (z_R ≈ 14.8); 130 against ≈ 16.7 in stress (z_R ≈ 27.8) | PP/influence.txt l.13-14 |
| SHOGEN-R1-PLUGIN-1 (b), descriptive | counts of m_t against the Poisson-binomial distribution of p̂ | calm: m = 1 observed 1,001 against ≈ 1,380 expected, m ≥ 3 observed 49 against ≈ 0.424 [calc]; stress: m = 1, 214 against ≈ 659, m ≥ 3, 118 against ≈ 0.224 [calc]; no test | PP/influence.txt l.17-40 |
| SHOGEN-CONTENU-DEP-1 | effective size N_eff of ρ̂ (block variance of its influence function) against the Fisher SE | ρ̂ equal to block 5 for the 55 pairs; median N_eff/N ≈ 0.0535 (ρ_raw) and ≈ 0.0556 (ρ_resid); N_eff < N_min = 300 for 3 pairs (ρ_raw) and 2 (ρ_resid) | PP/contenu.txt l.10-66 |

**What these analyses allow one to say.** The verdict of §3 depends on no almost-dead feed and on no feed with an anomaly rate above 1/2: there are none on J28. σ̂²_bloc,s, on which the discordance depends, is reproduced by a code distinct from `r1` on the real journals, common readers aside (second half of limitation 12 of §9.3). The windows of K are concentrated in the starts whose ASN probe of the harness carries a `resolve_failed`: 84 of the 154 windows of K in calm and 74 of the 133 in stress fall there, for 13.6% and 6.3% of the windows [calc]. The FAUX verdict is not identified under arbitrary censoring of the skipped windows: it rests on the assumption H_perte (doc 08, A(loss-non-informative)); an imputation of 19 skipped windows in calm, or of 42 in stress, gives « R1 discrimine » VRAI. The estimated effective size of the content series is of the order of 5% of N at the median and remains below N for the 55 pairs, on ρ_raw as on ρ_resid: for each, the Fisher SE (package §12 pt 12), which assumes independent pairs, is smaller than the block SE (ratio from 1.50 to 15.0 [calc]).

**What they do not allow one to say.** None identifies a cause: the concentration of K in the degraded starts is compatible with a common mode of the observer, without establishing it. Two exploratory statistics with a block standard error cross 2.33 where z_bloc,s does not: z_pool,bloc ≈ 2.60 and z_IF,bloc ≈ 2.37 in calm; none is in the rule or in the family, their level in finite samples is not measured, and they do not change the verdict (same status as the hors décision outputs of §9.3 pt 11). The runs taken as units keep an excess under an iid null distribution that ignores the persistence specific to each source; this is not a test of the dependence of range ≥ ℓ. The distribution of m_t is described, not tested. Nothing is said about the independence of the sources (doc 09).

**Remaining.** Not done, with their reason: the fixed-b form of DEP-FENETRES-2 (a) (Kiefer-Vogelsang, P-05, not filed); a tolerance and a null distribution of the event statistic (c); the test of the distribution of m_t of R1-PLUGIN-1 (b) (statistic and level to be sourced); an outer bound of z_bloc under arbitrary censoring (CENSURE-INFO-2; “Manski-type” attribution [inferred: P-08 not filed]); the level of z_IF,bloc and of z_pool,bloc (synthetic simulation). The `clock_check` does not enter the criterion of HOST-DEGRADED-2: its degradation signals depend on the sources that answer the probe; departure from the wording of the item, declared in the G1 journal.

## 12. Reproduce

- **Inputs**: the three sealed journals, designated by their sha256 (machine block, package l.217-219; §8.3), and the closing sums file (package l.220). Their format is specified by reference (package §1: `records.py` and `journal.py` at the collection commit `ed479c5`, doc 10 §6).
- **Code**: analysis commit `f35a70c19ba8269f1f7e2bcd31775e4fc513da20` (`s2-harness/shogen_s2`, `s2-harness/tools`); single-execution script `s2-harness/tools/rendu_unique.py`, sha256 `06d189cf84e7dca97bdfc0e1b695fc827a09473779505c7a8f1af1e7c26e9050` (package l.215-216); Python 3.11.15 at the time of the execution (ENR l.14).
- **Seal**: `docs/adr-0028/sceau/` (manifest, request, token, FreeTSA chain); offline check by `bash scripts/sceau/verify.sh` (§8.1).
- **Replay**: with the journals and the commit, the `recompute_*` entry points recompute the blocks from the journal alone (doc 10 §6; ADR-0003); their values are compared, string for string, with those of the filed renderings (§8.6, §8.9). A new production by `rendu_unique.py` would be a second execution, a declared deviation (annex D.4 b).
- **This report**: each value in it is cited by file and line; the scripts of the drafter and their outputs (§8.9) replay its computations from the renderings alone, without the journals.
- **What is not public**: the project repository is private (package §12 pt 16); the sealed journals are not published, and their publication is a precondition for the composition test SHOGEN-S2-TUYAU-MONARK-1 on the MONARK side (ADR §3; §4 pt 4). The sealed package, the seal, the renderings, the records and the scripts are in the same private repository and are not published: documents provided on request, under agreement. Checking the seal requires the sealed package, which is provided together with the seal on request: a third party who is given the sealed package, the seal and the renderings without the journals can check the seal and the arithmetic of the renderings, not recompute the renderings.

> *Addition dated 2026-10-04 06:52:35 UTC (G2 review of the DETTES-B1 work package, C-3; points “Code” and “Replay” above)*: from commit `0221a74` (DETTES-B1 work package, B1-1; `rendu_unique.py` from `0789d96`, B1-4), `s2-harness/shogen_s2` and `s2-harness/tools` differ from the analysis commit `f35a70c` (sha256 of `rendu_unique.py` at the head `5ee95dbf…` ≠ `sha256_script` `06d189cf…`): guards (2) and (4) refuse at the head; any replay (`recompute_*`) or re-execution of the S2 rendering is done on an extraction of `f35a70c`; at the head, the outputs differ by construction (block 5 (d), k_eff note, key `etiquette` of flag 2 of `j28-incluse`, ASN divergences of partial probe records).

> *Addition dated 2026-10-04 09:36:41 UTC (closing cp-2, C-7; limitation to be read with §9.3)*: an ASN change visible on a single base of a partial probe record is not searched for by the S2 renderings (semantics of the CORR work package: complete probe records only); the effect of the later fix SHOGEN-ASN-DIVERGENCE-PARTIELLE-1 on the sealed journals is not measured (SHOGEN-ASN-PARTIELLE-S2-1, annex B.49).

## Glossary (French → English)

### A. Passages kept in French (printed outputs, verdicts and sealed labels)

| French, as printed | English gloss |
|---|---|
| NE REJETTE PAS | does not reject |
| « R1 discrimine » = FAUX | “R1 discriminates” = false |
| « le modèle binomial de doc 10 §5.1, à fenêtres indépendantes, est rejeté ; la cause n'est pas identifiée entre co-défaillance des sources et dépendance sérielle des fenêtres » | the binomial model of doc 10 §5.1, with independent windows, is rejected; the cause is not identified between co-failure of the sources and serial dependence of the windows |
| « R1 rejette (s) » | R1 rejects (s) |
| hors décision | outside the decision |
| VRAI | true |
| « plage incluse » | range included |
| [SENSIBILITÉ] | SENSITIVITY |
| « rendu » | rendering |
| REJETTE | rejects |
| « BTC/USD-stable, devise marquée par flux » | BTC/USD-stable, currency marked per feed |
| « pool configuré = 12 flux » | configured pool = 12 feeds |
| « k nominal = 10 (hôtes distincts du pool) » | nominal k = 10 (distinct hosts of the pool) |
| « ok = 0 / 24585 lectures, n = 24585 » | ok = 0 / 24585 readings, n = 24585 |
| « 10 sources / 11 flux » | 10 sources / 11 feeds |
| « ok = 0 / 11397 lectures, n = 11397 » | ok = 0 / 11397 readings, n = 11397 |
| « fenêtres distinctes (window_close) calme 0, stress 0 ; asn_attribution 0 ; clock_check 0 » | distinct windows (window_close) calm 0, stress 0; asn_attribution 0; clock_check 0 |
| « causalité non établie » | causality not established |
| « kind=weekend_utc stress = samedi+dimanche UTC » | kind=weekend_utc stress = Saturday+Sunday UTC |
| « harnais vivant » | harness alive |
| « le résidu est à son MAXIMUM, publié » | the residual is at its MAXIMUM, published |
| « le z confirmatoire inclut les modes communs de l'observateur (hôte, DNS, réseau) » | the confirmatory z includes the common modes of the observer (host, DNS, network) |
| « n'est pas rejeté » | is not rejected |
| « aucune strate ne rejette ; strate(s) testée(s) : calme, stress » | no stratum rejects; stratum(s) tested: calm, stress |
| « nonÉv » | not evaluable |
| (panne / stale / horsE / nonÉv) | outage / stale / out-of-envelope / not evaluable |
| « côté livraison » | delivery side |
| « comparaison hétérogène déclarée » | heterogeneous comparison declared |
| « historique insuffisant » | insufficient history |
| « co-défaillance observée non expliquée par les axes R2 » | co-failure observed, not explained by the R2 axes |
| ÉTEINT | off |
| « aucun cluster à ≥ 2 flux (1) → tout reste au φ par paire de flux (bloc 4) » | no cluster with ≥ 2 feeds (1) → everything stays at the φ per pair of feeds (block 4) |
| « chemin de LECTURE ≠ amont (§3.2) : l'ASN mesuré est celui du fournisseur RPC (ethereum-rpc.publicnode.com), une infrastructure de lecture, pas l'amont du feed » | READING path ≠ upstream (§3.2): the measured ASN is that of the RPC provider (ethereum-rpc.publicnode.com), a reading infrastructure, not the upstream of the feed |
| « bornes à P̂_more fixé, non extérieures ; verdict non identifié sous censure arbitraire des fenêtres sautées » | bounds at fixed P̂_more, non-outer; verdict not identified under arbitrary censoring of the skipped windows |
| « non extérieures » | non-outer |
| « run maximal ≥ ℓ : σ̂²_bloc,s biaisé vers le bas ; SHOGEN-DEP-FENETRES-2 prioritaire avant G10 » | maximal run ≥ ℓ: σ̂²_bloc,s biased downward; SHOGEN-DEP-FENETRES-2 a priority before G10 |
| « [inféré : dérivation de l'AVIS-advisor-defi Q1 (iv)] » | [inferred: derivation from the AVIS-advisor-defi Q1 (iv)] |
| « seconde coupe » | second cut |
| NON ÉVALUABLE : strate non testée, hors décision (§1 bis.1 pt 2) | not evaluable: stratum not tested, outside the decision (§1 bis.1 pt 2) |
| « k_eff ≤ 10 (BORNE SUPÉRIEURE) » | k_eff ≤ 10 (UPPER BOUND) |
| « ni levé ni éteint » | neither raised nor off |
| « aucune strate testée » | no stratum tested |
| « strate poolée hors des entrées » | pooled stratum outside the inputs |
| « variante “exclue” = principale (blocs 1-6) ; variante “incluse” = sensibilité — biaisée vers le haut par construction ; documente l'exclusion D5 ; pas un estimateur alternatif » | variant ‘excluded’ = main (blocks 1-6); variant ‘included’ = sensitivity — biased upward by construction; documents the D5 exclusion; not an alternative estimator |
| « motif de l'exclusion (harnais dégradé, […]) : causalité non établie » | reason for the exclusion (degraded harness, […]): causality not established |
| `sensibilité « plage incluse » de la liste fermée (D2 pt 7), hors décision, biaisée vers le haut par construction` | “range included” sensitivity of the closed list (D2 pt 7), outside the decision, biased upward by construction |
| « gardes levées » | guards cleared |
| « conforme » | conformant |
| « vivant » | alive |
| « à son MAXIMUM, publié » | at its MAXIMUM, published |
| « aucun cluster à ≥ 2 flux (1) » | no cluster with ≥ 2 feeds (1) |
| « run_params divergents » | diverging run_params |
| « ajoutée après le pré-enregistrement, hors décision » | added after the pre-registration, outside the decision |
| « ajoutée après le pré-enregistrement, hors décision ; ne change pas le verdict de la règle scellée (« R1 discrimine » = FAUX, docs/11 §3) » | added after the pre-registration, outside the decision; does not change the verdict of the sealed rule (“R1 discriminates” = false, docs/11 §3) |
| « go exécution » | go execution |

### B. Terms

| French | English | Note |
|---|---|---|
| k_eff ; k nominal ; k nominal_s | k_eff ; nominal k ; nominal k_s | k_eff: number of classes of the measured R2 partition; never an independence count |
| enveloppe ; hors-enveloppe | envelope ; out-of-envelope |  |
| fenêtre ; fenêtres sautées | window ; skipped windows | one minute of the UTC grid |
| strate ; strate calme ; strate de stress ; strate poolée | stratum (pl. strata) ; calm stratum ; stress stratum ; pooled stratum | printed stratum names: calme, stress |
| flux | feed | a reading of the BTC/USD (or BTC/USDT) price served by a source |
| source ; place (d'échange) ; agrégateur ; oracle | source ; exchange ; aggregator ; oracle |  |
| hôte ; hôte de collecte | host ; collection host |  |
| panne | outage | status panne_transport kept as printed |
| écart (doc 10 §5.2) ; en écart ; co-écart ; taux d'écart | anomaly ; anomalous ; co-anomaly ; anomaly rate | a feed is anomalous in a window if in outage, stale or out of envelope |
| écart (sens courant) ; écart déclaré (à un texte) ; écart (contrôle d'horloge) | difference, gap ; declared departure ; offset | offset: clock-check sense (§9.2 pt 17), as in the median offset of §11.1 |
| déviation (déclarée) | (declared) deviation | departure from the pre-registered plan |
| co-défaillance | co-failure |  |
| discordance | discordance | rule case: z_s ≥ 2.33 and published z_bloc,s < 2.33 |
| sceau ; sceller ; scellé ; scellement | seal ; to seal ; sealed ; sealing |  |
| paquet (de pré-enregistrement) ; paquet scellé | (pre-registration) package ; sealed package |  |
| rendu (nom) | rendering | an output file of the single execution (SUITE, J14p, J14s, J28, RT, RAW) |
| exécution unique | single execution |  |
| sortie ; sortir 0 | output ; exit 0 |  |
| journal ; journaux scellés ; journal brut | journal ; sealed journals ; raw journal | JOURNAL: the project journal |
| relevé | probe record | diagnostic record of the harness (asn_attribution, clock_check) |
| enregistrement (d'oracle) | (oracle) record |  |
| lecture | reading | a data reading; also an interpretation; also an access listed in annex D.1 |
| rédacteur (frais) ; auteur ; validateur ; relecture | (fresh) drafter ; author ; validator ; review |  |
| valider | accept (at review) | the assurance qualifier listed in doc 09 is not used (gate S-G4) |
| orchestrateur ; investisseur ; sous-agent | orchestrator ; investor ; sub-agent |  |
| feu vert ; brouillon | go-ahead ; draft |  |
| dépôt (privé) ; versé | (private) repository ; filed |  |
| harnais ; démarrage | harness ; start |  |
| garde ; déclencheur | guard ; trigger |  |
| drapeau ; levé ; éteint | flag ; raised ; off | printed state kept: ÉTEINT, ETEINT |
| seuil ; puissance | threshold ; power |  |
| erreur-type ; erreur-type par blocs ; plancher d'erreur-type par blocs | standard error ; block standard error ; block standard-error floor |  |
| excès minimal détectable | minimum detectable excess | EMD_s |
| statistique confirmatoire | confirmatory statistic |  |
| censure ; bornes (non) extérieures | censoring ; (non-)outer bounds |  |
| plage (D5) ; segment ; coupe | (D5) range ; segment ; cut |  |
| variante exclue ; variante incluse | excluded variant ; included variant |  |
| sensibilité ; descriptif | sensitivity ; descriptive |  |
| bloc ; bloc machine | block ; machine block |  |
| jeton ; manifeste ; horodatage ; autorité d'horodatage | token ; manifest ; timestamp ; timestamping authority |  |
| délai de rétractation ; tête gardée ; voie (a) | withdrawal period ; guarded head ; route (a) |  |
| recalcul tiers ; chemin de recalcul ; rejeu | third-party recomputation ; recomputation path ; replay |  |
| commit d'analyse ; commit de collecte | analysis commit ; collection commit |  |
| amont ; amont déclaré | upstream ; declared upstream |  |
| résidu ; chemin de lecture ; chemin de mesure | residual ; reading path ; measurement path |  |
| mono-vantage ; sonde multi-résolveurs | single-vantage ; multi-resolver probe |  |
| constat ; [constat du rapport] ; inféré | finding ; [report finding] ; inferred | [calc]: drafter's computation |
| recopié ; imprimé ; étiquette | copied (verbatim outputs) or quoted (translated quotations) ; printed ; label | a translated quotation is not a verbatim copy; the original prevails |
| limite ; lot ; annexe | limitation ; work package ; annex |  |
| pt, pts ; n° ; l. | pt, pts ; No. ; l. | point(s) ; number ; line |
| exposition ; poste local ; session cloud | exposure ; local workstation ; cloud session |  |
| fonction de difficulté | difficulty function | Littlewood and Miller (L&M) |
| témoignage attesté | attested statement | doc 09 |
| J14 principal ; J14 second | main J14 ; second J14 | run names kept: j14-principal, j14-second |
