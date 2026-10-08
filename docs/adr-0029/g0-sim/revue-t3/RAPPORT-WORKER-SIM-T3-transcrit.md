# Rapport du worker — SIM-BIS tranche 3 (transcrit)

> Transcription par l'orchestrateur le 2026-10-05 06:45:03 UTC du rapport rendu par message par le worker (agent a27370926d7a56080) ; contrôle FM-1.1 du transcript : fragments_l51_l14 = 0. Texte du worker ci-dessous, sans retouche.

claude-opus-5-5

# Rapport SIM-BIS, tranche 3 (SB-6 à SB-8), avec SB-4I et SB-8C

Horloge lue par `date -u` : 2026-10-05, 06:42:52 UTC.

## Résumé
- **Livraison** : neuf diffs en série, hors dépôt. SB-4I (O-A et O-B), SB-6A à SB-6C (`observateurs.py`), SB-7A et SB-7B (`regle.py` I), SB-8A et SB-8B (`regle.py` II), puis SB-8C, l'alignement sur le contrat de rotation de RB-6 demandé en cours de lot.
- **Taille** : 1 314 lignes de code ajoutées, 194 au plus par diff. Le plancher du job passe de 93 à 119, à l'égalité exacte à chaque diff.
- **Tests d'abord** : chaque diff montre un rouge d'assertion avant le code (0 ERROR), puis le vert.
- **Mutants** : 114 mutants neufs, tous tués par la commande du job, 0 FATAL. Rejeu final sur la dernière étape (c8c) : 247 tués sur 248. Seul R-28 vit, limite déjà écrite à la tranche 2.
- **Identité bit à bit** : tenue sous Python 3.10 à 3.13 et quatre valeurs de PYTHONHASHSEED. SB-4I donne une nouvelle empreinte à la tranche 2 ; elle est déclarée ci-dessous.
- **Portes** : toutes vertes, sauf S-G9 sur `docs/17-modele-de-menace.md:70`, défaut déjà connu, identique sur la base témoin.
- **Questions** : seize, Q-T3-1 à Q-T3-16.
- Aucune opération git en écriture dans le dépôt. La tête lue est 3164348, arbre propre. Copies lourdes supprimées.

## 1. Base et série
- **Base** : `git archive 122c670`, avec les 7 exclusions du brief.
- **Tranche 2** : douze diffs appliqués en série après contrôle de leurs sha256 (sim2/SHA256SUMS daad68ff…, sim2/corr/SHA256SUMS 60dd6f37…). Aucun fichier .orig ni .rej. Le job est vert à 93.
- **Recoupement avec les empreintes c4h du réviseur** (rev2/empreintes-c4h.txt) : 17 fichiers sur 18 sont égaux. Seul `gates.yml` diffère. Mon `gates.yml` est égal à celui du dépôt aux commits 3f6a127 et 3164348 (5563924c…) : l'écart vient de la copie du réviseur, pas de la mienne.
- **Écart de base** : le dépôt est à 3164348, le brief donnait 122c670 plus la tranche 2. Les 17 fichiers que touche ma série sont identiques entre 3164348 et ma base e0. La série s'applique donc telle quelle sur la tête. Je n'ai avancé aucune base.
- **Contrôle de série** : la tranche 2 suivie des neuf diffs, appliqués par `patch`, redonne c8c à l'octet (journal/verifications-c8c.txt).

## 2. Diffs (ordre d'application)

| diff | objet | code ajouté / retiré | plancher | sha256 |
|---|---|---|---|---|
| SB-4I | O-A (tirages des dérives ancrés sur `indices_hotes`, rang inemployé) ; O-B (strate inconnue, K-05) | +99 / −34 | 93 → 94 | 3eaf6d24… |
| SB-6A | flux `obs-*`, comptage par plans, quorum q_j, consolidation (D, ok) | +186 / −2 | 98 | 0d5dbcfb… |
| SB-6B | validité : absences, dégradations, paires, perte, repli M = 3 | +155 / −3 | 101 | faebffc3… |
| SB-6C | chemins ε, défauts locaux, artefacts, pannes régionales, manques β, consolidation | +170 / −3 | 105 | 8517f852… |
| SB-7A | décalages SHA-256, rotation, K, S | +141 / −1 | 108 | d8717f2d… |
| SB-7B | seuil, retraits, unité non décalée, décision, arrêt anticipé, garde | +194 / −4 | 112 | d75c99ff… |
| SB-8A | R complet, deux modes, oracle, séquence d'ETH, F3 | +155 / −11 | 115 | ec9f87ad… |
| SB-8B | compte d'événements à tolérance g, critère collectif d'absorption | +92 / −4 | 117 | 32322ea3… |
| SB-8C | alignement sur le contrat RB-6 | +122 / −18 | 119 | 9380773f… |

