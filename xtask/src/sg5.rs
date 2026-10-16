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
//! **Texte affiché** (lot DETTES-T15, SHOGEN-SG5-COMMENTAIRE-HTML-1 ; DT15-g) :
//! une page HTML ou Markdown entre au corpus sans ce qu'elle ne donne jamais à
//! lire — commentaires `<!-- … -->` et factices (`<!…>`, `</…>`, DT15-h),
//! instructions de traitement (`<?…>`, DT15-h), contenu des éléments `script`
//! et `style` —, ôté avant le débalisage : une
//! citation d'un texte retiré d'une page, resté en commentaire ou dans un
//! script, est introuvable.
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
//!
//! **Emplacements interdits** (lot SG5-INTERDITS, 2026-10-04 ;
//! SHOGEN-SG5-NOTES-INTERDITS-1, ADR-0028 annexe B.51) : une citation
//! introuvable située sous `EMPLACEMENTS_INTERDITS` se rapporte par
//! `chemin:ligne` seul, en note comme en violation, jamais par son texte.
//! Verdict et comptes n'en dépendent pas. Limites : le masque ne couvre que
//! S-G5 (S-G4 imprime encore la ligne en extrait) ; un emplacement absent de
//! la liste, ou atteint par un lien symbolique, imprime son texte. Casse pliée
//! et composants `.jsonl` : DT4-f (DETTES-T4).

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

/// Extensions des pages rendues (HTML, et Markdown, dont le rendu cache aussi
/// ces constructions) : ce qu'elles ne donnent jamais à lire sort du corpus
/// (`retirer_non_affiche`). Ailleurs (texte brut, code, données), `<` n'ouvre
/// rien.
const EXTENSIONS_RENDUES: &[&str] = &["html", "htm", "md"];

/// Les emplacements interdits de lecture, liste du brief du lot SG5-INTERDITS
/// (G0 `docs/adr-0029/G0-lots-S2BIS.md`) : préfixes exacts de chemin relatif,
/// séparateur `/` (invariant 1 d'ADR-0013). `docs/15-` et `docs/16-` couvrent
/// fichier ou dossier ; les autres finissent par `/`. `docs/adr-0028/execution/`
/// ajouté par DETTES-T4 (DT4-b, adjudication Q-3) : interdit par les briefs de ce lot.
pub(crate) const EMPLACEMENTS_INTERDITS: &[&str] = &[
    "docs/15-",
    "docs/16-",
    "docs/pocket-report/",
    "docs/rapports/",
    "docs/adr-0025/",
    "docs/adr-0028/monark-m009a/",
    "docs/adr-0028/execution/",
];

