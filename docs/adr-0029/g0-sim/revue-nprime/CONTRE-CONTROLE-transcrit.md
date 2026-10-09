# Contre-contrôle de SB-11y et SB-11z (CONFORME en passe 3) (transcrit)

> Transcription par l'orchestrateur le 2026-10-09 18:27:52 UTC du fichier g2/cc/RAPPORT-CC.md ; contrôle FM-1.1 des transcripts de l'advisor (claude-fable-5-1), du générateur-correcteur, du réviseur et du contre-contrôleur (claude-opus-5-5), par le fm11.py versé et par celui de DETTES-T3 : fragments_l51_l14 = 0. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Contre-contrôle de NPRIME-NUL-1 (G2 de vérification des corrections de SB-11y et SB-11z), 2026-10-09, rédigé à partir de 15:24:30 UTC

## 0. Gate 0 et rôle
- Modèle résolu : `claude-opus-5-5`. Le préfixe est conforme.
- Rôle : contre-contrôleur neuf. Je n'ai écrit ni l'AVIS, ni l'ADJUDICATION, ni SB-11x, y ou z, ni la G2.
- Base : tête 798176f à l'entrée (14:53:58 UTC). Après le redémarrage du conteneur, la tête est 60fad53 (DETTES-T1 BM-1), comme l'a fixé l'orchestrateur. Toutes les gates et les mutants ci-dessous ont tourné sur la copie z = `git archive 60fad53` (exclusions du brief) + SB-11x + SB-11y + SB-11z.

## 1. Verdict
**CONFORME-AVEC-RÉSERVES**, avec la liste fermée R-1 à R-5 (§5).
- C-1, C-2, C-5 et C-6 répondent en entier à leur constat.
- C-4 répond à son constat. Une phrase du G0 n'est tenue qu'à moitié par les tests (R-2).
- C-3 et C-7 ont des tests qui ne portent pas toute la force voulue :
  - M-CC-01 reste vivant (R-4) ;
  - M-CC-03 et M-CC-04 ne tombent que par une ERROR (KeyError), jamais par une AssertionError (R-5).
- SB-11z est juste sur le G0 et sur les deux épingles qu'il touche, mais il oublie une troisième épingle (R-1).
- Toutes les gates sont vertes, sauf xtask. xtask est rouge à l'identique sur la base et sur z : le lot n'y est pour rien (E-2).

## 2. Corrections vérifiées
| id | constat de la G2 | vérification | jugement |
|---|---|---|---|
| C-1 | O-1, S et absorption confondus (G2-M04, M05, M06) | `test_etiquettes_croisees_et_octets` : (S, sans critère, [8]) puis (sans S, critère, [4]). Les 3 mutants sont tués par AssertionError (mut/campagne.txt). | en entier |
| C-2 | O-1, R de la cellule confondu avec R_approche (G2-M08) | Même test, R ∈ {99, 199} sous P (R 199, R_approche 99). C et r sont égaux à R ; C_S est comparé en octets à la référence. G2-M08 est tué par AssertionError. | en entier |
| C-3 | O-1, source de « vide » (G2-M01, M03) ; « une strate à n′ partiel perdrait sa statistique sans qu'un test le voie » | G2-M01 est tué par test_n_prime_partiel, G2-M03 par test_premiere_absente. Mais **M-CC-01 est VIVANT** : il appelle la règle à n′ = 650 puis remplace son résultat par l'enregistrement dégénéré. Le test n'exige que « n_prime ∈ causes » et l'appel de l'oracle. | incomplet → R-4 |
| C-4 | O-1, égalité Python et non en octets (G2-M12, M13) | Les deux sont tués par AssertionError. M-CC-02 (N de la variante en Fraction) est tué aussi. Le G0 (2) dit « en octets … à plusieurs n_s ». Or l'octet n'est comparé qu'à n_s = 2 736 ; la comparaison entre n_s = 3 et n_s = 2 736 reste en égalité Python (test_equivalence_regle). | conforme au constat ; R-2 sur le texte du G0 |
| C-5 | plancher exact | Ran 277 = plancher 277 (`--egal`), sur z et sur les 4 interpréteurs | en entier |
| C-6 | O-2, phrase inexacte du rapport du générateur | La phrase est absente (grep : 0) ; une marque datée est en place (l.49). | en entier |
| C-7 | O-6 / I-2 / I-3, comptes n′ = 0 et oracle | « n_prime_nul » et « oracle » sont posés par strate, et « oracle » est sommé par cellule. Le prédicat « i < ORACLE et n′ > 0 » est égal à la condition d'appel de `regle.oracle` dans `replication`. M-CC-05 (oracle compté par classe) est tué par AssertionError. Mais **M-CC-03 et M-CC-04** (comptes pris sur `premiere` au lieu de `n`) ne tombent que par une ERROR (KeyError de test_agreger) : test_compte_n_prime_et_oracle reste vert sous ces deux mutants. | incomplet → R-5 |

