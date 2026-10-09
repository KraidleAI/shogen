# Format des journaux d'observateur de S2-bis

- **Rattachement** : ADR-0029 §2.9 (l.238-240 : journal à enregistrement unique, chaîné, `fsync` au marqueur, point de
  contrôle horaire, fichiers quotidiens clos et sommés ; format spécifié et scellé au paquet) ; PROPOSITION du G0
  (`docs/adr-0029/g0-collecte/`), exigences E-C-16 à E-C-24 ; principe de SHOGEN-FORMAT-JOURNAUX-1 (annexe B d'ADR-0028,
  l.55).
- **Citations** (SHOGEN-S2BIS-CITATIONS-ADR-DECALEES-1) : « ADR-0029 l.N » renvoie à la ligne N de l'ADR-0029 au
  commit `e16956b`, convention du G0 COLLECTE-RECALC-DEPLOI, dont les renvois suivent le même texte. Les ajouts datés
  versés depuis décalent les numéros sans changer le texte cité (deux lignes insérées au §2.4 par `b9ba2b4` : le §2.9
  commence l.229 à `e16956b`, l.231 ensuite) ; un ajout daté se cite par sa date. Relevé du diff CB-18j : toutes les
  citations de l'ADR-0029 de ce texte, du code et des tests du collecteur suivent cette convention.
- **Statut** : texte tenu à jour à chaque sous-lot du collecteur ; il est scellé au paquet de S2-bis avec le commit du
  collecteur. Code de référence : `s2bis/shogen_s2bis/collecte/journal.py`. Le test de conformité d'un journal produit
  par le collecteur entier (E-C-24) est `s2bis/tests/test_bout_en_bout.py` (sous-lot CB-18e) : le point d'entrée
  tourne en sous-processus, et chaque enregistrement de son journal est contrôlé contre ce texte (champs exacts,
  types, grille, instants, ordre de la fenêtre), par un code de test qui n'importe rien du collecteur.
- **Corrections** : le diff CB-2d (2026-10-04) applique les corrections C-1, C-2 et C-6 (a) à (c) de la relecture G2
  de la tranche A de P1 (§2, §3.2, §4, §7.5, §8.1) ; le diff CB-2e applique C-3 (§8.4). Relecture G2 de la tranche B
  de P1 (2026-10-05) : le diff CB-11c applique C-1 et l'observation O-5 (§11.4, §11.6, §11.7, §13.2) ; CB-11d, C-5 et
  l'observation O-7 (§11.6, §13.1, §13.2) ; CB-11e, C-4 (§10.2, §11.6, §12, §13.1) ; CB-11f, C-2 (§12) ; CB-11g, C-3
  (§10.5) ; puis le diff CB-11h, CC-1 du contre-contrôle (§12). Relecture G2 du recalcul, tranche 1 (2026-10-05) :
  le diff CB-18f applique I-2 (§7.1) ; le diff SEGMENT-JOUR, N-1 (§6.1, §6.2, §7.2, §7.3) ; le diff ENTIER-ECRIVAIN,
  I-1 (§1.2, §2). Relecture G2 de la tranche C de P1 (2026-10-05) : le diff CB-18g applique C-1 (§14.1, §14.4) ; le
  diff CB-18h ferme l'item SHOGEN-S2BIS-CONFIG-REGLES-1 (§14.1) ; le diff CB-18i, par des tests seuls,
  SHOGEN-S2BIS-SEGMENTS-10-1 (§6.1) et SHOGEN-S2BIS-TEST-DISQUE-INSTABLE-1 (§13.5), et couvre le tuple au §1.2 ; le
  diff CB-18j écrit la convention des citations (en-tête, SHOGEN-S2BIS-CITATIONS-ADR-DECALEES-1) et place `run_params`
  dans l'ordre de la fenêtre (§11.5, observation de la G2). Lettres C-1 à C-5 du FORMAT (avis de l'advisor sur le
  banc de concordance des lecteurs du recalcul, adjugé par l'orchestrateur le 2026-10-05) : le diff CB-18n écrit C-4
  (§2, §8.3) ; le diff CB-18o, C-1 et C-2 (§7.1 : définition unique d'« intègre », sans limite déclarée ; l'item
  proposé SHOGEN-S2BIS-LIRE-BOOLEENS-1 n'a plus d'objet) ; le diff CB-18p, C-3 (§7.4) ; le diff CB-18q, C-5 (§5,
  §6.1, §7.7). Contre-contrôle de CB-18 (2026-10-05), adjugé par l'orchestrateur : le diff CB-18t applique O-1 (§7.4)
  et écrit la limite d'O-2 (§5). Relecture G2 d'intégration de P1 (2026-10-05) : le diff CB-19a applique C-1 (a)
  (§12) ; le diff CB-19b, C-1 (b) (§13.6, §14.1) ; le diff CB-19c, C-2 (a) (§6.4) ; le diff CB-19d, C-2 (b)
  et C-4 (c) (§4) ; le diff CB-19e, C-3 (a) et (b) (§11.4) ; le diff CB-19f, par des tests seuls, C-3 (c) et (d)
  (§14.2, §14.3) ; le diff CB-19g, C-4 (a), (b) et (d) (§9.1, §10.1, §11.5, §11.6).
