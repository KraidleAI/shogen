# Contre-contrôle des corrections C-1 à C-6 : tranche A du collecteur de S2-bis (diffs CB-2d et CB-2e)

- **Réviseur** : l'auteur de la relecture G2 (`G2-P1A.md`), qui n'a écrit aucune des corrections.
- **Gate 0** : modèle résolu **`claude-opus-5-5`** (identifiant exact déclaré par le harnais) ; effort `max` déclaré par
  la commande.
- **Horloge** (`date -u`) : début 2026-10-04 22:07:42 UTC ; rédaction à 22:22:22 UTC.
- **Commande** : message de l'orchestrateur, transmis par le coordinateur. **Lecture de C-1 adjugée** :
  - après un redémarrage, `ws ≤ dernière` est refusé ;
  - dans une même exécution, seul `ws < dernière` est refusé.
- **Brief du worker** : `corr/BRIEF-CORRECTIONS-P1A.md`, sha256 `36cda104…1134`.
- **Pièces du worker** : `corr/SHA256SUMS`, 74 lignes OK (`sha256sum -c`). Diffs `CB-2d.diff` (`8c4593ec…9f57`) et
  `CB-2e.diff` (`42ca2709…6c0e`).
- **Dépôt** : lecture seule, aucune opération git en écriture ; `git status` vide à la fin.
  - Tête au début : `b742e3c`, 7 commits après `86c07ff`, tous sous `JOURNAL.md` et `docs/adr-0029/etude-marche/`.
  - Tête à la fin : `b9ba2b4`. Ce commit ne touche que `JOURNAL.md`, `biblio/INDEX.md` et un ajout daté de l'ADR-0029
    (sources des rotations, côté recalcul).
  - Aucun de ces commits ne touche un chemin du lot.
- **Écritures** : `scratchpad/s2bis/p1/g2/` seulement (ce rapport, `contre/`).

## Verdict : CONFORME

- C-1 à C-6 sont tenues telles que je les ai écrites, avec la lecture de C-1 adjugée par l'orchestrateur ; Q-2 est
  tenue.
- Aucune reprise n'est demandée.
- Je ne peux pas donner d'avis sur les items I-C1 à I-C4 : leur texte n'est dans aucune pièce écrite (§6). Ce manque
  est rendu à l'orchestrateur.

## 1. Application en série, tailles

**Sur `b742e3c`.**
- `git archive HEAD` avec les exclusions habituelles donne 711 fichiers.
- Les neuf diffs (CB-0a à CB-2c, puis CB-2d et CB-2e) passent `git apply --check` puis `git apply`, en série : 726
  fichiers.
- Les 13 fichiers changés par CB-2d et CB-2e sont égaux aux empreintes `cb2e/…` du worker (13 sur 13).

**Sur `b9ba2b4`**, tête à la fin : même application, 726 fichiers ; les fichiers du lot sont identiques à l'octet
(`diff -rq`).

**Lignes de code ajoutées** (`git apply --numstat`, documents hors compte) :

| diff | code | documents | retirées | fichiers |
|---|---|---|---|---|
| CB-2d | 196 | 57 | 48 | 9 |
| CB-2e | 129 | 42 | 33 | 10 |

Les deux sont sous 200 lignes de code (R-25).

**Chaque état passe seul** (vérificateur avec la ligne de son propre `gates.yml`, réseau isolé) :

| état | ligne du job | 3.10 à 3.13 | runner |
|---|---|---|---|
| après CB-2d | `--aucun-saut --plancher 42` | 42 tests, conforme | 27 ok |
| après CB-2e | `--aucun-saut --egal --plancher 49` | 49 tests, conforme « Ran = 49 » | 32 ok |

