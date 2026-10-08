# Rapport du worker — CC2-1, CC2-2 de P1 tranche C (transcrit)

> Transcription par l'orchestrateur le 2026-10-05 13:54:08 UTC du rapport rendu par message par le worker (agent aa9c3df62627c22da) ; contrôle FM-1.1 : fragments_l51_l14 = 0. Texte du worker ci-dessous, sans retouche.

**Gate 0** : le modèle résolu est `claude-opus-5-5` (préfixe conforme). L'effort `max` vient de la fiche ; je ne peux pas l'observer de l'intérieur.

## Résumé

1. **CC2-2 traité.** CB-18r, s et t sont régénérés sur la base recalée (5f99ab5 plus les 20 diffs neufs, 20 sur 20 OK au SHA256SUMS c80d92bc ; arbre complet 2d180042, comme annoncé).
   - Le code est identique à corr2, fichier par fichier.
   - Dans la section METRIQUES de r, la note E-7 est retirée : c'est la seule différence de contenu.
   - Les sections METRIQUES de s et t sont identiques mot pour mot ; seuls les en-têtes de hunk bougent.
   - r, s, t et u s'appliquent avec sortie 0 et 0 décalage.
2. **CC2-1 traité.** CB-18u est un diff distinct, posé après t, qui applique le remède adjugé tel quel :
   - `LIBRE = "[0-9A-Za-z].*"` sur les trois `name` ;
   - `    timeout-minutes: [1-9][0-9]*`.

   L-35 (LC-03), L-36 (LC-01) et G-02 (`timeout-minutes` entre guillemets) sont rouges sous le gabarit de t et verts avec le remède.
3. **Ajout hors des deux cas nommés : G-03 et G-04.** Ils contrôlent le gabarit seul, sur le nom du job et sur le nom de l'étape 3, chacun ouvert par un guillemet fermé à la dernière ligne du bloc.
   - Sans eux, M-18u-04 et M-18u-06 survivaient.
   - Ma conclusion intermédiaire disait que ces deux mutants étaient « équivalents ». Elle était fausse : ces textes sont du YAML valide pour le témoin PyYAML, le gabarit muté les admet, le remède les refuse.
   - Chaque cas est rouge sous le gabarit de t et sous son seul mutant. Résultat : u tue 6 mutants sur 6.
4. **Leurres rejoués sur l'état final, avec les outils du réviseur.**
   - Les fichiers régénérés sont identiques octet pour octet à `cc2/travail/leurres2` et à `cc2/travail/leurres`.
   - Classés par l'étape du runner : 38 tués, 6 vivants. Les vivants sont N-12, N-14, LC-02, LC-08, LC-09 et LC-10.
   - Cela s'écarte de la liste attendue dans ton message : LC-08 est admis et LC-13 est refusé (voir E-1).
5. **Vérifications sur l'état final** (copie 02c3baa5, extraite hors du dépôt, réseau isolé) :
   - job s2bis sous python3.10 à 3.13 : Ran 184, égal au plancher 184 avec `--egal` ;
   - S2 : Ran 406 ; sim-bis : Ran 129 ;
   - crochets : 54 ok ;
   - matrice `-X dev -W error` : 184 OK sous les quatre versions, 0 avertissement ;
   - test de l'enregistreur de rôle : OK sous les quatre versions ;
   - xtask : verdicts et violations égaux au témoin r0, lui-même égal au témoin de corr2. Seule violation : S-G9 `docs/17-modele-de-menace.md:70`, connue ;
   - R-13 : aucune occurrence ;
   - secrets : 4 fichiers en mode index, 782 en `--tree`, sortie 0 dans les deux cas.
6. **Dépôt et corr2.** Le dépôt est à HEAD 5f99ab5, `git status` vide, lu en `--no-optional-locks`. corr2 est intact : SHA256SUMS 359bb47d, 123 sur 123 OK. Le nettoyage est fait (base, w, etats, cible-cargo, `__pycache__`, `tmp/*`) et aucun processus du lot ne tourne.

## Diffs (`corr3/diffs/`)

Code compté hors `docs/` ; tous restent sous 200 lignes de code. Aucun octet 92 n'est ajouté.

| diff | code | docs | sha256 |
|---|---|---|---|
| CB-18r | +71 / −20 | +41 / −0 | 6fe1224f… |
| CB-18s | +10 / −4 | +30 / −0 | be99c282… |
| CB-18t | +13 / −1 | +38 / −13 | a67119f6… |
| CB-18u | +30 / −12 | +37 / −0 | a9b41286… |

`corr3/SHA256SUMS` : 1892debe…, 133 sur 133 OK.

**Arbres**

- Copie hors exclusions : fc307ffd, puis 1d7f9d54 après les 20 diffs, puis r 49db95af → s f1736538 → t 0b09cbae → u **02c3baa5**.
- Arbre complet : 2d180042 → r 0faf158e → s 6c24f32b → t e81e24a3 → u **176ab70e**.

## Mutants

Tous lancés par la commande du job, avec une borne de 300 s et python3.12 ; 0 FATAL.

| campagne | résultat |
|---|---|
| r | 8 tués sur 8 |
| s | 3 sur 3 |
| t | 4 sur 4 |
| u (état final) | 6 sur 6 |
| CA-01 à CA-12 du réviseur (état final) | 12 sur 12 |

