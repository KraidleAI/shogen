//! Le harnais de fuzz du vérificateur — **couche portable**, ADR-0011 seuil 7.
//!
//! # Ce que ce module est, et ce qu'il n'est pas
//!
//! ADR-0011 seuil 7 : « *Totalité du vérificateur (fuzz)* : **zéro panique sur
//! toute suite d'octets** — seuil binaire, non négociable (S-G3, 12 §5) ;
//! budgets candidats : ≥ 15 min par CI, ≥ 4 h en nightly, corpus de graines
//! committé et croissant de chaque contre-exemple. »
//!
//! Ce harnais tient le **seuil** (zéro panique, fail-closed), le **corpus
//! committé et croissant**, et les **budgets**. Il ne tient PAS la partie
//! « instrumentée » : il n'est pas guidé par la couverture. Il ne voit pas
//! quelles branches un cas atteint, donc il n'apprend rien d'une exécution à la
//! suivante — un moteur libFuzzer ou AFL le fait, et trouve pour cette raison
//! des chemins profonds qu'un tirage aveugle atteint avec une probabilité
//! écrasée par la profondeur.
//!
//! **Cette limite est écrite ici plutôt que laissée à deviner** : l'outillage
//! guidé par la couverture est un choix qui engage la doctrine de toolchain
//! (ADR-0009 point 3 : « version exacte (pas `stable`) … jamais un canal
//! flottant ») — `cargo-fuzz`/libFuzzer exige une toolchain *nightly*
//! **supplémentaire**. Ce choix fait l'objet d'une demande de consultation
//! formée (R-26) et n'est pas tranché ici. En attendant, ce harnais est ce qui
//! tourne, sur les deux plateformes du critère de clôture, sans dépendance
//! nouvelle et sans toolchain nouvelle.
//!
//! # Les trois obligations d'exécution d'ADR-0011 point 2, tenues ici
//!
//! Elles sont écrites pour le property-based, et un fuzz aléatoire est le même
//! régime avec une distribution plus hostile — elles s'appliquent :
//!
//! * **la graine est consignée et le rejeu est exact** — la graine est imprimée
//!   à chaque exécution et se redonne par `--graine` ; le générateur est
//!   SplitMix64, entièrement défini ci-dessous, sans dépendance ;
//! * **la distribution des cas est imprimée AVANT le verdict** — le compte par
//!   classe de sortie (refusé, non canonique, trivial, canonique) et la part de
//!   cas non triviaux ;
//! * **tout contre-exemple devient un cas permanent** — une panique fait écrire
//!   les octets fautifs dans le corpus committé, et le harnais sort ROUGE.
//!
//! # Le partage `catch_unwind` / logique
//!
//! `std::panic::catch_unwind` est ici, dans la coquille, jamais dans la
//! bibliothèque `no_std` du vérificateur (ADR-0009 point 6). Ce qui est éprouvé
//! est [`shogen_verifier::eprouver`] : une fonction totale, sans I/O, qui
//! soumet une même suite d'octets aux trois surfaces d'octets du vérificateur.
//!
//! **Ce qu'un vert de ce harnais établit** : *tested* sur le corpus et les cas
//! tirés, avec leur compte et leur graine, à la date. Jamais *proven* : le
//! coupling effect est empirique (DeMillo p. 35) et l'absence de panique n'est
//! pas établie (ADR-0010, §Coûts point 6).

use std::path::{Path, PathBuf};
use std::time::{Duration, Instant};

/// Le répertoire du corpus committé, relatif à la racine du workspace.
pub const CORPUS: &str = "crates/shogen-verifier/fuzz-corpus";

/// Graine par défaut — fixe, pour que l'exécution sans argument soit rejouable
/// à l'identique. Un fuzz dont la graine change à chaque lancement ne se rejoue
/// pas, et un échec non rejouable n'est pas un fait (ADR-0011 point 2).
pub const GRAINE_PAR_DEFAUT: u64 = 0x5000_0011_0000_0007;

