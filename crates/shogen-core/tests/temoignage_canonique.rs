//! **La forme canonique des sept champs** — vecteur figé, ordre des clés
//! recalculé, refus nommés.
//!
//! Rattachement : 03 §1 (les sept champs), ADR-0002 (Core Deterministic
//! Encoding Requirements), ADR-0005 (le hash toujours, les octets par
//! politique), ADR-0016 C10 (le prédicat branché au décodage), ADR-0011 point 1.
//!
//! Le vecteur de référence est **reconstruit ici à la main**, en-tête par
//! en-tête, depuis la structure exigée par ADR-0002 — jamais recopié d'une
//! sortie de programme. Si l'encodeur bouge d'un octet, ce test tombe : la forme
//! canonique est un contrat d'octets, pas d'API.

use shogen_core::{
    CLE_ATTESTOR, CLE_BYTES, CLE_CLOCK, CLE_HASH, CLE_IDENTITY, CLE_INSTANT, CLE_KEY,
    CLE_OBSERVED_AT, CLE_RESIDUAL, CLE_SUBJECT, CLE_TRANSPORT, CLE_TRANSPORT_PROOF, ErreurDecodage,
    ErreurSubject, Lot, ORDRE_CANONIQUE_DU_TEMOIGNAGE, Temoignage, decoder_lot,
    decoder_temoignage_canonique, empreinte_sha256, encodage_de_cle, encoder_lot,
    encoder_temoignage_canonique,
};

mod commun;

use commun::{
    HORLOGE, IDENTITE, OCTETS_D_UTTERANCE, OCTETS_DE_PREUVE, RESIDU_1, RESIDU_2, SUBJECT,
    TRANSPORT, reference,
};

fn hexa(octets: &[u8]) -> String {
    octets.iter().map(|o| format!("{o:02x}")).collect()
}

#[test]
fn vecteur_de_reference_octet_par_octet() {
    let octets = encoder_temoignage_canonique(&reference());

    let mut manuel: Vec<u8> = Vec::new();
    manuel.extend_from_slice(&[0xa7]); // carte de 7 entrées

    manuel.extend_from_slice(&[0x67]); // texte(7)
    manuel.extend_from_slice(CLE_SUBJECT.as_bytes());
    manuel.extend_from_slice(&[0x78, 0x33]); // texte(51)
    manuel.extend_from_slice(SUBJECT.as_bytes());

    manuel.extend_from_slice(&[0x68]); // texte(8)
    manuel.extend_from_slice(CLE_ATTESTOR.as_bytes());
    manuel.extend_from_slice(&[0x81]); // tableau(1)
    manuel.extend_from_slice(&[0xa2]); // carte(2)
    manuel.extend_from_slice(&[0x63]); // texte(3)
    manuel.extend_from_slice(CLE_KEY.as_bytes());
    manuel.extend_from_slice(&[0x50]); // octets(16)
    manuel.extend_from_slice(commun::CLE_EPINGLEE);
    manuel.extend_from_slice(&[0x68]); // texte(8)
    manuel.extend_from_slice(CLE_IDENTITY.as_bytes());
    manuel.extend_from_slice(&[0x75]); // texte(21)
    manuel.extend_from_slice(IDENTITE.as_bytes());

    manuel.extend_from_slice(&[0x68]); // texte(8)
    manuel.extend_from_slice(CLE_RESIDUAL.as_bytes());
    manuel.extend_from_slice(&[0x82]); // tableau(2)
    manuel.extend_from_slice(&[0x73]); // texte(19)
    manuel.extend_from_slice(RESIDU_1.as_bytes());
    manuel.extend_from_slice(&[0x73]); // texte(19)
    manuel.extend_from_slice(RESIDU_2.as_bytes());

    manuel.extend_from_slice(&[0x69]); // texte(9)
    manuel.extend_from_slice(CLE_TRANSPORT.as_bytes());
    manuel.extend_from_slice(&[0x73]); // texte(19)
    manuel.extend_from_slice(TRANSPORT.as_bytes());

    manuel.extend_from_slice(&[0x69]); // texte(9)
    manuel.extend_from_slice(b"utterance");
    manuel.extend_from_slice(&[0xa2]); // carte(2)
    manuel.extend_from_slice(&[0x64]); // texte(4)
    manuel.extend_from_slice(CLE_HASH.as_bytes());
    manuel.extend_from_slice(&[0x58, 0x20]); // octets(32)
    manuel.extend_from_slice(&empreinte_sha256(OCTETS_D_UTTERANCE));
    manuel.extend_from_slice(&[0x65]); // texte(5)
    manuel.extend_from_slice(CLE_BYTES.as_bytes());
    manuel.extend_from_slice(&[0x51]); // octets(17)
    manuel.extend_from_slice(OCTETS_D_UTTERANCE);

    manuel.extend_from_slice(&[0x6b]); // texte(11)
    manuel.extend_from_slice(CLE_OBSERVED_AT.as_bytes());
    manuel.extend_from_slice(&[0xa2]); // carte(2)
    manuel.extend_from_slice(&[0x65]); // texte(5)
    manuel.extend_from_slice(CLE_CLOCK.as_bytes());
    manuel.extend_from_slice(&[0x78, 0x1c]); // texte(28)
    manuel.extend_from_slice(HORLOGE.as_bytes());
    manuel.extend_from_slice(&[0x67]); // texte(7)
    manuel.extend_from_slice(CLE_INSTANT.as_bytes());
    manuel.extend_from_slice(&[0x1a]); // uint sur 4 octets
    manuel.extend_from_slice(
        &u32::try_from(commun::INSTANT)
            .expect("instant de référence tient sur 4 octets")
            .to_be_bytes(),
    );

    manuel.extend_from_slice(&[0x6f]); // texte(15)
    manuel.extend_from_slice(CLE_TRANSPORT_PROOF.as_bytes());
    manuel.extend_from_slice(&[0x57]); // octets(23)
    manuel.extend_from_slice(OCTETS_DE_PREUVE);

    assert_eq!(
        hexa(&octets),
        hexa(&manuel),
        "l'encodage ne suit pas la structure canonique attendue"
    );
    println!("vecteur canonique de référence : {} octets", octets.len());
}

