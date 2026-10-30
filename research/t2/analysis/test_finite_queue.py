"""Tests for the toy model; NOT validation of the spatial model."""
import unittest
from finite_queue_exhaustive import simulate

class ToyQueueTests(unittest.TestCase):
    def test_empty_green_blocks_all_exits(self):
        self.assertEqual(simulate("LSLS", [0]*4, [0]*4, 1), 0)

    def test_conservation_indirect_via_admissible_exits(self):
        for seq in ("L", "S", "LS", "SLLS", "LSLSLS"):
            for capacity in (1, 2, 4):
                out = simulate(seq, [1]*len(seq), [1]*len(seq), capacity)
                self.assertLessEqual(out, len(seq))
                self.assertGreaterEqual(out, 0)

    def test_simple_monotonic_cases(self):
        examples = ("L", "S", "LLSS", "LSLSLS", "SSLLLLSS")
        for seq in examples:
            for sg in ((1,)*len(seq), (0,)*len(seq)):
                for lg in ((1,)*len(seq), (0,)*len(seq)):
                    self.assertGreaterEqual(simulate(seq, sg, lg, 2),
                                            simulate(seq, sg, lg, 1))

if __name__ == "__main__":
    unittest.main()
