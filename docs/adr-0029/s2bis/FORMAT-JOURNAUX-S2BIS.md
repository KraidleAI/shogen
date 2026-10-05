# Format des journaux d'observateur de S2-bis

- **Rattachement** : ADR-0029 §2.9 (l.238-240 : journal à enregistrement unique, chaîné, `fsync` au marqueur, point de
  contrôle horaire, fichiers quotidiens clos et sommés ; format spécifié et scellé au paquet) ; PROPOSITION du G0
  (`docs/adr-0029/g0-collecte/`), exigences E-C-16 à E-C-24 ; principe de SHOGEN-FORMAT-JOURNAUX-1 (annexe B d'ADR-0028,
  l.55).
- **Statut** : texte tenu à jour à chaque sous-lot du collecteur ; il est scellé au paquet de S2-bis avec le commit du
  collecteur. Code de référence : `s2bis/shogen_s2bis/collecte/journal.py`. Le test de conformité d'un journal produit
  par le collecteur entier (E-C-24) est celui du sous-lot CB-18.
- **Corrections** : le diff CB-2d (2026-10-04) applique les corrections C-1, C-2 et C-6 (a) à (c) de la relecture G2
  de la tranche A de P1 (§2, §3.2, §4, §7.5, §8.1) ; le diff CB-2e applique C-3 (§8.4).

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
| `ouverture` | `jour` (AAAA-MM-JJ, UTC), `suivante` (première fenêtre ni close ni déclarée en trou) | l'écrivain : premier enregistrement d'un journal neuf, puis de chaque fichier quotidien (§6) |
| `marqueur` | `ws` ; champs de la boucle (CB-4) | `marqueur(ws)` : clôt la fenêtre `ws` |
| `point` | `ws` : fenêtre qui clôt l'heure, (`ws` + w) multiple de 3 600 | l'écrivain, juste après ce marqueur ; son empreinte est la tête exportée (E-C-35) |
| `cloture` | `jour` : jour UTC du fichier qu'il clôt | l'écrivain : dernier enregistrement d'un fichier quotidien (§6) |
| `reprise` | `ws` (fenêtre de l'horloge au redémarrage), `suivante`, `queue` | l'écrivain, au redémarrage (§7) |
| `trou` | `de`, `a`, `cause` | l'écrivain, juste avant le marqueur qui suit des fenêtres sans marqueur (§7) |
| tout autre type (`lecture`, `sante`, `run_params`…) | `ws` ; champs de son sous-lot | `ecrire(type, ws, …)` |

Les types `ouverture`, `marqueur`, `point`, `cloture`, `reprise` et `trou` sont réservés à l'écrivain. Un champ nommé
`seq` ou `prec` est refusé.

Tout refus est nommé (`JOURNAL/…`) et n'écrit rien (CB-2d, C-6 de la G2 de P1) : l'enregistrement demandé est contrôlé
(type des valeurs, borne LIMITE du §7) avant la bascule de jour (§6) ou le `trou` (§8) qu'il appellerait.

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

L'écriture se fait sans tampon. `fsync` est appelé à chaque marqueur (après le point de contrôle s'il y en a un), et
seulement là. Un arrêt brutal peut donc perdre les enregistrements postérieurs au dernier marqueur, ou laisser une
dernière ligne tronquée.

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
L'écrivain ne se partage pas entre fils : un seul fil l'appelle (contrainte pour la boucle du pool, sous-lot CB-4).

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

## 7. Reprise et segments (CB-2b, E-C-21)

1. À l'ouverture d'un journal existant, verrou pris, l'écrivain relit les fichiers du plus récent au plus ancien, ligne
   à ligne (LIMITE = 4 194 304 octets au plus par ligne, saut compris ; l'écrivain refuse d'écrire une ligne plus
   longue), jusqu'au premier fichier qui contient un enregistrement intègre. Intègre : ligne terminée par 0x0A, objet
   JSON canonique, chaîné à la ligne précédente (`seq` + 1, `prec`) ; la première ligne d'un fichier est une
   `ouverture` ou une `reprise`. La lecture d'un fichier s'arrête à la première ligne non intègre : elle et tout ce qui
   suit forment la **queue** du fichier.
2. Une queue n'est jamais réécrite ni tronquée. S'il en existe une (dans le fichier repris, ou un fichier plus récent
   sans enregistrement intègre), l'écrivain ouvre un **segment** neuf : numéro suivant du jour le plus tardif entre le
   jour repris et celui de l'horloge (l'ordre des noms reste l'ordre de la chaîne), premier enregistrement `reprise`.
