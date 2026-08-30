import re,sys
h=open('index.html',encoding='utf-8').read()
def rx(s): return re.compile(r'\s+'.join(re.escape(w) for w in s.split()))
reps=[
# M1a Table 7 header
('<th class="num">Frozen transfer</th><th class="num">Trained upper bound</th><th class="num">Fuel-only</th>',
 '<th class="num">Frozen transfer</th><th class="num">Trained on same scores</th><th class="num">Fuel-only</th>'),
# M1b + M3 8.4 text (cite Table 7, disambiguate the two upper bounds)
('this\n  zero-shot rule reaches\n  <b>88.6% accuracy</b>, essentially equal to the trained upper bound (0.886 vs 0.886) and far above the\n  fuel-only chance level; the two track across effect sizes (0.86 at S = 1.5, 0.92 at S = 2.0).',
 'this zero-shot rule reaches <b>88.6% accuracy</b> (Table 7), matching a logistic classifier trained on the injected labels over the same two scores (0.886 vs 0.886) and far above the fuel-only chance level; the full-feature classifier of Section 8.3 sets the upper bound at 95.9%, and the frozen and same-score curves track across effect sizes (0.86 at S = 1.5, 0.92 at S = 2.0).'),
# M1c Table 7 caption
('The frozen source-derived rule\n  (no injection-label training) matches the trained upper bound; fuel magnitude alone stays at chance.',
 'The frozen source-derived rule (no injection-label training) matches a classifier trained on the same two scores with the injection labels; fuel magnitude alone stays at chance.'),
# M2 intro
('the signature recovers the cause at 95.9% accuracy.',
 'signatures frozen from their source domains recover the cause at 88.6% accuracy (95.9% for a classifier trained on the injected labels), while fuel magnitude alone is at chance.'),
# S1 Table 1 cell
('<td><b>yes (measured, 95.9%)</b></td>','<td><b>yes (measured, 88.6&ndash;95.9%)</b></td>'),
# S2 data availability script range
('scripts/p1_features.py</code> through\n  <code>scripts/p10_consolidated.py</code>',
 'scripts/p1_features.py</code> through\n  <code>scripts/p14_stress_baselines.py</code>'),
# S3 Section 5 model config
('(400 boosting\n  iterations, learning rate 0.05, maximum depth 6; the auxiliary conditions-only and behaviour-only\n  models use 300 iterations and depth 5)',
 '(300 boosting iterations, learning rate 0.05, and maximum depth 5; the headline coefficient of determination is unchanged at 400 iterations and depth 6)'),
# N2 grouped OOF
('excess \\(e_i = y_i - M(x_i)\\).','excess \\(e_i = y_i - M(x_i)\\), grouped out-of-fold.'),
# N3 abstention tau
('Withholding a decision when the two scores are close trades\n  coverage for accuracy:',
 'Withholding a decision when the two scores are close (a margin \\(\\tau\\)) trades coverage for accuracy:'),
# N1 z^A=z^k bridge
('cause A is aggressive driving with a\n  kinematic signature validated on labelled driving (Section 6.3), and cause B is a rich-mixture fault\n  with a fueling/combustion signature validated on the engine bench (Section 7).',
 'cause A is aggressive driving with a kinematic signature validated on labelled driving (Section 6.3), and cause B is a rich-mixture fault with a fueling/combustion signature validated on the engine bench (Section 7); in the notation of Section 4.6, \\(z^A = z^k\\) and \\(z^B = z^c\\).'),
]
miss=[]
for old,new in reps:
    p=rx(old); f=p.findall(h)
    if len(f)!=1: miss.append((len(f),old[:65])); continue
    h=p.sub(lambda m:new,h,count=1)
if miss:
    print("PROBLEMS:")
    for n,s in miss: print(f"  {n}: {s!r}")
    sys.exit(1)
open('index.html','w',encoding='utf-8').write(h); print("applied",len(reps),"edits")
