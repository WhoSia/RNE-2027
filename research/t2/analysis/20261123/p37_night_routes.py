"""Check P36 movement hypotheses against direct nighttime trajectory samples."""
from collections import Counter
import xml.etree.ElementTree as ET

from dlr_path_geometry import strip
from dlr_path_screen import raster
from dlr_route_evidence import BANDS, CELL_M, SOUTH, WEST, regions_and_gates

LEFT_CONNECTOR = "left_connector"
ROUTES = {3: (*BANDS, WEST), 4: (LEFT_CONNECTOR, SOUTH)}


def route_masks(map_path):
    regions, gate, _ = regions_and_gates(map_path)
    left = ET.parse(map_path).getroot().find("road[@id='300015']")
    length = float(left.attrib["length"])
    regions[LEFT_CONNECTOR] = set().union(*(
        raster(strip(left, lane, 0, length, CELL_M), CELL_M) for lane in (-1, -2)
    ))
    counts = Counter(cell for cells in regions.values() for cell in cells)
    for cells in regions.values():
        cells.difference_update(cell for cell, count in counts.items() if count > 1)
    return regions, gate
