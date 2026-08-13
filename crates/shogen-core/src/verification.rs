//! Les contrôles du vérificateur, **purs** — ce qu'un tiers recalcule hors ligne.
//!
//! Rattachement (G0) : **03 §4** (ce qu'un vérificateur offline vérifie sur un
//! témoignage isolé) ; **ADR-0015 point 8**, qui en fixe la forme exacte pour
//! S3 — (a) le lot décode et se ré-encode à l'octet près (acquis S2.5, tenu par
//! `lot.rs`), (b) l'empreinte d'`utterance` égale celle des octets révélés
//! rapportés par le binaire compagnon, (c) l'empreinte des octets de
//! `transport_proof` égale celle que le compagnon déclare avoir consommée,
//! (d) `residual` résout dans le registre publié, (e) **le verdict nomme la
//! délégation** ; **ADR-0005 règle 1** (le hash lie le témoignage à sa preuve) ;
//! **ADR-0010** (pur, total, sans I/O — le registre et le constat entrent en
//! **arguments**, jamais par un fichier lu d'ici).
//!
//! **Ce que ce module ne fait pas, et le dit** : il ne vérifie aucune preuve de
//! transport. Le contrôle cryptographique est exécuté ailleurs, par le binaire
//! compagnon d'ADR-0015 point 7, et le verdict le déclare — c'est le résidu
//! `A(transport-check-delegated)`. Un verdict d'ici ne dit jamais « vrai » : il
//! dit « conforme **sous** les hypothèses nommées » (03 §4).
//!
//! **Pourquoi le registre est un argument et non une constante.** Les
//! identifiants de résidus nomment des mécanismes de transport ; les inscrire au
//! cœur ferait de `shogen-core` un module qui nomme un transport — exactement ce
//! qu'ADR-0001 interdit et que la gate S-G1 attrape. Le registre publié
//! (`docs/08-assumptions.md`) entre donc en **donnée**, comme l'horodatage.

use crate::empreinte::{OCTETS_D_EMPREINTE, empreinte_en_hexadecimal, empreinte_sha256};
use crate::temoignage_canonique::Temoignage;

/// L'identifiant du résidu que la **forme d'intégration** impose, quel que soit
/// le transport : le contrôle cryptographique n'a pas été exécuté par ce
/// binaire (ADR-0015, point 8 alinéa e).
pub const RESIDU_DE_LA_DELEGATION: &str = "A(transport-check-delegated)";

/// Ce que le binaire compagnon déclare avoir vérifié et consommé.
///
/// Structure **portée en argument** : le cœur ne lance aucun processus et ne lit
/// aucun fichier (ADR-0010, point 1). La coquille produit ce constat ; le cœur
/// s'en sert pour établir la liaison, et rien d'autre.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Constat {
    /// Identité du binaire compagnon et de sa révision amont, verbatim.
    pub outil: String,
    /// Empreinte des octets de preuve que le compagnon déclare avoir consommés.
    pub empreinte_de_la_preuve: [u8; OCTETS_D_EMPREINTE],
    /// Empreinte des octets révélés que le compagnon déclare avoir vérifiés.
    pub empreinte_de_l_utterance: [u8; OCTETS_D_EMPREINTE],
}

/// Le verdict — ce qui a été établi, et **sous quoi**.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Verdict {
    /// Les résidus nommés, dans l'ordre : ceux du témoignage, puis celui de la
    /// délégation. Jamais agrégés en un « niveau » unique (03 §2).
    pub residus: Vec<String>,
    /// L'identité du binaire qui a fait le contrôle **que celui-ci n'a pas
    /// fait**.
    pub outil_delegue: String,
    /// Vrai si les octets d'`utterance` étaient portés et que leur empreinte a
    /// été **recalculée** ici ; faux si le témoignage ne porte que le hash
    /// (ADR-0005 règle 2 : la rétention est une politique de classe).
    pub octets_recalcules: bool,
}

/// Refus de vérification. Comme `ErreurDecodage`, chaque variante dit **quoi**,
/// et porte les valeurs qui l'ont produite : un refus se diagnostique sans
/// journal (le cœur ne journalise pas).
#[derive(Debug, Clone, PartialEq, Eq)]
#[non_exhaustive]
pub enum ErreurVerification {
    /// Aucun constat du compagnon : la liaison n'est pas établissable, donc le
    /// verdict est le refus (ADR-0010, point 5).
    ConstatAbsent,
    /// Registre des résidus vide : rien ne pourrait y résoudre, et un registre
    /// absent qui laisserait passer serait la faute exacte que S-G1 et
    /// *fail-safe defaults* existent à empêcher.
    RegistreVide,
    /// Les octets portés ne redonnent pas l'empreinte portée.
    LiaisonUtteranceRompue {
        portee: [u8; OCTETS_D_EMPREINTE],
        calculee: [u8; OCTETS_D_EMPREINTE],
    },
    /// L'empreinte portée n'est pas celle des octets révélés au compagnon.
    UtteranceNonConstatee {
        portee: [u8; OCTETS_D_EMPREINTE],
        constatee: [u8; OCTETS_D_EMPREINTE],
    },
    /// Les octets de preuve du lot ne sont pas ceux que le compagnon a
    /// consommés — c'est ce qui interdit de vérifier une preuve et d'en livrer
    /// une autre (ADR-0015, point 8 alinéa c).
    PreuveNonConstatee {
        calculee: [u8; OCTETS_D_EMPREINTE],
        constatee: [u8; OCTETS_D_EMPREINTE],
    },
    /// Un résidu ne résout pas dans le registre publié.
    ResiduNonResolu { residu: String },
}

