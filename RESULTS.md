# Results log

## P2 — Fuel model (RQ1)
MAF-derived fuel per 100 km, ICE only, driver+condition features, HistGBM, GroupKFold by vehicle.
**MAPE 13.3%, R² 0.673.** No vehicle-ID leakage.

## P3 — Variance decomposition (RQ2) — 14,170 trips, 194 vehicles
| Component | Share of total fuel variance |
|---|---|
| R² full (behaviour + environment, no vehicle ID) | 0.673 |
| environment-only (route/temp/aux/weight) | 0.592 |
| behaviour-only | 0.366 |
| **behaviour marginal** (unique over environment) | **0.081** |
| environment marginal (unique over behaviour) | 0.307 |
| **vehicle-baseline** (per-vehicle fixed effect) | **0.142** |
| unexplained (noise) | 0.185 |

Reading: environment/route dominates; **behaviour uniquely adds ~8%** (up to ~37% counting shared
variance with route); **vehicle-baseline is a real ~14%** persistent per-vehicle effect; ~18% noise.

### RQ4 — what is the vehicle-baseline?
Vehicle fixed effect regressed on static params: **FE ~ displacement + weight, R² = 0.231**.
=> only ~23% of the vehicle-baseline is engine size/weight; **~77% is a persistent, size-independent
per-vehicle effect** (tuning/condition/individual-vehicle differences — unlabelled in VED).

### Behaviour counterfactual (fuel above a gentle-driving reference)
Median **0.47 L/100km** above gentle driving (≈5% of median fuel), p90 1.59. **Monotonic across
aggression deciles**: [0.34, 0.42, 0.39, 0.41, 0.49, 0.58, 0.65, 0.78, 0.99, 1.55] — sanity check
passes (external UAH validation still pending, P4). Consistent with eco-driving literature (~5–15%).

## Fault+fuel dataset hunt (option 4) — outcome
Field-wide gap largely confirmed, BUT one real complement found:
- **EngineFaultDB** (GitHub leoxthomas/EngineFaultDB, GPL-3.0, IEEE Access 2023): 55,999 rows, 14 vars
  (MAP, TPS, RPM, speed, CO/HC/CO2/O2, lambda, AFR) + **fuel consumption (L/h, L/100km)** + **fault
  labels (0=none,1,2,3)**. Spark-ignition **test bench**; no driver/telematics. => a REAL fuel+fault
  set for a malfunction-detection arm, complementary to VED's driver-behaviour arm.
- EngineAD: real truck fleet with fuel-rate + fault labels but released PCA-reduced (raw fuel not
  recoverable), access-gated. Pursue authors only if a real-fleet arm is wanted.
- DEFault (diesel), SCANIA Component X, C-MAPSS: no usable fuel-consumption channel.

## P5 — Malfunction arm (EngineFaultDB), CLEAN (after fault definitions)
Fault labels (IEEE Access paper): 0=normal, 1=rich mixture, 2=lean mixture(inferred),
3=low-voltage/ignition(inferred; 2vs3 mapping from listing order, Table 4 is an image = uncertain).

Test: fuel model trained on NORMAL operating points (RPM,MAP,TPS,Force,Power,Speed), score faults.
- normal OOF residual: mean ~0, sd 0.202 (normal well-modelled).
- **Rich fault (1): +0.498 L/100km excess at matched operating point (+6.2% of median fuel);
  AFR 13.68 vs 14.07 (=> +7.5% fuel/air vs stoich); BSFC +10.6% vs normal.** The canonical over-fuel fault.
- Lean (2): ~0 excess (-0.06). Ignition (3): +0.15 (small). Lean/ignition are NOT excess-fuel faults.
- **Signature separability**: rich excess correlates with CO (+0.32), AFR (-0.32), HC (+0.27) =>
  fault-caused excess fuel is EMISSIONS/AFR-linked (steady-state), distinct from driver-caused excess
  which is KINEMATIC (accel/jerk/harsh). This is the unifying attribution principle.

