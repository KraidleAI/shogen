# cp-2 de clôture de S2 — rapport du validateur frais (lot CP2-G7, ADR-0028 D6 (ii), D9 voie A)

Validateur : `shogen-validateur`. **Gate 0 : modèle résolu `claude-fable-5-1`** (identifiant exact fourni par
l'environnement de la session ; effort `high` demandé, non observable de l'intérieur). Brief :
`scratchpad/cp2-g7/BRIEF-CP2-S2.md`, sha256 recalculé `aee4373f612c2274e6e53dbbfc43865a575badac112fc916f260ec9f43247672`
(égal à celui donné). `date -u` au départ : 2026-10-04 09:23:49 UTC ; à la rédaction : 09:29 UTC. Dépôt `/home/user/shogen`,
branche `partie-4-execution`, tête `5cc0d0488ceb97693143a91ab47f3da21a3ca64a` (2026-10-04 09:23:21 UTC ; `git status --short`
vide au départ et à la fin). Le dossier G7 versé (`docs/adr-0028/DOSSIER-G7-S2.md`, sha256 `a623d685…fffcd`) est identique à
l'octet à la copie du scratchpad.

Je n'ai validé ni écrit aucune pièce de S2. Ordre suivi : celui du brief (cp-2, puis G7 de l'orchestrateur, puis clôture).

## 0. Attestation (annexe D.3) et écritures

- **Pièces non ouvertes** : aucune pièce de la liste fermée D.2 (points 1 à 12, liste lue à l'annexe D l.32-47 sans en ouvrir le
  contenu) ; rien sous `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`,
  `docs/adr-0028/monark-m009a/` ; aucun `*.jsonl` ; aucun journal de campagne ; `cargo xtask verify` non lancé. Je n'ai
  calculé aucune statistique de campagne.
