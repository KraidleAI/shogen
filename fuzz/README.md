# `fuzz/` — les deux cibles de fuzz **instrumenté** du vérificateur

Rattachement (G0) : ADR-0011 seuil 7 ; ADR-0009 point 3 (clarification du
2026-08-13) ; ADR-0015 pt 15 (deny par workspace) ; `docs/R-8-outillage.md`.

Ce répertoire est un **workspace indépendant** (son propre `Cargo.lock`), au
même titre qu'`adapters/`. Il porte deux paquets qui enrobent **la même
cible** — `shogen_verifier::eprouver`, une fonction totale, `no_std`, sans
I/O — avec deux moteurs différents :

| paquet | moteur | toolchain | plateforme |
|---|---|---|---|
| `libfuzzer/` | libFuzzer, piloté par `cargo-fuzz` 0.13.2 | **nightly-2026-08-10**, épinglée par date, réservée à ce moteur | Linux en CI ; Windows possible mais dépendant d'un runtime MSVC hors dépôt (voir plus bas) |
| `afl/` | AFL++ 4.40c (version mesurée à l'exécution : clé `afl_version` de `fuzzer_stats`, campagnes du 2026-08-13 ; le job CI l'imprime aussi au journal de `cargo afl config --build`), piloté par `cargo-afl` 0.18.2 | la **1.97.1** du dépôt | Linux seulement (AFL++ n'a pas de cible Windows) |

Le **troisième** moteur n'est pas ici : `cargo xtask fuzz` est le harnais en
arbre, aveugle (non guidé par la couverture), à zéro dépendance et zéro outil,
et il tourne sur les deux plateformes. Les trois s'additionnent ; aucun ne
remplace l'autre.

Les trois partagent le **même corpus de graines committé** :
`crates/shogen-verifier/fuzz-corpus/` — des octets bruts, jamais du texte
(`.gitattributes` racine). Deux écarts de consommation, publiés : les jobs
CI passent aux moteurs une copie SANS `README.md` (le registre du corpus
n'est pas une graine), et AFL saute silencieusement la graine de taille
nulle (`dirigee-cbor-vide.bin`) — mesuré, rendu visible par le job.

## Rejouer les campagnes

Les commandes ci-dessous sont celles qui ont été **exécutées et mesurées** le
2026-08-13 (WSL2 Ubuntu, 24 cœurs, gcc 15.2.0). Les répertoires de sortie sont
hors dépôt : le corpus committé n'est jamais écrit par une campagne.

```sh
# ── moteur libFuzzer ────────────────────────────────────────────────────────
rustup toolchain install nightly-2026-08-10 --profile minimal --no-self-update
# La même garde que la CI : la nightly servie se vérifie à l'octet.
test "$(rustc +nightly-2026-08-10 --version)" =     "rustc 1.99.0-nightly (969b803cb 2026-08-09)" || echo "NIGHTLY DIVERGENTE"
cargo install cargo-fuzz --version =0.13.2 --locked

# Le PREMIER répertoire est celui où libFuzzer ÉCRIT ; les suivants sont lus.
cargo +nightly-2026-08-10 fuzz run --fuzz-dir fuzz/libfuzzer eprouver \
    ~/fuzz-out/libfuzzer-corpus \
    crates/shogen-verifier/fuzz-corpus \
    -- -max_total_time=660 -print_final_stats=1

# ── moteur AFL++ ────────────────────────────────────────────────────────────
cargo install cargo-afl --version =0.18.2 --locked
cargo afl config --build          # construit AFL++ depuis les sources
# Le binaire atterrit dans le target/ DU WORKSPACE fuzz/, pas dans celui de
# la racine : `--manifest-path` fixe le workspace. Mesuré le 2026-08-13 —
# `fuzz/target/release/eprouver-afl` existe, `target/release/eprouver-afl` non.
cargo afl build --release --locked --manifest-path fuzz/afl/Cargo.toml

# afl-fuzz SAUTE en silence toute graine de taille nulle : la copie et le
# `-size 0 -print` rendent visible ce que le corpus committé perd de ce
# côté-là (`dirigee-cbor-vide.bin`, graine légitime pour les deux autres
# moteurs).
mkdir -p ~/afl-in && cp crates/shogen-verifier/fuzz-corpus/* ~/afl-in/
rm -f ~/afl-in/README.md && find ~/afl-in -type f -size 0 -print -delete
AFL_SKIP_CPUFREQ=1 AFL_NO_AFFINITY=1 cargo afl fuzz \
    -i ~/afl-in -o ~/afl-out -V 660 -- fuzz/target/release/eprouver-afl
```

`kernel.core_pattern` doit valoir `core` (afl-fuzz refuse de démarrer sinon).
Il l'était déjà sur la machine de mesure ; en CI, le job l'impose par
`sudo sysctl`.

## La gate de distillation (lot FUZZ, 2026-10-09)

Le job `cargo-afl` mesure, avant sa campagne, la couverture des graines
distillées (`crates/shogen-verifier/fuzz-corpus/README.md`) par l'outil de la
mesure de référence, sur la cible AFL construite ci-dessus :

```sh
D=~/distillation && P=docs/adr-0028/revue-fuzz/pieces && mkdir -p "$D/corpus" "$D/base"
cp crates/shogen-verifier/fuzz-corpus/* "$D/corpus/" && rm "$D/corpus/README.md"
cp "$D/corpus/"* "$D/base/" && rm "$D/base/"dirigee-distillee-*
tar -xzf "$P/corpus-derive-2026-10-09.tar.gz" -C "$D"
for carte in base corpus derive; do
  cargo afl showmap -C -i "$D/$carte" -o "$D/$carte.carte" -- fuzz/target/release/eprouver-afl
done
cargo xtask fuzz-distillation "$D/base.carte" "$D/corpus.carte" "$D/derive.carte"
```

Le corpus dérivé de la mesure (2353 entrées, campagnes de 660 s des deux
moteurs) n'entre pas au corpus de graines, comme le veut `fuzz/.gitignore` :
il est versé en archive avec les pièces de revue du lot
(`docs/adr-0028/revue-fuzz/pieces/`), où la gate le relit.

## Ce qu'une campagne verte dit, et rien de plus

*tested* — sur les cas exécutés, avec leur compte, leur corpus de départ et
leur budget, à la date. Jamais *proven* : l'absence de panique n'est pas
établie (ADR-0010, §Coûts point 6). Un moteur guidé par la couverture change la
**probabilité** d'atteindre un chemin profond ; il ne change pas la nature de
ce qu'une campagne conclut.

## Windows : ce qui a été mesuré, et ce qu'on n'en conclut pas

Trois mesures du 2026-08-13 sur l'hôte Windows 10 (msvc, même nightly datée) :

1. `cargo fuzz build` : **vert**, 10,37 s.
2. `cargo fuzz run` tel quel : **rouge**, `exit code: 0xc0000135,
   STATUS_DLL_NOT_FOUND`. Cause lue dans la table d'imports du binaire produit,
   pas devinée : `clang_rt.asan_dynamic-x86_64.dll`, absent du `PATH` **et**
   absent de la toolchain rustup.
3. `cargo fuzz run` avec le répertoire du runtime MSVC au `PATH` : **vert**,
   « Done 349857 runs in 31 second(s) », code 0, zéro panique.

Ce qu'on en conclut : cargo-fuzz **n'est pas** inapte à Windows. Ce qui
empêche un job CI Windows est que ce runtime vit dans une installation Visual
Studio, sous un chemin qui porte un numéro de version de MSVC — pas un fait
stable d'une image de runner. Le job reste Linux, et c'est écrit comme une
dépendance d'environnement, pas comme une impossibilité. Pour AFL++, la
contrainte est d'une autre nature et n'admet pas ce contournement : il n'a pas
de cible Windows.
