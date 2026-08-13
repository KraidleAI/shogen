//! Le **prédicat de canonicité de `subject`** — ADR-0016, C1 à C10.
//!
//! Rattachement (G0) : **ADR-0016** (« La canonicalisation de `subject` : forme
//! construite, prédicat au vérificateur, aucun tri de requête »), point C10 :
//! « `shogen-core` porte une fonction **totale**
//! `subject_est_canonique(&[u8]) -> Result<(), ErreurSubject>` : sans I/O, sans
//! horloge, au régime d'ADR-0010, variantes d'erreur **nommées et positionnées**
//! au patron d'`ErreurDecodage` ». Grammaire de référence : RFC 3986 §3
//! (`host`, `port`, `path-abempty`, `segment`, `pchar`, `query`, `pct-encoded`,
//! `unreserved`, `sub-delims`), RFC 9110 §4.2.
//!
//! **Ce que ce module fait, et ce qu'il ne fait pas.** Il *contrôle*, il ne
//! *normalise* pas (C0) : aucune fonction d'ici ne rend un `subject` réécrit.
//! Ce n'est pas un normaliseur d'URI général et il ne doit jamais être décrit
//! comme tel (ADR-0016, §Coûts) : ni IDN, ni littéral d'adresse, ni scheme autre
//! que `https`, ni corps de requête.
//!
//! **L'ordre des contrôles est une décision, pas un accident** — un même octet
//! peut violer plusieurs clauses, et la variante rendue doit être stable d'une
//! exécution et d'une machine à l'autre (ADR-0010, *pur*) :
//!
//! 1. le scheme (C2), qui seul permet de découper le reste ;
//! 2. le `#` où qu'il soit (C9) — il n'appartient à aucun composant admis ;
//! 3. l'autorité : `userinfo` (C4), littéral d'adresse, hôte (C3) ;
//! 4. le port (C5) ;
//! 5. le chemin : vidité (C6), octets, triplets (C7), segments pointillés (C6,
//!    « contrôle après C7 ») ;
//! 6. la requête : vidité (C8), octets, triplets (C7), grammaire (C8).
//!
//! Régime d'assurance : *tested (avec compte)* — `tests/subject_canonique.rs`,
//! `tests/subject_proprietes.rs`, `tests/mutation_canonique.rs`.

/// Le préfixe imposé par C1 et C2 : `https`, en minuscules, et rien d'autre.
pub const PREFIXE_CANONIQUE: &str = "https://";

/// Le port par défaut du scheme, en graphie décimale (RFC 9110 §4.2.2 : « TCP
/// port 443 (the reserved port for HTTP over TLS) is the default. »).
pub const PORT_PAR_DEFAUT: &[u8] = b"443";

/// L'octet `%`, tête d'un triplet `pct-encoded` (RFC 3986 §2.1).
const PERCENT: u8 = b'%';
/// L'octet `.`, seul caractère d'un segment pointillé (C6).
const POINT: u8 = b'.';

