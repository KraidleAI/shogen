//! **Les vecteurs officiels de SHA-256** — ce qui établit `empreinte.rs`.
//!
//! Rattachement : ADR-0005 règle 1 (le hash des octets exacts lie le témoignage
//! à sa preuve), ADR-0011 point 1 (socle : unitaires ET property-based sur le
//! cœur), doc 03 (« aucun chiffre de seconde main »).
//!
//! **Provenance des vecteurs — aucun n'est écrit de mémoire.** Deux pièces
//! publiques, acquises le 2026-08-13, sha256 recalculés en destination, déposées
//! pour versement en `scratch/biblio-a-verser/` (le versement à `biblio/` et son
//! entrée d'INDEX appartiennent à l'orchestrateur — S-G6 exige l'entrée de
//! registre en même temps que l'octet) :
//!
//! | pièce | sha256 | ce qu'elle porte |
//! |---|---|---|
//! | `nist-cavp-sha-byte-test-vectors-2026-08-13.zip` (NIST CAVP, « SHA Test Vectors for Hashing Byte-Oriented Messages », `shabytetestvectors.zip`) | `929ef80b7b3418aca026643f6f248815913b60e01741a44bba9e118067f4c9b8` | `SHA256ShortMsg.rsp` (Len 0 à 512 bits) et `SHA256LongMsg.rsp` (Len 1304 bits et au-delà) |
//! | `nist-sha256-examples-intermediate-values-2026-08-13.pdf` (NIST, *SHA-256 Examples*, valeurs intermédiaires) | `7006b6549dad2fc8c6f29417a921f2e48208157ef496a7e1e1d7d17c5cc1e7db` | « abc » (un bloc) et le message de 56 octets (deux blocs) |
//!
//! **Couverture des frontières de rembourrage, dite exactement.** Le rembourrage
//! de FIPS 180-4 §5.1.1 ne dépend que du **reste** de la longueur modulo 64 :
//! les vecteurs à 55, 56, 57 et 64 octets exercent les quatre cas de branche
//! (reste < 56, reste = 56, reste > 56, reste = 0), et les vecteurs à 64 et 163
//! octets exercent la présence de blocs pleins **avant** la queue.
//!
//! **Ce qui manque et n'est pas caché** : aucune pièce détenue ne porte de
//! vecteur à 119 ou 120 octets. Le `SHA256ShortMsg.rsp` du CAVP s'arrête à
//! 64 octets et le `LongMsg` commence à 163 ; ces deux longueurs auraient les
//! restes 55 et 56, déjà couverts, mais avec un bloc plein en amont — la
//! combinaison exacte n'est donc pas couverte par un vecteur d'autorité. Écrire
//! ici qu'elle l'est serait un faux.

use shogen_core::{empreinte_en_hexadecimal, empreinte_sha256};

/// Un vecteur : sa provenance, son message (hexadécimal), son condensé attendu.
struct Vecteur {
    nom: &'static str,
    piece: &'static str,
    message: &'static str,
    condense: &'static str,
}

