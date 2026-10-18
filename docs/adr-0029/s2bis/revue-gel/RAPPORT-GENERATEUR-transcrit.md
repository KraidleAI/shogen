# Rapport du générateur du lot GEL-COLLECTEUR-1 (GEL-1 à GEL-9, C-1, C-2, C-5, C-6) (transcrit)

> Transcription par l'orchestrateur le 2026-10-18 15:17:59 UTC du fichier s2bis/gel/RAPPORT-GENERATEUR.md ; contrôle FM-1.1 du transcript du générateur par le fm11.py versé : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5 (646 occurrences, aucune autre). Texte ci-dessous avec 5 retouche(s) (E35, E38) : noms de marqueur de dette et locutions de la gate S-G4 cités en clair, mis en code, segments de code à doubles accents graves réécrits en segments simples, heures sans date mises en code (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Rapport du générateur — lot GEL-COLLECTEUR-1 (gel du collecteur de S2-bis, Q-C-06)

Gate 0 : modèle `claude-opus-5-5` (worker `shogen-worker`, effort high). Écrit le 2026-10-18 vers 02:25 UTC, mis à jour vers `03:25` UTC après le brief de correction `BRIEF-GEL-CORR.md` (C-1, C-2), puis vers `06:15` UTC après
`BRIEF-GEL-CORR2.md` (C-5, C-6, suite de la G2), puis vers `07:45` UTC après `BRIEF-GEL-CORR3.md` (C-8), puis vers `09:35` UTC après
`BRIEF-GEL-CORR4.md` (C-10, C-11).
Base : `1d7e5d485e78a8b3d3b713557de5cf236279f833`, relevée par `git rev-parse` sur le dépôt réel et sur les copies
(travail, vérification), égale à la tête du brief (`1d7e5d4`). Aucun commit, aucune écriture git sur le dépôt réel ;
copies creuses en non-cone (emplacements interdits et `*.jsonl` exclus). Réseau coupé (`unshare -n`, `lo` allumée)
pour toute commande de test ; `TMPDIR` du lot ; variable scellée jamais posée.

## 1. Livrables

Diffs en série : `diffs/GEL-1.diff` à `diffs/GEL-9.diff`, puis `g2/diffs/C-3.diff` et `g2/diffs/C-4.diff` (réviseur,
adoptés tels quels), puis `diffs/C-5.diff` et `diffs/C-6.diff`, `g2/diffs/C-7.diff` (réviseur, adopté tel quel),
puis `diffs/C-8.diff`, `g2/diffs/C-9.diff` (réviseur, adopté tel quel), `diffs/C-10.diff` et `diffs/C-11.diff`.
**Ordre d'application final : GEL-1, 2, 3, 4, 5, 7, 8, 6, 9, C-3, C-4, C-5, C-6, C-7, C-8, C-9, C-10, C-11**,
chacun appliqué sur le précédent depuis la base (`git apply --check` puis `git apply`, tous OK : `preuves/apply-check.txt`) ; arbre final
égal à la copie de travail (`diff -r`, `cmp`).

