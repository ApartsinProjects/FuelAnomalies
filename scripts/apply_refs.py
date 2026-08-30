import re,sys
h=open('index.html',encoding='utf-8').read()
def rx(s): return re.compile(r'\s+'.join(re.escape(w) for w in s.split()))
def cite(n): return f'[<a href="#r{n}">{n}</a>]'
reps=[
# 2.1 fuel modelling
('map engine parameters to fuel rate from OBD-II [<a href="#r9">9</a>]. These models predict consumption\n  accurately,',
 'map engine parameters to fuel rate from OBD-II [<a href="#r9">9</a>]. Classic modal-emission models set '
 'the physical baselines ('+cite(27)+' CMEM, '+cite(28)+' MOVES), and recent data-driven fuel models use '
 'smartphone telematics '+cite(29)+', cascaded real-world regression '+cite(30)+', neural drive-cycle '
 'models '+cite(31)+', and behaviour-aware predictors '+cite(32)+'. These models predict consumption accurately,'),
# 2.2 eco-driving / behaviour
('linked to efficiency through drive-cycle simulation\n  [<a href="#r13">13</a>].',
 'linked to efficiency through drive-cycle simulation [<a href="#r13">13</a>]. Large naturalistic-driving '
 'studies (SHRP2 '+cite(33)+'; UDRIVE '+cite(37)+', '+cite(38)+') and a driving-style-recognition survey '
 +cite(36)+' underpin behaviour recognition, eco-driving reviews quantify the fuel impact '+cite(34)+', and '
 'usage-based insurance applies telematics scoring commercially '+cite(35)+'.'),
# 2.3 predictive maintenance
('deep-learning fault diagnosis from driving signals [<a href="#r18">18</a>].',
 'deep-learning fault diagnosis from driving signals [<a href="#r18">18</a>]. Broader predictive-maintenance '
 'research contributes benchmark datasets and methods, including the SCANIA Component X multivariate benchmark '
 +cite(39)+', LSTM remaining-useful-life estimation '+cite(40)+', diesel-engine vibration diagnosis '+cite(43)
 +', and recent surveys '+cite(41)+', '+cite(42)+'.'),
# 2.4 anomaly detection
('isolation forest\n  [<a href="#r19">19</a>], one-class methods, and\n  autoencoder or recurrent models.',
 'isolation forest [<a href="#r19">19</a>], one-class support-vector methods '+cite(44)+', change-point '
 'detection '+cite(45)+', and autoencoder or recurrent models catalogued in recent surveys '+cite(47)+' and '
 'toolkits such as PyOD '+cite(46)+'.'),
# 2.5a SHAP + counterfactual
("Feature-attribution methods such as SHAP [<a href=\"#r23\">23</a>] explain a model's output in terms of\n  its input features.",
 "Feature-attribution methods such as SHAP [<a href=\"#r23\">23</a>] explain a model's output in terms of its "
 "input features, and counterfactual explanations state the minimal input change that would flip a decision "+cite(48)+"."),
# 2.5b weak-supervision framing extended
('a form of weak supervision [<a href="#r25">25</a>]: the',
 'a form of weak supervision [<a href="#r25">25</a>], drawing on transfer learning '+cite(49)+', multi-source '
 'domain adaptation '+cite(50)+', data-programming weak supervision '+cite(51)+', and mixture-of-experts '
 'evidence fusion '+cite(52)+': the'),
]
miss=[]
for old,new in reps:
    p=rx(old); f=p.findall(h)
    if len(f)!=1: miss.append((len(f),old[:60])); continue
    h=p.sub(lambda m:new,h,count=1)
if miss:
    print("PROBLEMS:"); [print(f"  {n}: {s!r}") for n,s in miss]; sys.exit(1)
open('index.html','w',encoding='utf-8').write(h); print("applied",len(reps),"citation edits")
