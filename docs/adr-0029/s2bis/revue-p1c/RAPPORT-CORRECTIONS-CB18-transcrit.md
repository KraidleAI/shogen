**Gate 0 : modèle résolu `claude-opus-5-5`.** La fiche demande l'effort max ; l'effort réel ne se voit pas de l'intérieur.

# Rapport du worker : corrections de la G2 de P1 tranche C (CB-18), puis ajout des lettres C-1 à C-5 du FORMAT

Date : 2026-10-05, horloge lue à 11:13:13 UTC.

**Base.** 3164348 (copie par git archive, avec les exclusions du brief), plus les 9 diffs de CB-18 (SHA256SUMS du worker vérifié). Arbre obtenu : e9 = 479ece28, reconstruit à l'identique depuis la base.

**Dépôt.** Je n'ai fait aucune écriture git dans /home/user/shogen : seulement `git --no-optional-locks` show, archive, diff et log.

**Tête du dépôt.** f5915a5 au début, **72aa806 à 11:06 UTC**. Le changement vient d'un autre lot (commits SIM-BIS SB-4i à SB-7a), qui a aussi 6 chemins indexés ; rien n'est de moi. Les conséquences pour le recalage sont au §7.

## 1. Résumé point par point

### Corrections du brief (liste fermée), diffs CB-18g à CB-18m

1. **C-1 budget (g).** `tolerance` est scellée dans formes.json. La règle devient tolérance + décalage + délai + marge ≤ δ, égalité admise (FORMAT §14.1, §14.4). La sonde du réviseur, rejouée, refuse désormais 14 et 15 s. MR-17 est tué.
2. **CONFIG-REGLES-1 (h).** Trois règles nommées : places-formes, hote-forme `[a-z0-9.-]{1,253}`, chemin-forme. Les tests à la borne tuent MR-18 et MR-22.
3. **Tests seuls (i).**
   - TEST-DISQUE-INSTABLE-1 : statvfs injecté.
   - SEGMENTS-10-1 : onze segments d'un même jour ; tue MR-26.
   - Tuple : MR-09 est tué, donc aucune justification n'est nécessaire.
4. **(j).**
   - Convention « ADR-0029 l.N » (commit e16956b) écrite dans l'en-tête du FORMAT.
   - `run_params` placé dans l'ordre de la fenêtre (§11.5).
   - METRIQUES, C-3 : boucle.py recomptée.
5. **C-2 ENREG-ROLE (k).** La ligne s2bis n'est lue que dans le job qui la suit. Le rouge MR-24 est montré.
6. **LIGNE-JOB-LEURRE-1 (l).**
   - Un analyseur unique (`etapes`, `lignes_du_job`) dans enforcement/verdict-suite-s2.py, partagé par K-01 à K-03 et par l'enregistreur.
   - Clés de premier niveau fermées.
   - Leurres C1 et C4 refusés.
   - Le runner passe de 33 à 57 cas.
7. **--egal sur le job S2 (m).** La ligne est `python3 -B enforcement/verdict-suite-s2.py --egal` (Ran = PLANCHER = 406). K-01 l'exige, et le cas L-22 refuse la même ligne sans `--egal`. Le couplage avec B-SEG-1 est vérifié : les tests sautés comptent dans Ran. MR-25 est tué.
8. **C-4 (biblio)** revient à l'orchestrateur ; aucun diff.

### Ajout : lettres du FORMAT (avis 6daf4065, adjudication e6528325), diffs CB-18n à CB-18q

9. **C-4 (n) : imbrication.**
   - N = 64, racine au niveau 1.
   - Refus `JOURNAL/imbrication` avant le sérialiseur, dans le même parcours que les entiers. Ce parcours devient postfixe, avec la hauteur retenue par conteneur : un conteneur partagé ne fait pas exploser le parcours, et un cycle reste `JOURNAL/type`.
   - `_lire` passant par `canonique`, une ligne de 65 niveaux est une queue en 3.10 comme en 3.12.
   - Profondeur réelle mesurée au bout en bout : **M = 4** (`run_params`, `formes.formes[i]`). Elle est écrite au §8.3 avec le seuil de 988 (3.10) et la mention « mesuré en 3.10 et 3.12 seulement ».
