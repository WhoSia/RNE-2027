import unittest

from p37_night_routes import ROUTES, count_routes, stage_counts, time_s


class NightRoutesTest(unittest.TestCase):
    def setUp(self):
        stamp = "2023-09-24T23:30:00+00:00"
        self.candidates = [({"id": "observed", "bracket_end_utc": stamp}, 3),
                           ({"id": "missing", "bracket_end_utc": stamp}, 3)]
        self.start = time_s(stamp)

    def test_missing_vehicle_stays_in_denominator(self):
        detections = {"observed": {zone: [self.start + i]
                                   for i, zone in enumerate(ROUTES[3], 1)}}
        stats = count_routes(self.candidates, detections)[3]
        self.assertEqual(stats["candidates"], 2)
        self.assertEqual(stats["windows_seconds"][10]["expected_only"], 1)
        self.assertEqual(stats["windows_seconds"][10]["neither"], 1)

    def test_receiver_hit_does_not_complete_a_path(self):
        detections = {"observed": {ROUTES[3][-1]: [self.start + 2]}}
        stages = stage_counts(self.candidates, detections)[3]
        self.assertEqual(stages["receiver_only_test"], 1)
        self.assertEqual(stages[ROUTES[3][-1]], 0)

    def test_alternative_path_requires_distinct_later_samples(self):
        connector, receiver = ROUTES[4]
        detections = {"observed": {connector: [self.start + 1], receiver: [self.start + 1]}}
        self.assertEqual(count_routes(self.candidates, detections)[3]["windows_seconds"][40]["neither"], 2)
        detections["observed"][receiver] = [self.start + 2]
        self.assertEqual(count_routes(self.candidates, detections)[3]["windows_seconds"][40]["alternative_only"], 1)