Lecture de « par cellule et par strate » (G0 (4)) : l'agrégat est écrit cellule par cellule, et « n_prime_nul » y est donné par strate. Je retiens cette lecture. Une somme par cellule n'aurait pas de sens net, puisqu'une même réplication peut avoir deux strates vides. Ce point n'est pas une réserve.

## 3. Mutants
Commande exacte du job, sur z : `python3 -B enforcement/verdict-suite-s2.py scripts/sim-bis --aucun-saut --egal --plancher 277`.
- Exécution : `iso.sh` (`env -u` des mandataires et `isole.sh`) ; borne de 300 s ; `start_new_session` et `killpg` ; PAR = 2.
- Classement : sortie 1 = tué, 0 = vivant, toute autre sortie = FATAL.
- Campagne : 14:59:26 → 15:23:55, PID 8555 (mut/campagne.txt).
- `ps` de fin : aucun processus de g2/cc ne reste (journal/ps-fin.txt).

| id | mutation | résultat | rouge |
|---|---|---|---|
| TEMOIN-debut / TEMOIN-fin | aucune | VIVANT, Ran 277 (138 s / 135 s) | — |
| G2-M01 | vide = `not suffisant` | TUÉ | AssertionError, test_n_prime_partiel |
| G2-M03 | vide = `prem is None` | TUÉ | AssertionError, test_premiere_absente |
| G2-M04, M05, M06, M08, M12, M13 | voir la G2 | TUÉS | AssertionError, test_etiquettes_croisees_et_octets |
| M-CC-01 (C-3) | `vide or ((t := _tester(…)) and not suffisant)`, sinon t : la règle est appelée, son résultat jeté à n′ < n_s/2 | **VIVANT** (sortie 0) | — |
| M-CC-02 (C-4) | N de la variante = `Fraction(demi(0, d))` | TUÉ | AssertionError, test_etiquettes_croisees_et_octets |
| M-CC-03 (C-7) | n_prime_nul compté sur `premiere is None` | TUÉ **par ERROR seule** | KeyError dans test_agreger ; 0 AssertionError |
| M-CC-04 (C-7) | oracle compté sur `premiere is not None` | TUÉ **par ERROR seule** | KeyError dans test_agreger ; 0 AssertionError |
| M-CC-05 (C-7) | oracle compté par classe | TUÉ | AssertionError, test_agreger |

Bilan :
- 13 mutants ont tourné : 12 tués, 1 vivant, 0 FATAL, 0 borne ; durées de 135 à 201 s.
- Sonde (journal/sonde.txt) : à i = 65, la strate de stress a n′ = 650, premiere = binance, et BTC donne [runs, n_prime], K = 1, unites = 6. Cet enregistrement diffère du dégénéré : M-CC-01 n'est donc pas un mutant équivalent.
- La cellule de test a une seule classe. À n′ = 0, premiere vaut toujours None, et c'est pourquoi M-CC-03 et M-CC-04 échappent à l'assertion.
- Propositions démontrées (propositions/test_nprime_cc.py, journal/propositions.txt) :
  - sur z : Ran 2, OK ;
  - sous M-CC-01, M-CC-03 et M-CC-04 : rouge, par AssertionError seule.

