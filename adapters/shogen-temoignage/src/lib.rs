#![forbid(unsafe_code)]
//! **Le constructeur du témoignage réel** — la coquille qui sait ce qui a été
//! interrogé, et qui paie une fois le coût de la normalisation.
//!
//! # Où ce paquet se tient, et pourquoi il n'est ni le cœur ni le vérificateur
//!
//! ADR-0016 C0 : « La normalisation a lieu **une fois, à la construction, dans
//! l'adapter** — le seul rang à savoir ce qui a été interrogé — et l'adapter
//! émet ensuite exactement les octets qu'il a inscrits dans `subject`. Le cœur
//! et le vérificateur ne normalisent **rien** ». Ce paquet est ce rang-là.
//! ADR-0001 le classe : un adapter, « testé, jamais prouvé ».
//!
//! Il ne conduit aucune session et n'ouvre aucune connexion : il **lit des
//! octets déjà déposés** — ceux qu'une session attestée a produits — et en fait
//! les sept champs de `03-temoignage.md` §1. C'est un constructeur, pas un
//! client.
//!
//! # Les recoupements qu'il fait, et pourquoi il les fait ici
//!
//! Le vérificateur contrôle des **liaisons** (ADR-0015 point 8) ; s'il les
//! contrôlait sur un lot que rien n'a jamais recoupé, le premier `verify` d'un
//! lot neuf serait aussi son premier contrôle. Ce constructeur recoupe donc
//! tout ce qu'il assemble, contre le constat du binaire compagnon et contre le
//! prédicat du cœur :
//!
//! * `subject` est construit, puis soumis à `shogen_core::subject_est_canonique`
//!   — « un désaccord constructeur/prédicat est un **rouge** : deux
//!   implémentations qui se contrôlent l'une l'autre » (ADR-0016 C10) ;
//! * les trois empreintes du constat sont **recalculées** sur les octets
//!   déposés, par `shogen_core::empreinte_sha256` (ADR-0018) — celle du
//!   compagnon vient d'une seconde implémentation, et l'indépendance des deux
//!   est ce qui fait du désaccord un refus (`empreinte.rs`) ;
//! * les longueurs et la taille de la preuve que le constat déclare sont
//!   comparées aux octets réellement lus ;
//! * l'hôte de `subject` est comparé à l'origine authentifiée (`server_name`),
//!   et la clé épinglée à la clé du contrôle délégué.
//!
//! Tout écart est un **refus nommé**, jamais une correction : un constructeur
//! qui rattrape ce qu'il ne comprend pas fabrique un lot dont personne ne sait
//! plus ce qu'il dit.
//!
//! # La convention d'épinglage de la clé
//!
//! `attestor.key` porte les octets US-ASCII de `<algorithme> <chiffres
//! hexadécimaux>` — la ligne même que le compagnon dépose à côté de la
//! présentation. L'algorithme entre dans les octets épinglés parce qu'ADR-0015
//! point 8 alinéa (f) demande « l'identité de la clé » et non ses seuls
//! chiffres. Le vérificateur recompose la même chaîne depuis les deux clés du
//! constat, et le cœur ne fait qu'une égalité d'octets (ADR-0001 : il ne nomme
//! aucun algorithme).

use shogen_core::{
    Attestor, ObservedAt, Temoignage, Utterance, empreinte_en_hexadecimal, empreinte_sha256,
    hote_de_subject, subject_est_canonique,
};

/// Le préfixe de scheme de la forme canonique (ADR-0016 C1/C2).
pub const PREFIXE: &str = "https://";
/// Le port par défaut du scheme, **omis** de la forme canonique (ADR-0016 C5).
pub const SUFFIXE_PORT_PAR_DEFAUT: &str = ":443";
/// Le séparateur de la convention d'épinglage.
pub const SEPARATEUR_DE_CLE: char = ' ';

