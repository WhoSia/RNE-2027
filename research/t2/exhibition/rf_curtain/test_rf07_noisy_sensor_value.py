"""RF07 tests of committed exact artificial Bayesian channel model."""
import unittest
from fractions import Fraction as F
from rf07_noisy_sensor_value import STATES,CHANNELS,cost,likelihood,evaluate,summarize

class TestRF07(unittest.TestCase):
    def test_likelihoods_normalized(self):
        for c in CHANNELS:
            for s in STATES: self.assertEqual(sum(likelihood(c,s).values()),1)
    def test_no_sensors(self):
        self.assertEqual(evaluate()['expected_cost'],0)
        self.assertEqual(evaluate()['oracle_cost'],-1)
        self.assertEqual(evaluate()['regret'],1)
    def test_aggregate(self):
        self.assertEqual(evaluate(('aggregate',))['regret'],F(1,2))
    def test_motion_no_information(self):
        self.assertEqual(evaluate(('motion_only',))['regret'],1)
    def test_noisy_pocket(self):
        self.assertEqual(evaluate(('noisy_pocket',))['regret'],F(1,2))
    def test_downstream_irrelevant(self):
        self.assertEqual(evaluate(('noisy_downstream',))['regret'],1)
    def test_adding_information_ideal_policy(self):
        for c in CHANNELS:
            if c!='aggregate':
                self.assertLessEqual(evaluate(('aggregate',c))['regret'],evaluate(('aggregate',))['regret'])
    def test_nonfree_useless_channel(self):
        self.assertGreater(evaluate(('motion_only',),sensor_fee=F(1,5))['net_cost'],evaluate()['net_cost'])
    def test_sensor_fee_zero(self):
        for c in CHANNELS:
            r=evaluate((c,))
            self.assertEqual(r['expected_cost'],r['net_cost'])
    def test_validation(self):
        with self.assertRaises(ValueError): evaluate(('aggregate','aggregate'))
        with self.assertRaises(ValueError): evaluate(('bad',))
        with self.assertRaises(ValueError): evaluate(sensor_fee=F(-1))
        with self.assertRaises(ValueError): evaluate(prior={s:F(0) for s in STATES})
        with self.assertRaises(ValueError): cost((9,9),'hold')
    def test_asymmetric_prior(self):
        prior={(0,0):F(7,10),(0,1):F(1,10),(1,0):F(1,10),(1,1):F(1,10)}
        self.assertLessEqual(evaluate(('noisy_pocket',),prior=prior)['regret'],evaluate(prior=prior)['regret'])
    def test_status(self):
        self.assertEqual(summarize()['status'],'SYNTHETIC_EXACT_NOT_MEASURED')

if __name__=='__main__': unittest.main()
