# Rapport du générateur de DETTES-T14, avec ses sections datées de correction (transcrit)

> Transcription par l'orchestrateur le 2026-10-10 06:47:25 UTC du fichier RAPPORT-GENERATEUR.md ; contrôle FM-1.1 des transcripts du lecteur du procurement, de l'advisor, du générateur et du réviseur G2, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèles résolus : claude-sonnet-5-5 (lecteur), claude-fable-5-1 (advisor), claude-opus-5-5 (générateur, réviseur). Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# RAPPORT-GENERATEUR — lot DETTES-T14 (BIBLIO)

Générateur G1 `shogen-worker`. Brief : `BRIEF-DETTES-T14.md` (sha256 `e728ff3c8908f2f5732f68b254aaab024c618d8e38784ff86f96d6f0c0744530`),
plus l'ajout de l'orchestrateur reçu vers 02:4x UTC (pièce GitHub, item B.92). Aucune écriture git, aucun commit, aucun
réseau (cargo `--offline`) ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée ; aucune pièce de D.2 ni dossier interdit ouvert.

## 0. Gate 0

Modèle résolu : `claude-opus-5-5` (identifiant exact donné par l'environnement), effort `max` demandé par la fiche.
Écrit en premier acte dans `NOTES.md` (2026-10-10 02:18:42 UTC).

## 1. Base et série

- Base des diffs : tête `ba5ea95709e122349448c5e3f024b0ca08d83e91` (2026-10-10 02:34:10 UTC, versement DETTES-T5, B.92).
  Relevé au départ : `ada4737`, avancée par l'orchestrateur ; aucun diff n'existait avant l'avance : toute la série est
  écrite contre `ba5ea95`. Les fichiers touchés sont égaux à la tête dans la copie de travail du dépôt (`git diff HEAD`
  vide) ; quatre fichiers d'une autre chaîne y sont indexés (`s2-harness/tests/…`, `s2bis/tests/…`) : non touchés.
- Copie : `git archive ba5ea95` sans `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`,
  `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/`, `**/*.jsonl` (`copie-base/`).
- Série DT14-a … DT14-i : `git apply --check` puis `git apply`, dans l'ordre, sur une copie neuve : 9/9, état final égal
  à l'état généré (`cmp`). Sha256 et lignes : §11.

| diff | fichiers | + / − | objet |
|---|---|---|---|
| DT14-a | `biblio/INDEX.md` | +51 −9 | compte (196), règle en tête (3 lignes de l'avis, mot pour mot), section des 35 artefacts |
| DT14-b | `biblio/INDEX.md` | +9 −0 | notes datées en fin de registre : renvoi de la règle, UConn ch. 9, Dong 2010 (dette 6), P-01, P-03, Agresti |
| DT14-c | `docs/10-mesures-pilotes-design.md` | +48 −0 | P-03 (§4.2), DONG-CORPS-1 (§4.2), BIBLIO-PAGES-4-3-1 (§4.3), dettes 1, 4, 7 (§10) |
| DT14-d | `docs/06-etat-de-lart-diversite.md` | +29 −0 | FETCH-AVANT-PUB-1, NUREG/CR-5485, « Finkbeiner 2025 », Ron/Nogueira, Eskandari |
| DT14-e | ADR-0028, annexe A | +5 −0 | erratum de D2 pt 4 (POOLEE-SOURCE-1) ; P-14 (§1 bis.7) ; erratum de la ligne POOLEE (annexe A) |
| DT14-f | `docs/11-mesures-pilotes.md` | +42 −0 | §11.1 : PEARSON-IF, R1-PLUGIN-1 (b), DEP-FENETRES-2 (a), CENSURE-INFO-2 |
| DT14-g | `docs/17-modele-de-menace.md` | +1 −0 | E1-METHODE-1 (i) |
| DT14-h | `revue-dettes5/ADJUDICATION.md`, son `SHA256SUMS` | +2 −2 | guillemets « » rétablis à la l.7 (B.92) ; somme de la l.1 du manifeste suivie |
| DT14-i | `WISHLIST.md` | +31 −0 | priorité 6 : P-15 (achat décidé), optionnels, gestes gratuits ; P-01 et P-03 sans objet |

Aucune ligne existante n'est réécrite, sauf : la ligne du compte de l'INDEX (S-G6 l'exige à chaque versement) ; quatre
paires de lignes de l'en-tête de l'INDEX rejointes (fins de ligne devenues espaces, texte identique : assertion du
générateur ; motif en Q-2) ; la l.7 de `ADJUDICATION.md` et la l.1 de son `SHA256SUMS` (demande de l'orchestrateur, B.92).
Chaque ajout porte l'heure `date -u` de la dernière écriture de son texte (`blocs/HORODATAGES.txt`).

## 2. Items : fermeture

| item | fermé par | phrase (où) | citations contrôlées (id du contrôle) |
|---|---|---|---|
| P-01 | DT14-b (note 4) | INDEX, note datée : pages visées lues sur l'image, sans lacune | ku-1219, ku-1225, ku-1226 |
| P-03 | DT14-c, DT14-b (note 5) | doc 10 §4.2, erratum daté (Q-E) ; `report.py` inchangé | fi-p14, fi-p14-normal, fi-p18, fi-p10 ; « n − 3 » lu sur l'image |
| P-05 | DT14-a, DT14-f | INDEX (DOI confirmé, préimpression) ; docs/11 §11.1 | kv-* |
| P-08 | DT14-a, DT14-f | INDEX (H&M version d'auteur, L&R ch. 1) ; docs/11 §11.1 ; aucun achat (Q-B) | hm-*, lr-* |
| P-10 | DT14-a, DT14-e | INDEX ; ADR §1 bis.7 | nk-* |
| P-11 | DT14-a | INDEX : RFC 3161 détenu à l'octet (copie du 2026-10-09 non versée, doublon), §2.1-§2.2 lus ; RFC 3628 versé | rfc3161-*, rfc3628-* |
| P-14 | DT14-e | ADR §1 bis.7 : « choix de conception » documenté (Q-C) | nk-embargo, osf-48h, osf-4ans |
| SHOGEN-PEARSON-IF-SOURCE-1 | DT14-a, DT14-f | docs/11 §11.1 : éq. (4) de Croux et Dehon, forme du code confrontée (`contenu.py` l.5, l.31), limite | cd-* |
| SHOGEN-DONG-CORPS-1 | DT14-a, DT14-b, DT14-c | doc 10 §4.2 et §10 (dette 1) ; INDEX, dette 6 fermée | d10-*, d9-* |
| SHOGEN-BIBLIO-PAGES-4-3-1 | DT14-a, DT14-c | doc 10 §4.3 et §10 (dette 4, fermée par Q-D, résidu écrit) | cg-pairs, py-*, pp-* |
| SHOGEN-FETCH-AVANT-PUB-1 | DT14-a, DT14-d, DT14-i | doc 06 §5 (onze demandes formées et traitées) ; WISHLIST (Malkhi-Reiter) | lps-*, ra-*, jm-*, vd-*, ron-*, esk-*, contrôles dédiés |
| SHOGEN-S2BIS-RFC-REGISTRE-1 | DT14-a | INDEX : trois entrées lues sur pièce ; limite « 0 à 2^32 exclu » [inféré] | rfc6793-*, rfc5398-*, rfc5737-* |
| SHOGEN-R1-PLUGIN-1 | DT14-a, DT14-f | docs/11 §11.1 : statistique et niveau sourcés, limite en trois membres (Q-3) | cl-*, nist-* |
| SHOGEN-CENSURE-INFO-2 | DT14-a, DT14-f | docs/11 §11.1 : attribution « de type Manski » sourcée | hm-*, lr-* |
| SHOGEN-DEP-FENETRES-2 (a) | DT14-a, DT14-f | docs/11 §11.1 : source détenue ; calcul sous le déclencheur de l'item (Q-5) | kv-* |
| SHOGEN-POOLEE-SOURCE-1 | DT14-a, DT14-b, DT14-e | ADR-0028 D2 pt 4 et annexe A : errata datés (non-attribution, Q-B) | uc-*, psu-*, ag-* |
| SHOGEN-E1-METHODE-1 (i) | DT14-a, DT14-g | docs/17 : méthode en quatre étapes, correspondance [inféré] | sp154-*, csrc-* |
| constat WISHLIST | DT14-i | le fichier existe à la racine ; recommandation Q-1 | — |
| B.92 (citation GitHub) | DT14-a, DT14-h | INDEX : page détenue, citation mot pour mot ; ADJUDICATION l.7 : guillemets rétablis | gh-* |

Restent ouverts, sur acte de l'investisseur : **P-15** et **SHOGEN-E1-METHODE-1 (ii)**. Déclencheur exact : l'achat
de l'e-book de Shostack (*Threat Modeling: Designing for Security*, Wiley, 2014, ISBN e-book 978-1-118-81005-7 ;
54,00 USD lus le 2026-10-09), décidé en Q-B. Au versement de l'e-book : entrée d'INDEX (règle en tête), lecture des
pages de P-15 (annexe B l.155), révision datée de docs/17 (STRIDE, critères de sortie, listes d'attaquants). Sans
achat : toute reprise de Shostack sort de docs/17 (Q-B). Fait maintenant : extraits officiels versés, table des
matières lue (pp. 29, 34, 61, 85, 477 sur l'image), achat inscrit à `WISHLIST.md` (DT14-i).

## 3. Phrases de fermeture proposées pour le bloc daté de l'annexe B

- **P-01 fermé** : scan détenu (`biblio/kunsch1989-aos-17-3-1217.pdf`) ; pages 1219, 1224-1227, 1231 et 1234 lues
  sur l'image le 2026-10-09 (lecteur du procurement), sans lacune ; citations recontrôlées par script (DT14-b).
- **P-03 fermé** (Q-E) : Fisher 1921 détenu et lu, *Metron* pp. 14 et 18, poids (n − 3) sur l'échelle z ; la forme
  1/√(n−3) est celle du manuel (Penn State STAT 509 L7) ; erratum daté de doc 10 §4.2 (DT14-c) ; `report.py` inchangé.
- **P-05 fermé** : DOI 10.1017/S0266466605050565 confirmé ; préimpression CAE WP 05-08 versée, Tables I à V lisibles ;
  pagination 1130-1164 non citable depuis cette copie (DT14-a).
- **P-08 fermé** (Q-B, aucun achat) : Horowitz et Manski, version d'auteur de juin 1999, et Little et Rubin, extrait
  officiel du chapitre 1, versés ; Manski 2003 et Little et Rubin entier restent optionnels à `WISHLIST.md` (DT14-a,
  DT14-i).
- **P-10 fermé** : préimpression OSF (CC0) versée et lue pour P-14 : aucune durée (PDF p. 5) ; version *PNAS* non lue,
  geste gratuit de l'investisseur, non bloquant (DT14-a).
- **P-11 fermé** : RFC 3161 détenu à l'octet (`ietf-rfc3161-time-stamp-protocol-2026-10-04.txt`, égal à la copie du
  2026-10-09), §2.1 et §2.2 lus et cités ; RFC 3628 versé (DT14-a).
- **P-14 fermé** (Q-C) : « choix de conception » documenté à ADR-0028 §1 bis.7 : P-10 ne fixe aucune durée ; OSF,
  48 h d'annulation et 4 ans d'embargo, précédent de pratique, non norme (DT14-e).
- **SHOGEN-PEARSON-IF-SOURCE-1 fermé** (Q-C) : Croux et Dehon 2010, éq. (4), versé ; la forme de `contenu.py` est
  l'éq. (4) en coordonnées centrées-réduites ; limite : énoncée au modèle Φρ, non hors de lui (docs/11 §11.1, DT14-f).
- **SHOGEN-DONG-CORPS-1 fermé** : corps de Dong 2010 lu, PVLDB 2009 versé et lu ; la lignée se cite pour l'idée de
  (2c), non pour sa statistique (doc 10 §4.2 et §10, DT14-c ; INDEX, dette 6, DT14-b).
- **SHOGEN-BIBLIO-PAGES-4-3-1 fermé** par la décision Q-D, résidu écrit : substitut d'API pour CoinGecko
  (`pairs` = 1372) ; page Pyth retirée, citation datée gardée ; copie du jour des publishers ; aucune copie du
  2026-08-05 détenue (doc 10 §4.3 et §10, DT14-c).
- **SHOGEN-FETCH-AVANT-PUB-1 fermé** : onze demandes formées et traitées : huit détenues (dix pièces), une à l'achat
  optionnel (Malkhi et Reiter, `WISHLIST.md`), deux introuvables (NUREG/CR-5485 gardé « copie non détenue » ;
  « Finkbeiner 2025 » : attribution retirée) (doc 06 §5, DT14-d).
- **SHOGEN-S2BIS-RFC-REGISTRE-1 fermé** : RFC 6793, 5398 et 5737 au registre, lues sur pièce ; l'encadrement
  « 0 à 2^32 exclu » d'`asn.py` l.18 découle de l'encodage sur quatre octets [inféré] (DT14-a).
- **SHOGEN-R1-PLUGIN-1 fermé** (Q-C) : statistique et niveau sourcés (Chen et Liu 1997 ; NIST §1.3.5.15), limite en
  trois membres lue sur la page courante ; le test n'est pas calculé, son niveau n'étant pas tenu (docs/11 §11.1,
  DT14-f).
- **SHOGEN-CENSURE-INFO-2 fermé** : attribution « de type Manski » sourcée (Horowitz et Manski, approche worst-case,
  bornes sharp ; limite : paramètre de population contre statistique de test [inféré]) ; borne de z_bloc :
  SHOGEN-CENSURE-ZBLOC-1 (docs/11 §11.1, DT14-f).
- **SHOGEN-DEP-FENETRES-2, volet (a)** : source détenue (P-05) ; correspondance b = 240/n_s [inféré] ; le calcul relève
  de l'item sous son déclencheur (run maximal ≥ ℓ), non atteint au J28 ; l'item reste ouvert pour (c) (docs/11 §11.1,
  DT14-f ; Q-5).
- **SHOGEN-POOLEE-SOURCE-1 fermé** (Q-B) par non-attribution : errata datés d'ADR-0028 D2 pt 4 et de la ligne POOLEE
  de l'annexe A ; z stratifié sous indépendance (UConn, Prop. 12.3), distinct de la statistique CMH (Agresti 2013
  p. 227 ; PSU STAT 504 §5.3.5) ; paquet scellé inchangé (DT14-e, DT14-a, DT14-b).
- **SHOGEN-E1-METHODE-1 (i) fermé** : NIST SP 800-154 (projet) versé et lu ; méthode en quatre étapes ; correspondance
  avec la forme de docs/17 [inféré] (DT14-g). **(ii) ouvert** : déclencheur, l'achat de Shostack (P-15).
- **Constat WISHLIST** : le `WISHLIST.md` de l'annexe B l.155 est le fichier de la racine du dépôt (versionné, 8
  commits) ; le constat « biblio/WISHLIST.md absent » venait d'un numéro de ligne d'extrait (l.21) et d'un chemin
  supposé ; aucune référence à corriger ; `WISHLIST.md` reçoit P-15 et les optionnels (DT14-i).
- **Retouche déclarée qui annule celle du B.92** : `docs/adr-0028/revue-dettes5/ADJUDICATION.md` l.7, guillemets « »
  rétablis ; la page du changelog GitHub du 2026-05-14 est détenue et la citation contrôlée mot pour mot à l'INDEX ;
  la l.1 du `SHA256SUMS` du dossier suit (DT14-h, DT14-a). La mention « [2nd, recherche du jour] » de la l.7 reste
  telle quelle : elle date l'état de la pièce au jour de l'adjudication.

## 4. Questions à l'orchestrateur (Q-n), avec recommandation et texte écrit

- **Q-1 — WISHLIST.** Fait : `WISHLIST.md` existe à la racine (versionné, 8 commits, dernier `8ce63ec` du 2026-08-20 ;
  sa règle des rediffusions pirates est l.31-33) ; l'annexe B l.155 le nomme sans dossier ; « l.21 » est la ligne de
  l'extrait du procurement ; `biblio/WISHLIST.md` serait ignoré par git (`.gitignore` l.7-8). **Recommandation** : ni
  correction de référence ni fichier neuf ; ajout daté à `WISHLIST.md` (DT14-i, écrit) et la phrase de fermeture du §3.
  Effet de bord à adjuger : DT14-i rend sans objet l'acte 8 du §1 bis.11 d'ADR-0028 (WISHLIST P-01, P-03), reste de
  SHOGEN-ERRATA-ADR0028-1 (annexe B l.727-730), item hors de la liste de ce lot : je ne le déclare pas fermé.
- **Q-2 — Placement de la règle en tête d'INDEX.** Une insertion simple décalait toutes les lignes du registre ; or au
  moins 12 documents nommés citent l'INDEX par numéro de ligne, dont le paquet scellé (5 fois : l.328, l.336, l.337,
  l.338 deux fois) et docs/17 (`biblio/INDEX.md:18`, `:19`), que S-G9 ne contrôle qu'en plage, pas en contenu.
  **Recommandation (appliquée, DT14-a)** : la règle tient en tête sans décaler une ligne : les paires de lignes 6-7,
  8-9, 10-11 et 12-13 de l'en-tête sont rejointes (texte identique au caractère près, blancs repliés ; assertion du
  générateur), et titre plus trois lignes prennent la place libérée ; tout le reste de l'INDEX va en fin de registre.
  Autre forme, si l'orchestrateur refuse de toucher aux fins de ligne de l'en-tête : la règle en fin de registre, avec
  un renvoi dans la ligne du compte (que S-G6 oblige déjà à réécrire).
- **Q-3 — Limite de R1-PLUGIN-1 (Q-C).** La page NIST §1.3.5.15 du 2026-10-09 a remplacé sa section « Definition »
  le 2024-04-01 : la règle « the expected frequency should be at least 5 » et le regroupement des classes de queue ne
  sont plus qu'en commentaire HTML (0 occurrence au texte affiché ; le procurement les a lus dans le source). Le texte
  affiché fonde les k − c degrés de liberté sur un paramètre estimé par maximum de vraisemblance sur les comptes des
  classes, « not from the individual observations ». **Recommandation (écrite, DT14-f)** : membre (2) reformulé (les
  p̂_i de Shōgen sont estimés sur les fenêtres individuelles : loi nulle non donnée par la source) ; membre (3) devenu
  choix de conception, la règle « ≥ 5 » n'ayant plus de source affichée.
- **Q-4 — Limite de PEARSON-IF (Q-C).** L'avis proposait « hors normalité la IF diffère ». Non retenu : en
  coordonnées centrées-réduites, la fonction d'influence du coefficient de Pearson a la même forme pour toute loi à
  variances finies [inféré : IF(Cov)/(σxσy) − (ρ/2)(IF(σx²)/σx² + IF(σy²)/σy²), avec IF(Cov) = x̃ỹσxσy − Cov et
  IF(σ²) = (x − μ)² − σ², donne x̃ỹ − (ρ/2)(x̃² + ỹ²)] ; ce qui dépend de la loi, c'est sa variance. **Texte écrit** :
  la pièce l'énonce au modèle Φρ (moyennes 0, variances 1 sans perte de généralité, §3) et ne l'énonce pas hors de
  lui ; l'emploi hors de Φρ repose sur la dérivation par fonction lisse de moments [inféré].
- **Q-5 — Portée de « DEP-FENETRES-2 (a) » dans ce lot.** Recommandation : la part procurement est fermée (source
  détenue, valeurs critiques lues) ; le calcul de z_bloc,s contre la valeur critique fixed-b reste dans l'item, sous
  son déclencheur (run maximal ≥ ℓ, non atteint au J28 : 6 et 2). Observation pour qui fera le calcul [inféré] : pour
  toute strate où b = 240/n_s ≥ 0,02, la valeur critique de 99 % de la Table I est ≥ 2,377 > 2,33 ; un seuil plus haut
  sur z_bloc,s ne fait que retirer des rejets : il ne peut pas changer un FAUX en VRAI ; sous b = 0,02, la table ne
  donne rien (la normale, 2,326, est sous 2,33).
- **Q-6 — Items PAROXYSME proposés (règle : toute limite rencontrée est rendue comme item à former).**
  (i) **SHOGEN-SG5-COMMENTAIRE-HTML-1** : S-G5 ne distingue pas un commentaire HTML du texte affiché
  (`retirer_balises` borne une balise à 300 octets ; un commentaire plus long reste au corpus) : une citation d'un
  texte retiré d'une page passe ; construction : ôter `<!-- … -->` avant le débalisage, avec un cas de test sur la page
  NIST ; déclencheur : prochain lot qui touche `xtask/src/sg5.rs`.
  (ii) **SHOGEN-REFS-LIGNE-CONTENU-1** : S-G9 (a) contrôle qu'une référence `chemin:ligne` tombe dans la plage du
  fichier, pas qu'elle désigne encore la même ligne ; toute insertion au milieu d'un fichier cité par numéro de ligne
  passe en vert ; construction possible : empreinte de la ligne citée à côté du numéro ; déclencheur : prochain lot qui
  touche `xtask/src/sg9.rs`.
  (iii) Borne déjà connue, rencontrée : `parait_anglais` exige deux mots-outils ; « Analyze the threat model. » est
  traité comme une citation française par S-G9 (e). Je l'ai évitée (traduction dans docs/17, texte exact à l'INDEX).
