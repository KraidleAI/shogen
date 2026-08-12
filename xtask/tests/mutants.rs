//! **Les mutants semés, en test permanent.**
//!
//! Doctrine gatewright, invariant 3 d'ADR-0013 : « *mutant semé tué avant tout
//! vert* — la violation que la gate existe à attraper est introduite, vue
//! mourir, restaurée, puis **committée comme test permanent**. Une gate jamais
//! exercée ainsi n'a pas de registre d'assurance. »
//!
//! Ce que ce fichier fait, à chaque exécution de `cargo test` :
//!
//! 1. copie les chemins exacts des deux rôles dans un arbre **temporaire**
//!    (l'arbre de travail n'est jamais modifié — règle du dépôt) ;
//! 2. contrôle que l'arbre copié intact est VERT (sinon la mesure suivante ne
//!    voudrait rien dire) ;
//! 3. injecte la violation, depuis une fixture versionnée de
//!    `xtask/tests/fixtures/` ;
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

#[test]
fn mutant_couverture_repertoire_de_role_supprime() {
    let racine = arbre_copie("couverture-role");
    std::fs::remove_dir_all(racine.join("crates/shogen-core/src"))
        .expect("suppression du répertoire de rôle");
    let rapports = gates(&racine);
    for gate in ["S-G1", "S-G2", "S-G3"] {
        exiger_rouge(rapport_de(&rapports, gate), "répertoire de rôle absent");
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
