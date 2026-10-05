# Loi de rotation de la règle R1-2 (S2-bis) : contrat d'entrée et de sortie, vecteurs

- **Rattachement** : ADR-0029 §2.4 c (l.135-141 : rotations circulaires sur la suite comprimée, R, seuil, graine,
  masques de bits) et §2.7 pts 2, 4 et 9 (l.200, l.202, l.212) ; G0 des lots COLLECTE-BIS, RECALC-BIS et DEPLOI-BIS
  (`docs/adr-0029/g0-collecte/`), exigences E-R-16 à E-R-18 de la PROPOSITION, réponse de l'AVIS à la question Q-R-02
  (encodage de l'entrée de SHA-256, sens du décalage, vecteurs au paquet) ; sous-lot RB-6.
- **Usage** : code de référence `s2bis/shogen_s2bis/recalc/rotation.py`. Ce contrat est celui de l'oracle croisé du lot
  SIM-BIS (G0 `docs/adr-0029/g0-sim/`, exigence E-S-51, sous-lot SB-13) : o(r, u) et K^(r) égaux sur les vecteurs du §5
  et sur des séries synthétiques.
- **Statut** : texte tenu à jour avec le code ; scellé au paquet de S2-bis avec le commit du recalcul (les vecteurs y
  entrent, AVIS Q-R-02). La règle elle-même (garde d'information, valeur par strate, séquence d'ETH) relève du sous-lot
  RB-7 ; ce module ne rend aucune valeur de la règle.

## 1. Entrées

1. **Graine** : 64 chiffres hexadécimaux minuscules, la forme imprimée au README du sceau du sha256 du manifeste scellé
   (l.200 ; annexe D.4 c d'ADR-0028 ; E-R-19). L'entrée de SHA-256 porte cette forme imprimée, non ses 32 octets.
2. **Strate** : `calme` ou `stress`, rien d'autre (AVIS Q-R-02, complément (1)).
3. **n** : entier, n ≥ 1, longueur de la suite comprimée des fenêtres évaluables retenues de la strate : n_s, ou n′_s au
   cas du §2.3 de l'ADR ; pour l'analyse conditionnelle (Q-R-11), la longueur de la sous-suite (AVIS Q-R-02,
   complément (4)). Le module ne reçoit que cette longueur.
4. **Position** : t = 0, 1, …, n − 1, rang de la fenêtre dans la suite comprimée, en ordre chronologique (t = 0 pour la
   première fenêtre retenue).
5. **r** : entier de 1 à 9 999, écrit en décimal sans zéro de tête (AVIS Q-R-02, complément (2)).
6. **Unité u** : nom d'hôte de configuration (E-R-15), en minuscules : lettres a à z, chiffres, « - » et « . », de 1 à
   253 caractères (constante `HOTE` du module, appliquée aussi par le chargeur `config_analyse`) ; donc ni « : », le
   séparateur de l'entrée (AVIS Q-R-02, complément (3)), ni espace, ni majuscule. Resserrement du complément (3),
   adjugé par l'orchestrateur le 2026-10-05 (Q-RB-13 de la relecture G2 de la tranche 1 de P3).
7. **Séries** : `classes` = {classe : {unité : masque}} ; le masque d'une unité est un entier, 0 ≤ masque < 2^n, dont le
   bit t vaut D(u, t), l'indicatrice d'écart consolidé au quorum de la fenêtre de rang t (§2.2 de l'ADR ; construite aux
   sous-lots RB-3 à RB-5).
8. **Première unité** : `premiere`, le premier hôte du pool BTC D1-bis de la strate, ou None. Elle n'est décalée dans
   aucune classe ; si elle manque à une classe, toutes les unités de cette classe sont décalées (l.200). *Précision de
   l.200 (Q-RB-5, adjugée le 2026-10-05)* : « ordre alphabétique » s'entend comme l'ordre strict des points de code
   (octets ASCII) des noms d'hôte de la configuration, celui que le chargeur exige de chaque liste d'unités
   (`unites-ordre`) ; ainsi un nom `api-x` précède un nom `api.y` (0x2D < 0x2E). La première unité effective de chaque
   strate dépend du pool D1-bis (sous-lot RB-7) : elle sera imprimée au rendu (item pour le sous-lot RB-15).
   *Précision de l.200 (Q-T3-15 de l'avis AVIS-SIM-T3, modifiée, adjugée par l'orchestrateur le 2026-10-05, avant
   E0)* : le pool BTC D1-bis de la strate est celui qui reste après les retraits D1-bis (a) et (b) et le seuil de flux
   presque mort (l.170) ; la première unité y est prise avant le critère collectif d'absorption candidat (E-S-35 de
   SIM-BIS, Q-S-15) et n'est pas recalculée après lui : si ce critère la retire d'une classe, elle manque à cette classe
   et toutes les unités de la classe sont décalées ; pool vide : None, toutes les unités sont décalées. Le module ne fait
   aucun retrait : il reçoit `premiere` ainsi prise (sous-lot RB-7).
9. **R et seuil** : paramètres de `lois`, R de 1 à 9 999 et seuil entier ≥ 0 (tests, oracle croisé). Au paquet, ils
   viennent du bloc `rotations` de `s2bis/config/analyse.json`, où le chargeur exige R = 9 999 et seuil = 99
   exactement (Q-RB-6), la cohérence (99 + 1)/(9 999 + 1) = 0,01 (l.202) restant contrôlée en seconde garde.

## 2. Décalages

1. **o(r, u)** : entier big-endian des 32 octets de SHA-256 appliqué aux octets UTF-8 de la chaîne ASCII
   `<graine>:<strate>:<r>:<u>`, réduit modulo n en arithmétique exacte. La classe n'entre jamais dans l'entrée :
   toutes les séries d'un même hôte sont décalées du même pas (rotations jointes par hôte, l.200). Un décalage nul est
   admis. Fonction `decalage(graine, strate, r, u, n)`.
2. **Sens** : la valeur de la position t va en (t + o) mod n, soit D′(t) = D((t − o) mod n). Sur un masque de n bits,
   le masque décalé vaut ((m << o) | (m >> (n − o))) & (2^n − 1) : fonction `tourner(m, o, n)`.

## 3. Lois de K et de S : `lois(graine, strate, n, classes, premiere, R, seuil)`

Pour chaque classe, m_t = Σ_u D(u, t) sur les unités de la classe :

1. **K** = #{t : m_t ≥ 2} (fenêtres à au moins deux écarts, l.120) ; **S** = Σ_t C(m_t, 2) (paires d'unités en écart dans
   une même fenêtre, l.212), calculée comme la somme, sur les paires d'unités, des fenêtres où les deux sont en écart.
