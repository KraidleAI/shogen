//! **Les mutants semés, en test permanent.**
//!
//! Doctrine gatewright, invariant 3 d'ADR-0013 : « *mutant semé tué avant tout
//! vert* — la violation que la gate existe à attraper est introduite, vue
//! mourir, restaurée, puis **committée comme test permanent**. Une gate jamais
//! exercée ainsi n'a pas de registre d'assurance. »
//!
//! Ce que ce fichier fait, à chaque exécution de `cargo test` :
//!
//! 1. construit un arbre **temporaire** (l'arbre de travail n'est jamais
//!    modifié — règle du dépôt) : copie des chemins exacts des deux rôles
//!    pour les gates de code (S-G1/2/3/7a), arbre **synthétique** pour les
//!    gates documentaires (S-G4/5/6/8 — les registres réels bougent à
//!    chaque passe, voir le commentaire de leur section) ;
//! 2. contrôle que l'arbre intact est VERT (sinon la mesure suivante ne
//!    voudrait rien dire) ;
//! 3. injecte la violation — depuis une fixture versionnée de
//!    `xtask/tests/fixtures/` pour le code Rust, en ligne pour les
//!    documents ;
//! 4. exige le ROUGE, et exige que le motif rapporté soit celui attendu ;
//! 5. l'arbre temporaire meurt avec le test.
//!
//! Registre : ces mutants sont des *mutants de gate* (ADR-0011, point 4,
//! premier registre) — **pas** de l'analyse de mutation : la population n'est
//! ni systématique ni comptée, et aucun score n'en sort. C'est un test négatif
//! de l'outil, et c'est tout ce qu'il prétend être.

use std::path::{Path, PathBuf};
use xtask::rapport::Rapport;

fn racine_depot() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .map(Path::to_path_buf)
        .expect("le manifeste xtask a un parent : la racine du dépôt")
}

fn fixture(nom: &str) -> String {
    let chemin = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("tests")
        .join("fixtures")
        .join(nom);
    std::fs::read_to_string(&chemin)
        .unwrap_or_else(|e| panic!("fixture illisible {} : {e}", chemin.display()))
}

/// Copie les chemins EXACTS sous gate dans un arbre temporaire neuf.
fn arbre_copie(nom_du_cas: &str) -> PathBuf {
    let cible = std::env::temp_dir().join(format!("shogen-mutant-{nom_du_cas}"));
    let _ = std::fs::remove_dir_all(&cible);
    let source = racine_depot();
    for relatif in ["crates/shogen-core/src", "crates/shogen-verifier/src"] {
        copier_repertoire(&source.join(relatif), &cible.join(relatif));
    }
    for relatif in [
        "crates/shogen-core/Cargo.toml",
        "crates/shogen-verifier/Cargo.toml",
    ] {
        let destination = cible.join(relatif);
        if let Some(parent) = destination.parent() {
            std::fs::create_dir_all(parent).expect("création du répertoire de copie");
        }
        std::fs::copy(source.join(relatif), destination).expect("copie du manifeste");
    }
    cible
}

fn copier_repertoire(source: &Path, cible: &Path) {
    std::fs::create_dir_all(cible).expect("création du répertoire de copie");
    for entree in std::fs::read_dir(source).expect("lecture du répertoire source") {
        let entree = entree.expect("entrée de répertoire");
        let chemin = entree.path();
        let nom = entree.file_name();
        if chemin.is_dir() {
            copier_repertoire(&chemin, &cible.join(nom));
        } else {
            std::fs::copy(&chemin, cible.join(nom)).expect("copie de fichier");
        }
    }
}

fn ajouter(racine: &Path, relatif: &str, fragment: &str) {
    let chemin = racine.join(relatif);
    let mut texte = std::fs::read_to_string(&chemin).expect("lecture du fichier à muter");
    texte.push_str(fragment);
    std::fs::write(&chemin, texte).expect("écriture du fichier muté");
}

