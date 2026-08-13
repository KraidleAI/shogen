//! **Le constructeur, testé — jamais prouvé** (ADR-0001).
//!
//! Deux étages : la construction de `subject` depuis des octets émis (le seul
//! endroit du dépôt où une normalisation d'ADR-0016 a lieu), et la construction
//! entière contre les **artefacts réels** du binaire compagnon.
//!
//! Ce que ces tests établissent : *tested* sur ces cas, à la date. Ils
//! n'établissent pas que tout constructeur possible produirait le même lot —
//! l'oracle de cette question est le prédicat du cœur, et il est appelé à
//! chaque construction.

use std::path::{Path, PathBuf};

use shogen_temoignage::{Entrees, Erreur, construire, subject_depuis_la_requete, valeur_texte};

/// Les artefacts de la session attestée réelle du 2026-08-13.
fn artefacts() -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("..")
        .join("shogen-tlsn-verify")
        .join("fixtures")
}

fn lire(nom: &str) -> Vec<u8> {
    std::fs::read(artefacts().join(nom)).expect("artefact réel présent")
}

fn texte_du_constat() -> String {
    String::from_utf8(lire("shogen-s3-binance.constat.json")).expect("constat en US-ASCII")
}

const RESIDUS: &[&str] = &["A(notary-neutrality)", "A(self-attestation)"];

fn entrees<'a>(emis: &'a [u8], recus: &'a [u8], preuve: &'a [u8], constat: &'a str) -> Entrees<'a> {
    Entrees {
        octets_emis: emis,
        octets_recus: recus,
        octets_de_preuve: preuve,
        texte_du_constat: constat,
        transport: "tlsn-mpc/1",
        identite_de_l_attestateur: "shogen:attestateur-de-demonstration-s3",
        horloge: "tlsn-mpc/1:connection_info.time",
        residus: RESIDUS,
    }
}

// ---------------------------------------------------------------------------
// `subject` — la seule normalisation du dépôt (ADR-0016 C0)
// ---------------------------------------------------------------------------