## 4. SB-11z et gates
**Application.** Les trois diffs s'appliquent dans l'ordre x, y, z, sur 798176f comme sur 60fad53 :
- `patch -p1 -F0` : code 0, aucun décalage ni fuzz ;
- `git apply --whitespace=error-all` : code 0 ;
- les deux arbres obtenus sont identiques (journal/application.txt).

**G0.** `G0-SIM-BIS.md` de z est égal, octet pour octet, au G0 de 60fad53 suivi de G0-AJOUT.md (cmp ; 11 912 + 2 446 = 14 358 octets) :
- sha256 recalculé : c6c8e692645a59b0d9c67452157c0b46303cb8b9646738d8c232684e545a6210 ;
- l'ancien, a216a953…, est le blob de la tête (journal/g0.txt).

**Épingles** (journal/preuves-z.txt) :
- la tête du rattachement vaut l'empreinte recalculée ;
- témoin : test_commun Ran 22 OK ;
- ancienne épingle remise : FAILED (failures=2 : test_g0_mesure, test_provenance_c_5) ;
- G0 augmenté d'un octet : FAILED (failures=1 : test_g0_mesure) ;
- chaque fois par AssertionError seule.

Aucune autre épingle de a216a953 ni des sha256 de parametres.json et test_commun.py, dans scripts, s2bis, enforcement, .github, s2-harness, xtask et crates. Dans docs/adr-0029/g0-sim/, lu sans récursion, **SHA256SUMS l.4 épingle encore a216a953…** et `sha256sum -c` y donne FAILED → R-1.

**Gates** (journal/gates.txt ; PID 7811 ; 14:58:08 → 15:17:34 ; commandes et planchers lus dans gates.yml de z) :
| gate | résultat |
|---|---|
| runner | 136 ok, 0 échec |
| sim-bis | conforme, Ran = 277 (`--egal`, plancher 277), 148 s |
| s2bis | conforme, Ran = 341 (plancher de 60fad53) |
| S2 | conforme, Ran = 415, 2 sauts nommant SHOGEN_S2_CAMPAGNE_CONTROL |
| calib-actifs | conforme, Ran = 65 |
| matrice 3.10 / 3.11 / 3.12 / 3.13 `-X dev -W error` | code 0, Ran 277, OK ; 0 « Exception ignored », 0 « Warning » |
| xtask (lignes VERDICT seules) | z et base : code 1 ; 10 lignes VERDICT **identiques** ; le 9e contrôle est ROUGE (1 violation), le global est ROUGE (E-2) |

L'écart E-10 du générateur est levé pour les suites : elles sont rejouées sur la tête 60fad53 + x + y + z, et toutes sont vertes. Pour xtask, le lot est neutre (base et z identiques).

**Forme** (journal/forme.txt) :
- R-25 : x +176 / −8, y +85 / −26, z +15 / −4, toutes sous 200 ;
- 0 TODO ou FIXME ;
- 0 octet 92 dans les trois diffs et dans les fichiers touchés, hormis les 4 de gates.yml, préexistants et en nombre égal dans la base ;
- Python : 119 caractères au plus.

**Écarts du générateur** :
- E-8 est admissible : le test n'est pas affaibli, l'assertion sur les clés est renforcée et le champ « n » est ajouté aux fixtures.
- E-9 est admissible : les écritures git ont eu lieu dans les copies seulement.
- E-11 est admissible : l'AssertionError visée est bien présente.

## 5. Réserves (liste fermée ; chacune corrigible dans le lot, aucune n'est un item)
- **R-1 (SB-11z, épingle oubliée).** Ajouter au diff SB-11z la ligne 4 de `docs/adr-0029/g0-sim/SHA256SUMS`, où `a216a953…  G0-SIM-BIS.md` devient `c6c8e692645a59b0d9c67452157c0b46303cb8b9646738d8c232684e545a6210  G0-SIM-BIS.md`.
  - Précédent : 12ce67f a changé cette ligne avec le G0.
  - Preuve à joindre : `sha256sum -c` du dossier, 5/5 OK.
