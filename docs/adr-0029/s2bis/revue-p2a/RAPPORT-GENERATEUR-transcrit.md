# Rapport du générateur de P2A, avec la section datée des corrections (transcrit)

> Transcription par l'orchestrateur le 2026-10-09 06:28:34 UTC du fichier RAPPORT-GENERATEUR.md ; contrôle FM-1.1 des quatorze transcripts d'agents qui ont touché `s2bis/p2a` ou `s2bis/p2b` : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Rapport du générateur : lot P2A (S2-bis, partie P2, tranche A : CB-6, CB-12, CB-13)

**Gate 0 : `claude-opus-5-5`**, l'identifiant exact du modèle qui tourne.

Base : 5cfe746, celle du brief. À 20:41 UTC, HEAD du dépôt réel est passé à `826c57e` (cinq commits SIM-BIS
SB-15A à SB-15E). Dans les chemins de la série, seul le plancher sim-bis de `gates.yml` y change (172 → 185). La
série s'applique aussi sur 826c57e ; sur cet arbre, runner 136, s2bis 291, sim-bis 185 et S2 415 sont conformes sous
3.12. Aucun commit, aucune écriture git. Je livre une série de diffs à adjuger.

## Série livrée (`p2a/diffs/`, dans l'ordre)

| diff | objet | code ajouté | plancher s2bis | mutants |
|---|---|---|---|---|
| CB-6a | 8 décodeurs BTC des places repris de S2, fixtures copiées octet pour octet, finitude, aucun flottant | 200 | 263 | 20/20 |
| CB-6b | CoinGecko, DefiLlama, Chainlink (hexadécimal strict, prix exact) ; contexte `Decimal` nommé | 59 | 265 | 12/12 |
| CB-6c | `decodeur` dans chaque forme ; lecture décodée ; les valeurs que l'écrivain refuserait sont rendues en `panne_decode` | 145 | 271 | 16/16 |
| CB-6d | tardives bornées, niveaux comptés sur les octets, graphe partagé refusé en temps borné | 124 | 276 | 11/11 |
| CB-12a | DNS : drapeau TC (section non lue, sans repli TCP), identifiant sur 16 bits | 61 | 279 | 11/11 |
| CB-12b | relevé ASN : A au résolveur propre, RIPEstat, Team Cymru ; échecs typés | 196 | 284 | 17/17 |
| CB-13a | processus secondaire : boucle de la carte ; relevé ASN hors du fil qui écrit, à la cadence scellée | 115 | 287 | 11/11 |
| CB-13b | `carte.json`, 5 règles croisées (dont `budget-partage`, E-C-33, et `hors-delta`) ; commande `secondaire` ; FORMAT §15 | 199 | 291 | 21/21 |

Total : 1 099 lignes `.py` et `.yml` (387 de production, 704 de tests). Mutants : 119 tués sur 119, aucun vivant, aucun
FATAL. Les mutants sont classés par la commande du job : le runner, puis la ligne s2bis de `gates.yml`, avec une
borne de 300 s. Chaque diff ajoute sa section METRIQUES ; CB-6a et CB-6b ajoutent la ligne G6 des fixtures copiées.

## Vérifications

- Chaque état de la série, sous python3.12 `-X dev -W error` et réseau isolé : runner `136 ok`, et s2bis conforme au
  plancher exact (`--egal`), de 263 à 291.
- État final, Python 3.10 à 3.13 : runner 136, s2bis 291 et sim-bis 172 conformes partout. S2 415 est conforme
  sous 3.11 à 3.13 ; sous 3.10, S2 est rouge comme l'item connu SHOGEN-S2-PY310-1 l'annonce (77 échecs, 3 erreurs).
  Les sorties ne contiennent aucune ligne « Exception ignored » ni « Warning ».
- La série s'applique sur une archive fraîche de 5cfe746 (`patch -p1` comme `git apply` rendent 0). Les 34 fichiers
  touchés sont égaux à l'état final.
- `cargo --locked xtask verify` sur la copie : S-G1 à S-G8, fmt, no_std et clippy sont VERT. S-G9 est ROUGE d'une
  seule violation, `docs/17:70`, connue du brief sur les copies (elle renvoie vers `docs/rapports/`, exclu).
- Contrôles de forme : aucun `__pycache__`, aucun octet 92 ajouté, aucun marqueur R-13. Bibliothèque standard seule
  (R-8). `SHOGEN_S2_CAMPAGNE_CONTROL` n'est jamais posée.

