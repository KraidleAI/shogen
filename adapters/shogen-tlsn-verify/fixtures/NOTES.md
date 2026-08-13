# Fixtures du compagnon `shogen-tlsn-verify` — une session attestée réelle

> Écrites le **2026-08-13**, passe S3 phase C, chantier T (le transport réel).
> Rattachement (G0) : **ADR-0015** (le transport de S3 : TLSNotary en mode
> Notary, vérification déléguée à un binaire compagnon épinglé — points 2, 3, 4,
> 7, 8 et son amendement (f)/(g)) ; **ADR-0005 règle 1** (la liaison hash) ;
> **ADR-0001** (les transports sont des adapters — testés, jamais prouvés) ;
> **docs/03-temoignage.md §1-§2** ; **docs/13-temoignage-e2e-design.md §2** ;
> **docs/10-mesures-pilotes-design.md §3.1** (le pool de sources).
>
> Rien de ce répertoire n'est une pièce bibliographique : `biblio/` reste le
> registre des pièces détenues et ne reçoit rien d'ici.

---

## 1. Ce que ces fichiers sont, et d'où ils viennent

Une **session MPC-TLS réelle** a été conduite le 2026-08-13 depuis WSL2
(Ubuntu 26.04 LTS, noyau `6.18.33.2-microsoft-standard-WSL2 x86_64`) contre
`api.binance.com` — ligne 1 de la table `docs/10-mesures-pilotes-design.md`
§3.1, endpoint `api.binance.com/api/v3/ticker/price?symbol=BTCUSDT`, sans clé,
en lecture seule. Le rôle de Notary était joué **en bibliothèque, dans le même
processus local** (« Verifier acting as Attestor », Rust Quick Start amont) :
aucun service hébergé n'a été sollicité, conformément à ADR-0015 pt 3 (le
serveur notaire amont est déprécié depuis alpha.13).

Le choix de Linux d'abord et non de Windows est une conséquence de mesure, pas
une préférence : la CI amont détenue porte 8 jobs, tous `ubuntu-latest`
(ADR-0015, motif de rejet 5 de la forme α).

| fichier | ce que c'est | d'où il vient (commande) | sha256 (recalculé, copié de `sha256sum`) |
|---|---|---|---|
| `shogen-s3-binance.attestation.tlsn` | l'attestation signée par le notaire, sérialisée `bincode` | `shogen-tlsn-session shogen-s3-binance` (dépôt automatique) | `bb6c142b79240d83fb2d0f8f684c94b78af3befb98b3e610bcd5c0fd7231fcfd` |
| `shogen-s3-binance.presentation.tlsn` | la présentation vérifiable : preuve d'attestation + preuve d'identité de serveur + preuve de transcript révélant **la totalité** des deux sens | idem | `47c38169f7d79af924eb6e87969d94ab67838c1d6305cd69ef86ac1df9b18da5` |
| `shogen-s3-binance.attestor-verifying-key.txt` | la clé de vérification du notaire, `<algorithme> <hex>` — c'est elle que le champ `attestor` du témoignage épinglera | idem | `100060a4f9355dc80feb6cbe56ce32a8a84feff378bb82b6997865f4800e4c6d` |
| `shogen-s3-binance.constat.json` | le constat imprimé par le compagnon sur cette présentation | `shogen-tlsn-verify shogen-s3-binance.presentation.tlsn > shogen-s3-binance.constat.json` | `7aba07cd8eb23ced38fee05195dfa57a9c30b981dae2faa293e977d076a05a25` |
| `shogen-s3-binance.recv-revele.bin` | les **octets révélés reçus** — la réponse HTTP complète, en-têtes et corps | `shogen-tlsn-verify … --ecrire-recv shogen-s3-binance.recv-revele.bin` | `c28a41ce87dafcd313d301ab56472b6f3cd1b3d81d903da787b0ca9dfffbeea0` |
| `shogen-s3-binance.sent-revele.bin` | les **octets révélés envoyés** — la requête HTTP complète | `shogen-tlsn-verify … --ecrire-sent shogen-s3-binance.sent-revele.bin` | `4ad0e84b4f078e7ee62482ca86853c09e3c17bf074274168d65c024d1777e24b` |
| `mutant-1-octet-retourne.tlsn` | présentation avec **un** octet retourné au rang 3017 (milieu) | script Python à trois lignes, `b[len(b)//2] ^= 0x01` | `c923d430ec0c5ff0d8a46120479bede40159f89040a91a7eaf19441e4e7ed033` |
| `mutant-2-tronquee.tlsn` | présentation **tronquée** de ses 32 derniers octets | `b[:-32]` | `469c9b187036213e10d0645fd3c5a80f8ebba1a768c150cd2aefc720ba1e43de` |
| `mutant-3-dernier-octet.tlsn` | présentation avec le **dernier** octet retourné | `b[-1] ^= 0xff` | `a496cdb26391b0328fe54b6c0237dfa9c249c0588f9c2cd6e0b338f3bea20928` |
| `mutant-1-octet-retourne.constat.json` | le **refus** structuré du compagnon sur ce mutant | `shogen-tlsn-verify mutant-1-octet-retourne.tlsn 2> …` | `f1c2313981731bad12cf3ba2dc37bddfe649370ebef933a586ca41a35d12c9d0` |
| `mutant-2-tronquee.constat.json` | idem | idem | `d7c4448c92816720a35b778c9dcaf93683048b4f8930ce305af815cc842fd7e6` |
| `mutant-3-dernier-octet.constat.json` | idem | idem | `121cdc1ac4d2786a0987173e6805ef2ee3ef69ddc7cb54b709a460ed21d9ad26` |

