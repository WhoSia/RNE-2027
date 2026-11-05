# P11-R / D16 research-track decision (2026-11-05)

Previous user doctrine from Drive chat archive 20261104.md: policy P12 remains FROZEN because its ranking may change when a more faithful traffic simulator and observational data arrive. Existing P12-A/B preserved. Only thought experiments, formalization, and unexecuted proposal sketches permitted.

Two distinct outputs from shared traffic-simulation infrastructure:
- Exhibit: finite road storage, pedestrian crossing occupancy, and queue spillback lead to prediction errors in simplistic models. Show concise physical cause, direct observations, matched SUMO comparison, uncertainty and reusable demonstrator. Not an optimization or controller project.
- Journal: timestamp causal consistency, discrete event semantics, finite-capacity modeling and error diagnostics; separate theoretical claims and baselines. Later policy ranking stability is idea-only and NOT an executed experiment.

Current development: a standalone finite-resource event scheduler, deterministic FIFO queue, explicit resources, class conflict graph, conservation and no-backdating assertions; 8/8 synthetic tests. It is NOT integrated into v6.10-N, P10 original is NOT replayed, and there is NO independent source-data or SUMO validation here. FIFO may induce spurious head-of-line blocking; fixed duration, no positions or car following.

Competition prior-art links:
- Official 2016 prize '운전자 맞춤식 신호등 구현을 통한 교차로 교통사고 감소 방안 연구': https://www.science.go.kr/mps/1079/bbs/423/moveBbsNttDetail.do?nttSn=27230
- Official 2002 prize '대기시간 최소화를 통한 교통신호 제어 최적화 시스템 구현에 관한 연구': https://www.science.go.kr/mps/1079/bbs/423/moveBbsNttDetail.do?nttSn=21997
- Official 2025 student PM prize moving noise/Doppler cancellation prototype: https://www.science.go.kr/mps/1079/bbs/423/moveBbsNttDetail.do?nttSn=47783
- Gyeongnam 2026 68th competition result: https://gnse.gne.go.kr/gnse/na/ntt/selectNttInfo.do?nttSn=3033701
- National exhibit rules and exclusion: https://www.science.go.kr/mps/1078/bbs/157/moveBbsNttList.do

***Check overlap and publication eligibility with organizers before public exhibition manuscript, demonstrations or journal preprint.***

Next gate: get untouched engine, raw observations and independent SUMO; never treat synthetic tests as field findings.