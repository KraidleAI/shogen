# Relecture G2 neuve de DETTES-T6 (transcrit)

> Transcription par l'orchestrateur le 2026-10-10 09:08:09 UTC du fichier g2/RAPPORT-G2.md ; contrôle FM-1.1 des transcripts du générateur-correcteur, du réviseur G2 et du contre-contrôleur, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# RAPPORT-G2 — relecture G2 neuve du lot DETTES-T6 (collecteur P2 de S2-bis : robustesse et tests, 16 items)

- **Rôle** : réviseur G2 (fiche `shogen-worker`), n'a rien écrit du lot. **Gate 0** : modèle résolu `claude-opus-5-5`
  (identifiant exact de l'invite système). Effort : `high` (brief ; même écart à la fiche que l'E-0 du générateur,
  admis par l'adjudication, décision de l'investisseur du 2026-10-08).
- **Heures** (`date -u`) : ouverture 2026-10-10 00:27:56 UTC ; rendu : voir §10.
- **Objet relu à 100 %** : série `diffs/DT6-a.diff` à `DT6-j.diff`, dans l'ordre, sur la tête
  `094fa5d3d5debe9dd466e37feee95200ca460dcf` (tête de `claude/compassionate-noether-szmdyj` lue à 00:28 UTC, égale à
  celle du brief) ; empreinte de la concaténation dans l'ordre :
  `491d0e522bedc8c342de864ff3c673d780d3feca3d30bc88114ce57e9ffb0b57` (recalculée : conforme au brief). Sha256 des
  diffs : a `fa5a8270…fe77`, b `5f570543…11d9`, c `76cce28d…7305`, d `0fac5962…43bf`, e `eb4617d0…35e3`, f
  `a89bf783…4526`, g `c643fb8d…9455`, h `04fbb1bd…8429`, i `608e4cba…88b9`, j `09fdc6f6…cade` (SHA256SUMS du lot :
  12 OK).
- **Pas d'enregistrement par `oracle_record.py`** (brief, point 4 : défaut d'extraction en correction au lot DETTES-T7 ;
  le lot ne touche pas le chemin S2) : tête relue `094fa5d3…460dcf`, empreinte relue `491d0e52…b0b57`.
- Dépôt lu seulement (`git --no-optional-locks`), aucune écriture git ; copie creuse `tmp/copie` (clone
  `--no-hardlinks --no-checkout`, sparse non-cone : dossiers interdits et `*.jsonl` exclus, 58 entrées sautées, aucun
  `.jsonl` extrait) ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée ; aucune pièce de D.2 ni dossier interdit ouvert ; aucun
  accès réseau (suites sous `isole.sh`, mandataires retirés) ; au plus deux processus lourds.

## 1. Verdict

**ACCEPTE-AVEC-CORRECTIONS**, liste fermée **C-1 à C-10** (§5). Quinze des seize fermetures sont vraies telles que
proposées ou avec des corrections de test et de texte ; celle de SHOGEN-S2BIS-STATUS-QUEUES-1 ne l'est qu'avec C-1
et C-2 (code) : l'I-3 qu'elle inclut (« `ws` non entier dans une `sante` ») fait encore lever `status` et `resume`
quand `ws` est une liste ou un objet, et la borne de 46 080 fenêtres écrite au §17.3 est passée d'une fenêtre par un
`ws` hors grille. Les trois fermetures de fait sont prouvées. Q-1 à Q-7 : adoptées (§4). Aucune correction n'ajoute
de test (cas ajoutés dans des tests existants) : plancher 357 inchangé.

## 2. Items (16) : la fermeture proposée est-elle vraie ?

