"""Finite downstream cellular link for T2.

Cell 0 is immediately downstream of the intersection stopline; increasing
indices travel toward the downstream stopline. One car per cell, at most one
cell per simulated second. The exit is permitted only by a downstream green
and configured minimum time headway. Vehicles are not teleported out of a
receiving link and stopline entry is refused if cell zero is occupied.

One movement step consists of (1) downstream exit, (2) parallel cell moves
based on snapshot occupancy, then (3) upstream stopline admission through
accept(vehicle). This is a deterministic 1D traffic approximation, not
empirically calibrated and not a microscopic car-following model.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class LinkConfig:
    cells:int=4
    downstream_cycle_s:int=60
    downstream_green_s:int=30
    downstream_offset_s:int=0
    exit_headway_s:int=2
    closure_windows:tuple[tuple[int,int],...]=() # absolute time window [start,end), not a bus model

class ReceivingCells:
    def __init__(self, config:LinkConfig):
        if (not isinstance(config.cells,int) or config.cells<1 or
            not isinstance(config.downstream_cycle_s,int) or config.downstream_cycle_s<1 or
            not isinstance(config.downstream_green_s,int) or
            not 0<=config.downstream_green_s<=config.downstream_cycle_s or
            not isinstance(config.downstream_offset_s,int) or
            not isinstance(config.exit_headway_s,int) or config.exit_headway_s<1):
            raise ValueError("invalid receiving link configuration")
        if any(not isinstance(a,int) or not isinstance(b,int) or a<0 or b<=a for a,b in config.closure_windows):
            raise ValueError("invalid exogenous closure interval")
        self.config=config
        self.occupied={}
        self.last_exit=-10**9
        self.exits=[]
        self.denied_entries=0
        self.max_occupied=0

    def green(self,t:int)->bool:
        c=self.config
        if any(a<=t<b for a,b in c.closure_windows):return False
        return (t+c.downstream_offset_s)%c.downstream_cycle_s<c.downstream_green_s

    def tick(self,t:int):
        """Move already-present vehicles. Return the vehicle discharged if any."""
        c=self.config
        finished=None
        last=c.cells-1
        if self.green(t) and last in self.occupied and t-self.last_exit>=c.exit_headway_s:
            finished=self.occupied.pop(last)
            self.last_exit=t
            self.exits.append((t,finished[0],finished[1]))
        snapshot=set(self.occupied)
        for i in range(last-1,-1,-1):
            if i in snapshot and i+1 not in snapshot:
                self.occupied[i+1]=self.occupied.pop(i)
        self._audit()
        return finished

    def accept(self,vehicle)->bool:
        """Vehicle tuple (ID, movement, arrival_second)."""
        if 0 in self.occupied:
            self.denied_entries+=1
            return False
        self.occupied[0]=vehicle
        self._audit()
        return True

    def _audit(self):
        if any(not 0<=i<self.config.cells for i in self.occupied):
            raise AssertionError("receiving road coordinate invalid")
        ids=[v[0] for v in self.occupied.values()]
        if len(ids)!=len(set(ids)):
            raise AssertionError("duplicate receiving road vehicle")
        self.max_occupied=max(self.max_occupied,len(self.occupied))

    def snapshot(self):
        return tuple((i,v[0],v[1]) for i,v in sorted(self.occupied.items()))

    def __len__(self):
        return len(self.occupied)
