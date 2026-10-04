//! Briques communes des gates documentaires (S-G4/S-G5/S-G6/S-G8).
//!
//! Rattachement (G0) : DEVOPS §3 (registre des gates), ADR-0013 (forme des
//! gates), 12 §10 item 2 (unité orchestrateur, passe S3). Même doctrine que
//! `roles.rs` : sélection par chemins exacts, fail-closed sur ce qui ne se
//! lit pas.
//!
//! Le blanchiment `prose_hors_citations` est aux documents ce que `code_seul`
//! est aux sources Rust : il remplace par des espaces les **citations
//! marquées** (guillemets français « … », guillemets anglais “ … ”, code
//! `inline` et blocs ```clôturés```), en conservant longueur et sauts de
//! ligne — le numéro de ligne rapporté est celui du fichier réel. Ce qui
//! reste est la **voix du projet**, la seule que S-G4 juge.

use crate::roles::{Recensement, fichiers_par_extension};
use std::path::{Path, PathBuf};

/// Recense récursivement les fichiers `.md` sous `racine/relatif`, triés.
/// Délègue à la brique commune de `roles.rs` (R-3, revue G2 du 2026-08-13).
pub fn fichiers_markdown(racine: &Path, relatif: &str) -> Recensement {
    fichiers_par_extension(racine, relatif, "md")
}

/// Liste les fichiers (non récursif) d'un répertoire, triés — pour `biblio/`,
/// qui est plate par convention. **La convention est mécanisée** (revue G2 du
/// 2026-08-13, majeure 5) : un sous-répertoire est une erreur, pas un
/// ensemble invisible — sinon déplacer un artefact dans un sous-dossier
/// suffirait à le soustraire au registre.
pub fn fichiers_du_repertoire(repertoire: &Path) -> Result<Vec<PathBuf>, String> {
    let entrees = std::fs::read_dir(repertoire)
        .map_err(|erreur| format!("lecture impossible de {} : {erreur}", repertoire.display()))?;
    let mut fichiers = Vec::new();
    for entree in entrees {
        let entree = entree.map_err(|erreur| {
            format!("entrée illisible dans {} : {erreur}", repertoire.display())
        })?;
        let chemin = entree.path();
        if chemin.is_dir() {
            return Err(format!(
                "sous-répertoire inattendu dans {} : {} — le registre suppose un répertoire plat, la gate refuse de conclure",
                repertoire.display(),
                chemin.display()
            ));
        }
        fichiers.push(chemin);
    }
    fichiers.sort();
    Ok(fichiers)
}

/// Résultat du blanchiment : le texte blanchi (même longueur, mêmes sauts de
/// ligne) et les incidents de forme (délimiteur ouvert jamais fermé).
pub struct ProseBlanchie {
    pub texte: String,
    pub incidents: Vec<String>,
}

/// Blanchit les citations marquées d'un document markdown.
///
/// Zones exclues de la voix du projet, dans cet ordre :
/// 1. blocs de code clôturés ``` … ``` (délimiteur en début de ligne) ;
/// 2. code `inline` (paire de backticks sur la même ligne) ;
/// 3. guillemets français « … » — multi-lignes, non imbriqués ;
/// 4. guillemets anglais courbes “ … ” — multi-lignes ;
/// 5. guillemets ASCII " … " — appariés séquentiellement **dans un même
///    paragraphe** ; un compte impair de " dans un paragraphe est un
///    **incident** et le paragraphe n'est pas blanchi (revue G2 du
///    2026-08-13, majeure 2 : l'ancien appariement glouton laissait une "
///    orpheline avaler la prose jusqu'à la citation suivante, sans bruit).
///
/// Fail-closed sur la typographie porteuse : un « sans », une clôture ```
/// jamais refermée ou une " orpheline est un **incident** — un document
/// malformé pourrait sinon cacher n'importe quoi derrière un délimiteur
/// ouvert.
pub fn prose_hors_citations(source: &str) -> ProseBlanchie {
    let mut sortie = source.as_bytes().to_vec();
    let mut incidents = Vec::new();

    blanchir_blocs_clotures(source, &mut sortie, &mut incidents);
    blanchir_inline(&mut sortie);
    blanchir_paire_multiligne(&mut sortie, "\u{ab}", "\u{bb}", true, &mut incidents);
    blanchir_paire_multiligne(&mut sortie, "\u{201c}", "\u{201d}", true, &mut incidents);
    blanchir_ascii_apparie(&mut sortie, &mut incidents);

    ProseBlanchie {
        texte: String::from_utf8_lossy(&sortie).into_owned(),
        incidents,
    }
}

/// Blanchit le code seul (blocs clôturés et code `inline`), même longueur et mêmes sauts de ligne : la prose et
/// ses citations restent lisibles (S-G9, lot DETTES-B2). Une clôture jamais refermée est l'incident de S-G4.
pub fn prose_sans_code(source: &str) -> String {
    let mut sortie = source.as_bytes().to_vec();
    blanchir_blocs_clotures(source, &mut sortie, &mut Vec::new());
    blanchir_inline(&mut sortie);
    String::from_utf8_lossy(&sortie).into_owned()
}

