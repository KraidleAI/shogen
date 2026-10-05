# Rapport du worker — CC-1, CC-2, O-1, O-2 de P1 tranche C (transcrit)

> Transcription par l'orchestrateur le 2026-10-05 13:06:01 UTC du rapport rendu par message par le worker (agent aa9c3df62627c22da) ; contrôle FM-1.1 : fragments_l51_l14 = 0. Texte du worker ci-dessous, sans retouche.

**Gate 0 : modèle résolu `claude-opus-5-5`.** La fiche demande l'effort max ; l'effort réel ne se voit pas de l'intérieur.

# Rapport du worker : corrections CC-1, CC-2, O-1 et O-2 du contre-contrôle de CB-18 (diffs CB-18r, CB-18s, CB-18t)

Date : 2026-10-05, horloge lue à 13:04:47 UTC. Le conteneur a redémarré pendant la vérification finale : je l'ai refaite en entier ; le passage interrompu ne compte pas (§6).

**Base.** Copie de 5f99ab5 par `git archive`, avec les sept exclusions (arbre fc307ffd). J'y ai appliqué les 20 diffs recalés, dans l'ordre du brief (SHA256SUMS eb39992b : 20 OK), sans décalage. La copie obtenue vaut f1aa47a0. L'arbre complet, recalculé dans un clone nu partagé jetable (`read-tree 5f99ab5` puis `apply --cached`), vaut **f342a14b**, comme l'annonce le brief.

**Dépôt.** Aucune écriture : seulement `git --no-optional-locks` (archive, show, diff, rev-parse, log) et un `git clone --shared` vers mon TMPDIR. La tête est 5f99ab5 et l'arbre de travail est propre.

## 1. Résumé point par point

1. **CC-1, remède (a) (CB-18r).** `cable()` = `gabarit` ET `analyseur`.
   - `gabarit` contrôle, à indentation exacte, les lignes brutes du bloc du job, ligne à ligne et dans l'ordre :
     - `name`, `runs-on: ubuntu-24.04`, `timeout-minutes`, `steps` ;
     - le checkout épinglé, son `with:` réduit à `persist-credentials: false` ;
     - le runner ;
     - une étape `run: |` ;
     - puis seulement des lignes d'indentation 10.
   - `analyseur` est la lecture de l'enregistreur de rôle, inchangée.
   - `job()` rend désormais les lignes brutes, sans les lignes vides ni les commentaires d'indentation 8 au plus. Il garde son nom, ce qui laisse l'outil `leurres_cc.py` du réviseur utilisable tel quel.
   - Le docstring de `cable()` dit exactement ces contrôles.
   - Cas ajoutés :
     - L-23 à L-28 : classes N-01, N-02, N-03, N-04, N-17 et N-18 ;
     - L-29 : `with:` du checkout vers un dépôt tiers ;
     - L-30, L-31, L-32 : non-régression (`if:` sur le checkout, `runs-on: ubuntu-24.04-arm`, checkout épinglé à un autre commit) ;
     - G-01 : indentation exacte du bloc.
   - L-01 à L-21 sont désormais jugés **par l'analyseur seul**. Sinon le gabarit masquerait ses mutants : jugés par `cable`, CA-03 survit (`sonde-masquage.txt`). Aucun cas n'est affaibli, et le runner passe de 58 à 69 cas.
2. **CC-2 (CB-18s).** Trois cas, dont le rouge est montré sous leur mutant :
   - L-33 : `env:` simple de premier niveau (tue CA-01) ;
   - L-34 : `runs-on` répété (tue CA-07) ;
   - A-03 : étapes imitées dans le nom plié du job, `etapes` égal à `[]` (tue CA-12).
   Le runner passe à 72 cas. La numérotation diffère de la preuve du réviseur, parce que CC-1 occupe L-23 à L-32.
3. **O-1 (CB-18t), au §7.4 :**
   - l'incise « (un objet nu rend déjà la ligne non intègre, §7.1 d) » ;
   - la phrase de l'avis l.78, mot pour mot ;
   - « Les lecteurs appliquent le §7.1 avant le §7.4. »
   Comparaison mot à mot avec l'état d'avant : seuls ces ajouts apparaissent. Un test de texte est ajouté (§7.4), d'où le plancher s2bis 183 → 184.
