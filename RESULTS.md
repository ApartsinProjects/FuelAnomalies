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

## P8 — Semi-synthetic ATTRIBUTION ACCURACY (must-fix #3 / reviewer W6)
Inject driver-caused vs fault-caused excess into 11,520 real VED trips (139 vehicles) with the SAME
fuel increase for both (so fuel magnitude alone cannot attribute). Signature attributor = kinematic +
combustion deviations vs vehicle baseline; GroupKFold by vehicle. Fuel-only baseline = chance control.
- Accuracy vs signature strength S (within-vehicle SD units): S0.5=0.713, S1=0.866, S1.5=0.946,
  S2=0.979, S2.5=0.992, S3=0.998. Fuel-only baseline pinned at ~0.50 throughout (as designed).
- **Bench-calibrated operating point**: bench rich fault = 3.0% fuel/air shift; VED within-vehicle LTFT
  SD (median) = 1.79% => S_bench ~= 1.66. **Attribution accuracy at S_bench = 0.959 (F1 0.959)**,
  near-symmetric confusion (~4% error each way).
Result: at a realistic (bench-calibrated) fault magnitude the signature attributes driver-vs-fault
excess at 96% while fuel magnitude alone is at chance. Directly measures attribution (fixes W6);
controls the injected effect size, sidestepping the trim-blind-target (W1) and range-restriction (W2)
critiques.

## P9 — Revision statistics (CIs, W1/W2/W4 rebuttals)
Cluster-bootstrap CIs (by vehicle, 1000x) + fixes for reviewer W1/W2/W4/W8. Scripts p9_ved_stats.py,
p9_bench_behav.py. JSON: data/processed/p9_*.json.
- **CIs**: fuel model R2 0.673 [0.628, 0.709]; MAPE 13.3% [12.3, 14.3]; env share 0.593 [0.542, 0.636];
  behaviour marginal 0.080 [0.060, 0.102]; vehicle-baseline 0.143 [0.114, 0.174]. Seed-stable (0.672-0.676).
- **W1 trim-correction**: driver-excess combustion R2 = -0.028 (trim-blind fuel) -> +0.012 (trim-corrected
  fuel MAF*(1+STFT+LTFT)/14.7). Dissociation SURVIVES; trims too small (median 1.52%, p90 11.04%) to matter.
- **W2 range restriction**: within-veh LTFT SD 1.79%, between-veh 4.41%. In the highest-trim 47 vehicles,
  corr(excess, LTFT) = -0.14 -> combustion still silent even where trim varies most.
- **W4 collinearity of bench 0.903**: single-feature R2 CO=0.734, HC=0.444, AFR=0.123, Lambda=0.121;
  corr(AFR,Lambda)=1.0. The 0.90 is carried by CO/HC (unburnt-fuel emissions), not one collinear feature;
  AFR-fuel coupling acknowledged. (NOTE: bench CV must SHUFFLE — Fault column is grouped/ordered; non-shuffled
  cv=5 spuriously gives -0.34. p6 already shuffled correctly; caught a bug in the p9 check.)
- **W4 covariate overlap** normal vs rich (standardized mean diff): RPM -0.09, Power -0.27, Speed -0.09
  (modest). Fault-0 not pristine: lambda 0.957, CO 2.16%.
- **Behaviour** (n=169, 143 aggressive/26 non): logreg AUC 0.958 [0.927, 0.981], RF 0.79; 1000-perm
  mean 0.471, p=0.001.
- **Attribution accuracy** at bench-calibrated S=1.66: 0.959 [0.956, 0.962].

## P10 — Consolidated one-pass VED numbers (revision consistency; scripts/p10_consolidated.py)
Single config HistGBM(300,0.05,depth5,seed0), GroupKFold(5) by vehicle, on the 14,170-trip/194-vehicle
decomposition panel (the featurization panel before 1-99% fuel clipping is 14,460 trips / 197 vehicles).
All shares from ONE artifact and sum to 1.0:
- R2_full 0.673, R2_env 0.593, R2_behav 0.368, behaviour-marginal 0.080, env-marginal 0.305,
  vehicle-baseline 0.143, unexplained 0.184 (sum = 1.000).
- Combustion axis on driver-excess (ONE reconciled value): trim-blind R2 = -0.028, trim-corrected +0.012;
  kinematic axis on driver-excess R2 = 0.084.
- Axis orthogonality: corr(kinematic, combustion) within-vehicle = -0.012 (p=0.21, n=11,609) -> ~orthogonal.
- S_bench = 1.66 (from unrounded 2.98% shift / 1.79% median within-vehicle LTFT SD; rounded inputs 3.0/1.79=1.68).
- Decile monotonicity Spearman rho=0.964, p=7.3e-6 (< 1e-5).
NOTE: supersedes the earlier -0.039 (P6) combustion value; use -0.028 everywhere.

