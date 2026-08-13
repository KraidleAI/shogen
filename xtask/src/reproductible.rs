//! **Le double-build de reproductibilité** — ADR-0012 D6.
//!
//! Rattachement (G0), au texte de la décision : la norme retenue est la
//! Définition 1 de Lamb & Zacchiroli — « every build produces bit-for-bit
//! identical artifacts, no matter the environment in which the build is
//! performed » —, cible **bit-à-bit pour `shogen-verifier`, Linux x86_64
//! d'abord**, « contrôlée dès le walking skeleton par un **double-build à
//! environnement varié** dont les empreintes sont comparées, gate bloquante ».
//! Le jeu de variations est celui qu'ADR-0012 D6 inline, calqué en plus petit
//! sur la pratique Debian : **six** — horloge (+18 mois), nom d'hôte,
//! locale/langue, fuseau horaire, chemin absolu du répertoire de build,
//! utilisateur.
//!
//! Trois contraintes de forme, chacune héritée d'une doctrine et non d'un goût :
//!
//! 1. **Couverture avant verdict** (ADR-0013, invariant 2) : chaque variation
//!    imprime *comment* elle a été exercée — au moyen fort, en substitut nommé,
//!    ou pas du tout avec son motif. Une variation que la plateforme ne permet
//!    pas ne disparaît jamais en silence. Elle ne rend pas non plus le verdict
//!    rouge : c'est un fait de plateforme, pas une violation — et le vert qui
//!    en sort « n'autorise aucun énoncé » sur ce qui n'a pas été varié
//!    (ADR-0012, « Ce que la décision coûte »).
//! 2. **Fail-closed** : toute construction qui échoue, tout binaire absent,
//!    toute lecture impossible est un ROUGE, jamais un « on n'a pas pu
//!    conclure ».
//! 3. **Zéro autorité ambiante** (ADR-0012 D7) : les deux constructions
//!    partent d'un environnement dont les variables de compilation héritées
//!    ont été **retirées** (`RUSTFLAGS`, `CARGO_TARGET_DIR`, …). Ce que le
//!    build reçoit est déclaré ici ou vient d'un fichier committé — jamais
//!    d'un réglage de poste. Corollaire opérationnel : si la reproductibilité
//!    exigeait un `--remap-path-prefix`, il entrerait par `.cargo/config.toml`
//!    ou par le profil du manifeste, sous revue, et non par cette commande.
//!
//! Windows : le bit-à-bit n'y est **pas** la cible ratifiée (D6 : « Windows *à
//! terme* et sans date »). La commande y tourne quand même et dit ce qu'elle a
//! pu varier — l'asymétrie de plateforme se publie (ADR-0012, coût nommé).

use shogen_core::{empreinte_en_hexadecimal, empreinte_sha256};
use std::path::{Path, PathBuf};
use std::process::Command;

/// L'instant de la construction A, **fixe**.
///
/// La commande ne lit aucune horloge : deux exécutions du double-build voient
/// le même couple d'instants, sinon le double-build serait lui-même une source
/// de variation non déclarée. (Même discipline que le lot d'exemple.)
const HORLOGE_A: u64 = 1_754_000_000;

/// +18 mois, la valeur nommée par la source (Lamb & Zacchiroli p. 5, reprise
/// par ADR-0012 D6), comptée en **548 jours** : l'unité « mois » n'a pas de
/// longueur, un décalage exact en a besoin d'une.
const DECALAGE_18_MOIS: u64 = 548 * 24 * 3600;

/// Le nom du répertoire de la construction B — délibérément plus long que
/// `a` : la variation « chemin absolu du répertoire de build » ne change pas
/// seulement le contenu du chemin, elle change sa **longueur**, ce qui
/// déplacerait tout ce qui l'incorpore.
const REPERTOIRE_B: &str = "b-chemin-absolu-notablement-plus-long-pour-en-varier-la-longueur";

/// Entrées jamais copiées dans les arbres de construction : poids (`.git`,
/// `target`), ou octets qui ne quittent pas le poste (`biblio`, DEVOPS §1).
/// La liste est **imprimée** avec le rapport : ce qui n'est pas copié se dit.
const ENTREES_NON_COPIEES: &[&str] = &[".git", "target", "biblio", "s2-harness"];

