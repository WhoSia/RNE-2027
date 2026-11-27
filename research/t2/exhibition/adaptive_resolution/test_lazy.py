import unittest
from fractions import Fraction as F
from model import Config,Model,witness_belief
from lazy_certificate import select_lazy
from certify import select

class LazyTests(unittest.TestCase):
    def test_skip_evaluation_with_incumbent(self):
        c=Config(erasure=F(1,4),service='random',schedule=(1,2,3,4));b=witness_belief();a,_=select(Model(c),b);x,_=select_lazy(Model(c),b)
        self.assertTrue(x['exact']);self.assertEqual(x['upper'],a['upper']);self.assertEqual(x['evaluations'],1);self.assertEqual(x['selected_depth'],1);self.assertEqual(x['explored_depth'],2);self.assertFalse(x['history'][-1]['evaluated'])
    def test_improve_incumbent_when_needed(self):
        x,_=select_lazy(Model(Config()),witness_belief());self.assertTrue(x['exact']);self.assertEqual(x['selected_depth'],2);self.assertEqual(x['evaluations'],2)
    def test_cap_without_certificate(self):
        x,_=select_lazy(Model(Config()),witness_belief(),max_depth=1);self.assertFalse(x['certified']);self.assertEqual(x['evaluations'],1)
if __name__=='__main__':unittest.main()
