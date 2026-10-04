# Rapport du worker : partie P1, brief A (sous-lots CB-0, CB-1, CB-2 de COLLECTE-BIS)

**Gate 0** : modèle résolu `claude-opus-5-5` (identifiant exact), effort max, fiche `shogen-worker`.
**Horloge** (`date -u`) : début 2026-10-04 17:08:10 UTC, fin 18:20:40 UTC.
**Brief** : `BRIEF-P1-A.md`. sha256 recalculé : `842b70acea5d9496e0f24a15dbfa74d509c14c983da904523983d02d8f098eaa`, égal à l'annoncé.
**Base** :
- Branche `claude/compassionate-noether-szmdyj`. Tête au début : `665898a2238d`. Tête à la fin : `34a17d8d44d0`.
- Entre les deux, deux commits de l'orchestrateur (`786a865`, `34a17d8`, brouillons publics du rapport S2). Ni l'un ni l'autre ne touche `.github/`, `enforcement/`, `s2bis/`, `s2-harness/` ou `docs/adr-0029/s2bis/` (contrôlé par `git diff --stat`).
- Copie de travail faite par `git archive` avec les exclusions du brief.
- Dépôt jamais écrit : `git status` est vide à la fin.

## 1. Résumé

- **Livré : 7 diffs consécutifs**, chacun ≤ 200 lignes de code ajoutées : CB-0a, CB-0b, CB-1a, CB-1b, CB-2a, CB-2b, CB-2c.
  - Ils s'appliquent en série sur `34a17d8`, contrôlé sur une extraction neuve.
  - L'arbre obtenu est identique, fichier par fichier, à mon arbre final.
- **Paquet neuf `s2bis/`**, bibliothèque standard seule :
  - `shogen_s2bis/collecte/config.py` : configurations scellées, refus nommés.
  - `shogen_s2bis/collecte/journal.py` : écrivain chaîné. Il couvre la ligne canonique, `seq` et `prec`, le fsync au marqueur, le point de contrôle horaire, le verrou exclusif, les fichiers quotidiens et les sommes, la reprise, les queues, les segments et les trous.
  - 34 tests, une garde réseau et les fonctions de fitness.
- **CI** :
  - job `s2bis-unittest` (image épinglée, plancher 34) ;
  - vérificateur S2 paramétré par `--aucun-saut` et `--plancher N`, sans changement du comportement par défaut ;
  - cas K-01 et K-02 du runner, qui lisent les étapes des deux jobs unittest dans `gates.yml`.
- **Documents** (hors compte) : pièce G6, baseline de métriques, spécification du format des journaux.
- **Tests d'abord** : rouge puis vert pour chaque diff (§4).
- **Mutants** : 102 nommés, 102 tués par leur test nommé, 0 vivant, 0 FATAL au passage final. Les passages intermédiaires sont consignés au §5.
- **Écart principal** : les tailles du G0 sont dépassées. Mesuré : CB-0 = 357 lignes de code, CB-1 = 241, CB-2 = 400. Le G0 estimait ≈ 190, 180 et 190. C'est environ 1,8 fois l'estimation [calc] ; d'où le découpage en 7 diffs. À adjuger.

## 2. Diffs, dans l'ordre d'application

Tous les fichiers sont sous `<scratchpad>/s2bis/p1/`.

| diff | objet | code ajouté | doc ajouté | retirées | plancher du job |
|---|---|---|---|---|---|
| CB-0a | paquet, `config.py`, garde réseau, pièce G6 | 197 | 33 | 0 | (pas de job) |
| CB-0b | fitness ; vérificateur paramétré ; runner (V-14, V-15, C-03 à C-05, K-01, K-02) ; job `s2bis-unittest` ; baseline | 160 | 40 | 15 | 10 |
| CB-1a | chaîne canonique, `seq`/`prec`, fsync au marqueur, point horaire, règles de fenêtre ; format §1 à §4 | 199 | 60 | 1 | 14 |
| CB-1b | verrou exclusif ; format §5 | 42 | 17 | 9 | 15 |
| CB-2a | fichiers quotidiens, clôture, sommes ; format §6 | 64 | 24 | 9 | 16 |
| CB-2b | reprise, queues, segments, borne de ligne, fenêtre du redémarrage ; format §7 | 200 | 36 | 14 | 25 |
| CB-2c | trous et causes, sommes rattrapées, durcissement contre l'imbrication excessive ; format §8 | 136 | 28 | 13 | 34 |

