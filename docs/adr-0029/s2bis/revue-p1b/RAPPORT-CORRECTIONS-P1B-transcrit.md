# Rapport du worker — corrections G2 de la tranche B (transcrit)

> Transcription par l'orchestrateur le 2026-10-05 02:13:24 UTC du rapport final du worker (agent a196dd4c7271735e6), texte rendu par message ; contrôle FM-1.1 du transcript : fragments_l51_l14 = 0. Texte du worker ci-dessous, sans retouche.

Gate 0 : je tourne sous `claude-opus-5-5` (identifiant donné par le harnais). Je n'ai aucun moyen de voir de l'intérieur si l'effort est bien `max`.

# Corrections G2 de la tranche B (C-1 à C-7, plus O-5 et O-7) : rapport du worker

Le travail s'est fait du 2026-10-05 00:09:05 au 02:11:02 UTC (`date -u`). Base : tête `6535821d52fc99131d67fcd7a14f7bf9e1244de3` (copie `git archive` avec les exclusions du brief), plus les 8 diffs CB-3a à CB-11b appliqués en série. Leurs sha256 sont égaux à ceux de `p1b/SHA256SUMS`.

Toutes les corrections sont faites et les gates passent, sauf S-G9 de xtask, rouge comme attendu sur une copie. Cinq diffs, à appliquer en série après CB-11b.

## Résumé C-n par C-n

- **C-1 (échéance exacte)** :
  - **Relevé** : à E, la boucle relève une seule fois, avant toute écriture, l'état de chaque lecture et de chaque sonde.
  - **Lecture non finie** : son résultat n'était pas rendu au relevé, ou il porte `fin` > E. Elle est alors classée `panne_transport` avec `fin` = E. Ses phases et son adresse sont celles atteintes à E (instants au plus E). Son résultat est compté tardif à la fenêtre suivante.
  - **Test** : écrivain ralenti injecté. Il est rouge sur la base (« b » y sort `ok`, comme dans la sonde S-B1 du réviseur).
- **C-2 (DNS)** :
  - (a) Un prédicat `repond` vérifie identifiant, bit QR, une seule question et la même. Tout datagramme non apparié est ignoré et l'attente continue. `forme` est réservé à une réponse appariée mal formée.
  - (b) Une adresse qui n'est pas une IPv4 littérale canonique (forme rendue par `ipaddress`) donne `forme`, sans exception, sans résolution et sans envoi.
  - Les tests couvrent S-D1, S-D2, S-D7, S-D8 et S-D9, plus un datagramme à deux questions et un datagramme court.
- **C-3 (TLS)** :
  - (a) `CONTEXTE` est armé comme le contexte d'urllib : ALPN `http/1.1` et `post_handshake_auth`. J'ai mesuré la ClientHello avec l'outil du réviseur, avant et après. Avant : 11 extensions. Après : `[0, 11, 10, 35, 16, 22, 23, 49, 13, 43, 45, 51, 21]`, identique à urllib sous Python 3.10 à 3.13 (OpenSSL 3.0.13).
  - (b) Tests sans réseau :
    - les attributs de `CONTEXTE`, lus sur une ClientHello écrite en mémoire (CERT_REQUIRED, contrôle du nom, ALPN, extension 49) ;
    - le chemin réussi, par une couche TLS injectée qui note `server_hostname` et la poignée, avec la phase `tls` journalisée.

    Ces tests tuent MG-01, MG-02 et MG-03.
- **C-4 (horloge, ferme SHOGEN-S2BIS-HORLOGE-RECUL-JOURNAL-1)** :
  - Les délais de `lire` et `interroger` se comptent sur `time.monotonic`. Les instants restent journalisés sur l'horloge murale.
  - La `sante` porte un nouveau champ `horloges` = `{murale, monotone}`. C'est le temps écoulé depuis le relevé précédent, sur chacune des deux horloges, en valeurs brutes. Un recul de l'horloge murale s'y lit `murale` < `monotone`.
  - Tests : S-C1, S-C2, recul de 180 s injecté entre deux fenêtres.
  - FORMAT §10.2, §11.6, §12 et §13.1 sont mis à jour.
