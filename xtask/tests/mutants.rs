//! **Les mutants semés, en test permanent.**
//!
//! Doctrine gatewright, invariant 3 d'ADR-0013 : « *mutant semé tué avant tout
//! vert* — la violation que la gate existe à attraper est introduite, vue
//! mourir, restaurée, puis **committée comme test permanent**. Une gate jamais
//! exercée ainsi n'a pas de registre d'assurance. »
//!
//! Ce que ce fichier fait, à chaque exécution de `cargo test` :
//!
//! 1. construit un arbre **temporaire** (l'arbre de travail n'est jamais
//!    modifié — règle du dépôt) : copie des chemins exacts des deux rôles
//!    pour les gates de code (S-G1/2/3/7a), arbre **synthétique** pour les
//!    gates documentaires (S-G4/5/6/8 — les registres réels bougent à
//!    chaque passe, voir le commentaire de leur section) ;
//! 2. contrôle que l'arbre intact est VERT (sinon la mesure suivante ne
//!    voudrait rien dire) ;
//! 3. injecte la violation — depuis une fixture versionnée de
//!    `xtask/tests/fixtures/` pour le code Rust, en ligne pour les
//!    documents ;
//! 4. exige le ROUGE, et exige que le motif rapporté soit celui attendu ;
//! 5. l'arbre temporaire meurt avec le test.
//!
//! Registre : ces mutants sont des *mutants de gate* (ADR-0011, point 4,
//! premier registre) — **pas** de l'analyse de mutation : la population n'est
//! ni systématique ni comptée, et aucun score n'en sort. C'est un test négatif
//! de l'outil, et c'est tout ce qu'il prétend être.

mod commun;

use commun::Arbre;
use std::path::{Path, PathBuf};
use xtask::rapport::Rapport;

fn racine_depot() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .map(Path::to_path_buf)
        .expect("le manifeste xtask a un parent : la racine du dépôt")
}

fn fixture(nom: &str) -> String {
    let chemin = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("tests")
        .join("fixtures")
        .join(nom);
    std::fs::read_to_string(&chemin)
        .unwrap_or_else(|e| panic!("fixture illisible {} : {e}", chemin.display()))
}

/// Copie les chemins EXACTS sous gate dans un arbre temporaire neuf.
fn arbre_copie(nom_du_cas: &str) -> Arbre {
    let cible = Arbre::nouveau("shogen-mutant", nom_du_cas);
    let source = racine_depot();
    for relatif in ["crates/shogen-core/src", "crates/shogen-verifier/src"] {
        copier_repertoire(&source.join(relatif), &cible.join(relatif));
    }
    for relatif in [
        "crates/shogen-core/Cargo.toml",
        "crates/shogen-verifier/Cargo.toml",
    ] {
        let destination = cible.join(relatif);
        if let Some(parent) = destination.parent() {
            std::fs::create_dir_all(parent).expect("création du répertoire de copie");
        }
        std::fs::copy(source.join(relatif), destination).expect("copie du manifeste");
    }
    cible
}

fn copier_repertoire(source: &Path, cible: &Path) {
    std::fs::create_dir_all(cible).expect("création du répertoire de copie");
    for entree in std::fs::read_dir(source).expect("lecture du répertoire source") {
        let entree = entree.expect("entrée de répertoire");
        let chemin = entree.path();
        let nom = entree.file_name();
        if chemin.is_dir() {
            copier_repertoire(&chemin, &cible.join(nom));
        } else {
            std::fs::copy(&chemin, cible.join(nom)).expect("copie de fichier");
        }
    }
}

fn ajouter(racine: &Path, relatif: &str, fragment: &str) {
    let chemin = racine.join(relatif);
    let mut texte = std::fs::read_to_string(&chemin).expect("lecture du fichier à muter");
    texte.push_str(fragment);
    std::fs::write(&chemin, texte).expect("écriture du fichier muté");
}

fn ecrire(racine: &Path, relatif: &str, contenu: &str) {
    let chemin = racine.join(relatif);
    if let Some(parent) = chemin.parent() {
        std::fs::create_dir_all(parent).expect("création du répertoire");
    }
    std::fs::write(&chemin, contenu).expect("écriture du fichier");
}

fn remplacer(racine: &Path, relatif: &str, avant: &str, apres: &str) {
    let chemin = racine.join(relatif);
    let texte = std::fs::read_to_string(&chemin).expect("lecture du fichier à muter");
    assert!(
        texte.contains(avant),
        "le texte à remplacer est absent de {relatif} : {avant}"
    );
    std::fs::write(&chemin, texte.replace(avant, apres)).expect("écriture du fichier muté");
}

fn gates(racine: &Path) -> Vec<Rapport> {
    vec![
        xtask::sg1::executer(racine),
        xtask::sg2::executer(racine, false),
        xtask::sg3::executer(racine),
        xtask::sg7a::executer(racine),
    ]
}

fn rapport_de<'a>(rapports: &'a [Rapport], gate: &str) -> &'a Rapport {
    rapports
        .iter()
        .find(|rapport| rapport.gate == gate)
        .unwrap_or_else(|| panic!("rapport {gate} absent"))
}

fn motifs(rapport: &Rapport) -> String {
    rapport
        .violations
        .iter()
        .map(|violation| {
            format!(
                "{}:{} {}",
                violation.chemin, violation.ligne, violation.motif
            )
        })
        .collect::<Vec<_>>()
        .join("\n")
}

/// Contrôle préalable, sans lequel aucun rouge ne prouverait rien : l'arbre
/// copié INTACT est vert sur les quatre gates.
#[test]
fn temoin_arbre_intact_est_vert() {
    let racine = arbre_copie("temoin");
    for rapport in gates(&racine) {
        assert!(
            rapport.vert(),
            "l'arbre intact devrait être VERT sur {} :\n{}",
            rapport.gate,
            motifs(&rapport)
        );
        assert_eq!(
            rapport.examines, rapport.presents,
            "{} : couverture incomplète ({} examinés sur {} présents)",
            rapport.gate, rapport.examines, rapport.presents
        );
        assert!(rapport.presents > 0, "{} : rien d'examiné", rapport.gate);
    }
}

fn exiger_rouge(rapport: &Rapport, attendu: &str) {
    // La sortie rouge est imprimée telle quelle : `cargo test -p xtask --test
    // mutants -- --nocapture` rejoue la preuve, elle ne la résume pas.
    rapport.imprimer();
    assert!(
        !rapport.vert(),
        "{} devait être ROUGE et ne l'est pas",
        rapport.gate
    );
    let motifs = motifs(rapport);
    assert!(
        motifs.contains(attendu),
        "{} est rouge mais pour un autre motif ; attendu « {attendu} », obtenu :\n{motifs}",
        rapport.gate
    );
}

#[test]
fn mutant_sg1_nom_de_transport_en_commentaire_du_coeur() {
    let racine = arbre_copie("sg1-commentaire");
    ajouter(
        &racine,
        "crates/shogen-core/src/temoignage.rs",
        &fixture("sg1_transport_commentaire.frag"),
    );
    let rapports = gates(&racine);
    exiger_rouge(rapport_de(&rapports, "S-G1"), "nom de transport « tlsn »");
}

#[test]
fn mutant_sg1_nom_de_transport_en_constante_du_verificateur() {
    let racine = arbre_copie("sg1-constante");
    ajouter(
        &racine,
        "crates/shogen-verifier/src/main.rs",
        &fixture("sg1_transport_constante.frag"),
    );
    let rapports = gates(&racine);
    exiger_rouge(
        rapport_de(&rapports, "S-G1"),
        "nom de transport « reclaim »",
    );
}

#[test]
fn mutant_sg2_arete_du_verificateur_vers_un_adapter() {
    let racine = arbre_copie("sg2-adapter");
    ajouter(
        &racine,
        "crates/shogen-verifier/Cargo.toml",
        &fixture("sg2_arete_adapter.frag"),
    );
    let rapports = gates(&racine);
    exiger_rouge(rapport_de(&rapports, "S-G2"), "arête vers un adapter");
}

#[test]
fn mutant_sg2_horloge_dans_le_verificateur() {
    let racine = arbre_copie("sg2-horloge");
    ajouter(
        &racine,
        "crates/shogen-verifier/src/main.rs",
        &fixture("sg2_horloge.frag"),
    );
    let rapports = gates(&racine);
    exiger_rouge(
        rapport_de(&rapports, "S-G2"),
        "forme interdite « std::time »",
    );
}

#[test]
fn mutant_sg2_io_dans_le_coeur() {
    let racine = arbre_copie("sg2-io");
    ajouter(
        &racine,
        "crates/shogen-core/src/cbor.rs",
        &fixture("sg2_io_coeur.frag"),
    );
    let rapports = gates(&racine);
    exiger_rouge(
        rapport_de(&rapports, "S-G2"),
        "forme interdite « println! »",
    );
}

