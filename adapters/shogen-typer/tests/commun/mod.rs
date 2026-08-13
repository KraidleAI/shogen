//! Le **corpus de la passe** — source unique des cas exercés par la suite.
//!
//! Toutes les suites tirent leurs cas d'ici : les assertions de variante
//! (`typage.rs`, `refus.rs`) et le compte d'itérations (`compte.rs`). Un cas
//! ajouté ou retiré change donc **à la fois** ce qui est asserté et ce qui est
//! compté — il n'y a pas deux listes qui pourraient diverger.
//!
//! `allow(dead_code)` : Rust compile ce module dans chaque binaire de test qui
//! le déclare, et chacun n'en emploie qu'une partie (même idiome et même raison
//! que `crates/shogen-core/tests/commun/mod.rs`).
#![allow(dead_code)]

use shogen_typer::{
    Devise, ErreurDecimale, ErreurInstant, ErreurJson, PROFONDEUR_MAXIMALE, RefusDeTypage,
    SUBJECT_EPINGLE,
};

/// D'où vient le dire d'un cas — la distinction est portée dans le type, pas
/// dans un commentaire : un dire construit ne doit jamais pouvoir passer pour
/// une réponse réelle.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Origine {
    /// Réponse réelle d'une source du pool S2, conservée octet pour octet.
    /// Provenance et sha256 : `tests/fixtures/PROVENANCE.md`.
    Reelle { fichier: &'static str },
    /// Dire construit pour la suite, jamais présenté comme réel.
    Construit,
}

/// Un cas que le typeur doit accepter, avec le fait attendu **en entier**.
pub struct CasAccepte {
    pub nom: &'static str,
    pub origine: Origine,
    pub subject: &'static str,
    pub dire: &'static [u8],
    pub mantisse: i128,
    pub exposant: i32,
    pub lexeme: &'static str,
    pub devise: Devise,
    pub instant: &'static str,
}

/// Un cas que le typeur doit refuser, avec **la** variante de refus attendue.
pub struct CasDeRefus {
    pub nom: &'static str,
    pub origine: Origine,
    pub subject: &'static str,
    pub dire: &'static [u8],
    pub refus: RefusDeTypage,
}

// ── Les dires réels ───────────────────────────────────────────────────────

const COINBASE_2026_08_05: &[u8] =
    include_bytes!("../fixtures/coinbase-btc-usd-ticker-2026-08-05.json");
const COINBASE_2026_08_13: &[u8] =
    include_bytes!("../fixtures/coinbase-btc-usd-ticker-2026-08-13.json");
const POOL_BINANCE: &[u8] = include_bytes!("../fixtures/pool-binance-2026-08-05.json");
const POOL_BITFINEX: &[u8] = include_bytes!("../fixtures/pool-bitfinex-2026-08-05.json");
const POOL_BITSTAMP: &[u8] = include_bytes!("../fixtures/pool-bitstamp-2026-08-05.json");
const POOL_CHAINLINK: &[u8] = include_bytes!("../fixtures/pool-chainlink-2026-08-05.json");
const POOL_COINGECKO: &[u8] = include_bytes!("../fixtures/pool-coingecko-2026-08-05.json");
const POOL_CRYPTOCOMPARE: &[u8] =
    include_bytes!("../fixtures/pool-cryptocompare-401-2026-08-05.json");
const POOL_DEFILLAMA: &[u8] = include_bytes!("../fixtures/pool-defillama-2026-08-05.json");
const POOL_GEMINI: &[u8] = include_bytes!("../fixtures/pool-gemini-2026-08-05.json");
const POOL_KRAKEN: &[u8] = include_bytes!("../fixtures/pool-kraken-2026-08-05.json");
const POOL_OKX_INDEX: &[u8] = include_bytes!("../fixtures/pool-okx-index-2026-08-05.json");
const POOL_OKX_TICKER: &[u8] = include_bytes!("../fixtures/pool-okx-ticker-2026-08-05.json");
const POOL_PYTH: &[u8] = include_bytes!("../fixtures/pool-pyth-2026-08-05.json");

