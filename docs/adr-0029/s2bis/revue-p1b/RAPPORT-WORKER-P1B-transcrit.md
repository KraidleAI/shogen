# Rapport du worker, tranche B de P1 (CB-3, CB-4, CB-5, CB-10, CB-11) — transcription par l'orchestrateur

Le harnais du worker interdit les fichiers de rapport ; rapport rendu par message (worker `claude-opus-5-5`, effort max, 2026-10-04
20:36:28 à 23:15:18 UTC), transcrit ici dans ses éléments vérifiables. Brief : `…/p1b/BRIEF-P1-B.md` (sha256 `0c6a2585…629d`).

## Livraison
Base de rendu : tête `1572f50` (tranche A commise jusqu'à CB-2e) ; s'applique aussi sur `435fa12`. 8 diffs en série dans `…/p1b/diffs/`,
SHA256SUMS de `…/p1b/` (230 lignes ; sha256 du fichier `987b4de4…c67b`) :

| diff | objet | code ajouté | plancher |
|---|---|---|---|
| CB-3a | `lecture.py`, octets de la requête, analyse de la réponse | 200 | 58 |
| CB-3b | `lire` : IPv4, phases, TLS, délai global, attrape-tout | 199 | 67 |
| CB-4 | boucle : plan par hôte, pool borné, échéance, `sante`, marqueur, résultats tardifs | 200 | 73 |
| CB-5 | tests T-LP-1 à T-LP-6, test de borne du corps | 135 | 81 |
| CB-10a | DNS filaire : requête et analyse | 142 | 85 |
| CB-10b | requête UDP (source, identifiant, délai) | 85 | 87 |
| CB-11a | sondes D-3 (brute), D-4, D-5, disque, empreinte du résolveur | 170 | 91 |
| CB-11b | sondes branchées à la boucle, liste blanche de `sante` | 40 | 92 |

Tests 49 → 92 ; rouge puis vert montré pour les 8 diffs ; mutants 114 nommés, 114 tués (CB-3 29, CB-4 16, CB-5 14, CB-10 30, CB-11 25) ;
suite s2bis `--aucun-saut --egal --plancher 92` conforme ; 3.10 à 3.13 avec `-X dev -W error` OK ; runner 32, hooks 54, S2 405,
secrets OK, R-13 0 ; xtask : S-G1 à S-G8 vertes, S-G9 rouge identique au témoin (copie sans `docs/rapports`). Preuves : `journal-d/`.

## Écarts déclarés (à adjuger)
- E-1 tailles : 1 171 lignes contre ≈ 880 au G0 (×1,33) ; CB-3, CB-10, CB-11 en deux diffs.
- E-2 trois bases successives, rejeu complet sur la dernière.
- E-3 choix de conception : (a) pas de ThreadPoolExecutor (futurs `concurrent.futures.Future` et fils démons ; écart à la lettre de
  l'ADR l.233, motivé par un essai mesuré : un fil pendu bloque la sortie du processus) ; (b) lecture non partie comptée, jamais
  écrite ; (c) D-2 brut (`retard_max` µs, `non_parties`) ; (d) partage des clés de `sante` entre CB-4 et CB-11 ; (e) D-3 : sortie brute
  d'une commande scellée journalisée sans analyse (écart au test « analyse de la sortie de chronyc sur une sortie gelée » : aucune
  source primaire du format accessible) ; (f) requête octet pour octet celle d'urllib, User-Agent de S2, **aucune redirection suivie**
  (S2 les suivait), corps plafonné à 1 Mio ; (g) marqueur sans champ propre (FORMAT §2 corrigé) ; (h) échelles de temps des tests T-LP ;
  (i) DNS : TXT en latin-1, pas de repli TCP si TC (drapeau journalisé).
- E-4 exposition : vers 20:42 UTC, un `grep -rn` récursif sur tout le dépôt, dossiers interdits compris, lignes des dossiers interdits
  filtrées avant affichage (3 lignes de chemins permis affichées) ; vers 20:44-20:46 UTC, deux `grep -rl` et un `du` sur tout le
  scratchpad de la session, arrêtés (liste du premier niveau et 5 chemins affichés, aucun contenu). FM-1.1 de sa transcription :
  0 fragment.
- E-5 Node 22 de l'hôte utilisé comme contre-contrôle (c-ares) en boucle locale ; aucune dépendance au dépôt.

## Effets des corrections de la tranche A et items B.60
C-1 compatible (ws ne recule jamais dans la boucle) ; C-2 : `OSError` ou `JOURNAL/casse` sort de `tourner` par propagation, la
fermeture du journal revient au point d'entrée (CB-18) ; aucune méthode ajoutée à `Journal`. SHOGEN-S2BIS-CORPS-BORNE-1 : fermé par
construction (plafond 1 Mio ; ligne au pire 1 398 622 octets < LIMITE 4 194 304 ; test et mutant). HORLOGE-RECUL-JOURNAL-1 : non fermé
(proposition : sommeil jusqu'à l'instant et champ `recul` dans `sante`, ≈ 40 lignes). ECRIVAIN-USAGE-1 : un seul fil écrit par
construction, sans garde mécanique ; « fermer et sortir » à CB-18.

## Items proposés
I-B1 SHOGEN-S2BIS-CHRONYC-FORMAT-1 (format de `chronyc` lu sur pièce avant le gel) ; I-B2 chemin TLS réussi non testé (smoke CB-16) ;
I-B3 pas de repli TCP si TC (D-5, CB-12) ; I-B4 la boucle ne contrôle pas que chaque nom du plan a sa lecture (test de câblage CB-18) ;
I-B5 incident d'exposition E-4.

## Questions du worker
1 découpage et un commit par diff ; 2 ajout daté pour l'écart E-3 (a) ; 3 D-3 brut ; 4 aucune redirection et User-Agent de S2 ;
5 HORLOGE-RECUL et fermeture ECRIVAIN-USAGE dans un CB-4c ou dans CB-18 ; 6 TC DNS sans repli TCP.

## Estimation
Tranche A 1 323 lignes (×2,36) ; tranche B 1 171 (×1,33) ; CB-18 ≈ 300 à 420 lignes ; P1 ≈ 3 000 à 3 250 lignes avec corrections.
