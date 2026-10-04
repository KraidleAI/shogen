//! **S-G5 `citations`** — une citation dans `docs/` ou `s2-harness/` doit
//! exister dans le registre bibliographique ou dans les octets détenus.
//!
//! Périmètre : celui de S-G4 (`crate::sg4::PERIMETRE`) — `docs/**/*.md`,
//! puis `s2-harness/**/*.md` depuis le 2026-10-02 (SHOGEN-ORACLE-PERIMETRE-1
//! (i), ADR-0028 annexe B).
//!
//! Ce qu'elle casse (DEVOPS §3) : « une citation entre guillemets dans
//! `docs/` introuvable dans les sidecars de `biblio/` — la règle
//! une-citation-un-grep, mécanisée (précédent : G12 Kraidle, avec sa leçon
//! de couverture) ».
//!
//! **Corpus de recherche, dans l'ordre** : `biblio/INDEX.md` (le registre,
//! committé — il porte verbatim les citations vérifiées), `WISHLIST.md`
//! (les titres de non-détenus y résolvent), puis les octets bruts de tout
//! fichier texte présent dans `biblio/` (HTML, txt, `*.sidecar`). Les PDF
//! ne sont pas greppés par la gate ; leurs octets entrent au corpus via les
//! sidecars régénérables (`just sidecars`, gitignorés) — d'où un corpus
//! local plus large que le corpus CI, et les rares citations que
//! l'extraction perd (ligature sans mapping) vivent à l'INDEX.
//!
//! **La leçon de couverture, assumée en deux régimes** : le régime est
//! détecté en comparant les octets présents au **compte déclaré à
//! l'en-tête d'INDEX** (revue G2 du 2026-08-13, bloquante 1b — l'ancienne
//! détection binaire `0 octet ⇒ partiel` basculait en régime strict sur
//! corpus tronqué). Corpus complet (présents ≥ déclarés, le poste local) :
//! une citation introuvable est une VIOLATION. Corpus incomplet (CI —
//! DEVOPS §1 : les octets ne sont jamais versionnés — ou checkout
//! partiel) : la gate contrôle ce qu'elle peut et **imprime** le ratio et
//! chaque fragment non contrôlé : un contrôle partiel qui se dit partiel,
//! jamais un vert qui prétend couvrir.
//!
//! **Résidu nommé** : la gate vérifie « la citation existe dans le corpus »,
//! pas « la citation est fidèle à sa source » — la fidélité reste
//! l'adjudication de l'orchestrateur au versement (méthodologie doc 03).

use crate::documents::{
    compte_declare_en_tete, fichiers_du_repertoire, fichiers_markdown, normaliser_pour_recherche,
};
use crate::rapport::{Rapport, lire};
use crate::roles::chemin_relatif;
use crate::sg4::PERIMETRE;
use crate::source::ligne_de;
use std::path::Path;

/// Longueur minimale (octets, après normalisation) d'un fragment contrôlé —
/// en dessous, le fragment est trop court pour identifier une source.
pub(crate) const LONGUEUR_MINIMALE: usize = 15;

/// Mots-fonction anglais **forts** (aucun n'est aussi un mot français ni un
/// mot de titre isolé). Un fragment est réputé citation anglaise s'il en
/// contient **au moins deux occurrences** : un seul « of » est un titre
/// d'ouvrage ou une locution — deux mots-fonction, c'est de la prose citée.
/// Ce seuil est une borne de couverture, imprimée : les fragments sous le
/// seuil ne sont PAS contrôlés par la gate.
const MOTS_ANGLAIS: &[&str] = &[
    " the ", " of ", " to ", " is ", " are ", " that ", " not ", " be ", " with ", " it ", " we ",
    " this ", " they ", " has ", " have ",
];

/// Nombre minimal d'occurrences de mots-fonction pour qualifier un fragment.
const OCCURRENCES_MINIMALES: usize = 2;

/// Extensions de `biblio/` lues comme texte pour le grep. Les extensions de
/// code et de manifeste sont entrées avec le corpus amont de la phase A S3
/// (sources Rust épinglées, manifestes, lock, workflow CI) — S-G5 a attrapé
/// leur absence le jour où une ADR a cité `presentation.rs` (2026-08-13).
const EXTENSIONS_TEXTE: &[&str] = &[
    "html", "htm", "txt", "md", "sidecar", "json", "xml", "rs", "toml", "yml", "yaml", "lock",
];

