from unittest import TestCase

from forecast_information import evaluate, envelope


class ForecastInformationTests(TestCase):
    def test_asymmetric_costs_imply_exact_threshold(self):
        result = evaluate([(0, -27), (1, 109)])
        self.assertEqual(result["strict_improvement_error_ceiling"], "27/109")
        self.assertEqual(result["grid"][0]["regret"], "0")
        self.assertEqual(result["grid"][5]["regret"], "27")

    def test_exact_message_can_still_be_insufficient(self):
        result = evaluate([(0, -27), (0, 109), (1, 60)])
        self.assertIsNone(result["strict_improvement_error_ceiling"])
        self.assertEqual(result["grid"][0]["regret"], "27")

    def test_adversary_may_use_zero_error_in_a_world(self):
        self.assertEqual(envelope([(0, 20)], (1, 0)), [(20, 0)])
