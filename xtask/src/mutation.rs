//! La gate du **score de mutation du cœur** — ADR-0011 seuils 3 et 4,
//! échéance 4 de 13 §3.
//!
//! # Ce que cette gate mesure, et ce qu'elle ne mesure pas
//!
//! Le score de mutation est défini par ADR-0011 point 3, qui le tient de Jia &
//! Harman (2011) : « The mutation score (MS) is the ratio of the number of
//! killed mutants over the total number of non-equivalent mutants ». La
//! division se fait donc sur les mutants **non équivalents**, et non sur tous
//! les mutants générés. Ici :
//!
//! ```text
//!   score = tués / (tués + survivants)
//! ```
//!
//! Les mutants que `cargo-mutants` classe *unviable* (le mutant ne compile
//! pas) sont **hors du dénominateur** : un mutant qui ne compile pas n'est pas
//! un programme, donc ni équivalent ni non équivalent — le compter au
//! dénominateur baisserait le score pour une raison qui n'est pas une
//! faiblesse de la suite. Les mutants *timeout* sont comptés **avec les
//! survivants** : un mutant qui fait boucler la suite n'a pas été tué, et le
//! traiter autrement serait s'acheter du score sur une ambiguïté.
//!
//! Ce que la gate **n'établit pas** : que la suite détecte les fautes réelles.
//! Le coupling effect est déclaré empirique par ses auteurs — « There is, of
//! course, no hope of "proving" the coupling effect; it is an empirical
//! principle » (DeMillo, Lipton & Sayward p. 35). Le registre du projet
//! s'applique sans remise : « suite *tested* : N mutants, M tués, K survivants
//! justifiés, [date] » (09-vocabulaire).
//!
//! Et le score ne montera jamais mécaniquement à 1 : « Automatically detecting
//! all equivalent mutants is impossible » (Jia & Harman §II.B, p. 4). C'est
//! pourquoi la gate ne demande pas 100 %, mais 80 % **et** que chaque
//! survivant soit justifié nommément.
//!
//! # La non-régression est mécanique
//!
//! ADR-0011 seuil 3 exige « chaque survivant justifié nommément en une ligne,
//! plus non-régression ». Les deux tiennent dans un seul mécanisme : le
//! fichier [`SURVIVANTS`] est la ligne de base. Un survivant qui y figure est
//! justifié (la justification est sur la ligne) ; un survivant qui n'y figure
//! pas est une **régression** et la gate casse. Un survivant nu — mesuré,
//! non justifié — est une dette nue, interdite (règle du 2026-08-05).

use std::path::{Path, PathBuf};
use std::process::Command;

/// Le paquet muté — le cœur pur, et lui seul.
///
/// ADR-0011 alternative (e), rejetée sur le coût et sur le fond : « les
/// adapters font de l'I/O : muter un adapter mesure surtout la stabilité de
/// son environnement. La mutation se pose donc là où elle est bornée et
/// déterministe — le cœur pur. »
pub const PAQUET_MUTE: &str = "shogen-core";

/// La ligne de base des survivants justifiés, relative à la racine.
pub const SURVIVANTS: &str = "crates/shogen-core/survivants.txt";

/// Le plancher d'ADR-0011 seuil 3, en pour cent.
///
/// « *candidat — ratification mainteneur due* » comme les six autres seuils
/// (ADR-0011 point 6) : il s'applique fail-closed, et « aucun ne se desserre
/// sans ADR ».
pub const PLANCHER: f64 = 80.0;

/// Le nombre de constructions/tests menés de front.
///
/// Valeur fixe et non « le nombre de cœurs » : c'est celle sous laquelle le
/// budget publié d'ADR-0011 seuil 4 a été **mesuré** (12 min 12 s pour 417
/// mutants, 2026-08-13). Un parallélisme qui suivrait la machine ferait varier
/// le temps d'un facteur inconnu d'un runner à l'autre, et le budget cesserait
/// d'être vérifiable. Une machine à moins de 4 cœurs tiendra plus longtemps —
/// c'est le `timeout-minutes` du job qui l'attrape, pas un ajustement
/// silencieux.
pub const JOBS: usize = 4;

/// Le résultat d'une exécution de la gate.
pub struct Rapport {
    /// Mutants tués.
    pub tues: usize,
    /// Mutants survivants (`missed` + `timeout`).
    pub survivants: Vec<String>,
    /// Mutants non viables — hors dénominateur.
    pub non_viables: usize,
    /// Survivants absents de la ligne de base : les régressions.
    pub regressions: Vec<String>,
    /// Survivants de la ligne de base qui n'ont pas été revus — la ligne de
    /// base a vieilli, ou le périmètre mesuré était partiel.
    pub base_non_revue: Vec<String>,
    /// Vrai si l'exécution portait sur un diff seul (budget de PR).
    pub sur_diff: bool,
}

impl Rapport {
    /// Le dénominateur d'ADR-0011 point 3 : les mutants **non équivalents**.
    pub fn non_equivalents(&self) -> usize {
        self.tues.saturating_add(self.survivants.len())
    }