/// Les cas acceptés — **tous réels**. Aucun dire construit n'est admis ici :
/// un typeur qui n'accepterait que des dires qu'on lui a écrits sur mesure
/// n'aurait rien montré.
pub fn corpus_accepte() -> Vec<CasAccepte> {
    vec![
        CasAccepte {
            nom: "coinbase réel 2026-08-05 — prix à décimales",
            origine: Origine::Reelle {
                fichier: "coinbase-btc-usd-ticker-2026-08-05.json",
            },
            subject: SUBJECT_EPINGLE,
            dire: COINBASE_2026_08_05,
            mantisse: 6_447_575,
            exposant: -2,
            lexeme: "64475.75",
            devise: Devise::Usd,
            instant: "2026-08-05T16:11:21.674372072Z",
        },
        CasAccepte {
            nom: "coinbase réel 2026-08-13 — prix entier (exposant nul)",
            origine: Origine::Reelle {
                fichier: "coinbase-btc-usd-ticker-2026-08-13.json",
            },
            subject: SUBJECT_EPINGLE,
            dire: COINBASE_2026_08_13,
            mantisse: 63_577,
            exposant: 0,
            lexeme: "63577",
            devise: Devise::Usd,
            instant: "2026-08-13T04:08:53.281522458Z",
        },
    ]
}

/// Les cas refusés — réels d'abord, construits ensuite.
pub fn corpus_de_refus() -> Vec<CasDeRefus> {
    let mut cas = corpus_de_refus_reel();
    cas.extend(corpus_de_refus_construit());
    cas
}

