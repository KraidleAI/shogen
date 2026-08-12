//! Tests *example-based* de la forme canonique : vecteur de référence, ordre
//! des clés recalculé, et refus des formes non canoniques.
//!
//! Rattachement : ADR-0002 (Core Deterministic Encoding Requirements),
//! ADR-0011 point 1 (socle : unitaires ET property-based sur le cœur).

use shogen_core::{
    CLE_CONTENU, CLE_INSTANT, CLE_SOURCE, ErreurDecodage, ORDRE_CANONIQUE_DES_CLES,
    TemoignageTrivial, decoder_temoignage, encodage_de_cle, encoder_temoignage,
};

/// Le témoignage de référence du walking skeleton (identique à celui de
/// `cargo xtask emettre-exemple`).
pub fn reference() -> TemoignageTrivial {
    TemoignageTrivial {
        source: String::from("exemple:source-factice"),
        instant: 1_754_000_000,
        contenu: b"lot d'exemple du walking skeleton".to_vec(),
    }
}

fn hexa(octets: &[u8]) -> String {
    octets.iter().map(|o| format!("{o:02x}")).collect()
}

#[test]
fn vecteur_de_reference_octet_par_octet() {
    let octets = encoder_temoignage(&reference());
    // Vecteur figé : si l'encodeur bouge d'un seul octet, ce test tombe. C'est
    // le point — la forme canonique est un contrat d'octets, pas d'API.
    // Il est reconstruit ici à la main, en-tête par en-tête, à partir de la
    // structure exigée par ADR-0002, et non recopié d'une sortie de programme.
    let mut manuel: Vec<u8> = Vec::new();
    manuel.extend_from_slice(&[0xa3]);
    manuel.extend_from_slice(&[0x66]);
    manuel.extend_from_slice(CLE_SOURCE.as_bytes());
    manuel.extend_from_slice(&[0x76]);
    manuel.extend_from_slice(reference().source.as_bytes());
    manuel.extend_from_slice(&[0x67]);
    manuel.extend_from_slice(CLE_CONTENU.as_bytes());
    manuel.extend_from_slice(&[0x58, 0x21]);
    manuel.extend_from_slice(&reference().contenu);
    manuel.extend_from_slice(&[0x67]);
    manuel.extend_from_slice(CLE_INSTANT.as_bytes());
    manuel.extend_from_slice(&[0x1a]);
    manuel.extend_from_slice(&1_754_000_000u32.to_be_bytes());

    assert_eq!(
        hexa(&octets),
        hexa(&manuel),
        "l'encodage ne suit pas la structure canonique attendue"
    );
    assert_eq!(octets.len(), 87, "longueur du vecteur de référence");
}

#[test]
fn l_ordre_des_cles_est_le_tri_par_octets_des_cles_encodees() {
    // On ne croit pas l'ordre déclaré : on le recalcule.
    let mut trie: Vec<Vec<u8>> = [CLE_SOURCE, CLE_CONTENU, CLE_INSTANT]
        .iter()
        .map(|cle| encodage_de_cle(cle))
        .collect();
    trie.sort();
    let declare: Vec<Vec<u8>> = ORDRE_CANONIQUE_DES_CLES
        .iter()
        .map(|cle| encodage_de_cle(cle))
        .collect();
    assert_eq!(
        declare, trie,
        "ORDRE_CANONIQUE_DES_CLES doit être le tri lexicographique par octets des clés encodées"
    );
}

#[test]
fn round_trip_exact_sur_la_reference() {
    let octets = encoder_temoignage(&reference());
    let decode = decoder_temoignage(&octets).expect("la référence doit décoder");
    assert_eq!(decode, reference());
    assert_eq!(encoder_temoignage(&decode), octets);
}

#[test]
fn entree_vide_refusee() {
    assert_eq!(decoder_temoignage(&[]), Err(ErreurDecodage::EntreeVide));
}

#[test]
fn octets_residuels_refuses() {
    let mut octets = encoder_temoignage(&reference());
    octets.push(0x00);
    match decoder_temoignage(&octets) {
        Err(ErreurDecodage::OctetsResiduels { restants, .. }) => assert_eq!(restants, 1),
        autre => panic!("attendu OctetsResiduels, obtenu {autre:?}"),
    }
}

