//! **S-G6 `index-sum`** — l'en-tête d'`INDEX.md` en accord avec le contenu
//! réel de `biblio/`, et chaque octet versé enregistré.
//!
//! Ce qu'elle casse (DEVOPS §3) : « l'en-tête d'INDEX.md en désaccord avec le
//! contenu réel de biblio/ — un compte d'artefacts déclaré est déjà parti en
//! dérive une fois ».
//!
//! Deux contrôles, du plus fort au plus faible :
//! 1. **chaque fichier présent dans `biblio/` (hors INDEX.md, hors
//!    `*.sidecar`) est nommé dans INDEX.md** — un artefact versé sans entrée
//!    de registre est exactement la dérive que la gate existe à attraper ;
//! 2. **le compte déclaré en tête d'INDEX (« N artefacts détenus ») égale le
//!    compte réel** des fichiers présents.
//!
//! **Environnements** : les octets de `biblio/` ne sont jamais versionnés
//! (DEVOPS §1) — en CI, seul INDEX.md existe. La gate y contrôle ce qui
//! reste contrôlable (l'en-tête se parse) et imprime que le compte réel
//! n'est contrôlable qu'en local. Un vert de CI dit donc moins qu'un vert
//! local, et il le dit.

use crate::documents::{compte_declare_en_tete, fichiers_du_repertoire};
use crate::rapport::Rapport;
use crate::roles::chemin_relatif;
use std::path::Path;

pub fn executer(racine: &Path) -> Rapport {
    let mut rapport = Rapport::nouveau("S-G6", "index-sum (registre INDEX vs octets de biblio/)");
    rapport
        .chemins_couverts
        .push(String::from("biblio/INDEX.md (en-tête + mentions)"));
    rapport.chemins_couverts.push(String::from(
        "biblio/* (listing plat, hors INDEX.md et *.sidecar)",
    ));

    let chemin_index = racine.join("biblio").join("INDEX.md");
    let index = match std::fs::read_to_string(&chemin_index) {
        Ok(texte) => {
            rapport.presents = 1;
            rapport.examines = 1;
            texte
        }
        Err(erreur) => {
            rapport.incident(format!(
                "biblio/INDEX.md illisible ({erreur}) — le registre est la pièce maîtresse, la gate refuse de conclure"
            ));
            return rapport;
        }
    };

    // 1. Le compte déclaré, parsé depuis l'en-tête (parseur partagé avec
    // S-G5, borné à une frontière de caractère — revue G2, mineure 7).
    let declare = compte_declare_en_tete(&index);
    let Some(declare) = declare else {
        rapport.incident(String::from(
            "en-tête d'INDEX.md sans compte parsable (« **N artefacts détenus** ») — un registre sans compte déclaré n'est pas contrôlable",
        ));
        return rapport;
    };

    // 2. Le contenu réel.
    let fichiers = match fichiers_du_repertoire(&racine.join("biblio")) {
        Ok(fichiers) => fichiers,
        Err(erreur) => {
            rapport.incident(erreur);
            return rapport;
        }
    };
    let artefacts: Vec<_> = fichiers
        .iter()
        .filter(|chemin| **chemin != chemin_index)
        .filter(|chemin| {
            chemin
                .extension()
                .map(|e| e.to_string_lossy().to_ascii_lowercase())
                != Some(String::from("sidecar"))
        })
        .collect();

    if artefacts.is_empty() {
        rapport.notes.push(format!(
            "environnement sans octets biblio/ (conception DEVOPS §1 : jamais versionnés) — compte déclaré {declare}, compte réel non contrôlable ici ; le contrôle plein est tenu en local par la même gate"
        ));
        return rapport;
    }

    rapport.presents = rapport.presents.saturating_add(artefacts.len());
    rapport.examines = rapport.examines.saturating_add(artefacts.len());

    // 3. Chaque octet versé a son entrée au registre — mention DÉLIMITÉE en
    // backticks, la graphie que l'INDEX emploie (revue G2, mineure 8 : une
    // sous-chaîne nue prenait « xa.txt » pour la mention de « a.txt »).
    let mut tous_mentionnes = true;
    for chemin in &artefacts {
        let nom = chemin
            .file_name()
            .map(|n| n.to_string_lossy().into_owned())
            .unwrap_or_default();
        if !index.contains(&format!("`{nom}`")) {
            tous_mentionnes = false;
            rapport.violation(
                chemin_relatif(racine, chemin),
                0,
                format!(
                    "artefact présent dans biblio/ mais absent du registre INDEX.md (mention `{nom}` attendue) — un octet versé sans entrée est la dérive que cette gate attrape"
                ),
                String::new(),
            );
        }
    }

    // 4. Le compte déclaré égale le compte réel — sauf régime de corpus
    // partiel : moins de fichiers que déclarés ET tous mentionnés au
    // registre = sous-ensemble d'un corpus enregistré (checkout partiel),
    // dit en note, jamais en vert muet. Résidu nommé : la suppression
    // locale d'un artefact enregistré est indistinguable de ce régime — le
    // sha256 par entrée de l'INDEX reste la pièce qui tranche.
    if artefacts.len() < declare && tous_mentionnes {
        rapport.notes.push(format!(
            "CORPUS PARTIEL : {} artefact(s) présent(s) sur {declare} déclaré(s), tous mentionnés au registre — le contrôle d'égalité du compte n'est tenu qu'en corpus complet",
            artefacts.len()
        ));
    } else if declare != artefacts.len() {
        rapport.violation(
            String::from("biblio/INDEX.md"),
            0,
            format!(
                "compte déclaré en tête ({declare}) ≠ compte réel ({}) — l'en-tête se re-mesure à chaque versement (règle de l'en-tête d'INDEX)",
                artefacts.len()
            ),
            String::new(),
        );
    }

    rapport.notes.push(format!(
        "compte déclaré {declare}, compte réel {} (hors INDEX.md et *.sidecar)",
        artefacts.len()
    ));
    rapport
}
