//! **L'analyseur du constat, variante d'erreur par variante d'erreur.**
//!
//! Rattachement (G0) : **ADR-0015 point 13** (le contrat figé : une ligne JSON
//! à clés triées, dix-huit clés, `version_du_constat` = 1) ; **ADR-0010**
//! point 5 (*fail-safe defaults* : ce qui n'est pas énuméré est refusé) ;
//! **ADR-0011** point 1 (l'étage unitaire) ; **13 §7 dette 1** — la couverture
//! du vérificateur, dont le non-couvert résiduel vivait précisément dans
//! `analyser_constat` et ses chemins d'erreur.
//!
//! Chaque cas asserte **la variante exacte**, jamais « ça a refusé » : un refus
//! qui tombe pour la mauvaise raison est un test qui ne mesure pas ce qu'il
//! croit. C'est ce que le typage de `ErreurConstat` rend possible — un
//! `Result<_, String>` n'aurait laissé que la comparaison de messages.
//!
//! Le constat de référence est **le vrai** (`tests/fixtures/`), décomposé en
//! paires clé/valeur puis recomposé : chaque cas ne change qu'une chose, et le
//! reste est la pièce réelle.

use shogen_verifier::{CLES_DU_CONSTAT, ErreurConstat, analyser_constat};

/// Les dix-huit paires du constat réel, dans l'ordre du contrat — recopiées de
/// `tests/fixtures/s3-binance.constat.json` (lu, jamais de mémoire).
fn paires() -> Vec<(&'static str, String)> {
    vec![
        ("attestor_cle_algorithme", texte("k256")),
        (
            "attestor_cle_hex",
            texte("036aaecb211badf2f35932adc21268bea583ad1a34b9e0f0f4781557cfe9482271"),
        ),
        ("connection_info_time", String::from("1786594228")),
        ("connection_info_version_tls", texte("V1_2")),
        (
            "empreinte_presentation_sha256",
            texte("47c38169f7d79af924eb6e87969d94ab67838c1d6305cd69ef86ac1df9b18da5"),
        ),
        (
            "empreinte_recv_revele_sha256",
            texte("c28a41ce87dafcd313d301ab56472b6f3cd1b3d81d903da787b0ca9dfffbeea0"),
        ),
        (
            "empreinte_sent_revele_sha256",
            texte("4ad0e84b4f078e7ee62482ca86853c09e3c17bf074274168d65c024d1777e24b"),
        ),
        ("octets_presentation", String::from("6034")),
        (
            "revision_amont",
            texte("0fe3c32d35382b3f290a43c4156399ca4512bb89"),
        ),
        ("server_name", texte("api.binance.com")),
        ("transcript_recv_authentifie", String::from("944")),
        ("transcript_recv_longueur", String::from("944")),
        ("transcript_recv_longueur_attestee", String::from("944")),
        ("transcript_sent_authentifie", String::from("173")),
        ("transcript_sent_longueur", String::from("173")),
        ("transcript_sent_longueur_attestee", String::from("173")),
        ("verdict", texte("presentation_verifiee")),
        ("version_du_constat", String::from("1")),
    ]
}

fn texte(valeur: &str) -> String {
    format!("\"{valeur}\"")
}

/// Recompose la ligne du contrat depuis des paires.
fn ligne(paires: &[(&str, String)]) -> String {
    let mut rendu = String::from("{");
    for (rang, (cle, valeur)) in paires.iter().enumerate() {
        if rang != 0 {
            rendu.push(',');
        }
        rendu.push_str(&format!("\"{cle}\":{valeur}"));
    }
    rendu.push('}');
    rendu
}

/// La ligne de référence, avec une paire remplacée.
fn avec(cle: &str, valeur: &str) -> String {
    let mut paires = paires();
    for paire in paires.iter_mut() {
        if paire.0 == cle {
            paire.1 = String::from(valeur);
        }
    }
    ligne(&paires)
}

/// La ligne de référence, privée d'une paire.
fn sans(cle: &str) -> String {
    let paires: Vec<(&str, String)> = paires()
        .into_iter()
        .filter(|paire| paire.0 != cle)
        .collect();
    ligne(&paires)
}

fn refus(texte: &str) -> ErreurConstat {
    match analyser_constat(texte) {
        Ok(constat) => panic!("constat accepté alors qu'il devait être refusé : {constat:?}"),
        Err(erreur) => erreur,
    }
}

// ---------------------------------------------------------------------------
// Le chemin qui accepte — et ce qu'il rend
// ---------------------------------------------------------------------------