/// Budget par défaut, en secondes : le plancher CI d'ADR-0011 seuil 7.
pub const DUREE_PAR_DEFAUT: u64 = 900;

/// Le plan d'une campagne de fuzz.
pub struct Plan {
    /// Racine du workspace.
    pub racine: PathBuf,
    /// Graine du générateur.
    pub graine: u64,
    /// Budget de temps.
    pub duree: Duration,
}

/// La distribution des cas, imprimée AVANT le verdict (ADR-0011 point 2).
#[derive(Default)]
pub struct Distribution {
    /// Cas où le cœur a refusé les octets.
    pub refuses: u64,
    /// Cas où le lot décode mais n'est pas sa propre forme canonique.
    pub non_canoniques: u64,
    /// Cas décodés en témoignage trivial, ré-encodage exact.
    pub triviaux: u64,
    /// Cas décodés en témoignage canonique, ré-encodage exact.
    pub canoniques: u64,
    /// Cas où le registre s'est analysé sans refus (surface texte 2).
    pub registres_acceptes: u64,
    /// Cas où le constat s'est analysé sans refus (surface texte 3).
    pub constats_acceptes: u64,
}

impl Distribution {
    /// Total des cas exécutés.
    pub fn total(&self) -> u64 {
        self.refuses
            .saturating_add(self.non_canoniques)
            .saturating_add(self.triviaux)
            .saturating_add(self.canoniques)
    }

    /// Les cas **non triviaux** au sens d'ADR-0011 point 6 : ceux qui ont
    /// franchi le décodage — un octet rejeté au premier octet n'exerce presque
    /// rien du vérificateur.
    ///
    /// La classe utile est nommée ici, en toutes lettres, parce que le seuil
    /// candidat qui la mesure (≥ 50 %) suppose qu'elle soit dite : sous le
    /// seuil, « la propriété est refusée (générateur à corriger, jamais seuil
    /// à baisser) ».
    pub fn non_triviaux(&self) -> u64 {
        self.non_canoniques
            .saturating_add(self.triviaux)
            .saturating_add(self.canoniques)
    }

    fn imprimer(&self) {
        let total = self.total();
        println!("  distribution des cas (imprimée AVANT le verdict — ADR-0011 point 2) :");
        println!("    total exécuté                : {total}");
        println!("    refusés au décodage          : {}", self.refuses);
        println!("    décodés, non canoniques      : {}", self.non_canoniques);
        println!("    canoniques — forme triviale  : {}", self.triviaux);
        println!("    canoniques — sept champs     : {}", self.canoniques);
        println!(
            "    (surfaces texte) registres analysés sans refus : {}",
            self.registres_acceptes
        );
        println!(
            "    (surfaces texte) constats analysés sans refus  : {}",
            self.constats_acceptes
        );
        let non_triviaux = self.non_triviaux();
        let pourcentage = if total == 0 {
            0.0
        } else {
            (non_triviaux as f64 * 100.0) / (total as f64)
        };
        println!(
            "    cas non triviaux (franchissent le décodage)     : {non_triviaux} ({pourcentage:.4} %)"
        );
        println!(
            "    ce que ce compte dit : la classe utile est étroite parce que la forme canonique est étroite — c'est un fait sur le générateur, pas un verdict sur le vérificateur"
        );
    }
}

/// Le résultat d'une campagne.
pub struct Rapport {
    /// La graine employée — à redonner par `--graine` pour rejouer.
    pub graine: u64,
    /// Nombre de graines du corpus chargées.
    pub graines_du_corpus: usize,
    /// Durée réellement écoulée.
    pub ecoule: Duration,
    /// La distribution des cas.
    pub distribution: Distribution,
    /// Les contre-exemples écrits au corpus, s'il y en a.
    pub contre_exemples: Vec<PathBuf>,
}

