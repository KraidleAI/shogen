//! La **forme canonique de témoignage** — les sept champs de `03-temoignage.md`
//! §1, en CBOR déterministe.
//!
//! Rattachement (G0) : **03 §1** (la table des sept champs, reprise ici sans
//! invention de vocabulaire : les clés CBOR sont les noms que la spécification
//! écrit) ; **ADR-0002** (Core Deterministic Encoding Requirements, RFC 8949) ;
//! **ADR-0005 règle 1** (le hash des octets exacts est toujours porté ; les
//! octets, eux, sont une politique de classe — d'où `bytes` facultatif) ;
//! **ADR-0010** (cœur pur, total, sans I/O, sans panique) ; **ADR-0015**
//! (`transport_proof` reste « opaque pour Shōgen » ; le contrôle
//! cryptographique est délégué) ; **ADR-0016 C10** (le prédicat de canonicité de
//! `subject` est branché **dans le décodage** : un témoignage à `subject` non
//! canonique est refusé, jamais réécrit).
//!
//! **Ce que la forme n'a pas**, et qu'aucune phrase ne doit laisser croire
//! (03 §0) : pas de champ vérité, pas de score de confiance, pas de
//! « validated ». Le cœur ne nomme aucun transport (ADR-0001, gate S-G1) : le
//! champ `transport` porte un identifiant **venu du lot**, jamais une constante
//! de ce code.
//!
//! **L'ordre des clés n'est pas une croyance** : il est le tri lexicographique
//! des clés *encodées* (RFC 8949), recalculé par `tests/temoignage_canonique.rs`
//! à chaque exécution.
//!
//! **Ce qui n'est pas décidé ici et se voit** : l'algorithme d'empreinte n'a pas
//! de champ. Il est SHA-256 par décision (`empreinte.rs`) ; un lot ne peut donc
//! pas en négocier un autre, et l'agilité d'algorithme, le jour où elle sera
//! due, entrera par une ADR et par un champ — pas par une branche.

use crate::cbor::{
    ControleDeTri, Lecteur, PREFIXE_CARTE, PREFIXE_TABLEAU, PREFIXE_UINT, ecrire_entete,
    ecrire_octets, ecrire_texte, lire_octets, lire_texte,
};
use crate::empreinte::OCTETS_D_EMPREINTE;
use crate::erreur::ErreurDecodage;
use crate::subject::subject_est_canonique;
use crate::temoignage::CLE_INSTANT;

/// Clé du champ `subject` — 03 §1 : « désignation canonique de la source
/// interrogée ».
pub const CLE_SUBJECT: &str = "subject";
/// Clé du champ `attestor` — 03 §1 : « identité(s) de l'attestateur … clés
/// épinglées ».
pub const CLE_ATTESTOR: &str = "attestor";
/// Clé du champ `residual` — 03 §1 : « l'identifiant de l'hypothèse résiduelle
/// du transport, résolu dans le registre des assumptions ».
pub const CLE_RESIDUAL: &str = "residual";
/// Clé du champ `transport` — 03 §1 : « identifiant du mécanisme d'attestation ».
pub const CLE_TRANSPORT: &str = "transport";
/// Clé du champ `utterance` — 03 §1 : « les octets exacts de la réponse (ou leur
/// hash + extraction) ».
pub const CLE_UTTERANCE: &str = "utterance";
/// Clé du champ `observed_at` — 03 §1 : « instant de l'observation, avec
/// l'horloge qui l'a produit ».
pub const CLE_OBSERVED_AT: &str = "observed_at";
/// Clé du champ `transport_proof` — 03 §1 : « l'artefact de preuve du transport,
/// opaque pour Shōgen ».
pub const CLE_TRANSPORT_PROOF: &str = "transport_proof";

