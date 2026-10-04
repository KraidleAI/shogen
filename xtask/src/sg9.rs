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
//! lignes de D.2 par sha256, graine et clé du constat, contenu de docs/16 ; (g) deux formes
//! proscrites et (h) structure des tables S et T (ligne T retirée, S sans menace ni motif, cellule de
//! résidu vide, jeton de chemin servi absent, marqueur entre guillemets au lieu du jeton) de
//! `verif_refs.py` (`docs/G1-lot-E1-modele-de-menace.md` §5) ; (i) et (j), propres au lot E1, sans
//! objet. Résidu : la fidélité des lignes citées reste au G2.
//! Coquille hors rôle S-G3 : tranches et indices bornés par construction (positions de motifs).

use crate::documents::{fichiers_markdown, normaliser_pour_recherche, prose_sans_code};
use crate::rapport::{Rapport, lire};
use crate::roles::chemin_relatif;
use crate::sg5::{LONGUEUR_MINIMALE, parait_anglais};
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
    controle_e(&mut r, racine, &t, &prose);
    controle_f(&mut r, &t);
    r.notes.push(String::from(
        "non mécanisés : lignes de D.2 par sha256 (outil FM-1.1), graine et clé du constat, contenu \
         de docs/16, (g) formes proscrites et (h) structure des tables S et T de verif_refs.py ; \
         résidu : la fidélité des lignes citées reste la lecture du G2",
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

const MOIS: &str = "janvier février mars avril mai juin juillet août septembre octobre novembre \
    décembre january february march april may june july august september october november december";

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
    let bas = prose.to_ascii_lowercase();
    for mois in MOIS.split(' ') {
        for p in occurrences_nues(&bas, mois) {
            let (tete, queue) = (&bas[..p], &bas[p + mois.len()..]);
            let tete_nue = tete.trim_end().trim_end_matches("er");
            let nombre_avant = tete_nue.ends_with(|c: char| c.is_ascii_digit());
            let nombre_apres = queue.trim_start().starts_with(|c: char| c.is_ascii_digit());
            let isole =
                !tete.ends_with(char::is_alphabetic) && !queue.starts_with(char::is_alphabetic);
            if isole && (nombre_avant || nombre_apres) {
                viol(r, t, p, "(d) date hors forme ISO (nom de mois)", "");
            }
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
        "(d) {iso} date(s) ISO ; non ISO et noms de mois refusés"
    ));
}

const E_APOSTROPHES: &str = "(e) citation entre apostrophes hors span de code";
const E_FRANCAISE: &str = "(e) citation française introuvable dans le dépôt";

fn controle_e(r: &mut Rapport, racine: &Path, t: &str, prose: &str) {
    for (p, _) in prose.match_indices('"') {
        viol(r, t, p, "(e) guillemet droit hors span de code", "");
    }
    let mut base = 0;
    for ligne in prose.split_inclusive('\n') {
        if let Some(p) = apostrophe_de_citation(ligne) {
            viol(r, t, base + p, E_APOSTROPHES, "");
        }
        base += ligne.len();
    }
    let (mut controlees, mut ecartees, mut anglaises) = (0, 0, 0);
    let (mut corpus, mut reste) = (None, prose);
    while let Some(ouverture) = reste.find('\u{ab}') {
        let p = prose.len() - reste.len() + ouverture;
        let suite = &reste[ouverture + '\u{ab}'.len_utf8()..];
        let Some((citation, apres)) = suite.split_once('\u{bb}') else {
            viol(r, t, p, "(e) guillemet ouvrant jamais refermé", "");
            break;
        };
        reste = apres;
        let n = normaliser_pour_recherche(citation);
        let n = n.trim_matches(|c: char| !c.is_alphanumeric());
        if parait_anglais(n) {
            anglaises += 1;
        } else if n.len() < LONGUEUR_MINIMALE {
            ecartees += 1;
        } else {
            controlees += 1;
            let pieces: &Vec<String> = corpus.get_or_insert_with(|| corpus_francais(r, racine));
            if !pieces.iter().any(|piece| piece.contains(n)) {
                viol(r, t, p, E_FRANCAISE, "");
            }
        }
    }
    r.notes.push(format!(
        "(e) guillemets droits et apostrophes de citation refusés hors du code ; françaises : \
         {controlees} contrôlée(s), {ecartees} sous {LONGUEUR_MINIMALE} octets (borne) ; \
         {anglaises} anglaise(s) laissée(s) à S-G5"
    ));
}

/// Position d'une apostrophe ouvrante (précédée d'un blanc, d'une parenthèse ou d'un crochet) refermée
/// sur la ligne par une apostrophe qu'aucune lettre ne suit : une élision (`l'acte`) n'ouvre rien.
fn apostrophe_de_citation(ligne: &str) -> Option<usize> {
    let c: Vec<(usize, char)> = ligne.char_indices().collect();
    let lu = |k: usize| c.get(k).map(|x| x.1);
    let apostrophe = |k: usize| matches!(lu(k), Some('\'' | '\u{2018}' | '\u{2019}'));
    let ouvre = |k: usize| {
        let devant =
            k == 0 || lu(k - 1).is_some_and(|p| p.is_whitespace() || "([\u{ab}".contains(p));
        apostrophe(k) && devant && lu(k + 1).is_some_and(|s| !s.is_whitespace())
    };
    let ferme = |k: usize| {
        let derriere = lu(k + 1).is_none_or(|s| !s.is_alphanumeric());
        apostrophe(k) && lu(k - 1).is_some_and(|p| !p.is_whitespace()) && derriere
    };
    let k = (0..c.len()).find(|k| ouvre(*k) && (k + 2..c.len()).any(ferme))?;
    c.get(k).map(|x| x.0)
}

/// Où une citation française de docs/17 doit se trouver : `docs/**/*.md` hors docs/17 et les `.md`
/// de la racine ; un texte de docs/17 ne valide jamais sa propre citation.
fn corpus_francais(r: &mut Rapport, racine: &Path) -> Vec<String> {
    let docs = fichiers_markdown(racine, "docs").fichiers;
    let entrees = std::fs::read_dir(racine).into_iter().flatten().flatten();
    let md = |p: &std::path::PathBuf| p.extension().is_some_and(|e| e == "md");
    let racine_md = entrees.map(|e| e.path()).filter(md);
    let mut pieces = Vec::new();
    for chemin in docs.into_iter().chain(racine_md) {
        let relatif = chemin_relatif(racine, &chemin);
        match std::fs::read_to_string(&chemin) {
            _ if relatif == PERIMETRE => {}
            Ok(texte) => pieces.push(normaliser_pour_recherche(&texte)),
            Err(e) => r.incident(format!("corpus de (e) illisible ({relatif}) : {e}")),
        }
    }
    pieces
}

/// (f) Pièces de l'annexe D.2 d'ADR-0028 (liste fermée à `5afbdd2`) par nom de fichier ou de dossier,
/// séparés par `|` : un nom nu suffit (D.2 n° 8). `SHA256SUMS-cloture-…`, admis, n'y figure pas.
const NOMS_D2: &str = "shogen-j28|baseline_step0|campagne-copie|measure-M009a|measure-m009a|\
    G1-lot-m009|G2-lot-m009|ADR-M002-phase1|campagne.md|_result.json|_workflow-output.json|\
    shogen-campagne|REPAIR-|INCIDENT-|CLOTURE-|J0-STATUS.txt|LISEZ-MOI.txt|ARCHIVE-shogen-interne|\
    AVIS-advisor-2026-09-26|etude-2026-09-25-pocket|PAROXYSME-Shogen.md|M009 measured on S2 traces";
const STATISTIQUES: [&str; 7] = ["z", "K", "k_eff", "φ", "ρ", "P_more", "P̂_more"];

/// (f) Motifs nus du texte entier (casse comprise, ou casse ASCII pliée), avec leur libellé.
fn motifs_f(t: &str) -> Vec<(usize, &'static str)> {
    let bas = t.to_ascii_lowercase();
    let mut trouves = Vec::new();
    for nom in NOMS_D2.split('|') {
        let positions = occurrences_nues(t, nom);
        let libelle = |p| (p, "(f) pièce de D.2 nommée");
        trouves.extend(positions.into_iter().map(libelle));
    }
    for motif in ["%", "pour cent", "pour-cent", "pourcent"] {
        let positions = occurrences_nues(&bas, motif);
        trouves.extend(positions.into_iter().map(|p| (p, "(f) pour-cent")));
    }
    trouves
}

fn controle_f(r: &mut Rapport, t: &str) {
    let mut trouves = motifs_f(t);
    let hexa = |c: char| c.is_ascii_hexdigit();
    for (p, _) in t.match_indices("::") {
        if t[..p].ends_with(hexa) || t[p + 2..].starts_with(hexa) {
            trouves.push((p, "(f) adresse IP"));
        }
    }
    for (p, _) in t.match_indices('@') {
        let queue = &t[p + 1..];
        let fin = queue.find(|c: char| !(c.is_ascii_alphanumeric() || "-.".contains(c)));
        let domaine = queue[..fin.unwrap_or(queue.len())].trim_end_matches('.');
        let fin_de_domaine = domaine.rsplit_once('.').filter(|(d, _)| !d.is_empty());
        let lettres = |x: &str| x.len() > 1 && x.chars().all(|c| c.is_ascii_alphabetic());
        let tld = fin_de_domaine.is_some_and(|x| lettres(x.1));
        if tld && t[..p].ends_with(|c: char| c.is_ascii_alphanumeric()) {
            trouves.push((p, "(f) adresse électronique"));
        }
    }
    for symbole in STATISTIQUES {
        for p in occurrences_nues(t, symbole) {
            let suite = t[p + symbole.len()..].trim_start();
            let signes = ["=", "≈", "<", ">", "≤", "≥"];
            let signe = signes.into_iter().find_map(|s| suite.strip_prefix(s));
            let nombre = signe.map(|s| s.trim_start().trim_start_matches(['-', '−', '+']));
            let chiffre = nombre.is_some_and(|n| n.starts_with(|c: char| c.is_ascii_digit()));
            if chiffre && !mot(avant(t, p)) {
                trouves.push((p, "(f) valeur statistique"));
            }
        }
    }
    for (p, motif) in trouves {
        viol(r, t, p, motif, "");
    }
    r.notes.push(String::from(
        "(f) pièces de D.2 (noms nus compris), pour-cent (signe et lettres), décimaux (hors §, FM-, \
         versions), statistiques, adresses : aucune forme recopiée en sortie",
    ));
}
