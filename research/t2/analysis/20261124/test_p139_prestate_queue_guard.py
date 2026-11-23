"""P139 pure decision-rule regression tests (no T2 simulation needed).

Run from repository root:
PYTHONPATH=research/t2:research/t2/analysis/20261122:research/t2/analysis/20261123:research/t2/analysis/20261124 python -m unittest research/t2/analysis/20261124/test_p139_prestate_queue_guard.py
"""
import unittest
from p139_prestate_queue_guard import (
    CALENDAR, calendar_choice, guard_choice, cost_regret, summarize
)


class FrozenPolicyTests(unittest.TestCase):
    def setUp(self):
        self.low = dict(outside_A=0, outside_B=0, approach_A=1,
                        approach_B=1, pocket_vehicles=0,
                        receiver_vehicles=2)
        self.high = dict(outside_A=2, outside_B=1, approach_A=1,
                         approach_B=1, pocket_vehicles=1,
                         receiver_vehicles=3)

    def test_calendar_is_frozen(self):
        self.assertEqual(CALENDAR, {
            (0, 30): 60, (15, 0): 30, (7, 15): 60, (23, 45): 30
        })

    def test_guard_changes_only_one_offset(self):
        for off in CALENDAR:
            expected = (30 if off == (7, 15) else CALENDAR[off])
            self.assertEqual(guard_choice(off, self.high), expected)
            self.assertEqual(guard_choice(off, self.low),
                             calendar_choice(off))

    def test_strict_boundary_and_input_immutable(self):
        s = dict(self.high, receiver_vehicles=2)
        self.assertEqual(guard_choice((7, 15), s), 60)
        s = dict(self.high, outside_A=1)
        self.assertEqual(guard_choice((7, 15), s), 60)
        before = dict(self.high)
        self.assertEqual(guard_choice((7, 15), self.high), 30)
        self.assertEqual(self.high, before)

    def test_regret_sign_and_dependent_comparison(self):
        rows = [
            dict(arms={'30':{'cost':100},'60':{'cost':120}},
                 choices={'calendar':60,'guard':30,'fixed30':30,'fixed60':60}),
            dict(arms={'30':{'cost':150},'60':{'cost':90}},
                 choices={'calendar':60,'guard':60,'fixed30':30,'fixed60':60})
        ]
        self.assertEqual(cost_regret(rows[0], 30), 0)
        self.assertEqual(cost_regret(rows[0], 60), 20)
        report = summarize(rows)
        self.assertEqual(report['calendar']['total_regret'], 20)
        self.assertEqual(report['guard']['total_regret'], 0)
        self.assertEqual(report['guard_triggered'], 1)
        self.assertEqual(report['guard_beneficial'], 1)
        self.assertEqual(report['guard_harmful'], 0)


if __name__ == "__main__":
    unittest.main()
