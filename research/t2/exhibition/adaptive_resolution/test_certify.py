import unittest
from fractions import Fraction as F
from model import Config,Model,witness_belief
from certify import select

class CertificateTests(unittest.TestCase):
 def test_first_only_needs_depth2(self):
    x,_=select(Model(Config()),witness_belief());self.assertEqual(x['selected_depth'],2);self.assertTrue(x['exact'])
 def test_cap_is_not_certificate(self):
    x,_=select(Model(Config()),witness_belief(),1);self.assertFalse(x['certified']);self.assertGreater(F(x['gap']),0)
 def test_epsilon_is_not_exactness(self):
    x,_=select(Model(Config()),witness_belief(),1,F(1));self.assertTrue(x['certified']);self.assertFalse(x['exact'])
 def test_invalid_cap(self):
    with self.assertRaises(ValueError):select(Model(Config()),witness_belief(),0)
if __name__=='__main__':unittest.main()
