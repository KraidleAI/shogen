# Loi de rotation de la règle R1-2 (S2-bis) : contrat d'entrée et de sortie, vecteurs

- **Rattachement** : ADR-0029 §2.4 c (l.135-141 : rotations circulaires sur la suite comprimée, R, seuil, graine,
  masques de bits) et §2.7 pts 2, 4 et 9 (l.200, l.202, l.212) ; G0 des lots COLLECTE-BIS, RECALC-BIS et DEPLOI-BIS
  (`docs/adr-0029/g0-collecte/`), exigences E-R-16 à E-R-18 de la PROPOSITION, réponse de l'AVIS à la question Q-R-02
  (encodage de l'entrée de SHA-256, sens du décalage, vecteurs au paquet) ; sous-lot RB-6.
- **Usage** : code de référence `s2bis/shogen_s2bis/recalc/rotation.py`. Ce contrat est celui de l'oracle croisé du lot
  SIM-BIS (G0 `docs/adr-0029/g0-sim/`, exigence E-S-51, sous-lot SB-13) : o(r, u) et K^(r) égaux sur les vecteurs du §4
  et sur des séries synthétiques.
- **Statut** : texte tenu à jour avec le code ; scellé au paquet de S2-bis avec le commit du recalcul (les vecteurs y
  entrent, AVIS Q-R-02).

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
6. **Unité u** : nom d'hôte de configuration (E-R-15), chaîne non vide de caractères ASCII imprimables (0x20 à 0x7E),
   sans « : », le séparateur de l'entrée (AVIS Q-R-02, complément (3)).

## 2. Décalages

1. **o(r, u)** : entier big-endian des 32 octets de SHA-256 appliqué aux octets UTF-8 de la chaîne ASCII
   `<graine>:<strate>:<r>:<u>`, réduit modulo n en arithmétique exacte. La classe n'entre jamais dans l'entrée :
   toutes les séries d'un même hôte sont décalées du même pas (rotations jointes par hôte, l.200). Un décalage nul est
   admis.
2. **Sens** : la valeur de la position t va en (t + o) mod n, soit D′(t) = D((t − o) mod n). Sur un masque de n bits
   (bit t = valeur de la position t), le masque décalé vaut ((m << o) | (m >> (n − o))) & (2^n − 1) : fonction
   `tourner(m, o, n)`.

## 3. Refus nommés de `decalage(graine, strate, r, u, n)`

Toute entrée hors du §1 lève `RefusRotation`, avant tout calcul : `ROTATION/graine` (autre chose que 64 hexadécimaux
minuscules en chaîne), `ROTATION/strate`, `ROTATION/n` (entier n ≥ 1, booléen refusé), `ROTATION/r` (entier de 1 à
9 999, booléen et chaîne refusés), `ROTATION/unite`.

## 4. Vecteurs, calculés hors du code

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
avec n′ = n/2.
