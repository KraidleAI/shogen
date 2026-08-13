//! L'**empreinte** des octets exacts — SHA-256, écrite à la main.
//!
//! Rattachement (G0) : **ADR-0005, règle 1** — « le hash des octets exacts est
//! toujours porté — il lie le témoignage à sa preuve de transport, sans
//! exception » ; **ADR-0010** (cœur pur, total, sans I/O, sans panique) ;
//! **ADR-0012 D3** (dépendances minimales) ; draft `scratch/adr-0018-draft.md`
//! pour l'arbitrage « implémentation manuelle » contre « crate épinglée » —
//! l'instruction est versée, la décision appartient à l'orchestrateur.
//!
//! La spécification suivie est FIPS 180-4 (*Secure Hash Standard*, NIST,
//! août 2015), §4.1.2 (les six fonctions logiques), §4.2.2 (les soixante-quatre
//! constantes), §5.1.1 (le rembourrage), §5.3.3 (la valeur initiale) et §6.2.2
//! (le calcul). Les constantes ci-dessous sont **transcrites de la pièce**, pas
//! de mémoire ; ce qui **établit** la transcription n'est pas la transcription
//! elle-même mais les vecteurs officiels de `tests/empreinte_vecteurs.rs` : une
//! seule constante fausse fait tomber les neuf.
//!
//! Ce que ce module **n'est pas** : un cadre d'agilité d'algorithme. L'empreinte
//! du témoignage est SHA-256 et rien d'autre ; aucun champ ne nomme
//! l'algorithme, donc aucun lot ne peut en négocier un autre. Le jour où un
//! second algorithme entre, il entre par une ADR et par un champ, jamais par une
//! branche silencieuse.
//!
//! Régime d'assurance : *tested (avec compte)*. Jamais *proven* : rien ici
//! n'établit la résistance de SHA-256, seulement la conformité de ce code aux
//! vecteurs détenus.
//!
//! Ce qui rattrape un condensé faux en aval (revue G2 de phase C,
//! trouvaille F3 — l'argument le plus fort, porté ici pour qu'il ne se
//! perde pas) : `empreinte_sha256` rend `[u8; 32]`, pas un `Result` — un
//! repli atteint produirait un condensé faux **sans signal**. Mais toutes
//! les comparaisons de `verification.rs` se font contre des empreintes
//! calculées **hors de cette crate** (le constat du binaire compagnon) :
//! un condensé faux d'un seul côté ne peut produire qu'un **refus**. Le
//! cas « les deux côtés faux ensemble » exigerait la même faute dans deux
//! implémentations indépendantes — c'est un fail-closed par comparaison
//! tierce, pas par typage. (Option S4, aux côtés de la question `sha2` :
//! typer la précondition — `bloc: &[u8; 64]` via `try_from` à erreur
//! nommée — supprimerait l'argument au lieu de le documenter.)

/// Longueur d'une empreinte SHA-256, en octets (FIPS 180-4 §1 : « 256 »).
use alloc::string::String;
use alloc::vec::Vec;

pub const OCTETS_D_EMPREINTE: usize = 32;

/// Longueur d'un bloc de message, en octets (512 bits — FIPS 180-4 §5.1.1).
const OCTETS_DE_BLOC: usize = 64;

/// Longueur du préfixe de bloc qui précède le champ de longueur (448 bits).
const OCTETS_AVANT_LONGUEUR: usize = 56;

/// Même seuil, décalé d'un bloc : cas où le rembourrage déborde.
const OCTETS_AVANT_LONGUEUR_DEBORDE: usize = 120;

/// Le premier octet de rembourrage : le bit « 1 » suivi de sept zéros
/// (FIPS 180-4 §5.1.1 — « Append the bit "1" to the end of the message »).
const OCTET_DE_REMBOURRAGE: u8 = 0x80;

/// La valeur de hachage : huit mots de 32 bits, **nommés** plutôt qu'indexés.
///
/// Un tableau conviendrait au calcul ; il ne convient pas à la discipline du
/// dépôt — `let [a, b, …] = tableau` est une forme que S-G3 lit comme une
/// indexation, et la gate ne se contourne pas. Les champs nommés donnent en
/// prime la lisibilité que FIPS 180-4 §6.2.2 emploie lui-même (a, b, …, h).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct Valeur {
    a: u32,
    b: u32,
    c: u32,
    d: u32,
    e: u32,
    f: u32,
    g: u32,
    h: u32,
}

