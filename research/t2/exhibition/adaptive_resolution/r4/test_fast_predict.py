import unittest
from fractions import Fraction as F
from receiving import initial,Model
from receiving_channel import ChannelModel
from fast_predict import FastModel,FastChannelModel
class TestFastPredict(unittest.TestCase):
    def test_models(self):
        b=initial((2,2),'0001')
        for old,new in [(Model(False),FastModel(False)),(Model(True),FastModel(True)),(ChannelModel(F(1,4)),FastChannelModel(F(1,4)))]:
            for a in (0,1):
                self.assertEqual(old.predict(b,a),new.predict(b,a))
                self.assertEqual(old.predict(tuple((x,w*7) for x,w in b),a),new.predict(tuple((x,w*7) for x,w in b),a))
    def test_malformed(self):
        old,new=ChannelModel(),FastChannelModel()
        b=initial((2,2),'0001')
        for bad in [(),((b[0][0],-1),),((b[0][0],0),)]:
            for model in (old,new):
                with self.assertRaises(ZeroDivisionError if not bad or bad[0][1]==0 else ValueError):model.predict(bad,0)
        with self.assertRaises(ValueError):new.predict(b,2)
if __name__=='__main__':unittest.main()
