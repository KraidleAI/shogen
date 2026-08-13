//! **L'analyseur du constat** — le contrat figé d'ADR-0015 point 13, lu à la
//! main, `no_std`, sans aucune dépendance.
//!
//! # Ce que ce module lit, et pourquoi il ne lit rien d'autre
//!
//! ADR-0015 point 13 fige le constat du binaire compagnon : **une ligne JSON à
//! clés triées**, dix-huit clés (`version_du_constat` comprise — compté sur la
//! pièce, `len()` de l'objet du constat réel = 18), et « toute évolution passe
//! par incrément de `version_du_constat` porté par amendement ». La même phrase
//! dit à qui ce module obéit : « le chantier vérificateur (vague 2) s'adosse à
//! **ce contrat**, pas au code du compagnon ».
//!
//! Le sous-ensemble est donc étroit par décision, pas par paresse : un objet
//! plat, des chaînes et des entiers non signés, des clés connues et triées. Tout
//! le reste de JSON — imbrication, tableaux, échappements, nombres à virgule ou
//! négatifs, espaces de mise en forme — est **refusé, jamais normalisé**. C'est
//! la posture déjà codée pour le CBOR (`temoignage.rs` : « un encodage valide
//! mais non canonique est refusé, pas normalisé ») et pour `subject`
//! (ADR-0016 C0), transposée au constat : deux graphies d'un même constat
//! seraient deux constats, et un analyseur qui les réconcilie devrait être cru
//! sur sa réconciliation.
//!
//! **Aucune dépendance nouvelle.** ADR-0015 point 6 : le vérificateur « reste à
//! zéro dépendance tierce » ; gate S-G2. Un analyseur JSON de l'écosystème
//! coûterait cette propriété pour un objet plat de dix-huit clés.
//!
//! # Les refus sont nommés et positionnés
//!
//! Au patron d'`ErreurDecodage` du cœur : chaque variante dit **quoi**, et porte
//! les valeurs qui l'ont produite. Un refus se diagnostique sans journal.
//!
//! # Le tri des clés porte deux exigences à la fois
//!
//! Les clés doivent être **strictement croissantes** en ordre d'octets. Ce
//! contrôle unique tient le « clés triées » du contrat **et** le refus de clé
//! répétée (une clé égale à la précédente n'est pas strictement croissante) —
//! trouvaille F7 de la revue G2 de phase C, démontrée : l'ordre des lignes
//! changeait le verdict. Les deux cas se distinguent quand même en variante,
//! parce qu'ils ne se diagnostiquent pas pareil.
//!
//! # Ce que l'analyse contrôle et ne transmet pas
//!
//! Six des dix-huit clés alimentent les contrôles d'ADR-0015 point 8 et
//! franchissent la frontière du cœur (voir `shogen_core::Constat`). Les douze
//! autres sont **contrôlées ici** — présence, type, forme, et pour trois d'entre
//! elles une valeur : `version_du_constat` vaut 1, `verdict` porte la valeur de
//! succès du contrat, et les longueurs de transcript sont égales dans chaque
//! sens. Cette dernière égalité est la **pré-condition de (b)** qu'ADR-0015
//! point 13 écrit noir sur blanc (« divergence authentifié/longueur = REFUS du
//! compagnon ») : la re-contrôler ici refuse un constat que le contrat déclare
//! impossible, au lieu de le croire sur parole.

use alloc::borrow::ToOwned;
use alloc::format;
use alloc::string::String;
use alloc::vec::Vec;

use shogen_core::{Constat, OCTETS_D_EMPREINTE};

/// Les dix-huit clés du contrat, **dans l'ordre trié** qu'exige ADR-0015
/// point 13 — l'ordre de ce tableau EST l'ordre attendu, et le contrôle de tri
/// n'en lit pas d'autre.
pub const CLES_DU_CONSTAT: [&str; 18] = [
    "attestor_cle_algorithme",
    "attestor_cle_hex",
    "connection_info_time",
    "connection_info_version_tls",
    "empreinte_presentation_sha256",
    "empreinte_recv_revele_sha256",
    "empreinte_sent_revele_sha256",
    "octets_presentation",
    "revision_amont",
    "server_name",
    "transcript_recv_authentifie",
    "transcript_recv_longueur",
    "transcript_recv_longueur_attestee",
    "transcript_sent_authentifie",
    "transcript_sent_longueur",
    "transcript_sent_longueur_attestee",
    "verdict",
    "version_du_constat",
];

