import re, sys
h=open('index.html',encoding='utf-8').read()

def rx(s):  # whitespace-flexible literal matcher
    return re.compile(r'\s+'.join(re.escape(w) for w in s.split()))

reps=[
('<div><span class="badge">Working draft</span><span class="badge">v0.4 (full)</span></div>',''),
('<div class="status">Full-length draft. Every number is a computed result traceable to a script in <code>scripts/</code> and an entry in <code>RESULTS.md</code>; confidence intervals are cluster bootstraps. References validated with bibtest.</div>',''),
('Because no public dataset carries fuel, mechanical-fault labels, and driver behaviour jointly, we adopt a two-arm design on real data',
 'No public dataset carries fuel, mechanical-fault labels, and driver behaviour jointly. We therefore adopt a two-arm design on real data'),
('(held-out \\(R^2\\) within 0.02 of zero), a silence that survives a trim-corrected',
 '(held-out \\(R^2 = -0.03\\)), a silence that survives a trim-corrected'),
('(held-out \\(R^2\\) within 0.02 of zero), a silence that survives trim-corrected fuel and the',
 '(held-out \\(R^2 = -0.03\\)), a silence that survives trim-corrected fuel and the'),
('A variance decomposition of trip fuel on a 197-vehicle public fleet (14,170 trips after fuel-quality filtering)',
 'A variance decomposition of trip fuel on a public fleet of 194 vehicles (14,170 trips after fuel-quality filtering of the 197-vehicle, 14,460-trip panel)'),
('An account of the field-wide absence of any joint fuel + fault + behaviour dataset, and a reproducible pipeline',
 'A documented survey of the joint fuel + fault + behaviour data gap, and a reproducible pipeline'),
('The evidence chain runs as follows:','The evidence chain (Figure 1) runs as follows:'),
('decompose that excess into a driver-behaviour component and a vehicle component.',
 'decompose that excess into a driver-behaviour component and a vehicle component (the vehicle-baseline defined in Section 4.3).'),
('lack driver context or ship dimensionality-reduced,','lack driver context or ship only dimensionality-reduced features,'),
('This documented gap is the reason for the two-arm design and the semi-synthetic bridge.',
 'This documented gap (Table 2) is the reason for the two-arm design and the semi-synthetic bridge.'),
('and the unexplained share is \\(1-R^2_{\\text{full}}-s_{\\text{veh}}\\).</p>',
 'and the unexplained share is \\(1-R^2_{\\text{full}}-s_{\\text{veh}}\\); here \\(\\bar e\\) and \\(\\bar f\\) are the fleet-mean residual and fleet-mean trip fuel.</p>'),
('A logistic attributor is trained on the two axis-deviations, \\((z^k, z^c)\\), under GroupKFold by vehicle',
 'A logistic attributor is trained on the two axis-deviations \\((z^k, z^c)\\) together with the vehicle baseline, under GroupKFold by vehicle'),
('Because no cause-labelled trip benchmark exists on real data, these comparisons establish a capability contrast; the quantitative accuracy comparison is the semi-synthetic experiment of Section 4.5.',''),
('Decomposing the variance of trip fuel (Table 4) shows','Decomposing the variance of trip fuel (Table 4, Figure 2) shows'),
('per-driver 0.984, 0.934, 0.992). A random forest reaches 0.79','per-driver 0.984, 0.934, 0.992; Figure 4). A random forest reaches 0.79'),
('A 1,000-permutation test collapses the AUC to chance (permuted mean 0.471, \\(p \\le 0.001\\)).',
 'Under a 1,000-permutation test the label-permuted AUC falls to chance (mean 0.471), placing the real AUC at \\(p = 0.001\\).'),
('Scoring the faults (Table 5), only the rich mixture burns measurably more: <b>+0.498 L/100km, or +6.2%</b>',
 'Scoring the faults (Table 5, Figure 5), only the rich mixture burns measurably more: <b>+0.50 L/100km, or +6.2%</b>'),
('<tr><td>Rich mixture (1)</td><td class="num">+0.498</td>','<tr><td>Rich mixture (1)</td><td class="num">+0.50</td>'),
('Regressing each excess on each axis (Table 6) gives the central qualitative result. The kinematic axis explains driver-caused excess (held-out \\(R^2 = 0.107\\))',
 'Regressing each excess on each axis (Table 6, Figure 6) gives the central qualitative result. The kinematic axis explains driver-caused excess (held-out \\(R^2 = 0.084\\))'),
('<tr><td>Kinematic (transient aggression)</td><td class="num">0.107</td>','<tr><td>Kinematic (transient aggression)</td><td class="num">0.084</td>'),
('This reproduces, as an independent consistency check, an earlier finding that per-vehicle fuel residual does not track fuel-trim drift on VED.',''),
('the fleet is healthy, its fuel trims are small, and the trims do not track efficiency, which is why the malfunction side of the attribution is anchored on a controlled bench rather than observed in the fleet.',
 'the fleet is healthy, which is why the malfunction side of the attribution is anchored on a controlled bench rather than observed in the fleet.'),
('The two-arm design is a response to a missing dataset, and naming what would close the gap turns the limitation into an agenda:',
 'Naming what would close the joint-data gap (Section 3.4) turns it into an agenda:'),
('<td><b>yes (measured, 96%)</b></td>','<td><b>yes (measured, 95.9%)</b></td>'),
('96% on ground truth','95.9% on ground truth'),
('<p class="kv" style="color:var(--muted)">All entries validated against Crossref/OpenAlex/DataCite (bibtest).</p>',''),
('scripts/p1_features.py</code> through <code>scripts/p9_bench_behav.py</code>','scripts/p1_features.py</code> through <code>scripts/p10_consolidated.py</code>'),
('Full-length working draft. Every filled number traces to a script in <code>scripts/</code> and an entry in <code>RESULTS.md</code>. &copy; 2026 Alexander Apartsin and Yehudit Aperstein.',
 '&copy; 2026 Alexander Apartsin and Yehudit Aperstein.'),
('On a 197-vehicle public fleet, behaviour and a persistent vehicle-baseline account for measurable 8% and 14% shares',
 'On a 194-vehicle public fleet, behaviour and a persistent vehicle-baseline account for measurable 8% and 14% shares'),
]
miss=[]
for old,new in reps:
    pat=rx(old); found=pat.findall(h)
    if len(found)!=1:
        miss.append((len(found),old[:70])); continue
    h=pat.sub(lambda m:new, h, count=1)
if miss:
    print("PROBLEMS:")
    for n,s in miss: print(f"  count={n}: {s!r}")
    sys.exit(1)
open('index.html','w',encoding='utf-8').write(h)
print("applied",len(reps),"edits OK")
