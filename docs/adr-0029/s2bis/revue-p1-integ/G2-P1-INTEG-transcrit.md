# Relecture G2 neuve d'intégration de la partie P1 (transcrit)

> Transcription par l'orchestrateur le 2026-10-05 16:44:37 UTC du rapport rendu par message par le réviseur (agent a6a81475c74aac459) ; contrôle FM-1.1 : fragments_l51_l14 = 0. Texte du réviseur ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`). L'annexe du rapport, texte intégral de `CLOTURE-P1.md`, n'est pas recopiée : elle est identique au fichier `CLOTURE-P1.md` (sha256 3928d1d6e90640a955e2d47881b8759d8986cc729d9f095ee7515438cda0e323), versé à côté.

Gate 0 : **claude-opus-5-5**. C'est l'identifiant exact du modèle sous lequel je tourne. L'effort « max » n'est pas observable de l'intérieur.

# Relecture G2 neuve d'intégration de la partie P1 (noyau du collecteur S2-bis), base 98c8537

**Verdict : ACCEPTE-AVEC-CORRECTIONS.** La liste fermée compte cinq corrections, C-1 à C-5, détaillées plus bas. La pièce de clôture est écrite : `<scratchpad>/s2bis/p1-integ/CLOTURE-P1.md` (sha256 `3928d1d6…e323`, 77 lignes). Son texte est recopié en annexe.

- Heures (`date -u`) : début 15:26:45, fin 16:41.
- Je n'ai fait aucune écriture git dans `/home/user/shogen`.
- Base vérifiée au début : `98c853782bdb…`, égale au brief.
- **La tête a bougé pendant la relecture.** Trois commits sont arrivés : `62ed36a` (CB-18v, runner : 5 cas de plus, L-37 à L-41, et METRIQUES, commis à 16:34:31), puis `d1f95d5` et `3014dde` (SIM-BIS). Je ne les ai pas relus.
- Le constat de C-5 (b) tient à la tête (mesuré).

## Résumé court

**Ce qui tient :**
- Le noyau tient sa conception.
- Une sonde du FORMAT, écrite d'après le texte seul, ne trouve **aucun écart** avec l'écrivain réel : 1 000 journaux synthétiques, 4 876 redémarrages, 1 801 queues déclarées, processus tués et pannes d'écriture injectées.
- Le point d'entrée réel sort proprement et laisse un journal conforme :
  - 25 fenêtres en 7 exécutions : panne de source, lecture pendue, recul d'horloge, SIGKILL, SIGTERM, seconde instance refusée ;
  - puis 1 800 fenêtres en 30 min : mémoire en plateau à 45,4 Mo, 18 fils au plus.
- Les réponses HTTP hostiles sont toutes closes dans le délai.

**Ce qu'aucune tranche ne voyait :**
- **C-1.** Un seul datagramme DNS hostile arrête le collecteur à chaque fenêtre.
- **C-2.** La reprise chaîne, déclare et somme des octets jamais synchronisés. Une coupure de courant crée alors une rupture non déclarée. Le fsync du dossier avait été accepté en tranche A « au plus tard CB-18 » et n'a jamais été fait ni inscrit.
- **C-3.** Cinq mutants d'interface survivent (25 tués sur 30). L'un d'eux empêcherait tout démarrage en production (w = 60).
- **C-4.** Quatre phrases du FORMAT ne disent pas ce que fait le code.
- **C-5.** Un vérificateur qui sort en 0 dès son chargement fait passer le runner sans aucun cas. L'enregistreur admet un plancher 0.

## 1. Couverture du G0 (sous-lots CB-0 à CB-5, CB-10, CB-11, CB-18)

Abréviations : `c/` = `s2bis/shogen_s2bis/collecte/`, `t/` = `s2bis/tests/`, lignes à 98c8537.

