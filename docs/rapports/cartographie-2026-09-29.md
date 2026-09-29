# Shōgen — cartographie de clôture de campagne S2 (2026-09-29)

Orchestrateur `claude-fable-5-1` (effort high). Règle Branchement (CLAUDE.md global). Workflow `wf_5cfd7896-a93` : 7 dimensions en lecture seule + 1 critique de complétude, 8 agents `claude-opus-5-5` effort max (R-1 : 8/8 préfixe vérifié), 0 mort, 3 177 269 jetons, 75 min, 1 069 appels d'outils. Dossier de configuration sur F: (`F:\claude-config`), règle « ≥ 4 agents » respectée.
Détails (tables complètes, ~100 paires) : `F:\tmp\shogen-carto-2026-09-29\{rust,harnais-s2,monark,registres,dettes-paroxysme,campagne,git-ci,critique}.md`, sorties brutes `_result.json`, sceau `SHA256SUMS.txt`.
**Non commité** : `cargo xtask verify` est ROUGE à HEAD (voir §2, R-01) et ADR-0013 pt 1 veut qu'un rouge arrête l'intégration. Ce document sera versé au dépôt par le lot « étape 1 ».

## 0. Rectifications de l'orchestrateur (dites à l'investisseur le 2026-09-29, réfutées par la mesure)

1. **« Pas de fichier PAROXYSME-Shogen.md » : FAUX.** Il existe hors dépôt : `F:/PRODUITS/paroxysme-2026-09-27/PAROXYSME-Shogen.md` (225 lignes, sha `a655c401…`, 35 limites, 27 items PX, 13 marqués « non »). Il a été rédigé à `91d9781` et est **périmé** : il ne tient compte ni de la clôture S2, ni d'ADR-0025, ni du lot A, ni des décisions 269-273. La dette réelle : ce registre n'est versionné ni référencé par sha dans aucun des deux dépôts ; il n'a pas été mis à jour à la clôture ; la campagne C7 n'est pas lancée alors que son déclencheur (fin de campagne) est atteint.
2. **« Chaîne B relancée au logon du 25/09 » : FAUX** (JOURNAL l.53 et INCIDENT l.9 le disent aussi). Aucun événement Winlogon 7001 n'a été enregistré entre le 2026-09-24 16:47:25Z et le 2026-09-28 12:12:01Z. Cause mesurée (C-04, déduction forte) : la relance ADR-0024 d'environ 18:13Z a arrêté le python de la chaîne B **sans sa boucle cmd**, et cette boucle l'a relancé en parallèle de la chaîne A. On voit deux démarrages, à 18:15:54Z et à 18:17:46Z. Origine de l'erreur (`error_origin`) : l'orchestrateur MONARK, pas l'environnement.
3. **« Pyth perdu vers le 03/09 » : FAUX.** Pyth répond `ok` pendant toute la calibration (2 876 ok sur 2 881). Il renvoie ensuite **HTTP 401 dès la première fenêtre de campagne**, le 2026-08-26 à 19:00Z : 0 ok sur 40 804 lectures (40 527 `panne_http` et 277 `panne_transport`). Mort située entre le 2026-08-23 et le 2026-08-26 19:00Z.
4. **Relance au logon « non testée » : dépassé.** La dimension harnais-s2 l'a testée : code retour 0, zéro appel interdit, les 3 fichiers identiques à l'octet. On l'a aussi observée : 3 logons après scellement, aucune écriture.

## 1. État mesuré (résumé)