- **Q-7 — Versement des octets.** Le compte 196 de DT14-a vaut une fois les 35 artefacts et 24 sidecars copiés dans
  `biblio/` du poste : `outils/verser_biblio.py` (contrôle chaque sha256 contre l'INDEX et chaque sidecar contre
  `outils/SIDECARS.sha256`, refuse toute différence, n'écrase rien). Avant cette copie, S-G6 dit « CORPUS PARTIEL » et
  S-G5 passe en régime de corpus incomplet (§10, exécution r3) : pas de rouge, mais un contrôle moins fort.

## 5. Limites (L-n)

- L-1 : Künsch, pages 1224, 1227, 1231 et 1234 : relevé du lecteur du procurement sur l'image ; je n'ai recontrôlé que
  les phrases lisibles dans l'OCR (pp. 1219, 1225, 1226).
- L-2 : Shostack, table des matières : pages 29, 34, 61, 85 et 477 lues par moi sur l'image ; 125, 133, 189, 198 et
  333 : relevé du lecteur, non relu.
- L-3 : Agresti p. 227 : l'OCR écrit « 2 x 2 » ; aucune citation ne porte ce passage ; l'image n'est pas relue.
- L-4 : RFC 5398, 5737 et 6793 : les Trust Legal Provisions de l'IETF ne sont pas lues ; « redistribuable : non (non
  établi) ».
