# Adjudication du lot PUBLICATION-S2-AMENDEMENTS (SHOGEN-PUBLICATION-S2-AMENDEMENTS-1) — orchestrateur, 2026-10-15 21:22:39 UTC (`date -u`)

## Contrôles
- Générateur : transcript 387 champs `model`, tous `claude-opus-5-5` ; FM-1.1 = 0 (deux outils) ; SHA256SUMS conforme ; diffs lus par l'orchestrateur (PA-a, PA-b, PA-c : substitutions et ajouts datés en fin de ligne ; engagements (i), (ii), (iii) de COINGECKO-2026-10-10 §4 tenus).
- G2 neuve (réviseur distinct) : 244 champs `model`, tous `claude-opus-5-5` ; FM-1.1 = 0 ; SHA256SUMS conforme (44) ; verdict **ACCEPTE**, aucun diff de correction ; empreinte de la série `58ba49e4…f899d4`.

## Décisions
1. **PA-a, PA-c, PA-b, PA-d adoptés à l'octet**, dans cet ordre (quatre commits, chaîne de commit après la chaîne DETTES-T7). « panne » → « lecture en échec » dans le texte courant français : adopté (cohérence des deux langues ; étiquettes scellées inchangées).
2. **L-1 + L-2 (avant la publication, même lot, phase 2)** : les en-têtes (EN l.7, FR l.13) disent « aucun nombre n'est changé ni ajouté » ; les ajouts datés portent une date. Substitution dans la ligne (aucune ligne décalée) : « aucun nombre n'est changé ni ajouté, hors les dates des ajouts datés du 2026-10-15 » (et l'équivalent anglais) ; contrat de `controle_public` mis en cohérence (les ajouts datés exclus du contrôle des nombres, table E-21..E-27 versée) ; empreinte de source de PA-d mise à jour, `controle_en` rejoué.
3. **L-4** : `interne/ACTEURS-NOMMES.md` l.52-53 « une panne » → « une lecture en échec » (même lot, phase 2). **L-6** : sorties de contrôle de `docs/publication/interne/` régénérées (phase 2).
4. **L-3** (49 lignes d'ajouts datés de `docs/11` au commit `6c04e91`, absentes des versions publiques) : item SHOGEN-PUBLICATION-S2-SYNC-DOCS11-1, à trancher avant le 2026-10-25 (porter ou dire pourquoi non) ; hors de ce lot. **L-5** : non retenu (déjà au §9.3 pt 5, G2).
5. **O-1 (« nombreuses »)** : non ajouté ; le sens de l'engagement (ni source unique ni principale) est tenu ; le mot n'a pour source qu'un courriel privé. **O-5** adopté (« amendement A-8 du glossaire » dans la phrase de fermeture). O-2, O-3, O-4 : de forme, non repris.
6. **Écarts** : E-2 du générateur (Chromium a tenté des connexions réseau de fond, en échec ; sortie identique à la variante hors réseau) admis, consigné ; E-1, E-3, E-4 admis ; expositions E-1, E-2 de la G2 admises. Enregistrement `oracle_record.py` du rôle G2 : non applicable (lot postérieur au cp-2 de S2).
7. **PDF** : reconstruit après la phase 2 ; son versement et l'envoi à CoinGecko restent des actes de l'investisseur (le rapport reste « Draft — not published »).

## Ajout daté du 2026-10-15 22:00:49 UTC (`date -u`) : adjudication de la phase 2 (G2 : ACCEPTE-AVEC-CORRECTIONS, C-1 hors dépôt)

Contrôles : générateur 521 champs `model` tous `claude-opus-5-5`, FM-1.1 = 0, SHA256SUMS 114 OK ; G2 (même réviseur, distinct du générateur) 244 + reprise, tous `claude-opus-5-5`, FM-1.1 = 0, SHA256SUMS 233 OK ; les diffs e, f, g lus par l'orchestrateur (a à e, g passent `git apply --check` seuls sur la tête ; f dépend de d, attendu).
- **PA-e, PA-f, PA-g adoptés à l'octet** ; **C-1 adoptée** (cinq tests de `tests-public/`, hors dépôt, appliquée par l'orchestrateur dans le dossier du lot).
- **L-9 (élargi par la G2)** : les sept commits se suivent sans commit intercalé (`chaine_pa.sh`) ; ni `controle_en` ni `controle_public` ne sont des gates de CI.
- **O-P2-1 adoptée** : la phrase de fermeture dira « les dates des ajouts datés sont les seules valeurs numériques ajoutées ; les ajouts portent aussi une heure, des renvois de section, le commit `ed479c5` et un chemin » ; libellé des en-têtes inchangé.
- **O-P2-4** : recette de rejeu de `controle_public.sortie.txt` (source `docs/11` à `2db4f40`, extraite hors dépôt) écrite au bloc daté de l'annexe B.
- **Items formés au versement** : SHOGEN-PUBLICATION-S2-SYNC-DOCS11-1 (L-3) ; SHOGEN-PUBLICATION-ACTEURS-RELEVE-1 (L-7 : relevé du §1 d'ACTEURS-NOMMES périmé, 32/24 mentions) ; SHOGEN-PUBLICATION-OUTILS-PUBLIC-VERSES-1 (L-8 : outils français du lot DOCS11-PUBLIC et `controle_public` amendé, avec C-1, non versés au dépôt). O-P2-2 (l.40 du glossaire « A-7 et A-8 ») : rejoint OUTILS-PUBLIC-VERSES-1 (changer l'empreinte imprimée par PA-g). O-P2-3, O-P2-5 : de forme.
- **Clôture CONFORME sans passe 3** (précédents DT2-q à t, DB1-r à t). PDF final sha256 `aa3e5802…2bfd7`, 17 pages : versement et envoi à CoinGecko = actes de l'investisseur.