#[test]
fn mutant_sg3_unwrap_dans_le_coeur() {
    let racine = arbre_copie("sg3-unwrap");
    ajouter(
        &racine,
        "crates/shogen-core/src/cbor.rs",
        &fixture("sg3_unwrap.frag"),
    );
    let rapports = gates(&racine);
    exiger_rouge(
        rapport_de(&rapports, "S-G3"),
        "forme divergente « unwrap( »",
    );
}

#[test]
fn mutant_sg3_indexation_dans_le_verificateur() {
    let racine = arbre_copie("sg3-indexation");
    ajouter(
        &racine,
        "crates/shogen-verifier/src/main.rs",
        &fixture("sg3_indexation.frag"),
    );
    let rapports = gates(&racine);
    exiger_rouge(rapport_de(&rapports, "S-G3"), "indexation non contrôlée");
}

#[test]
fn mutant_sg3_arithmetique_dans_le_coeur() {
    let racine = arbre_copie("sg3-arithmetique");
    ajouter(
        &racine,
        "crates/shogen-core/src/temoignage.rs",
        &fixture("sg3_arithmetique.frag"),
    );
    let rapports = gates(&racine);
    exiger_rouge(rapport_de(&rapports, "S-G3"), "arithmétique non contrôlée");
}

#[test]
fn mutant_sg3_attribut_forbid_unsafe_retire() {
    let racine = arbre_copie("sg3-forbid");
    remplacer(
        &racine,
        "crates/shogen-verifier/src/main.rs",
        "#![forbid(unsafe_code)]\n",
        "",
    );
    let rapports = gates(&racine);
    exiger_rouge(
        rapport_de(&rapports, "S-G3"),
        "attribut « #![forbid(unsafe_code)] » absent",
    );
}

/// Mutant semé de la **scission `no_std`** (2026-08-13, échéance ADR-0009
/// point 6) : depuis que `shogen-verifier` a deux racines de compilation, un
/// `forbid(unsafe_code)` retiré de la **bibliothèque** doit rougir tout autant
/// que retiré de la coquille. Avant la scission, la gate ne regardait que
/// `main.rs` — ce test est la preuve que le trou est fermé, pas l'affirmation
/// qu'il l'est.
#[test]
fn mutant_sg3_attribut_forbid_unsafe_retire_de_la_bibliotheque() {
    let racine = arbre_copie("sg3-forbid-lib");
    remplacer(
        &racine,
        "crates/shogen-verifier/src/lib.rs",
        "#![forbid(unsafe_code)]\n",
        "",
    );
    let rapports = gates(&racine);
    exiger_rouge(
        rapport_de(&rapports, "S-G3"),
        "attribut « #![forbid(unsafe_code)] » absent",
    );
}

#[test]
fn mutant_couverture_repertoire_de_role_supprime() {
    let racine = arbre_copie("couverture-role");
    std::fs::remove_dir_all(racine.join("crates/shogen-core/src"))
        .expect("suppression du répertoire de rôle");
    let rapports = gates(&racine);
    for gate in ["S-G1", "S-G2", "S-G3"] {
        exiger_rouge(
            rapport_de(&rapports, gate),
            "répertoire absent ou illisible",
        );
    }
}

#[test]
fn mutant_couverture_fichier_neuf_dans_le_role() {
    let racine = arbre_copie("couverture-fichier");
    ecrire(
        &racine,
        "crates/shogen-core/src/sous_module/ajout.rs",
        &fixture("couverture_fichier_ajoute.frag"),
    );
    let rapports = gates(&racine);
    exiger_rouge(
        rapport_de(&rapports, "S-G3"),
        "forme divergente « unwrap( »",
    );
    assert!(
        rapport_de(&rapports, "S-G3").presents >= 6,
        "le fichier neuf doit entrer dans la couverture"
    );
}

#[test]
fn mutant_sg7a_version_non_exacte() {
    let racine = arbre_copie("sg7a-version");
    remplacer(
        &racine,
        "crates/shogen-core/Cargo.toml",
        "version = \"=1.11.0\"",
        "version = \"1.11.0\"",
    );
    let rapports = gates(&racine);
    exiger_rouge(rapport_de(&rapports, "S-G7a"), "version non exacte");
}

#[test]
fn mutant_sg2_manifeste_illisible_par_la_gate() {
    let racine = arbre_copie("sg2-manifeste");
    ajouter(
        &racine,
        "crates/shogen-verifier/Cargo.toml",
        "\n[dependencies]\nune ligne que l'analyseur ne comprend pas {\n",
    );
    let rapports = gates(&racine);
    exiger_rouge(rapport_de(&rapports, "S-G2"), "non analysable");
}

// ---------------------------------------------------------------------------
// Gates documentaires S-G4/S-G5/S-G6/S-G8 (unité orchestrateur, passe S3 —
// dette 12 §10 item 2). Les mutants tournent sur un arbre SYNTHÉTIQUE minimal,
// pas sur une copie du dépôt : les registres réels bougent à chaque passe
// (versements biblio/, lignes de journal) et un test qui exigerait leur vert
// permanent coulerait la suite à chaque acquisition — le témoin synthétique
// fixe l'état « conforme » une fois pour toutes.
// ---------------------------------------------------------------------------

/// Construit l'arbre documentaire synthétique conforme : docs/ (registre 09
/// présent + une note propre), s2-harness/ (un README propre — périmètre de
/// S-G4/S-G5 depuis SHOGEN-ORACLE-PERIMETRE-1 (i)), JOURNAL.md valide,
/// biblio/INDEX.md dont l'en-tête et les mentions concordent avec deux
/// artefacts présents.
fn arbre_documentaire(nom_du_cas: &str) -> Arbre {
    let racine = Arbre::nouveau("shogen-mutant-doc", nom_du_cas);
    ecrire(
        &racine,
        "docs/09-vocabulaire.md",
        "# registre synthétique\n\n| interdit |\n|---|\n| « donnée vérifiée » |\n",
    );
    ecrire(
        &racine,
        "docs/note.md",
        concat!(
            "# note synthétique\n\n",
            "Le registre interdit « donnée vérifiée » — la locution est ici en\n",
            "citation marquée et la voix du projet reste propre.\n\n",
            "Une citation adossée : « this quotation is present in the corpus and\n",
            "it is checked by the gate ».\n",
        ),
    );
    ecrire(
        &racine,
        "s2-harness/README.md",
        concat!(
            "# harnais synthétique\n\n",
            "Le harnais nomme « donnée vérifiée » en citation marquée.\n\n",
            "Une citation adossée : « this quotation is present in the corpus and\n",
            "it is checked by the gate ».\n",
        ),
    );
    ecrire(
        &racine,
        "JOURNAL.md",
        concat!(
            "# journal synthétique\n\n",
            "| date | unité | résultat |\n",
            "|---|---|---|\n",
            "| 2026-08-11 | première unité | rendue |\n",
            "| 2026-08-12 | seconde unité | rendue |\n",
        ),
    );
    ecrire(
        &racine,
        "biblio/INDEX.md",
        concat!(
            "# registre synthétique\n\n",
            "**2 artefacts détenus** au 2026-08-12.\n\n",
            "| fichier |\n|---|\n",
            "| `artefact-a.html` |\n",
            "| `artefact-b.txt` |\n",
        ),
    );
    ecrire(
        &racine,
        "biblio/artefact-a.html",
        "<p>this quotation is present in the corpus and it is checked by the gate</p>\n",
    );
    ecrire(&racine, "biblio/artefact-b.txt", "contenu quelconque\n");
    racine
}

fn gates_documentaires(racine: &Path) -> Vec<Rapport> {
    vec![
        xtask::sg4::executer(racine),
        xtask::sg5::executer(racine),
        xtask::sg6::executer(racine),
        xtask::sg8::executer(racine),
    ]
}

/// Témoin : l'arbre documentaire synthétique conforme est VERT sur les quatre
/// gates — y compris la locution interdite PRÉSENTE mais en citation marquée —
/// et la ligne de couverture est pleine (invariant 2 d'ADR-0013, même
/// exigence que le témoin des gates de rôle).
#[test]
fn temoin_arbre_documentaire_intact_est_vert() {
    let racine = arbre_documentaire("temoin");
    let rapports = gates_documentaires(&racine);
    for rapport in &rapports {
        assert!(
            rapport.vert(),
            "l'arbre documentaire intact devrait être VERT sur {} :\n{}",
            rapport.gate,
            motifs(rapport)
        );
        assert_eq!(
            rapport.examines, rapport.presents,
            "{} : couverture incomplète ({} examinés sur {} présents)",
            rapport.gate, rapport.examines, rapport.presents
        );
        assert!(rapport.presents > 0, "{} : rien d'examiné", rapport.gate);
    }
    // Vert pour la bonne raison : le README synthétique du harnais est
    // recensé et sa couverture imprimée, pas ignoré.
    for gate in ["S-G4", "S-G5"] {
        let couverts = rapport_de(&rapports, gate).chemins_couverts.join("\n");
        assert!(
            couverts.contains("s2-harness/**/*.md : 1 fichier(s)"),
            "{gate} doit imprimer la couverture de s2-harness/ ; chemins :\n{couverts}"
        );
    }
}

