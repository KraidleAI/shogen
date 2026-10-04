//! **S-G9 `references`** — les contrôles (a) à (f) de l'oracle `verif_refs.py` du lot E1, mécanisés
//! sur le modèle de menace (`docs/17-modele-de-menace.md`).
//!
//! Rattachement (G0) : ADR-0028 annexe B.7, SHOGEN-E1-XTASK-REFS-1 (S-G8 ne lit que JOURNAL.md ; S-G5
//! ne contrôle ni les guillemets droits ni les citations françaises ; aucune gate ne résout les
//! références chemin et ligne) ; contrat : `docs/adr-0028/G0-lots-DETTES.md`, lot DETTES-B2. L'oracle
//! est hors dépôt : ses contrôles sont repris de leur description (`docs/G1-lot-E1-modele-de-menace.md`
//! §5), avec pour cas les survivants de la revue G2 d'E1 (`xtask/tests/mutants.rs`, section S-G9).
//!
//! (a) `chemin:ligne` en span de code : chemin canonique depuis la racine, fichier présent, plage dans
//! le fichier ; MONARK : sha de 40 chiffres ; cellule de contrôle d'une ligne T : une référence, ou
//! `[aucun contrôle]` et son motif. (b) `A(...)` défini au registre 08, casse comprise. (c) items
//! définis à l'annexe B, lots présents à l'annexe A. (d) dates ISO seulement. (e) ni guillemet droit
//! ni apostrophe de citation hors du code ; citation française « … » présente ailleurs dans le dépôt.
//! (f) ni pièce de D.2, ni pour-cent, ni décimal, ni statistique, ni adresse IP ou électronique.
//!
//! Bornes imprimées, jamais tues : MONARK (dépôt hors arbre), `biblio/` absente (DEVOPS §1), PX
//! (registre hors dépôt, D.2 n° 10), lots MONARK. Non mécanisés, déclarés : lignes de D.2 par sha256,
//! graine et clé du constat, contenu de docs/16. Résidu : la fidélité des lignes citées reste au G2.
//! Coquille hors rôle S-G3 : tranches et indices bornés par construction (positions de motifs).

use crate::rapport::{Rapport, lire};
use crate::source::{ligne_de, occurrences_nues};
use std::path::Path;

/// Le document sous gate, en chemin exact ; puis ses trois registres.
pub const PERIMETRE: &str = "docs/17-modele-de-menace.md";
const REGISTRES: [&str; 3] = [
    "docs/08-assumptions.md",
    "docs/adr-0028/ANNEXE-A-lots.md",
    "docs/adr-0028/ANNEXE-B-items.md",
];
const TITRE: &str = "références du modèle de menace (verif_refs.py mécanisé)";

pub fn executer(racine: &Path) -> Rapport {
    let mut r = Rapport::nouveau("S-G9", TITRE);
    let chemins = std::iter::once(PERIMETRE).chain(REGISTRES);
    let lus: Vec<_> = chemins.map(|c| lire_exact(&mut r, racine, c)).collect();
    let Ok([Some(t), Some(registre), Some(_), Some(_)]) = <[_; 4]>::try_from(lus) else {
        return r;
    };
    controle_b(&mut r, &t, &registre);
    r.notes.push(String::from(
        "non mécanisés : lignes de D.2 par sha256 (outil FM-1.1), graine et clé du constat, contenu \
         de docs/16 ; résidu : la fidélité des lignes citées reste la lecture du G2",
    ));
    r
}

fn lire_exact(r: &mut Rapport, racine: &Path, relatif: &str) -> Option<String> {
    r.chemins_couverts.push(relatif.to_string());
    if !racine.join(relatif).is_file() {
        r.incident(format!(
            "fichier absent : {relatif} (chemin exact, refus de conclure)"
        ));
        return None;
    }
    r.presents += 1;
    lire(r, racine, &racine.join(relatif))
}

/// Violation située dans docs/17 ; une forme de (f) ne se recopie jamais en extrait.
fn viol(r: &mut Rapport, t: &str, position: usize, motif: &str, extrait: &str) {
    let (ligne, _) = ligne_de(t, position);
    r.violation(PERIMETRE.into(), ligne, motif.into(), extrait.into());
}

/// Le caractère qui précède `position`.
fn avant(t: &str, position: usize) -> Option<char> {
    t.get(..position).and_then(|x| x.chars().next_back())
}

/// Vrai si `c` prolonge un mot (lettre, chiffre ou soulignement).
fn mot(c: Option<char>) -> bool {
    c.is_some_and(|c| c.is_alphanumeric() || c == '_')
}

const B_RESIDU: &str = "(b) résidu non défini au registre 08 (casse comprise)";

fn controle_b(r: &mut Rapport, t: &str, registre: &str) {
    fn entree(l: &str) -> Option<&str> {
        Some(l.trim_start().strip_prefix("| A(")?.split_once(')')?.0)
    }
    let definis: Vec<&str> = registre.lines().filter_map(entree).collect();
    let permis = |o: u8| o.is_ascii_alphanumeric() || b"-._".contains(&o);
    let forme = |n: &str| !n.is_empty() && n.bytes().all(permis);
    let mut resolus = 0;
    for p in occurrences_nues(t, "A(") {
        let Some((nom, _)) = t[p + 2..].split_once(')').filter(|x| forme(x.0)) else {
            continue;
        };
        if mot(avant(t, p)) {
            continue;
        }
        if definis.contains(&nom) {
            resolus += 1;
        } else {
            viol(r, t, p, B_RESIDU, nom);
        }
    }
    r.notes
        .push(format!("(b) {resolus} résidu(s) résolu(s) au registre 08"));
}
