# Rapport du générateur de DETTES-T6, avec ses sections datées de correction (phases 1 à 5) (transcrit)

> Transcription par l'orchestrateur le 2026-10-10 09:08:09 UTC du fichier RAPPORT-GENERATEUR.md ; contrôle FM-1.1 des transcripts du générateur-correcteur, du réviseur G2 et du contre-contrôleur, par le fm11.py versé et par celui de DT3-E : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# RAPPORT-GENERATEUR — lot de dettes DETTES-T6 (collecteur P2 de S2-bis : robustesse et tests, 16 items)

- **Rôle** : générateur G1 (fiche `shogen-worker`). **Gate 0** : modèle résolu `claude-opus-5-5` (identifiant exact lu
  dans l'invite système du worker). Effort demandé par le lanceur : `high` (la fiche dit `max` explicite : écart E-0).
- **Brief** : `BRIEF-DETTES-T6.md`, sha256 `48edfb433fe1a697228e6780173c3aefea6c4381975776dc2c7fc0a411fa17fd` ;
  `ITEMS-ANNEXE-B.md`, sha256 `712b2c52c28e2af221fcf5789e4d1cdcf126b1a0462a8f6e3f9e338c5a3d4d79`.
- **Base** : `50ca52d8580855b573dc62e046130ce951760c5e` (DT4-f, tête de `claude/compassionate-noether-szmdyj` lue à
  21:07:31 UTC). **Tête relue à la fin** : `094fa5d3d5debe9dd466e37feee95200ca460dcf` (Merge PR #10 : DETTES-T4 et correctif YAML DT5-0), relue à 00:24:55 UTC le 2026-10-10. La série s'applique sur les deux (§5).
- **Heures** (`date -u`) : début 2026-10-09 21:07:53 UTC ; redémarrage du conteneur vers 22:55 UTC (processus perdus,
  fichiers intacts ; reprise à 22:56:10 UTC depuis `NOTES.md`) ; rendu 2026-10-10 00:25:07 UTC.
- Dépôt lu seulement (`git --no-optional-locks`) ; aucune écriture git, aucun commit ; `SHOGEN_S2_CAMPAGNE_CONTROL`
  jamais posée ; aucune pièce de D.2 ni aucun dossier interdit ouvert ; aucun `.jsonl` du dépôt lu ; bibliothèque
  standard seule (R-8) ; suites et campagnes réseau coupé (`isole.sh`, variables de mandataire retirées).

## 1. Série de diffs (dans l'ordre d'application)

Compte R-25 (convention écrite par DT6-a) : lignes ajoutées des fichiers `.py` et `.yml` ; `.md` et fixture hors compte.

**Phase 2** : ce tableau est celui de la phase 1 (base `50ca52d`, planchers 343 à 357). La série rendue est celle du
§10 : DT6-a à DT6-k, recalée sur DETTES-T5 (planchers 344 à 358), nouveaux sha256.

| diff | objet | items (S2BIS-…) | R-25 | autres ajouts | sha256 | suite | mutants |
|---|---|---|---|---|---|---|---|
| DT6-a | borne basse des octets par occurrence ; cycle avant le sérialiseur ; convention R-25 | CANONIQUE-OCTETS-1, CORPS-BORNE-1 (résiduel), R25-COMPTE-1 | +77 | FORMAT-JOURNAUX-S2BIS.md +17, METRIQUES-S2BIS.md +28 | `fa5a827003a71f4c…` | 343 | 12/12 tués, 0 FATAL (témoin VIVANT) |
| DT6-b | borne d'exposant de `_entier` figée, docstring | DECODEURS-BORNE-TEST-1 | +26 | METRIQUES-S2BIS.md +24 | `5f570543b5880ab5…` | 344 | 9/9 tués, 0 FATAL (témoin VIVANT) |
| DT6-c | fichiers du journal ordinaires, lus sans attente | JOURNAL-FICHIER-SPECIAL-1 | +71 | FORMAT-JOURNAUX-S2BIS.md +13, METRIQUES-S2BIS.md +26 | `76cce28dbe6f9c01…` | 346 | 10/10 tués, 0 FATAL (témoin VIVANT) |
| DT6-d | `status` : arrêts nommés, grille bornée, disque partiel | STATUS-QUEUES-1 | +107 | FORMAT-JOURNAUX-S2BIS.md +21, METRIQUES-S2BIS.md +24 | `0fac5962e0bf51c5…` | 350 | 11/11 tués, 0 FATAL (témoin VIVANT) |
| DT6-e | D-3 jugé sur `chronyc -n tracking` lu sur pièce ; sortie d'erreur gardée | CHRONYC-FORMAT-1 | +144 | FORMAT-JOURNAUX-S2BIS.md +32, METRIQUES-S2BIS.md +35, tracking.txt +13 | `eb4617d04ebe368b…` | 352 | 17/17 tués, 0 FATAL (témoin VIVANT) |
| DT6-f | ASN en chiffres ASCII ; IPv4 littérale relevée directement | ASN-LECTURE-1, ASN-HOTE-IPV4-1 | +67 | FORMAT-JOURNAUX-S2BIS.md +16, METRIQUES-S2BIS.md +29 | `a89bf78354008bc1…` | 353 | 11/11 tués, 0 FATAL (témoin VIVANT) |
| DT6-g | journal du secondaire contrôlé de bout en bout (test seul) | SECONDAIRE-CONFORMITE-1 | +71 | FORMAT-JOURNAUX-S2BIS.md +2, METRIQUES-S2BIS.md +26 | `c643fb8df7669f0c…` | 354 | 10/10 tués, 0 FATAL (témoin VIVANT) |
| DT6-h | `run_params` trop grand : refus de configuration | ECRIVAIN-REFUS-ARRET-1 | +47 | FORMAT-JOURNAUX-S2BIS.md +6, METRIQUES-S2BIS.md +24 | `04fbb1bd9fc9c76a…` | 355 | 9/9 tués, 0 FATAL (témoin VIVANT) |
| DT6-i | phrases des §16 et §17 figées par `test_format` (tests seuls) | FORMAT-P2B-TESTS-1 | +46 | FORMAT-JOURNAUX-S2BIS.md +2, METRIQUES-S2BIS.md +22 | `608e4cbad5ac095b…` | 357 | 12/12 tués, 0 FATAL (témoin VIVANT) |
| DT6-j | forme fermée des jobs unittest : ligne `env` (commentaire YAML) | ENV-ETAPE-1 | +4 | — | `09fdc6f63ef3622a…` | inchangée | sans objet (commentaire) |

Chaque diff : rouge d'assertion montré avant le vert (tests finaux sur le code d'avant, ou, pour les diffs de tests
seuls, sur un mutant), planchers exacts recalés (`--egal`), section de METRIQUES quand la suite change, lignes de
120 caractères au plus, aucun `TODO`/`FIXME`, aucune barre oblique inverse ajoutée. Mutants : commande exacte du job
`s2bis-unittest` (runner des cas, puis ligne `verdict-suite-s2.py s2bis …` lue dans le `gates.yml` de la copie,
`python3` remplacé par `python3.12`, interpréteur de l'image ubuntu-24.04), borne de 300 s (dépassement FATAL),
réseau coupé, témoin T00 sans mutation VIVANT avant chaque campagne, fichiers restaurés et contrôlés par sha256 après
chaque mutant ; classement par la sortie (1 tué, 0 vivant, autre FATAL) ; chaque mutant contrôlé avant campagne
(application unique, syntaxe valide).

## 2. Items : fermeture et phrase proposée pour l'annexe B

Tableau (16 items, liste fermée du brief) :

| item | fermé par | tests (module.Classe.test) | mutants |
|---|---|---|---|
| S2BIS-CORPS-BORNE-1 | CB-3, CB-5 (corps) ; CB-6d `03fcfd4` (graphe) ; DT6-a (résiduel : cycle) | `test_lecture_pendue.LecturePendue.test_corps_maximal_ecrit_sous_la_borne_de_ligne` ; `test_journal.Ecrivain.test_graphe_partage_refuse_en_temps_borne` ; `test_journal.Ecrivain.test_cycle_refuse_avant_le_serialiseur` | DT6-a (A01, cycle laissé au sérialiseur) |
| S2BIS-CHRONYC-FORMAT-1 | DT6-e (Q-1, Q-6) | `test_status.Etat.test_d3_jugee_sur_la_sortie_gelee` ; `test_sante.Sondes.test_sortie_d_erreur_gardee_dans_la_borne` | DT6-e 17/17 tués |
| S2BIS-DNS-ID-16BITS-1 | CB-12a `af7c3cc` (vérifié) | `test_dns.Interroger.test_identifiant_hors_de_16_bits_refus_nomme` | V01 tué |
| S2BIS-ECRIVAIN-REFUS-ARRET-1 | C-1 de P1-C (sondes DNS) ; CB-6c `e6edba2` (décodeurs, vérifié) ; DT6-h (`run_params`) | `test_decodeurs.Politique.test_valeurs_refusees_par_l_ecrivain_jamais_rendues` ; `test_entree.Entree.test_run_params_qui_passerait_limite_refus_de_configuration` | V04 tué ; DT6-h 9/9 tués |
| S2BIS-ECRIVAIN-IMBRICATION-OCTETS-1 | CB-6d `03fcfd4` (vérifié) | `test_reprise.Reprise.test_niveaux_comptes_sur_les_octets_avant_le_decodeur` | V03 tué |
| S2BIS-TARDIVES-BORNE-1 | CB-6d `03fcfd4` (vérifié) | `test_boucle.Boucle.test_resultat_rendu_avant_la_place` | V02 tué |
| S2BIS-ASN-HOTE-IPV4-1 | DT6-f (Q-2) | `test_asn.Releve.test_hote_ipv4_litterale_releve_directement` ; `test_secondaire.Isolement.test_carte_pendue_ou_refusee_le_pool_intact` (relevé injecté) | F07 à F11 tués |
| S2BIS-ASN-LECTURE-1 | DT6-f (Q-3) | `test_asn.Decodage.test_ripestat_forme_de_s2_bornes_et_base_muette` ; `test_asn.Decodage.test_cymru_premier_txt_lisible_forme_de_s2` | F01 à F06 tués |
| S2BIS-CANONIQUE-OCTETS-1 | DT6-a (Q-4) | `test_journal.Ecrivain.test_octets_comptes_par_occurrence_avant_le_serialiseur` | DT6-a 12/12 tués |
| S2BIS-DECODEURS-BORNE-TEST-1 | DT6-b | `test_decodeurs.Bornes.test_borne_d_exposant_figee` | DT6-b 9/9 tués (dont K1-03) |
| S2BIS-JOURNAL-FICHIER-SPECIAL-1 | DT6-c | `test_reprise.Reprise.test_fichier_special_au_nom_d_un_fichier_du_journal` ; `test_status.LectureDuJournal.test_fichier_special_non_lu_sans_attente` | DT6-c 10/10 tués |
| S2BIS-STATUS-QUEUES-1 | DT6-d (Q-5) | `test_status.Etendue` : `test_fichiers_arretes_avant_leur_fin_nommes`, `test_saut_d_horloge_en_avant_refus_nomme`, `test_etendue_de_la_grille_a_la_borne`, `test_ligne_hors_format_jamais_une_trace` | DT6-d 11/11 tués |
| S2BIS-ENV-ETAPE-1 | DT6-j (Q-7) | runner (K-02 lit le job) | sans objet (commentaire) |
| S2BIS-FORMAT-P2B-TESTS-1 | DT6-i | `test_format.Format.test_paragraphe_16_tetes_depot_et_jeton` ; `test_paragraphe_17_status_et_resumes` | DT6-i 12/12 tués (dont K-C7-2) |
| S2BIS-R25-COMPTE-1 | DT6-a (en-tête de METRIQUES) | appliquée à chaque diff (§1) | sans objet (convention) |
| S2BIS-SECONDAIRE-CONFORMITE-1 | DT6-g | `test_secondaire.Conformite.test_journal_secondaire_conforme_au_format` | DT6-g 10/10 tués |

Phrases de fermeture proposées (style de B.88 à B.91 ; « DT6-x » à remplacer par le commit) :

- SHOGEN-S2BIS-CORPS-BORNE-1 **fermé** : borne du corps par CB-3 et CB-5 (l.1047) ; volet graphe par CB-6d (`03fcfd4` :
  valeurs comptées une fois par occurrence, sans développer le graphe ;
  `test_journal.Ecrivain.test_graphe_partage_refuse_en_temps_borne`) ; résiduel par DT6-a : un cycle placé derrière un
  graphe partagé n'était vu par le sérialiseur qu'après le développement du graphe (3,8 s pour 2^20 feuilles,
  mesuré) ; il est refusé `JOURNAL/type` avant le sérialiseur, en temps linéaire
  (`test_journal.Ecrivain.test_cycle_refuse_avant_le_serialiseur`, FORMAT §8.4).
- SHOGEN-S2BIS-CANONIQUE-OCTETS-1 **fermé** par DT6-a (Q-4) : `canonique` compte une borne basse des octets de la ligne,
  une fois par occurrence et sans développer le graphe (crochets, séparateurs, clés, chaînes, chiffres des entiers
  bornés par leur taille en bits), et refuse avant le sérialiseur une ligne qui passerait LIMITE (`JOURNAL/taille`) ;
  le sérialiseur écrit au plus 8 × LIMITE octets ; borne écrite au §8.4 ; une chaîne de 1 Mio partagée 1 000 fois,
  admise avant (10,2 s, pic de 2 Gio, mesuré), est refusée sans sérialisation
  (`test_journal.Ecrivain.test_octets_comptes_par_occurrence_avant_le_serialiseur`).
- SHOGEN-S2BIS-R25-COMPTE-1 **fermé** par DT6-a : convention en tête de `METRIQUES-S2BIS.md` (borne de 200 lignes sur les
  lignes ajoutées des fichiers `.py` et `.yml`, colonne des ajouts de `git diff --numstat` ; données, fixtures et
  documents hors compte, déclarés dans la section du sous-lot).
- SHOGEN-S2BIS-DECODEURS-BORNE-TEST-1 **fermé** par DT6-b : `test_decodeurs.Bornes.test_borne_d_exposant_figee` fige la
  borne exacte de `_entier` (9E+15 et 9,999999999999999E+15 convertis ; 1E+16, 1E+17, 10000000000000000 et 0E+16
  refusés avant int()) et rend 1E+199999 et 1E+200000 en `panne_decode` en moins de 0,1 s à chaque champ d'instant ;
  docstring exacte (0E+16 refusé) ; le mutant K1-03 du contre-contrôle de P2A est tué.
- SHOGEN-S2BIS-JOURNAL-FICHIER-SPECIAL-1 **fermé** par DT6-c : toute lecture du journal s'ouvre sans attente
  (`O_NONBLOCK`) et n'admet qu'un fichier ordinaire (`journal.ordinaire`, `JOURNAL/fichier`) ; l'écrivain refuse de
  démarrer devant un nom du journal ou des sommes qui n'est pas un fichier ordinaire, avant toute lecture et toute
  écriture ; `status` ne lit pas un tel fichier et le nomme (FORMAT §5, §7.7, §17.1 ;
  `test_reprise.Reprise.test_fichier_special_au_nom_d_un_fichier_du_journal`,
  `test_status.LectureDuJournal.test_fichier_special_non_lu_sans_attente`).
- SHOGEN-S2BIS-STATUS-QUEUES-1 **fermé** par DT6-d (Q-5) : grille de 46 080 fenêtres au plus (32 jours), au-delà le
  refus nommé `STATUS/grille` (avant : MemoryError en 3,6 s sous 512 Mio, mesuré) ; chaque fichier arrêté avant sa fin
  nommé avec son motif en dernière ligne du rapport (ligne illisible, hors FORMAT — I-3 —, jour postérieur au sien,
  ligne coupée, pas un fichier ordinaire, illisible) ; `disque` partiel « non relevé » (FORMAT §17.1, §17.3, §17.4 ;
  `test_status.Etendue`, 4 tests).
- SHOGEN-S2BIS-CHRONYC-FORMAT-1 **fermé** par DT6-e (Q-1, Q-6) : forme de la sortie de `chronyc -n tracking` lue sur
  pièce (source de chrony 4.6.1, `client.c` et `doc/chronyc.adoc`, sha256 au journal de provenance ; inchangée en 4.9)
  et écrite au FORMAT §13.3 ; `status` juge D-3 (§17.2 : relevé lisible, borne |System time| + Root dispersion + Root
  delay / 2 de plus de 1 s, statut autre que Normal, Insert second, Delete second, ou aucun relevé lisible d'une fenêtre
  commencée moins de 120 s avant) ; « hors D-3 » retiré du rapport et du quorum (§17.4, §17.6) ; la sonde garde la
  sortie d'erreur dans la borne de 4 096 caractères (O-3) ; `test_status.Etat.test_d3_jugee_sur_la_sortie_gelee`,
  `test_sante.Sondes.test_sortie_d_erreur_gardee_dans_la_borne`.
- SHOGEN-S2BIS-ASN-LECTURE-1 **fermé** par DT6-f (Q-3) : numéro d'AS de RIPEstat et de Cymru lu en entier ou en texte de
  1 à 10 chiffres ASCII, écart à `int()` de S2 écrit au §15.4 (souligné, signe, blancs, chiffres arabes-indiens et
  texte vide refusés : `test_asn.Decodage`).
- SHOGEN-S2BIS-ASN-HOTE-IPV4-1 **fermé** par DT6-f (Q-2) : un hôte écrit en IPv4 littérale canonique est relevé
  directement (`a` null, `ip` l'hôte, aucune requête A) ; une autre écriture est un nom (§15.4 ;
  `test_asn.Releve.test_hote_ipv4_litterale_releve_directement`).
- SHOGEN-S2BIS-SECONDAIRE-CONFORMITE-1 **fermé** par DT6-g : `test_secondaire.Conformite`, processus secondaire entier
  (cinq fenêtres), relevé ASN vers des serveurs factices de boucle locale, chaque enregistrement contrôlé contre le
  FORMAT (§1 à §14 par `anomalies` de `test_bout_en_bout`, §15 par des règles écrites dans le test) ; il tue 9 des
  10 mutants de la campagne, dont un que la suite laissait vivre (G05 : `run_params` du secondaire sans le sha256 de
  la carte).
- SHOGEN-S2BIS-ECRIVAIN-REFUS-ARRET-1 **fermé** : sondes DNS de P1 par C-1 ; décodeurs par CB-6c (`e6edba2`,
  `test_decodeurs.Politique.test_valeurs_refusees_par_l_ecrivain_jamais_rendues`) ; `run_params` par DT6-h : sa taille
  est contrôlée avant l'ouverture du journal, `seq` et `ws` sur 19 chiffres, refus `CONFIG/taille` (sortie 2, rien
  d'écrit), refus de l'écrivain rendu en refus de configuration (§14.4 ;
  `test_entree.Entree.test_run_params_qui_passerait_limite_refus_de_configuration`) ; aucun enregistrement que la boucle
  écrit n'atteint plus un refus de l'écrivain (§9.1, §13.6, §15.5, §16.5).
- SHOGEN-S2BIS-ECRIVAIN-IMBRICATION-OCTETS-1, SHOGEN-S2BIS-TARDIVES-BORNE-1 **fermés** par CB-6d (`03fcfd4`) et
  SHOGEN-S2BIS-DNS-ID-16BITS-1 **fermé** par CB-12a (`af7c3cc`) : fermetures de fait vérifiées sur l'état final de la
  série, un mutant par item qui rétablit le défaut de l'annexe B, tué par la commande du job (V01 à V04 :
  `test_dns.Interroger.test_identifiant_hors_de_16_bits_refus_nomme`, `test_boucle.Boucle.test_resultat_rendu_avant_la_place`,
  `test_reprise.Reprise.test_niveaux_comptes_sur_les_octets_avant_le_decodeur`, et pour les décodeurs
  `test_decodeurs.Politique.test_valeurs_refusees_par_l_ecrivain_jamais_rendues`).
- SHOGEN-S2BIS-FORMAT-P2B-TESTS-1 **fermé** par DT6-i : `test_format.Format.test_paragraphe_16_tetes_depot_et_jeton` et
  `test_paragraphe_17_status_et_resumes` figent 23 phrases normatives du §16 (dont celle du dépôt local de C-7) et 23
  du §17, et les bornes du texte égales à celles du code (1 024 octets, 16 têtes, 65 536 octets ; 46 080 fenêtres,
  131 072 octets) ; le mutant K-C7-2 du contre-contrôle de P2B est tué.
- SHOGEN-S2BIS-ENV-ETAPE-1 **fermé** par DT6-j (Q-7) : ligne écrite au job `s2bis-unittest` de `gates.yml` : la forme
  fermée des jobs unittest n'admet aucune clé `env` (workflow, job, étape : leurres L-10, L-12, L-19 et L-33 du runner,
  refusés) ; une variable dont une suite a besoin se pose dans la suite (son `tests/__init__.py`, comme la purge des
  mandataires) ; tout autre besoin amende le gabarit K du runner et l'analyseur de `enforcement/verdict-suite-s2.py`,
  avec leurs cas.

