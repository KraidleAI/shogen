//! **La coquille du binaire** — arguments, fichiers de contexte, et la
//! politique de rétention des octets.
//!
//! Rattachement (G0) : **ADR-0010** point 4 (« I/O, lecture d'arguments :
//! binaire CLI » — la coquille ne décide rien, mais elle refuse) et point 5
//! (*fail-safe defaults*) ; **ADR-0005 règle 2** (la rétention des octets est
//! une politique de classe : un témoignage peut ne porter que le hash) ;
//! **ADR-0011** seuil 7 (la cible fuzz est une fonction publique, éprouvée ici
//! sur quelques suites d'octets — le budget, lui, est au job dédié).
//!
//! Ces cas ne mesurent pas la logique de vérification : ils mesurent que la
//! coquille refuse **ce qu'elle ne peut pas exécuter**, au lieu de deviner.

use std::path::{Path, PathBuf};
use std::process::Command;

const CODE_USAGE: i32 = 64;
const CODE_CONTEXTE: i32 = 65;

fn fixtures() -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("tests")
        .join("fixtures")
}

fn lot_reel() -> Vec<u8> {
    std::fs::read(fixtures().join("s3-binance.lot.cbor")).expect("le lot réel est versionné")
}

fn repertoire(nom: &str) -> PathBuf {
    let chemin = std::env::temp_dir().join(format!("shogen-coquille-{nom}-{}", std::process::id()));
    let _ = std::fs::remove_dir_all(&chemin);
    std::fs::create_dir_all(&chemin).expect("création du répertoire de test");
    chemin
}

fn executer(arguments: &[&Path]) -> (i32, String, String) {
    let sortie = Command::new(env!("CARGO_BIN_EXE_shogen-verifier"))
        .args(arguments)
        .output()
        .expect("le binaire du vérificateur doit s'exécuter");
    (
        sortie.status.code().unwrap_or(-1),
        String::from_utf8_lossy(&sortie.stdout).into_owned(),
        String::from_utf8_lossy(&sortie.stderr).into_owned(),
    )
}

// ---------------------------------------------------------------------------
// Les arguments : chaque forme fautive a son refus
// ---------------------------------------------------------------------------

#[test]
fn une_option_donnee_deux_fois_est_refusee() {
    let registre = fixtures().join("s3-binance.registre.txt");
    let lot = repertoire("option-double").join("lot.cbor");
    std::fs::write(&lot, lot_reel()).expect("écriture du lot");
    let (code, _, erreur) = executer(&[
        lot.as_path(),
        Path::new("--registre"),
        &registre,
        Path::new("--registre"),
        &registre,
    ]);
    assert_eq!(code, CODE_USAGE, "{erreur}");
    assert!(erreur.contains("donnée deux fois"), "{erreur}");
}

#[test]
fn un_constat_donne_deux_fois_est_refuse() {
    let constat = fixtures().join("s3-binance.constat.json");
    let lot = repertoire("constat-double").join("lot.cbor");
    std::fs::write(&lot, lot_reel()).expect("écriture du lot");
    let (code, _, erreur) = executer(&[
        lot.as_path(),
        Path::new("--constat"),
        &constat,
        Path::new("--constat"),
        &constat,
    ]);
    assert_eq!(code, CODE_USAGE, "{erreur}");
    assert!(erreur.contains("donnée deux fois"), "{erreur}");
}

#[test]
fn une_option_inconnue_est_refusee() {
    let lot = repertoire("option-inconnue").join("lot.cbor");
    std::fs::write(&lot, lot_reel()).expect("écriture du lot");
    let (code, _, erreur) = executer(&[lot.as_path(), Path::new("--verbeux")]);
    assert_eq!(code, CODE_USAGE, "{erreur}");
    assert!(erreur.contains("option inconnue"), "{erreur}");
}

#[test]
fn deux_lots_a_la_fois_sont_refuses() {
    let repertoire = repertoire("deux-lots");
    let lot = repertoire.join("lot.cbor");
    std::fs::write(&lot, lot_reel()).expect("écriture du lot");
    let (code, _, erreur) = executer(&[lot.as_path(), lot.as_path()]);
    assert_eq!(code, CODE_USAGE, "{erreur}");
    assert!(erreur.contains("un seul lot à la fois"), "{erreur}");
}

#[test]
fn une_option_privee_de_sa_valeur_est_refusee() {
    let lot = repertoire("option-sans-valeur").join("lot.cbor");
    std::fs::write(&lot, lot_reel()).expect("écriture du lot");
    let (code, _, erreur) = executer(&[lot.as_path(), Path::new("--constat")]);
    assert_eq!(code, CODE_USAGE, "{erreur}");
    assert!(erreur.contains("attend un chemin"), "{erreur}");
}

// ---------------------------------------------------------------------------
// Les fichiers de contexte : illisibles, donc non conclus
// ---------------------------------------------------------------------------

#[test]
fn un_registre_illisible_est_un_refus_de_contexte() {
    let repertoire = repertoire("registre-illisible");
    let lot = repertoire.join("lot.cbor");
    std::fs::write(&lot, lot_reel()).expect("écriture du lot");
    let (code, _, erreur) = executer(&[
        lot.as_path(),
        Path::new("--registre"),
        &repertoire.join("absent.txt"),
    ]);
    assert_eq!(code, CODE_CONTEXTE, "{erreur}");
    assert!(erreur.contains("registre illisible"), "{erreur}");
}