/// Comment une variation a été obtenue — ou pourquoi elle ne l'a pas été.
pub enum Moyen {
    /// Exercée au moyen fort : l'entrée d'environnement réelle a changé.
    Fort(String),
    /// Exercée par un substitut, avec ce que le substitut **ne couvre pas**.
    Substitut { moyen: String, non_couvert: String },
    /// Non exercée sur cette plateforme, avec le motif.
    NonExercee { motif: String },
}

/// Une des six variations d'ADR-0012 D6.
pub struct Variation {
    pub nom: &'static str,
    pub moyen: Moyen,
}

impl Variation {
    fn etiquette(&self) -> &'static str {
        match self.moyen {
            Moyen::Fort(_) => "[exercée]   ",
            Moyen::Substitut { .. } => "[substitut] ",
            Moyen::NonExercee { .. } => "[NON EXERCÉE]",
        }
    }
}

/// Le résultat de la comparaison octet à octet des deux binaires.
pub enum Comparaison {
    Identiques,
    /// Le **premier** octet divergent, à sa position.
    DivergenceOctet {
        position: usize,
        a: u8,
        b: u8,
    },
    /// Aucune divergence dans le préfixe commun, mais des tailles différentes.
    TaillesDifferentes {
        prefixe_commun: usize,
        taille_a: usize,
        taille_b: usize,
    },
}

/// Compare deux binaires : le premier octet divergent fait foi.
///
/// Fonction **pure** — c'est elle qui décide du verdict, et c'est elle que les
/// témoins de `xtask/tests/reproductible.rs` exercent sans construire quoi que
/// ce soit.
pub fn comparer(a: &[u8], b: &[u8]) -> Comparaison {
    for (position, (octet_a, octet_b)) in a.iter().zip(b.iter()).enumerate() {
        if octet_a != octet_b {
            return Comparaison::DivergenceOctet {
                position,
                a: *octet_a,
                b: *octet_b,
            };
        }
    }
    if a.len() == b.len() {
        Comparaison::Identiques
    } else {
        Comparaison::TaillesDifferentes {
            prefixe_commun: a.len().min(b.len()),
            taille_a: a.len(),
            taille_b: b.len(),
        }
    }
}

/// Ce qu'on construit deux fois.
pub struct Plan {
    /// Racine du workspace à copier (jamais construite sur place).
    pub source: PathBuf,
    /// Paquet passé à `cargo build --package`.
    pub paquet: String,
    /// Répertoire de travail où naissent les deux arbres.
    pub base: PathBuf,
    /// Triple de cible explicite (`--target`), ou la cible hôte si absent.
    pub cible: Option<String>,
}

/// Le rapport du double-build, dans l'ordre où il s'imprime.
pub struct RapportDoubleBuild {
    pub paquet: String,
    pub cible: String,
    pub toolchain: String,
    pub repertoire_a: String,
    pub repertoire_b: String,
    /// Les deux binaires produits — imprimés pour qu'un tiers puisse les
    /// reprendre, et lus par le mutant de gate qui vérifie que la divergence
    /// est bien celle qu'il a injectée.
    pub binaire_a: PathBuf,
    pub binaire_b: PathBuf,
    pub variations: Vec<Variation>,
    pub notes: Vec<String>,
    pub empreinte_a: String,
    pub empreinte_b: String,
    pub taille_a: usize,
    pub taille_b: usize,
    pub comparaison: Comparaison,
}

impl RapportDoubleBuild {
    pub fn vert(&self) -> bool {
        matches!(self.comparaison, Comparaison::Identiques)
    }

