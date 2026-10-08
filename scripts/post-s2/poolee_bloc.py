"""SHOGEN-POOLEE-BLOC-1 (a) (ADR-0028 annexe B.13 l.224) : plancher d'erreur-type par blocs de la strate poolée,
z_pool,bloc = Σ_s (K_s − n_s·P̂_more,s) / √(Σ_s σ̂²_bloc,s), les σ̂²_bloc,s de la règle scellée (B-DEP-1) sommés entre
strates disjointes, sur le J28, plage exclue. Publié si la strate poolée publie z_pool (r1.strate_poolee) et si chaque
strate publie z_bloc (r1.bloc_strate : σ̂² > 0, n_s ≥ 30·ℓ) ; sinon motif. Exploratoire, hors famille, hors décision ;
son niveau n'est pas mesuré (POOLEE-BLOC-1 (b), lot DETTES-SIM)."""
from __future__ import annotations

import sys
from decimal import Decimal, localcontext

import commun
from commun import dec, r1


def poolee_bloc(base: dict) -> dict:
    """Numérateur, variance sommée, z_pool,bloc (Decimal 50) et motif de non-publication, depuis une sortie de
    r1.compute_r1 ; lignes de sortie."""
    st, pool = base["strates"], base["poolee"]
    sans = [s for s, b in st.items() if b["bloc"]["z_bloc"] is None]
    motif = (f"strate poolée sans z_pool (r1.strate_poolee : {pool.get('motif')})" if pool["z_pool"] is None else
             f"z_bloc non publié dans : {', '.join(sans)}" if sans else None)
    num = var = z = None
    with localcontext(r1.contexte_decimal()):
        termes = {s: +(Decimal(b["K"]) - Decimal(b["n"]) * b["P_more"]) for s, b in st.items()}
        if motif is None:
            num = +sum(termes.values(), Decimal(0))
            var = +sum((b["bloc"]["sigma2_bloc"] for b in st.values()), Decimal(0))
            z = +(num / var.sqrt())
    lignes = ["[SHOGEN-POOLEE-BLOC-1 (a)] z_pool,bloc = Σ_s (K_s − n_s·P̂_more,s) / √(Σ_s σ̂²_bloc,s) (forme de l'annexe "
              "B.13) ; exploratoire, hors famille, hors décision ; niveau non mesuré (POOLEE-BLOC-1 (b), lot DETTES-SIM)",
              *(f"« {s} » : K_s − n_s·P̂_more,s = {dec(termes[s])} ; σ̂²_bloc,s = {dec(b['bloc']['sigma2_bloc'])}"
                for s, b in st.items()),
              f"Σ_s (K_s − n_s·P̂_more,s) = {dec(num)} (égal au numérateur de la strate poolée scellée : "
              f"{'oui' if num == pool.get('numerateur') else 'non'}) ; Σ_s σ̂²_bloc,s = {dec(var)}",
              f"z_pool,bloc = {dec(z)}" + (f" — non publié : {motif}" if motif else " — exploratoire, hors famille, "
                                           "hors décision ; z_pool (forme binomiale, rendu) = " + dec(pool["z_pool"]))]
    return {"numerateur": num, "variance": var, "z": z, "motif": motif, "lignes": lignes}


def main(argv: list) -> int:
    return commun.executer("poolee_bloc.py", "SHOGEN-POOLEE-BLOC-1 (a)", lambda d: poolee_bloc(d["base"])["lignes"],
                           argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
