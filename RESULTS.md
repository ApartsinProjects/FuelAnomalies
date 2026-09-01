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

## P15 — E6: second behaviour dataset at VED-like 1 Hz (UAH-DriveSet, 6 drivers)
Credential-free UAH-DriveSet processed 1 Hz streams from a public GitHub mirror (official server down;
NOT redistributed - data/ gitignored; cite UAH-DriveSet as source). 940 windows (30 s), 172 aggressive
/ 768 normal, 6 drivers. Kinematic features (accel magnitude std/p95, lateral/longitudinal std, jerk,
harsh-lat rate, speed std/mean) at 1 Hz; aggressive-vs-normal, leave-one-driver-out (6 folds).
- Univariate AUC: lon_std 0.81, mag_p95 0.71, mag_std 0.70, jerk_rms 0.69, speed_std/mean 0.67.
- **LODO AUC: logreg 0.829, RF 0.808; per-driver 0.76-0.92; permutation mean 0.50, p=0.001.**
=> Kinematic/behaviour axis transfers to a SECOND dataset, 6 drivers, at VED-like 1 Hz (lower than
Zenodo's 400 Hz 0.958, as expected for the coarser regime). Addresses reviewer W7/E6.

## P16 — Real-data strengthening (scripts/p16_strengthen.py)
#1 Real high-kinematic vs high-combustion(trim) VED trips (natural variation, NO injection):
  kinematic-dominant excess mean +0.574 L/100km (median 0.457, n=1421); combustion-dominant -0.337
  (n=1466), at the both-low reference level (-0.339); MWU p=8.6e-37. corr(excess, kinematic z)=+0.222,
  corr(excess, |trim| z)=-0.002; even in highest-trim quartile corr=-0.029, mean excess -0.049.
  => On REAL trips the driver signature predicts fuel excess; the fueling-correction signature does not
  (healthy fleet). Real-data support for the driver axis + real orthogonality (complements synthetic).
#3 Fault-signature specificity on the real bench: combustion% vs normal = rich +4.17, lean -2.24,
  ignition -1.94. Fuel-fault flag rate (excess>0.3 AND combustion elevated): normal 0.022, rich 0.289,
  lean 0.095, ignition 0.100 => TPR(rich)=0.29 vs FPR(non-fuel avg)=0.07. The vehicle-fuel-fault
  signature is SPECIFIC to the rich (over-fuelling) fault; lean/ignition (not fuel faults) do not fire it.

## P17 — CORRECTED attribution (fixes Fable BUG-1..4; supersedes P8/P13 headline)
scripts/p17_attribution_fixed.py. Fixes: (1) unit-SD axes (P8 left kinematic axis at sd 0.55 vs
combustion 0.99 -> the old 95.9% trained vs 88.6% frozen gap was largely THIS normalization artifact;
at unit-SD both ~0.89 at symmetric S=1.66); (2) FEATURE-LEVEL driver injection along the real UAH
aggressive direction, scored with FROZEN weights (old score-level injection made weights irrelevant);
(3) MEASURED fuel-only baseline; (4) ASYMMETRIC calibration (driver Cohen's d = 0.65 from UAH 1 Hz;
fault 1.66 SD from bench).
- **Frozen source-derived attribution = 0.785** at realistic (S_driver=0.65, S_fault=1.66); trained
  upper bound 0.812; **falsification: negated driver weights -> 0.599, shuffled -> 0.727** (learned
  signature genuinely contributes); MEASURED fuel-only = 0.496 (chance).
- Honest headline is ~0.78-0.81, NOT 88.6/95.9. Driver effect at realistic aggression (d=0.65) is
  weaker than the bench fault (1.66 SD) -> asymmetric; accuracy rises with driver severity.
- Also fixes false claim in old 8.3 ("attributor sees vehicle baseline" - P8 X had 2 cols, no baseline).

## P19 — Conformal LR-fusion attribution (method upgrade for Algorithm 1)
scripts/p19_conformal.py. Replace margin-argmax with source-calibrated likelihood-ratio fusion +
split-conformal abstention. LR fusion accuracy = 0.812 (matches trained upper bound -> principled
fusion recovers what training does, zero-shot). Conformal selective risk (calibrated on held-out
normal, guarantee P(err|decide)<=alpha): a=0.05 -> coverage 0.459, realized error 0.048; a=0.10 ->
coverage 0.689, error 0.101; a=0.20 -> coverage 1.0, error 0.192. Guarantee holds empirically.
Also: orthogonal-weights floor (no driver info, fault axis alone) = 0.697; frozen 0.785 (+0.09),
negated 0.599 (-0.10). Airtight falsification.

## P18 — Hardening (scripts/p18_harden.py)
A. P16 #1 TRIM-CORRECTED: kin-dominant excess +0.585 (blind +0.576), comb-dominant -0.342 (blind -0.341),
   corr(excess,|trim|z)=0.00 either way. Trim-blindness objection FULLY answered; result robust.
B. P16 #3 OOF normal reference: flag rates normal 0.026 (in-sample 0.022), rich 0.288, lean 0.094,
   ignition 0.099. Specificity contrast survives OOF. BUT continuous per-sample fuel-fault score AUC
   (rich vs normal) = 0.58 -> specific but sensitivity operating-point-dependent (consistent w/ blocked-CV).
C. s_veh fold-demeaned: plain 0.128 -> fold-demeaned 0.125 -> reseed 0.125 (on trim subset). Fold-bias
   removes only ~0.003 -> vehicle-baseline share NOT a fold artifact.

## Cycle-3 corrections (Fable adversarial pass 3)
- CONFORMAL FIX (p19): calibration set is held-out VEHICLES' injected labelled variants (NOT "normal
  trips" - that was wrong). Added Hoeffding finite-sample UCB (delta=0.1): a=0.05 -> coverage 0.309,
  realized error 0.031; a=0.10 -> 0.646/0.088; a=0.20 -> 1.0/0.192. Guarantee now HOLDS (was 0.101>0.10).
  Conformal threshold IS calibrated on synthetic labels (carve-out to "no joint supervision"); deployable
  analogue = calibrate on injections synthesized from the customer fleet's own normal trips.
- CLOSED-FORM (item 1b): Table 7 = Gaussian theory. Bayes=Phi(sqrt(0.65^2+1.66^2)/2)=0.813 (measured
  trained/LR 0.812); argmax 0.5*(Phi(.65/sqrt2)+Phi(1.66/sqrt2))=0.778 (measured 0.785); orth floor 0.690
  (measured 0.697); negated 0.601 (measured 0.599). LR = Bayes rule of the injection model, so 0.812=upper
  bound is EXPECTED not a discovery. Reframe: empirical agrees with theory (validates unit-var Gaussian
  score model on real VED); evidential weight = calibration constants + falsification + real-data P16.
- DEPLOYED SIGNATURE (item 1d): the 4-feature speed-only UAH signature used in 8.3 has LODO AUC=0.694
  (OOF Cohen d=0.44), DISTINCT from the richer 6.3 signature (AUC 0.829). TRIP-LEVEL (recording-aggregated)
  Cohen d=1.27 >> window-level 0.65 -> 0.65 is CONSERVATIVE; realistic trip-level operating point gives
  attribution ~0.86 (sweep 1.5->0.874). Report both; deployed-signature AUC honestly.

## P20/P21 (Fable items 4 & 5) — 2026-08-31, run locally (7s and 13s; RunPod unnecessary for these CPU-only sklearn jobs)
- P20 (scripts/p20_driver_fuelcost.py) DRIVER INJECTION REAL FUEL COST: push the feature-level driver
  perturbation (Cohen d=0.65, along real UAH aggressive direction) through the expected-fuel model M.
  Raw per-feature step: speed_std +2.40, accel_p95 +0.154, harsh_accel_per_km +0.049, jerk_rms +0.014.
  RESULT: driver injection raises fuel by +1.07% MEDIAN (mean +1.31%, p90 +3.53%) vs bench fault +6.2%.
  => The two causes are NOT fuel-matched: a realistic-aggression driver signature costs ~1% fuel, well
  below the fault's 6.2%. This SHARPENS the thesis (attribution matters: same anomaly-detector trigger,
  very different magnitude AND cause), and corrects any implicit "equal fuel penalty" assumption.
