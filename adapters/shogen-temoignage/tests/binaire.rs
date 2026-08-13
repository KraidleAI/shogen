//! **Le binaire de l'adapter, exercé** — nominal et fail-closed.
//!
//! Rattachement (G0) : **ADR-0001** (« les transports sont des adapters,
//! *testés*, jamais prouvés » — un adapter dont le binaire n'est exercé par
//! aucun test n'est même pas testé) ; **ADR-0011 point 1** (l'étage
//! d'intégration : le vrai binaire, à travers des fichiers) ; **ADR-0015
//! points 8 et 13** (les recoupements que la construction doit tenir) ;
//! **ADR-0010 point 5** (*fail-safe defaults* : ce qui n'a pas été établi
//! n'est pas écrit).
//!
//! # Ce que ces cas établissent, et ce qui les rend capables de mordre
//!
//! `tests/construction.rs` exerce la **bibliothèque**. Personne n'exerçait le
//! **binaire** : ni sa lecture d'arguments, ni ses lectures de fichiers, ni son
//! recoupement propre de la clé déposée, ni son code de sortie (revue G2 de la
//! vague 2, majeure C2). C'est ce que ce fichier ferme.
//!
//! Le cas nominal ne se contente pas d'un code 0 : il compare le sha256 du lot
//! écrit à celui que `crates/shogen-verifier/tests/fixtures/PROVENANCE.md`
//! porte, **relevé par `sha256sum` de GNU coreutils** — une autre
//! implémentation de SHA-256 que celle du cœur. Un condensé faux d'un seul côté
//! ne peut produire qu'un écart.
//!
//! Les cas de refus travaillent sur des **copies temporaires** : les fixtures
//! du compagnon sont des pièces versionnées et ne sont jamais écrites par un
//! test.

use std::path::{Path, PathBuf};
use std::process::Command;

/// Le code de refus du binaire (`src/main.rs`) — asseré, jamais supposé.
const CODE_REFUS: i32 = 65;
/// Le préfixe des artefacts déposés de la session attestée réelle.
const PREFIXE: &str = "shogen-s3-binance";
/// Le sha256 du lot canonique réel, tel que `PROVENANCE.md` le porte — relevé
/// par `sha256sum` (GNU coreutils), hors de ce dépôt et hors du cœur.
const SHA_DU_LOT: &str = "8700d88f87253f0fd8496402601dc7326362a2cd9e6614a9bf44b79052f1e5a3";
/// Sa taille, elle aussi portée par `PROVENANCE.md`.
const OCTETS_DU_LOT: usize = 7399;

/// Les cinq artefacts que le binaire lit.
const ARTEFACTS: &[&str] = &[
    "sent-revele.bin",
    "recv-revele.bin",
    "presentation.tlsn",
    "constat.json",
    "attestor-verifying-key.txt",
];

/// Les artefacts de la session attestée réelle — **lus, jamais écrits**.
fn artefacts() -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("..")
        .join("shogen-tlsn-verify")
        .join("fixtures")
}

/// Un répertoire de travail propre à ce processus (même motif que les suites du
/// vérificateur : un chemin fixe se fait effacer sous un exécuteur parallèle).
fn repertoire(nom: &str) -> PathBuf {
    let chemin =
        std::env::temp_dir().join(format!("shogen-temoignage-{nom}-{}", std::process::id()));
    let _ = std::fs::remove_dir_all(&chemin);
    std::fs::create_dir_all(&chemin).expect("création du répertoire de test");
    chemin
}

/// Copie les cinq artefacts dans un répertoire temporaire, pour qu'un cas puisse
/// en abîmer un sans toucher aux pièces versionnées.
fn copier_les_artefacts(vers: &Path) {
    for suffixe in ARTEFACTS {
        let nom = format!("{PREFIXE}.{suffixe}");
        std::fs::copy(artefacts().join(&nom), vers.join(&nom)).expect("copie de l'artefact");
    }
}

