# Rapport du worker — corrections de SIM-BIS tranche 4 (transcrit)

> Transcription par l'orchestrateur le 2026-10-05 14:54:57 UTC du rapport rendu par message par le worker (agent af8b331845071f4b5) ; contrôle FM-1.1 : fragments_l51_l14 = 0. Texte du worker ci-dessous, sans retouche.

claude-opus-5-5

# Rapport du worker : corrections G2 et avis de la tranche 4 de SIM-BIS (diffs SB-14C à SB-14F)

- **Gate 0** : je tourne sous `claude-opus-5-5`, effort max.
- **Horloge** (`date -u`, 2026-10-05) : de 13:59:25 à 14:52:38 UTC.
- **Dépôt** : je l'ai lu par `git --no-optional-locks`, sans aucune écriture git.
  - Au début, tête `5f99ab5`, `git status` vide.
  - Pendant le lot, l'orchestrateur a fait avancer la tête : `0ae230d` à 14:36, puis `4da60cc` à 14:51. À la fin, 5 fichiers sont indexés par lui ; je n'y suis pour rien.
- **Base** : copie `git archive 5f99ab5` avec les 7 exclusions (786 fichiers, manifeste `00d8e4c4…`).
  - J'y ai appliqué SB-9A à SB-14B, chaque diff contrôlé contre `sim4/SHA256SUMS` (`f6c05f94…`).
  - Le résultat est identique à l'étape e14b de la tranche.

## Résumé, point par point

**1. Livraison** : 4 diffs en série après SB-14B. Chacun est vert seul, à son plancher exact, par la commande du job (runner : 33 ok, puis la ligne de `gates.yml`).

