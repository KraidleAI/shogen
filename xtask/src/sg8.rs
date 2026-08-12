//! **S-G8 `journal`** — l'intégrité mécanique du registre JOURNAL.md.
//!
//! Rattachement : DEVOPS §5 (« une ligne de JOURNAL.md par unité de
//! travail ») et 12 §10 item 2 (la gate garde le journal). Ce que la gate
//! contrôle : le registre **se lit comme un registre** — table présente,
//! trois cellules non vides par ligne, date ISO, ordre chronologique non
//! décroissant (une ligne insérée au mauvais endroit réordonne l'histoire —
//! le cas s'est produit le jour où cette gate a été écrite).
//!
//! **Résidu nommé** : la *complétude* (« une ligne PAR unité de travail »)
//! n'est pas mécanisable — aucun scanner ne sait qu'une unité a eu lieu sans
//! sa ligne. La gate tient la forme du registre ; la discipline d'écriture
//! reste à l'orchestrateur (DEVOPS §5).

use crate::rapport::Rapport;
use std::path::Path;

pub fn executer(racine: &Path) -> Rapport {
    let mut rapport = Rapport::nouveau("S-G8", "journal (intégrité mécanique de JOURNAL.md)");
    rapport.chemins_couverts.push(String::from("JOURNAL.md"));

    let chemin = racine.join("JOURNAL.md");
    let texte = match std::fs::read_to_string(&chemin) {
        Ok(texte) => {
            rapport.presents = 1;
            rapport.examines = 1;
            texte
        }
        Err(erreur) => {
            rapport.incident(format!(
                "JOURNAL.md illisible ({erreur}) — le journal est une exigence DEVOPS §5, la gate refuse de conclure"
            ));
            return rapport;
        }
    };

    let mut lignes_de_donnees = 0usize;
    let mut date_precedente: Option<String> = None;
    let mut en_tete_vu = false;

    for (index, ligne) in texte.lines().enumerate() {
        let numero = index.saturating_add(1);
        let nette = ligne.trim();
        if !nette.starts_with('|') {
            continue;
        }
        let cellules: Vec<&str> = nette.trim_matches('|').split('|').map(str::trim).collect();

        // L'en-tête et son séparateur.
        if !en_tete_vu {
            if cellules.first().copied() == Some("date") {
                if cellules != ["date", "unité", "résultat"] {
                    rapport.violation(
                        String::from("JOURNAL.md"),
                        numero,
                        format!(
                            "en-tête inattendu : {cellules:?} — attendu | date | unité | résultat |"
                        ),
                        nette.to_string(),
                    );
                }
                en_tete_vu = true;
            }
            continue;
        }
        // Ligne de séparation markdown : que des tirets/espaces, ET au moins
        // une cellule non vide — sans ce second terme, `|  |  |  |` passerait
        // pour un séparateur par vacuité (revue G2 du 2026-08-13, mineure 6).
        if cellules.iter().all(|cellule| {
            cellule
                .chars()
                .all(|caractere| caractere == '-' || caractere == ' ')
        }) && cellules.iter().any(|cellule| !cellule.is_empty())
        {
            continue;
        }

        // Une ligne de données : trois cellules non vides, date ISO, ordre.
        lignes_de_donnees = lignes_de_donnees.saturating_add(1);
        if cellules.len() != 3 || cellules.iter().any(|cellule| cellule.is_empty()) {
            rapport.violation(
                String::from("JOURNAL.md"),
                numero,
                format!(
                    "ligne de journal malformée : {} cellule(s), attendu 3 non vides (| date | unité | résultat |)",
                    cellules.len()
                ),
                extrait_court(nette),
            );
            continue;
        }
        let date = cellules.first().copied().unwrap_or("");
        if !date_iso_valide(date) {
            rapport.violation(
                String::from("JOURNAL.md"),
                numero,
                format!("date non ISO (AAAA-MM-JJ) : « {date} »"),
                extrait_court(nette),
            );
            continue;
        }
        if let Some(precedente) = &date_precedente
            && date < precedente.as_str()
        {
            rapport.violation(
                String::from("JOURNAL.md"),
                numero,
                format!(
                    "ordre chronologique rompu : {date} après {precedente} — une ligne insérée au mauvais endroit réordonne l'histoire"
                ),
                extrait_court(nette),
            );
        }
        date_precedente = Some(date.to_string());
    }

    if !en_tete_vu {
        rapport.incident(String::from(
            "aucun en-tête de table | date | unité | résultat | trouvé — JOURNAL.md n'est pas le registre attendu",
        ));
    }
    if lignes_de_donnees == 0 && en_tete_vu {
        rapport.incident(String::from(
            "table de journal vide — le journal a été instancié avec au moins l'unité qui l'instancie (12 §8.3)",
        ));
    }

    rapport.notes.push(format!(
        "{lignes_de_donnees} ligne(s) d'unité contrôlée(s) : 3 cellules, date ISO, ordre non décroissant"
    ));
    rapport.notes.push(String::from(
        "résidu : la complétude (une ligne PAR unité) n'est pas mécanisable — discipline DEVOPS §5, hors gate",
    ));
    rapport
}

fn date_iso_valide(date: &str) -> bool {
    let octets = date.as_bytes();
    octets.len() == 10
        && octets.iter().enumerate().all(|(index, octet)| match index {
            4 | 7 => *octet == b'-',
            _ => octet.is_ascii_digit(),
        })
}

fn extrait_court(ligne: &str) -> String {
    let mut extrait: String = ligne.chars().take(80).collect();
    if extrait.len() < ligne.len() {
        extrait.push('\u{2026}');
    }
    extrait
}