- L-5 : versions non éditeur (K&V, H&M, Nosek, Croux et Dehon, versions City) : pagination éditeur non citable ; textes
  publiés non comparés.
- L-6 : identité d'« AV 2011 » proposée par le procurement, non confirmée.
- L-7 : pages mutables (NIST, OSF, PSU, Pyth, GitHub, API CoinGecko) : l'ancre est le couple (date, sha256).
- L-8 : la correspondance de docs/17 avec les quatre étapes de SP 800-154 est mon inférence, marquée [inféré].
- L-9 : la copie de vérification exclut les dossiers interdits ; S-G9 y signale `docs/rapports/…:21` introuvable, comme
  sur la tête seule (exécution r0) ; le fichier existe au dépôt (test d'existence seul, contenu non lu).

## 6. Écarts (E-n)

- E-1 : un tube lisait et réécrivait le même bloc (`blocs/wishlist.txt`) : bloc tronqué à 02:55:48, réécrit en entier
  et redaté à 02:56:04 ; ensuite, toute correction de bloc passe par une copie préalable.
- E-2 : mon premier contrôle croisé des guillemets était faux (condition toujours vraie) ; corrigé, montré en échec sur
  une citation inventée (`outils/essai/diffs-faux`), puis rejoué.
- E-3 : un `find` sur ma copie de la tête (`copie-base`, dossiers interdits déjà exclus) pour compter les `*.jsonl` :
  0 ; aucune autre recherche récursive.
- E-4 : des séquences `\u…` tapées dans une commande sont arrivées converties en caractères (consigne
  SHOGEN-HARNAIS-ECHAPPEMENTS-1) ; sans effet sur les octets écrits (contrôlés : `cmp`, sha256, assertions) ; le motif
  qui en dépendait a été modifié par l'outil d'édition, sans shell.
- E-5 : la règle de l'avis n'est pas posée par une insertion simple en tête mais selon Q-2 (même texte, même place
  logique, aucune ligne décalée) : écart de forme au brief, à adjuger.

## 7. Journal de provenance (G1)

**Pièces de pilotage [lu]** : `BRIEF-DETTES-T14.md` (`e728ff3c…0530`, 45 l., entier) ; message de l'orchestrateur
(ajout B.92) ; `procurement/avis/ADJUDICATION.md` (`6a49420c…480f`, entier) ; `AVIS.md` (`181d2e85…397a`, entier) ;
`RAPPORT-PROCUREMENT.md` (`860bfe16…9397`, 190 l., entier) ; `dettes14/ITEMS-ANNEXE-B.md` (`b7e7f279…7dde`, entier) ;
`procurement/ITEMS-ANNEXE-B.md` (l.15-24) ; preuves du procurement (licences arXiv, OSF, fiche CSRC ; `SHA256SUMS-preuves`
rejoué : OK).

**Dépôt à `ba5ea95` [lu]** (lectures ciblées de fichiers nommés) : `biblio/INDEX.md` (entier) ; `WISHLIST.md` (entier) ;
doc 10 (entier) ; doc 06 (entier) ; ADR-0028 l.1-181 ; annexe B l.84-160, 212-223, 722-731, 762-800, B.92 ; annexe D
l.32-48 (D.2) ; annexe A (l.33-36 et carte des lignes) ; paquet scellé l.52-62 ; docs/11 l.976-1047 ; docs/17 l.1-30,
53-58, 72-86 et fin ; `docs/G1-lot-POST-PREREG.md` l.120-140, 290-310, 349-400 ; `scripts/post-s2/contenu.py` l.1-42 ;
`s2bis/shogen_s2bis/collecte/asn.py` l.14-22 ; `s2bis/tests/test_asn.py` l.1-20 ; `revue-dettes5/ADJUDICATION.md`
l.1-9 et son `SHA256SUMS` ; `xtask/src/sg5.rs`, `sg6.rs`, `sg9.rs`, `documents.rs`, `lib.rs`, `main.rs` (portions
lues) ; `enforcement/docs-sha256sums.py` (en-tête) ; `.gitignore` l.1-12. Recherches par motif sur des fichiers nommés
seulement (grep « Mantel|Cochran », références de ligne vers l'INDEX : 12 documents nommés par l'annexe B et la
passation ; liste écrite dans `tmp/noms-annexeB.txt`).

**Pièces [lu]** : les 35 pièces du lot (extraction `outils/extraire.sh` ; HTML : texte affiché, commentaires ôtés) ;
images lues : Kiefer et Vogelsang PDF p. 26 (Table I) ; Fisher PDF pp. 13 et 17 (*Metron* pp. 14 et 18) ; Shostack
table des matières pp. ix, x, xviii. Détenues relues : Fisher, Künsch et Agresti (OCR des sidecars de `biblio/`),
Dong 2010 (extraction refaite), UConn ch. 9 (métadonnées).

**[abs]** : Shostack au-delà du chapitre 1 ; NUREG/CR-5485 ; « Finkbeiner 2025 » ; versions éditeur (*PNAS*, *JASA*,
*SMA*, Cambridge) ; Mantel et Haenszel 1959 ; Cochran 1954 ; Trust Legal Provisions de l'IETF ; conditions d'usage de
GitHub, Pyth, CoinGecko.

**[2nd], attribué dans les textes au lecteur du procurement** : statuts HTTP des tentatives (403, 404, 500) ; identités
tirées de Crossref, OpenAlex et Semantic Scholar (DOI de SMA, ICDCS, PVLDB 2009) ; pages de Künsch lues sur l'image
(1224, 1227, 1231, 1234) ; pages 125, 133, 189, 198, 333 de la table de Shostack ; égalité à l'octet du chapitre 9 UConn
avec le fichier servi ; prix lus sur les fiches Wiley.

**Commandes et sorties (relevées)** :
- `sha256sum` des 59 fichiers de `pieces/` contre `SHA256SUMS` : 57/57 OK ; UConn et son sidecar absents du fichier de
  sommes ; `outils/compare_s4.py` : 35/35 pièces égales au tableau §4 (sha256 et taille) ;
  `outils/extraire.sh` : 24/24 sidecars égaux à l'octet à ma propre extraction ; `cmp` RFC 3161 : identiques.
- `outils/verif_citations.py` (éprouvé sur `outils/essai/` : mot muté, page fausse, ordre inversé, plus de 25 mots :
  refusés) : 129 contrôles, 0 échec (`verif-citations-dt14.tsv`) ; `outils/controles_dedies.py` : Nogueira, 429 : 0,
  115 : 0 ; Eskandari : « open problem » 0, « future work » 0, « common source » 0, « same source » 0, « single
  source » 0, « open question » 1 (titre de référence), « independen » 2 et « correlat » 1 sans rapport.
- `outils/croiser_citations.py` (éprouvé sur une citation inventée) : 179 guillemets ajoutés, 141 contrôlés par
  script, 38 libellés, chaînes d'absence, citations de pièces hors liste ou citations françaises du dépôt ; 12 de ces
  dernières vérifiées par `grep -F` sur leurs fichiers (12/12 trouvées), 4 non vérifiées, dont les deux fausses de la
  revue G2 (C-1, C-2). [Corrigé en phase 2, K-1 : la version adjugée disait 181 et 143, comptes de l'état de 03:10 ;
  §12.3.]
- Page NIST, texte affiché : « at least 5 » 0, « combine some bins » 0, « independent » 0 ; texte brut : les deux
  phrases présentes, dans le commentaire daté 2024/04/01.
- `git apply` de la série sur copie neuve : 9/9 ; état final égal au généré (`cmp`, 9 fichiers + `SHA256SUMS`).
- `python3 -B enforcement/docs-sha256sums.py .` : tête seule : conforme (35 `SHA256SUMS`, 299 lignes) ; série avant
  le suivi de la somme : refus `revue-dettes5/SHA256SUMS` l.1 ; série finale : voir §10.

**Chiffres recomptés** : 35 pièces, 34 versées du procurement plus la page GitHub ; compte 161 → 196 ; 24 sidecars,
31 → 55 ; Table I, 99 % : 2,377 (b = 0,02), 2,459 (b = 0,04) ; `pairs` = 1372 ; références par numéro de ligne vers
l'INDEX : 12 documents nommés, dont 5 dans le paquet scellé ; tranches : +51, +9, +48, +29, +5, +42, +1, +2, +31.

## 8. Actes laissés à l'orchestrateur

1. Adjuger Q-1 à Q-7 ; appliquer DT14-a … DT14-i dans l'ordre (`git apply`, vérifié sur copie neuve de `ba5ea95`).
2. Au même versement, copier les octets privés dans `biblio/` du poste :
   `python3 -I outils/verser_biblio.py biblio/INDEX.md outils/SIDECARS.sha256 biblio <procurement>/pieces dettes14/pieces-orchestrateur`
   (35 artefacts, 24 sidecars ; chaque sha256 contrôlé ; ne copie pas la RFC 3161 du 2026-10-09, doublon). Sans cette
   copie, le compte 196 reste déclaré sur 161 présents (S-G6 « CORPUS PARTIEL », S-G5 en corpus incomplet, vert).
3. Verser au bloc daté de l'annexe B les phrases du §3 ; y former, s'il les retient, les items de Q-6.
4. Transmettre `QUESTION-AVOCAT.md` à l'investisseur (acte de l'investisseur, Q-A) ; inscrire l'achat de Shostack
   (P-15) aux actes de l'investisseur.

