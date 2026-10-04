# Relecture G2 du lot DOCS11-PUBLIC (brouillon de la version publique filtrée de `docs/11`)

Réviseur G2 neuf (fiche `shogen-worker`), qui n'a rien écrit de ce lot. Horloge lue (`date -u`) : début
`Sun Oct  4 14:18:03 UTC 2026`, rédaction de ce rapport à `14:40:22 UTC`. Lecture seule du dépôt ; aucune opération git
en écriture ; écritures dans le seul dossier `…/scratchpad/s2bis/docs11pub/g2/`. Rien n'est publié.

- **Gate 0** : identifiant de modèle déclaré par l'environnement : `claude-opus-5-5` (préfixe attendu `claude-opus-5-5` :
  conforme). Effort `max` demandé ; non observable de l'intérieur de la session.
- **Brief** : `g2/BRIEF-G2-DOCS11-PUBLIC.md`, sha256 recompté `36eb464d94b9f3aad4bef1911b49fc46d051ea140111883f8ee6528c04f74a13`,
  égal à la valeur donnée.
- **Rattachement (G0)** : `docs/adr-0029/G0-lots-S2BIS.md` (sha256 `25a82120…a130`) l.13, ligne DOCS11-PUBLIC ; décision de
  l'investisseur, JOURNAL l.382 (2026-10-04 13:18:44 UTC) ; registre `docs/09-vocabulaire.md` (sha256 `001b9606…2f831`).
- **Base de la copie** : branche `claude/compassionate-noether-szmdyj`, tête `6d463faa565a36ce49ffbde7c0860691b684b382`,
  arbre propre. Le worker est parti de `75bf258` et a fini à `2c2fbe9` ; depuis, `c4cf982` et `6d463fa` (lot
  SG5-INTERDITS, 14:16-14:17 UTC). Aucune entrée du lot n'a changé (`git diff --name-only 75bf258 HEAD` sur `docs/11`,
  `docs/09`, le G0, l'annexe D et `xtask/src/sg4.rs` : 0 fichier) ; `docs/11` garde son sha256 `fcf93b87…53b7`.

## 0. Verdict

**ACCEPTE-AVEC-CORRECTIONS**, trois corrections (liste fermée C-1 à C-3, §1).

Le brouillon (sha256 `903d6d0c1ae146a56af40b9156903dcee6bbecd4adbf4c8d4d7f550300475433`) se reconstruit à l'octet depuis la
source ; aucun chemin local ou de bac à sable, nom de dépôt privé, identifiant de session ou d'agent, mention de Pocket ou
donnée personnelle nominative ne reste ; aucun nombre n'est inventé, ajouté ou changé (seuls des identifiants sont
retirés) ; le registre du doc 09 est tenu. Les corrections portent sur une phrase inexacte du statut ajouté au brouillon
(C-2) et sur la table de correspondance (C-1, C-3). Les décisions qui restent sont celles de l'investisseur (§7, §10).

## 1. Corrections (liste fermée)

**C-1 — Table, motif de G-08 (MONARK) : affirmation inexacte.** Le motif dit « déjà présent dans des documents destinés
au public (doc 08, doc 17) ». Faux pour le doc 17 : son en-tête porte « **Classification** : interne. Son inclusion dans
un export public est une décision de l'investisseur » (`docs/17-modele-de-menace.md` l.5, [lu]). MONARK n'apparaît dans
aucun document d'allure publique du dépôt (comptes : README 0, docs 00 à 07 : 0, `pitch-plates.html` 0) ; seulement au
doc 08 (2, registre sans mention de classification) et au doc 17 (22). Le journal G1 du worker classe ces documents en
« comptes seuls » : l'affirmation n'avait pas de lecture pour source. À faire : remplacer le motif, dans
`outils/construire_public.py` (liste `GARDES`), par un motif exact, par exemple : « Nom du projet connexe, nécessaire à
la déviation déclarée (§10) et au test de composition (§8.6, §12) ; absent des documents d'allure publique du dépôt ;
présent au doc 08 et au doc 17, classé interne ; garder sous décision explicite de l'investisseur, à qui ADR-0028 §4 pt 5
réserve la formulation publique de l'état de la pièce Shōgen côté MONARK ; aucun chemin, nom de fichier ni nom de
dépôt. » Régénérer la table.

