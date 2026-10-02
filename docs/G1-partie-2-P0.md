# Journal G1 — partie 2 de S2, lot P0 — rapport du worker, versé tel que livré

> **Note de l'orchestrateur (2026-10-02, au versement)** : texte du worker versé tel que livré, à une exception près : les guillemets « » de trois phrases anglaises **fictives** (fixtures des mutants, l.76, l.227, l.280 du fichier livré) sont remplacés par “ ”, pour que la gate S-G5 ne les prenne pas pour des citations de source (en corpus complet, elles seraient « introuvables »). Le code de `xtask/tests/mutants.rs` garde ses « ». Fichier livré : sha256 `52638e76…` ; aucun autre changement.

Gate 0 : `claude-opus-5-5`.

## Rapport G1, lot P0 : S-G4 et S-G5 étendues à `s2-harness/**/*.md` (SHOGEN-ORACLE-PERIMETRE-1, partie i)

Les deux gates couvrent désormais `docs/` et `s2-harness/`, et chacune imprime son compte par chemin. Les mutants rougissaient avant la modification des gates et sont verts après. Sur l'arbre réel, `cargo --locked xtask verify` est VERT :
- **S-G4** : 71 fichiers examinés sur 71 (69 de `docs/` + 2 de `s2-harness/`).
- **S-G5** : 72 sur 72 (70 + 2).
- **README et RUNBOOK** : aucune violation, donc aucun texte corrigé (sha256 inchangés).
- **Taille** : 3 fichiers, +132 −33, soit 165 lignes sous le plafond de 200. Rien n'est commité.

### 1. Journal de provenance

**Sources lues [lu]**
- `docs/adr-0028/G0-partie-2.md` l.1-28 (section P0, l.6-27).
- `docs/adr-0028/ANNEXE-B-items.md` l.180-199 (l.188).
- `docs/G1-lot-DOCS-S2.md` l.70-113 (C-9 à la l.90).
- `.claude/agents/shogen-devops.md` l.1-73 (§2, l.28-43).
- `docs/adr-0028/ANNEXE-D-preenregistrement.md` l.30-69 (liste D.2).
- `xtask/src/` en entier : `sg4.rs`, `sg5.rs`, `documents.rs`, `roles.rs`, `rapport.rs`, `lib.rs`, `main.rs`.
- `xtask/tests/mutants.rs` en entier.
- Manifestes : `xtask/Cargo.toml`, `Cargo.toml` racine, `.cargo/config.toml`, `rust-toolchain.toml`. Il n'y a ni lints de workspace ni `clippy.toml`.
- `docs/DEVOPS.md` l.81-82 (par grep).
- `.github/workflows/squelette.yml` l.50-62 et l.109-110 : checkout complet, sans clairsemage.
- `.gitignore` l.30-38.
- `run_campaign.py` l.202-240 et l.289 (par grep).
- `s2-harness/README.md` et `RUNBOOK-campagne.md` : traités par outil, qui n'imprime que des comptes ; contenu jamais affiché.

