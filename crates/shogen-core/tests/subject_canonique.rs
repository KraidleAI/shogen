//! **Le prédicat de canonicité de `subject`, clause par clause** — ADR-0016.
//!
//! Rattachement : ADR-0016 C1-C9 (une entrée de table par clause, avec la
//! variante que l'ADR nomme et la **position** attendue), ADR-0011 point 1.
//!
//! Le test n'est pas « ça refuse » : c'est « ça refuse **avec la variante
//! nommée, à l'octet nommé** ». Un prédicat qui refuserait tout serait vert sur
//! la première formulation et rouge sur celle-ci.

use shogen_core::{ErreurSubject, subject_est_canonique};

/// Le `subject` de référence : un endpoint de la forme du pool S2 (10 §3.1),
/// requête **verbatim**, aucun tri (ADR-0016 C8).
pub const REFERENCE: &str = "https://api.example.com/v3/simple/price?ids=bitcoin&vs_currencies=usd";

/// Les formes canoniques admises — chacune exerce une branche d'acceptation.
const ADMISES: &[(&str, &str)] = &[
    (
        REFERENCE,
        "hôte, chemin à trois segments, requête à deux clés",
    ),
    ("https://a.example/", "chemin minimal « / »"),
    ("https://a.example/?q=1", "chemin « / » suivi d'une requête"),
    ("https://a.example:8443/x", "port explicite non par défaut"),
    (
        "https://a.example/x?a=1&a=2",
        "clé répétée — jamais fusionnée (C8)",
    ),
    (
        "https://a.example/x?b=2&a=1",
        "ordre des paramètres conservé — jamais trié (C8)",
    ),
    (
        "https://a.example/%20espace",
        "triplet d'un caractère qui doit l'être",
    ),
    (
        "https://a.example/x?chemin=%2Fa%2Fb",
        "triplet d'un caractère réservé — ni décodé ni encodé (C7)",
    ),
    (
        "https://a.example/x?plus=a+b",
        "« + » est un sub-delim, jamais un espace (C8 point 5)",
    ),
    ("https://a-b.example/x", "tiret dans un label d'hôte"),
    ("https://a.example/a/b/c", "plusieurs segments"),
    (
        "https://a.example/x?t=:@!$&'()*,;=",
        "tous les sub-delims et « : », « @ » de pchar",
    ),
];

/// Un refus attendu : le `subject`, la variante nommée par l'ADR, la position.
struct Refus {
    subject: &'static str,
    clause: &'static str,
    attendu: ErreurSubject,
}

