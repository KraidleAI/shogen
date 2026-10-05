# AVIS advisor — lot SIM-BIS, tranche 2 (SB-3, SB-4) : les douze questions de conception de la couche des sources

- **Gate 0** : modèle résolu `claude-fable-5-1`, effort `medium` (explicite), rôle advisor (CLAUDE.md §7, amendement du 2026-09-18).
- **Date** : 2026-10-05. **Statut** : avis ; rien n'est décidé ici ; l'adjudication revient à l'orchestrateur.
- **Brief** : `…/sim2/g2/BRIEF-AVIS-SIM-T2.md` [lu]. **Pièces lues** [lu] : `…/sim2/g2/RAPPORT-WORKER-SIM-T2-transcrit.md` en entier (« RW l.n ») ;
  `docs/adr-0029/g0-sim/G0-SIM-BIS.md` en entier, ajout daté compris (« G0 l.n ») ; `docs/adr-0029/g0-sim/PROPOSITION.md` en entier
  (« prop. l.n ») ; `docs/adr-0029/g0-sim/AVIS.md` en entier (« AVIS l.n ») ; `docs/adr-0029/ADR-0029-campagne-S2-bis.md` l.1-229
  (§1, §2.1 à §2.8 ; « ADR l.n ») ; `docs/adr-0029/AVIS-STATS.md` en entier ; `docs/adr-0029/plan-s2bis/episodes.txt` en entier
  (« EP l.n ») ; code livré `…/sim2/etapes-784ebd2/rb4b/scripts/sim-bis/sources.py` en entier (« src l.n ») et
  `…/rb4b/scripts/sim-bis/parametres.json` en entier (« prm l.n ») ; `…/sim2/BRIEF-SIM-T2.md` en entier ; `docs/09-vocabulaire.md` l.1-60.
  Aucune commande lancée ; aucun sha256 recalculé ; les mesures du worker (temps, planchers, mutants) ne sont pas vérifiées.
- **Attestation (forme D.3)** : aucune pièce de la liste D.2 ouverte ; aucun `*.jsonl` ; rien de `docs/15-*`, `docs/16-*`,
  `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/` ; aucun rendu,
  aucun JOURNAL. Aucune donnée de S2-bis n'existe. Exposé aux valeurs **de S2** post-rendu que portent l'ADR §1.1 et EP (taux par
  unité, histogrammes, FIV_série) : sans effet sur S2-bis (ADR l.228, D.3-bis). Aucun fichier suivi modifié ; seul ce fichier est écrit.
