# Les mesures pilotes S2 — rapport de la campagne (exécution unique du 2026-10-04)

> **Statut** : rapport rédigé le 2026-10-04 (UTC) par un rédacteur frais (fiche `shogen-worker`, modèle
> `claude-opus-5-5`), qui n'a écrit ni le code d'analyse, ni le paquet de pré-enregistrement, ni les rendus.
> **Non publié** : sa publication est une décision de l'investisseur (ADR-0028 §4, pt 4 ; D9). Il rend compte de ce
> que les rendus de l'exécution unique impriment, sans réinterpréter la règle : le texte scellé fait foi (paquet
> §10.2, pts 1 à 11 ; pt 11 : un cas non prévu est une déviation déclarée, jamais une réécriture).
>
> **Rattachement** : ADR-0028 D6 (v) (sortie branchée `docs/11-mesures-pilotes.md`), D6 (vi) et D9 ; critère de
> sortie de `docs/10-mesures-pilotes-design.md` §7 ; paquet scellé `docs/adr-0028/PAQUET-PREREG-S2.md` (sha256
> `4d2a8276316b1c66a08aabb15ff3b39be812978e93dafc01a4e627f20d0af528`) ; rendus versés à l'octet dans
> `docs/adr-0028/execution/rendu-2026-10-04/`.
>
> **Provenance** : journal G1 du rédacteur, remis à l'orchestrateur avec ce fichier ; il liste chaque lecture, chaque
> commande et sa sortie. Chaque nombre de ce rapport est soit recopié d'un rendu (fichier et ligne cités), soit calculé
> par un script du rédacteur (marque [calc], sortie citée). Un calcul du rédacteur ne remplace jamais une valeur
> imprimée.

## 1. Résumé

Conventions de lecture et lexique : section suivante.

**Question.** S2 devait trancher la question posée par la feuille de route : « les axes R2 sont-ils observables en
pratique, et le test R1 discrimine-t-il quelque chose sur données réelles ? » (doc 10 §1). Le critère de sortie fixe le
livrable : « n fenêtres, K, z du pool, la partition R2 constatée, k_eff vs k nominal ; résultat négatif = résultat »
(doc 10 §7). La règle de décision est la règle scellée SHOGEN-CRITERE-R1-1 (paquet §10.2), évaluée une seule fois sur
le segment J28.

**Verdict de la règle.** Sur le J28 (35 982 fenêtres d'une minute après l'exclusion D5 ; pool d'analyse de 11 flux et
10 hôtes après le retrait de Pyth), la règle rend dans chacune des deux strates la valeur **NE REJETTE PAS, au titre de
la discordance** : la statistique confirmatoire z_s dépasse 2,33 (≈ 20,8 en calme, ≈ 28,5 en stress), mais le plancher
d'erreur-type par blocs la ramène sous le seuil (z_bloc,s ≈ 1,95 et ≈ 1,74). **« R1 discrimine » = FAUX**
(J28 l.435522). Pour chaque strate, le rendu imprime l'énoncé scellé du cas de discordance : « le modèle binomial de
doc 10 §5.1, à fenêtres indépendantes, est rejeté ; la cause n'est pas identifiée entre co-défaillance des sources et
dépendance sérielle des fenêtres » (J28 l.435517, l.435520), avec un excès minimal détectable EMD_s ≈ 196 fenêtres en
calme et ≈ 211 en stress. Côté R2, l'axe ASN a été observé : la partition constatée compte k_eff = 4 classes pour
k nominal = 10 hôtes (J28 l.435779-435780) ; le drapeau 1 est faux dans les deux strates et le drapeau 2 est éteint
(J28 l.435794-435795).

**Ce que ce verdict permet de dire.** Sur 24 585 fenêtres calmes et 11 397 fenêtres de week-end, axes panne, staleness
et hors-enveloppe, tel qu'observé par cet instrument (hôte, DNS et réseau du harnais compris) : le modèle binomial à
fenêtres indépendantes est rejeté dans les deux strates (énoncé scellé de la discordance) ; la règle pré-enregistrée,
qui exige aussi z_bloc,s ≥ 2,33, rend NE REJETTE PAS dans les deux strates, si bien que « R1 rejette (s) » n'est énoncé
pour aucune strate. Un résultat négatif est un résultat (doc 10 §7). L'axe ASN est observable : 7 des 10 hôtes
du pool partagent AS13335 (Cloudflare), côté livraison (J28 l.435691).

**Ce qu'il ne permet pas de dire.** Il n'établit ni n'exclut une co-défaillance des sources : la cause de la
discordance n'est pas identifiée (énoncé scellé). Il n'établit aucune dépendance de paire (ADR-0028 D3 : descriptif).
Il n'établit pas l'indépendance des sources (doc 09). Les descriptifs pré-enregistrés (§5), dont la décomposition de K
par lectures `panne_transport`, sont hors décision et n'identifient aucune cause. Les sorties hors décision qui
impriment « R1 discrimine » VRAI (J14 principal ; variante « plage incluse » du recalcul tiers) ne changent pas le
verdict (§7). Rien n'est dit sur la justesse d'un prix, ni hors des axes mesurés (A(axis-coverage), doc 08).

**Décisions de l'investisseur (énoncées ; ce rapport n'en tranche aucune).** Options pré-enregistrées :

- ADR-0028 D6 (vi), recopié (guillemets intérieurs rendus par “ ”) : « Clause datée après J28 : décision de
  l'investisseur (§4.10 b), sur la règle écrite au paquet (SHOGEN-CRITERE-R1-1). Si R1 discrimine : lot “benchmark
  continu” par un G0 neuf (réimplémentation dans le cœur, ou promotion G0-G7 de la collecte). Sinon, la collecte meurt
  comme prévu. » Erratum daté du même alinéa : « “R1 discrimine” := VRAI de la règle SHOGEN-CRITERE-R1-1 ; “la collecte
  meurt” reste une décision de l'investisseur ».
- ADR-0028 D9, recopié : « Après J28 : bifurcation = décision de l'investisseur (§4.10 b) », avec, pour la branche
  constatée ici : « Si (i) est faux : priorité à G4 et révision de 04 (doc 10 l.35-36 ; 05-roadmap l.126-127). »
- Paquet §10.2 pt 11, recopié : « FAUX → priorité à G4 et révision de 04, avec les EMD_s » ; « “La collecte meurt”
  reste une décision de l'investisseur (D6 vi), jamais une conséquence mécanique. »
- Publication du J14 et du J28, et de ce rapport (ADR-0028 §4 pt 4 ; D4 : le J14 n'est pas publié sans décision de
  l'investisseur).

Décisions consignées depuis, après l'exécution et avant ce rapport (JOURNAL l.322, 2026-10-04 02:42:19 UTC ; réponses
de l'investisseur recopiées) : collecte S2, « L'arrêter (Recommandé) » ; S2-bis, « Oui, préparer S2-bis (Recommandé) » ;
publication, « Oui, en principe (Recommandé) », le feu vert final restant à l'investisseur après lecture du rapport
validé ; priorité, « Position d'abord (Recommandé) ». Le JOURNAL y note que la bifurcation D9 suit la branche
« (i) faux » (G4, révision de doc 04), plus un lot ADR-S2-BIS.

## Conventions de lecture et lexique

Les rendus sont cités par abréviation et numéro de ligne (« J28 l.435516 » = ligne 435516 du rendu J28). Tous sont dans
`docs/adr-0028/execution/rendu-2026-10-04/`, sous le préfixe `shogen-27b0e30-rendu-20261004T011129Z-943.` :

| abréviation | fichier | contenu | sha256 |
|---|---|---|---|
| SUITE | `0-suite.out` | suite `s2-harness` (run `suite`) | `4f223a22950778c799b39b1856a400c965ac18b4b57625bfef3136c04daaeb3a` |
| J14p | `1-j14-principal.out` | J14 principal, hors décision | `246ebeea132392de15f34ccefff808e4e44b157498c3fdc1009282cc7e1e1498` |
| J14s | `2-j14-second.out` | J14 second, hors décision | `d89db3a94da67f48c00f3bbc7ce7710a092fc3ad14f935e874e8c905f0172b24` |
| J28 | `3-j28.out` | segment confirmatoire : blocs 1 à 6 et [SENSIBILITÉ] | `26877549658b7271f766b433e941c79a35169398238755fa4bbf77a4911d65c0` |
| RT | `4-recalcul-tiers.out` | recalcul tiers (`recompute_*`), JSON | `a76ad44832d28751e68c56d6844be0c0ebd83f1b79b89bd7a16611779d891ac8` |
| RAW | `5-raw.out` | verdict du journal brut | `e996c6343bbed572221b6a3eb7679286167b46b3452431136f3d622254ae97b8` |
| ENR | `json` | enregistrement d'oracle de rôle « rendu » | `355cf9bb43609c1c4b0f3ffebcd32d9d987e5e12e63277d9e4acbd467eb0fb5c` |

Autres pièces : PAQ = paquet scellé ; ADR = `docs/adr-0028/ADR-0028-decisions-sortie-S2.md` ; annexes A, B, D du même
dossier ; doc 04, doc 08, doc 09, doc 10 = `docs/04-certificat-diversite.md`, `docs/08-assumptions.md`,
`docs/09-vocabulaire.md`, `docs/10-mesures-pilotes-design.md`.

- **Valeurs complètes** : chaînes `Decimal` (précision 50) recopiées telles qu'imprimées, entre accents graves.
- **Arrondis de lecture** : dans le texte courant seulement, signalés par « ≈ », à 3 chiffres significatifs ; la valeur
  complète est dans une table, avec sa ligne.
- **[calc]** : calcul du rédacteur (scripts `d3_lift.py`, `controles_r1.py`, `comparer_recalcul.py`, `calc_divers.py`,
  bibliothèque standard Python, arithmétique exacte ou `decimal` ; sorties citées au §8.9 et au §6).
- **Aucune p-valeur** n'est donnée ni lue (paquet §10.2 pt 4). Les queues binomiales exactes que les rendus J14
  impriment hors décision sous la garde §5.4 ne sont pas recopiées ici ; elles restent lisibles aux lignes citées
  (§7.1, §7.2).
- **Vocabulaire** : registre de doc 09. L'indépendance de sources n'est jamais « établie » : un modèle d'indépendance
  est rejeté ou non rejeté, sur n fenêtres, sur des axes nommés, tel qu'observé par cet instrument.

**Lexique**, pour un lecteur extérieur (définitions de doc 10 et du paquet, résumées) :

- **Flux, source, hôte** : un flux est une lecture du prix BTC/USD (ou BTC/USDT) servie par une source (place
  d'échange, agrégateur ou oracle) ; deux flux peuvent partager un hôte (`www.okx.com`). Le pool configuré compte
  12 flux.
- **Fenêtre** : minute de la grille UTC (w = 60 s) ; dans chaque fenêtre, chaque flux compte pour une lecture.
- **Écart** (doc 10 §5.2) : un flux est en écart dans une fenêtre s'il est en panne (lecture absente, statut non `ok`
  ou prix absent), en staleness (horodatage porté plus vieux que σ_classe) ou hors enveloppe (écart relatif à la
  médiane des autres flux au-delà de τ_classe, avec au moins quatre répondantes).
- **n, K** : nombre de fenêtres analysées d'une strate ; nombre de ces fenêtres où au moins deux flux sont en écart.
- **P̂_more** : probabilité d'au moins deux écarts dans une fenêtre si les flux étaient sans lien entre eux, estimée
  depuis le taux d'écart de chaque flux (modèle de Knight et Leveson, doc 10 §5.1).
- **z_s, z_bloc,s** : écart de K à n·P̂_more, rapporté à l'erreur-type binomiale à fenêtres indépendantes (z_s) ou à
  une erreur-type par blocs qui admet une dépendance sérielle des fenêtres de portée inférieure à ℓ = 240 fenêtres,
  soit 4 h (z_bloc,s).
- **Règle SHOGEN-CRITERE-R1-1** : une strate testée (garde n·P̂_more(1 − P̂_more) ≥ 10 tenue) REJETTE si z_s ≥ 2,33
  et z_bloc,s ≥ 2,33 ; « R1 discrimine » vaut VRAI si au moins une strate rejette.
- **Strates** : stress = samedi et dimanche UTC ; calme = les autres jours ; calendrier fixé avant la campagne.
- **EMD_s** : excès minimal détectable de K, en fenêtres, à puissance 0,8 (choix de conception).
- **R2, k_eff, k nominal** : observables de diversité ; ici l'axe ASN, réseau qui annonce l'adresse de chaque hôte ;
  k_eff = nombre de classes après fusion des hôtes qui partagent un ASN mesuré ; k nominal = nombre d'hôtes.
- **J28, J14** : le J28 est le segment confirmatoire (38 600 fenêtres distinctes à n fixe, puis exclusion D5) ; les
  deux J14 sont des coupes du début de campagne (quatorze jours pour le principal, jusqu'au 2026-09-04 pour le
  second), hors décision.
- **D1, D5** : retrait des flux sans aucune lecture `ok` (ici Pyth) ; exclusion d'une plage de harnais dégradé, du 24 au
  26 septembre 2026.
- **Hors décision** : sortie imprimée et étiquetée, qui ne peut pas changer le verdict (paquet §10.2 pt 9).

## 2. Instrument et campagne

### 2.1 Classe de fait, pool, flux et hôtes

- Classe : « BTC/USD-stable, devise marquée par flux » ; « pool configuré = 12 flux » : binance, coinbase, kraken,
  okx_ticker, okx_index, bitstamp, gemini, bitfinex, coingecko, defillama, pyth, chainlink (J28 l.8-9) ;
  composition des devises du pool d'analyse : 9 USD / 2 USDT (l.46).
- Fenêtre w = 60 s (l.10) ; décimales `Decimal` à 50 chiffres (l.19) ; seuil z = 2,33 (l.21) ; garde
  n·P̂_more·(1−P̂_more) ≥ 10 (l.16, l.20) ; n_min = 4 répondantes pour l'axe hors-enveloppe (l.17).
- Seuils par classe, committés avant la campagne (J28 l.12-14) :

| classe (σ/τ) | flux | σ_classe (s) | τ_classe |
|---|---|---|---|
| `place_horodatee` | coinbase, okx_ticker, okx_index, bitstamp, gemini | `180.0` | `0.0045` |
| `sans_horodatage` | binance, kraken, bitfinex | `None` (staleness non évaluée) | `0.0045` |
| `agregateur` | coingecko, defillama | `1140.0` | `0.026` |
| `oracle_chainlink` | chainlink | `10695.0` | `0.0165` |
| `oracle_pyth` | pyth | `33.0` | `0.0015` |

- Définition d'écart imprimée (J28 l.435448) : par fenêtre et par flux du pool d'analyse, précédence panne >
  staleness > hors-enveloppe ; K = fenêtres à au moins deux écarts. Résidu imprimé : staleness « fail-open » pour
  binance, kraken et bitfinex, qui ne portent pas d'horodatage (l.435464).
- Hôtes : les 11 flux du pool d'analyse sont servis par 10 hôtes distincts (« k nominal = 10 (hôtes distincts du
  pool) », J28 l.435779) ; okx_index et okx_ticker partagent `www.okx.com` (l.435688) ; chainlink est lu par le RPC
  public `ethereum-rpc.publicnode.com` (l.435685).

