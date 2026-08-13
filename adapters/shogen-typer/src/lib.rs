#![forbid(unsafe_code)]
#![deny(
    clippy::unwrap_used,
    clippy::expect_used,
    clippy::panic,
    clippy::indexing_slicing,
    clippy::arithmetic_side_effects
)]
//! **`shogen-typer`** — le premier typeur : dire brut JSON d'un endpoint du
//! pool S2 → **fait prix typé**, décimal exact, fail-closed.
//!
//! # Rattachement (G0)
//!
//! * **ADR-0001** : les transports — et les typeurs avec eux — sont des
//!   **adapters** : « ils apportent les témoignages bruts, sont **testés et
//!   jamais prouvés** ». Rien ici n'est *proven*, et aucune phrase de ce paquet
//!   ne doit le laisser croire.
//! * **03 §3** : deux rangs qui ne se confondent jamais — le **dire brut**
//!   (hash des octets exacts, lien au `transport_proof`) et l'**extraction**
//!   (« le passage du brut au fait typé … est le travail d'un typeur, adapter
//!   identifié, testé jamais prouvé, dont l'identité et la version figurent
//!   dans le *fait*, pas dans le témoignage »). **Ce paquet ne touche à aucun
//!   témoignage** : il ne construit, ne modifie et ne signe rien de canonique.
//! * **08, A(typer-correctness)** : « Le typeur extrait du dire brut le fait
//!   annoncé (classe, valeur, unité) sans erreur de sens » — assurance visée à
//!   S3 : *tested*, avec compte d'itérations (voir [`identite`]). Cette
//!   assumption **n'est jamais déchargée** : elle est bornée par les tests et
//!   par l'identité du typeur dans le fait.
//! * **13 §2, pièce 4** : le typeur de la phase C de S3.
//! * **10 §3.1** : le pool S2 et ses formats re-mesurés le 2026-08-05 ; c'est
//!   de cette table que vient l'endpoint épinglé ci-dessous.
//! * **ADR-0016** : le `subject` est en forme canonique construite ; le
//!   prédicat total est au cœur, et ce typeur s'en sert.
//!
//! # Ce que ce typeur fait
//!
//! Un seul geste : `(subject, octets du dire) → fait prix typé`, pour **un**
//! endpoint — le ticker Coinbase Exchange BTC-USD du pool S2. Il lit deux
//! membres de l'objet racine du dire (`price`, `time`), les type exactement, et
//! rend un fait qui cite son propre typeur.
//!
//! # Ce que ce typeur ne fait PAS
//!
//! * **Aucune I/O, aucun réseau, aucune horloge.** Le dire lui est donné ; il
//!   ne va le chercher nulle part et ne date rien lui-même (03 §1 : l'instant
//!   est celui du transport, jamais celui de Shōgen).
//! * **Aucun arrondi, aucune troncature, aucun repli.** Ce qu'il ne type pas
//!   exactement, il le refuse en nommant la clause violée.
//! * **Aucun flottant binaire**, nulle part, à aucun rang.
//! * **Aucune liaison au témoignage** : il ne calcule pas le hash d'`utterance`
//!   et ne contrôle aucune preuve de transport. Cette liaison est le travail du
//!   cœur et du vérificateur (ADR-0005 règle 1, 03 §4) ; l'y dupliquer créerait
//!   un second endroit où elle pourrait être fausse.
//! * **Aucun jugement.** Pas de champ vérité, pas de confiance, pas de qualité
//!   de source — la forme du fait n'a pas de slot pour ce que la couche
//!   au-dessus ne doit pas croire (03 §0).
//!
//! # Régime d'assurance
//!
//! *tested (avec compte d'itérations)* — voir [`identite::COMPTE_D_ITERATIONS`]
//! et `tests/compte.rs`. Jamais *proven*.

pub mod decimale;
pub mod erreur;
pub mod fait;
pub mod identite;
pub mod instant;
pub mod json;

pub use decimale::{Decimale, typer_decimale};
pub use erreur::{ErreurDecimale, ErreurInstant, ErreurJson, PROFONDEUR_MAXIMALE, RefusDeTypage};
pub use fait::{Devise, FaitPrix};
pub use identite::{COMPTE_D_ITERATIONS, IdentiteDuTypeur, identite};
pub use instant::{Instant, typer_instant};
pub use json::{ObjetRacine, Valeur, analyser_objet_racine};

use shogen_core::subject_est_canonique;

