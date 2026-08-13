//! `shogen-tlsn-session` — UNE session MPC-TLS attestée contre une source réelle.
//!
//! Rattachement (G0) : **ADR-0015 pt 2** (mode Notary : attestation →
//! présentation) ; **ADR-0015 pt 3** (le rôle de Notary est joué par un
//! processus opéré par Shōgen, construit depuis la bibliothèque amont épinglée,
//! et non par un service hébergé — le serveur notaire amont est déprécié depuis
//! alpha.13) ; **ADR-0015 pt 4** (le résidu A(self-attestation)) ;
//! **ADR-0001** (adapter : testé, jamais prouvé) ;
//! **10-mesures-pilotes-design §3.1** (le pool de sources).
//!
//! ## Ce que ce binaire fait, en trois temps
//!
//! 1. **Notarisation.** Deux tâches d'un même processus — le *Prover* et le
//!    *Verifier acting as Attestor* — reliées par un tube en mémoire, conduisent
//!    ensemble la session MPC-TLS vers l'endpoint réel. Le Notary signe une
//!    attestation.
//! 2. **Présentation.** Le Prover construit une présentation qui **révèle la
//!    totalité** du transcript, dans les deux sens. Le motif est le contrôle (b)
//!    d'ADR-0015 pt 8 : le hash des octets révélés doit lier le témoignage à sa
//!    preuve, et une révélation partielle laisserait dans le tampon des octets
//!    non authentifiés dont l'empreinte ne lierait rien. Aucune donnée sensible
//!    ne circule ici : l'endpoint est public, en lecture seule, sans clé.
//! 3. **Dépôt.** Attestation, secrets et présentation sont écrits sur disque,
//!    ainsi que la clé de vérification du notaire — c'est elle que le témoignage
//!    épinglera dans son champ `attestor`.
//!
//! ## Ce que ce binaire NE démontre PAS
//!
//! La neutralité du notaire. Le notaire est ici Shōgen lui-même, c'est-à-dire la
//! partie dont 02-vision exige qu'on ne lui fasse pas confiance. C'est
//! exactement A(self-attestation) (registre 08, ADR-0015 pt 4). La clé de
//! signature est de surcroît **dérivée d'une graine publique écrite dans ce
//! fichier** : quiconque lit ce code peut signer une attestation qui passera la
//! vérification. Ce n'est pas un défaut à corriger, c'est le résidu à afficher —
//! S3 démontre la chaîne et la forme de l'artefact, pas la neutralité.

use std::{future::IntoFuture, time::Duration};

use futures::io::{AsyncReadExt as _, AsyncWriteExt as _};
use http_body_util::Empty;
use hyper::{Request, StatusCode, body::Bytes};
use hyper_util::rt::TokioIo;
use sha2::{Digest as _, Sha256};
use tokio::io::{AsyncRead, AsyncWrite};
use tokio_util::compat::{FuturesAsyncReadCompatExt, TokioAsyncReadCompatExt};

use tlsn::{
    Session,
    attestation::{
        Attestation, AttestationConfig, CryptoProvider,
        request::{Request as AttestationRequest, RequestConfig},
        signing::Secp256k1Signer,
    },
    config::{
        prove::ProveConfig, prover::ProverConfig, tls::TlsClientConfig,
        tls_commit::mpc::MpcTlsConfig, verifier::VerifierConfig,
    },
    connection::{CertBinding, ConnectionInfo, HandshakeData, ServerName, TranscriptLength},
    prover::ProverOutput,
    transcript::{ContentType, TranscriptCommitConfig},
    verifier::{VerifierCommitStart, VerifierOutput},
    webpki::RootCertStore,
};

/// La source interrogée — ligne 1 de la table 10 §3.1 (« Binance »,
/// `api.binance.com/api/v3/ticker/price?symbol=BTCUSDT`, sans clé, HTTP 200,
/// place primaire), reprise à l'octet près et non paraphrasée.
///
/// Le choix parmi les 11 sources répondantes est motivé : la réponse est la plus
/// courte du pool (un objet à deux champs), et le coût du protocole MPC croît
/// avec la taille du transcript.
const HOTE: &str = "api.binance.com";
const PORT: u16 = 443;
const CIBLE: &str = "/api/v3/ticker/price?symbol=BTCUSDT";

