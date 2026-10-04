//! Les gates de Shōgen, exécutables en local comme en CI par la même entrée :
//! `cargo xtask verify`.
//!
//! Rattachement (G0) : ADR-0013 (forme des gates : bloquantes, sélection par
//! rôle à chemins exacts, ligne de couverture avant verdict, mutant semé tué),
//! ADR-0010 (ce que les gates exécutent), ADR-0012 D3 (version exacte au
//! manifeste), DEVOPS §3 (le registre S-G1…S-G7).
//!
//! Les fonctions de gate prennent une **racine** en argument : c'est ce qui
//! rend les mutants semés rejouables sur un arbre copié (`xtask/tests/`) sans
//! jamais toucher l'arbre de travail.

pub mod documents;
pub mod exemple;
pub mod fuzz;
pub mod manifeste;
pub mod mutation;
pub mod rapport;
pub mod reproductible;
pub mod roles;
pub mod sg1;
pub mod sg2;
pub mod sg3;
pub mod sg4;
pub mod sg5;
pub mod sg6;
pub mod sg7a;
pub mod sg8;
pub mod sg9;
pub mod source;

use std::path::{Path, PathBuf};

/// Remonte depuis `depart` jusqu'au manifeste portant `[workspace]`.
pub fn racine_du_workspace(depart: &Path) -> Result<PathBuf, String> {
    let mut courant = Some(depart);
    while let Some(repertoire) = courant {
        let manifeste = repertoire.join("Cargo.toml");
        if let Ok(texte) = std::fs::read_to_string(&manifeste)
            && texte.contains("[workspace]")
        {
            return Ok(repertoire.to_path_buf());
        }
        courant = repertoire.parent();
    }
    Err(format!(
        "racine de workspace introuvable au-dessus de {}",
        depart.display()
    ))
}

/// Exécute toutes les gates mécanisées. Rend le code de sortie du processus.
///
/// Bloquant par construction (ADR-0013, point 1) : aucun avertissement, aucune
/// gate consultative, aucun `continue-on-error`.
pub fn verifier_tout(racine: &Path, avec_outils_cargo: bool) -> i32 {
    println!("=== cargo xtask verify — racine : {} ===", racine.display());
    println!();

    let rapports = vec![
        sg1::executer(racine),
        sg2::executer(racine, avec_outils_cargo),
        sg3::executer(racine),
        sg4::executer(racine),
        sg5::executer(racine),
        sg6::executer(racine),
        sg7a::executer(racine),
        sg8::executer(racine),
        sg9::executer(racine),
    ];

    let mut rouge = false;
    for rapport in &rapports {
        rapport.imprimer();
        if !rapport.vert() {
            rouge = true;
        }
        println!();
    }

    if avec_outils_cargo {
        for (nom, arguments) in outils_cargo() {
            match executer_cargo(racine, nom, arguments) {
                Ok(true) => println!("{nom} : VERT"),
                Ok(false) => {
                    println!("{nom} : ROUGE");
                    rouge = true;
                }
                Err(erreur) => {
                    println!("{nom} : ROUGE — {erreur}");
                    rouge = true;
                }
            }
            println!();
        }
    }

    if rouge {
        println!("=== VERDICT GLOBAL : ROUGE — l'intégration s'arrête (ADR-0013, point 1) ===");
        1
    } else {
        println!("=== VERDICT GLOBAL : VERT ===");
        println!(
            "Ce que ce vert dit, et rien de plus : les mutants semés de ces gates sont morts (xtask/tests). Hors de ce corpus, une gate ne dit rien (ADR-0013, point 2)."
        );
        0
    }
}

/// La cible **sans bibliothèque standard** sur laquelle la gate `no_std`
/// s'établit.
///
/// Pourquoi une cible bare-metal plutôt qu'une relecture du source : `#![no_std]`
/// écrit en tête d'un fichier n'est qu'une intention tant que rien ne l'oppose
/// à un environnement où `std` **n'existe pas**. `thumbv7em-none-eabi` n'a pas
/// de bibliothèque standard ; si une arête vers `std` réapparaît dans la
/// bibliothèque du vérificateur ou dans le cœur qu'elle appelle, la
/// construction échoue à la résolution de module, avant même l'édition de
/// liens. Contrôle exécuté le 2026-08-13 : `use std::collections::BTreeMap`
/// réintroduit dans `crates/shogen-verifier/src/lib.rs` → `error[E0433]:
/// cannot find module or crate `std` in this scope`, construction ROUGE ;
/// ligne retirée → VERT. La gate discrimine.
///
/// Un `rlib` n'exige ni `panic_handler` ni allocateur global : la construction
/// de la seule cible `lib` suffit, et elle entraîne `shogen-core` avec elle
/// (l'arête d'ADR-0010 point 3). Le binaire, lui, reste `std` par définition
/// (ADR-0010 point 4) et n'est pas construit pour cette cible.
///
/// Pré-requis d'environnement : `rustup target add thumbv7em-none-eabi`. S'il
/// manque, la gate est ROUGE — ce qui empêche de conclure est ROUGE, jamais
/// un vert par défaut (ADR-0010 point 5, même règle que le double-build D6).
pub const CIBLE_SANS_STD: &str = "thumbv7em-none-eabi";

fn outils_cargo() -> Vec<(&'static str, Vec<&'static str>)> {
    vec![
        ("cargo fmt --check", vec!["fmt", "--all", "--check"]),
        // Échéance contractée d'ADR-0009 point 6 (« `#![no_std]` + `alloc`
        // devient une gate en S3 »), maintenue telle quelle par ADR-0015
        // point 6, échéance 3 de 13 §3. Elle vit ici et non dans
        // `cargo xtask gates` : `gates` est lexicale et sans sous-processus
        // cargo par contrat (usage de `xtask/src/main.rs`).
        (
            "no_std du vérificateur (construction pour une cible sans bibliothèque standard)",
            vec![
                "build",
                "--locked",
                "--lib",
                "--package",
                "shogen-verifier",
                "--target",
                CIBLE_SANS_STD,
            ],
        ),
        (
            "cargo clippy -D warnings",
            vec![
                "clippy",
                "--locked",
                "--workspace",
                "--all-targets",
                "--",
                "-D",
                "warnings",
            ],
        ),
    ]
}

fn executer_cargo(racine: &Path, nom: &str, arguments: Vec<&str>) -> Result<bool, String> {
    println!("--- {nom} ---");
    let cargo = std::env::var("CARGO").unwrap_or_else(|_| String::from("cargo"));
    let statut = std::process::Command::new(cargo)
        .args(&arguments)
        .current_dir(racine)
        .status()
        .map_err(|erreur| format!("exécution impossible : {erreur}"))?;
    Ok(statut.success())
}