impl Rapport {
    /// Vert si et seulement si aucune panique n'a été observée.
    pub fn vert(&self) -> bool {
        self.contre_exemples.is_empty()
    }

    /// Imprime la couverture, la distribution, puis le verdict — dans cet
    /// ordre (ADR-0013 : la ligne de mesure passe avant le verdict).
    pub fn imprimer(&self) {
        println!("--- fuzz du vérificateur (ADR-0011 seuil 7) ---");
        println!("  graine               : {:#018x}", self.graine);
        println!(
            "  corpus committé      : {} graine(s)",
            self.graines_du_corpus
        );
        println!(
            "  budget écoulé        : {:.1} s",
            self.ecoule.as_secs_f64()
        );
        self.distribution.imprimer();
        if self.vert() {
            println!(
                "  VERDICT : VERT — zéro panique sur {} cas, graine {:#018x}",
                self.distribution.total(),
                self.graine
            );
            println!(
                "  ce que ce vert dit, et rien de plus : *tested* sur ces cas, avec leur compte et leur graine. Il n'établit pas l'absence de panique (ADR-0010, §Coûts point 6), et il n'est pas guidé par la couverture — la couche instrumentée reste due (R-26 en cours)."
            );
        } else {
            println!(
                "  VERDICT : ROUGE — {} contre-exemple(s), écrits au corpus :",
                self.contre_exemples.len()
            );
            for chemin in &self.contre_exemples {
                println!("    {}", chemin.display());
            }
            println!(
                "  « l'évasion devient un test » (DEVOPS §3) : ces octets sont désormais des graines permanentes du corpus."
            );
        }
    }
}

/// Exécute une campagne de fuzz.
///
/// Fail-closed : un corpus illisible ou vide est une **erreur**, jamais un
/// ensemble vide silencieux — sinon la gate deviendrait verte en supprimant ce
/// qu'elle éprouve (même règle que `roles::fichiers_par_extension`).
pub fn executer(plan: &Plan) -> Result<Rapport, String> {
    let repertoire = plan.racine.join(CORPUS);
    let graines = charger_corpus(&repertoire)?;

    let mut generateur = SplitMix64::depuis(plan.graine);
    let mut distribution = Distribution::default();
    let mut contre_exemples: Vec<PathBuf> = Vec::new();
    let depart = Instant::now();

    // Passe 1 — chaque graine du corpus, telle quelle. Le corpus est la partie
    // dirigée de l'épreuve : elle doit s'exécuter en entier, budget ou pas.
    for (nom, octets) in &graines {
        eprouver_un_cas(
            octets,
            &mut distribution,
            &repertoire,
            &mut contre_exemples,
            &format!("corpus:{nom}"),
        )?;
    }

    // Passe 2 — mutations tirées, jusqu'à épuisement du budget.
    let mut tampon: Vec<u8> = Vec::new();
    while depart.elapsed() < plan.duree {
        // Un lot de cas entre deux lectures d'horloge : `Instant::now()` à
        // chaque cas dominerait le coût de l'épreuve elle-même.
        for _ in 0..256 {
            let index = if graines.is_empty() {
                0
            } else {
                (generateur.suivant() % (graines.len() as u64)) as usize
            };
            tampon.clear();
            if let Some((_, base)) = graines.get(index) {
                tampon.extend_from_slice(base);
            }
            muter(&mut tampon, &mut generateur);
            eprouver_un_cas(
                &tampon,
                &mut distribution,
                &repertoire,
                &mut contre_exemples,
                "tiré",
            )?;
        }
    }

    Ok(Rapport {
        graine: plan.graine,
        graines_du_corpus: graines.len(),
        ecoule: depart.elapsed(),
        distribution,
        contre_exemples,
    })
}