- **Items de l'annexe B fermés au sous-lot CB-18** (2026-10-05) : le diff CB-18a ferme SHOGEN-S2BIS-ECRIVAIN-USAGE-1
  pour l'écrivain (§5) et porte les retouches de SHOGEN-S2BIS-FORMAT-RETOUCHES-1 (§12, en-tête) ; le diff CB-18b ferme
  SHOGEN-S2BIS-SOMMEIL-MURAL-1 (§10.2, §11.8), SHOGEN-S2BIS-SONDES-ECHEANCE-1 (§11.4, §13.2) et, pour la boucle,
  SHOGEN-S2BIS-PLAN-CABLAGE-1 (§11.9) ; le diff CB-18c achève SHOGEN-S2BIS-PLAN-CABLAGE-1 (câblage des sondes, §14) ;
  le diff CB-18d achève SHOGEN-S2BIS-ECRIVAIN-USAGE-1 (fermeture au point d'entrée, §14) ; le diff CB-18e verse le
  test de conformité de bout en bout (E-C-24) ; le diff CB-18f ferme SHOGEN-S2BIS-FORMAT-RETOUCHES-1, étendu par
  I-2, par ses tests nommés (`s2bis/tests/test_format.py` : la citation du §7.3, la marque « choix du lot » de la
  règle de source, CB-11h dans la puce « Corrections », valeurs prises au texte de l'item ; puis les contrôles de
  type de `_lire` dits au §7.1 et faits par `_lire`).
- **Partie P2, tranche A** (2026-10-08 ; sous-lots CB-6, CB-12, CB-13) : le diff CB-6c écrit le contenu de `valeurs`
  (§9.1, relevés des décodeurs de CB-6a et CB-6b) et le champ `decodeur` des formes (§14.1), et ferme pour les
  décodeurs SHOGEN-S2BIS-ECRIVAIN-REFUS-ARRET-1 (§9.1) ; le diff CB-6d ferme SHOGEN-S2BIS-TARDIVES-BORNE-1 (§13.6),
  SHOGEN-S2BIS-ECRIVAIN-IMBRICATION-OCTETS-1 (§8.3) et le volet graphe de SHOGEN-S2BIS-CORPS-BORNE-1 (§8.4) ; le
  diff CB-12a ferme SHOGEN-S2BIS-DNS-TC-1 et SHOGEN-S2BIS-DNS-ID-16BITS-1 (§12) ; le diff CB-13b écrit le §15
  (processus secondaire : journal, `carte.json` et ses règles croisées, boucle de la carte, relevé ASN de CB-12b et
  CB-13a, commande `secondaire`) et retouche les §12, §13.1 et §14.2.

## 1. Ligne et chaîne (CB-1)

1. Un journal est une suite de fichiers en UTF-8. Chaque enregistrement occupe une ligne terminée par l'octet 0x0A
   seul. Un lecteur découpe sur cet octet, et sur lui seul : les caractères U+2028 et U+2029 peuvent figurer dans une
   chaîne.
2. Chaque ligne est un objet JSON **canonique** : clés triées par point de code, séparateurs `,` et `:` sans espace,
   caractères hors ASCII écrits en UTF-8 (jamais en séquence `\u`), aucun nombre à virgule ni NaN (valeurs exactes :
   entiers JSON, décimaux en chaîne). Un entier a au plus 640 chiffres, signe non compté : 640 est la plus petite
   limite non nulle de conversion des entiers de Python (`sys.int_info.str_digits_check_threshold`), si bien que tout
   lecteur Python relit la ligne quel que soit son réglage. L'écrivain refuse un entier plus long avant toute écriture
   (`JOURNAL/entier` ; SHOGEN-S2BIS-ENTIER-ECRIVAIN-1, I-1 de la G2 du recalcul : un entier de 641 à 4 300 chiffres
   était écrit, puis lu comme une queue par le lecteur du recalcul) ; une ligne qui en porte un n'est pas intègre
   (§7.1). Réécrire l'objet lu sous cette forme redonne les octets de la ligne : c'est le contrôle de canonicité.
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
| `ouverture` | `jour` (AAAA-MM-JJ, UTC), `suivante` (première fenêtre ni close ni déclarée en trou) | l'écrivain : premier enregistrement d'un journal neuf, puis de chaque fichier quotidien (§6) |
| `marqueur` | `ws` ; aucun champ propre : la boucle (CB-4) n'en écrit pas, ses comptes vont à `sante` (§11) | `marqueur(ws)` : clôt la fenêtre `ws` |
| `point` | `ws` : fenêtre qui clôt l'heure, (`ws` + w) multiple de 3 600 | l'écrivain, juste après ce marqueur ; son empreinte est la tête exportée (E-C-35) |
| `cloture` | `jour` : jour UTC du fichier qu'il clôt | l'écrivain : dernier enregistrement d'un fichier quotidien (§6) |
| `reprise` | `ws` (fenêtre de l'horloge au redémarrage), `suivante`, `queue` | l'écrivain, au redémarrage (§7) |
| `trou` | `de`, `a`, `cause` | l'écrivain, juste avant le marqueur qui suit des fenêtres sans marqueur (§7) |
| tout autre type (`lecture`, `sante`, `run_params`, `tetes`…) | `ws` ; champs de son sous-lot | `ecrire(type, ws, …)` |

Les types `ouverture`, `marqueur`, `point`, `cloture`, `reprise` et `trou` sont réservés à l'écrivain. Un champ nommé
`seq` ou `prec` est refusé.

Tout refus est nommé (`JOURNAL/…`) et n'écrit rien (CB-2d, C-6 de la G2 de P1) : l'enregistrement demandé est contrôlé
(type des valeurs, entiers de 640 chiffres au plus du §1.2, borne LIMITE du §7, 64 niveaux d'imbrication au plus du
§8.3) avant la bascule de jour (§6) ou le
`trou` (§8) qu'il appellerait.

## 3. Fenêtres

1. `ws` est un entier, multiple de w = 60 s depuis l'époque Unix : la fenêtre est l'intervalle demi-ouvert [ws, ws + w).
2. Un **enregistrement de fenêtre** est un enregistrement écrit par `ecrire` ou `marqueur` (types autres que
   `ouverture`, `point`, `cloture`, `reprise` et `trou`). Il porte `ws` ≥ `suivante` et `ws` ≥ la dernière fenêtre
   écrite (CB-2d, C-1) :
   - aucune ligne n'est écrite pour une fenêtre déjà close par son marqueur ; le marqueur de `ws` porte `suivante` à
     ws + w ; les marqueurs sont donc strictement croissants ;
   - dans une exécution, `window_start` est non décroissant : plusieurs enregistrements d'une même fenêtre se suivent,
     jamais un enregistrement d'une fenêtre antérieure. En particulier, un enregistrement d'un jour J n'entre jamais
     dans le fichier de J + 1 après la clôture de J.
3. Un journal neuf ouvert pendant la fenêtre ws0 admet ws ≥ ws0 + w ; après une reprise, voir §7.

## 4. Durabilité

L'écriture se fait sans tampon. `fsync` est appelé (C-2 de la relecture d'intégration de P1, diffs CB-19c et CB-19d ;
C-4 (c) : la phrase d'avant le disait appelé au marqueur seul, ce que contredisaient les §6.2, §6.3 et §7.4) :
- à chaque marqueur, après le point de contrôle s'il y en a un ;
- à la bascule, après la `cloture` (§6.2) ; après chaque ligne du fichier de sommes (§6.3) ; après chaque `reprise`
  (§7.4) ;
- sur le dossier, après la création d'un fichier (§6.4) ;
- à la reprise (C-2 (b)) : avant d'écrire une `reprise` en segment neuf, sur le fichier dont elle chaîne la dernière
  ligne intègre et sur ceux dont elle déclare la queue, même déjà sommés ; avant d'écrire la somme d'un fichier, sur
  ce fichier.

Entre deux marqueurs, rien n'est synchronisé : un arrêt brutal peut donc perdre les enregistrements postérieurs au
dernier marqueur, ou laisser une dernière ligne tronquée.

**Coupure de courant** (preuve de C-2) : banc à coupures de la relecture d'intégration (outil du réviseur, sha256
`edca2fa8…`, rejoué sans modification ; graines 0 à 299, comme la relecture, sur des trajectoires qui diffèrent, le
banc tirant ses pannes au sort à chaque `fsync`). Modèle : chaque fichier revient, au pire, à sa taille au dernier
`fsync` de son inode, la part gardée au-delà pouvant finir en octets nuls. Résultat : 0 rupture et 0 somme fausse
(128 et 131 avant C-2), sur 1 438 redémarrages et 533 queues déclarées. Ce que le modèle prouve : aucune `reprise` ne
chaîne, ne déclare ni ne somme des octets qu'une coupure peut retirer, et aucune ligne du fichier de sommes ne précède
les octets qu'elle somme. Ce qu'il ne prouve pas : la durabilité d'une entrée de dossier (le modèle ne retire jamais
un fichier, §6.4) ; un `fsync` qui rend sans avoir écrit (cache d'écriture du disque) ; une perte sous la taille
synchronisée d'un fichier. Un journal neuf dont le premier fichier n'est pas encore synchronisé (avant son premier
marqueur) peut toujours, après une coupure, n'avoir aucune ligne intègre (§7.6).

**Arrêt sur erreur d'entrée-sortie** (CB-2d, C-2) : toute `OSError` levée par une écriture, un `fsync`, une ouverture
ou une fermeture de fichier pendant `ouvrir`, `ecrire` ou `marqueur` (bascule, sommes et reprise comprises) laisse
l'écrivain inutilisable. L'erreur remonte à l'appelant ; tout appel suivant est refusé (`JOURNAL/casse`) sans rien
écrire. `fermer` rend toujours le verrou, même si la fermeture du fichier échoue. L'instance suivante déclare la
ligne déchirée comme queue (§7) : aucun enregistrement n'est écrit après elle, et chaque ligne du fichier de sommes
reste égale au sha256 des octets de son fichier.

## 5. Un seul écrivain (CB-1b, E-C-16)

Le fichier `<préfixe>.verrou` du dossier du journal porte un verrou `flock` exclusif, pris sans attente avant toute
lecture ou écriture du journal et tenu jusqu'à la fermeture. Une seconde instance qui trouve le verrou pris s'arrête
sans rien lire ni écrire (JournalOccupe). Avec la chaîne, une écriture entrelacée de deux instances serait de toute
façon visible (`seq` ou `prec` rompu). C'est le moyen de fermeture par construction de SHOGEN-ENTRELACEMENT-D5-1 pour
S2-bis (Q-C-11 de la proposition, adoptée par l'avis) ; la fermeture de l'item reste un acte de l'orchestrateur.

**Un seul fil** (CB-18a, SHOGEN-S2BIS-ECRIVAIN-USAGE-1). L'écrivain ne se partage pas entre fils, et la garde est
mécanique :
- le fil qui appelle `ouvrir` est noté ; `ecrire` ou `marqueur` appelés d'un autre fil sont refusés (`JOURNAL/fil`) ;
- un écrivain s'ouvre une seule fois : un second `ouvrir` est refusé (`JOURNAL/ouvert`), sans toucher au verrou ni au
  fichier ouvert ;
- une écriture avant `ouvrir` ou après `fermer`, et l'ouverture d'un écrivain fermé, sont refusées (`JOURNAL/ferme`) ;
- une ouverture refusée (`JOURNAL/occupe`, `JOURNAL/fenetre`, `JOURNAL/nom`, `JOURNAL/illisible`) ferme l'écrivain et
  rend le verrou ;
- `fermer` est le seul appel admis de tout fil (nettoyage) ; il reste admis après une casse (§4).

Aucun de ces refus n'écrit. Les trois méthodes publiques d'écriture portent la même garde que la casse de C-2 (§4) ; un
test contrôle que toute méthode publique de l'écrivain la porte, `fermer` excepté.

Limite (O-2 du contre-contrôle de CB-18, item SHOGEN-S2BIS-PREFIXE-NOM-1) : un dossier par journal ; un préfixe qui en
prolonge un autre dans le même dossier fait refuser le plus court (`JOURNAL/nom`, §6.1).

## 6. Fichiers quotidiens et sommes (CB-2a, E-C-20)

1. Un fichier porte le nom `<préfixe>-<AAAA-MM-JJ>-<k>.jsonl` : jour UTC des fenêtres qu'il contient, puis numéro de
   segment k, en décimal sans zéro de tête (`0|[1-9][0-9]*`). Le numéro vaut 1 + le plus grand numéro de ce jour présent
   au dossier, 0 pour le premier fichier du jour (bascule : point 2 ; segments de reprise : §7.2). L'ordre de la chaîne
   est l'ordre (jour, k entier), non l'ordre des noms affiché par un listage. Au-delà de 9 segments d'un jour, l'ordre
   des noms en texte (celui de `ls`) n'est plus celui de la chaîne (« -10 » y précède « -2 ») ; un test couvre onze
   segments d'un même jour (SHOGEN-S2BIS-SEGMENTS-10-1). Lettre C-5 du FORMAT (diff CB-18q) : le numéro n'est jamais
   complété de zéros (pas de numéro sur trois chiffres) ; tout outil (rétention, sommes) trie en entier ou lit le
   fichier de sommes. À l'ouverture, l'écrivain refuse un nom qui commence par `<préfixe>-` et finit par `.jsonl` sans
   suivre cette grammaire (`JOURNAL/nom`, §5) ; à la bascule, un tel nom est ignoré, et le redémarrage suivant le
   refuse. Une seule exception au jour des fenêtres : après un redémarrage dont l'horloge est en arrière du jour d'un
   fichier présent, le segment de reprise porte ce jour, et les fenêtres antérieures s'y écrivent jusqu'à ce que
   l'horloge le rejoigne (§7.2). La grille divise l'heure (w divise 3 600), donc la journée : une fenêtre n'est jamais à
   cheval sur deux jours.
2. Le premier enregistrement de fenêtre d'un jour nouveau déclenche la bascule : l'écrivain ajoute `cloture` au fichier
   courant, appelle `fsync`, le ferme, inscrit sa ligne au fichier de sommes, puis crée le fichier du nouveau jour au
   numéro suivant de ce jour (point 1 : un fichier du jour déjà présent, vide par exemple, n'est jamais heurté ;
   SHOGEN-S2BIS-SEGMENT-JOUR-1), en création exclusive, ouvert par `ouverture` (`jour`, `suivante`). La chaîne
   continue : le `seq` et le `prec` de cette ouverture suivent ceux de la clôture.
3. Le fichier de sommes `<préfixe>.sha256` reçoit une ligne par fichier clos, `<sha256 en hexadécimal>  <nom>` (deux
   espaces, format de `sha256sum`), ajoutée puis suivie d'un `fsync`. `sha256sum -c <préfixe>.sha256`, lancé dans le
   dossier, la contrôle.
4. **Entrée de dossier** (C-2 (a) de la relecture d'intégration de P1, diff CB-19c ; remplace la limite déclarée
   jusque-là) : après la création d'un fichier du journal (journal neuf, bascule, segment de reprise), sa première
   ligne écrite, et après la création du fichier de sommes, sa première ligne écrite et synchronisée, l'écrivain
   appelle `fsync` sur le dossier : l'entrée du fichier créé est durable. La première ligne précède ce `fsync`, dont
   l'échec ne laisse donc pas un fichier vide. Ce que ce `fsync` garantit dépend du système de fichiers ; le banc à
   coupures de la relecture, dont le modèle ne porte que sur la taille des fichiers, ne le prouve pas (§4).

## 7. Reprise et segments (CB-2b, E-C-21)

1. À l'ouverture d'un journal existant, verrou pris, l'écrivain relit les fichiers du plus récent au plus ancien, ligne
   à ligne (LIMITE = 4 194 304 octets au plus par ligne, saut compris ; l'écrivain refuse d'écrire une ligne plus
   longue), jusqu'au premier fichier qui contient un enregistrement intègre. **Définition unique d'« intègre »**
   (lettres C-1 et C-2 du FORMAT, diff CB-18o ; elle remplace celle du diff CB-18f, I-2 de la G2 du recalcul, et les
   limites qu'il déclarait). Une ligne est **intègre** si et seulement si :
   (a) elle se termine par 0x0A et fait au plus LIMITE octets, saut compris ;
   (b) ses octets sont un objet JSON canonique (§1.2) dont tout entier a au plus 640 chiffres, signe exclu, et dont
   aucun conteneur n'est au-delà du niveau N = 64 (§8.3) ;
   (c) ses champs communs ont les types du §1.3 : `type` chaîne, `seq` entier, `prec` chaîne de 64 chiffres
   hexadécimaux minuscules ;
   (d) si `type` est réservé (§2), ses champs propres ont les types du §2 : `jour` chaîne ; `suivante`, `ws`, `de`,
   `a` entiers ; `queue` liste ou null ; `cause` chaîne ; un champ propre manquant rend la ligne non intègre ;
   (e) elle est chaînée à la ligne intègre qui la précède dans le fichier : `seq` + 1, `prec` égal au sha256 de ses
   octets ; la première ligne d'un fichier est une `ouverture` ou une `reprise`.
   Un booléen JSON n'est jamais un entier. Le lien de la première ligne d'un fichier à la dernière ligne intègre du
   fichier précédent ne fait pas partie de l'intégrité : il se juge à part (§7.7) et ne se juge que par les lecteurs.
   La lecture d'un fichier s'arrête à la première ligne non intègre : elle et tout ce qui suit forment la **queue** du
   fichier. Cette définition est la même chez l'écrivain (`Journal._lire`, code de référence), le lecteur du recalcul
   (RB-1) et le lecteur indépendant (RB-18) ; aucun des trois ne la relâche.
   Elle type aussi le `ws` d'un type non réservé (`lecture`, `sante`, `run_params`…), seul champ que le §2 lui donne :
   un entier, requis comme un champ propre au point (d) ; avec celui du `marqueur`, il donne la **dernière fenêtre
   écrite** (§7.5). Risque R-2 de l'avis, vérifié type par type au diff CB-18o : aucun type n'a de `ws` null ;
   `ouvrir` (dont la fenêtre est le `ws` de la `reprise`), `ecrire` et `marqueur` refusent tout `ws` qui n'est pas un
   entier (`JOURNAL/fenetre`, booléen compris), `point` reprend le `ws` de son marqueur, `run_params` s'écrit par
   `ecrire` (§11.5) ; le journal du test de bout en bout, relu à son second démarrage, n'a aucune queue. Les valeurs
   (`ws` multiple de w, `ws` ≥ `suivante`, `cause` parmi trois mots, `jour` au calendrier) restent de la
   **validité**, jugée au recalcul (RB-3), pas de l'intégrité (§3, §8).
2. Une queue n'est jamais réécrite ni tronquée. S'il en existe une (dans le fichier repris, ou un fichier plus récent
   sans enregistrement intègre), l'écrivain ouvre un **segment** neuf, premier enregistrement `reprise` : son jour est
   le plus tardif entre celui de l'horloge, celui du fichier repris et celui de tout fichier présent au dossier ; son
   numéro, 1 + le plus grand de ce jour. L'ordre des noms reste ainsi l'ordre de la chaîne, même quand l'horloge du
   redémarrage est en arrière du jour d'un fichier vide ou sans ligne intègre laissé par une panne
   (SHOGEN-S2BIS-SEGMENT-JOUR-1, N-1 de la G2 du recalcul : le segment prenait le jour de l'horloge, nommé avant le
   fichier qu'il déclarait, et la bascule suivante heurtait ce fichier). Les fenêtres d'un jour antérieur s'écrivent
   alors dans ce segment (§6.1).
3. Sans queue : un fichier repris d'un jour passé reçoit sa `cloture`, puis un fichier neuf s'ouvre par `reprise` ; un
   fichier repris déjà clos laisse place à un fichier neuf ouvert par `reprise` (jour et numéro de ces fichiers neufs :
   point 2) ; sinon `reprise` s'écrit à sa suite.
4. `reprise` porte `ws` (fenêtre de l'horloge au redémarrage), `suivante` (première fenêtre ni close ni déclarée en
   trou, lue dans l'état repris) et `queue` : liste de `{fichier, position, octets, sha256}` (octet de début de la
   queue, longueur, empreinte de ses octets), ou null. Un `fsync` suit son écriture. La chaîne reprend au dernier
   enregistrement intègre : le `prec` de la `reprise` est l'empreinte de sa ligne. **Déclaration exacte** (lettre C-3 du
   FORMAT, diff CB-18p) : `queue` est une liste non vide, dans l'ordre croissant (jour, k) des fichiers (§6.1), ou null
   sans queue ; elle est comparée sous forme canonique. L'écrivain l'écrit dans cet ordre : il relit les fichiers du
   plus récent au plus ancien (point 1) et range chaque queue trouvée devant les précédentes ; un test de deux pannes
   réelles, dont la seconde coupe la `reprise` d'un segment neuf, fixe cet ordre (risque R-1 de l'avis). Une liste vide,
   un objet nu (un objet nu rend déjà la ligne non intègre, §7.1 d), un autre ordre ou un booléen pour un entier font
   une déclaration fausse. À toute rupture (lien rompu, déclaration fausse, queue non déclarée), aucune queue en attente
   n'est réputée déclarée : toutes sont rendues avec la rupture. Une `reprise` au lien rompu ou à déclaration fausse est
   une rupture **non déclarée** ; sa déclaration n'est pas lue ; toutes les queues en attente sont rendues avec elle. Ne
   comptent comme reprises déclarées que les `reprise` intègres, au lien juste, à déclaration exacte. Les lecteurs
   appliquent le §7.1 avant le §7.4. Ce point classe les ruptures ; la portée d'une rupture (quelles fenêtres deviennent
   D-1 « intégrité » autour d'elle) revient à la politique de rupture du paquet (RB-3, SHOGEN-S2BIS-RUPTURE-PORTEE-1).
   Le lien que juge ce point est celui du §7.7 : seuls les lecteurs le jugent.
5. Après une reprise, un enregistrement de fenêtre exige ws ≥ max(`suivante`, dernière fenêtre écrite + w, fenêtre
   du redémarrage + w) (CB-2d, C-1). La **dernière fenêtre écrite** est le `ws` du dernier enregistrement de fenêtre
   (§3.2) dans l'ordre de la chaîne ; si le fichier repris n'en contient aucun (coupure entre une `ouverture` ou une
   `reprise` et le premier enregistrement de fenêtre), elle est cherchée dans les fichiers précédents, du plus récent
   au plus ancien. Ainsi la fenêtre du redémarrage, toute fenêtre déjà close et toute fenêtre entamée sans marqueur
   par l'exécution précédente restent refusées, même si l'horloge a reculé : `window_start` est strictement croissant
   d'un démarrage au suivant. Une fenêtre entamée puis interrompue est déclarée par le `trou` qui précède le marqueur
   suivant (§8), jamais complétée par l'exécution suivante. La fenêtre du redémarrage reste refusée même si elle n'a
   encore aucune ligne (Q-4 de la G2, adjugée par l'orchestrateur) : un redémarrage coûte une fenêtre, déclarée
   `arret`.
6. Aucun enregistrement intègre dans tout le journal : refus nommé `JOURNAL/illisible` ; l'écrivain ne démarre pas et
   ne crée jamais une seconde chaîne dans le même dossier.
7. **Lecteurs** (lettre C-5 du FORMAT, diff CB-18q). Les fichiers du journal sont les fichiers du dossier dont le nom
   est `<préfixe>-<AAAA-MM-JJ>-<k>.jsonl` au sens du §6.1, lus dans l'ordre (jour, k entier). Un nom qui commence par
   `<préfixe>-` et finit par `.jsonl` sans satisfaire cette grammaire est un refus nommé ; un dossier sans aucun
   fichier du journal est un refus nommé. L'écrivain applique la même grammaire à la reprise (`_fichiers`) : il refuse
   de démarrer devant un nom non conforme (`JOURNAL/nom`, §6.1). La validité de la date au calendrier et l'égalité du
   `jour` d'une `ouverture` ou d'une `cloture` au nom de son fichier restent de la validité (RB-3). La reprise de
   l'écrivain ne juge pas le lien entre la première ligne d'un fichier et la dernière ligne intègre qui la précède
   dans la chaîne (§7.1) : ce lien se juge ici, par le lecteur du recalcul (RB-1) et le lecteur indépendant (RB-18)
   seuls.

## 8. Trous et sommes rattrapées (CB-2c, E-C-22, E-C-20)

1. Toute fenêtre sans marqueur porte sa cause. Quand un marqueur arrive pour ws > `suivante` de l'état (première
   fenêtre ni close ni déclarée), l'écrivain écrit d'abord `trou` : `de` = `suivante`, `a` = ws − w, `cause` :
   - `arret` pour le premier trou qui suit une reprise ;
   - `horloge_reculee` si l'horloge du redémarrage était en arrière de la dernière fenêtre close (fenêtre du
     redémarrage + w < `suivante`) ;
   - `saut` pour des fenêtres sautées pendant l'exécution.
   Un marqueur refusé n'écrit pas son trou (§2, CB-2d). Un `trou` écrit avance l'état, relu à la reprise
   (`suivante` = `a` + w) : après une coupure entre un trou et son marqueur, le même intervalle n'est jamais déclaré
   deux fois.
2. À la reprise, chaque fichier achevé (clos, abandonné à une queue, ou laissé pour un segment neuf) reçoit sa ligne
   au fichier de sommes s'il n'y figure pas, sha256 pris sur ses octets ; une dernière ligne coupée du fichier de sommes
   est close par un saut de ligne, jamais réécrite.
3. **Imbrication** (lettre C-4) : le **niveau** d'une valeur est 1 pour l'objet de la ligne, et n + 1 pour une valeur
   contenue dans un conteneur (objet ou liste) de niveau n. Un enregistrement a tous ses conteneurs au niveau N = 64
   au plus. L'écrivain refuse d'écrire un enregistrement plus profond (`JOURNAL/imbrication`), avant le sérialiseur,
   quel que soit le réglage de l'interpréteur ; sa relecture (`_lire`) et les lecteurs mesurent le niveau et tiennent
   pour non intègre (§7.1) toute ligne qui dépasse N, qu'un décodeur la lise ou lève RecursionError : ils comptent
   les niveaux eux-mêmes et ne se fient pas à l'exception. `_lire` compte, comme les lecteurs, le niveau d'une ligne
   sur ses octets, avant tout décodeur, après l'avoir lue en UTF-8 strict (CB-6d,
   SHOGEN-S2BIS-ECRIVAIN-IMBRICATION-OCTETS-1 : il décodait d'abord, et son verdict venait de RecursionError au-delà
   du seuil du décodeur) ; une RecursionError n'y est jamais un verdict. Un conteneur que l'enregistrement porte à
   plusieurs endroits compte à sa plus grande profondeur, celle de la ligne écrite. Motif de N : le plus profond
   enregistrement du collecteur mesure M = 4 niveaux au test de bout en bout (E-C-24 ; `run_params`,
   `formes.formes[i]` ; `lecture`, `valeurs[i].extra`, CB-6c), et une
   `sante` dont une sonde D-4 ou D-5 rend une réponse SOA ou TXT en atteint 6 (§12, §13.4) ; le plus petit seuil de
   lecture mesuré sur les décodeurs Python du projet est 988 niveaux (Python 3.10, limite de récursion par défaut ;
   seuils mesurés sous 3.10 et 3.12 seulement, banc de la G2 de RB-18) ; N est très au-dessus du premier et très
   au-dessous du second.
