//! Tests des régions STABLES de la bibliothèque — celles qui échappent au
//! périmètre du chantier vérificateur de la vague 2 (contrôles b/c/f/g sur
//! le constat réel, qui réécrira `analyser_constat` et ses chemins d'erreur).
//!
//! Rattachement : condition de validité de l'avis R-26 Q4 du 2026-08-13 —
//! « si une part stable du non-couvert échappe au chantier vague 2, ces
//! tests-là s'écrivent MAINTENANT ». Régions visées, relevées au rapport
//! llvm-cov du 2026-08-13 : `tete_hexadecimale` (l. 291+),
//! `premiere_divergence` (l. 303+), le refus de doublon d'`analyser_registre`
//! (l. 172+).
//!
//! La branche `NonCanonique` d'`examiner_lot` (l. 125+) n'est PAS couverte
//! ici, et ne peut pas l'être aujourd'hui : son inatteignabilité est
//! ÉTABLIE PAR LA MESURE, pas supposée (revue G2 vague 1) — le décodeur
//! canonique refuse toute forme qui n'est pas la sienne, donc tout octet
//! décodé se ré-encode identique. Trois mesures indépendantes concordent :
//! 678 528 272 cas de fuzz (classe « décodés-non-canoniques » = 0),
//! la campagne de corroboration du réviseur (15 314 192 cas, même classe
//! à 0), et le balayage exhaustif des 98 685 mutations d'un octet de
//! `dirigee-lot-canonique.bin` (0 `NonCanonique`). La branche est un
//! fail-safe contre un défaut FUTUR du décodeur : elle se garde, elle ne
//! se couvre pas — même famille que les survivants « équivalents au
//! programme » de `survivants.txt`.

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
fn temoin_la_branche_non_canonique_est_un_fail_safe_inatteignable() {
    // TÉMOIN, pas couverture : ce test documente et surveille l'argument
    // d'inatteignabilité du doc de module — le décodeur canonique refuse
    // toute forme qui n'est pas la sienne, donc une graine du corpus est
    // soit refusée, soit décodée-et-ré-encodée à l'identique, jamais
    // `NonCanonique`. Si ce témoin casse un jour, le décodeur a changé de
    // régime et la branche DOIT alors être couverte par un vrai test qui
    // assère ses trois champs.
    let canonique = std::fs::read("fuzz-corpus/dirigee-lot-exemple.bin")
        .or_else(|_| std::fs::read("../shogen-verifier/fuzz-corpus/dirigee-lot-exemple.bin"))
        .expect("graine dirigée du corpus de fuzz présente au dépôt");
    if let Examen::NonCanonique { .. } = shogen_verifier::examiner_lot(&canonique) {
        panic!(
            "la graine du corpus est devenue non-canonique : le décodeur a changé \
             de régime — couvrir la branche NonCanonique avec ses trois champs"
        );
    }
}
