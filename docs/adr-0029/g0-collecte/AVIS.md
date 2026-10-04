# AVIS advisor — G0 des lots COLLECTE-BIS, RECALC-BIS, DEPLOI-BIS (S2-bis) : les 45 questions techniques

- **Gate 0** : modèle résolu `claude-fable-5-1`, effort `medium` (explicite), rôle advisor (CLAUDE.md §7, amendement du 2026-09-18).
- **Date** : 2026-10-04. **Statut** : avis ; rien n'est décidé ici ; l'adjudication revient à l'orchestrateur (et à l'investisseur pour ce qui touche la durée de préparation, voir Q-G-04).
- **Pièces lues** [lu] : la proposition `scratchpad/s2bis/g0-collecte/G0-COLLECTE-RECALC-DEPLOI-proposition.md` (en entier, 928 lignes ; sha256 annoncé par le brief `0cdf84c2…bfd0`, non recalculé : pas d'outil shell dans cette fiche) ; `docs/adr-0029/ADR-0029-campagne-S2-bis.md` l.1-313 et l.378-402 (révision 3, acceptée, amendement du §2.6 compris) ; `docs/adr-0029/AVIS-STATS.md` l.46-52 (Q11) ; `docs/adr-0029/AVIS-OPS.md` par recherche (l.33, l.67) ; `docs/adr-0029/G0-lots-S2BIS.md` l.16-18 ; `docs/METHODE-PARTIES.md` l.1-30 par recherche ; `docs/PASSATION-CLOUD.md` l.220-223 par recherche. Non lus : `DECISIONS-ARCHITECTURE-S2BIS.md` et `AVIS-QUESTIONS-TECHNIQUES-V3.md` (cités par l'ADR ; je m'appuie sur ce que l'ADR en reporte).
- **Exposition (forme D.3)** : aucune pièce de la liste D.2 ouverte ; aucun `*.jsonl` ; rien de `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/`. Aucune donnée de S2-bis n'existe. J'ai lu dans l'ADR §1.1 les valeurs post-rendu de S2 (K, z, FIV), déjà publiques dans l'ADR acceptée.
- **Conventions** : « l.n » = ligne de l'ADR-0029 à `e16956b` (convention de la proposition) ; « prop. l.n » = ligne de la proposition ; [lu], [calc], [inféré] comme dans l'ADR. « Adoptée » = recommandation du rédacteur adoptée telle quelle. Marques : **[ADR]** = change la lettre de l'ADR, à amender par ajout daté ; **[précision ADR]** = l'ADR est muette, à écrire au paquet et, pour la traçabilité, en ajout daté ; **[gel]** = à trancher avant le gel du collecteur ; **[sceau]** = à trancher avant le sceau ; **[maintenant]** = à trancher avant d'ouvrir P1.

## 1. En bref

