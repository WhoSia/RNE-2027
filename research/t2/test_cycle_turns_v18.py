import unittest
from collections import Counter
from cycle_turns_v18 import arrange_cycle,PROFILES

class CycleInventoryTests(unittest.TestCase):
    def test_same_timestamps_and_turn_counts_every_cycle(self):
        src=tuple((i,"L" if i%5==0 else "S") for i in range(720))
        for profile in PROFILES:
            changed=arrange_cycle(src,profile,17)
            self.assertEqual([t for t,_ in changed],[t for t,_ in src])
            for cycle in range(6):
                self.assertEqual(Counter(r for t,r in src if t//120==cycle),
                                 Counter(r for t,r in changed if t//120==cycle))
    def test_repeatable(self):
        src=tuple((i,"L" if i%3==0 else "S") for i in range(240))
        for profile in PROFILES:
            self.assertEqual(arrange_cycle(src,profile,7),arrange_cycle(src,profile,7))
    def test_reject_invalid_profile(self):
        with self.assertRaises(ValueError):arrange_cycle(((0,"L"),),"invalid",0)

if __name__=="__main__":unittest.main(verbosity=2)