- **Conventions** : [lu], [calc] (calcul de tête de l'advisor sur un [lu]), [inféré]. **[G0]** = change la lettre du G0 (ajout daté) ;
  **[E0]** = valeur ou mécanisme à sceller dans `parametres.json` ou le README avant l'épinglage E0 (E-S-04), parce qu'il n'est fixé
  ni par le G0 ni par l'ADR et qu'un choix après lecture d'une sortie serait une déviation. « Adopté » = choix du worker tel quel.

## 1. En bref

1. **Aucune des douze questions ne change la lettre du G0** : aucun [G0]. Six portent une valeur ou un mécanisme à sceller avant
   E0 : Q-T2-2, Q-T2-5, Q-T2-6, Q-T2-7, Q-T2-10, Q-T2-11.
2. J'adopte **dix** choix tels quels (Q-T2-1, 3, 4, 5, 6, 7, 8, 9, 10, 12) et j'en **modifie deux** : Q-T2-2 (le mécanisme est
   adopté, mais E′ doit être tirée dans les seuls segments dégradés de Z, à loi égale, avant E0, pour le coût) et **Q-T2-11** (indice
   de flux ancré sur la liste D1-bis scellée de l'ADR, non sur la liste opérationnelle `calibration.unites`, sinon le changement
   d'identifiants prévu par Q-S-07 déplace tous les tirages entre la provisoire et la finale). Aucun rejet.
3. Trois constats que les pièces imposent d'écrire au paquet : (i) **la composante d'écart propre F est presque nulle sur EP** (écart
   − panne = 0 cellule pour 6 hôtes sur 10 en calme et 9 sur 10 en stress, maximum 3/24 585 chez gemini, EP l.13-92 [calc]) : F est
   en pratique la seule composante hors-enveloppe de Q-S-21, et la sensibilité « × 2 » d'E-S-09 est à peu près vide ; (ii) la
   couche des sources seule coûte ce que la proposition prévoyait pour la chaîne entière (RW l.26, prop. l.425) : le seuil A-3 de
   72 h de mur (prop. l.559) entre dans la fourchette ; (iii) la loi jointe (calme, stress) d'un hôte n'est pas celle d'un processus
   unique en temps réel, mais **aucune statistique par strate n'en dépend** (suite comprimée par strate, ADR l.137) : limite écrite,
   pas de défaut.

## 2. Les douze questions

### Q-T2-1 — Un processus stationnaire par strate, régime indépendant d'une strate à l'autre. **Adopté**, limite écrite ; pas de [G0].

- Ce que fait le code : pour chaque strate, `union` tire un renouvellement alterné stationnaire **sur toute la grille** [0, horizon)
  au taux de la strate (src l.219-241), puis `pannes` et `ecarts` ne gardent que les fenêtres de la strate par `self.masques[s] &`
  (src l.250, l.268) ; le régime Z est tiré par (hôte, strate), lui aussi sur toute la grille (src l.207-217). « Coupé à chaque
  jonction » (RW l.29) veut donc dire : tronqué par le masque de strate, non redémarré.
- **Niveau** : le test tranche strate par strate sur la suite comprimée des fenêtres évaluables de la strate (ADR l.137, l.199-200 ;
  E-S-23, prop. l.172). Dans la suite comprimée du calme, le voisin de vendredi 23:59 est lundi 00:00 : les deux fenêtres viennent du
  **même** processus « calme », continu sur la grille pendant les 2 880 fenêtres du week-end ; la corrélation sérielle à la jonction
  est celle d'un processus réel de même paramètres sur le même intervalle. Même chose en stress (dimanche 23:59 puis samedi 00:00 de
  la semaine suivante, 7 200 fenêtres d'écart, au-delà du plus grand τ_D de la grille E1, 4 320, prop. l.197). L'indépendance entre
  le processus « calme » et le processus « stress » n'affecte que la loi **jointe** des deux strates, que ni la règle (Bonferroni,
  ADR l.204), ni la règle de niveau du §4 (par strate, prop. l.258-266), ni le taux familial BTC puis ETH (par strate, prop. l.266)
  ne lisent. Le niveau mesuré par strate est donc celui du modèle voulu [inféré]. Les unités restent tirées indépendamment les unes
  des autres sous H0, ce qui est la seule hypothèse que la rotation exige (ADR l.135).
- **Statistique K et runs** : le taux marginal par strate est exact (processus stationnaire, part r = p, src l.84-96, l.159-170),
  donc n·P_more de chaque strate est celui de la proposition (prop. l.305-307) ; les runs de I_t se comptent sur la suite comprimée
  (E-S-28), où les jonctions n'interrompent rien de plus que dans la réalité. Un seul effet de second ordre : un épisode tronqué par
  le masque est raccourci, alors que la loi « tous épisodes » d'EP compte déjà les censurés à leur longueur vue (G0 l.33 pt 2) :
  double raccourcissement, à ajouter à la limite déjà écrite pour SHOGEN-SIM-BIS-STRESS-EPISODES-1 (écart des moyennes mesuré par
  le réviseur : −0,035 à +0,134 fenêtre en calme, G0 l.33).
- **Puissance** : les incidents (E-S-15) sont un seul processus sur toute la grille (src l.392-414), non coupés : la puissance à la
  cible ne dépend pas de ce choix.
- Pourquoi ne pas faire un seul processus réel à taux commuté : les taux d'EP diffèrent d'un facteur 3,5 entre strates pour
  chainlink (0,0028 contre 0,0099, EP l.25, l.65) et 3 pour defillama (EP l.37, l.77) ; un processus unique à taux commuté aux
  jonctions n'est stationnaire dans aucune strate au voisinage des jonctions, et E-S-38 calibre le régime **par strate**
  (prop. l.197). La construction du worker est la plus simple qui donne des marges exactes par strate et un régime calibrable par
  strate. Item SHOGEN-SIM-BIS-SOURCES-STRATES-1 (RW l.58) : à former comme **limite écrite** (constat : « la loi jointe calme/stress
  d'un hôte n'est pas celle d'un processus unique en temps réel ; sans effet sur les valeurs par strate »), sans code.

### Q-T2-2 — Régime E ∪ (E′ ∩ Z), E′ tirée fenêtre par fenêtre (L = 1), r′ ≥ 1 refusé. **Adopté sur le fond, modifié sur le lieu du tirage d'E′** [E0].

- **La calibration C0/C1/C2 garde son sens.** FIV_série(ℓ) mesure l'inflation de variance des sommes par blocs de ℓ fenêtres
  (EP l.93) ; sur EP, elle vaut 1,19 à ℓ = 2, 1,40 à ℓ = 3, 2,73 à ℓ = 10, 9,2 à ℓ = 60, 22,9 à ℓ = 240 en calme (EP l.129-140).
  Les longueurs d'épisodes (moyennes 1,05 à 1,45, EP l.13-52) n'expliquent que les premiers points ; ce que la famille d'E-S-12 doit
  reproduire, c'est la croissance à ℓ ≥ 10, qui est une modulation du **taux local** à l'échelle τ_D : elle dépend de (φ, κ, τ_D), pas
  de la loi des longueurs à l'intérieur du régime dégradé [inféré]. E′ à L = 1 dans Z produit exactement cette modulation (points
  supplémentaires groupés dans les segments dégradés de Z) ; elle sous-estime seulement, en régime dégradé, la part du FIV à ℓ = 2 et
  3 que des épisodes de 2 à 6 fenêtres donneraient. Sur les 17 points ℓ de la grille, 5 sont à ℓ ≤ 5 (prm l.23) : le critère d'E1
  (somme des carrés des log, prop. l.197) peut pousser légèrement vers un κ ou un τ_D plus grands pour compenser. **À écrire** : E1
  imprime le résidu log FIV par ℓ du point C2, pour que cette part se lise ; aucun changement de critère.
- **Pourquoi pas E′ en renouvellement à loi empirique** : la part d'un renouvellement à pauses d'au moins une fenêtre est bornée par
  μ/(μ + 1) (src l.91-96) ; à f = 1 (E1, E-S-38), κ = 50 et φ = 0,01, defillama en stress (p = 0,0198, EP l.77) donne
  r_E = p/(1 − φ + φκ) = 0,0133 et κ·r_E = 0,66 > μ/(μ + 1) ≈ 0,50 [calc] : la grille E1 serait infaisable pour ses points
  extrêmes. Le worker a raison de passer par L = 1 ; c'est la convention de S2 (src l.222, G0 SIM-NIVEAU cité).
- **Faisabilité, formule fermée** : r′ = r_E(κ − 1)/(1 − r_E) ≥ 1 ⇔ r_E ≥ 1/κ ⇔ **p_A ≥ φ + (1 − φ)/κ** [calc]. Le cas liant est
  (φ = 0,01, κ = 50) : seuil 0,0298. Sur les cellules du §5.1 : à f = 1 sans dérive (N0 est C0, P-grille à C2 au plus), le plus grand
  p_A est defillama stress 0,0198 < 0,0298 ; à f = 0,3 avec dérive de maximum 1,9 (N8, N9) : bitstamp calme 0,3 × 1,9 × 0,0193 =
  0,0110 ; avec transitoire × 3 (X2) : 0,0174 ; tous sous le seuil [calc]. Le refus `SOURCES/taux` (src l.232-233) ne devrait donc
  jamais se déclencher sur les cellules pré-déclarées ; il reste utile comme garde. L'item SHOGEN-SIM-BIS-REGIME-FAISABILITE-1
  (RW l.59) est à former avec cette formule et la liste des cellules à contrôler quand C1 et C2 sont épinglés ; une cellule à f = 1
  **et** dérive n'existe pas et ne doit pas être ajoutée sans ce contrôle.
- **Modification (coût, [E0])** : E′ est tirée sur toute la grille puis intersectée avec Z (src l.234-235). À r′ de 0,1 à 0,66 sur
  241 920 fenêtres, c'est de l'ordre de 10⁴ à 10⁵ segments par série et par strate, pour n'en garder que la part φ (1 à 10 %)
  [inféré] ; c'est vraisemblablement une part notable des 0,29 s par réplication (RW l.26), et elle croît avec κ, donc à C2. Tirer E′
  dans les seuls segments dégradés de Z (même loi de Bernoulli fenêtre par fenêtre, même flux) donne une loi identique et divise le
  coût par environ 1/φ [inféré]. Cela change l'ordre de consommation du flux, donc les octets des sorties : licite **avant E0 seulement**
  (E-S-04). À décider sur la mesure E-S-46 de SB-11, pas à l'estime ; si le worker la fait, test d'égalité des marges et du FIV à
  5 erreurs-types (oracle d'E-S-39) comme preuve.

### Q-T2-3 — H sur l'histogramme « panne », F sur l'histogramme « ecart », différence écartée, regroupement par type. **Adopté.**

- E-S-10 nomme « les histogrammes d'EP » par unité et par strate (prop. l.149) ; EP n'en donne que deux, « panne » et « ecart »
  (EP l.12-92). Un histogramme « différence » n'existe pas et serait presque vide ou négatif par cellule (écart − panne = 0 à 3
  cellules, voir Q-T2-4). Le regroupement en stress par type (src l.147-156) applique E-S-10 et l'avis Q-S-04 (AVIS l.32) tel quel.
- Conséquence à déclarer : comme l'écart d'EP comprend la panne, l'histogramme « ecart » est, à 1 à 3 cellules près, l'histogramme
  « panne » (EP l.13-16, l.19-20, l.27-28) : la loi de F est en pratique la loi de H. Sans effet numérique, F étant presque nulle
  (Q-T2-4).

### Q-T2-4 — F des autres classes = même taux, même loi que BTC, réalisation indépendante, × `autres` ; hors-enveloppe par (hôte, classe, strate), ni × f ni amincie. **Adopté**, avec un constat à écrire au paquet.

- **Réalisation indépendante** : E-S-09 dit « F d'ETH et des stables = F de BTC du même hôte (déclaré) » (prop. l.148), E-S-08
  « la dépendance entre classes d'un même hôte est admise » (prop. l.147) — admise, non exigée. L'ADR fait porter la dépendance
  inter-classes par la panne de transport de l'hôte (H commune à toutes ses classes, ADR l.162, l.200 : rotations jointes par hôte) ;
  un écart de contenu (prix dévié, réponse vieillie) est propre au flux. La lecture « même loi, tirage propre » est la bonne ; la
  rotation jointe par hôte rend de toute façon la loi de K de chaque classe insensible à la corrélation entre classes d'un même hôte
  (ADR l.200). Ce qui en dépend : la puissance de la séquence d'ETH (ADR l.162), portée par H, donc par les incidents : second ordre.
- **Le constat qui compte** : sur EP, cellules d'écart − cellules de panne = 0 pour binance, bitstamp, coinbase, coingecko, kraken,
  okx en calme (EP l.13-16, l.21-24, l.29-36, l.45-52) ; 2 pour bitfinex et chainlink, 1 pour defillama, 3 pour gemini (EP l.17-20,
  l.25-28, l.37-40, l.41-44) ; en stress, 2 pour gemini et 0 pour les neuf autres (EP l.53-92) [calc]. Le plus grand p_écart_propre
  vaut 3/24 585 = 1,2·10⁻⁴, soit 3,7·10⁻⁵ à f = 0,3, contre 2,5·10⁻⁴ par fenêtre pour la composante hors-enveloppe de référence
  (prop. l.148, l.578). **F est donc, à 7 fois près au moins, la seule composante hors-enveloppe** ; la sensibilité « × 2 » sur
  `autres` (src l.263) multiplie une quantité presque nulle. C'est cohérent avec S2 (« R1 n'a mesuré que la disponibilité »,
  ADR l.43), mais il faut l'écrire : le modèle nul synthétique teste K sur des pannes et sur le hors-enveloppe de Q-S-21, presque
  jamais sur des écarts de contenu propres. Je recommande que SB-11 imprime, en tête de chaque cellule, le taux effectif de F par
  (hôte, classe, strate) séparé en « propre » et « hors-enveloppe », et que la phrase soit portée par SHOGEN-SIM-BIS-TAU-NEUF-1
  (prop. l.607), dont c'est le sujet.
