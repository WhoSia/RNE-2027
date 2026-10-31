import unittest
from dataclasses import replace
from spatial_v10 import Config,phase,validate
from dual_lane_v11 import DualConfig,run
from arrival_design_v14 import ArrivalProfile,make_arrivals
from temporal_factorial_v14 import summarize

class TemporalTests(unittest.TestCase):
    def test_phase_rotation(self):
        base=Config()
        for t in range(120):
            self.assertEqual(phase(replace(base,signal_offset_s=30),t),phase(base,t+30))
    def test_invalid_offset_type(self):
        with self.assertRaises(ValueError):validate(Config(signal_offset_s=1.2))
    def test_same_arrivals_across_interventions(self):
        stream=make_arrivals(ArrivalProfile(duration_s=240,seed=7,arrival_offset_s=30))
        base=Config(duration_s=240,seed=7)
        for pocket in (14.,70.):
            z=run(DualConfig(base=replace(base,pocket_length_m=pocket),
                receiver_slots=2,receiver_headway_s=4),stream)
            self.assertEqual(z['generated'],z['network_out_S']+z['network_out_L']+z['remaining'])
    def test_missing_seed_cells_rejected(self):
        with self.assertRaises(AssertionError):
            summarize([{'rate':'steady','turn':'steady','arrival_offset':0,
             'signal_offset':0,'pocket_m':14,'network_S':3,'network_L':2,
             'network_total':5,'outside':0}])

if __name__=='__main__':unittest.main(verbosity=2)
