//! Les graines distillées du corpus de fuzz (13 §7 dette 3, lot FUZZ) : chacune rend le classement
//! que son nom annonce, au jugement du vérificateur lui-même, et le corpus committé est, à l'octet,
//! ce que le générateur écrit. Arbre temporaire sous `CARGO_TARGET_TMPDIR`, propre à la cible cargo.

use std::collections::BTreeMap;
use std::path::{Path, PathBuf};
use xtask::fuzz::{CORPUS, ecrire_corpus_dirige};

/// L'oracle : les trois surfaces du vérificateur, jamais le générateur.
fn classement(octets: &[u8]) -> String {
    let lot = format!("{:?}", shogen_verifier::examiner_lot(octets));
    match std::str::from_utf8(octets) {
        Ok(texte) => format!(
            "{lot} | {:?} | {:?}",
            shogen_verifier::analyser_constat(texte),
            shogen_verifier::analyser_registre(texte).map(|identifiants| identifiants.len())
        ),
        Err(_) => lot,
    }
}

#[test]
fn chaque_graine_distillee_rend_le_classement_que_son_nom_annonce() {
    let fautes: Vec<String> = xtask::distillation::graines()
        .iter()
        .map(|graine| (graine, classement(&graine.octets)))
        .filter(|(graine, rendu)| !rendu.contains(graine.attendu))
        .map(|(graine, rendu)| {
            format!("{} : attendu {}, rendu {rendu}", graine.nom, graine.attendu)
        })
        .collect();
    assert!(fautes.is_empty(), "{}", fautes.join("\n"));
}

/// Les graines `dirigee-*` d'un corpus, par nom.
fn graines_dirigees(corpus: &Path) -> BTreeMap<String, Vec<u8>> {
    let mut graines = BTreeMap::new();
    for entree in std::fs::read_dir(corpus).expect("corpus lisible") {
        let chemin = entree.expect("entrée lisible").path();
        let nom = chemin.file_name().map(|n| n.to_string_lossy().into_owned());
        if let Some(nom) = nom.filter(|nom| nom.starts_with("dirigee-")) {
            graines.insert(nom, std::fs::read(&chemin).expect("graine lisible"));
        }
    }
    graines
}

#[test]
fn le_corpus_committe_est_ce_que_le_generateur_ecrit_graines_distinctes() {
    let racine = PathBuf::from(env!("CARGO_TARGET_TMPDIR")).join("distillation-corpus");
    let _ = std::fs::remove_dir_all(&racine);
    ecrire_corpus_dirige(&racine).expect("corpus dirigé écrit");
    let ecrites = graines_dirigees(&racine.join(CORPUS));
    let depot = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("..")
        .join(CORPUS);
    assert!(
        ecrites == graines_dirigees(&depot),
        "corpus committé ≠ corpus régénéré"
    );
    let mut octets: Vec<&Vec<u8>> = ecrites.values().collect();
    octets.sort();
    octets.dedup();
    assert_eq!(
        octets.len(),
        ecrites.len(),
        "deux graines dirigées portent les mêmes octets"
    );
    assert!(
        ecrites
            .keys()
            .any(|nom| nom.starts_with("dirigee-distillee-"))
    );
}

// La gate `fuzz-distillation` : seuil, bornes, cartes hors forme, codes de sortie.

#[test]
fn seuil_de_la_gate_642_aretes() {
    // 1074 × 471 = 505 854 ; 789 × 641 = 505 749 < 505 854 ≤ 789 × 642 = 506 538.
    assert_eq!(xtask::distillation::seuil(), 642);
}

/// Une carte au format d'`afl-showmap` (`%06u:%u`) : `n` arêtes à partir de `debut`.
fn carte(debut: u64, n: u64) -> String {
    (debut..debut + n)
        .map(|arete| format!("{arete:06}:1\n"))
        .collect()
}

#[test]
fn gate_verte_au_seuil_rouge_dessous_et_sur_base_perdue() {
    use xtask::distillation::{Mesure, lire_carte, seuil};
    let lire = |texte: String| lire_carte(&texte).expect("carte de forme afl-showmap");
    let base = lire(carte(0, 10));
    assert!(Mesure::de(&base, &lire(carte(0, 10 + seuil()))).vert());
    assert!(!Mesure::de(&base, &lire(carte(0, 9 + seuil()))).vert());
    assert!(
        !Mesure::de(&base, &lire(carte(1, 10 + seuil()))).vert(),
        "arête 0 perdue"
    );
}

#[test]
fn carte_hors_forme_refusee() {
    // Chaque faute suit une ligne valide : une ligne fautive sautée ne passerait pas pour une carte vide.
    assert!(
        xtask::distillation::lire_carte("").is_err(),
        "carte vide acceptée"
    );
    for faute in ["abc", "000012", "000012:0", "000001:2", "1:1:2", "-1:1"] {
        let texte = format!("000001:1\n{faute}\n");
        assert!(
            xtask::distillation::lire_carte(&texte).is_err(),
            "{texte:?} accepté"
        );
    }
    let lue = xtask::distillation::lire_carte("000068:1\n000124:128\n").expect("carte valide");
    assert_eq!(lue.into_iter().collect::<Vec<_>>(), [68, 124]);
}

#[test]
fn commande_rend_0_vert_1_rouge_ou_illisible_64_usage() {
    let dossier = PathBuf::from(env!("CARGO_TARGET_TMPDIR")).join("distillation-cartes");
    std::fs::create_dir_all(&dossier).expect("dossier des cartes");
    let seuil = xtask::distillation::seuil();
    for (nom, n) in [("base", 10), ("verte", 10 + seuil), ("rouge", 9 + seuil)] {
        std::fs::write(dossier.join(nom), carte(0, n)).expect("carte écrite");
    }
    let code = |arguments: &[&str]| {
        std::process::Command::new(env!("CARGO_BIN_EXE_xtask"))
            .arg("fuzz-distillation")
            .args(arguments.iter().map(|nom| dossier.join(nom)))
            .status()
            .expect("xtask lancé")
            .code()
    };
    assert_eq!(code(&["base", "verte"]), Some(0));
    assert_eq!(code(&["base", "rouge"]), Some(1));
    assert_eq!(code(&["base", "absente"]), Some(1));
    assert_eq!(code(&["base"]), Some(64));
}
