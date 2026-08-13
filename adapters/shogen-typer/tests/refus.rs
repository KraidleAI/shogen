//! Les cas **refusés** — un par clause, avec la variante exacte.
//!
//! Rattachement (G0) : la règle gatewright reprise par 13 §1 — « un
//! vérificateur qui n'a jamais rejeté n'a rien montré ». Un typeur non plus.
//!
//! Ce qui est asserté n'est **jamais** `is_err()` : c'est l'égalité avec la
//! variante attendue, positions comprises. Un refus qui se produit pour la
//! mauvaise raison est un refus faux, et `is_err()` ne le voit pas.

mod commun;

use commun::{Origine, corpus_de_refus};
use shogen_typer::typer_dire;

#[test]
fn chaque_cas_de_refus_rend_sa_variante_exacte() {
    for cas in corpus_de_refus() {
        match typer_dire(cas.subject, cas.dire) {
            Ok(fait) => panic!(
                "cas « {} » ACCEPTÉ alors qu'il doit être refusé — fait : {fait:?}",
                cas.nom
            ),
            Err(refus) => assert_eq!(refus, cas.refus, "variante de refus — {}", cas.nom),
        }
    }
}

/// Le corpus de refus porte des dires **réels**, pas seulement du bruit
/// construit : une suite qui ne refuserait que ce qu'elle a fabriqué ne dirait
/// rien de ce qui arrive d'un réseau.
#[test]
fn le_corpus_de_refus_porte_des_dires_reels() {
    let reels = corpus_de_refus()
        .iter()
        .filter(|cas| matches!(cas.origine, Origine::Reelle { .. }))
        .count();
    let total = corpus_de_refus().len();
    println!("cas de refus : {total} au total, dont {reels} sur dire réel");
    assert!(reels >= 12, "cas de refus sur dire réel : {reels}");
}

/// Aucun refus ne doit dépendre de l'ordre d'exécution ni d'un état global : le
/// même cas rejoué rend le même refus.
#[test]
fn les_refus_sont_stables_au_rejeu() {
    for cas in corpus_de_refus() {
        let premier = typer_dire(cas.subject, cas.dire);
        let second = typer_dire(cas.subject, cas.dire);
        assert_eq!(premier, second, "rejeu — {}", cas.nom);
    }
}
