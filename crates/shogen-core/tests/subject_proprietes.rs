//! **Property-based sur le prédicat de `subject`** — ADR-0011 point 2,
//! ADR-0016 §Régime d'assurance (« le prédicat sera *tested* en phase C
//! (property-based + mutants, comptes à la date) »).
//!
//! Les trois propriétés dues par la mission de phase C :
//!
//! * **(a) ré-encodage à l'octet près** — tout `subject` accepté traverse la
//!   forme canonique du témoignage et en ressort **identique**, octet pour
//!   octet : c'est la propriété (a) d'ADR-0011 appliquée au champ dont ADR-0002
//!   disait qu'il restait ouvert ;
//! * **(b) mutation ciblée** — tout écart construit vers une forme interdite est
//!   refusé **avec la variante et la position attendues**. Le prédicat n'est pas
//!   seulement strict : il est strict *au bon endroit* ;
//! * **(c) totalité** — aucune suite d'octets ne fait diverger le prédicat.
//!
//! Les trois obligations d'exécution d'ADR-0011 point 2 sont tenues : graine
//! consignée et rejeu exact (`TestRng::deterministic_rng(RngAlgorithm::ChaCha)`,
//! persistance de fichier désactivée — un fichier d'état caché serait une
//! seconde source de vérité) ; distribution **imprimée avant le verdict** et
//! part de cas non triviaux en assertion (seuil 6) ; tout contre-exemple devient
//! un cas nommé de `subject_canonique.rs`.
//!
//! Registre d'assurance : *tested (avec compte)*. Jamais *proven*.

use proptest::prelude::*;
use proptest::test_runner::{Config, RngAlgorithm, TestRng, TestRunner};
use shogen_core::{
    Attestor, ErreurSubject, OCTETS_D_EMPREINTE, ObservedAt, Temoignage, Utterance,
    decoder_temoignage_canonique, empreinte_sha256, encoder_temoignage_canonique,
    subject_est_canonique,
};
use std::cell::Cell;

/// Seuil 5 d'ADR-0011 : ≥ 1 000 cas par propriété en CI (candidat).
const CAS: u32 = 1_000;
/// Seuil 6 d'ADR-0011 : ≥ 50 % de cas non triviaux (candidat).
const PART_NON_TRIVIALE_MINIMALE: f64 = 0.50;

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

/// Un `subject` canonique engendré, avec les repères dont les mutations ont
/// besoin (elles doivent savoir **où** est l'hôte, le chemin, la requête).
#[derive(Debug, Clone)]
struct SubjectEngendre {
    texte: String,
    /// Position du premier octet de l'hôte — toujours 8.
    debut_hote: usize,
    /// Position du premier octet du chemin (le « / »).
    debut_chemin: usize,
    /// Position du « ? », si une requête est présente.
    debut_requete: Option<usize>,
    /// Vrai si un port explicite est présent.
    porte_un_port: bool,
    /// Vrai si au moins un triplet percent figure dans le chemin ou la requête.
    porte_un_triplet: bool,
}

/// Les triplets admis par C7 : uniquement des caractères **réservés** ou des
/// caractères qui doivent être encodés. Jamais un non réservé (ce serait
/// `PercentEncodageInutile`).
const TRIPLETS_ADMIS: [&str; 6] = ["%2F", "%3F", "%23", "%5B", "%5D", "%20"];

fn strategie_label() -> impl Strategy<Value = String> {
    (
        prop::sample::select(vec!['a', 'b', 'x', 'z']),
        prop::collection::vec(prop::sample::select(vec!['a', 'q', '0', '9', '-']), 0..5),
    )
        .prop_map(|(tete, reste)| {
            let mut label = String::new();
            label.push(tete);
            label.extend(reste);
            // Un label ne finit jamais par « - » : le prédicat l'admettrait,
            // mais le générateur n'a pas à produire des formes que personne
            // n'émet — la mutation ciblée, elle, s'en charge.
            while label.ends_with('-') {
                label.pop();
            }
            label
        })
}

