# R-B — relecture G2 de rattrapage : `r2.py`, `lm.py`, `report.py` entiers (lacunes G-1 et G-4)

- **Mission** : brief commun `p4/BRIEF-G2-RATTRAPAGE.md` (sha256 `396dad51…22d2`) ; inventaire `p4/INVENTAIRE-G2-RECALCUL.md`
  (sha256 `2a22f47d…2303`, égal à la source citée en annexe B.40). Rattachement : ADR-0028 annexe B.40 (SHOGEN-G2-HISTO-RECALCUL-1,
  décision de l'orchestrateur : R-B = `r2.py`, `lm.py`, `report.py` entiers, sans correctif).
- **Rédaction** : 2026-10-02, de 21:29:43Z (`date -u`, début) à la clôture (heure en §9). Réviseur neuf : je n'ai écrit aucune ligne
  de ce code et aucun lot qui l'a produit.
- **Dépôt** : `/home/user/shogen`, branche `partie-4-execution`, HEAD `e586c0bf19360814a4814f00d4665e657ffb3ffa` au départ ;
  `git diff --stat 41f087e HEAD -- s2-harness` vide (code d'analyse = commit d'analyse scellé `41f087e`) ; `git status --short` vide
  au départ. HEAD est passé à `35a601e` (21:31:53Z : JOURNAL, annexe B, inventaire) puis à `5f6dcb6` (22:01:59Z : versement de
  R-C) pendant la relecture, commits de l'orchestrateur ; `git diff --stat 41f087e 5f6dcb6 -- s2-harness` vide, sha256 des trois
  fichiers inchangés : la relecture vaut pour ces trois têtes.
- **Périmètre, à HEAD** (lus en entier) : `s2-harness/shogen_s2/r2.py` (1 092 l., sha256 `27e7da73…e779`), `lm.py` (239 l.,
  `7ef17535…ac84`), `report.py` (786 l., `54e73548…a3c3`).
- **Classement** (brief) : A touche la décision ou fait échouer l'exécution ; B rendu hors décision ; C sans effet sur les sorties.

## 0. Gate 0

Modèle résolu : **`claude-opus-5-5`** (identifiant exact fourni par l'environnement de la session ; préfixe attendu des workers,
CLAUDE.md §7 : conforme). Effort : `max` selon la fiche (réglage non observable depuis l'agent).

## 1. Attestation (forme D.3), avec expositions déclarées

« Le réviseur R-B (`claude-opus-5-5`) n'a ouvert aucune pièce de la liste fermée D.2 (n° 1 à 12) ; il n'a rien lu sous
`docs/rapports/` ni sous `docs/adr-0025/` ; il n'a ouvert aucun `*.jsonl` réel ; il n'a jamais posé `SHOGEN_S2_CAMPAGNE_CONTROL`
(toutes les exécutions sous `env -u SHOGEN_S2_CAMPAGNE_CONTROL PYTHONDONTWRITEBYTECODE=1 python3 -B`) ; il n'a vu ni calculé aucun z,
K, P̂_more ni φ de campagne ; tous les journaux qu'il a lus ou produits sont des fixtures synthétiques (graine fixée) ou les fixtures
des tests. »

Expositions et écarts, déclarés :
1. **Comptes de classe M** vus dans des pièces autorisées, non recopiés ici : paquet §2, §3 et §6 et ADR-0028 D1, D2 pt 6, D4, D5 (comptes de
   lectures et de fenêtres, diagnostics `resolve_failed` dans et hors de la plage D5, comptes `clock_check` et `asn_attribution`) ;
   `tests/test_exclusion.py` l.263-299 (comptes de fenêtres par strate, comptes par type dans la plage) ; `PROCEDURE-EXECUTION.md` l.33
   (tailles en octets des trois journaux scellés). Aucun n'est un z, un K, un P̂_more ni un φ.
2. **Écritures machine sans affichage** : `git archive HEAD | tar -x` (copie d'arbre) puis `shutil.copytree` (copies des mutants) ont
   écrit les fichiers qui portent D.2 n° 5 et 6 ; aucune de leurs lignes n'a été affichée ni lue ; copies supprimées (§9).
3. **Parcours de noms sans contenu** : `find docs -maxdepth 2 -iname "*0026*" -not -path …` a lu les entrées de répertoire de
   `docs/rapports` et `docs/adr-0025` (noms seulement, filtrés à l'affichage, aucune sortie de ces dossiers) ; `du -sh` et
   `find arbre -name __pycache__` ont parcouru les mêmes dossiers de la copie (métadonnées). Écart à « exclure à la source », au sens
   strict ; à consigner par l'orchestrateur (contrôle FM-1.1). Toutes les recherches de contenu dans `docs/` ont visé des fichiers
   nommés ou porté `--exclude-dir=rapports --exclude-dir=adr-0025`.
4. Résultats **synthétiques** lus : paquet §10.3 (SIM-NIVEAU, étape S) ; sorties de mes propres fixtures (§5).

## 2. Fichiers lus (niveau [lu] sauf mention)

| pièce | lignes | motif |
|---|---|---|
| `s2-harness/shogen_s2/r2.py`, `lm.py`, `report.py` | entiers | périmètre |
| `s2-harness/shogen_s2/r1.py`, `records.py`, `window.py` | entiers | entrées du drapeau 2 et du rendu (`regle_critere`, `compute_r1`, `analysis_pools`, filtre) |
| `s2-harness/shogen_s2/collector.py` | l.63-252 | schéma de `run_params` (clés porteuses) |
| `s2-harness/shogen_s2/journal.py`, `model.py` | entiers (l.1-63, l.1-80) | schéma des lectures |
| `s2-harness/shogen_s2/sources.py` | l.60-110, l.225-402 | flux, hôtes, classes σ |
| `s2-harness/tools/rendu_unique.py` | l.25-59, l.360-505 | consommateur du périmètre (runs `--produire`, JSON du recalcul tiers) |
| `s2-harness/tools/oracle_record.py` | l.25-54 (et `grep`) | délai par commande, liste fermée |
| tests | `test_rendu_blocs` l.1-140 ; `test_sensibilite` l.47-107 ; `test_exclusion` l.70-95, l.180-212, l.255-320 ; `test_segment` l.30-70 ; `test_r2` l.280-360, l.395-452 ; `test_critere` l.367-389, l.400-445 ; `test_rendu_production` l.30-125 ; `grep` ciblés | couverture |
| `docs/adr-0028/PAQUET-PREREG-S2.md` (sha256 `494d770d…8097`) | l.1-85, l.92-222 (§8 non lu) | texte qui fait foi, §10.2 pts 1-11 |
| `docs/adr-0028/ADR-0028-decisions-sortie-S2.md` (`bc146415…d98f`) | l.18-117 | D1-D5, §1 bis.1 |
| `docs/10-mesures-pilotes-design.md` (`b306224f…9a44`) | l.202-595 | §4, §5, §6, §7 |
| `docs/adr-0028/ANNEXE-D-preenregistrement.md` | l.32-123 | D.2, D.3 |
| `docs/adr-0028/ANNEXE-B-items.md` | `grep` ciblés ; l.555-566 | items connus, B.40 |
| `docs/G1-lot-CRITERE-regle.md` (`ac77ef5d…d648`) | entier | cas fermés D-1 à D-28 (drapeau 2, blocs 3 et 6) |
| `docs/adr-0026/ADR-0026-k-eff-n-eff.md` | entier | k_eff publié avec sa partition et sa date |
| `docs/adr-0028/PROCEDURE-EXECUTION.md` | `grep` (l.4, l.33-34, l.44) | coût des runs |
| `git show ed479c5:s2-harness/shogen_s2/{collector,r2,records}.py` | `grep` des clés | clés porteuses écrites par la collecte |

## 3. Commandes et sorties (toutes en lecture sur le dépôt ; écritures dans `p4/R-B/` seulement)

- `date -u` (21:29:43Z) ; `git rev-parse HEAD` → `e586c0b…` ; `git status --short` → vide ; `git diff --stat 18cbfb6 HEAD --
  s2-harness` et `git diff --stat 41f087e HEAD -- s2-harness` → vides ; `wc -l` et `sha256sum` des trois fichiers (en-tête).
- `git archive HEAD | tar -x -C p4/R-B/arbre` ; sha256 des trois fichiers de la copie égaux à ceux du dépôt.
- **Suite de référence** sur la copie : `Ran 383 tests in 41.251s — OK (skipped=2)` ; 0 `__pycache__`.
- `git show ed479c5:…` : à la collecte, `collector.collect` écrit les neuf clés de `LOAD_BEARING_KEYS` et les neuf de
  `R2_LOAD_BEARING_KEYS` ; ces deux tuples sont identiques à HEAD (aucun refus par clé absente attendu des chemins R2).
- `gen_journal.py` (mon générateur, collecteur réel `collector.collect` + `r2.collect_asn` par chunk, comme
  `run_campaign.run_segment` ; prix synthétiques, ASN privés 64512+, Pyth toujours en HTTP 401, pannes tirées, graine 20261002) :
  - `synth-a` : 40 160 fenêtres depuis T0 = 1787770800, 466 chunks ; control 7 906 720 o, journal 140 950 977 o, raw 115 266 940 o ;
    sha256 `623e15ef…525a`, `b51e6d5c…2094`, `6cd189fb…1f04` ; 18,4 s.
  - `synth-c` (`--taille-chunk 10 --copie`) : 39 814 fenêtres, 3 982 chunks ; control 36 500 520 o, journal 139 760 218 o, raw
    114 322 606 o ; sha256 `a26df2d4…2b53`, `3491e209…1695`, `4cda78cb…d617` ; defillama recopie le prix de coingecko.
  - `small-copie`, `small-temoin` (`--fenetres 400`) : 338 fenêtres chacun.
- `bench.py` : les commandes `--produire` de l'exécution unique, lancées comme l'enregistreur (cwd `s2-harness` de la copie,
  `python3 -B tools/rendu_unique.py --produire <nom> --journaux <dossier>`, jeton de production sur un répertoire à point) : §5.
- `probe_frozenset.py`, `probe_b1_d4.py`, `mutants.py` : §4 et §6 ; sorties `probe_frozenset.out` (sha256 `3ed62b06…6e62`),
  `probe_b1_d4.out` (`dacf7e6d…f386`), `mut-res/*.json`. Scripts : `gen_journal.py` `0b30a891…6a72`, `bench.py` `da0269af…eb78`,
  `probe_frozenset.py` `14f6de26…b3d9`, `probe_b1_d4.py` `11c7dfed…1949`, `mutants.py` `68468c58…83dd`. Pour rejouer : extraire
  `git archive 41f087e` (ou HEAD) sous `p4/R-B/arbre`, puis lancer chaque script avec `arbre/s2-harness` en premier argument.

## 4. Constats

### A-1 (A ; plausibilité très faible [inféré]) — une paire « copie exacte » fait échouer le run `recalcul-tiers`, donc l'exécution unique

- **Où** : `r2.py` l.740 (`exact_copy_pairs: list[frozenset]`), l.756-757 (ajout d'un `frozenset`), l.763 (rendu dans `content`),
  l.1046-1054 et l.1080 (rendu tel quel par `compute_r2` et `recompute_r2_from_journal`). Consommateur : `rendu_unique.py`
  l.399-403 (le run `recalcul-tiers` met le retour de `r2.recompute_r2_from_journal` dans `out`) et l.409-412
  (`json.dumps(…, default=_decimal)`), `_decimal` l.363-366 (lève `TypeError` hors `Decimal`).
- **Scénario** : deux flux du pool d'analyse ont un prix identique (égalité `Decimal`) dans chacune de ≥ `content_n_min` = 300
  fenêtres communes, série non constante (`tick_identity`, l.583-589) → `content["exact_copy_pairs"] = [frozenset(…)]` →
  `json.dumps` appelle `_decimal(frozenset)` → `TypeError: frozenset hors du JSON du recalcul tiers` → le run sort ≠ 0 →
  l'enregistreur s'arrête au premier échec (`arret_premier_echec=True`) → `produire_tout` lève « run en échec » et retire le
  répertoire temporaire (`rendu_unique.py` l.426-458) : **aucune sortie**, J28 compris, bien que les trois rendus aient réussi. Le
  même journal redonne le même échec : le code étant gelé, une issue passe par un nouveau paquet (annexe B.40).
- **Preuve** (`probe_frozenset.py`, fixtures de 338 fenêtres, table des sorties remplacée par une table de fixture comme
  `tests/test_rendu_production.py`) : `[copie] exact_copy_pairs = [['coingecko', 'defillama']] ; types = ['frozenset']` ;
  `json.dumps(recompute_r2, default=rendu_unique._decimal) : TypeError : frozenset hors du JSON du recalcul tiers` ;
  `rendu_unique --produire recalcul-tiers : EXCEPTION TypeError` ; témoin sans copie : `code 0, 308095 octets, JSON relisible`.
  **À l'échelle, sur la table réelle des sorties** (`synth-c`, 39 814 fenêtres, n fixe 38 600, plage D5 ; commandes lancées comme
  par l'enregistreur) : j14-second, j14-principal et j28 sortent 0 (49,2 s, 66,0 s, 124,8 s ; bloc 5 du J28 :
  `coingecko×defillama … T=1 … {basis:doc→(b), COPIE-EXACTE→fusion}`, k_eff 7) ; **recalcul-tiers sort 1 après 441,7 s**, sortie
  standard vide, stderr `TypeError: frozenset hors du JSON du recalcul tiers` (`rendu_unique.py` l.366, appel l.412).
- **Au pire** : aucune sortie, jamais une sortie fausse ; la tentative est consignée (paquet §9, « Procédure »), puis il faut un
  nouveau paquet pour exécuter sur ces journaux.
- **Couverture** : aucun test ne fait passer une paire copie-exacte par le JSON du recalcul tiers
  (`test_recalcul_tiers_quatre_recompute_et_variante_incluse` tourne sur une fixture sans copie ; `en_json` des tests a la même
  limite que `_decimal`).
- **Plausibilité sur les journaux réels** : très faible [inféré] — il faut une égalité exacte des prix à chaque fenêtre commune
  sur ≥ 300 fenêtres (une seule différence annule la fusion) ; le seul amont déclaré qui recopie un autre flux du pool est
  defillama ← coingecko (`r2.METHOD_EDGES`, doc 10 §4.3 pt 5), lus au même instant mais par deux chemins à cadences propres. Non
  vérifiable sans lire les journaux (D.4 a). L'effet, s'il se produit, n'est pas un mauvais chiffre : c'est l'échec de
  l'exécution, sans sortie, consigné comme tentative (paquet §9, « Procédure »).

### B-1 (B ; plausible) — un relevé ASN en échec est publié comme une « divergence d'ASN », deux fois, y compris hors du pool

- **Où** : `r2.compute_partition` l.779-793 compare `(asn_ripestat, asn_cymru)` de deux relevés successifs d'un hôte sans regarder
  `status` ; `report.py` l.548-550 imprime chaque entrée « DIVERGENCE ASN (résidu 4, instantanéité) … (publiée, jamais écrasée) ».
  La boucle porte sur tous les relevés retenus, hôtes hors du pool d'analyse compris (hôte d'un flux retiré par D1 cas a).
- **Scénario** : ok(AS X) → `resolve_failed` → ok(AS X) pour un hôte : deux « divergences » `(X, X, t1) → (None, None, t2)` et
  `(None, None, t2) → (X, X, t3)`, alors qu'aucun ASN n'a changé ; même effet pour une base muette. Le résidu 4 (`RESIDUS_ASN`,
  doc 10 §4.1) vise un changement d'ASN entre deux relevés ; une panne de résolution n'en est pas un. La valeur de k_eff et le
  drapeau 2 ne lisent pas `asn_divergences` : rendu seul (bloc 5 et JSON du recalcul tiers).
- **Preuve** : `probe_b1_d4.py` (fixture à la main, 3 hôtes, un hors pool) : 4 divergences publiées, aucun ASN changé. Rendus
  synthétiques (taux d'échec de résolution tirés à 2 % hors plage, 15 % dans la plage, choix du générateur) : `synth-a` (chunks de
  40 à 130 fenêtres) : 34 lignes au J14 second, 64 au J14 principal, 160 au J28 (dont 20 pour `hermes.pyth.network`, hors du pool
  d'analyse), 238 au J28 incluse du recalcul tiers ; `synth-c` (chunks de 10 fenêtres, forme du collecteur par défaut) : 1 474 lignes
  au J28 ; **toutes** de la forme `(None, None, …)`.
- **Couverture** : le mutant M10 (divergence comparée seulement entre deux relevés ok) survit à la suite : aucun test ne fixe le
  traitement d'un relevé en échec ; les tests de divergence (`test_exclusion` l.206-208, `test_segment` l.63-65, `test_r2` l.345-353)
  posent des ASN distincts.
- **Plausibilité** : élevée — ADR-0028 D5 et le paquet §3 déclarent des `resolve_failed` hors de la plage D5 (classe M, non
  recopiée) ; le J28 en retient donc, et chaque échec isolé produit deux lignes. Le bloc 5 du J28 réel portera des « divergences
  d'ASN » qui sont des pannes de résolution [inféré].

### B-2 (B ; certain, selon la lecture du lieu de publication) — D3 : le lift et l'identité φ = (lift − 1)·√(…) ne sont pas imprimés

- **Texte** : paquet §5 (D3, recopié de l'ADR l.44-49) : « pour les paires de singletons (tables 2×2) : lift (membre gauche de l'éq.
  28 de L&M) en secondaire déclaré […] Publier l'identité φ = (lift−1)·√(p_A p_B / ((1−p_A)(1−p_B))), qui rend exacte la mention
  « proxy bruité ». Les quatre comptes par paire restent publiés » ; doc 10 §5.5 pt 4 : φ entre singletons, « un proxy bruité de
  l'éq. 28, publié avec ce caveat ».
- **Code** : `report.py` l.486-517 (bloc 4) et `lm.py` impriment φ et les quatre comptes par paire de flux ; aucun lift, aucune
  identité, aucun caveat « proxy bruité » ; pas d'étiquette singleton / intra-cluster sur les paires (`grep -i "lift\|odds"` dans
  `s2-harness/shogen_s2/` : 0 occurrence ; `grep lift` sur le rendu synthétique J28 : 0).
- **Effet** : hors décision (L&M, pt 9). Le lift reste recalculable des quatre comptes imprimés ; aucun lot de l'annexe A ni item de
  l'annexe B ne porte ce point (`grep D3` sur les deux annexes : seul l'item Fisher). Si D3 vise le rapport rédigé et non le script,
  le point devient une consigne de rédaction ; à trancher (item à former, §8).

### C-1 (C ; texte) — pt 10 : le texte scellé ne départage pas (« R1 discrimine » FAUX, k_eff non évaluable)

« éteint ⇔ FAUX, … ; non évaluable ⇔ NON ÉVALUABLE, ou k_eff non évaluable » : les deux équivalences valent ensemble dans ce cas.
Le code (`r2.py` l.964-967) contrôle k_eff d'abord et rend NON ÉVALUABLE (`probe_b1_d4.out` : `R1 discrimine = FAUX ; k_eff = None
; état = non_evaluable`), lecture D-4 du G1 de CRITERE (CV2-35), docstring l.954-955 ; le mutant MC20 de ce G1 la fixe. Ce n'est
pas un écart du code (il satisfait l'une des deux équivalences ; aucune implémentation ne satisfait les deux) mais une précédence
absente du texte scellé. Sur le J28 réel, k_eff non évaluable exige un hôte du pool sans relevé retenu ; ADR-0028 D5 déclare des
relevés après la plage pour tous les hôtes : cas non attendu [inféré].

### C-2 (C) — lacune de tests : aucune fixture du drapeau 2 ni des blocs 3 et 6 n'a d'hôte à deux flux (configuration de production)

En production, `okx_ticker` et `okx_index` partagent `www.okx.com` : k nominal du segment (hôtes) ≠ k nominal_s (flux) (D1 :
« 10 sources / 11 flux »). Les fixtures de la règle et du drapeau 2 ont un flux par hôte. Trois mutants qui confondent hôtes et
flux survivent : M03b (drapeau 2 sur un k nominal en flux : sur le J28 réel, LEVÉ deviendrait impossible), M15 (énoncé REJETTE :
k nominal_s en hôtes), M06 (« comparaison hétérogène déclarée » seulement si k nominal_s < k nominal : sur le J28 réel, 11 > 10,
l'étiquette disparaîtrait). Le code gelé est juste sur ces trois points (lecture et rendus synthétiques : `k nominal = 10`,
`k nominal_s = 11`, étiquette imprimée) ; la suite ne le protège pas. Sans effet sur les sorties du code gelé.

### C-3 (C) — lacune de tests : branche « VRAI, k_eff borne supérieure < k nominal » (ÉTEINT) non fixée

Le mutant M01 (borne supérieure ⇒ NON ÉVALUABLE même si k_eff < k nominal) survit. Le code (`r2.py` l.974-985) rend ÉTEINT, conforme
au pt 10 (borne < k nominal établit k_eff < k nominal). C'est la branche la plus probable du drapeau 2 si « R1 discrimine » est
VRAI et qu'un hôte a un dernier relevé en échec (k_eff est calculé sur le dernier relevé par hôte, `r2.py` l.782-795 ; les hôtes
d'un même AS mesuré avant la campagne, doc 10 §4.1, fusionnent) [inféré]. Sans effet sur les sorties du code gelé.

### C-4 (C) — commentaires et libellés périmés, sans effet sur les valeurs

- `r2.py` l.45-48 (docstring de module) décrit le drapeau 2 de la v0 (« levé (z ≥ 2,33 ∧ k_eff = k nominal) / éteint (z publié
  mais < 2,33 …) / non évaluable (z non publié …) ») ; la docstring de la fonction (l.950-959) et le code suivent la règle.
- `lm.py` l.33-34 (« C(12,2)=66 paires ») et l.168 (« 66 paires pour 12 ») : avec D1 (Pyth retiré), 11 flux, 55 paires.
- `report.py` l.489-490 : « N = 11 flux (pool) » quand seul le cas (a) s'applique (`cas_b` faux) : le nombre est celui du pool
  d'analyse, le libellé dit « pool ».

### Points relus sans constat (lecture [lu], preuve par test ou rendu synthétique)

- `r2.drapeau_2` : chacune des branches du pt 10 et de la lecture (a) (SHOGEN-CRITERE-PT10-CLAUSE-1) ; entrées = `regle_critere`
  sur `r1_out["strates"]` seul (poolée hors) ; R1 interne de `compute_r2` (l.1034-1040) identique à celui du bloc 3 (mêmes pool D1,
  `pool_by_strate`, `seuil_historique_valeur`, `n_min_hors_enveloppe`) ; k nominal du segment = hôtes du pool d'analyse (cas a seul).
- `compute_partition` : fusion sur ASN concordant et sur copie exacte seulement (jamais `basis:doc`) ; k_eff non évaluable sans
  relevé ou avec un hôte non sondé ; borne supérieure si hôte sondé non attribué ; dernier relevé par hôte après filtre (HS2-07).
- Bloc 3 : valeurs, cas, énoncés REJETTE / NE REJETTE PAS / discordance, EMD (√max = max√, D-11), « z_s ≤ −2,33 » (lecture D-13),
  « R1 discrimine », famille (m dynamique), drapeau « run maximal ≥ ℓ », étiquette de la poolée ; bloc 6 : ligne d'entrées, k
  nominal_s, « comparaison hétérogène déclarée » (D-16), strate poolée hors des entrées ; bloc 1 : retraits D1, k nominal par strate.
- `lm.compute_lm` : N = pool de la strate (D1 cas b), forme par paires, φ signé, identité de cohérence ; même classification que R1.
- Sérialisation JSON du recalcul tiers : hors `exact_copy_pairs`, tous les types rendus par `recompute_r2_from_journal`,
  `recompute_lm_from_journal` sont des `dict` à clés `str`, `list`, `tuple`, `int`, `float`, `bool`, `None` ou `Decimal`.

## 5. Mesures de durée sur journaux synthétiques (information pour SHOGEN-RENDU-COUT-1 ; aucune donnée réelle)

Hôte de cette session (Linux, 4 cœurs, 15 Go), commandes `--produire` lancées une à une comme par l'enregistreur (délai par
commande à l'exécution : 3 600 s, `oracle_record.DELAI_DEFAUT`).

| journaux | j14-second | j14-principal | j28 | recalcul-tiers | raw | RSS max |
|---|---|---|---|---|---|---|
| `synth-a` (40 160 fenêtres, control 7,9 Mo, journal 141 Mo) | 54,8 s, rc 0 | 62,3 s, rc 0 | 117,4 s, rc 0 | 401,7 s, rc 0 | non lancé | 1,30 Go |
| `synth-c` (39 814 fenêtres, chunk 10, control 36,5 Mo, journal 140 Mo, copie exacte) | 49,2 s, rc 0 | 66,0 s, rc 0 | 124,8 s, rc 0 | 441,7 s, **rc 1** (A-1 : `TypeError: frozenset hors du JSON du recalcul tiers`, sortie standard vide) | 12,6 s, rc 0 (lancé à part ; à l'exécution unique, jamais lancé après l'échec) | 1,47 Go |

sha256 des sorties : `out-a` j14-second `9cbcbdb8…1297`, j14-principal `e1537c83…cfbf`, j28 `64e0ac75…84c5`, recalcul-tiers
`85213d1e…85c0` ; `out-c` j14-second `4f56faed…2613`, j14-principal `390a62aa…ef62`, j28 `2b710da7…9a03`, recalcul-tiers vide
(`e3b0c442…b855`), raw `b1446e79…3fad` ; `bench-a.txt` `49de3b23…e74d`, `bench-c.txt` `9d880774…23c4`.

Lecture : à une taille de journal voisine de la campagne, la commande la plus longue reste sous le délai de 3 600 s avec une marge
d'un ordre de grandeur sur ces données ; le coût réel dépend aussi des données (queues binomiales de la co-aberrance, lignes du
bloc 2) [inféré]. Rendus synthétiques : bloc 3 complet, « R1 discrimine » FAUX, drapeau 2 ÉTEINT (k_eff 8, k nominal 10, k
nominal_s 11 par strate, « comparaison hétérogène déclarée »), [SENSIBILITÉ] complète.

## 6. Mutants (copie neuve de l'arbre par mutant, suite complète, variable retirée ; mort = code de retour ≠ 0)

| id | fichier | mutation | résultat | tests rouges |
|---|---|---|---|---|
| M00 | — | témoin | survit (OK, 383) | — |
| M01 | r2 | borne supérieure ⇒ NON ÉVALUABLE même si k_eff < k nominal | **survit** | — (C-3) |
| M02 | r2 | premier relevé par hôte au lieu du dernier | tué (2) | `test_bloc6_date_releve_retenu_apres_filtre`, `test_releve_sans_ts_compte_a_part` |
| M03 | r2 | k nominal du drapeau 2 en flux (`flux_by_host`) | tué (3 ERROR) | mort d'artefact : les trois tests passent une partition écrite à la main sans clé `flux_by_host` (`test_r2` l.442 et l.449, `test_poolee` l.218) ; rejouée en M03b |
| M03b | r2 | k nominal du drapeau 2 en flux (clusters) | **survit** | — (C-2) |
| M04 | lm | N = pool du segment au lieu du pool de la strate | tué (1) | `test_b_mort_en_stress_seul_retire_de_cette_strate_seulement` |
| M05 | lm | m² au lieu de m(m−1) | tué (5) | `test_pairwise_second_moment_hand_values`, `test_e_theta2_var_hand_values`, … |
| M06 | report | « comparaison hétérogène » seulement si k nominal_s < k nominal | **survit** | — (C-2) |
| M07 | r2 | fusion copie-exacte désactivée | tué (1) | `test_content_exact_copy_merges_hosts` |
| M08 | lm | φ sans signe | tué (1) | `test_perfect_anti_correlation_is_minus_one` |
| M09 | report | énoncé REJETTE : « ≤ » de k_eff perdu | tué (1) | `test_enonce_rejette_keff_borne` |
| M10 | r2 | divergence comparée seulement entre deux relevés ok | **survit** | — (B-1) |
| M12 | r2 | k nominal_s = k nominal du segment | tué (2) | `test_bloc6_entrees_k_nominal_heterogene`, `test_k_nominal_s_cas_b` |
| M15 | report | énoncé REJETTE : k nominal_s en hôtes | **survit** | — (C-2) |

14 exécutions (13 mutations, un témoin) : 8 tuées (dont M03 par artefact), 5 mutations survivent (M01, M03b, M06, M10, M15),
chacune rattachée à un constat. 0 `__pycache__` dans les copies ; `mut/` vide à la fin.

## 7. Plausibilité, en résumé

| constat | classe | plausible sur les journaux réels (12 flux, ≈ 40 000 fenêtres) |
|---|---|---|
| A-1 | A (échec de l'exécution) | très faible [inféré] : égalité exacte des prix sur ≥ 300 fenêtres communes |
| B-1 | B | élevée [inféré] : des `resolve_failed` hors plage sont déclarés (ADR D5) |
| B-2 | B | certaine (le rendu n'a pas la ligne), effet hors décision |
| C-1 | C (texte) | non attendue sur le J28 [inféré] |
| C-2, C-3, C-4 | C | sans effet sur les sorties du code gelé |

## 8. Limites et items à former (règle PAROXYSME)

1. **A-1** : porté à l'orchestrateur (annexe B.40 : choix de l'investisseur entre exécuter avec la limite déclarée et un nouveau
   paquet). Item proposé : SHOGEN-RECALCUL-JSON-COPIE-1 (sérialisation des paires copie-exacte dans le recalcul tiers ; test de
   composition avec une copie exacte). Propriétaire : orchestrateur ; déclencheur : avant l'exécution (décision) ; aucun correctif
   proposé ici.
2. **B-1** : SHOGEN-ASN-DIVERGENCE-ECHEC-1 (une panne de résolution n'est pas une divergence d'ASN ; hôtes hors pool) ; déclencheur :
   après l'exécution, ou limite écrite au rapport si l'exécution a lieu sur le code gelé.
3. **B-2** : SHOGEN-D3-LIFT-1 (où le lift et l'identité de D3 sont publiés : script ou rapport rédigé) ; déclencheur : avant la
   rédaction du rapport S2.
4. **C-1** : précédence D-4 non écrite au paquet ; à citer au rapport avec le drapeau 2 si le cas se présente.
5. **C-2, C-3** : SHOGEN-TESTS-HOTE-DEUX-FLUX-1 (fixture avec un hôte à deux flux pour la règle, le drapeau 2 et les blocs 3 et 6 ;
   branche VRAI + borne < k nominal) ; déclencheur : premier lot qui touche `r2.drapeau_2` ou les blocs 3 et 6.
6. **Mesure de durée** : faite sur journaux synthétiques seulement (§5) ; SHOGEN-RENDU-COUT-1 reste ouvert pour les journaux réels.
7. **Hors périmètre, non vérifié** : concordance des clés porteuses R2 sur les `run_params` du `control.jsonl` réel (les tests
   D.4 a ne contrôlent que les clés R1) ; la collecte déclarée sur un seul commit (`ed479c5`, paquet §1) la rend attendue.

## 9. Verdict et clôture

**Verdict : CONSTAT-A** (un constat A, A-1, à porter immédiatement à l'orchestrateur ; plausibilité très faible [inféré]).
Constats B : B-1, B-2. Constats C : C-1 à C-4.

Clôture : 2026-10-02 22:10:16Z (`date -u`) ; HEAD du dépôt à la clôture `5f6dcb6` (commit de l'orchestrateur, 22:01:59Z,
versement de R-C) ; `git diff --stat 41f087e 5f6dcb6 -- s2-harness` vide. Copies d'arbre supprimées (`p4/R-B/arbre`, `p4/R-B/mut/`,
répertoires de jeton vides) ; aucune écriture dans le dépôt ; aucune opération git en écriture ; `find s2-harness/shogen_s2
s2-harness/tools -name __pycache__` dans le dépôt : 0 ; `git status --short -- s2-harness` : vide. Observation, hors de mon fait :
le dépôt porte `s2-harness/tests/__pycache__/__init__.cpython-311.pyc` daté du 2026-10-02 04:36:57Z (avant cette session), hors des
chemins de la garde (2) (`shogen_s2`, `tools`), ignoré par git. Fichiers de travail conservés dans `p4/R-B/` : scripts
(`gen_journal.py`, `bench.py`, `probe_frozenset.py`, `probe_b1_d4.py`, `mutants.py`), sorties de sondes, `mut-res/`, `mut-log-*.txt`,
`bench-*.txt`, journaux synthétiques (`synth-a`, `synth-c`, `small-*`) et rendus synthétiques (`out-a/`, `out-c/`).
