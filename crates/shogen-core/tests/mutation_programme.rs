//! Les cas nés du **score de mutation de programme** — ADR-0011 seuil 3.
//!
//! Rattachement (G0) : ADR-0011 point 3 (« *mutant de programme* — un opérateur
//! de mutation appliqué à `shogen-core`. C'est le seul des trois qui produit un
//! **score** ») et seuil 3 (« chaque survivant justifié nommément en une ligne »).
//!
//! # Ce que ce fichier est
//!
//! La première mesure du score de mutation du cœur a été faite le 2026-08-13
//! (`cargo-mutants` 27.1.0, 417 mutants générés) et a laissé **34 survivants**
//! (351 tués, 32 non viables — trace : rapport du chantier G, JOURNAL du
//! 2026-08-13). Cette première mesure était NON REJOUABLE (course du
//! répertoire temporaire à chemin fixe, corrigée le même jour) : ses comptes
//! ne se réconcilient donc pas arithmétiquement avec l'état re-mesuré de
//! `survivants.txt` (22 lignes) — la population a bougé entre les mesures.
//! Chacun des 34 a été trié à la main. Ceux qui sont **tuables** le sont ici :
//! chaque test nomme le mutant qu'il tue et le fait qui le tue. Ceux qui sont
//! **équivalents** — aucune entrée du programme ne les distingue — sont
//! justifiés en une ligne dans `crates/shogen-core/survivants.txt`, avec leur
//! démonstration.
//!
//! C'est la forme que la doctrine du dépôt donne déjà au mutant semé de gate,
//! transposée au mutant de programme : « l'évasion devient un test »
//! (DEVOPS §3). Ici l'évasion n'est pas un attaquant, c'est un opérateur de
//! mutation qui a montré un trou de la suite — et le trou se bouche avec un
//! test, jamais avec un abaissement de seuil.
//!
//! # Ce que ce fichier n'est pas
//!
//! Une preuve. Le coupling effect est déclaré empirique par ses auteurs
//! (DeMillo, Lipton & Sayward p. 35) : tuer un mutant ne dit rien des fautes
//! réelles. On écrit « suite *tested* : N mutants, M tués, K survivants
//! justifiés, [date] », jamais « la suite détecte les fautes »
//! (09-vocabulaire).

mod commun;

use shogen_core::{
    Attestor, ErreurDecodage, ErreurSubject, ObservedAt, Temoignage, TemoignageTrivial, Utterance,
    decoder_temoignage, decoder_temoignage_canonique, empreinte_sha256, encoder_temoignage,
    encoder_temoignage_canonique, subject_est_canonique, verifier_temoignage,
};

