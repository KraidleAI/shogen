"""Adaptateur d'oracle r1 de f35a70c (G0 docs/adr-0029/g0-sim/G0-SIM-BIS.md ; sous-lot SB-14 ; E-S-01, E-S-39 ;
T-FIV-1, T-CAL-2 ; SHOGEN-SIM-BIS-WINDOW-EPINGLE-1) : les cinq modules épinglés du harnais de S2 au commit d'analyse
(section « oracle_r1 » de parametres.json, empreintes égales à celles de PLAN-S2BIS) sont lus dans le dépôt par
`git archive` (lecture seule, aucun verrou), extraits dans un dossier temporaire sous TMPDIR, contrôlés par sha256 avant
tout chargement (forme de scripts/plan-s2bis/commun.py, importer_harnais), puis chargés sous le nom shogen_s2 sans
toucher sys.path ; seuls ces fichiers peuvent être chargés. Rend r1 et window (calendrier de S2). SB-14a :
extraction et chargement. SB-14b : FIV_série de r1 (block_long_run_variance, forme d'episodes.courbe de PLAN-S2BIS)
sur la même entrée que calib_fiv.courbe. Adaptateur : jamais importé par le moteur (E-S-01, tests/test_fitness.py) ;
ni puissance, ni hasard, ni libm (tests/test_fitness_tirages.py)."""
import atexit
import hashlib
import importlib
import importlib.util
import io
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
from decimal import localcontext

import commun

_CHARGE: dict = {}


def extraire(prm: dict, dossier: str, depot: str = commun.RACINE) -> str:
    """Fichiers épinglés du harnais au commit de la section « oracle_r1 », lus par `git --no-optional-locks -C <depot>
    archive` et écrits sous `dossier` ; seuls les membres attendus, fichiers réguliers, sont lus (aucune extraction
    d'archive en bloc). git absent, commit ou fichier introuvable : ORACLE/extraction ; empreinte différente de
    l'épingle : ORACLE/sha256. Rend le chemin du paquet shogen_s2 extrait."""
    commun.garde_campagne()
    o = prm["oracle_r1"]
    chemins = {f"{o['dossier']}/{f}": f for f in sorted(o["fichiers"])}
    try:
        p = subprocess.run(["git", "--no-optional-locks", "-C", depot, "archive", "--format=tar", o["commit"], "--",
                            *chemins], capture_output=True, timeout=120, check=False)
    except (OSError, subprocess.SubprocessError) as e:
        raise commun.Refus("ORACLE/extraction", f"git : {type(e).__name__}") from None
    if p.returncode:
        raise commun.Refus("ORACLE/extraction", f"git archive {o['commit'][:12]} : sortie {p.returncode}")
    with tarfile.open(fileobj=io.BytesIO(p.stdout)) as tar:
        lus = {m.name: tar.extractfile(m).read() for m in tar.getmembers() if m.isreg() and m.name in chemins}
    for chemin, f in chemins.items():
        if chemin not in lus or hashlib.sha256(lus[chemin]).hexdigest() != o["fichiers"][f]:
            raise commun.Refus("ORACLE/sha256", f"{chemin} : absent ou différent de l'épingle")
    for chemin, octets in lus.items():
        os.makedirs(os.path.dirname(os.path.join(dossier, chemin)), exist_ok=True)
        with open(os.path.join(dossier, chemin), "wb") as g:
            g.write(octets)
    return os.path.join(dossier, o["dossier"], "shogen_s2")


def charger(prm: dict) -> dict:
    """{"r1", "window"} du harnais extrait (extraire), une fois par processus ; dossier temporaire retiré à la sortie.
    Paquet shogen_s2 chargé par importlib sous son nom ; un shogen_s2 déjà chargé d'ailleurs, ou un module chargé hors
    des fichiers épinglés : ORACLE/modules."""
    if not _CHARGE:
        dossier = tempfile.mkdtemp(prefix="oracle_r1_")
        atexit.register(shutil.rmtree, dossier, True)
        paquet = extraire(prm, dossier)
        if "shogen_s2" in sys.modules:
            raise commun.Refus("ORACLE/modules", "shogen_s2 déjà chargé hors de l'extraction")
        spec = importlib.util.spec_from_file_location("shogen_s2", os.path.join(paquet, "__init__.py"),
                                                      submodule_search_locations=[paquet])
        sys.modules["shogen_s2"] = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(sys.modules["shogen_s2"])
        mods = {n: importlib.import_module(f"shogen_s2.{n}") for n in ("r1", "window")}
        epingles = {os.path.realpath(os.path.join(dossier, prm["oracle_r1"]["dossier"], f))
                    for f in prm["oracle_r1"]["fichiers"]}
        charges = {os.path.realpath(m.__file__) for n, m in list(sys.modules.items()) if n.split(".")[0] == "shogen_s2"}
        if charges - epingles:
            raise commun.Refus("ORACLE/modules", f"modules hors des fichiers épinglés : {sorted(charges - epingles)}")
        _CHARGE.update(mods)
    return dict(_CHARGE)


def courbe(h: dict, pres: int, val: int, ells: list, w: int) -> list:
    """FIV_série de r1 extrait sur la même entrée que calib_fiv.courbe : série [(w·j, I_j)] des positions j présentes
    (masque pres ; I_j = bit j de val), puis, par ℓ, r1.block_long_run_variance et FIV_serie = +(σ̂²_bloc/γ̂₀) sous
    r1.contexte_decimal() (forme d'episodes.courbe de PLAN-S2BIS) ; None si n = 0 ou γ̂₀ = 0."""
    r1, bp = h["r1"], format(pres, "b")[::-1]
    bv = format(val, "b")[::-1].ljust(len(bp), "0")
    serie = [(w * j, int(bv[j])) for j in range(len(bp)) if bp[j] == "1"]
    out = []
    for ell in ells:
        v = r1.block_long_run_variance(serie, w, ell)
        with localcontext(r1.contexte_decimal()):
            fs = None if not v["n"] or v["gamma0"] == 0 else +(v["sigma2_bloc"] / v["gamma0"])
        out.append({"ell": ell, "n": v["n"], "K": v["K"], "numerateur": v["numerateur"], "gamma0": v["gamma0"],
                    "sigma2_bloc": v["sigma2_bloc"], "FIV_serie": fs})
    return out
