//! Les cas **acceptés** : des réponses réelles du pool S2, typées en entier.
//!
//! Rattachement (G0) : 08, A(typer-correctness) — « Le typeur extrait du dire
//! brut le fait annoncé (classe, valeur, unité) sans erreur de sens ». Ce qui
//! est asserté ici est donc le fait **entier**, champ par champ : une valeur
//! juste avec une devise fausse serait un fait faux.

mod commun;

use commun::corpus_accepte;
use shogen_typer::{COMPTE_D_ITERATIONS, identite, typer_dire};

#[test]
fn les_cas_reels_se_typent_champ_par_champ() {
    for cas in corpus_accepte() {
        let fait = match typer_dire(cas.subject, cas.dire) {
            Ok(fait) => fait,
            Err(refus) => panic!("cas « {} » refusé : {refus:?}", cas.nom),
        };
        assert_eq!(
            fait.valeur.mantisse(),
            cas.mantisse,
            "mantisse — {}",
            cas.nom
        );
        assert_eq!(
            fait.valeur.exposant(),
            cas.exposant,
            "exposant — {}",
            cas.nom
        );
        assert_eq!(fait.valeur.lexeme(), cas.lexeme, "lexème — {}", cas.nom);
        assert_eq!(fait.devise, cas.devise, "devise — {}", cas.nom);
        assert_eq!(fait.instant.graphie(), cas.instant, "instant — {}", cas.nom);
    }
}

/// La forme typée n'a rien perdu de ce que la source avait écrit : la graphie
/// reconstruite depuis (mantisse, exposant) est **l'octet pour octet** de la
/// source. C'est ce contrôle qui interdit la normalisation silencieuse des
/// zéros de queue — `64529.50000000` a huit décimales parce que la source en a
/// écrit huit.
#[test]
fn la_graphie_se_reconstruit_a_l_identique() {
    for cas in corpus_accepte() {
        let fait = match typer_dire(cas.subject, cas.dire) {
            Ok(fait) => fait,
            Err(refus) => panic!("cas « {} » refusé : {refus:?}", cas.nom),
        };
        assert_eq!(
            fait.valeur.graphie_reconstruite(),
            cas.lexeme,
            "reconstruction — {}",
            cas.nom
        );
    }
}

/// Le fait cite son typeur (03 §3) : nom, version, empreinte de logique,
/// compte d'itérations. Sans quoi rien en aval ne peut dire *qui* a extrait.
#[test]
fn le_fait_cite_son_typeur() {
    let attendue = identite();
    for cas in corpus_accepte() {
        let fait = match typer_dire(cas.subject, cas.dire) {
            Ok(fait) => fait,
            Err(refus) => panic!("cas « {} » refusé : {refus:?}", cas.nom),
        };
        assert_eq!(fait.typeur.nom, "shogen-typer");
        assert_eq!(fait.typeur.version, env!("CARGO_PKG_VERSION"));
        assert_eq!(fait.typeur.empreinte, attendue.empreinte);
        assert_eq!(fait.typeur.compte_d_iterations, COMPTE_D_ITERATIONS);
        assert_eq!(
            fait.typeur.empreinte.len(),
            64,
            "empreinte SHA-256 en hexadécimal"
        );
    }
}

/// Le `subject` épinglé satisfait le prédicat de canonicité du cœur — ce n'est
/// pas une évidence, c'est un fait à contrôler : une constante mal écrite ferait
/// refuser **tous** les dires, y compris les bons.
#[test]
fn le_subject_epingle_est_canonique() {
    assert_eq!(
        shogen_core::subject_est_canonique(shogen_typer::SUBJECT_EPINGLE.as_bytes()),
        Ok(())
    );
}

/// La devise ne vient pas du dire : elle vient de l'endpoint. Le contrôle est
/// que le code rendu est bien celui de l'endpoint épinglé.
#[test]
fn la_devise_est_celle_de_l_endpoint() {
    assert_eq!(shogen_typer::DEVISE_DE_L_ENDPOINT.code(), "USD");
}

/// Imprime les faits typés en entier (`cargo test -- --nocapture`) — pour
/// qu'un lecteur voie ce que le typeur produit, sans avoir à le déduire des
/// assertions.
#[test]
fn les_faits_reels_s_impriment_en_entier() {
    for cas in corpus_accepte() {
        let fait = match typer_dire(cas.subject, cas.dire) {
            Ok(fait) => fait,
            Err(refus) => panic!("cas « {} » refusé : {refus:?}", cas.nom),
        };
        println!("── fait typé — {} ──", cas.nom);
        println!("  subject      : {}", cas.subject);
        println!(
            "  valeur       : mantisse {} × 10^{} (lexème « {} »)",
            fait.valeur.mantisse(),
            fait.valeur.exposant(),
            fait.valeur.lexeme()
        );
        println!("  devise       : {}", fait.devise.code());
        println!("  instant      : {}", fait.instant.graphie());
        println!(
            "  typeur       : {} {} — empreinte {} — compte d'itérations {}",
            fait.typeur.nom,
            fait.typeur.version,
            fait.typeur.empreinte,
            fait.typeur.compte_d_iterations
        );
    }
}
