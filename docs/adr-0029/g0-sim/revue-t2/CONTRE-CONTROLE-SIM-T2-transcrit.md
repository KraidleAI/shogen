# Contre-contrôle des corrections de SIM-BIS tranche 2 (transcrit)

> Transcription par l'orchestrateur le 2026-10-05 04:04:50 UTC du rapport rendu par message par le réviseur G2 (agent a507e004d00e5d755) ; contrôle FM-1.1 du transcript : fragments_l51_l14 = 0. Texte du réviseur ci-dessous, sans retouche.

# Contre-contrôle des corrections G2 : SIM-BIS tranche 2 (SB-4C à SB-4H)

**Gate 0** : `claude-opus-5-5` (identifiant exact), effort max.
**Dates** (`date -u`) : 2026-10-05, de 03:49:12 à 04:03:34 UTC.
**Tête** : 122c670 au début et à la fin, arbre propre ; aucune opération git en écriture.
**Pièces** : `corr/SHA256SUMS` (`60dd6f37…`) 195 sur 195 OK. AVIS-SIM-T2 lu (`30950295…`). Le G0 reste `d9cffc0a…` sur le fichier, à 784ebd2 et à 122c670.
**Preuves** : `<scratchpad>/s2bis/sim2/g2/rev2/` (`SHA256SUMS` `7dc061c8…`, 52 entrées, aucun octet 92). Copies et cible cargo supprimées.

## Verdict : CONFORME (deux observations non bloquantes)

