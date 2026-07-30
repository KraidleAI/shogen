# Shōgen — vocabulaire interdit (v1, 2026-07-30)

> Registre de formulations interdites, sur le modèle du registre Kraidle :
> chaque entrée porte la formulation fautive, pourquoi elle ment, et la
> formulation correcte. Une formulation retirée d'ici exige une décision
> explicite. La gate S-G4 (DEVOPS §3) mécanisera cette liste.

## Héritées de la discipline (rappel)

Les trois mots d'assurance — *proven / tested (avec compte d'itérations) /
reviewed (qui, quand)* — et l'interdit sur *verified, validated,
guaranteed, ensures, safe* comme qualificatifs d'assurance, hors citation
verbatim et hors nom de calcul (« vérifier une signature » = calcul,
licite ; « donnée vérifiée » = surclamation, interdit).

## Propres à Shōgen

| interdit | pourquoi c'est un mensonge | on écrit à la place |
|---|---|---|
| « quorum de k sources **diverses** » (sans rangs) | confond déclaré et mesuré — la leçon K&L §4 / L&M p. 1603 | « quorum k_eff=…, axes R1/R2 mesurés : …, axes R3 déclarés : … » |
| « sources **indépendantes** » | l'indépendance ne s'observe pas, elle se teste ; même mesurée, elle n'est jamais établie — seulement non-rejetée sur des axes nommés | « sources sans co-défaillance détectée sur [fenêtre], sans recouvrement constaté sur [axes] » |
| « le certificat **garantit** l'indépendance » | le certificat rapporte des mesures ; A(axis-coverage) est indéchargeable en général | « le certificat rapporte k_eff, les mesures R1/R2 et leurs axes ; hors axes, rien n'est dit » |
| « **fait signé** » | l'attestation couvre les octets du dire ; le fait est produit par un typeur, testé jamais prouvé — personne ne signe un fait | « témoignage attesté, typé en fait (typeur identifié) » |
| « donnée **vraie** / prix **correct** / la source **dit vrai** » | la ligne fondatrice : l'attestation prouve le dire, jamais le vrai ; le quorum confine, il n'exactifie pas | « valeur admise dans l'enveloppe du quorum effectif, sous [résidus] » |
| « niveau de sécurité du lot » (agrégat) | les résidus de transport ne se moyennent pas — la règle des trois latences transposée (ADR-0001) | la liste des résidus, par témoignage |
| « k sources » (quand k_eff < k) | le nominal ment dès qu'une partition R2 fusionne des membres | « k nominal, k_eff mesuré » — k_eff en tête (04 §3) |
| « l'historique **prouve** l'absence de dépendance » | un z non significatif n'est pas une absence ; en dessous du seuil d'historique le certificat dit « historique insuffisant » (04 §2) | « le modèle d'indépendance n'est pas rejeté sur [n fenêtres, axes] » |
| « personne ne mesure l'indépendance » (et variantes) | faux depuis 1985 — l'homme de paille que LPS 2001 interdit ; le geste générique est occupé (06 §1) | le claim rescopé de 06 §1, avec son périmètre |
| « diversité **imposée** donc sûre » | SQA impose par étiquettes ; K&L/L&M : l'organisé n'a pas produit l'indépendance — seule la mesure convertit un axe en évidence | « axe imposé [nom], poids mesuré : [R1/R2 ou “non mesuré”] » |
| « attestor décentralisé » (pour un pool non compté) | la décentralisation non comptée dans la diversité est le mirroring possible (Chainlink v1) ; les attestors sont un axe R2 (ADR-0004) | « n attestors, comptés dans la partition R2 » |

## Règle d'application

Toute phrase sortante (doc, README, commit, réponse, benchmark public)
se relit contre cette table. Un terme trouvé fautif dans un document
committé se corrige **en classe** (tous les sites, même passe — règle
mécanique héritée), et s'il a résisté à une relecture, il entre ici avec
sa cicatrice.
