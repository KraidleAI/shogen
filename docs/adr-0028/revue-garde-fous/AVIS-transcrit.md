# Avis de l'advisor sur la proposition d'outils contre les erreurs de l'orchestrateur (transcrit)

> Transcription par l'orchestrateur le 2026-10-15 20:10:04 UTC du fichier garde-fous/AVIS.md ; contrôle FM-1.1 du transcript de l'advisor : fragments_l51_l14 = 0 ; modèle résolu : claude-fable-5-1. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Avis de l'advisor sur le lot GARDE-FOUS-ORCH

Advisor `claude-fable-5-1`, effort medium (CLAUDE.md §7). Écrit le 2026-10-10. Pièces lues, toutes deux en
entier : `scratchpad/garde-fous/PROPOSITION.md` (743 lignes, noté P) et
`scratchpad/garde-fous/ERREURS-ORCHESTRATEUR.md` (27 lignes, noté E). Rien d'autre n'a été ouvert : ni
fichier du dépôt, ni liste, ni recherche. Tout ce qui vient de l'inventaire des lecteurs est donc [2nd] à
travers P. Aucune écriture hors de ce fichier.

Verdict en une phrase : la proposition est sérieuse et bien tracée (P §1.5), ses parades mécaniques tiennent
pour les récidives les plus coûteuses (sceau, message depuis la source, pré-S-G5, heure, ajout en fin), mais
elle est deux à trois fois trop grosse pour un premier lot, elle contrôle au mauvais moment pour deux
classes (E11, E21) et elle repose sur une hypothèse non prouvée pour toute sa phase 2 (le crochet s'applique
aux sous-agents).

---

## (a) Rejeu de chaque classe contre sa parade

Je rejoue l'erreur réelle telle que E et P la décrivent. « Tient » : l'acte aurait été refusé avant le coût.
« Partiel » : une partie du coût évitée. « Règle seule » : rien de mécanique.