| diff | contenu | code + / − | plancher | sha256 |
|---|---|---|---|---|
| SB-14C | C-1 (composition `e1.fond` lue par `replication`) ; Q-T4-8 (noms de cellule) | +76 / −19 | 163 | 1c44d423… |
| SB-14D | C-2 (cas de R-04, R-06, R-07) ; O-1, cas R-05 ; O-7 | +70 / −7 | 166 | 0cd3649d… |
| SB-14E | C-5 ; O-3 (cache indexé sur l'épingle) ; O-1, cas R-08 et R-15 | +60 / −6 | 169 | 6dc93d54… |
| SB-14F | mention d'adjudication des valeurs Q-T4-1 à Q-T4-13, forme P-2 de la tranche 3 | +92 / −17 | 170 | 55e6db36… |

- Total : code +298 / −49, README +9 / −9. Le lot passe de 4 962 à 5 211 lignes. La plus longue ligne Python ajoutée fait 120 caractères.
- La série complète (11 diffs) passe `apply --check` puis `apply` sur la copie de 5f99ab5, et le résultat est égal à e14f.
- Je l'ai aussi appliquée sur des archives de `0ae230d` et de `4da60cc` : le job sim-bis y est conforme à 170. P1-C ne touche pas `scripts/sim-bis`, donc le plancher sim-bis n'est pas à recaler. Les fichiers indexés mais non committés n'ont pas été testés.

**2. C-1, composition d'E1.**
- `parametres.json` porte désormais une section `e1.fond` : f = 1, pannes longues 0, autres 1, hors-enveloppe 0, classe BTC, avec sa source (E-S-38, PROPOSITION l.197, Q-T4-13, AVIS-SIM-T4.md l.77-80). Le schéma la contrôle.
- `replication` lit cette composition. Une classe hors de `sources.classes` donne le refus nommé `E1/classe`.
- `test_composition_e1` épingle la composition écrite à la main.
  - Les états produits sont égaux, hôte par hôte, à ceux de `sources.Replication` sous un fond écrit à la main.
  - Cinq retouches de `e1.fond` (f = 1/2, longues 1/2, hors-enveloppe 1/4 000, classe USDC, classe ETH avec autres = 2) donnent chacune l'état attendu, différent de l'état scellé.
- R-02 et R-03 du réviseur sont tués. Leur texte d'origine a disparu avec C-1, je les ai donc transposés, chacun deux fois : dans `parametres.json` et dans le code qui lit la composition. R-01 est transposé de la même façon et tué aussi.
- Non-régression : la sonde du réviseur garde son empreinte `aa35ad01…`, 16 fois sur 16.

**3. C-2, trois cas écrits à la main**, chacun tué par son mutant dans la campagne :
- R-04 : `test_egalites_kappa_puis_tau_d`. À κ égal, (1/100, 5, 240) contre (1/10, 5, 60) donne (1/10, 5, 60), donc τ_D avant φ. Le test vérifie aussi κ avant τ_D (tue M-14D-04).
- R-06 : `test_portee_ep_l6`. Un t0 répété à 1 787 770 860 donne `CALIB/forme`.
- R-07 : `test_selection_refus_nommes`. C0 absent donne `E1/point`.

**4. C-3, provenance des mesures de mise au point : non versées.**
- Ces mesures datent d'environ 12:30 UTC, avant le redémarrage du conteneur. Je n'en ai trouvé ni le script ni les sorties : ni dans `sim4/journal`, ni dans `outils`, `brouillons`, `ebauches` ou `interrompus` (fouille dossier par dossier). Je ne les reconstitue pas, et aucun `*.jsonl` n'a été lu.
- Je ne peux pas attester les noms de cellule employés. Dans le pire cas :
  - `E1-C0`, i = 0 à 9 : ce nom n'est pas changé par Q-T4-8 ;
  - `E1-1/10-50-4320`, i = 0 à 9 : ce nom est devenu caduc, car le flux d'E1 de ce point s'appelle désormais `E1-1_10-50-4320`.
- Déclaration E-4, avec les valeurs vues : FIV(240) de I_t ≈ 2,0 en calme et 2,2 en stress au point (1/10, 50, 4 320), contre 1,06 et 1,04 sous C0, sur 10 réplications. Pour le seuil de `test_regime_groupe` (binance seule, 5 réplications) : au moins 12,05 au point (1/10, 50, 1 440), au plus 1,41 sous C0.
- Aucune valeur d'E1 n'a été choisie sur ces mesures. La grille et le critère restent ceux du G0.
- Je peux attester en revanche que les cellules des tests versés (`E1-essai`, `E1-taux`, `E1-regime`, `E1-oracle`, `E1-fond`, `E1-x`) ne sont pas des cellules d'E1. La sonde T4 calcule bien des cellules d'E1 réelles, mais n'imprime que l'empreinte.
- Correction de la phrase du rapport précédent : tous les chiffres de ce rapport-ci sont recomptés par les commandes de `journal/`, sauf les valeurs de mise au point ci-dessus, non versées.

**5. C-4** : le bon chiffre est **5 701** (30 286 − 24 585) en calme, et 2 094 en stress. Recompté (`journal/c4_recompte.txt`) et écrit dans le texte de Q-T4-5 de `parametres.json`.

**6. C-5** : Q-T4-12 est marqué dans `oracle_r1.charger`, et Q-T4-11 dans `extraire`. Les deux marques sont contrôlées par `test_valeurs_avis_t4` ; le mutant M-14F-07 (marque retirée) est tué.

**7. Q-T4-8, modifiée par l'avis** : les noms de cellule prennent la forme `E1-<num>_<den>-<κ>-<τ_D>` (par exemple `E1-1_100-5-60`, ou `E1-1_50-5-240` pour φ = 2/100).
- La forme est écrite dans `e1.questions.Q-T4-8`.
- Elle est testée par `test_parametres_e1` (noms écrits à la main, 65 noms distincts, aucun « / ») et par `test_valeurs_avis_t4`.

**8. O-1, cas tués** :
- R-05 : `test_c1_egal_c2` (C1 peut être C2, lettre du G0).
- R-08 : `test_nettoyage_du_dossier`. Un processus neuf, avec un TMPDIR vide, crée un seul dossier `oracle_r1_…`, charge r1 depuis ce dossier, et ce dossier est vide à la sortie.
- R-15 : `test_schema_du_commit`. Un commit abrégé, en majuscules ou de 41 caractères donne `PARAMETRES/schema`.

**9. O-3** : le cache est indexé sur l'épingle (commit, dossier, fichiers et leurs empreintes ; la source n'en fait pas partie). C'était simple à faire.
- Même épingle : mêmes modules, sans nouvelle extraction.
- Autre épingle dans le même processus : refus nommé `ORACLE/epingle`, car un processus ne peut charger qu'un paquet `shogen_s2`. Cette limite est écrite dans la docstring.

**10. O-7** : `selection` refuse désormais par un nom au lieu d'une `KeyError` ou d'une `ValueError` :
- `E1/ell` si `ell_c1` est absent de `calibration.ell` ;
- `E1/strate` si une strate de la cible n'a pas de courbe, pour un point comme pour C0.

**11. Mention d'adjudication des valeurs Q-T4-1 à Q-T4-13** (forme P-2 de la tranche 3) :
- `parametres.json` porte trois blocs : `variante.questions` (Q-T4-1 à 4), `e1.questions` (Q-T4-5 à 10 et 13), `oracle_r1.questions` (Q-T4-11 et 12).
- Chaque question cite ses lignes de l'avis (l.23-25, 27-29, 31-34, 36-40, 42-45, 47-50, 52-54, 56-59, 61-63, 65-67, 69-71, 73-75, 77-80) et ses lignes de la PROPOSITION (vérifiées).
- La source de chacune des trois sections cite le brief (`5e4487bc…`) et l'avis (`6dfc13e7…`, « douze adoptées, Q-T4-8 modifiée », l.14).
- Le prédicat de schéma `commun.question_t4` tient cette forme. Le README la mentionne à cinq endroits, et chaque numéro est marqué dans le module qui l'emploie.