fn strategie_hote() -> impl Strategy<Value = String> {
    prop::collection::vec(strategie_label(), 2..4).prop_map(|labels| labels.join("."))
}

fn strategie_segment() -> impl Strategy<Value = String> {
    prop::collection::vec(
        prop_oneof![
            3 => prop::sample::select(vec!["a", "b", "c", "0", "9", "-", "_", "~"]),
            1 => prop::sample::select(TRIPLETS_ADMIS.to_vec()),
        ],
        1..5,
    )
    .prop_map(|morceaux| morceaux.concat())
}

fn strategie_subject() -> impl Strategy<Value = SubjectEngendre> {
    (
        strategie_hote(),
        prop_oneof![
            2 => Just(None),
            1 => (1u32..65_535u32)
                .prop_filter("443 est le port par défaut, jamais explicite", |port| *port != 443)
                .prop_map(Some),
        ],
        prop::collection::vec(strategie_segment(), 0..3),
        prop_oneof![
            1 => Just(Vec::new()),
            3 => prop::collection::vec((strategie_segment(), strategie_segment()), 1..3),
        ],
    )
        .prop_map(|(hote, port, segments, parametres)| {
            let mut texte = String::from("https://");
            texte.push_str(&hote);
            let porte_un_port = port.is_some();
            if let Some(port) = port {
                texte.push(':');
                texte.push_str(&port.to_string());
            }
            let debut_chemin = texte.len();
            texte.push('/');
            texte.push_str(&segments.join("/"));
            let debut_requete = if parametres.is_empty() {
                None
            } else {
                let position = texte.len();
                texte.push('?');
                let rendu: Vec<String> = parametres
                    .iter()
                    .map(|(cle, valeur)| format!("{cle}={valeur}"))
                    .collect();
                texte.push_str(&rendu.join("&"));
                Some(position)
            };
            let porte_un_triplet = texte.contains('%');
            SubjectEngendre {
                texte,
                debut_hote: 8,
                debut_chemin,
                debut_requete,
                porte_un_port,
                porte_un_triplet,
            }
        })
}

fn part(compteur: &Cell<usize>, total: &Cell<usize>) -> f64 {
    let total = total.get();
    if total == 0 {
        return 0.0;
    }
    compteur.get() as f64 / total as f64
}

/// Un témoignage minimal portant le `subject` à éprouver : c'est le seul chemin
/// par lequel un `subject` devient des octets dans ce dépôt.
fn temoignage_portant(subject: &str) -> Temoignage {
    let octets = b"{\"price\":\"42.17\"}".to_vec();
    Temoignage {
        subject: String::from(subject),
        attestor: vec![Attestor {
            key: vec![0x04, 0x1a, 0x2b],
            identity: String::from("exemple:attestateur-1"),
        }],
        residual: vec![String::from("A(exemple-residu)")],
        transport: String::from("exemple-transport/1"),
        utterance: Utterance {
            hash: empreinte_sha256(&octets),
            bytes: Some(octets),
        },
        observed_at: ObservedAt {
            clock: String::from("exemple:horloge-du-transport"),
            instant: 1_754_000_000,
        },
        transport_proof: vec![0xde, 0xad, 0xbe, 0xef],
    }
}

