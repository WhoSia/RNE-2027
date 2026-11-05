"""Loss-aware regulatory overlay for a lane-level RoadIR.

All permissions require an explicit declaration; an unresolved movement is not
approved. This is a data-model research artifact, not a road legal opinion or an
operational controller. Local time zones must be provided by a caller.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, time
from math import isfinite
from zoneinfo import ZoneInfo
from road_ir import RoadIR

VEHICLES = frozenset({'passenger','bus','hgv','bicycle','emergency','pedestrian','motorcycle'})
DAY_NAMES = frozenset(range(7))

@dataclass(frozen=True)
class Window:
    """Local recurring weekday window, half-open, including overnight windows.

    start == end means full-day; days represent the weekday on which the
    window begins (not necessarily the weekday of the time being evaluated).
    """
    start_minute:int
    end_minute:int
    weekdays:frozenset[int]=frozenset(range(7))
    def __post_init__(self):
        if not (0 <= self.start_minute < 1440 and 0 <= self.end_minute < 1440):
            raise ValueError('time minute out of bounds')
        if not self.weekdays or not self.weekdays <= DAY_NAMES:raise ValueError('bad weekday set')
    def active(self, local:datetime)->bool:
        if local.tzinfo is None:raise ValueError('timezone-aware instant required')
        wd=local.weekday();now=local.hour*60+local.minute
        if self.start_minute == self.end_minute:return wd in self.weekdays
        if self.start_minute < self.end_minute:
            return wd in self.weekdays and self.start_minute <= now < self.end_minute
        return (wd in self.weekdays and now >= self.start_minute) or ((wd-1)%7 in self.weekdays and now < self.end_minute)

@dataclass(frozen=True)
class Rule:
    connection_id:str
    vehicle:str
    effect:str                 # 'allow' or 'deny'; no implicit other mode permission
    source_id:str              # documented evidence for this rule
    window:Window|None=None
    def __post_init__(self):
        if not self.connection_id or self.vehicle not in VEHICLES or self.effect not in ('allow','deny') or not self.source_id:
            raise ValueError('invalid rule')

@dataclass(frozen=True)
class Decision:
    status:str                 # ALLOW, DENY, UNKNOWN
    evidence:tuple[str,...]
    reason:str

class RoadRules:
    """Explicit per-connection regulatory assertions.

    Unknown is intentionally distinct from DENY. A DENY wins over any ALLOW;
    contradictory overlapping grants do not silently become legal. A caller
    may NOT treat UNKNOWN as permission for simulation.
    """
    def __init__(self,net:RoadIR,rules:tuple[Rule,...],tz_name:str):
        self.net=net
        self.tz=ZoneInfo(tz_name)
        known={c.id for c in net.connections}
        if any(r.connection_id not in known for r in rules):raise ValueError('rule references absent lane connection')
        self.rules=tuple(rules)
    def evaluate(self,connection_id:str,vehicle:str,instant:datetime)->Decision:
        if connection_id not in {c.id for c in self.net.connections}:raise KeyError('unknown connection')
        if vehicle not in VEHICLES:raise ValueError('unsupported vehicle class')
        if instant.tzinfo is None:raise ValueError('naive timestamp not allowed')
        local=instant.astimezone(self.tz)
        match=[r for r in self.rules if r.connection_id==connection_id and r.vehicle==vehicle and (r.window is None or r.window.active(local))]
        denied=tuple(sorted({r.source_id for r in match if r.effect=='deny'}))
        if denied:return Decision('DENY',denied,'explicit prohibition')
        allowed=tuple(sorted({r.source_id for r in match if r.effect=='allow'}))
        if allowed:return Decision('ALLOW',allowed,'explicit permission in this overlay')
        return Decision('UNKNOWN',(), 'insufficient regulatory evidence')
    def verified_route(self,lanes:tuple[str,...],vehicle:str,instant:datetime)->tuple[Decision,...]:
        if not lanes:raise ValueError('empty route')
        if len(lanes)==1:return ()
        decisions=[]
        for a,b in zip(lanes,lanes[1:]):
            options=[c for c in self.net.connections if c.source==a and c.destination==b]
            if not options:raise ValueError('broken physical route')
            # Parallel turn connections must be disambiguated; an ALLOW on one
            # cannot certify the others with the same lane end points.
            if len(options)!=1:raise ValueError('ambiguous parallel connections')
            decisions.append(self.evaluate(options[0].id,vehicle,instant))
        return tuple(decisions)

@dataclass(frozen=True)
class Limitation:
    component:str
    field:str
    reason:str
    evidence:str
    def __post_init__(self):
        if not all((self.component,self.field,self.reason,self.evidence)):
            raise ValueError('complete limitation evidence required')

def readiness(net:RoadIR, rules:RoadRules, vehicle:str,instant:datetime)->dict:
    """Completeness audit, not proof of traffic safety."""
    decisions={c.id:rules.evaluate(c.id,vehicle,instant).status for c in net.connections}
    return {'connections':len(decisions),'allowed':sum(v=='ALLOW' for v in decisions.values()),
            'denied':sum(v=='DENY' for v in decisions.values()),
            'unknown':sum(v=='UNKNOWN' for v in decisions.values()),
            'unresolved_importer_facts':list(net.unresolved),'research_only':True}
