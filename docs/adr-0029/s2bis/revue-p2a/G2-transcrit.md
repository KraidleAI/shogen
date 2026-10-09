# Relecture G2 de P2A (transcrit)

> Transcription par l'orchestrateur le 2026-10-09 06:28:34 UTC du fichier g2/RAPPORT-G2.md ; contrôle FM-1.1 des quatorze transcripts d'agents qui ont touché `s2bis/p2a` ou `s2bis/p2b` : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Relecture G2 neuve du lot P2A (S2-bis, partie P2, tranche A : CB-6, CB-12, CB-13)

**Gate 0 : `claude-opus-5-5`** (identifiant exact du modèle qui tourne ; fiche `shogen-worker`, effort max). Réviseur
neuf : je n'ai écrit aucun des diffs relus. Rapport du 2026-10-08, 21:51 UTC (`date -u`).

## Verdict : ACCEPTE-AVEC-CORRECTIONS (liste fermée C-1 à C-3)

La série est saine sur l'essentiel :
- les huit diffs s'appliquent, sur 5cfe746 comme sur la tête réelle eb83db6 ;
- planchers exacts à chaque état ; runner, s2bis, S2 et sim-bis conformes ;
- six items de l'annexe B fermés, chacun par un test dont j'ai reproduit le rouge sur le code d'avant ;
- égalité exacte avec S2 sur les onze fixtures ;
- isolement par processus tenu.

Trois corrections sont dues avant le commit :

| n° | gravité | objet |
|---|---|---|
| C-1 | bloquante | un horodatage en nombre JSON à grand exposant tient le GIL dans le décodeur et fait manquer l'échéance du collecteur |
| C-2 | tests | six bornes codées et écrites ne sont figées par aucun test (6 mutants vivants sur mes 26) |
| C-3 | document | les « formes BTC » demandées par le brief et la PROPOSITION ne sont ni versées ni déclarées |

## 1. Base, intégrité, méthode

- **SHA256SUMS du générateur** : `sha256sum -c` donne 152 OK et 0 échec. Le sha256 du fichier vaut
  `61476b6c2033463c0bcc5102285b5f76157c49c07e83c0db2fa86139ca987fb5`, égal à l'annonce. Tous les fichiers présents
  sont couverts (le fichier lui-même excepté).
- **Base** : `git --no-optional-locks archive` de 5cfe746 avec les sept exclusions du brief (vérifiées absentes).
  - La tête réelle est `eb83db6` à 20:46 UTC.
  - Sur les chemins de la série, seule la ligne sim-bis de `gates.yml` y diffère (172 → 194).
- **États** : `etats/0` à `etats/13b` par `patch -p1` cumulatif (code 0 pour les huit diffs). Les 34 fichiers touchés
  sont ceux que la série déclare.
