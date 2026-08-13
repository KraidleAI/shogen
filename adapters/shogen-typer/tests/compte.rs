//! Le **compte d'itérations** — mesuré, jamais déclaré de tête.
//!
//! Rattachement (G0) : **08, A(typer-correctness)** — « cible : tested à S3,
//! avec **compte d'itérations par typeur** » ; **09-vocabulaire** — « les trois
//! mots d'assurance : *proven / tested (avec compte d'itérations) / reviewed
//! (qui, quand)* » ; **10 §8**, entrée A(typer-correctness) — « Le rapport S2
//! publie le **compte d'exécutions de chaque décodeur** — première marche vers
//! la cible de 08 ».
//!
//! Ce que ce fichier fait : il exécute **le corpus de la passe** — chaque cas
//! accepté, chaque cas de refus, chaque cas généré par les trois propriétés —
//! en tenant un compteur, imprime le total, et **échoue** si le total mesuré
//! diffère de la constante que le typeur porte dans son identité. Le nombre
//! écrit dans `src/identite.rs` ne peut donc pas être un nombre de tête : il ne
//! survit à `cargo test` que s'il est vrai.
//!
//! Ce que le compte **est** : le nombre d'exécutions de `typer_dire` sur le
//! corpus de la passe, tel que ce harnais les exécute — une fois chacune.
//! Ce qu'il **n'est pas** : un total sur toute la suite (les autres binaires de
//! test rejouent des sous-ensembles du même corpus, ils n'ajoutent aucun cas),
//! ni un nombre de tests, ni une couverture.

mod commun;

use commun::{
    CAS_PAR_PROPRIETE, NOMBRE_DE_PROPRIETES, corpus_accepte, corpus_de_refus, dire_construit,
    executeur, strategie_graphie_hostile, strategie_lexeme_decimal, strategie_octets,
};
use shogen_typer::{COMPTE_D_ITERATIONS, SUBJECT_EPINGLE, typer_dire};
use std::cell::Cell;

#[test]
fn le_compte_d_iterations_declare_est_celui_qui_est_mesure() {
    let executions = Cell::new(0u64);
    let compter = |executions: &Cell<u64>| {
        executions.set(executions.get().saturating_add(1));
    };

    let acceptes = corpus_accepte();
    for cas in &acceptes {
        compter(&executions);
        let _ = typer_dire(cas.subject, cas.dire);
    }
    let apres_acceptes = executions.get();

    let refuses = corpus_de_refus();
    for cas in &refuses {
        compter(&executions);
        let _ = typer_dire(cas.subject, cas.dire);
    }
    let apres_refuses = executions.get();

    let resultat_a = executeur().run(&strategie_octets(), |octets| {
        compter(&executions);
        let _ = typer_dire(SUBJECT_EPINGLE, &octets);
        Ok(())
    });
    let resultat_b = executeur().run(&strategie_lexeme_decimal(), |graphie| {
        compter(&executions);
        let _ = typer_dire(SUBJECT_EPINGLE, &dire_construit(&graphie));
        Ok(())
    });
    let resultat_c = executeur().run(&strategie_graphie_hostile(), |graphie| {
        compter(&executions);
        let _ = typer_dire(SUBJECT_EPINGLE, &dire_construit(&graphie));
        Ok(())
    });

    let mesure = executions.get();
    println!("── compte d'itérations du typeur, mesuré ──");
    println!("  cas acceptés (réels)      : {}", apres_acceptes);
    println!(
        "  cas de refus              : {}",
        apres_refuses.saturating_sub(apres_acceptes)
    );
    println!(
        "  cas générés ({NOMBRE_DE_PROPRIETES} propriétés × {CAS_PAR_PROPRIETE}) : {}",
        mesure.saturating_sub(apres_refuses)
    );
    println!("  TOTAL MESURÉ              : {mesure}");
    println!("  déclaré (identite::COMPTE_D_ITERATIONS) : {COMPTE_D_ITERATIONS}");

    assert!(resultat_a.is_ok(), "propriété (a) : {resultat_a:?}");
    assert!(resultat_b.is_ok(), "propriété (b) : {resultat_b:?}");
    assert!(resultat_c.is_ok(), "propriété (c) : {resultat_c:?}");
    assert_eq!(
        mesure, COMPTE_D_ITERATIONS,
        "le compte déclaré dans src/identite.rs ment : mesuré {mesure}"
    );
}
