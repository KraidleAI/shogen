//! Le **fait prix typé** — ce que le typeur produit.
//!
//! Rattachement (G0) : **03 §3** (deux rangs jamais confondus : le dire brut et
//! l'extraction ; « le fait cite [son typeur] ») ; **09-vocabulaire** —
//! l'interdit « **fait signé** » : « l'attestation couvre les octets du dire ;
//! le fait est produit par un typeur, testé jamais prouvé — personne ne signe
//! un fait ». Ce type n'a donc **aucun** champ de signature, aucun champ de
//! confiance, aucun champ de qualité.
//!
//! Ce qu'un fait porte, et rien d'autre : une valeur décimale exacte, sa
//! devise, l'instant que la source a daté, et l'identité du typeur qui l'a
//! extrait.

use crate::decimale::Decimale;
use crate::identite::IdentiteDuTypeur;
use crate::instant::Instant;

/// La devise d'un fait prix.
///
/// **Elle ne vient pas du dire.** Le dire de Coinbase ne l'étiquette pas : elle
/// vient de l'endpoint interrogé (`/products/BTC-USD/ticker`), donc du
/// `subject`. Le dossier S2 nomme déjà ce mode de lecture au même endroit —
/// 10 §3.1, ligne DefiLlama : « USD **par convention d'endpoint, non étiqueté
/// dans le JSON** ». C'est la raison pour laquelle ce typeur exige un `subject`
/// épinglé : sans lui, la devise serait une supposition.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[non_exhaustive]
pub enum Devise {
    /// Dollar des États-Unis.
    Usd,
}

impl Devise {
    /// Le code de la devise.
    pub fn code(self) -> &'static str {
        match self {
            Devise::Usd => "USD",
        }
    }
}

/// Un fait prix typé.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FaitPrix {
    /// La valeur, en décimal exact — jamais un flottant binaire.
    pub valeur: Decimale,
    /// La devise, lue à l'endpoint.
    pub devise: Devise,
    /// L'instant daté par la source, en graphie verbatim.
    pub instant: Instant,
    /// L'identité du typeur qui a produit ce fait.
    pub typeur: IdentiteDuTypeur,
}
