# P144 — T2·RF-CURTAIN 모든 주요 의사결정의 수치 감사 (2026-11-24)

## 계보와 판정 범위

20261121 RF-CURTAIN 원 설계와 RF05 blind holdout, RF10/RF11 실행본, P140–P143의 실패 및 현장·SUMO 동치성 미해결을 직접 대조했다. 이 문서는 오직 **T2와 RF-CURTAIN의 현재 실행·검증·연구 운영 의사결정 21개**를 평가한다. 사용자 연구 프로젝트 외부의 인사·예산 또는 법적 승인은 대리 결정하지 않는다. 점수는 **주관적 자원배분 지표(성공 확률이 아님)**.

## 평가식

모든 축 0~5. 
- I (0.30): 핵심 연구 질문인 **녹색 신호 무방출의 물리적 원인 식별** 및 정책 정보가치 관련성
- V (0.25): 반증가능성/독립적 원인 구분력
- F (0.20): 지금 준비된 도구에서 구현·재생가능성
- R (0.15): 데이터 누출·원인 오인·동치성 착각을 줄이는 정도
- C (0.10): 비용·소요시간 효율

`score = 20×(0.30I + 0.25V + 0.20F + 0.15R + 0.10C)`. 비교 단위는 이 연구에 관한 **추가 작업의 우선순위**이며 실험 성능이나 연구자의 능력은 평가하지 않는다. 프로그램용 점수와 결정은 [P144_DECISION_SCORE_LEDGER.json](P144_DECISION_SCORE_LEDGER.json)에서 재계산할 수 있다.

## 분기별 연구책임자 결정·반론

| 분야 | 선택·순위점수 | 왜 선택했는가 | 무엇이 판정을 바꾸는가 |
|---|---|---|---|
| 관측 품질 | 누락된 시행의 abstain 보존 98 | 성공적으로 측정된 것만 골라 분석하는 선택 편향 방지 | 누락 이유와 데이터 생성 과정을 사전 보고해야 진정한 실패율 |
| 연구 무결성 | 비공개 블라인드 배정 98 | 공개 seed는 분석자가 참값 순서를 복원할 수 있음 | 보호 디렉터리 자체가 공유 Drive 권한으로 노출되면 실패 |
| 측정 도구 | 공식 ESP-CSI 형식 검토 96 | 장치별 인코딩에 따라 RF10의 특징량 의미가 뒤집힐 수 있음 | 실제 보유 장비의 SoC/firmware와 원본 수신 출력 없으면 최종 판정 HOLD |
| 선행성 | 기존 원방법 복제 우선 95.5 | WiTraffic의 CSI/EMD, Varaiya의 MaxPressure는 기존 연구 | 원 논문 단계까지의 진짜 재현인지 확인, 부분 유사체면 그렇게 표기 |
| 물리 진단 | RF12 정지 점유 반례 94 | 시간분산 0이 정지 장애물 부재를 의미하지 않음 | 실제 CSI에선 환경 drift/AGC가 더 강하게 개입할 수 있음 |
| 대안 센서 | 1-link RSSI 기준선 93.5 | 저가 센서 대비 CSI 추가 가치 판단 | baseline에 유리한 쉬운 배치를 고르지 말 것 |
| 일반화 | 미사용 세션×위치 93 | 동일 환경 내 packet-level 랜덤 분할은 데이터 누출 | 주요 홀드아웃 P2/S3 고정, 시각/위치 공동 이동 |
| 통합 | RF10→RF05 실제 schema & missingness 92 | CSV 파싱과 evaluator가 일치해야 의미 있는 보고서 | 현재 RF10/11 국소8 + RF12 5 통과와 end-to-end는 다름 |
| 물리 실험 | 실제 기관 장비 재고·허가 90 | 호환 CSI 보드 유무를 추측해서 장비 구매/측정을 시작하면 안 됨 | 감독자·기관 장비 담당자 확인시 재평가 |
| 연구 무결성 | RF11 blind leak audit 89 | 공개 고정 seed 발견 후 수정, 기타 파일/권한 누출 감사 필요 | 실제 파일 접근권한·holdout 불변성 검증 |
| 교통 모델 | SUMO 개별 퇴장 parity 87 | 독립 물리엔진 불일치 중 정책 일반화 주장 불가 | 차량별 도착·정지선·받는 링크·퇴장 순서가 맞으면 실측 연계 우선도 상승 |
| 선행 정책 | MP/CTM 독립 모형 85 | 기존 V31의 heuristic 실패를 정통 MP 이론 반례라고 할 수 없음 | 운동·공급·이동류별 압력을 독립 구현해 정확한 조건 비교 |
| 임계값 튜닝 | P140형 임의 q≥14 재튜닝 38 | P140/P141 실패, P142 미발동; 다시 13,15 탐색은 overfit 위험 | 더 좋은 관측변수·외부 모형 검증 후에만 탐색 재개 |