| item (SHOGEN-S2BIS-…) | fermeture proposée | jugement | preuves du réviseur |
|---|---|---|---|
| CORPS-BORNE-1 | CB-3, CB-5 (corps) ; CB-6d (graphe) ; DT6-a (cycle) | vraie | l.1047 (corps fermé), l.1165 (graphe à CB-6) lues ; `_parcours` et `canonique` lus : cycle refusé `JOURNAL/type` avant `json.dumps` (test à l'espion qui lève, graphe de 2^40 feuilles) ; suite verte ; A01 du générateur (cycle laissé au sérialiseur) tué |
| CHRONYC-FORMAT-1 | DT6-e (Q-1, Q-6) | vraie, avec C-3, C-4, C-7 | forme relue dans `client.c` 4.6.1 (sha256 recontrôlés) ; fixture = `chronyc.adoc` l.147-159 ; `chrony`, `trois`, `etat` lus ; R05, R06 tués ; R10, R11, R12 vivants (valeurs mal formées de Root delay, Root dispersion, `sortie` non texte : aucune variante) -> C-7 ; ordre des deux sorties inexact au texte -> C-3 ; « à adjuger » au §17.2 -> C-4 |
| DNS-ID-16BITS-1 | CB-12a `af7c3cc` (de fait) | vraie | diff de `af7c3cc` lu (refus nommé, test) ; contrôle présent à l'état final ; W01 (contrôle retiré, struct.error rétabli) tué par `test_identifiant_hors_de_16_bits_refus_nomme` |
| ECRIVAIN-REFUS-ARRET-1 | C-1 de P1-C ; CB-6c `e6edba2` ; DT6-h | vraie | `_run_params` et `main` lus : contrôle avant `construire` et `ouvrir`, refus `CONFIG/…` sortie 2 ; FORMAT §9.1, §13.6, §15.5, §16.5 relus (bornes de taille, §16.5 « toute valeur rendue est admise par l'écrivain ») ; suite verte |
| ECRIVAIN-IMBRICATION-OCTETS-1 | CB-6d `03fcfd4` (de fait) | vraie | diff de `03fcfd4` lu ; `_lire` : `_trop_profonde` avant `json.loads` ; W03 (décodeur avant le compte) tué par deux tests de `test_reprise` |
| TARDIVES-BORNE-1 | CB-6d `03fcfd4` (de fait) | vraie | `boucle._lire` : `set_result` puis `release` dans un `finally` ; W02 (place rendue avant le résultat) tué par `test_resultat_rendu_avant_la_place` |
| ASN-HOTE-IPV4-1 | DT6-f (Q-2) | vraie | `_litterale`, `releve` lus ; §15.4 ; tests du relevé et de `Conformite` (`a` null, `ip` l'hôte) |
| ASN-LECTURE-1 | DT6-f (Q-3) | vraie, avec C-9 | `_asn` lu (`[0-9]` n'admet que l'ASCII) ; R16 tué ; R15 vivant (longueur de 1 à 10 chiffres non figée) -> C-9 |
| CANONIQUE-OCTETS-1 | DT6-a (Q-4) | vraie | `_octets` : borne basse vérifiée à la main (3/10 < log10 2 ; 6 octets au plus par caractère compté 1 ; 24 par nombre à virgule compté 3 : 8 × LIMITE) ; R14 tué |
| DECODEURS-BORNE-TEST-1 | DT6-b | vraie | les cinq sites d'appel de `_entier` (okx, defillama, bitstamp, gemini, coingecko) couverts par les gabarits du test ; docstring exacte (0E+16 : exposant ajusté 16) |
| JOURNAL-FICHIER-SPECIAL-1 | DT6-c | vraie, avec C-8 | `ordinaire`, contrôle par `stat` d'`ouvrir`, `_lire`, `_empreinte`, `_sommes`, `status.enregistrements` lus ; R13 vivant (`O_NONBLOCK` de `_synchro`, ajouté par DT6-c, non éprouvé) -> C-8 |
| STATUS-QUEUES-1 | DT6-d (Q-5) | vraie seulement avec C-1, C-2, C-5, C-6, C-10 | I-3 (« `ws` non entier dans une `sante` ») : `ws` liste ou objet lève encore TypeError dans `status` et `resume` (sonde P1 ; fuzz P4 : 193 traces sur 3 000 journaux, toutes de ce type ; 0 après C-1) -> C-1 ; grille de 46 081 fenêtres admise pour un `ws` hors grille (sonde P2) -> C-2 ; motifs `illisible (<exception>)` et `ligne coupée` d'une ligne de plus de LIMITE non éprouvés (R02, R03 vivants) -> C-5, C-6 ; `ligne coupée` passager pendant la collecte (sonde P5b) -> C-10 ; R01 (grille allouée avant le contrôle) tué |
| ENV-ETAPE-1 | DT6-j (Q-7) | vraie | leurres L-10, L-12, L-19, L-33 relus dans le runner (l.642-655) ; purge des mandataires dans `tests/__init__.py` l.13-14 ; runner 137 ok |
| FORMAT-P2B-TESTS-1 | DT6-i | vraie | 23 phrases du §16 et 23 du §17 recomptées dans le test ; bornes égales au code |
| R25-COMPTE-1 | DT6-a (en-tête de METRIQUES) | vraie | convention lue ; compte recompté (`git apply --numstat`) : a 77, b 26, c 71, d 107, e 144, f 67, g 71, h 47, i 46, j 4 |
| SECONDAIRE-CONFORMITE-1 | DT6-g | vraie | test lu (FORMAT §1 à §14 par `anomalies`, §15 par règles écrites) ; suite verte |

## 3. Fermetures de fait (DNS-ID-16BITS-1, TARDIVES-BORNE-1, IMBRICATION-OCTETS-1)

Prouvées par les commits cités et par des mutants qui rétablissent le défaut de l'annexe B, tués par la commande du
job, sur l'état final de la série : ceux du générateur (V01 à V03, spécification `travail/mutants/dt6v.py`
`9b2c4ea0…1b10` et résultats `sorties/mutants-DT6-V.json` relus) et ceux du réviseur, de formes différentes (W01 à
W03, §7).

| item | commit (lu par `git show`) | défaut de l'annexe B | état final | V (générateur) | W (réviseur) |
|---|---|---|---|---|---|
| DNS-ID-16BITS-1 (l.1057) | `af7c3cc` CB-12a : `requete` refuse un identifiant hors de 16 bits (ValueError nommée), test `test_identifiant_hors_de_16_bits_refus_nomme` | `struct.error` non nommé | contrôle présent, inchangé par la série | V01 (borne retirée) TUÉ | W01 (contrôle retiré entier) TUÉ par le même test |
| TARDIVES-BORNE-1 (l.1158) | `03fcfd4` CB-6d : `boucle._lire` rend le résultat (`set_result`) avant la place (`release`, dans un `finally`) ; test `test_resultat_rendu_avant_la_place` | place libérée avant le résultat | présent | V02 TUÉ | W02 (place rendue dans le `try`, avant le résultat) TUÉ par le même test |
| IMBRICATION-OCTETS-1 (l.1160) | `03fcfd4` CB-6d : `_lire` compte les niveaux sur les octets (`_trop_profonde`) avant `json.loads` ; test `test_niveaux_comptes_sur_les_octets_avant_le_decodeur` | verdict tiré de RecursionError | présent | V03 (compte retiré) TUÉ | W03 (décodeur avant le compte) TUÉ par ce test et `test_queue_imbrication_profonde_et_refus_a_l_ecriture` |

Le volet décodeurs de ECRIVAIN-REFUS-ARRET-1 (`e6edba2` CB-6c) est de même vérifié par V04 (générateur) et par la
lecture de `decodeurs.decoder` et de `test_valeurs_refusees_par_l_ecrivain_jamais_rendues`.

## 4. Questions Q-1 à Q-7 (recommandations codées, adoptées pour la G2) : jugement

- **Q-1 (âge du relevé D-3 en fenêtres ; « Invalid » jugé D-3) : ADOPTÉE.** ADR-0029 l.108 [lu] : « aucun relevé
  chrony de moins de 120 s ; valeur relevée à chaque fenêtre » ; l.239 [lu] : relevé chrony = valeur D-3 de la `sante`
  de chaque fenêtre ; PROPOSITION E-C-25 [lu] nomme « âge du relevé ». La forme (a) mesure l'âge du relevé à la
  grille du journal : la sonde part à ws + w − δ, le relevé de la fenêtre précédente a 60 s à l'instant des lectures,
  celui d'avant 120 s : (a) est la lecture exacte de « moins de 120 s ». La forme (c) (« Ref time », âge de la
  dernière mise à jour de la référence de chrony) mesure une autre grandeur que le relevé que l'ADR nomme ; que la
  dispersion racine en tienne compte est [inféré] (non lu sur pièce) : (c) écartée sur le seul texte de l'ADR.
  « Invalid » (valeur hors des quatre connues, `client.c` %L [lu]) jugé D-3 : serrage, admis (une gate se serre) ;
  l'ADR ne nomme que « Not synchronised » : écart nommé au FORMAT §17.2, à reprendre par RB-3 (L-1). Correction de
  texte liée : C-4 (« à adjuger » périmé).
- **Q-2 (IPv4 littérale relevée directement) : ADOPTÉE.** `hote-forme` (§14.1, `[a-z0-9.-]{1,253}`) admet ces hôtes ;
  (a) relève l'AS de l'adresse que la lecture contacte ; (b) changerait la configuration admise. La comparaison à la
  forme canonique double le refus des zéros de tête et des formes courtes d'`ipaddress` (« 192.0.2.007 » et
  « 127.1 » refusés, mesuré sous 3.10.20 et 3.13.14) : sans effet, sans dommage.
