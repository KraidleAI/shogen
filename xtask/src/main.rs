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
        // ADR-0012 D6. Cette commande n'entre PAS dans `verify` : elle coûte
        // deux constructions release complètes, et sa cible ratifiée est Linux
        // x86_64 seul — la mettre dans `verify` rendrait rouge sur Windows une
        // gate dont Windows n'est pas la cible, ou obligerait à un
        // contournement par plateforme au cœur de l'entrée commune. Elle est
        // bloquante là où elle est ratifiée : le job CI Linux
        // (.github/workflows/reproductibilite.yml).
        "double-build" => {
            let mut base = None;
            let mut cible = None;
            let mut faute = None;
            while let Some(argument) = arguments.next() {
                // Un drapeau privé de sa valeur est une FAUTE, jamais un repli
                // silencieux sur le défaut : `--base` désigne le répertoire que
                // le double-build efface récursivement, et le seul dégât
                // irréversible que cette commande puisse commettre serait de
                // l'effacer ailleurs que là où l'appelant croyait le poser.
                match argument.as_str() {
                    "--base" => match arguments.next() {
                        Some(valeur) => base = Some(PathBuf::from(valeur)),
                        None => faute = Some(String::from("--base attend un répertoire")),
                    },
                    "--cible" => match arguments.next() {
                        Some(valeur) => cible = Some(valeur),
                        None => faute = Some(String::from("--cible attend un triple de cible")),
                    },
                    autre => faute = Some(format!("argument inconnu : {autre}")),
                }
            }
            if let Some(faute) = faute {
                eprintln!("{faute}");
                eprintln!(
                    "usage : cargo xtask double-build [--base <répertoire>] [--cible <triple>]"
                );
                return 64;
            }
            let plan = xtask::reproductible::Plan {
                source: racine.clone(),
                paquet: String::from("shogen-verifier"),
                base: base.unwrap_or_else(|| std::env::temp_dir().join("shogen-double-build")),
                cible,
            };
            match xtask::reproductible::executer(&plan) {
                Ok(rapport) => {
                    println!();
                    rapport.imprimer();
                    if rapport.vert() { 0 } else { 1 }
                }
                Err(erreur) => {
                    // Fail-closed : ce qui empêche de conclure est ROUGE.
                    eprintln!("D6 — double-build : ROUGE — {erreur}");
                    1
                }
            }
        }
        _ => {
            eprintln!("usage : cargo xtask <verify|gates|emettre-exemple|muter|double-build>");
            eprintln!("  verify           : toutes les gates + fmt + clippy (l'entrée de CI)");
            eprintln!("  gates            : les gates lexicales seules, sans sous-processus cargo");
            eprintln!("  emettre-exemple  : écrit le lot d'exemple du walking skeleton");
            eprintln!("  muter            : écrit une copie du lot avec un octet remplacé");
            eprintln!(
                "  double-build     : construit le vérificateur deux fois sous 6 variations d'environnement et compare les octets (ADR-0012 D6)"
            );
            64
        }
    }
}
