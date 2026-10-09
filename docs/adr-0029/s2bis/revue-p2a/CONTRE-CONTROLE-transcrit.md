# Contre-contrôle de P2A (transcrit)

> Transcription par l'orchestrateur le 2026-10-09 06:28:34 UTC du fichier g2/cc/RAPPORT-CC.md ; contrôle FM-1.1 des quatorze transcripts d'agents qui ont touché `s2bis/p2a` ou `s2bis/p2b` : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Contre-contrôle des corrections de la G2 du collecteur P2 (tranche A, puis tranche B)

**Gate 0 : `claude-opus-5-5`** (identifiant exact du modèle qui tourne ; worker, effort max). Contre-contrôleur neuf :
je n'ai écrit ni les diffs, ni leurs corrections, ni les deux G2. Je vérifie, je ne corrige pas. Ouverture le
2026-10-09 à 03:38 UTC ; rapport écrit à partir de 05:05 UTC (heures lues par `date -u`).

Le même texte est versé à `p2a/g2/cc/RAPPORT-CC.md` et à `p2b/g2/cc/RAPPORT-CC.md`.

## 0. Méthode commune

- **Base** : extraction neuve de c58b997 (`git --no-optional-locks archive`, sept exclusions du brief vérifiées
  absentes) sous `p2a/g2/cc/base`. Le dépôt réel n'a été lu qu'en `--no-optional-locks`, tête b07147d ; aucune
  écriture git.
- **États construits par moi** (`patch -p1`, code 0 partout) :
  - P2A final : base + `p2a/diffs/` (8 diffs) ;
  - P2A d'avant la G2 : base + `p2a/diffs/envoi-1/` ;
  - P2B final : base + `p2b/diffs/` (10 diffs, `-F0`) ;
  - P2B d'avant la G2 : base + `p2b/diffs-v1-5cfe746/` ;
  - variante : P2A final + `p2b/diffs-apres-p2a/` (10 diffs, `-F0`).
- **Exécution** : réseau isolé (`unshare -n`, lo seule), `SHOGEN_S2_CAMPAGNE_CONTROL` retirée et jamais posée,
  `-X dev -W error` (`PYTHONDEVMODE=1`, `PYTHONWARNINGS=error` pour les enfants), TMPDIR dédié sous `cc/tmp`. Un seul
  processus lourd à la fois : campagnes, matrices et xtask en série.
- **Mutants** : classés par la commande exacte du job (runner, puis ligne s2bis lue au `gates.yml` de la copie mutée,
  python3.12, borne de 300 s ; sortie 1 = TUÉ, 0 = VIVANT, autre ou borne = FATAL). Copie neuve par mutant, ancre
  unique exigée. Pour chaque TUÉ, j'ai relevé les tests en échec.