- **C-5 (sondes bornées)** :
  - Une sonde dont l'instance précédente n'a pas rendu n'est pas relancée : elle vaut null. Une sonde qui lève vaut null et repart à la fenêtre suivante.
  - Le nombre de sondes encore en cours est journalisé (`fils.sondes`).
  - Test : sondes pendues sur trois fenêtres. Il y a 3 fils de sonde en tout, le même nombre à chaque fenêtre, contre 9 sans la correction.
- **C-6 (tests de la boucle bornés en temps)** : `test_boucle` et `test_sante.Branchement` font tourner la boucle dans un fil joint en 5 s, avec un helper partagé `borne`. M-LP-3, rejoué par la commande du job, sort maintenant en **1** en 76 à 79 s ; il pendait la suite.
- **C-7 (vivants à tuer)** : MG-11, MG-13, MG-18, MG-19, MG-21, MG-23, MG-24, MG-26, MG-29 et MG-31 sont tous tués, chacun par un test nommé, avec le rouge montré sur le mutant. MG-21 et MG-23 l'ont été sous une forme réécrite (même mutation, texte changé par CB-11f et CB-11e). MG-22 reste vivant, comme le réviseur l'a jugé équivalent en pratique.
- **O-5** : le futur d'une lecture rend toujours une `Lecture`. Une BaseException suit son cours, elle n'est pas masquée, et `abandonnes` ne surcompte plus. Un retour qui n'est pas une `Lecture` donne `autre`.
- **O-7** : sans sondes, la `sante` reste complète (champs nuls, `fils.sondes` à 0).
- **Q2** : j'ai mis le motif de l'écart ThreadPoolExecutor dans FORMAT §11.7. Texte proposé pour le JOURNAL, à consigner par l'orchestrateur : « Écart à la lettre de l'ADR-0029 l.235 (« concurrent.futures ») : futurs `concurrent.futures.Future`, `wait`, `BoundedSemaphore` et fils démons, sans ThreadPoolExecutor. Ce dernier joint ses fils à la sortie de l'interpréteur, même après `shutdown(wait=False, cancel_futures=True)` : un fil de lecture pendu bloquerait l'arrêt (essais du worker et du réviseur, Python 3.10 à 3.13). FORMAT §11.7 porte le motif (diff CB-11c). »
- **SHOGEN-S2BIS-MUT-COMMANDE-1** : toutes mes campagnes passent par `outils/campagne_job.py`. Il lit la ligne du job dans `gates.yml` (suite entière, `--egal`, plancher de l'état), la lance sous python3.12 en réseau isolé, avec une borne de 300 s. Sortie 1 = tué, 0 = vivant ; sortie 3, toute autre sortie ou borne dépassée = FATAL (groupe de processus tué).

## Livraison

| diff | objet | code ajouté | plancher exact | rouge sur l'état précédent | mutants (commande du job) |
|---|---|---|---|---|---|
| CB-11c | C-1, C-6, O-5, MG-11/13/29 | 162 | 97 | 3 tests | 14/14 (dont M-LP-3 sorti en 1) |
| CB-11d | C-5, O-7, MG-26 | 107 | 101 | 6 | 11/11 (rejoué après retouche : 11/11) |
| CB-11e | C-4, MG-23 | 143 | 106 | 17 | 12/12 |
| CB-11f | C-2, MG-18/19/21/24 | 69 | 111 | 8 | 12/12 |
| CB-11g | C-3, MG-31 | 87 | 114 | 1 | 10/10 |

- La suite passe de 92 à 114 tests.
- Chaque état est vert seul : `verdict-suite-s2.py s2bis --aucun-saut --egal --plancher N`, rc 0, `Ran` = N.
- Les tests qui ne tuent qu'un mutant sont verts sur la base, par construction : MG-11, MG-29, MG-18, MG-19, MG-24, MG-26, MG-31, et le chemin TLS réussi. Leur rouge est montré sur le mutant, dans les campagnes.

**Rejeu final par la commande du job** (fait deux fois, v1 puis v2 après la retouche de relecture ; résultats identiques) :

| jeu | mutants | tués | vivants | inapplicables (texte changé) |
|---|---|---|---|---|
| `mutants_g2.py` du réviseur | 30 | 24 | 1 (MG-22) | 5 |
| `mutants_g2_b.py` du réviseur (MG-31) | 1 | 1 | 0 | 0 |
| M-LP du worker | 14 | 11 | 0 | 3 (M-LP-1a, M-LP-6, M-LP-8) |
| formes réécrites des 8 inapplicables | 8 | 8 | 0 | 0 |

**Gates sur la copie complète (tête + 8 diffs + 5 diffs)** :
- Python 3.10 à 3.13 en `-X dev -W error` : 114 tests OK, 0 avertissement.
- Ligne du job sous chaque version : conforme, rc 0.
- Runner : 32 ok. Hooks : 54 ok.
- Suite S2 : 405 tests OK, 2 sauts nommés ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée.
- Secrets (index et `--tree`) : OK, 14 fichiers.
- R-13 : 0 dans les fichiers du lot.
- R-8 : bibliothèque standard seule (`ipaddress`, `contextlib`, `queue`, `unittest.mock`).
- xtask : S-G1 à S-G8, fmt, no_std et clippy verts. S-G9 rouge seulement sur `docs/17:70` (copie sans `docs/rapports`). Les lignes de verdict sont identiques à celles du témoin t0 du réviseur.
- Sous charge (8 boucles actives, 2 passages, refait après la retouche) : OK.

## Écarts à adjuger

- **E-1, relevé des sondes** : j'ai étendu C-1 aux sondes, mais seulement « inachevée au relevé = null ». La règle `fin` > E n'est pas appliquée aux sondes, car leurs instants ne sont pas dans le même domaine d'horloge dans les tests. Une sonde rendue entre E et le relevé (quelques ms de dépassement de l'attente) est donc gardée.
- **E-2, `fils.abandonnes`** : le compte inclut les lectures de la fenêtre rendues après E. Elles n'étaient pas finies à E ; FORMAT §11.6 est reformulé en ce sens.
- **E-3, O-7** : je l'ai traitée par des champs nuls quand il n'y a pas de sondes, et non en rendant `sondes` obligatoire. Le contrôle du câblage reviendrait à CB-18, comme I-B4 pour O-6.
- **E-4, C-4** : le nom et la forme du champ (`horloges`, deux temps écoulés, null à la première fenêtre) sont de mon choix. Le temps écoulé entre `depart` et le début de `lire` se lit sur l'horloge murale, borné à 0 ; une avance de l'horloge murale dans cet intervalle raccourcirait le délai. Cette limite est déclarée au FORMAT §10.2.
- **E-5, C-3** : j'arme `CONTEXTE` par deux lignes au niveau du module. Ainsi MG-02 et MG-03 restent applicables tels quels. `post_handshake_auth` est posé sans le test `is not None` que fait http.client ; c'est sans effet sur 3.10 à 3.13, où la ClientHello mesurée est identique à celle d'urllib.
- **E-6, mutants réécrits** : 8 mutants du réviseur et du worker ne s'appliquaient plus au texte changé. Je les ai réécrits avec la même mutation : MG-12, MG-17, MG-21, MG-23, MG-27, M-LP-1a, M-LP-6, M-LP-8.
- **E-7, retouche de relecture après les premières campagnes** :
  - une assertion de `test_sonde_pendue_jamais_relancee` dépendait de l'ordre des fils : je l'ai rendue indépendante de l'ordre ;
  - j'ai reformulé FORMAT §11.6 et §10.2 ;
  - j'ai ajouté le rejeu final à METRIQUES.

  Après cette retouche, j'ai refait les états, le rouge de CB-11d, la campagne de CB-11d, le rejeu final, les gates et la charge.