/// Refus sur dires **réels** : onze autres flux du pool S2, plus la réponse 401
/// réelle de CryptoCompare. Ce sont de vraies réponses de vraies sources — ce
/// que le typeur doit refuser, ce n'est pas seulement du bruit hostile, c'est
/// aussi du JSON parfaitement valide qui n'est pas le sien.
fn corpus_de_refus_reel() -> Vec<CasDeRefus> {
    let manque = |cle: &'static str| RefusDeTypage::ChampManquant { cle };
    vec![
        CasDeRefus {
            nom: "binance réel — porte price, ne porte aucun instant",
            origine: Origine::Reelle {
                fichier: "pool-binance-2026-08-05.json",
            },
            subject: SUBJECT_EPINGLE,
            dire: POOL_BINANCE,
            refus: manque("time"),
        },
        CasDeRefus {
            nom: "bitfinex réel — racine tableau (l'anomalie de forme de 10 §3.1)",
            origine: Origine::Reelle {
                fichier: "pool-bitfinex-2026-08-05.json",
            },
            subject: SUBJECT_EPINGLE,
            dire: POOL_BITFINEX,
            refus: RefusDeTypage::Json {
                erreur: ErreurJson::RacineNonObjet {
                    position: 0,
                    trouve: b'[',
                },
            },
        },
        CasDeRefus {
            nom: "bitstamp réel — le prix s'y nomme last, pas price",
            origine: Origine::Reelle {
                fichier: "pool-bitstamp-2026-08-05.json",
            },
            subject: SUBJECT_EPINGLE,
            dire: POOL_BITSTAMP,
            refus: manque("price"),
        },
        CasDeRefus {
            nom: "chainlink réel — réponse JSON-RPC, aucun prix nommé",
            origine: Origine::Reelle {
                fichier: "pool-chainlink-2026-08-05.json",
            },
            subject: SUBJECT_EPINGLE,
            dire: POOL_CHAINLINK,
            refus: manque("price"),
        },
        CasDeRefus {
            nom: "coingecko réel — le prix est imbriqué, jamais à la racine",
            origine: Origine::Reelle {
                fichier: "pool-coingecko-2026-08-05.json",
            },
            subject: SUBJECT_EPINGLE,
            dire: POOL_COINGECKO,
            refus: manque("price"),
        },
        CasDeRefus {
            nom: "cryptocompare réel — corps d'erreur 401 (source écartée du pool)",
            origine: Origine::Reelle {
                fichier: "pool-cryptocompare-401-2026-08-05.json",
            },
            subject: SUBJECT_EPINGLE,
            dire: POOL_CRYPTOCOMPARE,
            refus: manque("price"),
        },
        CasDeRefus {
            nom: "defillama réel — prix imbriqué sous coins",
            origine: Origine::Reelle {
                fichier: "pool-defillama-2026-08-05.json",
            },
            subject: SUBJECT_EPINGLE,
            dire: POOL_DEFILLAMA,
            refus: manque("price"),
        },
        CasDeRefus {
            nom: "gemini réel — le prix s'y nomme last",
            origine: Origine::Reelle {
                fichier: "pool-gemini-2026-08-05.json",
            },
            subject: SUBJECT_EPINGLE,
            dire: POOL_GEMINI,
            refus: manque("price"),
        },
        CasDeRefus {
            nom: "kraken réel — prix sous la clé retournée XXBTZUSD",
            origine: Origine::Reelle {
                fichier: "pool-kraken-2026-08-05.json",
            },
            subject: SUBJECT_EPINGLE,
            dire: POOL_KRAKEN,
            refus: manque("price"),
        },
        CasDeRefus {
            nom: "okx indice réel — enveloppe code/msg/data",
            origine: Origine::Reelle {
                fichier: "pool-okx-index-2026-08-05.json",
            },
            subject: SUBJECT_EPINGLE,
            dire: POOL_OKX_INDEX,
            refus: manque("price"),
        },
        CasDeRefus {
            nom: "okx ticker réel — enveloppe code/msg/data",
            origine: Origine::Reelle {
                fichier: "pool-okx-ticker-2026-08-05.json",
            },
            subject: SUBJECT_EPINGLE,
            dire: POOL_OKX_TICKER,
            refus: manque("price"),
        },
        CasDeRefus {
            nom: "pyth réel — mantisse et exposant séparés, sous parsed",
            origine: Origine::Reelle {
                fichier: "pool-pyth-2026-08-05.json",
            },
            subject: SUBJECT_EPINGLE,
            dire: POOL_PYTH,
            refus: manque("price"),
        },
        CasDeRefus {
            nom: "subject réel d'une autre source du pool (binance) — canonique, non épinglé",
            origine: Origine::Reelle {
                fichier: "coinbase-btc-usd-ticker-2026-08-05.json",
            },
            subject: "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",
            dire: COINBASE_2026_08_05,
            refus: RefusDeTypage::SubjectNonEpingle {
                attendu: SUBJECT_EPINGLE,
            },
        },
    ]
}

