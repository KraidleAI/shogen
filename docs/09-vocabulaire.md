# Shōgen — vocabulaire interdit (v3, 2026-08-13 ; v2 2026-08-12 ; v1 2026-07-30)

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
| « Shōgen évalue la qualité d'une source » / « nos sources sont bonnes » | la qualité d'un marché (profondeur, liquidité) est hors périmètre (ADR-0007) ; nous mesurons une *relation entre* sources, pas la valeur de l'une | « k_eff = …, amonts nommés : … — leur profondeur n'est pas mesurée ici » |
| « attestor décentralisé » (pour un pool non compté) | la décentralisation non comptée dans la diversité est le mirroring possible (Chainlink v1) ; les attestors sont un axe R2 (ADR-0004) | « n attestors, comptés dans la partition R2 » |

## Propres à l'ingénierie (S2.5, 2026-08-12 — proposées par les ADR-0009 à 0013, adjugées par l'orchestrateur)

| interdit | pourquoi c'est un mensonge | on écrit à la place |
|---|---|---|
| « le vérificateur est **sûr** parce qu'il est en Rust » / « Rust **garantit** la sûreté mémoire de notre code » | ce qui est machine-checked (Jung et al. 2018) est un langage formalisé — ni `rustc`, ni la stdlib, ni notre code ; A(toolchain-soundness) reste au registre | « cœur et vérificateur posés `forbid(unsafe_code)` ; la preuve RustBelt porte sur un langage formalisé, pas sur notre code » |
| « le cœur **ne peut pas paniquer** » / « la totalité **garantit** l'absence d'erreur » | S-G3 est lexicale : elle rejette des formes nommées, elle n'atteint ni le débordement, ni une panique de dépendance (ADR-0010, coûts pt 6) | « S-G3 verte (formes nommées rejetées) ; l'absence de panique n'est pas établie — bornée par tests de propriété et fuzz » |
| « couverture élevée **donc** suite efficace » / une couverture-cible | l'artefact détenu qui la mesure conclut « should not be used as a quality target » (Inozemtseva & Holmes) | « couverture X % (garde-fou de sous-test, seuil candidat) ; le validateur de la suite est le score de mutation » |
| « le score de mutation **prouve** que la suite détecte les fautes » | le coupling effect est déclaré empirique par ses auteurs (« no hope of "proving" », DeMillo p. 35) — A(coupling-effect) au registre | « suite *tested* : N mutants, M tués, K survivants justifiés, [date] » |
| « mutant semé » sans son registre | trois registres qui ne se confondent pas : mutant de gate (test négatif d'outil), mutant de programme (seul à produire un score), octet muté du lot (test négatif de données) — ADR-0011 pt 4 | le registre nommé : « mutant de gate », « mutant de programme (score) », « octet muté du lot » |
| « build **reproductible** » (qualificatif nu) | sans compte de rebuilds ni jeu de variations, c'est une intention ; 6 variations valident moins que les 30+ de Debian et ça se dit (ADR-0012 D6) | « rebuild identique sous [n] variations, [k] exécutions, plateforme [x] » |
| « chaîne d'approvisionnement **sécurisée** » | « Point solutions … cannot guarantee the security of the entire chain as a whole » (in-toto) ; nos mesures sont par étape | la liste des contrôles en place, et ce qu'ils ne couvrent pas |
| « SLSA niveau N » (sans propriétés de plateforme établies) | le niveau dépend de propriétés de la plateforme de build qu'aucune pièce détenue n'établit (ADR-0012) | « provenance attestée par [plateforme] ; niveau SLSA non établi sur pièce » |
| « CI verte **donc** code correct » / « gate verte donc conforme » | une gate verte n'atteste que ce que ses mutants semés ont montré (ADR-0013 pt 2) ; hors corpus, elle ne dit rien | « gate S-Gx verte, n mutants semés tués le [date] » |

## Propres au transport S3 (2026-08-13 — proposées par ADR-0015, adjugées par l'orchestrateur)

| interdit | pourquoi c'est un mensonge | on écrit à la place |
|---|---|---|
| « preuve publiquement vérifiable » (nue) | le projet amont lui-même : « You don't get public verifiability and zero trust at the same time » — la portabilité s'achète par un notaire | « attestation portable, vérifiable par quiconque fait confiance à la clé du notaire [identité] » |
| « transport vérifié par shogen-verifier » | en forme β le vérificateur contrôle la liaison hash→preuve, pas la cryptographie de la preuve (ADR-0015 pt 8) | « liaison hash→preuve contrôlée par shogen-verifier ; contrôle cryptographique délégué à shogen-tlsn-verify [révision] » |
| « zkTLS trustless » / « transport sans confiance » | designated-verifier : « Every zkTLS protocol today is designated-verifier in this way. » | « designated-verifier ; portable sous confiance en [notaire] » |

## Règle d'application

Toute phrase sortante (doc, README, commit, réponse, benchmark public)
se relit contre cette table. Un terme trouvé fautif dans un document
committé se corrige **en classe** (tous les sites, même passe — règle
mécanique héritée), et s'il a résisté à une relecture, il entre ici avec
sa cicatrice.
