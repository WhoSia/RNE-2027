import unittest
from p18_exploratory_service_witness import witness

class ServiceWitnessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.data=witness()
    def test_expected_cost_order(self):
        self.assertEqual(self.data['paths']['baseline']['score'],11998)
        self.assertEqual(self.data['paths']['left_4s']['score'],11998)
        self.assertEqual(self.data['paths']['left_8s']['score'],12304)
    def test_late_receiver_entry_rejection(self):
        ev=self.data['paths']['left_8s']['left_turn_service_events_tick84_to129']
        self.assertTrue(any(e['tick']==120 and e['reason']=='receiver_entry_cell_busy' for e in ev))
        self.assertTrue(any(e['tick']==121 and e['reason']=='receiver_entry_cell_busy' for e in ev))
    def test_more_early_left_turns(self):
        a=self.data['paths']['left_4s']['left_turn_service_events_tick84_to129']
        b=self.data['paths']['left_8s']['left_turn_service_events_tick84_to129']
        def crossings_at_84_to95(events):return [e['tick'] for e in events if e['reason']=='stopline_cross' and 84<=e['tick']<95]
        self.assertEqual(crossings_at_84_to95(a),[87,89])
        self.assertEqual(crossings_at_84_to95(b),[87,89,91,93])
    def test_same_demand(self):
        self.assertEqual(len({v['generated'] for v in self.data['paths'].values()}),1)
    def test_posthoc_not_field(self):self.assertIn('POSTHOC',self.data['status'])

if __name__=='__main__':unittest.main()
