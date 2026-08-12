//! Sous-ensemble **canonique minimal** de CBOR, écrit à la main.
//!
//! ADR-0002 : « Payloads en CBOR contraint aux **Core Deterministic Encoding
//! Requirements** de RFC 8949 ». Ce module n'implémente que le fragment
//! nécessaire au témoignage trivial du walking skeleton (12 §5) :
//!
//! * entiers non signés (type majeur 0) en **sérialisation préférée** (forme la
//!   plus courte) ;
//! * chaînes d'octets (type majeur 2) et de texte (type majeur 3), **longueur
//!   définie** uniquement ;
//! * cartes (type majeur 5), longueur définie, **clés triées** par ordre
//!   lexicographique des octets de leur encodage, sans doublon.
//!
//! Ce qui n'est **pas** couvert est refusé, jamais toléré : entiers négatifs,
//! tableaux, étiquettes, flottants, valeurs simples, longueurs indéfinies.
//! Choisir une crate CBOR réelle est un travail S3 sous R-8, pas de S2.5 :
//! aucune dépendance n'est introduite ici (ADR-0012 D3, D5).
//!
//! **Décodeur strict par décision** : il n'accepte que la forme canonique. C'est
//! ce qui rend vraie la seconde moitié de la propriété (a) d'ADR-0011 —
//! `encode(decode(b)) == b` pour tout `b` accepté.

use crate::erreur::ErreurDecodage;

/// Masque des trois bits de type majeur.
const MASQUE_MAJEUR: u8 = 0xE0;
/// Masque des cinq bits d'information additionnelle.
const MASQUE_INFORMATION: u8 = 0x1F;

/// Préfixe du type majeur 0 — entier non signé.
pub(crate) const PREFIXE_UINT: u8 = 0x00;
/// Préfixe du type majeur 2 — chaîne d'octets.
pub(crate) const PREFIXE_OCTETS: u8 = 0x40;
/// Préfixe du type majeur 3 — chaîne de texte.
pub(crate) const PREFIXE_TEXTE: u8 = 0x60;
/// Préfixe du type majeur 5 — carte.
pub(crate) const PREFIXE_CARTE: u8 = 0xA0;

/// Seuil au-delà duquel l'argument ne tient plus dans les cinq bits.
const ARGUMENT_DIRECT_MAX: u64 = 23;
/// Valeurs d'information annonçant 1, 2, 4 et 8 octets d'argument.
const INFO_UN_OCTET: u8 = 24;
const INFO_DEUX_OCTETS: u8 = 25;
const INFO_QUATRE_OCTETS: u8 = 26;
const INFO_HUIT_OCTETS: u8 = 27;
/// Valeur d'information de la longueur indéfinie.
const INFO_INDEFINIE: u8 = 31;

/// Tronque sans perte : l'appelant garantit par sa branche que `v <= 0xFF`.
fn octet_bas(v: u64) -> u8 {
    (v & 0xFF) as u8
}

/// Écrit un en-tête (préfixe de type majeur + argument) en sérialisation
/// préférée : la forme la plus courte, exigée par le sous-ensemble canonique.
///
/// Totale : définie pour tout `u64`, sans allocation dimensionnée par une
/// donnée d'entrée, sans panique.
pub(crate) fn ecrire_entete(sortie: &mut Vec<u8>, prefixe: u8, argument: u64) {
    if argument <= ARGUMENT_DIRECT_MAX {
        sortie.push(prefixe | octet_bas(argument));
    } else if argument <= u64::from(u8::MAX) {
        sortie.push(prefixe | INFO_UN_OCTET);
        sortie.push(octet_bas(argument));
    } else if argument <= u64::from(u16::MAX) {
        sortie.push(prefixe | INFO_DEUX_OCTETS);
        sortie.extend_from_slice(&((argument & 0xFFFF) as u16).to_be_bytes());
    } else if argument <= u64::from(u32::MAX) {
        sortie.push(prefixe | INFO_QUATRE_OCTETS);
        sortie.extend_from_slice(&((argument & 0xFFFF_FFFF) as u32).to_be_bytes());
    } else {
        sortie.push(prefixe | INFO_HUIT_OCTETS);
        sortie.extend_from_slice(&argument.to_be_bytes());
    }
}

/// Convertit une longueur de mémoire en argument CBOR.
///
/// La branche `Err` est inatteignable sur toute cible où `usize <= u64` (toutes
/// celles que la toolchain épinglée sert). Si elle l'était, l'encodage produit
/// serait **rejeté par notre propre décodeur** — un refus, jamais une panique.
pub(crate) fn argument_de_longueur(longueur: usize) -> u64 {
    // `unwrap_or` est total (aucune panique possible) : c'est la valeur de
    // repli, pas un `unwrap`. Le repli `u64::MAX` produirait un en-tête que
    // notre propre décodeur refuse — fail-closed jusque dans l'inatteignable.
    u64::try_from(longueur).unwrap_or(u64::MAX)
}

/// Écrit une chaîne de texte (type majeur 3), longueur définie.
pub(crate) fn ecrire_texte(sortie: &mut Vec<u8>, texte: &str) {
    let octets = texte.as_bytes();
    ecrire_entete(sortie, PREFIXE_TEXTE, argument_de_longueur(octets.len()));
    sortie.extend_from_slice(octets);
}

/// Écrit une chaîne d'octets (type majeur 2), longueur définie.
pub(crate) fn ecrire_octets(sortie: &mut Vec<u8>, octets: &[u8]) {
    ecrire_entete(sortie, PREFIXE_OCTETS, argument_de_longueur(octets.len()));
    sortie.extend_from_slice(octets);
}