const REFUS: &[Refus] = &[
    Refus {
        subject: "http://a.example/",
        clause: "C2 — scheme https uniquement",
        attendu: ErreurSubject::SchemeNonHttps { position: 0 },
    },
    Refus {
        subject: "HTTPS://a.example/",
        clause: "C2 — scheme en minuscules",
        attendu: ErreurSubject::SchemeNonHttps { position: 0 },
    },
    Refus {
        subject: "",
        clause: "C2 — un subject vide n'a pas de scheme",
        attendu: ErreurSubject::SchemeNonHttps { position: 0 },
    },
    Refus {
        subject: "https://A.example/",
        clause: "C3 — majuscule d'hôte",
        attendu: ErreurSubject::HoteMajuscule {
            position: 8,
            octet: b'A',
        },
    },
    Refus {
        subject: "https://a%2Eexample/",
        clause: "C3 — triplet dans l'hôte",
        attendu: ErreurSubject::HotePercentEncode { position: 9 },
    },
    Refus {
        subject: "https://[2001:db8::1]/",
        clause: "C3 — littéral d'adresse entre crochets",
        attendu: ErreurSubject::HoteLitteralAdresse { position: 8 },
    },
    Refus {
        subject: "https://192.0.2.1/",
        clause: "C3 — forme pointillée (RFC 3986 §7.4)",
        attendu: ErreurSubject::HoteLitteralAdresse { position: 8 },
    },
    // Les quatre graphies de la revue G2 de phase C (trouvaille F1) : tout
    // client conforme au WHATWG les résout en IPv4 (ends in a number checker,
    // pièce détenue) — le drapeau chiffres-et-points ne les voyait pas.
    Refus {
        subject: "https://0x7f000001/x",
        clause: "C3 — dernier label 0x… (WHATWG ends in a number, pièce détenue)",
        attendu: ErreurSubject::HoteLitteralAdresse { position: 8 },
    },
    Refus {
        subject: "https://0x7f.1/x",
        clause: "C3 — dernier label tout en chiffres après un label 0x…",
        attendu: ErreurSubject::HoteLitteralAdresse { position: 8 },
    },
    Refus {
        subject: "https://0x7f.0x0.0x0.0x1/x",
        clause: "C3 — labels hexadécimaux en chaîne",
        attendu: ErreurSubject::HoteLitteralAdresse { position: 8 },
    },
    Refus {
        subject: "https://1.2.3.0xff/x",
        clause: "C3 — dernier label 0x… derrière des labels décimaux",
        attendu: ErreurSubject::HoteLitteralAdresse { position: 8 },
    },
    Refus {
        subject: "https://é.example/",
        clause: "C3 — hôte IDN, refusé jamais converti",
        attendu: ErreurSubject::HoteNonAscii {
            position: 8,
            octet: 0xC3,
        },
    },
    Refus {
        subject: "https://a_b.example/",
        clause: "C3 — octet hors du jeu d'hôte",
        attendu: ErreurSubject::CaractereHorsGrammaire {
            position: 9,
            octet: b'_',
        },
    },
    Refus {
        subject: "https:///chemin",
        clause: "C3 — hôte vide",
        attendu: ErreurSubject::HoteVide { position: 8 },
    },
    Refus {
        subject: "https://user@a.example/",
        clause: "C4 — userinfo",
        attendu: ErreurSubject::UserinfoPresent { position: 12 },
    },
    Refus {
        subject: "https://a.example:443/",
        clause: "C5 — port par défaut explicite",
        attendu: ErreurSubject::PortParDefautExplicite { position: 18 },
    },
    Refus {
        subject: "https://a.example:80a0/",
        clause: "C5 — port non décimal",
        attendu: ErreurSubject::PortNonDecimal { position: 20 },
    },
    Refus {
        subject: "https://a.example:0443/",
        clause: "C5 — zéro de tête",
        attendu: ErreurSubject::PortNonDecimal { position: 18 },
    },
    Refus {
        subject: "https://a.example:/x",
        clause: "C5 — port vide",
        attendu: ErreurSubject::PortNonDecimal { position: 18 },
    },
    Refus {
        subject: "https://a.example",
        clause: "C6 — chemin vide",
        attendu: ErreurSubject::CheminVide { position: 17 },
    },
    Refus {
        subject: "https://a.example?q=1",
        clause: "C6 — chemin vide devant une requête",
        attendu: ErreurSubject::CheminVide { position: 17 },
    },
    Refus {
        subject: "https://a.example/a/../b",
        clause: "C6 — segment « .. »",
        attendu: ErreurSubject::SegmentPointille { position: 20 },
    },
    Refus {
        subject: "https://a.example/./b",
        clause: "C6 — segment « . »",
        attendu: ErreurSubject::SegmentPointille { position: 18 },
    },
    Refus {
        subject: "https://a.example/%2f",
        clause: "C7.1 — chiffre hexadécimal minuscule",
        attendu: ErreurSubject::TripletPercentMinuscule { position: 18 },
    },
    Refus {
        subject: "https://a.example/%41",
        clause: "C7.2 — triplet d'un caractère non réservé",
        attendu: ErreurSubject::PercentEncodageInutile {
            position: 18,
            octet: b'A',
        },
    },
    Refus {
        subject: "https://a.example/%7E",
        clause: "C7.2 — « ~ » est non réservé",
        attendu: ErreurSubject::PercentEncodageInutile {
            position: 18,
            octet: b'~',
        },
    },
    Refus {
        subject: "https://a.example/%2",
        clause: "C7.3 — triplet tronqué",
        attendu: ErreurSubject::TripletPercentMalForme { position: 18 },
    },
    Refus {
        subject: "https://a.example/%ZZ",
        clause: "C7.3 — triplet non hexadécimal",
        attendu: ErreurSubject::TripletPercentMalForme { position: 18 },
    },
    Refus {
        subject: "https://a.example/%00",
        clause: "C7.3 — octet nul encodé",
        attendu: ErreurSubject::OctetNulEncode { position: 18 },
    },
    Refus {
        subject: "https://a.example/x?",
        clause: "C8 — « ? » nu",
        attendu: ErreurSubject::RequeteVide { position: 19 },
    },
    Refus {
        subject: "https://a.example/x?ids[]=1",
        clause: "C8 — crochets hors grammaire (le cas Pyth du §Coûts)",
        attendu: ErreurSubject::CaractereHorsGrammaire {
            position: 23,
            octet: b'[',
        },
    },
    Refus {
        subject: "https://a.example/x#frag",
        clause: "C9 — fragment",
        attendu: ErreurSubject::FragmentPresent { position: 19 },
    },
    Refus {
        subject: "https://a.example/é",
        clause: "C1 — octet ≥ 0x80 hors de l'hôte",
        attendu: ErreurSubject::OctetNonAscii {
            position: 18,
            octet: 0xC3,
        },
    },
];

