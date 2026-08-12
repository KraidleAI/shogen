# `just verify` — la même entrée qu'en CI (DEVOPS §3 : « mêmes gates en local
# via `just verify` » ; ADR-0013, point 4). Ce fichier ne fait que déléguer :
# la logique des gates vit dans `xtask`, pas dans deux endroits.

default:
    @just --list

# Toutes les gates mécanisées + fmt + clippy.
verify:
    cargo xtask verify

# La suite complète, verrouillée (dont les mutants semés des gates).
test:
    cargo test --locked --workspace -- --nocapture

# Le walking skeleton de bout en bout : émission, verdict, mutation, refus.
skeleton:
    cargo xtask emettre-exemple target/lots/lot.cbor
    cargo run --locked --quiet --package shogen-verifier -- target/lots/lot.cbor
    cargo xtask muter target/lots/lot.cbor target/lots/lot-mute.cbor 0 255
    ! cargo run --locked --quiet --package shogen-verifier -- target/lots/lot-mute.cbor

# S-G7, volets licences/bans/sources/advisories (exige cargo-deny installé).
deny:
    cargo deny --locked check
