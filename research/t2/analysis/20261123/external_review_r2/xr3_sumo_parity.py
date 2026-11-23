"""XR3 (external review r2): geometry-matched SUMO replica of one T2 world and the E0 parity gates.

Builds (netconvert) a 140 m two-lane approach whose last 7 m carries a 1-slot left pocket, a
signalised stopline J1, a 28 m single-lane shared receiver (4 x 7 m vehicles), a signalised
downstream stopline J2 and a 200 m exit. Vehicle spacing 7 m (length 5 + minGap 2), vmax 7 m/s.
L vehicles may use only the pocket lane at the stopline (own vClass); S vehicles only lanes 0/1.
Signals are written as explicit non-repeating programs from the exact T2 calendars.

Gates (all must pass before any policy-sign comparison is allowed):
  E0a identity: same 60 IDs and movements, all exit.
  E0b inflow: SUMO insertion (depart) time vs T2 admission time onto the approach: median |diff| <= 1 s
       (both engines hold vehicles outside the link when the entry is occupied; raw arrival is identical).
  E0c signals: TraCI-sampled J1/J2 states match the T2 calendars at every whole second.
  E0d storage: receiver holds at most 4 vehicles and reaches 4.
  E0e exits: median |exit_SUMO - exit_T2| <= 3 s and 90th percentile <= 10 s, per policy arm.
"""
import json, os, statistics, subprocess, sys, tempfile
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

import sumo
os.environ.setdefault("SUMO_HOME", sumo.SUMO_HOME)
import traci  # noqa: E402

from p85_signal_coordination import build_config, run, phases  # noqa: E402
from p118_temporal_arrival_holdout import tape_with_random_times  # noqa: E402
from receiving_cells_v15 import ReceivingCells  # noqa: E402
from spatial_v10 import phase as base_phase  # noqa: E402

HERE = Path(__file__).resolve().parent
BIN = Path(sumo.SUMO_HOME) / "bin"
HORIZON = 1500


def t2_reference(cfg, tape, period, phi):
    cp = run(cfg, tape, checkpoint_at=84, trace=True)

    def green(self, t):
        return ((t - 84 + phi) % period) < period // 2
    with patch.object(ReceivingCells, "green", green):
        r = run(cfg, tape, resume_from=cp, phase_overrides=phases(6, "left_first"), trace=True)
    assert r["remaining"] == 0
    last, lane, cross, admit = {}, {}, {}, {}
    for f in r["frames"]:
        for x, vid, _ in f["A"]:
            lane.setdefault(vid, "A"); admit.setdefault(vid, f["t"])
        for x, vid, _ in f["B"]:
            lane.setdefault(vid, "B"); admit.setdefault(vid, f["t"])
        for _, vid, _ in f["receiver"]:
            last[vid] = f["t"]
    for e in r["service_events"]:
        if e["reason"] == "stopline_cross":
            cross[e["vehicle_id"]] = e["t"]
    exit_t = {v: t + 1 for v, t in last.items()}
    return dict(exit=exit_t, lane=lane, cross=cross, admit=admit, cost=sum(exit_t[i] - tape[i][0] for i in range(len(tape))))


def calendars(cfg, period, phi):
    up, down = [], []
    ov = phases(6, "left_first")
    for t in range(HORIZON):
        if t < 84:
            u = base_phase(cfg.base, t)
            d = (t % 60) < 30
        else:
            u = next((v for a, b, v in ov if a <= t < b), base_phase(cfg.base, t))
            d = ((t - 84 + phi) % period) < period // 2
        up.append(u); down.append(d)
    return up, down


def runs_to_phases(states):
    out = []
    for s in states:
        if out and out[-1][1] == s:
            out[-1][0] += 1
        else:
            out.append([1, s])
    return out