10. **C-1 et C-2 (o) : définition unique d'« intègre ».**
    - Le §7.1 reprend mot pour mot la lettre (a) à (e) de l'avis et la suite (« Un booléen JSON n'est jamais un entier… aucun des trois ne la relâche »). Les limites déclarées de CB-18f sont retirées.
    - `_lire` est aligné via `_types`, qui compare `type(v)`, jamais `isinstance` :
      - `type` chaîne, `seq` entier, `prec` `[0-9a-f]{64}` ;
      - champs propres de chaque type réservé présents et typés ;
      - `ws` entier et requis pour tout type non réservé.
    - C-1 : §1.2 gardé tel quel ; la borne des 640 chiffres entre au point (b) ; le code reste `JOURNAL/entier`.
    - **R-2, vérifié type par type** : aucun type n'a de `ws` null. `ouvrir`, `ecrire` et `marqueur` refusent tout `ws` non entier, booléen compris ; `point` recopie celui de son marqueur ; `run_params` passe par `ecrire`. C'est écrit au §7.1, et le test de bout en bout vérifie que la reprise du second démarrage ne déclare aucune queue.
    - test_format §7.1 réécrit : il vérifie le texte, puis que `_lire` le fait, champ par champ et type par type.
11. **C-3 (p) : ordre de la liste `queue`.**
    - Le §7.4 porte la lettre du réviseur, les deux précisions de l'avis (ordre croissant (jour, k) ; l'écrivain écrit dans cet ordre) et le classement : seules comptent comme déclarées les `reprise` intègres, au lien juste, à déclaration exacte.
    - **R-1** : le code écrivait déjà dans cet ordre (`insert(0)` en relisant du plus récent au plus ancien) ; aucun code ne change.
    - Test neuf de deux pannes réelles : disque plein sur une lecture du 4, puis sur la `reprise` du segment neuf du 5. La reprise suivante déclare [04-0, 05-0]. Rouge montré sous le mutant `append`.
12. **C-5 (q) : grammaire des noms.**
    - `_fichiers` suit `(0|[1-9][0-9]*)`.
    - À l'ouverture, un nom `<préfixe>-….jsonl` hors grammaire est refusé (`JOURNAL/nom`) : rien n'est écrit, le verrou est rendu.
    - À la bascule, un tel nom est ignoré, parce que le refuser là écrirait la `cloture` avant le refus ; le redémarrage suivant le refuse.
    - Pas de numéro sur 3 chiffres.
    - FORMAT : §5 ; §6.1 (lettre) ; §7.7 (lettre des lecteurs, dont le dossier sans fichier du journal = refus nommé).
    - Le test des onze segments sert de test à 10 segments ou plus ; MR-26 est porté en M-18q-02 et tué.
13. **Banc RB-1 et journaux d'exemple de RB-18** rejoués contre l'écrivain corrigé (§6). Je n'ai pas modifié les lecteurs RB-1 ni RB-18.

## 2. Diffs

La série s'applique sur 3164348 + les 9 diffs. e9 + 11 diffs → arbre **199454e1** (état final), sans décalage ni flou.

