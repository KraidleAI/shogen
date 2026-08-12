// Mutant semé (couverture) : un fichier NOUVEAU sous le répertoire du rôle.
// Une gate qui travaillerait sur une liste figée de fichiers le manquerait ;
// la sélection est par répertoire à chemin exact, récursive.
fn mutant_seme_dans_un_fichier_neuf() -> u8 {
    let valeur: Option<u8> = None;
    valeur.unwrap()
}