/// Clé de l'empreinte, dans la sous-carte `utterance`.
pub const CLE_HASH: &str = "hash";
/// Clé des octets exacts, dans la sous-carte `utterance` — **facultative**
/// (ADR-0005 règle 2 : la rétention des octets est une politique par classe).
pub const CLE_BYTES: &str = "bytes";
/// Clé de l'identité de l'horloge, dans la sous-carte `observed_at`.
pub const CLE_CLOCK: &str = "clock";
/// Clé de la clé épinglée, dans une entrée d'`attestor`.
pub const CLE_KEY: &str = "key";
/// Clé de l'identité, dans une entrée d'`attestor`.
pub const CLE_IDENTITY: &str = "identity";

/// Nombre d'entrées de la carte canonique du témoignage — les sept de 03 §1.
pub const NOMBRE_DE_CHAMPS_DU_TEMOIGNAGE: u64 = 7;

/// L'ordre d'écriture des clés, qui **est** l'ordre canonique : tri
/// lexicographique par octets des clés encodées (RFC 8949 — ADR-0002).
pub const ORDRE_CANONIQUE_DU_TEMOIGNAGE: [&str; 7] = [
    CLE_SUBJECT,
    CLE_ATTESTOR,
    CLE_RESIDUAL,
    CLE_TRANSPORT,
    CLE_UTTERANCE,
    CLE_OBSERVED_AT,
    CLE_TRANSPORT_PROOF,
];

/// Le « dire » — jamais interprété à ce rang (03 §3).
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Utterance {
    /// L'empreinte SHA-256 des octets exacts. **Toujours portée**, sans
    /// exception (ADR-0005 règle 1).
    pub hash: [u8; OCTETS_D_EMPREINTE],
    /// Les octets exacts, quand la politique de classe les retient.
    pub bytes: Option<Vec<u8>>,
}

/// L'instant de l'observation **et l'horloge qui l'a produit** (03 §1 : « celle
/// du transport, jamais celle de Shōgen »).
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ObservedAt {
    /// Identité de l'horloge — donnée portée, opaque au cœur.
    pub clock: String,
    /// L'horodatage, en secondes, **donnée portée** : le cœur ne lit aucune
    /// horloge (ADR-0010, point 1 ; gate S-G2).
    pub instant: u64,
}

/// Une identité d'attestateur et sa clé épinglée (03 §1 : « qui pourrait
/// forger, nominativement »).
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Attestor {
    /// La clé épinglée, octets opaques au cœur.
    pub key: Vec<u8>,
    /// L'identité, opaque au cœur.
    pub identity: String,
}

/// Le témoignage en forme canonique — les sept champs, tous obligatoires.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Temoignage {
    /// La désignation canonique, satisfaisant le prédicat d'ADR-0016.
    pub subject: String,
    /// Les attestateurs, au moins un.
    pub attestor: Vec<Attestor>,
    /// Les hypothèses résiduelles nommées, au moins une, **dans l'ordre émis**.
    pub residual: Vec<String>,
    /// L'identifiant du mécanisme d'attestation, opaque au cœur.
    pub transport: String,
    /// Le dire.
    pub utterance: Utterance,
    /// L'instant et son horloge.
    pub observed_at: ObservedAt,
    /// L'artefact de preuve, **opaque** : le cœur n'en interprète aucun octet.
    pub transport_proof: Vec<u8>,
}