/// Refus de canonicité de `subject`.
///
/// Chaque variante dit **où** (position d'octet dans le `subject`) et **quoi** —
/// le patron d'`ErreurDecodage` : un refus se diagnostique sans journal, le cœur
/// ne journalisant pas (ADR-0010, point 1).
///
/// Les noms sont ceux qu'ADR-0016 emploie clause par clause. Deux variantes
/// n'ont **pas** de nom à l'ADR et sont nommées ici, à ratifier ou à renommer
/// par l'orchestrateur : `SchemeNonHttps` (C2 énonce la règle sans nommer le
/// refus) et `HoteVide` (C3 exige un nom enregistré ; l'ABNF `reg-name` admet
/// le vide, une désignation vide ne désigne rien).
#[derive(Debug, Clone, PartialEq, Eq)]
#[non_exhaustive]
pub enum ErreurSubject {
    /// Un octet ≥ 0x80 hors de l'hôte — C1 : « Tout octet ≥ 0x80 est refusé ».
    OctetNonAscii { position: usize, octet: u8 },
    /// Le `subject` ne commence pas exactement par `https://` — C2.
    SchemeNonHttps { position: usize },
    /// Une majuscule dans l'hôte — C3 (RFC 3986 §6.2.2.1).
    HoteMajuscule { position: usize, octet: u8 },
    /// Un triplet percent dans l'hôte — C3.
    HotePercentEncode { position: usize },
    /// Un littéral d'adresse : crochets, ou hôte tout en chiffres et points — C3.
    HoteLitteralAdresse { position: usize },
    /// Un octet non ASCII dans l'hôte (IDN) — C3 : refusé, jamais converti.
    HoteNonAscii { position: usize, octet: u8 },
    /// Hôte vide : `https:///…`.
    HoteVide { position: usize },
    /// Un `@` dans l'autorité — C4 (RFC 9110 §4.2.4).
    UserinfoPresent { position: usize },
    /// Le port par défaut écrit explicitement — C5.
    PortParDefautExplicite { position: usize },
    /// Port vide, non décimal, ou à zéro de tête — C5.
    PortNonDecimal { position: usize },
    /// Chemin vide — C6 (RFC 9110 §4.2.3).
    CheminVide { position: usize },
    /// Un segment `.` ou `..`, graphies percent-encodées comprises — C6.
    SegmentPointille { position: usize },
    /// Un chiffre hexadécimal minuscule dans un triplet — C7.1.
    TripletPercentMinuscule { position: usize },
    /// Un triplet codant un caractère non réservé — C7.2.
    PercentEncodageInutile { position: usize, octet: u8 },
    /// Un `%` qui n'ouvre pas un triplet bien formé — C7.3.
    TripletPercentMalForme { position: usize },
    /// `%00` — C7.3 (RFC 3986 §7.3).
    OctetNulEncode { position: usize },
    /// Un `?` suivi de rien — C8.
    RequeteVide { position: usize },
    /// Un octet hors de la grammaire du composant — C1, C3, C8.
    CaractereHorsGrammaire { position: usize, octet: u8 },
    /// Un `#` où que ce soit — C9.
    FragmentPresent { position: usize },
}

impl core::fmt::Display for ErreurSubject {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        match self {
            Self::OctetNonAscii { position, octet } => write!(
                f,
                "octet non ASCII à l'octet {position} : 0x{octet:02x} — un caractère hors US-ASCII est déjà percent-encodé quand le subject existe (ADR-0016 C1)"
            ),
            Self::SchemeNonHttps { position } => write!(
                f,
                "scheme non conforme à l'octet {position} : « {PREFIXE_CANONIQUE} » exigé, en minuscules (ADR-0016 C2)"
            ),
            Self::HoteMajuscule { position, octet } => write!(
                f,
                "majuscule dans l'hôte à l'octet {position} : 0x{octet:02x} — l'hôte est normalisé en minuscules à la construction (ADR-0016 C3)"
            ),
            Self::HotePercentEncode { position } => write!(
                f,
                "triplet percent dans l'hôte à l'octet {position} — refusé, jamais décodé (ADR-0016 C3)"
            ),
            Self::HoteLitteralAdresse { position } => write!(
                f,
                "littéral d'adresse à l'octet {position} — son interprétation dépend de la plateforme du lecteur, donc n'est pas recalculable hors ligne (ADR-0016 C3, ADR-0003)"
            ),
            Self::HoteNonAscii { position, octet } => write!(
                f,
                "hôte non ASCII à l'octet {position} : 0x{octet:02x} — un nom IDN est refusé, jamais converti (ADR-0016 C3)"
            ),
            Self::HoteVide { position } => write!(
                f,
                "hôte vide à l'octet {position} — une désignation sans autorité ne désigne rien (ADR-0016 C3)"
            ),
            Self::UserinfoPresent { position } => write!(
                f,
                "userinfo présent à l'octet {position} — interdit d'émission par RFC 9110 §4.2.4 (ADR-0016 C4)"
            ),
            Self::PortParDefautExplicite { position } => write!(
                f,
                "port par défaut explicite à l'octet {position} — le port 443 s'omet (ADR-0016 C5)"
            ),
            Self::PortNonDecimal { position } => write!(
                f,
                "port non décimal à l'octet {position} — décimal, sans zéro de tête, non vide (ADR-0016 C5)"
            ),
            Self::CheminVide { position } => write!(
                f,
                "chemin vide à l'octet {position} — un chemin vide s'écrit « / » à la construction (ADR-0016 C6)"
            ),
            Self::SegmentPointille { position } => write!(
                f,
                "segment pointillé à l'octet {position} — « . » et « .. » sont refusés, jamais retirés (ADR-0016 C6)"
            ),
            Self::TripletPercentMinuscule { position } => write!(
                f,
                "triplet percent en minuscules à l'octet {position} — chiffres hexadécimaux en majuscules (ADR-0016 C7.1)"
            ),
            Self::PercentEncodageInutile { position, octet } => write!(
                f,
                "percent-encodage inutile à l'octet {position} : le caractère 0x{octet:02x} n'est pas réservé, il est décodé à la construction (ADR-0016 C7.2)"
            ),
            Self::TripletPercentMalForme { position } => write!(
                f,
                "triplet percent mal formé à l'octet {position} — tout « % » ouvre deux chiffres hexadécimaux (ADR-0016 C7.3)"
            ),
            Self::OctetNulEncode { position } => write!(
                f,
                "octet nul encodé à l'octet {position} — « %00 » est refusé (ADR-0016 C7.3, RFC 3986 §7.3)"
            ),
            Self::RequeteVide { position } => write!(
                f,
                "requête vide à l'octet {position} — le « ? » nu est refusé (ADR-0016 C8)"
            ),
            Self::CaractereHorsGrammaire { position, octet } => write!(
                f,
                "caractère hors grammaire à l'octet {position} : 0x{octet:02x} (ADR-0016 C1/C3/C8)"
            ),
            Self::FragmentPresent { position } => write!(
                f,
                "fragment présent à l'octet {position} — un composant jamais émis vers l'origine n'a pas de place dans la désignation (ADR-0016 C9)"
            ),
        }
    }
}

