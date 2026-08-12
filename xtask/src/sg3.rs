//! **S-G3 `fail-closed`** — les formes qui divergent au lieu de refuser.
//!
//! Ce qu'elle casse (DEVOPS §3) : « `unwrap`/`expect`/`panic!`/arithmétique non
//! vérifiée dans `shogen-verifier` et `shogen-core` » — « un vérificateur qui
//! panique sur un lot malveillant est un déni qui ne dit pas son nom ».
//! Pourquoi : ADR-0010, points 1 et 5 (*fail-safe defaults*, Saltzer &
//! Schroeder) et ADR-0009, point 2 (`forbid(unsafe_code)` comme gate).
//!
//! **Ce que cette gate NE fait PAS**, écrit ici pour qu'aucune phrase du dépôt
//! ne le lise à l'envers (ADR-0010, §Coûts point 6) : elle est **lexicale**.
//! Elle ne dit rien de l'échec d'allocation, d'une panique venue d'une
//! dépendance, ni du comportement du binaire sur une entrée hostile — c'est le
//! test de mutation d'octet (`crates/shogen-core/tests`) qui prend le relais,
//! et « zéro panique » n'est jamais établi par cette gate.
//!
//! Limite connue et assumée : l'interdit d'opérateur arithmétique rejetterait
//! aussi une borne de trait `A + B`. Le cœur n'en porte aucune aujourd'hui ; le
//! jour où il en aura besoin, la gate se raffine par ADR — jamais par une
//! exception de chemin ni un `#[allow]` (charte §2, ADR-0013 point 1).

use crate::rapport::{Rapport, lire};
use crate::roles::{ROLES, chemin_relatif, fichiers_rust};
use crate::source::{code_seul, est_caractere_de_mot, ligne_de, occurrences_bornees};
use std::path::Path;

/// Formes qui divergent, repérées bornées (donc `debug_assert!` ne déclenche
/// pas `assert!` — les assertions de debug sont admises par ADR-0010, point 6).
pub const FORMES_DIVERGENTES: &[&str] = &[
    "unwrap(",
    "expect(",
    "panic!",
    "unreachable!",
    "todo!",
    "unimplemented!",
    "assert!",
    "assert_eq!",
    "assert_ne!",
    "unsafe",
    "get_unchecked",
    "unwrap_unchecked",
];

/// L'attribut qui doit figurer en tête de chaque fichier racine de rôle.
pub const ATTRIBUT_FORBID: &str = "#![forbid(unsafe_code)]";

pub fn executer(racine: &Path) -> Rapport {
    let mut rapport = Rapport::nouveau("S-G3", "fail-closed (aucune forme divergente)");

    for role in ROLES {
        rapport
            .chemins_couverts
            .push(format!("{} : {}/**/*.rs", role.nom, role.racine_source));

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

            for forme in FORMES_DIVERGENTES {
                for decalage in occurrences_bornees(&code, forme) {
                    let (ligne, contenu) = ligne_de(&code, decalage);
                    rapport.violation(
                        relatif.clone(),
                        ligne,
                        format!(
                            "forme divergente « {forme} » dans le rôle « {} » — une entrée mal formée doit être une valeur d'erreur, jamais une divergence (ADR-0010, point 1)",
                            role.nom
                        ),
                        contenu,
                    );
                }
            }

            for (decalage, motif) in indexations(&code) {
                let (ligne, contenu) = ligne_de(&code, decalage);
                rapport.violation(
                    relatif.clone(),
                    ligne,
                    format!(
                        "indexation non contrôlée « {motif} » dans le rôle « {} » — utiliser `.get(..)` et traiter l'absence",
                        role.nom
                    ),
                    contenu,
                );
            }

            for (decalage, motif) in arithmetiques(&code) {
                let (ligne, contenu) = ligne_de(&code, decalage);
                rapport.violation(
                    relatif.clone(),
                    ligne,
                    format!(
                        "arithmétique non contrôlée « {motif} » dans le rôle « {} » — utiliser `checked_*` / `saturating_*` et nommer le cas limite",
                        role.nom
                    ),
                    contenu,
                );
            }
        }

        // `forbid(unsafe_code)` sur le fichier racine du rôle (ADR-0009, point 2)
        let racine_crate = racine.join(role.fichier_racine);
        match std::fs::read_to_string(&racine_crate) {
            Ok(texte) => {
                if !texte.contains(ATTRIBUT_FORBID) {
                    rapport.violation(
                        role.fichier_racine.to_string(),
                        1,
                        format!(
                            "attribut « {ATTRIBUT_FORBID} » absent du fichier racine du rôle « {} » — ADR-0009, point 2",
                            role.nom
                        ),
                        String::new(),
                    );
                }
            }
            Err(erreur) => rapport.incident(format!(
                "fichier racine de rôle illisible : {} ({erreur})",
                role.fichier_racine
            )),
        }
    }

    rapport.notes.push(String::from(
        "gate LEXICALE : elle rejette des formes nommées ; elle n'établit pas « le cœur ne peut pas paniquer » (ADR-0010, §Coûts point 6)",
    ));
    rapport
}

