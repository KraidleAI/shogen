# Relecture G2 neuve de DETTES-T2 (transcrit)

> Transcription par l'orchestrateur le 2026-10-15 13:51:21 UTC du fichier dettes2/g2/RAPPORT-G2.md ; contrôle FM-1.1 des transcripts du générateur-correcteur, du réviseur G2 et des deux contre-contrôleurs, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# DETTES-T2 (SHOGEN-CALIB-FORMES-API-1) : rapport de la revue G2

**Gate 0** : modèle résolu `claude-opus-5-5`, réviseur neuf. Je n'ai écrit aucun des diffs. Horloge lue par `date -u` :
début à 16:10:00Z, fin à 16:33:43Z, le 2026-10-09. Dossier : `<scratchpad>/s2bis/dettes2/g2/`, avec son NOTES.md et un
TMPDIR dédié (`g2/tmp`).

Objet de la revue : `diffs-tete/DT2-a.diff` à `DT2-d.diff`, dans leur état de la passe Q1 du rapport du générateur
(§9). Les sha256 sont 4a07b368…, 1cddb96c…, 1cc25657… et 9aef8d1b…, recalculés par `sha256sum`. Ils s'appliquent en série
sur la tête 0cfbe3e, base relevée par `git rev-parse HEAD` et égale à celle du brief. Contrat : `formes-api/DECISION.md`,
points 1 à 5 et ajout daté de 15:29:27 UTC.

## Verdict : ACCEPTE-AVEC-CORRECTIONS (liste fermée C-1 à C-6)

Les cinq points de la DECISION et son ajout daté sont réalisés. Le code est juste sous chaque lecture non écrite des
bornes :
- je l'ai vérifié par une propriété indépendante sur 10 638 cas, avec 0 erreur ;
- les tests le montrent sur le serveur local.

Les gates sont vertes, et 17 mutants sur 19 sont tués. Restent :
- un relâchement d'OKX qui va au-delà de la lettre du point 4 (C-1) ;
- un refus d'octobre peu lisible (C-2, réponse à Q-DT2-2) ;
- une garde de cohérence manquante (C-3) ;
- deux trous de test révélés par mes mutants N01 et N07 (C-4, C-5) ;
- un chiffre périmé dans le G1 (C-6).

Aucune de ces corrections ne demande de reprendre la conception.

### Corrections (liste fermée)

**C-1. OKX : relâchement limité aux mois acquis** (DT2-c, `bougies.charger` et `bougies.serie`).

Le constat :
- Avec `voisins` > 0, toute minute hors fenêtre d'un mensuel est écartée sans refus, quelle que soit sa date.
- Le point 4 lève le refus pour « les minutes des mois voisins » seulement.
- Démonstration (`travail/demo-okx.out`, contre `demo-okx-tete.out`) :
  - un mensuel d'OKX qui porte une ligne du 2025-01-01 passe sans refus ;
  - un mensuel dont tous les temps sont en microsecondes donne 0 minute gardée et aucun refus ;
  - la tête refusait ces deux cas par `CA/format : temps hors fenêtre ou hors minute`.
- Sur la fenêtre principale, l'oracle de SH §4 rattraperait probablement le cas. Sur septembre, rien ne le rattrape,
  sauf une ligne de complétude à 0.

Forme proposée :
- En mode `voisins`, une minute hors fenêtre n'est écartée que si elle tombe dans une **garde des mois acquis** :
  [début du premier mois de `mois(fen, voisins)` − 14 h ; début du mois qui suit le dernier + 14 h). Les 14 h couvrent
  tout décalage de UTC−12 à UTC+14.
- Hors de cette garde, la minute reste un refus `CA/format : temps hors fenêtre ou hors minute`.
- Mise en œuvre :
  - `serie` reçoit un paramètre `garde` (None pour les pages) ;
  - la borne des mois est calculée sans importer `acquerir` dans `bougies`, par exemple une fonction de `socle` que
    `acquerir.mois` réutilise.
- Test :
  - dans `test_formes_okx`, un mensuel avec une ligne de 2025-01-01, puis un mensuel en microsecondes : refus nommé
    attendu, valeur écrite à la main ;
  - les trois décalages déjà testés (0, +8 et −4) restent verts.
