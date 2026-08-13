# Dossier d'instruction — licence du dépôt (échéance ADR-0014, S3)

> **CLOS le 2026-08-13 — la décision est prise : ADR-0017, « MIT OR
> Apache-2.0 » uniforme sur le workspace**, décidée par l'orchestrateur sur
> délégation explicite du mainteneur (« tranche… de façon définitive »),
> adjugée sur ce dossier. Q1 tranchée en son troisième terme (le moat est
> la neutralité) ; Q2 oui (brevets voulus pour eux-mêmes) ; Q3 sans objet
> ((c) rejetée) ; Q4-Q5 sans objet ((b) rejetée) ; Q6 non nécessaires ;
> Q7 : champ posé d'avance, opposabilité au passage public. Ce dossier
> reste la pièce d'instruction de la décision.

> **Ce document ne tranche pas.** ADR-0014 pt 1 nomme le propriétaire de la
> décision : « Propriétaire : le mainteneur. » Ce dossier instruit les trois
> options pré-cadrées sur les pièces détenues, chiffre leurs conséquences, et
> se termine (§13) par les questions exactes que le mainteneur doit trancher.
> Il n'exprime aucune préférence de rédacteur.
>
> **Régime de preuve.** Chaque énoncé sur ce que dit une licence porte sa
> citation verbatim, greppable dans une pièce détenue de `biblio/` (une
> citation = un grep ; chaque citation de ce dossier a été greppée sur la
> copie détenue avant écriture). Les énoncés qui ne sont pas des citations
> sont marqués **[raisonnement]** (déduction sur texte détenu) ou
> **[non détenu]** (manque nommé, §11). Aucun chiffre de seconde main.
>
> **Avertissement de portée, énoncé une fois et valable partout.** Les pièces
> détenues sont des **textes de licence** et des **conventions d'écosystème**.
> Aucune n'est une analyse juridique, une jurisprudence, ni un avis d'avocat.
> Ce dossier lit ce que les textes disent ; il ne qualifie pas juridiquement
> des situations que les textes ne qualifient pas eux-mêmes (§11, manques
> M1–M4). Rédacteur : worker `claude-opus-5[1m]`, passe S3, 2026-08-12.

---

## 1. Le cadre contracté — ce que ce dossier doit servir

