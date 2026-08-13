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
