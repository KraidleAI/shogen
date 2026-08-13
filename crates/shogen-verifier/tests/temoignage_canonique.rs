//! **Les trois mutants du critère de S3, sur le vrai binaire.**
//!
//! Rattachement : **05 §S3 / 13 §1** — « une commande `shogen verify <lot>`
//! retourne "valide sous A(...)" sur un témoignage réel, et échoue
//! (fail-closed, raison structurée) sur les 3 mutants semés : preuve altérée,
//! hash d'utterance faux, résidu non résolu » ; **ADR-0015 point 8** ;
//! **ADR-0011 point 1** (l'étage d'intégration).
//!
//! Le lot est **réécrit à la main ici**, en-tête par en-tête, sans passer par
//! `shogen-core` : le vérificateur n'a aucune dépendance de développement
//! (S-G2), et un test qui produirait son entrée avec l'encodeur qu'il vérifie ne
//! testerait que la cohérence de l'encodeur avec lui-même. L'empreinte SHA-256
//! des octets d'`utterance` et celle de la preuve sont, elles aussi, écrites en
//! dur — recalculées hors de ce dépôt, elles sont ce qui rend le test capable de
//! prendre l'implémentation en défaut.
//!
//! **Provenance des deux empreintes écrites en dur** (2026-08-13) : calculées par
//! **deux implémentations tierces concordantes**, hors de ce dépôt et hors de
//! `crates/shogen-core/src/empreinte.rs` — `System.Security.Cryptography.SHA256`
//! de .NET et `sha256sum` de GNU coreutils. C'est la condition qui donne au test
//! son pouvoir : une empreinte produite par le code vérifié ne prendrait ce code
//! en défaut sur aucune erreur, puisqu'elle bougerait avec lui.

use std::path::{Path, PathBuf};
use std::process::Command;

/// Les octets d'`utterance` du lot de référence.
const OCTETS_D_UTTERANCE: &[u8] = b"{\"price\":\"42.17\"}";
/// Leur empreinte SHA-256, en hexadécimal — tierce, jamais de mémoire.
const EMPREINTE_D_UTTERANCE: &str =
    "04f501ade9aec2a345218a7264fe2dec87d2f0fbf7a6c500605dbc425a6fac9d";
/// Les octets de preuve, opaques.
const OCTETS_DE_PREUVE: &[u8] = b"preuve-opaque-d'exemple";
/// Leur empreinte SHA-256, en hexadécimal — tierce, jamais de mémoire.
const EMPREINTE_DE_PREUVE: &str =
    "9c114e983a7b36eddd59ad5584f40b8beddb04918e665107e8e362fcd0252c86";

const SUBJECT: &str = "https://api.example.com/v3/simple/price?ids=bitcoin";
const IDENTITE: &str = "exemple:attestateur-1";
const RESIDU_1: &str = "A(exemple-residu-1)";
const RESIDU_2: &str = "A(exemple-residu-2)";
const RESIDU_DE_LA_DELEGATION: &str = "A(transport-check-delegated)";
const TRANSPORT: &str = "exemple-transport/1";
const HORLOGE: &str = "exemple:horloge-du-transport";
const OUTIL: &str = "exemple-compagnon/1 (revision 0000000)";

/// Écrit un en-tête CBOR en sérialisation préférée — la seule forme admise.
fn entete(octets: &mut Vec<u8>, prefixe: u8, argument: u64) {
    if argument <= 23 {
        octets.push(prefixe | (argument as u8));
    } else if argument <= 0xFF {
        octets.push(prefixe | 24);
        octets.push(argument as u8);
    } else if argument <= 0xFFFF {
        octets.push(prefixe | 25);
        octets.extend_from_slice(&(argument as u16).to_be_bytes());
    } else {
        octets.push(prefixe | 26);
        octets.extend_from_slice(&(argument as u32).to_be_bytes());
    }
}

fn texte(octets: &mut Vec<u8>, valeur: &str) {
    entete(octets, 0x60, valeur.len() as u64);
    octets.extend_from_slice(valeur.as_bytes());
}