## 9. Ajout B.92 : preuve demandée (S-G5)

- `normaliser_pour_recherche` (`xtask/src/documents.rs`, boucle de pli) saute tout caractère `*` et tout accent grave :
  les accents graves de la citation versée ne gênent pas la correspondance ; aucune forme de rechange n'est nécessaire.
- Découpage de S-G5 sur la l.7 rétablie : fragment « update the `runs-on:` target » : un seul mot-outil anglais
  (« the »), non contrôlé (borne `parait_anglais`) ; fragment « to the new label `windows-2025-vs2026` » : contrôlé.
- Contrôle négatif (exécution r1 : tête + DT14-h seul, 161 octets, régime complet) : `VIOLATION
  docs/adr-0028/revue-dettes5/ADJUDICATION.md:7 — citation introuvable … : « to the new label windows-2025-vs2026 »`
  (le fragment imprimé est déjà sans accents graves).
- Série complète : régime complet (196/196) : S-G5 vert, 0 violation ; régime partiel, l'état du dépôt avant versement
  (r3, 161/196) : 0 fragment non contrôlé ; régime CI, INDEX seul (r4) : 280 fragments non contrôlés, aucun de
  `revue-dettes5`, 0 occurrence de « to the new label » : le fragment se résout par l'entrée d'INDEX seule.

## 10. Gates et contrôles (copie de `ba5ea95` sans dossiers interdits ni `*.jsonl`, série appliquée)

