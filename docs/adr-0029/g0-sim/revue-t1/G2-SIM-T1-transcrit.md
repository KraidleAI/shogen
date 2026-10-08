# Relecture G2 du lot SIM-BIS, tranche 1 (SB-0a à SB-5b) — transcription par l'orchestrateur

Rapport rendu par message (le harnais interdit les fichiers de rapport). Réviseur G2 neuf `claude-opus-5-5`, 2026-10-05 00:12:36 à
00:43:41 UTC ; sorties et outils sous `…/sim1/g2/rev/`.

## Verdict : ACCEPTE-AVEC-CORRECTIONS (C-1 à C-6, liste fermée)
Neuf diffs en série sur `dbbad9e` et `762abbd`, arbre = 14 empreintes, ≤ 200 lignes de code chacun (SB-2a à 200), chaque état vert seul
à plancher exact (4, 10, 13, 17, 24, 28, 30, 35, 37). Tirages exacts : oracle entier indépendant sur 20 090 valeurs difficiles (k/7,
k/p premiers jusqu'à 2^127 − 1, flottants ± 2^-200, milieux exacts, sous-normaux, rationnels aléatoires), 0 écart ; tables (EP l.14,
k/7, lois géométriques) identiques à l'oracle ; garde de 128 bits juste ; `math.nextafter` exact au sens d'E-S-43 (nextUp IEEE 754).
Identité bit à bit : 16 exécutions (Python 3.10 à 3.13 × 4 PYTHONHASHSEED), même sha256 `89505b96…24b15c`. Calibration recalculée par
`bc` (EP l.17, l.49, l.140) ; calendrier vérifié à la main et contre `datetime` et `window.py`. Rouge/vert rejoués sur cinq pas.
Mutants du réviseur (classés par la commande du job, borne 300 s) : 34, 23 tués, 11 vivants dont 2 équivalents (R-10, R-11) ; mutants du
worker rejoués par la commande du job : 137 tués. CI conforme ; R-13 0 ; R-8 ; secrets OK ; xtask S-G1 à S-G8 vertes.

## Corrections
- **C-1 (E-S-02, D.4 a)** : chemin par défaut de la garde non testé (R-28) : cas qui remplace `commun.os.environ` par le mapping fictif
  (`mock.patch.object`), sans putenv ni sous-processus ; `charger_parametres()` et `lire_entree(prm, "episodes")` sans `environ` rendent
  `CAMPAGNE/variable`.
- **C-2 (E-S-03)** : schéma non testé au chargement (R-26) : JSON valide hors schéma (`{"lot": "SIM-BIS"}`) → `PARAMETRES/schema`.
- **C-3 (E-S-01)** : la frontière admet qu'un module du moteur importe un adaptateur d'oracle (R-34) : retirer `oracle_r1` et
  `oracle_recalc` des noms admis pour les modules du moteur ; cas refusé `import oracle_r1`.
- **C-4 (E-S-41)** : (a) refus d'un flux à moitié renseigné non testé (R-03) : `chaine(A, "N1", 0, "sources", None)` et
  `chaine(A, "N1", 0, None, 0)` → `ALEAS/champ` ; (b) composant et indice absents tous deux admis (`graine_flux(A, "N1", 0, None, None)`
  = 64 premiers bits de `graine_regle`) : exiger les deux champs, avec test.
- **C-5** : mutants vivants à tuer par un cas écrit à la main chacun : R-02 (un seul appel de u() par tranche : p = 1/4, rangs 2, borne 2,
  `suite(0.5)` à une valeur → None), R-07 (`.JSONL` majuscules refusé en entrée et en sortie), R-08 (épingle de 65 caractères refusée au
  schéma), R-12 (EP l.13 « n_s = 0 ; cellules = 0 » : 0/0 lève `InvalidOperation` ; attendu `CALIB/coherence`), R-13 (EP l.14 « 1×301 » →
  « 1×300 1×1 » : refus « strictement croissantes »).
- **C-6 (E-10)** : dates de `gates.yml` (en-tête et commentaire du job) portées à la date du commit.

## Observations
O-1 `_episode` : StopIteration non nommée si un quantile dépasse 100 ; O-2 `_sans_flottant` ne voit pas les clés flottantes d'un dict ;
O-3 modules non encore consommés (SB-11) ; O-4 ENREG-ROLE-1 à tenir avant la G2 de la partie S-1 ; O-5 la regex de K-03 n'est pas mutée.

## Avis sur écarts, questions, items
E-1 à E-10 acceptés (E-3 « tests après le code » accepté tel que déclaré ; pour la tranche 2, exiger un rouge d'assertion consigné avant
le code) ; Q-1 à Q-8 : d'accord avec la sous-découpe, `Fraction(cellules, n_s)`, indice à 0 et composants en liste fermée sous schéma
avant E0, `nextafter` admis, pas de garde réseau, scellement tel quel à E0, numérotation SB-0 à SB-14. **Q-2 / I-1** : constat exact
(`episodes.py` l.47-50 compte tous les épisodes, censurés compris ; EP l.13-14 : 332 épisodes dont 51 censurés) ; E-S-10 (« épisodes
complets … histogrammes d'EP ») n'est pas réalisable à la lettre : écart du G0 à porter par écrit ; la loi « tous épisodes » avec limite
écrite est la bonne (écart des moyennes complets / tous : −0,035 à +0,134 fenêtre en calme, −0,023 à +0,015 en stress). Items I-1 à I-6
d'accord (I-3 étendu aux méthodes de `random` autres que `random()` ; I-4 mesuré 33 à 83 ms par table). Limite neuve : sous `unshare -n`,
l'interface `lo` reste éteinte (commande `ip` absente) et la suite s2bis échoue sur `test_boucle_locale_permise` (artefact d'isolement) :
item ou consigne SHOGEN-HARNAIS-UNSHARE-LO-1.
