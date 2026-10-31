"""Tests for the existing v0.8 model; executed locally before upload."""
import unittest
from dataclasses import replace
from finite_storage_v08 import Setup, run, generated_stream, validate, signal

class FiniteStorageTests(unittest.TestCase):
    def test_storage(self):
        self.assertEqual(validate(Setup(left_length_m=28,through_length_m=56)),(4,8))
        with self.assertRaises(ValueError): validate(Setup(cycle=50))
    def test_protected_schedule(self):
        for leading in (True,False):
            c=Setup(leading=leading)
            vals=[signal(c,t) for t in range(c.cycle)]
            self.assertEqual(vals.count('L'),c.left_green)
            self.assertEqual(vals.count('S'),c.through_green)
    def test_conservation(self):
        for length in (0,14,28,70):
            r=run(Setup(duration=360,left_length_m=length))
            self.assertEqual(r['arrivals'],r['total_exits']+r['remaining'])
            self.assertLessEqual(r['max_L'],r['pocket_slots'])
            self.assertLessEqual(r['max_S'],r['through_slots'])
    def test_all_straight_placebo(self):
        c=Setup(duration=600,left_share=0)
        x=run(replace(c,left_length_m=7))
        y=run(replace(c,left_length_m=70))
        self.assertEqual(x['exits_S'],y['exits_S'])
        self.assertEqual(x['block_L_s'],y['block_L_s'])
    def test_no_left_pocket(self):
        c=Setup(duration=360,left_share=1,left_length_m=0)
        r=run(c)
        self.assertEqual(r['total_exits'],0)
        self.assertEqual(r['remaining'],r['arrivals'])
    def test_paired_determinism(self):
        c=Setup(duration=400)
        s=generated_stream(c)
        self.assertEqual(run(c,s),run(c,s))
    def test_ablated_infinite_pocket(self):
        c=Setup(duration=600,left_share=.6,left_length_m=7)
        a=run(c);b=run(c,pocket_infinite=True)
        self.assertLessEqual(a['max_L'],1)
        self.assertEqual(a['arrivals'],b['arrivals'])
        self.assertEqual(b['block_L_s'],0)

if __name__=='__main__':
    unittest.main(verbosity=2)
