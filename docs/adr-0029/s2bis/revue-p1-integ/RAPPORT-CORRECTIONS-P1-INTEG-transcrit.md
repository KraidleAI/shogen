# Rapport du worker — corrections C-1 à C-5 de la relecture G2 d'intégration de P1, diffs CB-19a à CB-19h (transcrit)

> Transcription par l'orchestrateur le 2026-10-05 18:59:02 UTC du rapport rendu par message par le worker (agent ac367cc9d0e73cfb6) ; contrôle FM-1.1 : fragments_l51_l14 = 0. Texte du worker ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`). Reçu pendant la pause demandée par l'investisseur : transcrit seulement, adjudication et contre-contrôle à la reprise.

Gate 0 : **claude-opus-5-5**. C'est l'identifiant exact du modèle sous lequel je tourne. L'effort « max » n'est pas observable de l'intérieur.

# Corrections C-1 à C-5 de la relecture G2 d'intégration de P1 : diffs CB-19a à CB-19h

**Les cinq corrections sont faites, en huit diffs.** Appliqués en série par `git apply` sur une extraction neuve de la base 47b2177, ils redonnent l'état final à l'octet. Les 96 mutants neufs sont tous tués ; les 30 du réviseur, rejoués sur l'état final, aussi.

- Heures (`date -u`) : de 17:20:51 à 18:57:13 UTC.
- Base : `47b217785ac7…`, égale au brief.
- Copie faite par `git --no-optional-locks archive`, avec les exclusions du brief : aucune entrée exclue, aucun `*.jsonl`.
- Je n'ai fait aucune écriture git. À la fin, la tête est inchangée et le statut est vide.

## Résumé, point par point

**C-1 (a), diff CB-19a.** Une réponse appariée de plus de 512 octets devient `forme`.
- Le contrôle est dans `interroger`, après l'appariement : un datagramme non apparié reste ignoré, quelle que soit sa taille. `analyser` ne porte pas la borne (pour un futur repli TCP).
- FORMAT §12 : la règle, avec deux citations de la RFC 1035 mot pour mot (§2.3.4 l.529, §4.2.1 l.1756-1758). Je les ai contrôlées contre le fichier du registre (`d14ae809…`) avec la normalisation de S-G5 réécrite en Python : TROUVÉ, et un témoin altéré est bien ABSENT.
- Tests : 512 octets retenue, 513 en `forme`, datagramme non apparié de 600 octets ignoré, réponse hostile du réviseur (65 502 octets) en `forme`.

**C-1 (b), diff CB-19b.** Sept témoins et sept noms au plus.
- Le schéma admet désormais `[s, n]` ; au-delà, refus `CONFIG/borne`.
- Calcul, écrit au FORMAT §13.6 et dans METRIQUES :
  - `reponses` fait au plus 1 + 495 × (18 × 1 024 + 85) / 36 = 254 609,75 octets ;
  - cela repose sur un lemme : un nom décodé a au plus 2 × 512 caractères. Je l'ai vérifié par tirage sur 600 000 messages. Le plus long trouvé fait 526 caractères pour 362 octets, donc une borne à 1 × L serait fausse.
- Témoin de la plus grande `sante` : sa ligne canonique fait **3 823 224 octets**. Le test la recompte, et un calcul indépendant du code donne le même chiffre. Marge sous LIMITE : 371 080 octets.
- Bornes voisines : huit témoins et huit noms donnent 4 343 471 octets, au-delà de LIMITE.

**C-2 (a), diff CB-19c.** `fsync` du dossier après chaque création : fichier du journal, première ligne écrite, et fichier de sommes. Les tests passent par l'espion de fsync. Le FORMAT §6.4 est réécrit.

**C-2 (b), diff CB-19d.** Avant une `reprise` en segment neuf, `fsync` du fichier qu'elle chaîne et de ceux dont elle déclare la queue, même déjà sommés. Avant toute somme, `fsync` du fichier sommé. Le FORMAT §4 est réécrit.
- **Preuve exigée**, banc du réviseur rejoué sans modification sur les graines 0 à 299 :
  - **0 rupture et 0 somme fausse**, contre 128 et 131 sur la base ;
  - mon agrégateur redonne exactement les chiffres du réviseur sur la base, ce qui valide le compte ;
  - sans coupure, sur 1 000 graines : 0 rupture, et 27 journaux illisibles avec les trois mêmes refus finals (graines 39, 97, 297) que la mesure du réviseur.
- Ce que le modèle ne prouve pas est écrit au §4 :
  - les entrées de dossier ;
  - un `fsync` qui rend sans avoir écrit ;
  - une perte sous la taille synchronisée d'un fichier.

**C-3 (b) et (a), diff CB-19e.**
- (b) Le client pose l'adresse au suivi avant `phases["dns"]` ; test par suivi espion.
- (a) Test du client réel dans la boucle : lecture pendante à E, `delai`, phases `dns` et `connexion`, adresse posée. Il tue MI-09 et MI-10.