| diff | code +/− | docs +/− | plancher s2bis | sha256 |
|---|---|---|---|---|
| CB-18g | +30/−9 | +31/−9 | 134 | 90338aea… |
| CB-18h | +38/−4 | +27/−4 | 135 | 98a2c4e8… |
| CB-18i | +41/−9 | +30/−6 | 136 | 1a311fc7… |
| CB-18j | +17/−2 | +33/−4 | 137 | 1c354a5a… |
| CB-18k | +15/−11 | +14/−0 | 137 | aa80a88a… |
| CB-18l | +180/−37 | +34/−0 | 137 | 8b7f15ed… |
| CB-18m | +19/−8 | +18/−0 | 137 (S2 : --egal, 406) | d227685b… |
| CB-18n | +78/−22 | +41/−4 | 139 | b8da19c9… |
| CB-18o | +70/−38 | +56/−10 | 139 | 515545a0… |
| CB-18p | +27/−1 | +31/−2 | 140 | 693887ed… |
| CB-18q | +42/−10 | +47/−12 | 141 | b935b6d7… |

- Tous les diffs restent ≤ 200 lignes de code ajoutées ; le plus gros est CB-18l (180).
- Octets 92 ajoutés : 0 partout.
- Lignes ajoutées de plus de 120 caractères : seulement des lignes de tableaux METRIQUES (g 1, n 2, o 1, q 1), dans le style déjà en place.
- Les sections METRIQUES de g à q sont incluses dans les diffs.

## 3. Mutants

Classés par la commande du job, borne de 300 s, python3.12, réseau isolé ; sortie 1 = tué, 0 = vivant, autre = FATAL.

- **Réviseur, MR-01 à MR-26 : tous tués.**
  - MR-24 : rouge montré sur l'état k, puis porté en MR-24' dans la campagne l.
  - Les 25 autres et MR-12b : 26/26 sur l'état de fin des corrections.
  - Rejoués sur le code final de l'ajout : 23/23. MR-08, MR-09 et MR-26, dont les lignes visées ont changé, sont portés en M-18n-07, M-18n-06 et M-18q-02, tous tués.
- **Échantillon de 20 de mes mutants de CB-18** (Random(20261005)) : 20/20 tués.
- **Mutants neufs : 93, tous tués au dernier passage, 0 FATAL.**
  - Par diff : g 6, h 10, i 4, j 4, k 2 (dont MR-24), l 25, m 4, n 7, o 20, p 2, q 9.
  - Les 25 de l comprennent 5 leurres neufs contre l'analyseur.
- **Passages non comptés :**
  - l, premier passage : 2 vivants ; L-12 et L-14 réécrits. Puis un trou trouvé dans l'analyseur (`env :` de premier niveau) ; clés de premier niveau fermées, campagne refaite.
  - o, premier passage : M-18o-19 vivant (`point` retiré des types réservés), parce que le test des refus ne couvrait que `marqueur`. Le test couvre maintenant les six types réservés.
  - Les passages interrompus par le redémarrage du conteneur ont été refaits.

## 4. Vérifications sur l'état final (199454e1)

| contrôle | résultat |
|---|---|
| job s2bis, python3.10 à 3.13 | VIVANT, Ran 141 = plancher |
| job S2 | Ran 406, `--egal` |
| job sim-bis | Ran 93 |
| crochets | 54 ok |
| suite s2bis en `-X dev -W error`, 3.10 à 3.13 | 141 OK, 0 avertissement |
| test du rôle, 4 versions | OK |
| xtask | S-G1 à S-G8 VERT ; fmt, no_std, clippy VERT ; S-G9 ROUGE, `docs/17-modele-de-menace.md:70` seul (connu), identique au témoin e9 |
| R-13 | 0 occurrence sur les 16 fichiers touchés (motif lu dans gates.yml) ; contrôle positif 1 |
| secrets | mode index : 15 fichiers OK ; `--tree` : 747 OK |
| contournement de rôle (outil du réviseur, copie avec `shell: bash`) | C1 à C6 refusés ; C7 enregistré en échec ; enforcement/, s2-harness/ et scripts/ identiques de m à l'état final |

## 5. Rouges de l'ajout

