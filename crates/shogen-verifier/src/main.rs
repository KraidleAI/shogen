#![forbid(unsafe_code)]
#![deny(
    clippy::unwrap_used,
    clippy::expect_used,
    clippy::panic,
    clippy::indexing_slicing,
    clippy::arithmetic_side_effects
)]
//! Vérificateur offline — la **coquille impérative** du walking skeleton
//! (ADR-0010, point 4 : « I/O, lecture d'arguments : binaire CLI »).
//!
//! Ce qu'il fait, et rien de plus : lit des fichiers d'octets, les passe à la
//! bibliothèque, imprime — puis **nomme son résidu**. Il ne réclame aucune
//! capacité qu'il n'exerce : ni réseau, ni horloge, ni aléa (ADR-0010, point 8 ;
//! gate S-G2). Il ne sait pas écrire : produire un lot d'exemple est le travail
//! de `cargo xtask emettre-exemple`, pas le sien.
//!
//! Fail-closed (ADR-0010, point 5) : tout octet muté, tronqué, en trop ou non
//! canonique donne un code de sortie non nul et une **erreur nommée**.
//!
//! # Ce fichier est `std`, et c'est sa définition
//!
//! ADR-0009 point 6 contracte `#![no_std]` + `alloc` en gate à S3, et ADR-0015
//! point 6 la maintient telle quelle. La logique du vérificateur est donc
//! passée en bibliothèque `no_std` (`src/lib.rs`) et ce fichier en est la
//! **coquille mince** : il ne garde que ce que `core` et `alloc` ne peuvent pas
//! faire — `std::fs`, `std::env`, `std::process::exit`, l'impression. Aucune
//! décision ne se prend ici ; toutes se lisent dans la bibliothèque, et se
//! construisent pour une cible sans bibliothèque standard.
//!
//! # Les deux formes de lot, et les deux entrées de contexte
//!
//! Un lot est soit le **témoignage trivial** du squelette (12 §5), soit le
//! **témoignage canonique** des sept champs de 03 §1. Le cœur trie sur les
//! octets ; ce binaire n'ajoute aucune heuristique.
//!
//! Sur un témoignage canonique, 03 §4 exige trois contrôles, dont deux ont
//! besoin d'une donnée que le lot ne peut pas porter lui-même — un lot fourni
//! par un tiers ne peut pas être son propre témoin :
//!
//! * `--registre <fichier>` : le **registre publié** des identifiants de résidus
//!   (`docs/08-assumptions.md`). Il entre en argument et non en constante :
//!   ces identifiants nomment des mécanismes d'attestation, et ce binaire n'en
//!   nomme aucun (ADR-0001, gate S-G1).
//! * `--constat <fichier>` : ce que le **binaire compagnon** d'ADR-0015 point 7
//!   déclare avoir vérifié et consommé. Le contrôle cryptographique de la preuve
//!   de transport est exécuté par lui, **jamais par ce binaire**, et le verdict
//!   le dit en toutes lettres (ADR-0015, point 8 alinéa e).
//!
//! **La forme de ces deux entrées est une décision d'implémentation** : ADR-0015
//! fixe *ce* qui doit être contrôlé, pas l'interface par laquelle le contexte
//! arrive. Deux fichiers texte, lus en clair, recalculables à la main : c'est le
//! choix le plus contrôlable par un tiers, et il est remonté comme tel.

use shogen_core::{Constat, Verdict, empreinte_en_hexadecimal};
use shogen_verifier::{
    Examen, OPTION_CONSTAT, OPTION_REGISTRE, analyser_constat, analyser_registre, examiner_lot,
    examiner_verification, tete_hexadecimale,
};

/// Lot conforme au sous-ensemble canonique.
const CODE_CONFORME: i32 = 0;
/// Usage : arguments mal formés.
const CODE_USAGE: i32 = 64;
/// Un fichier de contexte est illisible ou mal formé.
const CODE_CONTEXTE: i32 = 65;
/// Le fichier de lot n'a pas pu être lu.
const CODE_LECTURE: i32 = 66;
/// Le décodage a refusé le lot (erreur nommée du cœur).
const CODE_DECODAGE: i32 = 2;
/// Le lot décode, mais son ré-encodage diffère : il n'était pas canonique.
const CODE_ROUND_TRIP: i32 = 3;
/// Le lot est canonique, mais un contrôle de 03 §4 a refusé.
const CODE_VERIFICATION: i32 = 4;

