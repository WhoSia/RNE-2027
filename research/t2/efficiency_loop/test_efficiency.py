from unittest import TestCase

from efficiency import evaluate
from experiments import generated
from signal_model import Plan, run


class Efficiency(TestCase):
    def test_diagnostics_match_plant(self):
        p = Plan((24,16,20,12),False,0)
        s = generated()[3]
        fixed = evaluate(p,s,"fixed")
        expected = run(p,s)
        self.assertEqual((fixed["cost"], fixed["completed"], fixed["remaining"]),
                         (expected.cost, expected.completed, expected.remaining))
        for policy in ("fixed","queue","receiving"):
            x = evaluate(p,s,policy,trace=True)
            self.assertEqual(x["area"],sum(x["area_by_movement"]))
            self.assertEqual(sum(x["stopline"]),sum(p[0] for p in x["opportunity"].values()))
            self.assertEqual(len(x["trace"]),s.horizon)
        self.assertGreater(sum(p[2] for p in fixed["opportunity"].values()),0)
