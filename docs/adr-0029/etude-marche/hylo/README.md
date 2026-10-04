# Hylo et protocoles d'autres chaînes qui dépendent d'oracles (2026-10-04)

Pièce de contexte commercial, **non normative** : elle ne fonde aucune décision de mesure. Étude qualitative sur sources publiques
lues (site, documentation, SDK, audits, DefiLlama, articles d'incident). Aucune prise de contact.

- `HYLO-ET-AUTRES-CHAINES.md` : la pièce (lecteur `claude-sonnet-5-5`) ; corrections G2 C1 à C8 et reprises R1 à R5 appliquées (§8).
  Au versement, une seule ligne retouchée (l. 286 : chemin du dossier de travail remplacé par `<scratchpad>/`) : sha256 versé `2ca03145…`,
  sha256 de la pièce contrôlée `1a981140…f0dbb`.
- `corrections-g2/apply1.py`, `apply2.py`, `apply3.py` : remplacements exacts ; rejoués sur la version relue par la G2 (sha256
  `a24e7cf2…94f65`, hors dépôt), ils redonnent la pièce contrôlée à l'octet (rejoué par l'orchestrateur, `cmp` identique).
- `quotes.txt`, `chk.py`, `corrections-g2/mkquotes.py` : contrôle des citations contre la copie désignée (0 problème).
- `INDEX-COPIES.md` : copie → URL (127 sur 193 ; 66 « non consignée », aucune URL devinée).
- `g2/G2-HYLO.md` : relecture G2 neuve (`claude-opus-5-5`), ACCEPTE-AVEC-CORRECTIONS ; `g2/CONTRE-CONTROLE-HYLO.md` : contre-contrôle
  des corrections (reprises R1 à R5, appliquées ; rejeu orchestrateur : 126 citations, 0 à reprendre).
- Briefs : `BRIEF-HYLO-SOLANA.md`, `g2/BRIEF-G2-HYLO.md`, `g2/BRIEF-CORRECTIONS-HYLO.md` (chemin du dossier de travail remplacé par `<scratchpad>/`).
- Copies des pages lues (`pages/`, `pages2/`, ~193 fichiers dont trois PDF d'audit) **hors dépôt** : empreintes dans `SHA256SUMS.copies`.