#[test]
fn propriete_a_tout_subject_accepte_se_reencode_a_l_octet_pres() {
    let total = Cell::new(0usize);
    let non_triviaux = Cell::new(0usize);
    let avec_requete = Cell::new(0usize);
    let avec_triplet = Cell::new(0usize);

    let resultat = executeur().run(&strategie_subject(), |engendre| {
        total.set(total.get().saturating_add(1));
        if engendre.porte_un_port || engendre.debut_requete.is_some() || engendre.porte_un_triplet {
            non_triviaux.set(non_triviaux.get().saturating_add(1));
        }
        if engendre.debut_requete.is_some() {
            avec_requete.set(avec_requete.get().saturating_add(1));
        }
        if engendre.porte_un_triplet {
            avec_triplet.set(avec_triplet.get().saturating_add(1));
        }

        // Le prédicat accepte ce que le générateur prétend canonique.
        if let Err(erreur) = subject_est_canonique(engendre.texte.as_bytes()) {
            return Err(TestCaseError::fail(format!(
                "forme canonique refusée : « {} » — {erreur}",
                engendre.texte
            )));
        }

        // Et il traverse la forme canonique du témoignage sans perdre un octet.
        let temoignage = temoignage_portant(&engendre.texte);
        let octets = encoder_temoignage_canonique(&temoignage);
        let decode = decoder_temoignage_canonique(&octets)
            .map_err(|e| TestCaseError::fail(format!("témoignage refusé : {e}")))?;
        prop_assert_eq!(decode.subject.as_bytes(), engendre.texte.as_bytes());
        prop_assert_eq!(encoder_temoignage_canonique(&decode), octets);
        Ok(())
    });

    println!(
        "(a) subject — {} cas ; non triviaux {:.1} % ; avec requête {:.1} % ; avec triplet {:.1} %",
        total.get(),
        part(&non_triviaux, &total) * 100.0,
        part(&avec_requete, &total) * 100.0,
        part(&avec_triplet, &total) * 100.0
    );
    resultat.unwrap_or_else(|e| panic!("propriété (a) réfutée : {e}"));
    assert!(
        part(&non_triviaux, &total) >= PART_NON_TRIVIALE_MINIMALE,
        "distribution trop triviale ({:.1} %) — corriger le générateur, jamais le seuil (ADR-0011, seuil 6)",
        part(&non_triviaux, &total) * 100.0
    );
}

/// Les classes de mutation : chacune fabrique une forme interdite à partir d'un
/// `subject` canonique et **annonce** la variante et la position attendues.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Mutation {
    HoteEnMajuscule,
    HoteAvecSoulignement,
    HoteNonAscii,
    HoteEntreCrochets,
    HoteEfface,
    UserinfoInsere,
    PortParDefaut,
    PortAZeroDeTete,
    CheminEfface,
    SegmentPointille,
    TripletMinuscule,
    TripletInutile,
    TripletTronque,
    OctetNulEncode,
    RequeteVidee,
    CrochetDansLeChemin,
    OctetNonAsciiDansLeChemin,
    FragmentAjoute,
    SchemeDegrade,
}

const MUTATIONS: [Mutation; 19] = [
    Mutation::HoteEnMajuscule,
    Mutation::HoteAvecSoulignement,
    Mutation::HoteNonAscii,
    Mutation::HoteEntreCrochets,
    Mutation::HoteEfface,
    Mutation::UserinfoInsere,
    Mutation::PortParDefaut,
    Mutation::PortAZeroDeTete,
    Mutation::CheminEfface,
    Mutation::SegmentPointille,
    Mutation::TripletMinuscule,
    Mutation::TripletInutile,
    Mutation::TripletTronque,
    Mutation::OctetNulEncode,
    Mutation::RequeteVidee,
    Mutation::CrochetDansLeChemin,
    Mutation::OctetNonAsciiDansLeChemin,
    Mutation::FragmentAjoute,
    Mutation::SchemeDegrade,
];