fn executer(repertoire_des_artefacts: &Path, sortie: &Path) -> (i32, String, String) {
    let resultat = Command::new(env!("CARGO_BIN_EXE_shogen-temoignage"))
        .arg(repertoire_des_artefacts)
        .arg(PREFIXE)
        .arg(sortie)
        .output()
        .expect("le binaire de l'adapter doit s'exécuter");
    (
        resultat.status.code().unwrap_or(-1),
        String::from_utf8_lossy(&resultat.stdout).into_owned(),
        String::from_utf8_lossy(&resultat.stderr).into_owned(),
    )
}

fn empreinte_hexadecimale(octets: &[u8]) -> String {
    shogen_core::empreinte_en_hexadecimal(&shogen_core::empreinte_sha256(octets))
}

// ---------------------------------------------------------------------------
// (i) LE RUN NOMINAL
// ---------------------------------------------------------------------------

#[test]
fn run_nominal_le_lot_ecrit_est_celui_qui_est_versionne_a_l_octet() {
    let repertoire = repertoire("nominal");
    let sortie = repertoire.join("s3-binance.lot.cbor");
    let (code, rendu, erreur) = executer(&artefacts(), &sortie);
    assert_eq!(
        code, 0,
        "le run nominal échoue\nstdout:{rendu}\nstderr:{erreur}"
    );

    let octets = std::fs::read(&sortie).expect("le lot doit avoir été écrit");
    assert_eq!(
        octets.len(),
        OCTETS_DU_LOT,
        "la taille du lot écrit ne suit plus PROVENANCE.md"
    );
    assert_eq!(
        empreinte_hexadecimale(&octets),
        SHA_DU_LOT,
        "le lot construit n'est plus, à l'octet, celui qui est versionné : la \
         chaîne de provenance du critère de sortie de S3 est rompue"
    );

    // Le rendu dit ce qu'il a écrit — un binaire qui réussit en silence ne se
    // relit pas.
    assert!(rendu.contains("lot canonique écrit"), "{rendu}");
    assert!(
        rendu.contains("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"),
        "le subject construit doit être imprimé : {rendu}"
    );
    println!("{rendu}");
}

#[test]
fn sans_les_trois_arguments_le_binaire_refuse_en_nommant_son_usage() {
    let resultat = Command::new(env!("CARGO_BIN_EXE_shogen-temoignage"))
        .output()
        .expect("le binaire de l'adapter doit s'exécuter");
    let code = resultat.status.code().unwrap_or(-1);
    let erreur = String::from_utf8_lossy(&resultat.stderr).into_owned();
    assert_eq!(code, CODE_REFUS, "un appel sans argument doit refuser");
    assert!(erreur.contains("REFUS (fail-closed)"), "{erreur}");
    assert!(erreur.contains("usage :"), "{erreur}");
}

#[test]
fn un_artefact_absent_est_un_refus_nomme_jamais_une_panique() {
    let repertoire = repertoire("artefact-absent");
    let artefacts_partiels = repertoire.join("artefacts");
    std::fs::create_dir_all(&artefacts_partiels).expect("création");
    copier_les_artefacts(&artefacts_partiels);
    std::fs::remove_file(artefacts_partiels.join(format!("{PREFIXE}.recv-revele.bin")))
        .expect("retrait de l'artefact");
    let sortie = repertoire.join("lot.cbor");

    let (code, _, erreur) = executer(&artefacts_partiels, &sortie);
    assert_eq!(code, CODE_REFUS, "artefact absent accepté : {erreur}");
    assert!(erreur.contains("lecture impossible"), "{erreur}");
    assert!(!erreur.contains("panicked"), "{erreur}");
    assert!(
        !sortie.exists(),
        "aucun lot ne doit être écrit sur un refus"
    );
}

// ---------------------------------------------------------------------------
// (ii) LES FIXTURES ABÎMÉES — sur COPIES, jamais sur les pièces versionnées
// ---------------------------------------------------------------------------

/// Prépare une copie des artefacts et laisse le cas en abîmer un.
fn cas_abime(nom: &str, abimer: impl FnOnce(&Path)) -> (i32, String, PathBuf) {
    let repertoire = repertoire(nom);
    let copies = repertoire.join("artefacts");
    std::fs::create_dir_all(&copies).expect("création");
    copier_les_artefacts(&copies);
    abimer(&copies);
    let sortie = repertoire.join("lot.cbor");
    let (code, _, erreur) = executer(&copies, &sortie);
    (code, erreur, sortie)
}

