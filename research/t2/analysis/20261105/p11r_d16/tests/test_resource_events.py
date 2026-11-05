import unittest
from src.resource_events import Request,run

class ResearchOnlyOccupancyTests(unittest.TestCase):
    def test_one_resource_queue(self):
        q=[Request(0,"a",("link",),1.,"car"),Request(.5,"b",("link",),1.,"car")]
        self.assertEqual(run(q,{"link":1})["entries"],{"a":0,"b":1.})
    def test_crosswalk_conflict(self):
        q=[Request(0,"v",("road",),1.,"car"),Request(.1,"p",("walk",),2.,"ped")]
        z=run(q,{"road":1,"walk":1},{frozenset(("car","ped"))})
        self.assertEqual(z["entries"]["p"],1.)
    def test_exact_release(self):
        q=[Request(0,"a",("link",),1.,"car"),Request(1,"b",("link",),1.,"car")]
        self.assertEqual(run(q,{"link":1})["entries"]["b"],1.)
    def test_preservation(self):
        q=[Request(i*.1,str(i),("link",),1.,"car") for i in range(100)]
        z=run(q,{"link":1})
        self.assertEqual(len(z["entries"]),100)
        self.assertEqual(set(z["entries"]),set(z["exits"]))
        self.assertTrue(all(z["entries"][str(i)]>=q[i].at for i in range(100)))
    def test_duplicate_identity(self):
        q=[Request(0,"a",("link",),1.,"car"),Request(1,"a",("link",),1.,"car")]
        with self.assertRaises(ValueError): run(q,{"link":1})
    def test_invalid_resource(self):
        with self.assertRaises(ValueError): run([Request(0,"a",("unknown",),1.,"car")],{"link":1})
    def test_backward_effect(self):
        q=[Request(47.,"a",("link",),.1625,"car"),Request(47.15,"b",("link",),1.,"car")]
        self.assertAlmostEqual(run(q,{"link":1})["entries"]["b"],47.1625)
if __name__=="__main__":unittest.main()