3. Sans queue : un fichier repris d'un jour passé reçoit sa `cloture`, puis le fichier du jour s'ouvre par `reprise` ;
   un fichier repris déjà clos laisse place à un fichier neuf ouvert par `reprise` ; sinon `reprise` s'écrit à sa suite.
4. `reprise` porte `ws` (fenêtre de l'horloge au redémarrage), `suivante` (première fenêtre ni close ni déclarée en
   trou, lue dans l'état repris) et `queue` : liste de `{fichier, position, octets, sha256}` (octet de début de la
   queue, longueur, empreinte de ses octets), ou null. Un `fsync` suit son écriture. La chaîne reprend au dernier
   enregistrement intègre : le `prec` de la `reprise` est l'empreinte de sa ligne.
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
7. Limite déclarée : la reprise ne contrôle pas le lien entre la première ligne d'un fichier et la dernière du fichier
   précédent ; ce contrôle revient au lecteur du recalcul (RB-1) et au lecteur indépendant (RB-18).

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
3. Une ligne d'imbrication excessive (le décodeur JSON lève RecursionError) est non intègre : elle et la suite forment
   une queue (§7). L'écrivain refuse d'écrire un tel enregistrement (`JOURNAL/type`).
4. L'écrivain refuse de même, en temps borné, un enregistrement qui contient une structure cyclique (`JOURNAL/type`) :
   le contrôle de cycle du sérialiseur `json` précède le parcours des valeurs (CB-2e, C-3). Une sous-structure
   partagée sans cycle reste admise ; elle est écrite autant de fois qu'elle figure.

## 9. Enregistrement `lecture` (CB-3a ; E-C-03, E-C-04, E-C-17)

1. Une lecture donne un seul enregistrement, de type `lecture`, écrit dans sa fenêtre `ws`. Ses champs propres :
   - `statut` : `ok`, `panne_http`, `panne_transport` ou `panne_decode` (statuts lisibles par `r1.classify_ecart` de
     S2) ;
   - `sous_type` : pour `panne_transport` seulement, l'un de `dns`, `connexion`, `tls`, `delai`, `coupure`, `autre` ;
     null pour tout autre statut ;
   - `code` : code HTTP de la réponse (entier) ; null si aucune réponse n'a été lue ;
   - `depart`, `fin` : instants de départ et de fin de la lecture ;
   - `phases` : objet qui donne l'instant de fin de chaque phase atteinte (§10) ;
   - `adresse` : adresse IPv4 et port contactés, `a.b.c.d:port` ; null si la résolution n'a pas rendu ;
   - `brut` : octets du corps de la réponse, en base64 (alphabet standard, avec remplissage) ; `sha256` : leur
     empreinte, en 64 chiffres hexadécimaux minuscules ;
   - `valeurs` : valeurs décodées par le décodeur de la forme (sous-lots CB-6 et suivants) ; null avant décodage.
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
   | `dns` | la résolution du nom en IPv4 seule (`getaddrinfo` en `AF_INET`) rend une adresse ; la première est contactée | `dns` (échec, aucune adresse, ou délai épuisé pendant la résolution) |
   | `connexion` | la connexion TCP est établie | `connexion` |
   | `tls` | la poignée TLS aboutit (certificat vérifié, nom d'hôte contrôlé) | `tls` |
   | `requete` | les octets de la requête sont envoyés | `coupure` |
   | `corps` | la réponse est lue entière | `coupure` (fin du flux ou connexion rompue avant la fin annoncée) ; `autre` (réponse illisible, ou plus de 1 048 576 octets) |

2. Délai global : la lecture entière dispose de 10 s depuis son départ (ADR-0029 l.233). Chaque attente reçoit le temps
   qui reste, jamais un délai par opération ; un délai épuisé pendant une phase autre que `dns` donne le sous-type
   `delai`. La résolution est un appel bloquant que le client ne peut pas interrompre : l'échéance de la boucle (§11)
   la borne.
3. Réponse lue entière : code 200, statut `ok` ; tout autre code, `panne_http` avec ce code et le corps reçu. Aucune
   redirection n'est suivie (S2 suivait celles d'urllib) : un code 3xx est un `panne_http`.
4. Toute autre anomalie (défaut imprévu, requête dont l'hôte, le chemin ou la méthode sort de l'ASCII imprimable sans
   espace) donne `panne_transport` de sous-type `autre`. Une lecture ne lève jamais.
