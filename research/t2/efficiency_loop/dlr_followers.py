"""Screen same-lane followers using observed K047 tracks and downstream route evidence."""
import argparse
from bisect import bisect_right
from collections import defaultdict
import csv
from dataclasses import dataclass
from datetime import datetime
import json
from math import cos, floor, radians
from pathlib import Path
import xml.etree.ElementTree as ET

from dlr_path_cases import CLOCK
from dlr_path_geometry import pocket_screen_strips, pose, strip
from dlr_path_screen import EXPECTED_MAP, ORIGIN, masks, raster, sha

BANDS = ((80, 105), (105, 135), (135, 155))
CELL_M = .25
TICKS_PER_S = 20


def approach_lookup(map_path):
    road = ET.parse(map_path).find("./road[@id='100000']")
    lookup = {}
    ambiguous = set()
    for lane in (-1, -2, -3, -4):
        for s in range(BANDS[0][0], BANDS[-1][1]):
            angle = pose(road, s+.5)[2]
            for cell in raster(strip(road, lane, s, s+1, CELL_M), CELL_M):
                if cell in lookup:
                    ambiguous.add(cell)
                lookup[cell] = (lane, s+.5, angle)
    for cell in ambiguous:
        del lookup[cell]
    return lookup


@dataclass(frozen=True)
class Approach:
    tick: int
    track: str
    lane: int
    position_m: float
    speed: float


def observations(map_path, track_path):
    if sha(map_path) != EXPECTED_MAP:
        raise ValueError("Unrecognized K047 map")
    regions = masks(map_path, CELL_M)
    regions["south_exit"] = set().union(*(raster(p,CELL_M) for p in
                                         pocket_screen_strips(map_path)["south_exit"]))
    points = approach_lookup(map_path)
    downstream = defaultdict(lambda: defaultdict(set))
    approach = []
    with track_path.open(newline="", encoding="utf-8-sig") as stream:
        for row in csv.DictReader(stream):
            if row["interpolated"].strip().lower() != "false":
                continue
            cell = (floor((float(row["center_easting"])-ORIGIN[0])/CELL_M),
                    floor((float(row["center_northing"])-ORIGIN[1])/CELL_M))
            here = points.get(cell)
            zones = [k for k in ("left_connector","south_exit","through_connector","west_receiving")
                     if cell in regions[k]]
            if here is None and not zones:
                continue
            if sum(float(row[f"classifications_{kind}"]) for kind in ("car","truck","van")) < .5:
                continue
            stamp = (datetime.fromisoformat(row["timestamp"]) - CLOCK).total_seconds()
            tick = round(stamp*TICKS_PER_S)
            track = row["id"]
            if here is not None:
                lane, s, heading = here
                if cos(radians(float(row["yaw"]))-heading) >= cos(radians(35)):
                    approach.append(Approach(tick, track, lane, s, float(row["velocity_magnitude"])))
            for zone in zones:
                downstream[track][zone].add(tick)
    return approach, downstream


def route_after(first, downstream):
    """Require consecutive zones in order. Future route is a diagnostic label."""
    stop = first + 90*TICKS_PER_S
    matches = []
    for movement, connector, exit_zone in (
            ("left","left_connector","south_exit"), ("through","through_connector","west_receiving")):
        outbound = sorted(t for t in downstream.get(exit_zone, ()) if first < t <= stop)
        junction = sorted(t for t in downstream.get(connector, ()) if first < t <= stop)
        # The fifth connector sample must precede at least five exit samples.
        if len(junction) >= 5 and sum(t > junction[4] for t in outbound) >= 5:
            matches.append(movement)
    return matches[0] if len(matches) == 1 else "unknown"


def green_clock(signal):
    samples = []
    with signal.open(newline="", encoding="utf-8-sig") as stream:
        for row in csv.DictReader(stream):
            if int(row["id"]) == 3:
                stamp = (datetime.fromisoformat(row["timestamp"]) - CLOCK).total_seconds()
                code = int(row["state"])
                stage = "green" if code in (5,6) else "non_green" if code in (3,4,7,8) else "unknown"
                samples.append((stamp,stage))
    samples.sort()
    times = [t for t,_ in samples]
    if not times or any(a >= b for a,b in zip(times,times[1:])):
        raise ValueError("Signal samples are missing or repeated")

    def status(tick):
        first = bisect_right(times,(tick-.5)/TICKS_PER_S)-1
        last = bisect_right(times,(tick+.5)/TICKS_PER_S)
        if first < 0 or last == len(times) or last != first+1 or times[last]-times[first] > 1.25:
            return "unknown"
        a,b = samples[first][1],samples[last][1]
        return a if a == b else "unknown"

    return status


