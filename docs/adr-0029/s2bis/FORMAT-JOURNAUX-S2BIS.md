# Format des journaux d'observateur de S2-bis

- **Rattachement** : ADR-0029 §2.9 (l.238-240 : journal à enregistrement unique, chaîné, `fsync` au marqueur, point de
  contrôle horaire, fichiers quotidiens clos et sommés ; format spécifié et scellé au paquet) ; PROPOSITION du G0
  (`docs/adr-0029/g0-collecte/`), exigences E-C-16 à E-C-24 ; principe de SHOGEN-FORMAT-JOURNAUX-1 (annexe B d'ADR-0028,
  l.55).
- **Statut** : texte tenu à jour à chaque sous-lot du collecteur ; il est scellé au paquet de S2-bis avec le commit du
  collecteur. Code de référence : `s2bis/shogen_s2bis/collecte/journal.py`. Le test de conformité d'un journal produit
  par le collecteur entier (E-C-24) est celui du sous-lot CB-18.

## 1. Ligne et chaîne (CB-1)

1. Un journal est une suite de fichiers en UTF-8. Chaque enregistrement occupe une ligne terminée par l'octet 0x0A
   seul. Un lecteur découpe sur cet octet, et sur lui seul : les caractères U+2028 et U+2029 peuvent figurer dans une
   chaîne.
2. Chaque ligne est un objet JSON **canonique** : clés triées par point de code, séparateurs `,` et `:` sans espace,
   caractères hors ASCII écrits en UTF-8 (jamais en séquence `\u`), aucun nombre à virgule ni NaN (valeurs exactes :
   entiers JSON, décimaux en chaîne). Réécrire l'objet lu sous cette forme redonne les octets de la ligne : c'est le
   contrôle de canonicité.
3. Champs communs à tout enregistrement :
   - `type` : chaîne ;
   - `seq` : entier ; 0 pour le premier enregistrement du journal, puis plus un à chaque enregistrement, d'un fichier
     au suivant ;
   - `prec` : 64 chiffres hexadécimaux minuscules, sha256 des octets de la ligne précédente, octet 0x0A compris ;
     64 zéros pour `seq` = 0.
4. La **tête** est le couple (`seq` du dernier enregistrement, sha256 des octets de sa ligne, 0x0A compris).

## 2. Types d'enregistrement

| type | champs propres | écrit par |
|---|---|---|
| `ouverture` | `jour` (AAAA-MM-JJ, UTC), `suivante` (première fenêtre admise) | l'écrivain : premier enregistrement d'un journal neuf |
| `marqueur` | `ws` ; champs de la boucle (CB-4) | `marqueur(ws)` : clôt la fenêtre `ws` |
| `point` | `ws` : fenêtre qui clôt l'heure, (`ws` + w) multiple de 3 600 | l'écrivain, juste après ce marqueur ; son empreinte est la tête exportée (E-C-35) |
| `cloture` | `jour` : jour UTC du fichier qu'il clôt | l'écrivain : dernier enregistrement d'un fichier quotidien (§6) |
| tout autre type (`lecture`, `sante`, `run_params`…) | `ws` ; champs de son sous-lot | `ecrire(type, ws, …)` |

Les types `ouverture`, `marqueur`, `point`, `cloture`, `reprise` et `trou` sont réservés à l'écrivain. Un champ nommé
`seq` ou `prec` est refusé.

## 3. Fenêtres

1. `ws` est un entier, multiple de w = 60 s depuis l'époque Unix : la fenêtre est l'intervalle demi-ouvert [ws, ws + w).
2. Un enregistrement de fenêtre (tout type sauf `ouverture` et `point`) porte `ws` ≥ `suivante` : aucune ligne n'est
   écrite pour une fenêtre déjà close par son marqueur. Le marqueur de `ws` porte `suivante` à ws + w ; les marqueurs
   sont donc strictement croissants.
3. Un journal neuf ouvert pendant la fenêtre ws0 admet ws ≥ ws0 + w.

## 4. Durabilité

L'écriture se fait sans tampon. `fsync` est appelé à chaque marqueur (après le point de contrôle s'il y en a un), et
seulement là. Un arrêt brutal peut donc perdre les enregistrements postérieurs au dernier marqueur, ou laisser une
dernière ligne tronquée.

## 5. Un seul écrivain (CB-1b, E-C-16)

Le fichier `<préfixe>.verrou` du dossier du journal porte un verrou `flock` exclusif, pris sans attente avant toute
lecture ou écriture du journal et tenu jusqu'à la fermeture. Une seconde instance qui trouve le verrou pris s'arrête
sans rien lire ni écrire (JournalOccupe). Avec la chaîne, une écriture entrelacée de deux instances serait de toute
façon visible (`seq` ou `prec` rompu). C'est le moyen de fermeture par construction de SHOGEN-ENTRELACEMENT-D5-1 pour
S2-bis (Q-C-11 de la proposition, adoptée par l'avis) ; la fermeture de l'item reste un acte de l'orchestrateur.

## 6. Fichiers quotidiens et sommes (CB-2a, E-C-20)

1. Un fichier porte le nom `<préfixe>-<AAAA-MM-JJ>-<k>.jsonl` : jour UTC des fenêtres qu'il contient, puis numéro de
   segment `k` (0 pour le premier fichier du jour ; segments de reprise : §7). La grille divise l'heure (w divise
   3 600), donc la journée : une fenêtre n'est jamais à cheval sur deux jours.
2. Le premier enregistrement de fenêtre d'un jour nouveau déclenche la bascule : l'écrivain ajoute `cloture` au fichier
   courant, appelle `fsync`, le ferme, inscrit sa ligne au fichier de sommes, puis crée le fichier du nouveau jour
   (création exclusive), ouvert par `ouverture` (`jour`, `suivante`). La chaîne continue : le `seq` et le `prec` de
   cette ouverture suivent ceux de la clôture.
3. Le fichier de sommes `<préfixe>.sha256` reçoit une ligne par fichier clos, `<sha256 en hexadécimal>  <nom>` (deux
   espaces, format de `sha256sum`), ajoutée puis suivie d'un `fsync`. `sha256sum -c <préfixe>.sha256`, lancé dans le
   dossier, la contrôle.
4. Limite déclarée : la création d'un fichier n'est pas suivie d'un `fsync` du dossier ; la durabilité de l'entrée de
   répertoire après une coupure de courant n'est pas établie ici (item proposé à l'orchestrateur).