- P21 (scripts/p21_realdata_attribution.py) REAL-DATA WEAK-LABEL ATTRIBUTION (no injection): CIRCULAR
  NON-RESULT, recorded as a methodological finding, NOT a paper number. Proxy labels built from the two
  signature axes (driver=top-decile kinematic+excess>0; fault=top-decile within-veh combustion+excess>0;
  contested both-high excluded). LR-fusion accuracy 0.999 EVEN after removing the mutual-exclusion clamp.
  ROOT CAUSE (verified): the classifier decides on the SAME two axes that define the proxies, so any proxy
  drawn from those axes is trivially recovered -> accuracy carries ZERO information. CONCLUSION: on VED
  (no ground-truth cause labels) attribution ACCURACY cannot be validated on real data at all; this is
  exactly why calibrated semi-synthetic injection is the only route to a ground-truth attribution number.
  What real data DOES support (no synthetic): group sizes 662 driver-proxy / 469 fault-proxy / 63 contested
  out of 11,304; both carry real positive excess (driver 1.65, fault 1.58 L/100km). Use as a descriptive
  triage-yield statement, not an accuracy claim.

## P22 (Fable Edit 6) — magnitude-fusion, DEMONSTRATE the floor — 2026-08-31 (9s local)
scripts/p22_magnitude_fusion.py: add per-trip excess-magnitude as a THIRD likelihood channel to the
p19 fusion, calibrated to REAL per-cause fuel effects (driver +1.07% median via model M, fault +6.2%
bench), with magnitude NOISE = real OOF fuel residual sd = 17.1%.
RESULT: 2-channel (equal-mag) 0.812 -> 3-channel (with magnitude) 0.815 (gain +0.003). Magnitude-ONLY
0.562 (near chance). Equal-mag control 0.808 ~ floor.
VERIFIED vs closed form: magnitude d=(6.2-1.07)/17.12=0.30 -> Bayes Phi(0.15)=0.560 matches magonly
0.562; 3ch sqrt(1.77^2+0.30^2)=1.795 -> Phi(0.897)=0.815 matches. All invariants pass (I1 3>=2, I2
magonly>0.5, I3 equal-mag recovers floor).
INTERPRETATION (stronger than "loose floor"): per-trip fuel magnitude is nearly useless for attribution
because trip-to-trip noise (17%) swamps the 5-pt gap -> (a) the equal-fuel floor is TIGHT (magnitude
adds 0.003), (b) closes the "just threshold the excess" objection with a number: thresholding attributes
at 0.562 (chance) per trip while signatures give 0.812. Signatures, not magnitude, carry the attribution.
Over many trips of a vehicle the magnitude gap becomes usable; per trip it is not. Paper 8.3 corrected
(removed the earlier overstatement that fusing magnitude does "strictly better" -> honest +0.003 + the
threshold-rebuttal). results.json magnitude_fusion.

