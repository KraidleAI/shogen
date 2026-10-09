# Adjudication de l'orchestrateur sur le rapport du générateur de DETTES-T4 (2026-10-09 18:47:13 UTC, `date -u`)

Pièce : `RAPPORT-GENERATEUR.md` et `INVENTAIRE.md` (générateur `claude-opus-5-5` ; FM-1.1 : 0 fragment). Règle « aucune dette ».
- **Q-1** : exemption des 11 lignes de `docs/adr-0028/sim-niveau/SHA256SUMS` gardée, épinglée par numéros de ligne et sha256 de ces lignes (`7f45c55e…`) ; motif écrit dans le script : lignes gardées à la clôture de SHOGEN-SIM-SOMMES-1 (le paquet les cite par numéro), fichiers jamais versés (poste local). Toute autre ligne absente reste un refus.
- **Q-2** : refus d'un `*.jsonl` listé : confirmé.
- **Q-3** : si la liste de `xtask/src/sg5.rs` a le sens « dossiers interdits » (à établir par lecture ciblée de sg5.rs et de ses tests), `docs/adr-0028/execution/` y est ajouté dans un diff **DT4-b** avec son test (aucun item) ; sinon, question écrite au rapport avec la lecture.
- **L-1** : les noms `SHA256SUMS.raw`, `SHA256SUMS.copies`, `SHA256SUMS-ECHANTILLONS.txt` sont hors du contrôle (nom exact `SHA256SUMS` seulement) : dit dans la docstring et le README des contrôles, avec la raison (fichiers listés jamais versés).
- **L-2** : à préciser par le générateur (« la forge ne démarre pas les jobs » : quelle forge, quels jobs ?). **L-3**, **L-4** : notés.
- **E-2** admis (copie creuse sans dossiers interdits ni *.jsonl, sortie de noms seulement, hors docs/) ; rappel de la règle pour la suite. E-1, E-3 à E-5 admis.

## Ajout daté du 2026-10-09 19:26:58 UTC (`date -u`) : adjudication de la G2 (ACCEPTE-AVEC-CORRECTIONS, C-1 à C-3)
Pièce : `g2/RAPPORT-G2.md` (réviseur neuf `claude-opus-5-5` ; FM-1.1 : 0 fragment). Diff neuf **DT4-d** après DT4-c (forme : `g2/DT4-d-propose.diff`, donnée) :
- C-1 : un `SHA256SUMS` dont le chemin réel est interdit est refusé sans ouverture ; C-2 : les trois tests (N3, N8 tués) ; C-3 : les deux `docs/adr-0028/sceau/**/PAQUET.sha256` nommés hors du contrôle, avec la raison (rejoué par `scripts/sceau/verify.sh` ; le second échoue par construction, paquet rescellé).
- **C-4 (L-G2-1, aucune dette, au lieu d'un item)** : `os.walk` avec `onerror` qui fait sortir en 3 (erreur interne) ; test par doublure qui lève PermissionError ; mutant.
- **Q-G2-1** : le serrage est gardé (une seule forme de chemin, sans `./`) ; il est écrit au README des contrôles, avec la consigne : un `SHA256SUMS` versé ne nomme que des pièces versées.
- Enregistrement `oracle_record.py` : sans objet (lot hors du chemin S2 ; la consigne DT3-C vise le chemin S2). E-G2-1 à E-G2-3 admis.

## Ajout daté du 2026-10-09 19:58:14 UTC (`date -u`) : adjudication du contre-contrôle (CONFORME-AVEC-RÉSERVES, R-1 à R-3)
Pièce : `g2/cc/RAPPORT-CC.md` (contre-contrôleur neuf `claude-opus-5-5` ; FM-1.1 : 0 fragment). Diff **DT4-e** après DT4-d (forme : `g2/cc/DT4-e-propose.diff`, donnée) :
- C-5 (R-1) : tout composant de chemin qui finit en `.jsonl` est interdit ; C-6 (R-2) : voisins de préfixe dans les deux cas de lien (K1, K2 tués) ; C-7 (R-3) : motif « hors forme » exigé, cas barre oblique inverse (K3, K4 tués).
- **C-8 (O-5, aucune dette)** : la comparaison aux emplacements interdits se fait aussi sur le chemin plié en casse (`casefold`), pour qu'un système de fichiers insensible à la casse (poste Windows) ne puisse pas contourner la liste ; test sur chemins synthétiques en casse mêlée.
- **C-9 (O-6, aucune dette)** : même règle des composants `.jsonl` (et du pliage de casse si S-G5 compare des chemins) dans `xtask/src/sg5.rs`, dans un diff **DT4-f** avec ses tests Rust, si la lecture ciblée de sg5.rs montre que la règle s'y applique ; sinon une phrase écrite au rapport qui dit pourquoi.
- O-4 noté (FIFO : échec fermé, impossible dans git). E-CC-1 à E-CC-3 admis.
- Forme de versement retenue (point 6 du CC) : elle sera suivie par l'orchestrateur au versement de ce lot.

## Ajout daté du 2026-10-09 20:27:50 UTC (`date -u`) : adjudication de la passe 2 du contre-contrôle (CONFORME-AVEC-RÉSERVES, R-4)
R-1 à R-3 levées ; C-8 et C-9 justes (aucun faux interdit dans les 1 123 chemins indexés). **C-10 (R-4)** : diff **DT4-g** (forme : `g2/cc/DT4-g-propose.diff`) : quatre voisins autorisés lus (`rapportsX`, `adr-0028/Execution-bis`, `b.jsonlx`, `ADR-00250`), motif exigé ; preuve : PX4 tué ; plancher 26 inchangé. E-CC-4 admis.

## Ajout daté du 2026-10-09 20:30:18 UTC (`date -u`) : clôture de la revue
DT4-g (générateur, 20:29:36 UTC) est identique, lignes ajoutées et retirées, à `g2/cc/DT4-g-propose.diff`, forme que le contre-contrôleur a éprouvée sur copie en passe 2 (suite verte, Ran 26, PX4 et 17 mutants tués) ; R-4 levée ; **verdict final : CONFORME**, sans passe 3 (comparaison faite par l orchestrateur, `diff` des lignes +/− : identiques).
