#![no_std]
#![forbid(unsafe_code)]
#![deny(
    clippy::unwrap_used,
    clippy::expect_used,
    clippy::panic,
    clippy::indexing_slicing,
    clippy::arithmetic_side_effects
)]
//! La **logique** du vérificateur offline, sans I/O — `#![no_std]` + `alloc`.
//!
//! # Pourquoi ce module existe (G0)
//!
//! ADR-0009 point 6 : « `#![no_std]` + `alloc` devient une gate en S3 ».
//! ADR-0015 point 6 la maintient telle quelle — « elle n'est ni repositionnée
//! ni reportée ». Or le binaire `shogen-verifier` lit des fichiers, lit des
//! arguments et sort avec un code : trois capacités que `core` n'a pas et que
//! `alloc` ne rend pas. Un binaire entièrement `no_std` ne serait pas le
//! vérificateur d'ADR-0010 point 4 (« I/O, lecture d'arguments : binaire CLI »).
//!
//! La forme retenue est donc la seule qui satisfasse les deux textes à la
//! lettre : **la logique en bibliothèque `no_std`, le binaire en coquille
//! `std` mince**. La coquille garde exactement ce que `core` ne peut pas
//! faire — `std::fs`, `std::env`, `std::process::exit`, l'impression — et rien
//! d'autre. Tout ce qui décide est ici, et se construit pour une cible sans
//! bibliothèque standard.
//!
//! Ce que cette scission **n'est pas** : une refonte. Aucune fonction n'est
//! réécrite, aucun message ne change, aucune signature publique du cœur n'est
//! touchée. Les fonctions déplacées sont celles qui étaient déjà pures dans
//! `main.rs` ; celles qui imprimaient ont été coupées en deux à l'endroit exact
//! où l'impression commençait.
//!
//! # Le point d'entrée qui consomme des octets
//!
//! [`eprouver`] est la cible que consomme un fuzzer (ADR-0011 seuil 7 : « zéro
//! panique sur toute suite d'octets »). Elle est **totale** et **sans I/O** :
//! elle prend une suite d'octets quelconque et la soumet aux trois surfaces
//! d'octets du vérificateur — le lot, le registre, le constat — puis jette les
//! résultats. Ce qu'elle établit, si elle ne panique jamais sur un corpus :
//! *tested* sur ce corpus, avec son compte. Jamais *proven* : l'absence de
//! panique n'est pas établie (ADR-0010, §Coûts point 6).
//!
//! `catch_unwind` n'est **pas** ici : c'est une capacité `std`, elle appartient
//! au harnais, pas à la logique.

extern crate alloc;

use alloc::boxed::Box;
use alloc::format;
use alloc::string::String;
use alloc::vec::Vec;

use shogen_core::{
    Constat, ErreurDecodage, ErreurVerification, Lot, OCTETS_D_EMPREINTE, Temoignage,
    TemoignageTrivial, Verdict, decoder_lot, encoder_lot, verifier_temoignage,
};

/// L'option du registre publié des résidus.
pub const OPTION_REGISTRE: &str = "--registre";
/// L'option du constat du binaire compagnon.
pub const OPTION_CONSTAT: &str = "--constat";

/// Les clés du fichier de constat.
pub const CLE_OUTIL: &str = "outil";
/// Clé de l'empreinte de la preuve de transport.
pub const CLE_EMPREINTE_PREUVE: &str = "empreinte-preuve";
/// Clé de l'empreinte de l'utterance.
pub const CLE_EMPREINTE_UTTERANCE: &str = "empreinte-utterance";

/// Ce que le vérificateur a établi sur une suite d'octets, avant toute
/// impression et avant tout code de sortie.
///
/// Le tri est celui des octets, jamais une heuristique : c'est le cœur qui
/// classe (ADR-0010 point 3).
///
/// Volontairement **exhaustif** — pas de `#[non_exhaustive]`, à rebours des
/// erreurs du cœur. Motif : la coquille du binaire est une crate distincte de
/// cette bibliothèque, et `#[non_exhaustive]` l'obligerait à porter un bras
/// `_` — c'est-à-dire un comportement par défaut sur une variante que
/// personne n'a écrite. ADR-0010 point 5 (*fail-safe defaults*) l'interdit :
/// une variante nouvelle doit casser la compilation de la coquille, pas y
/// tomber dans un fourre-tout.
#[derive(Debug)]
pub enum Examen {
    /// Le cœur a refusé les octets — erreur nommée.
    Refuse(ErreurDecodage),
    /// Le lot décode mais son ré-encodage diffère : il n'était pas canonique.
    NonCanonique {
        /// Octets du lot fourni.
        octets_du_lot: usize,
        /// Octets du ré-encodage.
        octets_reencodes: usize,
        /// Position du premier octet divergent, ou mention de longueur.
        divergence: String,
    },
    /// Témoignage trivial du walking skeleton (12 §5), ré-encodage exact.
    Trivial {
        /// Le témoignage décodé.
        temoignage: Box<TemoignageTrivial>,
        /// Longueur du ré-encodage, identique au lot.
        octets_reencodes: usize,
    },
    /// Témoignage canonique des sept champs de 03 §1, ré-encodage exact.
    Canonique {
        /// Le témoignage décodé.
        temoignage: Box<Temoignage>,
        /// Longueur du ré-encodage, identique au lot.
        octets_reencodes: usize,
    },
}

