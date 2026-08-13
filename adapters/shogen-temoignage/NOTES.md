# `shogen-temoignage` — le constructeur du témoignage réel

> Écrit le **2026-08-13**, passe S3 phase C **vague 2**, chantier V.
> Rattachement (G0) : **ADR-0001** (les transports sont des adapters — testés,
> jamais prouvés) ; **ADR-0016 C0/C10** (la normalisation a lieu une fois, à la
> construction, dans l'adapter ; le prédicat vit au cœur) ; **03 §1** (les sept
> champs) ; **ADR-0015 points 8 et 13** ; **13 §6 point 2** (un lot à un
> témoignage).

---

## 1. Ce que ce paquet est

Le **seul rang du dépôt qui sait ce qui a été interrogé**. Il lit les artefacts
déposés d'une session attestée réelle — octets émis, octets reçus, preuve de
transport, constat du binaire compagnon, ligne de clé de vérification — et en
fait les sept champs de la forme canonique.

Il ne conduit aucune session, n'ouvre aucune connexion, n'installe rien : il lit
des fichiers et en écrit un. La session, elle, a été conduite par le conducteur
du compagnon (`adapters/shogen-tlsn-verify/`, `fixtures/NOTES.md` §1).

**Zéro dépendance tierce.** Une seule arête, vers `shogen-core` par chemin — le
sens permis (l'arête interdite par S-G2 est `shogen-verifier -> adapters/*`).
R-8 n'a donc rien à instruire : il n'y a aucune installation. Aucun `deny.toml`
local n'est dû, exactement comme pour `shogen-typer`.

## 2. Les recoupements — pourquoi un constructeur qui ne recoupe rien est inutile

Le vérificateur contrôle des **liaisons** (ADR-0015 point 8). S'il les
contrôlait sur un lot que rien n'a jamais recoupé, le premier `verify` d'un lot
neuf serait aussi son premier contrôle, et un lot faux ne se distinguerait d'un
lot vrai qu'au moment de sa publication. Ce constructeur recoupe donc tout ce
qu'il assemble, et **refuse** au premier écart :

| recoupement | contre quoi | ce qu'il attrape |
|---|---|---|
| `subject` construit → `shogen_core::subject_est_canonique` | le **prédicat du cœur** (ADR-0016 C10) | un désaccord constructeur/prédicat — « un ROUGE : deux implémentations qui se contrôlent l'une l'autre » |
| hôte de `subject` → `server_name` | le constat | un lot qui désignerait une autre origine que celle authentifiée |
| `empreinte_sha256` des octets reçus / émis / de la preuve → les trois empreintes du constat | **deux implémentations de SHA-256** (celle du cœur, ADR-0018 ; celle du compagnon) | un octet de travers dans n'importe quel artefact ; un condensé faux d'un seul côté ne peut produire qu'un refus |
| longueurs lues → `transcript_*_longueur`, `octets_presentation` | le constat | un artefact tronqué ou rallongé, nommé plus tôt que par son empreinte |
| clé composée `<algorithme> <chiffres>` → la ligne déposée `…attestor-verifying-key.txt` | deux pièces du compagnon | une clé épinglée qui viendrait d'ailleurs que du contrôle conduit |
| `version_du_constat` = 1, `verdict` = succès | le contrat d'ADR-0015 point 13 | un constat d'une autre version, ou un constat de **refus** employé comme s'il validait |
| lot écrit → `decoder_lot` puis `encoder_lot` | le contrôle (a) | une forme qu'aucun décodeur ne reprend à l'octet près |

## 3. La convention d'épinglage de la clé

`attestor.key` porte les octets **US-ASCII** de `<algorithme> <chiffres
hexadécimaux>` — la ligne même que le compagnon dépose. Pour la session de S3 :
`k256 036aaecb…482271`, **71 octets**.

Trois raisons, écrites parce que la convention se porte aux deux bouts (ici, et
dans l'analyseur du vérificateur) :

1. ADR-0015 point 8 alinéa (f) demande « l'identité de la clé », pas ses seuls
   chiffres : sans l'algorithme, deux algorithmes distincts pourraient présenter
   les mêmes chiffres et l'épinglage ne dirait plus contre quoi le contrôle a
   été conduit ;
2. la forme est **lisible** : un refus d'épinglage se diagnostique à l'œil, sans
   outil, ce que des octets bruts n'offriraient pas ;
3. le cœur n'en sait rien et n'a pas à en savoir : il fait une **égalité
   d'octets** (ADR-0001 — il ne nomme aucun algorithme de transport).

## 4. Ce que l'adapter ne fait pas

- **Il ne trie pas la requête.** ADR-0016 C8 : la requête est reprise octet pour
  octet, dans l'ordre émis. Aucun tri, aucune déduplication, aucune fusion de
  clés répétées, aucune réécriture `+`/espace.
- **Il ne suit aucune redirection et ne résout aucun nom** (ADR-0016 R1/R2).
- **Il ne juge rien.** `residual` lui est **donné** ; il ne décide pas quels
  résidus un transport porte — c'est 03 §2 et le registre 08 qui le disent. Et
  `A(transport-check-delegated)` n'entre PAS dans le champ : le vérificateur
  l'ajoute au verdict (ADR-0015 point 8 alinéa e), et l'écrire ici le ferait
  nommer deux fois.
- **Il n'établit rien sur le contenu.** Ce qui a été dit reste un dire ; le
  passage au fait typé est le travail d'un typeur (03 §3, `shogen-typer`).

## 5. Rejouer

```
cd adapters/shogen-temoignage
cargo build --locked
./target/debug/shogen-temoignage \
    ../shogen-tlsn-verify/fixtures \
    shogen-s3-binance \
    ../../crates/shogen-verifier/tests/fixtures/s3-binance.lot.cbor
```

Le lot obtenu est celui du dépôt : 7399 octets, sha256
`8700d88f87253f0fd8496402601dc7326362a2cd9e6614a9bf44b79052f1e5a3`
(`crates/shogen-verifier/tests/fixtures/PROVENANCE.md`). La commande ne touche
pas le réseau.

## 6. Ce que le vert de ses tests dit, et rien de plus

*tested* sur ces cas, à la date (14 cas, 2026-08-13). ADR-0001 : un adapter est
« testé, jamais prouvé ». Rien ici n'établit que tout constructeur possible
produirait le même lot — l'oracle de cette question est le prédicat du cœur, et
il est appelé à chaque construction.
