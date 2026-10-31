import unittest
from prospective_court_v06 import (
    EXPLORATION_SEEDS, HOLDOUT_SEEDS, interaction, negative_control_no_left,
    sign_court, validate_split)

class ProspectiveCourtTests(unittest.TestCase):
    def test_split(self):
        validate_split()
        self.assertTrue(set(EXPLORATION_SEEDS).isdisjoint(HOLDOUT_SEEDS))
        with self.assertRaises(ValueError): validate_split((0,1),(1,2))

    def test_interaction(self):
        d={(-21,2):100,(-21,4):120,(-13,2):102,(-13,4):108}
        self.assertEqual(interaction(d),-14)
        with self.assertRaises(ValueError): interaction({(-21,2):1})

    def test_placebo(self):
        p={(-21,2):10,(-21,4):10,(-13,2):12,(-13,4):12}
        self.assertEqual(negative_control_no_left(p).status,'PASS')
        p[-13,4]=13
        self.assertEqual(negative_control_no_left(p).status,'FAIL')

    def test_holdout_refutes_sign(self):
        self.assertEqual(sign_court((-2,-1),(-3,0)).status,'REFUTED')
        self.assertEqual(sign_court((-2,-1),(-3,-4)).status,'PASS_TOY_ONLY')
        self.assertEqual(sign_court((-2,1),(-3,-4)).status,'FAIL')

if __name__ == '__main__': unittest.main()