2. Pour r = 1 … R, les séries décalées de o(r, u) (§2) donnent K^(r) et S^(r) ; `K_r[r − 1]` = K^(r), `S_r[r − 1]` =
   S^(r).
3. **C** = #{r : K^(r) ≥ K} ; **K_crit** = le plus petit entier k ≥ 0 tel que #{r : K^(r) ≥ k} ≤ seuil, soit la valeur
   de rang seuil + 1 de la loi rangée en ordre décroissant, plus un (0 si seuil ≥ R) ; **K_moyen** = Σ_r K^(r)/R en
   rationnel exact (`fractions.Fraction`), le K̄_rot de l.200.
4. **C_S**, **S_crit** et **S_moyen** de même sur la loi de S, avec les mêmes r (l.212). S_crit suit la définition de
   K_crit, l'ADR ne la donnant pas.
5. Sortie : {classe : {"K", "C", "K_crit", "K_moyen", "K_r", "S", "C_S", "S_crit", "S_moyen", "S_r"}}, classes dans
   l'ordre trié de leurs noms. La décision C ≤ seuil et ses gardes sont au sous-lot RB-7.

Aides publiques : `compter(masques)` rend (K, S) d'une liste de masques ; `resume(x, loi, seuil)` rend (C, x_crit,
moyenne).

## 4. Refus nommés

Toute entrée hors du §1 lève `RefusRotation`, avant tout calcul : `ROTATION/graine` (autre chose que 64 hexadécimaux
minuscules en chaîne), `ROTATION/strate`, `ROTATION/n` (entier n ≥ 1, booléen refusé), `ROTATION/r` (entier de 1 à
9 999, booléen et chaîne refusés), `ROTATION/unite` (nom d'unité ou première unité), `ROTATION/R` (R de 1 à 9 999 ou
seuil négatif), `ROTATION/classes` (pas un dictionnaire de dictionnaires, ou nom de classe non textuel),
`ROTATION/masque` (masque négatif, booléen, ou au-delà de n bits).

## 5. Vecteurs, calculés hors du code

Graine de test : `6fce4df75bac7db6ff01817b407f6331e49ec2ebf31f02e6672d3ab8a3bc9688`, sha256 de la chaîne ASCII
`SHOGEN-RB6-VECTEURS`. Pour chaque ligne : `printf '%s' "<graine>:<strate>:<r>:<u>" | sha256sum`, puis l'empreinte,
écrite en majuscules, convertie en entier et réduite par `bc` (`ibase=16; x=<EMPREINTE>; ibase=A; x % <n>`). Aucun
Python dans ce calcul (journal G1 du sous-lot RB-6a ; script `vecteurs_rb6.sh`).

