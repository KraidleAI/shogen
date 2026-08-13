//! Les **refus nommés** du typeur.
//!
//! Rattachement (G0) : **ADR-0010, point 1** (le patron suivi : « une entrée
//! mal formée est une **valeur** du type de retour (erreur nommée), jamais une
//! divergence », et chaque variante dit *où* et *quoi*) ; **ADR-0010, point 5**
//! (fail-safe defaults) ; **10 §8**, entrée A(typer-correctness) — « décodage
//! par position fixe et par clé retournée ; indécodable ⇒ panne ». La formule
//! sœur appartient à une **autre** pièce et se cite séparément : le module de
//! décodage de l'instrument S2 (`s2-harness/shogen_s2/sources.py`, en-tête) —
//! « un indécodable devient une panne, jamais une valeur inventée ».
//!
//! Le typeur n'est pas le cœur : il n'hérite pas de son régime, il en copie la
//! **discipline de refus**. Ce qu'il ne type pas exactement, il le refuse en
//! nommant la clause violée — aucun arrondi, aucune troncature, aucun repli
//! silencieux.

use shogen_core::ErreurSubject;

/// Profondeur d'imbrication maximale admise dans le dire (voir [`ErreurJson`]).
pub const PROFONDEUR_MAXIMALE: usize = 32;

/// Refus d'analyse du dire brut, au niveau de la grammaire JSON (RFC 8259).
#[derive(Debug, Clone, PartialEq, Eq)]
#[non_exhaustive]
pub enum ErreurJson {
    /// Aucun octet à analyser.
    EntreeVide,
    /// Le dire n'est pas de l'UTF-8 valide — RFC 8259 §8.1 impose UTF-8.
    EntreeNonUtf8 { position: usize },
    /// Un octet attendu ne s'y trouve pas.
    OctetInattendu {
        position: usize,
        attendu: u8,
        trouve: u8,
    },
    /// L'entrée s'arrête au milieu d'une valeur.
    FinPrematuree { position: usize },
    /// La racine du dire n'est pas un objet JSON : le typeur ne lit que des
    /// objets à membres nommés (10 §3.1 : « clé retournée, jamais clé
    /// demandée » — l'analogue JSON de la règle de position fixe).
    RacineNonObjet { position: usize, trouve: u8 },
    /// Deux fois la même clé dans un même objet. RFC 8259 §4 (détenue, lue) :
    /// « The names within an object SHOULD be unique. » et « When the names
    /// within an object are not unique, the behavior of software that receives
    /// such an object is unpredictable. Many implementations report the last
    /// name/value pair only. » Deux analyseurs peuvent donc lire deux valeurs
    /// différentes du **même** dire, dont l'empreinte est pourtant unique
    /// (ADR-0005 règle 1) : le typeur refuse plutôt que de choisir.
    CleDupliquee { position: usize, cle: String },
    /// Un caractère de contrôle non échappé dans une chaîne — RFC 8259 §7.
    CaractereDeControle { position: usize, octet: u8 },
    /// Une séquence `\x` dont `x` n'est pas un échappement admis.
    EchappementInconnu { position: usize, octet: u8 },
    /// `\u` non suivi de quatre chiffres hexadécimaux.
    EchappementUnicodeMalForme { position: usize },
    /// Un demi-substitut UTF-16 sans son pair.
    SubstitutOrphelin { position: usize, unite: u16 },
    /// Un nombre JSON qui ne satisfait pas la grammaire de la RFC 8259 §6.
    NombreMalForme { position: usize },
    /// Une suite de lettres qui n'est ni `true`, ni `false`, ni `null`.
    LitteralInconnu { position: usize },
    /// Imbrication au-delà de [`PROFONDEUR_MAXIMALE`]. Ce refus est une borne
    /// de construction : sans lui, un dire hostile fait diverger l'analyseur
    /// par la pile, ce qui serait une panique — donc un déni, pas un refus.
    ProfondeurExcessive {
        position: usize,
        profondeur_maximale: usize,
    },
    /// Des octets subsistent après la valeur racine.
    OctetsResiduels { position: usize, restants: usize },
}

