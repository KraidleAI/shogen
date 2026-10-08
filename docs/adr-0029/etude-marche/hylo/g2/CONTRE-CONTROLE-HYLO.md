# Contre-contrôle des corrections G2 sur « Hylo et autres chaînes » (limite L4 de `G2-HYLO.md`)

- **Gate 0** : modèle qui m'exécute : `claude-opus-5-5` (identifiant exact ; réviseur G2, effort `max`). Je n'ai appliqué aucune correction.
- **Date** : `date -u` lu à 21:26 UTC puis 21:35 UTC, le 2026-10-04.
- **Pièce contrôlée (v2)** : `HYLO-ET-AUTRES-CHAINES.md`, sha256 `4aeb9860dceb3f3c9de7c73648843c90a095be968499f6e890794d2374e4b9cc`. C'est l'empreinte annoncée, inchangée du début à la fin du contrôle.
- **Version relue (v1)** : `HYLO-ET-AUTRES-CHAINES.v1-avant-G2.md`, sha256 `a24e7cf2…94f65`, identique octet pour octet à la version de ma G2.
- **Pièces jointes contrôlées** : `INDEX-COPIES.md` (`7c772e67…`), `quotes.txt` (`56b48aae…`), `chk.py` (`9722ccca…`), `corrections-g2/apply1.py` (`bf35d5f9…`), `corrections-g2/apply2.py` (`aa5374af…`), `SHA256SUMS` (`288f6090…`).
- **Réseau** : aucune requête. **Écrits** : uniquement dans `g2/` (ce fichier et `g2/cc/`).

## Verdict : liste fermée de reprises (R1 à R5)

Non CONFORME en l'état, à cinq reprises près. Toutes sont des retouches de texte, sans nouvelle collecte.

Sur le fond, les corrections C1 à C8 sont appliquées, sauf trois sous-points : C2 (a), l'échelle de C5 (a) et la phrase de C5 (h). La précision sur Switchboard est tenue : aucun lien causal entre attaque et fermeture, et rien n'est dit sur Solana au-delà des deux phrases citées des sources.

## 1. Résultats des cinq contrôles demandés

### (1) Chaque Cn appliquée telle que je l'ai écrite

| Cn | Statut | Constat (lignes de v2) |
|---|---|---|
| C1 | Appliquée | L142 commence désormais par “Each vault requires”. |
| C2 | **Partielle** | Huit lignes de `quotes.txt` réalignées. `chk.py` est désormais sensible à la casse. « citations contrôlées par `chk.py` » en L289 ; « contre la copie que le rapport désigne » en L6. **Mais** la ligne 1 de `quotes.txt`, à citation vide, n'est pas supprimée, et “suspected” est rattaché à Solana Compass au lieu de Full Sail (R3). |
| C3 | Appliquée | (a) ADV-01 critique (L18, L96). (b) Six constats (L18). (c) ADV-03 corrigé (L96). (d) 44 FIXED et 7 ACKNOWLEDGED (L98). (e) « écart de date » retiré (L96, L258). |
| C4 | Appliquée | (a) L69. (b) L83. (c) L35 et L112. (d) L15, L23, L118. (e) L16. (f) L88 et L250. (g) L16, L90, L262. |
| C5 | **Partielle** | (b) à (g) appliqués (L20, L22, L158, L178–179, L201, L206, L211–212, L218, L224, L247, L261, L263, L277). La précision Switchboard est tenue : L20, L212, L222 et L224 ne disent aucun lien causal ; sur Solana, seulement “We have received no reports of similar behavior on Solana.” (post-mortem) et “at that time” (Solana Compass), en L211. **Mais** (a) : l'échelle de confiance énoncée contredit sept attributions (R1). Et (h) : la phrase révisée du §3.3 contredit les définitions du §1.7 (R2). |
| C6 | Appliquée | (a) L23, L118. (b) L119. (c) L138. (d) L251. (e) L121, L165. (f) L289. (g) L120. |
| C7 | Appliquée | (a) L159. (b) L155. |
| C8 | Appliquée | (a) Trois anomalies déclarées (L279, L288). L'URL de `jupx-742488.raw` est déclarée « non consignée » au lieu d'être donnée : c'est une limite honnêtement rendue, je l'accepte. (b) `SHA256SUMS` régénéré. |
| Observations | Appliquées | O3 (L150, L157), O4 et O5 (L202), O6 (L171), O7 (L261), O1 (`INDEX-COPIES.md`). O2, O8 et O9 sont laissées, ce qui est licite. |

