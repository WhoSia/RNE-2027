"""PHYS-06 regression checks for configurable target-lane clearance.

Default gap=1 is required to preserve PHYS-04 output metrics. A larger gap is
a *synthetic sensitivity parameter*, not a calibrated human gap-acceptance law.
"""
import unittest
from dataclasses import replace

from dual_lane_v11 import DualConfig, run
from spatial_v10 import Config, arrivals
from physical_transfer_screen import score


def case(gap=1):
    base = Config(seed=0, duration_s=240, demand_vph=1800,
                  left_fraction=.5, pocket_length_m=14.)
    return DualConfig(base=base, through_B_share=0.,
                      allow_lane_changes=True, change_zone_m=100.,
                      receiver_slots=4, receiver_mode="cells",
                      lane_change_target_gap_cells=gap)


class TargetClearanceTests(unittest.TestCase):
    def test_default_preserves_precommitted_reference_witness(self):
        c = case()
        self.assertEqual(c.lane_change_target_gap_cells, 1)
        direct = run(c, arrivals(c.base))
        self.assertEqual(score(direct), 14011)
        self.assertEqual(direct["changes_A_to_B"], 34)
        self.assertEqual(direct["network_out_S"], 30)
        self.assertEqual(direct["network_out_L"], 15)
        self.assertEqual(direct["remaining"], 75)

    def test_valid_clearances_checkpoint_and_conservation(self):
        for gap in (1, 2, 3):
            with self.subTest(gap=gap):
                c = case(gap)
                tape = arrivals(c.base)
                checkpoint = run(c, tape, checkpoint_at=84)
                direct = run(c, tape)
                self.assertEqual(direct, run(c, tape, resume_from=checkpoint))
                self.assertEqual(direct["generated"],
                                 direct["network_out_S"] +
                                 direct["network_out_L"] + direct["remaining"])
                self.assertEqual(direct["config"]["lane_change_target_gap_cells"],
                                 gap)
                self.assertGreaterEqual(direct["lane_change_target_gap_denials"], 0)

    def test_gap_changes_are_forbidden_during_resume(self):
        c = case(1)
        tape = arrivals(c.base)
        checkpoint = run(c, tape, checkpoint_at=84)
        with self.assertRaisesRegex(ValueError, "incompatible physical"):
            run(case(2), tape, resume_from=checkpoint)

    def test_invalid_gap_values_fail_closed(self):
        for bad in (0, -1, 20, True, 1.5, "2"):
            with self.subTest(value=bad):
                c = case(bad)
                with self.assertRaisesRegex(ValueError, "target clearance"):
                    run(c, arrivals(c.base))

    def test_explicit_gap_1_is_not_a_new_physical_model(self):
        c = case()
        tape = arrivals(c.base)
        explicit = replace(c, lane_change_target_gap_cells=1)
        self.assertEqual(run(c, tape), run(explicit, tape))


if __name__ == "__main__":
    unittest.main()