fn chaine_d_octets(octets: &mut Vec<u8>, valeur: &[u8]) {
    entete(octets, 0x40, valeur.len() as u64);
    octets.extend_from_slice(valeur);
}

fn depuis_hexadecimal(rendu: &str) -> Vec<u8> {
    rendu
        .as_bytes()
        .chunks_exact(2)
        .map(|paire| {
            u8::from_str_radix(std::str::from_utf8(paire).expect("ASCII"), 16)
                .expect("chiffre hexadécimal")
        })
        .collect()
}

/// Le lot de référence : un témoignage canonique aux sept champs de 03 §1.
fn lot_de_reference(
    empreinte_d_utterance: &str,
    octets_d_utterance: &[u8],
    octets_de_preuve: &[u8],
    residus: &[&str],
) -> Vec<u8> {
    let mut octets: Vec<u8> = Vec::new();
    entete(&mut octets, 0xa0, 7); // carte de 7 entrées

    texte(&mut octets, "subject");
    texte(&mut octets, SUBJECT);

    texte(&mut octets, "attestor");
    entete(&mut octets, 0x80, 1); // tableau(1)
    entete(&mut octets, 0xa0, 2); // carte(2)
    texte(&mut octets, "key");
    chaine_d_octets(&mut octets, &[0x04, 0x1a, 0x2b, 0x3c]);
    texte(&mut octets, "identity");
    texte(&mut octets, IDENTITE);

    texte(&mut octets, "residual");
    entete(&mut octets, 0x80, residus.len() as u64);
    for residu in residus {
        texte(&mut octets, residu);
    }

    texte(&mut octets, "transport");
    texte(&mut octets, TRANSPORT);

    texte(&mut octets, "utterance");
    entete(&mut octets, 0xa0, 2); // carte(2)
    texte(&mut octets, "hash");
    chaine_d_octets(&mut octets, &depuis_hexadecimal(empreinte_d_utterance));
    texte(&mut octets, "bytes");
    chaine_d_octets(&mut octets, octets_d_utterance);

    texte(&mut octets, "observed_at");
    entete(&mut octets, 0xa0, 2); // carte(2)
    texte(&mut octets, "clock");
    texte(&mut octets, HORLOGE);
    texte(&mut octets, "instant");
    entete(&mut octets, 0x00, 1_754_000_000);

    texte(&mut octets, "transport_proof");
    chaine_d_octets(&mut octets, octets_de_preuve);

    octets
}

fn lot_intact() -> Vec<u8> {
    lot_de_reference(
        EMPREINTE_D_UTTERANCE,
        OCTETS_D_UTTERANCE,
        OCTETS_DE_PREUVE,
        &[RESIDU_1, RESIDU_2],
    )
}

fn repertoire(nom: &str) -> PathBuf {
    let chemin = std::env::temp_dir().join(format!("shogen-canonique-{nom}"));
    let _ = std::fs::remove_dir_all(&chemin);
    std::fs::create_dir_all(&chemin).expect("création du répertoire de test");
    chemin
}

/// Le registre publié de référence, écrit comme `docs/08-assumptions.md` le
/// donnerait : un identifiant par ligne.
fn ecrire_registre(repertoire: &Path, residus: &[&str]) -> PathBuf {
    let chemin = repertoire.join("registre.txt");
    let mut texte = String::from("# registre publié des résidus (08-assumptions.md)\n");
    for residu in residus {
        texte.push_str(residu);
        texte.push('\n');
    }
    std::fs::write(&chemin, texte).expect("écriture du registre");
    chemin
}

/// Le constat que le binaire compagnon d'ADR-0015 rendrait.
fn ecrire_constat(repertoire: &Path, empreinte_preuve: &str, empreinte_utterance: &str) -> PathBuf {
    let chemin = repertoire.join("constat.txt");
    let texte = format!(
        "# constat du binaire compagnon (ADR-0015 points 7 et 8)\noutil = {OUTIL}\nempreinte-preuve = {empreinte_preuve}\nempreinte-utterance = {empreinte_utterance}\n"
    );
    std::fs::write(&chemin, texte).expect("écriture du constat");
    chemin
}

