# Contre-contrôle bref de RB-1l (remède de NC-1 ; transcrit)

> Transcription par l'orchestrateur le 2026-10-05, vers 22:41 UTC, du rapport rendu par message par le réviseur (agent afb8e4911502ce931) ; contrôle FM-1.1 : fragments_l51_l14 = 0. Texte du réviseur ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

**Gate 0** : modèle résolu `claude-opus-5-5` (préfixe conforme), réviseur `shogen-worker`, effort max. J'ai travaillé de 22:36:56 à 22:39:32 UTC le 2026-10-05, heures lues par `date -u`. Aucune écriture git dans le dépôt.

# Contre-contrôle de RB-1l (remède de NC-1) : CONFORME

Le diff et les sommes de corr3 sont vérifiés : `RB-1l.diff` 3ac6af25…aa0d, `SHA256SUMS` ab04216f…, aucun écart au contrôle. Ma copie est 47b2177, plus les 21 diffs, plus RB-1l (arbre `38f9fa35…`). Liste fermée : aucune correction.

1. **Cas F-1**, sous 3.10 et 3.12, K = 2000 et K = 20000 :
   - RB-1 et RB-18 rendent tous deux une queue en 145, de 4 016 et de 40 016 octets.
   - Avec l'outil du banc sur les mêmes journaux : 2 concordants sur 2 sous chaque version.
   - NC-1 est fermé.
2. **BOM.**
   - En ligne 2, RB-18 rend aussi la ligne non intègre, en queue (145, 148), comme RB-1 (`LECTEUR/json`).
   - L'octet 0xFF donne (145, 10) chez les deux. Un BOM en ligne 1 donne (0, 148) chez les deux.
   - Même résultat sous 3.10 et 3.12. Aucune discordance.
3. **Banc, familles c et d** (écrivain réel de l'état final, graine 18, py3.12) : 3 062 journaux (c 3 000, d 62), 3 062 concordants, 0 discordant. Les deux lecteurs refusent ensemble 39 journaux (absent/vide 16, nom/nom 23).
4. **Mutant, tests et forme.**
   - **M-1l-01** est tué, par la commande du job (borne 300 s, réseau isolé) :
     - témoin [0, 0], Ran 255 ;
     - mutant [0, 1], avec `test_octets_lus_en_utf8_strict` en échec.
   - **Tests** : le diff n'en retire ni n'en affaiblit aucun. Ses seules lignes retirées sont la docstring et l'appel `json.loads` de `lecteur.py`.
   - **Rouges du worker** relus : 4 échecs sous 3.10 et 3 sous 3.12, cohérents avec F-1 (le cas K = 2000 ne casse que sous 3.10). Le runner donne 87 ok.
   - **Forme** :
     - aucun octet 92 ajouté ; les deux du diff sont en lignes de contexte ;
     - fichiers finaux : `lecteur.py` 2 octets 92, `test_lecteur.py` 8, tous des `\n` ;
     - R-13 : 0 ; lignes `.py` toutes ≤ 120 caractères.

**Écart** : mon premier lancement de la génération passait par `sh -c` ; le contrôle de sécurité de l'outil l'a refusé et il n'a pas été exécuté. Je l'ai refait sans `sh -c`, avec un script écrit par Write qui ne supprime rien. Le `_tmp` du corpus est resté en place ; il est hors manifeste et le banc ne le lit pas.

**Journal G1.**
- Sources [lu] : RB-1l.diff (code et tests), `_integre` final (l.104-122), mutants de RB-1l, rouges du worker sous 3.10 et 3.12, runner.
- PID réels :
  - campagne : 5210, témoin [5211, 5227], mutant [5750, 5775] ;
  - banc sur le cas F-1 : [5327, 5328] sous 3.12 et [5343, 5344] sous 3.10 ;
  - banc c et d : [6433, 6707].
- Les copies lourdes sont supprimées (copie du dépôt, corpus, tmp). Le `SHA256SUMS` du premier contre-contrôle (`cc/`) reste vérifié : 38 entrées, toutes OK.

Fichiers dans `<scratchpad>/s2bis/rb18/cc2/` :
- `SHA256SUMS` : 12 entrées, contrôle OK, sha256 `3e1e7cf8f0512f8d4051df76fae1130e6b361f08dda69f74da120a02f6553bd3`
- `NOTES.md`
- `preuves/` : `sonde-f1.txt`, `banc-f1.txt`, `sonde-bom.txt`, `banc-cd.txt`, `banc-cd-generation.log`, `mutant-1l-01.txt`, `mutant-1l-01.log`, `forme.txt`
- `outils/` : `generer_cd.py`, `mutant_1l.py`, `sonde_bom.py`