#[test]
fn le_subject_vient_de_la_requete_reellement_emise() {
    let emis = lire("shogen-s3-binance.sent-revele.bin");
    let subject = subject_depuis_la_requete(&emis).expect("la requête réelle est exploitable");
    assert_eq!(
        subject,
        "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    );
}

#[test]
fn l_hote_est_plie_en_minuscules_et_le_port_par_defaut_omis() {
    // C3 (casse de l'hôte) et C5 (port par défaut) : normalisés **ici**, une
    // fois, et jamais au vérificateur.
    let requete = "GET /v1/prix HTTP/1.1\r\nHost: API.Example.COM:443\r\n\r\n";
    assert_eq!(
        subject_depuis_la_requete(requete.as_bytes()).expect("canonique"),
        "https://api.example.com/v1/prix"
    );
}

#[test]
fn la_requete_est_reprise_verbatim_jamais_triee() {
    // C8 : aucun tri, aucune déduplication, aucune fusion de clés répétées.
    let requete = "GET /v1/p?b=2&a=1&a=3 HTTP/1.1\r\nhost: api.example.com\r\n\r\n";
    assert_eq!(
        subject_depuis_la_requete(requete.as_bytes()).expect("canonique"),
        "https://api.example.com/v1/p?b=2&a=1&a=3"
    );
}

#[test]
fn une_requete_sans_entete_host_est_refusee() {
    let requete = "GET /v1/prix HTTP/1.1\r\naccept: */*\r\n\r\n";
    assert_eq!(
        subject_depuis_la_requete(requete.as_bytes()),
        Err(Erreur::EnteteHostAbsente)
    );
}

#[test]
fn une_cible_non_absolue_est_refusee() {
    let requete = "GET v1/prix HTTP/1.1\r\nhost: api.example.com\r\n\r\n";
    assert!(matches!(
        subject_depuis_la_requete(requete.as_bytes()),
        Err(Erreur::CibleNonAbsolue { .. })
    ));
}

#[test]
fn une_ligne_de_requete_mal_formee_est_refusee() {
    let requete = "GET /v1/prix\r\nhost: api.example.com\r\n\r\n";
    assert!(matches!(
        subject_depuis_la_requete(requete.as_bytes()),
        Err(Erreur::LigneDeRequeteMalFormee { .. })
    ));
    assert_eq!(
        subject_depuis_la_requete(b""),
        Err(Erreur::LigneDeRequeteAbsente)
    );
}

#[test]
fn un_hote_hors_forme_est_refuse_par_le_predicat_du_coeur() {
    // Le désaccord constructeur/prédicat est un ROUGE (ADR-0016 C10) : ici le
    // constructeur ne peut PAS produire une forme canonique, et il le dit au
    // lieu de la rattraper.
    let requete = "GET /v1/prix HTTP/1.1\r\nhost: 192.0.2.1\r\n\r\n";
    assert!(matches!(
        subject_depuis_la_requete(requete.as_bytes()),
        Err(Erreur::SubjectNonCanonique { .. })
    ));
}

// ---------------------------------------------------------------------------
// L'extraction minimale du constat
// ---------------------------------------------------------------------------

#[test]
fn l_extraction_lit_les_valeurs_du_constat_reel() {
    let constat = texte_du_constat();
    assert_eq!(
        valeur_texte(&constat, "server_name").expect("clé présente"),
        "api.binance.com"
    );
    assert_eq!(
        valeur_texte(&constat, "revision_amont").expect("clé présente"),
        "0fe3c32d35382b3f290a43c4156399ca4512bb89"
    );
    assert!(matches!(
        valeur_texte(&constat, "cle_absente"),
        Err(Erreur::CleDuConstatIllisible { .. })
    ));
}

// ---------------------------------------------------------------------------
// La construction entière, contre les artefacts réels
// ---------------------------------------------------------------------------

#[test]
fn le_temoignage_reel_se_construit_et_porte_ses_sept_champs() {
    let emis = lire("shogen-s3-binance.sent-revele.bin");
    let recus = lire("shogen-s3-binance.recv-revele.bin");
    let preuve = lire("shogen-s3-binance.presentation.tlsn");
    let constat = texte_du_constat();
    let temoignage =
        construire(&entrees(&emis, &recus, &preuve, &constat)).expect("les recoupements tiennent");

    assert_eq!(
        temoignage.subject,
        "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    );
    assert_eq!(temoignage.transport, "tlsn-mpc/1");
    assert_eq!(temoignage.observed_at.instant, 1_786_594_228);
    assert_eq!(temoignage.residual, RESIDUS);
    assert_eq!(temoignage.transport_proof.len(), 6034);
    assert_eq!(temoignage.utterance.bytes.as_ref().map(Vec::len), Some(944));
    // La convention d'épinglage : la ligne même que le compagnon a déposée.
    let deposee =
        String::from_utf8(lire("shogen-s3-binance.attestor-verifying-key.txt")).expect("US-ASCII");
    assert_eq!(
        String::from_utf8(temoignage.attestor[0].key.clone()).expect("US-ASCII"),
        deposee.trim()
    );
}

#[test]
fn un_octet_recu_de_travers_rompt_le_recoupement_d_empreinte() {
    let emis = lire("shogen-s3-binance.sent-revele.bin");
    let mut recus = lire("shogen-s3-binance.recv-revele.bin");
    let preuve = lire("shogen-s3-binance.presentation.tlsn");
    let constat = texte_du_constat();
    recus[0] ^= 0x01;
    match construire(&entrees(&emis, &recus, &preuve, &constat)) {
        Err(Erreur::RecoupementRompu { quoi, .. }) => {
            assert_eq!(quoi, "empreinte des octets reçus");
        }
        autre => panic!("le recoupement devait tomber : {autre:?}"),
    }
}

#[test]
fn une_preuve_tronquee_rompt_le_recoupement_de_taille() {
    let emis = lire("shogen-s3-binance.sent-revele.bin");
    let recus = lire("shogen-s3-binance.recv-revele.bin");
    let mut preuve = lire("shogen-s3-binance.presentation.tlsn");
    let constat = texte_du_constat();
    preuve.truncate(6000);
    match construire(&entrees(&emis, &recus, &preuve, &constat)) {
        Err(Erreur::RecoupementRompu { quoi, .. }) => {
            // L'empreinte tombe la première : elle est plus fine que la taille.
            assert_eq!(quoi, "empreinte de la preuve de transport");
        }
        autre => panic!("le recoupement devait tomber : {autre:?}"),
    }
}

#[test]
fn un_constat_sans_succes_est_refuse_avant_toute_construction() {
    let emis = lire("shogen-s3-binance.sent-revele.bin");
    let recus = lire("shogen-s3-binance.recv-revele.bin");
    let preuve = lire("shogen-s3-binance.presentation.tlsn");
    let constat =
        texte_du_constat().replace("\"presentation_verifiee\"", "\"verification_refusee\"");
    match construire(&entrees(&emis, &recus, &preuve, &constat)) {
        Err(Erreur::RecoupementRompu { quoi, .. }) => assert_eq!(quoi, "verdict du constat"),
        autre => panic!("un constat sans succès ne construit rien : {autre:?}"),
    }
}

#[test]
fn une_liste_de_residus_vide_est_refusee() {
    let emis = lire("shogen-s3-binance.sent-revele.bin");
    let recus = lire("shogen-s3-binance.recv-revele.bin");
    let preuve = lire("shogen-s3-binance.presentation.tlsn");
    let constat = texte_du_constat();
    let mut entrees = entrees(&emis, &recus, &preuve, &constat);
    entrees.residus = &[];
    assert_eq!(construire(&entrees), Err(Erreur::ResidusVides));
}

#[test]
fn chaque_refus_du_constructeur_s_imprime() {
    let cas = [
        Erreur::LigneDeRequeteAbsente,
        Erreur::EnteteHostAbsente,
        Erreur::ResidusVides,
        Erreur::CibleNonAbsolue {
            cible: String::from("v1"),
        },
        Erreur::LigneDeRequeteMalFormee {
            ligne: String::from("GET"),
        },
        Erreur::SubjectNonCanonique {
            subject: String::from("https://X/"),
            cause: String::from("majuscule dans l'hôte"),
        },
        Erreur::CleDuConstatIllisible {
            cle: String::from("x"),
        },
        Erreur::ValeurDuConstatMalFormee {
            cle: String::from("x"),
            valeur: String::from("y"),
        },
        Erreur::RecoupementRompu {
            quoi: String::from("x"),
            constate: String::from("a"),
            mesure: String::from("b"),
        },
    ];
    for erreur in cas {
        let rendu = erreur.to_string();
        assert!(
            rendu.len() > 20,
            "un refus dit ce qui l'a produit : « {rendu} »"
        );
        println!("{rendu}");
    }
}