fn executer(arguments: &[&Path]) -> (i32, String, String) {
    let sortie = Command::new(env!("CARGO_BIN_EXE_shogen-verifier"))
        .args(arguments)
        .output()
        .expect("le binaire du vérificateur doit s'exécuter");
    (
        sortie.status.code().unwrap_or(-1),
        String::from_utf8_lossy(&sortie.stdout).into_owned(),
        String::from_utf8_lossy(&sortie.stderr).into_owned(),
    )
}

/// Prépare un cas : écrit le lot, le registre et le constat, rend leurs chemins.
fn preparer(nom: &str, lot: &[u8], residus_du_registre: &[&str]) -> (PathBuf, PathBuf, PathBuf) {
    let repertoire = repertoire(nom);
    let chemin_lot = repertoire.join("lot.cbor");
    std::fs::write(&chemin_lot, lot).expect("écriture du lot");
    let registre = ecrire_registre(&repertoire, residus_du_registre);
    let constat = ecrire_constat(&repertoire, EMPREINTE_DE_PREUVE, EMPREINTE_D_UTTERANCE);
    (chemin_lot, registre, constat)
}

const REGISTRE_COMPLET: &[&str] = &[RESIDU_1, RESIDU_2, RESIDU_DE_LA_DELEGATION];

#[test]
fn temoignage_canonique_intact_le_verdict_nomme_les_residus_et_la_delegation() {
    let (lot, registre, constat) = preparer("intact", &lot_intact(), REGISTRE_COMPLET);
    let (code, sortie, erreur) = executer(&[
        &lot,
        Path::new("--registre"),
        &registre,
        Path::new("--constat"),
        &constat,
    ]);
    assert_eq!(
        code, 0,
        "lot intact refusé\nstdout:{sortie}\nstderr:{erreur}"
    );
    assert!(
        sortie.contains(&format!(
            "VERDICT : valide sous {RESIDU_1}, {RESIDU_2}, {RESIDU_DE_LA_DELEGATION}"
        )),
        "le verdict doit nommer les résidus DANS L'ORDRE, délégation comprise : {sortie}"
    );
    assert!(
        sortie.contains("jamais par ce binaire"),
        "le verdict doit nommer ce qu'il n'a PAS vérifié (ADR-0015 point 8 alinéa e) : {sortie}"
    );
    assert!(
        sortie.contains(OUTIL),
        "le verdict nomme le binaire à qui le contrôle a été délégué : {sortie}"
    );
    assert!(
        sortie.contains("aucune horloge lue"),
        "l'instant est une donnée portée, et le verdict le dit : {sortie}"
    );
    assert!(
        sortie.contains("round-trip exact"),
        "le contrôle (a) d'ADR-0015 point 8 reste acquis : {sortie}"
    );
}

#[test]
fn mutant_1_preuve_alteree_est_refusee_fail_closed() {
    let mut preuve = OCTETS_DE_PREUVE.to_vec();
    preuve[0] ^= 0x01;
    let lot = lot_de_reference(
        EMPREINTE_D_UTTERANCE,
        OCTETS_D_UTTERANCE,
        &preuve,
        &[RESIDU_1, RESIDU_2],
    );
    let (chemin, registre, constat) = preparer("preuve", &lot, REGISTRE_COMPLET);
    let (code, _, erreur) = executer(&[
        &chemin,
        Path::new("--registre"),
        &registre,
        Path::new("--constat"),
        &constat,
    ]);
    assert_ne!(code, 0, "preuve altérée acceptée");
    assert!(
        erreur.contains("VERDICT : refusé (fail-closed)"),
        "{erreur}"
    );
    assert!(erreur.contains("preuve non constatée"), "{erreur}");
    assert!(!erreur.contains("panicked"), "{erreur}");
}