/// Applique la mutation. Rend les octets mutés et l'erreur attendue, ou `None`
/// quand la mutation ne s'applique pas à ce `subject` (pas de port à dégrader,
/// pas de requête à vider) : une mutation inapplicable est **comptée**, jamais
/// silencieusement réputée réussie.
fn muter(engendre: &SubjectEngendre, mutation: Mutation) -> Option<(Vec<u8>, ErreurSubject)> {
    let octets = engendre.texte.as_bytes().to_vec();
    let debut_hote = engendre.debut_hote;
    let debut_chemin = engendre.debut_chemin;
    // Le premier octet **après** le « / » du chemin : le lieu des mutations de
    // chemin qui doivent rester dans un segment.
    let dans_le_chemin = debut_chemin.saturating_add(1);
    match mutation {
        Mutation::HoteEnMajuscule => {
            let mut mute = octets.clone();
            let ancien = *mute.get(debut_hote)?;
            let nouveau = ancien.to_ascii_uppercase();
            if nouveau == ancien {
                return None;
            }
            *mute.get_mut(debut_hote)? = nouveau;
            Some((
                mute,
                ErreurSubject::HoteMajuscule {
                    position: debut_hote,
                    octet: nouveau,
                },
            ))
        }
        Mutation::HoteAvecSoulignement => {
            let mut mute = octets.clone();
            *mute.get_mut(debut_hote)? = b'_';
            Some((
                mute,
                ErreurSubject::CaractereHorsGrammaire {
                    position: debut_hote,
                    octet: b'_',
                },
            ))
        }
        Mutation::HoteNonAscii => {
            let mut mute = octets.clone();
            *mute.get_mut(debut_hote)? = 0xC3;
            Some((
                mute,
                ErreurSubject::HoteNonAscii {
                    position: debut_hote,
                    octet: 0xC3,
                },
            ))
        }
        Mutation::HoteEntreCrochets => {
            let mut mute = octets.clone();
            mute.insert(debut_hote, b'[');
            Some((
                mute,
                ErreurSubject::HoteLitteralAdresse {
                    position: debut_hote,
                },
            ))
        }
        Mutation::HoteEfface => {
            let mut mute: Vec<u8> = octets.get(..debut_hote)?.to_vec();
            mute.extend_from_slice(octets.get(debut_chemin..)?);
            Some((
                mute,
                ErreurSubject::HoteVide {
                    position: debut_hote,
                },
            ))
        }
        Mutation::UserinfoInsere => {
            let mut mute: Vec<u8> = octets.get(..debut_hote)?.to_vec();
            mute.extend_from_slice(b"u@");
            mute.extend_from_slice(octets.get(debut_hote..)?);
            Some((
                mute,
                ErreurSubject::UserinfoPresent {
                    position: debut_hote.saturating_add(1),
                },
            ))
        }
        Mutation::PortParDefaut => {
            if engendre.porte_un_port {
                return None;
            }
            let mut mute: Vec<u8> = octets.get(..debut_chemin)?.to_vec();
            mute.extend_from_slice(b":443");
            mute.extend_from_slice(octets.get(debut_chemin..)?);
            Some((
                mute,
                ErreurSubject::PortParDefautExplicite {
                    position: debut_chemin.saturating_add(1),
                },
            ))
        }
        Mutation::PortAZeroDeTete => {
            if engendre.porte_un_port {
                return None;
            }
            let mut mute: Vec<u8> = octets.get(..debut_chemin)?.to_vec();
            mute.extend_from_slice(b":08443");
            mute.extend_from_slice(octets.get(debut_chemin..)?);
            Some((
                mute,
                ErreurSubject::PortNonDecimal {
                    position: debut_chemin.saturating_add(1),
                },
            ))
        }
        Mutation::CheminEfface => {
            let mute: Vec<u8> = octets.get(..debut_chemin)?.to_vec();
            Some((
                mute,
                ErreurSubject::CheminVide {
                    position: debut_chemin,
                },
            ))
        }
        Mutation::SegmentPointille => {
            let mut mute: Vec<u8> = octets.get(..dans_le_chemin)?.to_vec();
            mute.extend_from_slice(b"../");
            mute.extend_from_slice(octets.get(dans_le_chemin..)?);
            Some((
                mute,
                ErreurSubject::SegmentPointille {
                    position: dans_le_chemin,
                },
            ))
        }
        Mutation::TripletMinuscule => {
            let mut mute: Vec<u8> = octets.get(..dans_le_chemin)?.to_vec();
            mute.extend_from_slice(b"%2f");
            mute.extend_from_slice(octets.get(dans_le_chemin..)?);
            Some((
                mute,
                ErreurSubject::TripletPercentMinuscule {
                    position: dans_le_chemin,
                },
            ))
        }
        Mutation::TripletInutile => {
            let mut mute: Vec<u8> = octets.get(..dans_le_chemin)?.to_vec();
            mute.extend_from_slice(b"%41");
            mute.extend_from_slice(octets.get(dans_le_chemin..)?);
            Some((
                mute,
                ErreurSubject::PercentEncodageInutile {
                    position: dans_le_chemin,
                    octet: b'A',
                },
            ))
        }
        Mutation::TripletTronque => {
            let mut mute: Vec<u8> = octets.get(..dans_le_chemin)?.to_vec();
            mute.extend_from_slice(b"%Z");
            mute.extend_from_slice(octets.get(dans_le_chemin..)?);
            Some((
                mute,
                ErreurSubject::TripletPercentMalForme {
                    position: dans_le_chemin,
                },
            ))
        }
        Mutation::OctetNulEncode => {
            let mut mute: Vec<u8> = octets.get(..dans_le_chemin)?.to_vec();
            mute.extend_from_slice(b"%00");
            mute.extend_from_slice(octets.get(dans_le_chemin..)?);
            Some((
                mute,
                ErreurSubject::OctetNulEncode {
                    position: dans_le_chemin,
                },
            ))
        }
        Mutation::RequeteVidee => {
            if engendre.debut_requete.is_some() {
                return None;
            }
            let mut mute = octets.clone();
            mute.push(b'?');
            let position = octets.len();
            Some((mute, ErreurSubject::RequeteVide { position }))
        }
        Mutation::CrochetDansLeChemin => {
            let mut mute: Vec<u8> = octets.get(..dans_le_chemin)?.to_vec();
            mute.push(b'[');
            mute.extend_from_slice(octets.get(dans_le_chemin..)?);
            Some((
                mute,
                ErreurSubject::CaractereHorsGrammaire {
                    position: dans_le_chemin,
                    octet: b'[',
                },
            ))
        }
        Mutation::OctetNonAsciiDansLeChemin => {
            let mut mute: Vec<u8> = octets.get(..dans_le_chemin)?.to_vec();
            mute.push(0xFF);
            mute.extend_from_slice(octets.get(dans_le_chemin..)?);
            Some((
                mute,
                ErreurSubject::OctetNonAscii {
                    position: dans_le_chemin,
                    octet: 0xFF,
                },
            ))
        }
        Mutation::FragmentAjoute => {
            let mut mute = octets.clone();
            let position = mute.len();
            mute.extend_from_slice(b"#f");
            Some((mute, ErreurSubject::FragmentPresent { position }))
        }
        Mutation::SchemeDegrade => {
            let mut mute: Vec<u8> = b"http://".to_vec();
            mute.extend_from_slice(octets.get(debut_hote..)?);
            Some((mute, ErreurSubject::SchemeNonHttps { position: 0 }))
        }
    }
}