### 2.2 Pool d'analyse (ADR-0028 D1)

| strate | retrait (cas) | comptes imprimés | k nominal_s | source |
|---|---|---|---|---|
| calme | pyth, cas (a) | « ok = 0 / 24585 lectures, n = 24585 » | « 10 sources / 11 flux » | J28 l.42, l.44 |
| stress | pyth, cas (a) | « ok = 0 / 11397 lectures, n = 11397 » | « 10 sources / 11 flux » | J28 l.43, l.45 |

Pyth est retiré de R1, de L&M et de R2 dans les deux strates (cas (a) : aucune lecture `ok` dans aucune strate). L'ADR
porte le compte sur le journal entier : « 0 `ok` sur 40 804 lectures, HTTP 401 dès 2026-08-26T19:00Z » (ADR l.25).
Aucun retrait au cas (b) n'est imprimé.

### 2.3 Segment J28 (ADR-0028 D4, D2 pt 6)

- Segment : `[1787770800 ; 1790558880) = [2026-08-26T19:00:00+00:00 ; 2026-09-28T01:28:00+00:00)`, semi-ouvert, même
  borne sur `window_start`, `ts` et `harness_ts`, n fixe = 38 600 (J28 l.31).
- Le journal compte 38 600 fenêtres distinctes : première `1787770800` (2026-08-26T19:00:00Z), dernière
  `window_start` `1790558820` (2026-09-28T01:27:00Z) (l.28) ; T_fin = 1790558820 + 60 = 1790558880 [calc].
- Le segment ne retire rien : « fenêtres distinctes (window_close) calme 0, stress 0 ; asn_attribution 0 ;
  clock_check 0 » (l.32).

### 2.4 Exclusion D5 (amendement d'ADR-0025 déc. 1)

- Bornes : `window_start` dans `[1790273880 ; 1790435280]` (fermée ; 2026-09-24T18:18:00Z à 2026-09-26T15:08:00Z,
  J28 l.33) ; `ts` et `harness_ts` dans `[1790273880 ; 1790435340)` (l.34).
- Retiré par la plage (l.35-36) : 1 709 fenêtres calmes et 909 fenêtres de stress ; 5 313 relevés `asn_attribution`
  (4 498 `ok`, 815 `resolve_failed`) ; 483 relevés `clock_check`.
- Motif (ADR l.60) : `resolve_failed` 15,3 % dans la plage contre 1,85 % hors plage, santé du harnais DNS, pas une
  statistique de source ; « causalité non établie » (rappelée par le rendu, J28 l.435801).
- Contrôle [calc] : 1 709 + 909 = 2 618 ; 38 600 − 2 618 = 35 982 = 24 585 + 11 397.

### 2.5 Strates et n par strate

- Calendrier ex ante : « kind=weekend_utc stress = samedi+dimanche UTC », décision opérateur committée avant le
  lancement, jamais déduite des données (J28 l.27).
- n_calme = 24 585 fenêtres complétées (J28 l.435451) ; n_stress = 11 397 (l.435471).
- Couverture des cinq week-ends (J28 l.435814-435818) : 2026-08-29, 1 140 fenêtres sur 2 880 (19 h 00 min) ;
  2026-09-05, 2 801 ; 2026-09-12, 2 611 ; 2026-09-19, 2 874 ; 2026-09-26, 1 971 dans la variante exclue (32 h 51 min),
  909 fenêtres retirées par la plage D5.

### 2.6 Fenêtres sautées

- Grille de pas 60 s sur le segment, sans marqueur `window_close`, hors plage D5 : 5 701 en calme, 2 094 en stress,
  toutes causes confondues, sous l'hypothèse H_perte (A(loss-non-informative), doc 08) (J28 l.37).
- Ventilation (l.38-41) : « harnais vivant » (sautée entre deux marqueurs d'un même démarrage) 17 en calme, 150 en
  stress ; cause non attribuée par le journal (arrêt ou passage entre démarrages) 5 684 en calme, 1 944 en stress.
- Contrôle [calc] : la grille du segment compte (1790558880 − 1787770800)/60 = 46 468 fenêtres ; 46 468 − 38 600
  (marqueurs) − 73 (fenêtres de la plage sans marqueur, J28 l.435806) = 7 795 = 5 701 + 2 094.
- Le harnais a démarré 4 093 fois sur la campagne, avec des `run_params` concordants sur les champs porteurs (J28 l.26).

### 2.7 Hôte de collecte et limites de l'observateur

- La collecte S2 est une lecture HTTPS nue par un harnais (doc 10 §1, non-objet 1) ; la seule interaction avec une
  chaîne est une lecture `eth_call` par RPC public (doc 10 §1, non-objet 4).
- Les rendus portent la trace d'un hôte de collecte Windows : chemin `F:\shogen-campagne\sigma-tau.json` (J28 l.7) ;
  erreurs de socket `WinError 10013` dans les relevés ASN de fin de J14 principal (J14p l.209885). Le JOURNAL situe
  cette collecte sur le poste de l'investisseur : consigne pour S2-bis, verbatim, « cette fois on le fait sur un VPS,
  pas sur mon PC » (JOURNAL l.324).
- Un seul point d'observation et un seul résolveur par relevé ASN, `cloudflare-dns.com` (J28 l.435676-435688) ; le rendu
  publie lui-même les résidus 3 (mono-vantage ; sonde multi-résolveurs « DUE », J28 l.435772) et 5 (le chemin de mesure
  appartient à la classe mesurée, « le résidu est à son MAXIMUM, publié », l.435774).
- L'affectation des fenêtres aux strates et aux segments repose sur l'horloge de l'hôte, A(harness-clock) (doc 08 ;
  paquet §12 pt 17). Le bloc 1 du J28 imprime 3 610 relevés `controle_horloge` de démarrage (l.48-3657 ; compte
  [calc] par recherche de lignes) ; leur étendue n'est pas calculée par le rendu (paquet §12 pt 17) ni par ce rapport.
- Le libellé du descriptif de l'annexe D.5 le rappelle : « le z confirmatoire inclut les modes communs de l'observateur
  (hôte, DNS, réseau) » (J28 l.435531).

## 3. Verdict confirmatoire (J28, règle SHOGEN-CRITERE-R1-1)

La règle est évaluée mécaniquement par le script d'exécution unique sur le segment J28, pool d'analyse D1 par strate,
exclusion D5, dans chaque strate confirmatoire (paquet §10.2 pt 1). Les comparaisons portent sur les valeurs `Decimal`
non arrondies, à la constante `Decimal("2.33")`, avec l'inégalité « ≥ » (pt 4 ; rappel imprimé, J28 l.435515).

### 3.1 Entrées et valeur par strate (valeurs complètes)

| entrée (pt 1) | calme | stress | J28 |
|---|---|---|---|
| n_s (fenêtres complétées) | `24585` | `11397` | l.435451 ; l.435471 |
| K_s (fenêtres à ≥ 2 écarts) | `154` | `133` | l.435451 ; l.435471 |
| P̂₀ | `0.94236061369788154146024296580093086828513938470018` | `0.94068072247707197570660265774160717593176388308751` | l.435465 ; l.435485 |
| P̂₁ | `0.056276435879320695626255997808433611118939114709424` | `0.057852878561437609992981152213024246102249979400096` | l.435466 ; l.435486 |
| P̂_more,s | `0.0013629504227977629135010363906355205959215005903986` | `0.0014663989614904143004161900453685779659861375123928` | l.435467 ; l.435487 |
| garde n_s·P̂_more,s(1−P̂_more,s) (seuil 10) | `33.462466216157713120610261901717310599417168320476` | `16.688041699661428674928415017858500902580981925520` | l.435468 ; l.435488 |
| z_s | `20.829495417808173515660354538360738280133057485734` | `28.466243694685921454102240881955034913016073716310` | l.435469 ; l.435489 |
| ℓ | `240` | `240` | l.435494 ; l.435498 |
| γ̂₀,s | `153.03534675615212527964205816554809843400447427293` | `131.44792489251557427393173642186540317627445819075` | l.435494 ; l.435498 |
| σ̂²_bloc,s | `3837.3644239148386709307388556071047850697416032311` | `4444.2268779663177986090438425985366511755710614584` | l.435494 ; l.435498 |
| FIV_s | `114.67667682132543551816351669459307932477895917439` | `266.31206692493364443057277635430175333060222847741` | l.435495 ; l.435499 |
| R_centrage,s | `4.5733433324247139833425606396397303313682246279750` | `7.8767735159232268649296718039283324323387017357003` | l.435495 ; l.435499 |
| FIV_série,s | `25.075020282924108215938185508697612502356118056163` | `33.809791075822184156289564915103491737231918165960` | l.435495 ; l.435499 |
| z_bloc,s | `1.9450967130759827973431520036612640074344098711768` | `1.7443544612798118150330419847751992092506597257981` | l.435496 ; l.435500 |
| run maximal de I_t | `6` | `2` | l.435497 ; l.435501 |
| EMD_s (fenêtres) | `196.46940578076511214605312297686775770638678422511` | `211.43482468284790300599634573463971654187425170170` | l.435518 ; l.435521 |
| fraction EMD_s/n_s | `0.0079914340362320566258309181605396688105099363117799` | `0.018551796497573738966920798958904950122126371124129` | l.435518 ; l.435521 |
| valeur de la règle (pt 5) | NE REJETTE PAS (discordance) | NE REJETTE PAS (discordance) | l.435516 ; l.435519 |

Lecture (arrondis signalés) : en calme, n = 24 585, K = 154, P̂_more ≈ 0,00136, garde ≈ 33,5 (tenue), z_s ≈ 20,8 ≥ 2,33
et z_bloc ≈ 1,95 < 2,33 ; en stress, n = 11 397, K = 133, P̂_more ≈ 0,00147, garde ≈ 16,7 (tenue), z_s ≈ 28,5 ≥ 2,33 et
z_bloc ≈ 1,74 < 2,33. Les deux strates sont testées : garde §5.4 tenue, σ̂²_bloc,s > 0 et n_s ≥ 30·ℓ = 7 200, donc
z_bloc,s publiée (pts 2, 3 et 5).

[calc] Par construction (même numérateur K_s − n_s·P̂_more,s, paquet pt 3), z_bloc,s = z_s/√FIV_s : l'écart entre les
deux statistiques est porté en entier par FIV_s ≈ 115 en calme et ≈ 266 en stress, produit de R_centrage,s (≈ 4,57 ;
≈ 7,88) et de FIV_série,s (≈ 25,1 ; ≈ 33,8). Le rapport n'en tire aucune cause (pt 8).

### 3.2 Énoncés imprimés (pt 8), mot pour mot

Lignes J28 l.435515 à l.435522, recopiées par extraction (`sed -n '435515,435522p'`) :

```text
  ── règle SHOGEN-CRITERE-R1-1 (ADR-0028 §1 bis.1 pts 1-11 ; forme scellée) : valeur par strate ; comparaisons sur les Decimal publiées, non arrondies, au seuil 2.33, « ≥ » ; aucune p-valeur
    « calme » : z_s = 20.829495417808173515660354538360738280133057485734 ≥ 2,33 ; z_bloc = 1.9450967130759827973431520036612640074344098711768 < 2,33 → NE REJETTE PAS (discordance)
    « calme » : « le modèle binomial de doc 10 §5.1, à fenêtres indépendantes, est rejeté ; la cause n'est pas identifiée entre co-défaillance des sources et dépendance sérielle des fenêtres »
    « calme » : EMD_s = (2,33 + 0,8416)·max(√(n_s·P̂_more,s·(1 − P̂_more,s)), σ̂_bloc,s) = 196.46940578076511214605312297686775770638678422511 fenêtres ; fraction de n_s = 0.0079914340362320566258309181605396688105099363117799 (puissance 0,8 : choix de conception ; aucun seuil sur l'EMD)
    « stress » : z_s = 28.466243694685921454102240881955034913016073716310 ≥ 2,33 ; z_bloc = 1.7443544612798118150330419847751992092506597257981 < 2,33 → NE REJETTE PAS (discordance)
    « stress » : « le modèle binomial de doc 10 §5.1, à fenêtres indépendantes, est rejeté ; la cause n'est pas identifiée entre co-défaillance des sources et dépendance sérielle des fenêtres »
    « stress » : EMD_s = (2,33 + 0,8416)·max(√(n_s·P̂_more,s·(1 − P̂_more,s)), σ̂_bloc,s) = 211.43482468284790300599634573463971654187425170170 fenêtres ; fraction de n_s = 0.018551796497573738966920798958904950122126371124129 (puissance 0,8 : choix de conception ; aucun seuil sur l'EMD)
  « R1 discrimine » (§1 bis.1 pt 6 ; déclencheur de D6 (vi) et D9) = FAUX : aucune strate ne rejette ; strate(s) testée(s) : calme, stress
```

Le cas de discordance (garde tenue, z_s ≥ 2,33, z_bloc,s publiée < 2,33) a la valeur NE REJETTE PAS ; la strate
imprime l'énoncé de discordance et EMD_s, et non l'énoncé « n'est pas rejeté » ; ce cas n'est jamais un VRAI (paquet
§10.2 pts 5 et 8). Cette lecture « un seul test » de la discordance a été ratifiée par l'orchestrateur le 2026-09-30,
sous veto, avant le scellement (paquet §10.1). EMD_s = (2,33 + 0,8416)·max(√(n_s·P̂_more,s(1−P̂_more,s)), σ̂_bloc,s) :
la puissance 0,8 est un choix de conception, sans aucun seuil sur l'EMD (pt 8). Ici le maximum est σ̂_bloc,s dans les
deux strates [calc : √σ̂²_bloc,s ≈ 61,9 et ≈ 66,7 contre √garde ≈ 5,78 et ≈ 4,09].

### 3.3 « R1 discrimine »

« R1 discrimine » vaut FAUX : « aucune strate ne rejette ; strate(s) testée(s) : calme, stress » (J28 l.435522). Par
le pt 6, FAUX signifie qu'aucune strate ne REJETTE, qu'au moins une NE REJETTE PAS et qu'aucune n'est en rejet non
qualifiable. C'est le déclencheur de D6 (vi) et de D9 (§1, décisions de l'investisseur).