#[test]
fn le_constat_de_reference_est_accepte_et_sa_projection_est_celle_du_contrat() {
    let constat = analyser_constat(&ligne(&paires())).expect("le constat de référence est valide");
    assert_eq!(
        constat.revision_amont,
        "0fe3c32d35382b3f290a43c4156399ca4512bb89"
    );
    assert_eq!(constat.instant_de_connexion, 1_786_594_228);
    assert_eq!(constat.origine_authentifiee, "api.binance.com");
    // La convention d'épinglage : `<algorithme> <chiffres>`, en US-ASCII.
    assert_eq!(
        String::from_utf8(constat.cle_du_controle.clone()).expect("US-ASCII"),
        "k256 036aaecb211badf2f35932adc21268bea583ad1a34b9e0f0f4781557cfe9482271"
    );
    assert_eq!(constat.cle_du_controle.len(), 71);
    assert_eq!(
        shogen_core::empreinte_en_hexadecimal(&constat.empreinte_de_l_utterance),
        "c28a41ce87dafcd313d301ab56472b6f3cd1b3d81d903da787b0ca9dfffbeea0"
    );
    assert_eq!(
        shogen_core::empreinte_en_hexadecimal(&constat.empreinte_de_la_preuve),
        "47c38169f7d79af924eb6e87969d94ab67838c1d6305cd69ef86ac1df9b18da5"
    );
}

#[test]
fn le_constat_reel_versionne_est_accepte_tel_quel() {
    // Le fichier, pas sa reconstitution : c'est lui que le binaire lit, fin de
    // ligne comprise.
    let chemin = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("tests")
        .join("fixtures")
        .join("s3-binance.constat.json");
    let texte = std::fs::read_to_string(&chemin).expect("constat réel versionné");
    let constat = analyser_constat(&texte).expect("le constat réel est valide");
    assert_eq!(constat.origine_authentifiee, "api.binance.com");
    // Les paires de ce fichier de test et la pièce réelle disent la même chose :
    // si l'une bouge sans l'autre, ce test tombe.
    assert_eq!(
        constat,
        analyser_constat(&ligne(&paires())).expect("référence valide")
    );
}

#[test]
fn le_contrat_porte_dix_huit_cles_et_elles_sont_triees() {
    assert_eq!(CLES_DU_CONSTAT.len(), 18);
    let mut triees = CLES_DU_CONSTAT.to_vec();
    triees.sort_unstable();
    assert_eq!(
        triees.as_slice(),
        CLES_DU_CONSTAT.as_slice(),
        "le tableau du contrat EST l'ordre attendu : il doit être trié"
    );
    // Et il décrit exactement les paires du constat réel.
    let noms: Vec<&str> = paires().into_iter().map(|paire| paire.0).collect();
    assert_eq!(noms.as_slice(), CLES_DU_CONSTAT.as_slice());
}

// ---------------------------------------------------------------------------
// L'enveloppe
// ---------------------------------------------------------------------------

#[test]
fn une_entree_vide_est_refusee() {
    assert!(matches!(
        refus(""),
        ErreurConstat::FinPrematuree { position: 0, .. }
    ));
}

#[test]
fn une_enveloppe_qui_n_est_pas_un_objet_est_refusee() {
    assert!(matches!(
        refus("[1,2]"),
        ErreurConstat::CaractereInattendu {
            position: 0,
            trouve: b'[',
            ..
        }
    ));
}

#[test]
fn un_objet_tronque_est_refuse() {
    let complet = ligne(&paires());
    let tronque = complet.get(..complet.len() - 1).expect("bornes");
    assert!(matches!(
        refus(tronque),
        ErreurConstat::FinPrematuree { .. }
    ));
}

#[test]
fn des_octets_apres_l_objet_sont_refuses() {
    let mut deux = ligne(&paires());
    deux.push_str(&ligne(&paires()));
    assert!(matches!(
        refus(&deux),
        ErreurConstat::OctetsResiduels { .. }
    ));
}

#[test]
fn un_separateur_inconnu_entre_paires_est_refuse() {
    let ligne = ligne(&paires()).replacen("\",\"attestor_cle_hex\"", "\";\"attestor_cle_hex\"", 1);
    assert!(matches!(
        refus(&ligne),
        ErreurConstat::CaractereInattendu { trouve: b';', .. }
    ));
}