/// Un cas : l'appel sous `catch_unwind`, le classement, et l'écriture du
/// contre-exemple s'il y a panique.
fn eprouver_un_cas(
    octets: &[u8],
    distribution: &mut Distribution,
    repertoire: &Path,
    contre_exemples: &mut Vec<PathBuf>,
    origine: &str,
) -> Result<(), String> {
    // Le classement passe par `examiner_lot`, qui est ce que `eprouver`
    // appelle en premier : classer et éprouver sont le même chemin, jamais
    // deux implémentations qui pourraient diverger (R-3).
    let classement = std::panic::catch_unwind(|| {
        let examen = shogen_verifier::examiner_lot(octets);
        let (registre_ok, constat_ok) = match std::str::from_utf8(octets) {
            Ok(texte) => (
                shogen_verifier::analyser_registre(texte).is_ok(),
                shogen_verifier::analyser_constat(texte).is_ok(),
            ),
            Err(_) => (false, false),
        };
        shogen_verifier::eprouver(octets);
        (classe(&examen), registre_ok, constat_ok)
    });

    match classement {
        Ok((classe, registre_ok, constat_ok)) => {
            match classe {
                Classe::Refuse => distribution.refuses = distribution.refuses.saturating_add(1),
                Classe::NonCanonique => {
                    distribution.non_canoniques = distribution.non_canoniques.saturating_add(1);
                }
                Classe::Trivial => distribution.triviaux = distribution.triviaux.saturating_add(1),
                Classe::Canonique => {
                    distribution.canoniques = distribution.canoniques.saturating_add(1);
                }
            }
            if registre_ok {
                distribution.registres_acceptes = distribution.registres_acceptes.saturating_add(1);
            }
            if constat_ok {
                distribution.constats_acceptes = distribution.constats_acceptes.saturating_add(1);
            }
            Ok(())
        }
        Err(_) => {
            let chemin = ecrire_contre_exemple(repertoire, octets, origine)?;
            contre_exemples.push(chemin);
            Ok(())
        }
    }
}

enum Classe {
    Refuse,
    NonCanonique,
    Trivial,
    Canonique,
}

fn classe(examen: &shogen_verifier::Examen) -> Classe {
    match examen {
        shogen_verifier::Examen::Refuse(_) => Classe::Refuse,
        shogen_verifier::Examen::NonCanonique { .. } => Classe::NonCanonique,
        shogen_verifier::Examen::Trivial { .. } => Classe::Trivial,
        shogen_verifier::Examen::Canonique { .. } => Classe::Canonique,
    }
}

/// Écrit un contre-exemple au corpus. Le nom porte l'empreinte des octets :
/// deux fois le même contre-exemple ne fait pas deux fichiers, et le nom se
/// recalcule (`shogen_core::empreinte_sha256`, ADR-0018 — jamais une seconde
/// implémentation de SHA-256, R-3).
fn ecrire_contre_exemple(
    repertoire: &Path,
    octets: &[u8],
    origine: &str,
) -> Result<PathBuf, String> {
    let empreinte = shogen_core::empreinte_en_hexadecimal(&shogen_core::empreinte_sha256(octets));
    let court = empreinte.get(..16).unwrap_or(empreinte.as_str());
    let chemin = repertoire.join(format!("panique-{court}.bin"));
    std::fs::write(&chemin, octets).map_err(|erreur| {
        format!(
            "contre-exemple non écrit ({}) : {erreur} — une panique observée et non consignée serait pire que la panique",
            chemin.display()
        )
    })?;
    eprintln!(
        "PANIQUE observée (origine : {origine}) — {} octet(s) écrits dans {}",
        octets.len(),
        chemin.display()
    );
    Ok(chemin)
}

