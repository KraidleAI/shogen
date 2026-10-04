# Relecture G2 — lot DETTES-A (documents)

- **Gate 0** : modèle résolu `claude-opus-5-5` (fiche `shogen-worker`, réviseur neuf, rôle G2). Effort : `max` demandé par le brief, non lisible de l'intérieur de la session (déclaré, non vérifié).
- **Horloge** : `date -u` au départ `Sun Oct  4 05:36:40 UTC 2026` ; avant rédaction `Sun Oct  4 06:03:47 UTC 2026`.
- **Brief** : `…/scratchpad/dettes/G2-A/BRIEF-G2-DETTES-A.md`, sha256 recalculé `6ce0346db97c4f4449098762dd6595cd09bd1847d6bed0039a1b6a913de6406b` = annoncé.
- **Pièces relues** (sha256 recalculés, égaux à `sorties/finale/sha256-livrables.txt` du worker) :
  `DETTES-A-1-registres.diff` `740c5a8e…38df` ; `DETTES-A-2-readme-harnais.diff` `d7bcecc5…7bbd` ;
  `DETTES-A-3-fiche-worker.diff` `3895ddfd…9902` ; `fragment-amendement-ADR-0025-a-poser-par-orchestrateur.txt` `f881bab8…2937` ;
  `sondes/sonde_dettes_a.py` `91ace16d…39c7ab` ; `sondes/mutants_dettes_a.py` `abea108c…fa9b` ; `sondes/verification-finale.sh` `534601a3…c7ab` ;
  `historique/compter.sh` `5636878d…968d`. Le rapport du worker = `sorties/finale/bilan.txt` et les sondes (brief) ; aucun journal G1
  ni liste d'écarts n'est versé dans le dossier : l'« écart 5 » n'est connu que par le brief (placement des notes du JOURNAL).
- **Dépôt** : `/home/user/shogen`, branche `partie-4-execution`, tête `3e275a2` (base du worker : `5afbdd2`). Aucune opération git
  en écriture sur le dépôt. `git status --short` vide au départ ; en fin de relecture, 12 entrées apparues pendant la relecture
  (`docs/adr-0029/CONTRE-EXPERTISE-DECISIONS.md`, `docs/adr-0029/DECISIONS-ARCHITECTURE-S2BIS.md`, `docs/adr-0029/etude-marche/`,
  `scripts/controle/SHA256SUMS`, `scripts/controle/sorties-fm11/etude-*.json`) : travail parallèle, pas de ce réviseur (noms lus, contenu
  non ouvert) ; aucune ne touche les six fichiers du lot. Fichiers écrits : ce rapport et le dossier de travail `G2-A/travail/`.

## Attestation d'exposition

