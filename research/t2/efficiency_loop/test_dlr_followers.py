from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from dlr_followers import Approach, green_clock, review, route_after, runs


class FollowerEvidence(TestCase):
    def test_posthoc_route_requires_order_and_unique_movement(self):
        east_left = {"left_connector": range(10,15), "south_exit": range(15,20)}
        self.assertEqual(route_after(0,east_left),"left")
        self.assertEqual(route_after(12,east_left),"unknown")
        self.assertEqual(route_after(0,east_left | {
            "through_connector":range(11,16),"west_receiving":range(16,21)}),"unknown")

    def test_unsampled_bins_break_runs(self):
        self.assertEqual(runs([1,2,4,5,6]),[(1,2),(4,6)])

    def test_signal_transition_and_unknown_stay_unresolved(self):
        with TemporaryDirectory() as d:
            path = Path(d)/"signal.csv"
            path.write_text("timestamp,id,state\n"
                            "2023-09-24T12:30:00+00:00,3,3\n"
                            "2023-09-24T12:30:01+00:00,3,5\n"
                            "2023-09-24T12:30:02+00:00,3,5\n"
                            "2023-09-24T12:30:03+00:00,3,0\n")
            clock = green_clock(path)
            self.assertEqual([clock(t) for t in (10,20,30,50)],["unknown","unknown","green","unknown"])

    def test_known_follower_cannot_bypass_unclassified_intermediate_track(self):
        tracks = [Approach(0,"f",-3,90,.5),Approach(0,"middle",-3,96,.5),Approach(0,"l",-3,102,.5)]
        routes = {"f":{"through_connector":range(10,15),"west_receiving":range(15,20)},
                  "l":{"left_connector":range(10,15),"south_exit":range(15,20)}}
        result = review(tracks,routes,lambda _: "green")
        self.assertEqual(result["slow_left_ahead_of_through"]["green"]["pairs"],0)
        self.assertEqual(result["unresolved_movement_ahead_of_through"]["green"]["pairs"],1)