1. Sur les 45 questions, j'adopte la recommandation du rédacteur pour 37 ; j'en modifie 8 (Q-C-02, Q-C-05, Q-C-06, Q-D-03, Q-D-05, Q-R-13, Q-G-04, et Q-D-01 sur un détail de contrôle). Aucune ne remet en cause la structure proposée (paquet `s2bis/`, cinq parties, écrivain chaîné, processus séparé pour la carte).
2. Six écarts à la lettre de l'ADR sont justifiés et doivent être portés par ajout daté : l.241 (archive au lieu d'un clone, Q-D-01), l.245 (réplication par l'espace de sauvegarde seul, Q-D-02), l.107 (D-2 étendu, Q-C-02, avec une correction de formulation), l.241 pare-feu (Q-D-07), l.231 vocabulaire « réutilisés » (Q-R-12), l.308 et l.393 tailles et jalons (Q-G-04). Un septième écart est possible si la lecture croisée de la Storage Box n'existe pas (Q-D-03, l.218 et l.240).
3. Le point qui touche l'investisseur : la préparation annoncée dans la question de valeur 3 (« environ 8 semaines », l.401) devient environ 11 à 12 semaines si le périmètre est tenu (Q-G-04). Ce n'est pas une question technique : il faut le lui dire au premier accord de partie (A-1), avec l'option « réduire le périmètre ».
4. Chemin critique confirmé : la collecte, pas le calcul. P1 et P3 peuvent partir sans SIM-BIS (Q-G-02), à une réserve près pour RB-7 et suivants.

## 2. Les sept questions traitées en détail

### Q-D-01 — Archive du seul paquet `s2bis/` au lieu d'un clone du dépôt privé **[ADR l.241] [gel : avant DB-2, et au paquet]**

**Recommandation : adoptée, avec un contrôle de plus.** Motifs :
- Le dépôt est privé (PASSATION l.220 [lu]). Un clone sur quatre serveurs tiers exige un jeton de lecture sur chaque observateur, c'est-à-dire un secret de plus, alors que l'ADR veut « aucune clé » sur les observateurs (l.243). Il y pose aussi tout l'historique, dont les dossiers interdits (prop. l.741-743) : c'est une exposition D.2 inutile et une surface T-12 de doc 17 (l.242) élargie.
- Le collecteur n'a besoin que de `s2bis/` : la frontière E-C-01 interdit tout import de `shogen_s2` (prop. l.162). La garde (2) de l'exécution unique, qui porte aussi sur `s2-harness/shogen_s2` (prop. l.460), concerne la machine de rendu, pas les observateurs : rien à embarquer de plus.
- **Contrôle à ajouter** : ne pas faire reposer le contrôle sur le seul sha256 du fichier d'archive. Le résultat de `git archive` dépend de la version de git et de l'horodatage du commit [inféré : en-têtes tar] ; il est stable pour un commit donné, mais c'est une propriété de l'outil, non du contenu. Écrire au paquet un **manifeste par fichier** (chemin, sha256) produit depuis l'arbre du commit scellé, et faire contrôler par le script le sha256 de l'archive **et** le manifeste après extraction ; `run_params` porte le commit (E-C-23). Le manifeste est aussi ce qu'un tiers recalcule sans git.
- **Acheminement** : l'archive est déposée par l'investisseur dans le sous-compte de sauvegarde de chaque observateur (un geste de plus dans A-5, prop. l.856), l'observateur la lit avec la clé qu'il a déjà. Les champs « script de démarrage » des consoles sont trop petits pour embarquer l'archive [inféré : limites de quelques dizaines de kilo-octets chez les fournisseurs courants ; à lire sur pièce à DB-0].
- **Risque** : si l'archive est déposée avant le commit scellé (pour la mise en service), il faut la redéposer au gel ; la règle Q-C-06 (gel avant rodage) le règle : une seule archive, celle du commit gelé, déposée avant la mise en service.

### Q-D-02 — Volume des journaux contre des disques de 25 Go ; rétention locale bornée **[ADR l.245] [sceau pour la valeur mesurée ; gel pour la mécanique]**

**Recommandation : adoptée.** Détails et motifs :
- Les deux ordres de grandeur ne se contredisent pas : 17 Go par observateur et par mois (l.279) est une borne haute avec marge de deux, qui compte quatre classes, l'ensemble témoin et la carte ; 1,8 Go par mois (prop. l.750-751) extrapole S2 sur quatre classes **sans la carte et sans tenir compte des réponses groupées** (une réponse CoinGecko pour quatre actifs est bien plus grosse qu'un ticker). La vérité est entre les deux, et le G0 ne doit pas la deviner : **concevoir pour la borne haute**, mesurer au rodage (lecture admise « taille des journaux », l.221).
- À 17 Go par mois, un disque de 25 Go tient 1,5 mois (prop. l.924 [calc]) : la rétention locale bornée n'est pas une option, c'est une nécessité. Avec N = 7 jours de rétention après copie contrôlée, l'occupation locale reste sous 4 Go [calc : 17/30 × 7], loin de l'alerte à 80 % (E-D-11). **Je recommande N = 7 jours**, scellé, et : suppression par fichier quotidien clos seulement (jamais le fichier du jour), après égalité du sha256 distant (E-D-10, T-DP-11).
- L'écart à l.245 (« quatre copies par réplication entre observateurs ») est justifié par deux motifs, pas un : le volume, **et** le modèle d'accès : une réplication entre observateurs exige des flux SSH entre eux, que le pare-feu de l.241 n'ouvre pas, et crée un canal par lequel un observateur compromis atteint les trois autres (doc 17, entrée « transport et réplication », E-D-19). La chaîne (E-C-18), l'échange des têtes (E-C-35) et le jeton (E-C-36) donnent l'intégrité ; la Storage Box, ses instantanés (A-5) et le Drive à la clôture donnent la durabilité. Amender l.245 en « copie locale bornée à N jours, espace de sauvegarde et ses instantanés, Drive à la clôture ».
- **Risque résiduel** : la copie horaire (E-D-10) tombe en panne pendant plus de N jours → le disque se remplit sans suppression possible ; l'alerte disque à 80 % (E-D-11) couvre ce cas ; il faut que la procédure N1-N3 (E-D-17) dise quoi faire (relancer la copie ; jamais supprimer à la main).
- **Acte de l'investisseur** : si le rodage mesure plus que prévu, un disque plus grand est un coût (A-10) ; à chiffrer avant.

