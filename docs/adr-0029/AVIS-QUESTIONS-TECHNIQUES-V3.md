# AVIS advisor — ADR-0029 révision 3, cinq questions techniques du §8.2

- **Gate 0** : modèle résolu `claude-fable-5-1`, effort `medium` (fiche advisor, CLAUDE.md §7, amendement 2026-09-18). Date : 2026-10-04 (UTC).
- **Pièces lues [lu]** : `scratchpad/adr-s2bis/v3/ADR-0029-campagne-S2-bis-v3.md` (« v3 » ; l.1-262, l.412-471, plus les lignes trouvées par recherche : l.265, l.341-344, l.390-398, l.519-526) ; `docs/adr-0029/DECISIONS-ARCHITECTURE-S2BIS.md` (« DÉC », en entier, le §7 primant) ; `docs/adr-0029/AVIS-STATS.md` et `docs/adr-0029/AVIS-OPS.md` (en entier). Non lues : CE, EP, P1 à P8, SC (citées ici au second degré, via v3 et DÉC : [2nd]).
- **Attestation (forme D.3 d'ADR-0028)** : aucune pièce de `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/`, aucun `*.jsonl` ouverts. Exposition : valeurs de **S2** post-rendu portées par v3 §1.1 (z, K, P̂_more, FIV, τ observé), sans effet sur S2-bis, campagne neuve (v3 l.12). Aucune donnée de S2-bis n'existe. Aucun fichier suivi modifié.
- Conventions : « v3 l.n », « DÉC l.n », « STATS », « OPS » ; [inféré] = raisonnement de l'advisor ; [calc] = calcul de l'advisor.

## Résumé

| q. | recommandation | avant le sceau ? |
|---|---|---|
| 1 | Carte dans le **collecteur scellé** pour les sources prêtes au gel, lue dans un **processus et un journal séparés** du pool, hors de la fenêtre δ du pool ; aucune lecture de la carte avant le rendu ; les sources non prêtes attendent **l'après-rendu** (aucun flux hors paquet pendant la campagne) | oui (commit scellé, D.2-bis) |
| 2 | σ des places et agrégateurs sur ETH et stables = **max(plancher ADR-0020, σ_BTC de la même classe de source re-dérivé sur S2, 3 × P99 des suites de bougies à volume nul)** ; plancher de τ des agrégateurs = **τ_places(actif) × (τ_agr_BTC / τ_places_BTC)**, borné par CAPO ; formules dans l'ADR, valeurs au G0 de CALIB-ACTIFS | oui (formules) ; valeurs au G0 |
| 3 | Condition du G0 lue **classe par classe** ; seconde vague = **second paquet (τ, σ, énoncés), mêmes observateurs, même collecteur gelé, T_début_2 ≥ sceau_2 + 24 h, n_s identiques, lectures antérieures hors inférence** ; pour F3 (hors décision) accepter « planchers seuls » plutôt qu'une vague | la lecture classe par classe : oui ; la forme de la vague : au G0 de CALIB-ACTIFS, mais le collecteur doit déjà contenir les flux |
| 4 | Confirmer le **vote binaire à q_j** sur l'indicateur « P_j > seuil » par observateur ; ajouter N_témoin ≥ 2 pour qu'un observateur vote, « état indéterminé » si moins de 2 votants, seuil scellé **0,5 %** avec grille imprimée ; limite écrite : témoin aveugle à un décrochage joint USDC et USDT contre l'USD | oui (seuil et vote scellés), enjeu faible (hors décision) |
| 5 | **Imprimer S sur les données, hors décision**, avec la même loi de rotation (mêmes r, graine, R) ; phrase fixée d'avance « sans effet sur la décision » ; coût : 45 popcounts par rotation | oui (liste hors décision du §2.7 pt 9 scellée) |

Aucune de ces réponses ne change le budget du §3 ni la durée de la campagne BTC ; la q. 3 peut prolonger la location des observateurs du décalage entre les deux T_début (voir q. 3).

## Q1 — Carte : collecteur scellé ou flux hors paquet ?

**Ce que disent les pièces.** DÉC §7 n° 11 (l.111) laisse deux voies : carte servie au rendu unique, ou « collectée hors paquet sur un flux déclaré non scellé ». v3 §2.10 (l.256) pose les deux contraintes : (a) au collecteur scellé, seules les sources prêtes au gel entrent ; (b) un flux hors paquet lu pendant la campagne livrerait des co-défaillances corrélées à celles du pool (mêmes ASN, « 28 hôtes mesurés, 5 ASN », v3 l.257 [2nd, EP]). Le modèle d'accès interdit tout agent sur les observateurs pendant le segment confirmatoire (v3 l.239, OPS Q12). La décision G4 de l'orchestrateur admet un « brin exploratoire facultatif sur un VPS distinct, hors décision » (v3 l.49). Le budget de temps par fenêtre est déjà serré : 5 + 4 + 10 + 1 = 20 s pour cinq lectures séparées par hôte, environ 50 lectures par fenêtre pour les quatre classes, « davantage si la carte est lue par les observateurs » (v3 l.232).

**Options.**
- (a) Carte dans le collecteur scellé des quatre observateurs, même processus, même journal.
- (b) Carte dans le collecteur scellé, **processus et journal séparés** sur chaque observateur, lectures décalées hors de la fenêtre δ du pool.
- (c) Flux hors paquet sur un cinquième VPS, déclaré non scellé, lu pendant la campagne.
- (d) Carte collectée **après** le rendu, hors paquet (le Root Count v0 part de S2, DÉC l.111 ; rien n'attend la carte avant le rendu).

**Recommandation : (b) pour les sources prêtes au gel ; (d) pour les autres ; (c) écartée.** Motifs :
1. (a) met la carte dans la chaîne critique du pool : des dizaines de lectures de plus dans les 20 s de δ, un pool de fils plus gros, des fils abandonnés plus nombreux ; un retard de départ de plus de 5 s dégrade l'observateur (D-2, v3 l.106) et censure la fenêtre pour **toutes** les classes. La carte, hors vote, ne doit jamais pouvoir censurer le vote [inféré]. (b) l'isole : processus systemd distinct, lectures parties par exemple à ws + 5 s (le pool part à ws + w − 20 s, v3 l.231), pool de fils propre, journal chaîné propre avec sa propre tête (la tête entre dans l'échange de têtes et le jeton quotidien, v3 l.237). Un relevé de la carte reste un statut de source au sens de D.2-bis (v3 l.224) ; rien n'en est lu avant le rendu.
2. (c) ajoute un fournisseur, un compte, un VPS (coût de quelques euros par mois, v3 l.77) et surtout une **exposition** : un flux « non scellé » lu pendant la campagne n'a ni inventaire D.1-bis ni lecteurs désignés ; ses pannes sont celles des ASN du pool (v3 l.256) ; un lecteur qui le voit sait, avant le rendu, quand Cloudflare a toussé. C'est précisément ce que SHOGEN-S2BIS-CARTE-AVEUGLE-1 (v3 l.440) veut éviter. Si l'orchestrateur veut quand même (c), il faut l'inventorier comme un statut de source de S2-bis et ne le servir qu'au rendu : à ce prix, (c) n'apporte rien de plus que (b).
3. (d) est gratuite : aucun produit n'attend la carte avant le rendu (DÉC l.111 ; v3 l.415) ; une source dont la licence ou le décodeur n'est pas prêt au gel (v3 l.255 : décodeur, fixtures, smoke, page de licence par source) entre à la carte après le rendu sur un flux déclaré, sans toucher au commit scellé.

**À écrire au paquet** : liste fermée des sources de la carte au gel ; processus et journal séparés ; heure de départ des lectures de la carte dans la fenêtre ; règle « un échec de la carte n'affecte ni D-1 à D-5 ni le marqueur de clôture du pool » ; le volume de journal recalculé (v3 l.235 compte « environ × 4 » sans la carte).

**Risques** : débit par adresse partagé entre le pool et la carte sur un même hôte (CoinGecko : 5 à 15 appels par minute, v3 l.232 [2nd, P6 C5]) : une source présente à la fois au pool et à la carte (Chainlink sur plusieurs chaînes, DEX par RPC) doit respecter un seul budget par hôte, à chiffrer au G0 de la carte ; charge disque ; une panne du processus carte qui tue la machine (mémoire) : limites systemd (`MemoryMax`) à poser.

**Avant le sceau : oui.** Le collecteur est un commit scellé ; ajouter une source après change le commit (v3 l.256).

## Q2 — σ et planchers de τ pour ETH et les stables

**Ce que disent les pièces.** D-4 fixe τ des places (1,5 × P99,9 de |clôture − médiane LOO des clôtures|), les planchers des oracles poussés (τ ≥ 1,5 × seuil de déviation ; σ = 1,5 × heartbeat : ETH 5 400 s, USDC 124 200 s, USDT 129 600 s) (DÉC l.34-37). Le §7 n° 5 (l.105) dit que les τ des agrégateurs et des oracles sur ETH et stables sont « planchers seuls ». Ne sont pas fixés : σ des places et des agrégateurs (une bougie ne porte pas de staleness) et le plancher de τ des agrégateurs (v3 l.185, l.438). Le rodage ne peut pas servir (lectures de prix et de staleness interdites, v3 l.188, l.220). Pour BTC, σ = max(plancher ADR-0020, 3 × P99 staleness) sur S2, planchers 30 s (places horodatées), 300 s (agrégateurs), 5 400 s (Chainlink), aucun pour les places sans horodatage (v3 l.179 ; STATS Q4).

**Options pour σ (places, agrégateurs).**
- (a) Planchers d'ADR-0020 seuls (30 s, 300 s) : axe staleness très sensible, nombreux écarts propres aux observateurs.
- (b) **Transfert du σ_BTC re-dérivé** par classe de source, hôte par hôte : la staleness d'un ticker mesure la fraîcheur de livraison de l'hôte, propriété du canal plus que de l'actif [inféré].
- (c) (b) plus une correction par la liquidité de la paire, calibrée sur les bougies : 3 × P99 de la durée des suites de bougies à volume nul (une bougie sans transaction = pas de nouveau « dernier prix » : le ticker porte alors un horodatage ancien, faux positif de staleness) [inféré].
- (d) σ « infini » (axe staleness désactivé) pour ces classes.

**Recommandation : σ(actif, classe) = max(plancher ADR-0020, σ_BTC(classe) re-dérivé par TAU-SIGMA-S2BIS, grid-ceil(3 × P99 des suites de bougies à volume nul, 60 s))**, maximum sur les deux strates, par actif ; formule dans l'ADR, valeurs au G0 de CALIB-ACTIFS avant tout calcul (v3 l.182). Motifs : pour ETH, les places du pool cotent ETH avec une liquidité proche de BTC, le troisième terme restera sous σ_BTC et (b) suffit ; pour USDC/USD à trois places fiat (v3 l.170) et pour USDT/USD, les transactions sont espacées et (c) évite de compter la rareté des échanges comme une panne de livraison. (d) est à écarter : la staleness est le seul axe qui attrape une source « restée à 1,000 » pendant un décrochage (DÉC l.31 ; v3 l.97 (a)) ; la désactiver viderait la variable d'état de son usage. Limite écrite : un σ calibré sur des bougies historiques est une dérive de régime déclarée (même caveat que τ, v3 l.186). Agrégateurs : aucune bougie ne les calibre ; (b) seul (σ_BTC agrégateurs, cadence de l'hôte) [inféré].

**Options pour le plancher de τ des agrégateurs.**
- (a) τ_agr_BTC re-dérivé, tel quel, pour les quatre actifs : sur un stable, un τ de l'ordre de 2 % (τ committé 2,6 % en S2, v3 l.42) rend l'axe aveugle.
- (b) τ_agr(actif) = τ_places(actif) : ignore que l'agrégateur lisse plusieurs places et arrive en retard, d'où un écart systématique plus grand que celui d'une place (τ committé agrégateurs 2,6 % contre 0,45 % places en S2, v3 l.42 : rapport ≈ 5,8 [calc]).
- (c) **τ_agr(actif) = grid-ceil(τ_places(actif) × τ_agr_BTC / τ_places_BTC, 0,05 %)**, borné par 0,05 % ≤ τ < 2,85 % (CAPO, v3 l.178) : transfert du **rapport** entre classes mesuré sur S2, appliqué au τ de l'actif.

**Recommandation : (c)**, avec le rapport pris sur les τ re-dérivés de BTC (P99,9), non sur les τ committés de S2. Motif : une seule hypothèse, déclarée (le rapport agrégateur/place ne dépend pas de l'actif), au lieu de deux ; la règle est fixée avant tout calcul et ne lit aucune donnée d'agrégateur ; pour les stables, elle donne un τ d'agrégateur de quelques dixièmes de pour cent, cohérent avec le plancher d'oracle 0,375 % (v3 l.184). Imprimer à côté, descriptif, la valeur (a). Pour les oracles stables, l'axe reste aveugle par construction, déjà écrit (v3 l.185).

**Risques** : les bougies sans volume peuvent être absentes des fichiers (certaines API omettent les minutes vides) : à vérifier au G0 (la minute absente vaut bougie à volume nul [inféré]) ; une source d'ETH cotée en USDT (binance, okx, v3 l.97) porte le même « co-défaillance de cotation » ; le rapport (c) suppose que CoinGecko et defillama servent les quatre actifs avec la même cadence : à lire au G0 (SHOGEN-S2BIS-PAIRES-1).

**Avant le sceau : oui** pour les formules (elles entrent au paquet, v3 l.215) ; les valeurs sont des sorties de CALIB-ACTIFS, avant le sceau aussi.

## Q3 — Seconde vague : forme, et lecture de la condition du G0

**Ce que disent les pièces.** §7 n° 5 (DÉC l.105) : décalage du sceau d'une à deux semaines **si** le G0 de CALIB-ACTIFS établit des historiques à 1 minute pour ≥ 4 places par classe ; « sinon ETH et stables passent en seconde vague et le sceau BTC n'est pas décalé ». v3 l.187 le lit littéralement (une classe en défaut envoie les trois en seconde vague) et pose la question ; v3 l.451 note qu'une lecture classe par classe « n'est pas écrite ». Faits connus : USDC/USD n'a que trois places fiat (Kraken, Bitstamp, Bitfinex ; Coinbase n'a pas la paire, v3 l.170 [2nd, SC C2]) ; Gemini liste la paire (v3 l.187 [2nd, P6 C3]). F3 est hors décision (DÉC l.21 ; v3 l.200) ; F2 est en séquence fixe et ses énoncés sont scellés (DÉC l.101). La question de valeur q. 9 (v3 l.396) demande à l'investisseur de choisir entre sceller BTC tout de suite et décaler. Les décodeurs ETH/USDC/USDT et de l'ensemble témoin font partie du collecteur réécrit (v3 l.229).

**Lecture de la condition.** Options : (i) tout-ou-rien (lecture littérale) ; (ii) **classe par classe** ; (iii) classe par classe pour F2, et pour F3 une condition propre.

**Recommandation : (iii).** Motifs :
1. La condition « ≥ 4 places » protège la calibration de τ (la médiane LOO des clôtures demande au moins 4 séries). Elle n'a de sens que par classe : ETH a ses historiques (Coinbase, Binance, Kraken, Bitstamp sont tous dans le pool) et serait envoyé en seconde vague à cause d'USDC, dont le pool fiat compte trois places par construction (v3 l.170). Sous (i), la condition est presque sûrement fausse pour USDC/USD, donc la seconde vague est presque sûrement imposée aux trois classes : la correction n° 5 se contredirait avec le §7 n° 3 (« pool USDC/USD fiat à trois places », DÉC l.103) [inféré].
2. Pour F3, hors décision, l'enjeu de pré-enregistrement est faible : un τ de place calibré sur 3 séries (médiane LOO de 2 = moyenne) est imprécis, mais la sortie est étiquetée « exploratoire, hors décision » et F3 est « presque sûrement NON ÉVALUABLE sans décrochage » (v3 l.210). Proposition : pour F3, le G0 exige ≥ 3 places **ou** passe en « planchers seuls » (τ_places = plancher d'oracle 0,375 %, déclaré), sans seconde vague. Une seconde vague pour une mesure hors décision coûte des semaines de location pour un résultat attendu « rien à signaler » (q. 11, v3 l.398).
3. Pour F2, la lecture classe par classe garde la séquence BTC → ETH dans le même paquet, qui est tout son intérêt (co-écart inter-classe par hôte, v3 l.208) ; une seconde vague d'ETH perd la synchronie avec BTC et rend la « puissance de la séquence » (v3 l.159) sans objet.

**Forme de la seconde vague, si elle a lieu.** Options : (a) mêmes observateurs, **après** le rendu BTC (séquentielle) ; (b) mêmes observateurs, **en parallèle**, second paquet scellé avant son propre T_début_2 ; (c) autres observateurs ; (d) collecte jointe et sceau de F2/F3 après la collecte, sous D.2-bis (comme S2, scellée après coup).

**Recommandation : (b).** Le collecteur gelé lit déjà les quatre classes dès T_début_1 (ajouter un décodeur après le sceau changerait le commit, v3 l.256) ; le second paquet ne porte que τ, σ, énoncés, cellule cible d'ETH, seuil de P_j et sa graine propre (v3 l.196 : « une seconde vague a sa propre suite et sa propre graine ») ; il est scellé avant T_début_2 ≥ genTime + 24 h, avec go écrit (forme de v3 l.214) ; les lectures ETH/stables entre T_début_1 et T_début_2 sont **hors inférence**, comme la calibration de S2 (v3 l.180, l.218), déclarées ; n_s et T_max de la vague 2 sont ceux de BTC (v3 l.159), donc T_fin_2 = T_fin_1 + (T_début_2 − T_début_1) : location prolongée du décalage seulement (quelques semaines × fourchette haute ≈ 56 €/mois, STATS Q6 ; [calc : 2 à 4 semaines ≈ 26 à 52 € HT]). (a) expose les rédacteurs de la vague 2 aux résultats de BTC (acceptable mais à déclarer, D.3-bis) et double la durée de location ; (c) perd la continuité des identités o, des ASN et du rodage ; (d) est la forme de S2 (scellée après la collecte), que la révision 3 a voulu quitter (v3 l.214) : à n'admettre que pour F3, hors décision, si l'investisseur refuse tout décalage.

**Risques** : si T_début_2 tombe après la fin d'une strate BTC, les strates ne se recouvrent plus et le co-écart inter-classe par hôte perd ses fenêtres communes [inféré] ; deux graines dans un même dépôt de paquets : nommer clairement « paquet-1 (BTC) », « paquet-2 (ETH, stables) » ; la rotation jointe par hôte (D-2) reste intra-classe pour la décision, donc rien ne change pour BTC.

**Avant le sceau : oui pour la lecture classe par classe** (elle décide du contenu du paquet-1) ; **la forme de la vague au G0 de CALIB-ACTIFS**, mais le collecteur gelé doit déjà porter les flux des quatre classes et de l'ensemble témoin, quel que soit le choix.

## Q4 — Vote de la variable d'état

**Ce que disent les pièces.** D-3 : P_j = |médiane − 1| imprimée par fenêtre, analyse conditionnelle au-delà d'un seuil scellé (DÉC l.28-30) ; §7 n° 3 : ensemble témoin USDC/USDT chez OKX, Uniswap, Curve, hors des classes USD (DÉC l.103) ; v3 l.208 propose [inféré] : P_j par fenêtre et par observateur sur l'ensemble témoin ; fenêtre « en décrochage » si au moins q_j observateurs valides mesurent P_j > seuil. Le §2.2 pt 6 (v3 l.94) a tranché, pour les écarts, « par observateur puis consolidé » et écarté le prix consolidé entre observateurs.

**Options.**
- (a) **Vote binaire à q_j** sur « P_j(o) > seuil » (règle proposée).
- (b) Médiane des P_j(o) des observateurs valides, comparée au seuil (prix consolidé entre observateurs).
- (c) Aucune consolidation : analyse conditionnelle par observateur, puis vote sur les écarts comme d'habitude.
- (d) Vote à q_j avec persistance (état « décrochage » tenu tant que la condition est vraie sur ≥ k fenêtres consécutives).

**Recommandation : (a), confirmée, avec trois précisions.** Motifs : les mêmes que v3 l.94 : mêler des prix lus à des instants différents par quatre observateurs créerait un P_j que personne n'a lu (b) ; (c) ne donne pas une variable d'état unique par fenêtre, ce que l'analyse conditionnelle demande ; (a) est un vote simple, recalculable par un tiers, homogène avec §2.2 pt 3. (d) ajoute un paramètre d'échelle (k) de la nature de ℓ, que la révision 2 a voulu éviter (v3 l.132) ; inutile : un décrochage dure des heures, le vote par fenêtre le suit tout seul [inféré]. Précisions :
1. **N_témoin** : un observateur ne vote sur P_j que s'il a au moins 2 lectures `ok` du témoin dans j (3 sources : OKX, Uniswap, Curve ; la médiane de 2 est une moyenne, déclarée) ; sinon il est « sans voix » sur l'état. Si moins de 2 observateurs valides ont voix, l'état de j est **indéterminé** ; les fenêtres indéterminées sont comptées à part et exclues de l'analyse conditionnelle, non de la strate.
2. **Seuil scellé** : 0,5 % (50 points de base) en règle, grille {0,25 ; 0,5 ; 1 ; 2} % imprimée [inféré : les décrochages de 2022-2023 que D-9 veut rejouer, DÉC l.69, dépassent largement 1 % ; 0,5 % reste au-dessus du bruit d'une paire stable/stable, dont les écarts des places sont de l'ordre de 1e-4 à 1e-3 — à confirmer sur l'historique de CALIB-ACTIFS, avant le sceau, sur des données disjointes]. Le rejeu historique de D-9 (v3 l.265) est le test public de ce seuil : s'il est fait avant le sceau, il le calibre sur des données disjointes ; sinon le seuil reste [inféré] et déclaré.
3. **Limite écrite** : le témoin USDC/USDT mesure le décrochage **relatif** des deux stables ; un décrochage joint contre l'USD (les deux à 0,97) laisse P_j ≈ 0 : le témoin est aveugle à ce cas, couvert seulement par le descriptif « écart au pair des médianes des classes USD » (v3 l.208), qui lit les données testées. Et OKX est un hôte du pool BTC (v3 l.165) : une panne d'OKX retire une voix au témoin dans la fenêtre même où elle fait un écart BTC ; d'où la règle N_témoin ≥ 2 et l'impression de la fraction de fenêtres indéterminées par strate.

**Risques** : seuil trop bas → analyse conditionnelle sur des fenêtres « calmes », diluée ; trop haut → aucune fenêtre en 16 semaines (q. 11 déjà posée) : la grille couvre les deux ; dépendance du témoin aux RPC (Uniswap, Curve : un hôte RPC chacun, v3 l.171) : une panne de RPC n'est pas un décrochage, elle rend l'observateur sans voix, c'est voulu.

**Avant le sceau : oui**, seuil, vote et N_témoin entrent au paquet (v3 l.215 : « variable d'état P_j, son ensemble témoin, son seuil conditionnel »). Enjeu faible : tout est hors décision.

## Q5 — Statistique S sur les données

**Ce que disent les pièces.** DÉC §8 (l.122) : S = Σ_j C(m_j, 2) évaluée par SIM-PUISSANCE-BIS en sensibilité ; statistique de décision seulement pour une campagne ultérieure à pool élargi. v3 l.208 : « la statistique S n'est évaluée qu'en simulation » ; v3 l.453 : l'imprimer sur les données coûterait peu [inféré du rédacteur]. La loi de rotation existe déjà (v3 l.196) ; les séries sont des masques de bits (v3 l.138).

**Options.**
- (a) Simulation seule (DÉC §8 tel quel).
- (b) **Imprimer S sur les données, hors décision**, avec sa loi de rotation (mêmes r, même graine, même R), C_S, S_crit, S̄_rot.
- (c) (b) et S en sensibilité nommée de la décision.

**Recommandation : (b).** Motifs : (i) coût nul en construction : S = Σ_{u<v} bit_count(D_u & D_v) sur les masques déjà rotés, 45 popcounts par rotation, contre les ET de paires que K demande déjà [calc, inféré] ; (ii) S est la statistique qu'une campagne à pool élargi utiliserait (DÉC l.122) : la mesurer sur un pool de 10 donne, avant cette campagne, une mesure réelle de son comportement (dispersion de la loi de rotation, rapport S/K), là où SIM-PUISSANCE-BIS ne donne qu'un modèle homogène (v3 l.161) ; (iii) hors décision, elle n'entame aucun α. (c) est à écarter : « sensibilité » de la décision suggère qu'un désaccord entre K et S aurait un sens pour le verdict ; or S et K sur le même pool sont deux lectures de la même co-occurrence, et la liste des sensibilités (v3 l.208, (i) à (viii)) porte des variantes de la **règle**, pas d'autres statistiques.

**Garde à écrire d'avance** (jardin des chemins qui bifurquent [inféré]) : le paquet porte la phrase « la valeur de S, son C_S et sa loi ne changent aucune valeur de R1-2 ; un C_S ≤ 99 avec C_s ≥ 100 (ou l'inverse) est une trouvaille descriptive publiée, jamais un REJETTE ni un NE REJETTE PAS » ; S n'a aucune phrase du registre doc 09 ; elle est imprimée dans le bloc hors décision, après le verdict.

**Risques** : lecture publique « S aurait rejeté » : couverte par la phrase ci-dessus et par l'étiquette ; aucun risque de calcul.

**Avant le sceau : oui**, parce que la liste hors décision du §2.7 pt 9 est scellée et que le script d'exécution unique est scellé (v3 l.217) ; décision à prendre au G0 de RECALC-BIS, qui précède le sceau.

## Ce qu'une réponse change au budget ou à la durée

- q. 1, 2, 4, 5 : texte du paquet et code des lots COLLECTE-BIS, CALIB-ACTIFS, RECALC-BIS ; budget et durée inchangés.
- q. 3 : si seconde vague (b), location prolongée du décalage T_début_2 − T_début_1 (2 à 4 semaines, ≈ 26 à 52 € HT à la fourchette haute de STATS Q6 [calc]) ; lecture classe par classe : évite une seconde vague d'ETH presque certaine sous la lecture littérale, donc économise plutôt qu'elle ne coûte.

## Points à porter dans l'ADR (liste fermée, propositions de texte)

| où (v3) | texte actuel | texte proposé |
|---|---|---|
| l.187 et l.451 | « en lecture littérale de la correction n° 5, une classe en défaut envoie ETH et les stables ensemble en seconde vague » | « la condition se lit classe par classe ; pour F3, hors décision, ≥ 3 places ou planchers seuls, sans seconde vague ; forme de la vague : second paquet, mêmes observateurs, même collecteur gelé, T_début_2 ≥ sceau_2 + 24 h, lectures antérieures hors inférence » (sous réserve de l'orchestrateur, qui a signé le §7) |
| l.185 | « ils le sont au G0 de CALIB-ACTIFS, avant tout calcul » | ajouter les formules de la q. 2 ; les valeurs restent au G0 |
| l.208 | « la statistique S n'est évaluée qu'en simulation (§2.4 h ; §8.2, question 5) » | « S imprimée sur les données, hors décision, même loi de rotation ; phrase de garde » |
| l.208, l.215 | variable d'état : vote à q_j, seuil « scellé » sans valeur | ajouter N_témoin ≥ 2, état indéterminé, seuil 0,5 % et grille, limite « décrochage joint » |
| l.256 | « sa forme (machine, lecteurs, moment de lecture) est à fixer avant le sceau » | « carte au collecteur scellé, processus et journal séparés, hors de δ ; aucune lecture avant le rendu ; sources non prêtes au gel : après le rendu » |
