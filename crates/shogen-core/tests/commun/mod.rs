// Le témoignage canonique de référence, partagé par les suites de tests.
//
// `allow(dead_code)` : Rust compile ce module **dans chaque binaire de test**
// qui le déclare, et chacun n'en emploie qu'une partie. L'attribut ne desserre
// aucune gate ni aucun plancher (charte `shogen-devops` §2 vise le desserrage de
// gate) — il neutralise un faux positif de l'idiome `tests/commun/mod.rs`.
#![allow(dead_code)]

use shogen_core::{
    Attestor, Constat, ObservedAt, RESIDU_DE_LA_DELEGATION, Temoignage, Utterance, empreinte_sha256,
};

/// Les octets d'`utterance` du témoignage de référence.
pub const OCTETS_D_UTTERANCE: &[u8] = b"{\"price\":\"42.17\"}";
/// Les octets de preuve — **opaques** : le cœur n'en interprète aucun.
pub const OCTETS_DE_PREUVE: &[u8] = b"preuve-opaque-d'exemple";
/// Le `subject` de référence, canonique au sens d'ADR-0016.
pub const SUBJECT: &str = "https://api.example.com/v3/simple/price?ids=bitcoin";
/// Les identifiants portés — aucun ne nomme un transport réel : le cœur est sous
/// gate S-G1, et un test du cœur l'est avec lui.
pub const IDENTITE: &str = "exemple:attestateur-1";
pub const RESIDU_1: &str = "A(exemple-residu-1)";
pub const RESIDU_2: &str = "A(exemple-residu-2)";
pub const TRANSPORT: &str = "exemple-transport/1";
pub const HORLOGE: &str = "exemple:horloge-du-transport";
pub const INSTANT: u64 = 1_754_000_000;
/// L'identité du binaire compagnon, telle qu'un constat la porte.
pub const OUTIL: &str = "exemple-compagnon/1 (revision 0000000)";

/// Le témoignage canonique de référence.
pub fn reference() -> Temoignage {
    Temoignage {
        subject: String::from(SUBJECT),
        attestor: vec![Attestor {
            key: vec![0x04, 0x1a, 0x2b, 0x3c],
            identity: String::from(IDENTITE),
        }],
        residual: vec![String::from(RESIDU_1), String::from(RESIDU_2)],
        transport: String::from(TRANSPORT),
        utterance: Utterance {
            hash: empreinte_sha256(OCTETS_D_UTTERANCE),
            bytes: Some(OCTETS_D_UTTERANCE.to_vec()),
        },
        observed_at: ObservedAt {
            clock: String::from(HORLOGE),
            instant: INSTANT,
        },
        transport_proof: OCTETS_DE_PREUVE.to_vec(),
    }
}

/// Le registre publié de référence : les résidus du témoignage **et** celui de
/// la délégation, qu'ADR-0015 point 8 alinéa e impose au verdict.
pub fn registre() -> Vec<String> {
    vec![
        String::from(RESIDU_1),
        String::from(RESIDU_2),
        String::from(RESIDU_DE_LA_DELEGATION),
    ]
}

/// Le constat que le binaire compagnon rendrait sur ce témoignage.
pub fn constat() -> Constat {
    Constat {
        outil: String::from(OUTIL),
        empreinte_de_la_preuve: empreinte_sha256(OCTETS_DE_PREUVE),
        empreinte_de_l_utterance: empreinte_sha256(OCTETS_D_UTTERANCE),
    }
}
