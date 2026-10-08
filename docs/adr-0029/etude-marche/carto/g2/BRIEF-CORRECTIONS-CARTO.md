# Brief — application des corrections G2 à CARTO-DEFI-ORACLES.md (lecteur, auteur de la pièce)

Lecteur `shogen-lecteur`. Dépôt `/home/user/shogen` en lecture seule ; aucune opération git ; lis `date -u` avant toute date. Tu écris
seulement dans `<scratchpad>/s2bis/marche2/carto/` (hors `g2/`, que tu
lis seulement). Aucun réseau (tout est dans `raw/` et `out/`).

Relecture G2 : `g2/G2-CARTO.md`, §7, corrections C-1 à C-13 (liste fermée). Applique-les toutes, avec les **adjudications de
l'orchestrateur** suivantes là où la G2 laisse un choix :
- **C-1** : corrige `traite.py` (toutes les entrées d'un oracle ; casse ; alias `bsc`→`Binance` ; chaîne présente à TVL nulle = 0 ;
  repli sur la TVL totale seulement sans correspondance, montré à part dans T2). Ton résultat doit égaler `g2/sortie-t2-attendu.txt` ;
  tout écart est expliqué.
- **C-2** : la règle écrite d'avance reste (mort = `deadFrom` renseigné, écrit tel quel) ; les 24 protocoles `deadUrl` restent dans le
  périmètre et sont **déclarés** en biais (nombre, valeur, aucun parmi les cibles). Pas de recomptage.
- **C-3** : les comptes restent ; les cas Re (PoR), PoolTogether V5 (RNG), PoolTogether V3, Polymarket et Across (UMA, [inféré]) sont
  **déclarés** en biais, avec les chiffres « sans RNG/PoR » de la G2 donnés à titre indicatif ; §1 reformulé « dépendent d'un prix ou
  déclarent un oracle ».
- **C-6 et C-7** : **Sky Lending sort de la liste courte** (son acheteur, la gouvernance de Sky, est déjà visé par P1 sous « Spark/Sky » :
  le dire dans la réserve) ; **Jito Liquid Staking entre** à sa place (Solana, Switchboard seul déclaré [lu]), avec sa ligne complète
  (panier, incidents, pourquoi). Ethereum tombe à 3 cibles G. Mets à jour la répartition par chaîne.
- **C-13** : `out/perimetre.csv` sera versé avec la pièce (cite-le avec son sha256) ; `raw/` reste hors dépôt, empreintes seules ; la
  section 8 cite les chemins de versement `docs/adr-0029/etude-marche/carto/` (pièce, scripts, `cibles.json`, `pourquoi.json`,
  `out/perimetre.csv`, SHA256SUMS) ; ajoute la ligne d'exposition (pièces du dépôt lues, interdits non ouverts).
- C-4, C-5, C-8 à C-12 : telles que la G2 les écrit.
Registre 09 (`docs/09-vocabulaire.md`) : aucune locution interdite ; citations web entre “ ”, jamais « ». Rejoue la chaîne hors réseau
dans le bon ordre, recalcule SHA256SUMS. Ajoute en fin de pièce une section « Corrections G2 appliquées » (C-n → ce qui a changé).
Gate 0 (identifiant exact). Résumé court en français, avec pour chaque C-n : appliquée / écart motivé.