`cargo --locked --offline xtask verify`, cible propre au dossier du lot (journal `journaux/verify-final-2.txt`) :

| contrôle | copie définitive (196 octets) | tête seule, r0 (161 octets) |
|---|---|---|
| S-G1 à S-G4, S-G7a, S-G8 | VERT | VERT |
| S-G5 | VERT, 330 fragments contrôlés, corpus 196/196 | VERT, corpus 161/161 |
| S-G6 | VERT, compte déclaré 196 = réel 196 | VERT, 161 = 161 |
| S-G9 | ROUGE, 1 violation : docs/17:71, `docs/rapports/cartographie-2026-09-29.md:21` introuvable | ROUGE, la même à docs/17:70 |
| `cargo fmt --check`, `no_std`, `clippy -D warnings` | VERT, VERT, VERT | non relancés (aucun code touché) |
| VERDICT GLOBAL | ROUGE (S-G9 seul) | ROUGE (S-G9 seul) |

La violation S-G9 tient à la copie partielle : `docs/rapports/` en est exclu par le brief ; la ligne de docs/17 qui la
porte est antérieure au lot (ma série la décale d'une ligne, de 70 à 71) ; le fichier existe au dépôt (test
d'existence seul, contenu non lu). `python3 -B enforcement/docs-sha256sums.py .` : `conforme : 35 SHA256SUMS, 299
ligne(s), dont 11 absente(s) admise(s) (SHOGEN-SIM-SOMMES-1) ; 4 fichier(s) non listé(s), non refusés` (sortie 0).
Suite `s2-harness` (`env -u SHOGEN_S2_CAMPAGNE_CONTROL PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s
tests -t .`) : `Ran 419 tests`, `OK (skipped=2)`, sortie 0 (avant les dernières retouches de texte, aucune ne touche le
code). Exécutions de contrôle r0, r1, r3, r4 : `journaux/gates-r*.txt`.

## 11. Livrables (sha256 : `SHA256SUMS` du dossier)

| diff | sha256 | + / − |
|---|---|---|
| DT14-a | `94c16b789e643e86f95f61a54ac17621c2b4a3f15bf44bdc841da1dac774e171` | +51 −9 |
| DT14-b | `9f14cb30a7ee41d469f89cac31b027bc5096f07f7d84df8a887710486019ce26` | +9 −0 |
| DT14-c | `8808c9694053163b2332bf285e87a460c8e530c405577abd6ccd9d4e8e36bd8e` | +48 −0 |
| DT14-d | `95e1bc6f5f375702315023f6266b7f8ab47e43faf5f398a6c586354d875cd9d8` | +29 −0 |
| DT14-e | `c29960d77104737fb32b57da602f93d45d2ba8b549fa769bc4f30b536030d496` | +5 −0 |
| DT14-f | `29d1f195e7ffb3b715abbfa5896eee4ff0a7f7753a53e46c52d4aeecf450309e` | +42 −0 |
| DT14-g | `e193663491ad5df5c6b9a28023f9cc0f90fbca92d2d033967b22a2eb1f6f72ed` | +1 −0 |
| DT14-h | `2a086c9899ee973eeef1234ba4bc8a6084741c1dfbc009189a683948dade1458` | +2 −2 |
| DT14-i | `d35ee7f3be81a57097b6be2d6f6b5525539c48619d4037ec3566514c74677c9f` | +31 −0 |

Concaténation des neuf diffs dans l'ordre : `fb6e6fe6b055b83827ac718425bd934fe5f093b5b58638d07bf6e9a35163b189`.
Autres : `NOTES.md`, `QUESTION-AVOCAT.md`, `blocs/` (textes datés et `HORODATAGES.txt`), `outils/` (scripts, entrées et
sorties : `verif_citations.py`, `citations_dt14.py`, `citations-dt14.json`, `verif-citations-dt14.tsv`,
`croiser_citations.py`, `croiser-citations.sortie.txt`, `controles_dedies.py` et sa sortie, `compare_s4.py` et sa
sortie, `extraire.sh`, `index_dt14.py`, `generer_diffs.py`, `verser_biblio.py`, `SIDECARS.sha256`, `ecrire_bloc.sh`,
`executions_controle.sh`, `essai/`), `journaux/` (sorties des gates, du `verify`, de la suite).

## 12. Ajout daté du 2026-10-10 05:15:50 UTC (`date -u`) : phase 2, sur l'adjudication de la G2 (ajout de 04:37:02 UTC)

Les §0 à §11 restent la phase 1, telle qu'adjugée, sauf la ligne de K-1 au §7, corrigée et marquée. Ce §12 décrit la
série finale `diffs-c3/`. Ses phrases (§12.8) et ses actes (§12.10) remplacent ceux du §3 et du §8, point 1.

### 12.1 Pilotage [lu]

- `ADJUDICATION.md` du lot : `f66b1947…2f42`, lu en entier, dont l'ajout daté de 04:37:02.
- `g2/RAPPORT-G2.md` : `4539ffdf…549c`, 348 l., lu en entier.
- `g2/corrections/C-1.diff`, `C-2.diff` et `P-1.diff` (sha256 au §12.2).
- Outils du réviseur, lus puis employés sans modification : `refs_decalees.py` (`c15a0ace…7a56`), `refs_index.py`
  (`4a46493b…2fdd`) et `controle_entete.py` (`7e38d8da…c653`), avec sa liste `g2/tmp/noms-g2-presents.txt`
  (`a8de9af4…3b87`, 117 noms).

### 12.2 Acte 1 : C-1, C-2 et P-1 à l'identique

- `diffs/DT14-j.diff` = `C-1.diff` (`ac6d0696…538d8c`), `DT14-k.diff` = `C-2.diff` (`f59b4f2a…3118b35`) et
  `DT14-l.diff` = `P-1.diff` (`190b3008…f9b9`) : contrôle `cmp`, octet pour octet.
- Série `diffs/` a…l : `git apply` 12/12 sur `ba5ea95` et sur `dda4bbc`. Empreinte de la concaténation :
  `4426f867edcd3807cf8539fcaee05065032f86c5e8d54b3703ceb0eac41cbd9b`.
- Cette série garde les positions de la phase 1. Elle est remplacée par `diffs-c3/` (§12.4).

### 12.3 K-1

- Les chiffres « 181 » et « 143 » du §7 et de `NOTES.md` sont ceux de l'état de 03:10 (entrée de 03:10:24 des NOTES).
  Ils ont été pris avant les retouches de 03:18, qui ont réécrit le bloc de docs/11 et celui de l'annexe A à 03:18:47,
  puis la section d'INDEX à 03:18:57.
- La sortie finale de `croiser_citations.py` (03:18:58) dit 179 et 141, et le rapport de 03:22 a repris les chiffres
  de 03:10. Ce sont deux citations de moins dans les blocs retouchés [inféré : leurs versions de 03:10 ne sont pas
  gardées].
- Correction : la ligne du §7 dit maintenant 179 et 141, avec une marque. Dans la même phrase, « 12/12 » est précisé :
  12 citations du dépôt avaient été vérifiées sur 16, et les deux fausses (C-1, C-2) étaient parmi les quatre non
  vérifiées.
- `NOTES.md` est un journal : sa ligne de 03:10:24 garde son chiffre d'époque, et l'entrée de 05:13:18 l'explique.

### 12.4 C-3 : la série corrigée `diffs-c3/`

**Forme.** Chaque ajout daté ou erratum daté de DT14-c à DT14-g et DT14-i est placé en fin de document. Aucune ligne
existante n'est déplacée.
- Doc 10, doc 06, ADR-0028 et docs/11 reçoivent un titre « Ajouts datés en fin de document ». Il est suivi d'une
  phrase datée qui dit pourquoi les ajouts sont là, puis d'un ajout par section visée. Chaque ajout s'ouvre sur
  **Vise …**, nomme la section visée et dit que son texte est inchangé.
- Docs/17 : une puce datée en fin de liste du §7, comme les deux ajouts datés qui l'y précèdent ; elle vise la ligne
  **Forme de la table**.
- `WISHLIST.md` : la priorité 6 vient après « Déjà réglé », avec une phrase sur ce placement.
- Annexe A : l'erratum était déjà en fin de document ; seul son renvoi change.

**Diffs de la série corrigée**, à appliquer dans l'ordre :

| diff | fichiers | + / − | sha256 | origine |
|---|---|---|---|---|
| DT14-a | INDEX | +51 −9 | `94c16b78…e171` | `diffs/`, octet pour octet |
| DT14-b | INDEX | +9 −0 | `9f14cb30…ce26` | `diffs/`, octet pour octet |
| DT14-c | doc 10 | +57 −0 | `1aeed91b…7f91` | relocalisé ; O-2, O-5 |
| DT14-d | doc 06 | +34 −0 | `0d1342d1…3aa2` | relocalisé |
| DT14-e | ADR-0028, annexe A | +9 −0 | `52647335…547a` | relocalisé ; renvoi de l'annexe A |
| DT14-f | docs/11 | +49 −0 | `7574b8f6…4fa5` | relocalisé ; O-3 |
| DT14-g | docs/17 | +1 −0 | `c5c9b1b9…5626` | relocalisé |
| DT14-h | `revue-dettes5` | +2 −2 | `2a086c98…1458` | `diffs/`, octet pour octet |
| DT14-i | `WISHLIST.md` | +32 −0 | `ef815944…97d8` | relocalisé |
| DT14-j | INDEX | +2 −2 | `ac6d0696…538d8c` | C-1, octet pour octet |
| DT14-k | doc 10 | +2 −2 | `aa8eac97…6e9b` | C-2 rebasé |
| DT14-l | `WISHLIST.md` | +6 −1 | `da46b4a1…b8a5` | P-1 rebasé |
| DT14-m | INDEX | +6 −6 | `89eb22c6…bc73` | neuf : O-1, O-4, renvois C-3 |

- Concaténation des treize diffs, dans l'ordre :
  `23bfdaf17372d0d0b304ca54b88e754945bb316641c88111213934b01fe9087d`.
- R-25 : au plus 57 lignes ajoutées par diff. R-13 : 0 TODO, FIXME ou XXX.
- Largeur des lignes ajoutées : doc 10 ≤ 105, doc 06 ≤ 77, docs/11 ≤ 118, `WISHLIST.md` ≤ 94. INDEX, ADR-0028, annexe A,
  docs/17 et `ADJUDICATION.md` portaient déjà des lignes longues (`phase2/forme-diffs-c3.txt`).
- Générateur : `outils/generer_diffs_c3.py`. Il porte une assertion par étape : toute ligne de la base garde son numéro
  et son texte, sauf les réécritures déclarées.

**K et L rebasés.** `outils/memes_changements.py` compare chaque diff rebasé au diff adopté, heures `date -u` masquées
(`phase2/memes-changements-k-l.txt`).
- DT14-k et C-2 portent les mêmes opérations au mot : « Fisher ; » devient « Fisher, », puis « §7.8 » est inséré.
- DT14-l et P-1 portent la même puce, ses cinq lignes ajoutées identiques à l'octet.
- Chaque bloc corrigé est redaté à sa propre écriture : bloc P-03 à 04:56:45, titre de la priorité 6 à 04:56:45.
- **E-6** : pour que C-2 reste un diff distinct, DT14-c remet en fin de doc 10 le texte de phase 1, avec sa citation au
  point-virgule, et DT14-k le corrige. La série s'applique donc entière.

**DT14-m (INDEX)** réécrit sur place six lignes du lot ; aucune n'est insérée ni retirée.
- La ligne datée de la section et celle des notes sont redatées à 04:57:32.
- La rangée Kiefer et Vogelsang est corrigée selon O-4.
- Les notes 3, 5 et 6 renvoient aux ajouts placés en fin de doc 10 et d'ADR-0028 (C-3), et la note 5 dit « ajout
  daté » (O-1).

**Preuves.**
- `refs_decalees.py` du réviseur, sans modification, sur la série (`phase2/refs-decalees-serie-c3.txt`) : 220 renvois
  relevés, **0 décalé**, 0 document. Avec `dda4bbc` pour base : 220 renvois, 0 décalé.
- Variante `outils/refs_decalees_premier1.py` : le même code, exécuté avec PREMIER = 1 pour chaque cible. Elle compte
  tout renvoi dont la ligne a changé, où qu'il pointe. Sur la série : 0. Sur la série de phase 1 : 151 renvois dans
  44 documents, comme le réviseur.
- `outils/lignes_conservees.py`, preuve sans motif de renvoi, fichier par fichier : CONFORME sur `ba5ea95` et sur
  `dda4bbc`. Seules changent les lignes réécrites déclarées : INDEX l.3 et l.6-14, `ADJUDICATION.md` l.7, `SHA256SUMS`
  l.1.
- La même preuve sur la série de phase 1 : NON CONFORME, 843 lignes. En détail : doc 10, 405 dès la l.301 ;
  ADR-0028, 295 dès la l.36 ; docs/17, 106 dès la l.8 ; docs/11, 24 dès la l.1048 ; doc 06, 8 dès la l.124 ;
  `WISHLIST.md`, 5 dès la l.249.
- `refs_index.py` du réviseur : 36 renvois vers l'INDEX. Seule la l.3 diffère, comme en phase 1 : c'est la ligne du
  compte, réécrite à chaque versement.
- Application : `outils/verifier_serie_c3.sh` passe 13/13 sur `ba5ea95` et sur `dda4bbc` (tête du dépôt, relue à
  05:15:26). L'état final est égal à `copie-c3/` (`cmp`). Les fichiers touchés sont identiques entre ces deux commits.

### 12.5 Décalages antérieurs à `ba5ea95`, pour DETTES-T15 (non corrigés)

Outil : `outils/decalages_anterieurs.py`.
- Il relève les renvois avec les motifs du réviseur, lus dans son source, sur ses huit cibles et ses 117 fichiers.
- Il date chaque renvoi par `git blame --porcelain` à `ba5ea95`, en lecture seule. Le paquet scellé est daté par son
  commit de scellement `8b14567`.
- Il compare ensuite la ligne citée au commit d'écriture et à `ba5ea95`. Il n'imprime que des jetons.

Résultat (`phase2/decalages-anterieurs-ba5ea95.tsv`) :
- 311 numéros cités : 228 exacts, 75 décalés, 6 réécrits ou retirés, 2 hors plage.
- 83 renvois non exacts, dans 24 documents : doc 10, 38 ; ADR-0028, 34 ; annexe A, 8 ; docs/11, 2 ; doc 06, 1.
- Paquet scellé : ses six numéros vers doc 10 sont décalés de +2 depuis `8b14567` (paquet l.16 : l.555 et l.579 ;
  l.56 : l.379 et l.380 ; l.63 : l.519 et l.522). Ses renvois à ADR-0028 (l.29-42) et à docs/17 (l.108) sont exacts à
  `ba5ea95` et le restent après la série.
- ADR-0028 renvoie lui-même à doc 10 (l.35, l.41, l.44, l.46, l.119) avec un décalage de +16.

Vers l'INDEX (`outils/decalages_anterieurs_index.py`, `phase2/decalages-anterieurs-ba5ea95-index.tsv`) : 65 numéros,
64 exacts, 1 réécrit (l.3, la ligne du compte).

Limites :
- Le dernier commit qui a touché la ligne d'un renvoi n'est pas toujours celui qui l'a écrit.
- Les deux « hors plage » visent sans doute d'autres documents. Exemple : ADR-0028 l.319, « corpus doc 06 l.269 », vise
  le doc 06 du corpus de conformité, non celui de Shōgen.

### 12.6 O-1 à O-5

- **O-1, traitée.** Note 5 d'INDEX : « ajout daté de doc 10, placé en fin de document, qui vise §4.2 (b) » (DT14-m).
  La phrase de P-03 (§12.8) dit aussi « ajout daté ».
- **O-2, traitée.** L'ajout de fin de doc 10 qui vise §10 dit : « corps de Dong 2010 lu aux pp. 1358-1361 et 1365
  (lecteur du procurement), citations recontrôlées par script » (DT14-c). La phrase de §12.8 le dit aussi. La note 3
  d'INDEX renvoie aux pages qu'elle cite déjà.
- **O-3, traitée.** Puce DEP-FENETRES-2 (a) de docs/11 : « Le calcul de (a) reste dans l'item, sous son déclencheur
  (…) ; l'item reste ouvert pour ce calcul et pour (c). » (DT14-f), repris au §12.8.
- **O-4, traitée.** La rangée K&V ne recopie plus la formule : b y est décrit en prose (rapport de la largeur de bande M
  à la taille d'échantillon T, notation lue sur l'image), et la phrase de la source se clôt par la citation « be used »
  (p. 13).
  - Deux contrôles ajoutés : `kv-be-used` et `kv-recommande-be-used`, le second avec les deux fragments dans l'ordre sur
    la même page. Les deux sont TROUVÉES.
  - Leurs mutants (« be adopted », ordre inversé) sont INTROUVABLES.
- **O-5, traitée par reformulation.** « Les seules racines imprimées par Fisher » devient « Les racines imprimées aux
  pp. 10 (cas fraternel) et 11 (erreur probable de r), vues sur l'image ».
  - J'ai vu ces deux pages sur l'image en phase 2 : PDF pp. 9 et 10, *Metron* pp. 10 et 11.
  - L'affirmation d'absence, qui reposait sur l'[abs] du lecteur du procurement, est retirée.

### 12.7 Contrôles de la phase 1, rejoués sur la série finale

**Citations.**
- `verif_citations.py` sur `citations-dt14-c3.json` (les 129 contrôles de phase 1, plus les deux d'O-4) : 131
  contrôles, 0 échec (`verif-citations-dt14-c3.tsv`).
- `croiser_citations.py` sur le diff net de `ba5ea95` à l'état final (`phase2/net-c3/`) : 182 « », 142 contrôlés par
  script, 40 classés à la main.
- Le compte : 182 = 179 + « Déjà réglé » + « les optionnels retenus » + « be used ». C-1 et C-2 remplacent deux
  citations sans changer le compte.
- Les 40 se répartissent ainsi :
  - 19 occurrences de citations du dépôt. `outils/citations_depot_attribuees.py` les cherche dans le fichier que le
    texte leur attribue (`report.py`, littéraux adjacents joints) : 17 contrôles, 17 TROUVÉES. Le mutant à la forme
    C-2 est ABSENT de `report.py`.
  - 8 chaînes d'absence, à 0 occurrence : contrôles « absent » de la liste et `controles_dedies.py`.
  - 10 libellés : « redistribuable » ×2, « oui » ×2, « price-aggregation » ×2, « === page N === », « N artefacts
    détenus », « 2018 » et « n − 3 » (lu sur l'image). « aucune licence lue », citation de la règle en tête, compte
    parmi les citations du dépôt.
  - 3 citations de pièce hors liste : « COPYRIGHTED MATERIAL » ×2 et « Definition ». Leurs lignes sont inchangées depuis
    la phase 1, relue par la G2.
- La vérification sans attribution (`outils/citations_depot.py`) trouve aussi la forme C-2 du point-virgule dans
  ADR-0028 l.133 et dans l'annexe B l.107. C'est pourquoi le contrôle se fait au fichier attribué.

**En-tête d'INDEX.** `controle_entete.py` du réviseur, avec AVIS `181d2e85…` : règle = AVIS l.25-27 octet pour octet,
quatre jonctions exactes, lignes 15-387 inchangées. VERDICT CONFORME (`phase2/controle-entete-c3.txt`).

**Régime complet** (`copie-verif-c3`, octets versés par `verser_biblio.py` : 59 copiés, puis 0 copié et 59 déjà
présents) :
- S-G5 VERT : 330 fragments contrôlés, corpus 196/196.
- S-G6 VERT : 196 = 196.
- Mutant « rare event » → « rare case » dans l'ajout Dong relocalisé : S-G5 ROUGE,
  `docs/10-mesures-pilotes-design.md:736` (`journaux/gates-c3-mutant-rare-case.txt`).

**Régime INDEX seul**, celui de la CI (`journaux/gates-c3-index-seul.txt`) :
- S-G5 VERT : 330 contrôlés, 280 non contrôlés, comme en phase 1. Le seul non contrôlé d'un fichier touché est
  antérieur au lot, à doc 10 l.507 ; la G2 l'a vu à la l.546 de la série de phase 1, décalé de 39 lignes.
- S-G6 : compte non contrôlable ici, VERT.

**`docs-sha256sums.py`** : « conforme : 35 SHA256SUMS, 299 ligne(s), dont 11 absente(s) admise(s)
(SHOGEN-SIM-SOMMES-1) ; 4 fichier(s) non listé(s), non refusés », sortie 0. Le `sha256sum -c` de `revue-dettes5` donne
4/4 OK.

**`cargo --locked --offline xtask verify`** (copie complète, `journaux/verify-c3.txt`, 05:05:32 à 05:07:41 UTC). Lignes
VERDICT seules :
- S-G1 à S-G4 : VERT, VERT, VERT, VERT.
- S-G5 VERT ; S-G6 VERT ; S-G7a VERT ; S-G8 VERT.
- S-G9 : `VERDICT : ROUGE (1 violation(s))`.
- `cargo fmt --check : VERT` ; no_std du vérificateur : VERT ; `cargo clippy -D warnings : VERT`.
- `=== VERDICT GLOBAL : ROUGE — l'intégration s'arrête (ADR-0013, point 1) ===`, sortie 1.

La violation S-G9, `docs/17-modele-de-menace.md:70`, est antérieure au lot : elle vient de la copie creuse (dossier
exclu). Elle est à la même ligne qu'à `ba5ea95`, alors que la série de phase 1 la portait à :71 : docs/17 n'est plus
décalé.

**Autres contrôles.** Suite `s2-harness` sur `copie-c3` : `Ran 419 tests`, `OK (skipped=2)`, sortie 0.
`lint-model-pinning.sh` : OK (R-1). `journaux-modele.py` : conforme.

### 12.8 Phrases de fermeture, version finale (remplacent le §3)

- **P-01 fermé** : inchangé (§3).
- **P-03 fermé** (Q-E) : Fisher 1921 détenu et lu, *Metron* pp. 14 et 18 ; poids (n − 3) sur l'échelle z. La forme
  1/√(n−3) est celle du manuel (Penn State STAT 509 L7). Ajout daté de doc 10, placé en fin de document, qui vise
  §4.2 (b) (DT14-c, DT14-k) ; `report.py` inchangé.
- **P-05, P-08, P-10, P-11 fermés** : inchangés (§3).
- **P-14 fermé** (Q-C) : « choix de conception » documenté par un ajout daté placé en fin d'ADR-0028, qui vise
  §1 bis.7. P-10 ne fixe aucune durée ; OSF prévoit 48 h d'annulation et 4 ans d'embargo, précédent de pratique, non
  norme (DT14-e).
- **SHOGEN-PEARSON-IF-SOURCE-1 fermé** (Q-C) : Croux et Dehon 2010, éq. (4), versé. La forme de `contenu.py` est
  l'éq. (4) en coordonnées centrées-réduites. Limite : la forme est énoncée au modèle Φρ, non hors de lui (ajout daté en
  fin de docs/11, qui vise §11.1, DT14-f).
- **SHOGEN-DONG-CORPS-1 fermé** : corps de Dong 2010 lu aux pp. 1358-1361 et 1365 (lecteur du procurement), citations
  recontrôlées par script ; PVLDB 2009 versé et lu. La lignée se cite pour l'idée de (2c), non pour sa statistique
  (ajouts datés en fin de doc 10, qui visent §4.2 (b) et §10, DT14-c ; INDEX, note 3 et dette 6, DT14-b et DT14-m).
- **SHOGEN-BIBLIO-PAGES-4-3-1 fermé** par la décision Q-D, avec un résidu écrit : substitut d'API pour CoinGecko
  (`pairs` = 1372) ; page Pyth retirée, citation datée gardée ; copie du jour des publishers ; aucune copie du
  2026-08-05 détenue (ajouts datés en fin de doc 10, qui visent §4.3 et §10, DT14-c).
- **SHOGEN-FETCH-AVANT-PUB-1 fermé** : onze demandes formées et traitées.
  - Huit sont détenues (dix pièces).
  - Une est à l'achat optionnel : Malkhi et Reiter, `WISHLIST.md`.
  - Deux sont introuvables : NUREG/CR-5485, gardé comme « copie non détenue », et « Finkbeiner 2025 », dont
    l'attribution est retirée.
  - Ajout daté en fin de doc 06, qui vise §5 point 5 (DT14-d).
- **SHOGEN-S2BIS-RFC-REGISTRE-1 fermé** : inchangé (§3).
- **SHOGEN-R1-PLUGIN-1 fermé** (Q-C) : statistique et niveau sourcés (Chen et Liu 1997 ; NIST §1.3.5.15). La limite,
  en trois membres, est lue sur la page courante. Le test n'est pas calculé, son niveau n'étant pas tenu (ajout daté en
  fin de docs/11, qui vise §11.1, DT14-f).
- **SHOGEN-CENSURE-INFO-2 fermé** : l'attribution « de type Manski » est sourcée par Horowitz et Manski (approche
  worst-case, bornes sharp). Limite : paramètre de population contre statistique de test [inféré]. La borne de z_bloc
  reste à SHOGEN-CENSURE-ZBLOC-1 (ajout daté en fin de docs/11, DT14-f).
- **SHOGEN-DEP-FENETRES-2, volet (a)** : source détenue (P-05) ; correspondance b = 240/n_s [inféré]. Le calcul de (a)
  reste dans l'item, sous son déclencheur (run maximal ≥ ℓ), non atteint au J28 ; l'item reste ouvert pour ce calcul et
  pour (c) (ajout daté en fin de docs/11, DT14-f ; Q-5).
- **SHOGEN-POOLEE-SOURCE-1 fermé** (Q-B), par non-attribution.
  - Erratum daté placé en fin d'ADR-0028, qui vise D2 pt 4, et erratum daté de la ligne POOLEE en fin d'annexe A.
  - z est une statistique stratifiée sous indépendance (UConn, Prop. 12.3), distincte de la statistique CMH (Agresti
    2013 p. 227 ; PSU STAT 504 §5.3.5).
  - Paquet scellé inchangé (DT14-e, DT14-a, DT14-b, DT14-m).
- **SHOGEN-E1-METHODE-1 (i) fermé** : NIST SP 800-154 (projet) versé et lu ; méthode en quatre étapes ; correspondance
  avec la forme de docs/17 [inféré] (ajout daté en fin de docs/17, qui vise la ligne Forme de la table, DT14-g).
  **(ii) ouvert** : son déclencheur est l'achat de Shostack (P-15).
- **Constat WISHLIST** : le `WISHLIST.md` de l'annexe B l.155 est le fichier de la racine du dépôt. Il reçoit en fin
  de fichier la priorité 6 : P-15, les optionnels et les gestes gratuits (DT14-i, DT14-l).
- **Acte 8 du §1 bis.11 d'ADR-0028**, phrase de la G2 avec P-1 appliquée : « Acte 8 du §1 bis.11 d'ADR-0028 soldé
  (DT14-i et P-1 de la revue G2) : `WISHLIST.md`, priorité 6, porte P-01 et P-03 sans objet (détenus et lus) et les
  optionnels retenus (P-04, P-06, P-07, P-09 de la série P, et ceux du procurement PAROXYSME) ; le reste de
  SHOGEN-ERRATA-ADR0028-1 est inchangé par ce lot. » Dans `diffs-c3/`, P-1 est DT14-l.
- **Retouche B.92** : inchangée (§3).
- **C-3 et K-2**, phrase proposée : « Aucun ajout du lot ne décale une ligne d'un document cité par numéro : les ajouts
  sont placés en fin de document (C-3), et `refs_decalees.py` de la revue G2 relève 0 renvoi décalé sur 220. Les
  renvois par numéro de ligne du paquet scellé se lisent à son commit de scellement, `8b14567`. Ses renvois à doc 10
  (l.379-380, l.519-522, l.555-579) étaient déjà décalés de deux lignes à `ba5ea95`, par des lots antérieurs. La liste
  des renvois non exacts à `ba5ea95` va au brief de DETTES-T15 (SHOGEN-REFS-LIGNE-CONTENU-1). »
- **K-3**, phrase proposée : « En régime CI (INDEX seul), S-G5 ne rougit pas une citation altérée d'une pièce non
  versée. Seul le régime complet la refuse, une fois les octets versés par `verser_biblio.py` (Q-7) : c'est conforme à
  la conception (DEVOPS §1). »
- **K-4** : limite écrite, inchangée. Les attributions hors guillemets, les pages en prose et les valeurs lues sur image
  n'ont pas de contrôle mécanique.

### 12.9 Écarts de la phase 2

- **E-6** : la citation au point-virgule est rétablie en fin de doc 10 par DT14-c et corrigée par DT14-k (§12.4).
- **E-7** : un `grep -n` sur `ANNEXE-D-preenregistrement.md`, fichier permis, cherchait l'emplacement de D.2. Il a
  affiché aussi des lignes de D.1 et de D.3 (attestations et inventaire). Aucune pièce de D.2 n'a été ouverte, et aucune
  valeur n'a été lue.
- **E-8** : un `find -maxdepth 3` sur `copie-c3/`, copie creuse sans dossiers interdits, cherchait un `__pycache__`.
  Il n'en a trouvé aucun.
- **E-9** : deux défauts d'outil, corrigés.
  - La première version de `citations_depot.py` rapportait certaines citations à la ligne précédente (fenêtre de deux
    lignes). Elle a été corrigée et rejouée.
  - `croiser_citations.py` comptait « be used » comme contrôlé parce que c'est une sous-chaîne d'une citation de
    Künsch. Deux contrôles explicites ont été ajoutés.

### 12.10 Actes laissés à l'orchestrateur (remplacent le §8, point 1)

1. Appliquer `diffs-c3/DT14-a.diff` … `DT14-m.diff` dans l'ordre (`git apply`). La série est vérifiée sur `ba5ea95` et
   sur `dda4bbc`. Les diffs de `diffs/` gardent les positions de la phase 1 et ne s'appliquent pas en plus.
2. Le versement des octets est inchangé (§8, point 2).
3. Verser au bloc daté de l'annexe B les phrases du §12.8, au lieu de celles du §3.
4. Joindre au brief de DETTES-T15 `phase2/decalages-anterieurs-ba5ea95.tsv` et `-index.tsv`.

### 12.11 Journal de provenance de la phase 2 (G1)

**[lu]** :
- Pièces de pilotage : §12.1.
- Dépôt à `ba5ea95` :
  - fins de doc 10 (l.685-709), doc 06 (l.120-131), ADR-0028 (l.318-330), docs/11 (l.1040-1071), docs/17 (l.86-113)
    et `WISHLIST.md` (l.244-254) ;
  - doc 10 §4.2 et §4.3 (l.277-375) ; ADR-0028 l.28-36 et l.145-150 ; docs/11 §11.1 (table) ;
  - `report.py` l.385-388 et l.562-569 ; `asn.py` l.18 ; annexe D l.33-47 (noms de D.2) ;
  - `xtask/src/sg5.rs` l.286-330 et `documents.rs` (`normaliser_pour_recherche`).
- Images : Fisher PDF pp. 9-10 (*Metron* pp. 10-11) et K&V PDF p. 13 (`phase2/images/`).

**Commandes et sorties** : celles des §12.2 à §12.7, avec leurs sorties dans `phase2/` et `journaux/` :
`verify-c3.txt`, `gates-c3-index-seul.txt`, `gates-c3-mutant-rare-case.txt`, `docs-sha256sums-c3.txt`,
`suite-s2-harness-c3.txt` et `lints-c3.txt`.

**Chiffres recomptés** :
- 220 renvois et 0 décalé ; 151 et 44 en phase 1 ; 843 lignes en phase 1.
- 311 numéros : 228 exacts, 75 décalés, 6 réécrits ou retirés, 2 hors plage ; 83 non exacts dans 24 documents ; INDEX
  65 et 64.
- 182 = 179 + 3 citations ; 131 contrôles ; 17 attributions ; 19 + 8 + 10 + 3 = 40.
- Tranches : +51, +9, +57, +34, +9, +49, +1, +2, +32, +2, +2, +6, +6.

### 12.12 Livrables de la phase 2

- Diffs : `diffs/DT14-j.diff`, `-k.diff` et `-l.diff` ; `diffs-c3/` (13 diffs).
- Blocs : `blocs-c3/` (textes datés, `HORODATAGES.txt`).
- `outils/` : `ecrire_bloc_c3.sh`, `generer_diffs_c3.py`, `gabarits_kl.py`, `gabarits_m.py`, `comparer_blocs.py`,
  `verifier_serie_c3.sh`, `lignes_conservees.py`, `refs_decalees_premier1.py`, `decalages_anterieurs.py`,
  `decalages_anterieurs_index.py`, `memes_changements.py`, `forme_diffs.py`, `citations_dt14_c3.py`,
  `citations-dt14-c3.json`, `verif-citations-dt14-c3.tsv`, `citations_depot.py` et `citations_depot_attribuees.py`.
- Sorties : `phase2/` et `journaux/*-c3*`.
- Copies : `copie-c3/` (état généré) et `copie-tete/` (`dda4bbc`).
- Le `SHA256SUMS` du dossier est régénéré.
