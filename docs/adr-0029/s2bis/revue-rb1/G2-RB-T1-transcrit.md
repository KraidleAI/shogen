# Relecture G2 neuve — recalcul P3, tranche 1 (transcrit)

> Transcription par l'orchestrateur le 2026-10-05 06:40:27 UTC du rapport rendu par message par le réviseur G2 (agent adaf0b340f903e00b) ; contrôle FM-1.1 du transcript : fragments_l51_l14 = 0. Texte du réviseur ci-dessous, sans retouche.

# Relecture G2 de la partie P3 du recalcul de S2-bis, tranche 1 (RB-0a à RB-1c)

**Gate 0** : modèle `claude-opus-5-5` (fiche `shogen-worker`, effort max), réviseur G2 neuf. Je n'ai rien écrit de ce lot.
Passe du 2026-10-05, de 05:43:26 à 06:38 UTC (`date -u`). Rapport par message.

## Verdict : ACCEPTE-AVEC-CORRECTIONS

La liste fermée compte quatre corrections, C-1 à C-4 (§12).

## Résumé

Le code est juste sur tout ce que j'ai éprouvé.

- **Série** : elle s'applique sur `122c670` et sur la tête `3164348`. Chaque état est vert seul, à son plancher exact, par la commande du job. Chaque diff fait au plus 200 lignes.
- **Rotation** : mes calculs indépendants la confirment. Les six vecteurs sont retrouvés par `sha256sum` et `bc`, et quatre petits cas calculés sans importer le module donnent les mêmes lois.
- **Lecteur** : il classe comme le FORMAT sur 10 cas construits à la main. Sur 5 000 altérations, il s'arrête au même endroit que le `_lire` de l'écrivain. Sur 1 762 journaux produits par l'écrivain réel avec 8 700 redémarrages, il ne donne aucun écart. Sa mémoire reste plate de 0,18 à 11,9 Mo.
- **Ce qui manque** :
  - Sur mes 20 mutants, 6 survivent à la commande du job. Tous portent sur les queues, les déclarations et le lien aux bords de fichiers. Ils ne sont pas équivalents : le code est juste, mais aucun test ne fixe ces six comportements (C-2).
  - Le chargeur ne contrôle pas le plancher de σ des oracles par actif : USDC 124 200 s, USDT 129 600 s. Ce plancher est dans le rattachement d'E-R-09 (C-1).
  - Deux corrections sont documentaires (C-3, C-4).
- **Défaut hors lot** : mon banc a fait sortir un défaut de l'écrivain du collecteur (P1), reproduit de façon déterministe. C'est un item à former (N-1).

## 1. Base et pièces

- Empreintes : `sha256sum -c` de `rb1/SHA256SUMS` donne 112 lignes OK. Le fichier lui-même a pour sha256 `fe0e16b6…1431`. Les empreintes des sept diffs sont égales à celles du rapport.
- Base et tête :
  - base `122c670`, tête `3164348`, inchangée de 05:43 à 06:37 UTC ;
  - entre les deux, seuls changent `gates.yml` (plancher du job `sim-bis`, 49 → 93) et l'ajout daté du G0 de COLLECTE.
- Copies faites par `git --no-optional-locks archive`, avec les exclusions du brief appliquées côté git (vérifiées absentes). `TMPDIR` dédié. Réseau isolé par `isole.sh` (`ebaa1c78`) et `lo_up.py` (`b532be4b`).
- `/home/user/shogen` : lecture seule, aucune opération git en écriture ; `git status` est vide à la fin.

## 2. Contrôle 1 : série

- **Application** : `git apply --check` puis `git apply` des sept diffs, en série, sortie 0 sur `122c670` et sur `3164348`. Les arbres finaux `s2bis/` et `enforcement/` sont identiques (`diff -r`).
- **Lignes ajoutées hors `docs/`** (mon comptage) : 199, 128, 102, 140, 159, 189, 64, soit 981. Tout est sous 200.
- **Chaque état seul**, par la commande du job :
  - méthode : runner `run-fixtures-verdict-suite-s2.py`, puis la ligne lue dans le `gates.yml` de l'état ; `python3.12` (3.12.3, image `ubuntu-24.04`), réseau isolé ;
  - runner : 33 ok à chaque état ;
  - verdict « conforme … Ran = N » pour N = 117, 122, 125, 130, 134, 141, 144 (base 114).

