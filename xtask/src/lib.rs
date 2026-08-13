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
pub mod manifeste;
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

fn outils_cargo() -> Vec<(&'static str, Vec<&'static str>)> {
    vec![
        ("cargo fmt --check", vec!["fmt", "--all", "--check"]),
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