## Écarts et décisions à prendre

- **E-1, à adjuger.** Ta liste attendue nomme LC-13 et omet LC-08 ; le résultat est l'inverse.
  - LC-08 (`timeout-minutes: 600`) passe, parce que `[1-9][0-9]*`, que tu as adjugé, l'admet.
  - LC-13 (ancre `&` et alias `*`) est refusé, ce qui est plus strict.
  - C'est exactement le résultat de la preuve du réviseur (`NOTES-CC2.md` l.14 et 21 : POC « LC-01/03/07/13 refusés », LC-08 « sans effet »).
  - Si tu veux LC-08 refusé, le serrage possible est `    timeout-minutes: 10` en littéral dans GABARIT, plus un cas G sur 600. Je ne l'ai pas fait, puisque l'adjudication fixe la regex.
- **E-2, à adjuger.** G-03 et G-04 vont au-delà de L-35 et L-36. Ils figent la règle « scalaire simple sur les trois lignes » et tuent M-18u-04 et M-18u-06. `sonde-equivalents-u.txt` reste dans les preuves comme trace de la conclusion abandonnée.
- **E-3, à savoir.** Les preuves de la racine de `preuves/` pour u, CA et les leurres (`campagne-*.txt`, `vert-CB-18u.txt`) ont tourné sur l'état intermédiaire ef307f3, à 75 cas. `preuves/final3/` les remplace. `rouge-CB-18u.txt` reste la preuve rouge de L-35, L-36 et G-02.
- **E-4, à savoir.** CB-18r ajoute une ligne de tableau METRIQUES de plus de 120 caractères. Plus de 20 lignes existantes du fichier dépassent déjà cette largeur ; cette ligne est inchangée depuis corr2.
- **Items non vérifiés.**
  - [abs] : la validité YAML côté forge (LC-01, G-03, G-04). Le témoin PyYAML n'a servi que hors du code.
  - [2nd] : « LC-09 et LC-10 échouent à l'exécution » est le classement du réviseur ; je ne l'ai pas rejoué.

## Journal G1

**Sources**

- [lu] Tes messages CC2-1, CC2-2 et la précision sur corr3.
- [lu] `cc2/travail/NOTES-CC2.md` (ef41dcf5), relu aux lignes 8 à 24.
- [lu] `poc-remede-lc03.diff` (28df4502) et `.txt` (938c58d4) ; `leurres2-runner-reel.txt` (0f6749b0) ; `mutants-E5-t.txt` (18a61280).
- [lu] Outils du réviseur, exécutés : `leurres_cc2.py` (60b63776) et `leurres_cc.py` (833d72b4).
- [lu] `rebase/diffs/SHA256SUMS` (c80d92bc) ; témoin xtask de corr2 (1dc77478) ; runner, vérificateur et gates.yml de la copie.

**Commandes et sorties**

- `date -u` : 13:36:34 à la reprise, 13:52:25 au nettoyage.
- `rouge_u2.py` → `rouge-G03-G04.txt` : code tel quel 77 ok ; gabarit de t 72 ok et 5 échecs ; M-18u-01 et 02 font échouer L-35, G-03, G-04 ; M-18u-03 G-02 ; M-18u-04 G-03 ; M-18u-05 L-35 ; M-18u-06 G-04.
- `sonde_g03_g04.py` : G-03 donne un YAML valide (runs-on None, 0 étape) ; G-04 aussi (étape 3 réduite à `name`) ; le gabarit refuse les deux.
- `verif_serie.sh` : 0 décalage partout ; arbres comme ci-dessus.
- `verif_finale3.sh` : PID réel 17829 (SID 17829, parent setsid 17827), de 13:44:53 à 13:51:52, ligne FIN présente.
- `r13.py` : motif sha256 ce8609f6… ; grep sortie 1 sur les 5 fichiers touchés ; contrôle positif : 1 ligne.
- `gate-secrets.sh` (clone jetable, HEAD r0, index = final) : sortie 0 en index et en `--tree`.

**Chiffres recomptés** : runner 289 lignes (`wc -l`), 77 cas « ok » ; lignes de code par diff (`compte_diffs.py`) ; 0 octet 92 ajouté.

Tout est dans `<scratchpad>/s2bis/cb18/corr3/` :
- `diffs/` : CB-18r.diff, CB-18s.diff, CB-18t.diff, CB-18u.diff
- SHA256SUMS
- NOTES.md
- fichiers-touches.txt
- `metriques/` : r.md, s.md, t.md, u.md
- `mutants/` : mutants_cb18r.py, mutants_cb18s.py, mutants_cb18t.py, mutants_cb18u.py, ca_reviseur.py, leurres_u.py
- leurres-cc-u/
- leurres-cc2-u/
- `outils/` : rouge_u2.py, sonde_g03_g04.py, verif_serie.sh, verif_finale3.sh, sommes.sh
- `preuves/final3/`
- `preuves/` : rouge-CB-18u.txt, rouge-G03-G04.txt, sonde-g03-g04.txt, verif-serie.txt, compte-diffs.txt, r13-final.txt, secrets-final.txt, leurres-cc-final.txt, leurres-cc2-final.txt
