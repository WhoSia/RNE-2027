# T2 v0.7 — Gyeongnam Science Fair deliverable-first research charter
Date: 2026-10-31. Decision: **PIVOT SCOPE, not kill T2**.
This charter supersedes novelty-maximization as a scheduling priority, not
scientific integrity rules. Keep historical v0.2–v0.6 files intact.

## The actual project
Build, demonstrate, and validate a **Korean signalized intersection
turn-lane storage and spillback model**, with one defensible local-use
case and an actionable scenario comparison. A well-sourced adaptation
of established traffic models qualifies as the engineering baseline.
Do not claim a novel underlying traffic theory merely for implementing it.

### Core title (working Korean)
한국형 신호교차로의 좌회전 대기차로 길이 및 신호 운영에 따른
직진 흐름 저해 현상 모델링과 개선 시나리오 분석

## Minimum exhibition-ready outcome (MVP)
1. A single selected Gyeongnam/Changwon-style intersection geometry:
   through/turn lane layout, turn-pocket length, upstream approach
   length, phase sequence, cycle timings, and demand (observed if
   permitted, otherwise explicitly representative scenario).
2. Working visual model: time–space queue propagation, blocked pocket
   entry, spillback, and discharge. Conservation and lane occupancy
   invariants tested; **calibrated vs hypothetical** states explicit.
3. Scenario factorial: pocket lengths × turn ratios × phase offsets /
   leading-vs-lagging. Show throughput by movement, lost effective
   green, mean/max queue, spillback count/duration. Matched arrivals,
   repeated seeds, stable warm-up/measurement horizon.
4. Baseline comparison: at least one simple queue-capacity baseline,
   plus model ablations (disable spillback, disable history) to show
   what the more detailed model adds.
5. A practical recommendation scoped to the test intersection and
   observed/assumed inputs; physical feasibility and safety cautions.
6. Exhibit assets: diagrams of actual vs modeled lanes, model live
   animation or recorded trajectory, parameter sliders, graphs, method
   diagram, concise limitations.

## Small theory cherry on top (choose ONE only if supported)
A. A finite counterexample demonstrating why turn proportion
   alone can be insufficient; pair the histories by total arrivals
   but change within-cycle order; show the queue mechanism.
B. A storage threshold or critical ratio boundary with a
   derived approximation and a held-out simulation test.
C. A green lost-time accounting identity for a specified toy
   transition model, with conservation/phase proof.
Not required for the engineering MVP. Must not delay 1–5.

## Observability / sensors are SUPPORT, not a new topic
Use observation only to obtain/validate model variables:
- signal phase times -> traffic signal observation or official plans;
- stopline movement counts -> model output validation;
- queue length per cycle -> calibration of upstream supply and
  spillback mechanism;
- turn fraction -> demand input.
The previous observation-equivalence code is an optional detector
uncertainty diagnostic. It is **not** a required full classification
research programme, and no sensor hardware is required for T2.
If no permitted field data arrive, use explicitly synthetic scenarios
and report no field calibration.

## Practical 14-day executable work plan (relative workdays)
Days 1–2: choose one intersection geometry/proxy and freeze source
tables; implement geometry/config schema and phase diagrams.
Days 3–5: repair baseline simulator physics: spatial slots, lane-change
logic or transparent exclusion; add per-cycle queue/bay occupancy and
event logging, test and visualize.
Days 6–8: run 3-factor scenarios, negative-control and conservation
checks; summarize movement-specific outcomes.
Days 9–10: independent comparator (SUMO optional if easy; simple
analytical capacity/CTM mandatory); distinguish expected/measured.
Days 11–12: limited calibration to anonymized field aggregate data
if available; otherwise stress-test the synthetic assumptions.
Days 13–14: exhibition report, figures, video/demo, thesis/limitations
and one optional small proposition.

## Stopping rule and gate
DO NOT pursue another independent novelty, sensor observability,
inverse problem, or paper survey unless it changes a required
model parameter, mechanism, validation, or practical recommendation.
Timebox prior-art reading to implementing explicit source-derived
equations/parameters. The project succeeds when a reproducible,
physically interpretable Korean-style model and an evaluated
intervention comparison exist, not when the whole research domain
is new A-to-Z.

## Provenance of the scope correction
A past CUBE-REV Chat Archive around 2026-10-23 already called for
reusing proven algorithms and warned against excessive novelty
gating. R&E 2027's 2026-10-27 research charter had stronger
kill/pivot/novelty requirements suited to theoretical work.
The 2026-10-28 local field-relevance note already specified the
direct question: when left-turn queues accumulate between signals,
why can through vehicles fail to discharge during green?
This v0.7 explicitly prioritizes that original deliverable.

## Ownership
GitHub: code, tests, small reproducible configurations and manifests.
Drive: literature harvest, local field observation log, report and
presentation. Do not enable Actions; do not merge main automatically.
