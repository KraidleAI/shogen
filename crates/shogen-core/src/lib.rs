#![forbid(unsafe_code)]
#![deny(
    clippy::unwrap_used,
    clippy::expect_used,
    clippy::panic,
    clippy::indexing_slicing,
    clippy::arithmetic_side_effects
)]
//! Cœur de Shōgen — **pur, total, sans I/O, sans panique** (ADR-0010, point 1).
//!
//! Rattachement (G0) : ADR-0002 (CBOR déterministe), ADR-0010 (architecture),
//! ADR-0011 (tests), 12 §5 (walking skeleton).
//!
//! Ce que ce module **ne fait pas**, et qu'aucune phrase du dépôt ne doit
//! laisser croire : il ne calcule aucune statistique, ne nomme aucun transport,
//! ne lit aucune horloge, n'ouvre aucun fichier. `forbid(unsafe_code)` retire
//! la classe « sûreté mémoire » du fragment sans `unsafe` — ce qui est
//! machine-checked (Jung et al. 2018) est un langage formalisé, pas `rustc` ni
//! notre code (ADR-0009).
//!
//! # Carte des points de frontière
//!
//! Livrable exigé par ADR-0010, point 6 et §Coûts point 7 : « la **carte des
//! points de frontière** est un livrable du walking skeleton (12 §5) ; sans
//! elle, la règle se dégrade en préférence personnelle ». Meyer, p. 44 : le
//! spectre *demanding* / *tolerant* ; ici il est réparti, pas laissé au goût.
//!
//! | point d'entrée | style | précondition | ce qui l'établit |
//! |---|---|---|---|
//! | [`decoder_lot`] | **tolérant** | aucune — tout `&[u8]`, y compris hostile | lui-même : il trie sur le nombre d'entrées de la carte de tête, un fait d'octets |
//! | [`decoder_temoignage`] | **tolérant** | aucune — tout `&[u8]`, y compris hostile | lui-même : c'est l'établissement UNIQUE de la forme canonique dont dépend tout l'intérieur |
//! | [`decoder_temoignage_canonique`] | **tolérant** | aucune — tout `&[u8]`, y compris hostile | lui-même, prédicat de `subject` compris (ADR-0016 C10) |
//! | [`subject_est_canonique`] | **tolérant** | aucune — toute suite d'octets | lui-même : c'est le prédicat, il n'a pas de précondition |
//! | [`empreinte_sha256`] | **tolérant** | aucune — toute suite d'octets | totale par construction : elle ne refuse rien, elle rend un condensé |
//! | [`verifier_temoignage`] | exigeant | l'argument est un [`Temoignage`] déjà décodé, donc déjà canonique | le décodage, qui est la frontière |
//! | [`encoder_temoignage`], [`encoder_temoignage_canonique`], [`encoder_lot`] | exigeant | l'argument est une valeur déjà typée | le système de types |
//! | [`encodage_de_cle`] | exigeant | l'argument est un `&str` (donc UTF-8 valide) | le système de types |
//!
//! Tout le reste (`cbor::Lecteur` et ses opérations, `lire_texte`,
//! `lire_octets`, `ControleDeTri`, les lecteurs de sous-cartes) est **interne**
//! et écrit en style exigeant : ces fonctions supposent établie la précondition
//! posée par la frontière, et ne la revérifient pas — le double contrôle
//! défensif est refusé (ADR-0010, point 6 ; Meyer p. 41 et p. 44).
//!
//! Ce que cette carte **n'établit pas** : que le cœur ne peut pas paniquer. La
//! gate S-G3 rejette une liste de formes nommées ; l'absence de panique n'est
//! pas établie (ADR-0010, §Coûts point 6).

mod cbor;
mod empreinte;
mod erreur;
mod lot;
mod subject;
mod temoignage;
mod temoignage_canonique;
mod verification;

pub use empreinte::{OCTETS_D_EMPREINTE, empreinte_en_hexadecimal, empreinte_sha256};
pub use erreur::ErreurDecodage;
pub use lot::{Lot, decoder_lot, encoder_lot};
pub use subject::{ErreurSubject, PORT_PAR_DEFAUT, PREFIXE_CANONIQUE, subject_est_canonique};
pub use temoignage::{
    CLE_CONTENU, CLE_INSTANT, CLE_SOURCE, NOMBRE_DE_CHAMPS, ORDRE_CANONIQUE_DES_CLES,
    TemoignageTrivial, decoder_temoignage, encodage_de_cle, encoder_temoignage,
};
pub use temoignage_canonique::{
    Attestor, CLE_ATTESTOR, CLE_BYTES, CLE_CLOCK, CLE_HASH, CLE_IDENTITY, CLE_KEY, CLE_OBSERVED_AT,
    CLE_RESIDUAL, CLE_SUBJECT, CLE_TRANSPORT, CLE_TRANSPORT_PROOF, NOMBRE_DE_CHAMPS_DU_TEMOIGNAGE,
    ORDRE_CANONIQUE_DU_TEMOIGNAGE, ObservedAt, Temoignage, Utterance, decoder_temoignage_canonique,
    encoder_temoignage_canonique,
};
pub use verification::{
    Constat, ErreurVerification, RESIDU_DE_LA_DELEGATION, Verdict, verifier_temoignage,
};
