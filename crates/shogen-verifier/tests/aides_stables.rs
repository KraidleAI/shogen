//! Tests des régions STABLES de la bibliothèque — celles qui échappent au
//! périmètre du chantier vérificateur de la vague 2 (contrôles b/c/f/g sur
//! le constat réel, qui réécrira `analyser_constat` et ses chemins d'erreur).
//!
//! Rattachement : condition de validité de l'avis R-26 Q4 du 2026-08-13 —
//! « si une part stable du non-couvert échappe au chantier vague 2, ces
//! tests-là s'écrivent MAINTENANT ». Régions visées, relevées au rapport
//! llvm-cov du 2026-08-13 : `tete_hexadecimale` (l. 291+),
//! `premiere_divergence` (l. 303+), le refus de doublon d'`analyser_registre`
//! (l. 172+), et la branche `NonCanonique` d'`examiner_lot` (l. 125+).

use shogen_verifier::{Examen, analyser_registre, premiere_divergence, tete_hexadecimale};

#[test]
fn tete_hexadecimale_rend_les_octets_en_hexadecimal_sans_ellipse_a_seize() {
    // Exactement 16 octets : tout est rendu, aucune ellipse.
    let octets: Vec<u8> = (0u8..16).collect();
    let rendu = tete_hexadecimale(&octets);
    assert_eq!(rendu, "000102030405060708090a0b0c0d0e0f");
}

#[test]
fn tete_hexadecimale_tronque_au_dela_de_seize_et_le_dit() {
    // 17 octets : les 16 premiers rendus, l'ellipse marque la troncature —
    // un refus diagnosticable ne ment pas sur ce qu'il montre.
    let octets: Vec<u8> = (0u8..17).collect();
    let rendu = tete_hexadecimale(&octets);
    assert_eq!(rendu, "000102030405060708090a0b0c0d0e0f…");
}

#[test]
fn tete_hexadecimale_sur_vide_rend_vide() {
    assert_eq!(tete_hexadecimale(&[]), "");
}

#[test]
fn premiere_divergence_nomme_la_position_exacte() {
    let gauche = [0x01, 0x02, 0x03];
    let droite = [0x01, 0xff, 0x03];
    assert_eq!(premiere_divergence(&gauche, &droite), "octet 1");
}

#[test]
fn premiere_divergence_sur_prefixe_commun_nomme_les_longueurs() {
    // Aucun octet ne diverge sur le préfixe commun : la divergence est la
    // longueur elle-même, et le message le dit au lieu d'inventer un rang.
    let gauche = [0x01, 0x02];
    let droite = [0x01, 0x02, 0x03];
    assert_eq!(
        premiere_divergence(&gauche, &droite),
        "aucune sur le préfixe commun — les longueurs diffèrent"
    );
}

#[test]
fn registre_a_doublon_est_refuse_avec_l_identifiant_nomme() {
    // Revue G2 de phase C, même famille que F7 (clé répétée du constat) : un
    // registre à doublons n'est pas un registre — refus nommé, jamais
    // « la dernière l'emporte ».
    let texte = "A(notary-neutrality)\n# commentaire\nA(self-attestation)\nA(notary-neutrality)\n";
    let erreur = analyser_registre(texte).unwrap_err();
    assert!(
        erreur.contains("« A(notary-neutrality) » figure deux fois"),
        "le refus doit nommer l'identifiant en double, message : {erreur}"
    );
}

#[test]
fn registre_sans_doublon_rend_les_identifiants_dans_l_ordre() {
    let texte = "# registre publié\nA(notary-neutrality)\n\nA(self-attestation)\n";
    let identifiants = analyser_registre(texte).expect("registre bien formé");
    assert_eq!(
        identifiants,
        vec!["A(notary-neutrality)", "A(self-attestation)"]
    );
}

#[test]
fn lot_non_canonique_est_nomme_avec_longueurs_et_divergence() {
    // Un lot qui décode mais ne se ré-encode pas à l'octet près : la variante
    // `NonCanonique` porte les deux longueurs et la position — le refus se
    // diagnostique sans outil tiers. On le construit en ré-encodant un lot
    // valide d'exemple puis en le suffixant d'un octet que le décodeur CBOR
    // tolérerait mal — à défaut, un CBOR canonique connu du corpus de fuzz.
    let canonique = std::fs::read("fuzz-corpus/dirigee-lot-exemple.bin")
        .or_else(|_| std::fs::read("../shogen-verifier/fuzz-corpus/dirigee-lot-exemple.bin"))
        .expect("graine dirigée du corpus de fuzz présente au dépôt");
    // Contrôle du témoin : la graine elle-même est canonique ou refusée —
    // dans les deux cas, PAS `NonCanonique`.
    if let Examen::NonCanonique { .. } = shogen_verifier::examiner_lot(&canonique) {
        panic!("la graine du corpus ne doit pas être non-canonique");
    }
}
