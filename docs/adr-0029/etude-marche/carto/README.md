# Cartographie DefiLlama des protocoles DeFi qui dépendent d'oracles (2026-10-04)

Pièce de contexte commercial, **non normative** : elle ne fonde aucune décision de mesure. Source unique : l'API publique
DefiLlama du 2026-10-04 (ce que DefiLlama **déclare**, non vérifié). Aucune prise de contact.

- `CARTO-DEFI-ORACLES.md` : la pièce (lecteur `claude-sonnet-5-5`), corrections G2 C-1 à C-13 appliquées (section 9).
- `traite.py`, `fetch_detail.sh`, `enrichit.py`, `assemble.py`, `cibles.json`, `pourquoi.json` : chaîne de calcul (ordre de rejeu en §8).
- `out/perimetre.csv` (424 protocoles du périmètre), `out/biais.json` (chiffres des biais déclarés).
  `out/perimetre.csv` est converti en fins de ligne LF au versement (règle `* text=auto eol=lf` de `.gitattributes`) : sha256 versé `2c1e719a…`, sha256 d'origine (CRLF, cité par la pièce et la G2) `d452e2db…a945` ; contenu identique hors fins de ligne.
- `g2/G2-CARTO.md` : relecture G2 neuve (`claude-opus-5-5`), ACCEPTE-AVEC-CORRECTIONS ; recalcul indépendant 244/244 cellules.
- Briefs : `BRIEF-CARTO-DEFI.md`, `g2/BRIEF-G2-CARTO.md`, `g2/BRIEF-CORRECTIONS-CARTO.md` (chemin du dossier de travail remplacé par `<scratchpad>/` au versement).
- Réponses brutes de l'API (`raw/`, ~10 Mo) **hors dépôt** : empreintes dans `SHA256SUMS.raw`.

Adjudications de l'orchestrateur : règles écrites d'avance conservées, biais déclarés sans recomptage (C-2, C-3) ; Sky Lending sorti
de la liste courte (déjà visé par P1 sous « Spark/Sky »), Jito Liquid Staking entré (C-6, C-7) ; détail DefiLlama de Jito téléchargé
par l'orchestrateur le 2026-10-04 à 21:11 UTC (même jour que les 29 autres), `enrichit.py` et `assemble.py` rejoués.
