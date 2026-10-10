//! **Distillation du corpus de fuzz** — 13 §7 dette 3 ; SHOGEN-FUZZ-DISTILLATION-1 (ADR-0028
//! annexe A, lot FUZZ).
//!
//! Les campagnes instrumentées atteignent des arêtes que le corpus dirigé n'atteint pas. Plutôt
//! que de verser leurs entrées, illisibles, la distillation nomme les formes qu'elles exercent —
//! surtout les refus nommés du vérificateur, à chaque profondeur de ses surfaces — et les écrit en
//! graines `dirigee-distillee-*`, régénérées par `cargo xtask fuzz-corpus`. Chaque graine porte un
//! fragment du classement que le vérificateur doit en rendre (`attendu`), contrôlé par
//! `xtask/tests/distillation.rs`. Mesure et seuil : `crates/shogen-verifier/fuzz-corpus/README.md`.
//!
//! La gate `cargo xtask fuzz-distillation` juge deux cartes `afl-showmap -C`, sans et avec les
//! graines distillées, et refuse sous ⌈1074 × 471/789⌉ = 642 arêtes gagnées. Hors de `verify`
//! comme `fuzz` : la mesure exige la cible instrumentée (job `cargo-afl` de `fuzz.yml`, Linux).

use crate::fuzz::{constat_dirige, temoignage_canonique_exemple};
use shogen_core::{Attestor, Temoignage, encoder_temoignage_canonique};
use std::collections::BTreeSet;
use std::path::Path;

/// Une graine distillée : son nom au corpus, ses octets, et ce que le vérificateur doit en dire.
pub struct Graine {
    pub nom: String,
    pub octets: Vec<u8>,
    pub attendu: &'static str,
}

/// Les graines distillées, dans un ordre fixe.
pub fn graines() -> Vec<Graine> {
    let canonique = encoder_temoignage_canonique(&temoignage_canonique_exemple());
    let mut graines = Vec::new();
    let mut ajouter = |nom: String, octets, attendu| {
        let nom = format!("dirigee-distillee-{nom}");
        graines.push(Graine {
            nom,
            octets,
            attendu,
        });
    };
    // 1. Le lot canonique dont seul `subject` change : une règle d'ADR-0016 par graine.
    for (nom, subject, attendu) in SUBJECTS {
        let mut temoignage = temoignage_canonique_exemple();
        temoignage.subject = String::from(subject);
        let octets = encoder_temoignage_canonique(&temoignage);
        ajouter(format!("subject-{nom}.bin"), octets, attendu);
    }
    // 2. Le lot canonique dont un champ change : un refus de contenu par champ.
    for (nom, alterer, attendu) in ALTERATIONS {
        let mut temoignage = temoignage_canonique_exemple();
        alterer(&mut temoignage);
        let octets = encoder_temoignage_canonique(&temoignage);
        ajouter(format!("lot-{nom}.bin"), octets, attendu);
    }
    // 3. Le lot canonique dont un en-tête ou une clé change : un refus de structure par carte.
    for (nom, motif, remplacement, attendu) in SUBSTITUTIONS {
        let octets = remplacer(&canonique, motif, remplacement);
        ajouter(format!("lot-{nom}.bin"), octets, attendu);
    }
    // 4. Le lot canonique tronqué juste après une clé : la valeur manque à cette profondeur.
    for cle in CLES_TRONQUEES {
        let mut motif = vec![0x60 | (cle.len() as u8)];
        motif.extend_from_slice(cle.as_bytes());
        let fin = position(&canonique, &motif).map_or(0, |debut| debut + motif.len());
        let octets = canonique.get(..fin).unwrap_or_default().to_vec();
        let nom = format!("lot-tronque-apres-{cle}.bin");
        ajouter(nom, octets, "Refuse(FinPrematuree");
    }
    // 5. Le constat accepté (ADR-0015 pt 13) dont un fragment change : un refus nommé par graine.
    let constat = constat_dirige("041a2b3c");
    for (nom, motif, remplacement, attendu) in CONSTATS {
        let octets = constat.replacen(motif, remplacement, 1).into_bytes();
        ajouter(format!("constat-{nom}.txt"), octets, attendu);
    }
    // 6. Les bords du décodeur CBOR que le corpus dirigé ne portait pas, puis le registre en texte
    //    riche : toutes les largeurs UTF-8, les blancs Unicode, les fins de ligne mêlées.
    for (nom, octets, attendu) in CBOR {
        ajouter(format!("cbor-{nom}.bin"), octets.to_vec(), attendu);
    }
    for (nom, texte, attendu) in REGISTRES {
        let octets = texte.as_bytes().to_vec();
        ajouter(format!("registre-{nom}.txt"), octets, attendu);
    }
    graines
}

