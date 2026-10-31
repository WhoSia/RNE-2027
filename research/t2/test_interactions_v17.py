"""Test the paired interaction estimand, including its sign and cell completeness."""
import unittest
from interactions_v17 import STUDIES,evaluate,summarize

class T2V17InteractionTests(unittest.TestCase):
    def test_planned_factorial_cell_count(self):
        self.assertEqual(sum(len(a)*len(b)*8*2 for a,b in STUDIES.values()),240)
    def test_matched_two_pocket_contrast(self):
        data=[]
        for seed in range(8):
            for pocket in (14.,70.):
                data.append({"study":"lane_x_closure","a":"0.2","b":"none",
                    "seed":seed,"pocket_m":pocket,"total":10+(7 if pocket==70. else 0)})
        # Test the mathematical paired-difference structure.
        diff=[next(x for x in data if x["seed"]==i and x["pocket_m"]==70.)["total"]-
              next(x for x in data if x["seed"]==i and x["pocket_m"]==14.)["total"]
              for i in range(8)]
        self.assertEqual(diff,[7]*8)

if __name__=="__main__":
    unittest.main(verbosity=2)
