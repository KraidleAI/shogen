//! **Property-based** sur le typeur — trois propriétés.
//!
//! Rattachement (G0) : **ADR-0011, point 2** (property-based, graine consignée,
//! distribution imprimée avant le verdict, contre-exemple devenu test
//! permanent). Le point 2 vise le **cœur pur** ; le typeur est un adapter et
//! n'y est pas assujetti — la discipline est reprise ici parce qu'elle est
//! celle du dépôt, pas parce qu'elle serait due.
//!
//! * **(a) totalité** — aucune suite d'octets ne fait diverger le typeur ;
//! * **(b) fidélité décimale** — pour toute graphie admissible, le fait typé
//!   se **reconstruit à l'identique** : la forme (mantisse, exposant) ne perd
//!   rien de ce que la source avait écrit, zéros de queue compris ;
//! * **(c) jamais d'altération silencieuse** — sur une graphie quelconque, le
//!   typeur ou bien refuse en nommant sa clause, ou bien accepte une valeur qui
//!   se reconstruit à l'identique. Il n'existe pas de troisième issue, et c'est
//!   *cette* propriété qui interdit l'arrondi silencieux.
//!
//! Régime d'assurance : *tested (avec compte d'itérations)*. Jamais *proven*.

mod commun;

use commun::{
    CAS_PAR_PROPRIETE, dire_construit, executeur, strategie_graphie_hostile,
    strategie_lexeme_decimal, strategie_octets,
};
use shogen_typer::{RefusDeTypage, SUBJECT_EPINGLE, typer_dire};
use std::cell::Cell;

/// Part minimale de cas non triviaux (patron du seuil 6 d'ADR-0011).
const PART_NON_TRIVIALE_MINIMALE: f64 = 0.50;

fn part(compteur: &Cell<usize>, total: &Cell<usize>) -> f64 {
    let total = total.get();
    if total == 0 {
        return 0.0;
    }
    compteur.get() as f64 / total as f64
}

#[test]
fn propriete_a_totalite_sur_octets_quelconques() {
    let total = Cell::new(0usize);
    let non_triviaux = Cell::new(0usize);
    let non_utf8 = Cell::new(0usize);
    let acceptes = Cell::new(0usize);

    let resultat = executeur().run(&strategie_octets(), |octets| {
        total.set(total.get().saturating_add(1));
        if !octets.is_empty() {
            non_triviaux.set(non_triviaux.get().saturating_add(1));
        }
        if core::str::from_utf8(&octets).is_err() {
            non_utf8.set(non_utf8.get().saturating_add(1));
        }
        // Le seul contrôle : l'appel REND. Une divergence ne se rattrape pas
        // par une assertion — elle se constate par l'absence de plantage.
        if typer_dire(SUBJECT_EPINGLE, &octets).is_ok() {
            acceptes.set(acceptes.get().saturating_add(1));
        }
        Ok(())
    });

    println!(
        "(a) totalité — cas : {}, non vides : {} ({:.1} %), non UTF-8 : {}, acceptés : {}",
        total.get(),
        non_triviaux.get(),
        part(&non_triviaux, &total) * 100.0,
        non_utf8.get(),
        acceptes.get()
    );
    assert!(resultat.is_ok(), "propriété (a) : {resultat:?}");
    assert_eq!(total.get(), CAS_PAR_PROPRIETE as usize);
    assert!(part(&non_triviaux, &total) >= PART_NON_TRIVIALE_MINIMALE);
}

#[test]
fn propriete_b_fidelite_de_la_forme_decimale() {
    let total = Cell::new(0usize);
    let avec_fraction = Cell::new(0usize);
    let negatifs = Cell::new(0usize);

    let resultat = executeur().run(&strategie_lexeme_decimal(), |graphie| {
        total.set(total.get().saturating_add(1));
        if graphie.contains('.') {
            avec_fraction.set(avec_fraction.get().saturating_add(1));
        }
        if graphie.starts_with('-') {
            negatifs.set(negatifs.get().saturating_add(1));
        }
        let dire = dire_construit(&graphie);
        let fait = match typer_dire(SUBJECT_EPINGLE, &dire) {
            Ok(fait) => fait,
            Err(refus) => {
                return Err(proptest::test_runner::TestCaseError::fail(format!(
                    "graphie admissible « {graphie} » refusée : {refus:?}"
                )));
            }
        };
        proptest::prop_assert_eq!(fait.valeur.lexeme(), graphie.as_str());
        proptest::prop_assert_eq!(fait.valeur.graphie_reconstruite(), graphie.as_str());
        Ok(())
    });

    println!(
        "(b) fidélité — cas : {}, avec fraction : {} ({:.1} %), négatifs : {}",
        total.get(),
        avec_fraction.get(),
        part(&avec_fraction, &total) * 100.0,
        negatifs.get()
    );
    assert!(resultat.is_ok(), "propriété (b) : {resultat:?}");
    assert_eq!(total.get(), CAS_PAR_PROPRIETE as usize);
    assert!(part(&avec_fraction, &total) >= PART_NON_TRIVIALE_MINIMALE);
}

#[test]
fn propriete_c_jamais_d_alteration_silencieuse() {
    let total = Cell::new(0usize);
    let refuses = Cell::new(0usize);
    let acceptes = Cell::new(0usize);

    let resultat = executeur().run(&strategie_graphie_hostile(), |graphie| {
        total.set(total.get().saturating_add(1));
        let dire = dire_construit(&graphie);
        match typer_dire(SUBJECT_EPINGLE, &dire) {
            Ok(fait) => {
                acceptes.set(acceptes.get().saturating_add(1));
                proptest::prop_assert_eq!(fait.valeur.lexeme(), graphie.as_str());
                proptest::prop_assert_eq!(fait.valeur.graphie_reconstruite(), graphie.as_str());
            }
            Err(refus) => {
                refuses.set(refuses.get().saturating_add(1));
                // Le dire construit est du JSON bien formé et son instant est
                // valide : le seul refus possible porte sur la décimale, et il
                // est NOMMÉ. Un refus générique passerait ici sans être vu.
                proptest::prop_assert!(
                    matches!(refus, RefusDeTypage::Decimale { cle: "price", .. }),
                    "refus non attribué à la décimale : {:?}",
                    refus
                );
            }
        }
        Ok(())
    });

    println!(
        "(c) altération — cas : {}, refusés : {} ({:.1} %), acceptés : {}",
        total.get(),
        refuses.get(),
        part(&refuses, &total) * 100.0,
        acceptes.get()
    );
    assert!(resultat.is_ok(), "propriété (c) : {resultat:?}");
    assert_eq!(total.get(), CAS_PAR_PROPRIETE as usize);
    // Les deux issues doivent être visitées : une propriété qui ne verrait que
    // des refus n'aurait rien montré de l'acceptation, et réciproquement.
    assert!(refuses.get() > 0, "aucun refus vu");
    assert!(acceptes.get() > 0, "aucune acceptation vue");
}
