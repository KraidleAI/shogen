# Rapport du worker — corrections de RB-1 d'après la lettre du FORMAT (RB-1h à RB-1k ; transcrit)

> Transcription par l'orchestrateur le 2026-10-05 17:58:59 UTC du rapport rendu par message par le worker (agent a1ccbf20eedaeb933) ; contrôle FM-1.1 : fragments_l51_l14 = 0. Texte du worker ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`). Reçu pendant la pause demandée par l'investisseur : transcrit seulement, adjudication et contre-contrôle à la reprise.

# Rapport du worker : corrections de RB-1 (lecteur principal) d'après la lettre du FORMAT (C-14, C-15, C-1 à C-5), diffs RB-1h à RB-1k

**Gate 0** : modèle `claude-opus-5-5`, fiche `shogen-worker`, effort max.
- Travail du 2026-10-05, de 16:12:45 à 17:56:29 UTC (`date -u`).
- Dépôt en lecture seule : aucune écriture git, `--no-optional-locks` partout.

## Résumé

- **Base.** Copie de la tête **98c8537**, prise par `git archive` avec les exclusions du brief (vérifiées absentes). Le job y donne : classe 0, Ran 184, runner 77 ok.
  - Pendant le lot, l'orchestrateur a avancé la tête à 12ce67f puis à 47b2177. Voir E-8 et I-3.
- **Livraison.** Quatre diffs en série sur 98c8537 :

  | diff | objet | code ajouté | plancher exact (`--egal`) |
  |---|---|---|---|
  | RB-1h | C-14, lettres C-1 et C-2 (définition unique d'« intègre ») | 140 | 190 |
  | RB-1i | C-15 premier point, lettre C-3 (déclaration comparée sous forme canonique) | 58 | 192 |
  | RB-1j | C-15 second point, lettre C-4 (64 niveaux, comptés par le lecteur) | 69 | 194 |
  | RB-1k | lettre C-5 (grammaire des noms) | 49 | 195 |

  - Chaque diff reste sous 200 lignes de code ajoutées.
  - La série s'applique sur 98c8537 et redonne chaque état à l'identique (`diff -r`).
- **Tests d'abord.** Le rouge a été montré sur des souches (code d'avant, tests du diff). Échecs d'assertion : 15, 1, 4 et 1, avec 0 erreur.
- **Mutants**, classés par la commande du job (runner, puis la ligne s2bis de gates.yml ; borne 300 s ; python3.12 ; réseau isolé) :
  - 19 + 12 + 12 + 12 = **55 tués sur 55**, chacun par son test visé ; 0 vivant, 0 FATAL.
  - Rejeu sur l'état final : **46 sur 46** (42 mutants des trois premiers diffs, plus 4 mutants de preuve des points déjà conformes).
- **Contrôles finaux**, tous verts :
  - suite sous `-X dev -W error` en 3.10, 3.11, 3.12 et 3.13 : Ran 195, OK, 0 avertissement ;
  - ligne du job sous les quatre interpréteurs : conforme, Ran = 195 ; runner : 77 ok ;
  - `s2-harness` : Ran 406, OK (skipped=2) ; hooks : 54 ok ;
  - gate des secrets : OK sur les 4 fichiers touchés ; R-13 : 0 ;
  - `xtask` : lignes de verdict identiques au témoin (S-G9 sur `docs/17:70`, cas connu).
- **Sortie identique entre versions** : même sha256 global `a6dfea91…` sous 3.10 à 3.13, sur 16 journaux synthétiques. L'ancien code divergeait selon la version (voir C-4).

## 1. Tableau lettre par lettre

Les écarts ont été mesurés par sondes sur la tête (`preuves/sondes-base.txt`).

