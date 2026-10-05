# Contre-contrôle bref de RB-1h..k et RB-18a..i, et banc de concordance rejoué (transcrit)

> Transcription par l'orchestrateur le 2026-10-05, vers 22:30 UTC, du rapport rendu par message par le réviseur (agent afb8e4911502ce931) ; contrôle FM-1.1 : fragments_l51_l14 = 0. Texte du réviseur ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

**Gate 0** : modèle résolu `claude-opus-5-5` (préfixe conforme), fiche `shogen-worker`, réviseur, effort max. J'ai travaillé de 22:08:58 à 22:23:48 UTC le 2026-10-05, heures lues par `date -u`. Je n'ai fait aucune écriture git dans `/home/user/shogen`.

# Contre-contrôle de RB-1h..k et RB-18a..i, et rejeu du banc (C-13)

## Verdict : NON-CONFORME, une seule correction (NC-1, sur RB-1)

**NC-1 (RB-1, C-15 second point, lettre C-4 ; FORMAT §1.1, §7.1 b, §8.3).**
- **Le défaut.** `lecteur.py` l.107 appelle `json.loads(ligne, …)` sur les octets bruts. Or `json.loads` reconnaît l'UTF-16 et l'UTF-32 à leurs octets NUL de tête, alors que `_trop_profonde` compte les niveaux sur les octets lus comme de l'UTF-8.
  - Dans une ligne en UTF-16-LE, un guillemet échappé décale l'appariement des guillemets : le compte voit 1 niveau.
  - Le décodeur, lui, descend au-delà de sa limite, et RecursionError sort de la lecture sans verdict.
  - L'issue dépend de l'interpréteur : avec K = 2000, la lecture casse sous 3.10 seulement ; avec K = 20000, sous 3.10 et sous 3.12. C'est ce que C-4 interdit (« quel que soit le réglage de l'interpréteur », « ne se fient pas à l'exception »).
  - RB-18 rend une queue dans tous les cas, en décodant en UTF-8 strict avant de compter.
- **Cas minimal.** Un fichier `pool-2026-10-05-0.jsonl` avec :
  - ligne 1 : une `ouverture` intègre ;
  - ligne 2 : `('{"a' + chr(92) + '"":' + '[' * K + chr(0x0A00)).encode('utf-16-le')`. Elle se termine par les octets 00 0A et ne contient qu'un seul 0x0A.
- **Mesuré avec l'outil du banc.** Sous py3.12 : 1 discordance (K = 20000). Sous py3.10 : 2 discordances (K = 2000 et K = 20000). RB-1 rend `EXC/RecursionError`, RB-18 rend une queue (145, 4016) et (145, 40016).
- **Classement.** Le défaut est celui du lecteur RB-1 ; la lettre n'est pas muette. La prémisse de sa Q-1 (« RecursionError ne peut venir que de l'environnement ») est fausse.
- **Correction attendue.**
  - Décoder la ligne en UTF-8 strict avant de compter et de décoder, pour que le compte et le décodeur voient le même texte. Une erreur de décodage rend la ligne non intègre.
  - Ajouter un test qui reprend les deux lignes minimales sous 3.10 et 3.12, avec son rouge montré : on attend une queue à la position 145.
  - Écrire un mutant qui rétablit `json.loads` sur les octets ; il doit être tué.
  - Corriger la Q-1 dans le rapport de RB-1.

## Contrôles

1. **Lettres C-1 à C-5 et corrections C-6 à C-15.** J'ai lu `lecteur.py` et `oracle_indep.py` finaux en entier. Hors NC-1, tout est conforme.
   - **C-1 / C-7** : un entier de plus de 640 chiffres rend la ligne non intègre, chez les deux lecteurs.
   - **C-2 / C-9 / C-14** : types exacts (`type(v)`), `prec` en 64 hexadécimaux, champs propres exigés, `ws` entier pour un type non réservé.
   - **C-3 / C-10 / C-15 (premier point)** : déclaration en forme canonique ; toutes les queues sont rendues avec la rupture ; la déclaration d'une reprise au lien rompu n'est pas lue.
   - **C-6** : une `queue` en objet nu rend la ligne non intègre, comme adjugé.
   - **C-4 / C-11** : N = 64, la racine au niveau 1, pour les lignes en UTF-8.
   - **C-5 / C-8** : sondes faites.
     - `-100` est lu ; `-007` et un chiffre arabe-indien sont refusés (`nom`).
     - Un dossier sans fichier du journal est refusé : `LECTEUR/absent` d'un côté, `ORACLE/vide` de l'autre.
   - **C-12** : les tests G-07, G-08, G-13 et G-14 et le test tracemalloc sont présents.
   - **C-13** : pas de `recalc/__init__.py`, `REGLES` non touché. La ligne s2bis passe avec `--egal` et Ran = 254, sous 3.10 et 3.12. Le runner donne 87 ok.
