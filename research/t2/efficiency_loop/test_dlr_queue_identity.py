import unittest

import pandas as pd

from dlr_queue_identity import STOP_M, presence_label, queue_ids


class QueueIdentityTests(unittest.TestCase):
    def test_preserves_chain_and_breaks_at_long_gap(self):
        rows = pd.DataFrame({
            "tick": [10,10,10,10], "lane": [-3,-3,-3,-4],
            "id": [1,2,3,4], "s": [STOP_M-3,STOP_M-9,STOP_M-35,STOP_M-3],
            "velocity_magnitude": [.5,.8,.1,4], "dimension_length": [4]*4,
        })
        self.assertEqual(queue_ids(rows,1,8), {(10,-3):(1,2)})
        self.assertEqual(queue_ids(rows,.5,8), {(10,-3):(1,)})

    def test_interval_censoring(self):
        self.assertEqual(presence_label(10,10,11),"observed_by_last_green")
        self.assertEqual(presence_label(10.5,10,11),"first_observed_in_transition_bracket")
        self.assertEqual(presence_label(11,10,11),"first_observed_after_green")