    /// Le score, en pour cent. `None` quand le dénominateur est nul — un score
    /// sur zéro mutant n'est pas 100 %, c'est l'absence de mesure.
    pub fn score(&self) -> Option<f64> {
        let denominateur = self.non_equivalents();
        if denominateur == 0 {
            return None;
        }
        Some((self.tues as f64 * 100.0) / (denominateur as f64))
    }

    /// Vert : le plancher est tenu ET aucun survivant nouveau.
    ///
    /// Sur un diff (budget de PR), le plancher ne s'applique pas : un diff
    /// d'une ligne peut n'engendrer que des mutants difficiles, et un score
    /// calculé sur trois mutants ne dit rien. Ce qui s'applique toujours,
    /// c'est la non-régression — c'est elle que la PR doit tenir.
    pub fn vert(&self) -> bool {
        if !self.regressions.is_empty() {
            return false;
        }
        if self.sur_diff {
            return true;
        }
        match self.score() {
            Some(score) => score >= PLANCHER,
            None => false,
        }
    }

    /// Imprime la mesure AVANT le verdict (ADR-0013 : la ligne de couverture
    /// passe avant la conclusion).
    pub fn imprimer(&self) {
        println!("--- score de mutation du cœur (ADR-0011 seuils 3 et 4) ---");
        println!("  paquet muté          : {PAQUET_MUTE}");
        println!(
            "  périmètre            : {}",
            if self.sur_diff {
                "diff de la PR (--in-diff) — budget d'ADR-0011 seuil 4"
            } else {
                "le paquet entier — run complet d'ADR-0011 seuil 3"
            }
        );
        println!("  mutants tués         : {}", self.tues);
        println!("  mutants survivants   : {}", self.survivants.len());
        println!(
            "  mutants non viables  : {} (hors dénominateur — un mutant qui ne compile pas n'est pas un programme)",
            self.non_viables
        );
        println!(
            "  non équivalents      : {} (dénominateur, Jia & Harman p. 4)",
            self.non_equivalents()
        );
        match self.score() {
            Some(score) => {
                println!("  SCORE                : {score:.4} % (tués / non équivalents)")
            }
            None => println!(
                "  SCORE                : aucun — dénominateur nul, il n'y a rien à mesurer"
            ),
        }
        println!(
            "  ce que ce score dit : la suite est *tested* sur cette population de fautes semées, à cette date. Le coupling effect est empirique (DeMillo p. 35) — il ne dit RIEN des fautes réelles."
        );

        if !self.survivants.is_empty() {
            println!("  survivants mesurés :");
            for survivant in &self.survivants {
                println!("    {survivant}");
            }
        }
        if !self.base_non_revue.is_empty() {
            println!(
                "  survivants de la ligne de base non revus dans ce périmètre : {}",
                self.base_non_revue.len()
            );
        }

        if self.regressions.is_empty() {
            println!("  non-régression : tenue — aucun survivant hors de la ligne de base");
        } else {
            println!(
                "  non-régression : ROMPUE — {} survivant(s) absent(s) de {SURVIVANTS} :",
                self.regressions.len()
            );
            for regression in &self.regressions {
                println!("    {regression}");
            }
            println!(
                "  chaque survivant se tue par un test, ou se justifie en une ligne dans {SURVIVANTS}. Un survivant nu est une dette nue, interdite (règle du 2026-08-05)."
            );
        }

        if self.vert() {
            println!("  VERDICT : VERT");
        } else {
            println!("  VERDICT : ROUGE");
        }
    }
}

