# R&E 2027 T2 — 신호안 최적화와 관측의 가치

DLR-UT K047의 동쪽 접근로 실측 재생, 합성 교차로의 정확한 신호안 탐색, D51 관측 불확실성 실험을 재현한다. Python 3.11 이상과 표준 라이브러리를 사용한다.

## 재현

```sh
python -m unittest -v
python experiments.py timing results/timing.json
python sensing.py results/predecision_sensing.json
python experiments.py optimize results/optimization.json
python cycle_sensitivity.py results/cycle_sensitivity.json
python field_replay.py /path/to/prior-t2-dlr-root results/dlr_replay.json
python field_scenarios.py /path/to/prior-t2-dlr-root results/field_scenarios.json
```

실측 재생에는 기존 연구에서 사용한 `day/dayHHMM_signals.csv`와 `week1/wide/HHMM/daylight_crossings.csv`가 필요하다. 출력에 입력 SHA-256을 넣었다. 좌회전과 직진의 이동류는 출구로 분류했으므로 데이터는 사후에 확인된 관측 코호트다. 기존 전처리의 지도·차량 원자료·검지선 규칙은 앞선 1주 차 패키지에 기록했다. 이 ZIP에는 차량 ID와 궤적 원자료가 없다. 지정 홀드아웃 18:00–18:30 UTC는 열지 않았다. 시간 측정은 동일 실행에서 얻은 예시이며, 결과의 비용·계획·평가 수가 재현 기준이다.

## 목적함수와 정답의 범위

시각 t 직후 모형 안에 남은 각 이동류 인원·차량 수에 가중치를 곱해 합산한다. 종료 시 잔류에 추가 비용을 부과한다. 기본에서는 차량과 보행자의 가중치는 1이고 잔류 개체당 60을 더한다. 직진, 보호 좌회전, 교차 방향 직진, 보행의 네 호환 단계에 단계별 3초 전이와 1초 출발 손실을 가정한다. 신호 밖 각 이동류에 수용 한계와 별도 방출 달력을 둔다. 상류 진입 버퍼와 보행 대기열은 무한으로 둔다. 전이는 단일 무방출 구간으로 모델링했다. 별도 황색·전적색·보행청소, 우회전, 실제 보행 최소시간, 하류 공유 차로는 구현·보정이 남아 있다.

실행은 현재 후보의 완료된 시나리오 점수, 누적 대기열 비용과 이동류별 완화 모형을 이용한다. 완화 모형은 공용 FIFO와 저장 한계를 풀고 동일한 방출 기회에 각 이동류를 가장 일찍 통과시킨다. 각 이동류의 k번째 실제 통과보다 완화 모형의 k번째 통과가 늦어질 수 없으므로 양수 가중치 및 잔류 페널티 아래 비용 하한이 된다. 하한이 현 최선보다 엄격히 클 때만 후보를 버려 동률 규칙을 보존한다. 특정 시나리오의 완전정보 최적 비용을 뺀 경우에도 하한 성질은 유지된다. 동일한 유한 후보군에서 전수 행렬로 확인했다.

## 해석

- 고정 84초 최악 비용 기준안 31,131, 정확 최적 29,403. 교차방향 집중·저수요에서는 일부 악화했다. 후회 최소화는 별도 최적해이며 최악 후회 3,446.
- 실측 재생의 적합과 평가를 시간 블록별로 나눴다. 2.05초 표본 공백 허용은 평가 오차를 본 뒤 시행한 민감도 분석이다. 같은 녹색 상태 표본 사이를 이어 붙인 가정이며 재평가 코호트의 판정에 그대로 고정해 적용할 계획이다.
- 실제 동쪽 도착과 합성 나머지 접근로를 조합한 실험은 관측 시계열에 대한 스트레스 테스트다. 독립 교차로 검증, DLR 현시안의 현장 개입 효과, 실측 병목의 인과 추정과 구별한다.
- 관측 계획에서 집계는 주어진 조건이다. 의사결정 이후에 걸치는 집계도 있으므로 실제 적용에서는 당시 알 수 있던 집계 또는 예측으로 교체해야 한다. 신호 전 공통 적색은 두 정책의 개입 시점을 맞추기 위한 실험 조건이다.

## 검증 기록

