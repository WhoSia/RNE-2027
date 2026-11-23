# 외부 심사 2차 실험 원장 (XR1–XR5)
실행: PYTHONPATH=research/t2:research/t2/analysis/20261123:research/t2/analysis/20261122:. 에서 각 스크립트 실행 (저장소 루트 기준).
| ID | 스크립트 | 결과 | 비고 |
|---|---|---|---|
| XR1 | xr1_split_receiver_falsifier.py | XR1_RESULT.json | 공유/분리(동일 시계)/분리(좌회전 자유) 하류 링크. 재실행 결과가 최초 실행과 수치 동일(상태·prereg 라벨만 개명) |
| XR2 | xr2_queue_model.py, xr2_queue_model_test.py | XR2_RESULT.json | T2 코드를 가져오지 않는 독립 FIFO 대기행렬 모형 |
| XR3 | xr3_sumo_parity.py | XR3_RESULT.json | SUMO 1.28.0 동치 검증: E0e(퇴장 시각) 불일치 → 정책 부호 비교 금지 |
| XR4 | xr4_frontier_scale.py | XR4_RESULT.json | P126/P127 경계 셀의 64기록 확대 |
| XR5 | xr5_threshold_prediction.py | XR5_RESULT.json | 사전등록한 저장 임계 예측: 규칙 기각됨 |
엔진 변경: research/t2/split_receiver_v1.py(신규), dual_lane_v11.py(선택 필드 receiver_split, receiver_split_left_free; 기본 경로는 바이트 동일), test_split_receiver_v1.py(6개).
회귀: 저장소 루트에서 PYTHONPATH=. pytest research/t2/test_*.py → 280 통과, 1 실패(test_physical_checkpoint_measurement_stress::test_zero_noise_is_identity). 이 실패는 내 변경 없이도(stash 상태) 동일하게 발생하는 기존 실패.
