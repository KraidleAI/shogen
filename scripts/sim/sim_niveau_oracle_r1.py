"""SHOGEN-SIM-NIVEAU-1, sous-lot SIM-NIVEAU-b : adaptateur d'oracle contre r1 (G0 du lot, §8 (4a) et (4)) et oracle (4b).
(4a) : plug-in, garde et z de sim_niveau_calc contre r1 à f5b8269, sur les 10 premières réplications de chaque cas.
Les p̂_i sont recalculés comme dans r1.compute_r1 (r1.py l.450-452) ; égalité exacte des Decimal (== et str) de p̂_i,
P̂₀, P̂₁, P̂_more (r1.poisson_binomial), de la garde (r1.gate_value), de la valeur de garde (r1.insufficient_history)
et de z (r1.z_score, garde tenue). (4) : σ̂² contre r1.block_long_run_variance, absente à f5b8269 : item
SHOGEN-SIM-NIVEAU-ORACLE4-1, déclencheur : commit de B-DEP-1. r1 vient d'un export `git archive f5b8269 s2-harness`,
jamais de F:/Shogen. (4b), C-1 du G2 : (i) recalcul de C.replication sans sim_niveau_calc et égalité exacte sur les
réplications de (4a) et sur FIXTURES ; (ii) --json : invariants de comptes par cas. Sortie ≠ 0 au premier écart
(« ECHEC (4a) », « ECHEC (4b i) », « ECHEC (4b ii) »), aucun fichier écrit.
Worker G1 claude-opus-5-5, 2026-09-30 ; (4b) : worker G1 de correction claude-opus-5-5, même jour.
Usage : python -B sim_niveau_oracle_r1.py --r1 EXPORT/s2-harness --sortie FICHIER.json [--replications 10] [--json F ...]"""
import argparse, hashlib, json, math, os, random, sys
from decimal import Decimal, localcontext
from fractions import Fraction

COMMIT = "f5b82693b8f1a99d6cc2fb53a5e3edd35b4e0a78"
R1_BLOB = "1d6a908cb2872ae261e09f1870bbaba5afca174c"             # git rev-parse f5b8269:s2-harness/shogen_s2/r1.py
NFLUX, ELL, N_MIN_BLOCS = 11, 240, 7200                            # (4b) : G0 §2, §4 et §5.4, jamais lus dans a1
VALEURS = ("REJETTE", "NE REJETTE PAS (z < 2,33)", "NE REJETTE PAS (discordance)", "NON ÉVALUABLE (garde §5.4)",
           "NON ÉVALUABLE (rejet non qualifiable)")                # libellés du journal G1 §3 g
CLES = ("R", "garde non tenue", "σ̂² = 0", "z_bloc non publiée", "z ≥ 2,33", "z_bloc ≥ 2,33", *VALEURS)
CHAMPS = ("e", "runs", "K", "phats", "P0", "P1", "P_more", "garde", "tenue", "z", "N", "z_bloc", "valeur", "ok2", "ok2b",
          "FIV", "R_centrage", "FIV_serie", "runs_I", "rmax")      # tous les champs de C.replication sauf « ligne »
FIXTURES = ((0.02, 60, 5000, range(20)), (0.003, 1, 10000, range(10)),  # (p, L, n, r) : n < 30ℓ ; garde non tenue ;
            (0.02, 1, 10000, (1056, 1292)), (0.02, 1, 25000, (358,)), (0.02, 60, 10000, (174,)))  # REJETTE (1056, 358),
# z < 2,33 ≤ z_bloc (1292), K = 0 (174) : branches absentes des 10 premières réplications (ajout du correcteur)


def octets(chemin):
    """Octets d'un fichier : blob git de r1.py, sha256 des scripts et des sim_niveau.json contrôlés."""
    with open(chemin, "rb") as f:
        return f.read()


