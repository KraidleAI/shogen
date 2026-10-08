# Partie 3 de S2 — G0 courts par étape (orchestrateur de la session cloud)

Rattachement : `docs/adr-0028/PLAN-PARTIE-3.md` ; ADR-0028 D2, §1 bis, annexes A, B, C, D. Chaque section est
datée ; une section écrite ne se réécrit pas.

## P3 — lot de code court avant la rédaction (2026-10-02 14:1x UTC)

- **Items** (annexe B) : SHOGEN-SCEAU-VERIFY-CHEMINS-1 (l.391) ; SHOGEN-SENS-PLAGES-2 (l.343) ;
  SHOGEN-CONTEXTE-MUTABLE-1 (l.357) ; SHOGEN-RENDU-RENAME-POSIX-1 (l.413) ; SHOGEN-RENDU-STATUS-HEAD-1 (l.435) ;
  SHOGEN-GO-PICKAXE-1 (l.436). Motif de les faire ici : tous sont dus « au G0 du PAQUET » ou au premier G0 qui
  touche le code ; le paquet scelle le commit d'analyse final, qui doit les porter.
- **Décisions de l'orchestrateur (constructions)** :
  - SCEAU-VERIFY-CHEMINS-1 : `scripts/sceau/verify.sh` et `make-tsq.sh` s'accordent sur une seule convention de
    chemins du manifeste `PAQUET.sha256` (chemins relatifs à la racine du dépôt, relus depuis la racine) ; sonde
    du worker de la partie 2 (`docs/G1-partie-2-etape-C-1.md`, L1) transformée en test reproductible (dépôt
    jetable, autorité de test locale, aucun réseau).
  - SENS-PLAGES-2 : lignes de week-end accordées au nombre de plages (singulier pour une, pluriel nombré sinon),
    comme SENS-PLAGES-1 ; épingles inchangées (une seule plage dans les fixtures épinglées), sinon re-capture
    justifiée.
  - CONTEXTE-MUTABLE-1 : le contexte nommé devient non modifiable par construction (fabrique qui rend un contexte
    neuf à chaque usage, ou objet figé), valeurs identiques ; test qui tente une affectation.
  - RENDU-RENAME-POSIX-1 : le renommage final refuse si la cible existe au moment du renommage (création
    exclusive de la cible ou contrôle atomique équivalent) ; test qui pose un répertoire vide entre le contrôle et
    le renommage.
  - RENDU-STATUS-HEAD-1 : la garde (2) juge l'arbre de travail contre le commit résolu, pas contre le HEAD courant.
  - GO-PICKAXE-1 : la voie (b) date le go par le premier commit dont `JOURNAL.md` porte une **ligne** contenant le
    sha256 entier (pas une sous-chaîne quelconque).
- **Tests** : tests d'abord, échec montré, une mutation par test ; règle scellée identique (`ea3a2d94…`) ;
  épingles ; suite verte (départ 376) ; `xtask verify` VERT ; fixtures seulement (D.4 a).
- **Taille** : ≤ 200 lignes par sous-lot ; coupe par item si besoin.

## S — niveau près de la garde (SHOGEN-CRITERE-GARDE-NIVEAU-1) (2026-10-02 14:3x UTC)

- **Source** : annexe B l.305 ; ADR-0028 §1 bis.1 pts 7 et 11 (« approximation normale à la garde ») ;
  `docs/adr-0028/G0-lot-SIM-NIVEAU.md` (générateur, graine, cas, sortie) ; `scripts/sim/`.
