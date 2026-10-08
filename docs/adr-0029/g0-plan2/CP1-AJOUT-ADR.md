# cp-1 bref — ajout daté à l'ADR-0029 accompagnant l'ajout au G0 de SIM-BIS (lot PLAN-S2BIS-2)

- **Gate 0** : modèle résolu `claude-fable-5-1`, effort `high` (validateur-humain, CLAUDE.md §7).
- **Heure** (`date -u`, lue avant toute lecture) : 2026-10-05 16:03:10 UTC. Dépôt lu à la tête `98c8537` (`git --no-optional-locks`) ; aucune opération git en écriture ; seul ce fichier est écrit.
- **Pièce jugée** : `…/plan2/inscription/AJOUT-ADR.md`, une ligne, sha256 `450202fd…cfd21d` [mesuré] ; 0 octet 92, 0 tabulation, un seul `2026-10-05 17:06:39 UTC`.
- **Rattachements lus [lu]** : ADR-0029 l.395-400 (fichier `b908842d…`, égal au commis) ; lettre v2 `…/plan2/LETTRE-AJOUT-G0-SIM.md` en entier (sha256 `f1629912…e628e` [mesuré] ; « L2 l.n ») ; G0 figé `…/plan2/inscription/G0-SIM-BIS.md` en entier (sha256 `a216a953…0e11e` [mesuré], 92 lignes) ; `…/plan2/inscription/HEURE.txt` ; mon rapport `…/plan2/CP1-AJOUT.md` ; G0 commis `docs/adr-0029/g0-sim/G0-SIM-BIS.md` (`d9cffc0a…`, inchangé). Hors liste, déclaré **E-1** : `…/plan2/inscription/G0-PLAN-S2BIS-2.md` en entier (« G0-P2 l.n »), parce que le texte ADR le cite et que sa dernière phrase (« une fois ») s'y rattache (adjudication 4) ; aucune autre pièce.
- **Attestation (forme D.3)** : aucune pièce de la liste D.2, aucun `*.jsonl`, aucun dossier interdit, aucune recherche récursive (`ls` non récursif de `…/plan2/inscription/`, `sed -n` et `diff` sur des fichiers nommés). Exposition : aucune valeur neuve ; aucune donnée de S2-bis n'existe.

## Verdict : ACCEPTE-AVEC-CORRECTIONS (C-1 à C-4, liste fermée)

Aucune décision de valeur (§3) : pas d'ESCALADE-INVESTISSEUR. Le point 4 (G0 figé) est conforme (§4).

## 1. Fidélité à la lettre v2

Remarque de numérotation : les « (2) » et « (5) » du texte ADR sont ceux de l'ajout de l.399, non ceux de la lettre ; ils résument tous deux le point (5) de la lettre v2 (L2 l.43-56, dont la phrase du fond de référence, C-3 du premier cp-1, L2 l.44-47), et empruntent à (1), (4) et (8) pour décrire C1. Le point (2) de la lettre (C2 inchangé, L2 l.31-32) est reflété par « C2 reste imprimé comme garde-fou ».

