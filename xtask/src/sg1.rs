//! **S-G1 `forbidden-symbols`** — aucun nom de transport dans le cœur ni dans
//! le vérificateur.
//!
//! Ce qu'elle casse (DEVOPS §3) : « un nom de transport (`tlsn`, `reclaim`,
//! `tee`, `zkpass`…) dans `shogen-core` ou `shogen-verifier` ».
//! Pourquoi : ADR-0001 — « le vocabulaire de faits de Shōgen ne nomme aucun
//! transport » ; les transports sont des adapters interchangeables, et la
//! couche Shōgen ne dépend d'aucun d'eux en particulier.
//!
//! Portée : sources **et manifestes** des deux rôles — un nom de transport qui
//! entre par une ligne de dépendance est un nom de transport quand même.
//! Le texte est scanné **brut** (commentaires et littéraux compris).

use crate::rapport::{Rapport, lire};
use crate::roles::{ROLES, chemin_relatif, fichiers_rust};
use crate::source::{ligne_de, occurrences_bornees};
use std::path::Path;

/// Les noms de transport interdits au cœur et au vérificateur.
///
/// Origine : ADR-0001 (§Contexte — TLSNotary, Reclaim, zkPass, Opacity,
/// vlayer, DECO ; attestations TEE) et DEVOPS §3, ligne S-G1. La liste est
/// **fermée et versionnée ici** : l'élargir est un resserrage (licite) ; la
/// réduire demande une ADR (charte §2).
pub const NOMS_DE_TRANSPORT: &[&str] = &[
    "tlsn",
    "tlsnotary",
    "notary",
    "notaire",
    "reclaim",
    "zkpass",
    "zktls",
    "deco",
    "opacity",
    "vlayer",
    "tee",
    "sgx",
    "enclave",
    "mpc",
];

pub fn executer(racine: &Path) -> Rapport {
    let mut rapport = Rapport::nouveau("S-G1", "forbidden-symbols (aucun nom de transport)");

    for role in ROLES {
        rapport
            .chemins_couverts
            .push(format!("{} : {}/**/*.rs", role.nom, role.racine_source));
        rapport
            .chemins_couverts
            .push(format!("{} : {}", role.nom, role.manifeste));

        let recensement = fichiers_rust(racine, role.racine_source);
        for incident in &recensement.incidents {
            rapport.incident(incident.clone());
        }
        let manifeste = racine.join(role.manifeste);
        let mut a_examiner = recensement.fichiers.clone();
        if manifeste.is_file() {
            a_examiner.push(manifeste);
        } else {
            rapport.incident(format!(
                "manifeste de rôle absent : {} (la gate refuse de conclure)",
                role.manifeste
            ));
        }
        rapport.presents = rapport.presents.saturating_add(a_examiner.len());

        for chemin in &a_examiner {
            let Some(texte) = lire(&mut rapport, racine, chemin) else {
                continue;
            };
            let relatif = chemin_relatif(racine, chemin);
            for nom in NOMS_DE_TRANSPORT {
                for decalage in occurrences_bornees(&texte, nom) {
                    let (ligne, contenu) = ligne_de(&texte, decalage);
                    rapport.violation(
                        relatif.clone(),
                        ligne,
                        format!(
                            "nom de transport « {nom} » dans le rôle « {} » — ADR-0001 : les transports sont des adapters, le cœur n'en nomme aucun",
                            role.nom
                        ),
                        contenu,
                    );
                }
            }
        }
    }

    rapport.notes.push(format!(
        "{} nom(s) de transport surveillé(s), bornés par non-mots (« committee » ne déclenche pas « tee ») ; texte brut, commentaires compris",
        NOMS_DE_TRANSPORT.len()
    ));
    rapport
}
