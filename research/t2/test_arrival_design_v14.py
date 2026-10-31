import unittest
from dataclasses import replace
from collections import Counter
from arrival_design_v14 import ArrivalProfile,make_arrivals

class ArrivalDesignTests(unittest.TestCase):
    def test_fractional_period_budgets(self):
        p=ArrivalProfile(duration_s=720,rates_vph=(600,1500,2100,900))
        events=make_arrivals(p)
        expected=sum(p.rates_vph[i%4]*p.period_s for i in range(12))//3600
        self.assertEqual(len(events),expected)
    def test_offset_preserves_total_and_route_mix(self):
        p=ArrivalProfile(left_shares=(.1,.5,.8),seed=9)
        base=make_arrivals(p)
        for offset in (0,15,35,59,60,120):
            changed=make_arrivals(replace(p,arrival_offset_s=offset))
            self.assertEqual(Counter(r for _,r in base),Counter(r for _,r in changed))
            self.assertTrue(all(changed[j][0]<=changed[j+1][0]
                                for j in range(len(changed)-1)))
    def test_repeatable(self):
        p=ArrivalProfile(seed=92)
        self.assertEqual(make_arrivals(p),make_arrivals(p))
    def test_share_changes_with_period(self):
        p=ArrivalProfile(duration_s=240,rates_vph=(1800,),left_shares=(0,1))
        for t,r in make_arrivals(p):
            self.assertEqual(r,'S' if t//60%2==0 else 'L')
    def test_invalid_profiles_rejected(self):
        for update in (dict(duration_s=125),dict(active_s=0),dict(rates_vph=(-3,)),
                       dict(left_shares=(1.1,)),dict(arrival_offset_s=1.5)):
            with self.assertRaises(ValueError):
                make_arrivals(replace(ArrivalProfile(),**update))

if __name__=="__main__":unittest.main(verbosity=2)
