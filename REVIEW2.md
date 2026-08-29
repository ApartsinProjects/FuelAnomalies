# Fable review of FULL paper (v0.4, 2026-08-29)

**Verdict: MINOR REVISION (borderline, leaning accept).** Science holds; the design, evidence chain,
and honest framing are strong. Blocking issues are number-traceability/consistency, all cheap to fix.

## MUST-FIX (before submission)
1. **Combustion R2 on driver-excess appears as both -0.039 (Table 6/8.1, from P6) and -0.028 (8.4, from
   P9)** — same construct, two scripts. Reconcile to one co-computed value or add an explanatory clause + log.
2. **"R2 <= 0" (abstract + Contribution 3) is contradicted by the paper's own trim-corrected +0.012.**
   Replace with "R2 ~ 0" / "within 0.02 of zero" / "at most ~1%".
3. **Panel attribution mismatch**: Contribution 2 + abstract pair the decomposition with "14,460 trips",
   but it was computed on 14,170/194 (Table 4 caption correct). Fix to 14,170; also LOG the 14,460/197
   panel size in RESULTS.md (currently unlogged).
4. **Table 5 lean/ignition BSFC (-29%, -35%) untraceable in RESULTS.md text** (they ARE in p5b output:
   lean 1.534, ignition 1.411 vs normal 2.175) and physically odd (misfire using less fuel/work =
   operating-point-sampling artifact). Add a table note explaining, or drop the BSFC cells for non-rich rows.

## SHOULD-FIX
5. Recompute Table 4 in ONE pass so all 6 rows come from one artifact and shares sum exactly
   (1-0.673-0.143=0.184 vs listed 0.185; P3 vs P9 third-decimal drift on env 0.592/0.593 etc.).
6. Log the decile Spearman (rho=0.964, p=7.3e-6; so "p<1e-5" is slightly off, use p<1e-4 or exact).
   Fix S_bench rounding: 3.0/1.79=1.68 not 1.66 (or state unrounded inputs).
7. In 8.3, add one line: injection assumes the hypothesis's axis-separability (measures detectability
   vs real noise, not the truth of separability, which rests on bench + silent cell). Also: measured
   accuracy (0.946@S1.5, 0.959@S1.66) EXCEEDS the Gaussian-optimal Phi(S/sqrt2)~0.86-0.88 — explain
   (median-SD calibration + model sees vehicle baselines); report empirical axis dispersion / axis corr.
8. Report corr(kinematic, combustion) on VED to back "nearly orthogonal" in 9.1.

## NICE-TO-HAVE
- Rename figure files to match caption numbers (Fig2 loads fig1_*, Fig6 loads fig2_double_dissociation,
  etc.); rename fig2_double_dissociation -> signature_contrast.
- Permutation "p <= 0.001" (1000-perm floor). Remove em-dashes from Figure 1 SVG labels + &mdash; (house style).
- Trim triple repetition of "healthy fleet, trims small" (6.2/9.3/10) and the duplicated benchmark call
  (9.4 + conclusion). Abstract: "95.9%" not "96% (CI [0.956,0.962])" precision mismatch.

## Numbers that CHECK OUT (audited vs RESULTS.md)
R2 0.673 [0.628,0.709], MAPE 13.3%, seeds 0.672-0.676, counterfactual 0.47/1.59 + deciles, FE 23%,
rich +0.498/+6.2%/AFR 13.68/+7.5%/BSFC +10.6%, kinematic 0.107, bench 0.903 (CO 0.73/HC 0.44/AFR&lambda
0.12, corr 1.0), univariate -0.106/+0.333, SMD 0.09/0.27/0.09, baselines, AUC 0.958 [0.927,0.981]
per-driver 0.984/0.934/0.992 RF 0.79, attribution curve + 0.959 [0.956,0.962], trims 1.5%/11%, LTFT SD
1.79/4.41, high-trim r -0.14, 11,520/139, 169=143+26. Equations dimensionally correct; shuffled-CV note good.