impl core::fmt::Display for ErreurVerification {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        match self {
            Self::ConstatAbsent => write!(
                f,
                "constat du binaire compagnon absent : la liaison du témoignage à sa preuve n'est pas établissable, le verdict est le refus"
            ),
            Self::RegistreVide => write!(
                f,
                "registre des résidus vide : aucun identifiant ne pourrait y résoudre"
            ),
            Self::LiaisonUtteranceRompue { portee, calculee } => write!(
                f,
                "liaison d'utterance rompue : empreinte portée {}, empreinte des octets portés {}",
                empreinte_en_hexadecimal(portee),
                empreinte_en_hexadecimal(calculee)
            ),
            Self::UtteranceNonConstatee { portee, constatee } => write!(
                f,
                "utterance non constatée : empreinte portée {}, empreinte constatée par le compagnon {}",
                empreinte_en_hexadecimal(portee),
                empreinte_en_hexadecimal(constatee)
            ),
            Self::PreuveNonConstatee {
                calculee,
                constatee,
            } => write!(
                f,
                "preuve non constatée : empreinte des octets du lot {}, empreinte constatée par le compagnon {}",
                empreinte_en_hexadecimal(calculee),
                empreinte_en_hexadecimal(constatee)
            ),
            Self::ResiduNonResolu { residu } => write!(
                f,
                "résidu non résolu : « {residu} » ne figure pas au registre publié"
            ),
        }
    }
}

impl std::error::Error for ErreurVerification {}

/// Les contrôles (b), (c) et (d) d'ADR-0015 point 8, dans cet ordre.
///
/// **Totale** : aucune entrée ne la fait diverger. **Pure** : le registre et le
/// constat sont des arguments ; deux exécutions sur les mêmes arguments rendent
/// le même verdict, sur toute machine (ADR-0003).
///
/// L'ordre des contrôles est une décision : la liaison interne au témoignage
/// d'abord (elle ne dépend d'aucun tiers), la liaison au compagnon ensuite, la
/// résolution du registre en dernier — du plus recalculable au plus délégué.
pub fn verifier_temoignage(
    temoignage: &Temoignage,
    registre: &[String],
    constat: Option<&Constat>,
) -> Result<Verdict, ErreurVerification> {
    if registre.is_empty() {
        return Err(ErreurVerification::RegistreVide);
    }
    let constat = match constat {
        Some(constat) => constat,
        None => return Err(ErreurVerification::ConstatAbsent),
    };

    // (b1) — les octets portés redonnent l'empreinte portée. ADR-0005 règle 1 :
    // « le hash des octets exacts est toujours porté ». Quand les octets sont là
    // aussi, la liaison est recalculable **entièrement** ici.
    let octets_recalcules = match temoignage.utterance.bytes.as_ref() {
        Some(octets) => {
            let calculee = empreinte_sha256(octets);
            if calculee != temoignage.utterance.hash {
                return Err(ErreurVerification::LiaisonUtteranceRompue {
                    portee: temoignage.utterance.hash,
                    calculee,
                });
            }
            true
        }
        None => false,
    };

    // (b2) — l'empreinte portée est celle des octets révélés au compagnon.
    if temoignage.utterance.hash != constat.empreinte_de_l_utterance {
        return Err(ErreurVerification::UtteranceNonConstatee {
            portee: temoignage.utterance.hash,
            constatee: constat.empreinte_de_l_utterance,
        });
    }

    // (c) — les octets de preuve du lot sont ceux qui ont été vérifiés.
    let empreinte_de_la_preuve = empreinte_sha256(&temoignage.transport_proof);
    if empreinte_de_la_preuve != constat.empreinte_de_la_preuve {
        return Err(ErreurVerification::PreuveNonConstatee {
            calculee: empreinte_de_la_preuve,
            constatee: constat.empreinte_de_la_preuve,
        });
    }

    // (d) — chaque résidu résout, celui de la délégation compris : un registre
    // qui n'enregistre pas la délégation n'est pas le registre publié.
    let mut residus: Vec<String> = Vec::new();
    for residu in temoignage.residual.iter() {
        resoudre(residu, registre)?;
        residus.push(residu.clone());
    }
    resoudre(RESIDU_DE_LA_DELEGATION, registre)?;
    residus.push(String::from(RESIDU_DE_LA_DELEGATION));

    Ok(Verdict {
        residus,
        outil_delegue: constat.outil.clone(),
        octets_recalcules,
    })
}

/// Résolution d'un identifiant dans le registre publié — égalité d'octets, la
/// comparaison la moins chère et la seule qui ne demande à croire personne.
fn resoudre(residu: &str, registre: &[String]) -> Result<(), ErreurVerification> {
    if registre.iter().any(|entree| entree == residu) {
        return Ok(());
    }
    Err(ErreurVerification::ResiduNonResolu {
        residu: residu.to_owned(),
    })
}