/// Refus sur dires **construits** — chacun exerce une clause nommée.
fn corpus_de_refus_construit() -> Vec<CasDeRefus> {
    let json = |erreur: ErreurJson| RefusDeTypage::Json { erreur };
    let decimale = |erreur: ErreurDecimale| RefusDeTypage::Decimale {
        cle: "price",
        erreur,
    };
    let instant = |erreur: ErreurInstant| RefusDeTypage::Instant {
        cle: "time",
        erreur,
    };
    vec![
        // ── subject ──────────────────────────────────────────────────────
        CasDeRefus {
            nom: "subject en http — prédicat du cœur, C2",
            origine: Origine::Construit,
            subject: "http://api.exchange.coinbase.com/products/BTC-USD/ticker",
            dire: COINBASE_2026_08_05,
            refus: RefusDeTypage::SubjectNonCanonique {
                erreur: shogen_core::ErreurSubject::SchemeNonHttps { position: 0 },
            },
        },
        CasDeRefus {
            nom: "subject avec port 443 explicite — C5",
            origine: Origine::Construit,
            subject: "https://api.exchange.coinbase.com:443/products/BTC-USD/ticker",
            dire: COINBASE_2026_08_05,
            refus: RefusDeTypage::SubjectNonCanonique {
                erreur: shogen_core::ErreurSubject::PortParDefautExplicite { position: 34 },
            },
        },
        // ── grammaire JSON ───────────────────────────────────────────────
        CasDeRefus {
            nom: "dire vide",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"",
            refus: json(ErreurJson::EntreeVide),
        },
        CasDeRefus {
            nom: "objet non refermé",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"price\":\"1.00\"",
            refus: json(ErreurJson::FinPrematuree { position: 15 }),
        },
        CasDeRefus {
            nom: "octets non UTF-8 dans le dire",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"price\":\"1.\xff0\"}",
            refus: json(ErreurJson::EntreeNonUtf8 { position: 12 }),
        },
        CasDeRefus {
            nom: "clé dupliquée à la racine — RFC 8259 §4",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"price\":\"1.00\",\"price\":\"2.00\",\"time\":\"2026-08-05T16:11:21Z\"}",
            refus: json(ErreurJson::CleDupliquee {
                position: 16,
                cle: String::from("price"),
            }),
        },
        CasDeRefus {
            nom: "clé dupliquée dans un objet imbriqué",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"volume\":{\"a\":1,\"a\":2},\"price\":\"1.00\",\"time\":\"2026-08-05T16:11:21Z\"}",
            refus: json(ErreurJson::CleDupliquee {
                position: 17,
                cle: String::from("a"),
            }),
        },
        CasDeRefus {
            nom: "caractère de contrôle non échappé — RFC 8259 §7",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"price\":\"1.\n00\"}",
            refus: json(ErreurJson::CaractereDeControle {
                position: 12,
                octet: b'\n',
            }),
        },
        CasDeRefus {
            nom: "échappement inconnu",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"price\":\"1\\q00\"}",
            refus: json(ErreurJson::EchappementInconnu {
                position: 12,
                octet: b'q',
            }),
        },
        CasDeRefus {
            nom: "demi-substitut UTF-16 orphelin",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"price\":\"\\ud83d\"}",
            refus: json(ErreurJson::SubstitutOrphelin {
                position: 16,
                unite: 0xD83D,
            }),
        },
        CasDeRefus {
            nom: "échappement \\u tronqué",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"price\":\"\\u00\"}",
            refus: json(ErreurJson::EchappementUnicodeMalForme { position: 12 }),
        },
        CasDeRefus {
            nom: "nombre JSON à zéro de tête",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"trade_id\":01}",
            refus: json(ErreurJson::OctetInattendu {
                position: 13,
                attendu: b'}',
                trouve: b'1',
            }),
        },
        CasDeRefus {
            nom: "littéral inconnu",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"price\":tru}",
            refus: json(ErreurJson::LitteralInconnu { position: 9 }),
        },
        CasDeRefus {
            nom: "octets résiduels après l'objet racine",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"price\":\"1.00\"}{}",
            refus: json(ErreurJson::OctetsResiduels {
                position: 16,
                restants: 2,
            }),
        },
        CasDeRefus {
            nom: "imbrication au-delà de la borne",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: DIRE_TROP_PROFOND,
            refus: json(ErreurJson::ProfondeurExcessive {
                position: 36,
                profondeur_maximale: PROFONDEUR_MAXIMALE,
            }),
        },
        // ── champs ───────────────────────────────────────────────────────
        CasDeRefus {
            nom: "price en NOMBRE JSON — refusé, jamais converti",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"price\":64475.75,\"time\":\"2026-08-05T16:11:21Z\"}",
            refus: RefusDeTypage::ChampNonTextuel {
                cle: "price",
                position: 9,
            },
        },
        CasDeRefus {
            nom: "time en nombre JSON (époque, forme Bitstamp)",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"price\":\"1.00\",\"time\":1785946282}",
            refus: RefusDeTypage::ChampNonTextuel {
                cle: "time",
                position: 23,
            },
        },
        // ── grammaire décimale ───────────────────────────────────────────
        CasDeRefus {
            nom: "notation scientifique",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"price\":\"6.447575e4\",\"time\":\"2026-08-05T16:11:21Z\"}",
            refus: decimale(ErreurDecimale::NotationScientifique { position: 8 }),
        },
        // Un lexème non numérique porteur d'un « e » n'est PAS de la notation
        // scientifique : le diagnostic doit dire vrai (revue G2 vague 1 —
        // l'ancien balayage global rendait NotationScientifique sur
        // « unavailable », un diagnostic qui apprenait quelque chose de faux).
        CasDeRefus {
            nom: "lexème non numérique porteur d'un e",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"price\":\"unavailable\",\"time\":\"2026-08-05T16:11:21Z\"}",
            refus: decimale(ErreurDecimale::ChiffreAttendu { position: 0 }),
        },
        CasDeRefus {
            nom: "séparateur de milliers",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"price\":\"64,475.75\",\"time\":\"2026-08-05T16:11:21Z\"}",
            refus: decimale(ErreurDecimale::OctetHorsForme {
                position: 2,
                octet: b',',
            }),
        },
        CasDeRefus {
            nom: "prix vide",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"price\":\"\",\"time\":\"2026-08-05T16:11:21Z\"}",
            refus: decimale(ErreurDecimale::Vide),
        },
        CasDeRefus {
            nom: "blanc de tête",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"price\":\" 64475.75\",\"time\":\"2026-08-05T16:11:21Z\"}",
            refus: decimale(ErreurDecimale::ChiffreAttendu { position: 0 }),
        },
        CasDeRefus {
            nom: "signe plus explicite",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"price\":\"+64475.75\",\"time\":\"2026-08-05T16:11:21Z\"}",
            refus: decimale(ErreurDecimale::ChiffreAttendu { position: 0 }),
        },
        CasDeRefus {
            nom: "zéro de tête",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"price\":\"064475.75\",\"time\":\"2026-08-05T16:11:21Z\"}",
            refus: decimale(ErreurDecimale::ZeroDeTete { position: 0 }),
        },
        CasDeRefus {
            nom: "point décimal sans fraction",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"price\":\"64475.\",\"time\":\"2026-08-05T16:11:21Z\"}",
            refus: decimale(ErreurDecimale::ChiffreAttendu { position: 6 }),
        },
        CasDeRefus {
            nom: "second point décimal",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"price\":\"64475.75.5\",\"time\":\"2026-08-05T16:11:21Z\"}",
            refus: decimale(ErreurDecimale::PointDecimalRepete { position: 8 }),
        },
        CasDeRefus {
            nom: "zéro signé",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"price\":\"-0.00\",\"time\":\"2026-08-05T16:11:21Z\"}",
            refus: decimale(ErreurDecimale::ZeroSigne { position: 0 }),
        },
        CasDeRefus {
            nom: "perte de précision — quarante chiffres significatifs",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"price\":\"1234567890123456789012345678901234567890.5\",\"time\":\"2026-08-05T16:11:21Z\"}",
            refus: decimale(ErreurDecimale::CapaciteDeMantisseDepassee { chiffres: 40 }),
        },
        CasDeRefus {
            nom: "graphie non numérique",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"price\":\"NaN\",\"time\":\"2026-08-05T16:11:21Z\"}",
            refus: decimale(ErreurDecimale::ChiffreAttendu { position: 0 }),
        },
        // ── grammaire d'instant ──────────────────────────────────────────
        CasDeRefus {
            nom: "instant sans décalage",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"price\":\"1.00\",\"time\":\"2026-08-05T16:11:21\"}",
            refus: instant(ErreurInstant::FinPrematuree { position: 19 }),
        },
        CasDeRefus {
            nom: "instant à décalage non UTC",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"price\":\"1.00\",\"time\":\"2026-08-05T16:11:21+02:00\"}",
            refus: instant(ErreurInstant::DecalageNonUtc { position: 19 }),
        },
        CasDeRefus {
            nom: "séparateur T en minuscule",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"price\":\"1.00\",\"time\":\"2026-08-05t16:11:21Z\"}",
            refus: instant(ErreurInstant::OctetInattendu {
                position: 10,
                attendu: b'T',
                trouve: b't',
            }),
        },
        CasDeRefus {
            nom: "mois hors bornes",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"price\":\"1.00\",\"time\":\"2026-13-05T16:11:21Z\"}",
            refus: instant(ErreurInstant::ChampHorsBornes {
                champ: "date-month",
                valeur: 13,
            }),
        },
        CasDeRefus {
            nom: "30 février — RFC 3339 §5.7",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"price\":\"1.00\",\"time\":\"2026-02-30T16:11:21Z\"}",
            refus: instant(ErreurInstant::ChampHorsBornes {
                champ: "date-mday",
                valeur: 30,
            }),
        },
        CasDeRefus {
            nom: "29 février d'une année non bissextile",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"price\":\"1.00\",\"time\":\"2026-02-29T16:11:21Z\"}",
            refus: instant(ErreurInstant::ChampHorsBornes {
                champ: "date-mday",
                valeur: 29,
            }),
        },
        CasDeRefus {
            nom: "heure 24",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"price\":\"1.00\",\"time\":\"2026-08-05T24:11:21Z\"}",
            refus: instant(ErreurInstant::ChampHorsBornes {
                champ: "time-hour",
                valeur: 24,
            }),
        },
        CasDeRefus {
            nom: "fraction de seconde annoncée puis vide",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"price\":\"1.00\",\"time\":\"2026-08-05T16:11:21.Z\"}",
            refus: instant(ErreurInstant::FractionVide { position: 20 }),
        },
        CasDeRefus {
            nom: "octets après le Z",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"price\":\"1.00\",\"time\":\"2026-08-05T16:11:21Zx\"}",
            refus: instant(ErreurInstant::OctetsResiduels {
                position: 20,
                restants: 1,
            }),
        },
        CasDeRefus {
            nom: "instant en époque (forme Bitstamp/Gemini) donné comme chaîne",
            origine: Origine::Construit,
            subject: SUBJECT_EPINGLE,
            dire: b"{\"price\":\"1.00\",\"time\":\"1785946282\"}",
            refus: instant(ErreurInstant::FinPrematuree { position: 10 }),
        },
    ]
}

