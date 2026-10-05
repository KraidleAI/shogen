# Format des journaux d'observateur de S2-bis

- **Rattachement** : ADR-0029 §2.9 (l.238-240 : journal à enregistrement unique, chaîné, `fsync` au marqueur, point de
  contrôle horaire, fichiers quotidiens clos et sommés ; format spécifié et scellé au paquet) ; PROPOSITION du G0
  (`docs/adr-0029/g0-collecte/`), exigences E-C-16 à E-C-24 ; principe de SHOGEN-FORMAT-JOURNAUX-1 (annexe B d'ADR-0028,
  l.55).
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
  le diff CB-18f applique I-2 (§7.1).
- **Items de l'annexe B fermés au sous-lot CB-18** (2026-10-05) : le diff CB-18a ferme SHOGEN-S2BIS-ECRIVAIN-USAGE-1
  pour l'écrivain (§5) et porte les retouches de SHOGEN-S2BIS-FORMAT-RETOUCHES-1 (§12, en-tête) ; le diff CB-18b ferme
  SHOGEN-S2BIS-SOMMEIL-MURAL-1 (§10.2, §11.8), SHOGEN-S2BIS-SONDES-ECHEANCE-1 (§11.4, §13.2) et, pour la boucle,
  SHOGEN-S2BIS-PLAN-CABLAGE-1 (§11.9) ; le diff CB-18c achève SHOGEN-S2BIS-PLAN-CABLAGE-1 (câblage des sondes, §14) ;
  le diff CB-18d achève SHOGEN-S2BIS-ECRIVAIN-USAGE-1 (fermeture au point d'entrée, §14) ; le diff CB-18e verse le
  test de conformité de bout en bout (E-C-24) ; le diff CB-18f ferme SHOGEN-S2BIS-FORMAT-RETOUCHES-1, étendu par
  I-2, par ses tests nommés (`s2bis/tests/test_format.py` : la citation du §7.3, la marque « choix du lot » de la
  règle de source, CB-11h dans la puce « Corrections », valeurs prises au texte de l'item ; puis les contrôles de
  type de `_lire` dits au §7.1 et faits par `_lire`).

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
| `marqueur` | `ws` ; aucun champ propre : la boucle (CB-4) n'en écrit pas, ses comptes vont à `sante` (§11) | `marqueur(ws)` : clôt la fenêtre `ws` |
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

**Un seul fil** (CB-18a, SHOGEN-S2BIS-ECRIVAIN-USAGE-1). L'écrivain ne se partage pas entre fils, et la garde est
mécanique :
- le fil qui appelle `ouvrir` est noté ; `ecrire` ou `marqueur` appelés d'un autre fil sont refusés (`JOURNAL/fil`) ;
- un écrivain s'ouvre une seule fois : un second `ouvrir` est refusé (`JOURNAL/ouvert`), sans toucher au verrou ni au
  fichier ouvert ;
- une écriture avant `ouvrir` ou après `fermer`, et l'ouverture d'un écrivain fermé, sont refusées (`JOURNAL/ferme`) ;
- une ouverture refusée (`JOURNAL/occupe`, `JOURNAL/fenetre`, `JOURNAL/illisible`) ferme l'écrivain et rend le verrou ;
- `fermer` est le seul appel admis de tout fil (nettoyage) ; il reste admis après une casse (§4).

Aucun de ces refus n'écrit. Les trois méthodes publiques d'écriture portent la même garde que la casse de C-2 (§4) ; un
test contrôle que toute méthode publique de l'écrivain la porte, `fermer` excepté.

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
   `ouverture` ou une `reprise`. Les champs dont la reprise se sert sont contrôlés en type (`Journal._lire`, code de
   référence ; I-2 de la G2 du recalcul) : `seq` de la première ligne d'un fichier, entier ; `suivante` d'une
   `ouverture` ou d'une `reprise`, entier ; `ws` d'un `marqueur` ou d'un enregistrement de fenêtre, entier (il donne la
   **dernière fenêtre écrite**, §7.5) ; `a` d'un `trou`, tel que `a` + w soit un entier. Limites déclarées : un booléen
   JSON passe dans `a` et, hors de la première ligne, dans `seq` (`true` y vaut 1) ; `de` d'un `trou`, `ws` d'un
   `point` ou d'une `reprise` et `jour` ne sont pas contrôlés. La lecture d'un fichier s'arrête à la première ligne non
   intègre : elle et tout ce qui suit forment la **queue** du fichier.
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
   résultats tardifs (§11.6). Une lecture dont la fonction lève, BaseException comprise (O-5 : l'exception suit son
   cours, le résultat est rendu), ou ne rend pas une lecture, est `panne_transport` de sous-type `autre`.
