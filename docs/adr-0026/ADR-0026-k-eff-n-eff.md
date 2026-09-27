# ADR-0026 — Deux objets, deux noms : `k_eff` (compte de classes d'une partition R2) et `n_eff (inverse-Simpson)` (1/Σp²) ; dénominateur normatif d'une mesure de registre

- **Statut** : **G0 proposé** (rédigé par l'orchestrateur MONARK `claude-fable-5-1`, session « POKT X SHOGEN », 2026-09-27 01:3x UTC, sur l'adjudication du 26/09 — avis `advisor` Q2 et Q3, archivés `F:\PRODUITS\etude-2026-09-25-pocket\AVIS-advisor-2026-09-26.md`). À approuver au **checkpoint-1** (validateur-humain) avant toute correction de script ou de registre. Solde l'item **SHOGEN-KEFF-NEFF-ADR-1** (dette `04-certificat-diversite.md` §6.1 : « k_eff doit être défini par contraste avec le n_eff de Kish ») et porte **POCKET-DENOMINATEUR-1**.
- **Rattachement** : 04 §3 (« k_eff = nombre de classes de la partition, pas de membres » ; « R3 ne modifie jamais k_eff ») ; ADR-0008 (une arête `basis:doc` ne réduit pas k_eff) ; 09-vocabulaire (« k nominal, k_eff mesuré ») ; doc 15 §3 et §9.2/§9.3 ; ERC-8275 A.3.5 (`attestationCountEffective`, inverse-Simpson) [lu par le chercheur *agentique*] ; ADR-0006 pt 4 (« publier k_eff comme valeur à croire » interdit).

## Contexte — le glissement mesuré

1. Le script de mesure de l'étude Pocket (`F:\PRODUITS\etude-2026-09-25-pocket\lcd\analyse-suppliers.py`, prototype, jamais servi) imprime « `HHI … => k_eff (inverse Simpson) = …` » : il **nomme k_eff** une grandeur qui est 1/Σp² (inverse de l'indice de Simpson, « nombre effectif » au sens de Kish / de l'ERC-8275). Deux archives et le premier jet du doc 15 ont repris ce nom.
2. Dans Shōgen, `k_eff` est **défini** (04 §3) comme le **nombre de classes** d'une partition R2 établie par observables mesurés (`basis:measured`), jamais une moyenne pondérée. Sur Pocket, **aucune partition R2 n'est établie** (le seul observable on-chain est l'URL d'endpoint ; l'ASN est une dette P-3) : il n'existe donc **aucun « k_eff Pocket »**.
3. Le même script calcule la concentration **par service** en pondérant par **endpoint** (`svc_domains[sid][dom] += 1` pour chaque endpoint) alors qu'un siège de session est attribué par **supplier** (protocole §5, `session_hydrator.go` [lu]) ; et il prend pour dénominateur les **4 484 suppliers** alors que **165 n'ont aucun endpoint courant** (ils ne peuvent servir aucun siège). Valeurs déjà corrigées en aval (doc 15 §3 : eth 2,86 sur 4 158 suppliers candidats, contre 2,51 sur 7 587 endpoints **périmé** ; registre 3,08 sur 4 319 contre 3,3 sur 4 484 **non normatif**), mais le script et `RESULTATS-concentration.txt` portent encore les anciens noms et les anciennes unités.

## Décision (proposée)

1. **Deux noms, deux objets, partout** (docs, scripts, sorties, phrases publiques) :
   - **`k_eff`** = nombre de classes d'une partition R2 **établie** (`basis:measured`), entier, ≤ k nominal ; une arête `basis:doc` seule le laisse inchangé (ADR-0008) ; R3 ne le modifie jamais (04 §3). Il n'est publié **qu'avec** la partition qui le produit (les classes nommées, l'observable, la date) — sinon il redevient une valeur à croire (ADR-0006 pt 4).
   - **`n_eff (inverse-Simpson)`** = 1/Σᵢ pᵢ², réel, calculé sur une **répartition de parts** (sièges, suppliers, relais, stake) selon une clé d'agrégation **nommée** (domaine eTLD+1, propriétaire, ASN…). Il mesure la concentration, **pas** l'indépendance : deux domaines à parts égales donnent n_eff = 2 même s'ils partagent un hébergeur.
   - **Relation** : sur une même partition, n_eff ≤ k_eff, égalité à parts égales. Un n_eff **ne remplace jamais** un k_eff dans le certificat 04 ; il peut l'**accompagner** comme statistique descriptive, étiqueté avec sa clé et son dénominateur.
