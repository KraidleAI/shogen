//! **Property-based sur le cœur pur** — ADR-0011, point 2.
//!
//! Les trois propriétés dues en S2.5 (la quatrième, (d), naît avec le calcul de
//! partition en S3/S4 et n'a rien à faire ici) :
//!
//! * **(a) round-trip de la forme canonique** — `decode(encode(x)) == x` pour
//!   tout fait `x`, et `encode(decode(b)) == b` pour tout `b` accepté ;
//! * **(b) unicité de représentation** — deux chemins d'encodage d'un même fait
//!   donnent les mêmes octets, et deux faits distincts ne partagent jamais un
//!   encodage (injectivité) ;
//! * **(c) totalité** — aucune suite d'octets ne fait diverger le décodeur ; le
//!   pendant *tested* de S-G3, qui est lexicale et ne dit rien du binaire sur
//!   une entrée hostile.
//!
//! Les trois obligations d'exécution d'ADR-0011, point 2, sont tenues ici :
//!
//! 1. **graine consignée, rejeu exact** — le générateur est un `TestRng`
//!    déterministe (`RngAlgorithm::ChaCha`, graine par défaut fixe) : la même
//!    commande rejoue les mêmes cas, sur Windows comme sur Linux. La
//!    persistance de fichier de régression est désactivée exprès : un fichier
//!    d'état caché serait une seconde source de vérité ;
//! 2. **distribution imprimée AVANT le verdict** — chaque propriété imprime sa
//!    classification, et la part de cas non triviaux est une **assertion**
//!    (seuil 6 d'ADR-0011 : ≥ 50 %, candidat — ratification due) ;
//! 3. **tout contre-exemple devient un test permanent nommé** — à écrire dans
//!    `canonique.rs`, à la main, dans la même unité de travail que le
//!    correctif.
//!
//! Registre d'assurance : *tested (avec compte)*. Jamais *proven*.

use proptest::prelude::*;
use proptest::test_runner::{Config, RngAlgorithm, TestRng, TestRunner};
use shogen_core::{TemoignageTrivial, decoder_temoignage, encoder_temoignage};
use std::cell::Cell;

/// Seuil 5 d'ADR-0011 : ≥ 1 000 cas par propriété en CI (candidat).
const CAS: u32 = 1_000;
/// Seuil 6 d'ADR-0011 : ≥ 50 % de cas non triviaux (candidat).
const PART_NON_TRIVIALE_MINIMALE: f64 = 0.50;

/// Alphabet fixe, ASCII et non ASCII : le chemin UTF-8 du décodeur doit être
/// exercé, pas seulement le chemin `[a-z]`.
const ALPHABET: [char; 8] = ['a', 'z', '0', ':', '-', 'é', '漢', '🙂'];

fn executeur() -> TestRunner {
    let configuration = Config {
        cases: CAS,
        failure_persistence: None,
        ..Config::default()
    };
    TestRunner::new_with_rng(
        configuration,
        TestRng::deterministic_rng(RngAlgorithm::ChaCha),
    )
}

fn strategie_texte() -> impl Strategy<Value = String> {
    proptest::collection::vec(0usize..ALPHABET.len(), 0..24)
        .prop_map(|indices| indices.into_iter().map(|i| ALPHABET[i]).collect())
}

fn strategie_temoignage() -> impl Strategy<Value = TemoignageTrivial> {
    (
        strategie_texte(),
        prop_oneof![
            Just(0u64),
            0u64..24,
            0u64..=u64::from(u8::MAX),
            0u64..=u64::from(u16::MAX),
            0u64..=u64::from(u32::MAX),
            any::<u64>(),
        ],
        proptest::collection::vec(any::<u8>(), 0..64),
    )
        .prop_map(|(source, instant, contenu)| TemoignageTrivial {
            source,
            instant,
            contenu,
        })
}

fn part(compteur: &Cell<usize>, total: &Cell<usize>) -> f64 {
    let total = total.get();
    if total == 0 {
        return 0.0;
    }
    compteur.get() as f64 / total as f64
}

#[test]
fn propriete_a_round_trip_de_la_forme_canonique() {
    let total = Cell::new(0usize);
    let non_triviaux = Cell::new(0usize);
    let instants_larges = Cell::new(0usize);
    let sources_non_ascii = Cell::new(0usize);

    let resultat = executeur().run(&strategie_temoignage(), |temoignage| {
        total.set(total.get() + 1);
        if !temoignage.contenu.is_empty()
            && !temoignage.source.is_empty()
            && temoignage.instant != 0
        {
            non_triviaux.set(non_triviaux.get() + 1);
        }
        if temoignage.instant > u64::from(u32::MAX) {
            instants_larges.set(instants_larges.get() + 1);
        }
        if !temoignage.source.is_ascii() {
            sources_non_ascii.set(sources_non_ascii.get() + 1);
        }

        let octets = encoder_temoignage(&temoignage);
        // decode(encode(x)) == x
        let decode = decoder_temoignage(&octets)
            .map_err(|e| TestCaseError::fail(format!("encodage refusé par le décodeur : {e}")))?;
        prop_assert_eq!(&decode, &temoignage);
        // encode(decode(b)) == b, pour b accepté
        prop_assert_eq!(encoder_temoignage(&decode), octets);
        Ok(())
    });

    println!(
        "(a) round-trip — {} cas ; non triviaux {:.1} % ; instants > 2^32 : {:.1} % ; sources non ASCII : {:.1} %",
        total.get(),
        part(&non_triviaux, &total) * 100.0,
        part(&instants_larges, &total) * 100.0,
        part(&sources_non_ascii, &total) * 100.0
    );
    resultat.unwrap_or_else(|e| panic!("propriété (a) réfutée : {e}"));
    assert!(
        part(&non_triviaux, &total) >= PART_NON_TRIVIALE_MINIMALE,
        "distribution trop triviale ({:.1} %) — corriger le générateur, jamais le seuil (ADR-0011, seuil 6)",
        part(&non_triviaux, &total) * 100.0
    );
}

