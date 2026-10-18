# Brief de correction — lot GEL-COLLECTEUR-1, après le rapport du générateur (2026-10-18 02:29:12 UTC, `date -u`)

Même worker, même dossier `<scratchpad>/s2bis/gel/`, mêmes règles que `BRIEF-GEL.md` (dépôt réel `/home/user/shogen` en lecture seule ; toute commande git qui liste ou compare des chemins est limitée à une liste explicite de chemins ; `python3 -I -B` ; aucun réseau ; nettoyage des copies lourdes).

Adjudications :
- **Q-1** (fichier `<observateur>-<jour>.armement` au dépôt) : accepté.
- **Q-2 (TSA)** : erreur du brief (E45 de l'orchestrateur). Décision de l'investisseur du 2026-10-08 : horodatage chez Certigna (`docs/adr-0028/ANNEXE-B-items.md` l.1325 ; `docs/adr-0029/g0-collecte/G0-COLLECTE-RECALC-DEPLOI.md` l.44-46 : URL et authentification = acte extérieur dû avant DB-3). **Correction C-1** : retirer `https://freetsa.org/tsr` ; le champ `tsa` d'`observateurs.json` devient facultatif et **absent au gel** ; `jeton` refuse `--envoi` quand aucune `tsa` n'est scellée (refus nommé, sortie 2) et refuse toujours une URL différente de la `tsa` scellée quand elle existe ; la règle `tsa-https` reste pour le jour où l'URL sera scellée (DB-3), et toute mention de FreeTSA dans tes diffs est remplacée par « TSA scellée à DB-3 (Certigna, acte extérieur) ». FORMAT et METRIQUES ajustés.
- **Q-3** (`--observateurs` obligatoire, refus `CONFIG/observateur`) : accepté.
- **Q-4** : **Correction C-2** : verser `s2bis/config/carte.json` de production (à produire), carte vide (`formes` : []), paramètres cohérents avec `formes.json` (règles croisées d'`entree.py` l.110-125), test qui le charge par `configurer_secondaire` ; paquet : phrase « carte vide au gel, sources après le rendu ».
- Volet « délais de `resolv.conf` » de SHOGEN-S2BIS-CONFIG-PRODUCTION-1 : re-daté DB-2, texte de l'item à proposer au rapport ; volet TSA : re-daté DB-3.

Livraison : `diffs/GEL-7.diff` réécrit (C-1) et `diffs/GEL-9.diff` neuf (C-2, à produire) appliqué après GEL-6 ; les huit autres diffs inchangés sauf si C-1 l'exige (dis-le) ; ordre d'application final écrit au rapport ; plancher exact relevé ; mutants pour C-1 ; suite et matrice revertes sur une copie neuve ; `RAPPORT-GENERATEUR.md` et `SHA256SUMS` mis à jour.