4. **O-2 (CB-18t).** Une ligne de limite au §5 : un dossier par journal ; un préfixe qui en prolonge un autre fait refuser le plus court (`JOURNAL/nom`). Elle cite SHOGEN-S2BIS-PREFIXE-NOM-1, que l'orchestrateur forme. Aucun code.
5. **N-12 et N-14.** Aucun code : ils restent dans le résidu ANALYSEUR-RESIDUS-1.

## 2. Diffs (série sur la base recalée, sans décalage)

| diff | code +/− | docs +/− | runner | plancher s2bis | sha256 |
|---|---|---|---|---|---|
| CB-18r | +71/−20 | +42/−0 | 69 cas | 183 | a4ab9dfd… |
| CB-18s | +10/−4 | +30/−0 | 72 cas | 183 | 37c626e1… |
| CB-18t | +13/−1 | +38/−13 | 72 cas | 184 | d1594cf2… |

- **Octets 92 :** 0 ajouté. Un est retiré dans r : la regex `[\w-]` de l'ancien `job()`.
- **R-8 :** aucune dépendance ; PyYAML n'entre pas dans le code.
- **Lignes ajoutées de plus de 120 caractères :** une seule, une ligne de tableau METRIQUES.
- **METRIQUES :** une section par diff, en fin de fichier.
- **Arbres :** copie finale cea5ab97 ; arbre complet **9b21c597** depuis f342a14b.

## 3. Rouges

- **CC-1 :** sous le `cable()` d'avant, L-23 à L-29 et G-01 sont admis ; L-30 à L-32 étaient déjà refusés (`rouge-CB-18r.txt`).
- **CC-2 :** sur l'état r, CA-01, CA-07 et CA-12 survivent (69 ok, 0 échec). Sur l'état s, chacun fait échouer son cas, et lui seul (`rouge-CB-18s-CA.txt`).
- **Leurres :** à r0, l'outil du réviseur admet les 8 failles (`leurres-cc-r0.txt`). À l'état final, elles sont refusées (`leurres-cc-t.txt`).
- **O-1 :** `rouge-CB-18t.txt`, trois absences.

## 4. Mutants et leurres

Commande du job (runner, puis ligne de gates.yml), borne de 300 s, python3.12, réseau isolé.

| ensemble | résultat |
|---|---|
| CB-18r (mutants neufs) | 8 tués sur 8 : gabarit non appelé ; `runs-on`, checkout ou `with:` quelconques ; lignes après le gabarit ; fin du job ; commentaires gardés ; `re.match` |
| CB-18s | CA-01, CA-07, CA-12 : 3 sur 3 |
| CB-18t | 4 sur 4 |
| CA-01 à CA-12 du réviseur, sur l'état final | 12 sur 12 |
| 20 leurres du réviseur (régénérés par `leurres_cc.py` sur le gates.yml final) et 11 leurres neufs (LN-01 à LN-11) | 29 tués ; vivants : N-12 et N-14 seulement (résidu, sans code) |

Les 11 leurres neufs : `ref:` ou `repository:` dans le `with:`, `runs-on` répété, `if:`, `container:`, `continue-on-error` du job, runner caché dans un nom plié, checkout dans le nom plié du job, quatrième étape, `env:` en bloc, `-arm`.

Passages non comptés :
- un premier passage de r où le checkout quelconque survivait ; j'ai ajouté L-32 ;
- une campagne des leurres par `job.py`, archivée (voir E-1).

## 5. Vérifications sur l'état final

| contrôle | résultat |
|---|---|
| job s2bis, python3.10 à 3.13 | Ran **184** |
| job S2 | **406** (`--egal`) |
| job sim-bis | **129** |
| crochets | 54 ok |
| matrice `-X dev -W error`, 3.10 à 3.13 | 184 OK, 0 avertissement |
| test du rôle, 4 versions | OK |
| xtask | identique au témoin du contre-contrôle : S-G1 à S-G8, fmt, no_std et clippy VERT ; S-G9 ROUGE `docs/17-modele-de-menace.md:70` seul (connu) |
| R-13 | 0 occurrence sur les 5 fichiers touchés ; contrôle positif 1 |
| secrets | index : 4 OK ; `--tree` : 782 OK |

## 6. Écarts

