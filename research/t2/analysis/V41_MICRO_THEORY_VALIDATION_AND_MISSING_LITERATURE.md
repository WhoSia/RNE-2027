# T2 v4.1 — Parallel axes and physical parameter observability (2026-11-02)

## Executed contribution
Independent dimensioned IDM component (not yet linked into existing T2 engines); eight unit tests PASS locally. Github code `research/t2/microscopic/idm_reference.py` and `test_idm_reference.py`. Test examples: free acceleration positive, near stopped leader yields braking, speed floor zero, 70m/(4.5m+2.5m)=10 vehicle slots, receiving supply and invalid state exceptions. Executed source package SHA256 `b5d652d25977ae1a9e30651c61614ca4f2b6ef0da653d3fc1928f81ede15daf7`.

## Five coupled scientific axes
1. **Mechanisms:** dimensional IDM acceleration, safe gap, human response time; later lateral MOBIL, mixed fleet, slope, pedestrian phases and dwell times. Record what observations identify each parameter.
2. **Network mathematics:** movement-based conservation, link receiving supply, turn constraints, finite storage and spillback; distinguish from infinite point-queue max-pressure theorem.
3. **Control:** feasible stages, lost time, fixed/offset benchmarks and formal movement-pressure policy. Run equal arrival demand and action set with stage switch penalties.
4. **External validation:** field_v40 independently verifies timestamped counts, queue balance and day holdout. Add residual queues and travel-time distribution validation. No actual Gyeongnam dataset yet.
5. **Scale and translation:** pilot 3 junctions in Gyeongnam; another district or city as replication; multiple cities in Korea later. Monaco is only an external simulated stress benchmark.

## Physical IDM reference
For speed v, net gap s, leader speed v_l, desired speed v0, jam gap s0, headway T, accel a and comfortable braking b:
`a_IDM=a[1-(v/v0)^delta-(s*(v,v-vl)/s)^2]`,
`s*=s0+max(0,v*T+v*(v-vl)/(2sqrt(a*b)))`.
v in m/s; s,s0 in m; a,b in m/s^2. This continuous model is a reference component. Naive Euler position updates are NOT guaranteed collision free. The speed clamp is only a diagnostic helper, not a complete safe integration method. SUMO alternatives include Krauss, IDM, Wiedemann, EIDM, LC2013. See official SUMO documentation: https://sumo.dlr.de/docs/Definition_of_Vehicles%2C_Vehicle_Types%2C_and_Routes.html and https://sumo.dlr.de/userdoc/Car-Following-Models/ .

## Explicitly unproven
No empirical vehicle trajectory estimates, no parameter identifiability test, no signal safety constraints integrated, no physical microscopic model validation, no calibrated Korean corridor, no nationwide generalization. These are **planned** not executed.

## Literature receipt candidates (Drive author/title filename search; not exhaustive byte audit)
- Wagner & Erdmann (2025), SUMO’s Interpretation of the Krauß Model, DOI 10.52825/scp.v6i.2638.
- Ishaque & Noland (2009), Pedestrian and Vehicle Flow Calibration in Multimodal Traffic Microsimulation, DOI 10.1061/(ASCE)0733-947X(2009)135:6(338).
- Punzo, Ciuffo & Montanino (2012), Can Results of Car-following Model Calibration Based on Trajectory Data Be Trusted?, DOI 10.3141/2315-02.
- Microscopic Calibration and Validation of Car-Following Models – A Systematic Approach (2013), DOI 10.1016/j.sbspro.2013.05.050.
- Calibration of SUMO Car-Following and Lane-Change Models for Heterogeneous Traffic on Egyptian Two-Lane Two-Way Roads (2026), DOI 10.3390/su18147025.

Already in Drive: Kesting et al. (2007) MOBIL; Gipps (1981); Nagel & Schreckenberg (1992). Avoid duplicate intake.