pub fn executer(racine: &Path) -> Rapport {
    let mut rapport = Rapport::nouveau("S-G5", "citations (une-citation-un-grep, mécanisée)");
    // Le périmètre est recensé d'abord : sa couverture s'imprime même quand
    // le registre manque (retour anticipé ci-dessous).
    let mut fichiers = Vec::new();
    for relatif in PERIMETRE {
        let recensement = fichiers_markdown(racine, relatif);
        for incident in recensement.incidents {
            rapport.incident(incident);
        }
        rapport.chemins_couverts.push(format!(
            "{relatif}/**/*.md : {} fichier(s) (extraction des « … » anglais)",
            recensement.fichiers.len()
        ));
        fichiers.extend(recensement.fichiers);
    }
    rapport.presents = fichiers.len();
    rapport.chemins_couverts.push(String::from(
        "corpus : biblio/INDEX.md + octets texte de biblio/ présents",
    ));

    // 1. Le corpus.
    let index = racine.join("biblio").join("INDEX.md");
    let mut corpus = Vec::new();
    let texte_index = match std::fs::read_to_string(&index) {
        Ok(texte) => texte,
        Err(erreur) => {
            rapport.incident(format!(
                "biblio/INDEX.md illisible ({erreur}) — sans registre, aucune citation n'est contrôlable ; la gate refuse de conclure"
            ));
            return rapport;
        }
    };
    corpus.push(normaliser_pour_recherche(&texte_index));
    // WISHLIST.md : le registre des non-détenus — un titre d'ouvrage cité en
    // demande de procurement y résout légitimement.
    if let Ok(texte) = std::fs::read_to_string(racine.join("WISHLIST.md")) {
        corpus.push(normaliser_pour_recherche(&texte));
    }
    let mut octets_presents = 0usize;
    match fichiers_du_repertoire(&racine.join("biblio")) {
        Ok(fichiers) => {
            for chemin in fichiers {
                if chemin == index {
                    continue;
                }
                let extension = chemin
                    .extension()
                    .map(|e| e.to_string_lossy().to_ascii_lowercase())
                    .unwrap_or_default();
                if extension == "sidecar" {
                    // Extraction locale d'un PDF : entre au corpus, ne compte
                    // pas comme artefact (le PDF source compte, lui).
                    if let Ok(brut) = std::fs::read(&chemin) {
                        let texte = String::from_utf8_lossy(&brut);
                        corpus.push(normaliser_pour_recherche(&texte));
                    }
                    continue;
                }
                if !EXTENSIONS_TEXTE
                    .iter()
                    .any(|attendue| *attendue == extension)
                {
                    octets_presents = octets_presents.saturating_add(1); // PDF etc. : présent, non greppable
                    continue;
                }
                match std::fs::read(&chemin) {
                    Ok(brut) => {
                        let texte = String::from_utf8_lossy(&brut);
                        let depagine = retirer_pagination_rfc(&texte);
                        corpus.push(normaliser_pour_recherche(&retirer_balises(&depagine)));
                        octets_presents = octets_presents.saturating_add(1);
                    }
                    Err(erreur) => rapport.incident(format!(
                        "artefact présent mais illisible ({}) : {erreur}",
                        chemin_relatif(racine, &chemin)
                    )),
                }
            }
        }
        Err(erreur) => rapport.incident(erreur),
    }
    // Régime : complet si tous les octets déclarés au registre sont là.
    let declares = compte_declare_en_tete(&texte_index);
    let corpus_incomplet = match declares {
        Some(declares) => octets_presents < declares,
        None => octets_presents == 0,
    };

    // 2. Les citations des documents du périmètre.
    let mut controlees = 0usize;
    let mut ecartes = 0usize;
    let mut non_controlables = Vec::new();
    for chemin in &fichiers {
        let Some(texte) = lire(&mut rapport, racine, chemin) else {
            continue;
        };
        let relatif = chemin_relatif(racine, chemin);
        for (decalage, citation) in citations_francaises(&texte) {
            for fragment in fragments(&citation) {
                let normalise = normaliser_pour_recherche(&fragment);
                // Rognage des bords : une ponctuation de bord appartient à la
                // graphie du document citant (« "time" » vs « "time." » à la
                // source), pas à l'identité de la citation.
                let normalise = normalise
                    .trim_matches(|c: char| !c.is_alphanumeric())
                    .to_string();
                if normalise.len() < LONGUEUR_MINIMALE || !parait_anglais(&normalise) {
                    // Borne de couverture : les fragments courts ou sous le
                    // seuil de langue ne sont pas contrôlés — et ça se compte
                    // (revue G2 du 2026-08-13, majeure 3).
                    ecartes = ecartes.saturating_add(1);
                    continue;
                }
                controlees = controlees.saturating_add(1);
                // Second essai sans tirets ni espaces : l'extraction PDF
                // déshyphène en avalant les tirets réels (« bit-for-bit » →
                // « bit-forbit ») et les RFC en texte césurent les mots en
                // fin de ligne (« case-\ninsensitive » → « case- insensitive »
                // après pli des blancs) — l'identité d'une citation de 15+
                // caractères ne tient ni au tiret ni à l'espace.
                let compacte = |texte: &str| texte.replace(['-', ' '], "");
                let normalise_compacte = compacte(&normalise);
                if corpus.iter().any(|piece| {
                    piece.contains(&normalise) || compacte(piece).contains(&normalise_compacte)
                }) {
                    continue;
                }
                let (ligne, _) = ligne_de(&texte, decalage);
                if corpus_incomplet {
                    non_controlables.push(format!("{relatif}:{ligne} — « {normalise} »"));
                } else {
                    rapport.violation(
                        relatif.clone(),
                        ligne,
                        format!(
                            "citation introuvable dans le registre et les octets détenus : « {normalise} »"
                        ),
                        String::new(),
                    );
                }
            }
        }
    }

    rapport.notes.push(format!(
        "{controlees} fragment(s) de citation contrôlé(s), {ecartes} écarté(s) sous seuil (longueur ou langue — borne de couverture) ; corpus : INDEX + {octets_presents} artefact(s) local(aux) sur {} déclaré(s)",
        declares.map_or_else(|| String::from("?"), |n| n.to_string())
    ));
    if corpus_incomplet {
        rapport.notes.push(format!(
            "CORPUS INCOMPLET ({octets_presents} artefact(s) présent(s) sur {} déclaré(s) — conception DEVOPS §1 en CI, ou checkout partiel) : {} fragment(s) NON contrôlé(s) ici, dus au contrôle sur corpus complet",
            declares.map_or_else(|| String::from("?"), |n| n.to_string()),
            non_controlables.len()
        ));
        for manque in &non_controlables {
            rapport.notes.push(format!("  non contrôlé : {manque}"));
        }
    }
    rapport.notes.push(String::from(
        "résidu : l'existence au corpus est contrôlée, la fidélité à la source reste l'adjudication du versement (doc 03)",
    ));
    rapport
}

