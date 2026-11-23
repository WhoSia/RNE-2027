"""P94: capacity-feasibility unit screen for a two-movement pressure proxy.

This intentionally is NOT Varaiya/Gregoire's complete algorithm. A and B are
mutually exclusive stages into separate four-slot receiving links. It compares
an unconstrained queue-difference selector to a capacity-gated selector.
Run: python p94_capacity_gate_screen.py > P94_RESULT.json
"""
import json

CASES = (
    ("blocked_dominant", 12, 4, 6, 0),
    ("both_available", 8, 2, 5, 1),
    ("both_full", 10, 4, 10, 4),
    ("blocked_B_dominant", 1, 0, 9, 4),
    ("no_demand", 0, 0, 0, 0),
    ("available_B_preferred", 5, 3, 4, 0),
)
CAPACITY = 4

def audit_case(name, qa, oa, qb, ob):
    assert 0 <= oa <= CAPACITY and 0 <= ob <= CAPACITY
    assert qa >= 0 and qb >= 0
    pressure = {"A": qa - oa, "B": qb - ob}
    feasible = {"A": qa > 0 and oa < CAPACITY,
                "B": qb > 0 and ob < CAPACITY}
    # Fixed tie-break A. Always trying a selected blocked movement yields 0
    # discharge: it DOES NOT mean the real controller is permitted to waste green.
    naive = max(("A", "B"), key=lambda m: pressure[m])
    eligible = [m for m in ("A", "B") if feasible[m]]
    gated = max(eligible, key=lambda m: pressure[m]) if eligible else None
    return {"case": name, "queue": {"A": qa, "B": qb},
            "receiver_occupancy": {"A": oa, "B": ob},
            "pressure_proxy": pressure,
            "feasible_to_admit": feasible,
            "naive_choice": naive, "capacity_gated_choice": gated,
            "naive_one_tick_admissions": int(feasible[naive]),
            "gated_one_tick_admissions": int(gated is not None)}

def experiment():
    rows = [audit_case(*c) for c in CASES]
    by_case = {r["case"]: r for r in rows}
    assert by_case["blocked_dominant"]["naive_one_tick_admissions"] == 0
    assert by_case["blocked_dominant"]["gated_one_tick_admissions"] == 1
    assert by_case["both_full"]["gated_one_tick_admissions"] == 0
    assert by_case["no_demand"]["gated_one_tick_admissions"] == 0
    assert all(r["gated_one_tick_admissions"] >= r["naive_one_tick_admissions"] for r in rows)
    return {"evidence_grade": "algebraic single-tick controller feasibility test; not T2 engine and not a comparative delay result",
            "definition": "pressure = upstream_queue - downstream_occupancy, capacity=4",
            "warning": "capacity-gated proxy is not published normalized-pressure controller; no theorem or field performance transfers",
            "rows": rows}

if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2))