Les trois mutants sont du registre **« octet muté du lot » (test négatif de
données)** de `docs/09-vocabulaire.md` — ni mutant de gate, ni mutant de
programme, et ils ne produisent aucun score.

**Ces fichiers sont des octets, pas du texte.** `recv-revele.bin` porte 26
séquences CRLF (c'est du HTTP) et la machine d'écriture a `core.autocrlf = true` :
sans `adapters/shogen-tlsn-verify/.gitattributes` (`fixtures/** -text -diff`),
tout clone frais recevrait 918 octets au lieu de 944 et un sha256 différent. Le
motif chiffré est en `../MESURE-R8.md` §8. Ne retirez pas ce fichier.

**Un mot sur le mot « vérifiée ».** Le constat porte
`"verdict":"presentation_verifiee"`. C'est licite au sens de
`docs/09-vocabulaire.md` — « vérifier une signature = calcul, licite ; donnée
vérifiée = surclamation, interdit » : la chaîne nomme le **calcul**
`Presentation::verify` qui a rendu `Ok`, et rien d'autre. Elle ne dit ni que la
donnée est vraie, ni que le notaire est neutre. Ce que le vérificateur Shōgen
en fera est écrit à ADR-0015 pt 8 (e), et cette phrase-là porte les résidus.

### Ce qui n'est PAS déposé, et pourquoi

`shogen-s3-binance.secrets.tlsn` (5 613 octets, produit par la même commande)
**reste hors du dépôt**. Il porte le transcript complet et le matériel
d'ouverture des engagements : quiconque le détient peut fabriquer d'autres
présentations depuis la même attestation. Il n'est nécessaire à aucune
vérification, et la vérification offline rejouable ci-dessous ne le touche pas.

---

## 2. La vérification offline rejouable

```
cd adapters/shogen-tlsn-verify
cargo build --release
./target/release/shogen-tlsn-verify fixtures/shogen-s3-binance.presentation.tlsn
```

**Rejouée sans réseau, mesure du 2026-08-13** : la même commande dans un espace
de noms réseau vide (`unshare -rn`) imprime un constat **identique à l'octet
près** et rend 0 ; dans le même espace de noms, `curl -m 5` vers
`https://api.binance.com/` rend le code HTTP `000` et sort en erreur 6 (hôte non
résolu). La vérification ne touche donc pas le réseau : elle est un recalcul sur
les octets déposés.

**Rejouée sous Windows, mesure du 2026-08-13** : le compagnon construit
(`cargo build --locked --release`, succès en 30,68 s, toolchain épinglée 1.97.1)
et imprime sur la fixture — produite sous Linux — un constat **identique à
l'octet près** (`diff` sans sortie), code de sortie 0 ; le mutant 1 est refusé
avec le même code 67 et le même `detail`. La plateforme que l'amont ne teste
jamais (8 jobs CI amont, tous `ubuntu-latest`) ne change pas le constat.

**Ces fixtures ne pourrissent pas à l'expiration du certificat de la source.**
Mesure sur la source amont au commit épinglé : `Presentation::verify` valide la
chaîne de certificats **à l'instant de la connexion**, pas à l'horloge murale —
`crates/attestation/src/presentation.rs` passe
`attestation.body.connection_info().time` à
`ServerIdentityProof::verify_with_provider`, qui le transmet tel quel à
`opening.data().verify(&provider.cert, time, …)`
(`crates/attestation/src/connection.rs:102`). Ce qui peut vieillir est
autre chose et se nomme : le magasin de racines est **compilé dans le binaire**
(`RootCertStore::mozilla()`, alimenté par `webpki-root-certs`) ; une racine
retirée d'une future version de ce magasin ferait échouer la vérification d'une
présentation ancienne. C'est une propriété du compagnon, pas de la fixture.

---

## 3. Le constat, champ par champ

```json
{"attestor_cle_algorithme":"k256","attestor_cle_hex":"036aaecb211badf2f35932adc21268bea583ad1a34b9e0f0f4781557cfe9482271","connection_info_time":1786594228,"connection_info_version_tls":"V1_2","empreinte_presentation_sha256":"47c38169f7d79af924eb6e87969d94ab67838c1d6305cd69ef86ac1df9b18da5","empreinte_recv_revele_sha256":"c28a41ce87dafcd313d301ab56472b6f3cd1b3d81d903da787b0ca9dfffbeea0","empreinte_sent_revele_sha256":"4ad0e84b4f078e7ee62482ca86853c09e3c17bf074274168d65c024d1777e24b","octets_presentation":6034,"revision_amont":"0fe3c32d35382b3f290a43c4156399ca4512bb89","server_name":"api.binance.com","transcript_recv_authentifie":944,"transcript_recv_longueur":944,"transcript_recv_longueur_attestee":944,"transcript_sent_authentifie":173,"transcript_sent_longueur":173,"transcript_sent_longueur_attestee":173,"verdict":"presentation_verifiee","version_du_constat":1}
```

| clé du constat | contrôle d'ADR-0015 pt 8 qu'elle sert | ce que le vérificateur en fera |
|---|---|---|
| `attestor_cle_algorithme`, `attestor_cle_hex` | **(f)** — l'identité de la clé contre laquelle la vérification cryptographique a été conduite | comparer au champ `attestor` du témoignage ; sans quoi l'épinglage de clé serait décoratif (amendement du 2026-08-13) |
| `connection_info_time` | **(g)** | comparer à `observed_at` |
| `empreinte_recv_revele_sha256` | **(b)** | comparer au hash d'`utterance` porté par le témoignage (ADR-0005 règle 1) |
| `empreinte_presentation_sha256` | **(c)** | comparer au hash des octets de `transport_proof` — c'est ce qui interdit qu'on vérifie une preuve et qu'on en livre une autre |
| `revision_amont` | **(e)** | entre verbatim dans la chaîne de verdict « … a été exécuté par shogen-tlsn-verify [révision amont] » |
| `server_name` | — | l'identité authentifiée du serveur ; se recoupe avec l'origine de `subject` (ADR-0016) |
| `transcript_recv_authentifie` = `transcript_recv_longueur` | pré-condition de (b) | si les deux diffèrent, le compagnon **refuse** au lieu de hacher un tampon à remplissage non authentifié |
| `transcript_sent_authentifie` = `transcript_sent_longueur` | même règle, sens envoyé (ADR-0015 pt 13 : le refus porte les six longueurs — garde symétrique ajoutée par la revue G2 vague 1) | idem : `empreinte_sent_revele_sha256` n'est jamais l'empreinte d'un tampon à remplissage |

**Contrôle croisé de l'empreinte, fait le 2026-08-13.** Les trois empreintes
imprimées par le compagnon (crate `sha2` 0.10.9) ont été recalculées par
`sha256sum` de GNU coreutils sur les fichiers déposés : **3/3 identiques**
(`47c38169…` pour la présentation, `c28a41ce…` pour les octets reçus,
`4ad0e84b…` pour les octets envoyés). Deux implémentations tierces, même
résultat.

**Pourquoi le compagnon n'emploie PAS `shogen_core::empreinte_sha256`.** Le
module `crates/shogen-core/src/empreinte.rs` fonde explicitement son
fail-closed sur l'indépendance des deux implémentations : « toutes les
comparaisons de `verification.rs` se font contre des empreintes calculées **hors
de cette crate** (le constat du binaire compagnon) : un condensé faux d'un seul
côté ne peut produire qu'un **refus** ». Faire path-dépendre le compagnon du
cœur détruirait cette propriété. La seconde implémentation **est** le contrôle.

---

## 4. Fail-closed — mesuré, pas seulement écrit

La règle de `docs/13-temoignage-e2e-design.md` §1 : *un vérificateur qui n'a
jamais rejeté n'a rien montré.* Cinq cas négatifs, exécutés le 2026-08-13 ;
chaque sortie est une ligne JSON structurée sur la sortie d'erreur, et le code
de sortie est distinct par famille de refus.

| cas | code de sortie | `erreur` | `detail` (copié de la sortie) |
|---|---|---|---|
| un octet retourné au milieu | **67** | `verification_refusee` | `presentation error: server identity error caused by: server identity proof error: commitment: certificate opening does not match commitment` |
| présentation tronquée de 32 octets | **66** | `presentation_indecodable` | `bincode : io error: unexpected end of file` |
| dernier octet retourné | **67** | `verification_refusee` | `presentation error: transcript error caused by: transcript proof error: hash error caused by: hash opening does not match any commitment` |
| fichier absent | **65** | `presentation_illisible` | `pas-de-fichier.tlsn : No such file or directory (os error 2)` |
| aucun argument | **64** | `presentation_absente` | la ligne d'usage |

Aucun de ces cas n'imprime de constat partiel : la sortie standard reste vide et
le code est non nul. C'est la lettre d'ADR-0015 pt 7.

---

## 5. La révision amont, et comment elle se contrôle

- Commit épinglé : **`0fe3c32d35382b3f290a43c4156399ca4512bb89`**, dépôt
  `github.com/tlsnotary/tlsn`, daté **2026-06-23 09:23:29 +0200**, message
  `fix(tlsn): do not write into a closed 'client_io' (#1172)` (mesuré par
  `git log -1 --format="%H %ci %s"` sur un clone du 2026-08-13).
- **Trouvaille** : ce commit est, au 2026-08-13, le **HEAD** de la branche par
  défaut de l'amont (`git ls-remote https://github.com/tlsnotary/tlsn` rend
  `0fe3c32d35382b3f290a43c4156399ca4512bb89 HEAD`). Le corpus S3 est donc à
  jour de l'amont, et le suffixe `-g0fe3c32d` des pièces du pack T3 de
  `biblio/INDEX.md` désigne bien cet état.