/// Écrit les graines **dirigées** du corpus — celles qui se déduisent des
/// formes que le dépôt connaît déjà.
///
/// « Corpus de graines committé et croissant » (ADR-0011 seuil 7) a deux
/// moitiés qui ne se remplacent pas. *Dirigée* : une forme que les tests
/// existants exercent déjà, écrite ici pour que le fuzz parte du bord de la
/// forme canonique plutôt que du bruit — un tirage aveugle qui part de zéro
/// n'atteint jamais un CBOR canonique de 87 octets. *Croissante* : chaque
/// panique observée ajoute ses octets au corpus, et cette moitié-là ne se
/// régénère pas — elle serait perdue si cette commande écrasait le
/// répertoire. Elle n'écrase donc que les fichiers `dirigee-*`.
pub fn ecrire_corpus_dirige(racine: &Path) -> Result<Vec<String>, String> {
    let repertoire = racine.join(CORPUS);
    std::fs::create_dir_all(&repertoire).map_err(|erreur| {
        format!(
            "création du corpus impossible ({}) : {erreur}",
            repertoire.display()
        )
    })?;

    let lot_trivial = shogen_core::encoder_temoignage(&crate::exemple::temoignage_exemple());
    let mut graines: Vec<(&str, Vec<u8>)> = Vec::new();

    // 1. Le lot d'exemple intact — la seule forme que le walking skeleton
    //    accepte, et le point de départ de toutes les mutations utiles.
    graines.push(("dirigee-lot-exemple.bin", lot_trivial.clone()));

    // 1 bis. Le témoignage **canonique** des sept champs (03 §1) — la forme
    //    la plus profonde du vérificateur : elle seule fait entrer le prédicat
    //    de `subject` (ADR-0016), la liaison au hash (ADR-0005) et les trois
    //    contrôles de 03 §4. Sans cette graine, un tirage aveugle n'atteint
    //    jamais cette classe : mesure du 2026-08-13, corpus sans elle, 20 s de
    //    fuzz — 22 057 486 cas exécutés, classe « sept champs » à **0**.
    let canonique = shogen_core::encoder_temoignage_canonique(&temoignage_canonique_exemple());
    graines.push(("dirigee-lot-canonique.bin", canonique.clone()));
    let mut canonique_mute = canonique.clone();
    if let Some(case) = canonique_mute.last_mut() {
        *case ^= 0xFF;
    }
    graines.push((
        "dirigee-lot-canonique-dernier-octet-mute.bin",
        canonique_mute,
    ));

    // 2. Les deux octets que le walking skeleton mute déjà (justfile,
    //    squelette.yml) : l'octet de structure 0 et l'octet 31.
    for (nom, index) in [
        ("dirigee-lot-octet-0-mute.bin", 0usize),
        ("dirigee-lot-octet-31-mute.bin", 31usize),
    ] {
        let mut octets = lot_trivial.clone();
        if let Some(case) = octets.get_mut(index) {
            *case = 255;
        }
        graines.push((nom, octets));
    }

    // 3. Troncature et octet en trop — les deux refus que les tests de bout en
    //    bout du vérificateur exercent nommément.
    let mut tronque = lot_trivial.clone();
    tronque.truncate(lot_trivial.len().saturating_div(2));
    graines.push(("dirigee-lot-tronque.bin", tronque));
    let mut en_trop = lot_trivial.clone();
    en_trop.push(0x00);
    graines.push(("dirigee-lot-octet-en-trop.bin", en_trop));

    // 4. Les bords du décodeur CBOR, un par forme que le cœur nomme en refus :
    //    entrée vide, longueur indéfinie (argument 31), argument non préféré,
    //    type majeur inattendu, carte de tête sans entrée.
    graines.push(("dirigee-cbor-vide.bin", Vec::new()));
    graines.push(("dirigee-cbor-longueur-indefinie.bin", alloc_octets(&[0xBF])));
    graines.push((
        "dirigee-cbor-argument-non-prefere.bin",
        alloc_octets(&[0xA3, 0x78, 0x06, b's', b'o', b'u', b'r', b'c', b'e']),
    ));
    graines.push((
        "dirigee-cbor-type-majeur-inattendu.bin",
        alloc_octets(&[0x83, 0x01, 0x02, 0x03]),
    ));
    graines.push(("dirigee-cbor-carte-vide.bin", alloc_octets(&[0xA0])));

    // 5. Les surfaces TEXTE — registre et constat. Elles consomment des octets
    //    tout autant que le lot, et la cible fuzz les couvre : le corpus doit
    //    donc porter des formes qui les font entrer, pas seulement du CBOR.
    graines.push((
        "dirigee-registre.txt",
        b"# registre publie\nA(exemple-residu-1)\nA(exemple-residu-2)\nA(transport-check-delegated)\n"
            .to_vec(),
    ));
    graines.push((
        "dirigee-registre-doublon.txt",
        b"A(exemple-residu-1)\nA(exemple-residu-1)\n".to_vec(),
    ));
    // 5 bis. Le constat, **au contrat d'ADR-0015 point 13** : une ligne JSON à
    //    clés triées, dix-huit clés. La graine porte la forme ACCEPTÉE — sans
    //    elle, l'analyseur du constat serait atteint par ses seuls premiers
    //    octets et jamais par sa construction finale (le contrôle de version,
    //    le verdict, les six longueurs). La seconde graine porte une forme
    //    refusée tard : hexadécimal de longueur impaire.
    graines.push((
        "dirigee-constat.txt",
        constat_dirige("041a2b3c").into_bytes(),
    ));
    graines.push((
        "dirigee-constat-hexadecimal-impair.txt",
        constat_dirige("041a2b3").into_bytes(),
    ));
    // 6. Les graines DISTILLÉES (13 §7 dette 3) : les formes que les campagnes instrumentées
    //    exerçaient, nommées (`crate::distillation`).
    let distillees = crate::distillation::graines();
    graines.extend(
        distillees
            .iter()
            .map(|g| (g.nom.as_str(), g.octets.clone())),
    );

    let mut journal = Vec::new();
    journal.push(format!("corpus dirigé : {}", repertoire.display()));
    for (nom, octets) in &graines {
        let chemin = repertoire.join(nom);
        std::fs::write(&chemin, octets)
            .map_err(|erreur| format!("écriture de {} impossible : {erreur}", chemin.display()))?;
        journal.push(format!("  {nom} : {} octet(s)", octets.len()));
    }
    journal.push(format!("{} graine(s) dirigée(s) écrite(s)", graines.len()));
    Ok(journal)
}

