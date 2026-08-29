# FuelAnomalies — Research & Paper Plan

_Draft v0.4 — 2026-08-29 — two-arm, signature-based attribution_

## v0.4 unifying thesis (current direction)
**Excess fuel consumption is separable by CAUSE via its signature**: driver-caused excess is
TRANSIENT/KINEMATIC (accel, jerk, harsh events, at normal AFR); malfunction-caused excess (rich
mixture) is STEADY-STATE and AFR/EMISSIONS-linked. We demonstrate this on the two public datasets that
each carry one ground truth: **VED** (real fleet, driver behaviour + vehicle-baseline decomposition)
and **EngineFaultDB** (controlled bench, labelled engine faults + fuel). This directly addresses the
original goal — attribute excess fuel to driver vs vehicle malfunction — while being honest that no
single dataset carries both grounds (the documented field-wide gap).

Evidence in hand: Arm 1 (VED) fuel model R²=0.673, behaviour ~8% marginal / vehicle-baseline ~14%
variance, behaviour counterfactual ~0.5 L/100km monotonic in aggression. Arm 2 (EngineFaultDB) rich
fault = +6.2% excess fuel at matched operating point, emissions-linked signature (corr with CO/HC/AFR),
lean/ignition not excess-fuel faults. See RESULTS.md.

Honest scoping: Arm 2's fuel-relevant malfunction is the RICH-MIXTURE fault specifically; it is a
controlled bench (no driver context). The 2-vs-3 (lean vs ignition) label mapping is unverified.

---
_(v0.3 detail below — being folded into v0.4)_
_Draft v0.3 — 2026-08-29 — pivot after go/no-go: driver-behaviour vs vehicle-baseline decomposition_

## What changed from v0.2 (read first)
The primary go/no-go **failed**: on VED, per-vehicle fuel residual does NOT track fuel-trim drift
(between- and within-vehicle r≈0, placebo-calibrated). Root cause: VED is a healthy consumer fleet
(trims small, median +1.5%), fuel trim measures AFR correction not efficiency, and per-vehicle
residual is confounded by engine-size heterogeneity — with no fault/odometer/age ground truth.
See `diagnostics/gonogo_health_validation.md`. **Decision: reframe the "vehicle" component from
"malfunction/health" to "vehicle-baseline heterogeneity" (make/model/size/condition, bundled), all on
real data.** A background search (option 4) continues hunting for a real fault+fuel dataset to
optionally re-add a malfunction arm later.

## 1. One-sentence thesis
We detect excess-fuel trips from public OBD + GPS trajectory data and **decompose** each trip's excess
into a **driver-behaviour** contribution and a **vehicle-baseline** contribution, validating the
behaviour side against an independent behaviour-labelled dataset (UAH-DriveSet) and characterizing the
vehicle side against static vehicle parameters — a fully real-data, identifiable decomposition.

## 2. Research questions
- **RQ1 (model).** How well do trajectory-derived driving features + conditions predict trip fuel?
  (Have: MAPE 13.3%, R² 0.673, driver+condition features only, GroupKFold by vehicle.)
- **RQ2 (decomposition).** Can we split a trip's excess fuel into behaviour vs vehicle-baseline vs
  residual, as an interpretable variance decomposition and a per-trip attribution?
- **RQ3 (behaviour validation).** Does the behaviour component agree with independent aggressive-driving
  labels (UAH-DriveSet) and with within-VED harsh-driving measures?
- **RQ4 (vehicle characterization).** How much of the vehicle-baseline component is explained by static
  params (displacement, class, weight) vs unexplained persistent per-vehicle effect?
- **RQ5 (baseline gap).** Do detection-only / feature-relevance methods fail to produce this validated
  behaviour-vs-vehicle split?

## 3. Identifiability (honest scope)
VED has ~one driver per vehicle, so per-trip driver-vs-vehicle causation is not identifiable at the
unit level. We therefore claim a **model-based decomposition of expected excess**, where:
- behaviour component = counterfactual fuel change from this trip's driving vs an efficient reference,
- vehicle-baseline component = persistent per-vehicle effect after driving+conditions are removed,
- validated by convergent external evidence (behaviour ↔ UAH labels; vehicle ↔ static params).
We do NOT claim malfunction detection on VED. Malfunction is deferred to a possible synthetic arm or a
real fault+fuel dataset if the background hunt finds one.