/// Encode un témoignage canonique.
///
/// **Totale** : définie sur toute valeur du type, sans panique, sans I/O. Deux
/// encodeurs honnêtes du même fait produisent les mêmes octets (ADR-0002).
pub fn encoder_temoignage_canonique(temoignage: &Temoignage) -> Vec<u8> {
    let mut sortie = Vec::new();
    ecrire_entete(&mut sortie, PREFIXE_CARTE, NOMBRE_DE_CHAMPS_DU_TEMOIGNAGE);

    ecrire_texte(&mut sortie, CLE_SUBJECT);
    ecrire_texte(&mut sortie, &temoignage.subject);

    ecrire_texte(&mut sortie, CLE_ATTESTOR);
    ecrire_entete(
        &mut sortie,
        PREFIXE_TABLEAU,
        longueur_en_argument(temoignage.attestor.len()),
    );
    for attestor in &temoignage.attestor {
        ecrire_entete(&mut sortie, PREFIXE_CARTE, 2);
        ecrire_texte(&mut sortie, CLE_KEY);
        ecrire_octets(&mut sortie, &attestor.key);
        ecrire_texte(&mut sortie, CLE_IDENTITY);
        ecrire_texte(&mut sortie, &attestor.identity);
    }

    ecrire_texte(&mut sortie, CLE_RESIDUAL);
    ecrire_entete(
        &mut sortie,
        PREFIXE_TABLEAU,
        longueur_en_argument(temoignage.residual.len()),
    );
    for residual in &temoignage.residual {
        ecrire_texte(&mut sortie, residual);
    }

    ecrire_texte(&mut sortie, CLE_TRANSPORT);
    ecrire_texte(&mut sortie, &temoignage.transport);

    ecrire_texte(&mut sortie, CLE_UTTERANCE);
    let entrees = match temoignage.utterance.bytes {
        Some(_) => 2,
        None => 1,
    };
    ecrire_entete(&mut sortie, PREFIXE_CARTE, entrees);
    ecrire_texte(&mut sortie, CLE_HASH);
    ecrire_octets(&mut sortie, &temoignage.utterance.hash);
    if let Some(octets) = temoignage.utterance.bytes.as_ref() {
        ecrire_texte(&mut sortie, CLE_BYTES);
        ecrire_octets(&mut sortie, octets);
    }

    ecrire_texte(&mut sortie, CLE_OBSERVED_AT);
    ecrire_entete(&mut sortie, PREFIXE_CARTE, 2);
    ecrire_texte(&mut sortie, CLE_CLOCK);
    ecrire_texte(&mut sortie, &temoignage.observed_at.clock);
    ecrire_texte(&mut sortie, CLE_INSTANT);
    ecrire_entete(&mut sortie, PREFIXE_UINT, temoignage.observed_at.instant);

    ecrire_texte(&mut sortie, CLE_TRANSPORT_PROOF);
    ecrire_octets(&mut sortie, &temoignage.transport_proof);

    sortie
}

