# FuelAnomalies

**Attributing excess fuel consumption to driver behaviour versus vehicle malfunction: a
signature-based approach on public telemetry.**

Excess fuel has two causes with the same symptom: an aggressive driver and a malfunctioning vehicle
both burn more than they should. This project shows the two causes leave **separable signatures** and
builds a cross-dataset attribution framework on public data only.

Paper skeleton (GitHub Pages): **https://apartsinprojects.github.io/FuelAnomalies/**

## Headline results
- Expected-fuel model on VED (197 ICE cars, 14,460 trips): **R² = 0.673**.
- Variance decomposition: behaviour ~8% (marginal), vehicle-baseline ~14%, environment ~59%.
- Behaviour axis externally validated (Zenodo Driving Events): driver-held-out **AUC = 0.958**
  (permutation p = 0.032).
- Malfunction arm (EngineFaultDB): rich-mixture fault = **+6.2% excess fuel**, emissions-linked.
- **Double dissociation**: the combustion axis explains **90%** of fault-caused excess and **0%** of
  driver-caused excess.

## Structure
| Path | What |
|---|---|
| `index.html` | Paper skeleton (served via GitHub Pages) |
| `PLAN.md` | Research and paper plan (phase-by-phase) |
| `RESULTS.md` | Full results log, every number traced to a script |
| `DATA_READINESS.md` | P0 data audit |
| `scripts/p1..p6_*.py` | Feature pipeline, fuel model, decomposition, validation, attribution |
| `diagnostics/` | Negative results and sanity checks (kept out of the paper claims) |

## Data (not redistributed)
Obtain from original sources:
- **VED** (Apache-2.0): https://github.com/gsoh/VED
- **EngineFaultDB** (GPL-3.0): https://github.com/leoxthomas/EngineFaultDB
- **Driving Events** (CC-BY-4.0): https://zenodo.org/records/6570972

## Reproduce
Python 3.14, `pandas`, `scikit-learn`, `pyarrow`, `scipy`, `openpyxl`. Place datasets under
`data/raw/`, then run `scripts/p1_features.py` → `p6_attribution.py` in order.
