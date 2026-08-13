//! **Le mutant du double-build, et ses témoins** — ADR-0012 D6.
//!
//! Doctrine gatewright (ADR-0013, invariant 3) : « la violation que la gate
//! existe à attraper est introduite, vue mourir, restaurée, puis **committée
//! comme test permanent**. Une gate jamais exercée ainsi n'a pas de registre
//! d'assurance. » Ici la violation à attraper est une **non-reproductibilité**,
//! et elle ne peut pas s'écrire en fixture de texte : il faut deux
//! constructions réelles.
//!
//! Ce que ce fichier fait :
//!
//! 1. **Le mutant** — un arbre **synthétique** (un paquet jouet sans
//!    dépendance) dont la source incorpore `SOURCE_DATE_EPOCH`, c'est-à-dire
//!    l'horloge du build : exactement le défaut que Debian chasse avec sa
//!    variation d'horloge. Le double-build doit rendre ROUGE, et le test
//!    exige davantage que le rouge : que les octets injectés soient
//!    **retrouvés dans les binaires**, chacun le sien. Sinon un rouge de
//!    plateforme (voir le témoin ci-dessous) suffirait à faire passer le test
//!    sans rien prouver.
//!    L'arbre est synthétique et non `shogen-verifier` : injecter le défaut
//!    dans le vérificateur voudrait dire modifier le périmètre sous gate
//!    S-G3/S-G2 pour la durée d'un test — l'arbre jouet obtient la même
//!    démonstration sans toucher au produit.
//! 2. **Les témoins** — la fonction de comparaison (pure) sur des octets
//!    fabriqués, et les vecteurs de contrôle de l'empreinte : ils garantissent
//!    qu'un ROUGE vient d'une divergence réelle et non d'un comparateur ou
//!    d'un SHA-256 faux.
//! 3. **Le témoin de plateforme** (Linux seul) — le même arbre jouet **sans**
//!    injection doit rester identique sous les six variations. C'est lui qui
//!    dit que le rouge du mutant vient de l'injection et non de la machinerie.

use shogen_core::{empreinte_en_hexadecimal, empreinte_sha256};
use std::path::{Path, PathBuf};
use std::process::Command;
use xtask::reproductible::{Comparaison, Plan, comparer};

// ---------------------------------------------------------------------------
// Témoins de l'empreinte
// ---------------------------------------------------------------------------

/// Les valeurs attendues ont été **mesurées** le 2026-08-13 contre deux
/// implémentations indépendantes (`python hashlib` pour toutes, coreutils
/// `sha256sum` pour les trois premières) — pas recopiées de mémoire. Les trois
/// premiers cas sont aussi les exemples publiés de FIPS 180-4 ; la norme n'est
/// pas détenue dans `biblio/`, donc ce qui fait foi ici est la mesure.
#[test]
fn temoin_sha256_vecteurs_mesures() {
    let cas: &[(&[u8], &str)] = &[
        (
            b"",
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        ),
        (
            b"abc",
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
        ),
        (
            b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq",
            "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1",
        ),
    ];
    for (message, attendu) in cas {
        let obtenu = empreinte_en_hexadecimal(&empreinte_sha256(message));
        assert_eq!(
            &obtenu,
            attendu,
            "empreinte fausse sur un message de {} octet(s)",
            message.len()
        );
    }
}

/// Les frontières du bourrage (§5.1.1) : 55 octets tiennent dans un bloc avec
/// la longueur, 56 forcent un second bloc, 64 est un bloc plein, 119/120
/// refont la même paire un bloc plus loin. Un bourrage faux passe inaperçu
/// partout ailleurs.
#[test]
fn temoin_sha256_frontieres_de_bourrage() {
    let cas: &[(usize, &str)] = &[
        (
            55,
            "9f4390f8d30c2dd92ec9f095b65e2b9ae9b0a925a5258e241c9f1e910f734318",
        ),
        (
            56,
            "b35439a4ac6f0948b6d6f9e3c6af0f5f590ce20f1bde7090ef7970686ec6738a",
        ),
        (
            63,
            "7d3e74a05d7db15bce4ad9ec0658ea98e3f06eeecf16b4c6fff2da457ddc2f34",
        ),
        (
            64,
            "ffe054fe7ae0cb6dc65c3af9b61d5209f439851db43d0ba5997337df154668eb",
        ),
        (
            119,
            "31eba51c313a5c08226adf18d4a359cfdfd8d2e816b13f4af952f7ea6584dcfb",
        ),
        (
            120,
            "2f3d335432c70b580af0e8e1b3674a7c020d683aa5f73aaaedfdc55af904c21c",
        ),
        (
            1000,
            "41edece42d63e8d9bf515a9ba6932e1c20cbc9f5a5d134645adb5db1b9737ea3",
        ),
    ];
    for (longueur, attendu) in cas {
        let message = vec![b'a'; *longueur];
        let obtenu = empreinte_en_hexadecimal(&empreinte_sha256(&message));
        assert_eq!(&obtenu, attendu, "empreinte fausse sur {longueur} octets");
    }
}

