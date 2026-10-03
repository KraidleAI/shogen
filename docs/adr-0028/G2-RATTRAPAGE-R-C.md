# R-C — relecture G2 de rattrapage des corrections G2 de la partie 2 (lacune G-3 ; SHOGEN-G2-HISTO-RECALCUL-1)

Rédaction : 2026-10-02, de 21:29:45 UTC (`date -u` au départ) à 21:5x UTC (`date -u` lu à 21:56:28 avant rédaction).
Réviseur G2 neuf (fiche `shogen-worker`, règle 6) : je n'ai écrit aucune ligne de ce code, ni des corrections relues,
ni de leur relecture d'origine. Rattachement : brief commun `p4/BRIEF-G2-RATTRAPAGE.md` (sha256 `396dad51…`),
inventaire `p4/INVENTAIRE-G2-RECALCUL.md` (`2a22f47d…`) §4, lacune G-3 ; mission « R-C » de l'orchestrateur.

## 0. Gate 0, cadre, attestation D.3

- **Gate 0** : modèle résolu `claude-opus-5-5` (identifiant exact fourni par l'environnement de la session) ; préfixe
  attendu des workers (CLAUDE.md §7) : `claude-opus-5-5`, conforme. Effort : `max` (fiche).
- **Dépôt** : `/home/user/shogen`, branche `partie-4-execution`. HEAD à l'ouverture : `e586c0b` ; HEAD à la clôture :
  `35a601e9172a630bd0e55e4386b43de947c33a7c` (commit de l'orchestrateur pendant la relecture : annexe B, inventaire,
  JOURNAL ; `git diff --stat e586c0b HEAD -- s2-harness scripts` vide : code relu inchangé). `git status --short` vide
  au départ et à la clôture.
- **Périmètre** : `git diff 6eabaa4 0711cc1 -- s2-harness/tools/rendu_unique.py s2-harness/tools/oracle_record.py
  s2-harness/shogen_s2/records.py` (3 fichiers, +108 −35 ; sha256 de la sortie du diff `04376368…b8b4`), soit les commits
  `3ef3b25` (G2a : C-1, C-6), `093c076` (G2b : C-2), `cfc67f5` (G2c : C-3), `81b8a87` (G2d : C-4, C-5), `04553a7` (G2e :
  C-7, C-8) ; `15d831e` (G2f, tests seuls) rejoué pour la suite seulement. État relu : celui de HEAD (les lignes du
  périmètre que P3 a réécrites ensuite, `premier` de la voie (b) en `d69c914`, la seconde comparaison de (2) en
  `a6a99d8`, `contexte_decimal()` en `a4e44d0`, sont hors périmètre : relues comme contexte, sans verdict).
- **Code gelé** : aucun fichier du dépôt modifié ; aucun correctif proposé ; constats classés A/B/C (brief).

**Attestation (forme D.3), avec exposition déclarée.**

> « Je n'ai vu aucun z, aucun K, aucun P̂_more ni aucun φ de campagne, et je n'en ai calculé aucun. Je n'ai lu aucun
> taux d'écart ni de panne d'une source de la campagne. Je n'ai ouvert aucune pièce de la liste fermée D.2 (points 1 à
> 12, liste lue à l'annexe D l.32-48 sans ouvrir aucune pièce). »

Exposition déclarée (rien n'est recopié ici) :
1. Le paquet scellé, lu en entier (pièce de référence du brief), porte des comptes de classe M (annexe D.1 n° 7 et 8 :
   D1, D5, comptes de fenêtres des segments) et deux pourcentages de `resolve_failed` dans et hors de la plage (santé du
   résolveur DNS du harnais, « pas une statistique de source » selon le paquet §3 ; classe M, D.1 n° 8) : vus, non
   recopiés, sans usage dans cette relecture.
2. La procédure P5 (`PROCEDURE-EXECUTION.md` l.30) porte les tailles des trois journaux scellés (métadonnées) : vues,
   non recopiées.
3. Un `grep -n` d'en-têtes sur l'annexe D a affiché des lignes de D.1 (descriptions d'expositions, sans valeur), de D.3
   (formules d'attestation) et de D.4 ; aucune valeur de campagne.
4. Un premier `git archive HEAD | tar -x` a copié l'arbre entier dans mon dossier (dont `docs/rapports/`,
   `docs/adr-0025/` et `JOURNAL.md`) ; seuls les noms du premier niveau ont été listés (`ls | head`) ; copie supprimée
   (`rm -rf`) sans aucune lecture, remplacée par `git archive HEAD s2-harness enforcement`, puis `scripts/sceau`.
5. `JOURNAL.md` jamais ouvert ; aucune recherche récursive dans `docs/` (les `grep` visent des fichiers nommés) ; aucun
   `*.jsonl` réel (journaux de fixture seulement : collecteur réel sur horloge factice) ; rien lu hors du dépôt hors de
   `p4/` (le brief, l'inventaire et un `head` du blame de l'inventaire) et de mon dossier ; ni `liste_g2.py` ni aucune
   preuve des dossiers du réviseur de la partie 2 (`g2-partie-2/`) ou du correcteur (`lot-G2corr/`) ouverts : mutants
   reconstitués d'après leur description (§7).
6. `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée (`env | grep -c` : 0 au départ et à la clôture) ; toutes les commandes
   Python sous `env -u SHOGEN_S2_CAMPAGNE_CONTROL PYTHONDONTWRITEBYTECODE=1 python3 -B`, sur des copies `git archive`
   dans mon dossier, jamais dans le dépôt (`find s2-harness -name __pycache__` du dépôt : voir H-2, pas de moi).

## 1. Méthode

1. Lecture des deux pièces qui disent ce que chaque correction devait faire : `docs/G2-partie-2.md` (§3.2, §4, §10) et
   `docs/G1-partie-2-corrections-G2.md` (§3, §5, §6, §7) ; puis du diff entier du périmètre et des trois fichiers à
   HEAD en entier ; confrontation au texte du paquet scellé (§3, §6, §9, §10.2 pt 9, §12), qui fait foi.
2. Pour chaque correction : construction attendue → code → tests qui la portent → mutants → sonde de bout en bout
   quand la construction touche l'exécution réelle.
3. Non-régression : oracles versés de la règle et des épingles sur les arbres `6eabaa4`, `0711cc1` et HEAD ; sorties
   des cinq commandes `--produire` sur une même fixture, `6eabaa4` contre HEAD ; suite rejouée sur l'export de chacun
   des six commits ; suite rejouée dans la condition de production (jeton hérité).
4. Mutants : 30 du réviseur R-C sur les lignes du périmètre, 7 du réviseur de la partie 2 reconstitués ; une copie de
   l'arbre par mutant, ancre unique exigée, témoin d'abord, tout vivant rejoué contre la suite entière.

## 2. Sources lues

Toutes [lu] sauf mention. sha256 mesurés par moi.

- Brief commun l.1-44 (`396dad51…`) ; inventaire l.1-311 (`2a22f47d…`) ; `p4/blame_rendu_unique.py.txt` l.1-5
  (`90b59204…`, format seulement).
- `docs/G2-partie-2.md` l.1-487 (`0b45a458a53878f70b5826653eecc82615b980d7f57ce0317bee5c20391914d9`) ;
  `docs/G1-partie-2-corrections-G2.md` l.1-393 (`736516587f3968849649d345d52f44b9e6a4a4de15a101d519707522381d26e0`) :
  égaux aux sha que cite l'inventaire.
- Code à HEAD, en entier : `s2-harness/tools/rendu_unique.py` l.1-504 (`67b897a9…8f8d9`, égal à `sha256_script` du
  bloc machine du paquet), `s2-harness/tools/oracle_record.py` l.1-274 (`9be02e6b…`), `s2-harness/shogen_s2/records.py`
  l.1-419 (`eab35080…`) ; les deux derniers égaux aux sha finaux du journal des corrections §9.3.
- `docs/adr-0028/PAQUET-PREREG-S2.md` l.1-223 (`494d770d…8097`, sha du paquet du README du sceau) ;
  `docs/adr-0028/ANNEXE-D-preenregistrement.md` (`deb64179…`) l.32-48 (D.2), l.124-168 (D.4) et lignes d'un grep
  d'en-têtes ; `docs/adr-0028/PROCEDURE-EXECUTION.md` l.1-67 (`f386e11e…`) ; `docs/adr-0028/sceau/README.md` l.1-30
  (`5b6d22b1…`) ; `scripts/controle/README.md` (`68a12642…`), `regle_fixtures.py` (`5557fb56…`), `render_fixture.py`
  (`4084c42b…`), en entier.
- Tests à HEAD : `test_rendu_production.py` l.1-435 (`b9da1641…`) ; `test_rendu_unique.py` l.1-141 (`c56e5f46…`) ;
  `test_oracle_record.py` l.117-170 (`b00fcd8a…`) ; `test_lecteur.py` l.102-132 (`0d8c99a6…`) ; `test_sceau.py` (grep des
  chemins).
- Code de la collecte, commit `ed479c5` (lecture du code, aucun journal) : `collector.py` l.60-130 et l.190-260,
  `window.py` l.69-75, `r2.py` l.330-375, `run_campaign.py` l.245-275, `journal.py` l.61-63 ; recensement par `grep` des
  écrivains de `control.jsonl` dans tous les `.py` hors tests.
- `git blame -s -L 420,460 HEAD -- s2-harness/tools/rendu_unique.py`.
- [2nd] : la liste des lignes de HEAD « non lues par P3 » vient de l'inventaire §4 (G-3) ; je n'ai pas relu le rapport
  de P3 pour la vérifier ; je relis ces lignes en entier au §5 quel que soit ce point.
- [abs] : `liste_g2.py` et les preuves du réviseur de la partie 2 et du correcteur (hors de mon dossier, non ouverts).

## 3. Commandes et sorties (dossier `p4/R-C/`)

| commande | sortie |
|---|---|
| `git diff --stat 6eabaa4 0711cc1 -- <3 fichiers>` ; `git log 6eabaa4..0711cc1 -- <3 fichiers>` | 3 fichiers, +108 −35 ; les cinq commits du périmètre |
| `git diff --stat 6eabaa4 0711cc1 -- s2-harness` | dans `shogen_s2/`, seul `records.py` change (C-8) |
| `git diff --stat 0711cc1 HEAD -- <3 fichiers>` | `rendu_unique.py` +31 −16 (P3c à P3f, hors périmètre) |
| `git show --numstat` des six commits | égaux, fichier par fichier, au tableau du journal des corrections §2 |
| suite témoin, copie de HEAD (`s2-harness`, `enforcement`, `scripts/sceau`) | `Ran 383 tests`, `OK (skipped=2)` (`preuves/suite-temoin.out`, `df649aaa…`) ; premier essai sans `scripts/sceau` : 6 erreurs de `test_sceau` (script absent de ma copie partielle, présent dans l'extraction complète de la production), levées en l'ajoutant |
| suite, même copie, `SHOGEN_RENDU_PRODUCTION` hérité sur un répertoire existant à point (condition de production de C-1) | `Ran 383 tests`, `OK (skipped=2)` ; répertoire du jeton vide après (`preuves/suite-avec-jeton.out`, `e4f8e8da…`) |
| suite sur l'export de `6eabaa4`, `3ef3b25`, `093c076`, `cfc67f5`, `81b8a87`, `04553a7`, `15d831e` | 369, 370, 373, 373, 375, 376, 376 tests, chacun `OK (skipped=2)`, au compte de chaque message (`preuves/suites_par_commit.out`, `88131c8b…` ; `commits/*.out`) |
| `regle_fixtures.py` (`5557fb56…`) sur `6eabaa4`, `0711cc1`, HEAD | JSON `ea3a2d94ef1075603e8f7cfc53c68b26e51729b61714028e3fb03dc32f79cb29` trois fois |
| `render_fixture.py` (`4084c42b…`) sur les mêmes arbres | `4e62fbb8…` sans option, `d079dd9d…` avec, trois fois (épingles en vigueur) |
| sonde 5, `sondes/sonde_non_regression.py` (`bf3c564b…`) | `--produire` J14 principal, J14 second, J28, raw : identiques à l'octet entre `6eabaa4` et HEAD ; recalcul tiers : mêmes valeurs r1, d5, lm, r2, segment, plages, hors des clés `etiquette` et `avertissements` (`preuves/sonde_non_regression.out`, `91033062…`) |
| hôte : `git cat-file blob HEAD:<f> \| sha256sum` et `sha256sum <f>` pour les deux outils ; `git check-attr -a` ; `core.autocrlf`, `core.attributesFile` ; `.git/info/attributes` | blob = disque (`67b897a9…`, `9be02e6b…`) ; `text: auto`, `eol: lf` ; non posés ; absent : la garde (4) étendue par C-2 se lève sur l'hôte |
| `git rev-parse --verify HEAD^{commit}` ; `git diff --quiet 41f087e HEAD -- <CHEMINS>` ; `git status --porcelain --untracked-files=all --ignored -- <CHEMINS>` | `35a601e…` ; code 0 ; vide |
| `grep` des appelants de `filtre_horodatage`/`filtre_lecture`/`parse_control`/`parse_asn` ; des écrivains de stderr ; des normalisations de chemin dans `shogen_s2/` | `control.jsonl` toujours lu sans `parse_float` ; seul écrivain de stderr : `records.py` l.97 ; aucune normalisation (`abspath`, `realpath`, `Path`) |
| sondes 1 à 6 (§4, §6, §8) | `preuves/sonde_*.out` (sha au §10) |
| moteur de mutants (`mutants/moteur.py`, `e24b463b…` ; `mutants/liste.py`, `c675b42c…`) | §7 (`preuves/mutants.out`, `7867ff7b…` ; `preuves/mutants-M30.out`, `7e3aadcf…`) |

## 4. Correction par correction

| correction | construction attendue (G2 §10) | code à HEAD | tests, mutants, sondes | verdict |
|---|---|---|---|---|
| C-1 (`3ef3b25`) | jeton `SHOGEN_RENDU_PRODUCTION` posé par `produire_tout` sur le temporaire voisin (chemin absolu) avant l'enregistreur, retiré en `finally` ; `--produire` refuse (code 2, sortie vide, motif) sans jeton sur un répertoire existant à point | l.37, l.378-382 (avant toute autre chose), l.434, l.453 ; `tmp` absolu (`mkdtemp(dir=<abspath>)`) | M01, M03, M04 tués ; M02 vivant, équivalent (§7) ; sonde 6 (a) : appel à la main sans jeton : code 2, 0 octet ; suite entière avec jeton hérité : verte, rien écrit dans le temporaire | conforme |
| C-6 (`3ef3b25`) | au rôle « rendu », `noms des runs == ["suite", *PRODUCTION]` | `oracle_record.py` l.225-226 ; `RUNS` (`rendu_unique.py` l.54) = `["suite", *PRODUCTION]` (`oracle_record.py` l.31) | M23, M25 tués ; M24 vivant (constat C-3) | conforme |
| C-2 (`093c076`) | (i) HEAD résolu une fois, lu par (1), (2), voie (b), enregistreur, relecture ; (ii) (4) : blobs de `<head>` égaux au script lancé et à l'enregistreur chargé | `head` l.132-140 (paresseux, premier appel en (1), écart déclaré au journal §5 pt 1) ; l.153, l.166-168, l.194-201, l.269, l.435, l.442 | M05 à M10 tués ; R27 tué ; blobs = disque sur l'hôte | conforme |
| C-3 (`cfc67f5`) | S, Gc par `git log -S` ; refus si Gc = S, S non ancêtre de Gc, ct(Gc) ≤ ct(S), date hors [ct(S) ; ct(Gc)] ; T0 = ct(Gc) | l.250, l.255-261 (`premier` réécrit par `d69c914`, hors périmètre) | M11 à M14 tués ; R01, R02 tués ; voie (b) hors du chemin de l'exécution prévue (jeton FreeTSA au sceau, aucun `GO-sans-ancre.txt` à HEAD) | conforme ; serrage de bord (constat C-4) |
| C-4 (`81b8a87`) | refus `sortie` si une entrée `.<nom de --sortie>.*` existe dans le parent, avec ou sans `--deviation` | l.346-350, avant toute autre règle de `destination` | M15, M16, R05 tués ; sonde 6 (b) : SIGKILL du groupe pendant la production réelle, débris `.sortie.*` (sorties `suite`, `j14-principal`), puis `--gardes-seules` : refus `sortie`, code 2 | conforme ; trou de forme d'argument (constat C-1) |
| C-5 (`81b8a87`) | calcul sous `redirect_stderr` ; avertissements sans le préfixe du dossier des journaux ; étiquette, avertissements, rendu ; clé `avertissements` ; raw : verdict puis avertissements | l.391-414 | M17 à M20 tués ; R28 vivant, équivalent (P2 §4.1, toujours vrai) ; sonde 4 : aucun avertissement Python parasite capturé, même sous `-W always` | conforme pour les avertissements ; résidu sur le verdict `raw` (constat B-1) |
| C-7 (`04553a7`) | clé `etiquette` par entrée du recalcul tiers (texte de la variante incluse) ; étiquette du J28 complétée | l.47-49, l.52-53 (`INCLUSE` hors des délimiteurs), l.400-403 | M21, M22, R20 tués ; sonde 5 : valeurs inchangées ; étiquette du J28 confrontée au paquet §10.2 pt 9 : les six items du pt 9 qui concernent le J28 y sont nommés, les J14 et la seconde coupe ont leur étiquette (l.43, l.45) ; paquet §6 (« texte exact : l.43-49 ») concorde | conforme |
| C-8 (`04553a7`) | `ValueError` nommée si l'horodatage est booléen, ni `int` ni `float`, ou non fini | `records.py` l.33, l.355-357, l.369-372 (trois champs, avant le segment) | M26 à M28 tués ; M29, M30 vivants (constat C-2) ; code de collecte `ed479c5` [lu] : `window_start` entier (`window.window_start` rend `int`), `harness_ts` = `now_fn()` (`time.time()`), `ts` = `time.time()` (`collect_asn` ; le dictionnaire d'attribution n'a pas de clé `ts` qui l'écraserait) ; seuls écrivains de `control.jsonl` : `collector.collect`/`clock_check`, `r2.collect_asn` | conforme ; sans effet sur des journaux écrits par ce code [lu] ; une réparation manuelle des journaux (pièces REPAIR-* de D.2 n° 8, non ouvertes) n'est pas couverte [inféré] |

Non-régression, toutes corrections : règle et épingles identiques sur `6eabaa4`, `0711cc1`, HEAD ; sorties de
`--produire` identiques (sonde 5) ; chaque commit vert au compte de son message.

## 5. Lignes de HEAD non lues par P3 (inventaire, G-3) : relecture

| fichier, lignes | commit | relu | constat |
|---|---|---|---|
| `rendu_unique.py` l.48-49 | `04553a7` | étiquette du J28 complétée (§4, C-7) | aucun |
| `rendu_unique.py` l.52-53 | `04553a7` | `INCLUSE`, hors des délimiteurs de la table (la substitution de `monter_prod` ne l'efface pas) | aucun |
| `rendu_unique.py` l.250 | `cfc67f5` | `fromisoformat` sur la date du go : toujours datée (motif `GO` : `Z` ou `+00:00`) ; Python 3.11.15 lit `Z` | aucun |
| `rendu_unique.py` l.255-263 | `cfc67f5` | ordre S/Gc, ascendance, ct, bornes de date, `return tg` ; l.262-263 lignes vides | C-4 (serrage de bord) |
| `rendu_unique.py` l.346-350 | `81b8a87` | motif échappé (`glob.escape` du parent et du nom), pas de débris lu sur un parent absent (liste vide) | C-1 (barre finale) |
| `rendu_unique.py` l.374-377 | `3ef3b25`, `81b8a87` | docstring de `produire`, fidèle au code | aucun |
| `rendu_unique.py` l.378-382 | `3ef3b25` | contrôle du jeton, avant `argparse` ; `basename` d'un chemin sans barre finale | C-5 (nom `v` réutilisé l.394, sans effet) |
| `rendu_unique.py` l.391-394 | `81b8a87` | `redirect_stderr` ; branche raw | B-1 |
| `oracle_record.py` l.191-192 | `3ef3b25` | docstring de `verifier` | C-5 (ligne coupée) |
| `oracle_record.py` l.225-226 | `3ef3b25` | contrôle des runs (§4, C-6) | C-3 (test) |
| `records.py` l.33, l.355-357, l.369-372 | `04553a7` | `import math` utilisé l.370 ; docstring fidèle ; contrôle C-8 | C-2 (test) |
| (`093c076`, 25 lignes, lues par P3 comme état final) | `093c076` | verdict sur C-2 : §4 | aucun |

## 6. Constats

### B-1 — verdict `raw` en refus : chemin absolu du dossier des journaux dans la sortie (résidu de C-5)

- **Lieu** : `rendu_unique.py` l.393-398 (`except ValueError as e: texte = f"refus — {e}"`), avec `records.py` l.103-106
  (`ValueError` « ligne … NON finale dans {path} »), hors de la réécriture de C-5 (l.408, avertissements seulement).
- **Scénario** : `raw.jsonl` porte une ligne corrompue non finale → le run `raw` sort 0 avec le verdict « refus — ligne
  JSON corrompue NON finale dans `<chemin absolu du dossier des journaux>`/raw.jsonl (ligne k) : … » → les octets de la
  sortie `raw`, leur sha256 (enregistrement de rôle rendu, ligne JOURNAL de l'exécution) et les rendus versés au dépôt
  (procédure §5) dépendent du dossier des journaux sur l'hôte (`$J`, scratchpad de la session) ; un tiers qui rejoue
  avec les mêmes journaux ailleurs obtient d'autres octets. C'est l'objet même de C-5 (G2 §3.2 pt 6 : « les octets et le
  sha256 consigné dépendent de ce chemin » ; message de `81b8a87` : « octets indépendants du chemin des journaux »). La
  construction littérale de C-5 ne visait que les avertissements : le correcteur l'a appliquée telle quelle ; le résidu
  est dans l'objectif, pas dans l'application.
- **Preuve** : sonde 1, `sondes/sonde_raw_chemin.py` (`302bde8f…`), sortie `preuves/sonde_raw_chemin.out`
  (`9549370a…`) : mêmes journaux de fixture (ligne 2 de `raw.jsonl` coupée) dans deux dossiers, lancement comme
  l'enregistreur (argv de `COMMANDES`, stderr fusionnée, jeton posé) : exit 0 les deux fois ; sha256 `fb7945a1…` et
  `4a57ac06…` ; sorties différentes, chemin absolu présent.
- **Décision** : aucune valeur de la règle ne bouge (verdict `raw` hors décision, Q7, sortie 0 quel que soit le
  verdict).
- **Plausibilité sur les journaux réels** [inféré] : `journal.append_jsonl` (`ed479c5`, `journal.py` l.61-63) ouvre en
  ajout et écrit `json + "\n"` sans réparer une fin coupée ; une coupure pendant l'écriture d'une ligne de `raw.jsonl`
  suivie d'une reprise (prise en charge par `run_campaign`) laisse une ligne corrompue non finale. Seul `raw.jsonl` peut
  être touché pour que le cas se produise : la même corruption dans `journal.jsonl` ou `control.jsonl` ferait échouer
  les runs J14 avant `raw` (fail-closed, hors périmètre). Non mesurable sans ouvrir les journaux (D.4 a) ; SHOGEN-RAW-
  FIN-1 déclare le verdict inconnu avant l'exécution.
- **Classe B.**

### C-1 — `--sortie` terminé par « / » : débris d'une tentative interrompue non vus (C-4)

`destination` (l.346-347) normalise (`abspath`) et cherche `.sortie.*` ; `produire_tout` (l.426, hors périmètre) nomme
son temporaire `.<basename(cible)>.` ; avec `--sortie <d>/sortie/`, `basename` est vide : temporaire `..xxxx`, invisible
au motif ; une nouvelle tentative n'est pas refusée. Écart au paquet §9 l.106 (« Des débris d'une tentative
interrompue font refuser l'exécution suivante ») pour cette forme d'argument. Preuve : sonde 3,
`sondes/sonde_barre_finale.py` (`19f84f83…`), `preuves/sonde_barre_finale.out` (`854d830d…`) : sans barre, refus
nommé ; avec barre, « aucun refus (débris non vus) ». Sans effet sur les sorties ; la procédure P5 §3 écrit `--sortie
docs/adr-0028/execution/rendu-<date>`, sans barre finale. **Classe C.**

### C-2 — test de C-8 : `window_start` et `harness_ts` non couverts

M30 (contrôle restreint à `ts`) et M29 (contrôle seulement sous segment) passent la suite entière : le test
`TestTsNumerique` (`test_lecteur.py` l.102-116) ne pose que `ts` d'un `asn_attribution` sous segment. Le code contrôle
bien les trois champs ; M29 est équivalent sur le chemin de production (toutes les sorties passent un segment ; l'appel
à plage seule de `report.py` l.238 porte sur des enregistrements déjà contrôlés). Trou de test, sans effet sur les
sorties. **Classe C.**

### C-3 — test de C-6 : `suite` en tête non exigé par un test

M24 (`noms[1:] == list(PRODUCTION)`) passe la suite entière : les tests refusent l'enregistrement à un seul run `suite`
et l'ordre inverse, pas un enregistrement à six runs dont le premier n'est pas `suite`. Le code est juste. **Classe C.**

### C-4 — voie (b) : serrage de bord au-delà du texte du paquet

`rendu_unique.py` l.256 refuse `tg <= ts` (ct(Gc) ≤ ct(S)) même pour un Gc descendant strict de S ; le paquet §9 l.103
dit « dans un commit descendant strict du commit du scellement, la date du go comprise entre ces deux commits » : un go
daté de la seconde du scellement, épinglé par un descendant strict commis dans la même seconde, passe le texte et est
refusé par le code. Serrage fail-closed, cohérent avec D.4 c (« postérieur au scellement ») ; voie (b) hors du chemin de
l'exécution prévue (voie (a)). **Classe C.**

### C-5 — style, sans effet

`oracle_record.py` l.191-193 : docstring coupée après « sha256 d'un » ; `rendu_unique.py` l.155, l.158, l.254 : motifs
« à HEAD » alors que la lecture porte sur le commit résolu (la docstring de g1 dit `<head>`) ; l.394 : `v` (verdict)
réemploie le nom du jeton de l.378. **Classe C.**

Aucun constat de classe A dans le périmètre.

## 7. Mutants

Moteur `mutants/moteur.py` (`e24b463b…`), liste `mutants/liste.py` (`c675b42c…`) ; témoin sans mutation : suite
entière `Ran 383`, `OK (skipped=2)` (deux fois). Sorties : `preuves/mutants.out` (`7867ff7b…`, 21:44:04 à 21:48:38 UTC)
et `preuves/mutants-M30.out` (`7e3aadcf…`).

| id | correction, ligne | mutation | issue |
|---|---|---|---|
| M01 | C-1, l.379 | `isdir` → `exists` (fichier admis) | tué (`test_produire_reserve…`) |
| M02 | C-1, l.453 | retrait du `pop` du jeton | **vivant**, équivalent : après succès ou échec, le chemin du jeton n'existe plus (renommé ou retiré) et le processus de production se termine |
| M03 | C-1, l.434 | jeton posé sur le parent du temporaire | tué (`test_nominal_bout_en_bout`) |
| M04 | C-1, l.379 | point initial non exigé | tué |
| M05 | C-2, l.197 | enregistreur retiré de (4) | tué (2 tests) |
| M06 | C-2, l.197 | script retiré de (4) | tué |
| M07 | C-2, l.139 | `head` = « HEAD » | tué (9 échecs) |
| M08 | C-2, l.153 | (1) relit « HEAD » | tué |
| M09 | C-2, l.199 | (4) relit « HEAD » | tué |
| M10 | C-2, l.435 | enregistreur sur « HEAD » | tué |
| M11 | C-3, l.256 | `tg <= ts` → `tg < ts` | tué |
| M12 | C-3, l.258 | borne haute de la date retirée | tué |
| M13 | C-3, l.258 | borne basse retirée | tué |
| M14 | C-3, l.256 | ascendance retirée | tué |
| M15 | C-4, l.348 | débris ignorés sous `--deviation` | tué |
| M16 | C-4, l.347 | point initial du motif retiré | tué |
| M17 | C-5, l.408 | préfixe sans séparateur final | tué |
| M18 | C-5, l.414 | avertissements après le rendu | tué |
| M19 | C-5, l.391 | capture retirée | tué |
| M20 | C-5, l.411 | clé `avertissements` retirée | tué |
| M21 | C-7, l.400 | étiquette du J28 reprise pour la variante incluse | tué |
| M22 | C-7, l.49 | drapeau du run maximal retiré de l'étiquette | tué |
| M23 | C-6, l.226 | seul `suite` en tête exigé | tué |
| M24 | C-6, l.226 | `suite` non exigé (`noms[1:]`) | **vivant** (constat C-3) |
| M25 | C-6, l.226 | comparaison sans ordre | tué |
| M26 | C-8, l.370 | non fini admis | tué |
| M27 | C-8, l.370 | booléen admis | tué |
| M28 | C-8, l.370 | chaîne admise | tué (TypeError au lieu du refus nommé) |
| M29 | C-8, l.370 | contrôle sous segment seulement | **vivant** (constat C-2 ; équivalent en production) |
| M30 | C-8, l.370 | contrôle sur `ts` seulement | **vivant** (constat C-2) |
| R01 | P2, voie (b) l.253 | première occurrence du go → dernière | tué |
| R02 | P2, `GO` l.33 | décalage horaire quelconque | tué |
| R03 | P2, g2 l.166 | `--no-textconv` retiré | vivant, équivalent (P2 §4.1) |
| R05 | P2, `destination` l.352 | `lexists` → `exists` | tué |
| R20 | P2, l.400 | variante incluse prise sur les sorties sans plage | tué |
| R27 | P2, l.442 | relecture sans `--depot` | tué |
| R28 | P2, l.410 | JSON hors du contexte nommé | vivant, équivalent (P2 §4.1) |

Bilan : 37 mutants ; 31 tués ; 6 vivants : M02, R03 et R28 équivalents ; M29 équivalent sur le chemin de production
seulement ; M24 et M30 non équivalents (trous de test, code juste), portés avec M29 par les constats C-2 et C-3. Les
mutants R reconstitués portent sur les lignes que leur description désigne ; R04, R06 à R19, R21 à R26, R29 visent des
lignes hors du périmètre.

## 8. Signalements hors périmètre (règle PAROXYSME)

### H-1 — dossier parent de `--sortie` absent : exception après « gardes levées » (A par la lettre du brief)

- **Lieu** : `rendu_unique.py` l.426 (`397605c`, relu en P2) : `tempfile.mkdtemp(…, dir=<parent de --sortie>)` est hors
  du `try` de `produire_tout`.
- **Scénario** : la procédure P5 §3 (`PROCEDURE-EXECUTION.md` l.40-41) passe `--sortie
  docs/adr-0028/execution/rendu-<date>` ; `docs/adr-0028/execution/` n'existe pas à HEAD (`git ls-tree`, `ls`) et
  aucune étape de la procédure ne le crée. `--gardes-seules` sort 0 (rien n'est créé) ; la commande de production
  imprime « gardes levées », puis lève `FileNotFoundError` non rattrapée : trace Python, sortie 1, aucun run, rien
  d'écrit ; la ligne « échec de production à <heure> » (SHOGEN-RENDU-ECHEC-DIAG-1) n'est pas imprimée.
- **Preuve** : sonde 2, `sondes/sonde_parent_absent.py` (`38ba043b…`), `preuves/sonde_parent_absent.out` (`7f38fa31…`) :
  parent présent, code 0 et six runs ; parent absent, « gardes levées » puis `FileNotFoundError`, aucun run, rien
  d'écrit.
- **Effet** : aucune valeur fausse ; une tentative échouée (pas une seconde exécution, Q8), à consigner au JOURNAL.
  Classe A au sens littéral du brief (« faire échouer l'exécution (exception) »), levable sans code : créer le dossier
  parent avant le §3 de la procédure (ou choisir un `--sortie` dont le parent existe). À porter à l'orchestrateur avant
  l'exécution (échéance du délai : 2026-10-03T17:44:30Z).

### H-2 — `s2-harness/tests/__pycache__/` dans l'arbre de travail du dépôt (observation, sans effet)

Né le 2026-10-02 à 04:36:57Z (`stat`), avant cette session ; ignoré (`.gitignore` l.33) ; hors des chemins de la garde
(2) et du contrôle `find` de la procédure §1 ; `git archive` ne l'emporte pas. Pas de moi (aucune commande Python dans
le dépôt).

## 9. Verdict

**ACCEPTE-AVEC-CONSTATS** sur le périmètre : les huit corrections du code (C-1 à C-8) font ce que leur construction
demandait, sans régression mesurée (règle, épingles, sorties de production, suites par commit) ; aucun constat A ; un
constat B (B-1, résidu de l'objectif de C-5 sur le verdict `raw`) ; cinq constats C. Hors périmètre, **H-1** (classe A
par la lettre, exception à l'exécution si la procédure P5 est suivie telle quelle) est à porter immédiatement à
l'orchestrateur.

## 10. Clôture

- Sorties de preuve (sha256) : `suite-temoin.out` `df649aaa…`, `suite-avec-jeton.out` `e4f8e8da…`,
  `suites_par_commit.out` `88131c8b…`, `sonde_raw_chemin.out` `9549370a…`, `sonde_parent_absent.out` `7f38fa31…`,
  `sonde_barre_finale.out` `854d830d…`, `sonde_avertissements.out` `7bba3378…`, `sonde_non_regression.out` `91033062…`,
  `sonde_coupure.out` `5cac877a…`, `mutants.out` `7867ff7b…`, `mutants-M30.out` `7e3aadcf…` ; sondes : `sonde_raw_chemin.py`
  `302bde8f…`, `sonde_parent_absent.py` `38ba043b…`, `sonde_barre_finale.py` `19f84f83…`, `sonde_avertissements.py`
  `2ceacee6…`, `sonde_non_regression.py` `bf3c564b…`, `sonde_coupure.py` `081b16ab…`, `suites_par_commit.sh` `45bd3f1e…` ;
  oracles : `oracles/regle-*.json` `ea3a2d94…` (trois), `oracles/rendu-*.txt` `2e366a91…` (trois).
- Copies d'arbre supprimées (`arbre/`, `oracles/arbre-6eabaa4/`, `oracles/arbre-0711cc1/`, exports de `commits/`,
  `mut/`, `tmp/`) ; restent dans `p4/R-C/` : ce rapport, `sondes/`, `mutants/`, `preuves/`, `oracles/` (sorties),
  `commits/*.out`.
- Effets de bord déclarés : (a) les deux suites du §3 lancées sans `TMPDIR` (témoin, jeton hérité) ont laissé leurs
  répertoires temporaires de test dans le répertoire temporaire du système ; non retirés (indiscernables de ceux
  d'autres relectures en cours), jamais lus ; tous les autres lancements avaient `TMPDIR` dans mon dossier, retiré ;
  (b) le premier `git status --short` a été lancé sans `--no-optional-locks` (rafraîchissement possible des métadonnées
  de l'index, aucun contenu) ; les lectures git suivantes du dépôt l'avaient pour la plupart.
- Aucune opération git en écriture ; aucun fichier du dépôt modifié ; `git status --short` vide à la clôture ;
  `SHOGEN_S2_CAMPAGNE_CONTROL` et `SHOGEN_RENDU_PRODUCTION` absentes de l'environnement (`env | grep -c` : 0).
- R-13 : aucun marqueur de dette nu dans ce rapport ni dans les sondes.
- Sha256 de ce rapport : dans la remise à l'orchestrateur (un fichier ne porte pas son propre sha).
- Dettes : aucune hors des constats B-1, C-1 à C-5 et des signalements H-1, H-2, rendus à l'orchestrateur.