- **R-2 (C-4 / G0 (2), « en octets … à plusieurs n_s »).** Dans `test_equivalence_regle`, remplacer `assertEqual(reference(rg, 3), reference(rg, 2736))` par la même égalité sur `octets(…)`, idéalement pour n_s ∈ {3, 4, 7}.
  - Mesuré sur z : vrai pour les deux cellules (journal/r2-octets-ns.txt).
- **R-3 (texte, règle « aucune dette » ; O-4).** O-4 n'est pas un défaut : aucune règle ni gate ne borne une rangée Markdown, et le format était déjà là (8 rangées de plus de 120 caractères avant le lot). Il ne faut donc ni item ni réserve sur le tableau.
  - Retirer de RAPPORT-GENERATEUR §10 (l.267) la phrase « une refonte du tableau peut être formée en item, sans blocage ». C'est un item flottant, sans lot nommé.
  - La remplacer par « O-4 : aucun défaut (format préexistant, aucune règle enfreinte) ; ni item ni réserve ».
- **R-4 (C-3 incomplet, M-CC-01 vivant).** Ajouter `test_n_prime_partiel_resultat` (texte dans propositions/test_nprime_cc.py) :
  - un espion `side_effect` sur `executer._tester`, à i = 65 ;
  - assertion : l'enregistrement BTC de stress est celui que `_tester` a rendu, et « unites » n'est pas dans ses causes.
- **R-5 (C-7, source des comptes ; M-CC-03 et M-CC-04 tués par ERROR seule).** Ajouter `test_compte_premiere_absente` (même fichier) :
  - `regle.premiere` est rendue None, aux réplications i = 0 et 1 ;
  - attendus : n′ nul [calme 0, stress 1], oracle [2, 1], cellule 3.
- Conséquences de R-4 et R-5 :
  - le plancher sim-bis passe à 279 (`--egal`) ;
  - ajout d'environ 45 lignes, dans SB-11y ou dans un diff neuf SB-11y2, au choix de l'orchestrateur ; l'un comme l'autre reste sous 200 ;
  - preuves : M-CC-01, -03 et -04 tués par AssertionError sous la commande du job.

## 6. Écarts du contre-contrôleur
- **E-1.** `git init`, alternates vers les objets du dépôt réel, et un commit local, dans mes copies base et z seulement (oracle_r1 et oracle_recalc lisent par `git archive`). Le dépôt réel n'a reçu aucune écriture ; mes commandes git sur lui portaient `--no-optional-locks`.
- **E-2.** xtask est ROUGE (9e contrôle) à l'identique sur base et sur z.
  - Cause probable : les exclusions du brief sur ma copie. Elle n'est pas vérifiable, puisque seules les lignes VERDICT ont été lues.
  - Le générateur, sur une archive complète de 2229e15, obtenait 10 VERT.
  - Le jugement « lot neutre » tient à l'identité base/z. Le vert absolu reste à constater par la CI au commit.
- **E-3.** Un horodatage de NOTES (« 14:57-15:05 ») avait été écrit sans lecture d'horloge. Il est corrigé dans NOTES : l'heure a été lue, l'application a eu lieu entre 14:55:01 et 14:57:20.
- **E-4.** Redémarrage du conteneur. Les copies ont été refaites sur 60fad53 et rien n'a été compté d'avant la reprise. La reprise a été constatée à 14:57:20 UTC ; le `ps` ne montrait aucun reste.
- **E-5.** La machine était partagée avec un autre agent (dettes2, visible au `ps`). Les durées sont restées sous la borne.

