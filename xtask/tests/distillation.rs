//! Les graines distillées du corpus de fuzz (13 §7 dette 3, lot FUZZ) : chacune rend le classement
//! que son nom annonce, au jugement du vérificateur lui-même, et le corpus committé est, à l'octet,
//! ce que le générateur écrit. Arbres temporaires : `commun::Arbre`, nom unique, effacés à la fin.

mod commun;

use commun::Arbre;
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
    let racine = Arbre::nouveau("distillation", "corpus");
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

// La gate `fuzz-distillation` : seuil sur l'apport du dérivé recalculé, bornes, cartes hors forme,
// codes de sortie.

#[test]
fn seuil_471_sur_789_de_l_apport_du_derive() {
    use xtask::distillation::seuil;
    // 1074 × 471 = 505 854 ; 789 × 641 = 505 749 < 505 854 ≤ 789 × 642 = 506 538.
    assert_eq!(seuil(1074), 642);
    assert_eq!(seuil(789), 471);
    assert_eq!(seuil(100), 60, "47 100 / 789 = 59,7 : arrondi au-dessus");
}

/// Une carte au format d'`afl-showmap` (`%06u:%u`) : `n` arêtes à partir de `debut`.
fn carte(debut: u64, n: u64) -> String {
    (debut..debut + n)
        .map(|arete| format!("{arete:06}:1\n"))
        .collect()
}

#[test]
fn gate_compte_l_apport_du_derive_seul_et_refuse_un_apport_nul() {
    use xtask::distillation::{Mesure, lire_carte, seuil};
    let lire = |texte: String| lire_carte(&texte).expect("carte de forme afl-showmap");
    // Base : arêtes 0 à 9 ; le dérivé en apporte 100 de plus (10 à 109) ; seuil 60.
    let (base, derive, s) = (lire(carte(0, 10)), lire(carte(0, 110)), seuil(100));
    assert!(Mesure::de(&base, &lire(carte(0, 10 + s)), &derive).vert());
    assert!(!Mesure::de(&base, &lire(carte(0, 9 + s)), &derive).vert());
    let hors_apport = lire(carte(0, 10) + &carte(500, 100));
    assert!(
        !Mesure::de(&base, &hors_apport, &derive).vert(),
        "gain hors de l'apport compté"
    );
    let perdue = lire(carte(1, 10 + s));
    assert!(
        !Mesure::de(&base, &perdue, &derive).vert(),
        "arête 0 perdue"
    );
    let tout = lire(carte(0, 110));
    assert!(
        !Mesure::de(&base, &tout, &base).vert(),
        "apport du dérivé nul"
    );
}

#[test]
fn apport_compte_en_ensemble_quand_le_derive_manque_des_aretes_de_la_base() {
    use xtask::distillation::{Mesure, lire_carte, seuil};
    let lire = |texte: String| lire_carte(&texte).expect("carte de forme afl-showmap");
    // Base 0 à 9 ; dérivé 5 à 109, sans les arêtes 0 à 4 de la base (mesure réelle : 3 arêtes de
    // la base hors du dérivé). E = 10 à 109, 100 arêtes, seuil 60 ; |dérivé| − |base| donnerait 57.
    let (base, derive) = (lire(carte(0, 10)), lire(carte(5, 105)));
    let mesure = Mesure::de(&base, &lire(carte(0, 10 + 59)), &derive);
    assert_eq!((mesure.apport, seuil(mesure.apport)), (100, 60));
    assert!(!mesure.vert(), "59 arêtes gagnées dans E, sous le seuil 60");
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
    let dossier = Arbre::nouveau("distillation", "cartes");
    std::fs::create_dir_all(&dossier).expect("dossier des cartes");
    let seuil = xtask::distillation::seuil(100);
    let cartes = [
        ("base", 10),
        ("derive", 110),
        ("verte", 10 + seuil),
        ("rouge", 9 + seuil),
    ];
    for (nom, n) in cartes {
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
    assert_eq!(code(&["base", "verte", "derive"]), Some(0));
    assert_eq!(code(&["base", "rouge", "derive"]), Some(1));
    assert_eq!(code(&["base", "verte", "absente"]), Some(1));
    assert_eq!(code(&["base", "verte"]), Some(64));
    assert_eq!(code(&["base", "verte", "derive", "derive"]), Some(64));
}
