# Contre-contrôle du lot <lot> (gabarit du lot GARDE-FOUS-ORCH, GF-9b)

Modèle résolu : `<identifiant exact>` ; base de la copie : `<sha de git rev-parse HEAD>` ; heures lues par `date -u`.

## Série rejouée diff par diff

| diff | appliqué sur le précédent | vérification (lignes de `gates.yml`, cible cargo par défaut) | verdict |
|---|---|---|---|

## Groupes de commit

Un diff rouge seul, vert avec un autre, forme un groupe avec lui : la chaîne commet le groupe en un seul pas. Ligne
fixe, lue par `avant_acte.py chaine` avant tout pas (erreur E11), une seule par rapport : `aucun` si chaque diff est
vert seul, sinon les groupes séparés par des points-virgules, les diffs d'un groupe joints par `+` (nom du fichier du
diff sans `.diff`), par exemple `GROUPES : FZ-x+FZ-i`.

GROUPES : aucun

## Verdict

CONFORME, ou NON-CONFORME avec les réserves R-n.