/// Décode un témoignage canonique depuis des octets **venus de l'extérieur**.
///
/// Point de frontière (carte des frontières : `lib.rs`), style *tolérant* : tout
/// écart devient une erreur nommée et positionnée. Strict par décision — un
/// encodage CBOR valide mais non canonique est **refusé, pas normalisé** — et
/// cette rigueur s'étend au contenu : `subject` passe le prédicat d'ADR-0016,
/// les listes ne sont pas vides, les identifiants sont ASCII et sans doublon.
pub fn decoder_temoignage_canonique(octets: &[u8]) -> Result<Temoignage, ErreurDecodage> {
    if octets.is_empty() {
        return Err(ErreurDecodage::EntreeVide);
    }
    let mut lecteur = Lecteur::nouveau(octets);

    let position_carte = lecteur.position();
    let taille = lecteur.entete_de_type(PREFIXE_CARTE)?;
    if taille != NOMBRE_DE_CHAMPS_DU_TEMOIGNAGE {
        return Err(ErreurDecodage::TailleCarteInattendue {
            position: position_carte,
            attendue: NOMBRE_DE_CHAMPS_DU_TEMOIGNAGE,
            trouvee: taille,
        });
    }

    let mut subject: Option<String> = None;
    let mut attestor: Option<Vec<Attestor>> = None;
    let mut residual: Option<Vec<String>> = None;
    let mut transport: Option<String> = None;
    let mut utterance: Option<Utterance> = None;
    let mut observed_at: Option<ObservedAt> = None;
    let mut transport_proof: Option<Vec<u8>> = None;
    let mut tri = ControleDeTri::nouveau();

    for _ in 0..NOMBRE_DE_CHAMPS_DU_TEMOIGNAGE {
        let position_cle = lecteur.position();
        let cle = lire_texte(&mut lecteur)?;
        tri.suivante(position_cle, &cle)?;

        if cle == CLE_SUBJECT {
            subject = Some(lire_subject(&mut lecteur)?);
        } else if cle == CLE_ATTESTOR {
            attestor = Some(lire_attestor(&mut lecteur)?);
        } else if cle == CLE_RESIDUAL {
            residual = Some(lire_residual(&mut lecteur)?);
        } else if cle == CLE_TRANSPORT {
            transport = Some(lire_identifiant(&mut lecteur, CLE_TRANSPORT)?);
        } else if cle == CLE_UTTERANCE {
            utterance = Some(lire_utterance(&mut lecteur)?);
        } else if cle == CLE_OBSERVED_AT {
            observed_at = Some(lire_observed_at(&mut lecteur)?);
        } else if cle == CLE_TRANSPORT_PROOF {
            transport_proof = Some(lire_octets(&mut lecteur)?);
        } else {
            return Err(ErreurDecodage::CleInconnue {
                position: position_cle,
                cle,
            });
        }
    }

    if !lecteur.termine() {
        return Err(ErreurDecodage::OctetsResiduels {
            position: lecteur.position(),
            restants: lecteur.restants(),
        });
    }

    // Passage d'`Option` à valeur sans `unwrap` : la seule sortie licite d'une
    // absence est une erreur nommée (ADR-0010, points 1 et 5).
    let subject = exiger(subject, CLE_SUBJECT)?;
    let attestor = exiger(attestor, CLE_ATTESTOR)?;
    let residual = exiger(residual, CLE_RESIDUAL)?;
    let transport = exiger(transport, CLE_TRANSPORT)?;
    let utterance = exiger(utterance, CLE_UTTERANCE)?;
    let observed_at = exiger(observed_at, CLE_OBSERVED_AT)?;
    let transport_proof = exiger(transport_proof, CLE_TRANSPORT_PROOF)?;

    Ok(Temoignage {
        subject,
        attestor,
        residual,
        transport,
        utterance,
        observed_at,
        transport_proof,
    })
}

/// Un champ absent est une erreur nommée, jamais un défaut silencieux.
fn exiger<T>(valeur: Option<T>, cle: &'static str) -> Result<T, ErreurDecodage> {
    match valeur {
        Some(valeur) => Ok(valeur),
        None => Err(ErreurDecodage::ChampManquant { cle }),
    }
}

/// La longueur d'une liste en argument CBOR. La branche de repli produirait un
/// en-tête que notre propre décodeur refuse — fail-closed jusque dans
/// l'inatteignable (même geste que `cbor::argument_de_longueur`).
fn longueur_en_argument(longueur: usize) -> u64 {
    u64::try_from(longueur).unwrap_or(u64::MAX)
}

/// `subject` : lu comme texte, puis **soumis au prédicat** d'ADR-0016.
fn lire_subject(lecteur: &mut Lecteur<'_>) -> Result<String, ErreurDecodage> {
    let position = lecteur.position();
    let texte = lire_texte(lecteur)?;
    match subject_est_canonique(texte.as_bytes()) {
        Ok(()) => Ok(texte),
        Err(cause) => Err(ErreurDecodage::SubjectNonCanonique { position, cause }),
    }
}

/// Un identifiant porté : texte non vide, ASCII. ASCII parce qu'un identifiant
/// dont la comparaison dépendrait d'une table Unicode versionnée ne serait pas
/// recalculable hors ligne (ADR-0003 ; même motif qu'ADR-0016 C3).
fn lire_identifiant(
    lecteur: &mut Lecteur<'_>,
    cle: &'static str,
) -> Result<String, ErreurDecodage> {
    let position = lecteur.position();
    let texte = lire_texte(lecteur)?;
    controler_identifiant(&texte, position, cle)?;
    Ok(texte)
}

