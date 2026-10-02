# Journal G1 — partie 3 de S2, étape S (niveau près de la garde)

- **Gate 0 (R-1)** : modèle résolu **`claude-opus-5-5`** (identifiant exact déclaré par le harnais dans le contexte de la session du worker), effort max ; worker G1 de l'étape S, contexte frais.
- **Mandat** : brief de l'orchestrateur de la session cloud (partie 3 de S2, étape S), branche `partie-3-paquet`, HEAD `3414e0f` (`3414e0f57cda743efc3e817c6eec16a571542e95`). Aucun commit, aucune opération git en écriture (R-19, R-20). Git en lecture seule : `rev-parse`, `status --short`, `diff --quiet`, `diff --stat`, `log`, `show HEAD:<chemin>`, `cat-file -t`, et `archive` vers le dossier de travail hors dépôt.
- **Rattachement (G0)** : `docs/adr-0028/G0-partie-3.md`, section « S » (sha256 `226d0099f31bad5c2821ed2aae3a61ab84535010d8a5c1e02e3ea5a4e340be7e`, lu à 14:49Z) ; `docs/adr-0028/ANNEXE-B-items.md` l.305, item SHOGEN-CRITERE-GARDE-NIVEAU-1 ; ADR-0028 §1 bis.1 pts 2, 3, 5, 7 et 11 ; G0 de SIM-NIVEAU (`docs/adr-0028/G0-lot-SIM-NIVEAU.md`, sha256 `1da137e6…5269`) et son journal G1 (`docs/G1-lot-SIM-NIVEAU.md`, sha256 `f7807398…f049`).
- **Périmètre d'écriture** : fichiers neufs de `scripts/sim/` ; sortie neuve et `SHA256SUMS` de `docs/adr-0028/sim-niveau/` ; ce journal. Travail hors dépôt : `$TMPDIR/etape-S/`, avec `TMPDIR=/tmp/claude-0/-home-user-shogen/7ba84933-ba6d-5813-9ef4-ca3ac4febd16/scratchpad` et `PYTHONDONTWRITEBYTECODE=1` pour toutes les commandes. Chemins réservés à l'autre worker (`s2-harness/tools/`, `s2-harness/shogen_s2/`, `scripts/sceau/`) : non touchés ; r1 n'est lu qu'au commit HEAD (`git show`, `git archive`), jamais dans l'arbre de travail.

## 0. Attestation d'exposition (forme de l'annexe D.3)

**Je n'ai vu ni z, ni K, ni P̂_more, ni φ des journaux de campagne, et je n'en ai calculé aucun. Je n'ai lu aucun taux d'écart ni de panne d'une source de la campagne. Je n'ai ouvert aucune donnée de campagne ni aucun journal scellé ; aucune statistique S2 n'a été calculée.** Les z, K, P̂_more et taux de ce journal portent sur des données synthétiques seules.

- **Non ouverts** : toutes les pièces de l'annexe D.2 (n° 1 à 11), dont les deux qui sont au dépôt (n° 5 et n° 6 : aucune ligne de l'une ni de l'autre), exclues de toutes mes recherches (`grep` restreints à des fichiers nommés hors D.2) ; aucun journal scellé ni copie ; `JOURNAL.md` non ouvert ; aucune transcription de session. Dans mon export de HEAD (`git archive 3414e0f`, dossier de travail), les fichiers de ces deux pièces ont été supprimés sans ouverture (`rm`) avant toute exécution. Les chemins de D.2 ne sont pas recopiés ici, pour ne pas lever de faux positif au contrôle FM-1.1 par motifs (précédent : journal G1 de SIM-NIVEAU, §8) ; ils figurent dans le rapport du worker. Le dossier de travail partagé (`scratchpad`) porte des fichiers d'autres agents, dont une copie de `JOURNAL.md` : non ouverts, seul `etape-S/` est lu et écrit.
- **Pièces lues** : au § Provenance (§8), avec leur niveau.
- **Exposé à** (classe M, constantes de conception, résultats synthétiques ; aucun taux par source, aucune statistique de résultat) : les comptes opérationnels que portent l'annexe D.1 (n° 6 à 9 : comptes de Pyth, diagnostics DNS du harnais, n = 35 982 ; 2 618 ; 17 314 ; 9 261), l'ADR §1 bis.2 (ordres de grandeur n ≈ 10⁴ et 2,5·10⁴ ; bornes calendaires des strates stress des J14, 5 760 et 2 880) et le §0 du G0 de SIM-NIVEAU (mêmes comptes, pertes de fenêtres, `resolve_failed`, `clock_check`) ; les résultats synthétiques de SIM-NIVEAU (journal G1 de SIM-NIVEAU, §4 et §6) ; les noms des pièces de D.2 (texte de D.2) ; le nom d'une source dans D.3 (a), valeurs masquées.
- Aucune de ces valeurs n'entre dans les paramètres de l'étape, sauf l'ordre de grandeur n ≈ 2,5·10⁴ que porte l'ADR §1 bis.2 et qui est le n de SIM-NIVEAU (§1.2).

## 1. Pré-enregistrement, écrit avant toute exécution (2026-10-02, 14:50Z, `date -u`)

Aucun code de l'étape n'existe à cette heure ; aucune simulation n'a été lancée. Seul a tourné le calcul de conception `calc_cas.py` (§1.3), qui ne simule rien. Ni les cas, ni R (par sa règle, §1.5), ni la graine, ni les définitions des taux, ni les classes de garde, ni la règle de lecture ne changent après la lecture d'une sortie. Une exécution à paramètres changés serait une déviation déclarée, ses sorties conservées avec leurs sha256.

### 1.1 Modèle nul et code de calcul : ceux de SIM-NIVEAU, inchangés

- Chaque réplication est `sim_niveau_calc.replication(p, L, n, r)` (sha256 `815ffd6d98603929ead4d3f4b6ee520a82f3e1340e4b8a728b4512e53e8eacbf`, blob `981654cd…` à HEAD, identique au gel 2 de SIM-NIVEAU), appelée sans modification ni substitution : 11 flux simulés, mutuellement indépendants par construction, chacun chaîne de Markov stationnaire à deux états de taux marginal p et de run moyen L (L = 1 : tirages indépendants) ; grille complète, une strate ; I_t = 1{m_t ≥ 2}, K ; plug-in p̂_i = e_i/n et P̂_more (réplique de r1 à `f5b8269`) ; garde n·P̂(1 − P̂) ≥ 10 ; z_s ; σ̂²_bloc (ℓ = 240) en deux formes entières ; z_bloc publiée si σ̂² > 0 et n ≥ 30·ℓ = 7 200 ; valeur de la règle (§1 bis.1 pt 5) ; drapeaux des oracles (2) et (2b).
- Agrégation de chaque cas par `sim_niveau.agreger` (sha256 `4fe7ea29248744dac59a3cebad665ab1977e8fa602f96b233b28d80519ffff88`), inchangée : comptes, taux z, z_bloc et règle avec erreur-type, diagnostics, oracles (2), (2b) et (5), empreinte des enregistrements. Aucune ligne de la règle n'est recopiée dans le code neuf.
- **Écarts déclarés au cadre de SIM-NIVEAU** :
  - (E-a) p varie par cas (§1.3) au lieu de p = 0,02 : c'est l'objet. Le critère de domaine du G0 de SIM-NIVEAU (§3 : garde tenue et σ̂² > 0 dans toutes les réplications du pilote) est levé à dessein : près de la garde, les fractions « garde non tenue » et « σ̂² = 0 » font partie de ce qui est mesuré ; elles sont imprimées par cas ;
  - (E-b) n ∈ {7 200 ; 25 000} au lieu de {10⁴ ; 2,5·10⁴} (§1.3) ;
  - (E-c) grille (n, g) complète pour L = 1, réduite à ses quatre coins pour L ∈ {5, 20, 60} (§1.3) ;
  - (E-d) R par bloc de cas (§1.5) au lieu de 10⁵ ;
  - (E-e) taux ajoutés : conditionnels à la garde tenue, par classe de la garde imprimée, référence binomiale exacte (§1.6) ;
  - (E-f) la réplique de r1 dans `sim_niveau_calc` est celle de `f5b8269` ; r1 à HEAD calcule P̂₀, P̂₁ et P̂_more en rationnels exacts avec une seule division `Decimal` (SHOGEN-PMORE-RESIDU-1, commit `957525a`, docstring de `r1.poisson_binomial` lue à HEAD). Écart de valeur attendu de l'ordre du dernier chiffre à la précision 50 [inféré] ; il est mesuré, et la valeur de la règle comparée à `r1.regle_critere` à HEAD, par l'oracle S-b (§1.7).

### 1.2 Pourquoi ces n : la garde de blocs

