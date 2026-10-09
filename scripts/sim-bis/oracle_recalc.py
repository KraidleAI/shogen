"""Adaptateur d'oracle croisé avec RECALC-BIS (G0 docs/adr-0029/g0-sim/G0-SIM-BIS.md ; sous-lot SB-13, première passe ;
E-S-01, E-S-51 ; contrat docs/adr-0029/s2bis/ROTATION-S2BIS.md ; SHOGEN-SIM-BIS-CONTRAT-RB6-1) : les fichiers épinglés
du paquet s2bis au commit cité (section « oracle_recalc » de parametres.json : shogen_s2bis.recalc.rotation de RB-6,
son chargeur config_analyse, config/analyse.json et les tests de RB-6, lus comme texte) sont lus dans le dépôt par
`git archive` (lecture seule, aucun verrou), contrôlés par sha256 avant toute écriture, puis écrits dans un
dossier donné (forme d'oracle_r1). SB-13a : épingle et extraction. Adaptateur : jamais importé par le moteur
(E-S-01, tests/test_fitness.py) ; ni puissance, ni hasard, ni libm (tests/test_fitness_tirages.py)."""
import hashlib
import io
import os
import subprocess
import tarfile

import commun


def extraire(prm: dict, dossier: str, depot: str = commun.RACINE) -> str:
    """Fichiers épinglés du paquet au commit de la section « oracle_recalc », lus par `git --no-optional-locks -C
    <depot> archive` et écrits sous `dossier` ; seuls les membres attendus, fichiers réguliers, sont lus (aucune
    extraction d'archive en bloc). Le dépôt doit porter le commit (historique complet en CI, Q-T4-11). Variable de la
    copie scellée posée : CAMPAGNE/variable ; git absent, commit ou fichier introuvable : ORACLE/extraction ; empreinte
    différente de l'épingle : ORACLE/sha256. Rend le chemin du dossier du paquet extrait (s2bis)."""
    commun.garde_campagne()
    o = prm["oracle_recalc"]
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
    return os.path.join(dossier, o["dossier"])