| diff | objet | lignes de code (R-25) | plancher s2bis | mutants |
|---|---|---|---|---|
| GEL-1 | `formes.json` de production (formes fondues, ordre gardé ; w 60, delta 20 s, delai 10 s, tolerance 5 s, marge 1 s, places 40), `formes-pool.json` supprimé | 61 | 433 | 11 tués (+1 rejoué après FATAL inapplicable) |
| GEL-2 | hôte Binance `data-api.binance.vision` ; paquet §4 « Remplaçants écrits d'avance » (`api.binance.com` ; `www.cern.ch` pour D-5) | 16 | 433 | 8 tués |
| GEL-3 | règle `nom-forme` (constante `capture.NOM` partagée), pool et carte | 29 | 434 | 14 tués, 1 vivant équivalent (cache de `re`) |
| GEL-4 | reprise de capture (manifeste au départ, `flush` par ligne, `--reprise`, refus `manifeste`, `somme`, `fichier`) | 148 | 436 | 17 tués (+1 rejoué après FATAL inapplicable) |
| GEL-5 | bloc du témoin : requête groupée `[eth_blockNumber, eth_call, eth_blockNumber]`, `bloc_avant`, `bloc_apres`, fixtures réécrites | 116 | 437 | 16 tués (campagne entière rejouée après 2 vivants) |
| GEL-7 (réécrit, C-1) | `observateurs.json` (o1 à o4 ; `tsa` facultative, absente au gel), `--observateurs` pour `status`, `resume`, `jeton` ; `--envoi` refusé sans TSA scellée ou autre qu'elle (`CONFIG/tsa`) ; `.armement` | 173 | 440 | 25 tués (campagne entière rejouée après C-1) |
| GEL-8 | paquet §5 (Q-C-07) et §6 (coupure de la carte) ; documentation seule | 0 | 440 | — |
| GEL-6 | `sante.json` de production (`chronyc -n tracking` ; trois témoins D-4 ; `www.kernel.org`, `www.arin.net` ; 2 s) | 30 | 441 | 9 tués |
| GEL-9 (neuf, C-2) | `carte.json` de production, carte vide (depart 5 s, delai 10 s, marge 1 s, places 1, ASN quotidien) ; paquet §6 | 24 | 442 | 9 tués |
| C-3, C-4 (G2) | diffs du réviseur, non modifiés | — | 442 | (G2) |
| C-5 (I-1 de la G2) | enregistrement `tetes` de la boucle sur la liste fermée (avant la borne NOMBRE ; `TETES/liste`) ; `pool --depot` exige `--observateurs` ; liste à `run_params` | 66 | 443 | 14 tués |
| C-6 (I-2, Q-1, Q-2 de la G2) | carte de production : quatre remplaçants de Binance (`binance_<actif>_remplacant`, `api.binance.com`), places 4 ; paquet §4 et §6 | 22 | 443 | 9 tués |
| C-7 (G2) | diff du réviseur, non modifié | — | 443 | (G2) |
| C-8 (I-4 de la G2) | liste fermée des journaux des têtes (`tetes.JOURNAUX` = `pool`, `secondaire`) ; refus `TETES/journal` borné ; aucune éviction possible (au plus huit têtes lues) | 45 | 444 | 11 tués |
| C-9 (G2) | diff du réviseur, non modifié | — | 444 | (G2) |
| C-10 (I-6 de la G2) | `secondaire --depot` : tête du journal `secondaire` exportée à chaque point, sans enregistrement `tetes` (`Boucle(…, consigner=False)`) | 60 | 446 | 10 tués (un rejoué après correction du test) |
| C-11 (I-7 de la G2) | `test_carte_pendue_ou_refusee_le_pool_intact` en un processus, horloges et lectures injectées (tests seuls) | 44 | 446 | 3 mutants du code gardé, tués |

GEL-1 à GEL-5 inchangés. GEL-8 et GEL-6 : lignes ajoutées et retirées identiques à leur première version (contrôlé
par `diff` des lignes `+`/`-`), régénérés seulement parce que le contexte de leurs blocs METRIQUES (fin de la section
GEL-7, réécrite par C-1) a changé : C-1 l'exige. Aucun diff ne nomme plus FreeTSA (`grep -ci freetsa` : 0 partout).

Mutants : `scripts/controle/mutants.py` du dépôt réel (arbre relu), commande du job `s2bis-unittest` (runner puis
ligne s2bis), borne 300 s, copie mutée à part ; relevé `ps` de fin vide à chaque campagne (moissonneur). Diff, sortie
et classement de chaque mutant : `mutants/GEL-k/` et `mutants/GEL-k.out`. Rouges d'assertion : `preuves/GEL-k-rouge.txt`
(détail par diff dans METRIQUES, une section par diff, forme INT-P2).

## 2. Vérifications finales (copie neuve = base + les dix-huit diffs ; job s2bis vert à chaque état : `preuves/serie.txt`)

