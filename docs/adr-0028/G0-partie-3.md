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
