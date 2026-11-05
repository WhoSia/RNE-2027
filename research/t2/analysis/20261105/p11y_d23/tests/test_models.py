import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from transit_schedule import Connection, earliest_arrival, shortest_distance, scenario
from zone_phases import Movement, simulate, DeadlockError

class TestTimetable(unittest.TestCase):
    def setUp(self):
        self.c = scenario()
    def test_longer_but_faster(self):
        dist, route = shortest_distance(self.c, 'O', 'D')
        self.assertEqual((dist, route), (3.0, ('O', 'N', 'D')))
        r = earliest_arrival(self.c, 'O', 'D', 0)
        self.assertEqual(r['arrival'], 14)
        self.assertEqual(r['distance_km'], 8.0)
        self.assertEqual(r['transfers'], 1)
    def test_transfer_margin_changes_destination(self):
        a = earliest_arrival(self.c, 'O', 'D', 0, transfer_min=1)
        b = earliest_arrival(self.c, 'O', 'D', 0, transfer_min=2)
        self.assertEqual((a['arrival'], b['arrival']), (14,20))
    def test_no_transfers_blocks_2_leg_trip(self):
        self.assertIsNone(earliest_arrival(self.c, 'O', 'D', 0, max_transfers=0))
    def test_invalid_trip_times(self):
        with self.assertRaises(ValueError): earliest_arrival([Connection('x','O','D',2,2,1)],'O','D',0)
    def test_duplicate_stop_same_trip_valid_continuity(self):
        cs = [Connection('x','O','A',0,2,1),Connection('x','A','D',2,5,1)]
        r = earliest_arrival(cs,'O','D',0,max_transfers=0)
        self.assertEqual((r['arrival'],r['transfers']), (5,0))
    def test_unreachable(self):
        self.assertIsNone(earliest_arrival(self.c,'D','O',0))
    def test_departure_time_changes_selected_trip(self):
        r = earliest_arrival(self.c,'O','D',15)
        self.assertGreaterEqual(r['arrival'],15)
        self.assertTrue(r['legs'])
    def test_invalid_transfer(self):
        with self.assertRaises(ValueError): earliest_arrival(self.c,'O','D',0,transfer_min=-1)

class TestSequentialOccupancy(unittest.TestCase):
    def test_phased_holds_upstream_while_downstream_busy(self):
        demands=[Movement('ped',0,(('B',3),)),Movement('car',0,(('A',2),('B',2))),Movement('follower',1,(('A',1),))]
        r=simulate(demands)
        self.assertIn((3,'release','car','A'),r['log'])
        self.assertIn((3,'enter','car','B'),r['log'])
        self.assertEqual(r['starts']['follower'],3)
        self.assertEqual(r['finishes']['car'],5)
    def test_independent_movements(self):
        r=simulate([Movement('a',0,(('A',3),)),Movement('b',1,(('B',2),))])
        self.assertEqual(r['starts'],{'a':0,'b':1})
    def test_same_zone_serialized(self):
        r=simulate([Movement('a',0,(('A',3),)),Movement('b',0,(('A',1),))])
        self.assertEqual(r['starts']['b'],3)
    def test_two_way_gridlock_detected(self):
        with self.assertRaises(DeadlockError): simulate([Movement('a',0,(('A',2),('B',1))),Movement('b',0,(('B',2),('A',1)))])
    def test_invalid_duration(self):
        with self.assertRaises(ValueError):simulate([Movement('a',0,(('A',0),))])
    def test_no_negative_clock(self):
        with self.assertRaises(ValueError):simulate([Movement('a',-1,(('A',1),))])
    def test_same_tick_release_first(self):
        r=simulate([Movement('a',0,(('A',2),)),Movement('b',2,(('A',1),))])
        self.assertEqual(r['starts']['b'],2)
    def test_no_duplicate_ids(self):
        with self.assertRaises(ValueError):simulate([Movement('a',0,(('A',1),)),Movement('a',1,(('B',1),))])

if __name__ == '__main__': unittest.main()

class TestIndependentOracle(unittest.TestCase):
    def test_random_small_dags_against_exhaustive_enumeration(self):
        """Independent path enumeration verifies the label setting algorithm."""
        import random
        rng = random.Random(20261105)
        from transit_schedule import earliest_arrival
        for n in range(150):
            connections = []
            for i in range(4):
                for j in range(i + 1, 4):
                    for k in range(rng.randint(0, 2)):
                        dep = rng.randrange(0, 20)
                        connections.append(Connection(f't_{n}_{i}_{j}_{k}',str(i),str(j),dep,dep+rng.randint(1,5),1.0))
            if not connections:
                continue
            margin=rng.randint(0,3)
            start=rng.randint(0,8)
            def exhaustive(stop,t,last,changes):
                if stop=='3':
                    return t
                result=float('inf')
                for c in connections:
                    change = int(last is not None and last != c.trip)
                    if c.origin==stop and changes+change <=2 and c.depart >= t + (margin if change else 0):
                        result=min(result,exhaustive(c.destination,c.arrive,c.trip,changes+change))
                return result
            expected=exhaustive('0',start,None,0)
            out=earliest_arrival(connections,'0','3',start,transfer_min=margin,max_transfers=2)
            self.assertEqual(out['arrival'] if out else float('inf'),expected)
