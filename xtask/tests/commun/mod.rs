//! Les arbres temporaires des tests de `xtask` (SHOGEN-XTASK-TMP-NOMS-FIXES-1) : sous la cible cargo
//! de la copie (`CARGO_TARGET_TMPDIR`), à un nom unique (processus et rang), effacés à la fin du test,
//! panique comprise. Deux exécutions simultanées ne partagent aucun chemin, aucun dossier ne reste.

use std::path::{Path, PathBuf};
use std::sync::atomic::{AtomicUsize, Ordering};

pub struct Arbre(PathBuf);

impl Arbre {
    /// `<prefixe>-<cas>-<processus>-<rang>` sous `CARGO_TARGET_TMPDIR`.
    pub fn nouveau(prefixe: &str, cas: &str) -> Self {
        static RANG: AtomicUsize = AtomicUsize::new(0);
        let rang = RANG.fetch_add(1, Ordering::Relaxed);
        let nom = format!("{prefixe}-{cas}-{}-{rang}", std::process::id());
        Arbre::sur(PathBuf::from(env!("CARGO_TARGET_TMPDIR")).join(nom))
    }

    /// L'arbre au chemin donné, vidé de ce qu'un processus tué y aurait laissé.
    pub fn sur(chemin: PathBuf) -> Self {
        let _ = std::fs::remove_dir_all(&chemin);
        Arbre(chemin)
    }
}

impl std::ops::Deref for Arbre {
    type Target = PathBuf;
    fn deref(&self) -> &PathBuf {
        &self.0
    }
}

impl AsRef<Path> for Arbre {
    fn as_ref(&self) -> &Path {
        &self.0
    }
}

impl Drop for Arbre {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.0);
    }
}
