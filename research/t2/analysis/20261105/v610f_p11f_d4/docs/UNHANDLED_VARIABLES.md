# T2 — 아직 못 다룬 변인 (2026-11-05 P11-F 상태 감사)

`NOT_MODELLED` means no validated implementation in the **integrated** production-grade vehicle engine; some fields have already been represented in separate contracts. `PARTIAL` means an isolated schema/parser/fixture exists but does not imply full behavior. The list is a research-scope taxonomy, NOT an exhaustive ontology of the world's roads.

## 01. 도로 토폴로지·지형
1. 고가/지하의 실제 종단고 곡선 — PARTIAL (선언된 layer만)
2. 종단경사에 따른 차량 동역학 — NOT_MODELLED
3. 횡단경사와 곡선 반경 — NOT_MODELLED
4. 다층 터널 합류와 분기 — NOT_MODELLED
5. 회전교차로·다지 원형교차로의 우선권 — NOT_MODELLED
6. 인터체인지·다이아몬드·클로버잎 — PARTIAL (방향 그래프만)
7. 비정형 5·6지 교차로의 실제 conflict zone — NOT_MODELLED
8. 신호 없는 교차로의 양보·정지 규칙 — NOT_MODELLED
9. 단속류·연속류의 전환 구간 — NOT_MODELLED
10. 좌·우측통행 지역 규칙 — NOT_MODELLED

## 02. 차로 기하·공간적 큐
11. 실제 차로 폭·측방 이격 — NOT_MODELLED
12. 실측 정지선의 3D 좌표 — NOT_MODELLED
13. 실측 보행자 횡단보도 다각형 — NOT_MODELLED
14. 연결부의 곡률·스플라인 — NOT_MODELLED
15. 좌회전 포켓의 저장상한 — PARTIAL (길이/footprint 상한만)
16. 우회전 포켓의 합류 및 포화차두시간 — NOT_MODELLED
17. 테이퍼·차로감소·병목 형상 — NOT_MODELLED
18. 버스전용차로·HOV 차로의 세부 운영 — PARTIAL (권한 선언만)
19. 주정차·상하차에 따른 차로 점유 — NOT_MODELLED
20. 차로별 대기열 충격파·차량별 위치 — NOT_MODELLED

## 03. 규제·시간 변동
21. OSM node-via turn relations — PARTIAL (엄격한 작은 부분집합)
22. OSM via-way 다중경유 회전제한 — NOT_MODELLED (명시적 미지원)
23. 복수 from/to 멤버가 있는 복합 규칙 — NOT_MODELLED
24. OSM conditional holiday·sunrise·school term — NOT_MODELLED
25. 도로 표지판의 시각·지역법적 우선순위 — NOT_MODELLED
26. 버스·택시·비상차·화물 예외의 완전한 위계 — PARTIAL
27. 가변차로 개폐 전 차량 완전 퇴거 확인 — NOT_MODELLED
28. 시간대별 일방통행과 주행방향 변경 — PARTIAL (선언된 일정만)
29. 차량 총중량·축하중·위험물 규제 — PARTIAL (총중량만)
30. 계절별 제한속도와 공사 임시 규정 — NOT_MODELLED

## 04. 미시 차량 동역학
31. 차종별 가감속·제동모델 — NOT_MODELLED (현재 연결 엔진)
32. 운전자 반응시간과 분산 — NOT_MODELLED
33. IDM·Krauss·Wiedemann 등 차량추종 — NOT_MODELLED
34. MOBIL 등 차로변경의 의사결정 — NOT_MODELLED
35. 비보호회전 간격수락/양보 — NOT_MODELLED
36. 대형차 내륜차·회전 swept path — NOT_MODELLED
37. 경사·노면마찰과 제동거리 — NOT_MODELLED
38. 오토바이 필터링·모터바이크 특성 — NOT_MODELLED
39. 트레일러·중량차의 종방향 동역학 — NOT_MODELLED
40. 자율주행·일반차의 혼합 반응 — NOT_MODELLED