#[test]
fn propriete_b_toute_mutation_ciblee_est_refusee_avec_sa_variante() {
    let total = Cell::new(0usize);
    let appliquees = Cell::new(0usize);
    let inapplicables = Cell::new(0usize);

    let resultat = executeur().run(
        &(
            strategie_subject(),
            prop::sample::select(MUTATIONS.to_vec()),
        ),
        |(engendre, mutation)| {
            total.set(total.get().saturating_add(1));
            let Some((mute, attendu)) = muter(&engendre, mutation) else {
                inapplicables.set(inapplicables.get().saturating_add(1));
                return Ok(());
            };
            appliquees.set(appliquees.get().saturating_add(1));
            let obtenu = subject_est_canonique(&mute);
            prop_assert_eq!(
                obtenu,
                Err(attendu),
                "mutation {:?} sur « {} »",
                mutation,
                engendre.texte
            );
            Ok(())
        },
    );

    println!(
        "(b) mutation ciblée — {} cas ; appliquées {:.1} % ; inapplicables {:.1} % ({} classes de mutation)",
        total.get(),
        part(&appliquees, &total) * 100.0,
        part(&inapplicables, &total) * 100.0,
        MUTATIONS.len()
    );
    resultat.unwrap_or_else(|e| panic!("propriété (b) réfutée : {e}"));
    assert!(
        part(&appliquees, &total) >= PART_NON_TRIVIALE_MINIMALE,
        "trop de mutations inapplicables ({:.1} % appliquées) — le générateur ne mord pas",
        part(&appliquees, &total) * 100.0
    );
}

