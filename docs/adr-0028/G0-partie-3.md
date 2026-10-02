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