#[test]
fn un_deux_points_manquant_est_refuse() {
    let ligne =
        ligne(&paires()).replacen("\"version_du_constat\":1", "\"version_du_constat\"=1", 1);
    assert!(matches!(
        refus(&ligne),
        ErreurConstat::CaractereInattendu { trouve: b'=', .. }
    ));
}

#[test]
fn la_ligne_supporte_ses_fins_de_ligne_mais_pas_ses_espaces_interieurs() {
    // Un fichier finit par une fin de ligne : la refuser n'apprendrait rien.
    let avec_fin = format!("{}\r\n", ligne(&paires()));
    assert!(analyser_constat(&avec_fin).is_ok());
    // À l'intérieur, aucun espace : la mise en forme est un refus, pas une
    // normalisation (posture d'ADR-0016 C0).
    let aere = ligne(&paires()).replacen("{\"", "{ \"", 1);
    assert!(matches!(
        refus(&aere),
        ErreurConstat::CaractereInattendu { trouve: b' ', .. }
    ));
    let aere_valeur =
        ligne(&paires()).replacen("\"version_du_constat\":1", "\"version_du_constat\": 1", 1);
    assert!(matches!(
        refus(&aere_valeur),
        ErreurConstat::EspaceInterdit { .. }
    ));
}

// ---------------------------------------------------------------------------
// Les chaînes
// ---------------------------------------------------------------------------

#[test]
fn un_echappement_est_refuse_au_lieu_d_etre_interprete() {
    assert!(matches!(
        refus(&avec("server_name", "\"api.binance\\u002ecom\"")),
        ErreurConstat::EchappementInterdit { .. }
    ));
}

#[test]
fn un_octet_non_ascii_est_refuse() {
    assert!(matches!(
        refus(&avec("server_name", "\"api.binancé.com\"")),
        ErreurConstat::OctetNonAscii { .. }
    ));
}

#[test]
fn un_espace_dans_une_chaine_est_refuse() {
    assert!(matches!(
        refus(&avec("server_name", "\"api binance com\"")),
        ErreurConstat::EspaceInterdit { .. }
    ));
}

#[test]
fn un_octet_de_controle_dans_une_chaine_est_refuse() {
    assert!(matches!(
        refus(&avec("server_name", "\"api\u{7}binance.com\"")),
        ErreurConstat::CaractereInattendu { trouve: 0x07, .. }
    ));
}

#[test]
fn une_chaine_non_fermee_est_refusee() {
    let ligne = ligne(&paires()).replacen("\"verdict\"", "\"verdict", 1);
    assert!(matches!(refus(&ligne), ErreurConstat::CleInconnue { .. }));
    // Et la fin prématurée franche : la dernière valeur privée de son guillemet.
    let mut tronque = ligne_sans_fermeture();
    tronque.push('}');
    assert!(matches!(
        refus(&tronque),
        ErreurConstat::FinPrematuree { .. } | ErreurConstat::CaractereInattendu { .. }
    ));
}

fn ligne_sans_fermeture() -> String {
    String::from("{\"attestor_cle_algorithme\":\"k256")
}

// ---------------------------------------------------------------------------
// Les clés
// ---------------------------------------------------------------------------

#[test]
fn une_cle_inconnue_est_refusee_et_nommee() {
    let ligne = ligne(&paires()).replacen("\"server_name\"", "\"server_names\"", 1);
    match refus(&ligne) {
        ErreurConstat::CleInconnue { cle, .. } => assert_eq!(cle, "server_names"),
        autre => panic!("variante inattendue : {autre:?}"),
    }
}

#[test]
fn une_cle_repetee_est_refusee_et_nommee() {
    let ligne = ligne(&paires()).replacen(
        "\"server_name\":\"api.binance.com\"",
        "\"server_name\":\"api.binance.com\",\"server_name\":\"api.binance.com\"",
        1,
    );
    match refus(&ligne) {
        ErreurConstat::CleRepetee { cle, .. } => assert_eq!(cle, "server_name"),
        autre => panic!("variante inattendue : {autre:?}"),
    }
}

/// Les paires de référence, les deux premières échangées : même contenu, ordre
/// différent — le contrat veut l'ordre.
fn paires_permutees() -> Vec<(&'static str, String)> {
    let mut paires = paires();
    paires.swap(0, 1);
    paires
}

#[test]
fn des_cles_non_triees_sont_refusees() {
    let paires = paires_permutees();
    match refus(&ligne(&paires)) {
        ErreurConstat::CleNonTriee {
            precedente, cle, ..
        } => {
            assert_eq!(precedente, "attestor_cle_hex");
            assert_eq!(cle, "attestor_cle_algorithme");
        }
        autre => panic!("variante inattendue : {autre:?}"),
    }
}

