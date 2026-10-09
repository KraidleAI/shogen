# Avis de l'advisor sur NPRIME-NUL-1 (transcrit)

> Transcription par l'orchestrateur le 2026-10-09 18:27:52 UTC du fichier AVIS.md ; contrôle FM-1.1 des transcripts de l'advisor (claude-fable-5-1), du générateur-correcteur, du réviseur et du contre-contrôleur (claude-opus-5-5), par le fm11.py versé et par celui de DETTES-T3 : fragments_l51_l14 = 0. Texte ci-dessous sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

# Avis advisor — SHOGEN-SIM-BIS-NPRIME-NUL-1 (n′_s = 0 dans SIM-BIS)

Advisor `claude-fable-5-1`, effort medium (CLAUDE.md §7). 2026-10-09. Lecture seule ; aucune pièce de la liste D.2 ouverte,
aucune pièce interdite par le brief ouverte, aucune recherche récursive sur docs/ ni sur le dépôt. Pièces lues : `regle.py`
et `calendrier.py` (tête), `executer.py` (copie e11w, absent de la tête), `variante.py` et `tests/test_regle.py`,
`tests/test_oracle_recalc.py` (tête, par grep ciblé), PROPOSITION.md (table E-S), G0-SIM-BIS.md (93 lignes), RAPPORT-G2 §7 et
§11, RAPPORT-CC (section NPRIME), `journal/nprime.txt`.

## 1. Ce que le code fait aujourd'hui (mesuré ou lu)

