from unittest import TestCase

from field_replay import metrics, predict, slots


class Replay(TestCase):
    def test_intervals_and_unserved(self):
        green = ((121.2, 122.2, 124.2, 125.2),)
        self.assertEqual(slots(green, "narrow", 0, 1), [245, 246, 247, 248])
        self.assertEqual(slots(green, "wide", 0, 2), [243, 245, 247, 249])
        vehicles = ((121,123), (121,123.5), (130,135))
        outcome = predict(vehicles, [246,247], 2)
        self.assertEqual(outcome, [(121,123,123), (121,123.5,123.5), (130,135,None)])
        self.assertEqual(metrics(outcome,green)["penalized_absolute_sum"], 180)