/// La version du contrat que cet analyseur lit — et la seule.
pub const VERSION_DU_CONSTAT: u64 = 1;

/// La valeur de `verdict` qu'un constat de succès porte — **figée au contrat**
/// par ADR-0015 point 19 (adjudication R-26 du 2026-08-13).
///
/// Le point 13 ne figeait que les dix-huit **clés**, laissant ce jeton hors de
/// la règle d'évolution : un amont qui l'aurait renommé aurait cassé cet
/// analyseur sans qu'aucun incrément de `version_du_constat` ne le signale. Le
/// point 19 l'y fait entrer — tout changement du jeton amont force
/// l'incrément, comme les clés.
///
/// Elle nomme **un calcul qui a rendu `Ok`**, jamais une donnée vraie : c'est la
/// lecture qu'impose `docs/09-vocabulaire.md` (« vérifier une signature =
/// calcul, licite ; donnée vérifiée = surclamation, interdit »).
pub const VERDICT_DE_SUCCES: &str = "presentation_verifiee";

/// Le séparateur de la clé épinglée : la clé du contrôle s'écrit
/// `<algorithme> <chiffres hexadécimaux>`.
///
/// **Convention d'écriture, portée aux deux bouts** : l'adapter qui construit le
/// témoignage épingle ces octets-là dans `attestor.key`, et cet analyseur les
/// recompose depuis les deux clés du constat. Le cœur, lui, ne fait qu'une
/// égalité d'octets et n'a pas à connaître cette convention (ADR-0001).
/// Pourquoi l'algorithme entre dans les octets épinglés : sans lui, deux
/// algorithmes différents pourraient présenter les mêmes chiffres et l'épinglage
/// ne dirait plus contre quoi le contrôle a été conduit — ADR-0015 point 8
/// alinéa (f) demande « l'identité de la clé », pas ses seuls chiffres.
pub const SEPARATEUR_DE_CLE: char = ' ';

