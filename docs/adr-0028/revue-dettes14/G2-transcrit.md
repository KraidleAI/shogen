# Relecture G2 neuve de DETTES-T14 (passes 1 et 2) (transcrit)

> Transcription par l'orchestrateur le 2026-10-10 06:47:25 UTC du fichier g2/RAPPORT-G2.md ; contrôle FM-1.1 des transcripts du lecteur du procurement, de l'advisor, du générateur et du réviseur G2, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèles résolus : claude-sonnet-5-5 (lecteur), claude-fable-5-1 (advisor), claude-opus-5-5 (générateur, réviseur). Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# RAPPORT G2 — lot DETTES-T14 (BIBLIO), revue neuve à 100 %

Réviseur G2 `shogen-worker`, neuf (je n'ai ni écrit ni relu ce lot). **Gate 0 : `claude-opus-5-5`** (identifiant exact
donné par l'environnement ; écrit en premier acte dans `NOTES.md`, 2026-10-10 03:24:48 UTC). Brief : `BRIEF-G2.md`,
sha256 `5169e7dc35e3cbc185b6de023c2a685277f4515696b20118185e5ac614aa4a9d`. Rapport écrit à partir de 2026-10-10
04:31:01 UTC (`date -u`). Aucune écriture git, aucun réseau, `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée (retirée par
`env -u` à chaque lancement), aucune pièce de D.2 ni dossier interdit ouvert, aucune variable de clé lue.

- Série : DT14-a … DT14-i, **empreinte recalculée** (concaténation dans l'ordre) :
  `fb6e6fe6b055b83827ac718425bd934fe5f093b5b58638d07bf6e9a35163b189`, égale au brief.
- Base : `ba5ea95709e122349448c5e3f024b0ca08d83e91` (copie `git archive` sparse, sans `docs/15-*`, `docs/16-*`,
  `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`,
  `docs/adr-0028/execution/`, `**/*.jsonl`) : `git apply --check` puis `git apply`, 9/9.
- **Tête du moment** (fin de revue) : `dda4bbcc2b0f480eb0c39d7891237e0e3d2b0918` (« Forge, premier passage de
  DETTES-T5 et du lot FUZZ (PR n 11) : annexe B.95, JOURNAL »). Les dix fichiers touchés par la série y sont
  identiques à `ba5ea95` (`git diff --stat` vide) ; la série s'y applique : `git apply --check` puis `git apply`, 9/9.

## 0. Verdict : **ACCEPTE-AVEC-CORRECTIONS** (liste fermée : C-1, C-2)

Deux citations du dépôt, mises entre guillemets, ne sont pas mot pour mot. Tout le reste est conforme (citations de
pièces, pages, en-tête d'INDEX, sommes, dates, gates, forme). Corrections écrites et éprouvées sur la série
(`corrections/C-n.diff`, à appliquer **après** DT14-i, `git apply -p1`) ; texte corrigé écrit à 2026-10-10 04:26:02 UTC
(`date -u`), date reportée dans les blocs redatés (règle du lot : la date est la dernière écriture du texte ; si
l'orchestrateur réécrit encore ces textes, il les redate).

- **C-1 — DT14-a, `biblio/INDEX.md` l.427 (rangée `nogueira-…`)** : « (le « 429 contre 115 » de doc 06 §2 est de Ron
  et al.) » devient « (le « 429 co-déf. vs 115 prédites » de doc 06 §2 est de Ron et al.) » ; doc 06 l.49 (§2) porte
  « 429 co-déf. vs 115 prédites », jamais « 429 contre 115 » (0 occurrence). Bloc redaté, l.390 :
  « *Ajout daté du 2026-10-10 04:26:02 UTC (`date -u`), générateur G1 du lot DETTES-T14 (`claude-opus-5-5`), rangée
  Nogueira corrigée par la revue G2 (C-1) ; ». Diff : `corrections/C-1.diff` (sha256 `ac6d0696…538d8c`, +2 −2).
- **C-2 — DT14-c, `docs/10-mesures-pilotes-design.md` l.309** : « (« transformation de Fisher ; Penn State STAT 509
  L7 ») » devient « (« transformation de Fisher, Penn State STAT 509 L7 §7.8 ») » : c'est la ligne imprimée réelle
  (`s2-harness/shogen_s2/report.py` l.566-567 à `ba5ea95`, littéraux joints : « … SE(artanh r) = 1/√(N−3),
  transformation de Fisher, Penn State STAT 509 L7 §7.8) ») ; la forme au point-virgule est celle que prescrivait
  l'annexe B l.107, pas celle du code. Bloc P-03 redaté, l.301 : « *Ajout daté du 2026-10-10 04:26:02 UTC (`date -u`) ;
  lot DETTES-T14 ; P-03, décision Q-E de ». Ligne corrigée : 103 caractères (≤ 120). Diff : `corrections/C-2.diff`
  (sha256 `f59b4f2a…3118b35`, +2 −2).
- Épreuve (base `ba5ea95` + DT14-a…i + C-1 + C-2 + P-1) : en-tête d'INDEX CONFORME, lignes 15-386 inchangées,
  `docs-sha256sums.py` conforme, `xtask gates` en régime INDEX seul et en régime complet : S-G5 VERT (330 fragments),
  S-G6 VERT (196 = 196 en complet), S-G9 inchangé (`docs/17-modele-de-menace.md:71`) ; les deux citations corrigées
  sont mot pour mot dans leurs fichiers (contrôle par script). Empreinte de C-1 puis C-2 concaténés :
  `3a6082af032d0d9528f8efe3f1b51108097dd571b7aa8d28a784d4cab21e9ec6`.

Hors liste, **proposition facultative P-1** (`corrections/P-1.diff`, sha256 `190b3008…f9b9`, +6 −1) : solde le reste de
l'acte 8 du §1 bis.11 (§4.4 ci-dessous) ; elle n'est pas une correction de défaut.

## 1. Citations (point 1)

**Méthode, indépendante du générateur.** Mes scripts (`outils/`) : `parse_diffs.py` (lignes ajoutées et leur numéro
final) ; `guillemets.py` (tous les « … » des lignes ajoutées, lignes repliées recollées) ; `table_citations.py` (MA
table de rattachement de chaque segment à sa pièce et à sa page, établie en lisant le contexte de la série) ;
`extraire_g2.py` (mon extraction : `pdftotext` 24.02.0 en mode par défaut, pages séparées ; HTML : texte affiché,
commentaires, `<script>` et `<style>` ôtés ; commentaires à part) ; OCR propre `tesseract` (300 dpi) des pages scannées
citées (Künsch PDF 3, 9, 10 ; Fisher PDF 13, 17 ; Agresti PDF 245), en plus des sidecars OCR de `biblio/` ;
`verifier_citations_g2.py` (mot pour mot, blancs repliés, accents graves ôtés côté citation, « … » et « [θ] » en
fragments ordonnés ; tout repli de second rang aurait été signalé : aucun n'a servi) ; `controle_pages.py` (lit la
page que la série déclare après la citation, convention pages imprimées pour Fisher, Künsch, Dong 2010, Agresti, et
partout où « imprimée » est écrit, pages PDF sinon, et vérifie la citation à cette page). Sortie :
`outils/verif-citations-g2.tsv`.

**Résultat** : **179** segments « » ajoutés (le générateur en compte 179 dans sa sortie
`croiser-citations.sortie.txt`, mais 181 dans son rapport §7 et ses NOTES : constat K-1).
- 135 citations de pièces : 133 trouvées à la page attribuée (121 sur texte, 12 sur pièce scannée, à la fois sur le
  sidecar OCR et sur mon OCR) ; les 2 autres (« COPYRIGHTED MATERIAL », Shostack toc et ch. 1) sont un filigrane, lu par
  moi sur l'image (toc p. ix, ch. 1 p. 1) et présent, fragmenté, dans la couche texte (« CO PY RI GH TE D MA TE RI AL »).
- Pages déclarées : 31 contrôlées, 31 conformes ; 50 citations sans page accolée, page portée par le contexte, vérifiées
  à la page de ma table. Autres lectures sur image : Table I de K&V (PDF p. 26, 99 % : 2,377 à b = 0,02 ; 2,459 à
  b = 0,04 ; « right tail critical values », p. 13) ; Shostack toc pp. ix, x, xviii (29, 34, 61, 85, 477) ; Fisher
  *Metron* p. 18 « (n − 3) ».
- Longueur : maximum 25 mots (NIST, « [θ] » compté pour un mot) ; aucune au-delà.
- 13 chaînes d'absence : 0 occurrence chacune dans la portée dite (texte affiché pour le HTML ; aussi 0 dans le HTML brut
  pour les deux chaînes Pyth ; NIST : « at least 5 » et « combine some bins in the tails » présentes seulement dans le
  commentaire daté 2024/04/01).
- 17 citations du dépôt : 15 exactes (dont « forme stratifiée », vérifiée à part : `report.py` l.387 et G1 du lot
  POOLEE, D-10) ; **2 non mot pour mot** (C-1, C-2). 14 libellés (dont « n − 3 », lu sur l'image).
- Attribution (auteur, titre, version, DOI, date) vérifiée sur les pièces ou les preuves du procurement (fiches CSRC,
  Cambridge Core `citation_doi`, Crossref H&M : 77-84, 95(449) ; pages abs arXiv : CC BY-NC-SA 4.0, CC BY 4.0 ×2,
  `nonexclusive-distrib/1.0` ; API OSF : 2dxu5 → licence `563c1cf88c5e4a3877f9e96c` = « CC0 1.0 Universal » ; fiches
  Wiley : 54.00 / 68.00 et 108.95 / 87.00 USD, ISBN). `pdfinfo` : métadonnées NIST SP (2016-03-14) et UConn (2020-09-02).
- Formules : aucune recopiée hors citation courte, hors « b = M/T » à la rangée K&V (notation de trois symboles qui
  achève la citation coupée ; observation O-4).

**Les 38 « non-citations » du générateur** (sa sortie `croiser-citations.sortie.txt`), une à une : 10 libellés
(« redistribuable » ×2, « aucune licence lue », « === page N === », « oui » ×2, « price-aggregation » ×2, « N artefacts
détenus », « 2018 ») ; 8 chaînes d'absence, 0 occurrence vérifiée (« 2^32 », « hybrid between a mean and a median »,
« already publishing data to Pyth Network », « open problem », « future work », « common source », « same source »,
« single source ») ; 14 citations du dépôt exactes (« pas de sidecars encore », « entier de 0 à 2^32 exclu »,
« AV 2011 » ×2, « annexe B l.21 », « règle de `WISHLIST.md` », « Finkbeiner 2025 » ×2, « 429 co-déf. vs 115
prédites », « (type Mantel-Haenszel) », « forme stratifiée », « type Mantel-Haenszel », « La forme MH », « de type
Manski ») ; **4 citations de pièces**, vraies mais classées à tort comme non-citations (« COPYRIGHTED MATERIAL » ×2,
« Definition » de la page NIST, « n − 3 » lu sur l'image de Fisher) ; **2 fausses** : « 429 contre 115 » (C-1) et
« transformation de Fisher ; Penn State STAT 509 L7 » (C-2), absentes de la source qu'elles nomment (le générateur dit
« 12/12 » citations françaises trouvées : ces deux-là n'en étaient pas).

## 2. Textes validés et dates (point 2)

- Réécritures (mon parseur) : DT14-a −9 (l.3, ligne du compte exigée par S-G6 ; l.6-13, rejointes deux à deux) ;
  DT14-h −2 (l.7 d'`ADJUDICATION.md`, demandée par l'annexe B.92 ; l.1 du `SHA256SUMS`, qui suit). Tout le reste :
  ajouts datés ou errata datés, placés après le texte qu'ils disent inchangé (vérifié en contexte : doc 10 §4.2 ×2,
  §4.3 après les cinq points, §10 après la table ; doc 06 §5 pt 5 ; ADR D2 pt 4 et §1 bis.7 ; annexe A en fin ;
  docs/11 §11.1 après « Restes » ; docs/17 après la ligne « Forme de la table » ; `WISHLIST.md` avant « Déjà réglé »).
- Dates (`controle_dates.py`) : 14 mentions datées, chacune dans un bloc de `blocs/` ; chaque bloc porte la date de sa
  **dernière** écriture au journal `blocs/HORODATAGES.txt` (14/14) et se retrouve tel quel dans la série ; mtimes des
  blocs égaux à ces dates (aucune retouche après datation) ; diffs générés à 03:18:57.66, après la dernière écriture
  (03:18:57) ; NOTES du générateur concordantes (03:10:24 : procédé ; 03:22:34 : retouches de fin redatées, docs/11 et
  annexe A à 03:18:47, section d'INDEX à 03:18:57).

## 3. INDEX (point 3, Q-2)

- **Règle** : INDEX l.12-14 = AVIS l.25-27, **octet pour octet** (`controle_entete.py`).
- **Lignes rejointes** : base l.6+7, 8+9, 10+11, 12+13 = copie l.6, 7, 8, 9, fin de ligne remplacée par **un** espace,
  égalité exacte ; base l.14 = copie l.10 ; titre daté l.11 ; l.15 et suivantes de la base **toutes inchangées au même
  numéro** (15-386).
- **Lignes citées par numéro** (`refs_index.py`, 117 fichiers nommés par l'annexe B, la passation, `CLAUDE.md`,
  `JOURNAL.md` ; paquet scellé : jetons de référence seuls, écart E-4) : 36 renvois vers l'INDEX ; tous visent des
  lignes ≥ 15 (paquet : l.328, l.336, l.337, l.338 ×2 ; docs/17 : :18, :19, :325, :327 ; doc 10, docs/08, G1, G2,
  CP1, ETAT-REGISTRE, RECHERCHE-G4…), sauf INDEX l.3 (`docs/G2-lot-CORR.md` l.355, journal de lecture de la ligne du
  compte, que S-G6 fait réécrire à chaque versement) et des plages de lecture l.1-20 et l.1-239 (journaux) : **aucune
  ligne d'INDEX citée n'est décalée**. Mutant M04 (une ligne de plus dans l'en-tête) : 38 numéros cités changent de
  contenu, tué.
- **Compte 196** : `verser_biblio.py` (sha256 `90f7db38…1436`), lancé sur une copie du `biblio/` du poste (161
  artefacts, 31 sidecars) : « 35 rangées ; 59 fichier(s) copiés » ; seconde passe : « 0 copiés ; 59 déjà présents à
  l'identique » ; résultat : 196 artefacts, 55 sidecars ; la RFC 3161 du 2026-10-09 n'est pas copiée (doublon).
  S-G6 complet : « compte déclaré 196, compte réel 196 ».
- **Entrées** (`controle_entrees.py`) : 35/35 sha256 et tailles recalculés sur les octets ; minute de la date = mtime
  UTC de la pièce ; URL = tableau §4 du procurement (34) ; GitHub : `date-fetch.txt` 2026-10-10T02:35:23Z ; pages
  déclarées = `pdfinfo`. Sidecars (`controle_sidecars.py`) : 24/24 égaux à l'octet à mon `pdftotext` page par page ;
  `SIDECARS.sha256` conforme. **Colonne « redistribuable »** (`controle_redistribuable.py`) : 8 « oui » (CC0 ×2 dont
  « CCO » d'OSF, notice RFC 3628, domaine public NIST SP, CC BY-NC PSU, CC BY ×2, CC BY-NC-SA), 27 « non » :
  conforme à ma lecture des licences.

## 4. Fermetures (point 4)

### 4.1 Phrases du rapport §3, contre la série
Vraies sur la série : P-01 (et mon OCR des pp. 1224, 1227, 1231, 1234 confirme la lisibilité et les contenus annoncés),
P-05, P-08, P-10, P-11, P-14, PEARSON-IF-SOURCE-1, BIBLIO-PAGES-4-3-1, FETCH-AVANT-PUB-1 (11 = 15 noms − 4 détenus ;
8 détenues / 10 pièces, 1 achat optionnel, 2 introuvables), S2BIS-RFC-REGISTRE-1 (`asn.py` l.18 ; `test_asn.py` l.4,
l.5), R1-PLUGIN-1, CENSURE-INFO-2 (SHOGEN-CENSURE-ZBLOC-1 existe, annexe B l.797), POOLEE-SOURCE-1 (paquet l.56 et
l.59, lus : « (type Mantel-Haenszel) », §4 = l.54-60), E1-METHODE-1 (i) et (ii), constat WISHLIST (8 commits à
`ba5ea95`, règle l.31-33 ; extrait du procurement l.21 = annexe l.155), retouche B.92 (§5). Précisions de forme
proposées pour le bloc daté (observations, non bloquantes) :
- **O-1, P-03** : le texte de doc 10 est un « Ajout daté », non un « erratum » ; écrire « ajout daté de doc 10 §4.2 b »
  (la note 5 de DT14-b dit « erratum daté » : même remarque).
- **O-2, DONG-CORPS-1** : « corps de Dong 2010 lu aux pp. 1358-1361 et 1365 (lecteur du procurement), citations
  recontrôlées par script » au lieu de « corps de Dong 2010 lu ».
- **O-3, DEP-FENETRES-2 (a)** : « … le calcul de (a) reste dans l'item, sous son déclencheur ; l'item reste ouvert pour
  ce calcul et pour (c) » (Q-5 adoptée le dit ; la phrase ne le dit qu'implicitement).

### 4.2 Q-3, Q-4, Q-5
- **Q-3** : vérifié sur la page : texte affiché « at least 5 » 0, « combine some bins in the tails » 0, « independent »
  0 ; commentaire « 2024/04/01: Following section replaced with material » ; « not from the individual observations »
  présent ; DT14-f écrit les trois membres en conséquence ([inféré] au membre 1, à raison).
- **Q-4, dérivation relue** : IF(Cov) = (x − μx)(y − μy) − Cov ; IF(σ²) = (x − μ)² − σ² ; ρ = Cov·(σx²)^(−1/2)(σy²)^(−1/2),
  donc IF(ρ) = IF(Cov)/(σxσy) − (ρ/2)(IF(σx²)/σx² + IF(σy²)/σy²) = x̃ỹ − ρ − (ρ/2)(x̃² − 1 + ỹ² − 1) = x̃ỹ −
  (ρ/2)(x̃² + ỹ²), pour toute loi à variances finies : **exacte**. `contenu.py` l.5 et l.31 en sont la forme en
  coordonnées centrées (x̃_t ỹ_t/√(sxx syy) − (ρ̂/2)(x̃_t²/sxx + ỹ_t²/syy)). C&D §3 p. 6 : invariance linéaire,
  « without loss of generality » : vérifié.
- **Q-5** : Table I (99 %) croissante en b, 2,377 à 0,02 ; « right tail » ; z_bloc au noyau de Bartlett (ADR l.95),
  ℓ = 240, runs maximaux 6 et 2 (docs/11 l.248, §5.4 l.475) : l'observation [inférée] tient.

### 4.3 Items restants
P-15 et E1-METHODE-1 (ii) : déclencheur écrit (achat de l'e-book de Shostack, 54,00 USD, acte de l'investisseur) :
conforme au brief.

### 4.4 Acte 8 du §1 bis.11 d'ADR-0028 (SHOGEN-ERRATA-ADR0028-1, annexe B l.727-730)
**DT14-i ne le solde pas entièrement.** Texte de l'acte (ADR l.170) : « WISHLIST.md : P-01, P-03 et les optionnels
retenus (registre des non-détenus, où S-G5 résout les titres) ». DT14-i solde la part P-01 et P-03 (« Sans objet »,
Künsch 1989 et Fisher 1921 détenus et lus). **Reste** « les optionnels retenus » : à la date de l'acte, les demandes
marquées « optionnel » de la série P du même amendement [inféré] : P-04 (Carlstein 1986), P-06 (Newey et West 1987),
P-07 (Hall, Horowitz et Jing 1995), P-09 (Lahiri 2003), annexe B l.118, l.120, l.121, l.123 ; 0 occurrence à
`WISHLIST.md` et à l'INDEX, à la base comme après la série (les optionnels que DT14-i inscrit sont ceux du procurement
PAROXYSME).
- Phrase exacte, sans P-1 : « Acte 8 du §1 bis.11 d'ADR-0028 : la part P-01 et P-03 est soldée par DT14-i
  (`WISHLIST.md`, priorité 6 : sans objet, Künsch 1989 et Fisher 1921 détenus et lus) ; reste « les optionnels
  retenus » : P-04, P-06, P-07 et P-09 (annexe B l.118, l.120, l.121, l.123), à inscrire à `WISHLIST.md` ou à déclarer
  non retenus. »
- Phrase exacte, avec P-1 appliquée : « Acte 8 du §1 bis.11 d'ADR-0028 soldé (DT14-i et P-1 de la revue G2) :
  `WISHLIST.md`, priorité 6, porte P-01 et P-03 sans objet (détenus et lus) et les optionnels retenus (P-04, P-06, P-07,
  P-09 de la série P, et ceux du procurement PAROXYSME) ; le reste de SHOGEN-ERRATA-ADR0028-1 est inchangé par ce
  lot. »

## 5. Gates (point 5)

`cargo --locked --offline xtask verify` (copie série, `biblio/` = INDEX seul ; `journaux/verify-serie.txt`,
03:49:54-03:50:09 UTC), **lignes VERDICT seules** :
- S-G1 `VERDICT : VERT (0 violation(s))` ; S-G2 VERT ; S-G3 VERT ; S-G4 VERT ; S-G5 VERT ; S-G6 VERT ; S-G7a VERT ;
  S-G8 VERT ; S-G9 `VERDICT : ROUGE (1 violation(s))` ; `cargo fmt --check : VERT` ; `no_std du vérificateur … :
  VERT` ; `cargo clippy -D warnings : VERT` ; `=== VERDICT GLOBAL : ROUGE — l'intégration s'arrête (ADR-0013, point
  1) ===` (sortie 1).
- Violation S-G9 : `docs/17-modele-de-menace.md:71` (copie creuse ; à `ba5ea95` seul, la même à `:70`).

S-G5 dans les deux régimes (`xtask gates`, binaire du même build) :
- **INDEX seul** (CI) : VERT ; 330 fragments contrôlés, 280 non contrôlés (base : 324 et 281 ; seul changement de
  liste : « overlapping blocks should be used when one can afford the computations » de `LECTURES-PARTIE-3.md` devient
  contrôlé par la note 4) ; parmi les fragments des fichiers touchés, un seul non contrôlé, antérieur au lot (doc 10
  l.546). S-G6 : « compte réel non contrôlable ici », VERT.
- **Complet** (octets copiés par `verser_biblio.py`) : S-G5 VERT, 330 contrôlés, corpus 196/196, aucun non contrôlé ;
  S-G6 VERT, 196 = 196 ; S-G9 la même violation seule. Base complète (161) : S-G5 324, S-G6 161 = 161, S-G9 `:70`.

`python3 -B enforcement/docs-sha256sums.py .` : « docs-sha256sums : conforme : 35 SHA256SUMS, 299 ligne(s), dont 11
absente(s) admise(s) (SHOGEN-SIM-SOMMES-1) ; 4 fichier(s) non listé(s), non refusés » (sortie 0) ; `sha256sum -c` du
dossier `revue-dettes5` : 4/4 OK ; l.1 = sha256 de la nouvelle `ADJUDICATION.md` (`38ca49c4…438d`).

Lignes `gates.yml` des jobs dont un fichier est touché :
- `g5-dette`, l.78 (`git grep -nE '(\b(TODO|FIXME):|…)' -- ':!biblio/' …`) : même motif sur les dix fichiers touchés,
  base et série : 0.
- `g1-model-pinning` : l.167 (`docs-sha256sums.py`, ci-dessus : conforme) ; l.157 (`lint-model-pinning.sh .`) :
  « OK (R-1) : 7 fichier(s) ; liste blanche : … » ; l.162 (`journaux-modele.py .`) : « conforme (52 journaux exemptés
  par nom et sha256) ».
- `g3-secrets`, l.204 (`gate-secrets.sh --tree`) : l'outil exige un arbre git ; ses motifs VENDOR et GENERIC
  (`gate-secrets.sh` l.62-63, lus du fichier, éprouvés sur deux chaînes formées : 1 et 1) appliqués aux dix fichiers
  touchés, base et série : 0.
- `squelette.yml` l.118-119 (`cargo run --locked --package xtask -- verify`) : le `verify` ci-dessus.
- Suite `s2-harness` (aucun code touché ; contrôle de non-régression) : `Ran 419 tests`, `OK (skipped=2)`, sortie 0.

## 6. Forme (point 6)

R-25 : +51 −9, +9, +48, +29, +5, +42, +1, +2 −2, +31 (≤ 200 ; égal au rapport). R-13 : 0 TODO/FIXME/XXX ajouté.
Aucun octet de pièce au dépôt : seuls des fichiers texte suivis, citations ≤ 25 mots, aucun extrait de sidecar.
Lignes ≤ 120 là où le fichier le tient : doc 10 (max 105), doc 06 (77), docs/11 (118), `WISHLIST.md` (94 ; fichier ≤
103) ; INDEX, ADR-0028, annexe A, docs/17, `ADJUDICATION.md` portent déjà des lignes longues (170, 166, 139, 63, 32
lignes > 120 à la base). Rendu markdown : titre ATX, liste et table de l'en-tête séparés comme il faut.

## 7. Mutants (point 7)

`outils/mutants.py` : une chaîne remplacée dans une copie des diffs (présence unique contrôlée), série mutée appliquée
sur une archive neuve de `ba5ea95`, contrôles nommés ; « tué » = résultat différent de celui de la série d'origine
(référence recalculée à chaque passe). Passe 1 (M01-M16) : `journaux/mutants-passe1.txt` ; passe 2 (M15-M19, tous les
contrôles) : `journaux/mutants-passe2.txt`, `outils/mutants-sortie.tsv`.

| id | mutation | tué par |
|---|---|---|
| M01 | INDEX, C&D : « unbounded » → « bounded » | `verifier_citations_g2` |
| M02 | INDEX, Nosek : « sealed until … » p. 10 → p. 11 | `controle_pages` |
| M03 | note 4, Künsch : p. 1225 → p. 1224 (imprimée) | `controle_pages` |
| M04 | une ligne de plus dans l'en-tête d'INDEX | `controle_entete`, `refs_index` |
| M05 | sha256 de RFC 5737, dernier chiffre | `controle_entrees`, `verser_biblio.py` (REFUS) |
| M06 | date de docs/11 : 03:18:47 → 03:18:46 | `controle_dates` |
| M07 | taille de RFC 5737 : 7036 → 7037 | `controle_entrees` |
| M08 | compte 196 → 195 | S-G6 en régime complet (INDEX seul : non vu) |
| M09 | B.92 : « new label » → « next label », somme suivie | S-G5 en régime complet, `ADJUDICATION.md:7` (INDEX seul : non vu) |
| M10 | `SHA256SUMS` l.1, dernier chiffre | `docs-sha256sums.py` (refus l.1) |
| M11 | « redistribuable » de C&D : non → oui | `controle_redistribuable` |
| M12 | règle : « conditions lues » → « conditions vues » | `controle_entete` |
| M13 | citation K&V portée à 27 mots (mots exacts de la source) | `verifier_citations_g2` (> 25 mots) |
| M14 | ADR : « (type Mantel-Haenszel) » → « (type Cochran-Mantel-Haenszel) » | `verifier_citations_g2` (citation du dépôt) |
| M15 | docs/11 : « Croux et Dehon 2010 » → 2011 (hors citation) | intégrité bloc/série seule (`controle_dates`) |
| M16 | doc 10 : « pp. 14 et 18 » → « pp. 14 et 19 » (prose) | intégrité bloc/série seule |
| M17 | docs/11 : Table I 2,377 → 2,337 | intégrité bloc/série seule |
| M18 | doc 10, Dong 2009 : « rare event » → « rare case » | `verifier_citations_g2` ; S-G5 complet (`docs/10-mesures-pilotes-design.md:342`) |
| M19 | note 6, Agresti (scan) : « independent » → « dependent » | `verifier_citations_g2` (sidecar OCR et mon OCR) |

19 mutants, 16 tués par un contrôle de fond. M15, M16, M17 ne sont vus que parce que le texte de la série ne serait
plus celui du bloc daté du générateur : une erreur écrite dès le bloc ne serait vue par aucun contrôle mécanique
(constat K-4 ; valeurs vraies vérifiées à la main : 2010, pp. 14 et 18, 2,377).

## 8. Constats

- **K-1** (G1 du générateur) : rapport §7 et NOTES : « 181 guillemets ajoutés, 143 contrôlés par script » ; sa sortie
  `croiser-citations.sortie.txt` dit 179 et 141 ; mon décompte : 179. Chiffre du rapport à rectifier au versement de son
  journal.
- **K-2** (renvois par numéro de ligne vers les autres fichiers touchés ; classe SHOGEN-REFS-LIGNE-CONTENU-1, formée,
  DETTES-T15) : `outils/refs_decalees.py` (jetons seuls) relève, dans les 117 fichiers nommés, 151 renvois décalés dans
  44 documents (ADR-0028 55, docs/17 48, doc 10 47, docs/11 1), surtout des journaux G1/G2 et avis ; dont, dans le
  **paquet scellé**, « ADR-0028-decisions-sortie-S2.md` l.29-42 » (paquet l.3) et « doc 17 l.108 » (paquet l.205),
  exacts à `ba5ea95` (= `8b14567` sur ces lignes) et décalés par DT14-e (insertion à l.36) et DT14-g (insertion à l.8) ;
  ses renvois à doc 10 (l.379-380, l.519-522, l.555-579) étaient déjà décalés à `ba5ea95` par des lots antérieurs ; le
  paquet épingle ses références « à `8b14567` ». Q-2 a protégé l'INDEX seul. Recommandation : le bloc daté dit que les
  renvois par numéro du paquet se lisent à son commit de scellement, et la liste va au brief de DETTES-T15.
- **K-3** : en régime INDEX seul (CI), S-G5 ne rougit pas une citation de la série altérée (M09, M18 : fragments « non
  contrôlés ») ; seul le régime complet (octets versés, Q-7) la refuse : conforme à la conception (DEVOPS §1), à dire
  au bloc daté avec Q-7.
- **K-4** : attributions hors guillemets, pages en prose et valeurs lues sur image n'ont aucun contrôle mécanique (M15 à
  M17) ; je les ai relues sur pièce.
- **K-5** : acte 8 (§4.4) : reste « les optionnels retenus ».

Observations sans suite obligée : O-1 à O-3 (§4.1) ; **O-4** : « b = M/T » hors guillemets à la rangée K&V ; **O-5** :
« Les seules racines imprimées par Fisher (p. 10 ; p. 11) » (doc 10) repose sur l'[abs] du lecteur du procurement
(OCR des 31 pages, pages vues sur image) ; je n'ai relu sur image que les pp. 13 et 17 du PDF.

## 9. Écarts (E-n)

- **E-1** : un `ls` non récursif de `docs/` et de `docs/adr-0028/` **de ma copie** (noms seuls, dossiers interdits déjà
  absents), puis plus aucune liste de `docs/`.
- **E-2** : un `grep` sur `.github/workflows/*.yml` de ma copie (motif de nom sur sept fichiers de workflow).
- **E-3** : enregistrement de rôle G2 (`oracle_record.py --role G2`, SHOGEN-G2-ENREG-ROLE-1) **non fait** : le brief ne
  le demande pas, et l'outil extrait par `git archive` l'arbre entier du commit (dossiers interdits et `*.jsonl`
  compris), contraire aux interdits du brief. À adjuger ; si l'orchestrateur le veut, il faut une forme sparse de
  l'outil.
- **E-4** : paquet scellé : outre les lignes citées par la série (l.56, l.59, lues), j'ai extrait par script des
  **jetons** de référence (`INDEX.md` l.N, renvois à ADR, doc 10, doc 17, « à `8b14567` ») et les numéros de titres
  (`## N`), sans afficher de ligne.
- **E-5** : passe 1 des mutants interrompue à M17 (chaîne présente deux fois) : M17 refait en passe 2, non compté en
  passe 1. Ma première commande OCR a dépassé 120 s et a fini en arrière-plan (sans effet).
- **E-6** : la sortie de S-G9 imprime le chemin cible de la référence de docs/17 l.71 (un fichier de `docs/rapports/`) :
  jamais ouvert ; S-G5 imprime des fragments d'autres documents (aucun d'un dossier interdit, absents de la copie).
- Octets privés : `biblio/` du poste copié dans `complet/` et `base-complet/` de mon dossier (régime complet), liés en
  dur dans les arbres de mutants puis déliés ; copies supprimées en fin de revue.

## 10. Journal de provenance (G1 de cette revue)

**Pilotage [lu]**, entiers : `BRIEF-G2.md` (`5169e7dc…4a9d`) ; `ADJUDICATION.md` du lot (`f3e79c3c…bee2d`) ;
`RAPPORT-GENERATEUR.md` (`62991bd3…a0d4`) ; `BRIEF-DETTES-T14.md` (`e728ff3c…0530`) ; `ITEMS-ANNEXE-B.md` du lot
(`b7e7f279…7dde`) ; `NOTES.md` du générateur (`37728dea…ba13`) ; procurement `avis/ADJUDICATION.md` (`6a49420c…480f`),
`avis/AVIS.md` (`181d2e85…397a`), `RAPPORT-PROCUREMENT.md` (`860bfe16…9397`, 191 l.) ; outils du générateur lus :
`verser_biblio.py`, `extraire.sh`, `ecrire_bloc.sh`, `croiser_citations.py` et sa sortie, `generer_diffs.py` (l.1-60),
`blocs/HORODATAGES.txt`, `tmp/noms-annexeB.txt`, `SIDECARS.sha256`.

**Pièces [lu]** (par script sur mon extraction ; images vues : Shostack toc pp. ix, x, xviii et ch. 1 p. 1, Fisher
*Metron* pp. 14 et 18 ; OCR propre : Künsch PDF 3, 8, 9, 10, 11, 15, 18, Fisher PDF 13 et 17, Agresti PDF 245) : les
35 pièces du lot ; détenues : `fisher1921-…`, `kunsch1989-…`, `agresti-2013-…` (sidecars OCR et mon OCR),
`dong-2010-…` (`pdftotext`), `ietf-rfc3161-…-2026-10-04.txt` (sha256 = copie du 2026-10-09) ; preuves du procurement
(`SHA256SUMS-preuves` rejoué : OK) : fiche CSRC, pages abs arXiv ×4, API OSF ×2, fiches Wiley ×2, page Cambridge Core,
Crossref H&M.

**Dépôt à `ba5ea95` [lu]**, lectures ciblées de fichiers nommés : `biblio/INDEX.md` (en-tête, section du lot, lignes
citées) ; `WISHLIST.md` (titres, l.27-35, l.236-280) ; doc 10 (l.280-348, 358-405, 722-749) ; doc 06 (titres, l.49,
l.99-131) ; docs/11 (l.248, 475-481, 986, 1010-1089) ; docs/17 (l.1-9, titres, en-têtes de table) ; ADR-0028 (l.29-37,
l.95, l.146-156, l.167-185) ; annexe A (l.33, l.144-150) ; annexe B (l.107-128, l.155, l.183-184, l.223, l.720-732,
l.797, l.1545-1572 ; à la tête : ajouts après l.1570) ; annexe D (l.30-50, D.2) ; paquet scellé (l.56, l.59 ; E-4) ;
`scripts/post-s2/contenu.py` l.1-42 ; `asn.py` l.18 ; `test_asn.py` l.1-6 ; `report.py` l.387, l.560-570 ; G1 du lot
POOLEE (D-10, par recherche sur le fichier) ; `CP2-S2.md` l.30-40 ; `gates.yml` (jobs) ; `squelette.yml` l.115-119 ;
`xtask/src/main.rs`, `lib.rs` (portions), `sg6.rs` (motif) ; `gate-secrets.sh` l.60-73 ; `oracle_record.py` (en-tête) ;
`revue-dettes5/ADJUDICATION.md` l.7 et `SHA256SUMS`. Recherches par motif sur fichiers nommés seulement (sauf E-1, E-2).

**[abs]** : Shostack au-delà des extraits ; versions éditeur ; Fisher hors pp. 13-17 du PDF (O-5) ; Dong 2010 hors
pp. 1358-1361 et 1365 ; NUREG/CR-5485 ; « Finkbeiner 2025 » ; Trust Legal Provisions de l'IETF.
**[2nd]** : identités de la série P (annexe B, « [2nd] sauf mention ») reprises en P-1.

**Commandes et sorties (relevées)** : `cat DT14-a..i | sha256sum` → `fb6e6fe6…b189` ; `git apply --check`/`apply` 9/9
(base et tête `dda4bbc`) ; `parse_diffs.py` → +51 −9 … +31 ; `controle_entete.py` → CONFORME ; `verifier_citations_g2.py`
→ P 133 OK + 2 sur image, A 13/13, D 14 OK + 1 ÉCHEC + 2 à part ; `controle_pages.py` → 31/31 ; `controle_dates.py` →
14/14 ; `controle_entrees.py` → 35/35 ; `controle_sidecars.py` → 24/24 ; `controle_redistribuable.py` → CONFORME ;
`refs_index.py` → 36 renvois, [3] seul ; `refs_decalees.py` → 151 / 44 ; `verser_biblio.py` → 59 copiés puis 0/59 ;
`xtask verify` et `gates` → §5 ; `docs-sha256sums.py` → conforme, sortie 0 ; suite `s2-harness` → 419, OK (2 sautés) ;
`mutants.py` → §7. Journaux : `journaux/`.

**Chiffres recomptés** : 179 segments ; 135 / 13 / 17 / 14 ; 35 entrées, 8 « oui » ; 161 + 35 = 196 ; sidecars 31 + 24
= 55 ; fragments S-G5 324 → 330, non contrôlés 281 → 280 ; tranches +51, +9, +48, +29, +5, +42, +1, +2, +31 ; 19 mutants,
16 tués au fond.

## 11. Livrables

`RAPPORT-G2.md`, `NOTES.md`, `SHA256SUMS` (de ce dossier) ; `corrections/C-1.diff`, `C-2.diff`, `P-1.diff` ;
`outils/` (scripts ci-dessus, `verif-citations-g2.tsv`, `mutants-sortie.tsv`, `refs-decalees.sortie.txt`,
`secrets_touches.sh`) ; `journaux/` (verify, gates des quatre régimes, corrections, docs-sha256sums, lint, suite,
mutants) ; `tmp/` : extractions et OCR (texte), `guillemets.json`, `diffs.json`. Copies du dépôt et cible cargo
supprimées.

## 12. Ajout daté du 2026-10-10 05:31:41 UTC (`date -u`) : passe 2 sur la série `diffs-c3/` (C-1, C-2, P-1, C-3, K-1)

Même réviseur, Gate 0 inchangé (`claude-opus-5-5`). Pièces : message de l'orchestrateur (passe 2) ; `ADJUDICATION.md`
du lot (`b8c2a46b…dff1`, ajouts de 04:37:02 et de 05:17:57) ; `RAPPORT-GENERATEUR.md` §12 (`76fd3398…235a`, ajout de
05:15:50) ; `blocs-c3/` et son `HORODATAGES.txt`. Série : `diffs-c3/DT14-a` à `DT14-m`, **empreinte recalculée**
`23bfdaf17372d0d0b304ca54b88e754945bb316641c88111213934b01fe9087d`, égale au message. Interdits tenus, aucune écriture
git, aucun réseau, `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée, un processus lourd à la fois.

### 12.0 Verdict de la passe 2 : **ACCEPTE** (aucune correction nouvelle)

C-1, C-2 et P-1 sont dans la série à l'identique, C-3 est tenue, K-1 est corrigé. Rien à corriger dans `diffs-c3/`.
La série s'applique en entier et dans l'ordre (E-6 : DT14-c remet en fin de doc 10 le texte de phase 1, citation au
point-virgule comprise, que DT14-k corrige ; appliquer DT14-c sans DT14-k rétablirait la citation fausse).

### 12.1 C-3 tenue (point 1)
- `outils/refs_decalees.py` (`c15a0ace…7a56`, inchangé depuis la passe 1), base `ba5ea95`, état final : **220 renvois
  relevés, 0 décalé, 0 document** (`p2/refs-decalees-c3.txt`).
- Ma preuve sans motif, `outils/lignes_fixes.py` (`0406ba52…60b2`) : pour chacun des dix fichiers, toute ligne de la
  base garde son numéro et son texte, hors réécritures déclarées (INDEX l.3 et l.6-14, `ADJUDICATION.md` l.7,
  `SHA256SUMS` l.1) ; tout le reste est ajouté après la dernière ligne de la base (INDEX +51 dès l.387 ; doc 10 +57 dès
  l.710 ; doc 06 +34 dès l.132 ; ADR-0028 +7 dès l.331 ; annexe A +2 dès l.149 ; docs/11 +49 dès l.1072 ; docs/17 +1 à
  l.114 ; `WISHLIST.md` +37 dès l.255) : **CONFORME**. Donc **0 ligne citée changée**, hors la l.3 de l'INDEX (ligne du
  compte, journal de lecture de `G2-lot-CORR.md` l.355) et la l.7 d'`ADJUDICATION.md` (changement voulu par B.92).
- `refs_index.py` : 36 renvois vers l'INDEX, seule la l.3 diffère, comme en passe 1.
- Paquet scellé (jetons seuls) : ADR-0028 l.29-42 et doc 17 l.108 sont, dans l'état final, égaux octet pour octet à
  `8b14567` ; ses renvois à doc 10 (l.379-380, l.519-522, l.555, l.579) visent à `ba5ea95` et dans l'état final le
  texte de `8b14567` décalé de +2 (antérieur au lot ; liste du générateur pour DETTES-T15).
- Échec montré (`p2/outils/mutants_c3.py`, `journaux/mutants-c3.txt`) : série de la passe 1 : `lignes_fixes` NON
  CONFORME, 151 renvois décalés dans 44 documents ; DT14-g de la passe 1 remis dans la série c3 : NON CONFORME, 48
  renvois décalés dans 16 documents.

### 12.2 Textes en fin de document (point 2)
Lus en entier dans l'état final. Chaque document reçoit « ## Ajouts datés en fin de document », une phrase datée de
placement, puis un ajout par cible ; les cibles sont exactes :
- doc 10 : **Vise §4.2 (b)** (P-03 ; « ### 4.2 (b) L'axe corrélation de contenu », où sont l'erratum du 2026-09-30 et
  l'ajout du 2026-10-02) ; **Vise §4.2 (b), précédent académique de (2c)** (paragraphe de base l.317, dans §4.2) ;
  **Vise §4.3 (c), points 2 à 4** (« ### 4.3 (c) L'axe méthode commune », cinq points) ; **Vise §10, dettes 1, 4 et 7**.
- doc 06 : **Vise §5, point 5** (« Dettes de fetch ouvertes »). ADR-0028 : **Vise D2, point 4 (Strate poolée en forme
  stratifiée)** ; **Vise §1 bis.7, alinéa Ouverture de l'exécution** (le délai de 24 h y est ; il est aussi au premier
  alinéa, et le texte dit les deux alinéas inchangés : exact). docs/11 : **Vise §11.1, paragraphe Restes**. docs/17 :
  puce en fin de document, qui « vise la ligne **Forme de la table** de l'en-tête » (l.7). Annexe A : erratum resté en
  fin, renvoi à « l'erratum daté d'ADR-0028 qui vise D2 pt 4 (placé en fin de l'ADR, même lot) ». `WISHLIST.md` :
  priorité 6 après « Déjà réglé », avec sa phrase de placement.
- Disent toujours vrai : 177 des 182 « » sont, à l'octet et dans le même ordre, ceux de la passe 1 (report de ma table) ;
  les renvois relatifs sont justes (« ajout ci-dessus visant… », « la table qui précède », « de cette section ») ; O-2,
  O-3 et la ligne « table de §11.1, ligne SHOGEN-R1-PLUGIN-1 (b) » sont vrais ; O-5 : *Metron* p. 10 (PDF 9) imprime
  1/√(n − 3/2), cas du type fraternel (p. 14 : « those for correlations of the fraternal type »), et p. 11 (PDF 10)
  0,67449(1 − r²)/√(n − 1) : **vu sur l'image**. « cité ailleurs par numéro de ligne » : vrai pour les six documents
  (renvois relevés : doc 10 40, doc 06 4, ADR-0028 50, docs/11 29, docs/17 49, `WISHLIST.md` 1).

### 12.3 DT14-j, k, l, m (point 3)
- **DT14-j = C-1** : `cmp`, octet pour octet (`ac6d0696…538d8c`). DT14-a, b, h : égaux à la passe 1 (`cmp`).
- **DT14-k ≡ C-2** et **DT14-l ≡ P-1** : lignes ajoutées et retirées identiques à l'octet, hors lignes datées ; les
  lignes datées ne diffèrent que par l'heure (04:56:45, réécriture du générateur) et, pour k, par le préfixe
  « **Vise §4.2 (b).** » et le repli.
- **DT14-m** (+6 −6, lignes du lot seulement) : l.390 et l.430 redatées à 04:57:32 (et « rangée Kiefer et Vogelsang
  retouchée sur son observation O-4 ») ; **O-4** : la rangée K&V ne recopie plus « b = M/T », écrit « b (rapport de la
  largeur de bande M à la taille d'échantillon T, … « = ») » puis « « be used » (p. 13, imprimée 11) » : « we recommend
  that the critical value corresponding to » … « be used » se suivent sur la p. 13 (entre eux : « b = M=T ») ;
  **O-1** : note 5, « ajout daté de doc 10, placé en fin de document, qui vise §4.2 (b) » ; notes 3 et 6 : renvois C-3
  justes (O-2 compris : « pages et lecteur ci-dessus »). **Juste.**

### 12.4 Mes contrôles sur la série finale (point 4)
- **Citations** (`p2/outils/net_ajouts.py` : texte net base → final ; `guillemets.py` ; ma table reportée par
  `reporter_table.py`, 177 rattachements de la passe 1 + 5 à la main ; `verifier_citations_g2.py` et
  `controle_pages.py` inchangés à l'octet) : **182** segments ; P 134 OK + 2 filigranes (vus sur l'image en passe 1) ;
  D 17 OK (dont C-1 : doc 06 l.49 ; « Déjà réglé » ; « les optionnels retenus », ADR l.170) + 2 vérifiées à part (C-2 :
  littéraux joints de `report.py` l.565-567 ; « forme stratifiée » : `report.py`) ; A 13/13 ; 14 libellés ; aucune au-delà
  de 25 mots ; pages déclarées 31/31 (`p2/verif-citations-c3.tsv`). La forme au point-virgule n'est plus dans doc 10.
- **Dates** (`p2/outils/controle_dates_c3.py`, `p2/controle-dates-c3.txt`) : 18 mentions datées, chacune écrite par un
  bloc de `blocs-c3/` dont la dernière écriture est cette heure (règle d'INDEX : 02:59:27, texte inchangé) ; dates de la
  passe 2 entre 04:37:02 et la génération de `diffs-c3/` (04:58:33) ; paragraphes des blocs tous dans l'état final, sauf
  `d10-p03` (04:55:14, remplacé par `d10-p03-k`, E-6) et le titre de `wishlist` (redaté par `wishlist-l`) : **CONFORME**.
- **En-tête d'INDEX** (`controle_entete.py`) : règle = AVIS l.25-27 à l'octet, quatre jonctions exactes, lignes 15-386
  inchangées : **CONFORME**. Entrées (`controle_entrees.py`) 35/35, « redistribuable » conforme.
- **Gates** : `cargo --locked --offline xtask verify` (état final, INDEX seul ; `journaux/verify-c3.txt`), lignes
  VERDICT : S-G1 à S-G8 VERT ; S-G9 `VERDICT : ROUGE (1 violation(s))` ; `cargo fmt --check : VERT` ; no_std : VERT ;
  `cargo clippy -D warnings : VERT` ; `=== VERDICT GLOBAL : ROUGE … ===` (sortie 1). Violation S-G9 :
  `docs/17-modele-de-menace.md:70`, la même qu'à `ba5ea95` (copie creuse ; docs/17 n'est plus décalé).
  **S-G5, INDEX seul** : VERT, 330 contrôlés, 280 non contrôlés (base : 324 / 281 ; seul changement : le fragment Künsch de
  `LECTURES-PARTIE-3.md`, devenu contrôlé) ; fichiers touchés : un seul non contrôlé, antérieur, doc 10 l.507.
  **S-G5, complet** (biblio du poste + `verser_biblio.py` : 59 copiés, puis 0 et 59 identiques ;
  `journaux/gates-c3-complet.txt`) : VERT, 330 contrôlés, corpus 196/196 ; S-G6 VERT, 196 = 196 ; S-G9 la même seule.
  `docs-sha256sums.py` : conforme (35, 299), sortie 0 ; `revue-dettes5` 4/4 OK.
- Forme : R-25 au plus +57 (a +51, b +9, c +57, d +34, e +9, f +49, g +1, h +2, i +32, j +2, k +2, l +6, m +6) ; R-13 :
  0 ; largeurs : doc 10 ≤ 105, doc 06 ≤ 77, docs/11 ≤ 118, `WISHLIST.md` ≤ 94.
- Mutants de la passe 2 : date fausse en fin de docs/11 → `controle_dates_c3` NON CONFORME ; « be used » → « be
  adopted » → citation ÉCHEC ; cible « Vise §4.4 (c) » → vue seulement par l'intégrité bloc/série (classe K-4 : une
  cible « Vise » se contrôle à la lecture, ce que j'ai fait).

### 12.5 Tête (point 5)
Tête du moment, relue à 05:30:35 UTC : `dda4bbcc2b0f480eb0c39d7891237e0e3d2b0918` ; les dix fichiers touchés n'ont pas
changé depuis `ba5ea95` (`git diff --name-only` vide) ; `diffs-c3/DT14-a` à `DT14-m` : `git apply --check` puis
`git apply`, **13/13** ; l'état obtenu est égal, fichier par fichier (`cmp`), à celui de la série sur `ba5ea95`.

### 12.6 Constats et écarts de la passe 2
- K-1 : corrigé au §7 du rapport du générateur, avec sa marque (179 / 141 ; 12 vérifiées sur 16, les deux fausses parmi
  les quatre non vérifiées).
- Aucun écart nouveau de ma part. Copies de la passe 2 (`p2/base`, `p2/final`, `p2/complet`, cible cargo, archive,
  images) supprimées après usage ; restent les sorties et les outils (`p2/`, `journaux/*-c3*`).