/// Verdict et résidu, en toutes lettres. La conformité est une propriété des
/// **octets**, pas du monde : ADR-0001 (Shōgen ne construit aucun transport et
/// ne juge pas la vérité d'une source).
const VERDICT_CONFORME: &str = "VERDICT : octets conformes au sous-ensemble canonique ; résidu : la conformité ne dit rien de la vérité de la source — ADR-0001";

/// Le code de sortie est **rendu**, jamais imposé par `std::process::exit`.
///
/// # Pourquoi, et ce que le contournement coûtait (mesuré le 2026-08-13)
///
/// `std::process::exit` termine le processus **sans dérouler la sortie
/// normale** du programme. Conséquence mesurée, et cause de la dette
/// « couverture vérificateur NON mesurée » du JOURNAL : sous
/// `-Cinstrument-coverage`, le binaire créait bien son fichier de profil mais
/// n'y écrivait **rien** — `verif-39584.profraw`, **0 octet**, `llvm-profdata
/// show` : « empty raw profile file ». Les compteurs n'étaient jamais vidés,
/// donc `cargo llvm-cov` rapportait **0,00 %** sur `main.rs` et `lib.rs` alors
/// que dix tests de bout en bout exerçaient le binaire. La couverture n'était
/// pas basse : elle n'était pas mesurable, ce qui est pire, parce que 0,00 %
/// se lit comme un fait alors que c'est un défaut d'instrument.
///
/// `ExitCode` rend le contrôle à la sortie normale : les compteurs sont vidés,
/// le profil est écrit, et le code de sortie est celui que `executer` a
/// choisi. Aucun code de sortie ne change — la table `CODE_*` est intacte, et
/// les tests de bout en bout qui les assèrent le vérifient.
fn main() -> std::process::ExitCode {
    std::process::ExitCode::from(octet_de_sortie(executer()))
}

/// Réduit un code de sortie à l'octet que le système d'exploitation transporte.
///
/// Tous les codes de ce binaire tiennent dans un `u8` (0, 2, 3, 4, 64, 65, 66)
/// et la conversion est donc exacte. Le bras d'échec n'est pas mort pour
/// autant : il rend un code futur hors plage visible à l'exécution (refus
/// imprimé, sortie 64) plutôt qu'un modulo 256 silencieux — rien ne
/// l'établit à la compilation. Un verdict tronqué qui se lirait comme un
/// autre verdict serait exactement la faute qu'un vérificateur fail-closed
/// ne peut pas commettre (ADR-0010 point 5).
fn octet_de_sortie(code: i32) -> u8 {
    match u8::try_from(code) {
        Ok(octet) => octet,
        Err(_) => {
            eprintln!(
                "  erreur nommée : code de sortie {code} hors de la plage transportable — refus plutôt que troncature silencieuse"
            );
            CODE_USAGE_OCTET
        }
    }
}

/// La valeur de repli de [`octet_de_sortie`], égale à [`CODE_USAGE`].
const CODE_USAGE_OCTET: u8 = 64;

/// Les arguments reconnus.
struct Arguments {
    lot: std::ffi::OsString,
    registre: Option<std::ffi::OsString>,
    constat: Option<std::ffi::OsString>,
}

