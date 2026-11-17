from unittest import TestCase

from actuated import MAX_GREEN, MIN_GREEN, Observation, Ring
from signal_model import STAGES, Plan, Scenario, run


class Actuated(TestCase):
    def test_clearance_bounds_and_conflicts(self):
        plan = Plan((24,12,20,8), False, 0)
        for congested in (False, True):
            s = Scenario("bounds", 500, ())
            c = Ring(plan, s, "queue")
            output = [c(t, (10 if congested else 0,) * 6, (0,) * 6, 10 if congested else 0)
                      for t in range(s.horizon)]
            self.assertTrue(all(any(set(x) <= set(stage) for stage in STAGES) for x in output))
            for stage, start, end, kind in c.periods:
                self.assertEqual(end-start, (MAX_GREEN if congested else MIN_GREEN)[stage])
                self.assertEqual(output[end:end+plan.clearance], [()] * plan.clearance)
                self.assertEqual(kind, "max" if congested else "gap")

    def test_detection_delay_and_reset(self):
        plan = Plan((24,12,20,8), False, 0)
        s = Scenario("delay", 18, ())
        a = Ring(plan,s,"queue")
        b = Ring(plan,s,"queue",Observation(delay=5))
        for t in range(s.horizon):
            bay = (2 if t >= 9 else 0,0,0,0,0,0)
            a(t,bay,(0,)*6,0)
            b(t,bay,(0,)*6,0)
        self.assertEqual(b.periods[0][2], 10)
        self.assertFalse(a.periods)
        with self.assertRaises(ValueError):
            run(plan,s,fast=True,controller=Ring(plan,s,"queue"))

    def test_receiving_can_gap_while_queue_waits(self):
        p = Plan((24,12,20,8), False, 0)
        s = Scenario("blocked",18,())
        a = Ring(p,s,"queue")
        b = Ring(p,s,"receiving")
        for t in range(18):
            a(t,(2,0,0,0,0,0),s.link,0)
            b(t,(2,0,0,0,0,0),s.link,0)
        self.assertFalse(a.periods)
        self.assertEqual(b.periods[0],(0,0,10,"gap"))

    def test_confirmation_waits_for_second_empty_check(self):
        p = Plan((24,12,20,8),False,0)
        s = Scenario("confirm",18,())
        c = Ring(p,s,"confirmed")
        for t in range(18):
            c(t,(0,)*6,(0,)*6,0)
        self.assertEqual(c.periods[0],(0,0,13,"gap"))

    def test_initial_stage_can_be_varied_without_changing_ring_order(self):
        p = Plan((24,12,20,8),True,0)
        c = Ring(p,Scenario("start",80,()),"queue",start_stage=2)
        for t in range(80):
            c(t,(0,)*6,(0,)*6,0)
        self.assertEqual([s for s,*_ in c.periods[:4]],[2,3,1,0])