- `calendrier.retenues` rend, quand aucune fenêtre évaluable n'est présente à T_max, `{"masque": 0, "n": 0, "atteinte": None,
  "suffisant": False}` (calendrier.py l.62-63). Ce n'est pas un refus : n′ = 0 est une valeur légitime de la couche SB-5.
- `executer.replication` calcule `n = {s: ret[s]["n"]}` (l.384), puis `regle.retraits` avec ce n (l.385-386) : à n = 0,
  tout ok(u, s) vaut 0, donc chaque unité est retirée en « D1-bis (a) » ou « (b) » (regle.py l.119-124) ; les séries de
  chaque classe sont vides et `prem = None` (executer.py l.389, l.393). Puis `_tester` appelle `regle.oracle`/`regle.tester`
  avec n = 0 (l.348-349, l.394) : `_controler` → `_cle` lève `REGLE/entier` (regle.py l.46-47). C'est le refus mesuré
  (`journal/nprime.txt` l.6 ; RAPPORT-CC l.233-236).
- Le refus de n < 1 dans `regle` n'est pas accidentel : il est l'alignement SB-8c sur le contrat RB-6 §4 « refus nommés de
  toutes les entrées avant tout calcul (graine, n, …) » (regle.py l.9-11, l.38-41, l.184-187) et il est scellé par des tests
  (test_regle.py l.36, l.47, l.420, l.442 : « n nul (REGLE/entier) ») ; l'oracle croisé SB-13 repose sur ce contrat
  (test_oracle_recalc.py l.1, l.182, l.242). `variante.py` emprunte les mêmes contrôles (variante.py l.6-7, l.36, l.56) ; `filtrer`
  et `loi_evenements` aussi (regle.py l.300, l.334).
- La garde de la règle, à séries vides, donne déjà une réponse définie : `_entrees` rend unites = 0, K = 0, runs = 0, aucune
  rotation calculée (regle.py l.195-197, l.204) ; `_valeur` rend NON ÉVALUABLE avec toutes les causes vraies (l.164-165).
  Mesuré à n = 1 : 0 ou 1 unité → [unites, k_crit, runs, n_prime] (RAPPORT-CC l.241-242). La seule chose qui manque à n = 0
  est donc le passage de la porte `_cle`/`_masques`.
- Exigences : E-S-28 définit testable ⇔ (≥ 2 unités en écart) ∧ (K_crit ≥ 2) ∧ (≥ 2 runs) ∧ (n′_s ≥ n_s/2), et « NON
  ÉVALUABLE compté par cause » (PROPOSITION.md l.182). À n′_s = 0, les quatre conditions sont fausses. E-S-52 demande les
  fréquences par cause, « information insuffisante, détaillée en ≤ 1 unité en écart, K_crit < 2, moins de 2 runs ;
  n′_s < n_s/2 » (l.221). E-S-45 : un lot interrompu se refait, jamais compté (l.209) — d'où le blocage d'E0 par un refus
  reproductible (RAPPORT-G2 l.306-307).
- `frequences` compte « insuffisante » dès qu'une cause parmi unites/k_crit/runs est présente, n_prime à part, et tient la
  table des combinaisons (executer.py l.40, l.62-66, l.78-81). `agreger` lit la forme du premier enregistrement (« avec »,
  « variante ») et l'exige de tous (l.436-442).

## 2. Options

**(a) Refus nommé distinct (REPLICATION/nprime) qui arrête la cellule.**
Conforme à la lettre du contrat RB-6 §4 (refus avant calcul), message explicite. Mais : (i) ce refus serait déterministe
par (cellule, i) (graines par réplication, E-S-41/E-S-44), donc le lot échouerait à chaque reprise : E0 reste bloqué
(E-S-45, RAPPORT-G2 l.306) ; (ii) il retire une réplication du dénominateur R ou fait tomber la cellule, alors qu'E-S-28
demande que le cas soit **compté** par cause ; (iii) il déplace vers l'opérateur un choix (« que faire de la cellule ? »)
que la règle a déjà tranché. Je ne le recommande pas. Variante « refus attrapé dans `calculer_lot` et converti en
enregistrement » : c'est (b) avec un détour.

**(b) NON ÉVALUABLE à liste de causes fixe, dans `executer.replication`.** Recommandée, voir §3.

**(b′) Même chose avec causes = [n_prime] seul**, hors « insuffisante ». Isole l'axe « n′_s < n_s/2 » d'E-S-52, mais
contredit la sémantique des causes « non exclusives » de la garde (regle.py l.144-145, l.163-165) et crée une discontinuité
entre n′ = 0 ([n_prime]) et n′ = 1 à 0 unité ([unites, k_crit, runs, n_prime], mesuré). L'axe isolé existe déjà par la
table des combinaisons (executer.py l.64-65, l.80-81). Non recommandée.

**(c) Relâcher `_cle`/`_masques` à n ≥ 0 dans `regle` (SB-7).** Le plus petit diff en apparence, mais : change le contrat
partagé avec RB-6 (regle.py l.9-11 ; item SHOGEN-SIM-BIS-CONTRAT-RB6-1 ; test_oracle_recalc.py l.1) ; casse des tests scellés
(test_regle.py l.420, l.442) ; laisse des bords non contrôlés (`decalage` fait `% n`, l.61 ; `tourner` fait `x >> (n − o)`,
l.67 ; `filtrer` fait `Fraction(…, n)`, l.335 ; `variante.demi(n, diviseur)`), sûrs seulement tant que les séries sont vides.
Un correctif de SB-7 rouvrirait RB-6 pour un cas que RB-6 (réel, recalc) ne rencontre pas. Non recommandée.

## 3. Recommandation

**(b), dans `executer.replication` (SB-11), avant tout appel à `regle` ou `variante`**, comme application directe de
la garde d'E-S-28 au niveau de la chaîne, sans toucher au contrat de `regle` :

1. Dans la boucle par strate (executer.py l.388-401), si `n[s] == 0` : pour chaque classe, `res[cl]` reçoit un
   enregistrement dégénéré, et la branche `loi_evenements` (l.395-397) est sautée ; `retraits`, `premiere`, `M`,
   `valeurs` (regle.strate), `retraits` imprimés et `impressions` restent tels quels (ils sont déjà corrects à n = 0).
2. Contenu de l'enregistrement dégénéré, **défini comme « ce que la règle rend sur des séries vides »**, pas inventé :
   `valeur = "NON ÉVALUABLE"`, `causes = list(regle.CAUSES)` = [unites, k_crit, runs, n_prime] (chacune vraie à n′ = 0 :
   0 unité < 2, C1 = 0 ≤ seuil, 0 run < 2, 0 < n_s/2 ; RAPPORT-CC l.243-244), `K = 0`, `S = 0` si S suivie sinon None,
   `runs = 0`, `unites = 0`, et les compteurs tels que `decider` les produit à 0 unité (aucun arrêt anticipé : `C = R`,
   `C1 = 0`, `C_S = R` si S suivie sinon None, `r = R` ; regle.py l.149-159, l.204). Mêmes sous-blocs que la forme
   normale quand la cellule les demande : `avec` (mêmes champs, `retirees = []`, `indice = 0`), `variante[d]` (mêmes champs,
   N à définir par la même recette, `variante.demi`), pour que `agreger` (l.436-442) trouve la même forme dans tous les
   enregistrements. Le G0 du correctif doit écrire cette liste, champ par champ (O-CC-6, RAPPORT-CC l.282-285).
3. `regle` reste intact : n = 0 y reste `REGLE/entier` ; `regle.CAUSES` est la seule source de la liste (pas de littéral
   dans `executer`).
4. Spécification : ajout daté au G0 (G0-SIM-BIS.md) sous E-S-28/E-S-52 : « n′_s = 0 : NON ÉVALUABLE, causes [unites,
   k_crit, runs, n_prime], compté en information insuffisante et en n_prime, sans appel à la règle ; aucun refus » ; une
   ligne au tableau d'items.

Pourquoi `executer` et pas `regle` : le contrat de `regle` (n ≥ 1) est celui de RB-6 et de l'oracle croisé ; n′ = 0 est
un état de la **collecte simulée** (calendrier, SB-5), pas de la règle ; la décision « strate sans fenêtre retenue =
non testable » est déjà celle d'E-S-28 (n′_s ≥ n_s/2 faux). Le lieu qui connaît n′ et la forme de l'enregistrement est
`replication`.

## 4. Risques

- **Croisement RB-6 (CONTRAT-RB6-1, oracle_recalc)** : nul avec (b) — `regle.py`, ses refus et les vecteurs du contrat
  (test_oracle_recalc.py l.182, l.242) ne changent pas. Avec (c) : contrat à rouvrir, tests scellés à réécrire, RB-6 à
  réaligner (regle.py l.9-11).
- **Taux d'information insuffisante (§5.1)** : avec (b), chaque réplication à n′ = 0 compte +1 en NON ÉVALUABLE, +1 en
  chacune des quatre causes, +1 en « insuffisante », +1 en combinaison « unites+k_crit+runs+n_prime » (executer.py
  l.75-81). Le taux d'insuffisante monte donc dans les cellules qui produisent n′ = 0 ; c'est une information vraie (0 unité
  en écart) et l'axe « n′_s < n_s/2 seul » reste lisible par la combinaison « n_prime » (sans les trois autres). À
  signaler au paquet (E-S-52 : « imprimées au paquet »). Aujourd'hui aucune cellule n'emploie la grille « large »
  (RAPPORT-G2 l.295, O-11) : l'effet attendu sur E0/E1 est petit, mais un lot ne doit pas tomber pour autant.
- **Forme des enregistrements** : si l'enregistrement dégénéré n'a pas exactement les clés de la forme normale (« avec »,
  « variante », « C_S »), `agreger` lève KeyError (l.439-442) — ce serait un nouveau blocage d'E0 à l'agrégation, plus
  tard et plus cher. D'où le test 2 ci-dessous.
- **Oracle d'E-S-29 (i < 200)** : à n′ = 0, aucune comparaison anticipé/complet n'est faite pour cette strate ; le
  sous-ensemble pré-déclaré reste « les 200 premières », mais le nombre de comparaisons effectives baisse. À écrire dans
  le G0 ; sans conséquence sur la preuve (aucune rotation n'existe à comparer).
- **E-S-44** : l'enregistrement dégénéré doit être déterministe et JSON canonique (Fraction/Decimal via `jsonable`,
  l.85-96) ; pas de risque si les valeurs sont des entiers et None.
- **Mutants de site d'appel** (MUT-EQUIV-FIXTURE-1, RAPPORT-G2 l.332-335) : la branche `n[s] == 0` est un site d'appel de
  plus ; la fixture doit exercer tous les sous-blocs (S suivie, absorption, variante non vide, evenements ≥ 2).

## 5. Tests qui prouveront le choix

1. **Reproduction** (recette RAPPORT-CC l.233-236) : `executer.replication(P99, EP, cel(couche__grille="large",
   couche__repli=True), POINTS, 1, 1)` ne lève plus ; garde de fixture : `strates["stress"]["n"] == 0` et
   `strates["calme"]["n"] > 0` (le test échoue si la fixture cesse de produire n′ = 0, comme la garde de C-6, RAPPORT-CC
   l.289) ; pour chaque classe : `valeur == "NON ÉVALUABLE"`, `causes == list(regle.CAUSES)`, `premiere is None`,
   `retraits` non vide.
2. **Forme** : `sorted(res_stress[cl]) == sorted(res_calme[cl])` pour chaque classe et chaque sous-bloc (`avec`,
   `variante[d]`), sur une cellule à S suivie, absorption True, variante non vide, evenements ≥ 2 ; puis
   `agreger(k, [rec] * 3)` et `frequences` passent, avec `insuffisante == 3`, `causes[x] == 3` pour les quatre causes,
   `combinaisons == {"unites+k_crit+runs+n_prime": 3}`.
3. **Équivalence avec la règle** (preuve que rien n'est inventé) : l'enregistrement dégénéré de la classe égale, champ par
   champ, `_court(regle.tester({}, None, graine, "stress", 1, n_s, p, R, S))` pour S ∈ {False, True} et n_s ≥ 3 (à n = 1
   et séries vides, la règle rend exactement la liste complète et C = R, C1 = 0, r = R). Idem pour `avec` et `variante`.
4. **Non-régression du contrat** : `regle.tester(…, n=0, …)` lève toujours `REGLE/entier` (test_regle.py l.420, l.442
   inchangés) ; `test_oracle_recalc.py` inchangé et vert.
5. **Déterminisme** (E-S-44) : `ecrire_lot` deux fois sur cette fixture → même sha256 ; 1 contre 4 processus,
   PYTHONHASHSEED 0 contre 1 (à joindre au passage hors suite demandé en Q-SB11-16, RAPPORT-G2 l.318-319).
6. **Mutants à tuer** : `n[s] == 0` → `n[s] < 0` (jamais pris : tué par 1) ; causes littérales au lieu de `regle.CAUSES`
   (tué par 3 si CAUSES change) ; branche `evenements` non sautée (tué par 1 : REGLE/entier réapparaît) ; `C = 0` au lieu
   de `R` (tué par 3).

## 6. Ce que l'orchestrateur doit adjuger

- Le lieu : `executer.replication` (SB-11), `regle` intact.
- La liste : `list(regle.CAUSES)`, comptée en insuffisante et en n_prime (pas b′).
- Les valeurs des compteurs de l'enregistrement dégénéré : « ce que `regle.tester` rend sur séries vides » (test 3), à
  écrire explicitement dans le G0.
- L'ajout daté au G0 et la ligne d'item (O-CC-6), avant E0.
