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
        // ADR-0011 seuils 3 et 4. Hors de `verify` pour la même raison que
        // `double-build` : 12 min 12 s mesurées le 2026-08-13 pour le run
        // complet (417 mutants, `-j 4`), au-dessus du budget de 10 min/PR
        // d'ADR-0011 seuil 4. Elle est bloquante là où elle est budgétée — le job CI
        // dédié (.github/workflows/mutation.yml), en deux régimes.
        "mutation" => {
            let mut diff = None;
            let mut faute = None;
            while let Some(argument) = arguments.next() {
                match argument.as_str() {
                    "--in-diff" => match arguments.next() {
                        Some(valeur) => diff = Some(PathBuf::from(valeur)),
                        None => {
                            faute = Some(String::from(
                                "--in-diff attend le chemin d'un fichier de diff unifié",
                            ));
                        }
                    },
                    autre => faute = Some(format!("argument inconnu : {autre}")),
                }
            }
            if let Some(faute) = faute {
                eprintln!("{faute}");
                eprintln!("usage : cargo xtask mutation [--in-diff <fichier>]");
                return 64;
            }
            match xtask::mutation::executer(&racine, diff.as_deref()) {
                Ok(rapport) => {
                    println!();
                    rapport.imprimer();
                    if rapport.vert() { 0 } else { 1 }
                }
                Err(erreur) => {
                    // Fail-closed : ce qui empêche de conclure est ROUGE.
                    eprintln!("mutation : ROUGE — {erreur}");
                    1
                }
            }
        }
        // ADR-0011 seuil 7. Comme `double-build`, cette commande n'entre PAS
        // dans `verify` : son unité est le budget de temps (≥ 15 min en CI,
        // ≥ 4 h en nightly), pas la seconde. Elle est bloquante là où elle est
        // budgétée : le job CI dédié (.github/workflows/fuzz.yml).
        "fuzz" => {
            let mut graine = xtask::fuzz::GRAINE_PAR_DEFAUT;
            let mut duree = xtask::fuzz::DUREE_PAR_DEFAUT;
            let mut faute = None;
            while let Some(argument) = arguments.next() {
                // Même règle que `double-build` : un drapeau privé de sa
                // valeur, ou une valeur illisible, est une FAUTE — jamais un
                // repli silencieux sur le défaut. Un budget qu'on croit avoir
                // donné et qui n'a pas été lu produit un vert qui ne vaut rien.
                match argument.as_str() {
                    "--graine" => match arguments.next().and_then(|v| lire_u64(&v)) {
                        Some(valeur) => graine = valeur,
                        None => {
                            faute = Some(String::from(
                                "--graine attend un entier (décimal, ou hexadécimal préfixé 0x)",
                            ));
                        }
                    },
                    "--duree" => match arguments.next().and_then(|v| v.parse::<u64>().ok()) {
                        Some(valeur) => duree = valeur,
                        None => faute = Some(String::from("--duree attend un nombre de secondes")),
                    },
                    autre => faute = Some(format!("argument inconnu : {autre}")),
                }
            }
            if let Some(faute) = faute {
                eprintln!("{faute}");
                eprintln!("usage : cargo xtask fuzz [--graine <entier>] [--duree <secondes>]");
                return 64;
            }
            let plan = xtask::fuzz::Plan {
                racine: racine.clone(),
                graine,
                duree: std::time::Duration::from_secs(duree),
            };
            match xtask::fuzz::executer(&plan) {
                Ok(rapport) => {
                    println!();
                    rapport.imprimer();
                    if rapport.vert() { 0 } else { 1 }
                }
                Err(erreur) => {
                    // Fail-closed : ce qui empêche de conclure est ROUGE.
                    eprintln!("fuzz : ROUGE — {erreur}");
                    1
                }
            }
        }
        // 13 §7 dette 3 (lot FUZZ). Hors de `verify` comme `fuzz` : les deux cartes viennent
        // d'`afl-showmap` sur la cible instrumentée, dans le job `cargo-afl` de fuzz.yml (Linux).
        "fuzz-distillation" => match (arguments.next(), arguments.next(), arguments.next()) {
            (Some(base), Some(corpus), None) => {
                match xtask::distillation::juger(&PathBuf::from(base), &PathBuf::from(corpus)) {
                    Ok(mesure) => {
                        mesure.imprimer();
                        if mesure.vert() { 0 } else { 1 }
                    }
                    Err(erreur) => {
                        // Fail-closed : ce qui empêche de conclure est ROUGE.
                        eprintln!("distillation : ROUGE — {erreur}");
                        1
                    }
                }
            }
            _ => {
                eprintln!("usage : cargo xtask fuzz-distillation <carte-sans-distillees> <carte>");
                64
            }
        },
        // Réécrit les graines DIRIGÉES du corpus — celles qui se déduisent des
        // formes du dépôt. Les contre-exemples, eux, ne se régénèrent pas :
        // ils sont écrits par une panique observée et restent au corpus.
        "fuzz-corpus" => match xtask::fuzz::ecrire_corpus_dirige(&racine) {
            Ok(rapport) => {
                for ligne in &rapport {
                    println!("{ligne}");
                }
                0
            }
            Err(erreur) => {
                eprintln!("{erreur}");
                65
            }
        },
        _ => {
            eprintln!(
                "usage : cargo xtask <verify|gates|emettre-exemple|muter|double-build|mutation|fuzz|fuzz-corpus|fuzz-distillation>"
            );
            eprintln!("  verify           : toutes les gates + fmt + clippy (l'entrée de CI)");
            eprintln!("  gates            : les gates lexicales seules, sans sous-processus cargo");
            eprintln!("  emettre-exemple  : écrit le lot d'exemple du walking skeleton");
            eprintln!("  muter            : écrit une copie du lot avec un octet remplacé");
            eprintln!(
                "  double-build     : construit le vérificateur deux fois sous 6 variations d'environnement et compare les octets (ADR-0012 D6)"
            );
            eprintln!(
                "  mutation         : score de mutation du cœur, seuil 80 % et non-régression (ADR-0011 seuils 3 et 4)"
            );
            eprintln!(
                "  fuzz             : éprouve le vérificateur sur des suites d'octets tirées depuis le corpus committé (ADR-0011 seuil 7)"
            );
            eprintln!("  fuzz-corpus      : réécrit les graines dirigées du corpus de fuzz");
            eprintln!(
                "  fuzz-distillation : juge deux cartes afl-showmap, sans et avec les graines distillées (13 §7 dette 3)"
            );
            64
        }
    }
}

/// Lit un entier décimal, ou hexadécimal préfixé `0x`.
///
/// Les graines s'impriment en hexadécimal (`{:#018x}`) : elles doivent se
/// **redonner** sous la forme où elles ont été lues, sinon le rejeu exact
/// qu'ADR-0011 point 2 exige devient une conversion à la main.
fn lire_u64(texte: &str) -> Option<u64> {
    match texte
        .strip_prefix("0x")
        .or_else(|| texte.strip_prefix("0X"))
    {
        Some(reste) => u64::from_str_radix(&reste.replace('_', ""), 16).ok(),
        None => texte.replace('_', "").parse::<u64>().ok(),
    }
}
