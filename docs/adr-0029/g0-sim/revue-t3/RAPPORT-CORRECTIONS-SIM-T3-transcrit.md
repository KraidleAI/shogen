# Rapport du worker — corrections de SIM-BIS tranche 3 (transcrit)

> Transcription par l'orchestrateur le 2026-10-05 09:28:59 UTC du rapport rendu par message par le worker (agent aef2058e8f1b80b8d) ; contrôle FM-1.1 du transcript : fragments_l51_l14 = 0. Texte du worker ci-dessous, sans retouche.

claude-opus-5-5

# Rapport : corrections G2 et avis de la tranche 3 de SIM-BIS (diffs SB-8D à SB-8G, après SB-8C)

- **Horloge** (`date -u`) : 2026-10-05, de 07:43:51 à 09:27:15 UTC.
- **Dépôt** : lu seulement, avec `git --no-optional-locks`. Aucune opération git en écriture. `git status --short` est vide au début et à la fin.
- **Tête du dépôt** : 31643485… au début, f5915a57… à la fin. L'orchestrateur a commis 12 commits RECALC-BIS pendant le lot (voir E-10).
- **Base de travail** : celle du brief. Copie `git archive 3164348` avec les 7 exclusions, 751 fichiers. Les 9 diffs de la tranche 3 y sont appliqués après contrôle de leurs sha256 (9 sur 9 OK). L'état obtenu est égal à `sim3/etapes/c8c` sur ses 21 fichiers.
- **Verdict attendu de ma part** : livraison complète. Toutes les adjudications de la liste fermée sont traitées. Une seule pièce sort de la série SIM : le texte de la règle pour ROTATION.

## Résumé, point par point

1. **Livraison** : quatre diffs en série.

   | diff | contenu | code ajouté / retiré | plancher |
   |---|---|---|---|
   | SB-8D | C-1, C-2 | +80 / −13 | 119 → 122 |
   | SB-8E | P-7, O-4, O-1 | +106 / −24 | → 125 |
   | SB-8F | Q-T3-7, Q-T3-13, Q-T3-15 | +112 / −37 | → 127 |
   | SB-8G | P-2 : valeurs Q-T3 dans parametres.json | +95 / −28 | → 128 |

   - Chaque état passe la commande du job à son plancher exact : runner 33 sur 33, puis la ligne de `gates.yml`, verdict conforme.
   - Aucun octet 92 dans les diffs ni dans `scripts/sim-bis`. Plus longue ligne Python : 120 caractères.
2. **C-1** : `oracle()` refuse `REGLE/oracle` quand, S suivie, la réponse à « C_S ≤ seuil » diffère entre l'arrêt anticipé et le mode complet.
   - T-REG-2 est étendu aux 60 premières instances avec S suivie. Elles couvrent C_S ≤ 9 et > 9, des arrêts et des passes complètes, dont une passe que seul C_S retient.
   - Cas forcé par `mock` sur le C_S de `complet` (instance 2).
   - Rouge avant le code : 1 FAIL (« Refus not raised »), 0 ERROR.
3. **C-2** : trois tests neufs, chacun rouge sous son mutant (FAIL) et vert sur le code (`journal/c2-rouge-sous-mutant.txt`).
   - (a) `test_artefacts_consolides_e_s_21` : tue V-02 et V-25.
   - (b) `test_unites_series_nulles_e_s_28` : tue V-22.
   - (c) `test_loi_des_absences_parametres` : tue V-20. Les longueurs observées sont exactement {5, 180, 4 320}.
4. **C-3** : le recompte des octets 92, fichier par fichier, est en fin de rapport.
5. **Q-T3-7 (modifié)** : `couche["perte"]` vaut désormais W, en semaines.
   - L'instant est tiré sur W × 7 jours, jour puis fenêtre du jour, jamais sur T_max.
   - Refus `OBSERVATEURS/perte` si W n'est pas un entier ≥ 1, ou si la durée nominale dépasse l'horizon.
6. **Q-T3-13 (modifié)** : `loi_evenements` rend, pour chaque g, `{"E", "C" = #{E^(r) ≥ E}, "C_bas" = #{E^(r) ≤ E}}`.
   - Un cas écrit à la main.
   - Un oracle naïf : décalages refaits par hashlib, rotation position par position, événements sur la suite linéaire. 30 instances, R = 40, les quatre g.
