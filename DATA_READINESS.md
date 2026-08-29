# P0 — VED Data Readiness Report

_2026-08-29. Based on VED Dynamic Part 1 (22 weekly CSVs; 3 weeks deep-sampled) + static files._

## Verdict: **GO** — with three target/preprocessing adjustments locked below.

## What VED actually is
- 383 personal cars, Ann Arbor MI, Nov 2017–Nov 2018, ~374k mi. Two 7z dynamic archives (~176 MB)
  + static Excel. Apache-2.0. Paper: Oh, LeBlanc, Peng, IEEE T-ITS 2020 (arXiv:1905.02081).
- Static split confirmed: **264 ICE, 93 HEV, 27 PHEV/EV** (`Vehicle Type` col).
- Records keyed by `(VehId, Trip)`; GPS + OBD time series per trip.
- Trip inventory (sample): median **498 points/trip**, median **6.9 min**, p90 17.6 min. Plenty of trips
  (2,230 unique trips across just 3 weeks of Part 1).

## Signal coverage (3-week sample, fraction non-null)
| Signal | Coverage | Role |
|---|---|---|
| Vehicle Speed | 99.9% | behaviour + model |
| Engine RPM | 98.7% | model |
| **MAF[g/sec]** | **82.8%** (ICE 78.8%, HEV 98.7%) | **fuel target source** |
| Absolute Load | 75.0% | model |
| **LTFT Bank 1** | **57.4%** (260/326 vehicles; median 63.6% of a vehicle's rows) | **health signal (RQ3)** |
| STFT Bank 1 | 60.9% | health signal |
| Fuel Trim Bank 2 | 14–18% | mostly single-bank engines — **use Bank 1 only** |
| `Fuel Rate[L/hr]` | **~0–3%** | **UNUSABLE — do not use as target** |

## Three locked decisions
1. **Target = MAF-derived fuel, ICE only.** `Fuel Rate[L/hr]` PID is essentially empty and never
   co-occurs with MAF (0 overlapping rows). Derive fuel from MAF: `L/hr = MAF[g/s] / 14.7 (AFR) /
   745 (g/L) * 3600`. Yields sane values (median 1.87, p99 16.2 L/hr). This is the standard VED
   approach. **Restrict the core fuel model to the 264 ICE vehicles** (HEV fuel is confounded by the
   electric path; treat HEV as a possible robustness extension, EV excluded).
2. **Health signal = LTFT/STFT Bank 1.** Solid coverage: 245/326 vehicles have ≥20% LTFT rows. This is
   the load-bearing signal for the primary go/no-go (vehicle component vs trim drift). Bank 2 too sparse.
3. **Resample irregular timestamps.** Within-trip dt is irregular: median 700 ms, mode 100 ms (10 Hz),
   p10 100 / p90 1600 ms. Resample each trip to a fixed **1 Hz** grid in P1 before deriving accel/jerk;
   run the planned sampling-rate ablation using the 10 Hz-dense segments.

## Implications for the plan
- Core dataset for the paper: **264 ICE vehicles**, MAF-derived fuel target, LTFT/STFT-Bank-1 health.
- The primary go/no-go (vehicle-health component ↔ fuel-trim drift) is **feasible**: both the fuel
  target (MAF) and the trim signal are present on the same ICE vehicles with good coverage.
- Only Part 1 downloaded so far (22 weeks). Part 2 (~94 MB) pending for the full year.

## Next
P1 feature pipeline: per-trip 1 Hz resample → driving features (speed dist, +accel, jerk, harsh
events, idle frac, stops/km, grade) + fuel target (MAF-derived) + per-vehicle trim aggregates.