### Q-D-03 — Échange des têtes et compte des fenêtres évaluables entre observateurs **[précision ADR l.218, l.240 ; ADR si la lecture croisée n'existe pas] [gel : la forme du dépôt des têtes entre à CB-15 et CB-17]**

**Recommandation : différente sur un point : rendre le jeton quotidien indépendant de la lecture croisée.**
- Ce que l'ADR exige : chaque journal consigne les têtes des trois autres (l.240) ; un jeton RFC 3161 par jour « sur les quatre têtes » (l.218) ; `status` imprime le compte de fenêtres évaluables (l.244), qui demande M_j ≥ 2, donc la validité des autres observateurs (prop. l.756-757).
- Le mécanisme proposé (dépôt dans l'espace de sauvegarde, lecture croisée) n'est établi sur aucune pièce (prop. l.762). Si la Storage Box n'offre pas la lecture entre sous-comptes, trois choses tombent d'un coup : les têtes consignées, le manifeste à quatre têtes, le compte de `status`. Il faut donc une forme qui ne dépende pas de ce fait :
  1. **Jeton** : chaque observateur horodate **chaque jour sa propre tête** (quatre jetons par jour ; FreeTSA est gratuit et sans compte, l.294 ; les conditions d'un usage automatisé sont lues à DB-0, E-D-21). Quand les têtes des autres sont lisibles, le manifeste les inclut en plus. L'intégrité de chaque chaîne est ainsi ancrée quoi qu'il arrive à la lecture croisée ; la consignation croisée devient un renfort, non une condition. Si la lecture croisée est impossible, c'est un écart à l.218 (« sur les quatre têtes ») à amender ; sinon c'est une précision.
  2. **Résumé de santé** : chaque observateur publie, avec sa tête, un résumé **par fenêtre** limité à « valide / non valide, code D », sans aucun statut de source (D.2-bis, l.226). C'est ce que `status` lit chez les autres pour compter M_j. Le résumé est lui-même chaîné dans le journal de santé (il n'est qu'une projection d'enregistrements déjà écrits), donc recalculable.
  3. **`status`** : deux sorties, toujours : le compte **local** de fenêtres valides par strate (toujours disponible) et le compte **à quorum** quand au moins un résumé des autres est lisible, avec l'âge des résumés lus. L'investisseur voit quatre `status` ; aucun n'est faux faute de lecture croisée.
- **Repli du rédacteur** (`status` chez l'investisseur sur une copie des résumés, prop. l.763) : à écarter. L'ADR veut que l'investisseur n'exécute rien d'autre que les gestes N1-N3 (l.242, l.244) ; une commande chez lui, sur des copies, est un agent de plus à tenir hors des données.
- **Risque** : les résumés de santé publiés sont lus par l'orchestrateur au rodage ; ils ne portent que D-1 à D-5 : compatibles avec les lectures admises (l.221). Il faut un test « liste blanche des clés du résumé » comme pour la santé (prop. l.268).
- **À établir à DB-0** : lecture croisée entre sous-comptes de la Storage Box ; sinon, la forme ci-dessus suffit sans changer le code (le « dépôt » est un répertoire, lisible ou non).

### Q-R-01 — Axe des runs de I_t pour la garde d'information **[précision ADR l.201] [sceau ; et à transmettre à SIM-BIS]**

**Recommandation : adoptée (suite comprimée), avec deux précisions.**
- Motif du rédacteur, que je confirme : sur la grille UTC, une perte de quorum au milieu d'un incident unique le coupe en deux runs et fait passer la garde que l'avis STATS Q11 oppose précisément à « un épisode unique » (AVIS-STATS l.52 ; l.201). Sur la suite comprimée, la censure ne crée pas de run.
- Cohérence : la rotation se fait sur la suite comprimée (l.198) ; K et ses runs doivent être lus sur le même objet, sinon la garde et la loi nulle ne parlent pas de la même série.
- **Effet inverse, à déclarer** : sur la suite comprimée, deux épisodes réellement distincts séparés par une longue censure (quorum perdu plusieurs heures) deviennent adjacents et comptent pour un seul run. La garde est alors **plus sévère** (NON ÉVALUABLE plus souvent), jamais plus laxiste : c'est le bon sens de l'erreur pour une garde. L'imprimer : nombre de runs sur la suite comprimée (décision) et sur la grille (descriptif, hors décision), pour que le lecteur voie l'écart.
- **Définition à écrire au paquet** : run = suite maximale de positions **adjacentes de la suite comprimée** où m_j ≥ 2. « Deux runs » = au moins deux telles suites. La forme de `r1.bloc_strate` (grille) reste celle de z_bloc hors décision, comme le dit le rédacteur (prop. l.574).
- **SIM-BIS** doit mesurer la fréquence de NON ÉVALUABLE avec **cet** axe (l.201 : « SIM-NIVEAU-BIS et SIM-PUISSANCE-BIS mesurent la fréquence de NON ÉVALUABLE ») ; sinon la fréquence imprimée au paquet ne décrit pas la règle codée. C'est le seul point où ce G0 rétroagit sur SIM-BIS.

### Q-R-02 — Encodage de l'entrée de SHA-256 et sens du décalage **[précision ADR l.198] [sceau ; gel du code à RB-6]**

**Recommandation : adoptée, avec quatre compléments.**
- Entrée : octets UTF-8 de la chaîne ASCII `<graine en 64 hexadécimaux minuscules>:<strate>:<r décimal>:<u>` (prop. l.577). Bon choix : la graine est **imprimée en hexadécimal** au README du sceau (l.198, D.4 c) ; hacher sa forme imprimée, et non ses 32 octets, c'est hacher exactement ce que le tiers lit. Les deux formes sont équivalentes en sécurité ; une seule est recalculable sans ambiguïté.
- Compléments à sceller : (1) libellés de strate fixés : `calme` et `stress`, en ASCII minuscules, rien d'autre ; (2) r en décimal sans zéro de tête, de 1 à 9 999 ; (3) u = nom d'hôte de configuration (E-R-15), et **refus nommé** si un libellé de strate ou d'unité contient « : » ou un caractère hors ASCII imprimable (le séparateur doit rester sans ambiguïté) ; (4) le modulo est pris sur l'entier big-endian **entier** des 32 octets, en arithmétique exacte, et le diviseur est n_s ou n′_s **de la strate** (l.198) — pour l'analyse conditionnelle (Q-R-11), c'est la longueur de la **sous-suite**, à écrire aussi.
- Sens : « la valeur de la position t est envoyée en (t + o) mod n » (prop. l.579), c'est-à-dire D′(t) = D((t − o) mod n). Les deux sens donnent la même loi nulle (symétrie des décalages) ; un seul donne les mêmes K^(r) à l'octet : il faut le fixer, et le mutant « sens inversé » (prop. l.516) a un sens seulement si le vecteur de test est calculé hors du code, ce que le rédacteur prévoit (prop. l.512-513).
- Trois vecteurs de test écrits à la main avec `sha256sum` et une conversion d'entier par un outil distinct (prop. l.512-513) : adopté ; en ajouter un où o = 0 (décalage nul admis, l.198) et un où o = n − 1.

### Q-G-02 — Démarrer P1 et P3 sans attendre SIM-BIS **[G0 de vague l.17, non l'ADR] [maintenant]**

**Recommandation : adoptée pour P1 en entier et pour RB-0 à RB-6 ; réserve écrite pour RB-7 et suivants.**
- Le G0 de vague fait dépendre COLLECTE-BIS ‖ RECALC-BIS de SIM-BIS (`G0-lots-S2BIS.md` l.17 [lu]). L'ADR, elle, ne l'impose pas : les lots 4 et 5 sont numérotés, non enchaînés, et le jalon « lots 3 à 6 commis à S+5 » (l.393) les suppose menés en parallèle. Changer cette dépendance est un amendement du G0 de vague par l'orchestrateur, pas de l'ADR.
- Pour le collecteur, aucune sortie de SIM-BIS n'entre : n_s, T_max, tolérance sont des paramètres d'analyse (prop. l.801). P1 part sans attendre.
- Pour le recalcul, la réserve : SIM-BIS peut faire entrer **un critère collectif d'absorption** dans RB-5 (Q-R-10 ; SHOGEN-FLUX-ABSORPTION-COLLECTIVE-1, prop. l.568-569) et doit comparer la rotation enroulée à la variante de Harris (l.141, l.203) ; si la variante non enroulée devait entrer en sensibilité, RB-6 et RB-11 changent de forme. Donc : RB-0 à RB-6 partent ; **RB-7 (règle) attend la clôture de SIM-NIVEAU-BIS**, ou accepte par écrit d'être rouvert, ce qui coûte une G2 partielle de plus. Le chemin critique étant la collecte (prop. l.805), cette attente ne retarde rien.

### Q-G-04 — Taille (8 100 à 8 600 lignes) et jalons (S+5 à revoir) **[ADR l.308, l.393] [maintenant ; informer l'investisseur]**

**Recommandation : différente du rédacteur sur la forme : ne pas poser l'alternative « revoir le jalon ou réduire le périmètre » à l'orchestrateur seul ; les deux, et l'investisseur informé.**
- L'estimation est crédible, plutôt basse que haute : S2 compte 5 791 lignes de code et 8 774 de tests mesurées (prop. l.917) pour un seul actif, sans chaîne, sans santé, sans concurrence, sans carte (prop. l.230-232) ; S2-bis fait tout cela et ne réutilise que les décodeurs et quelques fonctions pures (prop. §2.1, §3.1). L'ADR l.308 chiffrait « par analogie » (l.308 [lu]) ; la base mesurée prime.
- Le jalon S+5 pour les lots 3 à 6 (l.393) suppose 46 à 49 sous-lots, cinq G2 à 100 %, cinq accords de l'investisseur, plus PLAN-S2BIS, CALIB-ACTIFS et SIM-BIS, en cinq semaines. La G2 à 100 % par partie (METHODE-PARTIES l.30) est le goulot, pas l'écriture.
- **Ce qu'il faut faire** : (1) **réduire ce que l'ADR permet déjà de réduire** : la carte n'entre au collecteur que « prête au gel » (l.259) — fixer **maintenant** la date de coupure de la carte égale au gel du collecteur, et accepter k = 0 à 2 lots CB-14 (les autres sources passent après le rendu, hors paquet, comme l'ADR le prévoit) ; CB-19 va au lot RODAGE (Q-C-13) ; (2) **revoir le jalon** par ajout daté à l.393 : lots 3 à 6 à S+7 ou S+8, déploiement S+8-9, sceau S+10-11, fin attendue S+27-28, T_max S+34-35 — mêmes mécanismes que le glissement d déjà prévu pour CALIB-ACTIFS (l.393), budget inchangé puisque les serveurs ne sont loués qu'au déploiement (l.279), horizon de 12 mois tenu (l.393) ; (3) **l'investisseur** a accepté « environ 8 semaines de préparation (9 à 10 si …) » (l.401). Passer à 11-12 semaines change ce qu'il a accepté : à lui dire en langage clair au premier accord de partie (A-1), avec l'alternative « réduire la carte à zéro source pour tenir 9-10 semaines ». Ce n'est pas une adjudication technique.
- **Ne pas réduire** : le noyau du collecteur (P1), la chaîne, la santé, le smoke sans prix, `status`. Ce sont les réponses à ce qui a fait échouer S2 (§1.2).
- Risque : un découpage en sous-lots de 200 lignes a un coût fixe (journal G1, ligne d'annexe A, ligne JOURNAL par sous-lot, prop. l.290-292) ; 46 à 49 sous-lots font ce coût 46 à 49 fois. Je ne propose pas de relever le plafond (R-25) ; je le signale pour le calendrier.

## 3. Les 38 autres questions

### Générales
- **Q-G-01** emplacement : adoptée. Les documents sous `docs/adr-0029/s2bis/` restent dans le périmètre des gates documentaires (prop. l.69-70).
- **Q-G-03** une G2 par partie : adoptée (METHODE-PARTIES l.30). Si la carte dépasse deux lots CB-14, scinder P2 en « contenus du pool » et « carte », chacune avec sa G2 et son accord, plutôt qu'une G2 de 2 400 lignes.
- **Q-G-05** analyse statique : pas d'outil nouveau sans contrôle R-8 préalable (CLAUDE.md §5) ; en attendant, la limite écrite plus les fonctions de fitness (frontière, garde réseau, déterminisme, E-C-41) et la compilation en `-W error`. L'orchestrateur tranche ; hors ADR.
- **Q-G-06** pièce G6 : adoptée ; à écrire à CB-0 (bibliothèque standard seule), complétée à DB-0 par le tableau R-8 des paquets système.

### COLLECTE-BIS
- **Q-C-01** IPv4 seule : adoptée ; cohérent avec l'ASN mesuré sur l'adresse réelle (l.79) et avec IPv6 refusé au pare-feu (Q-D-07). **[gel]**
- **Q-C-02** lecture non partie : **modifiée**. Le principe est juste (défaut de l'observateur, jamais de la source, l.102). Mais « partie plus de 5 s après ws + w − δ » est faux pour les lectures **séparées et décalées** d'un même hôte : la cinquième part par construction 4 s après la première (l.234 : « 5 + 4 + 10 + 1 = 20 »). Formuler : « toute lecture planifiée partie plus de 5 s après **son instant planifié**, ou non partie, dégrade l'observateur dans j ». **[ADR l.107] [gel, et avant le rodage : gel des seuils l.115]**
- **Q-C-03** instant des sondes : adoptée ; pool de fils distinct, jointes avant l'échéance ; valeur scellée (l.116). **[gel]**
- **Q-C-04** deux journaux : adoptée (l.235 l'impose pour la carte ; le relevé ASN y va naturellement).
- **Q-C-05** fixtures : adoptée avec une précision : la « recapture par le smoke du premier observateur avant le gel » doit être une **commande séparée**, qui écrit les octets dans un fichier sans rien imprimer (le smoke ne doit jamais imprimer un prix, E-C-37). Cette capture précède le rodage et n'est pas une donnée de S2-bis (aucune campagne n'existe) ; date et sha256 consignés. **[gel]**
- **Q-C-06** gel avant le rodage : adoptée ; c'est déjà l'ADR (l.115, l.217). Précision : une correction qui touche le chemin de lecture ou le journal refait le rodage **entier** (14 jours) pour les quatre observateurs, pas 7 ; 7 jours ne valent que pour un remplaçant (l.224). Une correction limitée à `status`, au smoke ou aux outils peut se contenter de 7 jours, déclarée. **[précision ADR l.220]**
- **Q-C-07** traduction de la q. 10 : question juste. Avant de créer des formes, vérifier avec l'advisor STATS si l'ADR ne contient pas déjà les deux mesures : « contre le dollar réel » = classe USDC/USD (places fiat, l.171) ; « telle que la DeFi la consomme » = Chainlink USDC/USD (classe « borné ») et l'ensemble témoin sur chaîne (l.172) ; « leur écart » = écart au pair des médianes des classes USD (Q-R-04) et P_j. Si oui, aucune forme nouvelle, et c'est écrit au paquet. **[gel de `formes.json`]**
- **Q-C-08** remplaçants : adoptée ; lus par le processus secondaire, hors du vote, bascule avant le sceau seulement.
- **Q-C-09** liste fermée de la carte : adoptée ; date de coupure = gel du collecteur (voir Q-G-04).
- **Q-C-10** budget OKX : regrouper (`/market/tickers`) seulement si une sixième forme s'impose ; décision à CB-7/CB-8 quand les paires servies sont connues (CALIB-ACTIFS). Un regroupement rend les pannes identiques entre actifs d'OKX ; l'ADR l'admet et le déclare (l.234). **[gel]**
- **Q-C-11** ENTRELACEMENT-D5-1 : adoptée ; fermeture par construction pour S2-bis ; la qualification sur S2 est un lot à `f35a70c`, à l'orchestrateur ; re-dater l'item.
- **Q-C-12** COLLECTOR-FISHER-1 : re-dater « fin de la quarantaine », ne pas fermer : fermer un item sur un code qu'on ne touche pas demande un motif sur l'item lui-même, que ce G0 n'établit pas.
- **Q-C-13** outil de rodage : au G0 du lot RODAGE (c'est l'instrument des lectures admises de D.1-bis, l.221), mais codé, relu et commis **avant la mise en service** : il n'est pas optionnel.
- **Q-C-14** contexte Decimal copié : adoptée ; égalité testée côté recalc.
- **Q-C-15** résultats tardifs : adoptée. **[gel]**
- **Q-C-16** COLLECT-PREVWS-1 : adoptée ; requalification à l'orchestrateur.

### RECALC-BIS
- **Q-R-03** rupture de chaîne : adoptée ; préciser la portée : de la dernière fenêtre à marqueur intègre avant la rupture jusqu'au premier marqueur du segment de reprise déclaré ; ces fenêtres valent D-1 « intégrité ». **[précision ADR] [sceau]**
- **Q-R-04** P_j par classe USD en descriptif : adoptée ; ne sert jamais à choisir des fenêtres (l.210, AQT Q4). **[sceau]**
- **Q-R-05** définitions : adoptées (matrice de co-défaillance ; décalages de (iii) ; tolérance à SIM-BIS). Pour (viii), Westfall-Young min-P en une étape : p marginale de chaque test à la rotation r obtenue par **rang** dans la loi de rotation de la même classe (tri, pas de seconde boucle), min-P sur {BTC, ETH} × strates avec les mêmes r. Source primaire non détenue : marquer [2nd] au paquet, c'est une sensibilité. **[sceau]**
- **Q-R-06** axe contenu de R2 : l'ADR est muette (l.248 [lu]). Proposition à l'advisor STATS : statistiques de contenu calculées **par observateur** sur ses propres lectures, publiées par observateur ; une fusion R2 par contenu seulement si au moins deux observateurs la mesurent (même règle que l'ASN, l.247). **[précision ADR l.248] [sceau]**
- **Q-R-07** rendu de la carte dans RECALC-BIS : oui ; « servie au rendu unique » (l.259) ne peut se faire ailleurs.
- **Q-R-08** lecteur indépendant par un autre auteur : adoptée ; verdict imprimé, sans fermer l'exécution.
- **Q-R-09** script neuf calqué : adoptée ; S2 reste à `f35a70c`.
- **Q-R-10** critère collectif : adoptée ; voir la réserve de Q-G-02.
- **Q-R-11** analyse conditionnelle : adoptée ; même hachage, **modulo la longueur de la sous-suite** (voir Q-R-02). **[sceau]**
- **Q-R-12** sens de « réutilisé » : adoptée ; ajout daté à l.231. **[ADR]**
- **Q-R-13** T_début : **modifiée**. L'heure d'un commit est une métadonnée que l'auteur fixe ; ne pas la prendre comme borne. Prendre l'**instant écrit dans l'acte de go** lui-même (pièce du paquet) : T_début = premier `window_start` ≥ max(genTime + 24 h, instant du go) ; le script le calcule et compare au README, comme le veut E-R-07. **[précision ADR l.216] [sceau]**

### DEPLOI-BIS
- **Q-D-04** système et Python : adoptée (Debian stable, versions au descripteur ; Python ≥ 3.10 pour `int.bit_count`).
- **Q-D-05** résolveur épinglé : je penche pour l'**option 1** (configuration de résolution immuable : `resolv.conf` figé ou systemd-resolved avec serveurs fixes et DNS du DHCP ignoré) pour O2 à O4, unbound seulement sur O1. Motif : l'option 2 place un cache local devant chaque famille ; D-5 mesurerait alors « cache + amont », et le résolveur journalisé ne serait plus celui de la famille (l.82). Avis OPS attendu, comme le demande le rédacteur. **[avant P5]**
- **Q-D-06** NTP : adoptée ; aucun serveur sur un ASN du pool (donc pas `time.cloudflare.com`, AS13335) ; pas de mélange lissage / non lissage de la seconde intercalaire (donc pas Google à côté d'instituts de métrologie) ; liste fixe, pas de pool dynamique, sinon l'empreinte (l.83) ne gèle rien. À lire sur pièce à DB-0.
- **Q-D-07** pare-feu : adoptée ; IPv6 refusé (cohérent avec Q-C-01). **[ADR l.241]**
- **Q-D-08** redémarrages : adoptée ; un redémarrage est un trou D-1 journalisé (E-C-22), jamais deux observateurs à la fois, consigné dans `interventions.md`.
- **Q-D-09** exercices avant fermeture des items : adoptée (E-D-22).
- **Q-D-10** OpenTimestamps : adoptée ; au lot PAQUET-S2BIS ; c'est une dépendance nouvelle (R-8) et un acte de l'investisseur (l.218).

## 4. Tableau des marques

| question | change l'ADR (ajout daté) | avant le gel du collecteur | avant le sceau | maintenant |
|---|---|---|---|---|
| Q-D-01 | l.241 | DB-2 (avant la mise en service) | sha de l'archive et manifeste au paquet | |
| Q-D-02 | l.245 | mécanique de rétention (DB-4) | volume mesuré au rodage, N = 7 j scellé | |
| Q-D-03 | précision l.218, l.240 ; écart si lecture croisée impossible | forme du dépôt des têtes (CB-15, CB-17) | | DB-0 : lire la Storage Box |
| Q-R-01 | précision l.201 | | oui ; axe transmis à SIM-BIS | |
| Q-R-02 | précision l.198 | | oui ; vecteurs au paquet | |
| Q-G-02 | non (G0 de vague l.17) | | | oui |
| Q-G-04 | l.308, l.393 | | | oui ; informer l'investisseur (q. 3, l.401) |
| Q-C-02 | l.107 | oui (et avant le rodage) | | |
| Q-C-06 | précision l.220 | | | oui |
| Q-D-07 | l.241 | | | avant P5 |
| Q-R-12 | l.231 | | | |
| Q-R-03, Q-R-06, Q-R-13 | précisions | | oui | |
| Q-C-01, 03, 05, 07, 10, 15 | non | oui | | |
| Q-R-04, 05, 11 | non | | oui | |
| Q-D-05 | non | | | avant P5 (avis OPS) |
| les autres | non | au fil des sous-lots | | |

## 5. Ce que cet avis ne fait pas

Il ne vérifie ni les tailles ni les mesures du rédacteur (aucune commande lancée) ; il ne lit pas DÉC ni AQT en entier ; il ne tranche aucune question de valeur (q. 3, q. 10, q. 13). Les affirmations sur les limites des consoles cloud-init et sur les serveurs NTP sont [inféré], à lire sur pièce à DB-0.