/// Repère les indexations `x[...]` : un crochet ouvrant précédé d'un caractère
/// d'identifiant, d'une parenthèse fermante ou d'un crochet fermant.
///
/// Les formes de type (`&[u8]`, `[u8; 8]`, `Vec<[u8; 4]>`) et les attributs
/// (`#[...]`) ne sont pas des indexations : leur crochet est précédé d'un
/// caractère qui n'est ni un identifiant ni une fermeture.
fn indexations(code: &str) -> Vec<(usize, String)> {
    /// Mots-clés qui peuvent précéder un crochet SANS qu'il s'agisse d'une
    /// indexation : position de type (`&'a mut [u8]`) ou de littéral de
    /// tableau (`for x in [..]`). Une durée de vie (`'a [u8]`) est traitée à
    /// part, par le caractère `'` qui la précède.
    const MOTS_NON_INDEXABLES: &[&str] = &[
        "mut", "in", "as", "return", "match", "dyn", "impl", "const", "static", "type", "where",
        "fn", "move", "ref",
    ];
    let octets = code.as_bytes();
    let mut trouvees = Vec::new();
    for (index, octet) in octets.iter().copied().enumerate() {
        if octet != b'[' || index == 0 {
            continue;
        }
        let mut fin_mot = index;
        while fin_mot > 0 {
            let caractere = octets.get(fin_mot.saturating_sub(1)).copied().unwrap_or(0);
            if caractere == b' ' || caractere == b'\t' {
                fin_mot = fin_mot.saturating_sub(1);
            } else {
                break;
            }
        }
        if fin_mot == 0 {
            continue;
        }
        let precedent = octets.get(fin_mot.saturating_sub(1)).copied().unwrap_or(0);
        if precedent == b')' || precedent == b']' {
            trouvees.push((index, String::from("…()[…]")));
            continue;
        }
        if !est_caractere_de_mot(precedent) {
            continue;
        }
        let mut debut = fin_mot;
        while debut > 0
            && est_caractere_de_mot(octets.get(debut.saturating_sub(1)).copied().unwrap_or(0))
        {
            debut = debut.saturating_sub(1);
        }
        let avant = if debut == 0 {
            0
        } else {
            octets.get(debut.saturating_sub(1)).copied().unwrap_or(0)
        };
        if avant == b'\'' {
            continue;
        }
        let identifiant = code.get(debut..fin_mot).unwrap_or("");
        if MOTS_NON_INDEXABLES.contains(&identifiant) {
            continue;
        }
        trouvees.push((index, format!("{identifiant}[…]")));
    }
    trouvees
}

/// Repère les opérateurs arithmétiques nus. `->` n'en est pas un ; `<<`/`>>` et
/// les opérateurs binaires (`&`, `|`, `^`) ne sont pas visés (ils ne débordent
/// pas silencieusement sur nos types) ; les méthodes `checked_*`,
/// `saturating_*`, `wrapping_*` sont la voie licite.
fn arithmetiques(code: &str) -> Vec<(usize, String)> {
    let octets = code.as_bytes();
    let mut trouvees = Vec::new();
    for (index, octet) in octets.iter().copied().enumerate() {
        let suivant = octets.get(index.saturating_add(1)).copied().unwrap_or(0);
        let precedent = if index == 0 {
            0
        } else {
            octets.get(index.saturating_sub(1)).copied().unwrap_or(0)
        };
        let motif = match octet {
            b'+' => "+",
            b'-' => {
                if suivant == b'>' {
                    continue;
                }
                "-"
            }
            b'*' => "*",
            b'/' => "/",
            b'%' => "%",
            _ => continue,
        };
        // `::*` (import glob) n'est pas une multiplication.
        if octet == b'*' && precedent == b':' {
            continue;
        }
        trouvees.push((index, String::from(motif)));
    }
    trouvees
}