Le fichier `SHA256SUMS` du même dossier est contrôlé par `sha256sum -c` (diffs, outils, fichiers finaux, arbre en série). Son contenu :

```
77b843835c5d3ac5ccc6514b579a28f6c06087d1e8662b0e31f9defa3821dc8b  diffs/CB-0a.diff
3e724c74b76c73a78f0dbbacb19b4372510823a534ce2e43b8225b97a3b6397c  diffs/CB-0b.diff
e74cf0b14e9d4f4cb16fbf9ca10dd11f598db6c0129cec1254e0d2a4277f7c37  diffs/CB-1a.diff
e51f7e78d83de865f62ef68a6621f21e211756d1b3a8f3479f11b5947a4e9af9  diffs/CB-1b.diff
7c7af80286de07eded0bb0aa20e6a61601d17c0d9c91a04cc0f4ddfd14c6b1b2  diffs/CB-2a.diff
8f401c0ceb3e48ac8dbb9858655abd6b954274205896031ffdde2beb31c18c3f  diffs/CB-2b.diff
cb71dcd95182c6b0e946341d3017a110f3623ae9da728dd9a970fc9835f64e7a  diffs/CB-2c.diff
8d1f6f7e7d5ba26b64b90b9cd6f8d52e19afbe61dd6cd2796fe8170978c4a071  .github/workflows/gates.yml
95b0ffdeb95ad7e25c0ef69f42d1b49c89afb2835b2a11dc9a32a419ccab4e3f  enforcement/verdict-suite-s2.py
03a503d5da725e3578e923ef214826fd458c48d0e48db3030206366bf0ac6a2e  enforcement/tests/run-fixtures-verdict-suite-s2.py
3908b0944bac803df5d2e447dddc9344d5dc61db2e5531d729b5c926425762d8  s2bis/shogen_s2bis/__init__.py
bda7b00bfe0a80cc52fc20e286b6164544c9792d75b9e0554167f5dd4e9b45bf  s2bis/shogen_s2bis/collecte/__init__.py
77f909e56b1a6f3290dbfdd34c9aa4ce8cde66bee65694220724853343b7035a  s2bis/shogen_s2bis/collecte/config.py
c87b0045ec0853d07a84ed6e778fed0756600512a34152f3964a21577df4bacb  s2bis/shogen_s2bis/collecte/journal.py
9be14d84de05529ea2d0a119b4d6b20de994336391b8bed7efc0d1f429a36a11  s2bis/tests/__init__.py
4f00f6a686b67d3aab93d64e049c01f6dbd33582ed95c609af3627cf3ac105ef  s2bis/tests/test_config.py
f03465b5763cd543ca264b63162e1ec5269eca650d86b15b5d7d62b90f2668cb  s2bis/tests/test_garde.py
93e1aaf6d21d93ea44635314d14714ead8713ff9e21d92582eee18ad4a5cc6fe  s2bis/tests/test_fitness.py
e920f73b863d9474e430a77d2a65336e2829a2003b5344dc954d16914168349c  s2bis/tests/test_journal.py
09b5b4a364ac810e1e4b393b5db05267c4c01b76b5a9a6c2a208e5712009262c  s2bis/tests/test_fichiers.py
9f717fb496ebe1603e7445b8230cb2608de9657242e72a67e7fb4b85acbc43aa  s2bis/tests/test_reprise.py
bb515ef7050fec64e894d93149a9d1d044effb36f4e7bc7e513dabf66b98272f  s2bis/tests/test_trous.py
c6d30c092cd3aec4b9e3e10215f62f763dfc9b8eaadb36cc084693ffc923e6c7  docs/adr-0029/s2bis/G6-PAQUET-S2BIS.md
5c4809098e7c599239f58e294c1e76e5d370c4b97ecfcefebcdf3f5f976c7135  docs/adr-0029/s2bis/METRIQUES-S2BIS.md
ed21d51cda0919c0ef478f51b313b2f0a761d5a1aefb1c3e54d4195ec4b9e575  docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md
```

Les outils de contrôle, hors dépôt, sont dans le même dossier et ont aussi leurs empreintes dans `SHA256SUMS` :
- `campagne.py` (`5720e25e…`) : lanceur de mutants ;
- `mutants-cb0a.py`, `mutants-cb0b.py`, `mutants-cb1.py`, `mutants-cb2a.py`, `mutants-cb2.py` ;
- `faire_diff.sh`, `longueurs.py`.