- `rouge-CB-18n.txt` : 3 échecs.
- `rouge-CB-18o.txt` (texte du §7.1) et `rouge-CB-18o-code.txt` (code d'avant : 10 sous-tests, plus les sondes `type` et `prec`).
- `rouge-CB-18o-r2-bout-en-bout.txt`, `rouge-CB-18o-reserves.txt`.
- `rouge-CB-18p-R1.txt`, `rouge-CB-18q.txt`.
- Mesure de M : `sonde-profondeur-e2e.txt`.

## 6. Banc RB-1 et journaux d'exemple, contre l'écrivain corrigé

Le lecteur RB-1 est celui de f5915a5 (lecteur.py 27d6adf6), non modifié.

**Banc original** (banc_lecteur.py 2e320fd1) : C1 à C4 ok, puis arrêt à C5. L'écrivain refuse désormais 10**700 (`JOURNAL/entier`), ce qui est attendu depuis I-1.

**Copie ajustée** (seul C5 change ; `banc-lecteur-ajuste.diff`), même résultat en 3.12 et en 3.10 :
- C1 à C10 : ok.
- Propriété sur 300 graines : aucun écart (270 journaux, 1 345 redémarrages, 1 140 queues déclarées).
- Différentiel : **12 écarts sur 3 000 altérations**. Ils sont tous du même type : l'écrivain est plus strict au point (c), sur un `prec` mal formé en première ligne. C'est la classe E04c de la lettre C-2 ; la correction de RB-1 doit la fermer.

**Exemples E01 à E11** (14 journaux) : l'écrivain classe chaque cas comme la lettre le dit.
- E01 : queue au point (b), `JOURNAL/entier`.
- E03 : refus `JOURNAL/nom`.
- E04a, E04b, E04c : non intègres au point (c).
- E05 : non intègre au point (d).
- E10 : queue au point (b). En 3.12 la cause est l'imbrication, en 3.10 RecursionError ; la position est la même.
- E06, E07, E08, E09 : lignes intègres ; C-3 relève des lecteurs.
- E11 : la reprise dont la queue est un objet nu est non intègre au point (d).
- E02 (dossier vide) : l'écrivain ouvre un journal neuf. Le refus nommé du dossier vide est une règle des lecteurs.

## 7. Recalage sur la tête 72aa806

Entre 3164348 et 72aa806, seuls deux fichiers de la série ont changé :
- METRIQUES : sections RB ajoutées en fin de fichier ;
- gates.yml : plancher s2bis 156 et plancher sim-bis 108.

Ces deux fichiers mis à part, les 20 diffs (9 + 11) s'appliquent sans décalage sur 72aa806. J'ai essayé un gates.yml recalé : celui de la série, avec s2bis à 183 (156 + 27) et sim-bis à 108. Avec ce fichier, les trois jobs passent par leur commande : s2bis Ran 183, sim-bis 108, S2 406. La suite s2bis en `-X dev -W error` 3.12 donne 183 OK, tests du lecteur RB-1 compris. Pour le commit : plancher s2bis 183, et sections METRIQUES de la série à placer après les sections RB.

## 8. Écarts

- **E-1.** Le conteneur a redémarré. Les passages de campagne interrompus ont été archivés, non comptés, puis refaits.
- **E-2.** Les journaux d'exemple sont des `*.jsonl`, que le brief interdit ; c'est votre ajout qui demande de les rejouer. Ils n'ont été lus que par programme (écrivain, outil `rejeu_exemples.py`). Je n'en ai affiché aucun contenu, seulement des comptes, positions, codes et empreintes (empreinte de l'ensemble : 3a745610).
- **E-3.** Le banc tourne sur une copie ajustée, seul C5 changé, parce que l'original s'arrête à C5 depuis I-1. L'exécution de l'original est aussi consignée.
- **E-4.** Le premier lancement du banc a échoué (`/usr/bin/time` absent, sortie 127) ; il a été relancé et ne compte pas.
- **E-5.** L'assertion R-2 du test de bout en bout (aucune queue) fait double emploi avec la vérification de chaîne de `chaine`, qui échoue d'abord sous la sonde. Je l'ai gardée parce que c'est la parade explicite de l'avis.
- **E-6.** Les états des campagnes o2, p2 et q2 diffèrent de la série finale par les METRIQUES et par un seul commentaire, retiré pour ne pas ajouter d'octet 92. Différence vérifiée ; les résultats de mutation valent pour la série finale.
- **E-7.** `git checkout` n'a servi que dans le dépôt jetable w, jamais dans /home/user/shogen.
- **E-8.** Deux horodatages de mes notes avaient été écrits sans lire l'horloge ; corrigés dans les notes.

## 9. Pour l'orchestrateur

**Phrase à ajouter à SHOGEN-S2BIS-RUPTURE-PORTEE-1** (B.65, absent de 3164348), texte de l'avis l.78 :
« Une `reprise` au lien rompu ou à déclaration fausse est une rupture **non déclarée** ; sa déclaration n'est pas lue ; toutes les queues en attente sont rendues avec elle. Ne comptent comme reprises déclarées que les `reprise` intègres, au lien juste, à déclaration exacte. »

**Observations à adjuger** (aucune n'est écrite dans les diffs, lettres gardées exactes) :
- **O-1.** Le cas « objet nu » de C-3 n'est jamais atteint : le point (d) de C-2 (`queue` liste ou null) rend déjà la ligne non intègre. Une telle ligne devient donc une queue non déclarée, et non une déclaration fausse. Les lecteurs doivent appliquer le §7.1 avant le §7.4. Je propose d'ajouter au §7.4 une incise « (un objet nu rend déjà la ligne non intègre, §7.1 d) ».
- **O-2.** Collision de préfixes : un journal `pool-x` dans le même dossier ferait refuser `pool` (`JOURNAL/nom`). Sans effet en S2-bis, puisque le point d'entrée fixe `pool` et un dossier par journal. Item proposé : SHOGEN-S2BIS-PREFIXE-NOM-1.
- **O-3.** Le §7.4 cite SHOGEN-S2BIS-RUPTURE-PORTEE-1, et l'en-tête cite l'item proposé SHOGEN-S2BIS-LIRE-BOOLEENS-1 comme « sans objet ». Ni l'un ni l'autre n'est inscrit à l'annexe B de la base 3164348.

**Items du brief :**
- Restent ouverts : RUNPARAMS-CALENDRIER-1, ECRIVAIN-REFUS-ARRET-1, SIGTERM sans `finally` (DB-3), PY310-1.
- LIRE-BOOLEENS est fermé côté écrivain par CB-18o ; les lecteurs suivront la lettre.
- Le nom de segment sur 3 chiffres est écarté par C-5.

**Items proposés :**
- SHOGEN-S2BIS-HOTE-COMMUN-1 : règle d'hôte commune à la collecte et au recalcul, avec un test d'égalité au recalage.
- SHOGEN-S2BIS-ENREG-FORME-JOB-1 : l'enregistreur exclut sans exiger la forme K.
- SHOGEN-S2BIS-ANALYSEUR-RESIDUS-1 : YAML non modélisé (ancres, `with:` du checkout, validité du workflow).
- SHOGEN-S2BIS-TOLERANCE-D2-1 : tolérance scellée = seuil D-2 du recalcul.
- Q-3 : l'`env` d'une étape est incompatible avec la forme fermée.

**Fermetures à prononcer** (acte de l'orchestrateur) : CONFIG-REGLES-1, SEGMENTS-10-1, TEST-DISQUE-INSTABLE-1, LIGNE-JOB-LEURRE-1, CITATIONS-ADR-DECALEES-1, et N-1 de la G2 de RB-18 (SHOGEN-S2BIS-IMBRICATION-SEUIL-1), côté écrivain.

**Banc à verser (N-3)** : son cas C5 est à mettre à jour (voir la copie ajustée).

## 10. Journal G1 (provenance)

**[lu]**, avec empreinte et portée :
- brief bfca4aff (en entier) ; AVIS-FORMAT 6daf4065 (en entier) ; ADJUDICATION-FORMAT e6528325 (en entier) ; G2-RB18-transcrit 1ddabaee (l.68-202, puis l.194-202 relues).
- banc_lecteur.py 2e320fd1 (en entier) ; exemples : INDEX.txt 4d01dd1f et noms de fichiers.
- G2-CB18 transcrit ce9e2a11 ; RAPPORT-WORKER transcrit ea24dd5e ; NOTES du réviseur fe0b92bb ; BRIEF-CB18 17e03a1a ; outils du réviseur (mutants_g2 2f529209, campagne_g2 71c25a2f, jobg2 ba6f1f3d, sonde_budget 83e5f98e, contournement_role f69de729, echantillon bea73819) ; SHA256SUMS du worker 3641e431.
- G0 COLLECTE fe57eeb1 ; FORMAT et METRIQUES de la série (en entier, et l.330-649) ; ADR-0029 à e16956b (l.100-112, 225-250) ; G2-P1A l.285-312 ; ANNEXE-B, B.60 et grep des trois noms d'items (0 résultat dans la base) ; ANNEXE-D l.32-48 (liste D.2 seule) ; G1-lot-DETTES-B1 l.212-232.
- Code et tests du collecteur touchés ; à 72aa806 : test_lecteur.py 2c1c1378 (l.1-120), diff de test_fitness 5a10a3a1 et de gates.yml, noms de fichiers des commits.

**[abs]** : lecteur.py et contre-épreuve de RB-18 (seulement importés par le banc ; seules les lignes d'import ont été lues), PROPOSITION, pièces D.2, tout `*.jsonl` hors traitement par programme des exemples, dossiers exclus. **[2nd]** : aucun chiffre.

**Commandes et sorties** : chaque sortie est dans un fichier de preuves (`preuves/` : 143 fichiers ; dont `final2/`, `mutants-*.txt`, `rouge-*.txt`, `banc-*`, `rejeu-exemples-*`, `classe-differentiel-*`, `tete-72aa806-*`, `verif-serie-final2.txt`, `compte-diffs-final2.txt`, `r13-final2.txt`, `secrets-final2.txt`).

**Chiffres recomptés par moi** : lignes et tests des tables METRIQUES (wc, compte des `def test_`) ; lignes de code des diffs (`compte_diffs.py`) ; planchers 134 à 141, 183 et 406 (Ran mesuré) ; M = 4 ; seuils et écarts du banc.

**PID réels** (tous terminés, rien ne tourne) : 718, 30511, 10407, 10691, 19595, 29820.

**Nettoyage** : base, e9, w, etats, tmp et cible-cargo supprimés ; le dossier `corr` fait 1,9 Mo.

## 11. Fichiers

- Diffs : `<scratchpad>/s2bis/cb18/corr/diffs/` (CB-18g.diff à CB-18q.diff)
- Sections METRIQUES : `<scratchpad>/s2bis/cb18/corr/metriques/`
- Mutants : `<scratchpad>/s2bis/cb18/corr/mutants/`
- Preuves : `<scratchpad>/s2bis/cb18/corr/preuves/`
- Outils : `<scratchpad>/s2bis/cb18/corr/outils/`
- Notes : `<scratchpad>/s2bis/cb18/corr/NOTES.md`
- Sommes : `<scratchpad>/s2bis/cb18/corr/SHA256SUMS` (sha256 ddd515b5…, 235 entrées, contrôle `sha256sum -c` : 235 OK)
- Recalage proposé de gates.yml sur la tête : `<scratchpad>/s2bis/cb18/corr/preuves/tete-72aa806-gates-recale.diff`
