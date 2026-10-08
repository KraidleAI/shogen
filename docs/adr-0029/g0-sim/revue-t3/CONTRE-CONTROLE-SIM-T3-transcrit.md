# Contre-contrôle des corrections de SIM-BIS tranche 3 (transcrit)

> Transcription par l'orchestrateur le 2026-10-05 10:05:09 UTC du rapport rendu par message par le réviseur G2 (agent a388ef21916294a7b) ; contrôle FM-1.1 du transcript : fragments_l51_l14 = 0. Texte du réviseur ci-dessous, sans retouche.

claude-opus-5-5

# Contre-contrôle des corrections de SIM-BIS, tranche 3 (SB-8D à SB-8G et patch ROTATION)

- **Gate 0** : `claude-opus-5-5`, effort max ; réviseur G2 de la tranche.
- **Horloge** (`date -u`) : 2026-10-05, de 09:29:07 à 10:04:07 UTC.
- **Redémarrage du conteneur** (vers 10:02) : il est survenu après la fin de tous mes travaux (dernier `FIN` à 10:00:41, sommes à 10:01). Les preuves sont intactes et aucun processus n'était à relancer.
- **Dépôt** : tête f5915a5, `git status --short` vide. Aucune opération git en écriture.
- **Pièces** : `corr/SHA256SUMS` (48edd0ed…), 189 sur 189 OK.
- **Preuves** : `<scratchpad>/s2bis/sim3/g2/rev/`, fichiers `cc-*` de `sorties/`, `outils/`, `notes-cc.txt` ; `SHA256SUMS` c24296b0…, 121 sur 121 OK.
- **Nettoyage** : copies, cible cargo et TMPDIR supprimés.

## Verdict : liste fermée d'un seul point, CC-1. Tout le reste est conforme.

**CC-1 (C-1, oracle à la frontière)**
- Le code de C-1 est juste, mais la borne « C_S ≤ seuil » de `oracle()` n'est fixée par aucun test.
- Mon mutant X-01 (« < » au lieu de « ≤ ») survit à la suite.
- Mon prototype `outils/proto_corrections_cc1.py` simule les deux modes par mock de `deux_modes` (R = 999, seuil 9). Sur le code livré, ses 4 cas passent : refus pour 9 contre 10 ; aucun refus pour 8/9, 10/11 et 9/9.
- Sous X-01, deux cas échouent : la faute 9 contre 10 n'est pas vue, et 8 contre 9 lève une fausse alerte.
- Demande : ajouter ce cas de frontière à T-REG-2, rouge sous X-01 et vert sur le code.

## Résultats, point par point

**1. C-1 à C-3 et mes mutants**
- **C-1** : la faute d'arrêt sur C_S de ma G2 (anticipé 6 contre complet 207) est désormais refusée, REGLE/oracle. Mes prototypes C-1 et C-2 passent tous sur l'état final (6 sur 6).
- **C-2** : V-02 et V-25 sont tués par `test_artefacts_consolides_e_s_21`, V-22 par `test_unites_series_nulles_e_s_28`, V-20 par `test_loi_des_absences_parametres`.
- **C-3** : je recompte 29 octets 92 dans 8 des 33 fichiers de `sim3/outils`, comme le nouveau rapport ; 0 ailleurs.
- **Mes 28 mutants**, rejoués par la commande du job (borne 300 s, 41 s au plus) : 28 tués, 0 FATAL.
- **V-10a et V-12a** sont fidèles : « : » admis dans les noms d'unité, et « > » au lieu de « ≥ » pour C. Mes réécritures indépendantes V-10b et V-12b sont tuées aussi.
- **Mutants en plus** : X-02 à X-09 (8) et M-8D-01, M-8F-06 du worker sont tués ; X-01 vit (CC-1). Bilan : 39 sur 40.