#[test]
fn chaque_cle_du_contrat_est_exigee() {
    // Le contrôle porte sur les DIX-HUIT : retirer n'importe laquelle est un
    // refus, et le refus la nomme. Un contrat dont une seule clé serait
    // facultative ne serait pas figé.
    for cle in CLES_DU_CONSTAT {
        let erreur = refus(&sans(cle));
        match erreur {
            ErreurConstat::CleManquante { cle: manquante } => assert_eq!(manquante, cle),
            // `version_du_constat` et `verdict` sont lus en tête : retirer une
            // autre clé peut faire tomber leur contrôle d'abord si le retrait
            // les emporte — ce n'est pas le cas ici, mais le test le dirait.
            autre => panic!("clé « {cle} » retirée : variante inattendue {autre:?}"),
        }
    }
}

// ---------------------------------------------------------------------------
// Les types et les valeurs
// ---------------------------------------------------------------------------

#[test]
fn un_entier_la_ou_une_chaine_est_attendue_est_refuse() {
    match refus(&avec("server_name", "1786594228")) {
        ErreurConstat::TypeInattendu { cle, .. } => assert_eq!(cle, "server_name"),
        autre => panic!("variante inattendue : {autre:?}"),
    }
}

#[test]
fn une_chaine_la_ou_un_entier_est_attendu_est_refusee() {
    match refus(&avec("connection_info_time", "\"1786594228\"")) {
        ErreurConstat::TypeInattendu { cle, .. } => assert_eq!(cle, "connection_info_time"),
        autre => panic!("variante inattendue : {autre:?}"),
    }
}

#[test]
fn une_valeur_qui_n_est_ni_chaine_ni_entier_est_refusee() {
    assert!(matches!(
        refus(&avec("connection_info_time", "true")),
        ErreurConstat::CaractereInattendu { trouve: b't', .. }
    ));
    assert!(matches!(
        refus(&avec("connection_info_time", "-1")),
        ErreurConstat::CaractereInattendu { trouve: b'-', .. }
    ));
}

#[test]
fn une_valeur_absente_en_fin_de_ligne_est_refusee() {
    assert!(matches!(
        refus("{\"attestor_cle_algorithme\":"),
        ErreurConstat::FinPrematuree { .. }
    ));
}

#[test]
fn un_entier_a_zero_de_tete_est_refuse() {
    assert!(matches!(
        refus(&avec("octets_presentation", "06034")),
        ErreurConstat::EntierNonCanonique { .. }
    ));
}

#[test]
fn un_entier_hors_plage_est_refuse_au_lieu_de_deborder() {
    // Vingt chiffres de 9 : au-delà de ce qu'un entier de 64 bits porte. Un
    // compte tronqué qui se lirait comme un autre compte serait la faute qu'un
    // vérificateur fail-closed ne peut pas commettre.
    assert!(matches!(
        refus(&avec("octets_presentation", "99999999999999999999")),
        ErreurConstat::EntierNonCanonique { .. }
    ));
}

#[test]
fn le_zero_seul_reste_une_forme_canonique() {
    // `0` n'est pas un « zéro de tête » : c'est le nombre zéro. Le refuser
    // serait refuser une valeur licite du contrat.
    // L'analyseur ne juge pas la taille d'une preuve : il la lit. Ce qui la
    // recoupe est le constructeur du témoignage (adapter), pas ce module.
    assert!(
        analyser_constat(&avec("octets_presentation", "0")).is_ok(),
        "« 0 » est un entier canonique, pas un zéro de tête"
    );
}

#[test]
fn une_version_inconnue_est_refusee_avant_tout_le_reste() {
    match refus(&avec("version_du_constat", "2")) {
        ErreurConstat::VersionInattendue { attendue, trouvee } => {
            assert_eq!(attendue, 1);
            assert_eq!(trouvee, 2);
        }
        autre => panic!("variante inattendue : {autre:?}"),
    }
}

#[test]
fn un_verdict_sans_succes_est_refuse() {
    match refus(&avec("verdict", "\"verification_refusee\"")) {
        ErreurConstat::VerdictSansSucces { trouve } => assert_eq!(trouve, "verification_refusee"),
        autre => panic!("variante inattendue : {autre:?}"),
    }
}

