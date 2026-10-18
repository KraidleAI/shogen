# Adjudication des noms témoins DNS de D-5 — orchestrateur, 2026-10-17 23:40:13 UTC (`date -u`)

Pièce lue : `LECTURE-DNS-TEMOINS.md` (lecteur `claude-sonnet-5-5`, Gate 0 en tête ; mesures du 2026-10-17 entre 23:28:53 et 23:37:47 UTC).

- **Retenu pour `sante.json` (GEL-6)** : `noms` = [`www.kernel.org`, `www.arin.net`]. Motifs (pièce l.25, l.43, l.69-70) : TTL servi jamais au-dessus de 60 s sur les sondages ; aucun serveur de noms ni opérateur commun entre les deux ; aucune adresse ni autorité dans un ASN du pool (ADR l.80).
- **Remplaçant écrit d'avance** (Q-C-08, section « Remplaçants écrits d'avance » du paquet, GEL-2) : `www.cern.ch` (pièce l.60, l.71), réserve : un seul opérateur.
- **Lecture de « deux autorités distinctes »** (ADR l.110) : celle du lecteur (pièce l.79) est adoptée : les deux noms n'ont aucun serveur de noms ni opérateur en commun, de sorte qu'une panne d'une autorité ne fait pas tomber les deux noms.
- **Limite reconnue** : le TTL d'origine n'a pas pu être lu sur un serveur autoritaire depuis ce poste (pièce §0 : relais récursif sur UDP/53). L'ADR l.110 prévoit la mesure « au rodage » : la confirmation (TTL ≤ 60 s, autorités, ASN) se fait au smoke de DB-2 et aux premiers jours du rodage sur le résolveur réel de chaque observateur. Item à former au versement : SHOGEN-S2BIS-DNS-TEMOINS-RODAGE-1, déclencheur DB-2 (mise en service), sortie : TTL et autorités journalisés, les deux noms confirmés ou le remplaçant substitué avant le sceau.
