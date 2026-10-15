# Premier contre-contrôle de DETTES-T2 (cc1) (transcrit)

> Transcription par l'orchestrateur le 2026-10-15 13:51:21 UTC du fichier dettes2/g2/cc/RAPPORT-CC.md ; contrôle FM-1.1 des transcripts du générateur-correcteur, du réviseur G2 et des deux contre-contrôleurs, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# DETTES-T2 (SHOGEN-CALIB-FORMES-API-1) : contre-contrôle neuf

**Gate 0** : modèle résolu `claude-opus-5-5` (Opus 5.5), effort max. Rôle : contre-contrôleur neuf. Je n'ai écrit ni
les diffs ni la G2. Horloge lue par `date -u` : début à 18:11:02Z, fin à 18:35:24Z, le 2026-10-09. Dossier :
`<scratchpad>/s2bis/dettes2/g2/cc/`, avec NOTES.md et un TMPDIR dédié (`cc/tmp`, vide à la fin).

**Objet** : les six diffs `dettes2/diffs-tete/DT2-a.diff` à `DT2-f.diff`, appliqués en série sur 0cfbe3e. Sha256
recalculés, égaux au G1 (§10 pour a à e, §11 pour f) :
- a `4a07b368…`, b `1cddb96c…`, c `f3d6733e…`, d `ae440f30…`, e `92601231…`, f `6b25dccc…` ;
- concaténation a à f, dans cet ordre : `d3d35e3fc6b1809197734f35adeef7159e6fc6f79f2b46d29905c554d48ab165`.

**Contrat** : `formes-api/DECISION.md` (sha256 `e678428b…`) : points 1 à 5 et quatre ajouts datés (Q-DT2 ; C-1 à C-7 ;
Q-DT2-7 et C-8 ; limite de C-8 et base). Contexte : BRIEF-CA, G0-CALIB-ACTIFS, PROPOSITION §4.1, §4.2 et §5.

## Verdict : CONFORME-AVEC-RÉSERVES (liste fermée R-1 à R-3)

Les corrections C-1 à C-8 répondent à leurs constats et aux décisions. Les gates sont vertes ou identiques à la tête.

Propriété : je l'ai rejouée sous mon propre simulateur.
- Aucune perte silencieuse et aucune minute hors fenêtre gardée, sous toutes les lectures que les décisions modélisent.
- Une lecture que les décisions ne modélisent pas laisse des pertes : c'est la limite L-1, rendue plus bas.

Mutants : 33 tués sur 35, témoin vivant. Les deux vivants :
- X03 révèle un trou de test sur la reprise (R-2) ;
- X06 est équivalent (démonstration au §3).

Restent trois réserves :
- R-1 : la limite admise de C-8 n'est pas écrite comme telle au README ;
- R-2 : le repérage d'une page suspecte à la reprise n'est pas testé ;
- R-3 : la cohérence des paramètres ne garantit pas que les demi-requêtes restent sous `pas`.

### Réserves (liste fermée)

**R-1. README : écrire la limite admise de C-8.**
- Ce qu'exige la DECISION (ajout du 18:10:42 UTC) : la limite est écrite au README du lot, phrase à vérifier par le
  contre-contrôle.
