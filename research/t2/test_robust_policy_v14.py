import unittest
from robust_policy_v14 import evaluate

class RobustScreenTests(unittest.TestCase):
    def test_average_and_worst_are_computed_separately(self):
        data=[{'pocket_m':28.,'signal_offset':0,
               'mean_total':100+i,'mean_network_S':60,'mean_network_L':40+i}
              for i in range(8)]
        x=evaluate(data)[0]
        self.assertEqual(x['min_total_across_contexts'],100)
        self.assertEqual(x['mean_total_across_contexts'],103.5)
    def test_reject_incomplete_contexts(self):
        with self.assertRaises(ValueError):
            evaluate([{'pocket_m':14.,'signal_offset':0}])

if __name__=='__main__':unittest.main(verbosity=2)