**C-3 (c) et (d), diff CB-19f, tests seuls.**
- (c) Point d'entrée à w = 60 avec une horloge hors de la grille. Il tue MI-12.
- (d) Délai et places lus de `formes.json` jusqu'à la boucle. Il tue MI-13 et MI-14.

**C-4.**
- (a), (b) et (d) sont écrites au FORMAT dans le diff CB-19g, sans code de production.
- (c) est portée par CB-19d, qui réécrivait déjà le §4 pour C-2.

**C-5, diff CB-19h.**
- (a) `oracle_record.py` exige `--plancher [1-9][0-9]*`. Testé avec un commit à `--plancher 0` et un autre à `--plancher 07`.
- (b) Le runner sort en 3 sur toute exception au chargement du vérificateur, `SystemExit` compris. Deux cas neufs, R-01 (`sys.exit(0)` au chargement) et R-02 (exception au chargement), font passer le runner de 85 à 87 cas.
- Aucun cas existant n'est retiré ni affaibli. Les leurres du réviseur de CB-18 donnent les mêmes verdicts sur la base et sur CB-19h, une fois normalisés le chemin de l'arbre et le plancher affiché.

**De bout en bout,** avec les outils du réviseur sur le code final, en réseau isolé :
- la réponse DNS hostile donne une `sante` de 242 octets, contre 6 209 510 ;
- le point d'entrée avec un témoin hostile sort deux fois en 0, contre deux sorties 1 `JOURNAL/taille`, et sa sonde ne trouve ni rupture ni écart ;
- la reproduction de C-2 ne laisse ni rupture ni écart après la coupure.

**Matrice** (`-X dev -W error`, réseau isolé, état final) :
- 3.11, 3.12 et 3.13 : runner 87, s2bis Ran = 203, S2 Ran = 406, tout conforme ;
- 3.10 : runner et s2bis conformes ; S2 rouge, 77 FAIL et 3 ERROR, l'item connu PY310-1, aux mêmes chiffres que la relecture.

**xtask** (`cargo --locked xtask verify`) : verdicts identiques sur la base et sur l'état final.
- S-G1 à S-G8 VERT ; S-G9 ROUGE par la seule violation connue `docs/17:70` ; fmt, no_std et clippy VERT.
- S-G5 contrôle 320 fragments, contre 319 sur la base.

## Tableau final

| correction | diff | tests neufs | mutants |
|---|---|---|---|
| C-1 (a) | CB-19a | `test_dns` ×2 (512/513 et non apparié ; hostile du réviseur) ; `test_format` §12 | 13/13 (deux réécrits sur une ancre unique) |
| C-1 (b) | CB-19b | `test_entree` (sept admis, huit refusés) ; `test_sante.Taille` (3 823 224 octets) ; `test_format` §13.6 | 15/15 |
| C-2 (a) | CB-19c | `test_fichiers` (fsync du dossier après chaque création) ; `test_format` §6.4 | 12/12 |
| C-2 (b), C-4 (c) | CB-19d | `test_reprise` ×2 (deux reprises après coupure ; somme rattrapée) ; `test_format` §4 ; banc 0/0 | 13/13 |
| C-3 (a), (b) | CB-19e | suivi espion ; client réel dans la boucle ; `test_format` §11.4 | 13/13, dont MI-09 et MI-10r |
| C-3 (c), (d) | CB-19f | w = 60 ; délai et places | 13/13, dont MI-12, MI-13, MI-14 |
| C-4 (a), (b), (d) | CB-19g | `test_format` C-4 ; résolution tardive ; `run_params` après la bascule | 11/11 |
| C-5 (a), (b) | CB-19h | runner R-01, R-02 ; deux sous-tests de l'enregistreur | 11/11 |
| 30 du réviseur | état final | — | 30/30 (MI-10 rejoué réécrit, même mutation) |

