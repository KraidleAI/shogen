# Relecture G2 neuve du sous-lot RB-2 (C-1 à C-8) (transcrit)

> Transcription par l'orchestrateur le 2026-10-19 01:29:07 UTC du fichier s2bis/rb2/g2/RAPPORT-G2.md ; contrôle FM-1.1 du transcript du réviseur G2 par le fm11.py versé : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5 (255 occurrences, aucune autre). Texte ci-dessous avec 3 retouche(s) (E35, E38) : noms de marqueur de dette et locutions de la gate S-G4 cités en clair, mis en code, segments de code à doubles accents graves réécrits en segments simples, heures sans date mises en code (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Relecture G2 du sous-lot RB-2 (fusion des quatre observateurs, `run_params`, re-décodage) — rapport du réviseur

- **Gate 0** : modèle `claude-opus-5-5` (identifiant de l'environnement d'exécution), effort high ; fiche `shogen-worker`,
  réviseur G2 distinct du générateur (je n'ai écrit aucun des diffs RB2-a à RB2-h). Aucun commit, aucune écriture git sur
  `/home/user/shogen`, aucune pièce de D.2 ouverte, `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée (retirée par `isole.sh`).
- **Dates** (`date -u`) : reprise à 2026-10-18 21:06:45 UTC (une première relecture, interrompue par un redémarrage du
  conteneur, a laissé des restes : mis de côté dans `ancien/`, sans valeur de preuve ; tout est rejoué) ; ajout au G0 de
  C-4 écrit à 2026-10-18 21:27:42 UTC ; dernière vérification à 2026-10-18 22:45:15 UTC (§3).
- **Base** : copie `copie/`, clone local neuf de `/home/user/shogen`, tête `709d4a71694f521fb11490ba889e29aebf0faf1f`
  (`git rev-parse HEAD`, dépôt réel et copie), égale à celle du brief (`709d4a7`).
- **Série relue** : `../diffs/RB2-a.diff` à `RB2-h.diff`, sha256 égaux à `../SHA256SUMS` (345 lignes `OK`) ; empreinte de
  la série (sha256 de la concaténation dans l'ordre a..h) :
  `e5445eb247585a6e1598319b81be063a72075421af15a70b42e83689393d403f`.

## 1. Verdict

**ACCEPTE-AVEC-CORRECTIONS**, liste fermée C-1 à C-8. Diffs byte-exacts contre l'arbre final de la série, à appliquer dans
l'ordre après RB2-h : `diffs/RB2-G2-1.diff` (code et tests : C-1, C-2, C-3, C-5, C-7 ; sha256
`7e8e377db662dc3eac63c10b29637f2c056b5fa02253d3f2c812cc040a8d2bc0`) puis `diffs/RB2-G2-2.diff` (documents : C-4, C-6 ;
sha256 `504c366f43f6670e59138914b83df5f64df27d866ce0e2262e7755db7bcf2e09`). C-8 corrige le rapport du générateur (texte,
hors dépôt). `git apply --check` et `git apply` des dix diffs sur une extraction neuve de `709d4a7` : sortie 0 dix fois,
sept fichiers égaux à l'arbre corrigé (`preuves/apply-corrections.txt`).

| C-n | défaut (preuve) | correction |
|---|---|---|
| C-1 | `_redecoder` : `base64.b64decode(validate=True)` n'est pas strict : bits de fin non nuls admis sous 3.10 à 3.13, remplissage en trop admis sous 3.10 à 3.12 et refusé sous 3.13 (`preuves/b64-versions.txt`) : le verdict de re-décodage d'un même `brut` change avec la version (essai E1 : `egal` sous 3.11, `base64` sous 3.13, `preuves/essais-final-python3.1x.txt`) ; contraire au FORMAT §9.1 (« base64 (alphabet standard, avec remplissage) ») et au critère « base64 strict ». En plus, le décodeur est appelé avant la comparaison du sha256 (essai E7 : 1 appel sur un sha256 faux) : la checklist demande base64 et sha256 contrôlés d'abord | `brut` exigé égal à `b64encode` de ses octets ; sha256 comparé avant tout décodage, cause `sha256` sans appel du décodeur |
| C-2 | `FUSION/relecture` ne compare que la tête : le lecteur tolère les ruptures, donc un fichier antérieur réécrit entre les passes (chaîne refaite, `commit` d'un `run_params` changé) laisse la tête intacte ; la passe 2 rend ces fenêtres sans refus, avec une seule rupture `LECTEUR/lien` (essai E2) ; une `Fusion` neuve refuse `FUSION/commit` | intégrité entière (`releve` : tête, ruptures avec leur `apres`, queues déclarées, queue finale) exigée égale à celle de la passe 1 ; chaque tronçon de chaîne est ainsi fixé par la ligne qui le clôt |
| C-3 | ruptures, `trou` et `reprise` qu'aucun enregistrement de fenêtre ne suit sont perdus : une `reprise` finale (démarrage arrêté avant `run_params`, par exemple disque plein) n'est rendue nulle part (essai E6) ; la checklist exige les ruptures, trous et reprises rendus à leur place | rendus en fin de journal, `integrite[o, j]["sans_fenetre"]` |
| C-4 | le G0 ne porte ni l'adjudication de Q-RB2-1 (son ajout du `16:13:07` UTC la dit « à adjuger ») ni la décision de Q-RB2-13 (observateur absent admis, quorum de trois), qui change ce que RB-3 reçoit (D-1 « absence », M_j) | ajout daté au G0 (`21:27:42` UTC), à adopter par l'orchestrateur |
| C-5 | un fichier à la place du dossier d'un observateur fait remonter une `NotADirectoryError` non nommée (essai E4) ; le module promet un refus nommé pour tout écart | `FUSION/dossier` |
| C-6 | METRIQUES, section RB2-h : une ligne de 137 caractères (`preuves/colonnes.txt` ; les trois titres de plus de 120 caractères suivent un précédent du fichier, 4 titres longs à la base) | paragraphe replié à 120 colonnes au plus |
| C-7 | six de mes douze mutants vivent sur l'arbre final (§2, campagne `revue`), aucun équivalent : r02 porteuses comparées par `==` (`1 == True`), r03 `brut` nul ou non ASCII non attrapé (exception qui remonte), r05 témoin filtré par le nom de la forme (site d'appel : aucune fixture où forme et décodeur diffèrent, SHOGEN-MUTANTS-SITE-APPEL-1), r06 suffixe sans souligné, r11 `blocs` d'une `panne_decode` du témoin (TypeError), r14 `panne_http` re-décodée (Q-RB2-6) ; r04 (sha256 après les valeurs) vit aussi, réglé par C-1 | tests neufs de `RevueG2` (cas `nul`, `non-ascii`, `sha256-et-valeurs` ; quatre tests) ; les six mutants rejoués sur l'arbre corrigé : tués |
| C-8 | rapport du générateur §6 : SHOGEN-S2BIS-CARTE-REMPLACANTS-RECALC-1 est à la l.2004 de l'annexe B, non 2005 (le brief aussi) ; SHOGEN-HARNAIS-ISOLE-LO-1 est périmé (`isole.sh` modifié à 2026-10-18 20:12:27 UTC, nomme le `lo_up.py` de son dossier ; mesuré conforme à `21:2x` UTC : réseau injoignable, `lo` allumée) ; SHOGEN-S2BIS-DECODEURS-FERMETURE-1 garde un déclencheur périmé (« adjudication de Q-RB2-1 », faite) ; SHOGEN-S2BIS-FUSION-COUT-1 peut citer la mesure mémoire E5 | texte (§5) |

Après RB2-G2-1 : plancher du job 471 (463 + 8 tests de `RevueG2`), R-25 : 156 lignes de code ajoutées.

## 2. Checklist

1. **Série — conforme, une instabilité hors RB-2.** `outils/serie.sh` sur la copie neuve : `check sortie 0`,
   `apply sortie 0` huit fois ; runner `verdict-suite-s2 : 153 ok, 0 échec` à chacun des neuf états ; job s2bis
   `conforme (code 0, résumé final, aucun saut, Ran = …)` à 446, 447, 449, 455, 456, 458, 460, 463 ; à l'état c, premier
   passage `refus : code de sortie 1` : FAIL de `test_sante.Branchement.test_sante_liste_blanche_sondes_au_depart_jointes_avant_l_echeance`
   (instant `…901000000` au lieu de `…900000000`, course du faux temps sous charge ; module de collecte, que RB-2 ne
   touche pas) ; copie ramenée à c (`git apply -R` de h à d), job rejoué deux fois : `conforme … Ran = 453` deux fois,
   puis d à h réappliqués, fichiers égaux (`preuves/serie/job-c*.txt`). Item proposé (§5). Écart du brief : il attend un
   plancher final de 461 ; RB2-h écrit 463 et la suite en compte 463 (je suis le diff, comme le brief le demande). Arbre
   final : S2 `conforme (… sauts nommant SHOGEN_S2_CAMPAGNE_CONTROL, Ran = 423)`, sim-bis `conforme (… Ran = 279)` ;
   matrice 3.10 à 3.13 `-X dev -W error` : `Ran 463 tests`, `OK`, sortie 0, 0 ligne `Exception ignored` ni `Warning` ;
   `cargo --locked xtask verify` (cible par défaut) : S-G1 à S-G9 `VERDICT : VERT (0 violation(s))`, fmt, no_std, clippy
   `VERT`, `=== VERDICT GLOBAL : VERT ===`, sortie 0, aussi avec `fusion.py` et `test_fusion.py` en intention d'ajout
   (`git add -N` sur la copie : la limite « fichiers non suivis » du générateur, levée ; `preuves/finales-h/`).
2. **Frontière — conforme.** AST de chaque module de `recalc` (`outils/ast_frontiere.py`, `preuves/ast-frontiere.txt`) :
   `fusion.py` importe de `collecte` le seul `from ..collecte.decodeurs import DECODEURS, decoder` ; aucun accès
   `sys.modules`, `__globals__`, `__dict__`, `getattr`, `eval`, `exec`, `importlib` dans `recalc`. Fermeture à
   l'exécution, indépendante du test (`sys.modules` après `import shogen_s2bis.collecte.decodeurs`, 3.10 à 3.13) :
   exactement les cinq modules que fixe `test_fermeture_des_decodeurs`, aucun module hors bibliothèque standard
   (`preuves/fermeture-runtime.txt`). Ajout daté au G0 : décision et motif écrits. Limite : Python n'interdit pas à
   l'exécution l'accès aux modules chargés (`sys.modules`) ; seule l'analyse syntaxique le tient.
3. **`run_params` — conforme**, plus C-7 (r02). Clés porteuses, commit, sha256 aux clés exactes, contenus canoniques,
   descripteur, concordance au premier démarrage, `python` non porteuse : tests et mutants c02, c04, c05, c09, c12, r01,
   r09, r12 tués ; liste `observateurs` égale à la liste fermée par le contenu (r09 tué).
4. **Re-décodage — avec C-1 et C-7.** `ok` et `panne_decode` re-décodées, égalité de statut, valeurs, `extra` ; écarts
   listés jamais réparés (f10 tué) ; mutant « sha256 seul comparé » (f01) tué. Défauts : C-1 (base64 non strict et
   dépendant de la version ; décodeur avant le sha256), r03 et r14 vivants (C-7).
5. **Flux — avec C-2 et C-3.** Ruptures, trous, reprises à leur place (d01, d11 tués), `ws` en recul (e01), doubles,
   relecture (e03) : conformes ; mémoire bornée : pic `tracemalloc` de la passe 2 constant (150 fenêtres : 321 852
   octets ; 600 : 317 405, sous 3.11 ; essai E5). Défauts : C-2, C-3.
6. **Témoin et remplaçants — avec C-7.** `est_temoin` sur la classe du décodeur scellé (g01 tué), `blocs` sur `ok` égal
   seulement (g06 tué), `est_remplacant` sur le seul secondaire (g03 tué) ; tests nommés pour les deux items. Vivants :
   r05 (site d'appel), r06 (souligné), r11 (`panne_decode` du témoin) : C-7.
7. **Observateur absent — conforme**, plus C-5. Trois présents avec constat, deux refusés avant toute lecture, un journal
   sur deux refusé : tests ; h01, h05, h08, r08, r10 tués.
8. **Tests — conforme.** Jeux synthétiques écrits par `collecte/journal.py` (et quatre lignes à la main, recul de `ws`) ;
   aucun journal réel. Rouges rejoués (`outils/rouges.sh`, module de test de chaque état sur le code du précédent) :
   b `FAILED (errors=1)`, c `(failures=22, errors=1)`, d `(errors=2)`, e `(failures=5, errors=1)`, f `(failures=1,
   errors=2)`, g `(failures=1, errors=2)`, h `(errors=6)` ; a vert (la règle vit dans le module de test), rouge
   `FAILED (failures=1)` avec l'ancienne règle `recalc` (`preuves/rouge-a-regle-ancienne.txt`), comme l'écrit METRIQUES.
9. **Mutants — six fautes, corrigées (C-7).** Commande du job `s2bis-unittest` par `scripts/controle/mutants.py` du dépôt
   réel, borne 300 s, témoin vivant à chaque campagne, relevé `ps` de fin vide : générateur, échantillon de 25 (`gen1`
   13, `gen2` 12) : 25 tués ; les miens, 12 (`revue`) : 5 tués, 7 vivants (r02, r03, r04, r05, r06, r11, r14) ; arbre
   corrigé (`corr`) : les six vivants applicables rejoués et 8 mutants des corrections : 14 tués, 0 vivant, 0 FATAL.
   Diffs et sorties : `mutants/<liste>/`, classements `preuves/mutants-<liste>.txt`. Chaque tué l'est par un test de
   `test_fusion` ou de `test_fitness` (relevé des FAIL et ERROR de chaque sortie) ; au run de g03, un second FAIL,
   `test_secondaire.Conformite.test_journal_secondaire_conforme_au_format` (temps réel, hors RB-2), sans effet sur le
   classement (§5).
10. **Robustesse — conforme** (essai E3, arbre final) : `brut` `@@@`, `QQ=`, espace, non ASCII, nul, entier, liste :
    `base64` ; JSON profond (200 000 crochets, 100 000 objets), entier géant (5 000 et 100 000 chiffres), exposant
    `1e999999999`, hors UTF-8, vide : `statut` ou `valeurs` ; rien d'imprimé, aucune exception. Sous r03 (vivant), un
    `brut` nul remonterait : C-7 le fixe.
11. **Documentation — avec C-4, C-6, C-8.** METRIQUES : une section par diff, comptes de R-25 recomptés (70, 96, 187,
    180, 54, 106, 106, 75) ; R-13 : aucun TODO ni FIXME ; heures datées ; FORMAT : aucune section ne décrit la fusion
    (§16 [abs] au générateur comme à moi) ; lignes : C-6 ; items : C-8 et §5.

## 3. Arbre corrigé (copie à h, plus RB2-G2-1 et RB2-G2-2)

`preuves/finales-corr/` : runner `153 ok, 0 échec` ; job s2bis `conforme (code 0, résumé final, aucun saut, Ran = 471)` ;
S2 `conforme (… Ran = 423)` ; sim-bis `conforme (… Ran = 279)` ; matrice 3.10 à 3.13 `-X dev -W error` : `Ran 471 tests`,
`OK`, sortie 0, 0 ligne `Exception ignored` ni `Warning` ; xtask : S-G1 à S-G9 `VERT`, fmt, no_std, clippy `VERT`,
`=== VERDICT GLOBAL : VERT ===`, sortie 0 (fichiers neufs en intention d'ajout) ; aucun fichier ignoré sous les chemins
touchés. Tests de `RevueG2` rouges sur le code de RB2-h (`preuves/corr-rouge-python3.11.txt` :
`FAILED (failures=4, errors=2)` ; 3.13 : `failures=3, errors=2`, le remplissage en trop y étant déjà refusé), verts sur
l'arbre corrigé (`Ran 24 tests`, `OK`, 3.11 et 3.13). Essais E1 à E7 rejoués sur l'arbre corrigé : E1 `base64` sous 3.11
et 3.13, E2 `FUSION/relecture`, E4 `FUSION/dossier`, E6 reprise rendue en `sans_fenetre`, E7 0 appel du décodeur
(`preuves/essais-corr-python3.1x.txt`).

## 4. Écarts et limites du réviseur (règle PAROXYSME)

- **E-1** : une énumération récursive `find <copie légère final/> -name __pycache__ -prune -print` (sortie vide), contraire
  à l'interdit du brief ; ensuite, absence de `__pycache__` contrôlée par `git status --short --ignored` limité à des
  chemins listés.
- **E-2** : un premier relevé de la fermeture à l'exécution lancé `python3.11 -B` et `python3.13 -B` sans `-I` ; refait
  sous `-I -B` pour les quatre versions (seule sortie versée).
- **E-3** : écritures d'index hors du dépôt réel : `git init` et `git add` (chemins listés) dans l'arbre d'essai `corr/`,
  `git add -N` de deux fichiers dans la copie ; aucun commit. Le job est lancé `python3 -I -B enforcement/…`, gates.yml
  écrit `python3 -B`.
- **E-4** : une suppression `rm -rf "$G/etat-c"` (variable dans un script `sh -c`) a été arrêtée par la garde de Claude
  Code ; l'arbre léger a été supprimé ensuite par son chemin absolu écrit en toutes lettres, commande à part.
- **E-5** : copie entière, non creuse : les emplacements interdits y sont présents, jamais ouverts ni listés ; la sortie
  complète de `xtask` (qui cite des lignes de documents) a été supprimée, seules les lignes de verdict sont gardées.
- **E-6** : la première relecture interrompue a lancé ses propres campagnes ; ses sorties (dans `ancien/`) ne sont pas
  comptées ; ses listes de mutants ont été relues, recontrôlées (`outils/valider_mutants.py`) et rejouées.
- **Limites** : coût en temps de la fusion sur un volume de campagne non mesuré ; enregistrement G2 par
  `oracle_record.py` non fait (RB-2 n'est pas un lot du chemin S2 soumis au cp-2) ; un autre réviseur (DB-2) travaillait
  en parallèle : mes jobs et campagnes attendaient la fin de ses campagnes de mutants (`outils/attendre.sh`), pas de ses
  suites.

## 5. Items (règle PAROXYSME)

Fermetures proposées par le générateur : justes, à deux précisions près. SHOGEN-S2BIS-TEMOIN-RECALC-1 : ajouter le test
`test_fusion.RevueG2.test_temoin_filtre_par_le_decodeur_de_la_forme` et `test_panne_decode_du_temoin_sans_blocs_et_panne_http_jamais_redecodee`
(C-7) aux tests cités. SHOGEN-S2BIS-CARTE-REMPLACANTS-RECALC-1 : l.2004 ; ajouter `RevueG2.test_suffixe_exact_avec_son_souligne`.

Items proposés par le générateur : RIPESTAT-REDECODAGE-1 (accepté) juste ; DECODEURS-FERMETURE-1 à reformuler
(décision prise : fermeture testée ; reste l'absence d'entrée-sortie non prouvée et l'accès à l'exécution par
`sys.modules`, déclencheur : le sceau) ; FUSION-COUT-1 juste, mémoire de la passe 2 mesurée bornée sur un journal (E5),
durée non mesurée ; ISOLE-LO-1 à ne pas former (périmé, C-8).

Items à former :

| item | constat | propriétaire | déclencheur | prix | origine |
|---|---|---|---|---|---|
| SHOGEN-S2BIS-TEST-SANTE-COURSE-1 | `test_sante.Branchement.test_sante_liste_blanche_sondes_au_depart_jointes_avant_l_echeance` a échoué une fois sur les 24 suites s2bis complètes sans mutant de cette relecture (série 9, rejeux 2, matrices 8, témoins 4, job corrigé 1) (instant de sonde lu une seconde après l'instant attendu, faux temps avancé par le fil de la boucle avant que le fil de la sonde le lise ; machine chargée par un autre lot) ; rejoué deux fois vert | orch. | avant le sceau (le job `--egal` sans saut ne tolère pas un faux rouge) ; à rattacher à SHOGEN-S2BIS-TESTS-TEMPS-REEL-1 si l'orchestrateur le juge de même classe | instant de la sonde pris sous une porte que le test ouvre avant d'avancer le faux temps [inféré] | relecture G2 de RB-2 |
| SHOGEN-S2BIS-TESTS-TEMPS-REEL-1 (précision) | premier échec mesuré : `test_secondaire.Conformite.test_journal_secondaire_conforme_au_format` (un `releve_asn` de plus dans le journal, sous charge) au run du mutant g03 de cette relecture, 2026-10-18 vers 22:00 UTC ; l'item disait « aucun échec mesuré » | orch. | inchangé (avant le sceau) | inchangé | relecture G2 de RB-2 |
| SHOGEN-S2BIS-FUSION-PAQUET-SCHEMA-1 | `fusion.paquet` lit les quatre configurations par `json.loads` simple (clé double, flottant admis) et la fusion lit `observateurs.json`, `formes.json` et `carte.json` sans schéma : un paquet mal formé donne `KeyError` ou `TypeError` non nommés avant tout contrôle ; l'égalité des sha256 à ceux des `run_params` (calculés sur des fichiers que le lecteur strict du collecteur a admis) protège les contenus, pas l'ordre des contrôles | orch. | script d'exécution unique (garde du sha256 du paquet, D.4 b) ou RB-17 | lecture stricte du paquet (forme de `config_analyse`) et refus `FUSION/config` nommés [inféré] | relecture G2 de RB-2 |
| SHOGEN-S2BIS-DECODEURS-UTF16-1 | `decodeurs.decoder` passe les octets à `json.loads`, qui reconnaît UTF-16 et UTF-32 : un corps UTF-16 est décodé `ok` (essai E3, cas `utf16` : écart `valeurs`, non `statut`) ; le lecteur du journal l'avait refusé pour ses lignes (NC-1) | orch. | prochaine ouverture du code gelé des décodeurs (rodage, AVIS Q-C-06) | UTF-8 strict avant `json.loads`, écart à S2 nommé [inféré] | relecture G2 de RB-2 |

## 6. Journal de provenance (G1)

**Sources** (toutes à `709d4a7` sauf les pièces du lot) :

| source | niveau | lu |
|---|---|---|
| `BRIEF-G2.md`, `../BRIEF-RB2.md`, `../BRIEF-RB2-CORR.md`, `../RAPPORT-GENERATEUR.md`, `../NOTES.md` | [lu] | entiers |
| `../diffs/RB2-a.diff` à `RB2-h.diff` | [lu] | entiers, dans l'ordre |
| `docs/adr-0029/g0-collecte/PROPOSITION.md` | [lu] | l.1-80, l.420-440, l.466-474, l.578-585 |
| `docs/adr-0029/g0-collecte/AVIS.md` | [lu] | l.100-112 |
| `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md` | [lu] | l.80-115 (fin, ajouts) |
| `docs/adr-0029/ADR-0029-campagne-S2-bis.md` | [lu] | l.74-80, l.170-176, l.214-224 |
| `docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md` | [lu] | titres ; §9 (l.366-462), §14 et §15 (l.667-846) ; §16 [abs] |
| `docs/adr-0028/ANNEXE-B-items.md` | [lu] | l.1978-2008 (recherche dans ce seul fichier) |
| `docs/adr-0029/s2bis/METRIQUES-S2BIS.md` | [lu] | sections RB2-a à RB2-h (diffs), comptes de lignes longues |
| `s2bis/shogen_s2bis/recalc/lecteur.py`, `collecte/lecture.py` | [lu] | entiers |
| `s2bis/shogen_s2bis/collecte/decodeurs.py` | [lu] | l.1-80, l.200-393 |
| `s2bis/shogen_s2bis/collecte/journal.py` | [lu] | l.137-166, l.234-320, l.399-440 |
| `collecte/entree.py`, `collecte/config.py`, `recalc/config_analyse.py` | [lu] | l.177-190 ; l.15-50 ; ligne de `TEMOIN` |
| `recalc/rotation.py`, `recalc/oracle_indep.py` | [abs] | relevé AST des imports seul |
| `s2bis/tests/test_sante.py` | [lu] | l.160-200 |
| `scripts/controle/mutants.py`, `scripts/controle/README.md` | [lu] | l.1-60 ; l.1-40 |
| `s2bis/config/observateurs.json`, `carte.json` | [lu] | entiers (noms et décodeurs de la carte relevés par `json`) |

**Commandes** (sous `scratchpad/outils/isole.sh`, `TMPDIR` du dossier, `python3 -I -B` ; sorties dans `preuves/`) :

| commande | sortie relevée |
|---|---|
| `git rev-parse HEAD` (dépôt, copie) | `709d4a71694f521fb11490ba889e29aebf0faf1f` |
| `sha256sum -c ../SHA256SUMS` | 345 `OK`, aucun écart |
| `outils/serie.sh` | `preuves/serie/` (§2 pt 1) |
| job à l'état c rejoué deux fois | `conforme … Ran = 453` deux fois |
| `outils/rouges.sh` ; règle ancienne | §2 pt 8 |
| `outils/finales.sh finales-h` ; xtask avec `git add -N` | §2 pt 1 |
| `outils/b64.py` sous 3.10 à 3.13 | `QUJD=` : `b'ABC' NON-CANONIQUE` sous 3.10 à 3.12, `refus Excess padding not allowed` sous 3.13 ; `QR==` admis partout |
| `outils/test_g2_essais.py` sur l'arbre final et corrigé, 3.11 et 3.13 | §1, §2, §3 |
| `scripts/controle/mutants.py <copie> s2bis-unittest mutants/<liste>.json --borne 300` | gen1 13/13, gen2 12/12, revue 5/12 tués ; corr 14/14 ; relevés `ps` vides (28, 26, 26, 30 groupes) |
| `outils/faire_diffs.sh` ; dix diffs sur extraction neuve | `check sortie 0`, `apply sortie 0` ; égaux à `corr/` |
| `outils/finales_corr.sh` | `preuves/finales-corr/` |

**Chiffres recomptés** : planchers (`Ran` de chaque job) ; lignes de code par diff (script sur les `+` des `.py` et
`.yml`) ; tailles des fixtures (`wc -c` : kraken 308, binance 45) ; lignes de plus de 120 caractères (`outils/colonnes.py`,
caractères et non octets).