7. **Q-T3-15 (modifié)** : aucun code ne change, la règle tient déjà par construction. `premiere()` est calculée après les retraits et avant `filtrer`. Si l'unité est absorbée, elle manque à la classe et `rotation()` décale toutes les unités.
   - La règle est écrite dans les docstrings de `premiere` et de `filtrer`, et dans celle du module.
   - Un test de caractérisation la fixe ; le mutant M-8F-06 (« première unité présente non décalée ») est tué.
   - ROTATION : patch hors série, plus bas.
   - La ligne pour RB-7 est plus bas.
8. **Valeurs Q-T3-2 à Q-T3-16 (P-2)** : écrites dans `parametres.json`.
   - `observateurs.questions` (Q-T3-2 à 12, et 16) et `regle.questions` (Q-T3-13 à 15).
   - Chaque texte porte la valeur et sa source : lignes de l'AVIS-SIM-T3 (sha256 da343918…) et de la PROPOSITION.
   - La provenance est dans les deux `source` : adjugé le 2026-10-05, avant E0, par le brief des corrections (fa243d23…).
   - Le schéma impose la forme : prédicat `commun.question`, texte qui cite les deux pièces.
   - Le numéro Q-T3-n est marqué dans le module qui emploie la valeur.
   - Test `test_valeurs_avis_t3` : présence, refus de schéma, marques. Rouge : 1 FAIL, 0 ERROR.
9. **P-7** : noms d'unité limités à `[a-z0-9.-]`, de 1 à 253 caractères (`NOM_UNITE`, `LONG_UNITE`).
   - Le refus `REGLE/libelle` est levé dans `_cle`. Ses appelants lui passent les noms : `decalage`, et `_controler` pour `tester`, `deux_modes`, `oracle` et `loi_evenements`. L'unité non décalée est comprise.
   - « ␠! » et « ~ », admis jusqu'ici, sont refusés. Les dix noms courts et les noms DNS passent.
   - Vérifié en lecture seule à f5915a5 : la règle est équivalente à celle commise pour RB-6, `HOTE = re.compile("[a-z0-9.-]{1,253}")` en `fullmatch`. Les six vecteurs du contrat commis (9db81092…) sont ceux du test de SB-8C.
10. **O-1** : en stress, la loi regroupée somme désormais EP sur la liste scellée `sources.indices_hotes`, et non plus sur le pool opérationnel.
    - Un hôte sans ligne d'EP lève `SOURCES/loi`.
    - Test `test_loi_regroupee_ancree_o_1` : pool sans coinbase, loi d'okx = 1×662 2×11, état des autres hôtes égal à l'octet, calme et stress présents. Rouge : FAIL, le pool réduit donnait 1×651.
11. **O-4** : `Couche()` refuse `OBSERVATEURS/indice` quand `ue` ou `repli` est ≥ M. Rouge : FAIL.
12. **Mutants** : commande du job, borne de 300 s. Durée la plus longue : 96,7 s.

    | campagne | résultat |
    |---|---|
    | réviseur, V-01 à V-28 | 28 tués sur 28. V-10 et V-12 sont adaptés en V-10a et V-12a (ligne changée, même mutation). V-02, V-20, V-22 et V-25 sont morts. |
    | neufs, M-8D-01 à M-8G-03 | 20 tués sur 20 |
    | tranche, mes 248 (dix adaptés en « a ») | 247 tués sur 248. R-28 reste vivant : c'est la limite écrite. |

    Total : 296 mutants, 295 tués, 0 FATAL.
13. **Identité bit à bit** : Python 3.10 à 3.13 × PYTHONHASHSEED 0, 1, 4242 et aléatoire.
    - Témoin c8c : les quatre anciennes empreintes sont reproduites.
    - Sur c8g, sondes de la tranche 2 : 8d97a9dc… et d3ba1eb6…, inchangées, 16 sur 16 chacune.
    - **Nouvelles empreintes déclarées** :
      - sonde T3 du worker : `8895661a7022d00df7bc0e12ae75c22d1606f29b922b636c01b6af3b9c96beab`, 16 sur 16 ;
      - sonde T3 du réviseur : `03304e5e098402dc7744256d89bb3e18a356fd939ca98bd664d32c0e25ca170f`, 16 sur 16.
    - Ces sondes sont dérivées des originales : perte en semaines, clé C_bas. En mode « compat », qui retire C_bas, elles redonnent sur c8g les anciennes empreintes 42e935b0… et a7cf3bab…. La seule différence de sortie est donc la clé ajoutée.
    - **O-1** :
      - O-1 ne change aucune empreinte de pool complet : les mêmes 10 hôtes sont sommés.
      - Sonde neuve à pool réduit, sans coinbase, en calme et en stress : c8d, avant O-1, rend 59a7de6f… « instable » ; c8g rend `b1310f64a649ff81b145bc2f85355a45d66354a1504cab350c5a8cd36015315e` « stable », 16 sur 16.
    - Mode strict `-X dev -W error` : 128 tests OK, 8 fois sur 8.