- **E-1.** J'ai classé les leurres par l'étape du runner, qui est la même dans les trois jobs (`campagne_leurres.py`), et non par `job.py`. Un leurre réécrit les étapes de son job : `job.py` exécuterait donc les étapes du leurre lui-même. Par exemple, le `git clone` de N-03 sort en 128 hors réseau, et N-16 fait planter l'outil. Cet essai est archivé, non compté.
- **E-2.** Mon `campagne.py` connaît désormais le job sim-bis (arbre entier).
- **E-3.** Au §7.4, la paraphrase de CB-18p est **remplacée** par la phrase de l'avis l.78, mot pour mot, plutôt que doublée.
- **E-4.** `cable()` n'a plus les exclusions textuelles d'avant (`-m unittest`, `continue-on-error`, `if:` dans des lignes dépouillées). Le gabarit et l'analyseur les couvrent ; il ne reste qu'une différence sans portée : ces mots, écrits dans un nom, ne sont plus refusés. Aucun cas ne change de verdict.
- **E-5.** Les lignes du gabarit pour les étapes 2 et 3 doublent l'analyseur, par défense en profondeur. Des mutants y seraient équivalents ; je n'en ai pas généré.
- **E-6.** Redémarrage du conteneur à 12:56. La vérification finale interrompue est archivée dans `preuves/verif-interrompue/` et a été refaite en entier. Les campagnes étaient terminées avant.
- **E-7.** Les sections METRIQUES de CB-18g à CB-18q citent encore les planchers d'avant le recalage (le recalage les a gardés tels quels). La section CB-18r le signale : il faut leur ajouter 42.
- **E-8.** Quelques heures notées sans lecture d'horloge, corrigées dans mes notes.

## 7. Items pour l'orchestrateur

- Former SHOGEN-S2BIS-PREFIXE-NOM-1 : le §5 le cite.
- Étendre ANALYSEUR-RESIDUS-1 à N-12 et N-14.
- K-ETAPES-LEURRE-1 est sans objet, puisque le remède (a) est appliqué.

## 8. Journal G1

**[lu] :**
- Pièces du lot : BRIEF-CC-CB18 5d8f0ab0 (en entier) ; CONTRE-CONTROLE-CB18-transcrit 49ab9605 (en entier).
- Preuves et outils du réviseur : poc-remede-cc1.diff 04c562ea et .txt 1a7877ed ; poc-remede-cc2.diff e7baab62 et .txt a3873ab8 ; leurres-sq.txt 7087bb7b ; mutants-CC-sq.txt 73b49fcc ; ca01, ca07-ca12, leurres-runner-reel ; `leurres_cc.py` 833d72b4 et `mutants_cc.py` 7e94d59a (en entier).
- Autres : AVIS-FORMAT l.78 ; SHA256SUMS des diffs recalés ; runner, vérificateur et gates.yml de l'arbre recalé ; FORMAT §5 et §7.4 ; mes notes de corr.

**[abs] :** `recalc/lecteur.py`, l'oracle de RB-18, les pièces D.2, tout `*.jsonl`, les dossiers exclus, les NOTES-CC du réviseur, mon rapport transcrit.

**[2nd] :** aucun. Tous les chiffres sont recomptés : arbres, comptes de cas, Ran, lignes des diffs.

**PID réels, tous terminés :** 17315, 24333, 32715 (interrompu par le redémarrage), 708.

**Nettoyage :** base, w, etats, tmp et cible-cargo supprimés ; corr2 fait 1,4 Mo.

## 9. Fichiers

- Diffs : `<scratchpad>/s2bis/cb18/corr2/diffs/` (CB-18r.diff, CB-18s.diff, CB-18t.diff)
- Sections METRIQUES : `<scratchpad>/s2bis/cb18/corr2/metriques/`
- Mutants : `<scratchpad>/s2bis/cb18/corr2/mutants/`
- Leurres régénérés : `<scratchpad>/s2bis/cb18/corr2/leurres-cc-t/`
- Preuves : `<scratchpad>/s2bis/cb18/corr2/preuves/` (dont `campagne-*.txt`, `rouge-*.txt`, `leurres-cc-r0.txt`, `leurres-cc-t.txt`, `sonde-masquage.txt`, `final2/`, `verif-serie.txt`)
- Outils : `<scratchpad>/s2bis/cb18/corr2/outils/`
- Notes : `<scratchpad>/s2bis/cb18/corr2/NOTES.md`
- Sommes : `<scratchpad>/s2bis/cb18/corr2/SHA256SUMS` (123 entrées, 123 OK, sha256 359bb47d…)
