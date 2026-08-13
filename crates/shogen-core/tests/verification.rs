//! **Les trois mutants du critère de S3, au rang du cœur.**
//!
//! Rattachement : **05 §S3 / 13 §1** — le critère de sortie exige que le
//! vérificateur « échoue (fail-closed, raison structurée) sur les 3 mutants
//! semés : **preuve altérée, hash d'utterance faux, résidu non résolu** » ;
//! **ADR-0015 point 8** (la forme exacte des contrôles) ; **ADR-0005 règle 1**.
//!
//! Les trois mutants sont ici des **cas de test nommés**, pas des démonstrations
//! manuelles (13 §4, phase C). Le même trio est rejoué sur le binaire, à
//! travers des fichiers, dans `crates/shogen-verifier/tests/`.
//!
//! *La règle gatewright, transposée : un vérificateur qui n'a jamais rejeté n'a
//! rien montré.*

mod commun;

use commun::{OCTETS_D_UTTERANCE, OCTETS_DE_PREUVE, RESIDU_1, constat, reference, registre};
use shogen_core::{
    ErreurVerification, RESIDU_DE_LA_DELEGATION, empreinte_sha256, verifier_temoignage,
};

#[test]
fn temoignage_intact_le_verdict_nomme_ses_residus_et_la_delegation() {
    let verdict = verifier_temoignage(&reference(), &registre(), Some(&constat()))
        .expect("le témoignage de référence doit passer les trois contrôles");
    assert_eq!(
        verdict.residus,
        vec![
            String::from(RESIDU_1),
            String::from(commun::RESIDU_2),
            String::from(RESIDU_DE_LA_DELEGATION),
        ],
        "le verdict nomme les résidus du témoignage PUIS celui de la délégation"
    );
    assert!(
        verdict.octets_recalcules,
        "les octets étaient portés : la liaison a été recalculée ici"
    );
    assert_eq!(verdict.outil_delegue, commun::OUTIL);
    println!(
        "verdict — résidus nommés : {:?} ; contrôle cryptographique délégué à « {} »",
        verdict.residus, verdict.outil_delegue
    );
}

#[test]
fn mutant_1_preuve_alteree() {
    // Un octet de `transport_proof` change : le lot ne porte plus la preuve qui
    // a été vérifiée. C'est ce qui interdit de vérifier une preuve et d'en
    // livrer une autre (ADR-0015, point 8 alinéa c).
    let mut altere = reference();
    let mut preuve = OCTETS_DE_PREUVE.to_vec();
    preuve[0] ^= 0x01;
    altere.transport_proof = preuve.clone();

    match verifier_temoignage(&altere, &registre(), Some(&constat())) {
        Err(ErreurVerification::PreuveNonConstatee {
            calculee,
            constatee,
        }) => {
            assert_eq!(calculee, empreinte_sha256(&preuve));
            assert_eq!(constatee, empreinte_sha256(OCTETS_DE_PREUVE));
        }
        autre => panic!("attendu PreuveNonConstatee, obtenu {autre:?}"),
    }
}

#[test]
fn mutant_2_hash_d_utterance_faux() {
    // Le hash porté ne correspond plus aux octets portés : la liaison
    // témoignage → preuve est rompue à l'intérieur même du témoignage
    // (ADR-0005 règle 1).
    let mut faux = reference();
    faux.utterance.hash[0] ^= 0x01;

    match verifier_temoignage(&faux, &registre(), Some(&constat())) {
        Err(ErreurVerification::LiaisonUtteranceRompue { portee, calculee }) => {
            assert_eq!(portee, faux.utterance.hash);
            assert_eq!(calculee, empreinte_sha256(OCTETS_D_UTTERANCE));
        }
        autre => panic!("attendu LiaisonUtteranceRompue, obtenu {autre:?}"),
    }
}

#[test]
fn mutant_2_bis_hash_juste_mais_octets_changes() {
    // La même liaison, prise par l'autre bout : les octets changent et le hash
    // suit. Le témoignage est alors cohérent avec lui-même — et c'est le
    // **constat du compagnon** qui le refuse. Sans cette seconde moitié, un
    // producteur malhonnête n'aurait qu'à recalculer le hash.
    let mut recompose = reference();
    let octets = b"{\"price\":\"99.99\"}".to_vec();
    recompose.utterance.hash = empreinte_sha256(&octets);
    recompose.utterance.bytes = Some(octets.clone());

    match verifier_temoignage(&recompose, &registre(), Some(&constat())) {
        Err(ErreurVerification::UtteranceNonConstatee { portee, constatee }) => {
            assert_eq!(portee, empreinte_sha256(&octets));
            assert_eq!(constatee, empreinte_sha256(OCTETS_D_UTTERANCE));
        }
        autre => panic!("attendu UtteranceNonConstatee, obtenu {autre:?}"),
    }
}

