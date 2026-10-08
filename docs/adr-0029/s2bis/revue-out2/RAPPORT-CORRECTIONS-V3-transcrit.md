# Rapport des corrections — OUT2, vague 3 (transcrit)

> Transcription par l'orchestrateur le 2026-10-08 17:39:28 UTC du rapport rendu par l'agent a3a8586c8cc52a289 (workflow wf_ae64f812-f4d) ; contrôle FM-1.1 : fragments_l51_l14 = 0 ; modèle résolu au transcript : claude-opus-5-5. Texte de l'agent ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

**Gate 0 : `claude-opus-5-5`** (identifiant tiré du contexte système ; l'effort `max` vient de la fiche, je ne peux pas le mesurer de l'intérieur). Horloge : de 14:58:27 à 16:42 UTC, le 2026-10-08.

**Verdict.** Les six points de la liste fermée sont tenus en quatre diffs neufs, OUT-2g à OUT-2j. 55 mutants sur 55 sont tués, sans FATAL ; la matrice 3.10 à 3.13 est verte hors le rouge connu PY310-1 ; `gates.yml` est inchangé et aucun cas ni test n'est retiré.

**Écart de base, à adjuger.** Pendant la passe, la tête du dépôt est passée de e6657dc à b46672b : 13 commits externes PLAN-S2BIS-2, le dernier à 16:11:59 UTC.
- Je n'ai fait aucune écriture git. Le statut est vide et `.git/HEAD` est inchangé. `.git/index` a changé du fait de ces commits.
- Les fichiers du contrat sont identiques entre les deux têtes (`git diff --stat` vide sur `enforcement`, `s2-harness`, `gates.yml`, `s2bis` et `scripts/sim-bis`) : les diffs s'appliquent tels quels.
- Les diffs restent bâtis sur e6657dc, la base du brief ; je n'ai pas avancé la base.

## Diffs (série après OUT-2f ; OUT-2a à OUT-2f inchangés)

La série base, puis OUT-2a à OUT-2j par `patch -p1 -F0`, redonne l'arbre final entier.

| Diff | Objet | Ajoutées / retirées | sha256 |
|---|---|---|---|
| OUT-2g | C-1 à C-3, tests seuls | 50 / 27 | `0c6ca1e6fa9520f6c595aea99d95917f7242fa0ad924f3aaf671f6c9712ce765` |
| OUT-2h | C-4, O-1, O-2 | 160 / 38 | `640c3d7d88ff9f240d9fe5cc5e7daed4c4d0488a88f1a850aa84f20653a17184` |
| OUT-2i | ENREG-SUITE-COMPTE-1 | 142 / 21 | `96094e91e4f8a8a88524f0977b186368e0035bbd99b380f7b2cfaaad6960ea4d` |
| OUT-2j | ENREG-DRAPEAUX-1 | 48 / 10 | `9b41f9d10815e4f361fb3411970252ebe92a7f659e0d2b2950871688a8b8648e` |

C-3 ne tient pas dans OUT-2b : ses tests sont nés dans OUT-2d et OUT-2f, d'où des diffs neufs.

## Ce que fait chaque point

- **C-1** : I-01 pose son corps sous chacun des 11 imports qui suivent la garde du runner. Sur l'état g, D02 donne « ÉCHEC I-01 » ; avec les anciens tests, il survit.
- **C-2** : I-04 pose un module marqué et transparent sous re, secrets, shutil, subprocess et tempfile (et importlib/ dans OUT-2h). D04 donne « ÉCHEC I-04 ».
- **C-3** : un `.pyc` sans source est maintenant testé à l'écriture et à la lecture. D11 donne 3 FAIL, F10 en donne 1, tous « ValueError not raised ».
- **C-4, le vecteur est fermé** :
  - le vérificateur refuse, nommément et avant tout lancement, tout fichier compilé sous la racine de la suite : `.pyc`, `.pyo`, `.so` nu, `.pyd` et les suffixes de `EXTENSION_SUFFIXES` ;
  - il suit les liens de dossiers et lit chaque dossier une seule fois ;
  - l'enregistreur applique la même règle, à l'écriture comme à la lecture ;
  - LE-11, LE-13 et LF-04 sont refusés, et les l.30 et l.59 sont réécrites pour être vraies ;
  - aucune racine actuelle n'est touchée : 0 fichier compilé et 0 lien sous s2-harness, s2bis et sim-bis, 0 fichier compilé sur les 872 fichiers de l'arbre, mesuré avant et après la matrice.