- Ce que porte le README : la règle du refus seulement (l.23-24 : « refus CA/format si une demi-réponse est elle-même
  tronquée ou si la page suspecte n'a pas ses demi-pages »).
- Ce qui manque : rien ne dit que ce refus peut sortir sans faute de la place, sous une lecture non écrite de Coinbase,
  ni que la première acquisition réelle le montrera.
- Forme proposée, à placer après la l.24 :
  > Limite admise (DECISION de FORMES-API-1, ajout du 2026-10-09 18:10:42 UTC). Coinbase n'écrit pas sa lecture. Sous la
  > lecture « les `pas` bougies les plus récentes jusqu'à `end` », avec `end` exclu, deux cas suffisent pour que le
  > refus sorte sans faute de la place : la dernière minute propre d'une page et le milieu de cette page sont sans
  > échange, ou bien cette dernière minute et la minute qui suit la page. C'est un échec fermé, jamais une perte. La
  > première acquisition réelle montrera si ce cas se produit.
- Chiffres à l'appui : `travail/recentes-lot.out` et la limite L-2.

**R-2. Test de la reprise d'une page suspecte (mutant X03 VIVANT).**
- La DECISION (C-8) et le brief demandent que la page suspecte soit repérée à l'acquisition et à la reprise.
- Le code le fait. Je l'ai vérifié par `outils/reprise_cc.py` (`travail/reprise-cc.out`) :
  - premier passage : les demi-requêtes sont refusées, et l'acquisition s'arrête en CA/acquisition ;
  - second passage : la page n'est pas redemandée, les quatre demi-pages le sont, et la série est égale à la vérité.
- Aucun test ne le montre. Le mutant X03 survit à toute la suite. Il s'écrit `if man.present(rel): continue` avant
  `requete` : une page déjà acquise n'est jamais examinée, et ses demi-pages ne sont pas redemandées.
  - `test_demi_pages` fait bien deux passages, mais le premier acquiert déjà les demi-pages.
- Forme proposée : un cas de `test_demi_pages`.
  - Au premier passage, le serveur rend 404 aux demi-requêtes, d'où le refus `CA/acquisition`.
  - Au second passage, il les sert.
  - Attendus, écrits à la main : les quatre URL de demi-pages et aucune page au second passage ; six fichiers ; série
    égale à la vérité.
  - Le mutant X03 doit rougir.
- Placement : dans DT2-f, s'il reste à 200 lignes ajoutées au plus (il en a 183 aujourd'hui), sinon dans un DT2-g. Le
  plancher suit le `Ran` exact, et `SHA256SUMS` est recalculé.

**R-3. Cohérence : demi-requêtes sous `pas`.**
- La DECISION (C-8) dit : « chacune sous `pas` bougies, donc jamais plafonnée ».
- `socle.coherent` n'exige que 0 ≤ 2c < `pas`. Or la plus grande demi-requête compte (`pas` + 1) // 2 + 2c créneaux.
  Une demi-requête dépasse donc `pas` dès que 2c dépasse environ `pas`/2. Exemple : `pas` 300 et c = 75 sont admis
  aujourd'hui.
- Mesure (`travail/demis-cc.out`) : sur pas 3 à 40, 327 415 demi-requêtes dépassent `pas` pour des couples cohérents
  (3, 1), (5, 2), (6, 2), etc.
- Le simulateur en tire un refus `CA/acquisition` nommé (Coinbase rejette au-delà de 300 points, [lu]). C'est un échec
  fermé, mais hors de la garantie écrite.
- Les valeurs du lot sont sûres : 152 pour 300, 502 pour 1 000, 5 000 pour 10 000.
- Forme proposée :
  - pour l'accès `pages`, ajouter (`pas` + 1) // 2 + 2c < `pas` à `coherent` ;
  - cas `coinbase chevauchement=75` dans `test_parametres_coherence`, attendu `CA/parametres` (le `Ran` ne change pas) ;
  - mutant : garde retirée.

## 1. C-1 à C-8 contre leurs constats et les décisions

