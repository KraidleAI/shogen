# Brief — corrections G2 et avis de la tranche 2 du lot SIM-BIS (diffs SB-4C, SB-4D…, après SB-4B)

Worker `shogen-worker`, effort max. Dépôt `/home/user/shogen` en lecture seule : **aucune opération git en écriture**. Lis `date -u`
avant toute date. Tu travailles dans `<scratchpad>/s2bis/sim2/corr/`,
avec un `TMPDIR` dédié.

Base : copie de la tête 784ebd2 (`git archive HEAD | tar -x …`, avec les exclusions `docs/rapports`, `docs/adr-0025`,
`docs/adr-0028/monark-m009a`, `docs/15-*`, `docs/16-*`, `docs/pocket-report`). Applique dessus, en série, les six diffs
`…/sim2/diffs-784ebd2/SB-3A.diff` … `SB-4B.diff`, dans l'ordre et sous les noms de `…/sim2/SHA256SUMS`.

Pièces à lire :
- relecture G2 : `…/sim2/g2/G2-SIM-T2-transcrit.md` (ACCEPTE-AVEC-CORRECTIONS, liste fermée C-1 à C-5). Ses outils sont dans
  `…/sim2/g2/rev/` : les prototypes de cas sont dans `rev/stat/proto_corrections.py`, les mutants R-01 à R-28 et leurs outils dans
  `rev/outils/`. Repère-les par leur nom, sans recherche récursive large ;
- avis de l'advisor : `…/sim2/g2/AVIS-SIM-T2.md` ;
- ton rapport précédent : `…/sim2/g2/RAPPORT-WORKER-SIM-T2-transcrit.md`.

Contrat : le G0 `docs/adr-0029/g0-sim/G0-SIM-BIS.md`, avec son ajout daté du 2026-10-05.

## Adjudications de l'orchestrateur (liste fermée de ce lot de corrections)

- **C-1 à C-4** : telles qu'écrites par le réviseur.
  - Pour C-1 (a) à (j), pars de ses prototypes. Chaque cas doit être rouge sous son mutant et vert sur le code.
  - Pour C-4, l'accès par `getattr` (R-28) s'écrit comme limite.
- **C-5** :
  - `sources.source` cite l'ajout daté du G0 du 2026-10-05 01:45:03 (points 2 et 3) ;
  - **et** `rattachement` porte le sha256 actuel du G0 (`d9cffc0a…` : recalcule-le sur la tête, ne le recopie pas). La valeur
    précédente est mentionnée dans le texte de provenance.
- **C-6 (avis Q-T2-11, modification adoptée, avant E0)** : l'indice de flux reste entier (forme E-S-41).
  - h est pris dans une liste `sources.indices_hotes` **scellée et immuable** : les 10 hôtes D1-bis de l'ADR, dans un ordre écrit et
    sourcé (ADR-0029 l.168 ; EP l.8), distincte des listes opérationnelles.
  - Un hôte d'un pool qui n'y figure pas est refusé par un refus nommé. Un hôte retiré laisse son rang inemployé.
  - Même règle pour les unités faibles : leur indice est leur rang dans `indices_hotes`, et non plus dans `spec["hotes"]`.
  - Tests : refus, stabilité de l'indice quand un pool est réordonné ou réduit.
  - Les octets des sorties changent : déclare la nouvelle empreinte d'identité, mesurée sur 3.10 à 3.13.
- **C-7 (avis Q-T2-5, Q-T2-6, Q-T2-10, adoptés)** : écris dans `parametres.json` les valeurs de l'avis, chacune avec sa source (ligne de
  l'AVIS et de la PROPOSITION). Cela ferme, avant E0, les items DERIVE-AMPLITUDE-1 et ABS-POPULATIONS-1.
  - Poids des pannes longues : 1:1:1 en nombre d'épisodes.
  - Les cinq valeurs des dérives du tableau Q-T2-6, avec la mention « rapport 19, même enveloppe que la tendance ».
  - Population des paires et des triplets : les 7 hôtes AS13335.
  - Hôtes faibles : les k premiers de la liste `as13335` scellée, k ∈ {1 ; 2 ; 4}.
  - Partenaire de l'unité faible : tiré par incident, uniforme parmi les six autres hôtes AS13335. Avec k ≥ 2 unités faibles, l'hôte
    imposé est tiré uniformément parmi elles.
  - Bascule : la première unité faible.
  - Si le code lit ces valeurs, branche-les ; sinon, un test vérifie leur présence et leur forme sous le schéma.
- **C-8 (avis Q-T2-6, oracle manquant)** : un test « taux moyen de la série amincie = moyenne de m(t)·p, à 5 erreurs-types » pour la
  tendance et pour le saut.
- **O-2** : écrire « ≈ » dans la phrase d'`amincir`.
- **Restent en items, sans code dans ce lot** :
  - O-1 : schéma fermé des cellules à SB-11 ;
  - O-3, O-5, O-6 : limites écrites au paquet ;
  - Q-T2-2, E′ tiré dans les seuls segments de Z : décidé sur la mesure E-S-46 à SB-11 (CALCUL-1) ;
  - les impressions demandées par l'avis : résidus log FIV par ℓ d'E1, taux effectifs de F par cellule, épisodes longs sous N4.
  - O-4 est un erratum du G0, porté par l'orchestrateur.

## Règles

- Les tests d'abord, avec un **rouge d'assertion montré avant le code**, pour chaque C-n.
- Rejoue par la commande du job (runner d'abord, puis la ligne de `gates.yml`, borne de 300 s ; dépassement = FATAL) :
  - les 28 mutants du réviseur : tout vivant meurt, sauf R-28, qui est une limite ;
  - tes 80 mutants : les 4 adaptés compris ;
  - au moins dix mutants neufs pour C-6, C-7 et C-8.
- Bibliothèque standard seule.
- Diffs en série, **chacun ≤ 200 lignes de code ajoutées**, plancher exact relevé à chaque diff.
- Identité bit à bit : graines, PYTHONHASHSEED, Python 3.10 à 3.13.
- R-13, R-8. Aucune opération réseau (`unshare -n`). Aucune lecture de journal de campagne.
- `cargo --locked xtask verify` sur la copie : lignes de verdict seules ; S-G9 `docs/17:70` est connu.
- Journal G1 dans le rapport, et SHA256SUMS.
- Nettoie tes copies lourdes à la fin.

Interdits :
- `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`,
  `docs/adr-0028/execution/` ;
- tout `*.jsonl` réel ;
- toute pièce de D.2 ;
- **aucune recherche récursive (grep -r, git grep, du, find large) sur `docs/`, sur le dépôt entier ni sur le scratchpad entier**.

Rapport par message si le harnais refuse le fichier. Gate 0 : l'identifiant exact du modèle en tête. Résumé court en français,
C-n par C-n.