Je n'ai ouvert aucune pièce de `docs/15-*`, `docs/16-*`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, aucun
`*.jsonl`, aucune pièce de la liste D.2 (pts 1 à 12) ; les copies extraites par `git archive` les excluent. `SHOGEN_S2_CAMPAGNE_CONTROL`
jamais posée (`env -u`). ADR-0025 : métadonnées `git log` seules. ADR-0026 et ADR-0027 : contrôles par script (booléens et numéros de
ligne, aucun texte affiché), parce que l'ADR-0029 déclare de la matière Pocket à ADR-0026 l.3, l.8-10, l.19-21, l.36-42. JOURNAL, section
du 2026-09-27 (l.55-78, matière Pocket) : jetons seulement, jamais affichée. Exposition déclarée : le titre de cette section (`grep "^## "`)
et le sujet du commit `7bf1ad6` (affiché par `git log`), qui nomment un addendum du doc 15 et une mesure du 27/09 : lus, non repris ;
l'extrait de JOURNAL l.96 (section ADR-0028) porte la mention « docs Pocket hors GitHub ». Valeurs de S2 lues après l'exécution unique
(docs/11 §1, §2.3-2.5, §3.1, §4.1-4.2, §8.1, §10.3 ; tableau 1.1 d'ADR-0029), lecture que le contrôle (2) du brief exige.

## 0. Verdict

**ACCEPTE-AVEC-CORRECTIONS** — liste fermée **C-1 à C-6** (§2). Aucune ne change la démarche du lot ; toutes sont des corrections de
texte. Les textes corrigés ont été appliqués sur une copie et rejoués : gates vertes, ajouts seuls (§2, fin).

## 1. Contrôles du brief

**(1) Application sur la tête.** `git apply --check -v` des trois diffs sur `3e275a2` : rc 0 chacun (lecture seule). Sur une copie
`git archive 3e275a2` (exclusions ci-dessus, plus `biblio/INDEX.md`) : `git apply` rc 0 ×3 ; `diff -rq` copie vierge / patchée = exactement
les six fichiers annoncés. Entre `5afbdd2` et `3e275a2`, seuls `JOURNAL.md` (+14) et `docs/adr-0029/` ont changé parmi les fichiers
pertinents ; `s2-harness/` est inchangé depuis `f35a70c` (`git diff --stat` vide jusqu'à `5afbdd2` et jusqu'à `3e275a2`).

**(2) Exactitude contre les sources.**

- Dates d'index = commit de création (`git log --diff-filter=A --follow`) : ADR-0024 `7850bea` 2026-09-24 ; ADR-0025 `d363070` 2026-09-26 ;
  ADR-0026 et ADR-0027 `7bf1ad6` 2026-09-27 (01:29 UTC) ; ADR-0028 `ce63fed` 2026-09-29 ; ADR-0029 `7cfa0df` 2026-10-04. **Toutes exactes.**
- Intitulés : ADR-0024 = l.1 du fichier mot pour mot ; ADR-0026 et ADR-0027 : égalité de l.1 avec « `# ADR-00NN — ` + intitulé de l'index »
  (contrôle par script, normalisation des marques `*` et `` ` ``) ; ADR-0028 et ADR-0029 = l.1 ; ADR-0025 : intitulé **reconstitué** et déclaré
  comme tel (JOURNAL l.51-53, sujet de `d363070`), non vérifiable sans ouvrir le fichier (acte A-2).
- Statuts : ADR-0024 = l.3 (« vas y, configure ça », 2026-09-24 18:13 UTC) ; ADR-0025 = JOURNAL l.82 (03:00 UTC, décision 269) et l.88
  (272), dernier commit du dossier `7f8b5cc` (2026-09-29 18:25 UTC) antérieur à `ce63fed` (19:59 UTC) : exacts ; ADR-0026/0027 : jetons
  « Statut », « G0 », « proposé », « MONARK », « 2026-09-27 » présents à l.3 ; « aucun checkpoint-1 consigné » **non établi au-delà du
  fichier** (C-5) ; ADR-0028 = l.3-4 et JOURNAL (sceau en vigueur du 2026-10-03, docs/11 §8.1) : exact ; **ADR-0029 : périmé à la tête
  (C-1).**
- Note datée de DECISIONS : blocs `## ADR-` présents pour 0001 à 0022 seulement (exact) ; `0abc881` porte les errata d'ADR-0023 (+5 l.) :
  exact. Omission relevée : l'heure de la ligne d'index d'ADR-0023 (C-6).
- Feuille de route, chiffres contre `docs/11-mesures-pilotes.md` : n = 35 982 (§1 l.29 ; §2.4 l.186), 24 585 / 11 397 (§2.5 l.192), K = 154 / 133
  (§3.1 l.235), z_s 20,829… / 28,466… → « ≈ 20,8 / ≈ 28,5 », z_bloc 1,9451… / 1,7444… → « ≈ 1,95 / ≈ 1,74 » (§3.1 l.240, l.247), segment
  J28 `[2026-08-26T19:00Z ; 2026-09-28T01:28Z)` et 38 600 (§2.3), partition (un cluster de sept hôtes sur AS13335 et trois singletons ;
  k_eff = 4, k nominal = 10 hôtes ; §4.1 l.355-361), énoncé scellé mot pour mot (§1 l.33-35), « R1 discrimine » = FAUX, quatre décisions
  de l'investisseur (§1 l.68-71), genTime 2026-10-03T01:04:10Z (§8.1 l.689), branche D9 (§1 l.62) : **tous exacts.** Ligne R-S2 de l'annexe A
  (l.132) et lot CP2-G7 (G0-lots-DETTES l.26) : exacts. **Phrase S2-bis : périmée (C-1).**
- ADR-0023 : la conséquence 2 (l.39) porte « **J14 (~4 sept) / J28 (18 sept)** » ; l'erratum la cite exactement et reprend mot pour mot le
  texte prescrit par ADR-0028 D4 (« J14 = [2026-08-26T19:00Z ; 2026-09-09T19:00Z) (ADR-0028 D4) ; J28 = segment d'ADR-0028 D2 pt 6 »).
  **Exact.** Avec l'erratum d'heure du 2026-09-29 (l.5), le point 1 du §8 est posé en entier.
- JOURNAL, note REG-05 : la table passe de l.42 (2026-08-20) à l.43 (2026-09-18), aucune ligne datée entre les deux ; commits de la période
  (branche courante et `--all`, du 2026-08-21 au 2026-09-18) : exactement `36593b6`, `ed479c5`, `5b6469a`. **Exact.** Note 273 : annexe B
  l.15 (« décision 273 (CHANTIERS MONARK l.1971) ») et §4.10 (a) l.273 cités exactement ; texte verbatim de 273 absent du dépôt (`git grep`
  hors chemins interdits) ; section « 2026-09-29 (suite) — ADR-0028 » présente (l.94). **Mais 273 est nommée à l.96** (C-4) ; placement (C-3).
- README : comptes recomptés par moi (§6) : **307** `b323f03`, **376** `0cc5a92`, **383** `fdc7252`, **398** `f35a70c`, **398** `5afbdd2`,
  **398** `3e275a2`, chacun « OK (skipped=2) », sortie 0 ; sauts = `TestExclusionJournalReel.test_ii_plage_adr0025_retire_2618_fenetres` et
  `…test_ii_plage_adr0025_comptes_par_type` (`tests/test_exclusion.py`), variable absente. `37db486` = A2 (DOCS-S2-b) : exact. La liste
  des lots coïncide exactement avec `git log b323f03..f35a70c -- s2-harness/tests`. **Deux défauts : RENDU-2 rattaché à l'étape C, et
  critère de la liste non dit (C-2).** Ajout final : rendus présents dans `docs/adr-0028/execution/rendu-2026-10-04/` ; « proposée »
  exact à la tête.
- Fiche : sources des cinq consignes vérifiées une à une : G0 de D8c §5.1 h (l.122) et §15 (l.573, l.575) ; G1 de D8c §11 (l.398, 399, 402,
  413, 414), E-7 (l.334), E-9 (l.466), E-10 (l.467), l.312 (C-07, C-12) ; G0 de D8c §7.3 (C-07 l.363, C-12 l.368) ; E-1 des G1 de B0 (l.155)
  et de D8a (l.247) ; G2 de la partie 4, B-2 (l.217, l.310-313 : « défaut 30 min, maximum 2 h », premier plan 10 min) ; procédure d'exécution,
  ajout K-2 (l.79, `setsid nohup`) ; JOURNAL l.278 (partie 4, P1 : « HARNAIS-BASH-WSL-1 sans objet (hôte Linux) ») ; contrat des runners
  « Sortie : 0 tout passe, 1 un cas échoue, 3 erreur fatale » (`run-fixtures-model-pinning.sh` l.14-15, `run-fixtures-secrets.sh` l.12 ;
  `run-fixtures-hooks.sh` : `fatal` → 3, fin `[ "$KO" -eq 0 ]`). **Toutes exactes.**

**(3) Ajouts datés seulement.** Trois diffs en ajouts purs : +42 −0, +20 −0, +34 −0 (≤ 200, R-25) ; chaque ajout porte sa date (index :
colonne date + note datée ; feuille de route : en-tête et « État au 2026-10-04 » ; ADR-0023 : « Erratum daté » ; JOURNAL : « Note datée » ;
README : « 2026-10-04 — mesure » et « Ajout daté » ; fiche : titre de section daté). Aucune ligne existante retirée ni réécrite.

**(4) Fiche.** Frontmatter identique à l'octet : sha256 `579710c8d16e6e76fc7c0c82e98abf9256cdd10af4f83906190343b05ca66b77` (401 octets)
avant et après ; `model: claude-opus-5-5`, `effort: max` ; le fichier patché = le fichier d'origine suivi de 2 882 octets (ajout en fin de
corps seulement). Consignes conformes aux lignes B.16 (l.273, 274, 277, 287, 288), sources ci-dessus ; observations O-2, O-3. Sur la copie
patchée de `3e275a2` : `enforcement/lint-model-pinning.sh .` → `OK (R-1) : 6 fichier(s)`, rc 0 ; `run-fixtures-model-pinning.sh` → `95 ok,
0 échec` ; `cargo --locked xtask verify` → `=== VERDICT GLOBAL : VERT ===`, EXIT 0, 8 gates « VERT (0 violation(s)) », aucune ligne de
violation ; hook versionné (dépôt jetable de ce réviseur : copie + `git apply --index`) → `OK (hook)`, rc 0 ; `gate-secrets.sh --tree` →
`OK (secrets) : 486 fichier(s)`, rc 0.

**(5) R-13 et registre 09.** Motif du hook (`enforcement/hooks/pre-commit` l.21) sur les 96 lignes ajoutées : 0 ; recherche insensible
TODO/FIXME/XXX/TBD : 0 (le hook exclut `.claude/` : la fiche a été balayée à part, 0). Registre 09 : S-G4 verte (15 locutions mécanisées) ;
relecture complète faite contre les quatre tables et la règle d'application : aucune faute (« indépendantes » n'apparaît que dans la citation
scellée, sur des fenêtres ; k_eff en tête de k nominal ; « validé » ne qualifie que le verdict du rôle validateur, avec « cp-1 complet » et
date ; les autres touches du crible sont des faux positifs : « mesure », « livraison », « CORRECTIONS »). Octets : aucun CR, UTF-8, aucun
espace de fin ; aucune ligne ajoutée n'égale ADR-0025 l.14 ni la cartographie l.51 (sha256 comparés), aucun motif de D.2.

**(6) Notes du JOURNAL : en fin de fichier** (C-3). Motifs : (a) le JOURNAL est le registre chronologique opposable (ADR-0013) ; S-G8 en
écrit le principe (`xtask/src/sg8.rs` l.6-7 : « ordre chronologique non décroissant (une ligne insérée au mauvais endroit réordonne
l'histoire — le cas s'est produit le jour où cette gate a été écrite) ») et ne lit que les lignes de table : les notes, en citation (`>`),
n'échappent à la gate que par leur forme ; (b) tous les errata du JOURNAL sont ajoutés à la suite, à leur date : l.173 « Erratum orchestrateur
(entrée précédente) », l.201, l.258, l.274, l.296 ; aucun précédent d'insertion datée au milieu ; (c) depuis `e25d840`, les heures du JOURNAL
sont produites par le script d'écriture : une entrée de fin reçoit son heure exacte ; (d) la trouvabilité est gardée par les renvois explicites
(l.42 → l.43, l.96), qui restent valides puisque l'ajout vient après eux. La gate S-G8 reste verte avec les notes en fin (rejoué, §2).

**(7) SHOGEN-ERRATA-ADR0028-1 reste ouvert.** Après ce lot : §8 pt 1 posé en entier, pt 3 posé (avec C-3, C-4), pt 4 posé (et ADR-0029).
Restent : **pt 2** (amendement daté en tête d'ADR-0025, déc. 1) non posé, aucun commit du dossier depuis `7f8b5cc` ; texte prêt
(`fragment-…txt`, `f881bab8…`, sous-ensemble fidèle de D5 l.57-62 : extension à tous les types, bornes par type, une seule règle,
sensibilité au paquet ; comptes et motif laissés à D5 et au bloc 1), acte de l'orchestrateur avec la procédure de D.2 n° 6 ; **pt 5**
(registre PAROXYSME référencé par sha) : seulement par préfixe `a655c401…` (D.2 n° 10, `70c5004`), sha complet sur le poste local, classe G ;
**pt 6** (transmissions à l'orchestrateur MONARK) : MONARK-S2-M009A-EXPOSITION-1 fermé (B.38) ; S2-TUYAU-MONARK-1 et VITRINE-MONARK-1
sans trace (état du registre l.180 : « à confirmer »). **Limite rendue (PAROXYSME)** : la suite du §8 (§1 bis.11, « suite du §8 ») n'est pas
suivie par l'état du registre pour cet item ; les actes 7, 9, 10, 11, 12 sont posés (doc 10 l.285 ; `.gitattributes` l.67 ; `sceau/README.md`,
`verify.sh`, `paquet.tsq` ; JOURNAL l.123 ; doc 08, 3 occurrences), mais **l'acte 8** (WISHLIST P-01, P-03 : 0 occurrence de « P-0 » dans
`WISHLIST.md`, P-03 = Fisher 1921, versé depuis à `biblio/`, `c32c285` : peut-être caduc pour lui) et **les actes 13 à 16** (renvois datés
de doc 10 §5.4, §5.6, §7 et doc 04 §2 : 0 occurrence de « 1 bis » dans doc 10 et dans doc 04) **ne sont pas posés** : item à former, ou
liste restante d'ERRATA-ADR0028-1 à étendre.

## 2. Corrections (liste fermée)

**C-1 — ADR-0029 : état périmé à la tête (diff 1, deux sites).** À `3e275a2`, le cp-1 complet d'ADR-0029 v2 est rendu
(`docs/adr-0029/CP1-ADR0029.md` §6 : ACCEPTE-AVEC-CORRECTIONS, sept corrections ; commit `898ee9c` ; ADR-0029 sha256 `86f1ff23…`) et le JOURNAL
(entrée de 04:52:48 UTC, l.352) dit : « Statut : proposée, en attente de l'étude de marché (élargissement du pool, ETH, USDC, USDT) puis des
actes de l'investisseur (§6). » (décision de l'investisseur de 04:44:36 UTC, l.350). Les deux sites présentent encore le cp-1 comme une
condition à venir.

