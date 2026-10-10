//! Les arbres temporaires des tests (SHOGEN-XTASK-TMP-NOMS-FIXES-1) : nom unique sous la cible cargo,
//! effacés à la fin, panique comprise ; aucun test ne compose plus de chemin temporaire à la main.

mod commun;

use commun::Arbre;
use std::path::PathBuf;

#[test]
fn arbre_unique_sous_la_cible_et_efface_a_la_fin_panique_comprise() {
    let (a, b) = (
        Arbre::nouveau("essai", "cas"),
        Arbre::nouveau("essai", "cas"),
    );
    assert_ne!(*a, *b, "deux arbres du même cas partagent un chemin");
    assert!(a.starts_with(env!("CARGO_TARGET_TMPDIR")));
    let nom = a.file_name().map(|n| n.to_string_lossy().into_owned());
    let processus = std::process::id().to_string();
    assert!(
        nom.is_some_and(|n| n.contains(&processus)),
        "nom sans le processus"
    );
    std::fs::create_dir_all(a.join("x/y")).expect("arbre créé");
    let chemin = a.to_path_buf();
    drop(a);
    assert!(!chemin.exists(), "arbre laissé après le test");
    let mut garde = PathBuf::new();
    let _ = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
        let c = Arbre::nouveau("essai", "panique");
        std::fs::create_dir_all(c.join("x")).expect("arbre créé");
        garde = c.to_path_buf();
        panic!("panique voulue");
    }));
    assert!(
        !garde.as_os_str().is_empty() && !garde.exists(),
        "arbre laissé par une panique"
    );
    drop(b);
}

#[test]
fn arbre_sur_un_reste_le_vide_d_abord() {
    let chemin = PathBuf::from(env!("CARGO_TARGET_TMPDIR")).join(format!(
        "essai-reste-d-un-processus-tue-{}",
        std::process::id()
    ));
    std::fs::create_dir_all(chemin.join("vieux")).expect("reste posé");
    let arbre = Arbre::sur(chemin.clone());
    assert!(
        !arbre.join("vieux").exists(),
        "reste d'un processus tué gardé"
    );
}

#[test]
fn aucun_test_ne_compose_de_chemin_temporaire_a_la_main() {
    let dossier = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tests");
    let mut lus = 0;
    for entree in std::fs::read_dir(&dossier).expect("tests lisibles") {
        let chemin = entree.expect("entrée lisible").path();
        let nom = chemin.file_name().map(|n| n.to_string_lossy().into_owned());
        if chemin.extension().is_some_and(|e| e == "rs") && nom.as_deref() != Some("arbres.rs") {
            let source = std::fs::read_to_string(&chemin).expect("source lisible");
            for motif in ["temp_dir()", "CARGO_TARGET_TMPDIR"] {
                assert!(
                    !source.contains(motif),
                    "{} : {motif} hors de commun::Arbre",
                    chemin.display()
                );
            }
            lus += 1;
        }
    }
    assert!(lus >= 3, "{lus} fichier(s) de test lus");
}