/// Valeur initiale H(0), FIPS 180-4 §5.3.3, transcrite de la pièce.
const VALEUR_INITIALE: Valeur = Valeur {
    a: 0x6a09_e667,
    b: 0xbb67_ae85,
    c: 0x3c6e_f372,
    d: 0xa54f_f53a,
    e: 0x510e_527f,
    f: 0x9b05_688c,
    g: 0x1f83_d9ab,
    h: 0x5be0_cd19,
};

/// Les soixante-quatre constantes K{256}, FIPS 180-4 §4.2.2.
///
/// La pièce les imprime en tableau de huit lignes sur huit colonnes lu « from
/// left to right » ; l'ordre rétabli ici est K0..K63.
const CONSTANTES: [u32; 64] = [
    0x428a_2f98,
    0x7137_4491,
    0xb5c0_fbcf,
    0xe9b5_dba5,
    0x3956_c25b,
    0x59f1_11f1,
    0x923f_82a4,
    0xab1c_5ed5,
    0xd807_aa98,
    0x1283_5b01,
    0x2431_85be,
    0x550c_7dc3,
    0x72be_5d74,
    0x80de_b1fe,
    0x9bdc_06a7,
    0xc19b_f174,
    0xe49b_69c1,
    0xefbe_4786,
    0x0fc1_9dc6,
    0x240c_a1cc,
    0x2de9_2c6f,
    0x4a74_84aa,
    0x5cb0_a9dc,
    0x76f9_88da,
    0x983e_5152,
    0xa831_c66d,
    0xb003_27c8,
    0xbf59_7fc7,
    0xc6e0_0bf3,
    0xd5a7_9147,
    0x06ca_6351,
    0x1429_2967,
    0x27b7_0a85,
    0x2e1b_2138,
    0x4d2c_6dfc,
    0x5338_0d13,
    0x650a_7354,
    0x766a_0abb,
    0x81c2_c92e,
    0x9272_2c85,
    0xa2bf_e8a1,
    0xa81a_664b,
    0xc24b_8b70,
    0xc76c_51a3,
    0xd192_e819,
    0xd699_0624,
    0xf40e_3585,
    0x106a_a070,
    0x19a4_c116,
    0x1e37_6c08,
    0x2748_774c,
    0x34b0_bcb5,
    0x391c_0cb3,
    0x4ed8_aa4a,
    0x5b9c_ca4f,
    0x682e_6ff3,
    0x748f_82ee,
    0x78a5_636f,
    0x84c8_7814,
    0x8cc7_0208,
    0x90be_fffa,
    0xa450_6ceb,
    0xbef9_a3f7,
    0xc671_78f2,
];

/// Empreinte SHA-256 d'une suite d'octets quelconque.
///
/// **Totale** : définie sur tout `&[u8]`, sans panique, sans I/O, sans horloge.
/// Aucune allocation n'est dimensionnée par la longueur du message : le message
/// est consommé par blocs de 64 octets et seule la **queue** (au plus 128
/// octets, borne fixe) est matérialisée.
pub fn empreinte_sha256(message: &[u8]) -> [u8; OCTETS_D_EMPREINTE] {
    let mut etat = VALEUR_INITIALE;
    let mut blocs = message.chunks_exact(OCTETS_DE_BLOC);
    for bloc in blocs.by_ref() {
        etat = comprimer(etat, bloc);
    }
    let reste = blocs.remainder();

    // Rembourrage, FIPS 180-4 §5.1.1 : l'octet 0x80, puis des zéros jusqu'à
    // 56 octets modulo 64, puis la longueur en bits sur 64 bits gros-boutistes.
    // La cible est choisie par branche plutôt que par un reste de division :
    // `reste` vit dans 0..64 par construction de `chunks_exact`.
    let mut queue: Vec<u8> = Vec::with_capacity(OCTETS_DE_BLOC.saturating_mul(2));
    queue.extend_from_slice(reste);
    queue.push(OCTET_DE_REMBOURRAGE);
    let cible = if reste.len() < OCTETS_AVANT_LONGUEUR {
        OCTETS_AVANT_LONGUEUR
    } else {
        OCTETS_AVANT_LONGUEUR_DEBORDE
    };
    while queue.len() < cible {
        queue.push(0);
    }
    // Longueur en bits. `saturating_mul` est total ; le débordement exigerait un
    // message de 2^61 octets, que la mémoire d'une machine ne porte pas.
    let bits = u64::try_from(message.len())
        .unwrap_or(u64::MAX)
        .saturating_mul(8);
    queue.extend_from_slice(&bits.to_be_bytes());

    for bloc in queue.chunks_exact(OCTETS_DE_BLOC) {
        etat = comprimer(etat, bloc);
    }
    concatener(etat)
}