- **Ni × f ni amincie** : la grille {0 ; 2,5·10⁻⁴ ; 10⁻³} est « par fenêtre », absolue (prop. l.148) : f, qui partage le bruit de S2
  entre sources et observateur (AVIS l.31), ne s'y applique pas ; l'amincissement par dérive modélise la dérive des défaillances de
  la source, non un artefact de seuil : simplification cohérente, à déclarer dans le README. Un seul (hôte, classe, strate) par flux
  (src l.266) : l'indépendance entre classes du hors-enveloppe correspond à des τ distincts par classe (ADR l.185-190).

### Q-T2-5 — Pannes longues sur H seulement ; 1 h, 1 jour, 3 jours également probables. **Adopté** [E0], diagnostic à imprimer.

- Sur H seulement : une panne d'une heure à trois jours est une indisponibilité de l'hôte (ADR l.96, « panne de la source ou de sa
  livraison globale »), donc commune à ses classes (E-S-08) ; un écart de contenu de trois jours sans panne n'a pas d'analogue dans
  EP (max 6 fenêtres, EP l.29). Adopté.
- Poids : E-S-11 énumère trois durées et « une part déclarée du taux marginal » (prop. l.150), sans poids. Deux lectures : (a) poids
  égaux par **nombre** d'épisodes (worker, src l.182-184) ; (b) poids égaux par **part de temps** (nombres ∝ 1/durée, 72 : 3 : 1). Repères
  [calc, sur EP et N4 à f = 0,3, part 0,5] : la somme des taux de panne calme des 10 hôtes vaut 0,0561 (EP l.13-52), d'où une part
  longue totale 0,0084 ; sous (a), longueur moyenne 1 940 fenêtres, environ **1 épisode long par réplication sur la grille de 24
  semaines**, dont un tiers de 3 jours ; sous (b), moyenne 170 fenêtres, environ 12 épisodes dont 11 d'une heure et 0,2 de 3 jours. N4
  veut « des épisodes jusqu'à plusieurs jours » (ADR l.205 pt 7) : (a) les fait exister dans une réplication sur trois environ, (b)
  presque jamais. Je recommande **(a)**, la lecture littérale de la liste, avec le diagnostic : SB-11 imprime la distribution du nombre
  d'épisodes longs réalisés par durée sous N4, et la phrase de limite éventuelle de N4 dit que la cellule mélange des réplications
  avec et sans panne de plusieurs jours. Poids scellés dans `parametres.json` avant E0 (item SHOGEN-SIM-BIS-DERIVE-AMPLITUDE-1,
  RW l.58, qui les porte).