2. **Formule d'énoncé obligatoire** pour toute mesure de registre : « n_eff (inverse-Simpson) = *v*, clé = *X*, unité = *supplier candidat* / *siège* / *relais estimé*, dénominateur = *N* (exclus : *m*, motif), date, source (LCD hauteur *h* / indexeur) ». Un chiffre sans ces cinq champs est un défaut au sens de la règle Dettes.
3. **Dénominateur normatif d'un registre Pocket** (avis advisor Q3) : **suppliers ayant au moins un endpoint courant** (4 319 au 25/09 20:47:39Z ; 165 exclus, signalés) ; **unité par service = supplier candidat** (un supplier = un siège potentiel), jamais l'endpoint ; le domaine d'endpoint est un rang **R2 « couche RelayMiner »** (déclaré on-chain et servi), pas l'origine de la réponse. Les valeurs par endpoint existantes sont citées comme telles et marquées **périmées**.
4. **Correction du prototype** (`analyse-suppliers.py`, item POCKET-DENOMINATEUR-1) : (a) renommer chaque sortie `k_eff (inverse Simpson)` → `n_eff (inverse-Simpson)` ; (b) dénominateur = suppliers avec endpoint, exclus comptés et imprimés ; (c) par service : un supplier candidat compte **une fois** par domaine (dédoublonnage des endpoints d'un même supplier sur un même service ; un supplier annonçant deux domaines sur un service est **signalé** et compté selon une règle explicite : une part par domaine annoncé, motif imprimé) ; (d) sortie `RESULTATS-concentration-v2.txt` **à côté** de l'ancienne (jamais d'écrasement : l'ancienne est référencée par sha dans deux archives et le doc 15 §14).
5. **Oracle non-LLM du pt 4** : rejeu du script corrigé sur les 18 fichiers `suppliers-q*.json` gelés (sha `lcd/SHA256-suppliers.txt`) ⇒ doit reproduire **3,08** (registre, 4 319) et **2,86** (eth, 4 158) à ±0,01, et imprimer 165 exclus ; test versionné avec le script (les fichiers bruts restent hors dépôt, 34 Mo × 18 : le test lit un chemin déclaré et **échoue franchement** s'il est absent, jamais un « skip » silencieux).
6. **Registres à porter** (dans le même lot, après checkpoint-1) : 04 §3 (définition de n_eff par contraste, dette §6.1 pt 1 soldée pour la partie Kish) ; 04 §6 (rayer la partie « n_eff de Kish » du pt 1 ; le contraste TIFS 2016 / Vendi Score reste dû tel quel) ; 09-vocabulaire (ligne « n_eff n'est pas un k_eff ») ; doc 15 §3 (déjà conforme, 26/09 ; renvoi à cette ADR) ; `RESULTATS-concentration.txt` (bandeau « noms périmés, voir v2 », jamais réécrit).

## Alternatives écartées

- **Renommer k_eff en n_eff partout dans Shōgen** : détruirait la sémantique de 04 §3 (compte de classes d'une partition mesurée), qui est la thèse du produit ; l'inverse-Simpson est une statistique de concentration, pas un quorum.
- **Garder « k_eff » pour l'inverse-Simpson « comme l'ERC-8275 »** : l'ERC nomme sa grandeur `attestationCountEffective`, pas k_eff ; adopter son nom exact (n_eff inverse-Simpson) évite les deux collisions.
- **Dénominateur 4 484 « parce que c'est le registre »** : 165 suppliers sans endpoint ne peuvent tenir aucun siège ; les compter dilue la concentration mesurée sans base protocolaire.

## Ce que la décision coûte

Une correction de prototype et son test (worker, ≤ 1 h) ; trois registres à porter ; aucune pièce servie touchée (règle Branchement : les scripts d'étude ne sont pas « built » et ne le deviennent pas par cette ADR).

## Tuyaux (règle Branchement, déclaration obligatoire)

- Entrée : `lcd/suppliers-q*.json` gelés (sha), produits par `fetch-suppliers.py` le 25/09.
- Sortie : `RESULTATS-concentration-v2.txt`, consommé par le doc 15 §3 (renvoi) et par toute note future ; **aucune surface servie** ne le consomme — statut « prototype de mesure », jamais « built ».
- Test : oracle du pt 5.

## Provenance

Avis advisor Q2/Q3 (26/09, archivés) ; doc 15 §3, §9.2, §9.3 (sha `ae227cf8…` avant addendum) ; `analyse-suppliers.py` lu le 27/09 01:1x UTC (lignes `hhi_*`, `svc_domains`) ; 04 §3, §6 ; 09-vocabulaire l.20/26. Advisor intégré indisponible dans la session de rédaction (consigné).
