# AVIS — seuil de SHOGEN-FLUX-QUASI-MORT-1 (fixé d'avance, auteur sans exposition)

- Auteur : advisor Shōgen, modèle résolu `claude-fable-5-1`, effort `medium` (CLAUDE.md §7, amendement du 2026-09-18).
- Date : 2026-10-02 (heure de l'orchestrateur).
- Objet : annexe B l.101 (`docs/adr-0028/ANNEXE-B-items.md`) : « Seuil fixé d'avance : avant l'exécution unique, par un auteur sans exposition aux taux de présence par flux (attestation D.3 ; ces taux sont des lectures de classe M déjà faites, D.1 n° 10), écrit à cette annexe par amendement daté ».
- Méthode : raisonnement par la conception seule (doc 10 §5.1 ; ADR-0028 D1 ; code `r1.analysis_pools`), jamais par les données. Aucun chiffre de campagne n'est utilisé hors ceux que l'ADR porte déjà (§5 de cet avis).

## 1. Le seuil et sa définition opérationnelle

**Seuil : un demi.** Dans une strate s du segment analysé, un flux f est « quasi mort » et retiré du pool de la strate si, et seulement si,

    2 · ok(f, s) < n_s

c'est-à-dire si son taux de lectures `ok` est strictement inférieur à 1/2 des fenêtres retenues de la strate. Comparaison en entiers, sans `Decimal`, sans arrondi.

Définition exacte de chaque terme, alignée sur la règle de retrait de D1 telle que codée au lot B0 (`s2-harness/shogen_s2/r1.py` l.421-438, `analysis_pools`) :

1. **Numérateur ok(f, s)** : nombre de fenêtres retenues de la strate s où la lecture last-wins de f (une par couple (fenêtre, flux), `build_reading_map`, l.412-418) a `status == "ok"` **et** `price` non nul — le prédicat de réponse de `classify_ecart` (l.180) et d'`analysis_pools` (l.433). Une lecture `ok` sans prix n'est pas `ok`. Une lecture `ok` peut rester un écart (staleness, hors-enveloppe) : le critère ne regarde pas cela.
2. **Dénominateur n_s** : nombre de fenêtres complétées retenues de la strate s (marqueurs `window_close` dédupliqués par `window_start`, `build_window_strate`, l.403-409 ; `n[st]` dans `analysis_pools`, l.427). Ce n_s est le même que celui de z_s (règle pt 2 ; `compute_r1` l.556).
3. **Lectures absentes** : une fenêtre retenue sans lecture de f compte au dénominateur et pas au numérateur. C'est la convention de R1 : lecture `None` ⇒ PANNE (`classify_ecart` l.180-181). Un flux qui n'émet plus de ligne est le plus mort de tous ; le dénominateur « lectures présentes » (`tot[st, f]`, l.432) le laisserait passer ; il est écarté (§3, V3).
4. **Lectures orphelines** (fenêtre sans marqueur retenu) : hors compte, comme dans `analysis_pools` (l.431) et dans n, K, P̂_more (`records.filtre_lecture`, l.394-399).
5. **Par strate** : le critère s'évalue dans chaque strate s ∈ {calme, stress}, comme le cas (b) de D1 (ADR l.23). Un flux retiré d'une strate reste au pool de l'autre si le critère n'y mord pas. Il n'y a pas de forme « segment » (§3, V4).
6. **Après le filtre de lecture** : segment (D4 / D2 pt 6) puis exclusion D5, dans cet ordre, sur les marqueurs (`records.filtre_lecture`, l.394-411 ; appel l.798-801 de `recompute_from_journal`), puis le compte. Autrement dit : même pool de fenêtres que la règle scellée (règle pt 1 : « pool d'analyse D1 par strate, exclusion D5 »). Dans la sensibilité « plage incluse », le critère se recompte sur ses propres fenêtres retenues ; mais la sensibilité de l'item porte sur la règle scellée (plage exclue) et n'a pas à être croisée avec une autre (§4, L7).
7. **Composition avec D1** : D1 (a) et (b) sont des cas particuliers du critère (ok = 0 ⇒ 2·0 < n_s dès que n_s ≥ 1). Le retrait de la sensibilité remplace donc la règle de retrait de D1 par la règle `2·ok(f, s) < n_s`, dans la même fonction, et retire a fortiori tout ce que D1 retire. Si n_s = 0, aucun retrait (convention d'`analysis_pools`, l.425).
8. **Une seule passe, sans itération, sans ordre** : ok(f, s) et n_s ne dépendent pas de la composition du pool (ni de τ, ni de σ, ni de l'enveloppe leave-one-out). Retirer un flux ne change le critère d'aucun autre. Le résultat est le même quel que soit l'ordre des flux.
9. **Égalité 2·ok(f, s) = n_s** : le flux reste au pool (inégalité stricte, « sous un seuil » au sens littéral de l'item). Convention déclarée, cas de mesure nulle en pratique (§4, L5).
10. **Ce qui est recalculé** : par strate, la règle SHOGEN-CRITERE-R1-1 scellée (`r1.compute_r1` avec `pool_by_strate` réduit, puis `r1.regle_critere`), pts 1 à 8 : n_s (inchangé), K_s, P̂_more,s, garde, z_s, σ̂²_bloc,s, z_bloc,s, valeur et EMD_s. Pas le drapeau 2 (pt 10 : k_eff vient de R2, hors sensibilité) ; la strate poolée stratifiée peut être imprimée à côté, hors décision, comme au rendu principal. Le bloc 1 de la sensibilité nomme chaque retrait avec ok(f, s), n_s et le k nominal_s résultant (D1 (c), ADR l.24).
11. **Étiquette** : « ajoutée après le pré-enregistrement ; hors décision » (annexe B l.101 ; annexe D.5 l.190).

Texte proposé pour l'amendement daté de l'annexe B l.101 : « Seuil fixé le 2026-10-02 : un flux f est retiré du pool de la strate s si 2·ok(f, s) < n_s, où ok(f, s) est le nombre de fenêtres retenues de s (segment, puis exclusion D5) dont la lecture last-wins de f a `status == "ok"` et un prix, et n_s le nombre de fenêtres retenues de s ; lecture absente = non `ok` ; égalité : le flux reste ; une passe, par strate ; D1 (a)/(b) en sont des cas particuliers. Auteur : advisor `claude-fable-5-1`, attestation D.3 jointe. »

## 2. Motif : le demi est le point où le signe du signal bascule

Le modèle (doc 10 §5.1, l.386-402) : p̂ᵢ = fenêtres où i est en écart / n ; P̂₀ = Π(1 − p̂ᵢ), P̂₁ = Σᵢ p̂ᵢ Πⱼ≠ᵢ(1 − p̂ⱼ), P̂_more = 1 − P̂₀ − P̂₁ ; K = fenêtres à ≥ 2 écarts ; z = (K − n·P̂_more)/√(n·P̂_more(1 − P̂_more)). Les p̂ᵢ sont estimés sur la même strate (plug-in, règle pt 11 : « z_s et z_bloc,s conservateurs par le plug-in de P̂_more »).

**Ce qu'un flux presque mort fait à K.** Soit f un flux de taux d'écart p_f et m_t le nombre d'écarts parmi les N − 1 autres flux dans la fenêtre t. La fenêtre compte dans K si D_f,t + m_t ≥ 2, soit : (D_f,t = 1 et m_t ≥ 1) ou (D_f,t = 0 et m_t ≥ 2). Sous indépendance de f et des autres, par fenêtre :

    E[K]/n = p_f · P(m ≥ 1) + (1 − p_f) · P(m ≥ 2).

Le flux f agit comme un **poids de mélange** entre deux statistiques sur les autres flux : « au moins un écart » (poids p_f) et « au moins deux écarts » (poids 1 − p_f). À p_f = 1 (flux mort), K compte les fenêtres où **un seul** autre flux est en écart : le test « ≥ 2 » du pool est devenu un test « ≥ 1 » des autres. C'est le cas (b) de D1 (ADR l.23 : « un flux sans lecture est en écart dans chaque fenêtre de la strate »).

**Ce qu'il fait à P̂_more.** À p_f → 1 : P̂₀ → 0 et P̂₁ → Π_{j≠f}(1 − p̂ⱼ), donc P̂_more → 1 − Π_{j≠f}(1 − p̂ⱼ) = probabilité, sous indépendance, qu'au moins un autre flux soit en écart. Le centrage reste exact sous le modèle nul (le niveau n'est pas touché), mais P̂_more est bien plus grand que la probabilité « ≥ 2 », donc le dénominateur √(n·P̂_more(1 − P̂_more)) grossit : z est comprimé, et la garde §5.4 est tenue plus facilement, avec une statistique qui ne porte plus le bon signal.

**Absorption et signe.** Prenons une co-défaillance positive entre deux flux vivants a et b, de taux petits, covariance c > 0 (les autres flux négligeables au premier ordre) : P(m = 2) = p_a p_b + c, P(m = 0) = 1 − p_a − p_b + p_a p_b + c, donc P(m ≥ 1) = p_a + p_b − p_a p_b − c. L'excès de K sur son espérance plug-in vaut, par fenêtre,

    p_f · (−c) + (1 − p_f) · (+c) = c · (1 − 2 p_f).

- p_f = 0 : excès +c, le test voit la co-défaillance ;
- p_f = 1 : excès −c, soit K − n·P̂ ≈ −n·Cov : c'est exactement le motif de D1 (ADR l.27, avis advisor-defi Q1) ;
- **p_f = 1/2 : excès nul.** Au-delà, la contribution devient négative : le flux « absorbe » la co-défaillance des autres et pousse z vers le bas (annexe D.5 l.190 : « pousse z vers le bas par absorption »).

Le facteur (1 − 2 p_f) vaut, au premier ordre en les taux, pour chaque paire de flux vivants, donc pour la somme des covariances de paires du reste du pool. Le demi n'est donc pas un chiffre choisi parmi d'autres : c'est **le point de bascule du signe** de la sensibilité du test à la co-défaillance entre les flux vivants. Même numérateur pour z_bloc,s (règle pt 3) : même bascule.

**Passage du taux d'écart au taux `ok`.** Le critère retenu porte sur ok(f, s), pas sur p̂_f, parce que (i) l'item nomme « taux `ok` » et D1 est écrite en ok(f, s) (ADR l.21) ; (ii) ok(f, s)/n_s est une grandeur de **disponibilité** (classe M, D.1 n° 10), qui n'entre pas dans le résultat, alors que p̂_f est une composante du résultat : conditionner un retrait sur p̂_f serait sélectionner sur la sortie ; (iii) toute lecture non `ok` ou absente est une PANNE, donc un écart (l.180-181) : écarts(f, s) ≥ n_s − ok(f, s), d'où **2·ok(f, s) < n_s ⇒ p̂_f > 1/2**. Le critère `ok` est une condition suffisante de bascule, calculable sans classification, sans τ ni σ.

**Pourquoi « un demi » et non « rare ».** Le libellé « lectures `ok` rares » de D.5 décrit la cause (une panne de transport ou d'authentification quasi permanente) ; le mécanisme, lui, bascule à un demi. Tout flux dont le taux `ok` est entre 0 et 1/2 a déjà une contribution de signe négatif : le laisser au pool sous prétexte qu'il n'est « pas assez rare » ne corrigerait pas la limite nommée par E-D1b. Inversement, un flux entre 1/2 et 1 contribue positivement, à puissance réduite : ce n'est plus un « flux quasi mort » mais un « flux faible », objet d'une autre question (§4, L3).

## 3. Variantes écartées

- **V1 — un taux « rare » littéral (ok < 5 %, 10 %, 20 %)**. Aucun mécanisme ne désigne l'une de ces valeurs ; il faudrait en choisir une parmi plusieurs, ce qui est un chemin d'analyse (annexe D.5 l.190 : « toute règle à seuil serait un chemin d'analyse » ; ici, un seul seuil, dérivé, pas choisi). Elle laisserait au pool des flux à contribution négative (p_f entre le taux choisi et 1/2).
- **V2 — seuil sur p̂_f (taux d'écart) > 1/2**. Plus proche de la dérivation, mais dépend de τ_classe, σ_classe et de l'enveloppe ; conditionne un retrait sur une composante du résultat ; retirerait un flux vivant mais déviant (staleness, hors-enveloppe), ce qui n'est pas « mort » et serait une autre sensibilité (§4, L2).
- **V3 — dénominateur « lectures présentes » (`tot[st, f]`)**. Un flux qui cesse d'écrire des lignes aurait un taux `ok` élevé sur peu de lignes et échapperait au retrait, alors que R1 le compte en panne à chaque fenêtre absente. Contraire à la convention de `classify_ecart`.
- **V4 — critère sur le segment (somme des strates)**. Le mécanisme agit par strate (p̂ᵢ, K, P̂_more par strate) ; D1 (b) traite déjà le flux mort dans une seule strate par strate ; un flux mort en stress et vivant en calme serait soit retiré à tort du calme, soit gardé à tort en stress.
- **V5 — comptes avant exclusion D5, ou sur le journal entier**. La règle scellée est évaluée après D5 (pt 1) ; le script applique D1 sur les marqueurs filtrés (`r1.py` l.798-801). Les comptes de Pyth « sur le journal entier » de l'ADR (l.25) sont un fait déjà écrit, pas la procédure du rendu.
- **V6 — seuil relatif aux autres flux (médiane des taux `ok`, écart à la moyenne)**. Dépend des données et de la composition du pool ; demanderait une itération ; chemin d'analyse.
- **V7 — seuil tiré de la borne CV2-17 (p̄ > 1/(N−1)², 1 % pour N = 11 ; règle pt 11)**. Autre mécanisme : mode commun qui touche toutes les sources, pas un flux seul ; pas transposable.
- **V8 — critère temporel (plus long run de pannes ≥ ℓ)**. Mesure la dépendance sérielle d'un flux, pas son absorption ; relève de SHOGEN-DEP-FENETRES-2.
- **V9 — retrait itératif**. Sans objet : le critère ne dépend pas du pool (§1, pt 8).
- **V10 — égalité retirée (≤)**. Écartée au profit du « < » littéral de l'item ; à l'égalité, la contribution de premier ordre est nulle et le flux ne fait que dilater P̂_more ; cas de mesure nulle, convention déclarée.

## 4. Risques et limites (règle PAROXYSME : chaque limite est un item à former)

- **L1 — dérivation au premier ordre.** Le facteur (1 − 2 p_f) suppose des taux d'écart petits chez les flux vivants et une alternative par paires ; avec des taux élevés ou une dépendance d'ordre supérieur, le point de bascule n'est pas exactement 1/2. Item : **SHOGEN-FLUX-QUASI-MORT-2**, mesure synthétique du point de bascule (modèle nul et alternative de SIM-NIVEAU, un flux à p_f variable, 11 flux), avant tout usage de la sensibilité dans une proposition à l'investisseur ; prix : réutilisation de `scripts/sim/` [inféré]. La valeur 1/2 reste celle de cet avis : la mesure ne la modifie pas (même principe que la règle pt 7).
- **L2 — proxy par le taux `ok`.** Un flux à taux `ok` élevé mais p̂_f > 1/2 par staleness ou hors-enveloppe absorbe de la même façon et n'est pas retiré. Déclaré ; item : **SHOGEN-FLUX-DEVIANT-1**, sensibilité sur p̂_f, exploratoire, conditionnée sur une composante du résultat, jamais hors étiquette.
- **L3 — flux faibles (taux `ok` entre 1/2 et 1).** Chacun réduit la puissance d'un facteur (1 − 2 p_f) sur la co-défaillance des autres, sans basculer. Non traité par cette sensibilité ; le bloc 1 imprime déjà `ok_windows` et n par source (`compute_r1` l.624). Item : **SHOGEN-FLUX-FAIBLE-1**, puissance de la règle en fonction du profil des taux `ok` (synthétique).
- **L4 — effet sur la garde et sur la valeur.** Retirer un flux change P̂_more,s et le pool de L&M (N) ; une strate peut passer sous la garde §5.4 ou changer de valeur. La sensibilité est hors décision ; toute divergence avec le rendu principal est déclarée, jamais arbitrée (règle pt 11 : « un cas non prévu est une déviation déclarée »). Item : couvert par SHOGEN-FLUX-QUASI-MORT-1 (sortie à étiqueter).
- **L5 — égalité exacte.** Convention « < » (§1, pt 9) ; si une égalité se produit, elle est imprimée.
- **L6 — pool réduit sous N_MIN_HORSENV = 4.** Si une strate garde moins de 4 flux, l'axe (i) devient non évaluable partout ; avec 11 flux et un critère à 1/2, improbable ; refus nommé si cela arrive (fail-closed, pas de z fabriqué). Item : **SHOGEN-POOL-MIN-1**, garde explicite de taille de pool dans la sensibilité.
- **L7 — croisement avec les autres sensibilités.** Le critère n'est défini que pour la règle scellée (plage exclue, J28). Son application à « plage incluse » ou aux J14 serait une sensibilité supplémentaire, non demandée ; si elle est produite, elle est étiquetée de même. Item : à inscrire dans SHOGEN-FLUX-QUASI-MORT-1 (portée : J28, plage exclue).
- **L8 — k nominal_s et comparaison hétérogène.** Après retrait, k nominal_s diffère entre strates ou du k nominal du segment (R2) : mention « comparaison hétérogène déclarée » (règle pt 10), sans drapeau 2 dans la sensibilité.
- **L9 — code.** La sensibilité réutilise `analysis_pools` avec le prédicat `2·ok < n` à la place de `not ok` ; ses tests (fixtures D.4 a, un flux à 49 %, 50 %, 51 % de fenêtres `ok`, un flux sans ligne, une égalité) sont au prix de l'item (≈ 70 lignes, annexe B l.101). Réviseur ≠ générateur (G2).
- **L10 — ce que la sensibilité ne dit pas.** Elle ne distingue pas l'absorption d'une co-défaillance réelle impliquant f ; elle ne « corrige » pas la règle ; elle ne rend aucun verdict (annexe B l.101 : « hors décision »).

## 5. Attestation D.3 (auteur du seuil)

Je n'ai vu aucun z, K, P̂_more ni φ de campagne, ni aucun taux de présence ou de panne par flux ou par source de la campagne, et je n'en ai calculé aucun ; je n'ai ouvert aucune pièce de D.2 (points 1 à 12, liste lue à l'annexe D §D.2 sans en ouvrir le contenu). Je n'ai ouvert ni `JOURNAL.md`, ni `docs/rapports/`, ni `docs/adr-0025/`, ni `docs/adr-0028/monark-m009a/`, ni aucun `*.jsonl`, ni aucun journal G1/G2, ni rien hors du dépôt. Grep utilisé en mode noms et en-têtes de sections seulement (`^#+ ` sur quatre fichiers ; une recherche de mots « mort|quasi|absorption|presque » dans doc 09, sans résultat autre que les en-têtes).

Ce à quoi j'ai été exposé (classe M ou synthétique, déjà écrit dans les pièces autorisées) :
- les comptes de Pyth de D1 : 0 `ok` sur 40 804 lectures, HTTP 401 dès 2026-08-26T19:00Z (ADR l.25 ; PAQUET §2 l.45 ; annexe D.1 n° 7) ;
- les diagnostics DNS de D5 : `resolve_failed` 15,3 % dans la plage contre 1,85 % hors plage ; 5 313 `asn_attribution` dont 815 `resolve_failed` ; 483 `clock_check` (ADR l.58-60 ; PAQUET §3 l.50) — santé du harnais, pas une statistique de source (D.1 n° 8) ;
- les comptes de fenêtres et bornes : n = 35 982 ; 2 618 ; 17 314 ; 9 261 ; 38 600 ; bornes de la plage D5 (ADR l.37, l.52-53, l.59 ; D.1 n° 9) ; bornes calendaires des strates stress des J14 (ADR l.122) ;
- les sorties **synthétiques** de SIM-NIVEAU et de l'étape S (PAQUET §10.3, l.134-165) : taux de rejet à tort sous modèle nul simulé ; ce ne sont pas des données de campagne ;
- les seuils de conception antérieurs à la campagne : 2,33 ; 10 ; ℓ = 240 ; 7 200 ; 0,8416 ; N_MIN_HORSENV = 4 ; τ et σ par classe non lus.

Aucune de ces valeurs n'entre dans le seuil : il est dérivé du modèle de doc 10 §5.1 et de la forme du compte de D1.

## 6. Fichiers ouverts (tous dans `/home/user/shogen`)

- `docs/adr-0028/ANNEXE-D-preenregistrement.md` (entier : D.1 à D.5, dont la liste D.2, sans ouvrir ses pièces) ;
- `docs/adr-0028/ADR-0028-decisions-sortie-S2.md` (entier, l.1-328) ;
- `docs/adr-0028/ANNEXE-B-items.md` (l.85-124, dont l.101) ;
- `docs/adr-0028/PAQUET-PREREG-S2.md` (en-têtes par grep ; §2 l.41-52 ; §10-§11 l.109-188) ;
- `docs/10-mesures-pilotes-design.md` (en-têtes par grep ; §5 l.376-556) ;
- `docs/04-certificat-diversite.md` (en-têtes par grep ; §2 l.45-104) ;
- `docs/09-vocabulaire.md` (grep d'en-têtes et de mots ; l.1-62) ;
- `s2-harness/shogen_s2/r1.py` (entier) ;
- `s2-harness/shogen_s2/records.py` (entier) ;
- `biblio/INDEX.md` (l.1-239 et l.330-339).
