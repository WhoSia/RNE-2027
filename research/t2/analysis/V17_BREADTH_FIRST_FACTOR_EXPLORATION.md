# T2 v1.7 — Breadth-first factor screening and interaction triage
Date: 2026-10-31. Branch: research/t2-spatial-fig2-v02.
**Status: LOCAL SYNTHETIC EXPERIMENT; NO FIELD CALIBRATION.**

## Research strategy
This version intentionally broadens the hypothesis space instead of
over-refining one previous mechanism. Eight heterogeneous factor families
were implemented, each with three explicit levels, two pocket lengths
(14m and 70m), and eight paired deterministic seeds: **384 runs**.
Two selected interactions added another **240 runs**:
(1) through-lane-B share × downstream outage (144 runs);
(2) turn-fraction timing × leading/lagging protected signal (96 runs).
**624 total new simulated cases**.

The local execution was tested with 11 new tests and 26 selected inherited
regressions: **37/37 PASS**. Source/test outputs and CSV are available in
the local artifact bundle. The executed local files and connector-authored
GitHub files are not yet certified byte-identical.

## Eight factor families and 14m→70m mean total-network gains
Eight synthetic seeds, 720s, 1,500 veh/h nominal demand, 30% nominal
turning share, 2 through lanes, 4-cell receiving link, 30s green / 60s.
Results (vehicles per 720s):
- Demand timing: steady +29.0; alternating 900/2100 +29.625;
  frontloaded +30.625.
- Turn-share timing: steady +29.0; alternating 5%/55% +20.375;
  frontloaded +26.625. Actual realized turning proportions differ
  slightly across these profiles (mean 29.75%, 30.46%, 30.50%);
  therefore these contrasts are not pure timing interventions.
- Through B-lane allocation: 20% +30.50; 50% +29.0; 80% +13.375.
- Effective stopline headway: 2s +29.0; 3s +18.375; 4s +20.875.
  This is a proxy, not a simulated heavy-truck fleet.
- Signal allocation (L/S protected seconds): 25/60 +35.875;
  35/50 +29.0; 45/40 +28.875.
- Downstream receiving cells: 2 +31.75; 4 +29.0; 8 +21.375.
- Downstream phase offset: 0s +29.0; 20s +1.75; 40s +18.75.
- Exogenous downstream service outage: none +29.0;
  2×15s +22.0; 2×30s +16.625.
  Outages merely suppress downstream service, NOT a microscopic
  bus-stop, collision, lane closure or incident response model.

## Two interaction examples
Lane B fraction 20%, pocket benefit under outages none/2×15s/2×30s:
+30.5 / +18.875 / +15.125 network exits.
Lane B fraction 80%: +13.375 / +13.625 / +19.625.
Thus a single scalar outage effect is insufficient; sensitivity
can reverse sign depending on lane allocation.

With steady turn share, leading-phase pocket benefit +29.0,
lagging +36.25. With frontloaded turning-share profile, leading
+26.625, lagging +26.0. The signal-order preference depends on
synthetic demand profile; no real-world operational recommendation.

## Next candidate families; avoid premature deep modeling
1. Heavy-vehicle and bus proportions with heterogeneous *physical*
   vehicle length, headway, acceleration and lane selection.
2. Bus-stop curb location/dwell and actual blocking-lane geometry,
   instead of the exogenous downstream outage proxy.
3. Initial queue and unserved traffic at the observation boundary;
   do not confuse fixed-horizon exits with stabilized capacity.
4. Upstream platoon coordination and adjacent signals under matching
   signal phase plans and measured arrivals.
5. Pedestrian/cyclist crossing phases and turning conflicts, with
   safety constraints; never infer safety from throughput alone.
6. Tapers, pockets, lane-drop zones, temporary lane use and
   realistic lane-change gap acceptance.
7. Data provenance, sensor detection errors, uncertainty in lane
   dimensions and realized turn proportions.
8. Construction feasibility, land take, cost and directional equity.

## Validation gate
Unit tests / conservation are computational verification only.
External validity still needs a real approach geometry, phase plan,
anonymous cycle counts and held-out observation periods.
No GitHub Actions, no workflow writes, no main merge.