/// Le refus du constructeur — nommé, et porteur de ce qui l'a produit.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Erreur {
    /// La requête émise n'a pas de ligne de requête lisible.
    LigneDeRequeteAbsente,
    /// La ligne de requête n'a pas la forme `<méthode> <cible> <version>`.
    LigneDeRequeteMalFormee { ligne: String },
    /// La cible de la requête n'est pas un chemin absolu.
    CibleNonAbsolue { cible: String },
    /// L'en-tête `host` manque : sans lui, rien ne dit quelle origine a été
    /// interrogée — et l'inventer serait fabriquer une désignation.
    EnteteHostAbsente,
    /// Le `subject` construit ne satisfait pas le prédicat du cœur — un
    /// désaccord constructeur/prédicat (ADR-0016 C10).
    SubjectNonCanonique { subject: String, cause: String },
    /// Une clé du constat est absente ou illisible.
    CleDuConstatIllisible { cle: String },
    /// Une valeur du constat n'est pas du type attendu.
    ValeurDuConstatMalFormee { cle: String, valeur: String },
    /// Un recoupement a échoué : ce que le constat déclare et ce que les octets
    /// déposés donnent ne coïncident pas.
    RecoupementRompu {
        quoi: String,
        constate: String,
        mesure: String,
    },
    /// La liste des résidus est vide : 03 §1 en fait un champ obligatoire, et
    /// un témoignage sans résidu prétendrait n'en avoir aucun.
    ResidusVides,
}

impl core::fmt::Display for Erreur {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        match self {
            Self::LigneDeRequeteAbsente => write!(
                f,
                "octets émis sans ligne de requête : rien ne dit ce qui a été interrogé"
            ),
            Self::LigneDeRequeteMalFormee { ligne } => write!(
                f,
                "ligne de requête mal formée : « {ligne} » — « <méthode> <cible> <version> » attendu"
            ),
            Self::CibleNonAbsolue { cible } => write!(
                f,
                "cible de requête non absolue : « {cible} » — un chemin commençant par « / » est attendu (ADR-0016 C6)"
            ),
            Self::EnteteHostAbsente => write!(
                f,
                "en-tête « host » absente des octets émis : l'origine interrogée ne s'invente pas"
            ),
            Self::SubjectNonCanonique { subject, cause } => write!(
                f,
                "subject construit non canonique : « {subject} » — {cause} (désaccord constructeur/prédicat, ADR-0016 C10)"
            ),
            Self::CleDuConstatIllisible { cle } => {
                write!(f, "constat : clé « {cle} » absente ou illisible")
            }
            Self::ValeurDuConstatMalFormee { cle, valeur } => write!(
                f,
                "constat : valeur mal formée pour « {cle} » — « {valeur} »"
            ),
            Self::RecoupementRompu {
                quoi,
                constate,
                mesure,
            } => write!(
                f,
                "recoupement rompu ({quoi}) : le constat déclare « {constate} », les octets déposés donnent « {mesure} »"
            ),
            Self::ResidusVides => write!(
                f,
                "aucun résidu : 03 §1 fait de `residual` un champ obligatoire, et un témoignage sans résidu prétendrait n'en avoir aucun"
            ),
        }
    }
}

impl core::error::Error for Erreur {}

/// Ce dont la construction a besoin — **des octets déjà déposés**, jamais une
/// connexion.
pub struct Entrees<'a> {
    /// Les octets révélés du sens émis : la requête complète.
    pub octets_emis: &'a [u8],
    /// Les octets révélés du sens reçu : la réponse complète — c'est
    /// l'`utterance`.
    pub octets_recus: &'a [u8],
    /// Les octets de la preuve de transport, **opaques**.
    pub octets_de_preuve: &'a [u8],
    /// Le constat du binaire compagnon, tel quel.
    pub texte_du_constat: &'a str,
    /// L'identifiant du mécanisme d'attestation (03 §1, champ `transport`).
    pub transport: &'a str,
    /// L'identité de l'attestateur — « qui pourrait forger, nominativement ».
    pub identite_de_l_attestateur: &'a str,
    /// L'identité de l'horloge qui a daté (03 §1 : « celle du transport,
    /// jamais celle de Shōgen »).
    pub horloge: &'a str,
    /// Les identifiants de résidus du transport, **dans l'ordre émis**.
    pub residus: &'a [&'a str],
}