- **Journaux scellés intacts** : sha256 vérifiés concordants avant et après, à trois reprises (orchestrateur, dimension campagne, critique). 38 600 fenêtres distinctes, 2 207 doublons, **couverture calendaire de 83,068 %** (7 868 fenêtres manquantes réparties en 438 trous). Après l'exclusion ADR-0025 : n = 35 982, strate stress 189,95 h ≥ 166,8 h.
- **Les « 11 doublons inexpliqués » sont expliqués** : ce sont les fenêtres de 14:57 à 15:07Z du 2026-09-26, entre le recompte et l'arrêt de la chaîne B. Il n'y a aucun doublon hors de la plage exclue.
- **Code Rust** : 205 tests sur 205 à la racine, témoignage 20/20, typeur 28/28. La chaîne réelle a été rejouée à l'octet (présentation → constat → lot → verdict), et le verdict est **identique à la fixture MONARK** (4 fixtures sur 4). Harnais S2 : 178 tests verts ; le livrable du lot A est identique au commit `742f1fc`.
- **Gates** : `cargo xtask verify` ROUGE depuis `f068972` (35 commits intégrés gate rouge : 3 poussés + 32 locaux) — S-G8 (dates non ISO, JOURNAL l.39-40), S-G4 ×5, S-G5 ×43 (poste). Code Rust vert.
- **Git et CI** : 32 commits signés n'existent qu'en local sur F: (rien de poussé depuis `ed479c5`, le 2026-08-26). La CI ne démarre plus depuis le 2026-08-18 : 169 des 172 échecs sont des jobs jamais lancés, avec un budget Actions à 0 $ et `prevent_further_usage=true`. Le blocage est intermittent : fuzz et mutation ont tourné au vert du 01/09 au 11/09.
- **Le J14 n'a pas tourné, cause ÉTABLIE** : la tâche Claude à usage unique a démarré le 2026-09-09 à 09:00:07Z et sa session est morte en 9 s sur « weekly limit ». La re-dérivation de τ (2026-08-31 02:00Z) est morte en 14 s sur « organization has disabled Claude subscription ». **Les deux tâches tournaient sous `claude-opus-5[1m]`, un modèle banni** : elles ont été créées le 26/08, douze jours après le bannissement.
- **S3** : le critère est tenu en substance (`temoignage_reel.rs:122/167/199/304`), mais la commande `shogen verify` n'existe pas, et la distillation fuzz, le threat model E1, Build L2, DEVOPS v2, l'audit de phase E et le passage public restent ouverts. S3 n'est pas clôturable (R-05).

## 2. Constats bloquants et majeurs (preuves dans les fichiers de détail)

### Bloquants
- **SUP-01 — le pool d'analyse inclut Pyth mort.** R1, L&M et R2 sont calculés sur les 12 flux de `run_params.pool`. La conséquence 3 d'ADR-0023 (k nominal −1, k_eff sur les sources présentes) n'est pas implémentée. ADR-0023 est commitée (`5b6469a`) mais toujours « proposé », et aucune acceptation n'est consignée. Cela **bloque J14 et J28**.
- **R-01 — gates rouges** (voir §1). Préalable à tout commit.
- **F-DP-01 — la « lecture asymétrique du poolé écrite d'avance, §5.5 » n'existe pas.** ADR-0020 et RUNBOOK §5 l'invoquent, mais le doc 10 §5.5 traite de l'estimateur L&M. La décision 273 n'est consignée que dans CHANTIERS MONARK.