#[test]
fn mutant_sg4_locution_interdite_dans_la_voix_du_projet() {
    let racine = arbre_documentaire("sg4-locution");
    ajouter(
        &racine,
        "docs/note.md",
        "\nCette donnée vérifiée fonde le verdict.\n",
    );
    let rapports = gates_documentaires(&racine);
    exiger_rouge(rapport_de(&rapports, "S-G4"), "« donnée vérifiée »");
}

#[test]
fn mutant_sg4_guillemet_ouvert_jamais_referme() {
    let racine = arbre_documentaire("sg4-guillemet");
    ajouter(
        &racine,
        "docs/note.md",
        "\nUne « citation ouverte qui ne se referme jamais.\n",
    );
    let rapports = gates_documentaires(&racine);
    exiger_rouge(rapport_de(&rapports, "S-G4"), "jamais refermé");
}

#[test]
fn mutant_sg5_citation_hors_corpus() {
    let racine = arbre_documentaire("sg5-citation");
    ajouter(
        &racine,
        "docs/note.md",
        "\nUne citation forgée : « this quotation is not anywhere in the corpus\nand the gate must catch it ».\n",
    );
    let rapports = gates_documentaires(&racine);
    exiger_rouge(rapport_de(&rapports, "S-G5"), "citation introuvable");
}

// SHOGEN-ORACLE-PERIMETRE-1 (i) (ADR-0028 annexe B) : README et RUNBOOK de
// `s2-harness/` entrent au périmètre de S-G4 et S-G5. Chaque mutant exige le
// ROUGE pour le motif attendu ET situé dans le harnais.
fn exiger_rouge_dans_le_harnais(rapport: &Rapport, attendu: &str) {
    exiger_rouge(rapport, attendu);
    let motifs = motifs(rapport);
    assert!(
        motifs.contains("s2-harness/README.md:"),
        "{} : la violation doit être située dans le harnais ; motifs :\n{motifs}",
        rapport.gate
    );
}

#[test]
fn mutant_sg4_locution_interdite_dans_le_harnais() {
    let racine = arbre_documentaire("sg4-harnais");
    ajouter(
        &racine,
        "s2-harness/README.md",
        "\nCette donnée vérifiée fonde le verdict du harnais.\n",
    );
    let rapports = gates_documentaires(&racine);
    exiger_rouge_dans_le_harnais(rapport_de(&rapports, "S-G4"), "« donnée vérifiée »");
}

#[test]
fn mutant_sg5_citation_hors_corpus_dans_le_harnais() {
    let racine = arbre_documentaire("sg5-harnais");
    ajouter(
        &racine,
        "s2-harness/README.md",
        "\nUne citation forgée : « this sentence is not in the corpus and it\nmust be caught in the harness ».\n",
    );
    let rapports = gates_documentaires(&racine);
    exiger_rouge_dans_le_harnais(rapport_de(&rapports, "S-G5"), "citation introuvable");
}

/// Le refus sur répertoire absent tient pour le chemin neuf : supprimer
/// `s2-harness/` ne fait pas disparaître sa couverture, il rend les deux
/// gates ROUGES (même doctrine que `mutant_couverture_repertoire_de_role_supprime`).
#[test]
fn mutant_couverture_harnais_supprime() {
    let racine = arbre_documentaire("couverture-harnais");
    std::fs::remove_dir_all(racine.join("s2-harness")).expect("suppression du harnais synthétique");
    let rapports = gates_documentaires(&racine);
    for gate in ["S-G4", "S-G5"] {
        exiger_rouge(
            rapport_de(&rapports, gate),
            "répertoire absent ou illisible : s2-harness",
        );
    }
}

#[test]
fn mutant_sg6_artefact_verse_sans_entree_de_registre() {
    let racine = arbre_documentaire("sg6-non-enregistre");
    ecrire(
        &racine,
        "biblio/artefact-c.txt",
        "octets versés sans entrée\n",
    );
    let rapports = gates_documentaires(&racine);
    exiger_rouge(rapport_de(&rapports, "S-G6"), "absent du registre");
}

#[test]
fn mutant_sg6_compte_declare_en_derive() {
    // La dérive courante : un versement sans remise à jour de l'en-tête —
    // le compte déclaré est INFÉRIEUR au réel. (La direction inverse,
    // déclaré > réel avec tous les présents mentionnés, est le régime
    // « corpus partiel » : note imprimée, résidu nommé dans sg6.rs — c'est
    // le témoin `temoin_sg6_corpus_partiel…` qui la fige.)
    let racine = arbre_documentaire("sg6-compte");
    remplacer(
        &racine,
        "biblio/INDEX.md",
        "**2 artefacts détenus**",
        "**1 artefacts détenus**",
    );
    let rapports = gates_documentaires(&racine);
    exiger_rouge(rapport_de(&rapports, "S-G6"), "compte déclaré en tête (1)");
}

#[test]
fn mutant_sg8_ordre_chronologique_rompu() {
    let racine = arbre_documentaire("sg8-ordre");
    ajouter(
        &racine,
        "JOURNAL.md",
        "| 2026-08-10 | unité insérée au mauvais endroit | rendue |\n",
    );
    let rapports = gates_documentaires(&racine);
    exiger_rouge(rapport_de(&rapports, "S-G8"), "ordre chronologique rompu");
}

#[test]
fn mutant_sg8_ligne_de_journal_malformee() {
    let racine = arbre_documentaire("sg8-malforme");
    ajouter(
        &racine,
        "JOURNAL.md",
        "| 2026-08-12 | cellule manquante |\n",
    );
    let rapports = gates_documentaires(&racine);
    exiger_rouge(rapport_de(&rapports, "S-G8"), "malformée");
}

/// Témoins du régime « corpus partiel » (revue G2 du 2026-08-13, majeure 4) :
/// la branche qui transforme les violations en notes est celle qui porte la
/// promesse « un contrôle partiel qui se dit partiel » — elle se teste comme
/// le reste, sinon le vert de CI repose sur du code hors registre d'assurance.
fn arbre_documentaire_sans_octets(nom_du_cas: &str) -> Arbre {
    let racine = arbre_documentaire(nom_du_cas);
    std::fs::remove_file(racine.join("biblio/artefact-a.html")).expect("suppression artefact a");
    std::fs::remove_file(racine.join("biblio/artefact-b.txt")).expect("suppression artefact b");
    racine
}

#[test]
fn temoin_sg5_corpus_incomplet_dit_partiel_et_liste_les_non_controles() {
    let racine = arbre_documentaire_sans_octets("sg5-partiel");
    ajouter(
        &racine,
        "docs/note.md",
        "\nUne citation forgée : « this quotation is not anywhere in the corpus\nand the gate must catch it ».\n",
    );
    let rapport = xtask::sg5::executer(&racine);
    rapport.imprimer();
    assert!(
        rapport.vert(),
        "en corpus incomplet, l'introuvable est une note, pas une violation :\n{}",
        motifs(&rapport)
    );
    let notes = rapport.notes.join("\n");
    assert!(
        notes.contains("CORPUS INCOMPLET"),
        "la note de régime partiel doit s'imprimer ; notes :\n{notes}"
    );
    assert!(
        notes.contains("this quotation is not anywhere in the corpus"),
        "chaque fragment non contrôlé doit être listé nommément ; notes :\n{notes}"
    );
}

#[test]
fn temoin_sg6_corpus_partiel_dit_partiel_sans_vert_muet() {
    let racine = arbre_documentaire_sans_octets("sg6-partiel");
    let rapport = xtask::sg6::executer(&racine);
    rapport.imprimer();
    assert!(
        rapport.vert(),
        "biblio/ sans octets = régime partiel, pas une violation :\n{}",
        motifs(&rapport)
    );
    let notes = rapport.notes.join("\n");
    assert!(
        notes.contains("compte déclaré 2") && notes.contains("non contrôlable"),
        "la note doit nommer le compte déclaré et le contrôle non tenu ; notes :\n{notes}"
    );
}

#[test]
fn mutant_sg4_guillemet_ascii_orphelin_ne_blanchit_rien_et_se_dit() {
    let racine = arbre_documentaire("sg4-ascii-orphelin");
    ajouter(
        &racine,
        "docs/note.md",
        "\nIl a dit \"bonjour, et cette donnée vérifiée fonde le verdict \"selon nous\".\n",
    );
    let rapport = xtask::sg4::executer(&racine);
    rapport.imprimer();
    assert!(!rapport.vert(), "S-G4 devait être ROUGE");
    let motifs = motifs(&rapport);
    assert!(
        motifs.contains("donnée vérifiée"),
        "la locution ne doit pas être cachée par l'appariement glouton ; motifs :\n{motifs}"
    );
    assert!(
        motifs.contains("orphelin"),
        "le guillemet ASCII orphelin doit être un incident ; motifs :\n{motifs}"
    );
}

