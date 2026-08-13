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
