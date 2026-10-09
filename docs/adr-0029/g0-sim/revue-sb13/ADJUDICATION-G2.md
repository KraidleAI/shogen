# Adjudication de l'orchestrateur sur la G2 de SB-13 (2026-10-08, après 22:01 UTC)
Pièce d'entrée : `g2/RAPPORT-G2.md` (à lire en entier). Le brief `BRIEF-SB13.md` reste en vigueur (règles, interdits durs, commandes) ; aucune écriture git ; `date -u` avant toute date ; NOTES.md tenu.
Base : **c58b997** (ne diffère de 5e386c4 que par JOURNAL.md, README.md, README.fr.md). Corrige la série de `diffs-apres-sb15/` (noms SB-13A à SB-13D, SB-13E seulement si nécessaire), ≤ 200 lignes de code ajoutées par diff, plancher exact dans `gates.yml` à chaque diff.
À corriger (liste fermée) :
- C-1 : cas de `test_croiser_voit_les_ecarts` avec une unité absente de BTC, o altéré, écart `("o", r, u)` attendu ; tue M-G2-01.
- C-2 : au moins une entrée croisée à n′ < n_s (ex. sixième vecteur avec n_s = 109 440), sans écart attendu ; tue M-G2-02.
- C-3 : la ligne `oracle_recalc.py` au README de `scripts/sim-bis`.
- C-4 (O-2) : une part des séries synthétiques à 10 unités par classe, pour croiser S^(r) avec 8 écarts ou plus à une même position ; tue M-G2-13 par un test de `test_oracle_recalc.py` ; durée du test dite.
- C-5 (O-4) : le commentaire de `fetch-depth: 0` dans `gates.yml` nomme aussi SB-13.
- C-6 (O-1) : un test qui distingue l'`analyse.json` extrait au commit épinglé de celui de l'arbre de travail, pour tuer M-G2-12 ; si cela dépasse le lot ou 200 lignes, le dire et proposer l'item.
Questions : Q-SB13-1 à 5 adoptées ; Q-SB13-6 : pas d'extension, SHOGEN-S2BIS-HOTE-COMMUN-1 reste ouvert (« deux textes sur trois liés ») ; Q-SB13-7 : par C-3. E-6 (`git grep` borné) consigné ; plus aucun `git grep`. CONTRAT-RB6-1 fermé au commit après contre-contrôle ; ORACLE-RB7-1 ouvert.
Preuves : rouge d'assertion par test neuf ; les 17 mutants du réviseur rejoués (`g2/outils/`, lecture) avec M-G2-01, 02, 13 (et 12 si C-6) tués ; ≥ 2 mutants neufs par correction ; mode strict 3.10 à 3.13 × deux PYTHONHASHSEED en `-X dev -W error` ; runner, jobs s2bis, S2, sim-bis aux planchers exacts ; xtask (lignes de verdict seules) ; forme.
Rendu (valeur de retour), Gate 0 en tête : diffs (sha256, code ajouté, planchers), tableau C-1 à C-6 avec fichier:ligne et test, mutants, matrice, écarts ; aussi en section datée à la fin de `RAPPORT-GENERATEUR.md`, `SHA256SUMS` recalculé.
