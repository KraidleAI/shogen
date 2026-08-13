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
/// L'hôte du `subject` — l'origine que le constat doit rapporter (recoupement
/// d'origine, ADR-0015 point 13).
const ORIGINE: &str = "api.example.com";
const IDENTITE: &str = "exemple:attestateur-1";
const RESIDU_1: &str = "A(exemple-residu-1)";
const RESIDU_2: &str = "A(exemple-residu-2)";
const RESIDU_DE_LA_DELEGATION: &str = "A(transport-check-delegated)";
const TRANSPORT: &str = "exemple-transport/1";
const HORLOGE: &str = "exemple:horloge-du-transport";
/// La révision amont, verbatim, que le verdict reprend (ADR-0015 pt 8 alinéa e).
const REVISION_AMONT: &str = "0000000000000000000000000000000000000000";
/// L'instant porté par le témoignage — et, contrôle (g) oblige, celui que le
/// constat rapporte comme instant de connexion.
const INSTANT: u64 = 1_754_000_000;
/// L'algorithme et les chiffres de la clé épinglée, tels que le constat les
/// porte ; la convention d'épinglage en fait les octets `attestor.key`.
const CLE_ALGORITHME: &str = "exemple";
const CLE_CHIFFRES: &str = "041a2b3c";
/// Les octets épinglés, composés selon la convention — écrits ici en toutes
/// lettres pour que le test dise la même chose que l'adapter, sans partager de
/// code avec lui.
const CLE_EPINGLEE: &[u8] = b"exemple 041a2b3c";
/// L'empreinte SHA-256 de la suite VIDE — le sens émis de ce lot synthétique
/// ne porte aucun octet. Valeur mesurée, déjà au dépôt
/// (`xtask/tests/reproductible.rs`, vecteurs contrôlés par deux
/// implémentations tierces), jamais recopiée de mémoire.
const EMPREINTE_DU_VIDE: &str = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855";

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
    chaine_d_octets(&mut octets, CLE_EPINGLEE);
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
    entete(&mut octets, 0x00, INSTANT);

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