/// Décode, ré-encode et compare : les deux premiers des trois contrôles que le
/// binaire exerce sur un lot, sans rien imprimer.
///
/// Tolérante au sens de Meyer : aucune précondition, tout `&[u8]` y compris
/// hostile (carte des points de frontière, `shogen_core`).
pub fn examiner_lot(octets: &[u8]) -> Examen {
    let lot = match decoder_lot(octets) {
        Ok(lot) => lot,
        Err(erreur) => return Examen::Refuse(erreur),
    };
    let reencode = encoder_lot(&lot);
    if reencode.as_slice() != octets {
        return Examen::NonCanonique {
            octets_du_lot: octets.len(),
            octets_reencodes: reencode.len(),
            divergence: premiere_divergence(octets, &reencode),
        };
    }
    let octets_reencodes = reencode.len();
    match lot {
        Lot::Trivial(temoignage) => Examen::Trivial {
            temoignage: Box::new(temoignage),
            octets_reencodes,
        },
        // `Lot::Canonique` porte déjà son `Box` (le cœur boxe la grande
        // variante pour ne pas gonfler l'enum) : on le transporte tel quel.
        Lot::Canonique(temoignage) => Examen::Canonique {
            temoignage,
            octets_reencodes,
        },
    }
}

/// Le troisième contrôle : les trois exigences de 03 §4 sur un témoignage
/// canonique déjà décodé.
///
/// Exigeante au sens de Meyer : la précondition — le témoignage est canonique —
/// est établie par le décodage, qui est la frontière. Ce n'est qu'un renvoi au
/// cœur ; il est ici pour que la coquille n'ait aucune décision à prendre.
pub fn examiner_verification(
    temoignage: &Temoignage,
    registre: &[String],
    constat: Option<&Constat>,
) -> Result<Verdict, ErreurVerification> {
    verifier_temoignage(temoignage, registre, constat)
}

/// Le registre publié : un identifiant par ligne, `#` pour les commentaires.
///
/// Format volontairement pauvre : il doit se relire à l'œil et se recalculer à
/// la main depuis `docs/08-assumptions.md` (ADR-0003 : recalculable offline).
pub fn analyser_registre(texte: &str) -> Result<Vec<String>, String> {
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
    Ok(identifiants)
}

/// Le constat du binaire compagnon : trois clés, une par ligne.
pub fn analyser_constat(texte: &str) -> Result<Constat, String> {
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

/// Une empreinte en hexadécimal : exactement 64 chiffres, aucune tolérance.
pub fn empreinte_depuis_hexadecimal(
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
pub fn tete_hexadecimale(octets: &[u8]) -> String {
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
pub fn premiere_divergence(gauche: &[u8], droite: &[u8]) -> String {
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

/// **La cible fuzz** — ADR-0011 seuil 7 : « zéro panique sur toute suite
/// d'octets ».
///
/// Une seule suite d'octets, soumise aux **trois** surfaces d'octets du
/// vérificateur : le lot (binaire), le registre (texte) et le constat (texte).
/// Les mêmes octets jouent les trois rôles — c'est ce qui rend un corpus de
/// graines exploitable par n'importe quel moteur, et c'est pourquoi la fonction
/// ne rend rien : elle existe pour ne pas diverger.
///
/// Totale et sans I/O : elle ne lit aucun fichier, n'imprime rien, ne sort
/// pas du processus. Ce que son passage établit sur un corpus est *tested*
/// avec son compte, jamais *proven*.
pub fn eprouver(octets: &[u8]) {
    // Surface 1 — le lot, sur les octets bruts.
    let examen = examiner_lot(octets);

    // Surfaces 2 et 3 — le registre et le constat, sur les mêmes octets lus
    // comme du texte. Des octets non-UTF-8 ne sont pas un échec de l'épreuve :
    // la coquille lit ces fichiers en texte, un contenu non-UTF-8 y est refusé
    // avant d'atteindre ces fonctions. L'épreuve reproduit ce partage.
    let (registre, constat) = match core::str::from_utf8(octets) {
        Ok(texte) => (
            analyser_registre(texte).unwrap_or_default(),
            analyser_constat(texte).ok(),
        ),
        Err(_) => (Vec::new(), None),
    };

    // Surface 1 bis — la vérification de 03 §4, alimentée par les surfaces 2
    // et 3. C'est le seul chemin qui exerce ensemble les trois contrôles.
    if let Examen::Canonique { temoignage, .. } = examen {
        let _ = examiner_verification(&temoignage, &registre, constat.as_ref());
    }
}
