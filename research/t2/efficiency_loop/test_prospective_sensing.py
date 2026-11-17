from collections import deque
from dataclasses import replace
from itertools import product
from unittest import TestCase

from d51_phase_order import Params, phase
from prospective_sensing import evaluate, information_at_decision
from timing_bounds import ALPHABET, exact


def enumerate_outcome(path, initial, config, *, lead, decision):
    source,left,through = deque(initial[0]),initial[2],initial[1]
    queue_at_choice, area = None, 0
    config = replace(config,left_first=lead)
    for tick in range(config.horizon_s):
        if tick == decision:
            queue_at_choice = left
        if tick < len(path) and path[tick]:
            source.append(path[tick])
        old_left,old_through = left,through
        green = phase(tick-decision,config) if tick >= decision else "R"
        left -= int(green == "L" and left > 0)
        through -= int(green == "T" and through > 0)
        if source and source[0] == "L" and old_left < config.left_capacity:
            left += 1
            source.popleft()
        elif source and source[0] == "T" and old_through < config.through_capacity:
            through += 1
            source.popleft()
        area += len(source)+left+through
    assert not (source or left or through)
    return queue_at_choice,area


class ProspectiveEvidence(TestCase):
    def test_mid_bin_decision_exposes_only_closed_bins(self):
        self.assertEqual(information_at_decision(((1,1),(2,0),(0,2)),3,5,2),
                         (((1,1),(0,0),(0,0)),((1,1),(2,2),(2,2)),(2,2,2)))

    def test_cross_movement_total_cap_applies_jointly(self):
        base = exact(3,((0,0),),bin_upper=((2,2),),bin_total_upper=(1,))
        self.assertEqual(base.paths,7) # empty and either movement in any of three slots
        with self.assertRaises(ValueError):
            exact(3,((1,1),),bin_total_upper=(1,))

    def test_snapshot_is_before_arrival_on_decision_tick(self):
        params = Params(left_capacity=1,horizon_s=130)
        common = dict(config=params,observed={0:("",),1:("L",)},decision_tick=1)
        self.assertIsNone(exact(2,((0,1),),**common,decision_left=(1,)))
        self.assertEqual(exact(2,((0,1),),**common,decision_left=(0,)).paths,1)

    def test_exact_partitions_match_direct_queue_replay(self):
        p = Params(left_capacity=1,horizon_s=130)
        starts = (("",0,0),("",0,1))
        worlds = {0:[],1:[]}
        for path,start in product(product(ALPHABET,repeat=4),starts):
            if path[:2].count("T") != 1 or path[:2].count("L") != 0 or sum(bool(x) for x in path[2:]) > 1:
                continue
            snap_l,area_l = enumerate_outcome(path,start,p,lead=True,decision=2)
            snap_r,area_r = enumerate_outcome(path,start,p,lead=False,decision=2)
            self.assertEqual(snap_l,snap_r)
            worlds[snap_l].append(area_l-area_r)
        for occ,values in worlds.items():
            b = exact(2,((1,0),(0,0)),p,initial=starts,bin_upper=((1,0),(1,1)),
                      bin_total_upper=(1,1),decision_tick=2,decision_left=(occ,))
            self.assertEqual((b.low,b.high,b.paths),(min(values),max(values),len(values)))

    def test_hidden_counts_never_change_live_policy(self):
        p = Params(left_capacity=1,horizon_s=150)
        a = evaluate(((1,1),(1,0)),p,3,2)
        b = evaluate(((1,1),(0,2)),p,3,2)
        self.assertNotEqual(a["oracle"],b["oracle"])
        for key in ("forecast","sensors"):
            self.assertEqual(a[key],b[key])

    def test_controlled_reversal_survives_without_full_pocket(self):
        from pocket_witness import witness

        by_case = witness()["variants"]
        for capacity in (2,3):
            for tag,expected in (("empty_initial",12),("one_left_initial",-12)):
                row = by_case[f"capacity_{capacity}_{tag}"]
                lead,lag = row["lead"],row["lag"]
                self.assertEqual(lead["area_vehicle_seconds"]-lag["area_vehicle_seconds"],expected)
                self.assertEqual(lead["pocket_at_decision"],lag["pocket_at_decision"])
                self.assertEqual(lead["source_waiting_behind_left_ticks"],0)
                self.assertEqual(lag["source_waiting_behind_left_ticks"],0)
