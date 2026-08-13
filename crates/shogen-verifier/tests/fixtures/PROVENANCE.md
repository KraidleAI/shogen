# Fixtures du critère de sortie de S3 — le témoignage réel et son contexte

> Écrites le **2026-08-13**, passe S3 phase C **vague 2**, chantier V (le
> vérificateur consomme le constat réel).
> Rattachement (G0) : **13 §1** (le critère de sortie, à la lettre) ;
> **ADR-0015 points 8 et 13** ; **ADR-0005 règle 1** ; **ADR-0016** ;
> **03 §1** (les sept champs).
>
> Rien de ce répertoire n'est une pièce bibliographique : `biblio/` reste le
> registre des pièces détenues et ne reçoit rien d'ici.

---

## 1. Les trois fichiers, ce qu'ils sont, d'où ils viennent

| fichier | ce que c'est | d'où il vient (commande) | octets | sha256 (recalculé, copié de `sha256sum`) |
|---|---|---|---|---|
| `s3-binance.lot.cbor` | **le lot canonique réel** : un lot à un témoignage (13 §6 pt 2), sept champs de 03 §1, en CBOR déterministe | `shogen-temoignage adapters/shogen-tlsn-verify/fixtures shogen-s3-binance crates/shogen-verifier/tests/fixtures/s3-binance.lot.cbor` | 7399 | `8700d88f87253f0fd8496402601dc7326362a2cd9e6614a9bf44b79052f1e5a3` |
| `s3-binance.constat.json` | le **constat réel** du binaire compagnon sur la présentation de cette session — copie à l'octet près de `adapters/shogen-tlsn-verify/fixtures/shogen-s3-binance.constat.json` | `cp` (aucune retouche : le sha256 ci-contre est celui que `fixtures/NOTES.md` §1 porte déjà) | 875 | `7aba07cd8eb23ced38fee05195dfa57a9c30b981dae2faa293e977d076a05a25` |
| `s3-binance.registre.txt` | le **registre publié** des résidus, un identifiant par ligne | la commande complète du §1 bis ci-dessous (en-tête + extraction + tri) | 616 | `899898227e7ab1f75bb2f65caed636fa881d82cbd03fa053c7362b14e33e304d` |

Le registre porte **18** identifiants (compté à l'exécution : le vérificateur
imprime « registre publié : 18 identifiant(s) »). Il est *dérivé* de
`docs/08-assumptions.md`, jamais recopié à la main : le refaire est le contrôle.

### 1 bis. La commande de dérivation du registre, entière et rejouable

La rédaction précédente ne portait que l'extraction (`grep … | sort -u`) et
mentionnait « trois lignes de commentaire » sans les donner : elle ne
reproduisait pas les 616 octets, donc elle ne se rejouait pas (revue G2 de la
vague 2, mineure C6). La voici en entier — l'en-tête est dans la commande, et
`LC_ALL=C` fixe l'ordre du tri, qui dépend sinon de la locale de la machine
(ADR-0003 : recalculable **sur toute machine**). À exécuter depuis la racine du
dépôt :

```sh
{ cat <<'EOF'
# Registre publié des résidus — extrait de docs/08-assumptions.md le 2026-08-13.
# Un identifiant par ligne, « # » pour les commentaires : le format se relit à
# l'œil et se recalcule à la main depuis le registre (ADR-0003).
EOF
grep -o 'A([a-z0-9-]*)' docs/08-assumptions.md | LC_ALL=C sort -u
} > crates/shogen-verifier/tests/fixtures/s3-binance.registre.txt
```

Rejeu fait le 2026-08-13, sortie relevée : **616 octets**, sha256
`899898227e7ab1f75bb2f65caed636fa881d82cbd03fa053c7362b14e33e304d`, et `diff`
avec le fichier versionné **vide**.

## 2. La chaîne de provenance du lot, maillon par maillon

Le lot n'a pas été écrit : il a été **construit** par `adapters/shogen-temoignage`
depuis les artefacts de la session attestée réelle du 2026-08-13
(`adapters/shogen-tlsn-verify/fixtures/`, NOTES.md §1). Chaque champ vient d'un
octet déposé, et le constructeur refuse si un seul recoupement tombe :

| champ (03 §1) | d'où il vient | recoupement fait à la construction |
|---|---|---|
| `subject` | la **ligne de requête** et l'en-tête `host` de `shogen-s3-binance.sent-revele.bin` — `GET /api/v3/ticker/price?symbol=BTCUSDT HTTP/1.1`, `host: api.binance.com` | canonicalisé une fois (ADR-0016 C0 : scheme `https`, hôte en minuscules, port par défaut omis, requête **verbatim**), puis soumis à `shogen_core::subject_est_canonique` — un désaccord constructeur/prédicat serait un rouge (C10) |
| `attestor` | `shogen-s3-binance.attestor-verifying-key.txt`, ligne `k256 036aae…` | la ligne déposée est comparée à celle **composée** depuis `attestor_cle_algorithme` + `attestor_cle_hex` du constat : deux pièces, une seule clé (71 octets épinglés) |
| `residual` | 03 §2, ligne `tlsn-mpc` : `A(notary-neutrality)`, `A(self-attestation)` | tous deux résolvent au registre ; `A(transport-check-delegated)` n'est **pas** dans le champ — le vérificateur l'ajoute au verdict (ADR-0015 pt 8 e), et l'écrire ici le ferait nommer deux fois |
| `transport` | `tlsn-mpc/1` (ADR-0015 pt 1 — la valeur déjà écrite en 03 §2) | — |
| `utterance` | les **944 octets reçus** de `shogen-s3-binance.recv-revele.bin`, portés (`bytes`) et hachés (`hash`) | `empreinte_sha256` recalculée = `empreinte_recv_revele_sha256` du constat (`c28a41ce…`), et longueur = `transcript_recv_longueur` |
| `observed_at` | `connection_info_time` du constat = **1786594228**, horloge nommée `tlsn-mpc/1:connection_info.time` | c'est l'horloge du transport, jamais celle de Shōgen (03 §1) ; le contrôle (g) la recompare au constat |
| `transport_proof` | les **6034 octets** de `shogen-s3-binance.presentation.tlsn`, opaques | empreinte recalculée = `empreinte_presentation_sha256` (`47c38169…`), et longueur = `octets_presentation` |