## 반대역 검토: 핵심 반박 5개

1. **BUILDER:** RF10은 실제 공식 CSV 열을 수용한다. **SKEPTIC:** 열 이름이 같아도 `compensate_gain`과 신형 칩의 12-bit 포맷 또는 신호 보정에 따라 숫자 의미가 다르다. 공식 Espressif `csi_recv`는 ESP32-C5/C61 조건부로 12-bit unpacking을 수행하므로 **legacy signed 8-bit I/Q만 허용하는 현재 RF10은 모든 Espressif 장치용 범용 파서가 아니다**. 결론: 장치별 profile과 최소 1개 진짜 출력 전에는 hardware-ready CLAIM 금지.
2. **STATISTICIAN:** RF11은 300개 표본을 갖는다. **SKEPTIC:** 300은 앞으로 시행할 계획일 뿐 실제 관측 0이다. 또한 독립 단위는 raw CSI packet이 아니라 **물리적으로 다시 배치한 trial**, 도메인 단위는 session 및 placement다. 결과의 신뢰구간은 trial cluster를 고려해야 한다.
3. **PHYSICIST:** 시간분산 특징은 움직임을 측정한다. **SKEPTIC:** 정지한 금속 모형차량은 시간분산 0일 수 있다. RF12에서 빈 10, 정지15, 환경 drift15가 각각 일정할 때 특징분산 0이고, empty baseline 대비 평균차 5는 static과 drift 모두 같다. 이는 **구성한 수학적 반례**이지 RF 측정 결과 아님.
4. **POLICY:** RF 분류 정확도가 개선된다면 신호 제어도 개선된다. **SKEPTIC:** 다른 잠재 상태가 같은 RF 클래스값을 보이거나 두 상태의 최선 행동이 같을 수 있다. 실제 관측오류를 반영한 정책 후회까지 확인해야 한다.
5. **INDEPENDENT AUDITOR:** 신규성 점수는 낮다. **DIRECTOR:** 선행방법을 정확히 재현하는 교과 수준의 체계적 실험도 충분히 유효한 성과다. 저자의 선행방법을 새로 발명했다고 주장하지만 않으면 된다.

## 이번 구현: P145 RF12 정지 점유 반례

[rf12_static_occupancy_audit.py](../../exhibition/rf_curtain/rf12_static_occupancy_audit.py)와 [test_rf12_static_occupancy_audit.py](../../exhibition/rf_curtain/test_rf12_static_occupancy_audit.py)는 사람이 만든 4개 **스칼라 채널 세계**를 계산한다: empty 10/10/10/10, static 15/15/15/15, environmental drift 15/15/15/15, moving 10/12/14/16. 시간분산 empty/static/drift=0, moving=√5. 고정 empty와의 평균차 empty=0, static=5, drift=5. 따라서 static/drift가 단일 값에서는 완전히 식별 불가라는 **반증**을 제공한다. 이 스칼라 예시는 채널전파 법칙, 다중안테나 CSI, 측정 오차 등은 재현하지 않으며 수학적 존재반례만 말한다.

로컬 Python stdlib RF10 3 + RF11 5 + RF12 5 = **13/13 unit tests PASS**, 0개 새 실제 RF 측정, 0개 실제 T2/SUMO 시뮬레이터 실행. 엄밀하게 구분한다.

## 운용 게이트

- 공개도로 신호 제어/교사 허가 없는 시험/타인 Wi-Fi 프레임 포획 및 단말 ID 추적 금지.
- 기존 `main`만 사용하고 WhoSia 본인 기여와 독립 동료 성과를 구별. github-actions[bot] 미사용.
- Drive/Docs에는 날짜 20261124 기록, 원본 소스/결과 및 명시적 부정 결과를 함께 보관한다.
- 보유 문헌 직접 열람/초록 열람/원문 실험 재현은 구별한다. 이 작업에서는 Espressif 공식 예제와 드라이버 원문 및 WiTraffic 서지를 확인했으며 WiTraffic 논문 전체 정확한 절차를 새로 돌린 것은 아니다.

### 출처
- 공식 CSV 및 칩별 구현: https://github.com/espressif/esp-csi/blob/master/examples/get-started/csi_recv/main/app_main.c
- 공식 ESP32 invalid word: https://docs.espressif.com/projects/esp-idf/en/release-v5.5/esp32/api-guides/wifi.html
- WiTraffic 서지 및 EMD: https://digitalcommons.memphis.edu/facpubs/3343/
- 2025 *Time Matters*: https://openreview.net/pdf?id=TZqcUbpQGU
- 2026 OpenCSI 공개 설명: https://arxiv.org/abs/2607.26665