## 05. 혼잡·차량 경로
41. 용량 예약 대신 실제 위치 기반 링크 점유 — NOT_MODELLED
42. 다차로 직진/좌회전 차로간 공유대기열 — PARTIAL (FIFO만)
43. merge/diverge의 실제 우선순위 — NOT_MODELLED
44. 수요 유입의 시간대별 연속 확률과 차종·차로 결합 — PARTIAL (합성만)
45. OD 수요 추정과 경로 선택 — NOT_MODELLED
46. 동적 경로 재배정·우회 — NOT_MODELLED
47. 도시 전체 gridlock 및 경계 차단 — NOT_MODELLED
48. 신호군과 링크 저장공간의 동적 충격파 결합 — NOT_MODELLED
49. 시뮬레이션 시작 전 기존 차량 상태 초기화 — NOT_MODELLED
50. 빈 링크·막힌 링크의 혼재와 중간 출입로 — NOT_MODELLED

## 06. 신호·우선권의 물리적 표현 (정책 최적화 동결과 구분)
51. 실제 SUMO active tlLogic와 WAUT/프로그램 전환 — PARTIAL (정적 구조만)
52. 황색 진입 가능의 법적·물리적 조건 — NOT_MODELLED (차량 엔진)
53. 적색 후 clearance/교차로 비우기 시간 — PARTIAL (컨트롤러 프로토타입만)
54. 보행신호·차량신호 충돌도 — NOT_MODELLED
55. 후행/선행 보호 좌회전 — NOT_MODELLED
56. 비보호 좌회전의 대향 차량 경로 — NOT_MODELLED
57. 무신호 교차로의 priority / gap acceptance — NOT_MODELLED
58. 철도 건널목 차단기와 열차 점유 — NOT_MODELLED
59. 교량 가동/터널 폐쇄 시 차량 대피 — NOT_MODELLED
60. 감응식 신호 검지기 설치·오탐·지연 — PARTIAL (센서 객체 프로토타입만)

## 07. 보행·자전거·대중교통
61. 보행자 공간 그래프와 횡단 경로 — NOT_MODELLED
62. 횡단보도 폭·보행시간 분포 — NOT_MODELLED
63. 보행자 우회전 충돌 및 양보 — NOT_MODELLED
64. 장애인 보행속도·접근성 — NOT_MODELLED
65. 자전거 전용교차로·대기 박스 — NOT_MODELLED
66. 킥보드·마이크로모빌리티 수요 — NOT_MODELLED
67. 버스정류장 승하차/정차시간 — NOT_MODELLED
68. 트램·버스 차로 공유 및 우선권 — NOT_MODELLED
69. 택시·배달차량 연석 이용 — NOT_MODELLED
70. 보행자 신호 호출 및 보행자 지연 지표 — NOT_MODELLED

## 08. 네트워크 데이터·좌표/정본
71. 실제 OSM 전체 PBF 원본 보관 — NOT_ACQUIRED
72. OSM 3D layer/bridge/tunnel의 정확한 geometry-to-lane 변환 — PARTIAL (별도 witness만)
73. OpenDRIVE elevationProfile / superelevation — NOT_MODELLED
74. OpenDRIVE junction laneLink / priority — NOT_MODELLED
75. CityFlow/SUMO의 완전 신호 프로그램 로딩 — PARTIAL
76. GPS 좌표계·투영·부호화 및 측량 오차 — NOT_MODELLED
77. 누락된 제한속도/차로 수 자동 보완의 신뢰도 — NOT_MODELLED
78. 자동 양방향 도로 변환 후 법적 방향 검증 — NOT_MODELLED
79. 세계 각국 도로표지·주행규칙 버전 관리 — NOT_MODELLED
80. 대규모 도로망 그래프 병렬 partition·memory budget — NOT_MODELLED