#[test]
fn des_longueurs_incoherentes_sont_refusees_dans_les_deux_sens() {
    match refus(&avec("transcript_recv_authentifie", "900")) {
        ErreurConstat::LongueursIncoherentes {
            sens,
            longueur,
            authentifie,
            attestee,
        } => {
            assert_eq!(sens, "reçu");
            assert_eq!((longueur, authentifie, attestee), (944, 900, 944));
        }
        autre => panic!("variante inattendue : {autre:?}"),
    }
    match refus(&avec("transcript_sent_longueur_attestee", "100")) {
        ErreurConstat::LongueursIncoherentes { sens, .. } => assert_eq!(sens, "émis"),
        autre => panic!("variante inattendue : {autre:?}"),
    }
}

// ---------------------------------------------------------------------------
// L'hexadécimal et la clé épinglée
// ---------------------------------------------------------------------------

#[test]
fn une_empreinte_a_chiffre_fautif_est_refusee() {
    let empreinte = "z28a41ce87dafcd313d301ab56472b6f3cd1b3d81d903da787b0ca9dfffbeea0";
    match refus(&avec(
        "empreinte_recv_revele_sha256",
        &format!("\"{empreinte}\""),
    )) {
        ErreurConstat::HexadecimalInvalide { cle, octet } => {
            assert_eq!(cle, "empreinte_recv_revele_sha256");
            assert_eq!(octet, b'z');
        }
        autre => panic!("variante inattendue : {autre:?}"),
    }
}

#[test]
fn une_empreinte_en_majuscules_est_refusee_au_lieu_d_etre_repliee() {
    // Deux graphies d'un même constat seraient deux constats : le contrat en
    // écrit une, et l'analyseur ne replie pas (posture d'ADR-0016 C0).
    let empreinte = "C28A41CE87DAFCD313D301AB56472B6F3CD1B3D81D903DA787B0CA9DFFFBEEA0";
    assert!(matches!(
        refus(&avec(
            "empreinte_recv_revele_sha256",
            &format!("\"{empreinte}\"")
        )),
        ErreurConstat::HexadecimalInvalide { octet: b'C', .. }
    ));
}

#[test]
fn une_empreinte_de_mauvaise_longueur_est_refusee() {
    let court = "c28a41ce";
    match refus(&avec(
        "empreinte_presentation_sha256",
        &format!("\"{court}\""),
    )) {
        ErreurConstat::LongueurHexadecimaleInvalide {
            cle,
            attendue_en_octets,
            trouvee_en_chiffres,
        } => {
            assert_eq!(cle, "empreinte_presentation_sha256");
            assert_eq!(attendue_en_octets, Some(32));
            assert_eq!(trouvee_en_chiffres, 8);
        }
        autre => panic!("variante inattendue : {autre:?}"),
    }
}

#[test]
fn une_cle_epinglee_a_nombre_impair_de_chiffres_est_refusee() {
    match refus(&avec("attestor_cle_hex", "\"036aa\"")) {
        ErreurConstat::LongueurHexadecimaleInvalide {
            cle,
            attendue_en_octets,
            trouvee_en_chiffres,
        } => {
            assert_eq!(cle, "attestor_cle_hex");
            assert_eq!(attendue_en_octets, None);
            assert_eq!(trouvee_en_chiffres, 5);
        }
        autre => panic!("variante inattendue : {autre:?}"),
    }
}

#[test]
fn une_empreinte_de_longueur_impaire_est_refusee() {
    // Le nombre impair et la mauvaise longueur tombent au même endroit : la
    // conversion EST le contrôle. Le message dit la longueur attendue.
    match refus(&avec("empreinte_recv_revele_sha256", "\"abc\"")) {
        ErreurConstat::LongueurHexadecimaleInvalide {
            attendue_en_octets,
            trouvee_en_chiffres,
            ..
        } => {
            assert_eq!(attendue_en_octets, Some(32));
            assert_eq!(trouvee_en_chiffres, 3);
        }
        autre => panic!("variante inattendue : {autre:?}"),
    }
}

#[test]
fn une_cle_epinglee_vide_est_refusee() {
    assert!(matches!(
        refus(&avec("attestor_cle_hex", "\"\"")),
        ErreurConstat::LongueurHexadecimaleInvalide {
            trouvee_en_chiffres: 0,
            ..
        }
    ));
}

