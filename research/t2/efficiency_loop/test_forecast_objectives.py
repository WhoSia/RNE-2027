from unittest import TestCase

from d51_phase_order import Params
from forecast_objectives import evaluate, objective_records
from uncertain_pocket_sensing import by_count


class ForecastObjectives(TestCase):
    def test_objectives_can_choose_opposite_policies(self):
        r = objective_records([(8, 9, ("T",), ()), (7, 1, ("L",), ())])
        self.assertEqual(r["absolute"], [8, 9])
        self.assertEqual(r["regret"], [6, 1])
        self.assertEqual((r["absolute_choice"], r["regret_choice"]), ("lag", "lead"))

    def test_manual_enumeration_matches_dp_for_each_service_calendar(self):
        visible = ((1, 1), (0, 2))
        for amber in (0, 3):
            p = Params(horizon_s=180, left_capacity=2, intergreen_s=5, amber_service_s=amber)
            b, _ = by_count(visible, 6, 2, p)
            r = evaluate(visible, 6, 2, p)
            self.assertEqual(r["worlds"], b.paths)
            self.assertEqual(r["delta_bounds"], [b.low, b.high])
            self.assertEqual(min(r["regret"]), b.regret)