Autres emplacements :
- preuves (sorties rouge et vert, campagnes, gates) : sous-dossier `journal/` ;
- arbres après chaque diff : `cb0a` à `cb2c` ;
- série appliquée sur `34a17d8` : `serie`.

## 3. Exigences couvertes

**Correspondance exigence par exigence**
- **E-C-01** (CB-0b) : la frontière d'imports est lue par `ast`. Sont admis la bibliothèque standard et le sous-paquet. Sont refusés l'import relatif sortant, l'import dynamique et le sous-paquet sans règle. Tests : `test_frontiere_du_paquet`, `test_frontiere_refuse`.
- **E-C-02** (CB-0a) : chargement, sha256 des octets lus, champs exacts, types, bornes, cohérence ; refus `CONFIG/…`. **Partiel** : « `run_params` porte le commit » relève de CB-18.
- **E-C-16** (CB-1b) : verrou `flock` exclusif sans attente. Une seconde instance lève `JournalOccupe` sans rien écrire. La libération à la fermeture est testée.
- **E-C-18** (CB-1a) : `seq`, `prec` (sha256 de la ligne, saut de ligne compris), genèse de 64 zéros, forme canonique. Les octets attendus sont écrits à la main ; la chaîne est recalculée par un code de test indépendant.
- **E-C-19** (CB-1a) : fsync au marqueur seulement (espion par inode). Un point de contrôle suit la fenêtre qui clôt l'heure.
- **E-C-20** (CB-2a, rattrapage en CB-2c) : un fichier par jour UTC, clôture, sommes au format `sha256sum`, chaîne continue ; deux bascules testées sur 1 442 fenêtres.
- **E-C-21** (CB-2b et CB-2c) : la reprise repart du dernier enregistrement intègre.
  - Formes de queue testées : ligne coupée, octets NUL, ligne non canonique, ligne mal chaînée, ligne trop longue, imbrication excessive.
  - Une queue n'est jamais réécrite. Elle est déclarée dans `reprise` (fichier, position, octets, sha256) et un segment neuf s'ouvre.
  - Si le segment neuf est lui-même illisible, la reprise se replie sur le précédent.
- **E-C-22** (CB-2c, avec CB-1a et CB-2b) :
  - un `trou` (cause `arret`, `horloge_reculee` ou `saut`) précède le marqueur qui suit des fenêtres sans marqueur ;
  - la fenêtre du redémarrage et les fenêtres closes sont refusées ;
  - après une horloge reculée, aucune fenêtre n'est répétée.
- **E-C-40** (CB-0a) : garde réseau sur toute la suite.
- **E-C-41** (CB-0b) : fonctions de fitness (frontière, réseau, mêmes octets sous cinq graines de hachage, compilation avec les avertissements en erreur) ; baseline versée.
- **PROPOSITION §1 pt 6** : job neuf ; résumé final exigé ; aucun saut admis ; plancher relevé à chaque diff ; étapes lues par K-01 et K-02. La suite S2 est inchangée (405, OK, skipped=2).
- **Q-G-05 et Q-G-06** : limite SAST écrite dans la pièce G6, compilation avec avertissements en erreur, pièce G6 versée.
- **Q-C-11** (ENTRELACEMENT-D5-1) : le verrou et la chaîne en sont le moyen de fermeture ; prononcer la fermeture reste votre acte.

**Tests et mutants obligatoires de la proposition §2.4**
- « prec décalé d'un rang » : M-1a-04.
- « seq non incrémenté au changement de fichier » : M-2a-02.
- « fsync retiré » : M-1a-07.
- « verrou retiré » : M-1b-01.
- « queue tronquée sur place » : M-2b-01.
- « doublon admis » : M-2c-05.
- « chaîne remise à zéro » : M-2a-01.
- « import shogen_s2 ajouté » : M-0b-07.
- « vraie socket » : M-0a-14, M-0a-16, M-0a-18.

Tous sont tués par leur test nommé.

**Hors périmètre** : E-C-17, E-C-23, E-C-24 (test de conformité au format, CB-18 ; la spécification est commencée) et les autres sous-lots.

## 4. Rouge avant, vert après

