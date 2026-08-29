# Diagnostics: EngineFaultDB malfunction arm — audit + caution

_2026-08-29. Script: scripts/p5_faultarm.py. Data: data/raw/EngineFaultDB_Final.csv (56k rows)._

## Setup
Operating-point fuel model (RPM, MAP, TPS, Force, Power, Speed → Consumption L/100KM), 5-fold OOF,
no fault label. R2=0.883. Then compare residual (excess fuel at matched operating point) by fault.

## Findings (interpret with caution — see caveat)
- Excess-fuel residual by fault: fault0 +0.37, fault1 +0.13, fault2 -0.22, fault3 -0.00 (L/100km).
  ANOVA F=840 (p~0) but effect sizes SMALL and NOT "fault→more fuel". Fault 0 has the HIGHEST residual.
- Raw fuel L/100km: f0=9.25, f1=9.88, f2=8.32, f3=8.51.
- Combustion signatures reveal fault semantics (labels are NOT ordinal severity):
  - **Fault 1 = rich/incomplete combustion**: lambda 0.93 (richest), AFR 13.68, CO 3.17% (highest),
    HC 260ppm (highest), fuel 9.88 (highest). Genuine malfunction→excess-fuel.
  - Faults 2,3 = leaner/cleaner (lambda ~0.98, CO ~1.3), LOWER fuel than fault 0.
  - **Fault 0 is NOT a pristine baseline**: lambda 0.957, CO 2.16% (moderately rich).
- Operating points differ across faults (f2/f3 sampled at higher mean RPM/Power/Speed), muddying the
  matched-residual comparison though ranges overlap.
- Fault classification: macro-F1 0.405 (all signals), 0.335 (fuel only). Faults 2&3 heavily confused.

## Caveat / blocker
README does NOT define what fault 0/1/2/3 physically are. Cannot frame the malfunction arm until the
paper's fault taxonomy is known (agent fetching it). My initial assumption "0=healthy, higher=worse"
was WRONG (root cause of the counterintuitive residual result).

## Provisional read
There IS a real signal — the rich-combustion fault burns measurably more fuel with worse emissions —
but this is one condition, not a clean severity gradient, and fault 0 is not a healthy reference. The
arm is viable but weaker/subtler than hoped; its exact framing depends on the fault definitions.