- **E-8, incidents de procédure, sans effet sur les résultats** :
  - `METRIQUES` de e2 et e3 avait été copié trop tôt : je l'ai reconstruit, puis vérifié chaque pas (e_k + diff = e_{k+1}) ;
  - une attente `pgrep -f` se retrouvait elle-même : arrêtée (sortie 144) ;
  - l'essai TLS du réviseur avait écrit des `__pycache__` dans e4 et e5 : retirés, diffs vérifiés propres ;
  - le mutant M-11e-06 visait le mauvais test ; il est tué par `test_delai_reseau_forme_et_identifiant_aleatoire`.
- **E-9, exposition** : une sortie de `ps` (vers 01:35 UTC) a affiché la ligne de commande d'un processus du harnais, avec un identifiant de session. C'est le même cas que E-R4 du réviseur. Aucune pièce du dépôt ni de D.2 n'a été lue. Aucune recherche récursive sur `docs/`, le dépôt ou le scratchpad entiers.
- **E-10, réseau** : `essai_hello.py` (MemoryBIO), les essais `ipaddress` et la gate des secrets (git local) ont tourné hors `unshare -n`, sans ouvrir de socket. Tout le reste a tourné sous `unshare -n`.

## Items proposés (règle PAROXYSME)

1. **SHOGEN-S2BIS-SOMMEIL-MURAL-1** : le sommeil par défaut de la boucle convertit une seule fois l'instant mural en durée.
   - Mesure (`essais/sonde_sommeil_mural_2.py`) : un recul de 1 s pendant le sommeil fait partir les lectures 1 s trop tôt (`d2.retard_max` = −999 772 µs). `horloges` journalise bien ce recul : `murale` 999 904 µs contre `monotone` 1 999 905 µs.
   - Un recul avant le premier relevé d'une exécution ne se voit que par un `retard_max` négatif.
   - Proposition : dormir jusqu'à l'instant mural, en boucle (environ 5 lignes et 1 test). Déclencheur : G0 de CB-18.