#[test]
fn mutant_2_hash_d_utterance_faux_est_refuse_fail_closed() {
    let mut empreinte = String::from(EMPREINTE_D_UTTERANCE);
    empreinte.replace_range(0..1, "9");
    let lot = lot_de_reference(
        &empreinte,
        OCTETS_D_UTTERANCE,
        OCTETS_DE_PREUVE,
        &[RESIDU_1, RESIDU_2],
    );
    let (chemin, registre, constat) = preparer("hash", &lot, REGISTRE_COMPLET);
    let (code, _, erreur) = executer(&[
        &chemin,
        Path::new("--registre"),
        &registre,
        Path::new("--constat"),
        &constat,
    ]);
    assert_ne!(code, 0, "hash d'utterance faux accepté");
    assert!(
        erreur.contains("VERDICT : refusé (fail-closed)"),
        "{erreur}"
    );
    assert!(erreur.contains("liaison d'utterance rompue"), "{erreur}");
    assert!(!erreur.contains("panicked"), "{erreur}");
}

#[test]
fn mutant_3_residu_non_resolu_est_refuse_fail_closed() {
    let lot = lot_de_reference(
        EMPREINTE_D_UTTERANCE,
        OCTETS_D_UTTERANCE,
        OCTETS_DE_PREUVE,
        &[RESIDU_1, "A(residu-jamais-publie)"],
    );
    let (chemin, registre, constat) = preparer("residu", &lot, REGISTRE_COMPLET);
    let (code, _, erreur) = executer(&[
        &chemin,
        Path::new("--registre"),
        &registre,
        Path::new("--constat"),
        &constat,
    ]);
    assert_ne!(code, 0, "résidu non résolu accepté");
    assert!(
        erreur.contains("VERDICT : refusé (fail-closed)"),
        "{erreur}"
    );
    assert!(erreur.contains("résidu non résolu"), "{erreur}");
    assert!(erreur.contains("A(residu-jamais-publie)"), "{erreur}");
}

#[test]
fn sans_registre_ni_constat_le_lot_canonique_est_refuse() {
    // Fail-safe defaults : ce que le vérificateur n'a pas pu établir n'est pas
    // admis par défaut. Un lot canonique sans contexte n'est pas « valide » —
    // il est **non conclu**, et le binaire le dit en refusant.
    let repertoire = repertoire("sans-contexte");
    let chemin = repertoire.join("lot.cbor");
    std::fs::write(&chemin, lot_intact()).expect("écriture du lot");
    let (code, _, erreur) = executer(&[&chemin]);
    assert_ne!(code, 0, "lot canonique accepté sans contexte");
    assert!(erreur.contains("registre des résidus vide"), "{erreur}");
}

#[test]
fn un_constat_mal_forme_est_refuse_sans_panique() {
    let repertoire = repertoire("constat-mal-forme");
    let chemin = repertoire.join("lot.cbor");
    std::fs::write(&chemin, lot_intact()).expect("écriture du lot");
    let registre = ecrire_registre(&repertoire, REGISTRE_COMPLET);
    let constat = repertoire.join("constat.txt");
    std::fs::write(&constat, "outil = x\nempreinte-preuve = zz\n").expect("écriture");
    let (code, _, erreur) = executer(&[
        &chemin,
        Path::new("--registre"),
        &registre,
        Path::new("--constat"),
        &constat,
    ]);
    assert_ne!(code, 0);
    assert!(erreur.contains("constat mal formé"), "{erreur}");
    assert!(!erreur.contains("panicked"), "{erreur}");
}

#[test]
fn un_subject_non_canonique_est_refuse_au_decodage() {
    // ADR-0016 C10 : le refus a lieu au **décodage**, avant tout contrôle de
    // liaison — un témoignage dont le subject n'est pas canonique n'existe pas.
    let mut lot = lot_intact();
    let position = lot
        .windows(SUBJECT.len())
        .position(|f| f == SUBJECT.as_bytes())
        .expect("le subject figure dans le lot");
    lot[position + 8] = b'A'; // première lettre de l'hôte, en majuscule
    let (chemin, registre, constat) = preparer("subject", &lot, REGISTRE_COMPLET);
    let (code, _, erreur) = executer(&[
        &chemin,
        Path::new("--registre"),
        &registre,
        Path::new("--constat"),
        &constat,
    ]);
    assert_ne!(code, 0);
    assert!(erreur.contains("subject non canonique"), "{erreur}");
    assert!(erreur.contains("majuscule dans l'hôte"), "{erreur}");
}