/// Un mot du planning de message, par indice.
///
/// Le repli `0` n'est **jamais** atteint : `planning` porte exactement les mots
/// déjà produits, et chaque appel se fait sur un indice strictement inférieur à
/// sa longueur. Il n'existe pas de « refus » possible ici (la fonction rend un
/// condensé, pas un `Result`) : ce que l'inatteignabilité doit à la preuve, les
/// neuf vecteurs officiels le paient — un repli atteint changerait le condensé
/// et les ferait tomber.
fn mot_de(planning: &[u32], indice: usize) -> u32 {
    planning.get(indice).copied().unwrap_or(0)
}

/// `Ch(x, y, z)` — FIPS 180-4 §4.1.2, équation (4.2).
fn choix(x: u32, y: u32, z: u32) -> u32 {
    (x & y) ^ (!x & z)
}

/// `Maj(x, y, z)` — FIPS 180-4 §4.1.2, équation (4.3).
fn majorite(x: u32, y: u32, z: u32) -> u32 {
    (x & y) ^ (x & z) ^ (y & z)
}

/// `Σ0{256}(x)` — FIPS 180-4 §4.1.2, équation (4.4).
fn grand_sigma0(x: u32) -> u32 {
    x.rotate_right(2) ^ x.rotate_right(13) ^ x.rotate_right(22)
}

/// `Σ1{256}(x)` — FIPS 180-4 §4.1.2, équation (4.5).
fn grand_sigma1(x: u32) -> u32 {
    x.rotate_right(6) ^ x.rotate_right(11) ^ x.rotate_right(25)
}

/// `σ0{256}(x)` — FIPS 180-4 §4.1.2, équation (4.6).
fn petit_sigma0(x: u32) -> u32 {
    x.rotate_right(7) ^ x.rotate_right(18) ^ x.wrapping_shr(3)
}

/// `σ1{256}(x)` — FIPS 180-4 §4.1.2, équation (4.7).
fn petit_sigma1(x: u32) -> u32 {
    x.rotate_right(17) ^ x.rotate_right(19) ^ x.wrapping_shr(10)
}

/// Le calcul d'un bloc — FIPS 180-4 §6.2.2, étapes 1 à 4.
///
/// Style **exigeant** (ADR-0010, point 6) : `bloc` fait exactement 64 octets,
/// précondition établie par le seul appelant (`chunks_exact`), non revérifiée.
fn comprimer(etat: Valeur, bloc: &[u8]) -> Valeur {
    // Étape 1 — le planning de message {Wt}.
    let mut planning: Vec<u32> = Vec::with_capacity(CONSTANTES.len());
    for morceau in bloc.chunks_exact(4) {
        let mut mot: u32 = 0;
        for octet in morceau.iter().copied() {
            mot = mot.wrapping_shl(8) | u32::from(octet);
        }
        planning.push(mot);
    }
    let mut indice = 16usize;
    while indice < CONSTANTES.len() {
        let mot = petit_sigma1(mot_de(&planning, indice.wrapping_sub(2)))
            .wrapping_add(mot_de(&planning, indice.wrapping_sub(7)))
            .wrapping_add(petit_sigma0(mot_de(&planning, indice.wrapping_sub(15))))
            .wrapping_add(mot_de(&planning, indice.wrapping_sub(16)));
        planning.push(mot);
        indice = indice.wrapping_add(1);
    }

    // Étape 2 — les huit variables de travail.
    let mut a = etat.a;
    let mut b = etat.b;
    let mut c = etat.c;
    let mut d = etat.d;
    let mut e = etat.e;
    let mut f = etat.f;
    let mut g = etat.g;
    let mut h = etat.h;

    // Étape 3 — les soixante-quatre tours. L'addition est modulo 2^32
    // (FIPS 180-4 §6.2.2 : « Addition (+) is performed modulo 2^32 ») : c'est
    // `wrapping_add`, et c'est la seule arithmétique licite ici.
    for (tour, constante) in CONSTANTES.iter().copied().enumerate() {
        let t1 = h
            .wrapping_add(grand_sigma1(e))
            .wrapping_add(choix(e, f, g))
            .wrapping_add(constante)
            .wrapping_add(mot_de(&planning, tour));
        let t2 = grand_sigma0(a).wrapping_add(majorite(a, b, c));
        h = g;
        g = f;
        f = e;
        e = d.wrapping_add(t1);
        d = c;
        c = b;
        b = a;
        a = t1.wrapping_add(t2);
    }

    // Étape 4 — la valeur de hachage intermédiaire.
    Valeur {
        a: etat.a.wrapping_add(a),
        b: etat.b.wrapping_add(b),
        c: etat.c.wrapping_add(c),
        d: etat.d.wrapping_add(d),
        e: etat.e.wrapping_add(e),
        f: etat.f.wrapping_add(f),
        g: etat.g.wrapping_add(g),
        h: etat.h.wrapping_add(h),
    }
}