### Série
- Les 12 diffs passent `--check` et s'appliquent en série sur 122c670.
- `scripts/sim-bis` et le runner sont égaux aux empreintes de c4h (16 fichiers). `gates.yml` n'en diffère que par le plancher s2bis (114 au lieu de 49).
- Sur 784ebd2 : 17 empreintes sur 17.
- Lignes de code ajoutées : 109, 45, 46, 77, 47, 27.
- Chaque état est vert seul à son plancher exact : 75, 85, 87, 88, 90, 91, 93. Commande : runner (33 ok) puis ligne du job, sous `unshare -n` avec `lo` allumée par ioctl (aucune commande `ip` sur l'hôte).

### 1. Mes corrections : C-1 à C-5 et O-2 sont corrigées
- **Mes 28 mutants**, rejoués par la commande du job (runner d'abord, borne 300 s) sur la série posée sur 122c670 : **27 tués, 0 FATAL**.
  - R-28 reste vivant : c'est la limite écrite, présente dans les docstrings de `refus_puissance` et `refus_hasard` et dans le README.
  - R-01a est bien la même mutation que R-01 : `rang(prm, h)` devient l'indice 0 pour toutes les unités faibles. Il est tué par `test_faibles_independantes`.
- **C-2 et C-3**, vérifiés avec mes sondes de la première passe :
  - κ = 1/2, φ = 2 ou −1/2 avec κ = 1, ou τ_D = 0 : `SOURCES/regime`, par `regime()` comme par `pannes()` ;
  - unité faible hors du pool (bybit) : `SOURCES/faible`.
- **C-5** : l'empreinte est recalculée, l'ancienne valeur est citée, et les points 2 et 3 de l'ajout daté sont cités.
- **O-2** : « ≈ » est écrit.

### 2. C-6 (indices_hotes)
- **Ordre** : celui de l'ADR-0029 l.168, que j'ai lu ; EP l.8 confirme aucun retrait. La source est écrite dans `parametres.json`.
- **Refus** : `SOURCES/indice` pour un hôte absent ou une liste à doublon, par `indice()`, `etat()` et `faibles()`.
- **Identité** : ma sonde donne `a78a9c33…c03c3` 16 fois sur 16 (3.10.20, 3.11.15, 3.12.3, 3.13.14 × PYTHONHASHSEED 0, 1, 4242, aléatoire). La sonde du worker donne `a424e5e8…`.
- **Loi des tirages inchangée** (seuls les flux bougent) ; mes contrôles remesurés :
  - composantes : 2 208 combinaisons exactes ;
  - réplication complète : 60 taux, χ² = 36,5, |z| ≤ 1,84 ;
  - régime : marge z = −0,43 ; part de Z z = +0,82 ; séjour moyen 19,95 ; P(·|Z=0) z = −0,38 ; P(·|Z=1) z = −1,64 ;
  - pannes longues : |z| ≤ 1,79 sur 3 000 réplications ;
  - incidents et tirages des dérives identiques au premier passage, leurs flux n'étant pas indexés par hôte ;
  - amincissement : χ²(16) = 22,2 et 15,4 sur 2 000 réplications par cellule. Un χ² de 32,8 obtenu à 600 réplications était une fluctuation.

### 3. C-7 (valeurs sourcées)
- Les valeurs sont fidèles à l'AVIS (Q-T2-5 l.135-144 ; tableau Q-T2-6 l.148-154 ; Q-T2-10 l.202-216) et à la PROPOSITION (l.150, l.152, l.155). Toutes les lignes citées sont vérifiées.
- `poids_longues [1, 1, 1]` est branché dans `loi_longues`, avec `SOURCES/loi` si le nombre de poids diffère du nombre de durées.
- `tendance_par_semaine` et `absorption` ne sont pas lus par le code ; leur présence et leur forme sous le schéma sont testées.

### 4. C-8 (oracles du taux aminci)
Les z sont recalculés par mon propre script ; Σ m(t) calculée terme à terme est égale à la formule fermée.

| cellule | tendance (croissant / décroissant) | saut (croissant / décroissant) |
|---|---|---|
| celle du test, 60 réplications | −0,48 / −1,35 | +1,05 / −0,75 |
| cellule neuve, 300 réplications | +1,22 / −1,14 | +1,96 / +0,40 |

Les valeurs sur la cellule du test sont égales à celles du rapport.

### 5. Gates sur 122c670
- Runner : 33 ok.
- Jobs : sim-bis Ran 93, s2bis Ran 114, s2-harness 405 OK (skipped=2).
- Python 3.10 à 3.13 avec `-W error` (PYTHONHASHSEED 0 et 7) : 93 OK partout.
- R-13 : aucun marqueur. R-8 : seul `import calendrier` est ajouté. Octets 92 : 0 dans le lot et dans les six diffs.
- xtask : S-G1 à S-G8 VERT ; fmt, no_std et clippy VERT ; S-G9 ROUGE sur docs/17:70, déjà connu.
- Mutants en plus : mes K-01 à K-04 (rang décalé, flux faible commun, poids inversés, amincissement à a + 1) sont tués. Les 16 mutants neufs et les 6 compléments du worker, rejoués avec mon outil, sont tous tués.

### 6. Écarts et points du worker
- **E-1** : accepté ; ce sont des retouches de texte, et mes rejeux portent sur les diffs finaux.
- **E-2** : accepté ; 0 octet 92 dans le lot et les diffs (vérifié).
- **E-3** : accepté ; comptes et noms seulement, dossiers interdits exclus des copies. À l'avenir, limiter ces commandes à `scripts/sim-bis`.
- **E-4 et E-5** : acceptés.
- **E-6** : accepté ; c'est le fil d'alarme voulu, et ton adjudication garde le G0 intact.
- **E-7** : accepté ; exposition permise.
- **Point 1** : d'accord ; le refus est un défaut sûr. Voir O-A.
- **Point 2** : d'accord avec ton adjudication ; l'empreinte et l'épingle de `test_provenance_c_5` restent valides.
- **Point 3** : d'accord ; une surcharge incohérente échoue fermée.
- **Point 4** : sans effet ; 7,5 à 10,4 s pour un job borné à 10 min.
- **Point 5** : d'accord.

## Observations (non bloquantes)
- **O-A** : `derives()` tire les sens et les hôtes à saut dans l'ordre de `calibration.unites`. Un pool réordonné ou réduit réaffecte donc les dérives entre hôtes. Mesuré : l'état vrai des autres hôtes change avec « tendances » ou « sauts + initiale », et reste identique sans dérive. C'est hors de la lettre de C-6. À ancrer sur `indices_hotes` avant E0, avec la correspondance des identifiants de Q-S-07 (point 1 du worker).
- **O-B** : mon mutant K-05 survit. Le refus d'une strate inconnue par `indice()` n'est pas testé ; sous le mutant, l'erreur devient une `ValueError` non nommée. La lacune est antérieure aux corrections et sans effet en pratique.
