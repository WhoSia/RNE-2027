"""Independent event-driven oracle for P92 tick-simulation output.

Unlike p92_exposure_negative_control.py, this computes an explicit departure
timestamp for each vehicle, then integrates delay as sum(exit-arrival).
Usage: python test_p92_independent_oracle.py
"""
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
START, STOP = 84, 684


def oracle(arrivals, cycle):
    exits = []
    last = -10**9
    for arrival in sorted(arrivals):
        t = max(arrival, last + 2)
        while not 2 <= (t - START) % cycle < cycle // 2:
            t += 1
        if t >= STOP:
            raise AssertionError("unfinished arrival")
        exits.append(t)
        last = t
    return {"departures": len(exits),
            "queue_vehicle_seconds": sum(t-a for t, a in zip(exits, sorted(arrivals))),
            "last_exit_second": exits[-1] if exits else None}


class IndependentP92(unittest.TestCase):
    def test_archived_rows_against_event_oracle(self):
        archive = json.loads((HERE / "P92_RESULT.json").read_text())
        cases = {
            "empty": [],
            "sparse": [START+10+60*i for i in range(5)],
            "single_initial_platoon_80": [START]*80,
            "uniform_90": [START+2*i for i in range(90)],
        }
        self.assertEqual(len(archive["rows"]), len(cases))
        for row in archive["rows"]:
            demand = row["demand"]
            self.assertIn(demand, cases)
            arrivals = cases[demand]
            self.assertEqual(row["generated"], len(arrivals))
            for period in (30, 60):
                with self.subTest(demand=demand, period=period):
                    actual = row["outcomes"][str(period)]
                    expected = oracle(arrivals, period)
                    for key, value in expected.items():
                        self.assertEqual(actual[key], value)
                    self.assertEqual(actual["remaining"], 0)
                    self.assertEqual(actual["nominal_green_seconds"], 300)
                    self.assertEqual(actual["service_eligible_seconds"], 260 if period == 30 else 280)

    def test_zero_demand_is_not_capacity_loss(self):
        empty = oracle([], 30), oracle([], 60)
        self.assertEqual(empty[0]["queue_vehicle_seconds"], 0)
        self.assertEqual(empty[0], empty[1])


if __name__ == "__main__":
    unittest.main()