Reconciled paper's "rich consumes less fuel/hour": true per-hour (rich ran at lower power points) but
HIGHER per-distance and per-work (BSFC) — matched-operating-point analysis isolates the real penalty.

## P6 — Signature-based attribution: DOUBLE DISSOCIATION (headline)
Excess defined net of context (VED: route/temp/weight; bench: operating point). Two axes:
KINEMATIC (transient aggression) and COMBUSTION (VED fuel trims; bench AFR/lambda/CO/HC).

| axis | DRIVER-excess (VED) R2 | FAULT-excess (bench, rich) R2 |
|---|---|---|
| kinematic  | +0.107 | n/a (steady-state bench) |
| combustion | -0.039 | +0.903 |

corr(excess, combustion% vs stoich): VED -0.106 (silent); bench rich +0.333.
=> Combustion axis explains ~90% of fault-excess, ~0% of driver-excess. Kinematic axis explains
driver-excess. The two causes are separable by SIGNATURE. Reproduces the go/no-go null (trims don't
explain VED excess) as an independent consistency check.

HONESTY CAVEATS: (1) On the bench, AFR and fuel are physically coupled (rich AFR = more fuel almost
by definition), so combustion R2=0.90 for fault-excess is physically expected, NOT a surprising ML
result; the non-trivial finding is the DISSOCIATION (same axis silent for driver-excess). (2) Driver
and fault ground truths are in different datasets, so this is a double dissociation across datasets,
not a single-trip competing-cause classifier. (3) Bench lacks a kinematic axis (steady-state), which
is itself consistent with fault-excess being non-transient.

## P4 — Behaviour-axis external validation (Zenodo 6570972, Driving Events)
UAH-DriveSet servers down; pivoted to open CC-BY-4.0 Zenodo dataset (3 drivers, 400 Hz linear accel,
169 labeled events: 143 aggressive / 26 non-aggressive). Kinematic features (accel magnitude stats,
harsh-event rate, energy) per event window; aggressive vs non-aggressive, DRIVER HELD OUT (LOGO CV).
- Univariate AUC: mag_std 0.672, mag_p95 0.657, energy 0.646, harsh_per_s 0.639 (all MWU p<0.05).
  jerk_rms at raw 400 Hz does NOT separate (AUC 0.48) — noise-dominated; amplitude features carry it.
- **Logistic regression, leave-one-driver-out: AUC = 0.958** (per-driver 0.984/0.934/0.992). RF 0.783
  (RF overfits the 2 training drivers; linear model generalizes better with only 3 drivers).
- **Permutation test: real 0.958 vs permuted mean 0.482 (max 0.648), p=0.032** => signal is real,
  not leakage. The kinematic/behaviour axis separates aggressive driving cross-dataset. Arm 1 external
  validation COMPLETE.

## P7 — Baselines (RQ5)
Framing: NO cause-labelled trip benchmark exists (identifiability limit), so this is a CAPABILITY
contrast, not a metric horse-race. Baseline components compared against are model outputs, not truth.
- IsolationForest (detection-only): corr(score, excess)=+0.16 (weak detector), corr(score, behaviour
  comp)=+0.22, corr(score, |vehicle comp|)=-0.01 => yields ONE anomaly score, does not recover the
  vehicle cause, no per-trip decomposition.
- Feature relevance (permutation importance, Barbado-style surrogate): top features speed_mean (0.95),
  weight_lb (0.69), vsp_mean (0.16) => ranks raw features (route/size), not a driver-vs-vehicle split.
- Pooled ablation: 1.23 L/100km per-vehicle systematic effect remains UNATTRIBUTED without explicit
  vehicle modelling; our decomposition recovers it as the vehicle-baseline component.
Conclusion: detection + relevance DETECT and RANK; only our method ATTRIBUTES a trip's excess to
driver vs vehicle components. Capability increment, honestly not a labelled-accuracy win.
