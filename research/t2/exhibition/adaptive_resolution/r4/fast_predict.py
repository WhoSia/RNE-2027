"""Optional R3 exact predictor; Python reference retained unchanged."""
from collections import defaultdict
from fractions import Fraction as F
from math import gcd
from receiving_channel import ChannelModel
from receiving import Model, mass

class PredictMixin:
    def _predict(self,b,a):
        if not b or any(w <= 0 for _, w in b):
            return super()._predict(b,a)
        # Group raw integer weights by free observation before reducing each group.
        groups=defaultdict(dict); v=[0]*7; total=mass(b); den=8*total
        for x,w in b:
            for y,r in self.step(x,a):
                g=groups[self.observe(y,0)]
                g[y]=g.get(y,0)+w
                for i,z in enumerate(r):v[i]+=w*z
        parts=[]; check=0
        for _,g in sorted(groups.items()):
            n=sum(g.values());check+=n
            d=gcd(*g.values())
            parts.append((F(n,den),tuple(sorted((x,w//d) for x,w in g.items()))))
        assert check==den
        return tuple(F(z,den) for z in v),tuple(parts)

class FastModel(PredictMixin,Model):pass
class FastChannelModel(PredictMixin,ChannelModel):pass