/// Remplace la première occurrence de `motif` ; sans occurrence, les octets restent intacts, et
/// le test du classement le voit.
fn remplacer(octets: &[u8], motif: &[u8], remplacement: &[u8]) -> Vec<u8> {
    match position(octets, motif) {
        Some(debut) => {
            let (tete, reste) = octets.split_at(debut);
            let queue = reste.get(motif.len()..).unwrap_or_default();
            [tete, remplacement, queue].concat()
        }
        None => octets.to_vec(),
    }
}

fn position(octets: &[u8], motif: &[u8]) -> Option<usize> {
    let largeur = motif.len().max(1);
    octets.windows(largeur).position(|fenetre| fenetre == motif)
}

/// 13 §7 dette 3 : « ≥ 471 des 789 arêtes » que le corpus dérivé atteignait hors du corpus dirigé.
pub const FRACTION: (u64, u64) = (471, 789);

/// Les arêtes du corpus dérivé hors du corpus dirigé d'origine, mesurées le 2026-10-09 (README du
/// corpus) : la base de la fraction sur le binaire courant, qui n'est plus celui de 471/789.
pub const ARETES_DU_DERIVE: u64 = 1074;

/// Le seuil de la gate, en arêtes gagnées par les graines distillées : ⌈1074 × 471 / 789⌉.
pub fn seuil() -> u64 {
    ARETES_DU_DERIVE
        .saturating_mul(FRACTION.0)
        .div_ceil(FRACTION.1)
}

/// Lit une carte d'`afl-showmap -C` : une ligne `arête:compte` par arête atteinte, compte non nul.
/// Ligne hors forme, arête répétée ou carte vide : faute, la gate refuse de conclure.
pub fn lire_carte(texte: &str) -> Result<BTreeSet<u32>, String> {
    let mut aretes = BTreeSet::new();
    for (index, ligne) in texte.lines().enumerate() {
        let lue = ligne.split_once(':').and_then(|(arete, compte)| {
            Some((arete.parse::<u32>().ok()?, compte.parse::<u32>().ok()?))
        });
        match lue {
            Some((arete, compte)) if compte > 0 && aretes.insert(arete) => {}
            _ => {
                return Err(format!(
                    "ligne {} hors forme ou répétée : {ligne}",
                    index + 1
                ));
            }
        }
    }
    if aretes.is_empty() {
        return Err(String::from("carte vide, aucune arête"));
    }
    Ok(aretes)
}

/// La mesure, imprimée avant le verdict (ADR-0013, point 2).
pub struct Mesure {
    /// Arêtes du corpus sans les graines distillées.
    pub base: usize,
    /// Arêtes du corpus entier.
    pub corpus: usize,
    /// Arêtes du corpus entier hors de la base : l'apport des graines distillées.
    pub gagnees: usize,
    /// Arêtes de la base absentes du corpus entier : non nul, les deux cartes sont incomparables.
    pub perdues: usize,
}

impl Mesure {
    pub fn de(base: &BTreeSet<u32>, corpus: &BTreeSet<u32>) -> Self {
        let gagnees = corpus.difference(base).count();
        let perdues = base.difference(corpus).count();
        let (base, corpus) = (base.len(), corpus.len());
        Self {
            base,
            corpus,
            gagnees,
            perdues,
        }
    }

    /// Vert si les graines distillées gagnent au moins le seuil, sur deux cartes comparables.
    pub fn vert(&self) -> bool {
        self.perdues == 0 && self.gagnees as u64 >= seuil()
    }

