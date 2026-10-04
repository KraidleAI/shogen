# ADR-0029 — Campagne S2-bis à observateurs multiples sur VPS : écart à quorum, exclusion de dégradation écrite d'avance, loi nulle par rotations, pré-enregistrement prospectif

- **Statut** : **proposée** (lot ADR-S2-BIS). Rédigée le 2026-10-04, de 02:46 à 03:33 UTC (`date -u`), par un rédacteur frais (fiche `shogen-worker`, modèle résolu `claude-opus-5-5`, effort max), sur le brief de l'orchestrateur (`BRIEF-ADR-S2BIS.md`, sha256 `b2a15c16…bb6f`). Aucune dépense, aucun compte créé, aucun code. **Ne s'applique qu'après** : (1) la clôture de S2 (lot R-S2, `docs/adr-0028/G0-lots-apres-S2.md` l.11 et l.14) ; (2) les réponses des advisors aux questions techniques du §8.2 ; (3) un cp-1 du validateur ; (4) l'acte budgétaire de l'investisseur sur le §3 (« budget soumis à l'investisseur avant toute dépense », JOURNAL l.322).
- **Rattachement** :
  - décisions de l'investisseur du 2026-10-04 (JOURNAL l.322, l.324, verbatim) ; avis produit `docs/adr-0028/AVIS-PRODUIT-APRES-S2.md` §2 (l.36-45) ; G0 du lot, `docs/adr-0028/G0-lots-apres-S2.md` l.14, et décision technique G4 du même fichier (l.20-26) ; avis G4 `docs/adr-0028/AVIS-G4-NOTAIRE.md` §3 (l.44-52) ;
  - ADR-0028 : D1 (l.20-28), D2 (l.29-42), D5 (l.57-62), §1 bis.1 (règle SHOGEN-CRITERE-R1-1, l.89-114), D6 (i) et (vi) (l.186-189, l.200), D9 (l.222-233), annexe D (pré-enregistrement) ; ADR-0024 (n fixe, l.15-18) ; ADR-0022 (règle de τ, l.19) ; ADR-0023 (Pyth, invariant « strictement sans clé », l.10, l.25) ; ADR-0026 (k_eff, l.15) ;
  - `docs/10-mesures-pilotes-design.md` §3-§5 ; `docs/04-certificat-diversite.md` §2 ; registres `docs/08-assumptions.md` et `docs/09-vocabulaire.md` ; `docs/17-modele-de-menace.md` ; `docs/DEVOPS.md` §4 ; `docs/R-8-outillage.md` ; `s2-harness/` (collecte et chemin de recalcul).