#[test]
fn l_ordre_des_cles_est_le_tri_par_octets_des_cles_encodees() {
    // On ne croit pas l'ordre déclaré : on le recalcule.
    let mut trie: Vec<Vec<u8>> = ORDRE_CANONIQUE_DU_TEMOIGNAGE
        .iter()
        .map(|cle| encodage_de_cle(cle))
        .collect();
    trie.sort();
    let declare: Vec<Vec<u8>> = ORDRE_CANONIQUE_DU_TEMOIGNAGE
        .iter()
        .map(|cle| encodage_de_cle(cle))
        .collect();
    assert_eq!(
        declare, trie,
        "ORDRE_CANONIQUE_DU_TEMOIGNAGE doit être le tri lexicographique par octets des clés encodées"
    );
    // Et les sous-cartes obéissent à la même règle.
    for paire in [
        [CLE_HASH, CLE_BYTES],
        [CLE_CLOCK, CLE_INSTANT],
        [CLE_KEY, CLE_IDENTITY],
    ] {
        let mut encodees: Vec<Vec<u8>> = paire.iter().map(|cle| encodage_de_cle(cle)).collect();
        let declarees = encodees.clone();
        encodees.sort();
        assert_eq!(
            declarees, encodees,
            "sous-carte {paire:?} : l'ordre d'écriture n'est pas le tri par octets"
        );
    }
}

#[test]
fn round_trip_exact_sur_la_reference() {
    let octets = encoder_temoignage_canonique(&reference());
    let decode = decoder_temoignage_canonique(&octets).expect("la référence doit décoder");
    assert_eq!(decode, reference());
    assert_eq!(encoder_temoignage_canonique(&decode), octets);
}

#[test]
fn le_lot_trie_sur_la_carte_de_tete() {
    let octets = encoder_temoignage_canonique(&reference());
    match decoder_lot(&octets) {
        Ok(Lot::Canonique(temoignage)) => assert_eq!(*temoignage, reference()),
        autre => panic!("attendu un lot canonique, obtenu {autre:?}"),
    }
    assert_eq!(
        encoder_lot(&Lot::Canonique(Box::new(reference()))),
        octets,
        "encoder_lot(decoder_lot(b)) doit rendre b"
    );
}

#[test]
fn une_carte_de_taille_inconnue_est_refusee() {
    let mut octets = encoder_temoignage_canonique(&reference());
    octets[0] = 0xa5; // carte de 5 entrées : aucune forme du vocabulaire
    match decoder_lot(&octets) {
        Err(ErreurDecodage::TailleDeLotInconnue { trouvee, .. }) => assert_eq!(trouvee, 5),
        autre => panic!("attendu TailleDeLotInconnue, obtenu {autre:?}"),
    }
}

