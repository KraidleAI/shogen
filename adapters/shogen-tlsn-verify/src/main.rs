//! `shogen-tlsn-verify` — le compagnon de vérification du transport `tlsn-mpc/1`.
//!
//! Rattachement (G0) : **ADR-0015 pt 7** (le binaire compagnon, hors workspace,
//! amont épinglé par révision git exacte, exécute
//! `Presentation::verify(&CryptoProvider)` et imprime un résultat structuré) ;
//! **ADR-0015 pt 8** et son amendement du 2026-08-13, contrôles (b), (c), (f),
//! (g) ; **ADR-0005 règle 1** (le hash des octets exacts lie le témoignage à sa
//! preuve de transport) ; **ADR-0001** (les transports sont des adapters —
//! testés, jamais prouvés).
//!
//! Ce que ce binaire **est** : l'exécutant du contrôle cryptographique que
//! `shogen-verifier` ne fait pas et déclare ne pas faire (09-vocabulaire, entrée
//! « transport vérifié par shogen-verifier »). Ce qu'il **n'est pas** : une
//! partie de l'artefact de confiance du projet. Il est remplaçable ; son constat
//! est ce qui compte, et le vérificateur le recoupe champ par champ.
//!
//! ## Le constat
//!
//! Une ligne JSON, **clés triées par ordre d'octets croissant**, écrite sur la
//! sortie standard. La forme est stable : c'est elle que `shogen-verifier`
//! consommera. Un succès est la seule sortie qui porte `"verdict"` ;
//! un échec porte `"erreur"` et **rien d'autre du constat** — jamais un constat
//! partiel muet (ADR-0015 pt 7, fail-closed).
//!
//! ## Régime d'assurance
//!
//! *tested*, jamais *proven*. Rien ici n'établit la soundness du protocole
//! MPC-TLS amont, ni la neutralité du notaire — A(notary-neutrality),
//! A(self-attestation), A(transport-check-delegated) et A(upstream-alpha)
//! restent au registre 08.

use std::io::Write as _;

use sha2::{Digest as _, Sha256};
use tlsn_attestation::{CryptoProvider, presentation::Presentation};

/// La révision amont contre laquelle ce compagnon est construit.
///
/// Cette constante doit être **identique** à la `rev` du manifeste et à la
/// source du `Cargo.lock` ; le contrôle est mécanique (voir `fixtures/NOTES.md`,
/// section « révision amont »). Elle entre dans le constat parce qu'ADR-0015
/// pt 8 (e) exige que le verdict du vérificateur nomme la révision du
/// compagnon qui a exécuté le contrôle cryptographique.
const REVISION_AMONT: &str = "0fe3c32d35382b3f290a43c4156399ca4512bb89";

/// Version de la forme du constat. Un changement de forme change ce nombre :
/// un consommateur qui ne le reconnaît pas refuse, il ne devine pas.
const VERSION_DU_CONSTAT: u32 = 1;

/// Codes de sortie. Zéro n'est rendu que par un constat complet.
mod code {
    /// Vérification conduite, constat complet imprimé.
    pub const SUCCES: i32 = 0;
    /// Usage : arguments de ligne de commande inutilisables.
    pub const USAGE: i32 = 64;
    /// Le fichier de présentation n'a pas pu être lu.
    pub const LECTURE: i32 = 65;
    /// Les octets ne décodent pas en `Presentation`.
    pub const DECODAGE: i32 = 66;
    /// `Presentation::verify` a refusé.
    pub const VERIFICATION: i32 = 67;
    /// La vérification a réussi mais le constat exigible ne peut pas être
    /// formé (pas de nom de serveur, pas de transcript, octets non
    /// authentifiés là où le contrôle (b) exige des octets authentifiés).
    pub const CONSTAT_INCOMPLET: i32 = 68;
    /// L'écriture d'un fichier demandé par option a échoué.
    pub const ECRITURE: i32 = 69;
}

