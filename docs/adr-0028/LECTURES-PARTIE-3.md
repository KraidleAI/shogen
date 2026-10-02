# Lectures de la partie 3 de S2 — Künsch 1989, Fisher 1921, sources du poolé

Lecteur : session cloud, 2026-10-02. Rapport écrit par le lecteur ; aucun fichier suivi modifié, aucune opération git.

## Gate 0

Modèle sous lequel tourne ce lecteur : `claude-sonnet-5-5` (identifiant exact déclaré par l'environnement : « Sonnet 5.5, model ID claude-sonnet-5-5 »). Conforme au roster lecteurs de CLAUDE.md §7.

## Méthode

- Scans lus avec l'outil Read, page par page : Künsch, les 25 pages (pp. 1217-1241 ; page du fichier n = page de la revue 1216 + n ; la page 1 du fichier est la première page de l'article, avec un bandeau JSTOR en pied, et non une couverture) ; Fisher, pp. 1-18 et 25-27 du fichier (page de Metron = page du fichier + 1 ; le pied de page porte aussi la pagination d'archive 205-231 = Metron + 203) ; Agresti 2013, la seule page 245 du fichier (= p. 227 du livre).
- Théorème 3.3 de Künsch relu sur un agrandissement du scan (rendu à 220 dpi, rogné, fichiers de travail dans le dossier de scratchpad de la session, non suivis) parce que les exposants sont illisibles dans l'OCR.
- Vérification numérique du Thm 3.1 (script jetable, non suivi) : sur une série AR(1) simulée (n = 60, ℓ = 7), σ̂²_Jack calculé par la définition (2.3)-(2.6) avec w_n = 1 sur le bloc et le membre de droite de (3.9) avec les poids v_n(k)/v_n(0) = 1 − |k|/ℓ donnent 0,045953227358328 et 0,045953227358328 (écart de l'ordre de 1e-16) ; Σ_t β_n(t,k) = 1 vérifié. C'est un contrôle de ma lecture, pas une source.
- Règle lue : ADR-0028 §1 bis.1, pts 3 (« Plancher d'erreur-type ») et 7 (« Prémisse de la borne »), par lecture ciblée. `report.py` et `biblio/INDEX.md` lus par recherche ciblée seulement. Aucune pièce de la liste D.2, aucun journal de campagne, ni `docs/adr-0025/`, ni la cartographie du 2026-09-29, n'ont été ouverts.
- Niveaux : [lu] = lu sur le scan, page de la revue citée ; [abs] = absent de la source ; [calc] = calcul du lecteur à partir d'un [lu], signalé comme tel. Aucun [2nd] n'est utilisé. Les citations anglaises sont entre « », les autres passages anglais entre “ ”.

## Point 1 — Künsch 1989, Ann. Statist. 17(3) : 1217-1241

Notation de l'auteur : longueur de bloc `l = l(n)` (l minuscule italique, notée ℓ ci-dessous), n nombre d'observations, poids `w_n(i)`, `σ̂²_Jack`, `σ²_as` (variance asymptotique), `R(k)` covariance, `α(k)` coefficients de mélange fort.

### 1(a) Équivalence du jackknife par blocs avec une covariance pondérée

Fait de base [lu] : le jackknife supprime ou sous-pondère, une fois chacun, les blocs de ℓ observations consécutives, j = 0, …, n − ℓ (éq. (2.3)-(2.4), p. 1220) ; le choix h = indicatrice de (0,1) pour la fonction h de (2.5) « corresponds to simple deletion of blocks » (p. 1220). Avec w_n(i) = 1 pour 1 ≤ i ≤ ℓ, on a ‖w_n‖₁ = ‖w_n‖₂² = ℓ. L'estimateur de variance est la variance empirique des T_N^(j) avec la normalisation (2.6) (p. 1220), σ̂²_Jack estimant la variance de T_N (échelle 1/n).

Équivalence, énoncé exact [lu] — Théorème 3.1, p. 1224 : pour la moyenne arithmétique,
`σ̂²_Jack = n⁻¹ · Σ_{k=−ℓ+1}^{ℓ−1} [v_n(k)/v_n(0)] · R̃_n(k)`  (éq. (3.9)),
où v_n est la convolution de w_n avec elle-même : `v_n(k) = Σ_{j=1}^{ℓ−|k|} w_n(j)·w_n(j+|k|)` (éq. (3.6), p. 1223), et où R̃_n(k) est l'estimation de covariance (3.7)-(3.8) (p. 1223-1224). Commentaire de l'auteur [lu] p. 1224 : « turns out to be a lag weight estimate of the spectral density at zero » (n·σ̂²_Jack) ; et, résumé p. 1217 : « equivalent to a weighted covariance estimate of the spectral density of the observations at zero ».

Poids dans le cas du bloc supprimé simplement [calc, à partir de (3.6) p. 1223 et de la phrase p. 1220] : v_n(k) = ℓ − |k|, v_n(0) = ℓ, donc v_n(k)/v_n(0) = 1 − |k|/ℓ pour |k| < ℓ. Confirmation indirecte [lu] : la remarque 3.3 (p. 1226) dit que, pour h = indicatrice, (3.12) devient « ℓ n⁻¹ 4σ⁴_as/3 », ce qui suppose h∗h(x) = 1 − |x| (∫(1−|x|)² dx = 2/3). Confirmation numérique [calc] : voir Méthode.

Coïncidence avec (1 − k/ℓ) : oui pour les poids, au sens suivant. Forme `n·σ̂²_Jack = R̃_n(0) + 2·Σ_{k=1}^{ℓ−1} (1 − k/ℓ)·R̃_n(k)` (R̃_n(−k) = R̃_n(k), car (3.8) emploie |k|). Mais l'identité de Künsch n'est pas écrite sous la forme « 1 − k/ℓ » dans l'article [abs : aucune occurrence du facteur 1 − |k|/ℓ, du mot « Bartlett » ni de « triangulaire » dans les 25 pages ; l'article ne parle que de v_n(k)/v_n(0) et de la convolution h∗h, éq. (3.11), p. 1224] ; le rapprochement avec le noyau de Bartlett est un calcul du lecteur, non une assertion de l'auteur.

En quoi le reste diffère de la formule de la règle (pt 3) [lu] :
1. R̃_n(k) n'est pas le γ̂_k de la règle. L'auteur le définit (3.7)-(3.8) avec des poids β_n(t,k) égaux à (n − ℓ + 1)⁻¹ pour ℓ − |k| ≤ t ≤ n − ℓ + 1, différents aux bords et de somme 1, et centré sur μ̂_n = Σ α_n(t)X_t (éq. (3.2)-(3.3), p. 1223), non sur la moyenne empirique. Il écrit (p. 1224) : « very similar to the usual sample covariance except that it has a smaller bias ». Et p. 1230 : « Except for the nonstandard version of the sample covariances », σ̂²_Jack(M_N) = σ̂²_Infl. Pour la forme usuelle (2.14) p. 1222 avec poids ω_n(k), l'auteur dit seulement, après (3.9) : « If we choose the weights accordingly, it almost coincides with » σ̂²_Infl (p. 1224). Donc l'égalité exacte vaut pour R̃_n ; avec les γ̂_k usuels centrés sur Ī_s, l'équivalence n'est qu'approchée.
2. Échelle. σ̂²_Jack estime la variance de la moyenne ; n·σ̂²_Jack estime σ²_as = Σ_k R(k) (variance de long terme par observation). La règle (pt 3 lu) écrit σ̂²_bloc,s = γ̂₀ + 2Σ(1−k/ℓ)γ̂_k et l'emploie comme écart-type du compte K_s (numérateur K_s − n_s·P̂, FIV_s = σ̂²_bloc/(n_s·P̂(1−P̂))) : ce n'est cohérent avec Künsch que si les γ̂_k sont des sommes de produits (échelle n·σ²_as, soit n²·σ̂²_Jack), non des moyennes. Le texte du pt 3 (« Comptes entiers par lag ») le suggère mais ne le dit pas explicitement [abs dans le texte lu du pt 3 : normalisation des γ̂_k]. Je n'ai pas ouvert le code. À confirmer par l'orchestrateur.
3. Bootstrap par blocs. Künsch définit aussi un bootstrap qui tire n/ℓ blocs avec remise parmi les n − ℓ + 1 blocs chevauchants (p. 1217-1218, éq. (2.7)-(2.11), pp. 1220-1221). Il montre que le bootstrap et le jackknife à suppression simple donnent la même estimation de variance : « the bootstrap and the jackknife with simple deletion lead to the same variance estimate » (p. 1226), Thm 3.4 (p. 1227) : σ̂²_Boot = σ̂²_Jack pour w_n(i) = 1. Le nom « blocs mobiles » n'est pas employé par l'auteur [abs] ; son terme est « overlapping blocks » (p. 1223, remarque 3.1 : « differs from Carlstein's (1986) method only by using overlapping blocks and general weights »). Sa remarque 3.3 (p. 1226) : « overlapping blocks should be used when one can afford the computations ».

### 1(b) Théorèmes 3.2 et 3.3, corollaire 3.1

Tous trois concernent le jackknife de la moyenne arithmétique avec des poids de la forme (2.5) [lu].

- Théorème 3.2 (pp. 1224-1225), biais. Hypothèse sur ℓ : ℓ = ℓ(n) → ∞. (i) Pour h = indicatrice de (0,1) : si ℓ = o(n^{1/2}) et Σ|k||R(k)| < ∞, alors E[n·σ̂²_Jack] − σ²_as ~ −ℓ⁻¹·Σ|k|R(k). (ii) Pour h∗h deux fois continûment dérivable en 0 : si ℓ = o(n^{1/3}) et Σk²|R(k)| < ∞, alors le biais est d'ordre ℓ⁻² (p. 1225). Ce théorème donne un biais, pas une consistance. Le biais de (i) est négatif quand Σ|k|R(k) > 0 [calc, simple lecture du signe]. La formule exacte du biais à ℓ fini est (3.10) (p. 1224), valable sous ℓ = o(n) et Σ|j||R(j)| < ∞ (lemme 3.1) : elle comprend, outre le terme de poids Σ(v_n(k)/v_n(0) − 1)R(k), le terme −Σ_{|k|≥ℓ}R(k) et un terme en n⁻¹.
- Théorème 3.3 (p. 1225), variance. Hypothèses [lu sur l'agrandissement du scan, exposants illisibles en OCR] : E[|X_t|^{6+δ}] < ∞ et Σ k²·α(k)^{δ/(6+δ)} < ∞ (mélange fort α(k)) ; poids de la forme (2.5) avec ℓ(n) = o(n). Conclusion (3.12) : Var(n·σ̂²_Jack) ~ ℓ·n⁻¹·2σ⁴_as·∫₋₁¹ h∗h(x)² dx / h∗h(0)². L'auteur justifie le choix des coefficients de mélange : « The following theorem uses the strong mixing coefficients » (p. 1225). Remarque 3.3 (p. 1226) : pour h indicatrice, la variance vaut ~ ℓ·n⁻¹·4σ⁴_as/3.
- Corollaire 3.1 (p. 1226) : « Under the conditions of Theorem 3.3 the jackknife for the arithmetic mean is consistent » si ℓ = o(n) et ℓ(n) → ∞ (la condition en mathématique est illisible en OCR, lisible sur le scan : « if l = o(n) and l(n) → ∞ »). Le résumé, p. 1217, dit la même chose : « consistency is obtained if l = l(n) → ∞ and l(n)/n → 0 », sous « appropriate conditions ».
- Vitesses [lu, p. 1226] : en égalant biais² et variance, l'ordre optimal est ℓ = O(n^{1/3}) pour h indicatrice (erreur quadratique moyenne de n·σ̂²_Jack en O(n^{−2/3})) et ℓ = O(n^{1/5}) pour h lisse (O(n^{−4/5})). L'auteur ajoute que la constante exige de connaître σ²_as et Σ|k|^j R(k) (p. 1226). Aucun résultat à ℓ fixe, ni en échantillon fini [abs]. Aucune règle de choix de ℓ égale à une constante comme 240, ni de condition du type n ≥ 30ℓ [abs]. Hors du cadre : dépendance longue, pour laquelle le jackknife sous-estime systématiquement la variance d'un facteur (ℓ/n)^{1−β} (remarque 3.2 (iii), p. 1225 : « excludes models with long-range dependence »).

Réserve de lecture [lu] : le Thm 3.2 et le lemme 3.1 supposent Σ|k||R(k)| < ∞ ; le Thm 3.3 et donc le corollaire 3.1 ne l'énoncent pas ; l'article ne dit pas que la condition de mélange du Thm 3.3 l'implique.

Verdict sur la phrase de la règle (pt 7) « la variance par blocs est consistante quand ℓ croît sans borne et que ℓ/n tend vers 0 (Künsch 1989, Thm 3.2-3.3 [2nd : …]) » : partiellement fidèle.
- Fidèle : le régime (ℓ → ∞, ℓ/n → 0) et la conclusion de consistance, pour la moyenne arithmétique (ce qu'est K_s/n_s) avec suppression simple de blocs chevauchants.
- Imprécis : la consistance est le corollaire 3.1, qui s'appuie sur le Thm 3.3 (variance) et sur (3.10) / Thm 3.2 (biais) ; le Thm 3.2 seul est un résultat de biais, sous ℓ = o(n^{1/2}).
- Omis : les hypothèses de dépendance et de moments (suite stationnaire, E|X_t|^{6+δ} < ∞ — vrai pour I_t à valeurs {0,1} —, et Σk²α(k)^{δ/(6+δ)} < ∞), que la phrase remplace par « une dépendance sérielle de portée < ℓ » (formulation de la règle, non de Künsch). Deux conséquences [calc depuis (3.10)] : la condition de Künsch ne porte pas sur une portée inférieure à ℓ ; et une portée < ℓ n'annule que le terme de troncature −Σ_{|k|≥ℓ}R(k), pas le biais de taper −ℓ⁻¹Σ|k|R(k) du Bartlett, qui subsiste (négatif si les autocorrélations sont positives, donc σ̂²_bloc tend à sous-estimer et z_bloc à surestimer).
- Hors source : ℓ = 240 fixe et n_s ≥ 30ℓ sont des choix de conception ; le théorème est asymptotique en ℓ et ne les couvre pas.
- Le marqueur « [2nd : lu sur OCR … scan en procurement P-01] » peut être levé : les énoncés sont désormais lus sur le scan, mais l'OCR ne les rend pas lisibles (voir 1(c)).

Formulation proposée pour la phrase du pt 7 (à la place de « la variance par blocs est consistante … Thm 3.2-3.3 […] ») :
« la variance par blocs est consistante, pour la moyenne d'une suite stationnaire fortement mélangeante (moment d'ordre 6+δ fini, Σ k²·α(k)^{δ/(6+δ)} < ∞), quand ℓ = ℓ(n) tend vers l'infini avec ℓ/n → 0 (Künsch 1989, corollaire 3.1, p. 1226, appuyé sur le Thm 3.3, p. 1225, pour la variance et sur la formule (3.10) et le Thm 3.2, pp. 1224-1225, pour le biais ; énoncé asymptotique, sans résultat à ℓ fixé ni en échantillon fini ; ℓ = 240 est un choix de conception) ; son biais est de l'ordre de −ℓ⁻¹·Σ|k|R(k) sous ℓ = o(n^{1/2}) (Thm 3.2 (i)) ».

Verdict sur la phrase de la règle (pt 3) « σ̂²_bloc,s = γ̂₀,s + 2·Σ(1 − k/ℓ)·γ̂_k,s … blocs mobiles, noyau de Bartlett (Künsch 1989) » : partiellement fidèle. Les poids 1 − k/ℓ sont ceux de Künsch pour la suppression simple de blocs (calcul de lecteur confirmé numériquement) ; Künsch ne nomme ni « Bartlett » ni « blocs mobiles » ; son R̃_n diffère des γ̂_k centrés sur Ī_s (poids β_n, centrage μ̂_n) ; l'échelle de σ̂²_bloc,s (somme et non moyenne) n'est pas fixée par le texte lu. Formulation proposée : « σ̂²_bloc,s est l'estimateur à poids triangulaires (1 − k/ℓ) de la variance de long terme ; il correspond au jackknife par suppression de blocs chevauchants de longueur ℓ de Künsch 1989 (Thm 3.1, éq. (3.9), p. 1224, avec w_n = 1 : v_n(k)/v_n(0) = 1 − |k|/ℓ), à ceci près que Künsch emploie la covariance empirique modifiée R̃_n (éq. (3.8)) et non les γ̂_k centrés sur Ī_s ; la dénomination « noyau de Bartlett » est celle de l'analyse spectrale et n'est pas de Künsch ». Si la mention « Bartlett » doit être sourcée, il faut une autre source (Künsch cite Priestley 1981 pour les estimateurs spectraux à poids, pp. 1222 et 1225 : non lu ici).

### 1(c) Qualité de l'OCR du jour (tesseract 5.3.4)

Texte courant : identique au scan sur tous les passages cités ci-dessus. Vérification mécanique (recherche des citations, espaces normalisées) : positive pour les 12 citations de Künsch du rapport. Une seule particularité : l'apostrophe de « Carlstein's » est courbe dans l'OCR (le scan aussi).
Mathématique : illisible ou fausse. Erreurs relevées :
- p. 1217, résumé : « l = l(n) → ∞ and l(n)/n → 0 » devient « / = I(n) > o and I(n)/n > 0 » (ℓ lu « / » ou « I », → lu « > », ∞ lu « o ») ; « block of l » devient « block of J ».
- p. 1220, (2.5)-(2.6) : « Choosing for h the indicator function 1(0,1) » devient « Choosing for A the indicator function 1,1) » ; (2.6) est en lambeaux.
- p. 1223, (3.6)-(3.7) et p. 1224, (3.9) (équation décisive du point 1(a)) : inutilisables (« o(k) = Le unl J)un(7 + |Al) » ; « SFack = n-? k d 0,( Rk) /v,(0)R,(R) ») ; seuls les mots de la phrase après (3.9) sont exacts.
- p. 1224-1225, Thm 3.2 : « ℓ = ℓ(n) → ∞ » devient « 1 = I(n) > 0 » ; « ℓ = o(n^{1/2}) » devient « 1 = o(n'””) » ; les formules de biais sont altérées.
- p. 1225, Thm 3.3 : « E[|X_t|^{6+δ}] < ∞ et Σk²α(k)^{δ/(6+δ)} < ∞ » devient « E[|X,|§+®] < 0 and Lk7a(k)°/6*® < 00 » : exposants perdus ; (3.12) altérée. Le texte de la ligne de présentation (« Consider the jackknife for the arithmetic mean and assume ») est exact.
- p. 1226, Cor. 3.1 : « ℓ = o(n) and ℓ(n) → ∞ » devient « 1 = o(n) and l(n) > oo » (lisible par substitution) ; la partie en mots est exacte ; les ordres O(n^{−2/3}), O(n^{−4/5}) sont devenus « O(n~?/%) », « O(n~*/*) ».
La gate des citations de ces passages mathématiques échouera ; les citations retenues sont des passages en texte courant, exacts dans l'OCR. L'OCR antérieure (`2026-09-29/kunsch1989.ocr.txt`) donne les mêmes lectures fausses sur Thm 3.2, Thm 3.3 et Cor. 3.1 (exposants perdus de même) ; sa provenance n'étant pas établie, je n'en tire rien.

## Point 2 — Fisher 1921, Metron 1(3) : 3-32

Notation de l'auteur [lu] : n = nombre de paires d'observations ; r = coefficient de corrélation de l'échantillon ; ρ = valeur de population ; z = variable transformée de l'échantillon, ζ = valeur transformée de la population ; transformation (V), p. 7 (p. 210 du recueil) : « ρ = tanh ζ » et « r = tanh z » ; « tanh⁻¹ » dans la table (pas de notation « artanh ») ; poids d'une observation : « weight », en unités n − 3.

Où l'auteur introduit z [lu] :
- p. 7, §2 « The transformation of the curves of random sampling of correlations within classes of 2 » (corrélations intraclasses), éq. (V) : « could be reduced both to approximate normality and to approximate constancy of the probable error » (la phrase se poursuit « by the transformation »). Cadre : « hypothetical infinite Gaussian population from which the sample is drawn » (p. 5), n paires indépendantes.
- p. 12, §3 « The corresponding transformation for simple interclass correlations » : applique (V) à la corrélation ordinaire r de paires (x, y).
- p. 26, Table I : z = tanh⁻¹ r = ½(log(1 + r) − log(1 − r)) ; p. 27 : « the exact formula », z = ½(log_e(1 + r) − log_e(1 − r)), pour r au-dessus de 0,990 (0,995 généralement).

Erreur-type de z [lu] :
- Corrélation ordinaire (interclasse, §3) : p. 14, le poids d'une observation passe de n − 3 à n − 2½ quand ρ va de 0 à ±1 (paraphrase du scan, p. 14 ; la ligne est dégradée dans l'OCR, donc non citée) ; la courbe en z est « is therefore sufficiently normal and constant in deviation » pour être représentée par une erreur probable, laquelle « This may be obtained from the same table as before entered with the value » n − 3 (p. 14). P. 18 : le poids de chaque échantillon sur l'échelle z est pris égal à (n − 3) (paraphrase du scan ; la formule est dégradée dans l'OCR) et « be attached to values of z may therefore be taken straight from the numbers of observations ».
- Corrélation intraclasse (§2) : p. 10, « The standard deviation is independent of ρ, and very nearly agrees with the formula » 1/√(n − 3/2).
- Vérification [calc, sur [lu]] : exemple III, p. 15 : n = 25, erreur probable de z = ± 0,1438 ; 0,67449/√22 = 0,14380 (0,67449 est le coefficient imprimé p. 11). Cela confirme que l'erreur probable est 0,67449 × (n − 3)^{−1/2}, c'est-à-dire un écart-type 1/√(n − 3) en z.
- La formule « écart-type de z = 1/√(n − 3) » n'est pas imprimée littéralement par Fisher [abs] : l'auteur donne le poids n − 3 et l'erreur probable lue dans une table à l'entrée n − 3 ; l'écart-type 1/√(n − 3) en est la lecture [calc]. Le mot « weight » n'est pas défini explicitement comme inverse de la variance dans les pages lues [abs] (p. 19 le déduit de la dérivée seconde au mode).

Fidélité de la chaîne imprimée par le rapport (`report.py`, ligne 565-566) : « SE(artanh r) = 1/√(N−3), transformation de Fisher, Penn State STAT 509 L7 §7.8 ». Verdict : fidèle sur le fond, avec trois réserves, et attribuée par le rapport à Penn State, non à Fisher, ce qui est exact (la formule 1/√(n−3) sous cette forme se trouve dans la page Penn State de l'INDEX, pas littéralement chez Fisher).
1. La formule est approchée : Fisher parle de courbe « approximately normal », légèrement leptokurtique (« the true curve in z is slightly leptokurtic », p. 12, β₂ = 3,17 pour l'exemple de la p. 11) et d'un poids qui varie de n − 3 à n − 2½ avec ρ (p. 14), négligeable (p. 18).
2. N doit être le nombre de paires indépendantes tirées d'une population gaussienne : cadre de Fisher (p. 5, p. 18). Pour des fenêtres sérialement dépendantes, la source ne dit rien [abs].
3. Notation : Fisher écrit n (paires), z, ζ et tanh⁻¹ ; « artanh » et « N » sont modernes.
Si le rapport (ou la règle) cite Fisher 1921 pour l'erreur-type, la formulation exacte à imprimer est : « SE(z) ≈ 1/√(N−3) (poids N−3 sur l'échelle z, Fisher 1921, Metron 1, pp. 14 et 18 ; N = nombre de paires indépendantes ; approximation) ».

Qualité de l'OCR du jour sur Fisher : texte courant correct, avec césures (« ade-quately », « varia-bility ») et fautes ponctuelles : « ρ » lu « p » ; « The weights. to be attached » (point parasite, p. 18) ; « fron n—3 » et « n—2"/ aso » à la p. 14 ; « (p. 358) » lu « (p. 338) » p. 15. Formules illisibles ou fausses : éq. (V) p. 7 (« ep ==tanh¢ / y= tanh z »), éq. (VI), Table I p. 26 (« g == tanh ‘r= 5 (log 1+ — log 1— 1) ») et formule exacte p. 27 (« z = ½(log_e 1+r − log_e 1−r) » en lambeaux). Chiffres : l'exemple III de la p. 15 est faux dans l'OCR : « 0.6980 » pour 0,6930 et « 20,1488 » pour ± 0,1438. Aucun chiffre ni aucune formule de Fisher ne doit donc être pris dans l'OCR. Les citations retenues (pp. 5, 7, 10, 14, 18) sont retrouvées mot pour mot dans l'OCR (sauf la césure des lignes) : « could be reduced … », « is therefore sufficiently normal … », « This may be obtained … », « be attached to values of z … », « hypothetical infinite Gaussian population … », « The standard deviation is independent of » (suite « ρ » non retenue). La citation « the true curve in z is slightly leptokurtic » (p. 12) est présente.

## Point 3 — SHOGEN-POOLEE-SOURCE-1 : sources du poolé

| Pièce | Par nom de fichier (`biblio/`, `scratch/biblio-a-verser/`) | Par `biblio/INDEX.md` | Verdict |
|---|---|---|---|
| Mantel & Haenszel 1959 | aucun fichier ; aucune correspondance sur « mantel », « haenszel », « cmh » | aucune ligne | absente |
| Cochran 1954 | aucun fichier ; aucune correspondance sur « cochran » | aucune ligne | absente |
| Agresti 2013, « Categorical Data Analysis », 3e éd. | `scratch/biblio-a-verser/2026-09-29/agresti-2013-categorical-data-analysis-3e.pdf` (sha256 `8b322914aa8a3ac33fa2bcb999f2571cadf103d408763fb4acd8e8d8c24e8e1e`, recalculé = celui de `SHA256SUMS.txt` du dossier ; 742 pages) et son `.ocr.txt` ; copyright « © 2013 by John Wiley & Sons » (OCR, p. 6 du fichier) | aucune ligne (recherche « agresti », « mantel », « cochran », « cmh » : zéro occurrence dans les 328 lignes) | présente dans `scratch/`, hors `biblio/`, hors INDEX |

Note : d'autres pièces Agresti sont dans `scratch/biblio-a-verser/2026-09-29/` (diapositives 2016, `agresti-site/`, recension Neves 2014) ; ce ne sont pas Agresti 2013. Je n'ai pas cherché Mantel-Haenszel ni Cochran à l'intérieur d'autres documents ; la demande portait sur noms de fichier et INDEX.

Statistique de Cochran-Mantel-Haenszel dans Agresti 2013 [lu, repérage] : §6.4.2 « Cochran–Mantel–Haenszel Test of Conditional Independence », p. 227 du livre (page 245 du fichier PDF ; l'OCR marque la même page « 245 »). L'éq. (6.6) y définit la statistique, avec un attribut à Mantel & Haenszel (1959) (variance hypergéométrique) et à Cochran (1954) (variance binomiale, version Cochran), puis le nom commun. Citation unique, exacte dans l'OCR : « Cochran (1954) proposed a similar test statistic. » (p. 227). La §6.4 commence p. 225 (table des matières : « 6.4 Mantel-Haenszel and Related Methods for Multiple 2 x 2 Tables, 225 ») ; la version généralisée est §8.4.3 (non lue).

Qualité de l'OCR sur ce passage : texte identique au scan ; les formules (6.6) et les variances sont en lambeaux (indices, fractions) ; le tiret long remplace le tiret demi-cadratin dans « Cochran—Mantel—Haenszel ». Repérage seulement : le contenu mathématique de (6.6) n'est pas à reprendre de l'OCR.

## Limites

- La vérification numérique du Thm 3.1 porte sur une série simulée et sur le cas w_n = 1 ; elle contrôle ma lecture de (3.6)-(3.9), pas le théorème en général.
- Je n'ai pas lu Priestley 1981, Carlstein 1986, ni aucune source citée par Künsch ; l'attribution « Bartlett » reste sans source dans le dossier lu.
- L'échelle des γ̂_k de la règle (somme ou moyenne) n'est pas fixée par le texte du pt 3 que j'ai lu ; je n'ai pas ouvert le code (r1.py). À confirmer.
- Fisher : le fichier d'archive porte en page 1 une « Author's Note (CMS 1.2a) » et un passage de tête d'introduction qui ne sont pas du texte de 1921 (note rétrospective de l'archive, non datée sur la page) ; je n'en tire rien. Non lues sur le scan : pp. 20-25 de Metron (fichier 19-24) et pp. 29-32 ; seul repérage par OCR.
- Les pages 1 (Fisher, note d'auteur) et 2 (début de l'introduction) du fichier sont sans numéro de Metron imprimé visible ; la correspondance Metron = fichier + 1 est déduite des en-têtes des pp. 3-17 et 25-27 du fichier.
- Agresti 2013 : une seule page (245) lue sur le scan ; le reste est repérage par OCR.
