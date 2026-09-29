# Proof-integrity and proof-sampling weaknesses in poktroll (Pocket Network, Shannon) at v0.1.35

**A private, good-faith security disclosure to the Pocket Network maintainers.**

Prepared by the MONARK team (Shōgen analysis component). Independent security research.
Analyzed commit: `poktroll @ a109dd0bae65c1d96b010d65f4cdc5bc77a50fc2` (release **v0.1.35**).
Report date: 2026-09-29. Channel: GitHub private security advisory.

---

## Abstract

We report a cluster of proof-integrity weaknesses and one proof-sampling weakness in the
Shannon protocol implementation (`github.com/pokt-network/poktroll`) as read at the deployed
commit `a109dd0` (v0.1.35), together with its pinned dependencies `smt@v0.14.1` and
`shannon-sdk`. All findings rest on reading the **public, open-source code** at a pinned commit;
every mechanism was exercised in **local, offline keeper and library tests** at that commit, with
no network access, no POKT, no account, and nothing written to any live network.

Four items are reported, at deliberately different confidence levels:

- **F1 — Proof-sampler entropy collapse (MECHANISM ESTABLISHED at code + PREDICTION).**
  The seed passed to the probabilistic proof sampler is truncated by `binary.Varint`, folding
  roughly half of all seeds into a 128-value range (~7 bits). A local 128-seed enumeration
  predicts an **effective probabilistic-proof rate below the intended parameter — ≈ half in the
  sub-percent regime** (the deficit shrinks as the intended probability grows; see §5). This is a
  code mechanism and a prediction the maintainers can verify against their own configured parameter
  and settlement data.

- **F2 — Claim-inflation cluster (CONFIRMED).** A claim's relay `Count` and compute-unit `Sum`
  are read directly from the committed Merkle-sum-tree root and are **not bound to distinct
  served work**; the mandatory-proof "spot check" is bypassable because the proven leaf's
  *position* is not bound to the relation hash. Reproduced end-to-end at the settlement path.
  Economic impact is **bounded by the application budget floor** — this is not unlimited theft.

- **F3 — Response-integrity check absent (MECHANISM ESTABLISHED, CONDITIONAL EXPLOITABILITY).**
  `ValidateRelayResponse` in `shannon-sdk` does not compare `SHA256(payload)` against the signed
  `payload_hash`. Exploitability is conditional on a threat model (a malicious supplier, or an
  intermediary on the RelayMiner→gateway path); it is the weakest of the four.

- **F4 — Settlement re-draw of an invalid proof (LEAD, UNTESTED).** The settlement code appears
  to re-derive the proof requirement from a claim hash that changes once `ProofValidationStatus`
  is written, which *plausibly* re-draws the requirement for a well-formed-but-invalid proof.
  This is an untested hypothesis at code level, offered as future work, **not a finding**.

We propose concrete remediations for each and a reproduction package by reference (tree sha, test
names, deterministic environment). A severable cover letter (separate file) proposes a possible
collaboration; it is deliberately kept out of this disclosure.

---

## 0. Good-faith research and responsible-disclosure statement

This is **independent, good-faith security research by the MONARK team**, long-time members of the
Pocket community, who set out to study poktroll in depth. **We are not acting under any contract,
commission, permission, or reward arrangement with the Pocket Network Foundation or any related
party, and we claim none.** Our sole purpose is to help the maintainers strengthen the protocol.

The findings rest on reading the **public open-source code** at a pinned commit (`a109dd0`); no
permission is needed or claimed to read published source. All mechanism testing was **local**:
an isolated sandbox, source obtained from a pinned release tarball, no live network, no POKT, no
account, no submission, nothing written on any mainnet or testnet, and nothing made public.

We are disclosing **privately**, via a **GitHub private security advisory**, so that the maintainers
can remediate before any public discussion. **We publish no on-chain aggregates about network
participants** in this report. Where a real-world rate is discussed (F1), it is presented as a
code-level mechanism and a prediction that the maintainers can verify against their own data — not
as a datum we mined. We hold nothing back on remediation and we make no public statement, even
anonymized, ahead of coordinated disclosure.

We note in the interest of full transparency (see §4) that the analysis was carried out by LLM
agents operating under a strict verification discipline. We do not ask the reader to trust that;
the reproduction package (§8) and the sealed local tests are what answer the natural distrust —
every mechanism can be re-run by the maintainers, deterministically, from the public code.

---

## 1. Motivation

The MONARK team has followed Pocket for years, as members of its community. Our own system
(**Shōgen**) is a measurement layer whose central concern is **source co-failure** — the question
of when nominally independent data sources actually fail together. That interest led us to study
Pocket Network (Shannon) as a decentralized data-supply substrate: what, precisely, does its proof
machinery *prove*, and what does it leave unproven? We read the protocol as deployed, at code, to
answer that for ourselves.