fn ecrire(racine: &Path, relatif: &str, contenu: &str) {
    let chemin = racine.join(relatif);
    if let Some(parent) = chemin.parent() {
        std::fs::create_dir_all(parent).expect("création du répertoire");
    }
    std::fs::write(&chemin, contenu).expect("écriture du fichier");
}

fn remplacer(racine: &Path, relatif: &str, avant: &str, apres: &str) {
    let chemin = racine.join(relatif);
    let texte = std::fs::read_to_string(&chemin).expect("lecture du fichier à muter");
    assert!(
        texte.contains(avant),
        "le texte à remplacer est absent de {relatif} : {avant}"
    );
    std::fs::write(&chemin, texte.replace(avant, apres)).expect("écriture du fichier muté");
}

fn gates(racine: &Path) -> Vec<Rapport> {
    vec![
        xtask::sg1::executer(racine),
        xtask::sg2::executer(racine, false),
        xtask::sg3::executer(racine),
        xtask::sg7a::executer(racine),
    ]
}

fn rapport_de<'a>(rapports: &'a [Rapport], gate: &str) -> &'a Rapport {
    rapports
        .iter()
        .find(|rapport| rapport.gate == gate)
        .unwrap_or_else(|| panic!("rapport {gate} absent"))
}

fn motifs(rapport: &Rapport) -> String {
    rapport
        .violations
        .iter()
        .map(|violation| {
            format!(
                "{}:{} {}",
                violation.chemin, violation.ligne, violation.motif
            )
        })
        .collect::<Vec<_>>()
        .join("\n")
}

/// Contrôle préalable, sans lequel aucun rouge ne prouverait rien : l'arbre
/// copié INTACT est vert sur les quatre gates.
#[test]
fn temoin_arbre_intact_est_vert() {
    let racine = arbre_copie("temoin");
    for rapport in gates(&racine) {
        assert!(
            rapport.vert(),
            "l'arbre intact devrait être VERT sur {} :\n{}",
            rapport.gate,
            motifs(&rapport)
        );
        assert_eq!(
            rapport.examines, rapport.presents,
            "{} : couverture incomplète ({} examinés sur {} présents)",
            rapport.gate, rapport.examines, rapport.presents
        );
        assert!(rapport.presents > 0, "{} : rien d'examiné", rapport.gate);
    }
}

fn exiger_rouge(rapport: &Rapport, attendu: &str) {
    // La sortie rouge est imprimée telle quelle : `cargo test -p xtask --test
    // mutants -- --nocapture` rejoue la preuve, elle ne la résume pas.
    rapport.imprimer();
    assert!(
        !rapport.vert(),
        "{} devait être ROUGE et ne l'est pas",
        rapport.gate
    );
    let motifs = motifs(rapport);
    assert!(
        motifs.contains(attendu),
        "{} est rouge mais pour un autre motif ; attendu « {attendu} », obtenu :\n{motifs}",
        rapport.gate
    );
}

#[test]
fn mutant_sg1_nom_de_transport_en_commentaire_du_coeur() {
    let racine = arbre_copie("sg1-commentaire");
    ajouter(
        &racine,
        "crates/shogen-core/src/temoignage.rs",
        &fixture("sg1_transport_commentaire.frag"),
    );
    let rapports = gates(&racine);
    exiger_rouge(rapport_de(&rapports, "S-G1"), "nom de transport « tlsn »");
}

#[test]
fn mutant_sg1_nom_de_transport_en_constante_du_verificateur() {
    let racine = arbre_copie("sg1-constante");
    ajouter(
        &racine,
        "crates/shogen-verifier/src/main.rs",
        &fixture("sg1_transport_constante.frag"),
    );
    let rapports = gates(&racine);
    exiger_rouge(
        rapport_de(&rapports, "S-G1"),
        "nom de transport « reclaim »",
    );
}

#[test]
fn mutant_sg2_arete_du_verificateur_vers_un_adapter() {
    let racine = arbre_copie("sg2-adapter");
    ajouter(
        &racine,
        "crates/shogen-verifier/Cargo.toml",
        &fixture("sg2_arete_adapter.frag"),
    );
    let rapports = gates(&racine);
    exiger_rouge(rapport_de(&rapports, "S-G2"), "arête vers un adapter");
}