- runner `run-fixtures-verdict-suite-s2.py` : 153 cas `ok`, sortie 0 ;
- job s2bis : `verdict-suite-s2 : conforme (code 0, résumé final, aucun saut, Ran = 446)` (plancher 446, `--egal`) ;
- job S2 : `verdict-suite-s2 : conforme (code 0, résumé final, sauts nommant SHOGEN_S2_CAMPAGNE_CONTROL, Ran = 423)` ;
- job sim-bis : `verdict-suite-s2 : conforme (code 0, résumé final, aucun saut, Ran = 279)` ;
- matrice `-X dev -W error` de la suite s2bis : 3.10.20, 3.11.15, 3.12.3, 3.13.14 : code 0, `Ran 446`, `OK` (sous 3.11 : trois passages complets, `matrice-3.11-passage1..3.txt`), aucune
  ligne `Exception ignored` ni `Warning` ; aucun `__pycache__` laissé ;
- `cargo --locked xtask verify` (cible par défaut de la copie, hors ligne) : S-G1 à S-G8 `VERDICT : VERT` (8 lignes),
  `cargo fmt --check : VERT`, `no_std du vérificateur … : VERT`, `cargo clippy -D warnings : VERT` ; S-G9
  `VERDICT : ROUGE (1 violation(s))` : `docs/17-modele-de-menace.md:70` renvoie à `docs/rapports/…`, emplacement
  exclu de la copie creuse (interdit du brief) ; violation connue (adjudication de P2C), sans lien avec les diffs ;
  le verdict global ROUGE vient de ce seul fait.

## 3. Items de l'annexe B : fermetures proposées

- **SHOGEN-S2BIS-NOM-FORME-1** (l.1983) : fermé par GEL-3. Texte proposé : « Règle `nom-forme` de `formes.json` et de
  `carte.json` au motif `capture.NOM` (une seule constante), FORMAT §14.1 et §19 ; tests
  `tests.test_entree.Entree.test_regle_nom_forme` et `tests.test_formes_pool.Formes.test_formes_controlees_requetes_construites` ».
- **SHOGEN-S2BIS-CAPTURE-PARTIELLE-1** (l.1984) : fermé par GEL-4. Texte proposé : « Manifeste créé au départ, ligne
  vidée après chaque fichier ; `capture --reprise` (sommes recontrôlées ; refus `manifeste`, `somme`, `fichier`) ;
  FORMAT §19.5 ; tests `tests.test_capture.Capture.test_reprise_apres_une_capture_coupee` et
  `test_reprise_refusee_avant_toute_lecture` ».
- **SHOGEN-S2BIS-TEMOIN-BLOC-1** (l.1980) : fermé par GEL-5. Texte proposé : « Uniswap et Curve en requête JSON-RPC
  groupée encadrée, `bloc_avant` et `bloc_apres` en extra (non atomique, écart attendu d'au plus un bloc), FORMAT
  §9.1 ; test `tests.test_temoin.Lot.test_blocs_encadrants_apparies_par_id`, fixtures groupées ». Le datage par bloc
  reste au recalcul (RB-2, SHOGEN-S2BIS-TEMOIN-RECALC-1).
- **SHOGEN-S2BIS-OBSERVATEURS-LISTE-1** (l.1327) : fermé par GEL-7. Texte proposé : « Liste fermée scellée
  `config/observateurs.json`, lue par `status`, `resume` et `jeton` ; noms hors de la liste ignorés et nommés ; tests
  `test_entree.Entree.test_liste_des_observateurs_scellee`, `test_status.Resumes.test_quorum_sur_la_liste_fermee`,
  `test_tetes.Jeton.test_jeton_liste_fermee_et_armement`, `test_tetes.Jeton.test_commande_jeton`,
  `test_status.Resumes.test_commande_status_avec_depot` ».
- **SHOGEN-S2BIS-CONFIG-PRODUCTION-1** (l.1152 ; volet l.1334) : fermeture **partielle** : volets formes (GEL-1,
  `test_valeurs_scellees_liees_a_l_adr`), marge du pool (places 40), sondes (GEL-6,
  `test_sante_de_production_liee_a_l_adr`), carte (GEL-9 et C-6, `test_carte_de_production`), état d'armement (GEL-7,
  `.armement`) fermés. Texte proposé pour le reste de l'item : « Restent deux volets : (a) délais de `resolv.conf`
  (configuration de déploiement des observateurs, hors du paquet Python), re-daté DB-2 ; (b) URL de la TSA dans
  `observateurs.json` (champ `tsa`, absent au gel ; Certigna, URL et authentification en acte extérieur, ajout daté
  du 2026-10-10 au G0, point 6), re-daté DB-3 : `jeton` refuse tout `--envoi` d'ici là (`CONFIG/tsa`) ».

