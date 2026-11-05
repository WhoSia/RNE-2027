# D29 — External reproduction: an inspectable interface, NOT an external run

Built `src/validation.py`, which opens **existing** SUMO `tripinfo` XML (never generates or fakes a field record), requires a coherent arrival/departure/duration and unique vehicle IDs, and refuses unmatched model/external cohorts by default. It reports duration MAE, signed bias, maximum absolute error. A separate queue CSV contract explicitly requires `queue_vehicles`: link detector counts cannot silently substitute for queue-length observations. Source SHA256 receipts are available via `file_receipt`.

**SUMO executable status:** not installed (`sumo` command absent; `sumolib`/`traci` Python modules absent). The XML ingestion test uses a *synthetic test fixture*, not actual SUMO. No NGSIM/inD scene trajectories or site queue observations have been loaded; no real GTFS feed acquired this turn. Official output schema: https://eclipse.dev/sumo/docs/Simulation/Output/TripInfo.html and https://sumo.dlr.de/docs/Simulation/Output/ .

Minimum independent validation before any physical or external effect claim:
1. Select one geometrically matched road and identical demand, signal and types; define units, clock, network topology.
2. Run SUMO microscopic model, preserve command line, executable version, `net.xml`, `routes.xml`, route/tripinfo/FCD outputs and SHA256 receipts.
3. Match vehicle IDs and arrival cohorts; report missing IDs and arrival-time bias, not just finished trips.
4. Compare queue length, first queue occurrence, max storage, travel-time distribution and initial temporal divergence; repeat across dt and random seeds.
5. Compare field observations on disjoint dates/locations with explicit measurement uncertainty; never equate counts and bumper-to-bumper queues.

Evidence state **HOLD** for independent SUMO and physical truth despite working parser/tests.
