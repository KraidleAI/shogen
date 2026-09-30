# G0 — lot SIM-NIVEAU (item SHOGEN-SIM-NIVEAU-1) : niveau de z_s, z_bloc,s et de la règle sous le modèle nul, par simulation synthétique

- **Statut** : G0 proposé, planification à l'aveugle, contexte frais ; soumis au cp-1 bref du validateur-humain (annexe A, colonne « cp-1 » : bref). Conseil de planification, jamais verdict : G7 à l'orchestrateur, cp-1 au validateur.
- **Date** : 2026-09-30 (début du travail 07:02:45Z, `date -u`).
- **Auteur** : worker G0, modèle résolu **`claude-opus-5-5`** (identifiant exact déclaré par le harnais, R-1), effort `max`. Mandat : commande de mission de l'orchestrateur Shōgen (`claude-fable-5-1`), HEAD `f5b8269` (`f5b82693b8f1a99d6cc2fb53a5e3edd35b4e0a78`, 2026-09-30T07:48:19+01:00).
- **R-20** : aucun commit, aucun workflow. Git en lecture seule : `log`, `rev-parse`, `show <sha>:<chemin>`, `diff --quiet`, `status --porcelain`, `ls-files`. **Aucun `GIT_DIR`, aucun `GIT_WORK_TREE`, aucun `--write-tree`.**
- **Écritures** : sous `F:\tmp\shogen-lots\SIM-NIVEAU\` seulement (ce fichier, dossier `g0-mesure\`) et création de `F:\tmp\shogen-tests-tmp\`. **Rien d'écrit sur C:** (`python -B`, `PYTHONDONTWRITEBYTECODE=1`, `TMP`, `TEMP` et `TMPDIR` sur `F:/tmp/shogen-tests-tmp`). Rien d'écrit dans `F:\Shogen` (`git status --porcelain` inchangé : seul `?? .claude/worktrees/`, préexistant).
- **Web** : deux lectures sur place de la documentation Python 3.14.7 (`firecrawl_scrape`, `maxAge: 0`, 2026-09-30 vers 07:14Z) ; aucune API de données.
- **Rattachement** : ADR-0028 §1 bis.1 pts 3, 5 et 7 ; §1 bis.2 ; §1 bis.10 (blob `8b0c2890…` à `f5b8269`) ; annexe A, ligne SIM-NIVEAU (blob `bd833e17…`) ; annexe D.2 à D.4 (blob `7874017e…`) ; CRITIQUE v2 §4.1 et §4.3 ; AVIS-advisor-defi-2026-09-30 Q1 (v) ; RECONCILIATION-Q2-advisor-defi §3.

## 0. Attestation d'exposition (forme de l'annexe D.3)

**Je n'ai vu ni z, ni K, ni P̂_more, ni φ des journaux de campagne, et je n'en ai calculé aucun. Je n'ai lu aucun taux d'écart ni de panne d'une source de la campagne. Aucune statistique S2 n'a été calculée.**

**Pièces de D.2 et de la commande de mission non ouvertes** (ni contenu, ni ligne) :
- `F:\shogen-campagne\*` (journaux scellés, REPAIR-*, INCIDENT-*, CLOTURE-*, `J0-STATUS.txt`, `LISEZ-MOI.txt`) et toute copie, dont `F:\tmp\shogen-g2-lotA\work\campagne-copie\` ;
- `F:\tmp\shogen-j28\*` (dont `baseline_step0.out`) ;
- `F:\Monark\docs\measure-M009a.md`, `G1-lot-m009.md`, `G2-lot-m009.md`, ADR-M002 ;
- `F:\tmp\shogen-carto-2026-09-29\` en entier : `campagne.md`, dossier `campagne\`, `_result.json`, `_workflow-output.json`, `CARTOGRAPHIE-2026-09-29.md`, `PAROXYSME-Shogen.md`, dossier `avis-adr0028\` ;
- `docs/rapports/cartographie-2026-09-29.md` : aucune ligne ; `docs/adr-0025/*` : aucune ligne ;
- `ARCHIVE-shogen-interne.md`, `AVIS-advisor-2026-09-26.md` (Pocket) ;
- `JOURNAL.md` : non ouvert ; aucune transcription de session ;
- contenu des autres dossiers de `F:\tmp\shogen-lots\` : noms de fichiers seulement (`ls`).

**Pièces lues** (lecture seule) :
- ADR-0028 (blob `8b0c2890…`) : l.1-62 (en-tête, §1 D1 à D5) et l.63-180 (§1 bis) ; annexe A entière ; annexe D entière (D.1 ne porte, par construction, aucune valeur de taux, de z, de K, de P̂_more ni de φ) ;
- dossier `F:\tmp\shogen-paquet\consultations-2026-09-30\` (`sha256sum -c SHA256SUMS.txt` : 11/11 OK) : RECONCILIATION-Q2-advisor-defi (`b820171c…`) entière ; AVIS-advisor-defi (`5619e2ac…`) l.5-47, plus les lignes affichées par des `grep` ; CRITIQUE v2 (`9d6fbf70…`) l.3-40 et l.215-312 ; DEMANDE, DECISIONS-orchestrateur, AVIS-advisor et CRITIQUE v1 : fragments de ≤ 160 caractères affichés par un `grep` des motifs « 0,02 », « p = », « arbitraire » (aucun ne porte un taux de source) ;
- doc 10 (blob `993c8bc4…`, dernière modification `2d02276` du 2026-08-20, antérieure à la campagne) : l.360-482 (§5.1 à §5.4), l.612-668 (§9), plus des `grep` ; doc 09 (blob `f7ca4e41…`) entier ;
- `docs/adr-0022/sigma-tau.json` entier (blob `472ecbbf80add87b92bbed3bcc69c4e9208f9a32` à `f5b8269` ; seul commit : `ed479c5`, 2026-08-26T18:58:57Z, avant la première fenêtre) ;
- `s2-harness/shogen_s2/r1.py` (blob `1d6a908c…`) : l.1-80, l.199-280, l.379-524, plus un `grep` des `def` ;
- corpus : `templates/adr.md` ; doc 02 l.29-40 et des `grep` ; `xtask/src` (`grep` du périmètre balayé) ; `.github/workflows/gates.yml` (`grep`).

**Exposé à** (classe M, constantes de conception et résultats synthétiques ; aucun taux par source, aucune statistique de résultat) :
- comptes opérationnels repris par l'ADR et les avis : n = 35 982 (J28) ; 2 618 fenêtres exclues, dont 909 en stress ; 17 314 et 9 261 (coupes J14) ; Pyth, 0 lecture `ok` sur 40 804 ; `resolve_failed` 815 sur 5 313 (15,3 % dans la plage contre 1,85 % hors plage : santé du harnais DNS) et 735 sur 39 717 ; 483 `clock_check` ; pertes de 2 552, 4 468 et 645 fenêtres ; T_fin = 38 600ᵉ fenêtre ; bornes epoch de la plage ADR-0025 ; fin de campagne vers 2026-09-28T01:27Z ;
- constantes antérieures à la campagne : σ_classe et τ_classe de `sigma-tau.json` ; K&L (N = 27, n = 10⁶, K = 1255, z = 100,51) ; « si P̂_more ≈ 10⁻³, n ≳ 10 010 fenêtres » (doc 10 §9 pt 5) ;
- résultats de simulations **synthétiques** antérieures, à p = 0,02 (RECONCILIATION §3, CRITIQUE v2 §4.3, AVIS Q1 (v)) : taux de rejet de z de 10 à 34 % sous runs de 5 à 60, aucun rejet de z_bloc à ℓ = 240 sur R ≤ 150 ; fixture synthétique K = 30 et 288 (annexe A, ligne B0) ;
- le nom d'une source (binance) dans l'attestation D.3 (a), dont les valeurs sont masquées.
- Aucune de ces valeurs n'entre dans le choix de p (§3), sauf n (ordres de grandeur fixés par l'annexe A) et les constantes de conception nommées.

## 1. Objet et conséquence pré-déclarée

**Objet.** Mesurer, par simulation sur données synthétiques seules, le taux de rejet à tort à 2,33 de z_s, de z_bloc,s (ℓ = 240) et de la règle SHOGEN-CRITERE-R1-1 (valeur REJETTE, ADR §1 bis.1 pt 5) sous un modèle nul exact : écarts des 11 flux mutuellement indépendants par construction (modèle d'indépendance du pool de doc 10 §5.1), avec dépendance sérielle markovienne. C'est la mesure que demande §1 bis.1 pt 7 : « Il n'est pas démontré ≤ 0,01 en échantillon fini : SHOGEN-SIM-NIVEAU-1 le mesure avant le scellement, et sa sortie est versée au paquet. »

**Conséquence pré-déclarée (C-6 du cp-1 de l'amendement ; ADR §1 bis.1 pt 7 ; annexe A)** : la sortie ne modifie ni ℓ, ni le seuil, ni la règle ; elle est imprimée avec l'erreur-type de Monte-Carlo de chaque cas ; tout changement de ℓ après sa lecture est un nouvel amendement daté, sous le veto §4.10 a.

**Ajout de ce G0 (même principe)** : ni p, ni R, ni la graine, ni la liste des cas, ni les définitions des taux ne changent après la lecture d'une sortie. Une seconde exécution à paramètres changés est une déviation déclarée ; les sorties des deux exécutions sont conservées, avec leurs sha256.

## 2. Modèle nul exact

- **Flux** : N = 11 flux simulés, indexés i = 1..11 ; D_{i,t} ∈ {0, 1} vaut 1 si le flux i est en écart dans la fenêtre t ; t = 1..n, grille complète (aucune fenêtre absente), une seule strate.
- **Indépendance entre flux** : les 11 processus (D_{i,t})_t sont mutuellement indépendants, par construction. C'est le modèle d'indépendance du pool de doc 10 §5.1, simulé ; ce n'est une affirmation sur aucune source réelle (doc 09).
- **Loi d'un flux** : chaîne de Markov stationnaire à deux états, taux marginal P(D_{i,t} = 1) = p, avec P(D_t = 1 | D_{t−1} = 1) = a et P(D_t = 1 | D_{t−1} = 0) = b :
  - L ∈ {5, 20, 60} : a = 1 − 1/L, b = p/(L(1−p)). Longueur moyenne d'un run d'écart : exactement L. Corrélation au retard 1 : ρ = a − b = 1 − 1/(L(1−p)), paramétrisation de la RECONCILIATION §3. Loi stationnaire : b/(1 − a + b) = p exactement en arithmétique exacte ; avec les flottants a et b, à l'arrondi double près [inféré] ;
  - **L = 1 := tirages indépendants** (annexe A : « L = 1 : tirages indépendants ») : a = b = p, ρ = 0, run moyen 1/(1−p) = 1,0204. Écart déclaré à la formule : prise à L = 1, ρ = 1 − 1/(L(1−p)) donnerait ρ = −p/(1−p) ≈ −0,0204 (run moyen exactement 1), qui n'est pas iid. La RECONCILIATION §3 posait « L = None ⇒ iid » : même objet que ce L = 1 ;
  - état initial D_{i,1} ~ Bernoulli(p), la loi stationnaire : chaque fenêtre a exactement la loi marginale du modèle de §5.1.
- **Agrégats** : m_t = Σ_i D_{i,t} ; I_t = 1{m_t ≥ 2} ; K = Σ_t I_t (« fenêtres à ≥ 2 écarts », doc 10 §5.1 ; même sommande que `compute_r1`, r1.py l.424-440).
- **Portée de la dépendance** : elle est géométrique, donc de portée infinie ; la prémisse « portée < ℓ » du pt 7 n'est qu'approchée. La corrélation du flux au retard ℓ vaut ρ^240 : 1,6·10⁻²⁴ (L = 5), 3,5·10⁻⁶ (L = 20), **1,6·10⁻² (L = 60)** (`calc_constantes.out.txt`). Le niveau mesuré à L = 60 inclut donc le biais de troncature du noyau de Bartlett au-delà de ℓ. Le script imprime ρ^ℓ par cas.

## 3. Taux marginal : p = 0,02, fixé ici à l'aveugle

**Valeur.** p = 0,02, le même pour les 11 flux et pour les 8 cas. Arithmétique exacte (`calc_constantes.py`, `fractions`) : P₀ = 0,98¹¹ = 0,8007313507 ; P₁ = 11·0,02·0,98¹⁰ = 0,1797560175 ; **P_more(0,02) = 0,0195126317**. Garde de doc 10 §5.4 en espérance : n·P_more(1−P_more) = 191,32 à n = 10⁴ et 478,30 à n = 2,5·10⁴, soit 19,1 et 47,8 fois le seuil 10.

**D'où vient p : critère de domaine, puis choix du moins favorable.**
1. *Point de départ, doc 10* : la seule échelle de P_more antérieure à la campagne est la contrainte de conception de doc 10 §9 pt 5 : « si P̂_more ≈ 10⁻³, n ≳ 10 010 fenêtres, soit ≈ 7,0 jours à w = 60 s, par strate ». Le taux par flux qui la réalise est p_d = 0,0043196 (P_more(p_d) = 10⁻³, bissection dans `proto_temps.py`).
2. *Critère de domaine* : la simulation doit mesurer le niveau de la règle là où elle s'évalue, et non la garde §5.4 ni la dégénérescence σ̂² = 0 (qui rend z_bloc non publiée). Critère : garde tenue et σ̂² > 0 dans les R_pilote = 200 réplications synthétiques du pilote au cas le plus persistant (L = 60, n = 10⁴ : le plus petit n, le moins de runs).
3. *Pilote de domaine* (synthétique ; `proto_temps.out.txt`, rejoué à l'identique dans `proto_temps.out2.txt` ; il n'imprime **aucun** taux de rejet) :

| p | L | n | n·P_more(1−P_more) | garde non tenue | σ̂² = 0 | runs d'écart par flux (espérance) |
|---|---|---|---|---|---|---|
| 0,0043196 (p_d) | 1 | 10⁴ | 9,99 | 118/200 | 0/200 | 42,56 (43,01) |
| 0,0043196 (p_d) | 60 | 10⁴ | 9,99 | 136/200 | 156/200 | 0,68 (0,72) |
| 0,01 | 60 | 10⁴ | 51,53 | 8/200 | 45/200 | 1,64 (1,67) |
| 0,02 | 60 | 10⁴ | 191,3 | 0/200 | 0/200 | 3,38 (3,33) |

   À l'échelle de conception de doc 10, la garde tombe dans 59 à 68 % des réplications : la simulation y mesurerait la garde, pas le niveau. À p = 0,01, z_bloc n'est pas publiable dans 22,5 % des réplications du cas le plus persistant. À p = 0,02, aucune réplication du pilote n'est hors domaine (borne unilatérale à 95 % de la fraction hors domaine : 1 − 0,05^(1/200) = 1,5 %).
4. *Choix du moins favorable dans le domaine* : p = 0,02 est la plus petite valeur de la série 1-2-5 {…, 0,005 ; 0,01 ; 0,02 ; 0,05 ; …} qui tient le critère : 0,01 échoue (45/200) et p_d = 0,0043 échoue ; 0,005, compris entre les deux, n'a pas été simulé et son échec est inféré par monotonie du nombre de runs en p [inféré]. On prend la plus petite parce que la conservativité du plug-in croît avec p : facteur de variance du numérateur 0,6867 (SD 0,8286) à p = 0,02 contre 0,8236 (SD 0,9075) à p = 0,01 (CRITIQUE v2 §4.2, l.258 [lu] ; AVIS-advisor-defi Q1 pt 5, l.33 [lu] ; au premier ordre, facteur ≈ 1 − 20p pour N = 11, dérivation du rédacteur [inféré]). Au-dessus de 0,02, le test serait mesuré dans une configuration plus favorable.
5. *Robustesse du critère* : les fractions hors domaine du pilote sont nettes (0/200 contre 45/200). Toute exigence de domaine comprise entre 1 % et 20 % de réplications hors domaine donne le même p. Le pilote a été lancé avant l'écriture de ce critère ; ce G0 le déclare.

**Provenance, mot pour mot.**
- p = 0,02 apparaît d'abord dans AVIS-advisor-defi-2026-09-30, l.40 : « SYNTHÉTIQUE (N = 11, p égal 0,02 sauf mention … p est arbitraire ». Son auteur atteste, l.7 et l.11, « Je n'ai vu ni z, ni K, ni P̂_more, ni φ » et « sans aucun taux d'écart par source ». La RECONCILIATION (l.15 et l.89 : « p = 0,02 arbitraire ») et la CRITIQUE v2 (§4.3, l.297) le reprennent.
- Un `grep` de « 0,02 », « p = » et « arbitraire » sur DEMANDE et DECISIONS-orchestrateur, les deux pièces écrites par l'orchestrateur, exposé (D.3 a), ne trouve que la borne de famille 0,02 (D2 pt 4) : l'orchestrateur n'a pas suggéré de taux de source.
- **Coïncidence assumée** : p = 0,02 est le p des chiffres « 10 à 34 % » du texte scellable (§1 bis.1 pt 7) et de la ligne de repli (§1 bis.3). La sortie de ce lot les remesure donc au même p, à R = 10⁵ au lieu de R ≤ 150, avec l'erreur-type de chaque cas : le paquet ne portera pas deux jeux de chiffres à deux p différents.
- **Exposition déclarée** : l'auteur de ce G0 a lu les niveaux synthétiques antérieurs à p = 0,02 (ligne « Exposé à »). Ils ne motivent pas le choix : le motif est le domaine (points 2 à 4), qui écarte les p plus petits, et la direction du plug-in, qui écarte les p plus grands.
- **Aucune donnée de campagne** : p ne vient d'aucun taux de source. Les seules entrées du choix sont doc 10 §5.4 (seuil 10), doc 10 §9 pt 5 (échelle 10⁻³), N = 11 (D1), les n et L de l'annexe A, ℓ = 240, et le pilote synthétique.

**Limite déclarée** : le niveau n'est mesuré qu'à p = 0,02. Aux p < 0,02, le plug-in est moins conservateur, mais le domaine se dégrade au cas le plus persistant. Item formé : SHOGEN-SIM-NIVEAU-P-1 (§10).

## 4. Cas, nombre de réplications, graine

- **Cas** (annexe A) : L ∈ {1, 5, 20, 60} × n ∈ {10⁴ ; 2,5·10⁴}, soit 8 cas, dans cet ordre (L croissant, puis n croissant). Constantes communes : ℓ = 240 ; seuil `Decimal("2.33")` (`SEUIL_Z`, r1.py l.58) avec « ≥ » ; garde `Decimal(10)` (`SEUIL_HIST`, l.56) avec « < » pour « non tenue » ; garde de blocs n ≥ 30·ℓ = 7 200, qui ne mord sur aucun cas (n ≥ 10⁴) et reste codée ; `DECIMAL_PREC` = 50 (l.55).
- **Paramètres par cas** (`calc_constantes.out.txt` ; flottants IEEE-754 tels que Python les calcule) :

| L | a | b | ρ | ρ^240 | runs d'écart attendus par flux (n = 10⁴ / 2,5·10⁴) |
|---|---|---|---|---|---|
| 1 | 0.02 | 0.02 | 0 | 0 | 196 / 490 |
| 5 | 0.8 | 0.004081632653061224 | 0,795918 | 1,6·10⁻²⁴ | 40 / 100 |
| 20 | 0.95 | 0.001020408163265306 | 0,948980 | 3,5·10⁻⁶ | 10 / 25 |
| 60 | 0.9833333333333333 | 0.00034013605442176874 | 0,982993 | 1,6·10⁻² | 3,33 / 8,33 |

- **R = 10⁵ réplications par cas** (annexe A : « au moins 10⁴ »). Motif : au niveau nominal α = 1 − Φ(2,33) = 0,00990308 (`statistics.NormalDist`, CRITIQUE v2 §4.2 [lu], recalculé), l'erreur-type de Monte-Carlo vaut 9,90·10⁻⁴ = 0,100·α à R = 10⁴ et 3,13·10⁻⁴ = 0,032·α à R = 10⁵. R = 10⁵ résout donc un écart de 10 % de α à 3 erreurs-types, ce que R = 10⁴ ne fait pas. Le prix est mesuré (§7) : environ 5,3 h de CPU au total.
- **Graine** : GRAINE = 20260930, fixée ici. Aucune autre graine n'a été essayée pour ce lot : le prototype utilise l'étiquette distincte `SIM-NIVEAU-proto`, donc des flux sans lien avec ceux du lot.
- **Dérivation par réplication**, indépendante de l'ordre d'exécution et du nombre de processus : seed(L, n, r) = entier big-endian des 8 premiers octets de sha256 de la chaîne ASCII `SHOGEN-SIM-NIVEAU-1|20260930|p=0.02|L={L}|n={n}|r={r}` (r = 0..R−1), puis `random.Random(seed)` (Mersenne Twister de la bibliothèque standard).
- **Stabilité du flux** [lu, docs.python.org/3.14/library/random.html, « Notes on Reproducibility », lu le 2026-09-30 vers 07:14Z] : (paraphrase, source non versée à biblio/ : random() rend la même suite pour la même graine avec le semeur compatible). Seul `random()` est utilisé. Chaque processus possède ses propres instances ; aucun fil d'exécution partagé.
- **Ordre des tirages** : pour i = 1..11 puis t = 1..n, exactement 11·n appels à `rng.random()` par réplication. D_{i,1} = [U < p] ; pour t ≥ 2, D_{i,t} = [U < a] si D_{i,t−1} = 1, [U < b] sinon (inégalité stricte). a et b sont les flottants `1.0 - 1.0/L` et `p/(L*(1.0 - p))`, avec p = 0.02 en littéral flottant ; à L = 1, a = b = p.

## 5. Statistiques calculées à chaque réplication (réplique de r1 à `f5b8269`, pas une approximation)

1. **Comptes** : e_i = Σ_t D_{i,t} ; K = #{t : m_t ≥ 2}.
2. **Plug-in** (doc 10 §5.1 ; `compute_r1`, r1.py l.450-452 et l.480-483) : p̂_i = `+(Decimal(e_i)/Decimal(n))` en contexte de précision 50 ; (P̂₀, P̂₁, P̂_more) = réplique ligne à ligne de `poisson_binomial` (l.199-216) ; garde = réplique de `gate_value` (l.219-223) ; garde tenue ⇔ garde ≥ 10 ; si la garde est tenue, z = réplique de `z_score` (l.231-238). Le choix du plug-in plutôt que du P_more théorique reproduit ce que fait `compute_r1`, c'est-à-dire ce que la règle évaluera.
3. **σ̂²_bloc**, estimateur de §1 bis.1 pt 3 : σ̂² = γ̂₀ + 2·Σ_{k=1}^{ℓ−1} (1 − k/ℓ)·γ̂_k, avec γ̂_k = Σ (I_t − Ī)(I_{t+k} − Ī) sur les paires présentes et Ī = K/n. Deux formes exactes en entiers, toutes deux calculées à chaque réplication :
   - *forme en lags*, « comptes entiers par lag », celle que §1 bis.1 pt 3 prescrit à B-DEP-1 : ℓn²σ̂² = N_lag = Σ_{k=0}^{ℓ−1} W_k·(n²·C_k − n·K·(S_k + S′_k) + K²·M_k), avec W_0 = ℓ, W_k = 2(ℓ − k), C_k = #{t : I_t = I_{t+k} = 1}, S_k = Σ I_t et S′_k = Σ I_{t+k} sur les paires (t, t+k) présentes, M_k = nombre de ces paires (n − k sur la grille complète). Les comptes se lisent sur des masques de bits : C_k = popcount(X & (X ≫ k)), etc. Sur 40 réplications, la forme en lags coûte 1,0 à 2,3 ms par réplication (`proto_temps.out.txt`) ;
   - *forme en sommes de blocs* (identité de CRITIQUE v2 §4.1) : ℓn²σ̂² = N_bloc = n²·A − 2nK·B + K²·C, où A = Σ_j c_j², B = Σ_j c_j·m_j et C = Σ_j m_j². La somme court sur les n + ℓ − 1 blocs de longueur ℓ de la série complétée par des 0 ; c_j compte les I = 1 du bloc j, m_j ses fenêtres présentes.
   - *Dérivation de l'identité*, recalculable : Σ_j B_j² = Σ_{t,u} x_t·x_u·#{j : t, u ∈ bloc j} = Σ_{t,u} x_t·x_u·(ℓ − |t − u|)₊, avec x_t = I_t − Ī (0 hors grille) ; en divisant par ℓ, on retrouve la forme en lags. Égalité exigée : N_lag = N_bloc en entiers, à chaque réplication (oracle 2b).
   - σ̂² = N/(ℓn²), rationnel exact, converti une seule fois en `Decimal(N)/Decimal(ℓ·n²)` (précision 50).
4. **z_bloc** = (Decimal(K) − Decimal(n)·P̂_more)/√σ̂² (précision 50 ; même numérateur que z), publiée ⇔ σ̂² > 0 (⇔ N > 0 ; ⇔ K ∉ {0, n}, CV2-10) et n ≥ 7 200.
   - Sources : `Decimal.sqrt` : (paraphrase, source non versée à biblio/ : sqrt rend la racine carrée en pleine précision) ; (paraphrase : la construction depuis un entier ou un flottant est une conversion exacte) [lu, docs.python.org/3.14/library/decimal.html, 2026-09-30].
5. **Valeur de la règle** (§1 bis.1 pt 5 ; comparaisons en `Decimal` non arrondies, pt 4) :
   - garde non tenue → NON ÉVALUABLE (cause « garde §5.4 ») ;
   - garde tenue ∧ z < 2,33 → NE REJETTE PAS ;
   - garde tenue ∧ z ≥ 2,33 ∧ z_bloc publiée ∧ z_bloc ≥ 2,33 → **REJETTE** (⇔ min(z, z_bloc) ≥ 2,33) ;
   - garde tenue ∧ z ≥ 2,33 ∧ z_bloc publiée ∧ z_bloc < 2,33 → NE REJETTE PAS (« discordance ») ;
   - garde tenue ∧ z ≥ 2,33 ∧ z_bloc non publiée → NON ÉVALUABLE (cause « rejet non qualifiable »).
6. **Diagnostics** (hors objet, imprimés) : FIV = σ̂²/(n·P̂(1−P̂)) ; R_centrage = Ī(1−Ī)/(P̂(1−P̂)) ; FIV_série = σ̂²/γ̂₀ ; runs de I_t (nombre, longueur moyenne, run maximal) ; drapeau « run maximal ≥ ℓ » (§1 bis.1 pt 9) ; comptes z ≤ −2,33 et z_bloc ≤ −2,33 (« hors famille, sans conclusion », pt 8).

## 6. Sorties

Trois fichiers, écrits seulement si tous les oracles internes passent (fail-closed : sortie ≠ 0 et aucun fichier écrit sinon), sans jamais écraser un fichier existant :
- **`sim_niveau.json`** (schéma `shogen.sim-niveau.v1`) :
  - en-tête : `item`, `script_sha256` (calculé à l'exécution sur les octets du script), `parametres` (N, p en chaîne, L, n, R, ℓ, seuils, garde de blocs, GRAINE, formule de dérivation, précision), `alpha_nominal`, texte de la conséquence pré-déclarée (§1) ;
  - par cas : L, n, a, b, ρ, ρ^ℓ, P_more(p) théorique ;
  - par cas, les **comptes** : R, garde non tenue, σ̂² = 0, z ≥ 2,33, z_bloc ≥ 2,33, REJETTE, NE REJETTE PAS, discordance, NON ÉVALUABLE par cause, z ≤ −2,33, z_bloc ≤ −2,33, run maximal ≥ ℓ ;
  - par cas, les **taux** (x, r = x/R, SE, et la borne unilatérale à 95 % quand x = 0) ;
  - par cas, les **diagnostics** : moyenne et écart-type de z (réplications à garde tenue) et de z_bloc (réplications où elle est publiée) ; médianes de FIV, FIV_série et R_centrage ; run maximal moyen ; moyenne de K/n ;
  - par cas, les **oracles** : résultats de (2), (2b) et (5), et une empreinte sha256 de la suite ordonnée des enregistrements par réplication (entiers et chaînes `Decimal`).
- **`sim_niveau.txt`** : en-tête (paramètres, α nominal, conséquence pré-déclarée), puis une ligne par cas avec L, n, R, garde non tenue, σ̂² = 0, taux z ≥ 2,33 (SE), taux z_bloc ≥ 2,33 (SE), taux REJETTE (SE ; borne à 95 % si x = 0), discordances, NON ÉVALUABLE (garde ; non qualifiable), SD(z), SD(z_bloc), FIV médian, run maximal ≥ ℓ.
- **`sim_niveau.log.txt`**, hors bit-identité : version de Python et `sys.executable`, plate-forme, nombre de processus, horodatages et durées, ligne de commande.

**Taux et dénominateurs** (tous sur les R réplications du cas, sans conditionnement) :
- r_z = #{garde tenue ∧ z ≥ 2,33}/R ;
- r_bloc = #{z_bloc publiée ∧ z_bloc ≥ 2,33}/R, qui mesure z_bloc seule, indépendamment de la garde §5.4 ;
- **r_règle = #{REJETTE}/R**, qui est le taux de rejet de min(z, z_bloc) au sens de la règle.

Pour chaque taux, SE = √(r(1−r)/R). Si x = 0, le SE vaut 0 et n'informe pas : la ligne imprime aussi la borne unilatérale exacte à 95 %, 1 − 0,05^(1/R) = 3,00·10⁻⁵ à R = 10⁵ (en une ligne : P(0 | r) = (1−r)^R = 0,05). α nominal = 1 − Φ(2,33) est imprimé à côté, pour comparaison. Aucun critère n'est tiré de cette comparaison (C-6).

**Formats** : entiers ; `Decimal` en chaîne ; flottants par `repr` pour le JSON, format fixe pour le texte ; sommes flottantes par `math.fsum` dans l'ordre des réplications ; médianes par `statistics.median`. Ni heure, ni durée, ni nom d'hôte, ni version dans le JSON et le texte (oracle 1).

**Chemin de versement** : les deux fichiers et leurs sha256 sont versés au paquet par l'orchestrateur (emplacement fixé par le lot PAQUET ; proposition : `docs/adr-0028/sim-niveau/`). Le sha versé est celui des octets produits par l'exécution du paquet (§7), jamais d'un fichier ré-écrit.

## 7. Implémentation : chemin, temps mesuré, décision Rust

**Chemin fixé** : **`scripts/sim/sim_niveau.py`** dans le dépôt, avec l'adaptateur d'oracle **`scripts/sim/sim_niveau_oracle_r1.py`** (§8, oracles 4 et 4a).
- Hors harnais : hors des chemins gardés par D.4 b (2) (`s2-harness/shogen_s2`, `s2-harness/tools`), donc sans effet sur la garde « code d'analyse du paquet ».
- Hors du périmètre balayé par `cargo xtask verify` : S-G4 et S-G5 ne recensent que les `.md` de `docs/` (`xtask/src/sg4.rs:102`, `sg5.rs:145`). Hors du job `s2-harness-unittest` (`gates.yml` l.92 : `unittest discover -s tests`).
- Le dossier `scripts/` n'existe pas à `f5b8269` ; le lot PAQUET y prévoit `scripts/sceau/` (ADR §1 bis.11 pt 10).
- Travail du G1 et du G2 : sous `F:\tmp\shogen-lots\SIM-NIVEAU\` ; commit par l'orchestrateur seul (R-20), après le G2.
- **Règle du sha** : l'exécution du paquet se fait sur le blob commis, exporté par `git archive <commit> scripts/sim | tar -x -C F:/tmp/shogen-lots/SIM-NIVEAU/exec-<commit>/`. Le `script_sha256` écrit dans le JSON est celui des octets exécutés, qui doivent être égaux au blob commis (contrôle : `git show <commit>:scripts/sim/sim_niveau.py | sha256sum`). Le paquet cite le commit, le sha du script et le sha de chaque sortie.
- Alternative écartée : le script sous `F:\tmp\` seulement, versé au paquet ensuite. Elle n'est ni versionnée ni revue sur diff, et un tiers ne la rejoue qu'à partir d'une copie.

**Bibliothèque standard seule** : `random`, `hashlib`, `decimal`, `fractions` (contrôles seulement), `itertools`, `math`, `statistics`, `json`, `multiprocessing`, `argparse`, `os`, `sys`. Aucune dépendance nouvelle (R-8 : sans objet).

**Temps mesuré** (`g0-mesure/proto_temps.py`, sha256 `ddf32543…6827`) : chemin chaud réel, c'est-à-dire 11·n tirages de Bernoulli par réplication, comptes en `bytearray`, plug-in et z en `Decimal`, σ̂² par sommes de blocs, puis par la forme en lags et contrôle d'égalité. Horloge murale `time.perf_counter`, Python 3.14.5 (`C:\Users\KACIMI\AppData\Local\Python\pythoncore-3.14-64\python.exe`), Windows 10 (build 19045), 24 processeurs logiques :

| exécution | n = 2,5·10⁴, L = 60 | n = 2,5·10⁴, L = 1 | n = 10⁴, L = 60 | n = 10⁴, L = 1 |
|---|---|---|---|---|
| 1 (07:10:27Z, `proto_temps.out.txt`, `b52fae75…`) | **0,292 s** / 10 rép. | **0,311 s** | 0,119 s | 0,120 s |
| 2 (`proto_temps.out2.txt`, `e36c3bd1…`) | **0,313 s** | **0,342 s** | 0,128 s | 0,138 s |

- Soit **0,029 à 0,034 s par réplication à n = 2,5·10⁴**, dont environ 70 % pour la génération. C'est environ 60 fois sous le seuil de 2 s/réplication (2/0,0342 = 58) de la commande de mission : **pas d'implémentation Rust** (non ouverte ; aucun crate, aucun `CARGO_HOME` utilisé).
- Prix total estimé avec la pire mesure : 4·10⁵ × 0,0342 + 4·10⁵ × 0,0138 = 19 200 s ≈ 5,3 h de CPU [inféré, par extrapolation linéaire en R].
- Sur 12 processus (`--processus 12`), environ 27 min par exécution complète [inféré : échelle linéaire non mesurée ; les durées réelles sont écrites au `.log.txt`]. La sonde `g0-mesure/proto_pool.py` (`292c31e2…`) a exécuté un `multiprocessing.Pool` (démarrage `spawn`, ordre de `imap` conservé), sortie 0.
- Si le G1 mesurait plus de 2 s par réplication (régression), la question Rust serait rouverte par un amendement de ce G0, jamais contournée.

**Parallélisme** : `multiprocessing.Pool(k).imap` sur les indices r, dans l'ordre, par paquets ; agrégation dans le processus principal, dans l'ordre des r. Comme la graine dépend de (L, n, r) seulement, les sorties ne dépendent pas de k (oracle 1b). k est un paramètre d'exécution, écrit au `.log.txt` seulement.

**Commandes** : `TMP`, `TEMP` et `TMPDIR` valent `F:/tmp/shogen-tests-tmp` ; `PYTHONDONTWRITEBYTECODE=1`.
- Exécution du paquet : `python -B <export>/scripts/sim/sim_niveau.py --sortie F:/tmp/shogen-lots/SIM-NIVEAU/run-<commit>-A --processus 12`, puis la même commande avec `…-B`. Les valeurs par défaut sont R = 10⁵, p = 0,02 et les 8 cas ; `--R`, `--p` et `--cas` ne servent qu'aux essais et, pour `--p`, à l'item SHOGEN-SIM-NIVEAU-P-1 ; le JSON écrit leurs valeurs.
- Aucun fichier dans `F:\Shogen` ; aucun `__pycache__`.

**Taille (R-25, seuil 200 lignes ajoutées par lot)**, estimation [inféré, à partir du prototype : 114 lignes non vides (l.1-129 de `proto_temps.py`) pour en-tête, générateur, plug-in, z, les deux formes de σ̂², z_bloc et la réplication ; 173 lignes au total] :
- `sim_niveau.py` ≈ 200 lignes : générateur 20, réplique du plug-in et de z 30, σ̂² en deux formes 30, réplication et règle 30, agrégation et taux 35, sorties 35, CLI et `Pool` 20 ;
- `sim_niveau_oracle_r1.py` ≈ 60 lignes.

Coupe proposée : **SIM-NIVEAU-a** (le script et les oracles 1, 1b, 2, 2b, 3 et 5) et **SIM-NIVEAU-b** (l'adaptateur, oracles 4a et 4). Si la mesure du G1 dépasse 200 lignes pour a, le G1 sous-coupe (générateur et statistiques, puis sorties et CLI) et chaque sous-lot reçoit sa ligne datée dans l'annexe A (précédent : lots B0 et B-SEG-1).

## 8. Oracles non-LLM

Les oracles (1) à (4) sont ceux de l'annexe A ; (1b), (2b), (4a) et (5) sont ajoutés par ce G0. Tout oracle interne en échec fait sortir le script en ≠ 0, sans écrire de fichier.

- **(1) Bit-identité** : deux exécutions du paquet (R = 10⁵, 8 cas, même graine), dossiers `-A` et `-B`. Les sha256 de `sim_niveau.json` et de `sim_niveau.txt` doivent être égaux (`cmp`), et les empreintes par cas aussi. Rejouées par l'orchestrateur.
- **(1b) Invariance au parallélisme** : R = 2 000, 8 cas, `--processus 1` contre `--processus 12`. JSON et texte doivent être identiques. Précondition du (1), exigée aussi au G2.
- **(2) Identité γ̂₀ = n·Ī(1−Ī)** à chaque réplication. γ̂₀ est calculé à partir des comptes du retard 0 (C_0, S_0, S′_0, M_0), en entiers : n²·C_0 − nK·(S_0 + S′_0) + K²·M_0 = n·(nK − K²). Le résultat R/R par cas est imprimé ; toute réplication en échec arrête le script.
- **(2b) Forme en lags = forme en sommes de blocs** : égalité exacte des entiers N_lag et N_bloc (§5.3) à chaque réplication, R/R imprimé. Le prototype l'a constatée sur ses 40 réplications chronométrées (`proto_temps.out.txt` : « identite lags == blocs sur les 10 : True », quatre fois). Elle rend l'oracle (4) exécutable : la forme en lags est celle que B-DEP-1 doit coder.
- **(3) Erreur-type imprimée par cas** : chaque taux du JSON porte x, r et SE, et la borne de x = 0. Contrôle au G2 : lecture du schéma, puis recalcul de SE depuis x et R pour les 24 taux.
- **(4) σ̂² du script = `r1.block_long_run_variance`** sur les 10 premières réplications de chaque cas, dès que B-DEP-1 est commis. `block_long_run_variance` est absente à `f5b8269` (`grep -rn` sur `s2-harness/` : aucune occurrence).
  - Critère : si B-DEP-1 expose ses comptes entiers par lag, égalité exacte de ces comptes ; sinon |σ̂²_r1 − N/(ℓn²)| ≤ 10⁻⁴⁰·N/(ℓn²), avec `Fraction(Decimal)` exacte. Marge : à la précision 50, une annulation de 10³ entre termes laisse l'erreur d'arrondi plusieurs ordres de grandeur sous 10⁻⁴⁰ [inféré].
  - La série synthétique est passée sur la grille window_start = 1 767 225 600 + 60·t (2026-01-01T00:00:00Z, epoch multiple de 60 ; t = 0..n−1), en une seule strate. L'appel exact est écrit au G1 de SIM-NIVEAU-b, après lecture de la signature commise.
  - Item conditionnel : SHOGEN-SIM-NIVEAU-ORACLE4-1 (§10).
- **(4a) Plug-in et z du script = r1 à `f5b8269`**, exécutable aujourd'hui, sur les 10 premières réplications de chaque cas. Égalité `Decimal` exacte (`==`) de P̂₀, P̂₁ et P̂_more contre `r1.poisson_binomial(phats)`, de la garde contre `r1.gate_value`, de la valeur de garde contre `r1.insufficient_history`, et de z contre `r1.z_score(n, K, P̂_more)` quand la garde est tenue.
  - r1 est importé depuis `git -C F:/Shogen archive f5b8269 s2-harness | tar -x -C F:/tmp/shogen-lots/SIM-NIVEAU/oracle-r1-f5b8269/`, avec `python -B`. Jamais depuis `F:\Shogen`, où l'import écrirait `__pycache__`.
  - Sortie : enregistrement JSON (commit, blob de `r1.py`, comptes d'égalités) ; sortie ≠ 0 au premier écart.
- **(5) Générateur contre la théorie**, par cas : moyenne sur R de K/n contre P_more(p) exact ; moyenne sur R de p̄ = Σ_i e_i/(11n) contre p. L'écart est exprimé en erreurs-types empiriques (écart-type sur R divisé par √R) et imprimé ; |écart| > 5 SE fait sortir le script en ≠ 0. Si le générateur suit le §2, la probabilité de fausse alarme sur les 16 contrôles est de l'ordre de 10⁻⁵ (P(|N(0,1)| > 5) = 5,7·10⁻⁷ par contrôle).
  - Motif : sous stationnarité, E[I_t] = P_more(p) exactement. Cet oracle attrape un état initial ou une transition fausse, un a et un b inversés, ou un K mal compté.

**Mutants de programme à faire tuer au G2** (registre ADR-0011) :

| # | mutant | oracle qui le tue |
|---|---|---|
| 1 | poids de Bartlett 1 − k/ℓ → 1 − (k+1)/ℓ (dans une seule forme) | (2b) |
| 2 | centrage sur P̂_more au lieu de Ī (une forme) | (2b), (4) |
| 3 | lag 0 compté deux fois (W_0 = 2ℓ) | (2b) |
| 4 | a et b inversés | (5) |
| 5 | K = fenêtres à ≥ 1 écart | (5) |
| 6 | graine dérivée de l'indice global de la tâche au lieu de (L, n, r) | (1b) |
| 7 | plug-in en flottants | (4a) |
| 8 | p̂_i = e_i/(n−1), ou P̂₁ sans le facteur Π_{j≠i}(1 − p̂_j) | (4a) |
| 9 | L = 1 codé en chaîne avec ρ = −p/(1−p) | aucun oracle : mutant de spécification, à tuer par relecture contre §2 (déclaré) |
| 10 | « ≥ 2,33 » → « > 2,33 » | aucun oracle : mutant équivalent en probabilité (égalité exacte à 2,33 de mesure nulle), déclaré |

Non inscrit : le sens de la garde (« non tenue ⇔ < 10 » contre « ≤ 10 ») n'est distingué par aucune donnée de ce lot, car la garde vaut ≫ 10 à p = 0,02 ; il est tenu par la relecture au G2 de la réplique ligne à ligne de `insufficient_history` (r1.py l.226-228). Le G2 ajoute tout mutant qu'il juge utile ; un mutant survivant non déclaré ici est un constat.

## 9. Tuyaux (règle Branchement)

- **Entrée** : les constantes de ce G0 (p, L, n, R, GRAINE et sa dérivation, ℓ, seuils), codées dans `scripts/sim/sim_niveau.py` au commit C.
- **Sortie** : `sim_niveau.json` et `sim_niveau.txt`, avec leurs sha256.
- **État** : fichiers versés au paquet ; sha écrits au JOURNAL par l'orchestrateur, avec C et le sha du script.
- **Consommateurs** : (a) le texte scellé, §1 bis.1 pt 7 (niveau), qui renvoie à cette sortie ; (b) le cp-1 du lot PAQUET, qui la lit ; (c) le lecteur tiers du paquet, qui rejoue le script au commit C.
- **Tests de composition** :
  - oracle (1) : le rejeu depuis le blob commis redonne les mêmes sha ;
  - la sortie versée entre sous le sha du paquet (`PAQUET.sha256`), que la garde (1) de D.4 b contrôle au RENDU-1 ;
  - oracle (4a) aujourd'hui, et (4) après B-DEP-1 : la réplique du script et r1 concordent.
- **Tuyau conditionnel déclaré** : l'oracle (4) attend B-DEP-1 (item ORACLE4-1). Ce n'est pas un tuyau absent : son déclencheur est écrit.

## 10. Limites déclarées et items formés (règle Dettes, règle PAROXYSME)

| item | limite | construction qui la lève | prix | déclencheur | garde d'aveuglement |
|---|---|---|---|---|---|
| **SHOGEN-SIM-NIVEAU-ORACLE4-1** | l'oracle (4) de l'annexe A n'est pas exécutable à `f5b8269` (`block_long_run_variance` absente) | appel de `r1.block_long_run_variance` dans l'adaptateur, critère du §8 (4) | ≈ 15 lignes dans `sim_niveau_oracle_r1.py` ; une exécution de moins d'une minute | commit de B-DEP-1 (ordre §1 bis.10, avant le scellement). Au repli §1 bis.3, l'oracle s'exécute quand z_bloc est calculée après, étiquetée « ajoutée après le pré-enregistrement » | synthétique seul |
| **SHOGEN-SIM-NIVEAU-P-1** | niveau mesuré au seul p = 0,02 ; le plug-in est moins conservateur aux p plus petits, et la garde y cède au cas le plus persistant (§3) | même script, `--p` sur la grille fixée ici à l'aveugle : p ∈ {0,0043196 (échelle de doc 10 §9 pt 5), 0,005, 0,01, 0,05}, mêmes L, n, R et GRAINE. Couvre le niveau à la borne de la garde (approximation normale unilatérale et asymétrie binomiale ; remarque de la RECONCILIATION §5 (i), pré-enregistrée par doc 10 §5.4) | 0 ligne de plus (`--p` est prévu au §7) ; ≈ 21 h de CPU, ≈ 1,8 h sur 12 processus [inféré, même base que §7] | après le G7 de SIM-NIVEAU-a ; avant le cp-1 de PAQUET si le calendrier le permet, sinon après l'exécution unique. C-6 s'applique : ne modifie ni ℓ, ni le seuil, ni la règle | grille fixée ici ; jamais un taux de source ; sortie étiquetée « exploratoire, hors G0 principal » |
| **SHOGEN-SIM-NIVEAU-MODELES-1** | le modèle nul simulé est homogène (même p et même L pour les 11 flux), sur grille complète, à durées d'écart géométriques ; le réel a des fenêtres absentes (D.5 : sautées, pertes) et des flux hétérogènes | trois extensions synthétiques : (a) fenêtres absentes (processus de trous indépendant des écarts, à paramètres fixés au G0 de l'item) ; (b) hétérogénéité (p_i, L_i) sur motifs fixés à l'aveugle (par exemple une moitié des flux à p/2 et l'autre à 2p) ; (c) durées d'écart à queue lourde. La dépendance de portée ≥ ℓ reste l'objet de SHOGEN-DEP-FENETRES-2 (existant, §1 bis.1 pt 9) | ≈ 40 lignes [inféré] et une exécution par extension | après le G7 de SIM-NIVEAU ; avant le scellement si le calendrier le permet ; C-6 s'applique | paramètres de conception seuls ; tout motif calqué sur des taux de source réels attend l'exécution unique et s'étiquette « ajouté après le pré-enregistrement » |

- Aucun de ces items ne demande de procurement : ce sont des constructions synthétiques, sans source nouvelle.
- **Non-limite, pour mémoire** : la documentation Python s'engage par écrit sur la stabilité de `random()` d'une version à l'autre (citation [lu] au §4) ; la version est écrite au `.log.txt`.

## 11. Risque résiduel (revue de sprint)

- **Spécification mal lue** (MAST FM-1.1) : L = 1 est défini au §2 (iid) contre la formule ρ ; mutant 9 à tuer par relecture.
- **Non-déterminisme caché** : flux par (L, n, r), agrégation ordonnée, `fsum`, aucune horloge dans les sorties ; oracles (1) et (1b).
- **Réplique qui diverge de r1** : oracle (4a), dès le G1.
- **B-DEP-1 code un autre estimateur** que la forme en lags de §1 bis.1 pt 3 : oracle (4), qui fait apparaître l'écart ; ce G0 ne tranche pas pour B-DEP-1.
- **Choix de p influencé par une lecture** : exposition déclarée (§0, §3), motif écrit, grille de l'item P-1 fixée ici.
- **Lecture de la sortie comme un verdict** : C-6 recopiée dans le JSON et dans le texte. La sortie décrit un niveau sous un modèle nul synthétique ; elle n'établit rien sur les sources réelles (doc 09).

## 12. Relevé et commandes rejouables

Fichiers écrits par ce G0 (`F:\tmp\shogen-lots\SIM-NIVEAU\`) :

| fichier | sha256 | rôle |
|---|---|---|
| `g0-mesure/proto_temps.py` | `ddf3254300266609e844b74c21927ef54a707a5a696046bf04aaab902ba66827` | prototype de mesure du temps et du domaine ; aucun taux de rejet imprimé |
| `g0-mesure/proto_temps.out.txt` | `b52fae751555c65fd448d5225bbe871afcbe707c0fea5b69efae5f27e6334ab6` | exécution 1 (07:10:27Z à 07:10:37Z) |
| `g0-mesure/proto_temps.out2.txt` | `e36c3bd198f55c72be629ab9c6eb2fadb151cb97a7a55ee9e977b5d9cbba9129` | exécution 2 ; lignes du pilote identiques à l'exécution 1 (`diff` vide hors lignes de temps) |
| `g0-mesure/proto_pool.py` | `292c31e2dd7b0ac6d67c64e48ab531bd9fce55ea0084596b6d8b38592059e15c` | sonde `multiprocessing` (spawn), sortie 0 |
| `g0-mesure/calc_constantes.py` | `e0ea2f01fa416e66a3bd273c8ca40d139a39568bdfb71427b4b484cbb5801390` | constantes dérivées (P_more, a, b, ρ, ρ^240, α, SE, prix) |
| `g0-mesure/calc_constantes.out.txt` | `b26be9d900809a7f5f1ca82025eca3add0aa33c49f542a8dcad32b28a2829c4e` | sa sortie |
| `G0-lot-SIM-NIVEAU.md` | rendu hors du fichier, dans la sortie structurée du worker (un fichier ne porte pas son propre sha) | ce G0 |

Rejeu (Git Bash, aucune écriture hors de `F:\tmp`) :

```
export TMP=F:/tmp/shogen-tests-tmp TEMP=F:/tmp/shogen-tests-tmp TMPDIR=F:/tmp/shogen-tests-tmp PYTHONDONTWRITEBYTECODE=1
cd /f/tmp/shogen-lots/SIM-NIVEAU/g0-mesure
sha256sum -c <(printf '%s *%s\n' ddf3254300266609e844b74c21927ef54a707a5a696046bf04aaab902ba66827 proto_temps.py)
python -B proto_temps.py > /f/tmp/shogen-tests-tmp/rejeu.out.txt   # environ 11 s ; les lignes DOMAINE et p_d sont déterministes
diff <(grep -v 'TEMPS\|debut\|fin' proto_temps.out.txt) <(grep -v 'TEMPS\|debut\|fin' /f/tmp/shogen-tests-tmp/rejeu.out.txt)
python -B calc_constantes.py | diff - calc_constantes.out.txt
python -B proto_pool.py
git -C /f/Shogen rev-parse f5b8269:docs/adr-0022/sigma-tau.json   # 472ecbbf80add87b92bbed3bcc69c4e9208f9a32
grep -rn block_long_run_variance /f/Shogen/s2-harness/ ; echo "aucune occurrence attendue a f5b8269"
```

Fin de rédaction : 2026-09-30, 07:26Z (`date -u`, relevé avant le calcul du sha256 final).