| point | décision | constat (état final) | tenue |
|---|---|---|---|
| C-1 | garde des mois acquis ± 14 h | `bougies.charger` l.183-185 : garde = [début du premier mois − 50 400 s ; début du mois qui suit le dernier + 50 400 s). 50 400 s = 14 h. Bornes recalculées par `date -u -d` : 1777543200 = 2026-04-30 10:00Z = 2026-05-01 − 14 h ; 1785592800 = 2026-08-01 14:00Z. Cas de `test_okx_garde_et_mois_absent` : bornes admises, minute d'avant et borne haute refusées, 2025-01-01 et microsecondes refusés. Mutants G01 et M21 tués. | oui |
| C-2 | refus nommé du mensuel non publié, code 4, lisible | `acquerir.mensuels` l.95-100 : `REFUS CA/acquisition : mensuel 2026-10 non obtenu (téléchargement impossible (HTTPError)) ; un mensuel n'est publié qu'après la fin de son mois ; actif ETH ; place okx`. `main` sort en code 4 pour CA/acquisition (l.219). README l.27-29 : ligne citée mot pour mot. G07 tué. | oui |
| C-3 | `voisins` = 0 hors des mensuels | `socle.coherent` l.150 ; cas `kraken voisins=1` dans `test_socle`. | oui |
| C-4 | cas N01 | `coinbase chevauchement=-1` (`test_socle` l.83) ; N01 tué. | oui |
| C-5 | cas N07 | `test_formes`, cas 7 : W0 + 390 hors de la page 0, refus `temps hors fenêtre ou hors minute` ; N07 tué. | oui |
| C-6 | échelle refaite | G1 §10 et §11 datés. Refait ici (§4) : 83,1 s de `tau.py`, 874 672 Kio, 440 pages, fragment `ba896088…` inchangé. | oui |
| C-7 et Q-DT2-7 | refus `CA/format` de troncature, avec la condition adoptée | `bougies.tronquee` : au moins `pas` bougies, une avant le départ, aucune à la dernière minute propre ou après. Le seuil « au moins » est plus large que « exactement », sans effet (G15 tué). Bitstamp sous « fin exclue, depuis `end` » reste admis (G14 tué par ce cas). | oui |
| C-8 | demi-pages | Les sept éléments de la décision sont tous tenus (détail sous ce tableau). | oui, avec R-1 à R-3 |
| limite de C-8 | écrite au README | Seul le refus est écrit, pas la limite. | **R-1** |

Les sept éléments de C-8 :
- **Repérage à l'acquisition et à la reprise** : `acquerir.pages` l.188-192 lit le fichier de page après `requete`, même
  déjà présent. Vérifié par `reprise-cc.out` ; le test manque (R-2).
- **Même débit** : même objet `Debit`, même clé de place ; pauses de 0,34 s ; X04 et H07 tués.
- **Fichiers** : `.1.json` et `.2.json`.
- **Chargement** : l.176-179. La page n'est plus contrôlée et reste filtrée ; chaque demi-page est filtrée à
  [max(dk, dép) ; min(bk, borne) + 60).
- **Refus nommés** : demi-page tronquée, découpage (une seule demi-page présente : X05 tué), page sans ses demi-pages :
  refus C-7.
- **Complétude** : « pages redemandées k » (`tau.completude` l.233) ; H10 tué.
- **Couverture** : 0 erreur sur 842 754 cas (`demis-cc.out`).

## 2. Propriété (rejouée sur l'état final, étendue aux demi-pages)

- **Rejeu de `g2/outils/propriete.py`** (sha256 `7afe427d…`) : 10 638 cas, 0 erreur (`travail/propriete-g2-rejeu.out`).
- **Ma version, `outils/propriete_cc.py`.** Elle n'appelle que `acquerir.pages` puis `bougies.charger`, en boîtes
  noires. `acquerir.lire_url` y est remplacé par une fonction en mémoire : aucun réseau, même sous isolement.
  - Domaine :
    - `pas` de 3 à 16, c de 0 à (`pas` − 1)/2, fenêtres de 1 à 3·`pas` minutes ;
    - `start` et `end` inclus ou exclus ;
    - minutes sans échange tirées au hasard, avec une probabilité de 0, 0,1 ou 0,3 ;
    - minutes sans échange visées aux bornes : dernière minute propre, milieu m, première minute de la page suivante.
  - Modes du serveur :
    - `exact` ;
    - `recentes` : les `pas` plus récentes jusqu'à `end`, lecture de C-7 et de la limite de C-8 ;
    - `cpt-g` : plafond compté en bougies, ancré g minutes avant `start` (g = 1, 2, 4, 9, 30, ou variable par
      requête) : c'est la troncature de O-7, C-7 et C-8 ;
    - `cren-g` : plafond compté en créneaux, soit la fenêtre décalée de g minutes ; voir L-1.
  - Méthode : deux passages, dont le second ne doit rien redemander, puis le chargement.
  - Verdict par cas : JUSTE, REFUS nommé, PERTE (perte silencieuse) ou HORS-FENÊTRE (minute hors fenêtre gardée).