- La règle ne peut rendre REJETTE que si z_bloc est publiée, donc à n ≥ 7 200 (pt 3). Sous 7 200, z_bloc n'est jamais publiée : une strate rend NON ÉVALUABLE (rejet non qualifiable) exactement quand la garde est tenue et z_s ≥ 2,33, et jamais REJETTE. La distribution de la règle sous la garde de blocs se déduit donc du taux r_z (§1.6) sans simulation propre : REJETTE, discordance et rejet non qualifiable y fusionnent en rejet non qualifiable [inféré : la loi de z_s ne dépend pas de la garde de blocs]. Aucun cas n'est pris sous 7 200.
- **n = 7 200** (= 30·ℓ) : plus petit n où la règle peut rejeter ; à g fixé, le plus grand p ; σ̂²_bloc le plus bruité (30 blocs ; `cv_theorique` = √(4ℓ/(3n)) = 0,211 dans `r1.bloc_strate` à HEAD [lu], dérivation que sa docstring attribue à l'advisor-defi [2nd]).
- **n = 25 000** : ordre de grandeur de la plus grande strate du J28 et plus grand n de SIM-NIVEAU (ADR-0028 §1 bis.2 : n ≈ 2,5·10⁴ et 10⁴, comptes calendaires de classe M, annexe D.1 n° 9, repris tels que l'ADR les porte) ; à g fixé, le plus petit p, donc le plug-in le moins conservateur (§1.3, colonne f) : c'est le cas le moins favorable à z_s.

### 1.3 Cas, fixés à l'aveugle (aucune donnée de campagne)

- **Cible g = n·P_more(p)(1 − P_more(p)) ∈ {10 ; 15 ; 20 ; 30}** : 10 est le seuil de la garde §5.4 (pt 2) ; 30 la borne haute que fixe l'item ; 15 et 20 resserrent la grille vers 10, où l'asymétrie de la loi de K est la plus forte (elle décroît comme 1/√g [inféré : loi de K proche d'une loi de Poisson de moyenne ≈ g à P_more ≤ 4,2·10⁻³]).
- **p** : pour chaque (n, g), P* = plus petite racine de n·P(1 − P) = g, p* tel que P_more(p*) = P* (N = 11, bissection), puis **p = p* arrondi vers le haut à 4 chiffres significatifs** (donc g théorique ≥ g cible, à moins de 0,08 % près). Calcul : `calc_cas.py` (sha256 `c627d64f0ec3b6e7a9836b338638d6fc5cffc711efda2fdeee3111ce31a13175`), sortie `calc_cas.out.txt` (sha256 `ad95c4e3854676bf9552957c91326403285c1c3280c1de4fc9b105439cb1147b`), `Decimal` à 60 chiffres et `Fraction`, aucune simulation.
- **Facteur f** : variance du numérateur K − n·P̂_more rapportée à n·P_more(1 − P_more), au premier ordre, fenêtres iid (dérivation du worker [inféré] : f = [P(1−P) − 22c·Cov(I, D₁) + 11c²·p(1−p)]/(P(1−P)), c = ∂P_more/∂p_i = 10p(1−p)⁹, Cov(I, D₁) = p(1 − (1−p)¹⁰) − p·P). Contrôle : f(0,02) = 0,6867, valeur de la CRITIQUE v2 §4.2 que cite le G0 de SIM-NIVEAU §3 [2nd], recalculée.

| n | g cible | p retenu | P_more(p) | g théorique | runs d'écart attendus par flux, L = 1 / 5 / 20 / 60 | f |
|---|---|---|---|---|---|---|
| 7 200 | 10 | 0.005107 | 0,001391191 | 10,0026 | 36,58 / 7,36 / 1,84 / 0,62 | 0,9043 |
| 7 200 | 15 | 0.006279 | 0,002088249 | 15,0040 | 44,92 / 9,05 / 2,27 / 0,76 | 0,8841 |
| 7 200 | 20 | 0.007274 | 0,002785835 | 20,0021 | 51,99 / 10,48 / 2,63 / 0,88 | 0,8673 |
| 7 200 | 30 | 0.00896 | 0,004184387 | 30,0015 | 63,93 / 12,91 / 3,23 / 1,08 | 0,8400 |
| 25 000 | 10 | 0.00272 | 0,000400325 | 10,0041 | 67,82 / 13,60 / 3,40 / 1,14 | 0,9475 |
| 25 000 | 15 | 0.003338 | 0,000600672 | 15,0078 | 83,17 / 16,69 / 4,18 / 1,39 | 0,9360 |
| 25 000 | 20 | 0.00386 | 0,000800717 | 20,0019 | 96,13 / 19,30 / 4,83 / 1,61 | 0,9265 |
| 25 000 | 30 | 0.004741 | 0,001201569 | 30,0031 | 117,96 / 23,71 / 5,93 / 1,98 | 0,9108 |

- **Liste des 20 cas, dans l'ordre d'exécution** (L croissant, puis n, puis g) :
  - **bloc I, L = 1** (8 cas) : les huit lignes de la table ;
  - **bloc D, L ∈ {5, 20, 60}** (12 cas) : pour chaque L, les quatre coins (7 200 ; 0.005107), (7 200 ; 0.00896), (25 000 ; 0.00272), (25 000 ; 0.004741).
- **Motif du partage** : la limite « approximation normale à la garde » (pt 11) porte d'abord sur L = 1, où z_s est proche de son niveau nominal et où l'écart à 0,01 se joue à quelques millièmes : grille fine et R le plus grand. Sous dépendance, z_s seul est déjà déclaré ne pas tenir son niveau (pt 7 ; SIM-NIVEAU, R = 10⁵ : 8,2 à 33,7 % à p = 0,02) et la règle le tient largement loin de la garde (SIM-NIVEAU : au plus 7·10⁻⁵) ; les quatre coins bornent la région près de la garde. À L = 60, moins de deux runs d'écart par flux sont attendus dans tous les coins : c'est la structure de dépendance de SIM-NIVEAU au voisinage de la garde, gardée telle quelle, et l'état dégénéré du domaine y est une partie du résultat.
- **Même structure de dépendance que SIM-NIVEAU** : mêmes L ; mêmes formules (a, b) et même état initial (`sim_niveau_calc.chaine`, `generer`) ; ρ^ℓ imprimé par cas par `agreger`.

### 1.4 Graine

- **GRAINE = 20260930 et dérivation de SIM-NIVEAU, inchangées** : `sim_niveau_calc.graine(p, L, n, r)` = entier big-endian des 8 premiers octets de sha256 de `SHOGEN-SIM-NIVEAU-1|20260930|p={p!r}|L={L}|n={n}|r={r}`, puis `random.Random`. Chaîne de r = 0 du premier cas : `SHOGEN-SIM-NIVEAU-1|20260930|p=0.005107|L=1|n=7200|r=0`.
- **Flux distincts** de ceux de SIM-NIVEAU (p = 0,02) et de la grille de l'item SHOGEN-SIM-NIVEAU-P-1 (p ∈ {0,0043196 ; 0,005 ; 0,01 ; 0,05}, G0 de SIM-NIVEAU §10) : aucun p de la table n'y figure, et la chaîne porte p.
- **Motif de ne pas poser de graine neuve** : (i) « même discipline de graine » (G0 de la partie 3) prise à la lettre ; (ii) la chaîne est codée dans `sim_niveau_calc`, que l'étape ne modifie ni ne substitue ; (iii) l'oracle existant (`sim_niveau_oracle_r1.serie`) régénère les mêmes flux sans `sim_niveau_calc`, ce qui rend l'oracle S-b possible sans code de génération neuf. Aucune autre graine n'est essayée.

### 1.5 Nombre de réplications R : règle fixée avant la mesure du temps

- **Sonde de temps** (pas une exécution de l'étape) : 4 processus en parallèle appellent `sim_niveau_calc.replication` sur les cas **déjà publiés** de SIM-NIVEAU (p = 0,02, L = 1) : chacun 25 réplications à n = 10⁴ (r = 25k à 25k + 24, k = 0..3), puis 10 à n = 2,5·10⁴ (r = 10k à 10k + 9). Sortie : durées seules, aucun K, z ni valeur. t(10⁴) et t(2,5·10⁴) = moyennes, sur les 4 processus, du temps par réplication ; t(n) affine par ces deux points. Charge de la machine relevée avant et après (`/proc/loadavg`).
- **Durée prédite** d'une exécution complète à 4 processus : T = 1,15 × Σ_cas R_cas·t(n_cas)/4.
- **R_I** (bloc I) = la plus grande valeur de {100 000 ; 80 000 ; 60 000 ; 50 000 ; 40 000 ; 30 000 ; 25 000 ; 20 000 ; 15 000 ; 10 000} telle que T ≤ 40 min, avec **R_D = R_I/5** (bloc D) ; si aucune, R_I = 10 000 (déclaré).
- **Erreur-type de Monte-Carlo attendue** : SE = √(r(1 − r)/R) ; à r = 0,01 : 7,0·10⁻⁴ à R = 2·10⁴, 5,7·10⁻⁴ à 3·10⁴, 5,0·10⁻⁴ à 4·10⁴, 3,1·10⁻⁴ à 10⁵ ; à x = 0, borne unilatérale à 95 % 1 − 0,05^(1/R) ≈ 3/R. Les valeurs retenues sont écrites au §2, avec l'heure.

### 1.6 Définitions des taux (tous par cas, comptes entiers)

- **z_s seul** : r_z = #{garde tenue ∧ z_s ≥ 2,33}/R (définition de SIM-NIVEAU ; c'est aussi le taux de rejet à tort du repli §1 bis.3) ; r_z|t = #{garde tenue ∧ z_s ≥ 2,33}/#{garde tenue} (niveau du test quand il est fait).
- **Règle** : distribution des cinq valeurs à sous-cause (REJETTE ; NE REJETTE PAS (z < 2,33) ; NE REJETTE PAS (discordance) ; NON ÉVALUABLE (garde §5.4) ; NON ÉVALUABLE (rejet non qualifiable)) et des trois valeurs du pt 5, x/R chacune ; **taux de REJETTE à tort** r_règle = #{REJETTE}/R (sous le modèle nul, tout REJETTE est à tort) ; r_règle|t = #{REJETTE}/#{garde tenue}. r_bloc = #{z_bloc publiée ∧ z_bloc ≥ 2,33}/R, imprimé comme dans SIM-NIVEAU.
- **Classes de la garde imprimée** ĝ = n·P̂(1 − P̂) : [10 ; 12,5), [12,5 ; 15), [15 ; 20), [20 ; 30), [30 ; +∞) (sous 10 : garde non tenue). Par classe : effectif m_c, et, sur m_c, les taux de z_s ≥ 2,33, de REJETTE, de discordance et de rejet non qualifiable. Descriptif.
- **Référence binomiale exacte, P connu** (hors règle, sans plug-in ni garde aléatoire) : k* = plus petit entier k tel que (k − nP)/√(nP(1 − P)) ≥ 2,33, P = P_more(p) exact ; niveau de référence P(K ≥ k*) pour K ~ Bin(n, P), en `Decimal` à la précision 50. C'est le niveau exact de z à L = 1 si P était connu : il sépare l'effet de l'asymétrie (approximation normale) de celui du plug-in. Imprimé pour tous les cas, étiqueté « fenêtres iid » (sans objet sous dépendance).
- **Erreurs-types** : SE = √(r(1 − r)/D), D le dénominateur du taux ; à x = 0, borne 1 − 0,05^(1/D).

### 1.7 Oracles et bit-identité

- **Internes, à l'exécution (fail-closed : sortie ≠ 0 et aucun fichier)** : (2) n²γ̂₀ = n·K(n − K) et (2b) N_lag = N_bloc à chaque réplication ; (5) générateur contre la théorie (K/n contre P_more(p), p̄ contre p, run moyen contre L_n), |écart| ≤ 5 SE : ceux d'`agreger`, inchangés.
- **Oracle (4) existant, rejoué inchangé** : `scripts/sim/sim_niveau_oracle4.py` contre `r1.block_long_run_variance` d'un export `git archive 3414e0f s2-harness`.
- **Oracle S-b (neuf)**, contre r1 à HEAD (même export) : pour chaque cas, les réplications r = 0..49, **toutes** les REJETTE, les 50 premières discordances et tous les rejets non qualifiables de l'exécution A (indices écrits dans le JSON) ; série régénérée par `sim_niveau_oracle_r1.serie` (sans `sim_niveau_calc`) ; égalité exacte de e, runs et K ; égalité exacte du numérateur N contre `r1.block_long_run_variance` ; égalité de la valeur et du cas contre `r1.regle_critere` (entrée : z de `r1.z_score` si `r1.insufficient_history` est faux, bloc de `r1.bloc_strate`, garde de `r1.gate_value`) ; P̂_more, garde, z et z_bloc égaux à 10⁻⁴⁰ près en relatif (écart maximal imprimé).
- **Rejeu complémentaire** (contrôle d'environnement, déclaré) : `scripts/sim/sim_niveau_oracle_r1.py` contre un export de `f5b8269`, avec `--json` sur la sortie A de l'étape et sur `sim_niveau.json` (invariants (4b) (ii)).
- **Bit-identité** : exécution A complète (4 processus) ; exécutions B (4 processus) et C (1 processus) à R/20 dans chaque cas : JSON et texte de B et de C identiques à l'octet (deux exécutions, et invariance au nombre de processus) ; l'empreinte des R/20 premiers enregistrements de chaque cas de A (« empreinte_prefixe ») égale l'empreinte du même cas de B. Si la durée murale de A est ≤ 30 min, une exécution complète A′ (4 processus) est faite en plus et comparée à l'octet à A.

### 1.8 Règle de lecture et conséquence pré-déclarée

- Conséquence (G0 de la partie 3, section S ; §1 bis.1 pt 7, même principe) : la sortie ne modifie ni ℓ, ni le seuil, ni la règle ; elle est imprimée au paquet avec ses erreurs-types ; un niveau mesuré au-dessus de 0,01 devient une limite écrite au paquet, jamais une révision. Aucune modification de la règle n'est proposée ici.
- Lecture : pour r_z, r_z|t, r_règle et r_règle|t de chaque cas, la sortie imprime (r − 0,01)/SE. **Un taux de cas dont l'estimation ponctuelle dépasse 0,01 est un « niveau mesuré au-dessus de 0,01 »** et devient une limite (§ Limites) ; il est dit « au-dessus à deux erreurs-types » si r − 2·SE > 0,01. Les taux par classe de garde sont descriptifs : une classe au-dessus de 0,01 à deux erreurs-types est rapportée aux limites avec la mention « descriptif ».
- α nominal = 1 − Φ(2,33) imprimé pour comparaison, comme dans SIM-NIVEAU.

## 2. R fixé par la règle du §1.5 (2026-10-02, 14:52Z, `date -u`)

- **Sonde** : `sonde_temps.py` (sha256 `2aed34d019e8ae16e376f26739bec78abf7ab69fab2ad34f1aeab316e11d1e67`), exécutée de 14:52:20Z à 14:52:21Z, sortie `sonde_temps.out.txt` (sha256 `c1afd7c2bb2894f55d96dea5cf351980c7d69307b3696b631f5e457e10f7a949`), durées seules. Charge relevée : `/proc/loadavg` = 16,35 avant et après (machine partagée : quatre processus d'OCR d'un autre travail et la suite de l'autre worker y tournaient à 14:47Z, `ps`). Moyennes : t(10⁴) = 0,0166 s et t(2,5·10⁴) = 0,0377 s par réplication ; t(n) affine : t(7 200) = 0,01266 s.
- **Application de la règle** : T(R_I) = 1,15 × [R_I·(4·t(7 200) + 4·t(25 000)) + (R_I/5)·(6·t(7 200) + 6·t(25 000))]/4 ; T(40 000) = 50,2 min > 40 ; **T(30 000) = 37,6 min ≤ 40**. D'où **R_I = 30 000** (bloc I, L = 1) et **R_D = 6 000** (bloc D), soit 360 000 réplications par exécution complète.
- **Erreurs-types de Monte-Carlo attendues** : à r = 0,01, SE = 5,7·10⁻⁴ (R = 30 000) et 1,3·10⁻³ (R = 6 000) ; à x = 0, borne unilatérale à 95 % 1,0·10⁻⁴ et 5,0·10⁻⁴. Pour les taux conditionnels, D = #{garde tenue} ou m_c, plus petit, donc SE plus grande (imprimée).
- **Bit-identité** : B et C à R/20, soit 1 500 (bloc I) et 300 (bloc D) réplications par cas ; empreinte_prefixe de A sur les 1 500 et 300 premiers enregistrements.
- Les paramètres du §1 et ceux-ci sont figés à cette heure ; le code de l'étape s'écrit ensuite (§3).

## 3. Code : deux sous-lots, tests d'abord (heures `date -u` ou `stat`)

| fichier neuf | sous-lot | lignes (`wc -l`) | rôle |
|---|---|---|---|
| `scripts/sim/sim_garde_niveau_oracle_r1.py` | **S-b**, écrit le premier (avant 15:00Z) | 183 | oracle de l'étape : (T0) table des cas contre la table du §1.3 et du §2, recopiée dans l'oracle comme référence indépendante du code ; (T1) invariants de la sortie, plus les invariants (4b) (ii) existants de `sim_niveau_oracle_r1.invariants` ; (T2) référence binomiale : k* exact en `Fraction`, niveau contre `r1.binomial_tail_ge` ; (T3) réplications régénérées par `sim_niveau_oracle_r1.serie` et recalculées par r1 à `3414e0f` (`block_long_run_variance`, `poisson_binomial`, `gate_value`, `insufficient_history`, `z_score`, `bloc_strate`, `regle_critere`) |
| `scripts/sim/sim_garde_niveau.py` | **S-a** (15:00Z) | 199 | cas et R du §1 et du §2 ; chaque réplication par `sim_niveau_calc.tache` (donc `replication`), chaque cas par `sim_niveau.agreger` ; ajouts du §1.6 et du §1.7 ; sorties `garde_niveau.json`, `garde_niveau.txt`, `garde_niveau.log.txt` (fail-closed, mode `xb`) |

- **Réutilisation, sans duplication de la règle** : la valeur de la règle de chaque réplication est le champ `valeur` de `sim_niveau_calc.replication` ; S-a ne compare jamais z ni z_bloc pour classer une réplication. Les deux seuls usages de 2,33 dans S-a sont un compte (z ≥ 2,33 par classe de garde, comme `agreger`) et la recherche de k* de la référence, par `sim_niveau_calc.z_score`. Fonctions reprises : `sim_niveau_calc` (`tache`, `replication`, `z_score`, constantes), `sim_niveau` (`agreger`, `taux`, `sha256_fichier`, `VALEURS`, `N_FLUX`), `sim_niveau_oracle_r1` (`serie`, `invariants`). Aucun de ces fichiers n'est modifié (sha256 du §1.1 inchangés, `git diff --quiet HEAD -- scripts/sim/sim_niveau*.py` : rc 0).
- **R-25** : 199 + 183 = 382 lignes, en deux sous-lots de moins de 200 lignes chacun (précédent : coupe a1, a2, b de SIM-NIVEAU). Lignes datées de l'annexe A : acte de l'orchestrateur.
- **Bibliothèque standard seule** (Python 3.13.14, `/usr/bin/python3.13`) : `argparse`, `contextlib`, `hashlib`, `json`, `math`, `multiprocessing`, `os`, `platform`, `sys`, `time`, `collections`, `decimal`, `fractions`, `statistics`. Aucune dépendance nouvelle (R-8 sans objet). Fins de ligne LF (`grep -c $'\r'` = 0 sur les deux fichiers) ; aucun `TODO` ni `FIXME` (`grep`).
- **Chronologie du code** :
  - S-b écrit avant S-a (création de S-a : 15:00:02Z, `stat`) ; 15:00:12Z, essai e1 de S-a (diviseur 300, 4 processus) ; 15:00:42Z, S-b passe sur e1 ;
  - 15:01:56Z, S-b resserré (trouvaille du worker) : T3 n'exigeait pas que chaque indice publié soit de la valeur annoncée ; ajout du contrôle ;
  - 15:02Z-15:03Z, S-a publie ĝ minimal et maximal par classe et S-b vérifie que chaque classe reste dans ses bornes : les sommes de T1 ne voient pas une erreur de borne de classe (trouvaille du worker) ;
  - 15:03:44Z, essai e2 (gel de S-a, sha256 `51902b0db46e5cf680d4fec1d067455a6b2f6c5af6cefbaa4afb28ba2c6d707c`) ; S-b passe ;
  - 15:07Z, S-b resserré : `taux_ok` compare aussi la valeur de la borne à x = 0 (le banc v1 montrait que M4 ne mourait que par un compte non nul) ;
  - 15:10:32Z, **note d'intégration de l'orchestrateur** (lot P3, SHOGEN-CONTEXTE-MUTABLE-1 : `r1.CONTEXTE_DECIMAL` devient la fabrique `r1.contexte_decimal()`) : S-b prend le contexte par une fonction `contexte()` qui appelle `r1.contexte_decimal()` si elle existe, `r1.CONTEXTE_DECIMAL` sinon ; aucun alias n'est ajouté à `r1.py`. **r1 est chargé depuis un export figé de `3414e0f`** (`git archive`, blob `ce1da3dfc19e380d1a0ed33e2fec9ff410109bee`, égal à `git rev-parse 3414e0f:s2-harness/shogen_s2/r1.py`), jamais depuis l'arbre de travail : les sorties déjà produites (essais e1 et e2, bancs v1 et v2) l'ont été contre cet export, qui porte `CONTEXTE_DECIMAL` ; les valeurs du contexte sont les mêmes dans les deux formes ; elles ne sont pas affectées ;
  - 15:14:24Z, exécution A lancée (S-a au gel `51902b0d…`).

## 4. Tests : oracle S-b, essais et bancs de mutants (une mutation par contrôle)

- **Essais déclarés** (diviseur 300 : R = 100 au bloc I, 20 au bloc D ; 4 processus ; tous postérieurs au §1 et au §2) : e1 (15:00:12Z, S-a avant les bornes de classe) et e2 (15:03:44Z, gel de S-a). Sur e1 puis e2, S-b sort 0 : T0 20 cas ; T1 240 puis 260 invariants (12 puis 13 par cas) et 160 invariants (4b) (ii) ; T2 écart relatif maximal 7,3·10⁻⁴⁵ ; T3 645 réplications, valeur égale à `r1.regle_critere` dans les 645, P̂_more identique au dernier chiffre dans 95, écarts relatifs maximaux 1,1·10⁻⁴⁶ (P̂_more, garde) et 4,1·10⁻⁴⁴ (z, z_bloc). Ces essais ne servent qu'au fonctionnement ; aucun paramètre n'en dépend (tous fixés au §1 et au §2).
- **Échec montré** : chaque contrôle de S-b est montré en échec sur un mutant (bancs ci-dessous), puis en succès sur le code non muté (témoin).
- **Banc v1** (`mutants/banc.py`, sha256 `58ad7b0f…1685`), 15:05:37Z, interrompu à 15:06:57Z après six entrées (sortie conservée : `mutants/essai-1-interrompu/`) : M4 n'y mourait que par un compte non nul ; `taux_ok` est resserré (§3), le banc relancé.
- **Banc v2** (même pilote), 15:07:30Z à 15:14:17Z (`mutants/sortie-banc.txt`, sha256 `1f4bf3c2…7be1` ; `resultats.json` `b00c9239…140f`) : témoin conforme ; M1 à M8, M11 et M12 tués par le contrôle visé ; M9 (indices décalés dans les trois listes) et M10 (garde à 9 dans `sim_niveau_calc`) tués, mais par T1 et non par T3 : la cible T3 n'était pas atteinte. D'où le banc v3, aux mutants ciblés (§4 suite).
- **Banc v3** (`mutants/banc_v3.py`, sha256 `88b976c2078b77261fcf340b6011af735888e3e56f33eef776b665486b0ab84b`), sur S-a au gel `51902b0d…` et S-b au gel `7fbc82d35a533164675792c0b97c3f948cf985cfd407e84af05eab3e8725628d` (183 lignes), 15:19:24Z à 15:30:13Z, sortie `mutants/sortie-banc-v3.txt` (sha256 `f8b8bdfcd5ba4eb374d41963585253b02952b7ee3b2ed21b1f1dc07b957ac05a`), `mutants/v3/resultats.json` (`25376a0b4de8dd3eb18d9f174f65dde6ddf85527f2ecc33176a5735c17aa1874`). Une substitution textuelle par mutant, occurrence unique exigée, dans une copie (jamais dans les fichiers du dépôt) ; S-a de la copie au diviseur 300, puis S-b de la copie ; critère : S-a sort 0, S-b sort ≠ 0 avec le message du contrôle visé. **15 mutants tués par le contrôle visé sur 15 ; deux témoins conformes.**

| # | côté muté | mutation | contrôle visé | message de sortie (début) |
|---|---|---|---|---|
| témoin | — | aucune | tous passent | S-a 0, S-b 0 |
| M1 | S-a | p d'un cas : 0.00386 → 0.00387 | T0 table | `ECHEC (T0) : cas de la sortie différents de la table du journal` |
| M2 | S-a | g théorique avec (1 + P) | T0 g | `ECHEC (T0) : g théorique 10.00264…` |
| M3 | S-a | borne de classe ĝ < b → ĝ < b − 1 | T1 bornes de classe | `ECHEC (T1) : ĝ de chaque classe dans ses bornes` |
| M4 | S-a | taux conditionnel de z sur R au lieu de #{garde tenue} | T1 conditionnels | `ECHEC (T1) : conditionnels` |
| M5 | S-a | NE REJETTE PAS sans les discordances | T1 trois valeurs | `ECHEC (T1) : trois valeurs du pt 5` |
| M6 | S-a | seuil de lecture 0,01 → 0,0099 | T1 lecture | `ECHEC (T1) : lecture` |
| M7 | S-a | une seule discordance retenue | T1 indices | `ECHEC (T1) : indices` |
| M8 | S-a | référence : k* + 1 termes | T2 | `ECHEC (T2) : k* 18 contre 18, ou niveau` |
| M9 | S-a | indice des REJETTE décalé de 1 (modulo R) | T3 valeur annoncée | `ECHEC (T3) : indice de la sortie de valeur REJETTE, réplication de valeur NE REJETTE PAS (z < 2,33)` |
| M10 | `sim_niveau_calc` | garde §5.4 à 9 au lieu de 10 | T1 bornes de classe | `ECHEC (T1) : ĝ de chaque classe dans ses bornes` |
| M11 | `sim_niveau_calc` | p̂_i = e_i/(n − 1) | T3 P̂_more | `ECHEC (T3) : P_more, r1 0.0014594990…, script 0.0014598981…` |
| M12 | S-a | empreinte du préfixe sur 1 ≤ r ≤ R/20 | comparaison A contre B | 0 cas sur 20 à empreinte égale (témoin : 20 sur 20) |
| M13 | r1 (copie de l'export) | `regle_critere` : REJETTE ⇔ z_bloc ≥ 3,33 | T3 valeur | `ECHEC (T3) : valeur REJETTE contre r1.regle_critere discordance` |
| M14 | r1 (copie de l'export) | poids de Bartlett 2(ℓ − k + 1) | T3 N | `ECHEC (T3) : N contre r1.block_long_run_variance` |
| M15 | `sim_niveau_oracle_r1` (copie) | série à L = 1 tirée comme une chaîne à L = 5 | T3 génération | `ECHEC (T3) : e, runs ou K` |

- **Lecture du banc** : M13 à M15 mutent la référence (r1 ou le générateur indépendant), pas le code sous test : ils montrent que chaque comparaison de T3 est vivante. M10 est tué par T1 (classes), avant T3 : une garde décalée dans `sim_niveau_calc` est donc vue deux fois. Mutants non inscrits, équivalents en probabilité ou par construction : « ≥ 2,33 » contre « > 2,33 » (égalité de mesure nulle, comme au G0 de SIM-NIVEAU, mutant 10) ; borne de classe ĝ < b contre ĝ ≤ b (égalité de ĝ à 12,5, 15, 20 ou 30 de mesure nulle [inféré]).

## 5. Exécutions et bit-identité

Toutes depuis `/home/user/shogen` : `python3.13 -B scripts/sim/sim_garde_niveau.py --sortie <dossier> …`, S-a au gel `51902b0d…`, `sim_niveau.py` `4fe7ea29…` et `sim_niveau_calc.py` `815ffd6d…` (sha256 relus par le script et écrits dans chaque JSON). Python 3.13.14, Linux 6.18.44, glibc 2.39, 4 processeurs (`garde_niveau.log.txt`).

| exécution | paramètres | début et fin (`.log.txt`) | `garde_niveau.json` | `garde_niveau.txt` | `garde_niveau.log.txt` |
|---|---|---|---|---|---|
| **A** | `--processus 4` ; R0 | 15:14:24Z – 15:41:52Z (27 min 28 s) | `f421c41944c15d329400fffe700b779ad286236acbad5cf3a6ebcdfd7c18981b` | `e1d79bebc0b3f9beaf814ba2fd86311978fd9d4b790b46d72ed00af90d1ef94a` | `e5321ebab02519481155c896ac06cc6828d4d836557b3c767fb0da605fdd5a2b` |
| **B** | `--processus 4 --diviseur 20` | 15:15:34Z – 15:18:45Z | `e105573a371bf4654901fe4e083c1a626935e9e0cc47362cce58f55c022143df` | `3b5a9104475fb051091b2c2db969cdc4ea0d8075c1ddfd7bca88de28a45b5aee` | `0c3e19472eb1f45c8f375192028261652d69ee73e7698ecc2536e7080699ae08` |
| **C** | `--processus 1 --diviseur 20` (sans Pool) | 15:15:34Z – 15:19:07Z | identique à B | identique à B | `dea17d876d7b4290077e22c943892207e09a46dcfd027705d87d9b8d89a179d6` |

- **A** : 312 000 réplications (8 × 30 000 + 12 × 6 000), 4 PID distincts dans chaque cas ; sortie 0. Durée 27 min 28 s, sous les 60 min ; la prédiction de la règle du §1.5 était 37,6 min.
- **B = C à l'octet** (`cmp`, JSON et texte) : deux exécutions identiques, l'une à 4 processus (4 PID), l'autre sans Pool (1 PID) : bit-identité et invariance au parallélisme.
- **Préfixes** : pour les 20 cas, l'empreinte des R/20 premiers enregistrements de A (1 500 ou 300) est égale à l'empreinte du même cas de B, et `prefixe_R` de A égale R de B (`controles_bit.py`, sha256 `4324dc78114e9b5dedd1870cc09bbcd3ab663c21483a695d8a053f7356a671a4` : « CONTROLES DE BIT-IDENTITE : OK »). Les 1 500 ou 300 premières réplications de chaque cas de A sont donc reproduites à l'octet par B et par C.
- **A′** : la durée murale de A (27 min 28 s) est ≤ 30 min ; la règle du §1.7 impose une exécution complète A′ (4 processus), lancée à 15:42:15Z, comparée à l'octet à A au §5 bis.
- **Concurrence déclarée** : pendant A tournaient aussi, sur la même machine, quatre processus d'OCR d'un autre travail, la suite de l'autre worker, et, de ce worker, B, C, le banc v3, le rejeu de l'oracle (4) et le rejeu de SIM-NIVEAU (§7). Les durées par cas de A en dépendent (104 à 377 s au bloc I) ; les octets de A n'en dépendent pas (graine par (p, L, n, r), agrégation dans l'ordre des r, aucune horloge dans le JSON ni le texte).

## 5 bis. A′ (règle du §1.7) et bilan de bit-identité

- **A′** : `--processus 4`, 15:42:15Z – 15:57:10Z (14 min 55 s, machine moins chargée), sortie 0. `garde_niveau.json` `f421c419…981b` et `garde_niveau.txt` `e1d79beb…f94a` : **identiques à l'octet à A** (`controles_bit.py run-A run-B run-C run-A2` : « A = A' » pour les deux fichiers, « CONTROLES DE BIT-IDENTITE : OK », sortie 0). Journal d'exécution `610297b02eebf823d4afee9132a5dc261d1cb76860e7111e5e13d286cafabcb9` (heures, hors bit-identité).
- **Bilan** : deux exécutions complètes identiques à l'octet (A, A′) ; deux exécutions à R/20 identiques à l'octet, à 4 processus et sans Pool (B, C) ; préfixes de A égaux à B dans les 20 cas.

## 6. Résultats (exécution A ; sous le modèle nul synthétique seul)

Format des cellules : x ; r (SE) [(r − 0,01)/SE] ; à x = 0, borne unilatérale à 95 %. α nominal = 1 − Φ(2,33) = 0,00990308. « Sachant garde tenue » : dénominateur #{garde tenue}. Référence : P(K ≥ k*) pour K ~ Bin(n, P_more(p)), P connu, fenêtres iid (hors règle). Table recalculée depuis les comptes du JSON par `table_resultats.py` (sha256 `28831887…bc75`), indépendamment de S-a pour SE et écarts.

### 6.1 Bloc I (L = 1, fenêtres iid ; R = 30 000)

| L | n | p | g cible (théo.) | R | garde non tenue | σ̂² = 0 | r_z | r_z sachant garde tenue | r_règle | r_règle sachant garde tenue | discordances | NON ÉV. garde ; non qual. | référence iid : k* ; niveau |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 7200 | 0,005107 | 10 (10,003) | 30000 | 15161 | 2 | 173 ; 0,00577 (0,00044) [-9,7] | 173 ; 0,01166 (0,00088) [+1,9] | 25 ; 0,00083 (0,00017) [-55,0] | 25 ; 0,00168 (0,00034) [-24,7] | 148 | 15161 ; 0 | 18 ; 0,01443 |
| 1 | 7200 | 0,006279 | 15 (15,004) | 30000 | 0 | 0 | 288 ; 0,00960 (0,00056) [-0,7] | 288 ; 0,00960 (0,00056) [-0,7] | 64 ; 0,00213 (0,00027) [-29,5] | 64 ; 0,00213 (0,00027) [-29,5] | 224 | 0 ; 0 | 25 ; 0,01138 |
| 1 | 7200 | 0,007274 | 20 (20,002) | 30000 | 0 | 0 | 263 ; 0,00877 (0,00054) [-2,3] | 263 ; 0,00877 (0,00054) [-2,3] | 77 ; 0,00257 (0,00029) [-25,4] | 77 ; 0,00257 (0,00029) [-25,4] | 186 | 0 ; 0 | 31 ; 0,01385 |
| 1 | 7200 | 0,00896 | 30 (30,002) | 30000 | 0 | 0 | 237 ; 0,00790 (0,00051) [-4,1] | 237 ; 0,00790 (0,00051) [-4,1] | 63 ; 0,00210 (0,00026) [-29,9] | 63 ; 0,00210 (0,00026) [-29,9] | 174 | 0 ; 0 | 43 ; 0,01558 |
| 1 | 25000 | 0,00272 | 10 (10,004) | 30000 | 15156 | 0 | 178 ; 0,00593 (0,00044) [-9,2] | 178 ; 0,01199 (0,00089) [+2,2] | 14 ; 0,00047 (0,00012) [-76,5] | 14 ; 0,00094 (0,00025) [-35,9] | 164 | 15156 ; 0 | 18 ; 0,01436 |
| 1 | 25000 | 0,003338 | 15 (15,008) | 30000 | 0 | 0 | 344 ; 0,01147 (0,00061) [+2,4] | 344 ; 0,01147 (0,00061) [+2,4] | 41 ; 0,00137 (0,00021) [-40,5] | 41 ; 0,00137 (0,00021) [-40,5] | 303 | 0 ; 0 | 25 ; 0,01128 |
| 1 | 25000 | 0,00386 | 20 (20,002) | 30000 | 0 | 0 | 364 ; 0,01213 (0,00063) [+3,4] | 364 ; 0,01213 (0,00063) [+3,4] | 68 ; 0,00227 (0,00027) [-28,2] | 68 ; 0,00227 (0,00027) [-28,2] | 296 | 0 ; 0 | 31 ; 0,01359 |
| 1 | 25000 | 0,004741 | 30 (30,003) | 30000 | 0 | 0 | 335 ; 0,01117 (0,00061) [+1,9] | 335 ; 0,01117 (0,00061) [+1,9] | 107 ; 0,00357 (0,00034) [-18,7] | 107 ; 0,00357 (0,00034) [-18,7] | 228 | 0 ; 0 | 43 ; 0,01505 |

### 6.2 Bloc D (L ∈ {5, 20, 60} ; R = 6 000)

| L | n | p | g cible (théo.) | R | garde non tenue | σ̂² = 0 | r_z | r_z sachant garde tenue | r_règle | r_règle sachant garde tenue | discordances | NON ÉV. garde ; non qual. | référence iid : k* ; niveau |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 | 7200 | 0,005107 | 10 (10,003) | 6000 | 3220 | 193 | 404 ; 0,06733 (0,00324) [+17,7] | 404 ; 0,14532 (0,00668) [+20,2] | 0 ; 0,00000 (0,00000) [borne 5,0e-04] | 0 ; 0,00000 (0,00000) [borne 1,1e-03] | 404 | 3220 ; 0 | 18 ; 0,01443 |
| 5 | 7200 | 0,00896 | 30 (30,002) | 6000 | 0 | 0 | 682 ; 0,11367 (0,00410) [+25,3] | 682 ; 0,11367 (0,00410) [+25,3] | 0 ; 0,00000 (0,00000) [borne 5,0e-04] | 0 ; 0,00000 (0,00000) [borne 5,0e-04] | 682 | 0 ; 0 | 43 ; 0,01558 |
| 5 | 25000 | 0,00272 | 10 (10,004) | 6000 | 3179 | 173 | 352 ; 0,05867 (0,00303) [+16,0] | 352 ; 0,12478 (0,00622) [+18,4] | 0 ; 0,00000 (0,00000) [borne 5,0e-04] | 0 ; 0,00000 (0,00000) [borne 1,1e-03] | 352 | 3179 ; 0 | 18 ; 0,01436 |
| 5 | 25000 | 0,004741 | 30 (30,003) | 6000 | 0 | 0 | 812 ; 0,13533 (0,00442) [+28,4] | 812 ; 0,13533 (0,00442) [+28,4] | 0 ; 0,00000 (0,00000) [borne 5,0e-04] | 0 ; 0,00000 (0,00000) [borne 5,0e-04] | 812 | 0 ; 0 | 43 ; 0,01505 |
| 20 | 7200 | 0,005107 | 10 (10,003) | 6000 | 3553 | 2407 | 585 ; 0,09750 (0,00383) [+22,8] | 585 ; 0,23907 (0,00862) [+26,6] | 0 ; 0,00000 (0,00000) [borne 5,0e-04] | 0 ; 0,00000 (0,00000) [borne 1,2e-03] | 585 | 3553 ; 0 | 18 ; 0,01443 |
| 20 | 7200 | 0,00896 | 30 (30,002) | 6000 | 141 | 409 | 1441 ; 0,24017 (0,00551) [+41,7] | 1441 ; 0,24595 (0,00563) [+41,9] | 0 ; 0,00000 (0,00000) [borne 5,0e-04] | 0 ; 0,00000 (0,00000) [borne 5,1e-04] | 1441 | 141 ; 0 | 43 ; 0,01558 |
| 20 | 25000 | 0,00272 | 10 (10,004) | 6000 | 3404 | 2329 | 625 ; 0,10417 (0,00394) [+23,9] | 625 ; 0,24076 (0,00839) [+27,5] | 0 ; 0,00000 (0,00000) [borne 5,0e-04] | 0 ; 0,00000 (0,00000) [borne 1,2e-03] | 625 | 3404 ; 0 | 18 ; 0,01436 |
| 20 | 25000 | 0,004741 | 30 (30,003) | 6000 | 14 | 364 | 1494 ; 0,24900 (0,00558) [+42,8] | 1494 ; 0,24958 (0,00559) [+42,8] | 0 ; 0,00000 (0,00000) [borne 5,0e-04] | 0 ; 0,00000 (0,00000) [borne 5,0e-04] | 1494 | 14 ; 0 | 43 ; 0,01505 |
| 60 | 7200 | 0,005107 | 10 (10,003) | 6000 | 3859 | 4413 | 493 ; 0,08217 (0,00355) [+20,4] | 493 ; 0,23027 (0,00910) [+24,2] | 0 ; 0,00000 (0,00000) [borne 5,0e-04] | 0 ; 0,00000 (0,00000) [borne 1,4e-03] | 493 | 3859 ; 0 | 18 ; 0,01443 |
| 60 | 7200 | 0,00896 | 30 (30,002) | 6000 | 1140 | 2419 | 1312 ; 0,21867 (0,00534) [+39,1] | 1312 ; 0,26996 (0,00637) [+40,8] | 0 ; 0,00000 (0,00000) [borne 5,0e-04] | 0 ; 0,00000 (0,00000) [borne 6,2e-04] | 1312 | 1140 ; 0 | 43 ; 0,01558 |
| 60 | 25000 | 0,00272 | 10 (10,004) | 6000 | 3744 | 4314 | 524 ; 0,08733 (0,00364) [+21,2] | 524 ; 0,23227 (0,00889) [+25,0] | 0 ; 0,00000 (0,00000) [borne 5,0e-04] | 0 ; 0,00000 (0,00000) [borne 1,3e-03] | 524 | 3744 ; 0 | 18 ; 0,01436 |
| 60 | 25000 | 0,004741 | 30 (30,003) | 6000 | 520 | 2335 | 1487 ; 0,24783 (0,00557) [+42,7] | 1487 ; 0,27135 (0,00601) [+43,5] | 0 ; 0,00000 (0,00000) [borne 5,0e-04] | 0 ; 0,00000 (0,00000) [borne 5,5e-04] | 1487 | 520 ; 0 | 43 ; 0,01505 |

### 6.3 Classes de la garde imprimée ĝ, bloc I (sur les réplications à garde tenue ; taux de z_s ≥ 2,33 et de REJETTE dans la classe)

| L | n | p | [10 ; 12,5) | [12,5 ; 15) | [15 ; 20) | [20 ; 30) | [30 ; +∞) |
|---|---|---|---|---|---|---|---|
| 1 | 7200 | 0,005107 | m = 14581 ; z : 171 (0,0117) ; REJETTE : 24 (0,0016) | m = 258 ; z : 2 (0,0078) ; REJETTE : 1 (0,0039) | m = 0 | m = 0 | m = 0 |
| 1 | 7200 | 0,006279 | m = 697 ; z : 14 (0,0201) ; REJETTE : 3 (0,0043) | m = 14499 ; z : 143 (0,0099) ; REJETTE : 26 (0,0018) | m = 14795 ; z : 131 (0,0089) ; REJETTE : 35 (0,0024) | m = 9 ; z : 0 (0,0000) ; REJETTE : 0 (0,0000) | m = 0 |
| 1 | 7200 | 0,007274 | m = 0 | m = 14 ; z : 1 (0,0714) ; REJETTE : 0 (0,0000) | m = 15270 ; z : 143 (0,0094) ; REJETTE : 41 (0,0027) | m = 14716 ; z : 119 (0,0081) ; REJETTE : 36 (0,0024) | m = 0 |
| 1 | 7200 | 0,00896 | m = 0 | m = 0 | m = 1 ; z : 0 (0,0000) ; REJETTE : 0 (0,0000) | m = 15253 ; z : 129 (0,0085) ; REJETTE : 41 (0,0027) | m = 14746 ; z : 108 (0,0073) ; REJETTE : 22 (0,0015) |
| 1 | 25000 | 0,00272 | m = 14830 ; z : 178 (0,0120) ; REJETTE : 14 (0,0009) | m = 14 ; z : 0 (0,0000) ; REJETTE : 0 (0,0000) | m = 0 | m = 0 | m = 0 |
| 1 | 25000 | 0,003338 | m = 116 ; z : 0 (0,0000) ; REJETTE : 0 (0,0000) | m = 15148 ; z : 188 (0,0124) ; REJETTE : 18 (0,0012) | m = 14736 ; z : 156 (0,0106) ; REJETTE : 23 (0,0016) | m = 0 | m = 0 |
| 1 | 25000 | 0,00386 | m = 0 | m = 0 | m = 15164 ; z : 183 (0,0121) ; REJETTE : 30 (0,0020) | m = 14836 ; z : 181 (0,0122) ; REJETTE : 38 (0,0026) | m = 0 |
| 1 | 25000 | 0,004741 | m = 0 | m = 0 | m = 0 | m = 15215 ; z : 155 (0,0102) ; REJETTE : 45 (0,0030) | m = 14785 ; z : 180 (0,0122) ; REJETTE : 62 (0,0042) |

- Bloc D, classes (détail dans `garde_niveau.txt` et le JSON) : 55 classes non vides dans les 12 cas ; REJETTE vaut 0 dans chacune ; le taux de z_s ≥ 2,33 va de 0 (classe de 2 réplications) à 0,309, et de 0,102 à 0,309 dans les 48 classes d'au moins 100 réplications.

### 6.4 Lecture (règle du §1.8 ; aucun critère au-delà)

- **Règle SHOGEN-CRITERE-R1-1** : taux de REJETTE à tort ≤ 0,01 dans les 20 cas. Maximum : 0,00357 (SE 0,00034) à L = 1, n = 25 000, g = 30 ; de 0,00047 à 0,00357 au bloc I (sachant garde tenue : 0,00094 à 0,00357) ; 0 sur 6 000 dans les 12 cas du bloc D (borne 5,0·10⁻⁴ ; sachant garde tenue, borne de 5,0·10⁻⁴ à 1,4·10⁻³). Aucun rejet non qualifiable (n ≥ 7 200 et σ̂² = 0 ⇔ K = 0 ⇒ z_s < 0). Aucune classe de garde au-dessus de 0,01.
- **z_s seul, bloc I** : **niveau mesuré au-dessus de 0,01** pour cinq valeurs distinctes (huit des seize couples (cas, taux) ; à g ≥ 15 la garde est tenue dans toutes les réplications, d'où r_z = r_z|t) :
  - n = 25 000 : g = 15, r_z = 0,01147 (SE 0,00061 ; +2,4 SE) ; g = 20, 0,01213 (0,00063 ; +3,4 SE) ; g = 30, 0,01117 (0,00061 ; +1,9 SE) ; g = 10, sachant garde tenue, 0,01199 (0,00089 ; +2,2 SE) ;
  - n = 7 200 : g = 10, sachant garde tenue, 0,01166 (0,00088 ; +1,9 SE) ;
  - au-dessus à deux erreurs-types : n = 25 000 avec g = 15, g = 20, et g = 10 sachant garde tenue ;
  - au-dessous de 0,01 : n = 7 200 avec g = 15, 20, 30 (0,00960 ; 0,00877 ; 0,00790) ; et les deux taux inconditionnels à g = 10 (0,00577 et 0,00593), divisés par deux par la garde, qui tombe dans 50,5 % des réplications ;
  - classes de garde au-dessus de 0,01 à deux erreurs-types (descriptif) : cinq classes à n = 25 000, de 0,01200 à 0,01241.
- **z_s seul, bloc D** : de 0,059 à 0,249 (sachant garde tenue : 0,113 à 0,271), soit 6 à 27 fois 0,01 ; c'est la limite déjà écrite au pt 7, mesurée ici près de la garde.
- **Référence binomiale exacte à P connu** : de 0,01128 à 0,01558, au-dessus de 0,01 dans les 8 couples (n, p) : à P connu, l'approximation normale au seuil 2,33 sur une loi de K discrète et asymétrique dépasse déjà le niveau nominal. Le plug-in le ramène vers le bas, d'autant plus que p est grand (facteur f du §1.3 : 0,84 à 0,90 à n = 7 200, 0,91 à 0,95 à n = 25 000) : c'est pourquoi le dépassement mesuré se concentre à n = 25 000.
- **Domaine** : au bloc D, garde non tenue jusqu'à 3 859 sur 6 000 (L = 60, n = 7 200, g = 10) et σ̂² = 0 jusqu'à 4 413 sur 6 000 ; drapeau « run maximal de I ≥ ℓ » levé 4 et 1 fois (L = 60, g = 30) ; ρ^ℓ = 1,7·10⁻² à 1,75·10⁻² à L = 60 (`agreger`).
- **Sous la garde de blocs** (§1.2, déduit, non simulé) : à n < 7 200, la règle ne rend jamais REJETTE ; le taux de rejet non qualifiable y vaut r_z.

## 7. Oracles et contrôles (tous non-LLM)

| contrôle | exécution | résultat |
|---|---|---|
| (2) n²γ̂₀ = n·K(n − K) et (2b) N_lag = N_bloc, internes (`agreger`) | A, chaque réplication | R/R dans les 20 cas (312 000 réplications) |
| (5) générateur contre la théorie, interne (`agreger`) | A, 3 contrôles × 20 cas | 60 contrôles sous 5 SE ; écart maximal 2,89 SE (K/n, L = 1, n = 25 000, p = 0.00272) |
| **S-b** (T0 à T3) | A, 15:42:23Z – 15:43:26Z, 4 processus, r1 de l'export de `3414e0f` | sortie 0. T0 : 20 cas = table du §1.3 et du §2. T1 : 260 invariants et 160 invariants (4b) (ii). T2 : k* exact égal dans les 20 cas, niveau à 7,3·10⁻⁴⁵ près de `r1.binomial_tail_ge`. T3 : 2 367 réplications distinctes (r = 0..49 de chaque cas, les 459 REJETTE, les 1 000 discordances retenues, aucun rejet non qualifiable) ; dans les 2 367, valeur et cas égaux à `r1.regle_critere`, N égal à `r1.block_long_run_variance`, e, runs et K égaux à la régénération indépendante ; P̂_more identique au dernier chiffre dans 378 ; écart relatif maximal 3,9·10⁻⁴⁶ (P̂_more, garde) et 4,1·10⁻⁴⁴ (z, z_bloc). Enregistrement `garde_niveau_oracle_r1.json` |
| **Oracle (4) existant, rejoué inchangé** (`sim_niveau_oracle4.py`, sha256 `9b5b1b75…f8eb`, égal au fichier commis) | 15:15:45Z, r1 de l'export de `3414e0f` (blob `ce1da3df…`) | sortie 0 ; 320 égalités exactes (n, K, N et σ̂²_bloc sur 8 cas × 10 réplications de SIM-NIVEAU) ; enregistrement identique à `oracle4.json` versé (mesuré à `d0b9663`) hors les trois champs du commit, du blob et du sha256 de r1. Enregistrement `oracle4-3414e0f.json` |
| Oracle (4a) et (4b) existant, rejoué (contrôle d'environnement) | 15:44:14Z, r1 de l'export de `f5b8269` (blob `1d6a908c…`), `--json` sur `sim_niveau.json` et sur la sortie A | sortie 0 ; (4a) 1 363 égalités et (4b) (i) 2 280, cas et fixtures égaux à `oracle_4a_4b.json` versé ; (4b) (ii) : 64 invariants sur `sim_niveau.json`, 160 sur la sortie A. Enregistrement `oracle_4a_4b-rejeu.json` (dossier de travail, sha256 `ac8e6895c4958a1f604200204b18b21f4a1bdf56f84562ebabe0042a6de11fd1`) |
| Rejeu de l'oracle (1b) de SIM-NIVEAU (contrôle d'environnement) | 15:30:24Z – 15:32:41Z, `sim_niveau.py --R 2000 --processus 4` | JSON `3a5b91ce…69df` et texte `c241cb15…b8c` : égaux à l'octet aux sha256 inscrits au `SHA256SUMS` du dossier pour l'exécution du 2026-09-30 (Windows, Python 3.14.5). Le même code rend les mêmes octets ici (Linux, Python 3.13.14) ; la limite (m) du G1 de SIM-NIVEAU ne s'y manifeste pas |
| **Rejeux à la nouvelle tête `8ec45b8`** (ajout après A : HEAD a avancé pendant l'étape, 12 commits de l'orchestrateur, dont le lot P3 ; `scripts/sim` et `docs/adr-0028/sim-niveau` inchangés entre `3414e0f` et `8ec45b8`, `git diff --quiet` rc 0) | 15:59:49Z – 16:00:24Z, r1 de l'export de `8ec45b8` (blob `7ae940ec5812823309e059f5cad4dc2ecbba78bb`, forme `contexte_decimal()`) | oracle (4) existant inchangé : sortie 0, 320 égalités (`oracle4-8ec45b8.json`, dossier de travail, sha256 `9b351dc8e46cf7d1b428638deae333e192ea57eee7b012a59cc2eeb07e580309`) ; S-b sur la sortie A : sortie 0, T0 à T3 aux mêmes nombres qu'à `3414e0f` (2 367 réplications, valeur égale à `r1.regle_critere` dans les 2 367, P̂_more identique dans 378, mêmes écarts maximaux ; `garde_niveau_oracle_r1-8ec45b8.json`, dossier de travail, sha256 `d7748c71b74b014e0f340d1d3fa9d9fc96441e1fdd9ac91791122eae6e89d176`) |
| Suite `s2-harness` (`python3.13 -B -m unittest discover -s tests -t .`) | export de `3414e0f`, 14:53:50Z, puis le même export avec les deux fichiers neufs, 15:32:59Z | 376 tests, OK (2 sauts), les deux fois ; `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée |

- **SHOGEN-SIM-R1-DERIVE-1** (annexe B l.342) : T3 en donne la mesure sur les cas de l'étape. La réplique de `sim_niveau_calc` (r1 de `f5b8269`) et r1 de `3414e0f` donnent la même valeur de la règle sur les 2 367 réplications contrôlées, dont toutes les REJETTE ; P̂_more n'y diffère qu'au-delà du 45e chiffre significatif. Les 309 633 autres réplications ne sont pas recalculées par r1 : une valeur différente y exigerait z, z_bloc ou ĝ à moins de 10⁻⁴⁰ d'un seuil [inféré].

## 8. Provenance (G1)

### 8.1 Sources, avec leur niveau

- **[lu]** (lecture directe par ce worker, lecture seule) :
  - `docs/adr-0028/G0-partie-3.md`, entier (section S comprise), sha256 `226d0099…be7e` ;
  - `docs/adr-0028/ANNEXE-B-items.md` l.295-320 (l.305 : SHOGEN-CRITERE-GARDE-NIVEAU-1) ;
  - `docs/adr-0028/ANNEXE-D-preenregistrement.md` l.1-155 (D.1 à D.4) et ses titres ;
  - `docs/adr-0028/ADR-0028-decisions-sortie-S2.md` : lignes affichées par `grep -n "1 bis"`, puis l.89-125 (§1 bis.1 pts 1 à 11 et clauses, §1 bis.2) ;
  - `docs/adr-0028/G0-lot-SIM-NIVEAU.md` et `docs/G1-lot-SIM-NIVEAU.md`, entiers ;
  - `docs/adr-0028/PLAN-PARTIE-3.md` l.1-60 ;
  - `docs/10-mesures-pilotes-design.md` l.463-482 (§5.4) et les titres de §5.1 et §5.4 ;
  - `scripts/sim/sim_niveau.py`, `sim_niveau_calc.py`, `sim_niveau_oracle_r1.py`, `sim_niveau_oracle4.py`, entiers ;
  - `docs/adr-0028/sim-niveau/SHA256SUMS` et `oracle4.json`, entiers ; sha256 des cinq fichiers du dossier (`sim_niveau.json`, `sim_niveau.txt`, `oracle_4a_4b.json` non affichés) ;
  - `s2-harness/shogen_s2/r1.py` à `3414e0f` (`git show`) : l.1-70, l.205-390, l.508-700, liste des `def` ;
  - les 60 premières lignes de `git diff HEAD -- s2-harness/shogen_s2/r1.py` (changement en cours du lot P3), lues pour la note d'intégration de l'orchestrateur ;
  - `xtask/src/sg4.rs` l.1-101 et `xtask/src/sg5.rs` l.1-60 (périmètre et règles des gates S-G4 et S-G5 sur `docs/`) ;
  - Git : sujets des 6 derniers commits de `r1.py` et des 2 commits de `scripts/sim` et `docs/adr-0028/sim-niveau` ; `git grep` de `sim-niveau`, `scripts/sim`, `sim_niveau`, `G1-partie` dans `s2-harness`, `xtask`, `.github` à HEAD (une ligne sans rapport, `tools/oracle_record.py:41`) ;
  - `CLAUDE.md` du dépôt (fourni par le harnais).
- **[2nd]** :
  - le facteur 0,6867 du numérateur à p = 0,02 (CRITIQUE v2 §4.2), cité par le G0 de SIM-NIVEAU §3 ; recalculé ici par `calc_cas.py` : 0,6867 ;
  - la source du seuil de la garde §5.4 (UConn OER Math 3160, ch. 9, p. 121), citée par doc 10 §5.4 : non lue ;
  - `cv_theorique` = √(4ℓ/(3n)) : dérivation que la docstring de `r1.bloc_strate` attribue à l'advisor-defi ;
  - la stabilité de `random.random()` d'une version de Python à l'autre (documentation Python, citée par le G0 de SIM-NIVEAU §4) : non relue ; constatée ici sur un cas, voir §7 (rejeu de SIM-NIVEAU) ;
  - les résultats synthétiques de SIM-NIVEAU (journal G1 de SIM-NIVEAU, §4 et §6), repris au §1.3 pour motiver le partage des cas.
- **[abs]** : aucune.

### 8.2 Commandes lancées et sorties (heures `date -u` ; `TMPDIR` sur le scratchpad et `PYTHONDONTWRITEBYTECODE=1` partout)

| heure | commande (abrégée) | sortie |
|---|---|---|
| 14:32:43Z | `date -u ; git rev-parse --abbrev-ref HEAD ; git rev-parse --short HEAD ; git status --short` | `partie-3-paquet`, `3414e0f`, arbre propre |
| 14:3xZ | lectures du §8.1 (`cat`, `sed -n`, `grep -n`, `git show HEAD:…`) | — |
| 14:3xZ | `sha256sum -c SHA256SUMS` dans `docs/adr-0028/sim-niveau/` | 3 lignes OK (`sim_niveau.json`, `sim_niveau.txt`, `oracle4.json`) ; 11 fichiers listés absents du dépôt (§10) |
| 14:3xZ | `nproc ; lscpu ; free -g ; python3.13 --version` | 4 cœurs, 1 fil par cœur, 15 Gio ; Python 3.13.14 |
| 14:47Z | `ps aux --sort=-%cpu ; cat /proc/loadavg` | charge 16 ; quatre processus d'OCR d'un autre travail, suite de l'autre worker |
| 14:47Z | `python3.13 -B calc_cas.py` (deux fois : la première s'arrête sur une assertion de forme de chaîne, `0.008960` contre `0.00896`, corrigée par `normalize()`) | `calc_cas.out.txt` (§1.3) |
| 14:49Z | `git rev-parse HEAD` ; `sha256sum` des sources ; `git rev-parse HEAD:scripts/sim/*.py` ; `git diff --quiet HEAD -- scripts/sim docs/adr-0028/sim-niveau` | `3414e0f57cda…` ; rc 0 |
| 14:52:04Z | copie et sha256 du journal (pré-enregistrement) | `preenregistrement-1450Z.md`, `600471e2ccd1e5547e5e9469e5500b34f791e4421776fbf8b7c53fbc5af520c1` |
| 14:52:20Z | `python3.13 -B sonde_temps.py` | §2 |
| 14:52:49Z | copie et sha256 du journal (R fixé) | `preenregistrement-R-1452Z.md`, `83149555da44d1e7fee4b6116f234ad0a4ba508cbb1b59089418115ea79549eb` |
| 14:53Z | `git archive 3414e0f \| tar -x` (export complet) ; `rm` des pièces de D.2 de l'export, sans ouverture | — |
| 14:53:50Z | suite `s2-harness` sur l'export | 376 tests, OK (2 sauts) |
| 15:00Z à 15:14Z | essais e1 et e2, S-b sur e1 et e2, bancs v1 et v2 (§4) | §4 |
| 15:0xZ | `git archive f5b8269 s2-harness/shogen_s2 \| tar -x` ; `git hash-object` de r1 | blob `1d6a908c…` = `git rev-parse f5b8269:s2-harness/shogen_s2/r1.py` |
| 15:09Z | `git diff HEAD -- s2-harness/shogen_s2/r1.py \| head -60` | changement en cours du lot P3 (`contexte_decimal()`) |
| 15:14:24Z | exécution A | §5 |
| 15:15:34Z | exécutions B et C | §5 |
| 15:15:45Z | oracle (4) rejoué | §7 |
| 15:19:24Z | banc v3 | §4 |
| 15:30:24Z | rejeu de l'oracle (1b) de SIM-NIVEAU | §7 |
| 15:32:59Z | suite `s2-harness` sur l'export et les fichiers neufs | 376 tests, OK (2 sauts) |
| 15:42:23Z | S-b sur A | §7 |
| 15:44:14Z | oracle (4a) et (4b) rejoué | §7 |
| 15:4xZ | `controles_bit.py`, `table_resultats.py` | §5, §6 |
| 15:57Z | copie de la sortie A et des deux enregistrements dans `docs/adr-0028/sim-niveau/` ; quatre lignes ajoutées à `SHA256SUMS` ; `tail -n 4 SHA256SUMS \| sha256sum -c` | 4 OK |
| 15:59:23Z | `git rev-parse --abbrev-ref HEAD ; git log --oneline -4 ; git diff --quiet 3414e0f 8ec45b8 -- scripts/sim docs/adr-0028/sim-niveau` | HEAD = `8ec45b8` (12 commits de l'orchestrateur) ; rc 0 |
| 15:59:49Z | `git archive 8ec45b8 s2-harness/shogen_s2 \| tar -x` ; oracle (4) et S-b contre cet export | §7 |

### 8.3 Chiffres recomptés par ce worker

- Paramètres des cas (p, P_more, g théorique, runs attendus, facteur f) : `calc_cas.py`, en `Decimal` et `Fraction` ; f(0,02) = 0,6867 recalculé.
- R et durée prédite : script de la règle du §1.5 (`Fraction`), sur les temps de la sonde.
- Taux, erreurs-types, écarts à 0,01 : recalculés depuis les comptes du JSON par `table_resultats.py` (§6) et par T1 de S-b (formules du §1.6, indépendantes de S-a).
- Classes au-dessus de 0,01, extrêmes du bloc D, totaux (312 000 ; 459 REJETTE ; 1 000 discordances retenues ; 309 633 non recalculées par r1) : comptés sur le JSON de A.
- 0,0099 (α nominal) : lu dans la sortie (`NormalDist`), égal à la valeur citée par le G0 de SIM-NIVEAU.

## 9. sha256 des fichiers

| fichier | sha256 | taille |
|---|---|---|
| `scripts/sim/sim_garde_niveau.py` (S-a, neuf) | `51902b0db46e5cf680d4fec1d067455a6b2f6c5af6cefbaa4afb28ba2c6d707c` | 199 lignes |
| `scripts/sim/sim_garde_niveau_oracle_r1.py` (S-b, neuf) | `7fbc82d35a533164675792c0b97c3f948cf985cfd407e84af05eab3e8725628d` | 183 lignes |
| `docs/adr-0028/sim-niveau/garde_niveau.json` (sortie A, neuf) | `f421c41944c15d329400fffe700b779ad286236acbad5cf3a6ebcdfd7c18981b` | 169 872 octets |
| `docs/adr-0028/sim-niveau/garde_niveau.txt` (sortie A, neuf) | `e1d79bebc0b3f9beaf814ba2fd86311978fd9d4b790b46d72ed00af90d1ef94a` | 33 239 octets |
| `docs/adr-0028/sim-niveau/garde_niveau_oracle_r1.json` (S-b sur A, neuf) | `9a689015162104cdffd795139d0b9e5df3759bb47eba0a6a0be7b175e3320317` | 1 119 octets |
| `docs/adr-0028/sim-niveau/oracle4-3414e0f.json` (oracle (4) rejoué, neuf) | `0d44c76afa251c85f80723fa55751ce822036308ad623b971ad2f73eb8ef4ad5` | 903 octets |
| `docs/adr-0028/sim-niveau/SHA256SUMS` (modifié : quatre lignes ajoutées en fin de fichier, 18 lignes ; `tail -n 4 SHA256SUMS \| sha256sum -c` : 4 OK) | `47b223616f0c51b8dcd177137dd7b96aa2db00de40d4ebd788583e3a218a7237` | 1 687 octets |
| `docs/G1-partie-3-S.md` (ce journal, neuf) | donné dans le rapport du worker (un fichier ne porte pas son propre sha256) | — |

Fichiers du dossier de travail (`$TMPDIR/etape-S/`, non versés) : `calc_cas.py` `c627d64f…3175` et sa sortie `ad95c4e3…447b` ; `sonde_temps.py` `2aed34d0…1e67` et sa sortie `c1afd7c2…a949` ; instantanés du pré-enregistrement `preenregistrement-1450Z.md` `600471e2…20c1` et `preenregistrement-R-1452Z.md` `83149555…49eb` ; `controles_bit.py` `4324dc78…71a4` ; `table_resultats.py` `28831887…bc75` et `tables-A.md` `664488e9…81e1` ; journaux d'exécution A `e5321eba…5a2b`, A′ `610297b0…bcb9`, B `0c3e1947…ae08`, C `dea17d87…79d6` ; `oracles/oracle_4a_4b-rejeu.json` `ac8e6895…11fd1` ; `oracles/oracle4-8ec45b8.json` `9b351dc8…0309` et `oracles/garde_niveau_oracle_r1-8ec45b8.json` `d7748c71…d176` ; `mutants/banc_v3.py` `88b976c2…b84b`, `mutants/sortie-banc-v3.txt` `f8b8bdfc…c05a`, `mutants/v3/resultats.json` `25376a0b…1874` ; rejeu de SIM-NIVEAU `rejeu-sim-niveau-1b-p4/` (JSON `3a5b91ce…69df`, texte `c241cb15…b8c`, journal `9371ff35…0551`) ; sorties de la suite `suite-HEAD-avant.txt` `0de79bdb…6cfd` et `suite-HEAD-plus-S.txt` `05f55c45…ce8c`. Le dossier de travail est celui de la session : il n'est pas conservé au-delà ; les sha256 ci-dessus en restent la trace.

## 10. Écarts et incidents déclarés

- **E-1 (erreur de compte au §2, sans effet)** : le §2 écrit « soit 360 000 réplications par exécution complète » ; le compte exact est 8 × 30 000 + 12 × 6 000 = **312 000**. R_I, R_D et la durée prédite (calculée par script, Σ R_cas·t(n_cas)) sont justes. Le §2 n'est pas réécrit (pré-enregistrement épinglé par son sha256, `83149555…`) ; ce point en tient lieu d'erratum.
- **E-2 (sonde de temps peu représentative, sans effet)** : la sonde a duré une seconde (35 réplications par processus) sous une charge de 16 ; la durée prédite (37,6 min) a surestimé A (27 min 28 s). La règle du §1.5 est appliquée telle qu'écrite ; R n'a pas changé. Conséquence de la règle du §1.7 : A ≤ 30 min, donc exécution complète A′.
- **E-3 (graine)** : aucune graine neuve n'est posée ; la dérivation et GRAINE de SIM-NIVEAU sont reprises à la lettre, les flux de l'étape étant distincts par p (§1.4). Choix motivé, déclaré ici pour qu'il soit tranché (Q-6).
- **E-4 (écarts au cadre de SIM-NIVEAU)** : (E-a) à (E-f) du §1.1, dont le critère de domaine levé à dessein et la réplique de r1 de `f5b8269` (mesurée par T3, §7).
- **E-5 (concurrence pendant A)** : B, C, le banc v3, les rejeux et la suite ont tourné pendant A, avec deux charges extérieures (OCR, autre worker) ; sans effet sur les octets (B = C, préfixes égaux, A = A′ au §5 bis).
- **E-6 (incident d'outillage, sans effet)** : l'arrêt du banc v1 par `pkill -f banc.py` a aussi terminé le shell qui le lançait (code 144) ; le banc s'est arrêté, sa sortie partielle est conservée (`mutants/essai-1-interrompu/`).
- **E-7 (`SHA256SUMS` du dossier, antérieur à l'étape)** : il liste 14 fichiers, dont 11 absents du dépôt (`execution-B/…`, `oracle-1b/…`, `sim_niveau.log.txt`) et `oracle-4a-4b/oracle_4a_4b.json`, versé à la racine du dossier sous le nom `oracle_4a_4b.json` (même sha256 `bd3cc311…`) ; `sha256sum -c SHA256SUMS` y échoue donc (11 fichiers illisibles). Lignes existantes non touchées ; quatre lignes ajoutées en fin de fichier (§9), vérifiées seules (Q-2).
- **E-8 (fichiers versés)** : quatre fichiers neufs au dossier au lieu de deux : la sortie (`garde_niveau.json`, `garde_niveau.txt`) et deux enregistrements d'oracle (`garde_niveau_oracle_r1.json`, `oracle4-3414e0f.json`), comme `oracle4.json` et `oracle_4a_4b.json` pour SIM-NIVEAU ; le journal d'exécution `garde_niveau.log.txt` reste au dossier de travail (sha256 au §5). Retirer les deux enregistrements ne touche pas la sortie (Q-1).
- **E-10 (contrôle du pré-enregistrement)** : `diff preenregistrement-R-1452Z.md docs/G1-partie-3-S.md` ne montre aucune ligne retirée ni modifiée (zéro ligne « < ») ; de même entre les deux instantanés de 14:52Z : le §1 et le §2 sont intacts, le journal n'a reçu que des ajouts (§0, puis §3 à §12).
- **E-9 (r1 figé)** : S-b est mesuré contre r1 de `3414e0f`, pas contre l'arbre de travail, où le lot P3 modifie `r1.py` (§3) ; S-b reste exécutable contre la forme à `contexte_decimal()`. Seule lecture de l'arbre de travail sur ce chemin : les 60 premières lignes de `git diff HEAD -- s2-harness/shogen_s2/r1.py` (15:09Z), pour la note d'intégration ; rien n'en est calculé (l'en-tête « jamais dans l'arbre de travail » vise les calculs).

## 11. Limites (items à former par l'orchestrateur ; règle PAROXYSME)

- **L-1 (conséquence pré-déclarée : limite à écrire au paquet, jamais une révision)** — proposition de nom : SHOGEN-GARDE-NIVEAU-ZSEUL-1. Sous le modèle nul synthétique à fenêtres iid, **le niveau de z_s seul est mesuré au-dessus de 0,01 près de la garde** : à n = 25 000, 0,01117 à 0,01213 pour g de 15 à 30 (SE 0,00061 à 0,00063) et 0,01199 (SE 0,00089) sachant garde tenue à g = 10 ; à n = 7 200, g = 10, 0,01166 (SE 0,00088) sachant garde tenue. Trois de ces taux sont au-dessus à deux erreurs-types. La référence binomiale exacte à P connu (0,0113 à 0,0156) montre que l'approximation normale au seuil 2,33 dépasse le niveau nominal sur cette plage de g, et que seul le plug-in l'en rapproche, d'autant moins que p est petit. **Sous la règle, le taux de REJETTE à tort reste ≤ 0,00357 (SE 0,00034) dans les 20 cas.** Place proposée : la limite « approximation normale à la garde » du pt 11, avec les chiffres et leurs erreurs-types ; ce taux est aussi celui du repli §1 bis.3 (z_s seul). Prix : quelques lignes de texte [inféré].
- **L-2 (n non mesurés)** : seuls n = 7 200 et 25 000 sont simulés. Au-delà de 25 000, à g fixé, p décroît et le plug-in devient moins conservateur : le niveau de z_s seul s'y rapprocherait de la référence à P connu [inféré, non mesuré]. Entre 7 200 et 25 000 : interpolation non mesurée. Construction : même script, deux couples (n, p) de plus, pré-enregistrés ; prix ≈ 10 lignes et une exécution [inféré].
- **L-3 (modèle homogène)** : mêmes p et L pour les 11 flux, grille complète, durées géométriques : SHOGEN-SIM-NIVEAU-MODELES-1 (existant) s'applique tel quel à l'étape.
- **L-4 (résolution sous dépendance)** : R_D = 6 000 borne le taux de REJETTE à tort à 5,0·10⁻⁴ (95 %) par cas du bloc D ; la sortie établit « ≤ 0,01 » avec marge, pas une valeur sous 5·10⁻⁴.
- **L-5 (strates sous la garde de blocs, déduit et non simulé)** : à n < 7 200 (strates stress des J14, au plus 5 760 et 2 880 fenêtres, ADR §1 bis.2), la règle ne rend jamais REJETTE et son taux de rejet non qualifiable vaut r_z, mesuré ici aux n = 7 200 seulement.
- **L-6 (dérive de la réplique de r1)** : voir §7 et SHOGEN-SIM-R1-DERIVE-1 ; 309 633 réplications ne sont pas recalculées par r1.
- **L-7 (bit-identité entre plates-formes)** : héritée de SIM-NIVEAU (limite (m) de son G1) pour `alpha_nominal`, `borne95_si_x_nul`, `z_sd`, `z_bloc_sd`, `rho_puissance_ell` ; le rejeu de l'oracle (1b) de SIM-NIVEAU sur cette machine est identique à l'octet (§7), sans que cela couvre toutes les plates-formes.

## 12. Questions à l'orchestrateur

- **Q-1** : garder au dossier les deux enregistrements d'oracle (`garde_niveau_oracle_r1.json`, `oracle4-3414e0f.json`) ou n'y verser que la sortie (E-8) ?
- **Q-2** : `SHA256SUMS` du dossier : corriger les 11 lignes de fichiers non versés et le chemin de `oracle_4a_4b.json` (acte de l'orchestrateur, E-7) ?
- **Q-3** : former L-1 (nom proposé SHOGEN-GARDE-NIVEAU-ZSEUL-1) et ses lignes au paquet (pt 11 et repli §1 bis.3) ; former L-2 si un n hors de [7 200 ; 25 000] doit être couvert.
- **Q-4** : S-b et l'oracle (4) sont rejoués à `8ec45b8` (r1 du lot P3, §7), aux mêmes résultats ; leurs enregistrements restent au dossier de travail. Faut-il verser ceux-là, ou les rejouer au commit d'analyse final si r1 change encore avant le scellement (SHOGEN-SIM-R1-DERIVE-1 : une commande chacun, moins d'une minute) ?
- **Q-5** : lignes datées de l'annexe A pour les sous-lots S-a (199 lignes) et S-b (183 lignes).
- **Q-6** : ratifier la reprise de la graine de SIM-NIVEAU (E-3), ou demander une étiquette propre, qui exigerait un changement de `sim_niveau_calc` ou une substitution de module, puis une nouvelle exécution déclarée.

Fin de rédaction : 2026-10-02, 16:01Z (`date -u`, relevé avant le calcul du sha256 final, donné dans le rapport du worker).
