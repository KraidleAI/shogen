#![forbid(unsafe_code)]
#![deny(
    clippy::unwrap_used,
    clippy::expect_used,
    clippy::panic,
    clippy::indexing_slicing,
    clippy::arithmetic_side_effects
)]
//! Vérificateur offline — la **coquille impérative** du walking skeleton
//! (ADR-0010, point 4 : « I/O, lecture d'arguments : binaire CLI »).
//!
//! Ce qu'il fait, et rien de plus : lit un fichier d'octets, le décode par le
//! cœur, ré-encode, compare — puis **nomme son résidu**. Il ne réclame aucune
//! capacité qu'il n'exerce : ni réseau, ni horloge, ni aléa (ADR-0010, point 8 ;
//! gate S-G2). Il ne sait pas écrire : produire un lot d'exemple est le travail
//! de `cargo xtask emettre-exemple`, pas le sien.
//!
//! Fail-closed (ADR-0010, point 5) : tout octet muté, tronqué, en trop ou non
//! canonique donne un code de sortie non nul et une **erreur nommée**.

use shogen_core::{decoder_temoignage, encoder_temoignage};

/// Lot conforme au sous-ensemble canonique.
const CODE_CONFORME: i32 = 0;
/// Usage : le vérificateur attend exactement un chemin.
const CODE_USAGE: i32 = 64;
/// Le fichier n'a pas pu être lu.
const CODE_LECTURE: i32 = 66;
/// Le décodage a refusé le lot (erreur nommée du cœur).
const CODE_DECODAGE: i32 = 2;
/// Le lot décode, mais son ré-encodage diffère : il n'était pas canonique.
const CODE_ROUND_TRIP: i32 = 3;

/// Verdict et résidu, en toutes lettres. La conformité est une propriété des
/// **octets**, pas du monde : ADR-0001 (Shōgen ne construit aucun transport et
/// ne juge pas la vérité d'une source).
const VERDICT_CONFORME: &str = "VERDICT : octets conformes au sous-ensemble canonique ; résidu : la conformité ne dit rien de la vérité de la source — ADR-0001";

fn main() {
    std::process::exit(executer());
}

fn executer() -> i32 {
    let mut arguments = std::env::args_os().skip(1);
    let chemin = match arguments.next() {
        Some(chemin) => chemin,
        None => {
            usage();
            return CODE_USAGE;
        }
    };
    if arguments.next().is_some() {
        usage();
        return CODE_USAGE;
    }

    let affichage = chemin.to_string_lossy().into_owned();
    let octets = match std::fs::read(&chemin) {
        Ok(octets) => octets,
        Err(erreur) => {
            eprintln!("VERDICT : refusé (fail-closed)");
            eprintln!("  erreur nommée : lot illisible « {affichage} » : {erreur}");
            return CODE_LECTURE;
        }
    };

    println!("shogen-verifier — lot : {affichage}");
    println!("  octets lus : {}", octets.len());
    println!("  tête du lot : {}", tete_hexadecimale(&octets));

    let temoignage = match decoder_temoignage(&octets) {
        Ok(temoignage) => temoignage,
        Err(erreur) => {
            eprintln!("VERDICT : refusé (fail-closed)");
            eprintln!("  erreur nommée : {erreur}");
            eprintln!("  variante : {erreur:?}");
            return CODE_DECODAGE;
        }
    };

    let reencode = encoder_temoignage(&temoignage);
    if reencode.as_slice() != octets.as_slice() {
        eprintln!("VERDICT : refusé (fail-closed)");
        eprintln!(
            "  erreur nommée : ré-encodage divergent — le lot décode mais n'est pas sa propre forme canonique"
        );
        eprintln!("    octets du lot     : {}", octets.len());
        eprintln!("    octets ré-encodés : {}", reencode.len());
        eprintln!(
            "    première divergence : {}",
            premiere_divergence(&octets, &reencode)
        );
        return CODE_ROUND_TRIP;
    }

    println!("  décodage : accepté (sous-ensemble canonique CBOR, RFC 8949 — ADR-0002)");
    println!(
        "  ré-encodage : {} octets, identiques au lot (round-trip exact)",
        reencode.len()
    );
    println!("  source : « {} »", temoignage.source);
    println!(
        "  instant porté : {} (donnée du lot, aucune horloge lue)",
        temoignage.instant
    );
    println!("  contenu : {} octet(s)", temoignage.contenu.len());
    println!("{VERDICT_CONFORME}");
    CODE_CONFORME
}

fn usage() {
    eprintln!("usage : shogen-verifier <chemin-du-lot>");
    eprintln!("  vérifie qu'un lot est un témoignage trivial en forme canonique.");
}

/// Rend les premiers octets en hexadécimal, pour qu'un refus soit
/// diagnosticable sans outil tiers.
fn tete_hexadecimale(octets: &[u8]) -> String {
    let mut rendu = String::new();
    for octet in octets.iter().copied().take(16) {
        rendu.push_str(&format!("{octet:02x}"));
    }
    if octets.len() > 16 {
        rendu.push('…');
    }
    rendu
}

/// Position du premier octet divergent, ou une mention de longueur.
fn premiere_divergence(gauche: &[u8], droite: &[u8]) -> String {
    let position = gauche
        .iter()
        .copied()
        .zip(droite.iter().copied())
        .position(|(a, b)| a != b);
    match position {
        Some(position) => format!("octet {position}"),
        None => String::from("aucune sur le préfixe commun — les longueurs diffèrent"),
    }
}
