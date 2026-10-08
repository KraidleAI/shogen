# Contre-contrôle bref de CB-18r, s, t (transcrit)

> Transcription par l'orchestrateur le 2026-10-05 13:24:08 UTC du rapport rendu par message par le réviseur G2 (agent a2fb4f197970d4d60) ; contrôle FM-1.1 : fragments_l51_l14 = 0. Texte du réviseur ci-dessous, sans retouche.

**Gate 0 :** je tourne sous `claude-opus-5-5`.

# Contre-contrôle bref de CB-18r, CB-18s et CB-18t : **NON-CONFORME**, liste fermée **CC2-1** et **CC2-2**

J'ai lu l'horloge (`date -u`) à 13:06:22 au début et à 13:22:15 à la fin.

**Base.** 5f99ab5, plus les 20 diffs recalés (20 OK), plus r, s et t (SHA256SUMS de corr2 : 123 OK). Je les ai appliqués dans mon propre clone nu, par `apply --cached`. Arbres obtenus : r a9e89f2e, s 871c8ba0, t **9b21c597**, comme annoncé. L'extraction de t avec les exclusions donne cea5ab97, la même que celle du worker.

## Point par point

**1. Leurres.**
- **Mes 20 leurres** (`leurres_cc.py`, sur le `gates.yml` final) : les 8 failles du premier contre-contrôle sont refusées chacune par son cas K. Les 10 refus sont gardés. Seuls N-12 et N-14 passent.
- **13 leurres neufs contre le gabarit** (`leurres_cc2.py`), dont 5 sont refusés : `runs-on` entre guillemets, espace finale, tag du checkout changé, `with:` en flux, `!!str |`.
- **8 passent K-01 à K-03 et le runner réel** (72 ok) :
  - **LC-03, c'est CC2-1.**
  - **LC-01** relève de la même classe (CC2-1).
  - **LC-02** : un commentaire d'indentation 8 suivi de `set +e`. Le YAML est invalide ; c'est du résidu de validité.
  - **LC-13** : ancre et alias ; c'est le résidu déjà déclaré.
  - **LC-07** (nom de job en bloc plié) et **LC-08** (`timeout-minutes` à 600) : sans effet sur ce que K certifie.
  - **LC-09 et LC-10** : une espace insécable dans le bloc. Le job échoue alors à l'exécution (sortie 127 ou 3) : la gate reste fermée.

**2. Mutants CA et anti-masquage.**
- CA-01 à CA-12 : **12 tués sur 12** par la commande du job sur t. Le rouge de CB-18s est reproduit : à l'état r, les trois mutants survivent (69 ok) ; à l'état s, chacun fait échouer son seul cas (L-33, L-34, A-03).
- L-01 à L-21 jugés par l'analyseur seul : c'est **sain**.
  - À q, l'analyseur seul refusait déjà chacun de ces leurres.
  - Le gabarit seul en refuse 12 (L-01 à L-04, L-08 à L-12, L-14, L-18, L-34). Jugés par `cable`, ces 12 cas masqueraient les mutants de l'analyseur.
  - Le composé reste couvert : K-01 à K-03 et L-00 comme témoins, L-22 (refus de l'analyseur à travers `cable`), L-23 à L-32 (refus du gabarit à travers `cable`).

**3. Runner : 58 → 72 cas, aucun affaibli.**
- V, E et C sont identiques octet pour octet.
- Les 58 identifiants sont gardés et leurs libellés n'ont pas changé. Les données de L-00 à L-21, A-01, A-02 et L-22 sont identiques.
- Ajouts : L-23 à L-34, G-01 et A-03.
- Rouge de CB-18r reproduit : sous le `cable` de q, L-23 à L-29 et G-01 sont admis ; L-30 à L-32 étaient déjà refusés.
- **E-4 : juste.** Les mots exclus ne peuvent plus figurer que dans une valeur libre (nom ou timeout), sans effet.
- **E-5 : exact.** J'ai joué trois mutants du gabarit (shell de l'étape 3, `run: |`, ligne du runner) : tous VIVANTS, donc équivalents pour `cable`. C'est acceptable : ces lignes servent d'ancres de position. Des cas G sur le gabarit seul sont possibles, mais pas exigés.

**4. Lettres du FORMAT.**
- **O-1 :** la phrase de l'avis l.78 est au §7.4 mot pour mot. L'incise reprend exactement le texte de l'adjudication, et la phrase « Les lecteurs appliquent le §7.1 avant le §7.4. » est ajoutée.
- **E-3** (remplacement de la paraphrase de CB-18p) : sain. La paraphrase est contenue dans la phrase de l'avis, et j'ai vérifié par comparaison mot à mot qu'aucun autre mot ne change.
- **O-2 :** la ligne du §5 est conforme. Elle correspond à ce que j'avais montré : c'est le préfixe court qui est refusé.
- Seul autre changement du FORMAT : la puce « Corrections ».
- Le test ajouté produit 3 absences sur le FORMAT d'avant.

**5. Arbre final : tout est conforme.**
- **Jobs** (borne de 300 s, réseau isolé) : s2bis Ran **184** sous 3.10, 3.11, 3.12 et 3.13 ; S2 **406** avec `--egal` ; sim-bis **129** ; runner 72 ok.
- **Matrice `-X dev -W error`** : 184 OK, 0 avertissement, de 3.10 à 3.13. Le test du rôle passe sous 3.11 à 3.13 ; sous 3.10, il a un échec, déjà connu (PY310-1).
- **R-13 :** 0 sur 203 lignes ajoutées ; contrôle positif 2 sur 2.
- **Octets 92 :** 0 ajouté, 1 retiré dans r, comme déclaré. Aucun import neuf.
- **xtask :** S-G1 à S-G8, fmt, no_std et clippy sont VERT. S-G9 est ROUGE pour `docs/17:70` seul. Les verdicts sont identiques à ceux de f342a14b.

