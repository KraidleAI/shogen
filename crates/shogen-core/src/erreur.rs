//! Les erreurs **nommées** du décodage.
//!
//! ADR-0010, point 1 (*total*) : « Une entrée mal formée est une **valeur** du
//! type de retour (erreur nommée), jamais une divergence. » Chaque variante dit
//! *où* (position d'octet) et *quoi*, pour qu'un refus soit diagnosticable sans
//! journal — le cœur ne journalise pas (ADR-0010, point 1, *sans I/O*).

/// Refus de décodage. Un lot que le cœur ne sait pas classer est refusé, jamais
/// admis par défaut (ADR-0010, point 5 : *fail-safe defaults*).
use alloc::string::String;

#[derive(Debug, Clone, PartialEq, Eq)]
#[non_exhaustive]
pub enum ErreurDecodage {
    /// Aucun octet à décoder.
    EntreeVide,
    /// Les octets requis dépassent ce que l'entrée contient.
    FinPrematuree {
        position: usize,
        octets_requis: usize,
        octets_disponibles: usize,
    },
    /// Type majeur CBOR autre que celui attendu à cette position.
    TypeMajeurInattendu {
        position: usize,
        prefixe_attendu: u8,
        prefixe_trouve: u8,
    },
    /// Longueur indéfinie (argument 31) : interdite par les Core Deterministic
    /// Encoding Requirements de la RFC 8949 (ADR-0002).
    LongueurIndefinie { position: usize },
    /// Argument encodé sur plus d'octets que nécessaire : viole la sérialisation
    /// préférée exigée par le sous-ensemble canonique (ADR-0002).
    EntierNonPrefere {
        position: usize,
        argument: u64,
        octets_utilises: u8,
    },
    /// Valeur d'information 28, 29 ou 30 : réservée par la RFC 8949.
    ArgumentReserve { position: usize, information: u8 },
    /// Longueur annoncée non représentable en mémoire sur cette machine.
    /// Aucune allocation n'est faite avant ce contrôle (ADR-0010, point 1).
    LongueurHorsMemoire { position: usize, longueur: u64 },
    /// La carte du témoignage n'a pas exactement le nombre d'entrées attendu.
    TailleCarteInattendue {
        position: usize,
        attendue: u64,
        trouvee: u64,
    },
    /// Taille de carte hors d'un ensemble admis à plusieurs valeurs — le cas
    /// d'`utterance` ({1, 2} : empreinte seule, ou empreinte + octets). Une
    /// variante dédiée parce qu'un message « 2 attendue(s) » sur une carte à
    /// 3 entrées annoncerait une attente que le code n'a pas (revue G2 de
    /// phase C, trouvaille F4 — un refus se diagnostique sans journal).
    TailleCarteHorsEnsemble {
        position: usize,
        admises: &'static [u64],
        trouvee: u64,
    },
    /// Clé absente du vocabulaire du témoignage trivial.
    CleInconnue { position: usize, cle: String },
    /// Clés non triées : l'ordre lexicographique par octets des clés encodées
    /// est une exigence du sous-ensemble canonique (ADR-0002).
    ClesNonTriees {
        position: usize,
        precedente: String,
        courante: String,
    },
    /// Même clé deux fois.
    CleDupliquee { position: usize, cle: String },
    /// Une clé attendue manque.
    ChampManquant { cle: &'static str },
    /// Chaîne de texte qui n'est pas de l'UTF-8 valide.
    TexteNonUtf8 { position: usize, longueur: usize },
    /// Des octets subsistent après le témoignage : un lot canonique n'a pas de
    /// queue (sinon deux suites d'octets distinctes décoderaient au même fait).
    OctetsResiduels { position: usize, restants: usize },
    /// La carte de tête n'a le nombre d'entrées d'aucune forme connue de lot.
    /// Fail-closed jusqu'au cas dégénéré (ADR-0010, point 5) : un lot que le
    /// cœur ne sait pas classer est refusé, jamais admis par défaut.
    TailleDeLotInconnue { position: usize, trouvee: u64 },
    /// `subject` ne satisfait pas le prédicat de canonicité — ADR-0016 C10 : le
    /// témoignage est **refusé**, jamais réécrit.
    SubjectNonCanonique {
        position: usize,
        cause: crate::subject::ErreurSubject,
    },
    /// L'empreinte portée n'a pas la longueur d'un condensé SHA-256.
    LongueurDEmpreinteInvalide {
        position: usize,
        attendue: usize,
        trouvee: usize,
    },
    /// Un champ obligatoire est présent mais vide : liste sans élément, texte
    /// sans caractère, clé épinglée sans octet. Le vide n'est pas une valeur
    /// admissible d'un champ dont 03 §1 dit qu'il est obligatoire.
    ChampVide { position: usize, cle: &'static str },
    /// Un identifiant porté sort de l'US-ASCII : sa comparaison dépendrait
    /// d'une table Unicode versionnée, donc ne serait pas recalculable hors
    /// ligne (ADR-0003 ; même motif qu'ADR-0016 C3).
    ChampNonAscii {
        position: usize,
        cle: &'static str,
        octet: u8,
    },
    /// Deux fois la même entrée dans une liste où la répétition n'ajoute rien.
    /// Refus, jamais déduplication (ADR-0016 C0, transposé).
    EntreeDupliquee {
        position: usize,
        cle: &'static str,
        valeur: String,
    },
}

impl core::fmt::Display for ErreurDecodage {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        match self {
            Self::EntreeVide => write!(f, "entrée vide : aucun octet à décoder"),
            Self::FinPrematuree {
                position,
                octets_requis,
                octets_disponibles,
            } => write!(
                f,
                "fin prématurée à l'octet {position} : {octets_requis} octet(s) requis, {octets_disponibles} disponible(s)"
            ),
            Self::TypeMajeurInattendu {
                position,
                prefixe_attendu,
                prefixe_trouve,
            } => write!(
                f,
                "type majeur inattendu à l'octet {position} : préfixe 0x{prefixe_attendu:02x} attendu, 0x{prefixe_trouve:02x} trouvé"
            ),
            Self::LongueurIndefinie { position } => write!(
                f,
                "longueur indéfinie à l'octet {position} : interdite par le sous-ensemble canonique"
            ),
            Self::EntierNonPrefere {
                position,
                argument,
                octets_utilises,
            } => write!(
                f,
                "entier non préféré à l'octet {position} : argument {argument} encodé sur {octets_utilises} octet(s) d'argument"
            ),
            Self::ArgumentReserve {
                position,
                information,
            } => write!(
                f,
                "argument réservé à l'octet {position} : valeur d'information {information}"
            ),
            Self::LongueurHorsMemoire { position, longueur } => write!(
                f,
                "longueur hors mémoire à l'octet {position} : {longueur} octet(s) annoncé(s)"
            ),
            Self::TailleCarteInattendue {
                position,
                attendue,
                trouvee,
            } => write!(
                f,
                "taille de carte inattendue à l'octet {position} : {attendue} entrée(s) attendue(s), {trouvee} trouvée(s)"
            ),
            Self::TailleCarteHorsEnsemble {
                position,
                admises,
                trouvee,
            } => write!(
                f,
                "taille de carte hors ensemble admis à l'octet {position} : {admises:?} entrée(s) admise(s), {trouvee} trouvée(s)"
            ),
            Self::CleInconnue { position, cle } => write!(
                f,
                "clé inconnue à l'octet {position} : « {cle} » n'est pas du vocabulaire du témoignage trivial"
            ),
            Self::ClesNonTriees {
                position,
                precedente,
                courante,
            } => write!(
                f,
                "clés non triées à l'octet {position} : « {courante} » ne suit pas « {precedente} » dans l'ordre par octets"
            ),
            Self::CleDupliquee { position, cle } => {
                write!(f, "clé dupliquée à l'octet {position} : « {cle} »")
            }
            Self::ChampManquant { cle } => write!(f, "champ manquant : « {cle} »"),
            Self::TexteNonUtf8 { position, longueur } => write!(
                f,
                "texte non UTF-8 à l'octet {position} : {longueur} octet(s) refusé(s)"
            ),
            Self::OctetsResiduels { position, restants } => write!(
                f,
                "octets résiduels à partir de l'octet {position} : {restants} octet(s) en trop"
            ),
            Self::TailleDeLotInconnue { position, trouvee } => write!(
                f,
                "forme de lot inconnue à l'octet {position} : carte de {trouvee} entrée(s) — aucune forme du vocabulaire ne l'admet"
            ),
            Self::SubjectNonCanonique { position, cause } => {
                write!(f, "subject non canonique à l'octet {position} : {cause}")
            }
            Self::LongueurDEmpreinteInvalide {
                position,
                attendue,
                trouvee,
            } => write!(
                f,
                "longueur d'empreinte invalide à l'octet {position} : {attendue} octet(s) attendu(s), {trouvee} trouvé(s)"
            ),
            Self::ChampVide { position, cle } => write!(
                f,
                "champ vide à l'octet {position} : « {cle} » est obligatoire et n'admet pas le vide"
            ),
            Self::ChampNonAscii {
                position,
                cle,
                octet,
            } => write!(
                f,
                "champ non ASCII à l'octet {position} : « {cle} » porte l'octet 0x{octet:02x}"
            ),
            Self::EntreeDupliquee {
                position,
                cle,
                valeur,
            } => write!(
                f,
                "entrée dupliquée à l'octet {position} : « {valeur} » figure deux fois dans « {cle} »"
            ),
        }
    }
}

impl core::error::Error for ErreurDecodage {}
