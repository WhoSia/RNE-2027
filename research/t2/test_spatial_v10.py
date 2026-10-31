import unittest
from dataclasses import replace
from spatial_v10 import Config,validate,phase,arrivals,simulate

class SpatialTests(unittest.TestCase):
    def test_phases(self):
        for order in ("leading","lagging"):
            c=Config(phase_order=order)
            x=[phase(c,t) for t in range(c.cycle_s)]
            self.assertEqual((x.count("L"),x.count("S")),(35,50))
    def test_physical_geometry(self):
        self.assertEqual(validate(Config()),(20,4))
        with self.assertRaises(ValueError):validate(Config(pocket_length_m=140))
    def test_conservation_and_storage(self):
        for length in (0,14,28,42,70):
            y=simulate(Config(duration_s=360,pocket_length_m=length),trace=True)
            self.assertEqual(y["generated"],y["exit_L"]+y["exit_S"]+y["remaining"])
            self.assertLessEqual(y["max_bay_queue"],y["pocket_cells"])
    def test_all_through_placebo(self):
        c=Config(duration_s=480,left_fraction=0)
        a=simulate(replace(c,pocket_length_m=14))
        b=simulate(replace(c,pocket_length_m=70))
        self.assertEqual(a["exit_S"],b["exit_S"])
    def test_zero_pocket_all_left(self):
        self.assertEqual(simulate(Config(duration_s=360,pocket_length_m=0,
                                         left_fraction=1))["exit_L"],0)
    def test_matched_stream(self):
        c=Config(duration_s=480,seed=15)
        s=arrivals(c)
        self.assertEqual(s,arrivals(replace(c,pocket_length_m=70)))
        self.assertEqual(simulate(c,s),simulate(c,s))
    def test_cycle_carryover(self):
        x=simulate(Config(duration_s=360))
        self.assertEqual(len(x["cycles"]),3)
        self.assertEqual(x["cycles"][-1]["exit_L"],x["exit_L"])
    def test_uniform_vs_platoon(self):
        c=Config(duration_s=600)
        a=arrivals(c)
        b=arrivals(replace(c,arrival_pattern="platoon"))
        self.assertEqual(len(a),len(b))
        self.assertNotEqual(a,b)
    def test_no_teleport(self):
        c=Config(duration_s=480,seed=3)
        z=simulate(c,trace=True)
        admitted={}
        for t,event,vid,lane,x in z["events"]:
            if event=="admit":admitted[vid]=t
            if event=="merge":
                self.assertGreaterEqual(t-admitted[vid],z["approach_cells"]-z["pocket_cells"]-1)
            if event=="exit":self.assertGreater(t,admitted[vid])

if __name__=="__main__":
    unittest.main(verbosity=2)
