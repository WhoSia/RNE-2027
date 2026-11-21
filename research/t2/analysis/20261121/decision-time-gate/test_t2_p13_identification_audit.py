"""P13 tests: exact equality, group-dependence and sign thresholds."""
import unittest
from t2_p13_identification_audit import Record, audit, archive_correction_example


def row(name, group, obs, effect, action="abstract_left_pulse"):
    return Record(name, group, obs, effect, action, "synthetic_fixed_fixture")


class StrictSignAuditTests(unittest.TestCase):
    def test_true_alias(self):
        result = audit((row("a","g1",(1,2,3,4,5,6),-10),
                        row("b","g2",(1,2,3,4,5,6),20)))[0]
        self.assertEqual(result["classification"], "STRICT_OPPOSITE_SIGNS_SAME_OBSERVATION")
        self.assertEqual(result["independent_arrival_groups"], 2)
    def test_different_observation_not_alias(self):
        results = audit((row("a","g1",(1,2,3,4,5,6),-10),
                         row("b","g2",(1,2,3,4,5,7),20)))
        self.assertTrue(all(v["classification"].startswith("NOT_STRICTLY") for v in results))
    def test_different_actions_not_alias(self):
        results = audit((row("a","g1",(1,2,3,4,5,6),-10),
                         row("b","g2",(1,2,3,4,5,6),20,"another")))
        self.assertEqual(len(results), 2)
    def test_tie_is_not_strict_opposition(self):
        result = audit((row("a","g1",(0,)*6,0),row("b","g2",(0,)*6,20)))[0]
        self.assertTrue(result["classification"].startswith("NOT_STRICTLY"))
    def test_epsilon_margin(self):
        self.assertTrue(audit((row("a","g1",(0,)*6,-6),
                               row("b","g2",(0,)*6,6)))[0]["classification"].startswith("STRICT"))
        self.assertTrue(audit((row("a","g1",(0,)*6,-5),
                               row("b","g2",(0,)*6,6)))[0]["classification"].startswith("NOT"))
    def test_group_not_row_count(self):
        result = audit((row("a","g1",(0,)*6,-7),
                        row("b","g1",(0,)*6,9),row("c","g1",(0,)*6,11)))[0]
        self.assertEqual(result["world_rows"],3)
        self.assertEqual(result["independent_arrival_groups"],1)
    def test_boolean_observation_rejected(self):
        with self.assertRaises(ValueError):
            row("a","g1",(True,0,0,0,0,0),-8)
    def test_nan_infinite_rejected(self):
        for value in (float("nan"),float("inf"),True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                row("a","g1",(0,)*6,value)
    def test_duplicate_ids_rejected(self):
        with self.assertRaises(ValueError):
            audit((row("a","g1",(0,)*6,-8),row("a","g2",(0,)*6,9)))
    def test_missing_metadata_rejected(self):
        with self.assertRaises(ValueError):
            row("","g1",(0,)*6,-8)
    def test_bad_epsilon_rejected(self):
        for eps in (-1,float("nan"),True):
            with self.subTest(eps=eps), self.assertRaises(ValueError):
                audit((),epsilon=eps)
    def test_archive_no_false_alias(self):
        example=archive_correction_example()
        self.assertFalse(example["six_counts_equal"])
        self.assertEqual(example["archived_delta_pair"],(34,-178))
    def test_empty_audit(self):
        self.assertEqual(audit(()),())


if __name__=="__main__": unittest.main()