#[test]
fn mutant_sg6_sous_repertoire_dans_biblio() {
    let racine = arbre_documentaire("sg6-sous-repertoire");
    ecrire(
        &racine,
        "biblio/sous-dossier/y.txt",
        "octets déplacés hors du plat\n",
    );
    let rapport = xtask::sg6::executer(&racine);
    rapport.imprimer();
    assert!(!rapport.vert(), "S-G6 devait être ROUGE");
    assert!(
        motifs(&rapport).contains("sous-répertoire inattendu"),
        "le sous-répertoire doit être un incident, pas un ensemble invisible ; motifs :\n{}",
        motifs(&rapport)
    );
}

#[test]
fn mutant_sg8_ligne_de_table_entierement_vide() {
    let racine = arbre_documentaire("sg8-vide");
    ajouter(&racine, "JOURNAL.md", "|  |  |  |\n");
    let rapports = gates_documentaires(&racine);
    exiger_rouge(rapport_de(&rapports, "S-G8"), "malformée");
}

// ---------------------------------------------------------------------------
// S-G5 et emplacements interdits (lot SG5-INTERDITS, 2026-10-04 ; SHOGEN-SG5-NOTES-INTERDITS-1,
// ADR-0028 annexe B.51) : une citation introuvable située dans un emplacement interdit ne
// s'imprime que par `chemin:ligne`, jamais par son texte, et le verdict ne change pas. La sortie
// contrôlée est celle du binaire (`xtask gates`), pas un champ du rapport. Les six emplacements
// sont recopiés de la liste des briefs, indépendamment du code ; le septième, `docs/adr-0028/execution/`,
// ajouté par DETTES-T4 (DT4-b, adjudication Q-3 : liste des briefs de ce lot).
// ---------------------------------------------------------------------------

const FACTICES_INTERDITS: [&str; 7] = [
    "docs/15-factice.md",
    "docs/16-factice.md",
    "docs/pocket-report/factice.md",
    "docs/rapports/factice.md",
    "docs/adr-0025/factice.md",
    "docs/adr-0028/monark-m009a/factice.md",
    "docs/adr-0028/execution/factice.md",
];

/// Écrit, ligne 3 de `relatif`, une citation anglaise introuvable au corpus, portant `marque`.
fn citation_factice(racine: &Path, relatif: &str, marque: &str) {
    let texte = format!(
        "# fixture factice\n\nUne citation : « the {marque} sentence of this file is not in the corpus ».\n"
    );
    ecrire(racine, relatif, &texte);
}

/// L'arbre augmenté des sept fixtures interdites, marquées `zorglub0` à `zorglub6`.
fn avec_factices_interdits(racine: Arbre) -> Arbre {
    for (rang, relatif) in FACTICES_INTERDITS.iter().enumerate() {
        citation_factice(&racine, relatif, &format!("zorglub{rang}"));
    }
    racine
}

/// Sortie du binaire (stdout puis stderr) : `xtask gates`, lexical, sans sous-processus cargo.
fn sortie_du_binaire(racine: &Path) -> String {
    ecrire(racine, "Cargo.toml", "[workspace]\n");
    let sortie = std::process::Command::new(env!("CARGO_BIN_EXE_xtask"))
        .arg("gates")
        .current_dir(racine)
        .output()
        .expect("lancement du binaire xtask");
    // Rouge global attendu (arbre sans rôles) : toute autre sortie est un lancement manqué.
    assert_eq!(
        sortie.status.code(),
        Some(1),
        "binaire : {:?}",
        sortie.status
    );
    let (stdout, stderr) = (&sortie.stdout, &sortie.stderr);
    format!(
        "{}{}",
        String::from_utf8_lossy(stdout),
        String::from_utf8_lossy(stderr)
    )
}

/// Exige : S-G5 imprimée, aucune marque `zorglub` (le texte), chaque fixture en `chemin:3`.
fn exiger_chemin_ligne_sans_texte(sortie: &str, avant: &str, apres: &str) {
    assert!(sortie.contains("--- S-G5"), "S-G5 absente :\n{sortie}");
    assert!(
        !sortie.contains("zorglub"),
        "texte d'une citation en emplacement interdit imprimé :\n{sortie}"
    );
    for relatif in FACTICES_INTERDITS {
        let attendu = format!("{avant}{relatif}:3{apres}");
        assert!(
            sortie.contains(&attendu),
            "« {attendu} » absent :\n{sortie}"
        );
    }
}

const NOTE_MASQUES: &str = "fragment(s) introuvable(s) rapporté(s) par chemin:ligne seul";

#[test]
fn mutant_sg5_interdits_complet_chemin_ligne_sans_texte() {
    let racine = avec_factices_interdits(arbre_documentaire("sg5-interdits-complet"));
    // Une citation trouvée au corpus, en emplacement interdit : ni violation, ni masque.
    ajouter(
        &racine,
        "docs/rapports/factice.md",
        "\n« this quotation is present in the corpus and it is checked by the gate ».\n",
    );
    // Verdict inchangé : ROUGE, sept violations, une par fixture, ligne 3.
    let rapport = xtask::sg5::executer(&racine);
    let motifs = motifs(&rapport);
    assert_eq!(
        rapport.violations.len(),
        7,
        "sept violations attendues :\n{motifs}"
    );
    for relatif in FACTICES_INTERDITS {
        let attendu = format!("{relatif}:3 citation introuvable");
        assert!(
            motifs.contains(&attendu),
            "« {attendu} » absent :\n{motifs}"
        );
    }
    exiger_chemin_ligne_sans_texte(&sortie_du_binaire(&racine), "VIOLATION ", " — ");
    let notes = rapport.notes.join("\n");
    assert!(notes.contains(&format!(": 7 {NOTE_MASQUES}")), "{notes}");
}

#[test]
fn mutant_sg5_interdits_incomplet_chemin_ligne_sans_texte() {
    let racine = avec_factices_interdits(arbre_documentaire_sans_octets("sg5-interdits-partiel"));
    // Verdict inchangé : VERT, neuf fragments non contrôlés (deux de l'arbre, sept factices).
    let rapport = xtask::sg5::executer(&racine);
    let notes = rapport.notes.join("\n");
    assert!(rapport.vert(), "VERT attendu :\n{}", motifs(&rapport));
    assert!(notes.contains(": 9 fragment(s) NON contrôlé(s)"), "{notes}");
    exiger_chemin_ligne_sans_texte(&sortie_du_binaire(&racine), "non contrôlé : ", "\n");
    assert!(notes.contains(&format!(": 7 {NOTE_MASQUES}")), "{notes}");
}

/// Témoin des bornes (préfixes exacts) : hors des sept emplacements, le texte reste imprimé.
#[test]
fn temoin_sg5_interdits_voisins_gardent_le_texte() {
    let racine = arbre_documentaire("sg5-interdits-voisins");
    let voisins = [
        "docs/150-voisin.md",
        "docs/160-voisin.md",
        "docs/rapports-publics/voisin.md",
        "docs/pocket-reportage/voisin.md",
        "docs/adr-00250/voisin.md",
        "docs/adr-0028/voisin.md",
        "docs/adr-0028/monark-m009ab/voisin.md",
        "docs/adr-0028/execution-bis/voisin.md",
        "docs/b.jsonlx/voisin.md",
        "s2-harness/docs/rapports/voisin.md",
    ];
    for relatif in voisins {
        citation_factice(&racine, relatif, "visible");
    }
    let rapport = xtask::sg5::executer(&racine);
    let motifs = motifs(&rapport);
    assert_eq!(rapport.violations.len(), voisins.len(), "{motifs}");
    for relatif in voisins {
        let attendu = format!(
            "{relatif}:3 citation introuvable dans le registre et les octets détenus : « the visible sentence of this file is not in the corpus »"
        );
        assert!(
            motifs.contains(&attendu),
            "« {attendu} » absent :\n{motifs}"
        );
    }
}

/// DT4-f (DETTES-T4, C-9 du contre-contrôle) : casse pliée (majuscules puis minuscules, `ſ` compris) et tout
/// composant en `.jsonl`, dossier compris : la citation se rapporte par `chemin:ligne` seul, verdict inchangé.
#[test]
fn mutant_sg5_interdits_casse_et_jsonl() {
    let racine = arbre_documentaire("sg5-interdits-casse");
    let factices = [
        "docs/Rapports/factice.md",
        "docs/adr-0028/EXECUTION/factice.md",
        "docs/rapport\u{17F}/factice.md",
        "docs/b.jsonl/factice.md",
        "docs/x/Y.JSONL/factice.md",
    ];
    for (rang, relatif) in factices.iter().enumerate() {
        citation_factice(&racine, relatif, &format!("zorglub{rang}"));
    }
    let rapport = xtask::sg5::executer(&racine);
    let motifs = motifs(&rapport);
    assert_eq!(rapport.violations.len(), factices.len(), "{motifs}");
    assert!(!motifs.contains("zorglub"), "texte imprimé :\n{motifs}");
    for relatif in factices {
        let attendu = format!(
            "{relatif}:3 citation introuvable dans le registre et les octets détenus (emplacement interdit"
        );
        assert!(
            motifs.contains(&attendu),
            "« {attendu} » absent :\n{motifs}"
        );
    }
}