### 3.4 Famille de Bonferroni et prémisse de la borne (pt 7)

Ligne imprimée (J28 l.435503) :

```text
  famille de Bonferroni pré-enregistrée (ADR-0028 D2 pt 4) : m = 2 (strates testées : calme, stress ; m ≤ 2 ; §1 bis.1 pt 6), tests unilatéraux au seuil 2,33 ; borne P(au moins un rejet à tort) ≤ 2 × 0,01 = 0,02 sous le modèle nul joint (§1 bis.1 pt 7) : modèle d'indépendance du pool de doc 10 §5.1 et dépendance sérielle des fenêtres de portée < ℓ = 240 (A(window-dependence), registre 08) ; niveau asymptotique, non démontré ≤ 0,01 en échantillon fini (SHOGEN-SIM-NIVEAU-1)
```

Prémisse, recopiée du paquet §10.2 pt 7 : « La borne vaut sous le modèle nul joint : le modèle d'indépendance du pool de
doc 10 §5.1, avec une dépendance sérielle des fenêtres de portée < ℓ (A(window-dependence), doc 08). Le niveau est
asymptotique […]. Il est conservateur sous fenêtres iid (plug-in de P̂_more). Il n'est pas démontré ≤ 0,01 en
échantillon fini ». Les mesures de SIM-NIVEAU et de l'étape S, faites avant le scellement sur données synthétiques
seules (paquet §10.3), ne disent rien des sources réelles : sous le modèle nul simulé, le taux de rejet à tort de la
règle va de 0,001590 (SE 0,000126) à 0,001810 (SE 0,000134) à fenêtres indépendantes, et reste au plus 0,00357
(SE 0,00034) près de la garde ; celui de z_s seul atteint 0,337300 (SE 0,001495) sous dépendance sérielle (runs moyens
de 60 fenêtres) (paquet §10.3, tables l.139-148 et l.153-162). Par conséquence pré-déclarée, ces sorties ne modifient ni
ℓ, ni le seuil, ni la règle (pt 7).

### 3.5 Écarts par flux (bloc 3)

p̂ᵢ = écarts du flux / n_s ; les valeurs complètes de p̂ᵢ sont aux lignes citées. « nonÉv » compte les cellules non
évaluables sur l'axe hors-enveloppe, qui ne sont pas des écarts (J28 l.435448).

| flux | classe | calme : écart (panne / stale / horsE / nonÉv) | stress : écart (panne / stale / horsE / nonÉv) | J28 |
|---|---|---|---|---|
| binance | `sans_horodatage` | 372 (372 / 0 / 0 / 0) | 46 (46 / 0 / 0 / 0) | l.435453 ; l.435473 |
| coinbase | `place_horodatee` | 56 (56 / 0 / 0 / 0) | 11 (11 / 0 / 0 / 0) | l.435454 ; l.435474 |
| kraken | `sans_horodatage` | 34 (34 / 0 / 0 / 0) | 46 (46 / 0 / 0 / 0) | l.435455 ; l.435475 |
| okx_ticker | `place_horodatee` | 64 (64 / 0 / 0 / 0) | 6 (6 / 0 / 0 / 1) | l.435456 ; l.435476 |
| okx_index | `place_horodatee` | 64 (64 / 0 / 0 / 0) | 7 (7 / 0 / 0 / 1) | l.435457 ; l.435477 |
| bitstamp | `place_horodatee` | 475 (475 / 0 / 0 / 0) | 39 (39 / 0 / 0 / 0) | l.435458 ; l.435478 |
| gemini | `place_horodatee` | 68 (65 / 3 / 0 / 0) | 21 (19 / 2 / 0 / 0) | l.435459 ; l.435479 |
| bitfinex | `sans_horodatage` | 32 (30 / 0 / 2 / 0) | 51 (51 / 0 / 0 / 0) | l.435460 ; l.435480 |
| coingecko | `agregateur` | 56 (56 / 0 / 0 / 0) | 127 (127 / 0 / 0 / 1) | l.435461 ; l.435481 |
| defillama | `agregateur` | 159 (158 / 1 / 0 / 0) | 226 (226 / 0 / 0 / 0) | l.435462 ; l.435482 |
| chainlink | `oracle_chainlink` | 71 (69 / 0 / 2 / 0) | 113 (113 / 0 / 0 / 0) | l.435463 ; l.435483 |

## 4. Drapeaux et R2 (blocs 5 et 6 du J28)

### 4.1 Tête de certificat (bloc 6), recopiée

Lignes J28 l.435779 à l.435797, recopiées par extraction (`sed -n '435779,435797p'`) :

```text
  k nominal = 10 (hôtes distincts du pool)
  k_eff     = 4  — k_eff = nombre de classes de la partition R2 measured (§5.6)
  date de la partition, axe ASN (ADR-0026 déc. 1 ; HS2-07) = relevé asn_attribution retenu (dernier par hôte, après filtre de lecture) : min 1790558275.4337332 = 2026-09-28T01:17:55.433733+00:00 ; max 1790558282.5194278 = 2026-09-28T01:18:02.519428+00:00 ; 10 / 10 hôtes du pool — descriptif seulement (ADR-0028 annexe D.5)
  relevés asn_attribution retenus sans ts (hôtes du pool, entrée malformée) = 0 — comptés à part, hors date de la partition (SHOGEN-BLOC6-TS-1)
  R3 (déclaration : entité légale, juridiction, méthodologie annoncée) ne modifie JAMAIS k_eff (§5.6 / 04 §3) — seuls les recouvrements R2 measured partitionnent.
  PARTITION NOMMÉE (ADR-0007 : nomme l'amont, jamais un compte anonyme) :
    cluster = {api-pub.bitfinex.com, api.coingecko.com, api.exchange.coinbase.com, api.kraken.com, coins.llama.fi, ethereum-rpc.publicnode.com, www.okx.com} via AS13335 CLOUDFLARENET - Cloudflare, Inc. [fusion ASN partagé AS13335 CLOUDFLARENET - Cloudflare, Inc. — côté livraison (§4.1, résidu 1)] ; flux = ['bitfinex', 'chainlink', 'coinbase', 'coingecko', 'defillama', 'kraken', 'okx_index', 'okx_ticker']
        amont déclaré (basis:doc, ne fusionne pas) : binance → coingecko (coingecko.com/en/exchanges/binance)
        amont déclaré (basis:doc, ne fusionne pas) : coinbase → pyth (pyth.network/publishers)
        amont déclaré (basis:doc, ne fusionne pas) : coingecko → defillama (docs.llama.fi/llms-full.txt)
        caveat : chemin de LECTURE ≠ amont (§3.2) : l'ASN mesuré est celui du fournisseur RPC (ethereum-rpc.publicnode.com), une infrastructure de lecture, pas l'amont du feed
    cluster = {api.binance.com} via AS16509 AMAZON-02 - Amazon.com, Inc. ; flux = ['binance']
        amont déclaré (basis:doc, ne fusionne pas) : binance → coingecko (coingecko.com/en/exchanges/binance)
    cluster = {api.gemini.com} via AS14618 AMAZON-AES - Amazon.com, Inc. ; flux = ['gemini']
    cluster = {www.bitstamp.net} via AS19551 INCAPSULA - Incapsula Inc ; flux = ['bitstamp']
  DRAPEAU 1 « historique insuffisant » (§5.4) par strate : {'calme': False, 'stress': False}
  DRAPEAU 2 « co-défaillance observée non expliquée par les axes R2 » (§5.6) : état = ETEINT
      « R1 discrimine » FAUX : le modèle d'indépendance n'est rejeté dans aucune strate testée (bloc 3)
      entrées (ADR-0028 §1 bis.1 pt 10) : « R1 discrimine » = FAUX (bloc 3) ; k_eff = 4 ; k nominal du segment (hôtes) = 10 ; k nominal_s (flux du pool de la strate) : « calme » = 11, « stress » = 11 — comparaison hétérogène déclarée ; strate poolée hors des entrées
```

- **Partition nommée et datée** : quatre classes sur l'axe ASN, dont un cluster de sept hôtes et huit flux fusionnés sur
  AS13335 (Cloudflare), « côté livraison » (résidu 1 de doc 10 §4.1), et trois singletons : `api.binance.com`
  (AS16509), `api.gemini.com` (AS14618), `www.bitstamp.net` (AS19551). Date : relevés `asn_attribution` retenus,
  dernier par hôte, entre 2026-09-28T01:17:55Z et 01:18:02Z, 10 hôtes sur 10 (l.435781). Les arêtes `basis:doc`
  (binance → coingecko, coinbase → pyth, coingecko → defillama) sont des amonts déclarés : elles ne fusionnent pas
  (ADR-0008, rappelé l.435786-435788).
- **k_eff = 4, k nominal = 10** (hôtes distincts du pool, l.435779-435780) ; k nominal_s = 11 flux dans chaque strate,
  « comparaison hétérogène déclarée » (l.435797). k_eff n'est pas un compte d'indépendance : c'est le nombre de classes
  de la partition R2 constatée (doc 10 §5.6) ; z n'est jamais composé dans k_eff.
- **Drapeau 1** « historique insuffisant » : faux dans les deux strates (l.435794).
- **Drapeau 2** « co-défaillance observée non expliquée par les axes R2 » : **ÉTEINT** (l.435795). Par le pt 10, le
  drapeau est éteint dès que « R1 discrimine » est FAUX ; ses entrées sont imprimées (l.435797), strate poolée exclue.
  Le drapeau est un signal sur A(axis-coverage), jamais la règle (pt 10).

### 4.2 R2 en résumé (bloc 5)

- **(a) Axe ASN** (l.435673-435691) : 10 hôtes, un relevé retenu chacun, le dernier (2026-09-28T01:17:55Z à
  01:18:02Z), résolveur `cloudflare-dns.com`, attribution croisée RIPEstat et Team Cymru « concordant » pour les 10.
  Un recouvrement mesuré :
  AS13335 partagé par `api-pub.bitfinex.com`, `api.coingecko.com`, `api.exchange.coinbase.com`, `api.kraken.com`,
  `coins.llama.fi`, `ethereum-rpc.publicnode.com` et `www.okx.com` (l.435691). Chaînes CNAME imprimées : binance vers
  CloudFront, gemini vers un équilibreur AWS, bitstamp vers Incapsula, okx vers le CDN de Cloudflare (l.435678,
  l.435682, l.435687, l.435689).
- **(b) Axe contenu** (l.435693-435752) : 35 982 fenêtres ; N_min = 300 fenêtres communes par paire (choix de
  conception) ; seul critère de fusion v0 : identité exacte (T = 1) sur au moins N_min fenêtres communes (l.435695).
  Aucune paire n'est fusionnée sur cet axe : la liste des copies exactes du recalcul tiers est vide (RT l.10991). Les
  statistiques par paire (ρ_raw, ρ_resid, T, T_Δ, co-aberrance, décalage) sont descriptives ; l'écart de peg USDT/USD
  est porté par ρ_resid (J28 l.47). La dépendance sérielle sur cet axe est hors portée (SHOGEN-CONTENU-DEP-1, §11).
- **(c) Axe méthode** (l.435754-435764) : cinq entrées `basis:doc` (trois arêtes d'amont : binance → coingecko, coinbase → pyth, coingecko → defillama ; deux déclarations d'estimateur : coingecko, pyth), qui déclenchent (b) et ne partitionnent pas.
- **(d) Corrélations entre clusters** : le rendu imprime « aucun cluster à ≥ 2 flux (1) → tout reste au φ par paire de
  flux (bloc 4) » (l.435767). Le JSON du recalcul tiers porte, pour le J28, `"cluster_pairs": {}` et
  `"n_multi_clusters": 1` (RT l.10985-10987). [constat du rapport] Le libellé se lit mal à côté du bloc 6, qui nomme un
  cluster de huit flux : la partition compte un seul cluster d'au moins deux membres, donc aucune paire de tels
  clusters, et l'estimateur principal de D3 entre clusters (corrélation des séries Θ̂, analogue de l'éq. 35 de L&M)
  n'a pas d'objet sur le J28.
- **(e) Les sept résidus de l'axe ASN** sont imprimés avec la table (l.435769-435776), notamment : le fronting (k_eff
  compté côté livraison), la mono-vantage, l'instantanéité (attribution datée, re-mesurée à chaque quorum), et le
  chemin de mesure qui appartient à la classe mesurée.

### 4.3 Divergences ASN pour des hôtes hors du pool (SHOGEN-ASN-DIVERGENCE-HORS-POOL-1, annexe B.44)

Aucune divergence ASN n'apparaît dans les rendus. Une recherche de la chaîne `DIVERGENCE` donne 0 ligne dans J14p,
J14s, J28, RT et RAW, et une seule dans SUITE, qui est un nom de test (SUITE l.379) ; le JSON du recalcul tiers porte
`"asn_divergences": []` dans ses quatre entrées (RT l.4522, l.8900, l.13335, l.18099). Il n'y a donc aucune ligne à
étiqueter ni à retirer : le cas que l'item prévoyait (relevés d'hôtes retirés par D1 cas (a), c'est-à-dire de Pyth) ne se
présente pas dans ces rendus.

### 4.4 Caveats du chemin de lecture (RPC)

- Chainlink est lu par `eth_call` sur le RPC public `ethereum-rpc.publicnode.com` (doc 10 §1, non-objet 4 ; J28
  l.435685). Le rendu le dit : « chemin de LECTURE ≠ amont (§3.2) : l'ASN mesuré est celui du fournisseur RPC
  (ethereum-rpc.publicnode.com), une infrastructure de lecture, pas l'amont du feed » (l.435789). Le classement de
  chainlink dans le cluster AS13335 porte donc sur l'infrastructure de lecture.
- Même règle pour tout hôte servi derrière un CDN : l'IP observée est la couche de livraison, pas l'origine (résidu 1,
  l.435770).
- Pyth, lu par un service HTTP qui a répondu 401 dès le premier jour (ADR l.25), est hors du pool d'analyse (§2.2) :
  aucune mesure de ce rapport ne porte sur lui.

## 5. Descriptifs pré-enregistrés (annexe D.5, paquet §11), hors décision

Ces traitements sont descriptifs, hors décision et sans paramètre ; aucun n'entre dans la règle ni dans la liste fermée
des sensibilités (paquet §11 ; libellé imprimé, J28 l.435524).

### 5.1 τ observé contre τ committé (SHOGEN-TAU-REDERIV-1)

Le τ committé avant la campagne sert à tous les confirmatoires ; le τ observé est défini d'avance : P99 et maximum de
|p − médiane_LOO|/médiane_LOO des cellules (fenêtre, flux) arrivées à l'axe hors-enveloppe, par classe, sur le segment,
sans ré-estimation (J28 l.435525 ; paquet §11).