/// Vrai si `relatif` (chemin relatif, séparateur `/`) est sous un emplacement
/// interdit : ses citations se rapportent par `chemin:ligne` seul. DT4-f
/// (DETTES-T4, C-9) : comparaison sur le chemin plié en casse (majuscules puis
/// minuscules, au plus près d'un système de fichiers insensible à la casse), et
/// tout composant qui finit en `.jsonl`, dossier compris, est interdit.
pub(crate) fn emplacement_interdit(relatif: &str) -> bool {
    let plie = relatif.to_uppercase().to_lowercase();
    EMPLACEMENTS_INTERDITS
        .iter()
        .any(|prefixe| plie.starts_with(prefixe))
        || plie
            .split('/')
            .any(|composant| composant.ends_with(".jsonl"))
}

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
                        let brut = String::from_utf8_lossy(&brut);
                        let texte = if EXTENSIONS_RENDUES.contains(&extension.as_str()) {
                            retirer_non_affiche(&brut)
                        } else {
                            brut.into_owned()
                        };
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
    let mut masques = 0usize;
    let mut non_controlables = Vec::new();
    for chemin in &fichiers {
        let Some(texte) = lire(&mut rapport, racine, chemin) else {
            continue;
        };
        let relatif = chemin_relatif(racine, chemin);
        let interdit = emplacement_interdit(&relatif);
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
                // Emplacement interdit : `chemin:ligne` seul, jamais le texte
                // (SHOGEN-SG5-NOTES-INTERDITS-1) ; le verdict est le même.
                if interdit {
                    masques = masques.saturating_add(1);
                }
                if corpus_incomplet {
                    non_controlables.push(if interdit {
                        format!("{relatif}:{ligne}")
                    } else {
                        format!("{relatif}:{ligne} — « {normalise} »")
                    });
                } else {
                    let motif = if interdit {
                        String::from(
                            "citation introuvable dans le registre et les octets détenus (emplacement interdit : texte jamais imprimé)",
                        )
                    } else {
                        format!(
                            "citation introuvable dans le registre et les octets détenus : « {normalise} »"
                        )
                    };
                    rapport.violation(relatif.clone(), ligne, motif, String::new());
                }
            }
        }
    }

    rapport.notes.push(format!(
        "{controlees} fragment(s) de citation contrôlé(s), {ecartes} écarté(s) sous seuil (longueur ou langue — borne de couverture) ; corpus : INDEX + {octets_presents} artefact(s) local(aux) sur {} déclaré(s)",
        declares.map_or_else(|| String::from("?"), |n| n.to_string())
    ));
    rapport.notes.push(format!(
        "emplacements interdits (SHOGEN-SG5-NOTES-INTERDITS-1) : {masques} fragment(s) introuvable(s) rapporté(s) par chemin:ligne seul, texte jamais imprimé ; verdict inchangé"
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

/// Ôte d'une page ce qu'elle ne donne jamais à lire, en un balayage de gauche
/// à droite comme la tokenisation HTML (WHATWG) : commentaires
/// (SHOGEN-SG5-COMMENTAIRE-HTML-1), commentaires factices et instructions de
/// traitement (DT15-h), éléments `script` et `style` jusqu'à la fermante qui
/// les clôt (DT15-g). Une balise
/// ordinaire est recopiée entière pour le débalisage : ce qu'écrit une valeur
/// d'attribut n'ouvre rien (DT15-k) ; le contenu d'un élément de texte brut
/// (`TEXTE_BRUT`) est recopié tel quel : un `<!--` ou un `<script` écrit dans un
/// `title` ou un `textarea` n'ouvre rien (relecture G2, C-6). Ce qu'un script
/// ou une interaction peut montrer (`template`, `noscript`, attribut `hidden`,
/// CSS) reste. Lecture sans analyseur : texte ôté en trop (bloc de code
/// Markdown, balise écrite dans un `textarea`), jamais gardé en trop, hors de
/// deux cas. Un contenu SVG ou MathML, lu ici comme du HTML : un `</script` ou
/// un `</style` écrit dans un commentaire, une section CDATA ou une valeur
/// d'attribut à l'intérieur d'un tel script ou style l'y clôt trop tôt. Un
/// ouvreur écrit dans un extrait ou un bloc de code Markdown, que le rendu
/// affiche, et dont la fin tomberait dans une construction vraie. Temps linéaire.
/// Appliqué au corpus seulement, avant le débalisage.
fn retirer_non_affiche(texte: &str) -> String {
    let mut sortie = String::with_capacity(texte.len());
    let mut reste = texte;
    let mut etranger = 0usize;
    while let Some(ouverture) = reste.find('<') {
        sortie.push_str(reste.get(..ouverture).unwrap_or(""));
        let suite = reste.get(ouverture..).unwrap_or("");
        let (gardee, longueur) = match longueur_non_affichee(suite) {
            Some(longueur) => (0, longueur),
            None => {
                let lue = longueur_de_balise(suite.as_bytes()).unwrap_or(1);
                let longueur = lue.saturating_add(texte_brut(suite.as_bytes(), lue, &mut etranger));
                (longueur, longueur)
            }
        };
        sortie.push_str(suite.get(..gardee).unwrap_or(""));
        reste = suite.get(longueur..).unwrap_or("");
    }
    sortie.push_str(reste);
    sortie
}

/// Éléments dont la construction de l'arbre bascule la tokenisation (WHATWG,
/// algorithmes « generic RCDATA » et « generic raw text ») : RCDATA (`title`,
/// `textarea`) et RAWTEXT (`xmp`, `iframe`, `noembed`, `noframes`) jusqu'à leur
/// fermante, PLAINTEXT (`plaintext`) jusqu'au bout du texte. Leur contenu est du
/// texte : ni commentaire ni script n'y commence. `noscript` reste lu comme du
/// balisage (lecture sans script, celle qui l'affiche).
const TEXTE_BRUT: [&str; 7] = [
    "<title",
    "<textarea",
    "<xmp",
    "<iframe",
    "<noembed",
    "<noframes",
    "<plaintext",
];

/// Longueur du contenu de texte brut qui suit une balise `TEXTE_BRUT` longue de
/// `lue` octets (relecture G2 de DETTES-T15, C-6) ; 0 après toute autre balise,
/// et dans un contenu `svg` ou `math` (profondeur `etranger`, tenue ici), où ces
/// éléments ne basculent pas la tokenisation.
fn texte_brut(t: &[u8], lue: usize, etranger: &mut usize) -> usize {
    let auto_fermee = t.get(..lue).is_some_and(|b| b.ends_with(b"/>"));
    if balise(t, 0, "<svg") || balise(t, 0, "<math") {
        *etranger = etranger.saturating_add(usize::from(!auto_fermee));
        return 0;
    }
    if balise(t, 0, "</svg") || balise(t, 0, "</math") {
        *etranger = etranger.saturating_sub(1);
        return 0;
    }
    let Some(nom) = TEXTE_BRUT
        .iter()
        .find(|nom| *etranger == 0 && balise(t, 0, nom))
    else {
        return 0;
    };
    let fermante = format!("</{}", nom.get(1..).unwrap_or(""));
    let fin = if *nom == "<plaintext" {
        t.len()
    } else {
        (lue..t.len())
            .find(|i| balise(t, *i, &fermante))
            .unwrap_or(t.len())
    };
    fin.saturating_sub(lue)
}

/// Longueur, depuis son `<`, d'une construction jamais affichée (jusqu'au bout
/// du texte si elle ne se ferme pas) ; `None` pour une balise ou un `<` de texte.
fn longueur_non_affichee(suite: &str) -> Option<usize> {
    if let Some(corps) = suite.strip_prefix("<!--") {
        return Some(fin_de_commentaire(corps).saturating_add(4));
    }
    // Commentaire factice (DT15-h) : `<!` sans `--`, ou `</` suivi d'un
    // caractère qui n'est ni une lettre ASCII ni `>` ; instruction de traitement :
    // `<?` (tokenisation WHATWG du 2026-10-14, 13.2.5.72 à 13.2.5.76 ; commentaire
    // factice si sa cible est invalide, `xml` ou `xml-stylesheet`). Tous clos au
    // premier `>`, jusqu'au bout du texte sans lui.
    let fermante_factice = suite.strip_prefix("</").and_then(|r| r.chars().next());
    let factice = suite.starts_with("<!")
        || suite.starts_with("<?")
        || fermante_factice.is_some_and(|c| !c.is_ascii_alphabetic() && c != '>');
    if factice {
        return Some(suite.find('>').map_or(suite.len(), |q| q.saturating_add(1)));
    }
    [("<script", "</script"), ("<style", "</style")]
        .into_iter()
        .find(|(ouvrante, _)| balise(suite.as_bytes(), 0, ouvrante))
        .map(|(ouvrante, fermante)| fin_d_element(suite, ouvrante, fermante))
}

/// Fin d'un commentaire, dans son corps : `>` ou `->` tout de suite
/// (commentaire vide), sinon le premier `--` suivi de `>` ou de `!>` ; sans
/// fin, le bout du texte. Un seul passage sur le corps.
fn fin_de_commentaire(corps: &str) -> usize {
    if corps.starts_with('>') {
        return 1;
    }
    if corps.starts_with("->") {
        return 2;
    }
    let mut depuis = 0usize;
    while let Some(p) = corps.get(depuis..).and_then(|r| r.find("--")) {
        let tirets = depuis.saturating_add(p);
        let apres = corps.get(tirets.saturating_add(2)..).unwrap_or("");
        if apres.starts_with('>') {
            return tirets.saturating_add(3);
        }
        if apres.starts_with("!>") {
            return tirets.saturating_add(4);
        }
        depuis = tirets.saturating_add(1);
    }
    corps.len()
}

/// Vrai si `t` porte en `i` le `motif` (`<script`, `</style`…, casse ASCII
/// ignorée) suivi d'un blanc, de `/`, de `>` ou de la fin du texte.
fn balise(t: &[u8], i: usize, motif: &str) -> bool {
    let fin = i.saturating_add(motif.len());
    t.get(i..fin)
        .is_some_and(|lu| lu.eq_ignore_ascii_case(motif.as_bytes()))
        && t.get(fin).is_none_or(|o| b"\t\n\x0c\r />".contains(o))
}

/// Fin d'un élément `script` ou `style`, depuis son `<` : après la fermante
/// qui le clôt, sinon le bout du texte. `style` se clôt à sa première
/// fermante ; `script` suit les états de la tokenisation : après `<!--`, un
/// `<script` fait ignorer les fermantes jusqu'à `-->`. Ouvrante et fermante
/// se lisent jusqu'à leur vrai `>` (`fin_de_balise`, DT15-j).
fn fin_d_element(suite: &str, ouvrante: &str, fermante: &str) -> usize {
    let t = suite.as_bytes();
    let script = ouvrante == "<script";
    let mut i = fin_de_balise(t, ouvrante.len());
    let mut etat = 0u8; // 0 : données ; 1 : échappé, après `<!--` ; 2 : doublement échappé
    while i < t.len() {
        if script && etat > 0 && t.get(i..i.saturating_add(3)) == Some(b"-->".as_slice()) {
            etat = 0;
        } else if balise(t, i, fermante) {
            if etat < 2 {
                return fin_de_balise(t, i.saturating_add(fermante.len()));
            }
            etat = 1;
        } else if script && etat == 0 && t.get(i..i.saturating_add(4)) == Some(b"<!--".as_slice()) {
            etat = 1;
            i = i.saturating_add(2);
            continue;
        } else if script && etat == 1 && balise(t, i, "<script") {
            etat = 2;
        }
        i = i.saturating_add(1);
    }
    t.len()
}

/// Fin d'une balise ouvrante ou fermante, depuis son nom ou l'octet qui le
/// suit : après le `>` qui la clôt hors des valeurs d'attribut entre
/// guillemets, selon les états de la balise dans la tokenisation (nom,
/// attribut, valeur) ; sans ce `>`, le bout du texte, qu'une balise inachevée
/// n'affiche pas (DT15-j ; toute balise depuis DT15-k).
fn fin_de_balise(t: &[u8], depuis: usize) -> usize {
    #[derive(Clone, Copy)]
    enum Etat {
        Nom,
        AvantAttribut,
        Attribut,
        ApresAttribut,
        AvantValeur,
        Valeur,
    }
    let mut etat = Etat::Nom;
    let mut i = depuis;
    while let Some(&o) = t.get(i) {
        let blanc = o.is_ascii_whitespace();
        etat = match (etat, o) {
            (_, b'>') => return i.saturating_add(1),
            (Etat::AvantValeur, b'"' | b'\'') => {
                let valeur = t.get(i.saturating_add(1)..).unwrap_or_default();
                let Some(q) = valeur.iter().position(|&x| x == o) else {
                    return t.len();
                };
                i = i.saturating_add(q).saturating_add(1);
                Etat::AvantAttribut
            }
            (Etat::AvantValeur, _) if blanc => Etat::AvantValeur,
            (Etat::AvantValeur | Etat::Valeur, _) if !blanc => Etat::Valeur,
            (Etat::Valeur, _) => Etat::AvantAttribut,
            (_, b'/') => Etat::AvantAttribut,
            (Etat::Attribut | Etat::ApresAttribut, b'=') => Etat::AvantValeur,
            (Etat::Attribut | Etat::ApresAttribut, _) if blanc => Etat::ApresAttribut,
            (Etat::Nom, _) if !blanc => Etat::Nom,
            (_, _) if blanc => Etat::AvantAttribut,
            (_, _) => Etat::Attribut,
        };
        i = i.saturating_add(1);
    }
    t.len()
}

/// Retire les balises d'un texte de corpus : une citation d'une page détenue
/// traverse souvent une balise d'emphase en plein milieu de phrase. Une balise
/// est lue entière (`longueur_de_balise`), sans borne de longueur : le texte
/// de ses attributs ne reste jamais au corpus (DT15-k, Q-8) ; tout autre `<`
/// est du texte. Chaque octet est lu une fois : temps linéaire (Q-9). Appliqué
/// au corpus seulement — jamais aux aiguilles.
fn retirer_balises(texte: &str) -> String {
    let mut sortie = String::with_capacity(texte.len());
    let mut reste = texte;
    while let Some(ouverture) = reste.find('<') {
        sortie.push_str(reste.get(..ouverture).unwrap_or(""));
        let suite = reste.get(ouverture..).unwrap_or("");
        let longueur = longueur_de_balise(suite.as_bytes());
        if longueur.is_none() {
            sortie.push('<');
        }
        reste = suite.get(longueur.unwrap_or(1)..).unwrap_or("");
    }
    sortie.push_str(reste);
    sortie
}

/// Longueur, depuis son `<`, d'une balise que la tokenisation HTML lit comme
/// telle : `<` ou `</` suivi d'une lettre ASCII, jusqu'à son vrai `>`
/// (`fin_de_balise`), ou `</>`, qu'elle ignore ; `None` pour un `<` de texte.
fn longueur_de_balise(suite: &[u8]) -> Option<usize> {
    let lettre = |o: Option<&u8>| o.is_some_and(u8::is_ascii_alphabetic);
    if lettre(suite.get(1)) {
        Some(fin_de_balise(suite, 1))
    } else if suite.get(1) == Some(&b'/') && lettre(suite.get(2)) {
        Some(fin_de_balise(suite, 2))
    } else if suite.get(1..3) == Some(b"/>".as_slice()) {
        Some(3)
    } else {
        None
    }
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