#[test]
fn une_cle_epinglee_de_longueur_libre_est_admise() {
    // La longueur d'une clé n'est PAS fixée par le contrat : l'y figer ferait
    // du vérificateur un binaire qui connaît la taille des clés d'un
    // algorithme — ce qu'ADR-0001 lui interdit. Seules la parité et la
    // non-vacuité sont exigées.
    let constat = analyser_constat(&avec("attestor_cle_hex", "\"abcd\""))
        .expect("une clé de deux octets est licite");
    assert_eq!(
        String::from_utf8(constat.cle_du_controle).expect("US-ASCII"),
        "k256 abcd"
    );
}

#[test]
fn un_algorithme_vide_est_refuse() {
    match refus(&avec("attestor_cle_algorithme", "\"\"")) {
        ErreurConstat::ValeurVide { cle } => assert_eq!(cle, "attestor_cle_algorithme"),
        autre => panic!("variante inattendue : {autre:?}"),
    }
}

#[test]
fn un_algorithme_portant_le_separateur_est_refuse() {
    // « k 256 » et « k » + « 256 » composeraient la même chaîne épinglée : la
    // décomposition cesserait d'être unique, et l'épinglage d'être une identité.
    // (L'espace étant déjà refusé dans une chaîne, la garde est une seconde
    // barrière : elle tient même si le jeu de caractères admis s'élargit.)
    let erreur = refus(&avec("attestor_cle_algorithme", "\"k 256\""));
    assert!(
        matches!(erreur, ErreurConstat::AlgorithmeAmbigu { .. })
            || matches!(erreur, ErreurConstat::EspaceInterdit { .. }),
        "variante inattendue : {erreur:?}"
    );
}

#[test]
fn une_revision_amont_vide_est_refusee() {
    match refus(&avec("revision_amont", "\"\"")) {
        ErreurConstat::ValeurVide { cle } => assert_eq!(cle, "revision_amont"),
        autre => panic!("variante inattendue : {autre:?}"),
    }
}

#[test]
fn une_origine_vide_est_refusee() {
    match refus(&avec("server_name", "\"\"")) {
        ErreurConstat::ValeurVide { cle } => assert_eq!(cle, "server_name"),
        autre => panic!("variante inattendue : {autre:?}"),
    }
}

#[test]
fn une_version_de_couche_vide_est_refusee() {
    match refus(&avec("connection_info_version_tls", "\"\"")) {
        ErreurConstat::ValeurVide { cle } => assert_eq!(cle, "connection_info_version_tls"),
        autre => panic!("variante inattendue : {autre:?}"),
    }
}

// ---------------------------------------------------------------------------
// Les refus se lisent
// ---------------------------------------------------------------------------

#[test]
fn chaque_refus_s_imprime_et_nomme_ce_qui_l_a_produit() {
    // Un refus qui ne se lit pas n'est pas diagnosticable, et le vérificateur ne
    // journalise pas : le message EST le diagnostic.
    let cas: Vec<(&str, String)> = vec![
        ("fin prématurée", String::new()),
        ("enveloppe", String::from("[1]")),
        (
            "clé inconnue",
            ligne(&paires()).replacen("\"verdict\"", "\"verdicts\"", 1),
        ),
        ("clé manquante", sans("server_name")),
        ("version", avec("version_du_constat", "7")),
        ("verdict", avec("verdict", "\"autre_chose\"")),
        ("hexadécimal", avec("attestor_cle_hex", "\"0g\"")),
        ("longueur", avec("empreinte_recv_revele_sha256", "\"ab\"")),
        ("vide", avec("server_name", "\"\"")),
        ("type", avec("server_name", "1")),
        ("entier", avec("octets_presentation", "007")),
        ("longueurs", avec("transcript_sent_authentifie", "1")),
        ("clés non triées", ligne(&paires_permutees())),
        ("longueur libre", avec("attestor_cle_hex", "\"036\"")),
        (
            "empreinte de longueur impaire",
            avec("empreinte_recv_revele_sha256", "\"abc\""),
        ),
        ("échappement", avec("server_name", "\"a\\tb\"")),
        ("non-ASCII", avec("server_name", "\"aé\"")),
        ("espace", avec("server_name", "\"a b\"")),
        ("résiduels", format!("{}x", ligne(&paires()))),
    ];
    for (nom, texte) in cas {
        let erreur = refus(&texte);
        let rendu = erreur.to_string();
        assert!(
            rendu.starts_with("constat"),
            "cas « {nom} » : le message doit dire de quoi il parle — « {rendu} »"
        );
        assert!(
            rendu.len() > 30,
            "cas « {nom} » : un message de refus dit ce qui l'a produit — « {rendu} »"
        );
        println!("{nom} → {rendu}");
    }
}