/// Le `subject` que ce typeur sait lire, et le seul.
///
/// C'est la ligne 2 de la table re-mesurée de 10 §3.1 (« Coinbase Exchange »,
/// sans clé, HTTP 200, horodatage porté dans le dire), écrite en forme
/// canonique d'ADR-0016 : `https`, hôte en minuscules, port par défaut
/// implicite, aucun segment pointillé, aucune requête.
///
/// **Pourquoi épingler** : la devise n'est pas dans le dire (voir
/// [`Devise`]). Elle se lit à l'endpoint. Un typeur qui accepterait n'importe
/// quel `subject` attribuerait donc une devise supposée à une valeur lue — la
/// faute exacte que le typeur existe pour empêcher.
pub const SUBJECT_EPINGLE: &str = "https://api.exchange.coinbase.com/products/BTC-USD/ticker";

/// La devise de l'endpoint épinglé.
pub const DEVISE_DE_L_ENDPOINT: Devise = Devise::Usd;

/// La clé du membre qui porte le prix, dans le dire de cet endpoint.
///
/// Lecture **par clé retournée**, jamais par position : c'est la règle que la
/// re-mesure V2 du pool a imposée (10 §3.1, notes — « position fixe, jamais
/// “dernier élément” ; clé retournée, jamais clé demandée »), après l'anomalie
/// Bitfinex (11 champs là où le schéma en documente 10).
pub const CLE_DU_PRIX: &str = "price";

/// La clé du membre qui porte l'instant daté par la source.
pub const CLE_DE_L_INSTANT: &str = "time";

/// Type un dire brut en fait prix.
///
/// **Total** : `subject` et `dire` sont des entrées quelconques ; tout ce qui
/// n'est pas typable exactement rend un [`RefusDeTypage`] nommé.
///
/// Les contrôles, dans l'ordre — l'ordre est une décision, pas un accident :
/// un même dire peut violer plusieurs clauses et le refus rendu doit être
/// stable d'une exécution et d'une machine à l'autre.
///
/// 1. `subject` canonique au sens d'ADR-0016 C10 (prédicat du cœur) ;
/// 2. `subject` égal, octet à octet, à [`SUBJECT_EPINGLE`] ;
/// 3. le dire s'analyse en objet JSON (clés uniques, profondeur bornée) ;
/// 4. le membre `price` existe, est une **chaîne**, et type en décimale exacte ;
/// 5. le membre `time` existe, est une **chaîne**, et type en instant RFC 3339
///    UTC.
pub fn typer_dire(subject: &str, dire: &[u8]) -> Result<FaitPrix, RefusDeTypage> {
    if let Err(erreur) = subject_est_canonique(subject.as_bytes()) {
        return Err(RefusDeTypage::SubjectNonCanonique { erreur });
    }
    if subject != SUBJECT_EPINGLE {
        return Err(RefusDeTypage::SubjectNonEpingle {
            attendu: SUBJECT_EPINGLE,
        });
    }
    let racine = analyser_objet_racine(dire).map_err(|erreur| RefusDeTypage::Json { erreur })?;

    let graphie_du_prix = membre_textuel(&racine, CLE_DU_PRIX)?;
    let valeur = typer_decimale(graphie_du_prix).map_err(|erreur| RefusDeTypage::Decimale {
        cle: CLE_DU_PRIX,
        erreur,
    })?;

    let graphie_de_l_instant = membre_textuel(&racine, CLE_DE_L_INSTANT)?;
    let instant = typer_instant(graphie_de_l_instant).map_err(|erreur| RefusDeTypage::Instant {
        cle: CLE_DE_L_INSTANT,
        erreur,
    })?;

    Ok(FaitPrix {
        valeur,
        devise: DEVISE_DE_L_ENDPOINT,
        instant,
        typeur: identite(),
    })
}

/// Le membre textuel de la racine porté par `cle`, ou le refus qui le nomme.
///
/// Un membre **non** textuel est refusé, jamais converti : les prix se lisent
/// comme chaînes chez cette source, et un nombre JSON serait typé par
/// l'analyseur du consommateur — beaucoup le typent en flottant binaire.
fn membre_textuel<'racine>(
    racine: &'racine ObjetRacine,
    cle: &'static str,
) -> Result<&'racine str, RefusDeTypage> {
    match racine.membre(cle) {
        None => Err(RefusDeTypage::ChampManquant { cle }),
        Some((Valeur::Texte(graphie), _)) => Ok(graphie),
        Some((_, position)) => Err(RefusDeTypage::ChampNonTextuel { cle, position }),
    }
}
