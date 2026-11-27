# 학생용 대응 실험 인수인계 — 2026-11-28
상태: 교사 검토용 초안. 실험 결과 없음. 기존 R3 모델의 관측 원장과 별도로 집계 재고의 검증 절차를 연습한다. 실제 도로나 신호기 조작은 하지 않는다.
## 준비와 역할
종이 토큰, 3단계 도착/서비스 카드, 기록지, 노트북. 학생 A는 규칙을 수행하고 학생 B는 실제 토큰 수와 기록을 확인한다. 역할 교대는 교정 파일에 기록하며, 평가 단계에서 참값 기록자가 정책의 최종 성과를 미리 보지 않도록 한다. 교사 승인 전에는 source=synthetic으로 연습만 한다.
## 기록 파일
paired_trial_manifest_TEMPLATE.json: 빈 배열, 교사가 승인한 실험 설계만 추가. paired_trial_records_TEMPLATE.json: 빈 배열, 실제 측정한 행만 추가. 두 파일에는 정답·예상 효과를 넣지 않는다. 각 manifest block: id/session/tapeId는 익명 식별자, split=calibration/evaluation, source=synthetic 또는 실제 승인 후 teacher_approved_tabletop, initial=초기 전체 토큰 수, budget=허용 관측 크레딧, arrivals/service=각 세 단계 도착 수/최대 이탈 수 배열, order=두 arm의 실행 순서. 동일 세션·테이프 및 동일 집계 스케줄의 split 중복을 허용하지 않는다. 합계 일치는 개별 움직임 일치가 아님.
각 기록: block,arm=fixed/candidate,order=1/2,stage=1/2/3,status=ok/missing/invalid/aborted,start,arrival,exit,end,credit. 실패행은 다섯 수치 null, 누락은 0으로 대체하지 않는다. 출발 재고에서 이탈한 뒤 도착을 더하는 집계 계약에 맞춘다. arm을 재실행하거나 제거하지 않고 실패 이유를 별도 원장에 남긴다. 양 arm에서 동일 테이프/초기 재고, 순서 사전 무작위화, 예산 상한 동일, 실제 사용량 별도.
## 실행
Node.js가 있는 PC에서 이 디렉터리에서 `node paired_trial_ledger.js`는 기존 합성 19 checks, `node paired_trial_ledger.js manifest.json records.json`는 입력 검증. 빈 template은 실험이 없으므로 거부하는 것이 정상. 결과의 COMPLETE_LEDGER_ONLY는 집계 원장 완전성일 뿐 검정 통과가 아니다. R3 이동별 모형 및 관측 swap 교정은 별도 r3/calibration.py와 독립 토큰 카드/라벨을 사용한다. 이 집계 연습을 R3 실험 결과로 섞지 않는다.
## 사전 합의
본실험 전 학생이 가설, comparator, 초기 조건, 비용 계산, 실패 처리, 효과 크기, 표본 단위를 직접 설명한다. 12개 pilot은 절차·분산 점검 제안일 뿐 confirmatory evidence 아님. 학생/교사 실제 실행, 독립 라벨, 세션 효과, 시간 정합성, 이동류별 검증 및 안전한 교실 범위는 아직 미승인/미실행. 수집 이후에는 원래 기록을 보존하고 수정 이력을 별도 보관한다.
