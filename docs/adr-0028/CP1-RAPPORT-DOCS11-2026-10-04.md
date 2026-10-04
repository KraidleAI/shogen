# CP1-RAPPORT — validation fraîche du rapport S2 `11-mesures-pilotes.md`

Validateur : `shogen-validateur` (CLAUDE.md §7). Date `date -u` : 2026-10-04 03:18 UTC.

## Gate 0

Modèle sous lequel je tourne : `claude-fable-5-1` (Fable 5.1, effort high). Attendu : `claude-fable-5-1`. Conforme.

## Attestation d'exposition (ADR-0028 annexe D, D.3)

Instance neuve. Je n'ai écrit ni le code, ni le paquet, ni le rapport. Brief lu en premier
(sha256 `c76b96732fd83c571289ef557f65472c73b91934bf179aeb50e138d0c57ce0f8`, conforme).
Je n'ouvre aucune pièce interdite : `docs/15-*`, `docs/16-*`, `docs/rapports/`, `docs/adr-0025/`,
`docs/adr-0028/monark-m009a/`, `*.jsonl` ; `JOURNAL.md` seulement entrées 2026-10-03 / 2026-10-04.
`SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée. Aucune opération git en écriture.

## Fichiers ouverts (au fil de l'eau)

Pièce : `…/scratchpad/rapport/11-mesures-pilotes.md`, 1011 lignes, sha256 `4604fff312eda48916691c778b0e755186e4538486499677e7d50fea9f0f6a2a`
(égal à l'attendu du brief) ; lue en entier (l.1-1011).

| pièce | portion lue |
|---|---|
| `…/rapport/BRIEF-RAPPORT.md` (brief du rédacteur) | en entier (85 l.) |
| `…/rapport/G1-rapport.md` (journal du rédacteur) | en entier (335 l.) |
| `…/rapport/d3_lift.py`, `d3_lift.sortie.txt`, `controles_r1.sortie.txt`, `comparer_recalcul.sortie.txt`, `calc_divers.sortie.txt` | en entier ; sha256 recomptés |
| rendu J28 `…943.3-j28.out` (435 821 l.) | l.1-48 (bloc 1, clés) ; l.3657-3660 (bordure du bloc 2, 2 lignes d'en-tête seulement) ; l.435447-435540 (bloc 3) ; l.435539-435548, 435551-435552, 435563, 435606-435614, 435621-435627, 435662-435666 (bloc 4, lignes citées) ; l.435671-435821 (blocs 5, 6, [SENSIBILITÉ]). Bloc 2 jamais lu ni recopié ; `controle_horloge` comptés par grep (3 610) |
| rendu J14p `…943.1-j14-principal.out` | l.1, 31, 33, 38-39, 209555-209623 (lignes citées), 209777-209786, 209876, 209885, 209907-209909 |
| rendu J14s `…943.2-j14-second.out` | l.1, 31, 38-39, 112112-112180 (lignes citées), 112437-112454 |
| recalcul tiers `…943.4-recalcul-tiers.out` | l.2, 3, 23, 1520, 4522, 5048, 5060, 6557, 8900, 9462, 9489, 10984-10991, 13335, 13897, 13924, 14934, 15167, 15421, 17705, 18045-18049, 18099 |
| `…943.5-raw.out` | en entier (1 l.) |
| `…943.0-suite.out` | l.207, 209, 379, 621, 623 |
| `…943.json` (enregistrement) | l.1-32, l.125-142 ; clés et runs par `json.load` |
| `docs/adr-0028/PAQUET-PREREG-S2.md` | l.1-10 (dont l.8 en entier), §5 l.61-66, §7 l.81-86, §9 l.93-109, §10-§13 l.110-223 (en entier) ; §1 l.13-21 par grep |
| `docs/adr-0028/ADR-0028-decisions-sortie-S2.md` | l.18-62 (D1-D5), l.89-115 (§1 bis.1), l.145-160 (1 bis.7-8), l.195-205 (D6), l.220-262 (D9, §3, §4) |
| `docs/adr-0028/ANNEXE-D-preenregistrement.md` | en entier (211 l.) |
| `docs/adr-0028/ANNEXE-B-items.md` | titres ; B.6 l.91-129 ; B.13 l.217-227 (grep) ; B.18 l.301-311 ; B.38-B.45 l.542-664 |
| `docs/adr-0028/ANNEXE-A-lots.md` | lignes CORR, G2-P4, V, G2-P3 (l.128-131) |
| `docs/adr-0028/PLAN-PARTIE-4.md` | en entier |
| `docs/adr-0028/sceau/README.md`, `sceau/premier-2026-10-02/README.md` | en entier |
| `docs/adr-0028/AVIS-SEUIL-FLUX-QUASI-MORT.md` | l.1-40 |
| `docs/09-vocabulaire.md` | en entier (63 l.) |
| `docs/10-mesures-pilotes-design.md` | titres ; l.1-49 (§1) ; §7 l.583-594 |
| `docs/08-assumptions.md` | lignes `A(...)` par grep (l.15-42) |
| `JOURNAL.md` | **seulement** l.300-332 (entrées des 2026-10-03 et 2026-10-04), repérées par `grep -n "^> \*\*2026-10-0[34]"` |
| `CLAUDE.md` (contexte système) | fourni par l'environnement |

Non ouverts : `docs/15-*`, `docs/16-*`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, tout `*.jsonl`,
`docs/PASSATION-CLOUD.md`, le code `s2-harness/`. La copie d'arbre `arbre/` (git archive, exclusions du brief) a été lue
par `cargo xtask verify` seul ; je n'y ai ouvert aucun fichier.

## Commandes et sorties (fichiers de travail dans ce dossier)

1. `sha256sum` des 7 rendus et du `.json` : égaux aux 7 valeurs de la table du rapport l.81-87 et au JOURNAL l.314.
2. `grep -n '^\[BLOC\|^\[SENS\|^\[ÉTIQ'` sur J28/J14p/J14s : repères égaux à ceux du rapport et du G1 (J28 : 1, 6, 3659,
   435447, 435539, 435671, 435778, 435799).
3. `check_decimals.py` (ce dossier) : chaque valeur `Decimal` entre accents graves du rapport (≥ 8 chiffres) est
   recherchée **à la ligne citée** du rendu désigné : **80 valeurs contrôlées, 80 trouvées à la ligne citée, 0 écart** ;
   4 valeurs sans numéro de ligne sur leur propre ligne (l.478, 479, 485, 611) retrouvées par recherche globale aux
   lignes J28 435497, 435501, 435494, 435509, qui sont bien celles citées dans le voisinage.
4. `check_verbatim.py` : blocs recopiés comparés ligne à ligne aux rendus : pt 8 (rap. l.267-274 ↔ J28 435515-435522),
   bloc 6 (l.334-352 ↔ 435779-435797), Bonferroni (l.295 ↔ 435503), HOST-DEGRADED-1 (l.445-447 ↔ 435531-435533),
   étiquettes J14p/J14s (l.544 ↔ J14p l.1 ; l.584 ↔ J14s l.1), règle J14p (l.564-568 ↔ 209619-209623), raison RT
   (l.650 ↔ RT 18046), RAW (l.776 ↔ RAW l.1) : **tous IDENTIQUES**. Phrase scellée de discordance : 2 occurrences dans le
   rapport, 2 dans le J28, identiques. Étiquette RT l.13924 présente mot pour mot (l.640).
5. `d3_lift.copie.py` (copie de `d3_lift.py`, sha256 `8f91474c…9381` égal) rejoué sur le J28 : `--mutant` → « ÉCHEC —
   identité fausse sur [2 1 1 6] », sortie 1 ; normal → sortie 0, **sortie identique octet pour octet** à
   `d3_lift.sortie.txt` (sha256 `77ae69ec…c73f`) : 110 tables, identité exacte 110/110, écart max 2,38·10⁻⁵⁰.
6. `lift_main.py` : trois lifts à la main (fractions) depuis les quatre comptes imprimés :
   calme binance×bitstamp [52 320 423 23790] (l.435547) → lift 21307/2945 ≈ 7,2349745331 ; stress bitstamp×gemini
   [3 36 18 11340] (l.435627) → 3799/91 ≈ 41,7472527473 ; calme binance×gemini [20 352 48 24165] (l.435552) →
   40975/2108 ≈ 19,4378557875 ; identité φ² = (lift−1)²·p_A p_B/((1−p_A)(1−p_B)) exacte dans les trois cas ; φ recalculé
   égal à φ imprimé jusqu'au 50ᵉ chiffre. Égaux à la table du rapport l.514-519.
7. Gates : `git archive HEAD | tar -x -C arbre --exclude=docs/rapports --exclude=docs/adr-0025
   --exclude=docs/adr-0028/monark-m009a` (tête `25406c8`, branche `partie-4-execution` ; les trois chemins exclus absents
   de la copie, contrôlé par `test -e`), rapport copié en `arbre/docs/11-mesures-pilotes.md` (sha256 identique), puis
   `cargo --locked xtask verify` : **code de sortie 0, VERDICT GLOBAL VERT, 0 ligne `VIOLATION`** ; S-G1 à S-G8, fmt,
   no_std, clippy tous VERTS (sortie `verify-cp1.out`). Sans `--exclude=biblio`, le rouge « biblio/INDEX.md illisible »
   de l'essai A du rédacteur n'apparaît pas.
8. Sceau (lecture seule) : `sha256sum` paquet `4d2a8276…f528`, manifeste `51942351…a3e9`, jeton `9edb19b5…6b0e`, premier
   manifeste `680a95fd…4209`, premier jeton `5f5ce535…0ee8` : égaux au rapport §8.1 et aux README. `openssl ts -reply
   -text` : série `0x08CFC8D5`, `Oct  3 01:04:10 2026 GMT` ; premier jeton `0x08CC76D7`, `Oct  2 17:44:30 2026 GMT`.
9. Gardes rejouées (lecture seule) : `git show 27b0e30:JOURNAL.md | grep -o <sha paquet>` → l.304 ; `git diff --quiet
   f35a70c 27b0e30 -- s2-harness/shogen_s2 s2-harness/tools` → 0 ; idem contre HEAD `25406c8` → 0 ; `git merge-base
   --is-ancestor f35a70c 27b0e30` → 0 ; sha256 de `rendu_unique.py` à `f35a70c` = `06d189cf…9050` (= bloc machine).
10. sha256 des scripts et sorties du rédacteur : les 8 valeurs de la table §8.9 (l.800-803) recomptées égales.
11. `grep` de registre sur le rapport (`garanti|prouv|sûr|robuste|vérifié`) : 0 occurrence fautive ; « établit » n'apparaît
    que nié ou pour l'égalité de chaînes de l'oracle (§8.6) ; aucun `TODO|FIXME`.
12. Contrôles ponctuels sur les rendus : `run maximal ≥ ℓ` : 1 seule ligne dans le J28 (l.1) ; φ négatifs bloc 4 : 0 en
    calme, 5 en stress ; `DIVERGENCE` : 0 dans J14p/J14s/J28/RT/RAW, 1 dans SUITE (l.379) ; J14p l.209777-209786 : les
    10 relevés en `resolve_failed` ; `controle_horloge` : 3 610 ; bloc 5 (c) : 5 entrées `basis:doc`, dont 3 arêtes « → ».

## Constats numérotés

**Contrôle 1 — exactitude des chiffres.** Sections 3 et 4 : les 32 valeurs complètes de la table §3.1, la table §3.5
(11 flux × 2 strates × 5 comptes), les énoncés pt 8, la ligne de Bonferroni, la tête de certificat recopiée, k_eff/k nominal,
drapeaux, partition, dates : toutes égales aux lignes citées (constats 3, 4, 12). Échantillon hors sections 3-4, bien
au-delà de 40 valeurs : §2 (segment l.31, exclusion l.33-36, sautées l.37-41, retraits l.42-45, 9 USD/2 USDT l.46,
démarrages l.26, calendrier l.27, 38 600 l.28, couverture des week-ends l.435814-435818 — tous égaux ; identités [calc]
46 468 − 38 600 − 73 = 7 795 = 5 701 + 2 094 refaites) ; §5 (τ observé l.435526-435530, décomposition de K, censure
l.435536-435537, runs, cv — 24 valeurs égales) ; §7 (J14p, J14s, poolée, sensibilité, L&M, RT — 36 valeurs égales ; z_pool
recompté 33,4353667803) ; §8 (sha256, genTime, séries, durée 22 min 20 s, 398/62,358 s, 436 fichiers, tailles — égaux).
**Aucun écart trouvé.**

**Contrôle 2 — énoncés scellés.** Phrases du pt 8 recopiées mot pour mot (deux fois, l.269 et l.272, plus l.33-35 en
texte courant, identiques à J28 l.435517/435520). Étiquettes des sorties hors décision recopiées (J14p l.1, J14s l.1,
RT l.13924, J28 l.435800-435802, l.435505, l.435539 et l.435544-435546). « R1 discrimine » : « aucune strate ne rejette ;
strate(s) testée(s) : calme, stress » (l.286 ↔ 435522). Aucune p-valeur (les queues des J14 ne sont pas recopiées,
l.98-100, l.673-677). Aucun énoncé de cause ; la discordance est partout rapportée comme « NE REJETTE PAS (discordance) »
avec la phrase scellée ; §3.2 l.277-282 et §9.3 pt 1 n'en font ni un rejet ni un non-rejet net. Conforme.

**Contrôle 3 — lift de D3.** Rejoué (constats 5, 6) ; « proxy bruité » présent l.494 et l.524, recopié du paquet §5 l.63.
Conforme.

**Contrôle 4 — complétude.** Items 1 à 12 du brief du rédacteur tous présents (§1 à §12, dans l'ordre). Plan de la
partie 4, étape R : verdict, énoncés pt 8, limites §12 (les 20 points, une ligne chacun, §9.2), déviations (D.1 n° 16 §10.1,
premier sceau §10.3, MONARK-S2-M009A §10.2 avec l'attestation D.3 (i) « non » exacte, B.45 §10.4), analyses ajoutées
(§11 : 8 items, FLUX-QUASI-MORT-1 avec le seuil « 2·ok(f, s) < n_s » de l'avis, contrainte QUASI-MORT-PREDICAT-1 ; aucune
calculée). Déviations exactes contre annexe D l.28, paquet l.8 (v) et B.38 : dates, classe « R présumée », « nature exacte
du taux non établie sans lecture », lecteurs, « lève la limite écrite à la section 8 » — tous conformes aux sources.
Conforme.

**Contrôle 5 — registre et neutralité.** Aucun terme interdit de doc 09 (constat 11). Chaque énoncé sur sources réelles
porte l'instrument (l.41, l.102, l.221-222, l.566, §9.3 pt 5). D6 (vi) et D9 recopiés de l'ADR l.200, l.230, l.232 avec
l'erratum, et le pt 11 du paquet l.133 ; aucune recommandation ; les décisions du JOURNAL l.322 et l.324 rapportées comme
telles, verbatim. Conforme.

**Contrôle 6 — publication.** Liste ci-dessous ; rien corrigé.

**Contrôle 7 — gates.** Sortie 0, VERT, 0 `VIOLATION` (constat 7).

**Observations (sans correction exigée).**
- O-1 (l.44) : « Un résultat négatif est un résultat (doc 10 §7) » suit immédiatement le NE REJETTE PAS de discordance ;
  le rattachement à doc 10 §7 (critère de sortie, FAUX) est juste et la phrase l.40-44 reste prudente ; signalé parce que
  le pt 8 du paquet réserve cette locution au cas « hors discordance ».
- O-2 (§1) : résumé plus long qu'une demi-page (recopies de D6 (vi), D9, pt 11) ; déclaré par le rédacteur (G1, écart 6) ;
  fidélité préférée à la concision, acceptable.
- O-3 (l.3-4, l.712, l.737) : le rapport nomme le modèle du rédacteur et de l'exécutant (`claude-opus-5-5`) ; exact (G1,
  ENR l.2) ; relève de la liste « publication ».

## Corrections (liste fermée)

| n° | ligne | texte actuel | texte proposé | motif |
|---|---|---|---|---|
| C-1 | l.383 | « **(c) Axe méthode** (l.435754-435764) : cinq arêtes `basis:doc`, qui déclenchent (b) et ne partitionnent pas. » | « **(c) Axe méthode** (l.435754-435764) : cinq entrées `basis:doc` (trois arêtes d'amont : binance → coingecko, coinbase → pyth, coingecko → defillama ; deux déclarations d'estimateur : coingecko, pyth), qui déclenchent (b) et ne partitionnent pas. » | J28 l.435755-435764 : 5 entrées, dont 3 seulement sont des arêtes « → » ; le bloc 6 (l.435786-435788) n'en nomme que trois, ce qu'un lecteur rapprocherait de « cinq arêtes » |

Aucune autre correction. Classe : C (sans effet sur une valeur ni sur une lecture de la règle).

## Liste « publication » (à décider par l'investisseur ; non corrigé)

1. l.5 : mention « **Non publié** » dans le statut — à réécrire si publication.
2. l.3-4, l.712, l.737, l.3 : identifiants de modèles (`claude-opus-5-5`), fiche `shogen-worker` — provenance interne.
3. l.211 : chemin local Windows `F:\shogen-campagne\sigma-tau.json` (recopié du rendu J28 l.7).
4. l.212 : code d'erreur hôte `WinError 10013` (J14p l.209885) — révèle l'OS de l'hôte de collecte.
5. l.213-214, l.885 : « le poste de l'investisseur » et le verbatim « cette fois on le fait sur un VPS, pas sur mon PC »
   (JOURNAL l.324) — propos privé de l'investisseur et information sur son matériel.
6. l.914-915 : dépôt privé `KraidleAI/monark-governance`, commit `aa04924`, item MONARK-S2-M009A-EXPOSITION-1, « lots M009 »
   (l.932) — gouvernance interne d'un autre dépôt.
7. l.933-934 : identifiants de session `90684fb2`, `carto:monark`.
8. l.1008 : dépôt privé `KraidleAI/shogen` nommé.
9. l.729 : « Téléchargés de Drive » — lieu de stockage des journaux.
10. l.68-72, l.972-974 : décisions d'affaires de l'investisseur (arrêt de la collecte, S2-bis, « Position d'abord », options
    « (Recommandé) ») recopiées du JOURNAL — à décider si elles sortent telles quelles.
11. Renvois `JOURNAL l.304/306/310/312/314/322/324` et `paquet l.8/215-220`, `ADR l.25/60`, annexes A/B/D : pièces du dépôt
    privé, non suivables par un lecteur extérieur tant que le dépôt n'est pas publié.
12. Tiers nommés avec constats : Pyth (« HTTP 401 dès le premier jour », l.410, l.892), Cloudflare/AS13335 (7 hôtes sur 10),
    Incapsula, Amazon ; hôtes (`ethereum-rpc.publicnode.com`, `www.okx.com`…) — ADR §4 pt 4 prévoit un préavis privé à des
    acteurs nommés avant publication.
13. Nom et détails des gardes/outils internes (`rendu_unique.py`, `oracle_record.py`, `verify.sh`, `SHOGEN_RENDU_PRODUCTION`)
    — publiables seulement si le dépôt le devient (§12 dit déjà ce qui n'est pas public).
14. Aucune matière Pocket (docs 15/16), aucun chemin `/tmp`, aucun `*.jsonl` recopié, aucune adresse IP : rien à retirer
    sur ces points.

## Verdict

**ACCEPTE-AVEC-CORRECTIONS** — une seule correction, C-1 (l.383), de classe C ; aucune valeur, aucun énoncé scellé, aucune
lecture de la règle à changer. Pas d'ESCALADE-INVESTISSEUR : le rapport ne tranche aucune décision de valeur ; la seule
décision qui reste est la publication, déjà réservée à l'investisseur par le rapport lui-même (l.5, l.65-66, l.70), avec la
liste « publication » ci-dessus comme matière.

Fermeture : `date -u` → voir ci-dessous.
Sun Oct  4 03:29:22 UTC 2026
