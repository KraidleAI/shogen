//! **S-G2 `verifier-isolation`** — la direction des arêtes est un fait de
//! link-time, pas une intention.
//!
//! Ce qu'elle casse (DEVOPS §3) : « une arête de dépendance du vérificateur
//! vers un adapter, ou une dépendance réseau/horloge dans le vérificateur ».
//! Pourquoi : ADR-0010, point 3 — « `shogen-verifier -> shogen-core`, et rien
//! d'autre » ; « offline, sans confiance dans Shōgen » doit être contrôlable
//! par un tiers depuis les manifestes.
//!
//! Trois contrôles, énoncés séparément parce qu'ils n'établissent pas la même
//! chose :
//!
//! * **(a) manifestes** — l'ensemble EXACT des dépendances déclarées par rôle ;
//! * **(b) fermeture réelle** — `cargo tree -e normal` : ce que le linker voit,
//!   transitives comprises. Ce contrôle a besoin de `cargo` ; il est sauté sur
//!   un arbre synthétique (mutants) et la note le dit ;
//! * **(c) lexical** — aucun appel d'horloge, de réseau ou d'aléa dans les
//!   sources ; et, pour le cœur seul, aucune I/O du tout (ADR-0010, point 1).
//!   Contrôle **syntaxique** : il rejette une liste de formes nommées, il
//!   n'établit pas « sans I/O » (ADR-0010, §Coûts point 6 ; gate mécanique
//!   complète — `no_std` — assignée à S3).

use crate::manifeste::analyser;
use crate::rapport::{Rapport, lire};
use crate::roles::{ROLES, chemin_relatif, fichiers_rust};
use crate::source::{code_seul, ligne_de, occurrences_nues};
use std::path::Path;

/// Formes d'horloge, de réseau et d'aléa — interdites aux DEUX rôles.
pub const FORMES_HORLOGE_RESEAU: &[&str] = &[
    "std::time",
    "SystemTime",
    "Instant::now",
    "UNIX_EPOCH",
    "std::net",
    "TcpStream",
    "TcpListener",
    "UdpSocket",
    "getrandom",
    "thread::sleep",
    "SystemTime::now",
];

/// Formes d'I/O et de journalisation — interdites au **cœur** seul (la coquille
/// a le droit d'en faire : ADR-0010, point 4).
pub const FORMES_IO_COEUR: &[&str] = &[
    "std::fs",
    "std::env",
    "std::io",
    "std::process",
    "println!",
    "eprintln!",
    "print!",
    "eprint!",
    "dbg!",
    "File::open",
    "File::create",
];

/// Dépendances directes admises, par rôle et par section.
fn admises(role: &str, section: &str) -> Vec<&'static str> {
    match (role, section) {
        ("coeur", "dependencies") => vec![],
        ("coeur", "build-dependencies") => vec![],
        ("coeur", "dev-dependencies") => vec!["proptest"],
        ("verificateur", "dependencies") => vec!["shogen-core"],
        ("verificateur", "build-dependencies") => vec![],
        ("verificateur", "dev-dependencies") => vec![],
        _ => vec![],
    }
}