/// Le contrôle d'un identifiant, isolé pour servir aux textes lus en liste.
fn controler_identifiant(
    texte: &str,
    position: usize,
    cle: &'static str,
) -> Result<(), ErreurDecodage> {
    if texte.is_empty() {
        return Err(ErreurDecodage::ChampVide { position, cle });
    }
    for octet in texte.as_bytes().iter().copied() {
        if !octet.is_ascii() {
            return Err(ErreurDecodage::ChampNonAscii {
                position,
                cle,
                octet,
            });
        }
    }
    Ok(())
}

/// L'en-tête d'un tableau non vide.
fn entete_de_tableau(lecteur: &mut Lecteur<'_>, cle: &'static str) -> Result<u64, ErreurDecodage> {
    let position = lecteur.position();
    let taille = lecteur.entete_de_type(PREFIXE_TABLEAU)?;
    if taille == 0 {
        return Err(ErreurDecodage::ChampVide { position, cle });
    }
    Ok(taille)
}

/// `residual` : liste non vide d'identifiants, **ordre émis conservé**, sans
/// doublon.
///
/// Pourquoi le doublon est refusé plutôt qu'ignoré : dédupliquer serait
/// réécrire, et 03 §2 exige que les résidus se publient « par mécanisme, jamais
/// agrégés » — deux fois le même résidu n'ajoute rien et rendrait deux lots
/// distincts porteurs du même sens. Refus nommé, jamais normalisation
/// silencieuse (ADR-0016 C0, transposé).
fn lire_residual(lecteur: &mut Lecteur<'_>) -> Result<Vec<String>, ErreurDecodage> {
    let taille = entete_de_tableau(lecteur, CLE_RESIDUAL)?;
    let mut residus: Vec<String> = Vec::new();
    for _ in 0..taille {
        let position = lecteur.position();
        let identifiant = lire_texte(lecteur)?;
        controler_identifiant(&identifiant, position, CLE_RESIDUAL)?;
        if residus.iter().any(|deja| deja == &identifiant) {
            return Err(ErreurDecodage::EntreeDupliquee {
                position,
                cle: CLE_RESIDUAL,
                valeur: identifiant,
            });
        }
        residus.push(identifiant);
    }
    Ok(residus)
}

/// `attestor` : liste non vide de couples (clé épinglée, identité).
///
/// Le doublon exact (même clé ET même identité) est refusé, par la même
/// justification que `lire_residual` — et par une raison propre au champ
/// (adjudication de la revue G2 de phase C, trouvaille F5) : 03 §1 fait
/// d'`attestor` le champ qui dit « qui pourrait forger, nominativement »,
/// et ADR-0004 en fait un axe R2 du certificat de diversité — un
/// attestateur répété est précisément la forme qui gonflerait un compte de
/// diversité (la leçon K&L §4 : un axe déclaré n'est pas un axe
/// protecteur). Refus nommé, jamais déduplication silencieuse.
fn lire_attestor(lecteur: &mut Lecteur<'_>) -> Result<Vec<Attestor>, ErreurDecodage> {
    let taille = entete_de_tableau(lecteur, CLE_ATTESTOR)?;
    let mut attestors: Vec<Attestor> = Vec::new();
    for _ in 0..taille {
        let position_carte = lecteur.position();
        let entrees = lecteur.entete_de_type(PREFIXE_CARTE)?;
        if entrees != 2 {
            return Err(ErreurDecodage::TailleCarteInattendue {
                position: position_carte,
                attendue: 2,
                trouvee: entrees,
            });
        }
        let mut tri = ControleDeTri::nouveau();
        let mut key: Option<Vec<u8>> = None;
        let mut identity: Option<String> = None;
        for _ in 0..entrees {
            let position_cle = lecteur.position();
            let cle = lire_texte(lecteur)?;
            tri.suivante(position_cle, &cle)?;
            if cle == CLE_KEY {
                let position = lecteur.position();
                let octets = lire_octets(lecteur)?;
                if octets.is_empty() {
                    return Err(ErreurDecodage::ChampVide {
                        position,
                        cle: CLE_KEY,
                    });
                }
                key = Some(octets);
            } else if cle == CLE_IDENTITY {
                identity = Some(lire_identifiant(lecteur, CLE_IDENTITY)?);
            } else {
                return Err(ErreurDecodage::CleInconnue {
                    position: position_cle,
                    cle,
                });
            }
        }
        let attestor = Attestor {
            key: exiger(key, CLE_KEY)?,
            identity: exiger(identity, CLE_IDENTITY)?,
        };
        if attestors
            .iter()
            .any(|deja| deja.key == attestor.key && deja.identity == attestor.identity)
        {
            return Err(ErreurDecodage::EntreeDupliquee {
                position: position_carte,
                cle: CLE_ATTESTOR,
                valeur: attestor.identity,
            });
        }
        attestors.push(attestor);
    }
    Ok(attestors)
}