**C-2 — Brouillon, phrase de statut ajoutée par E-01 (l.4-9) : affirmation trop large.** Elle dit que « les références
à des pièces ou dossiers non publics » sont retirées. Or le brouillon cite encore de nombreuses pièces non publiques :
JOURNAL (27 mentions), ADR-0028 et ses annexes, rendus, paquet, sceau, journaux G1, scripts, sorties PP/, tous au dépôt
privé, comme le dit le brouillon lui-même au §12 (« Ce qui n'est pas public » : « le dépôt du projet est privé » ;
« Les rendus et le sceau sont au même dépôt privé »). Seules les références aux dossiers exclus (ADR-0025), aux pièces
D.2 et au lieu de stockage d'une copie ont été retirées. À faire : réécrire la phrase pour qu'elle ne dise plus que toutes
ces références sont retirées et pour qu'elle dise que les autres pièces citées sont au dépôt privé et que leur diffusion
n'est pas décidée, **sans ajouter aucun chiffre**. Texte proposé (sans chiffre) : « Par rapport au rapport source, les
chemins de poste local, les noms de dépôts privés, les identifiants de session ou d'agent, les renvois à des pièces ou
dossiers exclus de toute diffusion et des mentions de gouvernance interne sans objet pour un lecteur extérieur sont
retirés ou remplacés par une phrase neutre ; une formule est mise au registre du vocabulaire du projet. Les autres pièces
citées (journal du projet, ADR et annexes, rendus, sceau, scripts) le restent : elles sont au dépôt privé du projet
(section « Reproduire », « Ce qui n'est pas public ») et leur diffusion n'est pas décidée. » Mettre à jour le motif de
E-01, régénérer brouillon, table et diff, rejouer le contrôle (CONFORME attendu, aucune exception nouvelle), les 61 tests
et la campagne de mutants. Si le nombre de lignes du statut change, mettre à jour les renvois « b. l.N » de
`ACTEURS-NOMMES.md` (§2 à §5) et régénérer `acteurs_nommes.sortie.txt` (décalage des lignes).

**C-3 — Table : deux passages examinés au regard du point 1 manquent à la liste des passages gardés.** Ajouter à
`GARDES` (puis régénérer la table) :
- **G-17** « M009 » (§10.1, §10.2 ; brouillon l.919, 934, 938 ; source l.913, 928, 932) : l'identifiant d'item
  `MONARK-S2-M009A-EXPOSITION-1` (deux fois) et « les sessions MONARK des lots M009 » nomment la mesure MONARK M009a, objet
  des pièces D.2 n° 2 et n° 12 ; ni chemin, ni nom de fichier, ni contenu, ni valeur ; nécessaires à la déviation
  déclarée ; même décision de l'investisseur que G-08. (Le worker l'a examiné : son test `test_texte_neutre` le tient pour
  neutre ; il manque seulement à la table que lira l'investisseur.)
- **G-18** « PX-Shogen-13 » (§5.1, §9.3, §11 ; brouillon l.442, 443, 910, 996) : identifiant d'item de la séquence
  PAROXYSME, dont le registre hors dépôt est la pièce D.2 n° 10 ; aucun contenu de cette pièce ; renvoi opaque pour un
  lecteur extérieur.

Rien d'autre n'est exigé. Les remarques du §9 sont facultatives.

## 2. Contrôle 1 — rejeu : le brouillon est-il reproduit à l'octet ? Oui.

- Construction rejouée dans un dossier neuf (`g2/rejeu-construction/`) : `construire_public.py` sur `docs/11` (sha256
  `fcf93b87…53b7`), sortie 0, 13 retouches ; brouillon `903d6d0c…5433` (98 546 octets, 1 077 lignes), table `6af200f7…d46d`,
  diff `3c2265b9…c9ce` : les trois **identiques à l'octet** aux livrables du worker (`cmp`).
- Contrôle rejoué : `controle_public.py SOURCE BROUILLON TABLE`, sortie 0, « VERDICT : CONFORME — sept contrôles sur
  sept ». Sortie comparée ligne à ligne à celle du worker : 144 lignes chacune, 2 différentes (l.4 et l.6, chemins
  absolus chez moi, relatifs chez le worker), les 142 autres identiques.
- Rejeu de la table écrit par moi (lecture des lignes « | E- », « ⏎ » rendu en saut de ligne, chaque retouche appliquée
  une fois sur la source) : 13 retouches trouvées une fois chacune, résultat sha256 `903d6d0c…5433`, **identique au
  brouillon**.
- Diff indépendant (GNU diffutils 3.10) : 10 blocs, aux lignes source 3-7, 14, 70-71, 178, 211, 624, 729, 914-915,
  933-934, 1064, exactement celles de E-01 à E-13 ; toutes les autres lignes sont identiques.

## 3. Contrôle 2 — recherche indépendante de ce qui ne doit pas sortir

Moyen indépendant des outils du worker : trois scripts à moi (`recherche_g2.py`, `inventaire_g2.py`, `perimetre_g2.py`),
liste de motifs à moi, plus un inventaire exhaustif lu à l'œil.

**Motifs du réviseur** (53 familles, dont 40 bloquantes et 13 à examiner, `recherche_g2.sortie.txt`) : lecteurs
Windows suivis d'une barre, barre oblique inverse, `/tmp`, racines Unix, dossiers Windows (Users, AppData, OneDrive…), traces du harnais (scratchpad, worktree,
`.claude`…), variables d'hôte ; Kraidle, governance, forges (github, gitlab, `git@`), « Monark » en casse de dossier,
PRODUITS ; `session_`, identifiants connus de sessions et d'outils, UUID, noms de fiches d'agent, `carto:`, `wf_`,
marques de Claude Code ; docs 15 et 16, `rapports`, `0025`, M009 et M002, measure-, hikae, ukemi, pocket, pokt, grove,
cartographie, empreintes des pièces D.2 n° 5 et 6, dossier de campagne, sorties de cartographie, étude, archive et avis
hors dépôt, PAROXYSME, le commit de D.2 n° 12 et les mots du sujet de ce commit, Drive, Google, bucket, sigma-tau,
critique ; courriels, noms connus, téléphones, IPv4, adresses postales, argent, noms de machine, secrets ; plus une
recherche séparée des fuseaux horaires et heures locales (0 : seul « cet », démonstratif, répond).

**Résultat** : 0 occurrence dans le brouillon pour toutes les familles, sauf quatre touches, qualifiées une à une :
- « rapports » l.438, 809 : au sens de ratios (« rapports P99/τ ») : faux positif ;
- « 0025 » l.525, 529 : chiffres de décimales (`0.00251765…`, `0,00252`) : faux positif ;
- « EUR » l.782, 785 : fin de « LECTEUR » (SHOGEN-RAW-LECTEUR-1) : faux positif ;
- « M009 » l.919, 934, 938 : reste à signaler (R-1 ci-dessous).

