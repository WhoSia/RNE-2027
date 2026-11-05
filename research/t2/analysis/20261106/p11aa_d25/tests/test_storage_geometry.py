import random
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from phase_network import Step, Movement, StorageGeometry, simulate


def one(name, t, zone='A', ticks=4):
    return Movement(name,t,name,'vehicle',(Step((zone,),ticks),))


class TestPhysicalPackingGate(unittest.TestCase):
    def test_two_cars_fit_fifteen_metres(self):
        ds=[one('first',0), one('second',1)]
        geom=StorageGeometry({'A':15000},{'first':4500,'second':4500},2000)
        self.assertEqual(simulate(ds,{'A':2}, storage=geom).starts['second'],1)
    def test_bus_and_car_do_not_fit_fifteen_metres(self):
        ds=[one('bus',0),one('car',1)]
        cap={'A':2}
        geom=StorageGeometry({'A':15000},{'bus':11000,'car':4500},2000)
        self.assertEqual(simulate(ds,cap).starts['car'],1)
        self.assertEqual(simulate(ds,cap,storage=geom).starts['car'],4)
    def test_bus_and_car_fit_seventeen_point_five_metres(self):
        ds=[one('bus',0),one('car',1)]
        geom=StorageGeometry({'A':17500},{'bus':11000,'car':4500},2000)
        self.assertEqual(simulate(ds,{'A':2},storage=geom).starts['car'],1)
    def test_invalid_or_missing_physical_metadata(self):
        ds=[one('a',0)]
        for geom in (StorageGeometry({'A':15000},{},2000),
                     StorageGeometry({'A':15000},{'a':4500},-1),
                     StorageGeometry({'A':15000},{'a':0},2000),
                     StorageGeometry({'A':4000},{'a':4500},2000),
                     StorageGeometry({'B':15000},{'a':4500},2000)):
            with self.subTest(geometry=geom), self.assertRaises(ValueError):
                simulate(ds,{'A':2},storage=geom)
    def test_phase_handoff_with_physical_storage(self):
        ds=[Movement('lead',0,'L','car',(Step(('A',),2),Step(('B',),3))),
            one('follow',1)]
        geom=StorageGeometry({'A':10000,'B':15000},{'lead':8000,'follow':4500},2000)
        z=simulate(ds,{'A':2,'B':1},storage=geom)
        self.assertEqual(z.starts['follow'],2)
        self.assertEqual(z.finishes['lead'],5)
    def test_random_single_zone_matches_independent_packing_oracle(self):
        rng=random.Random(20261106)
        for _ in range(100):
            lengths={str(i):rng.choice([3500,4500,6000,9000,11000]) for i in range(10)}
            ds=[Movement(str(i), i*10, 'common', 'vehicle', (Step(('A',),10000),)) for i in range(10)]
            max_mm= rng.choice([12000,18000,30000,50000])
            geom=StorageGeometry({'A':max_mm},lengths,2000)
            if any(x>max_mm for x in lengths.values()):
                with self.assertRaises(ValueError): simulate(ds,{'A':10},storage=geom)
                continue
            z=simulate(ds,{'A':10},storage=geom)
            # Independent FIFO oracle: event timestamps from arrivals + expiries.
            pending = []
            active = []  # [(departure, identity)]
            expected = {}
            now = 0
            next_arrival = 0
            while len(expected) < 10 or active:
                future = ([ds[next_arrival].arrival] if next_arrival < len(ds) else [])
                future += [exit_time for exit_time, _ in active]
                now = min(future)
                active = [(end, name) for end, name in active if end > now]
                while next_arrival < 10 and ds[next_arrival].arrival == now:
                    pending.append(ds[next_arrival].identity)
                    next_arrival += 1
                while pending:
                    candidate = pending[0]
                    used = sum(lengths[name] for _,name in active)
                    used += 2000 * max(0, len(active)-1)
                    required = lengths[candidate] + (2000 if active else 0)
                    if used + required > max_mm:
                        break
                    pending.pop(0)
                    expected[candidate] = now
                    active.append((now+10000, candidate))
            self.assertEqual(z.starts, expected)


if __name__=='__main__': unittest.main()
