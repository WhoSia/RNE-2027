import unittest
from spatial_v10 import Config
from dual_lane_v11 import DualConfig,run

class ServiceEventReconciliationTests(unittest.TestCase):
    def test_denied_events_reconcile_with_counter(self):
        for slots in (1,2,4):
            c=DualConfig(base=Config(duration_s=360,demand_vph=1800),
                through_B_share=.5,receiver_mode="cells",
                receiver_slots=slots,downstream_green_s=15)
            y=run(c,trace=True)
            d=[x for x in y["service_events"] if x["reason"] in
               ("receiver_entry_cell_busy","receiver_capacity_full")]
            self.assertEqual(len(d),y["receiver_full_denied_s"])
    def test_crossed_vehicle_ids_are_unique(self):
        c=DualConfig(base=Config(duration_s=480,seed=9),
            receiver_mode="cells",receiver_slots=4)
        y=run(c,trace=True)
        crossed=[e["vehicle_id"] for e in y["service_events"] if e["reason"]=="stopline_cross"]
        self.assertEqual(len(crossed),len(set(crossed)))
        self.assertEqual(len(crossed),y["exit_S"]+y["exit_L"])
    def test_traces_are_opt_in(self):
        c=DualConfig(base=Config(duration_s=120),receiver_mode="cells",receiver_slots=4)
        self.assertNotIn("service_events",run(c,trace=False))
        self.assertIn("service_events",run(c,trace=True))
    def test_denied_vehicle_does_not_instantly_cross_same_second(self):
        c=DualConfig(base=Config(duration_s=540),receiver_mode="cells",
            receiver_slots=2,downstream_green_s=15)
        y=run(c,trace=True)
        events={}
        for e in y["service_events"]:
            events.setdefault((e["t"],e["vehicle_id"]),set()).add(e["reason"])
        self.assertTrue(all(not ("stopline_cross" in r and
           ("receiver_capacity_full" in r or "receiver_entry_cell_busy" in r))
           for r in events.values()))

if __name__=="__main__":unittest.main(verbosity=2)
