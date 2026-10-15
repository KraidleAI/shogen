# Contre-contrôle neuf de DETTES-T2 (cc2, passes 1 et 2, et R-9 ; clôture CONFORME) (transcrit)

> Transcription par l'orchestrateur le 2026-10-15 13:51:21 UTC du fichier dettes2/g2/cc2/RAPPORT-CC.md ; contrôle FM-1.1 des transcripts du générateur-correcteur, du réviseur G2 et des deux contre-contrôleurs, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# RAPPORT-CC : contre-contrôle neuf de DETTES-T2, passes C-13, C-14 et C-15 (DT2-h à DT2-k)

**Gate 0** : `claude-opus-5-5` (identifiant exact du modèle qui sert ce contre-contrôle ; effort max de la fiche worker).
Rôle : contre-contrôleur neuf ; je n'ai ni écrit ni relu ce lot. Brief : `g2/cc2/BRIEF-CC.md`, sha256 `22ab3f75432c1669b9c12cfc8f45239aa755294b15631740aa1c667b5506141e`.
Horloge (`date -u`) : début 2026-10-10 04:29:09 UTC ; fin 2026-10-10 06:21:54 UTC.
Base : `dda4bbcc2b0f480eb0c39d7891237e0e3d2b0918` (`git rev-parse HEAD` du dépôt, égale à la base du brief). Série `DT2-a` à `DT2-k`,
empreinte de la concaténation dans l'ordre recalculée : `1c86a417ba32babbc990e0c657b6afaebb2792f464a4ffdfe8b200718ce41f98` (conforme).
Objet : DT2-h (`780252af…`), DT2-i (`d041a67a…`), DT2-j (`a9fa3607…`), DT2-k (`7ef18354…`), dans l'état final de la série.
Tête du dépôt en fin de passe : `4d6f149` (DETTES-T14, commits d'un autre acteur). Entre dda4bbc et elle, `git diff --stat`
est vide sous `scripts/calib-actifs` et pour `gates.yml` : l'examen vaut tel quel. `WISHLIST.md` est modifié dans l'index par un
autre acteur ; je n'ai fait aucune écriture git.

## Verdict : CONFORME-AVEC-RÉSERVES (R-1 à R-5)

C-13, C-14 et C-15 sont faits comme décidé. Leurs tests sont rouges sur le code d'avant puis verts, et tous les jobs rejoués sont verts.
Sur mes 18 mutants (X05b compris, qui remplace X05), 13 sont tués ; les autres sont déclarés : deux équivalents (X05b, X17), deux
trous de test fermés par R-4 et R-5 (X07, X14), un non terminant remplacé (X05, FATAL, non compté).

Ma propriété (24 000 cas, écrite sans lire celle du générateur) trouve en revanche une **perte silencieuse neuve**, hors du tirage du
générateur. Elle contredit l'énoncé de C-15 (« le cas plafond ancré avant le début de l'historique ne peut alors plus atteindre une
fenêtre admise ») et le « 0 perte en mode hist » du §14 : c'est **R-1**. Elle se ferme en une condition, rouge sur la série puis verte,
éprouvée sur la série entière. R-2 (décalage vers l'avant), R-3 (README), R-4 et R-5 (trous de test) sont de moindre portée.
Aucune ne touche la prémisse de C-9 : sur données complètes, 0 perte en 7 947 cas.

## 1. Constats

### 1.1 C-13, C-14 et C-15 tels que faits (lus ligne à ligne dans l'état final)
- **C-13** (DT2-h, DT2-i). `socle.doubles` : second découpage décalé de h = ⌊u/2⌋, soit 74 et 249 minutes pour u = 148 et 498.
  Il va de début − h à fin + h au moins ; ses pages ne sont pas coupées à la fenêtre (fichiers `double-<début>.json`).
  `bougies.serie` contrôle chaque réponse sur [min(première bougie, cœur) ; dernière minute de sa page] contre toutes les bougies
  servies par tous les fichiers, celles qui sont hors filtre comprises : une absente donne CA/format, motif DISCORDE (TRONQUEE
  pour une page C-7, son motif pour une demi-page). Des valeurs différentes avec un fichier du second découpage donnent DISCORDE.
  `couverture` vaut 2 pour Coinbase et Bitstamp, 1 ailleurs ; cohérence : 1 ou 2, et 2 seulement pour une place paginée d'au moins
  2 minutes utiles. Complétude : « seconde couverture n pages ».
- **C-14** : `socle.demis` rend [] pour une page d'un seul point.
- **C-15** (DT2-j, DT2-k). `socle.sonde` : sondes de ⌊pas/2⌋ créneaux, recul exponentiel depuis fin − ⌊pas/2⌋ jusqu'à
  `historique.debut`, puis dichotomie. L'acquisition se fait par `acquerir.pages`, en couverture double ; la recherche est rejouée
  au chargement (`bougies._sonde`), et les fichiers doivent être exactement ceux de la recherche. Refus CA/avant-historique :
  (a) départ le plus précoce < T0 + pas − ⌊pas/2⌋ + 1 minutes ; (c) une bougie servie au plus tard en T0 ; (d) aucune bougie
  servie et aucune sonde non vide.
- Vérifié à la main :
  - les 11 sondes du test de couverture (25, −487, −231, −103, −167, −199, −215, −207, −211, −213, −214 ; T0 = −200), et les
    19 requêtes ;
  - les bandes de la perte R-1 sur ce banc (cren g = 100 : H0 dans ]−60 ; −54] ; crenp g = 100 : H0 dans ]−39 ; −33]).
- Rouges rejoués (`rouges/`), AssertionError seulement :
  - tests de DT2-h sur le code de l'état g : Ran 9, 8 FAIL, 0 ERROR ;
  - tests de l'état final (`test_sonde`, `test_couverture`, `test_socle`) sur le code de l'état i : Ran 9, 6 FAIL, 0 ERROR.
  Ces comptes sont égaux à ceux du rapport (`rouge-c13-final`, `rouge-c15`). Vert : job calib, Ran 77 (§4).

### 1.2 R-1 : perte silencieuse, toutes les sondes vides et la fenêtre servie (C-15)
**Constat.** `bougies.serie` ne refuse (d) que si aucune requête de la fenêtre ne sert de bougie. Si toutes les sondes reviennent
vides alors qu'une requête de la fenêtre sert des bougies, T0 est inconnu : ni (a) ni (c) ne peuvent jouer, et la fenêtre est admise.

Ce cas survient sous une fenêtre décalée de g minutes vers l'arrière (« cren »), ou sous un plafond en créneaux ancré g > pas −
⌊pas/2⌋ minutes avant start (« crenp »).
- Les sondes partent de fin − ⌊pas/2⌋, plus tôt que les requêtes les plus tardives : le second découpage dépasse la fin de h minutes.
- Elles reculent ensuite, toutes décalées de g.
- Quand le début de l'historique H0 tombe entre leur portée et celle de la requête la plus tardive, elles reviennent toutes vides.
- Seule cette requête sert des bougies, toutes hors de la fenêtre.
- La fenêtre est admise vide, ou incomplète.

Dans ma propriété, 96 des 97 cas ont un décalage ou un ancrage plus grand que la fenêtre ; le 97e est en marché mince (densité
0,3). H0 y tombe dans une bande d'au plus une page de minutes utiles, g minutes avant la fin : entre les deux plus grandes bornes
(cren) ou les deux plus grands départs (crenp), décalés de g. L'ancre de la requête fautive est avant H0 : c'est le cas « plafond
ancré avant le début de l'historique » que C-15 devait fermer.

