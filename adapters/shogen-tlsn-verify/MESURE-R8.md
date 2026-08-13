# Mesure R-8 du compagnon `shogen-tlsn-verify` — le compte définitif

> Mesures du **2026-08-13**, passe S3 phase C, chantier T. Toutes les valeurs de
> ce document sont **copiées de la sortie de la commande citée en regard**, sur
> le workspace `adapters/shogen-tlsn-verify` **construit**. Aucune n'est une
> estimation.
>
> Rattachement (G0) : **ADR-0015**, note d'adjudication — « le compte définitif
> est la mesure R-8 du compagnon, due en phase C » ; **ADR-0012 D5** (R-8 en
> deux moitiés) ; **R-8** du corpus (vérification registre AVANT installation).
>
> Environnement : WSL2, Ubuntu 26.04 LTS, noyau `6.18.33.2-microsoft-standard-WSL2
> x86_64`, `cargo 1.97.1 (c980f4866 2026-06-30)` / `rustc 1.97.1 (8bab26f4f
> 2026-07-14)` — la toolchain épinglée du dépôt.

---

## 1. Le compte de fermeture — ce que la phase C tranche

ADR-0015 portait **deux** chiffres pour la forme α, calculés sur les manifestes
et le lock amont détenus : **116** (fermeture à features déclarées, worker de
phase B) et **359** (fermeture majorante sans élagage de features, recompte
orchestrateur). Ni l'un ni l'autre ne mesurait la forme retenue. Voici la
mesure de la forme retenue, sur le binaire qui existe.

| grandeur | valeur MESURÉE | commande dont la sortie porte la valeur |
|---|---|---|
| paquets tiers du graphe **normal**, cible hôte, `name+version` uniques | **96** | `cargo tree -e normal --prefix none --no-dedupe \| sed 's/ (.*//' \| sort -u \| grep -cv '^shogen-tlsn-verify'` |
| les mêmes, **noms** uniques (versions confondues) | **89** | même commande, `sed 's/ v[0-9].*//'` |
| paquets tiers du graphe normal, **toutes cibles** (`--target all`) | **117** | `cargo tree -e normal --target all --prefix none --no-dedupe \| …` |
| paquets tiers, **toutes cibles et toutes arêtes** (normal + build + dev) | **122** | `cargo tree --target all --prefix none --no-dedupe \| …` |
| blocs `[[package]]` du `Cargo.lock` du compagnon | **123** | `grep -c '^\[\[package\]\]' Cargo.lock` |

**Le compte définitif attendu par ADR-0015 est donc 96** (fermeture tierce du
graphe normal, cible de construction), **117** si l'on refuse tout filtrage de
cible, **123** paquets au lock. Les trois se déduisent l'un de l'autre par une
règle explicite, et aucun ne dépend d'un jugement.

**Ce que l'écart aux chiffres d'ADR-0015 mesure** : la forme β ne dépend pas de
la crate parapluie `tlsn` mais de **`tlsn-attestation` seule** — la vérification
n'a besoin d'aucune pièce du protocole MPC. Pour comparaison mesurée, le
conducteur de session (`session/`, qui tire `tlsn` entier) porte **267** paquets
tiers au graphe normal et **308** blocs au lock, avec **38** entrées git.
L'ordre de grandeur d'ADR-0015 (« plus de cent crates tierces dans les deux
cas ») était juste pour la forme α ; la forme β coûte **96**, soit un tiers de
ce que coûterait le graphe complet du transport.

Pour mémoire, l'état que la forme β protège, **re-mesuré le 2026-08-13 après
écriture du compagnon** : `cargo tree -p shogen-verifier -e normal` rend
**2 lignes** — `shogen-verifier` et `shogen-core`, une seule arête. Le workspace
racine a **3 membres** (`shogen-core`, `shogen-verifier`, `xtask`,
par `cargo metadata --no-deps`) et n'en compte aucun de ce répertoire.
ADR-0015 pt 6 tient, et il tient **mécaniquement** : le compagnon est un
workspace indépendant, avec son propre `Cargo.lock` ; aucune arête ne peut
remonter.

---

## 2. Crates épinglées par révision git

**4** entrées `source = "git+"` au `Cargo.lock` du compagnon
(`grep -c 'source = "git+' Cargo.lock`) :

| crate | dépôt | révision au lock |
|---|---|---|
| `tlsn-attestation` 0.1.0-alpha.16-pre | `github.com/tlsnotary/tlsn` | `0fe3c32d35382b3f290a43c4156399ca4512bb89` |
| `tlsn-core` 0.1.0-alpha.16-pre | `github.com/tlsnotary/tlsn` | idem |
| `tlsn-tls-core` 0.1.0-alpha.16-pre | `github.com/tlsnotary/tlsn` | idem |
| `rs_merkle` 1.4.2 | `github.com/tlsnotary/rs-merkle.git` (fork) | `85f3e827451e18c21f110068b4322fb99d2f0a8c` |

