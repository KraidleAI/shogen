# Rapport du worker — SB-14G et SB-14H (transcrit)

> Transcription par l'orchestrateur le 2026-10-05 15:37:39 UTC du rapport rendu par message par le worker (agent af8b331845071f4b5) ; contrôle FM-1.1 : fragments_l51_l14 = 0. Texte du worker ci-dessous, sans retouche.

claude-opus-5-5

# Rapport du worker : SB-14G (cellule de C0 renommée) et SB-14H (épingle du G0 après l'ajout daté PLAN-S2BIS-2)

Le job sim-bis passe sur les deux diffs, mais un point bloque le commit de la tranche 4 sur la tête actuelle : depuis le commit CB-18r de P1-C, le gabarit K-03 du runner refuse la ligne `fetch-depth: 0` du job sim-bis (détail au dernier point).

- **Gate 0** : `claude-opus-5-5`, effort max. Horloge (`date -u`, 2026-10-05) : de 14:55:58 à 15:36:38 UTC.
- **Dépôt** : lu par `git --no-optional-locks`, aucune écriture git. Tête `98c8537` à la fin, `status` vide.
- **Base** : la même que pour le rapport précédent (copie de 5f99ab5 avec les 7 exclusions, puis SB-9A à SB-14F).

## Diffs, à appliquer après SB-14F

| diff | contenu | code + / − | plancher | sha256 |
|---|---|---|---|---|
| SB-14G | cellule de C0 renommée `E1-C0-v2` ; Q-T4-8 récrit ; test | +22 / −8 | 171 | a4709990… |
| SB-14H | `rattachement` pointe sur `a216a953…` ; épingle de `test_commun` l.60 ; test d'alarme sur le G0 ; README +6 / −3 | +21 / −9 | 172 | 2ee7845a… |

- Le G0 figé ne fait **pas** partie de SB-14H : c'est vous qui le committez, dans le même commit.
- La série complète (base + 13 diffs) est égale à l'étape finale e14h. La plus longue ligne Python ajoutée fait 120 caractères.

## SB-14G
- **Nom** : `E1-C0-v2`. Il n'a aucun « / » et n'était employé nulle part dans le lot (vérifié par grep, fichier par fichier).
- **Q-T4-8** dans `e1.questions` : « cellules « E1-C0-v2 » pour C0 », plus le motif mot pour mot : « E-4 : valeurs de E1-C0 i = 0..9 possiblement vues en mise au point, 2026-10-05 ». Les citations de l'avis et de la PROPOSITION sont conservées.
- **Test** : `test_cellule_c0_renommee`. Il vérifie que C0 s'appelle `E1-C0-v2`, que plus aucun nom n'est `E1-C0`, et que le nom et le motif sont dans Q-T4-8. J'ai aussi mis à jour `test_parametres_e1`.
  - Rouge avant le code : 2 FAIL, 0 ERROR.
  - Le mutant qui rétablit `E1-C0` (M-14G-01) est tué par les deux tests. M-14G-02 (ancien nom remis dans Q-T4-8) et M-14G-03 (motif retiré) sont tués aussi.
- **Identité** (Python 3.10 à 3.13 × PYTHONHASHSEED 0, 1, 4242, aléatoire) :
  - nouvelle empreinte T4 : `4054de39bb155e719f1bef84809977190eb2f95960b754df7e65b3414642070a`, 16 cas sur 16 ;
  - avec le seul ancien nom `E1-C0` : `ca650d2e…`, 16 sur 16 ;
  - avec les noms d'avant Q-T4-8 : `6998101d…`, 16 sur 16 ;
  - sonde du réviseur `aa35ad01…`, 16 sur 16 ; sondes T2 et T3 inchangées, 8 sur 8 chacune ; mode strict 8 sur 8.
- Rien d'autre n'a changé : les noms des points de la grille étaient déjà neufs depuis Q-T4-8.

## SB-14H
- **G0 figé** : j'ai recalculé son sha256, `a216a953…0e11e`, égal à la valeur donnée. Le fichier fait 92 lignes : le G0 de 5f99ab5 plus l'ajout daté des lignes 35 à 92, que j'ai lu.
- **`rattachement`** : il épingle `a216a953…` et cite l'ajout. La valeur `d9cffc0a…` est citée « avant l'ajout daté PLAN-S2BIS-2 du 2026-10-05 15:05:43 UTC », et `eeaceb6b…` reste citée.
- **Épingle de `test_commun.py`** : mise à jour, toujours à la ligne 60.
- **Texte de provenance** : le README cite l'ajout et précise que `e1.ell_c1` et la règle actuelle de C1 restent en place d'ici le diff d'intégration. Je n'ai touché ni à `e1.ell_c1` ni au calcul de C1.
- **Le fil d'alarme n'existait pas.** Aucun test ne lisait le G0 : `test_provenance_c_5` ne compare que deux chaînes. Avec l'ancien G0, la suite serait donc restée verte. J'ai ajouté `test_g0_mesure` : il mesure le sha256 de `docs/adr-0029/g0-sim/G0-SIM-BIS.md` dans le dépôt et exige que le `rattachement` épingle cette valeur.
- **Résultats du job** (runner, puis la ligne de `gates.yml`, borne de 300 s) :

