# Rapport du worker, lot SIM-BIS tranche 1 (SB-0, SB-1, SB-2, SB-5) — transcription par l'orchestrateur

Rapport rendu par message (le harnais interdit les fichiers de rapport). Worker `claude-opus-5-5`, effort max, 2026-10-04 23:06:07 à
2026-10-05 00:08:07 UTC. Brief `…/sim1/BRIEF-SIM-T1.md` (sha256 `7c894f96…edfd`). Base vérifiée : `6535821`.

## Livraison
9 diffs en série dans `…/sim1/diffs/` (SHA256SUMS du dossier, 81 lignes, sha256 `a5d4908b…5704`) : SB-0a (175 lignes de code), SB-0b (157),
SB-0c (90 ; job `sim-bis-unittest` plancher 13, cas K-03 du runner), SB-1a (102 ; 17), SB-1b (180 ; 24), SB-2a (200 ; 28), SB-2b (54 ; 30),
SB-5a (161 ; 35), SB-5b (86 ; 37). Total 1 205 lignes de code (≈ 690 au G0, ×1,75). Code dans `scripts/sim-bis/` (`commun.py`, `aleas.py`,
`calibration.py`, `calendrier.py`, `parametres.json`, README, 37 tests). Hors de `scripts/sim-bis/` : `gates.yml` (job neuf), runner
(K-03). Vérificateur inchangé.

## Exigences couvertes (selon le worker)
E-S-01 (frontière d'imports par `ast`), E-S-02 (double épingle, refus `.jsonl`, garde de la variable de campagne par mapping fictif),
E-S-03 (schéma fermé, sources par section, aucun flottant), E-S-05 (étiquette), E-S-06 (écriture partielle, octet 92), E-S-43 partie
JSON et tirages exacts (`seuil` par quotient entier puis `math.nextafter` ; tables géométriques de 4 096 rangs, garde de 128 bits, refus
`ALEAS/seuil-ambigu`), E-S-48 partie écriture (exclusif, fsync, lien dur), E-S-41, E-S-42 (flux SHA-256 → `random.Random`, méthode
`random` liée seule), E-S-37 (EP en `Fraction`, quotients refaits sous le contexte de r1), E-S-14, E-S-23, E-S-25, E-S-28 partie runs
(calendrier, T_début, compression ; test croisé avec `window.py` de `f35a70c` chargé par chemin après contrôle d'empreinte).

## Preuves
Rouge avant / vert après pour chaque diff (SB-0c : rouge par runner et sondes) ; vert sous Python 3.10 à 3.13 avec `-W error` ;
PYTHONHASHSEED 0, 1, 4242. Mutants : 137, tous tués par leur test nommé (deux survivants de premier passage, tests renforcés).
Gates sur la série : S2 405 OK ; s2bis 49 ; sim-bis 37 ; runner 33 ; hooks 54 ; model-pinning 95 ; secrets 147 cas et `--tree` OK ;
R-13 0 ; xtask S-G1 à S-G8 vertes, S-G9 rouge connu sur copie.

## Écarts
E-1 tailles (×1,75 ; ×1,62 hors CI) ; E-2 base avancée (JOURNAL seul) ; E-3 tests écrits après le code, rouge montré par mutant ou sonde ;
E-4 survivants de premier passage ; E-5 S-G9 sur copie ; E-6 PyYAML de l'hôte en lecture seule pour la syntaxe de `gates.yml` ; E-7 choix
de conception : (a) `seuil` par `math.nextafter`, tables et garde dans `parametres.json` ; (b) une section de paramètres par sous-lot ;
(c) en-têtes d'EP constants dans `calibration.py` ; (d) test croisé par chargement de `window.py` sous empreinte ; (e) lundi de
référence 2026-12-07 indicatif ; (f) aucune garde réseau dans les tests (le G0 ne l'exige pas ; modules réseau interdits au moteur par
`ast`) ; (g) lien dur sans écrasement, pas de fsync du dossier ; (h) `Refus` dérive d'`Exception`, codes « DOMAINE/motif » ; E-8 rapport
par message ; E-9 barres obliques inverses dans des commandes, octets écrits contrôlés (0 dans le lot) ; E-10 date du commentaire du job.

## Items proposés
I-1 EP ne permet pas de reconstruire la loi des épisodes complets (censure massive en stress) : loi « tous épisodes » avec limite, ou
PLAN-S2BIS-2 ; I-2 `ecrire` sur `os.link` (refus non nommé sans lien dur ; dossier non fsyncé) ; I-3 le contrôle libm ne voit ni `**` ni
`pow` ; I-4 coût d'une table géométrique ≈ 70 ms (cache) ; I-5 le test croisé dépend de l'égalité de `window.py` avec `f35a70c` ; I-6
estimation ×1,75.

## Questions du worker
Q-1 sous-découpe en 9 diffs ; Q-2 I-1 (loi tous épisodes ou PLAN-S2BIS-2) ; Q-3 p = cellules/n_s exact en `Fraction` ; Q-4 indice de
réplication 0 ou 1, noms de composants pré-déclarés ; Q-5 `math.nextafter` admis au sens d'E-S-43 ; Q-6 garde réseau dans les tests ;
Q-7 lundi de référence, table de 4 096 rangs et garde de 128 bits scellés tels quels à E0 ; Q-8 numérotation SB-0 à SB-14 (proposition)
ou SB-1 à SB-15 (G0 et JOURNAL).

## Estimation
Reste ≈ 3 000 à 3 300 lignes en 17 à 19 diffs (≈ 3 700 avec corrections) ; lot ≈ 4 200 à 4 900 lignes ; mur de la tranche ≈ 1 h.
