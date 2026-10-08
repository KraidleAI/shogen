# Contre-contrôle bref de la réserve R-1 (OUT-1a, OUT-1b ; transcrit)

> Transcription par l'orchestrateur le 2026-10-06 02:17:49 UTC du rapport rendu par message par le réviseur (agent a6a81475c74aac459) ; contrôle FM-1.1 : fragments_l51_l14 = 0. Texte du réviseur ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

Gate 0 : claude-opus-5-5

# Contre-contrôle bref de la réserve R-1 (OUT-1a, OUT-1b)

**Verdict : CONFORME. La liste fermée est vide.**

Les quatre premiers points de l'adjudication s'appuient sur mes propres mesures. Le point 2 s'appuie en plus sur la limite que le worker a déclarée.

**Cadre de la mesure**
- Base : la tête 11b9d43. Le dépôt n'a pas bougé : statut vide, aucune écriture git.
- Les sha256 des pièces sont conformes : OUT-1a 6c5c43c4, OUT-1b b9235596, SHA256SUMS f17ae9c0.
- J'ai appliqué les deux diffs à une copie faite par `git archive`, avec les exclusions habituelles.
- Tout a tourné sous `isole.sh`, avec `PYTHONDEVMODE=1` et `PYTHONWARNINGS=error`.
- Date de travail : 2026-10-06, de 02:01 à 02:17 UTC (`date -u`).

## 1. Leurre L2 et sorties du vérificateur : tenu
- **Enregistreur :** L2 est refusé sous 3.11 et sous 3.12. Le refus est nommé : « vérificateur du commit … autre que celui de l'outil … refus ». L0, L0b, L1 et L3 ne changent pas.
- **Runner :**
  - `os._exit(0)` au chargement donne la sortie 3 (« vérificateur illisible »).
  - `sys.exit(0)` pendant un cas donne la sortie 1 (« réponse absente »).
  - `os._exit(0)` pendant un cas donne aussi la sortie 1.
  - Le témoin avec le vrai vérificateur passe : 97 ok.

## 2. Leurres neufs contre le protocole : tenu
| Leurre | Sortie | Lecture |
|---|---|---|
| D4 : « pret » forgé au chargement | 1 | refusé |
| D5 : réponse forgée sur le canal pendant un appel | 1 | refusé |
| D6b : écriture sur le stdout d'origine pendant un appel | 1 | refusé |
| D6a : `print()` pendant un appel | 0 | sans effet : le texte va sur stderr, comme prévu |
| D7 : rejeu d'un transcript complet | 0 | **non refusé** |

Pour D7, j'ai d'abord capturé le canal du vrai vérificateur, soit 175 lignes. Un module sans aucun code de vérification les rejoue au chargement. Le runner rend alors « 97 ok, 0 échec » et sort en 0.

Cette limite est bien déclarée par le worker. Son rapport (`RAPPORT-R1-transcrit.md`, l.131-133) la pose en item à former, au niveau [inféré] : « un vérificateur qui reconnaît les entrées des cas peut rendre les valeurs attendues … la lecture du diff du vérificateur reste nécessaire ». D7 entre dans cette classe et la mesure.

## 3. Cas : tenu
- Les 87 noms de la base sont gardés à l'identique. Dix cas s'ajoutent (B-01 à B-04, R-03 à R-08), ce qui donne 97.
- R-01 et R-02 sont gardés et sortent toujours en 3.
- Seuls trois blocs sont retirés : l'ancien bloc d'import, l'ancien bloc R-01/R-02 (qui est déplacé) et `sys.exit(1 if KO else 0)`. Ce dernier est remplacé par `bilan`, qui est plus strict.

## 4. Matrice : tenue
| Python | Runner | s2bis | S2 |
|---|---|---|---|
| 3.12 | 97 ok | Ran = 255, conforme | Ran = 407, conforme |
| 3.10 | 97 ok | Ran = 255, conforme | rouge : 77 FAIL + 3 ERROR |

Pour 3.10, j'ai aussi lancé S2 sur la base 11b9d43 seule : Ran 406, avec le même rouge de 77 + 3. Les 80 noms rouges sont identiques entre la base et la copie finale (sha256 6de48d41 pour les deux listes). Le test ajouté passe sous 3.10. Il ne reste donc que le rouge connu.

