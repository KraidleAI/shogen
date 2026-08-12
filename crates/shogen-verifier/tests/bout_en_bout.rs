//! **Le sommet de la pyramide : exactement un test de bout en bout** — le
//! walking skeleton lui-même (ADR-0011, point 1 : « au démarrage, **exactement
//! un** : le walking skeleton »).
//!
//! Il exerce le vrai binaire, pas une fonction : `CARGO_BIN_EXE_shogen-verifier`
//! est lancé comme un tiers le lancerait, sur un fichier d'octets.
//!
//! Le lot de référence est **réécrit à la main ici**, en-tête par en-tête,
//! sans passer par `shogen-core` : le vérificateur n'a aucune dépendance de
//! développement (S-G2), et un test qui produirait son entrée avec l'encodeur
//! qu'il vérifie ne testerait que la cohérence de l'encodeur avec lui-même.

use std::path::PathBuf;
use std::process::Command;

/// Le lot de référence, écrit octet par octet depuis la structure canonique
/// exigée par ADR-0002 (RFC 8949, Core Deterministic Encoding Requirements).
fn lot_de_reference() -> Vec<u8> {
    let mut octets: Vec<u8> = Vec::new();
    octets.push(0xa3); // map(3)
    octets.push(0x66); // texte(6)
    octets.extend_from_slice(b"source");
    octets.push(0x76); // texte(22)
    octets.extend_from_slice(b"exemple:source-factice");
    octets.push(0x67); // texte(7)
    octets.extend_from_slice(b"contenu");
    octets.push(0x58); // octets, longueur sur 1 octet
    octets.push(0x21); // 33
    octets.extend_from_slice(b"lot d'exemple du walking skeleton");
    octets.push(0x67); // texte(7)
    octets.extend_from_slice(b"instant");
    octets.push(0x1a); // uint, longueur sur 4 octets
    octets.extend_from_slice(&1_754_000_000u32.to_be_bytes());
    octets
}

fn repertoire(nom: &str) -> PathBuf {
    let chemin = std::env::temp_dir().join(format!("shogen-e2e-{nom}"));
    let _ = std::fs::remove_dir_all(&chemin);
    std::fs::create_dir_all(&chemin).expect("création du répertoire de test");
    chemin
}

fn executer(chemin: &PathBuf) -> (i32, String, String) {
    let sortie = Command::new(env!("CARGO_BIN_EXE_shogen-verifier"))
        .arg(chemin)
        .output()
        .expect("le binaire du vérificateur doit s'exécuter");
    (
        sortie.status.code().unwrap_or(-1),
        String::from_utf8_lossy(&sortie.stdout).into_owned(),
        String::from_utf8_lossy(&sortie.stderr).into_owned(),
    )
}

#[test]
fn lot_intact_accepte_et_le_residu_est_nomme() {
    let repertoire = repertoire("intact");
    let chemin = repertoire.join("lot.cbor");
    std::fs::write(&chemin, lot_de_reference()).expect("écriture du lot");

    let (code, sortie, erreur) = executer(&chemin);
    assert_eq!(
        code, 0,
        "lot intact refusé\nstdout:{sortie}\nstderr:{erreur}"
    );
    assert!(
        sortie.contains("VERDICT : octets conformes au sous-ensemble canonique"),
        "verdict absent : {sortie}"
    );
    assert!(
        sortie.contains("résidu : la conformité ne dit rien de la vérité de la source"),
        "le résidu doit être NOMMÉ dans le verdict : {sortie}"
    );
    assert!(
        sortie.contains("ADR-0001"),
        "le résidu cite son ADR : {sortie}"
    );
    assert!(
        sortie.contains("aucune horloge lue"),
        "l'instant est une donnée portée, et le verdict le dit : {sortie}"
    );
}

/// Les octets de **charge utile** : ceux dont la valeur est libre par
/// construction du format (le contenu opaque, et la valeur de l'horodatage tant
/// qu'elle reste en forme préférée).
///
/// **Limite du walking skeleton, mesurée et nommée ici plutôt que tue** : muter
/// l'un de ces octets ne produit pas un lot malformé — il produit un *autre*
/// témoignage, parfaitement canonique, que le vérificateur accepte à juste
/// titre. Détecter cette classe de mutation exige la liaison du témoignage à sa
/// preuve, c'est-à-dire le **hash des octets exacts** qu'ADR-0005 rend
/// obligatoire (« le hash des octets exacts est toujours porté … sans
/// exception ») — travail de S3, exclu de S2.5 (12 §1, aucune logique produit).
/// Écrire ici « tout octet muté est refusé » serait une surclamation.
fn positions_de_charge_utile(longueur: usize) -> Vec<usize> {
    let mut positions: Vec<usize> = (41..74).collect(); // les 33 octets de `contenu`
    positions.extend(83..longueur); // les 4 octets de la valeur de `instant`
    positions
}

