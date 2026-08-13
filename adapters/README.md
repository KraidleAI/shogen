Un adapter par transport d'attestation (ADR-0001) — **aucun n'existe en S2.5** (12 §1, non-objet 1) : ce répertoire est vide par décision, et le vérificateur n'aura jamais d'arête vers lui (gate S-G2).

**Amendement du 2026-08-13 (S3 phase C, chantier T).** Le répertoire n'est plus
vide : `shogen-tlsn-verify/` porte le binaire compagnon de vérification du
transport `tlsn-mpc/1` (ADR-0015 pt 7) et, sous `session/`, le conducteur de la
session attestée (ADR-0015 pts 2-3). La seconde moitié de la phrase ci-dessus,
elle, **tient sans changement et se mesure** : ce sont deux workspaces
INDÉPENDANTS, avec leurs propres `Cargo.lock` ; le workspace racine ne les
compte pas parmi ses membres, et `cargo tree -p shogen-verifier -e normal`
rend toujours **2 lignes** (`shogen-verifier` → `shogen-core`, une seule arête)
après leur écriture — mesure du 2026-08-13. Le détail est dans
`shogen-tlsn-verify/MESURE-R8.md`.

**Amendement du 2026-08-13 (S3 phase C, chantier Y — fusion orchestrateur).**
`shogen-typer/` porte le premier typeur (JSON → fait prix typé, endpoint
épinglé : ticker Coinbase Exchange BTC-USD, 10 §3.1 ligne 2) — même patron :
workspace autonome à `Cargo.lock` propre, hors membres du workspace racine,
zéro dépendance nouvelle (la seule directe est `shogen-core` par chemin,
la seule de dev `proptest =1.11.0`, déjà contrôlée R-8 en S2.5). L'identité
du typeur va dans le fait, jamais dans le témoignage (03 §3) ; détail dans
`shogen-typer/NOTES.md`. La re-mesure des 2 lignes ci-dessus a été refaite
APRÈS l'écriture du typeur (rapport chantier Y, 2026-08-13) : inchangée.

**Amendement du 2026-08-13 (S3 phase C, chantier V).**
`shogen-temoignage/` porte le **constructeur du témoignage canonique** : il lit
les artefacts déposés d'une session attestée (les fixtures du compagnon) et
écrit **un lot** aux sept champs de 03 §1, `subject` canonicalisé une fois à la
construction (ADR-0016 C0), chaque liaison recoupée contre le constat du
compagnon. C'est le rang que l'ADR-0016 C0 désigne — « la normalisation a lieu
une fois, à la construction, dans l'adapter » — et il ne pouvait donc vivre ni
au cœur ni au vérificateur.

Même patron que les deux précédents, et **mesuré, pas déclaré** (2026-08-13) :

* **workspace autonome**, `Cargo.lock` propre, hors des membres du workspace
  racine (ADR-0012 D1) ;
* **zéro dépendance tierce** — `cargo tree -e normal` rend **2 lignes**
  (`shogen-temoignage` → `shogen-core`, une seule arête), et
  `cargo tree -e normal,dev` rend **les mêmes 2 lignes** : la table
  `[dev-dependencies]` est vide. R-8 n'a donc rien à instruire (il n'y a pas
  d'installation) et aucun `deny.toml` local n'est dû, exactement comme pour
  `shogen-typer` ;
* **re-mesure de la phrase du haut**, refaite APRÈS l'écriture de cet adapter :
  `cargo tree -p shogen-verifier -e normal` rend toujours **2 lignes**. La
  seconde moitié de la phrase d'origine — « le vérificateur n'aura jamais
  d'arête vers lui » — tient donc au troisième adapter comme au premier.

Le binaire est exercé par `tests/binaire.rs` (run nominal comparé au sha256 du
lot versionné, trois fixtures abîmées sur copies temporaires) et par le job CI
`.github/workflows/temoignage.yml`, deux plateformes, seuil de couverture
bloquant ≥ 60 % lignes (ADR-0011 seuil 2 ; mesure du 2026-08-13 : **90,51 %**).
