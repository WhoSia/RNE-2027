import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from refinement_reference import run,Config
from sensor_court import SensorActuated,run_case,aggregate

class D34(unittest.TestCase):
    def test_refinement(self):
        a=[run(d)['exit_time_s'] for d in [1,.5,.25,.125,.0625]]
        self.assertEqual(len(a),5)
        self.assertLess(abs(a[-1]-a[-2]),abs(a[0]-a[1]))
        self.assertTrue(all(1 < t < 100 for t in a))
    def test_invalid(self):
        for dt in [0,-1,float('inf'),float('nan'),2]:
            with self.assertRaises(ValueError):run(dt)
    def test_zero_overtaking_not_claimed(self):
        self.assertEqual(run(.5)['dt_s'],.5)
    def test_short_road(self):
        with self.assertRaises(ValueError):run(.25,Config(road_m=3))

class D36(unittest.TestCase):
    def test_invalid_sensor(self):
        for d in (-.1,1.1):
            with self.assertRaises(ValueError):SensorActuated(dropout=d)
        with self.assertRaises(ValueError):SensorActuated(delay_steps=2)
    def test_zero_noise_original_observation(self):
        c=SensorActuated(dropout=0,ghost_prob=0,noise_seed=1)
        for t in range(10):c.observe(t,{'A':2,'C':0})
        self.assertEqual(c.sensor_mismatches,0)
    def test_max_dropout(self):
        c=SensorActuated(dropout=1,ghost_prob=0)
        c.observe(0,{'A':5,'C':3})
        self.assertEqual(c.sensor_mismatches,2)
    def test_deterministic(self):
        a=run_case(401,18,3,'actuated',.2,1)
        b=run_case(401,18,3,'actuated',.2,1)
        self.assertEqual(a,b)
    def test_fixed_noise_independence(self):
        a=run_case(401,18,3,'fixed10',0,0)
        self.assertEqual(a['uncompleted'],0)
        self.assertIsNone(a['sensor_mismatch_ticks'])
    def test_censored_policy_report(self):
        res=aggregate([run_case(401,40,1,'actuated',.5,1,horizon=60)])
        self.assertFalse(res[0]['all_complete'])
        self.assertIsNone(res[0]['mean_travel_s'])

if __name__=='__main__':unittest.main()
