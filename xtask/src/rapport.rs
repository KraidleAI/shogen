//! Le format de rapport commun à toutes les gates.
//!
//! Invariant 2 d'ADR-0013 : « **ligne de couverture avant verdict** — une gate
//! imprime sa couverture (N examinés sur N présents) **avant** de dire vert ou
//! rouge. La couverture est un signal affiché, jamais le critère de succès. »
//!
//! Conséquence de conception, pour ne pas trahir la seconde moitié de la
//! phrase : un fichier présent mais non examiné n'est pas soustrait de la
//! couverture — c'est une **violation** à part entière (`incidents`). Le verdict
//! reste donc décidé par les violations, et la couverture reste un signal.

use std::path::Path;

/// Une violation constatée, localisée.
pub struct Violation {
    pub chemin: String,
    pub ligne: usize,
    pub motif: String,
    pub extrait: String,
}

/// Le rapport d'une gate.
pub struct Rapport {
    pub gate: &'static str,
    pub titre: &'static str,
    pub chemins_couverts: Vec<String>,
    pub presents: usize,
    pub examines: usize,
    pub violations: Vec<Violation>,
    pub notes: Vec<String>,
}

impl Rapport {
    pub fn nouveau(gate: &'static str, titre: &'static str) -> Self {
        Self {
            gate,
            titre,
            chemins_couverts: Vec::new(),
            presents: 0,
            examines: 0,
            violations: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn violation(&mut self, chemin: String, ligne: usize, motif: String, extrait: String) {
        self.violations.push(Violation {
            chemin,
            ligne,
            motif,
            extrait,
        });
    }

    /// Un incident de couverture (fichier ou rôle non examinable) est une
    /// violation : la gate refuse de conclure sur ce qu'elle n'a pas lu.
    pub fn incident(&mut self, motif: String) {
        self.violations.push(Violation {
            chemin: String::from("(couverture)"),
            ligne: 0,
            motif,
            extrait: String::new(),
        });
    }

    pub fn vert(&self) -> bool {
        self.violations.is_empty()
    }

    pub fn imprimer(&self) {
        println!("--- {} — {} ---", self.gate, self.titre);
        println!("  chemins couverts (exacts) :");
        for chemin in &self.chemins_couverts {
            println!("    {chemin}");
        }
        // LA ligne de couverture, imprimée AVANT le verdict.
        println!(
            "  couverture : {} fichier(s) examiné(s) sur {} présent(s)",
            self.examines, self.presents
        );
        for note in &self.notes {
            println!("  note : {note}");
        }
        if self.violations.is_empty() {
            println!("  VERDICT : VERT ({} violation(s))", self.violations.len());
        } else {
            for violation in &self.violations {
                if violation.ligne > 0 {
                    println!(
                        "  VIOLATION {}:{} — {}",
                        violation.chemin, violation.ligne, violation.motif
                    );
                } else {
                    println!("  VIOLATION {} — {}", violation.chemin, violation.motif);
                }
                if !violation.extrait.is_empty() {
                    println!("      | {}", violation.extrait);
                }
            }
            println!("  VERDICT : ROUGE ({} violation(s))", self.violations.len());
        }
    }
}

/// Lit un fichier en texte ; rend `None` et enregistre l'incident si la lecture
/// échoue (fail-closed : un fichier illisible n'est jamais « propre »).
pub fn lire(rapport: &mut Rapport, racine: &Path, chemin: &Path) -> Option<String> {
    match std::fs::read_to_string(chemin) {
        Ok(texte) => {
            rapport.examines = rapport.examines.saturating_add(1);
            Some(texte)
        }
        Err(erreur) => {
            let relatif = crate::roles::chemin_relatif(racine, chemin);
            rapport.incident(format!(
                "fichier présent mais non examinable ({relatif}) : {erreur}"
            ));
            None
        }
    }
}