The reading surfaced a set of gaps between what the proof system appears to guarantee and what the
code actually enforces. Because those gaps bear on the integrity of settlement, we chose to write
them up carefully, test the mechanisms locally, and disclose them privately to the maintainers.
This report is the technical result; a separate, severable cover letter records a possible
collaboration and is kept entirely out of this disclosure.

---

## 2. Scope and versions

All references are to public source at pinned revisions. Line numbers below were re-checked
against the pinned files (their sha256 are listed in Appendix B).

- Repository: `github.com/pokt-network/poktroll`, release **v0.1.35** =
  commit `a109dd0bae65c1d96b010d65f4cdc5bc77a50fc2` (GitHub release page, 2026-08-12; checked
  2026-09-29).
- `smt` library pinned at **v0.14.1** by `go.mod`; `shannon-sdk` at its pinned revision
  (`v0.0.0-20260812141256-a508808fbbe0`, commit `a508808fbbe0`); Go toolchain **1.26.5** (read
  from `go.mod`).
- The v0.1.35 line is the deployed, consensus-breaking mainnet release from height **883667**
  (2026-08-18) onward. We state this as a fact **the maintainers can confirm against their own
  chain/upgrade history**; it is not presented as a datum we mined.

### 2.1 Patch status (first-hand, GitHub, 2026-09-29) — `[mesure]`

Checked directly on GitHub on 2026-09-29:

- No release newer than v0.1.35 on the releases page.
- No published security advisory (`/security/advisories` empty).
- `x/proof/keeper/proof_validation.go` (poktroll `main`): last change **2026-01-27**, before
  v0.1.35 → **unchanged** since the analyzed commit.
- `proofs.go` / `VerifyClosestProof` (`smt` `main`): last change **2025-07-15** → **unchanged**.
- `relay.go` (`shannon-sdk` `main`): the only post-window change is commit `9bf0b02`
  (2026-08-27), a **build/import optimization** (it replaces the `poktroll/app` import with a local
  `const accountAddressPrefix = "pokt"`, bumps Go, and pins poktroll v0.1.35); the
  **response-validation logic is unchanged** (patch read in full, 2026-09-29).
- Reserve: histories were read on GitHub; any embargoed/private fix is not visible to us. A
  byte-diff `a109dd0..main` of the three files would let this "unchanged" claim rest on a full
  `[mesure]` rather than on file history; it is a nice-to-have, not a blocker.

To the best of our first-hand knowledge on 2026-09-29, the mechanisms below are **unpatched** in
the public tree.

---

## 3. Threat model

We consider three actors, none of which requires privileged access to the chain:

1. **A malicious or opportunistic supplier.** Any party can stake as a supplier (permissionless).
   A supplier constructs its own claim (the Merkle-sum-tree root it commits) and, when a proof is
   required, the proof it submits. F1, F2, and F4 concern what such a supplier can commit and get
   settled.
