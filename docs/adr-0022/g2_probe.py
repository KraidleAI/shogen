"""G2 adversarial probe — imports the REAL F:\\Shogen code, feeds adversarial inputs,
verifies fail-closed guards fire and the semantic change holds. NO write to F:\\Shogen.
Run: python g2_probe.py  (from anywhere; sys.path points at the harness)."""
import sys, os, json, tempfile
from decimal import Decimal

sys.path.insert(0, r"F:\Shogen\s2-harness")

from shogen_s2 import records, run_campaign, r1, sources  # real modules

PASS, FAIL = [], []
def check(name, cond):
    (PASS if cond else FAIL).append(name)

# ---- 1. effective_run_params: scalar tau_classe LEVE ; mapping PASSE -----------
def _base(tau_classe):
    return {
        "pool": ["coinbase"], "w": 60,
        "sigma_classe": {"place_horodatee": "30"},
        "sigma_class_of_flux": {"coinbase": "place_horodatee"},
        "tau_classe": tau_classe,
        "decimal_prec": 50, "seuil_historique_valeur": "10",
        "n_min_hors_enveloppe": 4,
        "strate_calendar": {"kind": "single"},
    }
try:
    records.effective_run_params([_base("0.005")])   # SCALAIRE legacy (str)
    check("effrp scalar tau raises", False)
except ValueError as e:
    check("effrp scalar tau raises (SCALAIRE legacy)", "SCALAIRE legacy" in str(e))
# mapping passes
try:
    out = records.effective_run_params([_base({"place_horodatee": "0.0045"})])
    check("effrp mapping tau passes", out["tau_classe"] == {"place_horodatee": "0.0045"})
except Exception as e:
    check("effrp mapping tau passes", False); print("  unexpected:", e)

# Prove the guard is LOAD-BEARING: without it, sigma_tau_from_params would blow up
# on a scalar (str has no .items()) => AttributeError, NOT the clean fail-close.
try:
    records.sigma_tau_from_params(_base("0.005"))
    check("sigma_tau_from_params on scalar would raise (guard is load-bearing)", False)
except AttributeError:
    check("sigma_tau_from_params on scalar -> AttributeError (guard load-bearing)", True)
except Exception as e:
    check("sigma_tau_from_params on scalar -> some error", True); print("  got:", type(e).__name__)

# ---- 2. _load_committed_sigma_tau: scalar / out-of-range / incomplete ----------
def _write(obj):
    d = tempfile.mkdtemp(prefix="g2probe_")
    p = os.path.join(d, "st.json")
    with open(p, "w", encoding="utf-8") as f: json.dump(obj, f)
    return p

# scalar tau -> raise
try:
    run_campaign._load_committed_sigma_tau(_write(
        {"sigma_classe": {"place_horodatee": "30"}, "tau_classe": "0.005"}))
    check("loader scalar tau raises", False)
except run_campaign.SigmaTauNonRepresentable as e:
    check("loader scalar tau raises (jamais un scalaire)", "mapping" in str(e))
# out-of-range tau (>=1) -> raise
try:
    run_campaign._load_committed_sigma_tau(_write(
        {"sigma_classe": {"place_horodatee": "30"}, "tau_classe": {"place_horodatee": "50"}}))
    check("loader tau>=1 raises", False)
except run_campaign.SigmaTauNonRepresentable as e:
    check("loader tau out-of-(0,1) raises", "hors de (0, 1)" in str(e))
# incomplete: a sigma class with NO tau -> raise (completeness)
try:
    run_campaign._load_committed_sigma_tau(_write(
        {"sigma_classe": {"place_horodatee": "30", "sans_horodatage": None},
         "tau_classe": {"place_horodatee": "0.0045"}}))   # sans_horodatage lacks tau
    check("loader incomplete tau raises", False)
except run_campaign.SigmaTauNonRepresentable as e:
    check("loader incomplete tau raises (classes sans tau)", "sans" in str(e).lower())
# null tau -> raise (revision pending)
try:
    run_campaign._load_committed_sigma_tau(_write(
        {"sigma_classe": {"place_horodatee": "30"}, "tau_classe": None}))
    check("loader null tau raises", False)
except run_campaign.SigmaTauNonRepresentable as e:
    check("loader null tau raises (revision EN ATTENTE)", "ATTENTE" in str(e))