fn main() {
    let arguments: Vec<String> = std::env::args().skip(1).collect();
    match executer(&arguments) {
        Ok(constat) => {
            println!("{constat}");
            std::process::exit(code::SUCCES);
        }
        Err(echec) => {
            // L'échec s'écrit sur la sortie d'erreur ET porte un code non nul.
            // Il est structuré comme le succès : un consommateur lit la même
            // forme dans les deux cas.
            eprintln!("{}", echec.en_json());
            std::process::exit(echec.code);
        }
    }
}

/// Un échec nommé : jamais un message nu, jamais un constat partiel.
struct Echec {
    code: i32,
    raison: &'static str,
    detail: String,
}

impl Echec {
    fn nouveau(code: i32, raison: &'static str, detail: impl Into<String>) -> Self {
        Self {
            code,
            raison,
            detail: detail.into(),
        }
    }

    fn en_json(&self) -> String {
        // Clés triées : code, detail, erreur, revision_amont, version_du_constat.
        format!(
            "{{\"code\":{},\"detail\":{},\"erreur\":{},\"revision_amont\":{},\"version_du_constat\":{}}}",
            self.code,
            json_chaine(&self.detail),
            json_chaine(self.raison),
            json_chaine(REVISION_AMONT),
            VERSION_DU_CONSTAT
        )
    }
}

/// Options de ligne de commande, tenues à la main : aucune dépendance
/// d'analyse d'arguments n'entre dans un adapter dont la fermeture est mesurée.
struct Options {
    presentation: String,
    ecrire_recv: Option<String>,
    ecrire_sent: Option<String>,
}

fn lire_options(arguments: &[String]) -> Result<Options, Echec> {
    const USAGE: &str = "usage : shogen-tlsn-verify <presentation.tlsn> \
         [--ecrire-recv <fichier>] [--ecrire-sent <fichier>]";

    let mut presentation: Option<String> = None;
    let mut ecrire_recv: Option<String> = None;
    let mut ecrire_sent: Option<String> = None;

    let mut index = 0usize;
    while index < arguments.len() {
        let argument = arguments[index].as_str();
        match argument {
            "--ecrire-recv" | "--ecrire-sent" => {
                let Some(valeur) = arguments.get(index + 1) else {
                    return Err(Echec::nouveau(
                        code::USAGE,
                        "option_sans_valeur",
                        format!("{argument} attend un chemin. {USAGE}"),
                    ));
                };
                if argument == "--ecrire-recv" {
                    ecrire_recv = Some(valeur.clone());
                } else {
                    ecrire_sent = Some(valeur.clone());
                }
                index += 2;
            }
            autre if autre.starts_with("--") => {
                return Err(Echec::nouveau(
                    code::USAGE,
                    "option_inconnue",
                    format!("option inconnue : {autre}. {USAGE}"),
                ));
            }
            autre => {
                if presentation.is_some() {
                    return Err(Echec::nouveau(
                        code::USAGE,
                        "argument_surnumeraire",
                        format!("argument en trop : {autre}. {USAGE}"),
                    ));
                }
                presentation = Some(autre.to_string());
                index += 1;
            }
        }
    }

    let Some(presentation) = presentation else {
        return Err(Echec::nouveau(
            code::USAGE,
            "presentation_absente",
            USAGE.to_string(),
        ));
    };

    Ok(Options {
        presentation,
        ecrire_recv,
        ecrire_sent,
    })
}

