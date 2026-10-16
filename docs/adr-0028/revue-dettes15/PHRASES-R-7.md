# Phrases de fermeture (R-7 du contre-contrôle, forme corrigée de C-8)

```
R-7 — Phrases de fermeture, forme corrigée de C-8 (contre-contrôle neuf de DETTES-T15, 2026-10-15). Elles remplacent
celles de C-8 là où elles diffèrent ; elles supposent R-1 à R-6 et R-8 adoptées (sinon, voir la dernière section).
Chiffres du contre-contrôle : journaux de g2/cc/journaux/.

SHOGEN-SG5-COMMENTAIRE-HTML-1 : « Fermé par DT15-a, complété par DT15-g, DT15-h, DT15-j et DT15-k, par les corrections
C-2, C-5 et C-6 de la relecture G2 et par les réserves R-2 à R-4 du contre-contrôle. S-G5 ôte des pages HTML et
Markdown du corpus, avant le débalisage, ce qu'elles ne donnent jamais à lire : les commentaires `<!-- … -->`, dont la
fin suit la tokenisation HTML (WHATWG, page du 2026-10-14 lue par la relecture G2) ; les commentaires factices (`<!`
sans `--`, `</` suivi d'un caractère qui n'est ni une lettre ni `>`) et les instructions de traitement (`<?`), jusqu'au
premier `>`, sans borne de longueur ; le contenu des éléments `script` et `style`, jusqu'à la fermante qui les clôt :
casse ignorée, états de la tokenisation pour `script`, balises lues jusqu'à leur vrai `>` ; tout ce qui suit
`<frameset>`. Le contenu d'un élément de texte brut (`title`, `textarea`, `xmp`, `iframe`, `noembed`, `noframes`,
`plaintext`) se lit trois fois, comme du balisage, comme du texte partout et comme du texte hors d'un contenu SVG ou
MathML : le corpus garde ce que les trois lectures gardent, jamais plus que la série sans C-6 ni que C-6 (sens sûr : un
ouvreur écrit dans un `textarea` affiché est ôté en trop). Sans fin, la construction court jusqu'au bout du fichier.
Ce qu'un script ou une interaction peut montrer reste au corpus. 32 des 53 tests neufs de DT15-a à k sont rouges
d'assertion sur le code d'avant leur diff (27 tests mutants, 4 témoins et le test de temps de DT15-k ; les deux tests
du double échappement de DT15-g, verts sur DT15-f, tuent des mutants) ; 7 des 11 tests de la relecture le sont sur la
série, 11 des 12 tests de R-3 sur la série corrigée, les 2 tests mutants de R-4 sur l'état d'avant ; les 3 tests de R-2
tuent les mutants qui retirent `xmp`, `noembed` ou `noframes`. Mutants : 12 de DT15-a et 52 de DT15-g à k ; 26 de la
relecture G2, tous tués sauf un équivalent déclaré ; 25 du contre-contrôle, tués sauf un équivalent (N10) et un mutant
qui ôte davantage (M11, sens sûr). Sur le corpus complet de la session, S-G5 est vert avant et après la série
(353 fragments contrôlés à la tête `6117ea1` ; 372 à `87e37d1`, réserves R-3 et R-4 comprises). Limites : contenu SVG
ou MathML lu comme du HTML, dont un élément de texte brut écrit dans le `title` d'un SVG (L-9) ; ouvreur écrit dans un
extrait ou un bloc de code Markdown (L-13) ; texte d'un `iframe`, d'un `noembed` ou d'un `noframes`, que la page
n'affiche pas. »

DT15-h (L-6) : phrase de C-8, inchangée.

Q-8 et Q-9 : phrases de §P3.5, sauf « corpus complet vert (347 fragments) », qui devient « corpus complet vert avant et
après la série (353 fragments à la tête `6117ea1`, 372 à `87e37d1`) ».

SHOGEN-REFS-LIGNE-CONTENU-1 : phrase de C-8, à trois changements près. « et par les corrections C-3, C-4, C-5, C-7 et C-9
de la relecture G2 » devient « par les corrections C-3, C-4, C-5, C-7 et C-9 de la relecture G2 et par les réserves R-1
et R-6 du contre-contrôle ». « et refuse sans la lire une entrée qui nomme un emplacement interdit » devient « et refuse
sans la lire une entrée qui nomme un emplacement interdit (un test voit une lecture faite avant le refus, R-1) ».
« 24 de la relecture, tous tués sauf deux, attendus (L-1 : le commit d'une entrée n'est lu qu'en forme hors du paquet) »
devient « 24 de la relecture, tous tués sauf deux, attendus (L-1 : le commit d'une entrée n'est lu qu'en forme hors du
paquet) ; 16 du contre-contrôle, 7 de code, tous tués (un par S-G9 sur le registre réel), et 9 de données : 5 tués,
2 équivalents, 2 vivants attendus (L-1 et L-2) ».

SHOGEN-RUNNERS-FLOTTANT-QUADRATIQUE-1 : phrase de C-8, où « (`--egal` ; plancher de la tête plus un, 61 à `4543667`,
C-10) » devient « (`--egal` ; plancher de la tête plus un, refait sur la tête du versement par `c10_generique.py`, corrigé
par R-5 et R-8 : 64 à `87e37d1`, 89 à `5d41d80`, 90 à `2726793`, 91 à `f9533e1`, 92 à `1d46d25`) », et « 6 de la relecture, tous tués par la ligne du job » devient « 6 de la
relecture et 5 du contre-contrôle, tous tués par la ligne du job ».

SHOGEN-PRESG5-QUADRATIQUE-1 (DT15-i) : phrase de C-8, l'adjudication du 2026-10-15 15:05:10 UTC (DT15-m, phase 4, « dans
le dépôt ») primant ; ajouter « contre-contrôle : DT15-i appliqué à une copie du `presg5.py` du scratchpad
(sha256 `60de40770b2889b7`), égal à `presg5/apres` ; différentiel de 119 364 cas sans écart ; tests de DT15-i : 3 verts
en 0,48 s sur la version corrigée, 2 rouges (plus de 20 s pour 8 000 000 de caractères) sur l'ancienne ».

Si R-2 à R-4 ne sont pas adoptées : la phrase de C-8 pour SHOGEN-SG5-COMMENTAIRE-HTML-1 est fausse sur « Le contenu des
éléments de texte brut (…) est recopié tel quel : un `<!--` ou un `<script` n'y ouvre rien » (dix formes où C-6 garde
un texte que la page n'affiche pas et que la série ôtait : §4.3 du rapport du contre-contrôle) et sur « Les tests mutants
sont rouges d'assertion sur le code d'avant leur diff » (deux tests mutants de DT15-g sont verts sur DT15-f).

```