### (2) `work/cites.py` rejoué

J'ai écrit `g2/cc/cites_v2.py` (sha256 `c06d696a…`). Il reprend ma table de désignation v1, indexée par le texte de la citation, et désigne d'après leur contexte en v2 les 16 citations nouvelles (27 occurrences).

Résultat : **123 citations, 0 introuvable dans la copie désignée, 0 qui ne passerait qu'en normalisation large**.
- 118 en octets exacts ;
- 4 aux espaces près ;
- 1 qui ne diffère que par l'échappement markdown `\$` (L76, déjà acceptée en G2).

La comparaison est sensible à la casse. Aucune citation ne dépasse 24 mots. Il n'y a aucune « » dans la pièce. Sortie : `g2/cc/cites_v2.out`.

`chk.py` régénéré : `problemes: 0`.

### (3) Registre 09 sur tout le texte nouveau

Les formulations relevées en C6 ont disparu du corps du texte. Elles ne figurent plus qu'à titre de mention, dans le journal du §8 (L306, L308).

Le reste du texte nouveau n'emploie aucun qualificatif d'assurance. On y trouve :
- « garantie » au sens de collatéral ;
- « validation » et « vérification » au sens de calcul ;
- « vrai » au sens booléen ;
- des négations conformes au registre (« n'en serait pas établie », « aucun lien causal n'est établi »).

Contrôle S-G4 approché (`LOCUTIONS_INTERDITES` de `xtask/src/sg4.rs`, appliqué à la prose hors “ ”, « » et code) : 0 occurrence, sur v2 comme sur `INDEX-COPIES.md`. R-13 : 0. S-G5 : aucune « » anglaise.

**Les lignes 119 et 138 sont acceptables :**
- **L119** : « l'indépendance n'en serait pas établie » est la forme même que prescrit le registre (l. 21 : l'indépendance n'est jamais établie).
- **L138** : « Deux fournisseurs déclarés indépendants (la page promet “Independent infrastructure and operators”) : aucune mesure du recouvrement de leurs racines n'est publiée ». L'adjectif est attribué au tiers : « déclarés » est suivi de sa promesse citée mot pour mot. La phrase dit aussitôt qu'aucune mesure n'existe, ce qui sépare le déclaré du mesuré, comme l'exige le registre (l. 20–21). Ce n'est pas l'interdit « sources indépendantes » dans la voix du projet. Une variante, facultative : « que la page présente comme indépendants ».

### (4) Rien d'autre n'a changé que ce que les corrections demandent

Le diff v1 → v2 compte 38 blocs (`g2/cc/diff-v1-v2.txt`, `g2/cc/opcodes.txt`). Chacun relève de C1 à C8 ou d'une observation appliquée, à quatre exceptions près, toutes sans effet sur le fond :
- un resserrage de vocabulaire, « non vérifié(es) » et « invérifiés » devenant « non recoupé(es) » (L106, L135, L264) ;
- le titre du §7 (L284) ;
- la ligne de date et le modèle de la révision (L5) ;
- l'ajout du §8.

Aucun fait, chiffre ou date n'a changé hors des corrections. La précision ajoutée sur Drift (L208) est fidèle à la copie : Chainalysis écrit “which has not yet been independently verified by a completed third-party investigation”.