impl core::error::Error for ErreurSubject {}

/// Le prédicat de canonicité — **fonction totale** sur toute suite d'octets.
///
/// Point de frontière au sens d'ADR-0010, point 6 : style *tolérant*,
/// précondition vide, tout écart devient une valeur d'erreur nommée. Il ne
/// transforme rien : C0 — « la normalisation a lieu une fois, à la construction,
/// dans l'adapter ».
pub fn subject_est_canonique(octets: &[u8]) -> Result<(), ErreurSubject> {
    // 1. C2 — le scheme, comparé aux octets exacts. Un `subject` plus court que
    // le préfixe, vide, ou en majuscules tombe ici.
    if octets.get(..PREFIXE_CANONIQUE.len()) != Some(PREFIXE_CANONIQUE.as_bytes()) {
        return Err(ErreurSubject::SchemeNonHttps { position: 0 });
    }
    let debut_autorite = PREFIXE_CANONIQUE.len();

    // 2. C9 — le `#`, où qu'il soit. Contrôlé avant la découpe : sans cela, un
    // `#` dans la requête serait rendu « hors grammaire », ce qui dirait moins.
    for (position, octet) in octets.iter().copied().enumerate() {
        if octet == b'#' {
            return Err(ErreurSubject::FragmentPresent { position });
        }
    }

    // 3. Découpe. L'autorité court jusqu'au premier `/` ou `?` ; le `#` n'existe
    // plus à ce point.
    let fin_autorite = premier_parmi(octets, debut_autorite, b"/?");
    controler_autorite(octets, debut_autorite, fin_autorite)?;

    // 4. Chemin et requête.
    let debut_requete = premier_parmi(octets, fin_autorite, b"?");
    controler_chemin(octets, fin_autorite, debut_requete)?;
    controler_requete(octets, debut_requete, octets.len())
}

/// L'**hôte** d'un `subject`, extrait par découpe — jamais réécrit.
///
/// Style *exigeant* au sens de Meyer (carte des frontières, `lib.rs`) : la
/// précondition — le `subject` satisfait [`subject_est_canonique`] — est établie
/// par le décodage, qui est la frontière. **C'est de là que vient la sûreté, et
/// de nulle part ailleurs.**
///
/// La fonction est **totale** (ADR-0010, point 1) — aucune entrée ne la fait
/// diverger — mais son repli ne couvre qu'un seul écart : l'**absence du
/// préfixe canonique**, pour laquelle elle rend la chaîne vide, c'est-à-dire
/// une valeur qu'aucune identité de serveur authentifiée n'égale. Elle ne rend
/// PAS la chaîne vide sur toute entrée hors forme : sur `https://` suivi de
/// n'importe quoi, elle découpe et rend ce qu'elle trouve, hôte non canonique
/// compris. Un appelant qui l'emploierait sans la précondition établie
/// obtiendrait donc une découpe, pas un refus — et c'est pourquoi la
/// précondition est nommée ici plutôt que supposée.
///
/// Elle ne normalise rien : ADR-0016 C0 place la normalisation à la
/// construction, et le rang du vérificateur ne fait que refuser.
pub fn hote_de_subject(subject: &str) -> &str {
    let Some(reste) = subject.strip_prefix(PREFIXE_CANONIQUE) else {
        return "";
    };
    // C1 : l'hôte court jusqu'au port, au chemin ou à la requête — les trois
    // délimiteurs que la grammaire admet après l'autorité.
    let fin = premier_parmi(reste.as_bytes(), 0, b":/?");
    reste.get(..fin).unwrap_or("")
}

