"""Real-time *simulation-only* phase-policy research prototype.

No street controller is connected, and no phase can bypass its minimum-green,
yellow, or all-red constraints. Sensors and events are synthetic inputs. A physical
intersection requires independent safety review and properly mapped conflicts.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class PhaseGuard:
    min_green_s: float=4.
    max_green_s: float=15.
    yellow_s: float=3.
    all_red_s: float=1.
    def __post_init__(self):
        vs=(self.min_green_s,self.max_green_s,self.yellow_s,self.all_red_s)
        if not all(isfinite(v) for v in vs) or self.min_green_s<=0 or self.max_green_s<self.min_green_s or self.yellow_s<0 or self.all_red_s<0:
            raise ValueError('invalid phase guard')

@dataclass(frozen=True)
class Observation:
    time_s:float
    main_queue:int
    side_queue:int
    main_downstream_free:int
    side_downstream_free:int
    def __post_init__(self):
        if not isfinite(self.time_s) or self.time_s<0 or any(not isinstance(v,int) or v<0 for v in (self.main_queue,self.side_queue,self.main_downstream_free,self.side_downstream_free)):
            raise ValueError('invalid observation')

class PhaseController:
    """Time-stamped finite state machine with a guarded two-phase change.

    Policy: fixed-duration, gap-proxy actuated, or queue-pressure. The observations
    are assumed current and from a trusted simulated detector contract.
    """
    def __init__(self,policy:str,guard:PhaseGuard=PhaseGuard(),fixed_green_s:float=8.):
        if policy not in ('fixed','actuated','pressure'):raise ValueError('unknown policy')
        if not isfinite(fixed_green_s) or not guard.min_green_s<=fixed_green_s<=guard.max_green_s:
            raise ValueError('bad fixed green duration')
        self.policy=policy;self.guard=guard;self.fixed_green_s=fixed_green_s
        self.active='main';self.state='green';self.since=0.;self.last_observation=-1.;self.log=[(0.,'main','green')]
    def pressure(self,obs):
        return (min(obs.main_queue,obs.main_downstream_free),min(obs.side_queue,obs.side_downstream_free))
    def observe(self,obs:Observation):
        if obs.time_s<self.last_observation-1e-9:raise ValueError('backdated observation')
        if obs.time_s<self.since-1e-9:raise ValueError('backdated internal state')
        self.last_observation=obs.time_s
        t=obs.time_s
        # Process mandatory timed transitions at their actual deadlines, not at
        # the next sparse sensor timestamp. This prevents over-long unsafe green.
        for _ in range(20000):
            if self.state=='yellow':
                deadline=self.since+self.guard.yellow_s
                if deadline>t+1e-9:break
                self.since=deadline;self.state='all_red';self.log.append((self.since,self.active,'all_red'));continue
            if self.state=='all_red':
                deadline=self.since+self.guard.all_red_s
                if deadline>t+1e-9:break
                self.since=deadline;self.active='side' if self.active=='main' else 'main'
                self.state='green';self.log.append((self.since,self.active,'green'));continue
            duration=self.fixed_green_s if self.policy=='fixed' else self.guard.max_green_s
            deadline=self.since+duration
            if deadline>t+1e-9:break
            self.since=deadline;self.state='yellow';self.log.append((self.since,self.active,'yellow'))
        else:
            raise ValueError('observation gap too large for deterministic replay')
        if self.state!='green':return self.active,self.state
        elapsed=t-self.since
        if elapsed+1e-9 < self.guard.min_green_s:return self.active,self.state
        current=obs.main_queue if self.active=='main' else obs.side_queue
        other=obs.side_queue if self.active=='main' else obs.main_queue
        p_m,p_s=self.pressure(obs); p_current,p_other=(p_m,p_s) if self.active=='main' else (p_s,p_m)
        if self.policy=='fixed':should_switch=elapsed+1e-9>=self.fixed_green_s
        elif self.policy=='actuated':should_switch=current==0 and other>0
        else:should_switch=p_other>p_current
        should_switch=should_switch or elapsed+1e-9>=self.guard.max_green_s
        if should_switch:
            self.state='yellow';self.since=t;self.log.append((t,self.active,'yellow'))
        return self.active,self.state
