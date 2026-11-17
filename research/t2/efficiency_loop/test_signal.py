from dataclasses import replace
from random import Random
from unittest import TestCase

from signal_model import Plan, Scenario, calendar, run


class Signal(TestCase):
    def test_random_equivalence_and_abandonment(self):
        rng = Random(17)
        for i in range(110):
            horizon = rng.randrange(15, 160)
            arrivals = tuple(sorted((rng.randrange(horizon), rng.randrange(7))
                                    for _ in range(rng.randrange(100))))
            s = Scenario(str(i), horizon, arrivals,
                         bay=tuple(rng.randrange(1, 6) for _ in range(6)),
                         link=tuple(rng.randrange(1, 6) for _ in range(6)),
                         receive_cycle=rng.randrange(9, 25), receive_green=rng.randrange(1, 8),
                         receive_offset=rng.randrange(15), terminal=rng.randrange(60),
                         headway=tuple(rng.randrange(1, 6) for _ in range(7)),
                         weights=tuple(rng.randrange(1, 4) for _ in range(7)))
            plan = Plan(tuple(rng.randrange(4, 22) for _ in range(4)), bool(i % 2), i % 25)
            slow, fast = run(plan, s, False), run(plan, s, True)
            self.assertEqual(replace(slow, ticks=fast.ticks), fast)
            self.assertEqual(run(plan, s, fast=True, limit=fast.cost), fast)
            if fast.area:
                self.assertIsNone(run(plan, s, fast=True, limit=fast.area - 1))

    def test_boundary_and_storage(self):
        p = Plan((5, 5, 5, 5), False, 0, clearance=1, startup=0)
        s = Scenario("a", 5, ((0, 0), (0, 0), (1, 0)),
                     bay=(1,) * 6, link=(1,) * 6, receive_cycle=9, receive_green=1,
                     receive_offset=4, terminal=10, headway=(1,) * 7)
        self.assertEqual(calendar(p, s.headway)[0], (0, 1, 2, 3, 4))
        result = run(p, s)
        self.assertEqual((result.completed[0], result.remaining[0], result.area, result.cost),
                         (1, 2, 13, 33))

    def test_positive_link_travel_matches_both_engines_and_bound(self):
        from signal_model import lower_cost
        p = Plan((15,9,14,8),False,0)
        base = Scenario("travel",200,((0,0),(1,0),(2,0),(3,0),(3,6)),
                        link=(1,2,2,2,2,2), receive_cycle=8, receive_green=8)
        for duration in (1,3,9,30):
            s = replace(base,travel=(duration,)*6)
            a = run(p,s)
            b = run(p,s,fast=True)
            self.assertEqual(a,replace(b,ticks=a.ticks))
            self.assertLessEqual(lower_cost(p,s),a.cost)
        self.assertGreater(run(p,s).cost,run(p,base).cost)
