//! **Le critère de sortie de S3, exécuté sur un témoignage réel** — et les
//! trois mutants semés, en cas de test nommés.
//!
//! Rattachement (G0) : **13 §1**, repris à la lettre — « une commande
//! `shogen verify <lot>` retourne "valide sous A(notary-neutrality)" sur un
//! témoignage réel, et échoue (fail-closed, raison structurée) sur les 3
//! mutants semés : **preuve altérée, hash d'utterance faux, résidu non
//! résolu** » ; **13 §4 phase C** — « les 3 mutants semés du critère de sortie
//! sont des **cas de test nommés**, pas des démonstrations manuelles » ;
//! **ADR-0015 point 8** et son amendement (f)/(g) ; **ADR-0015 point 13** (le
//! contrat du constat, dont ce fichier consomme la pièce réelle).
//!
//! # Ce qui rend ces cas capables de prendre le code en défaut
//!
//! Rien n'est fabriqué ici : le lot, le constat et le registre sont les
//! **fixtures versionnées** de `tests/fixtures/`, dont `PROVENANCE.md` porte la
//! chaîne et les sha256. Le constat vient du binaire compagnon, c'est-à-dire
//! d'une **autre implémentation de SHA-256** que celle du cœur — un condensé
//! faux d'un seul côté ne peut produire qu'un refus.
//!
//! Les mutants sont du registre « **octet muté du lot** » de
//! `docs/09-vocabulaire.md` : test négatif de données. Ni mutant de gate, ni
//! mutant de programme ; ils ne produisent aucun score.
//!
//! # Pourquoi les mutations changent une lettre plutôt que d'inverser un octet
//!
//! Inverser un octet (`^= 0xff`) dans un identifiant ou dans `subject`
//! produirait un octet non-ASCII, et le lot serait refusé **au décodage**
//! (`ChampNonAscii`, `SubjectNonCanonique`) — un refus juste, mais pas celui
//! que le cas mesure. Une lettre ASCII remplacée par une autre laisse le lot
//! parfaitement canonique et fait tomber exactement le contrôle visé. Le cas
//! doit mordre là où il dit mordre.

use std::path::{Path, PathBuf};
use std::process::Command;

/// Codes de sortie du binaire (`src/main.rs`) — asserés, jamais supposés.
const CODE_CONFORME: i32 = 0;
const CODE_VERIFICATION: i32 = 4;
const CODE_CONTEXTE: i32 = 65;

/// La chaîne du critère de sortie, telle que 13 §1 l'écrit.
const VERDICT_ATTENDU: &str =
    "VERDICT : valide sous A(notary-neutrality), A(self-attestation), A(transport-check-delegated)";
/// La révision amont, verbatim, qu'ADR-0015 point 8 alinéa e fait entrer dans
/// la chaîne de verdict — copiée du constat réel, jamais de mémoire.
const REVISION_AMONT: &str = "0fe3c32d35382b3f290a43c4156399ca4512bb89";

fn fixtures() -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("tests")
        .join("fixtures")
}

fn lot_reel() -> Vec<u8> {
    std::fs::read(fixtures().join("s3-binance.lot.cbor")).expect("le lot réel est versionné")
}

/// Un répertoire de travail **propre à ce processus** (même motif que les
/// autres suites : la gate de mutation lance quatre suites de front).
fn repertoire(nom: &str) -> PathBuf {
    let chemin = std::env::temp_dir().join(format!("shogen-reel-{nom}-{}", std::process::id()));
    let _ = std::fs::remove_dir_all(&chemin);
    std::fs::create_dir_all(&chemin).expect("création du répertoire de test");
    chemin
}

