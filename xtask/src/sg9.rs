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
//! Bornes imprimées, jamais tues : MONARK (dépôt hors arbre), `biblio/` sans octets (DEVOPS §1,
//! prédicat de S-G6), PX (registre hors dépôt, D.2 n° 10), lots MONARK. Non mécanisés, déclarés :
//! lignes de D.2 par sha256, graine et clé du constat, contenu de docs/16. Résidu : la fidélité des
//! lignes citées reste au G2.
//! Coquille hors rôle S-G3 : tranches et indices bornés par construction (positions de motifs).

use crate::documents::prose_sans_code;
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
    let Ok([Some(t), Some(registre), Some(a), Some(b)]) = <[_; 4]>::try_from(lus) else {
        return r;
    };
    let prose = prose_sans_code(&t);
    controle_a(&mut r, racine, &t);
    controle_b(&mut r, &t, &registre);
    controle_c(&mut r, &t, &prose, &a, &b);
    controle_nombres(&mut r, &t, &prose);
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

const A_MONARK: &str = "(a) référence MONARK sans sha de 40 chiffres";
const A_CHEMIN: &str = "(a) référence : chemin absolu ou non canonique";
const A_ABSENT: &str = "(a) référence : fichier introuvable depuis la racine";
const A_PLAGE: &str = "(a) référence : plage hors du fichier";
const A_CELLULE: &str = "(a) cellule de contrôle sans référence ni motif";

/// Spans de code `inline` (deux backticks sur une ligne) : décalage du contenu, contenu.
fn spans(t: &str) -> Vec<(usize, &str)> {
    let (mut trouves, mut base) = (Vec::new(), 0usize);
    for ligne in t.split_inclusive('\n') {
        let mut morceaux = ligne.split('`');
        let mut position = base + morceaux.next().map_or(0, str::len);
        while let (Some(contenu), Some(apres)) = (morceaux.next(), morceaux.next()) {
            trouves.push((position + 1, contenu));
            position += contenu.len() + apres.len() + 2;
        }
        base += ligne.len();
    }
    trouves
}

/// `12` ou `12-14` : la plage d'une référence.
fn plage(texte: &str) -> Option<(usize, usize)> {
    let (a, b) = texte.split_once('-').unwrap_or((texte, texte));
    let chiffres = |s: &str| !s.is_empty() && s.bytes().all(|o| o.is_ascii_digit());
    (chiffres(a) && chiffres(b)).then(|| Some((a.parse().ok()?, b.parse().ok()?)))?
}

fn sha_monark(chemin: &str) -> bool {
    let reste = chemin.strip_prefix("F:/Monark@");
    let sha = reste.and_then(|x| x.split_once(':'));
    let hexa = |o: u8| matches!(o, b'0'..=b'9' | b'a'..=b'f');
    sha.is_some_and(|(s, _)| s.len() == 40 && s.bytes().all(hexa))
}

fn canonique(chemin: &str) -> bool {
    let normal = |s: &str| !s.is_empty() && s != "." && s != "..";
    let segments = chemin.split('/').all(normal);
    segments && !chemin.contains(['\\', ':'])
}

fn nombre_de_lignes(fichier: &Path) -> Option<usize> {
    let o = std::fs::read(fichier).ok()?;
    let ouverte = o.last().is_some_and(|x| *x != b'\n');
    Some(o.iter().filter(|x| **x == b'\n').count() + usize::from(ouverte))
}

fn controle_a(r: &mut Rapport, racine: &Path, t: &str) {
    let (mut resolues, mut monark, mut absentes) = (0, 0, Vec::new());
    let sans_octets = biblio_sans_octets(racine);
    for (p, span) in spans(t) {
        let Some((chemin, lignes)) = span.rsplit_once(':') else {
            continue;
        };
        let Some((debut, fin)) = plage(lignes) else {
            continue;
        };
        if span.starts_with("F:/Monark") {
            monark += 1;
            if !sha_monark(chemin) {
                viol(r, t, p, A_MONARK, span);
            }
            continue;
        }
        if chemin.contains(char::is_whitespace) || !chemin.contains(['/', '.']) {
            continue;
        }
        let fichier = racine.join(chemin);
        let motif = if !canonique(chemin) {
            A_CHEMIN
        } else if sans_octets && chemin.starts_with("biblio/") && !fichier.exists() {
            absentes.push(span);
            continue;
        } else {
            match nombre_de_lignes(&fichier) {
                None => A_ABSENT,
                Some(n) if debut == 0 || debut > fin || fin > n => A_PLAGE,
                Some(_) => {
                    resolues += 1;
                    continue;
                }
            }
        };
        viol(r, t, p, motif, span);
    }
    let mut base = 0;
    for ligne in t.split_inclusive('\n') {
        let cellule = ligne.split('|').nth(5);
        let ligne_t = ligne.trim_start().starts_with("| T-");
        if cellule.is_some_and(|c| ligne_t && !cellule_controle(c)) {
            viol(r, t, base, A_CELLULE, "");
        }
        base += ligne.len();
    }
    let borne = if sans_octets {
        "sans octets, non contrôlée(s) ici (DEVOPS §1)"
    } else {
        "peuplée, contrôle plein"
    };
    r.notes.push(format!(
        "(a) {resolues} référence(s) résolue(s) ; {monark} MONARK (forme du sha seule, dépôt hors \
         arbre) ; biblio/ {borne} : [{}]",
        absentes.join(", ")
    ));
}

