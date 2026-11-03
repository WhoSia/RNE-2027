# T2 v6.7-P1 — Manage complexity without analysis paralysis

The number of factorial cells is product of factor-level counts: 3 newly added binary mechanisms require 2^3=8 cells, 6 common seed replicates produce 48 simulations. Six binary factors would be 64 cells before replications and independent baselines. Therefore use screened factors, a sparse interaction design and targeted adversarial stress tests, not uncontrolled feature accumulation.

Recommended modular interface: VehicleType (length, width, acceleration/braking, minGap), ArrivalProcess (OD and temporal distribution), SignalSchedule (phase and pedestrian exclusive segments), ConnectionGeometry (lane/turn/crosswalk polygons), ReceivingSupply (meter capacity, downstream discharge), SimulatorState (single ownership of vehicles and event logs), Measurement (finite-horizon censoring and field-data errors), Policy (never claim operational safety).

Promote next: real link receiving queues and discharge headway with a finite-coordinate occupancy model; movement-specific mixed fleet saturation flows; crosswalk polygons with pedestrian/bicycle agents; turning+lane-change intent; train/test dates and SUMO reference. Validate separately on movement flow, queue length, velocity/trajectory, and finished journey time. Class-length changes alone do not mean a calibrated truck model. Zero sampled overlap does not prove continuous-time collision avoidance.

Exhibition: first test prediction of real directional flow and queue time series. Academic paper: only after empirical validation assess observation sufficiency, policy regret, heterogeneous-model equivalence.