fn executer() -> i32 {
    let arguments = match lire_arguments() {
        Ok(arguments) => arguments,
        Err(erreur) => {
            eprintln!(
                "usage : shogen-verifier <chemin-du-lot> [{OPTION_REGISTRE} <fichier>] [{OPTION_CONSTAT} <fichier>]"
            );
            eprintln!("  vérifie qu'un lot est un témoignage en forme canonique.");
            eprintln!("  {erreur}");
            return CODE_USAGE;
        }
    };

    let affichage = arguments.lot.to_string_lossy().into_owned();
    let octets = match std::fs::read(&arguments.lot) {
        Ok(octets) => octets,
        Err(erreur) => {
            eprintln!("VERDICT : refusé (fail-closed)");
            eprintln!("  erreur nommée : lot illisible « {affichage} » : {erreur}");
            return CODE_LECTURE;
        }
    };

    println!("shogen-verifier — lot : {affichage}");
    println!("  octets lus : {}", octets.len());
    println!("  tête du lot : {}", tete_hexadecimale(&octets));

    match examiner_lot(&octets) {
        Examen::Refuse(erreur) => {
            eprintln!("VERDICT : refusé (fail-closed)");
            eprintln!("  erreur nommée : {erreur}");
            eprintln!("  variante : {erreur:?}");
            CODE_DECODAGE
        }
        Examen::NonCanonique {
            octets_du_lot,
            octets_reencodes,
            divergence,
        } => {
            eprintln!("VERDICT : refusé (fail-closed)");
            eprintln!(
                "  erreur nommée : ré-encodage divergent — le lot décode mais n'est pas sa propre forme canonique"
            );
            eprintln!("    octets du lot     : {octets_du_lot}");
            eprintln!("    octets ré-encodés : {octets_reencodes}");
            eprintln!("    première divergence : {divergence}");
            CODE_ROUND_TRIP
        }
        Examen::Trivial {
            temoignage,
            octets_reencodes,
        } => {
            imprimer_decodage(octets_reencodes);
            // Substitution de forme (revue G2 de phase C, autour de F8) : un
            // appelant qui fournit --registre/--constat demande les contrôles
            // de 03 §4 — un lot trivial n'en porte aucun. Sortir en 0 en
            // ignorant ces options serait un déclassement silencieux ; on
            // refuse. Sans ces options, la forme triviale reste le contrat
            // du walking skeleton (conformité seule, dite comme telle).
            if arguments.registre.is_some() || arguments.constat.is_some() {
                eprintln!("VERDICT : refusé (fail-closed)");
                eprintln!(
                    "  erreur nommée : options de vérification fournies sur une forme triviale — ce lot ne porte ni preuve, ni résidu, ni attestateur : rien de ce que --registre/--constat contrôlent"
                );
                return CODE_CONTEXTE;
            }
            println!("  forme : témoignage trivial du walking skeleton (12 §5)");
            println!("  source : « {} »", temoignage.source);
            println!(
                "  instant porté : {} (donnée du lot, aucune horloge lue)",
                temoignage.instant
            );
            println!("  contenu : {} octet(s)", temoignage.contenu.len());
            println!("{VERDICT_CONFORME}");
            CODE_CONFORME
        }
        Examen::Canonique {
            temoignage,
            octets_reencodes,
        } => {
            imprimer_decodage(octets_reencodes);
            verifier_le_temoignage(&temoignage, &arguments)
        }
    }
}

/// La ligne de décodage, commune aux deux formes de lot acceptées.
fn imprimer_decodage(octets_reencodes: usize) {
    println!("  décodage : accepté (sous-ensemble canonique CBOR, RFC 8949 — ADR-0002)");
    println!("  ré-encodage : {octets_reencodes} octets, identiques au lot (round-trip exact)");
}