| lettre, point | écart trouvé | diff | test qui le fixe ou le prouve | mutants tués |
|---|---|---|---|---|
| C-14 a, `type` chaîne | `type` 5 ou null lu intègre | RB-1h | `test_champs_communs_et_objet` | M-1h-06 |
| C-14 b, `seq` entier non booléen (l.67) | `seq: true` admis (`True == 1` au lien) | RB-1h | `test_champs_communs_et_objet` | M-1h-01, 02 |
| C-14 c, `prec` hexadécimal en tête de fichier | `prec` de tête non contrôlé (absent, null, 63 ou 65 chiffres, majuscules) | RB-1h | `test_champs_communs_et_objet`, `test_tete_de_segment_non_integre_par_ses_types` | M-1h-03, 04, 05 |
| C-14 d, `a` d'un trou (l.71, `+ 0`) | `a: true` admis | RB-1h | `test_champs_propres_aux_types_du_paragraphe_2` | M-1h-01, 02 |
| C-15, déclaration sous forme canonique (l.146) | `==` lisait comme exacte une déclaration à `true`/`false` pour 1/0 | RB-1i | `test_declaration_exacte_sous_forme_canonique` (cas « booléens ») | M-1i-01, 02, 12 |
| C-15, borne d'imbrication | aucune borne | RB-1j | `test_imbrication_comptee_par_le_lecteur` | M-1j-01 à 09, 11, 12 |
| C-1, entier de plus de 640 chiffres : ligne non intègre | **déjà conforme** (`LECTEUR/entier-long`, quel que soit le réglage, signe exclu) | — | `test_entier_de_640_chiffres…`, `test_queue_finale_toleree…`, `test_causes_nommees` | M-P-01, 02 (rejeu final) |
| C-2 a, ligne de LIMITE octets au plus | **déjà conforme** (`readline(LIMITE)`) | RB-1h (preuve) | `test_ligne_de_limite_octets_integre_un_octet_de_plus_queue` (4 194 304 octets, puis un de plus) | M-1h-17, 18 |
| C-2 b, JSON canonique, UTF-8 en clair, objet | **déjà conforme** | RB-1h, RB-1i (preuves) | `test_caracteres_hors_ascii_en_clair` ; clés non triées dans `test_causes_nommees` ; ligne non objet dans `test_champs_communs_et_objet` | M-1h-12, M-1i-02, 12 |
| C-2 d, champs propres typés et présents | `jour`, `de`, `cause`, `queue`, `ws` d'un `point` et d'une `reprise` non contrôlés ; champ absent admis | RB-1h | `test_champs_propres_aux_types_du_paragraphe_2` (chaque champ, chaque type) | M-1h-07, 08, 10, 13 |
| C-2, un booléen n'est jamais un entier | dans tous les champs entiers du §2 et dans les déclarations | RB-1h, RB-1i | ci-dessus | M-1h-01, 02, M-1i-01 |
| C-2, `ws` null vérifié type par type (R-2) | `ws` null admis pour `lecture`, `sante`, `run_params`, `point`, `reprise` | RB-1h | `test_ws_null_type_par_type` | M-1h-09, 16 |
| C-2 e, chaîne dans le fichier | **déjà conforme** | — | `test_causes_nommees` (3 cas `chaine`), `test_lignes_integres_et_etat` | M-1h-14, M-P-03 |
| C-2 et C-3, §7.1 appliqué avant §7.4 | une `reprise` à `queue` objet nu était lue comme rupture `declaration` | RB-1h | `test_tete_de_segment_non_integre_par_ses_types` | M-1h-08 |
| C-3, ordre croissant (jour, k) | **déjà conforme** (ordre de lecture) | RB-1i (preuve) | cas « ordre décroissant » ; `test_deux_queues_declarees_ensemble_par_l_ecrivain` | M-1i-03, 09 |
| C-3, liste vide, null, champ de plus | **déjà conforme** | RB-1i (preuve) | même test ; `test_liste_vide_sans_queue_en_attente` | M-1i-04, 05, 06 |
| C-3, toutes les queues rendues avec la rupture ; lien rompu : déclaration non lue | **déjà conforme** | RB-1i (preuve) | cas « lien faux » et « ouverture » | M-1i-07, 08, 10, 11 |
| C-4, N = 64, racine au niveau 1 | 65 niveaux lus intègres | RB-1j | `test_imbrication_comptee_par_le_lecteur` ; cas imbrication de `test_queue_finale…` | M-1j-01, 02, 12 |
| C-4, niveaux comptés par le lecteur, jamais RecursionError | RecursionError devenait `LECTEUR/json` ; seuil variable selon la version (992 sous 3.10 et 3.11, 9 998 sous 3.12, 9 999 sous 3.13) | RB-1j | même test (100 000 niveaux), `test_causes_nommees`, `test_recursion_error_jamais_un_verdict` | M-1j-09, 10 |
| C-5, k suit `0\|[1-9][0-9]*` | `[0-9]+` : `-01`, `-00` et `-007` lus comme segments (deux segments 0) | RB-1k | `test_grammaire_des_noms_refus_nommes` | M-1k-01, 07, 12 |
| C-5, nom du préfixe hors grammaire : refus nommé | ignoré | RB-1k | même test (10 noms : `LECTEUR/nom`) | M-1k-03 à 06, 08, 10, 11 |
| C-5, dossier vide : refus nommé ; ordre (jour, k entier) | **déjà conforme** | RB-1k (preuve) | même test ; `test_ordre_de_la_chaine_et_journal_absent` | M-1k-02, 09 |