#[test]
fn mutant_sg2_horloge_dans_le_verificateur() {
    let racine = arbre_copie("sg2-horloge");
    ajouter(
        &racine,
        "crates/shogen-verifier/src/main.rs",
        &fixture("sg2_horloge.frag"),
    );
    let rapports = gates(&racine);
    exiger_rouge(
        rapport_de(&rapports, "S-G2"),
        "forme interdite « std::time »",
    );
}

#[test]
fn mutant_sg2_io_dans_le_coeur() {
    let racine = arbre_copie("sg2-io");
    ajouter(
        &racine,
        "crates/shogen-core/src/cbor.rs",
        &fixture("sg2_io_coeur.frag"),
    );
    let rapports = gates(&racine);
    exiger_rouge(
        rapport_de(&rapports, "S-G2"),
        "forme interdite « println! »",
    );
}

#[test]
fn mutant_sg3_unwrap_dans_le_coeur() {
    let racine = arbre_copie("sg3-unwrap");
    ajouter(
        &racine,
        "crates/shogen-core/src/cbor.rs",
        &fixture("sg3_unwrap.frag"),
    );
    let rapports = gates(&racine);
    exiger_rouge(
        rapport_de(&rapports, "S-G3"),
        "forme divergente « unwrap( »",
    );
}

#[test]
fn mutant_sg3_indexation_dans_le_verificateur() {
    let racine = arbre_copie("sg3-indexation");
    ajouter(
        &racine,
        "crates/shogen-verifier/src/main.rs",
        &fixture("sg3_indexation.frag"),
    );
    let rapports = gates(&racine);
    exiger_rouge(rapport_de(&rapports, "S-G3"), "indexation non contrôlée");
}

#[test]
fn mutant_sg3_arithmetique_dans_le_coeur() {
    let racine = arbre_copie("sg3-arithmetique");
    ajouter(
        &racine,
        "crates/shogen-core/src/temoignage.rs",
        &fixture("sg3_arithmetique.frag"),
    );
    let rapports = gates(&racine);
    exiger_rouge(rapport_de(&rapports, "S-G3"), "arithmétique non contrôlée");
}

#[test]
fn mutant_sg3_attribut_forbid_unsafe_retire() {
    let racine = arbre_copie("sg3-forbid");
    remplacer(
        &racine,
        "crates/shogen-verifier/src/main.rs",
        "#![forbid(unsafe_code)]\n",
        "",
    );
    let rapports = gates(&racine);
    exiger_rouge(
        rapport_de(&rapports, "S-G3"),
        "attribut « #![forbid(unsafe_code)] » absent",
    );
}

/// Mutant semé de la **scission `no_std`** (2026-08-13, échéance ADR-0009
/// point 6) : depuis que `shogen-verifier` a deux racines de compilation, un
/// `forbid(unsafe_code)` retiré de la **bibliothèque** doit rougir tout autant
/// que retiré de la coquille. Avant la scission, la gate ne regardait que
/// `main.rs` — ce test est la preuve que le trou est fermé, pas l'affirmation
/// qu'il l'est.
#[test]
fn mutant_sg3_attribut_forbid_unsafe_retire_de_la_bibliotheque() {
    let racine = arbre_copie("sg3-forbid-lib");
    remplacer(
        &racine,
        "crates/shogen-verifier/src/lib.rs",
        "#![forbid(unsafe_code)]\n",
        "",
    );
    let rapports = gates(&racine);
    exiger_rouge(
        rapport_de(&rapports, "S-G3"),
        "attribut « #![forbid(unsafe_code)] » absent",
    );
}

#[test]
fn mutant_couverture_repertoire_de_role_supprime() {
    let racine = arbre_copie("couverture-role");
    std::fs::remove_dir_all(racine.join("crates/shogen-core/src"))
        .expect("suppression du répertoire de rôle");
    let rapports = gates(&racine);
    for gate in ["S-G1", "S-G2", "S-G3"] {
        exiger_rouge(
            rapport_de(&rapports, gate),
            "répertoire absent ou illisible",
        );
    }
}