#[test]
fn toute_troncature_est_refusee() {
    let octets = encoder_temoignage(&reference());
    for longueur in 0..octets.len() {
        let tronque = &octets[..longueur];
        let resultat = decoder_temoignage(tronque);
        assert!(
            resultat.is_err(),
            "le préfixe de {longueur} octet(s) ne doit pas décoder : {resultat:?}"
        );
    }
}

#[test]
fn longueur_indefinie_refusee() {
    // 0xbf = map(*) — longueur indéfinie, interdite par le sous-ensemble.
    let mut octets = encoder_temoignage(&reference());
    octets[0] = 0xbf;
    match decoder_temoignage(&octets) {
        Err(ErreurDecodage::LongueurIndefinie { position }) => assert_eq!(position, 0),
        autre => panic!("attendu LongueurIndefinie, obtenu {autre:?}"),
    }
}

#[test]
fn entier_non_prefere_refuse() {
    // « instant » encodé sur 8 octets alors que 4 suffisent : forme non préférée.
    let mut octets: Vec<u8> = Vec::new();
    octets.extend_from_slice(&[0xa3, 0x66]);
    octets.extend_from_slice(CLE_SOURCE.as_bytes());
    octets.extend_from_slice(&[0x60]); // texte vide
    octets.extend_from_slice(&[0x67]);
    octets.extend_from_slice(CLE_CONTENU.as_bytes());
    octets.extend_from_slice(&[0x40]); // octets vides
    octets.extend_from_slice(&[0x67]);
    octets.extend_from_slice(CLE_INSTANT.as_bytes());
    octets.extend_from_slice(&[0x1b]);
    octets.extend_from_slice(&1_754_000_000u64.to_be_bytes());
    match decoder_temoignage(&octets) {
        Err(ErreurDecodage::EntierNonPrefere {
            argument,
            octets_utilises,
            ..
        }) => {
            assert_eq!(argument, 1_754_000_000);
            assert_eq!(octets_utilises, 8);
        }
        autre => panic!("attendu EntierNonPrefere, obtenu {autre:?}"),
    }
}

#[test]
fn cles_non_triees_refusees() {
    // Les mêmes trois champs, dans le mauvais ordre : contenu avant source.
    let mut octets: Vec<u8> = Vec::new();
    octets.extend_from_slice(&[0xa3, 0x67]);
    octets.extend_from_slice(CLE_CONTENU.as_bytes());
    octets.extend_from_slice(&[0x40]);
    octets.extend_from_slice(&[0x66]);
    octets.extend_from_slice(CLE_SOURCE.as_bytes());
    octets.extend_from_slice(&[0x60]);
    octets.extend_from_slice(&[0x67]);
    octets.extend_from_slice(CLE_INSTANT.as_bytes());
    octets.extend_from_slice(&[0x00]);
    match decoder_temoignage(&octets) {
        Err(ErreurDecodage::ClesNonTriees {
            precedente,
            courante,
            ..
        }) => {
            assert_eq!(precedente, CLE_CONTENU);
            assert_eq!(courante, CLE_SOURCE);
        }
        autre => panic!("attendu ClesNonTriees, obtenu {autre:?}"),
    }
}

#[test]
fn cle_dupliquee_refusee() {
    let mut octets: Vec<u8> = Vec::new();
    octets.extend_from_slice(&[0xa3, 0x66]);
    octets.extend_from_slice(CLE_SOURCE.as_bytes());
    octets.extend_from_slice(&[0x60]);
    octets.extend_from_slice(&[0x66]);
    octets.extend_from_slice(CLE_SOURCE.as_bytes());
    octets.extend_from_slice(&[0x60]);
    octets.extend_from_slice(&[0x67]);
    octets.extend_from_slice(CLE_INSTANT.as_bytes());
    octets.extend_from_slice(&[0x00]);
    match decoder_temoignage(&octets) {
        Err(ErreurDecodage::CleDupliquee { cle, .. }) => assert_eq!(cle, CLE_SOURCE),
        autre => panic!("attendu CleDupliquee, obtenu {autre:?}"),
    }
}

