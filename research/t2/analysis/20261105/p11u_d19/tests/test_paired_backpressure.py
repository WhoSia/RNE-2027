import sys
import unittest
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.cell_link_model import Config, simulate
from src.paired_backpressure import compare


class PairedBackpressureTests(unittest.TestCase):
    def test_synthetic_closed_gate_increases_unadmitted_demand(self):
        result, _ = compare(Config())
        self.assertIsNotNone(result.first_excess_source_queue_s)
        self.assertGreater(result.max_excess_source_queue_veh, 0)
        self.assertLess(result.max_flow_conservation_residual, 1e-9)

    def test_open_gate_is_identical_to_itself(self):
        result, rows = compare(Config(downstream_closed_until_s=0))
        self.assertIsNone(result.first_excess_source_queue_s)
        self.assertTrue(all(row['excess_source_queue_veh'] == 0 for row in rows))

    def test_queue_does_not_mean_spillback(self):
        # With the exit open, 1.5 veh/s demand exceeds 1 veh/s saturation.
        c = Config(arrival_veh_per_s=1.5, downstream_closed_until_s=0)
        result, _ = compare(c)
        self.assertEqual(result.first_any_source_queue_s, 1.)
        self.assertIsNone(result.first_excess_source_queue_s)
        self.assertGreater(simulate(c)['summary']['max_source_queue_veh'], 0)

    def test_high_demand_closure_effect_not_conflated_with_demand_queue(self):
        c = Config(arrival_veh_per_s=1.5, downstream_closed_until_s=12)
        result, _ = compare(c)
        self.assertEqual(result.first_any_source_queue_s, 1.)
        self.assertIsNotNone(result.first_excess_source_queue_s)
        self.assertGreater(result.max_excess_source_queue_veh, 0)

    def test_time_resolution_and_conservation(self):
        for dt in (1., 0.5, 0.25, 0.125, 0.0625):
            s, rows = compare(Config(dt_s=dt))
            with self.subTest(dt=dt):
                self.assertEqual(len(rows), round(24 / dt))
                self.assertLess(s.max_flow_conservation_residual, 1e-7)
                self.assertTrue(all(row['departure_deficit_veh'] >= -1e-7 for row in rows))

    def test_invalid_tolerance(self):
        for value in (-0.1, float('nan'), float('inf')):
            with self.subTest(value=value), self.assertRaises(ValueError):
                compare(Config(), tolerance=value)

    def test_data_source_not_modified(self):
        c = Config()
        compare(c)
        self.assertEqual(c.downstream_closed_until_s, 12.)

    def test_mismatched_closed_and_open_only_gate_changed(self):
        c = Config(dt_s=.25, arrival_veh_per_s=.75)
        res, rows = compare(c)
        self.assertEqual(rows[-1]['t_end_s'], 24)
        self.assertLess(res.max_flow_conservation_residual, 1e-8)


if __name__ == '__main__':
    unittest.main()