/// Exécute le vrai binaire sur un lot donné, avec le constat et le registre
/// **réels**.
fn verifier(nom: &str, lot: &[u8]) -> (i32, String, String) {
    let repertoire = repertoire(nom);
    let chemin = repertoire.join("lot.cbor");
    std::fs::write(&chemin, lot).expect("écriture du lot");
    executer(&[
        chemin.as_path(),
        Path::new("--registre"),
        &fixtures().join("s3-binance.registre.txt"),
        Path::new("--constat"),
        &fixtures().join("s3-binance.constat.json"),
    ])
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

/// La position du premier octet d'une aiguille dans le lot — un test qui
/// cherche ce qu'il mute plutôt que d'écrire un décalage en dur ne devient pas
/// faux en silence le jour où la forme bouge.
fn position(lot: &[u8], aiguille: &[u8]) -> usize {
    lot.windows(aiguille.len())
        .position(|fenetre| fenetre == aiguille)
        .unwrap_or_else(|| panic!("aiguille absente du lot réel : {aiguille:?}"))
}

/// Remplace une lettre ASCII par une autre, à la première occurrence d'une
/// aiguille textuelle : la longueur ne change pas, donc l'encodage CBOR reste
/// valide et le lot reste canonique.
fn muter_une_lettre(lot: &mut [u8], aiguille: &str, decalage: usize, lettre: u8) {
    let debut = position(lot, aiguille.as_bytes());
    let cible = debut
        .checked_add(decalage)
        .expect("décalage dans les bornes");
    let case = lot.get_mut(cible).expect("position dans les bornes");
    assert_ne!(*case, lettre, "la mutation doit changer quelque chose");
    *case = lettre;
}

// ---------------------------------------------------------------------------
// LE CRITÈRE DE SORTIE
// ---------------------------------------------------------------------------

#[test]
fn critere_de_sortie_le_temoignage_reel_est_valide_sous_ses_residus() {
    let (code, sortie, erreur) = verifier("critere", &lot_reel());
    assert_eq!(
        code, CODE_CONFORME,
        "le témoignage réel est refusé\nstdout:{sortie}\nstderr:{erreur}"
    );
    assert!(
        sortie.contains(VERDICT_ATTENDU),
        "le verdict du critère de sortie doit nommer ses trois résidus DANS L'ORDRE : {sortie}"
    );
    // ADR-0015 point 8 alinéa e : la révision amont entre VERBATIM dans la
    // chaîne, et la phrase dit ce que ce binaire n'a PAS fait.
    assert!(
        sortie.contains(REVISION_AMONT),
        "la révision amont du constat doit entrer verbatim dans le verdict : {sortie}"
    );
    assert!(
        sortie.contains("jamais par ce binaire"),
        "le verdict nomme la délégation : {sortie}"
    );
    // Le témoignage est réel : son subject désigne l'endpoint interrogé, et son
    // instant vient de l'horloge du transport.
    assert!(
        sortie.contains("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"),
        "le subject réel doit être imprimé : {sortie}"
    );
    assert!(
        sortie.contains("aucune horloge lue"),
        "l'instant est une donnée portée, et le verdict le dit : {sortie}"
    );
    assert!(
        sortie.contains("round-trip exact"),
        "le contrôle (a) reste acquis sur le lot réel : {sortie}"
    );
    println!("{sortie}");
}

// ---------------------------------------------------------------------------
// LES TROIS MUTANTS SEMÉS DU CRITÈRE (13 §1)
// ---------------------------------------------------------------------------

/// Mutant (i) — **preuve altérée**. Un octet des 6034 octets de
/// `transport_proof` change : le lot ne porte plus la preuve qui a été
/// vérifiée. Contrôle (c) d'ADR-0015 point 8.
#[test]
fn mutant_1_preuve_alteree_refus_c_fail_closed() {
    let mut lot = lot_reel();
    // Le dernier octet du lot est le dernier octet de `transport_proof` :
    // c'est le champ de queue de la forme canonique (ordre des clés,
    // `temoignage_canonique.rs`).
    let dernier = lot.last_mut().expect("le lot n'est pas vide");
    *dernier ^= 0x01;

    let (code, _, erreur) = verifier("preuve", &lot);
    assert_eq!(
        code, CODE_VERIFICATION,
        "preuve altérée acceptée : {erreur}"
    );
    assert!(
        erreur.contains("VERDICT : refusé (fail-closed)"),
        "{erreur}"
    );
    assert!(
        erreur.contains("preuve non constatée"),
        "le refus doit être celui du contrôle (c) : {erreur}"
    );
    assert!(
        erreur.contains("PreuveNonConstatee"),
        "la variante exacte doit être imprimée : {erreur}"
    );
    assert!(!erreur.contains("panicked"), "{erreur}");
}

/// Mutant (ii) — **hash d'utterance faux**. Un octet de l'empreinte portée
/// change ; les octets, eux, restent ceux qu'ils étaient. C'est (b1) qui tombe :
/// les octets portés ne redonnent plus l'empreinte portée (ADR-0005 règle 1).
#[test]
fn mutant_2_hash_d_utterance_faux_refus_b1_fail_closed() {
    let mut lot = lot_reel();
    // `hash` en texte CBOR (`0x64` + « hash »), puis l'en-tête de chaîne
    // d'octets de 32 (`0x58 0x20`), puis l'empreinte.
    let mut aiguille = vec![0x64u8];
    aiguille.extend_from_slice(b"hash");
    aiguille.extend_from_slice(&[0x58, 0x20]);
    let debut = position(&lot, &aiguille);
    let cible = debut
        .checked_add(aiguille.len())
        .expect("décalage dans les bornes");
    let case = lot.get_mut(cible).expect("position dans les bornes");
    *case ^= 0x01;

    let (code, _, erreur) = verifier("hash", &lot);
    assert_eq!(
        code, CODE_VERIFICATION,
        "hash d'utterance faux accepté : {erreur}"
    );
    assert!(
        erreur.contains("VERDICT : refusé (fail-closed)"),
        "{erreur}"
    );
    assert!(
        erreur.contains("liaison d'utterance rompue"),
        "le refus doit être celui de la liaison interne (b1) : {erreur}"
    );
    assert!(
        erreur.contains("LiaisonUtteranceRompue"),
        "la variante exacte doit être imprimée : {erreur}"
    );
    assert!(!erreur.contains("panicked"), "{erreur}");
}

/// Mutant (ii bis) — **hash d'utterance faux, et octets faux avec lui**. Les
/// deux bougent ensemble, donc (b1) passe : c'est (b2) qui tombe, parce que
/// l'empreinte portée n'est plus celle que le compagnon a constatée.
///
/// Sans ce cas, un lecteur pourrait croire que (b2) est mort : (b1) le masque
/// dès que les octets sont portés.
#[test]
fn mutant_2_bis_utterance_entiere_substituee_refus_b2_fail_closed() {
    let mut lot = lot_reel();
    // Un octet des 944 octets portés : ils vivent après l'en-tête `bytes`.
    let mut aiguille = vec![0x65u8];
    aiguille.extend_from_slice(b"bytes");
    let debut = position(&lot, &aiguille);
    // `0x59` + longueur sur deux octets (944 > 255) : l'en-tête fait 3 octets.
    let cible = debut
        .checked_add(aiguille.len())
        .and_then(|position| position.checked_add(3))
        .expect("décalage dans les bornes");
    let case = lot.get_mut(cible).expect("position dans les bornes");
    let octets_mutes = *case ^ 0x01;
    *case = octets_mutes;
    // ... et l'empreinte portée est recalculée sur les octets mutés, pour que
    // (b1) passe et que (b2) soit le contrôle qui tranche.
    let octets_portes = octets_de_l_utterance(&lot);
    let empreinte = shogen_core::empreinte_sha256(&octets_portes);
    let mut aiguille_hash = vec![0x64u8];
    aiguille_hash.extend_from_slice(b"hash");
    aiguille_hash.extend_from_slice(&[0x58, 0x20]);
    let debut_hash = position(&lot, &aiguille_hash)
        .checked_add(aiguille_hash.len())
        .expect("décalage dans les bornes");
    for (rang, octet) in empreinte.iter().copied().enumerate() {
        let cible = debut_hash.checked_add(rang).expect("dans les bornes");
        if let Some(case) = lot.get_mut(cible) {
            *case = octet;
        }
    }

    let (code, _, erreur) = verifier("utterance-substituee", &lot);
    assert_eq!(
        code, CODE_VERIFICATION,
        "utterance substituée acceptée : {erreur}"
    );
    assert!(
        erreur.contains("utterance non constatée"),
        "le refus doit être celui de la liaison au constat (b2) : {erreur}"
    );
    assert!(
        erreur.contains("UtteranceNonConstatee"),
        "la variante exacte doit être imprimée : {erreur}"
    );
}

/// Les 944 octets portés par `utterance.bytes`, relus du lot — pour que le cas
/// précédent recalcule l'empreinte sur ce que le lot dit vraiment.
fn octets_de_l_utterance(lot: &[u8]) -> Vec<u8> {
    let mut aiguille = vec![0x65u8];
    aiguille.extend_from_slice(b"bytes");
    aiguille.extend_from_slice(&[0x59, 0x03, 0xB0]); // 944 octets
    let debut = position(lot, &aiguille)
        .checked_add(aiguille.len())
        .expect("dans les bornes");
    let fin = debut.checked_add(944).expect("dans les bornes");
    lot.get(debut..fin)
        .expect("les 944 octets portés sont dans le lot")
        .to_vec()
}

/// Mutant (iii) — **résidu non résolu**. Un identifiant du champ `residual`
/// devient un identifiant qu'aucun registre ne publie. Contrôle (d).
#[test]
fn mutant_3_residu_non_resolu_refus_d_fail_closed() {
    let mut lot = lot_reel();
    // « A(notary-neutrality) » → « A(notarx-neutrality) » : même longueur, tout
    // ASCII, lot toujours canonique.
    muter_une_lettre(&mut lot, "A(notary-neutrality)", 7, b'x');

    let (code, _, erreur) = verifier("residu", &lot);
    assert_eq!(
        code, CODE_VERIFICATION,
        "résidu non résolu accepté : {erreur}"
    );
    assert!(
        erreur.contains("VERDICT : refusé (fail-closed)"),
        "{erreur}"
    );
    assert!(erreur.contains("résidu non résolu"), "{erreur}");
    assert!(
        erreur.contains("A(notarx-neutrality)"),
        "le refus doit nommer l'identifiant fautif : {erreur}"
    );
    assert!(
        erreur.contains("ResiduNonResolu"),
        "la variante exacte doit être imprimée : {erreur}"
    );
}

// ---------------------------------------------------------------------------
// LES DEUX CHARGES QUE L'AMENDEMENT DU 2026-08-13 A SORTIES DU NON-LIÉ
// ---------------------------------------------------------------------------

/// Contrôle (f) — la clé épinglée est celle contre laquelle le contrôle délégué
/// a été conduit. Avant l'amendement, ces 4 octets (ici 71) étaient liés par
/// **aucun** contrôle recalculable : l'épinglage était décoratif.
#[test]
fn mutant_f_cle_epinglee_substituee_refus_fail_closed() {
    let mut lot = lot_reel();
    // Un chiffre de la clé épinglée devient un autre chiffre : même longueur,
    // toujours ASCII.
    muter_une_lettre(&mut lot, "k256 036aaecb", 5, b'1');

    let (code, _, erreur) = verifier("cle-epinglee", &lot);
    assert_eq!(
        code, CODE_VERIFICATION,
        "clé épinglée substituée acceptée : {erreur}"
    );
    assert!(erreur.contains("attestateur non constaté"), "{erreur}");
    assert!(
        erreur.contains("AttestorNonConstate"),
        "la variante exacte doit être imprimée : {erreur}"
    );
    assert!(
        erreur.contains("décoratif"),
        "le refus dit POURQUOI il existe : {erreur}"
    );
}

/// Contrôle (g) — l'instant porté est celui de la connexion constatée. L'autre
/// charge que l'amendement a fermée.
#[test]
fn mutant_g_instant_substitue_refus_fail_closed() {
    let mut lot = lot_reel();
    // `instant` en texte CBOR, puis l'en-tête d'entier sur 4 octets (`0x1a`),
    // puis la valeur gros-boutiste : on mute son octet de poids faible.
    let mut aiguille = vec![0x67u8];
    aiguille.extend_from_slice(b"instant");
    aiguille.push(0x1a);
    let debut = position(&lot, &aiguille);
    let cible = debut
        .checked_add(aiguille.len())
        .and_then(|position| position.checked_add(3))
        .expect("décalage dans les bornes");
    let case = lot.get_mut(cible).expect("position dans les bornes");
    *case ^= 0x01;

    let (code, _, erreur) = verifier("instant", &lot);
    assert_eq!(
        code, CODE_VERIFICATION,
        "instant substitué accepté : {erreur}"
    );
    assert!(erreur.contains("instant non constaté"), "{erreur}");
    assert!(
        erreur.contains("InstantNonConstate"),
        "la variante exacte doit être imprimée : {erreur}"
    );
}

/// L'alinéa **(h)** — le recoupement d'origine, ratifié par ADR-0015 point 17 :
/// l'hôte de `subject` est l'identité de serveur authentifiée que le constat
/// rapporte. Sans lui, un lot désignant une autre origine passerait (b), (c),
/// (f) et (g).
///
/// Ce que (h) ne ferme PAS — le chemin et la requête de `subject` — est la
/// limite d'ADR-0015 point 17 bis : elle est énumérée par le balayage de
/// `tests/temoignage_canonique.rs` et affichée par la phrase de verdict.
#[test]
fn mutant_origine_hote_substitue_refus_fail_closed() {
    let mut lot = lot_reel();
    // « api.binance.com » → « api.binancf.com » : hôte toujours canonique
    // (minuscule, ASCII, sans triplet), donc le refus n'est PAS un refus de
    // décodage — c'est le recoupement qui tranche.
    muter_une_lettre(&mut lot, "https://api.binance.com/", 18, b'f');

    let (code, _, erreur) = verifier("origine", &lot);
    assert_eq!(
        code, CODE_VERIFICATION,
        "origine substituée acceptée : {erreur}"
    );
    assert!(erreur.contains("origine non constatée"), "{erreur}");
    assert!(
        erreur.contains("api.binancf.com"),
        "le refus doit montrer l'hôte porté : {erreur}"
    );
    assert!(
        erreur.contains("OrigineNonConstatee"),
        "la variante exacte doit être imprimée : {erreur}"
    );
}

// ---------------------------------------------------------------------------
// LE CONTEXTE : sans registre, sans constat, avec un constat abîmé
// ---------------------------------------------------------------------------

#[test]
fn sans_contexte_le_lot_reel_est_refuse() {
    // *Fail-safe defaults* : ce que le vérificateur n'a pas pu établir n'est pas
    // admis par défaut. Un lot réel sans contexte n'est pas « valide » — il est
    // **non conclu**, et le binaire le dit en refusant.
    let repertoire = repertoire("sans-contexte");
    let chemin = repertoire.join("lot.cbor");
    std::fs::write(&chemin, lot_reel()).expect("écriture du lot");
    let (code, _, erreur) = executer(&[chemin.as_path()]);
    assert_eq!(code, CODE_VERIFICATION, "lot réel accepté sans contexte");
    assert!(erreur.contains("registre des résidus vide"), "{erreur}");
}

#[test]
fn un_constat_reel_ampute_d_une_cle_est_refuse() {
    // Le contrat d'ADR-0015 point 13 fige dix-huit clés ; un constat qui en perd
    // une n'est pas un constat, et le refus le nomme.
    let repertoire = repertoire("constat-ampute");
    let chemin = repertoire.join("lot.cbor");
    std::fs::write(&chemin, lot_reel()).expect("écriture du lot");
    let constat = std::fs::read_to_string(fixtures().join("s3-binance.constat.json"))
        .expect("constat réel versionné");
    let ampute = constat.replacen("\"server_name\":\"api.binance.com\",", "", 1);
    let chemin_constat = repertoire.join("constat.json");
    std::fs::write(&chemin_constat, ampute).expect("écriture du constat amputé");

    let (code, _, erreur) = executer(&[
        chemin.as_path(),
        Path::new("--registre"),
        &fixtures().join("s3-binance.registre.txt"),
        Path::new("--constat"),
        &chemin_constat,
    ]);
    assert_eq!(code, CODE_CONTEXTE, "constat amputé accepté : {erreur}");
    assert!(erreur.contains("clé « server_name » absente"), "{erreur}");
    assert!(erreur.contains("CleManquante"), "{erreur}");
}

#[test]
fn un_constat_reel_a_cle_repetee_est_refuse() {
    // Trouvaille F7, portée au contrat : l'ordre des clés ne change jamais le
    // verdict, et une clé répétée n'est pas « la dernière l'emporte ».
    let repertoire = repertoire("constat-repete");
    let chemin = repertoire.join("lot.cbor");
    std::fs::write(&chemin, lot_reel()).expect("écriture du lot");
    let constat = std::fs::read_to_string(fixtures().join("s3-binance.constat.json"))
        .expect("constat réel versionné");
    let repete = constat.replacen(
        "\"server_name\":\"api.binance.com\",",
        "\"server_name\":\"api.binance.com\",\"server_name\":\"api.binance.com\",",
        1,
    );
    let chemin_constat = repertoire.join("constat.json");
    std::fs::write(&chemin_constat, repete).expect("écriture du constat à doublon");

    let (code, _, erreur) = executer(&[
        chemin.as_path(),
        Path::new("--registre"),
        &fixtures().join("s3-binance.registre.txt"),
        Path::new("--constat"),
        &chemin_constat,
    ]);
    assert_eq!(code, CODE_CONTEXTE, "constat à clé répétée accepté");
    assert!(erreur.contains("clé répétée"), "{erreur}");
    assert!(erreur.contains("CleRepetee"), "{erreur}");
}
