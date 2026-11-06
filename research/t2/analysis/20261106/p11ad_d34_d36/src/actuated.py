"""Research-only queue-observed two-approach phase switching (not a field controller).
A and C are never both green; transition has a mandatory all-red interval.
Observations include only present-time queue proxy, not future departures.
"""
from dataclasses import dataclass, field

@dataclass
class Actuated:
    approaches: tuple[str,str] = ('A','C')
    min_green: int = 6
    max_green: int = 15
    clearance: int = 2
    threshold: int = 2
    phase: str = 'A'
    elapsed: int = 0
    pending_next: str | None = None
    log: list[tuple[int,str]] = field(default_factory=list)
    last_observed: int = -1

    def __post_init__(self):
        if len(set(self.approaches))!=2 or self.phase not in self.approaches:
            raise ValueError('two distinct approaches required')
        if not (0 < self.min_green <= self.max_green and self.clearance >= 1 and self.threshold >= 0):
            raise ValueError('invalid timing')

    def observe(self,t:int,counts:dict[str,int]):
        if type(t) is not int or t<0 or set(counts)!=set(self.approaches) or any(type(x) is not int or x<0 for x in counts.values()):
            raise ValueError('invalid detector observation')
        if t!=self.last_observed+1:raise ValueError('non-consecutive observation')
        self.last_observed=t
        if t==0:
            self.log.append((0,self.phase));return
        self.elapsed+=1
        if self.phase=='ALL_RED':
            if self.elapsed>=self.clearance:
                self.phase=self.pending_next
                self.pending_next=None
                self.elapsed=0
                self.log.append((t,self.phase))
            return
        other=next(x for x in self.approaches if x!=self.phase)
        if self.elapsed>=self.max_green or (self.elapsed>=self.min_green and counts[other]>0 and (counts[self.phase]==0 or counts[other]>=counts[self.phase]+self.threshold)):
            self.pending_next=other
            self.phase='ALL_RED'
            self.elapsed=0
            self.log.append((t,'ALL_RED'))

    def permits(self, road:str, t:int)->bool:
        return self.phase==road
