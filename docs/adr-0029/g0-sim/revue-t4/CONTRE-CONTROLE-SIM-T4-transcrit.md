# Contre-contrôle des corrections de SIM-BIS tranche 4 (transcrit)

> Transcription par l'orchestrateur le 2026-10-05 16:01:17 UTC du rapport rendu par message par le réviseur G2 (agent a16dbe18b742b1838) ; contrôle FM-1.1 : fragments_l51_l14 = 0. Texte du réviseur ci-dessous, sans retouche.

claude-opus-5-5

# Contre-contrôle des corrections G2 de SIM-BIS, tranche 4 (SB-14C à SB-14H)

- **Gate 0** : `claude-opus-5-5`, effort max. Je suis le réviseur de la G2 de la tranche ; je n'ai rien généré.
- **Horloge** (`date -u`, 2026-10-05) : de 15:37:59 à 16:00:21 UTC. Reprise depuis mes `NOTES.md`.
- **Dépôt** : tête `98c8537`, `git status` vide au début et à la fin ; aucune opération git en écriture.
- **Preuves** : `…/sim4/g2/cc/outils/` et `…/sim4/g2/cc/sorties/`. `…/sim4/g2/SHA256SUMS-REVISEUR` (119 entrées, `c49c27df…`) est OK. Copies lourdes supprimées.

## Verdict : CONFORME

Aucune correction demandée. Les observations plus bas ne bloquent pas.

## Pièces et série
- `corr/SHA256SUMS` : `4093f50d…`, 317 sur 317 OK. Les six diffs et le G0 figé (`a216a953…`, 92 lignes) sont à leurs empreintes.
- Copie `git archive 5f99ab5`, puis les 7 + 6 diffs : `apply --check` et `apply` sans échec.
  - Tailles : +76/−19, +70/−7, +60/−6, +92/−17, +22/−8, +21/−9. Toutes ≤ 200 ; ligne Python la plus longue : 120.
  - Chaque état est égal à l'étape correspondante du worker.
- Job (runner 33 ok, puis la ligne de `gates.yml`, sous `isole.sh`, borne 300 s) :
  - G0 ancien : e14c à 163, e14d à 166, e14e à 169, e14f à 170, e14g à 171, tous conformes ;
  - **e14h + G0 figé : 172 conforme** ;
  - e14h + G0 ancien : sortie 1, `test_g0_mesure` est le seul test en échec.

## Points demandés

1. **C-1 à C-5 : conformes.** Mes 20 mutants rejoués sur e14h (G0 figé) par la commande du job, borne 300 s : 23 exécutions (R-01 à R-03 en deux versions chacun), **21 tués, 2 vivants (R-16, R-17), 0 FATAL**, témoin 0/0 à 172.
   - Transposition : j'ai écrit mes propres versions de R-01 à R-03 ; elles coïncident avec celles du worker. R-03c reproduit exactement l'original (F de la classe de rang 1 sur les hôtes BTC) ; R-03p porte la mutation dans `parametres.json`. Tous sont tués par `test_composition_e1`.
   - Le pool BTC de `sources.classes` est identique, ordre compris, à `calibration.unites`.
   - Les autres corrections, tuées par leurs tests : R-04, R-06, R-07 (C-2) ; R-05, R-08, R-15 (O-1).
   - Q-T4-5 porte 5 701 ; « 5 707 » a disparu (C-4). Q-T4-11 et Q-T4-12 sont marqués dans le code (C-5).
   - Les citations de l'avis (l.23-25 à l.77-80) et de la PROPOSITION correspondent aux titres. Les empreintes du brief (`5e4487bc…`) et de l'avis (`6dfc13e7…`) sont exactes.
   - Survivants justifiés : R-16 est équivalent pour la sélection (minimum sous `_rang`, ordre total, cellules nommées par point). R-17 est indétectable en local ; en CI, l'échec est fermé.
2. **C-3 : oui, le renommage suffit pour les valeurs, pas pour le savoir.**
   - Valeurs : tous les noms d'E1 en vigueur au moment du coup d'œil sont caducs (les points par Q-T4-8, C0 par SB-14G). Aucun flux neuf n'a été imprimé : les sondes ne sortent que des empreintes, et les cellules des tests et les miennes sont hors de la forme d'E1. Aucune réplication de la future sortie épinglée d'E1 n'a donc pu être vue.
   - Ce n'est pas un choix de graine : un seul renommage, dont le motif est écrit avant tout regard sur les flux neufs.
   - Le savoir (le constat) ne s'efface pas. Il reste déclaré sous E-4, avec les valeurs vues, au JOURNAL, et il est déjà cité comme motif par l'ajout daté du G0.
