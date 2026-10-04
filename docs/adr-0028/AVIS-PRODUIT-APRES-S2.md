# Avis advisor — après S2 : chemin de Shōgen vers un produit vendu et un standard institutionnel

- **Gate 0** : modèle résolu `claude-fable-5-1` (advisor, effort medium ; CLAUDE.md §7). Date : 2026-10-04 (date de session ; pas d'accès shell pour `date -u`).
- **Brief** : `scratchpad/avis-produit/BRIEF-AVIS-PRODUIT.md`, sha256 `a992eca0…2199c`.
- **Attestation d'exposition (forme ADR-0028 annexe D.3)** : je n'ai ouvert aucune pièce de `docs/15-*`, `docs/16-*`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, ni aucun `*.jsonl`. Je n'ai pas lu le bloc 2 du rendu (repère `grep -n '^\[BLOC'` seulement). Pièces lues : ADR-0028 (corps, §1 à §8), docs 02, 04, 05, 06, 07, 08, 09, 10 (§1, §5, §7), 17, et les blocs 3, 5, 6 et la section SENSIBILITÉ de `docs/adr-0028/execution/rendu-2026-10-04/shogen-27b0e30-rendu-20261004T011129Z-943.3-j28.out` (l.435447-435821). Les valeurs z/K sont post-rendu : leur lecture est autorisée par le brief.
- **Conventions** : « rendu » = le fichier J28 ci-dessus ; [inféré] = mon raisonnement.

## 1. Ce que S2 établit pour le produit

**Ce qui est établi, et utilisable par un acheteur institutionnel (axe R2, descriptif, daté).**
- Concentration de la couche de livraison : 7 hôtes sur 10 derrière AS13335 Cloudflare, attribution croisée RIPEstat = Cymru « concordant » sur 10/10 hôtes, datée 2026-09-28T01:17-01:18Z (rendu l.435676-435691) ; k_eff = 4 pour k nominal = 10, partition nommée (rendu l.435779-435793). C'est exactement l'« angle vide n°2 » de l'état de l'art (doc 06 l.59-62) : personne ne publie cette mesure pour les sources d'un feed. Elle est recalculable depuis les journaux scellés (ADR-0003 ; doc 04 l.174-181).
- L'axe contenu ne fusionne rien (critère T = 1 ; rendu l.435695, l.435767) mais corrobore les amonts déclarés : coingecko × defillama ρ_resid = 0,78 et co-aberrance z = 129 (rendu l.435726), cohérent avec `basis:doc` « Almost all tokens are priced using CoinGecko's API » (rendu l.435763). Un acheteur lit : « coins.llama.fi n'est pas un chemin d'amont distinct de coingecko » (rendu l.435763) — nommé, pas noté (ADR-0007, doc 04 l.112-116).
- Le drapeau 2 est éteint et la raison est imprimée (rendu l.435795-435797) : aucune surclamation possible.

**Ce que la mesure R1 dit, honnêtement.** La règle scellée rend NE REJETTE PAS (discordance) dans les deux strates : z_s = 20,8 et 28,5 mais z_bloc = 1,95 et 1,74 < 2,33 (rendu l.435516-435522). Lecture : le modèle binomial à fenêtres indépendantes est rejeté, la cause reste indécise entre co-défaillance des sources et dépendance sérielle (ADR-0028 §1 bis.1 pt 8). Le descriptif désigne fortement l'observateur [inféré] : K = 154 dont 153 fenêtres à ≥ 2 `panne_transport`, 0 fenêtre K faite d'écarts de prix (rendu l.435532-435533) ; c_s = 9 fenêtres « calme » où **tous** les flux du pool portent `panne_transport` en même temps (rendu l.435532) ; la sensibilité « plage ADR-0025 incluse » fait passer K de 154 à 408 en calme (rendu l.435807-435809) : la santé du harnais pèse plus que les sources. Le rendu le déclare lui-même : « le z confirmatoire inclut les modes communs de l'observateur (hôte, DNS, réseau) » (rendu l.435531). FIV ≈ 115 et 266 (rendu l.435495, l.435499) avec des runs maximaux de 6 et 2 (rendu l.435497, l.435501) : la dépendance n'est pas des rafales courtes mais un regroupement des pannes sur des heures [inféré], signature d'épisodes d'infrastructure du collecteur plutôt que de co-défaillances de contenu [inféré].

**Ce qu'on ne peut pas vendre à partir de ce résultat** (registre doc 09, l.20-31) :
- aucun certificat R1 : ni « co-défaillance mesurée » entre sources (cause non identifiée, pt 8 de la règle), ni « sources sans co-défaillance détectée » (doc 09 l.21 : la règle a rejeté le binomial) ; l'énoncé « n'est pas rejeté » est interdit d'impression en discordance (ADR-0028 §1 bis.1 pt 8) ;
- aucune phrase sur l'exactitude ou la qualité des sources (doc 09 l.24, l.30) ; aucune sur Pyth (0 lecture ok, retiré, ADR-0028 D1) ;
- aucun « risque Cloudflare » côté origine : k_eff est « côté livraison » (rendu l.435770, résidu 1) ; la mesure est mono-vantage, résolveur Cloudflare pour mesurer une dépendance à Cloudflare, résidu « à son MAXIMUM, publié » (rendu l.435772, l.435774) ;
- aucune généralisation : une classe (BTC/USD), un observateur, 28 jours, un hôte de collecte (brief ; doc 10 l.40-43 : lecture HTTPS nue, pas un lot de témoignages) ;
- aucun monitoring payant ni alerte : « rien ne se vend ni ne se publie avant que S2 ait produit ses n/K/z » est levé pour la publication, pas pour le payant (doc 05 l.156-159 ; doc 07 l.98-105 : le gratuit précède le payant).

**Verdict pour le produit** : le « cœur différenciant » (doc 02 l.85-92) est à moitié vivant : R2 discrimine sur données réelles ; R1 n'a pas été testé dans des conditions où il pouvait trancher. Ce n'est pas « les axes ne discriminent pas » (doc 05 l.126-127) : c'est « l'instrument R1 a mesuré son propre observateur » [inféré]. La révision de doc 04 est due (ADR-0028 D9 « si (i) est faux »), mais elle porte sur la définition d'écart et l'observateur, pas sur la thèse des rangs.

## 2. Bifurcation D9 et clause D6 (vi)

**Recommandation : suivre la conséquence pré-enregistrée (FAUX → priorité G4 et révision de 04 ; ADR-0028 D9, §1 bis.1 pt 11), ET lancer une campagne S2-bis pré-enregistrée, conçue pour être décisive.** Options :

| option | pour | contre | avis |
|---|---|---|---|
| (a) collecte arrêtée, point final | conforme à D6 (vi) et doc 10 l.33-34 (« jetable ») ; aucun coût | laisse la thèse centrale non testée ; le papier S5 n'a pas de chiffre R1 (doc 05 l.245) | insuffisant seul |
| (b) « benchmark continu » (promotion de la collecte) | continuité des séries | déclencheur D6 (vi) non atteint (FAUX) ; promouvoir un instrument qui mesure son observateur reproduit le défaut | **non** |
| (c) S2-bis : nouvelle campagne, nouveau G0, harnais réécrit sur la frontière D6 (i) | répond à la question d'origine ; les leçons de S2 sont nombreuses et datées | coût d'une campagne (≈ 4 à 6 semaines de collecte + lots) | **oui**, en parallèle de G4 et de la révision de 04 |

**Ce qui rend la règle décisive en S2-bis** (ordre d'importance [inféré]) :
1. **Plusieurs observateurs indépendants** (≥ 3 hôtes, ASN et résolveurs DNS de familles distinctes ; la sonde multi-résolveurs est déjà « DUE » par doc 10 §4.1, rendu l.435772). Définition d'écart « panne de source » := non-réponse constatée par **≥ 2 observateurs** dans la fenêtre ; une non-réponse vue par un seul observateur est une panne d'observateur, censurée et comptée à part (SHOGEN-HOST-DEGRADED-1 devient une règle ex ante, plus un descriptif). Le mode commun du collecteur sort de K par construction.
2. **Exclusion de dégradation du harnais écrite avant la campagne** (critère chiffré sur `resolve_failed` et `clock_check`), pour ne plus avoir à amender après coup comme ADR-0025/D5 (ADR-0028 D5).
3. **Statistique par événements ou ℓ repensé** : avec FIV 115-266 (rendu), la puissance par fenêtre est ruinée ; SHOGEN-DEP-FENETRES-2 (fixed-b, événements ; doc 08 l.30) doit être tranché **avant** le paquet, et n par strate fixé par un calcul de puissance qui prend ces FIV comme a priori. EMD_s observé : 196 fenêtres (0,8 % de n) en calme, 211 (1,9 %) en stress (rendu l.435518, l.435521) : cible d'effet à écrire.
4. **Pyth** : clé obtenue avant le lancement, ou flux retiré ex ante (ADR-0028 D1 (a) a dû le faire a posteriori).
5. **τ_classe** : P99 observé 3 à 5 fois sous τ (rendu l.435526-435530) : l'axe hors-enveloppe n'a presque jamais tiré (0 fenêtre K). Re-dériver τ sur S2 (SHOGEN-TAU-REDERIV-1) et le sceller pour S2-bis : c'est licite, les données de S2 ne sont pas celles de S2-bis.

**À pré-enregistrer avant S2-bis** : règle de décision (forme de SHOGEN-CRITERE-R1-1 adaptée), définition d'écart à quorum d'observateurs, liste des observateurs et de leurs ASN/résolveurs, pool et règle D1, strates et calendrier, règle d'arrêt à n fixe, ℓ ou statistique d'événements, règle d'exclusion de dégradation, τ et σ par classe, SIM-NIVEAU, inventaire D.1/attestations D.3, ancre externe du sceau (ADR-0028 D2, annexes D). Sans ces dix lignes, S2-bis refait S2.

**Risque principal** : S2-bis rend aussi « discordance » malgré les observateurs multiples. Alors le résultat est net : la dépendance sérielle est celle des sources (épisodes de marché/infrastructure communs), et c'est un résultat publiable sur l'objet, pas sur l'instrument [inféré].

## 3. Chemin vers un standard institutionnel

**Produit minimal vendable (12 mois)** : le **rapport de concentration d'infrastructure de livraison** pour un pool nommé par le client — k_eff côté livraison, partition ASN datée et cross-confirmée, amonts déclarés `basis:doc`, corroborations de contenu, liste exhaustive des axes non mesurés (doc 04 l.129-139, champ non optionnel) — recalculable offline. C'est le seul objet que S2 autorise à écrire sans vocabulaire interdit. Il devient « certificat de diversité » (R1 + R2) seulement après un S2-bis décisif.

**Qui achète** (doc 07 §3) : d'abord les oracles challengers (canal 2 ; « une arme contre l'incumbent », doc 07 l.43-52) et les protocoles de prêt (canal 3) ; les cabinets de risque (canal 1) sont conflités, aggravé par LlamaRisk/Chainlink CRE (ADR-0028 §4.8) : ne pas rouvrir D3 maintenant. L'angle réglementaire (DORA art. 28-30 tiers ICT, MiCA CASP) est cité par l'avis advisor-marché via ADR-0028 D9 (ii) (« DORA art. 29 ») ; **aucun texte DORA/MiCA n'est détenu dans biblio/** : procurement avant toute phrase commerciale [inféré, non détenu]. La concentration de fournisseurs ICT est exactement le vocabulaire qu'un rapport k_eff livraison parle [inféré].

**Preuve tierce, dans l'ordre** : (1) publication recalculable (`docs/11` + journaux + test de composition SHOGEN-S2-TUYAU-MONARK-1, ADR-0028 §3) ; (2) un recalcul public par un acteur hors équipe (c'est le critère D9 (ii)) ; (3) notaire tiers G4 pour que les témoignages S3/S4 cessent d'être auto-attestés (A(self-attestation), doc 08 l.20 ; doc 17 T-01) ; (4) revue indépendante du papier S5 (doc 05 l.240-245), dont les dettes de fetch (doc 06 l.117-122) sont bloquantes.

**Jalons** :
- 90 jours : `docs/11` commis et cp-2 ; clôture S2 (G7) ; préavis privé puis publication G9 (acte investisseur) ; recherche G4 rendue ; ADR S2-bis acceptée et paquet scellé ; export public filtré décidé (D10).
- 12 mois : S2-bis exécutée en rendu unique ; révision doc 04 ; S4 (certificat embarqué, k_eff) si S2-bis est VRAI ou NE REJETTE PAS net ; premier rapport de concentration vendu ou trois citations/recalculs externes ; arXiv S5.
- **Critère falsifiable de demande** (ADR-0028 D9 (ii), à reprendre tel quel) : dans les 90 jours après G9, au moins un acteur nommé hors équipe demande la méthodologie ou un certificat sur son pool, recalcule publiquement le chiffre, ou l'invoque au titre de DORA art. 29. Sinon : gap de packaging, question à l'investisseur (D9).

## 4. Les trois prochains lots (G0 rattachables, ordre, coût relatif)

1. **RENDU → `docs/11-mesures-pilotes.md` → cp-2 → G7 → clôture S2** (G0 : ADR-0028 D9 voie A, D6 (v), §3). Contenu : blocs 1-6 et sensibilités tels que rendus, vocabulaire doc 09, mention explicite « discordance ; cause non identifiée ; k_eff côté livraison ». Coût : faible (rédaction + revue, aucun code neuf). Débloque G9 et le critère de demande.
2. **DOC04-REV + G4-RECHERCHE** (G0 : ADR-0028 D9 « si (i) est faux » ; SHOGEN-G4-NOTAIRE-RECHERCHE-1, doc 17 T-01). Révision de doc 04 §2 : définition d'écart à quorum d'observateurs, A(window-dependence) au site (item 16 de §1 bis.11), « k_eff côté livraison » dans §3 ; recherche notaire tiers rendue avec options et coût. Coût : moyen (docs, zéro code). Peut courir en parallèle du lot 1.
3. **ADR S2-BIS** (G0 neuf : ADR de campagne, sous ADR-0024 pour la règle d'arrêt et ADR-0028 annexe D pour le pré-enregistrement). Contenu : les dix lignes du §2 ci-dessus, frontière D6 (i) respectée (collecte réécrite, chemin de recalcul réutilisé et déjà sous G0-G7, ADR-0028 D6 (ii)). Coût : moyen pour l'ADR ; élevé pour les lots de code et la campagne qui suivront (≥ 3 observateurs à opérer). À ne lancer qu'après la clôture S2 et l'acte de l'investisseur sur le budget.

Hors liste, volontairement : le lot « benchmark continu » (déclencheur non atteint) ; S4 (conditionné à D9 (i) et (ii)).

## 5. Décisions de valeur pour l'investisseur (langage clair, avec recommandation)

1. **Publier le J28 et les journaux (G9), avec préavis privé ?** Oui, avec le texte du lot 1 : « le test d'indépendance n'a pas pu trancher ; la concentration Cloudflare côté livraison est mesurée : 4 chemins indépendants sur 10 ». Publier le résultat négatif est ce qui rend le projet crédible (doc 05 l.126 : résultat négatif = résultat).
2. **Arrêter la collecte S2 ?** Oui, comme prévu (D6 vi). Elle n'est pas promue.
3. **Financer une campagne S2-bis à plusieurs observateurs ?** Oui : c'est la seule façon de savoir si R1 vaut quelque chose ; sans elle, Shōgen reste un produit R2 (concentration d'infrastructure), honorable mais plus étroit que la vision.
4. **Dépenser pour un notaire tiers (G4) ?** Lancer la recherche maintenant (gratuit) ; décider la dépense commerciale à son rendu. Sans G4, tout témoignage reste auto-attesté (doc 08 l.20) et aucun institutionnel ne l'acceptera [inféré].
5. **Envergure : position institutionnelle d'abord, ou revenu d'abord ?** (ADR-0028 §4.7) Position d'abord : benchmark gratuit et recalculable, revenu par rapports de concentration sur pools nommés dès qu'un acteur externe a recalculé. Le canal cabinets de risque reste fermé (§4.8).
6. **Passage public du dépôt ?** Export filtré après la clôture S2 (D10), jamais la bascule de visibilité (docs 15/16, §4.2/§4.11).
7. **Seuil alternatif 0,01 / 2,5758 (§4.10 b) ?** Non : la discordance ne vient pas du seuil, elle vient de la variance par blocs ; changer le seuil ne change rien ici (z_bloc = 1,95 et 1,74).
8. **Ancrer le sceau des prochains paquets (RFC 3161 / OpenTimestamps) ?** Oui, systématiquement (ADR-0028 §1 bis.7) : c'est ce qui permettra à un tiers de croire au pré-enregistrement de S2-bis sans croire Shōgen.

**Risques de cet avis** : (i) l'attribution des K à l'observateur est une inférence sur descriptifs, pas un test ; S2-bis peut la contredire ; (ii) le marché réglementaire (DORA/MiCA) n'est appuyé sur aucune pièce détenue ; (iii) le coût de ≥ 3 observateurs est estimé sans devis ; (iv) la fenêtre de 90 jours du critère de demande ne court qu'à partir de G9, qui attend un acte de l'investisseur.