def build(folder, cfg, tape, ref, period, phi):
    f = Path(folder)
    (f / "n.nod.xml").write_text("""<nodes>
 <node id="S" x="-140" y="0"/><node id="M" x="-7" y="0"/>
 <node id="J1" x="0" y="0" type="traffic_light"/><node id="J2" x="28" y="0" type="traffic_light"/>
 <node id="E" x="228" y="0"/></nodes>""")
    (f / "n.edg.xml").write_text("""<edges>
 <edge id="app1" from="S" to="M" numLanes="2" speed="7"/>
 <edge id="app2" from="M" to="J1" numLanes="3" speed="7">
  <lane index="0" disallow="taxi"/><lane index="1" disallow="taxi"/><lane index="2" allow="taxi"/></edge>
 <edge id="rcv" from="J1" to="J2" numLanes="1" speed="7"/>
 <edge id="out" from="J2" to="E" numLanes="1" speed="7"/></edges>""")
    (f / "n.con.xml").write_text("""<connections>
 <connection from="app1" to="app2" fromLane="0" toLane="0"/>
 <connection from="app1" to="app2" fromLane="1" toLane="1"/>
 <connection from="app1" to="app2" fromLane="1" toLane="2"/>
 <connection from="app2" to="rcv" fromLane="0" toLane="0"/>
 <connection from="app2" to="rcv" fromLane="1" toLane="0"/>
 <connection from="app2" to="rcv" fromLane="2" toLane="0"/>
 <connection from="rcv" to="out" fromLane="0" toLane="0"/></connections>""")
    subprocess.run([str(BIN / "netconvert"), "-n", "n.nod.xml", "-e", "n.edg.xml", "-x", "n.con.xml",
                    "-o", "n.net.xml", "--no-turnarounds", "--junctions.corner-detail", "0",
                    "--tls.left-green.time", "0", "--no-internal-links", "true"],
                   cwd=f, check=True, capture_output=True)
    # link indices at J1 per fromLane
    import sumolib
    net = sumolib.net.readNet(str(f / "n.net.xml"))
    j1 = {}
    for c in net.getEdge("app2").getOutgoing()[net.getEdge("rcv")]:
        j1[c.getFromLane().getIndex()] = c.getTLLinkIndex()
    assert sorted(j1) == [0, 1, 2] and sorted(j1.values()) == [0, 1, 2], j1
    up, down = calendars(cfg, period, phi)

    def j1_state(u):
        s = ["r"] * 3
        if u == "S":
            s[j1[0]] = s[j1[1]] = "G"
        if u == "L":
            s[j1[2]] = "G"
        return "".join(s)
    j1p = runs_to_phases([j1_state(u) for u in up])
    j2p = runs_to_phases(["G" if d else "r" for d in down])
    tl = ['<additional>']
    for tid, ph in (("J1", j1p), ("J2", j2p)):
        tl.append(f' <tlLogic id="{tid}" type="static" programID="t2" offset="0">')
        tl += [f'  <phase duration="{d}" state="{s}"/>' for d, s in ph]
        tl.append(' </tlLogic>')
    tl.append('</additional>')
    (f / "tls.add.xml").write_text("\n".join(tl))
    veh = ['<routes>',
           ' <vType id="S" vClass="passenger" length="5" minGap="2" maxSpeed="7" accel="7" decel="7" emergencyDecel="9" sigma="0" tau="1"/>',
           ' <vType id="L" vClass="taxi" length="5" minGap="2" maxSpeed="7" accel="7" decel="7" emergencyDecel="9" sigma="0" tau="1"/>',
           ' <route id="r" edges="app1 app2 rcv out"/>']
    for i, (t, m) in enumerate(tape):
        lane = 1 if m == "L" or ref["lane"].get(i) == "A" else 0
        veh.append(f' <vehicle id="v{i:02d}" type="{m}" route="r" depart="{t}" departLane="{lane}" departSpeed="max" departPos="base"/>')
    veh.append('</routes>')
    (f / "veh.rou.xml").write_text("\n".join(veh))


def simulate(folder, tape, up, down, step=0.25):
    f = Path(folder)
    traci.start([str(BIN / "sumo"), "-n", str(f / "n.net.xml"), "-r", str(f / "veh.rou.xml"),
                 "-a", str(f / "tls.add.xml"), "--step-length", str(step), "--no-step-log", "true",
                 "--time-to-teleport", "-1", "--collision.action", "warn", "--no-warnings", "true"])
    traci.trafficlight.setProgram("J1", "t2"); traci.trafficlight.setProgram("J2", "t2")
    depart, exit_t, cross, max_rcv, sig_bad = {}, {}, {}, 0, 0
    t = 0.0
    while t < HORIZON and len(exit_t) < len(tape):
        traci.simulationStep(); t = traci.simulation.getTime()
        for v in traci.simulation.getDepartedIDList():
            depart[v] = t
        on_rcv = traci.edge.getLastStepVehicleIDs("rcv")
        max_rcv = max(max_rcv, len(on_rcv))
        for v in on_rcv:
            cross.setdefault(v, t)
        for v in traci.edge.getLastStepVehicleIDs("out"):
            exit_t.setdefault(v, t)
        if abs((t - step) - round(t - step)) < 1e-9 and int(round(t - step)) < HORIZON:
            # state reported after the step that covers [k, k+step) is compared with calendar second k
            s1 = traci.trafficlight.getRedYellowGreenState("J1"); s2 = traci.trafficlight.getRedYellowGreenState("J2")
            k = int(round(t - step))
            want2 = "G" if down[k] else "r"
            sig_bad += (s2 != want2) + (("G" in s1) != (up[k] in ("L", "S")))
    traci.close()
    return depart, exit_t, cross, max_rcv, sig_bad


