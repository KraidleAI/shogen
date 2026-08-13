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

# Le double-build n'est PAS dans `verify` : il coûte deux constructions release
# complètes, et sa cible ratifiée est Linux x86_64 seul. Il est bloquant là où
# il est ratifié — .github/workflows/reproductibilite.yml. Sur Windows la
# commande tourne quand même et dit ce qu'elle a pu varier : le bit-à-bit n'y
# est pas la cible (ADR-0012 D6, « Windows à terme et sans date »).
#
# Deux constructions du vérificateur, 6 variations d'environnement entre elles, empreintes comparées (ADR-0012 D6).
double-build:
    cargo xtask double-build

# S-G7, volets licences/bans/sources/advisories (exige cargo-deny installé).
deny:
    cargo deny --locked check

# Régénère les sidecars texte des PDF de biblio/ (extraction locale pour la
# gate S-G5 ; *.sidecar est gitignoré — les octets ne quittent jamais le
# poste, DEVOPS §1). Exige pdftotext (poppler) sur le PATH.
sidecars:
    cd biblio && for f in *.pdf; do pdftotext -enc UTF-8 "$f" "$f.sidecar"; done