**Pièces D.2** : aucune ouverte, `SHOGEN_S2_CAMPAGNE_CONTROL` jamais posée (0 variable `SHOGEN*` dans l'environnement). Dans les sorties `verify` d'avant et de fin, j'ai compté par grep, sans rien afficher, les références `cartographie-2026-09-29.md:51` et `adr-0025/` : 0 et 0.

**Commandes et sorties**
- `date -u` : 02:56:33 UTC au départ. HEAD `37ea234`, branche `partie-2-rendu`. Avant le lot, seul `docs/adr-0028/G0-partie-2.md` est non suivi.
- **Mesure avant** (`verify`, rc 0, global VERT) :
  - S-G4 : couverture 69 sur 69.
  - S-G5 : 70 sur 70 ; 252 fragments contrôlés, 2680 écartés ; corpus incomplet (0 artefact sur 125) ; 218 non contrôlés.
- **`.md` sur le disque et dans l'index git** :
  - `docs/` : 70 sur le disque, 69 suivis. L'écart est le G0 non suivi, qui entre donc au périmètre sur le disque.
  - `s2-harness/` : 2 sur le disque (README, RUNBOOK) = 2 suivis. Aucun fichier non suivi, ni `data/` ni `__pycache__`.
- **Suites de référence avant** : `cargo --locked test -p xtask` donne 28 + 9 tests verts. La suite du harnais (`python3 -B -m unittest discover -s tests -t .`) donne `Ran 307 tests … OK (skipped=2)`.
- **Après le lot** :
  - `cargo --locked test -p xtask` : 31 + 9 verts. La ligne `error … jouet` vient d'un test existant de `reproductible.rs` (1 occurrence avant, 1 après).
  - Suite du harnais : 307 tests, OK (skipped=2), aucun `__pycache__` créé.
  - Mesure finale : `cargo fmt --check` rc 0 ; `verify` rc 0, les 8 gates VERTES ; fmt, `no_std` et clippy VERTS (la passe clippy affiche `Checking xtask`, donc le code modifié a bien été contrôlé).
- **Sondes jetables** (binaire construit, arbres du scratchpad) :
  - S-G5 sans `biblio/INDEX.md` : ROUGE, couverture « 0 examiné(s) sur 2 présent(s) ».
  - `s2-harness/` présent mais sans `.md` : S-G4 et S-G5 ROUGES, « aucun fichier .md sous s2-harness ».

**Chiffres recomptés**
- S-G4 : 71 = 70 `.md` de `docs/` comptés par `find`, moins le registre, plus 2. S-G5 : 72 = 70 + 2.
- Écart de S-G5 entre avant et après : 2680 → 2709 écartés, soit +29. Un script Python indépendant, écrit d'après la spécification en commentaire de `sg5.rs`, retrouve 29 fragments :
  - README : 8 citations « … », 9 fragments ;
  - RUNBOOK : 20 citations, 20 fragments ;
  - tous sous le seuil, 0 contrôlé.
- Les contrôlés restent à 252, les non contrôlés à 218, dont 0 de `s2-harness/`.
- S-G4 : les 15 `LOCUTIONS_INTERDITES` donnent 0 occurrence brute dans les deux fichiers, avant tout blanchiment.
- Typographie des deux fichiers : guillemets « et » équilibrés (8/8 et 20/20), guillemets droits 2 et 0, clôtures de code 2 et 12 (nombres pairs).
- Ligne `:8` des violations des mutants, recalculée à la main : la fixture a 6 lignes, le mutant ajoute une ligne vide puis la ligne fautive.

### 2. Preuve des mutants

**Avant la modification des gates** (`cargo --locked test -p xtask --test mutants`, rc 101) : 27 tests passent, 4 échouent.
```
mutant_couverture_harnais_supprime ... FAILED   → « S-G4 devait être ROUGE et ne l'est pas »
mutant_sg4_locution_interdite_dans_le_harnais ... FAILED → « S-G4 devait être ROUGE et ne l'est pas »
mutant_sg5_citation_hors_corpus_dans_le_harnais ... FAILED → « S-G5 devait être ROUGE et ne l'est pas »
temoin_arbre_documentaire_intact_est_vert ... FAILED → « S-G4 doit imprimer la couverture de s2-harness/ »
```
Sortie capturée du mutant S-G4 : `docs/**/*.md (hors …)`, couverture 1 sur 1, VERDICT VERT, alors que la locution est dans `s2-harness/README.md`. Mutant S-G5 : couverture 2 sur 2, VERT.

**Après** (`--nocapture harnais`) : les 3 tests passent.
```
S-G4  docs/**/*.md : 1 fichier(s) | s2-harness/**/*.md : 1 fichier(s) | couverture : 2 sur 2
      VIOLATION s2-harness/README.md:8 — « donnée vérifiée » dans la voix du projet … ROUGE
S-G5  couverture : 3 sur 3
      VIOLATION s2-harness/README.md:8 — citation introuvable … “this sentence is not in the corpus and it must be caught in the harness” ROUGE
Couverture (s2-harness/ supprimé) : S-G4 et S-G5 — « répertoire absent ou illisible : s2-harness (… la gate refuse de conclure) » ROUGE
```

### 3. Couverture

| | avant | après |
|---|---|---|
| S-G4 | 69 sur 69 (`docs/` seul) | 71 sur 71 (69 + 2), VERT |
| S-G5 | 70 sur 70 | 72 sur 72 (70 + 2), VERT |
| Non contrôlés de S-G5 | 218 | 218, **0 de `s2-harness/`** (régime partiel, 0 artefact sur 125) |

Fichiers de `s2-harness/` examinés : 2, `README.md` et `RUNBOOK-campagne.md`.

### 4. Diff

`git diff --stat` : `sg4.rs` 45 (+29 −16), `sg5.rs` 37 (+24 −13), `mutants.rs` 83 (+79 −4) ; total 132 insertions, 33 suppressions.

Copie : `/tmp/claude-0/-home-user-shogen/7ba84933-ba6d-5813-9ef4-ca3ac4febd16/scratchpad/lot-P0.diff` (sha256 `451452280250335b163ba014bc409650ceb339b045261e6b9a267e606ceb23a4`).

sha256 des fichiers finaux :
- `sg4.rs` : `b0f7f12527057f5c98435ced8aeca6d2b8847e377dea7d4b109816219f849bdb`
- `sg5.rs` : `1d0942431cad2e143b04a02af404b65242b5d55c32d7ad0e5af78f1c3259b867`
- `mutants.rs` : `5fb807ff33ff912a464361e1739d5a1046c0f753fcebcf573a2d7eeaaba3dbb0`

```diff
diff --git a/xtask/src/sg4.rs b/xtask/src/sg4.rs
--- a/xtask/src/sg4.rs
+++ b/xtask/src/sg4.rs
@@ -17,7 +17,9 @@
 //! Périmètre : `docs/**/*.md`, **hors `docs/09-vocabulaire.md`** — le
 //! registre qui énonce les interdits ne peut pas être scanné contre
-//! lui-même (sa section « héritées » nomme les mots hors guillemets).
+//! lui-même (sa section « héritées » nomme les mots hors guillemets) —, puis
+//! `s2-harness/**/*.md` sans exclusion (depuis le 2026-10-02 : README et
+//! RUNBOOK du harnais, SHOGEN-ORACLE-PERIMETRE-1 (i), ADR-0028 annexe B).
@@ -93,23 +95,34 @@
+/// Les arbres du périmètre, en chemins exacts et dans cet ordre. Chacun est
+/// recensé par `fichiers_markdown` : absent ou sans `.md`, il est un incident,
+/// jamais un ensemble vide. S-G5 lit cette même liste : un seul périmètre
+/// pour les deux gates.
+pub const PERIMETRE: &[&str] = &["docs", "s2-harness"];
+
 pub fn executer(racine: &Path) -> Rapport {
     let mut rapport = Rapport::nouveau("S-G4", "vocabulary (registre 09 mécanisé, voix du projet)");
-    rapport.chemins_couverts.push(String::from(
-        "docs/**/*.md (hors docs/09-vocabulaire.md — le registre lui-même)",
-    ));
-
-    let recensement = fichiers_markdown(racine, "docs");
-    for incident in &recensement.incidents {
-        rapport.incident(incident.clone());
-    }
-
     let registre = racine.join(REGISTRE);
-    let a_examiner: Vec<_> = recensement
-        .fichiers
-        .iter()
-        .filter(|chemin| **chemin != registre)
-        .collect();
+    let mut a_examiner = Vec::new();
+    for relatif in PERIMETRE {
+        let recensement = fichiers_markdown(racine, relatif);
+        for incident in recensement.incidents {
+            rapport.incident(incident);
+        }
+        let retenus: Vec<_> = recensement
+            .fichiers
+            .into_iter()
+            .filter(|chemin| *chemin != registre)
+            .collect();
+        rapport
+            .chemins_couverts
+            .push(format!("{relatif}/**/*.md : {} fichier(s)", retenus.len()));
+        a_examiner.extend(retenus);
+    }
+    rapport.chemins_couverts.push(format!(
+        "hors {REGISTRE} — le registre lui-même, seule exclusion du périmètre"
+    ));
     rapport.presents = a_examiner.len();
@@ -117,7 +130,7 @@
-    for chemin in a_examiner {
+    for chemin in &a_examiner {
diff --git a/xtask/src/sg5.rs b/xtask/src/sg5.rs
--- a/xtask/src/sg5.rs
+++ b/xtask/src/sg5.rs
@@ -1,5 +1,9 @@
-//! **S-G5 `citations`** — une citation dans `docs/` doit exister dans le
-//! registre bibliographique ou dans les octets détenus.
+//! **S-G5 `citations`** — une citation dans `docs/` ou `s2-harness/` doit
+//! exister dans le registre bibliographique ou dans les octets détenus.
+//!
+//! Périmètre : celui de S-G4 (`crate::sg4::PERIMETRE`) — `docs/**/*.md`,
+//! puis `s2-harness/**/*.md` depuis le 2026-10-02 (SHOGEN-ORACLE-PERIMETRE-1
+//! (i), ADR-0028 annexe B).
@@ -35,6 +39,7 @@
 use crate::roles::chemin_relatif;
+use crate::sg4::PERIMETRE;
 use crate::source::ligne_de;
@@ -66,9 +71,21 @@
     let mut rapport = Rapport::nouveau("S-G5", "citations (une-citation-un-grep, mécanisée)");
-    rapport
-        .chemins_couverts
-        .push(String::from("docs/**/*.md (extraction des « … » anglais)"));
+    // Le périmètre est recensé d'abord : sa couverture s'imprime même quand
+    // le registre manque (retour anticipé ci-dessous).
+    let mut fichiers = Vec::new();
+    for relatif in PERIMETRE {
+        let recensement = fichiers_markdown(racine, relatif);
+        for incident in recensement.incidents {
+            rapport.incident(incident);
+        }
+        rapport.chemins_couverts.push(format!(
+            "{relatif}/**/*.md : {} fichier(s) (extraction des « … » anglais)",
+            recensement.fichiers.len()
+        ));
+        fichiers.extend(recensement.fichiers);
+    }
+    rapport.presents = fichiers.len();
     rapport.chemins_couverts.push(String::from(
@@ -141,17 +158,11 @@
-    // 2. Les citations des docs.
-    let recensement = fichiers_markdown(racine, "docs");
-    for incident in &recensement.incidents {
-        rapport.incident(incident.clone());
-    }
-    rapport.presents = recensement.fichiers.len();
-
+    // 2. Les citations des documents du périmètre.
     let mut controlees = 0usize;
@@
-    for chemin in &recensement.fichiers {
+    for chemin in &fichiers {
diff --git a/xtask/tests/mutants.rs b/xtask/tests/mutants.rs
--- a/xtask/tests/mutants.rs
+++ b/xtask/tests/mutants.rs
@@ -386,8 +386,10 @@
 /// Construit l'arbre documentaire synthétique conforme : docs/ (registre 09
-/// présent + une note propre), JOURNAL.md valide, biblio/INDEX.md dont
-/// l'en-tête et les mentions concordent avec deux artefacts présents.
+/// présent + une note propre), s2-harness/ (un README propre — périmètre de
+/// S-G4/S-G5 depuis SHOGEN-ORACLE-PERIMETRE-1 (i)), JOURNAL.md valide,
+/// biblio/INDEX.md dont l'en-tête et les mentions concordent avec deux
+/// artefacts présents.
@@ -407,6 +409,16 @@
+    ecrire(
+        &racine,
+        "s2-harness/README.md",
+        concat!(
+            "# harnais synthétique\n\n",
+            "Le harnais nomme « donnée vérifiée » en citation marquée.\n\n",
+            "Une citation adossée : “this quotation is present in the corpus and\n",
+            "it is checked by the gate”.\n",
+        ),
+    );
@@ -454,12 +466,13 @@
-    for rapport in gates_documentaires(&racine) {
+    let rapports = gates_documentaires(&racine);
+    for rapport in &rapports {
@@
-            motifs(&rapport)
+            motifs(rapport)
@@ -468,6 +481,15 @@
+    // Vert pour la bonne raison : le README synthétique du harnais est
+    // recensé et sa couverture imprimée, pas ignoré.
+    for gate in ["S-G4", "S-G5"] {
+        let couverts = rapport_de(&rapports, gate).chemins_couverts.join("\n");
+        assert!(
+            couverts.contains("s2-harness/**/*.md : 1 fichier(s)"),
+            "{gate} doit imprimer la couverture de s2-harness/ ; chemins :\n{couverts}"
+        );
+    }
@@ -506,6 +528,59 @@
+// SHOGEN-ORACLE-PERIMETRE-1 (i) (ADR-0028 annexe B) : README et RUNBOOK de
+// `s2-harness/` entrent au périmètre de S-G4 et S-G5. Chaque mutant exige le
+// ROUGE pour le motif attendu ET situé dans le harnais.
+fn exiger_rouge_dans_le_harnais(rapport: &Rapport, attendu: &str) {
+    exiger_rouge(rapport, attendu);
+    let motifs = motifs(rapport);
+    assert!(
+        motifs.contains("s2-harness/README.md:"),
+        "{} : la violation doit être située dans le harnais ; motifs :\n{motifs}",
+        rapport.gate
+    );
+}
+
+#[test]
+fn mutant_sg4_locution_interdite_dans_le_harnais() {
+    let racine = arbre_documentaire("sg4-harnais");
+    ajouter(
+        &racine,
+        "s2-harness/README.md",
+        "\nCette donnée vérifiée fonde le verdict du harnais.\n",
+    );
+    let rapports = gates_documentaires(&racine);
+    exiger_rouge_dans_le_harnais(rapport_de(&rapports, "S-G4"), "« donnée vérifiée »");
+}
+
+#[test]
+fn mutant_sg5_citation_hors_corpus_dans_le_harnais() {
+    let racine = arbre_documentaire("sg5-harnais");
+    ajouter(
+        &racine,
+        "s2-harness/README.md",
+        "\nUne citation forgée : “this sentence is not in the corpus and it\nmust be caught in the harness”.\n",
+    );
+    let rapports = gates_documentaires(&racine);
+    exiger_rouge_dans_le_harnais(rapport_de(&rapports, "S-G5"), "citation introuvable");
+}
+
+/// Le refus sur répertoire absent tient pour le chemin neuf : supprimer
+/// `s2-harness/` ne fait pas disparaître sa couverture, il rend les deux
+/// gates ROUGES (même doctrine que `mutant_couverture_repertoire_de_role_supprime`).
+#[test]
+fn mutant_couverture_harnais_supprime() {
+    let racine = arbre_documentaire("couverture-harnais");
+    std::fs::remove_dir_all(racine.join("s2-harness")).expect("suppression du harnais synthétique");
+    let rapports = gates_documentaires(&racine);
+    for gate in ["S-G4", "S-G5"] {
+        exiger_rouge(
+            rapport_de(&rapports, gate),
+            "répertoire absent ou illisible : s2-harness",
+        );
+    }
+}
```
Les lignes de contexte sans changement entre les hunks sont abrégées par `@@`. Le texte exact est dans le fichier diff ci-dessus.

Hygiène : aucun `TODO` ni `FIXME`, aucun `#[allow]` (0 par grep), `git diff --check` propre, aucune dépendance neuve. Je n'ai touché ni `JOURNAL.md`, ni les annexes, ni `docs/pocket-report/`. Aucune opération git.

### 5. Écarts au G0

1. **Tests en plus du G0** :
   - mutant de couverture `mutant_couverture_harnais_supprime`, preuve directe du risque (a), refus non affaibli ;
   - témoin resserré : il exige la ligne `s2-harness/**/*.md : 1 fichier(s)` ;
   - aide `exiger_rouge_dans_le_harnais`, qui exige aussi que la violation soit située dans le harnais.

   Ce sont des resserrages, à retirer au G2 si on les juge hors mandat.
2. **Taille** : le G0 estimait ≈ 15 lignes de code et ≈ 60 de tests [inféré]. Mesuré : +53 −29 de code, commentaires de module compris, et +79 −4 de tests. L'écart vient du compte imprimé par chemin et du déplacement du recensement de S-G5.
3. **Changement de comportement dans un chemin d'erreur de S-G5** : le recensement passe avant le chargement du corpus. Si `biblio/INDEX.md` est illisible, la couverture imprime « 0 sur N présents » au lieu de « 0 sur 0 » (l'ancien retour anticipé précédait l'affectation de `presents`). Le verdict reste ROUGE. Les incidents de recensement précèdent désormais ceux de `biblio/`.
4. **Format des lignes `chemins_couverts` changé** : elles portent maintenant un compte par chemin, et l'exclusion du registre a sa propre ligne. Aucun outil n'analyse ces lignes ; seuls des documents datés citent `docs/**/*.md`.
5. **Périmètre unique** : `pub const PERIMETRE` dans `sg4.rs`, importé par `sg5.rs`. Je l'ai placé là pour rester dans la liste de fichiers du G0 ; `documents.rs` n'y figure pas.

### 6. Limites à former en items (règle PAROXYSME)

- **L-1, risque (b) du G0, constaté et déclaré.** Le recensement lit le disque, pas l'index git, et `.gitignore` l.38 ignore `s2-harness/data/` (sortie de collecte, des `.jsonl` d'après `run_campaign.py` l.237-240). Sur le poste local, que je ne peux pas vérifier d'ici, tout `.md` déposé là entrerait au périmètre : rendu redirigé dans un fichier, `.md` d'un environnement virtuel, notes.
  - Effet bénin : un ROUGE de nuisance.
  - Effet grave sous l'annexe D : S-G4 imprime la ligne fautive et S-G5 chaque fragment non contrôlé. Des lignes issues de la campagne pourraient alors paraître dans une sortie `verify` lue par un agent frais (FM-1.1).

  Item proposé : sur le poste local, avant le premier `verify` qui suit ce lot, comparer `find s2-harness -name '*.md'` et `git ls-files s2-harness`, par compte seulement. Le choix d'un recensement par l'index git relève d'une ADR, pas de moi. Même constat déjà vrai pour `docs/` : le G0 de la partie 2, non suivi, y est compté.