// ---------------------------------------------------------------------------
// S-G5 et commentaires HTML (lot DETTES-T15 ; SHOGEN-SG5-COMMENTAIRE-HTML-1, adjudication de DETTES-T14, Q-6 (i)) : un
// commentaire `<!-- … -->` d'une page détenue n'est pas du texte affiché. Fixture minimale, de la forme de la page NIST
// §1.3.5.15 du 2026-10-09 (règle retirée de la section affichée, restée en commentaire, balises comprises), non copiée.
// ---------------------------------------------------------------------------

/// La phrase témoin de l'arbre documentaire, suivie de `suite` : une page détenue `biblio/artefact-a.html`.
fn page_detenue(suite: &str) -> String {
    format!("<p>this quotation is present in the corpus and it is checked by the gate</p>\n{suite}")
}

/// S-G5 sur l'arbre documentaire, `biblio/<artefact>` réécrit, docs/note.md augmenté de la citation « `citation` ».
fn sg5_page(cas: &str, artefact: &str, contenu: &str, citation: &str) -> Rapport {
    let racine = arbre_documentaire(cas);
    ecrire(&racine, &format!("biblio/{artefact}"), contenu);
    ajouter(
        &racine,
        "docs/note.md",
        &format!("\nUne citation : « {citation} ».\n"),
    );
    let rapport = xtask::sg5::executer(&racine);
    rapport.imprimer();
    rapport
}

const REGLE_RETIREE: &str = "the rule that is kept only in this comment is not shown to the reader";
const AFFICHEE: &str = "the sentence after the comment is shown to the reader and it is found";

/// La forme NIST : en-tête et paragraphe balisés dans le commentaire, premier `>` à moins de 300 octets de `<!--`.
fn commentaire_nist() -> String {
    let remplissage = "the padding of this section is long and it has no tag in it. ".repeat(6);
    format!(
        "<!-- <h3>Definition</h3>\n<p>{REGLE_RETIREE}.</p>\n<p>{remplissage}</p> -->\n<p>{AFFICHEE}.</p>\n"
    )
}

#[test]
fn mutant_sg5_commentaire_html_regle_retiree_de_la_page() {
    let page = page_detenue(&commentaire_nist());
    let rapport = sg5_page(
        "sg5-commentaire-nist",
        "artefact-a.html",
        &page,
        REGLE_RETIREE,
    );
    exiger_rouge(&rapport, "citation introuvable");
}

/// Commentaire de plus de 300 octets sans balise (le débalisage le gardait entier), en `.html`, `.htm` et `.md`.
#[test]
fn mutant_sg5_commentaire_html_long_sans_balise() {
    let long = format!(
        "<!-- {REGLE_RETIREE} ; {} -->\n",
        "and it has no tag. ".repeat(20)
    );
    let cas = [
        ("artefact-a.html", page_detenue(&long)),
        ("artefact-d.htm", long.clone()),
        ("artefact-c.md", long.clone()),
    ];
    for (artefact, contenu) in cas {
        let rapport = sg5_page(
            &format!("sg5-long-{artefact}"),
            artefact,
            &contenu,
            REGLE_RETIREE,
        );
        exiger_rouge(&rapport, "citation introuvable");
    }
}

/// Commentaire jamais fermé : le reste du fichier n'est pas affiché (tokenisation HTML, fin de fichier en commentaire).
#[test]
fn mutant_sg5_commentaire_html_jamais_ferme() {
    let ouvert = format!("<p>debut</p><!-- jamais ferme\n<p>{AFFICHEE}.</p>\n");
    let rapport = sg5_page(
        "sg5-commentaire-ouvert",
        "artefact-a.html",
        &page_detenue(&ouvert),
        AFFICHEE,
    );
    exiger_rouge(&rapport, "citation introuvable");
}

/// `<!---!>` ne ferme pas le commentaire (en HTML, `-!>` au début n'est pas une fin) : il court jusqu'à `-->`.
#[test]
fn mutant_sg5_commentaire_html_fausse_fermeture() {
    let page = format!("<!---!><p>{REGLE_RETIREE}.</p> -->\n<p>suite</p>\n");
    let rapport = sg5_page(
        "sg5-fausse-fermeture",
        "artefact-a.html",
        &page_detenue(&page),
        REGLE_RETIREE,
    );
    exiger_rouge(&rapport, "citation introuvable");
}

/// Le texte affiché reste au corpus : après un commentaire NIST, après `<!-->` et `<!--->` (commentaires vides, fermés
/// tout de suite), après `--!>` (fermeture admise par la tokenisation HTML) et après `<!-xy>`, qui n'est pas `<!--`.
#[test]
fn temoin_sg5_commentaire_html_texte_affiche_garde() {
    let pages = [
        commentaire_nist(),
        format!("<!--><p>{AFFICHEE}.</p>\n"),
        format!("<!---><p>{AFFICHEE}.</p>\n"),
        format!("<!-- x --!><p>{AFFICHEE}.</p>\n<!-- y -->\n"),
        format!("<!-xy><p>{AFFICHEE}.</p>\n<!-- z -->\n"),
    ];
    for (rang, page) in pages.iter().enumerate() {
        let rapport = sg5_page(
            &format!("sg5-affiche-{rang}"),
            "artefact-a.html",
            &page_detenue(page),
            AFFICHEE,
        );
        assert!(
            rapport.vert(),
            "page {rang} : texte affiché perdu :\n{}",
            motifs(&rapport)
        );
    }
}

/// Hors HTML (texte brut), `<!--` n'ouvre rien : la phrase d'un long « commentaire » de `.txt` reste au corpus.
#[test]
fn temoin_sg5_commentaire_hors_html_reste_au_corpus() {
    let texte = format!(
        "<!-- {REGLE_RETIREE} ; {} -->\n",
        "and it has no tag. ".repeat(20)
    );
    let rapport = sg5_page(
        "sg5-commentaire-txt",
        "artefact-b.txt",
        &texte,
        REGLE_RETIREE,
    );
    assert!(
        rapport.vert(),
        "texte brut retiré à tort :\n{}",
        motifs(&rapport)
    );
}

// S-G5, éléments script et style (lot DETTES-T15, DT15-g ; adjudication Q-5) : leur contenu n'est jamais affiché.
// Fermante selon la tokenisation HTML : casse ignorée, nom suivi d'un blanc, de `/` ou de `>` ; dans un script,
// `<!--` puis `<script` font ignorer la fermante suivante jusqu'à `-->`. Fixtures minimales, aucune page copiée.

/// S-G5 sur la page détenue `page_detenue(page)` qui cite « `citation` » : ROUGE exigé si `rouge`, VERT sinon.
fn sg5_page_rouge(cas: &str, page: &str, citation: &str, rouge: bool) {
    let rapport = sg5_page(cas, "artefact-a.html", &page_detenue(page), citation);
    if rouge {
        exiger_rouge(&rapport, "citation introuvable");
    } else {
        assert!(
            rapport.vert(),
            "{cas} : texte affiché perdu :\n{}",
            motifs(&rapport)
        );
    }
}