### Majeurs, par nature
- **Intégrité statistique (SUP-02)** : deux lectures intermédiaires de statistiques S2 ont eu lieu avant J14 et J28, et avant l'existence de la règle poolée. La première au G1 du lot A (`r1.recompute_from_journal` sur les copies scellées, 2026-09-28 03:12Z), la seconde via MONARK `measure-m009a`. Précision : ADR-0024 et ADR-0025 ont été argumentées sur des heures de couverture, pas sur z. Il ne s'agit donc pas d'un arrêt optionnel au sens strict ; ces lectures sont à déclarer.
- **Harnais** : strate poolée absente (HS2-01) ; `raw.jsonl` écrit mais relu par personne (HS2-02) ; une dernière ligne coupée au milieu d'un caractère UTF-8 lève une erreur (HS2-03) ; aucun job CI ne lance les tests du harnais (GC-06). Doctrine en tension : le harnais est déclaré « jetable » alors que la règle PAROXYSME veut « nourrir MONARK » (HS2-13) — **question investisseur**.
- **Campagne** (chronologie corrigée au §3) : le trou de 42,5 h du 29 au 31/08 vient de la **limite d'exécution de 72 h de la tâche Windows `shogen-campagne`** (code `0x41306` SCHED_S_TASK_TERMINATED), machine allumée, et non d'une coupure (C-01). ADR-0024 l.9 l'attribue à tort. Les dates de coupure écrites dans REPAIR-18 et JOURNAL l.43 sont fausses (C-02). Les trois arrêts longs viennent d'un même mécanisme : ligne NUL non finale → lecteur qui refuse de lire → boucle de relance. Ils représentent 4 468 fenêtres, soit 56,8 % des pertes (C-03). 645 fenêtres ont été sautées alors que le harnais tournait (C-10).
- **Registres** : l'index DECISIONS s'arrête à ADR-0023 (REG-02) ; les statuts d'ADR-0023, 0026 et 0027 ne sont pas tranchés (REG-03, REG-10) ; la roadmap 05 est figée au 2026-08-20 (REG-04) ; le JOURNAL a un trou de 29 jours du 2026-08-20 au 2026-09-18 (REG-05, C-16) ; aucune entrée au journal de provenance depuis le 2026-08-26, lot A compris (REG-06) ; roster et UUID périmés dans CLAUDE.md point 7 et dans les corps d'agents (REG-07) ; point 8 « audit d'entrée dû » faux, AUDIT-ENTREE jamais rafraîchi (REG-08).
- **Branche orpheline** `roster-ban-alignment-2026-08-20` (GC-05, REG-09) : elle porte un **second ADR-0020** en collision avec celui de main, et une décision investisseur « PRISE et EXÉCUTÉE » (gates g1/g3/g5, `enforcement/`) jamais fusionnée. Cause : sessions concurrentes.
- **Sécurité locale (REG-17)** : `.claude/settings.local.json:13` autorise `Bash(rm -rf ./*)` ; biblio/ (151 entrées, 44 Mo) n'existe qu'en copie unique sans sauvegarde (SUP-04). Les preuves Pocket sont sous `F:\tmp\pocket-test` (4,1 Go, temporaire), et seul RAPPORT.md y est scellé (GC-08). Le plan S2 approuvé au checkpoint-1 n'existe que dans `scratch/`, ignoré par git (GC-07).
- **Dettes** : 11 dettes de fetch « avant publication » sans demande formée (F-DP-13). Les dettes biblio de rapport que le plan S2 prévoyait de solder pendant la campagne sont restées ouvertes : 10.1 non lue, 10.4 soldée à 1/4, 10.7 sans source alors que `report.py:280` imprime « Fisher », dette 2 ouverte (F-DP-14). LOOP-GUARD-1 et la re-dérivation de τ sont formées mais échues (F-DP-04, F-DP-06). La distillation fuzz est échue (F-DP-09). Le threat model E1 est ouvert depuis le 2026-08-13 alors que Shōgen est déjà exposé via MONARK (F-DP-10). La clé du notaire S3 est dérivée d'une graine publique, sans item propre (F-DP-35).
- **Côté MONARK (à transmettre à l'orchestrateur MONARK, pas des corrections Shōgen)** : le vérificateur n'est jamais exécuté, et `sha256(utterance.bytes)` n'est jamais recalculé (CARTO-MK-01) ; la liaison `attested→gate` compare l'URL requête comprise, alors que le vérificateur ne lie que l'hôte : la mutation `BTCUSDT→BTCUSDX` passe avec le code 0 (CARTO-MK-02) ; la vitrine « built » et README:33 s'appuient sur le verdict S3, contre ADR-0015 pt 3 et la règle D8 (CARTO-MK-03, F-DP-28) ; affirmations publiques sans support, dont des témoignages présentés comme continus et une indépendance des sources présentée comme mesurée (textes exacts dans `monark.md` §3), contraires au vocabulaire 09 (CARTO-MK-04/05) ; une arête d'exécution non servie campagne → `measure-m009a` → ADR-M002 D6 manque à la carto MONARK du 2026-09-24 (CARTO-MK-07) ; aucun item formé pour l'arête S4 → `gather` Kraidle (CARTO-MK-08) ; PASSATION:44 est périmé (watchdog déjà désactivé).

## 3. Chronologie corrigée des incidents de campagne

| période (UTC) | incident | effet mesuré | origine de l'erreur | item |
|---|---|---|---|---|
| 2026-08-21→23 | calibration 48 h, `tau_revision_needed` | 2 880 fenêtres, 0 trou ; lancement repoussé | — (clause fail-closed) | ADR-0022 |
| 2026-08-23→26 | Pyth passe à 401 (Hermes exige une clé) | 0 ok sur toute la campagne | environnement (amont) | ADR-0023 (proposée ; « ~03/09 » faux) |
| 2026-08-29 18:59Z → 08-31 13:32Z | limite d'exécution de 72 h de la tâche Windows | 2 552 fenêtres, 42,5 h, 1er week-end couvert à 39,6 % | outillage (orchestrateur) | à former : SHOGEN-TASK-72H-1 |
| 2026-08-31, 2026-09-09 | tâches Claude τ et J14 mortes (abonnement, limite hebdo) sous `claude-opus-5[1m]` | τ non re-dérivé, J14 non produit | outillage + roster | décision 270 ; à former |
| 2026-09-14 09:13Z / 09-18 17:53Z / 09-22 20:32Z | coupures → lignes NUL → boucle de relance | 4 468 fenêtres (56,8 % des pertes) | environnement + outillage (lecteur) | SHOGEN-TORN-LINE-1 ; REPAIR-16/18/23 |
| 2026-09-24 | prolongation (couverture, heures de stress) | cible 38 600 | — | ADR-0024 (cause du 29/08 mal attribuée) |
| 2026-09-24 18:15Z → 09-26 15:08:53Z | double pilote : relance ADR-0024 sans arrêter la boucle cmd de B | 2 207 doublons ; pannes binance 1,15 % → 13,18 % | orchestrateur (MONARK) | ADR-0025 acceptée ; LOOP-GUARD-1 échu |
| 2026-09-28 01:27Z | fin, n atteint | 38 600 ; scellement 02:52Z | — | clôture |

## 4. PAROXYSME — du Shōgen complet au Shōgen de MONARK (réponse à la demande investisseur du 2026-09-29)

État aujourd'hui : MONARK sert **une fixture S3 figée** (`s3-binance`, identique à l'octet à la sortie Shōgen rejouée), **sans exécuter le vérificateur**. Aucune sortie S2, S4 ou de certificat n'est servie. Arêtes à construire (détail, tests proposés et prérequis : `monark.md` §4) :

