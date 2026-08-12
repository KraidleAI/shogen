//! Le témoignage **trivial** du walking skeleton (12 §5) et sa forme canonique.
//!
//! Zéro logique produit (12 §1, non-objet 1) : trois champs factices, aucun
//! transport, aucune statistique. Ce qui est exercé ici n'est pas le fait
//! métier — c'est l'ossature : cœur pur → forme canonique → vérificateur
//! séparé.
//!
//! `instant` est une **donnée portée**, jamais une lecture d'horloge :
//! ADR-0010, point 1 — « Un horodatage est une **donnée** qui entre en
//! argument, jamais une lecture d'horloge ». La gate S-G2 le mesure.

use crate::cbor::{
    Lecteur, PREFIXE_CARTE, PREFIXE_OCTETS, PREFIXE_TEXTE, PREFIXE_UINT, ecrire_entete,
    ecrire_octets, ecrire_texte,
};
use crate::erreur::ErreurDecodage;

/// Clé du champ `source`.
pub const CLE_SOURCE: &str = "source";
/// Clé du champ `contenu`.
pub const CLE_CONTENU: &str = "contenu";
/// Clé du champ `instant`.
pub const CLE_INSTANT: &str = "instant";

/// Nombre d'entrées de la carte canonique du témoignage trivial.
pub const NOMBRE_DE_CHAMPS: u64 = 3;

/// L'ordre d'écriture des clés, qui **est** l'ordre canonique : tri
/// lexicographique par octets des clés encodées (RFC 8949, Core Deterministic
/// Encoding Requirements — ADR-0002).
///
/// Cet ordre n'est pas une croyance : `tests/canonique.rs` recalcule les trois
/// encodages de clés et vérifie que cette constante est bien leur tri.
pub const ORDRE_CANONIQUE_DES_CLES: [&str; 3] = [CLE_SOURCE, CLE_CONTENU, CLE_INSTANT];

/// Témoignage trivial : trois champs factices, rien d'autre.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TemoignageTrivial {
    /// Identifiant de source, opaque au cœur.
    pub source: String,
    /// Horodatage **porté en donnée**, jamais lu d'une horloge.
    pub instant: u64,
    /// Octets bruts de l'énoncé.
    pub contenu: Vec<u8>,
}

/// Encode un témoignage dans la forme canonique.
///
/// **Totale** : définie sur toute valeur du type, sans panique, sans I/O. Deux
/// encodeurs honnêtes du même fait produisent les mêmes octets — c'est la
/// raison d'être d'ADR-0002, et la propriété (b) d'ADR-0011.
pub fn encoder_temoignage(temoignage: &TemoignageTrivial) -> Vec<u8> {
    let mut sortie = Vec::new();
    ecrire_entete(&mut sortie, PREFIXE_CARTE, NOMBRE_DE_CHAMPS);
    ecrire_texte(&mut sortie, CLE_SOURCE);
    ecrire_texte(&mut sortie, &temoignage.source);
    ecrire_texte(&mut sortie, CLE_CONTENU);
    ecrire_octets(&mut sortie, &temoignage.contenu);
    ecrire_texte(&mut sortie, CLE_INSTANT);
    ecrire_entete(&mut sortie, PREFIXE_UINT, temoignage.instant);
    sortie
}