def main():
    seed, ts, fam, share, cap = 86001, 88501, "stochastic_uniform", .75, 4
    tape = tape_with_random_times(build_config(seed, 900, share, 7, 4, .5), seed, ts, fam)
    cfg = build_config(seed, 900, share, 7, cap, .5)
    cfg = replace(cfg, base=replace(cfg.base, duration_s=4800))
    out = dict(world=dict(label_seed=seed, time_seed=ts, family=fam, share=share, capacity=cap), arms={})
    for period, phi in ((30, 15), (60, 30)):
        ref = t2_reference(cfg, tape, period, phi)
        up, down = calendars(cfg, period, phi)
        with tempfile.TemporaryDirectory() as d:
            build(d, cfg, tape, ref, period, phi)
            dep, ex, cr, mx, bad = simulate(d, tape, up, down)
        ids = [f"v{i:02d}" for i in range(len(tape))]
        exited = [v for v in ids if v in ex]
        ins_delay = [dep[v] - tape[int(v[1:])][0] for v in ids if v in dep]
        adm_err = sorted(abs(dep[v] - ref["admit"][int(v[1:])]) for v in ids if v in dep)
        cross_err = sorted(abs(cr[v] - ref["cross"][int(v[1:])]) for v in ids if v in cr and int(v[1:]) in ref["cross"])
        err = [ex[v] - ref["exit"][int(v[1:])] for v in exited]
        abs_err = sorted(abs(e) for e in err)
        gates = dict(E0a_identity=len(exited) == 60,
                     E0b_inflow=bool(adm_err) and statistics.median(adm_err) <= 1.0,
                     E0c_signals=bad == 0,
                     E0d_storage=mx == 4,
                     E0e_exits=bool(abs_err) and statistics.median(abs_err) <= 3 and abs_err[int(.9 * (len(abs_err) - 1))] <= 10)
        out["arms"][f"{period}/phi{phi}"] = dict(
            gates=gates, all_pass=all(gates.values()), exited=len(exited), max_receiver=mx, signal_mismatch_samples=bad,
            insertion_delay_max=max(ins_delay) if ins_delay else None,
            admission_error_median_abs=statistics.median(adm_err) if adm_err else None,
            admission_error_max_abs=max(adm_err) if adm_err else None,
            stopline_cross_error_median_abs=statistics.median(cross_err) if cross_err else None,
            stopline_cross_error_p90_abs=cross_err[int(.9 * (len(cross_err) - 1))] if cross_err else None,
            insertion_delay_median=statistics.median(ins_delay) if ins_delay else None,
            exit_error_median_abs=statistics.median(abs_err) if abs_err else None,
            exit_error_p90_abs=abs_err[int(.9 * (len(abs_err) - 1))] if abs_err else None,
            exit_error_signed_mean=sum(err) / len(err) if err else None,
            t2_cost=ref["cost"],
            sumo_cost=(sum(ex[v] - tape[int(v[1:])][0] for v in exited) if len(exited) == 60 else None))
        print(period, phi, json.dumps(out["arms"][f"{period}/phi{phi}"]), flush=True)
    a = out["arms"]
    out["policy_sign_comparison_allowed"] = all(x["all_pass"] for x in a.values())
    if out["policy_sign_comparison_allowed"]:
        out["t2_delta"] = a["30/phi15"]["t2_cost"] - a["60/phi30"]["t2_cost"]
        out["sumo_delta"] = a["30/phi15"]["sumo_cost"] - a["60/phi30"]["sumo_cost"]
    (HERE / "XR3_RESULT.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k != "arms"}))


if __name__ == "__main__":
    sys.exit(main())