fn alloc_octets(octets: &[u8]) -> Vec<u8> {
    octets.to_vec()
}

/// Une graine de constat au contrat d'ADR-0015 point 13, dont seuls les
/// chiffres de la clé épinglée varient.
///
/// Les valeurs reprennent celles du témoignage canonique de référence
/// ci-dessous, aux mêmes empreintes tierces, pour que le corpus et la suite
/// parlent de la même forme. `empreinte_sent_revele_sha256` est l'empreinte de
/// la suite VIDE (vecteur mesuré du dépôt) : ce lot d'exemple ne porte aucun
/// octet émis, et les trois longueurs du sens émis valent zéro en conséquence.
pub(crate) fn constat_dirige(chiffres_de_la_cle: &str) -> String {
    format!(
        "{{\"attestor_cle_algorithme\":\"exemple\",\
\"attestor_cle_hex\":\"{chiffres_de_la_cle}\",\
\"connection_info_time\":1754000000,\
\"connection_info_version_tls\":\"V1_2\",\
\"empreinte_presentation_sha256\":\"9c114e983a7b36eddd59ad5584f40b8beddb04918e665107e8e362fcd0252c86\",\
\"empreinte_recv_revele_sha256\":\"04f501ade9aec2a345218a7264fe2dec87d2f0fbf7a6c500605dbc425a6fac9d\",\
\"empreinte_sent_revele_sha256\":\"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855\",\
\"octets_presentation\":23,\
\"revision_amont\":\"0000000000000000000000000000000000000000\",\
\"server_name\":\"api.example.com\",\
\"transcript_recv_authentifie\":17,\
\"transcript_recv_longueur\":17,\
\"transcript_recv_longueur_attestee\":17,\
\"transcript_sent_authentifie\":0,\
\"transcript_sent_longueur\":0,\
\"transcript_sent_longueur_attestee\":0,\
\"verdict\":\"presentation_verifiee\",\
\"version_du_constat\":1}}\n"
    )
}