    /// Couverture d'abord, verdict ensuite (ADR-0013, invariant 2).
    pub fn imprimer(&self) {
        println!("--- D6 — double-build de reproductibilité (ADR-0012 D6) ---");
        println!("  paquet construit deux fois : {}", self.paquet);
        println!("  cible                      : {}", self.cible);
        println!("  toolchain (mesurée)        : {}", self.toolchain);
        println!("  construction A             : {}", self.repertoire_a);
        println!("  construction B             : {}", self.repertoire_b);
        println!("  variations entre A et B (couverture — 6 ratifiées, ADR-0012 D6) :");
        for variation in &self.variations {
            println!("    {} {}", variation.etiquette(), variation.nom);
            match &variation.moyen {
                Moyen::Fort(moyen) => println!("        moyen : {moyen}"),
                Moyen::Substitut { moyen, non_couvert } => {
                    println!("        substitut   : {moyen}");
                    println!("        NON COUVERT : {non_couvert}");
                }
                Moyen::NonExercee { motif } => println!("        motif : {motif}"),
            }
        }
        let (fortes, substituts, absentes) = self.decompte();
        println!(
            "  couverture : {fortes} variation(s) au moyen fort, {substituts} en substitut, {absentes} non exercée(s), sur 6 ratifiées"
        );
        for note in &self.notes {
            println!("  note : {note}");
        }
        println!("  empreintes SHA-256 des deux binaires :");
        println!("    A = {} ({} octets)", self.empreinte_a, self.taille_a);
        println!("      {}", self.binaire_a.display());
        println!("    B = {} ({} octets)", self.empreinte_b, self.taille_b);
        println!("      {}", self.binaire_b.display());
        match &self.comparaison {
            Comparaison::Identiques => {
                println!("  VERDICT : VERT — octets identiques sous les variations exercées.");
                println!(
                    "  Ce que ce vert dit, et rien de plus : les mêmes octets sous CE jeu de variations. Un build reproductible sous 6 variations n'autorise aucun énoncé sur les autres (ADR-0012, coût publié)."
                );
            }
            Comparaison::DivergenceOctet { position, a, b } => {
                println!(
                    "  PREMIER OCTET DIVERGENT : position {position} (0x{position:08x}) — A = 0x{a:02x}, B = 0x{b:02x}"
                );
                println!(
                    "  VERDICT : ROUGE — la construction dépend de l'environnement (Définition 1 rompue)."
                );
            }
            Comparaison::TaillesDifferentes {
                prefixe_commun,
                taille_a,
                taille_b,
            } => {
                println!(
                    "  AUCUNE divergence dans le préfixe commun ({prefixe_commun} octets), mais les tailles diffèrent : A = {taille_a}, B = {taille_b}"
                );
                println!(
                    "  VERDICT : ROUGE — la construction dépend de l'environnement (Définition 1 rompue)."
                );
            }
        }
    }

    fn decompte(&self) -> (usize, usize, usize) {
        let mut fortes = 0;
        let mut substituts = 0;
        let mut absentes = 0;
        for variation in &self.variations {
            match variation.moyen {
                Moyen::Fort(_) => fortes += 1,
                Moyen::Substitut { .. } => substituts += 1,
                Moyen::NonExercee { .. } => absentes += 1,
            }
        }
        (fortes, substituts, absentes)
    }
}

