# Adjudication du lot LECTURE-SHOSTACK (SHOGEN-E1-METHODE-1, volet (ii)) — orchestrateur, 2026-10-15 20:27:12 UTC (`date -u`)

## Contrôles du rendu
- Gate 0 : transcript `agent-a181ee99daa556c6f.jsonl`, champ `model` : 96 occurrences, toutes `claude-sonnet-5-5` (attendu pour un lecteur).
- FM-1.1 : `scripts/controle/fm11.py` et `fm11-neuf/fm11.py` : `fragments_l51_l14` = {resultats: 0, entrees: 0} pour les deux.
- `SHA256SUMS` du dossier : OK pour les trois scripts et les pièces.
- Contrôle des citations rejoué par l'orchestrateur (`python3 -I check_citations.py <sidecar> quotes.tsv rejeu.tsv`) : 91 citations ; 91 oui ; 0 non ; le fichier rejoué est identique à `citations.tsv` (colonnes 1 à 7). Cible du rapport vérifiée : docs/17 fait 114 lignes (l.114 = ajout daté du volet (i)) ; `biblio/INDEX.md` fait 460 lignes, l.460 = rangée Shostack, cellule 7 « pas encore lu … », cellule 8 « tout, avant lecture ; … ».
- Pièces interdites : aucune ouverte (rapport §0 ; brief).

## Décisions
1. **Rapport ACCEPTÉ.** La phrase d'ajout daté (rapport §2) est adoptée mot pour mot, la date et le lot remplis à l'insertion (`date -u`, lot LECTURE-SHOSTACK) ; elle se place après la l.114 de docs/17, aucune ligne décalée (C-3). Les deux cellules de la rangée INDEX (rapport §4) sont substituées mot pour mot.
2. **Écarts (a) à (f)** : la table reste un choix de l'orchestrateur (en-tête de docs/17, ligne **Forme de la table**) ; aucun n'est repris dans le texte validé de docs/17 par ce lot. Ils deviennent des items de l'annexe B, propriétaire orch., déclencheur : prochaine révision de docs/17 (lot E1-METHODE-FORME, à former) : colonnes *type* et *traitement* (a, e), critères de sortie par grille STRIDE, par classe d'attaquant et par test (b, d, f), menace T-19 disponibilité (c), menace T-20 rétrogradation (ch. 16, cas à instruire sur le code du compagnon). Les numéros T-19/T-20 sont indicatifs (rapport §2 et §3).
3. **Question laissée par le lecteur** (table d'hypothèses de Shostack : « impact si faux », « qui répond ») : `docs/08-assumptions.md` n'a pas été lu par le lecteur ; item formé, à instruire au G0 du même lot futur, non tranché ici.
4. **Limites reçues** : ch. 9 (priorisation, p. 167-178) et annexe B non lus : la part « proportionnée au risque » de l'item reste sourcée par le ch. 7 seul ; inscrite comme lecture complémentaire (item), non bloquante pour la fermeture du volet (ii), dont l'objet (forme et couverture de docs/17) est rendu.
5. **SHOGEN-E1-METHODE-1 (ii) fermé** par cet ajout daté ; (i) l'était par DETTES-T14 (l.114).
6. Versement : pièces dans `docs/adr-0028/revue-lecture-shostack/` (rapport transcrit, cette adjudication, `citations.tsv`, `check_citations.py`, `SHA256SUMS`) ; annexe B (amendement daté, numéro dynamique) ; JOURNAL ; par `verser_shostack.py`, hors chaîne, sur arbre propre ; puis xtask (VERDICT seuls), docs-sha256sums, journaux-modele, commit, push.