/// Le témoignage canonique de référence du corpus — **une graine, pas un
/// oracle**.
///
/// Il est construit ici avec l'encodeur du cœur, alors que le test de bout en
/// bout du vérificateur écrit ses octets à la main. La différence est
/// délibérée et ne se confond pas : un **test** produit par l'encodeur qu'il
/// vérifie ne prendrait cet encodeur en défaut sur rien (le motif écrit en
/// tête de `crates/shogen-verifier/tests/temoignage_canonique.rs`) ; une
/// **graine de fuzz** n'a pas à prendre quoi que ce soit en défaut — elle a à
/// être une forme valide d'où partir. L'oracle du fuzz est ailleurs : c'est
/// l'absence de panique.
///
/// Les valeurs reprennent celles du test de bout en bout, aux mêmes empreintes
/// tierces, pour que le corpus et la suite parlent de la même forme.
pub(crate) fn temoignage_canonique_exemple() -> shogen_core::Temoignage {
    shogen_core::Temoignage {
        subject: String::from("https://api.example.com/v3/simple/price?ids=bitcoin"),
        attestor: vec![shogen_core::Attestor {
            // La convention d'épinglage de l'adapter : `<algorithme> <chiffres
            // hexadécimaux>` — les mêmes octets que la graine de constat
            // ci-dessus recompose, pour que le corpus porte la forme réelle.
            key: b"exemple 041a2b3c".to_vec(),
            identity: String::from("exemple:attestateur-1"),
        }],
        residual: vec![
            String::from("A(exemple-residu-1)"),
            String::from("A(exemple-residu-2)"),
        ],
        transport: String::from("exemple-transport/1"),
        utterance: shogen_core::Utterance {
            hash: shogen_core::empreinte_sha256(b"{\"price\":\"42.17\"}"),
            bytes: Some(b"{\"price\":\"42.17\"}".to_vec()),
        },
        observed_at: shogen_core::ObservedAt {
            clock: String::from("exemple:horloge-du-transport"),
            instant: 1_754_000_000,
        },
        transport_proof: b"preuve-opaque-d'exemple".to_vec(),
    }
}

/// Charge les graines du corpus, triées par nom pour que l'ordre soit un fait
/// du dépôt et non de l'ordre de lecture du système de fichiers.
fn charger_corpus(repertoire: &Path) -> Result<Vec<(String, Vec<u8>)>, String> {
    if !repertoire.is_dir() {
        return Err(format!(
            "corpus absent : {} — le corpus committé est une pièce de la gate (ADR-0011 seuil 7), son absence est ROUGE",
            repertoire.display()
        ));
    }
    let mut graines: Vec<(String, Vec<u8>)> = Vec::new();
    let entrees = std::fs::read_dir(repertoire)
        .map_err(|erreur| format!("corpus illisible {} : {erreur}", repertoire.display()))?;
    for entree in entrees {
        let entree = entree.map_err(|erreur| format!("entrée de corpus illisible : {erreur}"))?;
        let chemin = entree.path();
        if !chemin.is_file() {
            continue;
        }
        let nom = entree.file_name().to_string_lossy().into_owned();
        if nom.ends_with(".md") {
            continue;
        }
        let octets = std::fs::read(&chemin)
            .map_err(|erreur| format!("graine illisible {} : {erreur}", chemin.display()))?;
        graines.push((nom, octets));
    }
    if graines.is_empty() {
        return Err(format!(
            "corpus vide : {} — le harnais refuse de conclure sur un périmètre vide",
            repertoire.display()
        ));
    }
    graines.sort_by(|gauche, droite| gauche.0.cmp(&droite.0));
    Ok(graines)
}