Précisions d'items existants proposées (sans item nouveau) : SHOGEN-S2BIS-RB3-DEGRADATIONS-1 (l.1331) couvre aussi D-3
(forme du §13.3, âge du §17.2, Q-1) ; SHOGEN-S2BIS-CONFIG-PRODUCTION-1 (l.1152) scelle la commande d'horloge
`chronyc -n tracking` (L-2).

## 3. Questions (décisions à deux formes) : recommandation motivée, codée

- **Q-1** (CHRONYC-FORMAT-1, âge du relevé D-3) : (a) âge compté en fenêtres du journal : une fenêtre est D-3 si aucune
  `sante` d'une fenêtre commencée moins de 120 s avant elle, elle comprise, ne porte un relevé lisible (avec w = 60 s :
  elle et la précédente) ; (b) âge compté sur les instants `debut`/`fin` de la sonde ; (c) âge compté sur « Ref time
  (UTC) » de chrony. **Recommandation (a), codée** : ADR-0029 l.239 fait du relevé chrony la valeur D-3 de
  l'enregistrement de santé de chaque fenêtre et l.108 dit « aucun relevé chrony de moins de 120 s » ; (b) lit
  l'horloge même que D-3 juge ; (c) mesure l'âge de la dernière mise à jour de la référence de chrony, autre grandeur,
  que la borne d'erreur couvre déjà (Root dispersion croît avec lui). Sous-point : le statut « Invalid » (valeur hors
  des quatre connues de `client.c`) est jugé D-3 comme « Not synchronised » ; autre forme : le traiter en relevé
  illisible (dernier relevé lisible de moins de 120 s). Recommandation : D-3, lecture prudente d'un statut de
  synchronisation inconnu.
