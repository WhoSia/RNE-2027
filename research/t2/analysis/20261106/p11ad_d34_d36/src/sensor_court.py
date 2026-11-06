"""Synthetic sensor error for research-only signal controller, no external actuation."""
from dataclasses import dataclass, field
from random import Random
from statistics import mean
from actuated import Actuated
from micro_world import FixedSignal,run
from od_and_policy import make_od_demand
from policy_audit import ROADS,assess

@dataclass
class SensorActuated(Actuated):
    dropout: float=0.0
    ghost_prob: float=0.0
    delay_steps: int=0
    noise_seed: int=0
    recorded: list=field(default_factory=list)
    sensor_mismatches: int=0
    def __post_init__(self):
        super().__post_init__()
        if not (0<=self.dropout<=1 and 0<=self.ghost_prob<=1) or self.delay_steps not in (0,1):
            raise ValueError('sensor settings out of experiment scope')
        self._rng=Random(self.noise_seed)
    def observe(self,t,counts):
        self.recorded.append(dict(counts))
        old=self.recorded[max(0,t-self.delay_steps)]
        observed={}
        for name in self.approaches:
            seen=sum(self._rng.random()>=self.dropout for _ in range(old[name]))
            seen+=int(self._rng.random()<self.ghost_prob)
            observed[name]=seen
            self.sensor_mismatches+=int(seen!=counts[name])
        super().observe(t,observed)

def run_case(seed:int, demand_n:int, headway:int, mode:str, noise:float=0.0, delay_steps:int=0, horizon:int=260):
    demand=make_od_demand({'east':('A','S'),'north':('C','S')},demand_n,seed,headway_s=headway,bus_every=7)
    signals=None;controller=None
    if mode=='fixed10':
        signals={'A':FixedSignal(24,10,0),'C':FixedSignal(24,10,12)}
    elif mode=='actuated':
        controller=SensorActuated(min_green=6,max_green=15,clearance=2,threshold=2,dropout=noise,ghost_prob=noise/5,delay_steps=delay_steps,noise_seed=seed+991)
    else:raise ValueError('unknown candidate')
    out=run(ROADS,demand,horizon_s=horizon,signals=signals,controller=controller)
    a=assess(demand,out,horizon)
    return {'seed':seed,'n':demand_n,'headway':headway,'mode':mode,'dropout':noise,'delay':delay_steps,'sensor_mismatch_ticks':controller.sensor_mismatches if controller else None,**a}

def aggregate(rows):
    groups={}
    for r in rows: groups.setdefault((r['n'],r['mode'],r['dropout'],r['delay']),[]).append(r)
    result=[]
    for (n,mode,noise,delay),rs in sorted(groups.items()):
        done=all(x['uncompleted']==0 for x in rs)
        result.append({'demand_n':n,'mode':mode,'dropout':noise,'delay':delay,'seeds':len(rs),
                       'all_complete':done,'censored_scenarios':sum(x['uncompleted']>0 for x in rs),
                       'mean_travel_s':mean(x['mean_s'] for x in rs) if done else None,
                       'mean_queue_max':mean(x['queue_max'] for x in rs),
                       'mean_disparity_s':mean(x['disparity_s'] for x in rs) if done else None,
                       'mean_censored_lower_bound_s':mean(x['censored_elapsed_lower_bound_s'] for x in rs)})
    return result