**ADR-0014, pt 1** (citations aux lignes du fichier, fragments d'une ligne
chacun) : « Le choix de licence est une décision d'entrée de S3 », au
déclencheur « nommé : le passage public du dépôt (DEVOPS §1, §7 pt 6) » ;
les options sont « cadrée d'avance — options à instruire : « MIT OR » /
« Apache-2.0 » (la convention de l'écosystème Rust, permissive, avec la » /
« concession de brevets d'Apache-2.0) ; AGPL-3.0 (protectrice) ; licences » /
« le vérificateur au régime le plus ouvert » / « (c'est l'artefact de
confiance). Propriétaire : le mainteneur. » / « Échéance : l'événement S3,
pas une date. »

**La borne de vision, non rouvrable ici — DEVOPS §1** : « l'artefact de
confiance du projet est le » vérificateur, « (« vérifiable offline sans
confiance dans Shōgen ») — un vérificateur » / « fermé contredit la vision,
donc le passage en public est calé sur son » / « existence (S3), pas sur un
calendrier marketing. »

**Conséquence de cadrage [raisonnement].** Aucune des trois options n'est un
vérificateur fermé : MIT, Apache-2.0 et AGPL-3.0 sont toutes des licences qui
publient la source. La borne de vision n'élimine donc **aucune** des trois ;
elle élimine une quatrième option (propriétaire / source fermée) qu'ADR-0014
n'a d'ailleurs pas cadrée. Ce que la vision **ne** dit **pas** : elle ne dit
pas *quelles obligations* le tiers reprend. C'est exactement l'espace où les
trois options diffèrent, et l'objet de ce dossier.

---

## 2. L'état de fait de notre dépôt — constaté sur octets, aujourd'hui

Ces faits sont lus dans le dépôt lui-même (pas dans `biblio/`) ; ils sont
vérifiables par relecture des fichiers nommés.

*Convention de renvoi, valable dans tout le dossier* : « §n » seul renvoie à
une section **de ce document** ; à l'intérieur des lectures de licence (§4) et
des tables Q1–Q3, « §n » renvoie à la section **de la licence lue**, nommée
juste avant (Apache-2.0 §3, AGPL-3.0 §13, etc.).

| fait | pièce | conséquence pour la décision |
|---|---|---|
| Les trois crates n'ont **aucun** champ `license` | `crates/shogen-core/Cargo.toml`, `crates/shogen-verifier/Cargo.toml`, `xtask/Cargo.toml` | la décision se matérialise par une écriture de manifeste (§10) |
| `publish = false` au niveau workspace | `Cargo.toml`, `[workspace.package]` | aucune crate n'est publiable ; c'est ce qui rend la gate silencieuse aujourd'hui |
| `private = { ignore = true }` | `deny.toml`, `[licenses]` | le re-serrage d'ADR-0014 pt 3 : « Rendre une crate publiable sans licence remet la gate au » / « rouge d'elle-même » |
| Liste `allow` de la gate : `Apache-2.0`, `MIT`, `BSD-2-Clause`, `BSD-3-Clause`, `ISC`, `Unicode-3.0`, `Zlib` | `deny.toml` | **`AGPL-3.0` n'y figure pas** — l'option (b) exige d'amender la liste (§7.3 et §10.3 pt 4) |
| `include-dev = true` | `deny.toml` | les dépendances de développement sont contrôlées aussi |
| **Zéro dépendance directe hors dev** sur le cœur et le vérificateur | `crates/shogen-core/Cargo.toml` (« ZÉRO dépendance directe hors dev »), `crates/shogen-verifier/Cargo.toml` | aujourd'hui aucune licence amont ne contraint quoi que ce soit — la contrainte n'arrive qu'avec ADR-0015 (§9) |
| L'arête `shogen-verifier → shogen-core` existe et est **obligatoire** | `crates/shogen-verifier/Cargo.toml` ; ADR-0010 pt 3 : « `shogen-verifier -> shogen-core`, et rien d'autre » | **contrainte dure sur l'option (c)** — voir §8.2 |
| Seule dépendance de dev du cœur : `proptest = "=1.11.0"` | `crates/shogen-core/Cargo.toml` | non redistribuée dans le binaire ; contrôlée quand même (`include-dev`) |

---

## 3. Les pièces détenues qui instruisent, et ce qu'elles sont

| pièce (`biblio/`) | ce que c'est | sha256 (INDEX §S3) |
|---|---|---|
| `apache-license-2.0-2026-08-12.txt` | texte canonique Apache-2.0, apache.org | `cfc7749b…c523d30` |
| `osi-mit-license-2026-08-12.html` | The MIT License, page canonique OSI | `4ce24f62…f628f861` |
| `gnu-agpl-3.0-2026-08-12.txt` | texte intégral AGPL-3.0, gnu.org (661 lignes) | `0d96a4ff…79abcb0` |
| `rust-lang-rust-copyright-2026-08-12.txt` | COPYRIGHT de rust-lang/rust | `172020db…82c4af` |
| `rust-lang-rust-readme-2026-08-12.md` | README de rust-lang/rust, section licence | `b3f6ef2f…17f33c8` |
| `rust-api-guidelines-necessities-2026-08-12.html` | Rust API Guidelines, C-PERMISSIVE | `1e0a7911…c814649a` |
| `cargo-reference-manifest-2026-08-12.html` | The Cargo Book, « The Manifest Format » | `3e02b4c9…7cd0cb57` |
| `tlsn-repo-readme-raw-2026-08-12.md` | README brut de tlsnotary/tlsn | `b95e34f3…296ff657` |
| `tlsn-repo-metadata-api-2026-08-12.json` | métadonnées GitHub API du dépôt amont | `4717e7aa…029768e4` |
| `tlsn-repo-root-contents-api-2026-08-12.json` | inventaire API de la racine du dépôt amont | `d81800c0…980ba6e5` |
| `tlsn-repo-workspace-cargo-toml-2026-08-12.toml` + 8 manifestes de crates `tlsn*` | manifestes amont | voir INDEX §S3, pack T2 |

---

## 4. Ce que chaque texte dit — lecture verbatim

### 4.1 MIT

**La concession** : « Permission is hereby granted, free of charge, to any
person obtaining a copy of this software and associated documentation files »
… « to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions: »

**La seule condition** : « The above copyright notice and this permission
notice shall be included in all copies or substantial portions of the
Software. »

**Ce que le texte ne contient pas — mesure faite sur la copie détenue** :
`grep -c -i patent osi-mit-license-2026-08-12.html` → **0 occurrence**. Le
texte MIT ne mentionne le brevet ni pour l'accorder, ni pour le refuser.
[raisonnement] Ce silence est la différence structurante avec Apache-2.0
(§4.2) ; ce que ce silence produit juridiquement n'est pas dit par la pièce
(manque M1, §11).

### 4.2 Apache-2.0

**La concession de brevets — §3, le motif nommé par ADR-0014** :
« 3. Grant of Patent License. Subject to the terms and conditions of » … « (except as
stated in this section) patent license to make, have made, » « use, offer to
sell, sell, import, and otherwise transfer the Work, ».

**Sa résiliation, dans la même section** : « institute patent litigation
against any entity (including a » … « granted to You under this License for
that Work shall terminate » — c'est-à-dire que l'agression en brevet contre
l'Œuvre coûte au demandeur la licence de brevet qu'il tenait d'elle.

**La frontière de l'Œuvre dérivée, écrite dans le texte lui-même — §1** :
« of this License, Derivative Works shall not include works that remain » …
« separable from, or merely link (or bind by name) to the interfaces of, ».
[raisonnement] Apache-2.0 **exclut explicitement le lien d'interface** de sa
définition d'œuvre dérivée. Aucune clause équivalente n'existe dans le texte
AGPL détenu — c'est l'asymétrie centrale du §5 (question Q2, embarquement
dans un produit fermé).

**Les charges de redistribution — §4** : « (a) You must give any other
recipients of the Work or » « Derivative Works a copy of this License; and » ;
« (b) You must cause any modified files to carry prominent notices » « stating
that You changed the files; and » ; et l'obligation NOTICE : « (d) If the Work
includes a "NOTICE" text file as part of its ».

**Le silence sur les marques — §6** : « 6. Trademarks. This License does not
grant permission to use the trade ». [raisonnement] La licence ne cède donc
pas le nom « Shōgen » ; le nom reste un levier distinct de la licence, dans
les trois options.

### 4.3 AGPL-3.0

**La clause réseau — §13, la raison d'être de l'option (b)** :
« 13. Remote Network Interaction; Use with the GNU General Public License. » —
« Notwithstanding any other provision of this License, if you modify the »
« Program, your modified version must prominently offer all users »
« interacting with it remotely through a computer network (if your version »
« supports such interaction) an opportunity to receive the Corresponding »
« Source of your version by providing access to the Corresponding Source »
« from a network server at no charge, through some standard or customary »
means of facilitating copying of software.

**Le déclencheur exact, à lire à la lettre** [raisonnement sur le texte
ci-dessus] : la clause se déclenche sur **« if you modify the »** « Program, »,
pas sur le seul fait d'offrir le service. Le texte le confirme en sens
inverse au §2 : « This License explicitly affirms your unlimited »
/ « permission to run the unmodified Program. » — **exécuter le
Programme non modifié est explicitement permis, sans condition.** Un
concurrent qui hébergerait Shōgen **tel quel** en service payant n'est donc
pas atteint par le §13. La protection porte sur les *modifications* offertes
à distance, pas sur l'exploitation commerciale.

**Le copyleft de combinaison — §5(c)** : « c) You must license the entire
work, as a whole, under this » « License to anyone who comes into possession
of a copy. »  Et sa borne, dans la même section : « in an aggregate does not
cause this License to apply to the other » « parts of the aggregate. »
[raisonnement] Le texte distingue donc l'*œuvre combinée* (§5c : la licence
s'étend au tout) de l'*agrégat* (§5 fin : elle ne s'étend pas). Où tombe un
binaire Rust liant statiquement une crate AGPL n'est pas tranché par le texte
détenu — manque M2 (§11). C'est la question dont dépend la réponse Q2 de
l'option (b), et elle n'est pas instruite ici.

**L'étendue de la source à livrer** : « the source code needed to generate,
install, and (for an executable » work) run the object code and to modify the
work — la « Corresponding Source » n'est pas le seul fichier modifié.

**Compatibilité Apache-2.0** : `grep -c -i apache gnu-agpl-3.0-2026-08-12.txt`
→ **0 occurrence**. Le texte AGPL détenu **ne dit rien** d'Apache-2.0. La
compatibilité de sens unique Apache-2.0 → GPLv3/AGPLv3 est un énoncé courant
de l'écosystème, mais **[non détenu]** : manque M3 (§11). Elle n'est ni
affirmée ni niée dans ce dossier.

---

## 5. Les trois questions du mainteneur, posées à chaque texte

Les trois questions du mandat, littéralement : un tiers peut-il **(Q1)**
reconstruire le vérificateur, **(Q2)** l'embarquer dans un produit fermé,
**(Q3)** offrir Shōgen en service sans publier ses modifications ?

| | **Q1 — reconstruire le vérificateur** | **Q2 — embarquer dans un produit fermé** | **Q3 — offrir en service sans publier ses modifications** |
|---|---|---|---|
| **MIT** | Oui. « the rights to use, copy, modify » ; seule charge : « The above copyright notice and this permission notice shall be included in all copies ». | Oui. Rien dans le texte n'oblige à publier la source d'un dérivé ; la charge est l'avis de copyright. | Oui. Le texte n'a **aucune** clause réseau. |
| **Apache-2.0** | Oui. §2 concède « reproduce, prepare Derivative Works of » ; charges §4(a)(b)(d). | Oui — et le texte va plus loin : le lien d'interface est **hors** œuvre dérivée (« shall not include works that remain » « separable from, or merely link (or bind by name) to the interfaces of, »). | Oui. Aucune clause réseau. |
| **AGPL-3.0** | Oui. Le copyleft n'empêche pas la reconstruction ; il l'**impose** en aval (§5c). | **Non, si combinaison** : « You must license the entire work, as a whole, under this » « License ». **Oui, si agrégat** : « in an aggregate does not cause this License to apply to the other » « parts of the aggregate ». La frontière n'est pas tranchée par le texte détenu — **manque M2**. | **Non pour les modifications** (§13 : « if you modify the » « Program, your modified version must prominently offer all users » …). **Oui pour l'inchangé** (§2 : « permission to run the unmodified Program »). |

**Lecture croisée [raisonnement].** Sur Q1 — la question que la vision
DEVOPS §1 rend non négociable — **les trois options répondent identiquement
oui.** Le choix de licence n'est donc *pas* le levier de l'ouverture du
vérificateur : l'ouverture est acquise dans les trois cas. Les options ne se
séparent que sur Q2 et Q3, c'est-à-dire sur ce que le **tiers** doit rendre,
jamais sur ce que **nous** publions.

---

## 6. Option (a) — « MIT OR Apache-2.0 »

### 6.1 Ce que la convention détenue en dit

**Rust lui-même** — `rust-lang/rust` COPYRIGHT : « The Rust Project is
dual-licensed under Apache 2.0 and MIT » terms ; et « 2.0 <LICENSE-APACHE> or
<http://www.apache.org/licenses/LICENSE-2.0> or the MIT » « license
<LICENSE-MIT> or <http://opensource.org/licenses/MIT>, at your option. »
README : « Rust is primarily distributed under the terms of both the MIT
license and the » Apache License (Version 2.0).

**La ligne directrice de l'écosystème** — Rust API Guidelines, **C-PERMISSIVE**
(« Crate and its dependencies have a permissive license ») : « The software
produced by the Rust project is dual-licensed, under either the » MIT or
Apache 2.0 « licenses. Crates that simply need the maximum » « compatibility
with the Rust ecosystem are recommended to do the same, in the » manner
described herein.

**L'avertissement que la même page porte, et qui est un fait utile** :
« Crates that desire perfect license compatibility with Rust are not
recommended » « to choose only the Apache license. » [raisonnement] Ceci
instruit contre un *Apache-2.0 seul* — option non cadrée par ADR-0014, mais
qu'on aurait pu croire équivalente à (a). Elle ne l'est pas selon la pièce.

**La règle de propagation, qui sera décisive en §8** : « The license of a
crate's dependencies can affect the restrictions on » « distribution of the
crate itself, so a permissively-licensed crate should » « generally only
depend on permissively-licensed crates. »

### 6.2 Ce que l'option achète, et à qui

- **Le tiers reconstruit le vérificateur** (Q1) sous la charge la plus légère
  qui existe : un avis de copyright conservé. C'est le régime qui met le moins
  d'obstacles entre la promesse d'ADR-0003 (« recalculable offline ») et son
  exercice réel.
- **La concession de brevets d'Apache-2.0 protège dans les deux sens**
  [raisonnement sur §3 détenu] : elle donne au tiers une licence de brevet
  explicite (ce que MIT seul ne fait pas — 0 occurrence de « patent »), et
  elle retire cette licence à qui nous attaque en brevet (« granted to You
  under this License for that Work shall terminate »). Pour un projet dont le
  cœur est un **appareil de mesure** (k_eff, axes R1/R2), c'est la clause
  d'ADR-0014 qui a le plus de contenu.
- **Le `OR` est un droit du destinataire, pas une ambiguïté** — Cargo Book
  (les balises `<code>` de la copie coupent la phrase ; fragments greppables) :
  « indicates the user may choose either license. Using » … « indicates » /
  « the user must comply with both licenses simultaneously. »

### 6.3 Ce que l'option coûte

- **Un concurrent peut prendre le vérificateur, le modifier, et ne rien
  rendre** (Q2 et Q3 = oui). Concrètement, un oracle installé peut embarquer
  `shogen-verifier` dans un produit fermé et le présenter comme son propre vérificateur.
- **Ce coût est-il un coût pour Shōgen ?** GTM §4 pt 2 répond, et sa réponse
  ne mentionne pas la licence : « un certificat vendu par le mesuré ne vaut rien ; »
  / « un tiers vérifiable offline, si. C'est le moat structurel — un oracle » /
  « qui voudrait « faire son propre Shōgen » produirait un bulletin » /
  « d'auto-notation. » [raisonnement] Le moat que le GTM revendique est la
  **neutralité du tiers mesureur**, pas l'exclusivité du code. Un fork du
  vérificateur exécuté par le mesuré lui-même retombe dans l'auto-notation que
  le GTM désigne comme sans valeur. Même structure au §6 pt 2, sur le
  cabinet de risque qui internaliserait la métrique : « parade : notre » /
  « instrument est publié et vérifiable, le leur serait un dire d'expert ; ».
  La parade nommée est la **publication**, jamais la restriction.
- **Ce que l'option ne protège pas et qu'aucun texte de licence ne protège** :
  le nom. Apache-2.0 §6 : « This License does not grant permission to use the
  trade » names — la marque reste hors licence, dans les trois options.

---

## 7. Option (b) — AGPL-3.0

### 7.1 Ce que l'option achète

- **Contre le fork fermé embarqué** (Q2) : §5(c) — « You must license the
  entire work, as a whole, under this » « License to anyone who comes into
  possession of a copy » — **sous réserve M2** (combinaison vs agrégat).
- **Contre le SaaS qui améliore sans rendre** (Q3, cas modifié) : §13.

### 7.2 Ce que l'option n'achète pas — trois limites lues au texte

1. **Elle n'empêche pas le service concurrent non modifié.** §2 : « permission
   to run the unmodified Program. » Un concurrent qui offre Shōgen tel quel en
   service payant est en règle. [raisonnement] Si la crainte du mainteneur est
   *quelqu'un vend mon travail*, l'AGPL ne la couvre qu'au cas *modifié*.
2. **Elle ne protège pas le certificat vendu.** Le produit payant nommé par
   GTM §5 est « le monitoring continu par feed avec alertes (dégradation de » /
   « k_eff, apparition d'un amont commun) ; les certificats à la demande sur » /
   « cas challenger) ; l'API d'intégration dans les rapports tiers. ». [raisonnement] Ce sont des
   **services** et des **données produites**, pas la distribution du
   vérificateur ; l'AGPL porte sur le code et sa source correspondante, et §2
   précise que « The output from running a » / « covered work is covered by this
   License only if the output, given its » / « content, constitutes a covered work. »
3. **Elle se retourne contre notre propre offre payante.** [raisonnement,
   conséquence directe du §13] Le service payant de GTM §5 fera nécessairement
   tourner du code Shōgen ; si ce code est une version **modifiée** de nos
   propres crates AGPL, le §13 nous oblige nous-mêmes à en offrir la
   Corresponding Source aux utilisateurs distants. La sortie usuelle est la
   double licence (nous détenons le copyright), qui **exige un accord de
   contribution** dès le premier contributeur externe — **[non détenu]**,
   manque M4 (§11).

### 7.3 Ce que l'option coûte, en mécanique et en adoption

- **Elle casse la gate telle qu'écrite.** `deny.toml` `allow` ne contient pas
  `AGPL-3.0`. [raisonnement] Rendre une crate AGPL publiable met la gate au
  rouge ; amender la liste est une **modification de gate**, donc une ADR
  (ADR-0014 pt 2 rappelle la règle : « charte
  `shogen-devops` §2 : jamais » / « d'affaiblissement sans ADR »).
- **Elle contredit la ligne directrice détenue de l'écosystème** : C-PERMISSIVE
  « Crates that simply need the maximum » « compatibility with the Rust
  ecosystem are recommended to do the same » — « the same » étant le dual
  MIT/Apache. Ce n'est pas un interdit, c'est une recommandation datée et
  citable ; l'écart se paie en adoption, non en illégalité.
- **Elle contamine en aval par construction.** Même page : « a
  permissively-licensed crate should » « generally only depend on
  permissively-licensed crates. » [raisonnement] Un consommateur permissif ne
  pourra pas dépendre de nos crates AGPL sans traiter la question §5(c). Or le
  **canal transverse** du GTM (§3 : « le client commun avec Kraidle », dont
  l'objet est « L'opérateur d'agents de trading, dès S3-S4 ») et le
  **canal 1** (dont l'offre est le k_eff « rapports, sous leur marque, notre
  certificat en preuve. ») supposent tous deux une **intégration dans le
  produit d'un tiers**.
  C'est le point de friction le plus concret de l'option (b) : elle protège
  contre le concurrent et gêne le client.
- **Le résidu qu'elle n'atteint pas** : `A(verifier-binary)` (08) —
  « Le binaire `shogen-verifier` qu'un tiers exécute correspond au code source
  publié ». Aucune licence ne décharge ce résidu ; sa décharge est le rebuild
  bit-à-bit (ADR-0012 D6). [raisonnement] Il faut le dire parce que la
  tentation existe de croire qu'une licence copyleft établirait quelque
  chose sur l'exécutable — elle ne dit rien de l'exécutable.

---

## 8. Option (c) — licences différenciées par crate

### 8.1 La mécanique existe, et elle est constatée en pratique amont

Le champ est **par paquet**, pas par dépôt — Cargo Book : « field contains the
name of the software license that the package » is released under. Et la pratique différenciée est constatée sur octets détenus dans le
workspace TLSNotary lui-même : `tlsn-crate-tls-core-cargo-toml-2026-08-12.toml`
porte `license = "Apache-2.0 OR ISC OR MIT"` tandis que
`tlsn-crate-tlsn-cargo-toml-2026-08-12.toml` porte `license = "MIT OR
Apache-2.0"`. Deux expressions différentes, deux crates du même workspace.

### 8.2 La contrainte dure que le cadrage d'ADR-0014 n'avait pas vue

ADR-0014 pt 1 formule l'option ainsi : « **différenciées par crate**, le
vérificateur au régime le plus ouvert » / « (c'est l'artefact de confiance). »

**[raisonnement — point à faire remonter]** Cette formulation se heurte à une
arête que le projet a rendue obligatoire par ailleurs. ADR-0010 pt 3 :
« `shogen-verifier -> shogen-core`, et rien d'autre » — et le manifeste
`crates/shogen-verifier/Cargo.toml` porte effectivement
`shogen-core = { path = "../shogen-core", version = "=0.0.0" }`. Le binaire
`shogen-verifier` **contient** donc le cœur. Conséquence :

- Si `shogen-core` est **AGPL** et `shogen-verifier` **MIT**, le binaire
  distribué est une combinaison des deux. §5(c) de l'AGPL prétend s'appliquer
  au tout : « You must license the entire work, as a whole, under this »
  « License ». Le vérificateur ne serait donc pas, en pratique, « au régime le
  plus ouvert » — il serait au régime du cœur.
- La différenciation ne fonctionne **que dans le sens croissant de
  permissivité vers l'aval** : le régime effectif du vérificateur est borné
  par celui du cœur, jamais l'inverse.
- Le sens inverse (cœur permissif, vérificateur AGPL) est mécaniquement
  possible mais [raisonnement] contredit l'intention citée : il fermerait
  précisément l'artefact que la vision veut le plus ouvert.

**La forme de (c) qui reste cohérente** [raisonnement] : cœur + vérificateur
au **même** régime permissif (l'artefact de confiance et ce qu'il contient),
et régime différent — plus protecteur — sur ce qui **ne** rentre **pas** dans
le binaire du vérificateur : `xtask` (l'outillage de gates), les futurs
`adapters/`, et le futur `shogen-collector` (DEVOPS §2). Cette forme est
instruite ici comme **variante (c′)** ; elle n'est pas recommandée, elle est
signalée parce que le cadrage d'ADR-0014 ne la distingue pas de (c).

### 8.3 Ce que (c) coûte en toutes variantes

- **Trois expressions SPDX à tenir cohérentes** au lieu d'une, plus les
  fichiers `LICENSE-*` correspondants, plus la ligne de README. Chaque crate
  nouvelle (un adapter par transport — ADR-0001) rouvre la question.
- **La revue devient obligatoire à chaque nouvelle arête** : toute dépendance
  interne nouvelle change le régime effectif du binaire qui la contient. C'est
  une charge de gate, pas une charge de rédaction — et la gate `S-G2` contrôle
  déjà la fermeture de dépendances réelle (`cargo tree -e normal`), donc le
  crochet mécanique existe.
- **Le lecteur externe doit lire trois manifestes** pour savoir ce qu'il a le
  droit de faire, là où (a) tient en une phrase de README.

---

## 9. La contrainte amont : ce qu'ADR-0015 importerait avec les crates TLSNotary

**Ce §9 est le résultat le plus matériel du dossier.** Aujourd'hui la question
est vide (zéro dépendance hors dev, §2) ; elle devient réelle à la seconde où
ADR-0015 retient « vérification du transport embarquée » (13 §2, première des
trois formes).

### 9.1 Ce que le projet amont déclare

`tlsn-repo-readme-raw-2026-08-12.md`, section License : « All crates in this
repository are licensed under either of » — Apache License, Version 2.0 / MIT
license — « at your option. » Et la clause d'entrée : « Unless you explicitly
state otherwise, any contribution intentionally submitted » for inclusion in
the work by you « shall be » dual licensed as above.

### 9.2 Ce que les autres pièces détenues constatent — et qui ne concorde pas

Quatre constats, chacun mesuré sur une copie détenue :

1. **GitHub ne détecte aucune licence pour le dépôt.**
   `tlsn-repo-metadata-api-2026-08-12.json` contient `"license":null`.
2. **Il n'y a aucun fichier LICENSE à la racine du dépôt amont.** Inventaire
   complet de `tlsn-repo-root-contents-api-2026-08-12.json`, énuméré en
   entier : `.dockerignore`, `.github`, `.gitignore`, `CONTRIBUTING.md`,
   `Cargo.lock`, `Cargo.toml`, `README.md`, `crates`, `pre-commit-check.sh`,
   `rustfmt.toml`, `set_tlsn_version.rs`, `tlsn-banner.png`. **Ni
   `LICENSE`, ni `LICENSE-MIT`, ni `LICENSE-APACHE`.** C'est exactement le
   dispositif que C-PERMISSIVE prescrit et qui manque : « containing the text
   of the licenses (which you can obtain, for instance, from » choosealicense.
3. **Le manifeste de workspace amont ne porte aucun champ de licence.**
   `grep -c -i license tlsn-repo-workspace-cargo-toml-2026-08-12.toml` → **0**.
   Il n'y a pas de `[workspace.package]` d'où une licence serait héritée.
4. **Deux crates n'ont aucun champ `license`** :
   `grep -c -i license tlsn-crate-attestation-cargo-toml-2026-08-12.toml` → **0** ;
   idem pour `tlsn-crate-formats-cargo-toml-2026-08-12.toml` → **0**. Les
   autres manifestes détenus en portent un (`tlsn`, `tlsn-core`,
   `tlsn-sdk-core`, `tlsn-mpc-tls`, `tlsn-wasm` : `license = "MIT OR
   Apache-2.0"` ; `tlsn-tls-core` : `license = "Apache-2.0 OR ISC OR MIT"`).

**Pourquoi le point 4 est le plus lourd** [raisonnement] : `tlsn-attestation`
est précisément la crate des types côté vérification — c'est d'elle que
viennent `presentation.rs`, `proof.rs`, `signing.rs`, tous détenus au pack T3
(INDEX §S3). La forme « vérification du transport embarquée » de 13 §2 importe
donc en priorité la crate dont **aucune pièce détenue ne porte la licence en
manifeste**. La déclaration du README couvre bien « All crates in this
repository », mais c'est une déclaration en prose, hors du champ que
l'outillage lit — et `cargo-deny`, notre gate, lit le champ.

**Un cinquième constat, mineur mais à ne pas taire** : le badge Apache du
README amont pointe sur un autre projet —
`[apache-badge]: https://img.shields.io/github/license/saltstack/salt` (ligne
10 de la copie détenue). Un badge n'est pas une preuve de licence ; ce
constat n'accuse rien, il rappelle que la déclaration lisible par machine
manque là où l'humain croit lire une licence.

### 9.3 Ce que cela contraint, par option

- **Sous (a) « MIT OR Apache-2.0 »** : concordance de régime. La règle
  C-PERMISSIVE est satisfaite (« a permissively-licensed crate should »
  « generally only depend on permissively-licensed crates »), et la liste
  `allow` de `deny.toml` couvre déjà `Apache-2.0`, `MIT` **et** `ISC` —
  y compris l'expression `Apache-2.0 OR ISC OR MIT` de `tlsn-tls-core`.
  **Aucun amendement de gate n'est requis.**
- **Sous (b) AGPL-3.0** : [raisonnement] rien dans les textes détenus
  n'interdit à un projet AGPL de consommer des crates permissives — le sens
  entrant (permissif → copyleft) est celui que le copyleft absorbe. Le sens
  sortant est celui qui se ferme (§7.3). Le coût de (b) ici n'est donc pas
  l'amont, c'est l'aval.
- **Dans les trois options** : la crate `tlsn-attestation` **sans champ
  `license`** fait échouer `cargo deny check licenses` dès qu'elle entre au
  graphe, quelle que soit notre propre licence. [raisonnement] Ce n'est pas
  une question de licence de Shōgen : c'est un **fait de gate** qui atterrira
  sur ADR-0015, avec trois sorties possibles — (i) demander à l'amont d'ajouter
  le champ (procurement P2, §11), (ii) l'exception `clarify`/`exceptions` de
  `cargo-deny` documentée et portée par ADR, (iii) la forme « déléguée à un
  binaire du transport invoqué à côté » de 13 §2, qui ne fait pas entrer la
  crate au graphe du tout. **Ce dossier ne choisit pas ; il signale que la
  décision de licence de Shōgen ne résout pas ce point-là.**

---

## 10. La mécanique de mise en œuvre — identique pour toutes les options

### 10.1 Le champ de manifeste

Cargo Book : « field contains the name of the software license that the package »
is released under ; « SPDX license expressions support AND and OR operators to
combine multiple » licenses ; le nom doit venir de la « SPDX license list 3.20 ».
Sémantique des opérateurs : « indicates the user may choose either license. Using »
… « the user must comply with both licenses simultaneously. » Et le rappel
registre (la copie détenue balise `license` et `license-file` en code ;
citation au texte rendu) :
« requires either license or license-file to be set. »

[raisonnement] Ce dernier point est le re-serrage mécanique d'ADR-0014 pt 3
vu depuis l'amont : tant que `publish = false`, rien ne l'exige ; le jour où
une crate devient publiable, le champ devient obligatoire.

### 10.2 Les fichiers

C-PERMISSIVE donne la recette complète pour (a) : le champ
`license = &quot;MIT OR Apache-2.0&quot;` au manifeste, puis les fichiers
`LICENSE-APACHE` et `LICENSE-MIT` à la racine, « containing the text of the
licenses (which you can obtain, for instance, from » choosealicense.com, puis
la section `## License` du README et la clause de contribution.

**Nous détenons déjà les textes** : `apache-license-2.0-2026-08-12.txt` est le
texte canonique apache.org (sha256 à l'INDEX). [raisonnement] Le texte MIT que
nous détenons est une **page HTML OSI**, pas un fichier texte canonique : un
`LICENSE-MIT` en clair reste à produire (§11, manque M5 — le plus léger de
tous, un fetch de `opensource.org/license/mit` en texte ou la recopie du
paragraphe déjà cité au §4.1 avec l'année et le titulaire).

### 10.3 L'écriture qui matérialise la décision

Quelle que soit l'option, la décision se pose en cinq écritures :

1. `Cargo.toml` (workspace) ou les trois manifestes : le champ `license` (ou
   `license.workspace = true` si le régime est uniforme).
2. Les fichiers `LICENSE-*` à la racine.
3. La section `## License` du `README.md` et la clause de contribution.
4. `deny.toml` : **inchangé sous (a) et (c′)** ; **amendé sous (b)** (ajouter
   `AGPL-3.0` à `allow`) — modification de gate, donc portée par ADR.
5. `docs/DEVOPS.md` §1 et `docs/DECISIONS.md` : la clôture d'ADR-0014.

### 10.4 Ce que la décision ne débloque **pas**

[raisonnement] Le champ `license` ne rend rien publiable : `publish = false`
reste au workspace, et c'est une décision distincte (ADR-0014 pt 3). Choisir
une licence et publier sur crates.io sont deux actes séparés — le premier est
dû à S3, le second n'est dû par aucun contrat détenu.

---

## 11. Ce qui n'est pas instruit sur pièce — manques nommés

Aucun de ces manques n'est contourné ; chacun est une candidate à procurement
adressée au mainteneur (règle du 2026-08-05). Les deux premiers ne sont pas
solubles par un fetch : ce sont des questions juridiques, pas
bibliographiques.

| # | manque | pourquoi il compte | forme de la résolution |
|---|---|---|---|
| **M1** | Ce que produit le **silence de MIT sur les brevets** (grep : 0 occurrence) | c'est le motif exact qu'ADR-0014 donne à Apache-2.0 (« concession de brevets d'Apache-2.0) ») ; l'effet du silence n'est pas dans le texte | avis juridique — **hors périmètre bibliographique**. Signalé comme tel : aucun fetch ne le comble |
| **M2** | La frontière **combinaison (§5c) / agrégat** pour un binaire Rust liant statiquement une crate AGPL | c'est la question dont dépend Q2 sous l'option (b), et Q1 sous l'option (c) telle que cadrée | avis juridique ; en appoint documentaire, la FAQ GPL de la FSF (gnu.org) — **non détenue** |
| **M3** | La **compatibilité Apache-2.0 → AGPL-3.0** (`grep -c -i apache` sur le texte AGPL : 0) | conditionne la faisabilité de (b) si ADR-0015 importe des crates Apache-2.0 | page *Various Licenses and Comments about Them* (gnu.org) — **non détenue**, librement redistribuable, **candidate à fetch par l'orchestrateur** |
| **M4** | La pratique d'**accord de contribution (CLA/DCO)** requise pour conserver la faculté de double licence sous (b) | sans elle, l'option (b) perd sa propre porte de sortie commerciale dès le premier contributeur externe | aucune pièce détenue ; candidate à procurement |
| **M5** | Un **texte MIT en clair** (`LICENSE-MIT`) — nous ne détenons que la page HTML OSI | mécanique pure : le fichier à poser à la racine sous (a) et (c′) | fetch trivial `opensource.org/license/mit` — **candidate à fetch par l'orchestrateur** |
| **P2** | Le **`CONTRIBUTING.md` de tlsnotary/tlsn** — présent à l'inventaire racine détenu, **jamais acquis** | c'est la pièce qui dirait si les contributions amont sont bien dual-licenciées, donc si la déclaration README couvre les crates sans champ | **candidate à fetch par l'orchestrateur** (raw.githubusercontent, épinglé au commit `0fe3c32d` comme le reste du pack T3) |
| **P3** | Les fichiers `LICENSE-MIT`/`LICENSE-APACHE` de tlsnotary/tlsn | ils **n'existent pas** à la racine (constat §9.2 pt 2) — le manque est un fait, pas une lacune d'acquisition | rien à procurer ; c'est le constat qui alimente P2 et la question Q6 (§13) |

**Note de méthode.** Aucun fetch n'a été exécuté par ce worker : le
téléchargement de pièces est un acte que le mainteneur autorise, et la règle
du projet prescrit qu'un manque **se nomme** plutôt qu'il ne se contourne.
M3, M5 et P2 sont prêts à être versés par l'orchestrateur sur instruction —
ce sont trois URL publiques, librement redistribuables, et leur absence
n'empêche pas les questions du §13 d'être posées.

---

## 12. Table de synthèse — options × conséquences

| conséquence | **(a) MIT OR Apache-2.0** | **(b) AGPL-3.0** | **(c) différenciées par crate** |
|---|---|---|---|
| **Q1 — un tiers reconstruit le vérificateur** | oui, charge minimale (avis de copyright) | oui, et l'aval est obligé de rester ouvert | oui ; **mais** le régime effectif du binaire est celui de `shogen-core`, pas celui déclaré sur `shogen-verifier` (§8.2) |
| **Q2 — embarquer dans un produit fermé** | oui ; Apache exclut même le lien d'interface de l'œuvre dérivée | non si combinaison (§5c) / oui si agrégat — **frontière non tranchée, M2** | selon la crate, avec la contrainte d'arête du §8.2 |
| **Q3 — service sans publier ses modifications** | oui | non pour les **modifications** (§13) ; **oui** pour le Programme **non modifié** (§2) | selon la crate qui tourne dans le service |
| **Vision DEVOPS §1 (vérificateur ouvert)** | respectée | respectée | respectée **si** cœur ≤ vérificateur en restriction (§8.2) |
| **GTM — moat revendiqué** | intact : le moat nommé est la neutralité du tiers, pas l'exclusivité (§4 pt 2, §6 pt 2) | ajoute une protection que le GTM ne revendique pas | idem (a) sur le périmètre vérificateur |
| **GTM — offre payante (§5)** | sans friction | **friction sur notre propre service** si nos crates modifiées tournent dedans (§7.2 pt 3) | friction limitée aux crates protégées |
| **GTM — canal 1 (instrument des cabinets, sous leur marque) et canal transverse Kraidle** | sans friction | friction directe : intégration tierce = question §5(c) | friction selon le placement des crates |
| **Convention Rust détenue (C-PERMISSIVE)** | c'est exactement la recette citée | écart assumé, citable, non interdit | mixte |
| **`deny.toml` (gate S-G7)** | **inchangé** — `Apache-2.0`, `MIT`, `ISC` déjà dans `allow` | **amendement requis** (`AGPL-3.0` absent) → ADR de gate | inchangé si les régimes restent dans la liste |
| **Amont TLSNotary si ADR-0015 embarque les crates** | concordant (§9.3) | absorbable en entrant, fermant en sortant | concordant selon le placement |
| **Le point de gate que la licence ne résout pas** | `tlsn-attestation` sans champ `license` bloque `cargo deny` — **dans les trois options** (§9.3) | idem | idem |
| **Coût de rédaction/maintenance** | 2 fichiers + 1 champ + 1 section README | 1 fichier + 1 champ + amendement de gate + question CLA (M4) | N champs, N fichiers, revue à chaque arête nouvelle |
| **Réversibilité** | [raisonnement] durcir plus tard est possible sur le code futur ; ce qui est publié sous (a) le reste | assouplir plus tard exige l'accord de tout contributeur non couvert par un CLA (M4) | selon la crate |
| **Ce qu'aucune option ne fait** | ne décharge pas `A(verifier-binary)` ; ne cède pas la marque (Apache §6) ; ne rend rien publiable (`publish = false` reste) | idem | idem |

---

## 13. Les questions exactes que le mainteneur doit trancher

Posées dans l'ordre où la réponse à l'une contraint les suivantes.

**Q1 — La question de fond, qui commande tout le reste.**
Le risque que le mainteneur veut couvrir est-il **(i)** *un tiers embarque notre
vérificateur dans un produit fermé et ne rend rien*, ou **(ii)** *un tiers
offre un service concurrent à partir de notre code* ? Les pièces
montrent que **(i)** est adressé par (b) sous réserve M2, et que **(ii)** ne
l'est **pas** par l'AGPL (§2 : « permission to run the unmodified Program »).
Si la réponse est *ni l'un ni l'autre — le moat est la neutralité*,
GTM §4 pt 2 et §6 pt 2 sont déjà écrits en ce sens et l'option (a) suffit.

**Q2 — La concession de brevets d'Apache-2.0 est-elle voulue pour elle-même ?**
ADR-0014 la nomme comme motif. Le texte détenu montre qu'elle fonctionne dans
les deux sens (§4.2). MIT ne dit rien du brevet (0 occurrence). Sous (b),
l'AGPL a sa propre clause §11 : « Each contributor grants you a non-exclusive,
worldwide, royalty-free » / « patent license under the contributor's essential
patent claims, to ». Question : la protection brevet
est-elle un critère de choix, ou un effet secondaire acceptable ?

**Q3 — Sous (c), quelle frontière exacte ?**
Le cadrage d'ADR-0014 (« le vérificateur au régime le plus ouvert ») est
mécaniquement borné par l'arête `shogen-verifier → shogen-core` d'ADR-0010
(§8.2). Le mainteneur retient-il **(c)** telle que cadrée — auquel cas
ADR-0014 pt 1 doit être corrigée — ou la variante **(c′)** (cœur et
vérificateur au même régime ouvert ; `xtask`, `adapters/`, `shogen-collector`
éventuellement plus protégés) ?

**Q4 — Sous (b) uniquement : la double licence est-elle voulue ?**
Si oui, un accord de contribution est requis avant le premier contributeur
externe (manque M4) et devient une unité de travail S3. Si non, l'offre
payante de GTM §5 devra tourner sur du code **non modifié**, ou publier ses
modifications.

**Q5 — L'amendement de `deny.toml` est-il accepté ?**
L'option (b) exige d'ajouter `AGPL-3.0` à la liste `allow` — une modification
de gate, donc une ADR (charte `shogen-devops` §2). Les options (a) et (c′) ne
touchent pas la gate.

**Q6 — Les trois fetches nommés sont-ils autorisés à l'orchestrateur ?**
`CONTRIBUTING.md` de tlsnotary/tlsn (P2), la page de compatibilité gnu.org
(M3), le texte MIT en clair (M5). Aucun n'est nécessaire pour trancher Q1–Q5 ;
P2 l'est pour ADR-0015.

**Q7 — Question de séquence, hors licence mais couplée.**
La décision de licence est-elle prise **maintenant** (elle débloque
`deny.toml` et l'écriture des manifestes) ou **au moment du passage public**
(13 §5 pt 2 : l'acte irréversible qui appartient au mainteneur) ? ADR-0014 dit
« l'événement S3, pas une date » et nomme le déclencheur : « le passage public
du dépôt ». Les deux moments peuvent être séparés — le champ `license` peut
être posé avant le passage public sans rien rendre opposable, puisque le dépôt
reste privé.

---

## Annexe — inventaire des citations et contrôle mécanique

**Contrôle exécuté sur le fichier final** (script de comptage passé sur le
corps du dossier, hors annexe) : **144 citations entre guillemets français**,
**144 résolues**, **0 non résolue**. Chaque citation a été retrouvée par
recherche littérale dans un fichier détenu ou dans un document du dépôt.
**102 sont adossées à une pièce de `biblio/`** ; les 42 autres citent des
documents internes du dépôt (`docs/`, manifestes, `deny.toml`).

Répartition par pièce de première attribution :

| pièce | citations |
|---|---|
| `gnu-agpl-3.0-2026-08-12.*` (texte + page) | 33 |
| `apache-license-2.0-2026-08-12.txt` (+ page) | 24 |
| `rust-api-guidelines-necessities-2026-08-12.html` (C-PERMISSIVE) | 19 |
| `cargo-reference-manifest-2026-08-12.html` | 13 |
| `osi-mit-license-2026-08-12.html` | 5 |
| `rust-lang-rust-copyright-2026-08-12.txt` | 3 |
| `tlsn-repo-readme-raw-2026-08-12.md` | 2 |
| `rust-lang-rust-readme-2026-08-12.md` | 1 |
| `biblio/INDEX.md` | 1 |
| autres pièces `biblio/` (fragments courts, attribution multiple) | 1 |
| **total `biblio/`** | **102** |
| `docs/DECISIONS.md` (ADR-0014, ADR-0010, ADR-0012) | 18 |
| `docs/07-gtm.md` | 12 |
| `docs/DEVOPS.md` | 4 |
| `docs/13-temoignage-e2e-design.md` | 3 |
| `docs/05-roadmap.md`, `docs/08-assumptions.md` | 2 |
| manifestes de crates (`shogen-core`, `shogen-verifier`) | 3 |

*Réserve d'honnêteté sur ce tableau* : quelques fragments courts (« patent »,
`license = "MIT OR Apache-2.0"`) apparaissent dans plusieurs pièces détenues ;
le script les attribue à la première trouvée. Cela n'affecte aucune
affirmation du dossier — ces fragments sont cités pour leur présence, pas
pour leur exclusivité.

**Mesures négatives** — comptages nuls, qui portent chacun une affirmation du
dossier et sont re-vérifiables par la même commande :

| commande | résultat | ce qu'elle établit |
|---|---|---|
| `grep -c -i patent biblio/osi-mit-license-2026-08-12.html` | **0** | MIT ne mentionne pas le brevet (§4.1) |
| `grep -c -i apache biblio/gnu-agpl-3.0-2026-08-12.txt` | **0** | le texte AGPL ne dit rien d'Apache-2.0 (§4.3, manque M3) |
| `grep -c -i license biblio/tlsn-repo-workspace-cargo-toml-2026-08-12.toml` | **0** | pas de licence héritée du workspace amont (§9.2 pt 3) |
| `grep -c -i license biblio/tlsn-crate-attestation-cargo-toml-2026-08-12.toml` | **0** | `tlsn-attestation` sans champ `license` (§9.2 pt 4) |
| `grep -c -i license biblio/tlsn-crate-formats-cargo-toml-2026-08-12.toml` | **0** | `tlsn-formats` sans champ `license` (§9.2 pt 4) |
| énumération complète de `tlsn-repo-root-contents-api-2026-08-12.json` | **12 entrées, aucune `LICENSE*`** | pas de fichier de licence à la racine amont (§9.2 pt 2) |
| `grep -F '"license":null' biblio/tlsn-repo-metadata-api-2026-08-12.json` | **1** | GitHub ne détecte pas de licence de dépôt (§9.2 pt 1) |

**Contrôle de vocabulaire (09-vocabulaire, gate S-G4 à venir)** : passe faite
sur le fichier final pour `garanti*`, `verified`, `validated`, `guaranteed`,
`ensures` employés comme qualificatifs d'assurance — **0 occurrence**. Le mot
« vérifier » n'apparaît que comme nom de calcul (« vérifier une signature »),
usage licite selon 09. Les trois mots d'assurance (*proven / tested /
reviewed*) ne sont revendiqués nulle part dans ce dossier : **rien ici n'est
tested ni proven** — c'est une instruction de décision, pas un résultat.

**Ce que ce dossier n'a pas fait, et pourquoi** : aucun téléchargement. Les
trois pièces qui manquent et qui sont librement acquérables (P2, M3, M5 —
§11) sont nommées à l'intention de l'orchestrateur, qui tient `INDEX.md` et
autorise les versements. Aucune ligne de `biblio/INDEX.md` n'a été touchée.
