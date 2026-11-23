"""Tests for the P129 movement-separated downstream receivers (split_receiver_v1)."""
from dataclasses import replace
import pytest

from spatial_v10 import Config
from dual_lane_v11 import DualConfig, run


def cfg(**kw):
    base = Config(seed=3, duration_s=900, demand_vph=900, left_fraction=.5,
                  pocket_length_m=7., phase_order="leading")
    return replace(DualConfig(base=base, receiver_slots=4, receiver_mode="cells",
                              through_B_share=.5, allow_lane_changes=True), **kw)


def tape(routes):
    return tuple((2 * i, r) for i, r in enumerate(routes))


def strip(r):
    return {k: v for k, v in r.items() if k not in ("config",)}


@pytest.mark.parametrize("route", ["S", "L"])
def test_single_movement_split_equals_shared(route):
    """With only one movement present, the other link is empty: split must equal legacy."""
    events = tape([route] * 30)
    a = run(cfg(), events, trace=True)
    b = run(cfg(receiver_split=True), events, trace=True)
    for k in ("network_out_S", "network_out_L", "remaining", "outside_vehicle_seconds",
              "upstream_vehicle_seconds", "receiver_vehicle_seconds", "receiver_denied_seconds"):
        assert a[k] == b[k], k
    assert [f["t"] for f in a["frames"]] == [f["t"] for f in b["frames"]]


def test_mixed_split_conserves_and_separates_movements():
    events = tape(["L", "S", "S", "L"] * 15)
    r = run(cfg(receiver_split=True), events, trace=True)
    assert r["remaining"] == 0 and r["network_out_S"] + r["network_out_L"] == 60
    for f in r["frames"]:
        for link, _, _, mv in f["receiver"]:
            assert link == mv  # an L vehicle never enters the S link and vice versa
        assert sum(1 for x in f["receiver"] if x[0] == "S") <= 4
        assert sum(1 for x in f["receiver"] if x[0] == "L") <= 4


def test_left_free_never_slower_for_left():
    events = tape(["L", "S", "S", "L"] * 15)
    same = run(cfg(receiver_split=True), events)
    free = run(cfg(receiver_split=True, receiver_split_left_free=True), events)
    assert free["remaining"] == same["remaining"] == 0
    assert free["receiver_vehicle_seconds"] <= same["receiver_vehicle_seconds"]


def test_default_config_output_has_no_split_keys():
    r = run(cfg(), tape(["S", "L"] * 5))
    assert "receiver_split" not in r["config"]


def test_invalid_combinations():
    with pytest.raises(ValueError):
        run(cfg(receiver_split_left_free=True), tape(["S"]))
    with pytest.raises(ValueError):
        run(cfg(receiver_split=True, receiver_mode="fifo"), tape(["S"]))