- **Expositions déclarées** (toutes postérieures à l'exécution, déjà versées au dépôt) : `docs/11-mesures-pilotes.md` §1, §3.3,
  §8.4, §8.7, §9.2 (l.828-832), §11, §12 (valeurs publiées du J28 : n, z_s, z_bloc,s, EMD_s, k_eff) ; lignes de verdict du rendu J28
  (`…943.3-j28.out` l.6, 3659, 435447, 435522, 435539, 435671, 435778, 435796-435799) ; sortie `…943.5-raw.out` entière (verdict
  `raw`, cinq horodatages et deux noms de flux) ; JOURNAL l.304, 306, 314 (coupées à 400-700 caractères : sha, genTime, heures) et
  l.318-376 (entrées du 2026-10-04) ; `PAQUET-PREREG-S2.md` l.76-135 et l.205-223 ; annexe B.54 ; `ETAT-REGISTRE-2026-10-04.md`
  l.1-25 ; sorties `g3-*.out`, `deny*.txt` du scratchpad de l'orchestrateur (lignes de résumé). Le contrôle FM-1.1 de ma transcription
  est un acte de l'orchestrateur.
- **Écritures** : ce fichier ; `cp2/depot/` (clone local du dépôt, `git clone --no-hardlinks`, puis `checkout f35a70c`, lecture
  seule sur l'original) ; `cp2/f35a70c/` (`git archive` extrait, lecture) ; mon enregistrement cp-2 et sa sortie (§1). **Écart
  déclaré** : le premier lancement de `oracle_record.py` (écriture) a utilisé le répertoire temporaire par défaut du système
  pour son extraction (`mkdtemp`), supprimé par l'outil lui-même (`ls /tmp | grep oracle_` : 0) ; les lancements suivants ont
  posé `TMPDIR` dans `cp2/`. Aucune opération git en écriture sur `/home/user/shogen` ; aucun fichier suivi modifié ;
  `PYTHONDONTWRITEBYTECODE=1` et `-B` partout ; `SHOGEN_S2_CAMPAGNE_CONTROL` retirée (`env -u`).

## 1. Contrôle 1 — mon enregistrement de rôle cp-2 (D6 (viii))

Commande (09:25:05 UTC, fin 09:26:14 UTC), sur ma copie `cp2/depot` à `f35a70c` :
`env -u SHOGEN_S2_CAMPAGNE_CONTROL PYTHONDONTWRITEBYTECODE=1 python3 -B s2-harness/tools/oracle_record.py --role cp-2 --commit
f35a70c19ba8269f1f7e2bcd31775e4fc513da20 --auteur claude-fable-5-1 --depot cp2/depot --sortie cp2`. `oracle_record.py` de la
tête est identique à celui de `f35a70c` (`git diff --quiet` vrai).

| contrôle | constaté |
|---|---|
| exit de la commande | **0** |
| fichier | `cp2/shogen-f35a70c-cp-2-20261004T092505Z-31092.json`, sha256 **`4baac09ba3d7aa6f678a21390fd23fb7b6ad15dd2b6619c76fcbbdc75b20597d`** |
| sortie du run | `cp2/shogen-f35a70c-cp-2-20261004T092505Z-31092.0-suite.out`, sha256 `efe6e02dc690bd52f10b4b75c09a07c1dd2a191499f7f779d433423fba120cd9` |
| `role`, `auteur`, `schema` | `cp-2`, `claude-fable-5-1`, `shogen.oracle-record.v1` |
| `tree.commit` | `f35a70c19ba8269f1f7e2bcd31775e4fc513da20` (gel jugé, B.54 pt 2) ; 417 fichiers hachés |
| `static_only` / `served_from` / `exit` | `false` / `null` / 0 ; `paquet.sha256` et `sceau.genTime` nuls (hors rôle rendu) |
| `env.SHOGEN_S2_CAMPAGNE_CONTROL` | `null` (non posée) ; `tests_avec_variable` vide |
| suite | `Ran 398 tests in 66.460s`, `OK (skipped=2)` ; deux sauts nomment la variable (l.207, l.209), compte de la procédure (`PROCEDURE-EXECUTION.md`, ajout K-1 : 398, skipped=2) |
| Python | 3.11.15 (celui de l'exécution, ENR l.14) |
| `--verifier` sur mon enregistrement, avec `--depot cp2/depot` | « conforme … tree.sha256 recalculé », **exit 0** |

**Enregistrement de G2 contrôlé** (D6 (viii) l.207 : « le cp-2 contrôle celui que cite le G2 ») : aucune relecture G2 au dépôt ne
cite d'enregistrement de rôle G2 (recherche des noms `shogen-<sha>-G2-…json` : 0 ; dossier G7 §2, réserve G2 (3) ; item
SHOGEN-G2-ENREG-ROLE-1, B.54). Le contrôle n'a pas d'objet. J'ai contrôlé à sa place l'enregistrement de rôle « rendu » du gel
(§2), seul enregistrement d'oracle cité pour `f35a70c`/`27b0e30`, et produit le mien. L'enregistrement
`execution/apres-execution/shogen-5afbdd2-cp-2-…json` de l'orchestrateur n'est pas un cp-2 (exit 1, variable posée ; dossier §4) : non
retenu.

## 2. Contrôle 2 — SHOGEN-CP2-RUNS-RENDU-1 : **CONFORME**

Commande (09:26:14 UTC) : `python3 -B s2-harness/tools/oracle_record.py --verifier
docs/adr-0028/execution/rendu-2026-10-04/shogen-27b0e30-rendu-20261004T011129Z-943.json --role rendu --commit
27b0e303f196699959bddc2607db6a1d808ce0db --depot /home/user/shogen` (`TMPDIR` dans `cp2/`) : « conforme : … tree.sha256 recalculé
sur /home/user/shogen », **exit 0**. Lecture du JSON par mes commandes :

| attendu (D.4 b l.136 ; paquet §9 « ordre des sorties » ; `oracle_record.py` l.31, l.224-226) | constaté |
|---|---|
| sha256 de l'enregistrement = JOURNAL l.314 | `355cf9bb43609c1c4b0f3ffebcd32d9d987e5e12e63277d9e4acbd467eb0fb5c` : égal |
| runs, dans l'ordre : `suite`, puis D.4 b (`j14-principal`, `j14-second`, `j28`, `recalcul-tiers`, `raw`) | **identiques, dans cet ordre, exit 0 chacun** ; `exit` global 0 |
| sha256 des six sorties | recalculés par moi : 6 sur 6 égaux (et égaux à JOURNAL l.314) |
| `tree.commit` | `27b0e303f196699959bddc2607db6a1d808ce0db` (tête gardée, JOURNAL l.314) ; 436 fichiers ; `tree.sha256` recalculé par `--depot` : 0 écart |
| `base` | `f35a70c…` ; `27b0e30` = `f35a70c` sur `shogen_s2` et `tools` (`git diff --quiet` vrai) |
| `paquet.sha256` | `4d2a8276316b1c66a08aabb15ff3b39be812978e93dafc01a4e627f20d0af528` = sha256 de `PAQUET-PREREG-S2.md` à la tête = manifeste `sceau/PAQUET.sha256` = JOURNAL l.304 |
| `sceau.genTime` | `2026-10-03T01:04:10Z` = jeton (`Time stamp: Oct 3 01:04:10 2026 GMT`, §3) = JOURNAL l.306 |
| sha256 de `rendu_unique.py` dans `tree.sha256` | `06d189cf…9050` = `sha256_script` du bloc machine (paquet l.216) |
| `static_only`, `served_from`, variable | `false`, `null`, `null` ; `tests_avec_variable` vide pour chaque run ; auteur `claude-opus-5-5` (liste blanche) |
| suite | `Ran 398 tests in 62.358s`, `OK (skipped=2)`, deux sauts nommant la variable |
| sensibilité « plage incluse » (paquet §7 : section du J28) | `[SENSIBILITÉ] PLAGE D'EXCLUSION INCLUSE … hors décision` à J28 l.435799 |

Le run `raw` sort 0 avec un verdict « refus » : voulu et écrit avant le sceau (paquet §12 pt 1 ; `docs/11` §8.7 et §9.2 pt 1).
L'item **SHOGEN-CP2-RUNS-RENDU-1 peut être fermé** sur ce contrôle.

## 3. Contrôle 3 — sceau

`bash scripts/sceau/verify.sh` (hors ligne) : manifeste → paquet `OK` ; `openssl ts -verify` contre la requête : `Verification: OK` ;
contre les octets du manifeste : `Verification: OK` ; `Time stamp: Oct 3 01:04:10 2026 GMT`, série `0x08CFC8D5`, TSA FreeTSA ;
manifeste `519423510b21ecbebda895d6e225ab0748fb0fe5a2b257a36c9301e36bfaa3e9` (= JOURNAL l.304) ; **exit 0**. Le sha du paquet scellé
(`4d2a8276…f528`) est celui de l'enregistrement « rendu » (§2). Les avertissements “is not a CA cert” sur `tsa.crt` sont attendus
(`-untrusted`).

## 4. Contrôle 4 — le dossier G7 : chaque état est-il juste ?

Sondage : au moins deux preuves par gate, relues par mes commandes.

| gate | état du dossier | sondage | avis sur l'état | la réserve bloque-t-elle la clôture de S2 ? |
|---|---|---|---|---|
| G0 | tenu | annexe A l.134 (ligne datée DETTES-B1) ; `G0-lots-DETTES.md` : ligne CP2-G7 (INSTRUMENT-S2-1, CP2-RUNS-RENDU-1) ; D6 (i)-(ii) l.186-196 | **juste** | — |
| G1 | tenu avec réserve | `G1-lot-CORR.md` sha `1849053c…ac56` et `G1-lot-DETTES-B1.md` `61c9b86d…89ef` : égaux ; `G1-lot-DETTES-A.md` : absent ; `19db9d9` ne touche que `gates.yml` et l'annexe B ; `journal-provenance.md` s'arrête au 2026-09-28 (l.30) | **juste** ; item SHOGEN-G1-JOURNAUX-MANQUANTS-1 (B.54) | **non** : les deux lots sans G1 au dépôt (CI-S2 = `gates.yml`, DETTES-A = README) ne touchent pas le code qui a produit les rendus |
| G2 | tenu avec réserve | shas de `G2-RATTRAPAGE-R-A.md`, `G2-lot-CORR.md`, `G2-lot-DETTES-B1.md` égaux ; CORR relu par une instance neuve jusqu'à `f35a70c` (l.1-12) ; `grep -il checklist` : 0 ; nom d'enregistrement G2 : 0. Nuance : R-A (l.75) et R-B (l.55, l.136) ont lu des plages de `test_r1`, `test_r2`, `test_exclusion`, `test_segment` comme appui, sans relecture à 100 % des fichiers de tests | **juste** (réserve (1) à nuancer : lecture partielle des tests, pas nulle) ; items G2-CHECKLIST-CORPUS-1, G2-ENREG-ROLE-1 (B.54) | **non** : les modules qui ont produit les rendus sont relus à 100 % (R-A, R-B à `41f087e`, CORR jusqu'à `f35a70c`), et l'oracle tiers `recompute_*` a recalculé chaque sortie (run `recalcul-tiers`, exit 0). Qualité « produit » : due |
| G3 | tenu avec réserve | JOURNAL l.374 : G3 opérant complet à `b24ff86` (xtask VERT ; verdict-suite conforme, Ran ≥ 405 ; 95/147/54 ok ; `--hors-refs` : « 0 objet(s) hors refs sur 3388 », deux comptes) ; sorties `g3-*.out` du scratchpad cohérentes ligne à ligne ; mon rejeu de la suite à `f35a70c` : 398 OK (§1) ; `G2-lot-DETTES-B2.md` l.62-70 (146/54/95, verify VERT) | **juste** ; **réserve (1) levée** par l'entrée du JOURNAL (§5) ; réserve (2) forge morte : décision de l'investisseur ; **réserve (3) SAST Python : aucun item formé en B.54** (C-2) ; (4) CI-S2-CABLAGE-1 existe | **non** ; mais le commit du G7/clôture est postérieur au rejeu (C-3) |
| G4 | non tenu en l'état des preuves | AUDIT l.17 (« Baseline métrique à poser au premier code ») et l.31-37 (séries R-15 « s.o. », « à relever au premier commit de code produit ») ; `grep churn|42010|fitness` : seul AUDIT et B.54 ; `PLANCHER = 405` (`verdict-suite-s2.py` l.18) et règle épinglée jouent un rôle de fitness sans être nommés G4 | **juste** (verdict motivé ci-dessous) ; item SHOGEN-G4-RECALCUL-METRIQUES-1 (B.54) | **non** pour la mesure ; **oui** pour l'énoncé D6 « qualité produit sous G0-G7 complets », qui ne peut pas être prononcé au G7 (C-1) |
| G5 | tenu avec réserve | motif g5 de `gates.yml` l.69 par `git grep` sur `s2-harness` et `enforcement/verdict-suite-s2.py`, à la tête et à `f35a70c` : aucune sortie ; ERRATA-ADR0028-1 re-daté par écrit (B.54 pt 3, « avant G9 ») | **juste** ; mais D8-AMONT-ERRATUM-1, PAROXYSME-REGISTRE-1, BUNDLE-CLOTURE-1 ne sont pas traités par B.54 (C-4) | **non**, si la ligne de clôture les nomme (C-4) : des items ouverts avec déclencheur écrit ne sont pas une dette nue (CLAUDE.md pt 6) |
| G6 | tenu avec réserve | README l.17 (bibliothèque standard seule) ; `LICENSE-MIT`, `LICENSE-APACHE`, doc 14 l.3-5 ; `r2.py` l.62-65 (`socket`, `urllib`, pour `collect_asn`, hors frontière) | **juste** ; item SHOGEN-G6-PIECE-RECALCUL-1 (B.54) | **non** : aucune distribution avant G9 (acte de l'investisseur) |

**Verdict motivé sur la réserve G4.** Le G4 n'est pas tenu : l'audit d'entrée exigeait la baseline R-15 et les fonctions de
fitness « au premier commit de code produit » (AUDIT l.17, l.37), et D6 fait du chemin de recalcul un code produit ; aucune
mesure n'existe au dépôt. Cette absence **ne touche pas la validité de la mesure S2** : le verdict repose sur la règle scellée
(paquet §10, sceau vérifié), le code gelé (`f35a70c`, bloc machine), l'exécution unique sous gardes (ENR conforme), l'oracle tiers
`recompute_*` qui recalcule chaque sortie, la relecture à 100 % des modules et la suite verte. Duplication, churn et ratio de
refactoring sont des contrôles de qualité du produit, pas de justesse des chiffres rendus. Donc : **la clôture de S2 (mesure
rendue, rapport validé) n'est pas bloquée** ; **l'énoncé de D6 « le chemin de recalcul est de qualité produit, sous G0-G7
complets » ne peut pas être prononcé au G7** tant que SHOGEN-G4-RECALCUL-METRIQUES-1 est ouvert. Le déclencheur posé en B.54
(« avant toute qualité “produit” du chemin, recalcul externe payant, G9 ») est le bon. Observation : la baseline peut encore être
relevée rétroactivement depuis l'historique git (`ce63fed..f35a70c`), ce qui rend l'item réalisable sans nouveau code.

Le dossier conclut correctement qu'il ne conclut pas le G7 ; ses six points du §6 sont tranchés par B.54, sauf le G3 (3) et les
trois items dus à la clôture (C-2, C-4).

## 5. Contrôle 5 — G3 au JOURNAL et SHOGEN-E1-AVIS-FRAICHEUR-1

- **JOURNAL l.374** (09:20:41 UTC) : toutes les commandes de §4.11 et des amendements (l.291, l.296-300) y sont, avec leurs résumés :
  `xtask` VERT ; `run-fixtures-verdict-suite-s2.py` 20 ok ; `verdict-suite-s2.py` conforme, `Ran ≥ 405`, `OK (skipped=2)` ;
  `model-pinning : 95 ok` et lint (6 fichiers, liste blanche à trois identifiants) ; `secrets : 147 ok`, `--tree` (613 fichiers),
  `--history` (396 commits), **`--hors-refs` avec ses deux comptes (0 sur 3388)** ; `hooks : 54 ok` ; `install-pre-commit.sh
  --verifier` conforme. Les sorties `g3-*.out` du scratchpad (horodatées 09:15-09:20 UTC) portent les mêmes lignes. Cohérent.
  Tête du rejeu : `b24ff86` ; le commit `5cc0d04` qui a suivi n'ajoute que des documents (JOURNAL, annexe B, dossier G7, un JSON de
  contrôle FM-1.1) ; le commit du G7/clôture n'existe pas encore (C-3).
- **JOURNAL l.376** : `cargo-deny` 0.20.2 (version égale à l'épingle de la CI, `compagnon.yml` l.104 : R-8 satisfait par l'épingle),
  `cargo deny fetch` (base `ef6173c`, 2026-10-03), `cargo fetch --locked` sur `fuzz` et `adapters/shogen-tlsn-verify`, puis
  `cargo deny --frozen check` sortie 0 sur les trois espaces, « advisories ok, bans ok, licenses ok, sources ok ». Les sorties
  `deny.txt`/`deny2.txt` montrent une première tentative sans `fetch` (exit 1 sur `fuzz` et `adapters`), puis le `fetch` et le vert :
  le JOURNAL décrit la séquence qui a réussi, `fetch` compris ; cohérent, aucune correction. Le vert d'avis cité ici (§ G3) est donc
  rafraîchi : la condition de l'item est remplie, sa fermeture en B.54 est juste.

## 6. Contrôle 6 — verdict de S2

- **Règle scellée appliquée** : paquet §10.2 pt 5 (NE REJETTE PAS si z_s ≥ 2,33 et z_bloc,s publiée < 2,33 : « discordance ») et pt 6
  (« R1 discrimine » FAUX si aucune strate ne REJETTE, au moins une NE REJETTE PAS, aucune en rejet non qualifiable). Le rendu J28
  imprime l.435522 : « “R1 discrimine” … = FAUX : aucune strate ne rejette ; strate(s) testée(s) : calme, stress », et l.435796-435797 le
  reprennent au bloc 6. `docs/11` §1 et §3.3 citent cette ligne mot pour mot, exposent le cas de discordance avec l'énoncé scellé du
  pt 8 et la valeur NE REJETTE PAS dans les deux strates : **le verdict publié est celui de la règle scellée appliquée aux rendus**.
- **Analyses d'après le pré-enregistrement** : `docs/11` §11 et §11.1 : chaque sortie porte « ajoutée après le pré-enregistrement,
  hors décision ; ne change pas le verdict » ; les sorties qui impriment VRAI (J14 principal, variante incluse) sont rangées hors
  décision (§1, §7). Conforme au paquet §7 et §10.2 pt 9.
- **Registre doc 09** (l.16-32) : `docs/11` écrit « n'établit pas l'indépendance des sources », « n'établit ni n'exclut une
  co-défaillance », « rien n'est dit sur la justesse d'un prix », k_eff = 4 avant k nominal = 10, « un résultat négatif est un
  résultat ». Aucun des interdits du registre (« indépendantes », « garantit », « prouve », « vrai ») n'est employé au sens interdit.
  **Rien n'est surclamé.**
- Manque mineur : SHOGEN-ASN-PARTIELLE-S2-1 (déclencheur « lot d'après pré-enregistrement, ou limite déclarée au rapport ») n'est ni
  traité par POST-PREREG ni cité dans `docs/11` (`grep` : 0) (C-7).

## 7. Ordre et gel

- **Gel jugé** : `f35a70c` (B.54 pt 2), celui des rendus ; mon enregistrement cp-2 y est. Les changements postérieurs du chemin
  (DETTES-B1) ont leurs G1/G2 propres (B.49) et ne servent à aucun rendu ; la tête diffère de `f35a70c` sur `shogen_s2`, `tools`,
  `tests` (13 fichiers, +219 −49) : cohérent avec la procédure (« tout rejeu de S2 se fait à `f35a70c` »).
- **Ordre** : D9 l.224, annexe A l.9 et l.11 disent « `docs/11` → cp-2 → G7 » ; D6 (ii) l.196 dit « G7 = orchestrateur, puis cp-2 ».
  L'orchestrateur a suivi les deux sources contre une et déclaré l'écart (B.54 pt 1) : acceptable ; l'ADR garde une contradiction
  interne (C-6).

## 8. Verdict : **ACCEPTE-AVEC-CORRECTIONS**

La mesure S2 est rendue sous le code gelé, la règle scellée et le sceau vérifié ; l'enregistrement « rendu » est conforme avec
recalcul de l'arbre ; mon enregistrement cp-2 sort 0 ; le rapport validé publie le verdict de la règle sans surclamer ; le dossier
G7 est juste dans chacun de ses états. **Aucune réserve ne bloque la clôture de S2** (mesure rendue et rapport validé). Les
corrections portent sur les textes du G7 et de la clôture, jamais sur les rendus ni sur les valeurs du rapport.

**Aucune escalade** : aucune décision de valeur, d'argent, de message public ou de droit n'est tranchée ici. Les décisions de
l'investisseur après S2 sont déjà consignées (JOURNAL l.322) ; la publication (G9) et la qualification « produit vendable » du
chemin lui restent (D6, D9) : ce rapport ne les prononce pas.

### Liste fermée de corrections (actes de l'orchestrateur, au G7 et au commit de clôture)

- **C-1 (G7, texte)** : le verdict G7 nomme le gel jugé (`f35a70c`) et dit explicitement que l'énoncé de D6 « chemin de recalcul de
  qualité produit, sous G0-G7 complets » **n'est pas prononcé** à ce G7 : G4 non tenu (SHOGEN-G4-RECALCUL-METRIQUES-1), réserves G1,
  G2 (deux), G6 disposées par leurs items de B.54 ; la clôture de S2 (mesure rendue, rapport validé) est prononcée séparément du
  statut « produit » du chemin, qui reste différé à la fermeture de ces items.
- **C-2 (G3 (3))** : former un item pour l'absence de SAST sur le code Python du chemin, ou le disposer par écrit (bibliothèque
  standard seule ; acte de qualité produit, même déclencheur que le G4) ; B.54 ne le couvre pas.
- **C-3 (G3 au commit de clôture)** : la ligne de clôture nomme le commit du rejeu G3 (`b24ff86`) et déclare que les commits qui le
  suivent jusqu'à la clôture (`5cc0d04` et le commit de clôture) ne touchent aucun code (documents, JSON de contrôle) ; sinon,
  rejouer. Dans tous les cas, `gate-secrets.sh --hors-refs` (sortie 0, deux comptes) précède le bundle de custodie
  (BUNDLE-CLOTURE-1, §4.11 amendement du 2026-10-04 08:25:38).
- **C-4 (items dus à la clôture, non traités par B.54)** : SHOGEN-D8-AMONT-ERRATUM-1 (reste « cartographie de clôture S2 à corriger ») :
  faire l'acte à la clôture ou re-dater par décision écrite ; SHOGEN-BUNDLE-CLOTURE-1 et SHOGEN-PAROXYSME-REGISTRE-1 : déclarés dus sur le
  poste local, déclenchés par le commit de clôture nommé (classe G), dans la ligne de clôture.
- **C-5 (D6 (viii))** : la ligne de clôture consigne qu'aucun enregistrement de rôle G2 n'existe pour le gel, que le cp-2 a contrôlé
  l'enregistrement « rendu » (§2) et produit le sien (`4baac09b…597d`), et renvoie à SHOGEN-G2-ENREG-ROLE-1.
- **C-6 (ADR-0028)** : ajout daté (jamais une réécriture) sous D6 (ii) l.196 : ordre retenu « cp-2 puis G7 » (D9 l.224, annexe A l.9,
  l.11), ou inscription dans la liste de SHOGEN-ERRATA-ADR0028-1.
- **C-7 (SHOGEN-ASN-PARTIELLE-S2-1)** : ajout daté d'une limite dans `docs/11` §9.3, ou re-datation de l'item par décision écrite.
- **C-8 (versement)** : verser mon enregistrement cp-2 et sa sortie à côté des rendus (par exemple
  `docs/adr-0028/execution/cp2-2026-10-04/`), sha256 au JOURNAL ; fermer SHOGEN-CP2-RUNS-RENDU-1 sur le §2 ; fermer
  SHOGEN-INSTRUMENT-S2-1 seulement après le texte du G7 de C-1.

## 9. Limites

- Doc 02 du corpus et `validateur-humain.md` : hors dépôt, non lus [abs] ; les définitions des gates sont celles du dépôt
  (AUDIT §1, ADR D6).
- Rapports G2 de la partie 1 : hors dépôt, cités de seconde main par le dossier [2nd] ; non relus.
- Je n'ai pas rejoué `xtask verify` ni les gates secrets/hooks/pinning (interdit ou hors brief) : je m'appuie sur le JOURNAL l.374 et
  les sorties du scratchpad de l'orchestrateur, relues ligne à ligne.
- Effort `high` : non observable de l'intérieur de la session.

> *Retouche de l'orchestrateur au versement (2026-10-04 09:39:39 UTC, `date -u`)* : l.89, la citation du message d'openssl passe de « » à “ ” (S-G5 : message d'un outil, non détenu au registre) ; aucun autre octet changé.