/// Les trois contrôles de 03 §4 sur un témoignage canonique.
fn verifier_le_temoignage(temoignage: &shogen_core::Temoignage, arguments: &Arguments) -> i32 {
    println!("  forme : témoignage canonique — les sept champs de 03 §1");
    println!("  subject : « {} »", temoignage.subject);
    println!(
        "  transport porté : « {} » (identifiant du lot, jamais une constante de ce binaire)",
        temoignage.transport
    );
    println!(
        "  observé à : {} selon l'horloge « {} » (donnée du lot, aucune horloge lue)",
        temoignage.observed_at.instant, temoignage.observed_at.clock
    );
    println!(
        "  empreinte d'utterance : {}",
        empreinte_en_hexadecimal(&temoignage.utterance.hash)
    );
    println!(
        "  preuve de transport : {} octet(s), opaques — ce binaire n'en interprète aucun",
        temoignage.transport_proof.len()
    );
    for attestor in temoignage.attestor.iter() {
        println!(
            "  attestateur : « {} », clé épinglée de {} octet(s)",
            attestor.identity,
            attestor.key.len()
        );
    }

    let registre = match arguments.registre.as_ref() {
        Some(chemin) => match lire_registre(chemin) {
            Ok(registre) => registre,
            Err(erreur) => {
                eprintln!("VERDICT : refusé (fail-closed)");
                eprintln!("  erreur nommée : {erreur}");
                return CODE_CONTEXTE;
            }
        },
        None => Vec::new(),
    };
    let constat = match arguments.constat.as_ref() {
        Some(chemin) => match lire_constat(chemin) {
            Ok(constat) => Some(constat),
            Err(erreur) => {
                eprintln!("VERDICT : refusé (fail-closed)");
                eprintln!("  erreur nommée : {erreur}");
                return CODE_CONTEXTE;
            }
        },
        None => None,
    };

    match examiner_verification(temoignage, &registre, constat.as_ref()) {
        Ok(verdict) => {
            imprimer_verdict(&verdict, temoignage);
            CODE_CONFORME
        }
        Err(erreur) => {
            eprintln!("VERDICT : refusé (fail-closed)");
            eprintln!("  erreur nommée : {erreur}");
            eprintln!("  variante : {erreur:?}");
            CODE_VERIFICATION
        }
    }
}

/// Le verdict : ce qui a été établi, **sous quoi**, et ce qui ne l'a pas été ici.
///
/// # Pourquoi la phrase de délégation nomme le transport et une révision, et
/// pas un binaire
///
/// ADR-0015 point 8 alinéa e **propose** une chaîne où le binaire compagnon est
/// nommé : « … a été exécuté par <le nom du compagnon> [révision amont], jamais
/// par ce binaire ». Deux faits du dépôt, mesurés, empêchent ce binaire d'écrire
/// ce nom-là dans ses sources :
///
/// * la gate **S-G1** interdit tout nom de transport dans le cœur et dans le
///   vérificateur (ADR-0001), et le nom du compagnon en porte un — la gate l'a
///   d'ailleurs prouvé en refusant une première rédaction de ce paragraphe qui
///   le citait ;
/// * le **contrat du constat** (ADR-0015 point 13) fige dix-huit clés dont
///   aucune ne porte le nom du binaire compagnon — seule `revision_amont` y
///   est, et « toute évolution passe par incrément de `version_du_constat` ».
///
/// La phrase nomme donc ce que les **données** portent : l'identifiant de
/// transport du témoignage (`transport`, une donnée du lot, jamais une
/// constante d'ici) et la révision amont, verbatim, du constat. Elle dit la
/// même chose que l'alinéa e — qui a fait le contrôle, et que ce binaire ne
/// l'a pas fait. **Cette rédaction est celle du registre** : ADR-0015 point 18
/// amende l'alinéa (e) à ce que les données permettent, et rejette
/// explicitement les deux autres voies (excepter la gate S-G1 ; ajouter une clé
/// de nom d'outil au constat). L'écart n'est plus un écart.
///
/// # Ce que la phrase ajoute depuis la vague 2
///
/// ADR-0015 point 17 bis (adjudication R-26) : la désignation complète de
/// `subject` — chemin et requête — n'est liée par aucun contrôle recalculable ;
/// seul l'hôte l'est, par l'alinéa (h). La limite **s'affiche** dans la même
/// phrase que le reste, parce qu'un verdict qui tairait ce qu'il ne couvre pas
/// serait lu comme s'il le couvrait.
fn imprimer_verdict(verdict: &Verdict, temoignage: &shogen_core::Temoignage) {
    if verdict.octets_recalcules {
        println!(
            "  liaison d'utterance : empreinte recalculée sur les octets portés (ADR-0005 règle 1)"
        );
    } else {
        println!(
            "  liaison d'utterance : octets non portés (politique de classe, ADR-0005 règle 2) — l'empreinte n'a pas été recalculée ici"
        );
    }
    let mut residus = String::new();
    for residu in verdict.residus.iter() {
        if !residus.is_empty() {
            residus.push_str(", ");
        }
        residus.push_str(residu);
    }
    println!("VERDICT : valide sous {residus}");
    println!(
        "  ce que ce verdict NE dit pas : le contrôle cryptographique de la preuve de transport a été exécuté par le binaire compagnon du transport « {} » à la révision amont {}, jamais par ce binaire ; la désignation complète de subject — chemin et requête — n'est liée par aucun contrôle recalculable ici, seul son hôte l'est (ADR-0015 point 17 bis, unité S4 « liaison de la désignation ») ; et la conformité ne dit rien de la vérité de la source — ADR-0001, ADR-0015",
        temoignage.transport, verdict.revision_amont_deleguee
    );
}