L'épinglage est **par révision**, jamais par version de registre : contrôle
registre de phase A (pièce `biblio/cratesio-search-tlsn-2026-08-12.json`), les
crates `tlsn*` n'existent pas sur crates.io. `rs_merkle` était déjà nommé par
ADR-0015 comme « ≥ 1 » crate git de la forme α ; la mesure confirme que la forme
β en hérite aussi, par `tlsn-core`.

---

## 3. Crates à chaîne C / build natif

Mesure par `cargo tree -e normal --prefix none --no-dedupe | sed 's/ v[0-9].*//' | sort -u | grep -x <nom>`
(présence au graphe normal, cible hôte) et `grep -c '^name = "<nom>"$' Cargo.lock`
(présence au lock, toutes arêtes) :

| crate | graphe normal (hôte) | lock | tirée par (mesuré, `cargo tree -e normal -i`) |
|---|---|---|---|
| `ring` | **1** | 1 | `rustls-webpki` 0.103.14, `sct` 0.7.1 et `tlsn-tls-core` — tous sous `tlsn-attestation` |
| `libc` | **1** | 1 | (transitive) |
| `cc` | **0** | 1 | build-dependency de `ring` — hors graphe normal, présente au lock |
| `windows-sys` | **0** | 1 | arête à cible Windows, filtrée par la cible hôte Linux |
| `web-time` | **1** | 1 | `tlsn-core` et `tlsn-tls-core` |
| `openssl-sys` | **0** | — | absente |