/// Refus de typage d'une valeur décimale.
///
/// La forme admise est délibérément **plus étroite** que le nombre JSON : ni
/// exposant, ni `+`, ni zéro de tête, ni blanc. Une graphie hors de cette forme
/// n'est pas corrigée, elle est refusée.
#[derive(Debug, Clone, PartialEq, Eq)]
#[non_exhaustive]
pub enum ErreurDecimale {
    /// Aucune graphie à lire.
    Vide,
    /// `e` ou `E` : la notation scientifique est refusée. Elle n'est pas
    /// convertie, parce qu'une conversion silencieuse changerait l'échelle
    /// écrite par la source, donc le nombre de chiffres significatifs qu'elle
    /// a publiés.
    NotationScientifique { position: usize },
    /// Un octet qui n'appartient pas à la forme admise (blanc, `+`, `,`, …).
    OctetHorsForme { position: usize, octet: u8 },
    /// Un chiffre est attendu ici et manque (après `-`, après `.`, fin).
    ChiffreAttendu { position: usize },
    /// Zéro de tête : `007`, `-0007`. La graphie de la source n'est pas
    /// rectifiée ; elle est refusée.
    ZeroDeTete { position: usize },
    /// Un second point décimal.
    PointDecimalRepete { position: usize },
    /// Un signe `-` devant une valeur nulle (`-0`, `-0.00`). La forme typée
    /// (mantisse entière) ne porte pas de zéro signé : l'accepter ferait perdre
    /// silencieusement le signe écrit par la source. Refusé, donc.
    ZeroSigne { position: usize },
    /// Plus de chiffres que la mantisse entière n'en porte : le typage exact
    /// est impossible. **Le typeur refuse au lieu d'arrondir** — c'est le cas
    /// « perte de précision » de la doctrine fail-closed.
    CapaciteDeMantisseDepassee { chiffres: usize },
    /// Le nombre de décimales dépasse ce que l'exposant porte.
    ///
    /// **Borne défensive, inatteignable en pratique** et il faut le dire : la
    /// capacité de la mantisse se ferme vers 39 chiffres, bien avant que le
    /// compte de décimales n'approche `i32::MAX`. Aucun cas du corpus ne
    /// l'exerce ; elle existe pour que la conversion `usize → i32` ne soit
    /// jamais faite sans issue nommée, pas parce qu'un dire pourrait
    /// l'atteindre.
    ExposantHorsCapacite { decimales: usize },
}

/// Refus de typage d'un instant.
///
/// La forme admise est un `date-time` RFC 3339 §5.6 (détenue, lue) en UTC
/// explicite, majuscules `T` et `Z`. La restriction de casse est **fondée sur
/// la pièce**, pas inventée : §5.6, NOTE — « Specifications that use this
/// format in such environments MAY further limit the date/time syntax so that
/// the letters 'T' and 'Z' used in the date/time syntax must always be upper
/// case. » Aucune conversion en époque n'est faite : l'instant reste la graphie
/// de la source (03 §1 : « la fraîcheur se calcule plus haut ; ici on
/// enregistre qui a daté »).
#[derive(Debug, Clone, PartialEq, Eq)]
#[non_exhaustive]
pub enum ErreurInstant {
    /// Graphie vide.
    Vide,
    /// Un octet attendu ne s'y trouve pas (séparateur `-`, `T`, `:`, `Z`).
    OctetInattendu {
        position: usize,
        attendu: u8,
        trouve: u8,
    },
    /// Un chiffre est attendu ici.
    ChiffreAttendu { position: usize },
    /// La graphie s'arrête avant la fin de la forme.
    FinPrematuree { position: usize },
    /// Décalage horaire autre que `Z` : le typeur ne convertit aucun fuseau —
    /// il refuse. Convertir serait réécrire la graphie de la source.
    DecalageNonUtc { position: usize },
    /// Fraction de seconde annoncée par `.` mais sans chiffre.
    FractionVide { position: usize },
    /// Un champ hors de ses bornes (mois 13, heure 24, jour 31 en février…).
    ChampHorsBornes { champ: &'static str, valeur: u32 },
    /// Des octets subsistent après le `Z`.
    OctetsResiduels { position: usize, restants: usize },
}

/// Refus de typage — l'unique type d'erreur rendu par le typeur.
#[derive(Debug, Clone, PartialEq, Eq)]
#[non_exhaustive]
pub enum RefusDeTypage {
    /// `subject` ne satisfait pas le prédicat de canonicité du cœur
    /// (ADR-0016 C10).
    SubjectNonCanonique { erreur: ErreurSubject },
    /// `subject` est canonique mais n'est pas celui que ce typeur sait lire.
    /// Un typeur est lié à **un** endpoint : la devise se lit à l'endpoint,
    /// pas dans le dire (voir [`crate::SUBJECT_EPINGLE`]).
    SubjectNonEpingle { attendu: &'static str },
    /// Le dire ne s'analyse pas.
    Json { erreur: ErreurJson },
    /// Une clé attendue manque à la racine du dire.
    ChampManquant { cle: &'static str },
    /// Une clé attendue est présente mais n'est pas une chaîne JSON. Le typeur
    /// ne lit les prix que comme chaînes : un nombre JSON serait typé par
    /// l'analyseur du consommateur, et beaucoup le typent en flottant binaire.
    ChampNonTextuel { cle: &'static str, position: usize },
    /// La valeur du champ prix n'est pas une décimale exacte admise.
    Decimale {
        cle: &'static str,
        erreur: ErreurDecimale,
    },
    /// La valeur du champ instant n'est pas un `date-time` RFC 3339 UTC.
    Instant {
        cle: &'static str,
        erreur: ErreurInstant,
    },
}