2. **An intermediary on the RelayMiner→gateway path** (F3). A party positioned between the
   RelayMiner that signs a response and the gateway/consumer that reads it. This is the actor whose
   *existence in a served deployment* we could not establish from code (see F3's bound).
3. **The victim of F2 is the application's staked (burned) budget**, not "the network at large":
   over-claiming is drawn from the application's committed stake, and is bounded by the
   per-supplier settlement floor (§5.F2, §6).

We do **not** model, and make no claim about, consensus-level attacks, key compromise, or
availability. This report is about the *integrity of what proofs assert at settlement*.

---

## 4. Methodology

Our method is deliberately code-first and reproducible, because the analysis was performed by LLM
agents and the honest answer to "why should we believe this?" is "re-run it".

- **Code-first reading at a pinned sha.** Every mechanism is grounded in specific lines of the
  public source at `a109dd0` (and the pinned `smt`/`shannon-sdk`), re-checked by sha (Appendix B).
  We do not rely on a running mainnet to establish any mechanism.
- **Local keeper and library tests at `a109dd0`.** Tests were written against the real code in an
  isolated sandbox: no network during testing (modules fetched once, then `GOPROXY=off`), no POKT,
  no account, nothing on any live network. Where the keeper package required generated mocks
  (git-ignored), they were regenerated from the repository's own `//go:generate` directives; no
  production code was modified.
- **Anti-false-positive controls.** Each confirmed mechanism carries a positive control (the honest
  case passes in the *same* harness), a negative control (a bad signature is rejected), and a
  specificity control (a valid value at a non-canonical position **with a bad signature** is
  rejected — proving the value is still checked). Three assertions are printed in each T-A run
  (inserted key ≠ relation hash; proven-leaf path ≠ `ph.Path(H(relation))`; the proven leaf is the
  closest), separating the "position" weakness (T-A) from a mere "proximity" artifact (T-A′).
- **Adversarial verification before consuming any finding.** Each confirmed mechanism was put to an
  independent panel that tried to refute it and to rule out harness artifacts (run
  `wf_759534a9-512`: 11 verifiers + 1 advisor lens), followed by an independent full replay in a
  fresh context (7/7 file-sha match on the base; the four tests and the oracle reproduced with
  `-count=1`). F1's mechanism was additionally checked by a first-hand 128-seed enumeration by the
  orchestrator.
- **An honest episode, told plainly.** For the grouped-leaf sub-result (P-09 within F2), a first
  agent's "correction" — that the survival rate was governed only by the number of *real* leaves,
  not by grouping — was itself **refuted by the panel**: at an identical committed sum, the grouped
  arrangement survives the spot check ≈ 0.984 of the time versus ≈ 0.0165 ungrouped (a ≈ 59× gain
  from grouping alone). We report this because it is exactly the kind of self-check the reader is
  entitled to see.
- **Provenance and human acceptance.** Every artifact is sha-pinned and carries its resolved model
  and date; `error_origin` is tracked; closure is gated by human acceptance, never self-declared by
  a generator.

We state plainly: **LLM agents did the analysis under this discipline.** The reproduction evidence
(§8, Appendix B) is what should answer any distrust — not our assertion.

---

## 5. Findings

Verdict levels used below: **CONFIRMED** (code + reproduced); **MECHANISM ESTABLISHED /
CONDITIONAL EXPLOITABILITY**; **LEAD (UNTESTED)**. Panel votes are preserved verbatim.

### F1 — Proof-sampler entropy collapse in `SeededFloat64`
**Level: MECHANISM ESTABLISHED (code) + PREDICTION (maintainer-verifiable). Independently
reproduced across three lenses; advisor-adjudicated.**

**Mechanism (code, `pkg/crypto/rand/float.go` L16–25).** The sampler computes
`seedHash = crypto.Sha256(join(seedParts))`, then `seed, _ := binary.Varint(seedHash)`, then
`rand.New(rand.NewSource(seed)).Float64()`. Two properties collapse the entropy:

1. `binary.Varint` reads a *single* varint from the hash and **discards the number of bytes
   consumed**. When the first byte of the hash is `< 0x80` (about half of all inputs), `binary.Varint`
   returns a value folded into the range **[-64, 63]** — only **128 distinct seeds** (~7 bits) for
   that entire half of the input space.
2. Because `math/rand` is seeded deterministically, those 128 seeds map to 128 fixed first
   `Float64()` values.

**Consequence.** A local enumeration of all 128 folded seeds shows that, **for a sub-percent draw
threshold, none of them** produces a `Float64()` below it. In that regime the folded half is
structurally absent from the low tail that triggers a probabilistic proof, the other half behaves
≈ uniformly, and the net effect is an **effective draw probability ≈ one half of the intended
parameter**. The deficit is **parameter-dependent**: it is largest when the intended probability is
small and shrinks as it grows (at a draw probability of 0.25 the folded half already covers part of
the low tail, so the deficit falls to roughly a quarter rather than a half). The exact factor for
any configured `proof_request_probability` is maintainer-computable from the mechanism below.

**First-hand oracle (orchestrator, `g7check/main.go`: 128-seed enumeration of the folded half plus a
large-seed Monte Carlo, 5,000,000 samples).** Verbatim output:

```
p=0.0010
k(<p) over 128 folded seeds  = 0
k(<=p) over 128 folded seeds = 0
P_large(<p) over 5000000 samples  = 0.001002
predicted P(<p) = 0.5*P_large + 0.5*(k/128) = 0.000501
ratio predicted/uniform = 0.5010
```

Read as a **prediction**: for a sub-percent intended draw probability (the governance parameter
`proof_request_probability`, e.g. on the order of 1‰), the mechanism predicts an **effective
probabilistic-selection rate ≈ 0.5‰**, i.e. **≈ half** — the illustrative operating point. The
maintainers supply their own configured parameter; the factor is exact for small probabilities and
smaller for larger ones (see the parameter-dependence note above). An independent replay on a
distinct RNG stream reproduced the same behavior (folded half never below the threshold; large half
≈ uniform; ratio ≈ 0.50).

**How to verify (maintainer-side).** This prediction is checkable **by the maintainers against their
own settlement data**: for any settlement window, compare the count of probabilistic-proof
selections against the count expected at the configured `proof_request_probability`. Our claim is
only that the **code mechanism predicts a factor of ≈ 1/2**, and that the enumeration above is
deterministic and re-runnable. **We do not present ourselves as having mined the on-chain rate; any
empirical consistency is an observation the maintainers can reproduce.**

**Honest bound (verbatim).** "Present as CODE MECHANISM + PREDICTION. Do NOT present ourselves as
having mined the on-chain figure; frame empirical consistency as maintainer-reproducible."

### F2 — Claim-inflation cluster: count/sum not bound to distinct served work; mandatory-proof guard bypassable
**Level: CONFIRMED. Panel vote: 3/0 (T-A); the grouped-leaf sub-result (P-09) 1/1 with an
orchestrator tie-break, then reproduced independently.**

This finding is a cluster of three composable mechanisms, all confirmed at the settlement path.

**(T-A) The proven leaf's position is not bound to the relation hash.**
`validateClosestPath` (`x/proof/keeper/proof_validation.go` L298–341) compares the *target* path
`proof.Path` to `expectedProofPath = protocol.GetPathForProof(blockHash, sessionId)` (L331–332). It
**never** compares the *position of the proven leaf* (`proof.ClosestPath`) to the hash of the
relation it carries. `verifyClosestProof` (L457–471) delegates to `smt.VerifyClosestProof`
(`smt/proofs.go` L357–391), which builds a nil path hasher (L366) and calls `VerifySumProof(...,
proof.ClosestPath, valueHash, sum, count, nilSpec)` (L391): it **trusts `proof.ClosestPath` as
given** and never re-derives the position from `H(value)`. A leaf may therefore sit at an
attacker-chosen position unrelated to its content and still verify.

*Reproduced.* At the settlement path (`EnsureValidProofSignaturesAndClosestPath`, i.e. the guarded
path — never `EnsureWellFormedProof` alone), a single valid relay inserted at a non-canonical key
settles with no error; the positive control (canonical key) passes; the negative and specificity
controls (bad signature) are rejected — proving rejection is on the signature, not the position.
(Test `TestWorker_TA_Keeper_PositionAndCount`; hardened oracle
`TestG2_TA_Keeper_HardenedOracle`; library-level `TestWorker_TA_Library_PositionNotBoundToHash`.)

**(T-A′) Count/sum are read from the committed root, not from distinct served work.**
`x/proof/types/claim.go` L20–21/L32–33 read the claim's compute-unit `Sum` and relay `Count`
**directly** from the committed Merkle-sum-tree root
(`smt.MerkleSumRoot(claim.GetRootHash()).Sum()` / `.Count()`), with no per-leaf re-verification of
distinctness. `x/tokenomics/keeper/token_logic_modules.go` L94–97 confirms in-code that settlement
pays on `root.Count`. Duplicating one valid relay at N non-canonical positions inflates the claimed
`Count` to N (measured at N = 2, 16, 1024), and the keeper-sampled "closest" leaf is **always a
valid relay** (depth grows ≈ log2(N)), so the mandatory-proof spot check passes.

**(P-09) Grouping false leaves under a common prefix decouples inflation from spot-check risk.**
A simulation at an identical committed sum shows the closest-leaf-is-valid rate at **≈ 0.9846
(grouped)** versus **≈ 0.0165 (ungrouped)** — a gain of **≈ 59×** from grouping alone (independent
control `TestG2_P09_GroupedVsUngrouped_WithVerify`, with each closest proof additionally re-run
against the committed root: `verifyFail = 0`). Marked `[measurement, simulation]`; **not** presented
as a proven mainnet exploit.

**Economic bound (this is the load-bearing honesty of F2).** The settled amount is capped by the
application-budget **floor** `= appStake / numSessions / numSuppliers`
(`token_logic_modules.go` L385; `settlement_context.go` L720–724), and settlement is burn=mint
against the application's stake (`tlm_relay_burn_equals_mint.go` L83–141). Inflation therefore
**cannot exceed that floor per supplier**; a supplier whose honest work is below the floor gains
strictly, at the expense of the **application's burned stake**. The victim is the application, and
the magnitude is bounded — **never "unlimited".**

**Honest bound (verbatim).** "Bounded by the application-budget floor (≤ floor per supplier); the
victim is the application's burned stake, not 'unlimited'. T-A is not the only lever (canonical-key
grinding also inflates count); T-A's marginal value = grinding cost avoided."

