//! **Octet muté ⇒ erreur nommée, jamais panique.**
//!
//! Registre : *octet muté du lot* — le troisième registre de « semé »
//! d'ADR-0011, point 4. Ce n'est ni un mutant de gate ni de l'analyse de
//! mutation : c'est un **test négatif de données**, et aucun score n'en sort.
//! L'appeler « mutation testing » serait un faux (ADR-0011, point 4).
//!
//! Ce que le test établit exactement, sur le vecteur de référence : pour
//! **chaque position** et **chaque valeur d'octet** (255 valeurs × N positions,
//! soit l'exhaustif des mutations d'un octet), le décodeur rend soit une erreur
//! nommée, soit un témoignage dont le ré-encodage **redonne exactement les
//! octets mutés**. Aucune troisième issue n'est admise : ni panique, ni
//! acceptation d'octets non canoniques.
//!
//! Ce qu'il n'établit pas : rien sur les mutations de plusieurs octets, ni sur
//! les entrées hors de ce voisinage. La propriété générale est portée par
//! `proprietes.rs` (propriété (c)), et le fuzz reste dû (ADR-0011, seuil 7).

use shogen_core::{TemoignageTrivial, decoder_temoignage, encoder_temoignage};

fn reference() -> TemoignageTrivial {
    TemoignageTrivial {
        source: String::from("exemple:source-factice"),
        instant: 1_754_000_000,
        contenu: b"lot d'exemple du walking skeleton".to_vec(),
    }
}

#[test]
fn chaque_octet_mute_donne_une_erreur_nommee_ou_un_lot_canonique() {
    let origine = encoder_temoignage(&reference());
    let mut refuses = 0usize;
    let mut acceptes_canoniques = 0usize;
    let mut essais = 0usize;

    for position in 0..origine.len() {
        for valeur in 0u16..=255 {
            let valeur = valeur as u8;
            if origine[position] == valeur {
                continue;
            }
            let mut mute = origine.clone();
            mute[position] = valeur;
            essais += 1;
            match decoder_temoignage(&mute) {
                Err(erreur) => {
                    // Une erreur nommée se dit : son rendu n'est jamais vide.
                    let rendu = format!("{erreur}");
                    assert!(
                        !rendu.trim().is_empty(),
                        "erreur muette à la position {position}, valeur {valeur}"
                    );
                    refuses += 1;
                }
                Ok(temoignage) => {
                    let reencode = encoder_temoignage(&temoignage);
                    assert_eq!(
                        reencode, mute,
                        "octet {position} := {valeur} : accepté mais NON canonique — \
                         deux suites d'octets distinctes donneraient le même fait"
                    );
                    acceptes_canoniques += 1;
                }
            }
        }
    }

    // Distribution imprimée AVANT le verdict, comme une ligne de couverture.
    println!(
        "mutation d'un octet — {} positions × 255 valeurs : {essais} essais, \
         {refuses} refus nommés, {acceptes_canoniques} acceptés canoniques (0 panique)",
        origine.len()
    );
    assert_eq!(
        refuses + acceptes_canoniques,
        essais,
        "toute mutation doit tomber dans l'une des deux issues admises"
    );
    assert!(
        refuses > 0,
        "aucun refus : le décodeur serait trop tolérant"
    );
}

#[test]
fn chaque_troncature_est_refusee_avec_une_erreur_nommee() {
    let origine = encoder_temoignage(&reference());
    for longueur in 0..origine.len() {
        let resultat = decoder_temoignage(&origine[..longueur]);
        let erreur = resultat.expect_err(&format!("préfixe de {longueur} octets accepté"));
        assert!(!format!("{erreur}").trim().is_empty());
    }
    println!(
        "troncature — {} préfixes stricts, tous refusés par une erreur nommée",
        origine.len()
    );
}

#[test]
fn chaque_octet_ajoute_en_queue_est_refuse() {
    let origine = encoder_temoignage(&reference());
    for valeur in 0u16..=255 {
        let mut allonge = origine.clone();
        allonge.push(valeur as u8);
        assert!(
            decoder_temoignage(&allonge).is_err(),
            "octet {valeur} ajouté en queue : doit être refusé (octets résiduels)"
        );
    }
    println!("queue — 256 valeurs d'octet ajoutées, toutes refusées");
}