| sous-lot | exigence | tenue | test | constat |
|---|---|---|---|---|
| CB-0 | E-C-01 | imports stdlib seuls (vérifié par `ast`) | `t/test_fitness.py:59`, `:64` | tenue |
| CB-0 | E-C-02 (lecture scellée) | `c/config.py:32-70` | `t/test_config.py:25-55` | tenue |
| CB-0 | E-C-40 | `t/__init__.py:29-35` | `t/test_garde.py:11`, `:29` | tenue (limites connues : `sendmsg`, `_socket`) |
| CB-0 | E-C-41 | fitness, METRIQUES | `t/test_fitness.py:85`, `:92` | tenue |
| CB-0 | §1 pt 6 (job, plancher) | `gates.yml:198-220`, `enforcement/verdict-suite-s2.py:36-53` | runner K-02, C-03…C-08 | tenue, sauf C-5 (b) |
| CB-1 | E-C-16 | `c/journal.py:182-187` | `t/test_journal.py:116` ; mon run G | tenue |
| CB-1 | E-C-18 | `c/journal.py:92-112`, `:368-381` | `t/test_journal.py:91`, `:96` | tenue |
| CB-1 | E-C-19 | `c/journal.py:206-213` | `t/test_journal.py:96`, `:105` | tenue |
| CB-2 | E-C-20 | `c/journal.py:237-246`, `:268-274`, `:352-366` | `t/test_fichiers.py:15-61`, `t/test_reprise.py:277` | tenue ; sous coupure : C-2 |
| CB-2 | E-C-21 | `c/journal.py:283-350` | `t/test_reprise.py:42-277` | tenue (banc : 0 écart) ; sous coupure : C-2 |
| CB-2 | E-C-22 | `c/journal.py:238`, `:247-248`, `:329-334` | `t/test_trous.py:16-113` | tenue |
| CB-3 | E-C-03 | `c/http.py:81-132`, `c/lecture.py:25-34` | `t/test_http_reseau.py:139-187`, `t/test_http.py:63-89` | tenue |
| CB-3 | E-C-04 | `c/http.py:111-125` | `t/test_http_reseau.py:125` | partage du suivi non testé : C-3 |
| CB-3 | E-C-05 | `c/http.py:107`, `:114` | `t/test_http_reseau.py:125` | tenue |
| CB-3 | E-C-17 | `c/lecture.py:36-40`, plafond `c/http.py:21`, `:57` | `t/test_http.py:83`, `t/test_lecture_pendue.py:125` | tenue |
| CB-4 | E-C-09 (part P1) | `c/boucle.py:35-44`, `c/entree.py:64-65` | `t/test_boucle.py:141`, `:306` | tenue ; regroupements : P2 |
| CB-4 | E-C-11 | `c/boucle.py:83` ; valeurs dans `formes.json` | `t/test_boucle.py:148` ; `DELAI` dans `t/test_lecture_pendue.py:104` | **valeurs de l'ADR (20 s, 10 s, 1 s, 5 s) : aucune configuration scellée, aucun test qui les lie** |
| CB-4 | E-C-12 | `c/boucle.py:97-119` | `t/test_boucle.py:157`, `:204`, T-LP-1, T-LP-2 | lectures factices seulement ; client réel : C-3 |
| CB-4 | E-C-13 | `c/boucle.py:68`, `:107-114` | `t/test_boucle.py:172`, `:180`, T-LP-3, T-LP-5 | tenue ; libellé : C-4 (a) |
| CB-4 | E-C-14 | `c/boucle.py:90-92` | `t/test_boucle.py:172`, `:239`, T-LP-5 | tenue |
| CB-4 | E-C-15 | `c/boucle.py:82-119` | **aucun test** (tenue par construction) | disque et empreinte lus sur le fil principal sans borne : item 4 |
| CB-5 | T-LP-1…6 | `t/test_lecture_pendue.py:53-125` | idem | tenue |
| CB-10 | E-C-27, E-C-28 (format) | `c/dns.py:23-119` | `t/test_dns.py:52-185` | taille de réponse non bornée : C-1 |
| CB-11 | E-C-25, E-C-26 | `c/boucle.py:116-118`, `c/sante.py:23-97` | `t/test_sante.py:164` ; `t/test_bout_en_bout.py:108-124` | tenue ; D-3 analysé au recalcul (CHRONYC-FORMAT-1) |
| CB-11 | E-C-27 | `c/sante.py:68-69` | `t/test_dns.py:52`, `t/test_sante.py:82` | **trois témoins de l'ADR et 2 s : non scellés** |
| CB-11 | E-C-28 | `c/sante.py:70-71`, `c/entree.py:94-95` | `t/test_entree.py:148` | **noms témoins non scellés** |
| CB-11 | E-C-29 | `c/boucle.py:85-87` | `t/test_sante.py:164` | tenue |
| CB-18 | E-C-02 (`run_params`) | `c/entree.py:57-83`, `:117` | `t/test_entree.py:76-146`, `:187` | taille de `run_params` non contrôlée : item 3 |
| CB-18 | E-C-16 (point d'entrée) | `c/entree.py:115-124` | `t/test_entree.py:187` | tenue (SIGTERM : item existant) |
| CB-18 | E-C-23 | `c/entree.py:117-118` | `t/test_entree.py:187`, `t/test_bout_en_bout.py:194` | calendrier absent (item RUNPARAMS-CALENDRIER-1) |
| CB-18 | E-C-24 | FORMAT ; `t/test_bout_en_bout.py:68-130` | `:163` | tenue ; libellés : C-4 |

**Exigences sans test :**
- E-C-11, E-C-27, E-C-28 : leurs valeurs (pas de configuration de production scellée) ;
- E-C-15 : aucun test explicite ;
- E-C-12 : jamais testée avec le client réel ;
- E-C-23 : le calendrier manque.

## 2. FORMAT et code

**Sonde et banc.**
- Sonde indépendante `outils/sonde_format.py` (`0b2d0dcd…`), écrite d'après le FORMAT seul. Elle couvre :
  - §6.1 et §7.7 : grammaire, ordre (jour, k) ;
  - §7.1 (a) à (e), avec niveaux et entiers comptés sur les octets ;
  - §7.4 : déclaration exacte des queues ;
  - la validité : grille, suivante, trous et causes, point, bascule, ordre de la fenêtre, `run_params` ;
  - les sommes.
- Banc `outils/banc_ecrivain.py` (`edca2fa8…`) sur l'écrivain réel. Il injecte :
  - des pannes : fsync EIO, écriture partielle ENOSPC, création refusée ;
  - des reculs et des avances d'horloge ;
  - des bascules ;
  - les refus attendus ;
  - des coupures.

**Résultats sans coupure** (`preuves/banc-coupure0.txt`) : 1 000 graines, 4 876 redémarrages, 1 801 queues déclarées. **0 écart** sur :
- la déclaration ;
- `_lire` comparé à la sonde, fichier par fichier ;
- l'état de reprise (suivante, attendu, cause) ;
- les refus, qui n'écrivent rien ;
- les sommes ;
- les ruptures.

Le seul défaut est 30 journaux devenus illisibles. Tous viennent d'une panne de la toute première écriture, sans aucune ouverture réussie auparavant (item 1).

**Résultats sous coupure de courant** (modèle : chaque inode revient au plus à sa taille au dernier fsync ; `preuves/banc-coupure1*.txt`) :
- 300 graines ;
- 128 finissent avec une rupture : 86 reprises au lien rompu, 86 déclarations fausses ;
- 131 finissent avec une somme fausse ;
- 0 écart au moment du redémarrage : la cause est la durabilité (C-2).

**Écarts de texte (C-4) :**
- §11.6 `tardives` ;
- §11.5 `run_params` après une bascule ;
- §4 « seulement là » ;
- §9.1 et §10.1 : le sous-type `dns` venu du client porte une phase et une adresse.

Sur boucle, lecture, DNS, santé, points d'entrée et `run_params`, le reste du texte est conforme au code (§9 à §14 relus ligne à ligne).

## 3. Bout en bout

Point d'entrée réel, `python3 -m shogen_s2bis.collecte pool`, sur la copie de 98c8537.
- Isolement : `unshare -n -m`, `lo` allumée, `/etc/resolv.conf` remplacé dans l'espace seul par un résolveur muet (127.0.9.54).
- Serveurs factices :
  - HTTPS signé par une CA de test passée par `SSL_CERT_FILE` (clés créées à l'exécution, détruites) ;
  - DNS : témoins SOA, un témoin muet, un résolveur avec NXDOMAIN.

**Scénario** (`outils/bout_en_bout_g2.py`, `preuves/e2e-A.json`), un PID par exécution :

| exécution | PID | sortie |
|---|---|---|
| A : 8 fenêtres, panne de la source c pendant 3 W | 3020 | 0 |
| B : recul de 2,5 s, D-3 lente | 3301 | 0 |
| C : SIGKILL en pleine fenêtre | 3534 | −9 |
| D : redémarrage | 3610 | 0 |
| E : SIGTERM | 3963 | −15 |
| F : redémarrage | 4047 | 0 |
| G : seconde instance | 4386 | 1, `JOURNAL/occupe` (la première, PID 4374, sort en 0) |

- **Journal :** 25 marqueurs. Ma sonde ne trouve ni rupture ni écart, `anomalies` du dépôt rend `[]`. Chaque démarrage écrit reprise puis `run_params` ; un trou `arret` suit C, E et la reprise.
- **Lectures :**
  - c en `connexion` pendant la panne ;
  - f pendue au DNS : classée `dns` à E, tardives d'environ 10 s ;
  - d au goutte-à-goutte, g muet : `delai` ;
  - e (2 Mio) : `autre`.
- **Horloge :** le recul se lit dans `horloges` (murale 3 998 027 µs, monotone 6 498 028 µs).
- **Pool à `places` = nombre de formes :** la lecture pendue fait 20 non-départs en 25 fenêtres. C'est mesuré à w = 4 s, sur une échelle de temps comprimée (item 2).

**Durée** (`outils/duree.py`) :
- 200 × 2 s, PID 19375 : sortie 0, mémoire 38,2 à 39,4 Mo, 9 fils au plus ;
- 1 800 × 1 s, PID 2286 : sortie 0, 1 800 marqueurs, mémoire en plateau à 45,37-45,46 Mo de 300 à 1 790 s (pente ≈ 0,05 Mo/h), 11 à 18 fils, au plus 10 lectures abandonnées, journal conforme (8 052 307 octets).

**Sonde pendue :** les sondes réelles sont bornées par leur délai.
- D-3 lente : `erreur: delai` à 2,4 s ;
- témoin muet : `delai`.

Le seul vrai blocage observé est sur le fil principal (FIFO, item 4).

## 4. Intégration entre tranches

**Défauts que les tranches ne voyaient pas :**
- **Refus de l'écrivain en pleine fenêtre** (DNS → santé → écrivain → point d'entrée) : C-1, mesuré. Les lectures de la fenêtre sont écrites, la `sante` est refusée, sortie 1. À la relance, le trou `arret` est correct, mais le refus revient à chaque fenêtre.
- **Échec du disque au moment d'une bascule** : sans coupure, banc juste. Avec coupure, voir C-2.
- **État partagé lecture ↔ boucle par `suivi`** : jamais testé avec le client réel (MI-09 et MI-10 vivants). Course : `http.py:111` pose `phases["dns"]` puis `adresse`, alors que la boucle lit les phases puis l'adresse (`boucle.py:99-100`). Un espion le montre (`preuves/ordre-suivi.txt`) : C-3 (b).
- **Câblage du point d'entrée vers l'écrivain et la boucle :** ouverture hors grille si w > 1 (MI-12), délai et places non vérifiés (MI-13, MI-14) : C-3.
- **Configuration admise mais impossible à journaliser :** `run_params` de 4 327 507 octets donne une sortie 1 à chaque démarrage, après l'ouverture (`preuves/configs-hostiles.json`) : item 3.
- **Exceptions non nommées :** une `MemoryError` (`config_resolveur` = `/dev/zero`) traverse le point d'entrée, sortie 1 par trace. Une `RuntimeError` au démarrage d'un fil ferait de même [inféré] : observation O-1.

## 5. Sécurité et robustesse

- **HTTP hostile** (`preuves/hostiles.json`) :
  - 150 en-têtes, en-tête de 70 Kio, réponse non HTTP, 2 Mio : `autre` ;
  - `Content-Length` de 10¹², bloc `ffffffffffff`, réponse muette ou au goutte-à-goutte : `delai` à 3,0 s ;
  - 302 : `panne_http` ;
  - mémoire +2 Mo au plus, aucune exception.
- **DNS hostile :** 4 077 réponses par pointeurs vers un nom de 255 octets de caractères de contrôle. La ligne `sante` fait 6 209 510 octets, au-delà de LIMITE (4 194 304). Le point d'entrée sort deux fois en 1 avec `JOURNAL/taille`, sans marqueur. Avec des lettres simples, 1 113 260 octets par sonde : C-1.
- **Configurations hostiles :**
  - FIFO comme `config_resolveur` : boucle pendue, aucun marqueur, aucune sortie (tuée à 20 s) ;
  - `/dev/zero` : `MemoryError` (essai fait sous `RLIMIT_AS` 1,5 Gio) ;
  - `run_params` trop long : voir la section 4.
- **Droits :** fichiers créés en 0o644 (`journal.py:182`, `:271`, `:280`) : item 6.
- **Secrets :** la gate des secrets sur un dépôt jetable des 32 fichiers de P1 donne `--tree` OK et `--history` OK. Le journal ne porte aucun secret.
- **Garde réseau :** relue ; les sous-processus de test importent `tests` ou ne touchent pas le réseau. Toutes mes exécutions ont tourné en `unshare -n`.

## 6. CI et gates

**Matrice** en `-X dev -W error` (`PYTHONDEVMODE=1`, `PYTHONWARNINGS=error`), lignes de `gates.yml` en réseau isolé (`preuves/jobs-3.1x.txt`) :

| Python | runner | s2bis | S2 | sim-bis |
|---|---|---|---|---|
| 3.10 | 77 ok | Ran = 184 | rouge : 77 FAIL, 3 ERROR (item connu SHOGEN-S2-PY310-1) | 129 |
| 3.11, 3.12, 3.13 | 77 ok | Ran = 184 | 406 | 129 |

- La suite s2bis compte 184 tests : 143 du collecteur et 41 du recalcul, alors que B.67 dit « 184 tests du collecteur ».
- PID sous 3.12 : runner 821, s2bis 847, S2 1145, sim-bis 3899.

**Enregistreur** (`preuves/leurres-enregistreur.txt`) :
- L0 vert : exit 0. L0b rouge : exit 1.
- **L1 (`--plancher 0`, suite vidée) : exit 0 et `--verifier` conforme sous 3.11** (le `python3` de la session). Sous 3.12, exit 1, mais seulement parce que unittest sort en 5.
- **L2 (vérificateur complaisant dans le commit) : exit 0 et conforme**, sous 3.11 comme sous 3.12.
- L3 (étape `sed` avant la ligne) : l'enregistreur n'est pas trompé.

**Runner :** avec un vérificateur qui fait `sys.exit(0)` à son chargement, le runner sort en 0 **sans aucun cas**. C'est mesuré à 98c8537 et à la tête (`preuves/runner-verificateur-complaisant.txt`).

**xtask** (`cargo --locked xtask verify` sur la copie, cible dédiée, lignes de verdict seules, `preuves/xtask-verdicts.txt`) :
- S-G1 à S-G8 VERT ;
- no_std, fmt et clippy VERT ;
- S-G9 ROUGE, seule violation `docs/17-modele-de-menace.md:70` (connue) ;
- verdict global ROUGE.

**Contrôles statiques :** R-13 donne 0 marqueur sur 32 fichiers (contrôle positif 1). R-8 : bibliothèque standard seule.

## 7. Mutants transverses

Mes 30 mutants (`outils/mutants.py`, `59b4fd2c…`), classés par la ligne du job s2bis, borne 300 s, `preuves/mutants.txt`.
- Témoin VIVANT (sortie 0).
- **25 TUÉS, 5 VIVANTS, 0 FATAL.**

Vivants, tous aux interfaces :
- **MI-09** : phases copiées, le suivi de la boucle reste vide.
- **MI-10** : adresse posée au suivi seulement à la fin de la lecture.
- **MI-12** : ouverture hors grille quand w > 1 ; en production, refus de démarrer.
- **MI-13** : délai scellé non transmis ; équivalent seulement si ce délai vaut 10 s.
- **MI-14** : taille scellée du pool ignorée.

Ma première campagne a été invalidée par un témoin rouge (le FORMAT manquait à ma copie). Elle n'est pas comptée et a été refaite entièrement (écart E-3).

## 8. Registre (je ne ferme rien, je signale)

**B.60**
- ENREG-ROLE-1, fermé : réellement fermé pour la couverture des suites ; deux leurres neufs (C-5 a, item 5).
- HORLOGE-RECUL-JOURNAL-1, fermé : réellement (recul mesuré dans `horloges`).
- CORPS-BORNE-1 :
  - fermé « pour la borne du corps » : juste ;
  - **le volet graphe reste ouvert sans déclencheur inscrit** (la G2 de P1-B le disait redaté à CB-6) ;
  - mesuré : `canonique` est exponentiel sur une structure partagée (profondeur 18, 20, 22 : 0,23 s, 0,78 s, 3,4 s ; `preuves/graphe-partage.txt`).
- RETENTION-1, ouvert, DB-4 : déclencheur juste ; ajouter les sommes fausses après coupure (C-2).
- ECRIVAIN-USAGE-1, fermé : réellement.
- G3-LIGNE-JOB-1 : consigne permanente, juste.
- P1-ESTIMATION-1 : ouvert, déclencheur juste, **valeur à mettre à jour** : P1 mesure environ 1 116 lignes de code et 2 789 lignes de tests (`wc -l`), soit environ 3 900 contre 1 620 estimées (×2,4), au-delà de la fourchette 2 900-3 200 de l'item.

**B.63**
- Ouverts, déclencheurs justes :
  - CHRONYC-FORMAT-1 ;
  - TLS-REUSSI-1 : le chemin réussi a marché de bout en bout avec une CA de test créée à l'exécution, sans fixture de clé ;
  - DNS-TC-1 ;
  - DNS-ID-16BITS-1.
- Fermés, réellement fermés :
  - PLAN-CABLAGE-1 : mais le câblage du délai et des places n'est pas testé (C-3 d) ;
  - SONDES-ECHEANCE-1 : MI-05 et MI-26 tués ;
  - SOMMEIL-MURAL-1 ;
  - FORMAT-RETOUCHES-1.

**B.67, items ouverts**
- Déclencheurs justes :
  - PREFIXE-NOM-1 ;
  - ANALYSEUR-RESIDUS-1 ;
  - RUNPARAMS-CALENDRIER-1 ;
  - SIGTERM-1 : mesuré, sortie −15, journal cohérent ;
  - PY310-1 ;
  - HOTE-COMMUN-1 ;
  - TOLERANCE-D2-1 ;
  - ENV-ETAPE-1.
- **ECRIVAIN-REFUS-ARRET-1 : déclencheur trop tardif.** P1 l'atteint seul par les sondes DNS (C-1). Après C-1, l'item garde CB-6 pour les décodeurs.
- PLAN-S2BIS-EXCLUSIONS-1 : hors de P1.

**B.67, items fermés :** réellement fermés. Vérifié par le banc ou par les tests :
- SEGMENT-JOUR-1 ;
- ENTIER-ECRIVAIN-1 ;
- CITATIONS-ADR-DECALEES-1 ;
- CONFIG-REGLES-1 ;
- LIGNE-JOB-LEURRE-1, côté runner ;
- LIRE-BOOLEENS-1 ;
- SEGMENTS-10-1 ;
- TEST-DISQUE-INSTABLE-1 ;
- IMBRICATION-SEUIL-1 ;
- K-ETAPES-LEURRE-1.

**Non formés**
- I-1 de P1-A (fsync du dossier, déclencheur « au plus tard CB-18 ») : couvert par C-2 (a).
- I-5 de P1-A (`JOURNAL/illisible` au premier démarrage) : item 1.
- I-2 de P1-A (extension SAST à `s2bis/`) : la limite est écrite dans G6 §3, l'item SAST-PYTHON-RECALCUL-1 n'a pas été étendu. À trancher par l'orchestrateur.

## Corrections (liste fermée)

**C-1 (CB-10, CB-11 ; FORMAT §12, §13 ; `dns.py:94-119`).**
- **Défaut :** une réponse UDP appariée n'a pas de borne de taille. Une seule réponse de 65 507 octets porte la `sante` au-delà de LIMITE, et le collecteur s'arrête à chaque fenêtre.
- **Règle :** RFC 1035 §2.3.4 (l.529 : « UDP messages 512 octets or less ») et §4.2.1 (l.1756-1758) [lu, `d14ae809…`].
- **À faire :**
  - (a) une réponse de plus de 512 octets devient `forme`, avec la règle citée au §12 ;
  - (b) borner au schéma de `sante.json` le nombre de témoins et de noms, de sorte que la plus grande `sante` possible reste sous LIMITE ; borne calculée et écrite.
- **Tests :** 513 octets → `forme` ; la réponse du réviseur → `forme` ; `sante` maximale construite sous LIMITE ; un mutant tué.

**C-2 (CB-1, CB-2 ; FORMAT §4, §6.4, §7.4 ; `journal.py:276-281`, `:315-350`).**
- (a) fsync du dossier après la création d'un fichier du journal et du fichier de sommes.
- (b) Avant d'écrire une `reprise` en segment neuf, rendre durables les octets dont elle dépend : le fichier dont elle chaîne la dernière ligne intègre, les fichiers dont elle déclare la queue, les fichiers qu'elle somme. Aujourd'hui seuls le fichier de sommes et le segment neuf sont synchronisés (`preuves/repro-reprise-durable.txt`).
- Tests par l'espion de fsync. FORMAT §4 et §6.4 à mettre à jour.

**C-3 (CB-3, CB-4, CB-18).**
- (a) Le client réel dans la boucle, avec une lecture pendante à E après dns et connexion : attendu `panne_transport:delai`, phases présentes, adresse posée. Tue MI-09 et MI-10.
- (b) Poser l'adresse avant `phases["dns"]` (ou lire l'adresse d'abord), avec un test par suivi espion.
- (c) Point d'entrée avec w > 1. Tue MI-12.
- (d) Câblage : délai et places lus de `formes.json`. Tue MI-13 et MI-14.

**C-4 (FORMAT seul).**
- (a) §11.6 : une lecture finie entre E et le relevé compte en `tardives` à la fenêtre suivante (`boucle.py:107-114`, test `t/test_boucle.py:204`).
- (b) §11.5 : `run_params` suit l'`ouverture` de la bascule qu'il déclenche (`preuves/run-params-bascule.txt`).
- (c) §4 : « et seulement là » contredit §6.2, §6.3 et §7.4.
- (d) §9.1 et §10.1 : une `dns` rendue par le client après une résolution tardive porte `phases.dns` et une adresse jamais contactée (`preuves/dns-tardive-adresse.txt`). L'écrire, ou aligner le client.

**C-5 (outillage CI).**
- (a) `oracle_record.py:115-116` : `--plancher [0-9]+` doit devenir `[1-9][0-9]*`, comme K-02. Test avec un commit `--plancher 0`.
- (b) `run-fixtures-verdict-suite-s2.py:39-45` : échouer fermé (sortie 3) sur toute exception au chargement du vérificateur, SystemExit compris. Test avec un vérificateur qui fait `sys.exit(0)`.

## Items à former (règle PAROXYSME, propriétaire l'orchestrateur)

1. **SHOGEN-S2BIS-PREMIERE-ECRITURE-1.** Une première écriture coupée d'un journal neuf le rend `JOURNAL/illisible` pour toujours (30 graines sur 1 000 au banc). Déclencheur : G0 de DB-6 et exercices A-7 ; la décision de code se prend au gel.
2. **SHOGEN-S2BIS-CONFIG-PRODUCTION-1.** Configurations scellées de production : valeurs de E-C-11, E-C-27 et E-C-28 liées à l'ADR par un test ; marge du pool au-dessus du nombre de formes ; délais de `resolv.conf`. Déclencheur : gel du collecteur.
3. **SHOGEN-S2BIS-RUNPARAMS-TAILLE-1.** Refus `CONFIG/taille` avant l'ouverture. Déclencheur : gel.
4. **SHOGEN-S2BIS-RESOLVEUR-LECTURE-1.** Lecture de l'empreinte et du disque bornée : fichier régulier exigé, taille plafonnée. Déclencheur : G0 de DB-1.
5. **SHOGEN-S2BIS-ENREG-VERIF-COMMIT-1.** L'enregistreur exécute le vérificateur du commit (L2). Remède : consigner son sha256 et le comparer à celui de l'outil. Déclencheur : avant la G2 de P2.
6. **SHOGEN-S2BIS-DROITS-JOURNAL-1.** Fichiers en 0o644. Déclencheur : G0 de DB-1 (UMask, dossier en 0700).

À inscrire aussi :
- le déclencheur du volet graphe de CORPS-BORNE-1 ;
- le nouveau périmètre d'ECRIVAIN-REFUS-ARRET-1 ;
- la nouvelle valeur de P1-ESTIMATION-1.

## Observations

- **O-1.** Exceptions non nommées : sortie 1 par trace, sans le message `collecte : arrêt`.
- **O-2.** La règle `noms-dns` admet tout libellé ASCII, espaces et caractères de contrôle compris.
- **O-3.** `_nom` ne borne pas à 255 octets un nom décompressé ; C-1 le borne de fait.
- **O-4.** L'agent utilisateur de S2 nomme le projet et son dépôt à chaque source : à écrire au modèle de menace.
- **O-5.** Commit `62ed36a` arrivé pendant la relecture, non relu ici.

## Écarts du réviseur

- **E-1.** `du -sh` sur ma copie et sur mon `tmp` (tailles seulement).
- **E-2.** Mes recherches dans `ANNEXE-B-items.md` (un seul fichier : « illisible », « fsync », « SAST », « CORPS-BORNE ») ont affiché environ 11 lignes hors de B.60, B.63, B.65 et B.67 (l.115, 282, 515, 639, 745, 751, 904, 916, 981, 1038, 1041). Aucune n'est une pièce D.2.
- **E-3.** Première campagne de mutants invalide ; j'ai tué mon propre groupe de processus 2115.
- **E-4.** Deux lancements du bout en bout ratés par des erreurs de mon outil ; j'ai tué mon propre groupe 2321.
- **E-5.** `ps` m'a montré la ligne de commande d'un processus d'un autre agent (`cb18/corr4`) ; je n'y ai pas touché.
- **E-6.** xtask lancé sans isolement réseau, en `nice` ; sa sortie complète est supprimée.
- **E-7.** R-13 et la gate des secrets limités aux fichiers de P1.
- **E-8.** Un `git show` à la tête `3014dde` pour le runner.

**Exposition.** Aucun `*.jsonl` réel. Seuls des journaux synthétiques écrits par l'écrivain dans mon `TMPDIR`, tous supprimés. Aucune pièce D.2, aucun dossier exclu. `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée.

## Journal G1

**[lu]**
- Brief (`21f31db2…`), lu en entier.
- G0 (`0e9001f3…`), en entier.
- PROPOSITION (`0cdf84c2…`, égal à l'annonce du G0) : l.1-449 et 783-927.
- AVIS (`a919b307…`), en entier.
- FORMAT (`4f0a509b…`), en entier.
- ADR-0029 (`b908842d…`) : l.100-117, l.231-251 et les titres.
- Annexe B (`1f57f63f…`) : B.60, B.63, B.65, B.67.
- G6-PAQUET (`2e690eb1…`), en entier.
- RFC 1035 : l.520-535 et l.1745-1765.
- Pièces de revue :
  - G2-P1A : l.95-154 et l.368-527 ;
  - G2-P1B transcrite, en entier ;
  - G2-CB18 transcrite, en entier ;
  - CONTRE-CONTROLE-3-CB18, en entier ;
  - RAPPORT-WORKER-P1A : par recherche.
- Code :
  - `collecte/*.py`, `verdict-suite-s2.py`, le runner, `gates.yml` et `oracle_record.py`, en entier ;
  - tests lus en entier : `__init__`, garde, fitness, bout en bout, entrée, lecture pendue, boucle ;
  - tests lus en partie : journal, http_reseau, format, `test_oracle_record.py` (l.1-40, l.373-430) ;
  - les autres tests par la liste de leurs noms et docstrings.

**[abs]**
- Les autres pièces de revue ;
- PROPOSITION l.450-782 et le reste de l'ADR ;
- D.2 et les dossiers exclus ;
- le JOURNAL ;
- le comportement de la forge.

**[2nd]** Aucun chiffre repris sans recompte. Les chiffres cités des pièces sont marqués comme tels.

**Outils et preuves.** Tout est indexé dans `SHA256SUMS-reviseur` (93 entrées, toutes OK).

## Fichiers

Dossier : `<scratchpad>/s2bis/p1-integ/`
- `CLOTURE-P1.md`
- `SHA256SUMS-reviseur` (`e713f746…`)
- `NOTES.md`
- `couverture.md`
- `outils/`
- `preuves/`

Copies lourdes, cible cargo et journaux synthétiques sont supprimés.
