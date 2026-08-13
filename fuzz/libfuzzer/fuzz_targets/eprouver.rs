//! Cible libFuzzer de [`shogen_verifier::eprouver`] — ADR-0011 seuil 7.
//!
//! # Zéro logique
//!
//! Ce fichier ne fait qu'une chose : passer les octets que le moteur produit à
//! `eprouver`, tels quels. Il ne filtre pas, ne tronque pas, ne normalise pas,
//! ne pré-décode pas. Un harnais qui ferait l'une de ces choses éprouverait un
//! vérificateur qui n'existe pas — et le seuil « zéro panique sur **toute**
//! suite d'octets » porte sur toute suite d'octets, pas sur celles qu'un
//! harnais aurait bien voulu laisser passer.
//!
//! # Ce que ce moteur ajoute au harnais en arbre
//!
//! `xtask/src/fuzz.rs` tire des mutations **aveugles** depuis le corpus
//! committé : il ne voit pas quelles branches un cas atteint, donc il n'apprend
//! rien d'une exécution à la suivante. libFuzzer est guidé par la
//! **couverture** : il conserve les entrées qui atteignent un bord nouveau et
//! mute à partir d'elles. La classe utile du harnais aveugle a été mesurée à
//! 1,8216 % (docs/13 §7 dette 2) ; c'est précisément l'écart que ce moteur
//! travaille.
//!
//! # Ce qu'un vert de cette cible dit, et rien de plus
//!
//! *tested* — sur les cas exécutés, avec leur compte, leur corpus de départ et
//! leur budget, à la date. Jamais *proven* : l'absence de panique n'est pas
//! établie (ADR-0010, §Coûts point 6). Un moteur guidé par la couverture
//! change la probabilité d'atteindre un chemin profond ; il ne change pas la
//! nature de ce qu'une campagne conclut.
//!
//! # Le partage `panic` / logique
//!
//! `eprouver` est totale, `no_std`, sans I/O (ADR-0009 point 6). La détection
//! de panique vit dans le moteur, jamais dans la bibliothèque — même partage
//! que le `catch_unwind` de la coquille `xtask`.

#![no_main]

use libfuzzer_sys::fuzz_target;

fuzz_target!(|octets: &[u8]| {
    shogen_verifier::eprouver(octets);
});
