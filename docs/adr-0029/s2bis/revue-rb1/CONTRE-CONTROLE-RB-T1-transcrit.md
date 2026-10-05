# Contre-contrôle des corrections du recalcul, tranche 1 (transcrit)

> Transcription par l'orchestrateur le 2026-10-05 08:38:51 UTC du rapport rendu par message par le réviseur G2 (agent adaf0b340f903e00b) ; contrôle FM-1.1 du transcript : fragments_l51_l14 = 0. Texte du réviseur ci-dessous, sans retouche.

# Contre-contrôle des corrections de la tranche 1 du recalcul (RB-1d à RB-1g)

**Gate 0** : `claude-opus-5-5`, réviseur. Passe du 2026-10-05, de 08:16:14 à 08:38 UTC (`date -u`). Rapport par message.

## Verdict : CONFORME

C-1 à C-4 sont corrigées. Les points de l'avis sont fidèles à l'ADR. Toutes les gates sont vertes sur la série complète. Il reste un point mineur, né de RB-1e, que je rends en item (point 5) et non en correction.

**Base** :
- empreintes : `corr/SHA256SUMS` donne 110 lignes OK (`d2705164…`) ;
- copie de `3164348` (tête inchangée pendant la passe), aux exclusions habituelles ;
- les 11 diffs s'appliquent en série, chaque `git apply --check` sort à 0 ;
- lignes de code ajoutées : 76, 83, 31 et 37 ; tailles finales égales au tableau du worker.

## 1. C-1 à C-4

- **C-1, corrigée** :
  - le plancher de σ de l'oracle par actif est BTC 5 400, ETH 5 400 (plancher de classe), USDC 124 200 et USDT 129 600 ;
  - le test admet le plancher et refuse le plancher − 1.