#[test]
fn chaque_octet_mute_est_refuse_fail_closed_ou_reste_canonique() {
    let repertoire = repertoire("mute");
    let origine = lot_de_reference();
    let charge_utile = positions_de_charge_utile(origine.len());
    let mut refuses: Vec<usize> = Vec::new();
    let mut acceptes: Vec<usize> = Vec::new();

    for position in 0..origine.len() {
        let mut mute = origine.clone();
        mute[position] ^= 0xff;
        let chemin = repertoire.join(format!("lot-{position}.cbor"));
        std::fs::write(&chemin, &mute).expect("écriture du lot muté");
        let (code, sortie, erreur) = executer(&chemin);
        if code == 0 {
            assert!(
                charge_utile.contains(&position),
                "octet {position} (STRUCTURE) inversé : le vérificateur a ACCEPTÉ — fail-closed rompu\nstdout:{sortie}"
            );
            assert!(
                sortie.contains("round-trip exact"),
                "octet {position} accepté sans round-trip exact : {sortie}"
            );
            acceptes.push(position);
        } else {
            assert!(
                erreur.contains("VERDICT : refusé (fail-closed)"),
                "octet {position} : verdict de refus absent\nstderr:{erreur}"
            );
            assert!(
                erreur.contains("erreur nommée :"),
                "octet {position} : l'erreur n'est pas nommée\nstderr:{erreur}"
            );
            assert!(
                !erreur.contains("panicked"),
                "octet {position} : PANIQUE au lieu d'un refus\nstderr:{erreur}"
            );
            refuses.push(position);
        }
    }

    println!(
        "mutation d'octet bout-en-bout — {} positions : {} refus fail-closed nommés, {} acceptations (toutes en charge utile), 0 panique",
        origine.len(),
        refuses.len(),
        acceptes.len()
    );
    assert_eq!(
        acceptes, charge_utile,
        "l'ensemble des acceptations doit être EXACTEMENT la charge utile — \
         toute autre acceptation est une rupture du fail-closed, toute absence \
         est un changement de format non déclaré"
    );
    assert_eq!(
        refuses.len(),
        origine.len() - charge_utile.len(),
        "tout octet de structure muté doit être refusé"
    );
}

#[test]
fn lot_tronque_refuse() {
    let repertoire = repertoire("tronque");
    let origine = lot_de_reference();
    for longueur in [0usize, 1, 10, 40, origine.len() - 1] {
        let chemin = repertoire.join(format!("lot-{longueur}.cbor"));
        std::fs::write(&chemin, &origine[..longueur]).expect("écriture du lot tronqué");
        let (code, _, erreur) = executer(&chemin);
        assert_ne!(code, 0, "troncature à {longueur} acceptée");
        assert!(erreur.contains("erreur nommée :"), "stderr : {erreur}");
    }
}

#[test]
fn lot_rallonge_refuse() {
    let repertoire = repertoire("rallonge");
    let mut octets = lot_de_reference();
    octets.push(0x00);
    let chemin = repertoire.join("lot.cbor");
    std::fs::write(&chemin, &octets).expect("écriture du lot rallongé");
    let (code, _, erreur) = executer(&chemin);
    assert_ne!(code, 0, "octet en trop accepté");
    assert!(erreur.contains("octets résiduels"), "stderr : {erreur}");
}

#[test]
fn fichier_absent_refuse_sans_panique() {
    let chemin = repertoire("absent").join("inexistant.cbor");
    let (code, _, erreur) = executer(&chemin);
    assert_ne!(code, 0);
    assert!(erreur.contains("lot illisible"), "stderr : {erreur}");
    assert!(
        !erreur.contains("panicked"),
        "le vérificateur ne doit pas paniquer : {erreur}"
    );
}

#[test]
fn sans_argument_refuse() {
    let sortie = Command::new(env!("CARGO_BIN_EXE_shogen-verifier"))
        .output()
        .expect("exécution");
    assert_ne!(sortie.status.code().unwrap_or(-1), 0);
    let erreur = String::from_utf8_lossy(&sortie.stderr);
    assert!(erreur.contains("usage :"), "stderr : {erreur}");
}