| segment du texte ADR | source dans la lettre v2 | constat |
|---|---|---|
| en-tête : G0 `docs/adr-0029/g0-plan2/G0-PLAN-S2BIS-2.md` ; ajout au G0 de SIM-BIS du 2026-10-05 15:05:43 UTC ; cp-1 « dans le dossier du G0 » | L2 l.19-22 ; G0 figé l.35 ; `HEURE.txt` ; G0-P2 l.3-8 | Chemins et heure égaux. « cp-1 de cet ajout » : l'antécédent est ambigu (l'ajout au G0 ou le présent ajout) : **C-4**. |
| « sans dépense ni jalon nouveau » | AV l.182 (cité au premier cp-1 §5) ; ADR l.395 inchangé | Vrai. |
| (2) fond de la cible au niveau C1, « calibré sur le groupement mesuré source par source … (FIV par hôte) » | L2 l.44-47 (fond de référence à C1 ; 10⁴ et bloc du paquet à C1) ; L2 l.23-30 (C1 = argmin Q₁ sur les FIV_u) | Fidèle. L'échelle aux trois niveaux et P-cible à C2 (L2 l.46-47) ne sont pas répétées : omission sans changement de sens, « C2 reste imprimé comme garde-fou » les couvre. |
| « déclaré borne haute du groupement propre » | L2 l.36-40 : « déclaré borne haute du groupement propre, **par hypothèse** … Ce sens n'est pas démontré pour la durée » ; L2 l.69 (8)(ii) : au bord, « borne haute » ne s'applique pas | Le qualificatif « par hypothèse » est retiré ; dans l'ADR, document que l'investisseur lit, la phrase se lit comme un fait établi : **C-2**. Le cas du bord est couvert par la dernière proposition de (5). |
| (5) « durée retenue = maximum de 16 semaines et de W*(C1) » | L2 l.43-44 | Fidèle. |
| « A-2 est posé si, et seulement si, W*(C1) ou W*(C0) dépasse 16 semaines, jamais sur W*(C2) seul » | L2 l.47-48 : « si, et seulement si, W*(C1) > 16 ou W*(C0) > 16, **ou si aucune durée de l'échelle ne tient (a) à (c) à l'un de ces deux niveaux** (§3 pt 4) ; jamais sur W*(C2) seul » | **Changement de sens** : avec « si, et seulement si », le texte ADR exclut A-2 quand aucune durée de l'échelle ne tient à C1 ou à C0 (W* inexistant), cas où la lettre et PROP §3 pt 4 (l.241-243) le posent. L'ADR serait plus étroit que le G0 sur une question à l'investisseur : **C-1**. |
| « un critère de bord pré-déclaré écrit la limite si C1 tombe au bord de la grille » | L2 l.69-72 | Fidèle (résumé). |
| « PLAN-S2BIS-2 précède E0 de SIM-BIS dans tous les cas » | L2 l.73-74 (9) ; l.65-66 (7) | Fidèle ; remplace à bon droit « précédé du lot PLAN-S2BIS-2 si la durée dépend du niveau de calibration » (l.399 pt 5). |
| « ses journaux ne sont lus que par ses scripts épinglés, une fois » | hors lettre v2 ; G0-P2 l.16 (adjudication 4 : « deux passes A et B dans un seul lancement … lancés une fois par l'orchestrateur ») ; ADR l.383 | Ajout hors des points (2) et (5), de sens juste mais de lettre fragile : « ses journaux » désigne par la grammaire les journaux de PLAN-S2BIS-2, alors que ce sont les journaux scellés de S2 ; « lus … une fois » peut se lire contre les deux passes A et B du G0 du lot : **C-3**. |

Omissions sans changement de sens (admises pour un ajout d'ADR, forme de l.399) : le contenu de la question A-2 (trois W*, phrase de (4), 20 % sous H0, phrase de (8)), le cas W*(C0) > 16 ≥ W*(C1) écrit en clair, la phrase de limite nommant C2, la règle « sans question » de (8)(iii). Tout cela reste au G0 de SIM-BIS (L2 l.49-56), que le texte ADR cite par son heure.

## 2. Justesse comme modification des points (2) et (5) de l.399

- **Pt 2** (l.399 : « fond de la cible calé sur S2 (f = 0,3, composante propre ε_u = (1 − f)·p̂_u, écrite au paquet), groupement au niveau C2, scénario L = 20 imprimé à côté ») : le texte ne touche que « groupement au niveau C2 » → C1 ; f = 0,3, ε_u et L = 20 restent, comme la lettre (L2 l.44-47) le veut. Juste.
- **Pt 5** (l.399 : « plancher de 16 semaines ; au-delà, acte de l'investisseur (A-2), précédé du lot PLAN-S2BIS-2 si la durée dépend du niveau de calibration ») : le plancher est conservé (max(16, ·)), la condition de A-2 est rendue explicite, le « précédé … si » devient « précède E0 dans tous les cas ». Juste, sous C-1.
- Forme : l'ajout vient après l'ajout du 23:02:56 (l.399), comme les ajouts précédents (l.397, l.399) ; « l'ajout précédent change en deux points » désigne sans ambiguïté celui de l.399. La formule « Le texte des lignes citées reste tel quel » de l.399 n'est pas répétée : rien n'est cité à la ligne, donc sans objet.

## 3. Décision de valeur cachée ?

Aucune. Pas de dépense (G0-P2 l.18 ; AV l.182), aucun jalon de l.395 modifié, aucune déclaration publique. A-2 reste une question à l'investisseur ; son déclencheur est une règle technique déjà adjugée au G0 de SIM-BIS (ajout du 15:05:43, (5)) après le premier cp-1. C-1 importe précisément parce que l'ADR est le texte que l'investisseur lit : la règle y doit être la même qu'au G0, ni plus large ni plus étroite.

## 4. G0 figé (`inscription/G0-SIM-BIS.md`)

[mesuré] : (a) l.1-33 identiques, octet pour octet, au G0 commis `d9cffc0a…` (`diff` : seule différence, la ligne vide 34, séparateur de même forme que la l.32) ; (b) l.35-92 identiques à la lettre v2 l.19-76 après retrait du préfixe « > » et substitution de `<date>` par « 2026-10-05 15:05:43 UTC (heure produite par le script d'écriture) » (`diff` vide) ; la parenthèse est la forme de la l.3 du G0 et de B.61 ; (c) `HEURE.txt` = « 2026-10-05 15:05:43 UTC », égal à la l.35 ; (d) 0 octet 92, 0 tabulation, fin de fichier par saut de ligne. **Conforme : c'est la lettre v2, l'heure annoncée, et rien d'autre.** Je rappelle que la lettre v2 intègre C-1 à C-6 avec les choix de l'orchestrateur (C-2 : lecture « à chacun des ℓ retenus ≥ 60 » ; C-4 : série de I_t seule, sur T4 l.50 que je n'ai pas ouvert) ; (8) y reste identique à AV l.117 (L2 l.129).

## 5. Corrections demandées (liste fermée, lettres exactes)

- **C-1 — règle de A-2 complète.** Remplacer « A-2 est posé si, et seulement si, W*(C1) ou W*(C0) dépasse 16 semaines, jamais sur W*(C2) seul » par « A-2 est posé si, et seulement si, W*(C1) ou W*(C0) dépasse 16 semaines ou n'existe pas sur l'échelle des durées, jamais sur W*(C2) seul ». Rattachement : L2 l.47-48 ; PROP §3 pt 4 (l.241-243).
- **C-2 — « par hypothèse ».** Remplacer « déclaré borne haute du groupement propre » par « déclaré, par hypothèse, borne haute du groupement propre ». Rattachement : L2 l.36-39 ; (8)(ii) L2 l.69.
- **C-3 — dernière phrase.** Remplacer « ses journaux ne sont lus que par ses scripts épinglés, une fois » par « les journaux scellés de S2 ne sont lus que par les scripts épinglés du lot, en un seul lancement (G0 du lot, adjudication 4 ; l.383) ». Rattachement : G0-P2 l.16 ; ADR l.383.
- **C-4 — antécédent du cp-1.** Remplacer « cp-1 de cet ajout dans le dossier du G0 de PLAN-S2BIS-2 » par « cp-1 de l'ajout au G0 de SIM-BIS et du présent ajout dans le dossier du G0 de PLAN-S2BIS-2 (`CP1-AJOUT.md`, `CP1-AJOUT-ADR.md`) », si l'orchestrateur verse ce rapport dans `docs/adr-0029/g0-plan2/` ; sinon écrire le seul chemin vrai. Rattachement : G0-P2 l.8 ; L2 l.64.

## 6. Observations (non bloquantes)

- **O-1** : le texte ADR ne dit pas que la confirmation à 10⁴ réplications et le bloc `[VALEURS POUR LE PAQUET DE S2-BIS]` se calculent à C1 (L2 l.45-46) ; « le groupement du fond de la cible … au niveau C1 » l'implique (pt 2 de l.399 porte le fond de la cible). Admis tel quel.
- **O-2** : le G0 du lot figé (G0-P2 l.3) porte encore `2026-10-05 17:06:39 UTC` ; l'heure de ce G0 doit être postérieure à 15:05:43 UTC (ajout au G0 de SIM-BIS) et antérieure à l'inscription au JOURNAL du sha256 du code (L2 l.62-63), et la paire d'heures consignée comme (7) le demande.
- **O-3** : le mot « une fois » de G0-P2 l.16 (« lancés une fois ») et la lettre de Q-P2-08 adoptée (AV l.72 : « un seul lancement ; deux passes A et B ») sont cohérents ; C-3 aligne l'ADR sur cette lettre.

## 7. Ce que ce cp-1 ne fait pas

Il ne relit ni la proposition, ni l'avis, ni `PERIMETRE-REDUIT.md`, ni les diffs ; il ne vérifie pas T4 l.50 (C-4 du premier cp-1) ; il ne tranche aucune question technique. Il n'écrit que ce fichier.