| strate | r | u | n | sha256 de l'entrée | o |
|---|---|---|---|---|---|
| calme | 1 | api.binance.com | 109 440 | `d7916cde6fb849bd1c4b44da609ecc6dc266f916228d974ec2d4c9354c235a07` | 107 527 |
| stress | 9 999 | ethereum-rpc.publicnode.com | 43 776 | `d4930a57b959d5b5551b5b74f7aeeb723cd829af5450a097f5e241e201eefba1` | 24 225 |
| calme | 4 242 | api.kraken.com | 54 720 | `e8e92c3a1c9ab48898bf83759e04ae158eb5eea32f952b1e652b08d520c64b7f` | 39 743 |
| calme | 1 | api.coinbase.com | 7 | `c6c0e4bc41e6eb4637c15e222e4d568d07f525e8d08e090c3d5395b9bc05c1a0` | 0 |
| calme | 7 | api.coinbase.com | 7 | `55a70a48e10570c44642dc4cc76ae8f059c5c8eac1c5d3e03ea9d23d5234d47e` | 6 |
| calme | 1 | api.binance.com | 54 720 | `d7916cde6fb849bd1c4b44da609ecc6dc266f916228d974ec2d4c9354c235a07` | 52 807 |

La quatrième ligne donne o = 0 et la cinquième o = n − 1 (AVIS Q-R-02) ; la sixième reprend l'entrée de la première
avec n′ = n/2. Les lois K^(r) et S^(r) sont contrôlées contre un comptage position par position écrit dans les tests
(`tests/test_rotation.py`, o recalculé par le test), sur des séries tirées au hasard et pour R = 9 999.

## 6. Coût mesuré

Masques synthétiques de densité 0,005 par fenêtre et par unité, R = 9 999, hôte de session partagé (charge moyenne
d'environ 3 sur 4 cœurs), journal G1 du sous-lot RB-6b, script hors dépôt `cout_rb6.py` :

| interpréteur | calme (n = 109 440), une classe de 10 unités | calme, quatre classes (10, 8, 6, 6) | stress (n = 43 776), une classe | stress, quatre classes |
|---|---|---|---|---|
| Python 3.12.3 | 7,5 s | 17,2 s | 2,5 s | 6,1 s |
| Python 3.10.20 | 6,7 s | 15,7 s | 2,2 s | 5,7 s |

Les deux interpréteurs rendent les mêmes K, C et K_crit ; la loi de BTC est la même, calculée seule ou jointe aux trois
autres classes. Les deux strates et les quatre classes font environ 23 s ; les huit sensibilités de l.212, si chacune
refait toutes les rotations, multiplient ce coût par au plus neuf : quelques minutes pour le rendu, bibliothèque
standard seule.

## 7. Limites

1. Le module ne reçoit que la longueur n de la suite retenue : la confusion entre n_s et n′_s ne peut s'y écrire ; elle
   se contrôle là où les deux valeurs coexistent (sous-lot RB-7), où le mutant obligatoire « modulo n_s au lieu de
   n′_s » (PROPOSITION §3.4) est dû (Q-RB-14).
2. La construction des masques (suite comprimée, n_s premières fenêtres évaluables, écarts consolidés) relève des
   sous-lots RB-3 à RB-5 ; ce contrat suppose des masques déjà construits.

## 8. Cohérence avec SIM-BIS (SB-7, SB-13)

Points tenus des deux côtés pour que l'oracle croisé (E-S-51) compare o(r, u) et K^(r) à l'octet (Q-RB-12, d'après
l'AVIS de la tranche 1 de P3, §2 ; adjugé le 2026-10-05) :

1. **Positions** : le bit t d'un masque est la position t de la suite comprimée, rang chronologique 0, 1, … (§1 pts 4
   et 7) ; c'est la convention de la compression de SIM-BIS (`scripts/sim-bis/calendrier.py`, `comprimer` : bits aux
   fenêtres retenues, dans l'ordre, en positions 0, 1, …).
2. **Identifiants des unités** : u est le nom d'hôte de configuration (§1 pt 6), jamais un nom court. SIM-BIS tient ses
   hôtes en noms courts (`sources.indices_hotes` de `scripts/sim-bis/parametres.json`) : l'oracle croisé hache les noms
   d'hôte, par la table scellée de correspondance de l'item SHOGEN-SIM-BIS-INDICES-IDENTIFIANTS-1 (annexe B d'ADR-0028).
3. **Première unité** : la règle du §1 pt 8 (ordre strict des points de code des noms d'hôte de la configuration), la
   même des deux côtés.
4. **R et seuil** : paramètres de `lois` (§1 pt 9) ; l'oracle compare à R égal, à R = 999 comme à R = 9 999.
5. **Libellés de strate** : `calme` et `stress` (§1 pt 2), ceux de `calibration.strates` de
   `scripts/sim-bis/parametres.json`.
6. **Masques** : 0 ≤ masque < 2^n (§1 pt 7) ; `ROTATION/masque` refuse tout masque de plus de n bits (§4) : SIM-BIS
   fournit des masques tronqués à n bits, ce que sa compression fait par construction.