- **O-1 et O-2** : la limite d'AMORCE est écrite au sens large, et la docstring dit que la suite est lancée par AMORCE.
- **ENREG-SUITE-COMPTE-1 (LF-06)** : `suite` passe par AMORCE du vérificateur de l'outil.
  - Un run sorti en 0 est jugé sur le compte réel.
  - Pour LF-06, l'écriture rend le code 1 avec exit 1 consigné, et la dernière ligne de sortie nomme le motif : « [oracle_record] compte réel absent … — exit 1 ».
  - La lecture refuse (exit) et cite ce motif.
- **ENREG-DRAPEAUX-1** : sous la matrice, l'enfant `-I` voyait « False [] » ; il voit maintenant « True ['default', 'error'] », comme la référence lancée sans `-I`, de 3.10 à 3.13.

**Rouges d'assertion montrés, tous en FAIL, aucun en ERROR** : 9 pour OUT-2i, 5 pour OUT-2j. Pour OUT-2h, sur un bouchon : 12 échecs au runner et 10 FAIL en S2.

## Choix

- **Q-9 (OUT-2g)** : I-04 est compté sans rien lancer dans une copie, comme I-01 à I-03.
- **Q-10 (OUT-2h)** :
  - j'ai ajouté `.pyd` au-delà du brief (serrage), pour qu'un arbre soit jugé pareil quelle que soit la plateforme ;
  - `sys.pycache_prefix` est gardé et épinglé par un cas neuf, F-15 ;
  - coût en local : un `__pycache__` laissé par un lancement sans `-B` est refusé, en le nommant. Les jobs lancent la suite en `-B`.
- **Q-11 (OUT-2i)** : « même amorçage », et non « par le vérificateur ». Le vérificateur retire la variable scellée, alors que le rôle « rendu » en a besoin.
- **Q-12 (OUT-2j)** : les drapeaux viennent de l'environnement, comme pour `suite` : `-X dev` si PYTHONDEVMODE n'est pas vide, un `-W` par filtre de PYTHONWARNINGS.

## Leurres (état f, puis état final)

- **Inchangés** : R-1 côté runner et côté enregistreur, G2 nonce N0 à N6, G2 enregistreur E1a à E7, G2 masque de 3.10 à 3.13, LD, LE-01 à LE-10, LE-12, LE-14, et les leurres D et E du correcteur.
- **Ceux que ce tour devait faire refuser le sont** : LE-11 et LE-13 passent de 0 à 1 ; LF-04 et LF-06 sont refusés.
- **Deux sorties restent conformes, au titre de limites** : LF-06 écrit par l'ancien outil et lu par le nouveau reste conforme (item 2 ci-dessous). N6', le leurre adapté par le correcteur (hors liste du brief), passe de 0 à 1 parce qu'il n'imite pas le motif neuf ; la limite « lit les requêtes » reste vraie (D6a et D-CAPTURE sortent en 0).

## Mutants, matrice, planchers

- **Mutants** (3.12, borne 300 s, classés runner, puis s2bis, S2, sim-bis) :

| Diff | Tués / total | Tués par | Vivants | FATAL |
|---|---|---|---|---|
| OUT-2g | 12 / 12 | runner 9, S2 3 | 0 | 0 |
| OUT-2h | 18 / 18 | runner 15, S2 3 | 0 | 0 |
| OUT-2i | 15 / 15 | S2 | 0 | 0 |
| OUT-2j | 10 / 10 | S2 | 0 | 0 |

