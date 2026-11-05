import math,random,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from lane_fifo import Demand,simulate
class TimestampAndMeasurementAudit(unittest.TestCase):
    def test_roundoff_collapses_nonzero_duration(self):
        with self.assertRaisesRegex(ValueError,'not representable'):simulate([Demand(1e16,'a','A',('r',),0.25)],{'r':1})
    def test_overflow_to_infinite_exit(self):
        with self.assertRaisesRegex(ValueError,'not representable'):simulate([Demand(1e308,'a','A',('r',),1e308)],{'r':1})
    def test_normal_timestamps_still_strictly_increase(self):
        z=simulate([Demand(1,'a','A',('r',),.25)],{'r':1});self.assertEqual(z.exits['a'],1.25);self.assertGreater(z.exits['a'],z.entries['a'])
    def test_zero_real_wait_not_counted(self):
        self.assertEqual(simulate([Demand(0,'a','A',('r',),1)],{'r':1}).max_waiting['A'],0)
    def test_blocked_vehicle_counts_as_waiting(self):
        z=simulate([Demand(0,'a','A',('r',),2),Demand(.1,'b','A',('r',),1)],{'r':1});self.assertEqual(z.max_waiting['A'],1)
    def test_two_simultaneous_one_slot_one_waits(self):
        z=simulate([Demand(0,'a','A',('r',),2),Demand(0,'b','A',('r',),1)],{'r':1});self.assertEqual(z.max_waiting['A'],1)
    def test_independent_lanes_immediate_admissions(self):
        z=simulate([Demand(0,'a','A',('ra',),1),Demand(0,'b','B',('rb',),1)],{'ra':1,'rb':1});self.assertEqual(z.max_waiting,{'A':0,'B':0})
    def test_preserves_conservation_for_deterministic_random(self):
        rng=random.Random(20261105)
        for _ in range(100):
            ds=[Demand(rng.randrange(0,100)/10,str(i),f'L{i%3}',(f'R{i%3}',),rng.randrange(1,15)/10) for i in range(32)]
            z=simulate(ds,{f'R{k}':2 for k in range(3)})
            self.assertEqual(set(z.entries),set(z.exits));self.assertTrue(all(z.exits[k]>z.entries[k] for k in z.entries))
            self.assertTrue(all(z.entries[d.identity]>=d.at for d in ds));self.assertTrue(all(v<=2 for v in z.max_occupation.values()))
