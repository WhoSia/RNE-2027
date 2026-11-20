# 2026-11-21 — Research OS 00_INTAKE 교통신호 PDF 6편 입고·정독 대조

원천 폴더: https://drive.google.com/drive/folders/1MLtYh0pv8QUZDReYzRqjDrOjRkSJAD16
정본 폴더: https://drive.google.com/drive/folders/1D2M4LHcejREhlyp6vTd71xxLLx-6ldUP
원본 파일 ID는 그대로 유지하고 저자·연도·표제 규칙으로 개명한 뒤 10_PAPERS에 옮겼다. **정본 폴더 이동 결과와 메타데이터 재조회가 성공했음.** 문학 EPUB, NOMOS ZIP과 다른 주제 파일은 이 작업에서 옮기지 않았다.

| 확보 원문 | Drive ID | 판본과 관련성 |
| --- | --- | --- |
| Long, Li, Lei & Wang (2026), When Better Traffic Forecasts Fail to Improve Signal Control | 1xfbbwXdee0_wGBWxpEb-3uM_BdZB5FvL | arXiv 2610.06992v1. 예측 MAE 개선(약 4%)과 제어효과 불일치를 직접 분석. 미래정보 누출, 행동 자유도와 평가목적 불일치를 명시. 우리가 '정확도와 가치 불일치를 최초로 발견했다'고 주장할 수 없음을 확정. |
| Shafik & Rakha (2025), Real-Time Turning Movement, Queue Length, and Traffic Density Estimation and Prediction | 1LJpiI0hENPuBmWadMgIbUP9Fp_rqZAum | Sensors 25, 830; DOI 10.3390/s25030830. CV 궤적과 상류 검지기, 두 단계 Kalman filter로 회전류와 대기열 추정. 교차로의 관측량 융합도 선행. |
| Huang, Huang, Zhou & Cheng (2025), Integrated Optimization of Dynamic Lane Allocation and Signal Timing | 1vq5kKhQmejR1KgwDiH-wdjtdhLxXUYot | Transportmetrica B 13(1), 2474656; DOI 10.1080/21680566.2025.2474656. 2층 MILP/MIQP, 신호와 차로 배정 공동 최적화. 동적 차로 전환 횟수와 지연의 tradeoff를 논의. 약 19.08%는 해당 연구의 모형 대조이며 우리 결과 아님. |
| Zhang, He & Zhu (2025), A Hierarchical DRL-Based Method for Coupled Optimisation of Traffic Signals and Vehicle Trajectories | 1MhNfNlb1aW-E1ellJxmTi91PlhnuKnW4 | Transportmetrica B 13(1), 2481395; DOI 10.1080/21680566.2025.2481395. CAV·HDV 혼합 주행과 비동기 신호·궤적 최적화, D3QN 및 SUMO. 우리 단순 모형과 물리적·운영적 모델링 깊이 차이를 경고. |
| Zou, Zheng, Liu & Liu (2024), Integrated Optimization of Traffic Signals and Vehicle Trajectories for Mixed Traffic | 18TvETpNACzvhLwsTNp6KCm3qwjurf6lv | 보유 파일은 SSRN 4760700에 제출된 **사전공개본**(본문 2023.11 제출 표시, 2024 SSRN 공개). 동명 정식 저널 출판본은 TRC 169, 104884 (2024), DOI 10.1016/j.trc.2024.104884. 파일을 출판본으로 잘못 명명하지 않음. |
| Kasarla & Abhilash (2025), Dynamic Right-Turn Signal Control at U.S. Traffic Intersections | 1ks-ckNoSIzd8boMufG5yrq-x0YfO2NK5 | ICEAMST-2025 proceedings; DOI 10.1109/ICEAMST67459.2025.11335700. GBRT 예측 + fuzzy Q-learning; SUMO 단일 교차로. 본 연구는 좌회전 포켓 문제와 직접 대응하지 않아 **방법 비교 참고**로만 둠. |

## 우선순위와 연구 방향

1. **가장 직접적인 논쟁 상대: Long(2026)**. 실제로 미래정보가 시점상 사용 가능한지, 예측기 성능이 맞는 손실함수에 연결되는지, 선택 가능 행동이 있는지 구별한다.
2. **현장 입력의 현실성: Shafik & Rakha(2025)**. 회전류·대기열을 실측센서로 추정하는 것이 이미 가능하며, 관측 정확도와 정보 지연을 별도로 다루어야 한다.
3. **상위 모형의 범위: Huang(2025), Zhang(2025), Zou(2024)**. 실제 차로 배정, 주행궤적, 차량 유형과 운영 제약이 넓게 연구되어 있다. T2는 이들을 모두 새로 해결한다고 과장하기보다 좁은 인과 질문에 집중한다.

## 미보유 원장 판정 교정

- **보유로 전환**: Long et al.(2026) arXiv 2610.06992v1; Shafik & Rakha(2025) Sensors 25:830. 두 건은 11월 21일 00_INTAKE에서 실재 원문을 확인하고 정본에 승격했다.
- **이번 확인에서 아직 미보유**: Liu et al.(2024) TRC 104614, DOI 10.1016/j.trc.2024.104614; Wan et al.(2024) TRC 104643, DOI 10.1016/j.trc.2024.104643. 본 검색은 서가의 완전무결한 중복 파일 전수검증이 아니라 제목·저자·DOI 중심 실재 확인이다.
- **이미 보유**: Guo, Krylatov & Wang(2026) 상류 센싱 경계; Hidas(2005) 합류·직조 차로변경 현장 및 미시모형.
- **판본 추가 확인**: Zou et al.(2024) 학술지 출판본은 서지상 존재하나 현재 확보한 것은 SSRN preprint.

이번 6편은 소유한 원문에서 초록·모형 개요·결론 및 한계를 대조했다. 논문 수치와 주장은 제시된 실험 조건 안에서만 해석한다. 인용만으로 T2의 새 알고리즘·실측 효과를 증명하지 않는다.

## 단위 실행 결론

이번 입고는 K047 사용자 화면을 만드는 일을 정당화하지 않는다. 입력의 추적·위치·시점이 없는 화면은 발표 근거로 부적합하므로 **K047 HTML 재생기와 템플릿을 활성 브랜치에서 퇴역**시켰다. 새 원자료가 없으면 원인 판정은 미확정으로 둔다. 그 대신 교통신호 제어의 **결정에 충분한 정보**와 **정확한 모형을 넘어갈 수 있는 조건**을 독립 계산으로 검증한다.
