# P2 integration review — hold release

Decision: ACCEPT reproducing both historical P1 source trees and demonstrating implementation-versus-policy confounding; HOLD canonical merge and real traffic validity.

Canonical contract for P3:
1) SignalTimeline with explicit green, yellow/lost, vehicle turn permission, pedestrian exclusive or concurrent conflict allowance and connector-rear-clearance, checked at precise timestamps.
2) Shared VehicleSpec for class geometry, acceleration/braking and headway; remove ad-hoc 0.5m truck numerical margin through invariant-safe integration.
3) ReceivingSpace plus spatially coherent connector state, consistent vehicle footprints, queue spillback; compare receiving-capacity assumptions.
4) Independent 2D space/time occupancy audit including full vehicle length and dynamic pedestrians; fixed-time interval overlap is a necessary check, not a spatial collision guarantee.
5) Matched input + all-drained or correctly censored output, field calibration and independent SUMO/holdout before exhibition realism claims.
6) Preserve P1a/P1b source as immutable and keep paper identifiability/regret separate from simulator artifacts.

No GitHub Actions bot credited. Research date 20261104; shared Research OS folder 02_RESEARCH_LOG/20261104 김우준의 사유. Original full-source ZIP in Drive ID 1rlCh-uiNu35VCCcZsqcxbccyZpY9cntN.