## 09. 실측 데이터·관측 인과성
81. Utah SPaT signalgroup→실제 회전/차로 매핑 — NOT_VERIFIED
82. BSM 차량 경로와 신호군의 시간·공간 결합 — NOT_VERIFIED
83. 진주 원본 교통량 바이트 및 정식 데이터사전 — NOT_ACQUIRED
84. 검지 통과량과 진입수요의 분리 추정 — NOT_MODELLED
85. 교통량 센서 검열·결측·표본 선택 편향 — NOT_MODELLED
86. 보정/검증 일자 독립성 — NOT_ESTABLISHED
87. 정체·대기열 실제 관측 레이블 — NOT_ACQUIRED
88. 실측 차종 분포·차길이·포화교통류 — NOT_VALIDATED
89. 신호 시각의 측정 오차와 clock drift — PARTIAL (전환구간만)
90. 현장 지연시간 ground truth와 모델 residual — NOT_VALIDATED

## 10. 환경·이상상황
91. 강우·적설·결빙/노면 마찰 — NOT_MODELLED
92. 안개·야간 가시거리 — NOT_MODELLED
93. 사고·공사·차로 폐쇄 이벤트 — NOT_MODELLED
94. 이벤트·휴일·축제 시 수요 급증 — NOT_MODELLED
95. 정류장/학교·병원 진출입 차량 집중 — NOT_MODELLED
96. 통신 지연·센서 고장·전원장애 — NOT_MODELLED
97. 임시차로·우회도로·비상복구 운영 — NOT_MODELLED
98. 산불/홍수 등 재난으로 인한 도로 단절 — NOT_MODELLED
99. 풍속·차량 동역학에 미치는 영향 — NOT_MODELLED
100. 고가·터널 환기·수용 인원/비상 통행 — NOT_MODELLED

## 11. 검증·수치적 정확성
101. 기존 P2 이벤트 인과성 완전 수리 — NOT_PROVEN
102. event-driven 새 모델의 P2 동등조건 검증 — NOT_PROVEN
103. 신호 시각·차량 완료시각 dt 수렴성 정리 — NOT_PROVEN
104. 차량 보존 외 기하학적 충돌 증명 — NOT_PROVEN
105. SUMO 네트워크 원본 raw seal + 실제 주행 — NOT_DONE
106. OpenDRIVE/OSM 네트워크의 거대한 실파일 부하검사 — NOT_DONE
107. 도시·국가별 랜덤 표본 도로형태 감사 — NOT_DONE
108. 접근제어 UNKNOWN 처리의 실제 법규 정확도 — NOT_VALIDATED
109. 원본/파생 데이터의 라이선스·시점 변동 감사 — PARTIAL
110. 장기간 교통수요의 외부 예측 잔차·holdout — NOT_DONE

## 12. 정책 트랙: 현재 잠정 동결
111. 일반적 다현시 최적화에서 feasible set 정확성 — FROZEN
112. 실시간 제어의 센서-차량 closed loop — FROZEN
113. 동적 OD 및 시간변동 제어 — FROZEN
114. 압력제어/감응제어/MPC 간 동등 예산 비교 — FROZEN
115. 보행자·버스·화물차 포함 다목적 최적화 — FROZEN
116. 회전차로 spillback 반영 정책 최적화 — FROZEN
117. 계산오차에 강건한 정책 인증 — FROZEN
118. 국가별 신호 운영 규칙과 안전한 후보 생성 — FROZEN
119. 재난 및 사고시 정책 전환 — FROZEN
120. 실제 도로 신호기와 연동(별도 승인/검증 전 불가) — FROZEN

### Critical model-boundary note
The newly implemented `WayGeometry.layer` is a **declared schematic level** only. An elevation difference has not been measured and cannot certify clearance. A strict planar segment intersection cannot detect endpoint touching or collinear overlap; a non-crossing result therefore is not full geometry certification. OSM relation `only_*` prohibits *other destinations only* within the supported simple relation subset; it is not an explicit permission to the selected destination. Regional default laws and OSM's unstated, implicit turning rules are absent.