    pub fn imprimer(&self) {
        let (numerateur, denominateur) = FRACTION;
        println!("--- distillation du corpus de fuzz (13 §7 dette 3) ---");
        println!("  arêtes, corpus sans graines distillées : {}", self.base);
        println!("  arêtes, corpus entier                  : {}", self.corpus);
        println!(
            "  arêtes de la base perdues (attendu 0)  : {}",
            self.perdues
        );
        println!(
            "  arêtes gagnées : {} ; seuil {} = ⌈{ARETES_DU_DERIVE} × {numerateur}/{denominateur}⌉",
            self.gagnees,
            seuil()
        );
        let verdict = if self.vert() { "VERT" } else { "ROUGE" };
        println!("  VERDICT : {verdict}");
    }
}

/// Juge deux cartes : celle du corpus sans les graines distillées, celle du corpus entier.
pub fn juger(carte_base: &Path, carte_corpus: &Path) -> Result<Mesure, String> {
    let lire = |chemin: &Path| {
        let texte = std::fs::read_to_string(chemin)
            .map_err(|erreur| format!("{} illisible : {erreur}", chemin.display()))?;
        lire_carte(&texte).map_err(|erreur| format!("{} : {erreur}", chemin.display()))
    };
    Ok(Mesure::de(&lire(carte_base)?, &lire(carte_corpus)?))
}

/// Une table, une ligne par graine : la macro garde la ligne hors de rustfmt (même forme que
/// `mutants_sg9!` de `xtask/tests/mutants.rs`).
macro_rules! lignes {
    ($($ligne:expr;)*) => { [$($ligne),*] };
}

const SUBJECTS: [(&str, &str, &str); 29] = lignes! {
    ("http", "http://api.example.com/v3", "SchemeNonHttps");
    ("fragment", "https://api.example.com/v3#prix", "FragmentPresent");
    ("userinfo", "https://moi@api.example.com/v3", "UserinfoPresent");
    ("crochets", "https://[2001:db8::1]/v3", "HoteLitteralAdresse");
    ("hote-vide", "https:///v3", "HoteVide");
    ("hote-non-ascii", "https://\u{e9}xample.com/v3", "HoteNonAscii");
    ("hote-percent", "https://api%2Eexample.com/v3", "HotePercentEncode");
    ("hote-majuscule", "https://API.example.com/v3", "HoteMajuscule");
    ("hote-souligne", "https://api_example.com/v3", "CaractereHorsGrammaire");
    ("ipv4", "https://192.0.2.1/v3", "HoteLitteralAdresse");
    ("label-hexa", "https://api.example.0x2a/v3", "HoteLitteralAdresse");
    ("label-nombre-point", "https://api.example.42./v3", "HoteLitteralAdresse");
    ("port-vide", "https://api.example.com:/v3", "PortNonDecimal");
    ("port-lettre", "https://api.example.com:44x/v3", "PortNonDecimal");
    ("port-zero", "https://api.example.com:0443/v3", "PortNonDecimal");
    ("port-443", "https://api.example.com:443/v3", "PortParDefautExplicite");
    ("chemin-vide", "https://api.example.com?ids=1", "CheminVide");
    ("point", "https://api.example.com/v3/./prix", "SegmentPointille");
    ("point-encode", "https://api.example.com/v3/%2E%2E/x", "PercentEncodageInutile");
    ("triplet-minuscule", "https://api.example.com/v3/%2f", "TripletPercentMinuscule");
    ("triplet-mal-forme", "https://api.example.com/v3/%G1", "TripletPercentMalForme");
    ("triplet-tronque", "https://api.example.com/v3/%2", "TripletPercentMalForme");
    ("nul-encode", "https://api.example.com/v3/%00", "OctetNulEncode");
    ("chemin-non-ascii", "https://api.example.com/v3/\u{e9}", "OctetNonAscii");
    ("chemin-espace", "https://api.example.com/v3/a b", "CaractereHorsGrammaire");
    ("requete-vide", "https://api.example.com/v3?", "RequeteVide");
    ("trois-points", "https://api.example.com/.../x", "Canonique {");
    ("requete-riche", "https://api.example.com:8443/v3/%2F/a.b?q=a/b?c&d=%2F", "Canonique {");
    ("chemin-riche", "https://a-1.example-2.com/a//.b/%22%B2%05%2B/:@!$&'()*+,;=-._~/R?q=%2F?/:@!$&'()*+,;=-._~", "Canonique {");
};

