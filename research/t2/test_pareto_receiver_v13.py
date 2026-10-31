import unittest
from pareto_receiver_v13 import nondominated,assess

class ParetoTests(unittest.TestCase):
    def test_tradeoff_retains_two_strategies(self):
        a=[{"pocket_m":14,"mean_network_S":90,"mean_network_L":20},
           {"pocket_m":28,"mean_network_S":85,"mean_network_L":30}]
        self.assertEqual(len(nondominated(a)),2)
    def test_remove_dominated_option(self):
        a=[{"pocket_m":14,"mean_network_S":90,"mean_network_L":20},
           {"pocket_m":28,"mean_network_S":85,"mean_network_L":18}]
        self.assertEqual([r["pocket_m"] for r in nondominated(a)],[14])
    def test_reject_missing_final_network_counter(self):
        with self.assertRaises(ValueError):nondominated([{"pocket_m":14}])
    def test_incomplete_factorial_rejected(self):
        with self.assertRaises(ValueError):
            assess([{"turn_share":.3,"receiver_slots":2,"receiver_headway_s":4,
                     "B_share":.5,"pocket_m":14,"mean_network_S":10,
                     "mean_network_L":10}])

if __name__=="__main__":
    unittest.main(verbosity=2)
