from unittest import TestCase

from offset_information import CYCLE, choose, experiment


class OffsetInformationTest(TestCase):
    def test_regret_conditions_on_only_available_information(self):
        rows = (
            {"id": "one", "x": 0, "costs": (0, 10) + (100,) * (CYCLE - 2)},
            {"id": "two", "x": 1, "costs": (40, 0) + (100,) * (CYCLE - 2)},
        )
        self.assertEqual(choose(rows, (), True), {"one": 1, "two": 1})
        self.assertEqual(choose(rows, ("x",), True), {"one": 0, "two": 1})

    def test_paired_design_and_information_nesting(self):
        report = experiment()
        self.assertEqual(len(report["worlds"]), 24)
        self.assertTrue(all(len(w["costs"]) == CYCLE for w in report["worlds"]))
        s = report["summary"]
        chain = [s[k]["worst_regret_s"] for k in (
            "pooled_minimax_regret", "counts", "counts_storage", "counts_storage_onset")]
        self.assertEqual(chain, sorted(chain, reverse=True))
        self.assertLessEqual(s["pooled_minimax_cost"]["worst_cost_s"],
                             s["pooled_minimax_regret"]["worst_cost_s"])