**Inventaire exhaustif** (`inventaire_g2.sortie.txt`, 640 lignes lues) : 194 passages entre accents graves, 50 jetons à
barre oblique, 47 noms de fichiers, 14 hôtes (tous des points d'accès publics des sources mesurées, du RPC et du
résolveur), 44 empreintes ou commits, 80 identifiants à tiret, 57 noms propres, 52 sigles. Aucun chemin du poste ou du
bac à sable, aucun nom de dépôt, aucun identifiant de session ou d'agent, aucun nom de personne privée, aucune adresse,
aucun numéro, aucun courriel. Noms de personnes présents : auteurs de méthode (Knight, Leveson, Künsch, Kiefer-Vogelsang,
Manski, Fisher, Poisson, Bonferroni) ; noms de sociétés : acteurs mesurés et infrastructures, tous dans `ACTEURS-NOMMES.md` (sondage de
40 autres noms de sociétés, chaînes, monnaies et hébergeurs : 5 présents, tous rattachés à un acteur de la liste,
« Ethereum » dans l'hôte de PublicNode, « AWS » et « CloudFront » pour Amazon, « Cymru », « Llama » ; aucun hors liste).

**Restes signalés (dans le brouillon)** :
- **R-1** « M009 » : `MONARK-S2-M009A-EXPOSITION-1` (l.919, 934) et « les sessions MONARK des lots M009 » (l.938).
  Étiquettes qui nomment la mesure MONARK M009a, objet des pièces D.2 n° 2 et n° 12. Pas un renvoi à la pièce elle-même
  (ni chemin, ni fichier, ni valeur) ; nécessaire à la déviation déclarée. Avis : garder, sous la décision de
  l'investisseur sur MONARK ; à lister à la table (C-3).
- **R-2** « PX-Shogen-13 » (l.442, 443, 910, 996) : identifiant d'item de la séquence PAROXYSME (registre hors dépôt :
  pièce D.2 n° 10). Aucun contenu. Avis : garder ; à lister à la table (C-3).
- **R-3** « un sous-agent de cartographie » (l.939) : rôle d'un lecteur, déjà traité par la retouche E-12 ; aucun renvoi
  au document de cartographie (dont la l.51 est la pièce D.2 n° 5). Avis : garder.
- **Donnée personnelle (faible)** : le poste personnel de l'investisseur et sa consigne « pas sur mon PC » (l.219-220,
  l.890-891), déjà examinés par le worker (G-02). Aucun nom, aucune adresse.