- **Rouges** : la correction est retirée d'une copie de l'état final (texte d'avant remis), puis le test neuf est
  lancé seul. Attendu : FAIL d'assertion, aucun ERROR. Le témoin intact passe.

---

## Tranche A (P2A)

### Verdict : CONFORME

Les cinq corrections de la liste fermée (C-1 à C-5) sont faites, et rien d'autre n'a changé. J'ai rejoué :
- le rouge de chaque correction ;
- les sondes et les leurres du réviseur qui fondaient C-1 et Q-2 ;
- les six vivants de la G2 (tous tués) ;
- 13 mutants neufs, dont 12 tués.

Les planchers et les gates sont exacts. Deux constats neufs de gravité faible ou nulle (O-A1, O-A2) ne remettent en
cause aucune correction.

### A.1 Intégrité et périmètre

- `p2a/SHA256SUMS` : 289 OK, 0 échec (sha256 du fichier `26548156…17f4`) ; `p2a/g2/SHA256SUMS` : 72 OK.
- Série corrigée : les 8 diffs s'appliquent sur c58b997 (34 fichiers). Mesures par diff :
  - code ajouté (`.py` et `.yml`) : 200 / 116 / 147 / 124 / 61 / 198 / 133 / 200 ;
  - planchers posés : 263 / 270 / 276 / 281 / 284 / 289 / 293 / 297 ;
  - octets 92 ajoutés, marqueurs R-13 et lignes de code de plus de 120 colonnes : 0.
  Tout est égal au tableau du générateur.
- METRIQUES : les 19 fichiers cités ont, à l'état final, le nombre de lignes et de tests annoncé
  (`cc/outils/metriques.py`).
- **Rien hors liste** : le delta « avant la G2 → corrigé » (`cc/preuves/delta-envoi1-final.diff`) touche 9 fichiers :
  - `decodeurs.py` : C-1 ;
  - `secondaire.py` : C-4 ;
  - `test_decodeurs`, `test_asn`, `test_secondaire`, `test_format` : C-1, C-2, C-4, C-5 ;
  - FORMAT : §9.1 (C-5), §12 (Q-3), §15.2 (Q-1), §15.4 (C-4) ;
  - METRIQUES ;
  - plancher de `gates.yml` (291 → 297).

  Un test existant, `test_carte_part_a_ws_plus_5_secondes_sans_sondes`, est adapté : un relevé part désormais au
  démarrage, il reçoit donc un relevé factice et filtre par type. Son assertion est inchangée. C'est une conséquence
  directe de C-4.

### A.2 Corrections, une par une

| n° | fait | preuve rejouée par le CC | écart |
|---|---|---|---|
| C-1 | oui : aide unique `_entier` (`decodeurs.py:47-57`) aux cinq sites (`:65` OKX, `:84` DefiLlama, `:103` Bitstamp, `:104` Gemini, `:108` CoinGecko). Refus avant `int()` d'un Decimal fini d'exposant ajusté ≥ 16, et d'un texte de plus de 4 300 caractères. La borne est écrite et motivée (2^53 < 10^16) | **rouge** : borne retirée, `Bornes` donne 5 FAIL d'assertion (un par champ, `panne_decode` après plus de 0,1 s ; 66 s), puis 5 OK en 0,11 s. **Leurres du réviseur sur l'état final** : `leurre_echeance` (corps hostile, point d'entrée `pool`) met les marqueurs à E − 0,29 s, lectures `panne_decode` (avant : E + 10,5 s, `panne_transport:delai`) ; `leurres_decodeurs` : 0 ÉCART (avant : 6), L-D4 au plus 0,000 s ; `mesure_exposant` : 1E+1e6, 2e6 et 3e6 en 0,0 s (avant : 10,4 / 41,1 / 94,6 s). **Sonde du CC** (`s1_entier.py`) : 15 instants hostiles × 5 champs, au plus 8,5 ms ; aucun contournement par coefficient géant à exposant négatif, ni par texte blanc de 1 Mo, ni par négatif | O-A1, O-A2 |
| C-2 | oui : six cas écrits à la main, aux valeurs du tableau C-2 de la G2 (six mots, 2^255, « -05:00 », AS 0 au RIPEstat et au TXT, première chaîne du TXT, `periode` de 86 401 s) | chaque mutant vivant de la G2 appliqué à l'état final : FAIL d'assertion du test visé (G01 et G02 : `test_chainlink_…` ; G03 : `test_horodatage_iso_…` ; G14 : `test_ripestat_…` et `test_cymru_…` ; G17 : `test_cymru_…` ; G20 : `test_carte_budget_…`). Le même mutant sur l'état d'avant la G2 donne OK : c'est bien le cas neuf qui tue | aucun |
| C-3 | oui : écart déclaré au rapport (l.119 et l.150), au G1 (l.196-197) et dans la section METRIQUES de CB-6c ; ligne SHOGEN-S2BIS-FORMES-BTC-1, déclencheur CB-8 | ligne vérifiée sur le code : aucune donnée neuve sous `s2bis/config/` (seul `analyse.json` de la base), `SPECS` à `sources.py:239` | aucun |
| C-4 | oui, dans le lot : relevé dû à la première fenêtre de l'exécution, puis à la première fenêtre lue qui suit un instant de la cadence, en mémoire seule (`secondaire.py:24`, `:29-31`) ; FORMAT §15.4 | **rouge** : condition d'avant remise, `test_releve_au_demarrage_et_instant_saute_rattrape` donne FAIL d'assertion (un seul `releve_asn`, à m(6)). **Leurre L-S1 du réviseur** (`leurre_secondaire`, pool et secondaire réels, puis reprise) : relevé à la première fenêtre et à la première fenêtre après la reprise (avant : seulement aux instants pairs de la cadence) | aucun |
| C-5 | oui : FORMAT §9.1, paragraphe « Instant ISO-8601 » (« T » et « Z » majuscules ; raison : `fromisoformat` ne lit pas pareil de 3.10 à 3.13 ; écart à S2 et à la RFC 3339 nommé) ; deux cas de casse au test ISO | **rouge** : paragraphe retiré, `test_paragraphes_9_et_14_…` donne FAIL d'assertion `[…, False, False]` | aucun |

Questions adjugées, vérifiées au FORMAT :
- Q-1 : « Règle scellée », §15.2 ;
- Q-3 : aucun repli TCP pour le relevé ASN non plus, §12, avec renvoi à SHOGEN-S2BIS-ASN-TRONCATURE-1.

