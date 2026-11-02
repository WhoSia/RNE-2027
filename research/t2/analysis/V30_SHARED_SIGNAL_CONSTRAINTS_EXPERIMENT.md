# T2 v3.0 — Shared signal switching rule benchmark (2026-11-02)

Executed local Python implementation, v3.0. Source, tests, CSV and JSON: https://drive.google.com/file/d/1qYVIIFoeQkG8t24J3BXEIYwX8JhS86Uz/view

Three serial intersections with side origins at 1 and 2, finite link storage, explicit vehicle IDs and identical arrivals across policies. Shared min green 6s and switching lost time 2s applied to fixed/coordinated/pressure. 32 scenario tuples (seeds 0..3, link capacity 4/12, main demand .35/.7 per second, offset 0/10s), 900s per scenario; 96 runs. Five unittest cases passed.

Mean completed OD trips: fixed 393.3125; coordinated 385.125; pressure heuristic 378.6875. Pressure below fixed in 32/32 paired conditions. Coordinated above fixed in 7/32.

This is NOT full Varaiya max-pressure, NOT real traffic validation, and NOT proof of global superiority of fixed-time. Pressure stage chooses main from upstream ready minus downstream occupancy vs side outside queue. No calibrated turning flows, saturation service, or realistic acceleration; side movement at origin zero is not permitted. Need event-level diagnosis.

Known critical issues: same transition parameters do not guarantee equal action opportunities; fixed offset=0 equals fixed schedule, and comparisons should account for paired ties; vehicle_system_seconds is finite horizon occupancy not full-trip delay; horizon truncation and initial empty queues; source code on Drive pending exact GitHub mirroring. No Actions.
