"""PRÉ-VOL : assemble le sigma-tau.json campagne EXACT (σ = clôture cloture-finale.json ;
τ PAR CLASSE = ADR-0022) et vérifie qu'il CHARGE via le nouveau loader (resolve_sigma_tau).
Read-only sur les dépôts ; écrit un fichier de pré-vol en scratchpad. Ne lance rien."""
import json, sys
sys.path.insert(0, r"F:\Shogen\s2-harness")
from shogen_s2 import run_campaign

clo = json.load(open(r"F:\shogen-campagne\cloture-finale.json", encoding="utf-8"))
sigma = clo["sigma_classe"]                          # {classe: str|None} issu de la clôture
tau_adr = {"oracle_pyth": "0.0015", "place_horodatee": "0.0045",
           "sans_horodatage": "0.0045", "oracle_chainlink": "0.0165",
           "agregateur": "0.026"}                    # ADR-0022 (par classe)
assembled = {"sigma_classe": sigma, "tau_classe": tau_adr,
             "_provenance": "ADR-0022 : σ = clôture calibration ; τ PAR CLASSE = ADR-0022"}
out = r"C:\Users\KACIMI\AppData\Local\Temp\claude\F--Shogen\90684fb2-4e7b-42e9-b820-f042dc4465f3\scratchpad\tau-facts\sigma-tau-preflight.json"
json.dump(assembled, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

sbc, tau, label = run_campaign.resolve_sigma_tau("campagne", out)
print("LOAD OK — le loader accepte le sigma-tau.json assemblé.")
print("sigma :", {k: (str(v) if v is not None else None) for k, v in sbc.items()})
print("tau   :", {k: str(v) for k, v in tau.items()})
print("label :", label)