/// Extrait les spans « … » d'un texte, avec le décalage d'octet de l'ouvrante.
/// Non imbriqués ; une ouvrante jamais refermée arrête l'extraction (le
/// document malformé est l'affaire de S-G4, qui le signale en incident).
fn citations_francaises(texte: &str) -> Vec<(usize, String)> {
    let mut spans = Vec::new();
    let mut reste = texte;
    let mut base = 0usize;
    while let Some(ouverture) = reste.find('\u{ab}') {
        let apres = ouverture.saturating_add('\u{ab}'.len_utf8());
        let Some(fermeture) = reste.get(apres..).and_then(|suite| suite.find('\u{bb}')) else {
            break;
        };
        let contenu = reste
            .get(apres..apres.saturating_add(fermeture))
            .unwrap_or("");
        spans.push((base.saturating_add(ouverture), contenu.to_string()));
        let suivant = apres
            .saturating_add(fermeture)
            .saturating_add('\u{bb}'.len_utf8());
        base = base.saturating_add(suivant);
        reste = reste.get(suivant..).unwrap_or("");
    }
    spans
}

/// Découpe une citation sur ses marques d'élision (… ou [...]), ses
/// insertions éditoriales ([s], [sic] — courtes, entre crochets) et ses
/// symboles hors alphabet latin étendu (Θ, φ, ≥ — l'extraction PDF ne les
/// rend pas fidèlement) : chaque fragment se cherche séparément — une
/// citation élidée est plusieurs extraits contigus de la source, pas une
/// sous-chaîne unique.
///
/// La typographie (’ “ ”) est pliée AVANT la scission (revue G2 du
/// 2026-08-13, majeure 3 : l'ancien prédicat `> 0x24F` scindait sur une
/// apostrophe courbe et perdait la queue de la citation en silence) ; la
/// scission garde le grec et les symboles (Θ scinde) mais épargne le bloc
/// de ponctuation générale U+2000–U+206F (tirets cadratins, guillemets —
/// symétriques entre aiguille et corpus, ils se cherchent tels quels).
fn fragments(citation: &str) -> Vec<String> {
    let pliee: String = citation
        .chars()
        .map(|c| match c {
            // Le même pli que `normaliser_pour_recherche` — aiguille et
            // corpus doivent plier pareil, sinon le pli crée le mismatch.
            '\u{2018}' | '\u{2019}' => '\'',
            '\u{201c}' | '\u{201d}' => '"',
            autre => autre,
        })
        .collect();
    let preparee = pliee
        .replace("[\u{2026}]", "\u{2026}")
        .replace("[...]", "\u{2026}")
        .replace("...", "\u{2026}");
    let sans_crochets = scinder_crochets(&preparee);
    sans_crochets
        .split(|c: char| {
            let point = c as u32;
            c == '\u{2026}' || (point > 0x24F && !(0x2000..0x2070).contains(&point))
        })
        .map(str::to_string)
        .collect()
}

