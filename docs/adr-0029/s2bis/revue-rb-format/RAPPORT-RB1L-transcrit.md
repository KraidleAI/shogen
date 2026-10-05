# Rapport du worker — RB-1l, correction de NC-1 du contre-contrôle de RB-1 (transcrit)

> Transcription par l'orchestrateur le 2026-10-05, vers 22:38 UTC, du rapport rendu par message par le worker (agent a1ccbf20eedaeb933) ; contrôle FM-1.1 : fragments_l51_l14 = 0. Texte du worker ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Rapport du worker : RB-1l, correction de NC-1 du contre-contrôle de RB-1

**Gate 0** : modèle `claude-opus-5-5`, fiche `shogen-worker`, effort max.
- Travail du 2026-10-05, de 22:26:46 à 22:36:02 UTC (`date -u`).
- Dépôt en lecture seule.

## Résumé

- **Base.** 47b2177 + les 21 diffs de `rebase-t5/diffs/` :
  - `SHA256SUMS` `2d2c7852…` vérifié, 21 fichiers OK ;
  - appliqués dans l'ordre de `rebaser_t5.py` : CB-19a à h, RB-1h à k, RB-18a à i ;
  - témoin du job sur cette base : classe 0, Ran 254.
- **Correction.** `_integre` décode la ligne en UTF-8 strict (`ligne.decode("utf-8")`) avant le compte des niveaux et avant le décodeur.
  - `_trop_profonde` compte sur `ligne`, c'est-à-dire l'UTF-8 de ce même texte. `json.loads` reçoit maintenant `texte`, et non plus les octets bruts.
  - Le compte et le décodeur lisent donc le même texte.
  - Une erreur de décodage rend la ligne non intègre, sous la cause `LECTEUR/utf8`.
  - Effet de bord : un BOM UTF-8 n'est plus retiré en silence ; la ligne devient non intègre (`LECTEUR/json`).
- **Test** : `Queues.test_octets_lus_en_utf8_strict`, avec quatre cas :
  - les deux lignes minimales de NC-1, en UTF-16-LE closes par 00 0A, K = 2 000 et K = 20 000 ;
  - un octet 0xFF ;
  - un BOM.
  - Chaque cas doit finir en queue à la position 145, derrière son `ouverture`.
  - Une RecursionError est rendue comme valeur, si bien que le rouge reste un échec d'assertion.
- **Rouge sur le code d'avant** (`preuves/rb1l-rouge-python3.1x.txt`), 0 erreur dans les deux cas :
  - sous 3.10 : 4 échecs. Les deux lignes de NC-1 donnent RecursionError, 0xFF est nommé `json`, le BOM est nommé `canonique` ;
  - sous 3.12 : 3 échecs. Le cas K = 2 000 y passe.
- **Vert.** `test_lecteur` passe sous 3.10 et 3.12 (Ran 32).
  - Ligne du job sous 3.10, 3.11, 3.12 et 3.13 : conforme, Ran = 255.
  - Runner : 87 ok.
- **Plancher** : 254 + 1 = **255** (`--egal`).
- **Mutants**, classés par la commande du job (runner, puis ligne `--plancher 255` ; borne 300 s ; python3.12 ; réseau isolé) : **6 tués sur 6**, chacun par son test visé ; 0 vivant, 0 FATAL.
  - M-1l-01 : `json.loads` rétabli sur les octets bruts (demandé par NC-1).
  - Cinq mutants neufs : décodage avec remplacement ; décodage en latin-1 ; `utf-8-sig` (BOM retiré) ; erreur de décodage non rattrapée ; cause de l'octet invalide mal nommée.
  - J'ai suivi votre consigne « au moins deux neufs » plutôt que le minimum de dix du brief, vu le budget et la taille du changement (8 lignes de code).
- **Diff** `corr3/diffs/RB-1l.diff`, sha256 `3ac6af25…aa0d` :
  - 37 lignes de code ajoutées ; section METRIQUES ajoutée en fin de fichier.
  - Fichiers finaux : `lecteur.py` 209 lignes (`0da699c2…`), `test_lecteur.py` 539 lignes (`a9b5766a…`).
- **Contrôles de forme.**
  - Octets 92 inchangés : `lecteur.py` 2, `test_lecteur.py` 8, `gates.yml` 4, METRIQUES 0. La barre est écrite `chr(92)` et le saut de ligne `bytes([10])`.
  - R-13 : 0. Toutes les lignes font au plus 120 caractères ; aucune espace en fin de ligne.
- **xtask** sur l'arbre complet (47b2177, les 21 diffs et RB-1l) : lignes de verdict identiques au témoin sans RB-1l. Seul S-G9 sur `docs/17:70` ressort, cas connu.

## Q-1 corrigée

Ma prémisse était fausse : « une RecursionError ne peut venir que de l'environnement ». NC-1 le montre :
- avec `json.loads` sur les octets bruts, le décodeur pouvait lire un autre texte que le compte (détection de l'UTF-16 ou de l'UTF-32) ;
- il plongeait alors dans des niveaux que le compte ne voyait pas.

Avec RB-1l, le compte et le décodeur lisent le même texte UTF-8, et une ligne comptée à 64 niveaux au plus n'y descend plus au-delà. Une RecursionError ne peut désormais venir que d'une pile d'appel déjà épuisée.

Le choix reste le même : l'exception remonte, sans verdict.

## Écarts

- **E-1.** Je n'ai pas ouvert les preuves du réviseur, rangées dans `rb18/cc/` : l'interdit du brief est maintenu. J'ai reproduit le cas d'après le texte adjugé de NC-1.
  - Les diffs RB-18 ont été appliqués mécaniquement ; leur code n'a pas été lu.
- **E-2.** Un `tail` de METRIQUES sur l'état recalé a affiché les titres des sections RB-18d à RB-18i et la fin de RB-18i. C'est un document partagé, hors de `rb18/` ; je n'en ai rien utilisé.
- **E-3.** Dans la section METRIQUES, le retour à la ligne coupe le code en ligne `` `--plancher 255` `` entre ses deux mots. C'est cosmétique.
- **E-4.** La tête du dépôt est maintenant 3576bef. Le brief fixait la base 47b2177 + 21 diffs ; je ne l'ai pas changée.

## Fichiers

Tout est dans `<scratchpad>/s2bis/rb1/corr3/` :
- `diffs/RB-1l.diff` ;
- `SHA256SUMS` : 27 lignes, contrôlé par `sha256sum -c`, sha256 `ab04216f…e55d` ;
- `NOTES.md` ;
- `outils/` : `tests_rb1l.py`, `code_rb1l.py`, `metriques_rb1l.py`, `mutants_rb1l.py`, `diff.py` ;
- `preuves/` :
  - rouges et verts : `rb1l-rouge-*.txt`, `rb1l-vert-*.txt` ;
  - campagne : `rb1l-mutants.txt` ;
  - job et runner : `job-python3.1x.txt`, `runner.txt` ;
  - xtask : `xtask-*` ;
  - comptes : `octets92.txt`, `RB-1l-comptes.txt` ;
  - témoin : `base-recale-job.txt` ;
- `travail/souche/test_lecteur.py` : les tests de la souche du rouge.

Copies lourdes supprimées : le dossier fait 496 Ko. Aucun processus à moi ne reste.
