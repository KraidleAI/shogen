//! `cargo xtask <commande>` — l'entrée unique des gates et de l'outillage.
//!
//! Coquille impérative (ADR-0010, point 4) : c'est ici que vivent les
//! arguments, les fichiers et les codes de sortie.

use std::path::PathBuf;

fn main() {
    std::process::exit(executer());
}

fn executer() -> i32 {
    let mut arguments = std::env::args().skip(1);
    let commande = arguments.next().unwrap_or_default();

    let depart = match std::env::current_dir() {
        Ok(chemin) => chemin,
        Err(erreur) => {
            eprintln!("répertoire courant illisible : {erreur}");
            return 70;
        }
    };
    let racine = match xtask::racine_du_workspace(&depart) {
        Ok(racine) => racine,
        Err(erreur) => {
            eprintln!("{erreur}");
            return 70;
        }
    };

    match commande.as_str() {
        "verify" => xtask::verifier_tout(&racine, true),
        "gates" => xtask::verifier_tout(&racine, false),
        "emettre-exemple" => {
            let chemin = match arguments.next() {
                Some(chemin) => PathBuf::from(chemin),
                None => {
                    eprintln!("usage : cargo xtask emettre-exemple <chemin>");
                    return 64;
                }
            };
            match xtask::exemple::emettre(&chemin) {
                Ok(taille) => {
                    println!(
                        "lot d'exemple écrit : {} ({taille} octets)",
                        chemin.display()
                    );
                    0
                }
                Err(erreur) => {
                    eprintln!("{erreur}");
                    65
                }
            }
        }
        "muter" => {
            let entree = arguments.next();
            let sortie = arguments.next();
            let index = arguments.next().and_then(|v| v.parse::<usize>().ok());
            let valeur = arguments.next().and_then(|v| v.parse::<u8>().ok());
            match (entree, sortie, index, valeur) {
                (Some(entree), Some(sortie), Some(index), Some(valeur)) => {
                    match xtask::exemple::muter(
                        &PathBuf::from(entree),
                        &PathBuf::from(&sortie),
                        index,
                        valeur,
                    ) {
                        Ok(()) => {
                            println!("lot muté écrit : {sortie} (octet {index} := {valeur})");
                            0
                        }
                        Err(erreur) => {
                            eprintln!("{erreur}");
                            65
                        }
                    }
                }
                _ => {
                    eprintln!("usage : cargo xtask muter <entree> <sortie> <index> <valeur>");
                    64
                }
            }
        }
        _ => {
            eprintln!("usage : cargo xtask <verify|gates|emettre-exemple|muter>");
            eprintln!("  verify           : toutes les gates + fmt + clippy (l'entrée de CI)");
            eprintln!("  gates            : les gates lexicales seules, sans sous-processus cargo");
            eprintln!("  emettre-exemple  : écrit le lot d'exemple du walking skeleton");
            eprintln!("  muter            : écrit une copie du lot avec un octet remplacé");
            64
        }
    }
}