| classe | τ_classe (committé) | N cellules | P99 observé | maximum observé | J28 |
|---|---|---|---|---|---|
| `agregateur` | `0.026` | 71395 | `0.0029870446819581321147177994146356252452815395638463` | `0.017649908208186827670019929236496737002324764533848` | l.435526 |
| `oracle_chainlink` | `0.0165` | 35800 | `0.0045133817598667881395689083527158792588820593853894` | `0.017842859661860400175061719273882056236385914669308` | l.435527 |
| `oracle_pyth` | `0.0015` | 0 | non défini | non défini | l.435528 |
| `place_horodatee` | `0.0045` | 179097 | `0.00084986241659292805372128990214331880618269790009557` | `0.0031005971796576586758169290273558058198265570013814` | l.435529 |
| `sans_horodatage` | `0.0045` | 107367 | `0.0016680227037502354455795456531406013037374194387754` | `0.0084293722922191923975621436933888192128120065521140` | l.435530 |

[calc] Le P99 observé est sous τ_classe dans les quatre classes définies (rapports P99/τ ≈ 0,115 ; 0,274 ; 0,189 ;
0,371). Le maximum observé dépasse τ_classe pour `oracle_chainlink` (≈ 1,08 τ) et `sans_horodatage` (≈ 1,87 τ), ce
qui est cohérent avec les cellules hors-enveloppe comptées au bloc 3 (chainlink et bitfinex, 2 chacune en calme,
§3.5). Une divergence entre τ observé et τ projeté est une trouvaille, pas un re-tune silencieux (ADR-0022 pt 3, cité
par le paquet §12 pt 13) ; la re-dérivation est PX-Shogen-13, après le rendu, jamais appliquée aux z confirmatoires. Réserve déjà écrite
(annexe B.45, note à PX-Shogen-13) : le τ observé (axe hors-enveloppe atteint) et le P99 de calibration (toutes
cellules évaluables) ne portent pas sur la même population.

### 5.2 Décomposition de K par lectures `panne_transport` (SHOGEN-HOST-DEGRADED-1)

Lignes J28 l.435531 à l.435533, recopiées par extraction :

```text
    décomposition de K (SHOGEN-HOST-DEGRADED-1) par nombre de lectures présentes au statut panne_transport (model.Status) des flux du pool D1 de la strate ; c_s = fenêtres où chaque flux du pool porte une lecture panne_transport ; le z confirmatoire inclut les modes communs de l'observateur (hôte, DNS, réseau)
    « calme » : K = 154 = K[≥ 2 panne_transport] 153 + K[1] 1 + K[0] 0 ; K[tous les écarts hors_enveloppe] = 0 ; c_s = 9
    « stress » : K = 133 = K[≥ 2 panne_transport] 133 + K[1] 0 + K[0] 0 ; K[tous les écarts hors_enveloppe] = 0 ; c_s = 0
```

En calme, 153 des 154 fenêtres comptées dans K portent au moins deux lectures au statut `panne_transport` parmi les
flux du pool de la strate, une en porte une, aucune n'en porte zéro ; en stress, les 133 en portent au moins deux.
Aucune fenêtre de K n'a tous ses écarts sur l'axe hors-enveloppe. c_s, nombre de fenêtres où chaque flux du pool porte
une lecture `panne_transport`, vaut 9 en calme et 0 en stress. Ce descriptif n'identifie aucune cause : il décrit la
composition de K, que la règle ne lit pas. La sensibilité qui retire les fenêtres à diagnostic d'hôte dégradé est un
item d'après l'exécution, non fait à la date du rapport (SHOGEN-HOST-DEGRADED-2, §11).

### 5.3 Censure : fenêtres sautées et bornes non extérieures (SHOGEN-CENSURE-INFO-1)

Les fenêtres sautées sont comptées au §2.6 (J28 l.37-41). Sous l'hypothèse H_perte (A(loss-non-informative) : les
pertes d'outillage sont non informatives), le rendu imprime des bornes à P̂_more fixé, avec s = fenêtres sautées de la
strate : z_bas = (K − (n+s)·P̂)/√((n+s)·P̂(1−P̂)) et z_haut = (K + s − (n+s)·P̂)/√((n+s)·P̂(1−P̂)), puis les mêmes avec
σ̂_bloc,s au dénominateur (J28 l.435535). Ligne d'en-tête imprimée : « bornes à P̂_more fixé, non extérieures ; verdict
non identifié sous censure arbitraire des fenêtres sautées » (l.435534).

| strate | s (fenêtres sautées) | z_bas | z_haut | z_bas avec σ̂_bloc | z_haut avec σ̂_bloc | J28 |
|---|---|---|---|---|---|---|
| calme | 5701 | `17.556689997555283653681146237762934756839540547496` | `905.50199539544630203447432173216643843074844907832` | `1.8196629136861220471711460494461585204157608817430` | `93.850742908789397830496314603025603356370670497401` | l.435536 |
| stress | 2094 | `25.473078564141066684303998709584385344769540455886` | `496.61005684969625124835679931557781942595489865145` | `1.6982937424929091779945784909896792520918497568624` | `33.109062569066257260750656346574928093519208266497` | l.435537 |

Ces bornes sont étiquetées « non extérieures » et ne portent aucune lecture d'identification (annexe D.5 ; CV2-24) :
imputer un écart à une fenêtre censurée élève aussi P̂_more, si bien que la borne basse n'est pas extérieure. Les
comptes de pertes mesurent l'ampleur de la censure, pas son caractère non informatif (paquet §12 pt 14). Les bornes
extérieures sont l'item SHOGEN-CENSURE-INFO-2, après l'exécution (§11).

### 5.4 Diagnostic de runs de I_t et FIV

- Runs de I_t = 1{m_t ≥ 2} (hors décision ; J28 l.435497, l.435501) : en calme, 119 runs, longueur moyenne
  `1.2941176470588235294117647058823529411764705882353`, run maximal 6 ; en stress, 130 runs, longueur moyenne
  `1.0230769230769230769230769230769230769230769230769`, run maximal 2. [calc] La longueur moyenne est K_s divisé par le
  nombre de runs (154/119 et 133/130).
- Le run maximal reste sous ℓ = 240 dans les deux strates : le drapeau « run maximal ≥ ℓ : σ̂²_bloc,s biaisé vers le
  bas ; SHOGEN-DEP-FENETRES-2 prioritaire avant G10 » (pt 9) n'est pas imprimé ; dans le J28, la locution n'apparaît
  que dans l'étiquette de tête (l.1).
- FIV_s et ses deux facteurs sont au §3.1 (l.435495, l.435499) ; le coefficient de variation théorique de σ̂²_bloc,s,
  √(4ℓ/(3n)), vaut `0.11408797792643129814123654880491384644099142081780` en calme et
  `0.16756361261114975367661284639462247100481161298594` en stress (l.435494, l.435498), marqué « [inféré : dérivation
  de l'AVIS-advisor-defi Q1 (iv)] » par le rendu (l.435493).

## 6. Lift et identité φ de D3 (SHOGEN-D3-LIFT-1, annexe B.42)

D3 (paquet §5, recopié pour l'essentiel) : entre singletons de la partition R2, φ des indicatrices d'écart reste
l'estimateur principal ; pour les paires de singletons (tables 2×2), le lift (membre gauche de l'éq. 28 de L&M) est un
secondaire déclaré ; « Aucune significativité par paire : c'est du descriptif » ; il faut publier l'identité
φ = (lift−1)·√(p_A p_B / ((1−p_A)(1−p_B))), « qui rend exacte la mention “proxy bruité” », et les quatre comptes par
paire. Les rendus ne calculent pas le lift (constat B-2 de la relecture R-B, annexe B.42) : il est recalculé ici par le
rédacteur, en arithmétique exacte, à partir des seuls quatre comptes imprimés au bloc 4 du J28.

- **Paires concernées** : la partition du J28 compte trois singletons, {binance}, {gemini} et {bitstamp} (J28 l.435790,
  l.435792, l.435793), donc trois paires de singletons par strate.
- **Définitions** : n = n11 + n10 + n01 + n00 ; p_A = (n11 + n10)/n ; p_B = (n11 + n01)/n ; lift = p_AB/(p_A·p_B) =
  n11·n/((n11 + n10)(n11 + n01)) ; φ = (n11·n00 − n10·n01)/√((n11 + n10)(n01 + n00)(n11 + n01)(n10 + n00)).
- **Méthode** : script `d3_lift.py` (bibliothèque standard, `fractions` et `decimal` à 80 chiffres), remis avec ce
  rapport (sha256 `8f91474cdded5694e733334fadf225b110d3378ddb560f1bee4066eca80f9381` ; sortie `d3_lift.sortie.txt`,
  sha256 `77ae69ec8666065d0e7ec3a13588f982d87de7bf1789ffe3f91813ea028dc73f`). L'identité est contrôlée exactement : φ²
  et (lift − 1)²·p_A·p_B/((1 − p_A)(1 − p_B)) sont deux rationnels égaux, et φ a le signe de lift − 1. Auto-test sur
  deux tables calculées à la main ([2 1 1 6] : lift = 20/9, φ = 11/21 ; [0 5 5 90] : lift = 0, φ = −1/19), qui échoue
  sous une identité mutée.

[calc] Sortie du script, mise en table (`table_lift.py`, réécriture de chaînes) ; le lift exact est une fraction
irréductible, ses décimales sont arrondies à 12 chiffres significatifs :

| strate | paire | [n11 n10 n01 n00] (J28) | p_A ; p_B | lift (exact) | lift ≈ | √(p_A·p_B/((1−p_A)(1−p_B))) ≈ | (lift − 1)·√(…) ≈ | φ imprimé (bloc 4) | identité exacte |
|---|---|---|---|---|---|---|---|---|---|
| calme | binance×bitstamp | [52 320 423 23790] (l.435547) | 124/8195 ; 95/4917 | 21307/2945 | 7.23497453311 | 0.0173978414435 | 0.108475098331 | `0.10847509833108362918259591106802162184159185904700` | oui |
| calme | bitstamp×gemini | [21 454 47 24063] (l.435551) | 95/4917 ; 68/24585 | 103257/6460 | 15.9840557276 | 0.00739211972867 | 0.110763933959 | `0.11076393395917706370581636186843800964431146805970` | oui |
| calme | binance×gemini | [20 352 48 24165] (l.435552) | 124/8195 ; 68/24585 | 40975/2108 | 19.4378557875 | 0.00652781686160 | 0.120358945901 | `0.12035894590128557980983967111642447373272429106910` | oui |
| stress | binance×bitstamp | [4 42 35 11316] (l.435622) | 46/11397 ; 13/3799 | 7598/299 | 25.4113712375 | 0.00373029540546 | 0.0910616259682 | `0.091061625968168214579556752802535961836177686365615` | oui |
| stress | binance×gemini | [3 43 18 11333] (l.435624) | 46/11397 ; 7/3799 | 11397/322 | 35.3944099379 | 0.00273512204339 | 0.0940729087904 | `0.094072908790429061895721354843595547904877588394058` | oui |
| stress | bitstamp×gemini | [3 36 18 11340] (l.435627) | 13/3799 ; 7/3799 | 3799/91 | 41.7472527473 | 0.00251765505523 | 0.102587526866 | `0.10258752686577574340266708561888701645711988440463` | oui |

En lecture arrondie [calc] : lift ≈ 7,23 ; 16,0 ; 19,4 en calme et ≈ 25,4 ; 35,4 ; 41,7 en stress, pour des φ imprimés
de ≈ 0,108 à ≈ 0,120 en calme et de ≈ 0,0911 à ≈ 0,103 en stress. Le facteur √(p_A·p_B/((1−p_A)(1−p_B))) est petit à
marges faibles (de ≈ 0,00252 à ≈ 0,0174 ici), et lift − 1 vaut φ divisé par ce facteur : c'est la relation que le
paquet publie pour rendre exacte la mention « proxy bruité ». Aucune lecture de décision n'en est tirée, aucune
significativité par paire n'est calculée, et l'odds ratio conditionnel, exploratoire et sans méthode fixée au
scellement, n'est pas calculé (paquet §5).

Contrôle des 110 tables du bloc 4 [calc] : l'identité est exacte sur 110 tables sur 110 (55 par strate), et φ recalculé
diffère de φ imprimé d'au plus 2,38·10⁻⁵⁰ en valeur absolue (sortie `d3_lift.sortie.txt`, l.2-3). Le lift n'est
publié que pour les paires de singletons, seules visées par D3.

## 7. Sorties hors décision (paquet §10.2 pt 9)

Le pt 9 les énumère : J14 principal et second (non confirmatoires), strate poolée (exploratoire), sensibilités « plage
incluse » (biaisée vers le haut par construction) et « seconde coupe », L&M (bloc 4), queues exactes, diagnostic de
runs. **Aucune ne change le verdict** : la règle est évaluée sur le seul J28, plage D5 exclue (pt 1), et « R1
discrimine » y vaut FAUX (§3.3). Chaque sortie est reproduite avec l'étiquette que le rendu imprime en tête.

### 7.1 J14 principal

Étiquette (J14p l.1) :

```text
[ÉTIQUETTE] j14-principal : hors décision, non confirmatoire (ADR-0028 D4, §1 bis.1 pt 9) ; plage D5 non passée : hors du segment (D2 pt 6 l'applique au J28)
```

Segment `[1787770800 ; 1788980400) = [2026-08-26T19:00:00+00:00 ; 2026-09-09T19:00:00+00:00)` (J14p l.31), règle ex
ante d'ADR-0022 pt 5 (D4) ; Pyth retiré des deux strates, cas (a) : 0 lecture `ok` sur 13 373 et sur 3 941 (l.38-39) ;
fenêtres sautées 1 027 et 1 819 (l.33).

| J14p : grandeur | calme | stress | J14p |
|---|---|---|---|
| n_s | `13373` | `3941` | l.209555 ; l.209575 |
| K_s | `50` | `8` | l.209555 ; l.209575 |
| P̂_more,s | `0.0013938968610775433013870221315659599986142913741574` | `0.00035260783541832319883608669380651774613270860280165` | l.209571 ; l.209591 |
| garde (seuil 10) | `18.614599673443475762938726299057869492601437469783` | `1.3891374858460684507352497516803467029217226329697` | l.209572 ; l.209592 |
| z_s | `7.2684387263613165124682538101673599947301495076272` | non publié (garde §5.4) | l.209573 ; l.209593 |
| z_bloc,s | `2.6455172861617278377464936516549168389991781470697` | non publié (garde de blocs, n_s < 7200) | l.209601 ; l.209605 |
| valeur de la règle (hors décision) | REJETTE | NON ÉVALUABLE : strate non testée, hors décision (§1 bis.1 pt 2) | l.209620 ; l.209622 |

Lignes de la règle (J14p l.209619 à l.209623), recopiées par extraction :

```text
  ── règle SHOGEN-CRITERE-R1-1 (ADR-0028 §1 bis.1 pts 1-11 ; forme scellée) : valeur par strate ; comparaisons sur les Decimal publiées, non arrondies, au seuil 2.33, « ≥ » ; aucune p-valeur
    « calme » : z_s = 7.2684387263613165124682538101673599947301495076272 ≥ 2,33 ; z_bloc = 2.6455172861617278377464936516549168389991781470697 ≥ 2,33 → REJETTE
    « calme » : « le modèle d'indépendance du pool (k nominal_s = 11 flux du pool de la strate, bloc 1 ; k_eff mesuré ≤ 10 (borne supérieure), bloc 6) est rejeté dans la strate calme sur 13373 fenêtres, axes panne / staleness / hors-enveloppe (résidu : staleness fail-open : binance, kraken, bitfinex), tel qu'observé par cet instrument (hôte, DNS et réseau du harnais compris) ; aucune dépendance de paire n'est établie »
    « stress » : z_s non publié (garde §5.4 : n·P̂_more·(1 − P̂_more) < 10) → NON ÉVALUABLE : strate non testée, hors décision (§1 bis.1 pt 2)
  « R1 discrimine » (§1 bis.1 pt 6 ; déclencheur de D6 (vi) et D9) = VRAI : strate(s) qui rejettent : calme
```

La famille compte m = 1 (l.209608) ; la strate poolée n'est pas publiée, la strate de stress étant sous la garde
(l.209614). Au bloc 6, les dix relevés ASN retenus en fin de segment (2026-09-09T18:49Z à 18:51Z) sont tous en
`resolve_failed` (J14p l.209777-209786) : k_eff n'est connu que comme borne supérieure, « k_eff ≤ 10 (BORNE
SUPÉRIEURE) » (l.209876) ; drapeau 1 vrai en stress seulement (l.209907) ; drapeau 2 non évaluable, « ni levé ni
éteint » (l.209908-209909), par la lecture (a) du pt 10. Le J14 est non confirmatoire et sa publication est une
décision de l'investisseur (D4 ; décision 270). **Ce « R1 discrimine » VRAI est hors décision et ne change pas le
verdict** (pts 1 et 9).

