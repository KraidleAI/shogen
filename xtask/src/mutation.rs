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
    /// Vrai si `cargo-mutants` a rendu le code 0 : le run a conclu proprement.
    /// C'est la seule condition sous laquelle « zéro mutant mesuré » peut être
    /// un état légitime (diff de documentation) et non un run effondré
    /// (revue G2 vague 1 — la famille « vert à vide »).
    pub run_propre: bool,
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
    ///
    /// Fail-closed sur l'absence de mesure (revue G2 vague 1) : un score
    /// absent n'est un vert QUE sur un diff dont le run a conclu proprement
    /// (`run_propre` — diff de documentation, zéro mutant engendré, code 0
    /// de l'outil). Partout ailleurs, l'absence de score est un refus de
    /// conclure, jamais un vert.
    pub fn vert(&self) -> bool {
        if !self.regressions.is_empty() {
            return false;
        }
        match self.score() {
            Some(score) => self.sur_diff || score >= PLANCHER,
            None => self.sur_diff && self.run_propre,
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
    // Répertoire de sortie NEUF par exécution (revue G2 vague 1) : la gate ne
    // peut plus consommer la sortie périmée d'un run antérieur comme si elle
    // était la mesure du jour — une sortie d'hier est illisible par
    // construction, pas par discipline. Sous target/, donc hors dépôt.
    let sortie_racine = racine
        .join("target")
        .join(format!("mutants-run-{}", std::process::id()));
    std::fs::create_dir_all(&sortie_racine).map_err(|erreur| {
        format!(
            "répertoire de sortie du run incréable ({}) : {erreur}",
            sortie_racine.display()
        )
    })?;
    let sortie = sortie_racine.join("mutants.out");

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
        .arg("--output")
        .arg(&sortie_racine)
        .current_dir(racine);
    if let Some(diff) = diff {
        commande.arg("--in-diff").arg(diff);
    }

    let statut = commande
        .status()
        .map_err(|erreur| format!("cargo-mutants inexécutable : {erreur} — l'outil s'installe à version exacte (`cargo install cargo-mutants --locked --version 27.1.0`), contrôle R-8 au rapport de passe du 2026-08-13"))?;
    // Le code de sortie n'est PAS jeté (revue G2 vague 1) : un code non nul
    // couvre aussi bien « des mutants ont survécu » — le fait que cette gate
    // est là pour juger — que l'erreur d'usage ou l'échec de ligne de base.
    // On ne départage pas par une table de codes (non documentée par l'outil,
    // et un chiffre non mesuré ne s'écrit pas) : on départage par la MESURE —
    // un run non propre qui n'a mesuré aucun mutant n'a pas de verdict.
    let run_propre = statut.success();

    // Quand le diff n'engendre AUCUN mutant, cargo-mutants imprime « No
    // mutants to filter », sort en 0 et n'écrit AUCUN fichier de sortie —
    // pas même vides (mesuré au premier run réel de la gate, CI
    // 31697390467 : la pousse ne touchait pas shogen-core et le fail-closed
    // « fichier absent = erreur » a classé rouge un cas légitime). Les
    // fichiers absents ne valent donc « listes vides » QUE sur un run
    // propre ; sur un run non propre, l'absence reste une erreur — c'est un
    // run interrompu.
    let tues = lire_liste_ou_vide(&sortie.join("caught.txt"), run_propre)?.len();
    let mut survivants = lire_liste_ou_vide(&sortie.join("missed.txt"), run_propre)?;
    survivants.extend(lire_liste_ou_vide(&sortie.join("timeout.txt"), run_propre)?);
    survivants.sort();
    let non_viables = lire_liste_ou_vide(&sortie.join("unviable.txt"), run_propre)?.len();

    if !run_propre && tues == 0 && survivants.is_empty() && non_viables == 0 {
        return Err(format!(
            "cargo-mutants a rendu le code {:?} sans mesurer aucun mutant : \
             un run qui n'a pas conclu n'a pas de verdict — l'absence de score \
             est un refus de conclure, jamais un vert",
            statut.code()
        ));
    }

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
        run_propre,
    })
}

/// Lit un fichier de sortie de `cargo-mutants` : une ligne par mutant.
///
/// Un fichier absent est une **erreur** : `cargo-mutants` les écrit tous les
/// quatre, même vides. Absent veut dire que l'outil n'a pas tourné jusqu'au
/// bout, et un score calculé sur un run interrompu est un faux.
/// `lire_liste`, sauf que l'ABSENCE du fichier vaut liste vide sur un run
/// PROPRE (code 0) : c'est le comportement documenté par la mesure de
/// cargo-mutants 27.1.0 quand le diff n'engendre aucun mutant — il n'écrit
/// rien du tout. Sur un run non propre, l'absence reste l'erreur de
/// `lire_liste` : un run interrompu n'a pas de listes.
fn lire_liste_ou_vide(chemin: &Path, run_propre: bool) -> Result<Vec<String>, String> {
    if run_propre && !chemin.exists() {
        return Ok(Vec::new());
    }
    lire_liste(chemin)
}

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