## Items de l'annexe B fermés (6), chacun par un test nommé

- ECRIVAIN-REFUS-ARRET-1 (part des décodeurs), CB-6c : `test_decodeurs.Politique.test_valeurs_refusees_par_l_ecrivain_jamais_rendues`.
- TARDIVES-BORNE-1, CB-6d : `test_boucle.Boucle.test_resultat_rendu_avant_la_place`.
- ECRIVAIN-IMBRICATION-OCTETS-1, CB-6d : `test_reprise.Reprise.test_niveaux_comptes_sur_les_octets_avant_le_decodeur`.
- CORPS-BORNE-1 (volet graphe), CB-6d : `test_journal.Ecrivain.test_graphe_partage_refuse_en_temps_borne`.
- DNS-TC-1, CB-12a : `test_dns.Interroger.test_drapeau_tc_garde_section_reponse_non_lue`.
- DNS-ID-16BITS-1, CB-12a : `test_dns.Interroger.test_identifiant_hors_de_16_bits_refus_nomme`.

## Questions de valeur et items à former

- Q-1 : budget de débit partagé. La règle du lot limite le pool et la carte, ensemble, à 5 lectures par hôte et par
  fenêtre. Le chiffre revient au G0 de la carte (CARTE-AVEUGLE-1).
- Q-2 : un relevé ASN manqué (fenêtre sautée, arrêt) n'est pas rattrapé : l'observateur perd ce relevé du jour.
  Faut-il le rattraper ?
- Q-3 : il n'y a pas de repli TCP sous TC. Une réponse A tronquée fait perdre le relevé ASN de l'hôte. Règle à adjuger.
- I-1 (proposé : ISO-CASSE-1) : le motif ISO n'admet que « T » et « Z ». S2 admettait « t » et l'espace ; la RFC 3339
  admet « t » et « z ». Mesuré, sans effet sur les fixtures.
- I-2 (proposé : RIPESTAT-FIXTURE-1) : les corps de RIPEstat et de Cymru des tests sont synthétiques ; il faut les
  capturer avant le gel.
- I-3 (proposé : RFC-REGISTRE-1) : les RFC 5398, 5737 et 6793 sont citées sans entrée au registre.
- I-4 et I-5 (G0 de RB-2) : le re-décodage au recalcul exige une copie des décodeurs, gardée égale par un test. Le
  contexte `Decimal` nommé n'a pas encore de test d'égalité côté recalcul.

## Écarts (détail : `G1-JOURNAL.md` §4)

- Le §15 du FORMAT, qui couvre CB-12b et CB-13a, n'arrive qu'avec CB-13b.
- Après les campagnes, j'ai corrigé deux docstrings et versé METRIQUES et G6 (`config.py` ; `decodeurs.py` :
  « ADR-0029 l.169 » devient « l.167 »). J'ai ensuite rejoué les états, la campagne de CB-13b et la matrice.