3. **Q-T4-8, O-1, O-3, O-7 : conformes.**
   - Noms recalculés hors du code : 65 distincts, aucun « / », égaux à ceux de `cellule`, `E1-C0` absent.
   - O-3, contrôlé en processus neufs : même épingle (source changée), même module ; autre commit ou autre empreinte après chargement, `ORACLE/epingle` ; mauvaise empreinte au premier appel, `ORACLE/sha256`.
   - O-7 : refus `E1/ell`, `E1/classe` et `E1/strate` vérifiés (`E1/strate` par le test et par le mutant).
4. **SB-14H : le fil d'alarme est sain.**
   - Le test hache le G0 présent dans l'arbre et le compare à l'épingle : la seule façon de passer est le bon fichier.
   - Le G0 figé ne contient ni CR ni octet 92, se termine par LF et commence exactement par le G0 de 5f99ab5. Avec `* text=auto eol=lf`, son empreinte est stable au checkout, Windows compris.
   - `G0_SUBSTITUT` n'existe que dans `leger.sh` du worker, pour copier un G0 dans un arbre léger. Il est absent du lot et ne peut pas contourner le test.
5. **Identité** (Python 3.10 à 3.13) :
   - `4054de39…` 16 sur 16 sur e14h ; ma sonde `aa35ad01…` 16 sur 16 ;
   - `ca650d2e…` sur e14f (4 sur 4) et par la sonde « C0 ancien » sur e14h (2 sur 2) ;
   - `6998101d…` sur e14b (4 sur 4) et par la sonde « noms anciens » sur e14h (2 sur 2). Seuls les noms ont changé ;
   - T2 et T3 inchangées (4 sur 4 chacune) ; mode strict 8 sur 8, 172 tests.
6. **Portes** (5f99ab5 + 13 diffs + G0 figé) :
   - s2bis 156 conforme ; s2-harness 405 OK (skipped=2) ;
   - hooks 54, model-pinning 95, secrets 147 ; `gate-secrets` OK (26 fichiers) ;
   - R-13 : 0 constat, témoin positif 1 ;
   - octets 92 : 0 dans le lot, les diffs, les outils, le journal, les étapes, les NOTES et le G0 figé ; 4 dans `gates.yml`, venus de la base ;
   - xtask, série et base : S-G1 à S-G8 VERT ; fmt, no_std et clippy VERT ; S-G9 ROUGE, 1 violation, la mention connue de `docs/17:70` ; section identique (`87b165c4…`).
7. **Information (98c8537)** : rien d'autre que `fetch-depth: 0`.
   - `gates.yml` de la tête plus les hunks des 13 diffs, qui s'appliquent sans échec ; runner de la tête : 76 ok, 1 échec (K-03), et 77 ok sans la ligne.
   - Un premier essai avec le `gates.yml` de 5f99ab5 donnait aussi un échec K-01 : c'était un artefact du mélange, refait correctement.

## Observations (non bloquantes)
- **Lignes pour le brief du diff d'intégration.** Le README et le `rattachement` de SB-14H ne nomment que C1 et `ell_c1`. L'ajout daté change aussi :
  - le calendrier d'E1, point (3) : `masque_j28` remplace les positions de Q-T4-5, dont le texte deviendra caduc ;
  - le niveau de durée (5), pour SB-12 ;
  - les impressions (6), pour SB-11 ;
  - l'ordre (7).
- **Au commit** : mettre à jour `docs/adr-0029/g0-sim/SHA256SUMS`, qui porte encore `d9cffc0a…` pour le G0. L'épingle de l'ADR (`b908842d…`) sera à mettre à jour au gel de son ajout daté ; aucun fil d'alarme ne la lit.
- **O-2, après CB-18v** : un K-03 qui exigerait `fetch-depth: 0` ferait mourir R-17.

## Mes écarts
- Des `\|` tapés dans des `grep` de lecture, pour l'affichage seulement ; aucun fichier écrit ainsi (0 octet 92 dans mes 119 fichiers).
- Un PID trouvé dans `/proc` par un motif étroit, celui de mon propre script.
- `AVIS-SIM-T4.md` lu, comme le permettait le message.

**PID réels** : campagne 5328, identité 5611, portes 13573 ; tous finis.