/// Octets hostiles : hasard pur, dérivés d'un `subject` canonique, et formes
/// canoniques — sans le troisième tas, la propriété ne dirait rien du chemin
/// d'acceptation.
fn strategie_octets_hostiles() -> impl Strategy<Value = (Vec<u8>, bool)> {
    let reference = b"https://api.example.com/v3/simple/price?ids=bitcoin".to_vec();
    let longueur = reference.len();
    prop_oneof![
        2 => prop::collection::vec(any::<u8>(), 0..120).prop_map(|v| (v, false)),
        3 => (
            prop::collection::vec((0..longueur, any::<u8>()), 0..6),
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
        1 => strategie_subject().prop_map(|e| (e.texte.into_bytes(), false)),
    ]
}

#[test]
fn propriete_c_le_predicat_ne_diverge_sur_aucune_suite_d_octets() {
    let total = Cell::new(0usize);
    let derives = Cell::new(0usize);
    let acceptes = Cell::new(0usize);
    let refuses = Cell::new(0usize);

    let resultat = executeur().run(&strategie_octets_hostiles(), |(octets, derive)| {
        total.set(total.get().saturating_add(1));
        if derive {
            derives.set(derives.get().saturating_add(1));
        }
        match subject_est_canonique(&octets) {
            Ok(()) => {
                acceptes.set(acceptes.get().saturating_add(1));
                // Un subject accepté est ASCII et commence par le préfixe : ce
                // sont les deux invariants dont tout le reste dépend.
                prop_assert!(octets.is_ascii());
                prop_assert!(octets.starts_with(b"https://"));
                // Et il est stable : le prédicat est pur, donc idempotent.
                prop_assert_eq!(subject_est_canonique(&octets), Ok(()));
            }
            Err(erreur) => {
                refuses.set(refuses.get().saturating_add(1));
                let rendu = format!("{erreur}");
                prop_assert!(!rendu.trim().is_empty());
            }
        }
        Ok(())
    });

    println!(
        "(c) totalité du prédicat — {} suites d'octets ; dérivées {:.1} % ; acceptées {} ; refusées {} ; paniques : 0",
        total.get(),
        part(&derives, &total) * 100.0,
        acceptes.get(),
        refuses.get()
    );
    resultat.unwrap_or_else(|e| panic!("propriété (c) réfutée : {e}"));
    assert!(
        part(&derives, &total) >= 0.25,
        "trop peu d'octets dérivés d'une forme canonique : le hasard pur n'atteint pas le cœur du prédicat"
    );
    assert!(
        acceptes.get() > 0,
        "aucune suite acceptée : la propriété ne dirait rien du chemin d'acceptation"
    );
}

#[test]
fn l_empreinte_est_bien_celle_du_temoignage_engendre() {
    // Garde-fou du générateur lui-même : si `temoignage_portant` cessait de lier
    // le hash aux octets, les propriétés (a) et (b) testeraient un objet qui
    // n'existe pas dans le produit.
    let temoignage = temoignage_portant("https://a.example/x");
    let octets = temoignage
        .utterance
        .bytes
        .clone()
        .expect("le témoignage d'épreuve porte ses octets");
    assert_eq!(temoignage.utterance.hash, empreinte_sha256(&octets));
    assert_eq!(temoignage.utterance.hash.len(), OCTETS_D_EMPREINTE);
}