#[test]
fn propriete_b_unicite_de_representation() {
    let total = Cell::new(0usize);
    let distincts = Cell::new(0usize);

    let resultat = executeur().run(
        &(strategie_temoignage(), strategie_temoignage()),
        |(gauche, droite)| {
            total.set(total.get() + 1);
            // Deux chemins d'encodage du MÊME fait : direct, et via un
            // aller-retour. Les octets doivent être identiques.
            let direct = encoder_temoignage(&gauche);
            let via_decodage = decoder_temoignage(&direct)
                .map(|t| encoder_temoignage(&t))
                .map_err(|e| TestCaseError::fail(format!("aller-retour refusé : {e}")))?;
            prop_assert_eq!(&direct, &via_decodage);

            // Injectivité : deux faits distincts n'ont jamais le même encodage.
            let autre = encoder_temoignage(&droite);
            if gauche != droite {
                distincts.set(distincts.get() + 1);
                prop_assert_ne!(&direct, &autre);
            } else {
                prop_assert_eq!(&direct, &autre);
            }
            Ok(())
        },
    );

    println!(
        "(b) unicité — {} paires ; paires de faits distincts : {:.1} %",
        total.get(),
        part(&distincts, &total) * 100.0
    );
    resultat.unwrap_or_else(|e| panic!("propriété (b) réfutée : {e}"));
    assert!(
        part(&distincts, &total) >= PART_NON_TRIVIALE_MINIMALE,
        "distribution trop triviale : trop peu de paires distinctes"
    );
}

/// Stratégie d'octets hostiles : moitié aléatoire pure, moitié dérivée d'un
/// encodage valide (mutations, troncatures, rallonges) — sans quoi le hasard
/// pur ne franchirait presque jamais le premier en-tête.
fn strategie_octets_hostiles() -> impl Strategy<Value = (Vec<u8>, bool)> {
    let reference = encoder_temoignage(&TemoignageTrivial {
        source: String::from("exemple:source-factice"),
        instant: 1_754_000_000,
        contenu: b"lot d'exemple du walking skeleton".to_vec(),
    });
    let longueur = reference.len();
    prop_oneof![
        2 => proptest::collection::vec(any::<u8>(), 0..200).prop_map(|v| (v, false)),
        3 => (
            proptest::collection::vec((0..longueur, any::<u8>()), 0..6),
            0..=longueur,
        )
            .prop_map(move |(mutations, coupe)| {
                let mut octets = reference.clone();
                for (position, valeur) in mutations {
                    if let Some(case) = octets.get_mut(position) {
                        *case = valeur;
                    }
                }
                octets.truncate(coupe);
                (octets, true)
            }),
        // Le chemin d'ACCEPTATION doit être exercé lui aussi : sans lui, la
        // propriété ne dirait rien de ce qui se passe quand le lot est bon.
        1 => strategie_temoignage().prop_map(|t| (encoder_temoignage(&t), false)),
    ]
}

#[test]
fn propriete_c_totalite_du_decodeur() {
    let total = Cell::new(0usize);
    let derives = Cell::new(0usize);
    let acceptes = Cell::new(0usize);
    let refuses = Cell::new(0usize);

    let resultat = executeur().run(&strategie_octets_hostiles(), |(octets, derive)| {
        total.set(total.get() + 1);
        if derive {
            derives.set(derives.get() + 1);
        }
        match decoder_temoignage(&octets) {
            Ok(temoignage) => {
                acceptes.set(acceptes.get() + 1);
                // Un lot accepté EST sa propre forme canonique : sinon deux
                // suites d'octets distinctes donneraient le même fait.
                prop_assert_eq!(encoder_temoignage(&temoignage), octets);
            }
            Err(erreur) => {
                refuses.set(refuses.get() + 1);
                // Une erreur nommée se dit.
                let rendu = format!("{erreur}");
                prop_assert!(!rendu.trim().is_empty());
            }
        }
        Ok(())
    });

    println!(
        "(c) totalité — {} suites d'octets ; dérivées d'un lot valide : {:.1} % ; acceptées : {} ; refusées : {} ; paniques : 0",
        total.get(),
        part(&derives, &total) * 100.0,
        acceptes.get(),
        refuses.get()
    );
    resultat.unwrap_or_else(|e| panic!("propriété (c) réfutée : {e}"));
    assert!(
        part(&derives, &total) >= 0.25,
        "trop peu d'octets dérivés d'un lot valide : le hasard pur n'atteint pas le cœur du décodeur"
    );
    assert!(
        acceptes.get() > 0,
        "aucune suite acceptée : la propriété ne dirait rien du chemin d'acceptation"
    );
}