/// Les positions d'octets que **rien** ne lie dans la forme d'ADR-0015 point 8.
///
/// Deux charges utiles du témoignage n'entrent dans aucun contrôle recalculable
/// par ce binaire, et il faut le dire au lieu de l'espérer :
///
/// - **la clé épinglée de l'attestateur** — les contrôles (b), (c) et (d) ne la
///   touchent pas, et le constat du compagnon (ADR-0015 point 8) déclare l'outil
///   et deux empreintes, **jamais la clé contre laquelle il a vérifié**. Rien ici
///   ne rattache donc la clé portée à celle qu'a employée le contrôle délégué ;
/// - **l'instant d'observation** — 03 §1 le veut ainsi (« la fraîcheur se calcule
///   plus haut ») : ce rang enregistre qui a daté, il ne date pas.
///
/// Ces deux trous ne sont pas des défauts de ce code : ce sont les **arêtes de la
/// délégation** telle qu'ADR-0015 point 8 la spécifie aujourd'hui. Les fermer
/// exigerait que le constat porte l'attestateur employé — une décision d'ADR, pas
/// une retouche de test. Ce test les mesure exactement pour qu'ils ne puissent ni
/// s'élargir en silence, ni être crus fermés.
fn positions_non_liees(lot: &[u8]) -> Vec<usize> {
    let mut positions: Vec<usize> = Vec::new();
    for (aiguille, charge) in [
        (CLE_ATTESTOR_ENCODEE.to_vec(), CLE_ATTESTOR.len()),
        (instant_encode(), 4usize),
    ] {
        let debut = lot
            .windows(aiguille.len())
            .position(|fenetre| fenetre == aiguille.as_slice())
            .expect("la charge non liée figure dans le lot");
        // La charge suit son en-tête d'un octet.
        let debut_charge = debut + (aiguille.len() - charge);
        positions.extend(debut_charge..debut_charge + charge);
    }
    positions.sort_unstable();
    positions
}

/// La clé épinglée du lot de référence, et son en-tête de chaîne d'octets.
const CLE_ATTESTOR: &[u8] = &[0x04, 0x1a, 0x2b, 0x3c];
const CLE_ATTESTOR_ENCODEE: &[u8] = &[0x44, 0x04, 0x1a, 0x2b, 0x3c];

/// L'instant du lot de référence, tel que l'encodeur l'écrit : en-tête `0x1a`
/// (entier non signé, argument sur quatre octets) puis l'argument gros-boutiste.
fn instant_encode() -> Vec<u8> {
    let mut aiguille = vec![0x1au8];
    aiguille.extend_from_slice(&1_754_000_000u32.to_be_bytes());
    aiguille
}