/// L'autorité : `userinfo` interdit (C4), hôte (C3), port (C5).
fn controler_autorite(octets: &[u8], debut: usize, fin: usize) -> Result<(), ErreurSubject> {
    // C4 — un `@` dans l'autorité, quelle que soit sa place.
    let position_arobase = premier_parmi_borne(octets, debut, fin, b"@");
    if position_arobase < fin {
        return Err(ErreurSubject::UserinfoPresent {
            position: position_arobase,
        });
    }
    // C3 — les crochets d'abord : ils portent un `:` qui tromperait la découpe
    // du port (RFC 3986 §3.2.2 : « This is the only place where square bracket
    // characters are allowed in the URI syntax. »).
    let position_crochet = premier_parmi_borne(octets, debut, fin, b"[]");
    if position_crochet < fin {
        return Err(ErreurSubject::HoteLitteralAdresse {
            position: position_crochet,
        });
    }

    let fin_hote = premier_parmi_borne(octets, debut, fin, b":");
    controler_hote(octets, debut, fin_hote)?;
    if fin_hote < fin {
        controler_port(octets, fin_hote.saturating_add(1), fin)?;
    }
    Ok(())
}

/// L'hôte : nom enregistré ASCII minuscule, ni IDN, ni littéral, ni triplet.
fn controler_hote(octets: &[u8], debut: usize, fin: usize) -> Result<(), ErreurSubject> {
    if debut >= fin {
        return Err(ErreurSubject::HoteVide { position: debut });
    }
    let mut chiffres_et_points_seulement = true;
    let mut position = debut;
    while position < fin {
        let octet = octet_a(octets, position);
        if !octet.is_ascii() {
            return Err(ErreurSubject::HoteNonAscii { position, octet });
        }
        if octet == PERCENT {
            return Err(ErreurSubject::HotePercentEncode { position });
        }
        if octet.is_ascii_uppercase() {
            return Err(ErreurSubject::HoteMajuscule { position, octet });
        }
        if !(octet.is_ascii_lowercase()
            || octet.is_ascii_digit()
            || octet == b'-'
            || octet == POINT)
        {
            return Err(ErreurSubject::CaractereHorsGrammaire { position, octet });
        }
        if !(octet.is_ascii_digit() || octet == POINT) {
            chiffres_et_points_seulement = false;
        }
        position = position.saturating_add(1);
    }
    // C3 — la forme pointillée. RFC 3986 §7.4 documente que son interprétation
    // dépend de la plateforme (« many implementations allow dotted forms of
    // three numbers, wherein the last part is interpreted as a 16-bit
    // quantity ») : un hôte fait de chiffres et de points seuls n'est pas un nom
    // enregistré, c'est une adresse écrite en clair.
    if chiffres_et_points_seulement {
        return Err(ErreurSubject::HoteLitteralAdresse { position: debut });
    }
    // C3 encore — les graphies numériques que le drapeau ci-dessus ne voit
    // pas (revue G2 de phase C, trouvaille F1) : tout client conforme au
    // WHATWG résout `0x7f000001`, `0x7f.1` ou `1.2.3.0xff` en adresse IPv4
    // (pièce détenue, *ends in a number checker* : un dernier label « "0X"
    // or "0x", followed by zero or more ASCII hex digits » ou tout en
    // chiffres est un nombre). Une désignation dont l'interprétation dépend
    // du lecteur n'est pas recalculable (ADR-0003) : le dernier label non
    // vide qui EST un nombre au sens de cette pièce est refusé. Plus strict
    // que la grammaire, donc faux négatifs seulement (RFC 3986 §6.1).
    if dernier_label_est_un_nombre(octets, debut, fin) {
        return Err(ErreurSubject::HoteLitteralAdresse { position: debut });
    }
    Ok(())
}