- **Q-2** (ASN-HOTE-IPV4-1) : (a) IPv4 littérale relevée directement ; (b) refusée par `hote-forme`.
  **Recommandation (a), codée** : `hote-forme` (§14.1) admet ces hôtes et la lecture les contacte sans résolution ; (b)
  changerait la configuration admise du pool et de la carte ; (a) relève l'AS de l'adresse réellement contactée. Forme
  canonique seule (`str(IPv4Address(h)) == h`) : « 127.1 » ou des zéros de tête restent des noms (L-3).
- **Q-3** (ASN-LECTURE-1) : (a) lecture stricte en chiffres ASCII, écart à S2 nommé au §15.4 ; (b) forme de S2
  (`int()`). **Recommandation (a), codée** : aucune des deux bases n'écrit un numéro d'AS avec souligné, signe, blancs
  ou chiffres d'une autre écriture ; un tel texte est une donnée altérée que (b) convertirait en AS plausible (« -0 »
  en 0, « ١٣٣٣٥ » en 13335) ; sur des réponses bien formées, (a) et (b) rendent les mêmes valeurs. Cymru garde la forme
  de S2 pour le découpage (premier mot du premier champ), le mot lu comme RIPEstat.
- **Q-4** (CANONIQUE-OCTETS-1) : (a) phrase seule au §8.4 (borne linéaire en valeurs et longueur des chaînes) ; (b)
  compte d'octets par occurrence et un test. **Recommandation (b), codée, avec la phrase** : (a) laisse un
  enregistrement de 1 Gio parvenir au sérialiseur avant tout refus (10,2 s, pic de 2 Gio, mesuré) ; (b) prend place
  dans le parcours que CB-6d fait déjà et borne la sortie du sérialiseur à 8 × LIMITE.
- **Q-5** (STATUS-QUEUES-1, borne de l'étendue) : (a) 32 jours, 46 080 fenêtres ; (b) 8 jours (rétention locale de
  7 jours et segment de reprise) ; (c) borne en mémoire. **Recommandation (a), codée** : plus de trois fois la
  rétention locale, un journal non purgé à temps reste lisible ; tout saut d'horloge au-delà est un refus nommé qui
  dit l'étendue ; (c) dépendrait de la machine.
- **Q-6** (CHRONYC-FORMAT-1, O-3, mémoire de la capture) : (a) borne de temps seule (délai de 2 s), sortie gardée coupée
  à 4 096 caractères ; (b) lecture bornée en octets, processus tué au-delà. **Recommandation (a), codée (état de
  DT6-e)** : la commande est scellée, locale, et sa sortie compte 13 lignes ; (b) remplacerait `subprocess.run` par une
  lecture à échéance et un arrêt de processus (≈ 25 lignes et leurs tests) sans gain sur la commande scellée. Limite
  écrite au §13.3 ; à reprendre si une sonde non scellée apparaît.
- **Q-7** (ENV-ETAPE-1, lieu de la ligne) : (a) commentaire du job `s2bis-unittest` dans `gates.yml` ; (b) docstring de
  l'analyseur (`enforcement/verdict-suite-s2.py`) ou du runner. **Recommandation (a), codée** : le brief borne le code du
  lot à `s2bis/`, au FORMAT et à `gates.yml` ; l'analyseur dit déjà qu'une ligne `env:` est exclue (`etapes`) ; (b)
  relève d'un lot qui touche l'enforcement.

## 4. Limites (L-n), sans item nouveau

- **L-1** : SHOGEN-S2BIS-RB3-DEGRADATIONS-1 (l.1331, G0 de RB-3) nomme D-4 et D-5 ; depuis DT6-e, `status` juge aussi
  D-3 : la règle de validité du recalcul doit reprendre la forme du §13.3 et l'âge du §17.2 (précision de l'item
  proposée).
- **L-2** : la commande d'horloge `chronyc -n tracking` n'est imposée par aucune règle de configuration (`sante.json`,
  `commande`) ; elle se scelle avec la configuration de production (SHOGEN-S2BIS-CONFIG-PRODUCTION-1, gel du
  collecteur ; précision proposée) ; une autre commande rendrait chaque fenêtre D-3 (défaut visible, jamais muet).
- **L-3** : une IPv4 écrite autrement qu'en forme canonique (« 127.1 », zéros de tête) est un nom, que le résolveur ne
  résout pas ; son écriture canonique relève de SHOGEN-S2BIS-NOMS-HOTE-RFC1123-1 (ouvert, l.1085 et l.1319).
- **L-4** : la forme de `tracking` est lue en chrony 4.6.1 et 4.9 ; la version installée se scelle au G0 de DEPLOI-BIS
  (R-8 des paquets système, ADR-0029 l.248) ; un écart de forme rendrait chaque fenêtre D-3 (visible).
- **L-5** : la signature de l'archive chrony 4.6.1 n'est pas vérifiée (clé du projet non détenue) ; archive, sources et
  documentation identifiées par sha256 (journal de provenance) ; la forme lue est confirmée par l'exemple de la
  documentation et par 4.9.
- **L-6** : mémoire de la capture D-3 bornée par le délai seul (Q-6).

## 5. Vérifications avant rendu (copie neuve à la tête, série appliquée)

Copie `tmp/tete` : clone du dépôt en lecture seule, sparse non-cone (dossiers interdits et `*.jsonl` exclus), à
`094fa5d3d5debe9dd466e37feee95200ca460dcf` (tête relue à 00:19 UTC) ; DT6-a à DT6-j appliqués dans l'ordre
(`git apply --check`, puis `git apply`) ; `s2bis/`, FORMAT et METRIQUES égaux octet pour octet à l'instantané final ;
`gates.yml` : seul écart, celui de la tête (DT5-0). Série aussi rejouée sur la base `50ca52d` : égale à l'instantané
final. Réseau coupé ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée ; sorties complètes `sorties/final-*.txt`.

| vérification (ligne de `gates.yml`, `python3` = python3.12) | résultat |
|---|---|
| runner `enforcement/tests/run-fixtures-verdict-suite-s2.py` | `verdict-suite-s2 : 137 ok, 0 échec` |
| job s2bis (`--aucun-saut --egal --plancher 357`) | `conforme (code 0, résumé final, aucun saut, Ran = 357)` |
| job S2 (`--egal`) | `conforme (code 0, résumé final, sauts nommant SHOGEN_S2_CAMPAGNE_CONTROL, Ran = 415)` |
| job sim-bis (plancher 279) | `conforme (…, aucun saut, Ran = 279)` |
| job calib-actifs (plancher 65) | `conforme (…, aucun saut, Ran = 65)` |
| job controle (plancher 26) | `conforme (…, aucun saut, Ran = 26)` |
| `enforcement/docs-sha256sums.py .` | `conforme : 34 SHA256SUMS, 295 ligne(s), dont 11 absente(s) admise(s) (SHOGEN-SIM-SOMMES-1) ; 4 fichier(s) non listé(s), non refusés` |
| `enforcement/journaux-modele.py .`, `lint-model-pinning.sh .` | conformes (52 journaux exemptés ; R-1 OK, 7 fichiers) |
| `cargo --locked xtask verify` | S-G1 à S-G8 : `VERDICT : VERT (0 violation(s))` (8 lignes) ; S-G9 : `VERDICT : ROUGE (1 violation(s))` ; `cargo fmt --check : VERT` ; no_std : VERT ; `cargo clippy -D warnings : VERT` ; global ROUGE |
| `cargo --locked test` (espace de travail) | 26 lignes `test result: ok.`, 259 tests passés, 0 échec |

**S-G9** : seule violation, `docs/17-modele-de-menace.md:70` cite `docs/rapports/cartographie-2026-09-29.md`, absent de
la copie sparse (dossier interdit au lot, jamais extrait). Témoin : la même copie sparse de la tête **sans** la série
(`tmp/tete0`) rend le même verdict, la même violation seule (`sorties/final-xtask-temoin-tete.txt`) ; les quatre
fichiers lus par S-G9 (modèle de menace, registre 08, annexes A et B) ne sont pas touchés par la série. Le vert de
S-G9 se constate sur l'arbre complet (orchestrateur).

**Matrice 3.10 à 3.13** (suite s2bis par le vérificateur du job, `-X dev -W error`, `PYTHONDEVMODE=1`,
`PYTHONWARNINGS=error` pour les sous-processus) :

| interpréteur | verdict | « Exception ignored » | « Warning » |
|---|---|---|---|
| Python 3.10.20 | conforme, Ran = 357, code 0 | 0 | 0 |
| Python 3.11.15 | conforme, Ran = 357, code 0 | 0 | 0 |
| Python 3.12.3 | conforme, Ran = 357, code 0 | 0 | 0 |
| Python 3.13.14 | conforme, Ran = 357, code 0 | 0 | 0 |

Campagnes de mutants (§1) : 10 campagnes finales, 105 mutants (12 + 9 + 10 + 11 + 17 + 11 + 10 + 9 + 12, et 4 de
vérification des fermetures de fait), 105 tués par la commande du job, 0 vivant, 0 FATAL, 0 équivalent retenu ;
témoin VIVANT avant chacune ; durée par exécution 40 à 101 s (sous la borne de 300 s) ; union des tests en échec relue
par campagne : aucun échec étranger au diff (`outils/echecs.py`).

## 6. Écarts (déclarés)

- **E-0** : effort `high` demandé par le lanceur ; la fiche `shogen-worker` et CLAUDE.md §7 disent `max` explicite
  pour un worker. Travail conduit sans réduction de périmètre.
- **E-1** (21:58 UTC) : un heredoc non quoté a substitué les accents graves d'un texte de METRIQUES (commandes `.py`,
  `.yml`… lancées par bash, introuvables, sans effet) ; fichier restauré depuis l'instantané 0 et réécrit par script en
  heredoc quoté ; règle tenue ensuite (heredocs toujours quotés).
- **E-2** : la première campagne de DT6-a tournait sur une copie sans `s2-harness/tests` ni FORMAT (tests en échec
  pour une autre cause que le mutant) : arrêtée, ne compte pas ; témoin T00 ajouté à l'outil, campagne rejouée.
- **E-3** : redémarrage du conteneur vers 22:55 UTC (cause extérieure) : campagnes e et f en cours perdues, ne comptent
  pas ; reprise depuis `NOTES.md` (22:56:10 UTC), sans perte de fichier.
- **E-4** : 18 lignes ajoutées de plus de 120 caractères dans les états e à i (et des continuations peu lisibles),
  vues à la reprise : remises en page (29 remplacements), AST contrôlé égal hors 4 variables intermédiaires nommées ;
  les campagnes en cours (e, f) arrêtées et rejouées.