- (a) `docs/DECISIONS.md`, ligne ADR-0029, colonne statut : remplacer
  ```
  proposée (lot ADR-S2-BIS) ; ne s'applique qu'après la clôture de S2, un cp-1 du validateur et l'acte budgétaire de l'investisseur (ligne Statut du fichier)
  ```
  par
  ```
  proposée (lot ADR-S2-BIS, révision 2 ; ligne Statut du fichier) ; cp-1 complet du validateur rendu le 2026-10-04 : ACCEPTE-AVEC-CORRECTIONS, sept corrections de texte appliquées (`docs/adr-0029/CP1-ADR0029.md`, commit `898ee9c`) ; JOURNAL, entrée de 04:52:48 UTC : « Statut : proposée, en attente de l'étude de marché (élargissement du pool, ETH, USDC, USDT) puis des actes de l'investisseur (§6) » ; ne s'applique qu'après la clôture de S2
  ```
- (b) `docs/05-roadmap.md`, paragraphe « État au 2026-10-04 » : remplacer
  ```
  statut « proposée », applicable seulement après la clôture de S2, un cp-1 du validateur et
  l'acte budgétaire de l'investisseur (ligne Statut de l'ADR).
  ```
  par
  ```
  statut « proposée » ; son cp-1 complet est rendu le 2026-10-04 (ACCEPTE-AVEC-CORRECTIONS,
  sept corrections de texte appliquées ; `docs/adr-0029/CP1-ADR0029.md`) ; JOURNAL, entrée de 04:52:48 UTC :
  « Statut : proposée, en attente de l'étude de marché (élargissement du pool, ETH, USDC, USDT) puis des
  actes de l'investisseur (§6) » ; elle ne s'applique qu'après la clôture de S2.
  ```

