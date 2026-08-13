//! Les contrôles du vérificateur, **purs** — ce qu'un tiers recalcule hors ligne.
//!
//! Rattachement (G0) : **03 §4** (ce qu'un vérificateur offline vérifie sur un
//! témoignage isolé) ; **ADR-0015 point 8**, qui en fixe la forme exacte pour
//! S3 — (a) le lot décode et se ré-encode à l'octet près (acquis S2.5, tenu par
//! `lot.rs`), (b) l'empreinte d'`utterance` égale celle des octets révélés
//! rapportés par le binaire compagnon, (c) l'empreinte des octets de
//! `transport_proof` égale celle que le compagnon déclare avoir consommée,
//! (d) `residual` résout dans le registre publié, (e) **le verdict nomme la
//! délégation** — **plus l'amendement du 2026-08-13** : (f) la clé épinglée
//! d'`attestor` égale celle contre laquelle le contrôle délégué a été conduit,
//! (g) `observed_at` égale l'instant de connexion que le constat rapporte,
//! **(h)** l'hôte de `subject` égale l'identité de serveur authentifiée que le
//! constat rapporte ; **ADR-0005 règle 1** (le hash lie le témoignage à sa
//! preuve) ; **ADR-0010** (pur, total, sans I/O — le registre et le constat
//! entrent en **arguments**, jamais par un fichier lu d'ici).
//!
//! **L'alinéa (h) — le recoupement d'origine.** ADR-0015 point 13 assignait à
//! la clé `server_name` du constat le rôle de « recoupement d'origine de
//! `subject` (ADR-0016) » sans que le point 8 n'en porte la lettre. Le contrôle
//! est **ratifié alinéa (h)** par ADR-0015 point 17 (amendement du 2026-08-13,
//! vague 2) : l'hôte de `subject` — extraction par découpe, jamais réécriture
//! (ADR-0016 C0, [`hote_de_subject`]) — doit égaler l'identité de serveur
//! authentifiée. Il est isolé dans un contrôle et une variante d'erreur uniques
//! (`OrigineNonConstatee`), et ne peut produire qu'un refus, jamais une
//! acceptation. Sans lui, l'hôte du `subject` n'est lié à rien : un lot
//! désignant une autre origine passerait (b), (c), (f) et (g).
//!
//! **Ce que (h) NE ferme PAS, et qui s'affiche** (ADR-0015 point 17 bis,
//! mesuré) : (h) recoupe l'**hôte**. Le chemin et la requête de `subject` — la
//! ressource désignée — ne sont liés par aucun contrôle recalculable en S3 ; un
//! lot dont la requête est altérée en ASCII à longueur égale est accepté. La
//! limite est affichée par la phrase de verdict de la coquille, énumérée par le
//! balayage de `crates/shogen-verifier/tests/temoignage_canonique.rs`, et son
//! traitement est l'unité S4 « liaison de la désignation ». Elle n'est jamais
//! niée ici.
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

use alloc::borrow::ToOwned;
use alloc::string::String;
use alloc::vec::Vec;