def serie(p, L, n, r):
    """(4b) Réplication r du cas (L, n) régénérée depuis le texte du G0 §2 et §4, sans sim_niveau_calc : 11·n appels à
    random(), flux i = 1..11 puis t = 1..n ; D_1 = [U < p], D_t = [U < a] si D_(t−1) = 1, [U < b] sinon ; chaîne
    p={p!r} de C-5 (en attente de Q-G1-2, comme a1). Rend e, runs, I."""
    ch = f"SHOGEN-SIM-NIVEAU-1|20260930|p={p!r}|L={L}|n={n}|r={r}"
    rnd = random.Random(int.from_bytes(hashlib.sha256(ch.encode("ascii")).digest()[:8], "big")).random
    a, b = (p, p) if L == 1 else (1.0 - 1.0 / L, p / (L * (1.0 - p)))
    m, e, runs = [0] * n, [], []
    for _ in range(NFLUX):
        x = [rnd() < p]
        for _t in range(1, n):
            x.append(rnd() < (a if x[-1] else b))
        e.append(sum(x))
        runs.append(x[0] + sum(1 for t in range(1, n) if x[t] and not x[t - 1]))
        m = [u + v for u, v in zip(m, x)]
    return e, runs, [int(v >= 2) for v in m]


def numerateur(I, n, K):
    """(4b) N = ℓn²σ̂² par produits de lags directs en entiers : y_t = n·I_t − K, G_k = Σ_t y_t·y_(t+k) = n²γ̂_k,
    N = ℓ·G_0 + Σ_{k=1}^{ℓ−1} 2(ℓ − k)·G_k (G0 §5.3) ; ni masques de bits ni sommes de blocs (formes de a1). Rend (N, G_0)."""
    y = [n * i - K for i in I]
    G = [math.sumprod(y[:n - k], y[k:]) for k in range(ELL)]
    return ELL * G[0] + sum(2 * (ELL - k) * G[k] for k in range(1, ELL)), G[0]


def valeur(tenue, z, zb, s):
    """(4b) Valeur de la règle (§1 bis.1 pt 5 ; G0 §5.5) : les cinq cas du texte, dans l'ordre de VALEURS ; un seul tient."""
    haut = tenue and z >= s
    vrais = [v for v, c in zip(VALEURS, (haut and zb is not None and zb >= s, tenue and z < s,
                                         haut and zb is not None and zb < s, not tenue, haut and zb is None)) if c]
    if len(vrais) != 1:
        sys.exit(f"ECHEC (4b i) : cas de la règle non disjoints ou incomplets : {vrais!r}")
    return vrais[0]


def recalcul(r1, p, L, n, r):
    """(4b) (i) Enregistrement attendu de C.replication(p, L, n, r), champs CHAMPS : serie, numerateur, r1, valeur."""
    e, runs, I = serie(p, L, n, r)
    K = sum(I)
    N, G0 = numerateur(I, n, K)
    with localcontext() as ctx:
        ctx.prec = r1.DECIMAL_PREC
        phats = [+(Decimal(x) / Decimal(n)) for x in e]                         # r1.compute_r1 l.450-452
        p0, p1, pm = r1.poisson_binomial(phats)
        garde, tenue = r1.gate_value(n, pm), not r1.insufficient_history(n, pm)
        z = r1.z_score(n, K, pm) if tenue else None
        zb = (+((Decimal(K) - Decimal(n) * pm) / (Decimal(N) / Decimal(ELL * n * n)).sqrt())
              if N > 0 and n >= N_MIN_BLOCS else None)                          # G0 §5.3-5.4
    q, s2, nr, rmax, c = Fraction(garde), Fraction(N, ELL * n * n), 0, 0, 0
    for i in I:
        c = c + 1 if i else 0
        nr, rmax = nr + (c == 1), max(rmax, c)
    return dict(zip(CHAMPS, (e, runs, K, phats, p0, p1, pm, garde, tenue, z, N, zb, valeur(tenue, z, zb, r1.SEUIL_Z),
                             True, True, float(s2 / q) if q else None,
                             float(Fraction(K, n) * (1 - Fraction(K, n)) / (q / n)) if q else None,
                             float(s2 / Fraction(G0, n * n)) if G0 else None, nr, rmax)))