## 3. Contrôle 2 : conformité, exigence par exigence

| exigence (rattachement de la proposition) | constat |
|---|---|
| §1 pt 2, frontière de `recalc` | Règle `recalc` seul, plus serrée que la proposition (qui admet aussi `collecte.decodeurs` et une liste fermée de S2) : admis. Le refus de `collecte` et de `shogen_s2` est testé. |
| §1 pt 3, configuration scellée (sha256, refus nommé si incomplète ou incohérente) | Conforme : sha256 des octets lus, `ANALYSE/a-fixer`, `ANALYSE/incoherent`. |
| E-R-05, seuils D-2 à D-5 | Valeurs du gabarit égales à l'ADR (5 s ; 1 s et 120 s ; 2 sur 3 et 2 s ; 2 sur 2 et 2 s), fixées par le test du gabarit. Le chargeur ne pose que des bornes génériques (voir O-1). |
| E-R-07, n_s, T_max, n′_s ≥ n_s/2 | Champs présents ; `n_s` et `t_max_s` à null (lots amont) ; `diviseur_n` = 2. Conforme. |
| E-R-09, τ et σ | τ : 0,05 % ≤ τ < 2,85 %, refus nommé, aucun écrêtage : conforme. σ ≥ planchers d'ADR-0020 : conforme. **σ ≥ plancher des oracles poussés par actif : non contrôlé (C-1).** |
| E-R-15, unités | ASCII imprimable sans « : », ordre strict des points de code, pools ⊆ BTC : conforme. L'unité non décalée est un paramètre ; elle sera calculée à RB-7. |
| E-R-16, rotation | Masques, o(r, u) (vecteurs), décalage joint par hôte, modulo n, sens de l'AVIS Q-R-02 : conforme. R = 9 999 au gabarit (voir O-1). |
| E-R-17 | Entiers et `Fraction` exacts : conforme. La décision relève de RB-7. |
| E-R-18 | S, C_S, S_crit, S̄_rot sur les mêmes r : conforme. S_crit est défini comme K_crit (Q-RB-11, [abs] dans l'ADR). |
| E-R-19 | La graine est une entrée (64 hexadécimaux minuscules). Son calcul relève de RB-19. Conforme. |
| E-R-20, E-R-25, E-R-27/28 | Gardes 2, 2, 2, 2 ; P_j 0,5 % et grille {0,25 ; 0,5 ; 1 ; 2} % ; tolérance à null. Conforme. |
| E-R-01 | Lecture en flux, chaîne dans le fichier et entre fichiers, genèse, segments de reprise admis, queue tolérée seulement si déclarée ou en fin de journal, entier long nommé. Conforme, mais six comportements ne sont pas testés (C-2). |
| E-R-02 | Rupture rendue à sa place, sans arrêt ni réparation. La portée relève de RB-3 (Q-RB-10). Conforme. |
| E-R-36 | Journaux écrits par l'écrivain de CB-1 ; attendus par `chaine` (code de test indépendant). Conforme. |
| §3.4, tests et mutants obligatoires (lecteur, rotation) | Présents. Le mutant « n_s au lieu de n′_s » ne peut pas s'écrire dans RB-6 (Q-RB-14 ; à refaire à RB-7). |

## 4. Contrôle 3 : justesse du lecteur

Mon banc `banc_lecteur.py` ne prend jamais ses attendus du lecteur. Il les prend :
- de l'intégrité par fichier selon `Journal._lire` (code de référence du FORMAT §7.1) ;
- ou de la construction du cas.

Résultats, sous 3.10, 3.12 et 3.13, 19 ok :

- **Cas construits à la main** :
  - C1 ligne coupée en fin de journal : queue finale, cause `fin` ;
  - C2 octets NUL : cause `fin` sans saut de ligne, `json` avec ;
  - C3 altération d'un fichier clos puis bascule normale (rupture sans reprise) : une rupture `lien` au premier enregistrement du fichier suivant, queue de cause `chaine`, ancre lue ;
  - C4 reprise qui déclare la queue : aucune rupture ;
  - C5 entier de 701 chiffres écrit par l'écrivain : `_lire` lit tout le fichier, le lecteur y voit une queue `entier-long` puis une rupture `lien`. C'est l'écart I-1, confirmé ;
  - C6 fichier du milieu retiré, premier retiré, deux noms échangés (trois ruptures), doublon en segment 7 (une rupture), fichier vide ignoré ;
  - C7 ligne de 4 194 304 octets exactement : lue intègre ;
  - C8 U+2028, U+2029, U+0085 et `\r` dans une chaîne ;
  - C9 reprise dans le même fichier avec horloge reculée ;
  - C10 ouverture du lendemain coupée puis reprise en segment 1.
- **Différentiel** : 3 000 (3.12) puis 5 000 (3.10, 3.13) altérations d'un fichier (octet changé, coupé, inséré, troncature). La fin intègre du lecteur est égale à celle de `_lire`.
- **Propriété**, sur 2 000 graines :
  - scénario : écrivain réel, sauts, bascules, pannes (troncature, NUL, ligne coupée), redémarrages avec horloge parfois reculée ;
  - volume : 1 762 journaux, 8 700 redémarrages, 7 298 queues déclarées, 716 queues finales ;
  - résultat : 0 écart sur le flux, les ruptures (aucune), `queues`, `queue_finale` et la tête.
  - Trois scénarios relèvent du défaut N-1 de l'écrivain (§14) : deux `FileExistsError` et une rupture `LECTEUR/declaration`, qui est le classement juste au sens du FORMAT §7.2.
- **Mémoire** (`memoire.py`, pic de `tracemalloc`) :
  - lecteur : 21 864, 21 679, 12 236 et 16 550 octets pour 184 Ko, 737 Ko, 2,96 Mo et 11,9 Mo (2 à 32 fichiers), sous 3.10 ; même allure sous 3.13 ;
  - témoin « fichier entier » : de 378 Ko à 1,32 Mo ;
  - la mémoire est bornée et la mesure discrimine.

## 5. Contrôle 4 : justesse de la rotation

- **Six vecteurs**, par `printf '%s' … | sha256sum`, puis `bc` :
  - résultats : 107 527 ; 24 225 ; 39 743 ; 0 ; 6 ; 52 807, avec des empreintes identiques à celles du worker ;
  - contrôles de `bc` : FF mod 7 = 3 ; (2^256 − 1) mod 109 440 = 13 695 par les deux voies ;
  - 107 527 mod 54 720 = 52 807 : cohérent.
- **Calcul indépendant**, sans importer le module :
  - cas A en shell seul (`sha256sum`, `bc`, `awk`), n = 5, 20 rotations, trois lignes vérifiées à la main (r0, r2, r12) ;
  - cas B (deux classes jointes, n = 7, R = 30), C (`premiere` à None, n = 9, R = 40), D (première unité absente de la classe), en Python sur des listes ;
  - `lois` donne les mêmes K, C, K_crit, K_moyen, K_r, S, C_S, S_crit, S_moyen et S_r, sous 3.10 et 3.13.
  - Exemple, cas A : K = 2, C = 17, K_crit = 3 (seuil 2), K̄ = 37/20, S = 2, C_S = 17, S_crit = 5, S̄ = 53/20.
- **Comparaison au `r1` de S2** : `r1.py` n'a aucune rotation ; la définition de K est la même (`win_ecarts >= 2`).
  - Écarts voulus :
    - rang dans la suite comprimée au lieu de la position de grille (ADR l.137, AVIS Q-R-01) ;
    - entiers et `Fraction` au lieu de `Decimal` (E-R-17) ;
    - décalage par SHA-256 et son encodage (AVIS Q-R-02) ;
    - unité = hôte, et non flux (§2.5).
  - Aucun écart fortuit trouvé.

## 6. Contrôle 5 : configuration

- **Ce qui marche** :
  - le gabarit est refusé en `ANALYSE/a-fixer` (n_s, t_max_s, tau_sigma, tolerance_evenements, unites) ;
  - complété, il est accepté ;
  - les bornes de τ (0,0005 admis, 0,0285 refusé), les fractions strictes (21 décimales refusées) et les planchers d'ADR-0020 marchent.
- **Ce que le chargeur accepte à tort** (`preuves/sondes_config.txt`) :
  - R = 99 avec seuil = 0, et R = 999 avec seuil = 9 (voir O-1) ;
  - σ = 5 400 s pour l'oracle USDC et σ = 6 000 s pour l'oracle USDT (C-1) ;
  - τ d'oracle sous 0,375 % (USDC) et sous 0,75 % (ETH) (voir O-2) ;
  - τ de BTC hors de la grille de 0,05 % (voir O-2) ;
  - une espace dans un nom d'unité (Q-RB-13, voir O-3).

Le rattachement d'E-R-09, « l.185-187 (autres actifs) », est écrit à `e16956b`. Relu par `git show e16956b:…`, l.186 y est « Planchers des oracles poussés : τ ≥ 1,5 × seuil de déviation (0,75 % ETH, 0,375 % stables) ; σ = 1,5 × heartbeat : ETH 5 400 s, USDC 124 200 s, USDT 129 600 s » ; c'est l.188 à la tête. L'énoncé « σ ≥ plancher » d'E-R-09 couvre donc ces valeurs, et la prémisse de Q-RB-4 (« E-R-09 ne fixe que la borne CAPO ») est inexacte pour σ.

## 7. Contrôle 6 : rouge et vert, rejoués sur quatre pas

Suite entière, `python3.12`, réseau isolé :

| pas | rouge | vert |
|---|---|---|
| RB-0b (code de RB-0a, tests de RB-0b) | 34 échecs dans 4 tests, 0 erreur | Ran 122, OK |
| RB-6a (souche du worker) | 23 échecs dans 3 tests, 0 erreur | Ran 125, OK |
| RB-6b (souche du worker) | 63 échecs dans 4 tests, 0 erreur | Ran 130, OK |
| RB-1c (souche du worker) | 2 échecs dans 2 tests, 0 erreur | Ran 144, OK |

Les souches sont le code de l'état précédent plus une API vide (vérifié par `diff`). À RB-1c, le test de mémoire n'est pas rouge : il caractérise un comportement déjà présent depuis RB-1b, et sa force est montrée par le mutant M-1c-05.

## 8. Contrôle 7 : mutants

Classement par la commande du job : runner puis ligne de `gates.yml`, borne de 300 s, FATAL au-delà, copie fraîche par mutant. Lanceur à moi : `campagne_g2.py` avec `job.py`.

- **Mes 20 mutants**, sur l'état final, témoin vert à 144 : **14 tués** par leur test visé, **6 vivants**, 0 FATAL. Les survivants :
  - G-13 : reprise à `queue` null admise alors qu'une queue attend ;
  - G-14 : déclaration non contrôlée quand aucune queue n'attend ;
  - G-15 : queue finale réduite à la dernière ;
  - G-16 : seule la dernière queue en attente gardée ;
  - G-19 : queue d'un octet ignorée ;
  - G-20 : lien non contrôlé pour une reprise en tête de segment.
- **Non-équivalence**, montrée sur des journaux de l'écrivain réel (`preuves/survivants-non-equivalents.txt`) : le lecteur original classe juste et chaque mutant classe faux. G-16 porte même sur un journal produit par l'écrivain réel après deux pannes successives, sans altération. C'est une faiblesse de la suite, pas du code (C-2).
- Les 14 tués comprennent le plancher Chainlink − 1, l'espace refusée, un bloc amont prérempli, `echo` au lieu de `printf`, 31 octets d'empreinte, r de 0 à R − 1, C + 1, la moyenne sur R + 1, x_crit à 1, l'unité non décalée prise par classe, 640 chiffres refusés et la rupture absente du flux.
- **Échantillon de 23 mutants du worker** (4, 4, 3, 4, 3, 3 et 2 par sous-lot), chacun rejoué sur l'état où il a été écrit, 7 témoins verts : **23 tués**, test visé en échec, 0 vivant, 0 FATAL.

## 9. Contrôle 8 : CI

- Seule la ligne du plancher change (114 → 144) ; `--aucun-saut` et `--egal` restent.
- `enforcement/` est inchangé (`diff -r`).
- `test_fitness.py` est resserré, rien n'est retiré :
  - règle de `recalc` ;
  - présence d'un module de `recalc` ;
  - refus de `..collecte` et de `shogen_s2.r1`.
- Le câblage K-02 du runner est vert. Aucune gate n'est affaiblie.

## 10. Contrôle 9 : règles et xtask

- **R-13** : 0. **R-8** : bibliothèque standard seule (analyse `ast` des huit fichiers).
- **Octets 92** :
  - comptés par fichier ;
  - chaque ligne qui en porte est lue : la regex `0\.[0-9]{1,20}` n'a qu'une barre (`od -c`), les autres sont des échappements voulus (`\n`, `\t`, `\x7f`, JSON dans les tests) ;
  - mes propres outils écrivent leurs barres par `chr(92)` et sont contrôlés.
- **Interpréteurs** : Python 3.10.20, 3.11.15, 3.12.3 et 3.13.14 en `-X dev -W error` donnent Ran 144, OK, 0 avertissement. La ligne du job est conforme sous les quatre.
- **Autres gates** :
  - `s2-harness` : Ran 405, OK (skipped=2) ;
  - gate des secrets en `--tree`, dans un index jetable de mon espace : « OK (secrets) : 12 fichier(s) ».
- **`cargo --locked xtask verify`**, hors réseau, sur la copie témoin et sur la copie avec la série :
  - lignes de verdict identiques entre les deux, et identiques à celles du worker ;
  - S-G1 à S-G8 vertes (S-G4 et S-G5 couvrent `docs/**/*.md`, donc `ROTATION-S2BIS.md`) ;
  - S-G9 rouge sur `docs/17-modele-de-menace.md:70`, cas connu sur les copies ;
  - fmt et clippy verts.

## 11. Contrôle 10 : avis sur les écarts et les items

- **E-1** (découpage en sept diffs) : justifié par R-25, tailles vérifiées. Admis.
- **E-2** (passage invalide de RB-6b) : les preuves concordent. M-6b-01 a atteint la borne (300,1 s), il est classé FATAL et non compté ; la campagne complète a été relancée (17 sur 17). Traitement conforme à SHOGEN-MUT-FATAL-1. Admis.
- **E-3** (artefacts de souche) : mon rejeu de RB-6b ne montre que des échecs d'assertion. Admis.
- **E-4** (ligne vide finale) : sans effet sur les tests ; mon rejeu des mutants M-1a et M-1b sur les états livrés les tue. Mais METRIQUES n'a pas été mis à jour (C-3).
- **E-5** (git hors du dépôt) : conforme ; j'ai fait de même pour la gate des secrets.
- **E-6** (machine partagée) : admis.
- **I-1** (entier à l'écriture) : confirmé par C5 (701 chiffres écrits puis vus en queue). À former, avec la borne de 640 chiffres écrite aussi au FORMAT §1.2, avant le gel.
- **I-2** (FORMAT §7.1, contrôles de type) : à former. Le FORMAT §7.2 est aussi en défaut (N-1).
- **I-3** (ancre d'une rupture) : à former, complété par N-2.
- **I-4** (configuration croisée), **I-5** (coût à re-mesurer), **I-6** (frontière vers S2) : à former tels quels.
- **I-7** (estimation) : rapports recalculés exacts (×2,18, ×2,17, ×1,27, ×1,85) ; restes de P3 ≈ 2 054 lignes, P4 ≈ 3 996. Information juste.
- **I-8** (assertions sur de grandes structures) : consigne utile. À former.

## 12. Corrections, liste fermée

**C-1 (RB-0b, E-R-09, code et test).** Contrôler σ ≥ plancher par (actif, `oracle_chainlink`) :

| actif | plancher de σ | source |
|---|---|---|
| BTC | 5 400 s | ADR-0020 |
| ETH | 5 400 s | ADR l.188 à la tête |
| USDC | 124 200 s | ADR l.188 à la tête |
| USDT | 129 600 s | ADR l.188 à la tête |

- Refus nommé `ANALYSE/sigma`.
- Un test : plancher admis et plancher − 1 refusé, pour USDC et USDT.
- Un mutant tué.

**C-2 (RB-1b et RB-1c, tests).** Ajouter des tests qui tuent G-13, G-14, G-15, G-16, G-19 et G-20 sous la commande du job. Comportements à fixer :
- reprise à `queue` null derrière une queue en attente → `LECTEUR/declaration` ;
- reprise déclarant une queue quand aucune n'attend → `LECTEUR/declaration` ;
- deux queues en fin de journal → les deux en `queue_finale` ;
- deux queues déclarées ensemble par la reprise suivante (deux pannes de l'écrivain réel) → aucune rupture, les deux dans `queues` ;
- queue d'un octet relevée ;
- reprise en tête de segment au lien faux → `LECTEUR/lien`.

Pour chacun : rouge montré sur le mutant, puis vert, et plancher relevé.

**C-3 (`METRIQUES-S2BIS.md`).** Corriger les comptes de lignes :
- RB-0a : `test_fitness.py` fait 74 lignes, et non 76 ;
- RB-1a : `test_lecteur.py` fait 76 lignes, et non 77 ;
- RB-1b : `test_lecteur.py` fait 202 lignes, et non 203.

**C-4 (`lecteur.py`, docstring de `_integre`).** Le troisième élément de l'état n'est pas « comme l'écrivain le calcule » : l'écrivain retient `ws + w` après un marqueur ou un trou (écart mesuré : 60 s). Corriger la docstring (type seul), ou la valeur et le test qui la fige.

## 13. Observations, non bloquantes

Les choix relèvent de l'orchestrateur ou des Q-RB.

- **O-1** (Q-RB-6) :
  - R et le seuil ne sont figés que par le test du gabarit ; le chargeur admet R = 99 avec seuil = 0, et R = 999 avec seuil = 9 ;
  - je recommande l'égalité R = 9 999 et seuil = 99 dans le chargeur ;
  - pour D-2 à D-5, garder des bornes génériques est défendable (l.115 : seuils amendables avant le sceau).
- **O-2** (Q-RB-4) : planchers de τ des oracles (l.188), grille de 0,05 % de τ de BTC (l.181), et σ(actif, classe) ≥ σ_BTC(classe) (l.189). Resserrements recommandés.
- **O-3** (Q-RB-13) : je recommande de restreindre les noms d'unité aux caractères d'un nom d'hôte (lettres, chiffres, « - » et « . »). Une espace finale crée une unité distincte, sans signal.
- **O-4** : la copie de la lecture JSON stricte de `collecte/config.py` n'a pas d'épreuve croisée, alors que la PROPOSITION emploie ce patron pour la copie de `window_start`.
- **O-5** : `queue_finale` tolère aussi des causes qu'une panne de l'écrivain ne produit pas (`chaine`, `canonique`, `champ`, `flottant`). La cause est relevée ; RB-3 devrait l'imprimer, ou une règle devrait trancher.
- **O-6** : le commentaire de `test_fitness.py`, « ni collecte (hors décodeurs) », décrit la règle de la proposition ; la règle codée refuse aussi les décodeurs.
- **O-7** : RB-6 reste susceptible de changer de forme si la variante non enroulée entre en sensibilité (ix) (ajout daté l.399 (3) ; AVIS Q-G-02).

## 14. Items à former (règle PAROXYSME)

**N-1, SHOGEN-S2BIS-SEGMENT-JOUR-1 (écrivain, CB-2, hors de ce lot).** Reproduit de façon déterministe (script dans la sortie de `preuves/`, et trois graines du banc).
- **Déclencheur** : une panne laisse le fichier du jour D sans ligne intègre (ou vide), puis l'écrivain redémarre avec l'horloge revenue au jour C < D.
- **Effet** :
  - l'écrivain crée le segment C-1 ; sa `reprise` déclare la queue de D-0, nommé après lui ;
  - l'ordre des noms n'est plus l'ordre de la chaîne, contrairement au FORMAT §7.2 ;
  - le lecteur signale `LECTEUR/declaration` ;
  - la bascule suivante vers D lève `FileExistsError` : l'écrivain est cassé (`JOURNAL/casse`).
- **Remède proposé** :
  - jour du segment neuf = max(jour de l'horloge, jour repris, jour de tout fichier existant) ;
  - à la bascule, numéro de segment = 1 + max(k du jour) ;
  - FORMAT §7.2 réécrit ;
  - avant le gel du collecteur.

**N-2 (complément d'I-3 et de Q-RB-10, pour RB-3).**
- La ligne `apres` d'une rupture n'est vérifiée par aucun successeur : une ligne altérée mais canonique est rendue intègre (C3b).
- Une ancre peut rendre des fenêtres déjà lues (doublon, C6b) ou antérieures (noms échangés).
- RB-3 doit donc contrôler la monotonie de `ws` à travers les ruptures, et inclure la fenêtre de `apres` dans la portée.

## 15. Journal G1 (provenance)

**[lu]** (préfixe du sha256) :
- **Briefs et rapport** :
  - brief G2 `876143f2` ;
  - rapport transcrit `b0977f09` ;
  - brief du worker `29d75bd2`, en entier.
- **G0** :
  - G0 `fe57eeb1` (tête) et `56f9ca73` (base), en entier ;
  - PROPOSITION `0cdf84c2`, l.1-618 et 783-927 (§4 DEPLOI non lu) ;
  - AVIS `a919b307`, en entier.
- **ADR-0029** :
  - à la tête (`b908842d`) : l.76-117, 135-142, 150-249, ajouts datés l.6, 143, 183, 397 et 399, et les lignes 120, 139, 141, 182, 200, 202, 212 ;
  - à `e16956b` : l.179-188, 198-203, 210.
- **FORMAT** `08c6b20e`, en entier.
- **Paquet `s2bis`** :
  - `collecte/journal.py` `958f5a8d`, en entier ;
  - `collecte/config.py` `77f909e5`, l.1-70 ;
  - `test_fitness.py` `93e1aaf6`, en entier ;
  - en-têtes de `test_journal.py` `87804f34`, `test_fichiers.py` `1c314a8d` et `test_reprise.py` `4c80609f`.
- **`s2-harness`** :
  - `r1.py` `c5666e8d`, l.1-60, 316-405 et 553-670 ;
  - `run_campaign.py` `12db6c84`, l.118-130 ;
  - `sources.py` `0c81fc33`, l.326-338.
- **CI et gates** :
  - vérificateur `83271f84`, l.1-80 ;
  - runner `2778270f`, l.1-40 ;
  - `gates.yml` `2f9f9c43`, l.185-222 ;
  - en-têtes de `sg4.rs` `b0f7f125`, `sg5.rs` `e2629451` et `gate-secrets.sh` `f89abf0f`.
- **SIM-BIS** : PROPOSITION `0e78afab` et AVIS `aaf70a4f`, par recherche ciblée.
- **Pièces du worker** : les 7 diffs en entier, ses outils, ses souches et ses preuves (extraits).

**[abs]** :
- définition de S_crit ;
- collation exacte de « ordre alphabétique » ;
- schéma d'`analyse.json` ;
- noms des classes dans `formes.json` ;
- portée d'une rupture sans reprise ;
- contrôles de type au FORMAT §7.1.

**[2nd]** : rien.

**Non ouverts** :
- `AVIS-RB-T1.md` de l'advisor, apparu pendant ma passe, non lu pour rester indépendant ;
- pièces de D.2, tout `*.jsonl` réel, dossiers interdits.

Aucune recherche récursive sur `docs/`, sur le dépôt ou sur le scratchpad. `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée.

**Chiffres recalculés** :
- VALIDE : 1 001 octets, `fcf18be5…cd14` ;
- `int_info.str_digits_check_threshold` = 640, défaut 4 300 (3.10 et 3.13) ;
- 24 semaines = 14 515 200 s ;
- n_calme = 109 440 et n_stress = 43 776 ;
- 0x2D < 0x2E ;
- les rapports d'I-7.

**Nettoyage** : copies, états, cible cargo (137 Mo) et temporaires supprimés. Le dossier du réviseur fait 716 Ko.

## 16. Fichiers

- Dossier du réviseur : `<scratchpad>/s2bis/rb1/g2/`.
- Empreintes : `<scratchpad>/s2bis/rb1/g2/SHA256SUMS-reviseur` (52 lignes, sha256 `184071d9…9623`).
- Outils : `…/rb1/g2/outils/`
  - `job.py`, `campagne_g2.py`, `mutants_g2.py`, `echantillon_worker.py`, `vise.py` ;
  - `banc_lecteur.py`, `memoire.py`, `verif_rotation.py`, `cas_a.sh`, `xtask.sh`.
- Preuves : `…/rb1/g2/preuves/`
  - `etat-*`, `rouge-*` et `vert-*` ;
  - `banc_lecteur_*`, `memoire_*`, `cas_a.txt`, `verif_rotation_attendu.json`, `sondes_config.txt`, `survivants-non-equivalents.txt` ;
  - `mutants-g2.*` et `mutants-echantillon-worker.*` ;
  - `dev-*`, `verdict-*`, `s2-harness-final.txt` et `xtask-*`.