### F3 — Response-integrity check absent in `ValidateRelayResponse`
**Level: MECHANISM ESTABLISHED, CONDITIONAL EXPLOITABILITY. Panel vote: 2/1. Third-party system
(`shannon-sdk`). Weakest of the four.**

**Mechanism (code).** `ValidateRelayResponse` (`shannon-sdk/relay.go` L86–129) performs Unmarshal →
`ValidateBasic` → fetch operator pubkey → `VerifySupplierOperatorSignature`. There is **no
comparison of `SHA256(payload)` against `payload_hash`.** `RelayResponse.ValidateBasic`
(`x/service/types/relay.go` L106–133) contains the payload-hash check **commented out** (L112–114);
the commented code is a *presence* check (`len == 0`), **not** an equality check. `GetSignableBytesHash`
(L66–100) sets `res.Payload = nil` when `PayloadHash != nil` (L89–90) before hashing — so the
operator's signature covers the **`payload_hash` field, not the payload bytes.** An intermediary can
replace the `payload` bytes while keeping `payload_hash` and the signature, and `ValidateRelayResponse`
accepts the altered response (test `TestWorker_P2_PayloadSubstitution`; positive control: a
consistent response is accepted).

**Bound / conditional exploitability.** This is a weakness of a **third-party system** (`shannon-sdk`).
Exploitation assumes a threat model: an intermediary on the RelayMiner→gateway path, or a malicious
supplier. We could **not** establish a served consumer of this path at code (the only pinned caller
is a test CLI); the served gateway path (PATH, at its `main`) returns raw bytes without adding the
comparison, so it does not close the gap, but neither did we establish a served victim. We therefore
state exploitability as **conditional**, not unconditional.

