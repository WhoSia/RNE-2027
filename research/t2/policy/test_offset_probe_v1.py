import unittest
from dataclasses import replace
from offset_probe_v1 import Config, is_green, periodic_platoons, simulate, offset_sweep, rank_key


class ProbeTests(unittest.TestCase):
    def test_green_wraps_across_cycle(self):
        self.assertTrue(is_green(1, 58, 60, 6))
        self.assertFalse(is_green(5, 58, 60, 6))

    def test_invalid_config_fails(self):
        with self.assertRaises(ValueError):
            Config(green_s=61)
        with self.assertRaises(ValueError):
            Config(downstream_offset_s=60)

    def test_zero_arrivals(self):
        r = simulate((), Config())
        self.assertEqual((r.arrivals, r.completed, r.unserved), (0, 0, 0))
        self.assertIsNone(r.mean_trip_s)

    def test_vehicle_conservation(self):
        arrivals = periodic_platoons()
        for r in offset_sweep(arrivals, Config()):
            self.assertEqual(r.arrivals, r.completed + r.unserved)

    def test_unserved_count_not_censored_out_of_objective(self):
        cfg = Config(horizon_s=20, travel_s=16)
        results = offset_sweep(tuple([0] * 10), cfg)
        self.assertTrue(all(r.unserved > 0 for r in results))
        self.assertEqual(min(results, key=rank_key).unserved, min(r.unserved for r in results))

    def test_platoon_arrival_validation(self):
        with self.assertRaises(ValueError):
            simulate((2, 1), Config())
        with self.assertRaises(ValueError):
            simulate((0, 601), Config())

    def test_offset_can_improve_synthetic_corridor(self):
        results = offset_sweep(periodic_platoons(), Config())
        baseline = results[0]
        best = min(results, key=rank_key)
        self.assertEqual(baseline.unserved, 0)
        self.assertEqual(best.unserved, 0)
        self.assertLess(best.mean_trip_s, baseline.mean_trip_s)

    def test_all_green_offset_independence(self):
        c = Config(cycle_s=10, green_s=10, travel_s=2, horizon_s=80)
        values = offset_sweep((0, 0, 1, 2), c)
        self.assertEqual(len({r.mean_trip_s for r in values}), 1)


if __name__ == '__main__':
    unittest.main()