| diff | rouge (avant le code) | vert |
|---|---|---|
| CB-0a | `test_config` : ImportError ; `test_garde` : garde absente ; FAILED (errors=2) | 6 tests |
| CB-0b | runner : TypeError (vérificateur sans paramètre), puis K-02 seul en échec (job absent) ; fitness : une sonde `import shogen_s2` et un échappement invalide donnent FAIL (frontière) et ERROR (compilation) | runner 27 cas, suite 10 |
| CB-1a | ImportError (module `journal` absent) | 14 |
| CB-1b | test « seconde instance » en échec | 15 |
| CB-2a | KeyError : aucun fichier du jour suivant | 16 |
| CB-2b | 8 tests de reprise en erreur, sous 3.10 et 3.11 | 25 |
| CB-2c | 5 tests de trous en échec | 34 |

Deux tests sont verts avant le code, par construction :
- `test_boucle_locale_permise` : non-régression de la garde ;
- `test_frontiere_refuse` : il teste le vérificateur de frontière lui-même.

**Gates sur l'arbre en série**
- Suite s2bis par le vérificateur : conforme sous 3.11 et 3.12 (Python de l'image CI). Sous 3.10 et 3.13 avec `-X dev -W error` : OK.
- Runner du vérificateur : 27 cas, 0 échec.
- Suite S2 par son vérificateur : 405, OK (skipped=2), conforme.
- Hook : 54 cas.
- Gate des secrets `--tree` (sur un index jetable) : 682 fichiers, OK.
- R-13 : aucun marqueur.
- `cargo --locked --offline xtask verify` (cible dédiée, sortie redirigée, lignes de verdict seules) : S-G1 à S-G8 vertes, S-G9 rouge (1 violation). Le témoin (tête sans mes diffs, mêmes exclusions) donne la même violation : voir E-5.

## 5. Mutants

Contrat (SHOGEN-MUT-FATAL-1) : sortie 1 et marque du test nommé = tué ; sortie 0 = vivant ; tout autre code = FATAL. Chaque campagne commence par un témoin vert ; chaque mutant tourne sur une copie fraîche.

**Passage final** : CB-0a 19/19, CB-0b 20/20, CB-1a 19/19, CB-1b 4/4, CB-2a 11/11, CB-2b 15/15, CB-2c 14/14, soit **102/102** ; tous les témoins verts.

Passages antérieurs, tous consignés dans `journal/` :
- **CB-2c, premier passage** : 10 tués, 2 vivants.
  - M-2c-04 (cause non remise à `saut`) : il manquait un cas « reprise, marqueur sans trou, puis saut ».
  - M-2c-07 (état non avancé après le trou) : l'assertion ne regardait pas assez d'enregistrements.
  - Tests renforcés, campagne relancée : 12/12, puis 14/14 avec les deux mutants du durcissement.
- **CB-0a** : après le durcissement, M-0a-13 était inapplicable, donc FATAL et passage invalide. Mutant corrigé, campagne relancée : 19/19.

Notes :
- CB-1b n'a que 4 mutants, mais le sous-lot CB-1 en compte 23.
- M-1b-02 (verrou bloquant) est tué par le délai interne du test (5 s), sans pendre la suite.
- Les mutants qui retirent la garde ont tenté de vraies sorties vers des cibles réservées (voir E-6).

## 6. Écarts, à adjuger

- **E-1 Tailles.** Les sous-lots du G0 sont livrés en 7 diffs. R-25 est tenu (chaque diff ≤ 200 lignes de code), mais pas le tableau §2.3 du G0. Il faut le dire au calendrier (Q-G-04) et revoir l'estimation des sous-lots restants de P1.
- **E-2 Base avancée pendant le travail.** Aucun conflit ; la série est vérifiée sur `34a17d8`.
- **E-3 Tests écrits après le code**, repérés en préparant les mutants. Leur rouge est montré par le mutant correspondant :
  - CB-1a : `ws` flottant (M-1a-18) ;
  - CB-1b : libération du verrou (M-1b-04) ;
  - CB-2b : segment ouvert par un marqueur (M-2b-12), horloge reculée d'un jour (M-2b-14), lecture coupée qui porte un champ `suivante` (M-2b-15) ;
  - CB-2c : cause remise à `saut` et trou en double (M-2c-04, M-2c-07) ;
  - imbrication excessive : config (M-0a-19), journal (M-2c-13, M-2c-14).
- **E-4 Durcissement découvert en relecture.** Une ligne JSON très imbriquée faisait lever `RecursionError` sous 3.10 à 3.13. Ce n'est pas une sous-classe de `ValueError`, donc elle n'était pas capturée. Elle aurait fait planter la reprise et la configuration au lieu d'un refus nommé. Corrigé dans CB-0a et CB-2c.
- **E-5 S-G9 rouge sur l'extraction.** La violation est identique au témoin sans mes diffs. Doc 17 contient exactement une ligne qui renvoie vers un dossier exclu par le brief (je n'ai affiché que le compte). À rejouer sur le dépôt réel.
- **E-6 Mutants de la garde.** Ils ont fait de vraies opérations réseau, vers des cibles réservées seulement : TEST-NET-1 `192.0.2.1` en TCP et UDP, et la résolution de `example.invalid` par le résolveur de l'hôte (8.8.8.8).
- **E-7 Choix de conception pris dans la latitude du G0**, à valider :
  - **(a) Vérificateur.** J'ai paramétré le vérificateur existant au lieu d'en écrire un neuf ; ses cas par défaut restent verts.
  - **(b) Plancher.** Il vit dans `gates.yml` (`--plancher N`), relevé à chaque diff ; l'égalité avec le compte des tests n'est pas mécanisée.
  - **(c) Avertissements en erreur.** Je m'en tiens à la compilation, lettre de Q-G-05, sans `PYTHONWARNINGS=error` sur toute la suite.
  - **(d) Configuration.** Refusés : les nombres à virgule (les décimaux s'écrivent en chaîne), les entiers de plus de 30 caractères et les listes vides.
  - **(e) Format des journaux.**
    - Aucun flottant ; UTF-8 sans échappement ; `prec` hache la ligne, saut compris.
    - Le point de contrôle porte seulement `ws` : la tête qu'il porte est son `prec`, et son empreinte est la tête exportée.
    - Noms : `<préfixe>-AAAA-MM-JJ-<k>.jsonl` ; sommes dans `<préfixe>.sha256` ; verrou `<préfixe>.verrou`.
    - Borne de 4 Mio par ligne.
    - La fenêtre du redémarrage est perdue.
    - Le trou est déclaré au marqueur suivant.
    - Un journal sans aucun enregistrement intègre donne le refus `JOURNAL/illisible` ; aucune seconde chaîne n'est créée.
  - **(f) Garde réseau.** `ReseauInterdit` dérive de `BaseException`, pour qu'un attrape-tout du code testé ne la masque pas ; la boucle locale est permise (serveurs factices de CB-5).
- **E-8 Outil local.** PyYAML, déjà installé sur l'hôte, a servi à un contrôle de syntaxe de `gates.yml` en lecture seule. Rien n'est ajouté au dépôt (R-8).
- **E-9 Journal G1.** Il est rendu dans ce message (§9) : l'environnement interdit d'écrire un fichier de rapport. `SHA256SUMS` est bien écrit.

## 7. Items à former (PAROXYSME)

- **I-1** Aucun fsync du dossier après la création d'un fichier journal : la durabilité de l'entrée de répertoire n'est pas établie. Déclencheur proposé : G2 de P1 ou CB-18.
- **I-2** Aucune analyse statique de sécurité (SAST) sur `s2bis/`. Étendre SHOGEN-SAST-PYTHON-RECALCUL-1 ou former un item neuf.
- **I-3** La reprise ne contrôle pas le lien entre la première ligne d'un fichier et la dernière du fichier précédent. Elle compare `seq` par valeur : un `true` à la place de 1 serait admis. Contrôle strict à prévoir au lecteur, à inscrire aux G0 de RB-1 et RB-18.
- **I-4** Un appel direct au module C `_socket` échappe à la garde réseau.
- **I-5** `JOURNAL/illisible` arrête l'observateur jusqu'à une intervention N3. À écrire dans la procédure d'intervention (DB-6) et dans les exercices de mise en service.
- **I-6** L'écrivain ne se partage pas entre fils : contrainte pour CB-4, écrite au format §5.
- **I-7** Estimation des sous-lots restants de P1 à revoir (voir E-1).

## 8. Questions

1. **Q-1** Acceptez-vous le découpage et la numérotation (CB-0a, 0b, 1a, 1b, 2a, 2b, 2c), avec un commit par diff ?
2. **Q-2** Faut-il mécaniser « plancher égal au compte des tests » par un cas K-03 ? Contrepartie : un conflit systématique sur la ligne `--plancher`, car RB-0 à RB-6 écrivent aussi dans `s2bis/tests/`.
3. **Q-3** Faut-il serrer avec `PYTHONWARNINGS=error` sur toute la suite s2bis ?
4. **Q-4** La fenêtre du redémarrage doit-elle rester refusée (une fenêtre perdue par redémarrage), ou être admise si elle n'a encore aucune ligne ? C'est un paramètre de censure à sceller avant le gel.
5. **Q-5** Les choix de format de E-7 (e) sont-ils à sceller tels quels au paquet ?
6. **Q-6** SHOGEN-CI-S2-CABLAGE-1 : son déclencheur (« prochain lot qui touche gates.yml ») est atteint, et K-01 lit désormais les étapes de `s2-harness-unittest`. L'item est-il fermé par ce lot ?
7. **Q-7** SHOGEN-ENTRELACEMENT-D5-1 : prononcez-vous la fermeture par construction pour S2-bis ?
8. **Q-8** Pouvez-vous rejouer `cargo xtask verify` sur le dépôt réel après application, pour S-G9 ?

## 9. Journal G1 (provenance)

**Lu** [lu]
- Le brief.
- G0 `G0-COLLECTE-RECALC-DEPLOI.md` (entier), `PROPOSITION.md` (entier, 928 lignes), `AVIS.md` (entier).
- ADR-0029 : l.1-14, l.214-253, l.375-434 (dont l'ajout daté de la l.395).
- `docs/METHODE-PARTIES.md`, `docs/adr-0029/G0-lots-S2BIS.md`, `docs/PASSATION-CLOUD.md` (entiers).
- Annexe D d'ADR-0028 : l.32-48 (liste D.2, sans ouvrir aucune pièce).
- Annexe B d'ADR-0028 : l.42, 43, 45, 55, 79, 80, 354, 685, 760, 762, 764, 798, 892-896, 916.
- `gates.yml`, `enforcement/verdict-suite-s2.py`, `run-fixtures-verdict-suite-s2.py`, `hooks/pre-commit`, `run-fixtures-hooks.sh` (entiers) ; `gate-secrets.sh` par recherche.
- `xtask` : `main.rs` l.1-80, en-têtes des gates S-G1 à S-G9, `sg4.rs` et `sg5.rs` en partie.
- `s2-harness/shogen_s2/journal.py` (entier), `window.py` l.1-80, `README.md` l.1-60.
- `JOURNAL.md` : ses 6 dernières lignes.
- `scripts/controle/fm11.py` l.1-60 ; G1 de PLAN-S2BIS (titres et l.1-25).
- `DEVOPS.md` et `R-8-outillage.md` par recherche ; `Cargo.toml` (licence) ; `LICENSE.txt` de CPython 3.12 (l.1-3 et l.73) ; `.gitignore` ; `/etc/resolv.conf`.

**Non ouverts** : `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, aucun `*.jsonl` réel, aucune pièce de la liste D.2. `SHOGEN_S2_CAMPAGNE_CONTROL` n'a jamais été posée ; le vérificateur et `campagne.py` la retirent de l'environnement.

**Valeurs de référence calculées hors du code**
- sha256 des octets de configuration `VALIDE` : `printf` puis `sha256sum`.
- 4 lignes canoniques, 3 maillons et la tête finale du journal : `printf` puis `sha256sum` ; `od -c` pour le « é » en UTF-8.
- Instants epoch : `date -u -d`.
- Chaque texte qui porte une barre oblique inverse est contrôlé sur les octets écrits (grep à partir de `printf '\134…'`, `od -c`).

**Chiffres recomptés** : lignes par `git apply --numstat` et `wc -l` ; tests par la découverte `unittest` ; mutants par les fichiers `journal/final-mutants-*.txt`. Aucun chiffre de seconde main.

**Exposition, à l'usage du contrôle FM-1.1**
- Le chemin du scratchpad imposé contient le motif de session de la liste FM-1.1 (retouche de versement).
- Les noms `control.jsonl`, `journal.jsonl` et `raw.jsonl` sont apparus comme texte, en lisant des fichiers du dépôt qui les citent : `gates.yml`, runner l.24, `PASSATION-CLOUD.md`, `README.md` et `journal.py` du harnais.
- Des noms de dossiers interdits figurent dans mes options `--exclude` (texte du brief) et dans un motif de comptage sur doc 17 (sortie : le nombre 1, rien d'autre).
- Aucune ligne de D.2 n'a été lue ni affichée.
