# G0 — proposition pour les lots COLLECTE-BIS, RECALC-BIS et DEPLOI-BIS (S2-bis), sans code

- **Statut** : proposition d'un worker à l'orchestrateur, à adjuger. Rien n'est décidé ici. Aucun code, aucune écriture au dépôt,
  aucune opération git.
- **Gate 0** : modèle résolu `claude-opus-5-5`, effort max (fiche `shogen-worker`).
- **Dates** (`date -u`) : lecture des pièces du 2026-10-04 16:16 à 16:39 UTC ; rédaction à partir de 16:39 UTC.
- **Brief** : `scratchpad/s2bis/g0-collecte/BRIEF-G0-COLLECTE.md`, sha256 `6c4cbd9d…24c1f`, recalculé, égal à l'annoncé.
- **Base lue** : branche `claude/compassionate-noether-szmdyj`. Tête au début de la lecture : `6c37859`. Tête à la fin : `e16956b`
  (commit de l'orchestrateur pendant la lecture, qui ajoute à l'ADR-0029 l'amendement daté du §2.6, l.181, lu en entier ; il ne
  touche ces lots qu'à E-R-09). Les « l.n » de l'ADR-0029 renvoient à `e16956b`. À 16:52 UTC, la tête est `4a31685` (six
  commits du lot PLAN-S2BIS, sous `scripts/plan-s2bis/` seulement). L'ADR-0029 et l'annexe B y sont inchangées (sha256
  `02f8f6cc…` et `31da5b35…`) [mesuré].
- **Rattachement** : ADR-0029 révision 3, acceptée : §2.1 (l.76-84), §2.2 (l.86-98), §2.3 (l.100-116), §2.4 c, e à h
  (l.135-162), §2.5 (l.164-173), §2.7 (l.192-212), §2.8 (l.214-227), §2.9 (l.229-248), §2.10 (l.250-260), §5, §6 lots 5 à 8
  (l.383-386), §8 (l.430-464). Décisions d'architecture (`DECISIONS-ARCHITECTURE-S2BIS.md`, le §7 prime) ; avis OPS (Q3, Q7, Q8,
  Q9, Q10, Q12) ; avis sur les questions techniques V3 (« AQT », Q1 à Q5) ; avis STATS (Q1, Q2, Q11) ; G0 de vague
  `docs/adr-0029/G0-lots-S2BIS.md` (l.17-18) ; ADR-0028 D6 (i) ; `docs/11-mesures-pilotes.md` §9 ; annexe B d'ADR-0028 (items
  cités avec leur ligne) ; JOURNAL l.382 (décisions de l'investisseur du 2026-10-04 : réponses directes, et recommandations de
  l'orchestrateur acceptées en bloc, « Toutes acceptées (Recommandé) », pour les questions 5, 6, 7, 10, 12 et 13).
- **Conventions** : [lu] lu sur la pièce ; [mesuré] commande lancée par le rédacteur (journal de provenance, §9) ; [calc] calcul
  du rédacteur ; [inféré] raisonnement du rédacteur ; [abs] absent des pièces lues. Exigences : E-C (collecte), E-R (recalcul),
  E-D (déploiement). Sous-lots : CB, RB, DB. Tests : T-… ; mutants : M-… ; questions techniques : Q-… ; actes de l'investisseur :
  A-n. Tailles : lignes ajoutées, tests compris, documents hors compte (annexe A d'ADR-0028, l.5 : « 200 lignes ajoutées par
  lot ») ; toutes les tailles sont des estimations [inféré].
- **Renvois de lignes** : un « l.n » sans autre mention renvoie à l'ADR-0029 à `e16956b`. Un identifiant d'item suivi de « (l.n) »
  renvoie à sa ligne de l'annexe B d'ADR-0028. Dans les tableaux « Réutilisé ou réécrit », un « l.n » placé après un fichier de
  S2 renvoie à ce fichier ; « ADR l.n » renvoie à l'ADR-0029.

## 0. En bref

1. Le code de S2-bis vit dans un paquet neuf, `s2bis/`, sous G0-G7 dès le premier commit. `s2-harness/` n'est pas modifié.
2. **COLLECTE-BIS** réécrit la collecte. Elle reprend les décodeurs de S2 et leurs fixtures. Tout le reste est neuf : lectures
   concurrentes avec échéance dure, sous-types de panne, journal chaîné à enregistrement unique, santé par fenêtre (chrony,
   témoins DNS), processus séparé pour la carte et les relevés ASN, têtes de chaîne et jeton quotidien, smoke sans prix,
   commande `status`. Deux limites de la collecte de S2 sont mesurées sur fixtures : une coupure pendant la lecture du corps fait
   lever `sources.read()`, et le délai d'`urllib` ne borne pas la résolution DNS (§9).
3. **RECALC-BIS** importe les fonctions pures du chemin de recalcul de S2 (`classify_ecart`, z, z_bloc, FIV, L&M, état ASN). Il
   ajoute un lecteur en flux, la consolidation au quorum, la rotation en masques de bits, la règle R1-2, la variable d'état, les
   sensibilités, la R2 multi-points de vue, le rendu, un lecteur indépendant et le script d'exécution unique. Les lecteurs et le
   rendu de S2 ne sont pas réutilisables tels quels : format de S2, lecture en mémoire entière.
4. **DEPLOI-BIS** écrit un script de premier démarrage unique (pare-feu, chrony, résolveur par famille, unités systemd,
   sauvegarde, signal de vie, jeton quotidien), testé sur une racine factice. Il écrit aussi la procédure d'intervention en
   langage clair et les entrées du modèle de menace.
5. **Taille** : environ 8 100 à 8 600 lignes avec tests, en 46 à 49 sous-lots de 200 lignes au plus [inféré]. C'est trois à
   quatre fois plus que l'ADR §3 (l.308), mais c'est cohérent avec la taille mesurée du harnais de S2 (5 791 lignes de code, 8 774 lignes de
   tests [mesuré]). Le jalon « lots 3 à 6 commis à S+5 » (l.393) est à revoir.
6. **Cinq parties** sont proposées (METHODE-PARTIES) : collecteur, noyau ; collecteur, contenus ; recalcul, moteur ; recalcul,
   sorties ; déploiement. Chacune a une relecture G2 neuve et un accord de l'investisseur.
7. **Questions techniques** : 45 au total (§6), dont six écarts à la lettre de l'ADR signalés sans être appliqués (§7). Les plus
   lourds :
   - le clone du dépôt privé sur des serveurs tiers ;
   - le volume des journaux contre des disques de 25 Go ;
   - le mécanisme d'échange des têtes et de `status` ;
   - l'axe des runs de la garde d'information ;
   - l'encodage de l'entrée de SHA-256 des décalages.
8. **Actes de l'investisseur** (§8) : un accord par partie ; les comptes ; les serveurs et le collage du script ; les sous-comptes
   de sauvegarde et les clés ; les quatre alertes ; les exercices de mise en service ; les gestes d'intervention pendant la mesure.

## 1. Règles communes aux trois lots

1. **Où vit le code** (Q-G-01). Proposition :
   - `s2bis/shogen_s2bis/collecte/` : code des observateurs ;
   - `s2bis/shogen_s2bis/recalc/` : chemin de recalcul ;
   - `s2bis/tools/` : exécution unique ;
   - `s2bis/config/` : données scellées ;
   - `s2bis/deploi/` : script et unités ;
   - `s2bis/tests/`.

   Les documents (spécification du format, pages de licence, procédure) vont sous `docs/adr-0029/s2bis/`, dans le périmètre
   actuel des gates S-G4 et S-G5. Rien ne change dans `s2-harness/` : la collecte de S2 reste en quarantaine (D6 (i)) et tout
   rejeu de S2 se fait à `f35a70c` (B.49).
2. **Frontière d'imports, testée** : c'est une fonction de fitness G4, dès CB-0.
   - `collecte` : bibliothèque standard et `collecte` seulement.
   - `recalc` : bibliothèque standard, `recalc`, `collecte.decodeurs` (re-décodage) et une liste fermée de fonctions du chemin de
     recalcul de S2 (§3.1). Aucun module en quarantaine en import direct.
   - Limite déclarée : `r1` importe `model.Status`, qui est en quarantaine [lu, `r1.py` l.56]. La garde (2) de l'exécution
     unique porte donc sur tout `s2-harness/shogen_s2`.
3. **Configuration scellée = données versionnées** :
   - fichiers concernés : formes de requête, santé (témoins, noms, seuils), carte, paramètres d'analyse ;
   - leur sha256 entre au paquet (l.217) ;
   - le code refuse une configuration incomplète ou incohérente, par un refus nommé ;
   - `run_params` porte le commit et le sha256 de chaque fichier chargé.
4. **Fixtures seulement** (D.4-bis, l.226) :
   - tests sans réseau, sous une garde réseau ;
   - aucun journal de S2 : `*.jsonl` interdits, `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée ;
   - aucun journal de S2-bis : les journaux de test sont fabriqués par l'écrivain de CB-1 ;
   - après le déploiement, aucun G1 ni G2 ne lit un journal de rodage. Les lectures de classe M sont réservées à
     l'orchestrateur (l.223).
5. **Tests d'abord** :
   - valeurs de référence indépendantes du code ;
   - échec montré avant correction ;
   - une mutation par test (METHODE-PARTIES §2) ;
   - campagnes de mutants classées par la sortie du runner : 1 tué, 0 vivant, 3 ou hors contrat = FATAL, relancée ;
   - campagnes longues découpées sous la borne de 10 min.
6. **Gates** :
   - suite `s2bis` sur un job CI neuf, image épinglée (SHOGEN-CI-RUNNERS-1, annexe B l.80) ;
   - la suite est jugée sur son résumé, et aucun saut n'est admis (SHOGEN-CI-S2-SAUT-1, l.79) ;
   - plancher relevé à chaque sous-lot (SHOGEN-CI-PLANCHER-SUIVI-1, l.764) ;
   - un test lit les étapes du job (SHOGEN-CI-S2-CABLAGE-1, l.760) ;
   - suite `s2-harness` inchangée : 405 tests, OK (skipped=2) [mesuré] ;
   - hook pre-commit ;
   - `cargo --locked xtask verify`, sortie redirigée, lignes de verdict seules ;
   - gate des secrets : aucune adresse de surveillance ni aucun identifiant au dépôt.
7. **Parties** (METHODE-PARTIES §2 ; Q-G-03) : cinq parties (§5). Chacune a :
   - une relecture G2 neuve à 100 %, avec la checklist G2 du corpus (SHOGEN-G2-CHECKLIST-CORPUS-1, l.893) ;
   - un enregistrement de rôle `shogen.oracle-record.v1` (SHOGEN-G2-ENREG-ROLE-1, l.894) ;
   - une revue de l'orchestrateur ;
   - un accord de l'investisseur.
8. **Vocabulaire** : registre doc 09, sans qualificatif d'assurance.

## 2. COLLECTE-BIS

### 2.1 Périmètre

**Modules à créer** (`s2bis/shogen_s2bis/collecte/`) :

| module | contenu |
|---|---|
| `config.py` | chargement des configurations scellées, sha256, refus nommés |
| `grille.py` | grille UTC (w = 60 s) et calendrier des strates. La convention est reprise de `shogen_s2.window.window_start` par copie, avec un test croisé côté tests |
| `lecture.py` | lecture typée : statut compatible avec `r1.classify_ecart` (`ok`, `panne_http`, `panne_transport`, `panne_decode`), sous-type, phases horodatées, adresse contactée, octets, valeurs décodées |
| `http.py` | client HTTPS par phases (DNS, connexion, TLS, requête, corps), IPv4, délai global de 10 s, attrape-tout typé |
| `decodeurs.py` | un décodeur par (hôte, actif) : BTC (repris), ETH, USDC, USDT, témoin |
| `journal.py` | écrivain unique chaîné, fsync au marqueur, fichiers quotidiens, point de contrôle, verrou exclusif, reprise |
| `dns.py` | client DNS minimal en UDP, format filaire (SOA, A, TXT, TTL, rcode) |
| `sante.py` | D-2 (horaires), D-3 (`chronyc`), D-4 (SOA des témoins), D-5 (noms témoins), disque, fils, empreinte du résolveur |
| `boucle.py` | boucle du processus du pool |
| `secondaire.py` | processus de la carte et du relevé ASN |
| `asn.py` | relevé ASN par le résolveur de l'observateur |
| `tetes.py` | têtes de chaîne, échange, manifeste, requête RFC 3161 |
| `smoke.py` | smoke sans prix |
| `status.py` | commande `status` |
| `__main__.py` | points d'entrée |

S'y ajoutent :
- les données : `s2bis/config/formes.json`, `sante.json`, `carte.json` ;
- les tests et fixtures : `s2bis/tests/` ;
- les documents, hors compte : `docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md`, une page de licence par source de la carte ;
- la CI : un job dans `.github/workflows/gates.yml`, et un vérificateur de suite, soit paramétré soit neuf.

**Réutilisé ou réécrit, avec motif** :

| S2 (quarantaine, D6 (i)) | S2-bis | motif |
|---|---|---|
| décodeurs de `sources.py` (l.125-218) et leurs fixtures | **repris** par copie, relus en G2 | ADR l.231 |
| `sources._http_get`, `_http_post_json`, `read` (l.48-79, l.378-402) | **réécrits** | aucun sous-type de panne (ADR l.236). `read()` est documenté « ne lève jamais » (l.380), mais une coupure pendant la lecture du corps laisse sortir `ConnectionResetError` [mesuré, §9, essai 1]. Le délai d'`urllib` ne borne pas la résolution DNS [mesuré, essai 2] |
| `sources.SPECS` (l.239-283) | **remplacé par des données scellées** (`formes.json`) | formes par (hôte, actif), regroupements imposés par le débit (ADR l.234), retrait ex ante d'une source sans changer le code (réponse à la q. 13 : sources retirées si les conditions interdisent la republication, JOURNAL l.382) |
| `collector.collect` (l.96-252) | **réécrit** | lectures en série (l.244-247), δ de 5 s par défaut (l.54) ou 10 s (`run_campaign.py` l.62), aucune échéance |
| `collector.clock_check` (l.63-93) | **remplacé** par le relevé chrony (D-3) | plausibilité croisée sur `source_ts`, « pas NTP » (l.28-30) ; elle lit des données de source (SHOGEN-CLOCKCHECK-SEMANTIQUE-1, ADR l.445) |
| `run_campaign.run_segment` (l.200-275) | **réécrit** en points d'entrée sous systemd | `collect_asn` tourne sur le fil de collecte à chaque chunk (l.262) ; `distinct_completed` relit tout `control.jsonl` (l.190-197) ; la reprise passe par un `.bat` qui reboucle (RUNBOOK l.62) |
| `journal.py` (deux fichiers, l.12 ; `append_jsonl` sans fsync, l.61-63) | **réécrit** | un enregistrement unique par lecture, chaîné, fsync au marqueur (ADR l.238 ; SHOGEN-RAW-LECTEUR-1 (l.45) ; SHOGEN-RAW-FIN-1 (l.354)) |
| `model.py` | **réécrit** (`lecture.py`) | sous-types, phases, adresse contactée ; les statuts restent lisibles par `classify_ecart` |
| `smoke.py` | **réécrit** | il imprime prix et fourchette du pool (l.42-43, l.60-64), or le rodage interdit toute lecture de prix (ADR l.222). Il faut aussi les formes (hôte, actif), le témoin et la carte (ADR l.81) |
| `closure.py` | **non repris** | la calibration de S2-bis relève de PLAN-S2BIS et de CALIB-ACTIFS |
| `r2.collect_asn` et `resolve_host_real` (l.315-379) | **réécrits** ; forme de `_ripestat_asn` reprise | résolveur unique `cloudflare-dns.com` en DoH (l.258) ; S2-bis exige le résolveur de chaque observateur et jamais 1.1.1.1 (ADR l.82) |
| `records.*_record`, `records.append_asn` | **remplacés** par les types du format de S2-bis | format neuf, scellé (ADR l.239) |

### 2.2 Exigences

| n° | exigence (testable) | rattachement |
|---|---|---|
| E-C-01 | Paquet neuf, bibliothèque standard seule ; aucun import de `shogen_s2` ; frontière testée par analyse syntaxique des imports | l.231-232 ; D6 (i) ; R-8 |
| E-C-02 | Configurations scellées chargées et contrôlées (champs, types, bornes) ; `run_params` porte le commit et le sha256 de chaque fichier | l.217 ; l.238 |
| E-C-03 | Une lecture ne lève jamais. Toute anomalie devient un statut typé. `panne_transport` porte un sous-type parmi {dns, connexion, tls, delai, coupure, autre} | l.236 ; essai 1 (§9) |
| E-C-04 | Pour chaque lecture, le journal porte : heure de départ et de fin, instants de fin de chaque phase, adresse contactée | l.233 |
| E-C-05 | Lectures en IPv4 seule (Q-C-01) | l.79 (ASN de l'adresse réelle) |
| E-C-06 | Décodeurs : BTC repris de S2, puis un décodeur par (hôte, actif) pour ETH, USDC, USDT, le témoin et la carte, chacun avec ses fixtures. Un prix non fini, nul ou négatif donne `panne_decode` | l.231 ; SHOGEN-PRIX-NON-FINI-1 (l.612) |
| E-C-07 | Tout calcul `Decimal` d'un décodeur (Chainlink, Uniswap, Curve) se fait sous un contexte nommé (précision, arrondi), jamais sous le contexte du fil (Q-C-14) | analogue de SHOGEN-CLOSURE-CONTEXTE-1 (l.352) |
| E-C-08 | Devise de cotation et classe de source dans chaque relevé | l.98 ; l.248 |
| E-C-09 | Formes de requête : CoinGecko regroupé (une requête par fenêtre et par observateur) ; Bitfinex regroupé ; ailleurs, requêtes séparées décalées d'au moins 1 s quand la limite de l'hôte l'exige, 5 au plus par hôte et par fenêtre ; requête BTC de S2 gardée là où c'est possible ; regroupements déclarés dans `formes.json` | l.234 |
| E-C-10 | Flux plafonnés (Chainlink USDC/USD et USDT/USD) : drapeau et valeur du plafond portés par la forme, lus par la classe « borné » au recalcul | l.98 (b) |
| E-C-11 | Départ des lectures à ws + w − δ, δ = 20 s ; délai de 10 s par requête ; échéance dure à ws + w − 1 s tenue par le fil principal | l.233 ; avis OPS Q7 |
| E-C-12 | À l'échéance : (a) le marqueur est écrit ; (b) une lecture non finie est classée `panne_transport:delai`, ou `:dns` si la résolution n'a pas rendu ; (c) le fil est abandonné | l.233 |
| E-C-13 | Pool de fils borné, taille scellée. Les fils abandonnés encore vivants sont comptés dans la santé. Un résultat tardif n'est jamais écrit comme lecture d'une fenêtre close : il est compté à part (Q-C-15) | l.233 |
| E-C-14 | Une lecture planifiée qui ne part pas faute de fil n'est jamais une panne de source (Q-C-02) | l.102 |
| E-C-15 | Aucune tâche bloquante sur le fil de la boucle entre deux fenêtres : ni relevé ASN, ni relecture du journal, ni lecture de source hors forme | [inféré] ; `run_campaign.py` l.190-197, l.262 |
| E-C-16 | Un seul processus par journal : verrou exclusif (`fcntl.flock`). Une seconde instance sort sans rien écrire | SHOGEN-ENTRELACEMENT-D5-1 (l.798) |
| E-C-17 | Un enregistrement unique par lecture : valeurs décodées, octets bruts en base64 et leur sha256 | l.238 |
| E-C-18 | Chaîne : chaque enregistrement porte `seq` et le sha256 des octets de l'enregistrement précédent ; sérialisation canonique (clés triées, séparateurs fixes, UTF-8) | l.238 |
| E-C-19 | fsync au marqueur de fenêtre ; enregistrement de point de contrôle horaire qui porte la tête | l.238 |
| E-C-20 | Fichiers quotidiens bornés à 00:00 UTC, clos par un enregistrement de clôture et sommés (sha256 dans un fichier de sommes). La chaîne continue d'un fichier au suivant | l.240 |
| E-C-21 | Reprise : la chaîne reprend au dernier enregistrement intègre. Une queue tronquée (ligne coupée, octets NUL) n'est jamais réécrite : un nouveau segment s'ouvre, et son enregistrement `reprise` la déclare (position, sha256) | SHOGEN-TORN-LINE-1 (l.42) |
| E-C-22 | Toute fenêtre sans marqueur porte sa cause : enregistrement `trou` à la reprise (arrêt du processus, horloge reculée). `window_start` est strictement croissant d'un démarrage au suivant | l.112 ; SHOGEN-CENSURE-S2BIS-1 (l.685) |
| E-C-23 | `run_params` à chaque démarrage : descripteur d'observateur (fournisseur, région, ASN mesuré, résolveur, versions des paquets, empreinte de configuration) et paramètres porteurs (w, δ, délai, échéance, taille du pool, calendrier, formes) | l.238 |
| E-C-24 | Format décrit dans un document scellé au paquet. Un test de conformité valide contre cette spécification un journal produit par l'écrivain | l.239 ; SHOGEN-FORMAT-JOURNAUX-1 (l.55) |
| E-C-25 | Santé, un enregistrement par fenêtre, sans aucune donnée tirée d'une lecture de source : D-2 (heure prévue, départ de la première lecture), D-3 (sortie de `chronyc` : décalage, délai et dispersion racine, statut, âge du relevé), D-4, D-5, fils abandonnés, disque, empreinte du résolveur | l.237 ; l.102 ; l.106-110 ; CLOCKCHECK-SEMANTIQUE-1 |
| E-C-26 | Le collecteur journalise des valeurs brutes. Le jugement « dégradé » se fait au recalcul et dans `status`, avec les seuils scellés [inféré : recalculable ; sert la sensibilité (ii)] | l.115-116 ; l.210 (ii) |
| E-C-27 | D-4 : une requête SOA de « . » en UDP par fenêtre et par témoin, vers 198.41.0.4, 192.36.148.17 et 193.0.14.129, délai de 2 s | l.109 |
| E-C-28 | D-5 : les deux noms témoins scellés sont résolus par le résolveur de l'observateur (client DNS dirigé vers son adresse) ; rcode, TTL et adresses journalisés | l.110 |
| E-C-29 | Instant des sondes de santé dans la fenêtre : fixé et scellé (Q-C-03) | l.116 ; l.217 |
| E-C-30 | Relevé ASN quotidien, par observateur et par hôte (quatre classes, témoin, carte). L'adresse A vient du résolveur propre ; RIPEstat et Cymru (TXT par le client DNS) sont journalisés séparément ; un échec est typé | l.247 ; l.80 ; l.224 (R-c) |
| E-C-31 | Le relevé ASN ne tourne jamais sur le fil du pool (Q-C-04) | l.233 ; [inféré] |
| E-C-32 | Carte : processus systemd distinct, avec son pool de fils et son journal chaîné ; départ à ws + 5 s (valeur scellée). Un échec de la carte n'affecte ni D-1 à D-5 ni le marqueur du pool | l.235 ; AQT Q1 |
| E-C-33 | Un hôte présent au pool et à la carte garde un seul budget de débit par adresse, selon une règle scellée | l.235 |
| E-C-34 | Une source n'entre au collecteur que prête au gel : conditions lues (page de licence), décodeur et fixtures relus en G2, smoke passé | l.259 (a) ; l.258 |
| E-C-35 | Têtes exportées à chaque point de contrôle. Les têtes des trois autres observateurs sont consignées dès leur lecture | l.240 |
| E-C-36 | Jeton RFC 3161 quotidien sur un manifeste des têtes. La requête est construite en bibliothèque standard ; le `.tsr` est conservé et son sha256 journalisé. L'envoi est armé par un paramètre que seul le go écrit de l'investisseur autorise | l.218 ; l.240 ; q. 7 (JOURNAL l.382) |
| E-C-37 | Smoke : chaque forme (hôte, actif), le témoin, chaque source de la carte ; CryptoCompare re-confirmée en 401. Sortie : statut, code HTTP, sous-type, latence, décodable oui ou non, **jamais un prix ni une fourchette**. Code 0 seulement si toutes les formes du pool et du témoin décodent | l.81 ; l.169 ; l.222 |
| E-C-38 | `status` imprime la santé seule (D-1 à D-5, dernier marqueur, tête, disque) et le compte de fenêtres évaluables par strate. Il ne lit aucun enregistrement de lecture | l.244 ; l.158 |
| E-C-39 | Outil de lecture du rodage, en classe M seulement. Il imprime : taux D-1 à D-5, quorum perdu, puis, par (o, forme) : fraction `ok`, codes HTTP, sous-types, latence ; ASN ; taille des journaux. Jamais un prix, une staleness, un hors-enveloppe, m_j ni une co-occurrence (Q-C-13) | l.221-222 |
| E-C-40 | Tests sur fixtures, sans réseau. Les fixtures neuves sont capturées hors campagne, avec date et sha256 consignés (Q-C-05) | l.226 ; D.4-bis |
| E-C-41 | Fonctions de fitness G4 dès CB-0 : frontière d'imports, absence de réseau, déterminisme (même entrée, mêmes octets). Une baseline de métriques est versée (lignes et tests par module, score de mutation par sous-lot) | G4 ; leçon de SHOGEN-G4-RECALCUL-METRIQUES-1 (l.892) |

### 2.3 Sous-lots (≤ 200 lignes ajoutées chacun ; tailles [inféré])

| sous-lot | objet | taille | dépend de |
|---|---|---|---|
| CB-0 | squelette `s2bis/`, `config.py`, job CI, vérificateur et plancher, fitness (frontière, garde réseau, déterminisme) | ≈ 190 | — |
| CB-1 | écrivain chaîné : sérialisation canonique, `seq` et `prec`, fsync injectable, verrou, point de contrôle | ≈ 180 | CB-0 |
| CB-2 | fichiers quotidiens et sommes ; reprise (queue tronquée, segment, trous, `window_start` croissant) | ≈ 190 | CB-1 |
| CB-3 | `lecture.py` et `http.py` (phases, sous-types, IPv4, délai global, attrape-tout) | ≈ 190 | CB-0 |
| CB-4 | boucle du pool : ordonnancement par hôte, départ, pool borné, échéance, marqueur, résultats tardifs | ≈ 170 | CB-1, CB-3 |
| CB-5 | tests « lecture pendue » (§2.4) et leurs mutants | ≈ 160 | CB-4 |
| CB-6 | décodeurs BTC repris, fixtures reprises, formes BTC, contrôle de finitude | ≈ 170 | CB-3 |
| CB-7 | décodeurs ETH, USDC, USDT des places, avec fixtures | ≈ 180 | CB-6 ; paires servies (SHOGEN-S2BIS-PAIRES-1, G0 de CALIB-ACTIFS) |
| CB-8 | agrégateurs regroupés (CoinGecko, DefiLlama) ; Chainlink ETH, USDC et USDT (plafond) | ≈ 170 | CB-6 |
| CB-9 | témoin (OKX USDC-USDT, Uniswap v3, Curve), contexte `Decimal` nommé | ≈ 180 | CB-6 ; adresses des contrats et hôtes RPC lus sur pièce |
| CB-10 | client DNS filaire (SOA, A, TXT, TTL, rcode) | ≈ 170 | CB-0 |
| CB-11 | santé par fenêtre (D-2 à D-5, disque, fils, résolveur), branchée à la boucle | ≈ 190 | CB-4, CB-10 |
| CB-12 | relevé ASN (A propre, RIPEstat, Cymru) | ≈ 150 | CB-10 |
| CB-13 | processus secondaire (carte et ASN) : journal propre, isolement, budget de débit partagé | ≈ 180 | CB-2, CB-12 |
| CB-14.k | sources de la carte prêtes au gel, par lots de 4 à 6 (décodeur, fixtures, smoke) ; k = 2 à 4 selon la liste fermée | ≈ 175 chacun | CB-13 ; licences lues (SHOGEN-S2BIS-LICENCES-API-1, l.443) |
| CB-15 | têtes : export, échange, manifeste, requête RFC 3161, `.tsr` | ≈ 180 | CB-2 |
| CB-16 | smoke sans prix | ≈ 140 | CB-6 à CB-9 |
| CB-17 | commande `status` | ≈ 160 | CB-2, CB-11 |
| CB-18 | points d'entrée, descripteur, `run_params`, test de bout en bout : collecteur, journal, conformité au format | ≈ 180 | tous les sous-lots du noyau |
| CB-19 | (option, ou lot RODAGE) outil de lecture du rodage | ≈ 160 | CB-18 |

Total : environ 3 480 à 3 990 lignes avec tests [inféré]. Pour comparaison, l'ADR l.308 donne 1 000 à 1 500 lignes, carte non
chiffrée. Base de l'écart : la collecte de S2 seule comptait environ 1 600 lignes de code et 1 080 lignes de tests (`collector`,
`sources`, `run_campaign`, `closure`, `smoke`, `journal`, `model`, plus `collect_asn` et leurs tests [mesuré, `wc -l`]), pour un
seul actif, sans chaîne, sans santé, sans concurrence et sans carte.

### 2.4 Tests attendus et mutants obligatoires

**« Lecture pendue »** (ADR l.233), sous-lot CB-5 :

| test | ce qu'il établit | mutants qu'il doit tuer |
|---|---|---|
| T-LP-1 (horloge et attente injectées) | une lecture qui ne rend jamais : à ws + w − 1 s, le marqueur est écrit, la lecture est `panne_transport:delai`, le fil est compté abandonné, la fenêtre suivante part à l'heure | M-LP-1 attente sans échéance ; M-LP-2 lecture non finie omise du journal ; M-LP-3 marqueur écrit seulement quand tous les fils ont fini ; M-LP-4 fil abandonné non compté |
| T-LP-2 | `getaddrinfo` injecté bloquant : la lecture est `panne_transport:dns` | M-LP-5 sous-type toujours `delai` |
| T-LP-3 | la lecture pendue rend après l'échéance : aucun enregistrement de lecture de la fenêtre close après son marqueur ; un compte « tardive » apparaît dans la santé suivante | M-LP-6 résultat tardif écrit |
| T-LP-4 (sous-processus, fils réels, w réduit par paramètre de test) | une lecture bloquée sur un `threading.Event` jamais posé : le collecteur écrit N marqueurs en temps borné. Le sous-processus a son propre délai, donc un mutant qui pend fait échouer le test sans pendre la suite | M-LP-1 rejoué en conditions réelles |
| T-LP-5 | plus de fils pendus que de places dans le pool : les lectures ne partent pas, aucune n'est écrite en panne de source ; la santé le dit (selon Q-C-02) | M-LP-7 lecture non partie écrite en panne |
| T-LP-6 | corps livré au goutte-à-goutte (un octet toutes les 0,5 s, serveur factice local) : la lecture est close au délai global de 10 s | M-LP-8 délai par opération seulement |

**Autres familles** (un mutant au moins par test) :
- **Client.** Défaut injecté à chaque phase : le sous-type attendu (M : sous-types permutés). Corps coupé : `panne_transport:coupure`,
  régression du défaut mesuré de S2 (M : l'exception sort). Codes 403, 429 et 451 : `panne_http` avec le code. Appel en
  `AF_INET` seulement (M : `AF_UNSPEC`).
- **Chaîne.**
  - Chaîne recalculée par un code de test indépendant, sur les octets écrits (M : `prec` décalé d'un rang ; `seq` non
    incrémenté au changement de fichier).
  - Espion de fsync : un appel par marqueur (M : fsync retiré).
  - Seconde instance refusée sans écriture (M : verrou retiré).
  - Queue tronquée conservée à l'octet et déclarée (M : queue tronquée sur place).
  - Horloge reculée à la reprise : aucun `window_start` répété, trou déclaré (M : doublon admis).
  - Bascule de 00:00 UTC : clôture, ligne de sommes, chaîne continue (M : chaîne remise à zéro).
- **Format.** Un journal produit par l'écrivain est conforme à la spécification (M : champ obligatoire omis).
- **Décodeurs.**
  - Fixtures BTC reprises : mêmes valeurs que `expected.json` de S2.
  - Prix non fini, nul ou négatif : `panne_decode` (M : contrôle retiré).
  - CoinGecko regroupé : quatre relevés.
  - Bitfinex regroupé : positions des champs (M : position décalée).
  - Prix Uniswap calculé sous le contexte nommé : une chaîne attendue qui diffère sous le contexte par défaut (M : contexte par
    défaut).
- **Santé.**
  - Liste blanche des clés de l'enregistrement : aucune clé tirée d'une lecture (M : décalage médian harnais-source ajouté).
  - Octets de la requête SOA égaux à une valeur écrite à la main d'après la disposition de la RFC 1035 (valeur indépendante du
    code).
  - Analyse de la sortie de `chronyc` sur une sortie gelée.
  - Valeurs brutes, aucun champ « dégradé » (M : jugement au collecteur).
- **Processus secondaire.** Une exception ou une pendaison de la carte ne change aucun marqueur du pool (M : lecture de la carte
  dans la boucle du pool). Budget partagé par hôte (M : dépassement).
- **Jeton.** Requête DER pour un sha256 fixé, égale aux octets produits hors du code par
  `openssl ts -query -data <fichier> -sha256 -cert -no_nonce` (OpenSSL 3.0.13 sur l'hôte de session [mesuré]) (M : `certReq`
  absent ; identifiant d'algorithme faux).
- **Smoke.** La sortie sur fixtures ne contient aucune des chaînes de prix décodées (M : prix imprimé). Sortie 0 si et seulement
  si tout décode.
- **Status.** Sortie identique avec et sans enregistrements de lecture dans le journal (M : `status` lit les lectures).
- **Fitness.** Un `import shogen_s2` ajouté est refusé (M). Un test qui ouvre une vraie socket est refusé (M).

### 2.5 Critères de sortie

1. **Par sous-lot** :
   - suite `s2bis` verte et plancher relevé ;
   - suite `s2-harness` inchangée (405, OK, skipped=2) ;
   - campagne de mutants conforme au contrat du runner ;
   - hook, gate des secrets, `xtask verify` verts (lignes de verdict seules) ;
   - journal G1 ;
   - ligne d'annexe A ;
   - ligne JOURNAL.
2. **Par partie** (P1, P2, §5) :
   - relecture G2 neuve à 100 % avec checklist et enregistrement de rôle ;
   - corrections appliquées, rouge avant et vert après ;
   - contrôle FM-1.1 des transcriptions du worker et du réviseur ;
   - revue de l'orchestrateur ;
   - accord de l'investisseur.
3. **Lot** :
   - test de bout en bout vert ;
   - format versé ;
   - commit candidat au sceau consigné ;
   - items fermés ou re-datés : ENTRELACEMENT-D5-1 (Q-C-11), CLOCKCHECK-SEMANTIQUE-1, TORN-LINE-1, RAW-REDECODAGE-1 (avec RB-2),
     COLLECTOR-FISHER-1 (Q-C-12) ;
   - SHOGEN-S2BIS-CARTE-AVEUGLE-1 (ADR l.451) : ce qui en reste reçoit sa réponse. Coût : CB-14.k. Calendrier : Q-C-09. Budget de
     débit partagé : E-C-33.
4. **G0** : cp-1 bref de ce G0 par un validateur frais, avant tout code (proposition), puisque ce code sera scellé.
5. **G7** : à la clôture de S2-bis (lot 11).

### 2.6 Risques et questions techniques

**Risques** :
- La liste des formes de requête dépend d'entrées encore ouvertes :
  - les paires servies par chaque hôte (SHOGEN-S2BIS-PAIRES-1, G0 de CALIB-ACTIFS) ;
  - les adresses du témoin, lues sur pièce ;
  - les licences (q. 13 : une source qui interdit la republication est retirée).
  Un retrait au pool impose de rejouer SIM-NIVEAU-BIS et SIM-PUISSANCE-BIS (l.173).
- OKX est déjà à la limite de cinq lectures séparées (BTC-USDT, index BTC-USD, ETH-USDT, USDT-USD, témoin USDC-USDT ;
  ADR l.234 [inféré]). La pièce CALIB-ACTIFS-G0 [lu] ne trouve sur OKX qu'une paire cotée en USD : USDT-USD.
- L'hôte de la session n'atteint ni Binance (451) ni Bybit (403) [lu, `ETUDE-POOL-BIS.md` §8] : leurs fixtures ne se capturent
  pas d'ici.
- La carte est ouverte en taille : une source = un décodeur, des fixtures, un smoke et une page de licence (EP §7).

**Questions** (adjudication : orchestrateur ; advisor OPS sur demande) :
- **Q-C-01 IPv4 seule.** Recommandé : oui (`AF_INET`). L'ASN est mesuré sur l'adresse IPv4, et une sortie IPv6 chez un seul
  fournisseur donnerait des chemins non comparables [inféré]. IPv6 refusé au pare-feu (Q-D-07).
- **Q-C-02 Lecture non partie faute de fil** (écart à la lettre de D-2, l.107, qui ne vise que la première lecture). Recommandé :
  « toute lecture planifiée partie plus de 5 s après ws + w − δ, ou non partie, dégrade l'observateur ». Motif : c'est un défaut
  de l'observateur, jamais de la source (principe l.102). À sceller avant le rodage (gel des seuils, l.115).
- **Q-C-03 Instant des sondes D-3, D-4 et D-5.** Recommandé : lancées à ws + w − δ en parallèle des lectures, sur un pool de fils
  distinct, jointes avant l'échéance. Elles décrivent alors le réseau au moment même des lectures [inféré]. Valeur scellée.
- **Q-C-04 Deux journaux par observateur** : pool d'un côté ; secondaire de l'autre, avec la carte et le relevé ASN. Recommandé :
  oui. Un seul écrivain par journal, le relevé ASN hors du fil du pool.
- **Q-C-05 Fixtures neuves.** Recommandé :
  - capture hors campagne depuis l'hôte de session, par le proxy, avec octets, date et sha256 consignés ;
  - pour les hôtes inaccessibles (Binance, Bybit), une fixture de forme documentée marquée « synthétique », recapturée par le
    smoke du premier observateur avant le gel, et relue en G2 ;
  - jamais un prix de campagne.
- **Q-C-06 Gel du collecteur avant le début du rodage.** Recommandé : oui. Toute correction après le début du rodage entraîne la
  reconstruction des quatre observateurs et un rodage refait d'au moins 7 jours, dont un week-end (règle des remplaçants, l.224).
  Le rodage décrit ainsi le code scellé.
- **Q-C-07 Réponse acceptée à la q. 10.** Recommandation de l'orchestrateur, acceptée en bloc par l'investisseur (« Toutes
  acceptées (Recommandé) »), texte recopié au JOURNAL l.382 : « USDC : les deux mesures, contre le dollar réel et telle que la
  DeFi la consomme, avec leur écart ». Sa traduction technique est absente de l'ADR [abs] : quelles formes de
  requête pour « telle que la DeFi la consomme », et quelle sortie pour « leur écart » ? À trancher avant le gel de `formes.json`
  et de la liste hors décision (advisor STATS).
- **Q-C-08 Réponse acceptée à la q. 12** (même forme, JOURNAL l.382) : « accès gratuits sans clé avec remplaçants écrits
  d'avance ». Recommandé :
  - une liste fermée de remplaçants par unité, au paquet ;
  - leurs décodeurs au collecteur dès le gel, lus par le processus secondaire, hors du vote ;
  - une bascule possible avant le sceau seulement, avec rodage refait selon Q-C-06.
- **Q-C-09 Liste fermée de la carte et date de coupure.** Les licences sont lues par un lecteur `claude-sonnet-5-5` avant chaque
  lot CB-14. Les sources non prêtes à la coupure attendent l'après-rendu (AQT Q1).
- **Q-C-10 Budget OKX.** Faut-il regrouper OKX (`/market/tickers`) si une sixième forme s'ajoute ?
- **Q-C-11 SHOGEN-ENTRELACEMENT-D5-1** (l.798, déclencheur : G0 du collecteur de S2-bis). Pour S2-bis, fermeture par
  construction : verrou exclusif (E-C-16), plus la chaîne, qui rend visible toute écriture entrelacée (E-C-18). La qualification
  sur les journaux de S2 est hors de portée d'un worker (`*.jsonl` interdits). Si l'orchestrateur la veut, c'est un lot d'après
  pré-enregistrement de S2, à `f35a70c`.
- **Q-C-12 SHOGEN-COLLECTOR-FISHER-1** (l.186). Le collecteur réécrit ne porte pas la ligne, et `collector.py` reste inchangé en
  quarantaine. Faut-il fermer l'item « sans objet », ou le re-dater à la fin de la quarantaine ?
- **Q-C-13 Lieu de l'outil de rodage** : CB-19, ou G0 du lot RODAGE ?
- **Q-C-14 Contexte des décodeurs.** Recommandé : le contexte complet de `r1.contexte_decimal` (précision 50, `ROUND_HALF_EVEN`,
  Emin et Emax, pièges ; `r1.py` l.62-68 [lu]), recopié sans import (frontière). Égalité testée côté `recalc`.
- **Q-C-15 Résultats tardifs.** Recommandé : jetés, comptés et leur latence journalisée dans la santé suivante, jamais un
  enregistrement de lecture.
- **Q-C-16 SHOGEN-COLLECT-PREVWS-1** (l.41). Sa définition est dans une pièce interdite (annexe B, en-tête ; D.2), non lue, et
  l'item est « non qualifiable en session cloud » (`docs/11` l.862). Ce G0 ne le qualifie pas. Le collecteur réécrit journalise
  la cause de toute fenêtre sans marqueur (E-C-22), quelle qu'elle soit. La requalification reste à l'orchestrateur.

### 2.7 Actes de l'investisseur

Aucun pendant ce lot, hors son accord pour les parties P1 et P2 (§8, A-1).

## 3. RECALC-BIS

### 3.1 Périmètre

**Modules à créer** (`s2bis/shogen_s2bis/recalc/`, `s2bis/tools/`) :

| module | contenu |
|---|---|
| `config_analyse.py` | schéma et contrôle des paramètres d'analyse scellés : τ et σ par (actif, classe de source), seuils de D-2 à D-5, n_s, T_max, R, seuil entier 99, gardes, tolérance des événements, seuil et grille de P_j, ordre des unités |
| `lecteur.py` | lecture en flux, contrôle de la chaîne, segments de reprise, ruptures, entiers longs |
| `fusion.py` | parcours fenêtre par fenêtre des journaux des quatre observateurs ; concordance de `run_params` ; re-décodage |
| `validite.py` | D-1 à D-5, M_j, q_j, censure par cause, T_début, strates, n_s premières fenêtres évaluables, n′_s |
| `consolidation.py` | e(o, u, j) par classe, lectures groupées, « borné », vote tout axe, écarts d'observateur, désaccords, `ok` consolidé, D1-bis, flux presque mort ; table compacte des votes |
| `rotation.py` | masques de bits, suite comprimée, décalages, K^(r), C_s, K_crit, K̄_rot, S, C_S, S_crit |
| `regle.py` | R1-2 : garde d'information, runs, valeurs, BTC, séquence d'ETH, F3, nommage, drapeau 2 |
| `etat.py` | variable d'état P_j et descriptifs des stables |
| `horsdecision.py` | sorties hors décision |
| `sensibilites.py` | (i) à (viii) |
| `r2bis.py` | R2 multi-points de vue, devise, R3 |
| `carte.py` | rendu descriptif de la carte |
| `rendu.py` | texte du rapport |
| `recompute.py` | oracle tiers, JSON |
| `oracle_indep.py` | lecteur indépendant |
| `tools/rendu_unique_bis.py` | exécution unique |

S'y ajoutent : `s2bis/config/analyse.json` (gabarit ; valeurs fixées au paquet) et les tests.

**Réutilisé ou réécrit** :

| S2 (chemin de recalcul, D6 (ii)) | S2-bis | motif |
|---|---|---|
| `window.window_start`, `window_end`, `strate_from_spec`, `verify_markers_against_spec` | **importés** | grille et calendrier inchangés (ADR l.194) |
| `r1.classify_ecart` | **importé**, appelé par (observateur, classe) avec les tables de la classe | ADR l.91 ; l.95 (iv) ; l.98 ; l.231 |
| `r1._median`, `contexte_decimal`, `DECIMAL_PREC` | **importés** | même médiane que `classify_ecart` pour la classe « borné », jamais une seconde implémentation |
| `r1.poisson_binomial`, `gate_value`, `insufficient_history`, `z_score`, `block_long_run_variance`, `bloc_strate`, `z_pool_stratifie` | **importés** | z_s, z_bloc, FIV et strate poolée hors décision (ADR l.199 ; l.210) |
| `lm.pairwise_second_moment`, `lm.phi_coefficient` | **importés** | L&M hors décision ; `compute_lm` lit le format de S2 |
| `r2._asn_state`, `r2._UnionFind` | **importés** | concordance RIPEstat et Cymru, partition |
| `r2.compute_partition` | **réécrit** (`r2bis`) | règle de fusion à deux observateurs au moins, union et intersection, stabilité (ADR l.247) |
| `r2.compute_content` | **question** (Q-R-06) | l'axe contenu de S2-bis n'est pas défini |
| `records.effective_run_params` | **importé**, avec la liste des clés porteuses de S2-bis | concordance entre démarrages |
| `records.read_jsonl_tolerant`, `parse_control`, `r1.parse_journal`, `filtre_lecture`, `t_fin_n_fixe` | **non réutilisés** | format de S2 ; lecture du fichier entier en mémoire (`records.py` l.92, `f.read().splitlines()`), incompatible avec les volumes annoncés (ADR l.279 : environ 17 Go par observateur et par mois) |
| `r1.compute_r1`, `regle_critere`, `fenetres_sautees*` | **non réutilisés** | règle R1-1 de S2 |
| `report.py` | **non réutilisé** tel quel ; conventions reprises (`_fmt_dec`, étiquettes) | blocs de S2 ; S2-bis a d'autres sorties (ADR l.197, l.210) |
| `tools/rendu_unique.py` | **calqué** dans un script neuf (Q-R-09) | constantes et chemins de S2 (l.24-53 du script) ; sommes sur plusieurs fichiers quotidiens |
| `tools/oracle_record.py` | réutilisé s'il accepte une liste de commandes en paramètre, sinon copie adaptée (Q-R-09) | liste fermée de commandes propre à S2 (l.31-34) |

Écart de vocabulaire signalé (Q-R-12) : l'ADR l.231 dit que `records` et `report` sont « réutilisés ». En pratique, seules leurs
fonctions pures et leurs conventions le sont. Lecteur et rendu sont neufs.

### 3.2 Exigences

| n° | exigence (testable) | rattachement |
|---|---|---|
| E-R-01 | Lecteur en flux, à mémoire bornée indépendante de la longueur des journaux. Chaîne contrôlée (`seq`, `prec`) dans chaque fichier et d'un fichier au suivant. Segments de reprise déclarés admis. Queue tronquée tolérée seulement si une reprise la déclare, ou en fin du dernier fichier. Entier JSON trop long : refus nommé | l.238 ; l.279 ; SHOGEN-TORN-LINE-UTF8-1 ; SHOGEN-JSON-ENTIER-LONG-1 (l.762) |
| E-R-02 | Politique scellée de rupture de chaîne (Q-R-03) | [inféré] ; principe de SHOGEN-RAW-FIN-1 (l.354) |
| E-R-03 | Octets bruts re-décodés par les décodeurs scellés ; égalité exigée avec la valeur journalisée ; verdict imprimé | SHOGEN-RAW-REDECODAGE-1 (l.355) |
| E-R-04 | Concordance des clés porteuses de `run_params` par observateur. Commit et sha256 des configurations égaux à ceux du paquet, sinon refus nommé avant tout calcul | l.217 ; l.219 ; SHOGEN-R2-RUNPARAMS-CONCORDANCE-1 (l.659) |
| E-R-05 | Observateur valide dans j : marqueur présent et non dégradé, aux seuils scellés : D-2 > 5 s ; D-3 > 1 s, ou « Not synchronised », ou aucun relevé de moins de 120 s ; D-4 au moins 2 témoins sur 3 sans réponse en 2 s ; D-5 2 noms sur 2 en échec | l.90 ; l.106-110 |
| E-R-06 | M_j, q_j = ⌊M_j/2⌋ + 1. Fenêtre évaluable si et seulement si M_j ≥ 2 ; sinon censurée et comptée par strate et par cause (absence, D-2 à D-5, intégrité) | l.94 ; l.112 |
| E-R-07 | T_début calculé par le script depuis le jeton ou le go, jamais lu dans un README. Pour chaque strate : les n_s premières fenêtres évaluables dans l'ordre chronologique, arrêt à T_max. n′_s et puissance réduite imprimés ; NON ÉVALUABLE si n′_s < n_s/2 | l.113 ; l.156 ; l.216 ; D.4 b (5) |
| E-R-08 | Strates par le calendrier scellé ; strates des marqueurs contrôlées | l.194 |
| E-R-09 | e(o, u, j) par `r1.classify_ecart` sur les seules lectures de o dans la classe c : médiane leave-one-out de o, N ≥ 4 répondantes, τ et σ de (actif, classe de source) lus de la configuration scellée. Bornes contrôlées : 0,05 % ≤ τ < 2,85 % ; σ ≥ plancher. Refus nommé hors bornes, jamais d'écrêtage | l.91 ; l.98 ; l.179-181 (BTC, amendement compris) ; l.185-187 (autres actifs) |
| E-R-10 | Une requête groupée donne un relevé par (unité, classe). Sa panne vaut panne pour chaque actif du groupe | l.234 |
| E-R-11 | Classe « borné » : flux plafonné dont l'écart (staleness ou hors-enveloppe) tombe dans une fenêtre où la médiane leave-one-out de o dépasse le plafond. Ni écart ni non évaluable ; compté par (o, u) | l.98 (b) |
| E-R-12 | Vote tout axe à q_j. Le type est l'axe de plus haute précédence parmi les votes. « Non évaluable » n'est pas un vote | l.92 |
| E-R-13 | Écart d'observateur (vote sans quorum) : censuré pour R1, compté par (o, u, axe). Désaccords comptés | l.93 |
| E-R-14 | `ok` consolidé : au moins q_j observateurs valides à statut `ok` avec un prix. Règle D1-bis (a)-(c) et seuil de flux presque mort 2·ok(u, s) < n_s (ou n′_s), par classe | l.168 ; l.171 |
| E-R-15 | Unités = noms d'hôte de configuration ; `okx_index` lu et journalisé, hors R1. Unité non décalée : le premier hôte du pool BTC D1-bis de la strate | l.166 ; l.198 |
| E-R-16 | Suite comprimée des fenêtres évaluables retenues, commune aux classes. D(u, ·) en entier-masque. Décalage circulaire de o(r, u) positions, avec o(r, u) = entier big-endian de SHA-256(graine ‖ « : » ‖ strate ‖ « : » ‖ r ‖ « : » ‖ u) mod n_s (ou n′_s). Décalage joint par hôte, indépendant de la classe. R = 9 999. Encodage des octets et sens du décalage : Q-R-02 | l.137 ; l.139 ; l.198 |
| E-R-17 | K_s, K_s^(r), C_s, K_crit,s et K̄_rot,s en entiers et rationnels exacts ; décision par C_s ≤ 99 | l.198 ; l.200 |
| E-R-18 | S = Σ_j C(m_j, 2), C_S, S_crit et S̄_rot sur les mêmes rotations, imprimés après le verdict avec la phrase scellée | l.210 ; AQT Q5 |
| E-R-19 | Graine = sha256 des octets du manifeste scellé, calculée par le script ; le README du sceau n'est qu'imprimé et comparé | l.198 ; D.4 c |
| E-R-20 | Strate testable si et seulement si : au moins 2 unités avec un écart consolidé au moins, K_crit,s ≥ 2, au moins 2 runs de I_t parmi les fenêtres K (axe : Q-R-01), et n′_s ≥ n_s/2. Valeurs REJETTE, NE REJETTE PAS, NON ÉVALUABLE (« information insuffisante ») ; loi de rotation imprimée en entier si non évaluable | l.201 |
| E-R-21 | « R1 discrimine (S2-bis) » sur BTC seul ; m imprimé. ETH en séquence fixe (NON TESTÉ (séquence) sinon). F3 étiquetée « exploratoire, hors décision », sans phrase du registre | l.202 ; l.208-209 |
| E-R-22 | Énoncés scellés imprimés mot pour mot. Excès critique et puissance à la cellule cible imprimés | l.204-209 |
| E-R-23 | Drapeau 2 (BTC) | l.211 |
| E-R-24 | Entrées imprimées par classe : liste du pt 1 | l.197 |
| E-R-25 | Variable d'état : P_j(o) = |médiane du témoin − 1| quand o a au moins 2 lectures `ok` du témoin. Vote binaire à q_j sur P_j(o) > 0,5 %, grille {0,25 ; 0,5 ; 1 ; 2} %. État « indéterminé » s'il y a moins de 2 votants ; fractions imprimées par strate. Analyse conditionnelle d'USDC/USD et d'USDT/USD sur les fenêtres en décrochage (Q-R-11). Écart au pair des classes USD (Q-R-04). Comptes « borné ». Co-occurrence USDT | l.210 ; AQT Q4 ; l.463 (q. 4 c) |
| E-R-26 | z_s avec sa garde, z_bloc (ℓ = 240) et FIV, par les fonctions de `r1` | l.199 |
| E-R-27 | Imprimés hors décision : R1 par observateur ; écarts d'observateur et désaccords ; matrice de co-défaillance des observateurs (définition : Q-R-05) ; distribution de M_j ; strate poolée ; L&M ; compte d'événements (tolérance : Q-R-05) et sa loi ; co-écart inter-classe par hôte | l.210 |
| E-R-28 | Sensibilités (i) à (viii), liste fermée. (iii) : décalages multiples de 1 440 positions ; (viii) : Westfall-Young min-P (formules : Q-R-05) | l.210 |
| E-R-29 | Partition R2 : pour chaque observateur valide, dernier relevé par hôte à la date de partition, concordant (`_asn_state`). Fusion si au moins 2 observateurs mesurent le même ASN pour les deux hôtes. Union et intersection en sensibilités ; jours de stabilité ; k_eff pour k nominal = 10. Relevés partiels et en échec traités explicitement ; hôtes hors pool étiquetés | l.247 ; ASN-DIVERGENCE-PARTIELLE-1 (l.641), -ECHEC-1 (l.597), ASN-STATUT-1 (l.173), -HORS-POOL-1 (l.642) |
| E-R-30 | Axe de devise : partition par classe. Appartenance déclarée aux amonts : rang R3, ne fusionne pas | l.248 |
| E-R-31 | Carte servie au rendu unique (Q-R-07). Par source : racines déclarées, hébergeur et ASN mesurés depuis chaque observateur, devise, cadence ; co-écarts descriptifs. Aucune entrée dans K, p̂_u ni la décision | l.254-260 |
| E-R-32 | Texte et JSON produits depuis une même structure. Points d'entrée `recompute_*` (oracle tiers). Deux exécutions donnent les mêmes octets | l.231 ; analogue de l'identité bit à bit demandée au lot 4 (l.382) |
| E-R-33 | Lecteur indépendant, écrit par un autre auteur, sans import du lecteur principal. Il recalcule pour BTC n_s, K_s et C_s ; verdict de concordance imprimé (Q-R-08) | SHOGEN-LECTEUR-INDEP-1 (l.802) ; `docs/11` l.901 |
| E-R-34 | Exécution unique en refus par défaut, gardes de la forme de D.4 b : (bloc) ; (1) sha du paquet au JOURNAL ; (2) code d'analyse égal au commit scellé (`s2bis/` et `s2-harness/shogen_s2`) ; (3) sha des fichiers de journaux égaux aux sommes de clôture ; (4) sha du script ; (5) délai ; (6) acte de l'investisseur. Si une garde refuse, rien n'est écrit. Enregistrement d'oracle produit | l.219 ; D.4 b |
| E-R-35 | Aucun regard intermédiaire : aucune commande ne calcule K, z ni un statut avant le rendu unique (`status` excepté, qui n'en calcule pas) | l.158 |
| E-R-36 | Tests sur journaux synthétiques produits par l'écrivain de CB-1. Valeurs de référence indépendantes du code ; échec montré avant correction | règle 4 ; D.4-bis |

### 3.3 Sous-lots (tailles [inféré])

| sous-lot | objet | taille | dépend de |
|---|---|---|---|
| RB-0 | `config_analyse.py` (schéma, bornes, refus nommés) | ≈ 150 | CB-0 |
| RB-1 | lecteur en flux (chaîne, reprises, ruptures, entiers longs, mémoire bornée) | ≈ 190 | CB-2 (format) |
| RB-2 | fusion des quatre observateurs, `run_params`, commit et configurations, re-décodage | ≈ 190 | RB-1, CB-6 à CB-9 |
| RB-3 | validité, M_j, censure, T_début, strates, n_s, n′_s | ≈ 180 | RB-2 |
| RB-4 | e(o, u, j) par classe, groupés, « borné » | ≈ 180 | RB-3 |
| RB-5 | vote, écarts d'observateur, désaccords, `ok` consolidé, D1-bis, table compacte des votes | ≈ 190 | RB-4 |
| RB-6 | rotation (masques, décalages, K^(r), C, K_crit, K̄, S) avec vecteurs indépendants | ≈ 190 | RB-0 |
| RB-7 | règle R1-2 (garde, runs, valeurs, séquence d'ETH, F3, nommage, drapeau 2) | ≈ 190 | RB-5, RB-6 |
| RB-8 | variable d'état, analyse conditionnelle, descriptifs des stables | ≈ 180 | RB-5, RB-6 |
| RB-9 | hors décision I (z_s, z_bloc, FIV, M_j, strate poolée, L&M) | ≈ 170 | RB-5 |
| RB-10 | hors décision II (R1 par observateur, matrice, événements, co-écart inter-classe) | ≈ 190 | RB-5, RB-6 |
| RB-11 | sensibilités (i) à (vi) | ≈ 180 | RB-7 |
| RB-12 | sensibilités (vii) et (viii) | ≈ 170 | RB-7 |
| RB-13 | R2 multi-points de vue, devise, R3 | ≈ 200 | RB-2 |
| RB-14 | carte (rendu descriptif) | ≈ 150 | RB-2 |
| RB-15 | rendu I (en-tête, entrées, verdict, énoncés scellés) | ≈ 190 | RB-7, RB-8 |
| RB-16 | rendu II (hors décision, sensibilités, R2, carte) | ≈ 190 | RB-9 à RB-14 |
| RB-17 | `recompute_*` (JSON), déterminisme à l'octet | ≈ 150 | RB-15, RB-16 |
| RB-18 | lecteur indépendant (autre auteur) | ≈ 180 | RB-1 (format seulement) |
| RB-19 | exécution unique I (bloc machine, gardes (1) à (6), refus sans écriture) | ≈ 200 | RB-17 |
| RB-20 | exécution unique II (table des sorties, enregistrement d'oracle, écriture atomique) | ≈ 190 | RB-19 |

Total : environ 3 800 lignes avec tests [inféré]. Pour comparaison, l'ADR l.308 donne environ 800 lignes (600 plus 200). Base de
l'écart : le chemin de recalcul de S2 compte environ 3 570 lignes de code dans les modules et 783 dans `tools/` [mesuré, `wc -l`].

### 3.4 Tests attendus et mutants obligatoires

- **Lecteur** :
  - rupture de chaîne détectée (M : contrôle sauté) ;
  - queue tronquée admise seulement si déclarée ;
  - mémoire : pic mesuré par `tracemalloc` sur deux journaux synthétiques de tailles 1 et 4 ; le pic ne croît pas avec la taille
    (M : lecture du fichier entier) ;
  - entier long : refus nommé.
- **Re-décodage.** Écart signalé (M : comparaison du seul sha).
- **Validité.** Bornes exactes de chaque seuil : 5 s, 1 s, statut, 120 s, 2 sur 3, 2 sur 2, 2 s (un mutant `>` contre `≥` par
  borne).
- **Quorum.** q_j pour M_j = 2, 3 et 4 (M : q fixé à 2 ; M : ⌈M_j/2⌉). Censure par cause comptée.
- **Consolidation** :
  - vote tout axe et précédence ;
  - « non évaluable » n'est pas un vote (M) ;
  - « borné » strict au-dessus de 1,05 (M : `≥`) ;
  - panne de requête groupée propagée à chaque actif.
- **D1-bis.** Borne 2·ok = n_s (M : `≤`).
- **Rotation** :
  - o(r, u) contre des vecteurs calculés hors du code, avec `sha256sum` sur la chaîne d'entrée et une conversion d'entier par un
    outil distinct ;
  - K^(r) par masques égal à un comptage naïf position par position (essais aléatoires sur petites séries) ;
  - C_s, K_crit (≤ 99) et K̄_rot sur un exemple fait à la main ;
  - mutants : classe dans l'entrée du hachage ; première unité décalée ; modulo n_s au lieu de n′_s ; sens du décalage inversé ;
    R = 9 998 ; `≥` contre `>` dans C_s ;
  - S égal à la somme naïve des paires.
- **Règle** :
  - C_s = 99 et 100 (M : `< 99`) ;
  - K_crit ≥ 2 (M : ≥ 1) ;
  - deux runs (M : un run) ;
  - n′_s ≥ n_s/2 (M : `>`) ;
  - ETH testé seulement si BTC rejette (M) ;
  - F3 sans phrase du registre (M) ;
  - « R1 discrimine » sur BTC seul (M : ETH inclus).
- **Variable d'état.** Moins de 2 votants donne « indéterminé ». Au moins 2 lectures `ok` du témoin (M : 1). Seuil strict.
  Sous-suite des fenêtres en décrochage.
- **Hors décision.** z_s, z_bloc et FIV égaux aux fonctions de `r1` sur la même série. Chaque statistique a son exemple fait à
  la main.
- **Sensibilités.** Chacune ne change que son paramètre (un mutant par sensibilité).
- **R2** :
  - fusion à 2 observateurs (M : union ; M : intersection) ;
  - un relevé partiel ne publie pas de divergence (DIVERGENCE-PARTIELLE-1) ;
  - un relevé en échec est exclu et compté ;
  - les hôtes hors pool sont étiquetés.
- **Rendu.** Phrases scellées dorées. Mêmes octets sur deux exécutions avec des `PYTHONHASHSEED` différents (M : itération sur
  un ensemble).
- **Oracle.** JSON égal aux valeurs rendues. Lecteur indépendant concordant. Test de frontière : le lecteur indépendant n'importe
  pas le principal (M).
- **Exécution unique.** Chaque garde a sa fixture de refus et son mutant, comme le RENDU-1 de S2 :
  - aucune sortie écrite sur refus ;
  - graine et T_début calculés, jamais lus (M : lecture du README) ;
  - « ni jeton vérifié ni go épinglé » donne une sortie non nulle.

### 3.5 Critères de sortie

1. Mêmes critères par sous-lot et par partie que COLLECTE-BIS (P3, P4).
2. **Lot** :
   - `recompute_*` et rendu concordants ;
   - lecteur indépendant concordant sur toutes les fixtures ;
   - exécution unique refusée sur chaque fixture de refus ;
   - deux exécutions identiques à l'octet ;
   - commit candidat au sceau consigné ;
   - items fermés ou re-datés : LECTEUR-INDEP-1 (pour S2-bis), RAW-REDECODAGE-1, FORMAT-JOURNAUX (analogue S2-bis) ;
   - q. 4 (c) tranchée (Q-R-04).
3. **G0** : cp-1 bref de ce G0, comme pour COLLECTE-BIS.
4. **G7** : à la clôture de S2-bis.

### 3.6 Risques et questions techniques

**Risques** :
- La charge de G2 est forte (environ 3 800 lignes en deux parties).
- Le coût de calcul est à mesurer. R = 9 999 rotations, quatre classes, deux strates et huit sensibilités font environ 640 000
  passes, chacune d'une dizaine d'opérations sur entiers de 110 000 bits [calc]. C'est de l'ordre de la minute [inféré], à
  mesurer en RB-6.
- Les entrées viennent d'autres lots : n_s, T_max et la tolérance des événements (SIM-BIS) ; τ et σ (PLAN-S2BIS, CALIB-ACTIFS) ;
  un critère collectif d'absorption éventuel (SHOGEN-FLUX-ABSORPTION-COLLECTIVE-1, l.872, déclencheur « pré-enregistrement de
  S2-bis » ; SHOGEN-FLUX-SERIEL-1, l.873).

**Questions** (adjudication : orchestrateur ; advisor STATS désigné) :
- **Q-R-01 Axe des runs de I_t pour la garde d'information** (pt 5, l.201 : non précisé). Recommandé : sur la **suite comprimée**.
  Motif [inféré] : une perte de quorum au milieu d'un incident commun le couperait en deux runs sur la grille UTC, et un épisode
  unique passerait la garde que l'avis STATS Q11 veut lui opposer. La forme de `r1.bloc_strate` (la grille) reste celle de z_bloc
  hors décision.
- **Q-R-02 Entrée de SHA-256 et sens du décalage** (l.198). Recommandé :
  - octets UTF-8 de la chaîne ASCII `<graine en 64 hexadécimaux minuscules>:<strate>:<r décimal>:<u>` ;
  - u = nom d'hôte de configuration ;
  - position t envoyée en (t + o) mod n.
  À sceller au paquet avec trois vecteurs de test.
- **Q-R-03 Rupture de chaîne.** Recommandé : un tronçon non intègre vaut absence (D-1) pour les fenêtres qu'il couvre, avec la
  cause « intégrité ». Ces fenêtres sont comptées, le verdict de chaîne est imprimé, rien n'est jamais réparé. Règle scellée ; la
  forme suit SHOGEN-RAW-FIN-1.
- **Q-R-04 Q. 4 (c) de l'ADR** (l.463), à confirmer à ce G0 : P_j par classe USD en descriptif. Recommandé : oui. C'est
  « l'écart au pair des médianes des classes USD » du pt 9, construit comme le témoin (vote binaire à q_j, au moins 2 lectures
  `ok` de la classe). Il ne sert jamais à choisir des fenêtres, puisqu'il lit les données testées (AQT Q4 pt 3).
- **Q-R-05 Définitions à sceller avant le gel** :
  - matrice de co-défaillance. Recommandé : par paire (o, o′), fenêtres où les deux sont non valides, et fenêtres où les deux
    votent panne pour toutes les unités ;
  - tolérance du compte d'événements (SIM-BIS ou PLAN-S2BIS) ;
  - décalages de (iii). Recommandé : 1 440 × (h mod ⌊n_s/1 440⌋), h tiré comme o(r, u) ;
  - formule de (viii), Westfall-Young min-P en une étape. La source primaire n'est pas détenue : elle n'est citée que via la FDA,
    au second degré (P6 C6).
- **Q-R-06 Axe contenu de R2 en S2-bis.** Les statistiques de `r2.compute_content` sont-elles calculées par observateur ? Avec
  quelle règle de fusion ? Le passage de R3 à R2 « par une corrélation de contenu mesurée » (l.248) suppose ce calcul ; l'ADR ne
  le définit pas [abs]. Advisor STATS.
- **Q-R-07 Rendu de la carte dans RECALC-BIS** (RB-14) : à confirmer. La carte est « servie au rendu unique » (l.259), mais
  l'ADR §6 lot 5 ne nomme que la collecte de la carte.
- **Q-R-08 Lecteur indépendant.** Recommandé : un autre worker l'écrit. Son verdict est imprimé sans fermer l'exécution (forme de
  SHOGEN-RAW-FIN-1).
- **Q-R-09 Script d'exécution unique.** Recommandé : un script neuf, calqué sur celui de S2. Le script de S2 reste tel qu'il est
  scellé à `f35a70c`. L'enregistreur est réutilisé si sa liste de commandes peut se passer en paramètre, sans toucher son
  comportement pour S2 ; sinon, copie adaptée.
- **Q-R-10** : si SIM-BIS ou le paquet adopte un critère collectif d'absorption, il entre à RB-5 avant le gel du recalcul.
- **Q-R-11 Analyse conditionnelle.** Recommandé : rotation sur la sous-suite comprimée des fenêtres en décrochage, avec les mêmes
  décalages.
- **Q-R-12 Sens de « réutilisé »** pour `records` et `report` (l.231) : précision demandée, sans changer la décision (§3.1).
- **Q-R-13 Règle exacte de T_début.** L'ADR fixe T_début ≥ genTime du jeton + 24 h, et un go écrit de l'investisseur (l.216).
  Proposé : premier `window_start` ≥ max(genTime + 24 h, heure du commit qui épingle le go). Le script la calcule et la compare
  au README du sceau. À sceller au paquet.

### 3.7 Actes de l'investisseur

Aucun pendant ce lot, hors son accord pour P3 et P4 (A-1). Le go de l'exécution unique relève du lot 11.

## 4. DEPLOI-BIS

### 4.1 Périmètre

Fichiers à créer :
- `s2bis/deploi/premier-demarrage.sh` : script cloud-init sous forme de script shell, unique pour les quatre observateurs. Les
  paramètres d'observateur sont en tête. Un mode d'essai écrit sur une racine factice, sans privilège et sans réseau.
- `s2bis/deploi/chrony.conf`, `nftables.conf`, `unbound.conf` (pour O1), modèles de résolveur pour O2 à O4.
- `s2bis/deploi/systemd/` :
  - `shogen-pool.service`, `shogen-secondaire.service` ;
  - minuteries de sauvegarde horaire, de signal de vie toutes les 5 min, de jeton quotidien et d'échange des têtes.
- `s2bis/deploi/outils/` : sauvegarde et rétention locale, signal de vie, alerte disque. Bibliothèque standard ou commandes de base.
- Les tests de ces fichiers.
- Documents, hors compte :
  - `docs/adr-0029/s2bis/PROCEDURE-INTERVENTION.md` (langage clair) et le gabarit `interventions.md` ;
  - les entrées de `docs/17-modele-de-menace.md` et de `docs/08-assumptions.md` (l.428) ;
  - le contrôle R-8 des paquets système dans `docs/R-8-outillage.md`.

Réutilisé : rien du harnais de S2. La tâche `schtasks`, le `.bat` et le watchdog sont remplacés par systemd (RUNBOOK l.62-65 ;
SHOGEN-TASK-72H-1, l.30 ; SHOGEN-SCHED-MONITOR-1, l.31). Les outils de sceau de S2 (`scripts/sceau/verify.sh`) servent de modèle
au contrôle des jetons quotidiens.

### 4.2 Exigences

| n° | exigence (testable) | rattachement |
|---|---|---|
| E-D-01 | Un script unique, versionné. Paramètres d'observateur en tête : identité o, fournisseur, région, famille de résolveur, adresses de surveillance et de sauvegarde. Ces adresses sont collées par l'investisseur et ne sont jamais versées | l.241 ; l.243 |
| E-D-02 | Rejouable mesuré : empreintes de configuration égales sur quatre jeux de paramètres, hors paramètres d'observateur | l.241 |
| E-D-03 | Utilisateur dédié sans droits d'administration pour les services. SSH entrant par clé seule ; ni root ni mot de passe | l.241 ; l.243 |
| E-D-04 | Paquets système de la distribution : chrony, unbound (O1), rsync, outil de pare-feu, python3. Contrôle R-8 écrit avant toute installation ; versions au descripteur | l.246 ; SHOGEN-S2BIS-R8-PAQUETS-1 (l.441) |
| E-D-05 | Pare-feu IPv4 et IPv6, refus par défaut. Sortant : HTTPS ; DNS vers le résolveur et vers les trois témoins D-4 ; NTP vers les serveurs fixés. Entrant : SSH par clé. Précisions de Q-D-07 | l.241 ; avis OPS Q3 pt 3 |
| E-D-06 | chrony scellé : au moins 4 serveurs d'au moins 2 opérateurs ; `makestep` au démarrage seulement ; serveurs choisis selon Q-D-06. Collecteur démarré après la synchronisation ; empreinte au paquet | l.83 |
| E-D-07 | Résolveur par famille : O1 unbound récursif, O2 Quad9, O3 Google, O4 résolveur du fournisseur ; jamais 1.1.1.1. La configuration survit au redémarrage et au renouvellement DHCP ; son empreinte est journalisée (Q-D-05) | l.82 |
| E-D-08 | Code acheminé au commit scellé, sha256 contrôlé avant tout démarrage ; refus et arrêt sinon (Q-D-01) | l.241 |
| E-D-09 | Unités systemd : `Restart=always` ; ordre après la synchronisation de l'horloge ; `MemoryMax` sur le processus secondaire ; aucune limite de durée d'exécution | l.235 ; l.244 ; SHOGEN-TASK-72H-1 |
| E-D-10 | Copie horaire des fichiers vers l'espace de sauvegarde (rsync sur SSH, un sous-compte par observateur, clés générées sur l'observateur). Rétention locale bornée : suppression seulement après égalité contrôlée du sha256 distant (Q-D-02) | l.240 ; l.243 ; l.245 |
| E-D-11 | Signal de vie toutes les 5 min, alerte après 15 min de silence. Alerte disque à 80 %. Le signal ne porte aucune donnée de lecture | l.244 ; l.237 |
| E-D-12 | Mises à jour de sécurité seulement, sans redémarrage automatique ; versions au descripteur (Q-D-08) | l.241 |
| E-D-13 | Descripteur d'observateur produit au premier démarrage : ASN de l'adresse réelle mesuré par RIPEstat et Cymru, région, fournisseur, résolveur, versions, empreinte | l.79 ; l.238 |
| E-D-14 | Smoke au premier démarrage, verdict affiché à la console, sans prix | l.81 ; E-C-37 |
| E-D-15 | Régions : quatre pays distincts, aucune paire dans la même métropole, un observateur hors UE et hors États-Unis, aucun aux États-Unis. Contrôle sur les régions réelles | l.81 ; SHOGEN-S2BIS-REGIONS-1 (l.442) |
| E-D-16 | Aucun observateur sur l'ASN d'un hôte des quatre classes ou du témoin (R-c). Contrôle sur le descripteur | l.80 ; l.224 |
| E-D-17 | Procédure d'intervention N1 à N3 en langage clair, gabarit `interventions.md`, exception écrite (option c). Une reconstruction garde l'identité o et date un nouveau descripteur | l.242 ; l.244 ; l.225 |
| E-D-18 | `status` accessible à l'investisseur, sans accès d'agent (Q-D-03) | l.242 ; l.244 |
| E-D-19 | Entrées de doc 17 : fournisseur qui lit ou altère disque ou horloge ; transport et réplication des journaux ; secrets ; accès d'agent ; disque plein ; dérive par mises à jour. Registre 08 : A(observer-distinctness), A(rotation-invariance) | l.428 ; §6 lot 6 |
| E-D-20 | Support cloud-init par offre et disponibilité Hetzner établis sur pièce avant le collage | SHOGEN-S2BIS-REGIONS-1 ; SHOGEN-S2BIS-HETZNER-DISPO-1 (l.446) |
| E-D-21 | Conditions d'usage de FreeTSA lues pour un usage automatisé quotidien (P-12) ; envoi armé sous le go | l.218 ; D.4 c l.163 |
| E-D-22 | Mise en service : (a) exercice d'alerte (arrêt volontaire, courriel reçu) ; (b) restauration d'une copie ; (c) têtes échangées ; (d) un jeton reçu et contrôlé (`openssl ts -verify`). C'est la condition de fermeture de SHOGEN-UPS-1, TASK-72H-1 et SCHED-MONITOR-1 | l.244 |

### 4.3 Sous-lots (tailles [inféré])

| sous-lot | objet | taille | dépend de |
|---|---|---|---|
| DB-0 | lectures sur pièce, sans code, par un lecteur `claude-sonnet-5-5` (détail sous le tableau) | 0 | — |
| DB-1 | script I : utilisateur, paquets, pare-feu IPv4 et IPv6, SSH, mises à jour ; mode d'essai sur racine factice | ≈ 190 | DB-0 |
| DB-2 | script II : chrony, résolveur par famille, acheminement du code, descripteur, smoke | ≈ 190 | DB-1 ; CB-16, CB-18 |
| DB-3 | unités systemd et minuteries | ≈ 150 | DB-1 |
| DB-4 | sauvegarde et rétention, échange des têtes, signal de vie, alerte disque | ≈ 180 | DB-3 ; CB-15 |
| DB-5 | rejouabilité (empreintes), contrôle des régions et de R-c | ≈ 140 | DB-2 |
| DB-6 | documents, hors compte (détail sous le tableau) | — | DB-1 à DB-5 |

**DB-0, lectures sur pièce** :
- R-8 des paquets, par l'index signé du miroir officiel : `deb.debian.org` est joignable depuis la session (`InRelease` de
  trixie, HTTP 200 [mesuré]), alors que les pages du registre avaient opposé un défi anti-robot lors de la rédaction de
  l'ADR (l.246) [lu] ;
- support cloud-init par offre ;
- régions de Singapour et de Tokyo ;
- disponibilité Hetzner ;
- serveurs NTP ;
- Storage Box : sous-comptes, lecture seule, port SSH, instantanés ;
- Healthchecks : forme du signal ;
- FreeTSA : conditions d'usage.

**DB-6, documents** : procédure d'intervention, `interventions.md`, doc 17, registre 08, tableau R-8.

Total : environ 850 lignes avec tests [inféré]. Pour comparaison, l'ADR l.308 donne environ 300 lignes de script.

### 4.4 Tests attendus et mutants obligatoires

- **T-DP-1.** `bash -n`, puis le mode d'essai sur une racine factice. `apt-get` et `systemctl` sont remplacés par des
  enregistreurs ; on contrôle les fichiers produits (M : étape omise).
- **T-DP-2. Pare-feu.**
  - Refus par défaut. Sortant autorisé : exactement 443/tcp ; 53 vers le résolveur et les trois témoins (toute destination pour
    O1, récursif) ; 123/udp vers les serveurs fixés ; SSH vers l'espace de sauvegarde. Entrant : SSH seul.
  - IPv6 selon Q-D-07.
  - Mutants : tout le sortant ouvert ; un témoin oublié.
- **T-DP-3. chrony.** Au moins 4 serveurs, au moins 2 opérateurs, `makestep` borné au démarrage (M : `makestep` sans limite).
- **T-DP-4. Résolveurs.** Chaque famille selon E-D-07 ; jamais 1.1.1.1 (M : 1.1.1.1 ajouté).
- **T-DP-5. sshd.** Clé seule ; ni root ni mot de passe (M : mot de passe admis).
- **T-DP-6. Unités.** `Restart=always`, ordre après chrony, `MemoryMax`, aucune limite de durée ; minuteries présentes
  (M : `RuntimeMaxSec` ajouté ; M : `Restart` retiré).
- **T-DP-7. Rejouabilité.** Quatre jeux de paramètres donnent des empreintes communes égales (M : un paramètre d'observateur fuit
  dans un fichier commun).
- **T-DP-8. Signal de vie.** Corps vide de toute donnée (M : santé jointe).
- **T-DP-9. Mises à jour.** Sécurité seulement, redémarrage automatique désactivé (M : activé).
- **T-DP-10. Code.** Un sha256 faux arrête tout ; rien ne démarre (M : contrôle sauté).
- **T-DP-11. Rétention.** Pas de suppression locale sans égalité du sha256 distant (M : suppression avant contrôle).

### 4.5 Critères de sortie

1. **Lot commis** :
   - tests et mutants conformes, G2 de la partie P5, revue ;
   - tableau R-8 versé **avant** toute installation ;
   - entrées des docs 17 et 08 posées ;
   - procédure lue et acceptée par l'investisseur ;
   - items SHOGEN-S2BIS-R8-PAQUETS-1, REGIONS-1 et HETZNER-DISPO-1 fermés par DB-0, ou re-datés avec motif.
2. **Mise en service**, après les actes A-2 à A-7 :
   - smoke `OK` sur les quatre observateurs ;
   - régions et ASN conformes (R-c) ;
   - exercices E-D-22 réussis ;
   - items SHOGEN-UPS-1, TASK-72H-1 et SCHED-MONITOR-1 fermés ; SHOGEN-CENSURE-S2BIS-1 constaté (causes journalisées) ;
   - JOURNAL.
3. **Rodage** : il démarre ensuite (lot 8).

### 4.6 Risques et questions techniques

**Risques** :
- Capacité ou région indisponible ; géo-blocage depuis Singapour (repli à Londres, l.81) ; filtrage de l'UDP/53 révélé par D-4.
- Disque trop petit (Q-D-02).
- Indisponibilité de l'investisseur pendant une panne (absorbée par le quorum jusqu'à deux observateurs, l.367).
- Dérive de configuration par mises à jour.
- Dépendance au service d'alerte et à FreeTSA.

**Questions** (adjudication : orchestrateur ; advisor OPS désigné) :
- **Q-D-01 Acheminement du code.** Écart à la lettre de l.241, « clone le dépôt à un commit épinglé ». Le dépôt est privé (§7 de
  la passation) : un clone exige des droits de lecture sur chaque observateur. Il pose aussi sur quatre disques de tiers tout
  l'historique, y compris les dossiers interdits et la matière Pocket (`docs/15-*`, `docs/16-*`, `docs/pocket-report/`, présents
  à la tête [mesuré, noms seuls]). Recommandé : une archive `git archive <commit scellé> s2bis/` (et, si la frontière l'exige, les
  seuls fichiers de `s2-harness` utiles), déposée sur l'espace de sauvegarde. Le script en contrôle le sha256, qui est écrit au
  paquet.
- **Q-D-02 Volume et rétention** :
  - l'ADR l.279 annonce environ 17 Go par observateur et par mois, marge de deux comprise [lu]. Les disques de base de
    DigitalOcean et de Linode font 25 Go (l.287, l.289) [lu]. À ce rythme, ils sont pleins en 1,5 mois environ, sans compter le
    système [calc] ;
  - une extrapolation depuis S2 donne un autre ordre de grandeur : 395 Mo pour 38 600 fenêtres (l.296) font 10,2 Ko par fenêtre,
    soit 0,44 Go par mois et environ 1,8 Go par mois pour quatre classes, carte non comprise [calc ; ×4 inféré] ;
  - « quatre copies par réplication entre observateurs » (l.245) est intenable sur ces disques au volume de l'ADR.

  Recommandé : rétention locale de N jours après copie contrôlée ; réplication par l'espace de sauvegarde seul ; volume mesuré au
  rodage (lecture admise, l.221) ; disque revu s'il le faut, ce qui est un acte de l'investisseur et un coût.
- **Q-D-03 Échange des têtes et `status` à quatre observateurs.** Le compte de fenêtres évaluables demande la santé des quatre
  observateurs. Recommandé :
  - chaque observateur dépose sa tête et un résumé de santé (validité par fenêtre, aucun statut de source) dans son dossier de
    l'espace de sauvegarde, et lit ceux des autres ;
  - `status` tourne sur n'importe quel observateur.

  À établir sur pièce : la Storage Box permet-elle une lecture croisée entre sous-comptes ? Sinon, `status` tourne chez
  l'investisseur, sur une copie des seuls résumés.
- **Q-D-04 Système et version de Python, identiques sur les quatre images.** Recommandé : Debian stable, version et paquets
  établis à DB-0. Python au moins 3.10 si le recalcul doit pouvoir tourner aussi sur un observateur (`int.bit_count`) [inféré].
- **Q-D-05 Résolveur épinglé.** Option 1 : `resolv.conf` immuable ou systemd-resolved fixé. Option 2 : unbound local partout,
  récursif sur O1 et en relais vers la famille sur O2 à O4 (un cache local qui respecte les TTL ; D-5 en tient compte).
  Avis OPS demandé.
- **Q-D-06 Serveurs NTP.** Liste fixée au G0. Aucun serveur sur un ASN du pool. Pas de mélange de serveurs qui lissent la seconde
  intercalaire avec des serveurs qui ne la lissent pas [inféré, à lire sur pièce à DB-0].
- **Q-D-07 Précisions au pare-feu de l.241** : SSH sortant vers l'espace de sauvegarde ; DNS sortant vers toute autorité pour O1
  (récursion) ; IPv6 refusé, ou soumis à la même politique ; NTP vers les seuls serveurs fixés.
- **Q-D-08 Redémarrages.** Les mises à jour sans redémarrage automatique (l.241) laissent des noyaux en attente. Recommandé : un
  redémarrage N2 par l'investisseur, observateur par observateur, jamais deux à la fois, consigné.
- **Q-D-09 Exercices de mise en service avant la fermeture des items de l.244.** Recommandé : oui (E-D-22).
- **Q-D-10 OpenTimestamps.** Hors de ces lots, pour mémoire. La réponse acceptée à la q. 7 ne nomme que l'horodatage quotidien
  FreeTSA (JOURNAL l.382), alors que la q. 7 posait aussi la question d'OpenTimestamps (l.405). C'est à poser au lot PAQUET-S2BIS.

### 4.7 Actes de l'investisseur

Voir §8, A-2 à A-11.

## 5. Parties, ordre et chemin critique

| partie | sous-lots | taille [inféré] | relecture | accord |
|---|---|---|---|---|
| P1 — collecteur, noyau | CB-0 à CB-5, CB-10, CB-11, CB-18 | ≈ 1 620 | une G2 neuve | investisseur |
| P2 — collecteur, contenus | CB-6 à CB-9, CB-12 à CB-17 (et CB-19) | ≈ 1 860 à 2 370 | une G2 neuve | investisseur |
| P3 — recalcul, moteur | RB-0 à RB-8 | ≈ 1 640 | une G2 neuve | investisseur |
| P4 — recalcul, sorties et exécution unique | RB-9 à RB-20 | ≈ 2 160 | une G2 neuve | investisseur |
| P5 — déploiement | DB-0 à DB-6 | ≈ 850 | une G2 neuve | investisseur |

**Ordre et chemin critique** :
- **Collecte et déploiement**, dans l'ordre : P1, puis P2, puis le gel du collecteur (Q-C-06), puis P5 et la mise en service,
  puis le rodage (14 jours), puis le sceau.
- **Recalcul**, en parallèle : P3 puis P4, finis avant le sceau, car le commit du recalcul est scellé (l.217).
- **Entrées attendues** :
  - G0 de CALIB-ACTIFS (paires servies, avant CB-7 et CB-8) ;
  - adresses du témoin lues sur pièce (avant CB-9) ;
  - licences du pool et de la carte (avant le gel ; SHOGEN-S2BIS-LICENCES-API-1) ;
  - SIM-BIS (n_s, T_max, tolérance) et PLAN-S2BIS ou CALIB-ACTIFS (τ, σ), pour la configuration scellée et non pour le code.

**Q-G-02.** Le G0 de vague fait dépendre COLLECTE-BIS et RECALC-BIS de SIM-BIS (`G0-lots-S2BIS.md` l.17). Aucune sortie de
SIM-BIS n'entre au code ; seule la configuration scellée l'attend. Recommandé : démarrer P1 et P3 sans attendre SIM-BIS. Le
chemin critique est la collecte, pas le calcul.

**Q-G-04 Taille et jalons.** Environ 8 100 à 8 600 lignes avec tests [inféré], contre environ 2 100 à 2 600 lignes dans l'ADR
l.308 pour ces trois lots, carte non chiffrée. Le jalon « S+0 à S+5 lots 3 à 6 commis et revus » (l.393) suppose environ 9 à
10 sous-lots et une relecture par semaine sur cinq semaines [calc]. Faut-il revoir le jalon, ou réduire le périmètre (la carte
à l'après-rendu, CB-19 au lot RODAGE) ?

## 6. Index des questions techniques (pour l'orchestrateur et les advisors)

- **Générales** :
  - Q-G-01 : emplacement du paquet et des documents (§1, pt 1) ;
  - Q-G-02 : dépendance à SIM-BIS (§5) ;
  - Q-G-03 : une relecture G2 par partie, METHODE-PARTIES (§1, pt 7) ;
  - Q-G-04 : taille et jalons (§5) ;
  - Q-G-05 : analyse statique de sécurité du paquet neuf (outil soumis à R-8, ou limite écrite ; leçon de
    SHOGEN-SAST-PYTHON-RECALCUL-1, l.916) ;
  - Q-G-06 : pièce G6 du paquet neuf (bibliothèque standard seule, licence ; leçon de SHOGEN-G6-PIECE-RECALCUL-1).
- **COLLECTE-BIS** : Q-C-01 à Q-C-16 (§2.6).
- **RECALC-BIS** : Q-R-01 à Q-R-13 (§3.6).
- **DEPLOI-BIS** : Q-D-01 à Q-D-10 (§4.6).

Advisors proposés :
- STATS : Q-R-01, Q-R-02, Q-R-04, Q-R-05, Q-R-06, Q-R-11, Q-R-13, Q-C-07 ;
- OPS : Q-C-01 à Q-C-06, Q-D-01 à Q-D-08 ;
- l'orchestrateur seul : le reste.

## 7. Écarts à la lettre de l'ADR, signalés et non appliqués

| où | lettre de l'ADR | écart proposé | question |
|---|---|---|---|
| l.241 | « clone le dépôt à un commit épinglé » | archive du seul paquet au commit scellé, sha256 au paquet | Q-D-01 |
| l.245 | « quatre copies par réplication entre observateurs et espace de sauvegarde » | réplication par l'espace de sauvegarde seul, rétention locale bornée | Q-D-02 |
| l.107 (D-2) | première lecture partie plus de 5 s après ws + w − δ | aussi : toute lecture planifiée non partie | Q-C-02 |
| l.241 (pare-feu) | « sortant HTTPS ; DNS vers le résolveur et vers les trois témoins D-4 ; NTP ; SSH entrant par clé seule » | SSH sortant vers la sauvegarde, DNS sortant pour O1, IPv6 | Q-D-07 |
| l.231 | `records` et `report` « réutilisés » | réutilisation limitée aux fonctions pures et aux conventions | Q-R-12 |
| l.308 | coûts en lignes | environ trois à quatre fois plus [inféré, base mesurée] | Q-G-04 |

## 8. Actes de l'investisseur (en langage clair)

- **A-1 Accords.** Donner votre accord une fois par partie (cinq parties, §5). Aucune question technique ne vous est posée.
- **A-2 Comptes.** Ouvrir vous-même :
  - Hetzner (un serveur et l'espace de sauvegarde) ;
  - OVHcloud (un serveur) ;
  - DigitalOcean (un serveur) ;
  - Akamai Linode (un serveur) ;
  - Healthchecks.io (gratuit).
- **A-3 Serveurs.** Pour chacun des quatre serveurs : choisir l'offre, la région et l'image qu'on vous indiquera ; coller le script
  préparé dans la case « script de démarrage » ; remplir les quelques valeurs indiquées en tête (le nom de l'observateur, votre
  adresse d'alerte, l'adresse de sauvegarde) ; démarrer le serveur.
- **A-4 Après le démarrage.** Recopier deux choses affichées par chaque serveur, l'adresse IP et la clé publique de sauvegarde, et
  nous transmettre l'adresse IP. Ce ne sont pas des secrets.
- **A-5 Sauvegarde.** Créer un sous-compte par serveur dans l'espace de sauvegarde, y coller la clé publique du serveur, activer
  les instantanés automatiques.
- **A-6 Alertes.** Créer quatre alertes dans Healthchecks (une par serveur : un signal attendu toutes les 5 minutes, alerte après
  15 minutes de silence) et coller leur adresse dans le script du serveur correspondant.
- **A-7 Exercices.** Avant le rodage, faire trois exercices guidés :
  - arrêter volontairement un service et vérifier que l'alerte arrive par courriel ;
  - confirmer qu'une copie de sauvegarde se restaure ;
  - confirmer qu'un horodatage quotidien est arrivé.
- **A-8 Pendant la mesure.** Vous êtes le seul à intervenir sur les serveurs. À chaque alerte, appliquer la procédure en trois
  gestes : redémarrer le service, puis la machine, puis la reconstruire depuis le script. Noter chaque geste dans le fichier
  d'interventions (qui, quand, quoi). Un agent n'intervient que sur votre autorisation écrite, au cas par cas.
- **A-9 Ce qu'il ne faut pas ouvrir.** N'ouvrez pas les fichiers de journal : ils contiennent l'état des sources, qui doit rester
  caché jusqu'au rendu. La commande `status` vous montre la santé des serveurs et le nombre de fenêtres utiles, sans rien
  révéler.
- **A-10 Disque.** Si le rodage montre que les journaux grossissent plus vite que prévu, il faudra choisir un disque plus grand
  chez un ou deux hébergeurs. Ce sera un petit coût, qu'on vous chiffrera avant.
- **A-11 Fin.** À la clôture : laisser faire la copie finale, déposer les journaux sur votre Drive, puis arrêter et résilier les
  serveurs.
- **A-12 Horodatage quotidien.** Votre go écrit, avant le début de la mesure, autorise aussi l'envoi automatique de l'horodatage
  quotidien (accepté en principe le 2026-10-04, q. 7).

## 9. Provenance

**Pièces lues dans le dépôt** [lu] (préfixe de sha256 à `e16956b`) :
- `docs/PASSATION-CLOUD.md` (`c7d40a0f…`), en entier ;
- ADR-0029 (`02f8f6cc…`), en entier ;
- DÉC (`603abda2…`, égal au préfixe cité par l'ADR) ;
- AVIS-OPS (`52fbfdb9…`) ; AQT (`836ece5e…`) ; AVIS-STATS (`52a1a69b…`) ;
- G0 de vague (`25a82120…`) ; G0 de PLAN-S2BIS (`81bf3f33…`) ;
- annexe D d'ADR-0028 (`deb64179…`), en entier ;
- ADR-0028, l.180-250 ;
- annexe B d'ADR-0028 (`31da5b35…`) : l.1-110, l.766-954 et les lignes des items cités ;
- `docs/11-mesures-pilotes.md` (`fcf93b87…`) : titres, §2.7, §9 ;
- `docs/METHODE-PARTIES.md` (`609b500d…`) ;
- `docs/10-mesures-pilotes-design.md` §3.3 et §4.1 ;
- `docs/17-modele-de-menace.md` (identifiants T-01 à T-18) ;
- `docs/R-8-outillage.md`, l.1-60 ;
- `docs/DEVOPS.md` §4 ;
- `docs/09-vocabulaire.md`, l.1-40 ;
- P6 (`1167e605…`) : l.1-60 et l.120-165 ;
- `ETUDE-POOL-BIS.md` (`d3780f13…`) : §7 et §8 ;
- `calib/SOURCES-HISTORIQUES.md` (`f649e30f…`) : l.1-40 et lignes trouvées par recherche ;
- recherches dans CP1-V3, G1-v3, CP1, G1 et CE (mots-clés des trois lots) ;
- JOURNAL l.382-398 (repérées par recherche de l'heure de l'entrée) ;
- dans `s2-harness/` :
  - en entier : `collector.py`, `sources.py`, `run_campaign.py`, `journal.py`, `model.py`, `smoke.py`, `records.py`,
    `window.py` ;
  - en partie : `r1.py` (l.140-535), `r2.py` (l.245-405), `tools/rendu_unique.py` (l.1-340), `README.md`, `RUNBOOK-campagne.md`
    (titres, l.36-70), en-têtes de `tests/test_sources.py` et `tests/test_collector.py` ;
- `enforcement/verdict-suite-s2.py`, l.1-60 ;
- `xtask/src/sg5.rs`, l.1-140.

**Non ouverts** : `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`,
`docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/`, tout `*.jsonl`, toute pièce de D.2 (liste lue en D.2, aucun contenu
ouvert), JOURNAL hors l.382-398. `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée.

**Mesures** [mesuré, 2026-10-04, hôte de la session, Python 3.11.15] :
1. Suite `s2-harness` : `python3 -B -m unittest discover -s tests -t .` donne « Ran 405 tests in 44.112s / OK (skipped=2) ».
2. Essai 1 (script `essais/essai_lecture.py`, sha256 `d67fcb40…2da`, sur fixture, sans réseau) : `sources.read()` lève
   `ConnectionResetError` quand le corps est coupé pendant sa lecture.
3. Essai 2 (même script) : `urllib.request.urlopen(timeout=0,5)` reste bloqué 3,03 s par une résolution DNS simulée de 3 s.
4. Tailles (`wc -l`) : `shogen_s2/*.py` et `tools/*.py` font 5 791 lignes ; `tests/*.py` font 8 774 lignes.
5. `openssl version` donne OpenSSL 3.0.13.
6. `deb.debian.org` : `InRelease` de trixie HTTP 200 ; `Packages.xz` de trixie main amd64 HTTP 206 (un octet demandé).

**Calculs** [calc] :
- 395 Mo / 38 600 fenêtres ≈ 10 233 octets par fenêtre ;
- × 43 200 fenêtres par mois ≈ 0,44 Go par mois ; × 4 ≈ 1,77 Go par mois ;
- 25 Go / 17 Go par mois ≈ 1,5 mois.

**Réviseur attendu** : l'orchestrateur, puis un validateur frais pour un cp-1 bref (proposition). Le rédacteur n'a généré aucun des
lots qu'il décrit.
