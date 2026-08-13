//! L'analyseur du **dire brut** — un sous-ensemble strict de RFC 8259, écrit
//! à la main.
//!
//! Rattachement (G0) : **RFC 8259** (détenue depuis le 2026-08-13,
//! `biblio/rfc-8259-json-2026-08-13.txt`) ; **ADR-0009** (dépendances
//! minimales) ; **ADR-0012 D3** ; **ADR-0018** (le précédent du dépôt : une
//! implémentation manuelle, adossée à des vecteurs, plutôt qu'une crate qui
//! entre au graphe).
//!
//! **Pourquoi à la main, et pas `serde_json`** — l'argument est technique, pas
//! idéologique : l'analyseur de `serde_json` type un nombre JSON non entier en
//! `f64` (flottant binaire) hors de sa fonctionnalité `arbitrary_precision`.
//! Or l'objet même de ce typeur est qu'aucun flottant binaire n'approche un
//! prix. Le choix se réduisait donc à « une dépendance nouvelle **plus** sa
//! fonctionnalité non par défaut » contre « un analyseur écrit ici, aux refus
//! nommés, qui rend les **lexèmes verbatim** ». Le dépôt a déjà tranché deux
//! fois dans ce sens (CBOR à la main, SHA-256 à la main) et pour la même
//! raison : le graphe de dépendances du produit est un observable de sécurité.
//!
//! **Ce que cet analyseur n'est pas** : un analyseur JSON généraliste. Il ne
//! conserve que les membres de l'objet **racine** ; il valide intégralement le
//! reste (sinon un dire malformé passerait pour bien formé), mais n'en garde
//! rien. Il ne doit jamais être décrit comme « un analyseur JSON » tout court.

use crate::erreur::{ErreurJson, PROFONDEUR_MAXIMALE};

/// Une valeur JSON, au grain dont le typeur a besoin.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Valeur {
    /// Une chaîne, échappements résolus.
    Texte(String),
    /// Un nombre, conservé **verbatim** : le typeur ne re-graphie rien.
    Nombre(String),
    /// `true`, `false` ou `null`.
    Litteral,
    /// Un objet imbriqué : validé, non conservé.
    Objet,
    /// Un tableau : validé, non conservé.
    Tableau,
}

/// Les membres de l'objet racine, dans l'ordre où le dire les porte.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ObjetRacine {
    membres: Vec<(String, Valeur, usize)>,
}

impl ObjetRacine {
    /// La valeur d'un membre **de la racine**, et la position d'octet où elle
    /// commence. Un membre homonyme imbriqué n'est jamais rendu ici.
    pub fn membre(&self, cle: &str) -> Option<(&Valeur, usize)> {
        self.membres
            .iter()
            .find(|(nom, _, _)| nom == cle)
            .map(|(_, valeur, position)| (valeur, *position))
    }

    /// Le nombre de membres de la racine.
    pub fn nombre_de_membres(&self) -> usize {
        self.membres.len()
    }
}

struct Analyseur<'a> {
    octets: &'a [u8],
    position: usize,
    profondeur: usize,
}

/// Analyse un dire brut et rend les membres de son objet racine.
///
/// **Total** : toute suite d'octets est une entrée admise ; ce qui n'est pas un
/// objet JSON bien formé rend un refus nommé, jamais une divergence.
pub fn analyser_objet_racine(octets: &[u8]) -> Result<ObjetRacine, ErreurJson> {
    if octets.is_empty() {
        return Err(ErreurJson::EntreeVide);
    }
    if let Err(erreur) = core::str::from_utf8(octets) {
        return Err(ErreurJson::EntreeNonUtf8 {
            position: erreur.valid_up_to(),
        });
    }
    let mut analyseur = Analyseur {
        octets,
        position: 0,
        profondeur: 0,
    };
    analyseur.sauter_blancs();
    let ouvrant = analyseur.octet_courant().ok_or(ErreurJson::FinPrematuree {
        position: analyseur.position,
    })?;
    if ouvrant != b'{' {
        return Err(ErreurJson::RacineNonObjet {
            position: analyseur.position,
            trouve: ouvrant,
        });
    }
    let racine = analyseur.objet(true)?;
    analyseur.sauter_blancs();
    if analyseur.position < analyseur.octets.len() {
        return Err(ErreurJson::OctetsResiduels {
            position: analyseur.position,
            restants: analyseur.octets.len().saturating_sub(analyseur.position),
        });
    }
    Ok(ObjetRacine { membres: racine })
}