/// Le témoignage trivial de référence — le même que `cargo xtask
/// emettre-exemple`, recopié ici pour que ce fichier soit lisible seul.
fn trivial() -> TemoignageTrivial {
    TemoignageTrivial {
        source: String::from("exemple:source-factice"),
        instant: 1_754_000_000,
        contenu: b"lot d'exemple du walking skeleton".to_vec(),
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Mutants tués : `Lecteur::position -> 0`, `Lecteur::position -> 1`,
//                `Lecteur::restants -> 1`  (crates/shogen-core/src/cbor.rs)
//
// Ces trois accesseurs n'alimentent QUE des champs d'erreur nommée. La suite
// asserait jusqu'ici l'existence du refus, jamais ses coordonnées — donc un
// accesseur qui aurait menti sur la position aurait passé la revue et les
// tests. C'est exactement ce qu'un refus « diagnosticable sans journal »
// (`erreur.rs`, en-tête) promet et que rien ne vérifiait.
// ─────────────────────────────────────────────────────────────────────────────

#[test]
fn les_octets_residuels_portent_leur_position_et_leur_compte_exacts() {
    let mut octets = encoder_temoignage(&trivial());
    let longueur_canonique = octets.len();
    // DEUX octets en trop, pas un : avec un seul, `restants` vaudrait 1 et un
    // accesseur qui rendrait constamment 1 passerait sans être vu.
    octets.push(0x00);
    octets.push(0x00);

    match decoder_temoignage(&octets) {
        Err(ErreurDecodage::OctetsResiduels { position, restants }) => {
            assert_eq!(
                position, longueur_canonique,
                "la position du refus doit être l'octet qui suit la forme canonique"
            );
            assert_eq!(restants, 2, "deux octets en trop, deux octets résiduels");
        }
        autre => panic!("attendu OctetsResiduels, obtenu {autre:?}"),
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Mutants tués : `replace > with >= in argument_est_prefere` × 3
//                (largeurs 1, 2 et 4 — crates/shogen-core/src/cbor.rs)
//
// La sérialisation préférée de la RFC 8949 exige la forme la PLUS COURTE. La
// suite refusait déjà des arguments largement au-dessus de leur borne ; elle ne
// touchait aucune BORNE. Or c'est exactement là que `>` et `>=` diffèrent : la
// valeur 23 sur un octet supplémentaire, 255 sur deux, 65535 sur quatre. Un
// encodeur hostile qui vise la borne passait donc la gate canonique.
// ─────────────────────────────────────────────────────────────────────────────

/// Vérifie qu'un en-tête de carte à la borne exacte d'une largeur est refusé
/// comme non préféré — et non comme autre chose.
fn exiger_entier_non_prefere(octets: &[u8], attendu: u64) {
    match decoder_temoignage(octets) {
        Err(ErreurDecodage::EntierNonPrefere { argument, .. }) => {
            assert_eq!(
                argument, attendu,
                "le refus doit nommer l'argument non préféré"
            );
        }
        autre => panic!(
            "attendu EntierNonPrefere({attendu}) sur {octets:02x?}, obtenu {autre:?} — \
             la borne de la sérialisation préférée n'est pas tenue"
        ),
    }
}

#[test]
fn la_borne_de_la_serialisation_preferee_est_refusee_sur_un_octet() {
    // Carte (0xA0) d'argument 23 écrit sur UN octet supplémentaire (info 24) :
    // 23 tient dans l'octet d'en-tête, donc cette forme n'est pas la plus
    // courte. `argument > 23` la refuse ; `argument >= 23` l'accepterait.
    exiger_entier_non_prefere(&[0xB8, 0x17], 23);
}

#[test]
fn la_borne_de_la_serialisation_preferee_est_refusee_sur_deux_octets() {
    // Argument 255 écrit sur DEUX octets (info 25) : il tenait sur un.
    exiger_entier_non_prefere(&[0xB9, 0x00, 0xFF], 255);
}

#[test]
fn la_borne_de_la_serialisation_preferee_est_refusee_sur_quatre_octets() {
    // Argument 65535 écrit sur QUATRE octets (info 26) : il tenait sur deux.
    exiger_entier_non_prefere(&[0xBA, 0x00, 0x00, 0xFF, 0xFF], 65_535);
}

#[test]
fn la_borne_de_la_serialisation_preferee_est_refusee_sur_huit_octets() {
    // Argument 4 294 967 295 écrit sur HUIT octets (info 27) : il tenait sur
    // quatre. C'est la borne la plus haute des quatre, et la seule que le
    // premier jet de ce fichier avait manquée — les quatre bras de
    // `argument_est_prefere` se ressemblent assez pour qu'on se trompe de
    // ligne, et c'est le score de mutation qui l'a dit, pas la relecture.
    exiger_entier_non_prefere(
        &[0xBB, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF],
        4_294_967_295,
    );
}

// ─────────────────────────────────────────────────────────────────────────────
// Mutant tué : `replace && with || in lire_attestor`
//              (crates/shogen-core/src/temoignage_canonique.rs)
//
// Le refus de doublon porte sur le COUPLE (clé, identité). Avec `||`, deux
// attestateurs distincts qui partagent leur clé — le cas réel d'un attestateur
// qui change d'identité sans changer de clé, et celui de deux rôles d'une même
// autorité — deviendraient un doublon, et un témoignage licite serait refusé.
// C'est un faux refus, la faute la plus coûteuse d'un vérificateur : elle ne
// se voit pas sur un lot valide qu'on n'a pas essayé.
// ─────────────────────────────────────────────────────────────────────────────

#[test]
fn deux_attestateurs_partageant_leur_cle_mais_pas_leur_identite_sont_admis() {
    let cle_partagee = vec![0x04, 0x1a, 0x2b, 0x3c];
    let temoignage = Temoignage {
        subject: String::from("https://api.example.com/v3/simple/price?ids=bitcoin"),
        attestor: vec![
            Attestor {
                key: cle_partagee.clone(),
                identity: String::from("exemple:attestateur-1"),
            },
            Attestor {
                key: cle_partagee,
                identity: String::from("exemple:attestateur-2"),
            },
        ],
        residual: vec![String::from("A(exemple-residu-1)")],
        transport: String::from("exemple-transport/1"),
        utterance: Utterance {
            hash: empreinte_sha256(b"{\"price\":\"42.17\"}"),
            bytes: Some(b"{\"price\":\"42.17\"}".to_vec()),
        },
        observed_at: ObservedAt {
            clock: String::from("exemple:horloge-du-transport"),
            instant: 1_754_000_000,
        },
        transport_proof: b"preuve-opaque-d'exemple".to_vec(),
    };

    let octets = encoder_temoignage_canonique(&temoignage);
    let relu = decoder_temoignage_canonique(&octets)
        .unwrap_or_else(|erreur| panic!("deux attestateurs de clé commune refusés : {erreur}"));
    assert_eq!(relu.attestor.len(), 2);
    assert_eq!(relu, temoignage);
}

#[test]
fn deux_attestateurs_identiques_restent_un_doublon_refuse() {
    // Le pendant du test précédent : le refus de doublon reste entier. Sans
    // celui-ci, on pourrait tuer le mutant `&&`→`||` en supprimant le contrôle.
    let attestor = Attestor {
        key: vec![0x04, 0x1a, 0x2b, 0x3c],
        identity: String::from("exemple:attestateur-1"),
    };
    let temoignage = Temoignage {
        subject: String::from("https://api.example.com/v3/simple/price?ids=bitcoin"),
        attestor: vec![attestor.clone(), attestor],
        residual: vec![String::from("A(exemple-residu-1)")],
        transport: String::from("exemple-transport/1"),
        utterance: Utterance {
            hash: empreinte_sha256(b"{\"price\":\"42.17\"}"),
            bytes: Some(b"{\"price\":\"42.17\"}".to_vec()),
        },
        observed_at: ObservedAt {
            clock: String::from("exemple:horloge-du-transport"),
            instant: 1_754_000_000,
        },
        transport_proof: b"preuve-opaque-d'exemple".to_vec(),
    };

    let octets = encoder_temoignage_canonique(&temoignage);
    match decoder_temoignage_canonique(&octets) {
        Err(ErreurDecodage::EntreeDupliquee { .. }) => {}
        autre => {
            panic!("attendu EntreeDupliquee sur deux attestateurs identiques, obtenu {autre:?}")
        }
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Mutant tué : `replace || with && in Composant::admet`
//              (crates/shogen-core/src/subject.rs, bras `Requete`)
//
// RFC 3986 §3.4 : `query = *( pchar / "/" / "?" )`. La suite n'exerçait que des
// requêtes sans `/` ni `?` — donc un prédicat qui les aurait refusés passait.
// Ce n'est pas une subtilité : `?` et `/` sont courants dans une requête réelle
// (un paramètre qui porte une URL, un chemin, une date), et les refuser ferait
// déclarer non canonique un `subject` que la RFC admet.
// ─────────────────────────────────────────────────────────────────────────────

#[test]
fn la_requete_admet_la_barre_oblique_et_le_point_d_interrogation() {
    // Ces deux octets sont admis DANS la requête par la RFC 3986 §3.4, et par
    // elle seule : ils ne sont pas des `pchar`.
    let subject = "https://api.example.com/v3/prix?source=https://amont/x&quand=?";
    assert!(
        subject_est_canonique(subject.as_bytes()).is_ok(),
        "« {subject} » doit être canonique : query = *( pchar / \"/\" / \"?\" )"
    );
}

#[test]
fn une_requete_vide_reste_refusee_nommement() {
    // Le pendant du test précédent, et une trouvaille de sa rédaction : le
    // premier `?` DÉLIMITE la requête, les suivants sont des octets de la
    // requête. Admettre `?` dans la requête n'admet donc pas une requête vide —
    // ADR-0016 la refuse nommément, et ce test verrouille ce refus pour qu'on
    // ne puisse pas tuer le mutant précédent en élargissant le prédicat.
    let avec_requete_vide = "https://api.example.com/v3/prix?";
    match subject_est_canonique(avec_requete_vide.as_bytes()) {
        Err(ErreurSubject::RequeteVide { .. }) => {}
        autre => panic!("attendu RequeteVide sur « {avec_requete_vide} », obtenu {autre:?}"),
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Mutants tués : `replace || with && in controler_hote`,
//                `replace == with != in controler_hote`
//                (crates/shogen-core/src/subject.rs, drapeau C3)
//
// Le drapeau « chiffres et points seulement » d'ADR-0016 C3 était couvert par
// ses cas centraux (`1.2.3.4`) et par aucun de ses bords. Or les deux mutants
// qui l'atteignent ne se voient QUE sur des bords : un hôte fait de points
// seuls, et un hôte sans aucun point. Le second contrôle de C3 — le *ends in a
// number checker* — rattrapait tous les autres cas, ce qui rendait le drapeau
// invisible à la suite tout en restant nécessaire.
// ─────────────────────────────────────────────────────────────────────────────

#[test]
fn un_hote_fait_de_points_seuls_est_refuse_comme_litteral() {
    // Le second contrôle de C3 ne le voit pas : ses labels sont tous vides,
    // donc « le dernier label non vide » n'existe pas et le vérificateur de
    // nombre rend faux. Seul le drapeau « chiffres et points seulement »
    // l'attrape — et rien ne le prouvait avant ce test.
    let subject = "https://.../v3/prix";
    match subject_est_canonique(subject.as_bytes()) {
        Err(ErreurSubject::HoteLitteralAdresse { .. }) => {}
        autre => panic!("attendu HoteLitteralAdresse sur « {subject} », obtenu {autre:?}"),
    }
}

#[test]
fn un_hote_sans_point_et_sans_chiffre_reste_un_nom_enregistre() {
    // Le pendant exact : sans point, le drapeau ne doit PAS rester armé. Un
    // hôte d'un seul label alphabétique est un nom enregistré parfaitement
    // ordinaire — le refuser serait un faux refus, et rien ne l'interdisait.
    let subject = "https://localhost/v3/prix";
    assert!(
        subject_est_canonique(subject.as_bytes()).is_ok(),
        "« {subject} » est un nom enregistré, pas une adresse écrite en clair"
    );
}

// ─────────────────────────────────────────────────────────────────────────────
// Mutants tués : trois bords de `dernier_label_est_un_nombre`
//                (crates/shogen-core/src/subject.rs)
//
// Le *ends in a number checker* transposé de la pièce WHATWG était exercé sur
// ses cas francs (`exemple.9`, `exemple.0x1f`) et sur aucune de ses coutures :
// le point terminal, le label qui ouvre par `0` sans être hexadécimal, et le
// label `0x` suivi d'un caractère non hexadécimal. Les trois se distinguent
// par un seul octet — et les trois sont exactement ce qu'un hôte hostile
// écrirait pour passer.
// ─────────────────────────────────────────────────────────────────────────────

#[test]
fn le_point_terminal_ne_cache_pas_un_dernier_label_numerique() {
    // `exemple.9.` — le point final est ignoré, donc le dernier label non vide
    // reste `9`. Sans ce test, une boucle qui lit un octet de trop rendrait
    // l'hôte acceptable en croyant que le dernier label est vide.
    let subject = "https://exemple.9./v3/prix";
    match subject_est_canonique(subject.as_bytes()) {
        Err(ErreurSubject::HoteLitteralAdresse { .. }) => {}
        autre => panic!("attendu HoteLitteralAdresse sur « {subject} », obtenu {autre:?}"),
    }
}

#[test]
fn un_label_qui_ouvre_par_zero_sans_etre_hexadecimal_reste_un_nom() {
    // `exemple.0a` : il ouvre par `0`, mais le second octet n'est ni `x` ni
    // `X` — ce n'est donc pas la graphie hexadécimale de la pièce. Le refuser
    // serait un faux refus sur un nom de domaine licite.
    let subject = "https://exemple.0a/v3/prix";
    assert!(
        subject_est_canonique(subject.as_bytes()).is_ok(),
        "« {subject} » : `0a` n'ouvre pas par `0x`, ce n'est pas un nombre"
    );
}

#[test]
fn un_label_0x_suivi_d_un_caractere_non_hexadecimal_reste_un_nom() {
    // `exemple.0x1g` : `g` n'est pas un chiffre hexadécimal, donc la graphie
    // `0x…` n'est pas complète et le label n'est pas un nombre. Sans ce test,
    // une boucle de contrôle qui ne s'exécute jamais rendrait « nombre » pour
    // tout label ouvrant par `0x` — et `exemple.0x` seul, lui, DOIT être
    // refusé (zéro ou plusieurs chiffres hexadécimaux), ce que le test
    // suivant verrouille.
    let subject = "https://exemple.0x1g/v3/prix";
    assert!(
        subject_est_canonique(subject.as_bytes()).is_ok(),
        "« {subject} » : `0x1g` n'est pas une graphie hexadécimale complète"
    );
}

#[test]
fn un_label_0x_sans_chiffre_reste_un_nombre_refuse() {
    // Le pendant : « "0X" or "0x", followed by ZERO or more ASCII hex digits »
    // — `0x` seul EST un nombre au sens de la pièce. Sans ce test, on pourrait
    // tuer le mutant précédent en n'admettant plus la graphie vide.
    let subject = "https://exemple.0x/v3/prix";
    match subject_est_canonique(subject.as_bytes()) {
        Err(ErreurSubject::HoteLitteralAdresse { .. }) => {}
        autre => panic!("attendu HoteLitteralAdresse sur « {subject} », obtenu {autre:?}"),
    }
}

// ---------------------------------------------------------------------------
// Vague 2 (2026-08-13) — les mutants nés du rendu de la clé épinglée
// ---------------------------------------------------------------------------
//
// Le contrôle (f) d'ADR-0015 point 8 (amendement du 2026-08-13) a fait entrer
// `rendu_de_cle` dans `verification.rs`, et la mesure de mutation de la vague 2
// a rendu QUATRE survivants sur cette seule fonction :
//
//   verification.rs:153:5  replace rendu_de_cle -> String with "xyzzy".into()
//   verification.rs:153:5  replace rendu_de_cle -> String with String::new()
//   verification.rs:154:22 replace match guard texte.is_ascii() with false
//   verification.rs:154:22 replace match guard texte.is_ascii() with true
//
// Ils sont **tuables**, donc ils se tuent — un survivant tuable n'a rien à
// faire dans `survivants.txt`. Ce qu'ils montraient est réel : aucune suite
// n'imprimait le refus d'épinglage, alors que ce refus est le seul endroit où
// un tiers lit QUELLE clé a été épinglée et QUELLE clé a servi. Un refus qu'on
// ne lit pas ne se diagnostique pas (le cœur ne journalise pas).

/// Le refus d'épinglage, avec deux clés US-ASCII : elles se lisent **en
/// toutes lettres**. Tue les deux mutants de valeur de retour, et le mutant de
/// garde à `false` (qui rendrait de l'hexadécimal sur une clé lisible).
#[test]
fn le_refus_d_epinglage_rend_une_cle_ascii_en_toutes_lettres() {
    let mut temoignage = commun::reference();
    temoignage.attestor = vec![Attestor {
        key: b"exemple aabbccdd".to_vec(),
        identity: String::from(commun::IDENTITE),
    }];
    let erreur = verifier_temoignage(&temoignage, &commun::registre(), Some(&commun::constat()))
        .expect_err("la clé épinglée n'est pas celle du contrôle : le refus est dû");
    let rendu = erreur.to_string();
    assert!(
        rendu.contains("exemple aabbccdd"),
        "la clé PORTÉE doit se lire dans le refus : {rendu}"
    );
    assert!(
        rendu.contains("exemple 041a2b3c"),
        "la clé du CONTRÔLE doit se lire dans le refus : {rendu}"
    );
}

/// Une clé épinglée non-ASCII **mais UTF-8 valide** : elle se rend en
/// hexadécimal, pas en lettres. Tue le mutant de garde à `true` — qui
/// laisserait passer en texte une suite d'octets dont la comparaison
/// dépendrait d'une table Unicode versionnée (même motif qu'ADR-0016 C3).
#[test]
fn le_refus_d_epinglage_rend_une_cle_non_ascii_en_hexadecimal() {
    let mut temoignage = commun::reference();
    // « clé » en UTF-8 : 63 6c c3 a9 — valide, non-ASCII.
    temoignage.attestor = vec![Attestor {
        key: "clé".as_bytes().to_vec(),
        identity: String::from(commun::IDENTITE),
    }];
    let erreur = verifier_temoignage(&temoignage, &commun::registre(), Some(&commun::constat()))
        .expect_err("clé épinglée hors contrôle : refus dû");
    let rendu = erreur.to_string();
    assert!(
        rendu.contains("636cc3a9"),
        "une clé non-ASCII se rend en hexadécimal : {rendu}"
    );
    // Et elle ne se rend PAS en lettres : le mot « clé » figure dans la phrase
    // du refus, c'est la VALEUR entre guillemets qu'on regarde.
    assert!(
        !rendu.contains("« clé »"),
        "elle ne se rend PAS en lettres : {rendu}"
    );
}

/// Une clé épinglée qui n'est même pas de l'UTF-8 : hexadécimal aussi. Le
/// pendant du cas précédent — sans lui, le bras de repli ne serait exercé par
/// rien.
#[test]
fn le_refus_d_epinglage_rend_une_cle_non_utf8_en_hexadecimal() {
    let mut temoignage = commun::reference();
    temoignage.attestor = vec![Attestor {
        key: vec![0xff, 0x00, 0x10],
        identity: String::from(commun::IDENTITE),
    }];
    let erreur = verifier_temoignage(&temoignage, &commun::registre(), Some(&commun::constat()))
        .expect_err("clé épinglée hors contrôle : refus dû");
    assert!(
        erreur.to_string().contains("ff0010"),
        "{}",
        erreur.to_string()
    );
}
