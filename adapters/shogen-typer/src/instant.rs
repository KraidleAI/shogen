//! L'**instant** porté par la source — graphie RFC 3339 contrôlée, jamais
//! convertie.
//!
//! Rattachement (G0) : **RFC 3339 §5.6 et §5.7** (détenue depuis le
//! 2026-08-13, `biblio/rfc-3339-datetime-2026-08-13.txt`) ; **03 §1**, champ
//! `observed_at` — « l'instant de l'observation, avec l'horloge qui l'a produit
//! (celle du transport, jamais celle de Shōgen) … la fraîcheur se calcule plus
//! haut ; ici on enregistre qui a daté » ; **10 §3.1** (Coinbase porte
//! `time` = `12:03:37.68Z` dans son dire).
//!
//! # Ce que ce module ne fait PAS, et pourquoi
//!
//! Il **ne convertit pas** l'instant en époque. L'instrument jetable de S2
//! (`s2-harness/shogen_s2/sources.py`) le fait et **tronque à la microseconde**
//! les neuf décimales que Coinbase émet — son propre commentaire le dit :
//! « Tolère 'Z' et une fraction à précision variable (Coinbase émet des ns) en
//! tronquant à la microseconde. » Cette troncature est
//! tolérable dans un instrument de mesure jetable ; elle est exactement ce
//! qu'un typeur fail-closed n'a pas le droit de faire. Ici la graphie est
//! contrôlée puis **conservée telle quelle** : pas d'époque, pas de troncature,
//! pas de fuseau converti.
//!
//! # La forme admise
//!
//! `date-time` de la RFC 3339 §5.6, restreint sur deux points, chacun fondé :
//!
//! 1. **`T` et `Z` en majuscules seulement.** §5.6, NOTE : « Specifications
//!    that use this format in such environments MAY further limit the date/time
//!    syntax so that the letters 'T' and 'Z' used in the date/time syntax must
//!    always be upper case. » La permission est dans la pièce ; on l'exerce.
//! 2. **Décalage `Z` seulement**, jamais `+hh:mm`. Un typeur qui accepterait un
//!    décalage devrait soit le conserver (deux graphies pour un même instant,
//!    donc deux faits distincts pour une même observation), soit le convertir
//!    (réécrire la source). Il refuse.
//!
//! Les bornes de champ sont celles de §5.6 et le tableau de §5.7 (maximum de
//! `date-mday` par mois, février bissextile compris) ; la seconde 60 est admise
//! parce que la pièce l'admet (« 00-58, 00-59, 00-60 based on leap second
//! rules »).

use crate::erreur::ErreurInstant;

/// Un instant en graphie RFC 3339 UTC, contrôlé et conservé verbatim.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Instant {
    graphie: String,
}

impl Instant {
    /// La graphie **verbatim** de la source.
    pub fn graphie(&self) -> &str {
        &self.graphie
    }
}

/// Positions fixes de la forme `YYYY-MM-DDThh:mm:ss` (19 octets).
const LONGUEUR_MINIMALE: usize = 19;