| classe | rejeu | verdict |
|---|---|---|
| K-1 brief | E6 (item cité ouvert alors que fermé, E l.12) : B4 lit la dernière ligne de l'annexe B qui nomme l'item et cherche « fermé » (P l.266). Tient si l'annexe B écrit toujours ce mot sur la dernière ligne de l'item ; sinon faux vert. E21 (règle absente du brief, E l.27) : le bloc commun des fiches la porte (P l.581), chargé d'office. Tient. LA-N15 (1 060 pages téléchargées sous un mutant, P l.51) : aucun contrôle du brief ne voit un mutant qui télécharge ; la ligne « sans variables de mandataire » du bloc commun est une règle. | partiel |
| K-2 interdits | LA-N08 (Read d'un rapport interdit) : H1 refuse par suffixe de composant (P l.334, l.209). Tient. E19 (`Glob *.md` à la racine, `grep -r`, `rm -rf /root/.gnupg`, E l.25) : H2 et H14 refusent (P l.335, l.347). Tient **si le crochet voit les outils des sous-agents** : E19 a été commis par des lecteurs et des advisors, pas par l'orchestrateur. P l.622 (Q-19) marque ce point [abs]. Sans cette preuve, la parade de K-2 ne couvre que l'auteur qui n'a pas commis E19. | tient sous condition Q-19 |
| K-3 fond | E3 (chaîne tuée à 30 min, E l.9) : H6 refuse `run_in_background` sans `timeout` (P l.339). Tient. E18 (`sleep` et sondage, E l.24) : règle 14 du skill (P l.460). | tient / règle |
| K-4 disque | E4 : H9 et `disque --min-go` (P l.268, l.342). Tient. Réserve : seuil 5 Go contre 7,6 Go libres mesurés (P l.616) : la garde sera à 2,6 Go du refus dès le premier jour ; voir Q-13. | tient |
| K-5 modèle | LA-N13 (`model` nu) : H5 et B6 (P l.338, l.266). Tient. | tient |
| K-6 état fragile | E11 (chaîne lancée alors que le tableau du CC disait FZ-x rouge seul, E l.17) : `commit --diff` compare l'index aux diffs nommés (P l.262, C6) ; cela ne dit rien du rouge intermédiaire. Le modèle de chaîne s'arrête au rouge, comme la chaîne d'origine s'est arrêtée : même coût (environ 40 min, E l.17). Seule la ligne fixe `GROUPES :` de Q-20 (P l.623) l'aurait empêchée, et elle est renvoyée en « lot optionnel ». | **pas empêchée** |
| K-7 outil non lu | règle seule, raison donnée (P l.150). Honnête. | règle |
| K-8 commit sans vert | LA-N05 (pièce retouchée après vérification, nouveau sha256, P l.63) : la clé du sceau = sha256(HEAD + arbre de l'index) (P l.261) ; la retouche change l'arbre, C1 refuse. Tient. Poussée rouge 84af148 : P1 exige un sceau de la tête. Tient. Limite L-5 (P l.726) : `verif` reste la fonction de l'orchestrateur ; une `verif` tronquée scelle quand même. | tient |
| K-9 message avant source | E8 (« trois passes » contre « sans passe 3 », E l.14) : C3 cherche le nombre de passes dans une source (P l.262) ; « trois passes » n'y est pas, refus. Tient. C2 (date de fichier du message plus récente que la source) : fragile, voir (c). | tient par C3 |
| K-10 S-G5 | E9 : `presg5` sort 1 sur un fragment anglais entre « » (P l.239-241). Tient (l'outil existe déjà, P l.235). E10 (copie d'une pièce dans une autre) : V2, inclusion de 500 caractères (P l.263). Tient. | tient |
| K-11 renvois décalés | E21 (103 renvois décalés par DT14-e et DT14-g, E l.27) : C7 refuse une insertion au milieu d'un fichier de `lignes-citees.txt` (P l.262). Tient **mais à la chaîne de commits**, c'est-à-dire après la phase de générateur et la G2 : le coût de E21 (une phase de générateur, une G2, P l.51) est déjà payé à ce moment. Voir (b). | tient trop tard |
| K-12 correctif sans mutation | règle seule (P l.155). Honnête ; E13 n'aurait pas été évité. | règle |
| K-13 forge seule | E12 (`(?:[&!]\S*\s*)*`) : le prototype le tue à n = 28 (P l.306-309). Tient. E1 (`gates.yml` illisible) : C8 et P3 délèguent à `workflows-yaml.py` (P l.262, l.264). Tient. E5 (cible cargo) : règle I-1 seule. | tient pour E1, E12 |
| K-14 affirmation publique | E2 (cause fausse) : `publier` ne voit que heures, citations, secrets (P l.265). La cause fausse passe. P le dit (l.157). | partiel |
| K-15 mandataire | E17 : H10 refuse une commande de la table (P l.343) ; tient dès la deuxième fois, la première reste. E20 : règle (P l.158). | partiel |
| K-16 heure | E14 (« 04:18 » et « 04:22 » à 04:14, E l.20) : écarts de 4 et 8 min, tolérance 120 s (P l.207) : deux refus. Tient. Une heure passée fausse n'est pas vue (L-3, P l.722). | tient |
| K-17 citation, compte, absence | E16 : C5 et `citations_fausses` avec la forme `JOURNAL l.143` (P l.217-218). Tient si l'orchestrateur écrit la référence dans l'une des formes reconnues ; une citation sans référence passe. E15 : `existe` n'agit que si on le lance (règle 3 du skill, P l.552). E7 : règle. | partiel |
| K-18, K-19, K-20 | règles seules, raisons données (P l.161-163). Honnête. | règle |
| K-21 heredoc | LA-N06 : H7 (P l.340). Tient. | tient |

Bilan : 11 classes tiennent (K-2 sous condition), 4 partielles, 5 règles, 1 non empêchée (K-6). La
proposition annonce « 16 sur 21 mécaniques » (P l.33) : je compte 15 et une (K-6) dont la mécanique ne
vise pas l'erreur.

---

## (b) Ce qui manque

1. **La preuve que le crochet s'applique aux sous-agents, avant de construire la phase 2.** Les erreurs
   de K-2 sont celles des lecteurs et advisors (E l.25). P renvoie la preuve au témoin H0 « lancé par le
   premier worker de chaque passe » (l.622), donc après la construction de GF-11 à GF-16 (six diffs,
   environ 1 055 lignes, P l.649-654). Il faut un témoin de dix lignes dans `settings.local.json` **avant**
   GF-11 : si les sous-agents ne sont pas vus, la phase 2 perd la moitié de sa valeur et doit être
   repensée (par exemple un bloc commun plus strict, ou un lanceur qui enveloppe les sous-agents).

2. **Le moment « réception des diffs d'un worker » n'a aucun contrôle.** E21, E13, E9 et E5 naissent
   dans la copie d'un worker ; la chaîne ne les voit qu'après la G2 et le contre-contrôle. Une
   sous-commande `avant_acte.py diff --fichier x.diff` qui rejoue sur un fichier de diff les mêmes
   contrôles que `commit` (C4 heures, C5 citations, C7 ajout en fin, V1 presg5 sur les `.md`, plus tard
   C10) coûte peu (même code, autre entrée) et déplace le refus avant la G2. Elle devrait être dans le
   premier lot, et aussi dans le bloc commun des fiches (« avant de rendre ton diff, lance… »).

3. **E11 n'a pas de parade.** La ligne fixe `GROUPES :` au rapport du CC (Q-20) est la seule ; elle doit
   passer en phase 1, avec un contrôle `avant_acte.py chaine --plan P --cc RAPPORT` qui refuse un plan où
   un diff listé rouge seul est commité sans son groupe.

4. **LA-N15 (téléchargement et processus orphelins sous mutant)** n'a que des règles. Un contrôle simple
   existe : H6 étendu aux lancements détachés (`setsid`, `nohup`, P l.459 les admet sans borne) et une ligne
   du bloc commun qui impose `timeout` aussi aux campagnes de mutants.

5. **Mesure des faux refus.** Le journal `refus.log` compte les refus (P l.328) mais pas les
   contournements (ligne `Décalage admis`, relance après correction, désactivation). Sans cette colonne, on
   ne saura pas si une garde protège ou si elle gêne. Ajouter un code `contourne` au journal dès GF-5.

6. **Le lot lui-même est un cas de K-19 et K-20.** Vingt diffs, 3 600 à 10 800 lignes (P l.35-36), trois
   G1, trois G2, trois à six CC (P l.666-667) : c'est plus gros que tout lot cité dans E. Il faut une règle
   d'arrêt écrite : après la phase 1, lecture du `refus.log` et décision de l'investisseur avant la
   phase 2 ; aucune phase 3 sans un refus réel enregistré pour la classe visée.

---

## (c) Trop lourd ou fragile

1. **`redos.py` (GF-17, GF-18 : 335 lignes, 10 mutants, sous-processus et `killpg`, P l.289-319)** pour
   une erreur survenue une fois (E12) et dont P dit que « CodeQL reste le juge » (l.319). À retirer du lot ou
   à réduire à une liste de motifs suspects par expression simple (quantificateur imbriqué `(…*)*`,
   `(…+)+`, `\S*\s*)*`), trente lignes, sans exécution.

2. **C2 (date de fichier du message plus récente que celle de la source, P l.262)** : la date de fichier
   change à chaque `git apply`, copie, `touch` ou extraction ; si une source est dans le dépôt, la chaîne
   elle-même la rajeunit et C2 refuse à tort ; si elle est dans le scratchpad, un `cp` suffit à la rajeunir.
   Remplacer par une ligne `Source-Sha: <sha256 de l'adjudication>` dans le message, comparée à la source
   au moment du commit : pas d'horloge, pas de faux refus, et une retouche de l'adjudication après
   l'écriture du message est vue. C3 garde son rôle.

3. **B4 (dernière ligne de l'annexe B qui nomme l'item porte « fermé », P l.266)** repose sur une forme
   de prose non fixée ; à faire en avertissement, ou après une ligne fixe d'état dans l'annexe B.

4. **`citations_fausses` (P l.208)** : fenêtre de 120 caractères, fragments, pliage des apostrophes. Au
   commit (C5) et sur les lignes ajoutées de tous les `.md`, le risque de faux refus est réel. Le garder,
   mais ne refuser que la forme stricte `« … » (chemin:N)` ; les autres formes en avertissement, comptées au
   journal, puis durcies après mesure.

5. **H2 sur `git ls-files` et `git grep` du dépôt entier (P l.335)** : l'orchestrateur en a un usage
   légitime et fréquent ; l'exemption « toutes les exclusions » exige d'écrire huit motifs à chaque fois.
   Mieux : un alias ou un sous-script `scripts/controle/ls_sans_interdits.sh` admis par H2.

6. **Quatre couches pour la même consigne** (skill, crochet, bloc commun, modèle de chaîne). La
   redondance est voulue, mais chaque changement de règle demande quatre diffs. Le test « texte à l'octet
   dans six fiches » (P l.568) est bon ; en échange, les skills ne devraient pas répéter les règles du bloc
   commun, seulement les commandes à lancer.

7. **Phase 1 à dix diffs** : trop pour « aucune configuration du harnais ». Voir l'ordre en (d).

---

## (d) Ordre de construction, du plus rentable au moins rentable

Rentabilité = (récidives × coût unitaire constaté) / lignes à écrire. Chiffres de P §1 et §7.

| rang | diff | pourquoi |
|---|---|---|
| 1 | GF-2 `presg5` versé + GF-7 `verser` | 7 refus S-G5, un `xtask` complet à chaque fois (P l.65) ; l'outil existe déjà (P l.235), le coût est presque nul. |
| 2 | GF-9 modèle de chaîne + GF-5 `sceller`/`commit` C1-C3 (C2 remplacé par `Source-Sha`) | 5 messages faux permanents, 3 commits ou poussées rouges (P l.63-64) ; dommage irréversible dans l'historique. |
| 3 | GF-20 bloc commun des fiches + test | 130 lignes (P l.659) ; couvre E19, E21 (règle), E5 (I-1), LA-N15 pour tous les sous-agents sans dépendre du harnais. À sortir de la phase 3. |
| 4 | GF-1 horloge et heures + skill `shogen-avant-ecrire` | 5 errata (P l.81) ; 160 lignes. |
| 5 | nouveau : `avant_acte.py diff` (réception d'un diff) + GF-6 réduit à C4, C5 strict, C7, C8 | déplace E21, E9, E14 avant la G2 ; réutilise le code de 2 et 4. |
| 6 | Q-20 `GROUPES :` + `avant_acte.py chaine` | seule parade de E11 (40 min par chaîne). |
| 7 | GF-4 interdits, racines, disque + GF-8 `pousser`, `publier`, `existe`, `disque --lister` | K-4 (nettoyage d'urgence), K-14/K-15 partiels, E15. |
| 8 | GF-10 les trois autres skills | texte seul ; après que les commandes existent. |
| **arrêt, lecture du journal des refus, accord de l'investisseur (Q-2, Q-19 prouvée)** | | |
| 9 | GF-11 + GF-14 (H8 git) | la garde que les skills ne remplacent pas : commit ou poussée sans `&&`. |
| 10 | GF-12 (H1, H2, H14), GF-13 (H3-H7), GF-15/16 | seulement si le témoin prouve la portée sur les sous-agents. |
| 11 | GF-19 `brief` réduit à B2, B5, B6, B7 + H13 | B3 et B4 en avertissement. |
| 12 | GF-17/18 `redos.py` | à retirer ou réduire (c.1). |

Les rangs 1 à 8 font environ 1 500 lignes et huit diffs : c'est un lot de taille normale pour ce dépôt,
mesurable (P l.620) avant d'engager le reste.

---

## (e) Réponses aux Q-n (P §6)

| Q | réponse |
|---|---|
| Q-1 | Oui, item d'annexe B en bloc daté et G0 court avant tout code ; un sous-item par contrôle mécanique, pas par classe (une classe peut avoir deux contrôles à deux moments). |
| Q-2 | Oui, accord de l'investisseur, pas de l'orchestrateur. Ajouter : témoin dans `settings.local.json` **avant** la construction de la phase 2 (b.1). |
| Q-3 | Hôte cloud seul d'abord (`settings.local.json`) ; le poste Windows attend la mesure. |
| Q-4 | D'accord : B5 ne contrôle que la cohérence brief/fiche tant que la phrase de l'investisseur n'est pas inscrite mot pour mot (c'est K-18 appliqué au lot lui-même). |
| Q-5, Q-6 | D'accord ; ligne source copiée en tête avec sha256 ; entrées du mandataire confirmées une à une, la première entrée vaut déjà H10. |
| Q-7, Q-8 | Lire avant d'écrire, oui. Pour D.2 : ne pas recopier les noms dans `interdits.txt` ; faire lire par `garde_commun` la liste déjà tenue par `fm11.py` (une seule source, aucun affichage). |
| Q-9 | Oui si G2 faite et interdits exclus ; sinon C7. L'appeler aussi depuis `avant_acte.py diff` (b.2). |
| Q-10 | Liste bonne ; y ajouter `scripts/controle/README.md` (déjà cité) et les fichiers de `garde/` eux-mêmes. |
| Q-11 | Oui ; la phrase du §4 de la fiche orchestrateur en première ligne, comme écrit (P l.574). |
| Q-12 | Noms des paliers dans un fichier de données, jamais dans le `.py` ; lire la portée du lint avant. |
| Q-13 | 5 Go est trop près de l'espace mesuré (7,6 Go, P l.710). Mesurer une cible cargo d'abord ; proposer 3 Go en refus et 6 Go en avertissement avec `--lister` ; et une règle de clôture : `disque --lister` et suppression des cibles des lots clos à chaque clôture. |
| Q-14 | Oui. Avec `Source-Sha:` en plus de `Diff-Id:` (c.2). |
| Q-15 | Oui ; une citation du passé entre guillemets. |
| Q-16 | Oui, DETTES-T7. |
| Q-17 | Ordre de (d), pas celui de P §7 ; arrêt mesuré après le rang 8. |
| Q-18 | Après la phase 2, avec témoin. |
| Q-19 | Non négociable : à prouver avant GF-11, pas « par le premier worker de chaque passe ». |
| Q-20 | Oui, et en phase 1 (b.3) : c'est la seule parade de E11. |
| Q-21 | Oui ; la ligne du CLAUDE.md appartient au mainteneur. |

---

## Risques de l'avis

- Je n'ai lu ni l'inventaire des lecteurs, ni les sources des coûts : tout coût est [2nd] par P. Si P a mal
  compté une récidive, l'ordre (d) bouge d'un rang, pas plus.
- Le contrat du crochet (sortie 2 bloquante, entrée JSON) est [2nd] dans P (l.325, l.699) et chez moi aussi :
  d'où l'insistance sur le témoin avant la phase 2.
- `Source-Sha` (c.2) est ma proposition, non prototypée : à tester dans GF-5 (un mutant : retouche de
  l'adjudication après écriture du message, refus attendu).