### F4 — Settlement re-draw of an invalid proof
**Level: LEAD (UNTESTED). This is a hypothesis and future work, not a finding.**

**Code-level lead only.** At settlement, the proof requirement is re-derived from the stored claim.
Validation writes `ProofValidationStatus` (protobuf field 4) into the claim; because that field is
included in `Marshal`, writing it **changes the claim's serialized bytes and therefore its hash**,
which is the hash that drives the proof-requirement draw
(`settle_pending_claims.go` L1056/L1153–1164; `validate_proofs.go` L197–198;
`settleClaim` reads status only when a proof is required, L1082–1120). It is therefore **plausible
that a well-formed-but-invalid proof would be re-drawn** at settlement (most likely to an "invalid"
outcome again) and, unless re-drawn into the "required" band, settled and paid.

**This is explicitly untested.** We did not build a keeper test for it (it is analogous to the F2
harness, but out of scope for the tests we ran). We deliberately **omit the on-chain counterfactual
figures** we hold internally; they are not needed to state the lead and we do not republish them.
We flag this as future work under our internal item identifier **POCKET-SETTLEMENT-REDRAW-1** and
would be glad to build the keeper test collaboratively if the maintainers find the lead credible.

**Non-claim.** F4 is **never** presented as confirmed, and never as a "finding".

---

## 6. Impact and severity

| Finding | What it breaks | Who pays | Bound / caveat |
|---|---|---|---|
| **F1** | The mandatory-proof sampler selects below the intended rate — ≈ half (audit ≈ 2× weaker) in the **sub-percent** regime, with a smaller deficit (≈ a quarter at a draw probability of 0.25) as the parameter grows | The integrity of the audit sampling, most acute for a small `proof_request_probability` | Code mechanism + parameter-dependent prediction; the exact factor for the configured parameter is **maintainer-verifiable**, not asserted by us |
| **F2** | A claim's `Count`/`Sum` is inflatable without distinct served work, and the mandatory-proof spot check is bypassable (position not bound; grouped/duplicated leaves) | The **application's burned stake** | **Bounded by the per-supplier settlement floor**; not unlimited; T-A is one lever among others (canonical-key grinding also inflates count) |
| **F3** | A relay response's bytes can be altered while keeping the signed `payload_hash` | A consumer that trusts the response bytes | **Conditional** on a threat model (intermediary / malicious supplier); no served consumer established at code; weakest item |
| **F4** | *(lead)* an invalid proof might be re-drawn at settlement and paid | *(untested)* | **UNTESTED**; hypothesis / future work only |

We do not assign a numeric CVSS; the severity of F1/F2 depends on parameters and application
budgets that the maintainers are best placed to weigh. Our qualitative reading: **F2 (with F1
weakening the audit that is supposed to catch it) is the substantive pair**; F3 is a real but
conditional third-party weakness; F4 is a lead.

---

## 7. Remediation

Each item has a direct, local fix.