#[test]
fn chaque_octet_de_structure_mute_est_refuse_ou_reste_canonique() {
    // La limite du squelette S2.5 est ici **levée** : muter un octet de charge
    // utile ne produit plus un autre témoignage acceptable, parce que le hash
    // d'`utterance` et le constat lient le lot à sa preuve (ADR-0005 règle 1).
    // Ce qui reste ouvert est **énuméré**, pas laissé au hasard : voir
    // `positions_non_liees`.
    let repertoire = repertoire("mutation");
    let origine = lot_intact();
    let registre = ecrire_registre(&repertoire, REGISTRE_COMPLET);
    let constat = ecrire_constat(&repertoire, EMPREINTE_DE_PREUVE, EMPREINTE_D_UTTERANCE);
    let mut refuses = 0usize;
    let mut acceptes: Vec<usize> = Vec::new();

    for position in 0..origine.len() {
        let mut mute = origine.clone();
        mute[position] ^= 0xff;
        let chemin = repertoire.join(format!("lot-{position}.cbor"));
        std::fs::write(&chemin, &mute).expect("écriture du lot muté");
        let (code, sortie, erreur) = executer(&[
            &chemin,
            Path::new("--registre"),
            &registre,
            Path::new("--constat"),
            &constat,
        ]);
        if code == 0 {
            acceptes.push(position);
            println!("octet {position} inversé : ACCEPTÉ\n{sortie}");
        } else {
            assert!(
                erreur.contains("VERDICT : refusé (fail-closed)"),
                "octet {position} : verdict de refus absent\nstderr:{erreur}"
            );
            assert!(
                !erreur.contains("panicked"),
                "octet {position} : PANIQUE au lieu d'un refus\nstderr:{erreur}"
            );
            refuses += 1;
        }
    }

    let attendues = positions_non_liees(&origine);
    println!(
        "mutation d'octet bout-en-bout — {} positions : {refuses} refus fail-closed nommés, {} acceptations, 0 panique",
        origine.len(),
        acceptes.len()
    );
    println!(
        "positions acceptées {acceptes:?} — attendues (charges non liées) {attendues:?} : \
         clé épinglée de l'attestateur et instant d'observation"
    );
    // Égalité d'ensembles, pas inégalité de compte : le test mord dans les deux
    // sens. Un contrôle qui disparaît élargit l'ensemble et tombe ici ; un
    // contrôle qui se resserre (le constat portant enfin l'attestateur employé)
    // le rétrécit et tombe ici aussi — auquel cas c'est `positions_non_liees`
    // qu'il faut réduire, en même temps que l'ADR qui l'aura permis.
    assert_eq!(
        acceptes, attendues,
        "l'ensemble des octets non liés a changé : hors la clé épinglée et \
         l'instant, la liaison hash → preuve ferme toute la classe que le \
         squelette S2.5 laissait ouverte (ADR-0005 règle 1, ADR-0015 point 8)"
    );
}

/// Revue G2 de phase C, trouvaille F7 (démontrée : l'ordre des lignes du
/// constat changeait le verdict) : une clé répétée est un refus nommé,
/// jamais « la dernière l'emporte ».
#[test]
fn un_constat_a_cle_repetee_est_refuse() {
    let (lot, registre, constat) = preparer("constat-cle-repetee", &lot_intact(), REGISTRE_COMPLET);
    let texte = std::fs::read_to_string(&constat).expect("constat de référence");
    let doublon = format!("{texte}empreinte-utterance = {EMPREINTE_D_UTTERANCE}\n");
    std::fs::write(&constat, doublon).expect("écriture du constat à doublon");
    let (code, sortie, erreur) = executer(&[
        &lot,
        Path::new("--registre"),
        &registre,
        Path::new("--constat"),
        &constat,
    ]);
    assert_ne!(code, 0, "un constat à clé répétée ne peut pas valider");
    assert!(
        erreur.contains("clé répétée"),
        "le refus doit nommer la clé répétée\nstdout:{sortie}\nstderr:{erreur}"
    );
}

/// Revue G2 de phase C, autour de F8 : la substitution de forme. Un appelant
/// qui fournit --registre/--constat demande les contrôles de 03 §4 ; un lot
/// TRIVIAL n'en porte aucun — sortir en 0 en ignorant les options serait un
/// déclassement silencieux.
#[test]
fn un_lot_trivial_avec_options_de_verification_est_refuse() {
    let repertoire = repertoire("trivial-avec-options");
    let chemin_lot = repertoire.join("lot-trivial.cbor");
    let trivial = shogen_core::TemoignageTrivial {
        source: String::from("exemple:source"),
        contenu: b"contenu d'exemple".to_vec(),
        instant: 1_754_000_000,
    };
    std::fs::write(&chemin_lot, shogen_core::encoder_temoignage(&trivial))
        .expect("écriture du lot trivial");
    let registre = ecrire_registre(&repertoire, REGISTRE_COMPLET);
    let (code, sortie, erreur) = executer(&[&chemin_lot, Path::new("--registre"), &registre]);
    assert_eq!(
        code, 65,
        "options de vérification sur forme triviale = refus de contexte
stdout:{sortie}
stderr:{erreur}"
    );
    assert!(
        erreur.contains("forme triviale"),
        "le refus doit nommer la substitution de forme : {erreur}"
    );
}