fn executer(arguments: &[String]) -> Result<String, Echec> {
    let options = lire_options(arguments)?;

    // (c) — les octets consommés sont hachés AVANT tout décodage, sur le tampon
    // exact qui sera décodé ensuite. C'est ce qui interdit qu'on vérifie une
    // preuve et qu'on en livre une autre (ADR-0015 pt 8 (c)).
    let octets_presentation = std::fs::read(&options.presentation).map_err(|erreur| {
        Echec::nouveau(
            code::LECTURE,
            "presentation_illisible",
            format!("{} : {erreur}", options.presentation),
        )
    })?;
    let empreinte_presentation = empreinte_hex(&octets_presentation);

    let presentation: Presentation =
        bincode::deserialize(&octets_presentation).map_err(|erreur| {
            Echec::nouveau(
                code::DECODAGE,
                "presentation_indecodable",
                format!("bincode : {erreur}"),
            )
        })?;

    // (f) — l'identité de la clé est capturée AVANT la vérification, sur l'objet
    // même qui va être vérifié : c'est donc bien la clé contre laquelle la
    // vérification cryptographique est conduite, et non une clé rapportée à
    // côté. `verify` consomme la présentation ; l'ordre est contraint.
    let clef = presentation.verifying_key();
    let algorithme_de_clef = clef.alg.to_string();
    let clef_hex = en_hexadecimal(&clef.data);

    let sortie = presentation
        .verify(&CryptoProvider::default())
        .map_err(|erreur| {
            Echec::nouveau(
                code::VERIFICATION,
                "verification_refusee",
                format!("{erreur}"),
            )
        })?;

    let Some(nom_de_serveur) = sortie.server_name else {
        return Err(Echec::nouveau(
            code::CONSTAT_INCOMPLET,
            "nom_de_serveur_absent",
            "la présentation ne porte pas de preuve d'identité de serveur : \
             le constat exigible par ADR-0015 pt 7 ne peut pas être formé",
        ));
    };

    let Some(transcript) = sortie.transcript else {
        return Err(Echec::nouveau(
            code::CONSTAT_INCOMPLET,
            "transcript_absent",
            "la présentation ne révèle aucun octet de transcript : \
             le contrôle (b) d'ADR-0015 pt 8 n'a rien à lier",
        ));
    };

    let octets_recus = transcript.received_unsafe();
    let octets_envoyes = transcript.sent_unsafe();
    let recus_authentifies = transcript.received_authed().len();
    let envoyes_authentifies = transcript.sent_authed().len();

    // (b) — le hash porte les octets RÉVÉLÉS de la réponse. Si un seul octet
    // reçu n'est pas authentifié, `received_unsafe()` contient du remplissage
    // non authentifié : hacher ce tampon produirait une empreinte qui ne lie
    // rien. On refuse, on ne hache pas autour.
    if recus_authentifies != octets_recus.len() {
        return Err(Echec::nouveau(
            code::CONSTAT_INCOMPLET,
            "octets_recus_non_authentifies",
            format!(
                "{} octets reçus sur {} sont authentifiés : le contrôle (b) exige \
                 la totalité des octets reçus, sans remplissage",
                recus_authentifies,
                octets_recus.len()
            ),
        ));
    }

    let empreinte_recus = empreinte_hex(octets_recus);
    let empreinte_envoyes = empreinte_hex(octets_envoyes);

    if let Some(chemin) = &options.ecrire_recv {
        ecrire(chemin, octets_recus)?;
    }
    if let Some(chemin) = &options.ecrire_sent {
        ecrire(chemin, octets_envoyes)?;
    }

    let information = &sortie.connection_info;
    let version_tls = format!("{:?}", information.version);

    // Clés triées par ordre d'octets croissant. La forme est le contrat.
    let mut constat = String::new();
    constat.push('{');
    pousser_chaine(&mut constat, "attestor_cle_algorithme", &algorithme_de_clef);
    constat.push(',');
    pousser_chaine(&mut constat, "attestor_cle_hex", &clef_hex);
    constat.push(',');
    pousser_nombre(&mut constat, "connection_info_time", information.time);
    constat.push(',');
    pousser_chaine(&mut constat, "connection_info_version_tls", &version_tls);
    constat.push(',');
    pousser_chaine(
        &mut constat,
        "empreinte_presentation_sha256",
        &empreinte_presentation,
    );
    constat.push(',');
    pousser_chaine(
        &mut constat,
        "empreinte_recv_revele_sha256",
        &empreinte_recus,
    );
    constat.push(',');
    pousser_chaine(
        &mut constat,
        "empreinte_sent_revele_sha256",
        &empreinte_envoyes,
    );
    constat.push(',');
    pousser_nombre(
        &mut constat,
        "octets_presentation",
        octets_presentation.len() as u64,
    );
    constat.push(',');
    pousser_chaine(&mut constat, "revision_amont", REVISION_AMONT);
    constat.push(',');
    pousser_chaine(&mut constat, "server_name", &nom_de_serveur.to_string());
    constat.push(',');
    pousser_nombre(
        &mut constat,
        "transcript_recv_authentifie",
        recus_authentifies as u64,
    );
    constat.push(',');
    pousser_nombre(
        &mut constat,
        "transcript_recv_longueur",
        octets_recus.len() as u64,
    );
    constat.push(',');
    pousser_nombre(
        &mut constat,
        "transcript_recv_longueur_attestee",
        u64::from(information.transcript_length.received),
    );
    constat.push(',');
    pousser_nombre(
        &mut constat,
        "transcript_sent_authentifie",
        envoyes_authentifies as u64,
    );
    constat.push(',');
    pousser_nombre(
        &mut constat,
        "transcript_sent_longueur",
        octets_envoyes.len() as u64,
    );
    constat.push(',');
    pousser_nombre(
        &mut constat,
        "transcript_sent_longueur_attestee",
        u64::from(information.transcript_length.sent),
    );
    constat.push(',');
    pousser_chaine(&mut constat, "verdict", "presentation_verifiee");
    constat.push(',');
    pousser_nombre(
        &mut constat,
        "version_du_constat",
        u64::from(VERSION_DU_CONSTAT),
    );
    constat.push('}');

    Ok(constat)
}

