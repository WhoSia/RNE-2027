import unittest
from dataclasses import replace
from world_contact_v09 import Params,check,green,demand,run

class WorldContactTests(unittest.TestCase):
    def test_geometry(self):
        self.assertEqual(check(Params()),(4,8,12))
        with self.assertRaises(ValueError): check(Params(cycle_s=40))
    def test_phase(self):
        for mode in ("leading","lagging"):
            c=Params(phase_order=mode)
            phases=[green(c,t) for t in range(c.cycle_s)]
            self.assertEqual((phases.count("L"),phases.count("S")),(35,50))
    def test_all_conserved(self):
        for seed in range(5):
            for policy in ("fifo","bypass"):
                c=Params(horizon_s=480,seed=seed,feeder_policy=policy)
                y=run(c)
                self.assertEqual(y["generated"],y["exits_L"]+y["exits_S"]+y["remaining"])
                self.assertGreaterEqual(y["generated"],y["admitted"])
                self.assertEqual(y["generated"]-y["admitted"],y["still_outside"])
    def test_paired_arrivals(self):
        c=Params(horizon_s=300,seed=7)
        a=demand(c)
        self.assertEqual(a,demand(replace(c,bay_length_m=70,feeder_policy="bypass")))
    def test_no_left_placebo(self):
        c=Params(horizon_s=540,turn_share=0)
        a=demand(c)
        x=run(replace(c,bay_length_m=7),a)
        y=run(replace(c,bay_length_m=70),a)
        self.assertEqual(x["exits_S"],y["exits_S"])
        self.assertEqual(x["blocked_L_seconds"],0)
    def test_platoon_and_uniform_have_different_schedule(self):
        c=Params(horizon_s=600)
        u=demand(c)
        p=demand(replace(c,arrival_pattern="platoon"))
        self.assertEqual(len(u),len(p))
        self.assertNotEqual(tuple(t for t,_ in u),tuple(t for t,_ in p))
    def test_reproducible_events(self):
        c=Params(horizon_s=480)
        self.assertEqual(run(c),run(c))
        for t,vid,r in run(c)["stopline_events"]:
            self.assertIn(r,("L","S"))
            self.assertGreaterEqual(t,0)
    def test_no_pocket_100pct_left(self):
        c=Params(horizon_s=240,bay_length_m=0,turn_share=1)
        y=run(c)
        self.assertEqual(y["exits_L"],0)
    def test_input_validation(self):
        c=Params(horizon_s=60,arrival_rate_vph=0)
        with self.assertRaises(ValueError): run(c,((9,"S"),(2,"L")))
        with self.assertRaises(ValueError): run(c,((0,"X"),))
    def test_storage_per_cycle(self):
        c=Params(horizon_s=360)
        y=run(c)
        self.assertEqual(len(y["cycle_history"]),3)
        self.assertTrue(all(z["bay"]<=y["storage_slots"]["bay"] for z in y["cycle_history"]))

if __name__=="__main__":
    unittest.main(verbosity=2)


class LimitedLookaheadTests(unittest.TestCase):
    def test_window_one_is_fifo(self):
        c=Params(horizon_s=600)
        for length in (14,28,70):
            a=run(replace(c,bay_length_m=length,feeder_policy="fifo"))
            b=run(replace(c,bay_length_m=length,feeder_policy="window",bypass_window=1))
            self.assertEqual(a["exits_S"],b["exits_S"])
            self.assertEqual(b["bypassed_head_vehicles"],0)
    def test_bounded_and_deterministic(self):
        c=Params(horizon_s=600,feeder_policy="window",bypass_window=3)
        a=run(c);b=run(c)
        self.assertEqual(a,b)
        self.assertGreater(a["bypassed_head_vehicles"],0)
    def test_large_window_matches_unbounded(self):
        c=Params(horizon_s=600)
        stream=demand(c)
        a=run(replace(c,feeder_policy="bypass"),stream)
        b=run(replace(c,feeder_policy="window",bypass_window=1000),stream)
        self.assertEqual(a["exits_S"],b["exits_S"])
        self.assertEqual(a["exits_L"],b["exits_L"])

class SignalOpportunityTests(unittest.TestCase):
    def test_signature_subset_of_empty_green(self):
        for length in (0,14,28,70):
            for turn_share in (0.0,0.3,1.0):
                c=Params(horizon_s=360,bay_length_m=length,turn_share=turn_share)
                y=run(c)
                self.assertLessEqual(y["straight_green_L_head_block_signature_s"],
                                     y["straight_green_empty_start_s"])
    def test_no_left_signature_in_all_through(self):
        c=Params(horizon_s=600,turn_share=0)
        y=run(c)
        self.assertEqual(y["straight_green_L_head_block_signature_s"],0)