// ---------------------------------------------------------------------------
// Témoins et mutants de la comparaison (la fonction qui rend le verdict)
// ---------------------------------------------------------------------------

#[test]
fn temoin_comparaison_octets_identiques_est_verte() {
    assert!(matches!(
        comparer(b"des octets identiques", b"des octets identiques"),
        Comparaison::Identiques
    ));
}

#[test]
fn mutant_comparaison_nomme_le_premier_octet_divergent() {
    // Deux divergences : c'est la PREMIÈRE qui doit être rapportée — un
    // rapport qui nommerait la dernière enverrait l'enquête au mauvais endroit.
    match comparer(b"abcdefgh", b"abXdefYh") {
        Comparaison::DivergenceOctet { position, a, b } => {
            assert_eq!(position, 2);
            assert_eq!(a, b'c');
            assert_eq!(b, b'X');
        }
        _ => panic!("une divergence d'octet devait être rapportée"),
    }
}

#[test]
fn mutant_comparaison_tailles_differentes_sans_divergence_de_prefixe() {
    // Le cas qu'une comparaison naïve par `zip` laisse passer en vert : B est
    // un préfixe de A. Fail-closed : c'est ROUGE, et le rapport dit pourquoi.
    match comparer(b"abcdefgh", b"abcd") {
        Comparaison::TaillesDifferentes {
            prefixe_commun,
            taille_a,
            taille_b,
        } => {
            assert_eq!(prefixe_commun, 4);
            assert_eq!(taille_a, 8);
            assert_eq!(taille_b, 4);
        }
        _ => panic!("des tailles différentes devaient être rapportées"),
    }
}

// ---------------------------------------------------------------------------
// Le mutant du double-build : une non-reproductibilité injectée, vue ROUGE
// ---------------------------------------------------------------------------

/// La valeur de `SOURCE_DATE_EPOCH` que la commande donne à la construction A,
/// et celle qu'elle donne à B (+18 mois). Elles sont fixes par décision
/// (`reproductible::HORLOGE_A`), ce qui rend ce test déterministe.
const HORODATAGE_A: &str = "1754000000";
const HORODATAGE_B: &str = "1801347200";

#[test]
fn mutant_double_build_attrape_un_horodatage_incorpore() {
    let racine = racine_du_cas("mutant-horodatage");
    let source = arbre_jouet(&racine, &Jouet::HorodatageIncorpore);
    let plan = Plan {
        source,
        paquet: String::from("jouet"),
        base: racine.join("build"),
        cible: None,
    };

    let rapport = xtask::reproductible::executer(&plan)
        .expect("les deux constructions du jouet doivent aboutir");
    rapport.imprimer();

    assert!(
        !rapport.vert(),
        "le double-build devait être ROUGE : le jouet incorpore l'horloge du build"
    );
    assert_ne!(
        rapport.empreinte_a, rapport.empreinte_b,
        "deux binaires divergents ne peuvent pas porter la même empreinte"
    );
    assert!(
        matches!(
            rapport.comparaison,
            Comparaison::DivergenceOctet { .. } | Comparaison::TaillesDifferentes { .. }
        ),
        "le rapport doit localiser la divergence, pas seulement la constater"
    );

    // La preuve de causalité : ce n'est pas un rouge de plateforme, c'est
    // l'horodatage injecté qu'on retrouve, chacun dans son binaire.
    let octets_a = std::fs::read(&rapport.binaire_a).expect("binaire A lisible");
    let octets_b = std::fs::read(&rapport.binaire_b).expect("binaire B lisible");
    assert!(
        contient(&octets_a, HORODATAGE_A.as_bytes())
            && !contient(&octets_a, HORODATAGE_B.as_bytes()),
        "le binaire A doit porter l'horodatage de la construction A, et lui seul"
    );
    assert!(
        contient(&octets_b, HORODATAGE_B.as_bytes())
            && !contient(&octets_b, HORODATAGE_A.as_bytes()),
        "le binaire B doit porter l'horodatage de la construction B, et lui seul"
    );
}