#[test]
fn cle_inconnue_refusee() {
    let mut octets: Vec<u8> = Vec::new();
    octets.extend_from_slice(&[0xa3, 0x61, b'a']); // clé "a"
    octets.extend_from_slice(&[0x60]);
    octets.extend_from_slice(&[0x66]);
    octets.extend_from_slice(CLE_SOURCE.as_bytes());
    octets.extend_from_slice(&[0x60]);
    octets.extend_from_slice(&[0x67]);
    octets.extend_from_slice(CLE_INSTANT.as_bytes());
    octets.extend_from_slice(&[0x00]);
    match decoder_temoignage(&octets) {
        Err(ErreurDecodage::CleInconnue { cle, .. }) => assert_eq!(cle, "a"),
        autre => panic!("attendu CleInconnue, obtenu {autre:?}"),
    }
}

#[test]
fn taille_de_carte_inattendue_refusee() {
    let mut octets = encoder_temoignage(&reference());
    octets[0] = 0xa2; // map(2)
    match decoder_temoignage(&octets) {
        Err(ErreurDecodage::TailleCarteInattendue {
            attendue, trouvee, ..
        }) => {
            assert_eq!(attendue, 3);
            assert_eq!(trouvee, 2);
        }
        autre => panic!("attendu TailleCarteInattendue, obtenu {autre:?}"),
    }
}

#[test]
fn longueur_gigantesque_ne_provoque_aucune_allocation() {
    // Une longueur de 2^63 annoncée pour le contenu : le décodeur doit refuser
    // sans jamais dimensionner un tampon sur cette valeur (ADR-0010, point 1).
    let mut octets: Vec<u8> = Vec::new();
    octets.extend_from_slice(&[0xa3, 0x66]);
    octets.extend_from_slice(CLE_SOURCE.as_bytes());
    octets.extend_from_slice(&[0x60]);
    octets.extend_from_slice(&[0x67]);
    octets.extend_from_slice(CLE_CONTENU.as_bytes());
    octets.extend_from_slice(&[0x5b]);
    octets.extend_from_slice(&0x7fff_ffff_ffff_ffffu64.to_be_bytes());
    let resultat = decoder_temoignage(&octets);
    assert!(
        matches!(
            resultat,
            Err(ErreurDecodage::FinPrematuree { .. })
                | Err(ErreurDecodage::LongueurHorsMemoire { .. })
        ),
        "attendu un refus de longueur, obtenu {resultat:?}"
    );
}

#[test]
fn texte_non_utf8_refuse() {
    let mut octets: Vec<u8> = Vec::new();
    octets.extend_from_slice(&[0xa3, 0x66]);
    octets.extend_from_slice(CLE_SOURCE.as_bytes());
    octets.extend_from_slice(&[0x61, 0xff]); // texte(1) = 0xff, invalide
    octets.extend_from_slice(&[0x67]);
    octets.extend_from_slice(CLE_CONTENU.as_bytes());
    octets.extend_from_slice(&[0x40]);
    octets.extend_from_slice(&[0x67]);
    octets.extend_from_slice(CLE_INSTANT.as_bytes());
    octets.extend_from_slice(&[0x00]);
    match decoder_temoignage(&octets) {
        Err(ErreurDecodage::TexteNonUtf8 { longueur, .. }) => assert_eq!(longueur, 1),
        autre => panic!("attendu TexteNonUtf8, obtenu {autre:?}"),
    }
}

#[test]
fn les_erreurs_sont_nommees_en_toutes_lettres() {
    // Une erreur qui ne se dit pas n'est pas nommée : le vérificateur imprime
    // ce Display, et c'est ce que lit un tiers.
    let rendu = format!("{}", ErreurDecodage::EntreeVide);
    assert!(rendu.contains("entrée vide"), "rendu : {rendu}");
    let rendu = format!(
        "{}",
        ErreurDecodage::ClesNonTriees {
            position: 3,
            precedente: String::from("contenu"),
            courante: String::from("source"),
        }
    );
    assert!(rendu.contains("clés non triées"), "rendu : {rendu}");
    assert!(rendu.contains("octet 3"), "rendu : {rendu}");
}
