# Rapport du worker — corrections de RB-18 (C-6 à C-13, recalage RB-18a à RB-18d ; transcrit)

> Transcription par l'orchestrateur le 2026-10-05 17:39:34 UTC du rapport rendu par message par le worker (agent af237d60363a99e96) ; contrôle FM-1.1 : fragments_l51_l14 = 0. Texte du worker ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`). Reçu pendant la pause demandée par l'investisseur : transcrit seulement, adjudication et contre-contrôle à la reprise.

**Gate 0 : `claude-opus-5-5`, effort `max`.**

Corrections livrées en neuf diffs (RB-18a à RB-18i), écrits sur 98c8537. Tous les jobs sont conformes et les 123 mutants sont tués. Le critère de sortie de C-13 (0 discordance au banc avec RB-1 corrigé) reste à jouer par toi : le banc et RB-1 me sont fermés. Rien n'est commité.

**1. Base et recalage (C-13)**
- Je suis parti de la copie `git archive` de 98c8537, avec les exclusions habituelles.
- La tête a avancé pendant la passe, d'abord à `dcc41f5` puis à `47b2177`. Le FORMAT et `s2bis/` n'ont pas changé entre 98c8537 et `47b2177` (`git diff --quiet`).
- Sur une archive de chacune des deux têtes, tous les hunks s'appliquent sauf les ajouts en fin de `METRIQUES-S2BIS.md`, qui se versent après les nouvelles sections. Le job s2bis y est conforme (Ran 224).
- RB-18a à RB-18d sont rejoués sans `recalc/__init__.py` et sans toucher `REGLES`.
- À la tête, l'écrivain refuse un entier de 641 chiffres (`JOURNAL/entier`). Dans le test de RB-18d, cette ligne est donc écrite à la main.
- Plancher mesuré à la base : **184**, et non 188 comme l'annonçait l'extrait.

**2. Diffs**

| diff | objet | code + | METRIQUES + | plancher | mutants |
|---|---|---|---|---|---|
| a à d | recalés | 161 / 199 / 131 / 113 | 21 / 20 / 17 / 17 | 194 / 201 / 211 / 216 | 19, 17, 11, 11 tués |
| e | C-7 et C-11 : entier long, imbrication | 86 | 20 | 216 | 15/15 |
| f | C-9 et C-6 : champs propres, `queue` | 46 | 19 | 218 | 13/13 |
| g | C-8 : noms | 70 | 21 | 219 | 15/15 |
| h | C-10, G-07, G-08 | 67 | 22 | 221 | 11/11 |
| i | G-13, G-14, mémoire | 42 | 19 | 224 | 11/11 |

Comportements selon la lettre :
- **Entier long et imbrication (C-7, C-11)** : un entier de plus de 640 chiffres ou un conteneur au-delà de 64 niveaux (racine au niveau 1) rend la ligne non intègre, jamais un refus. Les niveaux sont comptés sur le texte avant le décodeur, et RecursionError n'est plus attrapée.
- **Champs (C-9, C-6)** : les champs propres du §7.1 d sont exigés et typés, un booléen n'est jamais un entier. Une `queue` qui n'est ni liste ni null rend la `reprise` non intègre.
- **Noms (C-8)** : grammaire `0|[1-9][0-9]*` en chiffres ASCII ; un nom hors grammaire donne le refus `ORACLE/nom`, un dossier sans fichier du journal `ORACLE/vide`.
- **Déclaration (C-10)** : elle doit être exacte (ordre (jour, k), null sans queue). Toute rupture rend toutes les queues en attente, et la déclaration d'une `reprise` au lien rompu n'est pas lue.