## 5. Forme : tenue
- OUT-1a ajoute 151 lignes, sans aucun octet 92.
- OUT-1b ajoute 76 lignes, avec 2 octets 92 : les deux échappements du motif de test `r"^refus \(vérificateur\) : "`. Je les ai comptés sur les octets : ils sont justes.
- Aucune ligne ne dépasse 120 caractères.
- R-13 : aucun marqueur ; le contrôle positif répond bien.

## Observations hors liste, pour la formation des items au versement
- **O-1 (D7) :** l'item du worker sur les limites passe de [inféré] à [mesuré]. Sa formulation est à resserrer :
  - le runner ne juge que les réponses lues sur le canal ;
  - il n'a pas besoin de lire les requêtes : les réponses peuvent être écrites avant elles ;
  - un vérificateur qui reconnaît `--serveur` peut répondre juste au runner et mentir à l'étape du job.
  - La garantie réelle est donc : sortie 0 seulement si les CAS cas ont été joués et jugés sur le canal. Ce n'est pas : « les réponses viennent du code relu ».
  - Je suggère une phrase dans la docstring du runner. Une parade reste possible : refuser une réponse disponible avant l'envoi de sa requête, ou faire renvoyer un nonce. Elle ramènerait seulement D7 dans la classe « lit les entrées ».
- **O-2 (enregistreur) :** l'ancre de confiance est l'arbre de l'outil (`VERIF`), un choix que le worker motive en Q-3. La règle d'usage reste à écrire :
  - la comparaison ne vaut que si l'outil tourne depuis un arbre dont le vérificateur a été relu ;
  - lancée depuis l'arbre relu lui-même, elle est triviale.
- Je n'ai pas mesuré l'item proposé par le worker, le `unittest.py` qui masque le module standard.

## Écarts
- **E-1 :** ma note de travail disait d'abord « limite non déclarée ». Je l'avais écrite avant de lire `RAPPORT-R1-transcrit.md` (sha256 65b7366b). Elle est corrigée dans NOTES.md.
- **E-2 :** mon premier essai de D7 est invalide et je ne le compte pas. Sa capture de 350 lignes s'était mêlée au serveur de la copie R-08, et il sortait en 1. Je l'ai refait en ne capturant que le premier serveur (fichier ouvert en `O_EXCL`).
- **E-3 :** le contrôle de sécurité a refusé une commande `setsid nohup bash -c …`, qui ne visait aucune suppression. Je l'ai refaite par le fichier de script `matrice.sh`, sans contourner le contrôle.
- Je n'ai pas lancé xtask, qui n'est pas dans le point 5.

## Journal G1, bref
- **Lu [lu] :** BRIEF-R1.md, OUT-1a.diff, OUT-1b.diff, `RAPPORT-R1-transcrit.md` (l.24-32 et l.120-145), la docstring du runner final et les lignes modifiées d'`oracle_record`.
- **PID :**
  - `matrice.sh` : 22663 ;
  - `base310.sh` : 28100 (de 02:13:15 à 02:14:05) ;
  - le run D7 : 22469.
  - Tous sont terminés.
- **Interdits respectés :** aucun `*.jsonl` réel ni aucune pièce de D.2 ouverts. `SHOGEN_S2_CAMPAGNE_CONTROL` n'a jamais été posée : les scripts la retirent par `unset`. Seuls des journaux synthétiques ont été écrits, par les suites elles-mêmes, dans le TMPDIR de la copie, qui est supprimé.

## Fichiers
Tout est dans `<scratchpad>/s2bis/outillage/cc/` :
- **Notes et sommes :** `NOTES.md` et `SHA256SUMS-cc` (sha256 78f671ed, 12 entrées).
- **Preuves (`preuves/`) :**
  - `leurres-enregistreur.txt`
  - `leurres-runner.txt`
  - `leurres-runner-d7.txt`
  - `d7-transcript.txt`
  - `matrice.txt`
  - `s2-310-base-contre-finale.txt`
  - `rouges-3.10.txt`
- **Scripts :** `leurres_runner.py`, `leurres_enregistreur_r1.py`, `matrice.sh` et `base310.sh`.

Les copies lourdes (`copie`, `base`, `tmp`, `bin`) sont supprimées.