/// Le témoin qui donne son sens au mutant : le même arbre, **sans** injection,
/// reste bit-à-bit identique sous les six variations.
///
/// **Linux seulement, et le motif est une mesure, pas une préférence.** Le
/// 2026-08-13, le double-build de `shogen-verifier` sur `x86_64-pc-windows-msvc`
/// (toolchain 1.97.1) a rendu ROUGE, premier octet divergent en **position
/// 240** : `e_lfanew` vaut 0xE8, donc 240 est le champ `TimeDateStamp` de
/// l'en-tête COFF (mesuré : A = 0xba contre B = 0xbc, l'écart d'horloge entre
/// les deux éditions de liens), les autres divergences étant les copies de cet
/// horodatage dans le répertoire de débogage et la signature RSDS du PDB.
/// L'éditeur de liens y estampille l'horloge : aucune des six variations n'est
/// en cause. La position 240 est retrouvée d'une passe à l'autre et sur deux
/// arbres différents — c'est un fait de plateforme stable, pas un aléa —, et la
/// même commande sur `x86_64-unknown-linux-gnu` rend VERT (empreintes
/// identiques sur trois exécutions, contrôlées contre `sha256sum`). C'est
/// exactement l'asymétrie qu'ADR-0012 D6 ratifie — « Linux x86_64 d'abord,
/// Windows *à terme* et sans date ». Un témoin qui serait rouge sur Windows
/// pour une raison étrangère à ce qu'il teste ne serait pas un témoin.
#[cfg(target_os = "linux")]
#[test]
fn temoin_double_build_sans_injection_reste_identique() {
    let racine = racine_du_cas("temoin-sans-injection");
    let source = arbre_jouet(&racine, &Jouet::Sain);
    let plan = Plan {
        source,
        paquet: String::from("jouet"),
        base: racine.join("build"),
        cible: None,
    };

    let rapport = xtask::reproductible::executer(&plan)
        .expect("les deux constructions du jouet doivent aboutir");
    rapport.imprimer();

    assert!(
        rapport.vert(),
        "sans injection, les six variations ne doivent rien changer aux octets"
    );
    assert_eq!(rapport.empreinte_a, rapport.empreinte_b);
}

/// Fail-closed : une construction qui n'aboutit pas n'est pas « aucune
/// divergence constatée ». Le double-build refuse de rendre un verdict, et
/// dit **laquelle** des deux constructions a échoué.
///
/// C'est le chemin qu'une commande complaisante prendrait pour être verte :
/// ne pas construire, ne rien comparer, ne rien trouver.
#[test]
fn mutant_construction_en_echec_ne_rend_aucun_verdict() {
    let racine = racine_du_cas("mutant-compilation");
    let source = arbre_jouet(&racine, &Jouet::NeCompilePas);
    let plan = Plan {
        source,
        paquet: String::from("jouet"),
        base: racine.join("build"),
        cible: None,
    };

    let erreur = xtask::reproductible::executer(&plan)
        .err()
        .expect("une source qui ne compile pas ne peut donner aucun rapport");
    assert!(
        erreur.contains("construction A") && erreur.contains("fail-closed"),
        "l'erreur doit nommer la construction en échec et son régime ; obtenu : {erreur}"
    );
}

/// `--base` est effacé récursivement : le désigner sur un arbre de travail
/// serait la seule faute irréversible de cette commande. Le mutant vise les
/// deux fautes de frappe plausibles — `--base` posé SUR les sources, et
/// `--base` posé SOUS elles.
///
/// Les deux ont été vues nuire quand le garde-fou était retiré : la copie de
/// l'arbre dans un répertoire situé sous lui-même récurse jusqu'au débordement
/// de pile (`STATUS_STACK_BUFFER_OVERRUN`, mesuré le 2026-08-13).
#[test]
fn mutant_base_dans_l_arbre_source_est_refusee_avant_toute_suppression() {
    let racine = racine_du_cas("mutant-base");
    let source = arbre_jouet(&racine, &Jouet::HorodatageIncorpore);

    for base in [source.clone(), source.join("travail")] {
        let plan = Plan {
            source: source.clone(),
            paquet: String::from("jouet"),
            base,
            cible: None,
        };
        let erreur = xtask::reproductible::executer(&plan)
            .err()
            .expect("un --base dans l'arbre source doit être refusé");
        assert!(
            erreur.contains("refus"),
            "le refus doit se nommer ; obtenu : {erreur}"
        );
        assert!(
            source.join("Cargo.toml").is_file(),
            "les sources doivent être intactes : le refus vient AVANT la suppression"
        );
    }
}