def verifier(r1, d, p, L, n, r):
    """(4b) (i) Compare l'enregistrement d de C.replication à recalcul (type, == et str) ; rend le nombre d'égalités."""
    for k, x in recalcul(r1, p, L, n, r).items():
        y = d.get(k, "<clé absente>")
        if not (type(x) is type(y) and x == y and str(x) == str(y)):
            sys.exit(f"ECHEC (4b i) : {k}, p={p!r} L={L} n={n} r={r} : attendu {str(x)[:70]}, script {str(y)[:70]}")
    return len(CHAMPS)


def invariants(chemin):
    """(4b) (ii) Invariants de comptes de chaque cas d'un sim_niveau.json (C-1 du G2) ; rend (nombre de cas, d'invariants)."""
    J, nb = json.loads(octets(chemin).decode("utf-8")), 0
    for c in J["cas"]:
        k, u, t = c["comptes"], c["taux"], f"{chemin} L={c['L']} n={c['n']}"
        if not set(CLES) <= set(k):
            sys.exit(f"ECHEC (4b ii) : clé absente, {t} : {sorted(set(CLES) - set(k))}")
        R, rej, disc, nq, npub = k["R"], k[VALEURS[0]], k[VALEURS[2]], k[VALEURS[4]], k["z_bloc non publiée"]
        regles = (("somme des cinq valeurs = R", sum(k[v] for v in VALEURS) == R),
                  ("z ≥ 2,33 = REJETTE + discordance + non qualifiable", k["z ≥ 2,33"] == rej + disc + nq),
                  ("REJETTE ≤ min(z ≥ 2,33 ; z_bloc ≥ 2,33)", rej <= min(k["z ≥ 2,33"], k["z_bloc ≥ 2,33"])),
                  ("REJETTE + discordance ≤ R − z_bloc non publiée", rej + disc <= R - npub),
                  ("non qualifiable ≤ z_bloc non publiée", nq <= npub),
                  ("z_bloc non publiée = σ̂² = 0 si n ≥ 30ℓ, = R sinon",
                   npub == (k["σ̂² = 0"] if c["n"] >= N_MIN_BLOCS else R)),
                  ("garde non tenue = NON ÉVALUABLE (garde §5.4)", k["garde non tenue"] == k[VALEURS[3]]),
                  ("x des taux z, z_bloc et règle = comptes",
                   (u["z"]["x"], u["z_bloc"]["x"], u["regle"]["x"]) == (k["z ≥ 2,33"], k["z_bloc ≥ 2,33"], rej)))
        for nom, ok in regles:
            if not ok:
                sys.exit(f"ECHEC (4b ii) : {nom}, {t}")
        nb += len(regles)
    return len(J["cas"]), nb