/// Bornes de préparation du protocole MPC (le matériel est préprocessé avant la
/// connexion ; les réduire améliore la performance). Valeurs de l'amont épinglé,
/// `crates/examples/src/lib.rs` : `1 << 12` et `1 << 14`.
const MAX_OCTETS_ENVOYES: usize = 1 << 12;
const MAX_OCTETS_RECUS: usize = 1 << 14;

/// Graine de la clé de signature du notaire. **Publique et documentée** — voir
/// l'avertissement en tête de fichier. Elle est dérivée d'une chaîne du projet
/// plutôt que prise à l'exemple amont (`[1u8; 32]`) pour qu'une attestation
/// Shōgen ne se confonde jamais avec une attestation de démonstration amont.
const GRAINE_DU_NOTAIRE: &[u8] = b"shogen-s3-notaire-de-demonstration-adr-0015";

type Erreur = Box<dyn std::error::Error + Send + Sync>;

#[tokio::main]
async fn main() -> Result<(), Erreur> {
    tracing_subscriber::fmt::init();

    let prefixe = std::env::args()
        .nth(1)
        .unwrap_or_else(|| "shogen-s3-binance".to_string());

    // Le tube en mémoire qui relie les deux rôles. Le Notary est une tâche du
    // même processus : c'est le montage « Verifier acting as Attestor » du
    // Quick Start amont, sans service hébergé (ADR-0015 pt 3).
    let (tube_notaire, tube_prouveur) = tokio::io::duplex(1 << 23);

    let tache_notaire = tokio::spawn(async move { notaire(tube_notaire).await });

    prouveur(tube_prouveur, &prefixe).await?;

    tache_notaire.await??;

    Ok(())
}

