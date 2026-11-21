"""P12 contract tests: invented ticks, no real signal/controller connection."""
import unittest

from t2_p12_phase_contract import (
    Stage, Contract, check_plan, duration_ticks, illustrative_four_tick_case,
)


def contract(green=6, yellow=2, red=1, cyclic=False):
    return Contract(
        {"through": green, "left": green},
        yellow, red,
        frozenset({"through", "left"}), cyclic=cyclic,
    )


class PhaseContractTests(unittest.TestCase):
    def test_four_tick_rejected(self):
        self.assertIn("stage_1:green_below_contract_minimum",
                      check_plan((Stage("left", 4, 0, 0),), contract()))
    def test_four_tick_not_universally_forbidden(self):
        self.assertEqual(check_plan((Stage("left", 4, 0, 0),), contract(green=4)), ())
    def test_transition_clearance_required(self):
        errors = check_plan((Stage("through", 8, 0, 0), Stage("left", 8, 0, 0)), contract())
        self.assertIn("stage_0:missing_yellow_change", errors)
        self.assertIn("stage_0:missing_red_clearance", errors)
    def test_clearance_pass(self):
        self.assertEqual(check_plan((Stage("through", 8, 2, 1),
                                     Stage("left", 8, 0, 0)), contract()), ())
    def test_cyclic_last_to_first(self):
        seq = (Stage("through", 8, 2, 1), Stage("left", 8, 0, 0))
        self.assertEqual(check_plan(seq, contract()), ())
        self.assertIn("stage_1:missing_red_clearance",
                      check_plan(seq, contract(cyclic=True)))
    def test_pedestrian_clearance(self):
        self.assertIn("stage_0:pedestrian_clearance_exceeds_green_plus_yellow",
                      check_plan((Stage("left", 8, 0, 0, 9),), contract()))
    def test_pedestrian_without_green(self):
        errors = check_plan((Stage("left", 0, 2, 1, 1),), contract(green=0))
        self.assertIn("stage_0:pedestrian_clearance_without_green", errors)
    def test_unknown_movement(self):
        self.assertIn("stage_0:unknown_movement",
                      check_plan((Stage("wrong", 8, 2, 1),), contract()))
    def test_empty_plan(self):
        self.assertEqual(check_plan((), contract()), ("empty_plan",))
    def test_non_integer_and_bool_rejected(self):
        for value in (True, False, -1, 2.0, "4"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                Stage("left", value, 0, 0)
    def test_invalid_contract(self):
        with self.assertRaises(ValueError):
            Contract({"left": True}, 0, 0, frozenset({"left"}))
        with self.assertRaises(ValueError):
            Contract({"left": 2}, 0, 0, frozenset({"left", "through"}))
    def test_illustrative_legacy_case(self):
        data = illustrative_four_tick_case()
        self.assertGreater(len(data["violations"]), 0)
        self.assertEqual(data["duration_ticks"], 12)
        self.assertEqual(data["status"], "ILLUSTRATIVE_SIMULATION_CONTRACT_NOT_REGULATORY")
    def test_duplicate_adjacent_rejected(self):
        result = check_plan((Stage("left", 8, 0, 0),
                             Stage("left", 8, 0, 0)), contract())
        self.assertIn("stage_0:duplicate_adjacent_movement", result)

    def test_single_stage_cyclic_not_duplicate(self):
        self.assertEqual(check_plan((Stage("left", 8, 0, 0),),
                                    contract(cyclic=True)), ())

    def test_duration_no_overlap(self):
        self.assertEqual(duration_ticks((Stage("through", 8, 2, 1),
                                         Stage("left", 8, 2, 1))), 22)


if __name__ == "__main__":
    unittest.main()