- Classement des mutants : runner, puis ligne de `gates.yml` (job s2bis ; job S2 pour l'enregistreur), borne de 300 s, témoins vivants, 0 FATAL.
- Planchers relevés à chaque diff (`--egal`) : 187, 190, 192, 195, 198, 200, 203, 203. Celui de S2 reste à 406.
- Lignes ajoutées par diff : au plus 152 (CB-19b), dont au plus 67 de code et de tests.

## Points qui demandent ta décision

- **Homonymie.** La PROPOSITION (l.227) réserve déjà « CB-19 » à l'outil de lecture du rodage, que l'AVIS (Q-G-04, Q-C-13) verse au lot RODAGE. J'ai gardé les noms du brief ; un renommage de la série serait à décider.
- **Conflits de fusion probables** avec les workers du recalcul : la ligne du plancher s2bis de `gates.yml`, la puce « Corrections » du FORMAT et la fin de METRIQUES. Mes planchers sont comptés sur ma seule série.
- **C-4 « FORMAT seul ».** Aucun code de production n'est touché. J'ai toutefois ajouté deux tests de comportement qui lient le texte au code existant ; c'est à adjuger.
- **Mes copies ne lancent pas sim-bis.** Son adaptateur exige l'historique git (`ORACLE/extraction`). Mes diffs ne touchent pas `scripts/sim-bis`, mais le job est à lancer dans le dépôt.

## Items à former (règle PAROXYSME)

1. **Runner, cas non couverts.** C-5 (b) ne traite que le chargement. Un `os._exit(0)` au chargement, ou un `sys.exit(0)` levé par une fonction du vérificateur pendant un cas, fait encore sortir le runner en 0. Remède possible : exiger le résumé final du runner, ou lancer le vérificateur en sous-processus.
2. **Borne de `tardives`.** Elle n'est bornée (2 × `places`) qu'en supposant qu'aucun fil ne reste entre `places.release()` et `futur.set_result()`. La marge en couvre encore 19 530. Remède possible : rendre le résultat avant la place.
3. **Item 1 du réviseur, inchangé.** Un journal neuf coupé avant son premier marqueur reste illisible. Sous coupures, 19 graines sur 300 sont illisibles, contre 14 sur la base, mais les trajectoires diffèrent ; sans coupure, le compte est identique à celui du réviseur.
4. **Limites de C-2.**
   - Le banc ne prouve pas la durabilité des entrées de dossier.
   - Le `fsync` passe par un descripteur en lecture seule, ce qui suppose la sémantique de Linux.
5. **Observation.** `oracle_record.ligne_du_job` ne rattrape que `OSError` et `SyntaxError` au chargement du vérificateur de l'outil.

## Écarts

- **E-1.** J'ai écrit deux heures au `NOTES.md` sans lire `date -u` ; elles sont corrigées.
- **E-2.** Le PID réel du banc sur la base n'est pas relevé, seulement celui de son parent `setsid`, 21709.
- **E-3.** Pour CB-19a, CB-19b et CB-19c, j'ai écrit le texte du FORMAT avant son test. Le rouge a été montré ensuite contre le FORMAT de l'état précédent. Le code, lui, a toujours suivi ses tests.
- **E-4.** J'ai reformaté sept lignes de plus de 120 caractères et deux littéraux d'octets à barre oblique inverse. C'était après les campagnes des états touchés, et le changement est sans effet sur le code exécuté. Aucun octet 92 n'est ajouté par la série.
- **E-5.** La matrice préliminaire a tourné pendant ce reformatage ; je l'ai refaite.
- **E-6.** J'ai affiché 20 lignes de la sortie de xtask, au lieu des seules lignes de verdict : des lignes de compilation et la violation connue, chemins seuls.

## Journal G1

**[lu], avec leur sha256 :**
- Brief (`970d91e2…`), lu en entier.
- Relecture transcrite (`fc7ac90f…`), `CLOTURE-P1.md` (`3928d1d6…`) et `NOTES.md` du réviseur (`53075051…`), en entier.
- G0 (`0e9001f3…`), AVIS (`a919b307…`) et FORMAT de la base (`4f0a509b…`), en entier.
- PROPOSITION (`0cdf84c2…`) : l.188-189, 227, 361, 788, 810, par recherche.
- ADR-0029 (`35563d8f…`) : les lignes D-4 et D-5, par recherche, dont l.109-110.
- METRIQUES : l.1-20, 229-338, 667-686, 785-803, 1034-1053, 1091-1171.
- Code et outillage : `collecte/*.py`, `verdict-suite-s2.py`, le runner et `oracle_record.py`, en entier.
- Tests : lus en entier ou par plages.
- xtask : `sg5.rs` et `documents.rs`, par plages.
- RFC 1035 : l.505-540 et 1740-1770.
- Outils et preuves du réviseur : empreintes contrôlées contre `SHA256SUMS-reviseur`.

**[abs] :** les pièces D.2, les dossiers exclus, tout `*.jsonl`, l'annexe B, le JOURNAL, la PASSATION et le reste de l'ADR et de la PROPOSITION.

**[2nd] :** les noms d'items repris de la relecture. Les chiffres de la relecture, eux, sont recomptés : banc, MI vivants, matrice 3.10.

**PID réels :**
- campagnes : 7499, 15524, 17615, 5108, 11258, 2974, 3125, 15670, 15947, 16800 ; les 30 du réviseur : 4615 ;
- banc avec coupures : 5112 ; banc sans coupure : 7214 ;
- matrice finale : 1403, puis un PID par job dans `jobs-3.x.txt` ;
- entrées hostiles : 16493 ; xtask préliminaire : 21490.

Les copies lourdes sont supprimées.

## Fichiers

Dossier : `<scratchpad>/s2bis/p1-integ/corr/`

- `diffs/CB-19a.diff` à `diffs/CB-19h.diff`, avec leur `diffs/SHA256SUMS`
- `SHA256SUMS` (`add12102…`, 104 entrées, toutes OK)
- `NOTES.md`
- `preuves/` : les rouges, les bancs, `mutants/resume-*.txt`, `matrice-finale/`, `leurres-cb18/`, `e2e-hostiles-CB19h.json`, `xtask-verdicts-*.txt`
- `outils/`
