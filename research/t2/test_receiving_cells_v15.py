import unittest
from receiving_cells_v15 import LinkConfig,ReceivingCells

class LinkTests(unittest.TestCase):
    def test_no_teleport_and_conservation(self):
        x=ReceivingCells(LinkConfig(cells=4,downstream_green_s=60))
        self.assertTrue(x.accept((0,'S',0)))
        for t in range(1,4):
            self.assertIsNone(x.tick(t))
            self.assertEqual(x.snapshot()[0][0],t)
        self.assertEqual(x.tick(4),(0,'S',0))
        self.assertEqual(len(x),0)
    def test_red_stores_vehicles(self):
        x=ReceivingCells(LinkConfig(cells=2,downstream_cycle_s=10,downstream_green_s=0))
        x.accept((0,'L',0))
        for t in range(50):x.tick(t)
        self.assertEqual(len(x),1)
    def test_backpressure(self):
        x=ReceivingCells(LinkConfig(cells=2,downstream_green_s=0))
        x.accept((0,'S',0))
        self.assertFalse(x.accept((1,'L',0)))
        self.assertEqual(x.denied_entries,1)
    def test_offset(self):
        a=ReceivingCells(LinkConfig(downstream_cycle_s=20,downstream_green_s=5,downstream_offset_s=7))
        b=ReceivingCells(LinkConfig(downstream_cycle_s=20,downstream_green_s=5))
        self.assertTrue(all(a.green(t)==b.green(t+7) for t in range(100)))
    def test_invalid_geometry(self):
        with self.assertRaises(ValueError):ReceivingCells(LinkConfig(cells=0))

if __name__=='__main__':unittest.main(verbosity=2)
