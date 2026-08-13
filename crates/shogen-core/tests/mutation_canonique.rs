//! **Octet muté ⇒ erreur nommée, jamais panique** — sur le `subject` et sur le
//! lot canonique.
//!
//! Registre : *octet muté du lot*, le troisième registre de « semé » d'ADR-0011
//! point 4. Ce n'est ni un mutant de gate ni de l'analyse de mutation : c'est un
//! **test négatif de données**, et aucun score n'en sort.
//!
//! Ce que ces tests établissent exactement : pour **chaque position** et
//! **chaque valeur d'octet**, le prédicat et le décodeur rendent soit une erreur
//! nommée, soit une valeur dont le ré-encodage redonne exactement les octets
//! mutés. Aucune troisième issue — ni panique, ni acceptation d'octets non
//! canoniques.
//!
//! Ce qu'ils n'établissent pas : rien sur les mutations de plusieurs octets. La
//! propriété générale est portée par `subject_proprietes.rs` (propriété (c)), et
//! le fuzz reste dû (ADR-0011, seuil 7).

use shogen_core::{
    decoder_temoignage_canonique, encoder_temoignage_canonique, subject_est_canonique,
};

mod commun;

/// Le `subject` de référence — celui de `subject_canonique.rs`.
const SUBJECT: &str = "https://api.example.com/v3/simple/price?ids=bitcoin&vs_currencies=usd";

#[test]
fn chaque_octet_mute_du_subject_donne_un_refus_nomme_ou_reste_canonique() {
    let origine = SUBJECT.as_bytes().to_vec();
    let mut refuses = 0usize;
    let mut acceptes = 0usize;
    let mut essais = 0usize;

    for position in 0..origine.len() {
        for valeur in 0u16..=255 {
            let valeur = valeur as u8;
            if origine[position] == valeur {
                continue;
            }
            let mut mute = origine.clone();
            mute[position] = valeur;
            essais += 1;
            match subject_est_canonique(&mute) {
                Err(erreur) => {
                    let rendu = format!("{erreur}");
                    assert!(
                        !rendu.trim().is_empty(),
                        "erreur muette à la position {position}, valeur {valeur}"
                    );
                    refuses += 1;
                }
                Ok(()) => {
                    // Un subject accepté après mutation est un AUTRE subject
                    // canonique — c'est licite, et c'est exactement ce que le
                    // hash d'utterance, lui, ne laisse pas passer.
                    assert!(mute.is_ascii(), "accepté mais non ASCII");
                    acceptes += 1;
                }
            }
        }
    }

    println!(
        "mutation d'un octet du subject — {} positions × 255 valeurs : {essais} essais, \
         {refuses} refus nommés, {acceptes} acceptés canoniques (0 panique)",
        origine.len()
    );
    assert_eq!(refuses + acceptes, essais);
    assert!(
        refuses > 0,
        "aucun refus : le prédicat serait trop tolérant"
    );
    assert!(
        acceptes > 0,
        "aucune acceptation : le prédicat serait trop strict, et le test ne dirait rien du chemin d'acceptation"
    );
}

#[test]
fn chaque_octet_mute_du_lot_canonique_donne_un_refus_nomme_ou_un_lot_canonique() {
    let origine = encoder_temoignage_canonique(&commun::reference());
    let mut refuses = 0usize;
    let mut acceptes_canoniques = 0usize;
    let mut essais = 0usize;

    for position in 0..origine.len() {
        for valeur in 0u16..=255 {
            let valeur = valeur as u8;
            if origine[position] == valeur {
                continue;
            }
            let mut mute = origine.clone();
            mute[position] = valeur;
            essais += 1;
            match decoder_temoignage_canonique(&mute) {
                Err(erreur) => {
                    let rendu = format!("{erreur}");
                    assert!(
                        !rendu.trim().is_empty(),
                        "erreur muette à la position {position}, valeur {valeur}"
                    );
                    refuses += 1;
                }
                Ok(temoignage) => {
                    let reencode = encoder_temoignage_canonique(&temoignage);
                    assert_eq!(
                        reencode, mute,
                        "octet {position} := {valeur} : accepté mais NON canonique — \
                         deux suites d'octets distinctes donneraient le même fait"
                    );
                    acceptes_canoniques += 1;
                }
            }
        }
    }

    println!(
        "mutation d'un octet du lot canonique — {} positions × 255 valeurs : {essais} essais, \
         {refuses} refus nommés, {acceptes_canoniques} acceptés canoniques (0 panique)",
        origine.len()
    );
    assert_eq!(refuses + acceptes_canoniques, essais);
    assert!(refuses > 0);
}