/// Remplace toute insertion éditoriale courte `[…]` (≤ 30 octets) par une
/// marque d'élision — « determine[s] the extent » se cherche en deux
/// fragments, sans exiger de la source une graphie qu'elle n'a pas.
fn scinder_crochets(texte: &str) -> String {
    let mut sortie = String::with_capacity(texte.len());
    let mut reste = texte;
    while let Some(ouverture) = reste.find('[') {
        let (avant, apres) = reste.split_at(ouverture);
        sortie.push_str(avant);
        match apres.get(1..).and_then(|suite| suite.find(']')) {
            Some(fermeture) if fermeture <= 30 => {
                sortie.push('\u{2026}');
                reste = apres.get(fermeture.saturating_add(2)..).unwrap_or("");
            }
            _ => {
                sortie.push('[');
                reste = apres.get(1..).unwrap_or("");
            }
        }
    }
    sortie.push_str(reste);
    sortie
}

/// Retire la pagination des RFC en texte brut : le pied « […] [Page N] »,
/// l'en-tête « RFC NNNN … 20NN » et les sauts de page interrompent des
/// phrases en plein milieu (constaté : RFC 3986 §6.2.3, coupée par la
/// page 41 dans une citation d'ADR-0016). Appliqué au corpus seulement.
fn retirer_pagination_rfc(texte: &str) -> String {
    texte
        .lines()
        .filter(|ligne| {
            let net = ligne.trim_end();
            let pied = net.ends_with(']')
                && net.contains("[Page ")
                && (net.contains("Standards Track") || net.contains("Informational"));
            let entete = net.starts_with("RFC ")
                && net.len() > 40
                && net
                    .rsplit(' ')
                    .next()
                    .is_some_and(|fin| fin.len() == 4 && fin.chars().all(|c| c.is_ascii_digit()));
            !(pied || entete || net.contains('\u{c}'))
        })
        .collect::<Vec<_>>()
        .join("\n")
}

/// Retire les balises `<…>` d'un texte de corpus HTML : une citation d'une
/// page détenue traverse souvent une balise d'emphase en plein milieu de
/// phrase. Appliqué au corpus seulement — jamais aux aiguilles.
fn retirer_balises(texte: &str) -> String {
    let mut sortie = String::with_capacity(texte.len());
    let mut reste = texte;
    while let Some(ouverture) = reste.find('<') {
        let (avant, apres) = reste.split_at(ouverture);
        sortie.push_str(avant);
        match apres.get(1..).and_then(|suite| suite.find('>')) {
            Some(fermeture) if fermeture <= 300 => {
                reste = apres.get(fermeture.saturating_add(2)..).unwrap_or("");
            }
            _ => {
                sortie.push('<');
                reste = apres.get(1..).unwrap_or("");
            }
        }
    }
    sortie.push_str(reste);
    sortie
}

/// Heuristique de langue : le corpus détenu est anglophone ; un fragment
/// sous `OCCURRENCES_MINIMALES` mots-fonction anglais est de la prose ou un
/// titre du projet, hors périmètre (borne de couverture, imprimée en note).
pub(crate) fn parait_anglais(fragment: &str) -> bool {
    let bas = format!(" {} ", fragment.to_ascii_lowercase());
    let occurrences: usize = MOTS_ANGLAIS
        .iter()
        .map(|mot| bas.matches(mot).count())
        .sum();
    occurrences >= OCCURRENCES_MINIMALES
}