## 2. Diffs

| diff | sha256 | souche du rouge | campagne |
|---|---|---|---|
| RB-1h | `756a3311…2975` | `1-RB-1h-souche` | 19 sur 19, 26,7 à 28,0 s |
| RB-1i | `95551f07…e627` | `3-RB-1i-souche` | 12 sur 12 |
| RB-1j | `77746130…afffc` | `5-RB-1j-souche` | 12 sur 12 |
| RB-1k | `fdd7966f…3f00` | `7-RB-1k-souche` | 12 sur 12 |

**Code, RB-1h.** `_types` porte les points (c) et (d) : table `CHAMPS` du §2, `HEX`, types exacts par `type(v)`. `RESERVES` est tiré de `CHAMPS`. `_integre` suit l'ordre (a), (b), (c)-(d), (e).

**Code, RB-1i.** Nouvelle fonction `_canonique`, qui sert à la fois au contrôle de canonicité de la ligne et à la comparaison des déclarations.

**Code, RB-1j.** Nouvelle fonction `_trop_profonde`, qui compte les niveaux sur les octets, avant tout décodeur.
- Elle retire les échappements (barre doublée, puis barre et guillemet) ; les guillemets restants bornent les chaînes ; seuls les crochets hors chaînes comptent.
- La barre oblique inverse est écrite `bytes([92])`, donc aucun octet 92 n'est ajouté.
- `except ValueError` seul : RecursionError n'est plus rattrapée.

**Code, RB-1k.** `fichiers()` applique la grammaire, lève `LECTEUR/nom`, et garde `LECTEUR/absent`.

**METRIQUES.** Chaque diff ajoute sa section en fin de `METRIQUES-S2BIS.md` : objet, comptes, rouge, mutants et plancher. Le texte complet est dans les diffs.

**État final** :

| fichier | lignes | sha256 |
|---|---|---|
| `lecteur.py` | 203 | `94894d78…` |
| `test_lecteur.py` | 511 (31 tests) | `2745ff9b…` |
| `gates.yml` | — | `a62aa984…` |
| `METRIQUES-S2BIS.md` | 1 202 | `f424bfab…` |