- **F1 (seed derivation).** Do not pass a `binary.Varint`-truncated value as the RNG seed. Derive
  the seed from the **full 32 bytes** of `seedHash` (e.g. seed a 64-bit source from
  `binary.BigEndian.Uint64(seedHash[:8])`, or use a hash-to-float that consumes the whole digest),
  so that all input entropy reaches `Float64()`. A regression test should assert that the empirical
  selection rate over many distinct seeds matches the configured probability within a tight
  tolerance (the current mechanism fails such a test at ≈ 0.5×).
- **F2 (bind position and count to served work).**
  - Bind the proven leaf's **position to the relation hash**: at validation, re-derive the expected
    leaf key from `H(relation)` and require `proof.ClosestPath` to match it (rather than trusting
    the supplied path). Equivalently, verify the leaf against a path hasher that recomputes the key
    from the value.
  - Bind **`Count`/`Sum` to distinct served work**: enforce leaf distinctness (reject duplicate
    relay leaves), and/or make the mandatory-proof spot check sample enough independent leaves that
    grouping/duplication cannot survive with high probability. The goal is that the committed
    `Count` cannot exceed the number of *distinct, served* relays.
- **F3 (response integrity).** Restore the equality check: add `SHA256(payload) == payload_hash`
  in `ValidateRelayResponse` (and un-comment/repair the equality — not merely presence — check in
  `RelayResponse.ValidateBasic`). Ensure the served path (PATH) performs this comparison before
  returning bytes.
- **F4 (re-draw).** If the lead is confirmed, exclude `ProofValidationStatus` (and any other
  post-validation mutable field) from the claim serialization that feeds the proof-requirement
  draw, so that writing a validation status cannot re-draw the requirement. A keeper test analogous
  to the F2 harness would settle whether the lead is real.

---

## 8. Reproduction package (by reference)

We provide reproduction **by reference**, not as a runnable attack recipe: the pinned tree, the
file sha, the deterministic environment, and the **names** of the sealed tests and their raw output.
This is sufficient for a maintainer to re-run every mechanism and insufficient as a turnkey exploit.

- **Pinned tree.** `poktroll @ a109dd0bae65c1d96b010d65f4cdc5bc77a50fc2`; `smt@v0.14.1`;
  `shannon-sdk@a508808fbbe0`; Go 1.26.5.
- **Deterministic environment.** Isolated sandbox; modules fetched once then `GOPROXY=off`; all
  tests run with `-count=1`; generated mocks regenerated from the repository's own `//go:generate`
  directives; no production code modified; no network to any Pocket endpoint during testing.
- **Sealed evidence (resealed, sha-pinned, 2026-09-29).** The reports, the first-hand oracle, and
  the keeper/oracle sources are held in a sealed custody directory
  (`test-evidence-2026-09-29/`), enumerated by `SHA256SUMS-2026-09-29.txt`. The sha of each artifact
  are reproduced in Appendix B so that the maintainers can confirm they are re-running exactly what
  we ran.
- **Tests and oracles (by name).**
  - `TestWorker_TA_Library_PositionNotBoundToHash` — library-level: a leaf at a non-canonical key
    verifies (F2/T-A).
  - `TestWorker_TA_Keeper_PositionAndCount` and `TestG2_TA_Keeper_HardenedOracle` — settlement path:
    non-canonical position settles; `Count` = N at N = 2/16/1024; controls reject on signature
    (F2/T-A, T-A′). In the hardened oracle the passing assertions **are** the oracle
    (`require.NoError` on the attack cases, `require.Error` on the controls).
  - `TestWorker_P3_GroupedLeavesInflation_Sim` and `TestG2_P09_GroupedVsUngrouped_WithVerify` —
    grouped vs ungrouped survival at identical committed sum (F2/P-09).
  - `TestWorker_P2_PayloadSubstitution` — altered payload with kept `payload_hash`/signature is
    accepted (F3).
  - `g7check/main.go` — first-hand 128-seed enumeration (F1 prediction).
- **Re-run sketch.** In the pinned tree, e.g.
  `go test ./x/proof/keeper/ -run TestWorker_TA_Keeper_PositionAndCount -count=1 -v`,
  `go test ./pkg/crypto/protocol/ -run 'TestWorker_TA_Library|TestWorker_P3' -count=1 -v`,
  `go test ./pkg/crypto/rand/ -run TestWorker_TB_SeededFloat64_MechanismRate -count=1 -v`,
  and `go run ./g7check` for the F1 oracle. Exact file names and sha are in Appendix B.

---

## 9. Limitations and non-claims

We state the boundaries of this work explicitly. Each item below is a deliberate **non-claim**.

- **We do NOT claim "unlimited theft".** F2 is **bounded by the application-budget floor**
  (≤ floor per supplier); the victim is the application's burned stake.