- **Conventions** : « rendu » = `docs/adr-0028/execution/rendu-2026-10-04/shogen-27b0e30-rendu-20261004T011129Z-943.3-j28.out` (rendu J28 de l'exécution unique, sha256 `26877549…65c0`, JOURNAL l.314) ; « l.n » renvoie à la ligne n du fichier nommé juste avant ; [lu] lu sur la source ; [calc] calcul du rédacteur sur un [lu] ou sur données synthétiques ; [inféré] raisonnement du rédacteur ; [abs] absent de la source lue. Les prix sont lus le 2026-10-04 sur les pages nommées au §3. Journal de provenance : `G1-ADR-0029.md` (même dossier).
- **Exposition du rédacteur** (forme de l'annexe D.3 d'ADR-0028) : j'ai lu les blocs 1, 3, 5, 6 et la section [SENSIBILITÉ] du rendu (valeurs de z, K, P̂_more, FIV de **S2**, post-rendu, lecture autorisée par le brief), jamais le bloc 2 ni le bloc 4 ; aucun `*.jsonl` ; aucune pièce de `docs/15-*`, `docs/16-*`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/` ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée. Aucune donnée de S2-bis n'existe. Constat : ADR-0026, source nommée par le brief, porte de la matière Pocket (l.3, l.8-10, l.19-21, l.36-42) ; lue avant de le constater ; rien n'en est repris ici hors la définition de k_eff.

## 1. Contexte

### 1.1 Ce que S2 a mesuré (rendu J28, exécution unique du 2026-10-04)

| objet | calme | stress | source |
|---|---|---|---|
| fenêtres retenues n | 24 585 | 11 397 | rendu l.435451, l.435471 |
| K (fenêtres à ≥ 2 écarts) | 154 | 133 | idem |
| P̂_more | 0,0013630 | 0,0014664 | rendu l.435467, l.435487 |
| z_s (seuil 2,33) | 20,83 | 28,47 | rendu l.435469, l.435489 |
| z_bloc (ℓ = 240) | 1,945 | 1,744 | rendu l.435496, l.435500 |
| FIV = R_centrage × FIV_série | 114,7 = 4,57 × 25,1 | 266,3 = 7,88 × 33,8 | rendu l.435495, l.435499 |
| runs de I_t : nombre ; longueur moyenne ; maximum | 119 ; 1,29 ; 6 | 130 ; 1,02 ; 2 | rendu l.435497, l.435501 |
| valeur de la règle SHOGEN-CRITERE-R1-1 | NE REJETTE PAS (discordance) | NE REJETTE PAS (discordance) | rendu l.435516, l.435519 |
| K décomposé : ≥ 2 `panne_transport` ; 1 ; 0 ; « tous hors-enveloppe » | 153 ; 1 ; 0 ; 0 | 133 ; 0 ; 0 ; 0 | rendu l.435532-435533 |
| c_s (fenêtres où tout le pool est en `panne_transport`) | 9 | 0 | idem |
| fenêtres sautées s (sans marqueur, hors plage D5) | 5 701, dont 5 684 non attribuées | 2 094, dont 1 944 non attribuées | rendu l.37-41 |
| Pyth (lectures `ok`) | 0 / 24 585 | 0 / 11 397 | rendu l.42-43 |

« R1 discrimine » = FAUX (rendu l.435522). La phrase scellée imprimée pour chaque strate est : « le modèle binomial de doc 10 §5.1, à fenêtres indépendantes, est rejeté ; la cause n'est pas identifiée entre co-défaillance des sources et dépendance sérielle des fenêtres » (rendu l.435517, l.435520). Côté R2 : 7 hôtes sur 10 derrière AS13335 (rendu l.435691), k_eff = 4 pour k nominal = 10 (rendu l.435779-435780).

### 1.2 Pourquoi la règle n'a pas tranché

1. **K est fait de pannes de transport, vues d'un seul point.** 153 des 154 fenêtres K du calme et les 133 du stress portent au moins deux `panne_transport`, aucune n'est faite d'écarts de prix (rendu l.435532-435533) ; le rendu l'écrit : « le z confirmatoire inclut les modes communs de l'observateur (hôte, DNS, réseau) » (rendu l.435531). Le collecteur range sous `panne_transport` tout défaut sans réponse HTTP, DNS, connexion, délai ou coupure, sans sous-type (`s2-harness/shogen_s2/sources.py` l.44-58 et l.389-390). Une coupure du réseau de l'hôte, ou de son résolveur, met donc toutes les sources en panne dans la même fenêtre : c'est une co-défaillance de l'observateur, comptée comme co-défaillance des sources [inféré].
2. **Un seul observateur, un seul résolveur.** Hôte unique, le poste de l'investisseur (« pas sur mon PC », JOURNAL l.324), sous Windows (`s2-harness/RUNBOOK-campagne.md` l.40-68 : tâche `schtasks`, fichier `.bat`) ; résolveur unique `cloudflare-dns.com`, résidus 3 et 5 de l'axe ASN « à son MAXIMUM, publié » (rendu l.435772, l.435774). Coupures de courant et redémarrages (ADR-0024 l.8-9) ; item SHOGEN-UPS-1, « un hôte distant pour S3 » (ADR-0024 l.23) ; plage D5 retirée pour harnais dégradé, `resolve_failed` à 15,3 % contre 1,85 % hors plage (ADR-0028 l.60).
3. **Horloge non disciplinée par NTP.** Le contrôle d'horloge de S2 est une plausibilité croisée `harness_ts − source_ts`, « pas NTP » (`s2-harness/shogen_s2/collector.py` l.28-30, l.63-93). Sur les 3 610 contrôles du bloc 1 (rendu l.48-3657), la médiane par contrôle va de −52,2 s à +96,3 s ; 506 dépassent 10 s en valeur absolue, 110 dépassent 30 s [calc]. Cette mesure mêle la fraîcheur des sources et l'horloge de l'hôte : elle ne s'attribue pas [inféré] ; les valeurs négatives, qui placent l'horloge de l'hôte en retard sur les horodatages portés, désignent l'hôte [inféré].
4. **FIV élevés et plancher qui s'auto-masque.** FIV = 115 et 266, dont un facteur sériel de 25 et 34 (rendu l.435495, l.435499) : les 154 fenêtres K du calme se comportent comme environ 6 grappes, celles du stress comme 4 (K / FIV_série [calc]). Le plancher z_bloc estime la variance sur les données mêmes : sous un excès groupé en grappes, les grappes du signal gonflent σ̂_bloc. Une première simulation synthétique du rédacteur (8 semaines de calme ; `calc/sim_rotation.py`, journal G1, entrée 39) donne à la règle R1-1 un taux de rejet de 0 à 0,06 contre des incidents communs groupés, là où un test qui conditionne sur la structure temporelle propre de chaque source rejette de 0,02 à 1,00 selon le scénario, et de 0,44 à 1,00 quand les épisodes de panne propres sont courts [calc] ; la seconde simulation, par durée, est au §2.4 d.
5. **Deux flux d'un même hôte dans le pool d'indépendance.** `okx_ticker` et `okx_index` sont lus sur `www.okx.com` (rendu l.435688) ; le pool d'analyse de R1 compte 11 flux pour 10 sources (rendu l.44-45). Une panne de l'hôte OKX produit à elle seule une fenêtre à deux écarts, alors que P̂_more les traite comme indépendants. La contribution à K n'est pas mesurée [inféré] ; aucune pièce lue ne traite ce point pour R1 (le cas est traité pour k nominal et le drapeau 2, annexe B l.599).
6. **Pyth mort, τ jamais atteint.** Pyth : 0 lecture `ok`, HTTP 401, « Hermes now requires an API Key » (ADR-0023 l.15-16), retiré après coup par D1 (a) (rendu l.42-43). τ observé (P99) : 0,30 % contre τ = 2,6 % (agrégateurs), 0,45 % contre 1,65 % (Chainlink), 0,085 % contre 0,45 % (places horodatées), 0,17 % contre 0,45 % (places sans horodatage) (rendu l.435526-435530) : aucune fenêtre K n'est faite d'écarts hors-enveloppe ; R1 n'a mesuré que la disponibilité.

### 1.3 Ce que l'investisseur a décidé (verbatim)

- « Oui, préparer S2-bis (Recommandé) », option décrite « ADR d'abord, budget soumis à l'investisseur avant toute dépense » ; collecte S2 : « L'arrêter (Recommandé) » ; priorité : « Position d'abord (Recommandé) » (JOURNAL l.322).
- « cette fois on le fait sur un VPS, pas sur mon PC » (JOURNAL l.324).
- Décision technique G4 de l'orchestrateur : « S2-bis : mesure R1/R2 sans témoignage notarié (brin exploratoire facultatif sur un VPS distinct, hors décision) » (`docs/adr-0028/G0-lots-apres-S2.md` l.25).

### 1.4 Ce que cette ADR ne fait pas

Elle n'achète rien, n'ouvre aucun compte, n'écrit aucun code, ne lit aucun journal. Elle ne modifie ni la règle scellée de S2 ni son verdict. Elle propose une campagne neuve, dont les données n'existent pas, et la règle qui la jugera, écrite avant elle.

## 2. Décision proposée

### 2.1 Observateurs

- **Nombre : M = 4 observateurs**, chacun un VPS loué, aucun sur le poste de l'investisseur (JOURNAL l.324). Argument [inféré] : (i) avec le quorum majoritaire du §2.2, quatre observateurs gardent la fenêtre évaluable jusqu'à deux observateurs perdus ou bloqués (trois observateurs, jusqu'à un seul), et exigent 3 accords sur 4 quand tous sont valides ; si ε est la probabilité qu'un chemin d'observateur échoue seul sur une source dans une fenêtre, une fausse panne de source demande trois échecs simultanés (≈ 4ε³), contre deux (≈ 3ε²) pour M = 3 ; (ii) quatre familles de résolveurs distinctes existent sans Cloudflare (ci-dessous) ; (iii) le coût marginal d'un observateur est de quelques euros par mois (§3) ; (iv) au-delà, chaque observateur ajoute un compte chez un fournisseur de plus, acte de l'investisseur. Repli écrit d'avance : si l'un des quatre fournisseurs ne peut pas être ouvert avant le sceau, le paquet scelle M = 3 (quorum 2 de 3) ; la décision se prend avant le sceau, jamais pendant la campagne.
- **Fournisseurs distincts, ASN distincts** (aucun achat ici ; détenteurs lus sur RIPEstat le 2026-10-04 [lu]) : proposition O1 Hetzner (AS24940, Hetzner Online GmbH), O2 OVHcloud (AS16276, OVH SAS), O3 DigitalOcean (AS14061, DigitalOcean LLC), O4 Akamai Linode (AS63949, Akamai Connected Cloud). Remplaçants : Scaleway (AS12876), UpCloud (AS202053), Vultr (AS20473), Contabo (AS51167). L'ASN d'un observateur est **mesuré sur son adresse réelle** au déploiement (RIPEstat et Team Cymru, chaîne de l'axe R2, `docs/10-mesures-pilotes-design.md` l.206-214), jamais déduit du nom du fournisseur.
- **Aucun observateur sur l'ASN d'une source du pool — possible, donc exigé.** Les hôtes du pool sont sur AS13335, AS16509, AS14618 et AS19551 (rendu l.435676-435689 ; détenteurs Cloudflare, Amazon ×2, Incapsula, lus sur RIPEstat [lu]). Aucun fournisseur proposé n'en relève ; AWS (dont Lightsail) est exclu à ce titre [inféré : Lightsail est un service d'Amazon]. L'enquête ASN faite depuis chaque observateur au rodage (§6) le contrôle ; un hôte de source qui rejoint l'ASN d'un observateur pendant la campagne est déclaré au rapport, jamais corrigé.
- **Régions** : quatre pays distincts ; au plus deux observateurs dans une même région métropolitaine ; un observateur hors de l'Union européenne si son essai de lecture passe ; aucun aux États-Unis, par précaution : doc 10 note un géo-blocage 451 de Binance selon juridiction, supposition (c) qui « ne fonde rien » (`docs/10-mesures-pilotes-design.md` l.185-189). Le critère factuel est l'essai : chaque observateur lit avec succès, depuis son adresse, les flux sans clé du pool (11, Pyth exclu) avant le sceau (smoke, `s2-harness/shogen_s2/smoke.py`), sinon il est remplacé avant le sceau.
- **Résolveurs DNS de familles distinctes**, un par observateur : O1 récursif local (unbound, résolution depuis la racine, sans tiers) ; O2 Quad9 (9.9.9.9 et 149.112.112.112, AS19281 [lu]) ; O3 Google Public DNS (8.8.8.8 et 8.8.4.4, AS15169 [lu]) ; O4 résolveur de son fournisseur. **Aucun observateur n'utilise 1.1.1.1** (AS13335 [lu], l'ASN de 7 hôtes du pool : résidu 5, rendu l.435774). Le résolveur exact reste journalisé par enregistrement, comme en S2 (rendu l.435772). Effet attendu : une panne de résolveur ne touche qu'un observateur, donc reste sous le quorum [inféré].
- **Horloge** : chrony sur chaque observateur, au moins quatre serveurs NTP d'au moins deux opérateurs. La borne d'erreur est celle de la documentation de chrony : « clock_error <= |system_time_offset| + root_dispersion + (0.5 * root_delay) » [lu, `https://chrony-project.org/doc/4.6/chronyc.html`]. Seuil : un observateur est dégradé pour une fenêtre si cette borne dépasse **1 s**, ou si le statut est « Not synchronised » (même page [lu]) — critère D-3 du §2.3. Motif du seuil : les lectures partent à ws + w − δ avec δ = 15 s (§2.9) ; 1 s laisse chaque lecture dans sa fenêtre et ne pèse pas sur la staleness : le plus petit σ committé d'une classe du pool d'analyse est 180 s (places horodatées ; σ_pyth = 33 s porte sur une classe sans donnée), rendu l.12 [inféré].
- **Critères de choix des fournisseurs** (aucun achat) : entité juridique distincte ; ASN propre distinct des autres observateurs et des hôtes du pool ; tarif public lu ; facturation horaire ou mensuelle sans engagement long ; IPv4 incluse ou achetable ; au moins 1 Go de mémoire et 20 Go de disque ; centre de données hors des États-Unis ; console permettant de coller un script de premier démarrage (cloud-init) sans accès SSH d'un agent (§2.9).

### 2.2 Définition d'écart à quorum

Notations : unité u (hôte, §2.5) ; fenêtre j (w = 60 s, grille UTC, `s2-harness/shogen_s2/window.py` l.69-77) ; observateur o.

1. **Observateur valide** dans j : o a écrit le marqueur de clôture de j (comme en S2, `collector.py` l.15-19) et n'est pas dégradé dans j au sens du §2.3. V_j = ensemble des observateurs valides ; M_j = |V_j|.
2. **Classement par observateur** : chaque observateur classe chaque unité avec ses propres lectures, selon la définition d'écart de S2 inchangée — panne > staleness > hors-enveloppe, τ et σ par classe, N ≥ 4 répondantes (`docs/10-mesures-pilotes-design.md` l.420-443 ; rendu l.435448) ; la médiane leave-one-out est calculée **sur les lectures de cet observateur**. On note e(o, u, j) ∈ {panne, staleness, hors-enveloppe, aucun, non évaluable} ; « non évaluable » n'est pas un écart (rendu l.435448).
3. **Écart de source (consolidé)** : u est en écart dans j si et seulement si un même axe a ∈ {panne, staleness, hors-enveloppe} est constaté par au moins q_j observateurs valides, avec **q_j = ⌊M_j/2⌋ + 1** (3 sur 4, 2 sur 3, 2 sur 2) ; si plusieurs axes atteignent le quorum, le type suit la précédence. Les sous-types de panne (transport, HTTP, décodage) comptent pour l'axe panne.
4. **Panne d'observateur, désaccord** : un écart vu par au moins un observateur valide sans quorum sur son axe est un **écart d'observateur** : censuré pour R1 (ni dans p̂_u, ni dans K) et compté à part par (o, u, axe). Un écart sans quorum sur aucun axe alors que q_j observateurs voient un écart d'axes différents est un **désaccord**, compté à part.
5. **Fenêtre évaluable** : M_j ≥ 2. Sinon **quorum perdu** : la fenêtre est censurée (hors n), comptée par strate et par cause (absence, dégradation D-2 à D-5).
6. **Effet sur staleness et hors-enveloppe : par observateur, puis consolidé — tranché.** Motifs [inféré] : (i) les lectures d'un observateur sont prises dans un même intervalle de quelques secondes ; mêler les prix de quatre observateurs mêlerait des instants séparés de quelques secondes et créerait des écarts de prix artificiels sur un marché qui bouge ; (ii) une réponse servie en cache à un seul observateur (point de présence du CDN, variante régionale d'une API) ne fait pas un écart de source ; (iii) avec M_j = 2, une médiane entre observateurs serait une moyenne, un prix que personne n'a lu ; (iv) chaque journal d'observateur garde la forme d'un journal S2 : `r1.classify_ecart` se réutilise par observateur, et la consolidation est un vote simple, recalculable par un tiers. L'option « prix consolidé » est écartée au §4.
7. **Sens nouveau de « panne de source »** (écart déclaré à `docs/10-mesures-pilotes-design.md` l.435-436, « non-réponse avant clôture de fenêtre, erreur de transport ») : une panne vue d'un seul point est une panne du chemin ou de l'observateur ; une panne vue de q_j points distincts est une panne de la source ou de sa livraison globale. Le mode commun du CDN partagé reste compté quand il est global (résidu 1, rendu l.435770) ; une panne d'un point de présence régional sort de K. Les modes communs simultanés d'au moins q_j observateurs restent dans K : c'est la limite résiduelle, mesurée par la matrice de co-défaillance des observateurs (descriptif, §2.7 pt 9). Ce changement entre à doc 04 par le lot DOC04-REV.