fn ecrire(chemin: &str, octets: &[u8]) -> Result<(), Echec> {
    let mut fichier = std::fs::File::create(chemin).map_err(|erreur| {
        Echec::nouveau(
            code::ECRITURE,
            "fichier_non_creable",
            format!("{chemin} : {erreur}"),
        )
    })?;
    fichier.write_all(octets).map_err(|erreur| {
        Echec::nouveau(
            code::ECRITURE,
            "ecriture_echouee",
            format!("{chemin} : {erreur}"),
        )
    })
}

fn empreinte_hex(octets: &[u8]) -> String {
    let mut hacheur = Sha256::new();
    hacheur.update(octets);
    en_hexadecimal(&hacheur.finalize())
}

fn en_hexadecimal(octets: &[u8]) -> String {
    const CHIFFRES: &[u8; 16] = b"0123456789abcdef";
    let mut sortie = String::with_capacity(octets.len() * 2);
    for octet in octets {
        sortie.push(CHIFFRES[usize::from(octet >> 4)] as char);
        sortie.push(CHIFFRES[usize::from(octet & 0x0f)] as char);
    }
    sortie
}

/// Échappement JSON (RFC 8259 §7) tenu à la main : les guillemets, la barre
/// oblique inverse, et tout point de code de contrôle sous U+0020.
fn json_chaine(valeur: &str) -> String {
    let mut sortie = String::with_capacity(valeur.len() + 2);
    sortie.push('"');
    for caractere in valeur.chars() {
        match caractere {
            '"' => sortie.push_str("\\\""),
            '\\' => sortie.push_str("\\\\"),
            '\n' => sortie.push_str("\\n"),
            '\r' => sortie.push_str("\\r"),
            '\t' => sortie.push_str("\\t"),
            c if (c as u32) < 0x20 => {
                sortie.push_str(&format!("\\u{:04x}", c as u32));
            }
            c => sortie.push(c),
        }
    }
    sortie.push('"');
    sortie
}

fn pousser_chaine(sortie: &mut String, clef: &str, valeur: &str) {
    sortie.push_str(&json_chaine(clef));
    sortie.push(':');
    sortie.push_str(&json_chaine(valeur));
}

fn pousser_nombre(sortie: &mut String, clef: &str, valeur: u64) {
    sortie.push_str(&json_chaine(clef));
    sortie.push(':');
    sortie.push_str(&valeur.to_string());
}
