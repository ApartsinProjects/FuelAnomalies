import re,sys
h=open('index.html',encoding='utf-8').read()
def rx(s): return re.compile(r'\s+'.join(re.escape(w) for w in s.split()))
reps=[
# Title (h1 + <title>)
('Driver or Vehicle? Signature-Based Attribution of Excess Fuel Consumption<br> Using Public Fleet Telemetry and an Engine-Fault Bench',
 'Driver or Vehicle? Multi-Source Signature Attribution of Excess Fuel Consumption<br> Under Missing Joint Cause Labels'),
('<title>Driver or Vehicle? Signature-Based Attribution of Excess Fuel Consumption</title>',
 '<title>Driver or Vehicle? Multi-Source Signature Attribution of Excess Fuel</title>'),
# 95.9% qualifiers
('the signature attributes driver-versus-fault excess at 95.9% accuracy (95% CI [95.6, 96.2]) against a fuel-only baseline at chance.',
 'the signature attributes driver-versus-fault excess at 95.9% accuracy (95% CI [95.6, 96.2]) in a calibrated semi-synthetic test, against a fuel-only baseline at chance.'),
('the signature attributes the cause at 95.9% accuracy where magnitude alone is at chance.',
 'the signature attributes the cause at 95.9% accuracy in a calibrated semi-synthetic evaluation, where magnitude alone is at chance.'),
# Monotonicity relabel (W6)
('The component increases with independently measured aggression: across deciles of harsh-event rate its mean rises from 0.34 to 1.55 L/100km (Figure 3), monotone from the median upward, with a Spearman rank correlation of 0.96 across deciles (\\(p < 10^{-5}\\)).',
 'The component increases across deciles of the harsh-event rate (Figure 3): its mean rises from 0.34 to 1.55 L/100km, monotone from the median upward, with a Spearman rank correlation of 0.96 across deciles (\\(p < 10^{-4}\\)). Because the harsh-event rate is itself an input to the behaviour features, this is an internal face-validity check; the independent validation is the external dataset of Section 6.3.'),
# fueling-correction reframe in 4.4
('The combustion axis is observable in both worlds and placed on a common percent-fuel-per-air scale: in VED as the fuel trims, \\(c^{\\text{VED}} = \\text{STFT}+\\text{LTFT}\\), and on the bench directly from the air-fuel ratio,',
 'On the bench the axis is the air-fuel-ratio deviation directly. In VED the observable is the short- and long-term fuel trims, which are the engine control unit\'s feedback corrections to the base fuel schedule rather than a direct air-fuel-ratio measurement; we therefore treat the VED side as a fueling-correction signal, \\(c^{\\text{VED}} = \\text{STFT}+\\text{LTFT}\\), placed on a common percent-fuel-per-air scale with the bench,'),
]
miss=[]
for old,new in reps:
    p=rx(old); f=p.findall(h)
    if len(f)!=1: miss.append((len(f),old[:70])); continue
    h=p.sub(lambda m:new,h,count=1)
if miss:
    print("PROBLEMS:")
    for n,s in miss: print(f"  {n}: {s!r}")
    sys.exit(1)
open('index.html','w',encoding='utf-8').write(h)
print("applied",len(reps),"edits")