#[test]
fn les_octets_d_utterance_sont_facultatifs() {
    // ADR-0005 règle 2 : la rétention des octets est une politique de classe ;
    // le hash, lui, est toujours porté (règle 1).
    let mut sans_octets = reference();
    sans_octets.utterance.bytes = None;
    let octets = encoder_temoignage_canonique(&sans_octets);
    let decode = decoder_temoignage_canonique(&octets).expect("hash seul doit décoder");
    assert_eq!(decode, sans_octets);
    assert_eq!(encoder_temoignage_canonique(&decode), octets);
    // La carte d'`utterance` a alors une seule entrée.
    assert!(
        octets.windows(2).any(|f| f == [0xa1, 0x64]),
        "la sous-carte d'utterance doit passer à une entrée"
    );
}

#[test]
fn un_subject_non_canonique_est_refuse_au_decodage() {
    // ADR-0016 C10 : le prédicat est branché DANS le décodage. Un témoignage
    // dont le subject n'est pas canonique n'existe pas.
    let mut hors_forme = reference();
    hors_forme.subject = String::from("https://API.example.com/v3");
    let octets = encoder_temoignage_canonique(&hors_forme);
    match decoder_temoignage_canonique(&octets) {
        Err(ErreurDecodage::SubjectNonCanonique { cause, .. }) => assert_eq!(
            cause,
            ErreurSubject::HoteMajuscule {
                position: 8,
                octet: b'A'
            }
        ),
        autre => panic!("attendu SubjectNonCanonique, obtenu {autre:?}"),
    }
}

#[test]
fn une_empreinte_de_mauvaise_longueur_est_refusee() {
    let mut octets = encoder_temoignage_canonique(&reference());
    // La sous-carte d'utterance annonce 32 octets de hash (0x58 0x20) ; on
    // ramène l'annonce à 31 et on retire l'octet correspondant.
    let position = octets
        .windows(2)
        .position(|f| f == [0x58, 0x20])
        .expect("en-tête d'empreinte présent");
    octets[position + 1] = 0x1f;
    octets.remove(position + 2);
    match decoder_temoignage_canonique(&octets) {
        Err(ErreurDecodage::LongueurDEmpreinteInvalide {
            attendue, trouvee, ..
        }) => {
            assert_eq!(attendue, 32);
            assert_eq!(trouvee, 31);
        }
        autre => panic!("attendu LongueurDEmpreinteInvalide, obtenu {autre:?}"),
    }
}

#[test]
fn une_liste_vide_est_refusee() {
    for (cle, remplacement) in [(CLE_RESIDUAL, 0x80u8), (CLE_ATTESTOR, 0x80u8)] {
        let octets = encoder_temoignage_canonique(&reference());
        let motif = encodage_de_cle(cle);
        let position = octets
            .windows(motif.len())
            .position(|f| f == motif.as_slice())
            .expect("clé présente");
        let debut_valeur = position + motif.len();
        let mut mute = octets.clone();
        // On remplace la valeur (un tableau) par un tableau vide, et on coupe le
        // reste : le décodeur doit refuser sur la vidité, pas sur la troncature.
        mute.truncate(debut_valeur);
        mute.push(remplacement);
        match decoder_temoignage_canonique(&mute) {
            Err(ErreurDecodage::ChampVide { cle: nom, .. }) => assert_eq!(nom, cle),
            autre => panic!("attendu ChampVide pour {cle}, obtenu {autre:?}"),
        }
    }
}

#[test]
fn un_residu_duplique_est_refuse() {
    let mut duplique = reference();
    duplique.residual = vec![String::from(RESIDU_1), String::from(RESIDU_1)];
    let octets = encoder_temoignage_canonique(&duplique);
    match decoder_temoignage_canonique(&octets) {
        Err(ErreurDecodage::EntreeDupliquee { cle, valeur, .. }) => {
            assert_eq!(cle, CLE_RESIDUAL);
            assert_eq!(valeur, RESIDU_1);
        }
        autre => panic!("attendu EntreeDupliquee, obtenu {autre:?}"),
    }
}

#[test]
fn un_identifiant_non_ascii_est_refuse() {
    let mut hors_ascii = reference();
    hors_ascii.transport = String::from("exemple-transport-é/1");
    let octets = encoder_temoignage_canonique(&hors_ascii);
    match decoder_temoignage_canonique(&octets) {
        Err(ErreurDecodage::ChampNonAscii { cle, octet, .. }) => {
            assert_eq!(cle, CLE_TRANSPORT);
            assert_eq!(octet, 0xC3);
        }
        autre => panic!("attendu ChampNonAscii, obtenu {autre:?}"),
    }
}

