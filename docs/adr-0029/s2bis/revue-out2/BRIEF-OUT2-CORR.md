# Brief — corrections d'OUT-2 (C-1 à C-3 de la G2) et trois items mesurés à fermer (OUT-2d, OUT-2e, OUT-2f)

Worker `shogen-worker`, effort max. Mêmes règles, base (e6657dc), interdits et commandes que `<scratchpad>/s2bis/outillage2/BRIEF-OUT2.md` (scratchpad = `<scratchpad>`). Tu écris dans `<scratchpad>/s2bis/outillage2/corr/` (`TMPDIR` dédié, `NOTES.md`).

## Pièces
- Les diffs du générateur `<scratchpad>/s2bis/outillage2/diffs/OUT-2a.diff`, `OUT-2b.diff`, `OUT-2c.diff` et son rapport `RAPPORT-OUT2-transcrit.md`.
- La relecture `<scratchpad>/s2bis/outillage2/G2-OUT2-transcrit.md` : corrections C-1 à C-3, items 1 à 4. Le remède proposé par le réviseur (`g2/preuves/remede/*.diff`) est une donnée : tu peux t'en inspirer, mais tu écris et tu prouves toi-même.

## Adjudication de l'orchestrateur
- Q-1 à Q-4 du générateur : tenus. E-7 : OUT-2c sans mutants, admis (texte seul ; le leurre E1 du réviseur en tient lieu).
- **C-1, C-2, C-3 : à corriger dans OUT-2b** (tests seulement ; le code produit est juste). Le diff OUT-2b corrigé remplace l'ancien ; rejoue ses campagnes en y ajoutant B4, C4 et C7.
- **Trois items mesurés, fermés dans ce lot** (« ne pas laisser de dette »), en diffs neufs, chacun ≤ 200 lignes de code ajoutées, appliqués après OUT-2c :
  1. **OUT-2d, SHOGEN-S2BIS-SCRIPT-MASQUE-1** [mesuré] : un `enforcement/subprocess.py` complaisant fait rendre « conforme » à la ligne s2bis sans lancer la suite ; un `enforcement/tests/json.py` fait sortir le runner en 0 sans jouer un cas ; un `enforcement/tests/secrets.py` annulerait le nonce. Les lignes du job, le serveur du runner et les commandes de production de l'enregistreur tournent sans isolement. Ferme toute la classe : lancement isolé (`-I`, ou forme équivalente motivée ; dis ce que `-I` (donc `-E`) change pour `PYTHONHASHSEED`, `PYTHONDEVMODE`, `PYTHONWARNINGS` et les drapeaux `-X dev -W error`, mesuré sous 3.10 à 3.13), et refus nommé de tout fichier masquant posé à côté des scripts de preuve si l'isolement ne suffit pas. Si tu changes des lignes de `.github/workflows/gates.yml`, garde-les reconnaissables par les motifs `verdict-suite-s2.py s2bis `, `^ *python3 -B enforcement/verdict-suite-s2.py( --egal)?$` et `verdict-suite-s2.py scripts/sim-bis ` ou dis exactement leur forme neuve.
  2. **OUT-2e, SHOGEN-S2BIS-SUITE-RESUME-FORGE-1** [mesuré] : un test qui écrit un résumé forgé puis appelle `os._exit(0)` obtient « conforme (Ran = 255) », alors que la suite a 2 tests réels dont un en FAIL. Le vérificateur ne doit plus croire le texte de la suite : par exemple un amorçage fourni par le vérificateur qui lance `unittest` et rend le vrai compte (lancés, échecs, erreurs, sautés) sur un canal séparé, avec un nonce, après la fin réelle du programme de test ; résumé absent, forgé ou en désaccord : refus nommé. Écris ton choix (Q-n) et sa limite.
  3. **OUT-2f, SHOGEN-S2BIS-MASQUES-LECTURE-1** [mesuré par le réviseur, E7] : un enregistrement `suite` écrit par l'outil de base sur une racine masquée est lu conforme par l'arbre relu. La lecture (`--verifier`) doit refuser, nommément, un enregistrement dont l'arbre porte un masque.
- Item de la limite sous 3.9 : `sys.stdlib_module_names` n'existe qu'à partir de 3.10 ; `s2-harness/README.md` annonce ≥ 3.9. Dis-le dans le texte (la version minimale réelle), sans élargir le lot.

## Règles
Tests d'abord, rouge d'assertion montré ; au moins 8 mutants par diff neuf, classés par la commande du job (runner, ligne s2bis, S2), borne 300 s ; planchers exacts recalés (`CAS` du runner, `PLANCHER` de S2, suite s2bis et sim-bis si elles changent, METRIQUES par diff si la suite s2bis change) ; matrice 3.10 à 3.13 en `-X dev -W error` ; leurres de R-1, de la G2 d'OUT-2 et les tiens : mêmes verdicts sauf ceux que le lot doit faire refuser ; R-13, R-8, octets 92, 120 caractères ; `cargo --locked xtask verify` : lignes de verdict seules.

## Rendu
Par message (ta valeur de retour), Gate 0 en tête : diffs finaux (OUT-2a, OUT-2b corrigé, OUT-2c, OUT-2d, OUT-2e, OUT-2f : sha256, lignes ajoutées), tableau C-1 à C-3, choix Q-n, leurres, mutants, matrice, planchers, écarts, items à former.