4. L'écrivain refuse de même, en temps borné, un enregistrement qui contient une structure cyclique (`JOURNAL/type`) :
   le contrôle de cycle du sérialiseur `json` précède le parcours des valeurs (CB-2e, C-3). Une sous-structure
   partagée sans cycle reste admise ; elle est écrite autant de fois qu'elle figure. L'écrivain en compte les valeurs
   une fois par occurrence, sans développer le graphe, et refuse avant le sérialiseur un enregistrement de plus de
   LIMITE valeurs, qui ferait plus de LIMITE octets (`JOURNAL/taille` ; CB-6d, volet graphe de
   SHOGEN-S2BIS-CORPS-BORNE-1 : `canonique` développait le graphe, en temps exponentiel).

## 9. Enregistrement `lecture` (CB-3a ; E-C-03, E-C-04, E-C-17)

1. Une lecture donne un seul enregistrement, de type `lecture`, écrit dans sa fenêtre `ws`. Ses champs propres :
   - `statut` : `ok`, `panne_http`, `panne_transport` ou `panne_decode` (statuts lisibles par `r1.classify_ecart` de
     S2) ;
   - `sous_type` : pour `panne_transport` seulement, l'un de `dns`, `connexion`, `tls`, `delai`, `coupure`, `autre` ;
     null pour tout autre statut ;
   - `code` : code HTTP de la réponse (entier) ; null si aucune réponse n'a été lue ;
   - `depart`, `fin` : instants de départ et de fin de la lecture ;
   - `phases` : objet qui donne l'instant de fin de chaque phase atteinte (§10) ;
   - `adresse` : `a.b.c.d:port`, l'adresse résolue (la première que rend la résolution, et son port) ; null si la
     résolution n'a pas rendu. Elle n'a été contactée que si `phases` porte la connexion (C-4 (d) de la relecture
     d'intégration de P1, diff CB-19g ; §10.1) ;
   - `brut` : octets du corps de la réponse, en base64 (alphabet standard, avec remplissage) ; `sha256` : leur
     empreinte, en 64 chiffres hexadécimaux minuscules ;
   - `valeurs` (CB-6c) : null, sauf pour le statut `ok` : liste des relevés que rend le décodeur de la forme
     (`decodeur` de `formes.json`, §14.1), un par actif que la réponse porte ; chaque relevé est un objet aux clés
     exactes `actif`, `classe`, `devise`, `prix`, `ts_source` et `extra` : `actif`, l'un de `BTC`, `ETH`, `USDC`,
     `USDT` ; `classe`, la classe de source, l'un de `place_horodatee`, `sans_horodatage`, `agregateur`,
     `oracle_chainlink` (noms d'`analyse.json`) ; `devise`, la devise de cotation (`USD`, `USDT`) ; `prix`, décimal en
     chaîne, texte d'un Decimal fini et strictement positif ; `ts_source`, l'instant que porte la source, en
     microsecondes entières de 0 à 2^53 exclu, null pour une source sans horodatage ; `extra`, objet de chaînes propre
     à la source. Un corps que le décodeur ne lit pas, ou dont le prix n'est pas fini, est nul ou négatif, donne
     `panne_decode`, `code` et `brut` gardés, `valeurs` null.
   - **Instant ISO-8601** (C-5 de la G2 de P2A) : un instant de source écrit en ISO-8601 (Coinbase, champ `time`) est
     lu par un motif fixe : date `AAAA-MM-JJ`, « T » majuscule, heure `hh:mm:ss`, fraction de chiffres facultative
     (tronquée à la microseconde, comme en S2), puis « Z » majuscule, `±hh:mm` ou rien (instant lu en UTC). « t »,
     « z », un espace entre la date et l'heure ou `+hhmm` donnent `panne_decode`. Raison : `datetime.fromisoformat`,
     que lisait S2 (`_iso_to_epoch`), ne lit pas la même chose de 3.10 à 3.13 (sous 3.10, il refuse une fraction de
     quatre chiffres, « Z » et `+0000`, que 3.11 admet : mesuré) ; un motif fixe lit pareil sous chaque version. C'est
     un écart à S2, qui admettait « t », l'espace et, de 3.11 à 3.13, `+0000` (mesuré), et à la RFC 3339 §5.6, qui
     admet « t » et « z » minuscules ; Coinbase écrit « T » et « Z » (fixture de S2).
   - **Valeurs refusées par l'écrivain** (CB-6c, SHOGEN-S2BIS-ECRIVAIN-REFUS-ARRET-1) : les valeurs d'un décodeur
     passent, avant d'être rendues, le contrôle de l'écrivain (`canonique` : aucun flottant, entiers de 640 chiffres au
     plus, 64 niveaux au plus, texte encodable en UTF-8) et une borne de 2 097 152 octets de JSON canonique, saut de
     ligne compris ; sinon la lecture est `panne_decode`, `valeurs` null. Aucune valeur que l'écrivain refuserait ne
     l'atteint : son refus (`JOURNAL/…`) arrêterait le processus, que systemd relancerait avec un trou à chaque
     fenêtre. Avec un corps de 1 048 576 octets (point 4) et des valeurs à leur borne, une `lecture` fait moins de
     3 500 000 octets, sous LIMITE (§7.1).
2. Tout instant d'un enregistrement de lecture est un entier : microsecondes depuis l'époque Unix (UTC). Les valeurs
   restent sous 2^53 : tout lecteur JSON les lit exactement.
3. La requête HTTP reprend octet pour octet celle qu'envoyait urllib en S2 (ordre des en-têtes compris, mesuré sur un
   serveur de boucle locale) : `Accept-Encoding: identity` (sans lui, tout codage serait admis : RFC 9110
   §12.5.3), `Host` (avec le port s'il n'est pas 443), `User-Agent` de S2, `Accept: application/json`,
   `Connection: close` ; pour une requête avec corps, `Content-Length` et `Content-Type: application/json`.
4. La réponse est lue au plus juste (`Content-Length`, blocs `chunked`, sinon jusqu'à la fermeture). Au plus
   1 048 576 octets sont reçus, en-têtes compris : au-delà, la lecture est `panne_transport` de sous-type `autre`.

## 10. Phases de la lecture et sous-types de panne (CB-3b ; E-C-03 à E-C-05)

1. Une lecture HTTPS passe par cinq phases, dans l'ordre ; `phases` porte l'instant de fin de chacune de celles qui
   ont abouti :

   | phase | ce qui la termine | défaut pendant la phase |
   |---|---|---|
   | `dns` | la résolution du nom en IPv4 seule (`getaddrinfo` en `AF_INET`) rend une adresse ; la première est retenue, puis contactée (phase `connexion`) | `dns` (échec, aucune adresse, ou délai épuisé pendant la résolution : une `dns` rendue après une résolution tardive porte `phases.dns` et une adresse non contactée, C-4 (d)) |
   | `connexion` | la connexion TCP est établie | `connexion` |
   | `tls` | la poignée TLS aboutit (certificat vérifié, nom d'hôte contrôlé) | `tls` |
   | `requete` | les octets de la requête sont envoyés | `coupure` |
   | `corps` | la réponse est lue entière | `coupure` (fin du flux ou connexion rompue avant la fin annoncée) ; `autre` (réponse illisible, ou plus de 1 048 576 octets) |

2. Délai global : la lecture entière dispose de 10 s depuis son départ (ADR-0029 l.233). Chaque attente reçoit le temps
   qui reste, jamais un délai par opération ; un délai épuisé pendant une phase autre que `dns` donne le sous-type
   `delai`. La résolution est un appel bloquant que le client ne peut pas interrompre : l'échéance de la boucle (§11)
   la borne. Le délai se compte sur l'horloge monotone du système, les instants journalisés sur l'horloge murale
   (C-4) : un recul ou une avance de l'horloge murale pendant la lecture ne change pas son délai. Il court depuis le
   départ de la lecture, que la boucle relève aussi sur l'horloge monotone et porte dans le suivi de la lecture, sans
   le journaliser (CB-18b) : le lancement du fil compte dans le délai, et l'horloge murale n'y entre jamais (limite
   E-4 des corrections de la tranche B, levée). Une lecture lancée hors de la boucle compte son délai depuis son
   début.
3. Réponse lue entière : code 200, statut `ok` ; tout autre code, `panne_http` avec ce code et le corps reçu. Aucune
   redirection n'est suivie (S2 suivait celles d'urllib) : un code 3xx est un `panne_http`.
4. Toute autre anomalie (défaut imprévu, requête dont l'hôte, le chemin ou la méthode sort de l'ASCII imprimable sans
   espace) donne `panne_transport` de sous-type `autre`. Une lecture ne lève jamais.
5. **Contexte TLS** (C-3) : celui qu'urllib arme en S2 quand aucun contexte n'est donné (`http.client`, Python 3.10 à
   3.13) : `ssl.create_default_context()` (certificat vérifié, nom d'hôte contrôlé), ALPN `http/1.1`, authentification
   après poignée annoncée. Le nom de la requête part en SNI. La ClientHello porte les mêmes extensions que celle
   d'urllib (mesure en boucle locale, Python 3.10 à 3.13, OpenSSL 3.0.13 : journal G1 des corrections de la tranche B).

## 11. Boucle du pool : lectures planifiées, échéance, santé de la boucle (CB-4 ; E-C-09, E-C-11 à E-C-15)

1. **Instants de la fenêtre ws** (ADR-0029 l.233 ; avis OPS Q7) : départ D = ws + w − δ, δ = 20 s ; échéance
   E = ws + w − 1 s. La lecture d'une forme part à D plus le décalage de la forme : 0, sauf sur un hôte dont la limite
   impose l'espacement, où la k-ième lecture de l'hôte part k s après D (k de 0 à 4) ; au plus 5 lectures par hôte et
   par fenêtre, au-delà le regroupement s'impose (l.234).
2. **Enregistrement `lecture`** : aux champs du §9 s'ajoutent `forme` (nom de la forme de requête) et `prevu`
   (instant planifié, en microsecondes). `depart` est l'instant où la boucle lance la lecture ; le délai global de la
   lecture court depuis cet instant.
3. **Pool borné** : une lecture ne part que si une place du pool est libre ; une place reste prise jusqu'à la fin de
   la lecture, même abandonnée. Une lecture qui ne part pas n'a **aucun** enregistrement `lecture` : ce n'est jamais
   une panne de source (Q-C-02) ; elle est comptée dans la santé (`non_parties`).
4. **Échéance** (C-1) : à E, le fil principal relève **une seule fois**, avant toute écriture, l'instant du relevé
   (horloges murale et monotone), puis l'état de chaque lecture partie et de chaque sonde (§13.2), et seulement
   ensuite le disque et l'empreinte du résolveur (CB-18b) ; puis, seul écrivain, il écrit une `lecture` pour chaque
   lecture partie.
   Une lecture est **non finie** si son résultat n'était pas rendu au relevé, ou s'il porte `fin` > E (rendu entre E
   et le relevé). Elle est alors `panne_transport`, de sous-type `dns` si la résolution n'avait pas rendu à E (aucune
   phase `dns` d'instant au plus E), sinon `delai` ; `fin` vaut E ; `phases` et `adresse` sont celles atteintes à E
   (instants au plus E ; `adresse` null sans phase `dns`) ; son fil est abandonné, et son résultat suit le chemin des
   résultats tardifs (§11.6). Le suivi est partagé (C-3 (b) de la relecture d'intégration de P1, diff CB-19e) : le
   client pose l'adresse au suivi avant la phase `dns`, et la boucle relève les phases avant l'adresse ; une phase
   `dns` relevée a donc toujours son adresse. Une lecture dont la fonction lève, BaseException comprise (O-5 :
   l'exception suit son cours, le résultat est rendu), ou ne rend pas une lecture, est `panne_transport` de sous-type
   `autre`.
5. **Ordre des enregistrements de la fenêtre** : les `lecture` dans l'ordre du plan (décalage, puis nom de forme),
   puis, dans la fenêtre qui clôt l'heure et si un dépôt des têtes est configuré, `tetes` (§16.6), puis `sante`,
   puis (`trou` s'il y a lieu, §8) `marqueur`. Dans la première fenêtre admise d'une exécution,
   `run_params` (§14.4) suit immédiatement l'`ouverture` ou la `reprise` du démarrage, ou, si cette fenêtre ouvre un
   jour nouveau, `run_params` suit l'`ouverture` de la bascule qu'il déclenche (C-4 (b) de la relecture d'intégration
   de P1 : `reprise` et `cloture` au fichier repris, `ouverture` et `run_params` au fichier du jour), et précède
   toute `lecture` ; si la boucle part d'une fenêtre plus tardive, celle de `run_params` reste sans marqueur,
   déclarée par le `trou` suivant. Une fenêtre dont l'échéance est déjà passée quand la boucle l'atteint n'est pas
   lue : le trou est déclaré au marqueur suivant (cause `saut`).
6. **Enregistrement `sante` de la boucle** (valeurs brutes, aucun jugement) :
   - `d2.retard_max` : plus grand retard au départ (instant de lancement moins instant planifié, en microsecondes)
     parmi les lectures parties ; null si aucune n'est partie. `d2.non_parties` : nombre de lectures planifiées qui ne
     sont pas parties faute de place. D-2 se juge au recalcul (règle Q-C-02 de l'avis : toute lecture partie plus de
     5 s après son instant planifié, ou non partie, dégrade l'observateur dans la fenêtre) ;
   - `fils.abandonnes` : lectures abandonnées, à savoir celles de la fenêtre (non finies à E, §11.4, même si leur
     résultat est arrivé entre E et le relevé), plus celles des fenêtres précédentes dont le résultat n'était pas
     arrivé au relevé ;
     `fils.tardives` : latences (fin moins départ, en microsecondes, triées) des lectures abandonnées aux relevés
     précédents dont le résultat est rendu au relevé de cette fenêtre : arrivé depuis le relevé précédent, ou déjà
     arrivé à ce relevé-là pour une lecture de la fenêtre précédente rendue entre son échéance et son relevé (non
     finie, §11.4) ; une lecture finie entre E et le relevé compte en `tardives` à la fenêtre suivante (C-4 (a) de la
     relecture d'intégration de P1). Un résultat tardif n'est jamais écrit comme lecture (Q-C-15) ;
     `fils.sondes` : instances de sonde encore en cours au relevé (§13.2), au plus une par sonde ; 0 sans sondes ;
   - `horloges` (C-4, ferme SHOGEN-S2BIS-HORLOGE-RECUL-JOURNAL-1) : `{murale, monotone}`, temps écoulé depuis le relevé
     de la fenêtre précédente de la même exécution, en microsecondes, lu sur l'horloge murale et sur l'horloge
     monotone ; null à la première fenêtre d'une exécution. Valeurs brutes : un recul de l'horloge murale entre deux
     fenêtres se lit `murale` < `monotone`, une avance `murale` > `monotone` ; la boucle, elle, ne recule jamais de
     fenêtre (§3.2).
7. Les fils de lecture sont des fils démons : un fil pendu n'empêche jamais le processus de s'arrêter. D'où des futurs
   `concurrent.futures` sans `ThreadPoolExecutor`, qui joint ses fils à la sortie de l'interpréteur, même après
   `shutdown(wait=False, cancel_futures=True)` (essais du worker et de la G2 de la tranche B, Python 3.10 à 3.13).
8. **Attentes sur l'horloge murale** (CB-18b, SHOGEN-S2BIS-SOMMEIL-MURAL-1) : la boucle attend le départ de chaque
   lecture et l'échéance par pas d'au plus 1 s, en relisant l'horloge murale après chaque pas, jusqu'à l'instant
   visé ; l'attente de l'échéance cesse aussi quand toutes les lectures et sondes ont rendu. Un recul de l'horloge
   murale pendant l'attente la prolonge, une avance l'abrège d'autant : une lecture ne part ni avant son instant
   planifié (avant CB-18b, un recul de 1 s la faisait partir 1 s trop tôt : mesures du worker et du réviseur des
   corrections de la tranche B, rejouées) ; après une avance, elle part au plus un pas après que l'horloge murale a
   atteint son instant, et une avance qui franchit cet instant la fait partir à la relecture suivante, retard que
   `retard_max` journalise. `d2.retard_max` reste donc positif ou nul ; une valeur négative ne peut venir que d'un
   recul entre la dernière lecture de l'horloge et le départ. La règle de validité du recalcul lit `retard_max` et
   `horloges` (§11.6).
9. **Plan câblé** (CB-18b, SHOGEN-S2BIS-PLAN-CABLAGE-1) : la boucle refuse à sa construction un plan dont un nom n'a
   pas de lecture (`BOUCLE/plan`), et le planificateur plus de cinq lectures sur un hôte (`BOUCLE/hote`) ; avant
   CB-18b, un tel nom donnait `panne_transport` de sous-type `autre` à chaque fenêtre (O-6 de la G2 de la tranche B).

## 12. Résultat d'une requête DNS (CB-10 ; E-C-27, E-C-28)

Les sondes D-4 et D-5 de l'enregistrement `sante` (§13) portent chacune le résultat d'une requête DNS en UDP, objet de
champs :
- `statut` : `reponse` (une réponse retenue), `delai` (aucune réponse retenue avant le délai), `forme` (adresse qui
  n'est pas une IPv4 littérale canonique, requête impossible, réponse appariée de plus de 512 octets ou mal formée) ou
  `reseau` (envoi refusé par le système) ;
- `rcode` : code de réponse (entier de 0 à 15 ; 0 NOERROR, 3 NXDOMAIN) ; `tc` : drapeau de troncature ; null tous deux
  sans réponse retenue ;
- `reponses` : liste de la section réponse, chaque élément `[nom, type, ttl, données]` : `nom` en texte terminé par
  un point ; `type` entier (1 A, 6 SOA, 16 TXT) ; `ttl` entier en secondes ; `données` : pour A, l'adresse en
  notation pointée ; pour TXT, la liste des chaînes (octets lus en latin-1) ; pour SOA, `[mname, rname, serial,
  refresh, retry, expire, minimum]` ; pour tout autre type, null. Null sans réponse retenue, et null quand le drapeau
  TC est posé (ci-dessous) ;
- `debut`, `fin` : instants de l'envoi et de la fin de l'attente, en microsecondes, sur l'horloge murale ; le délai se
  compte sur l'horloge monotone (C-4).

Une réponse est **appariée** si elle porte l'identifiant de la requête (tiré au hasard sur 16 bits), le bit QR, une
seule question et la même, casse ignorée (RFC 1035 §4.1.1-4.1.2, §7.3 ; casse : §2.3.3) ; elle est alors retenue, ou
`forme` si la suite est mal formée. Le lot exige en outre qu'elle vienne de l'adresse et du port interrogés : c'est un
**choix du lot**, non une règle de la RFC 1035, dont le §7.3 note que des serveurs répondent depuis une autre adresse
que celle qui a reçu la requête. Une telle réponse est ignorée, et la sonde finit en `delai` : un échec D-4 ou D-5 que
le rodage mesure (contre-contrôle de CB-11h).
**Taille** (C-1 (a) de la relecture d'intégration de P1, diff CB-19a) : une réponse appariée de plus de 512 octets est
`forme`, rien n'en est gardé. RFC 1035 §2.3.4 : « UDP messages 512 octets or less » ; §4.2.1 : « Messages carried by
UDP are restricted to 512 bytes (not counting the IP or UDP headers). Longer messages are truncated and the TC bit is
set in the header. » Le datagramme est reçu entier (65 535 octets au plus) avant ce contrôle, qui suit l'appariement :
un datagramme non apparié reste ignoré, quelle que soit sa taille. La borne est celle de l'UDP : `analyser` ne la porte
pas. Avant C-1, une seule réponse appariée de 65 502 octets (un nom de 255 octets, puis 4 076 pointeurs vers lui)
donnait une `sante` de 6 209 510 octets, au-delà de LIMITE (§7.1) : refus `JOURNAL/taille`, arrêt à chaque fenêtre.
Tout autre datagramme (écho de la requête, réponse à une autre question, datagramme trop
court) est ignoré, et l'attente continue jusqu'au délai (C-2). La requête ne passe par aucune résolution : l'adresse
est une IPv4 littérale **canonique** (quatre entiers décimaux pointés, sans zéro de tête : forme rendue par
`ipaddress`) ; toute autre valeur (nom, forme abrégée comme « 127.1 », null) donne `forme`, sans exception, sans
résolution et sans envoi (ADR-0029 l.109).
**Troncature** (CB-12a, SHOGEN-S2BIS-DNS-TC-1 ; O-4 de la G2 de la tranche B) : une réponse appariée au drapeau TC est
retenue, `statut` `reponse`, `rcode` lu, `tc` vrai ; sa section réponse, coupée par définition (RFC 1035 §4.2.1, cité
plus haut), n'est pas lue : `reponses` null. Avant CB-12a, une réponse coupée au milieu d'un enregistrement donnait
`forme`, drapeau perdu. Le client ne fait aucun repli en TCP (choix du lot, admis pour D-4 et D-5 par la G2 de la
tranche B) : le drapeau se lit au recalcul, et le relevé ASN (§15.4) tient une résolution tronquée pour une adresse non
obtenue, sans repli en TCP non plus (Q-3 de la G2 de P2A, adjugée le 2026-10-08 ; taux de troncature mesuré au rodage :
SHOGEN-S2BIS-ASN-TRONCATURE-1). **Identifiant** (CB-12a, SHOGEN-S2BIS-DNS-ID-16BITS-1 ; O-10) : entier de 0 à 65 535 ;
tout autre identifiant (injecté par un test, booléen compris) est un refus nommé de la requête (`requête DNS invalide :
identifiant`), donc `forme` pour `interroger`, qui ne lève pas (avant CB-12a : `struct.error`, non nommé).

## 13. Enregistrement `sante` complet (CB-11 ; E-C-25 à E-C-29)

1. Un enregistrement `sante` par fenêtre lue, avant le marqueur. Ses clés forment une **liste blanche fermée** :
   `type`, `ws`, `seq`, `prec`, `d2`, `fils`, `horloges` (§11.6), `d3`, `d4`, `d5`, `disque`, `resolveur`. Aucune clé
   n'est tirée d'une lecture de source ; aucun champ ne porte de jugement (« dégradé » se juge au recalcul et dans
   `status`, avec les seuils scellés, E-C-26). Une boucle construite sans sondes (tests de la boucle seule ; boucle de
   la carte, §15.3) écrit la même liste : `d3`, `disque` et `resolveur` null, `d4` et `d5` vides (O-7).
2. **Instant des sondes** (Q-C-03) : les sondes D-3, D-4 et D-5 partent au départ D = ws + w − δ, chacune sur son fil,
   hors du pool des lectures ; la boucle les attend avec les lectures, jusqu'à l'échéance au plus. Une sonde encore en
   cours au relevé de l'échéance (§11.4, avant toute écriture) vaut null, de même qu'une sonde finie après E (règle
   `fin` > E des lectures, CB-18b, SHOGEN-S2BIS-SONDES-ECHEANCE-1) : la fin de chaque sonde est relevée sur l'horloge
   monotone de la boucle, sans être journalisée, et comparée à E rapportée à cette horloge au relevé (instant monotone
   du relevé, moins son retard sur E à l'horloge murale). Une sonde dont l'instance précédente n'a pas
   rendu **n'est pas relancée** (C-5) : elle vaut null dans la fenêtre, et repart à la première fenêtre où l'instance
   précédente a rendu ; une sonde qui lève vaut null et repart de même. Le nombre d'instances encore en cours est
   journalisé (`fils.sondes`, §11.6) : les fils de sonde restent bornés, au plus un par sonde.
3. `d3` : sortie brute de la commande d'horloge scellée (configuration de l'observateur ; relevé chrony, ADR-0029
   l.83 et l.108) : `{sortie, code, debut, fin}`, où `sortie` est la sortie standard lue en UTF-8 (octet invalide
   remplacé par U+FFFD), 4 096 caractères au plus, et `code` le code de sortie ; ou `{erreur, debut, fin}`, `erreur`
   valant `absente` (commande introuvable), `delai` (plus de 2 s) ou `autre`. Le collecteur n'analyse pas cette
   sortie : la borne d'erreur, le statut et l'âge du relevé se lisent au recalcul.
4. `d4` : liste, dans l'ordre des témoins scellés, de `{adresse, …}` : adresse IPv4 littérale du témoin, puis le
   résultat de la requête SOA de « . » sans récursion, délai de 2 s (§12). `d5` : liste, dans l'ordre des noms
   scellés, de `{nom, …}` : le nom témoin, puis le résultat de sa requête A, avec récursion, au résolveur de
   l'observateur, délai de 2 s (§12).
5. `disque` : `{total, libre}` du système de fichiers du journal, en octets (`libre` : blocs disponibles pour un
   utilisateur ordinaire) ; ou `{erreur}` (nom de l'exception). `resolveur` : sha256 des octets de la configuration
   du résolveur de l'observateur (`/etc/resolv.conf` par défaut), null si elle ne se lit pas.
6. **Taille** (C-1 (b) de la relecture d'intégration de P1, diff CB-19b) : sept témoins et sept noms au plus
   (`sante.json`, §14.1) ; la plus grande `sante` possible fait au plus 3 823 224 octets, sous LIMITE (4 194 304
   octets, §7.1), marge de 371 080 octets. Calcul (détail : METRIQUES, section CB-19b) :
   - `reponses` d'une sonde : la réponse retenue fait 512 octets au plus (§12), dont 17 au moins d'en-tête et de
     question. Un nom décodé y a au plus 2 × 512 = 1 024 caractères : chaque pointeur vise avant le début du segment
     courant, si bien que les segments lus ne se chevauchent pas, hormis le dernier, qui ne chevauche que le
     précédent. Le sérialiseur écrit un caractère en six octets au plus (caractère de contrôle). Une réponse donne
     ainsi au plus (18 × 1 024 + 85) / 36 octets de JSON par octet du message qu'elle occupe, maximum atteint par une
     SOA dont les trois noms sont des pointeurs (36 octets) : `reponses` fait au plus 1 + 495 × (18 × 1 024 + 85) / 36
     octets, moins de 254 610 ;
   - témoin du calcul (test `test_sante.Taille`) : chaque sonde porte 14 réponses SOA dont les trois noms ont 1 024
     caractères de contrôle (259 239 octets, au-delà de la borne) ; tout autre champ est à sa borne : `sortie` de D-3
     en 4 096 caractères de contrôle, noms de D-5 en 253, `tardives` de 2 × 4 096 latences, entiers à leur plus longue
     écriture (instants de 17 caractères, écarts de 18, comptes de 19 chiffres, `seq` de 640) ;
   - hypothèse : `tardives` compte au plus 2 × `places` latences. Les lectures abandonnées au relevé précédent tiennent
     chacune une place, sauf celles de la fenêtre précédente finies entre son échéance et son relevé (au plus une par
     forme, et `places` ≥ formes). Depuis CB-6d (SHOGEN-S2BIS-TARDIVES-BORNE-1), le résultat d'une lecture est rendu
     avant sa place : une lecture dont le résultat n'est pas rendu tient sa place, sans exception ; la marge admet
     encore 19 530 latences.

## 14. Configurations, descripteur, câblage et point d'entrée (CB-18c, CB-18d ; E-C-02, E-C-16, E-C-23)

1. **Fichiers chargés** : chacun est lu en octets, son sha256 calculé sur ces octets, puis contrôlé (champs exacts,
   types, bornes, puis règles de cohérence nommées) :
   - `formes.json`, configuration scellée de la boucle : `w` (s, divise 3 600), `delta`, `tolerance`, `delai`,
     `marge` (µs ; `marge` < `delta` ≤ w·10⁶), `places` (taille du pool), `formes` : liste de `{nom, hote, port,
     chemin, methode, corps, espace, decodeur}` (noms uniques ; `GET` sans corps ou `POST` avec corps ; `espace` vrai :
     la limite de l'hôte impose l'espacement de 1 s entre ses lectures, même valeur pour toutes les formes d'un hôte ;
     `decodeur`, CB-6c : nom d'un décodeur de la liste fermée du code, règle `decodeur-connu`, qui lit le corps de
     chaque lecture `ok` de la forme, §9.1).
     `tolerance` est la tolérance de départ de D-2 : 5 s en production (ADR-0029 l.107, reformulée par l'ajout daté
     du 2026-10-04 17:03:38 UTC au §6 : « plus de 5 s après son instant planifié »). Règle `budget` (budget de
     l'ADR-0029 l.233-234 ; CB-18g, C-1 de la G2 de la tranche C) : `tolerance` + plus grand décalage du plan +
     `delai` + `marge` ≤ `delta`, égalité admise (en production, 5 + 4 + 10 + 1 = 20 ≤ 20 s) ; une lecture partie
     dans la tolérance finit ainsi avant l'échéance (§11.1). Avant C-1, la règle omettait la tolérance. Règles de
     forme (CB-18h, SHOGEN-S2BIS-CONFIG-REGLES-1) : `places` ≥ nombre de formes (`places-formes` : le pool est
     dimensionné sur le nombre de lectures, ADR-0029 l.234) ; `hote` de forme `[a-z0-9.-]{1,253}` (`hote-forme` :
     minuscules, chiffres, « . » et « - » seuls, même règle que le recalcul, Q-RB-13 de sa tranche 1) ; `chemin`
     de forme « / » suivi d'ASCII imprimable sans espace (`chemin-forme`, choix du lot : la lecture refuserait tout
     autre chemin à chaque fenêtre, §10.4) ;
   - `sante.json`, configuration scellée des sondes : `commande` (D-3, liste d'arguments), `temoins` (D-4, IPv4
     littérales canoniques, sept au plus), `noms` (D-5, noms DNS valides, sept au plus ; bornes du §13.6), `delai`
     (µs ; `delai` + `marge` ≤ `delta`, égalité admise : les sondes sont jointes avant l'échéance) ;
   - le **descripteur** de l'observateur, écrit au premier démarrage (lot DEPLOI-BIS) : `observateur` (de forme
     `[a-z0-9]{1,16}`, règle `observateur-nom`, CB-15c : il nomme ses fichiers au dépôt, §16.4 ; minuscules seules,
     C-6 de la G2 de P2B : un jumeau de casse n'est pas un autre observateur), `fournisseur`,
     `region`, `asn` (mesuré), `resolveur` (IPv4 littérale canonique, cible de D-5), `config_resolveur` (chemin de la
     configuration du résolveur, dont l'empreinte va à `sante.resolveur`), `versions` (paquets), `empreinte` (sha256
     de la configuration déployée, 64 chiffres hexadécimaux minuscules).

   Le commit est celui, scellé, de l'archive déployée : 40 chiffres hexadécimaux minuscules (aucune opération git sur
   l'observateur). Tout écart est un refus nommé (`CONFIG/…` ou `BOUCLE/…`), levé avant l'ouverture du journal.
2. **Câblage** (SHOGEN-S2BIS-PLAN-CABLAGE-1) : une lecture par forme ; plan par hôte (§11.1) ; sondes construites
   depuis `sante.json`, dirigées vers le résolveur du descripteur, disque relevé sur le dossier du journal ; la boucle
   tourne toujours avec ses sondes (§13.1 : une `sante` sans sondes n'existe que dans les tests de la boucle seule et
   au journal du processus secondaire, §15.3).
3. **Commande** (CB-18d) : `python3 -m shogen_s2bis.collecte pool --formes F --sante S --descripteur D --journal
   DOSSIER --commit SHA` (code de référence : `s2bis/shogen_s2bis/collecte/entree.py`). `--fenetres N` arrête après N
   fenêtres (essais) ; sans elle, la boucle tourne sans fin, sous systemd. `--depot DOSSIER` (CB-15c) : dépôt des
   têtes (§16) ; sans elle, ni enregistrement `tetes` ni export. Un refus de configuration donne la sortie 2
   et `collecte : refus : <code> : …` sur la sortie d'erreur, sans rien écrire.
4. **`run_params`** (CB-18d), écrit à chaque démarrage, aussitôt le journal ouvert, à la première fenêtre admise :
   `commit`, `sha256` (`{formes, sante, descripteur}` : sha256 des octets lus), les contenus `formes` (dont
   `tolerance`, CB-18g), `sante` et `descripteur`, `python` (version de l'interpréteur). Une fenêtre qui porte
   `run_params` puis n'a pas de marqueur est déclarée par le `trou` suivant (§8).
5. **Fermeture** (CB-18d, SHOGEN-S2BIS-ECRIVAIN-USAGE-1) : le journal est fermé à la sortie du point d'entrée, quelle
   qu'elle soit. Une OSError ou un refus de l'écrivain (`JOURNAL/casse` compris, et toute ouverture refusée) arrête la
   boucle : sortie 1, refus nommé (`collecte : arrêt : <code> : …`) ; systemd relance le service, et l'instance
   suivante reprend le journal (§7). Sortie 0 : les N fenêtres demandées sont écrites.

## 15. Processus secondaire : carte et relevé ASN (CB-12b, CB-13 ; E-C-30 à E-C-33)

1. **Isolement** (E-C-32 ; ADR-0029 l.235, AQT Q1) : la carte et le relevé ASN tournent dans un processus distinct de
   celui du pool (service systemd à lui, borné en mémoire par `MemoryMax` : lot DEPLOI-BIS), avec son pool de fils et
   son propre journal chaîné, au préfixe `secondaire` (fichiers `secondaire-AAAA-MM-JJ-k.jsonl`, verrou
   `secondaire.verrou`), du même format que celui du pool (§1 à §8) et sur sa grille (même w) ; sa tête entre dans
   l'échange des têtes et le jeton quotidien (CB-15). Le pool ne lit rien du secondaire : un refus,
   un arrêt, une lecture pendue de la carte n'écrivent rien au journal du pool, ni D-1 à D-5 ni son marqueur
   (`s2bis/tests/test_secondaire.py`, `Isolement` : les deux processus ensemble, carte pendue, carte refusée).
2. **`carte.json`** (CB-13b), configuration scellée : `depart`, `delai`, `marge` (µs), `places` (pool de fils de la
   carte), `asn` (`{periode, decalage}`, s ; `periode` de 86 400 s au plus : relevé au moins quotidien, E-C-30) et
   `formes`, liste de formes du §14.1, vide admise (sans source prête au gel, le processus relève l'ASN seul). Règles
   des formes du pool (§14.1 : `noms-uniques`, `methode-corps`, `hote-forme`, `chemin-forme`, `espace-par-hote`,
   `places-formes`, `decodeur-connu`), puis règles croisées avec `formes.json` du pool, que le secondaire charge aussi
   (son sha256 entre au `run_params` du secondaire, à comparer à celui du `run_params` du pool) :
   - `budget-partage` (E-C-33) : sur chaque hôte, les lectures du pool et de la carte, ensemble, sont au plus 5 par
     fenêtre (borne du §11.1) : un hôte présent aux deux garde un seul budget de débit, les limites lues étant par
     adresse (ADR-0029 l.234). Règle scellée (Q-1 de la G2 de P2A, adoptée le 2026-10-08) : un plafond, que le G0 de
     la carte (ADR-0029 l.235, SHOGEN-S2BIS-CARTE-AVEUGLE-1) peut serrer hôte par hôte, sur les limites lues ;
   - `espace-partage` : un hôte présent aux deux porte le même `espace` ;
   - `hors-delta` (E-C-32) : `depart` + plus grand décalage du plan de la carte + `delai` ≤ w·10⁶ − `delta` du pool,
     égalité admise : toute lecture de la carte finit avant le départ du pool ;
   - `marge-carte` : `depart` + plus grand décalage + `delai` + `marge` ≤ w·10⁶, égalité admise (budget du §14.1, sans
     tolérance : la carte n'a pas de D-2) ;
   - `cadence` : `periode` et `decalage` multiples de w, `decalage` < `periode`.

   En production, `depart` vaut 5 s (E-C-32, valeur scellée). Tout écart est un refus nommé (`CONFIG/…`), levé avant
   l'ouverture du journal.
3. **Boucle de la carte** : celle du pool (§11), départ D = ws + `depart` (δ de la carte : w − `depart`), échéance
   E = ws + w − `marge`, `places` de la carte, une lecture par forme au `delai` de la carte, décodée par le décodeur de
   sa forme (§9.1), et sans sondes : la `sante` porte les champs des sondes nuls ou vides (§13.1). Mêmes
   enregistrements `lecture`, `sante` et marqueur qu'au §11.
4. **Relevé ASN** (E-C-30, E-C-31 ; Q-C-04 ; CB-12b, CB-13a) : les hôtes relevés sont ceux du pool et de la carte,
   dans l'ordre des points de code. Un relevé est dû à la première fenêtre de chaque exécution, puis à la première
   fenêtre lue qui suit un instant de la cadence (ws mod `periode` = `decalage`) : un instant sauté, dans une fenêtre
   sautée ou pendant un arrêt, est rattrapé à la fenêtre lue suivante ou au redémarrage (C-4 de la G2 de P2A ;
   ADR-0029 l.247 : relevé quotidien), en mémoire seule, sans relecture du journal (E-C-15). Un enregistrement
   `releve_asn` (champs `hotes`, `lance`) note le relevé dû ; `lance` est faux si le relevé précédent n'a pas rendu :
   celui-ci est alors sauté (un fil de relevé au plus). Le relevé tourne sur un fil démon, jamais sur
   le fil qui écrit ; chaque hôte relevé est écrit en `asn` par le fil de la boucle, en tête de la première fenêtre qui
   suit son rendu (avant le `releve_asn` de cette fenêtre, s'il y en a un), dans l'ordre des hôtes. Champs de `asn` :
   - `hote` ;
   - `a` : résultat DNS (§12) de la requête A de l'hôte au résolveur du descripteur, récursion demandée (jamais
     1.1.1.1, ADR-0029 l.82) ;
   - `ip` : première adresse de type A de la section réponse ; null sans réponse retenue, sans A, ou sous le drapeau TC
     (`reponses` null, §12) ;
   - `ripestat` : null sans `ip` ; sinon les champs d'une `lecture` (§9.1) de
     `https://stat.ripe.net/data/prefix-overview/data.json?resource=<ip>`, dont `valeurs`, au statut `ok`, est
     `{asn, detenteur, prefixe}` : `data.asns[0].asn` et `.holder`, `data.resource` (forme de S2, r2.py l.275-289) ;
     `asn` et `detenteur` null si `asns` est vide ; `asn`, entier ou texte décimal lu comme `int()` de S2, de 0 à 2³²
     exclu ; 4 096 octets canoniques au plus ; tout autre corps : `panne_decode` ;
   - `cymru` : null sans `ip` ; sinon le résultat DNS (§12) de la requête TXT de `<d>.<c>.<b>.<a>.origin.asn.cymru.com.`
     au même résolveur, plus `asn` : premier nombre du premier champ (avant « | ») de la première chaîne de la première
     réponse TXT qui en a un, de 0 à 2³² exclu (forme de S2, `_cymru_asn` l.292-312) ; null sinon.

   Un défaut imprévu du relevé d'un hôte donne un `asn` à `a`, `ip`, `ripestat` et `cymru` nuls, et le relevé
   continue. Aucun jugement : la concordance des deux bases se juge au recalcul (E-R-29).
5. **Taille** : le plus grand `asn` (A et TXT au plus grand résultat du §13.6, corps RIPEstat de 1 048 576 octets,
   valeurs à leur borne, hôte de 253 caractères) fait moins de 2 000 000 octets, sous LIMITE (§7.1) : témoin
   `test_asn.Decodage.test_plus_grand_releve_sous_limite`.
6. **Commande** (CB-13b) : `python3 -m shogen_s2bis.collecte secondaire --formes F --carte C --descripteur D --journal
   DOSSIER --commit SHA` ; `--fenetres`, sorties, refus et fermeture comme aux §14.3 et §14.5 ; `run_params` comme au
   §14.4, `sha256` et contenus `{formes, carte, descripteur}`.

## 16. Têtes, dépôt et jeton quotidien (CB-15 ; E-C-35, E-C-36)

Rattachement : ADR-0029 l.218 et l.240 (jeton RFC 3161 quotidien, échange des têtes), AVIS du G0, Q-D-03 (chaque
observateur horodate chaque jour sa propre tête, et celles des autres quand elles sont lisibles ; le « dépôt » est un
dossier, lisible ou non). Code de référence : `s2bis/shogen_s2bis/collecte/tetes.py`. RFC 3161 lue au fichier du
registre (`biblio/ietf-rfc3161-time-stamp-protocol-2026-10-04.txt`, sha256 `39fd1764…8240`) ; les règles DER
(X.690) et l'identifiant de SHA-256 ne sont pas détenus : leurs octets sont ceux d'OpenSSL 3.0.13, mesurés.

Le dépôt est un dossier **local** de l'observateur (C-7 de la G2 de P2B ; Q-2) : la boucle y lit et y écrit sur son fil
(lecture des têtes, export), et un montage réseau pendu l'y bloquerait, ce qu'E-C-15 interdit ; l'échange avec les
autres observateurs (têtes, jetons, résumés) est le fait d'une unité séparée qui synchronise ce dossier (DB-4), hors du
collecteur.

1. **Requête d'horodatage** (CB-15a ; RFC 3161 §2.4.1) : `TimeStampReq` en DER : `version` 1 ; `messageImprint` :
   algorithme SHA-256 (OID 2.16.840.1.101.3.4.2.1, paramètres NULL), empreinte de 32 octets ; `nonce`, entier de 0 à
   2^64 − 1, s'il est donné ; `certReq` vrai ; ni `reqPolicy` ni `extensions`. Sans nonce, les octets sont ceux de
   `openssl ts -query -data <fichier> -sha256 -cert -no_nonce` (`test_tetes`). Une empreinte qui n'a pas 32 octets,
   un nonce hors de ces bornes : refus nommés `JETON/empreinte`, `JETON/nonce`.
2. **Statut d'une réponse** (RFC 3161 §2.4.2) : la réponse est une SEQUENCE qui couvre ses octets ; son premier élément,
   `PKIStatusInfo`, une SEQUENCE, commence par `PKIStatus`, INTEGER d'un octet de 0 à 5 ; le jeton (`TimeStampToken`,
   une SEQUENCE qui finit la réponse) est présent si et seulement si le statut vaut 0 ou 1. Longueurs : forme courte
   sous 128 octets, forme longue minimale de 1 à 4 octets au-delà. Tout autre cas est le refus `JETON/reponse`.
   **Liaison du jeton à la requête** (CB-15d ; C-1 de la G2 de P2B ; RFC 3161 §2.2 : « If any of the verifications above
   fails, the TimeStampToken SHALL be rejected » ; §2.4.1, §2.4.2) : le jeton est un `ContentInfo` de type id-signedData
   (1.2.840.113549.1.7.2) dont le `SignedData` encapsule un contenu de type id-ct-TSTInfo (1.2.840.113549.1.9.16.1.4)
   (octets des deux identifiants relevés par `openssl asn1parse`) ; au `TSTInfo`, l'algorithme du `messageImprint` est
   SHA-256 aux paramètres NULL et son empreinte celle de la requête (sha256 du manifeste, point 3) ; son `nonce` est
   celui de la requête, absent si la requête n'en porte pas (plus strict que la RFC, qui ne l'interdit pas). Un chemin
   DER illisible est le refus `JETON/reponse`, un écart le refus `JETON/liaison`. Ne sont pas contrôlés ici, limite
   déclarée : la signature et le certificat de la TSA (aucune vérification RSA ni ECDSA en bibliothèque standard ; ils
   se contrôlent hors ligne, `openssl ts -verify -queryfile`, comme `scripts/sceau/verify.sh`) ; le `genTime` (le nonce
   porte la fraîcheur, RFC 3161 §2.2).
3. **Manifeste du jour** : ligne JSON canonique (§1.2) `{jour, observateur, tetes}` : `jour`, jour UTC (AAAA-MM-JJ) ;
   `observateur` ; `tetes` : les têtes lues au dépôt, triées par observateur puis journal. Son sha256 est l'empreinte
   de la requête.
4. **Fichier de tête** (CB-15b ; E-C-35) : au dépôt, `<observateur>-<journal>.tete` (observateur `[a-z0-9]{1,16}`,
   journal `[a-z]{1,16}`, préfixe du journal), une ligne JSON canonique `{journal, observateur, seq, sha256, ws}` :
   la tête (§1.4) du point de contrôle (`point`, §2) de la fenêtre `ws`. Elle est écrite à chaque point de contrôle,
   par écriture atomique : fichier temporaire `.<nom>.tmp` écrit et synchronisé, renommé, dossier synchronisé ; un
   lecteur voit l'ancien fichier ou le nouveau, jamais un fichier partiel. Un échec de l'export ne lève pas : il est
   noté par le nom de son exception et porté par l'enregistrement `tetes` suivant (point 5).
5. **Lecture du dépôt** (CB-15b) : les fichiers de tête dont le nom suit la grammaire du point 4, sauf celui du journal
   qui lit, sont lus dans l'ordre des noms : ceux de l'observateur qui lit d'abord, 16 au plus, puis ceux des autres, 16
   au plus (CB-15d, C-2 de la G2 de P2B : sa tête est ancrée quoi qu'il arrive au dépôt, AVIS Q-D-03, point 1) ; chacun
   est une tête valide ou un refus nommé, un seul par fichier : `TETES/lecture` (fichier illisible), `TETES/taille`
   (plus de 1 024 octets), `TETES/forme` (pas une ligne JSON canonique aux clés exactes, ou entier de plus de 640
   chiffres), `TETES/champs` (observateur ou journal autre que ceux du nom, `seq` ou `ws` qui n'est pas un entier de 0 à
   10^18 − 1, ou de 0 à 10^12 − 1, `sha256` qui n'a pas 64 chiffres hexadécimaux minuscules) ; dossier illisible :
   `TETES/depot`. Champs rendus : `tetes` (têtes valides, les siennes d'abord), `refus` (`[nom, code]`), `ignores`
   (fichiers au-delà de ces bornes), `jeton` (CB-15e : `{fichier, sha256}` du dernier `<observateur>-<jour>.tsr` du
   dépôt par ordre des noms, ou null ; un `.tsr` illisible : refus `TETES/lecture`), `export` (échec du dernier export
   ou null). Toute valeur rendue est admise par l'écrivain : un dépôt hostile ne fait jamais refuser l'enregistrement
   (SHOGEN-S2BIS-ECRIVAIN-REFUS-ARRET-1).
6. **Enregistrement `tetes`** (CB-15c ; E-C-35) : avec un dépôt, la fenêtre qui clôt l'heure ((`ws` + w) multiple de
   3 600) porte, après ses `lecture` et avant sa `sante`, un enregistrement `tetes` dont les champs sont ceux de la
   lecture du dépôt (point 5), faite au relevé de l'échéance : les têtes des autres journaux sont consignées dès leur
   lecture. Après le marqueur et le point de contrôle, la tête du point, celle que rend l'écrivain, est exportée
   (point 4). Sans dépôt, ni l'un ni l'autre.
7. **Jeton du jour** (CB-15d ; E-C-36 ; AVIS Q-D-03, point 1) : un `<observateur>-<jour>.tsr` présent au dépôt : « déjà
   émis », rien n'est redemandé. Sinon : manifeste (point 3) des têtes valides du dépôt (point 5, les siennes d'abord,
   hors de la borne des autres ; aucune exclue ; sans tête de l'observateur, refus `JETON/tete`, rien n'est écrit),
   écrit en `<observateur>-<jour>.manifeste`, puis requête (point 1, au nonce donné) en `<observateur>-<jour>.tsq`, par
   écriture atomique (point 4). L'envoi ne part que si une fonction d'envoi est donnée (armement : point 8) ; sans elle,
   « non armé ». Armé, la réponse dont le statut (point 2) vaut 0 ou 1 et dont le jeton est lié à la requête (point 2,
   liaison) est conservée en `<observateur>-<jour>.tsr` (« émis ») ; un autre statut : refus `JETON/rejet` ; une réponse
   mal formée : `JETON/reponse` ; le jeton d'une autre requête (autre empreinte, autre nonce, sans nonce, autre
   algorithme) : `JETON/liaison` ; dans ces trois cas, rien n'est conservé et le jour reste à demander. Le sha256 du
   `.tsr` est journalisé par le `tetes` suivant (point 5).
8. **Commande `jeton` et envoi** (CB-15e ; E-C-36) : `python3 -m shogen_s2bis.collecte jeton --descripteur D --depot
   DOSSIER [--jour AAAA-MM-JJ] [--envoi URL]` : jour UTC de l'horloge par défaut ; observateur du descripteur (§14.1,
   contrôlé) ; nonce de 64 bits tiré à chaque requête (`secrets.randbits(64)`, figé par le test de la commande : C-5 de
   la G2 de P2B ; RFC 3161 §2.4.1, « e.g., a 64 bit integer »). L'envoi n'est armé que par `--envoi`, URL https de la
   TSA, que le déploiement ne pose que sous le go écrit de l'investisseur (ADR-0029 l.218) ; sans elle, rien ne part.
   Armé : POST de la requête, `Content-Type: application/timestamp-query` (RFC 3161 §3.4), aucune redirection suivie ;
   une réponse 200 d'au plus 65 536 octets passe au point 7, un autre code ou une réponse plus longue est le refus
   `JETON/http` ; une URL qui n'est pas https : `JETON/url`. Sortie : 0 et `jeton : <état> : <fichier> : sha256
   <empreinte>` ; 1 et `jeton : refus : <code> : …` (refus, erreur du réseau ou du dépôt) ; 2 pour un descripteur ou un
   jour refusé.

## 17. Commande `status` (CB-17 ; E-C-38)

Rattachement : ADR-0029 l.244 (« une commande `status` scellée n'imprime que la santé (D-1 à D-5, dernier marqueur,
tête de chaîne, espace disque) et le compte de fenêtres évaluables : aucun statut de source, aucun prix »), §2.3
(critères D-1 à D-5) ; PROPOSITION E-C-26, E-C-38 ; AVIS du G0, Q-D-03, points 2 et 3. Code de référence :
`s2bis/shogen_s2bis/collecte/status.py`.

1. **Lecture** (CB-17a) : le journal du pool est lu sans rien écrire ni prendre le verrou de l'écrivain (§5) : la
   lecture peut se faire pendant la collecte. Fichiers dans l'ordre (jour, k entier) de la grammaire du §6.1 ; aucun :
   refus `STATUS/journal`. Une ligne qui commence par `{"adresse":`, première clé de toute `lecture` en forme canonique
   (§1.2, §9.1, §11.2) et d'aucun autre type, est une `lecture` : elle n'est jamais décodée, et rien d'une lecture
   n'entre au jugement. Les autres lignes sont décodées ; un fichier s'arrête à sa première ligne coupée, illisible,
   sans `type` chaîne ni `seq` entier, ou d'un jour postérieur à celui de son fichier : `ws` à la fin du jour du nom du
   fichier ou au-delà, `suivante` au-delà (§6.1 : aucune fenêtre n'est d'un jour postérieur à celui de son fichier ;
   CB-17c, C-3 de la G2 de P2B). Un fichier dont le jour n'est pas au calendrier n'est pas lu. La chaîne n'est pas
   contrôlée : l'intégrité se juge au recalcul (RB-1, RB-18).
2. **Jugement d'une santé** (CB-17a ; ADR-0029 §2.3 ; seuils égaux au bloc `degradation` de
   `s2bis/config/analyse.json`, contrôlé par un test) : D-1, aucune `sante` lisible ; D-2, `d2.non_parties` non nul ou
   `d2.retard_max` au-delà de 5 s (règle Q-C-02 de l'AVIS, §11.6) ; D-4, au moins 2 témoins dont le résultat n'est pas
   une réponse retenue (`statut` autre que `reponse`, ou null) ; D-5, au moins 2 noms témoins non résolus (pas de
   réponse retenue, `rcode` non nul, ou aucune réponse de type 1, A). **D-3 n'est pas jugé** : le format de la sortie
   de `chronyc` n'est pas lu sur pièce (SHOGEN-S2BIS-CHRONYC-FORMAT-1, ouvert) ; est relevé, à part, un relevé D-3
   absent, en erreur ou de code non nul.
3. **État par fenêtre** (CB-17b) : sont jugées les fenêtres de w = 60 s (§3.1) de la première que le journal admet
   (`suivante` de son premier enregistrement), jamais avant le jour du premier fichier présent moins un jour (segment de
   reprise, §6.1 ; CB-17c, C-3 : un chiffre corrompu ne gonfle pas la grille), au dernier marqueur ; une fenêtre sans
   marqueur vaut D-1 ; une fenêtre close prend les codes de sa `sante` (point 2). Une fenêtre est **valide** si elle n'a
   aucun code. La tête est celle du dernier enregistrement lu hors `lecture`. Limites : seuls les fichiers présents sont
   lus (la rétention locale de 7 jours en retire, ajout daté du 2026-10-04 17:03:38 UTC à l'ADR-0029, point 2) ; la
   grille est celle de w = 60 s.
4. **Commande et rapport** (CB-17b) : `python3 -m shogen_s2bis.collecte status --journal DOSSIER` : sortie 0 et le
   rapport ; sortie 1 et `status : refus : …` (refus `STATUS/journal`, ou dossier illisible). Rapport, une ligne par
   rubrique : `status : journal « pool », lecture seule` ; `fenêtres : de <début> à <fin> UTC, <n> ; dernier marqueur :
   <fin> UTC` ; `tête : seq <s>, sha256 <h>` ; `disque : <libre> octets libres sur <total>` (dernière `sante`) ;
   `dégradations : D-1 <n> ; D-2 <n> ; D-3 non jugé (… ; relevé absent ou en erreur : <n>) ; D-4 <n> ; D-5 <n>` ;
   `dernière fenêtre : valide` ou `dégradée (<codes>)` ; `fenêtres valides hors D-3 (compte local) : calme <n> ; stress
   <n>` (strates : stress le samedi et le dimanche UTC, calme sinon, ADR-0029 l.196 ; « hors D-3 » : D-3 n'est pas jugé,
   point 2, tant que SHOGEN-S2BIS-CHRONYC-FORMAT-1 est ouvert ; C-7 de la G2 de P2B, Q-9). Aucun nombre à virgule, aucun
   statut de source, aucune valeur lue : la sortie est la même avec ou sans enregistrements `lecture`.
5. **Résumé par jour** (CB-17c ; AVIS Q-D-03, point 2) : commande `python3 -m shogen_s2bis.collecte resume --journal
   DOSSIER --depot DOSSIER --descripteur D` ; pour chaque jour UTC des fenêtres jugées (point 3), le fichier
   `<observateur>-<jour>.resume` au dépôt (écriture atomique, §16.4), une ligne canonique `{jour, observateur,
   fenetres}`, `fenetres` : `[ws, codes]` de chaque fenêtre du jour (codes vides : fenêtre valide). Aucune autre clé :
   c'est la liste blanche du résumé, que l'orchestrateur peut lire au rodage (lectures admises, ADR-0029 l.221) ;
   aucun statut de source. Le résumé est une projection des enregistrements du journal : il se recalcule sur le
   journal. Sortie 0 et `resume : <fichiers>` ; 1 refus du journal ou du dépôt ; 2 refus du descripteur.
6. **Compte à quorum** (CB-17d ; AVIS Q-D-03, point 3) : `status --journal J --depot D --descripteur F` ajoute au
   rapport, après le compte local : `quorum hors D-3 (au moins 2 observateurs valides) : calme <n> ; stress <n>` et
   `résumés lus : <o> jusqu'à <heure> UTC (âge <n> s) ; …`, ou `quorum : aucun résumé d'un autre observateur lisible` ;
   puis, s'il y en a, `résumés refusés : <fichier> (<code>) ; …`. Sont lus les résumés des autres observateurs pour les
   jours des fenêtres locales ; un résumé est refusé, un seul code par fichier : `RESUME/taille` (plus de 131 072
   octets), `RESUME/forme` (pas une ligne canonique aux clés exactes), `RESUME/champs` (observateur ou jour autre que
   ceux du nom, fenêtre hors du jour ou de la grille, codes inconnus, non textes compris, en double ou non triés, aucune
   fenêtre), `RESUME/lecture` ; aucun résumé ne fait échouer `status`. Une fenêtre compte à quorum si M_j ≥ 2 (ADR-0029
   §2.2 pt 5) : un pour l'observateur s'il y est valide, plus un par autre observateur dont un résumé lu la dit valide.
   L'âge d'un résumé court depuis la fin de sa dernière fenêtre. `--depot` sans `--descripteur` : refus
   `CONFIG/options`, sortie 2.
