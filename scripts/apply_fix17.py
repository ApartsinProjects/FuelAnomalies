import re,sys
h=open('index.html',encoding='utf-8').read()
def rx(s): return re.compile(r'\s+'.join(re.escape(w) for w in s.split()))
assert h.count('Table 8')==3 or h.count('Table 8')>=1
h=h.replace('Table 8','Table 7')   # baselines table is now the only high-numbered table
reps=[
# abstract
('signatures learned only in their source domains, frozen and combined on the target without joint supervision, attribute driver-versus-fault excess at 88.6% at the bench-calibrated effect size (a classifier trained on the injected labels reaches an upper bound of 95.9%), while fuel magnitude alone is at chance.',
 'signatures learned only in their source domains, frozen and combined on the target without joint supervision, attribute driver-versus-fault excess at 78.5% at a realistic operating point (rising to about 0.89 when the driver signal matches the fault magnitude), where a matched fuel-only baseline is at chance and negating the frozen weights collapses the result.'),
# contribution 4
('<b>Frozen source-derived signatures</b> learned in separate domains attribute driver-versus-fault\n      excess at 88.6% at a bench-calibrated magnitude (trained upper bound 95.9%) with no joint\n      supervision, where fuel magnitude alone is at chance.',
 '<b>Frozen source-derived signatures</b> learned in separate domains attribute driver-versus-fault\n      excess at 78.5% at a realistic operating point (up to ~0.89 at matched severity) with no joint\n      supervision and a passing falsification control, where a matched fuel-only baseline is at chance.'),
# intro
('signatures frozen from their source domains recover the cause at 88.6% accuracy (95.9% for a classifier trained on the injected labels), while fuel magnitude alone is at chance.',
 'signatures frozen from their source domains recover the cause at 78.5% at a realistic operating point (rising with driver severity), while a matched fuel-only baseline is at chance.'),
# Table 1 cell
('<td><b>yes (measured, 88.6&ndash;95.9%)</b></td>','<td><b>yes (measured, 0.79&ndash;0.93)</b></td>'),
# conclusion
('frozen signatures learned in separate source domains attribute the cause at 88.6% in a calibrated semi-synthetic transfer test (trained upper bound 95.9%), where magnitude alone is at chance.',
 'frozen signatures learned in separate source domains attribute the cause at 78.5% at a realistic operating point (up to ~0.89 at matched severity) in a calibrated semi-synthetic transfer test with a passing falsification control, where a matched fuel-only baseline is at chance.'),
]
miss=[]
for old,new in reps:
    p=rx(old); f=p.findall(h)
    if len(f)!=1: miss.append((len(f),old[:55])); continue
    h=p.sub(lambda m:new,h,count=1)
if miss:
    print("PROBLEMS:"); [print(f"  {n}: {s!r}") for n,s in miss]; sys.exit(1)
open('index.html','w',encoding='utf-8').write(h); print("applied",len(reps),"fixes")