2. **Banc rejoué** (`banc_concordance.py` de la G2, tel quel ; état final ; graines de `rejouer_banc.sh`) :
   - L'écrivain est celui de l'état final : sha256 `a39ab0dc…`, `journal.py` touché en dernier par CB-19d.
   - La famille a est faite des 24 fixtures de RB-18 régénérées sur l'état final, identiques sous 3.10 à 3.13.
   - **Résultat sous py3.12 comme sous py3.10 : 10 102 journaux, 10 102 concordants, 0 discordant.**

   | famille | journaux | concordants | dont refus des deux lecteurs |
   |---|---|---|---|
   | a (fixtures) | 24 | 24 | 1 |
   | b (banc de RB-1) | 7 016 | 7 016 | 0 |
   | c (écrivain réel) | 3 000 | 3 000 | 39 (16 absent/vide, 23 nom/nom) |
   | d (seuil d'imbrication) | 62 | 62 | 0 |

   - Chaque lecteur n'a chargé que son propre module.
   - **Table de correspondance des causes**, univoque et identique sous les deux versions :

   | RB-1 | RB-18 (causes) | occurrences |
   |---|---|---|
   | `lien` | contient `genese` ou `lien` | 177 + 137 + 317 + 2 180 |
   | `declaration` | contient `declaration` (sans `genese` ni `lien`) | 37 + 174 |
   | `queue-non-declaree` | `queue-non-declaree` seule | 43 |
   | refus `absent` | refus `vide` | 17 |
   | refus `nom` | refus `nom` | 23 |

3. **Mutants** (commande du job, borne 300 s, python3.12, réseau isolé ; témoins [0, 0], Ran 254). Les 25 mutants sont tués, chacun avec les sorties [0, 1] ; 0 vivant, 0 FATAL.
   - **RB-1, 10 sur 10.** Tirage à graine 1005 : M-1i-02, 05, 08, 09 ; M-1j-01, 05, 06, 07, 11 ; M-1k-09.
   - **RB-18, 10 sur 10** : Me08, Me14, Mf06, Mf08, Mf09, Mg09, Mh09, Mi04, Mi07, Mi09.
   - **Mes 5 mutants neufs, 5 sur 5** :
     - X1 : échappements non retirés avant le compte des niveaux (RB-18) ;
     - X2 : seule la dernière queue rendue avec la rupture (RB-18) ;
     - X3 : le signe compté dans les 640 chiffres (RB-1) ;
     - X4 : k trié comme du texte (RB-1) ;
     - X5 : déclaration attendue en ordre inverse (RB-1).
4. **Indépendance.** Le test de frontière est vert, aucun import croisé. Les incidents déclarés par les deux workers sont sans portée :
   - RB-1 : `ls` et `ps` n'ont affiché que des noms ; `du` a porté sur sa propre copie.
   - RB-18 : `od` a affiché 80 octets de la docstring générique de `recalc/__init__.py`.
5. **Forme.**
   - Octets 92 : aucun dans RB-18a..i. Côté RB-1, 2 dans `lecteur.py` et 8 dans `test_lecteur.py`, tous des `\n`, conformes aux comptes déclarés (2→2 et 6→8).
   - R-13 : 0 marqueur nu. Lignes `.py` ajoutées : toutes ≤ 120 caractères.
   - `xtask`, réseau isolé : 9 S-G VERT ; fmt, no_std et clippy VERT ; verdict global VERT.

## Observations et items à former (PAROXYSME)

- **O-1 (lettre muette).** Pour un dossier absent, RB-1 lève `FileNotFoundError` (refus non nommé) et RB-18 refuse `ORACLE/lecture`. Le banc les compte concordants, puisque les deux refusent. Le §7.7 ne nomme que le dossier sans fichier du journal.
- **O-2 (banc, N-3).** `banc_lecteur.py` du réviseur de RB-1 (`2e320fd1…`) ne tourne plus tel quel sur l'écrivain final : son cas C5 écrit `10**700`, ce que l'écrivain refuse maintenant (`JOURNAL/entier`).
  - J'ai fait une copie adaptée, `outils/banc_lecteur_adapte.py` (`e09983a4…`) : la borne est levée le temps du seul appel de C5.
  - Sa ligne C5 sort ÉCHEC par construction ; les 2 017 autres sortent ok.
  - Si le banc est versé, l'adaptation ou une ligne forgée doit l'accompagner.
- **O-3 (`xtask`).** Le vert global vient de ma copie, un clone complet : la référence de `docs/17:70` y existe. Le S-G9 rouge connu ne se voit que sur les copies `git archive` faites avec exclusions.
- **O-4 (dépôt).** À 22:23:35 UTC, six fichiers indexés sont apparus dans `/home/user/shogen` : la liste exacte de CB-19a. Ils ne viennent pas de moi : toutes mes écritures git étaient dans ma copie jetable, aujourd'hui supprimée.

## Journal G1

- **Sources [lu].**
  - Le brief, `ADJUDICATION-FORMAT.md` et la G2 de RB-18, §4 et §6.
  - FORMAT final : §1, §2, §6 à §8.
  - `lecteur.py` et `oracle_indep.py` finaux en entier ; `journal.py` l.55-102 et 296-330.
  - Les outils de la G2 et ceux des deux workers que j'ai utilisés.
  - Les deux rapports de correction, et le G1 de RB-18 l.195-230.
- **Rien n'a été ouvert** des chemins interdits, des `*.jsonl` réels ni de la liste D.2.
- **Base.** Ma copie est `47b2177` plus les 21 diffs (SHA256SUMS `2d2c7852…` vérifié). Son arbre `796f1a4a…` est le même que celui de `rebase-t5/w`.
- **PID réels.**
  - Campagnes : 2994 (RB-1), 2993 (RB-18), 2995 (neufs).
  - Banc : `sh` 9355 et génération 9362 ; lecteurs [11373, 12068] sous 3.12 et [12491, 12802] sous 3.10 ; cas F-1 [15535, 15536] et [15540, 15541].
  - `xtask` : 12957.
- **Écarts.**
  - E-1 : je n'ai pas consigné le PID du premier lancement du banc, qui a échoué à la génération sans rien produire.
  - E-2 : ma copie était un clone complet. Les chemins interdits y étaient présents sur disque ; je n'en ai ouvert aucun et la copie est supprimée.
  - E-3 : pour X1 à X5, la colonne « visé » valait `test_` ; les tests réellement en échec sont lus dans le champ des échecs.
- **Nettoyage.** Les copies lourdes sont supprimées (clone, banc de 426 Mo, cible cargo, fixtures, tmp) ; aucun processus ne reste.

## Fichiers

Tout est dans `<scratchpad>/s2bis/rb18/cc/` :
- `SHA256SUMS` : 38 entrées, contrôle OK, sha256 `7635a05b5549360ccc41526f9dda3f1d3bee12eb0a69230a13b42c592f3c58dc`
- `NOTES.md`
- `preuves/sonde-f1.txt`, `preuves/banc-f1.txt`, `preuves/cas-f1/`
- `preuves/banc-bilan.txt`, `preuves/table-causes.txt`, `preuves/banc-py3.12-rapport.json`, `preuves/banc-py3.10-rapport.json`, `preuves/banc-MANIFESTE.json.gz`
- `preuves/mutants-rb1.txt`, `preuves/mutants-rb18.txt`, `preuves/mutants-neufs.txt`
- `preuves/forme.txt`, `preuves/sonde-noms.txt`, `preuves/xtask-final-verdicts.txt`, `preuves/runner-3.12.txt`, `preuves/suite-3.10.txt`, `preuves/suite-3.12.txt`, `preuves/fixtures-export.txt`
- `outils/` : `echantillon.py`, `sonde_f1.py`, `sonde_noms.py`, `rejouer.sh`, `banc_lecteur_adapte.py`, `table_causes.py`, `forme.py`, `xtask.sh`
