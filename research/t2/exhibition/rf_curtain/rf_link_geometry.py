"""First-Fresnel geometry audit ONLY: not Wi-Fi CSI prediction or a ray tracer.

Use this before placing two RF links in a school/laboratory model. The first
Fresnel ellipse is not a detector's spatial footprint or a guarantee of
vehicle classification. No road sensor or controller is accessed.
"""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass

C_M_PER_S = 299_792_458.0


def first_fresnel_radius_m(frequency_ghz: float, path_length_m: float,
                            distance_from_tx_m: float | None = None) -> float:
    """Paraxial first-zone radius sqrt(lambda*d1*d2/(d1+d2))."""
    if not all(math.isfinite(x) and x > 0 for x in (frequency_ghz, path_length_m)):
        raise ValueError("frequency and path length must be positive finite numbers")
    d1 = path_length_m / 2 if distance_from_tx_m is None else distance_from_tx_m
    if not math.isfinite(d1) or not 0 < d1 < path_length_m:
        raise ValueError("point must be strictly between transmitter and receiver")
    wavelength = C_M_PER_S / (frequency_ghz * 1e9)
    return math.sqrt(wavelength * d1 * (path_length_m-d1) / path_length_m)


@dataclass(frozen=True)
class Link:
    name: str
    midpoint_x_m: float
    midpoint_y_m: float
    path_length_m: float
    frequency_ghz: float = 2.4

    def __post_init__(self):
        if not self.name.strip() or not all(map(math.isfinite, (self.midpoint_x_m, self.midpoint_y_m))):
            raise ValueError("invalid link name or midpoint")
        first_fresnel_radius_m(self.frequency_ghz, self.path_length_m)

    @property
    def radius_m(self):
        return first_fresnel_radius_m(self.frequency_ghz, self.path_length_m)


def pairwise_midpoint_gate(a: Link, b: Link) -> dict:
    """Midpoint-disc overlap heuristic; **not** RF lane separation proof."""
    dist=math.hypot(a.midpoint_x_m-b.midpoint_x_m,
                    a.midpoint_y_m-b.midpoint_y_m)
    total=a.radius_m+b.radius_m
    return {"link_a":a.name,"link_b":b.name,
            "midpoint_separation_m":dist,
            "sum_first_zone_midpoint_radii_m":total,
            "overlap_heuristic":dist < total,
            "boundary_contact":math.isclose(dist,total,rel_tol=1e-12,abs_tol=1e-12),
            "meaning":"MIDPOINT GEOMETRY HEURISTIC ONLY; multipath may couple links"}


def exhibition_geometry_audit() -> dict:
    # Two longitudinal inspection sections, not promises of separate traffic lanes.
    pocket=Link("pocket_entry_section",0,0,1.0,2.4)
    downstream=Link("downstream_receiving_section",0,.70,1.0,2.4)
    adjacent=Link("adjacent_scaled_lane",.175,0,1.0,2.4)  # 3.5m / 20 scale
    return {"status":"ANALYTIC_GEOMETRY_NOT_MEASURED_WIFI",
            "frequency_ghz":2.4,
            "sample_links":[{**asdict(x),"fresnel_midpoint_radius_m":x.radius_m}
                            for x in (pocket,downstream,adjacent)],
            "section_pair":pairwise_midpoint_gate(pocket,downstream),
            "adjacent_scaled_lane_pair":pairwise_midpoint_gate(pocket,adjacent),
            "warning":"Do not infer measured CSI resolution or static occupancy detection from this"}


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--json",action="store_true")
    args=parser.parse_args()
    output=exhibition_geometry_audit()
    if args.json:
        print(json.dumps(output,indent=2,ensure_ascii=False))
    else:
        for p in output['sample_links']:
            print(f"{p['name']}: radius {p['fresnel_midpoint_radius_m']:.3f} m")
        for k in ('section_pair','adjacent_scaled_lane_pair'):
            v=output[k]
            print(k, 'MIDPOINT_OVERLAP' if v['overlap_heuristic'] else 'NO_MIDPOINT_OVERLAP')
