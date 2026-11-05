import sys,unittest,random
from pathlib import Path
from dataclasses import replace
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from cell_link_model import Config,simulate

class CTMTests(unittest.TestCase):
    def test_finite_queues_source(self):
        z=simulate(Config())
        self.assertIsNotNone(z['summary']['first_source_blocked_end_s'])
        self.assertGreater(z['summary']['max_source_queue_veh'],0)
    def test_infinite_storage_does_not_block_gate(self):
        z=simulate(Config(infinite_storage_baseline=True))
        self.assertEqual(z['summary']['max_source_queue_veh'],0)
    def test_no_same_tick_cascade(self):
        z=simulate(Config(horizon_s=1))
        self.assertEqual(z['rows'][0]['cells_veh'],[0.5,0,0])
    def test_gate_closed(self):
        z=simulate(Config())
        for r in z['rows']:
            if r['t_end_s']<=12: self.assertEqual(r['cumulative_departed_veh'],0)
    def test_very_low_demand_no_spillback(self):
        z=simulate(Config(arrival_veh_per_s=0.05,downstream_closed_until_s=0))
        self.assertAlmostEqual(z['summary']['max_source_queue_veh'],0)
    def test_conservation_across_timegrid(self):
        for dt in [1.,.5,.25]:
            z=simulate(Config(dt_s=dt))
            self.assertLess(z['summary']['max_conservation_abs_error'],1e-8)
            for r in z['rows']:
                self.assertTrue(all(x>=-1e-9 for x in r['cells_veh']))
                self.assertTrue(all(x<=N+1e-9 for x,N in zip(r['cells_veh'],z['capacities_veh'])))
    def test_invalid_cfl(self):
        with self.assertRaises(ValueError):simulate(Config(dt_s=1.1,horizon_s=22))
    def test_invalid_negative_demand(self):
        with self.assertRaises(ValueError):simulate(Config(arrival_veh_per_s=-.1))
    def test_randomized_conservation(self):
        rng=random.Random(20261105)
        for _ in range(100):
            dt=rng.choice([.25,.5,1.])
            z=simulate(Config(dt_s=dt,arrival_veh_per_s=rng.random()*1.5,
                            downstream_closed_until_s=rng.choice([0,2,4,8,12])))
            self.assertLess(z['summary']['max_conservation_abs_error'],1e-7)
    def test_no_unearned_realworld_claim(self):
        z=simulate(Config())
        self.assertEqual(z['config']['infinite_storage_baseline'],False)
        self.assertNotIn('traffic_signal_optimization',z)
if __name__=='__main__':unittest.main()