### 7.2 J14 second (sensibilité « seconde coupe »)

Étiquette (J14s l.1) :

```text
[ÉTIQUETTE] j14-second : sensibilité de la liste fermée (seconde coupe, décision 270), hors décision, non confirmatoire ; plage D5 non passée : hors du segment (D2 pt 6 l'applique au J28)
```

Segment `[1787770800 ; 1788480060) = [2026-08-26T19:00:00+00:00 ; 2026-09-04T00:01:00+00:00)` (J14s l.31), coupe
« ≤ 2026-09-04T00:00Z » de la décision 270 (D4) ; Pyth retiré des deux strates, cas (a) (l.38-39).

| J14s : grandeur | calme | stress | J14s |
|---|---|---|---|
| n_s | `8121` | `1140` | l.112112 ; l.112133 |
| K_s | `5` | `1` | l.112112 ; l.112133 |
| P̂_more,s | `0.000014316253783038939038177418104725077784697432524987` | `0.000021469618207937163532218656623490189731153357463892` | l.112128 ; l.112149 |
| garde (seuil 10) | `0.11626063253151037288958691789311493515448564399261` | `0.024474839280311532597570565581073686929332258857146` | l.112129 ; l.112150 |
| z_s | non publié (garde §5.4) | non publié (garde §5.4) | l.112130 ; l.112151 |
| z_bloc,s | `2.0943484839416630978298953875433710863142063001875` | non publié (garde de blocs, n_s < 7200) | l.112159 ; l.112163 |
| valeur de la règle (hors décision) | NON ÉVALUABLE : strate non testée, hors décision (§1 bis.1 pt 2) | NON ÉVALUABLE : strate non testée, hors décision (§1 bis.1 pt 2) | l.112178 ; l.112179 |

Les deux strates sont sous la garde §5.4, donc non testées : « R1 discrimine » = NON ÉVALUABLE, « aucune strate
testée » (J14s l.112180) ; m = 0 (l.112166). En calme, z_bloc est imprimé (garde de blocs tenue, n_s ≥ 7 200), mais la
valeur de la strate reste NON ÉVALUABLE, la garde §5.4 primant (pt 5). Bloc 6 : k_eff = 4 pour k nominal = 10
(l.112437-112438), partition datée du 2026-09-03T23:56:54Z au 23:57:06Z (l.112439) ; drapeaux 1 vrais dans les deux
strates (l.112452) ; drapeau 2 non évaluable (l.112453-112454). **Hors décision ; ne change pas le verdict.**

### 7.3 Strate poolée (exploratoire, hors famille, hors décision)

Sur le J28, forme stratifiée de D2 pt 4, chaque strate sur son pool D1 (J28 l.435505-435510) :

- z_pool = `33.435366780260737654814166344529336014557255168635` (l.435510) ;
- Σ_s (K_s − n_s·P̂_more,s) = `236.77931489141074698973370238916004307092589875631` et
  Σ_s n_s·P̂_more,s(1 − P̂_more,s) = `50.150507915819141795538676919575811501998150245996` (l.435509).

Lecture : z_pool ≈ 33,4 ([calc] recompté à 33,4353667803 depuis les deux sommes imprimées). La strate poolée n'est
jamais dans les entrées de la règle ni dans celles du drapeau 2 (pt 9 ; « strate poolée hors des entrées », l.435797).
Son approximation normale n'est pas mesurée (SHOGEN-POOLEE-BLOC-1, §11). Elle n'est publiée dans aucun des deux J14
(strates sous la garde, J14p l.209614, J14s l.112172). **Hors décision ; ne change pas le verdict.**

### 7.4 Sensibilité « plage incluse » (liste fermée, D2 pt 7)

Section [SENSIBILITÉ] du J28 (l.435799-435820). Libellé imprimé : « variante “exclue” = principale (blocs 1-6) ;
variante “incluse” = sensibilité — biaisée vers le haut par construction ; documente l'exclusion D5 ; pas un
estimateur alternatif » (l.435800, guillemets intérieurs rendus par “ ”) ; « motif de l'exclusion (harnais dégradé,
ADR-0025) : causalité non établie » (l.435801). R1 seul par variante, ni L&M ni R2 (l.435802).

| strate | variante | n | K | P̂_more | z | drapeau 1 | J28 |
|---|---|---|---|---|---|---|---|
| calme | exclue (principale) | 24585 | 154 | `0.0013629504227977629135010363906355205959215005903986` | `20.829495417808173515660354538360738280133057485734` | False | l.435807 |
| calme | incluse (sensibilité) | 26294 | 408 | `0.0039561837661865178605964292161309130218132671860844` | `29.863015876556250088619968054838673686543339634366` | False | l.435808 |
| stress | exclue (principale) | 11397 | 133 | `0.0014663989614904143004161900453685779659861375123928` | `28.466243694685921454102240881955034913016073716310` | False | l.435810 |
| stress | incluse (sensibilité) | 12306 | 133 | `0.0013272367906723694408097789913642102856351014485357` | `28.887094091051972755366700337792595909958417732478` | False | l.435811 |

- Écart de z (incluse − exclue) : `9.033520458748076572959613516477935406410282148632` en calme (l.435809),
  `0.420850396366051301264459455837560996942344016168` en stress (l.435812).
- Pertes par type retirées par la plage (SHOGEN-DP-JOURNAL-LOSS-1, l.435803-435806) : celles du §2.4, plus, dans la
  plage, 73 fenêtres de grille sans marqueur en calme et 0 en stress, et aucune lecture absente des fenêtres à marqueur
  (pool D1 de la variante incluse).
- Couverture par week-end : §2.5 (l.435813-435820).
- Le recalcul tiers rend aussi la variante incluse du J28, sous l'étiquette d'entrée
  `sensibilité « plage incluse » de la liste fermée (D2 pt 7), hors décision, biaisée vers le haut par construction`
  (RT l.13924). Il y imprime z_bloc `2.5084623121105959997807452114411311466491022293836` en calme (RT l.14934) et
  `1.7478959678777101321272619734145717678436022586316` en stress (RT l.15167), et, dans le drapeau 2 de la variante,
  `"r1_discrimine": "VRAI"` (RT l.18045), `"rejette": ["calme"]` (l.18047-18049) et l'état `eteint` (l.17705),
  avec la raison imprimée à la l.18046 (recopiée ci-dessous). [constat du rapport] Le paquet §7 évitait un rendu
  complet de cette variante, qui imprimerait « R1 discrimine » sans étiquette (contre le pt 9) ; le JSON du recalcul
  tiers porte cette clé pour la variante, étiquetée au niveau de l'entrée seulement. **Hors décision, biaisée vers le
  haut par construction ; ne change pas le verdict.**

```text
    "raison": "« R1 discrimine » VRAI (strate(s) : calme) mais k_eff = 4 < k nominal du segment = 10 : recouvrement R2 mesuré explique au moins en partie la co-défaillance",
```

### 7.5 L&M (bloc 4)

Fonction de difficulté Θ sur N = 11 flux, pool d'analyse D1 (J28 l.435539) ; corrélations φ signées par paire de flux,
matrice de co-écarts complète, « Cov<0 possible » (l.435544, l.435546).

| L&M (bloc 4) | calme | stress | J28 |
|---|---|---|---|
| Σ mⱼ | 1451 | 693 | l.435541 ; l.435606 |
| Ê(Θ) | `0.0053654297705548468208626841939837668940780594227818` | `0.0055277704659120821268754935509344564359041853119242` | l.435542 ; l.435607 |
| Ê(Θ²) | `0.00058498345258564904690591084733854715550871743672239` | `0.0011262932031555353482176330294256064195521947561954` | l.435543 ; l.435608 |
| Var̂(Θ) | `0.00055619561596289281070470998663090781236412718685660` | `0.0010957369568317254707066076636531337727625164483380` | l.435544 ; l.435609 |
| φ définies / 55 | 55 | 55 | l.435545 ; l.435610 |
| paires à co-écart (n11 > 0) | 55 | 50 | l.435545 ; l.435610 |

Les φ les plus élevés sont, en calme, kraken×bitfinex et okx_ticker×okx_index (≈ 0,454 et ≈ 0,452 ; l.435563,
l.435548) ; en stress, coingecko×chainlink (≈ 0,901 ; l.435614), kraken×bitfinex (≈ 0,763 ; l.435621),
defillama×chainlink (≈ 0,691 ; l.435613) et coingecko×defillama (≈ 0,686 ; l.435612). Cinq φ sont négatifs en stress,
aucun en calme (l.435662-435666). Ce sont des descriptifs : aucune significativité par paire (D3), aucune dépendance
de paire établie. **Hors décision ; ne change pas le verdict.**

### 7.6 Queues exactes

Sous la garde §5.4, les rendus impriment la queue binomiale exacte hors décision (J14p l.209594 ; J14s l.112131,
l.112152) ; aucune strate du J28 n'est sous la garde, et aucune queue n'y est imprimée. Ces valeurs ne sont pas
recopiées ici (conventions de lecture). **Hors décision ; ne changent pas le verdict.**

## 8. Contrôles de l'exécution

### 8.1 Sceau

- **Paquet** `docs/adr-0028/PAQUET-PREREG-S2.md`, commit `3be95be`, sha256
  `4d2a8276316b1c66a08aabb15ff3b39be812978e93dafc01a4e627f20d0af528`, écrit au JOURNAL le 2026-10-03 à 01:02:51 UTC
  (JOURNAL l.304 ; `docs/adr-0028/sceau/README.md`). [calc] sha256 recompté égal le 2026-10-04.
- **Manifeste** horodaté `docs/adr-0028/sceau/PAQUET.sha256`, sha256
  `519423510b21ecbebda895d6e225ab0748fb0fe5a2b257a36c9301e36bfaa3e9` (recompté égal).
- **Jeton RFC 3161 de FreeTSA** `paquet.tsr`, sha256 `9edb19b53379f370e291c5da01d4df3bc269b67a44feddb589d1211ec5ec6b0e`,
  série `0x08CFC8D5`, **genTime 2026-10-03T01:04:10Z**, horloge de FreeTSA (README du sceau ; JOURNAL l.306). Rejoué
  par le rédacteur le 2026-10-04 : `openssl ts -reply -in docs/adr-0028/sceau/paquet.tsr -text` imprime
  `Time stamp: Oct  3 01:04:10 2026 GMT` ; `bash scripts/sceau/verify.sh` sort 0, avec
  `docs/adr-0028/PAQUET-PREREG-S2.md: OK` (le manifeste recontrôle les octets du paquet) et `Verification: OK` deux fois
  (le jeton contre la requête, puis contre les octets du manifeste et la chaîne de FreeTSA). L'avertissement d'OpenSSL
  “is not a CA cert” porte sur `tsa.crt`, passé en certificat de signature et non en autorité.
- **Délai de rétractation** (A-7) : 24 h depuis genTime, échéance 2026-10-04T01:04:10Z (README du sceau).
- **Ouverture** : go de l'investisseur, verbatim « go exécution », consigné le 2026-10-04 à 01:06:36 UTC, après
  l'échéance (JOURNAL l.310) ; voie (a) (jeton), T0 = genTime (JOURNAL l.314).
- **Premier sceau, cité** : paquet `494d770d704dc7c342f0c6deec269e5642b3621bf451922f991e4ca1fb968097` (commit
  `ddf8c54`), manifeste `680a95fdf50908cea797ae4fe9f0b42c43b5a99fcad755cb410e26fa6e794209`, jeton série `0x08CC76D7`,
  genTime 2026-10-02T17:44:30Z (`docs/adr-0028/sceau/premier-2026-10-02/README.md` ; [calc] sha256 du manifeste et
  genTime relus égaux). Il est cité parce que la règle A-8 l'exige : un sceau remplacé avant l'exécution reste cité
  (« le premier sha reste cité », ADR §1 bis.8 ; paquet §9). Il a été remplacé avant toute exécution (§10.3) et
  n'ouvre plus aucune exécution (README du premier sceau, ajout daté du 2026-10-03).
- **Ce que le sceau n'atteste pas** : le jeton atteste l'existence des octets du manifeste au plus tard à genTime,
  rien de plus, et rien sur des lectures antérieures des données (annexes D.1, D.3) ; il se contrôle sous confiance en
  FreeTSA, opérateur individuel, sans accord de niveau de service lu ; l'ancre de durabilité OpenTimestamps n'est pas
  faite (README du sceau ; paquet §12 pt 16).