/// Le refus d'un constat — nommé, positionné, et porteur de ce qui l'a produit.
///
/// `#[non_exhaustive]` au patron des erreurs du cœur : une variante nouvelle ne
/// doit pas tomber dans un fourre-tout chez un appelant tiers.
#[derive(Debug, Clone, PartialEq, Eq)]
#[non_exhaustive]
pub enum ErreurConstat {
    /// Le constat s'est arrêté avant sa fin.
    FinPrematuree {
        position: usize,
        attendu: &'static str,
    },
    /// Un octet n'est pas celui que la grammaire attend à cette position.
    CaractereInattendu {
        position: usize,
        trouve: u8,
        attendu: &'static str,
    },
    /// Un octet d'espacement dans l'objet : la ligne du contrat n'en porte
    /// aucun, et l'analyseur ne met rien en forme (il refuse).
    EspaceInterdit { position: usize },
    /// Un octet hors US-ASCII : le contrat n'en porte aucun, et une comparaison
    /// qui dépendrait d'une table Unicode versionnée ne serait pas recalculable
    /// hors ligne (même motif qu'ADR-0016 C3).
    OctetNonAscii { position: usize, octet: u8 },
    /// Un échappement JSON (`\`) : refusé plutôt qu'interprété — aucune valeur
    /// du contrat n'en a besoin, et un décodeur d'échappements est une surface
    /// de plus dans l'artefact de confiance.
    EchappementInterdit { position: usize },
    /// Une clé que le contrat ne nomme pas.
    CleInconnue { position: usize, cle: String },
    /// Une clé répétée — trouvaille F7 : l'ordre ne change jamais le verdict.
    CleRepetee { position: usize, cle: String },
    /// Deux clés dans le désordre : le contrat les veut triées.
    CleNonTriee {
        position: usize,
        precedente: String,
        cle: String,
    },
    /// Une clé du contrat manque.
    CleManquante { cle: &'static str },
    /// La valeur n'est pas du type que le contrat lui donne.
    TypeInattendu {
        cle: &'static str,
        attendu: &'static str,
    },
    /// Un entier hors forme canonique : vide, à zéro de tête, ou hors `u64`.
    EntierNonCanonique { position: usize },
    /// `version_du_constat` n'est pas celle que cet analyseur lit.
    VersionInattendue { attendue: u64, trouvee: u64 },
    /// Un chiffre hexadécimal fautif — majuscules comprises : le contrat en
    /// écrit une seule graphie, et deux graphies d'un même constat seraient deux
    /// constats (posture d'ADR-0016 C0, transposée).
    HexadecimalInvalide { cle: &'static str, octet: u8 },
    /// Une longueur hexadécimale fausse.
    LongueurHexadecimaleInvalide {
        cle: &'static str,
        attendue_en_octets: Option<usize>,
        trouvee_en_chiffres: usize,
    },
    /// Une valeur vide là où le contrat exige une identité.
    ValeurVide { cle: &'static str },
    /// L'algorithme de la clé porte le séparateur de la convention d'épinglage :
    /// les octets épinglés cesseraient d'être décomposables sans ambiguïté.
    AlgorithmeAmbigu { cle: &'static str },
    /// Le constat ne porte pas la valeur de succès : le contrôle délégué n'a pas
    /// rendu `Ok`, et un verdict bâti dessus dirait le contraire de la pièce.
    VerdictSansSucces { trouve: String },
    /// Les trois longueurs d'un sens divergent — pré-condition de (b) rompue
    /// (ADR-0015 point 13).
    LongueursIncoherentes {
        sens: &'static str,
        longueur: u64,
        authentifie: u64,
        attestee: u64,
    },
    /// Des octets après l'objet : une ligne, un constat.
    OctetsResiduels { position: usize, restants: usize },
}

impl core::fmt::Display for ErreurConstat {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        match self {
            Self::FinPrematuree { position, attendu } => write!(
                f,
                "constat mal formé : fin prématurée à l'octet {position} — {attendu} attendu"
            ),
            Self::CaractereInattendu {
                position,
                trouve,
                attendu,
            } => write!(
                f,
                "constat mal formé : octet {trouve:#04x} à la position {position} — {attendu} attendu"
            ),
            Self::EspaceInterdit { position } => write!(
                f,
                "constat mal formé : espacement à l'octet {position} — le contrat d'ADR-0015 point 13 est une ligne sans mise en forme, refusée plutôt que normalisée"
            ),
            Self::OctetNonAscii { position, octet } => write!(
                f,
                "constat mal formé : octet non US-ASCII {octet:#04x} à la position {position}"
            ),
            Self::EchappementInterdit { position } => write!(
                f,
                "constat mal formé : échappement à l'octet {position} — aucune valeur du contrat n'en porte, l'analyseur refuse au lieu d'interpréter"
            ),
            Self::CleInconnue { position, cle } => write!(
                f,
                "constat mal formé : clé inconnue « {cle} » à l'octet {position} — le contrat en fige dix-huit"
            ),
            Self::CleRepetee { position, cle } => write!(
                f,
                "constat mal formé : clé répétée « {cle} » à l'octet {position} — l'ordre des clés ne change jamais le verdict"
            ),
            Self::CleNonTriee {
                position,
                precedente,
                cle,
            } => write!(
                f,
                "constat mal formé : clés non triées à l'octet {position} — « {cle} » après « {precedente} »"
            ),
            Self::CleManquante { cle } => write!(
                f,
                "constat mal formé : clé « {cle} » absente — un constat incomplet n'est pas un constat"
            ),
            Self::TypeInattendu { cle, attendu } => {
                write!(f, "constat mal formé : « {cle} » n'est pas {attendu}")
            }
            Self::EntierNonCanonique { position } => write!(
                f,
                "constat mal formé : entier hors forme canonique à l'octet {position} — zéro de tête, ou hors de la plage d'un entier de 64 bits"
            ),
            Self::VersionInattendue { attendue, trouvee } => write!(
                f,
                "constat mal formé : version_du_constat {trouvee}, {attendue} attendue — toute évolution du contrat passe par amendement d'ADR-0015 point 13"
            ),
            Self::HexadecimalInvalide { cle, octet } => write!(
                f,
                "constat mal formé : « {cle} » porte l'octet {octet:#04x}, chiffre hexadécimal minuscule attendu"
            ),
            Self::LongueurHexadecimaleInvalide {
                cle,
                attendue_en_octets,
                trouvee_en_chiffres,
            } => match attendue_en_octets {
                Some(attendue) => write!(
                    f,
                    "constat mal formé : « {cle} » porte {trouvee_en_chiffres} chiffre(s), {attendue} octet(s) attendus"
                ),
                None => write!(
                    f,
                    "constat mal formé : « {cle} » porte {trouvee_en_chiffres} chiffre(s) — un nombre pair et non nul est attendu"
                ),
            },
            Self::ValeurVide { cle } => write!(
                f,
                "constat mal formé : « {cle} » vide — ce qui se nomme dans un verdict ne peut pas être vide"
            ),
            Self::AlgorithmeAmbigu { cle } => write!(
                f,
                "constat mal formé : « {cle} » porte le séparateur de la convention d'épinglage — la clé épinglée cesserait d'être décomposable sans ambiguïté"
            ),
            Self::VerdictSansSucces { trouve } => write!(
                f,
                "constat sans succès : verdict « {trouve} », « {VERDICT_DE_SUCCES} » attendu — le contrôle délégué n'a pas rendu ce que le contrat appelle un succès"
            ),
            Self::LongueursIncoherentes {
                sens,
                longueur,
                authentifie,
                attestee,
            } => write!(
                f,
                "constat incohérent (sens {sens}) : longueur {longueur}, authentifié {authentifie}, attesté {attestee} — la pré-condition du contrôle (b) est rompue (ADR-0015 point 13)"
            ),
            Self::OctetsResiduels { position, restants } => write!(
                f,
                "constat mal formé : {restants} octet(s) résiduels à partir de la position {position} — le contrat est UNE ligne"
            ),
        }
    }
}

impl core::error::Error for ErreurConstat {}

/// Une valeur du sous-ensemble : une chaîne, ou un entier non signé.
#[derive(Debug, Clone, PartialEq, Eq)]
enum Valeur {
    Texte(String),
    Entier(u64),
}

/// Le lecteur — une position dans les octets, et rien d'autre.
///
/// Aucun opérateur arithmétique nu (`clippy::arithmetic_side_effects` est
/// `deny` sur cette bibliothèque) : les avancées passent par `saturating_add`,
/// dont le débordement produirait une position figée et donc un refus, jamais
/// une lecture hors bornes.
struct Lecteur<'a> {
    octets: &'a [u8],
    position: usize,
}

impl<'a> Lecteur<'a> {
    fn nouveau(octets: &'a [u8]) -> Self {
        Self {
            octets,
            position: 0,
        }
    }

    fn regarder(&self) -> Option<u8> {
        self.octets.get(self.position).copied()
    }

    fn avancer(&mut self) {
        self.position = self.position.saturating_add(1);
    }

    fn exiger(&mut self, attendu_octet: u8, attendu: &'static str) -> Result<(), ErreurConstat> {
        match self.regarder() {
            Some(octet) if octet == attendu_octet => {
                self.avancer();
                Ok(())
            }
            Some(octet) => Err(ErreurConstat::CaractereInattendu {
                position: self.position,
                trouve: octet,
                attendu,
            }),
            None => Err(ErreurConstat::FinPrematuree {
                position: self.position,
                attendu,
            }),
        }
    }
}

/// Analyse le constat du binaire compagnon — **le point de frontière** de ce
/// module, style *tolérant* : aucune précondition, tout `&str` y compris
/// hostile.
///
/// Ce qu'elle rend est la **projection** que les contrôles du cœur consomment
/// (`shogen_core::Constat`) ; ce qu'elle a contrôlé est le contrat entier.
pub fn analyser_constat(texte: &str) -> Result<Constat, ErreurConstat> {
    // Les seuls octets d'espacement admis sont ceux qui entourent la ligne : un
    // fichier finit par une fin de ligne, et refuser cela n'apprendrait rien à
    // personne. À l'intérieur de l'objet, aucun.
    let ligne = texte.trim_matches(|caractere: char| caractere.is_ascii_whitespace());
    let mut lecteur = Lecteur::nouveau(ligne.as_bytes());

    lecteur.exiger(b'{', "« { » d'ouverture d'objet")?;

    let mut valeurs: Vec<(&'static str, Valeur)> = Vec::new();
    let mut precedente: Option<&'static str> = None;

    loop {
        let position_cle = lecteur.position;
        let cle = lire_texte(&mut lecteur)?;
        let cle = reconnaitre_cle(&cle, position_cle)?;
        controler_le_tri(precedente, cle, position_cle)?;
        precedente = Some(cle);

        lecteur.exiger(b':', "« : » entre la clé et sa valeur")?;
        let valeur = lire_valeur(&mut lecteur)?;
        valeurs.push((cle, valeur));

        match lecteur.regarder() {
            Some(b',') => lecteur.avancer(),
            Some(b'}') => {
                lecteur.avancer();
                break;
            }
            Some(octet) => {
                return Err(ErreurConstat::CaractereInattendu {
                    position: lecteur.position,
                    trouve: octet,
                    attendu: "« , » ou « } »",
                });
            }
            None => {
                return Err(ErreurConstat::FinPrematuree {
                    position: lecteur.position,
                    attendu: "« , » ou « } »",
                });
            }
        }
    }

    if lecteur.position < lecteur.octets.len() {
        return Err(ErreurConstat::OctetsResiduels {
            position: lecteur.position,
            restants: lecteur.octets.len().saturating_sub(lecteur.position),
        });
    }

    construire(&valeurs)
}

/// Une clé du contrat, ou un refus. La reconnaissance rend la chaîne
/// **statique** du tableau : la suite compare des `&'static str`, jamais des
/// copies qui pourraient diverger.
fn reconnaitre_cle(cle: &str, position: usize) -> Result<&'static str, ErreurConstat> {
    for connue in CLES_DU_CONSTAT {
        if connue == cle {
            return Ok(connue);
        }
    }
    Err(ErreurConstat::CleInconnue {
        position,
        cle: cle.to_owned(),
    })
}

/// Le tri strict — il porte le « clés triées » du contrat ET le refus de clé
/// répétée (F7).
fn controler_le_tri(
    precedente: Option<&'static str>,
    cle: &'static str,
    position: usize,
) -> Result<(), ErreurConstat> {
    let Some(precedente) = precedente else {
        return Ok(());
    };
    match precedente.as_bytes().cmp(cle.as_bytes()) {
        core::cmp::Ordering::Less => Ok(()),
        core::cmp::Ordering::Equal => Err(ErreurConstat::CleRepetee {
            position,
            cle: cle.to_owned(),
        }),
        core::cmp::Ordering::Greater => Err(ErreurConstat::CleNonTriee {
            position,
            precedente: precedente.to_owned(),
            cle: cle.to_owned(),
        }),
    }
}

/// Une chaîne citée du sous-ensemble : ASCII, sans échappement, sans octet de
/// contrôle.
fn lire_texte(lecteur: &mut Lecteur<'_>) -> Result<String, ErreurConstat> {
    lecteur.exiger(b'"', "« \" » d'ouverture de chaîne")?;
    let mut rendu = String::new();
    loop {
        let position = lecteur.position;
        let Some(octet) = lecteur.regarder() else {
            return Err(ErreurConstat::FinPrematuree {
                position,
                attendu: "« \" » de fermeture de chaîne",
            });
        };
        if octet == b'"' {
            lecteur.avancer();
            return Ok(rendu);
        }
        if octet == b'\\' {
            return Err(ErreurConstat::EchappementInterdit { position });
        }
        if !octet.is_ascii() {
            return Err(ErreurConstat::OctetNonAscii { position, octet });
        }
        if octet.is_ascii_whitespace() {
            return Err(ErreurConstat::EspaceInterdit { position });
        }
        if octet.is_ascii_control() {
            return Err(ErreurConstat::CaractereInattendu {
                position,
                trouve: octet,
                attendu: "un caractère imprimable",
            });
        }
        rendu.push(char::from(octet));
        lecteur.avancer();
    }
}

/// Une valeur : chaîne citée, ou entier décimal non signé.
fn lire_valeur(lecteur: &mut Lecteur<'_>) -> Result<Valeur, ErreurConstat> {
    match lecteur.regarder() {
        Some(b'"') => Ok(Valeur::Texte(lire_texte(lecteur)?)),
        Some(octet) if octet.is_ascii_digit() => Ok(Valeur::Entier(lire_entier(lecteur)?)),
        Some(octet) if octet.is_ascii_whitespace() => Err(ErreurConstat::EspaceInterdit {
            position: lecteur.position,
        }),
        Some(octet) => Err(ErreurConstat::CaractereInattendu {
            position: lecteur.position,
            trouve: octet,
            attendu: "une chaîne citée ou un entier non signé",
        }),
        None => Err(ErreurConstat::FinPrematuree {
            position: lecteur.position,
            attendu: "une chaîne citée ou un entier non signé",
        }),
    }
}

/// Un entier décimal non signé en forme canonique : au moins un chiffre, aucun
/// zéro de tête au-delà du zéro seul, et dans la plage `u64`.
///
/// Le débordement est un **refus nommé**, jamais un modulo : un compte tronqué
/// qui se lirait comme un autre compte est exactement la faute qu'un
/// vérificateur fail-closed ne peut pas commettre (ADR-0010, point 5).
fn lire_entier(lecteur: &mut Lecteur<'_>) -> Result<u64, ErreurConstat> {
    let debut = lecteur.position;
    let mut valeur: u64 = 0;
    let mut chiffres = 0usize;
    while let Some(octet) = lecteur.regarder() {
        if !octet.is_ascii_digit() {
            break;
        }
        let quartet = u64::from(octet.wrapping_sub(b'0'));
        valeur = match valeur
            .checked_mul(10)
            .and_then(|dix| dix.checked_add(quartet))
        {
            Some(valeur) => valeur,
            None => return Err(ErreurConstat::EntierNonCanonique { position: debut }),
        };
        chiffres = chiffres.saturating_add(1);
        lecteur.avancer();
    }
    // Zéro de tête : `01` et `1` sont deux graphies d'un même nombre, et une
    // seule est la forme du contrat. (Le cas « aucun chiffre » n'atteint pas
    // cette fonction : `lire_valeur` ne l'appelle que sur un chiffre.)
    if chiffres > 1 && lecteur.octets.get(debut) == Some(&b'0') {
        return Err(ErreurConstat::EntierNonCanonique { position: debut });
    }
    Ok(valeur)
}

/// Rassemble les dix-huit valeurs contrôlées en la projection que le cœur
/// consomme.
fn construire(valeurs: &[(&'static str, Valeur)]) -> Result<Constat, ErreurConstat> {
    let version = entier(valeurs, "version_du_constat")?;
    // La version d'abord : lire le reste d'un contrat qu'on ne connaît pas
    // serait interpréter des octets sous une grammaire qui n'est pas la leur.
    if version != VERSION_DU_CONSTAT {
        return Err(ErreurConstat::VersionInattendue {
            attendue: VERSION_DU_CONSTAT,
            trouvee: version,
        });
    }

    let verdict = texte(valeurs, "verdict")?;
    if verdict != VERDICT_DE_SUCCES {
        return Err(ErreurConstat::VerdictSansSucces {
            trouve: verdict.to_owned(),
        });
    }

    // Les six longueurs — la pré-condition de (b) : un tampon à remplissage non
    // authentifié n'a pas d'empreinte qui lie quoi que ce soit.
    for (sens, cle_longueur, cle_authentifie, cle_attestee) in [
        (
            "reçu",
            "transcript_recv_longueur",
            "transcript_recv_authentifie",
            "transcript_recv_longueur_attestee",
        ),
        (
            "émis",
            "transcript_sent_longueur",
            "transcript_sent_authentifie",
            "transcript_sent_longueur_attestee",
        ),
    ] {
        let longueur = entier(valeurs, cle_longueur)?;
        let authentifie = entier(valeurs, cle_authentifie)?;
        let attestee = entier(valeurs, cle_attestee)?;
        if longueur != authentifie || longueur != attestee {
            return Err(ErreurConstat::LongueursIncoherentes {
                sens,
                longueur,
                authentifie,
                attestee,
            });
        }
    }

    // Les clés portées mais non comparées : contrôlées de type et de forme, puis
    // laissées au constat. Les nommer ici est ce qui fait de leur absence un
    // refus.
    let _ = entier(valeurs, "octets_presentation")?;
    let version_de_couche = texte(valeurs, "connection_info_version_tls")?;
    exiger_non_vide(&version_de_couche, "connection_info_version_tls")?;

    // L'empreinte du sens émis n'est plus jetée (`let _ =`) : elle se porte
    // jusqu'au `Constat` du cœur, sous son nom (ADR-0015 point 17 bis,
    // adjudication R-26). Aucun contrôle ne la consomme encore — le témoignage
    // ne porte pas les octets du sens émis — mais la donnée voyage, et l'unité
    // S4 « liaison de la désignation » la consommera. Une donnée lue, contrôlée
    // puis abandonnée est une donnée que la passe suivante devra re-instruire.
    let empreinte_du_sens_emis = empreinte(valeurs, "empreinte_sent_revele_sha256")?;

    let revision_amont = texte(valeurs, "revision_amont")?;
    exiger_non_vide(&revision_amont, "revision_amont")?;
    let origine = texte(valeurs, "server_name")?;
    exiger_non_vide(&origine, "server_name")?;

    Ok(Constat {
        revision_amont,
        cle_du_controle: cle_du_controle(valeurs)?,
        instant_de_connexion: entier(valeurs, "connection_info_time")?,
        origine_authentifiee: origine,
        empreinte_de_la_preuve: empreinte(valeurs, "empreinte_presentation_sha256")?,
        empreinte_de_l_utterance: empreinte(valeurs, "empreinte_recv_revele_sha256")?,
        empreinte_du_sens_emis,
    })
}

/// Les octets épinglés : `<algorithme> <chiffres hexadécimaux>`, en US-ASCII.
///
/// Les chiffres sont **contrôlés** (hexadécimal minuscule, nombre pair et non
/// nul) puis repris verbatim : le témoignage épingle une chaîne lisible, et le
/// cœur ne fait qu'une égalité d'octets.
fn cle_du_controle(valeurs: &[(&'static str, Valeur)]) -> Result<Vec<u8>, ErreurConstat> {
    let algorithme = texte(valeurs, "attestor_cle_algorithme")?;
    exiger_non_vide(&algorithme, "attestor_cle_algorithme")?;
    if algorithme.contains(SEPARATEUR_DE_CLE) {
        return Err(ErreurConstat::AlgorithmeAmbigu {
            cle: "attestor_cle_algorithme",
        });
    }
    let chiffres = texte(valeurs, "attestor_cle_hex")?;
    controler_hexadecimal(&chiffres, "attestor_cle_hex")?;
    Ok(format!("{algorithme}{SEPARATEUR_DE_CLE}{chiffres}").into_bytes())
}

/// Une empreinte : soixante-quatre chiffres hexadécimaux minuscules, sans
/// tolérance — la longueur EST le contrôle.
fn empreinte(
    valeurs: &[(&'static str, Valeur)],
    cle: &'static str,
) -> Result<[u8; OCTETS_D_EMPREINTE], ErreurConstat> {
    let chiffres = texte(valeurs, cle)?;
    let paires = chiffres.as_bytes();
    let mut octets: Vec<u8> = Vec::new();
    for paire in paires.chunks_exact(2) {
        let mut valeur: u8 = 0;
        for chiffre in paire.iter().copied() {
            match valeur_hexadecimale(chiffre) {
                Some(quartet) => valeur = valeur.wrapping_shl(4) | quartet,
                None => {
                    return Err(ErreurConstat::HexadecimalInvalide {
                        cle,
                        octet: chiffre,
                    });
                }
            }
        }
        octets.push(valeur);
    }
    // Le nombre impair et la mauvaise longueur tombent au même endroit : la
    // **conversion est le contrôle**, comme au cœur (`lire_utterance` : « la
    // conversion EST le contrôle de longueur … aucun `unwrap` n'est
    // nécessaire »).
    if !paires.chunks_exact(2).remainder().is_empty() {
        return Err(ErreurConstat::LongueurHexadecimaleInvalide {
            cle,
            attendue_en_octets: Some(OCTETS_D_EMPREINTE),
            trouvee_en_chiffres: chiffres.len(),
        });
    }
    match <[u8; OCTETS_D_EMPREINTE]>::try_from(octets.as_slice()) {
        Ok(empreinte) => Ok(empreinte),
        Err(_) => Err(ErreurConstat::LongueurHexadecimaleInvalide {
            cle,
            attendue_en_octets: Some(OCTETS_D_EMPREINTE),
            trouvee_en_chiffres: chiffres.len(),
        }),
    }
}

/// Chiffres hexadécimaux **minuscules**, en nombre pair et non nul — le contrôle
/// des clés dont la longueur n'est pas fixée par le contrat.
fn controler_hexadecimal(chiffres: &str, cle: &'static str) -> Result<(), ErreurConstat> {
    for octet in chiffres.as_bytes().iter().copied() {
        if valeur_hexadecimale(octet).is_none() {
            return Err(ErreurConstat::HexadecimalInvalide { cle, octet });
        }
    }
    let longueur = chiffres.len();
    if longueur == 0 || longueur.checked_rem(2) != Some(0) {
        return Err(ErreurConstat::LongueurHexadecimaleInvalide {
            cle,
            attendue_en_octets: None,
            trouvee_en_chiffres: longueur,
        });
    }
    Ok(())
}

/// Un chiffre hexadécimal **minuscule** — les majuscules sont refusées, pas
/// repliées : le contrat écrit une graphie, et en accepter deux ferait deux
/// constats d'un seul (posture d'ADR-0016 C0).
fn valeur_hexadecimale(octet: u8) -> Option<u8> {
    match octet {
        b'0'..=b'9' => Some(octet.wrapping_sub(b'0')),
        b'a'..=b'f' => Some(octet.wrapping_sub(b'a').wrapping_add(10)),
        _ => None,
    }
}

fn exiger_non_vide(valeur: &str, cle: &'static str) -> Result<(), ErreurConstat> {
    if valeur.is_empty() {
        return Err(ErreurConstat::ValeurVide { cle });
    }
    Ok(())
}

/// La valeur d'une clé, en chaîne — clé absente ou d'un autre type : refus nommé.
fn texte(valeurs: &[(&'static str, Valeur)], cle: &'static str) -> Result<String, ErreurConstat> {
    match trouver(valeurs, cle)? {
        Valeur::Texte(texte) => Ok(texte),
        Valeur::Entier(_) => Err(ErreurConstat::TypeInattendu {
            cle,
            attendu: "une chaîne",
        }),
    }
}

/// La valeur d'une clé, en entier.
fn entier(valeurs: &[(&'static str, Valeur)], cle: &'static str) -> Result<u64, ErreurConstat> {
    match trouver(valeurs, cle)? {
        Valeur::Entier(valeur) => Ok(valeur),
        Valeur::Texte(_) => Err(ErreurConstat::TypeInattendu {
            cle,
            attendu: "un entier non signé",
        }),
    }
}

/// La valeur d'une clé, **rendue par valeur** : le déréférencement d'un
/// emprunt est une forme que la gate S-G3 rejette dans ce rôle, et une copie
/// d'un objet de dix-huit paires ne coûte rien qui se mesure.
fn trouver(valeurs: &[(&'static str, Valeur)], cle: &'static str) -> Result<Valeur, ErreurConstat> {
    for paire in valeurs {
        if paire.0 == cle {
            return Ok(paire.1.clone());
        }
    }
    Err(ErreurConstat::CleManquante { cle })
}