### Q-T2-6 — Dérives : valeurs non fixées par le G0. **Adopté** pour les cinq valeurs [E0], avec leur source.

| valeur | choix du worker (prm l.41 ; src l.298-345) | source ou motif | avis |
|---|---|---|---|
| durée de la tendance | W·10 080 fenêtres (durée nominale), puis tenue jusqu'à T_max | E-S-13 (a) « au long de la campagne » (prop. l.152) ; les n_s sont atteints vers W semaines à 95 % d'évaluables (ADR l.158) ; prolonger linéairement jusqu'à T_max sortirait des bornes 0,1 et 1,9 | adopté |
| amplitude du saut | de 0,1 à 1,9 ou l'inverse, sens tiré, instant uniforme (jour, puis fenêtre) | mêmes bornes que (a) ; avec un instant uniforme sur la durée nominale, le multiplicateur moyen vaut 1 [calc], donc N9 garde le taux marginal de N1 et reste comparable ; un saut 1 → 1,9 changerait la marge | adopté ; écrire « rapport 19, même enveloppe que la tendance » |
| unités sautées | 3 hôtes sans remise parmi les 10 | E-S-13 (b) « sur trois unités » (prop. l.152) | adopté ; la première unité (non décalée) peut être tirée, sans effet sur le niveau (prop. l.514) |
| panne initiale | 4 320 fenêtres (3 jours, la plus longue des pannes longues) sur un hôte tiré parmi les 9 décalés | E-S-13 (c) « commence la campagne dans une panne longue » (prop. l.152) ; E-S-11 ; nuance Harris (ADR l.143 ; prop. l.69-71 : la première unité peut ne pas être stationnaire, le scénario vise une unité décalée) | adopté ; la part visible en stress dépend du T_début tiré (0 à 6 jours, Q-S-08) : à imprimer |
| transitoire | × 3 sur 10 080 fenêtres | fixé par E-S-13 (d) (prop. l.152) | adopté |

