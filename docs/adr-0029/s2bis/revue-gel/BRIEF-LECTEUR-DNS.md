# Brief lecteur — noms témoins DNS de D-5 (E-C-28) pour la configuration scellée du gel du collecteur

Orchestrateur, 2026-10-17 23:22:15 UTC (`date -u`). Lecteur `shogen-lecteur`, effort high. Tu travailles dans `<scratchpad>/s2bis/gel/dns/` (crée-le). Dépôt : `/home/user/shogen`, en lecture seule.

## Objet
Choisir, par mesure, les **deux noms témoins** de la sonde D-5 (résolveur de l'observateur) et un remplaçant, pour la configuration scellée `sante.json` (lot GEL-COLLECTEUR-1). Critères, à lire d'abord : `docs/adr-0029/ADR-0029-campagne-S2-bis.md` l.110 (D-5 : TTL ≤ 60 s, deux autorités distinctes, adresses et autorités hors des ASN du pool) et l.80 (ASN du pool : AS13335, AS16509, AS14618, AS19551) ; `docs/adr-0029/g0-collecte/PROPOSITION.md` l.188-189 (E-C-27, E-C-28) ; `docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md` l.586-600 (enregistrement `sante`, D-5).

## Mesures (réseau autorisé pour ce brief : DNS en UDP et HTTPS vers RIPEstat seulement ; aucune API de place, aucune clé)
1. Candidats de départ : www.python.org, www.kernel.org, www.debian.org, www.ripe.net, api.github.com, www.bbc.co.uk, www.eff.org, www.switch.ch, www.google.com ; ajoute des noms institutionnels stables si les critères l'exigent (registres de ccTLD, universités, organismes de normalisation).
2. Pour chaque candidat : la chaîne CNAME et le **TTL d'origine** de l'enregistrement A final, lu **directement sur un serveur autoritaire de la zone** (requête sans récursion : le TTL d'un résolveur récursif est décompté, il ne vaut pas) ; l'ensemble NS de la zone finale et l'opérateur de chaque NS ; l'ASN des adresses A et des adresses des NS, lus sur RIPEstat (`https://stat.ripe.net/data/network-info/data.json?resource=<IP>`). Code : `python3 -I -B` avec `socket` et `struct` (bibliothèque standard seule), scripts gardés dans ton dossier.
3. Écarte tout nom dont une adresse A ou un NS est dans un ASN du pool ; écarte tout nom dont le TTL d'origine dépasse 60 s.

## Sortie
Pièce à produire : `<scratchpad>/s2bis/gel/LECTURE-DNS-TEMOINS.md` (à produire) : un tableau par candidat (nom, chaîne CNAME, TTL d'origine, serveur autoritaire interrogé, NS et opérateurs, ASN des A et des NS, verdict et motif), chaque valeur marquée [mesuré] avec l'heure UTC de la mesure ; puis une recommandation : deux noms d'autorités distinctes et un remplaçant, en une ligne chacun avec les motifs ; puis les limites (ce qui n'a pas pu être mesuré). Aucun dump brut de plus de dix lignes dans la pièce ; les réponses brutes vont dans ton dossier. SHA256SUMS de ton dossier couvrant la pièce.

## Règles
- Gate 0 : l'identifiant exact de ton modèle en tête de la pièce et de ton message final (attendu `claude-sonnet-5-5`).
- Aucune modification d'un fichier suivi du dépôt ; aucune opération git en écriture ; toute commande git qui liste ou compare des chemins est limitée à une liste explicite de chemins (ici aucune commande git n'est nécessaire).
- Interdits : `docs/15-*`, `docs/16-*`, `docs/pocket-report/`, `docs/rapports/`, `docs/adr-0025/`, `docs/adr-0028/monark-m009a/`, `docs/adr-0028/execution/`, tout `*.jsonl`, toute pièce de D.2 ; ne jamais poser `SHOGEN_S2_CAMPAGNE_CONTROL` ; aucune recherche ou énumération récursive sur `docs/`, sur le dépôt ni sur le scratchpad.
- Message final court, en français : les deux noms, le remplaçant, les motifs, le chemin de la pièce.
