//! La **valeur décimale exacte** — mantisse entière et exposant de base dix.
//!
//! Rattachement (G0) : **ADR-0002** (l'encodage du dépôt est le CBOR
//! déterministe de la RFC 8949) ; **RFC 8949 §3.4.4** (détenue, lue) ; **10
//! §3.1** (les décodages du pool sont déjà de cette forme : Pyth
//! `price · 10^expo`, Chainlink « 8 décimales ») ; **ADR-0003** (recalculable
//! offline) et **ADR-0005 règle 1** (le lien aux octets exacts).
//!
//! # La forme retenue, et ce qui la fonde
//!
//! Un prix se représente ici par **deux entiers** — une mantisse `m` et un
//! exposant `e`, la valeur étant `m · 10^e`. Ce n'est pas un choix de goût :
//! c'est **exactement** la forme que la RFC 8949 §3.4.4 donne au numéro de tag
//! 4 (« Decimal Fractions »), dans la norme d'encodage qu'ADR-0002 a déjà
//! adoptée pour tout le dépôt. La pièce dit aussi *pourquoi* elle existe :
//!
//! > « Decimal fractions combine an integer mantissa with a base-10 scaling
//! > factor. They are most useful if an application needs the exact
//! > representation of a decimal fraction such as 1.1 because there is no
//! > exact representation for many decimal fractions in binary floating-point
//! > representations. »
//!
//! L'alternative — conserver la seule chaîne décimale validée — a été écartée
//! comme représentation *unique* : une chaîne ne se compare et ne s'additionne
//! pas sans être re-analysée à chaque usage, et chaque re-analyse est une
//! occasion nouvelle de se tromper. Elle n'est pas perdue pour autant : le
//! lexème de la source est **conservé à côté** de la forme typée (voir
//! [`Decimale::lexeme`]), parce qu'ADR-0003 veut un artefact recalculable et
//! qu'une échelle écrite par la source (`64529.50000000` — huit décimales,
//! dont sept zéros) est une information de la source, pas un bruit à
//! normaliser.
//!
//! **Aucun flottant binaire n'apparaît dans ce module, ni dans aucun chemin de
//! ce typeur.** Le type `f32`/`f64` n'y est jamais nommé ; le contrôle est
//! mécanisé par un test lexical de la suite.
//!
//! # La grammaire admise
//!
//! ```text
//! decimale = [ "-" ] partie-entiere [ "." 1*chiffre ]
//! partie-entiere = "0" / ( chiffre-non-nul *chiffre )
//! ```
//!
//! Plus étroite que le nombre JSON de la RFC 8259 §6 : **pas d'exposant**, pas
//! de `+`, pas de zéro de tête, pas de blanc. Ce qui sort de cette forme est
//! refusé avec sa clause, jamais rectifié.

use crate::erreur::ErreurDecimale;

/// Une valeur décimale exacte : `mantisse · 10^exposant`, plus le lexème dont
/// elle a été lue.
///
/// L'exposant produit par ce module est toujours **négatif ou nul** : il vaut
/// l'opposé du nombre de décimales écrites par la source.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Decimale {
    mantisse: i128,
    exposant: i32,
    lexeme: String,
}

impl Decimale {
    /// La mantisse entière.
    pub fn mantisse(&self) -> i128 {
        self.mantisse
    }

    /// L'exposant de base dix.
    pub fn exposant(&self) -> i32 {
        self.exposant
    }

    /// Le lexème **verbatim** lu dans le dire — jamais réécrit.
    pub fn lexeme(&self) -> &str {
        &self.lexeme
    }

    /// Reconstruit la graphie décimale depuis la seule forme typée.
    ///
    /// C'est le témoin de fidélité de la représentation : la propriété (a) de
    /// la suite exige `graphie_reconstruite() == lexeme()` sur tout lexème
    /// admis. Si les deux divergent, la forme typée a perdu quelque chose que
    /// la source avait écrit.
    pub fn graphie_reconstruite(&self) -> String {
        let negative = self.mantisse < 0;
        let chiffres = self.mantisse.unsigned_abs().to_string();
        let decimales = usize::try_from(self.exposant.saturating_neg()).unwrap_or(0);
        let mut graphie = String::new();
        if negative {
            graphie.push('-');
        }
        if decimales == 0 {
            graphie.push_str(&chiffres);
            return graphie;
        }
        let largeur = decimales.saturating_add(1);
        let manquants = largeur.saturating_sub(chiffres.len());
        let mut rembourres = String::new();
        for _ in 0..manquants {
            rembourres.push('0');
        }
        rembourres.push_str(&chiffres);
        let coupure = rembourres.len().saturating_sub(decimales);
        let entiere = rembourres.get(..coupure).unwrap_or_default();
        let fraction = rembourres.get(coupure..).unwrap_or_default();
        graphie.push_str(entiere);
        graphie.push('.');
        graphie.push_str(fraction);
        graphie
    }
}