/// `utterance` : l'empreinte toujours, les octets par politique.
fn lire_utterance(lecteur: &mut Lecteur<'_>) -> Result<Utterance, ErreurDecodage> {
    let position_carte = lecteur.position();
    let entrees = lecteur.entete_de_type(PREFIXE_CARTE)?;
    if entrees != 1 && entrees != 2 {
        return Err(ErreurDecodage::TailleCarteHorsEnsemble {
            position: position_carte,
            admises: &[1, 2],
            trouvee: entrees,
        });
    }
    let mut tri = ControleDeTri::nouveau();
    let mut hash: Option<[u8; OCTETS_D_EMPREINTE]> = None;
    let mut bytes: Option<Vec<u8>> = None;
    for _ in 0..entrees {
        let position_cle = lecteur.position();
        let cle = lire_texte(lecteur)?;
        tri.suivante(position_cle, &cle)?;
        if cle == CLE_HASH {
            let position = lecteur.position();
            let octets = lire_octets(lecteur)?;
            // La conversion **est** le contrôle de longueur : aucune empreinte
            // d'une autre taille n'entre, et aucun `unwrap` n'est nécessaire.
            match <[u8; OCTETS_D_EMPREINTE]>::try_from(octets.as_slice()) {
                Ok(valeur) => hash = Some(valeur),
                Err(_) => {
                    return Err(ErreurDecodage::LongueurDEmpreinteInvalide {
                        position,
                        attendue: OCTETS_D_EMPREINTE,
                        trouvee: octets.len(),
                    });
                }
            }
        } else if cle == CLE_BYTES {
            bytes = Some(lire_octets(lecteur)?);
        } else {
            return Err(ErreurDecodage::CleInconnue {
                position: position_cle,
                cle,
            });
        }
    }
    Ok(Utterance {
        hash: exiger(hash, CLE_HASH)?,
        bytes,
    })
}

/// `observed_at` : l'horloge qui a daté, et la date qu'elle a produite.
fn lire_observed_at(lecteur: &mut Lecteur<'_>) -> Result<ObservedAt, ErreurDecodage> {
    let position_carte = lecteur.position();
    let entrees = lecteur.entete_de_type(PREFIXE_CARTE)?;
    if entrees != 2 {
        return Err(ErreurDecodage::TailleCarteInattendue {
            position: position_carte,
            attendue: 2,
            trouvee: entrees,
        });
    }
    let mut tri = ControleDeTri::nouveau();
    let mut clock: Option<String> = None;
    let mut instant: Option<u64> = None;
    for _ in 0..entrees {
        let position_cle = lecteur.position();
        let cle = lire_texte(lecteur)?;
        tri.suivante(position_cle, &cle)?;
        if cle == CLE_CLOCK {
            clock = Some(lire_identifiant(lecteur, CLE_CLOCK)?);
        } else if cle == CLE_INSTANT {
            instant = Some(lecteur.entete_de_type(PREFIXE_UINT)?);
        } else {
            return Err(ErreurDecodage::CleInconnue {
                position: position_cle,
                cle,
            });
        }
    }
    Ok(ObservedAt {
        clock: exiger(clock, CLE_CLOCK)?,
        instant: exiger(instant, CLE_INSTANT)?,
    })
}