### 8.2 Gardes (annexe D.4 b ; paquet §9)

- `--gardes-seules` sur les journaux réels à 01:11:19 UTC : « gardes levées », sortie 0 ; production lancée à
  01:11:27 UTC, processus 943, auteur `claude-opus-5-5`, tête gardée `27b0e303f196699959bddc2607db6a1d808ce0db`,
  voie (a) (JOURNAL l.314).
- Rejeux en lecture seule par le rédacteur, le 2026-10-04 : garde (1), le sha256 du paquet figure au JOURNAL de la tête
  gardée, l.304 (`git show 27b0e30:JOURNAL.md`, sha seul affiché) ; garde (2),
  `git diff --quiet f35a70c 27b0e30 -- s2-harness/shogen_s2 s2-harness/tools` sort 0 (de même contre les têtes
  `81c5ad7` et `25406c8` de la branche pendant la rédaction du rapport), et `f35a70c` est ancêtre de `27b0e30` ; garde (4), le sha256 de
  `s2-harness/tools/rendu_unique.py` au commit `f35a70c` vaut `06d189cf84e7dca97bdfc0e1b695fc827a09473779505c7a8f1af1e7c26e9050`,
  égal à la clé `sha256_script` du bloc machine (paquet l.216). La garde (4) est une garde contre l'édition
  accidentelle, pas une preuve (paquet §9).
- Garde (3) : sha256 des journaux téléchargés égaux au bloc machine et au fichier de sommes (JOURNAL l.312 ; §8.3).

### 8.3 Journaux et sorties

- Journaux scellés (bloc machine, paquet l.217-219 ; JOURNAL l.312) : `control.jsonl`
  `351f51b2e4b7421b4ee286c27465cde239124d6edd70c0e550741d22f83366ff` ; `journal.jsonl`
  `98c5793ec460e3c009b7f743796800ae7259f71c65a4063a3c315e8eea595d74` ; `raw.jsonl`
  `39ffb13fb0e5939ff88285ce256fbd416b0665c20ee6394c512eed7d2175c15d` ; fichier de sommes de clôture
  `70910984076474987239d8c7a9da786acc95c38b375ad572d78afa297bf8caf4` (paquet l.220). Téléchargés de Drive sans aucun
  affichage de contenu, tailles 41 676 139, 148 930 880 et 204 107 558 octets égales aux attendues, sha256 égaux
  (JOURNAL l.312).
- Sorties : les sept sha256 de la table des conventions, recomptés par le rédacteur, sont égaux à ceux que le JOURNAL
  consigne (l.314) et à ceux des runs de l'enregistrement (ENR l.31-132).

### 8.4 Enregistrement d'oracle (D6 (viii))

ENR, schéma `shogen.oracle-record.v1` (l.138), rôle `rendu` (l.15), auteur `claude-opus-5-5` (l.2), base
`f35a70c19ba8269f1f7e2bcd31775e4fc513da20` (l.3), `ecrit` `2026-10-04T01:11:29Z` (l.4), variable
`SHOGEN_S2_CAMPAGNE_CONTROL` à `null` (l.8), `exit` 0 (l.10), `paquet.sha256` égal au sha du paquet (l.12), Python
`3.11.15` (l.14), `sceau.genTime` `2026-10-03T01:04:10Z` (l.136), `served_from` `null` (l.139), `static_only` `false`
(l.140), `tree.commit` `27b0e303f196699959bddc2607db6a1d808ce0db` extrait par `git archive`, 436 fichiers hachés (l.142 ;
[calc] compte des entrées). Six runs, dans l'ordre `suite`, `j14-principal`, `j14-second`, `j28`, `recalcul-tiers`,
`raw`, chacun de sortie 0 et sans test lancé avec la variable (`tests_avec_variable` vide) (l.31-132). Relu par
`oracle_record.py --verifier … --role rendu --commit 27b0e303…` : « conforme » (JOURNAL l.314).

### 8.5 Suite `s2-harness`

`Ran 398 tests in 62.358s` (SUITE l.621) et `OK (skipped=2)` (l.623). Les deux tests sautés sont les tests de comptes
qui liraient une copie scellée par `SHOGEN_S2_CAMPAGNE_CONTROL` (SUITE l.207, l.209) : la variable n'a pas été posée
(ENR l.8 ; annexe D.4 a).

### 8.6 Oracle `recompute_*` (run `recalcul-tiers`) : ce qu'il établit et ce qu'il n'établit pas

- **Objet** : le JSON des points d'entrée `recompute_*` du chemin de recalcul (ADR-0028 D6 (i) ; oracle tiers
  d'ADR-0003) pour le J14 principal, le J14 second, le J28 et la variante incluse du J28 (RT l.3, l.5048, l.9462,
  l.13897), chacun avec son étiquette (RT l.23, l.5060, l.9489, l.13924) ; aucun avertissement du lecteur
  (`"avertissements": []`, RT l.2).
- **Ce qu'il établit** [calc] : les 126 valeurs comparées (n, K, P̂_more, garde, z, γ̂₀, σ̂²_bloc, cv, FIV et ses
  facteurs, z_bloc, runs, décomposition de K, état du drapeau 2 et « R1 discrimine », pour le J28, le J14 principal et
  le J14 second) sont égales, chaîne pour chaîne, à celles des rendus (`comparer_recalcul.py`, §8.9). Dans cette
  exécution, le chemin de recalcul et le chemin du rapport rendent donc les mêmes valeurs depuis le journal seul.
- **Ce qu'il n'établit pas** : une implémentation indépendante. Les deux chemins appellent les mêmes modules gelés
  (`r1`, `lm`, `r2`, `records`), sous le même Python, sur le même hôte, dans la même exécution : c'est un contrôle de
  cohérence entre deux points d'entrée, pas un recalcul par un code tiers. L'oracle indépendant en arithmétique exacte,
  écrit depuis le texte scellé, a été comparé à `r1` sur 585 journaux synthétiques avant le sceau, avec 0 écart
  (annexe B.43), et non sur les journaux réels. Ce n'est pas non plus le test de composition
  SHOGEN-S2-TUYAU-MONARK-1 : « L'oracle `recompute_*`, rejoué dans l'exécution unique, est un contrôle interne :
  ce n'est pas le test de composition » (ADR §3). Il ne dit rien de la fidélité des journaux aux sources
  (A(history-integrity), doc 08).

### 8.7 Verdict du journal brut

RAW l.1, recopiée par extraction :

```text
verdict raw.jsonl (records.verifier_raw ; SHOGEN-RAW-FIN-1) : refus — lecture(s) de raw.jsonl absente(s) de journal.jsonl : [(1790275920, 'binance', Decimal('1790275970.0000675')), (1790277780, 'binance', Decimal('1790277830.0003345')), (1790283600, 'binance', Decimal('1790283650.0009525')), (1790283840, 'okx_ticker', Decimal('1790283890.0004282')), (1790285940, 'binance', Decimal('1790285990.0001917'))] — refus (SHOGEN-RAW-LECTEUR-1)
```

- Le vérificateur du journal brut refuse (SHOGEN-RAW-LECTEUR-1) : cinq lectures de `raw.jsonl` sont absentes de
  `journal.jsonl`, quatre de binance et une d'okx_ticker. [calc] Leurs `window_start` valent 2026-09-24T18:52Z, 19:23Z,
  21:00Z, 21:04Z et 21:39Z : toutes dans la plage D5 `[1790273880 ; 1790435280]` (`controles_r1.py`), donc hors de
  n, K et P̂_more du J28 (§2.4), et hors des deux segments J14, qui finissent le 2026-09-09 et le 2026-09-04.
- Ce verdict ne ferme pas l'exécution, par construction écrite avant le sceau (paquet §12 pt 1, SHOGEN-RAW-FIN-1) :
  « L'exécution unique imprime et enregistre ce verdict sans qu'il la ferme (run nommé qui sort 0 quel que soit le
  verdict […] ; la liste des gardes de D.4 b est fermée) ». Le run `raw` est sorti 0 (ENR l.126-127).

### 8.8 Durée

Production lancée à 01:11:27 UTC, terminée à 01:33:47 UTC, sortie 0 (JOURNAL l.314), soit 22 min 20 s [calc] ; la
suite a tourné en 62,358 s (SUITE l.621). Une seule exécution, aucune tentative échouée (JOURNAL l.314).

### 8.9 Recomptes du rédacteur [calc]

Scripts du rédacteur, bibliothèque standard Python, remis avec ce rapport. Les trois premiers ont d'abord été lancés
sous une mutation qui doit les faire échouer, puis normalement (journal G1) ; `calc_divers.py` n'a pas de mode mutant :
il fait des opérations élémentaires sur des valeurs recopiées, citées ligne par ligne dans son code.

| script | objet | résultat | sha256 du script ; de la sortie |
|---|---|---|---|
| `controles_r1.py` | depuis les entiers imprimés (écarts par flux, n, K, s) : P̂₀, P̂₁, P̂_more exacts ; z_s, γ̂₀, z_bloc (σ̂² imprimé), FIV et facteurs, cv, EMD_s, bornes de censure, écart de z de la sensibilité, z_pool ; valeur de la règle ; identités entières ; verdict brut contre la plage D5 | écart relatif maximal aux valeurs imprimées 4,21·10⁻⁵⁰ (dernier chiffre de la précision 50) ; valeur de la règle recomptée égale à l'imprimée dans les deux strates | `11779f798b948b155462c7b66460009a0a2c991bb27653c2ad344c6c83744c4f` ; `0469a499233d66cd64031c7cf21e82bf01615658e3f14cc25d8221afe5581e3e` |
| `comparer_recalcul.py` | JSON du recalcul tiers contre les blocs 3 et 6 des rendus | 126 valeurs sur 126 égales à la chaîne près | `4e61cea803c902054e6fcbd2cc6a29f7c71ac1a2f8bfd824aefaa851ebef7585` ; `8e6731f9f3c6f0a73ad2fb7938e66c215dafe1d0c13934f4d6f804d6dd57459e` |
| `d3_lift.py` | lift et identité φ de D3 (§6) | identité exacte sur 110 tables sur 110 ; écart à φ imprimé ≤ 2,38·10⁻⁵⁰ | `8f91474cdded5694e733334fadf225b110d3378ddb560f1bee4066eca80f9381` ; `77ae69ec8666065d0e7ec3a13588f982d87de7bf1789ffe3f91813ea028dc73f` |
| `calc_divers.py` | racines, durée, sommes, rapports τ, z_pool, gardes des J14, sommes des écarts par type | valeurs citées [calc] dans le texte | `4d210cb65fb56fc5c0ef00ec31480bbe96426746191c5efa38a9e2def99a1c98` ; `de7bd825bba4e71aeac9437dfafa26eb3101d00c3d1ea0b992b103c33f4c52af` |

σ̂²_bloc,s n'est pas recalculable sans la série I_t, donc sans lire le journal : il est pris tel qu'imprimé, et le
recompte de z_bloc,s ne contrôle que la division par sa racine. Les tables de ce rapport ont été extraites des rendus
par scripts (`extraire_tables.py`, `extraire_d5.py`, `extraire_hd.py`, `table_lift.py`), sans recopie à la main.

## 9. Limites

### 9.1 Limites écrites avec la règle (paquet §10.2, pts 2, 7 et 11)

1. Dépendance sérielle de portée ≥ ℓ non corrigée : σ̂²_bloc,s y est biaisé vers le bas (pt 11).
2. Même sous une portée < ℓ, biais de l'estimateur à poids triangulaires de l'ordre de −ℓ⁻¹·Σ_k |k|·R(k) : sous
   autocorrélations positives, σ̂²_bloc,s sous-estime et z_bloc,s surestime (pt 11, SHOGEN-BARTLETT-BIAIS-1).
3. z_s et z_bloc,s sont conservateurs par le plug-in de P̂_more ; un non-rejet en est moins probant (pt 11 ;
   SHOGEN-R1-PLUGIN-1).
4. Puissance réduite, voire négative, contre un mode commun qui touche toutes les sources, dès que
   Σ_i (∂P_more/∂p_i)(1 − p_i) > 1 − P_more (pt 11 ; SHOGEN-R1-PLUGIN-1).
5. Approximation normale à la garde ; près de la garde, à fenêtres iid, le niveau de z_s seul est mesuré au-dessus de
   0,01 sur données synthétiques, alors que la règle tient (pt 11, SHOGEN-GARDE-NIVEAU-ZSEUL-1 ; §3.4).
6. Niveau asymptotique, non démontré ≤ 0,01 en échantillon fini ; la borne 0,02 vaut sous le modèle nul joint (pt 7).
7. Sous la garde §5.4, écart déclaré à doc 10 §5.4 : la strate n'est pas testée, sa queue exacte est hors décision
   (pt 2).
8. « Aucun auteur de la règle n'a vu z, K, P̂_more ni φ (annexe D.3) » (pt 11), sous les limites de l'inventaire D.1
   et des mesures de l'annexe B.37 (§10).

### 9.2 Limites et procédures écrites au paquet (§12, points 1 à 20)

1. SHOGEN-RAW-FIN-1 : l'oracle du journal brut reste strict ; son verdict est imprimé sans fermer l'exécution (§8.7).
2. SHOGEN-ENREG-G1-1 : l'enregistreur n'extrait qu'un commit ; un enregistrement G1 sur un travail non commis n'est pas
   productible.
3. SHOGEN-ENREG-DELAI-CHAMP-1 : le délai (3 600 s par commande) n'est pas un champ de l'enregistrement ; il ne tue que
   l'enfant direct.
4. SHOGEN-CENSURE-VIVANT-PORTEE-1 : « harnais vivant » veut dire même démarrage avant et après la fenêtre sautée ; une
   mise en veille pendant un démarrage est comptée « vivant ».
5. SHOGEN-RENDU-TABLE-REELLE-1 : la table réelle des sorties n'a jamais tourné de bout en bout sur fixture ; l'exécution
   unique en est la première exécution complète.
6. SHOGEN-RENDU-CLI-REPORT-1 : `python -m shogen_s2.report` rend des journaux sans garde ; procédure : aucun rendu des
   journaux scellés hors de `rendu_unique.py`.
7. SHOGEN-RENDU-JETON-MAIN-1 : le jeton `SHOGEN_RENDU_PRODUCTION` ferme l'appel accidentel de `--produire`, pas l'appel
   délibéré.
8. SHOGEN-RENDU-ORC-OCTETS-1 : la garde (4) hache les fichiers sur le disque, pas les octets chargés en mémoire.
9. SHOGEN-RENDU-RENAME-FENETRE-1 : sous POSIX, une fenêtre reste entre la création exclusive de la cible et le
   renommage.