// ---------------------------------------------------------------------------
// L'arbre jouet
// ---------------------------------------------------------------------------

fn racine_du_cas(cas: &str) -> PathBuf {
    let racine = std::env::temp_dir().join(format!("shogen-d6-{cas}"));
    let _ = std::fs::remove_dir_all(&racine);
    racine
}

/// Ce que la source du jouet contient.
enum Jouet {
    /// Rien qui dépende de l'environnement : la construction doit être stable.
    ///
    /// N'existe que là où un témoin peut l'exiger — c'est-à-dire sur la cible
    /// ratifiée (voir `temoin_double_build_sans_injection_reste_identique`).
    /// Ailleurs, ce jouet n'aurait aucun test pour l'employer, et une variante
    /// jamais construite est du code mort que `-D warnings` refuse à juste
    /// titre.
    #[cfg(target_os = "linux")]
    Sain,
    /// L'INJECTION : l'horloge du build entre dans le binaire. C'est le patron
    /// de non-reproductibilité le plus courant, et celui que la variation
    /// d'horloge de D6 vise.
    HorodatageIncorpore,
    /// Une source qui ne compile pas — pour exercer le fail-closed.
    NeCompilePas,
}

/// Écrit un paquet jouet sans dépendance et rend le chemin de sa racine.
///
/// La source vit sous `<racine>/source`, jamais sous `<racine>/build` que le
/// double-build efface à chaque exécution.
fn arbre_jouet(racine: &Path, jouet: &Jouet) -> PathBuf {
    let source = racine.join("source");
    std::fs::create_dir_all(source.join("src")).expect("création de l'arbre jouet");
    ecrire(
        &source.join("Cargo.toml"),
        "[package]\nname = \"jouet\"\nversion = \"0.0.0\"\nedition = \"2021\"\n\n[[bin]]\nname = \"jouet\"\npath = \"src/main.rs\"\n\n[dependencies]\n",
    );
    let source_rust = match jouet {
        #[cfg(target_os = "linux")]
        Jouet::Sain => "fn main() {\n    println!(\"jouet\");\n}\n",
        Jouet::HorodatageIncorpore => {
            "const HORODATAGE_DU_BUILD: &str = env!(\"SOURCE_DATE_EPOCH\");\n\nfn main() {\n    println!(\"jouet construit a {HORODATAGE_DU_BUILD}\");\n}\n"
        }
        Jouet::NeCompilePas => "fn main() {\n    ceci n'est pas du Rust\n}\n",
    };
    ecrire(&source.join("src").join("main.rs"), source_rust);
    generer_lockfile(&source);
    source
}

fn ecrire(chemin: &Path, contenu: &str) {
    if let Some(parent) = chemin.parent() {
        std::fs::create_dir_all(parent).expect("création du répertoire");
    }
    std::fs::write(chemin, contenu)
        .unwrap_or_else(|e| panic!("écriture {} : {e}", chemin.display()));
}

/// Le double-build construit avec `--locked` (ADR-0012 D1) : l'arbre jouet
/// doit donc porter son lockfile, et c'est cargo qui l'écrit — un lockfile
/// recopié en dur périmerait au premier changement de format.
fn generer_lockfile(source: &Path) {
    let cargo = std::env::var("CARGO").unwrap_or_else(|_| String::from("cargo"));
    let statut = Command::new(cargo)
        .args(["generate-lockfile", "--offline"])
        .current_dir(source)
        .env_remove("CARGO_TARGET_DIR")
        .status()
        .expect("cargo generate-lockfile exécutable");
    assert!(statut.success(), "génération du lockfile jouet en échec");
}

fn contient(botte: &[u8], aiguille: &[u8]) -> bool {
    botte
        .windows(aiguille.len())
        .any(|fenetre| fenetre == aiguille)
}
