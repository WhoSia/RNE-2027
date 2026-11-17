from dataclasses import replace
from unittest import TestCase

from d50_turn_pocket import Vehicle
from d51_phase_order import Params, phase, simulate
from timing_bounds import exact


class FinitePocketCalendar(TestCase):
    def test_amber_service_does_not_shift_green_start(self):
        base = Params(left_first=True, intergreen_s=5, service_headway_s=2)
        with_amber = replace(base, amber_service_s=3)
        self.assertEqual([phase(t, base) for t in (10, 11, 12, 14, 16, 17, 18, 19)],
                         ["L", "R", "R", "R", "R", "T", "R", "T"])
        self.assertEqual([phase(t, with_amber) for t in (12, 14, 15, 16, 17)],
                         ["L", "L", "R", "R", "T"])

    def test_refuses_overlap_or_nonpositive_headway(self):
        for options in ({"intergreen_s": 13}, {"intergreen_s": 2, "amber_service_s": 3},
                        {"service_headway_s": 0}):
            with self.subTest(options=options), self.assertRaises(ValueError):
                Params(**options)

    def test_exact_path_and_direct_simulation_agree(self):
        base = Params(through_green_s=3, left_green_s=2, cycle_s=14, horizon_s=100,
                      left_capacity=1, intergreen_s=2, amber_service_s=1, service_headway_s=2)
        schedule = ("L", "L", "T", "", "T")
        arrivals = [Vehicle(arrival_s=i, movement=m, ident=i) for i, m in enumerate(schedule) if m]
        counts = ((2, 2),)
        bound = exact(5, counts, base, observed={t: (m,) for t, m in enumerate(schedule)})
        lag, lead = (simulate(arrivals, replace(base, left_first=flag)) for flag in (False, True))
        self.assertEqual((lag.unserved, lead.unserved), (0, 0))
        delta = round((lead.mean_vehicle_delay_s - lag.mean_vehicle_delay_s) * len(arrivals))
        self.assertEqual((bound.low, bound.high, bound.paths), (delta, delta, 1))

    def test_fixed_late_arrival_reverses_sign_when_amber_service_is_added(self):
        p = Params(horizon_s=130, left_capacity=2, intergreen_s=5)
        observed = {tick: ("L" if tick == 11 else "",) for tick in range(12)}
        tight = exact(12, ((0, 1),), p, observed=observed)
        extended = exact(12, ((0, 1),), replace(p, amber_service_s=3), observed=observed)
        self.assertEqual((tight.low, tight.high), (31, 31))
        self.assertEqual((extended.low, extended.high), (-17, -17))
