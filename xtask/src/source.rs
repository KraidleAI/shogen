//! Lecture de source Rust pour les gates lexicales.
//!
//! Deux régimes, et la distinction est une décision, pas un détail :
//!
//! * **texte brut** — S-G1 (noms de transport) scanne TOUT, commentaires et
//!   littéraux compris : un commentaire qui nomme un transport dans le cœur
//!   viole ADR-0001 (« le vocabulaire de faits de Shōgen ne nomme aucun
//!   transport ») exactement comme du code ;
//! * **code seul** — S-G3 (formes qui paniquent, indexation, arithmétique)
//!   scanne le code débarrassé des commentaires et des littéraux : sinon la
//!   phrase « n'utilisez jamais `unwrap()` » dans un commentaire rendrait la
//!   gate rouge, et la gate serait désarmée par ses propres faux positifs.
//!
//! `code_seul` préserve les positions d'octet et les fins de ligne : le numéro
//! de ligne rapporté est celui du fichier réel.

/// Vrai si l'octet peut faire partie d'un identifiant Rust ASCII.
pub fn est_caractere_de_mot(octet: u8) -> bool {
    octet.is_ascii_alphanumeric() || octet == b'_'
}

fn octet_a(octets: &[u8], index: usize) -> u8 {
    octets.get(index).copied().unwrap_or(0)
}

/// Remplace commentaires (ligne, bloc imbriqué, doc) et littéraux (texte, texte
/// brut, octets, caractère) par des espaces, en conservant longueur et sauts de
/// ligne.
pub fn code_seul(source: &str) -> String {
    let octets = source.as_bytes();
    let mut sortie = octets.to_vec();
    let taille = octets.len();
    let mut index = 0usize;

    let blanchir = |sortie: &mut Vec<u8>, debut: usize, fin: usize| {
        let mut position = debut;
        while position < fin {
            if let Some(case) = sortie.get_mut(position)
                && *case != b'\n'
                && *case != b'\r'
            {
                *case = b' ';
            }
            position = position.saturating_add(1);
        }
    };

    while index < taille {
        let courant = octet_a(octets, index);
        let suivant = octet_a(octets, index.saturating_add(1));

        // Commentaire de ligne (y compris /// et //!)
        if courant == b'/' && suivant == b'/' {
            let mut fin = index;
            while fin < taille && octet_a(octets, fin) != b'\n' {
                fin = fin.saturating_add(1);
            }
            blanchir(&mut sortie, index, fin);
            index = fin;
            continue;
        }

        // Commentaire de bloc, imbriqué
        if courant == b'/' && suivant == b'*' {
            let debut = index;
            let mut profondeur = 1usize;
            let mut position = index.saturating_add(2);
            while position < taille && profondeur > 0 {
                let a = octet_a(octets, position);
                let b = octet_a(octets, position.saturating_add(1));
                if a == b'/' && b == b'*' {
                    profondeur = profondeur.saturating_add(1);
                    position = position.saturating_add(2);
                } else if a == b'*' && b == b'/' {
                    profondeur = profondeur.saturating_sub(1);
                    position = position.saturating_add(2);
                } else {
                    position = position.saturating_add(1);
                }
            }
            blanchir(&mut sortie, debut, position.min(taille));
            index = position.min(taille);
            continue;
        }

        // Chaîne brute : r"..." ou r#"..."#  (et b prefix : br"...")
        if (courant == b'r' || courant == b'b')
            && !(index > 0 && est_caractere_de_mot(octet_a(octets, index.saturating_sub(1))))
        {
            let mut position = index.saturating_add(1);
            if courant == b'b' && octet_a(octets, position) == b'r' {
                position = position.saturating_add(1);
            }
            if courant == b'r' || octet_a(octets, index.saturating_add(1)) == b'r' {
                let mut dieses = 0usize;
                while octet_a(octets, position) == b'#' {
                    dieses = dieses.saturating_add(1);
                    position = position.saturating_add(1);
                }
                if octet_a(octets, position) == b'"' {
                    let debut = index;
                    position = position.saturating_add(1);
                    'brute: while position < taille {
                        if octet_a(octets, position) == b'"' {
                            let mut fermeture = position.saturating_add(1);
                            let mut comptes = 0usize;
                            while comptes < dieses && octet_a(octets, fermeture) == b'#' {
                                comptes = comptes.saturating_add(1);
                                fermeture = fermeture.saturating_add(1);
                            }
                            if comptes == dieses {
                                position = fermeture;
                                break 'brute;
                            }
                        }
                        position = position.saturating_add(1);
                    }
                    blanchir(&mut sortie, debut, position.min(taille));
                    index = position.min(taille);
                    continue;
                }
            }
        }

        // Chaîne ordinaire (et b"...")
        if courant == b'"' {
            let debut = index;
            let mut position = index.saturating_add(1);
            while position < taille {
                let a = octet_a(octets, position);
                if a == b'\\' {
                    position = position.saturating_add(2);
                    continue;
                }
                if a == b'"' {
                    position = position.saturating_add(1);
                    break;
                }
                position = position.saturating_add(1);
            }
            blanchir(&mut sortie, debut, position.min(taille));
            index = position.min(taille);
            continue;
        }

        // Littéral de caractère vs durée de vie ('a) : on ne blanchit que si une
        // apostrophe fermante est trouvée à courte distance.
        if courant == b'\'' {
            if let Some(fin) = fin_de_litteral_caractere(octets, index) {
                blanchir(&mut sortie, index, fin);
                index = fin;
                continue;
            }
            index = index.saturating_add(1);
            continue;
        }

        index = index.saturating_add(1);
    }

    String::from_utf8_lossy(&sortie).into_owned()
}