/// Le *ends in a number checker* de la pièce WHATWG, transposé : le dernier
/// label non vide de l'hôte est un « nombre » s'il est entièrement fait de
/// chiffres ASCII, ou s'il ouvre par `0x`/`0X` suivi de zéro ou plusieurs
/// chiffres hexadécimaux. (Le point final éventuel — hôte en `exemple.` —
/// laisse un label vide qui n'est pas un nombre ; on regarde le dernier
/// label NON vide, comme la pièce le fait.)
fn dernier_label_est_un_nombre(octets: &[u8], debut: usize, fin: usize) -> bool {
    // Fin effective : ignore un unique point terminal.
    let mut fin_effective = fin;
    if fin_effective > debut && octet_a(octets, fin_effective.saturating_sub(1)) == POINT {
        fin_effective = fin_effective.saturating_sub(1);
    }
    if fin_effective <= debut {
        return false;
    }
    // Début du dernier label : après le dernier point restant.
    let mut debut_label = debut;
    let mut position = debut;
    while position < fin_effective {
        if octet_a(octets, position) == POINT {
            debut_label = position.saturating_add(1);
        }
        position = position.saturating_add(1);
    }
    if debut_label >= fin_effective {
        return false;
    }
    // Tout en chiffres ASCII ?
    let mut tout_chiffres = true;
    let mut position = debut_label;
    while position < fin_effective {
        if !octet_a(octets, position).is_ascii_digit() {
            tout_chiffres = false;
        }
        position = position.saturating_add(1);
    }
    if tout_chiffres {
        return true;
    }
    // Ouvre par 0x/0X suivi de zéro ou plusieurs chiffres hexadécimaux ?
    // (La majuscule X est déjà refusée en amont par HoteMajuscule ; on la
    // couvre quand même — ce prédicat ne dépend pas de l'ordre des contrôles.)
    if octet_a(octets, debut_label) == b'0'
        && fin_effective > debut_label.saturating_add(1)
        && matches!(octet_a(octets, debut_label.saturating_add(1)), b'x' | b'X')
    {
        let mut position = debut_label.saturating_add(2);
        while position < fin_effective {
            if !octet_a(octets, position).is_ascii_hexdigit() {
                return false;
            }
            position = position.saturating_add(1);
        }
        return true;
    }
    false
}

/// Le port : décimal, sans zéro de tête, jamais 443.
fn controler_port(octets: &[u8], debut: usize, fin: usize) -> Result<(), ErreurSubject> {
    if debut >= fin {
        return Err(ErreurSubject::PortNonDecimal { position: debut });
    }
    let mut position = debut;
    while position < fin {
        if !octet_a(octets, position).is_ascii_digit() {
            return Err(ErreurSubject::PortNonDecimal { position });
        }
        position = position.saturating_add(1);
    }
    if octets.get(debut).copied() == Some(b'0') {
        return Err(ErreurSubject::PortNonDecimal { position: debut });
    }
    if octets.get(debut..fin) == Some(PORT_PAR_DEFAUT) {
        return Err(ErreurSubject::PortParDefautExplicite { position: debut });
    }
    Ok(())
}

/// Le chemin : jamais vide, `pchar`/`/` seulement, triplets de C7, aucun segment
/// pointillé.
fn controler_chemin(octets: &[u8], debut: usize, fin: usize) -> Result<(), ErreurSubject> {
    if debut >= fin {
        return Err(ErreurSubject::CheminVide { position: debut });
    }
    controler_octets(octets, debut, fin, Composant::Chemin)?;

    // C6 — les segments, contrôlés APRÈS C7, comme l'ADR l'écrit. Un segment
    // s'ouvre après chaque `/`.
    let mut debut_segment = debut.saturating_add(1);
    let mut position = debut_segment;
    while position <= fin {
        let fini = position >= fin;
        let separateur = octets.get(position).copied() == Some(b'/');
        if fini || separateur {
            if segment_est_pointille(octets, debut_segment, position) {
                return Err(ErreurSubject::SegmentPointille {
                    position: debut_segment,
                });
            }
            debut_segment = position.saturating_add(1);
        }
        position = position.saturating_add(1);
    }
    Ok(())
}

/// La requête : absente, ou présente et non vide, reprise **verbatim**.
fn controler_requete(octets: &[u8], debut: usize, fin: usize) -> Result<(), ErreurSubject> {
    if debut >= fin {
        // Pas de `?` du tout : la requête est absente, ce qui est licite.
        return Ok(());
    }
    let debut_valeur = debut.saturating_add(1);
    if debut_valeur >= fin {
        return Err(ErreurSubject::RequeteVide { position: debut });
    }
    controler_octets(octets, debut_valeur, fin, Composant::Requete)
}

