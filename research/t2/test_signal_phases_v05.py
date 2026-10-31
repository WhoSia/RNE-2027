"""Run: python -m unittest discover -s research/t2 -p 'test_signal_phases_v05.py' -v."""
import unittest
from signal_phases_v05 import Phase, PhaseConfig, phase_at, greens

class TestProtectedPhaseSchedule(unittest.TestCase):
    def test_lengths_and_no_overlap(self):
        for order in ('leading','lagging'):
            c=PhaseConfig(order=order)
            states=[phase_at(t,c) for t in range(c.cycle)]
            self.assertEqual(states.count(Phase.LEFT),54)
            self.assertEqual(states.count(Phase.THROUGH),60)
            self.assertEqual(states.count(Phase.CLEARANCE),6)
            self.assertEqual(states.count(Phase.RED),30)
            self.assertTrue(all(not (s and l) for s,l in (greens(t,c) for t in range(c.cycle))))
    def test_order(self):
        self.assertEqual(phase_at(0,PhaseConfig(order='leading')),Phase.LEFT)
        self.assertEqual(phase_at(0,PhaseConfig(order='lagging')),Phase.THROUGH)
    def test_periodicity(self):
        c=PhaseConfig()
        self.assertEqual([phase_at(t,c) for t in range(150)],[phase_at(t+150,c) for t in range(150)])
    def test_reject_infeasible(self):
        with self.assertRaises(ValueError):
            PhaseConfig(cycle=110)
    def test_clearance_is_not_green(self):
        c=PhaseConfig(order='leading')
        self.assertEqual(phase_at(54,c),Phase.CLEARANCE)
        self.assertEqual(greens(54,c),(False,False))

if __name__ == '__main__':
    unittest.main()
