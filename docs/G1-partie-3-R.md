# Journal G1 — partie 3 de S2, étape R (rédaction du paquet)

**Nature** : rapport du rédacteur frais (`shogen-worker`, `claude-opus-5-5`), versé tel quel par l'orchestrateur le 2026-10-02 (fichier source sha256 `8007951e3be5d218b0d243340bee1add13558277a7afbf2ad751e22e544a6911`) ; adjudication et contrôle FM-1.1 : annexe B, bloc B.32, et JOURNAL.


Rédigé le 2026-10-02, de 16:06 à 16:42 UTC (`date -u` lu à 16:06:42, 16:21:36, 16:31:37, 16:35:54, 16:37:48, 16:40:21, 16:41:14). Rattachement : `docs/adr-0028/G0-partie-3.md`, section « R » (l.47-86) ; ADR-0028 D2 ; annexe A, ligne PAQUET (l.39). Base : `partie-3-paquet` à `8b14567` (arbre propre au départ). Aucune opération git en écriture ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée (la suite a tourné sous `env -u`).

## 0. Gate 0

Modèle sous lequel tourne ce rédacteur : **`claude-opus-5-5`** (identifiant exact déclaré par l'environnement : “You are powered by the model named Opus 5.5. The exact model ID is claude-opus-5-5” (guillemets anglais posés au versement : énoncé de l’environnement, hors corpus S-G5)). Effort demandé par la fiche : max.

## 1. Attestation D.3

**Je n'ai vu aucun z, aucun K, aucun P̂_more, aucun φ de campagne, et je n'en ai calculé aucun. Je n'ai lu aucun taux d'écart ni de panne d'une source de la campagne. Je n'ai ouvert aucune pièce de la liste fermée D.2 (points 1 à 11), aucun journal de campagne ni copie, aucun fichier du dossier de la pièce D.2 n° 6, ni la cartographie du 2026-09-29 (pièce D.2 n° 5), ni la transcription de session de l'orchestrateur (D.2 n° 11).** Les z, K, P̂_more et taux que j'ai lus portent sur des données synthétiques seules (sorties de SIM-NIVEAU et de l'étape S).

- **Exposé à** (classe M ou constantes, tous portés par des pièces autorisées) : comptes de l'ADR (D1 : 0 `ok` sur 40 804 lectures de Pyth, HTTP 401 ; D5 : 5 313 `asn_attribution` dont 815 `resolve_failed`, 483 `clock_check`, `resolve_failed` 15,3 % dans la plage contre 1,85 % hors plage ; n = 35 982, 17 314, 9 261 ; bornes calendaires de §1 bis.2 : n ≈ 2,5·10⁴ et 10⁴, 5 760, 2 880, n_stress ≤ 2 061) ; annexe B l.38 (« 645 fenêtres ont été sautées alors que le harnais tournait », citation de la cartographie l.34 portée par l'annexe) ; annexe D l.159 (4 093 `run_params`) ; les noms des pièces de D.2 (texte de D.2) ; l'attestation D.3 (a), dont les deux valeurs sont masquées dans le texte (je ne les ai pas vues) ; résultats synthétiques de SIM-NIVEAU et de l'étape S ; sujets de commits (`git log`, chemins de code seulement).
- **Noms vus sans ouverture** : listage du dossier de travail partagé de la session (noms de dossiers d'autres agents, aucun ouvert ; seul mon dossier `paquet/` a été lu et écrit) ; listage de `docs/` (noms de dossiers, dont celui de la pièce n° 6 et `rapports/`, non ouverts) ; listage de `docs/adr-0028/` et de `docs/adr-0028/sim-niveau/` ; noms des fichiers ignorés de `biblio/` (`git status --ignored`).
- **Sortie d'outil persistée par le harnais** : la première lecture de `garde_niveau.txt` par `cat` a été versée par l'outil dans un fichier de résultats hors de mon dossier ; je ne l'ai pas ouvert (relecture faite sur la source par `Read`).
- **Contrôle FM-1.1 de ma transcription (déclaration pour l'orchestrateur)** : des chaînes de D.2 figurent dans des entrées de mes appels d'outils, sans ouverture de pièce : (1) un appel Bash de comptage (avant 16:21 UTC) : `find docs s2-harness -name '*.md'` avec exclusion à la source du dossier de la pièce n° 6, puis comptes seuls (`wc -l`, `grep -c`) des `.md` de ce dossier sur le disque et dans l'index (résultat : 1 et 1 ; aucun nom ni contenu affiché) — contrôle de SHOGEN-PERIMETRE-DISQUE-1 (a) ; (2) le script `controles.py` (écrit par heredoc, lancé cinq fois) porte une liste de motifs de D.2, cherchés **dans mon paquet** pour s'assurer qu'il n'en contient aucun (résultat : 0) ; (3) trois appels `grep -c` sur mes propres sorties de `xtask verify`, avec une expression de motifs de D.2 (résultat : 0 chaque fois), faits **avant** d'afficher ces sorties ; (4) le bloc machine du paquet et `sonde_bloc.py` portent les trois noms nus des journaux scellés, exigés par le format (G0 de la partie 2 §C ; fiche de mission). Aucune autre occurrence attendue. Je ne recopie pas ces motifs ici, pour ne pas en ajouter.
- **Écart à une consigne déclarée** : CLAUDE.md demande à toute session cloud de lire d'abord `docs/PASSATION-CLOUD.md` ; je ne l'ai pas ouvert, la fiche fixant une liste fermée de sources autorisées sous la règle absolue de D.2 (question Q-11).

## 2. Fichiers ouverts (avec lignes)

**Sources autorisées par la fiche** :
- `docs/adr-0028/G0-partie-3.md` : entier (l.1-86).
- `docs/adr-0028/ADR-0028-decisions-sortie-S2.md` : entier (l.1-328) ; l.93-110 extraites telles quelles dans `regle-original.md` (sha256 `c17f1a56…684f`).
- `docs/adr-0028/ANNEXE-A-lots.md` : entier (l.1-128). `ANNEXE-B-items.md` : entier (l.1-464). `ANNEXE-C-MAST.md` : entier. `ANNEXE-D-preenregistrement.md` : entier (l.1-176 ; liste D.2 lue, pièces non ouvertes). `ANNEXE-E-avis-non-suivis.md` : entier, lignes coupées à 400 caractères.
- `docs/adr-0028/LECTURES-PARTIE-3.md` : entier (l.1-117).
- `docs/adr-0028/G0-partie-2.md` : entier (l.1-188).
- `docs/adr-0028/sim-niveau/` : `sim_niveau.txt` (l.1-22), `garde_niveau.txt` (l.1-67), `SHA256SUMS` (l.1-18), `oracle4.json`, `oracle4-3414e0f.json`, `garde_niveau_oracle_r1.json` (entiers) ; sha256 recalculés de huit fichiers, `sim_niveau.json`, `garde_niveau.json` et `oracle_4a_4b.json` non affichés.
- `docs/G1-partie-3-S.md` : l.1-100, l.170-259, l.347-366, et recherches ciblées. `docs/G1-lot-SIM-NIVEAU.md` : l.92-151 et recherches ciblées (l.1-16, l.148, l.193-194).
- `docs/G1-partie-2-P0.md` (recherche ciblée : l.3-88, l.316-328), `docs/G1-partie-2-corrections-G2.md` (l.25, l.44, l.258-268, l.338, l.368-370), `docs/G1-partie-2-etape-B-2.md` et `-B-3.md` (recherche ciblée de L10 et du harnais vivant) ; `docs/G2-partie-2.md` (recherche de « paquet », l.113-140, l.405-432).
- `docs/08-assumptions.md` (l.28-31, l.39, l.42), `docs/09-vocabulaire.md` (entier), `docs/10-mesures-pilotes-design.md` (titres ; l.277-331, l.374-498, l.539-593), `docs/17-modele-de-menace.md` (l.82-109).
- `biblio/INDEX.md` : l.3, l.54, l.328, l.336-338 (recherche ciblée).
- `s2-harness/` (code) : `tools/rendu_unique.py` entier ; `tools/oracle_record.py` l.1-70, l.110-189 et recherches ; `shogen_s2/r1.py` l.55-74, l.300-395, l.605-630, l.677-705 et liste des `def` ; `shogen_s2/r2.py` l.866-990 ; `shogen_s2/records.py` l.351-419 ; `shogen_s2/report.py` l.563-567 (recherche « Fisher ») ; `shogen_s2/sources.py` l.299-305 ; recherche de « odds » dans `shogen_s2/` (0).
**Lectures d'outillage hors de la liste de la fiche** (pour ne pas m'exposer par la sortie de `verify`, tenir les gates et contrôler des affirmations ; aucune donnée de campagne) : `xtask/src/sg4.rs` (entier), `sg5.rs` (l.1-240), `documents.rs` (l.75-230, l.275-300), `rapport.rs` (l.60-110), `sg8.rs` (l.120-140), en-têtes de `sg6.rs`, `sg7a.rs`, `sg8.rs`, `lib.rs` (recherche) ; `scripts/sim/sim_niveau_calc.py`, `sim_niveau_oracle_r1.py`, `sim_niveau_oracle4.py` (lignes de recherche de `f5b8269` et `R1_BLOB`) ; `scripts/sceau/verify.sh` (l.1-30) ; `enforcement/hooks/pre-commit` (l.21, motif R-13) ; `.gitattributes` (recherche de « paquet », 0) ; git en lecture : `status`, `log` (sujets, chemins de code et de documents d'ADR-0028), `rev-parse`, `merge-base --is-ancestor`, `ls-files` (comptes).

## 3. Table de correspondance : section du paquet → sources

| section | sources (fichier, ligne, à `8b14567`) |
|---|---|
| en-tête | G0-partie-3 l.47-86 ; ADR l.29-42 ; annexe A l.39 ; annexe B l.14 ; annexe C l.13 ; sha256 recalculés des pièces ; annexe D l.5 (règle d'écriture) ; LECTURES l.15 (notation) |
| 1 | ADR l.32, l.37, l.241 ; annexe B l.164 (EX-E1-2) ; G0-partie-3 l.85-86 ; `rendu_unique.py` l.29 ; `git log` (sujets) et `git merge-base` (91 commits) |
| 2 | ADR l.21-27 ; annexe E l.54 ; annexe D l.176 |
| 3 | ADR l.58-62 ; annexe D.1 n° 8 (l.20) ; `records.py` l.351-381 ; `rendu_unique.py` l.39, l.46 ; G0-partie-2 l.177 ; recompte des époques (`recompte.py`) |
| 4 | ADR l.35 ; doc 10 l.392-395 ; annexe A l.34 ; `r1.py` l.306-317 ; annexe B l.223, l.224, l.310 ; G0-partie-3 l.54-56 ; LECTURES l.100-108 ; `biblio/INDEX.md` l.338 |
| 5 | ADR l.44-49, l.132, l.264-267 ; `biblio/INDEX.md` l.338 ; LECTURES l.117 ; recherche « odds » |
| 6 | ADR l.37, l.52-55 ; `rendu_unique.py` l.39-50 ; `records.py` l.384-391 ; G0-partie-2 l.177-179 ; recompte des époques |
| 7 | ADR l.118 ; G0-partie-2 l.176 ; annexe B l.98-103, l.224, l.310 ; annexe D l.171 |
| 8 | annexe D l.7-29, l.31-45, l.47-108 (renvoi, sha256 `329d5794…`) ; ADR l.39 ; annexe C l.13 ; annexe B l.144 |
| 9 | ADR l.40, l.42, l.149, l.153 ; annexe D l.112-118, l.121-130, l.141-153 ; annexe B l.163, l.380, l.392, l.412, l.416, l.423, l.445 ; G0-partie-2 l.115-133, l.180-183 ; `rendu_unique.py` l.29-54, l.83-105, l.151-306, l.341-360, l.419-500 |
| 10.1 | ADR l.91, l.112-114, l.126-128 ; annexe B l.97 ; `r1.py` l.71-74, l.677-704 ; `r2.py` l.949-985 |
| 10.2 | ADR l.93-110 (recopie) ; écarts : section 4 ci-dessous |
| 10.3 | `sim_niveau.txt` l.2-14 ; `garde_niveau.txt` l.2-26 ; `SHA256SUMS` l.11-16 ; `oracle4.json`, `oracle4-3414e0f.json`, `garde_niveau_oracle_r1.json` ; G1 SIM-NIVEAU l.96-103, l.148, l.193 ; G1 étape S l.17-58, l.169-172, l.243-250, l.350-355 ; annexe B l.342, l.460, l.462, l.464 ; `sim_niveau_oracle_r1.py` l.16-17 ; `git rev-parse` des blobs de r1 |
| 10.4 | `sim_niveau_calc.py` l.13 ; `r1.py` l.71 ; `r2.py` l.776 ; annexe B l.308, l.448-450, l.459 ; LECTURES l.25-31, l.42-44, l.52, l.59 |
| 11 | annexe D l.159, l.167-176 ; ADR l.139 ; doc 08 l.31 ; annexe A l.79-82 ; annexe B l.101 ; commits des lots |
| 12 | annexe B l.32, l.38, l.41, l.60, l.89, l.165, l.185, l.341, l.354, l.370, l.379-381, l.385, l.403, l.424, l.433-434, l.446-447, l.451 ; doc 10 l.285-297 ; ADR l.133-135 ; LECTURES l.86-92 ; `biblio/INDEX.md` l.328, l.337 ; `report.py` l.565-566 ; `oracle_record.py` l.41-42, l.154-156, l.163-164 ; `rendu_unique.py` l.392-398, l.435-437 ; `records.py` l.351-381 ; `r2.py` l.877-881 ; `r1.py` l.627 ; `sources.py` l.301-304 ; annexe D l.134-153 ; doc 17 l.108 ; doc 08 l.42 ; G0-partie-3 l.71-84 |
| 13 | G0-partie-3 l.73-78, l.85-86 ; G0-partie-2 l.115-118 ; `rendu_unique.py` l.25-36, l.83-105 ; annexe D l.143 ; sonde `sonde_bloc.py` |

## 4. Écarts à la recopie de §1 bis.1 (pts 1 à 11, ADR l.93-110)

Recopie mécanique (`transforme_regle.py`, sha256 `6381716b…bbb9`) : six remplacements exacts, chacun trouvé une fois ; texte d'origine `regle-original.md` (`c17f1a56…684f`), texte recopié `regle-paquet.md` (`843d0833…1e90`), présent octet pour octet dans le paquet (contrôlé par `count == 1`). Lignes touchées : pts 3, 7, 10 et 11 ; les autres lignes sont identiques. Ni ℓ, ni le seuil, ni la règle, ni aucune valeur ne changent.

| # | lieu | ancien texte | nouveau texte (résumé) | autorisation |
|---|---|---|---|---|
| E-1 | pt 3 | « (Künsch 1989 ; attribution sous la clause C-7 qui suit le pt 11) » | « (Künsch 1989, Thm 3.1, éq. (3.9), p. 1224 [lu] : poids v_n(k)/v_n(0), égaux à 1 − \|k\|/ℓ pour la suppression simple de blocs chevauchants de longueur ℓ [calc, éq. (3.6), p. 1223] ; les noms « Bartlett » et « blocs mobiles » ne sont pas de l'auteur [abs]) [C-7] » | clause C-7 (ADR l.114 : pages lues [lu], mention retirée) ; G0 §R l.60-61 ; SHOGEN-PT7-ATTRIBUTION-1 (annexe B l.448 : « ces pages et énoncés [lu] ») ; Künsch versé (`biblio/INDEX.md` l.336) |
| E-2 | pt 3 | (rien) après « γ̂_k centrés sur Ī_s = K_s/n_s » | « [ajout du paquet : SHOGEN-PT3-NORMALISATION-1 : γ̂_k = Σ_t (I_t − Ī_s)(I_{t+k} − Ī_s), sommes, et non moyennes, … ; γ̂₀,s = n_s·Ī_s(1 − Ī_s)] » | G0 §R l.61-62 ; annexe B l.449 ; contrôlé sur le code (`r1.py` l.322, l.346-353) |
| E-3 | pt 7 | « (Künsch 1989, Thm 3.2-3.3 [2nd : lu sur OCR par l'advisor-defi ; scan en procurement P-01, requis avant le scellement] ; attribution sous la clause C-7 qui suit le pt 11) » | « (Künsch 1989, corollaire 3.1, p. 1226, pour la moyenne d'une suite stationnaire, sous les conditions du Thm 3.3, p. 1225 : moment d'ordre 6+δ fini, Σ k²·α(k)^{δ/(6+δ)} < ∞ en mélange fort, ℓ = o(n), et ℓ(n) → ∞ [lu]) [C-7] » | clause C-7 ; G0 §R l.60-61 ; SHOGEN-PT7-ATTRIBUTION-1 ; LECTURES l.43-44 |
| E-4 | pt 10 | (rien) après « non évaluable ⇔ NON ÉVALUABLE, ou k_eff non évaluable. » | « [ajout du paquet : SHOGEN-CRITERE-PT10-CLAUSE-1, lecture (a)] Un k_eff connu seulement comme borne supérieure (hôtes sondés non attribués) n'établit pas l'égalité au k nominal du segment : « R1 discrimine » VRAI avec cette borne égale au k nominal rend le drapeau non évaluable. » | G0 §R l.63 ; annexe B l.308 ; conforme au code (`r2.py` l.973-977) |
| E-5 | pt 11 | (rien) après « (σ̂²_bloc biaisé vers le bas) ; » | biais de l'estimateur à poids triangulaires de l'ordre de −ℓ⁻¹·Σ_k \|k\|·R(k) (Thm 3.2 (i), pp. 1224-1225, et (3.10), p. 1224 [lu]) ; sous autocorrélations positives, σ̂²_bloc,s sous-estime et z_bloc,s surestime ; renvoi à SIM-NIVEAU (10.3) | G0 §R l.62-63 ; annexe B l.450 ; fiche, règle 1 ; LECTURES l.42, l.52 |
| E-6 | pt 11 | (rien) après « approximation normale à la garde ; » | z_s seul au-dessus de 0,01 près de la garde (cinq taux avec SE, trois au-dessus à deux SE) ; règle ≤ 0,00357 (SE 0,00034), 0 sur 6 000 sous dépendance ; aucune révision | fiche, règle 1 (SHOGEN-GARDE-NIVEAU-ZSEUL-1) ; annexe B l.459 (« limite écrite au pt 11 du paquet ») ; G0 §S (conséquence pré-déclarée) ; `garde_niveau.txt` l.7-26 |

Hors du texte de la règle (non comptés comme écarts, marqués en 10.4) : repères de ligne `r1.py:58` → l.71 et `r2.py:783` → l.776 à `8b14567`.

## 5. Items traités, un par un

| item | traitement au paquet | ligne de l'item |
|---|---|---|
| SHOGEN-PREREG-S2-1 | le paquet lui-même | annexe B l.14 |
| SHOGEN-PT7-ATTRIBUTION-1 | §10.2 pts 3 et 7 (E-1, E-3) | B l.448 |
| SHOGEN-PT3-NORMALISATION-1 | §10.2 pt 3 (E-2) | B l.449 |
| SHOGEN-BARTLETT-BIAIS-1 | §10.2 pt 11 (E-5) | B l.450 |
| SHOGEN-CRITERE-PT10-CLAUSE-1 | §10.2 pt 10 (E-4) | B l.308 |
| SHOGEN-GARDE-NIVEAU-ZSEUL-1 | §10.2 pt 11 (E-6) ; la ligne du repli §1 bis.3 n'est pas écrite : la forme scellée est la règle (§10.1) | B l.459 |
| SHOGEN-CRITERE-GARDE-NIVEAU-1 | §10.3, sorties de l'étape S avec SE | B l.305 |
| SHOGEN-SIM-NIVEAU-1 | §10.3, sorties avec SE | B l.104 |
| SHOGEN-SIM-R1-DERIVE-1 | §10.3, blobs de r1 (`1d6a908c…`, `ea921bb7…`, `ce1da3df…`, `7ae940ec…`) | B l.342 |
| SHOGEN-SIM-REJEU-GEL-1 | §10.3, acte de l'orchestrateur au remplissage | B l.462 |
| SHOGEN-GARDE-NIVEAU-N-1 | §10.3 (limites des mesures), hors du texte de la règle | B l.460 |
| SHOGEN-DEP-FENETRES-1 | §10.1 (fermé : forme scellée = règle) | B l.97 |
| SHOGEN-CRITERE-R1-1 | §10 | B l.56, l.106 |
| SHOGEN-POOLEE-SOURCE-1 (clause C-6) | §4, source par l'état de `biblio/` | B l.223 ; G0 §R l.54-56 |
| SHOGEN-POOLEE-BLOC-1 | §4 et §7 (limite, après l'exécution) | B l.224, l.310 |
| SHOGEN-RAW-FIN-1 | §12 pt 1 | B l.354 |
| SHOGEN-ENREG-G1-1 | §12 pt 2 | B l.370 |
| SHOGEN-ENREG-DELAI-CHAMP-1 | §12 pt 3 (3 600 s, exit 124) | B l.381 |
| SHOGEN-CENSURE-VIVANT-PORTEE-1 | §12 pt 4 | B l.379 |
| SHOGEN-RENDU-TABLE-REELLE-1 | §12 pt 5 | B l.403 |
| SHOGEN-RENDU-CLI-REPORT-1 | §12 pt 6 | B l.424 |
| SHOGEN-RENDU-JETON-MAIN-1 | §12 pt 7 | B l.433 |
| SHOGEN-RENDU-ORC-OCTETS-1 | §12 pt 8 | B l.434 |
| SHOGEN-RENDU-RENAME-FENETRE-1 | §12 pt 9 | B l.446 |
| SHOGEN-GO-PICKAXE-FUSION-1 | §12 pt 10 | B l.447 |
| SHOGEN-AXES-SIGMA-NUL-1 | §12 pt 11 | B l.341 |
| SHOGEN-PAQUET-ERRATUM-FISHER-1, SHOGEN-FISHER-SE-1 | §12 pt 12 (erratum z′/ρ, demi-largeurs recalculées, formulation du lecteur) | B l.185, l.451 |
| SHOGEN-TAU-REDERIV-1 | §11 (traitement) et §12 pt 13 (limite) | B l.32 |
| SHOGEN-CENSURE-INFO-1 | §11 et §12 pt 14 | B l.38 |
| SHOGEN-SEG-DEMARRAGE-1 | §12 pt 15 | B l.89 |
| Limite « sceau privé » (D.4 c) | §12 pt 16 et §9 | annexe D l.134, l.153 |
| EX-E1-1 | §9, garde (3) | B l.163 |
| EX-E1-2 | §1, §12 pt 20, §13 | B l.164 ; G0 §R l.73-75 |
| EX-E1-3 (décision « non »), limite T-17 | §12 pt 17 | B l.165 ; G0 §R l.71-72 |
| SHOGEN-COLLECT-PREVWS-1 (limite) | §12 pt 18 | B l.41 ; G0 §R l.79-81 |
| SHOGEN-ATTEST-ADVISOR-1 (limite) | §12 pt 19 et §8 | B l.60 ; G0 §R l.82-84 |
| Bloc machine (décision de remplissage) | §13 | G0 §R l.76-78 |
| SHOGEN-HOST-DEGRADED-1, -DP-JOURNAL-LOSS-1, bloc 6, E-D1b, SHOGEN-FLUX-QUASI-MORT-1 | §11 (D.5 amendée) | annexe D l.169-176 ; B l.101 |
| SHOGEN-EXPOSITION-ORCH-CLOUD-1 | §8 (D.1 n° 15, par renvoi) | B l.422 |
| SHOGEN-E1-SCAN-TRANSCRIPTS-1 | §8 (acte de l'orchestrateur, renvoi) | B l.144 |
| SHOGEN-RENDU-UNIQUE-1, SHOGEN-SCEAU-ANCRE-1 | §9, §13 (sha du script ; conditions de l'ancre) | B l.57, l.105 |
| SHOGEN-CONTENU-DEP-1, X-1 | §5, §12 pt 12 | B l.103 ; ADR l.132 |
| SHOGEN-RENDU-HOTE-1, -HOTE-ATTRIBUTS-GIT-1, -P3-HOTE-1 ; items de la procédure de la partie 4 | §9, par renvoi seulement (actes hors texte) | B l.392, l.423, l.445 et autres |

**Cas fermés par le rédacteur (règle FM-2.4, annexe C l.29), avec l'autre forme possible** :
1. Attribution de « type Mantel-Haenszel » (§4) : retenue « parenté de structure, non une identité [inféré] », la forme de D2 pt 4 étant dérivée ici ; autre forme : attribuer la forme de D2 pt 4 à la version de Cochran (1954) d'après Agresti p. 227 [2nd par Agresti]. Motif : le texte de la clause C-6 de la revue G2 de POOLEE est hors de mes sources (seul son résumé au G0 §R est lu) ; Cochran 1954 n'est pas versé.
2. Placement des chiffres de l'étape S dans le pt 11 (E-6, avec SE) plutôt qu'un renvoi seul à §10.3 ; autre forme : pt 11 sans chiffres, renvoi à §10.3.
3. SHOGEN-GARDE-NIVEAU-N-1 écrit en §10.3, hors du texte de la règle (la fiche n'autorise au pt 11 que deux ajouts) ; autre forme : ajout au pt 11, non autorisé ici.
4. Citation « 10 à 34 % » du pt 7 gardée (recopie ; aucune valeur ne change) et chiffres de SIM-NIVEAU imprimés à côté en §10.3 ; autre forme : remplacer la citation (question Q-G1-7 du journal G1 de SIM-NIVEAU l.193, ouverte dans mes sources).
5. SHOGEN-SEG-DEMARRAGE-1 : la règle d'appartenance est lue de D2 pt 6 (« appliqué par horodatage à tous les types ») et du code (`records.py` l.373) : chaque enregistrement de démarrage est dans le segment ssi son propre horodatage y est ; autre forme : rattacher les enregistrements de démarrage au démarrage qui les porte (non retenue : contraire à D2 pt 6).
6. Lecture (a) du pt 10 rédigée dans les termes du code (`r2.py` l.955-956, l.974) ; une borne supérieure inférieure au k nominal donne « éteint » par le texte d'origine (k_eff < k nominal établi), sans phrase ajoutée.
7. Table des commits (§1) : lots d'analyse et lots hors chemin d'analyse (D8a-c, E1) sur une ligne à part ; autre forme : omettre ces derniers.

## 6. Items non traités, avec motif

- **SHOGEN-FORMAT-JOURNAUX-1** (B l.55 ; « format … spécifié par référence (`records.py`, `journal.py` au commit `ed479c5` ; doc 10 §6) et scellé », déclencheur « avant le rendu ») : hors de la liste du G0 §R ; une ligne au §1 le scellerait avec le paquet (question Q-5).
- **Seuil de SHOGEN-FLUX-QUASI-MORT-1** (B l.101 : fixé avant l'exécution unique, par amendement daté de l'annexe B) : non fixé ici (hors G0 §R) ; question Q-7.
- **SHOGEN-G2-HISTO-RECALCUL-1**, **SHOGEN-CI-S2-SAUT-1** (avant le rendu), **SHOGEN-SIM-SOMMES-1** (relecture G2 de la partie 3), **SHOGEN-PERIMETRE-DISQUE-1 (b)** (décision d'ADR) : hors du texte du paquet. Mesure faite pour (a) sur cet arbre : `.md` sur le disque sous `docs/` et `s2-harness/` = 88 = `.md` de l'index (87 hors du dossier de la pièce n° 6, plus 1 dans ce dossier, compté sans affichage).
- **Actes de l'orchestrateur au lot PAQUET, absents à `8b14567`** : ligne `PAQUET.sha256 -text` de `.gitattributes` (ADR §1 bis.11 pt 9, l.171 ; annexe D l.142 ; recherche : 0) ; `docs/adr-0028/sceau/README.md` (pt 10, l.172 ; dossier absent de `docs/adr-0028/`).
- **Renvois datés de §1 bis.11 pts 13 à 16** (doc 10 §5.4, §5.6, §7 ; doc 04 §2) : non visibles aux lignes lues de doc 10 (l.478-483, l.549-553, l.581-586) ; actes de l'orchestrateur, hors de mon fichier.

## 7. Questions pour l'orchestrateur

- **Q-1** (Q-G1-7) : garder au pt 7 la citation « 10 à 34 % » (recopie) avec les chiffres de SIM-NIVEAU à côté (§10.3), ou trancher autrement (amendement daté hors de ce lot) ?
- **Q-2** (SHOGEN-POOLEE-SOURCE-1, clause C-6) : la formulation du §4 (« parenté de structure [inféré] ; Agresti 2013 p. 227 [lu] ; Mantel & Haenszel 1959 et Cochran 1954 non cités comme lus ») tient-elle la clause C-6, dont je n'ai lu que le résumé du G0 §R ?
- **Q-3** : chiffres de l'étape S dans le pt 11 (E-6) et SHOGEN-GARDE-NIVEAU-N-1 en §10.3 : placements acceptés ?
- **Q-4** : repères `r1.py:58` → l.71 et `r2.py:783` → l.776 en §10.4 (hors du texte de la règle) : acceptés ?
- **Q-5** : ajouter SHOGEN-FORMAT-JOURNAUX-1 au §1 (une ligne) ?
- **Q-6** : la ratification datée de la fermeture de la discordance (clause C-2, ADR l.113) est-elle posée ? Le texte recopié la suppose (pts 5 et 8) ; je n'ai pas lu le JOURNAL.
- **Q-7** : qui fixe, et quand, le seuil de SHOGEN-FLUX-QUASI-MORT-1 (auteur sans exposition aux taux de présence par flux) ?
- **Q-8** : `.gitattributes` (`PAQUET.sha256 -text`) et `docs/adr-0028/sceau/README.md` : à poser avant le scellement (§1 bis.11 pts 9-10).
- **Q-9** : garder la ligne « hors chemin d'analyse » (D8a-c, E1) de la table du §1 ?
- **Q-10** : constats périmés hors de mon fichier, à errata : doc 08 l.30 (« Künsch 1989 n'est pas détenue : OCR seul ») ; doc 10 l.288 (Fisher 1921 « non détenu ») ; docstring de `r1.block_long_run_variance` (`r1.py` l.323, « OCR seul, [2nd] ») et de `r1.regle_critere` (l.678-679, texte normatif « à f5b8269 ») — tout changement de code après le gel refait le bloc ; nom de l'item de modèle homogène : « SHOGEN-SIM-MODELES-1 » (annexe B l.464) contre « SHOGEN-SIM-NIVEAU-MODELES-1 » (journal G1 de l'étape S l.351).
- **Q-11** : lecture de `docs/PASSATION-CLOUD.md` non faite (consigne de CLAUDE.md pour toute session cloud ; liste fermée de la fiche) : à confirmer.
- **Q-12** : contrôle FM-1.1 : les occurrences déclarées au §1 (comptage, liste de motifs de `controles.py`, `grep -c` sur mes sorties, noms nus des journaux au bloc) sont-elles admises comme usages d'exclusion et de contrôle ?

## 8. Contrôles et sorties

- **Gates** : `cargo --locked xtask verify` sur l'arbre réel, avec le paquet en place : **`=== VERDICT GLOBAL : VERT ===`**, code 0, 16:40:21-16:41:14 UTC, sur la forme finale du paquet (`verify-final.out`, sha256 `c8bf32e0a1bf7b12c164cc2d9187bbb14c9e1960f5acf14c6577258a0f5099af` ; même résultat aux passages de 16:31 et 16:35 sur des formes antérieures). Avant affichage : code de sortie lu, 0 ligne « VIOLATION » ou « non contrôlé », 0 motif de D.2. Comparaison sans le paquet (fichier déplacé hors de l'arbre puis remis, 16:33 UTC ; `verify-sans-paquet.out`, `fba8830f…c625`) : VERT aussi ; seules différences : S-G4 87 → 88 fichiers, S-G5 88 → 89 fichiers, fragments contrôlés 276 → 276 (aucune citation anglaise ajoutée), écartés 3 194 → 3 279, et deux durées de compilation. Extrait de la sortie finale :

```
--- S-G4 — vocabulary (registre 09 mécanisé, voix du projet) ---
    docs/**/*.md : 86 fichier(s)
    s2-harness/**/*.md : 2 fichier(s)
  couverture : 88 fichier(s) examiné(s) sur 88 présent(s)
  VERDICT : VERT (0 violation(s))
--- S-G5 — citations (une-citation-un-grep, mécanisée) ---
    docs/**/*.md : 87 fichier(s) (extraction des « … » anglais)
    s2-harness/**/*.md : 2 fichier(s) (extraction des « … » anglais)
  couverture : 89 fichier(s) examiné(s) sur 89 présent(s)
  note : 276 fragment(s) de citation contrôlé(s), 3279 écarté(s) sous seuil (longueur ou langue — borne de couverture) ; corpus : INDEX + 128 artefact(s) local(aux) sur 128 déclaré(s)
  VERDICT : VERT (0 violation(s))
S-G1, S-G2, S-G3, S-G6 (128 sur 128), S-G7a, S-G8 (36 lignes) : VERT ; cargo fmt --check, no_std, clippy -D warnings : VERT
=== VERDICT GLOBAL : VERT ===
```

- **Suite `s2-harness`** (`python3 -B -m unittest discover -s tests -t .`, `env -u SHOGEN_S2_CAMPAGNE_CONTROL`, `TMPDIR` sur mon dossier, `PYTHONDONTWRITEBYTECODE=1`) : `Ran 383 tests` … `OK (skipped=2)`, code 0 (`suite.out`, `c7c39849…7052`) ; aucun fichier neuf sous `s2-harness/` (`git status --ignored` : seul `tests/__pycache__/`, préexistant).
- **Bloc machine** (`sonde_bloc.py`, `e7e7c440…78ad`, sur une copie hors dépôt de `rendu_unique.py` et `oracle_record.py`) : le paquet tel quel est refusé par `lire_bloc` (« ligne du bloc malformée … commit_analyse [à remplir …] ») ; avec des valeurs de fixture à la place des marqueurs, il est accepté (six clés, trois journaux `control`, `journal`, `raw`). Une seule ouverture de bloc (ligne 211).
- **Contrôles statiques** (`controles.py`, `443b2f26…7827`) : clôtures paires ; backticks pairs par ligne ; « » alternés et fermés ; aucun “ ” ; guillemets droits pairs par paragraphe hors code ; 0 locution mécanisée de S-G4 ; 0 forme « garanti », « vérifié », « prouv », « sûr », « reproductible », « sécurisé » ; 0 motif de D.2 ; noms de journaux seulement aux lignes 214-216 ; motif R-13 du hook : 0.
- **Recomptes** (`recompte.py`, `3b088ef2…bbb2`) : époques de D4, D5 et du J14 second ; demi-largeurs de Fisher à N = 300 avec 1,96/√297 : 0,1132 ; 0,0852 ; 0,0217 (ADR : 0,113 ; 0,085 ; 0,022) ; SE de neuf cellules des sorties de simulation, égales aux valeurs imprimées ; borne à x = 0 : 4,992·10⁻⁴ (R = 6 000), 2,996·10⁻⁵ (R = 10⁵) ; 30·240 = 7 200.
- **Commits** : les 91 jetons de 7 chiffres du paquet sont des commits résolus sans ambiguïté et ancêtres de `8b14567`.

## 9. Livrable

- `docs/adr-0028/PAQUET-PREREG-S2.md` : fichier neuf, non suivi. Forme remise à l'adjudication : 220 lignes, 58 999 octets, sha256 `c8ee6caf3f8b49f842241f2392d52db7d1c74b912c4865aa13342184525260e9`. **Forme finale après les corrections C-1 à C-5 (section 10) : 222 lignes, 60 508 octets, sha256 `ccbe67501bb2aa92f7d32a4b5541e1ae3bcd73efde56da1ad09f621638551a16`**, avant le remplissage du bloc par l'orchestrateur.
- Dossier de travail : `/tmp/claude-0/-home-user-shogen/7ba84933-ba6d-5813-9ef4-ca3ac4febd16/scratchpad/paquet/` (gabarit, recopie de la règle, scripts de contrôle, sorties).

## 10. Corrections C-1 à C-5 (adjudication de l'orchestrateur : ACCEPTE-AVEC-CORRECTIONS, liste fermée)

Reprise du 2026-10-02, de 16:46 à 16:49 UTC (`date -u` lu à 16:46:02, 16:47:29, 16:48:20 et 16:49:17, avant l'écriture de cette section). Mêmes règles que la fiche : aucune pièce de D.2 ouverte, aucune opération git en écriture, aucun caractère des pts 1 à 11 de §10.2 changé.

**Corrections appliquées** (script de remplacements exacts, chacun trouvé une fois ; gabarit avant correction conservé : `paquet-gabarit-avant-C.md`, paquet avant correction : `paquet-avant-C.md`) :
- **C-1** (§1, puce neuve avant la table des commits, ligne 15) : SHOGEN-FORMAT-JOURNAUX-1. Contrôle préalable : `git ls-tree ed479c5 -- s2-harness/shogen_s2/records.py s2-harness/shogen_s2/journal.py` liste les deux fichiers (le repli « `journal.py` absent » n'a pas servi) ; `git rev-parse ed479c5:<chemin>` : `records.py` blob `ef3f7c43e60687879c781c5532118d401f920d69`, `journal.py` blob `369012c2c6893559c891bdc5ec32b99b4ac3c62f` ; commit `ed479c5dd3b00aea521d339fbd63882af9e19023` ; doc 10 §6 aux l.555-579 à `8b14567` (titre l.555, §7 à l.581). Texte : « le format des journaux lus par le chemin de recalcul est spécifié par référence : … au commit `ed479c5` (… présence des deux chemins contrôlée par `git ls-tree`, blobs par `git rev-parse ed479c5:<chemin>`), et doc 10 §6 (l.555-579 à `8b14567`) », avec l'item et ADR D6 (vii), l.201.
- **C-2** (§10.1, ligne 111, phrase ajoutée après « … et ne sont pas recopiées. ») : « La clause C-2 (discordance, ADR l.113) est ratifiée par l'orchestrateur le 2026-09-30, sous veto (`JOURNAL.md` l.125 : « cas de discordance (z_s ≥ 2,33 ∧ z_bloc,s publiée < 2,33) = NE REJETTE PAS » par la forme « un seul test » (min) d'A-1 ; « la strate imprime l'énoncé de discordance ET l'EMD_s ») ; les pts 5 et 8 en dépendent. » Ligne du JOURNAL contrôlée par `sed -n '125p' JOURNAL.md` (seule ligne lue). Deux écarts de forme, déclarés : les marques de gras qui entourent « NE REJETTE PAS » à la source ne sont pas reprises (texte visible identique) ; la phrase de la source porte des guillemets imbriqués (« un seul test », « n'est pas rejeté ») : la citation est donc coupée en deux citations courtes sans imbrication (S-G4 apparie « » sans imbrication), la partie « par la forme « un seul test » (min) d'A-1 » restant mot pour mot entre les deux.
- **C-3** (§10.4, puce neuve, ligne 170) : correspondance avec Künsch 1989 : égalité du Thm 3.1, éq. (3.9), pour la covariance R̃_n de l'auteur (poids β_n(t, k) différents aux bords, centrage sur μ̂_n ; éq. (3.2)-(3.3), p. 1223, et (3.7)-(3.8), pp. 1223-1224 [lu]) ; avec les γ̂_k centrés sur Ī_s, correspondance sur les poids, approchée (`LECTURES-PARTIE-3.md` §1(a), point 1, l.33-34) ; sans effet sur ℓ, le seuil ni la règle. Paraphrase : la citation anglaise de la l.34 n'est pas reprise.
- **C-4** (§10.3, puce SIM-NIVEAU, ligne 149) : « la reprise de la citation est la question Q-G1-7 (même journal, l.193), sans effet sur ℓ, le seuil ni la règle. » → « décision de l'orchestrateur (adjudication du paquet, 2026-10-02) : la citation reste au pt 7 (recopie) ; les chiffres mesurés sont ceux de la table ci-dessus, au même p ; Q-G1-7 fermée ; sans effet sur ℓ, le seuil ni la règle. » (texte de l'orchestrateur, tel quel).
- **C-5** (§10.3, puce « Limites de ces mesures », ligne 165) : « SHOGEN-SIM-MODELES-1, annexe B l.464 » → « SHOGEN-SIM-NIVEAU-MODELES-1, G0 de SIM-NIVEAU l.239 ». Ligne contrôlée par `sed -n '239p' docs/adr-0028/G0-lot-SIM-NIVEAU.md` (seule ligne lue) : l'item y est nommé SHOGEN-SIM-NIVEAU-MODELES-1 (modèle nul homogène, mêmes p et L pour les 11 flux, grille complète, durées d'écart géométriques). Ferme le dernier point de ma question Q-10.

**Diff** (`diff paquet-avant-C.md` contre la forme finale, `diff-C1-C5.txt`, sha256 `d1457f8af869b4cb6b1b5c4f1c754b46e8fa715a861e6a1ee66c69076ab41295`) : deux lignes insérées (15 et 170 de la forme finale), trois lignes modifiées (111, 149, 165) ; aucune autre. Segments changés dans les lignes modifiées : ligne 111, insertion de la phrase de C-2 ; ligne 149, dernière phrase remplacée (C-4) ; ligne 165, nom et source de l'item (C-5).

**Texte de la règle** : §10.2 identique octet pour octet avant et après (sha256 de la section `73e0aca83deb4477643d5c5b56cd41210a21439dce3d73457a4dd4b56e77ba2a` dans les deux formes) ; `regle-paquet.md` inchangé (`843d0833…1e90`) et présent une fois dans le paquet.

**Contrôles rejoués sur la forme finale** :
- `cargo --locked xtask verify` sur l'arbre réel : **`=== VERDICT GLOBAL : VERT ===`**, code 0, 16:47:29-16:48:20 UTC (`verify-C.out`, sha256 `2387b9216530c8ecf8ee71c2b56fe66db5012a20e72be1b9f988cf3b39fe6f5c`). Avant affichage : code de sortie lu, 0 ligne « VIOLATION » ou « non contrôlé », 0 motif de D.2. S-G4 88 sur 88 ; S-G5 89 sur 89, 276 fragments contrôlés (inchangé : aucune citation anglaise ajoutée), 3 284 écartés (+5) ; corpus 128 sur 128 ; S-G1 à S-G3, S-G6 à S-G8, fmt, no_std, clippy : VERT.
- Sonde du bloc (`sonde_bloc.py`) : refus du paquet tel quel ; acceptation avec valeurs de fixture (six clés, trois journaux). Une seule ouverture de bloc (ligne 213).
- Contrôles statiques (`controles.py`) : aucune erreur ; noms des journaux aux seules lignes 216-218 ; motif R-13 du hook : 0.
- Commits et objets cités : 91 jetons de 7 chiffres, tous commits ancêtres de `8b14567` ; 8 jetons de 40 chiffres, tous objets présents (6 blobs, 2 commits).
- Arbre : `git status --short` = `?? docs/adr-0028/PAQUET-PREREG-S2.md` seul ; HEAD `8b14567`.

**Sha256 final du paquet** : `ccbe67501bb2aa92f7d32a4b5541e1ae3bcd73efde56da1ad09f621638551a16` (222 lignes, 60 508 octets).

**Attestation D.3, renouvelée pour cette reprise** : je n'ai vu aucun z, aucun K, aucun P̂_more, aucun φ de campagne, et je n'en ai calculé aucun ; aucune pièce de D.2 ouverte ; aucun journal de campagne ni copie. Lectures en plus dans cette reprise : `JOURNAL.md` l.125 seule (ligne autorisée par l'orchestrateur ; elle porte le compte rendu du cp-1 de l'amendement du 2026-09-30, des chemins de pièces hors dépôt de ce cp-1 et d'un enregistrement de workflow, aucune pièce de D.2, aucune valeur de résultat ni taux de source) ; `docs/adr-0028/G0-lot-SIM-NIVEAU.md` l.239 seule ; `git ls-tree ed479c5` restreint aux deux chemins de C-1 ; `git rev-parse` de ces deux chemins et de `ed479c5^{commit}` ; doc 10 l.555-556 et l.578-581 ; `git cat-file -t` des huit objets de 40 chiffres ; mes propres fichiers de travail. Contrôle FM-1.1 : dans cette reprise, mes entrées d'outils portent de nouveau la liste de motifs de `controles.py` (cherchés dans mon paquet) et une expression `grep -c` de motifs de D.2 sur ma sortie `verify-C.out`, lue en compte avant affichage (0) ; usages de contrôle, sans ouverture de pièce (admis par l'orchestrateur, réponse à Q-12).

**Questions closes par l'adjudication** : Q-1 (C-4), Q-2, Q-3, Q-4, Q-5 (C-1), Q-6 (C-2), Q-7, Q-8, Q-9, Q-10 (C-5 pour le nom ; le reste en actes de l'orchestrateur), Q-11, Q-12. Aucune question neuve.

## 11. Corrections C-6 et C-7 (cp-1 complet du validateur frais, puis constat de l'orchestrateur ; liste fermée)

Reprise du 2026-10-02, de 17:06 à 17:14 UTC (`date -u` lu à 17:06:51, 17:08:04, 17:08:53, 17:09:05, 17:10:56, 17:12:07, 17:12:18, 17:13:12, 17:13:38). Mêmes règles : aucune pièce de D.2 ouverte, aucune opération git en écriture, §10.2 inchangé à l'octet.

**Paquet de départ contrôlé** : commité à `8b9536b` ; `git show 8b9536b:docs/adr-0028/PAQUET-PREREG-S2.md` et le fichier de l'arbre ont le même sha256, `ccbe67501bb2aa92f7d32a4b5541e1ae3bcd73efde56da1ad09f621638551a16`. HEAD a avancé pendant la reprise, sans acte de ma part : `b41ae0c` au départ, puis `cb16260` (17:10:58 UTC, versement du rapport du cp-1 du validateur) ; le paquet y est toujours `ccbe6750…1a16`.

**C-6** (§8, puce « Renvoi daté », ligne 88) : texte de l'orchestrateur inséré tel quel, juste avant « Pièces interdites : liste fermée D.2 (l.31-45, points 1 à 11). ». Contrôles avant écriture : annexe B l.51 à `8b14567` lue (`git show 8b14567:…ANNEXE-B-items.md | sed -n '51p'`, nom de pièce de D.2 masqué à l'affichage) : item MONARK-S2-M009A-EXPOSITION-1, propriétaire « orchestrateur MONARK (formé et transmis par Shōgen) », déclencheur « avant scellement » ; « transmis par CB-4 » : contrôlé dans l'ADR l.327 (§8 pt 6 : « transmission à l'orchestrateur MONARK de MONARK-S2-M009A-EXPOSITION-1, de SHOGEN-S2-TUYAU-MONARK-1 et de SHOGEN-VITRINE-MONARK-1 (CB-4) ») ; la mention est donc gardée. Guillemets : « avant scellement » forme une seule paire dans la phrase insérée (pas d'imbrication) ; S-G4 l'accepte (VERT ci-dessous).

**C-7** (§12 pt 16, « Sceau privé », ligne 203) : phrase datée de l'orchestrateur insérée telle quelle. Contrôles avant écriture, en lecture seule, contenu de la clé jamais affiché :
- `git config --get commit.gpgsign` : `true` ; `git config --get gpg.format` : `ssh` ; `user.signingkey` : posée (vérifiée par code de sortie, valeur non affichée) ;
- `git cat-file commit HEAD | grep -c gpgsig` : 1 (à `b41ae0c`) ; même compte à `8b9536b` : 1 ;
- `git branch -vv` : `partie-3-paquet` suit `origin/partie-3-paquet` (`b41ae0c` des deux côtés à 17:08 UTC) ; `main` suit `origin/main` à `afc7756`, qui ne contient pas HEAD (`git merge-base --is-ancestor` : faux) ;
- en plus (REST, champs d'état seuls) : `gh api repos/KraidleAI/shogen/pulls/1` : PR n° 1 ouverte, non fusionnée, `passation-cloud-2026-10-02` → `main` ;
- non mesurables par moi, repris comme déclarations de l'orchestrateur : la clé est celle de la session et non celle de l'investisseur ; aucun bundle hors ligne n'est fait en session cloud.
Toutes les sorties attendues par l'orchestrateur sont celles mesurées. Placement (cas fermé par le rédacteur, FM-2.4) : la phrase est insérée après la fin de la phrase qui porte l'ancre (« … et par le bundle hors ligne ; un tiers ne peut pas vérifier que le sceau précède le rendu ; la limite est alors écrite ici et au rapport. ») et avant « Avec l'ancre, … », pour ne changer aucune ponctuation du texte existant ; autre forme possible : couper la phrase juste après « hors ligne ».

**Diff contre `8b9536b` (et contre HEAD `cb16260`)** : `diff-C6-C7.txt`, sha256 `05574153316c4a1a628d976d885db58ecc1801c003af05a4cd6661bef8345850` ; `git diff --stat` : 1 fichier, 2 insertions, 2 suppressions (deux lignes modifiées, 88 et 203, par insertion de texte seulement). Le script de reconstruction exige que la forme finale soit exactement celle de `8b9536b` plus ces deux insertions (assertion tenue).

**Texte de la règle** : §10.2 identique octet pour octet à `8b9536b` et à HEAD (sha256 de la section `73e0aca83deb4477643d5c5b56cd41210a21439dce3d73457a4dd4b56e77ba2a`).

**Contrôles rejoués**
- `cargo --locked xtask verify`, arbre réel, 17:09:05-17:09:58 UTC (HEAD `b41ae0c`) : **ROUGE**, code 1 (`verify-C6-C7.out`, `effa6376…b967`). Lus avant tout affichage : 1 ligne de violation, 0 motif de D.2. Seuls le nom de la gate et le chemin ont été extraits, sans l'extrait de ligne : S-G5, `docs/adr-0028/CP1-PAQUET-2026-10-02.md:15`, fichier alors **non suivi**, déposé par un autre acteur (ni mon paquet, ni une pièce de D.2) ; son contenu n'a pas été affiché. Dans la même fenêtre, `.gitattributes` était modifié dans l'arbre par un autre acteur (4 lignes ajoutées, vues par `git diff --stat` seul) ; je n'y ai pas touché.
- Bac à sable de contrôle (`bac-C7/`) : `git archive HEAD` (`b41ae0c`) avec exclusion à la source des pièces de D.2 du dépôt et des `*.jsonl` (`tar -t` compté : 0 de ces noms), plus mon paquet corrigé (`cmp` identique) et les 128 artefacts de `biblio/` ; `target/debug/xtask gates` : **`=== VERDICT GLOBAL : VERT ===`**, code 0 (`gates-bac-C7.out`, `4b7c106c…14a5`) ; S-G4 87 sur 87, S-G5 88 sur 88, 276 fragments contrôlés, corpus 128 sur 128.
- `cargo --locked xtask verify`, arbre réel, 17:12:18-17:13:12 UTC (HEAD `cb16260`, où le fichier du cp-1 est désormais commité) : **`=== VERDICT GLOBAL : VERT ===`**, code 0 (`verify-C6-C7-bis.out`, sha256 `c42dda9bbb6e2daf69a8c102b15653451c40d37d801a0b0440949ab78401b13f`) ; lus avant affichage : 0 ligne de violation, 0 motif de D.2 ; S-G4 90 sur 90 (88 de `docs/` + 2), S-G5 91 sur 91, 281 fragments contrôlés, 3 485 écartés, corpus 128 sur 128 ; S-G1 à S-G3, S-G6 à S-G8, fmt, no_std, clippy : VERT.
- Sonde du bloc : refus tel quel, acceptation avec valeurs de fixture ; une seule ouverture (ligne 213). Contrôles statiques : aucune erreur ; noms de journaux aux seules lignes 216-218 ; motif R-13 : 0. Objets cités : 91 jetons de 7 chiffres, tous ancêtres de `8b14567` ; 8 jetons de 40 chiffres, tous présents (6 blobs, 2 commits).

**sha256 final du paquet** : `1295e907bf781c5bec98423b37e6fc3feab1a9e28bac438402747497ce3fd9e4` (222 lignes, 61 440 octets ; arbre : ` M docs/adr-0028/PAQUET-PREREG-S2.md`, seul changement).

**Attestation D.3, renouvelée pour cette reprise** : je n'ai vu aucun z, aucun K, aucun P̂_more, aucun φ de campagne, et je n'en ai calculé aucun ; aucune pièce de D.2 ouverte ; aucun journal de campagne ni copie ; le contenu du fichier du cp-1 n'a pas été affiché. Lectures en plus : annexe B l.51 à `8b14567` ; ADR l.327 (recherche de « CB-4 » dans l'ADR et l'annexe E ; numéros de ligne seuls dans l'annexe B) ; noms des fichiers changés entre `8b14567` et HEAD (`git diff --name-status`) ; configuration git de signature (deux valeurs, présence de la clé) ; compte `gpgsig` de deux commits ; `git branch -vv` (noms de branches et sujets de leurs têtes) ; état de la PR n° 1 (champs d'état seuls) ; sujets des quatre derniers commits ; listage compté de l'archive de HEAD. Contrôle FM-1.1 : mes entrées d'outils de cette reprise portent des motifs de D.2 dans les exclusions à la source de `git archive`, dans le compte `tar -t | grep -c`, dans deux `grep -c` sur mes sorties de `verify`, et dans `controles.py` ; usages d'exclusion et de contrôle, sans ouverture de pièce.

**Question** : aucune.
