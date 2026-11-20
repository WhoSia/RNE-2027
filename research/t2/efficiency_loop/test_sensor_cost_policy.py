from fractions import Fraction as F
import unittest
from sensor_cost_policy import Source,available,pick

class TimeAndCostTests(unittest.TestCase):
    def construct(self,key,*,is_forecast=False,issued_at=80,reported_at=81,target_at=83,
                  error=F(1,10),cost=1,provenance_ok=True):
        return Source(key,is_forecast,issued_at,reported_at,target_at,F(error),F(cost),provenance_ok)
    def test_late_report_unavailable(self):
        mode=self.construct('structure',reported_at=85)
        self.assertFalse(available(mode,84))
        self.assertTrue(available(mode,86))
    def test_realized_future_is_not_usable(self):
        a=self.construct('arrival',target_at=88,is_forecast=False)
        f=self.construct('arrival',target_at=88,is_forecast=True)
        self.assertFalse(available(a,84))
        self.assertTrue(available(f,84))
    def test_future_issued_not_available_and_provenance(self):
        a=self.construct('arrival',is_forecast=True,issued_at=85,reported_at=85,target_at=100)
        self.assertFalse(available(a,84))
        self.assertFalse(available(self.construct('arrival',provenance_ok=False),84))
    def test_untrusted_or_late_report_cannot_drive_choice(self):
        a=self.construct('structure',reported_at=90)
        chosen=pick([a],84,100)
        self.assertEqual(chosen['sources'],())
    def test_budget_prevents_acquisition(self):
        a=self.construct('structure',cost=20)
        self.assertEqual(pick([a],84,19)['sources'],())
        self.assertEqual(pick([a],84,21)['sources'],('structure',))
    def test_unhelpful_source_is_ignored(self):
        a=self.construct('arrival',is_forecast=True,error=0,cost=1,target_at=88)
        self.assertEqual(pick([a],84,30)['sources'],())
    def test_selects_mode_over_fusion_at_high_mode_error(self):
        a=self.construct('structure',error=F(1,10))
        b=self.construct('arrival',is_forecast=True,target_at=88,error=F(1,10))
        self.assertEqual(pick([a,b],84,100)['sources'],('structure',))
    def test_selects_fusion_when_mode_is_very_reliable(self):
        a=self.construct('structure',error=F(1,100))
        b=self.construct('arrival',is_forecast=True,target_at=88,error=F(1,10))
        self.assertEqual(pick([a,b],84,100)['sources'],('structure','arrival'))
    def test_validation(self):
        with self.assertRaises(ValueError):self.construct('else')
        with self.assertRaises(ValueError):self.construct('structure',issued_at=90,reported_at=80)
        with self.assertRaises(ValueError):pick([],84,-1)