- Ni sur incidents ni sur unités faibles (RW l.37) : aucune cellule du §5 ne combine une dérive avec un incident ou une unité faible
  (prop. l.284-301, l.311-320) ; à écrire comme limite de portée du générateur, pas comme refus.
- Construction par amincissement (src l.307-311) : la série est tirée au taux M·p puis chaque épisode gardé avec la probabilité
  m(début)/M : taux local m(t)·p, longueurs inchangées, régime Z et pannes longues amincis avec le reste. C'est juste pour le taux ;
  la part de temps après amincissement est approchée au second ordre (pauses non géométriques) : à déclarer. Le test T-GEN-1 à 5
  erreurs-types (prop. l.387) ne couvre pas le taux aminci : un oracle « taux moyen de la série amincie = moyenne de m(t)·p à 5
  erreurs-types » manque ; à demander à la G2 ou à SB-11.

### Q-T2-7 — Pools provisoires ETH 10, USDC 8 (sans coinbase ni okx), USDT 10. **Adopté comme provisoires** [E0 pour la provisoire ; remplacés avant la finale].

- Le G0 veut une exécution provisoire sur le pool de l'ADR puis une finale après le gel des pools (G0 l.29-31 ; Q-S-17, AVIS l.80) ;
  les pools sont lus dans `parametres.json` avec leur source (E-S-03, E-S-07). Le worker marque [inféré] ce qu'il infère (prm l.45) :
  conforme.
- Réserve à porter au constat PAIRES-1 (RW l.61) : l'ADR exclut « les paires stable/stable des classes USD » (ADR l.173) et ne
  nomme, pour USDC/USD contre le dollar fiat, que Kraken, Bitstamp, Bitfinex et Gemini (ADR l.173). La présence de binance dans
  USDC et de binance et okx dans USDT (prm l.42-43) suppose une paire fiat que je ne trouve pas dans les pièces lues ; le worker
  l'infère de « cotes en USDT admises comme pour BTC » (prm l.45), tolérance que l'ADR accorde à BTC (ADR l.98) et refuse aux
  classes stables (ADR l.173). Sans effet sur BTC ni sur le niveau ; effet sur la fréquence provisoire de NON ÉVALUABLE en F3
  (P-F3, N ≥ 4 répondantes, ADR l.173) et sur ETH sans condition. Rien à changer maintenant : le gel des pools (SHOGEN-S2BIS-PAIRES-1)
  tranche ; mais la provisoire doit imprimer la composition employée avec la mention [inféré], et la G2 de S-3 contrôle que la finale
  recopie `formes.json` (AVIS l.73).

### Q-T2-8 — Incidents : débuts au taux ρ·w/86 400 par fenêtre de grille, D fixe ou géométrique coupée à T_max, chevauchements fusionnés, ajoutés à H. **Adopté.**

- « ρ par jour de strate » (E-S-15, prop. l.154) : un processus au taux ρ par jour calendaire sur la grille donne ρ par jour dans
  chaque strate, puisque les deux strates partagent la même grille et la même densité de fenêtres par jour [calc] ; les 7,6 et 3,04
  incidents attendus à 16 semaines (prop. l.246) se retrouvent à la censure près. Équivalent à la lettre, plus simple qu'un processus
  par strate, et surtout **continu** : un incident qui commence vendredi soir frappe les deux strates, comme dans la réalité.