| # | capacité du Shōgen complet | état Shōgen | état MONARK | arête à construire | prérequis |
|---|---|---|---|---|---|
| G1 | témoignage canonique CBOR | construit, 1 lot réel | 1 lot figé | release Shōgen avec manifeste sha → chargeur MONARK avec contrôle d'identité | clôture S3, passage public |
| G2 | vérificateur offline | construit, critère S3 vert | non exécuté (parsing de texte) | vérificateur exécuté à l'appel (lib/WASM ou exécuteur publiant verdict + sha) | API stable ; wasm32 non mesuré |
| G3 | compagnon TLSNotary | construit (workspace autonome) | absent | constat recalculé par exécuteur hors outil | A(upstream-alpha) |
| G4 | témoin vivant à notaire tiers | notaire auto-opéré, clé de démo | absent | session réelle → lot → vérificateur → attest daté | PX-Shogen-3, clé notaire |
| G5 | liaison chemin+requête de `subject` | unité S4, options (a)/(b) | URL exacte non vérifiée | verdict liant la requête → garde gate | décision mainteneur |
| G6 | typeur (prix typé) | *tested*, aucun consommateur | absent | typeur du sujet servi → nombre typé au gate | typeur pour le sujet servi |
| G7 | liaison temporelle / fraîcheur | `observed_at` | « no temporal binding » | `observed_at` → garde de fraîcheur | fenêtre S4 |
| G8 | registre des résidus (08) | publié | committé, non consommé | registre → glossaire servi | aucun |
| G9 | mesures R1 : n, K, z | harnais + journaux scellés ; docs/11 absent | absent (m009a non servi) | docs/11 recalculable → panneau / page docs | chaîne de sortie S2 + go publication |
| G10 | R2 + k_eff (partition) | `r2.py` | absent | partition R2 datée → surface MONARK | ADR-0026 |
| G11 | n_eff | ADR-0026 (G0) | absent | aucune arête servie prévue | cp-1 ADR-0026 |
| G12 | certificat de diversité (04) | spécification seule, 0 code | absent (« fully developed ») | certificat → gate ou fichier publié | clôture S2 + S4 |
| G13 | verdict de quorum + lot vérifiable | 0 code | absent | lot de quorum → gate | S4 |
| G14 | `gather` Kraidle | roadmap seule | absent (INTERFACE-1 ≠ gather) | lot de quorum → stub `gather` | S4 |
| G15 | vocabulaire 09 + gate S-G4 | gate sur docs Shōgen | non appliqué | formes 09 → garde MONARK sur les surfaces Shōgen | aucun |
| G16 | registre PAROXYSME | hors dépôt, périmé | aucun | versionné ou référencé par sha, mis à jour à chaque clôture | clôture S2 |

Ordre recommandé : **temps 1**, corriger le registre public (vitrine « built » face à ADR-0015 pt 3 et D8, textes C3-C10, garde 09 = G15, glossaire des résidus = G8). La règle Branchement veut qu'un écart registre/réalité se solde avant toute nouvelle pièce. **Temps 2**, construire les arêtes G5 → G2 → G9 (après clôture S2 et go) → G4, puis G6/G7/G10, puis S4 (G12-G14).

## 5. Ce qui suit — (F) = fixé par les décisions 269-273 ; (+) = ajout soumis à go