- **Sonde du réviseur** : `sonde/attentes.py` (19 attentes S-01 à S-19, d'après le contrat seul). Son sha256
  `9197a7bb…cc5ed` a été consigné aux NOTES à 20:53 UTC, avant toute lecture des diffs, et n'a pas changé depuis.
- **Lecture** : j'ai lu les huit diffs en entier avant le rapport, le G1 et les NOTES du générateur.
- **Exécution** : réseau isolé (`unshare -n`, lo seule), `SHOGEN_S2_CAMPAGNE_CONTROL` retirée, `-X dev -W error`
  (`PYTHONDEVMODE=1` et `PYTHONWARNINGS=error` pour les enfants), TMPDIR dédié.

## 2. Exigences et items : où, et quel test les fige

Lignes à l'état final (`etats/13b`).

| exigence ou item | fichier:ligne | test qui le fige | constat |
|---|---|---|---|
| E-C-06 : BTC repris, fixtures, finitude | `collecte/decodeurs.py:82-95` (DECODEURS), `:104` (prix fini, > 0, exposant), `:106` (instant de 0 à 2^53) ; `tests/fixtures/btc/` (11) | `test_decodeurs.Reprise.test_fixtures_copiees_octet_pour_octet`, `…test_memes_valeurs_que_expected_json_de_s2`, `Finitude.test_prix_non_fini_nul_negatif_ou_flottant_panne` | tenu ; les 11 sha256 sont égaux à ceux de S2 (mesuré) ; voir C-1 et C-2 |
| E-C-07 : contexte nommé (Q-C-14) | `decodeurs.py:24-25`, `:114` | `Finitude.test_contexte_nomme_jamais_celui_du_fil` | tenu ; mon mutant G07 est tué |
| E-C-08 : devise et classe | `decodeurs.py:83-94` | `Reprise.test_memes_valeurs_que_expected_json_de_s2` | tenu ; G26 tué |
| FORMAT l.310 `valeurs`, E-C-17 | `decodeurs.py:111-130`, `entree.py:136` ; FORMAT §9.1, §14.1 | `Politique.test_lecture_decodee_panne_http_inchangee`, `test_entree.…test_lecture_decodee_par_le_decodeur_de_sa_forme`, `test_bout_en_bout` (relevé contrôlé contre le §9.1) | tenu |
| SHOGEN-S2BIS-ECRIVAIN-REFUS-ARRET-1 (décodeurs) | `decodeurs.py:118` (`canonique` et borne VALEURS) | `test_decodeurs.Politique.test_valeurs_refusees_par_l_ecrivain_jamais_rendues` (l.149), `…test_boucle_continue_quand_un_decodeur_rend_une_valeur_refusee` | fermé ; rouge reproduit sur le code de 6b ; mon leurre « confidence » en expansion (7 Mo) donne `panne_decode` en 0,27 s |
| SHOGEN-S2BIS-TARDIVES-BORNE-1 | `collecte/boucle.py:130-136` (résultat, puis place) | `test_boucle.Boucle.test_resultat_rendu_avant_la_place` (l.307) | fermé ; rouge reproduit sur 6c (`[False, False]`) |
| SHOGEN-S2BIS-ECRIVAIN-IMBRICATION-OCTETS-1 | `collecte/journal.py:92-103`, `:335-337` | `test_reprise.Reprise.test_niveaux_comptes_sur_les_octets_avant_le_decodeur` (l.128), `test_fitness.Fitness.test_copie_du_compte_des_niveaux` | fermé ; rouge reproduit ; G10 tué |
| SHOGEN-S2BIS-CORPS-BORNE-1, volet graphe | `journal.py:83` (valeurs comptées par occurrence), `:126` (refus) | `test_journal.Ecrivain.test_graphe_partage_refuse_en_temps_borne` (l.213) | fermé ; rouge reproduit ; G11 tué ; observation O-4 |
| SHOGEN-S2BIS-DNS-TC-1 | `collecte/dns.py:88-89` | `test_dns.Interroger.test_drapeau_tc_garde_section_reponse_non_lue` (l.228) | fermé ; mon leurre ne voit aucune socket TCP créée ; G13 et G25 tués ; Q-3 |
| SHOGEN-S2BIS-DNS-ID-16BITS-1 | `dns.py:32-33` | `test_dns.Interroger.test_identifiant_hors_de_16_bits_refus_nomme` (l.246) | fermé ; rouge reproduit ; 65536, -1, True, 2^70, 1.5 et « 1 » donnent `forme` ; G12 tué |
| E-C-11, E-C-12 : échéance dure | décodage dans le fil de lecture : `entree.py:136` | aucun | **cassé par C-1** |
| E-C-30 : relevé ASN | `collecte/asn.py:53-68`, `secondaire.py:24-42`, `entree.py:40-41` | `test_asn.*` (5), `test_secondaire.Secondaire.*` | tenu ; Q-2 (rattrapage) ; C-2 (G14, G17, G20) |
| E-C-31 : hors du fil qui écrit | `secondaire.py:27-42` | `Secondaire.test_releve_hors_du_fil_qui_ecrit_jamais_relance_en_double` | tenu ; G18, G19 et G24 tués |
| E-C-32 : processus distinct, départ, hors δ | `entree.py:99-100`, `:149-158` | `Configuration.test_construction_journal_propre_hors_delta_sans_sondes`, `Isolement.test_carte_pendue_ou_refusee_le_pool_intact` | tenu ; G22 et G23 tués |
| E-C-33 : budget de débit partagé | `entree.py:96-98` | `Configuration.test_carte_budget_partage_et_regles_croisees` | tenu sur les noms écrits ; G21 tué ; contournable par alias (O-3) |
| Brief l.6 et PROPOSITION l.214 : « formes BTC » | absentes | aucun | **C-3** |

## 3. Sonde du réviseur contre le lot

| attente | résultat |
|---|---|
| S-01 fixtures octet pour octet | OK (11 sha256 égaux) |
| S-02 égalité exacte avec S2 | OK (prix ; instants exacts en µs ; extras) |
| S-03 non fini, nul, négatif | OK (29 prix hostiles × 10 décodeurs) |
| S-04 aucun flottant | OK |
| S-05 corps hostiles | OK (préfixes ; 1 Mio profond ; 1 Mio de chiffres ; blancs) |
| S-06 exposants | **ÉCHEC : C-1** |
| S-07 types croisés | OK, sauf Kraken `c` en chaîne, qui donne le prix « 6 » comme S2 (O-1) |
| S-08 nombre à virgule | OK, texte du Decimal |
| S-09 champs manquants | OK (84 variantes : S2 et S2-bis concordent) |
| S-10 politique de l'écrivain | OK |
| S-11 contexte nommé | OK |
| S-12 `decodeur` des formes | OK |
| S-13 tardives | OK |
| S-14 niveaux sur les octets | OK |
| S-15 graphe partagé | OK (O-4) |
| S-16 TC | OK (Q-3) |
| S-17 identifiant | OK |
| S-18 relevé ASN | OK (O-2 ; C-2) |
| S-19 processus secondaire | OK pour le journal propre, la reprise, l'isolement et la règle de budget ; relevé en vol perdu à l'arrêt (Q-2) ; alias (O-3) |

## 4. Leurres du réviseur (tous en réseau isolé ; sorties sous `preuves/leurres/`)

| leurre | mesure | constat |
|---|---|---|
| L-D1 fixtures S2 | 11 sur 11 égaux à S2, instants exacts | OK |
| L-D2 préfixes tronqués | 2 120 préfixes ; S2-bis n'est jamais `ok` là où S2 diffère | OK |
| L-D3 prix hostiles | NaN et Infinity littéraux, « sNaN », « -inf », 0, -0, négatifs, types croisés, 1E±1000000 | OK |
| L-D4 horodatages (6 champs) | texte « 1e999999999 », 22 ou 5 000 chiffres, -1 : `panne_decode` en moins de 1 ms ; nombre JSON 1E+300000 : `panne_decode` en 1,0 à 2,0 s (3.10, 3.12, 3.13) | **ÉCART (C-1)** |
| exposant croissant (`exposant-3.12.txt`) | corps de 50 octets : 1E+1000000 en 10,4 s, 1E+2000000 en 41,1 s, 1E+3000000 en 94,6 s | quadratique |
| GIL (`gil-3.12.txt`) | décodage de 10,66 s ; le fil principal ne se réveille qu'une fois en 10,66 s | GIL tenu |
| L-D8 échéance (`echeance-3.12.txt`) | point d'entrée réel `pool`, w = 1 s : avec le corps témoin, marqueurs à E − 0,30 s ; avec le corps hostile, marqueurs à E + 10,45 à + 10,68 s, lectures écrites en `panne_transport:delai` (pas `panne_decode`), `trou` de 10 fenêtres (cause `saut`) | **C-1** |
| L-D5 DefiLlama `confidence` | `[1] × 524 188` (1 Mio), soit 7 Mo une fois passé par `str()` : `panne_decode` en 0,27 s | OK |
| L-D9 champs retirés | 84 variantes, 0 écart S2 / S2-bis | OK |
| L-A1 RIPEstat hostile (18 corps) | aucune exception ; `panne_decode` typé ; enregistrement borné | OK ; O-2 (« 13_335 », chiffres arabes-indiens, « -0 » admis) |
| L-A2 TXT de Cymru (14) | bornes 0 à 2^32 - 1 tenues | OK ; « +13335 » et « 1_3335 » admis (O-2) |
| L-A3 DNS hostile (TC, muet, autre identifiant, TXT, A de 5 octets, rcode 15, CNAME puis A, 513 octets) | aucune socket TCP ; 0,5 s au plus ; adresse seulement sur un A | OK |
| L-A4 identifiants hors 16 bits | `forme` | OK |
| L-A5 RIPEstat au goutte-à-goutte | `panne_transport:delai` en 0,50 s | OK |
| L-S1 pool et secondaire dans le même dossier, puis secondaire relancé | sorties 0 ; chaînes intactes (code indépendant) ; une `reprise` ; verrous distincts ; `asn` : A ok, ip 192.0.2.1, Cymru 64500, RIPEstat `panne_transport:dns` | OK ; le relevé lancé à la dernière fenêtre avant l'arrêt n'est jamais écrit (Q-2) |
| L-S2 budget par alias | `a.example.` et `127.000.000.001` admis : 10 lectures par fenêtre sur un même hôte | O-3 |

## 5. Mutants du réviseur

26 mutants, classés par la commande du job : runner puis ligne s2bis de `gates.yml` de la copie mutée, borne de 300 s,
python3.12. Bilan : **20 tués, 6 vivants, 0 FATAL** (`preuves/mutants/campagne.txt` ; outil `outils/mutants_g2.py`).

Tués, chacun par un test qui vise la règle mutée :

| mutant | règle mutée |
|---|---|
| G04 | 2^53 admis |
| G05 | prix nul admis |
| G06 | garde et borne retirées |
| G07 | contexte du fil |
| G08 | Kraken à plusieurs clés |
| G09 | `confidence` perdue |
| G10 | RecursionError prise pour un verdict |
| G11 | borne du graphe décuplée |
| G12 | identifiant booléen admis |
| G13 | TC ignoré quand des réponses suivent |
| G15 | AS flottant admis |
| G16 | RIPEstat interrogé sur le nom |
| G18 | un seul `asn` par fenêtre |
| G19 | relevé jamais relancé |
| G21 | `espace-partage` retirée |
| G22 | `marge-carte` relâchée |
| G23 | marge de la carte prise au pool |
| G24 | premier hôte seul |
| G25 | `reponses` vides sous TC |
| G26 | devise d'OKX ticker |

**Vivants** (aucun test ne fige ces bornes ; C-2) :

| mutant | substitution | fichier:ligne |
|---|---|---|
| G01 | résultat Chainlink de plus de cinq mots admis (`{320,}`) | `decodeurs.py:31` |
| G02 | int256 : 2^255 lu positif (`>` au lieu de `>=`) | `decodeurs.py:78` |
| G03 | signe du décalage ISO ignoré | `decodeurs.py:40` |
| G14 | AS 0 refusé (le FORMAT §15.4 l'admet : « de 0 à 2³² exclu ») | `asn.py:24` |
| G17 | dernière chaîne du TXT au lieu de la première (FORMAT §15.4) | `asn.py:47` |
| G20 | `periode` de 172 800 s admise (E-C-30 : « au moins quotidien », FORMAT §15.2) | `entree.py:41` |

## 6. Jobs, matrice, xtask, forme

| contrôle | résultat |
|---|---|
| chaque état, python3.12 (`preuves/etats/`) | runner 136 ok ; s2bis conforme à Ran = plancher : 255 (base), 263, 265, 271, 276, 279, 284, 287, 291 |
| état final, 3.10.20 / 3.11.15 / 3.12.3 / 3.13.14 (`preuves/matrice/`) | runner 136 ok ; s2bis 291 ; sim-bis 172 ; S2 415 conforme sous 3.11 à 3.13 |
| S2 sous 3.10 | rouge (77 échecs, 3 erreurs), avec des lignes FAIL et ERROR identiques sur la base (`preuves/etats/0-s2-3.10.txt`) : SHOGEN-S2-PY310-1, préexistant |
| lignes « Exception ignored » ou « Warning » | aucune, dans aucune sortie |
| série sur eb83db6 (`preuves/tete/`) | `patch -p1` à 0 ; runner 136 ; s2bis 291 ; sim-bis 194 ; S2 415, conformes sous 3.12 |
| `cargo --locked xtask verify`, état final et base (`preuves/xtask/`) | S-G1 à S-G8 VERT, fmt VERT, no_std VERT, clippy VERT ; S-G9 ROUGE `docs/17-modele-de-menace.md:70` sur les deux (connu des copies) |
| METRIQUES | lignes et nombre de tests de chaque fichier recomptés à chaque état : tout égal |
| code ajouté (.py et .yml) | 200 / 59 / 145 / 124 / 61 / 196 / 115 / 199, soit 387 de production, 704 de tests et 8 de `gates.yml` |
| octets 92 ajoutés, R-13, fins blanches, tabulations | 0 |
| lignes de plus de 120 caractères | dans les lignes de tableau .md seulement (usage établi) |
| R-8 | bibliothèque standard seule (`test_fitness`) |
| `__pycache__` | aucun dans les racines de suite |

## 7. Corrections (liste fermée)

### C-1 : un horodatage à grand exposant tient le GIL et casse l'échéance (E-C-11, E-C-12 ; leurre « exposants »)

**Où.** `s2bis/shogen_s2bis/collecte/decodeurs.py:51` (`int(d["ts"])`, OKX), `:70` (DefiLlama), `:88` (Bitstamp),
`:89` (Gemini) et `:91` (CoinGecko). Les nombres JSON y sont lus en Decimal (`:116-117`), puis `int()` les convertit.
Le décodage tourne dans le fil de lecture (`entree.py:136`).

**Preuve.**
- `int(Decimal("1E+N"))` est quadratique en N et ne rend pas le GIL. Mesures sur un corps de 50 octets : 10,4 s
  (N = 10^6), 41,1 s (2·10^6), 94,6 s (3·10^6).
- Point d'entrée réel `pool`, w = 1 s : chaque marqueur est écrit 10,45 à 10,68 s après son échéance ; la lecture est
  écrite `panne_transport:delai` au lieu de `panne_decode` ; des trous de 10 fenêtres suivent.
- En production (w = 60 s), un exposant de 3·10^6 tient le processus plus d'une fenêtre. Toute lecture en vol passe
  son délai de 10 s : l'observateur vote alors « panne » pour toutes ses unités (ADR-0029 §2.2 pt 8 (b)).
- Une source servie aux quatre observateurs les atteint tous.
- Aucun test du lot ne porte un exposant sur un horodatage. Celui du prix (`'"1E+1000000"'`) est refusé par la borne
  d'exposant et ne passe pas par `int()`.

**Remède.**
1. Borner avant la conversion, par une aide unique appelée aux cinq sites : refus si
   `type(x) is Decimal and x.is_finite() and x.adjusted() > 20`, sinon `int(x)`. C'est le `int()` de S2 pour toute
   valeur réaliste.
2. Ajouter un test par champ d'horodatage : nombre JSON `1E+1000000`, puis entier de 10^6 chiffres ; attendu
   `panne_decode` en moins de 0,1 s.
3. Ajouter le mutant « borne retirée », qui doit être tué.

**Prototype du réviseur, pièce et non livrable** (`preuves/leurres/remede-C1-prototype.diff`) :
- marqueurs de nouveau à E − 0,30 s, lectures `panne_decode` ;
- valeurs témoins inchangées ;
- suite s2bis 291 conforme (`echeance-proto-3.12.txt`, `proto-s2bis-3.12.txt`).

### C-2 : six bornes codées et écrites sans test (mutants vivants G01, G02, G03, G14, G17, G20)

**Où.** Ce sont les lignes du tableau du §5 : `decodeurs.py:31`, `:78`, `:40` ; `asn.py:24`, `:47` ; `entree.py:41`.

**Preuve.** `preuves/mutants/campagne.txt` : la suite reste conforme (Ran = 291) sous chacun des six mutants.

**Remède.** Un cas de test par borne, valeur écrite à la main, puis rejouer les six mutants, qui doivent être tués :

| borne | cas attendu |
|---|---|
| Chainlink | résultat de six mots : `panne_decode` (S2 : `len(h) != 5*64`) |
| int256 | réponse exactement 2^255 : `panne_decode` (négatif) |
| décalage ISO | « …T11:11:21-05:00 » : 1785946281 s en µs |
| AS | `asn` 0 (RIPEstat) et TXT « 0 &#124; x » : 0 admis, selon le FORMAT §15.4 |
| TXT | deux chaînes « 64500 &#124; x », « 64501 &#124; y » : 64500 |
| cadence | `periode` 86 401 : `CONFIG/borne` |

### C-3 : « formes BTC » ni versées ni déclarées (brief l.6 ; PROPOSITION l.214)

**Preuve.**
- Aucun diff n'ajoute de forme de requête BTC : aucune donnée sous `s2bis/config/` ; les requêtes de S2 viennent de
  `sources.py` (SPECS l.239-283).
- Ni le rapport, ni le G1, ni les NOTES du générateur ne nomment ce livrable (recherche dans ces seuls fichiers).

**Remède (document).**
- Déclarer l'écart au rapport, au G1 et dans la section METRIQUES de CB-6c.
- Le rattacher par une ligne à un item : soit SHOGEN-S2BIS-CONFIG-PRODUCTION-1 (déclencheur : gel), soit un item neuf
  proposé, SHOGEN-S2BIS-FORMES-BTC-1, déclencheur CB-8.

**Avis.** Verser les formes avec CB-8 :
- CoinGecko, DefiLlama et Bitfinex y deviennent regroupées (E-C-09), et le plan d'OKX y change (cinq lectures) ;
- le test devra comparer chaque forme gardée aux octets de la requête de S2 (E-C-09 : « requête BTC de S2 gardée »).

## 8. Écarts du lot, observations, avis sur les questions du générateur

### Écarts déclarés par le générateur

- Je les admets : E-2 (§15 du FORMAT versé avec CB-13b seulement), E-3 (METRIQUES et docstrings après les campagnes ;
  ma campagne a tourné sur l'état final), E-4 (rouges partiels), E-5 et E-7 (S2 sous 3.10, préexistant).
- O-1 du G1 (mutant obligatoire « lecture de la carte dans la boucle du pool » remplacé par le test de processus
  `Isolement`) : admis. Il manque toutefois au rapport court ; à y porter.

### Observations (sans correction ; à former en items, règle PAROXYSME)

- **O-1** : Kraken `c` en chaîne rend son premier caractère comme prix (« 6 »), comme S2. Le type des conteneurs n'est
  pas contrôlé. Item proposé : SHOGEN-S2BIS-DECODEURS-TYPES-1, déclencheur G0 de CB-7.
- **O-2** : l'ASN est lu par `int()` de S2, qui admet le souligné, le signe, les blancs et les chiffres
  arabes-indiens. C'est écrit au FORMAT §15.4 ; à trancher avec SHOGEN-S2BIS-RIPESTAT-FIXTURE-1.
- **O-3** : `budget-partage` compte par nom écrit. `a.example.` et `127.000.000.001` le contournent (mesuré). À
  verser à SHOGEN-S2BIS-NOMS-HOTE-RFC1123-1 (avant le gel des identifiants) : écriture canonique des hôtes.
- **O-4** : `canonique` borne le nombre de valeurs, pas les octets. Une longue chaîne partagée k fois s'écrit k fois
  avant le contrôle de taille. Aucun chemin du collecteur ne bâtit un tel enregistrement ; préciser « en temps borné »
  au §8.4.
- **O-5** : aucun test de conformité de bout en bout du journal `secondaire` contre le FORMAT §15 (E-C-24 pour le
  pool). Item proposé : SHOGEN-S2BIS-SECONDAIRE-CONFORMITE-1, avant la G2 de clôture de P2.
- **O-6** : un hôte écrit en IPv4 littérale (admis par `hote-forme`) n'est jamais relevé : sa requête A ne rend rien.
  À noter au §15.4.
- **O-7** (R-25) : CB-6a compte 200 lignes de code, plus 8 lignes de fixtures copiées. C'est conforme à la lettre du
  brief (« lignes de code ») ; la convention est à confirmer par l'orchestrateur.

### Avis sur les questions du générateur

- **Q-1 (budget)** : adopter la règle comme plafond scellé. Le G0 de la carte (CARTE-AVEUGLE-1) la serre hôte par hôte,
  sur les limites lues ; O-3 en plus.
- **Q-2 (rattrapage)** : rattraper. E-C-30 et ADR-0029 l.247 disent « quotidien », et la stabilité de R2 se compte en
  jours. Mon leurre montre aussi qu'un relevé en vol à l'arrêt est perdu. Règle proposée, sans relecture du journal
  (E-C-15) : un relevé à la première fenêtre de chaque exécution, et un rattrapage en mémoire si un instant de la
  cadence est sauté. À faire avant le gel (item), si ce n'est pas fait en P2.
- **Q-3 (TC sans TCP)** : pas de repli pour D-4 et D-5, comme admis. Pour le relevé ASN, hors échéance et dans le
  processus secondaire, le repli TCP est la règle (RFC 2181 §9, RFC 7766 [2nd]). Avis : mesurer le taux de TC au
  rodage (lecture « ASN » de classe M) et adjuger avant le gel ; item à former.
- **I-1 (ISO-CASSE-1)** : d'accord. La stricture est défendable (même lecture de 3.10 à 3.13), mais c'est un écart à
  S2 à écrire au §9.1.
- **I-2, I-3** : d'accord.
- **I-4** : vérifié. La règle codée de `test_fitness` refuse `recalc` → `collecte.decodeurs` (« plus serrée que
  PROPOSITION §1 pt 2 »). Une copie gardée égale sera nécessaire, ou un amendement à RB-2.
- **I-5** : d'accord.

## 9. Journal de provenance (G1)

**Sources [lu]** :
- brief P2A, entier ;
- G0 COLLECTE-RECALC-DEPLOI, entier ; AVIS, entier ; PROPOSITION l.1-449, puis par recherche CB-6, CB-12, CB-13 et
  P2 dans ce seul fichier ;
- ADR-0029 à e16956b (`git show`) : l.76-116, l.164-173, l.229-260 ;
- FORMAT, entier, base et final ;
- annexe B : recherche des déclencheurs CB-6, CB-12, CB-13 et « G2 de P2 » dans ce seul fichier ; l.1009-1012,
  l.1053-1057, l.1085, l.1110-1112, l.1150-1200, l.1222-1236 ;
- `s2-harness/shogen_s2/sources.py` l.1-402 ; `r2.py` l.240-405 ; `r1.py` l.50-75 ; `model.py` l.1-40 ;
  `tests/test_sources.py` ; `expected.json` ; `test_prix_non_fini.py` l.1-80 ;
- `docs/10-mesures-pilotes-design.md` l.200-216 ;
- `s2bis/` : collecte en entier (base et final), `recalc/lecteur.py` l.20-75, `test_fitness.py` l.1-80, les tests
  touchés par les diffs, `tests/__init__.py`, aides de `test_boucle` ;
- `enforcement/verdict-suite-s2.py` l.1-80 ; `gates.yml` l.146-250 ; `scripts/sim-bis/oracle_r1.py` l.30-60.

**[2nd]** : RFC 2181 §9 et RFC 7766 (connaissance du modèle, non relues ; avis Q-3 seulement). **[abs]** : aucune
pièce de D.2, aucun `*.jsonl`, aucun dossier interdit ouvert.

**Commandes et sorties** : sous `preuves/` (états, matrice, mutants, leurres, xtask, tête), chacune avec son code de
sortie et sa durée.

**Chiffres recomptés** :
- 152 OK au SHA256SUMS ;
- 34 fichiers touchés ;
- 1 099 lignes de code ajoutées (387 / 704 / 8) ;
- planchers 263 à 291 ;
- METRIQUES égales ;
- 26 mutants (20 / 6 / 0) ;
- fixtures : 11 sha256 égaux ;
- S2 sous 3.10 : 80 lignes FAIL et ERROR identiques sur la base.

**Écart du réviseur.** Trois de mes premiers scripts portaient des barres obliques ou des fichiers non fermés : un
regex d'outil, des sauts de ligne échappés et une séquence d'échappement unicode. Je les ai réécrits par `chr(92)` et
`chr(10)`, en classes `[(]`, ou avec `with`. Contrôle sur les octets écrits : 0 octet 92 dans `outils/` et `leurres/`,
et `sonde/attentes.py` en porte 6, tous des guillemets échappés (barre puis guillemet) de sa l.45, voulus, écrits par
l'outil d'écriture et contrôlés sur les octets (fichier figé par son sha256 avant la lecture des diffs). Le premier
passage des leurres des décodeurs a été refait après correction des fichiers non fermés (`ResourceWarning`).

## 10. Fichiers produits

Sous `<scratchpad>/s2bis/p2a/g2/` : `RAPPORT-G2.md`,
`NOTES.md`, `sonde/`, `leurres/`, `outils/`, `preuves/`, ainsi que `SHA256SUMS`, qui couvre tous ces fichiers.

Les copies lourdes sont supprimées en fin de relecture : base, états, prototype, tête, cible cargo, mutants, tmp.

Le sha256 du fichier `SHA256SUMS` est donné dans le message de rendu : il couvre ce rapport.
