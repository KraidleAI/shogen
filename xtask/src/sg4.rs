//! **S-G4 `vocabulary`** — les formulations interdites du registre 09 dans la
//! voix du projet.
//!
//! Ce qu'elle casse (DEVOPS §3) : « mots interdits (`verified`, `garanti`,
//! `quorum de .* sources diverses` sans rangs…) dans `docs/` hors citations
//! marquées ». Pourquoi : 09-vocabulaire — « La gate S-G4 (DEVOPS §3)
//! mécanisera cette liste » ; l'audit S1 a montré que la liste vit (deux
//! graves trouvés en relecture humaine).
//!
//! **Ce que la gate mécanise, et rien de plus** : le sous-ensemble **non
//! ambigu** du registre — les locutions qui, hors citation marquée, sont
//! fautives sans jugement de contexte. Le registre complet (09) reste
//! l'obligation de relecture de toute phrase sortante (09 §Règle
//! d'application) ; la gate borne le pire, elle ne remplace pas la relecture.
//! Élargir la liste est un resserrage (licite) ; la réduire demande une ADR
//! (charte shogen-devops §2).
//!
//! Périmètre : `docs/**/*.md`, **hors `docs/09-vocabulaire.md`** — le
//! registre qui énonce les interdits ne peut pas être scanné contre
//! lui-même (sa section « héritées » nomme les mots hors guillemets) —, puis
//! `s2-harness/**/*.md` sans exclusion (depuis le 2026-10-02 : README et
//! RUNBOOK du harnais, SHOGEN-ORACLE-PERIMETRE-1 (i), ADR-0028 annexe B).

use crate::documents::{fichiers_markdown, prose_hors_citations};
use crate::rapport::{Rapport, lire};
use crate::roles::chemin_relatif;
use crate::source::{ligne_de, occurrences_bornees};
use std::path::Path;

/// Le fichier du registre lui-même, seul exclu du périmètre.
const REGISTRE: &str = "docs/09-vocabulaire.md";

/// Les locutions interdites mécanisées, avec le motif du registre.
///
/// Origine : 09-vocabulaire (v2, 2026-08-12), colonnes « interdit ». La
/// liste est **fermée et versionnée ici** ; chaque entrée est bornée par
/// non-mots et cherchée insensible à la casse ASCII.
pub const LOCUTIONS_INTERDITES: &[(&str, &str)] = &[
    (
        "donnée vérifiée",
        "surclamation d'assurance (09 §héritées) — l'attestation couvre le dire, jamais le vrai",
    ),
    (
        "données vérifiées",
        "surclamation d'assurance (09 §héritées) — l'attestation couvre le dire, jamais le vrai",
    ),
    (
        "donnée vraie",
        "l'attestation prouve le dire, jamais le vrai (09) — « valeur admise dans l'enveloppe du quorum effectif, sous [résidus] »",
    ),
    (
        "données vraies",
        "l'attestation prouve le dire, jamais le vrai (09) — « valeur admise dans l'enveloppe du quorum effectif, sous [résidus] »",
    ),
    (
        "fait signé",
        "personne ne signe un fait — le fait est produit par un typeur, testé jamais prouvé (09)",
    ),
    (
        "faits signés",
        "personne ne signe un fait — le fait est produit par un typeur, testé jamais prouvé (09)",
    ),
    ("prix garanti", "le quorum confine, il n'exactifie pas (09)"),
    (
        "sources indépendantes",
        "l'indépendance ne s'observe pas, elle se teste — jamais établie, seulement non-rejetée sur des axes nommés (09)",
    ),
    (
        "sources diverses",
        "confond déclaré et mesuré — la leçon K&L §4 / L&M p. 1603 (09) : « quorum k_eff=…, axes mesurés : … »",
    ),
    (
        "niveau de sécurité du lot",
        "les résidus de transport ne se moyennent pas (09, ADR-0001) — la liste des résidus, par témoignage",
    ),
    (
        "attestor décentralisé",
        "la décentralisation non comptée est le mirroring possible (09, Chainlink v1) — « n attestors, comptés dans la partition R2 »",
    ),
    (
        "attestors décentralisés",
        "la décentralisation non comptée est le mirroring possible (09, Chainlink v1) — « n attestors, comptés dans la partition R2 »",
    ),
    (
        "verified",
        "qualificatif d'assurance interdit hors citation verbatim (09 §héritées)",
    ),
    (
        "validated",
        "qualificatif d'assurance interdit hors citation verbatim (09 §héritées)",
    ),
    (
        "guaranteed",
        "qualificatif d'assurance interdit hors citation verbatim (09 §héritées)",
    ),
];

/// Les arbres du périmètre, en chemins exacts et dans cet ordre. Chacun est
/// recensé par `fichiers_markdown` : absent ou sans `.md`, il est un incident,
/// jamais un ensemble vide. S-G5 lit cette même liste : un seul périmètre
/// pour les deux gates.
pub const PERIMETRE: &[&str] = &["docs", "s2-harness"];

pub fn executer(racine: &Path) -> Rapport {
    let mut rapport = Rapport::nouveau("S-G4", "vocabulary (registre 09 mécanisé, voix du projet)");
    let registre = racine.join(REGISTRE);
    let mut a_examiner = Vec::new();
    for relatif in PERIMETRE {
        let recensement = fichiers_markdown(racine, relatif);
        for incident in recensement.incidents {
            rapport.incident(incident);
        }
        let retenus: Vec<_> = recensement
            .fichiers
            .into_iter()
            .filter(|chemin| *chemin != registre)
            .collect();
        rapport
            .chemins_couverts
            .push(format!("{relatif}/**/*.md : {} fichier(s)", retenus.len()));
        a_examiner.extend(retenus);
    }
    rapport.chemins_couverts.push(format!(
        "hors {REGISTRE} — le registre lui-même, seule exclusion du périmètre"
    ));
    rapport.presents = a_examiner.len();
    if !registre.is_file() {
        rapport.incident(format!(
            "le registre {REGISTRE} est absent — la liste mécanisée n'a plus de source, la gate refuse de conclure"
        ));
    }

    for chemin in &a_examiner {
        let Some(texte) = lire(&mut rapport, racine, chemin) else {
            continue;
        };
        let relatif = chemin_relatif(racine, chemin);
        let prose = prose_hors_citations(&texte);
        for incident in &prose.incidents {
            rapport.incident(format!("{relatif} : {incident}"));
        }
        for (locution, motif) in LOCUTIONS_INTERDITES {
            for decalage in occurrences_bornees(&prose.texte, locution) {
                let (ligne, contenu) = ligne_de(&texte, decalage);
                rapport.violation(
                    relatif.clone(),
                    ligne,
                    format!("« {locution} » dans la voix du projet — {motif}"),
                    contenu,
                );
            }
        }
    }

    rapport.notes.push(format!(
        "{} locution(s) mécanisée(s) — le sous-ensemble non ambigu du registre 09 ; la relecture complète (09 §Règle) reste due, la gate ne la remplace pas",
        LOCUTIONS_INTERDITES.len()
    ));
    rapport.notes.push(String::from(
        "citations marquées exclues : « … », “ … ”, \" … \" (paires d'un même paragraphe, orphelin = incident), `code`, blocs ```",
    ));
    rapport.notes.push(String::from(
        "résidu : le lien liste-mécanisée ↔ registre 09 est de discipline, pas mécanisé — réduire la liste exige une ADR (charte §2), l'élargir est un resserrage licite",
    ));
    rapport
}