/// Un répertoire de travail **propre à ce processus**.
///
/// Le suffixe de PID n'est pas cosmétique (trouvaille du 2026-08-13, unité
/// mutation/fuzz) : sans lui le chemin est FIXE, et `remove_dir_all` en tête
/// l'efface. Tant qu'une seule suite tourne, personne ne le voit. Sous un
/// exécuteur parallèle — et la gate de mutation en est un, elle lance quatre
/// suites de front (`cargo xtask mutation`, `--jobs 4`) — deux processus
/// partagent le répertoire et l'un efface les lots de l'autre en pleine
/// itération. Le vérificateur rend alors « lot illisible » (code 66) sur un
/// lot qui existait, la position bascule de « acceptée » à « refusée », et le
/// test échoue pour une raison qui n'est pas celle qu'il mesure.
///
/// Effet mesuré avant correctif : le score de mutation n'était pas rejouable —
/// le mutant `subject.rs:522:17` était compté survivant au premier run et tué
/// aux suivants, sur un code de `subject.rs` que le lot trivial n'atteint même
/// pas. Un score non rejouable n'est pas un fait (ADR-0011 point 2).
fn repertoire(nom: &str) -> PathBuf {
    let chemin =
        std::env::temp_dir().join(format!("shogen-canonique-{nom}-{}", std::process::id()));
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

/// Le constat que le binaire compagnon d'ADR-0015 rendrait — **au contrat du
/// point 13** : une ligne JSON à clés triées, dix-huit clés.
///
/// Il est écrit à la main ici, clé par clé, sans passer par l'analyseur qu'il
/// alimente : un test qui produirait son entrée avec le lecteur qu'il vérifie ne
/// prendrait ce lecteur en défaut sur rien. Les six longueurs sont cohérentes
/// dans chaque sens, comme le contrat l'exige (pré-condition de (b)).
fn ecrire_constat(repertoire: &Path, empreinte_preuve: &str, empreinte_utterance: &str) -> PathBuf {
    ecrire_constat_ajuste(repertoire, empreinte_preuve, empreinte_utterance, INSTANT)
}

/// Le même, avec l'instant de connexion en paramètre — le contrôle (g) est le
/// seul à en dépendre.
fn ecrire_constat_ajuste(
    repertoire: &Path,
    empreinte_preuve: &str,
    empreinte_utterance: &str,
    instant: u64,
) -> PathBuf {
    let chemin = repertoire.join("constat.json");
    let octets_de_preuve = OCTETS_DE_PREUVE.len();
    let octets_recus = OCTETS_D_UTTERANCE.len();
    let texte = format!(
        "{{\"attestor_cle_algorithme\":\"{CLE_ALGORITHME}\",\
\"attestor_cle_hex\":\"{CLE_CHIFFRES}\",\
\"connection_info_time\":{instant},\
\"connection_info_version_tls\":\"V1_2\",\
\"empreinte_presentation_sha256\":\"{empreinte_preuve}\",\
\"empreinte_recv_revele_sha256\":\"{empreinte_utterance}\",\
\"empreinte_sent_revele_sha256\":\"{EMPREINTE_DU_VIDE}\",\
\"octets_presentation\":{octets_de_preuve},\
\"revision_amont\":\"{REVISION_AMONT}\",\
\"server_name\":\"{ORIGINE}\",\
\"transcript_recv_authentifie\":{octets_recus},\
\"transcript_recv_longueur\":{octets_recus},\
\"transcript_recv_longueur_attestee\":{octets_recus},\
\"transcript_sent_authentifie\":0,\
\"transcript_sent_longueur\":0,\
\"transcript_sent_longueur_attestee\":0,\
\"verdict\":\"presentation_verifiee\",\
\"version_du_constat\":1}}\n"
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
        sortie.contains(REVISION_AMONT),
        "le verdict reprend VERBATIM la révision amont du constat (ADR-0015 pt 8 e) : {sortie}"
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
    let constat = repertoire.join("constat.json");
    // L'ancien format à trois clés, aujourd'hui hors contrat : il n'est même
    // plus un objet du sous-ensemble, et le refus tombe au premier octet.
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

/// **Le balayage des octets du lot — deux opérateurs, et l'ensemble RÉEL des
/// régions que rien ne lie.**
///
/// # Ce que ce test certifiait à vide, et par quelle mesure on l'a su
///
/// Jusqu'à la revue G2 de la vague 2 (2026-08-13), ce balayage n'avait qu'un
/// opérateur — `^= 0xff` — et concluait « l'ensemble des acceptations est
/// VIDE ». Le vert était **vide de sens** : inverser un octet rend non-ASCII
/// tout octet de texte, et le lot tombe alors au DÉCODAGE (`ChampNonAscii`,
/// `SubjectNonCanonique`), jamais aux contrôles de liaison. Un opérateur qui
/// n'atteint pas les contrôles ne peut rien dire d'eux — et « aucune position
/// acceptée » se lisait comme « rien n'est non lié », ce qui était faux.
///
/// Mesure faite AVANT correction, sur ce lot de 381 octets : le même balayage
/// conduit avec la **substitution ASCII à longueur égale** de
/// `tests/temoignage_reel.rs` (`muter_une_lettre`) rend **84 positions
/// acceptées** sur 304 substitutions essayées, en **quatre régions**. Le même
/// geste sur le lot RÉEL accepte `?symbol=BTCUSDT` → `?symbol=BTCUSDX` en code
/// 0, et de même sur `attestor.identity`, `observed_at.clock` et `transport`.
///
/// # Ce que le test dit désormais
///
/// Il tourne avec les **deux** opérateurs et ÉNUMÈRE l'ensemble réel des
/// positions acceptées, asserté par égalité d'ensembles dans les deux sens :
///
/// * `^= 0xff` — ensemble VIDE, et c'est un fait sur **cet opérateur-là**, pas
///   une conclusion sur les contrôles ;
/// * substitution ASCII — exactement les positions substituables des quatre
///   régions non liées, **calculées depuis la structure du lot** et non écrites
///   en dur : le chemin et la requête de `subject` (hors schéma et hôte),
///   `attestor.identity`, `observed_at.clock`, `transport`.
///
/// Ces quatre régions sont la limite qu'**ADR-0015 point 17 bis** consigne :
/// l'alinéa (h) recoupe l'HÔTE de `subject` contre l'identité de serveur
/// authentifiée ; la ressource désignée — chemin et requête — n'est liée par
/// aucun contrôle recalculable en S3, et les trois identifiants restants ne le
/// sont pas davantage. La limite est **affichée et mesurée, jamais niée** : la
/// phrase de verdict la porte, ce balayage la chiffre, et l'unité S4 « liaison
/// de la désignation » la traite.
///
/// Le test mord dans les deux sens. Un contrôle qui disparaît élargit
/// l'ensemble et tombe ici ; un contrôle nouveau le rétrécit et tombe ici
/// aussi — la liste nommée se rétrécit alors avec le registre, jamais l'inverse.
///
/// Les cas qui asserent (f), (g) et (h) à la variante exacte, sur le témoignage
/// **réel**, vivent dans `tests/temoignage_reel.rs`.
#[test]
fn le_balayage_enumere_les_regions_que_rien_ne_lie() {
    balayer_les_octets();
}

/// La substitution ASCII à longueur égale : une lettre pour une autre lettre,
/// un chiffre pour un autre chiffre — le geste de `muter_une_lettre`
/// (`tests/temoignage_reel.rs`), généralisé au balayage.
///
/// Elle ne s'applique qu'aux octets **alphanumériques**, et c'est une décision :
/// ce sont les seuls dont le remplacement ne casse ni la structure CBOR (les
/// en-têtes ne sont pas du texte) ni la canonicité de `subject` (les
/// délimiteurs `/`, `?`, `=`, `.`, `:` ne bougent pas). Partout ailleurs
/// l'inversion d'octet reste le seul opérateur — et les deux ensembles
/// d'acceptations sont assertés **séparément**, pour qu'aucun ne masque
/// l'autre.
fn substitution_ascii(octet: u8) -> Option<u8> {
    match octet {
        b'a'..=b'z' => Some(if octet == b'x' { b'y' } else { b'x' }),
        b'A'..=b'Z' => Some(if octet == b'X' { b'Y' } else { b'X' }),
        b'0'..=b'9' => Some(if octet == b'7' { b'8' } else { b'7' }),
        _ => None,
    }
}

/// La position d'une aiguille dans le lot, **exigée unique**.
///
/// Un test qui cherche ce qu'il désigne ne devient pas faux en silence le jour
/// où la forme bouge ; l'unicité exigée est le second garde-fou — une aiguille
/// répétée rendrait la plage arbitraire.
fn position_unique(lot: &[u8], aiguille: &[u8]) -> usize {
    let occurrences: Vec<usize> = lot
        .windows(aiguille.len())
        .enumerate()
        .filter(|(_, fenetre)| *fenetre == aiguille)
        .map(|(position, _)| position)
        .collect();
    assert_eq!(
        occurrences.len(),
        1,
        "aiguille ni absente ni répétée exigée : « {} »",
        String::from_utf8_lossy(aiguille)
    );
    occurrences[0]
}

/// La plage d'octets d'une valeur textuelle du lot.
fn plage(lot: &[u8], valeur: &str) -> std::ops::Range<usize> {
    let debut = position_unique(lot, valeur.as_bytes());
    debut..debut.saturating_add(valeur.len())
}

/// Les quatre régions que rien ne lie, **nommées**, plages calculées depuis la
/// structure du lot (ADR-0015 point 17 bis).
fn regions_non_liees(lot: &[u8]) -> Vec<(&'static str, std::ops::Range<usize>)> {
    let debut_subject = position_unique(lot, SUBJECT.as_bytes());
    // L'hôte est la seule part de `subject` que l'alinéa (h) lie ; sa fin est le
    // début de ce que rien ne lie. On la trouve DANS le subject, plutôt que de
    // compter des octets de tête qu'un changement de forme démentirait.
    let decalage_hote = SUBJECT
        .find(ORIGINE)
        .expect("l'hôte figure dans le subject");
    let fin_hote = debut_subject
        .saturating_add(decalage_hote)
        .saturating_add(ORIGINE.len());
    vec![
        (
            "chemin et requête de subject (hors schéma et hôte)",
            fin_hote..debut_subject.saturating_add(SUBJECT.len()),
        ),
        ("attestor.identity", plage(lot, IDENTITE)),
        ("transport", plage(lot, TRANSPORT)),
        ("observed_at.clock", plage(lot, HORLOGE)),
    ]
}

fn balayer_les_octets() {
    // La limite du squelette S2.5 reste levée pour tout ce que les contrôles
    // atteignent : muter un octet de charge utile ne produit pas un autre
    // témoignage acceptable, parce que le hash d'`utterance` et le constat lient
    // le lot à sa preuve (ADR-0005 règle 1), et que (f), (g) et (h) lient la clé
    // épinglée, l'instant et l'hôte. Ce qui reste non lié est ci-dessous, nommé
    // et chiffré.
    let repertoire = repertoire("mutation");
    let origine = lot_intact();
    let registre = ecrire_registre(&repertoire, REGISTRE_COMPLET);
    let constat = ecrire_constat(&repertoire, EMPREINTE_DE_PREUVE, EMPREINTE_D_UTTERANCE);

    let regions = regions_non_liees(&origine);
    let nom_de_region = |position: usize| -> Option<&'static str> {
        regions
            .iter()
            .find(|(_, plage)| plage.contains(&position))
            .map(|(nom, _)| *nom)
    };

    let mut refuses = 0usize;
    let mut substitutions_essayees = 0usize;
    let mut acceptes_par_inversion: Vec<usize> = Vec::new();
    let mut acceptes_par_substitution: Vec<usize> = Vec::new();

    for position in 0..origine.len() {
        let octet = origine
            .get(position)
            .copied()
            .expect("position dans le lot");
        let mut operateurs: Vec<(&'static str, u8)> = vec![("inversion", octet ^ 0xff)];
        if let Some(remplacant) = substitution_ascii(octet) {
            substitutions_essayees = substitutions_essayees.saturating_add(1);
            operateurs.push(("substitution", remplacant));
        }

        for (operateur, remplacant) in operateurs {
            let mut mute = origine.clone();
            if let Some(case) = mute.get_mut(position) {
                *case = remplacant;
            }
            let chemin = repertoire.join(format!("lot-{operateur}-{position}.cbor"));
            std::fs::write(&chemin, &mute).expect("écriture du lot muté");
            let (code, _, erreur) = executer(&[
                &chemin,
                Path::new("--registre"),
                &registre,
                Path::new("--constat"),
                &constat,
            ]);
            if code == 0 {
                let region = nom_de_region(position).unwrap_or("HORS RÉGION NOMMÉE");
                println!("octet {position} ({operateur}) : ACCEPTÉ — région « {region} »");
                if operateur == "inversion" {
                    acceptes_par_inversion.push(position);
                } else {
                    acceptes_par_substitution.push(position);
                }
            } else {
                assert!(
                    erreur.contains("VERDICT : refusé (fail-closed)"),
                    "octet {position} ({operateur}) : verdict de refus absent\nstderr:{erreur}"
                );
                assert!(
                    !erreur.contains("panicked"),
                    "octet {position} ({operateur}) : PANIQUE au lieu d'un refus\nstderr:{erreur}"
                );
                refuses = refuses.saturating_add(1);
            }
        }
    }

    // L'ensemble ATTENDU : les positions substituables des régions nommées, et
    // rien d'autre. Il est dérivé du lot, jamais recopié d'un run précédent.
    let mut attendues: Vec<usize> = Vec::new();
    for (_, plage) in &regions {
        for position in plage.clone() {
            let octet = origine.get(position).copied().unwrap_or(0);
            if substitution_ascii(octet).is_some() {
                attendues.push(position);
            }
        }
    }
    attendues.sort_unstable();

    println!(
        "balayage à deux opérateurs — {} octets : {} inversions, {substitutions_essayees} substitutions ASCII, {refuses} refus fail-closed nommés, 0 panique",
        origine.len(),
        origine.len()
    );
    for (nom, plage) in &regions {
        let texte = String::from_utf8_lossy(origine.get(plage.clone()).unwrap_or(&[])).into_owned();
        println!(
            "  région non liée « {nom} » : octets {}..{} — « {texte} »",
            plage.start, plage.end
        );
    }
    println!("  acceptations par inversion    : {acceptes_par_inversion:?}");
    println!(
        "  acceptations par substitution : {} — {acceptes_par_substitution:?}",
        acceptes_par_substitution.len()
    );

    // Un ensemble attendu VIDE serait le retour exact du défaut corrigé : un
    // « vert » qui ne mesure rien. Le test refuse de conclure dans ce cas.
    assert!(
        !attendues.is_empty(),
        "les régions non liées d'ADR-0015 point 17 bis ne se dérivent plus du lot : \
         un ensemble attendu vide ferait de ce balayage un vert à vide"
    );

    // Opérateur 1 — inversion d'octet. L'ensemble est vide, et le test dit
    // pourquoi : cet opérateur n'atteint pas les contrôles de liaison sur les
    // champs textuels, il tombe au décodage.
    let aucune: Vec<usize> = Vec::new();
    assert_eq!(
        acceptes_par_inversion, aucune,
        "une inversion d'octet a été acceptée : elle devrait tomber au décodage \
         (non-ASCII) ou à un contrôle de liaison"
    );

    // Opérateur 2 — substitution ASCII. Égalité d'ensembles dans les deux sens
    // contre les régions NOMMÉES d'ADR-0015 point 17 bis.
    assert_eq!(
        acceptes_par_substitution, attendues,
        "l'ensemble des positions non liées a bougé. Attendu : les positions \
         substituables du chemin et de la requête de subject (hors schéma et \
         hôte), d'attestor.identity, de transport et d'observed_at.clock — \
         ADR-0015 point 17 bis, unité S4 « liaison de la désignation ». Un \
         contrôle nouveau rétrécit cet ensemble et se porte au registre ; un \
         contrôle perdu l'élargit et c'est une régression."
    );
}

/// Revue G2 de phase C, trouvaille F7 (démontrée : l'ordre des lignes du
/// constat changeait le verdict) : une clé répétée est un refus nommé,
/// jamais « la dernière l'emporte ». Portée au contrat du point 13, elle tombe
/// désormais sur le **tri strict** des clés.
#[test]
fn un_constat_a_cle_repetee_est_refuse() {
    let (lot, registre, constat) = preparer("constat-cle-repetee", &lot_intact(), REGISTRE_COMPLET);
    let texte = std::fs::read_to_string(&constat).expect("constat de référence");
    let doublon = texte.replacen(
        &format!("\"server_name\":\"{ORIGINE}\","),
        &format!("\"server_name\":\"{ORIGINE}\",\"server_name\":\"{ORIGINE}\","),
        1,
    );
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
