//! L'**analyseur du dire** exercé pour lui-même — les chemins que le ticker
//! Coinbase ne visite pas.
//!
//! Rattachement (G0) : RFC 8259 §7 (chaînes, échappements, paires de
//! substituts) et §6 (nombres), détenue depuis le 2026-08-13.
//!
//! Ces cas sont **construits** et le disent : le dire réel du pool ne porte ni
//! échappement, ni emoji, ni objet vide. Un analyseur qui ne serait exercé que
//! par le dire d'un seul endpoint n'aurait montré qu'un chemin.

use shogen_typer::{ErreurJson, Valeur, analyser_objet_racine};

fn texte(dire: &[u8], cle: &str) -> String {
    let racine = match analyser_objet_racine(dire) {
        Ok(racine) => racine,
        Err(erreur) => panic!("dire refusé : {erreur:?}"),
    };
    match racine.membre(cle) {
        Some((Valeur::Texte(valeur), _)) => valeur.clone(),
        autre => panic!("membre {cle} : {autre:?}"),
    }
}

#[test]
fn les_huit_echappements_a_deux_caracteres() {
    let lu = texte(br#"{"a":"\" \\ \/ \b \f \n \r \t"}"#, "a");
    assert_eq!(lu, "\" \\ / \u{0008} \u{000C} \n \r \t");
}

#[test]
fn l_echappement_unicode_du_plan_de_base() {
    assert_eq!(texte(b"{\"a\":\"\\u0041\\u00e9\\u6f22\"}", "a"), "Aé漢");
}

#[test]
fn la_paire_de_substituts_utf16() {
    assert_eq!(texte(b"{\"a\":\"\\ud83d\\ude00\"}", "a"), "😀");
}

#[test]
fn les_octets_multi_octets_passent_verbatim() {
    assert_eq!(texte("{\"a\":\"é漢🙂\"}".as_bytes(), "a"), "é漢🙂");
}

#[test]
fn le_lexeme_d_un_nombre_est_conserve_verbatim() {
    let racine = match analyser_objet_racine(br#"{"a":-0.5,"b":1E+30,"c":0}"#) {
        Ok(racine) => racine,
        Err(erreur) => panic!("dire refusé : {erreur:?}"),
    };
    for (cle, attendu) in [("a", "-0.5"), ("b", "1E+30"), ("c", "0")] {
        match racine.membre(cle) {
            Some((Valeur::Nombre(lexeme), _)) => assert_eq!(lexeme, attendu),
            autre => panic!("membre {cle} : {autre:?}"),
        }
    }
}

#[test]
fn objet_et_tableau_vides_sont_bien_formes() {
    let racine = match analyser_objet_racine(br#"{"o":{},"t":[],"n":null,"v":true,"f":false}"#) {
        Ok(racine) => racine,
        Err(erreur) => panic!("dire refusé : {erreur:?}"),
    };
    assert_eq!(racine.nombre_de_membres(), 5);
    assert!(matches!(racine.membre("o"), Some((Valeur::Objet, _))));
    assert!(matches!(racine.membre("t"), Some((Valeur::Tableau, _))));
    assert!(matches!(racine.membre("n"), Some((Valeur::Litteral, _))));
}

#[test]
fn les_blancs_de_la_rfc_sont_toleres() {
    let racine = match analyser_objet_racine(b" \t\r\n{ \"a\" : \"1\" , \"b\" : 2 } \n") {
        Ok(racine) => racine,
        Err(erreur) => panic!("dire refusé : {erreur:?}"),
    };
    assert_eq!(racine.nombre_de_membres(), 2);
}

#[test]
fn l_objet_racine_vide_est_bien_forme_mais_ne_porte_rien() {
    let racine = match analyser_objet_racine(b"{}") {
        Ok(racine) => racine,
        Err(erreur) => panic!("dire refusé : {erreur:?}"),
    };
    assert_eq!(racine.nombre_de_membres(), 0);
    assert!(racine.membre("price").is_none());
}

/// Un membre homonyme **imbriqué** ne remonte jamais à la racine : le typeur
/// lit `price` à la racine, et un `price` niché dans un sous-objet ne doit pas
/// pouvoir se faire passer pour lui.
#[test]
fn un_homonyme_imbrique_ne_remonte_pas() {
    let racine = match analyser_objet_racine(br#"{"data":{"price":"1.00"}}"#) {
        Ok(racine) => racine,
        Err(erreur) => panic!("dire refusé : {erreur:?}"),
    };
    assert_eq!(racine.nombre_de_membres(), 1);
    assert!(racine.membre("price").is_none());
}

#[test]
fn le_substitut_bas_seul_est_refuse() {
    assert_eq!(
        analyser_objet_racine(br#"{"a":"\ude00"}"#),
        Err(ErreurJson::SubstitutOrphelin {
            position: 12,
            unite: 0xDE00
        })
    );
}

#[test]
fn le_substitut_haut_suivi_d_autre_chose_est_refuse() {
    assert_eq!(
        analyser_objet_racine(br#"{"a":"\ud83dx"}"#),
        Err(ErreurJson::SubstitutOrphelin {
            position: 12,
            unite: 0xD83D
        })
    );
}

#[test]
fn une_virgule_finale_est_refusee() {
    assert_eq!(
        analyser_objet_racine(br#"{"a":"1",}"#),
        Err(ErreurJson::OctetInattendu {
            position: 9,
            attendu: b'"',
            trouve: b'}'
        })
    );
}