0. (+) **Étape 0, actes immédiats sans gate, sur go** :
   - retirer la règle `rm -rf` de `settings.local.json` (REG-17) ;
   - faire un `git bundle` des 32 commits vers un autre disque, et une sauvegarde scellée de biblio/ (SUP-04) ;
   - sceller par sha `baseline_step0.out` du G1 (SUP-02), `scratch/plan-s2.md` et les preuves Pocket (GC-07, GC-08).
1. (+) **Étape 1, remettre les gates au vert avant tout commit** : dates ISO et identifiants de runs faux au JOURNAL (l.39-40) ; les 5 sites S-G4 ; S-G5 ×43 (à dimensionner) ; puis versement de ce document, de l'entrée de provenance du lot A et des re-épinglages d'agents.
2. (F) **G2 du lot A** (réviseur distinct du générateur), parallélisable avec l'étape 1.
3. (+) **Pré-enregistrement** avant tout rendu J14/J28 (SUP-02) : décision 273 portée au JOURNAL ; décision investisseur sur ADR-0023 et le pool d'analyse (SUP-01) ; règle poolée écrite (F-DP-01), rédigée et validée par des agents sans accès aux lectures intermédiaires ; lectures intermédiaires déclarées.
4. (+) **Lot B0 « pool d'analyse »**, si la conséquence 3 d'ADR-0023 est acceptée.
5. (F) **Lot B** : sensibilité à l'inclusion ou l'exclusion de la plage, couverture par week-end (valeurs de référence 19,0 / 46,68 / 43,52 / 47,9 / 32,85 h), n = 35 982.
6. (F) **Lot strate poolée** (décision 273).
7. (F) **J14 rétroactif**, avec la coupe à trancher (§6 b).
8. (F) **J28**, puis oracle, puis `docs/11-mesures-pilotes.md`, cp-2, G7, clôture S2. Publication = acte investisseur.
- En parallèle, après l'étape 1 : registres (index DECISIONS 0024-0027, roadmap S2/S3, README et RUNBOOK, CLAUDE.md points 7-8) ; forge (facturation, runners avant le 2026-10-19, statuts requis sur main, décision de push) ; portage de la branche orpheline ; items à former (SHOGEN-POOL-ANALYSE-PYTH-1, SHOGEN-S2-INTERIM-READ-DISCLOSURE-1, SHOGEN-BIBLIO-CUSTODY-1, SHOGEN-TASK-72H-1, SHOGEN-SCHED-MONITOR-1, SHOGEN-TAU-REDERIV-1, etc. — liste complète dans `critique.md`).
- Fin de S3 (commande `verify`, cmp en CI des copies, CI du typeur et de la session, distillation, E1, Build L2, DEVOPS v2, phase E) **avant toute arête « release » vers MONARK**.
- PAROXYSME : registre versionné ou référencé par sha dans F:/Shogen, mis à jour (L-36..L-53, SUP-01/02/04) ; ordre de C7 à trancher face à J14/J28.

## 6. Décisions investisseur

(b) Coupe du J14 : ≤ 2026-09-04 00:00Z → **9 261** fenêtres, stress 19,0 h ; ou ≤ 2026-09-09 19:00Z (14 jours de collecte) → **17 315**.
(c) Actes hôte : retirer `Startup\shogen-resume.bat`, poser LOOP-GUARD-1, supprimer les 4 tâches désactivées (dont celle qui porte la limite de 72 h).
(d) Push : après l'étape 1 et le G2 du lot A ; trancher d'abord si les docs 15/16 (SENSIBLE) peuvent aller sur le remote privé (GC-04). Facturation Actions : acte investisseur.
(e) Branche orpheline : porter g1/g3/g5 dans un lot neuf, consigner la collision ADR-0020, puis retirer la branche.
(f) ADR-0023 : acceptation, avec un amendement du pool d'analyse (Pyth mort dès la première fenêtre).
(g) Paquet de pré-enregistrement : oui ou non.
(h) Règle `rm -rf ./*` : retrait.
(i) `git bundle` et sauvegarde de biblio/.
(j) Doctrine du harnais : jetable, ou promu pour nourrir MONARK (HS2-13).
(k) Procurements PXP-20 et PXP-30 (dus, échéance passée pour PXP-20).

## 7. Registre PAROXYSME (rappel obligatoire)

Registre `F:/PRODUITS/paroxysme-2026-09-27/PAROXYSME-Shogen.md` : hors dépôt, périmé à `91d9781`, 35 limites / 27 items PX / 13 sans item. Campagne C7 non lancée alors que son déclencheur est atteint ; PXP-20 et PXP-30 dus. À versionner ou à référencer par sha dans F:/Shogen à cette clôture.