/// Borne `biblio/` de (a) : le prédicat de S-G6, aucun octet versé à `biblio/` (dossier absent compris).
fn biblio_sans_octets(racine: &Path) -> bool {
    let dossier = racine.join("biblio");
    let index = dossier.join("INDEX.md");
    !dossier.exists()
        || crate::documents::fichiers_du_repertoire(&dossier)
            .is_ok_and(|f| !f.iter().any(|c| crate::sg6::octet_verse(c, &index)))
}

/// Une cellule de contrôle porte une référence `…:ligne`, ou `[aucun contrôle]` suivi d'un motif.
fn cellule_controle(c: &str) -> bool {
    let reference = |s: &(usize, &str)| s.1.rsplit_once(':').and_then(|x| plage(x.1)).is_some();
    let motif = c.split_once("[aucun contrôle]").map(|x| x.1);
    spans(c).iter().any(reference) || motif.is_some_and(|m| m.contains(char::is_alphanumeric))
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

/// Identifiant `SHOGEN-…-n`, `MONARK-…-n` ou `PX-Shogen-n` qui commence en `position`.
fn identifiant(t: &str, position: usize) -> Option<&str> {
    let reste = t.get(position..)?;
    let prefixes = ["SHOGEN-", "MONARK-", "PX-Shogen-"];
    let prefixe = prefixes.into_iter().find(|p| reste.starts_with(p))?;
    let fin = reste.find(|c: char| !(c.is_ascii_alphanumeric() || c == '-'));
    let fin = fin.unwrap_or(reste.len());
    let jeton = reste[..fin].trim_end_matches('-');
    let dernier = jeton.rsplit('-').next().unwrap_or("");
    let numero = !dernier.is_empty() && dernier.bytes().all(|o| o.is_ascii_digit());
    let majuscules = prefixe.starts_with("PX") || !jeton.bytes().any(|o| o.is_ascii_lowercase());
    let libre = !mot(avant(t, position)) && avant(t, position) != Some('-');
    (libre && majuscules && numero && jeton.len() > prefixe.len()).then_some(jeton)
}

/// Identifiant défini en tête de cellule (la première qui en porte un) : seul, ou suivi d'une espace
/// ou d'une parenthèse.
fn definition(cellule: &str) -> Option<&str> {
    let cellule = cellule.trim();
    let id = identifiant(cellule, 0)?;
    let suite = &cellule[id.len()..];
    (suite.is_empty() || suite.starts_with([' ', '('])).then_some(id)
}

/// Lots cités après « lot » ou « lots », en liste (« lots D8b et D8c ») ; vrai pour un lot MONARK.
fn lots(prose: &str) -> Vec<(usize, &str, bool)> {
    let mut cites = Vec::new();
    for (p, _) in prose.to_ascii_lowercase().match_indices("lot") {
        let suite = &prose[p + 3..];
        let suite = suite.strip_prefix('s').unwrap_or(suite);
        let Some(suite) = suite.strip_prefix(' ').filter(|_| !mot(avant(prose, p))) else {
            continue;
        };
        let monark = suite.strip_prefix("MONARK ");
        let mut reste = monark.unwrap_or(suite);
        loop {
            let fin = reste.find(|c: char| !(c.is_ascii_alphanumeric() || c == '-'));
            let fin = fin.unwrap_or(reste.len());
            let nom = reste[..fin].trim_end_matches('-');
            if !nom.starts_with(|c: char| c.is_ascii_uppercase()) {
                break;
            }
            cites.push((prose.len() - reste.len(), nom, monark.is_some()));
            let apres = reste[fin..].strip_prefix(", ");
            match apres.or_else(|| reste[fin..].strip_prefix(" et ")) {
                Some(s) => reste = s,
                None => break,
            }
        }
    }
    cites
}

fn controle_c(r: &mut Rapport, t: &str, prose: &str, annexe_a: &str, annexe_b: &str) {
    let mut definis = Vec::new();
    for ligne in annexe_b.lines().map(str::trim_start) {
        let puce = ligne.strip_prefix("- **");
        definis.extend(puce.and_then(|x| identifiant(x, 0)));
        let tete = ligne.strip_prefix('|').map(|l| l.split('|').take(2));
        definis.extend(tete.into_iter().flatten().find_map(definition));
    }
    let (mut items, mut px) = (0, Vec::new());
    for (p, _) in t.char_indices() {
        match identifiant(t, p) {
            Some(id) if id.starts_with("PX-") => px.extend(Some(id).filter(|i| !px.contains(i))),
            Some(id) if definis.contains(&id) => items += 1,
            Some(id) => viol(r, t, p, "(c) item non défini à l'annexe B", id),
            None => {}
        }
    }
    let (mut presents, mut monark) = (0, Vec::new());
    for (p, nom, de_monark) in lots(prose) {
        let phrase = format!("lot {nom}");
        let libre = |s: &str| s.starts_with(|c: char| !(c.is_ascii_alphanumeric() || c == '-'));
        let suites = annexe_a.match_indices(&phrase);
        let cite = suites
            .map(|(q, _)| &annexe_a[q + phrase.len()..])
            .any(libre);
        if de_monark {
            monark.extend(Some(nom).filter(|n| !monark.contains(n)));
        } else if cite || annexe_a.contains(&format!("**{nom}**")) {
            presents += 1;
        } else {
            viol(r, t, p, "(c) lot absent de l'annexe A", nom);
        }
    }
    r.notes.push(format!(
        "(c) {items} item(s) défini(s) à l'annexe B, {presents} lot(s) à l'annexe A ; non résolus, \
         listés : PX : [{}] (registre hors dépôt, D.2 n° 10) ; lots MONARK : [{}]",
        px.join(", "),
        monark.join(", ")
    ));
}

/// Suites de groupes de chiffres reliés par un même séparateur : (début, longueurs, séparateur).
fn suites(t: &str, separateurs: &[u8]) -> Vec<(usize, Vec<usize>, u8)> {
    let o = t.as_bytes();
    let chiffre = |i: usize| o.get(i).is_some_and(u8::is_ascii_digit);
    let (mut trouvees, mut i) = (Vec::new(), 0);
    while i < o.len() {
        if !chiffre(i) || (i > 0 && chiffre(i - 1)) {
            i += 1;
            continue;
        }
        let (debut, mut longueurs, mut sep) = (i, Vec::new(), 0);
        loop {
            let depart = i;
            while chiffre(i) {
                i += 1;
            }
            longueurs.push(i - depart);
            let s = o.get(i).copied().unwrap_or(0);
            if !(separateurs.contains(&s) && chiffre(i + 1) && (sep == 0 || sep == s)) {
                break;
            }
            (sep, i) = (s, i + 1);
        }
        trouvees.push((debut, longueurs, sep));
    }
    trouvees
}

/// (d) dates, sur la prose ; (f) décimaux et adresses IPv4, sur tout le texte.
fn controle_nombres(r: &mut Rapport, t: &str, prose: &str) {
    let mut iso = 0;
    for (debut, l, sep) in suites(prose, b"/.-") {
        let devant = l.len() == 3 && l[0] == 4 && l[1] <= 2 && l[2] <= 2;
        let derriere = l.len() == 3 && l[2] == 4 && l[0] <= 2 && l[1] <= 2;
        if sep == b'-' && l == [4, 2, 2] {
            iso += 1;
        } else if devant || derriere {
            viol(r, t, debut, "(d) date hors forme ISO (AAAA-MM-JJ)", "");
        }
    }
    for (debut, l, sep) in suites(t, b".,") {
        let exempte = avant(t, debut).is_some_and(|c| c.is_alphanumeric() || "§.-_/".contains(c));
        if sep == b'.' && l.len() == 4 && l.iter().all(|n| *n <= 3) {
            viol(r, t, debut, "(f) adresse IP", "");
        } else if l.len() == 2 && !exempte {
            viol(r, t, debut, "(f) nombre décimal", "");
        }
    }
    r.notes.push(format!(
        "(d) {iso} date(s) ISO ; formes numériques non ISO refusées"
    ));
}
