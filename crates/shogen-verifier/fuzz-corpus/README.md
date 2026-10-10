# Corpus de fuzz du vérificateur

Rattachement (G0) : **ADR-0011 seuil 7** — « zéro panique sur toute suite
d'octets — seuil binaire, non négociable (S-G3, 12 §5) ; budgets candidats :
≥ 15 min par CI, ≥ 4 h en nightly, **corpus de graines committé et croissant de
chaque contre-exemple** ». Échéance 5 de `docs/13-temoignage-e2e-design.md` §3.

Ces octets sont **versionnés**. Ce n'est pas une exception à la règle du dépôt
sur `biblio/` (les copies d'articles ne partent jamais au commit) : ce corpus
n'est la copie de rien. Chaque fichier est produit par le dépôt lui-même, ou
par une panique que le dépôt a observée.

## Les deux moitiés du corpus, qui ne se remplacent pas

| préfixe | origine | régénérable ? |
|---|---|---|
| `dirigee-*` | déduites des formes que le dépôt connaît — le lot d'exemple, le témoignage canonique des sept champs, les bords du décodeur CBOR, les deux surfaces texte (registre, et constat **au contrat d'ADR-0015 point 13**) | **oui** : `cargo xtask fuzz-corpus` les réécrit |
| `panique-*` | les octets exacts d'une panique observée, écrits par le harnais au moment où il l'a vue | **non** : rien ne les reconstruit |

`cargo xtask fuzz-corpus` n'écrase **que** les `dirigee-*`. Une commande qui
viderait le répertoire perdrait la moitié qui compte.

## Les graines distillées (`dirigee-distillee-*`, lot FUZZ, 2026-10-09)

13 §7 dette 3 (SHOGEN-FUZZ-DISTILLATION-1) : les campagnes instrumentées
atteignent des arêtes que les graines dirigées n'atteignent pas. Plutôt que
de verser leurs entrées, la distillation nomme les formes qu'elles exercent
(`xtask/src/distillation.rs`), une graine par forme : le plus souvent un refus
nommé du vérificateur, à chaque profondeur du lot canonique, du `subject`, du
constat et du CBOR, plus le registre en texte riche. Chaque graine porte le
classement que le vérificateur doit en rendre (`xtask/tests/distillation.rs`).
Ce sont des `dirigee-*` : `cargo xtask fuzz-corpus` les réécrit.

**Mesure de référence** (2026-10-09, Linux de la session cloud) : `afl-showmap
-C` d'AFL++ 4.40c (cargo-afl 0.18.2, rustc 1.97.1), binaire du commit
`c1122de`. Corpus dirigé d'origine, 16 graines : 1339 arêtes sur 3904. Corpus
dérivé de deux campagnes de 660 s (AFL++ ; libFuzzer sur nightly-2026-08-10,
graine 20261009), 2353 entrées : avec le corpus dirigé, 2413 arêtes, soit
1074 de plus que lui seul. Avec les 108 graines distillées : 2084 arêtes, 745
gagnées, dont 719 parmi les 1074 (66,95 %). La mesure 471/789 de 13 §7
(binaire de `20e1084`) n'est plus rejouable depuis `58dc96e` : la fraction
s'applique à la mesure neuve.

**La gate** : `cargo xtask fuzz-distillation <carte sans distillées> <carte
du corpus>` (job `cargo-afl` de `fuzz.yml`) refuse sous ⌈1074 × 471/789⌉ = 642
arêtes gagnées, ou si une arête du reste du corpus manque à la carte entière.
Un changement du vérificateur qui la fait passer sous le seuil appelle une
nouvelle distillation, jamais un seuil abaissé (13 §7 dette 3, verrou 2).

## Pourquoi une graine dirigée, et pas seulement du bruit

La forme canonique est étroite : un tirage qui part de zéro n'atteint jamais un
CBOR canonique de 87 octets, encore moins un témoignage de sept champs. La
mesure est au dossier — **20 s de fuzz, corpus sans le témoignage canonique :
22 057 486 cas exécutés, classe « sept champs » à 0**. La même mesure avec la
graine canonique ajoutée : **141 515 cas** dans cette classe. Le corpus n'est
pas un confort, c'est ce qui met le tirage au bord de la forme.

Le même argument vaut pour la surface **constat** depuis la vague 2 : le contrat
d'ADR-0015 point 13 est une ligne JSON de dix-huit clés triées, et aucun tirage
aveugle ne l'atteint. Les deux graines `dirigee-constat*.txt` portent donc la
forme acceptée et une forme refusée **tard** (hexadécimal de longueur impaire) :
sans elles, l'analyseur ne serait atteint que par ses premiers octets, jamais
par sa construction finale — contrôle de version, verdict, six longueurs.

## Ce que le passage du corpus établit

*Tested*, sur ces graines et sur les cas tirés, avec leur compte et leur
graine, à la date de l'exécution. Jamais *proven* : l'absence de panique n'est
pas établie (ADR-0010, §Coûts point 6), et le harnais n'est pas guidé par la
couverture — cette couche-là reste due (consultation R-26 du 2026-08-13).

## Quand une panique arrive

Le harnais écrit `panique-<16 premiers chiffres de l'empreinte>.bin` et sort
ROUGE. Le versement au dépôt est un **acte humain**, dans une PR, accompagné du
test nommé qui fixe le cas : « l'évasion devient un test » (DEVOPS §3). Le job
CI, lui, n'a pas le droit d'écrire au dépôt (`permissions: contents: read`) :
il imprime et casse.