# valid assembled file: sigma None class + tau present -> hors-env stays evaluable
try:
    sbc, tau, lbl = run_campaign._load_committed_sigma_tau(_write(
        {"sigma_classe": {"place_horodatee": "390", "sans_horodatage": None},
         "tau_classe": {"place_horodatee": "0.0045", "sans_horodatage": "0.0045"}}))
    check("loader valid: sans_horodatage sigma=None but tau present",
          sbc["sans_horodatage"] is None and tau["sans_horodatage"] == Decimal("0.0045"))
except Exception as e:
    check("loader valid assembled file", False); print("  unexpected:", e)

# ---- 3. _tau_for_flux mirror + classify_ecart semantic change ------------------
# unknown flux -> None (no class)
check("_tau_for_flux unknown flux -> None",
      r1._tau_for_flux("z", {"c": Decimal("0.005")}, {}) is None)
# flux whose class carries no tau -> None
check("_tau_for_flux class-without-tau -> None",
      r1._tau_for_flux("f", {"other": Decimal("0.005")}, {"f": "c"}) is None)
# present -> the class tau
check("_tau_for_flux present -> class tau",
      r1._tau_for_flux("f", {"c": Decimal("0.0045")}, {"f": "c"}) == Decimal("0.0045"))

# classify_ecart: unknown flux (no class) with responders -> NON_EVAL_HORSENV
# (was PAS_ECART under scalar tau — the ADR-0022 semantic change).
reading = {"status": "ok", "price": "100", "source_ts": 0}
got = r1.classify_ecart(reading, [Decimal(100)]*4, 5, 10**9, "z",
                        {"place_horodatee": Decimal(30)}, {},   # scof empty -> no class
                        {"c": Decimal("0.005")})
check("classify unknown flux -> NON_EVAL_HORSENV (semantic change, fail-closed)",
      got is r1.Ecart.NON_EVAL_HORSENV)

# classify_ecart: known flux, class HAS tau, price within -> PAS_ECART (unchanged path)
got2 = r1.classify_ecart(reading, [Decimal(100)]*4, 5, 10**9, "f",
                         {"c": Decimal("1e12")}, {"f": "c"}, {"c": Decimal("0.005")})
check("classify known flux within tau -> PAS_ECART", got2 is r1.Ecart.PAS_ECART)
# classify_ecart: known flux, price outside tau -> HORS_ENVELOPPE
got3 = r1.classify_ecart({"status": "ok", "price": "200", "source_ts": 0},
                         [Decimal(100)]*4, 5, 10**9, "f",
                         {"c": Decimal("1e12")}, {"f": "c"}, {"c": Decimal("0.005")})
check("classify known flux outside tau -> HORS_ENVELOPPE", got3 is r1.Ecart.HORS_ENVELOPPE)

# ---- 4. mirror shape: _tau_for_flux vs _sigma_floor_for_flux -------------------
import inspect
ts = inspect.getsource(r1._tau_for_flux)
ss = inspect.getsource(r1._sigma_floor_for_flux)
# both: get class, None-guard, .get(klass)
check("_tau_for_flux mirrors _sigma_floor structure",
      "sigma_class_of_flux.get(flux_id)" in ts and "if klass is None:" in ts
      and "return tau_by_class.get(klass)" in ts
      and "sigma_class_of_flux.get(flux_id)" in ss and "return sigma_by_class.get(klass)" in ss)

# ---- 5. Concordance §E : mapping tau, key-order independent ; divergence LEVE ---
# (a) same tau mapping, DIFFERENT key order across two starts -> effrp passes
b1 = _base({"place_horodatee": "0.0045", "agregateur": "0.026"})
b2 = _base({"agregateur": "0.026", "place_horodatee": "0.0045"})   # reordered
try:
    records.effective_run_params([b1, b2])
    check("effrp §E: same tau mapping, different key order -> concordant (passes)", True)
except Exception as e:
    check("effrp §E key-order concordance", False); print("  unexpected:", e)
# (b) tau differing in ONE class across starts -> raises 'divergents'
b3 = _base({"place_horodatee": "0.0045", "agregateur": "0.026"})
b4 = _base({"place_horodatee": "0.0045", "agregateur": "0.030"})   # one class differs
try:
    records.effective_run_params([b3, b4])
    check("effrp §E: divergent tau raises", False)
except ValueError as e:
    check("effrp §E: divergent tau across starts -> raises 'divergents'", "divergents" in str(e))

print("\n=== G2 PROBE RESULTS ===")
for n in PASS: print("PASS:", n)
for n in FAIL: print("FAIL:", n)
print(f"\n{len(PASS)} pass / {len(FAIL)} fail")
sys.exit(1 if FAIL else 0)