/// Le composant dont on contrôle les octets — il décide du jeu admis.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Composant {
    Chemin,
    Requete,
}

impl Composant {
    /// Vrai si l'octet est admis **hors triplet** dans ce composant.
    ///
    /// Chemin : `path-abempty = *( "/" segment )`, `segment = *pchar`.
    /// Requête : `query = *( pchar / "/" / "?" )` (RFC 3986 §3.3, §3.4).
    fn admet(self, octet: u8) -> bool {
        match self {
            Self::Chemin => est_pchar_hors_triplet(octet) || octet == b'/',
            Self::Requete => est_pchar_hors_triplet(octet) || octet == b'/' || octet == b'?',
        }
    }
}

/// Les octets d'un composant : ASCII, grammaire, et les trois règles de C7.
fn controler_octets(
    octets: &[u8],
    debut: usize,
    fin: usize,
    composant: Composant,
) -> Result<(), ErreurSubject> {
    let mut position = debut;
    while position < fin {
        let octet = octet_a(octets, position);
        if !octet.is_ascii() {
            return Err(ErreurSubject::OctetNonAscii { position, octet });
        }
        if octet == PERCENT {
            controler_triplet(octets, position, fin)?;
            position = position.saturating_add(3);
            continue;
        }
        if !composant.admet(octet) {
            return Err(ErreurSubject::CaractereHorsGrammaire { position, octet });
        }
        position = position.saturating_add(1);
    }
    Ok(())
}

/// Un triplet `pct-encoded` : deux chiffres hexadécimaux majuscules, ni `%00`,
/// ni le codage d'un caractère non réservé.
fn controler_triplet(octets: &[u8], position: usize, fin: usize) -> Result<(), ErreurSubject> {
    let position_haut = position.saturating_add(1);
    let position_bas = position.saturating_add(2);
    if position_bas >= fin {
        return Err(ErreurSubject::TripletPercentMalForme { position });
    }
    let haut = octet_a(octets, position_haut);
    let bas = octet_a(octets, position_bas);
    if !(haut.is_ascii_hexdigit() && bas.is_ascii_hexdigit()) {
        return Err(ErreurSubject::TripletPercentMalForme { position });
    }
    if haut.is_ascii_lowercase() || bas.is_ascii_lowercase() {
        return Err(ErreurSubject::TripletPercentMinuscule { position });
    }
    let valeur = match (valeur_hexadecimale(haut), valeur_hexadecimale(bas)) {
        (Some(haut), Some(bas)) => haut.wrapping_shl(4) | bas,
        // Inatteignable : `is_ascii_hexdigit` a déjà été établi. Refus plutôt que
        // divergence (ADR-0010, points 3 et 5).
        _ => return Err(ErreurSubject::TripletPercentMalForme { position }),
    };
    if valeur == 0 {
        return Err(ErreurSubject::OctetNulEncode { position });
    }
    if est_non_reserve(valeur) {
        return Err(ErreurSubject::PercentEncodageInutile {
            position,
            octet: valeur,
        });
    }
    Ok(())
}

/// Vrai si le segment `[debut, fin)` décode en `.` ou `..`.
///
/// Sans allocation : un segment pointillé fait au plus deux caractères décodés,
/// donc le comptage suffit. Les graphies encodées sont incluses (WHATWG, pièce
/// détenue : « ".." or an ASCII case-insensitive match for ".%2e", "%2e.", or
/// "%2e%2e" ») — elles sont déjà refusées par C7.2, et l'ADR demande le contrôle
/// quand même : la règle ne dépend pas de l'ordre où elle est écrite.
fn segment_est_pointille(octets: &[u8], debut: usize, fin: usize) -> bool {
    let mut points = 0usize;
    let mut position = debut;
    while position < fin {
        let octet = octet_a(octets, position);
        let (valeur, largeur) = if octet == PERCENT {
            // Borné par `fin` (revue G2 de phase C, trouvaille F2) : un
            // triplet qui déborderait le segment lirait des octets de la
            // requête. `controler_octets` (C7, exécuté AVANT — ordre
            // contractuel de `controler_chemin`) refuse déjà tout triplet
            // débordant ; cette borne rend la propriété locale vraie sans
            // dépendre de cet ordre.
            if position.saturating_add(2) >= fin {
                return false;
            }
            let haut = valeur_hexadecimale(octet_a(octets, position.saturating_add(1)));
            let bas = valeur_hexadecimale(octet_a(octets, position.saturating_add(2)));
            match (haut, bas) {
                (Some(haut), Some(bas)) => (haut.wrapping_shl(4) | bas, 3usize),
                _ => return false,
            }
        } else {
            (octet, 1usize)
        };
        if valeur != POINT {
            return false;
        }
        points = points.saturating_add(1);
        if points > 2 {
            return false;
        }
        position = position.saturating_add(largeur);
    }
    points == 1 || points == 2
}