## 4. Method
### 4.1 Fuel model + detector (RQ1) — DONE (baseline)
- Target: MAF-derived fuel per 100 km, ICE only. Features: speed dist, +accel, jerk, harsh events,
  idle, stops/km, %hwy, VSP(grade=0), OAT, AC/heater, weight, dist, dur. HistGBM, GroupKFold by vehicle.
- Excess-fuel event = significant positive OOF residual vs population expectation.

### 4.2 Decomposition (RQ2)
- **Behaviour component** = M(actual driving feats) − M(efficient-reference feats), reference =
  low-aggression percentile driving for matched conditions.
- **Vehicle-baseline component** = per-vehicle fixed effect (mean OOF residual), optionally split into
  static-explained (displacement/class/weight) + persistent unexplained.
- **Variance decomposition**: fraction of total fuel variance attributable to driving+conditions vs
  vehicle fixed effect vs residual.
- Per-trip interpretable output: "trip excess = X% behaviour + Y% vehicle-baseline".

### 4.3 Behaviour validation (RQ3)
- Within-VED: behaviour component rises monotonically with independent harsh-driving deciles.
- Cross-dataset: apply the behaviour-feature model to UAH-DriveSet; show it separates
  labelled aggressive/normal/drowsy driving.

### 4.4 Vehicle characterization (RQ4)
- Regress vehicle fixed effect on static params; report R² and the residual persistent component.

## 5. Baselines
1. RF/GBM fuel model + residual thresholding (detection only). [Abediasl 2024]
2. Unsupervised anomaly + SHAP feature-relevance (features, not components). [Barbado 2022]
3. Pooled model (no vehicle effect) ablation; no-behaviour-counterfactual ablation.

## 6. Metrics
- Fuel model: MAPE, nMAE, RMSE, R².
- Decomposition: variance-explained shares; stability across seeds/folds.
- Behaviour validation: monotonicity vs harsh deciles; UAH aggressive/normal AUC/separation.
- Vehicle characterization: static-param R² of the vehicle effect.

## 7. Contributions
1. A real-data, identifiable **driver-behaviour vs vehicle-baseline decomposition** of trip fuel.
2. **Convergent behaviour validation** (UAH cross-dataset + within-VED harsh-driving monotonicity).
3. Quantified **variance decomposition** of fuel into driving vs vehicle vs residual on a 197-vehicle,
   14.5k-trip public fleet.
4. Honest characterization of the identifiability limit + the field-wide fault+fuel data gap
   (evidenced by our negative trim result).

## 8. Datasets
- Primary: VED, 264 ICE (197 usable after QC), MAF-derived fuel, GPS behaviour features. Apache-2.0.
- Behaviour validation: UAH-DriveSet (aggressive/normal/drowsy labels).
- Optional generalization: Barreto obdii-ds3.
- (Pending) a real fault+fuel dataset from the background hunt → optional malfunction arm.

## 9. Target venues
IEEE T-ITS; Transportation Research Part C/D; Applied Energy. Faster: Sensors, IEEE Access.

## 10. Phase status
- P0 data audit — DONE (DATA_READINESS.md).
- P1 feature pipeline — DONE (data/processed/trip_features.parquet, 14,460 trips / 197 ICE veh).
- P2 fuel model + detector — DONE (R² 0.673). Go/no-go for health validation — DONE (negative).
- **P3 decomposition + variance sizing — NEXT.**
- P4 behaviour validation (within-VED monotonicity, then UAH cross-dataset).
- P5 vehicle characterization + baselines + ablations.
- P6 writing (paper-build, technical-diagram-designer, bibtest).

## 11. Risks & mitigations
- **"Vehicle-baseline" is heterogeneity, not malfunction** — less novel. Mitigate: strong behaviour
  validation + variance decomposition are the core; add malfunction arm only if a real dataset appears.
- **UAH domain shift** (smartphone vs OBD features). Mitigate: validate at feature level, report shift.
- **1 Hz smoothing** of harsh events. Mitigate: sampling ablation using 10 Hz-dense segments.
- **Unverified seminal refs** (VSP 1999, VT-Micro). Verify via bibtest.

## 12. Immediate next step
P3: extract vehicle fixed effects, compute the behaviour/vehicle/residual variance decomposition, and
show the behaviour component tracks harsh-driving deciles within VED.