- **C-2, corrigée** : six cas nommés.
- **C-3, corrigée** : 74, 76 et 202 lignes.
- **C-4, corrigée** : la docstring de `_integre` est exacte (`ws` et `a`, là où l'écrivain retient `ws + w` et `a + w`) ; l'état d'un marqueur est désormais fixé par un test.

**Mes mutants** :
- Rejoués sur l'état final, par la commande du job : runner, puis la ligne `--egal --plancher 156`, borne de 300 s, FATAL au-delà, témoin vert à 156.
- Résultat : **36 tués sur 36**, 0 vivant, 0 FATAL, chacun avec son test visé en échec, de 19,7 à 25,5 s par passage :
  - G-01 et G-03 à G-20, textes inchangés : 19 sur 19, dont les six vivants d'hier (G-13 à G-16, G-19, G-20) ;
  - G-02′ et mes 7 variantes de G-02 ;
  - 9 mutants neufs.

**G-02′ est une transposition fidèle** : même caractère (0x20), même frontière, même règle. Le sens est inversé parce que Q-RB-13 a inversé le statut de l'espace. Mes variantes tenaient l'autre côté de la frontière ; elles sont toutes tuées :
- « - » refusé, « z » refusé ;
- 253 caractères refusés, 254 admis ;
- majuscules admises ;
- `match` au lieu de `fullmatch`, côté chargeur comme côté décalages.

**Mes 9 mutants neufs, tous tués** :
- N-01 : σ de l'oracle USDC − 1 ;
- N-02 : plancher de τ de l'oracle ETH abaissé ;
- N-03 : grille de 0,05 % imposée à tous les actifs ;
- N-04 : σ ≥ σ_BTC étendu aux oracles ;
- N-05 : `>` au lieu de `>=` dans σ ≥ σ_BTC ;
- N-06 : bornes de R d'avant Q-RB-6 ;
- N-07 : la copie seule modifiée ;
- N-08 : l'original seul modifié ;
- N-09 : τ égal au plancher refusé.

## 2. Points de l'avis

- **Q-RB-4, fidèle.**
  - Planchers de τ des oracles : 0,75 % pour ETH, 0,375 % pour les stables (l.188).
  - Grille de 0,05 % sur toutes les classes de BTC seulement (l.181) ; pour les places des autres actifs, la grille est celle du G0 de CALIB-ACTIFS (l.187).
  - σ ≥ σ_BTC pour les places et les agrégateurs : c'est la lettre de l.189.
  - À l.181-189, j'ai relu l'ADR à la tête ; dans la PROPOSITION, les numéros sont ceux de `e16956b`.
- **Q-RB-6, fidèle** : R = 9 999 et seuil = 99 exacts (l.139, l.200, l.202) ; la cohérence alpha reste en seconde garde ; les tests à petit R passent par `lois()`.
- **Q-RB-13, fidèle à l'adjudication** : une seule constante `HOTE = [a-z0-9.-]{1,253}` (`fullmatch`), partagée par les décalages et le chargeur ; refus nommés.
- **Q-RB-1, fidèle** : le test compare par `ast` les segments `_objet` (l.20), `_entier` (l.27) et, dans `charger` (l.32), la lecture, le `try` et le retour (l.46). L'égalité vaut après normalisation des préfixes ; tout changement d'un seul côté est tué (N-07, N-08).
- **`ROTATION-S2BIS.md`, fidèle** :
  - le §1 pt 8 porte la précision de l.200 (Q-RB-5) ;
  - les faits du §8 sont vérifiés sur pièce : `comprimer` place les bits en positions 0, 1, … (`calendrier.py` l.76-81) ; `calibration.strates` vaut calme et stress ; `indices_hotes` est en noms courts ; l'item SHOGEN-SIM-BIS-INDICES-IDENTIFIANTS-1 existe (annexe B l.1068).

## 3. Adjudications des questions neuves

- **Q-RBc-1 (σ ≥ σ_BTC sur les places et les agrégateurs seulement)** : juste. Le σ des oracles est la valeur de l.188 (ETH 5 400 s, qui peut être sous σ_BTC) ; étendre la règle refuserait la valeur de l'ADR elle-même (N-04 le montre).
- **Q-RBc-2 (classe absente de BTC refusée)** : juste en refus par défaut. l.189 exige le terme σ_BTC(classe), et les pools sont pris parmi les hôtes de BTC (l.173).
- **Q-RBc-3 (item RFC 1123)** : d'accord. Le jeu de caractères garantit déjà ce que le hachage exige (ni « : », ni espace, une seule casse) ; la structure en étiquettes peut attendre le gel des identifiants, avec la RFC lue sur pièce.
- **Q-RBc-4 (item vers CALIB-ACTIFS)** : d'accord, avec une précision à écrire dans l'item. La grille de 0,05 % de τ des agrégateurs des autres actifs est fixée par l.189 elle-même ; ce contrôle ne dépend d'aucune valeur et pourrait se faire dès maintenant, comme celui de BTC.
- **Q-RBc-5 (0 ≤ masque < 2^n)** : juste. 2^n a son bit n hors de la suite, et le code le refuse (`m >> n == 0`) ; le « ≤ 2^n » du brief était inexact.
- **E-3** : sain. La nouvelle VALIDE fait 1 000 octets, `c7597368…a15e`, recalculé hors du code. Elle ne diffère de l'ancienne que par σ(BTC, place horodatée), de 180 à 30, changement exigé par la règle sigma-btc. La frontière reste éprouvée : un σ de l'oracle BTC à 10 800 s est admis, et un σ égal à σ_BTC aussi.

## 4. Gates sur la série complète (7 + 4 diffs sur 3164348)

- **Chaque état de correction seul**, par la commande du job : conforme à 150, 155, 155 et 156 ; runner 33 ok.
- **Interpréteurs** : Python 3.10.20, 3.11.15, 3.12.3 et 3.13.14 en `-X dev -W error` donnent Ran 156, OK, 0 avertissement ; la ligne du job est conforme sous les quatre.
- **Autres jobs** :
  - `sim-bis` : conforme, Ran 93 ;
  - `s2-harness` : conforme, 405 tests, OK (skipped=2).
- **Règles** :
  - R-13 : 0 sur les 11 diffs ;
  - R-8 : bibliothèque standard seule ;
  - octets 0x5C : nombre inchangé dans chacun des 7 fichiers ; la seule ligne ajoutée qui en porte est une ligne déplacée.
- **xtask** : lignes de verdict identiques entre le témoin et la série, et identiques à celles du worker. S-G1 à S-G8 vertes ; S-G9 rouge sur `docs/17:70`, cas connu ; fmt et clippy verts.
- **Non-régression** :
  - mon banc du lecteur : 500 graines, 452 journaux, 2 199 redémarrages, aucun écart (une collision connue, N-1) ;
  - rotation égale à mon calcul indépendant ;
  - les six vecteurs sont égaux.

## 5. Item proposé, non bloquant

**SHOGEN-S2BIS-DECIMAL-CONTEXTE-ANALYSE-1.**
- **Constat** : le contrôle `Decimal(τ) % GRILLE_BTC`, ajouté par RB-1e, est la seule opération du chargeur qui dépende du contexte décimal ambiant. Sous une précision de 1, `charger` lève une `InvalidOperation` non nommée ; il passe sous 28 et sous 2. Cela contredit le principe SHOGEN-DECIMAL-CONTEXTE-1 (contexte nommé, jamais celui de l'appelant).
- **Remède** : un contrôle exact et indépendant du contexte (`Fraction(τ) * 2000` entier), avec un test sous contexte hostile. Déclencheur : RB-2, premier appel de `charger` par le recalcul.
- **Pourquoi pas une correction** : aucun contexte réaliste n'est touché. Je le rends pour que l'orchestrateur en décide.

## 6. Fichiers

- Dossier : `<scratchpad>/s2bis/rb1/g2/cc/`
  - `outils/` : `mutants_cc.py`, `xtask.sh` ;
  - `preuves/` : `mutants-cc.*`, `etat-*`, `dev-*`, `verdict-*`, `sim-bis-final.txt`, `s2-harness-final.txt`, `runner-final.txt`, `xtask-*`, `banc_lecteur_final.txt` ;
  - empreintes : `SHA256SUMS-contre-controle` (25 lignes).
- Lanceurs réutilisés, inchangés : `…/rb1/g2/outils/job.py`, `campagne_g2.py`, `banc_lecteur.py`.
- Nettoyage : copies, états, témoin et cible cargo supprimés ; le dossier fait 488 Ko.
- Dépôt : aucune opération git en écriture, `git status` vide.