10. SHOGEN-GO-PICKAXE-FUSION-1 : `git log -G` ne lit pas les commits de fusion ; effet en refus seulement.
11. SHOGEN-AXES-SIGMA-NUL-1 : `axes_evaluables` marque « staleness » évaluable pour un σ de classe `None` ; sans effet
    en production.
12. SHOGEN-PAQUET-ERRATUM-FISHER-1 : le « (Fisher) » de doc 10 désigne la transformation z′ = artanh(r) ; l'intervalle
    « ≈ ±0,11 » vaut sur l'échelle z′ ; SE = 1/√(N−3) suppose des paires indépendantes ; N_min = 300 est un choix de
    conception.
13. SHOGEN-TAU-REDERIV-1 : τ n'est pas re-dérivé ; le τ committé sert à tous les confirmatoires (§5.1).
14. SHOGEN-CENSURE-INFO-1 : la censure informative n'est pas modélisée ; le verdict n'est pas identifié sous censure
    arbitraire des fenêtres sautées (§5.3).
15. SHOGEN-SEG-DEMARRAGE-1 : un enregistrement appartient au segment par son propre horodatage ; un segment sans
    `asn_attribution` retenu rend k_eff non évaluable.
16. Sceau privé : avec l'ancre (1), le jeton atteste l'existence des octets au plus tard à genTime, rien sur des lectures
    antérieures, sous confiance en FreeTSA ; en session cloud, les commits sont signés par la clé de la session et aucun
    bundle hors ligne n'est fait (§8.1).
17. Horloge du harnais (T-17) : l'affectation des fenêtres aux strates et aux segments repose sur l'horloge de l'hôte,
    A(harness-clock) ; l'étendue des écarts médians du contrôle d'horloge n'entre pas au bloc 1 (§2.7).
18. SHOGEN-COLLECT-PREVWS-1 : item non qualifiable en session cloud, hors règle ; requalification après S2.
19. SHOGEN-ATTEST-ADVISOR-1 : attestations d'advisors manquantes ; la classe R est exclue par l'inventaire D.1, pas par
    attestation.
20. Valeurs du bloc machine : les sha256 des journaux n'étaient que sur le poste local ; le validateur du paquet en a
    validé le texte et le format, pas les valeurs. À l'exécution, les journaux téléchargés leur sont égaux (§8.3).

### 9.3 Limites constatées d'après l'exécution

1. [constat du rapport] Le verdict se joue en entier sur le plancher d'erreur-type : z_s ≈ 20,8 et ≈ 28,5, mais
   FIV_s ≈ 115 et ≈ 266 ramènent z_bloc,s sous 2,33 (§3.1). La règle ne départage pas co-défaillance des sources et
   dépendance sérielle des fenêtres : c'est l'énoncé scellé de la discordance.
2. [constat du rapport] Les écarts comptés sont presque tous des pannes : en calme, 1 443 des 1 451 écarts (4 de
   staleness, 4 hors-enveloppe) ; en stress, 691 des 693 (2 de staleness, aucun hors-enveloppe) [calc, sommes du
   bloc 3, égales à Σ mⱼ du bloc 4]. K est formé, à une fenêtre près, de fenêtres à au moins deux lectures
   `panne_transport` (§5.2). Ces comptes décrivent ; ils n'identifient pas de cause.
3. [constat du rapport] La censure est large au regard de n : 7 795 fenêtres de grille sautées hors plage D5, dont
   7 628 sans cause attribuée par le journal, pour 35 982 fenêtres analysées, et 4 093 démarrages du harnais
   (§2.6) ; avec σ̂_bloc,s, les bornes non extérieures vont de ≈ 1,82 à ≈ 93,9 en calme et de ≈ 1,70 à ≈ 33,1 en stress
   (§5.3). H_perte est une hypothèse, non testée.
4. [constat du rapport] La partition R2 est un instantané : un relevé par hôte, le dernier, pris entre
   2026-09-28T01:17:55Z et 01:18:02Z (J28 l.435781). Elle ne décrit pas l'axe ASN sur les 33 jours. Sur le J14
   principal, les dix relevés retenus en fin de segment ont échoué et k_eff n'y est qu'une borne supérieure (§7.1).
5. [constat du rapport] Un seul observateur : un hôte de collecte (traces Windows dans les rendus ; le poste de
   l'investisseur, JOURNAL l.324), un résolveur DNS
   (Cloudflare DoH) par relevé ; la sonde multi-résolveurs et multi-vantage est « DUE » et le résidu 5 est « à son
   MAXIMUM, publié » (J28 l.435772, l.435774). Les écarts de R1 et l'axe ASN de R2 dépendent du même observateur.
6. [constat du rapport] L'axe staleness n'est pas évaluable pour binance, kraken et bitfinex, qui ne portent pas
   d'horodatage (J28 l.435464) : il couvre 8 des 11 flux du pool.
7. [constat du rapport] Couverture inégale de la strate de stress : le week-end du 2026-08-29 n'est couvert que sur
   19 h des 48 h, et celui du 2026-09-26 sur 32 h 51 min dans la variante principale, à cause de la plage D5 (§2.5).
8. [constat du rapport] Pyth est mort sur toute la campagne (HTTP 401 dès le premier jour, ADR l.25) : le pool perd un
   des deux flux de classe oracle, et chainlink n'est observé que par un RPC public (§4.4).
9. [constat du rapport] Le libellé du bloc 5 (d) du J28, « aucun cluster à ≥ 2 flux (1) », se lit mal à côté de la
   partition du bloc 6 ; l'estimateur principal de D3 entre clusters n'a pas d'objet sur le J28 (§4.2).
10. [constat du rapport] Le JSON du recalcul tiers porte `"r1_discrimine": "VRAI"` pour la variante « plage incluse »,
    étiquetée seulement au niveau de l'entrée (§7.4) ; une lecture de la ligne seule l'isolerait de son étiquette.
11. [constat du rapport] Deux sorties hors décision franchissent le seuil là où le J28 ne le franchit pas : le J14
    principal REJETTE en calme (z_bloc ≈ 2,65) et la variante incluse donne z_bloc ≈ 2,51 en calme (§7.1, §7.4). Le
    pt 9 les exclut de la décision ; ce rapport n'en tire aucune lecture.
12. [constat du rapport] Le recalcul tiers n'est pas une implémentation indépendante (§8.6) ; σ̂²_bloc,s n'est
    recompté par aucun code distinct sur les journaux réels.
13. [constat du rapport] Le τ observé dépasse τ_classe au maximum pour deux classes (§5.1) : trouvaille descriptive,
    sans re-tune ; la re-dérivation est PX-Shogen-13 (§11).
14. [constat du rapport] L'égalité octet à octet d'un rejeu des rendus sur un autre hôte ou une autre version de
    Python n'est pas mesurée (§12).

## 10. Déviations et expositions déclarées

### 10.1 Lecture D.1 n° 16 : exposition de l'orchestrateur de la session cloud

- **Ce qui est déclaré** (annexe D, D.1 n° 16, ajout daté du 2026-10-02 17:5x UTC, déviation déclarée au titre de D2
  pt 8) : en mesurant l'item MONARK-S2-M009A-EXPOSITION-1, l'orchestrateur de la session cloud a affiché les sujets des
  commits du dépôt privé `KraidleAI/monark-governance` qui touchent les pièces interdites de D.2 n° 2 ; le sujet du
  commit `aa04924` porte un taux estimé sur les traces S2, dont la valeur n'est recopiée nulle part ; le contenu des
  fichiers n'a pas été téléchargé (clone sans blobs). Date : 2026-10-02 vers 17:57Z ; classe R présumée (même mesure
  que la lecture n° 2, réimplémentation MONARK de `r1.classify_ecart` sur un instantané du 18/09 ; nature exacte du
  taux non établie sans lecture).
- **Situation dans la chronologie** : après le premier sceau (genTime 2026-10-02T17:44:30Z) et avant le second
  (2026-10-03T01:04:10Z). Le paquet révisé la recense : l'annexe D « compte 16 lectures en D.1 (la n° 16, exposition de
  l'orchestrateur de la session cloud, est datée du 2026-10-02 après le premier sceau et avant celui-ci) » (paquet l.8,
  (v)). Le texte de la règle (§10.2) était déjà scellé par le premier paquet et il est identique à l'octet dans le
  second (paquet l.8 ; JOURNAL l.304). L'exécution unique a été conduite par « l'orchestrateur de la session cloud »
  (JOURNAL l.310) ; c'est l'exécution mécanique d'un script scellé, sous les gardes du §8.
- L'item SHOGEN-MONARK-SUJET-COMMIT-1, qui mesurait les sessions ayant affiché ce sujet de commit, est fermé
  (annexe B.38).

### 10.2 Fermeture de MONARK-S2-M009A-EXPOSITION-1 (annexe B.38)

L'annexe B.38 demande que ce résultat soit « repris au rapport de l'exécution » ; il l'est ici, recopié pour
l'essentiel. L'item est fermé après le scellement (déclencheur « avant scellement » dépassé, écart consigné au paquet
§8 et au JOURNAL). Les lecteurs du chiffre de la lecture D.1 n° 2 sont les sessions MONARK des lots M009,
l'orchestrateur du poste local (session `90684fb2`) et ses sous-agents, et un sous-agent de cartographie
(`carto:monark`, sujet du commit seulement, non transmis) ; aucun auteur de la règle SHOGEN-CRITERE-R1-1 ni décideur,
sous les limites de l'annexe B.37 (recherche par jetons exacts, fenêtre de 300 caractères, fichiers textuels) ; plus
l'orchestrateur cloud après le premier scellement (D.1 n° 16, §10.1). Attestation de l'investisseur, décideur de la
règle, à la question de savoir s'il a vu ce chiffre : « non » (annexe D.3 (i)). Le paquet révisé note que cette
fermeture lève la limite écrite à son §8 (paquet l.8, (v)), dont le texte est resté inchangé.

### 10.3 Remplacement du premier sceau (A-8 ; lot CORR)

- Premier paquet : commit `ddf8c54`, sha256 `494d770d704dc7c342f0c6deec269e5642b3621bf451922f991e4ca1fb968097`, jeton
  FreeTSA de genTime 2026-10-02T17:44:30Z ; remplacé avant toute exécution ; il reste cité et n'ouvre plus aucune
  exécution (paquet l.8 ; §8.1).
- Motif : deux constats de classe A des relectures G2 de rattrapage, chacun capable de laisser l'exécution unique sans
  aucune sortie, sans produire de valeur fausse (annexe B.42, A-1 : un `frozenset` de paires de copies exactes que le
  recalcul tiers ne sérialisait pas ; annexe B.43, A-1 : un prix `ok` non fini qui levait une exception de `decimal`).
- Décision de l'investisseur du 2026-10-02 : « Corriger et resceller ». Lot CORR, commits `02f9c00`, `4002239`,
  `35cd2e2`, `4c831b8`, `e4bc2f1`, `a5a9de9`, `f35a70c`, suite 398 OK, règle et épingles inchangées à chaque commit
  (annexe A, ligne CORR ; annexe B.44).
- Effet sur le texte scellé : sections 1 à 12 inchangées, section 10.2 identique à l'octet ; aucune valeur, aucun
  seuil, aucune inégalité de la règle ne change ; nouveau bloc machine (commit d'analyse `f35a70c`) (paquet l.8 ;
  JOURNAL l.304).
- Dans cette exécution, aucun des deux cas corrigés ne s'est présenté : la liste des copies exactes est vide dans les
  quatre entrées du recalcul tiers (RT l.1520, l.6557, l.10991, l.15421), et aucun avertissement du lecteur n'est imprimé
  (RT l.2), alors que la précision (i) du paquet en prévoit un, compté par flux, pour tout prix non fini.

### 10.4 Précédence D-4 (SHOGEN-D4-PRECEDENCE-RAPPORT-1, annexe B.45)

La précédence D-4 (cas FAUX avec k_eff non évaluable, rendu NON ÉVALUABLE pour le drapeau 2) n'est pas écrite au
paquet ; elle est ratifiée (annexe B.18) et doit être citée au rapport si le cas se présente. **Le cas ne se présente
pas au J28** : « R1 discrimine » est FAUX et k_eff = 4 est évaluable (J28 l.435780) ; le drapeau 2 est éteint par le
pt 10 lui-même (l.435795). Il ne se présente pas non plus dans les sorties hors décision : au J14 principal, « R1
discrimine » est VRAI avec un k_eff borne supérieure, d'où un drapeau non évaluable par la lecture (a) du pt 10 (§7.1) ;
au J14 second, « R1 discrimine » est NON ÉVALUABLE, d'où un drapeau non évaluable par le pt 10 (§7.2).

### 10.5 Autres déviations

Aucune autre déviation n'est connue de l'orchestrateur à la date du brief de ce rapport (2026-10-04). Le JOURNAL
consigne une seule exécution, sans tentative échouée ni seconde exécution (l.314). Le refus « run_params divergents »
que craignait l'item SHOGEN-R2-RUNPARAMS-CONCORDANCE-1 ne s'est pas produit : l'exécution a écrit ses sept sorties
(annexe B.45 ; §8.4). Les décisions de l'investisseur consignées après l'exécution (JOURNAL l.322 ; §1) sont celles que
D6 (vi) et D9 lui réservent après le J28, plus un lot S2-bis ; à la connaissance du rédacteur, aucune ne change une
décision antérieure au sceau (ADR §1 bis.8 en ferait une déviation déclarée).

## 11. Analyses ajoutées après le pré-enregistrement : non faites à la date du rapport

Chacune portera l'étiquette obligatoire « ajoutée après le pré-enregistrement, hors décision » ; aucune n'est calculée
ici, aucune n'entre dans la règle ni ne peut changer le verdict (paquet §7, §11).

