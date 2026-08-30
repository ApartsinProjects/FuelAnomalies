import re,sys
h=open('index.html',encoding='utf-8').read()
def rx(s): return re.compile(r'\s+'.join(re.escape(w) for w in s.split()))
reps=[
# SHOULD-3 abstract
('with the behaviour axis externally validated on an independent\nlabelled driving dataset.',
 'with the behaviour axis externally validated on two independent labelled driving datasets.'),
# SHOULD-4a intro method sentence
('an independent labelled driving dataset validates the kinematic axis',
 'two independent labelled driving datasets validate the kinematic axis'),
# SHOULD-4b intro evidence chain
('the behaviour axis is validated to transfer to an independent\n  dataset',
 'the behaviour axis is validated to transfer to two independent datasets'),
# SHOULD-5 Figure 1 caption
('an independent dataset validates the behaviour axis',
 'two independent datasets validate the behaviour axis'),
# SHOULD-7 driver population not fleet
('the behaviour axis transfers to a different fleet, twice as many drivers, at the 1 Hz rate OBD\n  telematics actually provide.',
 'the behaviour axis transfers to a different driver population, twice as many drivers, at 1 Hz, the rate OBD telematics actually provide.'),
# NICE-9 drowsy handling
('(172 aggressive, 768 normal), kinematic features computed at 1 Hz separate',
 '(172 aggressive, 768 normal; drowsy windows excluded from the binary contrast), kinematic features computed at 1 Hz separate'),
# MUST-1 stale limitation
('the behaviour-axis\n  transfer is shown for amplitude features across sensing regimes rather than for the exact VED feature\n  set, and a dedicated 1 Hz-versus-high-rate sensitivity analysis is left to future work.',
 'the behaviour-axis transfer is shown on two labelled datasets, at 400 Hz for amplitude features and at the fleet’s own 1 Hz rate for VED-like kinematic features, rather than for the exact VED feature set.'),
# MUST-2a data availability add UAH
('Driving Events (<a href="https://zenodo.org/records/6570972">zenodo.org/records/6570972</a>,\n  CC-BY-4.0).',
 'Driving Events (<a href="https://zenodo.org/records/6570972">zenodo.org/records/6570972</a>, CC-BY-4.0); UAH-DriveSet [<a href="#r26">26</a>] (free for research use; obtained from a public mirror as the original server was unavailable, and not redistributed here).'),
# MUST-2b script range
('<code>scripts/p1_features.py</code> through\n  <code>scripts/p14_stress_baselines.py</code>',
 '<code>scripts/p1_features.py</code> through\n  <code>scripts/p15_uah_e6.py</code>'),
# NICE-8 acknowledgements
('We thank the creators of VED, EngineFaultDB, and the\n  Driving Events dataset for releasing their data openly.',
 'We thank the creators of VED, EngineFaultDB, the Driving Events dataset, and UAH-DriveSet for releasing their data openly.'),
]
miss=[]
for old,new in reps:
    p=rx(old); f=p.findall(h)
    if len(f)!=1: miss.append((len(f),old[:60])); continue
    h=p.sub(lambda m:new,h,count=1)
if miss:
    print("PROBLEMS:")
    for n,s in miss: print(f"  {n}: {s!r}")
    sys.exit(1)
open('index.html','w',encoding='utf-8').write(h); print("applied",len(reps),"edits")
