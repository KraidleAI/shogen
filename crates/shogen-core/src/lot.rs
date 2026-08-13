//! Le **lot** — ce que le vérificateur reçoit, et la seule porte par laquelle
//! des octets étrangers entrent dans le cœur.
//!
//! Rattachement (G0) : **13 §6 point 2** — « Le lot de S3 est un lot à un
//! témoignage : `shogen verify <lot>` du critère opère sur la structure de lot
//! du squelette S2.5, peuplée d'un témoignage réel unique » ; **ADR-0010**
//! point 5 (*fail-safe defaults*) ; **ADR-0002** (forme canonique unique).
//!
//! Deux formes coexistent, et le fait qu'elles coexistent est **écrit** plutôt
//! que caché :
//!
//! * le **témoignage trivial** du walking skeleton (trois champs factices,
//!   12 §5) — conservé tel quel, parce qu'un squelette qu'on casse en le
//!   remplaçant n'a jamais montré qu'il portait ;
//! * le **témoignage canonique** des sept champs de 03 §1.
//!
//! Le tri se fait sur le **nombre d'entrées de la carte de tête** — un fait
//! d'octets, lu avant toute autre interprétation, jamais sur une étiquette que
//! le lot se donnerait à lui-même. Toute autre taille est refusée : le défaut
//! est le refus, l'admission est énumérée.

use alloc::boxed::Box;
use alloc::vec::Vec;

use crate::cbor::{Lecteur, PREFIXE_CARTE};
use crate::erreur::ErreurDecodage;
use crate::temoignage::{
    NOMBRE_DE_CHAMPS, TemoignageTrivial, decoder_temoignage, encoder_temoignage,
};
use crate::temoignage_canonique::{
    NOMBRE_DE_CHAMPS_DU_TEMOIGNAGE, Temoignage, decoder_temoignage_canonique,
    encoder_temoignage_canonique,
};

/// Un lot décodé, dans l'une des deux formes admises.
///
/// **Volontairement exhaustive**, là où les erreurs sont `#[non_exhaustive]` :
/// une variante d'erreur nouvelle se traite par un message, une **forme de lot**
/// nouvelle se traite par une décision. Un consommateur qui écrirait
/// `_ => …` déciderait par défaut de ce qu'il ne connaît pas — exactement ce que
/// *fail-safe defaults* interdit (ADR-0010, point 5). L'ajout d'une forme est
/// donc une rupture d'API assumée, qui oblige chaque appelant à trancher.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Lot {
    /// Le témoignage trivial du walking skeleton (12 §5).
    Trivial(TemoignageTrivial),
    /// Le témoignage en forme canonique (03 §1).
    Canonique(Box<Temoignage>),
}

/// Décode un lot **venu de l'extérieur**, quelle que soit sa forme.
///
/// Point de frontière (carte des frontières : `lib.rs`), style *tolérant*.
/// L'en-tête est lu deux fois — une fois pour trier, une fois par le décodeur
/// choisi : chaque décodeur reste ainsi **complet et testable seul**, et le
/// coût est un en-tête, pas une structure partagée mutable.
pub fn decoder_lot(octets: &[u8]) -> Result<Lot, ErreurDecodage> {
    if octets.is_empty() {
        return Err(ErreurDecodage::EntreeVide);
    }
    let mut lecteur = Lecteur::nouveau(octets);
    let position = lecteur.position();
    let taille = lecteur.entete_de_type(PREFIXE_CARTE)?;
    if taille == NOMBRE_DE_CHAMPS {
        return Ok(Lot::Trivial(decoder_temoignage(octets)?));
    }
    if taille == NOMBRE_DE_CHAMPS_DU_TEMOIGNAGE {
        return Ok(Lot::Canonique(Box::new(decoder_temoignage_canonique(
            octets,
        )?)));
    }
    Err(ErreurDecodage::TailleDeLotInconnue {
        position,
        trouvee: taille,
    })
}

/// Ré-encode un lot. `encoder_lot(decoder_lot(b)) == b` pour tout `b` accepté :
/// c'est la seconde moitié de la propriété (a) d'ADR-0011, portée au rang du
/// lot.
pub fn encoder_lot(lot: &Lot) -> Vec<u8> {
    match lot {
        Lot::Trivial(temoignage) => encoder_temoignage(temoignage),
        Lot::Canonique(temoignage) => encoder_temoignage_canonique(temoignage),
    }
}