**6. E-7 : il faut corriger, une note ne suffit pas. C'est CC2-2.**

## CC2-1 : une chaîne entre guillemets sur plusieurs lignes, dans une valeur libre du gabarit, avale des lignes du gabarit

Les jokers `.*` du gabarit admettent un scalaire entre guillemets ouvert sur une ligne et fermé plusieurs lignes plus bas. Les lignes ainsi avalées gardent leur indentation exacte.
- **LC-03 :** le nom de l'étape 2 est `"cas…` et se ferme sur `- name: suite"`. K-02 certifie trois étapes. PyYAML (le seul analyseur YAML disponible ici, utilisé comme témoin) lit un YAML **valide à 2 étapes** : le runner est avalé dans un nom et ne tourne pas dans ce job.
- **LC-01 :** même mécanisme sur le nom du job, qui avale `runs-on` et `timeout-minutes`. PyYAML lit `runs-on` absent.

Je ne peux pas vérifier ici comment la forge lit ce YAML [abs]. Mais ce leurre défait l'exactitude que revendique le docstring du gabarit, et il manque au critère « seuls N-12 et N-14 passent ».

**Remède, preuve à l'appui** (`preuves/poc-remede-lc03.diff`, aucun octet 92) : imposer aux valeurs libres un scalaire simple, `name: [0-9A-Za-z].*` (trois lignes) et `timeout-minutes: [1-9][0-9]*`. J'ai ajouté deux cas, L-35 (LC-03) et L-36 (LC-01). Ils sont rouges avec le gabarit de t (72 ok, 2 échecs) et verts avec le remède (74 ok). LC-01, LC-03, LC-07 et LC-13 sont alors refusés ; les 20 leurres d'avant ne changent pas.

Si l'orchestrateur préfère ne pas coder, il faut au moins inscrire LC-03 et LC-01 au résidu ANALYSEUR-RESIDUS-1.

## CC2-2 : la note de CB-18r sur le recalage est incomplète

La note dit que les sections CB-18g à CB-18q citent les planchers d'avant le recalage. C'est vrai, mais incomplet :
- les sections CB-18a à CB-18f, SEGMENT-JOUR et ENTIER-ECRIVAIN citent aussi 117 à 133, au lieu de 159 à 175 ;
- au total, **49 valeurs** « Suite : N tests », « plancher du job : N » et `--plancher N` sont décalées de 42, dans 17 sections ; 26 d'entre elles sont hors du champ de la note ;
- chaque commit de a à q serait versé avec une METRIQUES qui contredit son propre `gates.yml`, et la note n'arrive qu'à r.

Valeurs justes : les Ran mesurés sur les 20 états recalés, de 159 à 183. **Correction recommandée :** que l'outil de recalage décale ces trois formes de 42 dans les 20 sections, comme il le fait déjà pour `gates.yml`. À défaut, il faut au moins étendre la note à CB-18a–CB-18q.

## Journal G1
- **[lu] :**
  - pièces du lot : BRIEF-CC-CB18 5d8f0ab0 ; rapport du worker cb0a37e6 (entier) ; AVIS-FORMAT 6daf4065 (l.75-79) ;
  - diffs r, s et t (a4ab9dfd, 37c626e1, d1594cf2) ;
  - le worker : `sonde-masquage.txt`, `campagne-leurres_t.txt`, `rouge-CB-18t.txt`, `sonde_cas_analyseur.py` d9d704fd et l'en-tête de `campagne_leurres.py` ;
  - l'arbre t : runner (l.1-30 et 134-271), FORMAT (§5 et §7.4, comparés à q), METRIQUES (l.963-1053, et par grep).
- **[abs] :** `lecteur.py`, l'oracle de RB-18, les pièces D.2, tout `*.jsonl`, les dossiers exclus, le comportement de la forge.
- **PID réels, tous terminés :** 30879, 3127 et 7179. PyYAML 6.0.1 du système a servi de témoin seulement ; rien n'a été installé.
- **Nettoyage :** copies, clone, index, cible cargo et TMP supprimés.

## Fichiers
- `<scratchpad>/s2bis/cb18/cc2/SHA256SUMS` (87 entrées, 87 OK, sha256 865ac33f…)
- `<scratchpad>/s2bis/cb18/cc2/travail/NOTES-CC2.md`
- `<scratchpad>/s2bis/cb18/cc2/travail/preuves/` :
  - `leurres2-t.txt`, `leurres-t.txt` ;
  - `poc-remede-lc03.diff` et `.txt` ;
  - `mutants-CA-t.txt`, `mutants-E5-t.txt` ;
  - `cas-runner-q.txt`, `cas-runner-t.txt` ;
  - `rouge-r-cable-avant.txt`, `rouge-s-CA.txt` ;
  - `verif-t.log`, `xtask-t-verdicts.txt`, `arbres-rst.txt`.
- `<scratchpad>/s2bis/cb18/cc2/travail/outils/` et `leurres2/` (les 13 `gates.yml` leurres)
