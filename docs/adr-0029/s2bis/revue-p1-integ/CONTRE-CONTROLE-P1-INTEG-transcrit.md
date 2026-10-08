# Contre-contrôle bref des corrections de la G2 d'intégration de P1 (CB-19a à CB-19h, commis en CB-20a à CB-20h ; transcrit)

> Transcription par l'orchestrateur le 2026-10-05, vers 22:20 UTC, du rapport rendu par message par le réviseur (agent a6a81475c74aac459) ; contrôle FM-1.1 : fragments_l51_l14 = 0. Texte du réviseur ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

Gate 0 : **claude-opus-5-5**.

# Contre-contrôle bref des corrections C-1 à C-5 (diffs CB-19a à CB-19h, à commettre en CB-20a à CB-20h) : **CONFORME**

**Liste fermée : vide.** Les huit diffs tiennent les corrections de ma relecture et je n'ai trouvé aucun défaut. Il reste les limites déjà déclarées par le worker (ses items 1 à 5), que vous formez au versement.

**Base.**
- Contrôle de 22:08:44 à 22:19:18 UTC (`date -u`). Tête vérifiée : 47b2177, statut vide au début comme à la fin, aucune écriture git.
- Les 8 diffs d'origine sont conformes à leur `SHA256SUMS`.
- Le recalage `rebase-t5` est conforme à son `SHA256SUMS` (`2d2c7852…`, 21 entrées OK). Ses diffs CB-19 ne diffèrent des originaux que par les lignes `index` (empreintes abrégées ou complètes) : le contenu est identique ligne à ligne.
- Les huit diffs s'appliquent en série par `git apply` sur une extraction neuve de 47b2177, faite avec les exclusions.

## 1. C-1 (DNS)

- **Comportement**, client réel en réseau isolé (`preuves/c1-taille.txt`) :
  - une réponse de 512 octets est retenue (`reponse`) ;
  - une réponse de 513 octets donne `forme` ;
  - un datagramme non apparié de 600 octets est ignoré, puis la vraie réponse est retenue.
