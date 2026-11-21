"""PHYS-08 trace witness regression and interpretation guards."""
import unittest
from physical_checkpoint_trace_witness import REGIMES, WITNESS, experiment


class TraceWitnessTests(unittest.TestCase):
    def test_same_prefix_within_each_demand_regime(self):
        data=experiment()
        self.assertEqual(data['witness_configuration'],WITNESS)
        for label,r in data['regimes'].items():
            self.assertTrue(r['trace']['identical_predecision_frames'])
            a,b=r['trace']['baseline'],r['trace']['intervention']
            self.assertEqual(a['generated'],b['generated'])
            self.assertEqual(a['generated'],a['network_out_S']+a['network_out_L']+a['remaining'])
            self.assertEqual(b['generated'],b['network_out_S']+b['network_out_L']+b['remaining'])

    def test_source_derived_reference_sign_reversal(self):
        data=experiment()['regimes']
        self.assertEqual(data['baseline']['trace']['delta_intervention_minus_baseline'],-281)
        self.assertEqual(data['lowturn']['trace']['delta_intervention_minus_baseline'],781)
        self.assertEqual(data['baseline']['trace']['baseline']['generated'],120)
        self.assertEqual(data['lowturn']['trace']['baseline']['generated'],90)
        self.assertNotEqual(data['baseline']['trace']['decision_observation'],
                            data['lowturn']['trace']['decision_observation'])

    def test_different_regimes_are_not_shared_predecision_state(self):
        self.assertEqual(REGIMES,(('baseline',1800,.5),('lowturn',1350,.3)))
        self.assertNotEqual(REGIMES[0][1:],REGIMES[1][1:])


if __name__=='__main__':
    unittest.main()