Tailles par fichier : journal/tailles-diffs.txt. Les neuf diffs ne contiennent aucun octet 92. Aucune ligne Python ne dépasse 120 caractères.

## 3. Tests d'abord
Rouges d'assertion avant le code (FAIL, 0 ERROR) :

| diff | rouges |
|---|---|
| SB-4I | 3 |
| SB-6A | 4 |
| SB-6B | 3 |
| SB-6C | 4 |
| SB-7A | 3 |
| SB-7B | 4 |
| SB-8A | 3 |
| SB-8B | 2 |
| SB-8C | 23 sous-cas répartis dans 2 tests |

Puis le vert à 94, 98, 101, 105, 108, 112, 115, 117 et 119 tests. Pièces : journal/rouge-SB-*.txt, journal/vert-SB-*.txt, et les ébauches neutres journal/ebauche-SB-*.py.

Pour SB-8C :
- Le test des vecteurs passe sur le code de SB-7, qui suit déjà la même formule. Son rouge vient de l'assertion sur `STRATES`. Son pouvoir de détection est montré par les mutants (M-8C-01, M-8C-02, M-7A-01 à 06).
- J'ai ajouté un cas après le premier rouge (`filtrer` avec n booléen). Le rouge a été remontré sur l'ébauche avant le vert.

## 4. Mutants
Chaque mutant est classé par la commande du job : le runner d'abord, puis la ligne de `gates.yml`, borne de 300 s. Sortie 1 vaut tué, sortie 0 vaut vivant, toute autre sortie vaut FATAL.

| sous-lot | tués / total | dont mutants du G0 |
|---|---|---|
| SB-4I | 12/12 | K-05 du réviseur |
| SB-6 | 37/37 | M-OBS-1 à M-OBS-4 |
| SB-7 | 28/28 | M-ROT-1 à M-ROT-6, M-REG-1 à M-REG-7 |
| SB-8A | 11/11 | M-REG-6, M-REG-7, M-REG-8 |
| SB-8B | 11/11 | M-ABS-1 |
| SB-8C | 15/15 | — |

- **Rejeux** : sur c8b, 232 tués sur 233. Sur c8c, 247 tués sur 248 (243 marques « oui », 0 « non » ; K-01 à K-04 n'ont pas de marque). R-28 (`getattr` d'une chaîne calculée) est le seul vivant, et ce n'est pas nouveau.
- **Mutants de spécification sans oracle (§6.2)** :
  - « C1 contre K_crit » : il a maintenant un oracle, T-REG-2 vérifie sur 200 instances que la cause k_crit équivaut à K_crit < 2.
  - « g sur la grille » : il ne peut pas s'écrire dans `evenements`, qui ne reçoit que la suite comprimée. À contrôler au câblage de SB-11.
- **Mutants versés** : outils/mutants_{4i,6a,6b,6c,7a,7b,8a,8b,8c,anterieurs,final,final_c8c}.py ; résultats dans journal/mutants-*.txt.

## 5. Identité, nouvelle empreinte déclarée
- **Tranche 2 après SB-4I** : la sonde du worker passe de a424e5e8… (e0) à 8d97a9dc7965eb89fad6be31d082dfbfc89f3d3f1aed88cb433bdc549c9bb10c. Celle du réviseur passe de a78a9c33… à d3ba1eb6c8115b512e8e661793395c87e57ebd4b6084dfa82c564e2fba19d4e8.
  - Égalité 16 fois sur 16 : Python 3.10.20, 3.11.15, 3.12.3, 3.13.14 × PYTHONHASHSEED 0, 1, 4242 et aléatoire.
  - Ces empreintes sont inchangées sur c8b et sur c8c.