/// Curseur de lecture, total : toute opération rend une valeur ou une erreur
/// nommée. Aucun accès indexé, aucune arithmétique non contrôlée.
pub(crate) struct Lecteur<'a> {
    donnees: &'a [u8],
    position: usize,
}

impl<'a> Lecteur<'a> {
    pub(crate) fn nouveau(donnees: &'a [u8]) -> Self {
        Self {
            donnees,
            position: 0,
        }
    }

    pub(crate) fn position(&self) -> usize {
        self.position
    }

    pub(crate) fn restants(&self) -> usize {
        self.donnees.len().saturating_sub(self.position)
    }

    pub(crate) fn termine(&self) -> bool {
        self.position >= self.donnees.len()
    }

    /// Rend la tranche des `longueur` prochains octets et avance le curseur.
    pub(crate) fn tranche(&mut self, longueur: usize) -> Result<&'a [u8], ErreurDecodage> {
        let debut = self.position;
        let fin = match debut.checked_add(longueur) {
            Some(fin) => fin,
            None => {
                return Err(ErreurDecodage::LongueurHorsMemoire {
                    position: debut,
                    longueur: argument_de_longueur(longueur),
                });
            }
        };
        match self.donnees.get(debut..fin) {
            Some(tranche) => {
                self.position = fin;
                Ok(tranche)
            }
            None => Err(ErreurDecodage::FinPrematuree {
                position: debut,
                octets_requis: longueur,
                octets_disponibles: self.restants(),
            }),
        }
    }

    fn octet(&mut self) -> Result<u8, ErreurDecodage> {
        let tranche = self.tranche(1)?;
        match tranche.first().copied() {
            Some(octet) => Ok(octet),
            // Inatteignable : `tranche(1)` a déjà établi la présence d'un octet.
            // Refus plutôt que divergence (ADR-0010, points 3 et 5).
            None => Err(ErreurDecodage::FinPrematuree {
                position: self.position,
                octets_requis: 1,
                octets_disponibles: 0,
            }),
        }
    }

    /// Lit un en-tête et rend `(préfixe de type majeur, argument)`.
    ///
    /// Refuse : longueur indéfinie, valeurs d'information réservées, et tout
    /// argument encodé sur plus d'octets que la forme préférée.
    pub(crate) fn entete(&mut self) -> Result<(u8, u64), ErreurDecodage> {
        let position = self.position;
        let premier = self.octet()?;
        let prefixe = premier & MASQUE_MAJEUR;
        let information = premier & MASQUE_INFORMATION;

        if information <= ARGUMENT_DIRECT_MAX_INFO {
            return Ok((prefixe, u64::from(information)));
        }
        if information == INFO_INDEFINIE {
            return Err(ErreurDecodage::LongueurIndefinie { position });
        }
        let octets_utilises: u8 = match information {
            INFO_UN_OCTET => 1,
            INFO_DEUX_OCTETS => 2,
            INFO_QUATRE_OCTETS => 4,
            INFO_HUIT_OCTETS => 8,
            _ => {
                return Err(ErreurDecodage::ArgumentReserve {
                    position,
                    information,
                });
            }
        };
        let largeur = usize::from(octets_utilises);
        let octets = self.tranche(largeur)?;
        // Repli gros-boutiste sans opérateur arithmétique et sans indexation :
        // au plus 8 décalages de 8 bits, aucun bit perdu (largeur <= 8).
        let mut argument: u64 = 0;
        for octet in octets.iter().copied() {
            argument = argument.wrapping_shl(8) | u64::from(octet);
        }
        if !argument_est_prefere(argument, largeur) {
            return Err(ErreurDecodage::EntierNonPrefere {
                position,
                argument,
                octets_utilises,
            });
        }
        Ok((prefixe, argument))
    }

    /// Lit un en-tête et exige le type majeur attendu.
    pub(crate) fn entete_de_type(&mut self, prefixe_attendu: u8) -> Result<u64, ErreurDecodage> {
        let position = self.position;
        let (prefixe, argument) = self.entete()?;
        if prefixe != prefixe_attendu {
            return Err(ErreurDecodage::TypeMajeurInattendu {
                position,
                prefixe_attendu,
                prefixe_trouve: prefixe,
            });
        }
        Ok(argument)
    }

    /// Convertit un argument de longueur en taille mémoire, sans allocation
    /// préalable : une longueur venue du lot ne dimensionne jamais un tampon
    /// avant d'avoir été confrontée aux octets réellement présents.
    pub(crate) fn longueur_memoire(&self, argument: u64) -> Result<usize, ErreurDecodage> {
        match usize::try_from(argument) {
            Ok(longueur) => Ok(longueur),
            Err(_) => Err(ErreurDecodage::LongueurHorsMemoire {
                position: self.position,
                longueur: argument,
            }),
        }
    }
}

/// Borne haute de l'information portée directement dans l'octet d'en-tête.
const ARGUMENT_DIRECT_MAX_INFO: u8 = 23;

/// Vrai si `argument` est bien encodé sur sa forme la plus courte pour la
/// largeur d'argument `largeur` (sérialisation préférée, RFC 8949).
fn argument_est_prefere(argument: u64, largeur: usize) -> bool {
    match largeur {
        1 => argument > ARGUMENT_DIRECT_MAX,
        2 => argument > u64::from(u8::MAX),
        4 => argument > u64::from(u16::MAX),
        8 => argument > u64::from(u32::MAX),
        _ => false,
    }
}