/// Contrôle une graphie d'instant, ou refuse en nommant la clause.
///
/// **Total** : toute chaîne est une entrée admise.
pub fn typer_instant(graphie: &str) -> Result<Instant, ErreurInstant> {
    let octets = graphie.as_bytes();
    if octets.is_empty() {
        return Err(ErreurInstant::Vide);
    }
    if octets.len() < LONGUEUR_MINIMALE {
        return Err(ErreurInstant::FinPrematuree {
            position: octets.len(),
        });
    }
    let annee = nombre(octets, 0, 4)?;
    separateur(octets, 4, b'-')?;
    let mois = nombre(octets, 5, 2)?;
    separateur(octets, 7, b'-')?;
    let jour = nombre(octets, 8, 2)?;
    separateur(octets, 10, b'T')?;
    let heure = nombre(octets, 11, 2)?;
    separateur(octets, 13, b':')?;
    let minute = nombre(octets, 14, 2)?;
    separateur(octets, 16, b':')?;
    let seconde = nombre(octets, 17, 2)?;

    // Bornes — RFC 3339 §5.6 (commentaires de l'ABNF) et §5.7 (tableau).
    if !(1..=12).contains(&mois) {
        return Err(ErreurInstant::ChampHorsBornes {
            champ: "date-month",
            valeur: mois,
        });
    }
    if jour < 1 || jour > jours_du_mois(annee, mois) {
        return Err(ErreurInstant::ChampHorsBornes {
            champ: "date-mday",
            valeur: jour,
        });
    }
    if heure > 23 {
        return Err(ErreurInstant::ChampHorsBornes {
            champ: "time-hour",
            valeur: heure,
        });
    }
    if minute > 59 {
        return Err(ErreurInstant::ChampHorsBornes {
            champ: "time-minute",
            valeur: minute,
        });
    }
    if seconde > 60 {
        return Err(ErreurInstant::ChampHorsBornes {
            champ: "time-second",
            valeur: seconde,
        });
    }

    let mut position = LONGUEUR_MINIMALE;
    if octets.get(position) == Some(&b'.') {
        position = position.saturating_add(1);
        let debut = position;
        while matches!(octets.get(position), Some(octet) if octet.is_ascii_digit()) {
            position = position.saturating_add(1);
        }
        if position == debut {
            return Err(ErreurInstant::FractionVide { position: debut });
        }
    }
    match octets.get(position) {
        None => {
            return Err(ErreurInstant::FinPrematuree { position });
        }
        Some(b'Z') => position = position.saturating_add(1),
        Some(_) => {
            return Err(ErreurInstant::DecalageNonUtc { position });
        }
    }
    if position < octets.len() {
        return Err(ErreurInstant::OctetsResiduels {
            position,
            restants: octets.len().saturating_sub(position),
        });
    }
    Ok(Instant {
        graphie: String::from(graphie),
    })
}

fn separateur(octets: &[u8], position: usize, attendu: u8) -> Result<(), ErreurInstant> {
    match octets.get(position) {
        None => Err(ErreurInstant::FinPrematuree { position }),
        Some(trouve) if *trouve == attendu => Ok(()),
        Some(trouve) => Err(ErreurInstant::OctetInattendu {
            position,
            attendu,
            trouve: *trouve,
        }),
    }
}

fn nombre(octets: &[u8], position: usize, largeur: usize) -> Result<u32, ErreurInstant> {
    let mut valeur: u32 = 0;
    for decalage in 0..largeur {
        let index = position.saturating_add(decalage);
        let octet = octets
            .get(index)
            .ok_or(ErreurInstant::FinPrematuree { position: index })?;
        if !octet.is_ascii_digit() {
            return Err(ErreurInstant::ChiffreAttendu { position: index });
        }
        valeur = valeur
            .saturating_mul(10)
            .saturating_add(u32::from(octet.saturating_sub(b'0')));
    }
    Ok(valeur)
}

/// Le maximum de `date-mday` — RFC 3339 §5.7, tableau (« 02 February, normal
/// 28 » / « 02 February, leap year 29 »).
fn jours_du_mois(annee: u32, mois: u32) -> u32 {
    match mois {
        1 | 3 | 5 | 7 | 8 | 10 | 12 => 31,
        4 | 6 | 9 | 11 => 30,
        2 => {
            if bissextile(annee) {
                29
            } else {
                28
            }
        }
        _ => 0,
    }
}

/// La règle bissextile transcrite de la pièce — RFC 3339 Appendix C, qui donne
/// un sous-programme C : « return (year % 4 == 0 && (year % 100 != 0 || year %
/// 400 == 0)); ». Reste écrite en arithmétique contrôlée (`checked_rem`) : le
/// dépôt refuse l'opérateur nu.
fn bissextile(annee: u32) -> bool {
    let divisible_par = |diviseur: u32| annee.checked_rem(diviseur) == Some(0);
    divisible_par(4) && (!divisible_par(100) || divisible_par(400))
}