use crate::empreinte::{OCTETS_D_EMPREINTE, empreinte_en_hexadecimal, empreinte_sha256};
use crate::subject::hote_de_subject;
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
///
/// **C'est une projection, pas le constat entier.** Le contrat d'ADR-0015
/// point 13 fige dix-huit clés ; celles qui n'entrent dans aucun contrôle
/// (version de la couche de transport, taille de la preuve, les six longueurs)
/// sont **contrôlées à l'analyse** — leur absence ou leur type faux est un
/// refus — puis ne franchissent pas cette frontière.
///
/// **Une exception, nommée** : `empreinte_du_sens_emis` traverse sans qu'aucun
/// contrôle ne la consomme. C'est l'adjudication d'ADR-0015 point 17 bis — la
/// donnée qui fermerait la désignation non liée existe au constat, et elle est
/// portée jusqu'ici au lieu d'être jetée, en attendant l'unité S4 qui l'emploie.
/// Le champ le dit dans sa propre documentation ; il n'est pas silencieux.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Constat {
    /// La révision amont du binaire compagnon, **verbatim** — elle entre telle
    /// quelle dans la chaîne de verdict (ADR-0015, point 8 alinéa e).
    pub revision_amont: String,
    /// La clé de vérification contre laquelle le contrôle délégué a été conduit,
    /// **octets opaques** au cœur (contrôle (f), amendement du 2026-08-13).
    ///
    /// La convention d'écriture de ces octets — algorithme, séparateur, chiffres
    /// — appartient à l'adapter qui construit le témoignage et à l'analyseur qui
    /// lit le constat ; le cœur ne fait qu'une **égalité d'octets**, la seule
    /// comparaison qui ne demande à croire personne (ADR-0001 : le cœur ne nomme
    /// aucun algorithme de transport).
    pub cle_du_controle: Vec<u8>,
    /// L'instant de connexion rapporté par le constat (contrôle (g)).
    pub instant_de_connexion: u64,
    /// L'identité de serveur authentifiée que le constat rapporte — recoupée
    /// avec l'hôte de `subject` par l'alinéa **(h)** (ADR-0015 point 8 alinéa
    /// (h), ratifié au point 17).
    pub origine_authentifiee: String,
    /// Empreinte des octets de preuve que le compagnon déclare avoir consommés.
    pub empreinte_de_la_preuve: [u8; OCTETS_D_EMPREINTE],
    /// Empreinte des octets révélés que le compagnon déclare avoir vérifiés.
    pub empreinte_de_l_utterance: [u8; OCTETS_D_EMPREINTE],
    /// Empreinte des octets du **sens émis** que le compagnon déclare avoir
    /// vérifiés — la donnée qui fermerait le trou du point 17 bis.
    ///
    /// **Aucun contrôle de ce module ne la consomme aujourd'hui, et c'est dit
    /// plutôt que caché** (adjudication R-26, ADR-0015 point 17 bis) : le
    /// témoignage ne porte pas les octets du sens émis, donc rien ne peut y être
    /// recoupé sans une évolution de forme ratifiée — clé de contrat
    /// supplémentaire (option a) ou champ supplémentaire à 03 §1 (option b),
    /// l'une et l'autre du ressort du mainteneur, instruites à l'unité S4
    /// « liaison de la désignation ».
    ///
    /// Elle est **portée jusqu'ici** au lieu d'être jetée à l'analyse : une
    /// donnée que la coquille lit, contrôle, puis abandonne est une donnée que
    /// la passe suivante devra re-instruire. Elle voyage ; l'unité S4 la
    /// consommera.
    pub empreinte_du_sens_emis: [u8; OCTETS_D_EMPREINTE],
}

/// Le verdict — ce qui a été établi, et **sous quoi**.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Verdict {
    /// Les résidus nommés, dans l'ordre : ceux du témoignage, puis celui de la
    /// délégation. Jamais agrégés en un « niveau » unique (03 §2).
    pub residus: Vec<String>,
    /// La révision amont, **verbatim**, du binaire qui a fait le contrôle **que
    /// celui-ci n'a pas fait** (ADR-0015, point 8 alinéa e).
    pub revision_amont_deleguee: String,
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
    /// `attestor` est vide : (f) n'a rien à comparer, donc il serait **satisfait
    /// à vide** — une boucle sans tour rend `Ok` sans avoir rien établi.
    ///
    /// Le décodage refuse déjà le tableau vide (`entete_de_tableau`,
    /// `temoignage_canonique.rs`), mais un `Temoignage` n'arrive pas ici par le
    /// seul décodage : la structure est publique et un adapter la construit
    /// directement. Le geste est donc répété au rang qui conclut — *fail-safe
    /// defaults* (ADR-0010, point 5) : ce qui n'a pas été établi n'est pas admis.
    AttestorVide,
    /// La clé épinglée par le témoignage n'est pas celle contre laquelle le
    /// contrôle délégué a été conduit — sans quoi l'épinglage serait décoratif
    /// (ADR-0015, point 8, amendement du 2026-08-13, alinéa f).
    AttestorNonConstate { portee: Vec<u8>, constatee: Vec<u8> },
    /// L'instant porté n'est pas celui de la connexion constatée (alinéa g).
    InstantNonConstate { porte: u64, constate: u64 },
    /// L'hôte du `subject` n'est pas l'identité de serveur authentifiée que le
    /// constat rapporte — alinéa **(h)** (ADR-0015 point 8 alinéa (h), ratifié
    /// au point 17). Le seul effet possible de (h) : un refus.
    OrigineNonConstatee { portee: String, constatee: String },
    /// Un résidu ne résout pas dans le registre publié.
    ResiduNonResolu { residu: String },
}