async fn prouveur<S>(tube: S, prefixe: &str) -> Result<(), Erreur>
where
    S: AsyncWrite + AsyncRead + Send + Sync + Unpin + 'static,
{
    let session = Session::new(tube.compat());
    let (pilote, mut poignee) = session.split();
    let tache_pilote = tokio::spawn(pilote);

    let prouveur = poignee
        .new_prover(ProverConfig::builder().build()?)?
        .commit(
            MpcTlsConfig::builder()
                .max_sent_data(MAX_OCTETS_ENVOYES)
                .max_recv_data(MAX_OCTETS_RECUS)
                .build()?,
        )
        .await?;

    let prise = tokio::net::TcpStream::connect((HOTE, PORT)).await?;
    // Désactive l'algorithme de Nagle pour réduire la latence de protocole
    // (note de performance de la crate `tlsn` amont).
    prise.set_nodelay(true)?;

    let (connexion_tls, prouveur) = prouveur.connect(
        TlsClientConfig::builder()
            .server_name(ServerName::Dns(HOTE.try_into()?))
            // Racines Mozilla de l'amont (`RootCertStore::mozilla()`, feature
            // `mozilla-certs`) : la source est publique, sa chaîne se valide
            // contre le magasin public, aucun certificat de fixture ici.
            .root_store(RootCertStore::mozilla())
            .build()?,
        prise.compat(),
    )?;
    let connexion_tls = TokioIo::new(connexion_tls.compat());

    let tache_prouveur = tokio::spawn(prouveur.into_future());

    let (mut emetteur, connexion) = hyper::client::conn::http1::handshake(connexion_tls).await?;
    tokio::spawn(connexion);

    let requete = Request::builder()
        .uri(CIBLE)
        .header("Host", HOTE)
        .header("Accept", "*/*")
        // « identity » demande au serveur de ne pas compresser : l'outillage
        // TLSNotary ne traite pas la compression (commentaire amont).
        .header("Accept-Encoding", "identity")
        .header("Connection", "close")
        // User-Agent neutre et nommé : rien d'un identifiant, rien d'un
        // navigateur usurpé.
        .header("User-Agent", "shogen-tlsn-session/0.0.0")
        .body(Empty::<Bytes>::new())?;

    let reponse = emetteur.send_request(requete).await?;
    let statut = reponse.status();
    if statut != StatusCode::OK {
        return Err(format!("la source a répondu {statut}, attendu 200").into());
    }

    let mut prouveur = tache_prouveur.await??;

    let (longueur_envoyee, longueur_recue) = prouveur.transcript().len();
    println!(
        "session conduite : {HOTE}{CIBLE} — statut {statut}, \
         transcript envoyé {longueur_envoyee} octets, reçu {longueur_recue} octets"
    );

    // Engagement sur la TOTALITÉ du transcript, dans les deux sens : c'est la
    // condition pour pouvoir tout révéler ensuite (motif au module).
    let mut constructeur = TranscriptCommitConfig::builder(prouveur.transcript());
    constructeur.commit_sent(&(0..longueur_envoyee))?;
    constructeur.commit_recv(&(0..longueur_recue))?;
    let engagement = constructeur.build()?;

    let mut constructeur = RequestConfig::builder();
    constructeur.transcript_commit(engagement);
    let configuration_de_requete = constructeur.build()?;

    let mut constructeur = ProveConfig::builder(prouveur.transcript());
    if let Some(configuration) = configuration_de_requete.transcript_commit() {
        constructeur.transcript_commit(configuration.clone());
    }
    let configuration_de_divulgation = constructeur.build()?;

    let ProverOutput {
        transcript_commitments,
        transcript_secrets,
        ..
    } = prouveur.prove(&configuration_de_divulgation).await?;

    let transcript_du_prouveur = prouveur.transcript().clone();
    let transcript_tls = prouveur.tls_transcript().clone();
    prouveur.close().await?;

    let mut constructeur = AttestationRequest::builder(&configuration_de_requete);
    constructeur
        .server_name(ServerName::Dns(HOTE.try_into()?))
        .handshake_data(HandshakeData {
            certs: transcript_tls
                .server_cert_chain()
                .ok_or("chaîne de certificats absente du transcript TLS")?
                .to_vec(),
            sig: transcript_tls
                .server_signature()
                .ok_or("signature serveur absente du transcript TLS")?
                .clone(),
            binding: transcript_tls.certificate_binding().clone(),
        })
        .transcript(transcript_du_prouveur)
        .transcript_commitments(transcript_secrets, transcript_commitments);

    let (requete_attestation, secrets) = constructeur.build(&CryptoProvider::default())?;

    poignee.close();
    let mut tube = tache_pilote.await??;

    tube.write_all(&bincode::serialize(&requete_attestation)?)
        .await?;
    tube.close().await?;

    let mut octets_attestation = Vec::new();
    tube.read_to_end(&mut octets_attestation).await?;
    let attestation: Attestation = bincode::deserialize(&octets_attestation)?;

    let fournisseur = CryptoProvider::default();
    // Contrôle de cohérence entre ce que le notaire a signé et ce que le
    // prouveur a vu. Un désaccord fait échouer ici, avant tout dépôt.
    requete_attestation.validate(&attestation, &fournisseur)?;

    std::fs::write(
        format!("{prefixe}.attestation.tlsn"),
        bincode::serialize(&attestation)?,
    )?;
    std::fs::write(
        format!("{prefixe}.secrets.tlsn"),
        bincode::serialize(&secrets)?,
    )?;

    // ---- Présentation : tout révéler, dans les deux sens ----
    let mut constructeur = secrets.transcript_proof_builder();
    constructeur.reveal_sent(&(0..longueur_envoyee))?;
    constructeur.reveal_recv(&(0..longueur_recue))?;
    let preuve_de_transcript = constructeur.build()?;

    let mut constructeur = attestation.presentation_builder(&fournisseur);
    constructeur
        .identity_proof(secrets.identity_proof())
        .transcript_proof(preuve_de_transcript);
    let presentation = constructeur.build()?;

    std::fs::write(
        format!("{prefixe}.presentation.tlsn"),
        bincode::serialize(&presentation)?,
    )?;

    // La clé de vérification du notaire, sous la forme exacte que le compagnon
    // imprimera : c'est ce que le témoignage épinglera dans `attestor`.
    let clef = presentation.verifying_key();
    let clef_hex = en_hexadecimal(&clef.data);
    std::fs::write(
        format!("{prefixe}.attestor-verifying-key.txt"),
        format!("{} {}\n", clef.alg, clef_hex),
    )?;

    println!("attestation, secrets et présentation déposés sous le préfixe « {prefixe} »");
    println!("clé de vérification du notaire : {} {}", clef.alg, clef_hex);

    Ok(())
}