- Ligne à committer : `--plancher 195`.
- Octets 92 : `lecteur.py` 2 → 2, `test_lecteur.py` 6 → 8 (deux `\n` ajoutés dans RB-1h, contrôlés par la position et l'octet suivant), `gates.yml` 4 → 4, METRIQUES 0 → 0.
- Toutes les lignes font au plus 120 caractères, sans espace ni tabulation en fin de ligne.

## 3. Rouges (assertion, 0 erreur)

- **RB-1h** : 15 échecs dans 4 tests.
  - 11 sous-tests des champs propres ; seuls `suivante` et le `ws` d'un `marqueur` étaient déjà typés.
  - Les champs communs, le `ws` null, et les deux têtes de segment, lues comme ruptures `declaration` et `lien`.
  - Les tests de preuve (a), (b) et l'état après un `point` passent déjà sur le code d'avant.
- **RB-1i** : 1 échec, la déclaration à booléens lue comme exacte.
- **RB-1j** : 4 échecs.
  - 65 niveaux intègres en listes, en objets et derrière une barre ; 100 000 niveaux nommés `json`.
  - RecursionError rattrapée.
  - Cause des 100 000 niveaux dans `test_causes_nommees`.
  - Ligne de 65 niveaux lue intègre en fin de fichier.
- **RB-1k** : 1 échec, premier nom non conforme lu sans refus. Sonde complète dans `preuves/rb1k-sondes-souche.txt`.

## 4. Questions (lettre muette) : mon choix et sa raison

- **Q-1. RecursionError sur une ligne de 64 niveaux au plus.** Ce cas ne peut venir que de l'environnement (pile de l'appelant épuisée).
  - Choix : l'exception remonte, sans verdict.
  - Raison : la ligne est intègre au compte ; tout verdict serait faux et dépendrait de l'environnement (« ne se fient pas à l'exception »).
- **Q-2. Noms des causes et ordre des contrôles.** La lettre fixe le verdict, pas la cause.
  - Choix : (a) `fin` ; (b) `imbrication`, puis `json`, `flottant`, `entier-long`, `canonique` ; (c) et (d) `champ` ; (e) `chaine`.
  - Conséquence pour le banc : comparer verdicts, positions, queues et ruptures, et non les noms de cause, sauf si l'orchestrateur fixe un vocabulaire commun.
- **Q-3. `ws` sur `ouverture`, `cloture` et `trou`.**
  - Choix : ce n'est pas un champ propre, il reste libre (null admis), comme dans `_types` de l'écrivain.
  - Raison : la définition n'est ni relâchée ni resserrée. Le mutant de resserrement M-1h-16 est tué.
- **Q-4. Ligne non JSON qui dépasse 64 niveaux au compte.**
  - Choix : cause `imbrication`, puisque le compte vient d'abord. Le verdict ne change pas.
- **Q-5. Moment du refus `LECTEUR/nom`.**
  - Choix : au début de l'itération, avant tout enregistrement rendu ; le dossier est listé une seule fois.
- **Q-6. Borne LIMITE.**
  - Choix : elle est tenue par la lecture (`readline(LIMITE)`), pas répétée dans `_integre`. Elle est fixée dans le flux à LIMITE et LIMITE + 1 octets.
- **Q-7. « Pas de numéros sur 3 chiffres ».**
  - Choix : je le lis comme « jamais complété de zéros », selon la parenthèse du FORMAT §6.1. `-007` est refusé ; `-100` est lu comme segment 100.
  - Raison : l'écrivain numérote 1 + max. M-1k-12 (k limité à deux chiffres) est tué.

## 5. Écarts déclarés

- **E-1.** `ls rb18/g2/` a affiché les noms des fichiers et dossiers de ce dossier. Seul le contenu d'`ADJUDICATION-FORMAT.md` a été lu ; rien d'autre dans `rb18/`.
- **E-2.** Deux `ps | grep` trop larges ont affiché des processus d'un autre worker (noms de processus seulement, rien touché). Ensuite, recherche restreinte à mes PID.
- **E-3.** Un `du -sh` sur ma copie entière du dépôt (taille seule). Je ne l'ai pas refait.
- **E-4.** Un heredoc non cité contenant des backquotes : substitution par bash, le script a échoué avant toute écriture, aucun fichier modifié. Ensuite, heredocs cités seulement.
- **E-5.** Passes non comptées, versées à part :
  - RB-1h, 16 mutants tués, avant les tests (a) et (b) ;
  - RB-1k, 11 tués, avant l'ajout du segment 100 ;
  - contrôles et `xtask` d'avant k = 100 ;
  - un rejeu final que j'ai interrompu (`kill` de mon groupe 31478) pour ajouter k = 100 ; il a été refait en entier.
