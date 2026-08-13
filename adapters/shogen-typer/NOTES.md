# `shogen-typer` — note de l'adapter

> S3 phase C, chantier Y — écrit le 2026-08-13 par un worker sous orchestration.
> Rien ici n'est *proven*. Le régime est *tested (avec compte d'itérations)*, et
> le compte est au §5.

## 1. Rattachement (G0)

| ancre | ce qu'elle impose ici |
|---|---|
| **ADR-0001** | un typeur est un **adapter** : « testé et jamais prouvé » |
| **03 §3** | deux rangs jamais confondus : le dire brut d'un côté, l'extraction de l'autre ; « l'identité et la version [du typeur] figurent dans le *fait*, pas dans le témoignage » |
| **08, A(typer-correctness)** | « le typeur extrait du dire brut le fait annoncé (classe, valeur, unité) sans erreur de sens » ; cible S3 : *tested*, **avec compte d'itérations par typeur** ; l'assumption n'est **jamais déchargée** — elle est bornée par les tests et par l'identité du typeur dans le fait |
| **13 §2 pièce 4** | le typeur de la phase C ; « l'extraction reste hors témoignage » |
| **10 §3.1** | le pool S2 re-mesuré le 2026-08-05 — c'est de là que vient l'endpoint épinglé, et de là que viennent les fixtures |
| **ADR-0016** | `subject` en forme canonique construite ; prédicat total au cœur, employé ici |
| **ADR-0002 / RFC 8949 §3.4.4** | la forme décimale retenue (§3 ci-dessous) |
| **ADR-0018** | l'empreinte du dépôt est SHA-256, écrite au cœur, adossée aux vecteurs NIST — le typeur s'en sert pour son identité |

## 2. Ce que le typeur fait, et ce qu'il ne fait pas

**Il fait** un seul geste : `(subject, octets du dire) → fait prix typé`, pour
**un** endpoint — le ticker Coinbase Exchange BTC-USD, ligne 2 de la table de
10 §3.1. Il lit deux membres de l'objet **racine** du dire (`price`, `time`),
les type exactement, et rend un fait qui cite son propre typeur.

**Il ne fait pas** :

- **aucune I/O, aucun réseau, aucune horloge** — le dire lui est donné ; il ne
  date rien lui-même (03 §1 : l'instant enregistré est celui du transport,
  jamais celui de Shōgen) ;
- **aucun arrondi, aucune troncature, aucun repli** — ce qu'il ne type pas
  exactement, il le refuse avec la clause violée ;
- **aucun flottant binaire**, à aucun rang ; le contrôle est mécanisé
  (`tests/identite.rs::aucun_flottant_binaire_dans_les_sources`, lexical — il
  rejette des formes nommées, il n'établit pas l'absence dans le binaire, même
  limite que la gate S-G3 du dépôt) ;
- **aucune liaison au témoignage** — il ne calcule pas le hash d'`utterance` et
  ne contrôle aucune preuve de transport. Cette liaison appartient au cœur et au
  vérificateur (ADR-0005 règle 1, 03 §4) ; la dupliquer ici créerait un second
  endroit où elle pourrait être fausse ;
- **aucun jugement** — pas de champ vérité, pas de confiance, pas de qualité de
  source (03 §0). Et le fait n'est **pas signé** : 09-vocabulaire interdit « fait
  signé », « personne ne signe un fait ».

**Membres inconnus** : le typeur lit par **clé retournée** et ignore les autres
membres de la racine (le dire Coinbase en porte sept de plus). C'est la règle que
la re-mesure V2 a imposée au pool — 10 §3.1, notes : « position fixe, jamais
“dernier élément” ; clé retournée, jamais clé demandée ». Refuser un membre
inconnu ferait tomber le typeur au premier champ ajouté par la source, ce qui
serait une panne sans faute. Un membre **homonyme imbriqué** ne remonte jamais à
la racine (`tests/analyseur.rs::un_homonyme_imbrique_ne_remonte_pas`).