**C-2 — README de `s2-harness` (diff 2).** (a) Le G0 de la partie 2 titre « B — RENDU-2 » (l.66) et « C — RENDU-1 » (l.106) ; plan l.24-25 :
remplacer `étape B : B0 à B6b ; étape C, RENDU-1 et RENDU-2 : C1a à C3f ;` par `étape B, RENDU-2 : B0 à B6b ; étape C, RENDU-1 : C1a à C3f ;`.
(b) La liste n'est exhaustive que pour les commits qui touchent la suite (P0, l'étape S, R, V, Sc de la partie 3 n'y sont pas) : remplacer
« `Lots commis depuis` ⏎ `  la mesure du 2026-10-02 :` » par « `Lots qui ont touché` ⏎ `` `s2-harness/tests` depuis la mesure du 2026-10-02 :`` »
(re-coupe de la ligne au choix).

**C-3 — JOURNAL : les deux notes passent en fin de fichier (diff 1 ; réponse au contrôle 6).** Retirer le bloc inséré entre l.44 et la
section « 2026-09-23 » (la zone redevient identique à l'octet à la tête) ; ajouter les deux notes après la dernière entrée existante au
moment du commit, chacune en entrée datée au format des entrées récentes (« `> **AAAA-MM-JJ HH:MM:SS UTC — Note datée (…)** : …` », heure
lue par `date -u` à l'insertion) ; dans la note REG-05, « le tableau ci-dessus » → « le tableau du début de ce journal » ; dans la note 273,
« » ci-dessous. » → « » ci-dessus. ».

**C-4 — JOURNAL, note 273 : précision (diff 1).** La décision 273 est nommée une fois au JOURNAL, l.96, comme objet du veto (« §4.10 : décisions
273, 269/272, ADR-0023, G5 au mainteneur »). Remplacer « n'a pas de ligne dans ce journal. » par « n'a pas d'entrée dans ce journal : elle n'y
est nommée qu'une fois, comme objet du veto de §4.10, à la section « 2026-09-29 (suite) — ADR-0028 » (l.96 à la tête `3e275a2`). »

**C-5 — DECISIONS, ADR-0026 et ADR-0027 : affirmation à ramener à sa preuve (diff 1, deux lignes).** La preuve citée (un seul commit,
`7bf1ad6`) n'établit que l'absence d'un checkpoint-1 dans le fichier. Le JOURNAL, section du 2026-09-27, porte des mentions de checkpoint-1
(l.57, avec ADR-0026, ADR-0027 et G0 ; l.59 ; l.61) et un « Checkpoint-1 » ACCEPTE-AVEC-CORRECTIONS (l.63, voisin de D11 et du doc 16, sans
ADR-0026/0027 nommées ; jetons seulement, section non lue). Remplacer, aux deux lignes, « aucun checkpoint-1 consigné (un seul commit du
fichier, `7bf1ad6`) » par « aucun checkpoint-1 consigné dans le fichier (un seul commit, `7bf1ad6`) » ; et l'orchestrateur, qui peut lire
cette section, vérifie avant le commit si elle consigne un checkpoint-1 d'ADR-0026 ou d'ADR-0027 : si oui, la colonne statut le dit.

**C-6 — DECISIONS, note datée : l'heure de la ligne d'ADR-0023 (diff 1).** La note met à jour le statut de la ligne d'ADR-0023, dont le titre
porte encore « HTTP 401 dès la fenêtre 1 (26/08 20:00 UTC) », heure corrigée en 19:00Z par ADR-0028 D1 et D4 et par l'erratum du 2026-09-29
(ADR-0023 l.5). Après « errata en tête de `docs/adr-0023/ADR-0023.md`, commit `0abc881`) ; », insérer « l'heure « 26/08 20:00 UTC » de sa
ligne se lit 2026-08-26T19:00Z (ADR-0028 D1 et D4 ; erratum du 2026-09-29 en tête du même fichier) ; ».

**Contre-épreuve des corrections.** Script `travail/appliquer_corrections.py` (sha256 `e1e223f6…980f` ; chaque remplacement exige une seule
occurrence) appliqué à une copie de la copie patchée (`corrige3-head`) : 8 remplacements « ok » ; `cargo --locked xtask verify` EXIT 0,
8 gates « VERT (0 violation(s)) », VERDICT GLOBAL VERT ; lint d'épinglage rc 0 ; hook rc 0 et `gate-secrets.sh --tree` 486 fichiers OK
(dépôt jetable) ; contre la tête vierge : DECISIONS +8 −0, feuille de route +30 −0, ADR-0023 +2 −0, README +20 −0, fiche +34 −0, JOURNAL +4 −0
(le JOURNAL corrigé commence par le JOURNAL de la tête à l'octet). Le script est une aide de vérification, pas un livrable à committer.

## 3. Actes de l'orchestrateur au commit (contrôles, hors texte du worker)

- **A-1** : les textes de C-1 valent à `3e275a2`. Des fichiers non suivis en cours d'écriture (`docs/adr-0029/DECISIONS-ARCHITECTURE-S2BIS.md`,
  `CONTRE-EXPERTISE-DECISIONS.md`, `etude-marche/`) annoncent un nouvel état : relire la ligne Statut d'ADR-0029 et le JOURNAL au moment du commit.
- **A-2** : en posant le pt 2 du §8 (ADR-0025), repérer l.14 par son sha256 `0fe88f1a…` sans l'afficher, comparer l.1 à l'intitulé reconstitué
  de l'index ; s'ils diffèrent, prendre l.1 et retirer la mention de provenance, avant le commit.
- **A-3** : contrôle FM-1.1 de la transcription du worker : la ligne d'index cite « l.3 du fichier » pour ADR-0026, que l'ADR-0029 déclare porteuse
  de matière Pocket ; son brief interdisait « toute matière Pocket » (affichage ou contrôle par jetons : à établir).
- **A-4** : DOC-HARNAIS-2 garde sa règle récurrente : le lot DETTES-B1 (tests dans `s2-harness`) change le compte et doit re-mesurer le README.
- **A-5** : hors de ce lot : la ligne Statut d'ADR-0029 (l.4) liste encore « (2) un cp-1 du validateur sur cette révision » alors qu'il est rendu ;
  un ajout daté au fichier est dû (acte ou item).

## 4. Observations non bloquantes

- **O-1** : DECISIONS (ADR-0028) et feuille de route datent le sceau du 2026-10-03 : c'est le sceau en vigueur ; le premier (2026-10-02, genTime
  17:44:30Z, remplacé avant toute exécution) « reste cité » par la règle A-8 (docs/11 §8.1, §10.3). Une incise le dirait.
