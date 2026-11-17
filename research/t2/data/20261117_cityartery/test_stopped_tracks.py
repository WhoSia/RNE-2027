from io import StringIO

from stopped_tracks import summarize


def test_crossing_track_remains_distinct_and_long_runs_count_once():
    data = """Type, vedio-id, Track ID-new, Time [s]-new, Speed [km/h]
Car,1,7,0,0
Car,1,7,1.001,0
Car,1,7,2.002,1
Car,1,7,3.003,2
Car,1,7,4.004,4
Car,1,7,5.005,0
Car,1,7,6.006,0
Car,1,7,7.007,0
Pedestrian,2,7,0,1
Pedestrian,2,7,1.001,1
Pedestrian,2,7,2.002,1
"""
    assert summarize(StringIO(data)) == {
        "tracks": {"Car": 1, "Pedestrian": 1},
        "episodes": {"Car": 2, "Pedestrian": 1},
        "tracks_with_episode": {"Car": 1, "Pedestrian": 1},
    }


def test_gap_cannot_create_a_stop_episode():
    data = """Type, vedio-id, Track ID-new, Time [s]-new, Speed [km/h]
Car,1,7,0,0
Car,1,7,1.001,0
Car,1,7,4.004,0
Car,1,7,5.005,0
"""
    assert summarize(StringIO(data))["episodes"] == {}