## P11/P12 — EAAI-review revision experiments (scripts/p11_eaai_ved.py, p12_eaai_trim_bench.py)
- **E1 cross-fitted vehicle-baseline (W2)**: in-sample share 0.143; HELD-OUT (split-half, estimate on
  half A, evaluate on half B) share 0.136-0.138 across min-trips 5/10/15/20; split-half reliability
  r=0.949 (160 veh, >=10 trips); shrinkage share 0.138. => vehicle component is REAL and stable, not an
  in-sample group-mean artifact.
- **E9 model comparison (expected fuel)**: mean -0.005, ridge 0.663, RF 0.640, HGB 0.673 => conclusions
  not specific to HGB (ridge nearly matches).
- **E10 leakage ablation**: operational (no RPM/load) R2=0.673; max-prediction (+RPM/load) R2=0.738
  (+0.065). Vehicle-share stable (0.143 vs 0.153). RPM/load are engine outputs, excluded for attribution.
- **E2 fuel-trim semantics (W3)**: driver-excess combustion R2: STFT-only 0.019, LTFT-only -0.051,
  both -0.028; trim-corrected additive 0.012 vs multiplicative 0.018 (median fuel diff 0.002 L/100km,
  negligible). Silence robust to STFT/LTFT split and correction form. Reframe axis as FUELING-CORRECTION.
- **E7 bench blocked CV (W9)**: rich-fault combustion R2: all-sensors shuffled 0.903 vs
  leave-operating-region-out (RPMxPower terciles) -0.483; deployable subset {AFR,Lambda,O2} shuffled
  0.918 vs blocked 0.123. => the 0.903 is within-region interpolation; it does NOT generalize across
  operating regions. The +6.2% matched-mean rich effect is a group comparison and is unaffected.
- **E8 counterfactual reference sensitivity**: behaviour-component median at gentle-reference percentile
  q10/q20/q30 = 0.41 / 0.49 / 0.25 L/100km (same order of magnitude; q20 used in paper).

## P13 — Frozen source-signature attribution (EAAI E3; scripts/p13_frozen_attribution.py)
Driver signature = logistic FROZEN from the external Zenodo aggressive-driving data (kinematic features
matched to VED: variability, p95, harsh-rate). Fault signature = combustion axis, direction+magnitude
from the bench. Neither is fit to the VED injection labels. Attribution rule = predict fault iff
standardized combustion score > kinematic score (argmax, zero-shot).
- Frozen argmax vs trained-on-injection logistic vs fuel-only, by S:
  S0.5 0.643/0.644/0.50 ; 1.0 0.769/0.768/0.50 ; 1.5 0.863/0.863/0.50 ; **Sbench1.66 0.886/0.886/0.50** ;
  2.0 0.924/0.925/0.50 ; 3.0 0.980/0.981/0.51.
  => FROZEN zero-shot rule MATCHES the trained upper bound; the 95.9% (P8, trained) is an upper bound,
  the honest transfer number at bench magnitude is ~0.886. Fuel-only stays at chance.
- Abstention (frozen, S_bench): tau0 cov1.00 acc0.886 ; tau0.5 cov0.86 acc0.929 ; tau1.0 cov0.71 acc0.957 ;
  tau1.5 cov0.56 acc0.971 ; tau2.0 cov0.41 acc0.982. => abstaining on ambiguous cases trades coverage for accuracy.

## P14 — Stress tests (E4) + task-aligned baselines (E5); scripts/p14_stress_baselines.py
Built on the frozen source-derived scores (p13). All zero-shot unless noted.
- E4 mixed-cause 2D grid (dominant-cause accuracy vs driver effect Sd x fault effect Sf): high off-diagonal,
  ~0.5 near the diagonal (ambiguous when both causes equal). Figure figures/mixed_cause_grid.
- E4 Gaussian score noise: acc 0.886 (sd0) -> 0.857 (0.5) -> 0.798 (1.0) -> 0.740 (1.5). Graceful.
- E4 systematic combustion bias: 0.886 -> 0.874 (0.5) -> 0.834 (1.0).
- E4 missing trim (combustion score dropped): 0.886 -> 0.851 (20%) -> 0.798 (50%).
- E4 probabilistic metrics at S_bench (frozen prob=sigmoid(cz-kz)): AUROC 0.951, AUPRC 0.945, Brier 0.092.
- E5 baselines at S_bench: frozen argmax 0.886; raw-threshold rule 0.891; likelihood-ratio prototype 0.886;
  trained full-feature logistic (upper bound) 0.952; fuel-only 0.506 (chance). => multiple signature-based
  attributors all ~0.88-0.89 zero-shot; fuel magnitude at chance. Robust to attributor choice (W10).