/// Les dix vecteurs employés, chacun avec la pièce et l'entrée qui le porte.
const VECTEURS: &[Vecteur] = &[
    Vecteur {
        nom: "chaîne vide (0 octet)",
        piece: "CAVP SHA256ShortMsg.rsp, Len = 0",
        message: "",
        condense: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    },
    Vecteur {
        nom: "un octet",
        piece: "CAVP SHA256ShortMsg.rsp, Len = 8",
        message: "d3",
        condense: "28969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c1",
    },
    Vecteur {
        nom: "trois octets",
        piece: "CAVP SHA256ShortMsg.rsp, Len = 24",
        message: "b4190e",
        condense: "dff2e73091f6c05e528896c4c831b9448653dc2ff043528f6769437bc7b975c2",
    },
    Vecteur {
        nom: "« abc » — un bloc",
        piece: "NIST SHA-256 Examples, One Block Message Sample",
        message: "616263",
        condense: "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
    },
    Vecteur {
        nom: "55 octets — dernier bloc juste sous la frontière",
        piece: "CAVP SHA256ShortMsg.rsp, Len = 440",
        message: "3ebfb06db8c38d5ba037f1363e118550aad94606e26835a01af05078533cc25f2f39573c04b632f62f68c294ab31f2a3e2a1a0d8c2be51",
        condense: "6595a2ef537a69ba8583dfbf7f5bec0ab1f93ce4c8ee1916eff44a93af5749c4",
    },
    Vecteur {
        nom: "56 octets — le rembourrage déborde d'un bloc",
        piece: "CAVP SHA256ShortMsg.rsp, Len = 448",
        message: "2d52447d1244d2ebc28650e7b05654bad35b3a68eedc7f8515306b496d75f3e73385dd1b002625024b81a02f2fd6dffb6e6d561cb7d0bd7a",
        condense: "cfb88d6faf2de3a69d36195acec2e255e2af2b7d933997f348e09f6ce5758360",
    },
    Vecteur {
        nom: "56 octets ASCII — deux blocs (message de la pièce d'exemples)",
        piece: "NIST SHA-256 Examples, Two Block Message Sample",
        message: "6162636462636465636465666465666765666768666768696768696a68696a6b696a6b6c6a6b6c6d6b6c6d6e6c6d6e6f6d6e6f706e6f7071",
        condense: "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1",
    },
    Vecteur {
        nom: "57 octets — au-delà de la frontière",
        piece: "CAVP SHA256ShortMsg.rsp, Len = 456",
        message: "4cace422e4a015a75492b3b3bbfbdf3758eaff4fe504b46a26c90dacc119fa9050f603d2b58b398cad6d6d9fa922a154d9e0bc4389968274b0",
        condense: "4d54b2d284a6794581224e08f675541c8feab6eefa3ac1cfe5da4e03e62f72e4",
    },
    Vecteur {
        nom: "64 octets — un bloc plein, queue de rembourrage seule",
        piece: "CAVP SHA256ShortMsg.rsp, Len = 512",
        message: "5a86b737eaea8ee976a0a24da63e7ed7eefad18a101c1211e2b3650c5187c2a8a650547208251f6d4237e661c7bf4c77f335390394c37fa1a9f9be836ac28509",
        condense: "42e61e174fbb3897d6dd6cef3dd2802fe67b331953b06114a65c772859dfc1aa",
    },
    Vecteur {
        nom: "163 octets — trois blocs",
        piece: "CAVP SHA256LongMsg.rsp, Len = 1304",
        message: "451101250ec6f26652249d59dc974b7361d571a8101cdfd36aba3b5854d3ae086b5fdd4597721b66e3c0dc5d8c606d9657d0e323283a5217d1f53f2f284f57b85c8a61ac8924711f895c5ed90ef17745ed2d728abd22a5f7a13479a462d71b56c19a74a40b655c58edfe0a188ad2cf46cbf30524f65d423c837dd1ff2bf462ac4198007345bb44dbb7b1c861298cdf61982a833afc728fae1eda2f87aa2c9480858bec",
        condense: "3c593aa539fdcdae516cdf2f15000f6634185c88f505b39775fb9ab137a10aa2",
    },
];

fn depuis_hexadecimal(texte: &str) -> Vec<u8> {
    assert!(
        texte.len().is_multiple_of(2),
        "hexadécimal impair : {texte}"
    );
    texte
        .as_bytes()
        .chunks_exact(2)
        .map(|paire| {
            let rendu = std::str::from_utf8(paire).expect("hexadécimal ASCII");
            u8::from_str_radix(rendu, 16).expect("chiffre hexadécimal")
        })
        .collect()
}