/// Décode un témoignage depuis des octets **venus de l'extérieur**.
///
/// C'est LE point de frontière du cœur (carte des frontières : `lib.rs`) : style
/// *tolérant* au sens de Meyer — précondition faible, toute entrée mal formée
/// devient une erreur nommée en retour. Ce contrôle n'est pas de la
/// programmation défensive : il est l'**établissement unique** de la
/// précondition dont tout l'intérieur dépend ensuite (ADR-0010, point 6).
///
/// Strict par décision : seule la forme canonique est acceptée. Un encodage
/// CBOR valide mais non canonique est **refusé**, pas normalisé.
pub fn decoder_temoignage(octets: &[u8]) -> Result<TemoignageTrivial, ErreurDecodage> {
    if octets.is_empty() {
        return Err(ErreurDecodage::EntreeVide);
    }
    let mut lecteur = Lecteur::nouveau(octets);

    let position_carte = lecteur.position();
    let taille = lecteur.entete_de_type(PREFIXE_CARTE)?;
    if taille != NOMBRE_DE_CHAMPS {
        return Err(ErreurDecodage::TailleCarteInattendue {
            position: position_carte,
            attendue: NOMBRE_DE_CHAMPS,
            trouvee: taille,
        });
    }

    let mut source: Option<String> = None;
    let mut contenu: Option<Vec<u8>> = None;
    let mut instant: Option<u64> = None;
    let mut cle_precedente: Option<(String, Vec<u8>)> = None;

    for _ in 0..NOMBRE_DE_CHAMPS {
        let position_cle = lecteur.position();
        let cle = lire_texte(&mut lecteur)?;
        let encodage = encodage_de_cle(&cle);

        // Tri strictement croissant : il établit à lui seul l'unicité des clés.
        // Aucun second contrôle « au cas où » (ADR-0010, point 6 : la condition
        // appartient à un seul côté, nommé).
        if let Some((precedente, encodage_precedent)) = cle_precedente.as_ref() {
            if encodage.as_slice() == encodage_precedent.as_slice() {
                return Err(ErreurDecodage::CleDupliquee {
                    position: position_cle,
                    cle,
                });
            }
            if encodage.as_slice() < encodage_precedent.as_slice() {
                return Err(ErreurDecodage::ClesNonTriees {
                    position: position_cle,
                    precedente: precedente.clone(),
                    courante: cle,
                });
            }
        }

        if cle == CLE_SOURCE {
            source = Some(lire_texte(&mut lecteur)?);
        } else if cle == CLE_CONTENU {
            contenu = Some(lire_octets(&mut lecteur)?);
        } else if cle == CLE_INSTANT {
            instant = Some(lecteur.entete_de_type(PREFIXE_UINT)?);
        } else {
            return Err(ErreurDecodage::CleInconnue {
                position: position_cle,
                cle,
            });
        }
        cle_precedente = Some((cle, encodage));
    }

    if !lecteur.termine() {
        return Err(ErreurDecodage::OctetsResiduels {
            position: lecteur.position(),
            restants: lecteur.restants(),
        });
    }

    // Passage d'`Option` à valeur sans `unwrap` : la seule sortie licite d'une
    // absence est une erreur nommée (ADR-0010, points 1 et 5).
    let source = match source {
        Some(valeur) => valeur,
        None => return Err(ErreurDecodage::ChampManquant { cle: CLE_SOURCE }),
    };
    let contenu = match contenu {
        Some(valeur) => valeur,
        None => return Err(ErreurDecodage::ChampManquant { cle: CLE_CONTENU }),
    };
    let instant = match instant {
        Some(valeur) => valeur,
        None => return Err(ErreurDecodage::ChampManquant { cle: CLE_INSTANT }),
    };

    Ok(TemoignageTrivial {
        source,
        instant,
        contenu,
    })
}

/// Encodage canonique d'une clé de texte — sert au contrôle du tri.
///
/// Le tri exigé porte sur les **octets des clés encodées**, pas sur les
/// chaînes : les deux ne coïncident pas en général (la longueur préfixe).
pub fn encodage_de_cle(cle: &str) -> Vec<u8> {
    let mut sortie = Vec::new();
    ecrire_texte(&mut sortie, cle);
    sortie
}

fn lire_texte(lecteur: &mut Lecteur<'_>) -> Result<String, ErreurDecodage> {
    let position = lecteur.position();
    let argument = lecteur.entete_de_type(PREFIXE_TEXTE)?;
    let longueur = lecteur.longueur_memoire(argument)?;
    let octets = lecteur.tranche(longueur)?;
    match core::str::from_utf8(octets) {
        Ok(texte) => Ok(texte.to_owned()),
        Err(_) => Err(ErreurDecodage::TexteNonUtf8 { position, longueur }),
    }
}

fn lire_octets(lecteur: &mut Lecteur<'_>) -> Result<Vec<u8>, ErreurDecodage> {
    let argument = lecteur.entete_de_type(PREFIXE_OCTETS)?;
    let longueur = lecteur.longueur_memoire(argument)?;
    Ok(lecteur.tranche(longueur)?.to_vec())
}
