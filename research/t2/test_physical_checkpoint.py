"""PHYS-04 stage A: checkpoint/resume contracts for the existing cellular engine.

Run locally: PYTHONPATH=research/t2 python -m unittest research/t2/test_physical_checkpoint.py
These tests are NOT an empirical calibration or a completed postdecision phase test.
"""
import unittest
from dataclasses import replace
from copy import deepcopy

from dual_lane_v11 import DualConfig, run
from spatial_v10 import Config, arrivals


def config(*, receiver_mode="cells", change_windows=()):
    return DualConfig(
        base=Config(duration_s=240, demand_vph=1800, left_fraction=.5, seed=7,
                    pocket_length_m=28., phase_order="leading"),
        through_B_share=.5, allow_lane_changes=True,
        change_zone_m=70., receiver_mode=receiver_mode, receiver_slots=4,
        lane_change_windows=change_windows,
    )


class CheckpointTests(unittest.TestCase):
    def test_resume_identity_cells_and_fifo_with_and_without_trace(self):
        for mode in ("cells", "fifo"):
            for trace in (False, True):
                with self.subTest(mode=mode, trace=trace):
                    c=config(receiver_mode=mode)
                    tape=arrivals(c.base)
                    direct=run(c, tape, trace=trace)
                    checkpoint=run(c, tape, trace=trace, checkpoint_at=84)
                    self.assertEqual(checkpoint["next_tick"], 84)
                    self.assertEqual(
                        direct, run(c, tape, trace=trace, resume_from=checkpoint)
                    )
                    # Reusing a checkpoint must not mutate the saved snapshot.
                    self.assertEqual(
                        direct, run(c, tape, trace=trace, resume_from=checkpoint)
                    )

    def test_postdecision_window_mutation_preserves_checkpoint(self):
        c=config(change_windows=((0, 240),))
        tape=arrivals(c.base)
        checkpoint=run(c, tape, checkpoint_at=84, trace=True)
        frozen=deepcopy(checkpoint)
        changed=replace(c, lane_change_windows=((0, 84), (120, 240)))
        branched=run(changed, tape, trace=True, resume_from=checkpoint)
        self.assertEqual(checkpoint, frozen)
        self.assertEqual(branched["generated"],
                         branched["network_out_S"]+branched["network_out_L"]+branched["remaining"])
        direct=run(c, tape, trace=True)
        self.assertEqual(direct,run(c, tape, trace=True, resume_from=checkpoint))
        self.assertEqual(direct["frames"][:84], branched["frames"][:84])

    def test_unsafe_phase_switch_rejected(self):
        c=config()
        tape=arrivals(c.base)
        checkpoint=run(c,tape,checkpoint_at=84)
        with self.assertRaisesRegex(ValueError, "clearance-safe"):
            run(replace(c,base=replace(c.base,phase_order="lagging")),
                tape,resume_from=checkpoint)

    def test_different_arrival_tape_rejected(self):
        c=config()
        tape=arrivals(c.base)
        checkpoint=run(c,tape,checkpoint_at=84)
        with self.assertRaisesRegex(ValueError, "arrival tape"):
            run(c,tape[:-1],resume_from=checkpoint)

    def test_change_before_checkpoint_rejected(self):
        c=config(change_windows=((0, 240),))
        tape=arrivals(c.base)
        checkpoint=run(c,tape,checkpoint_at=84)
        changed=replace(c,lane_change_windows=((0, 20),(84,240)))
        with self.assertRaisesRegex(ValueError,"before checkpoint"):
            run(changed,tape,resume_from=checkpoint)


if __name__=="__main__":
    unittest.main()
