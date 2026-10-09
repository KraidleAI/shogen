# Relecture G2 neuve de SB-13 (transcrit)

> Transcription par l'orchestrateur le 2026-10-09 00:44:06 UTC du texte rendu par l'agent a892126a600cd358b (workflow wf_b92ecd95-a7d) ; contrôle FM-1.1 de son transcript : fragments_l51_l14 = 0 ; modèle résolu : claude-opus-5-5. Texte de l'agent ci-dessous, sans retouche (seul le chemin du scratchpad est abrégé en `<scratchpad>`).

**Gate 0** : je tourne sous `claude-opus-5-5` (identifiant exact), en réviseur G2 neuf, effort max. Je n'ai écrit aucun des diffs relus. Relecture du 2026-10-08, de 21:09:51 à 22:01 UTC.

Je n'ai fait aucune écriture git dans `/home/user/shogen` et aucun commit. `SHOGEN_S2_CAMPAGNE_CONTROL` n'a jamais été posée. Je n'ai ouvert ni `*.jsonl`, ni pièce de D.2, ni dossier interdit, et je n'ai fait aucune recherche récursive.

## Verdict : ACCEPTE-AVEC-CORRECTIONS (liste fermée C-1 à C-3)

**E-S-51, première moitié : tenue.** Les vecteurs, les 100 séries et ma sonde indépendante donnent 0 écart. **CONTRAT-RB6-1** est tenu par trois tests qui lient vraiment les deux textes. La frontière E-S-01 reste testée. Deux de mes mutants survivent : ils ne sont pas équivalents et il leur manque un cas de test (C-1, C-2).

- **C-1 (M-G2-01 vivant).** `croiser` doit comparer o(r, u) pour toute unité décalée, mais `test_croiser_voit_les_ecarts` n'a que BTC.
  - Le mutant « o croisés pour les seules unités de BTC » (l.131) passe le job.
  - À ajouter : une unité absente de BTC, avec un o altéré, et l'écart `("o", r, u)` attendu.
  - La sonde montre que `croiser` intact voit cet écart (99 sur 99).
- **C-2 (M-G2-02 vivant).** Tous les appels de `croiser` passent n_s = n. Le sixième vecteur (n′ = n/2) est croisé à n = n_s = 54 720.
  - Le mutant « n_s transmis à RB-6 au lieu de n » (l.128) passe le job.
  - À ajouter : au moins une entrée à n′ < n_s, par exemple le sixième vecteur avec n_s = 109 440, sans écart attendu.
  - Sonde : 0 écart sur 39 séries à n_s ≠ n avec le code intact ; 33 séries en écart sous le mutant.
- **C-3 (Q-SB13-7).** Ajouter la ligne `oracle_recalc.py` au README de `scripts/sim-bis`, dans la variante pour 5e386c4. La raison de ne pas le toucher, le conflit avec SB-15, est tombée.

Ces corrections portent sur la variante, avec un plancher exact relevé si un test est ajouté, et des diffs de 200 lignes au plus.

## Contrôles

- **Intégrité.** `SHA256SUMS` du générateur (412 lignes) : `sha256sum -c` sort à 0. Les huit diffs ont les empreintes du rapport. La série appliquée sur une copie neuve de 5cfe746 donne exactement les étapes e13a à e13d.
- **Sonde, écrite avant de lire le code.**
  - Vecteurs par `sha256sum` et `bc` : 6 sur 6.
  - RB-6 extrait par moi de f458980, contre `regle.py` et une référence naïve, sur 200 séries : 818 114 K^(r) et 4 398 o, 0 écart.
  - Noms : 38 caractères admis sur 1 114 112, aucune divergence. Seuils : 100 R admis, aucune divergence de R = 0 à 10 100.
  - Recompte : 90 180 o et 105 714 K^(r) dans les 100 séries, comme le rapport.