fn blanchir(sortie: &mut [u8], debut: usize, fin: usize) {
    let mut position = debut;
    while position < fin && position < sortie.len() {
        if let Some(case) = sortie.get_mut(position)
            && *case != b'\n'
            && *case != b'\r'
        {
            *case = b' ';
        }
        position = position.saturating_add(1);
    }
}

/// Blocs ``` … ``` : le délimiteur est reconnu en début de ligne (espaces
/// admis devant). Une clôture ouverte sans fermeture est un incident.
fn blanchir_blocs_clotures(source: &str, sortie: &mut [u8], incidents: &mut Vec<String>) {
    let mut dans_bloc = false;
    let mut debut_bloc = 0usize;
    let mut decalage = 0usize;
    for ligne in source.split_inclusive('\n') {
        if ligne.trim_start().starts_with("```") {
            if dans_bloc {
                blanchir(sortie, debut_bloc, decalage.saturating_add(ligne.len()));
                dans_bloc = false;
            } else {
                dans_bloc = true;
                debut_bloc = decalage;
            }
        }
        decalage = decalage.saturating_add(ligne.len());
    }
    if dans_bloc {
        let (ligne, _) = crate::source::ligne_de(source, debut_bloc);
        incidents.push(format!(
            "clôture ``` ouverte ligne {ligne} jamais refermée — document malformé, la gate refuse de conclure"
        ));
        blanchir(sortie, debut_bloc, sortie.len());
    }
}

/// Code `inline` : paire de backticks sur la même ligne. Un backtick orphelin
/// n'exclut rien (pas d'incident : l'orphelin est courant et inoffensif).
fn blanchir_inline(sortie: &mut [u8]) {
    let taille = sortie.len();
    let mut index = 0usize;
    while index < taille {
        if sortie.get(index).copied() == Some(b'`') {
            let mut fin = index.saturating_add(1);
            while fin < taille {
                let octet = sortie.get(fin).copied().unwrap_or(0);
                if octet == b'`' {
                    blanchir(sortie, index, fin.saturating_add(1));
                    break;
                }
                if octet == b'\n' {
                    break;
                }
                fin = fin.saturating_add(1);
            }
            index = fin.saturating_add(1);
            continue;
        }
        index = index.saturating_add(1);
    }
}

/// Paire ouvrante/fermante multi-lignes (« … » ou “ … ”), non imbriquée.
/// `fail_closed` : une ouvrante jamais refermée est un incident et le reste
/// du document est blanchi (rien ne doit se cacher derrière).
fn blanchir_paire_multiligne(
    sortie: &mut [u8],
    ouvrante: &str,
    fermante: &str,
    fail_closed: bool,
    incidents: &mut Vec<String>,
) {
    let ouvrante = ouvrante.as_bytes();
    let fermante = fermante.as_bytes();
    let taille = sortie.len();
    let mut index = 0usize;
    while index < taille {
        if sortie.get(index..index.saturating_add(ouvrante.len())) == Some(ouvrante) {
            let mut fin = index.saturating_add(ouvrante.len());
            let mut fermee = false;
            while fin < taille {
                if sortie.get(fin..fin.saturating_add(fermante.len())) == Some(fermante) {
                    blanchir(sortie, index, fin.saturating_add(fermante.len()));
                    index = fin.saturating_add(fermante.len());
                    fermee = true;
                    break;
                }
                fin = fin.saturating_add(1);
            }
            if !fermee {
                if fail_closed {
                    let texte = String::from_utf8_lossy(sortie).into_owned();
                    let (ligne, _) = crate::source::ligne_de(&texte, index);
                    incidents.push(format!(
                        "guillemet ouvrant ligne {ligne} jamais refermé — document malformé, la gate refuse de conclure"
                    ));
                    blanchir(sortie, index, taille);
                }
                return;
            }
            continue;
        }
        index = index.saturating_add(1);
    }
}

/// Guillemets ASCII " … " : appariés séquentiellement (1-2, 3-4…) à
/// l'intérieur d'un même paragraphe (borné par ligne vide). Un compte
/// **impair** de " dans un paragraphe est un incident et le paragraphe
/// n'est **pas** blanchi : une " orpheline ne doit rien exclure, et elle
/// doit se dire (revue G2 du 2026-08-13, majeure 2).
fn blanchir_ascii_apparie(sortie: &mut [u8], incidents: &mut Vec<String>) {
    let taille = sortie.len();
    let mut debut_paragraphe = 0usize;
    let mut index = 0usize;
    // Découpe en paragraphes par lignes vides (une ligne ne contenant que
    // des blancs vaut vide), sur les octets déjà partiellement blanchis.
    while index <= taille {
        let fin_de_texte = index == taille;
        let ligne_vide = if fin_de_texte {
            true
        } else if sortie.get(index).copied() == Some(b'\n') {
            let mut regard = index.saturating_add(1);
            loop {
                match sortie.get(regard).copied() {
                    Some(b' ') | Some(b'\t') | Some(b'\r') => {
                        regard = regard.saturating_add(1);
                    }
                    Some(b'\n') | None => break true,
                    Some(_) => break false,
                }
            }
        } else {
            false
        };
        if ligne_vide {
            apparier_paragraphe(sortie, debut_paragraphe, index, incidents);
            debut_paragraphe = index.saturating_add(1);
        }
        if fin_de_texte {
            break;
        }
        index = index.saturating_add(1);
    }
}