- **We do NOT claim T-A is "the" lever.** Count can also be inflated by canonical-key grinding;
  T-A's marginal value is the grinding cost avoided. F2 is a cluster, not a single primitive.
- **We do NOT claim F3 is unconditionally exploitable.** It is a third-party (`shannon-sdk`)
  mechanism whose exploitation assumes an intermediary or a malicious supplier; **no served
  consumer was established at code** (the only pinned caller is a test CLI). It is the weakest item.
- **We do NOT present F1 as an on-chain figure we mined.** F1 is a **code mechanism plus a
  prediction** (effective rate ≈ half the intended parameter), verifiable by the maintainers
  against their own data. We publish **no on-chain aggregates** about network participants in this
  report.
- **F4 is NOT a finding.** It is an **untested code lead**; it is never "confirmed". We omit the
  on-chain counterfactual figures we hold internally.
- **Patch status is history-based** (GitHub file history + the read `shannon-sdk` patch), not a
  byte-diff `a109dd0..main`; embargoed/private fixes would not be visible to us.
- **The analysis was performed by LLM agents** under the verification discipline of §4; the
  reproduction package, not our word, is the basis for belief.

---

## 10. Coordination and disclosure timeline

- **2026-08 → 2026-09.** Independent code reading and local testing at `a109dd0`; internal
  adversarial verification and full replay.
- **2026-09-29.** Evidence resealed and sha-pinned; this report prepared for private disclosure.
- **On submission (this advisory).** Private disclosure to the maintainers via a **GitHub private
  security advisory**. We have made, and will make, **no public statement** — anonymized or
  otherwise — ahead of coordinated disclosure.
- **Proposed coordination.** We suggest a standard responsible-disclosure window (commonly 90 days)
  for a coordinated public advisory, adjustable by mutual consent; we are happy to follow the
  maintainers' preferred process and to help validate fixes. The exact window and any public-CVE
  handling are open and [investor to confirm at submission].
- **Contact / channel.** GitHub private security advisory on `pokt-network/poktroll`; an
  alternative contact address may be supplied at submission if the maintainers prefer
  [investor to confirm at submission].

---

## Appendix A — Claims register

| # | Finding | Level | Panel vote | Evidence (at `a109dd0`) | Honest bound (verbatim) |
|---|---|---|---|---|---|
| F1 | Proof-sampler entropy collapse: `binary.Varint` folds ~half of seeds to 128 values (~7 bits); predicted effective rate ≈ 0.5‰ vs intended ≈ 1‰ | MECHANISM ESTABLISHED (code) + PREDICTION | advisor-adjudicated; reproduced 3 lenses | `float.go` L16–25; `g7check/main.go` 128-seed enumeration (k<p = 0/128; predicted 0.501‰); maintainer-verifiable against own data | Present as CODE MECHANISM + PREDICTION; do NOT present ourselves as having mined the on-chain figure; empirical consistency is maintainer-reproducible |
| F2 | Claim inflation: count/sum not bound to distinct served work; mandatory-proof guard bypassable (T-A position + T-A′ duplicates + P-09 grouping) | CONFIRMED | 3/0 (T-A); P-09 1/1 tie-break, then reproduced | `proof_validation.go` L298–341/L457–471; `smt/proofs.go` L357–391; `claim.go` L20–21/L32–33; floor `token_logic_modules.go` L385 + `settlement_context.go` L720–724; burn=mint `tlm_relay_burn_equals_mint.go` L83–141; P-09 grouped 0.9846 vs 0.0165 (≈59×) | Bounded by the application-budget floor (≤ floor per supplier); victim is the application's burned stake, not "unlimited"; T-A is not the only lever (canonical-key grinding also inflates count); T-A's marginal value = grinding cost avoided |
| F3 | Response-integrity check absent: `ValidateRelayResponse` does not compare `H(payload) == payload_hash` | MECHANISM ESTABLISHED, CONDITIONAL EXPLOITABILITY | 2/1 | `shannon-sdk/relay.go` L86–129; `x/service/types/relay.go` L106–133 (commented presence check, not equality), L66–100/L89–90 | Third-party system (shannon-sdk); exploitability assumes an intermediary on RelayMiner→gateway or a malicious supplier; no served consumer established at code (only pinned caller = a test CLI); weakest of the four |
| F4 | LEAD (untested): settlement re-draw — writing `ProofValidationStatus` changes the claim hash driving the requirement draw; an invalid proof plausibly re-drawn and settled | LEAD (UNTESTED) | n/a | `settle_pending_claims.go` L1056/L1153–1164; `validate_proofs.go` L197–198; L1082–1120; **never tested at the keeper** | Present as a hypothesis / future work, never as a finding; on-chain counterfactual figures kept internal; item POCKET-SETTLEMENT-REDRAW-1 |

