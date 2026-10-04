# G0 des lots d'après S2 (2026-10-04)

Rattachement : ADR-0028 D9 (bifurcation après J28, branche « (i) faux » : priorité G4 et révision de doc 04), D6 (v)-(vi),
D10 ; directive de l'investisseur du 2026-10-04 (JOURNAL, verbatim) ; avis d'un advisor frais
`docs/adr-0028/AVIS-PRODUIT-APRES-S2.md` (écrit le 2026-10-04). Créé le 2026-10-04 02:38:15 UTC (heure produite par le script d'écriture).

## Lots (liste fermée ; chacun reçoit son propre G0 détaillé avant tout code)

| lot | objet | dépend de | qui |
|---|---|---|---|
| **R-S2** | rapport `docs/11-mesures-pilotes.md` → validateur → cp-2 → G7 → clôture de S2 | exécution unique (faite) | rédacteur frais, validateur, orchestrateur |
| **G4-RECHERCHE** | notaire tiers (doc 17 T-01, F-DP-35, PX-Shogen-3) : options, coût, intégration, risques ; aucune dépense | — | lecteur `claude-sonnet-5-5`, puis advisor |
| **DOC04-REV** | révision de doc 04 à la lumière de S2 : k_eff côté livraison, A(window-dependence), définition d'écart à quorum d'observateurs (si S2-bis), registre doc 09 | rapport R-S2 | rédacteur frais, validateur |
| **ADR-S2-BIS** | ADR de campagne : observateurs multiples (≥ 3, ASN et résolveurs distincts), écart à quorum, exclusion de dégradation ex ante, statistique d'événements ou ℓ et puissance (FIV de S2 en a priori), Pyth réglé ex ante, τ re-dérivé et scellé, pré-enregistrement (ADR-0028 annexe D) | clôture S2 ; acte budgétaire de l'investisseur | rédacteur, advisors, validateur |

Hors lots, par construction : « benchmark continu » (déclencheur D6 (vi) non atteint : « R1 discrimine » FAUX) ; S4
(conditionné à D9 (i) et (ii)). Décisions de valeur posées à l'investisseur : arrêt de la collecte S2, financement de
S2-bis, publication (G9), envergure (§4.7).