- D fixe par défaut, géométrique en sensibilité (src l.408-411) : Q-S-05 (a) et (b) adoptées (AVIS l.72). Hôtes tirés par incident,
  « chacun » à π ou « parmi » k sans remise (src l.374-389) : Q-S-05 (c). Un incident « chacun des 7 à 0,7 » touche au plus un hôte
  avec probabilité 0,3⁷ + 7·0,7·0,3⁶ ≈ 0,4 % [calc] : négligeable, à déclarer.
- Fusion des chevauchements et ajout à H (src l.413-414 ; src l.281-283) : conforme à ADR l.162 (panne de transport, toutes les
  classes), condition de la cible d'ETH (E-S-15). Au plus un début par fenêtre (Bernoulli) : à ρ ≤ 0,5 par jour, la probabilité de
  deux débuts dans une même fenêtre serait ≈ 6·10⁻⁸ [calc] : sans objet.

### Q-T2-9 — Unités faibles : type « panne » (toutes les classes de l'hôte) ou « ecart » (BTC seul), un processus sur toute la grille. **Adopté.**

- E-S-16 (prop. l.155) et B.39 décrivent une unité à écarts fréquents et markoviens ; la forme « ecart, BTC seul » est le flux
  déviant de SHOGEN-FLUX-DEVIANT-1 (prop. l.556), la forme « panne » l'hôte peu fiable. Un processus en temps réel sur toute la grille
  (src l.364-371), de part p_w dans les deux strates : la faiblesse est une propriété de l'hôte, non de la strate. La chaîne
  (a, b) = (1 − 1/L, p/(L(1 − p))) et le cas L = 1 iid (src l.358-361) sont la convention de S2 citée.
- Le masque faible est ajouté par OU à H ou à F (src l.282-283, l.286-289) : le taux effectif de l'hôte faible vaut
  p_w + p_H(1 − p_w), non p_w : à déclarer ; sans conséquence sur le scénario (p_w ≥ 0,25 domine). À p_w = 0,4 et L = 1, l'unité
  faible a 60 % de « ok » : le seuil de flux presque mort 2·ok < n_s (ADR l.170) ne la retire pas, c'est précisément le cas
  d'absorption que l'item veut mesurer (prop. l.124).

### Q-T2-10 — Hôtes faibles, population des triplets, partenaire de l'unité faible : paramètres de cellule à pré-déclarer à SB-11. **Adopté** [E0] ; valeurs proposées.

- E-S-16 ne les fixe pas (prop. l.155) ; ce sont des paramètres de cellule au sens d'E-S-03, à sceller avant E0 et avant l'exécution
  provisoire (P-abs y figure, prop. l.338). Propositions, chacune avec sa source, à adjuger :
  - **population des paires et des triplets** : les 7 hôtes AS13335 (prm l.44), comme la paire de la cible (Q-S-05 (c), prop. l.502) :
    même population pour les trois formes de co-défaillance, ce qui rend la comparaison paire/triplet/unité faible lisible ;
  - **hôtes faibles** : les k premiers de la liste `as13335` dans son ordre scellé (bitfinex, chainlink, coinbase, coingecko, prm l.44),
    k ∈ {1 ; 2 ; 4} : déterministe, lisible, dans la population des incidents, et hors de la première unité (binance), ce qui garde
    au scénario « impliquant l'unité faible » un hôte décalé (nuance Harris, ADR l.143) ;
  - **partenaire de l'unité faible** : tiré par incident, uniforme parmi les six autres hôtes AS13335 (mode « parmi », imposés = l'hôte
    faible, k = 2, src l.385-389), par analogie avec la paire tirée de Q-S-05 (c) ; avec k ≥ 2 unités faibles, l'imposé est tiré
    uniforme parmi elles (src l.385) : à écrire ;
  - **bascule** (14 cellules, prop. l.155) : une seule unité faible, la première de la liste.
  Item SHOGEN-SIM-BIS-ABS-POPULATIONS-1 (RW l.60) : à former avec ces valeurs ou celles que l'orchestrateur préfère ; ce qui compte est
  la date, avant E0.

### Q-T2-11 — Indice de flux positionnel (h·S + s)·10 + k, ou par nom. **Modifié** [E0] : indice entier, mais ancré sur la liste D1-bis scellée.

- Le problème est réel et plus large que le retrait d'un hôte : l'indice h est le rang dans `calibration.unites` (src l.173-179), et
  Q-S-07 prévoit que la finale emploie les identifiants de la configuration scellée de COLLECTE-BIS, dont l'ordre des octets diffère
  des noms courts (`api-pub.bitfinex.com` avant `api.binance.com`, prop. l.511-512). Si la liste est alors retriée, **tous** les
  flux de toutes les séries changent entre la provisoire et la finale, et plus rien ne permet d'attribuer une différence de sortie
  aux seuls pools et identifiants (ce que Q-S-17 promet : « la finale ne diffère que par les pools, les identifiants et ce qui en
  dépend », prop. l.561-562).