- **E-6.** Des `__pycache__` ont été créés par un comptage lancé sans `-B`. Supprimés, diffs régénérés ; les campagnes les ignoraient déjà.
- **E-7.** Pendant un essai à blanc, un cas de test plaçait une `lecture` en tête de segment ; c'est une ligne non intègre, pas une rupture. Corrigé en `ouverture` avant de bâtir les états officiels.
- **E-8.** La tête a bougé pendant le lot (98c8537 → 12ce67f → 47b2177). Le code `s2bis`, les tests et le FORMAT n'ont pas changé ; la ligne 220 de `gates.yml` vaut encore 184. Je n'ai rien avancé moi-même.

## 6. Items à former (règle PAROXYSME)

- **I-1 (pour P1, écrivain).** `Journal._lire` décode avant de compter les niveaux.
  - Au-delà du seuil du décodeur, son verdict vient de RecursionError. Il est juste par coïncidence, mais la lettre n'est pas tenue à la lettre.
  - Avec une pile épuisée, une ligne intègre deviendrait une queue.
  - Proposition : compter sur les octets avant de décoder, comme RB-1j, ou déclarer la limite.
- **I-2 (banc).** Les noms de cause diffèrent par construction entre RB-1 et RB-18. Le critère « 0 discordance » doit porter sur les verdicts et les sorties, pas sur les causes (voir Q-2).
- **I-3 (recalage).** Sur 47b2177, le hunk METRIQUES de RB-1h ne s'applique pas tel quel (sections ajoutées en fin de fichier depuis).
  - La série sans `docs/` s'y applique, et le job passe : classe 0, Ran 195, runner 85 ok (`preuves/job-sur-47b2177-hors-docs.txt`).
  - Il suffit d'ajouter les quatre sections en fin de fichier.
- **I-4 (mesure).** Coût du compte des niveaux.
  - Une ligne de 4 Mio avec 2,8 millions de crochets : 97 ms (`json.loads` : 195 ms).
  - Une ligne ordinaire : moins de 10 µs.
- **I-5 (information pour le banc).** L'ancien lecteur rendait des verdicts différents selon la version, pour une ligne de 5 000 niveaux.
  - sha256 global `2fda355a…` sous 3.10 et 3.11, `45d28a87…` sous 3.12 et 3.13 ;
  - le lecteur corrigé donne `a6dfea91…` partout ;
  - RB-18 est à contrôler sur ce point (non lu par moi).

## 7. Journal G1

**[lu]**, préfixe du sha256 et plage lue :
- Pièces du lot, en entier :
  - le brief `9190c83e` ;
  - l'extrait `1c61019a` ;
  - l'adjudication `e6528325`.
- Mes pièces de la tranche 1, en entier :
  - `BRIEF-RB-T1` `29d75bd2` ;
  - le brief de corrections `c33bfcdb` ;
  - le rapport de corrections `34789235`.
- Source de la lettre : FORMAT de la tête `4f0a509b`, lu en entier (482 lignes).
- Code et tests de la tête :
  - `lecteur.py` `27d6adf6` et `test_lecteur.py` `2c1c1378`, en entier ;
  - `journal.py` `e12dbb4f`, en entier ;
  - `test_format.py` `ba6f1d42` et `test_fichiers.py` `cdb65da6`, en entier ;
  - `test_journal.py` `09315614` (l.1-100), `test_reprise.py` `fdb6556b` (l.1-50), `tests/__init__.py` (l.1-30).