#[test]
fn un_constat_illisible_est_un_refus_de_contexte() {
    let repertoire = repertoire("constat-illisible");
    let lot = repertoire.join("lot.cbor");
    std::fs::write(&lot, lot_reel()).expect("écriture du lot");
    let (code, _, erreur) = executer(&[
        lot.as_path(),
        Path::new("--registre"),
        &fixtures().join("s3-binance.registre.txt"),
        Path::new("--constat"),
        &repertoire.join("absent.json"),
    ]);
    assert_eq!(code, CODE_CONTEXTE, "{erreur}");
    assert!(erreur.contains("constat illisible"), "{erreur}");
}

// ---------------------------------------------------------------------------
// ADR-0005 règle 2 — le témoignage qui ne porte que son hash
// ---------------------------------------------------------------------------

/// Le lot réel **privé de ses octets portés** : `utterance` ne garde que son
/// empreinte, la carte passe de deux entrées à une.
///
/// C'est la politique de classe d'ADR-0005 règle 2, et le verdict doit dire ce
/// qu'il n'a PAS recalculé — un verdict qui tairait la différence laisserait
/// croire que la liaison interne a été refaite.
fn lot_sans_octets_portes() -> Vec<u8> {
    let lot = lot_reel();
    let mut aiguille = vec![0x69u8];
    aiguille.extend_from_slice(b"utterance");
    aiguille.push(0xa2); // carte(2)
    let debut = lot
        .windows(aiguille.len())
        .position(|fenetre| fenetre == aiguille.as_slice())
        .expect("la sous-carte utterance figure dans le lot");
    let position_carte = debut + aiguille.len() - 1;

    // `bytes` et ses 944 octets : de l'en-tête de clé à la fin de la chaîne.
    let mut aiguille_bytes = vec![0x65u8];
    aiguille_bytes.extend_from_slice(b"bytes");
    aiguille_bytes.extend_from_slice(&[0x59, 0x03, 0xB0]); // 944 octets
    let debut_bytes = lot
        .windows(aiguille_bytes.len())
        .position(|fenetre| fenetre == aiguille_bytes.as_slice())
        .expect("les octets portés figurent dans le lot");
    let fin_bytes = debut_bytes + aiguille_bytes.len() + 944;

    let mut ampute: Vec<u8> = Vec::new();
    ampute.extend_from_slice(&lot[..position_carte]);
    ampute.push(0xa1); // carte(1) — `hash` seul
    ampute.extend_from_slice(&lot[position_carte + 1..debut_bytes]);
    ampute.extend_from_slice(&lot[fin_bytes..]);
    ampute
}

#[test]
fn un_temoignage_sans_octets_portes_est_valide_et_le_verdict_le_dit() {
    let repertoire = repertoire("sans-octets");
    let lot = repertoire.join("lot.cbor");
    std::fs::write(&lot, lot_sans_octets_portes()).expect("écriture du lot");
    let (code, sortie, erreur) = executer(&[
        lot.as_path(),
        Path::new("--registre"),
        &fixtures().join("s3-binance.registre.txt"),
        Path::new("--constat"),
        &fixtures().join("s3-binance.constat.json"),
    ]);
    assert_eq!(
        code, 0,
        "un témoignage à hash seul est licite (ADR-0005 règle 2)\nstdout:{sortie}\nstderr:{erreur}"
    );
    assert!(
        sortie.contains("octets non portés"),
        "le verdict doit dire ce qu'il n'a PAS recalculé : {sortie}"
    );
    assert!(
        sortie.contains("VERDICT : valide sous A(notary-neutrality)"),
        "{sortie}"
    );
}

// ---------------------------------------------------------------------------
// La cible fuzz — exercée ici sur quelques suites, budgetée ailleurs
// ---------------------------------------------------------------------------

#[test]
fn la_cible_fuzz_traverse_les_trois_surfaces_sans_diverger() {
    // `eprouver` est la fonction que les moteurs consomment (ADR-0011 seuil 7).
    // Ce test n'établit AUCUN seuil : les budgets (≥ 15 min CI, ≥ 4 h nightly)
    // vivent dans les jobs dédiés. Il établit que la cible reste appelable et
    // qu'elle traverse ses trois surfaces sur des entrées connues — un
    // changement de signature ou un chemin qui divergerait tomberait ici, à la
    // seconde, plutôt qu'au bout d'un budget.
    let cas: Vec<Vec<u8>> = vec![
        Vec::new(),
        vec![0xBF],
        lot_reel(),
        std::fs::read(fixtures().join("s3-binance.constat.json")).expect("constat versionné"),
        std::fs::read(fixtures().join("s3-binance.registre.txt")).expect("registre versionné"),
        b"A(notary-neutrality)\n".to_vec(),
        vec![0xff, 0xfe, 0xfd],
    ];
    for octets in &cas {
        shogen_verifier::eprouver(octets);
    }
    println!(
        "cible fuzz : {} suite(s) d'octets traversées, 0 divergence",
        cas.len()
    );
}
