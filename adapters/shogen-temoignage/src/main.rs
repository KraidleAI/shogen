#![forbid(unsafe_code)]
//! `shogen-temoignage` — la coquille : lit les artefacts déposés d'une session
//! attestée, écrit **un lot** en forme canonique.
//!
//! Usage :
//!
//! ```text
//! shogen-temoignage <répertoire-des-artefacts> <préfixe> <lot-de-sortie>
//! ```
//!
//! Les artefacts attendus sous `<répertoire>`, au nom que le compagnon leur
//! donne (`adapters/shogen-tlsn-verify/fixtures/NOTES.md` §1) :
//!
//! * `<préfixe>.sent-revele.bin` — les octets émis, d'où vient `subject` ;
//! * `<préfixe>.recv-revele.bin` — les octets reçus, qui **sont** l'`utterance` ;
//! * `<préfixe>.presentation.tlsn` — les octets de preuve, opaques ;
//! * `<préfixe>.constat.json` — le constat du binaire compagnon (ADR-0015
//!   point 13).
//!
//! Fail-closed : tout recoupement rompu est un code de sortie non nul et un
//! refus nommé sur la sortie d'erreur. Ce binaire n'ouvre aucune connexion : il
//! lit des fichiers et en écrit un.

use std::path::{Path, PathBuf};

/// Le transport de S3 (ADR-0015 point 1 — la valeur déjà écrite en 03 §2).
const TRANSPORT: &str = "tlsn-mpc/1";
/// L'identité de l'attestateur : Shōgen lui-même, et cela se dit
/// (ADR-0015 point 4 — A(self-attestation), rendue matérielle au point 16).
const IDENTITE_DE_L_ATTESTATEUR: &str = "shogen:attestateur-de-demonstration-s3";
/// L'horloge qui a daté — celle du transport, jamais celle de Shōgen (03 §1).
const HORLOGE: &str = "tlsn-mpc/1:connection_info.time";
/// Les résidus du transport, **dans l'ordre émis** (03 §2, ligne `tlsn-mpc`,
/// pour la durée de S3). Le résidu de la forme d'intégration
/// (`A(transport-check-delegated)`) n'est PAS ici : le vérificateur l'ajoute
/// lui-même au verdict (ADR-0015 point 8 alinéa e), et l'écrire deux fois le
/// ferait nommer deux fois.
const RESIDUS: &[&str] = &["A(notary-neutrality)", "A(self-attestation)"];

fn main() -> std::process::ExitCode {
    match executer() {
        Ok(rendu) => {
            println!("{rendu}");
            std::process::ExitCode::SUCCESS
        }
        Err(erreur) => {
            eprintln!("REFUS (fail-closed) : {erreur}");
            std::process::ExitCode::from(65)
        }
    }
}

fn executer() -> Result<String, String> {
    let mut arguments = std::env::args_os().skip(1);
    let (Some(repertoire), Some(prefixe), Some(sortie), None) = (
        arguments.next(),
        arguments.next(),
        arguments.next(),
        arguments.next(),
    ) else {
        return Err(String::from(
            "usage : shogen-temoignage <répertoire-des-artefacts> <préfixe> <lot-de-sortie>",
        ));
    };
    let repertoire = PathBuf::from(repertoire);
    let prefixe = prefixe.to_string_lossy().into_owned();
    let sortie = PathBuf::from(sortie);

    let octets_emis = lire(&repertoire, &format!("{prefixe}.sent-revele.bin"))?;
    let octets_recus = lire(&repertoire, &format!("{prefixe}.recv-revele.bin"))?;
    let octets_de_preuve = lire(&repertoire, &format!("{prefixe}.presentation.tlsn"))?;
    let texte_du_constat = lire_texte(&repertoire, &format!("{prefixe}.constat.json"))?;
    let ligne_de_cle = lire_texte(
        &repertoire,
        &format!("{prefixe}.attestor-verifying-key.txt"),
    )?;

    let entrees = shogen_temoignage::Entrees {
        octets_emis: &octets_emis,
        octets_recus: &octets_recus,
        octets_de_preuve: &octets_de_preuve,
        texte_du_constat: &texte_du_constat,
        transport: TRANSPORT,
        identite_de_l_attestateur: IDENTITE_DE_L_ATTESTATEUR,
        horloge: HORLOGE,
        residus: RESIDUS,
    };
    let temoignage =
        shogen_temoignage::construire(&entrees).map_err(|erreur| erreur.to_string())?;

    // Recoupement de plus, propre à la coquille : la clé épinglée composée
    // depuis le constat est la ligne que le compagnon a déposée à côté de la
    // présentation. Deux pièces, une seule clé.
    let composee = shogen_temoignage::cle_epinglee_du_constat(&texte_du_constat)
        .map_err(|erreur| erreur.to_string())?;
    let deposee = ligne_de_cle.trim();
    if composee != deposee {
        return Err(format!(
            "recoupement rompu (clé épinglée) : composée depuis le constat « {composee} », déposée par le compagnon « {deposee} »"
        ));
    }

    let octets =
        shogen_core::encoder_lot(&shogen_core::Lot::Canonique(Box::new(temoignage.clone())));
    // Contrôle (a) au rang du constructeur : ce qui vient d'être écrit se
    // relit et se ré-encode à l'octet près. Un lot qu'aucun décodeur ne
    // reprend n'est pas un lot.
    match shogen_core::decoder_lot(&octets) {
        Ok(relu) => {
            if shogen_core::encoder_lot(&relu) != octets {
                return Err(String::from(
                    "le lot écrit ne se ré-encode pas à l'octet près : la forme canonique n'est pas tenue",
                ));
            }
        }
        Err(erreur) => {
            return Err(format!("le lot écrit ne se relit pas : {erreur}"));
        }
    }

    std::fs::write(&sortie, &octets)
        .map_err(|erreur| format!("écriture impossible ({}) : {erreur}", sortie.display()))?;

    Ok(format!(
        "lot canonique écrit : {}\n  octets            : {}\n  subject           : {}\n  transport         : {}\n  observé à         : {} (horloge « {} »)\n  utterance         : {} octet(s) portés\n  preuve            : {} octet(s), opaques\n  clé épinglée      : {}\n  résidus portés    : {}",
        sortie.display(),
        octets.len(),
        temoignage.subject,
        temoignage.transport,
        temoignage.observed_at.instant,
        temoignage.observed_at.clock,
        temoignage
            .utterance
            .bytes
            .as_ref()
            .map(Vec::len)
            .unwrap_or_default(),
        temoignage.transport_proof.len(),
        composee,
        RESIDUS.join(", ")
    ))
}

fn lire(repertoire: &Path, nom: &str) -> Result<Vec<u8>, String> {
    let chemin = repertoire.join(nom);
    std::fs::read(&chemin).map_err(|erreur| format!("lecture impossible ({nom}) : {erreur}"))
}

fn lire_texte(repertoire: &Path, nom: &str) -> Result<String, String> {
    let chemin = repertoire.join(nom);
    std::fs::read_to_string(&chemin)
        .map_err(|erreur| format!("lecture impossible ({nom}) : {erreur}"))
}