2. **Sondes** : appliquer ou non `fin` > E aux sondes (E-1). À trancher par l'orchestrateur.
3. **Citations de RFC** dans les docstrings des tests (RFC 1035 §4.1.4, RFC 7301 §3.1, RFC 8446 §4.1.2 et §4.2.6) : non relues en session, le réseau étant interdit, donc [2nd]. Les valeurs testées, elles, sont mesurées sur la ClientHello d'urllib. À vérifier sur pièce.
4. **O-10** (identifiant hors 16 bits donne `struct.error`) : non traité, hors liste.

## Journal G1

**Sources lues [lu]** :
- les briefs (corrections, G2, P1-B) ;
- `G2-P1B-transcrit.md` et `RAPPORT-WORKER-P1B-transcrit.md` ;
- G0 `G0-COLLECTE-RECALC-DEPLOI.md` ;
- PROPOSITION l.164-190, 225-260, 325-335, 362-368 ; AVIS, lignes trouvées par grep (Q-C-02, 03, 15) ;
- ADR-0029 l.228-242 (l.235 : `concurrent.futures`) ;
- ANNEXE-B l.992-1015 (B.60) ; G2-P1A l.145-155 et 396-404 (N-3) ;
- FORMAT et METRIQUES de la base ;
- tout le code et tous les tests `s2bis/` de la base ;
- les sondes, mutants, outils et preuves du réviseur (`g2/travail`) ; les outils et mutants du worker ;
- `verdict-suite-s2.py` ; le job `s2bis-unittest` de `gates.yml` ;
- http.client 3.10 l.1438-1450 et 3.12 l.824-836 ; urllib/request.py 3.12 l.1379-1392 ;
- `s2-harness/shogen_s2/sources.py` l.36-80 ; en-tête de `gate-secrets.sh`.

**Sources [2nd]** : les sections de RFC (item 3) ; PEP 644 (OpenSSL ≥ 1.1.1 depuis Python 3.10).

**Commandes et sorties** : elles sont dans `preuves/`. Toutes les sorties citées ci-dessus viennent de mes propres lancements ; aucun chiffre de seconde main. Principales pièces : `etats.txt` et `etats-2.txt`, `rouges.txt`, `*-mutants*.txt`, `final-*`, `clienthello-avant-apres.txt`, `sonde-sommeil-mural*.txt`.

**Chiffres recomptés** :
- lignes de code ajoutées par `outils/compte.py`, confirmées par `git apply --numstat` ;
- lignes des fichiers par `wc -l` ;
- tests par le `Ran` du vérificateur ;
- recensement des barres obliques inverses avant et après : un seul changement voulu, `\r\n` dans l'en-tête servi octet par octet de `test_http_reseau.py`, contrôlé par `od -c`.

## Pièces

Tout est dans `<scratchpad>/s2bis/p1b/corr/` :
- **Diffs** : `diffs/CB-11c.diff` … `diffs/CB-11g.diff`
- **Empreintes** : `SHA256SUMS` (111 lignes, sha256 `e67dae394baaea2762a9cdfd9abae439ba611a0b09d2195c72881f420e2a2edc`)
- **Arbres** : `etapes/e0` à `etapes/e5` (mini-arbres d'étape), `final/` (copie complète)
- **Lanceur** : `outils/campagne_job.py`
- **Jeux de mutants** : `mutants_cb11c.py` … `mutants_cb11g.py`, `mutants_reecrits.py`
- **Preuves** : `preuves/`