- **O-2** : fiche, consigne WORKTREE : « (règle 2) » étend la liste littérale de la règle 2 (`git merge` n'y figure pas) ; resserrage licite
  (règle 7), mais un brief qui ordonne d'avancer une base en worktree (comme le G0 de D8c §15) devra le dire expressément.
- **O-3** : fiche, consigne MUT-FATAL : nommer le registre (« mutants de gate », ADR-0011 pt 4) suivrait mieux doc 09 (trois registres) ; la
  locution interdite (« mutant semé » sans registre) n'est pas employée.
- **O-4** : `sorties/finale/sha256.txt` (04:40) porte pour `mutants_dettes_a.py` `3368155…`, état antérieur ; le fichier actuel = `abea108…`
  = `sha256-livrables.txt` (04:43), qui fait foi.
- **O-5** : la sonde du worker passe à 19/19 sur la tête patchée alors que C-1 et C-2 existent : ses contrôles R2 et H1-H3 ne couvrent ni
  l'état du cp-1 d'ADR-0029 ni le rattachement étapes/RENDU.
- **O-6** : pas de journal G1 du worker dans le dossier (lectures et niveaux, écarts) ; ses écarts autres que le 5 n'ont pas été relus.

## 5. Items, un par un (après application de C-1 à C-6)

| item | état proposé | preuve |
|---|---|---|
| SHOGEN-REGISTRES-S2-1 | fermable au commit | REG-02 : six lignes d'index, dates exactes (C-1, C-5, C-6) ; REG-04 : « État au 2026-10-04 », chiffres = docs/11 (C-1) ; REG-05 : note datée, trois commits exacts (C-3) |
| SHOGEN-ERRATA-ADR0028-1 | **ouvert** | pts 1, 3, 4 posés ; restent pts 2, 5, 6 et les actes 8, 13-16 de §1 bis.11 (contrôle 7) |
| SHOGEN-DOC-HARNAIS-2 | fermable pour cette mesure ; règle récurrente maintenue | 398 recomptés à `5afbdd2` et à `3e275a2` ; historique 307/376/383/398 recompté (C-2 ; A-4) |
| SHOGEN-HARNAIS-ECHAPPEMENTS-1 | fermable au commit | consigne au corps ; G0 D8c §5.1 h, §15 ; B.16 l.273 |
| SHOGEN-WORKTREE-BASE-HOOK-1 | fermable au commit | consigne au corps ; C-07, C-12 ; E-1 de B0 et D8a ; B.16 l.274 (O-2) |
| SHOGEN-HARNAIS-TACHE-10MIN-1 | fermable au commit | consigne au corps ; E-7 de D8c ; B-2 et K-2 ; B.16 l.277 |
| SHOGEN-HARNAIS-BASH-WSL-1 | fermable au commit | consigne au corps ; E-9 de D8c ; JOURNAL l.278 ; B.16 l.287 |
| SHOGEN-MUT-FATAL-1 | fermable au commit | consigne au corps ; contrat 0/1/3 des runners ; E-10 de D8c ; B.16 l.288 (O-3) |

## 6. Journal de provenance

**Lectures** ([lu] sur la source ; [calc] calcul de ce réviseur ; [abs] absent de la source lue ; [2nd] de seconde main) :
brief G2 [lu] ; brief du worker `BRIEF-DETTES-A.md` [lu] ; trois diffs, fragment, `bilan.txt`, sorties finales, `verification-finale.sh`,
`compter.sh`, en-tête de `mutants_dettes_a.py` [lu] ; `docs/adr-0028/G0-lots-DETTES.md` (entier) [lu] ; `ETAT-REGISTRE-2026-10-04.md`
l.25-45, l.171-173, lignes des items, l.102, 116-117, 153, 180, 229-241, 254 [lu] ; `ANNEXE-B-items.md` l.1-12, l.15, l.40-70, l.255-300 [lu] ;
`ANNEXE-D-preenregistrement.md` l.3, l.24-30, l.32-47 [lu] ; `ADR-0028-decisions-sortie-S2.md` l.1-63, l.130-136, l.167-181, l.251-305
(extraits), l.318-327 [lu] ; `ANNEXE-A-lots.md` l.132 [lu] ; `docs/adr-0024/ADR-0024-…md` l.1-25 [lu] ; `docs/adr-0023/ADR-0023.md` entier [lu] ;
`docs/adr-0029/ADR-0029-…md` l.1-25 (tête et `5afbdd2`), grep « cp-1/statut » [lu] ; `docs/adr-0029/CP1-ADR0029.md` l.1-30, l.187-192 [lu] ;
`docs/11-mesures-pilotes.md` l.1-73, 169-196, 230-261, 329-393, 679-708, 940-957 [lu] ; `docs/DECISIONS.md` l.1-40, titres `## ADR-` [lu] ;
`docs/05-roadmap.md` titres, l.100-166 [lu] ; `s2-harness/README.md` l.60-103 [lu] ; `s2-harness/RUNBOOK-campagne.md` §9, mentions de tests [lu] ;
`JOURNAL.md` l.1-54, 79-99, 173-203 (en-têtes), 278, 330-354, mentions « 273 », « erratum », « partie 4 » [lu] ; l.55-78 [jetons seulement] ;
`docs/09-vocabulaire.md` entier [lu] ; `docs/adr-0028/G0-lot-D8c.md` titres, l.111-126, 363, 368, 571-581 [lu] ; `docs/G1-lot-D8c.md` titres et
lignes citées [lu] ; `docs/G1-lot-B0-pool-analyse.md` l.155, `docs/G1-lot-D8a.md` l.247 [lu] ; `docs/G2-partie-4.md` l.210-220, 310-316, 415-418
[lu] ; `docs/adr-0028/PROCEDURE-EXECUTION.md` l.79 [lu] ; `docs/adr-0028/G0-partie-2.md`, `PLAN-PARTIE-2.md` (mentions RENDU) [lu] ;
`enforcement/tests/run-fixtures-*.sh` en-têtes et fin [lu] ; `enforcement/hooks/pre-commit` l.1-21 [lu] ; `xtask/src/sg8.rs` l.1-80 [lu] ;
`docs/10-mesures-pilotes-design.md` (grep « 1 bis », « renvoi daté », l.285-287), `docs/04-certificat-diversite.md` (grep) , `WISHLIST.md` (grep),
`docs/08-assumptions.md` (compte), `.gitattributes` (grep), `biblio/INDEX.md` (grep Fisher) [lu ; « 1 bis » et « P-0 » : abs] ;
ADR-0025 : intitulé [2nd] (JOURNAL l.51-53, sujet de `d363070`) ; ADR-0026/0027 : l.1 et l.3 [jetons seulement].

**Commandes et sorties** (toutes sous `env -u SHOGEN_S2_CAMPAGNE_CONTROL`, `PYTHONDONTWRITEBYTECODE=1`, `-B` pour Python) :
- `sha256sum` brief et pièces → valeurs de l'en-tête ; `git rev-parse HEAD` → `3e275a2b2466245375041612c6d83b9ef2aafc10`.
- `git apply --check -v` ×3 sur le dépôt → rc 0 ×3 ; copie `git archive 3e275a2 | tar -x` (exclusions) + `git apply` ×3 → rc 0 ×3 ; `diff -rq` → 6 fichiers.
- `cargo --locked xtask verify` (copie patchée, `CARGO_NET_OFFLINE=true`) → `travail/xtask-head-patche.txt` (`d076ae55…f362`) : EXIT=0, VERDICT GLOBAL VERT ;
  S-G5 « 310 fragment(s) contrôlé(s) », aucun fragment non contrôlé dans les lignes ajoutées.
- `bash enforcement/lint-model-pinning.sh .` (patchée et vierge) → `OK (R-1) : 6 fichier(s)` rc 0 ×2 ; `run-fixtures-model-pinning.sh` → `95 ok, 0 échec`.
- Dépôt jetable (copie vierge, `git init`, commit de base, `git apply --index` ×3) : `enforcement/hooks/pre-commit` → `OK (hook)` rc 0 ;
  `gate-secrets.sh --tree` → `OK (secrets) : 486 fichier(s)` rc 0.
- Recomptage de la suite (copie de chaque commit, `python3 -B -m unittest discover -s tests -t .`) → `travail/historique/sorties.txt`
  (`80861295…b34b`) : b323f03 307 ; 0cc5a92 376 ; fdc7252 383 ; f35a70c 398 ; 5afbdd2 398 ; 3e275a2 398 ; tous « OK (skipped=2) », sortie 0 ;
  passe verbeuse à la tête `suite-3e275a2-v.txt` (`db2d4228…c755`) l.206-209 : les deux sauts nommés plus haut.
- `git log --diff-filter=A --follow` ×6 → dates de création (§1) ; `git log --since=2026-08-20 --until=2026-09-19` (branche et `--all`) → trois commits.
- `git log b323f03..f35a70c -- s2-harness/tests` → liste identique à celle du README ; `git diff --stat f35a70c {5afbdd2,3e275a2} -- s2-harness` → vide.
- Script de contrôle des intitulés et statuts d'ADR-0026/0027 → égalité de l.1, jetons de l.3 présents, « checkpoint-1 » à l.3 et l.22 (0026), l.3 et l.16 (0027).
- Jetons de JOURNAL l.55-78 → checkpoint-1 à l.57, 59, 61, « Checkpoint-1 » + ACCEPTE à l.63, checkpoint-2 à l.67, 69, 71.
- Motif R-13 du hook sur `travail/ajouts.txt` (`9a5d1b26…4853`, 96 lignes) → 0 ; sha256 par ligne contre `0fe88f1a…` et `5cc89b56…` → aucune égalité.
- Sonde du worker rejouée sur la tête patchée → `travail/sonde-worker-sur-tete.txt` (`b606afc5…01ce`) : 19 ok, 0 échec (O-5).
- Corrections : `appliquer_corrections.py` sur `corrige3-head` → 8 « ok » ; `xtask-corrige3.txt` (`54e4033a…47c4`) EXIT 0, VERT ; lint rc 0 ; hook rc 0 ; secrets OK.
- Non fait : rejeu de la campagne de mutants du worker (son script écrit dans le dossier du worker ; non demandé ; O-5 documente les angles morts).

**Chiffres recomptés** : dates d'index (6), commits de la période (3), comptes de la suite (6 commits), sauts (2), tailles des diffs (+42/+20/+34,
−0), frontmatter (401 octets, sha), ajout de la fiche (2 882 octets), lignes ajoutées (96 ; 98 après corrections), arrondis de z et z_bloc
recalculés depuis docs/11 §3.1. Aucun chiffre de seconde main.

## 7. Fichiers de travail (`…/scratchpad/dettes/G2-A/travail/`)

`appliquer_corrections.py` `e1e223f643136dbfbc8e8c3a7d2f50aa6dff3fa91920082a8e22ad949d28980f` ; `xtask-head-patche.txt` `d076ae55…f362` ;
`xtask-corrige3.txt` `54e4033a…47c4` ; `historique/sorties.txt` `80861295…b34b` ; `historique/suite-3e275a2-v.txt` `db2d4228…c755` ;
`sonde-worker-sur-tete.txt` `b606afc5…01ce` ; `ajouts.txt` `9a5d1b26…4853` ; copies `pristine-head/`, `patche-head/`, `corrige3-head/`,
dépôts jetables `jetable-head/`, `jetable-corrige3/` (variantes intermédiaires `corrige-head/`, `corrige2-head/`, `jetable-corrige/` conservées).
