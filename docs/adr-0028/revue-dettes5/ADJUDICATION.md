# Adjudication de l'orchestrateur sur le rapport du générateur de DETTES-T5 (2026-10-09 20:24:20 UTC, `date -u`)

Pièce : `RAPPORT-GENERATEUR.md` (générateur `claude-opus-5-5` ; FM-1.1 : 0 fragment). Règle « aucune dette ».

**Faits établis par l'orchestrateur :**
- `git ls-remote https://github.com/actions/checkout 'refs/tags/v7.0.1*'` (lecture seule, 2026-10-09 20:24:20 UTC) : `3d3c42e5aac5ba805825da76410c181273ba90b1  refs/tags/v7.0.1` (étiquette légère) : le SHA épinglé est celui du tag v7.0.1 ; résidu B.47 levé.
- Libellés Windows [2nd, recherche du jour] : le changelog GitHub du 2026-05-14 (`` update the `runs-on:` target … to the new label `windows-2025-vs2026` ``) et le README d'`actions/runner-images` donnent `windows-2025` et `windows-2025-vs2026` comme libellés ; `windows-2025-vs2026` est un libellé d'essai appelé à rejoindre `windows-2025` après la migration (issue runner-images n° 14004 : `windows-2025` sert déjà l'image vs2026 depuis le 2026-05-05).

**Décisions :**
- **Q-1** : variante **B** (`windows-2025`, libellé durable) ; la ligne « Runner Image » du premier run de la PR qui porte ce lot sera lue et consignée au JOURNAL par l'orchestrateur.
- **Q-2** : oui, dans ce lot : un contrôle qui refuse tout `runs-on` (et toute entrée de matrice `os`) en `-latest` dans les workflows, avec tests et câblage (job g1 ou controle), sur la forme des contrôles d'`enforcement/`.
- **Q-3** : gate Linux gardée, aucun saut ; une phrase dans l'installeur : sous Git Bash, `test -x` suit l'heuristique de MSYS (fichier qui commence par `#!`) [inféré] ; le premier passage de l'installeur sur le poste local (acte du mainteneur) le confirmera ; ajouté à la liste des actes extérieurs.
- E-1 à E-8 admis. Actes extérieurs : n° 4 (v7.0.1) fait ; n° 6 (lectures du prochain run) et n° 7 (annexe, inscription de SHOGEN-G1-FORGE-1) faits par l'orchestrateur au versement ; n° 8 : la G2 de ce lot touche le chemin S2 : enregistrement de rôle G2 selon la consigne DT3-C.

## Ajout daté du 2026-10-09 21:28:17 UTC (`date -u`) : adjudication de la phase 2 du générateur (section datée de 21:26:12 UTC)
Pièce : `RAPPORT-GENERATEUR.md` (FM-1.1 à faire au versement). Faits contrôlés par l'orchestrateur : `yaml.safe_load` du `gates.yml` de 6356a94 : OK ; de 4a4806f et de la tête b837efe : erreur `mapping values are not allowed here`, l.112 col. 94 ; les six autres workflows : OK. Sur la PR n° 10, le run du workflow `gates` a échoué sans job (cohérent) ; les autres workflows échouent sans machine (dépôt privé : acte de l'investisseur).
- **C-1 (DT5-0)** : défaut de l'orchestrateur (DT4-a, nom d'étape non vérifié par un analyseur YAML) ; DT5-0 commis seul et tout de suite, après relecture par l'orchestrateur et la chaîne complète ; la G2 du lot DETTES-T5 le relit avec la série.
- **C-2 (aucune dette, au lieu d'un item)** : diff neuf **DT5-8** : un contrôle qui charge chaque workflow de `.github/workflows/` avec un analyseur YAML et refuse tout fichier illisible (refus nommé, sortie 1 ; erreur interne 3), câblé au job g1 et au crochet local s'il en porte les étapes, avec tests (un workflow invalide synthétique refusé, la forme de DT4-a comprise ; la tête corrigée acceptée) et mutants. Dépendance : contrôle R-8 écrit **avant** tout emploi (`docs/R-8-outillage.md`) ; préférer le paquet de la distribution (`python3-yaml` d'Ubuntu 24.04, présent ou installé par `apt` dans le job, version au journal) à `pip` ; si aucune forme n'est admissible, proposer la forme et dire pourquoi.
- Q-1 à Q-3 : appliquées comme adjugées. E-9 (grep récursif sur deux dossiers de la copie) admis, rappel de la règle ; E-10, E-11 admis. Série à rebaser sur la tête qui portera DT5-0 commis.

## Ajout daté du 2026-10-09 21:44:53 UTC (`date -u`) : adjudication de la phase 3 (section datée de 21:43:41 UTC)
- DT5-8 admis pour la G2. **Q-4** : pas de câblage au crochet local (le crochet ne porte aucune étape Python du job g1 ; exiger PyYAML sur le poste local ferait refuser tout commit d'un poste qui ne l'a pas) ; la chaîne de commits de l'orchestrateur rejoue désormais `enforcement/workflows-yaml.py` avant chaque commit (procédure, chaînes `chaine_*.sh`) ; la limite est à écrire par la G2 si elle la juge juste.
- E-12, E-13 admis ; L-5 (YAML 1.1 de PyYAML, analyseur propre de la forge) : limite à écrire dans la docstring du contrôle si elle n'y est pas (la G2 le vérifie). À lire au premier run de la PR qui porte le lot : sortie de `dpkg-query` et branche prise ; ligne « Runner Image » (Q-1).
- Suite : G2 neuve à 100 % de DT5-0 (commis, c1122de) et DT5-1 à DT5-8 (non commis, sur c1122de), réviseur ≠ générateur, enregistrement de rôle G2 par `oracle_record.py` (consigne DT3-C : DT5-2 touche le chemin S2).

## Ajout daté du 2026-10-09 22:37:10 UTC (`date -u`) : adjudication de la G2 (ACCEPTE-AVEC-CORRECTIONS, C-1 à C-8)
Pièce : `g2/RAPPORT-G2.md` (réviseur neuf `claude-opus-5-5`, Gate 0 sur le transcript ; FM-1.1 : 0, deux versions de fm11) ; enregistrement de rôle G2 `shogen-c1122de-G2-20261009T220715Z-28656.json` (sha256 `4595fc5e…`, `--verifier` conforme).
- **C-1 à C-8 adoptées** telles que proposées : diffs `g2/propose/DT5-2-propose.diff`, `DT5-5-propose.diff`, `DT5-7-propose.diff`, `DT5-8-propose.diff`, appliqués en diffs séparés après DT5-8 (DT5-9 à DT5-12, R-25) ; plancher `controle-unittest` 35.
- **C-9 (aucune dette)** : la phrase fausse sur « un envoi » (C-6) est aussi dans `s2bis/tests/__init__.py` : même correction documentaire, dans un diff de ce lot.
- **C-10 (aucune dette, [abs] du réviseur)** : `runners-epingles` et `workflows-yaml` lisent tout fichier de `.github/workflows/` dont l'extension, pliée en casse, est `.yml` ou `.yaml`, fichiers cachés compris ; tout autre fichier y est compté et nommé à la sortie (non refusé) ; tests.
- **TMPDIR à noms fixes de `cargo test -p xtask`** : item existant SHOGEN-XTASK-TMP-NOMS-FIXES-1 (lot de dettes LOT-04, file) : aucun item neuf.
- **E-1** (l'enregistrement extrait le commit entier par `git archive`, dossiers interdits compris, dans le TMPDIR du réviseur ; hachés, jamais affichés) : admis pour cette relecture ; défaut structurel de l'outil : ajouté au lot DETTES-T7 (outils de preuve) : extraction sans les emplacements interdits, liste des chemins exclus consignée dans l'enregistrement, test. E-2 à E-6 admis.
- O-9 : inscription de SHOGEN-G1-FORGE-1 à l'annexe B au versement (acte n° 7 déjà prévu). Prémisse de DT5-3 mesurée (git 2.43.0 ignore un hook en 644) : à écrire au rapport de versement.
- Suite : corrections par le générateur, puis contre-contrôle neuf.

## Ajout daté du 2026-10-09 23:39:53 UTC (`date -u`) : adjudication du contre-contrôle, passe 1 (CONFORME-AVEC-RÉSERVES, R-1 à R-6)
Pièce : `g2/cc/RAPPORT-CC.md` (contre-contrôleur neuf `claude-opus-5-5`, Gate 0 sur le transcript ; FM-1.1 : 0, deux versions) ; tête relue `094fa5d`, série DT5-1..14 `28da581e…`.
- **R-1 à R-6 adoptées** dans la forme des diffs de `g2/cc/propose/` (`R-1` à `R-6-propose.diff`), appliqués en diffs DT5-15 à DT5-20, dans l'ordre, après DT5-14.
- **C-11 (aucune dette, au-delà de R-3)** : au lieu de seulement écrire la limite, les deux gardes réseau (`scripts/controle/tests/` et `s2bis/tests/__init__.py`, qui doivent rester égales octet pour octet si c'est la règle adjugée) refusent aussi `socket.getaddrinfo` et `socket.getnameinfo` pour tout hôte non local (boucle locale et littéraux de 127.0.0.0/8 et ::1 admis), avec tests (sonde : TENTATIVES +1, OSError) ; si une suite existante dépend d'une résolution non locale, le dire avec la mesure et garder la limite R-3 écrite. Diff DT5-21.
- E-14 du générateur corrigé par le contre-contrôle (les 3 mutants FATAL adaptés : 4/4 tués) : noté. Écarts du contre-contrôleur admis.
- Suite : générateur (DT5-15 à DT5-21), puis passe 2 du même contre-contrôleur.

## Ajout daté du 2026-10-10 00:22:41 UTC (`date -u`) : adjudication du contre-contrôle, passe 2 (CONFORME-AVEC-RÉSERVES, R-7, R-8)
Pièce : section datée de 2026-10-10 00:20:11 UTC de `g2/cc/RAPPORT-CC.md` (même contre-contrôleur ; FM-1.1 : 0). R-1 à R-6 levées ; C-11 juste sur son objet.
- **R-7 et R-8 adoptées** dans la forme de `g2/cc/propose/R-7-propose.diff` (`6586e5a2…`) puis `R-8-propose.diff` (`7db1663f…`), éprouvées par le contre-contrôleur sur la série entière (21 étapes en 0, mêmes comptes) : diffs **DT5-22** et **DT5-23**, repris à l'identique par le générateur, qui les relit et en répond ; si l'identité est constatée par l'orchestrateur, clôture CONFORME sans passe 3 (précédent : DT4-g, B.91).
- **Lapsus de l'orchestrateur, déclaré** : l'ajout de 23:39:53 UTC (C-11) parlait de « deux gardes » et nommait `scripts/controle/tests/` ; les gardes sont trois : `s2-harness/tests/__init__.py`, `s2bis/tests/__init__.py`, `scripts/calib-actifs/tests/__init__.py` ; R-8 rend les trois blocs égaux octet pour octet.
- **Épingle de CALIB-ACTIFS** : le `SHA256SUMS` de `scripts/calib-actifs` n'est **pas encore** épinglé au JOURNAL (`1d0cae17` absent du JOURNAL et de l'annexe B ; E-CA-27 : épinglage après la G2 et INV-1, non fait, B.85 « sans épinglage ni lancement ») : aucun ré-épinglage ; l'épingle se posera sur l'état final, après DETTES-T2 (qui se recalera sur la tête portant DT5-23).

## Ajout daté du 2026-10-10 00:34:20 UTC (`date -u`) : clôture de la revue
DT5-22 et DT5-23 (générateur, phase 6, 00:33:31 UTC) sont identiques octet pour octet (`cmp`, par l'orchestrateur) à `g2/cc/propose/R-7-propose.diff` et `R-8-propose.diff`, formes que le contre-contrôleur a éprouvées sur la série entière en passe 2 (21 étapes en 0, mêmes comptes, 16/16 et 2/2 mutants tués) ; le générateur a rejoué les rouges des trois modules ; R-7 et R-8 levées ; **verdict final : CONFORME**, sans passe 3 (précédent : DT4-g, B.91). Série DT5-1 à DT5-23 sur `094fa5d`, empreinte `30e600ca…`. Chaîne de commits : `chaine_d5.sh`.
