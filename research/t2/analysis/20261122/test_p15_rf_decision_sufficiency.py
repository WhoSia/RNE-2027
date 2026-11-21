"""Tests for artificial RF label / decision sufficiency contract; no RF hardware."""
import unittest
from fractions import Fraction
from p15_rf_decision_sufficiency import World, audit, fixed_fixtures, report_json


class P15Tests(unittest.TestCase):
    def test_three_fixture_groups(self):
        self.assertEqual(len(audit(fixed_fixtures())), 3)

    def test_true_opposition_in_invented_costs(self):
        by = {r['cohort']: r for r in audit(fixed_fixtures())}
        self.assertFalse(by['OPPOSITION']['decision_sufficient_in_enumerated_worlds'])
        self.assertEqual(by['OPPOSITION']['strict_opposition_pairs'], (('o1', 'o2'),))
        self.assertEqual(by['OPPOSITION']['minimax_regret'], '8')
        self.assertEqual(by['OPPOSITION']['minimax_actions'], ('baseline',))

    def test_alias_alone_not_decision_failure(self):
        by = {r['cohort']: r for r in audit(fixed_fixtures())}
        self.assertTrue(by['COMMON']['state_alias'])
        self.assertTrue(by['COMMON']['decision_sufficient_in_enumerated_worlds'])
        self.assertEqual(by['COMMON']['common_optimal_actions'], ('treatment',))
        self.assertEqual(by['COMMON']['minimax_regret'], '0')

    def test_ties_give_common_optimum(self):
        by = {r['cohort']: r for r in audit(fixed_fixtures())}
        self.assertEqual(by['TIE']['common_optimal_actions'], ('baseline',))
        self.assertEqual(by['TIE']['strict_opposition_pairs'], ())

    def test_epsilon_strict_border(self):
        w = (World('a','E','s1','free',1,0,'A',(('baseline',0),('treatment',-5))),
             World('b','E','s2','free',2,0,'A',(('baseline',0),('treatment',6))))
        self.assertFalse(audit(w)[0]['strict_opposition_pairs'])
        self.assertTrue(audit(w, epsilon=Fraction(4))[0]['strict_opposition_pairs'])

    def test_contracts_never_cross(self):
        w = (World('a','E','s1','free',1,0,'A',(('baseline',0),('treatment',-8))),
             World('b','E','s2','free',2,0,'B',(('baseline',0),('treatment',9))))
        self.assertEqual(len(audit(w)),2)
        self.assertFalse(any(r['strict_opposition_pairs'] for r in audit(w)))

    def test_feasible_action_sets_never_cross(self):
        w = (World('a','E','s1','free',1,0,'A',(('baseline',0),('treatment',-8))),
             World('b','E','s2','free',2,0,'A',(('baseline',0),('other',9))))
        self.assertEqual(len(audit(w)),2)

    def test_distinct_group_count(self):
        a,b = fixed_fixtures()[:2]
        b = World('o2', 'OPPOSITION', 'clock1','pocket',4,0,'virtual_same',
                  (('baseline',0),('treatment',9)))
        r = audit((a,b))[0]
        self.assertEqual(r['world_count'],2)
        self.assertEqual(r['independent_arrival_groups'],1)

    def test_duplicate_id_rejected(self):
        a = fixed_fixtures()[0]
        with self.assertRaises(ValueError): audit((a,a))

    def test_bool_cost_rejected(self):
        with self.assertRaises(ValueError):
            World('x','E','s','pocket',1,0,'A',(('baseline',False),('treatment',1)))

    def test_float_cost_rejected(self):
        with self.assertRaises(ValueError):
            World('x','E','s','pocket',1,0,'A',(('baseline',0.),('treatment',1)))

    def test_negative_state_and_bool_rejected(self):
        for n in (-1, True):
            with self.subTest(n=n), self.assertRaises(ValueError):
                World('x','E','s','pocket',n,0,'A',(('baseline',0),('treatment',1)))

    def test_invalid_label_rejected(self):
        with self.assertRaises(ValueError):
            World('x','E','s','camera',1,0,'A',(('baseline',0),('treatment',1)))

    def test_action_order_and_duplicate_rejected(self):
        for costs in ((('treatment',0),('baseline',1)), (('baseline',0),('baseline',1))):
            with self.subTest(costs=costs), self.assertRaises(ValueError):
                World('x','E','s','pocket',1,0,'A',costs)

    def test_fraction_costs_exact(self):
        w = (World('a','E','s1','pocket',1,0,'A',(('baseline',0),('treatment',Fraction(-1,3)))),
             World('b','E','s2','pocket',2,0,'A',(('baseline',0),('treatment',Fraction(1,2)))))
        self.assertEqual(audit(w,epsilon=Fraction(1,4))[0]['minimax_regret'], '1/3')

    def test_three_actions_common_optimum(self):
        w = (World('a','E','s1','pocket',1,0,'A',(('a',0),('b',1),('c',0))),
             World('b','E','s2','pocket',2,0,'A',(('a',0),('b',0),('c',2))))
        self.assertEqual(audit(w)[0]['common_optimal_actions'], ('a',))

    def test_empty_and_determinism(self):
        self.assertEqual(audit(()), ())
        self.assertEqual(report_json(), report_json())

    def test_invalid_epsilon_and_input(self):
        for eps in (-1, True, 0.1):
            with self.subTest(eps=eps), self.assertRaises(ValueError):
                audit((),epsilon=eps)
        with self.assertRaises(TypeError): audit([])


if __name__ == '__main__':
    unittest.main()