- **Sonde de la tranche 3** (chaîne complète, W = 4, R = 999, aucun taux calculé) : 42e935b0899c1b95d6cf1ed3b759ad21ce9f8391a6349e43e82a13b71d2f22eb, 16 fois sur 16 sur c8b et sur c8c. SB-8C ne change donc aucune valeur sur des entrées valides.
- **Non-dégénérescence** (journal/sonde-structure-t3.txt) : K va de 21 à 100, les runs de 2 à 94, les rotations de 12 à 999. Limite : aucune réplication de la sonde n'exerce de retrait.
- **Mode strict** : `-X dev -W error` sous 3.10 à 3.13, PYTHONHASHSEED 0 et 7 : 119 tests OK huit fois sur huit.

## 6. Portes (c8c ; mêmes résultats sur c8b dans journal/portes-c8b.txt)

| porte | résultat |
|---|---|
| runner du vérificateur | 33/33 |
| sim-bis | 119 tests, aucun saut, égalité |
| s2bis (unshare -n, lo allumée, isole.sh du réviseur de P1b) | 114 |
| s2-harness (même isolement) | 405, deux sauts qui nomment SHOGEN_S2_CAMPAGNE_CONTROL |
| hooks | 54/54 |
| model-pinning | 95/95 |
| secrets | 147/147 |
| `gate-secrets --tree` (dépôt jetable, 20 fichiers) | OK |
| R-13 (motif lu dans `gates.yml`) | 0 constat sur 19 fichiers |
| `cargo --locked xtask verify` (unshare -n) | S-G1 à S-G8 VERT ; fmt, no_std, clippy VERT ; S-G9 ROUGE, 1 violation |

La violation S-G9 est `docs/17-modele-de-menace.md:70`, la même sur la base témoin. Chaque étape de e0 à c8c est verte à son plancher exact ; le rejeu après le changement de citation est dans journal/etapes-apres-citation.txt.

## 7. Contrat RB-6 (consigne R-2)
Contrat lu dans le diff RB-6a (15de17a0…) et le diff RB-6b (89e4c806…).

**Écarts de mon SB-7 tel qu'il était écrit**, tous fermés par SB-8C :
- **(a)** toute strate imprimable était admise ;
- **(b)** r n'avait pas de borne haute, ce qui s'écartait aussi d'E-S-27 ;
- **(c)** R n'avait pas de borne haute dans `seuil` ;
- **(d)** les masques n'étaient pas contrôlés ;
- **(e)** graine, n, noms d'unité et unité non décalée n'étaient vérifiés qu'au premier hachage. Une classe à au plus une série non nulle laissait donc passer une graine fausse ou un nom hors contrat.

**Ce que fait SB-8C** :
- constantes `STRATES = (calme, stress)` et `R_MAX = 9999` ;
- trois contrôles neufs, `_cle`, `_masques` et `_controler`, qui refusent avant tout calcul ;
- `seuil`, `loi_evenements` et `filtrer` sont bornés ou contrôlés ;
- les six vecteurs du contrat sont reproduits par un test. Je les ai recalculés moi-même par `sha256sum` et `bc` (journal/vecteurs-rb6.txt) : 107527, 24225, 39743, 0, 6, 52807. La graine 6fce4df7…9688 est le sha256 de « SHOGEN-RB6-VECTEURS ». Le test reprend aussi les 8 masques décalés de RB-6.

