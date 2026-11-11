"""A/B physical bottleneck demonstration: frozen arrival and upstream capacity."""
import csv,json
from corridor import run

n=40
arrivals=[3.0 if i<25 else 0.0 for i in range(n)]
upstream=[4.0]*n
cases={'open_exit': [4.]*n,'downstream_blocked': [0.]*10+[1.]*20+[4.]*10}
rows=[];summary={}
for name,exits in cases.items():
    steps=run(arrivals,upstream,exits,downstream_storage=6.)
    for t,z in enumerate(steps):
        rows.append({'case':name,'step':t,'arrivals':arrivals[t],
                     'transfer':z.transfer,'exit':z.exit_flow,'upstream_queue':z.state.upstream,
                     'downstream_occupancy':z.state.downstream,'blocked':z.blocked,
                     'total_remaining':z.state.upstream+z.state.downstream,
                     'conservation_error':z.end_conservation_error})
    s=steps[-1].state
    summary[name]={'arrivals':s.cumul_arrivals,'exits':s.cumul_exits,
                   'remaining':s.upstream+s.downstream,
                   'max_upstream_queue':max(x.state.upstream for x in steps),
                   'steps_with_blocking':sum(x.blocked>1e-9 for x in steps),
                   'total_blocked_transfer_capacity':sum(x.blocked for x in steps)}
assert summary['open_exit']['arrivals']==summary['downstream_blocked']['arrivals']==75
assert summary['downstream_blocked']['max_upstream_queue']>summary['open_exit']['max_upstream_queue']
assert all(abs(v['arrivals']-v['exits']-v['remaining'])<1e-8 for v in summary.values())
with open('d46c_experiment.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
with open('d46c_experiment.json','w') as f:json.dump(summary,f,indent=2)
print(json.dumps(summary,indent=2))
