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
