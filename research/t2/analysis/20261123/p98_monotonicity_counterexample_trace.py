"""P98: trace all vehicles in the two P97 exceptions to lost-green monotonicity."""
import json
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch
from receiving_cells_v15 import ReceivingCells
from p85_signal_coordination import build_config,p31,run,phases,score
from p88_spatial_audit import aggregate,ZONES
from p89_startup_loss import clock_state

HERE=Path(__file__).resolve().parent
EXCEPTIONS=((85003,.5,'uniform','red',30,2,3),
            (85009,.5,'uniform','green',60,0,1))

def simulate(cfg,tape,cp,period,onset,loss):
    def green(link,t):
        assert t>=84 and not link.config.closure_windows
        return clock_state(t,period,onset,loss)[1]
    with patch.object(ReceivingCells,'green',green):
        r=run(cfg,tape,resume_from=cp,phase_overrides=phases(6,'left_first'),trace=True)
    assert r['remaining']==0
    zones,movement,vehicles=aggregate(r,cp,tape)
    upstream=[(x['t'],x['vehicle_id'],x['movement'],x['lane']) for x in r['service_events'] if x['reason']=='stopline_cross' and x['t']>=84]
    receiver=[]
    prev={a[1]:a[2] for a in cp['state']['receiver'].snapshot()}
    for f in r['frames']:
        if f['t']<84:continue
        curr={a[1]:a[2] for a in f['receiver']}
        for vid in set(prev)-set(curr):receiver.append((f['t'],vid,prev[vid]))
        prev=curr
    return {'cost':score(r,0),'zone':zones,'movement':movement,'vehicles':vehicles,
            'upstream':sorted(upstream),'receiver':receiver,
            'downstream_count':r['network_out_L']+r['network_out_S']}

def first_div(a,b):
    for i in range(max(len(a),len(b))):
        x=a[i] if i<len(a) else None;y=b[i] if i<len(b) else None
        if x!=y:return {'index':i,'loss_old':x,'loss_new':y}

def experiment():
    ref=json.loads((HERE/'P97_RESULT.json').read_text())['rows']
    lookup={(r['seed'],r['share'],r['clock'],r['onset']):r for r in ref}
    rows=[]
    for seed,share,clock,onset,period,old,new in EXCEPTIONS:
        cfg=build_config(seed,900,share,7,4,.5);tape=p31.clock(cfg.base,clock)
        cfg=replace(cfg,base=replace(cfg.base,duration_s=1440),downstream_offset_s=0)
        cp=run(cfg,tape,checkpoint_at=84,trace=True)
        a=simulate(cfg,tape,cp,period,onset,old)
        b=simulate(cfg,tape,cp,period,onset,new)
        reference=lookup[seed,share,clock,onset]['cost_by_period'][str(period)]
        assert (a['cost'],b['cost'])==(reference[old],reference[new])
        zone={z:b['zone'].get(z,0)-a['zone'].get(z,0) for z in ZONES}
        by_move={m:sum(b['movement'][m].get(z,0)-a['movement'][m].get(z,0) for z in ZONES)
                 for m in ('L','S')}
        vids=[]
        for vid,(t,m) in enumerate(tape):
            n=sum(b['vehicles'].get(vid,{}).get(z,0)-a['vehicles'].get(vid,{}).get(z,0)
                  for z in ZONES)
            vids.append({'id':vid,'movement':m,'arrival_s':t,'cost_new_minus_old':n})
        assert sum(zone.values())==sum(by_move.values())==sum(v['cost_new_minus_old'] for v in vids)==b['cost']-a['cost']
        positive=sorted((v for v in vids if v['cost_new_minus_old']>0),key=lambda v:-v['cost_new_minus_old'])
        negative=sorted((v for v in vids if v['cost_new_minus_old']<0),key=lambda v:v['cost_new_minus_old'])
        rows.append(dict(seed=seed,share=share,clock=clock,onset=onset,period=period,
                         loss_old=old,loss_new=new,cost_old=a['cost'],cost_new=b['cost'],
                         delta_new_minus_old=b['cost']-a['cost'],zone_delta=zone,movement_delta=by_move,
                         positive_vehicles=len(positive),negative_vehicles=len(negative),
                         top_positive=positive[:8],top_negative=negative[:8],
                         first_upstream_order_divergence=first_div(a['upstream'],b['upstream']),
                         first_receiver_departure_divergence=first_div(a['receiver'],b['receiver']),
                         first_12_receiver_old=a['receiver'][:12],first_12_receiver_new=b['receiver'][:12]))
    return {'scope':'two preselected exceptions to absolute-cost monotonicity in P97',
            'verification':'source P97 absolute cost + per-zone + per-movement + per-vehicle signed identities match',
            'caution':'observed order differences do not identify a unique causal mechanism without interventions on the conflicting vehicles',
            'rows':rows}

if __name__=='__main__':
    print(json.dumps(experiment(),indent=2))