- Mutant : garde retirée. Il doit rougir le test.

**C-2. Q-DT2-2 : nommer le refus du mensuel absent** (DT2-c, `acquerir.mensuels`).

Le constat (`travail/q2.out`, serveur local qui n'a pas 2026-10) :
- `acquerir.main` sort en code 4 avec `REFUS CA/acquisition : téléchargement impossible (HTTPError)`.
- La ligne ne nomme ni la place, ni l'actif, ni le mois. Au lanceur, l'écran porte seulement « acquerir.py en code 4 ».
- On ne peut donc pas distinguer ce refus attendu (mensuel d'octobre non publié) d'une panne réseau.
- Le §5.7 de la PROPOSITION demande pourtant qu'un refus nomme l'actif.

Forme proposée :
- Dans `mensuels`, l'échec de `lire_url` sur un fichier mensuel devient
  `Refus("CA/acquisition", f"mensuel {m} non obtenu ({motif}) ; un mensuel n'est publié qu'après la fin de son mois", actif, place=place)`,
  toujours en code 4. Le motif est celui de `lire_url`, nommé par le type ; le mois n'est pas l'URL, la règle « jamais
  par l'URL » est donc tenue.
- Test : le cas de `q2.py` (fenêtre descriptive, 2026-10 absent) donne le code 4 et la ligne exacte, écrite à la main.
- Mutant : message non nommé.
- Le README cite la ligne attendue jusqu'à la publication du mensuel.

**C-3. Cohérence : `voisins` = 0 hors des mensuels** (DT2-c, `socle.coherent`).

- Avec `voisins` > 0, Kraken (accès `archive`) deviendrait non strict sans refus de cohérence. Pour les pages, la clé
  serait ignorée en silence.
- Forme : `voisins` ≥ 0, et `voisins` = 0 sauf pour l'accès `mensuel` ou `mensuel_checksum`. C'est le pendant du
  « chevauchement 0 hors pages » déjà écrit.
- Test : un cas `kraken voisins=1` ajouté à `test_parametres_coherence`, qui doit donner `CA/parametres`.
- Mutant : contrôle retiré.

**C-4. Test du chevauchement négatif** (mutant N01 VIVANT).

- Le mutant qui retire `0 <=` du contrôle `0 ≤ 2c < pas` survit à toute la suite : aucun cas ne pose un chevauchement
  négatif.
- Un chevauchement négatif ferait demander des pages trouées (départ après le début).
- Forme : ajouter `lambda p: p["series"]["coinbase"].update(chevauchement=-1)` aux cas de `test_parametres_coherence`.
  Le décompte `Ran` ne change pas, puisque ce n'est qu'un cas de la liste.

**C-5. Test de la minute non ronde hors de la fenêtre d'une page** (mutant N07 VIVANT).

- Le mutant `if (t % 60 and not dehors) or (dehors and not fenetres)` survit : aucune page ne porte de temps non rond
  hors de sa fenêtre.
- La garde de forme n'est donc pas testée dans le mode filtré, ni pour les pages ni pour OKX.
- Forme : un cas de `test_doublons_et_decoupage` où la page 0 porte un temps non rond hors de [-1 ; 5), par exemple
  W0 + 390 s, écrit sans passer par `m[t]`. Refus attendu : `REFUS CA/format : temps hors fenêtre ou hors minute ;
  actif ETH ; place coinbase`.
- Le mutant N07 doit rougir.

**C-6. G1 : répétition à l'échelle refaite après Q1** (RAPPORT-GENERATEUR §5 et §9).

- Le §5 donne 90,2 s, 875 492 Kio et 439 pages de Coinbase d'ETH. Ces chiffres sont d'avant Q1 (299 minutes utiles
  par page), et le §9 ne les reprend pas.
- Je l'ai refaite sur l'état final (`travail/repetition.out`, même outil, même sha256 afee769a…) :
  - code 0, en 98,0 s, avec 875 324 Kio de mémoire maximale ;
  - **440** pages, ce qui concorde avec 131 040 / 298 = 439,7 ;
  - 29 lignes de complétude, Bitstamp à 131040/131040.
- Forme : une ligne datée au §9, avec ces chiffres ou ceux d'une nouvelle mesure du générateur.

Placement (R-25) :
- DT2-a a déjà 199 lignes ajoutées. Les cas de C-4 et C-5 vont donc dans DT2-b (107) ou dans un diff DT2-e.
- C-1 à C-3 vont dans DT2-c (108).
- Chaque diff doit rester à 200 lignes ou moins. Le plancher suit le nouveau `Ran` exact, et le `SHA256SUMS` du lot est
  recalculé.

## Constats (O-n)

- **O-1. Point 1 et ajout daté : réalisés et justes.**
  - Je l'ai établi par une propriété indépendante (`outils/propriete.py`, `travail/propriete.out`), écrite sans le code
    du lot.
  - Domaine : pas de 1 à 12, c de 0 à ⌊(pas−1)/2⌋, fenêtres de 1 à 3·pas + 1 minutes.
  - Sémantiques : `start` inclus ou exclu, croisé avec `end` inclus ou exclu, pour trois modes (bornes, `limit` compté
    depuis `end`, `limit` compté depuis `start`).
  - Propriétés vérifiées :
    - l'union des minutes servies, filtrées à [départ ; borne + 60) puis à la fenêtre, égale exactement la fenêtre ;
    - chaque requête tient en `pas` bougies inclusives ;
    - les pages sont contiguës et disjointes.
  - Résultat : 10 638 cas, 0 erreur.
  - Valeurs du lot recalculées : Coinbase u = 298, Bitstamp 998, Bitfinex 10 000 sans chevauchement (`[lu]` bornes
    incluses).
  - Les URL recalées de `test_pages` sont justes : 23:59-04:58, 04:57-09:56, 09:55-11:40 ; n = 702 de 1775001540 à
    1775043600 ; septembre n = 32 de 1790810940 à 1790812800.
- **O-2. Point 2 : réalisé.**
  - Le filtre [départ ; borne + 60) ∩ fenêtre garde les minutes de chevauchement, que le point 3 compare entre pages.
  - Il écarte les bougies qui précèdent `start` : sous la variante « avant », elles sont altérées et le test reste
    égal à la vérité.
  - Il écarte aussi la minute qui suit la fenêtre.
  - L'écart sans limite de distance est la lettre du point 2 (« écartées »). Deux filets restent : l'oracle de SH §4,
    où Coinbase, Bitstamp et Bitfinex figurent dans les concurrences de la fenêtre principale, et la complétude du
    point 5. Aucune correction.
- **O-3. Point 3 : réalisé.**
  - Un doublon identique entre deux fichiers est gardé une fois.
  - Un doublon contradictoire, en clôture ou en volume, donne le refus nommé « minute en double aux valeurs
    différentes » ; les mutants M12 et M15 sont tués.
  - Une minute en double dans un même fichier reste un refus (M14 de la campagne du générateur).
  - La comparaison porte sur les deux valeurs que lit la série (clôture, volume). Les ouvertures, hauts et bas ne sont
    pas lus par le lot.
  - En mode `voisins`, un doublon identique entre deux mensuels d'OKX est aussi admis, sans effet sur les valeurs.
- **O-4. Point 4 : réalisé**, sous réserve de C-1.
  - Mois 03 à 07 pour la fenêtre principale, 08 à 10 pour septembre, et 2026-11 à 2027-02 au passage d'année ;
    `date -u -d @1798758000` donne 2026-12-31 23:00 UTC.
  - Les décalages UTC, UTC+8 et UTC−4 sont testés aux deux bords de juin.
  - Binance et Kraken restent stricts (M10 tué ; cas Binance de `test_formes_okx`).
- **O-5. Point 5 : réalisé.**
  - Les comptes sont justes : reçues sur l'intervalle propre de la page, attendues = (fin − début)/60. Les mutants
    M25, N02 et N05 sont tués.
  - Ils sont imprimés dans `calib_actifs.txt`, après septembre, pour les deux fenêtres.
  - Lisibilité : une ligne par (actif, place, fenêtre), avec le détail par page. Pour Coinbase d'ETH, cela fait 440
    pages sur une seule ligne d'environ 9 Ko, lisible par un outil.
  - Les comptes ne sont imprimés que si le calcul aboutit. Un refus, qui est un échec fermé, ne les porte pas : c'est
    suffisant pour le point 5, qui vise la perte silencieuse.
  - E-CA-20 est tenu : le fragment n'en dépend pas (sha256 du fragment de la répétition égal à celui du générateur,
    ba896088…).
- **O-6. Échec fermé : préservé ailleurs qu'en C-1.**
  - Les refus restent : page absente ou hors découpage (M16 tué ; M17 du générateur), découpage exact, minute non
    ronde dans la fenêtre, nombre non fini, Binance et Kraken stricts.
  - Aucun test existant n'est affaibli. J'ai relu les recalages E-2 et E-3 :
    - `test_pages` : URL exactes neuves ;
    - `test_main` : URL exacte ;
    - `test_okx_reprise` : cinq mois, et la reprise est toujours vérifiée ;
    - `test_charger` : le `.partiel` est toujours exclu, et sa lecture rougirait par refus de découpage ;
    - `test_socle` : trois cas ajoutés, aucun retiré.
  - E-2, l'inversion de « aucune bougie demandée hors fenêtre », est voulue par le point 1. Sa trace est dans le README.
- **O-7. Limite (règle PAROXYSME)** : un cas de Coinbase n'est pas couvert par le code.
  - Le cas : une réponse de Coinbase plafonnée à 300 bougies et ancrée **avant** `start`, ce qui tronquerait la fin de
    la page.
  - Pourquoi il reste ouvert :
    - la documentation dit seulement que des bougies « may precede » `start`, et rien sur l'extrémité gardée en cas
      de plafond [abs] ;
    - le simulateur du lot prend la lecture « les plus récentes jusqu'à `end` ».
  - Ce qui le rendrait visible : seulement la complétude par page (reçues < attendues sur une paire liquide).
  - Item à former par l'orchestrateur : un essai réel autorisé, ou un contrôle « une page dont des bougies précèdent
    `start` et qui rend exactement `pas` bougies est suspecte ».
- **O-8. Q-DT2-2 : réponse.** Le code 4 est net. Le message ne l'est pas, d'où C-2. Le fait de calendrier (aucun
  lancement avant la publication du mensuel d'octobre d'OKX) est écrit au README.

## Rouge (tests d'abord)

- Les tests de l'état final ont été joués sur le code de la tête 0cfbe3e, modules `test_formes`, `test_formes_pages`,
  `test_formes_okx` et `test_comptes` (`travail/rouge-neufs.out`).
- Résultat : **36 FAIL, 0 ERROR**, uniquement des `AssertionError` ; les refus et les exceptions sont convertis en valeurs
  comparées.
- On y voit les pertes silencieuses de la tête sous « fin exclue » : `([1775001840, 1775002380], [], [])` et
  `([1775019540, 1775037540, 1775055540], …)`. On y voit aussi la première minute de chaque page sous « début exclu ».

## Mutants (`outils/mutants_g2.py`, écrit par moi ; `travail/mutants-g2.tsv`, `travail/mut/`)

Méthode :
- copie jetable de la racine, avec des substitutions exactes d'une seule occurrence ;
- ligne du job lue dans `gates.yml` de la copie (plancher 69) ;
- exécution sous `g2/outils/run.sh` (`env -u` des huit variables, puis `isole.sh`), puis `env -i` ;
- `start_new_session`, borne de 300 s par `killpg`, PAR = 2 ;
- classement : sortie 1 = TUÉ, 0 = VIVANT, toute autre = FATAL.

Campagne de 16:17:51Z à 16:21:55Z : **17 TUÉS, 3 VIVANTS (T00 témoin, N01, N07), 0 FATAL, 0 INVALIDE.**

**Rejoués (12 sur 43, tous TUÉS)** :
- M02 : borne sans chevauchement ;
- M07 : fenêtre de page non bornée ;
- M10 : Binance et Kraken non stricts ;
- M12 : doublon contradictoire admis ;
- M15 : volume non comparé ;
- M16 : page absente admise ;
- M21 : filtre d'OKX retiré ;
- M25 : reçues avec la minute de fin ;
- M32 : 2c = pas admis ;
- Q02 : départ = début ;
- Q07 : filtre depuis le début de page ;
- Q09 : cohérence en c < pas.

**Neufs** :

| id | mutation | résultat |
|---|---|---|
| N01 | cohérence sans `0 <=` (chevauchement négatif admis) | **VIVANT** → C-4 |
| N02 | fin de la dernière page non bornée à la fenêtre (comptes) | TUÉ |
| N03 | filtre depuis départ − 60 | TUÉ (la variante « avant » de Coinbase donne une contradiction) |
| N04 | `mois` : année figée à celle du début (passage d'année) | TUÉ (`test_mois`, `test_okx_mois_voisins`) |
| N05 | comptes : première minute de page non comptée | TUÉ |
| N06 | fenêtre de page bornée à début − 60 | TUÉ |
| N07 | minute non ronde tolérée hors de la fenêtre de page | **VIVANT** → C-5 |

## Gates

**Sur la copie d'archive** : tête 0cfbe3e avec sept exclusions, plus DT2-a à d ; le lot est identique à
`dettes2/travail/w` par `diff -r`.
- Job calib : Ran 69, conforme ; plancher 69 exact. La tête seule donne Ran 65, conforme.
- Matrice python 3.10, 3.11, 3.12 et 3.13, en `-X dev -W error` avec `PYTHONDEVMODE=1` et `PYTHONWARNINGS=error` :
  4 exécutions sur 4 en code 0, aucun « Exception ignored », aucun « Warning ».
- Runner : 136 ok. s2bis : Ran 341. S2 `--egal` : Ran 415.
- sim-bis : code 1 sur cette copie, avec 3 ERROR `git archive … sortie 128`, parce que la copie n'a pas de `.git`
  (E-G2-2). Refaite ci-dessous.

**Sur un clone local privé** (`git clone --no-checkout` du dépôt, puis tête 0cfbe3e et DT2-a à d dans le clone ; le
dépôt réel n'est pas touché) :
- calib 69, runner 136 ok, s2bis 341, **sim-bis Ran 268, conforme**, S2 415 : tous en code 0.
- xtask (`cargo --locked --offline xtask verify`, lignes VERDICT seules) : la tête du clone et l'état final donnent les
  mêmes 10 lignes, toutes VERT, VERDICT GLOBAL VERT.

**Répétition à l'échelle** (E-CA-26, synthétique) : voir C-6.

## Forme

- R-25, lignes ajoutées par diff : DT2-a 199, DT2-b 107, DT2-c 108, DT2-d 94 (lignes retirées : 60, 6, 35, 13). Les
  quatre sont sous 200.
- Aucun octet 92 ajouté. Aucun `TODO` ni `FIXME`.
- Aucune ligne de plus de 120 caractères dans les fichiers du lot. Certaines dépassent 120 octets, à cause des accents
  seulement.
- `SHA256SUMS` du lot : `sha256sum -c` passe, la couverture est exacte (liste égale aux fichiers), sha256
  e47a3c77…98fe, égal au §9 du générateur.
- Chemins touchés : `gates.yml` (ligne du plancher calib) et `scripts/calib-actifs/` seulement (E-CA-01).
- `SHA256SUMS` du dossier du générateur : `sha256sum -c` passe.

## Écarts (E-G2-n)

- **E-G2-1. Premier lancement de la campagne de mutants, sans résultat et non compté.**
  - J'ai sondé le PID de `setsid` (9827) au lieu de celui du processus Python (9828), et j'ai cru la campagne finie.
  - J'ai alors déplacé ses sorties et vidé `tmp` pendant qu'elle tournait.
  - Je l'ai tuée (`killpg` des sessions filles, puis kill 9828) et j'ai vérifié que `t2` était intact (`diff -r` égal à
    `w`).
  - Je l'ai relancée en tâche de fond de l'outil. Les restes sont sous `travail/essai1-interrompu/`.
- **E-G2-2. sim-bis rouge sur la copie d'archive**, par la seule absence de `.git`. Refait sur le clone : conforme.
- **E-G2-3. Le clone privé a écrit sur disque les chemins interdits de lecture.** Aucun n'a été ouvert. Le clone est
  supprimé à la fin.
- **E-G2-4. La gate sim-bis a extrait f35a70c et f45898040e10 dans le clone, par ses propres tests.**
  - Les tests en cause sont `test_croise_window_f35a70c`, `test_oracle_r1` et `test_oracle_recalc`. Ils ont fait un
    `git archive` vers le TMPDIR `g2/tmp`, vidé à la fin.
  - Je n'ai ouvert aucun octet extrait. Je n'ai lu que les lignes de verdict et de résumé de la suite.
  - Le brief de cette G2 demande la gate sim-bis. Mais `calib3/BRIEF-CA.md` range « aucune extraction de `f35a70c` »
    parmi les interdits durs du lot calib (E-CA-02 vise le code du lot), et le générateur n'a pas joué sim-bis.
  - Je le signale à l'orchestrateur, qui juge si la gate sim-bis doit se jouer ailleurs que dans un rôle de ce lot.
- **E-G2-5. Énumérations par nom sur mes copies complètes.**
  - Commandes : `find` de `__pycache__`, de `*.orig` et de `*.rej`, sur `t2`, `t2g` et le clone (qui contiennent
    `docs/`), et `ps aux | grep` large pour retrouver ma campagne.
  - Je n'ai ouvert aucun contenu. Je n'ai tué que mon arbre de processus, par le PPID 9828.
- Réseau :
  - sondes à 16:10:21Z et 16:33:14Z : 1.1.1.1 et 8.8.8.8 en errno 101, `urlopen` refusé, mandataire 127.0.0.1:44643 en
    errno 111 sous isolement ;
  - la sonde discrimine : le même mandataire est joint hors isolement ;
  - aucune requête vers une place réelle ;
  - `ps` de fin vide.
- Dépôt réel : status vide et HEAD 0cfbe3e à la fin. Aucune écriture git.
- `SHOGEN_S2_CAMPAGNE_CONTROL` n'a jamais été posée ; `run.sh` la retire.

## Journal de provenance (G1)

**Lu, niveau [lu]** :
- `formes-api/DECISION.md` (ajout daté compris) et `formes-api/RAPPORT.md` ;
- `dettes2/RAPPORT-GENERATEUR.md` et `NOTES.md` ;
- les quatre diffs en entier ;
- `bougies.py`, `acquerir.py`, et `tau.main` et `septembre` de l'état final ;
- `lancer.sh` (en-tête et étape réseau) ;
- PROPOSITION §4.1, §4.2 et §5 ;
- les outils du générateur (`mutants.py`, `batterie.sh`, `matrice.sh`, `xtask.sh`, `repetition.py`, `rouge.sh`), en
  lecture seule.

**Lu aussi** : `calib3/BRIEF-CA.md`, en entier, en fin de revue (16:34Z). Sa lecture a ajouté les écarts E-G2-4 et
E-G2-5 et n'a rien changé d'autre. Aucune lecture interdite ouverte.

**Chiffres recalculés par moi** :
- les découpages et les URL : à la main et par `propriete.py` ;
- `date -u -d @1798758000` et `@1798765200` ;
- 131 040 / 298 ;
- les comptes de lignes et d'octets 92 des diffs, par un script sur les octets.

**Commandes et sorties** : `travail/` contient :
- `sonde-debut.out` et `sonde-fin.out` ;
- `job-t2.out` et `job-tete.out` ;
- `rouge-neufs.out` ;
- `q2.out`, `demo-okx.out` et `demo-okx-tete.out` ;
- `propriete.out` ;
- `mutants-g2.{tsv,log}` et `mut/` ;
- `matrice_t2_*.out` ;
- `batterie_t2_*` et `batterie_clone_*` ;
- `xtask-{tete,t2}-verdicts.txt` ;
- `repetition.out`.

**Outils** (`outils/`) : `run.sh`, les sondes, `job.sh`, `batterie.sh`, `xtask.sh`, `mutants_g2.py`, `propriete.py`,
`q2.py`, `demo_okx.py`, et `repetition.py` (copie de l'outil du générateur, même sha256).

Les copies `tete`, `t2`, `t2g`, `x`, `rouge` et `clone` ont été supprimées. Elles se reconstruisent par `git archive
0cfbe3e`, puis `patch` de DT2-a à d.
