# Adjudication de l'orchestrateur — lot DETTES-T16 (BIBLIO-API), phase 1 (2026-10-15 10:45:32 UTC, `date -u`)

Contrôles avant lecture : Gate 0, 483 champs `model` du transcript, tous `claude-opus-5-5` ; FM-1.1 : 0 (deux outils) ; `SHA256SUMS` conforme ; `git apply --check` de DT16-a sur la tête du moment : passe.

## Décisions

- **Pièces** : les 8 pièces sont adoptées. Les trois pages de conditions non lisibles (Coinbase 403, Bitstamp défi Incapsula, Bitfinex rendue par script) restent « aucune licence lue » au registre, dans la forme de la règle en tête de l'INDEX.
- **Citation l.64 (OKX)** : coquille du chercheur (deux-points ajouté). Elle est corrigée au versement du rapport (lot DETTES-T2), par une retouche déclarée dans l'en-tête de la pièce transcrite, forme déjà employée pour la citation de Fisher. La l.40 (une espace) suit la même forme.
- **Encadrés d'OKX (§4)** : trouvaille adoptée. Un erratum daté est posé au versement du rapport : le [abs] du chercheur sur le fuseau d'OKX venait d'une copie incomplète ; la page détenue dit le fuseau UTC+8 et des bornes inclusives aux deux bouts. Ce point est porté à la G2 de DETTES-T16, qui dit s'il change une phrase de B.{DT2} de CALIB-FORMES-API-1 (le code lit déjà les mensuels en UTC+8 ; les bornes inclusives sont celles que le code suppose : à vérifier sur pièce par la G2).
- **Leçon de méthode** : « une copie par résumeur de fetch perd les encadrés ; un [abs] établi sur une telle copie n'est pas une absence » : au bloc daté de l'annexe B, et au bloc commun GF-20.
- **Conditions d'usage (signal 4)** : question de valeur pour l'investisseur, posée telle quelle au point d'étape : l'accord d'API d'OKX (§9.4) et la page de Bitstamp restreignent l'usage des données de marché, que CALIB-ACTIFS télécharge. Aucun acte avant sa réponse ; l'acquisition de CALIB-ACTIFS n'est pas lancée avant novembre.
- **`presg5.py` quadratique** (16 min sur la page OKX) : item SHOGEN-PRESG5-QUADRATIQUE-1, formé au versement ; déclencheur : le prochain lot qui touche `presg5.py` ou S-G5 (DETTES-T15 touche `sg5.rs` : le générateur de DT15 reçoit la question en phase 2).
- **SHOGEN-BIBLIO-COPIE-DURABLE-1** : étendu aux 8 pièces, précision d'item au versement.
- **[abs] de Coinbase et de Bitstamp** : capture à refaire ; item SHOGEN-BIBLIO-CONDITIONS-CAPTURE-1, acte de l'orchestrateur depuis un navigateur si le mandataire le permet, sinon acte de l'investisseur.
- **Écarts E-1 à E-8** : acceptés ; E-8 (parcours récursif de son propre dossier `tmp/target`) est dans son dossier, permis.

## Suite
- G2 neuve de DT16-a et des pièces (brief `g2/BRIEF-G2.md`).
- Versement privé des 8 pièces dans `biblio/` du dépôt : acte de l'orchestrateur après la G2, puis commit de DT16-a, puis versement de DETTES-T2 (`verser_d2.py`).

## Ajout daté du 2026-10-15 11:45:28 UTC (`date -u`) : adjudication de la G2 neuve

Contrôles : Gate 0, 496 champs `model`, tous `claude-opus-5-5` ; FM-1.1 : 0 (deux outils) ; `SHA256SUMS` conforme. Verdict ACCEPTE-AVEC-CORRECTIONS, C-1 et C-2 : **adoptées**. F-1 (retouche déclarée du rapport du chercheur, l.38, l.40, l.64, en-tête), F-2 (erratum daté OKX), F-3 (bloc B de `verser_d2.py`), F-4 (phrases de fermeture) : **adoptées telles quelles** ; mon adjudication du matin est nuancée comme la G2 le dit (le code est juste sous les deux découpages et ne suppose aucune borne inclusive pour OKX). S-1 (docstring d'`acquerir.py` l.81-82) : porté par l'orchestrateur au versement de DETTES-T2, forme de la G2, avec la mise à jour de `SHA256SUMS` de `scripts/calib-actifs/`. S-2 : ordre des actes suivi (DT16-a + C-1, versement privé, xtask, commit, d'un seul tenant), après la fin de la chaîne DB-1 (une seule chaîne à la fois dans l'arbre). S-3 : question des conditions d'usage portée à l'investisseur au point d'étape (citations de la G2 §5). Écarts : acceptés (chevauchement d'un xtask avec la chaîne, liste par motif sur un dossier de copie permis). Clôture sans passe 2 : les corrections sont des copies à l'octet de la G2.