- **E-5** : les campagnes de a, b, c avaient tourné avant des retouches de mise en page (docstrings, tests reformés) et
  celle de d sur une copie de la copie de travail où DT6-e avançait : toutes rejouées sur les instantanés finaux
  (`*-final`) ; les premières restent en historique.
- **E-6** : la première forme du mutant H06 laissait un `try` sans `except` (erreur de syntaxe, tué par `test_fitness`,
  non valide) : refaite (refus de l'écrivain propagé sans conversion) ; contrôle de syntaxe ajouté pour tous les
  mutants ; campagne h rejouée entière.
- **E-7** : une première forme de F08 (dt6f), jugée équivalente avant le redémarrage, a été remplacée par la forme
  actuelle (motif `[0-9.]+`, zéros de tête admis) ; sa forme exacte n'était pas consignée dans `NOTES.md` et le
  transcript (`.jsonl`) n'est pas lu : non restituable.
- **E-8** : défaut de la première écriture de DT6-e, trouvé en relecture du générateur (23:34 UTC) : `status.etat`
  lisait `e["ws"]` d'une `sante` (KeyError sur une `sante` sans `ws`, régression contre I-3 de DT6-d) et `chrony`
  admettait `code` faux (False == 0). Corrigé dans DT6-e avec ses tests (rouge FAIL 2 / ERROR 0, puis vert), propagé
  aux états suivants ; mutants E16 et E17 ajoutés ; campagnes e, f, g, i, V rejouées sur les instantanés corrigés.
- **E-9** : la section DT6-b de METRIQUES décrivait le rouge d'avant une retouche du test (FAIL 4, trois refus, 0,57 s) ;
  corrigée sur le rouge final (FAIL 5, quatre refus, 0,48 s).
- **E-10** : disque partagé tombé à 222 Mio entre 23:17 et 23:21 UTC (processus d'autres agents) ; aucun échec
  étranger aux diffs dans les campagnes (union des tests en échec relue, `outils/echecs.py`).
- **E-11** : la machine est partagée (deux autres agents) ; au plus deux processus lourds du lot à la fois, tenus par
  les chaînes de campagnes (une campagne à la fois par chaîne).
- **E-12** (relecture finale du générateur, 23:39 à 23:43 UTC) : abrégé du sha256 de `doc/chronyc.adoc` faux
  (`dc955e0f…c7a8`, quatre caractères pris au milieu ; juste : `dc955e0f…c5a7`) dans la docstring de `test_status` et
  au FORMAT §13.3 ; citation « ADR-0029 §2.3, l.83 » au §17.2 (la l.83 est au §2.1) ; paragraphe du §17.4 coupé en
  ligne courte. Corrigés (ajout daté DETTES-T6 porté à 23:42:21 UTC) ; les campagnes en cours ont été arrêtées et
  relancées après (les interrompues ne comptent pas).
- **E-13** : le correctif de 23:36 UTC laissait dans la docstring de `status.chrony` une ligne de 137 caractères (vue
  à la régénération des diffs, 00:15 UTC), remise en page à 00:15:59 UTC, après les campagnes e-final à V : elles ont
  tourné sur des copies qui ne diffèrent de l'état final que par cette docstring (AST égal hors docstrings, contrôlé
  sur la copie de h-final) ; non rejouées. La suite finale (matrice 3.10 à 3.13, job) tourne sur le texte final.

## 7. Journal de provenance (G1)

Sources lues (niveau ; empreinte au commit de la tête quand c'est une pièce du dépôt) :

- [lu] brief et `ITEMS-ANNEXE-B.md` (sha256 en tête) ; lignes d'annexe B relues à la source
  (`docs/adr-0028/ANNEXE-B-items.md`, sha256 à 094fa5d `709e146c69241cc5…`) : l.1010, 1047, 1051, 1057, 1085,
  1099-1117, 1152, 1158, 1160, 1165, 1295-1350 (B.84), 1331, 1336, 1390-1420, 1470-1557 (B.87 à B.91).
- [lu] `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md` entier (`d9160d3ed514a55c…`) ; `PROPOSITION.md` §2,
  l.111-373 (`0cdf84c25092101a…`) ; FORMAT entier (`e1277123aaacac65…`, identique de 50ca52d à 094fa5d) ;
  `METRIQUES-S2BIS.md` (`95198663785a07fc…`) ; ADR-0029 (`32a598931dd35c91…`) : titres de section, l.82, l.83,
  l.108, l.196, l.239, l.248.
- [lu] revues : `revue-p2a` (BRIEF, G2 entière, contre-contrôle l.130-175 et 255-310), `revue-p2b` (G2 l.200-280,
  RAPPORT-GENERATEUR l.125-182), `revue-p1c` (RAPPORT-CORRECTIONS l.170-200, contre-contrôle l.95-115), `revue-p1b`
  G2 l.44 et l.52 (`b57c676c4153d9d4…` : I-B1, O-3).
- [lu] code en entier : `s2bis/shogen_s2bis/collecte/` (journal, status, decodeurs, asn, dns, sante, secondaire, entree,
  boucle, config, lecture, http, tetes) ; `s2bis/tests/__init__.py` ; `gates.yml` (jobs unittest) ; runner l.1-40, l.555-625 et
  l.642-655 (gabarit K, leurres L-10, L-12, L-19, L-33) ; `enforcement/verdict-suite-s2.py` l.1-80 et `etapes`,
  `lignes_du_job`, `lancer` ; `enforcement/docs-sha256sums.py` l.1-40 ; `xtask/src/lib.rs` (étapes cargo de `verify`).
- [lu] chrony, source officielle : `https://chrony-project.org/releases/chrony-4.6.1.tar.gz`, sha256
  `571ff73fbf0ae3097f0604eca2e00b1d8bb2e91affe1a3494785ff21d6199c5c` (signature `chrony-4.6.1-tar-gz-asc.txt` non
  vérifiée, L-5) ; `client.c` `7e515f338655a34240a4a1238beab3eae1df85297a806f3984fbf30d6cfb2d6d`
  (`process_cmd_tracking` l.2173-2222 : formats l.2197-2206 ; `print_report` l.1645-1880 : `%O` l.1745-1750, `%L`
  l.1755-1775 ; aucun `setlocale`) ; `util.c` `4a11cb32e95540f31352c856839a1e5c40d54703ad106ae50cae217c74e9faf4` ;
  `doc/chronyc.adoc` `dc955e0f34af005fae7824d1896b411e6bb1943c7a8885578461c0c1e36ec5a7` (tracking l.142-260, exemple
  l.147-159 copié en fixture : sha256 égal, `07d2a4723391ddde2971acef0f753ca185ab751011ddc4489bd646d008bd934b` ;
  formule de la borne). `https://chrony-project.org/releases/chrony-4.9.tar.gz`, sha256
  `4924c6f530105bcd5b9e9e33c48a2ae1bfd889222c8480bc41601110efc864d0` : `process_cmd_tracking` et
  `UTI_TimespecToString` identiques à 4.6.1 ; `print_report` : seul ajout, largeur « * », inutilisée par `tracking`.

Mesures (toutes refaites dans ce lot, réseau coupé) : voir `NOTES.md` (sondes `travail/sondes/s1_cycle.py`,
`s2_saut.py` : cycle derrière 2^k feuilles partagées, 0,99 s à k = 18 et 3,78 s à k = 20 ; chaîne de 1 Mio partagée
1 000 fois admise en 10,2 s, pic de 2 Gio ; MemoryError de `status` en 3,6 s sous 512 Mio, refus nommé en 0,15 s ;
1E+199999 décodé en 0,48 s sous le mutant K1-03) ; sorties des rouges `sorties/rouge-*.txt`, des campagnes
`sorties/mutants-*.{log,json}`, des vérifications `sorties/final-*.txt`.

Outils du lot (dossier `outils/`) : `iso.sh` (isolement), `mutants.py` (campagnes), `chaine.sh` (enchaînement, une
campagne à la fois par chaîne), `copie_mut_etat.sh`, `rouge.sh`, `rouge_mutant.py`, `bilan.py`, `series.sh`
(régénération des diffs), `diff_etapes.sh`, `verifier_serie.sh`, `verifier_tete.sh`, `compte.py`, `largeur.py`
(largeur, `TODO`/`FIXME`, octet 92, fins blanches), `nb_tests.py`, `echecs.py`, `table_serie.py`, `copie_tete.sh`
(copie neuve à la tête), `verif_jobs.sh` (vérifications finales) ; `travail/largeur/` (remise en page et contrôle
d'AST) ; `travail/metriques/` (sections de METRIQUES).

## 8. Items à former

Aucun. Deux précisions d'items existants sont proposées (§2, fin) : SHOGEN-S2BIS-RB3-DEGRADATIONS-1 couvre aussi D-3 ;
SHOGEN-S2BIS-CONFIG-PRODUCTION-1 scelle la commande `chronyc -n tracking`.

## 9. Fichiers livrés (dossier du lot)

- `diffs/DT6-a.diff` à `diffs/DT6-j.diff` (à appliquer dans l'ordre ; base 50ca52d, applicables sur 094fa5d) ;
  `SHA256SUMS` (diffs, rapport, notes) ; `NOTES.md` (reprise possible depuis lui seul) ; ce rapport.
- Pièces de travail (non livrées, gardées pour la relecture) : `travail/etats/` (instantanés 0, a à j), `travail/mutants/`
  (spécifications, dont `dt6e-avant-correctif.py` et `dt6h-premier.py`), `sorties/` (rouges, campagnes, vérifications
  finales), `outils/`.

## 10. Phase 2 (ajout daté du 2026-10-10 02:52:05 UTC, `date -u`) : corrections de la G2 et recalage sur la tête

Demande du coordinateur (après l'adjudication de la G2, `ADJUDICATION.md`, ajout daté du 2026-10-10 01:14:58 UTC,
sha256 du fichier `ae2e111f…eb01` ; `g2/RAPPORT-G2.md` `6c2f62dc…97da` lu en entier ; `g2/corrections/G2-corrections.diff`
`2b6d931a…94ab` lu en entier). Heure lue au début : 2026-10-10 01:15:07 UTC ; `git log -1` au début : `3a41ff9`
(DETTES-T5 DT5-8).

### 10.1 Réponse aux corrections C-1 à C-10 (relues une à une, toutes acceptées dans la forme du réviseur)

- **C-1** (code) : juste. Une `sante` dont `ws` n'est pas entier n'entre plus en clé de `en_cours` ; elle reste la
  dernière santé (ligne `disque`), comme avant. Aucun autre lecteur de `en_cours` (le marqueur ne cherche qu'un `ws`
  entier). Rouge reproduit (FAIL : `TypeError` rendu par `sans_attente`).
- **C-2** (code) : juste ; `len(range(...))` se calcule sans allouer. Rouge reproduit (FAIL : `RefusStatus` non levé
  pour 46 081 fenêtres hors grille).
- **C-3** (textes) : juste : avec `stderr=subprocess.STDOUT`, les deux sorties partagent un tube et s'y suivent dans
  l'ordre des écritures ; ma première phrase (« suivie de ») était fausse.
- **C-4** : juste (« adoptée » après l'adjudication).
- **C-5, C-6, C-7, C-8, C-9** (tests) : justes ; chacun éprouve une ligne que la série a écrite sans test. Contrôle
  propre du générateur : mes mutants K06 à K13 (formes indépendantes, mêmes lignes) **vivent** sur l'état DT6-j
  (8/8, commande du job) et sont **tués** sur l'état DT6-k (8/8), chacun par le test que la correction ajoute.
- **C-10** (texte) : juste (le motif `ligne coupée` peut être passager pendant la collecte ; mesure du réviseur).
- Précisions d'items de l'adjudication (STATUS-RETENTION-1 ; « §16.2 » lu « §17.2 » pour RB3-DEGRADATIONS-1) :
  d'accord.

### 10.2 Diff DT6-k

`G2-corrections.diff` appliqué après DT6-j (`git apply --check`, puis `git apply`) : R-25 **+49** (`.py`), un seul
diff suffit. Ajouts du générateur : l'ajout daté DETTES-T6 du FORMAT nomme le diff DT6-k (« porte les corrections C-1
à C-10 de la G2 du lot (§13.3, §17.2, §17.4) ») et prend l'heure de cette écriture, **2026-10-10 01:18:37 UTC** ;
section METRIQUES « DT6-k ». Aucun test ajouté (cas dans des tests existants).

Rouges (tests d'abord) : C-1 et C-2, tests de DT6-k sur le `status.py` de DT6-j : FAIL 2, ERROR 0 ; C-5 à C-9, chaque
test sur le mutant qu'il vise (K06 à K13) : FAIL 1, ERROR 0 chacun (`sorties/rouge-DT6-k-*.txt`).

Mutants (`travail/mutants/dt6k.py`, sha256 `9adf809e5449…`) : **13 mutants, 13 tués** par la commande du job, 0
vivant, 0 FATAL, témoin VIVANT (`sorties/mutants-DT6-k.json`) : C-1 défait, dernière santé retenue pour un `ws` entier
seulement, C-2 défait, borne large, compte d'une fenêtre de moins, et K06 à K13 ci-dessus. Sur l'état DT6-j, K06 à
K13 : 8 vivants (`sorties/mutants-DT6-k-avant.json`).

### 10.3 Recalage de la série sur la tête

Têtes lues : `3a41ff9` (DT5-8, début de la phase), puis la chaîne DETTES-T5 jusqu'à `ada4737` (DT5-21, 02:17:46 UTC :
plancher s2bis 342), `0838597` (DT5-22), **`14597a6` (DT5-23, 02:27:19 UTC, dernier diff de DETTES-T5)**, `ba5ea95`
(versement DETTES-T5), puis trois commits du lot FUZZ (`6e01772`, `4d34923`, **`39718f4`**, tête relue au rendu,
02:50:19 UTC). Entre `094fa5d` et `39718f4`, DETTES-T5 touche `s2bis/tests/__init__.py` et `s2bis/tests/test_garde.py`
(que la série ne touche pas) et la ligne du plancher s2bis de `gates.yml` (341 → 342) ; ni le FORMAT ni METRIQUES ;
les commits FUZZ ne touchent aucun chemin de la série.

Méthode (`outils/recaler.py`) : instantanés neufs `travail/etats2/0` (tête, `git archive` en lecture seule) puis a à k ;
chaque fichier changé par la série est, à la tête, celui de la base de la série (sinon arrêt) et prend l'état de la
série ; `gates.yml` : celui de la tête, plancher s2bis = plancher de l'état + **delta (+1)**, bloc de DT6-j inséré à la
même ancre ; METRIQUES : lignes « Suite : N tests ; plancher du job : N » des sections DT6 portées à N + 1. Diffs
régénérés entre états successifs (`outils/series2.sh`) ; essai à blanc à delta 0 sur `1122ba6` : diffs identiques à
ceux de la phase 1 hors lignes `index` et en-têtes de bloc.

Série recalée rendue (`diffs/`, 11 diffs ; R-25 inchangé ; `largeur.py` : 0 signalement ; suite finale 358) :

| diff | sha256 | R-25 | plancher s2bis (état) |
|---|---|---|---|
| DT6-a | `20347c080642c57b8915cfc1a4f532666592f2d2fb0d8dc78e97e7fa8ea13c40` | +77 | 344 |
| DT6-b | `991f528cf136d27d4cd23383137b20cc5fea91201c7b828b4b8cc96d55ff799b` | +26 | 345 |
| DT6-c | `32c601d3c6ed9e93b8299ba27f8f65af01c457abbc9993f44130559d932cd054` | +71 | 347 |
| DT6-d | `631e434fc0f6095f50bfb0950d7a1cbcf31016737a3d4401b99fe6eb2d5e7dae` | +107 | 351 |
| DT6-e | `c945ffc609ddac13c349b7c1a09131b86fee03db383592bb1319abc20cfa5c60` | +144 | 353 |
| DT6-f | `bb2b5bfcc44e18d6703574e5a6f05bf94c2bb3efe81586f8b0e6f144ef20d240` | +67 | 354 |
| DT6-g | `59c6dbacbc2961aa7cb5eee32d6c9e2d0c3ec658ccd710ff596fe075e55a8094` | +71 | 355 |
| DT6-h | `17aee755e66b2b751b4a8da83970cbf60efad48601c9fd42f979271e1d14c71e` | +47 | 356 |
| DT6-i | `05953f10460eefc7673a082635e957f0d523aa5690ae979099fa47a12ef0260b` | +46 | 358 |
| DT6-j | `a78dbea2dc0a385cea35627ca217bf83f96d0bdb84ae94e23d9d471a7a6b30c8` | +4 | 358 |
| DT6-k | `1c521fe92cb6a3ef8c99c3b3abf398c09a4715c2e9e04c28267a02f9be451406` | +49 | 358 |

`git apply --check` puis application, dans l'ordre : sur `ada4737`, sur `14597a6` et sur `39718f4` : sortie 0 ; la copie
obtenue est égale octet pour octet aux instantanés recalés (s2bis/, FORMAT, METRIQUES, gates.yml). Diffs identiques
sur les trois têtes (aucun chemin de la série ne change entre elles). Version de la phase 1 gardée en
`sorties/diffs-phase1/` (avec son SHA256SUMS).

### 10.4 Vérifications sur la tête finale, série DT6-a à DT6-k appliquée

Sur **`14597a6` (DT5-23)**, copie neuve creuse, série DT6-a à DT6-k appliquée (`sorties/p2-14597a6/`) ; réseau coupé :

| vérification | résultat |
|---|---|
| runner | `verdict-suite-s2 : 137 ok, 0 échec` |
| job s2bis (`--plancher 358`) | `conforme (code 0, résumé final, aucun saut, Ran = 358)` |
| ligne s2bis à chaque état recalé | a 344, b 345, c 347, d 351, e 353, f 354, g 355, h 356, i 358, j 358, k 358 : chacun `conforme`, Ran = plancher |
| job S2 (`--egal`) | `conforme (…, sauts nommant SHOGEN_S2_CAMPAGNE_CONTROL, Ran = 419)` |
| jobs sim-bis, calib-actifs, controle | conformes, Ran = 279, 65, 36 |
| g1 : `runners-epingles.py`, `workflows-yaml` (cas et arbre), `lint-model-pinning` (cas et arbre), `journaux-modele`, `docs-sha256sums` | conformes (16 cas YAML, 7 workflows, PyYAML 6.0.1 ; 227 cas R-1 ; 34 SHA256SUMS) |
| g5 : cas du crochet (`run-fixtures-hooks.sh`) | `hooks : 57 ok, 0 échec` |
| matrice 3.10.20, 3.11.15, 3.12.3, 3.13.14 (`-X dev -W error`, `PYTHONDEVMODE=1`, `PYTHONWARNINGS=error`) | conforme, Ran = 358 chacune ; 0 « Exception ignored », 0 « warning » |
| `cargo --locked xtask verify` | S-G1 à S-G8 VERT ; S-G9 ROUGE (1 violation, `docs/17-modele-de-menace.md:70` → `docs/rapports/`, absent de la copie creuse : artefact admis par l'adjudication) ; fmt, no_std, clippy VERT |
| `cargo --locked test` | 26 lignes `test result: ok.`, 259 tests |
| mutants DT6-k sur l'état final recalé | 13/13 tués, témoin VIVANT, 0 FATAL |

Sur **`39718f4`** (tête au rendu) : série appliquée et égale aux instantanés ; runner 137 ok ; s2bis conforme Ran = 358 ;
controle conforme Ran = 36 ; xtask : même verdict (S-G9 seule ROUGE, même violation) ; `cargo test` : 27 lignes
`test result: ok.`, 265 tests (tests du lot FUZZ). Même passage sur `ada4737` (DT5-21) : identique
(`sorties/p2-ada4737/`).

Non lancés, déclarés : l'étape `git grep` de g5 (recherche dans tout l'arbre, interdite au lot ; les lignes ajoutées
de la série sont contrôlées par `largeur.py` : aucun `TODO`/`FIXME`) et le job g3-secrets (balayage de l'historique
entier). Écarts de la phase 2 : **E-14**, `tee /dev/stderr` dans `series2.sh` a mêlé des octets nuls au journal
`final2-series.txt` (compte et largeurs refaits à part : identiques) ; **E-15**, deux lignes de NOTES portaient une
heure ou un chiffre faux (« 01:33 » pour 01:30 ; « 6,5 Gio » pour 7,3) : corrigés aussitôt.

## 11. Phase 3 (ajout daté du 2026-10-10 04:26:48 UTC, `date -u`) : réserves R-1 à R-7 du contre-contrôle

Demande du coordinateur (contre-contrôle neuf : CONFORME-AVEC-RÉSERVES, R-1 à R-7 ; adjudication : dernier ajout
daté de `ADJUDICATION.md`, 03:52:42 UTC, sha256 du fichier `384a3f60…6386` ; `g2/cc/RAPPORT-CC.md` `d06bb58f…43ff`, lu
en entier). Heure lue au début : 2026-10-10 03:52:55 UTC ; `git log -1` au début : `0e03a9f` (DETTES-T5, versement
de DT5-24 et DT5-25, 03:51:31 UTC). Un seul processus lourd à la fois ; `df -h /` avant chaque compilation (6,8 à
7,7 Go libres).

### 11.1 DT6-l à DT6-r : les sept diffs du contre-contrôleur, repris octet pour octet

| diff | source (`g2/cc/propose/`) | sha256 | R-25 |
|---|---|---|---|
| DT6-l | `R-1.diff` | `6eb57a49fee9b498b4ab2d8655252f0e49d5eec2ac7ed8c95d6195ca2779b531` | +17 |
| DT6-m | `R-2.diff` | `ec0fbdb6e59bbf97fa1955e1d50c44cb769eb8a2bd48187a7bc6c720a0aff808` | +10 |
| DT6-n | `R-3.diff` | `03123c167e9a35b2f04032fa5326dda5149cd71ef6a5b15ef5da9ebd83bea7db` | +5 |
| DT6-o | `R-4.diff` | `94fdf8aedf9855a099260380a8e346834a846310d3d6270a657b8d676b031db4` | +3 |
| DT6-p | `R-5.diff` | `4c0238a4dd72cf9228688b480d79856cfc6a83d7164138ff56781ebfb599f719` | +3 |
| DT6-q | `R-6.diff` | `9005b69debdc80dbd4a0ea2d7c4a62e64cdbd87570d8f95ecba2c5d18f9b22bf` | +1 |
| DT6-r | `R-metriques.diff` | `358d0396ee93298ec30fe35008782f6598f619457a00f7f3888e5d01d31a03eb` | +0 (`.md` +28) |

`cmp` : identiques, 7 sur 7 ; sha256 égaux aux préfixes du coordinateur et aux lignes de `g2/cc/SHA256SUMS`.
`largeur.py` : aucune ligne de plus de 120 caractères, aucun TODO/FIXME nu, aucun octet 92. R-25 de la série a à r :
+748 (a à k +709, l à r +39), chaque diff sous 200.

### 11.2 Réponse aux diffs (une ligne chacun)

- **DT6-l (R-1, code et test)** : juste. La borne `max(len(x[1]) for x in (o, r, d)) > journal.CHIFFRES` précède le
  seul `int()` de `status` sur un texte de longueur libre ; 640 est la plus petite limite non nulle de l'interpréteur
  (`sys.int_info.str_digits_check_threshold`), donc une partie entière d'au plus 640 chiffres se convertit sous tout
  réglage, et `%.9f` d'un double en écrit 309 au plus (19 pour chrony, O-4 du contre-contrôle) : aucune sortie réelle
  n'est retirée ; des deux cas du test (4 301 chiffres sous la limite courante ; 641 sous 640, limite rendue par
  `addCleanup`), le premier est rouge sur le code d'avant (rejoué, §11.4), le second aussi (sonde du §11.3 : 641
  chiffres sous 640, `ValueError` à l'état k ; R1-M2 tué par lui). Borne exacte non figée : O-6.
- **DT6-m (R-2, test)** : juste. `bord` mesure la ligne à `z` vide, d'où une ligne de LIMITE + 1 octets (coupée) puis
  de LIMITE octets (lue ; `len(lu)` le vérifie sans dépendre du calcul) : la borne de `readline(LIMITE)` est tenue des
  deux côtés.
- **DT6-n (R-3, test)** : juste. Fenêtre 22 : trois témoins en `delai` (D-4), `d3` null, dernier relevé lisible
  420 s avant (fenêtre 15 ; D-3) ; l'attendu `["D-3", "D-4"]` est l'ordre que `lire_resume` exige des autres
  (`x[1] == sorted(set(x[1]))`) : un résumé non trié serait refusé (`RESUME/champs`).
- **DT6-o (R-4, test)** : juste. `json.dumps(0)` écrit 1 octet, `_octets(0)` doit valoir 1 (`max(v.bit_length(), 1)`) ;
  `0` et `False` restent deux éléments distincts du tuple.
- **DT6-p (R-5, test)** : juste. Premiers champs `""` et `" "` : None ; `(" | x", "64501 | y")` : l'`IndexError` du
  premier TXT est rattrapée, la réponse suivante est lue ; rouge en ERROR (le mutant lève), forme assumée par le
  contre-contrôle (E-5) : rattraper l'exception dans le test masquerait le défaut.
- **DT6-q (R-6, test)** : juste. Code −9 (processus tué par un signal, convention de `subprocess`) : relevé illisible,
  la fenêtre prend D-3 (dernier relevé lisible 120 s avant elle) ; le code 1 reste figé par la première variante
  (lisible, elle serait valide). La docstring du test dit encore « code 1 ou faux », le commentaire de la ligne nomme
  le code négatif : sans correction.
- **DT6-r (R-metriques)** : juste, et exacte sur la tête (chiffres recomptés : §11.6) ; aucune section ajoutée. Deux
  précisions sans correction : son titre nomme DT6-l seul, alors que l'adjudication verse R-1 à R-6 en DT6-l à DT6-q
  (O-5) ; « 1 vivant équivalent » s'entend sur le domaine du FORMAT (O-6).
- **R-7 (texte, sans diff)** : d'accord ; la phrase du §2 pour STATUS-QUEUES-1 se verse avec « en dernière ligne du
  rapport local (le compte à quorum suit, avec `--depot` : FORMAT §17.6) » (§17, point 6 « Compte à quorum », relu) et
  cite R-1, R-2 ; CHRONYC-FORMAT-1 cite R-1, R-3, R-6 ; CANONIQUE-OCTETS-1, R-4 ; ASN-LECTURE-1, R-5.

### 11.3 R-1, défaut de DT6-e : reste-t-il des défauts de la même classe ?

Classe (R-1, comme C-1) : une ligne JSON valide hors FORMAT fait lever à `status` ou à `resume` autre chose qu'un refus
nommé (`RefusStatus`, `ErreurJournal`, `OSError`, seuls rattrapés par `entree._status`) : trace Python, sortie 1,
contre I-3 de STATUS-QUEUES-1. **Il n'en reste aucun** dans les lecteurs de nombres de `status` et de `resume`. Lecture
du `status.py` final :

- `fichiers` : `int(k)` d'un nom de fichier (NAME_MAX, 255 octets : 233 chiffres au plus, sous la limite minimale de
  640), dans un `except ValueError`, comme le `strptime` du jour (l'an 0 y est refusé).
- `enregistrements` (journal) et `lire_resume` (résumés du dépôt) : le seul décodage d'un texte en nombre est
  `json.loads`, dont l'erreur de limite est une `ValueError` rattrapée (« ligne illisible » ; `RESUME/forme`) ;
  `lire_resume` refuse en outre par `canonique` tout entier de plus de 640 chiffres et tout flottant.
- `_au_dela`, `juger`, `trois`, `etat`, `quorum` : comparaisons et arithmétique d'entiers déjà décodés, aucune
  conversion de texte ; `juger` rattrape `KeyError`, `TypeError`, `AttributeError` ; `heure`, `strate` et
  `journal.jour` ne reçoivent que des `ws` bornés (grille : de la veille du premier jour nommé, an 1 au plus tôt, à la
  fin du dernier, an 9999 au plus tard, par `_au_dela` ; résumés : jour de leur nom, dans la grille) ;
  `len(range(...))` de C-2 : 5,3 milliards au plus, sous `sys.maxsize` d'un hôte 64 bits.
- `rapport` : `str()` d'entiers que `json.loads` a décodés sous la même limite (même nombre de chiffres) : ne lève pas.
- `chrony` : `int()` de la partie entière, seul `int()` sur un texte non borné (R-1, DT6-l) ; partie décimale de 9
  chiffres.

Sonde (`outils/sonde_classe.py`, `0f13f1816f0b…7a43`) : 783 cas, soit 16 nombres extrêmes (701 et 4 301 chiffres,
des deux signes ; 5 001 chiffres ; ±1e999, NaN, ±Infinity, 1.5, -0, 0, -1, 640 et 641 chiffres) dans 15 champs
numériques (`ws` et `seq` de `sante` et de `marqueur`, `suivante` d'une ouverture seule, `d2`, `d4`, `d5`, `disque`,
`d3.code`, `ws` d'un résumé d'un autre observateur au dépôt), et les parties entières de 19 à 5 000 chiffres des trois
valeurs de chrony,
sous les limites 640, 4 300 et 0 ; trois appels par cas (`rapport`, `rapport` avec dépôt, `resumes`). État DT6-k : 18
cas tracés, tous `ValueError` de `chrony` (partie entière au-delà de la limite, dans chacune des trois valeurs) ; état
final a à r : **0** (`sorties/p3-sonde-k.json` `2f56c6fe…c789`, `p3-sonde-final.json` `f3efbf24…13e0`). Non-vacuité
relue au texte du rapport (`outils/sonde_non_vide.py`, `sorties/p3-sonde-non-vide.txt`). Hors classe : O-7.

### 11.4 Rouges rejoués sur l'état DT6-k

`outils/rouge_reserve.py` (`b362cdc6…8633`) : copie de `s2bis/` de l'état DT6-k recalé (`travail/etats2/k`, égal à la
tête `0e03a9f` + DT6-a à DT6-k, §11.5), diff appliqué (`git apply --check` puis `git apply`), mutant du contre-contrôle
dans sa forme (`g2/cc/mutants/cc.py`, `7c0390fe…c5be`), `python3.12 -B -X dev -W error -m unittest <module>`, réseau
coupé (`sorties/p3-rouge-*.txt`).

| réserve | rouge | test en échec |
|---|---|---|
| R-1 : DT6-l, `status.py` remis à l'état k | FAIL 1, ERROR 0 : `'ValueError' != "disque : non relevé ({'libre': 13})"` | `test_ligne_hors_format_jamais_une_trace` |
| R-2 : DT6-m sur M01 (`readline(LIMITE + 1)`) | FAIL 1, ERROR 0 | `test_fichiers_arretes_avant_leur_fin_nommes` |
| R-3 : DT6-n sur M03 (codes non triés) | FAIL 1, ERROR 0 : `['D-4', 'D-3']` pour `['D-3', 'D-4']` | `test_d3_jugee_sur_la_sortie_gelee` |
| R-4 : DT6-o sur M07 (`_octets(0)` = 0) | FAIL 1, ERROR 0 : `(0, 0, 1)` | `test_octets_comptes_par_occurrence_avant_le_serialiseur` |
| R-5 : DT6-p sur M10 (`except ValueError` seul) | FAIL 0, ERROR 1 : `IndexError` | `test_cymru_premier_txt_lisible_forme_de_s2` |
| R-6 : DT6-q sur M12 (`code > 0` seul refusé) | FAIL 1, ERROR 0 | `test_d3_jugee_sur_la_sortie_gelee` |

Contrôles : chaque mutant seul sur l'état k, module OK (vivant, comme au §6.1 du contre-contrôle) ; chaque diff seul,
module OK.

### 11.5 Vert de la série complète, DT6-a à DT6-r, sur la tête `0e03a9f`

Copie neuve creuse (`outils/copie_tete3.sh`, `094d846b…54a3`) : DT6-a à DT6-k appliqués (`--check` puis application),
`s2bis/`, FORMAT et METRIQUES égaux à `travail/etats2/k` ; DT6-l à DT6-r appliqués, sortie 0. Réseau coupé ;
`outils/verif_jobs3.sh` (`9177bb2c…d003`), `sorties/p3-*.txt`. Le `python3` de cet hôte est 3.11.15 ; les étapes du job
se lancent avec un `python3` de tête de PATH lié à `/usr/bin/python3.12` (3.12.3, celui de l'image ubuntu-24.04).

| vérification | résultat |
|---|---|
| runner (étape du job, texte exact) | `verdict-suite-s2 : 137 ok, 0 échec` |
| job s2bis : bloc `run` de `gates.yml` l.289-291 de la copie, texte exact (`tmp/job-s2bis.sh`, `38561d49…1f17`), `bash --noprofile --norc -eo pipefail` | `Python 3.12.3` ; `Ran 358 tests` ; `verdict-suite-s2 : conforme (code 0, résumé final, aucun saut, Ran = 358)` ; sortie 0 |
| matrice 3.10.20, 3.11.15, 3.12.3, 3.13.14 (`-X dev -W error`, `PYTHONDEVMODE=1`, `PYTHONWARNINGS=error`) | conforme, Ran = 358 chacune ; 0 « Exception ignored », 0 « warning » |
| `docs-sha256sums` | conforme (38 SHA256SUMS) |
| `cargo --locked xtask verify` (cible par défaut) | lignes VERDICT : 8 × `VERDICT : VERT (0 violation(s))` (S-G1 à S-G8) ; `VERDICT : ROUGE (1 violation(s))` (S-G9 : `docs/17-modele-de-menace.md:70` → `docs/rapports/`, absent de la copie creuse, artefact admis) ; `=== VERDICT GLOBAL : ROUGE — l'intégration s'arrête (ADR-0013, point 1) ===` ; fmt, no_std, clippy VERT |
| `cargo --locked test`, cible par défaut (`target/` de la copie, règle I-1) | 28 lignes `test result: ok.`, 269 tests, 0 échec, 0 ignoré ; sortie 0 |
| mutants des réserves, commande du job (§11.6) | 8 tués, 1 vivant (R1-M4), 0 FATAL ; témoin VIVANT |

### 11.6 METRIQUES : la section de DT6-r est exacte sur la tête

Recomptés sur l'état final : `status.py` 277 lignes ; `test_status.py` 556 lignes, 24 tests ; `test_journal.py` 357,
17 ; `test_asn.py` 152, 6 ; suite 358 (Ran du job) ; aucun test ajouté ; rouges : §11.4 ; FORMAT §17.2 (« dans la
forme du §13.3 ») et §13.3 (`%.9f`) relus. Mutants rejoués par la commande du job (`outils/mutants.py`, spécification
`outils/spec_cc_p3.py` `33e21241…6e96`, qui reprend `g2/cc/mutants/reserves.py` `5a3924b6…a563` tel quel ; borne de
300 s ; python3.12 ; réseau coupé) sur la copie de la tête : témoin VIVANT ; M01, M03, M07, M10, M12, R1-M1 (R-1
défait), R1-M2 (borne 4 300), R1-M3 (borne 641) TUÉS, chacun par le test visé ; R1-M4 (borne 639) VIVANT ; 0 FATAL
(`sorties/p3-mutants-reserves.json`, `cff9c8ce…6667`). Copie restaurée, égale à l'état final (`travail/etats3/r`).

### 11.7 Observations (rendues à l'orchestrateur ; aucun diff ajouté à la série)

- **O-5** Titre de la section METRIQUES de DT6-r : « DT6-l (2026-10-10) : réserves R-1 à R-6… » ; avec le découpage de
  l'adjudication, il se lirait « DT6-l à DT6-q (2026-10-10) : réserves R-1 à R-6… » (une ligne, à décider au versement).
- **O-6** R1-M4 n'est équivalent que sur le domaine du FORMAT : une partie entière de 640 chiffres exactement (hors
  FORMAT) le distingue (sonde de non-vacuité, sous la limite 640 : 640 chiffres lus, borne énorme, D-3 ; 641
  illisibles, fenêtre valide sur le relevé de 60 s ; R1-M4 rend aussi les 640 illisibles). Essai, rapport seul
  (`outils/r1m4_essai.py`, `7c0162a6…5319`) : deux lignes de plus dans `test_ligne_hors_format_jamais_une_trace`,
  `d3` à `journal.CHIFFRES` chiffres et `self.assertIsNotNone(status.chrony(d3))` sous la limite 640, figent la borne
  exacte : vert sur le code, FAIL 1 sur R1-M4 et sur R1-M3. À former si l'orchestrateur veut la borne exacte, comme
  R-2 pour LIMITE.
- **O-7** Hors classe, sans trace : sous la limite 640, une ligne qui porte un entier de 641 à 4 300 chiffres est
  « ligne illisible » (fichier arrêté et nommé) ; sous la limite par défaut, elle est lue. Le verdict d'une telle ligne
  dépend donc du réglage de l'interpréteur, quand celui de `chrony`, avec R-1, n'en dépend plus. Le collecteur n'en
  écrit jamais (`canonique` : JOURNAL/entier, I-1).
- **O-8** Hors lot : `cargo --locked test` sur la tête laisse dans `TMPDIR` 34 arbres `shogen-<famille>-<cas>-<pid>`
  (canonique 10, coquille 8, e2e 5, reel 11 ; quatre processus ; créés à 04:12:03-05 UTC, pendant le seul `cargo test`
  de la phase), non retirés après un passage vert ; supprimés à la main. À former en item si ce n'est pas voulu.

### 11.8 Écarts de la phase 3 (déclarés)

- **E-16** Un `find` de la copie creuse `tmp/tete3` (noms `__pycache__` seuls, pour vérifier qu'aucun bytecode n'y
  était écrit ; aucun chemin interdit dans la copie creuse, aucun contenu lu) : écart à la lettre « aucune recherche
  récursive sur le dépôt entier ».
- **E-17** Un heredoc non protégé (`<<EOF`) a passé au shell les accents graves d'un script de correction du brouillon
  de cette section (`df -h /` lancé ; `delai`, `d3` : commandes introuvables) ; le script Python a échoué à la
  compilation (`SyntaxError`), donc sans rien exécuter ni écrire ; refait depuis un fichier, heredoc protégé (même
  faute que l'E-1 de la phase 1, sans effet ici).

### 11.9 Tête relue au rendu

`git log -1` : **`dda4bbc`** (« Forge, premier passage de DETTES-T5 et du lot FUZZ (PR n 11) : annexe B.95, JOURNAL »,
04:18:02 UTC), après `5e445c4` (fusion de la PR n 11). Entre `0e03a9f` et `dda4bbc`, aucun chemin de la série ni des
jobs lancés (`s2bis/`, `docs/adr-0029/s2bis/`, `.github/workflows/`, `enforcement/`, `s2-harness/tests`, `Cargo.*`,
`xtask`, `crates`) ne change. Sur `dda4bbc`, copie neuve : DT6-a à DT6-r s'appliquent (`--check` puis application),
`s2bis/`, FORMAT et METRIQUES égaux à l'état final ; runner 137 ok ; job s2bis, texte exact (bloc identique) : Ran =
358, conforme (`sorties/p3-dda4bbc/`). Copies lourdes supprimées après rendu des sorties (`tmp/tete3`, `tmp/sonde-k`).

## 12. Phase 4 (ajout daté du 2026-10-10 05:10:00 UTC, `date -u`) : DT6-s, DT6-t, DT6-u, dernière avant clôture

Demande du coordinateur (adjudication de la phase 3 : dernier ajout daté de `ADJUDICATION.md`, 04:28:30 UTC, sha256 du
fichier `7c964221…78d2`, lu d'abord). Heure lue au début : 2026-10-10 04:28:34 UTC ; `git log -1` au début et au
rendu : `dda4bbc`. Un seul processus lourd à la fois ; trois processus de charge au plus, pendant les seules mesures.

### 12.1 Diffs, après DT6-r

| diff | objet | sha256 | R-25 | fichiers |
|---|---|---|---|---|
| DT6-s | O-5 : titre de la section METRIQUES de DT6-r | `a5057683843895fe0787ca1e61c00db887be04943789ac94fb3fd491a6448888` | +0 | METRIQUES +1 −1 |
| DT6-t | O-6 : borne exacte de R-1 figée | `250e78ad245a10d19bff5689291e818a964d5607f5d0d76e97d772658586eb2a` | +4 | `test_status.py` +4 −1 ; METRIQUES +20 |
| DT6-u | SHOGEN-S2BIS-TEST-SANTE-CHARGE-1 | `f73b8ebd07841d32a7a9e6fc55bd4ffbc3dac7aad582631097c6df7ef2cd8ee9` | +5 | `test_sante.py` +5 −2 ; METRIQUES +27 |

Générés entre instantanés successifs (`travail/etats4/r` à `u`, `outils/diff_etapes.sh`) ; `largeur.py` : aucun
signalement. R-25 de la série a à u : +757. Aucune méthode de test créée (DT6-t ajoute deux lignes à une méthode
existante ; DT6-u corrige un test existant) : plancher s2bis inchangé, 358 (`--egal`).

### 12.2 DT6-s

Le titre devient « ## DT6-l à DT6-q (2026-10-10) : réserves R-1 à R-6 du contre-contrôle du lot (lot DETTES-T6) » ;
une ligne.

### 12.3 DT6-t

Les deux lignes de `outils/r1m4_essai.py` (la seconde avec un commentaire qui nomme DT6-t), après la boucle de R-1 de
`test_ligne_hors_format_jamais_une_trace` (la limite y vaut encore `journal.CHIFFRES`), et la docstring. Rouge et vert
(`outils/rouge_etat.py`, `sorties/p4-rouge-*.txt`, `python3.12 -B -X dev -W error`) : vert sur le code ; R1-M4 : FAIL 1
(`AssertionError: unexpectedly None`, la nouvelle assertion) ; R1-M3 : FAIL 1 (cas de 641 chiffres de la même méthode :
`'ValueError' != "disque : non relevé ({'libre': 14})"`) ; R1-M4 sur l'état DT6-s, avant DT6-t : OK (vivant).

### 12.4 DT6-u : SHOGEN-S2BIS-TEST-SANTE-CHARGE-1

Constat source, lu (E-18) : E-6 du G1 de DB-1 (`s2bis/db1/RAPPORT-GENERATEUR.md` l.196-199, NOTES l.69-70) :
`tests.test_sante.Branchement.test_sonde_rendue_apres_l_echeance_avant_le_releve_vaut_null` en ERROR (`TypeError`,
`enr["d3"]` nul), une fois en 81 suites complètes, pendant un mutant.

Reproduction, état DT6-r, sous 3 processus de charge (`python3.12 -c "while True: pass"`, bornés par `timeout 900`,
groupes tués à la fin ; `outils/charge.py`, `charge_rep.py`, `repete_test.py`) :

| mesure | passages | échecs | charge sur 1 min (moyenne ; min à max) | sortie |
|---|---|---|---|---|
| module `test_sante` (14 tests), un interpréteur par passage | 200 | 0 | 4,49 ; 1,92 à 5,56 | `sorties/p4-charge-avant.json` |
| le test seul, répété dans un interpréteur | 10 000 | **2 ERROR** (passages 656 et 4 722) : `TypeError: 'NoneType' object is not subscriptable` à `enr["d3"]["code"]` (l.259) | 4,03 ; 1,70 à 5,18 | `sorties/p4-rep-avant-10000.json` |

Cause, lue au test : son `attendre` injecté n'attend que les deux témoins (`futurs[2:]`), puis avance l'horloge à E et à
E + 1 ms ; il n'attend ni la lecture (`futurs[0]`) ni d3 (`futurs[1]`). Un fil de d3 que la charge retarde rend après
(non rendu au relevé, ou `fin` > E) : d3 vaut null, comme la règle `fin` > E le veut. Le code est juste ; le test ne
l'était pas. Les autres attentes du module, relues : `Temps.attendre` attend tous les futurs (0,5 s) pour les trois
autres tests de `Branchement` ; les tests de `Sondes` attendent chaque futur qu'ils affirment (5 s) ;
`test_sondes_en_parallele_arguments_et_ordre` borne 0,9 s pour 0,3 s ; aucun en échec sur les 400 passages chargés du
module (avant et après).

Correction du test : `attendre` attend d'abord la lecture et d3 (`concurrent.futures.wait(futurs[:2], 5)`, la borne de
ses autres attentes) ; d3 rend 20 ms réelles après son départ (`Faux(pause=0.02)`) : l'ordre que la charge défaisait
devient la règle du test, et le rouge sans l'attente est certain ; docstring. Aucun saut ; aucune borne d'attente
changée.

| mesure | passages | échecs | charge | sortie |
|---|---|---|---|---|
| rouge (test d'abord) : d3 lente, sans l'attente, sans charge | 200 | 200 ERROR (`TypeError`, le symptôme du constat) ; module `-X dev -W error` : FAILED (errors=1) | — | `sorties/p4-u-rouge-200.json` |
| vert : avec l'attente, sans charge | 200 | 0 ; module OK | — | `sorties/p4-u-vert-200.json` |
| après, le test seul, sous charge | 10 000 | **0** | 4,52 ; 1,60 à 5,63 | `sorties/p4-rep-apres-10000.json` |
| après, module `test_sante`, sous charge | 200 | **0** | 4,92 ; 4,32 à 5,56 | `sorties/p4-charge-apres.json` |

Écart de fréquence (1 en 81 suites chez DB-1 ; 2 en 10 000 ici) : la fenêtre dépend de l'affamement du fil de d3 ; une
suite complète (plus de fils dans le processus) sur une machine plus chargée l'élargit [inféré, non mesuré].

Phrase de fermeture proposée pour l'annexe B : « SHOGEN-S2BIS-TEST-SANTE-CHARGE-1 fermé par DT6-u (lot DETTES-T6) :
cause trouvée au test, non au code (l'attente injectée de `test_sonde_rendue_apres_l_echeance_avant_le_releve_vaut_null`
n'attendait ni la lecture ni d3 avant d'avancer l'horloge à E et à E + 1 ms : un fil de d3 retardé par la charge rendait
après E, et d3 valait null) ; correction : la lecture et d3 attendues d'abord (borne de 5 s), d3 lente de 20 ms ;
reproduit 2 fois en 10 000 passages chargés avant, 0 en 10 000 après ; 200 passages chargés du module, 0 échec ; rouge
certain sans l'attente (200 sur 200). »

### 12.5 Mutants (commande exacte du job ; borne de 300 s ; python3.12 ; réseau coupé)

Copie de la tête `dda4bbc` + DT6-a à DT6-r, `s2bis/` porté à l'état u (`outils/spec_p4.py`, `sorties/p4-mutants.json`) :
témoin VIVANT ; R1-M1 à R1-M4 (forme du contre-contrôleur) TUÉS par `test_ligne_hors_format_jamais_une_trace` (R1-M4,
vivant à la phase 3, l'est par DT6-t) ; U01 (`fin >= limite`), U02 (`fin > limite + 1000`), U03 (limite des sondes prise
au relevé) TUÉS par le test corrigé : la correction n'ôte rien à ce qu'il tient ; 0 FATAL.

### 12.6 Vert de la série a à u sur la tête du moment (`dda4bbc`)

Copie neuve creuse (`outils/copie_tete4.sh`) : DT6-a à DT6-u appliqués (`--check` puis application), `s2bis/`, FORMAT
et METRIQUES égaux à `travail/etats4/u` ; bloc `run` du job s2bis identique (`38561d49…1f17`). `outils/verif_jobs4.sh`,
`sorties/p4-*.txt`, réseau coupé :

| vérification | résultat |
|---|---|
| runner (étape du job, texte exact) | `verdict-suite-s2 : 137 ok, 0 échec` |
| job s2bis, texte exact du bloc `run` (l.289-291), `bash --noprofile --norc -eo pipefail`, `python3` = 3.12.3 | `Python 3.12.3` ; `Ran 358 tests` ; `verdict-suite-s2 : conforme (code 0, résumé final, aucun saut, Ran = 358)` ; sortie 0 |
| matrice 3.10.20, 3.11.15, 3.12.3, 3.13.14 (`-X dev -W error`, `PYTHONDEVMODE=1`, `PYTHONWARNINGS=error`) | conforme, Ran = 358 chacune ; 0 « Exception ignored », 0 « warning » |
| `docs-sha256sums` | conforme (39 SHA256SUMS) |

### 12.7 Écarts de la phase 4 (déclarés)

- **E-18** Pour trouver le test du constat, que le message ne nommait pas : `ls` non récursifs de la racine du
  scratchpad et de `s2bis/`, puis `grep` du motif « test_sante|81 passages|CHARGE » sur `s2bis/db1/*.md` (glob non
  récursif, qui a touché `BRIEF-DB1.md` : aucune ligne trouvée, rien affiché), et lecture de deux passages nommés
  (`RAPPORT-GENERATEUR.md` l.194-204, `NOTES.md` l.64-78) d'un autre lot.
- **E-19** Charge : quatre mesures de 2,5 à 7,2 min (21,5 min en tout), 3 processus de charge chacune, l'une après
  l'autre, rien d'autre de lourd pendant ce temps ; la machine portait aussi d'autres travaux (charge relevée jusqu'à
  5,63).

### 12.8 Tête relue au rendu

`git log -1` : `dda4bbc` (inchangée depuis le début de la phase). Copies lourdes supprimées (`tmp/tete4`, `tmp/charge`,
`tmp/u-vert`, `tmp/u-rouge`) ; instantanés gardés (`travail/etats4/r` à `u`).

## 13. Phase 5 (ajout daté du 2026-10-10 05:55:36 UTC, `date -u`) : réserve R-8 de la passe 2, DT6-v et DT6-w

Demande du coordinateur (passe 2 du contre-contrôle : CONFORME-AVEC-RÉSERVES, R-8 seule ; adjudication : dernier ajout
daté de `ADJUDICATION.md`, 05:46:44 UTC, sha256 du fichier `abd7f547…9f3a`, lu d'abord). Heure lue au début :
2026-10-10 05:46:49 UTC ; `git log -1` au début : `04f242d` (DETTES-T14 DT14-b, après `4b48108`, DT14-a).

### 13.1 DT6-v et DT6-w : les deux diffs du contre-contrôleur, repris octet pour octet

| diff | source (`g2/cc/propose/`) | sha256 | R-25 |
|---|---|---|---|
| DT6-v | `R-8.diff` | `e0a8facb96ac7fae2bf12a105eadd0d7e7b0084d99f8a013323d7519173c4e7e` | +2 |
| DT6-w | `R-8-metriques.diff` | `6389788b583152e7b87e4529eb8550e9026cde52b73e1531cf7fd7dc0eb014b0` | +0 (`.md` +18) |

`cmp` : identiques, 2 sur 2 ; sha256 égaux aux lignes de `g2/cc/SHA256SUMS` (comme ceux de `mutants/r8.py`
`bc035509…e085` et `mutants/p2.py` `8577e7fd…1f0e`). `largeur.py` : aucun signalement. R-25 de la série a à w : +759 ;
plancher inchangé, 358 (aucune méthode de test créée).

### 13.2 Réponse aux diffs (une ligne chacun)

- **DT6-v (R-8, test)** : juste. Le FORMAT (§13, point 2, « Instant des sondes ») pose la règle `fin` > E pour D-3, D-4
  et D-5 ; `joindre(lancees, 0)`, une fois toutes les sondes rendues, compare chaque `fin` (horloge monotone réelle, en
  µs) à 0 et nulle chaque sonde, d3 comprise : V4 (d3 exemptée) vivait, il est tué. Précision sans correction : la
  limite 0 précède toute fin parce que l'horloge monotone de Linux compte depuis le démarrage (Python n'en fixe pas
  l'origine) ; une limite `min(fins) − 1` ne dépendrait de rien.
- **DT6-w (R-8-metriques)** : juste, et exacte sur la tête : le titre nomme DT6-v, le diff qu'elle décrit ;
  `test_sante.py` 290 lignes, 14 tests ; suite 358 ; rouge sur V4 (FAIL 1), vert, matrice et V4 tué par la commande du
  job : rejoués (§13.3).

### 13.3 Rouge et vert, série a à w

Rouge (`outils/rouge_etat.py`, mutant V4 dans la forme de `g2/cc/mutants/r8.py`, `python3.12 -B -X dev -W error -m
unittest tests.test_sante`) : sur l'état u (avant DT6-v), V4 : OK (vivant) ; sur l'état w : **FAIL 1**,
`test_sondes_en_parallele_arguments_et_ordre` (`Tuples differ: ({'sortie': …}, …) != (None, [None, None, None], [None,
None])`) ; vert sur l'état w : OK (`sorties/p4-rouge-u-V4.txt`, `p4-rouge-w-V4.txt`, `p4-rouge-w-vert.txt`).

Copie neuve creuse de la tête **`04f242d`** (`outils/copie_tete4.sh`) : DT6-a à DT6-w appliqués (23 diffs, `--check`
puis application), `s2bis/`, FORMAT et METRIQUES égaux à `travail/etats4/w` ; bloc `run` du job s2bis identique
(`38561d49…1f17`). `outils/verif_jobs5.sh`, `sorties/p5-*.txt`, réseau coupé :

| vérification | résultat |
|---|---|
| runner (étape du job, texte exact) | `verdict-suite-s2 : 137 ok, 0 échec` |
| job s2bis, texte exact du bloc `run` (l.289-291), `bash --noprofile --norc -eo pipefail`, `python3` = 3.12.3 | `Python 3.12.3` ; `Ran 358 tests` ; `verdict-suite-s2 : conforme (code 0, résumé final, aucun saut, Ran = 358)` ; sortie 0 |
| matrice 3.10.20, 3.11.15, 3.12.3, 3.13.14 (`-X dev -W error`, `PYTHONDEVMODE=1`, `PYTHONWARNINGS=error`) | conforme, Ran = 358 chacune ; 0 « Exception ignored », 0 « warning » |
| V4 par la commande du job (`outils/spec_p5.py` → `r8.py`, borne de 300 s) | témoin VIVANT ; V4 TUÉ par `test_sondes_en_parallele_arguments_et_ordre` ; 0 FATAL (`sorties/p5-mutants.json`) |

Tête relue avant l'écriture de cette section : **`953270e`** (DETTES-T14 DT14-c, 05:50:32 UTC). Entre `dda4bbc` et
`953270e`, aucun chemin de la série ni des jobs (`s2bis/`, `docs/adr-0029/s2bis/`, `.github/workflows/`,
`enforcement/`, `s2-harness/tests`, `scripts/`) ne change. Sur `953270e`, copie neuve : DT6-a à DT6-w s'appliquent,
`s2bis/`, FORMAT et METRIQUES égaux à l'état w ; runner 137 ok ; job s2bis, texte exact : Ran = 358, conforme
(`sorties/p5-953270e/`). Copies lourdes supprimées.

### 13.4 Écart de la phase 5 (déclaré)

- **E-20** La commande de fond qui enchaînait le vert et la campagne nommait `outils/spec_p5.py` avant que je l'écrive ;
  écrit pendant le vert (05:48), avant son usage (05:52:10) : sans effet sur aucun résultat.