| item | ce qu'elle mesurera | source |
|---|---|---|
| SHOGEN-FLUX-QUASI-MORT-1 | la règle scellée recalculée par strate après retrait des flux « quasi morts », 2·ok(f, s) < n_s, seuil fixé d'avance par un auteur sans exposition aux taux de présence ; contrainte de construction SHOGEN-QUASI-MORT-PREDICAT-1 : compter « ok » par le prédicat de `r1.analysis_pools` sur la liste de `r1.parse_journal` | `docs/adr-0028/AVIS-SEUIL-FLUX-QUASI-MORT.md` §1 ; annexe B.39, B.44 |
| SHOGEN-HOST-DEGRADED-2 | la sensibilité « fenêtres à diagnostic d'hôte dégradé retirées », critère défini sur les seuls enregistrements de diagnostic du harnais (`asn_attribution.resolve_failed`, `clock_check`), jamais sur un statut de source | annexe B.6 ; annexe D.5 |
| SHOGEN-CENSURE-INFO-2 | les bornes extérieures de z sous censure arbitraire des fenêtres sautées (imputations quelconques, bornes de type Manski), avec la lecture « identifié » ou « non identifié sous censure arbitraire » | annexe B.6 (P-08) ; annexe D.5 |
| SHOGEN-DEP-FENETRES-2 | la dépendance sérielle de portée ≥ ℓ (asymptotique fixed-b, version linéarisée de Künsch, statistique par événements), décharge de A(window-dependence) ; prioritaire avant G10 si le run maximal est ≥ ℓ, ce qui n'est pas le cas au J28 (6 et 2, §5.4) | annexe B.6 |
| SHOGEN-R1-PLUGIN-1 | les limites du z transposé : variance de la fonction d'influence (conservativité du plug-in), test de la loi complète de m_t contre sa loi de Poisson-binomiale (absorption d'un mode commun large) | annexe B.6 |
| SHOGEN-CONTENU-DEP-1 | la dépendance sérielle sur l'axe contenu (N effectif < N pour N_min = 300 et le SE de Fisher), par une variance par blocs de ρ̂ | annexe B.6 ; paquet §12 pt 12 |
| SHOGEN-POOLEE-BLOC-1 | un plancher d'erreur-type par blocs pour la strate poolée et le niveau de z_pool sous le modèle nul, par simulation | annexe B.13, B.18 |
| PX-Shogen-13 | la re-dérivation de τ après le rendu, jamais appliquée aux z confirmatoires ; réserve : τ observé et P99 de calibration ne portent pas sur la même population | annexe D.5 ; paquet §12 pt 13 ; annexe B.45 |

### 11.1 Ajout daté du 2026-10-04 : analyses faites après le pré-enregistrement (lot POST-PREREG), hors décision

Chaque sortie porte en première ligne : « ajoutée après le pré-enregistrement, hors décision ; ne change pas le verdict
de la règle scellée (« R1 discrimine » = FAUX, docs/11 §3) ». Aucune n'entre dans la règle ni ne remplace une valeur
d'un rendu ; le verdict reste celui du §3. Code : `scripts/post-s2/`, qui réutilise les lecteurs du harnais sans
modifier `s2-harness` ; sorties : `docs/adr-0028/execution/post-prereg-2026-10-04/` (abrégé PP/ ci-dessous ; sha256 dans
`SHA256SUMS`) ; journal G1 du worker (`docs/G1-lot-POST-PREREG.md`), où les paramètres sont écrits le 2026-10-04 à
04:18:36 UTC, avant toute exécution sur les journaux. Exposition déclarée au moment de les fixer : bloc 3 du rendu J28
et ce rapport. Le seuil de FLUX-QUASI-MORT-1 vient de l'avis d'un auteur sans exposition (annexe B.39) ; celui de
FLUX-DEVIANT-1 (p̂_f > 1/2) est la valeur de la variante V2 du même avis, appliquée par le worker. Les constructions
viennent de l'annexe B, écrite avant l'exécution, sauf la forme du critère de HOST-DEGRADED-2 (sonde ASN du démarrage,
dernier marqueur, `clock_check` hors critère), choix du worker non écrit à l'annexe. Ces choix du worker sont fixés
avant l'exécution, après l'exposition déclarée ci-dessus, et nommés dans le journal G1. Contrôle de cohérence : chaque
sortie recompte n, K et P̂_more par strate et les trouve égaux, chaîne pour chaîne, au bloc 3 du J28 (PP/*.txt l.7-8).
Arrondis « ≈ » à 3 chiffres significatifs ; valeurs complètes aux lignes citées.

| item | ce qui est calculé | résultat | sortie |
|---|---|---|---|
| SHOGEN-FLUX-QUASI-MORT-1 (avec QUASI-MORT-PREDICAT-1 et POOL-MIN-1) | règle scellée recalculée par strate sans les flux à 2·ok(f, s) < n_s, ok compté par le prédicat de `r1.analysis_pools` | aucun flux retiré (taux `ok` minimal ≈ 0,981 en calme, bitstamp ; ≈ 0,980 en stress, defillama [calc]) ; règle recalculée identique à la règle scellée ; « R1 discrimine » recalculé = FAUX | PP/quasi-mort.txt l.10-16 |
| SHOGEN-FLUX-DEVIANT-1 (exploratoire, conditionnée sur p̂_f) | même recalcul sans les flux à p̂_f > 1/2 | aucun flux retiré (p̂_f maximal ≈ 0,0193 en calme, ≈ 0,0198 en stress [calc]) ; identique ; FAUX | PP/deviant.txt l.10-16 |
| SHOGEN-POOLEE-BLOC-1 (a) | z_pool,bloc = Σ_s (K_s − n_s·P̂_more,s)/√(Σ_s σ̂²_bloc,s) | ≈ 2,60 (z_pool binomial ≈ 33,4) ; exploratoire, hors famille ; niveau non mesuré (POOLEE-BLOC-1 (b), lot DETTES-SIM) | PP/poolee-bloc.txt l.12-13 |
| SHOGEN-HOST-DEGRADED-2 | règle recalculée sans les fenêtres des démarrages dont la sonde ASN porte un `resolve_failed` | 631 démarrages sur 4 172 ; fenêtres retirées 3 341 en calme et 720 en stress ; K passe de 154 à 70 et de 133 à 59 ; calme : z_s ≈ 18,1, z_bloc ≈ 1,80, NE REJETTE PAS (discordance), EMD_s ≈ 104 ; stress : garde ≈ 6,03 < 10, NON ÉVALUABLE ; FAUX | PP/hote-degrade.txt l.10-18 |
| SHOGEN-HORLOGE-ETENDUE-1 | offset médian des 3 610 `clock_check` retenus | aucun non évaluable ; minimum ≈ −52,2 s, médiane ≈ 1,42 s, maximum ≈ 96,3 s, étendue ≈ 148 s | PP/horloge-etendue.txt l.10-11 |
| SHOGEN-CENSURE-INFO-2 | bornes extérieures de z_s sous censure arbitraire des fenêtres sautées ; valeur de la règle sous deux imputations témoins | calme : z_s ∈ [≈ −169 ; ≈ 121] ; stress : [≈ −88,6 ; ≈ 81,5], bornes atteintes ; toutes fenêtres sautées propres : FAUX ; 19 fenêtres sautées en calme (42 en stress) imputées à deux écarts : REJETTE, d'où « R1 discrimine » VRAI sous cette imputation ; lecture : **non identifié sous censure arbitraire** | PP/censure.txt l.10-21 |
| SHOGEN-SIGMA-BLOC-INDEP-1 | classification, série I_t et σ̂²_bloc par un code indépendant de `r1` | 0 désaccord sur 270 435 cellules en calme et 125 367 en stress ; γ̂₀ et σ̂²_bloc égaux, chaîne pour chaîne, au bloc 3 | PP/sigma-indep.txt l.9-13 |
| SHOGEN-DEP-FENETRES-2 (b), qui est SHOGEN-R1-PLUGIN-1 (a) | variance par blocs de la fonction d'influence de K/n − P_more(p̂) (Künsch 1989, Ex. 2.2 et (2.14)) | σ̂²_IF,bloc ≈ 0,672·σ̂²_bloc en calme, ≈ 0,677 en stress ; z_IF,bloc ≈ 2,37 en calme, ≈ 2,12 en stress ; exploratoire, niveau non mesuré | PP/influence.txt l.10-11 |
| SHOGEN-DEP-FENETRES-2 (c) | runs de I_t pris comme unités, loi nulle iid à P̂_more | R = 119 contre E[R] ≈ 33,5 en calme (z_R ≈ 14,8) ; 130 contre ≈ 16,7 en stress (z_R ≈ 27,8) | PP/influence.txt l.13-14 |
| SHOGEN-R1-PLUGIN-1 (b), descriptif | comptes de m_t contre la loi de Poisson-binomiale de p̂ | calme : m = 1 observé 1 001 contre ≈ 1 380 attendus, m ≥ 3 observé 49 contre ≈ 0,424 [calc] ; stress : m = 1, 214 contre ≈ 659, m ≥ 3, 118 contre ≈ 0,224 [calc] ; aucun test | PP/influence.txt l.17-40 |
| SHOGEN-CONTENU-DEP-1 | taille effective N_eff de ρ̂ (variance par blocs de sa fonction d'influence) contre le SE de Fisher | ρ̂ égaux au bloc 5 pour les 55 paires ; N_eff/N médian ≈ 0,0535 (ρ_raw) et ≈ 0,0556 (ρ_resid) ; N_eff < N_min = 300 pour 3 paires (ρ_raw) et 2 (ρ_resid) | PP/contenu.txt l.10-66 |

**Ce que ces analyses permettent de dire.** Le verdict du §3 ne dépend d'aucun flux presque mort ni d'aucun flux à taux
d'écart supérieur à 1/2 : il n'y en a pas au J28. σ̂²_bloc,s, dont dépend la discordance, est reproduit par un code
distinct de `r1` sur les journaux réels, lecteurs communs mis à part (seconde moitié de la limite 12 du §9.3). Les
fenêtres de K se concentrent dans les démarrages dont la sonde ASN du harnais porte un `resolve_failed` : 84 des 154
fenêtres de K en calme et 74 des 133 en stress y tombent, pour 13,6 % et 6,3 % des fenêtres [calc]. Le verdict FAUX
n'est pas identifié sous censure arbitraire des fenêtres sautées : il repose sur l'hypothèse H_perte (doc 08,
A(loss-non-informative)) ; une imputation de 19 fenêtres sautées en calme, ou de 42 en stress, donne « R1 discrimine »
VRAI. La taille effective estimée des séries de contenu est de l'ordre de 5 % de N en médiane et reste sous N pour les
55 paires, sur ρ_raw comme sur ρ_resid : pour chacune, le SE de Fisher (paquet §12 pt 12), qui suppose des paires
indépendantes, est plus petit que le SE par blocs (rapport de 1,50 à 15,0 [calc]).

**Ce qu'elles ne permettent pas de dire.** Aucune n'identifie une cause : la concentration de K dans les démarrages
dégradés est compatible avec un mode commun de l'observateur, sans l'établir. Deux statistiques exploratoires à
erreur-type par blocs franchissent 2,33 là où z_bloc,s ne le fait pas : z_pool,bloc ≈ 2,60 et z_IF,bloc ≈ 2,37 en
calme ; aucune n'est dans la règle ni dans la famille, leur niveau en échantillon fini n'est pas mesuré, et elles ne
changent pas le verdict (même statut que les sorties hors décision du §9.3 pt 11). Les runs pris comme unités gardent un
excès sous une loi nulle iid qui ignore la persistance propre de chaque source ; ce n'est pas un test de la dépendance
de portée ≥ ℓ. La loi de m_t est décrite, pas testée. Rien n'est dit de l'indépendance des sources (doc 09).

**Restes.** Non faits, avec leur motif : la forme fixed-b de DEP-FENETRES-2 (a) (Kiefer-Vogelsang, P-05, non versée) ;
une tolérance et une loi nulle de la statistique par événements (c) ; le test de la loi de m_t de R1-PLUGIN-1 (b)
(statistique et niveau à sourcer) ; une borne extérieure de z_bloc sous censure arbitraire (CENSURE-INFO-2 ; attribution
« de type Manski » [inféré : P-08 non versée]) ; le niveau de z_IF,bloc et de z_pool,bloc (simulation synthétique). Le
`clock_check` n'entre pas au critère de HOST-DEGRADED-2 : ses signaux de dégradation dépendent des sources qui répondent
à la sonde ; écart au libellé de l'item, déclaré au journal G1.

## 12. Reproduire

- **Entrées** : les trois journaux scellés, désignés par leurs sha256 (bloc machine, paquet l.217-219 ; §8.3), et le
  fichier de sommes de clôture (paquet l.220). Leur format est spécifié par référence (paquet §1 : `records.py` et
  `journal.py` au commit de collecte `ed479c5`, doc 10 §6).
- **Code** : commit d'analyse `f35a70c19ba8269f1f7e2bcd31775e4fc513da20` (`s2-harness/shogen_s2`, `s2-harness/tools`) ;
  script d'exécution unique `s2-harness/tools/rendu_unique.py`, sha256
  `06d189cf84e7dca97bdfc0e1b695fc827a09473779505c7a8f1af1e7c26e9050` (paquet l.215-216) ; Python 3.11.15 lors de
  l'exécution (ENR l.14).
- **Sceau** : `docs/adr-0028/sceau/` (manifeste, requête, jeton, chaîne de FreeTSA) ; contrôle hors ligne par
  `bash scripts/sceau/verify.sh` (§8.1).
- **Rejeu** : avec les journaux et le commit, les points d'entrée `recompute_*` recalculent les blocs depuis le journal
  seul (doc 10 §6 ; ADR-0003) ; leurs valeurs se comparent, chaîne pour chaîne, à celles des rendus versés (§8.6, §8.9).
  Une nouvelle production par `rendu_unique.py` serait une seconde exécution, déviation déclarée (annexe D.4 b).
- **Ce rapport** : chaque valeur y est citée par fichier et ligne ; les scripts du rédacteur et leurs sorties (§8.9)
  rejouent ses calculs depuis les seuls rendus, sans les journaux.
- **Ce qui n'est pas public** : le dépôt `KraidleAI/shogen` est privé (paquet §12 pt 16) ; les journaux scellés ne sont
  pas publiés, et leur publication conditionne le test de composition SHOGEN-S2-TUYAU-MONARK-1 côté MONARK (ADR §3 ;
  §4 pt 4). Les rendus et le sceau sont au même dépôt privé : un tiers à qui l'on remet les rendus et le sceau sans
  les journaux peut contrôler le sceau et l'arithmétique des rendus, pas recalculer les rendus.

> *Ajout daté du 2026-10-04 06:52:35 UTC (relecture G2 du lot DETTES-B1, C-3 ; points « Code » et « Rejeu » ci-dessus)* : à partir du commit `0221a74` (lot DETTES-B1, B1-1 ; `rendu_unique.py` à partir de `0789d96`, B1-4), `s2-harness/shogen_s2` et `s2-harness/tools` diffèrent du commit d'analyse `f35a70c` (sha256 de `rendu_unique.py` à la tête `5ee95dbf…` ≠ `sha256_script` `06d189cf…`) : les gardes (2) et (4) refusent à la tête ; tout rejeu (`recompute_*`) ou ré-exécution du rendu de S2 se fait sur une extraction de `f35a70c` ; à la tête, les sorties diffèrent par construction (bloc 5 (d), note k_eff, clé `etiquette` du drapeau 2 de `j28-incluse`, divergences ASN de relevés partiels).
