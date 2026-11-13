# 2026-11-13 — Domestic Data Join Feasibility Addendum

## Seoul signal / map / movement candidates (official provider metadata, NOT RAW bytes)

1. Smart-intersection 5-minute directional volumes:
   https://t-data.seoul.go.kr/dataprovide/trafficdataviewfile.do?data_id=20001
   Dataset schema CROSS_ID, DIR_CD, STND_DT, STND_TM, LTURN_VOL, RTURN_VOL, STURN_VOL, UTURN_VOL; no automatically proven signal controller link.
2. C-ITS daily historic signal-state CSV:
   https://t-data.seoul.go.kr/dataprovide/trafficdataviewfile.do?data_id=10384
3. Intersection MAP archive:
   https://t-data.seoul.go.kr/dataprovide/trafficdataviewfile.do?data_id=10144
4. Lane/maneuver MAP data API:
   https://t-data.seoul.go.kr/category/dataviewopenapi.do?data_id=10122
   Identifiers include itstId, laneId, permDrcCd and lanePermMuvrCn.
5. Signal-to-lane-connection MAP metadata:
   https://t-data.seoul.go.kr/dataprovide/trafficdataviewopenapi.do?data_id=10123
   Identifiers include itstId, laneId, laneCnncId, signlgroupCd and signlPermMuvrNm.
   A separate CSV archive exists:
   https://t-data.seoul.go.kr/dataprovide/trafficdataviewfile.do?data_id=10146

**Critical unresolved join:** smart-intersection CROSS_ID versus C-ITS itstId, signal-controller ID and temporal consistency, including possible different coverage networks. Same type of name or geography is not proof of one-to-one correspondence. APIs may require a key; do not invent one. Some older traffic signal APIs are scheduled for retirement on 2026-11-15; use provider replacement paths.

## Changwon / Gyeongnam evidence

Official Changwon city traffic-volume annual survey:
https://www.data.go.kr/data/15063931/fileData.do
The 2024-10-18 dated CSV is described as 25 rows, covering survey sites / bidirectional annual counts 2020–2024, with explicit blank fields when a survey was not conducted. **Not** a time-stamped turning-movement count plus signal plan. It cannot calibrate D50/D51 phase interaction at one-second resolution. Keep it as a possible local context/needs-assessment dataset, not a primary policy validation input.

## Actionable acceptance condition

For Seoul or Changwon to be promoted to the primary exhibition testbed, acquire **actual raw rows** and verify an intersection ID/time/turn-movement/phase/lane geometry join. Preserve the original bytes, file hash and public attribution. Catalog metadata alone remains HOLD.