14. **Portes sur l'état final** :
    - runner 33 sur 33 ; sim-bis 128 ;
    - s2bis 114 et s2-harness 405 (2 sauts qui nomment la variable), tous deux sous `unshare -n` avec lo allumée par `isole.sh` (ebaa1c78…) ;
    - hooks 54 sur 54, épinglage 95 sur 95, secrets 147 sur 147 ; `--tree` OK (20 fichiers) ;
    - R-13 : 0 constat sur 19 fichiers ;
    - `cargo --locked xtask verify` : S-G1 à S-G8 VERT ; fmt, no_std et clippy VERT ; S-G9 ROUGE, 1 violation, `docs/17-modele-de-menace.md:70`. Identique sur la base témoin.
15. **Nouvelle tête f5915a5** (contrôle sur copie, aucune base avancée) : les 13 diffs s'appliquent. `scripts/sim-bis` est égal à c8g et le job est conforme à 128 (`journal/sur-tete-f5915a5.txt`).

## Rouges avant le code (FAIL seulement, 0 ERROR)

| diff | tests rouges | pièce |
|---|---|---|
| SB-8D | 1 : T-REG-2 ; puis les 4 cas de C-2, rouges sous V-02, V-25, V-22 et V-20 | `journal/rouge-SB-8D.txt`, `journal/c2-rouge-sous-mutant.txt` |
| SB-8E | 5 : O-4, P-7, deux sous-cas du test des refus RB-6, O-1 | `journal/rouge-SB-8E.txt` |
| SB-8F | 3 : perte, événements, oracle. Remontré avec les tests finaux sur le code de c8e (E-2). | `journal/rouge-SB-8F.txt` |
| SB-8G | 1 : `test_valeurs_avis_t3`. Remontré avec le test final sur le code de c8f (E-3). | `journal/rouge-SB-8G.txt` |

## ROTATION et ligne pour RB-7 (Q-T3-15)

- **Patch hors série** : `outils/ROTATION-Q-T3-15.patch` (sha256 775d5c2d…).
  - Il ajoute la précision de l.200 au §1, point 8, de `docs/adr-0029/s2bis/ROTATION-S2BIS.md`, dans sa version commise à f5915a5 (sha256 9db81092…), après la précision de Q-RB-5.
  - `git apply --check` passe. Ce fichier appartient à RECALC-BIS : je ne l'ai mis dans aucune série SIM.
- **Ligne pour le futur RB-7** : « `premiere` = premier hôte, par ordre des points de code des noms d'hôte de configuration, du pool BTC D1-bis de la strate restant après les retraits D1-bis (a), (b) et presque mort (ADR-0029 l.170) ; prise avant le critère collectif d'absorption et jamais recalculée après lui (absorbée d'une classe, elle y manque et toutes les unités de la classe sont décalées) ; pool vide : None (Q-T3-15, précision de l.200 adjugée le 2026-10-05, avant E0). »

## Items à former (PAROXYSME)

- **Restent sans code, comme le brief le prévoit** : O-3 (câblage de SB-11), O-5 (cellules de SB-11), P-3, P-5, P-6, P-9 (briefs de SB-11 et SB-13), Q-T3-1 (limite écrite, intacte).
- **L-1, neuf** : `calibration.unites` sert à la fois de format d'EP et de pool opérationnel.
  - Avec une liste réduite, EP est refusé (`CALIB/forme`, mesuré dans `journal/sonde-ep-pool-reduit.txt`).
  - O-1 ne joue donc que si le pool opérationnel est séparé de la liste d'EP. Le test et la sonde le font en mémoire.
  - Déclencheur : tout retrait du pool avant le sceau. À joindre à P-1 et à SHOGEN-S2BIS-LICENCES-API-1.
- **L-2** : la couche ne peut pas distinguer W de T_max exprimé en semaines (les deux sont entiers). Ligne à mettre au brief de SB-11 : passer le W de la cellule, celui de `calendrier.echelle`.
- **L-3** : patch ROTATION à appliquer par l'orchestrateur dans la série RECALC-BIS.
- **L-4** : les règles de noms de SIM-BIS et de RB-6 sont équivalentes aujourd'hui, mais aucun test ne lie les deux textes (Q-S-02 interdit d'importer RECALC-BIS). À traiter à SB-13 (SHOGEN-SIM-BIS-CONTRAT-RB6-1).
- **Interprétations déclarées** :
  - O-1 : j'ai lu « liste scellée de calibration » comme `sources.indices_hotes`.
  - O-4 : refus à la construction de la couche.
  - P-7 : code de refus `REGLE/libelle`.