**Restes hors du brouillon (pièces qu'il cite par empreinte)** — comptes seuls, aucun contenu affiché
(`perimetre_g2.sortie.txt`) ; ils pèsent sur l'item PERIMETRE (§8) :
- enregistrement d'oracle ENR (`…943.json`, sha256 `355cf9bb…`, cité au §8.4 et à la table des conventions) : chemins
  de dossiers interdits `docs/pocket-report/` ×3, `docs/15-` ×1, `docs/16-` ×1, `docs/adr-0025/` ×1, `docs/rapports/` ×4,
  et `/tmp/` ×5 (liste des fichiers de l'arbre haché). **Ne peut pas accompagner une publication tel quel**, et ne peut
  pas être filtré sans casser l'empreinte que le brouillon publie ;
- paquet scellé `PAQUET-PREREG-S2.md` : nom de l'organisation GitHub ×1, « ADR-0025 » ×4 ;
- rendus J14p, J14s et J28 : un chemin à lettre de lecteur chacun ; J28 et SUITE : « ADR-0025 » ×3 chacun ;
- JOURNAL.md : chemins à lettre de lecteur ×47, `/tmp/` ×24, nom d'organisation ×10, « pocket » ×49 ;
- ADR-0028, annexes B et D : nombreux motifs (chemins, noms de dépôt, ADR-0025, pocket) ;
- journal G1 du rédacteur (`docs/G1-rapport-docs11.md`) : `/tmp/` ×1, « ADR-0025 » ×3 ; journal G1 de POST-PREREG :
  « ADR-0025 » ×1, « pocket » ×2 ; `AVIS-SEUIL-FLUX-QUASI-MORT.md` et `CORRECTIONS-G2.md` des sorties PP/ : « ADR-0025 »
  ×1 chacun.
- Sans motif : sceau (deux README), docs 04, 08, 09, 10, autres sorties PP/.

## 4. Contrôle 3 — aucun nombre inventé, retiré ou changé hors identifiants

- **Par bloc du diff GNU** (suites de chiffres, outil à moi) : 0 chiffre ajouté ; retirés : « 0025 » ×2 (ADR-0025, E-05 et
  E-07), « 1 » (« déc. 1 », E-05), « 2 » ×2 et « 04924 » (« D.2 n° 2 » et le commit de D.2 n° 12, E-10), « 90684 » et
  « 2 » (identifiant de session, E-11). Tous des identifiants. Le contrôle du worker relève les mêmes retraits (11
  entrées de jetons : ADR-0025, D.2, le commit de D.2 n° 12, l'identifiant de session et leurs suites de chiffres).
- **Sondage indépendant de 55 valeurs** (`sondage_g2.py`, valeurs choisies par moi) : verdict « R1 discrimine » = FAUX
  (gras et ligne imprimée), « NE REJETTE PAS, au titre de », énoncé de discordance, z_s, z_bloc, P̂_more des deux
  strates, n et K, EMD, FIV, σ̂²_bloc, k_eff, k nominal, 35 982, 38 600, empreintes du paquet, du manifeste, du jeton, du
  premier paquet et du premier manifeste, genTime et séries des deux jetons, ligne `Time stamp` d'OpenSSL, commit
  d'analyse `f35a70c19ba8…`, sha256 de `rendu_unique.py`, sha256 des trois journaux et du fichier de sommes, tailles,
  tête gardée, empreintes du J28 et de l'ENR, Python 3.11.15, z_bloc du J14p, z_pool, compte de Pyth, AS13335,
  démarrages, fenêtres sautées, borne de Bonferroni, 126 valeurs, 398 tests, HOST-DEGRADED-2, z_IF et z_pool,bloc,
  échéance du délai, heures de production et d'écriture de l'ENR. **55 sur 55 au même compte dans la source et le
  brouillon** ; 54 dans des lignes identiques ; 1 (fichier de sommes `70910984…`) dans la ligne que touche E-08
  (« Drive » remplacé), valeur intacte.
- **Contre les pièces primaires du dépôt** (empreintes et en-têtes seulement) :
  - `PAQUET-PREREG-S2.md` `4d2a8276…f528` ; au commit `3be95be` : `4d2a8276…` ; au commit `ddf8c54` : `494d770d…8097` ;
  - manifeste `sceau/PAQUET.sha256` `51942351…a3e9` ; jeton `paquet.tsr` `9edb19b5…6b0e` ; `openssl ts -reply -text` :
    `Serial number: 0x08CFC8D5`, `Time stamp: Oct  3 01:04:10 2026 GMT` ; premier sceau : manifeste `680a95fd…4209`,
    `0x08CC76D7`, `Oct  2 17:44:30 2026 GMT` ;
  - `bash scripts/sceau/verify.sh` (lu en entier, n'écrit rien) : sortie 0, `docs/adr-0028/PAQUET-PREREG-S2.md: OK`,
    `Verification: OK` deux fois ;
  - commit d'analyse : `git rev-parse f35a70c` → `f35a70c19ba8269f1f7e2bcd31775e4fc513da20` (objet `commit`) ;
    `rendu_unique.py` à `f35a70c` : `06d189cf…9050` ; tête gardée `27b0e30` → `27b0e303f196699959bddc2607db6a1d808ce0db` ;
    `f35a70c` ancêtre de `27b0e30` ;
  - les sept empreintes de la table des conventions (SUITE, J14p, J14s, J28, RT, RAW, ENR) : **égales** ;
  - blocs recopiés, comparés par empreinte seule aux lignes du rendu J28 qu'ils citent : verdict (J28 l.435515-435522 et
    l.435522), tête de certificat R2 (l.435779-435797), décomposition de K (l.435531-435533) : **identiques à l'octet**.

## 5. Contrôle 4 — registre du doc 09

- Les 15 locutions de la gate S-G4, relues dans `xtask/src/sg4.rs` (`LOCUTIONS_INTERDITES`) : 0 occurrence dans le
  brouillon.
- Racines du doc 09 cherchées par moi (`vérifi-`, `valid-`, `garant-`, `sûr`, `assur-`, `prouv-`, `proven`, `safe`,
  `ensure`, `sécuris-`, `reproductib-`, `décentralis-`, `trustless`, `sans confiance`, `publiquement`, `dit vrai`,
  `donnée vraie`, `prix correct`, `qualité`, `k sources`, `indépendant`, `divers`) : les seules touches sont des noms
  de calcul (`--verifier`, « vérificateur du journal brut »), des sorties verbatim (`Verification: OK`), l'hypothèse statistique « à fenêtres indépendantes » ou
  « paires indépendantes », l'indépendance de code (« implémentation indépendante », « code indépendant de `r1` »), le
  rôle « validateur(s) », et les trois exceptions motivées par le worker : « « 10 sources / 11 flux » » ×2 (sortie
  imprimée, colonne k nominal_s) et « validé le texte et le format, pas les valeurs » (§9.2 pt 20, forme « reviewed
  (qui) » à portée bornée). « Il n'établit pas l'indépendance des sources (doc 09) » est présent.
- E-03 (« rapport validé » → « rapport ») est un resserrage admissible. Avis : registre tenu.

## 6. Contrôle 5 — les 16 passages gardés (avis du réviseur)

| n° | avis | motif |
|---|---|---|
| G-01 `claude-opus-5-5` | garder | identifiant de modèle, pas d'instance ; valeur de l'enregistrement scellé (ENR l.2) ; dire qu'une IA a rédigé et exécuté informe le lecteur |
| G-02 poste de l'investisseur, « pas sur mon PC » | garder la limite ; citation verbatim au choix de l'investisseur | un seul observateur sur un poste personnel Windows est une limite déclarée (point 2) ; la consigne verbatim est une donnée qui le concerne : il peut préférer une phrase neutre |
| G-03 « (Recommandé) » | garder | réponses recopiées mot pour mot ; les couper altérerait des citations |
| G-04 AVIS-advisor-defi | garder | dans une ligne imprimée par le rendu scellé ; avis hors dépôt (ADR-0028 l.10), distinct de la pièce D.2 n° 8 ; étiquette sans contenu |
| G-05 décision 270 | garder | imprimée par le rendu (J14s l.1) et motif de la seconde coupe (D4) ; renvoi sans contenu privé |
| G-06 « JOURNAL l. » | garder comme provenance | mais JOURNAL.md n'est pas publiable en l'état (comptes du §3) : relève de PERIMETRE |
| G-07 control, journal, raw `.jsonl` | garder | nom et sha256, ce que D.2 n° 7 admet ; indispensables au pré-enregistrement et à la reproduction |
| G-08 MONARK | garder sous décision explicite de l'investisseur ; motif à corriger (C-1) | nécessaire à la déviation déclarée ; ADR-0028 §4 pt 5 lui réserve la formulation publique |
| G-09 session cloud | garder | rôle, sans identifiant |
| G-10 « validé le texte et le format, pas les valeurs » | garder | limite recopiée du paquet, sujet nommé, portée bornée |
| G-11 « 10 sources / 11 flux » | garder | sortie imprimée recopiée, sous la colonne k nominal_s |
| G-12 J14 | à trancher par l'investisseur | garder seulement si son feu vert écrit couvre explicitement le J14 (ADR-0028 D4) ; sinon retouche déclarée qui retire les valeurs du J14 |
| G-13 processus 943, préfixe des rendus | garder | désignent les sorties, pas une session |
| G-14 `docs/adr-0028/` | garder | provenance ; ces chemins pointent vers le dépôt privé (C-2, PERIMETRE) |
| G-15 « du worker » | garder | auteur des analyses d'après pré-enregistrement et choix déclarés (limites) |
| G-16 poste local | garder | désignation générique |

## 7. Contrôle 6 — ce que l'investisseur doit trancher, en langage clair

**La phrase « Pyth est mort » (§9.3 pt 8, brouillon l.898).** Ce que montrent les données : le service de Pyth que
notre collecteur interrogeait a refusé l'accès (réponse HTTP 401, « non autorisé ») dès la première heure et pendant
toute la campagne : aucune des 40 804 lectures n'a donné de prix. Pyth a donc été retiré de l'analyse. Rien ne montre
que le réseau Pyth lui-même était en panne ; le rapport le dit ailleurs : « aucune mesure de ce rapport ne porte sur
lui » (§4.4). Le risque : publiée avec le nom de Pyth, la phrase se lit comme « Pyth a été en panne 33 jours ». Ce qu'il
faut trancher : (a) garder la phrase telle quelle (fidélité mot pour mot au rapport source) ; (b) la remplacer dans la
seule version publique par une phrase factuelle, par exemple « le flux pyth n'a donné aucune lecture valide sur toute la
campagne : le service interrogé a refusé l'accès (HTTP 401) dès le premier jour », retouche déclarée, aucun chiffre
changé ni ajouté ; (c) corriger d'abord le rapport source par un ajout daté, puis reconstruire la version publique.
Avis du réviseur : (b) ou (c), avant tout préavis envoyé à Pyth ; la limite elle-même (un flux d'oracle perdu, chainlink
lu par un seul RPC public) reste entière.

**La publication du J14 (ADR-0028 D4).** Le J14 désigne deux coupes du début de la campagne (les 14 premiers jours, et
une coupe au 4 septembre), calculées avec la même règle mais étiquetées « hors décision » : elles ne peuvent pas changer
le verdict. Dans la coupe principale, la règle aurait répondu « oui » en semaine (rejet en strate calme, z_bloc ≈ 2,65),
à l'inverse du verdict final sur 33 jours (« R1 discrimine » = FAUX). L'ADR-0028 D4 dit : le J14 n'est publié que sur
décision de l'investisseur. Le brouillon le publie (§7.1, §7.2, avec renvois aux §1, §2.7, §4.3, §7.3, §7.6, §9.3,
§10.4). Donc un feu vert donné sur ce brouillon publie aussi le J14 : il faut l'écrire explicitement. Ce qu'il faut trancher : publier
le J14 avec son étiquette (transparence : tout ce qui était prévu est montré, même ce qui va dans l'autre sens ; le
cacher ressemblerait à un tri des résultats) ou demander une version sans le J14 (retouche déclarée de plusieurs
sections). Avis du réviseur : publier avec l'étiquette, mais c'est sa décision, et elle doit figurer dans son feu vert
écrit.

## 8. Contrôle 7 — les cinq items proposés par le worker

| item proposé | avis | motif |
|---|---|---|
| SHOGEN-PUBLIC-PERIMETRE-1 (pièces qui accompagnent le rapport) | **former** | bloquant pour publier : le rapport promet un contrôle du sceau et des calculs par un tiers, mais les pièces sont au dépôt privé ; plusieurs pièces liées par empreinte portent des motifs privés (§3 : ENR avec des chemins de `docs/pocket-report/`, `docs/15-`, `docs/16-` ; paquet scellé ; trois rendus ; JOURNAL) et ne se filtrent pas sans casser leur empreinte. Ajouter ces faits à l'item |
| SHOGEN-PUBLIC-J14-1 | **former** | fermeture : mention explicite du J14 dans le feu vert écrit (§7) |
| SHOGEN-PUBLIC-PYTH-LIBELLE-1 | **former** | à trancher avant le préavis privé à Pyth (§7) |
| SHOGEN-PUBLIC-MENTION-FEU-VERT-1 | **former** (ou l'écrire au G0 du versement) | au feu vert, remplacer la mention de brouillon : une date ajoutée serait refusée par le contrôle (« nombre inventé ») ; il faudra une retouche déclarée et une exception motivée du contrôle |
| SHOGEN-PUBLIC-MOTIFS-OUVERTS-1 | **former**, fermeture par la lecture de l'investisseur | ma recherche indépendante et mon inventaire n'ont trouvé aucun nom privé inconnu ; seul l'investisseur connaît tous les noms privés |

Item supplémentaire proposé : **SHOGEN-PUBLIC-MONARK-1** — nommer publiquement MONARK et la mesure M009a dans la
déviation déclarée (§10) et le test de composition (§8.6, §12) : décision de l'investisseur (ADR-0028 §4 pt 5) ; à
défaut, retouche déclarée « un projet connexe ». Fermeture : sa réponse écrite.

## 9. Observations non bloquantes (facultatives)

- **O-1 (E-04)** : la liste « réponses de l'investisseur recopiées » (§1, l.75-77) omet sans le dire la réponse sur la
  priorité. Le motif est exact (JOURNAL l.322 la rattache à ADR-0028 §4.7, positionnement commercial, pas à D6 (vi) ni à
  D9). Une phrase neutre sans chiffre (« une réponse de stratégie commerciale n'est pas reprise ») rendrait l'omission
  visible.
- **O-2 (E-06)** : « chemin de fichier sur un volume local » perd l'indice qui montrait l'hôte Windows (la lettre de
  lecteur). « chemin de fichier à lettre de lecteur » le garderait, sans chemin.
- **O-3** : l.77 fait 177 caractères après la jonction de E-03 et E-04 ; remise en forme possible, sans changement de
  contenu.
- **O-4 (versement, pour l'orchestrateur)** : la table de correspondance recopie les passages retirés (pièce interne) ;
  les copies `mutants/texte/` du worker et ma copie `g2/rejeu-mutants/` portent à dessein les motifs injectés (chemins,
  nom d'organisation, identifiant de session court, commit de D.2 n° 12, Pocket) : à tenir hors de tout export public ;
  l'identifiant de la session de D.2 n° 11 n'y figure pas (0 fichier).

## 10. Questions pour l'investisseur (langage clair)

1. **Le J14.** Le rapport montre aussi les résultats des 14 premiers jours. Sur cette période courte, la règle aurait
   dit « oui, il y a un signal » ; le résultat final sur 33 jours dit « non ». Ces chiffres sont marqués « hors
   décision ». Vos règles disent que le J14 n'est publié que si vous le décidez. Publiez-vous le J14 avec le rapport
   (recommandé : tout montrer), ou voulez-vous une version sans lui ?
2. **« Pyth est mort ».** En réalité, le service de Pyth que nous interrogions nous a refusé l'accès dès le premier
   jour : nous n'avons eu aucune donnée, mais rien ne montre que Pyth était en panne. Gardez-vous la phrase, ou la
   remplace-t-on dans la version publique par une phrase factuelle (recommandé, avant d'écrire à Pyth) ?
3. **MONARK.** Le rapport nomme 9 fois votre projet MONARK, surtout pour déclarer qu'une mesure MONARK avait calculé un
   taux sur les données de S2 avant le scellement ; cette déclaration est nécessaire à l'honnêteté du pré-enregistrement.
   MONARK n'est nommé dans aucun des documents du projet destinés au public (présentation, vision, feuille de route).
   Acceptez-vous qu'il soit nommé publiquement, ou faut-il écrire « un projet connexe » ?
4. **Ce que vous publiez avec le rapport.** Le rapport dit qu'un tiers peut vérifier le sceau et les calculs avec les
   rendus, mais tout est dans un dépôt privé. Publiez-vous le rapport seul, ou avec le sceau et les rendus ? Attention :
   le fichier d'enregistrement de l'exécution contient des noms de fichiers de dossiers confidentiels (dont celui du
   rapport Pocket et les documents 15 et 16), le paquet scellé contient le nom de votre organisation GitHub, trois rendus contiennent un chemin
   de votre disque ; ces fichiers ne peuvent pas être nettoyés sans casser leurs empreintes.
5. **Votre poste personnel.** Le rapport dit que la collecte tournait sur votre ordinateur personnel et cite votre
   consigne « cette fois on le fait sur un VPS, pas sur mon PC ». Le fait doit rester (c'est une limite de la mesure).
   Gardez-vous la citation mot pour mot, ou une phrase neutre ?
6. **Noms privés.** En relisant, voyez-vous un nom (personne, société, dépôt, machine) qui ne doit pas sortir ? Notre
   recherche n'en a trouvé aucun, mais vous êtes le seul à les connaître tous.
7. **Préavis privé.** La liste des 22 acteurs nommés (dont 11 sources mesurées) est prête (`ACTEURS-NOMMES.md`) ; le
   préavis se fait avant la publication et après vos réponses 1 à 3.

## 11. Contrôles annexes

- **Tests du worker** : `tests/lancer_tests.py outils` rejoué : `Ran 61 tests`, `OK`, sortie 0 ; fixtures calculées à la
  main ; aucun cache Python écrit. Les tests figent `len(EDITS) == 13` mais ni le texte de E-01 ni le nombre de passages
  gardés : C-1 à C-3 les laissent verts.
- **Campagne de mutants** rejouée sur une copie (`g2/rejeu-mutants/`, 14:29:21-14:29:31 UTC) : T-0 sortie 0 (code et
  texte) ; « BILAN : 60 mutants ; tués 60 ; vivants 0 ; FATAL 0 », sortie 0 ; classement identique mutant par mutant à
  celui du worker. Le classement suit le contrat (1 tué, 0 vivant, toute autre sortie FATAL).
- **Suite `s2-harness`** (`env -u SHOGEN_S2_CAMPAGNE_CONTROL`, `TMPDIR` dans `g2/tmp-suite/`, `-B`), 14:34:03-14:34:47
  UTC : `Ran 405 tests in 42.820s`, `OK (skipped=2)`, sortie 0 ; aucun fichier du dépôt plus récent que le repère ;
  `git status --short` vide.
- **Liste des acteurs** : 22 lignes ; mes comptes (borne « lettre » par `isalpha`) égalent ceux du worker pour Binance 26,
  Pyth 19, Bitstamp 13, Chainlink 15, Gemini 12, OKX 19, DefiLlama 13. Les « points de lecture à signaler » (§5 de la
  liste) sont exacts et utiles au préavis.
- **Livrables du worker intacts** : empreintes recomptées égales au relevé initial ; aucun fichier hors `g2/` modifié
  après 14:17 UTC.

## 12. Journal de provenance du réviseur (G1)

**Sources**

| source | niveau | portée |
|---|---|---|
| brief G2 (`36eb464d…`) ; brief du worker (`f086b663…`) ; G1 du worker (`30315cb8…`) | [lu] | en entier |
| brouillon `11-mesures-pilotes-public.md` (`903d6d0c…`) | [lu] | en entier, l.1-1077 |
| `docs/11-mesures-pilotes.md` (`fcf93b87…`) | [lu] par différence | brouillon lu en entier et diff GNU (10 blocs) ; comptes et lignes par script |
| `TABLE-CORRESPONDANCE.md`, `diff-source-brouillon.txt`, `ACTEURS-NOMMES.md`, `acteurs_nommes.sortie.txt` | [lu] | en entier |
| `outils/construire_public.py`, `outils/controle_public.py` | [lu] | en entier |
| `outils/acteurs_nommes.py` ; tests ; `mutants/campagne_mutants.py` ; `campagne.sortie.txt` ; `gates/B-brouillon.sortie.txt` | [lu] partiel | l.1-80 ; lanceur en entier, `test_controle_public.py` l.1-150, `test_construire_public.py` l.70-110 et lignes citant E-01 ; l.1-30, 160-215, 278-330 ; tête et queue ; lignes de verdict |
| `docs/adr-0029/G0-lots-S2BIS.md` (`25a82120…`) | [lu] | en entier |
| JOURNAL.md | [lu] | l.382 et l.322 seulement ; ailleurs comptes seuls |
| `docs/09-vocabulaire.md` (`001b9606…`) | [lu] | en entier |
| `docs/adr-0028/ANNEXE-D-preenregistrement.md` (`deb64179…`) | [lu] | l.28-50 (liste D.2) ; l.173 et l.185 (PX-Shogen-13) |
| `docs/adr-0028/ADR-0028-decisions-sortie-S2.md` | [lu] partiel | titres ; l.51-56 (D4) ; l.252-262 (§4) ; lignes citant AVIS-advisor-defi (l.10, 25, 59, 68, 119) et PAROXYSME (l.1, 87, 139, 202) |
| `docs/17-modele-de-menace.md` | [lu] | l.1-12 (en-tête, dont « Classification : interne » l.5) |
| `docs/08-assumptions.md` ; README | [lu] partiel | l.1-8 et lignes citant MONARK (l.39, 40) ; l.1-15 |
| `xtask/src/sg4.rs` | [lu] partiel | `LOCUTIONS_INTERDITES` (l.38 et suivantes), l.142-154 |
| `scripts/sceau/verify.sh` | [lu] | en entier |
| docs 00-14, 17, README, pitch ; paquet, sceau, ADR-0028, annexes B et D, AVIS-SEUIL, G1 de POST-PREREG et du rédacteur, JOURNAL, 7 rendus, ENR, sorties PP/ | comptes seuls | motifs privés et mentions de MONARK, sans affichage |
| paquet, manifestes, jetons ; paquet à `3be95be` et `ddf8c54` ; `rendu_unique.py` à `f35a70c` ; 7 rendus ; 4 plages de lignes du J28 | empreintes seules | sha256 ; en-têtes `openssl ts -reply -text` des deux jetons |
| « le dépôt du projet est privé » | [2nd] | par le brouillon §12 (paquet §12 pt 16), non relu au paquet |
| corpus qualité (doc 02, doc 03) ; pièces D.2 ; dossiers interdits ; `*.jsonl` ; contenu des rendus | [abs] | non ouverts |

**Commandes et sorties** (heures `date -u` ; « 14:2x » quand l'heure exacte n'a pas été lue)

| heure | commande | sortie |
|---|---|---|
| 14:18:03 | `date -u` ; `sha256sum` du brief ; `git rev-parse HEAD` ; `git status --short` | brief `36eb464d…` égal ; `6d463fa…` ; arbre propre |
| 14:1x | `sha256sum` de toutes les pièces du lot | brouillon `903d6d0c…` égal au brief |
| 14:1x | `git log`, `git diff --name-only 75bf258 HEAD` (entrées du lot) | 0 entrée changée ; source `fcf93b87…`, registre `001b9606…` |
| 14:20:39 | `construire_public.py` dans `g2/rejeu-construction/` ; `cmp` | sortie 0 ; brouillon, table et diff identiques à l'octet |
| 14:2x | `controle_public.py` | sortie 0, CONFORME ; 2 lignes différentes (chemins) sur 144 |
| 14:2x | `recherche_g2.py` (`e9e3ac60…`) | 4 touches : 3 faux positifs, « M009 » (R-1) |
| 14:2x | `inventaire_g2.py` (`41f8312c…`) | 640 lignes lues ; aucun reste hors R-1 à R-3 |
| 14:2x | comptes MONARK, Kraidle, Classification ; en-tête du doc 17 | MONARK : README 0, docs 00-07 0, pitch 0, doc 08 2, doc 17 22 ; doc 17 l.5 « interne » |
| 14:2x | origine de PX-Shogen-13 et AVIS-advisor-defi (noms de fichiers, puis lignes de l'ADR-0028 et de l'annexe D) | AVIS-advisor-defi : avis hors dépôt (ADR-0028 l.10) ; PX-Shogen-13 : item PAROXYSME |
| 14:2x | JOURNAL l.322 | « priorité » rattachée à ADR-0028 §4.7 : motif de E-04 exact |
| 14:2x | `diff` GNU ; chiffres par bloc | 10 blocs ; 0 suite de chiffres ajoutée ; retraits d'identifiants seulement |
| 14:2x | `sondage_g2.py` (`9a11275b…`) | 55 valeurs, 55 au même compte ; 1 ligne touchée par E-08 |
| 14:2x | empreintes du sceau ; `git show` des états du paquet et du script, suivi de `sha256sum` ; `git rev-parse` ; `openssl ts -reply -text` | toutes égales (§4) |
| 14:2x | `bash scripts/sceau/verify.sh` | sortie 0 ; `OK`, `Verification: OK` ×2 |
| 14:2x | `sha256sum` des 7 rendus ; empreintes de 4 plages de lignes du J28 | toutes égales |
| 14:2x | racines du doc 09 ; locutions de S-G4 | 0 formule interdite hors 3 exceptions motivées |
| 14:29:21-14:29:31 | campagne de mutants sur copie | 60 tués, 0 vivant, 0 FATAL ; classement identique |
| 14:2x | `lancer_tests.py outils` | 61 OK, sortie 0 |
| 14:3x | `perimetre_g2.py` (`cd11db73…`) ; comptes de chemins interdits dans l'ENR | §3, restes hors du brouillon |
| 14:3x | recomptes des acteurs | égaux après correction de ma borne (E-G2-3) |
| 14:34:03-14:34:47 | suite `s2-harness` | 405 tests, OK (skipped=2), sortie 0 ; aucun fichier du dépôt touché |
| 14:3x | rejeu de la table écrit par moi | 13 retouches, `903d6d0c…`, identique |
| 14:3x | comparaison des sorties du contrôle et extraction des locutions S-G4, refaites sans barre oblique inverse | 2 lignes de chemins ; 0 locution |
| 14:3x | empreintes des livrables du worker | égales au relevé initial |
| 14:40:22 | `date -u` avant rédaction | — |

**Chiffres recomptés** : tous ceux du §4 (55 valeurs, 7 empreintes de rendus, 3 empreintes du sceau, 2 jetons,
2 états du paquet, commit et script d'analyse, 4 plages de lignes) ; comptes du §3 ; 61 tests ; 60 mutants ; 405 tests
de la suite ; comptes d'acteurs (7).

**Écarts du réviseur**
- **E-G2-1** (SHOGEN-HARNAIS-ECHAPPEMENTS-1) : deux commandes ont porté des barres obliques inverses tapées (un `sed`
  dans la première comparaison des sorties du contrôle ; une regex Python dans la première extraction des locutions de
  S-G4). Les deux résultats ont été refaits sans aucune barre (`chr`, comparaison ligne à ligne en Python ; extraction par
  guillemets `chr(34)`) et sont confirmés. Mes quatre scripts : 0 octet 0x5C (contrôlé).
- **E-G2-2** : au-delà du « rapport validé seul » du G0 du lot : empreintes des 7 rendus et de 4 plages de lignes du J28,
  comptes de motifs dans les rendus, l'ENR, le paquet, JOURNAL et l'ADR-0028 avec ses annexes ; aucun contenu de rendu
  affiché. Lignes affichées hors du lot : JOURNAL l.322 (qui porte le mot « Pocket ») et l.382 ; annexe D l.28-50 (liste
  D.2, avec chemins du poste, nom de dépôt privé et identifiant de session, même lecture que le worker) ; ADR-0028 l.10
  (liste d'avis hors dépôt) ; en-tête du doc 17 (chemins de fichiers de cartographie qui ne sont pas des pièces D.2). Le
  contrôle FM-1.1 de ma transcription est un acte de l'orchestrateur.
- **E-G2-3** : mon premier recompte des acteurs utilisait une borne fausse (plage `À-ÿ`, qui contient « × ») ; quatre
  écarts apparents ; recompte corrigé, comptes égaux à ceux du worker.
- **E-G2-4** : la consigne générale « pas de fichier de rapport » et le brief (rapport `G2-DOCS11-PUBLIC.md`) divergent ;
  j'écris le seul livrable du brief, dans `g2/`, et rends son contenu à l'orchestrateur.
- **E-G2-5** : base de ma copie `6d463fa`, postérieure à celle du worker (`75bf258` à `2c2fbe9`) ; entrées du lot
  inchangées ; aucune avance de base de ma part.

## 13. Fichiers du réviseur (dossier `g2/`)

`G2-DOCS11-PUBLIC.md` (ce rapport) ; scripts `recherche_g2.py` (`e9e3ac60…`), `inventaire_g2.py` (`41f8312c…`),
`sondage_g2.py` (`9a11275b…`), `perimetre_g2.py` (`cd11db73…`) et leurs sorties `*.sortie.txt` ; `rejeu-construction/`,
`rejeu-controle.sortie.txt`, `rejeu-tests.sortie.txt`, `diff-gnu.txt`, `verify-sceau.sortie.txt`, `rejeu-mutants/`
(copie et campagne rejouée), `tmp-suite/` (sortie de la suite). Aucune écriture ailleurs.