## 4. Adjudications reçues, questions et limites (règle PAROXYSME)

- **G2** (ACCEPTE-AVEC-CORRECTIONS ; C-3 et C-4 adoptés tels quels) : **C-5** (I-1) fait : `tetes.Depot(…, liste)`
  écarte avant la borne NOMBRE les fichiers de tête hors de la liste, en nomme seize au plus au refus `TETES/liste`
  (borne choisie par le lot : un dépôt hostile ne grossit pas l'enregistrement au-delà de LIMITE) et compte le reste aux
  `ignores` ; `pool --depot` exige `--observateurs`, refuse un observateur hors de la liste et porte la liste à
  `run_params`. **C-6** (I-2) fait : la carte porte les quatre remplaçants de Binance, lus par le processus secondaire.
  **Q-1** écrite au paquet §4 comme lecture de l'advisor de l'AVIS l.95. **Q-2** écrite au paquet §6 ; écart à
  ratifier : `places` vaut 4 et non 1, la règle `places-formes` exigeant une place par forme depuis C-6. **I-3** (texte
  d'item proposé) : « Volet de SHOGEN-S2BIS-TSA-CERTIGNA-1 : l'URL de la TSA scellée à DB-3 ne porte aucun secret
  (authentification hors de l'URL : `.armement` l'écrit en clair au dépôt) ; la règle `tsa-https` (sans port, hôte en
  minuscules) se relit sur l'URL de Certigna ; déclencheur DB-3 ».
- **C-10** (I-6, adjugée) : fait. Texte de fermeture proposé pour SHOGEN-S2BIS-TETE-SECONDAIRE-1 : « La commande
  `secondaire --depot` exporte la tête du journal `secondaire` à chaque point de contrôle
  (`<observateur>-secondaire.tete`), sans enregistrement `tetes` ; la tête est lue par l'enregistrement `tetes` du pool
  et par le jeton (journal de la liste fermée, C-8) ; FORMAT §15.6, §16.6 ; tests
  `test_secondaire.Secondaire.test_tete_du_secondaire_exportee_au_point` et `test_commande_secondaire_avec_depot` ;
  le journal se nomme `secondaire` (le texte de l'item disait `carte`) ».
- **C-11** (I-7, adjugée) : fait dans la borne (44 lignes) : le test d'isolement tourne en un processus, horloges et
  lectures injectées ; la séparation réelle des deux processus n'y est plus éprouvée (elle relève du déploiement, deux
  unités) ; un processus secondaire réel reste éprouvé par `Conformite` (temps réel, cinq fenêtres, contrôles de forme
  seulement). Item proposé à fermer : SHOGEN-S2BIS-SECONDAIRE-ISOLEMENT-TEMPS-1, par ce test.
- **C-8** (I-4 de la G2, adjugée) : fait ; le cas de C-7 (`ignores` 2 + 1) devient 1 + 1 avec seize refus
  `TETES/journal` ; au cas armé de `test_commande_jeton`, le manifeste avec liste n'a plus la tête `carte` des tests :
  `lier` y est espionné (appel relevé : réponse, sha256 du manifeste écrit, nonce), la liaison réelle restant éprouvée
  par `test_jeton_lie_a_la_requete`. Item I-5 (SHOGEN-S2BIS-CARTE-REMPLACANTS-RECALC-1) : rendu au recalcul (RB), rien à
  coder ici.
- FORMAT : C-6 recoupe aussi trois lignes de plus de 120 colonnes venues de GEL-2, GEL-3 et C-5 (texte inchangé).

- **Q-1** (`.armement` au dépôt) et **Q-3** (`--observateurs` exigée, `CONFIG/observateur`) : acceptées.
- **Q-2** (TSA) : correction C-1 faite (GEL-7 réécrit) : FreeTSA retirée ; `tsa` facultative et absente au gel,
  relue sous le schéma `entree.TSA` (règle `tsa-https`) quand elle est le seul champ en plus ; `jeton` refuse un
  `--envoi` sans TSA scellée (`CONFIG/tsa : --envoi sans TSA scellée`, sortie 2) et toujours une URL autre que la TSA
  scellée. Limite : le motif `tsa-https` refuse port et majuscules ; l'URL de Certigna pourra demander un amendement
  à DB-3.
- **Q-4** (carte de production) : correction C-2 faite (GEL-9 neuf) : `carte.json` vide, chargé par
  `configurer_secondaire` ; paquet §6 : « carte vide au gel, sources après le rendu ». Choix du lot : `places` 1 et
  relevé ASN à `00:00` UTC (`decalage` 0), sans pièce qui les fixe.
- **Item à former** (adjudication DNS) : SHOGEN-S2BIS-DNS-TEMOINS-RODAGE-1 (TTL d'origine, autorités et ASN des deux
  noms confirmés au smoke de DB-2 et au rodage, ou remplaçant substitué avant le sceau).
- **Limites** : réponse de Binance et du lot JSON-RPC depuis l'Europe non mesurée ici (`smoke` à DB-2) ;
  `www.cern.ch` : un seul opérateur. (La limite `O_NONBLOCK` de `capture --reprise` est fermée par C-4 de la G2 :
  `O_NOFOLLOW`, `O_NONBLOCK`, fichier ordinaire exigé.)
- **Écarts du lot** : E-1 `outils/isole.sh` du scratchpad appelle un `lo_up.py` absent : copie locale écrite
  (`outils/lo_up.py`, ioctl SIOCSIFFLAGS). E-2 citations du brief : δ et délai à l.233 suivent la convention du
  FORMAT (commit `e16956b`), texte courant l.235 ; la phrase de la carte citée AVIS l.75 est à l.77 (citée ainsi).
  E-3 deux mutants au texte avant absent (FATAL inapplicable) et un mutant visant une règle voisine : réécrits et
  rejoués. E-4 GEL-5 : deux vivants au premier passage (cas non séparants), tests réécrits, campagne entière
  rejouée ; GEL-7 : un vivant (URL non transmise), assertion ajoutée, mutant rejoué. E-5 rouges avec ERROR en plus des
  FAIL : GEL-5 (1), GEL-7 (2), C-1 (1 : envoi sans TSA non refusé dans la première version).

## 5. Journal de provenance (G1)

Sources [lu], sha256 complets :
- brief `scratchpad/s2bis/gel/BRIEF-GEL.md` `dfe047b50ae67f063353b2449bd4dc2c8e4169910fe789ff749ab03024bb5793` ;
- `AVIS-ADVISOR.md` `10ed1f5f2ffa1211e7bcfb9fe819323248af8a215db4934a1288a58a2149fb69` ;
- `p2c/ADJUDICATION.md` `ef2d146524d9262c264a5cf7ec71364c2f18eca74329d3c02fe9a49f60c45ade` ;
- `LECTURE-DNS-TEMOINS.md` `76d170cb8f99bed2191eb221492b690902931db74223ab645d869aef351a91d6` (l.20-80) ;
- `ADJUDICATION-DNS.md` `c55e443ec61e25828cd79fdd4da548fc8f1f691ffb16198348f5d8f7c5448620` ;
- G0 `G0-COLLECTE-RECALC-DEPLOI.md` `08c1e6b0d307e11509798bd9409c6947e11df381602e22ad20f10a32c8ec691d` (entier) ;
- PROPOSITION `0cdf84c25092101a9f2d8075fc90f59a5af7b689458b025635d42adb865fbfd0` (l.330-355, l.172, l.188-189) ;
- AVIS `a919b307e80f860733f9e114504c0ec93e30a87fabb0970b9384a854421616ce` (l.30-45, l.70-100) ;
- ADR-0029 `32a598931dd35c91afbc7e61fec532a1a18de2e4c69e188b2d22b97aadaa2801` (l.76-90, 105-118, 165-176, 215-240 ;
  lignes citées relues au commit `e16956b`) ;
- FORMAT `9db85b18a817a9c63fee7068788a67684c4fcedc61b060891eb39f9c7d9fc492` (en-tête, §9.1, §13 à §19) ;
- G6-PAQUET `09971330df5ea589208709dfa79e65126de94dd023cb9d5c9fd51d4a3a114ec1` (entier) ;
- METRIQUES `10e2d56c6c01b8fe639e43095e5fc3203f2fc04aceb3942c77e76d4fcaf76bcf` (sections INT-P2) ;
- ANNEXE-B `a531fd23554ccd0a68a6793b03258324501b4f238026b813d620806ec5221a73` (l.1152, 1327-1338, 1980-1984, recherche
  dans ce seul fichier) ;
- PAIRES-ET-TEMOIN `75535ad5a43c3d1b0fc7eaaaed52f260bc9c8c51f1dfbc45feb4dcddddc1258b` (l.37, 44, 90, 94, 131) ;
- `scripts/controle/mutants.py` `3e21878363ad7a106357abb666c3d8c5351f8ac94fcf3d95c4e64400abddad64` (docstring,
  l.140-260) et `scripts/controle/README.md` (l.429-470) ;
- `.github/workflows/gates.yml` `77182a393264c1a559b82d1e1ba97130a94eef9d80166354cc00c0c3c43de632` (l.180-300) ;
- code et tests de `s2bis/` touchés (entree, config, capture, decodeurs, sante, status, tetes et leurs tests).
- brief de correction n° 4 `BRIEF-GEL-CORR4.md` `94c21128175e8dd47528ac321b7922c8fcde7db2366cfd269509a8f3c882f716` (entier) ; `g2/diffs/C-9.diff` `f5466f5da5c13fc7f6a04919ad8a5fb43bfa1a415e22a9206614815cba9d2c7a` ;
- brief de correction n° 3 `BRIEF-GEL-CORR3.md` `58f94c45ec4024609feddacec808a0738fb9fba6a030e99192624eae20e04937` (entier) ; `g2/diffs/C-7.diff` `cab5ba3f41222bb86d97271f154a0b84d6b16a59ef8a1b1a6e6a97d4e3294550` ;
- brief de correction n° 2 `BRIEF-GEL-CORR2.md` `3a826cdb9157d28bf336587c9c57eebb3b879114b0fadc5d08970a2d40c357aa` (entier) ; `g2/RAPPORT-G2.md` `ac6d89f901c16d9db6e9b85f53c09bd00848a62ebf257efe5785e8e75f0cf21f` (l.115-140, l.255-268, l.293-326) ;
- brief de correction `BRIEF-GEL-CORR.md` `83e75b3c77adba44e3643241dcdc80d62c24bd69d6976af6a4941461d855ca88` (entier).
[2nd] : aucune (l'URL de FreeTSA, de seconde main, est retirée par C-1). [abs] : aucune.

Commandes : `git rev-parse` ; `git clone` local et `git sparse-checkout` ; `outils/job.sh` (runner puis ligne s2bis) à
chaque pas (`preuves/GEL-k-vert.txt`) ; `outils/campagne.sh` (mutants, détachées par `setsid nohup`, fin constatée par
le fichier d'erreur rempli) ; `git apply --check` ; matrice 3.10 à 3.13 ; `cargo --locked xtask verify`.
Chiffres recomptés : lignes de code par `git diff --numstat` sur chemins explicites (`.py`, `.yml`) ; tests par `Ran` ;
mutants par `outils/bilan.py` et `outils/tues.sh` sur les sorties de l'outil ; blocs en hexadécimal par `printf '%x'`
(26149791 : `18f039f` ; 26149796 : `18f03a4` ; 26149797 : `18f03a5`) ; sha256 de la fixture de Curve par `sha256sum`
(`596550e9eb1ab3d69a6206965241d4bea90544949752edb0ff6cef285fe61dd9`).

Copies lourdes supprimées en fin de lot, après chaque passe (`travail/depot`, `travail/mut`, `travail/verif`, `tmp`) ; gardés : `diffs/`,
`mutants/`, `preuves/`, `patchs/`, `outils/`, `NOTES.md`, ce rapport, `SHA256SUMS`.