- E-S-41 fixe la forme du flux, `…|<composant>|<indice>` (prop. l.205), et la tranche 1 a adjugé « composants des flux en liste
  fermée sous schéma avant E0 » (G0 l.33 pt 3) : mettre le nom de l'hôte dans le composant romprait la liste fermée ; mettre une
  chaîne dans `<indice>` romprait la forme. **Proposition** : garder la formule entière, mais prendre h dans une liste
  `sources.indices_hotes` **scellée et immuable**, égale aux 10 hôtes D1-bis de l'ADR dans un ordre écrit (ADR l.168 ; EP l.8 :
  aucun retrait), distincte des listes opérationnelles ; refus nommé si un hôte d'un pool n'y figure pas ; un hôte retiré laisse
  son rang inemployé. Les k emplacements 0 à 9 (0 : hôte ; 1 + c : classe ; src l.175) restent. Même traitement pour les unités
  faibles, dont l'indice est aujourd'hui le rang dans `spec["hotes"]` (src l.370-371) : le rang dans `indices_hotes`. Coût : une
  dizaine de lignes dans `sources.py` et une clé de schéma ; à faire en correction G2 ou en diff de SB-11, **avant E0**. Pas de [G0] :
  E-S-41 ne dit pas comment l'indice est formé.
- Ce que cela n'apporte pas : la stabilité des sorties entre provisoire et finale n'est pas exigée (deux épinglages distincts, G0
  l.30-31) ; l'avantage est diagnostique et de lecture pour la G2 de S-3. Le niveau ne dépend d'aucun de ces choix (prop. l.514).

### Q-T2-12 — Le coût de la couche des sources seule égale l'estimation de la proposition pour toute la chaîne. **Adopté comme constat** ; conséquences.