- **Matrice** : 136 ok, 255, 172 sous 3.10 à 3.13 ; S2 Ran = 415, conforme sous 3.11 à 3.13. Sous 3.10, le rouge PY310-1 garde les mêmes 80 noms qu'à la base, et les tests neufs passent. Aucune ligne « Exception ignored » ni « Warning ».
- **Planchers** : `CAS` va de 123 à 136, `PLANCHER` de 413 à 414 puis 415 ; s2bis et sim-bis sont inchangés, donc pas de section METRIQUES.
- **Forme** : aucune ligne de plus de 120 caractères, aucun marqueur R-13, bibliothèque standard seule. Les octets 92 par fichier sont inchangés.
- **xtask** : S-G1 à S-G8 VERT ; S-G9 ROUGE sur sa seule violation connue (`docs/17-modele-de-menace.md:70`) ; fmt, no_std et clippy VERT ; verdict global ROUGE, connu.

## Écarts

- **E-2** : la matrice a montré R-09 en échec sous 3.13. Le leurre `re.py` que j'avais ajouté en C-2 l'a révélé : sous 3.13, l'affichage d'une exception levée avant la garde importe `re` depuis le dossier du script. Je l'ai corrigé dans OUT-2g et j'ai tout rejoué.
- **E-3** : deux passes finales ont été arrêtées ; seule la troisième compte.
- **E-5** : le rouge d'OUT-2h est montré sur un bouchon, la forme admise au tour précédent.
- **E-8** : une commande a passé une barre oblique inverse (`xargs -d`). Le résultat a été contrôlé sur les octets, puis `SHA256SUMS` a été réécrit par un script Python.

## Items à former

1. Inscrire en annexe les trois items fermés par ce lot.
2. Un enregistrement `suite` écrit par un outil d'avant OUT-2i n'est pas rejugé à la lecture (même classe que l'item 3 de la revue). Le rejeter est une décision.
3. Limites d'OUT-2h : du code compilé chargé autrement n'est pas vu (écrit pendant le run, archive zip, dossier hors racine ajouté à `sys.path`). Un lien vers un très grand dossier allonge la lecture. Sous Windows sans droit de créer des liens, le runner échoue (échec fermé).
4. Limites d'OUT-2j : PYTHONHASHSEED est consigné mais n'a pas de drapeau équivalent. Les autres variables à drapeau ne sont pas rendues : PYTHONUTF8, PYTHONOPTIMIZE, etc.
5. Sous 3.13, une exception levée avant la garde d'un script importe `re` depuis le dossier du script. Règle pour tout futur script de preuve : la garde passe en tête.
6. `tools/README.md` ne dit pas que VERIF juge aussi `suite` ; je ne l'ai pas modifié, car c'est hors de la liste fermée.
7. Avec le leurre fork LE-05, un dossier temporaire peut rester ; le verdict n'est pas touché.
8. Restent visibles, sans changement : la limite d'OUT-2f, E-F3, N6', la limite sous 3.9 et PY310-1.

Interdits respectés : aucune pièce de D.2, aucun `*.jsonl`, aucun dossier interdit, la variable scellée jamais posée, rien sur Pocket. Les copies lourdes sont supprimées et aucun processus ne reste.

`SHA256SUMS` compte 333 entrées, vérifiées, et couvre le rapport ; son sha256 est `308c6b1a7e63892109fbae53b610f1082e8bad136480e26be3731a02ed292e60`. Le rapport a pour sha256 `42b73a1281ce2716ebea4b1b99dafe386e8e4d4bc62afcd7e8fad6f5cffa0cbc`.

Fichiers, dans `<scratchpad>/s2bis/outillage2/corr3/` :
- `RAPPORT-CORRECTIONS.md`
- `SHA256SUMS`
- `NOTES.md`
- `diffs/OUT-2g.diff`, `diffs/OUT-2h.diff`, `diffs/OUT-2i.diff`, `diffs/OUT-2j.diff`
- `livrables/`
- `preuves/` (dont `mutants/`, `leurres/`, `matrice/`, `rouge/`, `xtask/verdicts.txt`, `journaux/`)
- `outils/`
