"""Movement-separated downstream receiving links for T2 (P129 structural falsifier).

The legacy T2 engine sends left-turning (L) and through (S) vehicles into ONE
finite cellular receiver. Physically, the two movements usually enter different
downstream links. This wrapper holds one independent ReceivingCells per movement,
each with the same cell count, exit headway and signal clock as the legacy link
unless configured otherwise. It is used only when DualConfig.receiver_split=True;
the default (shared) path of dual_lane_v11 is unchanged and remains the
regression baseline.
"""
from receiving_cells_v15 import ReceivingCells, LinkConfig

MOVEMENTS = ("S", "L")


class SplitReceivingCells:
    def __init__(self, through: LinkConfig, left: LinkConfig):
        self.parts = {"S": ReceivingCells(through), "L": ReceivingCells(left)}

    def part(self, movement):
        return self.parts[movement]

    def tick_all(self, t):
        """Advance both links; return the vehicles discharged this tick (S first, then L)."""
        out = []
        for m in MOVEMENTS:
            v = self.parts[m].tick(t)
            if v is not None:
                out.append(v)
        return out

    @property
    def occupied(self):
        return {(m, i): v for m in MOVEMENTS for i, v in self.parts[m].occupied.items()}

    @property
    def denied_entries(self):
        return sum(p.denied_entries for p in self.parts.values())

    def snapshot(self):
        return tuple((m, i, vid, mv) for m in MOVEMENTS for i, vid, mv in self.parts[m].snapshot())

    def __len__(self):
        return sum(len(p) for p in self.parts.values())
