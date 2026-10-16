# Gabarits de rapport : règles de remplissage

Versé le 2026-10-15 (`date -u`, lot PRODUIT-R2, R2-b). Rattachement : ADR-0028 §4 pt 7 (envergure) et D9 ;
`docs/adr-0028/AVIS-PRODUIT-APRES-S2.md` §3 (produit minimal vendable : le rapport de concentration d'infrastructure de
livraison pour un pool nommé par un client) et §4 ; doc 04 §3 et §4 ; doc 09 en entier.

| fichier | objet |
|---|---|
| `RAPPORT-CONCENTRATION-POOL.md` | gabarit en français (le français fait foi) |
| `RAPPORT-CONCENTRATION-POOL-EN.md` | même gabarit en anglais, mêmes champs |

## Champs

Un champ s'écrit entre chevrons, sous la forme type point nom. Le type dit d'où vient la valeur :

- `sha256`, `commit`, `date`, `version` : une empreinte (64 chiffres hexadécimaux minuscules), un commit (40), une date
  UTC lue par `date -u` (forme `AAAA-MM-JJTHH:MM:SSZ`), une version de Python (forme `x.y.z`) ;
- un type qui est aussi le nom d'un champ `sha256` (ainsi `rendu`) : la valeur est recopiée, ligne pour ligne, de la
  pièce dont ce champ porte l'empreinte, à la sortie que le gabarit nomme par `chemin:ligne` ;
- `libre` : une déclaration du client (rang R3) ou une phrase du rédacteur.

## Règles

1. Le texte fixe du gabarit se garde à l'octet ; un rapport n'ajoute ni ne retire aucune phrase hors des champs. Les
   champs sont tous remplis, ou tous vides (gabarit) ; un champ répété porte partout la même valeur.
2. Aucun mot interdit de doc 09 (l.10-55), dans le texte comme dans les valeurs, recopies comprises ; la formulation
   correcte est celle de la troisième colonne de doc 09.
3. Aucun nombre sans sa source. Un champ de pièce recopie la pièce sans arrondi ni reformulation ; un champ `libre` qui
   porte un chiffre cite, sur la même ligne, l'empreinte d'une pièce du gabarit, avec la ligne si elle est connue
   (forme `[sha256.rendu l.12]`, ou `[sha256.rendu l.12-14]` pour une plage).
4. Aucune prétention R1 tant que S2-bis n'a pas rendu : ni les blocs 3 et 4 du rendu, ni les drapeaux du bloc 6, ni
   aucune phrase sur la co-défaillance des flux ; k_eff n'est jamais lu comme un compte d'indépendance.
5. La liste des axes non mesurés (§5 du gabarit) est un champ non optionnel (doc 04 l.129-139) : le champ propre au pool
   nomme au moins les hôtes non attribués et les flux retirés par D1, ou écrit qu'il n'y en a aucun.
6. Aucune phrase réglementaire (DORA, MiCA) : aucun texte n'est détenu au registre `biblio/` (AVIS-PRODUIT-APRES-S2 §3).

## Contrôle

```bash
python3 -B scripts/publication/gabarit_controle.py docs/publication/gabarits/RAPPORT-CONCENTRATION-POOL.md "$RAPPORT"
```

Sortie 0 : conforme ; 1 : refus, motifs sur la sortie d'erreur ; 3 : erreur (gabarit malformé, doc 09 dont une ligne
ancrée a changé). Le contrôle mécanise les règles 1, 2 (sous-ensemble ancré de doc 09), 3 et 4 (champs `libre`, jeton
`R1` en capitales seul : une phrase sur la co-défaillance qui ne l'écrit pas passe) ; il ne
juge ni le contexte d'une phrase, ni l'égalité d'une valeur à sa pièce, ni un nombre écrit en lettres (il ne lit que
les chiffres). La relecture humaine du rapport reste due (doc 09, règle d'application), par un réviseur qui n'a pas
rempli le rapport.

## Limites

- Le harnais ne collecte que le pool figé de S2 (`s2-harness/shogen_s2/sources.py`, `SPECS`) et ne porte que les arêtes
  `basis:doc` de ce pool : un pool client demande un lot rattaché ; sans lui, aucun gabarit ne se remplit.
- Un rapport rempli n'est ni publié ni vendu par son rédacteur : publication et vente restent des décisions de
  l'investisseur (ADR-0028 §4 pt 4 et pt 7, D9).
- L'alignement du rapport sur le gabarit cherche chaque texte fixe à sa première occurrence : une valeur qui contient le
  texte fixe suivant fait refuser le rapport (refus, jamais une acceptation).