- **Q-3 (numéro d'AS en chiffres ASCII seuls) : ADOPTÉE, avec C-9.** Les deux bases rendent des numéros décimaux
  ASCII ; un texte signé, souligné, blanc ou d'une autre écriture est une donnée altérée ; écart à S2 écrit au §15.4.
  La borne « 1 à 10 chiffres » du texte n'est figée par aucun test (R15 vivant) : C-9.
- **Q-4 (compte d'octets dans le code et phrase au §8.4) : ADOPTÉE.** La phrase seule laissait 1 Gio parvenir au
  sérialiseur ; le compte est pris dans le parcours de CB-6d, linéaire ; borne basse et rapport 8 recontrôlés à la main.
- **Q-5 (grille de `status` bornée à 32 jours) : ADOPTÉE.** Au regard de la rétention de 7 jours : la grille légitime
  compte au plus 9 jours (7 jours retenus, le jour courant, et le jour de reprise avant le premier fichier, plancher
  C-3) ; (b) 8 jours refuserait donc un journal sain. Au regard de la mémoire par les résumés (adjudication de DB-0,
  point 7 [lu] : mémoire = résumés quotidiens clos, exclus de la purge, copiés au dépôt) : `status` n'a pas à couvrir
  plus que la rétention ; 32 jours ne bornent que la grille du journal local, et le volume adopté (DB-0, point 8 :
  environ 23 jours d'autonomie sur 20 Go) rend un tel journal impossible sans saut d'horloge ou fichier forgé. Le
  refus nommé couvre aussi `resume` (même `etat`) : un saut d'horloge suspend la publication des résumés jusqu'au
  geste de l'opérateur ; visible, admis. Précision proposée pour SHOGEN-S2BIS-STATUS-RETENTION-1 (pas d'item neuf) :
  le compte cumulé tiré des résumés ne passe pas par la grille d'`etat` ni par GRILLE ; sa borne est la durée de la
  campagne. Exactitude de la borne : C-2.
- **Q-6 (capture D-3 bornée par le délai de 2 s) : ADOPTÉE.** `subprocess.run` lit au plus ce que la commande écrit
  en 2 s, puis la tue (POSIX : sortie déjà lue gardée dans l'exception) ; commande scellée, locale, 13 lignes ; limite
  écrite au §13.3 ; à reprendre si une sonde non scellée apparaît (déclencheur écrit). Texte de l'ordre des sorties :
  C-3.
- **Q-7 (règle `env` en commentaire de `gates.yml`) : ADOPTÉE.** Le brief du lot borne le code à `s2bis/`, FORMAT et
  `gates.yml` ; le commentaire est exact (leurres relus) et l'analyseur dit déjà qu'une étape `env:` est exclue.
- **Précisions d'items existants** (adoptées par l'adjudication) : d'accord. Pour SHOGEN-S2BIS-RB3-DEGRADATIONS-1, la
  ligne l.1331 cite « FORMAT §16.2 » pour le jugement de `status`, qui est au §17.2 depuis la numérotation actuelle (le
  §16.2 est le statut d'une réponse RFC 3161) : écrire « §17.2 » dans la précision versée.

## 5. Corrections (liste fermée C-1 à C-10)

Forme exacte : `corrections/G2-corrections.diff` (sha256 en §10), à appliquer après DT6-j (`git apply --check` vérifié
sur la copie à 094fa5d + série) ; scripts de remplacement exacts dans `corrections/` (chaque remplacement présent une
fois). Tests d'abord : rouge montré avant chaque code ; pour les tests seuls, rouge sur le mutant du réviseur qui
vivait. Aucun nombre de tests ne change (cas ajoutés dans des tests existants) : plancher 357 inchangé. Le FORMAT
changeant (C-3, C-4, C-10), l'heure de l'ajout daté DETTES-T6 se reporte à la dernière écriture (règle C-13) ; une
section de METRIQUES décrit les corrections (convention des sous-lots).

- **C-1 (code, STATUS-QUEUES-1, I-3)** : `status.etat` fait de `e.get("ws")` une clé de dictionnaire : une `sante` hors
  FORMAT dont `ws` est une liste ou un objet (ligne JSON valide) lève TypeError, trace Python de `status` et de `resume`
  (sonde P1 ; fuzz P4, graine 6 : 193 traces sur 3 000 journaux tirés, toutes de ce type). Forme : `derniere = e` ; la
  `sante` n'entre dans `en_cours` et ne donne un relevé D-3 que si `type(e.get("ws")) is int`. Test :
  `test_ligne_hors_format_jamais_une_trace` + deux `sante` (`ws` [1], puis {"a": 1}) : rouge FAIL (« TypeError » rendu
  par `sans_attente`), vert après ; fuzz P4 après C-1 : 0 trace sur 4 × 3 000 journaux (graines 6 à 9).
- **C-2 (code, STATUS-QUEUES-1)** : le compte `(max(juges) - debut) // W + 1` sous-estime d'une fenêtre la grille de
  `range(debut, max(juges) + W, W)` quand `ws` n'est pas sur la grille (hors FORMAT) : 46 081 fenêtres admises, contre «
  au plus 46 080 » au §17.3 (sonde P2). Forme : `n = len(range(debut, max(juges) + W, W)) if juges else 0`, refus si `n
  > GRILLE`, message sur `n`. Test : `test_etendue_de_la_grille_a_la_borne` + marqueur à 23:59:30 : rouge FAIL
  (RefusStatus non levé), vert après.
- **C-3 (textes, CHRONYC-FORMAT-1, O-3)** : « `sortie` est la sortie standard, suivie de la sortie d'erreur dans le même
  flux » (FORMAT §13.3 ; docstring de `horloge_systeme` ; METRIQUES DT6-e) est inexact : avec
  `stderr=subprocess.STDOUT`, les deux sorties sont mêlées dans l'ordre où la commande les écrit (sonde P3 : `sh` qui
  écrit l'erreur d'abord rend la ligne « ERREUR » avant la ligne « NORMAL » ; un programme C dont la sortie standard est
  un tube la tamponne [inféré : règle de stdio hors terminal, non mesurée sur chronyc]). Forme : « la sortie standard et
  la sortie d'erreur, mêlées dans un même tube dans l'ordre où la commande les écrit ».
- **C-4 (texte, Q-1)** : FORMAT §17.2 « (Q-1 du lot DETTES-T6, à adjuger : … » : périmé après l'adjudication ; forme : «
  (Q-1 du lot DETTES-T6, adoptée : … ».
- **C-5 (test, STATUS-QUEUES-1)** : le motif `illisible (<exception>)` (§17.4) n'est éprouvé par aucun test : R02
  (OSError non rattrapée à l'ouverture) vit. Forme : `test_fichiers_arretes_avant_leur_fin_nommes` + un lien
  `pool-2026-10-05-6.jsonl` vers un fichier absent, motif `illisible (FileNotFoundError)`. Rouge sur R02 : FAIL 1.
- **C-6 (test, STATUS-QUEUES-1)** : la borne de lecture d'une ligne (`readline(LIMITE)`, d'où le motif `ligne coupée`
  d'une ligne de plus de LIMITE octets) n'est éprouvée par aucun test : R03 (`readline()` sans borne) vit. Forme : même
  test + `pool-2026-10-05-7.jsonl`, une ligne JSON valide de plus de LIMITE octets close par un saut de ligne, motif
  `ligne coupée`. Rouge sur R03 : FAIL 1.
- **C-7 (test, CHRONYC-FORMAT-1)** : les contrôles des valeurs de Root delay et Root dispersion et du type de `sortie`
  ne sont éprouvés par aucun test (R10, R11, R12 vivent ; chacun rétablirait une trace de `status`). Forme :
  `test_d3_jugee_sur_la_sortie_gelee` + trois variantes (Root delay « 0.5 seconds », Root dispersion « 0.25 seconds »,
  `sortie` null : D-3, dernier relevé lisible à 180 s et plus), marqueur sans `sante` porté à la fenêtre 21, état pris
  par `sans_attente` (une exception devient un échec d'assertion). Rouge sur R10, R11, R12 : FAIL 1 chacun.
- **C-8 (test, JOURNAL-FICHIER-SPECIAL-1)** : l'ouverture sans attente de `_synchro`, ajoutée par DT6-c, n'est éprouvée
  par aucun test : R13 (sans `O_NONBLOCK`) vit. Chemin : reprise du même jour, fichier de la veille non sommé (`_sommes`
  le synchronise avant de le lire), tube posé après le contrôle par `stat`. Forme : dernier cas de
  `test_fichier_special_au_nom_d_un_fichier_du_journal` (fichier de sommes vide présent, tube au nom de la veille,
  `os.stat` simulé, espion de fsync) : refus `JOURNAL/fichier`, neuf refus. Rouge sur R13 : FAIL 1 (« bloqué »).
- **C-9 (test, ASN-LECTURE-1)** : la borne « 1 à 10 chiffres » n'est figée par aucun test : R15 (`[0-9]+`) vit. Forme :
  `test_ripestat_forme_de_s2_bornes_et_base_muette` + « 0000064500 » admis (64500) et « 00000064500 » refusé. Rouge sur
  R15 et R15b (`{1,9}`) : FAIL 1 chacun.
- **C-10 (texte, STATUS-QUEUES-1)** : lu pendant la collecte (§17.1 l'admet), le dernier fichier peut porter `ligne
  coupée` pour la ligne en cours d'écriture : une écriture de plusieurs pages se lit en cours (sonde P5b : 24 998
  relectures sur 25 037 voient un fichier sans saut de ligne final pendant 40 écritures de 3 Mio par un seul `os.write`
  en `O_APPEND`). Forme : phrase au §17.4 : motif passager, qui disparaît à la lecture suivante ; persistant, il dit une
  queue (§7).

## 6. Vérifications rejouées (copie creuse à 094fa5d + série ; réseau coupé ; `python3` -> `python3.12`)

| vérification (ligne de `gates.yml`) | résultat |
|---|---|
| runner `enforcement/tests/run-fixtures-verdict-suite-s2.py` | `verdict-suite-s2 : 137 ok, 0 échec` |
| job s2bis (`--aucun-saut --egal --plancher 357`) | `conforme (code 0, résumé final, aucun saut, Ran = 357)`, 40 s |
| matrice 3.10.20, 3.11.15, 3.12.3, 3.13.14 (`-X dev -W error`, `PYTHONDEVMODE=1`, `PYTHONWARNINGS=error`) | conforme, Ran = 357, sortie 0 ; 0 « Exception ignored », 0 « warning » (insensible à la casse), chacune |
| job S2 (`--egal`) | `conforme (code 0, résumé final, sauts nommant SHOGEN_S2_CAMPAGNE_CONTROL, Ran = 415)` |
| jobs sim-bis (279), calib-actifs (65), controle (26) | conformes, Ran = plancher, aucun saut |
| `enforcement/docs-sha256sums.py .` | `conforme : 34 SHA256SUMS, 295 ligne(s), dont 11 absente(s) admise(s) (SHOGEN-SIM-SOMMES-1) ; 4 fichier(s) non listé(s), non refusés` |
| `enforcement/journaux-modele.py .` ; `lint-model-pinning.sh .` | conforme (52 journaux exemptés) ; `OK (R-1) : 7 fichier(s)` |
| états intermédiaires : base reconstituée (`git apply -R` de j à a, égale à HEAD sur les 19 fichiers touchés), puis DT6-a … DT6-j un à un, ligne s2bis de chaque état | chaque état « conforme (code 0, résumé final, aucun saut, Ran = plancher) » : a 343, b 344, c 346, d 350, e 352, f 353, g 354, h 355, i 357, j 357 ; l'état j est identique à la copie de la série (`diff -rq`) |
| `cargo --locked xtask verify` (VERDICT seules) | S-G1 à S-G8 `VERDICT : VERT (0 violation(s))` ; S-G9 `VERDICT : ROUGE (1 violation(s))`, seule violation `docs/17-modele-de-menace.md:70 — (a) référence : fichier introuvable depuis la racine` (copie creuse, attendu) ; `cargo fmt --check : VERT` ; no_std : VERT ; `cargo clippy -D warnings : VERT` ; global ROUGE par S-G9 seule : rien d'autre ne rougit ; même sortie sur la copie corrigée |
| copie corrigée (série + C-1 à C-10) : runner ; job ; matrice 3.10 à 3.13 | runner `137 ok, 0 échec` ; job conforme, Ran = 357 ; matrice 3.10 à 3.13 conforme, Ran = 357, 0 « Exception ignored », 0 « warning » ; R02, R03, R10 à R13, R15, R15b tués par la commande du job (T00 VIVANT) |

## 7. Estimateur propre : mutants du réviseur

Formes écrites par le réviseur, complémentaires des 105 du générateur (relus : `travail/mutants/dt6*.py`), sur
`status` et sa grille, la lecture du journal et les fichiers spéciaux, le relevé ASN, chrony D-3, puis les trois
fermetures de fait sous des formes neuves. Commande exacte du job `s2bis-unittest` (runner, puis ligne de `gates.yml`
lue dans la copie, `python3` -> `python3.12`), réseau coupé, borne de 300 s ; classement par la sortie du vérificateur
(SHOGEN-MUT-FATAL-1) ; témoin T00 VIVANT ; chaque remplacement présent une fois, compilation contrôlée, fichiers
restaurés et contrôlés par sha256. Runner « 137 ok, 0 échec » à chaque exécution ; durée 45 à 52 s par exécution.

| id | mutant | sur la série | sur la série + corrections |
|---|---|---|---|
| R01 | grille allouée avant le contrôle de l'étendue | TUÉ (`test_saut_d_horloge_en_avant_refus_nomme`) | — |
| R02 | OSError à l'ouverture non rattrapée par `status` | VIVANT | TUÉ (C-5) |
| R03 | `readline()` sans borne dans `status` | VIVANT | TUÉ (C-6) |
| R05 | un relevé illisible efface le dernier relevé lisible | TUÉ (`test_d3_jugee_sur_la_sortie_gelee`) | — |
| R06 | délai et dispersion racine permutés dans la borne | TUÉ (même test) | — |
| R10 | valeur de Root delay non contrôlée | VIVANT | TUÉ (C-7) |
| R11 | valeur de Root dispersion non contrôlée | VIVANT | TUÉ (C-7) |
| R12 | type de `sortie` non contrôlé | VIVANT | TUÉ (C-7) |
| R13 | `_synchro` ouvert en attente | VIVANT | TUÉ (C-8) |
| R14 | crochets comptés 2 (borne au-dessus des octets) | TUÉ (`test_run_params_…`, `test_octets_comptes_…`) | — |
| R15 | texte d'AS sans borne de longueur | VIVANT | TUÉ (C-9) |
| R15b | texte d'AS de 1 à 9 chiffres | — | TUÉ (C-9) |
| R16 | Cymru : premier champ entier, non son premier mot | TUÉ (`test_cymru_premier_txt_lisible_forme_de_s2`) | — |
| W01 | DNS-ID-16BITS-1 : contrôle de l'identifiant retiré | TUÉ (`test_identifiant_hors_de_16_bits_refus_nomme`) | — |
| W02 | TARDIVES-BORNE-1 : place rendue avant le résultat | TUÉ (`test_resultat_rendu_avant_la_place`) | — |
| W03 | IMBRICATION-OCTETS-1 : décodeur avant le compte | TUÉ (deux tests de `test_reprise`) | — |

Bilan : sur la série, 15 mutants, 8 tués, 7 vivants, 0 FATAL, 0 équivalent ; chaque vivant est un manque de test
d'une ligne relue (aucun n'est équivalent : chacun change un comportement que le FORMAT écrit ou rétablit une trace) ;
sur la série corrigée, les 7 vivants et R15b sont tués par la commande du job (T00 VIVANT, Ran = 357).

## 8. Observations sans correction, écarts du réviseur

Observations (jugées, rien à corriger dans le lot) :
- **O-1** Les phrases de fermeture proposées pour l'annexe B (RAPPORT-GENERATEUR §2) sont exactes une fois les
  corrections appliquées (celle de STATUS-QUEUES-1 ne l'est qu'après C-1 et C-2) ; au versement, celles de
  STATUS-QUEUES-1, CHRONYC-FORMAT-1, JOURNAL-FICHIER-SPECIAL-1 et ASN-LECTURE-1 citent aussi les corrections qui les
  complètent (C-1, C-2, C-5, C-6, C-10 ; C-3, C-4, C-7 ; C-8 ; C-9) et leurs commits.
- **O-2** Les mesures d'avant (3,8 s pour 2^20 feuilles ; 10,2 s et 2 Gio ; MemoryError en 3,6 s sous 512 Mio) sont
  celles du générateur [2nd], non refaites : aucune ne porte un jugement de cette relecture ; R01 (grille allouée avant
  le contrôle) est tué par le test sous 512 Mio, ce qui recoupe la dernière.
- **O-3** L'authenticité de l'archive de chrony 4.6.1 n'est pas vérifiable hors réseau (L-5 du générateur, partagée) :
  les fichiers lus sont ceux qu'il a téléchargés, aux sha256 qu'il consigne ; la forme lue est confirmée par l'exemple
  de la documentation de la même archive.
- **O-4** La campagne du générateur pour DT6-e à DT6-i et V a tourné sur des copies qui ne diffèrent de l'état final que
  par une docstring (E-13) ; la campagne du réviseur tourne sur l'état final.

Écarts du réviseur (déclarés) :
- **E-1** Effort `high` demandé par le brief, `max` à la fiche : comme l'E-0 du générateur, admis par l'adjudication.
- **E-2** (01:02 UTC) Une première attente en tâche de fond (`until ! pgrep -f …`) se reconnaissait elle-même dans sa
  ligne de commande et ne pouvait finir : arrêtée (sortie 144), remplacée par une attente sur le PID ; sans effet sur
  les résultats.
- **E-3** Un contrôle de largeur par `awk length` comptait des octets (accents) : écarté, remplacé par un compte de
  caractères en Python (aucune ligne ajoutée de plus de 120 caractères, série et corrections).
- **E-4** (00:35 UTC) Une ligne de NOTES portait une plage horaire fausse (« 00:31-00:50 ») : corrigée aussitôt («
  00:31-00:35 »).
- **E-5** La première écriture de C-3 laissait une ligne de 172 caractères dans METRIQUES : reprise avant la génération
  du diff des corrections.
- **E-6** La confirmation des mutants sur la copie corrigée a tourné avant C-10 (texte du FORMAT seul, sans effet sur
  ces mutants) ; la vérification finale de la copie corrigée (runner, job, matrice) inclut C-10.
- **E-7** Pendant la campagne, des sondes légères (fuzz P4, P5) ont tourné : au plus deux processus lourds ; chaque
  mutant tué ne l'a été que par le test visé (listes d'échecs relues), le témoin est VIVANT.

## 9. Journal de provenance (G1 du réviseur)

Sources lues (niveau ; sha256 ; pièces du dépôt à 094fa5d, dans la copie creuse) :
- [lu] BRIEF-G2.md `2ca0d582…7807` ; BRIEF-DETTES-T6.md `48edfb43…a17fd` ; ITEMS-ANNEXE-B.md `712b2c52…4d79` (20 lignes
  comparées octet pour octet à l'annexe B : conformes) ; ADJUDICATION.md `58ee8355…9f2d` ; RAPPORT-GENERATEUR.md
  `97233576…2cc5` ; NOTES.md du générateur `e6273a31…542d` ; SHA256SUMS du lot (12 OK) ; diffs DT6-a à DT6-j en entier.
- [lu] `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md` entier `d9160d3e…0a9` ; `PROPOSITION.md` §2 (l.111-373)
  `0cdf84c2…bfd0` ; FORMAT final (§7.7, §8.4, §9.1 l.330-362, §13.3, §13.6, §14.4, §15.4-15.5, §16.4-16.6, §17 ; ajout
  daté) ; ADR-0029 l.76-120, 196, 239, 245, 248 `32a59893…2801` ; annexe B l.1010, 1047, 1051, 1057, 1110, 1116, 1158,
  1160, 1165, 1309, 1314-1317, 1328-1347 `709e146c…55fa` (grep ciblé du seul fichier) ; revue-p2b
  RAPPORT-GENERATEUR-transcrit l.170-185 `c214c43c…8a19` (I-3) ; revue-p1b G2-P1B-transcrit l.40-56 `b57c676c…af8ae9`
  (I-B1, O-3) ; `<scratchpad>/s2bis/db0/ADJUDICATION-DB0.md` `bbc4ae5a…5e9e` (points 7 et 8).
- [lu] code final entier : `status.py`, `journal.py`, `entree.py`, `asn.py` ; parties : `sante.py` l.1-45,
  `decodeurs.py` l.30-111, `boucle._lire`, `tetes.lire_borne`, tests touchés par la série ; runner l.20, l.642-655 ;
  `verdict-suite-s2.py` l.1-80, `lancer` ; `tests/__init__.py` l.5-14 ; `config_analyse.py` l.92, `analyse.json`.
- [lu] commits `af7c3cc`, `03fcfd4`, `e6edba2` (`git show --stat` et diffs des fichiers cités, lecture seule).
- [lu, copie téléchargée par le générateur, sha256 recontrôlés] chrony 4.6.1 : archive `571ff73f…9c5c`, `client.c`
  `7e515f33…2d6d` (l.1645-1660, 1735-1790, 2173-2222 ; aucun `setlocale`), `doc/chronyc.adoc` `dc955e0f…c5a7`
  (l.140-165, 225-262) ; archive 4.9 `4924c6f5…64d0` (hash seul). Authenticité de l'archive : non vérifiable hors réseau
  (L-5 du générateur, partagée).
- [2nd, non refait] mesures du générateur citées par ses phrases (3,8 s pour 2^20 feuilles ; 10,2 s et 2 Gio ; 3,6 s
  sous 512 Mio) : aucune n'entre dans un jugement de cette relecture.

Commandes lancées et sorties (toutes réseau coupé, `outils/iso.sh` `6c44c71a…9161` sur `isole.sh` `ebaa1c78…8a3e` et
`lo_up.py` `b532be4b…083e`, mandataires et `SHOGEN_S2_CAMPAGNE_CONTROL` retirés) : voir §6 et `NOTES.md` ; sorties
complètes dans `sorties/` (runner.txt, job-*.txt, matrice-3.1x.txt, docs-sha256sums.txt, journaux-modele.txt,
lint-r1.txt, mutants-g2.{log,json}, mutants-g2-corr.{log,json}, mutants-g2-extra-corr.json, rouge-*.txt, etats.txt,
corr-verifs.txt, xtask-*.txt). Outils : `outils/campagne.py` `ea55f142…45aa`, `outils/rouge_mutants.py`,
`outils/etats.sh` `a9037732…88d5`, `outils/matrice.sh`, `outils/matrice_corr.sh`, `outils/confirmation.sh`,
`outils/diff_corrections.sh` `21115cb1…ca51` ; sondes `sondes/p1_ws_liste.py`, `p2_grille_non_alignee.py`,
`p3_ordre_sorties.py`, `p4_fuzz_status.py` `84af58c0…c018`, `p5_lecture_pendant_ecriture.py`,
`p5b_lecture_pendant_ecriture.py` ; spécifications `mutants/g2.py` `88867485…02d0`, `mutants/g2-extra.py`.

## 10. Fichiers rendus

Rendu le 2026-10-10 01:13:52 UTC (`date -u`). Dans `<scratchpad>/s2bis/dettes6/g2/` : `RAPPORT-G2.md` (ce rapport),
`NOTES.md`, `corrections/G2-corrections.diff` (`2b6d931abcd012898402d97a42e4d36d878dae76780bdfec38ecf5bcfd5c94ab`, 221
lignes, à appliquer après DT6-j) et les scripts de remplacement qui l'ont produit, `mutants/`, `outils/`, `sondes/`,
`sorties/` ; `SHA256SUMS` du dossier écrit en dernier (hors `tmp/` ; copies et cible de construction supprimées). Aucun
commit, aucun push, aucune écriture dans le dépôt. Tête relue au rendu : `ba03914d…0c82` (chaîne DETTES-T5 en cours de
commit depuis 094fa5d) ; entre les deux, parmi les fichiers de la série, seul `.github/workflows/gates.yml` change : le
recalage de la série sur le plancher (+1, adjudication) revient au générateur ; le diff des corrections ne touche pas
`gates.yml` et n'ajoute aucun test.
