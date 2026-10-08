# Brief — OUT-2, troisième tour : corrections C-1 à C-4 de la revue de la vague 2, et deux items de l'enregistreur

Worker `shogen-worker`, effort max. Mêmes règles, base (e6657dc), commandes et interdits que `<scratchpad>/s2bis/outillage2/BRIEF-OUT2.md` et `BRIEF-OUT2-CORR.md` (scratchpad = `<scratchpad>`). Tu écris dans `<scratchpad>/s2bis/outillage2/corr3/` (`TMPDIR` dédié, `NOTES.md`). Adjudication de l'orchestrateur, 2026-10-08 14:58:00 UTC.

## Pièces
- Diffs de la vague 2 : `<scratchpad>/s2bis/outillage2/corr/diffs/` (OUT-2a à OUT-2f) et rapport `corr/RAPPORT-CORRECTIONS-transcrit.md`.
- Revue de la vague 2 : `<scratchpad>/s2bis/outillage2/corr/REVUE-transcrit.md` (C-1 à C-4, O-1 à O-5, items 1 à 6) ; son remède `corr/revue/remede/remede-C1-C3.diff` est une donnée : tu écris et prouves toi-même.

## À faire (liste fermée)
1. **C-1, C-2, C-3** de la revue : tests seulement (I-01 sur chaque import qui suit la garde du runner ; I-04 sur `re`, `secrets`, `shutil`, `subprocess`, `tempfile` ; `.pyc` sans source à l'écriture et à la lecture). D02, D04, D11, F10 tués.
2. **C-4 : le vecteur est fermé, pas seulement décrit** (item neuf SHOGEN-S2BIS-SUITE-CODE-COMPILE-1, mesuré) : le vérificateur refuse, nommément et avant tout lancement, tout fichier compilé sous la racine de la suite (`.pyc`, `.pyo`, et tout suffixe de `importlib.machinery.EXTENSION_SUFFIXES`, `.so` nu compris) ; la règle `bytecode` de l'enregistreur s'étend aux mêmes suffixes, à l'écriture et à la lecture. Leurres LE-11, LE-13, LF-04 : refusés. Texte des l.30 et l.59 rendu vrai. Aucune racine actuelle n'est touchée (mesure-le).
3. **O-1 et O-2** : la limite d'AMORCE écrite au sens large (« un test qui altère unittest dans son processus, qu'il vise ce mécanisme ou non ») ; la docstring du vérificateur l.4-5 dit qu'il lance la suite par AMORCE.
4. **SHOGEN-S2BIS-ENREG-SUITE-COMPTE-1 (mesuré, LF-06) : fermé.** La commande `suite` de l'enregistreur passe par le même amorçage (ou par le vérificateur) : résumé forgé puis `os._exit(0)` refusé nommément, à l'écriture et à la lecture.
5. **SHOGEN-S2BIS-ENREG-DRAPEAUX-1 (mesuré) : fermé.** Les enfants `-I` de l'enregistreur reçoivent en ligne de commande les drapeaux que l'environnement consigné demande (`PYTHONDEVMODE` → `-X dev`, `PYTHONWARNINGS` → `-W …`), ou tout autre moyen motivé ; mesuré sous la matrice.
6. Ne pas toucher : la limite d'OUT-2f sur les enregistrements d'un outil antérieur (item 3 de la revue, à former) ; les limites écrites E-F3, N6', 3.9.

## Règles et rendu
Diffs en série après OUT-2f, chacun ≤ 200 lignes de code ajoutées (OUT-2b corrigé si C-3 y tient, sinon diffs neufs OUT-2g, OUT-2h…) ; tests d'abord, rouge d'assertion montré ; au moins 8 mutants par diff neuf ; planchers exacts (`CAS`, `PLANCHER`) ; matrice 3.10 à 3.13 ; leurres de R-1, de la G2 et de la revue : mêmes verdicts sauf ceux que ce tour doit faire refuser ; `gates.yml` reconnaissable par les trois motifs ; xtask : lignes de verdict seules. Rendu par message (ta valeur de retour), Gate 0 en tête ; écris-le aussi dans `corr3/RAPPORT-CORRECTIONS.md` et couvre-le par ton `SHA256SUMS`.