**2. Les trois modifications de l'avis**
- **Q-T3-7 (perte sur W)** :
  - refus OBSERVATEURS/perte pour W = 0, −1, True, 1,5, 10 080 (l'ancienne forme en fenêtres) et une durée nominale au-delà de l'horizon ;
  - W = 1 sur 7 jours exacts est admis ;
  - instant toujours inférieur à 7W jours (maximum 10 079 et 20 158) ;
  - observateur perdu uniforme (χ² 1,70 et 0,12), jours χ² 10,97 sur 6 ddl.
- **Q-T3-13 (deux queues)** :
  - mon oracle naïf (hashlib, rotation position par position, suite linéaire) sur 120 instances × 4 valeurs de g, R = 50 : 0 écart ;
  - la queue basse est la plus petite 309 fois, la haute 160 fois, égalité 11 fois : la seconde queue informe bien, comme l'avis le prévoyait ;
  - plus 30 lois à R = 25 : 0 écart.
- **Q-T3-15** : la règle tient par construction (unité absente de la classe, donc toutes les unités décalées). Docstrings et test présents ; M-8F-06 tué.

**3. Valeurs Q-T3 de `parametres.json`**
- Les 15 citations pointent sur la bonne section de l'AVIS (da343918…) et sur les bonnes lignes de la PROPOSITION.
- Contenu comparé ligne à ligne pour Q-T3-2, 5, 6, 7, 10, 12, 13 et 15 : fidèle.
- Marques adopté / modifié / [E0] conformes pour les 15.

**4. P-7, O-1, O-4**
- **P-7** : 225 777 chaînes comparées à `HOTE` de `recalc/rotation.py` commis (4183fbe6…) : 0 écart.
  - Mêmes réponses des deux côtés aux bornes 253 et 254, aux majuscules, à `_`, `:`, l'espace, `~`, « ␠! » et au saut de ligne final.
  - Les dix noms courts sont admis des deux côtés.
- **O-1** : avec `sonde_4i.py` sur l'état final, réordonner ou réduire le pool ne change plus aucune fenêtre de stress, pour les 7 genres de dérive (avant : 745 à 10 862 fenêtres).
  - Seul le cas « sans binance » avec panne initiale change, du fait de la limite Q-T3-1, pas de la loi.
- **O-4** : refus OBSERVATEURS/indice pour ue [0, 1, 4], repli 4, repli 3 à M = 3 et ue [3] à M = 3 ; les jeux valides sont admis.

**5. Identité** (Python 3.10.20, 3.11.15, 3.12.3, 3.13.14 × PYTHONHASHSEED 0, 1, 4242, aléatoire)

| sonde | empreinte | résultat |
|---|---|---|
| T3 du worker, mode neuf | `8895661a…` | 16 sur 16 |
| T3 du réviseur, mode neuf | `03304e5e…` | 16 sur 16 |
| O-1 | `b1310f64…` « stable » | 16 sur 16 |
| T3 du worker, mode compat | 42e935b0… (ancienne) | 16 sur 16 |
| T3 du réviseur, mode compat | a7cf3bab… (ancienne) | 16 sur 16 |
| O-1 sur SB-8D, avant la correction | 59a7de6f… « instable » | rouge confirmé |
| tranche 2 (worker et réviseur de T2) | 8d97a9dc… et d3ba1eb6… | inchangées |

Les sondes dérivées ne diffèrent des originales que par les deux remplacements d'interface (vérifié par `diff`).

**6. Patch ROTATION** : `git apply --check` passe sur la version commise à f5915a5 (blob b8eeda3, sha256 9db81092…).
- Il s'insère au §1, point 8, après la précision de Q-RB-5.
- Son texte est conforme à la ligne pour RB-7 et à l'AVIS Q-T3-15.
- 0 octet 92.
- Les six vecteurs du contrat commis sont égaux à mes valeurs calculées par `bc`.

**7. Gates sur f5915a5 avec les 13 diffs**
- Les 13 diffs s'appliquent ; chaque état est vert à son plancher exact : 119, 122, 125, 127, 128. Diffs de +80, +106, +112 et +95 lignes de code. `gates.yml` ne change que sa ligne 242.
- Runner 33/33 ; sim-bis 128 ; s2bis 156 ; s2-harness 405 (2 sauts qui nomment la variable). s2bis et s2-harness tournent sous `unshare -n`, lo allumée.
- Mode strict `-X dev -W error` sous 3.10 à 3.13 : 128 OK, 8 fois sur 8.
- R-13 : 0 constat. Octets 92 : 0 dans le lot et dans les 13 diffs. `gate-secrets --tree` OK.
- xtask : S-G1 à S-G8 VERT ; fmt, no_std et clippy VERT ; S-G9 ROUGE, 1 violation (`17:70`), identique sur le témoin.
- Mes oracles indépendants, rejoués sur l'état final, ne trouvent aucun écart.

**8. Points du worker**
- **L-1** : à former. Vérifié : avec un `calibration.unites` réduit, EP est refusé (`CALIB/forme`). SB-11 doit séparer le pool opérationnel de la liste d'EP. Déclencheur : un retrait du pool avant le sceau.
- **L-2** : d'accord, c'est une ligne du brief de SB-11 (passer le W de la cellule). Le refus attrape déjà l'ancienne forme.
- **L-3** : d'accord. Le patch s'applique et il appartient à la série RECALC-BIS.
- **L-4** : d'accord. L'équivalence tient aujourd'hui (mesurée ci-dessus), mais aucun test ne lie les deux textes : le lien relève de SB-13.
- **E-1** : accepté ; l'état final ne porte aucun octet 92 (vérifié).
- **E-2** : accepté ; le test final tue M-8F-03 à 05 et mes X-02 et V-12a.
- **E-3** : accepté ; le rouge a été remontré.
- **E-4** : accepté ; j'ai commis le même écart (voir plus bas).
- **E-5** : accepté. Comptes et empreintes de ses seules copies ; à éviter même sur des copies.
- **E-6** : accepté. Seul le nom d'un fichier a été vu, sans contenu. Extraire les seules lignes de verdict.
- **E-7** : accepté ; toutes les lectures portent sur des pièces permises.
- **E-8** : accepté ; PID vérifiés par `/proc`.
- **E-9** : accepté ; la borne n'a pas été approchée.
- **E-10** : accepté ; je l'ai vérifié sur f5915a5.
- **E-11** : accepté ; dérivation fidèle et mode compat reproduit.

## Observation (non bloquante)
- La docstring de `Couche` est coupée au milieu de « indice i ≥ / 0 ». Cosmétique.

## Mes écarts
- **Barres obliques inverses tapées** : dans un `sed` qui dérivait `tailles_cc.py` (fichier vérifié, 0 octet 92), deux motifs `grep` et des regex d'affichage, et un `tr` de `/proc` (remplacé par `outils/cmdline.py`). Aucun effet sur un fichier écrit.
- **Heures non lues** : six heures écrites dans mes notes sans lire l'horloge, corrigées et marquées « non lue ».
- **Prototype** : une attente fausse dans la première version de `proto_corrections_cc1.py`, corrigée avant usage.

## Journal G1
- **[lu]** :
  - le brief des corrections (fa243d23…) et le rapport du worker ;
  - l'AVIS-SIM-T3 (da343918…) en entier ;
  - les 4 diffs, par l'état final ;
  - `rotation.py` (4183fbe6…) et ROTATION (9db81092…) à f5915a5 ;
  - les outils et le journal du worker cités ;
  - la PROPOSITION, aux lignes citées.
- **[abs]** : les G2 de RB-6 et RB-7.
- **Chiffres** : tous recomptés par mes commandes (`sorties/cc-*`).