Pourquoi le générateur ne l'a pas vu : sa propriété place toujours H0 avant s − g de toute requête hors « hist » ; en « hist », g vaut
1 000 et H0 vaut −3 pas − 40 (toutes les ancres avant l'historique, sondes comprises). Elle ne tire jamais cette bande.

**Preuves sur le vrai code** (`acquerir.pages` puis `bougies.charger` ; serveur simulé en processus à la frontière HTTP, sous
`isole.sh`) :
- banc minimal (`outils/banc.py`, `outils/diag.py`) : pas 30, c 1, fenêtre de 40 minutes. Sous cren g = 100 avec H0 = −57, et
  sous crenp g = 100 avec H0 = −36, la fenêtre est **admise avec 40 minutes manquantes sur 40**. Il y a 18 sondes, toutes vides ;
  une seule réponse est non vide (double 33 en cren, page 39 en crenp).
- échelle réelle (`outils/echelle.py`, `echelle.out`), marché échangé à chaque minute :
  - Coinbase pas 300, fenêtre de 88 pages puis de 131 040 minutes (886 pages, la fenêtre réelle de 91 jours) ;
  - Bitstamp pas 1000, 88 pages ;
  - cren et crenp, 6 cas sur 6 **admis sans aucune minute** (par exemple 131 040 manquantes sur 131 040). Sous R-1 + R-2
    (`echelle-R12.out`), les 6 sont refusés (« bougies servies, aucune sonde non vide »).
- propriété cc2 (§2) : 97 PERTE sur 24 000 (cren 56, crenp 38, retard variable 3), dont 36 à densité 1 ; parmi ces 36, 28 sans
  aucune bande muette.

**Forme exacte** (`propose/R-1.diff`, sur la série) :
- dans `bougies.serie`, la condition devient `if t0 and (t0[1] or tous and tous[0] <= t0[0])`. Motif « bougies servies, aucune
  sonde non vide » quand la fenêtre sert des bougies ; « aucune bougie servie » inchangé sinon ;
- docstring de `serie` ;
- `test_sonde` : deux cas, cren et crenp à g = 100, rouges sur la série (la fenêtre y est admise, 40 minutes manquantes). Ils sont
  insérés avant le cas « −23 », sur les bruts duquel opère la seconde partie du test ;
- `test_series` recalé : la sonde en `historique.debut` porte une bougie ;
- README (recul, refus) et `SHA256SUMS` du lot.

Le diff fait 5 fichiers, +33/−17, et porte aussi R-4. Ran reste à 77, le plancher est inchangé.

**Effet mesuré** (propriété cc2, même tirage ; calcul exact sur la colonne des sondes, confirmé par la campagne F108) :
- 97 PERTE deviennent des REFUS ;
- coût : 1 716 JUSTE deviennent des REFUS :
  - 1 291 fenêtres entièrement avant l'historique, que la règle même de C-15 refuserait si T0 était trouvé ;
  - 323 fenêtres proches du début de l'historique ;
  - 102 à historique lointain (67 sur données complètes), toutes en marché mince (densité ≤ 0,3) ou avec silences. Aucune en
    marché plus dense sans silence.

Alternative écartée, F4 (recul depuis le départ le plus tardif) : il reste 4 PERTE, et les refus sur données complètes passent de
3 004 à 3 711, parce que la dichotomie n'est pas monotone en marché mince.

### 1.3 R-2 : décalage vers l'avant non vu (C-13)
**Constat.** Le contrôle de C-13 couvre [min(première bougie, cœur) ; dernière minute]. Une réponse décalée de G minutes vers l'avant
perd ses minutes de tête, que seules des réponses plus précoces peuvent prouver. Il en découle deux pertes :
- au début de la fenêtre, aucune réponse plus précoce n'existe : un décalage G > h + c perd les premières minutes si les débuts de
  page sont sans échange. C'est le miroir de L-C13-2, qui n'est écrit qu'« au-delà de la fin » ;
- pour G plus grand que la fenêtre, toutes les réponses tombent après elle, sont écartées par le filtre (pt 2), et la fenêtre est
  **admise vide**, même avec un échange à chaque minute.

Propriété cc2 : 129 PERTE sur 24 000 (décalage vers l'avant, famille ajoutée à la liste du brief). Échelle réelle :
`outils/echelle_avant.py`, `echelle-avant.out` : sur la série, un décalage vers l'avant plus long que la fenêtre est
admis vide (Coinbase, 886 pages : 131 040 minutes manquantes sur 131 040 ; Bitstamp, 30 jours : 43 200 sur 43 200), alors
qu'un décalage de 5 000 minutes sur 88 pages est refusé par C-13 (DISCORDE). Sous R-1 + R-2 : les trois cas sont refusés (R-2).

**Forme exacte** (`propose/R-2.diff`, sur R-1) :
- refus nommé (CA/format, « réponse entièrement après la fin demandée et son chevauchement ») d'une réponse dont toutes les bougies
  suivent sa borne + c, c étant `cœur − départ` : `min(ts) > plafond[4] + plafond[5] - plafond[1]` ;
- test `test_couverture` « avant-100 », rouge sur la série ;
- README : règle, et miroir de L-C13-2.

Le diff fait 4 fichiers, +23/−9.

Une **bougie isolée** après la fin reste écartée. C'est imposé par le point 2 de la DECISION : `test_formes` sert une bougie 2 minutes
après la borne de la page 0 et exige qu'elle soit écartée. Ma première forme, F8' (`max(ts)`), a été refusée sur la série entière
(`test_formes`, 5 sous-cas) ; c'est le mutant Y03, tué.

Mesuré :
- F8' : 129 → 65 PERTE ;
- F8'' (la forme retenue) : 129 → 66 PERTE, dont 64 au-delà de la fin des données, 1 miroir de L-C13-2 et 1 en marché mince ;
  coût : 59 JUSTE → REFUS, tous sous décalage vers l'avant.

Sur les 66 pertes restantes, 64 ont toutes leurs réponses au-delà de la fin des données du marché : rien n'est servi pour la
fenêtre, ce qui est indiscernable d'une fenêtre muette, admise par conception. Sur les fenêtres du lot (91 et 30 jours), il
faudrait un décalage de plusieurs mois. Une est le miroir de L-C13-2 (décalage plus court qu'une requête) ; une est en marché
mince.

Alternative, si l'orchestrateur ne veut pas de refus neuf : écrire seulement le miroir de L-C13-2 et la perte totale au-delà de la
fenêtre au README.

### 1.4 R-3 : README de `scripts/calib-actifs` (point 5)
Forme exacte des corrections (texte complet dans `propose/R-1.diff` et `propose/R-2.diff`) :
- (i) la recherche **recule** de ⌊pas/2⌋ (2^j − 1) minutes tant que les sondes sont vides, avant la dichotomie : le README l'omet
  (« la première en fin − ⌊pas/2⌋ minutes, puis dichotomie ») ;
- (ii) « aucune bougie servie » : le code exige aussi qu'aucune sonde ne soit non vide (« ni sondée ») ; à écrire tel quel, ou
  selon R-1 ;
- (iii) L-C13-2, « 32 cas sur 60 000 dans la propriété, fenêtres de 1 à 10 minutes » : exact pour la propriété du générateur.
  Les 32 fenêtres sont toutes relevées : graines 7 et 12 rejouées sur l'état final (copie de son outil à plafond d'exemples
  levé ; lignes de comptes identiques à l'origine, 61 et 58), graine 11 d'origine ; elles valent 1 (21 cas), 2 (7), 3, 4 et
  10 (2). À préciser :
  - « dans la propriété du générateur » ;
  - 23 des 32 cas sont à chevauchement 0, configuration que les places en couverture double du lot n'ont pas (c = 1) ;
  - ma propriété trouve des pertes de queue jusqu'à 27 minutes de fenêtre (95 en marché mince) ;
- (iv) limites non écrites : celle de R-1, si elle n'est pas corrigée ; le miroir avant de L-C13-2 et la perte totale par décalage
  vers l'avant (R-2).

Le reste est exact :
- 74 et 249 minutes ; « environ 24 par paire et par fenêtre » (24 à 25 recalculées par `socle.sonde`) ;
- seuil pas − ⌊pas/2⌋ + 1 ;
- refus (a) et (c) ;
- garde C-7, C-8 et C-14 ; OKX.

### 1.5 R-4 : seuil (a) non épinglé (mutant X07 vivant)
Le seuil d'une minute de moins (`pas − pas // 2` au lieu de `pas − pas // 2 + 1`) passe la suite. Il n'est pas équivalent : avec un
historique depuis −22, la série refuse (−7 < −6) et le mutant admet.

Forme exacte : cas `(lecture, "exact", 0, -22, 200, avant)` dans `test_sonde` (`propose/R-1.diff`). X07 est tué sur l'arbre R.

### 1.6 R-5 : compte « seconde couverture » non épinglé (mutant X14 vivant)
Compter aussi les demi-pages du second découpage passe la suite. Ce n'est pas équivalent : les demi-pages de `double-` existent dès
qu'une page du second découpage est suspecte (C-8 sous « recentes »).

Forme exacte (`propose/R-5.diff`, sur R-2 ; 2 fichiers, +16/−2) : assertion dans `test_comptes`, sur un dossier écrit à la main
(une page, une page du second découpage redemandée, une autre non). Résultat attendu : « pages redemandées 1 ; seconde couverture
2 pages ». X14 est tué sur l'arbre R ; Ran reste à 77.

### 1.7 Observations, sans réserve
- **O-1, refus sur données complètes hors du modèle de marché du générateur.** Ce sont des échecs fermés, jamais des pertes.
  - (c) ne frappe que « recentes » (251 cas ; jamais cpt ni crenp dans la prémisse, ce qui confirme la marge du seuil (a)).
  - La dichotomie non monotone place T0 trop tard en marché mince : 97 refus (a) à historique lointain.
  - (d) frappe des fenêtres muettes en marché mince : 203.
  - « Aucun refus dans la prémisse de C-9 » est donc vrai dans le tirage du générateur (recompté), pas en général. Pour des paires
    liquides, ces refus ne surviennent pas.
- **O-2.** Une fenêtre entièrement avant l'historique, avec T0 entre fin − 1 et la dernière borne, est admise vide. C'est juste
  (vérité vide), mais contraire à la lettre de C-15. R-1 la refuse.
- **O-3.** Mutants déclarés équivalents :
  - X05b (milieu de la dichotomie arrondi au-dessus) : même x* et même T0 sous toute lecture monotone. Seule la suite des sondes
    diffère, et elle est rejouée de même au chargement ; les distances des tests sont des puissances de 2.
  - X17 (T0 pris à la dernière bougie de la sonde) : sous toute lecture fixe, la sonde retenue porte au plus une bougie, puisque sa
    voisine vide en couvre toutes les minutes sauf la dernière. X17 ne diffère que sous retard variable, où il refuse davantage.
- **O-4.** docs-sha256sums donne 39 SHA256SUMS et 314 lignes sur dda4bbc, contre 38 et 310 au générateur sur 0e03a9f (la tête a
  avancé) ; non investigué plus avant, faute de liste du dépôt (règle).

## 2. Ma propriété (`outils/propriete_cc2.py`, sha256 `5df0c28c0fd1d282cdfee859c3555518a69ae4c5764ac46283d5c4617e24f867` ; bilan `bilan-w.out`)
Le banc est écrit sans lire celle du générateur ; je ne l'ai lue qu'après le lancement de la mienne.
- Code exercé : le vrai code du lot (`acquerir.pages` avec les pages, le second découpage, les demi-pages et les sondes, puis
  `bougies.charger`), avec `acquerir.lire_url` remplacé en processus.
- Marché : déterministe par graine, aux formats Coinbase (minutes échangées seules) et Bitstamp (volume 0 sans échange).
- Tirage :
  - pas de 8 à 60, c de 1 ou 2 (cohérence de `socle.coherent`), fenêtre de 1 à 6 pages ;
  - lectures : exact (début et fin inclus ou exclus), recentes, cpt, crenp, cren vers l'arrière et vers l'avant, retard variable,
    plafond ancré à un point fixe avant l'historique, une valeur fausse ou une bougie retirée dans une réponse ;
  - g de 0 à 50 pas, ou plus que la fenêtre ;
  - H0 lointain, très lointain, au bord ou dans la fenêtre, ciblé sur la bande de R-1, ou après la fenêtre ;
  - densités de 1 à 0,03 ; bandes muettes en fin de page des deux découpages, silence long après H0, fenêtre muette.
- Verdicts : JUSTE (série = vérité), REFUS (socle.Refus), PERTE (série admise différente), ERREUR.

Graines 11 à 14, 6 000 cas chacune, soit **24 000 cas** (PID 8434, de 04:48:22 à 04:55:15). Résultats :

| Lecture | JUSTE | REFUS | PERTE | ERREUR |
|---|---|---|---|---|
| exact (prémisse) | 1 920 | 932 | 0 | 0 |
| recentes (prémisse) | 1 076 | 789 | 0 | 0 |
| cpt, g ≤ pas − ⌊pas/2⌋ | 998 | 681 | 0 | 0 |
| crenp, g ≤ pas − ⌊pas/2⌋ | 949 | 602 | 0 | 0 |
| cpt au-delà | 361 | 1 407 | 9 | 0 |
| crenp au-delà | 204 | 1 630 | 47 | 0 |
| cren vers l'arrière | 491 | 2 868 | 71 | 0 |
| cren vers l'avant | 130 | 628 | 129 | 0 |
| plafond ancré à un point fixe (cpt, crenp) | 87 | 1 792 | 0 | 0 |
| valeur fausse ; bougie retirée | 1 542 | 2 314 | 0 | 0 |
| retard variable (cpt, cren, crenp) | 758 | 1 575 | 10 | 0 |

Les pertes se répartissent par mécanisme :
- **M1** (aucune sonde non vide, fenêtre servie : R-1) : 97 ;
- **AV** (décalage vers l'avant : R-2) : 129 ;
- **queue** (L-C13-2) : 11, plus 29 en marché mince.

Il n'y a aucune perte sur données complètes (exact, recentes, cpt et crenp dans la prémisse : 7 947 cas), ni sous valeur fausse,
bougie retirée ou plafond à point fixe. Les refus sur données complètes sont de 3 004, dont 2 453 par conception (H0 proche ou après
la fenêtre) ; le reste relève de O-1.

Variantes, même tirage :
- F4 : `bilan-F4.out` ;
- F10 + F8' : `bilan-F108.out`, M1 97 → 0, AV 129 → 65 ;
- R-1 + R-2 (F8'') : `bilan-R12.out` (prop-R12, 24 000 cas) : M1 0, AV 66, queue 11 et marché mince 29 inchangés, 0 ERREUR ;
  refus sur données complètes 3 004 → 3 791 (R-1 seule).

## 3. Chiffres du rapport du générateur (point 2), recomptés par script sur ses sorties brutes
- Cas : 60 000 par passe (62 365 lignes de classe en C-15, moins 2 365 sous-comptes « redemandée »).
- **0 perte en « hist »** : cpt-hist 2 142 REFUS « réponse portant la première bougie de l'historique », crenp-hist 2 142 REFUS
  « aucune bougie servie » ; en C-13, 2 001 + 2 017 = 4 018 PERTE. Exact dans son tirage, mais faux en général : R-1.
- **Aucun refus dans la prémisse de C-9** : exact 2 145, recentes 2 145, cpt 5 913, crenp 5 951, tous JUSTE, aucun REFUS. Les
  JUSTE sont identiques à C-13. Exact dans son tirage (O-1).
- **12 refus au-delà** (L-C15-1) : cren 13 → 11 JUSTE et 11 191 → 11 193 REFUS ; crenp 687 → 677 et 10 496 → 10 506. Exact.
- **32 pertes de L-C13-2** : cren 10 + 20, crenp 2, identiques en C-13 et C-15. Les 28 exemples imprimés en C-15 ont L ∈ {1, 2, 3,
  4, 10}. Les 4 pertes non imprimées (graine 7 : 3 ; graine 12 : 1) sont relevées par rejeu sur l'état final (copie de son outil,
  plafond d'exemples levé ; lignes de comptes identiques à l'origine, 61 et 58, ce qui reproduit ses résultats). Les 32 ont L ∈ {1,
  2, 3, 4, 10} ; 23 sont à chevauchement 0, 9 à c ≥ 1. Exact.
- **Coût de la sonde**, recalculé par `socle.sonde` sur les paramètres réels (lecture exacte, T0 en 2014, 2016, 2021 ou 2024) :
  - 24 à 25 sondes par recherche, 10 recherches, soit 240 à 248 requêtes ;
  - attente de 32,6 à 33,3 s (Coinbase) et de 28,8 à 30,0 s (Bitstamp).
  Le rapport dit « environ 25 », « 250 », « 34 s » et « 30 s » : conforme à l'arrondi près.
- Autres chiffres :
  - +/− des diffs (h 200/53, i 93/63, j 35/8, k 190/44), 0 octet 92 dans les onze diffs ;
  - requêtes : Coinbase 4 716 (2 356 sans C-13), Bitstamp 2 112 (1 053), Bitfinex 108 ; débit 2 252 s = 37,5 min (20,6 sans C-13) ;
  - `SHA256SUMS` du lot : `3749accc…`.
  Tout est conforme.

## 4. Rejeux (point 3)
Conditions : copie A neuve (`git archive dda4bbc`, chemins interdits exclus comme chez le générateur, série appliquée ; lot identique
à la copie d'étude, `sha256sum -c` vert). Lignes exactes de son `gates.yml`, un job à la fois, sous `isole.sh` et
`env -u SHOGEN_S2_CAMPAGNE_CONTROL -u HTTPS_PROXY …`, `PYTHONDONTWRITEBYTECODE=1` (`outils/gates.sh`, sorties `gates/`).

| Job | Résultat (copie A, série) | Arbre R (série + R-1 + R-2 + R-5) |
|---|---|---|
| calib-actifs (`--plancher 77`) | code 0, Ran 77 = plancher, conforme | code 0, Ran 77 |
| matrice 3.10, 3.11, 3.12, 3.13 en `-X dev -W error` | 4/4 code 0, Ran 77, 0 « Exception ignored », 0 « Warning » | 4/4 code 0, Ran 77 |
| runner (run-fixtures-verdict-suite-s2) | 137 ok, 0 échec | — |
| controle | Ran 37, conforme | — |
| s2bis | Ran 342, conforme | — |
| S2 (`--egal`) | Ran 419, conforme (sauts nommant la variable) | — |
| docs-sha256sums | conforme, 39 SHA256SUMS, 314 lignes | conforme |
| journaux-modele | conforme | — |
| `cargo --locked --offline xtask verify` | code 1 ; 10 lignes VERDICT identiques à celles du générateur (8 VERT, 9e ROUGE à 1 violation, GLOBAL ROUGE) ; violation de la 9e (S-G9) : `docs/17-modele-de-menace.md:70` | — |
| `cargo --locked --offline test` (I-1) | code 0 ; 28 lignes « test result » toutes ok : 269 passés, 0 échec, 0 ignoré (les erreurs de la crate `jouet` viennent du test `mutant_construction_en_echec_ne_rend_aucun_verdict`, qui la compile cassée exprès) | — |

`--offline` est nécessaire dans l'espace réseau isolé, comme chez le générateur. La cible est celle par défaut de la copie
(`CARGO_TARGET_DIR` non posée ni héritée : `A/target`).

## 5. Mutants (point 4 ; `outils/mutants_cc2.py`, `outils/mutants_run.py`)
Les mutants sont les miens, chacun sur une ligne de DT2-h à DT2-k. La ligne du job est lue dans `gates.yml` ; un mutant à la fois,
borne de 600 s avec killpg, fichier restauré et vérifié par sha256. Classement par la sortie du vérificateur (0 vivant, 1 tué, autre
FATAL). Sorties : `mutants-cc2.tsv` (A), `mutants-cc2-X05b.tsv`, `mutants-cc2-R.tsv` (R).

| Mutant | Intention | A (série) | R |
|---|---|---|---|
| M00 | témoin, aucune mutation | vivant | vivant |
| X01 | second découpage non décalé (h = 0) | TUÉ (15 échecs) | |
| X02 | contrôle sans la dernière minute de la page | TUÉ (3) | |
| X03 | contrôle depuis le cœur seul | TUÉ (1) | |
| X04 | bougies hors filtre non prises comme preuve | TUÉ (6) | |
| X05 | milieu + 60 | FATAL (borne : dichotomie non terminante, E-3) | |
| X05b | milieu arrondi au-dessus | vivant, équivalent (O-3) | vivant |
| X06 | recul linéaire | TUÉ (3) | |
| X07 | seuil (a) − 1 minute | **vivant** (R-4) | TUÉ |
| X08 | (c) strict | TUÉ (1) | |
| X09 | (d) retiré | TUÉ (1) | |
| X10 | sondes non rejouées au chargement | TUÉ (12) | |
| X11 | cohérence, demi-page nulle admise | TUÉ (1) | |
| X12 | demi-requêtes d'une page d'un point | TUÉ (2) | |
| X13 | cohérence, sondes depuis le début admises | TUÉ (1) | |
| X14 | complétude, demi-pages du second découpage comptées | **vivant** (R-5) | TUÉ |
| X15 | sonde d'un créneau de trop | TUÉ (2) | |
| X17 | T0 à la dernière bougie de la sonde | vivant, équivalent sous lecture fixe (O-3) | vivant |
| X18 | motif DISCORDE selon l'ordre de lecture | TUÉ (1) | |
| Y01 | R-1 retirée | | TUÉ (test_sonde) |
| Y02 | R-2 retirée | | TUÉ (test_couverture) |
| Y03 | R-2 en forme F8' | | TUÉ (test_formes, pt 2) |

Sur la série : 18 mutants à moi (17, plus X05b qui remplace X05) : 13 TUÉS, 4 vivants (X05b et X17 équivalents ; X07 et X14,
trous de test), 1 FATAL (X05, non compté). Sur R, avec les réserves : X07 et X14 sont tués ; il ne reste vivants que les deux
équivalents déclarés. Y01 à Y03 retirent ou déforment les réserves : tous tués.

## 6. README (point 5)
Voir R-3. La sonde est dite sans son recul ; ses refus sont dits sans la condition « ni sondée » de (d). L-C13-2 et sa borne sont
dites conformément au rapport (32 cas, fenêtres de 1 à 10 minutes : vérifié sur les 32), mais sans préciser qu'il s'agit du
tirage du générateur. Les limites R-1 et R-2 ne sont pas écrites.

## 7. Écarts
- E-1 : un `du -sh` lancé sur ma copie d'étude `w`, dans le scratchpad (interdit par le brief). Il n'a affiché qu'un total, aucun nom
  de fichier.
- E-2 : la copie d'étude `w` a été extraite sans les exclusions du générateur. Aucun chemin interdit n'y a été lu ni listé par moi.
  Les rejeux ont été faits sur la copie A, avec exclusions, et `w` a été supprimée à 05:11 UTC.
- E-3 : mon mutant X05 ne terminait pas (borne, FATAL, non compté) ; il est remplacé par X05b.
- E-4 : `propose/R-1.diff` avait été régénéré pendant que la campagne de mutants portait une mutation de A. `git apply --check` l'a
  refusé ; le rejeu des jobs lancé sur R a été arrêté sans résultat ; les diffs ont été régénérés à partir de A restaurée.
- E-5 : mes premières formes de R-1 et R-2 ont échoué sur la série entière :
  - cas ajoutés après le cas « −23 » ;
  - F8' contraire au pt 2 ;
  - test R-2 en AttributeError sur la série.
  Corrigées, puis éprouvées de nouveau (§4).
- E-6 : `sleep` au premier plan (45 et 60 s) pour attendre les campagnes, avant de passer à des boucles bornées.
- E-7 : trois essais de ma propriété (`essai-300.tsv`, `essai-3000.tsv`, `essai-200.tsv`), faits avant de figer le tirage (bandes
  muettes plafonnées à une page, plage ciblée élargie, colonnes de classement), ne sont pas comptés.
- E-8 : outils retirés du dossier :
  - `fais_R1.py` et `fais_R2.py`, premières formes, remplacées par `fais_R.py` ; `fais_R1.py` était rendu invalide par une
    retouche en place ;
  - `rejeu.py`, écrit mais jamais lancé.
  Aucun résultat du rapport n'en dépend.
- E-9 : la machine est partagée avec d'autres agents (suites et mutants de dettes7 vus dans `ps`). Je n'ai eu qu'un
  processus lourd à la fois ; les durées des runs en portent la trace.
- E-10 : parmi les 6 jetons `chemin:ligne` extraits du bloc de la 9e vérification de xtask, un nomme un fichier sous
  `docs/rapports/`. Je n'en ai vu que le nom, extrait par filtre ; le fichier est absent de la copie (exclu) et n'a pas été lu.
  La violation retenue est le seul jeton porté par une ligne de violation (§4).

## 8. Journal de provenance (G1)
- [lu] (lu en entier ou dans les lignes citées, par moi) :
  - le brief (`22ab3f75…`) ; `formes-api/DECISION.md` en entier (ajouts jusqu'à 04:28:59) ; `RAPPORT-GENERATEUR.md` §13 et §14 ;
  - les diffs DT2-h à DT2-k en entier ;
  - dans l'état final : `socle.py`, `bougies.py`, `acquerir.py`, `README.md`, `parametres.json` (séries, historique, fenêtres) ;
    `tests/test_couverture.py`, `test_sonde.py`, `test_series.py`, `test_comptes.py`, `test_formes.py` (en-tête et cas),
    `test_formes_pages.py` (simulateur), `serveur.py`, `test_acquerir.py` (en-tête, `local`), `test_cli.py` (`banc`) ;
    `tau.completude` ;
  - `isole.sh` et `lo_up.py` (p1b) ; usage et sorties de `enforcement/verdict-suite-s2.py` ; `rust-toolchain.toml`,
    `.cargo/config.toml`, membres du `Cargo.toml` ;
  - `gates.yml` (lignes des jobs) ;
  - l'outil du générateur `propriete_c15.py`, après le lancement de ma propriété ; ses scripts `lourd-c15.sh`, `batterie2.sh`,
    `xtask-defaut.sh`, `matrice.sh` ;
  - ses sorties `propriete-c13-g*.out`, `propriete-c15-g*.out` et bilans, `batterie_c15A_docs.out`, `xtask-c15-*-verdicts.txt`
    (lignes VERDICT seules).
- [2nd] : aucun. Les chiffres du générateur sont recomptés sur ses sorties brutes, et les miens sur mes sorties.
- Non lus : aucune donnée de place de marché, aucune pièce de D.2, aucun chemin interdit, aucune ligne brute de xtask
  (lignes VERDICT et jetons `chemin:ligne` extraits par filtre, §4).
- Commandes et sorties : `NOTES.md` (horodaté), `echelle.out`, `bilan-*.out`, `compare-w-F108.out`, `gates/`, `rouges/`,
  `mutants-cc2*.tsv`, `echelle-avant.out`, `echelle-R12.out`, `compare-w-R12.out`, `gen-propriete-c15-g7.out`,
  `gen-propriete-c15-g12.out`,
  `xtask-verdicts.txt`, `xtask-SG9-chemins.txt`, `xtask-SG9-violation.txt`, `cargo-test-resultats.txt`, journaux
  `campagne-*.log`, `gates-*.log`, `suite-lourde.log`.
- Chiffres recomptés par script : tous ceux des §2 à §5 (aucun de seconde main).

## 9. Fichiers du dossier
`SHA256SUMS` (sha256 de chaque fichier rendu). Principaux fichiers rendus :
- `RAPPORT-CC.md` (ce rapport) et `NOTES.md` (journal horodaté) ;
- `propose/R-1.diff` (`eea88358…`, sur la série), `propose/R-2.diff` (`b8d5368d…`, sur R-1), `propose/R-5.diff` (`03ab4d2a…`,
  sur R-2). Ils sont à appliquer dans cet ordre par `git apply` ; empreinte de leur concaténation : `a98769c6…`. Éprouvés sur
  la série entière : job calib et matrice en code 0, Ran 77 ; docs conforme ;
- `outils/` : banc, propriété, bilans, lanceurs, mutants, fabrication des réserves ;
- sorties : `prop-*-g1[1-4].tsv` et `bilan-*.out`, `gates/`, `rouges/`, `mutants-cc2*.tsv`, `echelle*.out`,
  `gen-propriete-c15-g*.out`.

## Passe 2 : ajout daté du 2026-10-10 08:03:44 UTC (`date -u`)

**Gate 0** : `claude-opus-5-5` (inchangé). Demande : message de l'orchestrateur, passe 2 brève et complète sur DT2-p.
Lus [lu] avant tout travail :
- `formes-api/DECISION.md` (sha256 `43b9016f…`, 87 lignes), ajouts 06:25:41 et 07:00:12 ;
- `dettes2/RAPPORT-GENERATEUR.md` §15 (l. 938 à 1050 ; sha256 `cdc6fa80…` relevé à 07:50).

Horloge : début 07:00:58 ; ajout écrit à 08:03:44 ; base complétée à 08:04:55 (tête `d3d897b`) ; fin 08:05:11 UTC.

Base :
- **Copie B.** Tête du moment `01d74bdab065411f3ccf61d9e4b1147ab391954e`. La copie B est son `git archive`, chemins
  interdits exclus, plus DT2-a à DT2-p (`git apply` sans échec, `sha256sum -c` du lot vert).
- **Tête en fin de passe : `6e67309`** (DETTES-T6, autre acteur).
  - Rien n'a changé sous `scripts/calib-actifs`. Dans `gates.yml`, seule la ligne du job s2bis change (plancher
    344 → 356). L'index, modifié par un autre acteur, porte 358.
  - La série, appliquée sur le `git archive` de `6e67309` limité à ses deux chemins, donne un lot identique à celui de B
    (22 fichiers, `cmp`). L'examen vaut donc aussi à cette tête.
- **Tête relue à 08:04 : `d3d897b`** (DETTES-T6, autre acteur).
  - Rien n'a changé sous `scripts/calib-actifs`. `gates.yml` gagne un commentaire sur la forme des jobs (DT6-j), et
    la ligne s2bis passe à 358.
  - La série s'y applique, et le lot obtenu est identique : `SHA256SUMS` du lot `f9f7c0bf…`, `sha256sum -c` vert. La
    ligne du job calib est inchangée (`--plancher 78`).

### Verdict de la passe 2 : CONFORME-AVEC-RÉSERVES (R-6, R-7, R-8)

- **DT2-a à DT2-n** sont identiques à l'octet à ce que j'ai jugé ou écrit.
- **DT2-o** est vrai sur le code, sauf un compte, repris de mon rapport de passe 1 (R-7).
- **La garde de DT2-p** est juste, et suffisante pour ce qu'elle vise. Dans ma propriété, les 66 pertes « vers
  l'avant » deviennent des refus nommés, et 38 des 40 autres pertes aussi. Son coût est de 1 351 cas justes de la
  prémisse refusés, tous des fenêtres sans aucune minute échangée.
- **Deux trous de test**, chacun fermé par une réserve :
  - le bord de la garde n'est pas épinglé : quatre mutants non équivalents vivent (R-6) ;
  - la marge de R-2 n'est épinglée qu'à c = 1, alors que Bitfinex a c = 0 dans le lot (R-8, mutant P13).
- Avec R-6 à R-8, les 13 mutants de DT2-p sont tués. Tous les jobs sont verts, Ran 78 = plancher.

### P2-1. Identités (point 1)
- Empreinte de la concaténation de DT2-a à DT2-p dans l'ordre, recalculée :
  `a842a4341f43551fa5544a1259708990629642525235de6a93477f8faaf061bf` (conforme).
- DT2-a à DT2-k : identiques à l'octet à la série de ma passe 1 (`diffs-tete-dda4bbcc…/`, `cmp`, 11 sur 11).
- `cmp`, 3 sur 3 :
  - DT2-l est identique à `propose/R-1.diff` (`eea88358…`) ;
  - DT2-m à `R-2.diff` (`b8d5368d…`) ;
  - DT2-n à `R-5.diff` (`03ab4d2a…`).
- DT2-o : `fdf89c67…`, +13/−5. DT2-p : `00df0abd…`, +34/−8.

### P2-2. DT2-o, README (point 2)
Chaque point de R-3 est confronté au code de B :
- (i) **vrai.** Le recul des sondes (x_j = fin − ⌊pas/2⌋·2^j, puis dichotomie) est celui de `socle.sonde`. Écrit
  par DT2-l.
- (ii) **vrai.** « Aucune sonde non vide, que la fenêtre serve des bougies ou non » correspond à `bougies.serie`,
  condition `t0[1] or tous and tous[0] <= t0[0]`. Écrit par DT2-l.
- (iii) L-C13-2 :
  - **vrai** : « 32 cas sur 60 000 dans la propriété du générateur, fenêtres de 1 à 10 minutes, dont 23 à
    chevauchement 0, configuration absente des places du lot en couverture double (c = 1) ». Recompté en passe 1 ;
    dans `parametres.json`, Coinbase et Bitstamp sont en couverture 2 avec c = 1 ;
  - **vrai** : « 11 pertes de queue, fenêtres jusqu'à 27 minutes » ;
  - **faux pour un cas** : « 29 en marché mince (densité 0,3 ou moins, fenêtres jusqu'à 95 minutes) ». C'est R-7.
- (iv) **vrai.** Le miroir avant de L-C13-2 et le refus R-2 sont écrits par DT2-m. Le résidu écrit par DT2-o est
  exact (rejeu des cas 3654 et 3890, `rejeu-cas-p2.out`) : « 66 pertes vers l'avant ; 64 où rien n'est servi,
  1 miroir (fenêtre d'une minute), 1 en marché mince (densité 0,1 ; décalage de 58, fenêtre de 28) ». « La garde est
  au calcul » est vrai aussi (P2-3).
- **Renvois : aucun renvoi par numéro au README du lot.** Outil `outils/renvois_p2.py`, sortie `renvois-p2.out`, sur
  60 fichiers nommés un à un :
  - le lot ;
  - `JOURNAL.md` et `gates.yml` ;
  - 16 fichiers de `docs/adr-0029/g0-calib` et de `docs/adr-0029/calib`, listés par `git ls-files` sur ces deux
    chemins ;
  - DECISION.md, RAPPORT-GENERATEUR.md, et mes RAPPORT-CC.md, NOTES.md et BRIEF-CC.md.

  Le motif est écrit sans barre oblique inverse. Ses 10 occurrences sont toutes hors sujet : comptes de tests d'autres
  lots dans `JOURNAL.md`, statistiques de diff, un titre de section.

**Erratum de ma passe 1** (§1.4 (iii) et §2, « 29 en marché mince ») :
- les 29 pertes « autres » sont 28 pertes en marché mince (densité ≤ 0,3, fenêtres ≤ 95 minutes) et 1 perte à
  densité 1 ;
- ce cas est la graine 12, cas 3436 : Coinbase, pas 14, c 2, cpt g 90, fenêtre de 15 minutes. Les 11 requêtes des
  deux découpages ont leur dernière minute de cœur muette, et un long silence suit H0. La vérité compte 5 minutes
  échangées ;
- recompté sur `prop-w` et `prop-R12` ; mon propre bilan portait déjà les densités `{'0.03': 14, '0.1': 12, '0.3': 2,
  '1': 1}`.

DT2-o a repris mon compte ; R-7 le corrige.

### P2-3. DT2-p, revue complète (point 3)
**Code.** Lu ligne à ligne, dans `tau.calcul_actif`, l. 101 à 103 de B :
- `vides = [p for p in sorted(series) if all(x is None for x in closes[p])]` ;
- puis `CA/population : place sans minute active dans la fenêtre`, refus nommé par l'actif et par la première place
  vide de l'ordre trié.

**Juste.**
- `bougies.derniers` reporte la dernière clôture active. Une clôture vaut donc None jusqu'à la première minute active
  de la fenêtre, et jamais ensuite. « Toutes None » équivaut ainsi à « aucune minute active dans la fenêtre » : rien
  de servi, ou des minutes toutes sans échange.
- Le code `CA/population` existait déjà (`tau.places`).
- La garde vient après les clôtures de toutes les places, et avant `sigma.population`, `troisieme_terme` et
  `sigmas`, donc avant tout calcul. Vérifié (`verifie-R6.out`) : avec une place vide et BTC absents, c'est la garde
  qui refuse ; sans place vide, le refus est `CA/btc`.

**Suffisante pour ce qu'elle vise.**
- Elle contrôle toutes les places de la lecture de l'actif (`lec["places"]`), qui contiennent la population.
- Elle couvre aussi la fenêtre descriptive : `septembre` passe par `calcul_actif` et imprime le refus.
- Dans `tau.main`, le premier refus dans l'ordre des actifs arrête l'écriture. Hors de la garde, seuls `oracle_sh`,
  appelé avant elle, et la complétude, descriptive, lisent les séries, et rien n'est écrit en cas de refus.
- Sans la garde, j'ai mesuré l'effet sur le banc (P01 posé sur une copie, `sans-garde-p2.out`) :
  - ETH et USDT sont admis quelle que soit la place vidée ;
  - le σ des places horodatées passe de 180 à 90 s quand Coinbase est vidée ;
  - USDC est refusé par N_min.
  C'est conforme au §15 et à la docstring du test.

**Propriété rejouée.**
- Outil : `outils/propriete_cc2_p2.py` (`0f295c37…`), celle de la passe 1 plus le vrai `tau.calcul_actif` sur chaque
  série admise.
- Mêmes graines (11 à 14) et mêmes tirages : 24 000 cas (PID 19281, de 07:04:44 à 07:11:27).
- 0 ERREUR. Le verdict de chargement est identique à prop-R12 sur les 24 000 cas, et la garde est la seule cause de
  transition (`bilan-p2.out`, `bilan-p2-transitions.out`).
- **104 pertes deviennent des REFUS nommés de la garde** :
  - les 66 « vers l'avant » : les 64, le marché mince (graine 14, cas 3890) et le miroir (cas 3654) ;
  - 38 des 40 autres : 10 pertes de queue sur 11, et 28 « autres » sur 29.
- **Il reste 2 PERTE, partielles** (`rejeu-cas-p2.out`) :
  - graine 13, cas 4093 : cpt g 53, densité 0,3, fenêtre de 20 minutes ; 4 minutes échangées perdues sur 7 ;
  - graine 13, cas 5479 : retard variable, densité 0,3, fenêtre de 11 minutes ; 1 minute perdue sur 4.

  Dans les deux cas, la série admise garde une minute active. Elles sont donc hors de la garde par construction, et
  relèvent de mécanismes déjà écrits au README (L-C13-2, marché mince).
- **Cas justes de la prémisse refusés en plus : 1 351**, sur 7 947 cas à données complètes. Les refus sur données
  complètes passent de 3 791 à 5 142, et les JUSTE de 4 156 à 2 805.
  - Mécanisme unique : la vérité n'a aucune minute échangée dans la fenêtre. La garde ne peut pas distinguer ce cas
    d'une perte. Aucun des 2 555 cas JUSTE refusés par la garde n'a de vérité avec des minutes échangées.
  - Répartition :
    - fenêtre muette tirée : 477 ;
    - marché mince (densité ≤ 0,3) : 453 ;
    - silences aux densités 0,6 à 1 (bandes de fin de page, silence après H0) : 421.
  - Hors prémisse : 1 204 cas de plus, par le même mécanisme.
  - Ce sont des refus fermés, jamais des pertes. Sur les fenêtres du lot (91 et 30 jours, paires liquides), une place
    sans aucun échange sur toute la fenêtre n'est pas un cas de marché normal.

**Bord : « première minute sans échange : admise » n'est pas le bon bord.**
- Dans ce cas, kraken garde au moins 7 minutes actives sur 10 (`verifie-R6.out`). Le cas ne sépare que `all` de `any`
  (P02).
- Le bord exact est : **une seule minute active, la dernière, admise**. Toutes les clôtures valent alors None, sauf à
  la dernière minute. Ce cas tue P02, et aussi P08 (seuil de deux minutes actives), vivant sur la série.
- À l'inverse, une seule minute active en tête n'est pas un bord : `derniers` reporte sa clôture, et toutes les
  clôtures sont définies.

Le bord exact est ajouté par R-6.

**Mutants** : 13 mutants à moi, et le témoin.

Conditions des mutants :
- définitions dans `outils/mutants_p2.py`, lancement par `outils/mutants_run_p2.py` ;
- commande du job lue dans `gates.yml` de l'arbre : `python3 -B enforcement/verdict-suite-s2.py scripts/calib-actifs
  --aucun-saut --egal --plancher 78` ;
- un mutant à la fois, borne de 600 s, fichier restauré puis vérifié par sha256 ;
- classement selon le contrat du vérificateur : sortie 0 vivant, 1 tué, toute autre FATAL. Aucun FATAL ; Ran 78 à
  chaque run.

Arbres :
- B : la série ;
- C : la série + R-6 + R-7 ;
- T8 : la série + R-6 + R-7 + R-8.

| Mutant | Intention | B (série) | C (+ R-6 + R-7) | T8 (+ R-6 + R-7 + R-8) |
|---|---|---|---|---|
| M00 | témoin : aucune mutation (doit rester vivant) | vivant | vivant | vivant |
| P01 | garde retirée | TUÉ (1 échec) |  | TUÉ (1 échec) |
| P02 | refus dès une minute indéfinie (any) | TUÉ (1 échec) | TUÉ (1 échec) | TUÉ (1 échec) |
| P03 | refus seulement à deux places vides | TUÉ (1 échec) |  | TUÉ (1 échec) |
| P04 | code du refus changé | TUÉ (1 échec) |  | TUÉ (1 échec) |
| P05 | motif changé | TUÉ (1 échec) |  | TUÉ (1 échec) |
| P06 | place non nommée | TUÉ (1 échec) |  | TUÉ (1 échec) |
| P07 | actif non nommé | TUÉ (1 échec) |  | TUÉ (1 échec) |
| P08 | seuil de deux minutes actives au lieu d'une | vivant | TUÉ (1 échec) | TUÉ (1 échec) |
| P09 | dernière place vide nommée | vivant | TUÉ (1 échec) | TUÉ (1 échec) |
| P10 | série vide seulement (série toute sans échange admise) | TUÉ (1 échec) |  | TUÉ (1 échec) |
| P11 | dernière place (ordre trié) jamais contrôlée | vivant | TUÉ (1 échec) | TUÉ (1 échec) |
| P12 | garde après le calcul de σ (et non avant tout calcul) | vivant | TUÉ (1 échec) | TUÉ (1 échec) |
| P13 | marge de R-2 fixée à une minute au lieu de c (`bougies.py`) | vivant |  | TUÉ (1 échec) |

Case vide : mutant non rejoué sur cet arbre. Totaux :
- B : 14 runs, 8 tués et 6 vivants (M00 compris) ;
- C : 6 runs, 5 tués, M00 vivant ;
- T8 : 14 runs, 13 tués, M00 vivant ;
- aucun FATAL.

Lecture du tableau :
- **Sur la série**, 8 mutants sont tués par la commande du job (P01 à P07 et P10).
- **P08, P09, P11 et P12 sont non équivalents.** Chacun change le verdict sur une entrée du lot :
  - P08 : une seule minute active ;
  - P09 : deux places vides ;
  - P11 : okx vide, dernière place de l'ordre trié d'ETH ;
  - P12 : une place vide avec BTC absents (la garde n'est plus avant tout calcul).
- **P13 n'est équivalent que pour c = 1.** Or Bitfinex, paginée, a c = 0 dans `parametres.json`. Sous P13, une réponse
  dont la première bougie tombe à borne + 1 minute est admise, puis écartée par le filtre, sans refus. Le rouge est
  montré dans `rouges/rouge-R8.out` : `([], [], []) != APRES`.

### P2-4. Série complète (point 4)
Conditions :
- copie B (`outils/suite_p2.sh` ; sorties `gates/B2_*.out` et `cargo-test-p2-resultats.txt`) ;
- lignes exactes de `gates.yml`, un job à la fois ;
- sous `isole.sh`, variable et mandataires retirés, `PYTHONDONTWRITEBYTECODE=1`.

Épreuve des réserves : arbre T8 (`outils/suite_p2c.sh`, sorties `gates/T8_*.out`), égal à `var2/R678`.

| Job | B (série) | T8 (série + R-6 + R-7 + R-8) |
|---|---|---|
| calib-actifs, au texte de `gates.yml` (`--plancher 78`) | code 0, Ran 78 = plancher, conforme | code 0, Ran 78 = plancher, conforme |
| matrice 3.10, 3.11, 3.12, 3.13 en `-X dev -W error` | 4/4 code 0, Ran 78, 0 « Exception ignored », 0 « Warning » | 4/4 code 0, Ran 78, 0 « Exception ignored », 0 « Warning » |
| runner (`run-fixtures-verdict-suite-s2.py`) | 137 ok, 0 échec | — |
| controle | Ran 37, conforme | — |
| docs-sha256sums | conforme : 40 SHA256SUMS, 319 lignes (11 absentes admises, 4 fichiers non listés et non refusés) | conforme, mêmes comptes |
| `cargo --locked --offline test`, une fois, cible par défaut (`B/target`, `CARGO_TARGET_DIR` retirée) | code 0 en 16 s ; 28 lignes « test result », toutes ok : 269 passés, 0 échec, 0 ignoré | — |

Notes sur le tableau :
- Pour cargo, les erreurs de la crate `jouet` viennent du test `mutant_construction_en_echec_ne_rend_aucun_verdict`,
  qui la compile cassée exprès.
- Le générateur a compté 39 SHA256SUMS et 314 lignes sur `e5bf085`. L'écart vient de la tête : `01d74bd` porte les
  commits de DETTES-T6.
- Les réserves ne touchent que `scripts/calib-actifs`. Runner, controle et cargo n'en dépendent pas et n'ont pas été
  rejoués sur T8.

### P2-5. Réserves, forme exacte
Les trois diffs sont dans `propose/`. Ils s'appliquent dans l'ordre R-6, R-7, R-8, par `git apply`, sur la série a..p.
Empreinte de leur concaténation dans cet ordre :
`2da6d2f47322d012abd3917eef09c8756375fa2614c9a0e999d34d4ef65d8d4e`. Ils ne contiennent aucun octet 92, et aucune
ligne ajoutée ne dépasse 120 caractères.

- **R-6** (`propose/R-6.diff`, `a4ca9f69d926b9e215fa23d6e0e00608f515940e91a8ad1c7a0a360a12d8a124` ; 2 fichiers,
  +14/−3). Ajouts à `test_tau.test_place_vide` :
  - bord exact : kraken avec une seule minute active, la dernière, clôtures à 100, est admise (`dict`). La clôture 100
    évite `CA/borne` (E-P2-2) ;
  - okx vide, dernière place de l'ordre trié d'ETH : refus ;
  - binance et okx vides : refus nommé par binance ;
  - coinbase vide avec BTC absents : c'est la garde qui refuse, et non `CA/btc`.

  Le diff complète aussi la docstring et le `SHA256SUMS` du lot. Il tue P08, P09, P11 et P12, et P02 reste tué. Ran
  reste à 78.
- **R-7** (`propose/R-7.diff`, `afd84c807e0d5349259d9bfb1247f2149239ff5f9cdfb82cf57f67f3e509a52d` ; 2 fichiers,
  +6/−5). README, phrase de L-C13-2. « et 29 en marché mince (densité 0,3 ou moins, fenêtres jusqu'à 95 minutes) »
  devient : « et 29 autres hors de ce compte : 28 en marché mince (densité 0,3 ou moins, fenêtres jusqu'à 95 minutes)
  et 1 à densité 1 dont toutes les fins de page des deux découpages sont muettes (fenêtre de 15 minutes, 5
  échangées) ». Le diff met aussi à jour le `SHA256SUMS` du lot.
- **R-8** (`propose/R-8.diff`, `1a638e23283d99a80377a0b53144604645bff6952ac1f6f93da3f67e573286ba` ; 2 fichiers,
  +6/−1). Ajout à `test_couverture.test_double_couverture` d'un cas dans la configuration de Bitfinex :
  - couverture simple, chevauchement 0, fenêtre d'une page de 15 minutes sans échange, décalée d'une minute vers
    l'avant ;
  - la page 0 ne sert que la minute 15, après sa borne (14) + c (0) : `APRES`, refus nommé.

  Le diff complète aussi la docstring et le `SHA256SUMS` du lot. Le test est vert sur l'arbre muni de R-8
  (`var2/R678`) et rouge sous P13 (`rouges/rouge-R8.out`). Il tue P13, et Ran reste à 78.

Épreuve sur T8 (série + R-6 + R-7 + R-8) :
- jobs : P2-4 ;
- mutants : les 13 sont tués, M00 reste vivant (P2-3).

### P2-6. Observations, sans réserve
- **O-P2-1.** Les 2 pertes partielles restantes (P2-3) relèvent de L-C13-2 et du marché mince, tels que le README les
  écrit au chargement. Ce texte reste exact.
- **O-P2-2.** Le cas 3436 a c = 2, configuration absente des places du lot en couverture double. R-7 ne le dit pas, ce
  qui ne fausse pas sa phrase.

### P2-7. Écarts de la passe 2
- **E-P2-1.** `outils/suite_p2.sh` a été arrêté à l'étape (4), l'arbre C à refaire après le changement de R-6. Ses
  processus ont été tués par groupe ; aucun résultat de cette étape n'est compté.
- **E-P2-2.** La première forme de R-6 était fausse : avec une clôture à 1 sur la seule minute active, l'écart aux
  autres places est de 99 %, d'où `CA/borne`.
  - Le job calib de l'ancien arbre C est sorti en code 1 (`test_place_vide`).
  - `gates/C2_m3.10.out`, même arbre, porte le même échec (Ran 78, `FAILED`). Il est gardé comme trace et n'est pas
    compté.
  - La forme a été corrigée (clôture 100), puis éprouvée sur C, puis sur T8.
- **E-P2-3.** `gates/C2_calib.out`, sortie de ce job raté, a été supprimé avant la relance. Son contenu utile est
  consigné dans `NOTES.md`.
- **E-P2-4.** J'ai lancé `find -name __pycache__ -maxdepth 2` sur ma copie `C/scripts/calib-actifs` (le lot seul). La
  sortie était vide.
- **E-P2-5.** Dans `bilan-p2-transitions.out`, la colonne d'exemples est indexée par la seule cause. Elle est donc
  commune aux lignes « prémisse » et « hors prémisse ». Les comptes n'en dépendent pas.
- **E-P2-6.** À 07:27, j'avais noté P13 « équivalent pour c = 1 » sans vérifier les c du lot. La correction est R-8.
- **E-P2-7.** La mesure des renvois faite à 07:07 par `git grep` limité à une liste de chemins n'a pas son motif
  consigné. Elle est remplacée par `outils/renvois_p2.py`, rejouable.
- **E-P2-8.** Un premier recompte des lignes des diffs a été tapé avec des barres obliques inverses dans un motif awk,
  contre la règle du gabarit. Il a été refait en Python sans barre, avec les mêmes comptes. Les outils `fais_R6.py` et
  `fais_R8.py` portent des barres (guillemets triples échappés dans des chaînes Python) ; le contrôle porte sur les
  octets produits : `R-6.diff` et `R-8.diff` sans octet 92, texte attendu.

### P2-8. Journal de provenance (G1), passe 2
- [lu] :
  - DECISION.md (ajouts 06:25:41 et 07:00:12) et RAPPORT-GENERATEUR.md §15 ;
  - DT2-o et DT2-p en entier ;
  - dans B : `tau.py` (`calcul_actif`, `septembre`, `main`), `bougies.py` (`derniers`, `serie`, `charger`, `_sonde`),
    `sigma.population`, `parametres.json` (séries), `tests/test_tau.py` (`test_place_vide`),
    `tests/test_couverture.py` en entier, README l. 25 à 75.
- [2nd] : aucun. Tous les chiffres sont recomptés par script sur mes sorties.
- Non lus : aucune donnée de marché, aucune pièce de D.2, aucun chemin interdit, aucun `*.jsonl`. xtask n'a pas été
  relancé : il n'est pas dans la liste du point 4.
- Commandes et sorties :
  - `NOTES.md` (horodaté) ;
  - propriété : `prop-p2-g11.tsv` à `prop-p2-g14.tsv`, `essai-p2-300.tsv` (essai non compté), `campagne-p2.log`,
    `bilan-p2.out`, `bilan-p2-transitions.out`, `rejeu-cas-p2.out` ;
  - contrôles : `verifie-R6.out`, `sans-garde-p2.out`, `renvois-p2.out`, `renvois-p2-liste.txt` ;
  - suites et jobs : `suite-p2.log`, `suite-p2b.log`, `suite-p2c.log`, `gates/B2_*`, `gates/C3_*`, `gates/T8_*`,
    `cargo-test-p2-resultats.txt` ;
  - mutants et rouges : `mutants-p2.tsv`, `mutants-p2-C.tsv`, `mutants-p2-T8.tsv`, `rouges/rouge-R8.out`.
- Nettoyage à 08:03:15 UTC :
  - copies B (avec `B/target`), C, T8 et `var2/` supprimées ;
  - sortie brute de cargo test supprimée ; seules ses lignes « test result » et d'erreur en avaient été extraites ;
  - brouillons de cet ajout supprimés après son écriture, puis `tmp/` retiré ;
  - aucun processus cc2 restant.

### P2-9. Fichiers ajoutés
- `propose/R-6.diff`, `propose/R-7.diff`, `propose/R-8.diff` ;
- dans `outils/` : `propriete_cc2_p2.py`, `bilan_p2.py`, `campagne_p2.sh`, `copie_p2.sh`, `suite_p2.sh`,
  `suite_p2b.sh`, `suite_p2c.sh`, `cargo_test_p2.sh`, `mutants_p2.py`, `mutants_run_p2.py`, `fais_R6.py`, `fais_R7.py`,
  `fais_R8.py`, `verifie_R6.py`, `rejeu_cas_p2.py`, `renvois_p2.py`, `table_mutants_p2.py` ;
- les sorties citées en P2-8.

Le `SHA256SUMS` du dossier est régénéré en fin de passe, et `sha256sum -c` est vert.

## Ligne datée du 2026-10-10 08:11:32 UTC (`date -u`) : R-9

Demande : DECISION.md, ajout daté du 2026-10-10 08:06:21 UTC (lu ; sha256 `78c413ac…`).

- **Forme.** `propose/R-9.diff` (`2f678f385928e64145d7a753fc8a1793a11a72613714e04b7bdf73002cab5481` ; 2 fichiers,
  +13/−1) s'applique après R-8 sur la série a..p. Elle porte deux ajouts au README et met à jour le `SHA256SUMS` du
  lot :
  - (i) 7 lignes à la ligne de `tau.py`, après la garde `CA/population` : le coût de la garde (refus fermé et nommé,
    jamais une perte), ses comptes (1 351 cas justes de la prémisse, de 3 791 à 5 142 refus sur 7 947) et leur
    ventilation (477, 453, 421), puis la plausibilité pour les places du lot ;
  - (ii) 5 lignes sous L-C13-2 : les 66 et 38 des 40 pertes deviennent des refus nommés ; restent 2 pertes
    partielles (graine 13, densité 0,3).
  Aucun octet 92 ; aucune ligne du README ne dépasse 119 caractères.
- **Épreuve de R-6 à R-9 ensemble.** Arbre T9 : 01d74bd + DT2-a..p + R-6 + R-7 + R-8 + R-9 (`git apply --check`
  puis `apply`, sans échec).
  - Le lot passe `sha256sum -c` : `SHA256SUMS` `ef7f1063…`, README `57ee4f91…`.
  - Job calib-actifs : code 0, Ran 78 = plancher, conforme.
  - docs-sha256sums : conforme (40 SHA256SUMS, 319 lignes).
  - Empreinte de la concaténation R-6, R-7, R-8, R-9 :
    `b6c0d5c710bbd828cca6ab19ef303b0197fcc806c36aceec821f482780015141`.
- **Écarts entre la demande et le texte écrit**, tous vérifiés :
  - « 87 pages ou plus par découpage » ne vaut que pour Coinbase et Bitstamp (`fenetres-lot.out` : Bitstamp, 87 et 88
    pages sur 30 jours). Bitfinex n'a que 27 et 9 pages ; Binance, Kraken et OKX ne sont pas paginées. R-9 écrit
    donc : « paires liquides sur des fenêtres de 91 et de 30 jours (87 pages ou plus par découpage pour Coinbase et
    Bitstamp) » ;
  - les 2 pertes partielles gardent chacune 3 minutes actives : au moins une, ce qui suffit à passer la garde ;
  - le groupe de 421 compte 7 fenêtres sans aucune bande muette (densité 0,6, fenêtres de 1 à 3 minutes), vides
    par le seul tirage. R-9 le dit.
- **Erratum de P2-3.**
  - Au lieu de « silences aux densités 0,6 à 1 : 421 », lire : 421 à densité de 0,6 à 1, par bandes muettes ou
    silence après H0, sauf 7 vides par le tirage.
  - Au lieu de « garde une minute active », lire « garde des minutes actives (3 chacune) ».
- **Nettoyage.** Copies U, T9 et `var3/` supprimées ; aucun processus restant ; aucune écriture git.
- **Fichiers ajoutés.** `propose/R-9.diff`, `outils/fais_R9.py`, `outils/fenetres_lot.py`, `fenetres-lot.out`,
  `gates/T9_calib.out` et `gates/T9_docs.out`.
  Le `SHA256SUMS` du dossier est régénéré.