#[test]
fn les_vecteurs_officiels_sont_reproduits_a_l_octet_pres() {
    let mut longueurs: Vec<usize> = Vec::new();
    for vecteur in VECTEURS {
        let message = depuis_hexadecimal(vecteur.message);
        let obtenu = empreinte_en_hexadecimal(&empreinte_sha256(&message));
        assert_eq!(
            obtenu, vecteur.condense,
            "vecteur « {} » ({}) : condensé divergent",
            vecteur.nom, vecteur.piece
        );
        longueurs.push(message.len());
    }
    // Distribution imprimée AVANT le verdict, comme une ligne de couverture.
    println!(
        "vecteurs officiels SHA-256 — {} vecteurs, longueurs de message : {:?} octets",
        VECTEURS.len(),
        longueurs
    );
    assert_eq!(
        VECTEURS.len(),
        10,
        "le corpus de vecteurs a changé sans le dire"
    );
}

#[test]
fn les_quatre_cas_de_rembourrage_sont_exerces() {
    // Ce test ne recalcule rien : il **mesure** ce que le corpus couvre, pour
    // qu'une régression du corpus (un vecteur retiré) tombe ici plutôt que de
    // passer inaperçue.
    let mut restes: Vec<usize> = VECTEURS
        .iter()
        .map(|vecteur| depuis_hexadecimal(vecteur.message).len() % 64)
        .collect();
    restes.sort_unstable();
    restes.dedup();
    println!("restes de longueur modulo 64 couverts : {restes:?}");
    for attendu in [0usize, 55, 56, 57] {
        assert!(
            restes.contains(&attendu),
            "le reste {attendu} n'est plus couvert : la frontière de rembourrage correspondante n'est plus établie"
        );
    }
}

#[test]
fn le_condense_a_toujours_trente_deux_octets() {
    for longueur in [0usize, 1, 55, 56, 63, 64, 65, 127, 128, 200] {
        let message = vec![0x61u8; longueur];
        assert_eq!(
            empreinte_sha256(&message).len(),
            32,
            "longueur de condensé pour un message de {longueur} octet(s)"
        );
    }
}

#[test]
fn deux_messages_distincts_de_la_meme_longueur_donnent_deux_condenses() {
    // Propriété faible mais nécessaire : l'empreinte dépend des octets, pas
    // seulement de la longueur. Un « hash » constant passerait tous les tests de
    // forme et aucun de ceux-ci.
    let gauche = empreinte_sha256(b"lot d'exemple du walking skeleton");
    let droite = empreinte_sha256(b"lot d'exemple du walking skeletoN");
    assert_ne!(gauche, droite);
}

/// **Table séparée : contrôles croisés, NON-NIST** (adjudication ADR-0018,
/// question 3). Les longueurs 119 et 120 (reste 55/56 modulo 64 AVEC un bloc
/// plein en amont) ne sont couvertes par aucun vecteur d'autorité détenu :
/// le CAVP ShortMsg s'arrête à 64 octets, le LongMsg commence à 163. Les
/// condensés ci-dessous ne sont PAS des vecteurs NIST — ils ont été calculés
/// le 2026-08-13 par DEUX implémentations tierces indépendantes et
/// concordantes (python hashlib et GNU coreutils sha256sum), sur le message
/// déterministe octet(i) = (i*7 + 3) mod 256. Ils établissent la concordance
/// d'implémentation sur cette combinaison de frontières, rien de plus.
#[test]
fn controles_croises_non_nist_119_et_120_octets() {
    let cas: [(usize, &str); 2] = [
        (
            119,
            "9ce7368e4daf32341631b492e80359dc9f594b48453cd0dd5bf0b19279cc177e",
        ),
        (
            120,
            "7836b787757e95e58b3ca5aec90b1b004e8deba1e50e9675af9cabf1a13a04b5",
        ),
    ];
    for (longueur, attendu) in cas {
        let message: Vec<u8> = (0..longueur).map(|i| ((i * 7 + 3) % 256) as u8).collect();
        let obtenu = empreinte_en_hexadecimal(&empreinte_sha256(&message));
        assert_eq!(
            obtenu, attendu,
            "contrôle croisé non-NIST en défaut sur {longueur} octets"
        );
    }
}
