"""T2 v2.3: model-internal event accounting regression (synthetic only).

This test is intentionally independent of the legacy test_physical_invariants_v22
assertions, but still observes the model's own event stream.
Run locally: python -m unittest research/t2/test_event_accounting_v23.py -v
Do not run GitHub Actions.
"""
import unittest
from collections import Counter
from research.t2.dual_lane_v11 import DualConfig, run
from research.t2.spatial_v10 import Config


class EventAccountingV23(unittest.TestCase):
    def test_event_accounting_by_seed(self):
        for seed in range(8):
            cfg = DualConfig(
                base=Config(duration_s=720, demand_vph=1800,
                            pocket_length_m=14.0, left_fraction=0.5, seed=seed),
                through_B_share=0, allow_lane_changes=True,
                receiver_mode="cells", receiver_slots=4,
            )
            r = run(cfg, trace=True)
            services = r["service_events"]
            denied = [e for e in services if e["reason"] in
                      ("receiver_entry_cell_busy", "receiver_capacity_full")]
            access = [e for e in r["access_events"]
                      if e["event"] == "pocket_entry_denied"]
            with self.subTest(seed=seed):
                self.assertEqual(len(denied), r["receiver_denied_attempts"])
                self.assertEqual(len({e["t"] for e in denied}),
                                 r["receiver_denied_seconds"])
                self.assertEqual(len(access), r["pocket_block_seconds"])
                self.assertTrue(all("blocker_id" in e for e in access))
                self.assertGreaterEqual(r["receiver_denied_attempts"],
                                        r["receiver_denied_seconds"])


if __name__ == "__main__":
    unittest.main()
