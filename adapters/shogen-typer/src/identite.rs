//! L'**identité du typeur** — nom, version, empreinte de sa propre logique,
//! compte d'itérations.
//!
//! Rattachement (G0) : **03 §3** — « l'extraction … est le travail d'un
//! **typeur**, adapter identifié, testé jamais prouvé, dont l'identité et la
//! version figurent dans le *fait*, pas dans le témoignage » ; **08,
//! A(typer-correctness)** — « n'est jamais déchargée — bornée par tests + **identité
//! du typeur dans le fait** », « cible : tested à S3, avec **compte
//! d'itérations par typeur** » ; **ADR-0018** (l'empreinte du dépôt est
//! SHA-256, écrite au cœur, adossée aux vecteurs NIST).
//!
//! # Ce que « compte d'itérations » veut dire ici — instruction du terme
//!
//! Le registre 08 n'en donne pas la définition sur place ; le dépôt en porte
//! **une seule** glose, et c'est celle qui fait foi :
//!
//! * `docs/09-vocabulaire.md`, §« Héritées de la discipline » : « Les trois
//!   mots d'assurance — *proven / tested (avec compte d'itérations) / reviewed
//!   (qui, quand)* ». Le compte est donc l'**accompagnement obligatoire du mot
//!   `tested`** : dire « tested » sans compte est une assurance nue.
//! * `docs/10-mesures-pilotes-design.md` §8, entrée A(typer-correctness) : « Le
//!   rapport S2 publie le **compte d'exécutions de chaque décodeur** —
//!   première marche vers la cible de 08 (tested à S3, avec compte
//!   d'itérations). » Le compte d'un typeur est donc le compte
//!   **d'exécutions** du typeur par sa suite.
//!
//! D'où la définition tenue ici, et rien de plus large : **le nombre
//! d'exécutions du typeur sur le corpus de la passe** — cas réels, cas de
//! refus, et cas générés (property-based, graine déterministe). Ce n'est pas un
//! nombre de tests, pas un nombre d'assertions, pas une couverture.
//!
//! Le nombre est **déclaré ici** et **mesuré là-bas** : `tests/compte.rs`
//! exécute le corpus, compte réellement ses appels, imprime le total et
//! **échoue** si le total mesuré diffère de [`COMPTE_D_ITERATIONS`]. Un compte
//! écrit de tête ne survit pas à `cargo test`.

use shogen_core::{empreinte_en_hexadecimal, empreinte_sha256};
use std::sync::OnceLock;

/// Le nom du typeur — celui du paquet, jamais recopié à la main.
pub const NOM: &str = env!("CARGO_PKG_NAME");

/// La version du typeur — celle du manifeste, jamais recopiée à la main.
pub const VERSION: &str = env!("CARGO_PKG_VERSION");

/// Le compte d'itérations de ce typeur : nombre d'exécutions sur le corpus de
/// la passe. **Mesuré** par `tests/compte.rs`, qui échoue si ce nombre ment.
pub const COMPTE_D_ITERATIONS: u64 = 3_053;

/// Les fichiers qui **sont** la logique du typeur, dans un ordre fixe (celui
/// des chemins, trié). Embarqués à la compilation : l'empreinte porte sur ce
/// que le binaire contient, pas sur ce qu'un disque contient au moment où on
/// l'interroge. `tests/identite.rs` relit les mêmes fichiers depuis le disque
/// et compare — c'est ce qui attrape une dérive entre les deux.
pub const FICHIERS_DE_LOGIQUE: &[(&str, &str)] = &[
    ("src/decimale.rs", include_str!("decimale.rs")),
    ("src/erreur.rs", include_str!("erreur.rs")),
    ("src/fait.rs", include_str!("fait.rs")),
    ("src/identite.rs", include_str!("identite.rs")),
    ("src/instant.rs", include_str!("instant.rs")),
    ("src/json.rs", include_str!("json.rs")),
    ("src/lib.rs", include_str!("lib.rs")),
];

/// L'octet de cadrage entre les champs de l'entrée d'empreinte.
const CADRE: u8 = 0x0A;

/// L'identité d'un typeur, telle qu'un fait la porte.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct IdentiteDuTypeur {
    /// Le nom du paquet.
    pub nom: &'static str,
    /// La version du paquet.
    pub version: &'static str,
    /// L'empreinte SHA-256 de la logique, en hexadécimal minuscule.
    pub empreinte: String,
    /// Le compte d'itérations — voir [`COMPTE_D_ITERATIONS`].
    pub compte_d_iterations: u64,
}

/// L'identité de ce typeur.
pub fn identite() -> IdentiteDuTypeur {
    IdentiteDuTypeur {
        nom: NOM,
        version: VERSION,
        empreinte: empreinte_en_hexadecimal(&empreinte_de_la_logique()),
        compte_d_iterations: COMPTE_D_ITERATIONS,
    }
}

/// Les octets sur lesquels l'empreinte de la logique se calcule.
///
/// Cadrage explicite — chemin, longueur, contenu, chacun suivi d'un saut de
/// ligne : sans longueur, deux découpes différentes des mêmes fichiers
/// donneraient la même entrée, et l'empreinte cesserait d'identifier ce qu'elle
/// prétend identifier.
///
/// **Les fins de ligne sont ramenées à LF** avant le calcul. Le dépôt impose
/// déjà `* text=auto eol=lf` (`.gitattributes`), mais l'empreinte doit tenir
/// même sur une copie de travail qui aurait été extraite autrement : sinon
/// l'identité d'un typeur dépendrait du système de fichiers qui l'héberge, ce
/// qui n'a aucun sens. C'est la seule transformation de tout ce paquet, et elle
/// ne porte que sur l'entrée du calcul, jamais sur un dire ni sur un fait.
pub fn octets_de_la_logique() -> Vec<u8> {
    let mut octets = Vec::new();
    for (chemin, contenu) in FICHIERS_DE_LOGIQUE {
        let normalise: Vec<u8> = contenu
            .as_bytes()
            .iter()
            .copied()
            .filter(|octet| *octet != b'\r')
            .collect();
        octets.extend_from_slice(chemin.as_bytes());
        octets.push(CADRE);
        octets.extend_from_slice(normalise.len().to_string().as_bytes());
        octets.push(CADRE);
        octets.extend_from_slice(&normalise);
        octets.push(CADRE);
    }
    octets
}

/// L'empreinte SHA-256 de la logique du typeur, calculée une fois.
pub fn empreinte_de_la_logique() -> [u8; 32] {
    static EMPREINTE: OnceLock<[u8; 32]> = OnceLock::new();
    *EMPREINTE.get_or_init(|| empreinte_sha256(&octets_de_la_logique()))
}