#[test]
fn mutant_3_residu_non_resolu() {
    // Le témoignage nomme un résidu qui ne figure pas au registre publié : le
    // verdict ne peut pas dire « sous A(...) » pour un A(...) que personne n'a
    // publié (03 §4, point 3).
    let mut inconnu = reference();
    inconnu.residual = vec![String::from("A(residu-jamais-publie)")];

    match verifier_temoignage(&inconnu, &registre(), Some(&constat())) {
        Err(ErreurVerification::ResiduNonResolu { residu }) => {
            assert_eq!(residu, "A(residu-jamais-publie)");
        }
        autre => panic!("attendu ResiduNonResolu, obtenu {autre:?}"),
    }
}

#[test]
fn un_registre_sans_le_residu_de_delegation_est_refuse() {
    // Le registre publié DOIT enregistrer la délégation : un registre qui ne la
    // porte pas n'est pas le registre publié, et un verdict qui la tairait
    // vendrait un contrôle qui n'a pas eu lieu ici.
    let registre_incomplet = vec![String::from(RESIDU_1), String::from(commun::RESIDU_2)];
    match verifier_temoignage(&reference(), &registre_incomplet, Some(&constat())) {
        Err(ErreurVerification::ResiduNonResolu { residu }) => {
            assert_eq!(residu, RESIDU_DE_LA_DELEGATION);
        }
        autre => panic!("attendu ResiduNonResolu sur la délégation, obtenu {autre:?}"),
    }
}

#[test]
fn sans_constat_le_verdict_est_le_refus() {
    // Fail-safe defaults (ADR-0010, point 5) : ce qui n'a pas été établi n'est
    // pas admis par défaut.
    match verifier_temoignage(&reference(), &registre(), None) {
        Err(ErreurVerification::ConstatAbsent) => {}
        autre => panic!("attendu ConstatAbsent, obtenu {autre:?}"),
    }
}

#[test]
fn un_registre_vide_est_refuse() {
    match verifier_temoignage(&reference(), &[], Some(&constat())) {
        Err(ErreurVerification::RegistreVide) => {}
        autre => panic!("attendu RegistreVide, obtenu {autre:?}"),
    }
}

#[test]
fn un_temoignage_sans_octets_reste_verifiable_et_le_verdict_le_dit() {
    // ADR-0005 règle 2 : les octets sont une politique de classe. Sans eux, la
    // liaison n'est pas recalculée **ici** — elle repose entièrement sur le
    // constat, et le verdict le déclare plutôt que de le taire.
    let mut hash_seul = reference();
    hash_seul.utterance.bytes = None;
    let verdict = verifier_temoignage(&hash_seul, &registre(), Some(&constat()))
        .expect("un témoignage à hash seul reste vérifiable");
    assert!(
        !verdict.octets_recalcules,
        "sans octets portés, rien n'a été recalculé ici"
    );
}

#[test]
fn les_refus_se_disent_en_toutes_lettres() {
    let refus = [
        ErreurVerification::ConstatAbsent,
        ErreurVerification::RegistreVide,
        ErreurVerification::LiaisonUtteranceRompue {
            portee: empreinte_sha256(b"a"),
            calculee: empreinte_sha256(b"b"),
        },
        ErreurVerification::UtteranceNonConstatee {
            portee: empreinte_sha256(b"a"),
            constatee: empreinte_sha256(b"b"),
        },
        ErreurVerification::PreuveNonConstatee {
            calculee: empreinte_sha256(b"a"),
            constatee: empreinte_sha256(b"b"),
        },
        ErreurVerification::ResiduNonResolu {
            residu: String::from("A(inconnu)"),
        },
    ];
    for erreur in refus {
        let rendu = format!("{erreur}");
        assert!(!rendu.trim().is_empty(), "refus muet : {erreur:?}");
    }
}
