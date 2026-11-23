# T2 × RF-CURTAIN 2026-11-24 — 초심 복원, 원문 기반 재현, 센싱 장치 구현으로의 귀환

## 원칙: 무엇을 검증하는 연구였나

본 연구의 원래 물리 질문은 **'녹색 신호인데 차량이 방출되지 않는 원인을 관측으로 구분할 수 있는가'**이다. 진입 수요가 없는 상태, 직진 차량이 자유 통행하는 상태, 짧은 좌회전 포켓 진입부의 역류, 하류 저장 링크 포화, 두 병목 동시 발생은 전혀 다른 교통 현상이다. 이 원인들은 관측없이 '유효 초록시간 손실'이라는 하나의 수치로 묶일 수 있지만, 정책 반응은 같지 않을 수 있다.

2026-11-21 이전 공식 [RF-CURTAIN README](../../exhibition/rf_curtain/README.md)와 20261121 T2·RF-CURTAIN 연구사 Google Doc(1EBtlEcZJ5FCDgdqsmXOCLIJD-cVj8NVoTXZSB0zBxzw), 20261122 연구일지(1Zo0Z-Q50o3f7oLvOF-73vKOCQcDGLq5fynmGaStm0kA)를 직접 재조회해 복원했다. 아래 판단은 그 문헌에 명시된 목표와 후속 엔진 실험의 실제 한계를 연결한다.

## 현재 이탈한 지점

P136–P143은 30초·60초 패키지들의 사후 비용을 주로 비교했으며, 새 timestamp/route-label 조건에서 대기열 문턱의 정책 후회가 늘거나 조건 자체가 발동하지 않았다. 이는 실험군 자체에서 얻은 정당한 음성 결과이다. 다만 **현장에서 초록시간 손실이 생겼을 때 어떤 물리 원인이 우선인지 식별·보존 검산하는 기술**을 도입하지 않은 상태에서, 기존 시뮬레이터의 policy win률만 누적하는 것은 원래 질문으로부터 멀어진다.

상류 큐, 직진/좌회전 구분, 하류 수신/퇴장과 계측 가능한 packet-level 신호를 동일하다고 간주하지 않는다. 특히 같은 두 센서의 '움직임 변화'가 정지한 차량의 위치를 곧바로 식별하는 것은 아니다.

## 외부 선행연구: 독창성보다 충실한 기준선

1. Varaiya (2013), **Max pressure control of a network of signalized intersections**, Transportation Research C 36:177–195, DOI 10.1016/j.trc.2013.08.014: 차량/이동류 큐 압력, 공급제약, 안정성 기반선. 기존 RNE-2027 저장소는 이미 20261105 `paired_backpressure.py`와 `V31_PRESSURE_FAILURE_DIAGNOSTICS_AND_NEXT_TESTS.md`를 보유한다. 후자는 기존 비동등한 pressure heuristic이 fixed 대비 389 vs 368 completed로 실패한 사례를 기록한다. **Varaiya의 이론을 재현했다고 주장할 수 없으며, 기존의 비동등 정책 실패를 theorem 반례로 부르면 안 된다.** 필요한 후속은 명시적 movement pressure/feasible service, 종료/수신링크 용량, 동일 OD 물리 대응이다.
2. FHWA (2008), **Traffic Signal Timing Manual**, Ch 9: adaptive system에는 실제 정확한 탐지·위치·유지관리 문제가 필수. FHWA 2013 signalized intersections guide 및 ASCT measures of effectiveness는 차량/보행 신호, 대기열, 측정가능성의 독립 기준. 교통신호 최적화 전에 교차로별 인접 링크/검지기의 현실적인 관측을 모델링할 필요.
3. Won, Zhang & Son (2017), **WiTraffic** (ICCCN, DOI 10.1109/ICCCN.2017.8038380): Wi-Fi CSI 기반 교통량/차로 및 EMD 이용은 선행 문헌. RNE에는 이미 단순화한 [1D EMD baseline](../../exhibition/rf_curtain/witraffic_emd_baseline.py)이 존재하지만, 원본 field evaluation 재현 아님. 주제는 Wi-Fi 자체의 신규성이 아니라 우리가 정의한 특정 **포켓/하류 막힘 원인** 구분 여부이다.
4. Espressif 공식 `esp-csi` 및 `csi_recv`: 실제 ESP32에서 CSI packet extraction의 출발점이며, 최신 공식 예제 출력과 모델별 포맷 차이를 검증한다. 이 연구에서 승인된 교내 **자기 장비끼리 교환한 프레임**만 사용하며 제3자 단말 식별/패킷 스니핑은 금지한다. 공식 문서에 명시된 ESP32 `first_word_invalid` 선두 4byte와 신형 SoC의 다른 포맷을 일률적 parser라고 과장하지 않는다.
5. IETF RFC9724 (2025) 및 Apple wireless privacy: 무작위 MAC 주소는 수동 장치 추적을 불안정하게 만들고, 해당 ID 기반 추적은 프라이버시 우려가 크다. **T2·RF-CURTAIN은 장치 추적 사업이 아니라 연구자가 소유한 fixed RF link로 물리 장면의 채널 변화를 읽는 비영상 센서 실험**이라는 선을 유지한다.

## 실제 개발 — RF10/RF11