| arbre | G0 | sortie | détail |
|---|---|---|---|
| copie, avant le changement de `parametres.json` | figé | rouge | 2 FAIL |
| copie complète (base + 13 diffs) | figé | 0 | conforme à 172 |
| copie complète (base + 13 diffs) | ancien | 1 | `test_g0_mesure` FAIL : c'est le fil d'alarme |
| arbre léger e14h | figé / ancien | 0 / 1 | même résultat |

- **Mutants tués** : M-14H-01 (ancienne épingle remise), M-14H-02 (citation retirée), M-14H-03 (G0 modifié d'un seul octet).

## Contrôles sur l'état final e14h
- **Campagne finale**, 54 mutants (les 20 du réviseur, dont R-01 à R-03 transposés, M-VAR-1b, les 24 mutants neufs de SB-14C à F, puis 3 de SB-14G et 3 de SB-14H) : 51 tués, 0 FATAL, témoin 0/0 à 172. Trois survivent, comme prévu et justifiés comme avant : R-16, R-17 et M-VAR-1b. La même campagne sur e14g donne 48 tués sur 51.
- **Identité e14h** : les mêmes empreintes que sur e14g ; SB-14H ne change aucune sortie. Mode strict 8 sur 8 à 172.
- **Portes** (série complète avec le G0 figé) :
  - runner 33 ok ; sim-bis 172 ; s2bis 156 et s2-harness 405 OK (skipped=2), sous `isole.sh` ;
  - hooks 54, model-pinning 95, secrets 147 ; `gate-secrets` OK ; R-13 : 0 ; R-8 : bibliothèque standard seule ;
  - octets 92 : 0 dans le lot, les diffs, les outils et le journal ;
  - `xtask` : mêmes verdicts que la base (S-G9 ROUGE, la mention connue de `docs/17:70`).

## Points à trancher par vous
- **Bloquant pour le commit de la tranche 4 sur la tête actuelle (O-2).**
  - Les 13 diffs s'appliquent sur `492704b` comme sur `98c8537`.
  - Mais le nouveau gabarit de K-03 (CB-18r) refuse la ligne `fetch-depth: 0` que SB-14A met dans le job sim-bis (Q-T4-11) : 76 ok, 1 échec sur `98c8537`.
  - La tête seule passe (72 ok sur `492704b`), et la série sans cette ligne aussi (72 ok).
  - Je n'ai rien modifié dans `enforcement/`, qui est hors de mon lot. Il faut soit admettre (ou exiger) cette ligne dans le gabarit, soit choisir une autre voie.
- **Épingle de l'ADR-0029** : le `rattachement` cite toujours `b908842d…`. Or le point 5 de l'ajout annonce un ajout daté du même jour à l'ADR. Le texte dit désormais « empreinte d'avant l'ajout daté du même jour annoncé au point 5 ». Il faudra la mettre à jour quand l'ADR sera figé ; je n'ai pas ce fichier.
- **Lecture du G0 par les tests** : ils lisent désormais le G0. Toute exécution de la suite hors d'une copie complète du dépôt devra fournir ce fichier. Mes arbres légers le font, avec la variable `G0_SUBSTITUT`.

## Écarts
- **E-8** : l'outil Write a écrit deux barres obliques inverses dans `outils/mutants_14g.py`. Je les ai vues au compte d'octets avant toute exécution et j'ai réécrit le fichier avec `chr(34)` : 0 octet 92.
- **E-9** : séquences d'échappement tapées dans un `tr` pour lire `/proc/1832/environ`, en lecture seule ; rien n'a été écrit.
- **E-10** : quatre heures écrites dans NOTES sans lecture d'horloge, laissées approximatives avec la marque « x ». Une cinquième a été corrigée en 15:18:56.

## Journal G1
- **[lu]** : vos deux messages ; le G0 figé en entier (`a216a953…`), comparé ligne à ligne à celui de 5f99ab5 ; l'empreinte de l'ADR-0029 et celle du G0 à la tête ; les sorties du runner aux têtes successives.
- **PID réels** : 16371 et 1832 (campagnes), 16508 et 5677 (identité), 14103 (portes).
- **Exposition** : aucune pièce de D.2, aucun `*.jsonl`, aucune valeur FIV imprimée.
- Le dossier contient aussi `RAPPORT-CORRECTIONS-SIM-T4-transcrit.md`, que vous y avez déposé. Je ne l'ai ni modifié ni inclus dans les sommes.

## Fichiers
Tout est dans `<scratchpad>/s2bis/sim4/corr/` :
- `diffs/SB-14G.diff` et `diffs/SB-14H.diff` ;
- `etapes/e14g/` et `etapes/e14h/` ;
- dans `journal/` : `job-serie-g0-fige.txt`, `job-serie-g0-ancien.txt`, `mutants-final-14h.txt`, `identite-14h-synthese.txt`, `runner-tete-98c8537-serie.txt`, `portes.txt` ;
- `SHA256SUMS` régénéré : 317 entrées, sha256 `4093f50d71a59beff8e2e9f375e6df5c68e67e8355db49352b0ed055061594bc`, `sha256sum -c` OK.

Les copies lourdes sont supprimées.