## C-3 : octets 92, fichier par fichier (`journal/compte92.txt`)

- **Outils de la tranche 3 (`sim3/outils`, 33 fichiers)** : 29 octets.
  - appliquer_t2.sh 4, mutants_6b.py 10, mutants_6c.py 2, mutants_7b.py 4, mutants_8a.py 4, portes.sh 1, verifications.sh 1, verifications_c8c.sh 3.
  - Les 29 autres fichiers : 0.
  - Mon rapport précédent n'en comptait que 9 et omettait les 20 octets des quatre `mutants_*`.
- **`sim3/journal`, 80 fichiers** : 0.
- **Ce lot** : `corr/outils` 0 octet sur 32 fichiers ; `corr/journal` 0 sur 46 ; diffs 0 sur 4 ; notes 0 après nettoyage (voir E-1).

## Écarts déclarés

- **E-1, barres obliques inverses tapées.** L'état final de tous mes fichiers est contrôlé sur les octets : 0 octet 92.
  - (0) La première version de `base.sh` en portait 5 : trois continuations de ligne et les deux parenthèses échappées d'un `find`. Réécrite sans barre, elle redonne des arbres identiques : base 4bc92af6…, 751 fichiers ; série 86a3b242…, 755.
  - (1) Des retours à la ligne échappés dans des chaînes Python d'un heredoc, pour la docstring de `regle.py` : fichier contrôlé, ligne bien placée.
  - (2) Une séquence octale tapée dans le motif d'un `grep` : erreur de `grep`, sans effet.
  - (3) Des crochets échappés dans un `grep -v` d'affichage.
  - (4) La première version de `questions_t3.py` portait 4 guillemets échappés. Réécrite avec `chr(34)`, sa sortie est identique (`cmp`).
  - (5) Un `tr` sur l'octet nul pour lire `/proc/PID/cmdline` : remplacé par `outils/cmdline.py`.
  - (6) et (7) Des retours à la ligne échappés dans un heredoc et dans deux `printf` qui ajoutaient des lignes à mes notes. Effet vérifié ; 7 octets remplacés ensuite par « [barre] » dans les notes.
- **E-2** : le premier rouge de SB-8F donnait 1 ERROR. `pprint` d'un entier de plus de 4 300 chiffres. J'ai réécrit le test en segments et relâché la couverture de l'oracle : C = 0 n'est jamais observé. Le rouge a été remontré.
- **E-3** : j'ai ajouté un cas de refus à `test_valeurs_avis_t3` après son rouge, pour que M-8G-01 soit vu. Le rouge a été remontré.
- **E-4** : deux heures écrites dans mes notes sans lire l'horloge, corrigées. Aucune heure de ce rapport n'est estimée.
- **E-5** : parcours récursifs de mes copies, jamais du dépôt : un compte `find base -type f` et des empreintes agrégées (`empreinte_arbre.py`). Les dossiers interdits sont absents de ces copies. Rien n'est affiché hors des comptes et des empreintes.
- **E-6** : j'ai affiché les notes de la section S-G9 de xtask, au-delà des seules lignes de verdict. Elles ne contiennent que des chemins et des comptes, dont le nom d'un fichier de `docs/rapports`, sans son contenu.
- **E-7** : lectures au-delà de la liste du brief :
  - AVIS-RB-T1 l.12-14 et l.45-60 (Q-RB-5 à Q-RB-7), en plus de Q-RB-13 ;
  - la liste non récursive de `rb1/`, et ROTATION reconstruit depuis RB-6a et RB-6b ;
  - à f5915a5 : ROTATION §1 et §5, `rotation.py` l.17 et l.35-37, et les titres des commits limités à mes fichiers.
  - Motif : écrire la règle « dans ROTATION » et vérifier le « comme Q-RB-13 ».
- **E-8** : un `pgrep -n -x bash -s 0`, étroit, sans `-f`, dont le résultat n'a pas servi. Les PID réels viennent du journal des scripts et sont vérifiés par `/proc/PID/cmdline` : 18361 (campagnes), 24575 (identité), 28648 (portes). Un autre lot tournait (cb18, PID 20082) ; je n'y ai pas touché.
- **E-9** : machine chargée, charge jusqu'à 8,9. Les durées ne sont pas comparables ; la borne n'a jamais été approchée.
- **E-10** : la tête a avancé pendant le lot (12 commits RECALC-BIS). Parmi mes fichiers, seul `gates.yml` a changé, à sa ligne 218 (plancher s2bis 114 → 156). Ma base reste 3164348, comme le brief le demande. Je n'ai avancé aucune base ; c'est à l'orchestrateur d'adjuger.
- **E-11** : Q-T3-7 change l'interface des cellules. Les anciennes sondes T3 ne tournent plus telles quelles sur c8g ; elles ont des versions dérivées et déclarées.