### 2.3 Exclusion de dégradation écrite avant la campagne

Critères calculés **sur les seuls enregistrements de diagnostic** de l'observateur, **jamais sur un statut de source** (principe de SHOGEN-HOST-DEGRADED-2, `docs/adr-0028/ANNEXE-B-items.md` l.100). Un observateur est dégradé dans la fenêtre j si l'un des cas suivants est vrai :

| code | critère | seuil (écrit d'avance [inféré]) |
|---|---|---|
| D-1 | absence : pas de marqueur de clôture de j | — (observateur absent, non valide) |
| D-2 | retard ou débordement : première lecture partie plus de 5 s après ws + w − δ, ou une lecture finie après ws + w − 1 s | 5 s ; 1 s |
| D-3 | horloge : borne d'erreur chrony > 1 s, statut « Not synchronised », ou aucun relevé chrony de moins de 120 s | 1 s ; 120 s |
| D-4 | réseau : au moins 2 des 3 témoins sans réponse à une requête DNS SOA de « . » en 2 s ; témoins = trois serveurs racines de trois opérateurs distincts de la liste de `https://root-servers.org/` [lu : liste des opérateurs], lettres fixées au paquet | 2 sur 3 ; 2 s |
| D-5 | résolveur : échec de résolution, par le résolveur de l'observateur, de deux noms témoins fixés au paquet, servis hors des ASN du pool | 2 sur 2 ; 2 s |

- **Quorum perdu** : fenêtre censurée (§2.2 pt 5). Les critères ne lisent aucun statut de source ; la censure peut pourtant corréler avec un événement qui touche aussi les sources (incident réseau large) [inféré] : l'hypothèse A(loss-non-informative) (`docs/08-assumptions.md` l.31) reste engagée, et les comptes de censure par cause sont imprimés.
- **Strate** : la campagne vise n_s fenêtres évaluables (§2.4). Si n_s n'est pas atteint à T_max,s, la strate est évaluée sur les n′_s fenêtres recueillies si n′_s ≥ n_s/2, avec la puissance réduite imprimée ; sinon elle est NON ÉVALUABLE.
- **Observateur bloqué par une source** : un blocage durable (par exemple un refus HTTP systématique d'une source envers l'adresse d'un observateur) relève du quorum, pas de l'exclusion ; au rodage, un tel blocage fait remplacer l'observateur avant le sceau (§2.8).
- Les seuils sont des choix de conception, confirmés par les advisors (Q3) et mesurés au rodage (taux de dégradation par critère) ; ils sont scellés au paquet et **ne changent plus après le sceau** : la leçon de D5, amendée après coup (ADR-0028 l.57-62), n'a plus lieu d'être.

### 2.4 Statistique et puissance

**Unité statistique** : la fenêtre de 60 s, par strate ; indicatrice consolidée D(u, j) ∈ {0, 1} par unité ; m_j = Σ_u D(u, j) ; **K_s = #{j évaluable de s : m_j ≥ 2}** (transposition K&L inchangée, `docs/04-certificat-diversite.md` l.47-54).

**(a) La statistique par fenêtres avec ℓ, sous les FIV de S2 pris comme a priori.** Sous l'alternative E[K] = n·P·(1 + λ), la puissance 0,8 de la règle R1-1, où z_bloc est la condition liante, demande n ≥ (2,33 + 0,8416)²·FIV_série·(1 + λ)·(1 − (1 + λ)P)/(λ²·P) [calc, `calc/puissance.py`]. Avec P = P̂_more de S2 et FIV_série de S2 (25,1 et 33,8, rendu l.435495, l.435499), en jours calendaires (5/7 de calme, 2/7 de stress, 95 % de fenêtres évaluables) :

| λ (excès relatif) | calme : n ; jours | stress : n ; jours |
|---|---|---|
| 1 | 369 116 ; 378 | 462 490 ; 1 183 |
| 2 | 138 230 ; 142 | 173 179 ; 443 |
| 3 | 81 802 ; 84 | 102 474 ; 262 |
| 4 | 57 438 ; 59 | 71 946 ; 184 |

Si le quorum divise P par 10, la seule garde n·P̂(1 − P̂) ≥ 10 demande 73 381 fenêtres en calme (75 jours) et 68 205 en stress (175 jours) [calc]. En 12 semaines, la règle R1-1 ne détecte, à puissance 0,8, qu'un λ ≥ 3,0 en calme et ≥ 7,9 en stress [calc]. **Conclusion : sous les FIV de S2, la statistique par fenêtres avec ℓ ne peut pas rendre S2-bis décisive dans un délai raisonnable** ; la raison structurelle est l'auto-masquage (§1.2 pt 4).

**(b) La statistique par événements** (runs de I_t pris comme unités, SHOGEN-DEP-FENETRES-2 (c), annexe B l.98) demande une tolérance d'écart entre fenêtres pour former un événement — un paramètre d'échelle comme ℓ : en S2, 154 fenêtres K formaient 119 runs (rendu l.435497) mais environ 6 grappes. Et la loi nulle d'un compte d'événements demande encore un modèle des recouvrements fortuits. Elle est imprimée hors décision (§2.7 pt 9).

**(c) Décision : statistique par fenêtres, loi nulle par rotations circulaires indépendantes des séries de chaque unité, dans chaque strate.** Sous l'hypothèse d'indépendance des unités et de stationnarité de chacune dans la strate (A(window-stationarity), `docs/08-assumptions.md` l.29), décaler la série D(u, ·) de chaque unité d'un décalage circulaire propre laisse la loi jointe inchangée [inféré : invariance par rotation, exacte sur une série circulaire] ; la loi nulle de K s'obtient en recalculant K sur R rotations. Ce test **conserve la dépendance sérielle propre à chaque source** (durées des pannes, grappes) et **n'estime pas sa loi nulle sur l'alignement des pannes** : des incidents communs n'y entrent que par les marges de chaque unité, pas par leur simultanéité, d'où l'absence de l'auto-masquage de z_bloc [inféré ; mesuré en simulation, (d)] ; il n'a besoin ni de ℓ ni de l'approximation normale de la garde §5.4. Sources de la méthode (tests par translation torique, rotations aléatoires) : non détenues, procurement formé (SHOGEN-S2BIS-ROTATION-SOURCE-1, §8.1), requis avant le sceau ; jusque-là la construction est [inféré].

**(d) Puissance par simulation synthétique du rédacteur** (`calc/sim_duree.py`, graine 20261005 ; modèle : 10 unités, épisodes de panne propres markoviens de taux p_i = p̂_i calme de S2 × f et de longueur moyenne L ; incidents communs à ρ par jour de strate, durée moyenne 20 fenêtres, chacun touchant chacun des 7 hôtes AS13335 avec probabilité 0,7 ; R = 399 ; 200 réplications sous H0, 100 sous H1 ; aucune couche d'observateur simulée) [calc, synthétique] :

| strate, durée | scénario A (f = 0,3 ; L = 1) | B (f = 0,3 ; L = 20) | C (f = 1 ; L = 20, bruit de S2) |
|---|---|---|---|
| calme, 8 sem. | 0,93 / 1,00 (règle 0,00 / 0,18) | 0,67 / 0,88 (0,02 / 0,10) | 0,14 / 0,42 (0,00 / 0,00) |
| calme, 12 sem. | 0,97 / 1,00 (0,04 / 0,60) | 0,77 / 0,99 (0,01 / 0,54) | 0,14 / 0,61 (0,02 / 0,05) |
| calme, 16 sem. | 1,00 / 1,00 (0,20 / 0,83) | 0,91 / 0,99 (0,10 / 0,76) | 0,22 / 0,76 (0,00 / 0,20) |
| stress, 8 sem. | 0,69 / 0,92 (0,00 / 0,00) | 0,24 / 0,58 (0,00 / 0,00) | 0,05 / 0,14 (0,00 / 0,00) |
| stress, 12 sem. | 0,81 / 0,97 (0,01 / 0,02) | 0,36 / 0,78 (0,00 / 0,01) | 0,07 / 0,17 (0,00 / 0,01) |
| stress, 16 sem. | 0,92 / 0,99 (0,00 / 0,05) | 0,54 / 0,87 (0,00 / 0,05) | 0,10 / 0,35 (0,00 / 0,01) |

Cellule : puissance du test par rotations à ρ = 0,1 / 0,2 incident par jour ; entre parenthèses, la règle R1-1. Sous H0, le test par rotations rejette de 0,000 à 0,020 (erreur-type ≈ 0,007 à 0,01), la règle R1-1 0,000 ; la garde §5.4 n'est pas tenue dans 62 à 100 % des réplications des scénarios A et B à 8 et 12 semaines [calc]. Lecture : le scénario C est celui où le quorum ne réduirait pas le bruit propre des unités ; A et B, celui où il le divise par 3 [inféré]. Limites : modèle homogène en L, incidents sur le seul sous-ensemble AS13335, résolution R = 399, aucune couche d'observateur ; **ces chiffres orientent, ils ne fondent pas** : les lots SIM-NIVEAU-BIS et SIM-PUISSANCE-BIS les remplacent avant le sceau (§6).

**(e) n par strate et durée** (proposition, valeur finale fixée par SIM-PUISSANCE-BIS avant le sceau, sur des scénarios calibrés sur S2 par le lot PLAN-S2BIS) : **n_calme = 82 080 et n_stress = 32 832 fenêtres évaluables** (12 semaines calendaires à 95 % de fenêtres évaluables) ; **T_max = 18 semaines** depuis T_début. Les n_s fenêtres retenues sont les n_s premières fenêtres évaluables de la strate dans l'ordre chronologique depuis T_début ; la campagne s'arrête quand les deux strates ont atteint leur n_s, ou à T_max.

**(f) Règle d'arrêt à n fixe** (principe d'ADR-0024 l.15-18 et de RUNBOOK l.140-141 : « Fin à DATE FIXE, jamais "quand z croise 2,33" ») : aucun regard intermédiaire sur K, z ou un statut de source ; la surveillance ne lit que la santé et le compte de fenêtres évaluables (§2.8).

### 2.5 Pool

- **Unités R1 = hôtes, 10** : binance, coinbase, kraken, okx (flux `okx_ticker`), bitstamp, gemini, bitfinex, coingecko, defillama, chainlink (lu par `ethereum-rpc.publicnode.com`, `sources.py` l.223). `okx_index` reste au journal et à l'axe contenu de R2, hors de R1 : deux flux d'un même hôte sont dépendants par construction (§1.2 pt 5) ; k nominal compte déjà des hôtes (rendu l.435779). coingecko et defillama restent deux unités : leur amont déclaré (`basis:doc`, rendu l.435763) est le type de dépendance que R1 doit pouvoir montrer.
- **Pyth : retiré ex ante.** Motifs [lu] : Hermes exige une clé (ADR-0023 l.15) ; la page de plans de Pyth (`https://www.pyth.network/pricing`, redirigée vers `https://app.pyth.com/plans`) donne « Free $0 /month … No Pyth API access » et « Starter $500 /month … Pyth API access with API Key … No redistribution rights » ; l'invariant « strictement sans clé » d'ADR-0023 (l.10, l.25) et la publication des octets bruts (ADR-0003, ADR-0005 ; `s2-harness/shogen_s2/journal.py` l.8-14) s'y opposent [inféré : « No redistribution rights » contredit la publication d'un journal recalculable]. Une réintégration par lecture sur chaîne sans clé (voie B′ d'ADR-0023 l.47) n'est admise que si un lot dédié l'établit sur pièce **avant le sceau** (flux BTC/USD lisible sans clé, cadence documentée, décodeur testé, hôte de lecture distinct de celui de Chainlink) ; sinon Pyth reste dehors. Aucune décision sur Pyth après le sceau.
- **Règle D1 reprise** (ADR-0028 l.21-24) sur les lectures consolidées (« ok » = au moins q_j observateurs valides à statut `ok` avec un prix) : (a) unité sans `ok` dans toutes les strates : retirée ; (b) sans `ok` dans une strate : retirée de cette strate ; (c) retraits nommés avec leurs comptes. **Plus le seuil de flux presque mort, adopté ici ex ante** (il était une sensibilité après coup en S2, annexe B l.549) : une unité est retirée de la strate s si 2·ok(u, s) < n_s.
- **Rappel des exclusions** : CryptoCompare reste écartée et re-confirmée à chaque campagne (`s2-harness/README.md` l.20-21 ; `sources.py`, constante `EXCLUDED_CRYPTOCOMPARE`).

### 2.6 τ et σ

- **Re-dérivation sur S2, scellée pour S2-bis** (SHOGEN-TAU-REDERIV-1, PX-Shogen-13 ; annexe D.5 d'ADR-0028), par le lot TAU-SIGMA-S2BIS, avant le sceau, sur le segment J28 de S2, pool D1, exclusion D5, axe (i) atteint :
  - **σ_classe** : règle de clôture d'ADR-0021, `σ = max(plancher, 3 × P99 staleness)` (`s2-harness/shogen_s2/run_campaign.py` l.27-28), appliquée aux 28 jours de S2 au lieu des 48 h de calibration ;
  - **τ_classe** : forme de la règle d'ADR-0022 (l.19), avec un quantile robuste au lieu du maximum : **τ_c = grid-ceil(1,5 × P99,9_c, 0,05 %)**, borné par 0,05 % ≤ τ_c < 2,85 % (CAPO, ADR-0022 l.19, l.36). Motif [inféré] : les 28 jours de S2 peuvent contenir de vrais écarts, que le maximum transformerait en seuil (note de PX-Shogen-13 : τ observé et P99 de calibration ne portent pas sur la même population, annexe B l.662-664) ; pour les places sans horodatage, où la staleness n'est pas évaluable, la règle au maximum porterait τ de 0,45 % à environ 1,3 % et rendrait l'axe aveugle aux prix figés [calc : 1,5 × 0,843 %, rendu l.435530]. La valeur de la règle d'ADR-0022 (au maximum) est imprimée à côté, pour comparaison. Le choix P99,9 contre maximum est la question Q4 aux advisors.
- **Pourquoi c'est licite** : les données de S2-bis seront disjointes de celles de S2 ; S2 joue pour S2-bis le rôle que la calibration de 48 h jouait pour S2 (fenêtres de calibration « exclues à jamais de l'inférence », RUNBOOK l.104-109) ; la règle est fixée ici, avant tout calcul de P99,9 ; le rédacteur n'a vu que le P99 et le maximum imprimés (rendu l.435526-435530), déclarés ; les valeurs sont scellées au paquet et ne sont jamais re-réglées pendant S2-bis (« divergence = trouvaille, pas re-tune silencieux », ADR-0022 l.50). τ observé et σ observé de S2-bis sont imprimés, descriptifs.

### 2.7 Règle de décision SHOGEN-CRITERE-R1-2 (texte proposé, à recopier au paquet de S2-bis)

**Ce qui reste de R1-1** (ADR-0028 l.93-110) : transposition K&L (sources, fenêtres, écarts) ; K = fenêtres à ≥ 2 écarts ; trois axes et leur précédence ; w = 60 s ; strates calme/stress par calendrier (week-end UTC) ; niveau 0,01 par strate, famille de Bonferroni m ≤ 2, borne 0,02 ; trois valeurs ; noms « R1 rejette (s) » et « R1 discrimine » ; énoncés du registre doc 09 ; drapeau 2 aligné ; z_s imprimé intact ; liste hors décision ; conséquences pré-déclarées ; « un cas non prévu est une déviation déclarée, jamais une réécriture ».
**Ce qui change** : unité = hôte ; écart consolidé au quorum d'observateurs ; condition de dépendance par rotations au lieu de z_bloc ; décision en comptes entiers ; garde §5.4 sans effet sur la décision ; n fixe en fenêtres évaluables et T_max ; pool sans Pyth et seuil de flux presque mort ex ante ; τ et σ re-dérivés ; « excès critique » au lieu de l'EMD ; sens de la discordance ; campagne prospective.

1. **Portée.** Segment confirmatoire de S2-bis (§2.4 e), indicatrices consolidées au quorum (§2.2), unités du pool D1-bis par strate (§2.5), strates calme et stress. Entrées imprimées : n_s, fenêtres censurées par cause, K_s, P̂_more,s, z_s, C_s, R, graine, moyenne et quantile 0,99 de la loi de rotation.
2. **Statistique et loi nulle.** Pour r = 1..R, R = 9 999 : chaque unité u autre que la première (ordre alphabétique) est décalée circulairement de o(r, u) positions sur la suite chronologique des fenêtres évaluables de la strate ; K_s^(r) est recalculé. Décalages : o(r, u) = entier big-endian de SHA-256(graine ‖ « : » ‖ strate ‖ « : » ‖ r ‖ « : » ‖ u) modulo n_s ; graine = sha256 du manifeste scellé du paquet (fixée par le sceau, imprévisible avant). C_s = #{r : K_s^(r) ≥ K_s}.
3. **Hors décision, imprimés pour continuité** : z_s (doc 10 §5.1) avec sa garde §5.4, z_bloc à ℓ = 240 et FIV ; ils ne fixent aucune valeur.
4. **Comparaison** en entiers : C_s ≤ 99 ⇔ (C_s + 1)/(R + 1) ≤ 0,01. Aucun critère exprimé en p-valeur flottante (forme du pt 4 de R1-1).
5. **Valeur par strate.** REJETTE ⇔ C_s ≤ 99. NE REJETTE PAS ⇔ C_s ≥ 100 et strate testable. NON ÉVALUABLE ⇔ moins de deux unités avec au moins un écart consolidé dans la strate (loi de rotation dégénérée), ou n′_s < n_s/2 à T_max (§2.3).
6. **Nommage et famille.** « R1 rejette (s) » = valeur REJETTE. « R1 discrimine (S2-bis) » : VRAI si au moins une strate REJETTE (nommée) ; FAUX si aucune ne REJETTE et qu'au moins une NE REJETTE PAS ; NON ÉVALUABLE si aucune strate n'est testée. m = nombre de strates testées, imprimé ; borne P(au moins un rejet à tort) ≤ 2 × 0,01 = 0,02.
7. **Prémisse.** Modèle nul joint : processus d'écart consolidés des unités indépendants entre eux, chacun stationnaire dans la strate. Le test est exact sous invariance par rotation d'une série circulaire ; sur une série linéaire avec trous comprimés et week-ends concaténés, il est approché : SIM-NIVEAU-BIS en mesure le niveau avant le sceau (au moins 10⁴ réplications ; taux et longueurs d'épisodes hétérogènes ; épisodes jusqu'à plusieurs jours ; fenêtres censurées ; artefacts d'observateurs simultanés), imprimé avec son erreur-type. Conséquence pré-déclarée : cette mesure ne change ni R, ni le seuil, ni la règle ; un niveau mesuré au-dessus de 0,01 à deux erreurs-types devient une limite écrite au paquet.
8. **Énoncés** (registre doc 09, l.20-27) :
   - REJETTE : « le modèle d'indépendance des sources du pool (k nominal = … hôtes ; k_eff mesuré = …) est rejeté dans la strate s sur n_s fenêtres à quorum d'observateurs distincts, axes panne / staleness / hors-enveloppe, sous la loi de rotation qui conserve la dépendance sérielle propre à chaque source ; aucune dépendance de paire n'est établie ; les modes communs d'au moins q_j observateurs simultanés restent inclus » ;
   - NE REJETTE PAS : « le modèle d'indépendance n'est pas rejeté sur n_s fenêtres à quorum, axes … », avec l'**excès critique** = K_crit,s − K̄_rot,s, où K_crit,s est le plus petit k tel que #{r : K_s^(r) ≥ k} ≤ 99, et sa fraction de n_s ; aucun seuil sur l'excès critique ; un résultat négatif est un résultat ;
   - si z_s ≥ 2,33 (garde tenue) et C_s ≥ 100 : « le modèle binomial à fenêtres indépendantes est rejeté ; sous la loi de rotation, l'excès est compatible avec la superposition fortuite des épisodes propres des sources » ; valeur NE REJETTE PAS ; jamais un VRAI.
9. **Hors décision, imprimés et étiquetés** : z_s, z_bloc, FIV ; compte d'événements (runs de I_t à tolérance fixée au paquet) et sa loi de rotation ; variante « rotation par jours entiers » (diagnostic d'un calendrier commun des pannes) ; R1 par observateur (K, z de chaque journal pris seul, à la manière de S2) ; écarts d'observateur et désaccords par (o, u, axe) ; matrice de co-défaillance des observateurs ; strate poolée stratifiée ; L&M ; sensibilités de la liste fermée : (i) quorum fixe q = 2 ; (ii) exclusion de dégradation désactivée ; (iii) rotation par jours entiers.
10. **Drapeau 2** : levé ⇔ « R1 discrimine » VRAI et k_eff = k nominal (hôtes) de la partition R2 multi-points de vue (§2.9) ; éteint ⇔ FAUX, ou VRAI avec k_eff < k nominal ; non évaluable sinon (forme d'ADR-0028 l.109).
11. **Limites et conséquences.** Limites écrites avec la règle : stationnarité par strate supposée ; une non-stationnarité commune aux sources compte comme dépendance (mode commun de régime) ; modes communs d'au moins q_j observateurs simultanés inclus ; sens de « panne de source » restreint aux pannes vues de q_j points distincts (§2.2 pt 7) ; détection des écarts variable avec M_j ; résolution de Monte-Carlo 10⁻⁴. Conséquences : VRAI → proposition du G0 « benchmark continu » à l'investisseur et lecture du drapeau 2 (D6 (vi) et D9) ; FAUX → résultat négatif publié dans le vocabulaire du registre (doc 09 l.21, l.27), avec l'excès critique, et intégré à doc 04 par DOC04-REV ; aucune promotion de la collecte sans décision de l'investisseur ; NON ÉVALUABLE → question à l'investisseur (complément ou arrêt). « La collecte meurt » reste une décision de l'investisseur.

### 2.8 Pré-enregistrement

- **Prospectif** : à la différence de S2, scellée après la collecte, le paquet de S2-bis est **scellé avant le début du segment confirmatoire** : T_début ≥ genTime du jeton + 24 h, et go écrit de l'investisseur (ordre d'ADR-0028, annexe D.4 c l.160).
- **Contenu du paquet** (les dix lignes de l'avis produit, l.43, plus ce que cette ADR ajoute) : règle R1-2 (§2.7) ; définition d'écart à quorum (§2.2) ; liste des observateurs (fournisseur, ASN mesuré, région, famille de résolveur, adresse) ; pool et règle D1-bis (§2.5) ; strates et calendrier ; n_s, T_max, règle d'arrêt (§2.4) ; statistique et loi de rotation, R, construction de la graine ; critères de dégradation (§2.3) ; τ et σ par classe (§2.6) ; sorties de SIM-NIVEAU-BIS et SIM-PUISSANCE-BIS ; inventaire D.1-bis et attestations D.3-bis ; commits du collecteur et du chemin de recalcul ; spécification du format des journaux ; bloc machine.
- **Sceau à ancre externe** : jeton RFC 3161 de FreeTSA sur le manifeste (procédure de S2, annexe D.4 c l.156-157) **et** OpenTimestamps (complément de durabilité, l.158 ; client = dépendance nouvelle, R-8, acte de l'investisseur). Pendant la campagne, un jeton RFC 3161 par jour sur les têtes de chaîne des quatre journaux (§2.9).
- **Exécution unique** : un seul rendu, par un script scellé, refus par défaut, gardes de la forme de l'annexe D.4 b (sha du paquet au JOURNAL, code d'analyse égal au commit scellé, sha des journaux égaux aux sommes de clôture, sha du script, délai, acte de l'investisseur).
- **Annexes D reprises** : D.1-bis (inventaire des lectures sur les données de S2-bis : au rodage, santé, complétude, essais de lecture et disponibilité par couple observateur-unité, classe M ; pendant la campagne, santé et complétude seulement) ; D.2-bis (pièces interdites aux rédacteurs et validateurs frais : tout statut de source de S2-bis avant le rendu) ; D.3-bis (attestations, dont l'exposition de leurs auteurs aux résultats de S2, déclarée et sans effet sur la validité, S2-bis étant une campagne neuve) ; D.4-bis (fixtures seulement pour les G1/G2 des lots de S2-bis ; exécution unique ; sceau) ; D.5-bis (traitements descriptifs).
- **Rien de S2-bis n'est lu avant le sceau** hors du rodage, segment séparé comme l'était la calibration (RUNBOOK l.110-113), jamais consommé par le test ; le contrôle FM-1.1 des transcriptions des rédacteurs et validateurs frais est un acte de l'orchestrateur (annexe C d'ADR-0028).

### 2.9 Ingénierie

- **Frontière** (ADR-0028 D6 (i), l.186-189) : la collecte de S2 (`collector`, `sources`, `run_campaign`, `closure`, `smoke`, `journal`, `model`, `r2.collect_asn`, `records.append_asn`) reste en quarantaine. **La collecte de S2-bis est réécrite** dans un paquet neuf, **sous G0-G7 dès le premier commit** et non « jetable » : ses journaux sont la preuve de S2-bis. Les décodeurs de `sources.py` y sont repris avec leurs fixtures et relus en G2. **Le chemin de recalcul est réutilisé** (`records`, `window`, `r1.classify_ecart`, `r2`, `report`, sous G0-G7, D6 (ii)) et complété de deux modules neufs sous G0-G7 : `consolidation` (quorum, §2.2) et `rotation` (§2.7) ; les points d'entrée `recompute_*` restent l'oracle tiers.
- **Collecteur d'observateur** (bibliothèque standard Python seule, comme S2, `s2-harness/README.md` l.17-19) :
  - lectures **concurrentes bornées** (une par flux), démarrées à ws + w − δ, **δ = 15 s**, délai 10 s par requête ; heures de départ et de fin de chaque lecture journalisées (S2 lisait en série, `run_campaign.py` l.62-65) ;
  - **sous-type de panne de transport** : DNS, connexion, TLS, délai, coupure, autre (S2 n'en avait aucun, §1.2 pt 1) ;
  - **enregistrement de santé** par fenêtre : relevé chrony, témoins D-4 et D-5, horaires D-2 ;
  - **journal par observateur** à enregistrement unique par lecture (valeur décodée et octets bruts dans le même enregistrement, contre la classe de défaut de SHOGEN-RAW-LECTEUR-1, JOURNAL l.316), **chaîné** (chaque enregistrement porte le sha256 du précédent), `fsync` au marqueur de fenêtre, enregistrement de point de contrôle horaire avec la tête de chaîne ; descripteur d'observateur dans `run_params` (fournisseur, ASN mesuré, région, résolveur, empreinte de la configuration déployée) ;
  - format spécifié et scellé au paquet (même principe que SHOGEN-FORMAT-JOURNAUX-1, annexe B l.55).
- **Transport, sommes, scellement des journaux par observateur** : fichiers quotidiens clos et sommés ; copie horaire vers un espace de sauvegarde distinct des observateurs (rsync sur SSH, sous-compte par observateur) ; échange des têtes de chaîne entre observateurs (chaque journal consigne les têtes des trois autres) ; jeton RFC 3161 quotidien sur les quatre têtes ; à la clôture, fichier de sommes, sceau, dépôt sur le Drive de l'investisseur, comme pour S2 (JOURNAL l.312).
- **Déploiement rejouable** : un script de premier démarrage (cloud-init) versionné, collé par l'investisseur dans la console de chaque fournisseur, qui crée l'utilisateur, installe chrony et le résolveur, pose le pare-feu (sortant HTTPS, DNS, NTP ; SSH par clé seule), clone le dépôt à un commit épinglé et en contrôle le sha, installe les unités systemd (redémarrage automatique) et démarre le rodage ; l'empreinte de la configuration appliquée entre au descripteur d'observateur. « Rejouable » se mesure : même script sur les quatre observateurs, empreintes égales hors paramètres d'observateur.
- **Secrets** : aucune clé d'API (collecte sans clé) ; clés SSH générées sur chaque observateur ; identifiants de l'espace de sauvegarde et adresses de surveillance hors du dépôt, gardés par l'investisseur ; **aucun agent ne détient d'accès aux observateurs pendant la campagne** [inféré : limite l'exposition T-12 de doc 17 et l'exposition D.2-bis] — question Q12.
- **Supervision** : signal de vie de chaque observateur toutes les 5 minutes vers un service d'alerte (Healthchecks.io, offre gratuite [lu, §3]) qui écrit à l'investisseur après 15 minutes de silence ; procédure d'intervention en langage clair (redémarrer, reconstruire depuis le script). Répond à SHOGEN-SCHED-MONITOR-1 (« chaîne d'alerte vers un humain », annexe B l.31) et à SHOGEN-TASK-72H-1 (annexe B l.30 : aucune tâche planifiée à limite d'exécution) ; ces items se soldent à la mise en service du lot DEPLOI-BIS, pas par cette ADR.
- **Sauvegarde** : quatre copies par réplication entre observateurs et espace de sauvegarde ; instantanés de l'espace de sauvegarde ; Drive à la clôture.
- **R-8** : aucune dépendance Python neuve ; paquets système nouveaux (chrony, unbound, rsync, outil de pare-feu) contrôlés au registre de la distribution **avant installation**, au G0 du lot DEPLOI-BIS (les pages du registre Debian ont renvoyé un défi anti-robot le 2026-10-04 et n'ont pas été lues : item SHOGEN-S2BIS-R8-PAQUETS-1, §8.1).
- **Axe R2 multi-points de vue** : chaque observateur mesure l'attribution ASN depuis son point et son résolveur ; les quatre partitions sont publiées ; la partition du certificat fusionne un recouvrement mesuré depuis au moins deux points de vue (règle à fixer au paquet, Q10). Les résidus 3 et 5 de l'axe ASN baissent de « maximum » à « mesurés » [inféré].

## 3. Coût — budget à soumettre à l'investisseur

**Aucun achat ; aucun compte créé.** Prix lus le 2026-10-04 entre 02:58 et 03:04 UTC ; montants hors taxes sauf mention ; conversion des dollars au taux de référence de la BCE du 2026-10-02, 1 EUR = 1,1225 USD [lu, `https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml`].

| poste | offre | prix lu | page lue (2026-10-04, [lu]) |
|---|---|---|---|
| O1 | Hetzner Cost-Optimized (CLOUD_132) + IPv4 (CLOUD_21) | 5,49 € + 0,50 € = 5,99 €/mois au plus, en FSN1, NBG1, HEL1 | `https://www.hetzner.com/cloud/` (libellés) et `https://website-price-api.hetzner.com/api/v1/products/CLOUD_132`, `…/CLOUD_21` (valeurs que la page charge) ; la page porte aussi « Currently not available » près de « Shared Resources », portée non établie |
| O1, haut | Hetzner Regular Performance (CLOUD_122) + IPv4 | 11,49 € + 0,50 € = 11,99 €/mois ; 15,49 € + 0,50 € à Singapour (SIN1) | `…/products/CLOUD_122` |
| O2 | OVHcloud VPS-1 (2 vCores, 4 Go, 40 Go NVMe, trafic illimité hors Asie-Pacifique ; quota de 500 Go/mois en Asie-Pacifique) | « À partir de 3,81 € HT/mois soit 4,57 € TTC/mois » ; conditions du « à partir de » non lues | `https://www.ovhcloud.com/fr/vps/` |
| O2, haut | OVHcloud VPS-2 | « À partir de 7,21 € HT/mois » | idem |
| O3 | DigitalOcean Basic Regular 1 GiB (1 vCPU, 25 GiB SSD, 1 000 GiB de transfert) | 6,00 $/mois ; IPv4 incluse dans les offres groupées ; taxes selon le pays | `https://www.digitalocean.com/pricing/droplets` |
| O3, haut | DigitalOcean Basic Regular 2 GiB | 12,00 $/mois | idem |
| O4 | Linode Nanode 1 GB (1 vCPU, 25 Go, 1 000 Go de transfert) | 5,0 $/mois | `https://api.linode.com/v4/linode/types` (catalogue public ; la page HTML a répondu 403) |
| O4, haut | Linode 2GB | 12,0 $/mois | idem |
| remplaçant | Scaleway DEV1-S + IPv4 additionnelle | 0,00898 €/h (≈ 6,55 €/mois) + 0,005 €/h ; stockage facturé à part, prix non lu | `https://www.scaleway.com/en/pricing/virtual-instances/`, `…/pricing/network/` |
| sauvegarde | Hetzner Storage Box BX11 (1 TB, rsync sur SSH, sans durée minimale) | 3,20 €/mois | `https://www.hetzner.com/storage/storage-box/` et `…/products/ROBOT_1333` |
| alerte | Healthchecks.io Hobbyist (20 tâches) | 0 $/mois | `https://healthchecks.io/pricing/` |
| ancre | jeton RFC 3161 FreeTSA | « immédiat, gratuit, sans compte » (annexe D.4 c d'ADR-0028, l.157, lecture S2) | — |
| ancre | OpenTimestamps | aucun prix lu ; à lire avant l'usage (P-12, annexe D.4 c l.163) | — |
| transfert | inclus dans les offres lues (OVHcloud « Trafic illimité » ; DigitalOcean et Linode 1 000 Go/mois) ; besoin estimé ≈ 10 Go/mois par observateur [inféré : journaux S2 de 395 Mo pour 38 600 fenêtres, JOURNAL l.312, plus les échanges TLS] | 0 | — |
| écarté | clé Pyth Starter | 500 $/mois (≈ 445 €/mois), « No redistribution rights » | `https://app.pyth.com/plans` |

**Durée facturée** : déploiement et rodage (3 semaines) + campagne (≈ 12,6 semaines à 95 % de fenêtres évaluables) + clôture (1 semaine) ≈ 16,6 semaines → **4 mois** en fourchette basse ; T_max (18 semaines) + 4 semaines ≈ 22 semaines → **6 mois** en fourchette haute (mois entiers pour les offres au mois).

| fourchette | composition | par mois | total HT | avec réserve de 20 % | avec TVA 20 % (si applicable) |
|---|---|---|---|---|---|
| **basse** | O1 5,99 € ; O2 3,81 € ; O3 6 $ ; O4 5 $ ; sauvegarde 3,20 € ; alerte 0 | 13,00 € + 11,00 $ = 22,80 € | 91,20 € (4 mois) | 109,44 € | 131,33 € |
| **haute** | O1 11,99 € ; O2 7,21 € ; O3 12 $ ; O4 12 $ ; sauvegarde 3,20 € ; brin exploratoire G4 facultatif 11,99 € | 34,39 € + 24,00 $ = 55,77 € | 334,63 € (6 mois) | 401,55 € | 481,86 € |
| haute, O1 à Singapour | idem, O1 à 15,99 € | 59,77 € | 358,63 € | 430,35 € | 516,42 € |

[calc, `calc/budget.py`.] La TVA dépend du statut de l'acheteur [inféré]. Le coût des sessions d'agents n'est pas chiffré ici. **Ordre de grandeur à présenter à l'investisseur : entre environ 110 € et 520 € pour toute la campagne**, soit moins d'un mois de la clé Pyth écartée.

**Coût en lots** (hors dépense) : collecte réécrite et tests ≈ 700 à 1 000 lignes ; consolidation, rotation, rendu et tests ≈ 600 lignes ; simulations ≈ 400 lignes ; déploiement ≈ 300 lignes de script [inféré, par analogie avec les lots B-DEP-1 et CRITERE, annexe B l.98] ; plafond de 200 lignes de code par commit (R-25).

## 4. Alternatives écartées

| alternative | motif |
|---|---|
| « benchmark continu » par promotion de la collecte S2 | déclencheur non atteint : « R1 discrimine » FAUX (rendu l.435522 ; ADR-0028 l.200) ; reproduirait un instrument qui mesure son observateur (avis produit l.33) |
| un seul VPS | supprime les coupures du poste, pas le mode commun de l'observateur unique, cause principale (§1.2 pts 1-2) |
| le poste de l'investisseur | refusé par l'investisseur (JOURNAL l.324) ; coupures, redémarrages, fenêtres sautées (ADR-0024 l.8-9 ; rendu l.37-41) |
| cloud managé unique (plusieurs régions d'un même fournisseur, ou fonctions sans serveur) | plan de contrôle, réseau et ASN communs aux observateurs : leurs pannes seraient corrélées [inféré] ; AWS partage en outre l'ASN de Binance et de Gemini (rendu l.435677, l.435681) |
| M = 2 | pas de majorité ; un observateur perdu fait perdre le quorum |
| M = 3 | retenu comme repli écrit d'avance ; deux accords suffisent quand tout est valide (fausses pannes ≈ 3ε² contre ≈ 4ε³) ; deux observateurs perdus font perdre le quorum [inféré] |
| M ≥ 5 | un compte de plus chez un fournisseur de plus par observateur, pour un gain marginal sur la fausse panne (≈ 4ε³ déjà) [inféré] ; reste offert à l'investisseur |
| quorum fixe q = 2 sur 4 | fausses pannes ≈ 6ε², double de M = 3 [inféré] ; gardé en sensibilité (§2.7 pt 9) |
| prix consolidé (médiane entre observateurs) pour staleness et hors-enveloppe | mêle des instants distincts ; prix que personne n'a lu quand M_j = 2 ; cache le désaccord (§2.2 pt 6) |
| règle R1-1 inchangée (fenêtres avec ℓ) | auto-masquage ; sous les FIV de S2, 59 à 1 183 jours selon λ (1 à 4) et la strate (§2.4 a) ; puissance de 0 à 0,06 sur incidents groupés en simulation (§1.2 pt 4) |
| statistique par événements comme règle | paramètre d'échelle à fixer ; loi nulle encore à construire, par rotations (§2.4 b) ; gardée hors décision |
| asymptotique fixed-b (Kiefer & Vogelsang 2005, P-05, annexe B l.119) | variance de long terme toujours estimée sur les données, donc même risque d'auto-masquage [inféré] ; source non lue |
| arrêt à information atteinte (n·P̂(1 − P̂) ≥ cible) | pas un n fixe (ADR-0024) ; effet sur le niveau non mesuré |
| clé Pyth | 500 $/mois au moins, « No redistribution rights », invariant « strictement sans clé » (§2.5) |
| témoignages notariés sur les observateurs | charge du protocole dans le mode commun, témoignage auto-attesté (avis G4 l.46-50) ; brin exploratoire facultatif seulement |

## 5. Risques et ce qu'on en conclurait

- **S2-bis rend NE REJETTE PAS.** Résultat publiable : « le modèle d'indépendance n'est pas rejeté sur n_s fenêtres à quorum, axes … », avec l'excès critique, dans le vocabulaire du registre (doc 09 l.21, l.27). Le produit avance sur R2 (concentration de livraison, multi-points de vue) et sur une non-réjection R1 bornée par sa puissance (§2.4 d).
- **S2-bis rend encore une « discordance »** (z_s ≥ 2,33, rotations non significatives). Sous R1-2, c'est un NE REJETTE PAS dont l'énoncé dit que la dépendance sérielle propre des sources suffit à expliquer l'excès binomial : la cause est identifiée du côté sériel, ce que S2 ne pouvait pas faire [inféré]. Ce n'est plus l'état « cause non identifiée » de S2.
- **S2-bis rend REJETTE.** La question devient : quel mode commun ? Si les fenêtres K tiennent au sous-ensemble AS13335, le drapeau 2 est éteint (k_eff < k nominal) : « co-défaillance expliquée par l'axe ASN, côté livraison ». Sinon, drapeau 2 levé : axes R2 insuffisants (A(axis-coverage), `docs/08-assumptions.md` l.28).
- **NON ÉVALUABLE** (quorum perdu en masse, écarts consolidés trop rares pour que deux unités en portent un dans une même fenêtre) : question à l'investisseur, avec les comptes de censure.
- **Modes d'observateurs simultanés** (incident d'un transit européen commun) : ils restent dans K (§2.2 pt 7) ; atténués par les pays distincts et le critère D-4 ; mesurés par la matrice de co-défaillance des observateurs.
- **Dépendances fournisseurs** : capacité indisponible (mention Hetzner ci-dessus), adresse bloquée par une source (protections anti-robot des CDN), suspension de compte, hausse de prix ; le rodage les révèle et le remplacement se fait avant le sceau ; pendant la campagne, la perte d'un observateur est absorbée par le quorum majoritaire.
- **Coût** : borné par les prix lus ; risque de change sur les lignes en dollars ; réserve de 20 %.
- **Conditions d'usage des API publiques** : CoinGecko sans clé est « not suitable for scheduled polling » selon une lecture worker non re-établie (`docs/10-mesures-pilotes-design.md` l.180) ; quatre observateurs à une requête par minute chacun ; la republication des octets bruts relève de G9 (item SHOGEN-S2BIS-LICENCES-API-1).
- **Pré-enregistrement** : une lecture de statut de source pendant la campagne casserait l'aveuglement ; la surveillance est réduite à la santé et aux comptes de fenêtres (D.2-bis).

## 6. Lots, jalons et questions de valeur

**Lots** (chacun avec son G0 avant tout code ; ordre ; « ‖ » = en parallèle) :

1. R-S2 : rapport de S2, cp-2, G7, clôture (préalable ; lot existant).
2. ADR-0029 : réponses des advisors (§8.2), cp-1 du validateur, acte budgétaire de l'investisseur.
3. PLAN-S2BIS (données de S2, post-rendu, lectures inventoriées) : TAU-SIGMA-S2BIS (§2.6) ; distributions des longueurs d'épisodes par source et courbe FIV_série(ℓ) pour calibrer les simulations ; mesure descriptive de la contribution de la paire OKX à K de S2 (item SHOGEN-R1-HOTE-STRUCTUREL-1).
4. SIM-NIVEAU-BIS ‖ SIM-PUISSANCE-BIS : niveau et puissance de R1-2 (≥ 10⁴ réplications), scénarios calibrés au lot 3, couche d'observateurs simulée ; fixe n_s et T_max ; identité bit à bit de deux exécutions.
5. COLLECTE-BIS ‖ RECALC-BIS : collecteur réécrit (§2.9) ; consolidation, rotation, rendu, oracle tiers ; fixtures seulement ; G2 à 100 %.
6. DEPLOI-BIS : script de premier démarrage, R-8 des paquets système, pare-feu, supervision, sauvegarde ; procédure en langage clair ; entrées de doc 17 (§7).
7. Actes de l'investisseur : quatre comptes, quatre VPS, espace de sauvegarde, service d'alerte ; collage du script.
8. RODAGE (14 jours) : essais de lecture par observateur ; enquête ASN multi-points de vue ; taux de dégradation par critère ; taux de quorum perdu ; disponibilité par couple observateur-unité ; remplacements ; aucune statistique R1 calculée.
9. PAQUET-S2BIS : rédacteur et validateur frais ; contrôle FM-1.1 ; sceau (RFC 3161, OpenTimestamps) ; 24 h ; go de l'investisseur.
10. CAMPAGNE S2-bis : n fixe, surveillance de santé seulement, jetons quotidiens.
11. CLÔTURE et EXÉCUTION UNIQUE : sommes, dépôt sur Drive, go, rendu unique, rapport, cp-2, G7.
12. DOC04-REV ‖ dès l'acceptation : écart à quorum et loi de rotation dans doc 04 §2 ; entrées du registre 08.

**Jalons** (comptés depuis l'acceptation de l'ADR et l'acte budgétaire, en semaines) : S+0 acceptation ; S+0 à S+5 lots 3 à 6 commis et revus ; S+5 à S+6 déploiement ; S+6 à S+8 rodage (14 jours) ; S+8 paquet scellé ; S+8 + 1 jour début du segment confirmatoire ; S+21 fin attendue (S+26 au plus tard, T_max) ; S+22 à S+27 rendu unique et rapport. Cohérent avec l'horizon de 12 mois de l'avis produit (l.57).

**Questions de valeur pour l'investisseur** (langage clair) :

1. **Budget** : acceptez-vous une dépense totale d'environ 110 € à 520 € sur 4 à 6 mois, pour quatre petits serveurs loués chez quatre hébergeurs différents, un espace de sauvegarde et une alerte gratuite ?
2. **Comptes** : acceptez-vous d'ouvrir vous-même ces comptes (quatre hébergeurs et un espace de sauvegarde), puis de coller un script préparé dans chaque console ? Aucun agent n'y aurait accès pendant la mesure.
3. **Durée** : acceptez-vous une mesure d'environ 12 semaines (jusqu'à 18 en cas de pannes), précédée d'environ 6 à 8 semaines de préparation ? Une mesure plus courte risque de ne pas trancher.
4. **Pyth** : on le laisse de côté (accès payant, au moins 500 $ par mois, qui interdit de republier les données). D'accord ?
5. **Brin exploratoire** de témoignages notariés, hors décision, sur un serveur de plus (environ 12 € par mois) : oui ou non ?
6. **Alerte** : qui reçoit l'alerte et agit (vous, ou un agent que vous autorisez au cas par cas) ?
7. **Publication** : même principe que pour S2 à la fin (feu vert final après lecture du rapport) ?

## 7. Tuyaux (règle Branchement)

- **Entrée** : les quatre journaux d'observateurs, par leurs sha256 de clôture.
- **Sortie** : rapport S2-bis (règle R1-2, axe R2 multi-points de vue), consommé par MONARK et par le rapport de concentration d'infrastructure (avis produit l.49). **État : absent** ; rien de S2-bis n'est servi avant le rendu unique et le feu vert de l'investisseur.
- **Test de composition** : SHOGEN-S2BIS-TUYAU-1, rapport publié recalculé hors ligne depuis les journaux scellés, sur le modèle de SHOGEN-S2-TUYAU-MONARK-1 (ADR-0028 l.244) ; déclencheur : G0 de la publication.
- **Actes hors de ce dossier, à poser par l'orchestrateur** (aucun n'est posé ici) : registre `docs/08-assumptions.md`, entrées **A(observer-distinctness)** (les pannes d'observateurs distincts ne sont pas simultanées au-delà de ce que mesure la matrice de co-défaillance ; décharge partielle : quorum, pays et résolveurs distincts) et **A(rotation-invariance)** (prémisse du pt 7 de R1-2) ; `docs/17-modele-de-menace.md`, menaces neuves : fournisseur de VPS qui lit ou altère le disque ou l'horloge, transport et réplication des journaux, secrets sur les observateurs, accès d'un agent aux observateurs ; doc 04 §2 par DOC04-REV (« Sous indépendance, … la binomiale de K&L §5 », `docs/04-certificat-diversite.md` l.55-56, devient la loi de rotation pour S2-bis) ; index DECISIONS ; ligne JOURNAL.

## 8. Items formés et questions techniques ouvertes

### 8.1 Items (règle PAROXYSME : toute limite rencontrée est formée)

| item | constat | propriétaire | déclencheur |
|---|---|---|---|
| SHOGEN-R1-HOTE-STRUCTUREL-1 | deux flux d'un même hôte (OKX) dans le pool d'indépendance de R1 de S2 ; contribution à K non mesurée | orch. | lot PLAN-S2BIS ; mention au rapport de S2 (lot R-S2), étiquetée « ajoutée après le pré-enregistrement » |
| SHOGEN-R1-AUTOMASQUE-1 | puissance du plancher z_bloc contre un excès groupé en grappes (simulation synthétique, §2.4 d) ; à écrire comme limite de lecture de la discordance de S2 | orch. ; rédacteur du rapport | lot R-S2 |
| SHOGEN-S2BIS-ROTATION-SOURCE-1 | sources des tests par rotation ou translation torique non détenues ; procurement | orch. | avant le sceau de S2-bis |
| SHOGEN-S2BIS-SIM-1 | simulations du rédacteur (scratchpad, non versées) à remplacer par SIM-NIVEAU-BIS et SIM-PUISSANCE-BIS | orch. | lot 4 |
| SHOGEN-S2BIS-PYTH-ONCHAIN-1 | voie B′ (lecture sur chaîne sans clé) non instruite | orch. | avant le sceau, facultatif |
| SHOGEN-S2BIS-R8-PAQUETS-1 | registre des paquets système non lu (défi anti-robot) | orch. | G0 de DEPLOI-BIS, avant installation |
| SHOGEN-S2BIS-LICENCES-API-1 | conditions de republication des réponses des API publiques | orch. ; investisseur | G0 de la publication |
| SHOGEN-S2BIS-OPERATEUR-1 | modèle d'accès aux observateurs (investisseur seul, agent autorisé au cas par cas) | investisseur | acte budgétaire |
| SHOGEN-CLOCKCHECK-SEMANTIQUE-1 | le contrôle d'horloge de S2 mêle fraîcheur des sources et horloge de l'hôte (§1.2 pt 3) | orch. | rapport de S2 (limite) |
| SHOGEN-S2BIS-HETZNER-DISPO-1 | portée de « Currently not available » sur la page Hetzner non établie | orch. | G0 de DEPLOI-BIS |

### 8.2 Questions techniques ouvertes (aux advisors)

- **Q1** Loi nulle par rotations : validité sous trous comprimés et week-ends concaténés ; rotation par fenêtre contre par jour entier ; R = 9 999 ; décalages par SHA-256 ; graine = sha du manifeste.
- **Q2** Quorum majoritaire q_j = ⌊M_j/2⌋ + 1 contre q fixe ; accord par axe contre tout axe ; effet de M_j variable sur l'indépendance des indicatrices consolidées.
- **Q3** Seuils de dégradation (5 s, 1 s, 120 s, 2 témoins sur 3, 2 s) ; choix des témoins (serveurs racines, noms de résolution).
- **Q4** τ au P99,9 ou au maximum (règle d'ADR-0022) pour la re-dérivation sur S2 ; σ par la règle de clôture sur 28 jours.
- **Q5** Unité R1 = hôte (OKX = `okx_ticker`) ; coingecko et defillama en deux unités.
- **Q6** Cibles d'effet pour la puissance (taux d'incidents par jour, durée, part des unités touchées) ; garder le stress confirmatoire (m = 2) malgré une puissance plus faible.
- **Q7** Lectures concurrentes et δ = 15 s contre lectures en série et δ = 10 s.
- **Q8** M = 4 contre 3 ou 5 ; un observateur hors UE.
- **Q9** Lectures admises au rodage (classe M) et usage pour remplacer un observateur.
- **Q10** Règle de fusion de la partition R2 multi-points de vue.
- **Q11** Garde d'information du pt 5 (deux unités avec au moins un écart) suffisante, ou minimum d'écarts.
- **Q12** Modèle d'accès : aucun agent sur les observateurs pendant la campagne ; procédure d'intervention.

## 9. Provenance

- **Sources internes lues** [lu] (lignes au journal G1) : brief ; `docs/PASSATION-CLOUD.md` ; `JOURNAL.md` l.300-324 ; avis produit ; G0 des lots d'après S2 (dont l'ajout daté de 03:09:29 UTC) ; avis G4 §3 ; ADR-0028 (en entier) ; paquet de S2 (en entier) ; annexes B (lignes ciblées) et D (en entier) ; ADR-0022, 0023, 0024, 0026 ; docs 04 §2, 08, 09, 10 (l.1-276, l.376-500), 17 ; `docs/DEVOPS.md` ; `docs/R-8-outillage.md` l.1-60 ; `s2-harness/README.md`, `RUNBOOK-campagne.md`, `collector.py`, `run_campaign.py`, `sources.py` (l.1-120, l.230-402), `window.py`, `journal.py`, liste des fonctions de `records.py`, `tests/test_hote_deux_flux.py` l.1-40 ; rendu J28 blocs 1, 3, 5, 6 et [SENSIBILITÉ].
- **Sources externes lues** [lu], 2026-10-04 : pages et catalogues tarifaires du §3 ; RIPEstat (as-overview, network-info) ; documentation de chrony ; root-servers.org ; documentation de Pyth et page des plans ; taux BCE. Non lues : pages Vultr, Linode et UpCloud (HTTP 403), registre Debian (défi anti-robot), API Vultr (délai dépassé).
- **Calculs** [calc] (dossier `calc/` du rédacteur, non versé) : `puissance.py` (sha256 `e4b2c13e…a2da82`), `sim_rotation.py` (`1ca880e6…5aba`), `sim_duree.py` (`33d69e68…85f3fd`), `budget.py` (`94300058…1944`), sorties `sim_rotation_out_20261004.txt` (`bb745143…0ab7`) et `sim_duree_out_20261005.txt` (`68919e59…486e`). Recompte des valeurs du rendu : z, z_bloc, γ̂₀, FIV égaux aux valeurs imprimées à 6 chiffres.
- **Réviseurs prévus** : advisors (§8.2), validateur (cp-1), puis orchestrateur (R-21) ; le rédacteur n'a généré aucun des lots qu'il cite.
