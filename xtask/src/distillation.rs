//! **Distillation du corpus de fuzz** — 13 §7 dette 3 ; SHOGEN-FUZZ-DISTILLATION-1 (ADR-0028
//! annexe A, lot FUZZ).
//!
//! Les campagnes instrumentées atteignent des arêtes que le corpus dirigé n'atteint pas. Plutôt
//! que de verser leurs entrées, illisibles, la distillation nomme les formes qu'elles exercent —
//! surtout les refus nommés du vérificateur, à chaque profondeur de ses surfaces — et les écrit en
//! graines `dirigee-distillee-*`, régénérées par `cargo xtask fuzz-corpus`. Chaque graine porte un
//! fragment du classement que le vérificateur doit en rendre (`attendu`), contrôlé par
//! `xtask/tests/distillation.rs`. Mesure et seuil : `crates/shogen-verifier/fuzz-corpus/README.md`.

use crate::fuzz::temoignage_canonique_exemple;
use shogen_core::encoder_temoignage_canonique;

/// Une graine distillée : son nom au corpus, ses octets, et ce que le vérificateur doit en dire.
pub struct Graine {
    pub nom: String,
    pub octets: Vec<u8>,
    pub attendu: &'static str,
}

/// Les graines distillées, dans un ordre fixe.
pub fn graines() -> Vec<Graine> {
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
    graines
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