## P23 (Fable pass-2) — S_fault sensitivity + combustion aggregation — 2026-08-31 (local)
scripts/p23_sfault_sensitivity.py. Motivated by Fable pass-2: (i) headline is arithmetic in two
calibrated constants; S_fault (bench-AFR -> fleet-trim transfer) is the one never observed on a real
faulted vehicle; (ii) per-sample fault sensitivity (AUC 0.58/TPR 0.29) is a single-reading number.
(A) S_fault SWEEP [0.5..3.0] at S_driver=0.65 (empirical injection vs closed-form, agree <0.01):
    0.5->0.66, 0.8->0.70, 1.0->0.72, 1.33->0.76, 1.66->0.785, 2.0->0.805, 2.5->0.825, 3.0->0.834.
    => accuracy above chance across a 6x range; assumed 1.66 sits mid-curve; genuine fault (drives trim
    beyond normal variation) occupies the upper part. WEB SCOUT (web-researcher): NO public dataset pairs
    a confirmed fueling DTC (P0171/P0172) with logged closed-loop trims (VED/HCRL/Barreto have trims no
    faults; DEFault/EngineAD/EdgeImpulse have faults no usable trims). So S_fault is an open field
    measurement; paper 8.4 SWEEPS it + 9.4/10 name it as the reachable missing benchmark.
(B) Combustion AGGREGATION AUC (EngineFaultDB, mean combustion score over n rich vs normal): per-sample
    0.54 (d=0.41) -> n=5 0.76 -> n=10 0.80 -> n=20 0.92 -> n=50 0.99. Invariant (monotone & >=0.9 by 20)
    PASSES. Added to Sec 7: the single-reading 0.58 weakness is not the regime attribution operates in
    (persistent per-vehicle signal). results.json: sfault_sensitivity, combustion_aggregation.
Fuel-only canonical value re-confirmed 0.496 (was 0.497 stale in results.json/RESULTS.md; synced).

## P24 — construct-matched operating points (foreground realistic trip-level) — 2026-09-01
scripts/p24_operating_points.py. Motivation (user: "numbers seem small"): the headline 0.785 is the
DELIBERATELY CONSERVATIVE window-level (d=0.65, magnitude withheld) point. p14's AUROC 0.951 is from the
SUPERSEDED symmetric score-level S=1.66 injection and must NOT be quoted beside 0.785 (construct mismatch).
Recomputed accuracy + AUROC/AUPRC from the SAME p17 feature-level asymmetric injection at two points:
- window-level d=0.65 (conservative floor): acc 0.785, AUROC 0.878, AUPRC 0.871
- trip-level d~1.3 (realistic; VED records whole trips, aggregation raises aggressive-vs-normal effect
  0.65->~1.3): acc 0.856, AUROC 0.931, AUPRC 0.928
Cross-check: 0.856 matches severity sweep interpolation (d=1.0->0.827, 1.5->0.874). VERIFIED.
Paper reframed to FOREGROUND trip-level 0.856/AUROC 0.93 as realistic, keep 0.785 as conservative floor
(abstract, 8.3, contributions, conclusion, Fig7 caption). Also: abstract behaviour phrasing -> "up to 37%
(8% uniquely)"; 9.2 absolute-scale value sentence (small % = large recurring fleet cost). results.json
operating_points + stress AUROC annotated SUPERSEDED.
