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
//! Ce qu'il fait, et rien de plus : lit des fichiers d'octets, les passe au
//! cœur, ré-encode, compare — puis **nomme son résidu**. Il ne réclame aucune
//! capacité qu'il n'exerce : ni réseau, ni horloge, ni aléa (ADR-0010, point 8 ;
//! gate S-G2). Il ne sait pas écrire : produire un lot d'exemple est le travail
//! de `cargo xtask emettre-exemple`, pas le sien.
//!
//! Fail-closed (ADR-0010, point 5) : tout octet muté, tronqué, en trop ou non
//! canonique donne un code de sortie non nul et une **erreur nommée**.
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

use shogen_core::{
    Constat, Lot, OCTETS_D_EMPREINTE, Temoignage, Verdict, decoder_lot, empreinte_en_hexadecimal,
    encoder_lot, verifier_temoignage,
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

/// L'option du registre publié des résidus.
const OPTION_REGISTRE: &str = "--registre";
/// L'option du constat du binaire compagnon.
const OPTION_CONSTAT: &str = "--constat";

/// Les clés du fichier de constat.
const CLE_OUTIL: &str = "outil";
const CLE_EMPREINTE_PREUVE: &str = "empreinte-preuve";
const CLE_EMPREINTE_UTTERANCE: &str = "empreinte-utterance";

fn main() {
    std::process::exit(executer());
}

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

    let lot = match decoder_lot(&octets) {
        Ok(lot) => lot,
        Err(erreur) => {
            eprintln!("VERDICT : refusé (fail-closed)");
            eprintln!("  erreur nommée : {erreur}");
            eprintln!("  variante : {erreur:?}");
            return CODE_DECODAGE;
        }
    };

    let reencode = encoder_lot(&lot);
    if reencode.as_slice() != octets.as_slice() {
        eprintln!("VERDICT : refusé (fail-closed)");
        eprintln!(
            "  erreur nommée : ré-encodage divergent — le lot décode mais n'est pas sa propre forme canonique"
        );
        eprintln!("    octets du lot     : {}", octets.len());
        eprintln!("    octets ré-encodés : {}", reencode.len());
        eprintln!(
            "    première divergence : {}",
            premiere_divergence(&octets, &reencode)
        );
        return CODE_ROUND_TRIP;
    }

    println!("  décodage : accepté (sous-ensemble canonique CBOR, RFC 8949 — ADR-0002)");
    println!(
        "  ré-encodage : {} octets, identiques au lot (round-trip exact)",
        reencode.len()
    );

    match lot {
        Lot::Trivial(temoignage) => {
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
        Lot::Canonique(temoignage) => verifier_le_temoignage(&temoignage, &arguments),
    }
}

/// Les trois contrôles de 03 §4 sur un témoignage canonique.
fn verifier_le_temoignage(temoignage: &Temoignage, arguments: &Arguments) -> i32 {
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

    match verifier_temoignage(temoignage, &registre, constat.as_ref()) {
        Ok(verdict) => {
            imprimer_verdict(&verdict);
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
fn imprimer_verdict(verdict: &Verdict) {
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
        "  ce que ce verdict NE dit pas : le contrôle cryptographique de la preuve de transport a été exécuté par « {} », jamais par ce binaire ; et la conformité ne dit rien de la vérité de la source — ADR-0001, ADR-0015",
        verdict.outil_delegue
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

/// Le registre publié : un identifiant par ligne, `#` pour les commentaires.
///
/// Format volontairement pauvre : il doit se relire à l'œil et se recalculer à
/// la main depuis `docs/08-assumptions.md` (ADR-0003 : recalculable offline).
fn lire_registre(chemin: &std::ffi::OsString) -> Result<Vec<String>, String> {
    let texte = lire_texte(chemin, "registre")?;
    let mut identifiants: Vec<String> = Vec::new();
    for ligne in texte.lines() {
        let ligne = ligne.trim();
        if ligne.is_empty() || ligne.starts_with('#') {
            continue;
        }
        if identifiants.iter().any(|deja| deja == ligne) {
            return Err(format!(
                "registre mal formé : « {ligne} » figure deux fois — un registre à doublons n'est pas un registre"
            ));
        }
        identifiants.push(String::from(ligne));
    }
    println!("  registre publié : {} identifiant(s)", identifiants.len());
    Ok(identifiants)
}

/// Le constat du binaire compagnon : trois clés, une par ligne.
fn lire_constat(chemin: &std::ffi::OsString) -> Result<Constat, String> {
    let texte = lire_texte(chemin, "constat")?;
    let mut outil: Option<String> = None;
    let mut empreinte_de_la_preuve: Option<[u8; OCTETS_D_EMPREINTE]> = None;
    let mut empreinte_de_l_utterance: Option<[u8; OCTETS_D_EMPREINTE]> = None;

    for ligne in texte.lines() {
        let ligne = ligne.trim();
        if ligne.is_empty() || ligne.starts_with('#') {
            continue;
        }
        let Some((cle, valeur)) = ligne.split_once('=') else {
            return Err(format!(
                "constat mal formé : ligne sans « = » — « {ligne} »"
            ));
        };
        let cle = cle.trim();
        let valeur = valeur.trim();
        // Clé répétée : refus nommé, jamais « la dernière l'emporte » (revue
        // G2 de phase C, trouvaille F7 — démontrée : l'ordre des lignes
        // changeait le verdict). Même argument que le registre : un constat
        // à doublons n'est pas un constat.
        if cle == CLE_OUTIL {
            if outil.is_some() {
                return Err(format!("constat mal formé : clé répétée « {cle} »"));
            }
            outil = Some(String::from(valeur));
        } else if cle == CLE_EMPREINTE_PREUVE {
            if empreinte_de_la_preuve.is_some() {
                return Err(format!("constat mal formé : clé répétée « {cle} »"));
            }
            empreinte_de_la_preuve = Some(empreinte_depuis_hexadecimal(valeur, cle)?);
        } else if cle == CLE_EMPREINTE_UTTERANCE {
            if empreinte_de_l_utterance.is_some() {
                return Err(format!("constat mal formé : clé répétée « {cle} »"));
            }
            empreinte_de_l_utterance = Some(empreinte_depuis_hexadecimal(valeur, cle)?);
        } else {
            return Err(format!("constat mal formé : clé inconnue « {cle} »"));
        }
    }

    let outil = exiger(outil, CLE_OUTIL)?;
    if outil.is_empty() {
        return Err(String::from(
            "constat mal formé : « outil » vide — un contrôle délégué se nomme, sinon la délégation ne se vérifie pas",
        ));
    }
    Ok(Constat {
        outil,
        empreinte_de_la_preuve: exiger(empreinte_de_la_preuve, CLE_EMPREINTE_PREUVE)?,
        empreinte_de_l_utterance: exiger(empreinte_de_l_utterance, CLE_EMPREINTE_UTTERANCE)?,
    })
}

fn exiger<T>(valeur: Option<T>, cle: &str) -> Result<T, String> {
    match valeur {
        Some(valeur) => Ok(valeur),
        None => Err(format!("constat mal formé : clé « {cle} » absente")),
    }
}

fn lire_texte(chemin: &std::ffi::OsString, quoi: &str) -> Result<String, String> {
    let affichage = chemin.to_string_lossy().into_owned();
    match std::fs::read_to_string(chemin) {
        Ok(texte) => Ok(texte),
        Err(erreur) => Err(format!("{quoi} illisible « {affichage} » : {erreur}")),
    }
}

/// Une empreinte en hexadécimal : exactement 64 chiffres, aucune tolérance.
fn empreinte_depuis_hexadecimal(
    texte: &str,
    cle: &str,
) -> Result<[u8; OCTETS_D_EMPREINTE], String> {
    let octets = texte.as_bytes();
    let mut valeurs: Vec<u8> = Vec::new();
    for paire in octets.chunks_exact(2) {
        let mut valeur: u8 = 0;
        let mut complet = true;
        for chiffre in paire.iter().copied() {
            match valeur_hexadecimale(chiffre) {
                Some(quartet) => valeur = valeur.wrapping_shl(4) | quartet,
                None => complet = false,
            }
        }
        if !complet {
            return Err(format!(
                "constat mal formé : « {cle} » n'est pas de l'hexadécimal"
            ));
        }
        valeurs.push(valeur);
    }
    if !octets.chunks_exact(2).remainder().is_empty() {
        return Err(format!(
            "constat mal formé : « {cle} » a un nombre impair de chiffres"
        ));
    }
    match <[u8; OCTETS_D_EMPREINTE]>::try_from(valeurs.as_slice()) {
        Ok(empreinte) => Ok(empreinte),
        Err(_) => Err(format!(
            "constat mal formé : « {cle} » fait {} octet(s), {OCTETS_D_EMPREINTE} attendus",
            valeurs.len()
        )),
    }
}

fn valeur_hexadecimale(octet: u8) -> Option<u8> {
    match octet {
        b'0'..=b'9' => Some(octet.wrapping_sub(b'0')),
        b'A'..=b'F' => Some(octet.wrapping_sub(b'A').wrapping_add(10)),
        b'a'..=b'f' => Some(octet.wrapping_sub(b'a').wrapping_add(10)),
        _ => None,
    }
}

/// Rend les premiers octets en hexadécimal, pour qu'un refus soit
/// diagnosticable sans outil tiers.
fn tete_hexadecimale(octets: &[u8]) -> String {
    let mut rendu = String::new();
    for octet in octets.iter().copied().take(16) {
        rendu.push_str(&format!("{octet:02x}"));
    }
    if octets.len() > 16 {
        rendu.push('…');
    }
    rendu
}

/// Position du premier octet divergent, ou une mention de longueur.
fn premiere_divergence(gauche: &[u8], droite: &[u8]) -> String {
    let position = gauche
        .iter()
        .copied()
        .zip(droite.iter().copied())
        .position(|(a, b)| a != b);
    match position {
        Some(position) => format!("octet {position}"),
        None => String::from("aucune sur le préfixe commun — les longueurs diffèrent"),
    }
}