- Le contrôle de cohérence est mécanique en trois points, qui doivent porter la
  même chaîne : la constante `REVISION_AMONT` de `src/main.rs`, la clé `rev` du
  manifeste, et les entrées `source = "git+…"` du `Cargo.lock`
  (`grep 'source = "git+' Cargo.lock` : **4** entrées, dont 3 sur ce commit).
- **Trouvaille** : `prove.rs` (la notarisation) **n'est pas au corpus** —
  `biblio/` détient `present.rs` et `verify.rs` épinglés, pas `prove.rs`. Le
  conducteur de session `session/src/main.rs` est donc écrit d'après le clone au
  commit épinglé, et non d'après une pièce détenue. C'est un fait à consigner,
  pas un contournement : la pièce manquante est nommée.

---

## 6. Ce que ces fixtures ne démontrent pas

Le notaire est **Shōgen lui-même** : c'est A(self-attestation) (ADR-0015 pt 4,
registre 08). Sa clé de signature est de surcroît **dérivée d'une graine
publique écrite en clair** dans `session/src/main.rs` — quiconque lit ce code
peut signer une attestation qui passera la vérification. Ce n'est pas un défaut
à corriger dans cette passe : c'est le résidu à afficher. S3 démontre la chaîne
et la forme de l'artefact, pas la neutralité — et ce que S3 ne démontre pas se
dit dans la même phrase que ce qu'il démontre.

S'y ajoutent A(notary-neutrality), A(transport-check-delegated) et
A(upstream-alpha) (ADR-0015 pt 9). L'amont écrit de lui-même qu'il « should not
be used in production ».