/// Construit le témoignage canonique, et le refuse si un seul recoupement
/// tombe.
pub fn construire(entrees: &Entrees<'_>) -> Result<Temoignage, Erreur> {
    if entrees.residus.is_empty() {
        return Err(Erreur::ResidusVides);
    }

    // 1. Le contrat du constat, dans sa version.
    let version = valeur_entiere(entrees.texte_du_constat, "version_du_constat")?;
    recouper("version_du_constat", &version.to_string(), "1")?;
    let verdict = valeur_texte(entrees.texte_du_constat, "verdict")?;
    recouper("verdict du constat", &verdict, "presentation_verifiee")?;

    // 2. `subject` — construit, puis soumis au prédicat du cœur.
    let subject = subject_depuis_la_requete(entrees.octets_emis)?;

    // 3. Le recoupement d'origine : l'hôte construit EST l'origine
    //    authentifiée que le constat rapporte (ADR-0015 point 13).
    let origine = valeur_texte(entrees.texte_du_constat, "server_name")?;
    recouper("origine authentifiée", &origine, hote_de_subject(&subject))?;

    // 4. Les trois empreintes — recalculées ici, comparées à celles que le
    //    compagnon a calculées avec une AUTRE implémentation.
    for (quoi, cle, octets) in [
        (
            "empreinte des octets reçus",
            "empreinte_recv_revele_sha256",
            entrees.octets_recus,
        ),
        (
            "empreinte des octets émis",
            "empreinte_sent_revele_sha256",
            entrees.octets_emis,
        ),
        (
            "empreinte de la preuve de transport",
            "empreinte_presentation_sha256",
            entrees.octets_de_preuve,
        ),
    ] {
        let constatee = valeur_texte(entrees.texte_du_constat, cle)?;
        recouper(
            quoi,
            &constatee,
            &empreinte_en_hexadecimal(&empreinte_sha256(octets)),
        )?;
    }

    // 5. Les longueurs — un octet de plus ou de moins et l'empreinte du point 4
    //    n'aurait pas tenu ; ce recoupement-ci nomme l'écart plus tôt.
    for (quoi, cle, mesure) in [
        (
            "longueur des octets reçus",
            "transcript_recv_longueur",
            entrees.octets_recus.len(),
        ),
        (
            "longueur des octets émis",
            "transcript_sent_longueur",
            entrees.octets_emis.len(),
        ),
        (
            "taille de la preuve de transport",
            "octets_presentation",
            entrees.octets_de_preuve.len(),
        ),
    ] {
        let constatee = valeur_entiere(entrees.texte_du_constat, cle)?;
        recouper(quoi, &constatee.to_string(), &mesure.to_string())?;
    }

    // 6. La clé épinglée : la convention d'épinglage, composée depuis le
    //    constat lui-même.
    let algorithme = valeur_texte(entrees.texte_du_constat, "attestor_cle_algorithme")?;
    let chiffres = valeur_texte(entrees.texte_du_constat, "attestor_cle_hex")?;
    let cle_epinglee = format!("{algorithme}{SEPARATEUR_DE_CLE}{chiffres}");

    let instant = valeur_entiere(entrees.texte_du_constat, "connection_info_time")?;

    Ok(Temoignage {
        subject,
        attestor: vec![Attestor {
            key: cle_epinglee.into_bytes(),
            identity: String::from(entrees.identite_de_l_attestateur),
        }],
        residual: entrees.residus.iter().map(|r| String::from(*r)).collect(),
        transport: String::from(entrees.transport),
        utterance: Utterance {
            hash: empreinte_sha256(entrees.octets_recus),
            bytes: Some(entrees.octets_recus.to_vec()),
        },
        observed_at: ObservedAt {
            clock: String::from(entrees.horloge),
            instant,
        },
        transport_proof: entrees.octets_de_preuve.to_vec(),
    })
}

/// La ligne de clé épinglée telle que le compagnon la dépose — pour que
/// l'appelant puisse la recouper avec ce que la construction a composé.
pub fn cle_epinglee_du_constat(texte_du_constat: &str) -> Result<String, Erreur> {
    let algorithme = valeur_texte(texte_du_constat, "attestor_cle_algorithme")?;
    let chiffres = valeur_texte(texte_du_constat, "attestor_cle_hex")?;
    Ok(format!("{algorithme}{SEPARATEUR_DE_CLE}{chiffres}"))
}