Lignes d'items, vérifiées sur le code et exactes :
- RIPESTAT-FIXTURE-1 : r2.py l.275 et l.292 ;
- ASN-LECTURE-1 : `asn.py:23`, `int()` des cinq textes recalculé (13335, 13335, 13335, 0, 13335) ;
- RFC-REGISTRE-1 : 0 entrée RFC 6793, 5398 ni 5737 à `biblio/INDEX.md` ;
- RECALC-DECODEURS-COPIE-1 : règle `REGLES` de `test_fitness.py:13` ;
- RECALC-CONTEXTE-1 : r1.py l.62-68 ;
- CANONIQUE-OCTETS-1 : FORMAT l.302, « en temps borné » ;
- ASN-HOTE-IPV4-1 : `entree.py:30` ;
- précision de NOMS-HOTE-RFC1123-1.

### A.3 Mutants rejoués (`cc/preuves/mutants-p2a.txt`, 03:54-04:12 UTC)

| mutant | objet | classe | test(s) en échec |
|---|---|---|---|
| G01 | Chainlink : plus de cinq mots (`{320,}`) | TUÉ | `test_chainlink_reponse_mot_2_instant_mot_4` |
| G02 | 2^255 lu positif | TUÉ | idem |
| G03 | signe du décalage ISO ignoré | TUÉ | `test_horodatage_iso_meme_lecture_de_3_10_a_3_13` |
| G14 | AS 0 refusé | TUÉ | `test_cymru_…`, `test_ripestat_…` |
| G17 | dernière chaîne du TXT | TUÉ | `test_cymru_premier_txt_lisible_forme_de_s2` |
| G20 | `periode` de 172 800 s admise | TUÉ | `test_carte_budget_partage_et_regles_croisees` |
| K1-01 | C-1 : borne retirée (`if False:`) | TUÉ | `Bornes` (5) |
| K1-02 | C-1 : négatifs non bornés (`and x > 0`) | TUÉ | `Bornes` (5) |
| K1-03 | C-1 : borne relâchée à 200 000 | **VIVANT** | aucun (O-A1) |
| K1-04 | C-1 : borne de texte × 1 000 | TUÉ | `Bornes` (5) |
| K2-01 | C-2 : `MOTS.match` au lieu de `fullmatch` | TUÉ | `test_chainlink_…` |
| K2-02 | C-2 : AS 0 du TXT perdu (`or None`) | TUÉ | `test_cymru_…` |
| K2-03 | C-2 : plus grande chaîne du TXT | TUÉ | `test_cymru_…` |
| K2-04 | C-2 : 2^255 seul lu positif | TUÉ | `test_chainlink_…` |
| K4-01 | C-4 : rattrapage seulement après deux instants sautés | TUÉ | `test_releve_au_demarrage_…` et 2 autres |
| K4-02 | C-4 : relevé de démarrage seulement sur la cadence | TUÉ | `test_releve_au_demarrage_…` |
| K4-03 | C-4 : `>=` (relevé à chaque fenêtre) | TUÉ | `test_releve_au_demarrage_…`, `test_releve_a_la_cadence_…` |
| K5-01 | C-5 : raison retirée du §9.1 | TUÉ | `test_paragraphes_9_et_14_…` |
| K5-02 | C-5 : « t » et espace admis | TUÉ | `test_horodatage_iso_…` |

Bilan : 19 mutants, 18 TUÉS (runner à 0, ligne s2bis à 1, test visé en échec), 1 VIVANT, 0 FATAL. C-3 est un document
et n'a pas de mutant.

Une première campagne (03:52-03:54) est **invalide et non comptée** (écart E-CC-1) : 4 « TUÉS » sans aucun FAIL. Les
copies portaient des `__pycache__` laissés par mon leurre, et le vérificateur les refusait.

### A.4 Gates (état final P2A, `cc/preuves/matrice/bilan.txt`)

| contrôle | 3.10.20 | 3.11.15 | 3.12.3 | 3.13.14 |
|---|---|---|---|---|
| runner | 136 ok | 136 ok | 136 ok | 136 ok |
| s2bis (`--egal --plancher 297`) | Ran 297, conforme | idem | idem | idem |
| sim-bis (194) | Ran 194, conforme | idem | idem | idem |
| S2 (`--egal`, 415) | rouge : 77 échecs, 3 erreurs | Ran 415, conforme | idem | idem |

