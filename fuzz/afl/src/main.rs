//! Cible AFL++ de [`shogen_verifier::eprouver`] — ADR-0011 seuil 7.
//!
//! # Zéro logique, même règle que la cible libFuzzer
//!
//! Les octets que le moteur produit sont passés à `eprouver`, tels quels.
//! Aucun filtrage, aucune troncature, aucune normalisation. La MÊME cible est
//! enrobée par les deux moteurs : ce qui diffère entre `fuzz/libfuzzer` et
//! `fuzz/afl` est le moteur, jamais ce qui est éprouvé.
//!
//! # Pourquoi deux moteurs plutôt qu'un
//!
//! Ratification mainteneur du 2026-08-13. libFuzzer et AFL++ n'explorent pas de
//! la même façon — instrumentation, ordonnancement des entrées, opérateurs de
//! mutation et stratégie de conservation diffèrent —, donc l'un atteint des
//! chemins que l'autre laisse. Le coût est publié : deux jobs CI de plus.
//!
//! # `fuzz!` et la persistance
//!
//! La macro `afl::fuzz!` place la boucle en mode **persistant** : le processus
//! est réutilisé d'une entrée à la suivante au lieu d'être reforké, ce qui est
//! ce qui rend le débit d'AFL++ comparable à celui de libFuzzer. Elle attrape
//! aussi les paniques pour les rendre au moteur comme des plantages — la
//! détection reste donc dans le moteur, jamais dans la bibliothèque `no_std`
//! du vérificateur (ADR-0009 point 6).
//!
//! # Ce qu'un vert de cette cible dit, et rien de plus
//!
//! *tested* — sur les cas exécutés, avec leur compte, leur corpus de départ et
//! leur budget, à la date. Jamais *proven* (ADR-0010, §Coûts point 6).

fn main() {
    afl::fuzz!(|octets: &[u8]| {
        shogen_verifier::eprouver(octets);
    });
}