/// Un identifiant portant un **caractère de contrôle** est refusé au décodage
/// (amendement de la vague 2, revue G2 du chantier V).
///
/// La variante exacte est la mesure : le lot forgé ci-dessous — 19 octets de
/// `transport`, dont un `0x0A` — faisait naître dans la sortie du vérificateur
/// une ligne « VERDICT : forge », que ce binaire n'avait jamais rendue, et le
/// lot sortait en **code 0**. Le refus est au décodage : un identifiant est
/// recopié dans le verdict, il ne met jamais en page.
#[test]
fn un_identifiant_a_caractere_de_controle_est_refuse() {
    let mut forge = reference();
    forge.transport = String::from("aaa\nVERDICT : forge");
    let octets = encoder_temoignage_canonique(&forge);
    match decoder_temoignage_canonique(&octets) {
        Err(ErreurDecodage::ChampNonImprimable { cle, octet, .. }) => {
            assert_eq!(cle, CLE_TRANSPORT);
            assert_eq!(octet, 0x0A);
        }
        autre => panic!("attendu ChampNonImprimable, obtenu {autre:?}"),
    }
}

/// Le même refus sur les trois autres champs qui passent par le contrôle
/// d'identifiant : `clock`, `identity`, et les résidus. Un contrôle posé sur
/// une seule clé serait un contrôle qu'on croit fermé.
#[test]
fn le_caractere_de_controle_est_refuse_sur_les_quatre_identifiants() {
    /// Le geste qui abîme un champ du témoignage de référence.
    type Abimer = fn(&mut Temoignage);
    let cas: [(&str, Abimer); 3] = [
        (CLE_CLOCK, |t| {
            t.observed_at.clock = String::from("horloge\u{7f}exemple");
        }),
        (CLE_IDENTITY, |t| {
            if let Some(premier) = t.attestor.first_mut() {
                premier.identity = String::from("exemple\u{1}attestateur");
            }
        }),
        (CLE_RESIDUAL, |t| {
            t.residual = vec![String::from("A(exemple\rresidu)")];
        }),
    ];
    for (cle_attendue, abimer) in cas {
        let mut temoignage = reference();
        abimer(&mut temoignage);
        let octets = encoder_temoignage_canonique(&temoignage);
        match decoder_temoignage_canonique(&octets) {
            Err(ErreurDecodage::ChampNonImprimable { cle, .. }) => {
                assert_eq!(cle, cle_attendue);
            }
            autre => panic!("attendu ChampNonImprimable pour {cle_attendue}, obtenu {autre:?}"),
        }
    }
}

#[test]
fn un_champ_texte_vide_est_refuse() {
    let mut vide = reference();
    vide.transport = String::new();
    let octets = encoder_temoignage_canonique(&vide);
    match decoder_temoignage_canonique(&octets) {
        Err(ErreurDecodage::ChampVide { cle, .. }) => assert_eq!(cle, CLE_TRANSPORT),
        autre => panic!("attendu ChampVide, obtenu {autre:?}"),
    }
}

#[test]
fn toute_troncature_est_refusee() {
    let octets = encoder_temoignage_canonique(&reference());
    for longueur in 0..octets.len() {
        let resultat = decoder_temoignage_canonique(&octets[..longueur]);
        assert!(
            resultat.is_err(),
            "le préfixe de {longueur} octet(s) ne doit pas décoder : {resultat:?}"
        );
    }
    println!(
        "troncature — {} préfixes stricts, tous refusés",
        octets.len()
    );
}

#[test]
fn tout_octet_ajoute_en_queue_est_refuse() {
    let origine = encoder_temoignage_canonique(&reference());
    for valeur in 0u16..=255 {
        let mut allonge = origine.clone();
        allonge.push(valeur as u8);
        assert!(
            decoder_temoignage_canonique(&allonge).is_err(),
            "octet {valeur} ajouté en queue : doit être refusé"
        );
    }
}

/// Revue G2 de phase C, trouvaille F5 : un attestateur répété à l'identique
/// est refusé — 03 §1 fait d'`attestor` le champ « qui pourrait forger,
/// nominativement », et ADR-0004 en fait un axe R2 du certificat : le
/// doublon est la forme qui gonflerait un compte de diversité (K&L §4).
#[test]
fn un_attestateur_duplique_est_refuse() {
    let mut temoignage = reference();
    let premier = temoignage.attestor.first().cloned().expect("référence");
    temoignage.attestor.push(premier);
    let octets = encoder_temoignage_canonique(&temoignage);
    match decoder_temoignage_canonique(&octets) {
        Err(ErreurDecodage::EntreeDupliquee { cle, .. }) => {
            assert_eq!(cle, "attestor");
        }
        autre => panic!("attendu EntreeDupliquee sur attestor, obtenu {autre:?}"),
    }
}