fn apparier_paragraphe(sortie: &mut [u8], debut: usize, fin: usize, incidents: &mut Vec<String>) {
    let mut positions = Vec::new();
    let mut index = debut;
    while index < fin && index < sortie.len() {
        if sortie.get(index).copied() == Some(b'"') {
            positions.push(index);
        }
        index = index.saturating_add(1);
    }
    if positions.is_empty() {
        return;
    }
    if positions.len() % 2 != 0 {
        let texte = String::from_utf8_lossy(sortie).into_owned();
        let premiere = positions.first().copied().unwrap_or(debut);
        let (ligne, _) = crate::source::ligne_de(&texte, premiere);
        incidents.push(format!(
            "guillemet ASCII orphelin dans le paragraphe de la ligne {ligne} ({} guillemets) — document ambigu, la gate refuse de conclure sans rien blanchir",
            positions.len()
        ));
        return;
    }
    for paire in positions.chunks(2) {
        if let [ouvrante, fermante] = paire {
            blanchir(sortie, *ouvrante, fermante.saturating_add(1));
        }
    }
}

/// Parse « **N artefacts détenus** » dans l'en-tête d'INDEX.md — la fenêtre
/// est bornée aux ~500 premiers octets, coupés à une frontière de caractère
/// (revue G2 du 2026-08-13, mineure 7 : `get(..500)` rendait `None` sur une
/// coupe intra-UTF-8 et le repli cherchait dans tout le fichier). Partagé
/// par S-G5 (détection de régime) et S-G6 (contrôle du compte).
pub fn compte_declare_en_tete(index: &str) -> Option<usize> {
    let borne = index
        .char_indices()
        .map(|(position, _)| position)
        .take_while(|position| *position <= 500)
        .last()
        .unwrap_or(0);
    let tete = index.get(..borne).unwrap_or(index);
    let marqueur = " artefacts détenus";
    let fin = tete.find(marqueur)?;
    let avant = tete.get(..fin)?;
    let debut_nombre = avant.rfind(|c: char| !c.is_ascii_digit())?;
    avant
        .get(debut_nombre.saturating_add(1)..)?
        .parse::<usize>()
        .ok()
}

/// Normalise un fragment de texte pour la recherche de citations (S-G5) :
/// décode les entités HTML nommées courantes, plie la typographie
/// (apostrophes et guillemets courbes vers l'ASCII), retire l'emphase
/// markdown (`*` et `` ` ``) et plie toute suite de blancs en une espace.
///
/// Le pli typographique existe parce que le même passage vit en trois
/// graphies : U+2019 dans les docs, `&#39;` dans un HTML détenu, `'` dans un
/// sidecar — une recherche qui ne plie pas rate des citations exactes.
pub fn normaliser_pour_recherche(texte: &str) -> String {
    let decode = texte
        .replace("&quot;", "\"")
        .replace("&#39;", "'")
        .replace("&#x27;", "'")
        .replace("&#8217;", "'")
        .replace("&rsquo;", "'")
        .replace("&lsquo;", "'")
        .replace("&#8220;", "\"")
        .replace("&#8221;", "\"")
        .replace("&ldquo;", "\"")
        .replace("&rdquo;", "\"")
        .replace("&apos;", "'")
        .replace("&nbsp;", " ")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&amp;", "&")
        // Ligatures typographiques des PDF : l'extraction les rend telles
        // quelles ; « first » extrait porte ﬁ, la citation porte fi.
        .replace('\u{fb00}', "ff")
        .replace('\u{fb01}', "fi")
        .replace('\u{fb02}', "fl")
        .replace('\u{fb03}', "ffi")
        .replace('\u{fb04}', "ffl");
    let mut sortie = String::with_capacity(decode.len());
    let mut blanc_en_cours = false;
    for caractere in decode.chars() {
        let plie = match caractere {
            '\u{2018}' | '\u{2019}' => '\'',
            '\u{201c}' | '\u{201d}' => '"',
            autre => autre,
        };
        if plie == '*' || plie == '`' {
            continue;
        }
        if plie.is_whitespace() {
            if !blanc_en_cours {
                sortie.push(' ');
            }
            blanc_en_cours = true;
        } else {
            sortie.push(plie);
            blanc_en_cours = false;
        }
    }
    sortie.trim().to_string()
}