- **Construction** : prolonger le générateur de SIM-NIVEAU (même modèle nul, même code de calcul que la règle via
  l'oracle `sim_niveau_oracle_r1.py`, même discipline de graine) à des strates de n·P̂(1 − P̂) entre 10 et 30
  (cas nommés et fixés **à l'aveugle**, sans aucune donnée de campagne, avant toute exécution, avec motif) ;
  mesurer le niveau de z_s seul et de la règle, avec l'erreur-type de Monte-Carlo de chaque cas ; sortie versée
  sous `docs/adr-0028/sim-niveau/` (fichier neuf, sha256 au `SHA256SUMS` du dossier).
- **Conséquence pré-déclarée** (§1 bis.1 pt 7, même principe) : la sortie ne modifie ni ℓ, ni le seuil, ni la
  règle ; elle est imprimée au paquet avec ses erreurs-types ; un niveau mesuré au-dessus de 0,01 devient une
  limite écrite au paquet, jamais une révision.
- **Tests** : bit-identité de deux exécutions à la même graine ; oracle (4) inchangé ; Python 3.12+ (`math.sumprod`).
- **Exposition** : le worker atteste n'avoir vu aucune donnée de campagne (D.3).

## R — rédaction du PAQUET (2026-10-02 15:4x UTC)

- **Pièce** : `docs/adr-0028/PAQUET-PREREG-S2.md` (chemin de l'annexe A, ligne PAQUET). Rédaction par un **rédacteur
  frais** (`shogen-worker`, instance neuve), sans accès aux pièces de D.2 (liste fermée, points 1 à 11), avec
  attestation écrite D.3 ; validation par un **validateur frais** (`shogen-validateur`, `claude-fable-5-1`) ;
  contrôle non-LLM FM-1.1 des transcriptions des deux (chemins et motifs de D.2) par l'orchestrateur.
- **Plan imposé du paquet** : (1) mesures et commits (D2 pt 1 ; commits des lots de l'annexe A, partie 1 à 3) ;
  (2) D1, forme formelle ; (3) D5 ; (4) strate poolée stratifiée, exploratoire, famille de Bonferroni (D2 pt 4),
  source par l'état de `biblio/` (SHOGEN-POOLEE-SOURCE-1, clause C-6 : Agresti 2013 §6.4.2 versé et lu ; Mantel &
  Haenszel 1959 et Cochran 1954 absents) ; (5) D3 ; (6) D4 et segment J28 (D2 pt 6) ; (7) liste fermée des
  sensibilités (§1 bis.2) ; (8) inventaire D.1, par renvoi daté et sha256 de l'annexe D ; (9) contrôle système et
  exécution unique (D.4 a-c, gardes (1)-(6), EX-E1-1, procédure : tentative échouée sans sortie = ligne de JOURNAL,
  pas une seconde exécution) ; (10) **règle SHOGEN-CRITERE-R1-1**, recopie de §1 bis.1 pts 1 à 11 avec : clause C-7
  appliquée (Künsch 1989 versé et lu : poids du Thm 3.1 éq. (3.9) p. 1224, consistance = corollaire 3.1 p. 1226
  sous les conditions du Thm 3.3 p. 1225 ; SHOGEN-PT7-ATTRIBUTION-1), normalisation des γ̂_k en sommes
  (SHOGEN-PT3-NORMALISATION-1), limite du biais de Bartlett au pt 11 (SHOGEN-BARTLETT-BIAIS-1), lecture (a) du
  pt 10 (SHOGEN-CRITERE-PT10-CLAUSE-1), sorties de SIM-NIVEAU et de l'étape S citées avec leurs erreurs-types et
  le blob de `r1` mesuré (SHOGEN-SIM-R1-DERIVE-1, SHOGEN-CRITERE-GARDE-NIVEAU-1) ; (11) traitements de l'annexe D.5
  (descriptifs) ; (12) **limites et procédures écrites** dues par l'annexe B : RAW-FIN-1, ENREG-G1-1,
  ENREG-DELAI-CHAMP-1, CENSURE-VIVANT-PORTEE-1, RENDU-TABLE-REELLE-1, RENDU-CLI-REPORT-1, RENDU-JETON-MAIN-1,
  RENDU-ORC-OCTETS-1, RENDU-RENAME-FENETRE-1, GO-PICKAXE-FUSION-1, AXES-SIGMA-NUL-1, PAQUET-ERRATUM-FISHER-1 (avec
  SHOGEN-FISHER-SE-1), TAU-REDERIV-1, CENSURE-INFO-1, SEG-DEMARRAGE-1, limite « sceau privé » (D.4 c) ; (13) bloc
  machine `shogen-paquet-v1` (format du G0 §C de la partie 2).
- **Décisions de l'orchestrateur** :
  - EX-E1-3 : **non** — l'étendue des écarts du contrôle d'horloge n'entre pas au bloc 1 (aucun code après le gel
    du commit d'analyse) ; limite T-17 écrite au paquet (contrôle consigné, jamais bloquant).
  - EX-E1-2 : les sha256 complets des trois journaux scellés et du fichier de sommes entrent au bloc machine ; ils
    ne sont que sur le poste local (seul `control.jsonl` est au dépôt) : **acte de l'investisseur** (fichier de
    sommes de clôture), avant le remplissage du bloc.
  - Bloc machine : rempli par l'orchestrateur après la validation du texte, valeurs recalculées par commande
    (non-LLM) et vérifiées par `rendu_unique.py --gardes-seules` sur fixture ; le validateur valide le texte et le
    format du bloc, pas ses valeurs (déclaré au paquet).
  - SHOGEN-COLLECT-PREVWS-1 : **non qualifiable en session cloud** (sa définition est dans la dimension campagne de
    la cartographie, pièce D.2 n° 3, poste local) : limite écrite au paquet (item hors règle, sans effet connu sur
    la règle scellée, requalification après S2) ; écart au déclencheur de l'item, consigné au JOURNAL.
  - SHOGEN-ATTEST-ADVISOR-1 : **re-consultation impossible** (instances d'advisors du 2026-09-29, session
    locale) : leurs expositions connues sont de classe M (annexe D.1, lignes 3, 4, 11) ; limite écrite au paquet
    (attestations manquantes, classe R non exclue par attestation, exclue par l'inventaire) ; consigné au JOURNAL.
- **Gel** : le commit d'analyse final est celui de la tête de `partie-3-paquet` au moment du remplissage du bloc ;
  tout changement de code après ce point refait le bloc.
