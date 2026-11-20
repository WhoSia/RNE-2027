from unittest import TestCase

from bypass_windows import WINDOWS, information_scores
from signal_model import Plan, Scenario, run


class BypassWindowTests(TestCase):
    def test_bypass_only_while_eligible(self):
        plan = Plan((6, 6, 6, 6), False, 0)
        scenario = Scenario("test", 6, ((0, 1), (0, 1), (1, 0)),
                            bay=(1, 1, 1, 1, 1, 1), receive_green=36)
        closed = run(plan, scenario)
        self.assertEqual(run(plan, scenario, bypass_depth=1, bypass_ticks=(0,)), closed)
        self.assertEqual(run(plan, scenario, bypass_depth=1, bypass_ticks=()), closed)
        self.assertEqual(run(plan, scenario, bypass_depth=1, bypass_ticks=(1,)).completed[0], 1)
        with self.assertRaises(ValueError):
            run(plan, scenario, bypass_depth=1, bypass_ticks=(6,))

    def test_known_first_tick_does_not_distinguish_early_from_alternating(self):
        arrivals = (0, 0, 0)
        rows = [("early", arrivals, 8), ("alternating", arrivals, -5),
                ("late", arrivals, 20)]
        self.assertEqual(information_scores(rows, WINDOWS), {
            "none": 5, "open_at_decision": 5, "window": 0, "future_arrivals": 5, "both": 0,
        })