[RF10 CSI bridge](../../exhibition/rf_curtain/rf10_esp_csi_trial_bridge.py) 및 [test](../../exhibition/rf_curtain/test_rf10_esp_csi_trial_bridge.py)는 승인된 로컬 ESP-CSI CSV → 두 RF 링크별 패킷 진폭·RSSI → 독립 라벨이 부여된 리셋 trial → 표준 RF05 row로 연결한다. 버전별 CSI `first_word` 처리, CSV length and timestamp fail-closed, 결측 시 `quality=missing` abstain, identifer whitelist export, overlapping trial windows rejection을 구현했다. 실제 CSI 입력 0건; Python 국소 3개 unit tests만 통과.

[RF11 blind scheduler](../../exhibition/rf_curtain/rf11_blind_trial_schedule.py) 및 [test](../../exhibition/rf_curtain/test_rf11_blind_trial_schedule.py)는 3 sessions × 2 placements ×5 실험 클래스 ×10 resets = **300개 향후 물리 시행계획**을 독립 배정한다. 훈련 S1/P1,S2/P1 100개, frozen primary P2/S3 50, secondary 100, sealed P2/S1 reserve 50. 중요: 공개 seed를 쓰면 분석자가 정답을 재생할 수 있으므로 기본 secure random, 비공개 operator truth와 analyst blinded rows 다른 경로만 허용. 공개 seed 기반 초기 계획표는 **데모일 뿐 blind study에 사용 불가**.

2026-11-24 로컬 Python3.13: RF10/11 국소 **8/8 tests PASS**. 실제 무선 하드웨어 CSI, 도로 측정, 보행 포함 신호 안전성 또는 공식 SUMO exit parity 통과는 아직 전혀 주장하지 않는다.

## 연구를 둘로 나누되 분리시키지 않는다

**Track T — 교통 물리와 정책:** DLR의 공식 roadway lane/signal mapping 및 실제 정지선 차량 IDs를 먼저 확보하는 것을 진짜 게이트로 유지한다. SUMO XR3 E0e 개별퇴장 mismatch와 현장 lane-signal 매핑 HOLD가 해소되지 않았으므로 synthetic T2 결과로 실제 신호 제어를 정당화하지 않는다. 고정 신호·MaxPressure·CTM/대기열 선행 모델을 실제 구현/재현해도 연구 성과에 포함한다.

**Track E — 전람회 소형 실물 센싱:** 카메라 없이 물체가 같은 자리에서 **정지**했을 때도 P와 D 영역의 CSI가 구분 가능한가? 장치 위치, 반사물질, 세션이 바뀌었을 때 특정 원인을 여전히 분류할 수 있는가? **Wi-Fi가 기존 광학 차단센서와 비교해 추가 정보가 없다면 그 음성결과도 수용**한다. 판정은 각 클래스 confusion/macro-F1, abstention, unknown/false-cause, 레이턴시와 drift로 구성한다.

**Track Interface — 원인 식별에서 정책으로:** '어느 링크의 CSI가 이상한가'보다 먼저, **같은 RF 관측값이 다른 잠재 원인 상태에서 서로 다른 정책 비용을 유발하는가?**를 질문한다. 각 RF의 기여는 단순 분류 F1 개선이 아니라, 원인 구분 불가능성의 감소와 *실제로 측정한 오류확률* 아래의 정책 regret 감소로 나누어 검증한다. P143에서 가장 낮은 후회의 오프셋-only 규칙을 넘어섰다고 조기 주장하지 않는다.

## 독립 동료 과제/인계의 책임분리

연구일지에서는 독립 감사자를 **김세호**로 확인했다. 이번 사용자 메시지의 **김세환**이 동일인인지 확인되지 않았다. 따라서 누구의 명의로 제출할 새 원고를 대리 작성하거나 이미 동료가 장비 실험을 했다고 주장하지 않는다. 독립 소그룹에 맡기기 적합한 완전히 분리된 업무는 다음 세트이다: (A) 소유·승인된 ESP32 CSI 지원 여부 및 정확한 펌웨어 inventory, (B) RF10 출력에 대한 raw packet/clock/invalid-word/blank-field adversarial audit, (C) 학생이 아닌 **자체 실험장치의 사전 수동 물체 배치** 5종에 따른 RF11 300-trial 실행 가능성, (D) 분석자가 원본 truth 순서를 보지 않는지 검사, (E) RF05 session×placement holdout에서 RSSI와 CSI 비교 및 불확실한 class엔 abstain. 결과에는 실험자/검증자, 장비 모델, 버전, 독립 레이블, raw SHA, 통과·실패 여부를 남긴다.

**금지:** 공공도로 신호 변경, 학교/공용 무선망 제3자 프레임 수집, MAC 주소 추적, 타인 영상/자세 수집, 시험실 허가 없는 고출력 송신, K047 봉인 해제, 허위 실측값·원본 없는 성능 주장은 포함하지 않는다.

## 다음 연구 게이트

1. RF11 **비공개 정답 레이블** 소유자 확인 및 RF10의 실제 ESP32 1 packet I/Q 수신 가능 여부, 그때에만 물리 실험 시작.
2. RF10의 정적 물체를 과소검출할 수 있는 **time-dispersion-only** feature를 기존 무차원 수학 모델의 알려진 빈 장면 대비 magnitude-shift와 대조. 단 이 보정 결과를 CSI 실측처럼 부르지 않는다.
3. RF05 원래 300 physical trials and 2 hardware links test, frozen holdout. min-recall/macro-F1/missingness + optically measured ground truth paired comparison.
4. T2 기존 MaxPressure/CTM 선행 구현을 확인해 independent engine and real signal mapping mismatch부터 해결. 그 뒤에야 실제 관측을 투입한 정책 가치 분석.