/// Un test par page : la page, la citation, ROUGE exigé ou non.
macro_rules! pages_sg5 {
    ($($nom:ident : $page:expr, $citation:expr => $rouge:expr),* $(,)?) => {
        $(#[test] fn $nom() { sg5_page_rouge(stringify!($nom), &$page, $citation, $rouge); })*
    };
}

pages_sg5! {
    mutant_sg5_script_contenu_ote:
        format!("<script>var r = \"{REGLE_RETIREE}\";</script><p>x</p>"), REGLE_RETIREE => true,
    mutant_sg5_style_contenu_ote:
        format!("<style>/* {REGLE_RETIREE} */ p {{ color: red }}</style>"), REGLE_RETIREE => true,
    mutant_sg5_script_casse_et_fermante_espacee:
        format!("<SCRIPT type=\"text/javascript\">\"{REGLE_RETIREE}\"</Script >"), REGLE_RETIREE => true,
    mutant_sg5_script_fermante_d_un_autre_nom:
        format!("<script>x</scripts>\"{REGLE_RETIREE}\"</script>"), REGLE_RETIREE => true,
    mutant_sg5_script_jamais_ferme: format!("<p>debut</p><script>{REGLE_RETIREE}\n<p>suite</p>"), REGLE_RETIREE => true,
    mutant_sg5_script_doublement_echappe:
        format!("<script><!-- w(\"<script>a</script>\"); {REGLE_RETIREE} --></script>"), REGLE_RETIREE => true,
    mutant_sg5_script_doublement_echappe_deux_fois: format!(
        "<script><!-- <script></script><script></script> {REGLE_RETIREE} --></script>"
    ), REGLE_RETIREE => true,
    temoin_sg5_script_ferme_texte_suivant_affiche: format!("<script>x</script><p>{AFFICHEE}.</p>"), AFFICHEE => false,
    temoin_sg5_element_scripts_n_est_pas_un_script: format!("<scripts>{AFFICHEE}.</scripts>"), AFFICHEE => false,
    temoin_sg5_style_ferme_texte_suivant_affiche: format!("<style>p {{}}</style><p>{AFFICHEE}.</p>"), AFFICHEE => false,
    temoin_sg5_script_double_echappe_rendu_aux_donnees:
        format!("<script><!-- <script> --></script><p>{AFFICHEE}.</p>"), AFFICHEE => false,
    temoin_sg5_script_commentaire_vide: format!("<script><!--><script></script><p>{AFFICHEE}.</p>"), AFFICHEE => false,
    temoin_sg5_script_dans_un_commentaire: format!("<!-- <script> --><p>{AFFICHEE}.</p>"), AFFICHEE => false,
    temoin_sg5_commentaire_texte_colle_garde: format!("<!-- x -->{AFFICHEE}."), AFFICHEE => false,
    temoin_sg5_commentaire_trois_tirets: format!("<!-- a ---><p>{AFFICHEE}.</p>"), AFFICHEE => false,
}

// S-G5, commentaires factices (lot DETTES-T15, DT15-h ; limite L-6 fermée) : `<!` sans `--`, `<?`, et `</` suivi d'un
// caractère qui n'est ni une lettre ni `>` ouvrent un commentaire factice, clos au premier `>`, sans borne de longueur.

pages_sg5! {
    mutant_sg5_commentaire_factice_long:
        format!("<!x {REGLE_RETIREE} ; {} ><p>x</p>", "and it has no tag. ".repeat(20)), REGLE_RETIREE => true,
    mutant_sg5_instruction_factice_longue:
        format!("<?x {REGLE_RETIREE} ; {} ?><p>x</p>", "and it has no tag. ".repeat(20)), REGLE_RETIREE => true,
    mutant_sg5_fermante_factice_longue:
        format!("</ {REGLE_RETIREE} ; {} ><p>x</p>", "and it has no tag. ".repeat(20)), REGLE_RETIREE => true,
    mutant_sg5_commentaire_factice_jamais_ferme: format!("<p>x</p><!x {REGLE_RETIREE}"), REGLE_RETIREE => true,
    mutant_sg5_fermante_factice_lettre_non_ascii:
        format!("</é {REGLE_RETIREE} ; {} ><p>x</p>", "and it has no tag. ".repeat(20)), REGLE_RETIREE => true,
    temoin_sg5_factices_clos_au_premier_chevron:
        format!("<!DOCTYPE html><?xml version=\"1\"?></ x><!x><p>{AFFICHEE}.</p><p>y</p>"), AFFICHEE => false,
}

// S-G5, balises de script et de style (lot DETTES-T15, DT15-j) : la balise ouvrante ou fermante d'un script ou d'un
// style se clôt à son `>` hors des valeurs d'attribut entre guillemets (tokenisation HTML) ; une fermante écrite dans
// une valeur d'attribut ne clôt rien, une valeur jamais refermée court jusqu'au bout du texte.

pages_sg5! {
    mutant_sg5_script_ouvrante_guillemets:
        format!(r#"<script data-x="a></script>">{REGLE_RETIREE}</script><p>x</p>"#), REGLE_RETIREE => true,
    mutant_sg5_style_ouvrante_apostrophes:
        format!(r#"<style title='a></style>'>{REGLE_RETIREE}</style><p>x</p>"#), REGLE_RETIREE => true,
    mutant_sg5_script_fermante_guillemets:
        format!(r#"<script>x</script data-x=">{REGLE_RETIREE}"><p>y</p>"#), REGLE_RETIREE => true,
    mutant_sg5_script_guillemets_apres_blancs:
        format!(r#"<script a = "b></script>">{REGLE_RETIREE}</script>"#), REGLE_RETIREE => true,
    mutant_sg5_script_guillemet_jamais_ferme:
        format!(r#"<script a="b></script><p>{REGLE_RETIREE}</p>"#), REGLE_RETIREE => true,
    mutant_sg5_script_valeur_nue_puis_guillemets:
        format!(r#"<script a=b c="d></script>">{REGLE_RETIREE}</script>"#), REGLE_RETIREE => true,
    mutant_sg5_script_barre_puis_guillemets:
        format!(r#"<script/a="b></script>">{REGLE_RETIREE}</script>"#), REGLE_RETIREE => true,
    temoin_sg5_script_guillemet_dans_un_nom: format!(r#"<script a"b>x</script><p>{AFFICHEE}.</p>"#), AFFICHEE => false,
    temoin_sg5_script_egal_avant_le_nom: format!(r#"<script ="b>x</script><p>{AFFICHEE}.</p>"#), AFFICHEE => false,
    temoin_sg5_script_guillemet_dans_une_valeur_nue:
        format!(r#"<script a=b"c>x</script><p>{AFFICHEE}.</p>"#), AFFICHEE => false,
    temoin_sg5_script_valeur_entre_guillemets_close:
        format!(r#"<script a="b>c">x</script><p>{AFFICHEE}.</p>"#), AFFICHEE => false,
    temoin_sg5_script_fermante_guillemets_texte_suivant:
        format!(r#"<script>x</script a=">"><p>{AFFICHEE}.</p>"#), AFFICHEE => false,
}

// ---------------------------------------------------------------------------
// S-G9 (lot DETTES-B2, 2026-10-04 ; SHOGEN-E1-XTASK-REFS-1, ADR-0028 annexe B.7) : contrôles (a) à (f) de
// l'oracle hors dépôt `verif_refs.py` du lot E1, sur un docs/17 synthétique et ses registres. Chaque mutant
// ajoute UNE forme fautive et exige le ROUGE pour son motif ; les survivants de la revue G2 d'E1 (résidu en
// majuscules, apostrophes, décimal, pour-cent en lettres, nom nu de D.2 n° 8) ont leur test, la borne des
// lots MONARK son témoin.
// ---------------------------------------------------------------------------

/// L'arbre synthétique : `@@@ chemin` ouvre un fichier, les lignes suivantes sont son contenu.
const ARBRE_MENACE: &str = "\
@@@ docs/17-modele-de-menace.md
# modèle de menace synthétique

Statut du 2026-10-04 ; lot T1 ; lots MONARK G2 et G7 ; PX-Shogen-1 ; FM-1.1, FM-3.3, §4.10, 1.97.1.
Code : `crates/exemple.rs:2-3`, `crates/LISEZMOI:1`, `biblio/source.pdf.sidecar:9`,
`F:/Monark@0123456789abcdef0123456789abcdef01234567:apps/x.ts:4`. Résidu A(exemple-residu) ;
item SHOGEN-EXEMPLE-1 ; la source dit « une phrase française de la source, citée telle quelle ».
Formes non fautives : SOMMA(x), A(…), items MONARK-SHOGEN-* transmis, lot G9, 3 maisons, « bref ».
L'acte d'E1 et l'avis des pairs' sont lus ; « this quotation is English and is not checked here ».

| T | a | b | c | contrôle | r | i |
|---|---|---|---|---|---|---|
| T-01 x | a | b | c | [hors chemin servi] `crates/exemple.rs:1` | r | i |
| T-02 x | a | b | c | [aucun contrôle] motif écrit | r | i |
@@@ docs/08-assumptions.md
| A(exemple-residu) | énoncé |
@@@ docs/adr-0028/ANNEXE-A-lots.md
| **T1** (2026-10-04) | objet ; consommateur : docs/11 (lot G9) |
@@@ docs/adr-0028/ANNEXE-B-items.md
| SHOGEN-EXEMPLE-1 | objet | SHOGEN-MENTION-1 |
| 9 | ligne sans identifiant en tête | SHOGEN-MENTION-2 |
@@@ docs/RENVOIS-LIGNES.tsv
# registre synthétique des renvois (une ligne de commentaire)
renvoi\tjeton\tcible\tecrit\tlignes\tempreinte\tcommit
docs/17-modele-de-menace.md:4\tcrates/exemple.rs:2-3\tcrates/exemple.rs\t2-3\t2-3\t849ab6324f790f2f\t0000000
docs/17-modele-de-menace.md:4\tcrates/LISEZMOI:1\tcrates/LISEZMOI\t1\t1\t38e9b1de50176b4a\t0000000
docs/17-modele-de-menace.md:12\tcrates/exemple.rs:1\tcrates/exemple.rs\t1\t1\t4bb546d3a6668da1\t0000000
docs/adr-0028/PAQUET-PREREG-S2.md:1\texemple.rs l.2\tcrates/exemple.rs\t2\t2\t27fbd56e8c6236bc\t8b14567
docs/journal.md:1\texemple.rs l.3\tcrates/exemple.rs\t3\t3\tbe9b4817a9d4792f\t0000000
docs/journal.md:2\tancien.rs l.7\tcrates/ancien.rs\t7\t-\t03744d41bdab3b8d\tabcdef0
@@@ docs/journal.md
Lu : exemple.rs l.3 (dernière ligne).
Lu aussi : ancien.rs l.7 (fichier retiré depuis).
@@@ docs/adr-0028/PAQUET-PREREG-S2.md
Repère : exemple.rs l.2 (lu au commit de scellement).
@@@ docs/source.md
Selon lui, une phrase française de la source, citée telle quelle, fait foi.
@@@ crates/exemple.rs
ligne 1
ligne 2
ligne 3
@@@ crates/LISEZMOI
fichier sans extension
";

fn arbre_menace(nom_du_cas: &str) -> Arbre {
    let racine = Arbre::nouveau("shogen-mutant-sg9", nom_du_cas);
    for bloc in ARBRE_MENACE.split("@@@ ").skip(1) {
        let (relatif, contenu) = bloc.split_once('\n').expect("bloc : chemin puis contenu");
        ecrire(&racine, relatif, contenu);
    }
    racine
}

/// S-G9 sur l'arbre synthétique augmenté de `ajout` : VERT exigé, couverture pleine ; rend les notes.
fn notes_sg9_vert(cas: &str, ajout: &str) -> String {
    let racine = arbre_menace(cas);
    ajouter(&racine, xtask::sg9::PERIMETRE, ajout);
    let rapport = xtask::sg9::executer(&racine);
    rapport.imprimer();
    assert!(rapport.vert(), "VERT attendu :\n{}", motifs(&rapport));
    assert_eq!((rapport.examines, rapport.presents), (5, 5), "couverture");
    rapport.notes.join("\n")
}

#[test]
fn temoin_sg9_arbre_menace_intact_est_vert() {
    let notes = notes_sg9_vert("temoin", "");
    assert!(
        notes.contains("biblio/ sans octets, non contrôlée(s) ici (DEVOPS §1) : [biblio/source"),
        "borne biblio/ :\n{notes}"
    );
}

/// Bornes de (c) (revue G2 d'E1, C-G2-6) : un lot MONARK ou un PX n'est pas résolu ici, il est LISTÉ ;
/// (g) et (h) de l'oracle, non mécanisés, sont déclarés (revue G2 de DETTES-B2, C-4).
#[test]
fn temoin_sg9_bornes_monark_et_px_listees() {
    let notes = notes_sg9_vert("bornes", "\nlots MONARK G2, G99 et G8 ; PX-Shogen-99.\n");
    let listes = [
        "lots MONARK : [G2, G7, G99, G8]",
        "PX : [PX-Shogen-1, PX-Shogen-99]",
        "(g) formes proscrites et (h) structure des tables S et T",
    ];
    assert!(
        listes.iter().all(|l| notes.contains(l)),
        "bornes :\n{notes}"
    );
}

#[test]
fn mutant_couverture_sg9_perimetre_absent() {
    let racine = arbre_menace("perimetre-absent");
    std::fs::remove_file(racine.join(xtask::sg9::PERIMETRE)).expect("suppression de docs/17");
    exiger_rouge(&xtask::sg9::executer(&racine), "fichier absent : docs/17");
}

/// Borne `biblio/` (revue G2 de DETTES-B2, C-1) : posée sans octets `biblio/` seulement (prédicat de
/// S-G6) ; `biblio/` peuplée, une référence pendante est introuvable, une plage hors du fichier refusée.
fn exiger_rouge_sg9_biblio(cas: &str, sidecar: Option<&str>, attendu: &str) {
    let racine = arbre_menace(cas);
    ecrire(&racine, "biblio/factice.pdf", "octets versés");
    if let Some(contenu) = sidecar {
        ecrire(&racine, "biblio/source.pdf.sidecar", contenu);
    }
    exiger_rouge(&xtask::sg9::executer(&racine), attendu);
}

#[test]
fn mutant_sg9_a_biblio_peuplee_reference_pendante() {
    exiger_rouge_sg9_biblio("biblio-pendante", None, "fichier introuvable");
}

#[test]
fn mutant_sg9_a_biblio_peuplee_plage_hors_du_fichier() {
    exiger_rouge_sg9_biblio("biblio-plage", Some("1\n2\n3\n"), "plage hors du fichier");
}

/// Sans octet versé (`INDEX.md` et sidecars seuls, extension en toute casse), la borne tient.
#[test]
fn temoin_sg9_biblio_sidecars_seuls_sans_octets() {
    let racine = arbre_menace("biblio-sidecars");
    ecrire(&racine, "biblio/INDEX.md", "registre\n");
    ecrire(&racine, "biblio/autre.PDF.SIDECAR", "texte extrait\n");
    let rapport = xtask::sg9::executer(&racine);
    let notes = rapport.notes.join("\n");
    assert!(
        rapport.vert() && notes.contains("sans octets"),
        "{}",
        motifs(&rapport)
    );
}

fn exiger_rouge_sg9(cas: &str, fragment: &str, attendu: &str) {
    let racine = arbre_menace(cas);
    ajouter(&racine, xtask::sg9::PERIMETRE, fragment);
    exiger_rouge(&xtask::sg9::executer(&racine), attendu);
}

/// Un test par mutant : une seule forme fautive ajoutée à docs/17, un seul motif exigé.
macro_rules! mutants_sg9 {
    ($($nom:ident : $fragment:expr => $attendu:expr),* $(,)?) => {
        $(#[test] fn $nom() { exiger_rouge_sg9(stringify!($nom), $fragment, $attendu); })*
    };
}

mutants_sg9! {
    mutant_sg9_a_plage_hors_du_fichier: "\nVoir `crates/exemple.rs:3-4`.\n" => "plage hors du fichier",
    mutant_sg9_a_fichier_inexistant: "\nVoir `crates/absent.rs:1`.\n" => "fichier introuvable",
    mutant_sg9_a_reference_courte: "\nVoir `exemple.rs:2`.\n" => "fichier introuvable",
    mutant_sg9_a_chemin_absolu: "\nVoir `/crates/exemple.rs:2`.\n" => "chemin absolu ou non canonique",
    mutant_sg9_a_segment_parent: "\nVoir `crates/../crates/exemple.rs:2`.\n" => "chemin absolu ou non canonique",
    mutant_sg9_a_sans_extension_introuvable: "\nVoir `crates/LISEZ:1`.\n" => "fichier introuvable",
    mutant_sg9_a_monark_sans_sha: "\nVoir `F:/Monark:apps/x.ts:4`.\n" => "référence MONARK sans sha",
    mutant_sg9_a_monark_sha_court: "\nVoir `F:/Monark@0123abcd:apps/x.ts:4`.\n" => "référence MONARK sans sha",
    mutant_sg9_a_chemin_lecteur: "\nVoir `F:/tmp/x.md:3`.\n" => "chemin absolu ou non canonique",
    mutant_sg9_a_plage_inversee: "\nVoir `crates/exemple.rs:3-2`.\n" => "plage hors du fichier",
    mutant_sg9_a_ligne_zero: "\nVoir `crates/exemple.rs:0`.\n" => "plage hors du fichier",
    mutant_sg9_a_cellule_de_controle: "| T-03 x | a | b | c | [hors chemin servi] rien | r | i |\n" => "cellule de contrôle",
    mutant_sg9_a_aucun_controle_sans_motif: "| T-03 x | a | b | c | [aucun contrôle] | r | i |\n" => "cellule de contrôle",
    mutant_sg9_b_residu_invente: "\nRésidu A(residu-invente).\n" => "résidu non défini",
    mutant_sg9_b_residu_en_majuscules: "\nRésidu A(EXEMPLE-RESIDU).\n" => "résidu non défini",
    mutant_sg9_c_item_inexistant: "\nItem SHOGEN-INEXISTANT-9.\n" => "item non défini",
    mutant_sg9_c_item_mentionne_non_defini: "\nItem SHOGEN-MENTION-1.\n" => "item non défini",
    mutant_sg9_c_item_en_troisieme_cellule: "\nItem SHOGEN-MENTION-2.\n" => "item non défini",
    mutant_sg9_c_lot_absent: "\nVoir le lot ZZ9.\n" => "lot absent de l'annexe A",
    mutant_sg9_d_jj_mm_aaaa: "\nLe 30/09/2026.\n" => "date hors forme ISO",
    mutant_sg9_d_point_final: "\nLe 30.09.2026.\n" => "date hors forme ISO",
    mutant_sg9_d_aaaa_mm_jj_barres: "\nLe 2026/09/30.\n" => "date hors forme ISO",
    mutant_sg9_d_aaaa_m_j: "\nLe 2026-9-30.\n" => "date hors forme ISO",
    mutant_sg9_d_jj_mm_aaaa_tirets: "\nLe 30-09-2026.\n" => "date hors forme ISO",
    mutant_sg9_d_aaaa_mm_jj_points: "\nLe 2026.09.30.\n" => "date hors forme ISO",
    mutant_sg9_d_jour_et_mois: "\nLe 1er mars.\n" => "date hors forme ISO",
    mutant_sg9_d_mois_et_annee: "\nEn septembre 2026.\n" => "date hors forme ISO",
    mutant_sg9_e_guillemets_droits: "\nIl est écrit \"the verifier is never wrong about it\".\n" => "guillemet droit",
    mutant_sg9_e_apostrophes: "\nIl est écrit 'the verifier is never wrong about it'.\n" => "citation entre apostrophes",
    mutant_sg9_e_francaise_introuvable: "\nIl dit « une phrase qui ne figure dans aucun document ».\n" => "citation française introuvable",
    mutant_sg9_e_guillemet_orphelin: "\nIl dit « une phrase jamais refermée.\n" => "jamais refermé",
    mutant_sg9_f_chemin_de_d2: "\nVoir `F:/tmp/shogen-carto-2026-09-29/campagne.md`.\n" => "pièce de D.2",
    mutant_sg9_f_nom_nu_de_d2_n8: "\nVoir J0-STATUS.txt.\n" => "pièce de D.2",
    mutant_sg9_f_pour_cent_signe: "\nUn taux de 12 %.\n" => "pour-cent",
    mutant_sg9_f_pour_cent_en_lettres: "\nUn taux de douze pour cent.\n" => "pour-cent",
    mutant_sg9_f_nombre_decimal: "\nUn taux de 0,013.\n" => "nombre décimal",
    mutant_sg9_f_valeur_statistique: "\nOn mesure z = 3 sur la strate.\n" => "valeur statistique",
    mutant_sg9_f_ipv4: "\nHôte 192.0.2.1 contacté.\n" => "adresse IP",
    mutant_sg9_f_ipv6: "\nHôte 2001:db8::1 contacté.\n" => "adresse IP",
    mutant_sg9_f_adresse_electronique: "\nÉcrire à quelqu.un@example.org.\n" => "adresse électronique",
}

// S-G9 (a), registre des renvois (lot DETTES-T15 ; SHOGEN-REFS-LIGNE-CONTENU-1, adjudication de DETTES-T14, Q-6 (ii)) :
// une référence désigne encore le texte qu'elle citait. Empreintes de l'arbre synthétique calculées hors du code
// (`sha256sum`, 16 premiers chiffres) : « ligne 2⏎ligne 3 » 849ab632…, « fichier sans extension » 38e9b1de…,
// « ligne 1 » 4bb546d3…, « ligne 2 » 27fbd56e…, « ligne 3 » be9b4817….

/// S-G9 sur l'arbre synthétique où `fichier` a vu `avant` remplacé par `apres` : ROUGE exigé, pour `attendu`.
fn exiger_rouge_sg9_remplace(cas: &str, fichier: &str, avant: &str, apres: &str, attendu: &str) {
    let racine = arbre_menace(cas);
    remplacer(&racine, fichier, avant, apres);
    exiger_rouge(&xtask::sg9::executer(&racine), attendu);
}

/// Un test par mutant : un seul remplacement dans un fichier de l'arbre, un seul motif exigé.
macro_rules! mutants_registre {
    ($($nom:ident : $fichier:expr, $avant:expr, $apres:expr => $attendu:expr),* $(,)?) => {
        $(#[test] fn $nom() { exiger_rouge_sg9_remplace(stringify!($nom), $fichier, $avant, $apres, $attendu); })*
    };
}

const R: &str = "docs/RENVOIS-LIGNES.tsv";
const EXEMPLE: &str = "crates/exemple.rs";

mutants_registre! {
    mutant_sg9_a_insertion_au_milieu_du_fichier_cite:
        EXEMPLE, "ligne 1\n", "ligne 1\nligne 1 bis\n" => "texte cité changé ou déplacé",
    mutant_sg9_a_ligne_citee_reecrite_sur_place: EXEMPLE, "ligne 2", "ligne deux" => "texte cité changé ou déplacé",
    mutant_sg9_registre_jeton_hors_de_sa_ligne: R, "docs/journal.md:1\t", "docs/journal.md:2\t" => "jeton absent",
    mutant_sg9_registre_numero_absent_du_jeton: R, "\t3\t3\tbe9b", "\t13\t3\tbe9b" => "jeton absent",
    mutant_sg9_registre_empreinte_hors_forme: R, "be9b4817a9d4792f", "be9b4817a9d4792" => "hors forme",
    mutant_sg9_registre_colonne_manquante: R, "\t-\t03744d41bdab3b8d", "\t03744d41bdab3b8d" => "hors forme",
    mutant_sg9_registre_entete: R, "renvoi\tjeton", "renvois\tjeton" => "hors forme",
    mutant_sg9_registre_lignes_hors_du_fichier:
        R, "\t3\t3\tbe9b", "\t3\t4\tbe9b" => "lignes actuelles hors du fichier",
    mutant_sg9_registre_ligne_zero: R, "\t3\t3\tbe9b", "\t3\t0\tbe9b" => "hors forme",
    mutant_sg9_registre_fin_de_plage_seule: R, "\t2-3\t2-3\t", "\t3\t2-3\t" => "jeton absent",
    mutant_sg9_registre_debut_de_plage_seul: R, "\t2-3\t2-3\t", "\t2\t2-3\t" => "jeton absent",
    mutant_sg9_registre_commit_court: R, "\tabcdef0\n", "\tabc\n" => "hors forme",
    mutant_sg9_registre_scelle_hors_de_son_commit: R, "\t8b14567\n", "\t0000000\n" => "document scellé",
    mutant_sg9_registre_entree_orpheline: R, ":12\tcrates/exemple.rs:1", ":12\texemple.rs:1" => "sans référence (a)",
    mutant_sg9_registre_en_double: R, "\tabcdef0\n",
        "\tabcdef0\ndocs/journal.md:2\tancien.rs l.7\tcrates/ancien.rs\t7\t-\t03744d41bdab3b8d\tabcdef0\n"
        => "en double",
}

#[test]
fn mutant_sg9_a_reference_sans_entree_au_registre() {
    exiger_rouge_sg9(
        "sans-entree",
        "\nVoir `crates/exemple.rs:3`.\n",
        "sans entrée au registre des renvois",
    );
}

#[test]
fn mutant_couverture_sg9_registre_des_renvois_absent() {
    let racine = arbre_menace("registre-absent");
    std::fs::remove_file(racine.join(R)).expect("suppression du registre");
    exiger_rouge(
        &xtask::sg9::executer(&racine),
        "fichier absent : docs/RENVOIS-LIGNES.tsv",
    );
}

/// Témoin : sans octets versés ni emplacement interdit, l'entrée épinglée est listée ; `biblio/` peuplée, la référence
/// à un sidecar (octets non versionnés) et celle d'un emplacement interdit n'ont pas d'entrée et sont listées.
#[test]
fn temoin_sg9_registre_epinglees_et_bornes_listees() {
    let notes = notes_sg9_vert("registre-temoin", "");
    assert!(
        notes.contains("6 entrée(s), 5 texte(s) cité(s) retrouvé(s)"),
        "{notes}"
    );
    assert!(
        notes.contains("1 épinglée(s) à leur commit") && notes.contains("[docs/journal.md:2]"),
        "{notes}"
    );
    let racine = arbre_menace("registre-bornes");
    ecrire(&racine, "biblio/source.pdf.sidecar", &"x\n".repeat(9));
    ecrire(&racine, "docs/rapports/factice.md", "ligne\n");
    ajouter(
        &racine,
        xtask::sg9::PERIMETRE,
        "\nVoir `docs/rapports/factice.md:1`.\n",
    );
    let rapport = xtask::sg9::executer(&racine);
    let notes = rapport.notes.join("\n");
    assert!(rapport.vert(), "{}", motifs(&rapport));
    let bornes = "plage seule) : [biblio/source.pdf.sidecar:9, docs/rapports/factice.md:1]";
    assert!(notes.contains(bornes), "{notes}");
}

/// Une même référence deux fois sur une ligne de docs/17 : une seule entrée la couvre.
#[test]
fn temoin_sg9_registre_reference_double_sur_une_ligne() {
    let racine = arbre_menace("registre-double");
    ajouter(
        &racine,
        xtask::sg9::PERIMETRE,
        "\nVoir `crates/exemple.rs:1` et `crates/exemple.rs:1`.\n",
    );
    let entree = "docs/17-modele-de-menace.md:15\tcrates/exemple.rs:1\tcrates/exemple.rs\t1\t1\t4bb546d3a6668da1";
    ajouter(&racine, R, &format!("{entree}\t0000000\n"));
    let rapport = xtask::sg9::executer(&racine);
    assert!(rapport.vert(), "{}", motifs(&rapport));
}