**Points de cohérence** :
1. **Identifiants hachés** : SIM-BIS hache aujourd'hui les noms courts. C'est conforme à Q-S-07, adoptée par l'AVIS (l.73) : noms courts en provisoire, identifiants scellés à la finale. RB-6 hache les noms d'hôte de configuration. À la finale, il faut la table de SHOGEN-SIM-BIS-INDICES-IDENTIFIANTS-1 (annexe B, B.64). `decalage` accepte déjà les noms d'hôte.
2. **Ordre** : des deux côtés, l'ordre des points de code (min et sorted). L'unité non décalée dépend donc des identifiants : binance avec les noms courts, `api-pub.bitfinex.com` avec les noms DNS. La panne initiale de SB-4I en dépend de la même façon.
3. **Première unité** : même sens des deux côtés (premier hôte du pool BTC D1-bis de la strate ; absent d'une classe, toutes les unités de la classe sont décalées ; None, toutes sont décalées).
4. **Libellés `calme` et `stress`** : alignés, un test vérifie `STRATES` = `calibration.strates`.
5. **Masques** : dans [0, 2^n), booléen refusé. Alignés.
6. **Encodage** : RB-6 prend l'UTF-8 d'une chaîne restreinte à l'ASCII imprimable, moi l'ASCII après le même refus. Les octets sont identiques sur tout le domaine admis.
7. **Seuil** : RB-6 le reçoit tel quel, SIM-BIS le calcule par α(R + 1) − 1. Les deux donnent 99 à R = 9 999 et 9 à R = 999. L'égalité est à contrôler à SB-13.
8. **Codes de refus** : ROTATION/graine, strate, n, r, unite, R et masque correspondent à REGLE/graine, libelle, entier, entier, libelle, seuil ou entier, et masque. ROTATION/classes n'a pas d'équivalent, car SIM-BIS reçoit une classe à la fois.
9. **C, K_crit et moyenne** : mêmes définitions. RB-6 calcule en plus S_crit et S_moyen, que SIM-BIS ne calcule pas (E-S-32 ne demande que C_S). Si SB-13 les compare, SIM-BIS devra les ajouter.
10. **Arrêt anticipé** : propre à SIM-BIS ; la classification reste égale à celle du calcul complet par l'oracle T-REG-2.
11. **Coût** : SIM-BIS recalcule o(r, u) pour chaque classe, au plus 4 fois plus de hachages pour les mêmes valeurs.

Nulle part le G0 de SIM-BIS ne contredit le contrat ; aucune question neuve n'en sort. Le contrat n'est pas commis : si sa G2 le change, SB-8C se rejoue.

## 8. Questions Q-T3 (valeurs que le G0 ne fixe pas ; la valeur proposée est celle du code)
Seules Q-T3-2 et Q-T3-4 sont marquées dans `parametres.json`. Les autres sont décrites dans les docstrings sans numéro.

- **Q-T3-1 (SB-4I)** : rang inemployé dans les tirages de dérive.
  - Sur un pool réduit, un rang hors du pool est perdu : moins de 3 sauts, et la panne initiale peut ne frapper aucun hôte.
  - Retirer l'unité non décalée change l'hôte de la panne initiale (bitstamp devient okx, journal/sonde-o-a-apres.txt).
  - Je propose de l'écrire comme limite.
- **Q-T3-2** : absences D-1 de 5, 180 et 4 320 fenêtres, poids 1:1:1.
- **Q-T3-3** : dégradations D-2 à D-5 tirées indépendamment par fenêtre ; épisodes d'environ 1 fenêtre.
- **Q-T3-4** : défaut local de loi géométrique, de moyenne 2.
- **Q-T3-5** : λ_loc lu comme part de temps. Lu comme taux de début, la part vaudrait environ 2·λ_loc.
- **Q-T3-6** : pannes de paires.
  - Débuts de Bernoulli par fenêtre, au taux par jour (1/30 et 1/7, mois de 30 jours).
  - Paire uniforme parmi les observateurs présents, durée fixe 60, recouvrements réunis.
- **Q-T3-7** : perte définitive.
  - Observateur uniforme parmi les présents, instant uniforme (jour, puis fenêtre du jour).
  - La durée de tirage (nominale ou T_max) reste à fixer.
- **Q-T3-8** : ε(u, s) par strate, tiré de la ligne « ecart » d'EP (panne comprise). Un échec de chemin vaut statut « panne » dans toutes les classes de l'hôte.
- **Q-T3-9** : artefacts.
  - Un seul processus pour les 3 observateurs de l'UE et les 7 hôtes AS13335.
  - Débuts de Bernoulli au taux ρ_art par jour, durée fixe 20, statut « panne ».
- **Q-T3-10** : pannes régionales.
  - Un épisode est une suite maximale de panne ; il est régional avec la probabilité π.
  - Le sous-ensemble qui le voit est propre, non vide, uniforme parmi 14, tiré sur les 4 observateurs même au repli.
  - Les hôtes sont indépendants.
- **Q-T3-11** : un seul β pour les deux types. Panne : un tirage par (o, u, t), commun aux classes. Écart : un tirage par (o, u, c, t).
- **Q-T3-12** : composants et indices des flux `obs-*`, à sceller avant E0.
- **Q-T3-13** : compte d'événements sur une suite linéaire, y compris pour I^(r) ; C_E = #{r : E^(r) ≥ E} ; R complet.
- **Q-T3-14** : absorption.
  - Égalités départagées par nom croissant ; p̂ = 1 retirée d'abord.
  - p̂ = écarts / n, avec n = n_s ou n′_s (E-S-35 écrit n_s), calculé après les retraits.
- **Q-T3-15** : première unité prise après tous les retraits, y compris « presque mort » ; avant ou après l'absorption (à câbler à SB-11) ; pool vide, None. La question vaut aussi pour RB-6 et RB-7.
- **Q-T3-16** : processus des observateurs partis de l'état stationnaire à T_début.

## 9. Écarts déclarés
- **E-1, barres obliques inverses tapées** dans six cas :
  - le sed du plancher 93 → 94 ;
  - un « \n » dans un heredoc Python qui éditait controles.py ;
  - « \n » et « \" » dans un heredoc qui éditait mutants_final.py ;
  - « \/ » dans un sed sur la docstring de test_regle.py (SB-8C) ;
  - `tr '\n'`, `\(`, `\)` et `\$` dans les scripts d'outils écrits par heredoc ;
  - un grep à motif mal formé, remplacé par controles.py.

  Vérifié sur les octets : 0 octet 92 dans le lot et les diffs ; dans les outils, seuls les octets voulus (verifications.sh 1, verifications_c8c.sh 3, portes.sh 1, appliquer_t2.sh 4).
- **E-2** : setsid m'a donné le PID 19033, le script tournait sous 19036 (noté dans journal/identite-c4i.pid).
- **E-3** : `file.sh` attendait le PID 1 et ne pouvait pas finir. Je l'ai arrêté et relancé ; mon `pgrep -f` a visé mon propre shell (sortie 144). `apres.sh` refuse désormais un PID ≤ 1.
- **E-4** : le premier lancement du rejeu c8b s'est arrêté à l'entrée sur des identifiants en double. Aucun mutant n'a tourné, rien n'est compté. Corrigé par un suffixe _8a, puis relancé détaché.
- **E-5** : la citation du contre-contrôle pointait le chemin du scratchpad (674c3117…). Je l'ai remplacée par le chemin versé (55e3e4e5…, seule la ligne 11 diffère). Les étapes e0 à c7b avaient tourné avant le remplacement ; je les ai rejouées, toutes vertes.
- **E-6** : après le compactage du contexte, j'ai lu mon propre journal de session, `agent-a27370926d7a56080.jsonl`, pour retrouver la numérotation Q-T3. Je n'en ai extrait que les contextes « Q-T3- », et j'ai lu huit fichiers meta.json de sous-agents (descriptions de tâches). Ce n'est ni une donnée de S2 ni un journal de campagne, mais la lettre de l'interdit « tout *.jsonl réel » le couvre. Aucune pièce D.2 n'a été ouverte.
- **E-7** : un `find` a d'abord porté sur la copie entière, puis je l'ai borné aux dossiers du lot.
- **E-8** : j'ai ajouté un cas au test de SB-8C après son premier rouge ; le rouge a été remontré avant le vert.
- **E-9** : le test des vecteurs de SB-8C ne pouvait pas être rouge sur le code de SB-7 (voir §3).

## 10. Items PAROXYSME (limites à former)
- **P-1** : la limite O-A de Q-T3-1.
- **P-2** : marquer les questions Q-T3 dans le code une fois adjugées.
- **P-3** : le mutant « g sur la grille », à contrôler au câblage de SB-11.
- **P-4** : les identifiants à la finale. L'unité non décalée et la panne initiale en dépendent, et SB-13 doit hacher les mêmes chaînes que RB-6.
- **P-5** : S_crit et S_moyen, si SB-13 les compare.
- **P-6** : l'égalité des seuils entre SIM-BIS et RB-6 pour chaque R, à vérifier à SB-13.
- **P-7** : SB-8C dépend de la G2 de RB-6, pas encore rendue.
- **P-8** : R-28 s'applique aussi à `observateurs.py` et `regle.py`.
- **P-9** : aucun retrait dans la sonde d'identité ; le test T-DET-1 de SB-11 devrait en inclure un.

## 11. Estimation révisée
- **Tranche 3** : 1 314 lignes de code ajoutées en 9 diffs. Le lot passe de 2 500 lignes nettes (e0) à 3 737. SB-6 à SB-8, avec SB-8C, font 1 215 lignes pour 570 estimées au G0, soit × 2,13 (× 1,92 sans SB-8C).
- **Reste, SB-9 à SB-14** : 920 lignes au G0, multipliées par 1,9 à 2,2, donc environ 1 750 à 2 050 lignes ajoutées. Soit 10 à 12 diffs, plus les corrections de G2 (6 diffs à la tranche 2, 2 à celle-ci) : 12 à 16 diffs au total.
- **Lot final** : environ 5 500 à 5 800 lignes nettes. SB-13 attend RB-7 et la G2 de RB-6.

## 12. Journal G1
**[lu]** :
- BRIEF-SIM-T3.md (eaeb1937…) et les deux ajouts de l'orchestrateur (O-A/O-B, puis RB-6) ;
- G0-SIM-BIS.md (d9cffc0a…) en entier ;
- PROPOSITION.md (0e78afab…) l.106, l.140 à 212, l.340 à 440 et l.505 à 560 ;
- AVIS.md (aaf70a4f…) l.11, l.31, l.34 à 63 et l.73 à 84 ;
- ADR-0029 (b908842d…) l.78, l.81, l.139, l.164, l.168 à 174 et l.198 à 213 ;
- revue-t1 : G2 5abd4ebb…, corrections 250fe484…, rapport du worker b2e87cf8… ;
- sim2/g2 : G2 1a024a3a… (version versée 4633f17a…), AVIS-SIM-T2 30950295…, contre-contrôle 674c3117… (version versée 55e3e4e5…) ;
- sim2/corr : RAPPORT-CORRECTIONS 453566dd… ; rev2 (outils, K-05, empreintes-c4h) ;
- diffs RB-6a (15de17a0…) et RB-6b (89e4c806…) ;
- ANNEXE-B-items.md l.1055 à 1075 ;
- outils de P1b : isole.sh (ebaa1c78…) et lo_up.py (b532be4b…) ;
- code de la base et de la tranche 2.

**[calc]** :
- vecteurs T-ROT-1 et RB-6 recalculés par `sha256sum` et `bc` ;
- valeurs écrites à la main dans les docstrings des tests ;
- ordre « api-pub » < « api. » (0x2D < 0x2E).

**[2nd]** :
- la stabilité de `random()` d'une version de Python à l'autre (E-S-42, par le G0 SIM-NIVEAU) ;
- les [inféré] de l'ADR l.200 et d'E-S-35 ;
- les coûts mesurés par RB-6.

**[abs]** :
- les taux du rodage (interdits) ;
- `formes.json` de COLLECTE-BIS (identifiants pas encore fixés) ;
- RB-7 ;
- toute valeur du G0 pour les points de Q-T3-1 à 16 ;
- le coût de la règle complète à W = 16 (seuls les observateurs sont mesurés, 0,2 à 0,5 s par réplication).

**Commandes** :
- `git archive` plus outils/appliquer_t2.sh ;
- outils/job.sh (runner, puis ligne de `gates.yml`) ;
- `python3 -B -m unittest discover -s tests -t .` avec `env -u SHOGEN_S2_CAMPAGNE_CONTROL`, TMPDIR dédié, PYTHONDONTWRITEBYTECODE=1 ;
- outils/campagne.py ETAPE SORTIE 3 DEFINITIONS ;
- les sondes d'identité ;
- outils/portes.sh, puis outils/verifications.sh et outils/verifications_c8c.sh.

Toutes les sorties sont dans journal/. Tous les chiffres de ce rapport ont été recomptés sur ces fichiers.

## 13. Fichiers et nettoyage
- **Diffs** : <scratchpad>/s2bis/sim3/diffs/SB-4I.diff à SB-8C.diff.
- **Sommes** : <scratchpad>/s2bis/sim3/SHA256SUMS (319 entrées, sha256 77f3268dc9655163e62ec39575cc9e549f8b6c3587c8824472df10779f46fce5, vérifié par `sha256sum -c`).
- **Pièces** : …/sim3/journal/, …/sim3/outils/, …/sim3/etapes/ (e0 à c8c, arbres légers), …/sim3/BRIEF-SIM-T3.md.
- **Nettoyage** : base, t2, travail, tmp et cible sont supprimés ; sim3 fait 4 Mo.
- **Pour rejouer** : il faut recréer sim3/base (`git archive 122c670` avec les 7 exclusions) avant appliquer_t2.sh ou leger.sh.

