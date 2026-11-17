from dataclasses import replace
from itertools import product
from unittest import TestCase

from d50_turn_pocket import Vehicle
from d51_phase_order import Params, simulate
from timing_bounds import ALPHABET, exact, probe, sequence_count


def oracle(path, p):
    vehicles = [Vehicle(i, m, i) for i, m in enumerate(path) if m]
    pair = [simulate(vehicles, replace(p, left_first=flag)) for flag in (False, True)]
    assert not any(r.unserved for r in pair)
    return round(len(vehicles) * ((pair[1].mean_vehicle_delay_s or 0)
                                  - (pair[0].mean_vehicle_delay_s or 0)))


class LatentTiming(TestCase):
    def test_exhaustive_and_witnesses(self):
        p = Params(left_capacity=1, horizon_s=130)
        for bins in (((2, 0), (1, 1), (1, 1)), ((0, 1), (2, 0), (1, 0)),
                     ((1, 1), (0, 0), (1, 1))):
            parts = [tuple(x for x in product(ALPHABET, repeat=3)
                           if x.count("T") == T and x.count("L") == L) for T, L in bins]
            paths = {sum(xs, ()): oracle(sum(xs, ()), p) for xs in product(*parts)}
            for observed in ({}, {0: ("T", "L")}, {3: ("",), 5: ("T",)},
                             {1: ("L",), 2: ("L",)}):
                permitted = {x: d for x, d in paths.items()
                             if all(x[t] in options for t, options in observed.items())}
                result = exact(3, bins, p, observed)
                if not permitted:
                    self.assertIsNone(result)
                    continue
                self.assertEqual((result.low, result.high, result.paths),
                                 (min(permitted.values()), max(permitted.values()), len(permitted)))
                self.assertEqual(permitted[result.low_path], result.low)
                self.assertEqual(permitted[result.high_path], result.high)
            for labeled in (False, True):
                self.assertEqual(probe(3, bins, p, (0, 4), labeled)[1],
                                 sequence_count(3, bins))

    def test_truncated_horizon(self):
        with self.assertRaisesRegex(ValueError, "failed to drain"):
            exact(2, ((1, 0),), Params(horizon_s=2))

    def test_shared_initial_state_union(self):
        p = Params(left_capacity=2, horizon_s=160)
        bins = ((1,1), (2,0), (2,0), (1,1))
        states = (("",0,0), ("",1,0), ("TL",1,1))
        conditional = [exact(3,bins,p,initial=(state,)) for state in states]
        bound = exact(3,bins,p,initial=states)
        self.assertEqual((bound.low, bound.high, bound.paths),
                         (min(b.low for b in conditional), max(b.high for b in conditional),
                          sum(b.paths for b in conditional)))
        self.assertEqual(probe(3,bins,p,(9,10),True,initial=states)[1], bound.paths)

    def test_incomplete_counts_against_independent_oracle(self):
        p = Params(left_capacity=1, horizon_s=130)
        lo, hi = ((1,0),(0,1)), ((2,1),(1,2))
        paths = []
        for path in product(ALPHABET, repeat=6):
            if all(all(a <= part.count(m) <= b for a,b,m in zip(l,h,("T","L")))
                   for l,h,part in zip(lo,hi,(path[:3],path[3:]))):
                paths.append(oracle(path,p))
        bound = exact(3,lo,p,bin_upper=hi)
        self.assertEqual((bound.low,bound.high,bound.paths),(min(paths),max(paths),len(paths)))