- Mesuré par le worker : 0,29 s par réplication (N1), 0,34 s avec sauts, amorçage 4,7 s par processus (RW l.26) ; la proposition
  prévoyait 0,3 s « hors rotations » pour la chaîne entière (prop. l.425) et avait mesuré 2,10 s pour votes et quorum en tirage
  fenêtre par fenêtre (prop. l.423). Si la couche d'observateurs (SB-6) est écrite par sauts comme les sources, elle coûtera du même
  ordre que celles-ci, soit une chaîne de génération de 0,6 à 1 s par réplication [inféré]. Volume : E2 1,6·10⁵ réplications,
  E3 ≈ 2,2·10⁵ avec l'échelle aux trois niveaux (AVIS l.22), E1 2,6·10⁴ (prop. l.431-434) : environ 4·10⁵ réplications, soit 30 à
  40 h de CPU pour la seule couche des sources et 60 à 110 h pour la génération entière, à ajouter aux rotations (0,64 à 2,52 s par
  réplication sous H1 à R complet, prop. l.420 ; ≈ 560 rotations sous H0 à l'arrêt anticipé, prop. l.432) [calc, approximatif].
  **Le total plausible passe de 90-155 h à 150-250 h de CPU**, 40 à 60 h de mur sur 4 vCPU libres, le double sur un hôte partagé
  (prop. l.440) : le seuil A-3 de 72 h de mur (prop. l.559 ; G0 l.21) est dans la fourchette. Ce n'est pas une dette du worker :
  l'estimation de la proposition était [inféré] et E-S-46 prévoit la mesure sur le code commis avant toute campagne (prop. l.215).
- Où va le temps, d'après le code [inféré, non mesuré] : (i) deux processus par série (un par strate) sur toute la grille, chacun
  masqué (Q-T2-1) : nécessaire au modèle ; (ii) E′ tirée sur toute la grille puis intersectée avec Z (Q-T2-2) : réductible d'un
  facteur ≈ 1/φ à loi égale, avant E0 ; (iii) `masque` construit une chaîne de 241 920 caractères par série puis la convertit
  (src l.127-133) : remplaçable par une somme de ((1 << longueur) − 1) << début, sans changer un seul tirage ni un seul bit du résultat,
  donc licite à tout moment comme pure performance, à condition d'un test d'égalité ; (iv) la composante hors-enveloppe est tirée par
  renouvellement à pauses géométriques (src l.266-267), ce qui est déjà clairsemé.
- Recommandations : la mesure E-S-46 porte sur la chaîne entière à SB-11 **avant** toute décision d'optimisation ; les options (ii)
  et (iii) ne sont engagées que si la mesure le demande, et (ii) avant E0 seulement ; si le mur mesuré dépasse 48 h, Q-S-10 (b) et
  (c) s'appliquent (AVIS l.75) ; si 72 h, question A-3 à l'investisseur en langage clair (prop. l.623-625), jamais d'optimisation
  après E0. Constat porté par SHOGEN-SIM-BIS-CALCUL-1 (prop. l.606), comme le worker le propose (RW l.60-61).

## 3. Items proposés par le worker (RW l.58-61)

| item | avis |
|---|---|
| SHOGEN-SIM-BIS-SOURCES-STRATES-1 (Q-T2-1) | former comme limite écrite, constat resserré : « loi jointe calme/stress d'un hôte ≠ processus unique en temps réel ; sans effet sur les valeurs par strate » ; prix nul ; déclencheur : aucun (limite au paquet) |
| SHOGEN-SIM-BIS-DERIVE-AMPLITUDE-1 | former ; porte les valeurs de Q-T2-5 (poids 1 : 1 : 1) et Q-T2-6 (tableau) ; **à clore avant E0** par l'écriture dans `parametres.json` avec leur source |
| SHOGEN-SIM-BIS-REGIME-FAISABILITE-1 | former ; ajouter la formule p_A ≥ φ + (1 − φ)/κ et le contrôle par calcul sur les cellules du §5.1 et les 64 points d'E1 à f = 1 dès que C1 et C2 sont épinglés ; constat présent : aucune cellule pré-déclarée ne l'atteint [calc] ; règle : aucune cellule à f = 1 et dérive sans ce contrôle |
| SHOGEN-SIM-BIS-ABS-POPULATIONS-1 (Q-T2-10) | former ; valeurs proposées au §2 ; **à clore avant E0** |
| constat pour CALCUL-1 | adopter ; ajouter l'ordre de grandeur révisé (150 à 250 h de CPU [calc, approximatif]) et la liste des trois leviers avec leur licéité (avant E0 pour (ii), à tout moment pour (iii)) |
| constat pour PAIRES-1 | adopter ; ajouter la réserve « stable/stable exclues » (ADR l.173) sur binance et okx dans les classes stables |

Deux ajouts : (a) à SHOGEN-SIM-BIS-TAU-NEUF-1, le constat « F propre presque nulle sur EP ; F = hors-enveloppe en pratique ;
sensibilité × 2 vide » (Q-T2-4) ; (b) à SHOGEN-SIM-BIS-STRESS-EPISODES-1, le double raccourcissement (loi « tous épisodes » puis
troncature au masque, Q-T2-1).

## 4. Trois risques

1. **Calcul** (Q-T2-12) : la couche des sources consomme à elle seule l'estimation de la chaîne ; avec les observateurs et les
   rotations à R complet sous H1 et l'échelle aux trois niveaux, le mur peut atteindre le seuil A-3 sur un hôte partagé. Si
   l'optimisation est décidée après E0, c'est une déviation ; si elle est décidée à l'estime avant la mesure E-S-46, c'est du
   travail perdu : mesurer d'abord, à SB-11, sur la chaîne entière.
2. **Épinglage et attribution** (Q-T2-11) : l'indice positionnel sur une liste qui change d'ordre avec les identifiants (Q-S-07)
   fait que la finale ne partage aucun tirage avec la provisoire ; une divergence inattendue entre les deux ne pourrait être
   attribuée ni aux pools ni au code. À corriger avant E0, tant que c'est une ligne de conception et non une déviation.
3. **Sens de la calibration et contenu du modèle nul** (Q-T2-2, Q-T2-4) : avec E′ à L = 1, des épisodes doublement raccourcis et une
   F propre presque nulle, le modèle nul tire presque tout son groupement du régime Z et presque tout son K des pannes et du
   hors-enveloppe. C'est l'intention du G0 (C2 = « tout le groupement de S2 tient aux sources », prop. l.329-330), le cas le plus
   défavorable pour la rotation ; mais si C2 tombe au bord de la grille (κ = 50, τ_D = 4 320) et que la famille n'atteint pas la
   courbe d'EP, la limite de SHOGEN-SIM-BIS-FIV-IDENTIF-1 s'écrit (AVIS l.24) et la durée déclarée repose sur un artefact : d'où
   l'ordre déjà adjugé, PLAN-S2BIS-2 avant tout acte A-2 (G0 l.13-15). Les résidus par ℓ d'E1 et les taux effectifs de F par cellule
   sont les deux impressions qui permettent de le voir avant la finale.

## 5. Vérifications faites et ce que cet avis ne fait pas

Vérifiés [calc, de tête, sur EP et le code] : écart − panne par hôte et par strate (EP l.13-92) ; r′ = 0,66 pour defillama stress à
(φ, κ) = (0,01 ; 50) ; seuil p_A ≥ φ + (1 − φ)/κ et son application aux cellules du §5.1 ; multiplicateur moyen 1 d'un saut
0,1 ↔ 1,9 à instant uniforme ; ≈ 1 épisode long par réplication sous N4 à poids égaux ; équivalence « ρ par jour de grille » et
« ρ par jour de strate » ; probabilité ≈ 0,4 % d'un incident à au plus un hôte ; lecture de `union`, `pannes`, `ecarts`, `regime`,
`indice`, `incidents`, `faibles`, `touches`, `derives`, `amincir` contre les exigences citées. Non vérifiés : les mesures de temps,
les planchers, les mutants, les rouges, les sha256 du worker ; l'existence de paires fiat USDC/USD ou USDT/USD chez binance et okx
(pièces CALIB-ACTIFS non lues) ; la part réelle du coût attribuable à E′ et à `masque` (non mesurée). Aucune question de valeur n'est
tranchée ici ; la seule qui affleure est A-3 (calcul), sous la forme « seulement si » de la proposition (prop. l.623-625).