- S2 sous 3.10 : c'est SHOGEN-S2-PY310-1, préexistant. Les 80 lignes FAIL et ERROR sont identiques à celles de la base
  du réviseur. `s2-harness/`, `enforcement/` et `scripts/` sont identiques à la base (P2A n'y touche pas).
- Aucune ligne « Warning » ni « Exception ignored » dans les 16 sorties.
- xtask : voir §X.

### A.5 Constats neufs

- **O-A1 (faible ; test).** K1-03 vit : la borne de C-1 relâchée de 16 à 200 000 passe la suite.
  - Le test `Bornes` n'essaie que `1E+1000000` et des entiers de 10^6 chiffres. Or `int(Decimal("1E+199999"))` coûte
    0,51 s (mesuré).
  - Le code corrigé est juste et la liste de l'adjudication est tenue (« borne retirée » est tuée). Seule la résolution
    du test est en cause.
  - Remède possible, un cas : `1E+200000` en moins de 0,1 s. Une borne relâchée en dessous d'environ 10^5 reste
    indécelable par la durée, et quasi équivalente.
  - À adjuger (correctif d'une ligne de test, ou item).
- **O-A2 (nulle ; texte).** La docstring de `_entier` dit « rien de recevable n'est refusé ». Pourtant `0E+16` est
  refusé, alors que `int()` rendrait 0, instant recevable (`0 ≤ ts`). L'instant 1970 n'a aucun sens pour une source :
  c'est sans effet. Il suffirait d'écrire « aucun instant non nul ».

---

## Tranche B (P2B)

### Verdict : CONFORME-AVEC-RÉSERVES

Les sept corrections de la liste fermée (C-1 à C-7), la note Certigna et les items demandés sont faits. J'ai rejoué :
- un rouge par correction (15 retraits, tous FAIL, 0 ERROR) ;
- les sondes et leurres du réviseur (adaptés à C-6 pour C-1 et C-2 ; mémoire de `status`) ;
- les cinq vivants de la G2 (tous tués) ;
- 17 mutants neufs, dont 16 tués.

Gates exactes sur l'état final (298) et sur la variante (340).

**Réserve (liste fermée, un seul point, document) :**
- **R-B1** : préciser la ligne SHOGEN-S2BIS-STATUS-QUEUES-1, détail au §B.6 :
  1. ajouter le déclencheur réel d'un saut d'horloge en avant ;
  2. ajouter un remède qui le couvre (borne de l'étendue de la grille), celui de la ligne ne le couvrant pas ;
  3. dire que l'échec est une trace Python (`MemoryError`, sortie 1), et non un refus nommé.

### B.1 Intégrité et périmètre

- `p2b/SHA256SUMS` : 562 OK, 0 échec (sha256 du fichier `09239cf7…159e`) ; `p2b/g2/SHA256SUMS` : 92 OK. Les
  mini-arbres de travail (`travail/`, `travail2/`, 87 Mo) restent en partie hors SHA256SUMS : c'est déclaré au §10.9,
  et léger.
- Série sur c58b997 : les 10 diffs s'appliquent en `-F0`. Leurs sha256 sont égaux au tableau du générateur.
  - Code et tests ajoutés : 178 / 198 / 98 / 194 / 190 / 192 / 183 / 155 / 142 / 166.
  - Planchers : 262 / 266 / 270 / 274 / 277 / 282 / 287 / 290 / 293 / 298.
  - R-13 : 0 ; lignes de plus de 120 colonnes : 0.
- Variante : 10 diffs en `-F0` sur P2A final ; code ajouté 178 à 198 ; planchers 304 à 340.
- METRIQUES recomptées, égales : 7 fichiers à l'état final, 23 sur la variante.
- **Rien hors liste** : le delta « avant la G2 → corrigé » (`p2b/g2/cc/preuves/delta-v1-final.diff`) touche :
  - `entree.py` : C-6 seulement ;
  - `status.py` : C-3, C-6, C-7 ;
  - `tetes.py` : C-1, C-2, C-5, C-6, et la docstring ;
  - les trois tests (cas de C-1 à C-7, noms en minuscules après C-6) ;
  - FORMAT (§14.1, §15 entrée, §15.2, §15.4, §15.5, §15.7, §15.8, §16.1, §16.3, §16.4, §16.6) ;
  - METRIQUES et plancher.

  Aucun code Certigna, conformément à l'adjudication.

### B.2 Corrections, une par une

| n° | fait | preuve rejouée par le CC | écart |
|---|---|---|---|
| C-1 | oui : `lier` (`tetes.py:114-134`, appel `:292`, avant l'écriture du `.tsr`) contrôle au TSTInfo l'algorithme (SHA-256, NULL), l'empreinte (sha256 du manifeste) et le nonce (absent si la requête n'en a pas) ; écart : `JETON/liaison` ; DER illisible ou type de contenu autre : `JETON/reponse` ; rien n'est conservé ; FORMAT §15.2 et §15.7 | **rouge** : appel retiré, `test_jeton_lie_a_la_requete` donne FAIL. **Fixtures** : les quatre `JETONS` du test sont égaux octet pour octet à `travail2/ref/c1/*.tsr` ; `openssl ts -reply -text` les lit (nonces `…08`, `…09`, « unspecified », autre empreinte). **Leurres S-2/KO-2/KO-3 du réviseur, refaits avec ma propre TSA jetable** (`openssl ts -reply`, clés détruites ; `sondes/sonde_c1c2.py`) : réponse juste émise et `openssl ts -verify` OK ; autre empreinte, autre nonce, sans nonce et nonce en trop : `JETON/liaison`, aucun `.tsr`, l'appel suivant émet ; TSA sha1 seul : `JETON/rejet`. Sur l'état d'avant la G2, tous ces cas étaient « émis » | aucun ; genTime forgé encore « émis » : signature hors ligne, limite déclarée au §15.2 |
| C-2 | oui : siennes lues d'abord, 16 au plus, puis 16 des autres ; `ignores` compte les deux bornes (`tetes.py:257-268`, `:280`) | **rouge** : `lire_tetes(dossier)` remis, `test_sa_tete_toujours_au_manifeste` donne FAIL. **Leurre KO-1** (16 têtes `a00` à `a15`, puis `o1`) : « non armé », `o1` au manifeste, 17 têtes (avant : `JETON/tete`) | aucun |
| C-3 | oui : `_au_dela` (`status.py:59-61`), `ws` ≥ fin du jour du fichier ou `suivante` > fin, et le fichier s'arrête ; jour hors calendrier non lu (`:42-56`) ; plancher de la grille au premier jour moins un (`:106`, `:117`) | **rouge** : contrôle du jour retiré, puis plancher retiré : FAIL de `test_grille_bornee_…` (`MemoryError` sous 512 Mio). **Sonde mémoire du réviseur** sur l'état final : les trois cas sortent en 0, en 0,1 à 0,2 s, avec 22 à 23 Mio (avant : `MemoryError` en 9 s à 1,5 Gio) | résiduel en item : §B.6 |
| C-4 | oui : un test nommé par vivant (G-01 : `test_jeton_lie_a_la_requete` ; G-03 et G-04 : `test_envoi_borne_en_temps_et_en_octets` ; G-16 et G-17 : `test_commande_jeton`) | **rouge** : chaque mutant de la G2 appliqué à l'état final donne FAIL du test nommé, 0 ERROR | aucun |
| C-5 | oui : `secrets.randbits(64)` figé (`mock.call(64)` × 2, nonces des deux `.tsq` différents) ; `jeton` du `tetes` = `{fichier, sha256, manifeste, tsq}` (`tetes.py:247-253`) ; FORMAT §15.5, §15.8 | **rouge** : sha256 du manifeste et du `.tsq` retirés, `test_jeton_du_jour_…` donne FAIL ; G-16 donne FAIL de `test_commande_jeton` | aucun |
| C-6 | oui : `[a-z0-9]{1,16}` au descripteur (`entree.py:79`), au dépôt (`tetes.py:32`) et aux résumés (`status.py:32`) | **rouge** aux trois points (majuscules remises) : FAIL de `test_point_d_entree_…`, `test_lecture_du_depot_…` et `test_resumes_hostiles_refuses` | aucun |
| C-7 | oui : « hors D-3 » sur les deux lignes de compte (`status.py:185`, `:211`) ; FORMAT, entrée du §15 : dépôt local, synchronisé par une unité séparée (DB-4) | **rouge** : FAIL de `test_sante_seule_…` et de `test_compte_a_quorum_…` | la phrase du FORMAT n'est figée par aucun test (O-B1) |

### B.3 Mutants rejoués (`p2b/g2/cc/preuves/mutants-p2b.txt`, 04:24-04:43 UTC ; variante : `mutants-p2b-variante.txt`)

| mutant | objet | classe | test(s) en échec |
|---|---|---|---|
| G-01 | statut 1 refusé | TUÉ | `test_jeton_lie_a_la_requete` |
| G-03 | http sans délai | TUÉ | `test_envoi_borne_en_temps_et_en_octets` |
| G-04 | `r.read()` sans borne | TUÉ | idem |
| G-16 | nonce constant | TUÉ | `test_commande_jeton` |
| G-17 | contexte TLS non transmis | TUÉ | idem |
| K-C1-1 | nonce non contrôlé | TUÉ | `test_jeton_lie_a_la_requete` |
| K-C1-2 | empreinte non contrôlée | TUÉ | idem |
| K-C1-3 | algorithme non contrôlé (étiquette seule) | TUÉ | idem |
| K-C1-4 | type TSTInfo non contrôlé | TUÉ | idem |
| K-C2-1 | borne commune de 16 | TUÉ | `test_sa_tete_toujours_au_manifeste` |
| K-C2-2 | `ignores` mal compté | TUÉ | idem, et `test_seize_tetes_…` |
| K-C3-1 | plancher de deux jours | TUÉ | `test_grille_bornee_par_le_jour_des_fichiers` |
| K-C3-2 | `suivante` non bornée | TUÉ | idem |
| K-C3-3 | jour hors calendrier qui lève | TUÉ | idem |
| K-C4-1 | délai décuplé | TUÉ | `test_envoi_borne_…` |
| K-C4-2 | lecture jusqu'à 2 × PLAFOND | TUÉ | idem |
| K-C5-1 | mauvais fichier haché | TUÉ | `test_jeton_du_jour_…`, `test_lecture_sans_attente_…` |
| K-C5-2 | nonce de 32 bits | TUÉ | `test_commande_jeton` |
| K-C6-1 | casse repliée au descripteur | TUÉ | `test_point_d_entree_…` |
| K-C6-2 | jumeau de casse lu au dépôt (`re.I`) | TUÉ | `test_lecture_du_depot_…` |
| K-C7-1 | mention « hors D-3 » déplacée | TUÉ | `test_sante_seule_…` |
| K-C7-2 | phrase « dossier local » retirée du FORMAT | **VIVANT** | aucun (O-B1) |
| variante : G-16, G-17, K-C5-2, K-C6-1 sur `entree.py` fusionné | | 4 TUÉS | `test_commande_jeton`, `test_point_d_entree_…` |

Bilan : 26 mutants, 25 TUÉS par leur test visé, 1 VIVANT, 0 FATAL.

### B.4 Gates

| arbre | runner | s2bis | sim-bis | S2 | avertissements |
|---|---|---|---|---|---|
| P2B final, 3.10 à 3.13 (`matrice-final/bilan.txt`) | 136 ok × 4 | Ran 298, conforme × 4 | Ran 194 × 4 | 415 conforme sous 3.11-3.13 ; 3.10 rouge, 80 lignes FAIL/ERROR identiques à la base (SHOGEN-S2-PY310-1) | 0 |
| variante, 3.10 à 3.13 (`matrice-variante/bilan.txt`) | 136 ok × 4 | Ran 340, conforme × 4 | Ran 194 × 4 | idem | 0 |

xtask : voir §X.

### B.5 Variante sur P2A

- Le FORMAT porte le §15 de P2A, puis les §16 et §17 de P2B. Les renvois §16.4, §16.6, §16.9 et §17.6 sont
  renumérotés. Aucun « § » n'apparaît dans `tetes.py` ni `status.py`.
- `entree.py` fusionné : aiguillage `jeton`, `status`, `resume` avant celui de P2A ; `construire(*args, a.depot) if pool
  else construire_secondaire(*args)`. La règle `observateur-nom` vaut désormais aussi pour `secondaire` : c'est voulu
  par C-6, et toute la suite passe.
- Limite déclarée : la tête du journal secondaire n'est pas exportée (I-4).

### B.6 Jugement demandé : résiduel de C-3 et ligne Certigna

**SHOGEN-S2BIS-STATUS-QUEUES-1 (résiduel de C-3).**
- Mesure rejouée sur l'état final (`travail2/outils/sonde_grille.py`) : journal sain d'une ligne, plus
  `pool-2999-01-01-0.jsonl` portant un marqueur de ce jour. `status` sort en 1 sur `MemoryError` en 3,1 s, à 512 Mio.
  Le chiffre de la ligne (3,0 s) est exact.
- **Le choix d'en faire un item est admissible.** Les deux règles écrites de C-3 sont codées à la lettre et testées.
  Le résiduel passe par le **nom** d'un fichier, hors du texte de l'adjudication. La règle PAROXYSME veut qu'une
  limite soit rendue, et elle l'est.
- **La ligne n'est pas exacte au regard du code sur trois points (réserve R-B1) :**
  1. Le déclencheur ne se limite pas à un nom de fichier forgé : l'écrivain lui-même crée un tel fichier après un saut
     d'horloge en avant. La boucle prend `ws` sur l'horloge murale (`boucle.py:82`) et l'écrivain nomme le fichier par
     le jour de `ws` (`journal.py:118`, `:139`).
  2. Le remède proposé, « écarter les noms d'un jour postérieur au lendemain de l'horloge », ne couvre pas ce cas :
     `status` tourne sous la même horloge sautée. Une borne de l'étendue de la grille la couvre (par exemple la
     rétention locale de 7 jours, ou un nombre de fenêtres au plus).
  3. L'échec est une trace Python (`MemoryError`, sortie 1), pas un refus nommé.

  Gravité faible : il faut plusieurs années de saut sous 512 Mio. La ligne mêle en outre O-3 (fichier arrêté sans le
  dire) et ce résiduel ; les séparer serait plus clair. Le déclencheur « G0 de RB-18 (lecteur commun du recalcul) »
  n'a pas été vérifié par moi, faute d'avoir lu la pièce de RB-18.

**SHOGEN-S2BIS-TSA-CERTIGNA-1.** La ligne est complète au regard de l'adjudication :
- URL https ;
- forme de l'authentification de la requête et lieu de ses secrets, jamais journalisés ni commités ;
- identifiants des observateurs et lien au nom `[a-z0-9]{1,16}` ;
- déclencheur : lot 7.

Elle ajoute à bon droit la politique (`reqPolicy`) et la chaîne de certificats de la TSA, statut qualifié compris. Elle
est exacte au regard du code :
- `envoyer` ne pose que `Content-Type` (`tetes.py:297-316`) ;
- `requete` ne porte ni `reqPolicy` ni extension (FORMAT §15.1) ;
- la signature se vérifie hors ligne.

Aucun code Certigna n'a été ajouté.

**Autres lignes, vérifiées sur le code et exactes :**
- DEPOT-LIENS-1 : `lire_borne` ouvre en `O_RDONLY | O_NONBLOCK`, sans `O_NOFOLLOW` (`tetes.py:168`) ;
- JOURNAL-FICHIER-SPECIAL-1 : mesuré. Un tube au nom `pool-2026-10-09-0.jsonl` bloque `status` jusqu'à la borne de
  5 s (sortie 124) ; `status.py:67` ouvre sans `O_NONBLOCK` ;
- ENVOI-ECHEANCE-1 : `timeout=delai` par opération, `getaddrinfo` non borné ;
- OBSERVATEURS-LISTE-1 et RB3-DEGRADATIONS-1 : descriptives et justes ;
- volets ajoutés à CONFIG-PRODUCTION-1 et à CHRONYC-FORMAT-1 : conformes à l'adjudication.

### B.7 Constats neufs

- **O-B1 (faible ; test).** K-C7-2 vit. La phrase du FORMAT sur le dépôt local (C-7) n'est figée par aucun test,
  ni aucune phrase des §15 et §16 de P2B : `test_format` n'est pas touché par P2B, alors que P2A fige ses paragraphes
  par `test_format`. L'adjudication n'exigeait pas de test pour cette phrase. À adjuger : item, ou un cas de
  `test_format` au gel du FORMAT.
- **O-B2 (nulle ; forme).** Le rapport dit « octet 92 seulement dans des littéraux ». Or l'un est une continuation de
  ligne : dans `test_tetes.py` (CB-15c), après `vus.append(b.depot)),`. Elle est présente dès la phase 1 et n'a pas été
  relevée par la G2. Sans effet.

---

## X. xtask (lignes de verdict seules, comparées au témoin c58b997)

`cargo --locked xtask verify`, hors ligne, réseau isolé, cible dédiée (`cc/outils/xtask.sh`). La sortie brute n'est
jamais écrite : seules les lignes de verdict sont filtrées au fil.

| arbre | lignes de verdict | code | comparaison au témoin |
|---|---|---|---|
| témoin c58b997 (`p2a/g2/cc/preuves/xtask-temoin-c58b997.txt`) | 22 : S-G1 à S-G8 VERT ; S-G9 ROUGE (1 violation) ; fmt, no_std et clippy VERT ; global ROUGE | 1 | — |
| P2A final (`p2a/g2/cc/preuves/xtask-p2a-final.txt`) | 22 | 1 | identiques (`diff` vide) |
| P2B final (`p2b/g2/cc/preuves/xtask-p2b-final.txt`) | 22 | 1 | identiques |
| variante (`p2b/g2/cc/preuves/xtask-variante.txt`) | 22 | 1 | identiques |

S-G9 est ROUGE d'une violation des deux côtés : c'est le rouge connu des copies. Je n'ai pas relu son emplacement
(`docs/17-modele-de-menace.md:70` selon les deux G2), puisque la sortie brute n'est pas lue.

## Écarts du CC

- **E-CC-1** : mon leurre `leurre_secondaire` lance des enfants `python3` sans `-B`. Il a laissé deux `__pycache__`
  dans `cc/etats/final` (P2A), d'où une première campagne invalide (03:52-03:54 UTC). Cette campagne est arrêtée, non
  comptée, et versée sous `cc/preuves/invalide-mutants-p2a-pycache.txt`. Les `__pycache__` ont été retirés. L'état a
  été recomparé à une application neuve de la série (identique), puis la campagne refaite. Mon outil de mutants refuse
  désormais un état qui porte un `__pycache__`.
- **E-CC-2** : la sonde C-1/C-2 de P2B, lancée en `-I`, ignore `PYTHONDONTWRITEBYTECODE`. Elle a laissé 4
  `__pycache__` dans `p2b/g2/cc/etats/{final,v1}` (03:57), retirés à 03:59, avant toute campagne P2B. Depuis, j'emploie
  `-B` explicite.
- **E-CC-3** : une heure des NOTES (« 04:00 ») a d'abord été écrite par estimation. Elle est corrigée sur `date -u`
  (03:52).
- **E-CC-4** (barres obliques inverses) : `cc/outils/rouge_c45.py` porte 2 octets 92 (un saut de ligne échappé dans une
  ancre Python). L'ancre a été trouvée une seule fois, donc les octets sont justes. Trois commandes ont aussi porté des
  échappements : `python3 -c` avec des chiffres arabes-indiens, et deux éditions par script. Contrôle sur les octets
  écrits : 0 octet 92 dans tous les autres outils, sondes et listes du CC, dans les NOTES et dans ce rapport.
- **E-CC-5** : les leurres de C-1 et C-2 de P2B sont **adaptés** de `sonde_tetes.py` du réviseur, car sa TSA a ses
  clés détruites et ses noms (« O1 ») sont devenus invalides par C-6. J'ai fait ma propre TSA jetable sous
  `p2b/g2/cc/tmp/tsa`, avec des noms en minuscules et des refus attrapés. Les clés sont détruites en fin de passe.

## Journal de provenance (G1)

**[lu]**
- `p2a/ADJUDICATION-G2.md` (`be4bb4eb…`) ; `p2a/g2/RAPPORT-G2.md` (`2d7b5be5…`), en entier ;
  `p2a/RAPPORT-GENERATEUR.md` (`8a2754a4…`), section « Corrections de la G2 » en entier et le reste par titres ;
  `p2a/BRIEF-P2A.md` ; `p2a/G1-JOURNAL.md` (`2a7a7201…`), l.1-5 et l.190-200.
- `p2b/ADJUDICATION-G2.md` (`d98f8639…`) ; `p2b/g2/RAPPORT-G2.md` (`b253aa11…`), en entier ;
  `p2b/RAPPORT-GENERATEUR.md` (`651d1e64…`), §10 en entier ; `p2b/BRIEF-P2B.md`.
- Les 8 + 10 + 10 diffs, appliqués ; code et tests finals lus aux lignes citées.
- Deltas « avant la G2 → corrigé » lus en entier pour le code, les tests et le FORMAT ; METRIQUES par sections.
- `gates.yml` l.146-250 ; `verdict-suite-s2.py` par recherche des codes de sortie.
- `s2-harness/shogen_s2/sources.py` l.237-285 ; `r2.py` (recherche de trois `def`) ; `r1.py` l.62-68 ;
  `test_fitness.py` l.12-17.
- Outils et leurres des deux réviseurs (en-têtes et corps exécutés) ; `travail2/outils/sonde_grille.py` du générateur ;
  `travail2/ref/c1/verification.txt`.

**[2nd]**
- RFC 3161 §2.2 et §2.4.2 : citations de la G2 et du FORMAT, non relues sur le registre par moi. Mon jugement sur C-1
  repose sur le code et sur `openssl`.

**[abs]**
- Pièce de RB-18 (déclencheur de STATUS-QUEUES-1) : non lue.
- Aucune pièce de D.2, aucun `*.jsonl` réel, aucun dossier interdit.
- Aucun réseau réel, aucune clé ni secret ; rien sur Pocket.

**Commandes principales et sorties** (`p2a/g2/cc/preuves/`, `p2b/g2/cc/preuves/`) :
- `sha256sum -c` ;
- `patch -p1` des séries ;
- `outils/rouge_c2.py`, `rouge_c45.py`, `rouge_p2b.py` (rouges) ;
- `outils/mutants_cc.py` avec `liste_p2a.json`, `liste_p2b.json`, `liste_p2b_variante.json` ;
- `outils/gates.sh` (matrices) et `outils/xtask.sh` ;
- sondes `s1_entier.py`, `s2_int.py`, `sonde_c1c2.py`, `jetons.py`, sonde FIFO ;
- leurres du réviseur : `leurre_echeance`, `leurres_decodeurs`, `mesure_exposant`, `leurre_secondaire`,
  `sonde_status_memoire` ;
- `metriques.py` et `forme.py`.

**Chiffres recomptés par moi** : 289, 72, 562 et 92 lignes OK ; lignes ajoutées et planchers par diff ; METRIQUES (19,
7 et 23 fichiers) ; Ran 297, 298, 340, 194, 415 ; 80 lignes S2 3.10 ; 45 mutants (43 tués, 2 vivants, 0 FATAL) ;
durées et mémoire des sondes.