/// Huit mots de 32 bits en trente-deux octets gros-boutistes.
///
/// Écrit octet par octet, sans indexation ni déstructuration de tableau : la
/// contrainte de S-G3 devient ici une écriture qui **montre** l'ordre des octets
/// au lieu de le cacher derrière une conversion.
fn concatener(valeur: Valeur) -> [u8; OCTETS_D_EMPREINTE] {
    let (a0, a1, a2, a3) = quatre_octets(valeur.a);
    let (b0, b1, b2, b3) = quatre_octets(valeur.b);
    let (c0, c1, c2, c3) = quatre_octets(valeur.c);
    let (d0, d1, d2, d3) = quatre_octets(valeur.d);
    let (e0, e1, e2, e3) = quatre_octets(valeur.e);
    let (f0, f1, f2, f3) = quatre_octets(valeur.f);
    let (g0, g1, g2, g3) = quatre_octets(valeur.g);
    let (h0, h1, h2, h3) = quatre_octets(valeur.h);
    [
        a0, a1, a2, a3, b0, b1, b2, b3, c0, c1, c2, c3, d0, d1, d2, d3, e0, e1, e2, e3, f0, f1, f2,
        f3, g0, g1, g2, g3, h0, h1, h2, h3,
    ]
}

/// Les quatre octets d'un mot, du plus significatif au moins significatif.
fn quatre_octets(mot: u32) -> (u8, u8, u8, u8) {
    (
        octet_de(mot, 24),
        octet_de(mot, 16),
        octet_de(mot, 8),
        octet_de(mot, 0),
    )
}

/// L'octet d'un mot à un décalage de bits. `wrapping_shr` est total ; le masque
/// rend la troncature exacte, jamais approchée.
fn octet_de(mot: u32, decalage: u32) -> u8 {
    (mot.wrapping_shr(decalage) & 0xFF) as u8
}

/// Rend une empreinte en hexadécimal minuscule — la graphie des vecteurs
/// officiels et des messages d'erreur.
pub fn empreinte_en_hexadecimal(empreinte: &[u8; OCTETS_D_EMPREINTE]) -> String {
    let mut rendu = String::with_capacity(OCTETS_D_EMPREINTE.saturating_mul(2));
    for octet in empreinte.iter().copied() {
        rendu.push(chiffre_hexadecimal(octet.wrapping_shr(4)));
        rendu.push(chiffre_hexadecimal(octet & 0x0F));
    }
    rendu
}

/// Le chiffre hexadécimal minuscule d'un quartet. Total : tout `u8` hors 0..16
/// est impossible par construction des deux appels, et rend `'0'` plutôt qu'une
/// divergence.
fn chiffre_hexadecimal(quartet: u8) -> char {
    match quartet {
        0 => '0',
        1 => '1',
        2 => '2',
        3 => '3',
        4 => '4',
        5 => '5',
        6 => '6',
        7 => '7',
        8 => '8',
        9 => '9',
        10 => 'a',
        11 => 'b',
        12 => 'c',
        13 => 'd',
        14 => 'e',
        15 => 'f',
        _ => '0',
    }
}
