import unittest
from trace_factorial_v16 import summarize

class FactorialTraceTests(unittest.TestCase):
    def test_8_matched_seeds_required(self):
        one={"seed":0,"pocket_m":14.,"link_cells":2,"offset_s":0,
             "network_S":10,"network_L":4,"network_total":14,
             "receiver_denied_attempts":3,"pocket_denied_attempts":5,
             "receiver_entry_occupied_frames":7,
             "receiver_and_stopline_frames":2,"fork_signature_frames":1,
             "stopped_vehicle_seconds":8}
        with self.assertRaises(ValueError):summarize([one])
    def test_aggregate_uses_independent_seed_values(self):
        rows=[{"seed":i,"pocket_m":14.,"link_cells":2,"offset_s":0,
                "network_S":i,"network_L":2,"network_total":i+2,
                "receiver_denied_attempts":0,"pocket_denied_attempts":0,
                "receiver_entry_occupied_frames":i,
                "receiver_and_stopline_frames":0,
                "fork_signature_frames":0,"stopped_vehicle_seconds":0}
                for i in range(8)]
        r=summarize(rows)
        self.assertEqual(r[0]["mean_network_S"],3.5)
        self.assertEqual(r[0]["mean_receiver_entry_occupied_frames"],3.5)

if __name__=="__main__":unittest.main()