**12. Tests d'abord** : chaque pas montre un rouge d'assertion avant le code, sans aucune ERROR.

| pas | rouge avant le code | vert |
|---|---|---|
| SB-14C | 2 FAIL | 163 |
| SB-14D | 1 FAIL (O-7 ; les cas C-2 et R-05 sont verts sur le code et rouges sous leur mutant) | 166 |
| SB-14E | 1 FAIL (cache ; R-08 et R-15 rouges sous leur mutant) | 169 |
| SB-14F | 1 FAIL | 170 |

Mon premier rouge de SB-14C est sorti en ERROR (`ValueError` sur la conversion d'un masque de 46 468 bits). J'ai corrigé le test (helper `diff`) avant de retenir le rouge.

**13. Mutants** : classés par la commande du job, borne de 300 s.
- Campagnes par pas : 14C 13 sur 13 tués, 14D 8 sur 8, 14E 6 sur 6, 14F 7 sur 7 ; 0 FATAL.
- Campagne finale sur e14f (PID 1514, 48 exécutions) : 45 tués, 3 vivants, 0 FATAL, témoin 0/0.
  - Les 20 mutants du réviseur : tous tués sauf R-16 et R-17, comme prévu par l'adjudication.
  - Les 24 mutants neufs (M-14C-01 à M-14F-07) sont tués.
- Justification des trois vivants :
  - **R-16** est équivalent pour la sélection : le minimum se prend sous `_rang`, ordre total sur les points, donc l'ordre d'énumération n'y change rien. Les cellules sont nommées par point, pas par rang.
  - **R-17** est indétectable en local : les copies locales ont l'historique, et K-03 ne lit pas `with:`. En CI, sans `fetch-depth: 0`, le job échoue fermé (`ORACLE/extraction`), jamais vert en silence.
  - **M-VAR-1b** est équivalent, preuve à l'appui : pour |s| ≤ N, t − s ∈ [0, n). Contrôle exhaustif pour n de 1 à 12 : 334 050 cas, 0 différence. Hors du domaine, 87 384 cas et 43 692 différences, que `decalage` ne produit jamais.

**14. Identité bit à bit** (Python 3.10.20, 3.11.15, 3.12.3, 3.13.14 × PYTHONHASHSEED 0, 1, 4242, aléatoire) :
- Empreinte neuve, déclarée : sonde T4 du worker `ca650d2e71219e596de1b45f5a5d0fdf6814bf8602c6ff53498b72fbc218d375`, 16 sur 16. Elle change à cause des noms de cellule de Q-T4-8.
- Preuve que seuls les noms changent : la même sonde, avec les noms d'avant, redonne `6998101d…`, 16 sur 16.
- Sonde du réviseur `aa35ad01…` : 16 sur 16. Sondes T2 (`8d97a9dc…`, `d3ba1eb6…`) et T3 (`8895661a…`, `03304e5e…`) : 8 sur 8 chacune.
- Mode strict `-X dev -W error` : 8 sur 8, 170 tests OK.

**15. Portes**, sur la série complète :
- runner 33 ok ; sim-bis 170 ; s2bis 156 et s2-harness 405 OK (skipped=2), tous deux sous `isole.sh` (lo allumée).
- hooks 54, model-pinning 95, secrets 147 ; `gate-secrets --tree` sur 26 fichiers OK.
- R-13 : 0 constat. R-8 : bibliothèque standard et lot seuls (23 fichiers `.py`).
- Octets 92 : 0 dans le lot (25 fichiers), les diffs, les outils, le journal et NOTES. Les étapes en portent 37 chacune (4 dans `gates.yml`, 33 dans le runner), toutes venues de la base.
- `cargo --locked xtask verify`, série et base : S-G1 à S-G8 VERT ; fmt, no_std et clippy VERT ; S-G9 ROUGE, 1 violation, `17-modele-de-menace.md:70`. Verdicts identiques des deux côtés ; section S-G9 identique (`87b165c4…`).

## Items, sans code dans ce lot (limites rendues pour être formées)

- **O-2** : faire contrôler `fetch-depth: 0` par K-03, après le commit de P1-C qui touche le runner (SHOGEN-CI-S2-CABLAGE-1).
- **O-4**, deux lignes pour le brief de SB-11 :
  - l'oracle d'E-S-29 (200 premières réplications) doit couvrir la variante sur N1, N3, N4, N8, N9 et X1 (AVIS-SIM-T4 l.38) ;
  - imprimer, par point et par ℓ, l'écart-type des 200 FIV (AVIS-SIM-T4 l.50 ; SB11-IMPRESSIONS-1).
- **O-5** : le seuil 12,05 de `test_regime_groupe` est un seuil de non-régression mesuré, pas un oracle indépendant (E-S-53). Il est déclaré sous E-4.
- **O-6**, limite : sous E1, K vaut environ 20 à 50 fenêtres en calme, contre 148 pour EP. FIV(240) est donc très bruité d'une réplication à l'autre (0,94 à 6,6 au point extrême).
- **Item neuf, issu de C-3** : je ne peux pas exclure que les valeurs de `E1-C0` (i = 0 à 9) aient été vues avant E0. La décision revient à l'orchestrateur : déclaration au JOURNAL sous E-4, et éventuellement un nom de cellule C0 neuf avant E0.
- **Estimation** : les corrections ont coûté +298 lignes, soit environ 30 % des 982 lignes de la tranche, dans la fourchette prévue (+25 à 35 %).

## Écarts déclarés

- **E-1** : `manifeste.py` (`os.walk`) sur ma copie entière de la base, pour un compte et une empreinte seulement ; les dossiers exclus étaient absents.
- **E-2 à E-6** : barres obliques inverses tapées dans des commandes, cinq fois. Dans chaque cas, les octets écrits sont contrôlés : aucun octet 92 n'a été ajouté.
  - E-2 : apostrophes échappées dans un heredoc Python (ajout de `e1.fond`).
  - E-3 : délimiteur « / » échappé dans un `sed` sur `gates.yml` ; le fichier garde ses 4 octets 92 de la base, seul le plancher a changé.
  - E-4 : guillemets échappés dans un heredoc ; l'entrée concernée n'a jamais été écrite.
  - E-5 : un motif de `grep -c`, en lecture seule.
  - E-6 : un séparateur `awk`, sortie à l'écran ; tailles recomptées ensuite par `tailles.py`.
- **E-7** : parcours récursifs limités à mes propres dossiers (`scripts/sim-bis` des copies, `etapes`, `diffs`, `outils`, `journal`) : comptes et sommes seulement. Jamais `docs/`, le dépôt entier ni le scratchpad entier.

## Journal G1

**[lu]** :
- les briefs `BRIEF-CORRECTIONS-SIM-T4` (`5e4487bc…`) et `BRIEF-SIM-T4` (`52fd1b1b…`) ;
- `G2-SIM-T4-transcrit` (`4663486e…`), `AVIS-SIM-T4` (`6dfc13e7…`) et `RAPPORT-WORKER-SIM-T4-transcrit` (`fc178785…`), en entier ;
- les NOTES de `sim4` et du réviseur ; les outils, mutants et sorties du réviseur ;
- le G0 (`d9cffc0a…`) en entier ; PROPOSITION (`0e78afab…`) l.135, 138, 140, 172, 181-183, 187, 197, 198, 205, 207, 209, 522 ;
- le commit `1a906eb` (forme P-2) ;
- le code utile du lot à e14b ; `gates.yml` l.220-245 ; `isole.sh` (`ebaa1c78…`).

**[abs]** : ADR-0029, AVIS.md, annexe B, revue-t1 à revue-t3 (non relus pendant cette passe) ; EP, lu seulement par le code du lot, sous ses épingles.

**[2nd]** : l'arrondi correct de `Decimal.ln` et la stabilité de `random()` d'une version de Python à l'autre, recoupés par l'identité 16 sur 16.

**Exposition** : aucune pièce de D.2, aucun `*.jsonl`, aucun dossier exclu. `SHOGEN_S2_CAMPAGNE_CONTROL` n'a jamais été posée. Aucune valeur FIV de type E1 n'a été imprimée pendant cette passe.

**PID réels**, vérifiés par `/proc/PID/cmdline` : campagnes 16510, 20635, 24132, 30625 et 1514 ; identité 2230 ; portes 16626.

## Fichiers

Tout est dans `<scratchpad>/s2bis/sim4/corr/` :
- `diffs/SB-14C.diff` à `diffs/SB-14F.diff`, à appliquer dans cet ordre après SB-14B ;
- `etapes/` (e14b à e14f), `journal/` (rouges, verts, jobs, campagnes, identité, portes, comptes), `outils/` et `NOTES.md` ;
- `SHA256SUMS` : 219 entrées, sha256 `7a92d9b727717404ddce7b9d913234587eba1390f7bd38796f0992077fd6f85f`, `sha256sum -c` OK.

Les copies lourdes (base, série, travail, cible cargo, TMPDIR) sont supprimées.