**Autres gates sur l'état final.**
- Suite s2bis sous `-X dev -W error` (3.10 et 3.13) : 49 tests, 0 avertissement.
- Suite S2 par le vérificateur sans option : 405 tests, OK (skipped=2), conforme ; message inchangé (« Ran ≥ 405 »).
- R-8 (mon balayage `ast`) : bibliothèque standard seule ; un seul module neuf, `errno`, dans les tests.
- R-13 (motif exact de g5, index jetable) : sortie 1, 0 ligne.
- Secrets `--tree` : 717 fichiers, OK.
- Hook : 54 cas.
- `xtask`, sur `b742e3c` + 9 diffs, sur la base `b742e3c`, et sur `b9ba2b4` + 9 diffs :
  - S-G1 à S-G8 vertes ;
  - S-G9 rouge sur 1 violation, `docs/17-modele-de-menace.md:70`, la même avec et sans le lot ;
  - `fmt`, `no_std` et `clippy` verts ;
  - aucun téléchargement de `cargo`.

**Contrôle (1) : conforme.**

## 2. Chaque correction, telle qu'écrite

| correction | ce que le code et les tests font | preuve |
|---|---|---|
| **C-1 (a)** | `_fenetre` pose `suivante = ws` après chaque enregistrement de fenêtre : dans l'exécution, `ws < dernière` est refusé et l'égalité admise ; `marqueur` porte ensuite `suivante` à ws + w. | S-3 et S-4 refusés (`JOURNAL/fenetre`, octets inchangés) ; test `test_fenetre_anterieure_a_une_fenetre_ecrite_refusee` |
| **C-1 (b)** | `_lire` tient `derniere` : `ws` de tout type sauf `ouverture`, `point`, `cloture`, `reprise` et `trou` ; entier exigé. `_reprendre` la cherche au besoin dans les fichiers précédents et pose `suivante = max(attendu, (dernière ou 0) + w, ws + w)`. Après un redémarrage, `ws ≤ dernière` est donc refusé. | S-1 et S-2 refusés ; tests `…horloge_reculee_sans_doublon…` et `…redemarrage_dans_la_fenetre_du_dernier_marqueur` (m4 refusé), `…derniere_fenetre_cherchee_dans_le_fichier_precedent`, `…queue_fenetre_non_entiere` |
| **C-1 (c)** | Prémisse de `test_cause_remise_a_saut_par_un_marqueur_sans_trou` réécrite (journal sans fenêtre entamée), non supprimée. | diff de `test_trous.py` |
| **C-1 (d)** | Mutants « dernière non restaurée » et « monotonie retirée » tués : D-01 et D-02 du worker ; X-01 et X-02 à moi. | §3 |
| **C-2** | Le décorateur `_terminal` couvre `ouvrir`, `ecrire` et `marqueur`. Une `OSError` pose `casse` et remonte ; tout appel suivant lève `JOURNAL/casse` sans écrire. `fermer` rend le verrou dans un `finally` ; `_clore` oublie le descripteur avant de le fermer. | S-5 : marqueur réessayé refusé, marqueurs m1 et m2 sans doublon. S-6 : appels suivants refusés ; après reprise, queue déclarée (40 octets) et `sha256sum -c` OK. Sonde de plus : `fsync` en échec pendant la reprise, puis refus, puis instance suivante ouverte. Tests `…fsync_en_echec…`, `…ecriture_partielle…`, `…fermer_rend_le_verrou…`, `…bascule_en_echec_puis_fermer`. |
| **C-3** | `canonique` sérialise d'abord : `json` détecte le cycle, `ValueError` donne `JOURNAL/type`. Le parcours vient ensuite et se termine. Un partage sans cycle reste admis. | S-7 : refus immédiat (« Circular reference detected ») ; test sous délai de 5 s |
| **C-4** | (a) cas C-06 ; (b) cas C-07 ; (c) K-01 et K-02 refusent les lignes `if:` et `- if:`. | runner 32 sur 32 ; M-28, M-29 et M-32 tués |
| **C-5** | Tests neufs ou renforcés à valeurs écrites à la main, pour G-01 à G-08, G-10, G-11, G-13, G-19, G-20, M-07, M-18 et M-26. | §3 : tous tués |
| **C-6** | (a) Contrôle préalable `_ligne` au rang réel (seq + 1 + 2 × bascule + trou ; `prec` fictif de même longueur) avant toute bascule et tout trou ; docstring rendue vraie. (b) FORMAT §3.2 réécrit, règle de C-1 ajoutée, §7.5 vrai. (c) FORMAT §4 : arrêt sur erreur. (d) METRIQUES : campagnes du réviseur. (e) G6 : POSIX. | S-11 : refus sans bascule ; tests `…refus_n_ecrit_ni_trou_ni_bascule`, `…controle_au_rang_reel…` |
| **Q-2** | `--egal` (Ran = plancher) réservé au job s2bis ; K-02 l'exige ; le défaut du job S2 est inchangé. | V-16, V-17, C-08 ; X-14, X-15, X-20 tués |

