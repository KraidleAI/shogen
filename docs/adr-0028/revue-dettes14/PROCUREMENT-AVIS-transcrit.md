# Avis de l'advisor sur les suites du procurement PAROXYSME (transcrit)

> Transcription par l'orchestrateur le 2026-10-10 06:47:25 UTC du fichier procurement/avis/AVIS.md ; contrôle FM-1.1 des transcripts du lecteur du procurement, de l'advisor, du générateur et du réviseur G2, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèles résolus : claude-sonnet-5-5 (lecteur), claude-fable-5-1 (advisor), claude-opus-5-5 (générateur, réviseur). Texte ci-dessous avec une seule retouche, déclarée : l. 79 de l'original, le guillemet fermant de la citation de Fisher (*Metron* p. 18) est placé avant « (n − 3) », forme de `biblio/INDEX.md` : le nombre est lu sur l'image de la page, pas sur l'OCR, et S-G5 refuse la citation qui l'inclut ; le chemin du scratchpad est abrégé en `<scratchpad>`.

# AVIS advisor — suites du procurement PAROXYSME (Q-A à Q-E)

**Gate 0** : modèle `claude-fable-5-1` (identifiant donné par l'environnement), effort `medium` (CLAUDE.md §7, amendement 2026-09-18). **`date -u` : non lisible** (aucun outil d'exécution de commande dans cette session ; date de session fournie par l'environnement : 2026-10-09).

Pièces lues : `RAPPORT-PROCUREMENT.md` (191 l., en entier), `ITEMS-ANNEXE-B.md` (en entier), `biblio/INDEX.md` (l.1-191 et l.260-387, plus greps ciblés `licence|redistribut|copyright` et noms de fichiers), `.gitignore` du dépôt (en entier). `biblio/WISHLIST.md` (nommé à l'annexe B l.21) **n'existe pas à ce chemin** ; non cherché ailleurs (interdit de recherche récursive). Aucune pièce D.2, aucun `docs/15-*`, `16-*`, `rapports/`, `adr-0025/`, `monark-m009a/`, `execution/`, aucun `*.jsonl` ouvert. Niveaux : [lu] = lu dans la pièce citée ; [inféré] = mon raisonnement ; [2nd] = de mémoire, à vérifier.

---

## Q-A — Versement sans licence de redistribution

**Fait qui change la question.** Le dépôt n'expose pas les octets de `biblio/` : `.gitignore` l.1-8 [lu] : « les artefacts détenus … ne vont JAMAIS dans le dépôt — copyright et doctrine DEVOPS §1 : le registre est public, les octets restent privés. Allowlist : SEUL INDEX.md est versionné » (`biblio/*` ignoré, `!biblio/INDEX.md`). Le registre le répète à chaque versement récent : « Usage personnel de recherche, jamais redistribué (les octets de `biblio/` ne sont pas versionnés) » (INDEX l.332, l.342) ; « octets privés, jamais dans git » (l.384). Les `.sidecar` tombent sous `biblio/*` : privés aussi. Verser une pièce à `biblio/` n'est donc **pas** une redistribution ; c'est une copie d'étude locale, ce que les pages de garde lues autorisent (CentER : « copie pour étude privée », rapport §2.8 ; City : « usage personnel/recherche/non lucratif, contenu inchangé », rapport §4 l.149 ; arXiv `nonexclusive-distrib/1.0` : « redistribution non accordée au-delà d'arXiv », l.163 — une copie privée n'est pas une redistribution [inféré]).

**Options.**
- (a) Verser le fichier et son sidecar à `biblio/` (privé), la ligne d'INDEX (publique) portant URL, date, sha256, taille, conditions lues, citations ≤ 25 mots vérifiées. C'est la pratique déjà écrite du registre (colonnes du rapport §4 ; notes l.332, l.384).
- (b) Référence seule, sans fichier : perd la preuve d'octets (sha256 sans objet), rend S-G5 (grep sur sidecar) inopérante pour ces pièces ; ne protège rien de plus puisque le fichier n'est de toute façon pas publié.
- (c) Verser le fichier, mais limiter ce que l'INDEX public reproduit : citations courtes seulement, jamais de passage long, jamais de formule recopiée hors citation courte.

**Recommandation : (a) + (c)** = la règle existante, rendue explicite. Le lecteur a préparé exactement cette forme (rapport §3 et §4). Un « versement privé » n'exige pas d'acte de l'investisseur.

**Audit rétroactif.** Pas d'audit de « redistribution » à faire sur ce qui est dans `biblio/` aujourd'hui : rien n'en sort. En revanche un **contrôle mécanique de l'historique git est dû** : `.gitignore` l.4-6 [lu] dit que **l'ancienne liste par extension « laissait passer .json/.toml/.rs/.md/.txt/.yml/.lock »** jusqu'à la trouvaille G2 du 2026-08-13 ; le dépôt a été public. Acte de l'orchestrateur : `git log --all --name-only -- biblio/` (hors `INDEX.md`) et contrôle qu'aucun commit antérieur au 2026-08-13 ne contient un artefact ; si un tel commit existe dans l'historique public, c'est une rediffusion passée : question pour l'avocat, et purge d'historique = **acte de l'investisseur**.

**Question à poser à l'avocat (acte de l'investisseur)** — la seule qui compte : les copies d'étude et leurs extractions intégrales (sidecars) sont téléchargées et lues **dans un environnement cloud tiers** (session distante, scratchpad, Drive privé pour les scans, INDEX l.332) et parfois obtenues par un extracteur tiers (Firecrawl, INDEX l.379). Est-ce encore « usage privé d'étude » au sens des conditions lues (CentER, City, Metron « reproduced with permission », Agresti © Wiley) ? Jusqu'à la réponse : rien ne change, puisque rien n'est publié.

**Règle écrite proposée pour `biblio/`** (à inscrire en tête d'INDEX.md, un lot ; texte à trois lignes) :
1. `biblio/` contient des copies d'étude privées ; seul `INDEX.md` est versionné (`.gitignore`). Une pièce dont la source interdit la copie (miroirs pirates, copies non autorisées vues en recherche) n'entre jamais, même en privé (règle déjà appliquée : annexe B l.21, l.223).
2. Chaque entrée porte : URL exacte, date UTC, sha256, taille, **conditions lues** (ou « aucune licence lue »), version (éditeur / auteur / préimpression) et ce qui n'est pas citable depuis cette copie (pagination).
3. L'INDEX public ne reproduit que des citations ≤ 25 mots contrôlées mot pour mot ; un sidecar n'est jamais versionné ni recopié dans un document publié.

**Risques.** (i) Si Shōgen devient un « standard institutionnel » livré avec son corpus, la règle (a) ne tient plus : à ce moment seules les pièces à licence de redistribution (CC, domaine public US, RFC, préimpressions CC0) pourraient suivre — tenir dès maintenant une colonne « redistribuable : oui/non » pour ne pas refaire l'inventaire. (ii) Kalyuzhny (INDEX l.379) est une **extraction texte par un service tiers** d'une pièce « all rights reserved » : cas le plus exposé, à nommer à l'avocat.

---

## Q-B — Achats

**Shostack 2014 (P-15, E1-METHODE-1 (ii)).** Ce que l'item demande : « forme de la table (colonnes, critères de sortie) et couverture (listes d'attaquants, arbres de menaces) de docs/17 » (annexe B l.21). Les extraits libres ne portent que le chap. 1, la TdM et l'index : la TdM confirme les pages mais « le texte de ces chapitres n'est pas dans les extraits : citer Shostack au-delà du chapitre 1 exige l'achat » (rapport §2.6 [lu]). La partie (i), NIST SP 800-154 (projet, domaine public), est versable et couvre « une méthode sourcée de modélisation de menace » (annexe B l.136).
- Option 1 : acheter l'e-book, **54,00 USD** (valeur du jour, Wiley 2026-10-09, rapport §2.6). Option 2 : fermer (ii) sur la seule partie (i) et retirer de docs/17 toute reprise de Shostack (STRIDE, critères de sortie, listes d'attaquants) ou la ramener à « existe, pp. X (TdM) » sans contenu. Option 3 : reformuler docs/17 de mémoire : **non**, c'est une citation [2nd] interdite par S-G5.
- **Recommandation : option 1.** Le but (standard vendable, sans baisse de qualité) et le coût (le plus bas du lot) la justifient ; STRIDE et la table « critères de sortie » viennent de ce livre ; un standard qui cite un livre par sa table des matières serait une dette. Acte de l'investisseur : l'achat. Si l'investisseur refuse l'achat, option 2 (c'est une décision de périmètre de docs/17, pas une baisse de qualité, à condition de ne rien attribuer à Shostack).

**Little & Rubin 2019 et Manski 2003 (P-08, CENSURE-INFO-2).** Ce que l'item demande : « bornes de type Manski … vocabulaire des données manquantes » (annexe B l.102, l.122). Horowitz & Manski 2000 (version d'auteur, versable) porte précisément les bornes : « the bounds are sharp; they exhaust all of the information that is available given the data and the maintained assumptions », approche « worst-case » (rapport §2.2 [lu]). L'extrait libre de Little & Rubin, chap. 1 p. 14, définit MCAR, MAR, MNAR (rapport §2.2 [lu]).
- **Recommandation : aucun achat.** H&M 2000 (version d'auteur, citée comme telle, sans pagination JASA) suffit pour les bornes ; l'extrait Wiley ch. 1 suffit pour le vocabulaire. Manski 2003 ne devient nécessaire que si le texte invoque un théorème du livre par son numéro ; dans ce cas achat (prix non lu, Springer). Little & Rubin entier (87-108,95 USD) n'est pas nécessaire au but.
- Risques : la version de juin 1999 peut différer du texte JASA (rapport §2.2 : « mon relevé n'a pas comparé les deux ») — citer « version d'auteur, juin 1999 » et ne pas citer de page JASA ; si la pagination doit être citée, achat T&F (prix non lu) ou lecture humaine.

**Mantel & Haenszel 1959 et Cochran 1954 (POOLEE-SOURCE-1).** L'item demande « une source détenue qui énonce la forme de D2 pt 4 … et sa différence avec la statistique de Mantel-Haenszel » (annexe B l.223). Le constat 5 du rapport **change ce qu'il faut citer** : D2 pt 4 (somme stratifiée des K_s − n_s·P̂_s sur la racine de la somme des variances binomiales) **n'est pas** MH (variance hypergéométrique conditionnelle aux marges, table 2×2 par strate ; rapport §2.7 [lu]). Donc D2 pt 4 ne doit être attribué **ni** à MH **ni** à Cochran : c'est une somme de déviations binomiales indépendantes par strate, dont la variance se justifie par « If X and Y are independent, then Var(X + Y) = Var X + Var Y » (UConn, Prop. 12.3, p. 163, [lu] rapport §2.7) et l'approximation normale par le critère déjà détenu (INDEX l.54). La **différence** avec MH se cite sur deux sources détenues : Agresti 2013 §6.4.2 éq. (6.6), p. 227, lue sur le scan (INDEX l.338 [lu]) et PSU STAT 504 §5.3.5 (rapport §2.7 [lu]).
- **Recommandation : aucun achat nécessaire au but.** Rédiger D2 pt 4 comme construction propre (« statistique z stratifiée sous indépendance », sources : UConn Prop. 12.3 ; critère 10 §5.4) et écrire la phrase de distinction : « distincte de la statistique de Cochran-Mantel-Haenszel (Agresti 2013 §6.4.2 éq. 6.6 ; PSU STAT 504 §5.3.5), qui conditionne aux marges de chaque table 2×2 (variance hypergéométrique) et teste l'indépendance conditionnelle ». La clause C-6 de la revue G2 (attribution de D2 pt 4) se tranche par **non-attribution**, ce qui est plus juste que toute attribution.
- Cochran 1954 n'est à acheter que si quelqu'un veut **affirmer** que D2 pt 4 y figure (le rapport dit que seule sa lecture le trancherait) : je déconseille d'affirmer, donc de dépenser. MH 1959 : achat optionnel (primaire de la statistique), Agresti suffit pour un document de conception ; à laisser en liste de souhaits, prix non lu, acte de l'investisseur.
- Risque : si le texte validé dit déjà « Cochran 1954 » ou « Mantel-Haenszel » pour D2 pt 4, c'est un erratum daté, pas une retouche silencieuse.

---

## Q-C — Substituts

**P-14 (durée).** P-10 « ne donne aucune durée » (préimpression p. 5 : « sometimes after an embargo period », rapport §2.5 [lu]). L'aide OSF : annulation « within 48 hours after submission. After 48 hours, the submission will automatically be approved » ; « You can embargo it for up to four years » (rapport §2.5 [lu]).
- **Recommandation : garder l'étiquette « choix de conception » (A-7), mais désormais documentée**, phrase de limite : « La littérature lue (Nosek et al. 2018, préimpression OSF) ne fixe aucune durée ; la pratique d'un registre (OSF, aide officielle, copie du 2026-10-09) prévoit 48 h d'annulation avant approbation automatique et un embargo d'au plus quatre ans ; ces règles sont celles d'un registre, non une prescription ; Shōgen retient [durée] par choix de conception. » Le 48 h d'OSF est l'analogue le plus proche d'un délai de rétractation, à citer comme **précédent de pratique**, jamais comme norme.
- Résidu : la version PNAS (2600-2606) n'a pas été lue (préimpression peut diverger). Geste humain gratuit (rapport §5) = acte de l'investisseur, non bloquant.

**PEARSON-IF-SOURCE-1.** Croux & Dehon 2010, éq. (4) : IF((x,y), R_P, Φρ) = xy − ρ(x²+y²)/2, « which is an unbounded function, showing that RP is not B-robust », attribuée à Devlin et al. (1975) (rapport §2.8 [lu]).
- **Recommandation : adopter**, phrase de limite : « fonction d'influence de la corrélation de Pearson **sous la loi normale bivariée standard** Φρ (Croux & Dehon 2010, éq. (4), citant Devlin, Gnanadesikan & Kettenring 1975) ; la forme employée par le code [à confronter à l'éq. (4) ; la fiche dit “forme classique [inféré]”, annexe B l.799] ; hors normalité la IF diffère ». Si le code emploie cette IF pour N_eff sur des données non gaussiennes, le dire.
- Pièce : CentER DP = copie d'étude (versement privé, Q-A). Geste humain gratuit : la version éditeur serait en libre accès hybride CC BY-NC (OpenAlex, **[2nd]**, rapport §2.8), bloquée aux robots — un téléchargement en navigateur donnerait une copie paginée 497-515 et redistribuable : acte de l'investisseur, souhaitable, non bloquant.

**R1-PLUGIN-1 (b).** Chen & Liu 1997 (loi de Poisson-binomiale, « exact computation of the distribution of SZ ») + NIST e-Handbook §1.3.5.15 (χ² d'ajustement, « expected frequency should be at least 5 », ddl k − c, c = paramètres estimés + 1) (rapport §2.8 [lu]).
- **Recommandation : adopter** pour « statistique et niveau sourcés », avec phrase de limite en trois membres : (1) « le test χ² d'ajustement suppose des fenêtres **indépendantes** ; les m_t successifs sont dépendants (DEP-FENETRES-2) : le niveau nominal n'est pas garanti ; la correction sous dépendance reste ouverte (candidates : P-05 fixed-b, Künsch 1989) » ; (2) « les p̂_i étant estimés, les degrés de liberté sont réduits de leur nombre (NIST : c = nombre de paramètres estimés + 1) » ; (3) « classes de queue regroupées jusqu'à un effectif attendu ≥ 5 ». Page NIST mutable : ancre (date, sha256), comme INDEX l.55.
- Risque : présenter ce test comme « validé » alors que seule sa forme est sourcée ; le rapport le dit : « oui pour la statistique d'ajustement, non pour sa validité sous dépendance ».

---

## Q-D — Introuvables

Règle commune : doc 10 est validé, **retouche par ajout daté seulement** ; doc 06 idem par prudence. On ne retire pas une phrase vraie parce que sa page a disparu ; on écrit ce qu'on détient.

- **NUREG/CR-5485** (doc 06 §5.5) : tentatives du 2026-10-09 consignées (NRC 404, ADAMS 403, OSTI 500, archive.org 0 ; rapport §2.8). Œuvre du gouvernement fédéral US, a priori libre (comme INDEX l.288-290 pour NIST) [inféré] ; de mémoire, c'est le guide NRC de modélisation des défaillances de cause commune (Mosleh et al., 1998) **[2nd]**. **Recommandation :** garder la citation, ajout daté « copie non détenue ; page NRC et ADAMS inaccessibles au 2026-10-09 » ; toute affirmation sur son contenu reste [2nd] ; geste humain gratuit (navigateur sur ADAMS) = acte de l'investisseur ; ne pas verbatimer tant que non détenu.
- **« Finkbeiner 2025 »** : identité non établie ; le seul SoK Finkbeiner trouvé (ICBC 2025) traite du *selfish mining*, pas des oracles (rapport §2.8 [lu]). **Recommandation : retirer l'attribution** (ajout daté : « attribution non établie au 2026-10-09, référence retirée ») ; si la phrase a besoin d'un SoK oracles, Eskandari et al. 2021 est détenu (CC BY-NC-SA) — mais le rapport dit qu'**aucun passage** n'y « pose la dépendance d'amont commun comme problème ouvert » [abs] : si c'est ce que la phrase affirme, elle devient une affirmation propre de Shōgen [inféré], à dire comme telle.
- **Pyth `price-aggregation`** (doc 10 §4.3 pt 3) : page retirée, « Pythnet is being shut down as part of the Pyth Core sunset », expression « hybrid between a mean and a median » absente de la page de renvoi, aucun Wayback (rapport §2.8 [lu]). **Recommandation :** citation datée gardée, ajout daté : « vérifiée le 2026-08-05 ; page retirée par Pyth (constat du 2026-10-09, copie de la page de renvoi détenue) ; copie du 2026-08-05 **non détenue** ; la citation n'est plus re-vérifiable et décrit un mécanisme d'un produit en extinction ». Retrait de la phrase : non (elle était vraie à sa date) ; substitut : aucun trouvé ; geste humain (historique du dépôt docs de Pyth sur GitHub, non accessible à la session) = acte de l'investisseur, optionnel.
- **CoinGecko `exchanges/binance`** (403) : l'API officielle donne `pairs` = 1372, identique au chiffre daté de doc 10 §4.3 (rapport §2.8 [lu]). **Recommandation : substitut adopté**, ajout daté : « page HTML derrière anti-robot au 2026-10-09 ; chiffre re-vérifié sur l'API officielle (copie JSON datée, sha256) ». La copie octets-exacts de la page reste non détenue ; le dire.

---

## Q-E — Fisher 1921

Fisher imprime « The weight of each sample measured on the scale of z is taken to be » (n − 3) (Metron p. 18) et l'erreur probable de z « may be obtained from the same table as before entered with the value n−3 » (p. 14), mais **pas** « 1/√(N−3) » [abs sur l'OCR des 31 pages et les pages vues sur image] (rapport §2.9 [lu] ; INDEX l.337 [lu] concorde : « poids n − 3 sur l'échelle z pp. 14 et 18 »). Penn State STAT 509 L7 imprime « sd = 1/√(n−3) » (INDEX l.328 [lu]).

- **Recommandation : oui, fermer ainsi.** La ligne imprimée « (transformation de Fisher ; Penn State STAT 509 L7) » est exacte : elle attribue la **forme** au manuel, qu'elle nomme. P-03 se ferme au registre par : « primaire détenu et lu : Fisher 1921, Metron 1(3):3-32, pp. 14 et 18 : poids (n−3) sur l'échelle z ; la forme littérale 1/√(n−3) n'y est pas imprimée, elle est celle du manuel (STAT 509 L7) ». Erratum daté de doc 10 §4.2 b dans les mêmes termes (le rapport note que doc 10 le dit déjà et que la lecture « l'étend »).
- Ne pas modifier la ligne imprimée de `report.py` (code, tests, dorés) pour y ajouter Fisher : gain nul, coût réel (annexe B l.107 : sous-lots DOCS-S2-b). Si on y tient, un lot séparé.
- Limite à écrire : l'équivalence « poids (n−3) ⇔ variance 1/(n−3) » est une **inférence** (poids = inverse de la variance, usage de Fisher) [inféré], adossée à la phrase de p. 14 sur la courbe de z « sufficiently normal and constant in deviation ». Attention : les seules racines imprimées (1/√(n−3/2), p. 10 ; 0,67449(1−r²)/√(n−1), p. 11) concernent d'autres cas ; ne jamais les citer pour la ligne imprimée.
- Reste un acte de l'investisseur : aucun.

---

## Récapitulatif des actes de l'investisseur
1. Avocat : copies d'étude + sidecars lus en environnement cloud tiers ; extraction Firecrawl de Kalyuzhny (Q-A).
2. Décision visibilité/purge si l'audit d'historique git (orchestrateur) trouve un artefact de `biblio/` commité avant le 2026-08-13 (Q-A).
3. Achat Shostack e-book, 54,00 USD (valeur du jour) (Q-B). Aucun autre achat nécessaire au but ; MH 1959, Cochran 1954, Manski 2003, Little & Rubin entier : optionnels, prix partiellement non lus.
4. Gestes humains gratuits, non bloquants : PNAS Nosek (pagination), Croux & Dehon version éditeur, ADAMS pour NUREG/CR-5485, historique docs Pyth (Q-C, Q-D).

Fin de l'avis. Aucun fichier suivi modifié.