- **L-2.** `docs/DEVOPS.md` l.81-82, le registre des gates, dit encore S-G4 et S-G5 « dans `docs/` » : la gate est désormais plus serrée que son registre. Fichier hors de la liste du G0, non modifié.
- **L-3, constat sans item neuf.** Aujourd'hui, S-G5 ne contrôle aucun fragment de `s2-harness/` (29 fragments, tous sous le seuil). Comme le seuil s'applique avant la recherche dans le corpus (`sg5.rs`, test du seuil puis `continue`), le rejeu en corpus complet, partie (ii), ne peut rien changer pour `s2-harness/` sur le texte actuel ; il reste dû pour `docs/`. Les angles morts de S-G5 (guillemets droits et citations françaises non contrôlés, item SHOGEN-E1-XTASK-REFS-1 déjà formé) valent maintenant aussi pour le harnais.

### 7. Questions ouvertes pour l'orchestrateur

- **Q-1** : où placer `PERIMETRE` ? Dans `sg4.rs`, importé par S-G5 (choix actuel, dans la liste du G0), ou dans `documents.rs` (brique commune, hors liste) ?
- **Q-2** : acceptez-vous le changement du chemin d'erreur de S-G5 (écart 3) ?
- **Q-3** : faut-il amender DEVOPS §3 l.81-82 (L-2), dans un lot daté ?
- **Q-4** : la vérification de L-1 sur le poste local, avant d'y lancer `verify`.
- **Q-5** : gardez-vous les tests ajoutés au-delà du G0 (écart 1) ?

Toutes les sorties citées sont dans le scratchpad (`/tmp/claude-0/-home-user-shogen/7ba84933-ba6d-5813-9ef4-ca3ac4febd16/scratchpad/`), avec les copies des fichiers d'origine sous `orig/`.