**Rouge montré par moi.**
- Tests de l'état final contre le `journal.py` d'avant les corrections : FAILED (10 échecs, 4 erreurs), tous sur des
  tests de C-1, C-2, C-3 ou C-6.
- Runner final contre l'ancien vérificateur : `TypeError` (`egal`).
- Runner et vérificateur finaux contre l'ancien `gates.yml` : K-02 en échec.

**Sondes S-1 à S-7 et S-11**, rejouées sans changement (`reprise/outils/sondes_g2.py`, `65fb54ef…`) : toutes rendent le
comportement exigé (`preuves/sondes-contre.txt`). S-4 et S-7 finissent sur l'exception nommée elle-même, ma sonde ne
l'attrapant pas.

**Contrôle (2) : conforme.**

## 3. Mutants rejoués avec mon lanceur

**Lanceur.** `contre/outils/campagne2.py` : mon lanceur de la G2, même contrat (sortie 1 = tué, 0 = vivant, toute
autre sortie ou fragment inapplicable = FATAL ; témoin vert ; copie fraîche).
- Deux différences avec le lanceur de la G2 :
  - réseau isolé par `unshare -n` et `isole.py`, sans shell : le harnais a bloqué une commande `sh -c`, qu'il ne pouvait
    pas analyser ;
  - une cible « job » : la ligne du vérificateur, lue dans le `gates.yml` muté et lancée telle quelle.

**Résultats :**

| jeu | mutants | tués | vivants | FATAL |
|---|---|---|---|---|
| `mutants_g2.py`, sans changement | 41 | 36 | 0 | 5 (fragments inapplicables : M-12, M-20, M-31, M-33, M-47) |
| `mutants_prec.py`, sans changement | 32 | 30 | 0 | 2 (inapplicables : G-18, G-26) |
| mes réécritures des 7 fragments (`mutants_contre.py`, partie A) | 8 | 7 | 1 (G-26 contre le runner seul, attendu) | 0 |
| mutants neufs sur les corrections (partie B) | 19 | 19 | 0 | 0 |
| mutants propres du worker, rejoués | 30 | 30 | 0 | 0 |

Pour les mutants que la G2 marquait « aucun test attendu » ou « non précisé », le test qui les tue maintenant est l'un
des tests neufs.

**Les 7 fragments réécrits par le worker : même mutation ?**
- **M-20, M-31, M-33** : identiques sur le nouveau texte. La condition de trou est devenue une variable ; la ligne du job
  porte `--egal --plancher 49`.
- **M-47 et G-18** : `os.close(verrou)` devient `pass` ; même effet, le verrou n'est jamais rendu.
- **G-26** : même mutation, plancher ramené à 1, sur la nouvelle ligne. Le worker change la cible (« job »).
- **M-12 : non identique, plus forte.**
  - L'original retirait le seul terme `ws + w` (fenêtre du redémarrage admise).
  - La réécriture `suivante = attendu` retire aussi le terme de C-1.
  - J'ai rejoué la forme fidèle, `max(attendu, (dernière ou 0) + w)` : tuée par son test visé
    (`…fenetre_du_redemarrage_refusee`). La réécriture forte ne masquait donc aucune faiblesse.
  - Je recommande de garder la forme fidèle au jeu de référence (OC-1).

