# Fable peer review (2026-08-29) — submission readiness

**Verdict: NOT submission-ready; MAJOR REVISION. Core idea publishable; hygiene is a real asset.**
Best-fit venue after revision: IEEE T-ITS. Current-state readiness: IEEE Access / Sensors.

## Three decisive issues (resolvable with data in hand)
- **W1 trim-blind target**: VED fuel = MAF/14.7 assumes stoichiometric AFR, so trim-driven excess is
  subtracted out BEFORE analysis. The "combustion axis silent on VED" cell is partly guaranteed by the
  derivation. FIX: re-derive fuel as MAF*(1+STFT+LTFT)/14.7 and show the dissociation survives.
- **W2 range restriction**: VED is a healthy fleet (median trim +1.5%); the combustion axis may be
  silent simply because it has no variance there. FIX: analyze the high-trim tail (|LTFT|>p75); test
  excess-vs-trim where trim actually varies. Also: the "Driver-excess (VED)" column is really total
  residual (mostly vehicle-baseline+noise), so it over-labels.
- **W6 no attribution accuracy measured**: the method outputs a per-trip split but nothing evaluates
  if it's correct. FIX (highest value): semi-synthetic injection — inject bench-calibrated rich-fault
  fuel inflation (+6.2%) and known aggression perturbations into held-out VED trips, report attribution
  accuracy vs injected ground truth.

## Other major weaknesses
- **W3/W4**: not really a "double" dissociation (1 cell tautological [AFR-fuel coupled], 1 absent
  [kinematic n/a on bench], 1 weak [kinematic R2 0.107 on driver-excess], 1 genuine [combustion silent
  on VED, threatened by W1/W2]). Rename to "signature contrast"/"single dissociation". Move the
  tautological R2=0.90 out of the headline. Explain the 0.33 univariate r vs 0.90 multivariate R2 gap
  (collinearity/overfit check).
- **W5 title over-claims malfunction**: no real-fleet trip is ever attributed to a malfunction; vehicle
  side is heterogeneity, not fault. Retitle.
- **W7 behaviour validation fragile**: 169 events/3 drivers, 143:26 imbalance, LogReg 0.958 >> RF 0.783
  (report both), permutation p=0.032 floor-limited (run 1000+), validates 400Hz accel amplitude (NOT
  VED 1Hz features; jerk fails at 400Hz). Scope the claim to what was shown.
- **W8 no statistical rigor**: no CIs anywhere; add cluster-bootstrap CIs (by vehicle/driver), fold/seed
  stability for the decomposition.
- **W9 related work too thin** (7 refs; T-ITS expects 40+, positioning table, cite VT-Micro/PdM/trim
  diagnostics).
- **W10 bench operating-point confound**: show covariate overlap for "matched operating point".

## MUST-FIX (blocks submission)
1. Trim-corrected fuel re-run of the dissociation (W1).
2. Range-restriction / high-trim-tail analysis; relabel VED column (W2).
3. Semi-synthetic attribution-accuracy experiment (W6). Highest-value single addition.
4. Reframe/rename dissociation; move R2 0.90 out of headline; explain 0.33->0.90 gap (W3/W4).
5. Retitle (W5).
6. Bootstrap CIs everywhere; 1000+ permutations; decomposition stability (W7c/W8).

## SHOULD-FIX
Report RF alongside LogReg + class counts + per-driver CIs; bench covariate-overlap + note fault-0 not
pristine (lambda 0.957); resolve 2-vs-3 label mapping (OCR Table 4 or contact authors); expand related
work + positioning table; run the 1Hz smoothing ablation promised in PLAN; scope behaviour-validation
claim (feature/rate shift, jerk-at-400Hz failure).

## NICE-TO-HAVE
Worked per-trip decomposition figure (the product the intro sells); release code+processed features w/
DOI (zenodo-publish); VED Part 2 temporal stability; HEV appendix.

## Missing for real submission
Statistics (CIs, effect sizes not just p; ANOVA F=840 on 56k rows is trivially sig); reproducibility
(seeds, pins, one-command run, released features+code DOI); related-work depth; ethics paragraph
(driver-scoring = worker surveillance; misattribution has employment consequences); Fig 5 must visibly
mark which cell is tautological vs evidential.

## Title / abstract
Current title over-promises. Suggested: "Kinematic and Combustion Signatures Separate Driver-Caused
from Fault-Caused Excess Fuel Consumption: Cross-Dataset Evidence from Fleet Telemetry and an
Engine-Fault Bench" (or "Driver or Vehicle? Signature-Based Attribution of Excess Fuel Consumption on
Public Data"). Abstract: replace "double dissociation establishes" with the scoped claim; add the
credibility sentence (survives trim-correction + high-trim subset) after MUST-FIX 1-2; add one
quantitative payoff with CIs; drop "R2 0" phrasing (a negative held-out R2 = "no explanatory power").
