# Acteurs nommés dans le brouillon public de `docs/11` — liste pour le préavis privé (lot DOCS11-PUBLIC)

**Pièce interne, à ne pas publier.** Rédigée le 2026-10-04 (horloge lue : `date -u`, 14:05 UTC) par le worker du lot
(modèle `claude-opus-5-5`). Rattachement : brief du lot, point 4 ; décision de l'investisseur, q. 15, « acteurs mesurés
nommés avec préavis privé » (JOURNAL l.382) ; G0 `docs/adr-0029/G0-lots-S2BIS.md` l.13.

Brouillon visé : `11-mesures-pilotes-public.md`, sha256 `4de986544cee9622a0848f585103cea594352df65d02e8f51e6ef4c593fc7688`.
*Mise à jour datée du 2026-10-04 (14:5x UTC, `date -u`), après les corrections de la relecture G2 (C-1 à C-3, O-1, O-2) : nouvelle empreinte du brouillon ; son en-tête compte deux lignes de plus, d'où les renvois de ligne décalés de deux et le relevé du §1 régénéré ; aucun fait ni aucun compte de mentions ne change.*
*Mise à jour datée du 2026-10-04 (15:03 UTC, `date -u`), après les décisions de l'investisseur (JOURNAL l.390, 14:52:24 UTC) : nouvelle empreinte du brouillon ; l'en-tête compte encore deux lignes de plus (renvois décalés de deux) ; Pyth passe de 19 à 21 mentions (libellé factuel du §9.3 pt 8, mention de l'en-tête) ; §2, §4 et §5 suivent les décisions.*
Chaque nombre ci-dessous est recopié du brouillon, à la ligne citée (« b. l.N » = ligne N du brouillon) ; aucun n'est
calculé ici. Aucun contact n'a été pris ; aucun texte de préavis n'est rédigé : le contenu et le calendrier du préavis
sont à l'investisseur (ADR-0028 §4 pt 4 : « contacts de préavis »).

## 1. Relevé mécanique (script `outils/acteurs_nommes.py`, sortie `acteurs_nommes.sortie.txt`)

Une mention est une occurrence, insensible à la casse, d'un alias non précédé ni suivi d'une lettre (« Pyth » ne
compte pas « Python »).

| acteur | groupe | rôle dans la mesure | mentions | lignes du brouillon | sections |
|---|---|---|---|---|---|
| Binance | A | flux `binance` (place, sans horodatage) | 26 | 146, 156, 163, 325, 351, 355, 356, 366, 369, 385, 393, 508, 524, 526, 527, 528, 576, 786, 790, 898 | 2.1, 3.5, 4.1, 4.2, 6, 7.1, 8.7, 9.3 |
| Coinbase | A | flux `coinbase` (place horodatée) | 9 | 146, 155, 326, 350, 352, 369, 384, 393 | 2.1, 3.5, 4.1, 4.2 |
| Kraken | A | flux `kraken` (place, sans horodatage) | 11 | 146, 156, 163, 327, 350, 384, 576, 677, 678, 898 | 2.1, 3.5, 4.1, 4.2, 7.1, 7.5, 9.3 |
| OKX | A | flux `okx_ticker` et `okx_index` (places horodatées, un hôte) | 19 | 117, 147, 155, 165, 328, 329, 350, 385, 386, 677, 786, 790 | Conventions de lecture et lexique, 2.1, 3.5, 4.1, 4.2, 7.5, 8.7 |
| Bitstamp | A | flux `bitstamp` (place horodatée) | 13 | 147, 155, 330, 358, 367, 386, 508, 524, 525, 527, 529, 1020 | 2.1, 3.5, 4.1, 4.2, 6, 11.1 |
| Gemini | A | flux `gemini` (place horodatée) | 12 | 147, 155, 331, 357, 367, 386, 508, 525, 526, 528, 529 | 2.1, 3.5, 4.1, 4.2, 6 |
| Bitfinex | A | flux `bitfinex` (place, sans horodatage) | 12 | 147, 156, 163, 332, 350, 384, 444, 576, 677, 678, 898 | 2.1, 3.5, 4.1, 4.2, 5.1, 7.1, 7.5, 9.3 |
| CoinGecko | A | flux `coingecko` (agrégateur) | 18 | 147, 157, 333, 350, 351, 353, 356, 369, 384, 393, 678, 679 | 2.1, 3.5, 4.1, 4.2, 7.5 |
| DefiLlama | A | flux `defillama` (agrégateur) | 13 | 147, 157, 334, 350, 353, 369, 385, 393, 679, 1020 | 2.1, 3.5, 4.1, 4.2, 7.5, 11.1 |
| Pyth | A | flux `pyth` (oracle), retiré du pool d'analyse | 21 | 8, 41, 138, 147, 159, 172, 173, 175, 352, 369, 393, 409, 420, 438, 558, 598, 902 | titre, 1, Conventions de lecture et lexique, 2.1, 2.2, 4.1, 4.2, 4.3, 4.4, 5.1, 7.1, 7.2, 9.3 |
| Chainlink | A | flux `chainlink` (oracle, lu par RPC public) | 15 | 147, 158, 165, 335, 350, 414, 417, 437, 443, 444, 678, 679, 903 | 2.1, 3.5, 4.1, 4.4, 5.1, 7.5, 9.3 |
| Cloudflare | B | AS13335, partagé par sept hôtes ; résolveur DNS du harnais | 8 | 56, 225, 350, 366, 382, 386, 896 | 1, 2.7, 4.1, 4.2, 9.3 |
| Amazon (AWS, CloudFront) | B | AS16509 et AS14618 (deux hôtes) | 6 | 355, 357, 386 | 4.1, 4.2 |
| Incapsula | B | AS19551 (un hôte) | 3 | 358, 386 | 4.1, 4.2 |
| PublicNode | B | RPC public de lecture de chainlink | 6 | 166, 350, 354, 385, 414, 416 | 2.1, 4.1, 4.2, 4.4 |
| FreeTSA | C | autorité d'horodatage du sceau | 7 | 698, 699, 703, 716, 868, 953, 1067 | 8.1, 9.2, 10.3, 12 |
| RIPEstat | C | attribution ASN croisée | 1 | 382 | 4.2 |
| Team Cymru | C | attribution ASN croisée | 1 | 382 | 4.2 |
| OpenTimestamps | C | ancre de durabilité non faite | 1 | 716 | 8.1 |
| OpenSSL | C | outil de vérification du jeton | 2 | 700, 703 | 8.1 |
| USDT | C | devise de cotation de deux flux | 3 | 116, 148, 391 | Conventions de lecture et lexique, 2.1, 4.2 |
| MONARK | D | projet connexe (exposition déclarée, test de composition) | 9 | 777, 923, 924, 927, 935, 938, 942, 1075 | 8.6, 10.1, 10.2, 12 |

Groupes : A, source mesurée (flux du pool configuré) ; B, infrastructure nommée par la partition R2 ou par le chemin de
lecture ; C, service, outil ou monnaie nommé, non mesuré ; D, projet connexe nommé. Les auteurs cités pour la méthode
(Knight et Leveson, L&M, Künsch, Kiefer-Vogelsang, Manski, Fisher, Bartlett) ne sont pas des acteurs mesurés.

## 2. Ce que chaque source mesurée lira sur elle (groupe A)

Toutes les valeurs sont de la strate calme puis de la strate de stress, au J28, « tel qu'observé par cet instrument
(hôte, DNS et réseau du harnais compris) » (b. l.51-52) ; un écart est une panne, une staleness ou un hors-enveloppe
de la lecture faite par le harnais (b. l.120-122).

| source | écarts au J28 (b. l.325-335 ; panne / stale / horsE / nonÉv) | hôte et axe ASN (b. l.350-358, l.384-387) | autres mentions nominatives |
|---|---|---|---|
| Binance | 372 (372 / 0 / 0 / 0) ; 46 (46 / 0 / 0 / 0) ; classe `sans_horodatage` | `api.binance.com`, AS16509 (Amazon), singleton ; CNAME vers CloudFront | amont déclaré binance → coingecko ; paires de singletons avec bitstamp et gemini (§6, b. l.524-528) ; quatre des cinq lectures du journal brut absentes du journal sont de binance, toutes dans la plage exclue D5 (§8.7, b. l.789-792) |
| Coinbase | 56 (56 / 0 / 0 / 0) ; 11 (11 / 0 / 0 / 0) | `api.exchange.coinbase.com`, AS13335 | amont déclaré coinbase → pyth |
| Kraken | 34 (34 / 0 / 0 / 0) ; 46 (46 / 0 / 0 / 0) ; classe `sans_horodatage` | `api.kraken.com`, AS13335 | φ kraken×bitfinex ≈ 0,454 en calme, ≈ 0,763 en stress (§7.5, b. l.677-678) |
| OKX | `okx_ticker` 64 (64 / 0 / 0 / 0) ; 6 (6 / 0 / 0 / 1) ; `okx_index` 64 (64 / 0 / 0 / 0) ; 7 (7 / 0 / 0 / 1) | `www.okx.com` (un hôte pour deux flux), AS13335, CDN de Cloudflare | φ okx_ticker×okx_index ≈ 0,452 en calme (§7.5) ; une lecture `okx_ticker` du journal brut absente du journal, dans la plage exclue D5 (§8.7) |
| Bitstamp | 475 (475 / 0 / 0 / 0) ; 39 (39 / 0 / 0 / 0) | `www.bitstamp.net`, AS19551 (Incapsula), singleton | taux `ok` minimal en calme ≈ 0,981 (§11.1, b. l.1020) ; paires de singletons avec binance et gemini (§6) |
| Gemini | 68 (65 / 3 / 0 / 0) ; 21 (19 / 2 / 0 / 0) | `api.gemini.com`, AS14618 (Amazon), singleton ; équilibreur AWS | paires de singletons avec binance et bitstamp (§6) |
| Bitfinex | 32 (30 / 0 / 2 / 0) ; 51 (51 / 0 / 0 / 0) ; classe `sans_horodatage` | `api-pub.bitfinex.com`, AS13335 | φ kraken×bitfinex (voir Kraken) ; sa classe `sans_horodatage` a un maximum observé au-dessus de τ_classe, « cohérent avec les cellules hors-enveloppe comptées au bloc 3 » (2 en calme ; §5.1, b. l.443-445) |
| CoinGecko | 56 (56 / 0 / 0 / 0) ; 127 (127 / 0 / 0 / 1) ; classe `agregateur` | `api.coingecko.com`, AS13335 | amonts déclarés binance → coingecko, coingecko → defillama ; déclaration d'estimateur ; φ coingecko×chainlink ≈ 0,901 et coingecko×defillama ≈ 0,686 en stress (§7.5) |
| DefiLlama | 159 (158 / 1 / 0 / 0) ; 226 (226 / 0 / 0 / 0) ; classe `agregateur` | `coins.llama.fi`, AS13335 | taux `ok` minimal en stress ≈ 0,980 (§11.1, b. l.1020) ; φ defillama×chainlink ≈ 0,691 en stress (§7.5) |
| Pyth | aucun écart compté : retiré du pool d'analyse (cas (a)), « 0 `ok` sur 40 804 lectures, HTTP 401 dès 2026-08-26T19:00Z » (b. l.176) | — | « aucune mesure de ce rapport ne porte sur lui » (§4.4, b. l.420-421) ; libellé public du §9.3 pt 8 : « Aucune donnée de prix n'a été reçue de Pyth sur toute la campagne : l'accès au service interrogé a été refusé (HTTP 401) dès le premier jour (ADR l.25), et rien ne montre une panne de Pyth » (b. l.902 ; retouche E-14, décision de l'investisseur du 2026-10-04 ; le rapport source écrivait « Pyth est mort sur toute la campagne ») ; amont déclaré coinbase → pyth ; déclaration d'estimateur |
| Chainlink | 71 (69 / 0 / 2 / 0) ; 113 (113 / 0 / 0 / 0) ; classe `oracle_chainlink` | lu par `eth_call` sur `ethereum-rpc.publicnode.com` (AS13335) : « une infrastructure de lecture, pas l'amont du feed » (b. l.414-417) | φ avec coingecko et defillama (§7.5) ; sa classe `oracle_chainlink` a un maximum observé au-dessus de τ_classe, « cohérent avec les cellules hors-enveloppe comptées au bloc 3 » (2 en calme ; §5.1, b. l.443-445) |