5. **Ordre des enregistrements de la fenêtre** : les `lecture` dans l'ordre du plan (décalage, puis nom de forme),
   puis `sante`, puis (`trou` s'il y a lieu, §8) `marqueur`. Une fenêtre dont l'échéance est déjà passée quand la boucle
   l'atteint n'est pas lue : le trou est déclaré au marqueur suivant (cause `saut`).
6. **Enregistrement `sante` de la boucle** (valeurs brutes, aucun jugement) :
   - `d2.retard_max` : plus grand retard au départ (instant de lancement moins instant planifié, en microsecondes)
     parmi les lectures parties ; null si aucune n'est partie. `d2.non_parties` : nombre de lectures planifiées qui ne
     sont pas parties faute de place. D-2 se juge au recalcul (règle Q-C-02 de l'avis : toute lecture partie plus de
     5 s après son instant planifié, ou non partie, dégrade l'observateur dans la fenêtre) ;
   - `fils.abandonnes` : lectures abandonnées, à savoir celles de la fenêtre (non finies à E, §11.4, même si leur
     résultat est arrivé entre E et le relevé), plus celles des fenêtres précédentes dont le résultat n'était pas
     arrivé au relevé ;
     `fils.tardives` : latences (fin moins départ, en microsecondes, triées) des lectures abandonnées dont le résultat
     est arrivé depuis le relevé de la fenêtre précédente. Un résultat tardif n'est jamais écrit comme lecture (Q-C-15) ;
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
  n'est pas une IPv4 littérale canonique, requête impossible, ou réponse appariée mal formée) ou `reseau` (envoi
  refusé par le système) ;
- `rcode` : code de réponse (entier de 0 à 15 ; 0 NOERROR, 3 NXDOMAIN) ; `tc` : drapeau de troncature ; null tous deux
  sans réponse retenue ;
- `reponses` : liste de la section réponse, chaque élément `[nom, type, ttl, données]` : `nom` en texte terminé par
  un point ; `type` entier (1 A, 6 SOA, 16 TXT) ; `ttl` entier en secondes ; `données` : pour A, l'adresse en
  notation pointée ; pour TXT, la liste des chaînes (octets lus en latin-1) ; pour SOA, `[mname, rname, serial,
  refresh, retry, expire, minimum]` ; pour tout autre type, null. Null sans réponse retenue ;
- `debut`, `fin` : instants de l'envoi et de la fin de l'attente, en microsecondes, sur l'horloge murale ; le délai se
  compte sur l'horloge monotone (C-4).

Une réponse est **appariée** si elle porte l'identifiant de la requête (tiré au hasard sur 16 bits), le bit QR, une
seule question et la même, casse ignorée (RFC 1035 §4.1.1-4.1.2, §7.3 ; casse : §2.3.3) ; elle est alors retenue, ou
`forme` si la suite est mal formée. Le lot exige en outre qu'elle vienne de l'adresse et du port interrogés : c'est un
**choix du lot**, non une règle de la RFC 1035, dont le §7.3 note que des serveurs répondent depuis une autre adresse
que celle qui a reçu la requête. Une telle réponse est ignorée, et la sonde finit en `delai` : un échec D-4 ou D-5 que
le rodage mesure (contre-contrôle de CB-11h).
Tout autre datagramme (écho de la requête, réponse à une autre question, datagramme trop
court) est ignoré, et l'attente continue jusqu'au délai (C-2). La requête ne passe par aucune résolution : l'adresse
est une IPv4 littérale **canonique** (quatre entiers décimaux pointés, sans zéro de tête : forme rendue par
`ipaddress`) ; toute autre valeur (nom, forme abrégée comme « 127.1 », null) donne `forme`, sans exception, sans
résolution et sans envoi (ADR-0029 l.109).

## 13. Enregistrement `sante` complet (CB-11 ; E-C-25 à E-C-29)

1. Un enregistrement `sante` par fenêtre lue, avant le marqueur. Ses clés forment une **liste blanche fermée** :
   `type`, `ws`, `seq`, `prec`, `d2`, `fils`, `horloges` (§11.6), `d3`, `d4`, `d5`, `disque`, `resolveur`. Aucune clé
   n'est tirée d'une lecture de source ; aucun champ ne porte de jugement (« dégradé » se juge au recalcul et dans
   `status`, avec les seuils scellés, E-C-26). Une boucle construite sans sondes (tests de la boucle seule) écrit la
   même liste : `d3`, `disque` et `resolveur` null, `d4` et `d5` vides (O-7).
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

## 14. Configurations, descripteur, câblage et point d'entrée (CB-18c, CB-18d ; E-C-02, E-C-16, E-C-23)

1. **Fichiers chargés** : chacun est lu en octets, son sha256 calculé sur ces octets, puis contrôlé (champs exacts,
   types, bornes, puis règles de cohérence nommées) :
   - `formes.json`, configuration scellée de la boucle : `w` (s, divise 3 600), `delta`, `delai`, `marge` (µs ;
     `marge` < `delta` ≤ w·10⁶), `places` (taille du pool), `formes` : liste de `{nom, hote, port, chemin, methode,
     corps, espace}` (noms uniques ; `GET` sans corps ou `POST` avec corps ; `espace` vrai : la limite de l'hôte impose
     l'espacement de 1 s entre ses lectures, même valeur pour toutes les formes d'un hôte). Le plus grand décalage du
     plan, plus `delai` et `marge`, tient dans `delta` (budget de l'ADR-0029 l.233-234) ;
   - `sante.json`, configuration scellée des sondes : `commande` (D-3, liste d'arguments), `temoins` (D-4, IPv4
     littérales canoniques), `noms` (D-5, noms DNS valides), `delai` (µs ; `delai` + `marge` ≤ `delta` : les sondes
     sont jointes avant l'échéance) ;
   - le **descripteur** de l'observateur, écrit au premier démarrage (lot DEPLOI-BIS) : `observateur`, `fournisseur`,
     `region`, `asn` (mesuré), `resolveur` (IPv4 littérale canonique, cible de D-5), `config_resolveur` (chemin de la
     configuration du résolveur, dont l'empreinte va à `sante.resolveur`), `versions` (paquets), `empreinte` (sha256
     de la configuration déployée, 64 chiffres hexadécimaux minuscules).

   Le commit est celui, scellé, de l'archive déployée : 40 chiffres hexadécimaux minuscules (aucune opération git sur
   l'observateur). Tout écart est un refus nommé (`CONFIG/…` ou `BOUCLE/…`), levé avant l'ouverture du journal.
2. **Câblage** (SHOGEN-S2BIS-PLAN-CABLAGE-1) : une lecture par forme ; plan par hôte (§11.1) ; sondes construites
   depuis `sante.json`, dirigées vers le résolveur du descripteur, disque relevé sur le dossier du journal ; la boucle
   tourne toujours avec ses sondes (§13.1 : une `sante` sans sondes n'existe que dans les tests de la boucle seule).
3. **Commande** (CB-18d) : `python3 -m shogen_s2bis.collecte pool --formes F --sante S --descripteur D --journal
   DOSSIER --commit SHA` (code de référence : `s2bis/shogen_s2bis/collecte/entree.py`). `--fenetres N` arrête après N
   fenêtres (essais) ; sans elle, la boucle tourne sans fin, sous systemd. Un refus de configuration donne la sortie 2
   et `collecte : refus : <code> : …` sur la sortie d'erreur, sans rien écrire.
4. **`run_params`** (CB-18d), écrit à chaque démarrage, aussitôt le journal ouvert, à la première fenêtre admise :
   `commit`, `sha256` (`{formes, sante, descripteur}` : sha256 des octets lus), les contenus `formes`, `sante` et
   `descripteur`, `python` (version de l'interpréteur). Une fenêtre qui porte `run_params` puis n'a pas de marqueur
   est déclarée par le `trou` suivant (§8).
5. **Fermeture** (CB-18d, SHOGEN-S2BIS-ECRIVAIN-USAGE-1) : le journal est fermé à la sortie du point d'entrée, quelle
   qu'elle soit. Une OSError ou un refus de l'écrivain (`JOURNAL/casse` compris, et toute ouverture refusée) arrête la
   boucle : sortie 1, refus nommé (`collecte : arrêt : <code> : …`) ; systemd relance le service, et l'instance
   suivante reprend le journal (§7). Sortie 0 : les N fenêtres demandées sont écrites.