async fn notaire<S>(tube: S) -> Result<(), Erreur>
where
    S: AsyncWrite + AsyncRead + Send + Sync + Unpin + 'static,
{
    let session = Session::new(tube.compat());
    let (pilote, mut poignee) = session.split();
    let tache_pilote = tokio::spawn(pilote);

    let configuration = VerifierConfig::builder()
        .root_store(RootCertStore::mozilla())
        .build()?;

    let verificateur = match poignee.new_verifier(configuration)?.commit().await? {
        VerifierCommitStart::Mpc(verificateur) => verificateur.accept().await?.run().await?,
        VerifierCommitStart::Proxy(verificateur) => {
            // Refus nommé : ADR-0015 pt 1 fixe le transport à `tlsn-mpc/1`.
            // Le mode proxy est un AUTRE transport, avec un autre résidu ; il
            // n'entre pas ici par accident.
            verificateur
                .reject(Some("le transport de S3 est tlsn-mpc/1 (ADR-0015 pt 1)"))
                .await?;
            return Err("configuration de protocole refusée : mode proxy proposé".into());
        }
    };

    let (
        VerifierOutput {
            transcript_commitments,
            ..
        },
        verificateur,
    ) = verificateur.verify().await?.accept().await?;

    let transcript_tls = verificateur.tls_transcript().clone();
    verificateur.close().await?;

    let longueur_envoyee = longueur_des_donnees_applicatives(transcript_tls.sent());
    let longueur_recue = longueur_des_donnees_applicatives(transcript_tls.recv());

    poignee.close();
    let mut tube = tache_pilote.await??;

    let mut octets_de_requete = Vec::new();
    tube.read_to_end(&mut octets_de_requete).await?;
    let requete: AttestationRequest = bincode::deserialize(&octets_de_requete)?;

    // Clé de signature dérivée d'une graine publique (voir l'avertissement en
    // tête de module). SHA-256 de la graine donne les 32 octets scalaires.
    let mut hacheur = Sha256::new();
    hacheur.update(GRAINE_DU_NOTAIRE);
    let graine: [u8; 32] = hacheur.finalize().into();
    let clef_de_signature = k256::ecdsa::SigningKey::from_bytes(&graine.into())?;
    let signataire = Box::new(Secp256k1Signer::new(&clef_de_signature.to_bytes())?);
    let mut fournisseur = CryptoProvider::default();
    fournisseur.signer.set_signer(signataire);

    let mut constructeur = AttestationConfig::builder();
    constructeur.supported_signature_algs(Vec::from_iter(fournisseur.signer.supported_algs()));
    let configuration = constructeur.build()?;

    let CertBinding::V1_2(liaison) = transcript_tls.certificate_binding() else {
        return Err("version de liaison de certificat non supportée".into());
    };

    let mut constructeur = Attestation::builder(&configuration).accept_request(requete)?;
    constructeur
        .connection_info(ConnectionInfo {
            time: transcript_tls.time(),
            version: transcript_tls.version(),
            transcript_length: TranscriptLength {
                sent: longueur_envoyee as u32,
                received: longueur_recue as u32,
            },
        })
        .server_ephemeral_key(liaison.server_ephemeral_key.clone())
        .transcript_commitments(transcript_commitments);

    let attestation = constructeur.build(&fournisseur)?;

    tube.write_all(&bincode::serialize(&attestation)?).await?;
    tube.close().await?;

    // Laisse au prouveur le temps de lire avant que la tâche ne rende la main.
    tokio::time::sleep(Duration::from_millis(0)).await;

    Ok(())
}

fn longueur_des_donnees_applicatives<'a, I>(enregistrements: I) -> usize
where
    I: IntoIterator<Item = &'a tlsn::transcript::Record>,
{
    enregistrements
        .into_iter()
        .filter_map(|enregistrement| match enregistrement.typ {
            ContentType::ApplicationData => Some(enregistrement.ciphertext.len()),
            _ => None,
        })
        .sum()
}

fn en_hexadecimal(octets: &[u8]) -> String {
    const CHIFFRES: &[u8; 16] = b"0123456789abcdef";
    let mut sortie = String::with_capacity(octets.len() * 2);
    for octet in octets {
        sortie.push(CHIFFRES[usize::from(octet >> 4)] as char);
        sortie.push(CHIFFRES[usize::from(octet & 0x0f)] as char);
    }
    sortie
}