/// `subject` **construit** depuis les octets réellement émis — la seule source
/// qui sache ce qui a été interrogé.
///
/// Les normalisations d'ADR-0016 appliquées ici, et aucune autre : le scheme
/// est `https` (C2 — le transport atteste une session TLS), l'hôte est plié en
/// minuscules (C3), le port par défaut est omis (C5), un chemin vide devient
/// `/` (C6), et **la requête est reprise octet pour octet** (C8 : aucun tri,
/// aucune déduplication, aucune réécriture `+`/espace).
pub fn subject_depuis_la_requete(octets_emis: &[u8]) -> Result<String, Erreur> {
    let texte = String::from_utf8_lossy(octets_emis);
    let mut lignes = texte.split("\r\n");
    let ligne = lignes.next().ok_or(Erreur::LigneDeRequeteAbsente)?;
    if ligne.is_empty() {
        return Err(Erreur::LigneDeRequeteAbsente);
    }
    let mut morceaux = ligne.split(' ');
    let (Some(_methode), Some(cible), Some(_version), None) = (
        morceaux.next(),
        morceaux.next(),
        morceaux.next(),
        morceaux.next(),
    ) else {
        return Err(Erreur::LigneDeRequeteMalFormee {
            ligne: String::from(ligne),
        });
    };
    if !cible.starts_with('/') {
        return Err(Erreur::CibleNonAbsolue {
            cible: String::from(cible),
        });
    }

    let mut hote: Option<String> = None;
    for suivante in lignes {
        if suivante.is_empty() {
            break;
        }
        let Some((nom, valeur)) = suivante.split_once(':') else {
            continue;
        };
        // RFC 9110 : les noms de champ sont insensibles à la casse.
        if nom.eq_ignore_ascii_case("host") {
            hote = Some(String::from(valeur.trim()));
            break;
        }
    }
    let hote = hote.ok_or(Erreur::EnteteHostAbsente)?;
    // C3 — l'hôte est plié en minuscules à la construction. C5 — le port par
    // défaut du scheme est omis, avec son délimiteur.
    let hote = hote.to_ascii_lowercase();
    let hote = hote
        .strip_suffix(SUFFIXE_PORT_PAR_DEFAUT)
        .unwrap_or(&hote)
        .to_owned();

    let subject = format!("{PREFIXE}{hote}{cible}");
    match subject_est_canonique(subject.as_bytes()) {
        Ok(()) => Ok(subject),
        Err(cause) => Err(Erreur::SubjectNonCanonique {
            cause: cause.to_string(),
            subject,
        }),
    }
}

/// La valeur textuelle d'une clé du constat — **extraction minimale, propre à
/// cet adapter**.
///
/// Elle est volontairement *indépendante* de l'analyseur du vérificateur : deux
/// lectures écrites séparément qui doivent tomber d'accord sur les mêmes octets
/// valent mieux qu'une lecture partagée qui se tromperait aux deux bouts (R-3
/// interdit la duplication d'une **règle**, pas l'indépendance délibérée de
/// deux lecteurs qui se contrôlent — c'est le geste déjà tenu sur l'empreinte,
/// `fixtures/NOTES.md` §3).
pub fn valeur_texte(constat: &str, cle: &str) -> Result<String, Erreur> {
    let aiguille = format!("\"{cle}\":\"");
    let debut = constat
        .find(&aiguille)
        .ok_or_else(|| Erreur::CleDuConstatIllisible {
            cle: String::from(cle),
        })?
        + aiguille.len();
    let reste = constat
        .get(debut..)
        .ok_or_else(|| Erreur::CleDuConstatIllisible {
            cle: String::from(cle),
        })?;
    let fin = reste
        .find('"')
        .ok_or_else(|| Erreur::CleDuConstatIllisible {
            cle: String::from(cle),
        })?;
    reste
        .get(..fin)
        .map(String::from)
        .ok_or_else(|| Erreur::CleDuConstatIllisible {
            cle: String::from(cle),
        })
}

/// La valeur entière d'une clé du constat.
pub fn valeur_entiere(constat: &str, cle: &str) -> Result<u64, Erreur> {
    let aiguille = format!("\"{cle}\":");
    let debut = constat
        .find(&aiguille)
        .ok_or_else(|| Erreur::CleDuConstatIllisible {
            cle: String::from(cle),
        })?
        + aiguille.len();
    let reste = constat
        .get(debut..)
        .ok_or_else(|| Erreur::CleDuConstatIllisible {
            cle: String::from(cle),
        })?;
    let fin = reste
        .find(|caractere: char| !caractere.is_ascii_digit())
        .unwrap_or(reste.len());
    let chiffres = reste
        .get(..fin)
        .ok_or_else(|| Erreur::CleDuConstatIllisible {
            cle: String::from(cle),
        })?;
    chiffres
        .parse::<u64>()
        .map_err(|_| Erreur::ValeurDuConstatMalFormee {
            cle: String::from(cle),
            valeur: String::from(chiffres),
        })
}

/// Un recoupement : deux chaînes qui doivent être la même, ou un refus qui les
/// montre toutes les deux.
fn recouper(quoi: &str, constate: &str, mesure: &str) -> Result<(), Erreur> {
    if constate == mesure {
        return Ok(());
    }
    Err(Erreur::RecoupementRompu {
        quoi: String::from(quoi),
        constate: String::from(constate),
        mesure: String::from(mesure),
    })
}
