//! L'**identité du typeur** : ce que le binaire porte est ce que le dépôt
//! contient.
//!
//! Rattachement (G0) : **03 §3** (l'identité du typeur va dans le fait) ;
//! **ADR-0018** (l'empreinte du dépôt est SHA-256, écrite au cœur).
//!
//! L'empreinte embarquée est calculée sur des `include_str!` — donc sur ce que
//! la **compilation** a vu. Ce fichier relit les mêmes chemins **depuis le
//! disque** et recalcule : c'est ce qui attrape une dérive entre les deux (un
//! artefact rebâti d'un cache, une liste de fichiers oubliée).

use shogen_typer::identite::{FICHIERS_DE_LOGIQUE, empreinte_de_la_logique, octets_de_la_logique};
use std::fs;
use std::path::Path;

const CADRE: u8 = 0x0A;

fn racine() -> &'static Path {
    Path::new(env!("CARGO_MANIFEST_DIR"))
}

#[test]
fn l_empreinte_embarquee_est_celle_des_fichiers_sur_disque() {
    let mut octets = Vec::new();
    for (chemin, _) in FICHIERS_DE_LOGIQUE {
        let lu = fs::read(racine().join(chemin))
            .unwrap_or_else(|erreur| panic!("lecture de {chemin} : {erreur}"));
        let normalise: Vec<u8> = lu.into_iter().filter(|octet| *octet != b'\r').collect();
        octets.extend_from_slice(chemin.as_bytes());
        octets.push(CADRE);
        octets.extend_from_slice(normalise.len().to_string().as_bytes());
        octets.push(CADRE);
        octets.extend_from_slice(&normalise);
        octets.push(CADRE);
    }
    assert_eq!(
        octets,
        octets_de_la_logique(),
        "les octets d'identité embarqués diffèrent de ceux du disque"
    );
    assert_eq!(
        shogen_core::empreinte_sha256(&octets),
        empreinte_de_la_logique()
    );
    println!(
        "empreinte de la logique : {}",
        shogen_core::empreinte_en_hexadecimal(&empreinte_de_la_logique())
    );
}

/// Aucun fichier de logique n'échappe à l'identité : si `src/` gagne un module
/// et que la liste ne bouge pas, l'empreinte cesserait d'identifier la logique.
#[test]
fn la_liste_des_fichiers_de_logique_couvre_tout_src() {
    let mut sur_disque: Vec<String> = fs::read_dir(racine().join("src"))
        .unwrap_or_else(|erreur| panic!("lecture de src/ : {erreur}"))
        .filter_map(|entree| entree.ok())
        .map(|entree| entree.file_name().to_string_lossy().into_owned())
        .filter(|nom| nom.ends_with(".rs"))
        .map(|nom| format!("src/{nom}"))
        .collect();
    sur_disque.sort();

    let mut declares: Vec<String> = FICHIERS_DE_LOGIQUE
        .iter()
        .map(|(chemin, _)| String::from(*chemin))
        .collect();
    declares.sort();

    assert_eq!(
        declares, sur_disque,
        "src/ et FICHIERS_DE_LOGIQUE divergent"
    );
}

/// **Aucun flottant binaire, nulle part.** Contrôle lexical sur les sources du
/// typeur : `f32` et `f64` n'y apparaissent pas. Il est *syntaxique* — il
/// rejette des formes nommées, il n'établit pas l'absence de flottant dans le
/// binaire (même limite que la gate S-G3 du dépôt, ADR-0010 §Coûts point 6).
#[test]
fn aucun_flottant_binaire_dans_les_sources() {
    for (chemin, contenu) in FICHIERS_DE_LOGIQUE {
        for forme in ["f32", "f64", "as f", "to_bits", "from_bits"] {
            // Les commentaires de doc parlent des flottants pour dire qu'on
            // n'en veut pas : le contrôle ne porte que sur le code.
            let code: String = contenu
                .lines()
                .filter(|ligne| !ligne.trim_start().starts_with("//"))
                .collect::<Vec<_>>()
                .join("\n");
            assert!(
                !code.contains(forme),
                "forme « {forme} » trouvée dans le code de {chemin}"
            );
        }
    }
}