## 3. Infrastructures nommées (groupe B)

- **Cloudflare** : « 7 des 10 hôtes du pool partagent AS13335 (Cloudflare), côté livraison » (b. l.55-56) ; résolveur
  `cloudflare-dns.com` de chaque relevé ASN (§2.7, §4.2). Le rapport précise que l'IP observée derrière un CDN est la
  couche de livraison, pas l'origine (b. l.418-419).
- **Amazon** : AS16509 pour `api.binance.com` (CloudFront), AS14618 pour `api.gemini.com` (équilibreur AWS).
- **Incapsula** : AS19551 pour `www.bitstamp.net`.
- **PublicNode** : `ethereum-rpc.publicnode.com`, RPC public par lequel chainlink est lu.

## 4. Nommés sans être mesurés (groupes C et D)

FreeTSA (autorité d'horodatage du sceau ; le rapport la décrit comme « opérateur individuel, sans accord de niveau de
service lu », §8.1, b. l.716), RIPEstat et Team Cymru (attribution ASN croisée, « concordant »), OpenTimestamps (ancre non faite),
OpenSSL (outil), USDT (devise de cotation de deux flux ; « l'écart de peg USDT/USD est porté par ρ_resid », §4.2), et le
projet connexe MONARK (exposition déclarée au §10, test de composition aux §8.6 et §12 ; neuf mentions, une de plus que
la source, par la retouche E-09 qui remplace un nom de dépôt privé par « dépôt privé du projet MONARK ») ; nommé publiquement, par décision de l'investisseur du 2026-10-04 (JOURNAL l.390).

## 5. Points de lecture à signaler pour le préavis (le point 1 est retouché par décision de l'investisseur ; les autres ne le sont pas)

1. **Pyth.** Le rapport source écrivait au §9.3 pt 8 « Pyth est mort sur toute la campagne ». Sur décision de
   l'investisseur du 2026-10-04 (JOURNAL l.390), la version publique porte un libellé factuel (retouche E-14) :
   aucune donnée de prix reçue, accès refusé (HTTP 401) dès le premier jour, rien ne montre une panne de Pyth ;
   le §4.4 dit déjà qu'« aucune mesure de ce rapport ne porte sur lui ». Le préavis à Pyth peut citer ce libellé.
2. **Comptes d'écarts par source (§3.5).** Ce sont des lectures du harnais : le rapport dit que les écarts sont
   presque tous des pannes, que K est formé de fenêtres à au moins deux lectures `panne_transport`, et que « ces
   comptes décrivent ; ils n'identifient pas de cause » (§9.3 pt 2), la concentration de K dans les démarrages dégradés
   étant « compatible avec un mode commun de l'observateur, sans l'établir » (§11.1). Bitstamp (475 en calme), DefiLlama
   (226 en stress) et CoinGecko (127 en stress) portent les plus grands comptes.
3. **Partition ASN.** Le cluster AS13335 est « côté livraison » (CDN) : il ne dit rien de l'origine des sources, et
   pour chainlink il porte sur l'infrastructure de lecture.
4. **Journal brut (§8.7).** Les lectures absentes nomment binance et okx_ticker ; c'est un défaut de rapprochement des
   journaux du harnais, dans une plage exclue, pas un fait des sources.
5. **Ordre.** ADR-0028 §4 pt 4 lie publication et « contacts de préavis » ; le J14 (§7.1, §7.2) nomme aussi des
   sources ; il est publié avec son étiquette « hors décision », par décision de l'investisseur du 2026-10-04
   (JOURNAL l.390 ; ADR-0028 D4). Le rapport est publié seul ; le sceau, les rendus et les enregistrements sont
   remis sur demande, sous accord.