#[test]
fn mutant_couverture_fichier_neuf_dans_le_role() {
    let racine = arbre_copie("couverture-fichier");
    ecrire(
        &racine,
        "crates/shogen-core/src/sous_module/ajout.rs",
        &fixture("couverture_fichier_ajoute.frag"),
    );
    let rapports = gates(&racine);
    exiger_rouge(
        rapport_de(&rapports, "S-G3"),
        "forme divergente « unwrap( »",
    );
    assert!(
        rapport_de(&rapports, "S-G3").presents >= 6,
        "le fichier neuf doit entrer dans la couverture"
    );
}

#[test]
fn mutant_sg7a_version_non_exacte() {
    let racine = arbre_copie("sg7a-version");
    remplacer(
        &racine,
        "crates/shogen-core/Cargo.toml",
        "version = \"=1.11.0\"",
        "version = \"1.11.0\"",
    );
    let rapports = gates(&racine);
    exiger_rouge(rapport_de(&rapports, "S-G7a"), "version non exacte");
}

#[test]
fn mutant_sg2_manifeste_illisible_par_la_gate() {
    let racine = arbre_copie("sg2-manifeste");
    ajouter(
        &racine,
        "crates/shogen-verifier/Cargo.toml",
        "\n[dependencies]\nune ligne que l'analyseur ne comprend pas {\n",
    );
    let rapports = gates(&racine);
    exiger_rouge(rapport_de(&rapports, "S-G2"), "non analysable");
}

// ---------------------------------------------------------------------------
// Gates documentaires S-G4/S-G5/S-G6/S-G8 (unité orchestrateur, passe S3 —
// dette 12 §10 item 2). Les mutants tournent sur un arbre SYNTHÉTIQUE minimal,
// pas sur une copie du dépôt : les registres réels bougent à chaque passe
// (versements biblio/, lignes de journal) et un test qui exigerait leur vert
// permanent coulerait la suite à chaque acquisition — le témoin synthétique
// fixe l'état « conforme » une fois pour toutes.
// ---------------------------------------------------------------------------

/// Construit l'arbre documentaire synthétique conforme : docs/ (registre 09
/// présent + une note propre), s2-harness/ (un README propre — périmètre de
/// S-G4/S-G5 depuis SHOGEN-ORACLE-PERIMETRE-1 (i)), JOURNAL.md valide,
/// biblio/INDEX.md dont l'en-tête et les mentions concordent avec deux
/// artefacts présents.
fn arbre_documentaire(nom_du_cas: &str) -> PathBuf {
    let racine = std::env::temp_dir().join(format!("shogen-mutant-doc-{nom_du_cas}"));
    let _ = std::fs::remove_dir_all(&racine);
    ecrire(
        &racine,
        "docs/09-vocabulaire.md",
        "# registre synthétique\n\n| interdit |\n|---|\n| « donnée vérifiée » |\n",
    );
    ecrire(
        &racine,
        "docs/note.md",
        concat!(
            "# note synthétique\n\n",
            "Le registre interdit « donnée vérifiée » — la locution est ici en\n",
            "citation marquée et la voix du projet reste propre.\n\n",
            "Une citation adossée : « this quotation is present in the corpus and\n",
            "it is checked by the gate ».\n",
        ),
    );
    ecrire(
        &racine,
        "s2-harness/README.md",
        concat!(
            "# harnais synthétique\n\n",
            "Le harnais nomme « donnée vérifiée » en citation marquée.\n\n",
            "Une citation adossée : « this quotation is present in the corpus and\n",
            "it is checked by the gate ».\n",
        ),
    );
    ecrire(
        &racine,
        "JOURNAL.md",
        concat!(
            "# journal synthétique\n\n",
            "| date | unité | résultat |\n",
            "|---|---|---|\n",
            "| 2026-08-11 | première unité | rendue |\n",
            "| 2026-08-12 | seconde unité | rendue |\n",
        ),
    );
    ecrire(
        &racine,
        "biblio/INDEX.md",
        concat!(
            "# registre synthétique\n\n",
            "**2 artefacts détenus** au 2026-08-12.\n\n",
            "| fichier |\n|---|\n",
            "| `artefact-a.html` |\n",
            "| `artefact-b.txt` |\n",
        ),
    );
    ecrire(
        &racine,
        "biblio/artefact-a.html",
        "<p>this quotation is present in the corpus and it is checked by the gate</p>\n",
    );
    ecrire(&racine, "biblio/artefact-b.txt", "contenu quelconque\n");
    racine
}

