from dataclasses import replace
from random import Random
from unittest import TestCase

from optimize import catalog, oracle_offsets, search
from signal_model import Plan, Scenario, lower_cost, run


class Optimize(TestCase):
    def test_search_matches_independent_matrix(self):
        rng = Random(208)
        plans = tuple(Plan((22, 8, 20, 9), b, o) for b in (False, True) for o in range(0, 50, 7))
        for n in range(6):
            cases = tuple(Scenario(str(i), 90, tuple(sorted((rng.randrange(90), rng.randrange(7))
                          for _ in range(5 + i * 11))), terminal=n * 10) for i in range(4))
            matrix = {p: tuple(run(p, s, fast=False).cost for s in cases) for p in plans}
            for plan, row in matrix.items():
                for s, cost in zip(cases,row):
                    self.assertLessEqual(lower_cost(plan,s), cost)
            offsets = tuple(min(costs) for costs in zip(*matrix.values()))
            self.assertEqual(oracle_offsets(plans, cases)[0], offsets)
            for shifts in ((0,) * len(cases), offsets):
                want = min((max(c - k for c, k in zip(costs, shifts)), p)
                           for p, costs in matrix.items())
                for prune, relax in ((False,False),(True,False),(True,True)):
                    got = search(tuple(reversed(plans)), cases, shifts, prune=prune, relax=relax, first=plans[4])
                    self.assertEqual((got.value, got.plan), want)
                    self.assertEqual(got.evaluations + got.skipped + got.screened, len(plans) * len(cases))

    def test_exact_tie(self):
        plans = tuple(reversed(catalog()[:12]))
        got = search(plans, (Scenario("empty", 3, ()),))
        self.assertEqual((got.value, got.plan), (0, min(plans)))