**Traçabilité.** J'ai rejoué `apply1.py` puis `apply2.py` sur v1 ; le résultat (`g2/cc/sim/…`, sha256 `b5575f0a…`) diffère de v2. Les lignes L135, L204, L208, L264, L280, L284 et L291–292, ainsi que le §8 lui-même, ont été retouchées hors scripts, alors que le §8 dit que « les remplacements sont dans `apply1.py` et `apply2.py` » (R4).

### (5) `sha256sum -c`

205 lignes OK, code de sortie 0 (`g2/cc/sha-check-v2.out`). Couverture complète : tous les fichiers du dossier hors `g2/` sont listés, dont les quatre nouveaux. C'est conforme au §7 (L291–292 : « hors `g2/` »).

## 2. Reprises (liste fermée)

**R1 — Échelle de confiance du §3.1 (L197) et attributions (L201–L210).**

L'échelle énoncée dit :
- *élevée* : un primaire recoupé par une autre copie ;
- *moyenne* : une ou plusieurs secondaires concordantes, ou un primaire non recoupé ;
- *faible* : une seule secondaire non recoupée.

Sept lignes la contredisent :
- Loopscale (L203), Moonwell 2025-10-10 (L204), wrsETH (L205) et MAMO (L210) sont cotés « élevée », alors qu'aucune autre copie ne recoupe ces primaires (soit « moyenne » selon l'échelle) ;
- MarginFi (L201), JELLY (L202) et POPCAT (L206) sont cotés « moyenne » avec une seule source secondaire (soit « faible » selon l'échelle).

Choisir l'une des deux voies :
- **(a) Réécrire l'échelle** pour qu'elle décrive les attributions. Par exemple : « élevée = document de l'acteur ou de son gestionnaire de risque, qui détaille les transactions ; moyenne = presse ou analyste spécialisés, ou primaire partiel ; faible = article généraliste isolé ». Puis revoir chaque ligne, y compris « moyenne pour Sui » en L211, plus prudent que l'échelle.
- **(b) Garder l'échelle et ajuster les sept lignes.**

Dans les deux cas, mettre le §8 (C5 a et g) en accord.

**R2 — §3.3 point 1 (L222).** « Shōgen mesure une relation entre sources (racines communes) » restreint Shōgen à R2, contre la définition de L116 (R1 = écart entre sources d'un même actif ; R2 = carte des racines communes).
- Écrire « (écarts entre sources d'un même actif, R1 ; racines communes, R2 : §1.7) ».
- Pour la famille « flux erroné (wrsETH/ETH) », soit l'inclure dans « ce qui touche une relation entre prix de sources », soit dire pourquoi elle en est exclue. Une valeur aberrante d'un seul flux est en principe un écart de source au sens de R1 dès qu'il existe d'autres sources de la même paire (hors S2-bis) [inféré].

**R3 — `quotes.txt` (fin de C2 a).**
- Supprimer la ligne 1 (`pages/2nd-solanafloor-hylo.derived.txt|| `, citation vide).
- Rattacher “suspected” (ligne 2, aujourd'hui `pages2/inc-switchboard-shutdown.txt`) à `pages2/x-fullsail-2026-08-29.txt`, puisque les quatre occurrences (L20, L211, L224, L307) l'attribuent à Full Sail.
- Relancer `chk.py`.

L'affirmation du §8 (L304) « plus de ligne vide, plus de copie voisine » deviendra alors exacte.

**R4 — Traçabilité du §8 (L299).** Ajouter à un script, par exemple `corrections-g2/apply3.py`, les retouches faites hors scripts : L135, L204, L208, L264, L280, L284, L291–292 et le §8. À défaut, écrire au §8 qu'elles ont été faites à la main, en les listant.

**R5 — Forme.**
- (a) L202 : « un trader aurait (“allegedly manipulated”) le prix du jeton » → « un trader aurait manipulé (“allegedly manipulated”) le prix du jeton » (le verbe manque).
- (b) L307 : ‘no reports of similar behavior on Solana’ → “no reports of similar behavior on Solana”. Une citation web va entre “ ” ; c'est un fragment mot pour mot du post-mortem.

**Après les reprises** : régénérer `SHA256SUMS` et relancer `sha256sum -c`. Puis relancer `g2/cc/cites_v2.py`, en ajustant la désignation de “suspected” si la pièce change, et `chk.py`.

## 3. Observations hors liste (sans effet sur le verdict)

- **L291** : « `g2/` … jamais modifiée » est vrai du point de vue de l'auteur. Mais `g2/` reçoit les fichiers du réviseur, dont ce contre-contrôle : « non modifiée par l'auteur » serait exact.
- **L201** : « le protocole s'exprime “3 days after the incident” ». La source écrit “MarginFi contributor mrgnalt (@mrgnalt) issued a s tatement” : « un contributeur de MarginFi s'exprime » serait plus exact.
- **`INDEX-COPIES.md`** : 193 lignes pour 193 copies ; 127 avec URL, 66 « non consignée ». Les 98 URL données comme lues dans les octets y figurent toutes. Les 29 URL « déduites » sont étiquetées comme telles : 18 d'après le nom de la copie et un index, 6 audits d'après un lien et le nom du fichier, 5 sujets du forum Moonwell reconstruits à partir du `slug` et de l'`id`, la copie étant du JSON.
- **L119 et L138** : voir (3), acceptables.

## 4. Journal de provenance

- **Lu** :
  - la pièce v2 : §0, §1.3, §1.4, §1.7, §2, le §3 en entier, §4 à §8 ;
  - v1 ; `apply1.py` et `apply2.py` en entier ; `chk.py` ; les trois premières lignes de `quotes.txt` ;
  - `INDEX-COPIES.md` : en-tête, lignes Moonwell, Jupiter, Kamino et audits, et le paragraphe final ;
  - les copies : `inc-drift-chainalysis.txt` (pour la précision ajoutée) et, par mes scripts, toutes les copies désignées.

  Aucun fichier du dépôt n'a été ouvert pour ce contre-contrôle ; les règles S-G4 et S-G5 avaient été lues pendant la G2.
- **Commandes et sorties** :
  - `sha256sum` : la pièce donne `4aeb9860…`, la v1 `a24e7cf2…` ;
  - `sha256sum -c SHA256SUMS` : 205 OK, code 0 ; `comm` : seul écart, `SHA256SUMS` lui-même ;
  - `diff -u` v1 → v2 : 90 lignes `+` ou `-` ; `difflib` : 38 blocs ;
  - rejeu des scripts sur v1 : `lot 1 appliqué: 35`, `lot 2 appliqué`, sha256 `b5575f0a…`, différent de v2 ;
  - `cites_v2.py` : `citations 123 {'EXACT': 118, 'WS': 4, 'MD': 1, 'LARGE': 0, 'ABSENT': 0, 'NOMAP': 0} a reprendre 0` ;
  - `qalign_v2.py` : 110 lignes, 109 citations distinctes toutes couvertes, 1 ligne vide, 1 ligne sur une autre copie (“suspected”) ;
  - `chk.py` : `problemes: 0` ;
  - S-G4 approché : 0 ; R-13 : 0 ;
  - `INDEX-COPIES.md` : 193 / 127 / 66, et 98 URL contrôlées dans les octets, 0 absente.
- **Écrits** : `g2/CONTRE-CONTROLE-HYLO.md` ; dans `g2/cc/`, `sha-check-v2.out`, `listed.txt`, `present.txt`, `diff-v1-v2.txt`, `opcodes.txt`, `diff-scripts-vs-v2.txt`, `sim/HYLO-ET-AUTRES-CHAINES.md` (simulation des scripts, à ne pas confondre avec la pièce), `cites_v2.py` et `.out`, `qalign_v2.py` et `.out`, `chk-v2.out`.

## 5. Limites

Les vraies gates S-G4 et S-G5 restent à passer au versement : la limite L1 de `G2-HYLO.md` est inchangée. La table de désignation des citations nouvelles est la mienne, établie d'après leur contexte en v2.
