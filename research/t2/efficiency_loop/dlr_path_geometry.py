"""Sample K047 driving-lane boundaries from its OpenDRIVE map."""
from bisect import bisect_right
from math import ceil, cos, sin
import xml.etree.ElementTree as ET


def preceding(elements, key, s):
    starts = [float(element.attrib[key]) for element in elements]
    index = bisect_right(starts, s) - 1
    return elements[index] if index >= 0 else None


def polynomial(elements, key, s):
    element = preceding(elements, key, s)
    if element is None:
        return 0.0
    ds = s - float(element.attrib[key])
    a, b, c, d = (float(element.attrib[k]) for k in "abcd")
    return a + ds * (b + ds * (c + ds * d))


def pose(road, s):
    segment = preceding(road.findall("./planView/geometry"), "s", s)
    start, x, y, heading = (float(segment.attrib[k]) for k in ("s", "x", "y", "hdg"))
    distance = s - start
    shape = segment[0]
    if shape.tag == "line":
        return x + distance * cos(heading), y + distance * sin(heading), heading
    if shape.tag != "arc":
        raise ValueError(f"Unsupported OpenDRIVE geometry: {shape.tag}")
    curvature = float(shape.attrib["curvature"])
    end_heading = heading + distance * curvature
    return (x + (sin(end_heading) - sin(heading)) / curvature,
            y + (cos(heading) - cos(end_heading)) / curvature, end_heading)


def bounds(road, lane_id, s):
    section = preceding(road.findall("./lanes/laneSection"), "s", s)
    lanes = {int(lane.attrib["id"]): lane for lane in section.findall("./right/lane")}
    if lanes[lane_id].attrib["type"] != "driving":
        raise ValueError(f"Lane {lane_id} is not a driving lane")
    distance = s - float(section.attrib["s"])
    inner = polynomial(road.findall("./lanes/laneOffset"), "s", s)
    for adjacent in range(-1, lane_id, -1):
        inner -= polynomial(lanes[adjacent].findall("width"), "sOffset", distance)
    outer = inner - polynomial(lanes[lane_id].findall("width"), "sOffset", distance)
    x, y, angle = pose(road, s)
    return tuple((x - sin(angle) * d, y + cos(angle) * d) for d in (inner, outer))


def strip(road, lane, start, end, step):
    count = ceil((end - start) / step)
    sides = [bounds(road, lane, start + (end - start) * i / count)
             for i in range(count + 1)]
    return [a for a, _ in sides] + [b for _, b in reversed(sides)]


def corridors(path, step=.25):
    root = ET.parse(path).getroot()
    roads = {road.attrib["id"]: road for road in root.findall("road")}
    result = {}
    for name, road_id, lanes, start, end in (
            ("left_connector", "300015", (-1, -2), 0, None),
            ("through_connector", "300016", (-1, -2), 0, None),
            ("west_receiving", "101000", (-1, -2), 2, 24)):
        road = roads[road_id]
        if end is None:
            end = float(road.attrib["length"])
        result[name] = [strip(road, lane, start, end, step) for lane in lanes]
    return result


def pocket_screen_strips(path, step=.25):
    """Upstream scan band and downstream confirmation on the south exit."""
    root = ET.parse(path).getroot()
    roads = {road.attrib["id"]: road for road in root.findall("road")}
    east, south = roads["100000"], roads["279000"]
    return {"inner_through_at_taper": [strip(east, -3, 80, 105, step)],
            "inner_through_at_stop": [strip(east, -3, 135, 155, step)],
            "south_exit": [strip(south, lane, 5, 20, step) for lane in (-1, -2)]}