**Constat, sans arbitrage** : `ring` + `cc` **sont** dans la fermeture du
compagnon, et `web-time` (l'horloge) aussi. ADR-0015 rejetait la forme α en
partie pour cela (motifs 2 et 4) — mais ces motifs portaient sur l'entrée de ces
crates dans **`shogen-verifier`**, l'artefact de confiance et la cible de D6.
Ici elles sont dans un **adapter jetable et remplaçable**, hors D6 et hors
S-G2 ; c'est exactement ce que la forme β « absorbe » (ADR-0015, alternative (c)).
Le fait est consigné pour que personne n'ait à le redécouvrir : le compagnon
n'est pas à dépendances minimales, et il n'a jamais eu à l'être.

---

## 4. Le constat licence

### 4.1 Le champ `license` de `tlsn-attestation`, au commit épinglé

**Toujours vrai au 2026-08-13.** Contrôle refait sur le clone au commit
épinglé, et pas seulement sur la copie détenue :

- `git show 0fe3c32d…:crates/attestation/Cargo.toml | sha256sum` rend
  `366c21831bd8376fa0996fbb1627be4578f49e4d3e555ff44b955a200b5687f3` ;
- `sha256sum biblio/tlsn-crate-attestation-cargo-toml-g0fe3c32d.toml` rend
  **la même chaîne** — la pièce détenue est l'octet exact du commit ;
- `git show 0fe3c32d…:crates/attestation/Cargo.toml | grep -c license` rend
  **0**.

Recensement des licences de la fermeture complète (`cargo metadata
--format-version 1`, 122 paquets hors racine) : **une seule** crate sans champ
`license` — `tlsn-attestation 0.1.0-alpha.16-pre`. Les autres se répartissent en
64 « MIT OR Apache-2.0 », 23 « Apache-2.0 OR MIT », 7 « MIT », 3 « MIT/Apache-2.0 »,
3 « Apache-2.0 OR ISC OR MIT », 3 « Apache-2.0 WITH LLVM-exception OR Apache-2.0
OR MIT », 2 « Apache-2.0/MIT », 2 « ISC », 2 « CDLA-Permissive-2.0 »,
2 « BSD-2-Clause OR Apache-2.0 OR MIT », et 11 valeurs à une occurrence.

### 4.2 Ce que `cargo deny` dirait du workspace du compagnon

Le compagnon est **hors du périmètre de `cargo-deny` du dépôt principal** : la
CI exécute `cargo deny --locked check` à la racine, sans `working-directory`
(`.github/workflows/squelette.yml`), et le workspace racine a 3 membres dont
aucun n'est ici. Le fait n'est donc pas « la gate est rouge » — la gate ne voit
rien. Mais un fait masqué n'est pas un fait absent : la mesure a été faite **à
la main**, `cargo-deny 0.20.2` (la version exacte de la CI), config
`F:\Shogen\deny.toml`, depuis `adapters/shogen-tlsn-verify`.

`cargo deny --locked --config …/deny.toml check` rend
**`advisories FAILED, bans FAILED, licenses FAILED, sources FAILED`**, avec le
décompte suivant par type (`grep -oE '^(error|warning)\[[a-z-]+\]' | sort | uniq -c`) :

| type | compte | ce que c'est |
|---|---|---|
| `warning[duplicate]` | 7 | versions multiples d'une même crate dans le graphe |
| `error[source-not-allowed]` | 4 | les 4 sources git ci-dessus, non listées à `[sources]` |
| `error[rejected]` | 3 | licences hors liste blanche (voir ci-dessous) |
| `error[unmaintained]` | 2 | `bincode` et `rustls-pemfile` |
| `error[wildcard]` | 1 | la dépendance git `tlsn-attestation` n'a pas de contrainte de version |
| `error[unlicensed]` | 1 | `tlsn-attestation` |
| `warning[unlicensed]`, `warning[no-license-field]`, `warning[license-not-encountered]` | 1 chacun | — |

Le détail des trois `error[rejected]` :

- `tiny-keccak` 2.0.2 — `license = "CC0-1.0"`, « rejected: license is not
  explicitly allowed », tirée par `tlsn-attestation` et `tlsn-core` ;
- `webpki-root-certs` 1.0.9 — `license = "CDLA-Permissive-2.0"`, même refus ;
- `webpki-roots` 1.0.9 — même licence, même refus.

Aucune de ces trois n'est restrictive au sens du copyleft : CC0-1.0 est une
renonciation, CDLA-Permissive-2.0 est permissive. Elles échouent parce qu'elles
ne sont **pas listées** à `[licenses] allow` de `deny.toml`, liste écrite pour
le graphe du dépôt principal. C'est un fait de configuration, pas un fait de
licence.

Les deux `error[unmaintained]`, **non anticipés par ADR-0015** :

- **`bincode` — RUSTSEC-2025-0141** : « Due to a doxxing and harassment
  incident, the bincode team has taken the decision to cease development
  permanently. » ;
- **`rustls-pemfile` 1.0.4 — RUSTSEC-2025-0134** : « The rustls-pemfile crate is
  no longer maintained. … Solution: No safe upgrade is available! », tirée par
  `tlsn-tls-core`, donc par l'amont et non par nous.

**Ce que cela implique — consigné, non tranché** (l'arbitrage appartient à
l'orchestrateur, et la question `bincode` est portée en demande de consultation
dans le rapport de passe) :

1. Élargir le périmètre de `cargo-deny` au workspace du compagnon rendrait la
   gate **rouge sur 4 familles**. Aucune de ces rougeurs ne porte sur du code
   Shōgen : elles portent sur l'amont épinglé et sur son arbre.
2. La clause `clarify` qu'ADR-0015 refusait d'écrire pour la forme α (« un
   affaiblissement de gate porté par ADR, pour un confort d'architecture »)
   n'est **pas** requise ici, puisque rien n'est à assouplir : le périmètre de la
   gate n'a simplement pas été étendu. Le prix est la **visibilité** — ce
   document est le contre-poids, et il est versionné avec le code qu'il mesure.
3. La position de repli existe et est mesurée : l'amont déclare son intention au
   README (« All crates in this repository are licensed under either of »
   Apache-2.0 ou MIT), mais `cargo deny` lit le manifeste, pas le README.
   L'écart est un fait de manifeste, pas une ambiguïté juridique à interpréter
   ici.

---

## 5. Contrôle registre R-8 des deux dépendances NOUVELLES

Les deux seules crates que **nous** déclarons (tout le reste vient de l'amont).
Contrôle fait le 2026-08-13 **avant** usage, API crates.io, valeurs copiées de
la réponse :

| crate | version retenue | licence | yanked | téléchargements de la version | propriétaires | premier versement |
|---|---|---|---|---|---|---|
| `bincode` | 1.3.3 (`"1.3"`, borne du workspace amont) | `MIT` | non | 226 662 970 | **`ghost_3672`** (compte fantôme au registre) | 2014-11-20 |
| `sha2` | 0.10.9 (`"0.10"`) | `MIT OR Apache-2.0` | non | 331 752 307 | `tarcieri`, `newpavlov`, `github:rustcrypto:hashes` | 2016-05-06 |

Deux observations qui n'étaient pas au dossier :

- **`sha2` n'ajoute AUCUN nœud à la fermeture.** `cargo tree -e normal -i sha2`
  montre 5 dépendants **autres** que nous — `k256`, `p256`, `rs_merkle`,
  `tlsn-core`, `tlsn-tls-core`. La crate était déjà là ; nous la nommons, nous
  ne l'introduisons pas.
- **`bincode` porte deux signaux concordants** : le propriétaire crates.io est
  un compte fantôme (`ghost_3672`) et l'advisory RUSTSEC-2025-0141 déclare
  l'arrêt définitif du développement. Le format est pourtant celui de l'amont
  (`bincode = { version = "1.3" }` au manifeste racine amont ; l'exemple
  officiel `attestation_verify` lit la présentation par `bincode::deserialize`) :
  en changer, c'est cesser d'être lisible par l'outillage du transport. Le choix
  est une décision de fond — il est porté en **demande de consultation** (R-26),
  pas tranché ici.

---

## 6. Durées constatées (2026-08-13, machine du mainteneur, 24 cœurs)

| geste | durée | commande |
|---|---|---|
| clone de l'amont (`--filter=blob:none`) | **2,649 s** | `time git clone --filter=blob:none https://github.com/tlsnotary/tlsn` |
| construction `--release` du **compagnon**, à froid | **25,45 s** (`real 0m25,816s`) | `time cargo build --release` |
| construction `--release` du **conducteur de session**, à froid (registre déjà chaud) | **55,25 s** (`real 0m55,516s`) | idem, dans `session/` |
| **la session MPC-TLS réelle**, de bout en bout | **`real 0m1,284s`** | `time shogen-tlsn-session shogen-s3-binance` |
| vérification d'une présentation par le compagnon | **`real 0m0,006s`** | `time shogen-tlsn-verify …presentation.tlsn` |

Taille du binaire compagnon `--release` (Linux) : **1 687 192 octets**.

---

## 7. Le compagnon sous Windows — mesure, là où ADR-0015 n'avait qu'une inquiétude

ADR-0015 rejetait la forme α en partie parce que « le workflow CI amont détenu
porte 8 jobs, tous `runs-on: ubuntu-latest`, zéro Windows, zéro macOS » alors
que le critère de clôture exige vert sur Windows **et** Linux. La question
restait ouverte pour la forme β. Elle est **mesurée** :

| geste, sur Windows 10, toolchain épinglée du dépôt (1.97.1) | résultat |
|---|---|
| `cargo build --locked --release` dans `adapters/shogen-tlsn-verify` | **succès**, code 0, `Finished 'release' profile … in 30.68s` (`real 0m30,831s`) |
| exécution du binaire sur la fixture produite sous Linux | code **0** ; constat **identique à l'octet près** à `fixtures/shogen-s3-binance.constat.json` (`diff` sans sortie) |
| fail-closed sur `mutant-1-octet-retourne.tlsn` | code **67**, même `detail` que sous Linux |

Trois conséquences, consignées sans arbitrage :

1. La fermeture du compagnon **construit sous Windows**, y compris `ring` et sa
   chaîne C — l'amont ne le teste jamais, mais la partie qu'on en tire tient.
2. Le constat est **stable entre plateformes**, ce qui est la propriété dont
   `shogen-verifier` dépendra : il compare des chaînes, pas des flottants ni des
   chemins.
3. Une CI qui voudrait garder cette propriété doit **l'exécuter**, pas la
   supposer. Rien n'est encore branché : ce répertoire n'entre dans aucun
   workflow au 2026-08-13.

---

## 8. Une corruption évitée avant le premier commit — les fixtures sont des octets

Mesure du 2026-08-13, faite **avant** tout `git add` : `git config
--show-origin core.autocrlf` rend `file:C:/Program Files/Git/etc/gitconfig
true` sur la machine du mainteneur. Or `fixtures/shogen-s3-binance.recv-revele.bin`
est du HTTP : **26** séquences CRLF, **0** LF isolé, 944 octets
(`sent-revele.bin` : **7** CRLF, 173 octets). Git aurait classé ces fichiers
comme du texte et retiré les CR au versement.

Ce que cela aurait coûté, chiffré : la fixture reçue serait passée de **944** à
**918** octets à tout clone frais, et son sha256 de
`c28a41ce87dafcd313d301ab56472b6f3cd1b3d81d903da787b0ca9dfffbeea0` à
`3ac95a33873d85fab5385164fb74688dd7cdf03d05e037cadb8138a9e8ac8761`. Le champ
`empreinte_recv_revele_sha256` du constat n'aurait plus lié aucun octet, et le
contrôle (b) d'ADR-0015 pt 8 serait devenu inopérant — silencieusement, chez
autrui, jamais sur la machine qui a produit les fichiers.

La parade est `adapters/shogen-tlsn-verify/.gitattributes` : `fixtures/** -text
-diff`. Contrôle fait : `git check-attr text diff -- fixtures/…` rend
`text: unset` et `diff: unset` sur la fixture reçue **et** sur la présentation.
La liaison hash d'ADR-0005 règle 1 porte sur « les octets exacts » ; un filtre
de fin de ligne est exactement ce qu'elle interdit.

La construction du compagnon est **deux fois plus rapide** que celle du
conducteur, et l'écart mesure la même chose que le compte de fermeture : la
vérification n'a pas besoin du protocole.