fn gates_documentaires(racine: &Path) -> Vec<Rapport> {
    vec![
        xtask::sg4::executer(racine),
        xtask::sg5::executer(racine),
        xtask::sg6::executer(racine),
        xtask::sg8::executer(racine),
    ]
}

/// Témoin : l'arbre documentaire synthétique conforme est VERT sur les quatre
/// gates — y compris la locution interdite PRÉSENTE mais en citation marquée —
/// et la ligne de couverture est pleine (invariant 2 d'ADR-0013, même
/// exigence que le témoin des gates de rôle).
#[test]
fn temoin_arbre_documentaire_intact_est_vert() {
    let racine = arbre_documentaire("temoin");
    let rapports = gates_documentaires(&racine);
    for rapport in &rapports {
        assert!(
            rapport.vert(),
            "l'arbre documentaire intact devrait être VERT sur {} :\n{}",
            rapport.gate,
            motifs(rapport)
        );
        assert_eq!(
            rapport.examines, rapport.presents,
            "{} : couverture incomplète ({} examinés sur {} présents)",
            rapport.gate, rapport.examines, rapport.presents
        );
        assert!(rapport.presents > 0, "{} : rien d'examiné", rapport.gate);
    }
    // Vert pour la bonne raison : le README synthétique du harnais est
    // recensé et sa couverture imprimée, pas ignoré.
    for gate in ["S-G4", "S-G5"] {
        let couverts = rapport_de(&rapports, gate).chemins_couverts.join("\n");
        assert!(
            couverts.contains("s2-harness/**/*.md : 1 fichier(s)"),
            "{gate} doit imprimer la couverture de s2-harness/ ; chemins :\n{couverts}"
        );
    }
}

#[test]
fn mutant_sg4_locution_interdite_dans_la_voix_du_projet() {
    let racine = arbre_documentaire("sg4-locution");
    ajouter(
        &racine,
        "docs/note.md",
        "\nCette donnée vérifiée fonde le verdict.\n",
    );
    let rapports = gates_documentaires(&racine);
    exiger_rouge(rapport_de(&rapports, "S-G4"), "« donnée vérifiée »");
}

#[test]
fn mutant_sg4_guillemet_ouvert_jamais_referme() {
    let racine = arbre_documentaire("sg4-guillemet");
    ajouter(
        &racine,
        "docs/note.md",
        "\nUne « citation ouverte qui ne se referme jamais.\n",
    );
    let rapports = gates_documentaires(&racine);
    exiger_rouge(rapport_de(&rapports, "S-G4"), "jamais refermé");
}

#[test]
fn mutant_sg5_citation_hors_corpus() {
    let racine = arbre_documentaire("sg5-citation");
    ajouter(
        &racine,
        "docs/note.md",
        "\nUne citation forgée : « this quotation is not anywhere in the corpus\nand the gate must catch it ».\n",
    );
    let rapports = gates_documentaires(&racine);
    exiger_rouge(rapport_de(&rapports, "S-G5"), "citation introuvable");
}

// SHOGEN-ORACLE-PERIMETRE-1 (i) (ADR-0028 annexe B) : README et RUNBOOK de
// `s2-harness/` entrent au périmètre de S-G4 et S-G5. Chaque mutant exige le
// ROUGE pour le motif attendu ET situé dans le harnais.
fn exiger_rouge_dans_le_harnais(rapport: &Rapport, attendu: &str) {
    exiger_rouge(rapport, attendu);
    let motifs = motifs(rapport);
    assert!(
        motifs.contains("s2-harness/README.md:"),
        "{} : la violation doit être située dans le harnais ; motifs :\n{motifs}",
        rapport.gate
    );
}