### Forbidden phrasings → explicit non-claims (see §9)
- "unlimited theft" / "vol illimité" → **non-claim** (F2 bounded by app floor).
- "T-A is THE lever" → **non-claim** (canonical-key grinding also inflates count).
- F3 "unconditionally exploitable" → **non-claim** (conditional on threat model; no served consumer).
- "we established the on-chain cause" / republished mined aggregates → **non-claim** (F1 = mechanism + prediction; no on-chain aggregates in this report).
- F4 "finding" / "confirmed" → **non-claim** (untested lead).

## Appendix B — Verification chain and artifact sha256

**Base-file re-verification (7/7 sha match at `a109dd0` / pinned deps).**

| File | sha256 |
|---|---|
| `x/proof/keeper/proof_validation.go` | `d269c1905ea4aa14e3ce814b7d8de6bfa1275b8687a50e5b742743fbde0db6a8` |
| `smt@v0.14.1/proofs.go` | `be819710eb6f347433b91dcdede218b527b2b19858f10cd888debefac90d6c77` |
| `smt@v0.14.1/hasher.go` | `997b170305b75984e36abfffc5c2f66e4beb5c3464d1aeb1d5984deb28fa53f1` |
| `pkg/crypto/rand/float.go` | `7cea92755b8a0f1825ef68136edad7b196c17805371bb017198933c0a02fbdbf` |
| `x/service/types/relay.go` | `4ba663db0afce7a0bc460c4d178373a69ac0edd0af9dddaf3c519791fa2fc80b` |
| `x/tokenomics/keeper/token_logic_modules.go` | `73ec768d79ce97e6b832dabb4e64f4db4910217cdeb304c9af34750293af31b6` |
| `x/proof/types/claim.go` | `1e198c30813d33bde1af6af74f08746f224313eb44a8b1884bb5f99bd08f82ce` |

**Verification runs (internal identifiers, for our provenance).**
- `wf_759534a9-512` — adversarial verification panel (11 verifiers + 1 advisor lens; 0 errors).
- Independent full replay (fresh context): 7/7 base-file sha match; four tests + the 128-seed
  oracle reproduced with `-count=1` (T-B mechanism ratio ≈ 0.50; oracle prediction 0.501‰).
- `wf_4bf28a54-e17` — a further internal 3-lens verification (reproducibility, data integrity,
  soundness) whose **on-chain attribution outputs are held internal to our study and are not
  reproduced here**, consistent with §0 and §9.

**Sealed evidence directory (`test-evidence-2026-09-29/`), sha256 (from `SHA256SUMS-2026-09-29.txt`).**

| File | sha256 |
|---|---|
| `RAPPORT.md` | `eb1c577e1536bafb616a28e700b0738f0ba84c3e9ea089938d4be9aecf4cdeac` |
| `REPLAY-TB.md` | `25cff9ceb282e4dd1187c598bc0c779c80a7a46696964bdbbada25c1208fffba` |
| `REJEU-G2.md` | `688c069b7dff35f90145e46e26c1d89918903775b3ddd58cc0d0e81bf0e3c336` |
| `main.go` (g7check oracle) | `5944e3a7615e72115d2ce19b9225e222a91031c645f380523fdc54426d920751` |
| `keeper-tests/g7check__main.go` | `5944e3a7615e72115d2ce19b9225e222a91031c645f380523fdc54426d920751` |
| `keeper-tests/p09verif__main.go` | `522b54cfd98f9668860537328ec37afa9f4055242808bca6048c6f816a7ae2c1` |
| `keeper-tests/verif-p2__relay_3e1b2ab.go` | `4ba663db0afce7a0bc460c4d178373a69ac0edd0af9dddaf3c519791fa2fc80b` |
| `MISSION-worker-test-A-B.md` | `c35a0c62496b459ffcdd38b3dec763dacb3d7a7373f21af41a16e366e9ff7a86` |
| `MISSION-replay-TB.md` | `5cb298802ff306d9a4700b649f36a54d5903c356b9f469038469cf60c8903bfe` |

---

*Internal provenance (not part of the disclosure to Pocket).* Report drafted 2026-09-29 under the
MONARK/Shōgen engineering discipline; drafting model `claude-opus-5-5` (effort max); prepared for
gated outbound submission by the orchestrator (`claude-fable-5-1`); attaching ADR: ADR-0028; spec:
`docs/pocket-report/G0-claims-register.md`. Nothing in this report is submitted by any agent; the
investor submits. We claim no contract, reward, or permission from Pocket; this is independent,
good-faith research.