fn fin_de_litteral_caractere(octets: &[u8], debut: usize) -> Option<usize> {
    let apres = debut.saturating_add(1);
    if octet_a(octets, apres) == b'\\' {
        let mut position = apres.saturating_add(1);
        let borne = debut.saturating_add(10);
        while position < octets.len() && position < borne {
            if octet_a(octets, position) == b'\'' {
                return Some(position.saturating_add(1));
            }
            position = position.saturating_add(1);
        }
        return None;
    }
    let premier = octet_a(octets, apres);
    if premier == 0 {
        return None;
    }
    if premier.is_ascii() {
        // Caractère ASCII : la quote fermante ne peut être qu'immédiatement
        // après. Sans cette borne, `Foo<'a, 'b>` serait pris pour un littéral.
        if octet_a(octets, apres.saturating_add(1)) == b'\'' {
            return Some(apres.saturating_add(2));
        }
        return None;
    }
    // Caractère non ASCII : de 2 à 4 octets, tous des continuations UTF-8.
    let mut position = apres.saturating_add(1);
    let borne = apres.saturating_add(4);
    while position < octets.len() && position <= borne {
        let courant = octet_a(octets, position);
        if courant == b'\'' {
            return Some(position.saturating_add(1));
        }
        if courant < 0x80 {
            return None;
        }
        position = position.saturating_add(1);
    }
    None
}

/// Occurrences d'un motif **bornées par des non-mots** (ni avant ni après un
/// caractère d'identifiant), insensibles à la casse.
///
/// C'est ce qui distingue `tee` (nom de transport) de `committee`, et
/// `assert!` de `debug_assert!`.
pub fn occurrences_bornees(texte: &str, motif: &str) -> Vec<usize> {
    let bas = texte.to_ascii_lowercase();
    let motif_bas = motif.to_ascii_lowercase();
    let octets = bas.as_bytes();
    let motif_octets = motif_bas.as_bytes();
    let mut trouvees = Vec::new();
    if motif_octets.is_empty() {
        return trouvees;
    }
    let mut depart = 0usize;
    while let Some(position) = bas.get(depart..).and_then(|reste| reste.find(&motif_bas)) {
        let absolue = depart.saturating_add(position);
        let fin = absolue.saturating_add(motif_octets.len());
        let avant_est_mot = absolue > 0
            && est_caractere_de_mot(octet_a(octets, absolue.saturating_sub(1)))
            && est_caractere_de_mot(octet_a(octets, absolue));
        let apres_est_mot = fin < octets.len()
            && est_caractere_de_mot(octet_a(octets, fin))
            && est_caractere_de_mot(octet_a(octets, fin.saturating_sub(1)));
        if !avant_est_mot && !apres_est_mot {
            trouvees.push(absolue);
        }
        depart = absolue.saturating_add(1);
    }
    trouvees
}

/// Occurrences d'un motif **sans** condition de bornage (sous-chaîne nue).
pub fn occurrences_nues(texte: &str, motif: &str) -> Vec<usize> {
    let mut trouvees = Vec::new();
    if motif.is_empty() {
        return trouvees;
    }
    let mut depart = 0usize;
    while let Some(position) = texte.get(depart..).and_then(|reste| reste.find(motif)) {
        let absolue = depart.saturating_add(position);
        trouvees.push(absolue);
        depart = absolue.saturating_add(1);
    }
    trouvees
}

/// Numéro de ligne (1-based) et contenu de la ligne, pour un décalage d'octet.
pub fn ligne_de(texte: &str, decalage: usize) -> (usize, String) {
    let mut numero = 1usize;
    let mut debut_ligne = 0usize;
    for (index, caractere) in texte.char_indices() {
        if index >= decalage {
            break;
        }
        if caractere == '\n' {
            numero = numero.saturating_add(1);
            debut_ligne = index.saturating_add(1);
        }
    }
    let reste = texte.get(debut_ligne..).unwrap_or("");
    let contenu = match reste.find('\n') {
        Some(fin) => reste.get(..fin).unwrap_or(reste),
        None => reste,
    };
    (numero, contenu.trim().to_string())
}