#[test]
fn mutant_sg4_locution_interdite_dans_le_harnais() {
    let racine = arbre_documentaire("sg4-harnais");
    ajouter(
        &racine,
        "s2-harness/README.md",
        "\nCette donnée vérifiée fonde le verdict du harnais.\n",
    );
    let rapports = gates_documentaires(&racine);
    exiger_rouge_dans_le_harnais(rapport_de(&rapports, "S-G4"), "« donnée vérifiée »");
}

#[test]
fn mutant_sg5_citation_hors_corpus_dans_le_harnais() {
    let racine = arbre_documentaire("sg5-harnais");
    ajouter(
        &racine,
        "s2-harness/README.md",
        "\nUne citation forgée : « this sentence is not in the corpus and it\nmust be caught in the harness ».\n",
    );
    let rapports = gates_documentaires(&racine);
    exiger_rouge_dans_le_harnais(rapport_de(&rapports, "S-G5"), "citation introuvable");
}

/// Le refus sur répertoire absent tient pour le chemin neuf : supprimer
/// `s2-harness/` ne fait pas disparaître sa couverture, il rend les deux
/// gates ROUGES (même doctrine que `mutant_couverture_repertoire_de_role_supprime`).
#[test]
fn mutant_couverture_harnais_supprime() {
    let racine = arbre_documentaire("couverture-harnais");
    std::fs::remove_dir_all(racine.join("s2-harness")).expect("suppression du harnais synthétique");
    let rapports = gates_documentaires(&racine);
    for gate in ["S-G4", "S-G5"] {
        exiger_rouge(
            rapport_de(&rapports, gate),
            "répertoire absent ou illisible : s2-harness",
        );
    }
}

#[test]
fn mutant_sg6_artefact_verse_sans_entree_de_registre() {
    let racine = arbre_documentaire("sg6-non-enregistre");
    ecrire(
        &racine,
        "biblio/artefact-c.txt",
        "octets versés sans entrée\n",
    );
    let rapports = gates_documentaires(&racine);
    exiger_rouge(rapport_de(&rapports, "S-G6"), "absent du registre");
}

#[test]
fn mutant_sg6_compte_declare_en_derive() {
    // La dérive courante : un versement sans remise à jour de l'en-tête —
    // le compte déclaré est INFÉRIEUR au réel. (La direction inverse,
    // déclaré > réel avec tous les présents mentionnés, est le régime
    // « corpus partiel » : note imprimée, résidu nommé dans sg6.rs — c'est
    // le témoin `temoin_sg6_corpus_partiel…` qui la fige.)
    let racine = arbre_documentaire("sg6-compte");
    remplacer(
        &racine,
        "biblio/INDEX.md",
        "**2 artefacts détenus**",
        "**1 artefacts détenus**",
    );
    let rapports = gates_documentaires(&racine);
    exiger_rouge(rapport_de(&rapports, "S-G6"), "compte déclaré en tête (1)");
}

#[test]
fn mutant_sg8_ordre_chronologique_rompu() {
    let racine = arbre_documentaire("sg8-ordre");
    ajouter(
        &racine,
        "JOURNAL.md",
        "| 2026-08-10 | unité insérée au mauvais endroit | rendue |\n",
    );
    let rapports = gates_documentaires(&racine);
    exiger_rouge(rapport_de(&rapports, "S-G8"), "ordre chronologique rompu");
}

#[test]
fn mutant_sg8_ligne_de_journal_malformee() {
    let racine = arbre_documentaire("sg8-malforme");
    ajouter(
        &racine,
        "JOURNAL.md",
        "| 2026-08-12 | cellule manquante |\n",
    );
    let rapports = gates_documentaires(&racine);
    exiger_rouge(rapport_de(&rapports, "S-G8"), "malformée");
}