type Alteration = fn(&mut Temoignage);

const ALTERATIONS: [(&str, Alteration, &str); 15] = lignes! {
    ("attestor-vide", |t| t.attestor.clear(), "ChampVide { position: 71");
    ("residual-vide", |t| t.residual.clear(), "ChampVide { position: 134");
    ("residual-double", |t| t.residual.push("A(exemple-residu-1)".into()), "EntreeDupliquee");
    ("residual-quatre", |t| t.residual.extend(["A(c)".into(), "A(d)".into()]), "Canonique {");
    ("residual-retour", |t| t.residual.push("A(\r)".into()), "ChampNonImprimable");
    ("residual-non-ascii", |t| t.residual.push("A(\u{e9})".into()), "ChampNonAscii");
    ("identity-vide", |t| t.attestor.iter_mut().for_each(|a| a.identity.clear()), "ChampVide");
    ("identity-nul", |t| t.attestor.iter_mut().for_each(|a| a.identity.push('\0')), "ChampNonImprimable");
    ("key-vide", |t| t.attestor.iter_mut().for_each(|a| a.key.clear()), "ChampVide");
    ("attestor-double", |t| t.attestor.extend(t.attestor.clone()), "EntreeDupliquee");
    ("attestor-deux", |t| t.attestor.push(Attestor { key: b"x 2a".to_vec(), identity: "x:2".into() }), "Canonique {");
    ("sans-bytes", |t| t.utterance.bytes = None, "Canonique {");
    ("transport-cloche", |t| t.transport.push('\u{7}'), "ChampNonImprimable");
    ("clock-non-ascii", |t| t.observed_at.clock.push('\u{e9}'), "ChampNonAscii");
    ("instant-8-octets", |t| t.observed_at.instant = 1 << 40, "Canonique {");
};

const SUBSTITUTIONS: [(&str, &[u8], &[u8], &str); 18] = lignes! {
    ("cle-inconnue", b"\x67subject", b"\x67subjecu", "CleInconnue");
    ("cle-vide", b"\x67subject", b"\x60", "CleInconnue");
    ("cles-non-triees", b"\x68attestor", b"\x60", "ClesNonTriees");
    ("cle-double", b"\x68residual", b"\x68attestor", "CleDupliquee");
    ("texte-non-prefere", b"\x67subject\x78\x33", b"\x67subject\x79\x00\x33", "EntierNonPrefere");
    ("attestor-trois", b"\x81\xa2", b"\x81\xa3", "TailleCarteInattendue");
    ("attestor-cle-inconnue", b"\x63key", b"\x60", "CleInconnue");
    ("attestor-non-triees", b"\x68identity", b"\x60", "ClesNonTriees");
    ("attestor-identity-octets", b"\x63key", b"\x68identity", "TypeMajeurInattendu");
    ("utterance-trois", b"utterance\xa2", b"utterance\xa3", "TailleCarteHorsEnsemble");
    ("utterance-cle-inconnue", b"\x64hash", b"\x60", "CleInconnue");
    ("utterance-non-triees", b"\x65bytes", b"\x60", "ClesNonTriees");
    ("empreinte-courte", b"\x64hash\x58\x20", b"\x64hash\x58\x1f", "LongueurDEmpreinteInvalide");
    ("observed-at-trois", b"observed_at\xa2", b"observed_at\xa3", "TailleCarteInattendue");
    ("observed-at-cle-inconnue", b"\x65clock", b"\x60", "CleInconnue");
    ("observed-at-non-triees", b"\x67instant", b"\x60", "ClesNonTriees");
    ("instant-en-texte", b"\x65clock", b"\x67instant", "TypeMajeurInattendu");
    ("residuel", b"d'exemple", b"d'exemple\x00", "OctetsResiduels");
};