def main():
    """(4a) puis (4b) (i) sur les réplications 0..--replications−1 des 8 cas ; (4b) (i) sur FIXTURES ; (4b) (ii) sur chaque
    --json ; l'enregistrement n'est écrit (mode xb, jamais d'écrasement) que si tout passe."""
    ap = argparse.ArgumentParser(description="oracles (4a) et (4b) de SHOGEN-SIM-NIVEAU-1")
    ap.add_argument("--r1", required=True, help="dossier s2-harness exporté par git archive f5b8269")
    ap.add_argument("--sortie", required=True)
    ap.add_argument("--replications", type=int, default=10)
    ap.add_argument("--json", nargs="*", default=[], help="sim_niveau.json contrôlés par (4b) (ii)")
    a = ap.parse_args()
    if os.path.exists(a.sortie):
        sys.exit("refus : le fichier de sortie existe deja")
    sys.path.insert(0, os.path.abspath(a.r1))
    import sim_niveau as S, sim_niveau_calc as C
    from shogen_s2 import r1
    b = octets(r1.__file__)
    blob = hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()
    if blob != R1_BLOB:
        sys.exit(f"refus : r1.py importe ({r1.__file__}) n'est pas le blob de f5b8269 ({blob})")
    paires = [("DECIMAL_PREC", r1.DECIMAL_PREC, C.PREC), ("SEUIL_HIST", r1.SEUIL_HIST, C.SEUIL_HIST),
              ("SEUIL_Z", r1.SEUIL_Z, C.SEUIL_Z)]
    for nom, x, y in paires:
        if not (x == y and str(x) == str(y)):
            sys.exit(f"ECHEC (4a) : constante {nom} : r1 {x!r}, script {y!r}")
    cas, total4b = [], 0
    for L, n in S.CAS:
        k0, e4b = len(paires), 0
        for r in range(a.replications):
            d = C.replication(S.P_DEFAUT, L, n, r)
            with localcontext() as ctx:
                ctx.prec = r1.DECIMAL_PREC
                phats = [+(Decimal(x) / Decimal(n)) for x in d["e"]]
            p0, p1, pm = r1.poisson_binomial(phats)
            paires += [(f"p̂_{i + 1}", x, y) for i, (x, y) in enumerate(zip(phats, d["phats"]))]
            paires += [("P̂₀", p0, d["P0"]), ("P̂₁", p1, d["P1"]), ("P̂_more", pm, d["P_more"]),
                       ("garde", r1.gate_value(n, pm), d["garde"]),
                       ("garde tenue", not r1.insufficient_history(n, pm), d["tenue"])]
            if d["tenue"]:
                paires.append(("z", r1.z_score(n, d["K"], pm), d["z"]))
            for nom, x, y in paires[k0:]:
                if not (x == y and str(x) == str(y)):
                    sys.exit(f"ECHEC (4a) : {nom}, L={L} n={n} r={r} : r1 {x!r}, script {y!r}")
            e4b += verifier(r1, d, S.P_DEFAUT, L, n, r)
        cas.append({"L": L, "n": n, "replications": a.replications, "egalites": len(paires) - k0, "egalites_4b": e4b})
        total4b += e4b
    fixtures = []
    for p, L, n, rs in FIXTURES:
        e4b = sum(verifier(r1, C.replication(p, L, n, r), p, L, n, r) for r in rs)
        fixtures.append({"p": repr(p), "L": L, "n": n, "r": list(rs), "egalites_4b": e4b})
        total4b += e4b
    js = []
    for f in a.json:
        nc, ni = invariants(f)
        js.append({"json": f, "sha256": hashlib.sha256(octets(f)).hexdigest(), "cas": nc, "invariants": ni})
    rec = {"oracle": "(4a) et (4b) SHOGEN-SIM-NIVEAU-1 : r1 ; recalcul indépendant ; invariants", "commit_r1": COMMIT,
           "blob_r1": blob, "sha256_r1": hashlib.sha256(b).hexdigest(), "p": repr(S.P_DEFAUT),
           "script_sha256": {os.path.basename(m.__file__): hashlib.sha256(octets(m.__file__)).hexdigest()
                             for m in (S, C, sys.modules[__name__])},
           "comparaison": "Decimal : == et str() identiques ; booléen : == ; (4b) (i) : type, == et str() identiques",
           "constantes": 3, "egalites_total": len(paires), "cas": cas,
           "oracle_4b": {"champs": CHAMPS, "fixtures": fixtures, "egalites_total": total4b, "json": js},
           "oracle_4": ("absente à f5b8269 : r1.block_long_run_variance ; oracle (4) non exécutable, item "
                        "SHOGEN-SIM-NIVEAU-ORACLE4-1, déclencheur : commit de B-DEP-1")
           if not hasattr(r1, "block_long_run_variance") else "présente : appel à coder (item ORACLE4-1)"}
    with open(a.sortie, "xb") as f:
        f.write((json.dumps(rec, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))


if __name__ == "__main__":
    main()
