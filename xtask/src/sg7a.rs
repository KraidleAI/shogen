//! **S-G7a** — le volet MÉCANISABLE de S-G7 aujourd'hui : version exacte au
//! manifeste, portée par rôle à chemins exacts.
//!
//! Rattachement : ADR-0012 **D3** — « Dans `crates/shogen-core` et
//! `crates/shogen-verifier`, chaque dépendance directe porte une version
//! **exacte** » — et §Registres touchés : « le critère "version non exacte" est
//! **porté par rôle, à chemins exacts** ».
//!
//! **Ce qui manque à S-G7, et qui n'est pas ici** : licences hors liste et
//! advisories non traitées. Ces deux volets exigent `cargo-deny`, dont
//! l'installation est un acte de chaîne d'approvisionnement à part entière.
//! `deny.toml` est écrit et versionné ; tant que le binaire n'est pas installé
//! et **vu tourner**, cette passe ne rapporte aucun vert sur ces deux volets et
//! le blocage est nommé dans le rapport de passe. Une gate non instanciée qui
//! se tairait serait exactement le mode d'échec que la doctrine interdit.

use crate::manifeste::{analyser, contrainte_de_version};
use crate::rapport::{Rapport, lire};
use crate::roles::ROLES;
use std::path::Path;

pub fn executer(racine: &Path) -> Rapport {
    let mut rapport = Rapport::nouveau("S-G7a", "deps — version exacte au manifeste (ADR-0012 D3)");

    for role in ROLES {
        rapport
            .chemins_couverts
            .push(format!("{} : {}", role.nom, role.manifeste));
        let chemin = racine.join(role.manifeste);
        if !chemin.is_file() {
            rapport.incident(format!(
                "manifeste de rôle absent : {} (la gate refuse de conclure)",
                role.manifeste
            ));
            continue;
        }
        rapport.presents = rapport.presents.saturating_add(1);
        let Some(texte) = lire(&mut rapport, racine, &chemin) else {
            continue;
        };
        let analyse = analyser(&texte);
        for (ligne, contenu) in &analyse.non_analysables {
            rapport.violation(
                role.manifeste.to_string(),
                *ligne,
                String::from("ligne de dépendance non analysable par la gate — refus fail-closed"),
                contenu.clone(),
            );
        }
        for declaration in &analyse.declarations {
            match contrainte_de_version(&declaration.reste) {
                Some(contrainte) => {
                    if !contrainte.trim_start().starts_with('=') {
                        rapport.violation(
                            role.manifeste.to_string(),
                            declaration.ligne,
                            format!(
                                "version non exacte « {contrainte} » pour « {} » dans le rôle « {} » — ADR-0012 D3 exige `=x.y.z` sur ce périmètre",
                                declaration.nom, role.nom
                            ),
                            declaration.reste.clone(),
                        );
                    }
                }
                None => rapport.violation(
                    role.manifeste.to_string(),
                    declaration.ligne,
                    format!(
                        "aucune contrainte de version pour « {} » dans le rôle « {} » — ADR-0012 D3 : le changement d'une dépendance directe doit être un acte de revue VISIBLE au manifeste",
                        declaration.nom, role.nom
                    ),
                    declaration.reste.clone(),
                ),
            }
        }
    }

    rapport.notes.push(String::from(
        "cette gate ne porte QUE le volet « version exacte » de S-G7 ; les volets licences/bans/sources/advisories sont tenus par `cargo deny --locked check` (deny.toml, `just deny`, étape CI dédiée) et NE sont pas établis par ce vert",
    ));
    rapport
}
