import unittest
from t2_p14_clock_screen import tape_from_slots,simulate,screen,frozen_json,HORIZON
class P14Tests(unittest.TestCase):
    def test_tape(self): self.assertEqual(tape_from_slots((0,0)),(2,0,0,0))
    def test_invalid_slots(self):
        for bad in ((-1,0),(0,4),(0,True),(1,)):
            with self.subTest(bad=bad),self.assertRaises(ValueError): tape_from_slots(bad)
    def test_conservation_all(self):
        from itertools import combinations_with_replacement,product
        slots=list(combinations_with_replacement(range(HORIZON),2))
        for x,y in product(slots,repeat=2):
            a=tape_from_slots(x);b=tape_from_slots(y)
            for p in ('AABB','BBAA'):
                result=simulate(a,b,p)
                self.assertEqual(result['served']+result['lost']+result['terminal'],4)
    def test_equal_tape_same_result(self):
        a=(1,0,1,0);b=(0,1,0,1)
        self.assertEqual(simulate(a,b,'AABB'),simulate(a,b,'AABB'))
    def test_no_negative_counts(self):
        with self.assertRaises(ValueError):simulate((-1,0,0,0),(0,0,0,0),'AABB')
        with self.assertRaises(ValueError):simulate((True,0,0,0),(0,0,0,0),'AABB')
    def test_wrong_policy(self):
        with self.assertRaises(ValueError):simulate((0,)*4,(0,)*4,'other')
    def test_world_count(self):self.assertEqual(screen()['world_count'],100)
    def test_counts_partition(self):
        z=screen();self.assertEqual(z['negative']+z['positive']+z['ties'],100)
    def test_both_signs_exist(self):
        z=screen();self.assertGreater(z['negative'],0);self.assertGreater(z['positive'],0)
    def test_witness(self):
        n,p=screen()['witness'];self.assertLess(n['delta'],0);self.assertGreater(p['delta'],0)
        self.assertNotEqual((n['a'],n['b']),(p['a'],p['b']))
    def test_all_same_total_counts(self):
        for w in screen()['witness']:
            self.assertEqual(len(w['a']),2);self.assertEqual(len(w['b']),2)
    def test_scope(self):self.assertIn('NOT_PHYS',screen()['scope'])
    def test_deterministic_bytes(self):self.assertEqual(frozen_json(),frozen_json())
if __name__=='__main__':unittest.main()