- Contrat :
  - G0 `0e9001f3`, en entier, ajout daté Q-RB-13 et Q-RB-14 compris ;
  - PROPOSITION `0cdf84c2`, l.405-500 ;
  - AVIS `a919b307`, l.104-114, plus une recherche ciblée des mentions du lecteur.
- Pièces de CI et de documentation :
  - METRIQUES `beb6a9da` : l.1-20, 409-560, 870-962 et la fin ;
  - `gates.yml` `d606b4d2`, l.190-232 ;
  - `verdict-suite-s2.py` `6372cc85`, l.1-40 ;
  - `gate-secrets.sh` `f89abf0f`, l.1-30.
- Outils repris :
  - `job.py` `39084987`, copié à l'identique ;
  - `campagne_g2.py` `927a7475`, adapté pour copier aussi `docs/adr-0029/s2bis` ;
  - `isole.sh` `ebaa1c78`.

**[abs]** :
- Toutes les pièces de RB-18 hors de l'adjudication : `oracle_indep`, diffs, relecture, banc, contre-épreuve, `AVIS-FORMAT`.
- La RFC JSON, et la documentation des limites de récursion C ; j'ai mesuré moi-même à la place.

**[2nd]** : les chiffres du FORMAT (988 niveaux, M = 4). Je ne les ai pas utilisés ; mes propres mesures sont dans `preuves/seuil-recursion-avant-rb1j.txt`.

**Non ouverts** : aucune pièce de D.2, aucun `*.jsonl` réel, aucun dossier interdit. Aucune recherche récursive sur `docs/`, le dépôt ou le scratchpad. `SHOGEN_S2_CAMPAGNE_CONTROL` n'a jamais été posée.

**Chiffres recomptés** :
- `wc -l` des états :
  - `lecteur.py` : 147, 164, 172, 193, 203 ;
  - `test_lecteur.py` : 313, 408, 451, 481, 511 ;
- tests de la suite : 184, 190, 192, 194, 195 ;
- lignes de code ajoutées par diff (`diff.py`) ; rouges ; bilans des campagnes ; octets 92 ; seuils de récursion ; coût du compte.

**PID réels** :

| processus | PID |
|---|---|
| campagne RB-1h, première passe | 11323 |
| campagne RB-1h | 29042 |
| campagne RB-1i | 14518 |
| campagne RB-1j | 24663 |
| campagne RB-1k, première passe | 307 |
| campagne RB-1k | 7719 |
| contrôles finaux | 12404, puis 15577 |
| `xtask` | 30112, puis passe au premier plan |
| rejeu final | 31478 (interrompu), puis 28605 |

Aucun processus à moi ne reste.

## 8. Fichiers

Tout est dans `<scratchpad>/s2bis/rb1/corr2/` :
- **Diffs** : `diffs/RB-1h.diff`, `RB-1i.diff`, `RB-1j.diff`, `RB-1k.diff`.
- **Empreintes** : `SHA256SUMS`, 126 lignes, contrôlé par `sha256sum -c` ; son sha256 est `95e2d390…a1e4`.
- **Notes** : `NOTES.md`, journal de reprise.
- **outils/** :
  - mutants : `mutants_rb1h.py` à `mutants_rb1k.py`, `mutants_preuves.py`, `mutants_final.py` ;
  - campagnes et état : `campagne.py`, `job.py`, `rouge.sh`, `etats.sh` (rebâtit les neuf états depuis la tête et les diffs, vérifié identique), `verif_serie.sh` ;
  - contrôles : `final_controles.sh`, `xtask.sh`, `identite.py`, `seuil_recursion.py`, `octets92.py`, `habiller.py`, `diff.py`.
- **preuves/** : rouges, verts, campagnes, rejeu final, contrôles, sondes, seuils, coût, identité, `xtask`, vérification de la série ; les passes non comptées sont dans `v1-*/` et `interrompu/`.
- **travail/** : les fichiers de tests des souches et les scripts d'application.
- **Nettoyage** : copies du dépôt, états, `tmp` et cible cargo supprimés. Le dossier fait 1,4 Mo.
