from fractions import Fraction as F
import unittest
from sensor_fusion_decision import Channel, report_support, distribution, extremes, optimize
from finite_sensor_information import worlds, randomized_regret

class SyntheticSensorFusionTests(unittest.TestCase):
    def test_channel_validation(self):
        with self.assertRaises(TypeError): Channel(mode=1)
    def test_support_sizes(self):
        self.assertEqual(tuple(map(len,[report_support(c) for c in
             (Channel(),Channel(mode=True),Channel(arrival=True),Channel(mode=True,arrival=True))])),(1,2,8,16))
    def test_conditional_probabilities_exact(self):
        w=worlds()[0]
        for c in (Channel(),Channel(mode=True),Channel(arrival=True),Channel(mode=True,arrival=True)):
            for m in (F(0),F(1,10),F(1,2),F(1)):
                for a in (F(0),F(3,10),F(1)):
                    self.assertEqual(sum(distribution(w,c,m,a)),1)
        with self.assertRaises(ValueError):distribution(w,Channel(mode=True),F(-1,5),F(0))
    def test_identifiable_and_unidentifiable_worlds(self):
        baseline=optimize(Channel()).worst_regret
        expected=float(randomized_regret(d for m,b,d in worlds()))
        self.assertAlmostEqual(baseline,expected)
        self.assertAlmostEqual(optimize(Channel(mode=True)).worst_regret,float(F(9342,373)))
        self.assertAlmostEqual(optimize(Channel(arrival=True)).worst_regret,baseline)
        self.assertAlmostEqual(optimize(Channel(mode=True,arrival=True)).worst_regret,0)
    def test_information_is_never_harmful_with_zero_cost(self):
        for em,ea in ((F(0),F(0)),(F(1,10),F(1,5)),(F(3,10),F(1,5)),(F(1,2),F(1,2))):
            no=optimize(Channel(),em,ea).worst_regret
            mode=optimize(Channel(mode=True),em,ea).worst_regret
            future=optimize(Channel(arrival=True),em,ea).worst_regret
            fusion=optimize(Channel(mode=True,arrival=True),em,ea).worst_regret
            self.assertLessEqual(mode,no+1e-6)
            self.assertLessEqual(future,no+1e-6)
            self.assertLessEqual(fusion,min(mode,future)+1e-6)
    def test_weakening_error_bounds_cannot_improve_optimal_regret(self):
        results=[optimize(Channel(mode=True,arrival=True),e,e).worst_regret
                 for e in (F(0),F(1,10),F(3,10),F(1,2))]
        self.assertEqual(results,sorted(results))
    def test_error_and_cost_validation(self):
        with self.assertRaises(ValueError):extremes(Channel(mode=True),F(6,5),F(0))
        with self.assertRaises(ValueError):optimize(Channel(),cost=-1)
        x=optimize(Channel(mode=True),F(1,5))
        y=optimize(Channel(mode=True),F(1,5),cost=F(7,2))
        self.assertAlmostEqual(y.worst_regret-x.worst_regret,3.5)
    def test_endpoints_of_error_range_are_audited(self):
        s=optimize(Channel(mode=True,arrival=True),F(1,5),F(3,10))
        self.assertEqual(s.n_worlds,16)
        self.assertEqual(s.n_inequalities,64)
        self.assertEqual(len(s.p_left_by_report),16)