def runs(ticks):
    """Each run joins adjacent observed bins without bridging gaps."""
    sequence = sorted(set(ticks))
    if not sequence:
        return []
    spans = []
    first = previous = sequence[0]
    for t in sequence[1:]:
        if t != previous+1:
            spans.append((first,previous))
            first = t
        previous = t
    return spans+[(first,previous)]


def review(approach, downstream, signal_status, slow_limit=2):
    first = {}
    for row in approach:
        first[row.track] = min(first.get(row.track,row.tick),row.tick)
    movement = {track: route_after(t, downstream.get(track, {})) for track,t in first.items()}
    counts = {str(band): {m: set() for m in ("left","through","unknown","slow_left","slow_through")}
              for band in BANDS}
    groups = defaultdict(dict)
    left_control = defaultdict(set)
    for row in approach:
        if row.lane in (-1,-2):
            if movement[row.track] == "left":
                left_control["observed"].add(row.track)
                if row.speed <= slow_limit:
                    left_control["slow"].add(row.track)
            continue
        band = next(b for b in BANDS if b[0] <= row.position_m < b[1])
        m = movement[row.track]
        counts[str(band)][m].add(row.track)
        if row.speed <= slow_limit and m in ("left","through"):
            counts[str(band)]["slow_"+m].add(row.track)
        key = row.tick, row.lane
        state = groups[key]
        if row.track in state:
            # Ambiguous multiple observations for one ID in this lane and tick.
            state[row.track] = None
        else:
            state[row.track] = row
    candidates = defaultdict(list)
    controls = defaultdict(list)
    unresolved = defaultdict(list)
    excluded_ties = 0
    for (tick,lane), states in groups.items():
        # Skip bins whose complete within-lane ordering cannot be reconstructed.
        if None in states.values():
            continue
        ordered = sorted(states.values(), key=lambda q:q.position_m)
        if any(a.position_m == b.position_m for a,b in zip(ordered,ordered[1:])):
            excluded_ties += 1
            continue
        for follower, leader in zip(ordered, ordered[1:]):
            gap = leader.position_m-follower.position_m
            if (leader.speed > slow_limit or follower.speed > slow_limit or not 4 <= gap <= 18
                    or movement[follower.track] != "through"):
                continue
            route = movement[leader.track]
            target = {"left": candidates, "through": controls, "unknown": unresolved}[route]
            target[lane,leader.track,follower.track,signal_status(tick)].append(tick)

    def summaries(pairs):
        report = {}
        for light in ("green","non_green","unknown"):
            subset = {key:t for key,t in pairs.items() if key[-1] == light}
            episodes = [(b-a, a, b, lane, lead, follow)
                        for (lane,lead,follow,_),ticks in subset.items() for a,b in runs(ticks)]
            # Report positions in the first frame to disambiguate multiple pairs in one lane.
            longest = sorted(episodes,key=lambda x:(-x[0],x[1],x[3]))[:3]
            report[light] = {"pairs": len(subset), "observed_pair_bins": sum(map(len,subset.values())),
                             "runs_ge_1s": sum(d >= TICKS_PER_S for d,*_ in episodes),
                             "longest_runs": [{"lane":lane, "clock_start_s":a/TICKS_PER_S,
                                              "clock_end_s":b/TICKS_PER_S, "span_s":d/TICKS_PER_S,
                                              "leader_s_m":groups[a,lane][lead].position_m,
                                              "follower_s_m":groups[a,lane][follow].position_m}
                                             for d,a,b,lane,lead,follow in longest]}
        return report

    return {"band_track_counts": {b:{k:len(v) for k,v in c.items()} for b,c in counts.items()},
            "slow_left_ahead_of_through": summaries(candidates),
            "slow_through_ahead_of_through_control": summaries(controls),
            "unresolved_movement_ahead_of_through": summaries(unresolved),
            "dedicated_left_lane_control": {k:len(left_control[k]) for k in ("observed","slow")},
            "tied_position_lane_bins_excluded": excluded_ties}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("map",type=Path)
    parser.add_argument("output",type=Path)
    parser.add_argument("inputs",type=Path,nargs="+",help="Trajectory and signal CSV pairs")
    args = parser.parse_args()
    report = {}
    for track, signal in zip(args.inputs[::2],args.inputs[1::2],strict=True):
        if track.name.removeprefix("trajectories_") != signal.name.removeprefix("traffic-lights_"):
            parser.error("Trajectory and signal intervals must match")
        approach, downstream = observations(args.map, track)
        status = green_clock(signal)
        report[track.name] = {"trajectory_sha256":sha(track), "signal_sha256":sha(signal),
                              "approach_rows":len(approach), "results": {
                                  str(speed):review(approach,downstream,status,speed) for speed in (1,2,3)
                              }}
    args.output.write_text(json.dumps(report,indent=2)+"\n")