- `results/timing.json`의 예제에서 324개 호환 유입열의 선행−후행 차이는 −43~+65 차량·초다. 일부 구간의 미검출 수를 허용하면 972개, −171~+81이다. 시작 큐를 네 상태로 허용한 별도 계산에서는 1,296쌍, −432~+83이다.
- `results/predecision_sensing.json`의 세 개입 시점과 125개 집계 조합 중 65개가 모호했다. 이동류를 사전에 두 번 관측해 후회를 1 차량·초 줄인 경우는 4개였다. 시간순으로 적응할 수 있어도 최적 고정 관측을 이긴 경우는 0개였다.
- `results/cycle_sensitivity.json`에서 세 주기 2,442안을 함께 최적화했다. 이번 합성 환경에서는 네 목적 설정 모두 72초 후보가 이겼다. 기본 비용 25,969이며, 잔류 비용과 평가 시간 변경 시 최적 오프셋은 달라졌다. 주기가 달라지면 1시간당 전이 손실과 녹색 시간 비율도 달라지므로 주기 길이 단독 효과는 추정하지 않았다.
- `results/dlr_replay.json`에서 적합에 사용하지 않은 세 블록의 직진 코호트는 137대다. 1.2초 기준과 2.05초 민감도에서 녹색을 선택할 때 2.05초 가정의 평균 절대오차는 4.92, 4.08, 6.30초다. 실제 통과시각은 평가에만 썼지만 이동류·완전추적은 사후 필터에 들어갔다.
- `results/field_scenarios.json`의 세 시간대×네 난수 시나리오에서 훈련에서 고정한 85초 계획은 초기 기준 계획보다 목적함수를 0.87~19.74% 낮췄다. 12개 경우는 같은 현장 3개 블록을 공유하며 동쪽 밖의 수요는 합성이다.

## 신호 효율 후속 실험

`EFFICIENCY_LOOP.md`에 가설, 실행 결과, 다음 분기를 기록했다. `DATA_ACCESS.md`에 공개 신호 자료와 국내 문의 초안이 있다.

```sh
python policy_screen.py /path/to/prior-t2-dlr-root results/policy_screen.json
python policy_deep.py /path/to/prior-t2-dlr-root results/policy_deep.json
python dlr_green_audit.py /path/to/prior-t2-dlr-root results/dlr_green_audit.json
python objective_frontier.py results/pedestrian_frontier.json
python travel_stress.py results/travel_stress.json
python sensor_grid.py /path/to/prior-t2-dlr-root results/policy_deep.json results/sensor_grid.json
python policy_replay.py results/policy_deep.json results/schedule_transfer.json
python start_sensitivity.py results/policy_deep.json results/start_sensitivity.json
python sind_signal.py downloaded_signal.csv results/sind_tianjin_signal.json --site tianjin
```

## 직진 방출 기회 진단

[포켓·하류 용량을 교차한 합성 실험](GREEN_SERVICE_DIAGNOSIS.md)은 직진 차량이 없던 기회, 포켓 앞 공유 FIFO 대기, 하류 만차, 두 조건의 동시 관측을 구별한다.


## 2026-11-21 SF-01 — 결정 시점 정보·선행연구 재사용

[강건 정보 융합 연구](../analysis/20261121/sensor-fusion/FINDINGS.md) / [입력 가정과 수식](../analysis/20261121/sensor-fusion/LOSS_AND_OPTIMIZER.md) / [검증 기록](../analysis/20261121/sensor-fusion/VALIDATION_RECEIPT.md).

```sh
python -m unittest -v test_sensor_fusion_decision test_sensor_cost_policy test_sensor_fusion_frontier test_two_stage_queue_estimator
python sensor_fusion_decision.py ../analysis/20261121/sensor-fusion/robust_value_grid.json
python sensor_fusion_frontier.py ../analysis/20261121/sensor-fusion/sensor_frontier.json
# In research/t2 (NOT this directory):
python physical_transfer_screen.py analysis/20261121/decision-time-gate/physical_192_runs.json
```

마지막 명령은 실제 셀 물리모형 **192회 실행을 위한 재현 경로**이며 이번 작업에서 실행 완료되지 않았다. 결과가 생성되기 전까지는 검증 완료나 교통 성능 향상으로 인용하지 않는다. 칼만 추정은 Shafik & Rakha의 방법을 단순화한 예시이지 그 논문의 적응형 2단계 필터 재현이 아니다.
