# Diagnostics: primary go/no-go (health-side validation) — NEGATIVE

_2026-08-29. Scripts: scripts/p2_gonogo.py, scripts/p2_diagnostics.py._

## Question
Does a vehicle's fuel residual (fuel per 100km after controlling for driver-controllable +
condition features, GroupKFold by vehicle) track its fuel-trim drift |LTFT|? This was the plan's
PRIMARY external validator for the "vehicle-health" component.

## Result: NO (evidence-backed, calibrated with placebos)
- Fuel model: MAPE 13.3%, R2 0.673 (driver+conditions only, no vehicle ID). Solid baseline.
- Between-vehicle: resid_mean vs |LTFT| Pearson r=-0.075 (p=0.37); placebo shuffled r=-0.038. NULL.
- D1: resid_mean vs engine displacement r=+0.27 (p<1e-3) — vehicle residual is partly engine-size
  heterogeneity (thirsty big engine), not health. Residual sd=1.25 L/100km (real, but heterogeneous).
- D2: total fuel trim (STFT+LTFT) median +1.5%, p90 +11%. VED = healthy consumer fleet; trims small.
  MAF-stoich target is trim-blind by construction but the ignored fraction is only ~1.5% median.
- D3: within-vehicle demeaned resid vs trim: r=-0.078 (huge n so p<1e-16, but negligible effect,
  wrong sign); placebo r=-0.016. Trim and efficiency are decoupled even over time within a car.

## Root cause (not a bug)
1. VED is a fleet of HEALTHY personal cars: little real fuel-system malfunction exists to detect.
2. Fuel trim measures AFR correction, NOT fuel efficiency — physically distinct quantities.
3. Per-vehicle fuel residual is confounded by engine size/class heterogeneity; VED has no odometer,
   age, maintenance, or DTC/fault ground truth to isolate "health."

## Implication
The "validate vehicle-health component against fuel trims on real VED" plan is NOT viable. This is the
documented field-wide gap (no public dataset couples fuel flow with verified mechanical fault labels).
The BEHAVIOUR side remains strong (R2 0.673 from driving features; residual is real; UAH-DriveSet can
validate behaviour). Decision needed: narrow to a behaviour-validated paper, or add synthetic fault
injection as the only route to malfunction ground truth (+ release benchmark).
