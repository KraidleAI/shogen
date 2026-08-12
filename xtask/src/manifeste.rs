//! Analyse minimale et **fail-closed** des sections de dépendances d'un
//! manifeste.
//!
//! Aucun analyseur TOML n'est introduit : R-8 exige un contrôle de registre
//! avant toute dépendance nouvelle, et une gate qui dépend d'un arbre de crates
//! pour dire si l'arbre de crates est licite se mord la queue. La contrepartie
//! est assumée et **rendue visible** : toute ligne de section de dépendances
//! que cet analyseur ne comprend pas est signalée comme non analysable, ce qui
//! rend la gate ROUGE. Il refuse ce qu'il ne sait pas lire ; il ne le tolère
//! jamais.

/// Une déclaration de dépendance repérée dans un manifeste.
pub struct Declaration {
    pub ligne: usize,
    pub section: String,
    pub nom: String,
    pub reste: String,
}

pub struct AnalyseManifeste {
    pub declarations: Vec<Declaration>,
    /// Lignes de section de dépendances non analysables : (ligne, contenu).
    pub non_analysables: Vec<(usize, String)>,
}

fn est_section_de_dependances(entete: &str) -> bool {
    entete.ends_with("dependencies") || entete.contains("dependencies.")
}

/// Nom de section normalisé : `dependencies`, `dev-dependencies` ou
/// `build-dependencies`, quelle que soit la cible ou la sous-table.
fn categorie(entete: &str) -> String {
    if entete.contains("dev-dependencies") {
        String::from("dev-dependencies")
    } else if entete.contains("build-dependencies") {
        String::from("build-dependencies")
    } else if entete.contains("dependencies") {
        String::from("dependencies")
    } else {
        String::from(entete)
    }
}

pub fn analyser(texte: &str) -> AnalyseManifeste {
    let mut declarations = Vec::new();
    let mut non_analysables = Vec::new();
    let mut section = String::new();
    let mut dans_dependances = false;
    let mut sous_table: Option<String> = None;

    for (index, brute) in texte.lines().enumerate() {
        let numero = index.saturating_add(1);
        let ligne = brute.trim();
        if ligne.is_empty() || ligne.starts_with('#') {
            continue;
        }
        if ligne.starts_with('[') {
            let entete = ligne
                .trim_start_matches('[')
                .trim_end_matches(']')
                .trim()
                .to_string();
            dans_dependances = est_section_de_dependances(&entete);
            section = categorie(&entete);
            sous_table = None;
            if dans_dependances
                && entete.contains("dependencies.")
                && let Some(position) = entete.rfind("dependencies.")
            {
                let nom = entete
                    .get(position.saturating_add("dependencies.".len())..)
                    .unwrap_or("")
                    .trim()
                    .to_string();
                if !nom.is_empty() {
                    sous_table = Some(nom.clone());
                    declarations.push(Declaration {
                        ligne: numero,
                        section: section.clone(),
                        nom,
                        reste: String::new(),
                    });
                }
            }
            continue;
        }
        if !dans_dependances {
            continue;
        }
        if sous_table.is_some() {
            // Corps d'une sous-table [dependencies.nom] : les clés y sont des
            // attributs de la dépendance déjà déclarée par l'en-tête.
            if let Some(derniere) = declarations.last_mut() {
                derniere.reste.push_str(ligne);
                derniere.reste.push(' ');
            }
            continue;
        }
        let ouvrantes = ligne.matches('{').count();
        let fermantes = ligne.matches('}').count();
        if ouvrantes != fermantes {
            non_analysables.push((numero, ligne.to_string()));
            continue;
        }
        let Some(position) = ligne.find('=') else {
            non_analysables.push((numero, ligne.to_string()));
            continue;
        };
        let gauche = ligne.get(..position).unwrap_or("").trim();
        let droite = ligne
            .get(position.saturating_add(1)..)
            .unwrap_or("")
            .trim()
            .to_string();
        let nom = match gauche.find('.') {
            Some(point) => gauche.get(..point).unwrap_or(gauche).trim().to_string(),
            None => gauche.to_string(),
        };
        let nom = nom.trim_matches('"').to_string();
        if nom.is_empty()
            || !nom
                .chars()
                .all(|c| c.is_ascii_alphanumeric() || c == '-' || c == '_')
        {
            non_analysables.push((numero, ligne.to_string()));
            continue;
        }
        declarations.push(Declaration {
            ligne: numero,
            section: section.clone(),
            nom,
            reste: droite,
        });
    }

    AnalyseManifeste {
        declarations,
        non_analysables,
    }
}

/// Extrait la contrainte de version d'une déclaration, si elle en porte une.
pub fn contrainte_de_version(reste: &str) -> Option<String> {
    let texte = reste.trim();
    if texte.starts_with('"') {
        return Some(texte.trim_matches('"').to_string());
    }
    let position = texte.find("version")?;
    let apres = texte.get(position..)?;
    let egal = apres.find('=')?;
    let valeur = apres.get(egal.saturating_add(1)..)?.trim_start();
    let sans_guillemet = valeur.strip_prefix('"')?;
    let fin = sans_guillemet.find('"')?;
    Some(sans_guillemet.get(..fin)?.to_string())
}
