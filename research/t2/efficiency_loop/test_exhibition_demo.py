from unittest import TestCase

from exhibition_demo import example, query_report


class ExhibitionDemoTests(TestCase):
    def test_tree_ends_at_a_weakly_optimal_order_for_every_case(self):
        data = example()
        for penalty, record in query_report(data).items():
            depths = []
            for row in data["cases"]:
                node = record["tree"]
                visited = set()
                while "question" in node:
                    question = node["question"]
                    self.assertNotIn(question, visited)
                    visited.add(question)
                    node = node["branches"][row["order"][question]]
                depths.append(len(visited))
                delta = row["area"] + penalty * row["remaining"]
                self.assertTrue(delta <= 0 if node["order"] == "left" else delta >= 0)
            self.assertEqual(record["tree"]["depth"], max(depths))
            self.assertEqual(record["tree"]["total"], sum(depths))

    def test_three_cost_assumptions_change_how_much_must_be_known(self):
        report = query_report(example())
        self.assertEqual([report[p]["tree"]["depth"] for p in (0, 60, 120)], [2, 3, 0])
        self.assertEqual(report[60]["mean_questions_equal_weight"], "7/4")