fn lire_arguments() -> Result<Arguments, String> {
    let mut restants = std::env::args_os().skip(1);
    let mut lot: Option<std::ffi::OsString> = None;
    let mut registre: Option<std::ffi::OsString> = None;
    let mut constat: Option<std::ffi::OsString> = None;

    while let Some(argument) = restants.next() {
        let rendu = argument.to_string_lossy().into_owned();
        if rendu == OPTION_REGISTRE {
            if registre.is_some() {
                return Err(format!("option « {OPTION_REGISTRE} » donnée deux fois"));
            }
            registre = Some(valeur_d_option(&mut restants, OPTION_REGISTRE)?);
        } else if rendu == OPTION_CONSTAT {
            if constat.is_some() {
                return Err(format!("option « {OPTION_CONSTAT} » donnée deux fois"));
            }
            constat = Some(valeur_d_option(&mut restants, OPTION_CONSTAT)?);
        } else if rendu.starts_with("--") {
            return Err(format!("option inconnue : « {rendu} »"));
        } else if lot.is_some() {
            return Err(String::from("un seul lot à la fois"));
        } else {
            lot = Some(argument);
        }
    }

    match lot {
        Some(lot) => Ok(Arguments {
            lot,
            registre,
            constat,
        }),
        None => Err(String::from("aucun lot donné")),
    }
}

fn valeur_d_option(
    restants: &mut impl Iterator<Item = std::ffi::OsString>,
    option: &str,
) -> Result<std::ffi::OsString, String> {
    match restants.next() {
        Some(valeur) => Ok(valeur),
        None => Err(format!("l'option « {option} » attend un chemin")),
    }
}

/// Lit le registre publié, puis le fait analyser par la bibliothèque.
///
/// La coupure est à l'endroit exact où l'I/O s'arrête : ce qui reste ici est la
/// lecture du fichier et la ligne imprimée ; l'analyse est `no_std`.
fn lire_registre(chemin: &std::ffi::OsString) -> Result<Vec<String>, String> {
    let texte = lire_texte(chemin, "registre")?;
    let identifiants = analyser_registre(&texte)?;
    println!("  registre publié : {} identifiant(s)", identifiants.len());
    Ok(identifiants)
}

/// Lit le constat du binaire compagnon, puis le fait analyser par la
/// bibliothèque.
///
/// Le refus de l'analyseur est **typé** (`ErreurConstat`) ; il est rendu en
/// texte ici, au dernier moment, parce que c'est ici que l'impression a lieu.
fn lire_constat(chemin: &std::ffi::OsString) -> Result<Constat, String> {
    let texte = lire_texte(chemin, "constat")?;
    match analyser_constat(&texte) {
        Ok(constat) => Ok(constat),
        Err(erreur) => Err(format!("{erreur}\n  variante : {erreur:?}")),
    }
}

fn lire_texte(chemin: &std::ffi::OsString, quoi: &str) -> Result<String, String> {
    let affichage = chemin.to_string_lossy().into_owned();
    match std::fs::read_to_string(chemin) {
        Ok(texte) => Ok(texte),
        Err(erreur) => Err(format!("{quoi} illisible « {affichage} » : {erreur}")),
    }
}