impl Analyseur<'_> {
    fn octet_courant(&self) -> Option<u8> {
        self.octets.get(self.position).copied()
    }

    fn avancer(&mut self) {
        self.position = self.position.saturating_add(1);
    }

    fn sauter_blancs(&mut self) {
        // RFC 8259 §2 : les quatre seuls blancs admis.
        while let Some(octet) = self.octet_courant() {
            match octet {
                b' ' | b'\t' | b'\n' | b'\r' => self.avancer(),
                _ => break,
            }
        }
    }

    fn attendre(&mut self, attendu: u8) -> Result<(), ErreurJson> {
        match self.octet_courant() {
            None => Err(ErreurJson::FinPrematuree {
                position: self.position,
            }),
            Some(trouve) if trouve == attendu => {
                self.avancer();
                Ok(())
            }
            Some(trouve) => Err(ErreurJson::OctetInattendu {
                position: self.position,
                attendu,
                trouve,
            }),
        }
    }

    fn entrer(&mut self) -> Result<(), ErreurJson> {
        self.profondeur = self.profondeur.saturating_add(1);
        if self.profondeur > PROFONDEUR_MAXIMALE {
            return Err(ErreurJson::ProfondeurExcessive {
                position: self.position,
                profondeur_maximale: PROFONDEUR_MAXIMALE,
            });
        }
        Ok(())
    }

    fn sortir(&mut self) {
        self.profondeur = self.profondeur.saturating_sub(1);
    }

    /// Un objet. `conserver` dit si ses membres remontent (racine seule).
    fn objet(&mut self, conserver: bool) -> Result<Vec<(String, Valeur, usize)>, ErreurJson> {
        self.entrer()?;
        self.attendre(b'{')?;
        let mut membres: Vec<(String, Valeur, usize)> = Vec::new();
        let mut noms: Vec<String> = Vec::new();
        self.sauter_blancs();
        if self.octet_courant() == Some(b'}') {
            self.avancer();
            self.sortir();
            return Ok(membres);
        }
        loop {
            self.sauter_blancs();
            let position_de_cle = self.position;
            let nom = self.texte()?;
            // Unicité des noms — RFC 8259 §4, refus fail-closed.
            if noms.iter().any(|deja| deja == &nom) {
                return Err(ErreurJson::CleDupliquee {
                    position: position_de_cle,
                    cle: nom,
                });
            }
            noms.push(nom.clone());
            self.sauter_blancs();
            self.attendre(b':')?;
            self.sauter_blancs();
            let position_de_valeur = self.position;
            let valeur = self.valeur()?;
            if conserver {
                membres.push((nom, valeur, position_de_valeur));
            }
            self.sauter_blancs();
            match self.octet_courant() {
                Some(b',') => {
                    self.avancer();
                }
                Some(b'}') => {
                    self.avancer();
                    self.sortir();
                    return Ok(membres);
                }
                Some(trouve) => {
                    return Err(ErreurJson::OctetInattendu {
                        position: self.position,
                        attendu: b'}',
                        trouve,
                    });
                }
                None => {
                    return Err(ErreurJson::FinPrematuree {
                        position: self.position,
                    });
                }
            }
        }
    }

    fn tableau(&mut self) -> Result<(), ErreurJson> {
        self.entrer()?;
        self.attendre(b'[')?;
        self.sauter_blancs();
        if self.octet_courant() == Some(b']') {
            self.avancer();
            self.sortir();
            return Ok(());
        }
        loop {
            self.sauter_blancs();
            let _ = self.valeur()?;
            self.sauter_blancs();
            match self.octet_courant() {
                Some(b',') => {
                    self.avancer();
                }
                Some(b']') => {
                    self.avancer();
                    self.sortir();
                    return Ok(());
                }
                Some(trouve) => {
                    return Err(ErreurJson::OctetInattendu {
                        position: self.position,
                        attendu: b']',
                        trouve,
                    });
                }
                None => {
                    return Err(ErreurJson::FinPrematuree {
                        position: self.position,
                    });
                }
            }
        }
    }

    fn valeur(&mut self) -> Result<Valeur, ErreurJson> {
        match self.octet_courant() {
            None => Err(ErreurJson::FinPrematuree {
                position: self.position,
            }),
            Some(b'"') => Ok(Valeur::Texte(self.texte()?)),
            Some(b'{') => {
                let _ = self.objet(false)?;
                Ok(Valeur::Objet)
            }
            Some(b'[') => {
                self.tableau()?;
                Ok(Valeur::Tableau)
            }
            Some(b't') => {
                self.litteral(b"true")?;
                Ok(Valeur::Litteral)
            }
            Some(b'f') => {
                self.litteral(b"false")?;
                Ok(Valeur::Litteral)
            }
            Some(b'n') => {
                self.litteral(b"null")?;
                Ok(Valeur::Litteral)
            }
            Some(_) => Ok(Valeur::Nombre(self.nombre()?)),
        }
    }

    fn litteral(&mut self, attendu: &[u8]) -> Result<(), ErreurJson> {
        let debut = self.position;
        let fin = debut.saturating_add(attendu.len());
        match self.octets.get(debut..fin) {
            Some(lu) if lu == attendu => {
                self.position = fin;
                Ok(())
            }
            _ => Err(ErreurJson::LitteralInconnu { position: debut }),
        }
    }

    /// Un nombre JSON — RFC 8259 §6. Le lexème est rendu **verbatim**.
    fn nombre(&mut self) -> Result<String, ErreurJson> {
        let debut = self.position;
        if self.octet_courant() == Some(b'-') {
            self.avancer();
        }
        match self.octet_courant() {
            Some(b'0') => self.avancer(),
            Some(octet) if octet.is_ascii_digit() => {
                while matches!(self.octet_courant(), Some(o) if o.is_ascii_digit()) {
                    self.avancer();
                }
            }
            _ => return Err(ErreurJson::NombreMalForme { position: debut }),
        }
        if self.octet_courant() == Some(b'.') {
            self.avancer();
            if !matches!(self.octet_courant(), Some(o) if o.is_ascii_digit()) {
                return Err(ErreurJson::NombreMalForme {
                    position: self.position,
                });
            }
            while matches!(self.octet_courant(), Some(o) if o.is_ascii_digit()) {
                self.avancer();
            }
        }
        if matches!(self.octet_courant(), Some(b'e' | b'E')) {
            self.avancer();
            if matches!(self.octet_courant(), Some(b'+' | b'-')) {
                self.avancer();
            }
            if !matches!(self.octet_courant(), Some(o) if o.is_ascii_digit()) {
                return Err(ErreurJson::NombreMalForme {
                    position: self.position,
                });
            }
            while matches!(self.octet_courant(), Some(o) if o.is_ascii_digit()) {
                self.avancer();
            }
        }
        let lexeme = self
            .octets
            .get(debut..self.position)
            .and_then(|tranche| core::str::from_utf8(tranche).ok())
            .ok_or(ErreurJson::NombreMalForme { position: debut })?;
        Ok(String::from(lexeme))
    }

    /// Une chaîne JSON — RFC 8259 §7, échappements résolus.
    fn texte(&mut self) -> Result<String, ErreurJson> {
        self.attendre(b'"')?;
        let mut rendu = String::new();
        let mut debut_de_tranche = self.position;
        loop {
            let octet = self.octet_courant().ok_or(ErreurJson::FinPrematuree {
                position: self.position,
            })?;
            match octet {
                b'"' => {
                    self.pousser_tranche(&mut rendu, debut_de_tranche)?;
                    self.avancer();
                    return Ok(rendu);
                }
                b'\\' => {
                    self.pousser_tranche(&mut rendu, debut_de_tranche)?;
                    self.avancer();
                    self.echappement(&mut rendu)?;
                    debut_de_tranche = self.position;
                }
                // RFC 8259 §7 : « the characters that MUST be escaped:
                // quotation mark, reverse solidus, and the control characters
                // (U+0000 through U+001F) ».
                0x00..=0x1F => {
                    return Err(ErreurJson::CaractereDeControle {
                        position: self.position,
                        octet,
                    });
                }
                _ => self.avancer(),
            }
        }
    }

    /// Recopie la tranche littérale [debut, position) dans le rendu.
    ///
    /// La tranche est de l'UTF-8 valide : l'entrée entière l'est (contrôlée à
    /// l'entrée d'[`analyser_objet_racine`]) et les bornes tombent sur des
    /// octets ASCII (`"` ou `\`), jamais au milieu d'une séquence multi-octet.
    fn pousser_tranche(&self, rendu: &mut String, debut: usize) -> Result<(), ErreurJson> {
        let tranche = self
            .octets
            .get(debut..self.position)
            .and_then(|octets| core::str::from_utf8(octets).ok())
            .ok_or(ErreurJson::EntreeNonUtf8 { position: debut })?;
        rendu.push_str(tranche);
        Ok(())
    }

    fn echappement(&mut self, rendu: &mut String) -> Result<(), ErreurJson> {
        let octet = self.octet_courant().ok_or(ErreurJson::FinPrematuree {
            position: self.position,
        })?;
        let caractere = match octet {
            b'"' => '"',
            b'\\' => '\\',
            b'/' => '/',
            b'b' => '\u{0008}',
            b'f' => '\u{000C}',
            b'n' => '\n',
            b'r' => '\r',
            b't' => '\t',
            b'u' => {
                self.avancer();
                return self.echappement_unicode(rendu);
            }
            _ => {
                return Err(ErreurJson::EchappementInconnu {
                    position: self.position,
                    octet,
                });
            }
        };
        self.avancer();
        rendu.push(caractere);
        Ok(())
    }

    fn echappement_unicode(&mut self, rendu: &mut String) -> Result<(), ErreurJson> {
        let unite = self.quatre_hexadecimaux()?;
        // RFC 8259 §7 : les caractères hors du plan multilingue de base
        // s'écrivent en paire de substituts UTF-16.
        if (0xD800..=0xDBFF).contains(&unite) {
            let position_du_pair = self.position;
            if self.octet_courant() != Some(b'\\') {
                return Err(ErreurJson::SubstitutOrphelin {
                    position: position_du_pair,
                    unite,
                });
            }
            self.avancer();
            if self.octet_courant() != Some(b'u') {
                return Err(ErreurJson::SubstitutOrphelin {
                    position: position_du_pair,
                    unite,
                });
            }
            self.avancer();
            let bas = self.quatre_hexadecimaux()?;
            if !(0xDC00..=0xDFFF).contains(&bas) {
                return Err(ErreurJson::SubstitutOrphelin {
                    position: position_du_pair,
                    unite: bas,
                });
            }
            let haut = u32::from(unite).saturating_sub(0xD800);
            let bas = u32::from(bas).saturating_sub(0xDC00);
            let point = haut
                .checked_mul(0x400)
                .and_then(|gauche| gauche.checked_add(bas))
                .and_then(|somme| somme.checked_add(0x1_0000))
                .and_then(char::from_u32)
                .ok_or(ErreurJson::SubstitutOrphelin {
                    position: position_du_pair,
                    unite,
                })?;
            rendu.push(point);
            return Ok(());
        }
        if (0xDC00..=0xDFFF).contains(&unite) {
            return Err(ErreurJson::SubstitutOrphelin {
                position: self.position,
                unite,
            });
        }
        let point = char::from_u32(u32::from(unite)).ok_or(ErreurJson::SubstitutOrphelin {
            position: self.position,
            unite,
        })?;
        rendu.push(point);
        Ok(())
    }

    fn quatre_hexadecimaux(&mut self) -> Result<u16, ErreurJson> {
        let debut = self.position;
        let fin = debut.saturating_add(4);
        let chiffres = self
            .octets
            .get(debut..fin)
            .ok_or(ErreurJson::EchappementUnicodeMalForme { position: debut })?;
        let mut unite: u16 = 0;
        for chiffre in chiffres {
            let valeur = match chiffre {
                b'0'..=b'9' => chiffre.saturating_sub(b'0'),
                b'a'..=b'f' => chiffre.saturating_sub(b'a').saturating_add(10),
                b'A'..=b'F' => chiffre.saturating_sub(b'A').saturating_add(10),
                _ => {
                    return Err(ErreurJson::EchappementUnicodeMalForme { position: debut });
                }
            };
            unite = unite
                .checked_mul(16)
                .and_then(|gauche| gauche.checked_add(u16::from(valeur)))
                .ok_or(ErreurJson::EchappementUnicodeMalForme { position: debut })?;
        }
        self.position = fin;
        Ok(unite)
    }
}