**Devise** : elle n'est pas dans le dire. Elle vient de l'endpoint
(`/products/BTC-USD/ticker`), donc du `subject` — c'est pourquoi le `subject`
est **épinglé** et contrôlé octet à octet. Le dossier S2 nomme déjà ce mode de
lecture au même endroit (10 §3.1, ligne DefiLlama : « USD **par convention
d'endpoint, non étiqueté dans le JSON** »).

## 3. La forme décimale retenue — et pourquoi celle-là

**Retenu** : deux entiers — une **mantisse** `i128` et un **exposant** de base
dix `i32`, la valeur étant `m · 10^e` — **plus le lexème verbatim** de la source,
conservé à côté.

**Ce qui la fonde, sur pièce** : RFC 8949 §3.4.4 (détenue depuis le 2026-08-13,
`biblio/rfc-8949-cbor-2026-08-13.txt`, sha256 à l'INDEX) donne exactement cette
forme au tag 4, dans la norme d'encodage qu'ADR-0002 a **déjà** adoptée pour tout
le dépôt, et dit pourquoi elle existe :

> « Decimal fractions combine an integer mantissa with a base-10 scaling factor.
> They are most useful if an application needs the exact representation of a
> decimal fraction such as 1.1 because there is no exact representation for many
> decimal fractions in binary floating-point representations. »

Le dépôt pratique déjà cette forme là où il décode du réel : Pyth
(`price · 10^expo`) et Chainlink (« 8 décimales ») en 10 §3.1.

**Écarté — l'option « décimal-chaîne validée » comme représentation *unique*** : une
chaîne ne se compare ni ne s'additionne sans être re-analysée à chaque usage, et
chaque re-analyse est une occasion de plus de se tromper. Elle n'est pas perdue :
le lexème voyage **à côté** de la forme typée (ADR-0003, recalculable offline).

**Écarté — le flottant binaire** : c'est l'objet même du chantier.

**Aucune normalisation d'échelle.** `64529.50000000` garde ses huit décimales :
l'échelle qu'une source écrit est une information de la source. Le contrôle est
la propriété (b) — la graphie **reconstruite** depuis (mantisse, exposant) doit
être l'octet pour octet du lexème.

**La grammaire admise** est plus étroite que le nombre JSON :

```text
decimale = [ "-" ] partie-entiere [ "." 1*chiffre ]
partie-entiere = "0" / ( chiffre-non-nul *chiffre )
```

Pas d'exposant, pas de `+`, pas de zéro de tête, pas de blanc, pas de zéro signé.
Chaque écart a sa variante de refus (`ErreurDecimale`). Une variante fait
exception et le dit à sa définition : `ExposantHorsCapacite` est une **borne
défensive inatteignable en pratique** — la capacité de la mantisse se ferme vers
39 chiffres, bien avant que le compte de décimales n'approche `i32::MAX`. Aucun
cas du corpus ne l'exerce ; elle existe pour qu'aucune conversion ne soit faite
sans issue nommée.

**Perte de précision** : l'accumulation de la mantisse est en arithmétique
**contrôlée** (`checked_mul` / `checked_add`). Un prix à quarante chiffres n'est
pas tronqué à trente-huit : il n'est **pas typé du tout**
(`CapaciteDeMantisseDepassee`).

## 4. L'instant — contrôlé, jamais converti

Forme admise : `date-time` de RFC 3339 §5.6 (détenue depuis le 2026-08-13,
`biblio/rfc-3339-datetime-2026-08-13.txt`), restreinte sur deux points, chacun
fondé :

1. **`T` et `Z` en majuscules seulement** — §5.6, NOTE : « Specifications that
   use this format in such environments MAY further limit the date/time syntax so
   that the letters 'T' and 'Z' used in the date/time syntax must always be upper
   case. » La permission est dans la pièce ; on l'exerce.
2. **Décalage `Z` seulement**. Accepter `+hh:mm` obligerait soit à conserver deux
   graphies pour un même instant (deux faits pour une observation), soit à
   convertir — c'est-à-dire réécrire la source.

Bornes de champ : §5.6 (commentaires de l'ABNF) et le tableau de §5.7, février
bissextile compris. La seconde `60` est admise **parce que la pièce l'admet**
(« 00-58, 00-59, 00-60 based on leap second rules »).

**Aucune conversion en époque, aucune troncature.** L'instrument jetable de S2
(`s2-harness/shogen_s2/sources.py`) tronque les neuf décimales de Coinbase à la
microseconde — son propre commentaire le dit : « Tolère 'Z' et une fraction à
précision variable (Coinbase émet des ns) en tronquant à la microseconde. »
Tolérable dans un instrument jetable ; interdit ici.

## 5. « Compte d'itérations » — instruction du terme, et le compte

Le registre 08 emploie le terme sans le définir sur place. Le dépôt en porte
**deux** gloses, et elles concordent :

- `docs/09-vocabulaire.md`, § « Héritées de la discipline » : « Les trois mots
  d'assurance — *proven / tested (avec compte d'itérations) / reviewed (qui,
  quand)* ». Le compte est donc l'**accompagnement obligatoire du mot `tested`**.
- `docs/10-mesures-pilotes-design.md` §8, entrée A(typer-correctness) : « Le
  rapport S2 publie le **compte d'exécutions de chaque décodeur** — première
  marche vers la cible de 08 (tested à S3, avec compte d'itérations). »

D'où la définition tenue, et rien de plus large : **le nombre d'exécutions du
typeur sur le corpus de la passe** — cas acceptés, cas de refus, cas générés.
Ce n'est ni un nombre de tests, ni un nombre d'assertions, ni une couverture.

**Le compte est mesuré, pas déclaré.** `src/identite.rs` porte la constante
`COMPTE_D_ITERATIONS` ; `tests/compte.rs` exécute le corpus en tenant un
compteur, imprime le total et **échoue** si le total mesuré diffère de la
constante. Un nombre écrit de tête ne survit pas à `cargo test`.

Mesure du 2026-08-13 (`cargo test --locked -- --nocapture`, sortie copiée) :

```
── compte d'itérations du typeur, mesuré ──
  cas acceptés (réels)      : 2
  cas de refus              : 51
  cas générés (3 propriétés × 1000) : 3000
  TOTAL MESURÉ              : 3053
  déclaré (identite::COMPTE_D_ITERATIONS) : 3053
```

Ce que le compte **n'est pas** : un total sur toute la suite. Les autres
binaires de test rejouent des sous-ensembles du même corpus ; ils n'ajoutent
aucun cas.

## 6. L'identité du typeur

Portée dans le fait, jamais dans le témoignage (03 §3) :

| champ | valeur |
|---|---|
| nom | `shogen-typer` (du manifeste, `env!("CARGO_PKG_NAME")`) |
| version | `0.1.0` (du manifeste, `env!("CARGO_PKG_VERSION")`) |
| empreinte de la logique | `f75d28ad6177744dd196a4024d0d5c5ab2585184217e44a88fa9233648ed5980` — mesurée le 2026-08-13 |
| compte d'itérations | `3053` — mesuré (§5) |

L'empreinte est un **SHA-256** (celui du cœur, ADR-0018) sur les sept fichiers de
`src/`, embarqués par `include_str!`, dans l'ordre trié des chemins, avec cadrage
explicite (chemin, longueur, contenu). Sans le champ de longueur, deux découpes
différentes des mêmes fichiers donneraient la même entrée.

**Une seule transformation dans tout le paquet** : les fins de ligne sont
ramenées à LF avant ce calcul. Le dépôt impose déjà `* text=auto eol=lf`
(`.gitattributes`), mais l'identité d'un typeur ne doit pas dépendre du système
de fichiers qui l'héberge. Elle ne porte que sur l'entrée du calcul d'empreinte —
jamais sur un dire, jamais sur un fait.

Deux contrôles la tiennent : `tests/identite.rs` relit les mêmes chemins **depuis
le disque** et recalcule (attrape une dérive entre compilation et dépôt) ; et un
second test exige que `FICHIERS_DE_LOGIQUE` couvre **tout** `src/*.rs` (sans quoi
un module nouveau échapperait à l'identité).

## 7. Décisions d'outillage

**Analyseur JSON écrit à la main, aucune dépendance nouvelle.** L'argument est
technique : `serde_json` type un nombre JSON non entier en `f64` hors de sa
fonctionnalité `arbitrary_precision` — le flottant binaire que ce typeur existe
pour empêcher. Le choix se réduisait à « une dépendance nouvelle **plus** une
fonctionnalité non par défaut » contre « un analyseur écrit ici, aux refus
nommés, qui rend les lexèmes verbatim ». Le dépôt a tranché deux fois dans ce
sens et pour la même raison (CBOR à la main, ADR-0002/0010 ; SHA-256 à la main,
ADR-0018) : le graphe de dépendances du produit est un observable.
Conséquence R-8 : **aucun contrôle registre n'était dû**, aucune dépendance
nouvelle n'entre. La seule dépendance directe est `shogen-core` (chemin), et la
seule de développement est `proptest =1.11.0` — même crate, même version exacte
que le cœur, contrôle R-8 déjà fait le 2026-08-12 en S2.5.

**Borne de profondeur (32)**. Un dire hostile profondément imbriqué ferait
diverger un analyseur récursif par la pile — une panique, donc un déni, pas un
refus. La borne transforme ce mode en refus nommé (`ProfondeurExcessive`).

**Clés dupliquées refusées, à tous les niveaux.** RFC 8259 §4 : « The names
within an object SHOULD be unique » et « When the names within an object are not
unique, the behavior of software that receives such an object is unpredictable.
Many implementations report the last name/value pair only. » Deux analyseurs
peuvent donc lire deux valeurs différentes du **même** dire, dont l'empreinte est
pourtant unique (ADR-0005 règle 1). Le typeur refuse plutôt que de choisir.

**Workspace autonome.** `adapters/` n'est pas membre du workspace racine (commenté
au `Cargo.toml` racine) : ce paquet porte sa propre table `[workspace]` et son
propre `Cargo.lock` (ADR-0012 D1). Mesure du 2026-08-13 : les membres du
workspace racine restent `['shogen-core', 'shogen-verifier', 'xtask']` et
`cargo tree -p shogen-verifier -e normal` rend **2 lignes** — la gate S-G2 ne
voit aucune arête nouvelle. L'arête `adapter → shogen-core` est le sens permis
(ADR-0010 point 3 ne contraint que le vérificateur).

## 8. Ce que la suite exerce (2026-08-13)

`cargo test --locked` — **28 tests, 0 échec**, répartis :

| binaire | tests | ce qu'il tient |
|---|---|---|
| `typage.rs` | 6 | les deux dires réels Coinbase typés champ par champ ; reconstruction à l'identique ; le fait cite son typeur ; le `subject` épinglé satisfait le prédicat du cœur ; impression du fait entier |
| `refus.rs` | 3 | les **51** cas de refus, chacun asserté sur **sa variante exacte** (jamais `is_err()`) ; stabilité au rejeu |
| `analyseur.rs` | 12 | les chemins que le dire Coinbase ne visite pas : échappements, paire de substituts UTF-16, lexèmes de nombres verbatim, blancs, homonyme imbriqué |
| `proprietes.rs` | 3 | (a) totalité sur octets quelconques ; (b) fidélité de la forme décimale ; (c) jamais d'altération silencieuse |
| `compte.rs` | 1 | le compte déclaré est celui qui est mesuré |
| `identite.rs` | 3 | empreinte embarquée = empreinte du disque ; `src/` entièrement couvert ; aucun flottant binaire dans le code |

Distributions imprimées avant verdict (patron ADR-0011 obligation 2), mesure du
2026-08-13 :

```
(a) totalité — cas : 1000, non vides : 991 (99.1 %), non UTF-8 : 977, acceptés : 0
(b) fidélité — cas : 1000, avec fraction : 944 (94.4 %), négatifs : 507
(c) altération — cas : 1000, refusés : 980 (98.0 %), acceptés : 20
cas de refus : 51 au total, dont 13 sur dire réel
```

Graine déterministe (`RngAlgorithm::ChaCha`), persistance de régression
désactivée : la même commande rejoue les mêmes cas, sur Windows comme sur Linux.

`cargo fmt --check` propre, `cargo clippy --locked --all-targets -- -D warnings`
propre. Le paquet est posé `forbid(unsafe_code)` et `deny` sur `unwrap_used`,
`expect_used`, `panic`, `indexing_slicing`, `arithmetic_side_effects` — la
discipline du cœur, reprise ici parce que c'est celle du dépôt, pas parce
qu'elle serait due à un adapter.

## 9. Ce qui reste hors de ce paquet

- **Un second typeur** (Binance, Kraken…) : chaque endpoint est un typeur, avec
  son `subject` épinglé et son compte propre. A(typer-correctness) demande le
  compte **par typeur**.
- **Le score de mutation** : ADR-0011 seuil 3 vise le **cœur** (« ≥ 80 % du
  cœur ») ; il n'est pas dû sur un adapter, et ne doit pas être annoncé comme
  s'il l'avait été.
- **L'encodage CBOR du fait** : la forme (mantisse, exposant) est celle du tag 4
  de RFC 8949, mais **aucun encodage n'est écrit ici** — le fait est un type
  Rust, pas encore un artefact. C'est le travail du cœur, quand un fait devra
  voyager (S4).