/// **Clé altérée** — la ligne de clé déposée par le compagnon ne compose plus
/// la clé du constat. C'est le recoupement propre à la coquille : deux pièces,
/// une seule clé.
#[test]
fn cle_deposee_alteree_refus_de_recoupement_fail_closed() {
    let (code, erreur, sortie) = cas_abime("cle-alteree", |copies| {
        let chemin = copies.join(format!("{PREFIXE}.attestor-verifying-key.txt"));
        let ligne = std::fs::read_to_string(&chemin).expect("ligne de clé déposée");
        // Un chiffre hexadécimal pour un autre : même longueur, toujours ASCII —
        // la ligne reste bien formée, c'est le recoupement qui tranche.
        let altere = ligne.replacen("k256 036aae", "k256 036aaf", 1);
        assert_ne!(altere, ligne, "la mutation doit changer quelque chose");
        std::fs::write(&chemin, altere).expect("écriture de la clé altérée");
    });
    assert_eq!(code, CODE_REFUS, "clé altérée acceptée : {erreur}");
    assert!(erreur.contains("REFUS (fail-closed)"), "{erreur}");
    assert!(
        erreur.contains("recoupement rompu (clé épinglée)"),
        "{erreur}"
    );
    assert!(!erreur.contains("panicked"), "{erreur}");
    assert!(
        !sortie.exists(),
        "aucun lot ne doit être écrit sur un refus"
    );
}

/// **Constat de refus** — le compagnon a refusé la présentation ; son constat
/// ne porte pas de `verdict`, il porte une erreur. Construire un témoignage
/// par-dessus serait bâtir sur un refus.
#[test]
fn constat_de_refus_refus_fail_closed() {
    let (code, erreur, sortie) = cas_abime("constat-de-refus", |copies| {
        let refus = std::fs::read(artefacts().join("mutant-1-octet-retourne.constat.json"))
            .expect("constat de refus versionné");
        std::fs::write(copies.join(format!("{PREFIXE}.constat.json")), refus)
            .expect("écriture du constat de refus");
    });
    assert_eq!(code, CODE_REFUS, "constat de refus accepté : {erreur}");
    assert!(erreur.contains("REFUS (fail-closed)"), "{erreur}");
    assert!(
        erreur.contains("clé « verdict » absente ou illisible"),
        "le refus doit nommer la clé qui manque : {erreur}"
    );
    assert!(!erreur.contains("panicked"), "{erreur}");
    assert!(
        !sortie.exists(),
        "aucun lot ne doit être écrit sur un refus"
    );
}

/// **`recv` muté** — un octet des 944 octets reçus change. La longueur ne bouge
/// pas, donc c'est l'empreinte qui tranche : celle du cœur cesse d'égaler celle
/// que le compagnon a calculée avec une autre implémentation.
#[test]
fn octets_recus_mutes_refus_d_empreinte_fail_closed() {
    let (code, erreur, sortie) = cas_abime("recv-mute", |copies| {
        let chemin = copies.join(format!("{PREFIXE}.recv-revele.bin"));
        let mut octets = std::fs::read(&chemin).expect("octets reçus déposés");
        let dernier = octets
            .last_mut()
            .expect("les octets reçus ne sont pas vides");
        *dernier ^= 0x01;
        std::fs::write(&chemin, &octets).expect("écriture des octets mutés");
    });
    assert_eq!(code, CODE_REFUS, "octets reçus mutés acceptés : {erreur}");
    assert!(erreur.contains("REFUS (fail-closed)"), "{erreur}");
    assert!(
        erreur.contains("recoupement rompu (empreinte des octets reçus)"),
        "le refus doit nommer le recoupement qui tombe : {erreur}"
    );
    assert!(!erreur.contains("panicked"), "{erreur}");
    assert!(
        !sortie.exists(),
        "aucun lot ne doit être écrit sur un refus"
    );
}