/// Un dire dont l'imbrication dépasse [`PROFONDEUR_MAXIMALE`] : 33 tableaux.
const DIRE_TROP_PROFOND: &[u8] =
    b"{\"a\":[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]}";

/// Le nombre de cas générés par chacune des trois propriétés.
///
/// Seuil 5 d'ADR-0011 (candidat) : ≥ 1 000 cas par propriété en CI. Le typeur
/// est un adapter, pas le cœur — ADR-0011 point 2 vise le cœur pur ; le seuil
/// est repris ici parce qu'il est le seuil du dépôt, pas parce qu'il serait dû.
pub const CAS_PAR_PROPRIETE: u32 = 1_000;

/// Le nombre de propriétés exercées.
pub const NOMBRE_DE_PROPRIETES: u32 = 3;

// ── Les générateurs des propriétés ────────────────────────────────────────
//
// Ils vivent ici, et non dans `proprietes.rs`, parce que `compte.rs` exécute
// exactement les mêmes cas pour les compter : deux jeux de générateurs
// pourraient diverger, un seul ne le peut pas.

use proptest::prelude::Strategy;
use proptest::test_runner::{Config, RngAlgorithm, TestRng, TestRunner};

/// L'exécuteur des propriétés — graine **déterministe** : la même commande
/// rejoue les mêmes cas, sur Windows comme sur Linux (ADR-0011 point 2,
/// obligation 1). La persistance de fichier de régression est désactivée
/// exprès : un fichier d'état caché serait une seconde source de vérité.
pub fn executeur() -> TestRunner {
    let configuration = Config {
        cases: CAS_PAR_PROPRIETE,
        failure_persistence: None,
        ..Config::default()
    };
    TestRunner::new_with_rng(
        configuration,
        TestRng::deterministic_rng(RngAlgorithm::ChaCha),
    )
}

