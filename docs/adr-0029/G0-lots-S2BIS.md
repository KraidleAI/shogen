# G0 des lots de S2-bis et du produit (première vague)

Écrit par l'orchestrateur le 2026-10-04 à 13:21:12 UTC (`date -u`), après l'acceptation d'ADR-0029 par l'investisseur
(JOURNAL, entrée de 13:18:44 UTC, verbatim). Rattachement : ADR-0029 révision 3 (§2.6 CALIB-ACTIFS, §2.9 collecte, §2.11 produit,
§6 lots et jalons) ; ADR-0028 (S2 close, `docs/adr-0028/G7-S2.md`) ; annexe B d'ADR-0028 (items cités par identifiant).
Règles communes : un G0 de lot complète celui-ci avant tout code (périmètre exact, tests attendus, sortie) ; G1 journal de
provenance ; G2 relecture neuve à 100 % ; seul l'orchestrateur committe ; R-25, R-13, R-8 ; aucune dépense ni compte créé sans
l'acte de l'investisseur (lot 7 d'ADR-0029) ; Pocket : aucun accès.

| lot | objet | sortie | lit des données de campagne ? | dépend de |
|---|---|---|---|---|
| **SG5-INTERDITS** | SHOGEN-SG5-NOTES-INTERDITS-1 (priorité haute) : la gate S-G5 n'imprime plus que `chemin:ligne` pour les dossiers interdits, test de non-régression | `xtask/` | non | — |
| **DOCS11-PUBLIC** | version publique filtrée de `docs/11` (décision de l'investisseur) : retirer pièces privées, chemins du poste local, références aux dossiers interdits ; garder les valeurs publiées et le verdict, registre doc 09 ; rien n'est publié sans le feu vert écrit de l'investisseur après lecture | `docs/publication/11-mesures-pilotes-public.md` (brouillon) | non (rapport validé seul) | — |
| **CALIB-ACTIFS-G0** | première étape de CALIB-ACTIFS (ADR-0029 §2.6) : trouver, pour ETH/USD, USDC/USD et USDT/USD, des historiques publics à une minute antérieurs à S2 pour au moins quatre places par classe, conditions d'usage lues ; lecture classe par classe (décision de l'orchestrateur sur avis de l'advisor) | `docs/adr-0029/calib/SOURCES-HISTORIQUES.md` | non | — |
| **PLAN-S2BIS** | ADR-0029 §6 lot 3 : données de S2 post-rendu, lectures inventoriées, au commit d'analyse `f35a70c` | G0 propre à écrire | oui (journaux scellés, par scripts) | S2 close |
| **SIM-BIS** | SIM-NIVEAU-BIS ‖ SIM-PUISSANCE-BIS (§6 lot 4), avec SHOGEN-FLUX-ABSORPTION-COLLECTIVE-1 et SHOGEN-FLUX-SERIEL-1 | G0 propre à écrire | non | PLAN-S2BIS |
| **COLLECTE-BIS ‖ RECALC-BIS** | §6 lot 5 ; SHOGEN-ENTRELACEMENT-D5-1 au G0 de COLLECTE-BIS | G0 propres à écrire | non (fixtures) | SIM-BIS |
| **DEPLOI-BIS** | §6 lot 6 | G0 propre à écrire | non | COLLECTE-BIS |
| **REJEU-DECROCHAGES ‖ ROOT-COUNT-V0 ‖ GOUVERNANCE ‖ SORTIES-MACHINE** | produit hors campagne (§2.11) ; ROOT-COUNT-V0 sur les rendus de S2, tout recalcul à `f35a70c` | G0 propres à écrire | ROOT-COUNT-V0 : rendus seuls | — |

Première vague (ce G0) : SG5-INTERDITS, DOCS11-PUBLIC, CALIB-ACTIFS-G0, en parallèle. Les autres lots reçoivent leur G0 avant tout
travail. Roster : workers `claude-opus-5-5` effort max ; lecteurs `claude-sonnet-5-5` effort high ; validateurs et advisors
`claude-fable-5-1`.

> *Ajout daté du 2026-10-04 17:55:06 UTC (item G2 I-G2-1 du lot DOCS11-EN)* : ligne de lot ajoutée après coup : **DOCS11-EN** — traduction anglaise fidèle du brouillon public du rapport de S2 (demande de l'investisseur du 2026-10-04 : « le rapport doit être en anglais […] pro et institutionnel ») ; sortie `docs/publication/11-pilot-measurements-public-en.md` (brouillon, non publié) ; ne lit aucune donnée de campagne ; contrôle par script (nombres, registre transposé, motifs, blocs recopiés), tests et mutants versés à `scripts/publication/en/`.
