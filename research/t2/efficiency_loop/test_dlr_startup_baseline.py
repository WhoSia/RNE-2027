from unittest import TestCase

from dlr_startup_baseline import loss, paired_difference


class StartupIntervals(TestCase):
    def test_interval_and_coupled_error(self):
        self.assertEqual(loss(3,(2,4)),(0,1))
        self.assertEqual(loss(1,(2,4)),(1,3))
        self.assertEqual(paired_difference(2,4,(1,5)),(-2,2))
        self.assertEqual(paired_difference(2,4,(5,6)),(2,2))
        self.assertEqual(paired_difference(3,3,(1,5)),(0,0))


class PositionIntervals(TestCase):
    def test_phase_uses_one_clock_for_all_vehicles(self):
        from dlr_startup_position import phase_loss_bounds

        self.assertEqual(phase_loss_bounds([(0, 2, (0, 2)), (2, 0, (0, 2))]), (0, 0))
        self.assertEqual(phase_loss_bounds([(0, 2, (0, 2))]), (-2, 2))
        with self.assertRaises(ValueError):
            phase_loss_bounds([(0, 2, (0, 2)), (2, 0, (0, 3))])
