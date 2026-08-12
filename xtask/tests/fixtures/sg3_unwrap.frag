
// Mutant semé (S-G3) : une forme qui diverge au lieu de refuser.
fn mutant_seme_sg3_unwrap() -> u8 {
    let valeur: Option<u8> = None;
    valeur.unwrap()
}