/// Type une graphie décimale exacte, ou refuse en nommant la clause.
///
/// **Total** : toute chaîne est une entrée admise.
pub fn typer_decimale(graphie: &str) -> Result<Decimale, ErreurDecimale> {
    let octets = graphie.as_bytes();
    if octets.is_empty() {
        return Err(ErreurDecimale::Vide);
    }
    // La notation scientifique est cherchée d'abord, pour que son refus soit
    // celui qu'on lit — et non un « octet hors forme » qui n'apprendrait rien.
    if let Some(position) = octets.iter().position(|octet| matches!(octet, b'e' | b'E')) {
        return Err(ErreurDecimale::NotationScientifique { position });
    }
    let mut position = 0usize;
    let negative = octets.first() == Some(&b'-');
    if negative {
        position = 1;
    }
    let debut_entiere = position;
    let mut mantisse: i128 = 0;
    let mut chiffres = 0usize;
    while let Some(octet) = octets.get(position) {
        if !octet.is_ascii_digit() {
            break;
        }
        mantisse = accumuler(mantisse, *octet, &mut chiffres)?;
        position = position.saturating_add(1);
    }
    let longueur_entiere = position.saturating_sub(debut_entiere);
    if longueur_entiere == 0 {
        return Err(ErreurDecimale::ChiffreAttendu { position });
    }
    if longueur_entiere > 1 && octets.get(debut_entiere) == Some(&b'0') {
        return Err(ErreurDecimale::ZeroDeTete {
            position: debut_entiere,
        });
    }
    let mut decimales = 0usize;
    if octets.get(position) == Some(&b'.') {
        let position_du_point = position;
        position = position.saturating_add(1);
        while let Some(octet) = octets.get(position) {
            if !octet.is_ascii_digit() {
                break;
            }
            mantisse = accumuler(mantisse, *octet, &mut chiffres)?;
            decimales = decimales.saturating_add(1);
            position = position.saturating_add(1);
        }
        if decimales == 0 {
            return Err(ErreurDecimale::ChiffreAttendu {
                position: position_du_point.saturating_add(1),
            });
        }
    }
    if let Some(octet) = octets.get(position) {
        if *octet == b'.' {
            return Err(ErreurDecimale::PointDecimalRepete { position });
        }
        return Err(ErreurDecimale::OctetHorsForme {
            position,
            octet: *octet,
        });
    }
    if negative {
        if mantisse == 0 {
            return Err(ErreurDecimale::ZeroSigne { position: 0 });
        }
        mantisse = mantisse
            .checked_neg()
            .ok_or(ErreurDecimale::CapaciteDeMantisseDepassee { chiffres })?;
    }
    let exposant = i32::try_from(decimales)
        .ok()
        .and_then(|nombre| nombre.checked_neg())
        .ok_or(ErreurDecimale::ExposantHorsCapacite { decimales })?;
    Ok(Decimale {
        mantisse,
        exposant,
        lexeme: String::from(graphie),
    })
}

/// Ajoute un chiffre à la mantisse, en **arithmétique contrôlée**.
///
/// Le débordement n'est pas un arrondi : c'est un refus. C'est ici que se joue
/// le cas « perte de précision » — un prix à quarante chiffres significatifs
/// n'est pas tronqué à trente-huit, il n'est pas typé du tout.
fn accumuler(mantisse: i128, octet: u8, chiffres: &mut usize) -> Result<i128, ErreurDecimale> {
    let chiffre = i128::from(octet.saturating_sub(b'0'));
    *chiffres = chiffres.saturating_add(1);
    mantisse
        .checked_mul(10)
        .and_then(|decale| decale.checked_add(chiffre))
        .ok_or(ErreurDecimale::CapaciteDeMantisseDepassee {
            chiffres: *chiffres,
        })
}