#[test]
fn les_formes_canoniques_sont_admises() {
    for (subject, motif) in ADMISES {
        assert_eq!(
            subject_est_canonique(subject.as_bytes()),
            Ok(()),
            "forme canonique refusée ({motif}) : {subject}"
        );
    }
    println!(
        "acceptation — {} formes canoniques admises, une par branche",
        ADMISES.len()
    );
}

#[test]
fn chaque_clause_refuse_avec_sa_variante_a_sa_position() {
    for cas in REFUS {
        let obtenu = subject_est_canonique(cas.subject.as_bytes());
        assert_eq!(
            obtenu,
            Err(cas.attendu.clone()),
            "{} — subject « {} »",
            cas.clause,
            cas.subject
        );
    }
    println!(
        "refus nommés — {} cas, une variante et une position attendues par cas",
        REFUS.len()
    );
}

#[test]
fn les_dix_neuf_variantes_sont_toutes_exercees() {
    // Un prédicat qui ne pourrait plus produire une variante serait une
    // régression silencieuse : ce test la rend bruyante. Le compte est celui
    // d'`ErreurSubject`, dix-sept noms d'ADR-0016 plus les deux nommés au module
    // (`SchemeNonHttps`, `HoteVide`).
    let mut vues: Vec<String> = REFUS
        .iter()
        .map(|cas| format!("{:?}", cas.attendu))
        .map(|rendu| {
            rendu
                .split_whitespace()
                .next()
                .unwrap_or_default()
                .to_string()
        })
        .collect();
    vues.sort();
    vues.dedup();
    println!("variantes exercées ({}) : {vues:?}", vues.len());
    assert_eq!(
        vues.len(),
        19,
        "toutes les variantes d'ErreurSubject doivent être exercées"
    );
}

#[test]
fn les_refus_se_disent_en_toutes_lettres() {
    // Une erreur qui ne se dit pas n'est pas nommée : c'est ce rendu que le
    // vérificateur imprime, et c'est ce qu'un tiers lit.
    for cas in REFUS {
        let rendu = format!("{}", cas.attendu);
        assert!(!rendu.trim().is_empty(), "refus muet : {:?}", cas.attendu);
        assert!(
            rendu.contains("ADR-0016"),
            "un refus cite sa clause : {rendu}"
        );
        assert!(
            rendu.contains("octet"),
            "un refus dit où il se produit : {rendu}"
        );
    }
}

#[test]
fn le_predicat_ne_normalise_jamais() {
    // C0 : le prédicat *contrôle*, il ne réécrit pas. Sa signature l'établit
    // (`Result<(), _>` ne peut rendre aucun subject), ce test le documente au
    // rang du comportement : une forme non canonique reste refusée, jamais
    // « corrigée » puis admise.
    let non_canonique = "https://A.example/a/../b";
    assert!(subject_est_canonique(non_canonique.as_bytes()).is_err());
    // Et sa version normalisée à la main, elle, passe : la normalisation existe,
    // elle a lieu **ailleurs** (à la construction, dans l'adapter).
    assert_eq!(subject_est_canonique(b"https://a.example/b"), Ok(()));
}