/// Les opérateurs de mutation, tirés uniformément.
///
/// Ils sont volontairement pauvres et nommés : retournement de bit, écriture
/// d'octet, troncature, extension, découpe. C'est l'ensemble qu'un moteur
/// aveugle peut offrir ; un moteur guidé par la couverture choisit *où*
/// appliquer, et c'est exactement la différence que la consultation R-26 pose.
fn muter(tampon: &mut Vec<u8>, generateur: &mut SplitMix64) {
    // Entre 1 et 4 opérations par cas : une seule mutation atteint rarement
    // une forme canonique différente, quatre défont trop souvent la structure.
    let operations = 1 + (generateur.suivant() % 4);
    for _ in 0..operations {
        if tampon.is_empty() {
            tampon.push(generateur.suivant() as u8);
            continue;
        }
        let longueur = tampon.len();
        match generateur.suivant() % 5 {
            0 => {
                let index = (generateur.suivant() % (longueur as u64)) as usize;
                let bit = 1u8 << (generateur.suivant() % 8);
                if let Some(case) = tampon.get_mut(index) {
                    *case ^= bit;
                }
            }
            1 => {
                let index = (generateur.suivant() % (longueur as u64)) as usize;
                let valeur = generateur.suivant() as u8;
                if let Some(case) = tampon.get_mut(index) {
                    *case = valeur;
                }
            }
            2 => {
                let garde = (generateur.suivant() % (longueur as u64)) as usize;
                tampon.truncate(garde);
            }
            3 => {
                let combien = 1 + (generateur.suivant() % 8) as usize;
                for _ in 0..combien {
                    tampon.push(generateur.suivant() as u8);
                }
            }
            _ => {
                let coupe = (generateur.suivant() % (longueur as u64)) as usize;
                let queue: Vec<u8> = tampon.split_off(coupe);
                let repetitions = 1 + (generateur.suivant() % 3) as usize;
                for _ in 0..repetitions {
                    tampon.extend_from_slice(&queue);
                }
            }
        }
        // Borne dure : sans elle, l'opérateur d'extension fait croître le
        // tampon sans limite et le débit s'effondre au bout de quelques
        // minutes. La borne est un choix de budget, dit comme tel.
        if tampon.len() > 65_536 {
            tampon.truncate(65_536);
        }
    }
}

/// SplitMix64 — le générateur, écrit ici en entier plutôt qu'importé.
///
/// Motif : ADR-0012 D3 et R-8 ; le cœur et le vérificateur sont à zéro
/// dépendance, et faire entrer une crate de génération pseudo-aléatoire pour
/// **quatre lignes d'arithmétique** ferait payer un acteur de chaîne
/// d'approvisionnement de plus à l'outillage qui contrôle cette chaîne. Les
/// constantes sont celles de l'algorithme ; le rejeu est exact à graine égale,
/// sur toute plateforme, parce que tout y est en `wrapping_*` sur `u64` ET
/// que toute réduction se fait AVANT le cast en `usize` (revue G2 vague 1 :
/// `u64 as usize` tronque sur une cible 32 bits, et tronquer avant le modulo
/// changeait l'index tiré — le rejeu inter-plateformes en dépend).
struct SplitMix64 {
    etat: u64,
}

impl SplitMix64 {
    fn depuis(graine: u64) -> Self {
        Self { etat: graine }
    }

    fn suivant(&mut self) -> u64 {
        self.etat = self.etat.wrapping_add(0x9E37_79B9_7F4A_7C15);
        let mut z = self.etat;
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
        z ^ (z >> 31)
    }
}