- **Borne du schéma** : 7 témoins et 7 noms sont admis ; 8 sont refusés en `CONFIG/borne` (`preuves/c1-borne-7.txt`).
- **Recompte indépendant** (`recompte_sante.py`, construit d'après le §13.6, sans rien importer du collecteur) :

| grandeur | valeur recomptée |
|---|---|
| `reponses` d'une sonde (14 SOA) | 259 239 octets |
| borne du FORMAT, 1 + 495 × (18 × 1 024 + 85) / 36 | 254 609,75 octets |
| plus grande `sante`, 7 témoins et 7 noms | **3 823 224 octets**, marge de 371 080 sous LIMITE |
| plus grande `sante`, 8 témoins et 8 noms | 4 343 471 octets, au-delà de LIMITE |

- **Lemme des 2 × 512 caractères**, vérifié par raisonnement. Chaque segment commence avant le précédent. Il ne peut pas couvrir les octets de pointeur du segment précédent, car ils ne sont pas ASCII et `_nom` décode en ASCII. Seul le dernier segment, qui finit sur un octet 0, peut donc empiéter, et seulement sur l'avant-dernier.
- **Citations** : RFC 1035 l.529 et l.1756-1758, mot pour mot.

## 2. C-2 (durabilité)

- **Banc** : mon banc à coupures (`edca2fa8…`, inchangé), rejoué sur l'état final, graines 0 à 299 (`preuves/banc-coupure1-final.txt`) :
  - **0 rupture, 0 somme fausse, 0 écart** entre l'écrivain et la sonde ;
  - 1 438 redémarrages et 533 queues déclarées, soit les chiffres du worker ;
  - avant les corrections : 128 ruptures et 131 sommes fausses.
- **Code** : les synchronisations passent par le `fsync` injectable. L'ordre est conforme au §6.4 : fsync du dossier après la première ligne, et pour le fichier de sommes, après sa ligne et son propre fsync.
- **Limites du §4** : elles sont honnêtes. Le texte dit que le banc ne prouve ni la durabilité des entrées de dossier, ni un `fsync` qui rendrait sans écrire, ni une perte sous la taille synchronisée.
- **Journal neuf avant son premier marqueur** : il peut encore devenir illisible (§7.6). Au banc, 22 graines sur 300 sont dans ce cas ; c'est l'item 3 du worker.

## 3. C-3 (interfaces)

Mutants classés par la ligne du job (`--plancher 203`), borne de 300 s (`preuves/mutants-cc.txt`). Le témoin est vivant, et il n'y a aucun FATAL.
- **Tués : MI-09, MI-10** (réécrit sur le nouveau code, même mutation), **MI-12, MI-13, MI-14**.
- **Tués aussi, trois sondes neuves :**
  - ordre adresse/phases inversé ;
  - borne de 512 octets retirée ;
  - fsync des fichiers dont dépend la reprise retiré.
- **Ordre** : dans `http.py`, l'adresse est désormais posée avant `phases["dns"]`.

## 4. C-4 et C-5

- **FORMAT** : §4, §6.4, §9.1, §10.1, §11.4, §11.5, §11.6, §12 et §13.6, relus contre le code. Ils sont exacts.
- **Runner** (`preuves/c5-runner.txt`) :
  - avec un vérificateur qui fait `sys.exit(0)` à son chargement, il sort en **3** ;
  - il passe de 85 à 87 cas ;
  - tous les noms de cas existants sont gardés à l'identique, R-01 et R-02 s'y ajoutent ;
  - aucun cas existant n'est retiré ni affaibli : le diff ne retire que la fin de la docstring et la ligne `except`.
- **Enregistreur** (`preuves/c5-enregistreur.txt`) : il refuse `--plancher 0` sous 3.11 comme sous 3.12. Le leurre L2 (vérificateur complaisant dans le commit) le trompe encore, comme prévu : c'est l'item de ma relecture.

## 5. Forme

- **Octets 92** : aucun ajouté.
- **R-13** : 0 marqueur sur les 798 lignes ajoutées ; contrôle positif : 1.
- **120 caractères** : aucune ligne de code au-delà, sur 34 fichiers. Les seules lignes au-delà sont 5 lignes ajoutées dans des tableaux Markdown : 4 dans METRIQUES, 1 dans le tableau du §10.1 du FORMAT. C'est la convention déjà en place : la base en compte 46 dans ces deux fichiers.
- **xtask** sur la copie finale, lignes de verdict seules (`preuves/xtask-verdicts.txt`) :
  - S-G1 à S-G8 VERT ;
  - S-G9 ROUGE, seule violation `docs/17-modele-de-menace.md:70`, déjà connue ;
  - fmt, no_std et clippy VERT.

## À noter, sans effet sur le verdict

Un `os._exit(0)` au chargement fait encore sortir le runner en 0 (mesuré). C'est l'item 1 du worker, à former.

## Écarts

xtask a tourné sans isolement réseau, sous `nice`. Sa sortie complète est supprimée ; seules les lignes de verdict sont gardées.

## Journal G1

**[lu]**
- le rapport transcrit (`f00357d9…`) ;
- les 8 diffs ;
- le code et les tests modifiés, relus par différence ;
- le FORMAT ajouté, sections listées en §4 ci-dessus ;
- RFC 1035 l.529 et l.1756-1758.

**[2nd]** Aucun chiffre repris sans recompte.

**PID** : campagne de mutants 2068.

## Fichiers

Dossier : `<scratchpad>/s2bis/p1-integ/cc/`
- `NOTES.md`
- `SHA256SUMS-cc` (12 entrées OK, `8fdb0ac4…`)
- `preuves/`
- `recompte_sante.py`, `mutants_cc.py`, `leurres_enregistreur_cc.py`

Les copies et la cible cargo sont supprimées.