**Mutants neufs, tous tués par le test visé :**
- X-01 : monotonie retirée ;
- X-02 : dernière fenêtre non restaurée ;
- X-03 : dernière fenêtre non cherchée dans les fichiers précédents ;
- X-04 : une lecture ne compte pas comme fenêtre écrite ;
- X-19 : `ws` non entier admis ;
- X-05, X-06 : état terminal jamais posé, ou jamais lu ;
- X-07 à X-09 : `marqueur`, `ecrire` ou `ouvrir` hors de l'état terminal ;
- X-10 : verrou rendu seulement sans erreur ;
- X-17 : descripteur non oublié avant sa fermeture. Il est tué par le nettoyage de
  `…fermer_rend_le_verrou…`, qui refermerait le numéro ;
- X-11a : cycle non nommé ;
- X-11b : parcours avant le sérialiseur, tué par le délai du test (22 s) ;
- X-12 : contrôle préalable retiré ;
- X-13 : contrôle au mauvais rang ;
- X-14, X-15, X-20 : `--egal`.

**Contrôle (3) : conforme.**

## 4. G-26 contre le runner seul : acceptable

Oui. Le runner contrôle le câblage :
- présence de `--egal` (X-20 tué) ;
- étape du runner avant celle du vérificateur ;
- absence de `if:` et de `continue-on-error`.

Il ne compte pas les tests, et ce n'est pas son rôle. La justesse d'un plancher se juge contre le compte réel, que mesure
l'étape du job. Avec `--egal`, le job refuse tout plancher différent du compte : « Ran 49 > plancher 1 (--egal) »,
A-G-26j tué. Le plancher abaissé est donc tué par la gate elle-même.

Une condition (OC-2). Tant que la forge ne lance pas les jobs (GC-01), le G3 opérant de l'orchestrateur doit lancer la
ligne du job s2bis **telle qu'elle est écrite dans `gates.yml`**, `--egal` compris. Ni la suite nue, ni un plancher tapé
à la main. Je recommande que les entrées G3 du JOURNAL citent cette ligne.

## 5. Rien d'autre n'a changé

Lecture complète des changements des 13 fichiers entre la série relue (u7) et l'état final (u9), et de `journal.py`
final en entier.
- **Inchangés** : `config.py`, `tests/__init__.py`, `test_fitness.py`.
- **Chaque changement se rattache à C-1 à C-6 ou à Q-2** :
  - `journal.py` : C-1, C-2 (`_terminal`, `fermer`, `_clore`), C-3, C-6 ;
  - tests ; vérificateur (`--egal`) ; runner (C-4, Q-2) ;
  - `gates.yml` : plancher 34, puis 42, puis 49 et `--egal` ;
  - FORMAT, G6, METRIQUES.
- **Hors lettre, mais justifiés** :
  1. La ligne qui avançait l'état après un trou est retirée. Avec le contrôle préalable de C-6, un marqueur ne peut plus
     échouer qu'en `OSError`, donc en état terminal : la ligne était morte. C'est écrit à METRIQUES. Aucun test de la
     G2 ne s'en trouve affaibli : G-15, G-16 et les tests de trous restent tués ou verts.
  2. Le message de refus passe de « close » à « passée » (C-1).

**Contrôle (5) : conforme.**

## 6. Items I-C1 à I-C4 du worker : avis impossible ([abs])

Leur texte n'est dans aucune pièce écrite. J'ai cherché dans les deux diffs, `corr/`, `corr/tmp/`, `corr/verif*/` et
`corr/rouge*/` ; le rapport du worker n'est pas en fichier, et le message de commande ne les reproduit pas. Je donnerai
mon avis sur leur texte, transmis tel quel.