## 7. Journal de provenance (G1)
- **Lu [lu].** AVIS.md (2024f275…), ADJUDICATION.md (399bf4f3…, ajout daté compris), G0-AJOUT.md (2341498a…), g2/RAPPORT-G2.md (8eb3ea8d…), RAPPORT-GENERATEUR.md dont §10, SB-11x/y/z.diff (c86a4d9b…, 185db61b…, dbc91603…), g2/outils (mutants_g2.py, epingles_g0.py), outils du générateur (mutants_y.py, campagne_y.py, gates_y.sh, preuves_z.py, chaine_y.sh), mut-y/campagne.txt, journal/gates-y.txt, application-f2.txt, preuves-z.txt, g2/propositions/test_nprime_g2.py ; dans z : executer.py (_tester, _vide, replication, agreger), test_nprime.py, test_commun.py l.56-84, gates.yml (lignes des jobs), docs/adr-0029/g0-sim/SHA256SUMS.
- **Contrôles d'intégrité.** SHA256SUMS du générateur : 102/102 OK. g2/SHA256SUMS : 57/57 OK.
- **Commandes et sorties.** Voir NOTES.md, horodaté, et journal/ (application, g0, forme, sonde, preuves-z, propositions, r2-octets-ns, gates et g-*.txt, xtask-z et xtask-base, ps-fin) ; mut/ (campagne.txt et une sortie par run).
- **Chiffres recomptés par moi.** Ran 277, 341, 415, 65 et 22 ; 136 ok ; numstat ; octets 92 ; longueurs de lignes ; sha256 du G0 ; tailles en octets ; n′ par i ; classement des 13 mutants.
- **Interdits respectés.** Aucune pièce D.2 ni lecture interdite ouverte (exclusions dans l'archive) ; aucune recherche récursive sur docs/ ; SHOGEN_S2_CAMPAGNE_CONTROL jamais posée ; aucun réseau ; aucun commit, push ou fetch sur le dépôt réel.

## Passe 2 — section datée du 2026-10-09, écrite à partir de 16:47:01 UTC (`date -u`)
Gate 0 : modèle résolu `claude-opus-5-5`.
- Entrées :
  - ajout daté du 15:26:10 UTC dans ADJUDICATION.md ;
  - §11 de RAPPORT-GENERATEUR.md ;
  - SB-11x (c86a4d9b…, inchangé), SB-11y (f24a64a7…), SB-11z (0888a978…).
- Base : tête 0cfbe3e. Copie = `git archive 0cfbe3e` avec les exclusions du brief, puis x, y et z.
- Application : `patch -p1 -F0` et `git apply --whitespace=error-all` sortent en code 0 ; les deux arbres sont identiques (journal/application-p2.txt).

### Verdict de la passe 2
**CONFORME-AVEC-RÉSERVES, liste fermée réduite à R-6.**
- R-1, R-2, R-3 et R-5 sont levées en entier.
- R-4 est levée pour M-CC-01. Un mutant neuf, M-CC-06, reste vivant.
  - Cause : l'espion de C-11 garde une référence au dict rendu par `_tester`, et non une copie. Une modification de ce dict sur place, après l'appel, passe donc inaperçue.
  - Cette faiblesse vient de la forme que j'avais moi-même proposée pour R-4 (propositions/test_nprime_cc.py). Le générateur l'a reprise fidèlement.

### Réserves R-1 à R-5
| réserve | correction | vérification | jugement |
|---|---|---|---|
| R-1 | C-8 : l.4 de `docs/adr-0029/g0-sim/SHA256SUMS` → c6c8e692…6210 | `sha256sum -c` du dossier : 5/5 OK sur z (journal/c8-p2.txt). Le diff ne touche que cette ligne. | levée |
| R-2 | C-9 : `octets(y[cl]) == octets(reference(rg, n_s))` pour n_s ∈ {3, 4, 7, 2 736} | M-CC-02 et M-CC-07 (S écrit False) font rougir **test_equivalence_regle** en plus de test_etiquettes (AssertionError). | levée |
| R-3 | C-10 : phrase retirée du rapport ; marque datée l.267 « O-4 : aucun défaut … ; ni item ni réserve » | grep « peut être formée en item » : 0 | levée |
| R-4 | C-11 : test_n_prime_partiel_resultat | M-CC-01 tué par AssertionError. M-CC-06 vivant (ci-dessous). | levée pour M-CC-01 ; reste R-6 |
| R-5 | C-12 : test_compte_premiere_absente | M-CC-03, M-CC-04, M-CC-08 et M-CC-09 tués par AssertionError (test_compte_premiere_absente). Une ERROR KeyError s'ajoute dans test_agreger, sans effet sur le classement. | levée |

### Mutants de la passe 2
Commande du job, `--plancher 279`, sur z :
- exécution : iso.sh, borne 300 s, `start_new_session` et `killpg`, PAR = 2 ;
- campagne : 16:27:02 → 16:45:55, PID 31482 (mut-p2/campagne.txt).

| id | mutation | résultat |
|---|---|---|
| TEMOIN début / fin | aucune | VIVANT, Ran 279 (155 s / 146 s) |
| M-CC-01 | règle appelée, résultat remplacé par le dégénéré à n′ < n_s/2 | TUÉ, AssertionError (test_n_prime_partiel_resultat) |
| M-CC-02 | N de la variante en Fraction | TUÉ, AssertionError ×2 (test_equivalence_regle, test_etiquettes_croisees_et_octets) |
| M-CC-03 | n′ nul compté sur `premiere is None` | TUÉ, AssertionError (test_compte_premiere_absente) |
| M-CC-04 | oracle compté sur `premiere is not None` | TUÉ, AssertionError (test_compte_premiere_absente) |
| M-CC-05 | oracle compté par classe | TUÉ, AssertionError (test_agreger) |
| M-CC-06 (neuf, C-11) | à n′ < n_s/2, K et unites du dict rendu par `_tester` remis à 0 sur place | **VIVANT** |
| M-CC-07 (neuf, C-9) | S écrit False au lieu de l'entier 0 | TUÉ, AssertionError ×2 (test_equivalence_regle, test_etiquettes_croisees_et_octets) |
| M-CC-08 (neuf, C-12) | n′ nul compté aussi quand la première unité manque | TUÉ, AssertionError (test_compte_premiere_absente) |
| M-CC-09 (neuf, C-12) | oracle compté seulement si la première unité existe | TUÉ, AssertionError (test_compte_premiere_absente) |

Bilan :
- 9 mutants : 8 tués par AssertionError, 1 vivant ; 0 FATAL, 0 borne ; durées de 146 à 185 s.
- `ps` de fin : aucun processus de nprime/g2/cc (journal/ps-fin-p2.txt). Les processus restants appartiennent à un autre agent (dettes3).

### R-6 (réserve unique de la passe 2 ; corrigible dans SB-11y)
**Forme.** Dans test_n_prime_partiel_resultat, l'espion fige les octets au moment de l'appel :
- `r = vrai(p, rg, i, a)`, puis `vus.append((a[3], octets(r)))`, puis `return r` ;
- l'assertion devient `[x for s, x in vus if s == "stress"] == [octets(r["classes"]["BTC"])]`.

La fixture a evenements = 0 : aucune clé n'est ajoutée sur place par le code normal.

**Démonstration** (outils/r6.py, journal/r6.txt), sur une copie de tests/test_nprime.py :
- z : Ran 11, OK ;
- M-CC-01 et M-CC-06 : rouges par AssertionError seule.

**Effets.** Le plancher reste 279 et le diff change de 3 lignes environ. Preuve à joindre : M-CC-06 tué sous la commande du job.

### Gates (journal/gates-p2.txt ; PID 30379 ; 16:26:09 → 16:44:53)
| gate | résultat |
|---|---|
| runner | 136 ok, 0 échec |
| sim-bis | conforme, Ran = 279 (`--egal`, plancher 279 exact) |
| s2bis | conforme, Ran = 341 |
| S2 | conforme, Ran = 415, 2 sauts nommant SHOGEN_S2_CAMPAGNE_CONTROL |
| calib-actifs | conforme, Ran = 65 |
| matrice 3.10 / 3.11 / 3.12 / 3.13 `-X dev -W error` | code 0, Ran 279, OK ; 0 « Exception ignored », 0 « Warning » |
| xtask (lignes VERDICT seules) | z et base : 10 lignes identiques, et identiques à la passe 1. Le 9e contrôle est ROUGE sur la copie à exclusions (E-2) ; le lot est neutre. |

### SB-11z, forme et fichiers
- G0 de z = G0 de 0cfbe3e + G0-AJOUT (cmp) ; sha256 c6c8e692….
- Preuves d'épingle refaites (journal/preuves-z-p2.txt) :
  - témoin : 22 OK ;
  - ancienne épingle : FAILED (2) ;
  - G0 + 1 octet : FAILED (1) ;
  - par AssertionError seule.
- Fichiers identiques à la passe 1 : executer.py, test_executer.py, parametres.json et test_commun.py.
- Forme R-25 (journal/forme-p2.txt) :
  - x +176 / −8, y +116 / −28, z +16 / −5, toutes sous 200 ;
  - 0 TODO ou FIXME, 0 octet 92 ;
  - Python : 120 caractères au plus.
- E-13 (README non retouché pour C-9, C-11 et C-12) est admissible : la rangée de SB-11y nomme déjà « n′ partiel et première unité absente ».

### E-12 : aucune gate ne vérifie les SHA256SUMS des dossiers de docs
Lecture ciblée, sans aucune recherche sur docs/ :
- `grep -rn SHA256SUMS` sur xtask, enforcement et .github, dans la copie z (journal/e12-grep.txt). Une seule occurrence : xtask/src/sg9.rs l.489, la liste de noms de la D.2, qui n'est pas une vérification.
- `grep sha256sum | --check | Sha256` sur les mêmes dossiers : seulement le hook (install-pre-commit.sh), ses fixtures, temoignage.yml (empreinte d'une sortie) et reproductible.rs (binaires).
- xtask/src/documents.rs et sg5.rs : aucune somme de contrôle de docs.

Conclusion : aucune gate ne vérifie les SHA256SUMS de docs/. Ce n'est pas une réserve de ce lot. C'est un **lot nommé** à former par l'orchestrateur ; nom proposé : SHOGEN-DOCS-SHA256SUMS-GATE-1, une gate `sha256sum -c` des SHA256SUMS versés sous docs/. C-8 est prouvé par `sha256sum -c` avant et après, ce qui suffit.

### Écarts de la passe 2
- **E-6.** Copies base et z refaites sur 0cfbe3e, avec `git init`, alternates et un commit local, dans mes copies seulement. Le dépôt réel n'a reçu aucune écriture.
- **E-7.** Le commentaire de tête de outils/gates_p2.sh dit « base = 60fad53 », alors que la base est 0cfbe3e (texte hérité de la passe 1). Je ne l'ai pas retouché pendant l'exécution. Les commandes, elles, portaient sur travail/base = 0cfbe3e (journal/application-p2.txt).
- **E-8.** Machine partagée avec d'autres agents (dettes3) ; les durées sont restées sous la borne.

### Provenance de la passe 2
- **Lu [lu].** Ajout daté d'ADJUDICATION.md (15:26:10) ; §11 et l.265-270 de RAPPORT-GENERATEUR.md ; test_nprime.py de z (tests C-9, C-11, C-12) ; docs/adr-0029/g0-sim/SHA256SUMS ; xtask/src/sg9.rs l.480-495 ; xtask/src/documents.rs (tête) ; lignes grep citées.
- **Recomptés.** Ran 279, 341, 415, 65 et 22 ; 136 ok ; numstat ; octets 92 ; longueurs de lignes ; sha256 ; classement des 9 mutants.
- **Interdits respectés.** Aucune pièce D.2 ouverte ; aucune recherche sur docs/ ; SHOGEN_S2_CAMPAGNE_CONTROL jamais posée ; réseau coupé ; aucune écriture dans le dépôt réel.

## Passe 3 — section datée du 2026-10-09, écrite à partir de 18:01:41 UTC (`date -u`)
Gate 0 : modèle résolu `claude-opus-5-5`.
- Entrées : §12 de RAPPORT-GENERATEUR.md ; SB-11y (d9f73299…). SB-11x (c86a4d9b…) et SB-11z (0888a978…) sont inchangés.

### Verdict de la passe 3
**CONFORME.** R-6 est levée en entier. Aucune réserve ne reste.

### Vérifications
**Diff C-13.** Entre f24a64a7… et d9f73299…, SB-11y ne change que dans `test_n_prime_partiel_resultat` :
- l'espion fige `octets(r)` au moment de l'appel ;
- l'assertion compare `octets(r["classes"]["BTC"])` à ces octets ;
- la docstring nomme C-13 et M-CC-06.

C'est la forme proposée pour R-6 (journal/forme-p3.txt).

**Application** (journal/application-p3.txt) :
- sur 0cfbe3e : x, y et z passent par `patch -p1 -F0`, en code 0, sans décalage ;
- sur la tête relue à 17:53:29, 0781a68 : code 0, mais le hunk de gates.yml de x et de y s'applique avec un décalage de 6 lignes, sans fuzz. DETTES-T3 a en effet ajouté un job plus haut dans le fichier ;
- scripts/sim-bis est identique sur les deux têtes, et le plancher sim-bis reste 279 après z.

**Campagne** (mut-p3/campagne.txt ; 17:54:07 → 18:01:31 ; PID 10442) :
- copie z = 0cfbe3e + x + y + z ; commande du job `--plancher 279` ;
- iso.sh, borne 300 s, `start_new_session` et `killpg`, PAR = 2 ;
- `ps` de fin : aucun processus de nprime/g2/cc (journal/ps-fin-p3.txt).

| id | mutation | résultat |
|---|---|---|
| TEMOIN | aucune | VIVANT, Ran 279 (`--egal`, plancher exact), 153 s |
| M-CC-01 | règle appelée, résultat remplacé par le dégénéré | TUÉ, AssertionError (test_n_prime_partiel_resultat) |
| M-CC-06 | K et unites remis à 0 sur place après l'appel | TUÉ, AssertionError (test_n_prime_partiel_resultat) |
| M-CC-10 (neuf, espion) | liste des causes renversée sur place après l'appel (objet imbriqué) | TUÉ, AssertionError (test_n_prime_partiel_resultat), plus une ERROR dans test_compte_n_prime_et_oracle levée par `frequences` sur l'ordre des causes |
| M-CC-11 (neuf, espion) | à n′ < n_s/2, la règle reçoit n_s = n′ ; un seul appel, l'espion voit donc la même sortie | TUÉ, AssertionError (test_n_prime_partiel : cause n_prime absente) |

Bilan : 4 mutants sur 4 tués, chacun avec AssertionError ; 0 FATAL, 0 borne.

**Forme R-25.**
- x +176 / −8, y +119 / −28, z +16 / −5, toutes sous 200 ;
- 0 TODO ou FIXME, 0 octet 92 ;
- test_nprime.py et executer.py : 120 caractères au plus.

**Ce que je n'ai pas rejoué.** Les autres gates (runner, s2bis, S2, calib-actifs, matrice) ne sont pas rejouées dans cette passe courte. Elles ne lisent pas le fichier changé, à l'exception de la suite sim-bis, couverte par le témoin ci-dessus. Le générateur les donne vertes sur 0cfbe3e (§12).

### Écarts de la passe 3
- **E-9.** Copie z refaite, avec `git init`, alternates et un commit local, dans ma copie seulement. Le dépôt réel n'a reçu aucune écriture.
- **E-10.** Le §12 du générateur annonce « code 0 » sur 0781a68 sans mentionner le décalage de 6 lignes du hunk de gates.yml. Le décalage est sans effet sur le contenu, mais il faut le savoir au versement sur la tête qui avance.