pub fn executer(racine: &Path, avec_cargo: bool) -> Rapport {
    let mut rapport = Rapport::nouveau("S-G2", "verifier-isolation (arêtes, horloge, réseau)");

    for role in ROLES {
        rapport
            .chemins_couverts
            .push(format!("{} : {}", role.nom, role.manifeste));
        rapport
            .chemins_couverts
            .push(format!("{} : {}/**/*.rs", role.nom, role.racine_source));

        // (a) manifeste
        let chemin_manifeste = racine.join(role.manifeste);
        if chemin_manifeste.is_file() {
            rapport.presents = rapport.presents.saturating_add(1);
            if let Some(texte) = lire(&mut rapport, racine, &chemin_manifeste) {
                let analyse = analyser(&texte);
                for (ligne, contenu) in &analyse.non_analysables {
                    rapport.violation(
                        role.manifeste.to_string(),
                        *ligne,
                        String::from(
                            "ligne de dépendance non analysable par la gate — refus fail-closed",
                        ),
                        contenu.clone(),
                    );
                }
                for declaration in &analyse.declarations {
                    let permises = admises(role.nom, &declaration.section);
                    if !permises.contains(&declaration.nom.as_str()) {
                        rapport.violation(
                            role.manifeste.to_string(),
                            declaration.ligne,
                            format!(
                                "dépendance « {} » interdite en [{}] du rôle « {} » — admises : {:?} (ADR-0010, point 3)",
                                declaration.nom, declaration.section, role.nom, permises
                            ),
                            declaration.reste.clone(),
                        );
                    }
                    if declaration.reste.contains("adapters/")
                        || declaration.reste.contains("adapters\\")
                    {
                        rapport.violation(
                            role.manifeste.to_string(),
                            declaration.ligne,
                            format!(
                                "arête vers un adapter depuis le rôle « {} » — interdite sans exception (ADR-0001, ADR-0010 point 3)",
                                role.nom
                            ),
                            declaration.reste.clone(),
                        );
                    }
                }
            }
        } else {
            rapport.incident(format!(
                "manifeste de rôle absent : {} (la gate refuse de conclure)",
                role.manifeste
            ));
        }

        // (c) lexical
        let recensement = fichiers_rust(racine, role.racine_source);
        for incident in &recensement.incidents {
            rapport.incident(incident.clone());
        }
        rapport.presents = rapport.presents.saturating_add(recensement.fichiers.len());
        for chemin in &recensement.fichiers {
            let Some(texte) = lire(&mut rapport, racine, chemin) else {
                continue;
            };
            let code = code_seul(&texte);
            let relatif = chemin_relatif(racine, chemin);
            let mut interdits: Vec<&str> = FORMES_HORLOGE_RESEAU.to_vec();
            if role.nom == "coeur" {
                interdits.extend_from_slice(FORMES_IO_COEUR);
            }
            for forme in interdits {
                for decalage in occurrences_nues(&code, forme) {
                    let (ligne, contenu) = ligne_de(&code, decalage);
                    rapport.violation(
                        relatif.clone(),
                        ligne,
                        format!(
                            "forme interdite « {forme} » dans le rôle « {} » — le vérificateur ne réclame aucune capacité qu'il n'exerce (ADR-0010, points 1, 4 et 8)",
                            role.nom
                        ),
                        contenu,
                    );
                }
            }
        }
    }

    // (b) fermeture réelle des dépendances du vérificateur
    if avec_cargo {
        match fermeture_verificateur(racine) {
            Ok(crates) => {
                let attendues = ["shogen-verifier", "shogen-core"];
                let mut inattendues: Vec<String> = crates
                    .iter()
                    .filter(|nom| !attendues.contains(&nom.as_str()))
                    .cloned()
                    .collect();
                inattendues.sort();
                inattendues.dedup();
                if inattendues.is_empty() {
                    rapport.notes.push(format!(
                        "fermeture réelle (cargo tree -e normal) du vérificateur : {:?} — exactement l'arête attendue",
                        crates
                    ));
                } else {
                    rapport.violation(
                        String::from("crates/shogen-verifier (fermeture cargo tree)"),
                        0,
                        format!(
                            "dépendance(s) transitive(s) inattendue(s) dans le graphe du vérificateur : {inattendues:?}"
                        ),
                        String::new(),
                    );
                }
            }
            Err(erreur) => rapport.incident(format!(
                "fermeture de dépendances non contrôlable : {erreur} (la gate refuse de conclure)"
            )),
        }
    } else {
        rapport.notes.push(String::from(
            "contrôle (b) « fermeture réelle » sauté : arbre synthétique sans cargo — ce rapport n'établit que (a) et (c)",
        ));
    }

    rapport.notes.push(String::from(
        "(c) est syntaxique : il rejette des formes nommées, il n'établit pas « sans I/O » (ADR-0010, §Coûts point 6)",
    ));
    rapport
}

fn fermeture_verificateur(racine: &Path) -> Result<Vec<String>, String> {
    let cargo = std::env::var("CARGO").unwrap_or_else(|_| String::from("cargo"));
    let sortie = std::process::Command::new(cargo)
        .args([
            "tree",
            "--locked",
            "--package",
            "shogen-verifier",
            "--edges",
            "normal",
            "--prefix",
            "none",
            "--no-dedupe",
        ])
        .current_dir(racine)
        .output()
        .map_err(|erreur| format!("cargo tree inexécutable : {erreur}"))?;
    if !sortie.status.success() {
        return Err(format!(
            "cargo tree a échoué : {}",
            String::from_utf8_lossy(&sortie.stderr).trim()
        ));
    }
    let texte = String::from_utf8_lossy(&sortie.stdout).into_owned();
    let mut crates: Vec<String> = texte
        .lines()
        .filter_map(|ligne| ligne.split_whitespace().next())
        .filter(|nom| !nom.is_empty())
        .map(|nom| nom.to_string())
        .collect();
    crates.sort();
    crates.dedup();
    if crates.is_empty() {
        return Err(String::from("cargo tree n'a rien rendu"));
    }
    Ok(crates)
}