En attendant, voici les suites que j'aurais moi-même formées :
- **OC-3** : le G0 de CB-4 doit dire ce que fait la boucle sur une `OSError` ou sur `JOURNAL/casse` : fermer et sortir,
  systemd relançant le service. FORMAT §4 dit seulement que l'erreur remonte à l'appelant.
- **OC-4** : les observations O-2, O-4, O-5 et O-7 à O-11 de la G2 restent ouvertes, hors liste C ; à porter aux G0
  cités.

## 7. Observations du contre-contrôle (non bloquantes)

- **OC-1** : garder la forme fidèle de M-12 au jeu de référence (§3).
- **OC-2** : G3 opérant fidèle à la ligne du job (§4).
- **OC-3** et **OC-4** : voir le §6.
- **OC-5** (exposition) : la sortie S-G9 de `xtask` nomme la cible du renvoi de `docs/17:70`, un fichier de
  `docs/rapports/` absent de ma copie et non ouvert. Le nom figure donc dans ma transcription.

## 8. Journal de provenance

### Lu [lu]
- Le brief de correction ; `corr/SHA256SUMS` ; les deux diffs, au travers des changements u7 → u9 des 13 fichiers, lus
  en entier.
- `journal.py` final, en entier.
- Côté worker : `corr/outils/mutants_g2_final.py`, `mutant_g26_runner.py`, `mutants_cb2d.py` (en-tête) ;
  `preuves/final-2159/campagnes.txt`.

### Commandes et sorties
Sorties sous `g2/contre/preuves/`.

| contrôle | commande | sortie |
|---|---|---|
| (1) | `git archive` puis 9 × `git apply --check` et `git apply`, sur `b742e3c`, puis sur `b9ba2b4` | §1 |
| (1) | `--numstat` ; `sha256sum -c` des empreintes `cb2e/` | §1 |
| états | ligne du job de chaque `gates.yml`, 3.10 à 3.13, `unshare -n` | `job-u8-*`, `job-u9-*` ; runner `runner-u9.txt` (`ccefcbd5…`) |
| S2 | vérificateur sans option, `python3.12`, réseau isolé | 405, OK (skipped=2), de 22:11:53 à 22:12:40 UTC (`verdict-s2-defaut.txt`, `ce553a6e…`) |
| sondes | S-1 à S-7, S-11 ; sommes après écriture partielle ; `fsync` en échec à la reprise | §2 (`sondes-contre.txt`, `decbb9f0…`) |
| rouge | tests finaux contre `journal.py` de u7 ; runner contre l'ancien vérificateur et l'ancien `gates.yml` | `rouge-suite.txt` (`03f8daa0…`), `rouge-runner*.txt` |
| mutants | `campagne2.py` (`7047f386…`) avec `isole.py` (`d1b90939…`) | `mutants-g2-sur-u9.txt` (`b19e4479…`), `mutants-prec-sur-u9.txt` (`3f34b7cd…`), `mutants-contre.txt` (`395dee65…`), `mutants-worker-cb2d.txt` (`a7ffad58…`), `mutants-worker-cb2e.txt` (`0da8c1d0…`) |
| jeux de mutants | `mutants_contre.py` (`a6e01130…`) ; copies des jeux du worker (`4e430e57…`, `4e4e96eb…`, égales à son `SHA256SUMS`) | — |
| gates | R-8 (`ast`) ; R-13 (`git grep`, index jetable) ; secrets ; hook | §1 |
| xtask | `cargo --locked xtask verify`, détaché, cible dédiée | `xtask-final.txt` (`60c0e49c…`), `xtask-base.txt` (`d32d1edd…`), `xtask-tete2.txt` (`ced10b92…`) |

### Jamais ouverts
- Les dossiers interdits ; aucune pièce de D.2.
- Aucun `*.jsonl` réel. Les journaux des sondes et des tests sont synthétiques, écrits dans mon `TMPDIR`.
- `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée.

### Aucune opération réseau
- Suites et mutants sous `unshare -n`.
- Sondes, runner, hook et secrets : processus locaux.
- `cargo` sans téléchargement.