/// Rend une clé épinglée lisible : son texte quand elle en est un, ses chiffres
/// hexadécimaux sinon.
///
/// La convention d'écriture appartient à l'adapter (voir [`Constat`]) ; ce rendu
/// n'en suppose aucune — il rend ce qui se lit, et se rabat sur les octets. Un
/// refus se diagnostique sans outil tiers (le cœur ne journalise pas).
fn rendu_de_cle(octets: &[u8]) -> String {
    match core::str::from_utf8(octets) {
        Ok(texte) if texte.is_ascii() => String::from(texte),
        _ => {
            let mut rendu = String::new();
            for octet in octets {
                rendu.push_str(&alloc::format!("{octet:02x}"));
            }
            rendu
        }
    }
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
            Self::AttestorVide => write!(
                f,
                "attestor vide : le contrôle de la clé épinglée n'aurait rien à comparer et serait satisfait à vide — un contrôle sans objet n'établit rien"
            ),
            Self::AttestorNonConstate { portee, constatee } => write!(
                f,
                "attestateur non constaté : clé épinglée par le témoignage « {} », clé du contrôle délégué « {} » — un épinglage que rien ne recoupe est décoratif",
                rendu_de_cle(portee),
                rendu_de_cle(constatee)
            ),
            Self::InstantNonConstate { porte, constate } => write!(
                f,
                "instant non constaté : instant porté {porte}, instant de connexion constaté {constate}"
            ),
            Self::OrigineNonConstatee { portee, constatee } => write!(
                f,
                "origine non constatée : hôte du subject « {portee} », origine authentifiée constatée « {constatee} »"
            ),
            Self::ResiduNonResolu { residu } => write!(
                f,
                "résidu non résolu : « {residu} » ne figure pas au registre publié"
            ),
        }
    }
}

impl core::error::Error for ErreurVerification {}

/// Les contrôles (b), (c), (f), (g), (h) et (d) d'ADR-0015 point 8, dans cet
/// ordre.
///
/// **Totale** : aucune entrée ne la fait diverger. **Pure** : le registre et le
/// constat sont des arguments ; deux exécutions sur les mêmes arguments rendent
/// le même verdict, sur toute machine (ADR-0003).
///
/// L'ordre des contrôles est une décision : la liaison interne au témoignage
/// d'abord (elle ne dépend d'aucun tiers), les liaisons au constat ensuite — les
/// deux empreintes, puis les deux charges que l'amendement du 2026-08-13 a
/// sorties du non-lié (la clé épinglée et l'instant), puis (h) —, la résolution
/// du registre en dernier : du plus recalculable au plus délégué.
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

    // (f) — la clé épinglée est celle contre laquelle le contrôle délégué a été
    // conduit. **Toutes** les entrées d'`attestor` sont soumises au contrôle :
    // un constat atteste UN contrôle, conduit contre UNE clé ; une entrée
    // épinglant autre chose serait exactement l'épinglage décoratif que
    // l'amendement du 2026-08-13 a mesuré. (Le multi-attestateur d'ADR-0004
    // n'est pas cette forme-là : il agrège k témoignages au-dessus, « jamais un
    // objet co-signé ».)
    //
    // Le tableau vide est refusé AVANT la boucle : sans ce refus, (f) serait
    // satisfait à vide — zéro tour, `Ok`, rien d'établi. Même geste
    // qu'`entete_de_tableau` au décodage, répété ici parce que ce rang conclut
    // et que la structure entre aussi par la construction (revue G2, vague 2).
    if temoignage.attestor.is_empty() {
        return Err(ErreurVerification::AttestorVide);
    }
    for attestor in temoignage.attestor.iter() {
        if attestor.key != constat.cle_du_controle {
            return Err(ErreurVerification::AttestorNonConstate {
                portee: attestor.key.clone(),
                constatee: constat.cle_du_controle.clone(),
            });
        }
    }

    // (g) — l'instant porté est celui de la connexion constatée. 03 §1 : ce rang
    // enregistre **qui a daté**, il ne date pas ; le contrôle ne compare donc
    // pas à une horloge, il compare deux données portées.
    if temoignage.observed_at.instant != constat.instant_de_connexion {
        return Err(ErreurVerification::InstantNonConstate {
            porte: temoignage.observed_at.instant,
            constate: constat.instant_de_connexion,
        });
    }

    // (h) — l'hôte de `subject` est l'identité de serveur authentifiée
    // (ADR-0015 point 8 alinéa (h), ratifié au point 17). Aucune normalisation :
    // `subject` est déjà en forme canonique (le décodage l'a établi,
    // ADR-0016 C10), l'hôte s'en extrait par découpe et la comparaison est une
    // égalité d'octets. Ce que (h) ne ferme pas — chemin et requête — est
    // affiché, jamais nié (point 17 bis, unité S4).
    let hote = hote_de_subject(&temoignage.subject);
    if hote != constat.origine_authentifiee {
        return Err(ErreurVerification::OrigineNonConstatee {
            portee: hote.to_owned(),
            constatee: constat.origine_authentifiee.clone(),
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
        revision_amont_deleguee: constat.revision_amont.clone(),
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