/// Exécute `cargo-mutants` puis applique les deux critères d'ADR-0011.
///
/// `diff` porte le chemin d'un fichier de diff unifié pour le mode budget de
/// PR (`--in-diff`), ou `None` pour le run complet.
///
/// Fail-closed : tout ce qui empêche de conclure — outil absent, sortie
/// illisible, ligne de base absente — est une **erreur**, jamais un vert par
/// défaut.
pub fn executer(racine: &Path, diff: Option<&Path>) -> Result<Rapport, String> {
    let base = charger_ligne_de_base(racine)?;
    let sortie = racine.join("mutants.out");

    let mut commande = Command::new("cargo");
    commande
        .arg("mutants")
        .args(["--package", PAQUET_MUTE])
        .arg("--no-shuffle")
        // Parallélisme DÉCLARÉ, jamais hérité du défaut de l'outil. Motif de
        // dépôt : « tout ce dont un job dépend est déclaré là où il tourne »
        // (`.cargo/config.toml`, zéro autorité ambiante — ADR-0012 D7). Motif
        // de mesure : le budget d'ADR-0011 seuil 4 est un temps, et un temps
        // n'a de sens qu'à parallélisme connu. Fait constaté le 2026-08-13 :
        // la même gate lancée sans `--jobs` avait traité 36 mutants en 9 min
        // là où `-j 4` en traite 417 en 12 min 12 s — le défaut de l'outil
        // rendait le budget publié faux d'un ordre de grandeur.
        .args(["--jobs", &JOBS.to_string()])
        // La suite exécutée pour chaque mutant est celle du cœur et celle du
        // vérificateur — les deux qui exercent réellement `shogen-core`. Les
        // tests d'`xtask` en sont EXCLUS délibérément : ils lancent des
        // sous-processus `cargo` (gates, double-build), ce qui multiplierait
        // le temps par mutant sans rien ajouter au pouvoir de détection sur le
        // cœur. C'est un choix de budget (ADR-0011 seuil 4), dit comme tel.
        .args(["--cargo-test-arg", "--package"])
        .args(["--cargo-test-arg", PAQUET_MUTE])
        .args(["--cargo-test-arg", "--package"])
        .args(["--cargo-test-arg", "shogen-verifier"])
        .current_dir(racine);
    if let Some(diff) = diff {
        commande.arg("--in-diff").arg(diff);
    }

    let statut = commande
        .status()
        .map_err(|erreur| format!("cargo-mutants inexécutable : {erreur} — l'outil s'installe à version exacte (`cargo install cargo-mutants --locked --version 27.1.0`), contrôle R-8 au rapport de passe du 2026-08-13"))?;
    // Un code de sortie non nul de `cargo-mutants` signifie « des mutants ont
    // survécu » : ce n'est PAS une erreur d'exécution, c'est le fait que cette
    // gate est là pour juger. On ne le confond donc pas avec un échec d'outil,
    // et on lit les fichiers de sortie dans les deux cas. En revanche, une
    // sortie absente est bien une erreur — elle empêche de conclure.
    let _ = statut;

    let tues = lire_liste(&sortie.join("caught.txt"))?.len();
    let mut survivants = lire_liste(&sortie.join("missed.txt"))?;
    survivants.extend(lire_liste(&sortie.join("timeout.txt"))?);
    survivants.sort();
    let non_viables = lire_liste(&sortie.join("unviable.txt"))?.len();

    let regressions: Vec<String> = survivants
        .iter()
        .filter(|survivant| !base.iter().any(|ligne| ligne == *survivant))
        .cloned()
        .collect();
    let base_non_revue: Vec<String> = base
        .iter()
        .filter(|ligne| !survivants.iter().any(|survivant| survivant == *ligne))
        .cloned()
        .collect();

    Ok(Rapport {
        tues,
        survivants,
        non_viables,
        regressions,
        base_non_revue,
        sur_diff: diff.is_some(),
    })
}

/// Lit un fichier de sortie de `cargo-mutants` : une ligne par mutant.
///
/// Un fichier absent est une **erreur** : `cargo-mutants` les écrit tous les
/// quatre, même vides. Absent veut dire que l'outil n'a pas tourné jusqu'au
/// bout, et un score calculé sur un run interrompu est un faux.
fn lire_liste(chemin: &Path) -> Result<Vec<String>, String> {
    let texte = std::fs::read_to_string(chemin).map_err(|erreur| {
        format!(
            "sortie de cargo-mutants illisible ({}) : {erreur} — un score calculé sur un run interrompu serait un faux",
            chemin.display()
        )
    })?;
    Ok(texte
        .lines()
        .map(str::trim)
        .filter(|ligne| !ligne.is_empty())
        .map(String::from)
        .collect())
}

/// Charge la ligne de base des survivants justifiés.
///
/// Format : une ligne par survivant, `<mutant> # <justification>`. Le `#` et
/// ce qui suit sont la justification exigée par ADR-0011 seuil 3 ; le mutant
/// est la clé. Les lignes vides et celles qui commencent par `#` sont des
/// commentaires.
///
/// Une justification **vide** est un refus : le fichier existerait alors pour
/// contourner la règle qu'il sert.
pub fn charger_ligne_de_base(racine: &Path) -> Result<Vec<String>, String> {
    let chemin = racine.join(SURVIVANTS);
    let texte = std::fs::read_to_string(&chemin).map_err(|erreur| {
        format!(
            "ligne de base des survivants illisible ({}) : {erreur} — sans elle, « chaque survivant justifié » (ADR-0011 seuil 3) n'est pas mécanisable",
            chemin.display()
        )
    })?;
    let mut mutants = Vec::new();
    for (numero, ligne) in texte.lines().enumerate() {
        let ligne = ligne.trim();
        if ligne.is_empty() || ligne.starts_with('#') {
            continue;
        }
        let Some((mutant, justification)) = ligne.split_once('#') else {
            return Err(format!(
                "{SURVIVANTS} ligne {} : survivant sans justification — « {ligne} ». La forme est `<mutant> # <justification>` ; un survivant nu est une dette nue, interdite (règle du 2026-08-05).",
                numero.saturating_add(1)
            ));
        };
        if justification.trim().is_empty() {
            return Err(format!(
                "{SURVIVANTS} ligne {} : justification vide — « {ligne} ». Un « # » suivi de rien contourne la règle qu'il sert.",
                numero.saturating_add(1)
            ));
        }
        mutants.push(mutant.trim().to_string());
    }
    mutants.sort();
    Ok(mutants)
}

/// Le chemin de la ligne de base, pour l'appelant qui veut l'afficher.
pub fn chemin_de_la_ligne_de_base(racine: &Path) -> PathBuf {
    racine.join(SURVIVANTS)
}
