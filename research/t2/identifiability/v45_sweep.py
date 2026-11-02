import itertools,csv,json
from v45_feasible_signal import World,POLICIES,simulate,optima
from pathlib import Path
ROOT=Path(__file__).parent
worlds=[World(storage=c,arrivals_main=m,arrivals_side=s) for c,m,s in itertools.product((2,4,8,16),(1,2,3),(0,1,2,3))]
rows=[];twins=[]
for w in worlds:
    op,_=optima(w)
    for split in POLICIES:
        r=simulate(w,split)
        rows.append(dict(storage=w.storage,main=w.arrivals_main,side=w.arrivals_side,split=split,completed=r['completed'],remaining=r['remaining'],blocked=r['blocked'],optimum=int(split in op)))
for a,b in itertools.combinations(worlds,2):
    if a.storage!=b.storage or a.arrivals_main!=b.arrivals_main or a.arrivals_side==b.arrivals_side:continue
    if simulate(a,3)['completed']==simulate(b,3)['completed'] and set(optima(a)[0]).isdisjoint(optima(b)[0]):
        twins.append(dict(a=vars(a),b=vars(b),baseline_exits=simulate(a,3)['completed'],optima_A=optima(a)[0],optima_B=optima(b)[0]))
with (ROOT/'v45_results.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(ROOT/'v45_summary.json').write_text(json.dumps(dict(worlds=len(worlds),runs=len(rows),ambiguous_pairs=len(twins),examples=twins),indent=2))
print(len(worlds),len(rows),len(twins))