**3. Tests de C-12**
- G-07 : `test_reprise_au_lien_faux`.
- G-08 : `test_reprise_declare_deux_queues` (trois démarrages de l'écrivain réel, puis autre ordre, partie, doublon).
- G-13 : `test_sortie_hors_ascii`. G-14 : `test_usage` (0, 1 ou 3 arguments donnent le code 2).
- Mémoire : `Memoire.test_lecture_en_memoire_bornee`, sur des journaux de 1 et 4 Mio. Pics mesurés de 35 360 à 47 762 octets ; le test exige moins de 256 Kio et un pic qui ne croît pas avec le journal.
- G1 corrigé : le fichier de tests comptait **392** lignes à la fin de RB-18d (96 + 117 + 109 + 70), pas 385 ; 394 après recalage.

**4. Preuves**
- **Rouges** :
  - avant le code, pour e à h, sur le code de l'étape précédente (échecs d'assertion) ;
  - pour i, par mutants : ceux de G-13 et G-14 survivaient aux tests de h ;
  - pour a à d, rejoués sur 98c8537.
- **Verts** : sous 3.10 à 3.13 en `-X dev -W error`, la suite s2bis entière passe (224 tests). Les 24 fixtures du banc donnent les mêmes octets sur les quatre versions.
- **Mutants** : 123 sur 123 tués, tous avec les sorties [0, 1] et le test visé en échec ; aucun vivant ni FATAL.
- **Arbre final** (série appliquée par `patch -F0`) : job s2bis conforme (224), job S2 conforme (406), verdicts xtask identiques à la base (seul S-G9, `docs/17:70`, connu, est rouge), hook et secrets verts.
- 0 octet 92 dans le code et les diffs ; pas de TODO/FIXME nu ; bibliothèque standard seule ; lignes de code ≤ 120 caractères.

**5. Questions à adjuger (choix et raison au G1, §2 et §6)**
- **Q-R18-9** : pour C-6, l'extrait dit « déclaration fausse », la lettre dit « non intègre » (§7.1 d, §7.4). J'ai suivi la lettre.
- **Q-R18-10** : noms des refus `ORACLE/nom` (premier nom fautif en ordre des points de code) et `ORACLE/vide`.
- **Q-R18-11 et 12** : genèse traitée comme un lien rompu ; `queue-non-declaree` apparaît si et seulement si la rupture rend des queues.
- **Q-R18-13** : « tailles 1 et 4 » lu comme des journaux de 1 et 4 Mio.
- **Q-R18-14** : un nom de fichier hors UTF-8 sort échappé (`backslashreplace`) au lieu de faire planter la sortie.
- **Q-R18-15** : la clé `position` du refus est gardée mais vaut toujours null.
- **Q-R18-17** : RB-18b a 199 lignes de code, mais 219 avec sa section METRIQUES. Si la borne de 200 porte sur toutes les lignes, cette section peut être versée avec RB-18c (168 lignes au total).

**6. Incidents déclarés**
- Un `od -c` a affiché les 80 premiers octets de `recalc/__init__.py` (début de sa docstring) ; rien d'autre de `recalc/`, de `rb1/` ni de `g2/` hors l'adjudication n'a été lu.
- Le mutant Mg11 était mal écrit (une seule barre oblique inverse) ; il a été réécrit avant la campagne.
- Une heure écrite dans NOTES sans relire l'horloge a été corrigée.

**7. Limites à former**
- Banc de concordance avec RB-1 corrigé (C-13) : à jouer par toi.
- E-R-33 (n_s, K_s, C_s) reste hors de ce lecteur.
- La validité (RB-3) n'est pas jugée par l'oracle.
- La mémoire n'est mesurée que contre la longueur du journal.

Copies lourdes supprimées (`copie`, `arbre`, `cible`, `tmp`). Tous mes processus détachés sont terminés.

Fichiers, sous `<scratchpad>/s2bis/rb18/corr/` :
- `diffs/RB-18a.diff` … `RB-18i.diff`, `diffs/RB-18-cumul.diff`
- `G1-CORRECTIONS-RB18.md` (sha256 `1aa0a1fa…9415`)
- `SHA256SUMS` (1 285 entrées, contrôle OK ; sha256 `10126c95…04da5`)
- `NOTES.md`, `metriques/`, `preuves/`, `outils/`, `fixtures/`, `etapes/`