/// `unreserved = ALPHA / DIGIT / "-" / "." / "_" / "~"` (RFC 3986 §2.3).
fn est_non_reserve(octet: u8) -> bool {
    octet.is_ascii_alphanumeric()
        || octet == b'-'
        || octet == POINT
        || octet == b'_'
        || octet == b'~'
}

/// `sub-delims = "!" / "$" / "&" / "'" / "(" / ")" / "*" / "+" / "," / ";" / "="`
/// (RFC 3986 §2.2).
fn est_sous_delimiteur(octet: u8) -> bool {
    matches!(
        octet,
        b'!' | b'$' | b'&' | b'\'' | b'(' | b')' | b'*' | b'+' | b',' | b';' | b'='
    )
}

/// `pchar = unreserved / pct-encoded / sub-delims / ":" / "@"` (RFC 3986 §3.3),
/// privé du triplet, qui a son propre contrôle.
fn est_pchar_hors_triplet(octet: u8) -> bool {
    est_non_reserve(octet) || est_sous_delimiteur(octet) || octet == b':' || octet == b'@'
}

/// Valeur d'un chiffre hexadécimal, ou `None`.
fn valeur_hexadecimale(octet: u8) -> Option<u8> {
    match octet {
        b'0'..=b'9' => Some(octet.wrapping_sub(b'0')),
        b'A'..=b'F' => Some(octet.wrapping_sub(b'A').wrapping_add(10)),
        b'a'..=b'f' => Some(octet.wrapping_sub(b'a').wrapping_add(10)),
        _ => None,
    }
}

/// Position du premier octet de `cibles` à partir de `debut`, ou la longueur.
fn premier_parmi(octets: &[u8], debut: usize, cibles: &[u8]) -> usize {
    premier_parmi_borne(octets, debut, octets.len(), cibles)
}

/// Même chose, bornée à `fin`.
fn premier_parmi_borne(octets: &[u8], debut: usize, fin: usize, cibles: &[u8]) -> usize {
    let mut position = debut;
    while position < fin {
        if cibles.contains(&octet_a(octets, position)) {
            return position;
        }
        position = position.saturating_add(1);
    }
    fin
}

/// L'octet à une position, ou `0` si la position est hors de la tranche.
///
/// Le repli n'est jamais atteint, et la raison se nomme (revue G2 de phase C,
/// trouvaille F2 — l'ancien argument « toutes les boucles sont bornées »
/// était faux à un site) : les boucles de composant sont bornées par leur
/// `fin`, et les deux lectures en avant de `segment_est_pointille` sont
/// bornées par la garde locale de débordement PLUS la précondition établie
/// par `controler_octets` (tout `%` de `[debut, fin)` ouvre un triplet
/// entièrement contenu — l'ordre C7-puis-C6 de `controler_chemin` est
/// contractuel). Si le repli était atteint malgré tout : `0` n'appartient à
/// aucun jeu admis d'aucun composant — il fait **refuser** dans les jeux de
/// caractères ; dans `segment_est_pointille`, `valeur_hexadecimale(0)` rend
/// `None` et la fonction rend `false`, c'est-à-dire « pas un segment
/// pointillé » : cette direction-là est rattrapée par la garde locale
/// ci-dessus, qui ne dépend d'aucun ordre.
///
/// Cette forme remplace un itérateur `impl Iterator<..> + '_` : la borne de
/// trait `+` est la limite lexicale que S-G3 nomme elle-même dans sa
/// documentation. La gate ne se contourne pas — le code se plie.
fn octet_a(octets: &[u8], position: usize) -> u8 {
    octets.get(position).copied().unwrap_or(0)
}