- **Résultats** (graines 7, 11 et 12, soit 13 000 cas ; plus 600 cas d'essai de la graine 1, non versés) :
  - `exact`, `recentes` et `cpt` : JUSTE ou REFUS nommé seulement ; **0 PERTE**.
  - **0 HORS-FENÊTRE** dans tous les modes.
  - **0 reprise fautive** : le second passage n'a jamais rien redemandé.
  - Pages redemandées puis justes, graines 11 et 12 : `cpt` 102 et 87, `recentes` 20 et 34.
  - Refus : `demi-page redemandée plafonnée et tronquée`, ou le rejet simulé au-delà du plafond (R-3, petits `pas`
    seulement).
  - PERTE seulement sous `cren` : graine 11, 480 cas sur 1 236 (c ≥ 1) ; graine 12, 494 sur 1 252 (sorties
    `propriete-cc-g{7,11,12}.out`).
- **Aux paramètres du lot**, Coinbase avec `pas` 300 et c 1 :
  - `recentes-lot.out` : le refus de C-8 sort si et seulement si `end` est exclu, la dernière minute propre (297) est sans
    échange, et le milieu (148) ou la minute qui suit (298) l'est aussi. Le cas « 297 seul » est juste après redemande.
    Cela confirme la limite décrite par le générateur au §11 (voir L-2).
  - `cren-lot.out` : perte sous `cren` dès g = 2, même sur un marché liquide (voir L-1).

## 3. Force des tests (mutants, `outils/mutants_cc.py`)

Méthode :
- copie jetable de la racine ;
- substitutions exactes d'une seule occurrence ;
- ligne du job lue dans `gates.yml` de la copie (plancher 72) ;
- `cc/outils/run.sh` (`env -u` des huit variables et de la variable de campagne, `isole.sh`), puis `env -i` ;
- `start_new_session`, borne de 300 s par `killpg`, PAR = 2 ;
- classement : 1 = TUÉ, 0 = VIVANT, toute autre sortie = FATAL.

Campagne de 18:18:58Z à 18:27:44Z (PID réel 11709) : **33 TUÉS, 3 VIVANTS (M00 témoin, X03, X06), 0 FATAL, 0 INVALIDE**
(`travail/mutants-cc.tsv`).

**Rejoués (29, tous tués)** :
- H01 à H13, tous ;
- M02, M07, M12, M16, M21, M25, M27 ;
- Q02, Q07 ;
- N01, N07 ;
- G01, G07, G11, G12, G14.

Les chaînes viennent de la table M de `dettes2/outils/mutants.py` (sha256 `5e6fc2bd…`). M07 et M27, INVALIDES au premier
essai du générateur, s'appliquent ici.

**Neufs** :

| id | point faible visé | mutation | résultat |
|---|---|---|---|
| X01 | découpage `socle.demis` | seconde demi-page non élargie au début (m + 60) | TUÉ |
| X02 | découpage `socle.demis` | première demi-page non élargie à la fin (m) | TUÉ |
| X03 | reprise sur fichiers existants | page déjà acquise jamais examinée | **VIVANT** (R-2) |
| X04 | débit | intervalle des demi-pages divisé par deux | TUÉ |
| X05 | refus d'une seule demi-page | plan limité aux demi-pages présentes | TUÉ |
| X06 | contrôle de la demi-page | contrôle depuis le départ de la page au lieu de celui de la demi | VIVANT, **équivalent** |

Pourquoi X06 est équivalent :
- Une réponse d'au moins `pas` bougies aux minutes distinctes couvre au moins `pas` créneaux.
- Seconde demi-page : si la première bougie tombe dans [dép ; dk₂), la dernière est au moins à dép + 60(`pas` − 1),
  donc au moins à la borne, donc au moins à fin − 60. Ni le code ni le mutant ne refusent.
- Première demi-page : si la première bougie tombe dans [dk₁ ; dép), la dernière dépasse m, puisque 2c < `pas`.
- Les deux critères ne diffèrent donc jamais.

## 4. Gates (0cfbe3e + DT2-a à f ; lot égal à `dettes2/travail/w` par `diff -r`)

| gate | copie | résultat |
|---|---|---|
| calib-actifs | archive (7 exclusions) | Ran 72, conforme, plancher 72 exact, code 0 |
| runner | archive | 136 ok, 0 échec, code 0 |
| s2bis | archive | Ran 341, conforme, code 0 |
| S2 `--egal` | archive | Ran 415, conforme, code 0 |
| sim-bis | clone git (sparse, 7 exclusions) + série | Ran 268, conforme, code 0 (et calib Ran 72) |
| matrice python 3.10 à 3.13 en `-X dev -W error` | archive | 4 sur 4 en code 0, Ran 72 ; 0 « Exception ignored », 0 « Warning » |
| xtask (lignes VERDICT seules) | archive, tête et état final | 10 lignes identiques ; la 9e est ROUGE sur les deux (déjà connue sur copie) |
| xtask | clone sparse, tête et état final | 10 lignes identiques ; même 9e ROUGE sur les deux |
| échelle (`repetition.py`, sha256 `afee769a…` égal à celui du générateur) | archive | code 0 ; bruts écrits en 14,0 s ; `tau.py` en 83,1 s, 874 672 Kio ; 440 pages de Coinbase d'ETH ; 29 lignes de complétude, Bitstamp 131040/131040, « pages redemandées 0 » ; fragment `ba896088…` égal à celui du générateur |

Jeu régénéré (`diffs-tete-6f8bfd8…/`) :
- il s'applique en série sur 6f8bfd8 et sur 766f0c2 ;
- le lot obtenu est égal à celui de 0cfbe3e plus la série, et le plancher de 72 est présent ;
- hors des lignes `index` et `@@`, seul le contexte de `gates.yml` diffère (DT2-e identique). Cela confirme l'ajout du
  18:10:42 UTC.

## 5. Forme

- **R-25**, lignes ajoutées par diff, comptées par `outils/forme.py` sur les octets : a 199, b 107, c 170, d 94, e 37,
  f 183 (retirées : 60, 6, 46, 13, 16, 36). Toutes sont à 200 ou moins.
- 0 octet 92 ajouté, 0 dans le lot. 0 `TODO` ni `FIXME`. 0 ligne ajoutée de plus de 120 caractères.
- `SHA256SUMS` du lot : `sha256sum -c` passe et la couverture est exacte (liste égale aux fichiers). Sha256
  `a37d6b844883de1a764461ce066939b9362d3fe92360a031506381cf29a00262`, égal au G1 §11.
- Chemins touchés : `gates.yml` (ligne du plancher) et `scripts/calib-actifs/` seulement (E-CA-01).
- **Recalages, aucun test affaibli.** J'ai relu toutes les lignes retirées sous `tests/` dans les six diffs :
  - DT2-e et DT2-f : « fin exclue, avant » passe de refus à page redemandée et admise, ce que veut C-8 ;
  - « tronquee » passe au refus de la demi-page ;
  - les comptes gagnent « pages redemandées 0 » ;
  - les recalages d'avant la G2 ont été relus par elle (O-6) ;
  - aucune assertion n'est retirée sans être remplacée, aucun cas sauté.

## 6. Règle « aucune dette » et limites rendues (règle PAROXYSME)

Les réserves R-1 à R-3 se corrigent dans le lot. Les deux points ci-dessous ne sont pas des réserves : chacun appelle une
décision, et non une correction dans le cadre adopté.

**L-1. Lecture « plafond compté en créneaux » (fenêtre décalée) : pertes non refusées.**
- Le cadre adopté : C-7 et C-8 modélisent la troncature comme un plafond compté en bougies (« exactement `pas`
  bougies »).
- L'autre lecture, tout aussi non écrite : la documentation de Coinbase compte des « data points » issus de start, end et
  granularité, et dit que des bougies « may precede » start. Elle admet donc aussi un serveur qui rend [s − g ; e − g].
- Sous cette lecture :
  - une page dont la réponse a moins de `pas` bougies n'est pas suspecte ;
  - les demi-pages ne le sont jamais, puisqu'elles ont moins de `pas` créneaux ;
  - les g dernières minutes sont donc perdues sans refus, même sur un marché liquide (`cren-lot.out`). Par exemple, avec
    `end` exclu et g = 1, la dernière minute de la fenêtre est perdue.
- Le filet : les lignes de complétude par page montrent un déficit systématique sur ETH-USD, mais elles ne sont jamais
  décisives.
- Essai du critère sans la condition de compte (`propriete-cc-g7-sans-compte.out`) :
  - les pertes passent de 288 à 11 cas `cren` sur 752 ;
  - les refus passent de 521 à 661 en `cpt`, sur des données complètes.
- Aucune correction ne couvre les deux lectures sans refus en trop. La levée passe par un acte extérieur : un essai réel,
  ou la lecture des lignes de complétude à la première acquisition.
- À adjuger par l'orchestrateur, au choix :
  - (a) admettre la limite et l'écrire au README avec la consigne de lire la complétude de Coinbase avant d'adopter les
    valeurs ;
  - (b) resserrer le critère ;
  - (c) former un item, par exemple SHOGEN-CALIB-FORMES-API-CRENEAUX-1.

**L-2. Fréquence du cas résiduel de C-8 (admis sans item le 18:10:42 UTC).**
- Le cas est un refus nommé, jamais une perte.
- Par page, sous `recentes` avec `end` exclu et une probabilité p de minute sans échange, sa probabilité vaut
  p(2p − p²). Je l'ai vérifiée cas par cas dans `recentes-lot.out`.
- Sur les 440 pages de la fenêtre principale de Coinbase pour USDT-USD, la probabilité d'au moins un refus vaut 8,4 %
  pour p = 1 %, 29 % pour p = 2 % et 88 % pour p = 5 %.
- Sur 585 pages, septembre compris, elle vaut 11 %, 37 % et 94 %.
- ETH-USD n'est pas concerné, puisque p y est quasi nul.
- C'est un fait neuf pour l'adjudication : « deux minutes précises » n'est pas rare sur une paire mince. Je ne le
  compte pas en réserve, puisque la décision est prise.

**Consigne DT3-C** (enregistrement `oracle_record.py`) : sans objet. Ce lot n'est pas sur le chemin S2 (cp-2), et ce
rôle n'est pas une G2.

## 7. Écarts

- **E-CC-1.** J'ai d'abord noté le PID du `setsid` (11707), qui sort aussitôt, au lieu de celui du processus Python. J'ai
  sondé le vrai PID (11709, `/proc/PID/cmdline` lu). Aucune action erronée : c'est le même piège que E-G2-1.
- **E-CC-2. Clone de sim-bis.**
  - Le clone est en `--no-checkout --no-hardlinks`, avec un sparse-checkout qui exclut les sept chemins interdits : ils
    n'ont jamais été écrits sur disque.
  - La gate sim-bis a fait elle-même ses extractions dans mon TMPDIR (cas E-G2-4, admis). Je n'ai rien ouvert. Les trois
    dossiers temporaires restants étaient vides à la fin et je les ai supprimés.
- **E-CC-3. xtask.** La 9e ligne est ROUGE sur l'archive et sur le clone sparse, identique entre la tête et l'état
  final. La G2 avait tout VERT sur un clone complet. Je ne l'ai pas refait, pour ne pas écrire les chemins interdits ; le
  lot est neutre pour xtask.
- **E-CC-4.** J'ai fait des listages non récursifs des noms de `docs/` de ma copie d'archive et du clone, pour contrôler
  les exclusions. Je n'ai ouvert aucun contenu.
- **E-CC-5.** `propriete_cc.py` a été complété entre deux campagnes : verdict HORS-FENÊTRE séparé et garde `__main__`.
  - Graine 7 : version d'avant, où toute perte ou minute en trop compte en PERTE ; tous ses exemples ont 0 minute en trop.
  - Graines 11 et 12 : version finale, versée.
- **Réseau.**
  - Sondes à 18:11:41Z et 18:32:41Z : 1.1.1.1 et 8.8.8.8 en errno 101, `urlopen` refusé, mandataire 127.0.0.1:44643 en
    errno 111 sous isolement.
  - La sonde discrimine : le même mandataire est joint hors isolement.
  - Aucune requête vers une place réelle. `ps` de fin, filtré sur `cc/`, vide.
- **Dépôt réel.** Lecture seule (`--no-optional-locks`, `git archive`, `git clone`, `git show`). Tête lue : 766f0c2 au
  début, 963eba9 à la fin, du fait de la chaîne de commits de l'orchestrateur. Status vide. Aucune écriture.
  `SHOGEN_S2_CAMPAGNE_CONTROL` n'a jamais été posée : `run.sh` la retire.
- **Copies.** `tete`, `t`, `clone`, `rb-*`, `var-demi`, `target` et `rep` sont supprimées. Elles se reconstruisent par
  `git archive 0cfbe3e` avec les sept exclusions, puis `patch` de DT2-a à f.

## 8. Journal de provenance (G1)

**Lu [lu]** :
- `formes-api/DECISION.md`, en entier (quatre ajouts) ;
- `formes-api/RAPPORT.md`, en entier ;
- `dettes2/RAPPORT-GENERATEUR.md` (§0 à §11), `g2/RAPPORT-G2.md` et `g2/outils/propriete.py`, en entier ;
- outils du générateur : `run.sh`, `sonde_*`, `batterie.sh`, `lourd-c8.sh`, `matrice.sh`, `xtask.sh`, `repetition.py`,
  `mutants.py` (table M) ;
- `calib3/BRIEF-CA.md`, en entier ;
- `G0-CALIB-ACTIFS.md` et PROPOSITION §4.1, §4.2 et §5 (§5.1 à §5.9), avec des lignes de tableau coupées à 400
  caractères : la fin des cellules E-CA-07, E-CA-13, E-CA-15 et E-CA-23 n'est pas lue ;
- code de l'état final : `socle.py`, `acquerir.py`, `bougies.py` et `README.md` en entier ; `tau.completude` ;
- tests : `serveur.py`, `test_demi_pages.py`, `test_formes.py`, `test_formes_pages.py` et `test_formes_okx.py` en
  entier ; extraits de `test_acquerir`, `test_pages`, `test_series` et `test_socle` ;
- diffs : DT2-f (toutes les lignes hors contexte) ; lignes retirées sous `tests/` de a à f ; forme de a à f par script.

**Non lu** : aucune pièce interdite, aucun `*.jsonl`, aucune pièce D.2, aucun octet extrait par sim-bis.

**Chiffres recalculés par moi** :
- sha256 des diffs, de leur concaténation et des pièces ;
- lignes ajoutées et retirées, octets 92 ;
- `date -u -d` de 1777543200, 1785592800, 1777593600, 1785542400, 1735689600, 1782842400 et 1782864000 ;
- 50 400 s = 14 h ;
- tailles des demi-requêtes 152, 502 et 5 000 ;
- p(2p − p²) et les probabilités sur 440 et 585 pages ;
- m = 148 de la page 0 du lot, à la main.

**Commandes et sorties** (`travail/`) :
- `sonde-debut.out` et `sonde-fin.out` ; `forme.out` ;
- `propriete-g2-rejeu.out` ; `propriete-cc-g{7,11,12}.out` ;
- `propriete-cc-g7-sans-compte.out` et `propriete-cc-g7-var-demi.out` : essais de critère, hors lot ;
- `cren-lot.out`, `cren-lot-var-demi.out`, `recentes-lot.out`, `reprise-cc.out` et `demis-cc.out` ;
- `mutants-cc.{tsv,log}` et `mut/` ;
- `batterie.log` et `batterie_*` ; `lourd.log` et `matrice_t_*` ;
- `xtask-{tete,t,clone-tete,clone-t}-verdicts.txt` ;
- `repetition.out`.

**Outils** (`outils/`) : `run.sh`, les sondes, `forme.py`, `propriete_cc.py`, `cren_lot.py`, `recentes_lot.py`,
`reprise_cc.py`, `demis_cc.py`, `mutants_cc.py`, `batterie.sh`, `matrice.sh`, `xtask.sh`, `lourd.sh` et
`repetition.py` (copie, même sha256). Ce sont tous des outils hors lot.