- **Commit cité.** Les six empreintes à f458980 sont celles de l'épingle ; elles sont identiques à e6d201a, 5cfe746 et 5e386c4.
- **Mes 17 mutants**, classés par la commande du job (borne 300 s) : 14 tués, 3 vivants, 0 FATAL. Le troisième vivant, M-G2-12, est équivalent à ce commit (O-1).
- **Mode strict** (`-X dev -W error`, Python 3.10 à 3.13, PYTHONHASHSEED 0 et 3) : 8 runs sur 8 verts. Avec PYTHONDEVMODE et PYTHONWARNINGS hérités par les processus enfants, sous 3.12 et 3.13 : 2 sur 2 verts.
- **Planchers exacts** (chaque étape « conforme ») : 172 → 177 → 181 → 184 → 187 sur 5cfe746 ; 194 → 199 → 203 → 206 → 209 sur 5e386c4.
- **Portes**, sur les deux bases :
  - runner : 136 ok ;
  - sim-bis : conforme, aussi sous `unshare -n` ;
  - s2bis : 255 ;
  - S2 : 415, avec 2 sauts qui nomment la variable ;
  - hooks / model-pinning / secrets : 54 / 227 / 147 ok ;
  - `gate-secrets --tree` sur la variante : OK ;
  - R-13 : 0 constat.
- **Forme.** Aucun octet 92. La seule ligne ajoutée de plus de 120 caractères est la `source` du JSON.
- **xtask**, lignes de verdict identiques entre série et base, sur les deux bases : S-G1 à S-G8 VERT, S-G9 ROUGE (1 violation, déjà sur la base), fmt, no_std et clippy VERT.
- **La tête a avancé pendant ma relecture**, à c58b997. Ce saut ne touche que JOURNAL.md, README.md et README.fr.md à la racine, et les quatre diffs de la variante s'appliquent sur c58b997 : la variante reste celle à commettre.

## Observations (non bloquantes)

- **O-1.** Mutant M-G2-12 : lire `analyse.json` dans l'arbre de travail au lieu de l'extraction passe le job, parce que les octets sont identiques aujourd'hui. Aucun test ne distingue les deux chemins. À reprendre à la seconde passe.
- **O-2.** Les 100 séries ont au plus 6 unités par classe, contre 10 dans les pools réels. S^(r) avec 8 écarts ou plus à une même position n'est jamais croisé avec RB-6 : M-G2-13 n'est tué que par `test_regle`. E-S-51 n'exige que o et K^(r) ; ajouter des classes de 10 unités reste recommandé.
- **O-3.** Les rouges sont montrés par des ébauches ou par des mutations nommées. L'écart E-2 est déclaré. Acceptable.
- **O-4.** Le commentaire de `fetch-depth: 0` dans `gates.yml` ne cite que SB-14 ; SB-13 en est une seconde raison. Facultatif.
- **O-5.** `collecte/entree.py` n'existe pas à f458980 : la proposition « une ligne d'épingle » de Q-SB13-6 ne tient pas sous cette épingle.

## Avis sur les questions

- **Q-SB13-1** (section dans `parametres.json`, schéma dans `commun.py`) : adopter.
- **Q-SB13-2** (commit f458980) : adopter.
- **Q-SB13-3** (grandeurs comparées) : adopter, conforme à l'avis de la tranche 3 (AVIS-SIM-T3 l.120, P-5).
- **Q-SB13-4** (six fichiers extraits) : adopter.
- **Q-SB13-5** (forme des séries) : adopter, sous réserve de C-2.
- **Q-SB13-6** (HOTE-COMMUN-1) : ne pas l'étendre ici. Laisser l'item ouvert, avec la mention « deux textes sur trois liés » ; à reprendre à la seconde passe (O-5).
- **Q-SB13-7** (README) : faire la correction C-3.
- **CONTRAT-RB6-1** : fermable sur ces pièces ; tu adjuges. **ORACLE-RB7-1** reste ouvert.

## Écarts du réviseur

- **E-G2-1.** Quatre octets 92 dans mes premières sondes, réécrits par gabarit avant tout usage ; 0 octet 92 contrôlé ensuite.
- **E-G2-2.** J'ai affiché six lignes d'en-tête de la section S-G9 (aucune ligne de violation), en plus des lignes de verdict.
- **Nettoyage non fait.** L'outil a bloqué la suppression de `g2/copies/` (19 arbres, 258 Mo) et de `g2/cible/` (137 Mo, cible cargo). Je ne l'ai pas contourné : à retirer de ton côté si tu le veux. Aucune pièce du rendu n'est dans ces dossiers.

Fichiers, dans `<scratchpad>/s2bis/sb13/g2/` :
- RAPPORT-G2.md (sha256 `64e2630c…0e70`)
- NOTES.md
- SHA256SUMS (114 fichiers, `4f637b58…27bc`)
- logs/campagne-g2.log
- sonde/
- outils/