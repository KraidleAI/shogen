# Shōgen (証言 — "testimony")

*Version française : [README.fr.md](README.fr.md).*

**Attested-fact infrastructure for AI agents — the "perception" counterpart
of the Kraidle authority kernel.**

## The founding sentence

An attestation proves **what the source said** — never that the source tells
the truth. The whole project comes down to this distinction, and the name
carries it: a testimony is a deposition, not a truth.

## The product in one sentence (working hypothesis, not frozen)

A layer that turns the world's responses (APIs, feeds, pages) into
**attested testimonies, typed as dated facts with traceable provenance**
(the attestation covers the bytes; the typing is an identified adapter —
03 §3), aggregated by **quorums whose diversity is measured on its
observable axes** (infrastructure, upstream dependencies) **and only
declared on the others** (jurisdiction, operator), with ranks published
(04 §1), and delivered in a vocabulary that a decision kernel — starting
with Kraidle — can consume, with offline verification of the batch by a
third party.

## The relationship with Kraidle

- Kraidle: *bounded authority* — no irreversible action without a permit
  bound to the bytes. In Kraidle, perception is bounded and made visible,
  never prevented.
- Shōgen: *attested perception* — no critical fact without a testimony bound
  to its source, and no quorum without a measurement of independence.
- Kraidle's `gather` requires facts whose provenance is attested by their
  sources (ADR-0017 Kraidle) and quorums for critical classes (ADR-0023);
  A(indépendance des sources), i.e. source independence, is a named,
  undischarged debt there. Shōgen is the tool that discharges it. The two
  projects remain sovereign: Shōgen is sold to any agent, with or without
  Kraidle.

## Project status

- 2026-07-30: creation. Three candidate ideas recorded (`docs/00-idees.md`),
  Shōgen selected. Librarian pass executed (`docs/01-precedents.md`,
  `biblio/INDEX.md` — 8 artifacts); main conclusion: the transport primitive
  (zkTLS) is mature and must not be rebuilt (ADR-0001, `docs/DECISIONS.md`);
  the gap is the semantic/quorum/diversity layer above it. Written the same
  day: vision (`02`), canonical testimony form (`03`), diversity certificate
  (`04`), S0–S5 roadmap (`05`), DevOps plan (`DEVOPS.md`). Repository
  `Kraidle/shogen` created (private), founding commit signed. A multi-agent
  documentation audit (22 confirmed findings) was applied the same day — this
  text incorporates its corrections.

## Discipline

From day 1, this project adopts Kraidle's discipline, adapted: the three
assurance words (proven/tested/reviewed), sources opened before being cited,
figures measured within the pass, decisions in ADRs with alternatives and
costs. The `kraidle-*` skills apply mutatis mutandis until Shōgen has its own.

## License

This repository is dual licensed, at the recipient's option (ADR-0017,
Rust ecosystem convention):

- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE))
- MIT License ([LICENSE-MIT](LICENSE-MIT))

Unless you explicitly state otherwise, any contribution intentionally submitted
for inclusion in the work by you, as defined in the Apache-2.0 license, shall be
dual licensed as above, without any additional terms or conditions.

`biblio/` is not part of the repository as distributed (DEVOPS §1): the
artifacts held locally each keep their own regime.
