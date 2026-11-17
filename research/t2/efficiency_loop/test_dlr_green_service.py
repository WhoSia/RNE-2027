import unittest

from dlr_green_service import count_events


class ServiceWindowTests(unittest.TestCase):
    def test_half_open_and_green_end_clipping(self):
        events = [3.99,4.0,4.5,5.99,6.0]
        self.assertEqual(count_events(events,4,10),3)
        self.assertEqual(count_events(events,4,4.5),1)
        self.assertEqual(count_events(events,4,4),0)
