//! La **sélection par rôle à chemins exacts** — invariant 1 d'ADR-0013 :
//! « une gate énumère les chemins qu'elle couvre ; elle ne fait jamais confiance
//! à un nom qu'un fichier se choisit lui-même ».
//!
//! Conséquence directe : renommer une crate, déplacer un fichier hors de
//! `crates/<role>/src`, ou supprimer le répertoire d'un rôle ne fait pas
//! disparaître la gate — cela la rend ROUGE (`RepertoireDeRoleAbsent`).

use std::path::{Path, PathBuf};

/// Un rôle du workspace, avec les chemins EXACTS que les gates couvrent.
pub struct Role {
    /// Nom du rôle, tel qu'il est imprimé.
    pub nom: &'static str,
    /// Répertoire des sources, relatif à la racine du workspace.
    pub racine_source: &'static str,
    /// Manifeste du rôle, relatif à la racine du workspace.
    pub manifeste: &'static str,
    /// Fichier racine de la crate (celui qui doit porter `forbid(unsafe_code)`).
    pub fichier_racine: &'static str,
}

/// Les deux rôles sous gate : le cœur et le vérificateur (ADR-0010, DEVOPS §2).
/// `xtask/` et `adapters/` n'y sont PAS : ce sont des coquilles, elles ont le
/// droit de faire de l'I/O et de nommer des transports.
pub const ROLES: &[Role] = &[
    Role {
        nom: "coeur",
        racine_source: "crates/shogen-core/src",
        manifeste: "crates/shogen-core/Cargo.toml",
        fichier_racine: "crates/shogen-core/src/lib.rs",
    },
    Role {
        nom: "verificateur",
        racine_source: "crates/shogen-verifier/src",
        manifeste: "crates/shogen-verifier/Cargo.toml",
        fichier_racine: "crates/shogen-verifier/src/main.rs",
    },
];

/// Résultat d'un recensement de fichiers : ce qui est présent, et l'incident
/// éventuel qui empêche de le recenser.
pub struct Recensement {
    pub fichiers: Vec<PathBuf>,
    pub incidents: Vec<String>,
}

/// Recense récursivement les fichiers `.rs` sous `racine/relatif`, triés.
///
/// Fail-closed : un répertoire de rôle absent ou illisible est un **incident**,
/// pas un ensemble vide — sinon la gate deviendrait verte en supprimant ce
/// qu'elle surveille.
pub fn fichiers_rust(racine: &Path, relatif: &str) -> Recensement {
    fichiers_par_extension(racine, relatif, "rs")
}

/// Recense récursivement les fichiers d'une extension sous `racine/relatif`,
/// triés — la brique commune des recensements de gate (R-3 : une seule
/// implémentation, `fichiers_rust` et `fichiers_markdown` s'y ramènent).
pub fn fichiers_par_extension(racine: &Path, relatif: &str, extension: &str) -> Recensement {
    let repertoire = racine.join(relatif);
    let mut fichiers = Vec::new();
    let mut incidents = Vec::new();
    if !repertoire.is_dir() {
        incidents.push(format!(
            "répertoire absent ou illisible : {relatif} (chemin exact attendu — la gate refuse de conclure)"
        ));
        return Recensement {
            fichiers,
            incidents,
        };
    }
    parcourir(&repertoire, extension, &mut fichiers, &mut incidents);
    fichiers.sort();
    if fichiers.is_empty() {
        incidents.push(format!(
            "aucun fichier .{extension} sous {relatif} : la gate refuse de conclure sur un périmètre vide"
        ));
    }
    Recensement {
        fichiers,
        incidents,
    }
}

fn parcourir(
    repertoire: &Path,
    extension: &str,
    fichiers: &mut Vec<PathBuf>,
    incidents: &mut Vec<String>,
) {
    let entrees = match std::fs::read_dir(repertoire) {
        Ok(entrees) => entrees,
        Err(erreur) => {
            incidents.push(format!(
                "lecture impossible de {} : {erreur}",
                repertoire.display()
            ));
            return;
        }
    };
    for entree in entrees {
        match entree {
            Ok(entree) => {
                let chemin = entree.path();
                if chemin.is_dir() {
                    parcourir(&chemin, extension, fichiers, incidents);
                } else if chemin.extension().is_some_and(|e| e == extension) {
                    fichiers.push(chemin);
                }
            }
            Err(erreur) => incidents.push(format!(
                "entrée illisible dans {} : {erreur}",
                repertoire.display()
            )),
        }
    }
}

/// Chemin affiché relativement à la racine, en séparateurs `/` (stable
/// d'une plateforme à l'autre — la CI tourne Windows ET Linux).
pub fn chemin_relatif(racine: &Path, chemin: &Path) -> String {
    let relatif = chemin.strip_prefix(racine).unwrap_or(chemin);
    relatif.to_string_lossy().replace('\\', "/")
}
