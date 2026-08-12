//! Le lot d'exemple du walking skeleton, et sa mutation.
//!
//! Ces deux commandes vivent dans `xtask` — la coquille — et non dans le
//! vérificateur : le vérificateur ne réclame aucune capacité qu'il n'exerce, et
//! il n'a aucune raison de savoir **écrire** (ADR-0010, point 8, *least
//! privilege* de Saltzer & Schroeder).
//!
//! Le témoignage d'exemple est **fixe** : champs factices, `instant` porté en
//! donnée. Aucune horloge n'est lue nulle part dans la chaîne (12 §5).

use shogen_core::{TemoignageTrivial, encoder_temoignage};
use std::path::Path;

/// Le lot d'exemple, identique d'une exécution et d'une machine à l'autre.
pub fn temoignage_exemple() -> TemoignageTrivial {
    TemoignageTrivial {
        source: String::from("exemple:source-factice"),
        instant: 1_754_000_000,
        contenu: b"lot d'exemple du walking skeleton".to_vec(),
    }
}

pub fn emettre(chemin: &Path) -> Result<usize, String> {
    let octets = encoder_temoignage(&temoignage_exemple());
    if let Some(parent) = chemin.parent()
        && !parent.as_os_str().is_empty()
    {
        std::fs::create_dir_all(parent)
            .map_err(|erreur| format!("création de {} impossible : {erreur}", parent.display()))?;
    }
    std::fs::write(chemin, &octets)
        .map_err(|erreur| format!("écriture de {} impossible : {erreur}", chemin.display()))?;
    Ok(octets.len())
}

/// Écrit une copie du lot dont l'octet `index` est remplacé par `valeur`.
pub fn muter(entree: &Path, sortie: &Path, index: usize, valeur: u8) -> Result<(), String> {
    let mut octets = std::fs::read(entree)
        .map_err(|erreur| format!("lecture de {} impossible : {erreur}", entree.display()))?;
    let longueur = octets.len();
    let case = octets
        .get_mut(index)
        .ok_or_else(|| format!("index {index} hors du lot ({longueur} octets)"))?;
    *case = valeur;
    std::fs::write(sortie, &octets)
        .map_err(|erreur| format!("écriture de {} impossible : {erreur}", sortie.display()))?;
    Ok(())
}
