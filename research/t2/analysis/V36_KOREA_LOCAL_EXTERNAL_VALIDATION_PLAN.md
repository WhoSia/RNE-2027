# T2 V36 — Gyeongnam first, Korea generalization second

## Empirical-source discovery 2026-11-02
1. KTDB national transport DB offers road network, passenger/freight OD, road counts and explanatory thematic data via application: https://ktdb.go.kr/www/contents.do?key=203 . Regional OD data should not be equated to intersection turning counts.
2. View-T provides estimates of link volumes, average speeds and downloadable Level5.5 road network, along with API OD influence/path data: https://viewt.ktdb.go.kr/cong/map/moveNetworkDownload.do and https://viewt.ktdb.go.kr/cong/api/moveAPI.do?url=main . API access keys may require a request; inferred link data are not actual signal head observations.
3. Gyeongsangnam-do Changwon public count dataset metadata is recorded at https://data.edmgr.kr/dataView.do?id=data-gyeongnam-go_kr-15063931 . Check dataset vintage, count time unit and geography before use.
4. The RITHM Drive already contains Korea Expressway Corporation 2025 monthly/classified highway segment counts, file ID 1FZ6UtY50W6r6Fy6wgmDePHrfqK9foGpx. Read header fields: section, vehicle category, 12 months, annual average, prior-year average. This is highway segment aggregation, **not** urban signal timing or lane turn counts. Only reuse to exercise class mix and temporal aggregation pipelines, NOT to calibrate a Changwon signal intersection.

## Preferred empirical design
Pilot with one three-junction Changwon arterial, then replicate on a second Gyeongnam corridor (different urban pattern). Acquire verifiable lane geometry + link distances; signal stages/cycles and offsets; turning counts for AM/off-peak/PM; pedestrian crossing demand and bus stop activity; queue length and within-period travel time; use different weekdays for calibration vs holdout.

## Modeling goals
Hold known exogenous OD fixed. Compare feasible fixed-time, signal coordination and formal MP with same safety and phase constraints. Optimize network completed trips and vehicle-hours with pedestrian delay bounded. Search conditions where spillback destroys green progression. State source vintage and uncertainty, report sensitivity to demand, phase timing and geometric coding. Do not claim nationwide transfer from one Gyeongnam intersection. South Korea phase comes after multiple independent contexts.

## Readiness gate
As of 2026-11-02 no local city intersection turn count + phase + geometry dataset has been fully imported into executable SUMO in T2. Full local validation NOT PASSED. Monaco evidence is an external benchmark only.