- Rouges partiels : CB-6a, CB-6b et CB-13a ont des tests qui passent sur le bouchon par construction. Le rouge de
  CB-12b a été refait (7 échecs d'assertion).
- La suite S2 est rouge sous 3.10, comme l'item connu SHOGEN-S2-PY310-1 l'annonce : c'est préexistant.
- Trois commandes contenaient des barres obliques inverses ; j'ai contrôlé les octets écrits (0 octet 92).

## Estimation révisée des sous-lots restants de P2

Mesure : la tranche A fait 1 099 lignes contre ≈ 500 estimées (× 2,2 ; P1 était à × 2,4). Restent CB-7 (≈ 180),
CB-8 (≈ 170), CB-9 (≈ 180), CB-14.k (≈ 175 × k, k de 2 à 4), CB-15 (≈ 180), CB-16 (≈ 140) et CB-17 (≈ 160), soit
1 360 à 1 710 lignes estimées. Révision : 3 000 à 4 100 lignes avec tests, soit 16 à 21 diffs de 200 lignes au plus,
sans compter les corrections de G2. Sans réseau, aucune fixture neuve ne peut être capturée. CB-7, CB-8, CB-9 et
CB-14.k attendent donc une passe de capture (et LICENCES-API-1 ; CB-7 attend aussi PAIRES-1). CB-17 et CB-15 peuvent
partir sans capture.

## Pièces

`p2a/diffs/` (8 diffs), `p2a/preuves/` (rouges, campagnes, états, matrice, xtask, mesures), `p2a/outils/`,
`p2a/NOTES.md`, `p2a/G1-JOURNAL.md`, `p2a/RAPPORT-GENERATEUR.md`, `p2a/SHA256SUMS`. Les copies lourdes sont nettoyées.

## Corrections de la G2 (section datée du 2026-10-09 00:06:08 UTC, heure produite par `date -u`)

**Gate 0 : `claude-opus-5-5`.** Mandat : `ADJUDICATION-G2.md` (liste fermée C-1 à C-5), brief en vigueur. Base
c58b997 ; tête réelle relue à 00:06 UTC : `ebd156071794a92dc72a69ae5e62bf0e76a03a62`. Entre c58b997 et ebd1560,
`git diff --stat` sur `gates.yml`, `s2bis/` et `docs/adr-0029/s2bis/` est vide. Aucune écriture git. Série corrigée
sous les mêmes noms (CB-6a … CB-13b) ; aucun diff neuf. La série d'avant la G2 est gardée sous `diffs/envoi-1/`.

### Série corrigée (`diffs/`)

| diff | code ajouté | plancher s2bis (`--egal`) | corrections portées |
|---|---|---|---|
| CB-6a | 200 | 263 | aucune |
| CB-6b | 116 | 270 | C-1 (aide `_entier`, cinq sites, cinq tests `Bornes`) ; C-2 G01, G02, G03 |
| CB-6c | 147 | 276 | C-5 (FORMAT §9.1) ; C-3 déclaré (METRIQUES) |
| CB-6d | 124 | 281 | aucune (rejoué) |
| CB-12a | 61 | 284 | aucune (rejoué) |
| CB-12b | 198 | 289 | C-2 G14, G17 |
| CB-13a | 133 | 293 | C-4 (relevé au démarrage, rattrapage en mémoire) |
| CB-13b | 200 | 297 | C-2 G20 ; FORMAT §15.2 (Q-1 scellée), §15.4 (C-4), §12 (Q-3) |

Total 1 179 lignes `.py` et `.yml` : 410 de production, 761 de tests, 8 de `gates.yml`. Aucun octet 92 ajouté, aucun
marqueur R-13 (`preuves/corrections/forme-diffs.txt`, recalculé à 00:00 UTC, égal). Chaque diff porte sa section
METRIQUES, recomptée (`preuves/corrections/metriques-serie-2.txt`).

### Tableau des corrections

| n° | fait | test(s) | rouge d'assertion avant le code | mutants |
|---|---|---|---|---|
| C-1 | `decodeurs._entier`, seule aide, aux cinq sites (OKX `ts`, DefiLlama `timestamp`, Bitstamp `timestamp`, Gemini `volume.timestamp`, CoinGecko `last_updated_at`). Refus avant `int()` d'un Decimal fini d'exposant ajusté ≥ `CHIFFRES` = 16 (motif : 2^53 < 10^16, donc un tel instant, en s ou en ms, dépasse 2^53 µs, FORMAT §9.2), et d'un texte de plus de `TEXTE` = 4 300 caractères (limite par défaut de `int()`, quelle que soit la configuration) | `test_decodeurs.Bornes` : un test par champ ; nombre JSON `1E+1000000`, entier de 10^6 chiffres (±), texte de 10^6 chiffres, limite de l'interpréteur levée ; `panne_decode` en moins de 0,1 s, plus un témoin écrit à la main | `preuves/C-1/rouge-6b.txt` : 5 échecs d'assertion (un par champ, `panne_decode` après plus de 0,1 s) | MC1-01 « borne retirée », MC1-02 à MC1-10 (bornes relâchées ou serrées, chaque site sans l'aide) : 10/10 tués par le test visé |
| C-2 | six cas, valeurs écrites à la main : six mots de Chainlink, réponse égale à 2^255, décalage ISO « -05:00 », AS 0 (RIPEstat et TXT), première chaîne du TXT, `periode` de 86 401 s | `test_chainlink_reponse_mot_2_instant_mot_4`, `test_horodatage_iso_meme_lecture_de_3_10_a_3_13`, `test_ripestat_forme_de_s2_bornes_et_base_muette`, `test_cymru_premier_txt_lisible_forme_de_s2`, `test_carte_budget_partage_et_regles_croisees` | le code d'avant était juste ; le rouge est montré sous les six mutants du réviseur (`preuves/C-2/rouge-sous-mutants-g2.txt` : six fois code 1, échecs d'assertion) | G01, G02, G03, G14, G17 et G20 tués par le test visé ; MC2-01 à MC2-05 tués |
| C-3 | écart déclaré : la tranche A ne verse aucune forme de requête BTC (section METRIQUES de CB-6c, G1 §8, ce rapport) ; item neuf SHOGEN-S2BIS-FORMES-BTC-1, déclencheur CB-8 | document, sans test | sans objet | sans objet |
| C-4 | Q-2 adoptée. Un relevé ASN est dû à la première fenêtre de chaque exécution, puis à la première fenêtre lue qui suit un instant de la cadence. Un instant sauté est rattrapé en mémoire, sans relecture du journal (E-C-15). Écrit au FORMAT §15.4. Le code reste sous 200 lignes et dans le lot : aucun item | `test_secondaire.Secondaire.test_releve_au_demarrage_et_instant_saute_rattrape` | `preuves/C-4/rouge-13a.txt` : 1 échec d'assertion | MC4-01 à MC4-03 tués |
| C-5 | I-1 : la restriction du motif ISO (« T » et « Z » majuscules ; « t », « z », l'espace et `+hhmm` refusés) est écrite au FORMAT §9.1 avec sa raison (`fromisoformat` lit différemment de 3.10 à 3.13, mesuré), comme un écart à S2 et à la RFC 3339 §5.6 | `test_format.Format.test_paragraphes_9_et_14_valeurs_et_decodeur` | `preuves/C-5/rouge-6c-format.txt` : 1 échec d'assertion | MC5-01 à MC5-03 tués |

### Mutants (classés par la commande du job : runner, puis ligne s2bis de `gates.yml`, borne de 300 s, python3.12)

- Les 26 mutants du réviseur, rejoués sur l'état final : **26 tués sur 26**, dont les six vivants de la G2, chacun
  tué par son test visé. Joués deux fois : 22:48 UTC (`preuves/corrections/mutants/g2-26-sur-13b.txt`) et 23:51 UTC
  (`…/g2-26-sur-13b-2.txt`).
- Mutants neufs des corrections : 21, tous tués. C-1 : 10 (6b, `corr-6b.txt` 8 et `corr-6b-sites.txt` 2). C-2 : 5
  (6b, 12b, 13b). C-4 : 3 (13a). C-5 : 3 (6c). Chaque correction de code en compte au moins deux.
- Campagnes des sous-lots, rejouées sur les états corrigés : 20, 12, 16, 11, 11, 17, 11 et 21, soit 119 tués sur
  119. Celle de 13b a été jouée deux fois.
- Bilan général : 0 vivant et 0 FATAL ; le témoin est vert à chaque campagne. M12b-11 est tué hors du test visé,
  comme déjà déclaré en E-5.

### Matrice et jobs (réseau isolé, `-X dev -W error`, aucune ligne « Exception ignored » ni « Warning »)

| contrôle | résultat |
|---|---|
| chaque état, python3.12 (`preuves/corrections/etats-2/`) | runner 136 ok ; s2bis conforme à 263, 270, 276, 281, 284, 289, 293, 297 |
| état final, 3.10.20 / 3.11.15 / 3.12.3 / 3.13.14 (`preuves/corrections/matrice/`) | runner 136 ok ; s2bis 297 ; sim-bis 194 ; S2 415 conforme sous 3.11 à 3.13 |
| S2 sous 3.10 | 77 échecs, 3 erreurs, 2 sauts : les 80 lignes FAIL et ERROR sont identiques à celles d'avant la G2 (`preuves/final2/s2-3.10.txt`), soit SHOGEN-S2-PY310-1, préexistant |
| tête réelle ebd1560 + série, 3.12 (`preuves/corrections/tete-ebd/`) | `patch -p1` à 0 pour les huit diffs ; 34 fichiers sur 34 égaux à l'état final ; runner 136, s2bis 297, sim-bis 194, S2 415 conformes |
| archive fraîche c58b997 (`preuves/corrections/serie-appliquee.txt`) | `patch -p1` et `git apply` hors dépôt à 0 pour les huit diffs ; 34 fichiers sur 34 égaux |
| `cargo --locked xtask verify`, état final (`preuves/corrections/xtask.txt`) | S-G1 à S-G8 VERT, fmt, no_std et clippy VERT ; S-G9 ROUGE d'une seule violation, `docs/17-modele-de-menace.md:70`, connue des copies |

### Lignes d'items (constat, propriétaire, déclencheur, prix, origine)

| item | constat | propriétaire | déclencheur | prix | origine |
|---|---|---|---|---|---|
| SHOGEN-S2BIS-FORMES-BTC-1 | la tranche A de P2 ne verse aucune forme de requête BTC (aucune entrée de `formes.json`, aucune donnée sous `s2bis/config/`) : elle verse les décodeurs et les fixtures seulement ; les requêtes BTC de S2 restent dans `s2-harness/shogen_s2/sources.py` (`SPECS`, l.239-283) ; écart déclaré au rapport, au G1 et à la section METRIQUES de CB-6c | orch. | CB-8 (CoinGecko, DefiLlama et Bitfinex y deviennent regroupées, E-C-09 ; le plan d'OKX y passe à cinq lectures) | une forme par flux BTC gardé et un test qui compare chaque forme gardée aux octets de la requête de S2 (E-C-09 : « requête BTC de S2 gardée ») ; ≈ 40 lignes de données et 30 de test [inféré] | C-3 de la G2 de P2A (brief P2A l.6 ; PROPOSITION l.214) |
| SHOGEN-S2BIS-ASN-TRONCATURE-1 | sans repli TCP (§12, Q-3 adjugée : aucun repli pour D-4 et D-5), une réponse A ou TXT au drapeau TC laisse l'hôte sans `ip` (`reponses` null) ou sans `cymru.asn` : le relevé ASN de cet hôte est perdu ce jour-là ; le taux de troncature réel est inconnu (aucun réseau en P2A) | orch. | rodage (lecture « ASN » de classe M), adjugé avant le gel | une mesure au rodage (part des `asn` dont `a` ou `cymru` porte le drapeau TC, par hôte et par jour), puis une adjudication : repli TCP pour le seul relevé ASN (hors échéance, processus secondaire) ou règle gardée [inféré] | Q-3 de P2A, avis du réviseur (RFC 2181 §9, RFC 7766, [2nd]) ; adjudication du 2026-10-08 |
| SHOGEN-S2BIS-RIPESTAT-FIXTURE-1 | les corps RIPEstat (`prefix-overview`) et les TXT de Team Cymru des tests de CB-12b sont synthétiques, écrits d'après la forme que lit S2 (r2.py l.275-312), sans capture ; les conditions d'usage de RIPEstat et de Team Cymru ne figurent pas parmi celles lues le 2026-10-08 (B.81 : Binance Vision, Bitstamp, Kraken, OKX, Coinbase, Bitfinex ; voir SHOGEN-S2BIS-CONDITIONS-DECLAREES-1) | orch. | passe de capture, avant le gel | une capture datée de chaque base (sha256 consigné), deux fixtures, un test d'égalité de lecture ; lecture des deux conditions [inféré] | I-2 du générateur de P2A ; G2 de P2A §8 |
| SHOGEN-S2BIS-ASN-LECTURE-1 | `asn` de RIPEstat (texte) et premier nombre du TXT de Cymru sont lus par `int()` de S2 (`asn.py` l.23 ; écrit au §15.4) : le souligné (« 13_335 »), le signe (« +13335 », « -0 »), les blancs et les chiffres arabes-indiens sont admis (mesuré par la G2, L-A1 et L-A2 ; `int()` recontrôlé sur ces cinq textes : 13335, 13335, 13335, 0, 13335) | orch. | avec SHOGEN-S2BIS-RIPESTAT-FIXTURE-1, avant le gel | une décision : lecture stricte en chiffres ASCII (écart à S2 nommé au §15.4) ou forme de S2 gardée ; ≈ 10 lignes et un test [inféré] | O-2 de la G2 de P2A |
| SHOGEN-S2BIS-RFC-REGISTRE-1 | RFC 6793 (`asn.py` l.18), RFC 5398 et RFC 5737 (`tests/test_asn.py` l.1-5) sont nommées sans entrée au registre `biblio/INDEX.md` (0 occurrence, compté) ; citées de mémoire [2nd] | orch. (lecteur) | G2 de clôture de P2 | trois entrées au registre, lues sur pièce, ou renvois retirés ; une passe de lecture [inféré] | I-3 du générateur de P2A |
| SHOGEN-S2BIS-RECALC-DECODEURS-COPIE-1 | le re-décodage au recalcul (E-R-03) ne peut importer `collecte.decodeurs` : la règle codée de `test_fitness` refuse `recalc` → `collecte` (plus serrée que PROPOSITION §1 pt 2, vérifié par la G2) | orch. | G0 de RB-2 | une copie des décodeurs sous `recalc`, gardée égale par un test (comme la lecture JSON stricte et le compte des niveaux), ou un amendement daté de RB-2 ; ≈ 150 lignes copiées et 20 de test [inféré] | I-4 du générateur de P2A ; G2 de P2A §8 |
| SHOGEN-S2BIS-RECALC-CONTEXTE-1 | le contexte `Decimal` nommé des décodeurs (`decodeurs.CONTEXTE`, copie de r1.py l.62-68 de S2 ; Q-C-14) n'est comparé à aucun contexte du recalcul | orch. | G0 de RB-2 | un test d'égalité des champs du contexte côté recalcul ; ≈ 15 lignes [inféré] | I-5 du générateur de P2A |
| SHOGEN-S2BIS-DECODEURS-TYPES-1 | les décodeurs repris de S2 ne contrôlent pas le type des conteneurs : Kraken `c` en chaîne rend son premier caractère comme prix (« 6 »), comme S2 (G2, S-07) | orch. | G0 de CB-7 | un contrôle de type par décodeur (liste ou objet attendu), écart à S2 nommé au §9.1, un test par décodeur ; ≈ 30 lignes [inféré] | O-1 de la G2 de P2A |
| SHOGEN-S2BIS-CANONIQUE-OCTETS-1 | `journal.canonique` borne le nombre de valeurs (LIMITE), pas les octets : une longue chaîne partagée k fois s'écrit k fois avant le contrôle de taille ; le §8.4 dit « en temps borné » sans écrire la borne ; aucun chemin du collecteur ne bâtit un tel enregistrement | orch. | G2 de clôture de P2 | une phrase au §8.4 (borne écrite : linéaire en valeurs comptées et en longueur des chaînes), ou un compte d'octets par occurrence et un test ; ≈ 15 lignes [inféré] | O-4 de la G2 de P2A |
| SHOGEN-S2BIS-SECONDAIRE-CONFORMITE-1 | aucun test de conformité de bout en bout du journal `secondaire` (préfixe, `releve_asn`, `asn`, lectures de la carte) contre le FORMAT §15, comme `test_bout_en_bout` le fait pour le pool (E-C-24) | orch. | avant la G2 de clôture de P2 | un test de bout en bout ; ≈ 80 lignes [inféré] | O-5 de la G2 de P2A |
| SHOGEN-S2BIS-ASN-HOTE-IPV4-1 | un hôte écrit en IPv4 littérale, admis par `hote-forme` (§14.1, `[a-z0-9.-]{1,253}`), n'est jamais relevé : la requête A de ce nom ne rend pas d'adresse, `ip`, `ripestat` et `cymru` restent nuls (G2) ; le §15.4 ne le dit pas | orch. | G0 de la carte (SHOGEN-S2BIS-CARTE-AVEUGLE-1), au plus tard avant le gel | une règle (IPv4 littérale relevée directement, ou refusée par `hote-forme`), une phrase au §15.4 et un test [inféré] | O-6 de la G2 de P2A |
| SHOGEN-S2BIS-R25-COMPTE-1 | la convention de compte de R-25 n'est pas écrite : les lots de S2-bis comptent « lignes de code ajoutées » sur `.py` et `.yml` ; CB-6a compte 200 lignes de code, plus 8 fixtures copiées d'une ligne (`.bin`) et sa documentation, hors compte | orch. | avant la tranche B recalée de P2 | une phrase de convention (brief ou en-tête de METRIQUES) ; 1 ligne [inféré] | O-7 de la G2 de P2A |

Précision d'un item existant : **SHOGEN-S2BIS-NOMS-HOTE-RFC1123-1** (O-3 de la G2 de P2A). La règle `budget-partage`
(E-C-33, FORMAT §15.2) compte par nom d'hôte écrit : `a.example.` (point final) et `127.000.000.001` passent
`hote-forme` comme des hôtes distincts de `a.example` et de `127.0.0.1`, et contournent le budget (G2, L-S2 :
10 lectures par fenêtre sur un même hôte). L'écriture canonique des hôtes (sans point final ; IPv4 littérale refusée,
ou canonique comme au §12) se pose avec la structure en étiquettes, avant le gel des identifiants.

Non formé : SHOGEN-S2BIS-ISO-CASSE-1 (I-1). C-5 écrit la restriction et sa raison au FORMAT §9.1 (diff CB-6c), avec un
test (`test_format.Format.test_paragraphes_9_et_14_valeurs_et_decodeur`). C-4 est fait dans le lot (CB-13a, 133 lignes
de code) : aucun item.

Questions adjugées, consignées : Q-1 (cinq lectures par hôte et par fenêtre, pool et carte ensemble, règle scellée au
FORMAT §15.2) ; Q-3 (aucun repli TCP pour D-4 et D-5, FORMAT §12 ; ASN : SHOGEN-S2BIS-ASN-TRONCATURE-1). Écarts E-2
à E-7 admis par l'adjudication. O-1 du G1 (mutant « lecture de la carte dans la boucle du pool » remplacé par le test
de processus `test_secondaire.Isolement`) : admis par la G2, porté ici au rapport court.