## Journal G1

- **[lu]** :
  - mon brief (fa243d23…) ; la G2 transcrite (2b765c78…) ; l'AVIS-SIM-T3 (da343918…) ; mon rapport précédent (76603242…) ;
  - le G0 (d9cffc0a…) en entier ;
  - PROPOSITION (0e78afab…) l.152, 159-166, 173, 181, 186-189, 205, 290-293, 301, 535-545, 562-566 ;
  - ADR-0029 (b908842d…) l.170, 175, 200, 203 ;
  - AVIS-RB-T1 (2e542f5f…) l.12-14, 45-60, 86-97 ;
  - ROTATION d0078046…, reconstruit depuis RB-6a (15de17a0…) et RB-6b (89e4c806…), puis la version commise 9db81092… ;
  - outils et sorties du réviseur (rev/SHA256SUMS db37d015…, 82 sur 82 OK) ; mes outils de la tranche 3 (sim3/SHA256SUMS 77f3268d…, 319 sur 319 OK) ;
  - le code et les tests de la série ; `isole.sh` (ebaa1c78…) et `lo_up.py` (b532be4b…) ; `gates.yml`, job et ligne R-13.
- **[abs]** :
  - le brief des corrections de RB-T1 (non ouvert) ;
  - EP (lu par le code sous ses épingles seulement) ;
  - AVIS-SIM-T2 ; SB-11, SB-13 et RB-7, qui n'existent pas.
- **[2nd]** : la forme RFC 1123 des noms d'hôte (via Q-RB-13) ; la stabilité de `random()` entre versions de Python, recoupée ici par les sondes 16 fois sur 16.
- **[calc]** :
  - 4 320/4 505 ≈ 96 % (Q-T3-2) ;
  - décalages de r = 1 en calme modulo 8, par `sha256sum` et `bc` : binance 1, coinbase 1, kraken 4 ;
  - toutes les valeurs écrites à la main dans les docstrings des tests.
- **Exposition** : aucune pièce de D.2, aucun `*.jsonl`, aucun dossier exclu ouvert. `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée (`env -u` partout). Bibliothèque standard seule (R-8 sans objet).
- **Commandes et sorties**, toutes dans `corr/journal/` :
  - `base.txt`, `base-verif.txt` ;
  - `rouge-SB-8*.txt`, `vert-SB-8*.txt`, `c2-rouge-sous-mutant.txt`, `job-c8*.txt`, `tailles-SB-8*.txt`, `verifications.txt` ;
  - `campagnes.log`, `mutants-{reviseur,neufs,tranche}-c8g.txt` ;
  - `identite.txt`, `identite-o1.txt`, `sonde-o1-{avant,apres}.txt`, `sonde-ep-pool-reduit.txt` ;
  - `portes.txt`, `xtask-verdicts-{travail,base}.txt`, `sur-tete-f5915a5.txt`, `compte92.txt`.
- Tous les chiffres de ce rapport sont recomptés sur ces fichiers.

## Fichiers

Dossier de travail : `<scratchpad>/s2bis/sim3/corr/`

| pièce | chemin | sha256 |
|---|---|---|
| diffs, à appliquer après SB-8C | `diffs/SB-8D.diff` | 7e69e808… |
| | `diffs/SB-8E.diff` | 32564d9a… |
| | `diffs/SB-8F.diff` | 9777c0f8… |
| | `diffs/SB-8G.diff` | 027f5d12… |
| patch hors série | `outils/ROTATION-Q-T3-15.patch` | 775d5c2d… |
| sommes (189 entrées, `sha256sum -c` OK) | `SHA256SUMS` | 48edd0ed0d199290697814abef0265b0b0d0285fb8ea7d5ee7fce991ec24a73b |

- **Autres pièces** :
  - `etapes/c8c` à `c8g` (arbres légers) ;
  - `outils/` (32 fichiers, dont `base.sh` pour recréer la base, `mutants_corr.py`, `mutants_rejeu.py`, les sondes dérivées) ;
  - `journal/` ; `notes/NOTES.md`.
- **Nettoyage** : base, série, travail, TMPDIR et cible cargo sont supprimés ; 8,9 Go libres.