/// Des octets quelconques — y compris hostiles, y compris non UTF-8.
pub fn strategie_octets() -> impl Strategy<Value = Vec<u8>> {
    proptest::collection::vec(proptest::prelude::any::<u8>(), 0..96)
}

/// Une graphie décimale **admissible** : signe, partie entière sans zéro de
/// tête, fraction facultative. Les longueurs sont bornées bien en deçà de la
/// capacité de la mantisse : cette propriété teste la fidélité, pas la borne.
pub fn strategie_lexeme_decimal() -> impl Strategy<Value = String> {
    (
        proptest::bool::ANY,
        proptest::bool::ANY,
        1usize..10,
        proptest::collection::vec(0u8..10, 0..18),
        proptest::collection::vec(0u8..10, 0..18),
    )
        .prop_map(|(negative, zero_entier, tete, suite, fraction)| {
            let mut entiere = String::new();
            if zero_entier {
                entiere.push('0');
            } else {
                entiere.push(char::from(
                    b'0'.saturating_add(u8::try_from(tete).unwrap_or(1)),
                ));
                for chiffre in &suite {
                    entiere.push(char::from(b'0'.saturating_add(*chiffre)));
                }
            }
            let mut decimales = String::new();
            for chiffre in &fraction {
                decimales.push(char::from(b'0'.saturating_add(*chiffre)));
            }
            let nulle = entiere.chars().all(|c| c == '0') && decimales.chars().all(|c| c == '0');
            let mut graphie = String::new();
            // Le zéro signé est hors grammaire (ErreurDecimale::ZeroSigne) :
            // cette stratégie génère des graphies ADMISSIBLES, elle ne le
            // produit donc pas.
            if negative && !nulle {
                graphie.push('-');
            }
            graphie.push_str(&entiere);
            if !decimales.is_empty() {
                graphie.push('.');
                graphie.push_str(&decimales);
            }
            graphie
        })
}

/// L'alphabet des graphies hostiles : tout ce qui ressemble à un nombre sans
/// forcément en être un. Aucun `"` ni `\` : le dire construit autour reste du
/// JSON bien formé, et c'est bien la grammaire décimale qui est exercée.
const ALPHABET_HOSTILE: [char; 12] = ['0', '1', '9', '.', '-', '+', 'e', 'E', ',', ' ', '_', 'N'];

/// Une graphie quelconque sur l'alphabet hostile.
pub fn strategie_graphie_hostile() -> impl Strategy<Value = String> {
    proptest::collection::vec(0usize..ALPHABET_HOSTILE.len(), 0..14).prop_map(|indices| {
        indices
            .into_iter()
            .map(|index| ALPHABET_HOSTILE.get(index).copied().unwrap_or('0'))
            .collect()
    })
}

/// Un dire de la forme de l'endpoint épinglé, portant la graphie donnée.
pub fn dire_construit(prix: &str) -> Vec<u8> {
    let mut dire = String::from("{\"price\":\"");
    dire.push_str(prix);
    dire.push_str("\",\"time\":\"2026-08-05T16:11:21.674372072Z\"}");
    dire.into_bytes()
}