### Écarts de la passe de corrections

- E-9 : l'outil `outils/corr_6b.py` porte 100 octets 92. Ce sont des guillemets échappés dans les gabarits Python qui
  écrivent le code et les tests de 6b. Contrôle sur les octets écrits : la série n'ajoute aucun octet 92
  (`forme-diffs.txt`).
  Quatre sondes de cette reprise portaient aussi des barres tapées : guillemets échappés dans une mesure
  `python -c`, `[` échappé dans deux `grep` de repérage, et le caractère nul d'un `tr` de relevé des processus.
  Aucun fichier n'a été écrit par elles. Leurs résultats ont été recoupés : `panne_decode` partout ; une occurrence de
  chaque ancre de mutant, confirmée par l'application de MC1-09 et MC1-10. Une cinquième commande, l'édition de ce
  paragraphe par un script Python, portait deux sauts de ligne échappés ; contrôle sur les octets écrits : 0 octet 92
  dans ce rapport, le G1 et les NOTES.
- E-10 : `outils/mutants.py` tronque à quatre noms la liste des échecs qu'il affiche. Sous MC1-01 à MC1-04,
  `test_okx_ts` n'y figure pas ; il échoue pourtant aussi, ce qui a été sondé à part (NOTES).
- E-11 : les campagnes des sous-lots de la chaîne 1 (22:36 à 23:28 UTC) ont tourné avant la mise à jour de METRIQUES
  (6a à 13b) et du FORMAT de 13b (Q-1, Q-3), faite de 23:14 à 23:17 UTC. Ce sont des documents qu'aucune suite ne lit,
  sauf `test_format` pour le FORMAT de 13b. Ensuite, la chaîne 2 a rejoué :
  - les huit états ;
  - les campagnes de 13b (lot et correction) ;
  - les 26 mutants du réviseur ;
  - la matrice et xtask.
- E-12 : la campagne d'un autre worker (sb11) tournait sur la machine pendant les chaînes 1 et 2. Les durées
  relevées sont donc prises sous charge. Le pire décodage hostile de C-1 vaut 14,6 ms sous cette charge, pour un
  seuil de 0,1 s dans le test.
- Reprises : deux agents se sont arrêtés en cours de route. Les deux chaînes détachées (PID 12868, puis 30866) ont
  fini sans coupure (lignes « fin » de `campagnes.log` et de `campagnes-2.log`) ; rien n'est à refaire.

### Fichiers

Diffs : `diffs/CB-6a.diff` … `diffs/CB-13b.diff`. Preuves : `preuves/C-1/`, `C-2/`, `C-4/`, `C-5/` et
`preuves/corrections/` (états, mutants, matrice, tête, xtask, forme, METRIQUES). Outils : `outils/` (dont
`mutants_corr.py`, `mutants_g2_rejoues.py`, `campagnes_g2.sh`, `campagnes_g2b.sh`). `SHA256SUMS` est recalculé et couvre
ce rapport. Les copies lourdes (états, mutants, travail, cible cargo, tmp) sont supprimées.
