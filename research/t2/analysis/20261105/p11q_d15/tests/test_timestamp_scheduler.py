import unittest, random, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from timestamp_scheduler import execute,intentionally_flawed_tick

class TestCausalEventOrder(unittest.TestCase):
    def test_request_before_release(self):
        t,_=execute(47.15,47.1625)
        self.assertEqual(t,47.1625)
        self.assertLess(intentionally_flawed_tick(47.15,47.1625,0.05),t)
    def test_release_before_request(self):
        self.assertEqual(execute(48,47.1625)[0],48)
    def test_equal_time_release_first(self):
        self.assertEqual(execute(47.1625,47.1625)[0],47.1625)
    def test_randomized(self):
        gen=random.Random(20261105)
        for _ in range(10000):
            q,r=gen.uniform(0,120),gen.uniform(0,120)
            self.assertAlmostEqual(execute(q,r)[0],max(q,r),places=9)
    def test_tick_threshold(self):
        self.assertEqual(intentionally_flawed_tick(47.15,47.1625,0.01),47.1625)
    def test_invalid(self):
        with self.assertRaises(ValueError): execute(-1,1)
        with self.assertRaises(ValueError): execute(1,-1)
        with self.assertRaises(ValueError): intentionally_flawed_tick(1,2,0)
if __name__=="__main__":unittest.main()
