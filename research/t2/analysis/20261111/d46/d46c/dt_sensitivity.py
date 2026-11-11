"""Time-step comparison with fixed physical arrival/exit rates.
Synthetic fluid model; not an empirical claim.
"""
import json
from corridor import run

results=[]
for dt in (1.,0.5,0.25,0.125,0.0625):
    n=round(40/dt)
    arr=[];trans=[];dis=[]
    for k in range(n):
        t=k*dt
        arr.append((3.0 if t<25 else 0.)*dt)
        trans.append(4.*dt)
        dis.append((0. if t<10 else 1. if t<30 else 4.)*dt)
    seq=run(arr,trans,dis,6.)
    final=seq[-1].state
    results.append({'dt':dt,'arrival':final.cumul_arrivals,'exit':final.cumul_exits,
        'remaining':final.upstream+final.downstream,
        'peak_upstream':max(z.state.upstream for z in seq),
        'peak_downstream':max(z.state.downstream for z in seq),
        'blocked_physical_duration':sum(z.blocked>1e-9 for z in seq)*dt,
        'first_block_time':next((k*dt for k,z in enumerate(seq) if z.blocked>1e-9),None)})
assert all(abs(z['arrival']-75)<1e-8 for z in results)
assert all(abs(z['arrival']-z['exit']-z['remaining'])<1e-8 for z in results)
open('dt_sensitivity.json','w').write(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