/// Témoins du régime « corpus partiel » (revue G2 du 2026-08-13, majeure 4) :
/// la branche qui transforme les violations en notes est celle qui porte la
/// promesse « un contrôle partiel qui se dit partiel » — elle se teste comme
/// le reste, sinon le vert de CI repose sur du code hors registre d'assurance.
fn arbre_documentaire_sans_octets(nom_du_cas: &str) -> PathBuf {
    let racine = arbre_documentaire(nom_du_cas);
    std::fs::remove_file(racine.join("biblio/artefact-a.html")).expect("suppression artefact a");
    std::fs::remove_file(racine.join("biblio/artefact-b.txt")).expect("suppression artefact b");
    racine
}

#[test]
fn temoin_sg5_corpus_incomplet_dit_partiel_et_liste_les_non_controles() {
    let racine = arbre_documentaire_sans_octets("sg5-partiel");
    ajouter(
        &racine,
        "docs/note.md",
        "\nUne citation forgée : « this quotation is not anywhere in the corpus\nand the gate must catch it ».\n",
    );
    let rapport = xtask::sg5::executer(&racine);
    rapport.imprimer();
    assert!(
        rapport.vert(),
        "en corpus incomplet, l'introuvable est une note, pas une violation :\n{}",
        motifs(&rapport)
    );
    let notes = rapport.notes.join("\n");
    assert!(
        notes.contains("CORPUS INCOMPLET"),
        "la note de régime partiel doit s'imprimer ; notes :\n{notes}"
    );
    assert!(
        notes.contains("this quotation is not anywhere in the corpus"),
        "chaque fragment non contrôlé doit être listé nommément ; notes :\n{notes}"
    );
}

#[test]
fn temoin_sg6_corpus_partiel_dit_partiel_sans_vert_muet() {
    let racine = arbre_documentaire_sans_octets("sg6-partiel");
    let rapport = xtask::sg6::executer(&racine);
    rapport.imprimer();
    assert!(
        rapport.vert(),
        "biblio/ sans octets = régime partiel, pas une violation :\n{}",
        motifs(&rapport)
    );
    let notes = rapport.notes.join("\n");
    assert!(
        notes.contains("compte déclaré 2") && notes.contains("non contrôlable"),
        "la note doit nommer le compte déclaré et le contrôle non tenu ; notes :\n{notes}"
    );
}

#[test]
fn mutant_sg4_guillemet_ascii_orphelin_ne_blanchit_rien_et_se_dit() {
    let racine = arbre_documentaire("sg4-ascii-orphelin");
    ajouter(
        &racine,
        "docs/note.md",
        "\nIl a dit \"bonjour, et cette donnée vérifiée fonde le verdict \"selon nous\".\n",
    );
    let rapport = xtask::sg4::executer(&racine);
    rapport.imprimer();
    assert!(!rapport.vert(), "S-G4 devait être ROUGE");
    let motifs = motifs(&rapport);
    assert!(
        motifs.contains("donnée vérifiée"),
        "la locution ne doit pas être cachée par l'appariement glouton ; motifs :\n{motifs}"
    );
    assert!(
        motifs.contains("orphelin"),
        "le guillemet ASCII orphelin doit être un incident ; motifs :\n{motifs}"
    );
}

#[test]
fn mutant_sg6_sous_repertoire_dans_biblio() {
    let racine = arbre_documentaire("sg6-sous-repertoire");
    ecrire(
        &racine,
        "biblio/sous-dossier/y.txt",
        "octets déplacés hors du plat\n",
    );
    let rapport = xtask::sg6::executer(&racine);
    rapport.imprimer();
    assert!(!rapport.vert(), "S-G6 devait être ROUGE");
    assert!(
        motifs(&rapport).contains("sous-répertoire inattendu"),
        "le sous-répertoire doit être un incident, pas un ensemble invisible ; motifs :\n{}",
        motifs(&rapport)
    );
}

#[test]
fn mutant_sg8_ligne_de_table_entierement_vide() {
    let racine = arbre_documentaire("sg8-vide");
    ajouter(&racine, "JOURNAL.md", "|  |  |  |\n");
    let rapports = gates_documentaires(&racine);
    exiger_rouge(rapport_de(&rapports, "S-G8"), "malformée");
}