**Les empreintes se recoupent entre deux implémentations indépendantes** : celles
du constat viennent de la crate `sha2` employée par le compagnon, celles du
constructeur de `shogen_core::empreinte` (ADR-0018, implémentation manuelle à
vecteurs NIST). C'est le geste déjà tenu au §3 de `fixtures/NOTES.md` — « la
seconde implémentation **est** le contrôle ».

## 3. Ces fichiers sont des octets, pas du texte — et le motif, re-mesuré

`crates/shogen-verifier/tests/fixtures/** -text` est posé au `.gitattributes`
racine. **Le motif écrit ici la première fois était empiriquement faux** (revue
G2 de la vague 2) : il annonçait que sans la règle, `autocrlf = true` amputerait
le lot de ses CR au versement. Trois régimes d'attributs ont été comparés le
2026-08-13 sur copies de travail, `git -c core.autocrlf=true`, tailles relevées
avant et après. Voici ce que la mesure donne.

| fichier | LF, tel que versé | sans aucun attribut, après checkout `autocrlf=true` | avec la seule règle racine `* text=auto eol=lf` | avec `text` FORCÉ (heuristique binaire mise en défaut) |
|---|---|---|---|---|
| `s3-binance.lot.cbor` | 7399 | **7399** (inchangé) | 7399 | **7340** — blob amputé au versement |
| `s3-binance.constat.json` | 875 | **876** | 875 | 875 |
| `s3-binance.registre.txt` | 616 | **637** | 616 | 616 |

Trois faits en découlent, et ils remplacent le motif d'origine :

1. **Le lot survivrait sans la règle.** Il porte 420 octets nuls dans ses 8000
   premiers : l'heuristique de Git le classe **binaire**, et ni `text=auto` ni
   `autocrlf` ne le touchent.
2. **Ce que `autocrlf` gonflerait au checkout, ce sont le constat et le
   registre** — du texte pur en LF, 875 → 876 et 616 → 637. Mais la règle
   racine `* text=auto eol=lf` porte `eol=lf`, et `eol=lf` neutralise déjà
   autocrlf au checkout : mesuré avec la seule règle racine, les trois fichiers
   ressortent inchangés.
3. **Ce que `-text` ferme réellement**, et c'est sa seule raison d'être ici :
   la dépendance à l'heuristique binaire. Contrefactuel mesuré, attribut `text`
   forcé sur le répertoire — le blob du lot tombe à **7340 octets** (59
   séquences CRLF dont le CR est retiré) et son empreinte devient
   `f0f6c3b8971a03e67239b1800f4988a543c1d400554ec19edd352cf5ed16b16f` au lieu de
   `8700d88f…`. L'empreinte du lot est ce que le vérificateur compare au constat
   (ADR-0005 règle 1, « les octets exacts ») : le critère de sortie de S3 serait
   faux pour quiconque clone. L'heuristique dépend du **contenu**, pas du
   chemin ; un lot futur sans octet nul de tête basculerait en « texte » sans
   qu'aucune ligne ne change ici. La règle ferme ce basculement.

`-diff` a été **retiré** (revue G2 de la vague 2, mineure C4) : il coûtait la
relecture de trois fichiers versionnés sans rien protéger — la conversion de
fins de ligne ne dépend que de `text`, jamais de `diff`. Le constat et le
registre se relisent donc en diff ; le lot reste illisible parce qu'il est
binaire, non parce qu'un attribut le déclare.

Contrôle refait après le retrait, sortie copiée de `git check-attr text diff` :

```
crates/shogen-verifier/tests/fixtures/s3-binance.lot.cbor: text: unset
crates/shogen-verifier/tests/fixtures/s3-binance.lot.cbor: diff: unspecified
crates/shogen-verifier/tests/fixtures/s3-binance.constat.json: text: unset
crates/shogen-verifier/tests/fixtures/s3-binance.constat.json: diff: unspecified
crates/shogen-verifier/tests/fixtures/s3-binance.registre.txt: text: unset
crates/shogen-verifier/tests/fixtures/s3-binance.registre.txt: diff: unspecified
crates/shogen-verifier/tests/fixtures/PROVENANCE.md: text: auto
crates/shogen-verifier/tests/fixtures/PROVENANCE.md: diff: unspecified
```

(`PROVENANCE.md`, lui, reste du texte : une ligne d'exception le remet au
régime racine.)

## 4. Ce que ces fixtures ne démontrent pas

Le notaire de cette session est **Shōgen lui-même**, et sa clé de signature
dérive d'une graine publique écrite en clair (ADR-0015 pt 16). Le verdict rendu
sur ce lot est donc littéralement vrai et pratiquement creux : il est
*démonstratif*, pas *probant* (ADR-0015, §Coûts pt 3). Ce que ces fixtures
établissent est **la chaîne et la forme de l'artefact** — pas la neutralité de
qui l'a signé, et ce que S3 ne démontre pas se dit dans la même phrase que ce
qu'il démontre.