const CLES_TRONQUEES: [&str; 12] = lignes! {
    "attestor"; "key"; "identity"; "residual"; "transport"; "utterance"; "hash"; "bytes";
    "observed_at"; "clock"; "instant"; "transport_proof";
};

const CONSTATS: [(&str, &str, &str, &str); 26] = lignes! {
    ("fin-prematuree", ":1}", ":1", "Err(FinPrematuree");
    ("separateur", ":1}", ":1]", "Err(CaractereInattendu");
    ("valeur-nue", "\"server_name\":\"", "\"server_name\":t\"", "Err(CaractereInattendu");
    ("espace-chaine", "V1_2", "V1 2", "Err(EspaceInterdit");
    ("espace-valeur", ":23,", ": 23,", "Err(EspaceInterdit");
    ("non-ascii", "\"exemple\"", "\"ex\u{e9}mple\"", "Err(OctetNonAscii");
    ("echappement", "V1_2", "V1\\_2", "Err(EchappementInterdit");
    ("controle", "V1_2", "V1\u{7}_2", "Err(CaractereInattendu");
    ("cle-inconnue", "\"verdict\"", "\"verdikt\"", "Err(CleInconnue");
    ("cle-repetee", "\"verdict\":", "\"verdict\":\"x\",\"verdict\":", "Err(CleRepetee");
    ("cle-non-triee", "\"attestor_cle_algorithme\"", "\"verdict\"", "Err(CleNonTriee");
    ("cle-manquante", "\"octets_presentation\":23,", "", "Err(CleManquante");
    ("entier-en-chaine", ":23,", ":\"23\",", "Err(TypeInattendu");
    ("chaine-en-entier", "\"api.example.com\"", "7", "Err(TypeInattendu");
    ("zero-de-tete", ":23,", ":023,", "Err(EntierNonCanonique");
    ("debordement", ":1754000000,", ":99999999999999999999,", "Err(EntierNonCanonique");
    ("version-2", ":1}", ":2}", "Err(VersionInattendue");
    ("cle-majuscules", "041a2b3c", "041A2B3C", "Err(HexadecimalInvalide");
    ("empreinte-non-hexa", "\"9c11", "\"9g11", "Err(HexadecimalInvalide");
    ("empreinte-courte", "\"9c11", "\"11", "Err(LongueurHexadecimaleInvalide");
    ("cle-hexa-vide", "041a2b3c", "", "Err(LongueurHexadecimaleInvalide");
    ("revision-vide", "\"0000000000000000000000000000000000000000\"", "\"\"", "Err(ValeurVide");
    ("algorithme-vide", "\"exemple\"", "\"\"", "Err(ValeurVide");
    ("verdict-echec", "presentation_verifiee", "echec", "Err(VerdictSansSucces");
    ("longueurs", "authentifie\":17", "authentifie\":16", "Err(LongueursIncoherentes");
    ("residuel", ":1}", ":1}x", "Err(OctetsResiduels");
};

const CBOR: [(&str, &[u8], &str); 6] = lignes! {
    ("argument-reserve", b"\xbc", "Refuse(ArgumentReserve");
    ("argument-tronque", b"\xb8", "Refuse(FinPrematuree");
    ("non-prefere-4", b"\xba\x00\x00\x00\x03", "Refuse(EntierNonPrefere");
    ("non-prefere-8", b"\xbb\x00\x00\x00\x00\x00\x00\x00\x03", "Refuse(EntierNonPrefere");
    ("texte-hors-memoire", b"\xa3\x7b\xff\xff\xff\xff\xff\xff\xff\xff", "Refuse(LongueurHorsMemoire");
    ("texte-non-utf8", b"\xa3\x62\xff\xfe", "Refuse(TexteNonUtf8");
};

const REGISTRES: [(&str, &str, &str); 2] = lignes! {
    ("unicode", "\u{a0}A(x)\u{a0}\r\n\u{3000}# c\u{2003}\n\u{e9e9}A(y)\u{10ffff}\n\t\u{b}\u{c} A(z)\r\n\u{85}\n\r\n \n\0\n\u{206f}#x\n\u{feff}A(b)\n\u{608ce}\u{1f}\n", "Ok(7)");
    ("blanc", "                \t\u{c}", "Ok(0)");
};