/// Une construction : son répertoire, son environnement, son éventuel préfixe.
struct Construction {
    nom: &'static str,
    repertoire: PathBuf,
    environnement: Vec<(&'static str, String)>,
    /// Commande enveloppante (`faketime …`), vide quand il n'y en a pas.
    prefixe: Vec<String>,
}

/// Exécute le double-build et rend son rapport.
///
/// `Err` est réservé à ce qui empêche de **conclure** (copie impossible,
/// construction en échec, binaire introuvable) : l'appelant en fait un ROUGE.
pub fn executer(plan: &Plan) -> Result<RapportDoubleBuild, String> {
    verifier_base_jetable(plan)?;
    let repertoire_a = plan.base.join("a");
    let repertoire_b = plan.base.join(REPERTOIRE_B);

    // L'arbre de travail n'est jamais construit sur place : les deux
    // constructions vivent dans des copies, ce qui est aussi ce qui rend la
    // variation « chemin absolu » possible.
    let _ = std::fs::remove_dir_all(&plan.base);
    copier_arbre(&plan.source, &repertoire_a)?;
    copier_arbre(&plan.source, &repertoire_b)?;

    let faketime = faketime_disponible();
    // Ordre d'impression = ordre du jeu ratifié en ADR-0012 D6, jamais trié.
    let variations = variations_ratifiees(&repertoire_a, &repertoire_b, faketime);
    let notes = vec![
        format!(
            "entrées non copiées dans les arbres de construction : {}",
            ENTREES_NON_COPIEES.join(", ")
        ),
        String::from(
            "environnement de compilation hérité retiré des deux constructions (RUSTFLAGS, CARGO_ENCODED_RUSTFLAGS, CARGO_BUILD_RUSTFLAGS, RUSTDOCFLAGS, CARGO_TARGET_DIR) — zéro autorité ambiante, ADR-0012 D7",
        ),
        String::from(
            "les deux constructions sont verrouillées (`--locked`) : une résolution qui réécrirait le lockfile échoue au lieu de re-résoudre (ADR-0012 D1)",
        ),
    ];

    let construction_a = Construction {
        nom: "A",
        repertoire: repertoire_a.clone(),
        environnement: environnement_a(),
        prefixe: Vec::new(),
    };
    let construction_b = Construction {
        nom: "B",
        repertoire: repertoire_b.clone(),
        environnement: environnement_b(),
        prefixe: if faketime {
            vec![String::from("faketime"), String::from("+548d")]
        } else {
            Vec::new()
        },
    };

    let binaire_a = construire(plan, &construction_a)?;
    let binaire_b = construire(plan, &construction_b)?;

    let octets_a = std::fs::read(&binaire_a)
        .map_err(|erreur| format!("binaire A illisible ({}) : {erreur}", binaire_a.display()))?;
    let octets_b = std::fs::read(&binaire_b)
        .map_err(|erreur| format!("binaire B illisible ({}) : {erreur}", binaire_b.display()))?;

    Ok(RapportDoubleBuild {
        paquet: plan.paquet.clone(),
        cible: plan.cible.clone().unwrap_or_else(|| {
            format!("hôte ({}-{})", std::env::consts::ARCH, std::env::consts::OS)
        }),
        toolchain: toolchain_mesuree(),
        repertoire_a: repertoire_a.display().to_string(),
        repertoire_b: repertoire_b.display().to_string(),
        binaire_a,
        binaire_b,
        variations,
        notes,
        empreinte_a: empreinte_en_hexadecimal(&empreinte_sha256(&octets_a)),
        empreinte_b: empreinte_en_hexadecimal(&empreinte_sha256(&octets_b)),
        taille_a: octets_a.len(),
        taille_b: octets_b.len(),
        comparaison: comparer(&octets_a, &octets_b),
    })
}

/// `--base` est effacé récursivement à chaque exécution : il ne doit désigner
/// qu'un répertoire de travail jetable.
///
/// Deux refus, avant toute suppression. Ce sont des **garde-fous contre la
/// faute de frappe**, pas une frontière de sécurité : la comparaison de
/// chemins est lexicale, un lien symbolique bien placé la contournerait. Elle
/// coûte deux tests et évite la seule erreur irréversible que cette commande
/// puisse commettre.
fn verifier_base_jetable(plan: &Plan) -> Result<(), String> {
    if plan.source.starts_with(&plan.base) {
        return Err(format!(
            "refus : --base {} contient l'arbre source {} — l'effacer détruirait ce qu'on veut construire",
            plan.base.display(),
            plan.source.display()
        ));
    }
    if plan.base.starts_with(&plan.source) {
        // Mesuré : sans ce refus, la copie de l'arbre dans un répertoire situé
        // sous lui-même récurse jusqu'au débordement de pile.
        return Err(format!(
            "refus : --base {} est sous l'arbre source {} — la copie se recopierait elle-même sans fin",
            plan.base.display(),
            plan.source.display()
        ));
    }
    for temoin in ["Cargo.toml", ".git"] {
        if plan.base.join(temoin).exists() {
            return Err(format!(
                "refus d'effacer {} : ce répertoire porte un {temoin} — il ressemble à un arbre de travail, pas à un répertoire jetable",
                plan.base.display()
            ));
        }
    }
    Ok(())
}

/// Les six variations d'ADR-0012 D6, chacune avec l'état où la plateforme
/// courante la laisse. Rien n'est supposé : `faketime` est **probé**.
fn variations_ratifiees(
    repertoire_a: &Path,
    repertoire_b: &Path,
    faketime: bool,
) -> Vec<Variation> {
    let horloge_b = HORLOGE_A.wrapping_add(DECALAGE_18_MOIS);
    vec![
        Variation {
            nom: "horloge (+18 mois)",
            moyen: if faketime {
                Moyen::Fort(format!(
                    "faketime +548d sur la construction B, et SOURCE_DATE_EPOCH {HORLOGE_A} → {horloge_b}"
                ))
            } else {
                Moyen::Substitut {
                    moyen: format!("SOURCE_DATE_EPOCH {HORLOGE_A} → {horloge_b} (+548 jours)"),
                    non_couvert: String::from(
                        "l'horloge du système n'est pas déplacée (faketime absent du PATH) : un horodatage lu directement à l'horloge, sans passer par SOURCE_DATE_EPOCH, ne serait pas exercé par cette variation",
                    ),
                }
            },
        },
        Variation {
            nom: "nom d'hôte",
            moyen: Moyen::Substitut {
                moyen: String::from(
                    "HOSTNAME / HOST / COMPUTERNAME : shogen-batisseur-a → shogen-batisseur-b-au-nom-plus-long",
                ),
                non_couvert: String::from(
                    "le nom d'hôte du noyau est inchangé (le changer demande un espace de noms UTS ou des droits) : un outil qui appellerait gethostname(2) au lieu de lire l'environnement ne serait pas exercé",
                ),
            },
        },
        Variation {
            nom: "locale et langue",
            moyen: Moyen::Fort(String::from(
                "LANG / LC_ALL / LANGUAGE : C.UTF-8 + en_US:en → fr_FR.UTF-8 + fr_FR:fr",
            )),
        },
        Variation {
            nom: "fuseau horaire",
            moyen: Moyen::Fort(String::from("TZ : UTC → Asia/Tokyo")),
        },
        Variation {
            nom: "chemin absolu du répertoire de build",
            moyen: Moyen::Fort(format!(
                "{} → {} (contenu ET longueur différents)",
                repertoire_a.display(),
                repertoire_b.display()
            )),
        },
        Variation {
            nom: "utilisateur",
            moyen: Moyen::Substitut {
                moyen: String::from("USER / LOGNAME / USERNAME : batisseur-a → batisseur-b"),
                non_couvert: String::from(
                    "l'identité réelle du processus (UID, répertoire personnel) est inchangée : construire sous un second compte demande ce compte, que ni le poste ni le runner n'ont",
                ),
            },
        },
    ]
}

fn environnement_a() -> Vec<(&'static str, String)> {
    environnement(
        HORLOGE_A,
        "UTC",
        "C.UTF-8",
        "en_US:en",
        "shogen-batisseur-a",
        "batisseur-a",
    )
}

fn environnement_b() -> Vec<(&'static str, String)> {
    environnement(
        HORLOGE_A.wrapping_add(DECALAGE_18_MOIS),
        "Asia/Tokyo",
        "fr_FR.UTF-8",
        "fr_FR:fr",
        "shogen-batisseur-b-au-nom-plus-long",
        "batisseur-b",
    )
}

fn environnement(
    horloge: u64,
    fuseau: &str,
    locale: &str,
    langue: &str,
    hote: &str,
    utilisateur: &str,
) -> Vec<(&'static str, String)> {
    vec![
        ("SOURCE_DATE_EPOCH", horloge.to_string()),
        ("TZ", fuseau.to_string()),
        ("LANG", locale.to_string()),
        ("LC_ALL", locale.to_string()),
        ("LANGUAGE", langue.to_string()),
        ("HOSTNAME", hote.to_string()),
        ("HOST", hote.to_string()),
        ("COMPUTERNAME", hote.to_string()),
        ("USER", utilisateur.to_string()),
        ("LOGNAME", utilisateur.to_string()),
        ("USERNAME", utilisateur.to_string()),
    ]
}

/// Construit le paquet et rend le chemin du binaire produit.
fn construire(plan: &Plan, construction: &Construction) -> Result<PathBuf, String> {
    let cargo = std::env::var("CARGO").unwrap_or_else(|_| String::from("cargo"));
    let mut arguments = vec![
        String::from("build"),
        String::from("--locked"),
        String::from("--release"),
        String::from("--package"),
        plan.paquet.clone(),
    ];
    if let Some(cible) = &plan.cible {
        arguments.push(String::from("--target"));
        arguments.push(cible.clone());
    }

    let (programme, arguments) = match construction.prefixe.split_first() {
        Some((tete, queue)) => {
            let mut complets: Vec<String> = queue.to_vec();
            complets.push(cargo);
            complets.extend(arguments);
            (tete.clone(), complets)
        }
        None => (cargo, arguments),
    };

    println!(
        "--- construction {} — {} {} ---",
        construction.nom,
        programme,
        arguments.join(" ")
    );
    println!("    répertoire : {}", construction.repertoire.display());

    let mut commande = Command::new(&programme);
    commande
        .args(&arguments)
        .current_dir(&construction.repertoire);
    // Zéro autorité ambiante (ADR-0012 D7) : ce qui influence la compilation
    // est déclaré ici ou vient d'un fichier committé, jamais du poste.
    for variable in [
        "RUSTFLAGS",
        "CARGO_ENCODED_RUSTFLAGS",
        "CARGO_BUILD_RUSTFLAGS",
        "RUSTDOCFLAGS",
        "CARGO_TARGET_DIR",
    ] {
        commande.env_remove(variable);
    }
    commande.env("CARGO_TARGET_DIR", construction.repertoire.join("target"));
    for (nom, valeur) in &construction.environnement {
        commande.env(nom, valeur);
    }

    let statut = commande.status().map_err(|erreur| {
        format!(
            "construction {} : exécution impossible — {erreur}",
            construction.nom
        )
    })?;
    if !statut.success() {
        return Err(format!(
            "construction {} en échec ({statut}) — ROUGE fail-closed : le double-build ne conclut pas sur une construction qui n'a pas abouti",
            construction.nom
        ));
    }

    let mut binaire = construction.repertoire.join("target");
    if let Some(cible) = &plan.cible {
        binaire = binaire.join(cible);
    }
    let binaire =
        binaire
            .join("release")
            .join(format!("{}{}", plan.paquet, std::env::consts::EXE_SUFFIX));
    if !binaire.is_file() {
        return Err(format!(
            "construction {} : binaire attendu absent — {}",
            construction.nom,
            binaire.display()
        ));
    }
    Ok(binaire)
}

/// `faketime` est-il utilisable ? Probé, jamais supposé.
fn faketime_disponible() -> bool {
    Command::new("faketime")
        .arg("--version")
        .output()
        .map(|sortie| sortie.status.success())
        .unwrap_or(false)
}

/// La toolchain réellement servie, **mesurée** — un rapport de reproductibilité
/// sans la version du compilateur ne dit rien (ADR-0012 D2 : la toolchain est
/// une dépendance de build).
fn toolchain_mesuree() -> String {
    Command::new("rustc")
        .arg("--version")
        .output()
        .ok()
        .filter(|sortie| sortie.status.success())
        .map(|sortie| String::from_utf8_lossy(&sortie.stdout).trim().to_string())
        .unwrap_or_else(|| String::from("(non mesurable : `rustc --version` a échoué)"))
}

/// Copie récursive de l'arbre, `ENTREES_NON_COPIEES` exclues à tout niveau.
fn copier_arbre(source: &Path, cible: &Path) -> Result<(), String> {
    std::fs::create_dir_all(cible)
        .map_err(|erreur| format!("création de {} impossible : {erreur}", cible.display()))?;
    let entrees = std::fs::read_dir(source)
        .map_err(|erreur| format!("lecture de {} impossible : {erreur}", source.display()))?;
    for entree in entrees {
        let entree = entree
            .map_err(|erreur| format!("entrée illisible dans {} : {erreur}", source.display()))?;
        let nom = entree.file_name();
        if ENTREES_NON_COPIEES
            .iter()
            .any(|ignoree| nom.eq_ignore_ascii_case(*ignoree))
        {
            continue;
        }
        let chemin = entree.path();
        let destination = cible.join(&nom);
        if chemin.is_dir() {
            copier_arbre(&chemin, &destination)?;
        } else {
            std::fs::copy(&chemin, &destination).map_err(|erreur| {
                format!(
                    "copie de {} vers {} impossible : {erreur}",
                    chemin.display(),
                    destination.display()
                )
            })?;
        }
    }
    Ok(())
}
