# RF10 — 첫 실측 데이터가 들어왔을 때 진짜로 돌아가는 연결부 (2026-11-24)

**상태:** 물리 CSI 수신 **0회**. 검증된 것은 수신 완료 후 ESP-CSI 형식 CSV를 **오프라인에서** 표준화하는 파서의 합성 테스트 3개, 그리고 RF05 기대 스키마와의 정적 대응이다. 교내 실제 무선 장치, 전파환경, 실제 차량 검지는 미검증. 이 파일은 새로운 학술 성과를 주장하지 않는다.

## 초심으로의 연결

RF-CURTAIN 원 정본 [README](README.md), [APPARATUS_AND_LABELS](APPARATUS_AND_LABELS.md), [PILOT_PREREG](PILOT_PREREG.md)는 T2의 핵심 질문을 '녹색 신호 중 차량이 방출되지 못한 원인'으로 정의한다. 자유 통과(free)/진입 수요 없음(no_demand)/좌회전 포켓(pocket)/하류(downstream)/동시 차단(both) 다섯 조건은 실험자가 설치한 **탁상 장치의 독립 참값 레이블**이지 실제 도로 사건의 인과 진단이 아니다. T2 자체 신호 정책 연구와 RF-CURTAIN의 물리적 관측 연구는 병렬로 유지한다.

## 선행연구: 신규성 강요하지 않고 재현 순서 보존

1. Won, Zhang & Son (2017), *WiTraffic: Low-cost and non-intrusive traffic monitoring system using WiFi*, ICCCN, DOI 10.1109/ICCCN.2017.8038380 — Wi-Fi CSI를 이용한 차량·차로 감지와 Earth Mover's Distance 활용은 **이미 선행기술**이다. 원문 자체의 완전한 재현은 현재 아님. 기존 [witraffic_emd_baseline.py](witraffic_emd_baseline.py)는 1차원 histogram EMD 수학 부분만 시험한다. 원 논문의 절차·데이터·지상진실 레이블 전체를 구현했다는 설명 금지. 연구 메타정보: https://digitalcommons.memphis.edu/facpubs/3343/
2. Espressif first-party CSI csi_recv — 공식 예제가 CSI_DATA CSV 열 `type,id,mac,rssi,...local_timestamp,...len,first_word,data`를 출력한다. ESP32-C5/C61은 새로운 CSI 포맷 차이가 존재하여 칩별 파싱 경로가 동일하다고 단정할 수 없다. [Official get-started](https://github.com/espressif/esp-csi/blob/master/examples/get-started/README.md), [Official csi_recv](https://github.com/espressif/esp-csi/blob/master/examples/get-started/csi_recv/main/app_main.c).
3. Pravin Varaiya (2013), *Max pressure control of a network of signalized intersections* — 정책 동역학의 기존 기준선이며 병목 원인 식별·관측가능성이 신호 최적화보다 선행할 필요가 있음을 상기시킨다. 기존 정책보다 우월하다는 실험 결과 없이 임계값 정책 개선 주장 금지. DOI 10.1016/j.trc.2013.08.014.
4. Apple (현행 Wi-Fi 프레임 보호) 및 IETF RFC9724 — 무작위화된 단말 식별자는 수동 추적의 정확성과 프라이버시 양쪽에서 문제다. 이 프로젝트는 **비협조 제3자 단말 탐지/식별 추적을 아예 하지 않고**, 직접 소유·허가된 실험 TX/RX 사이의 CSI만 다룬다. 따라서 MAC de-randomization 같은 별도 연구는 이 프로젝트의 구현 경로가 아니다.

## RF10 실제 코드 경로

- [rf10_esp_csi_trial_bridge.py](rf10_esp_csi_trial_bridge.py): Espressif CSV `CSI_DATA` 행을 로드, CSI signed I/Q pair에서 amplitude mean을 계산. malformed byte, length mismatch, 중복·역전 timestamp 및 `first_word_invalid`를 **실패 처리**한다. 여기서 가능한 칩별 인코딩/CSI 선별·calibration은 아직 검증하지 않았다. `first_word=1`은 단순히 버리지 않고 안전하게 멈춘다. 이는 공식 로그를 언제나 모두 수락한다는 주장이 아니다.
- 두 개의 구역 링크 1,2는 각각 **별도의 자체 TX/RX 장비**, 별도의 로컬 클록으로 CSV를 읽고, 수동 레이블 manifest에 있는 각 링크별 측정창 `start_us,stop_us`로 연결한다. 클록 동기화를 추측해 두 수신기의 microsecond timestamp를 합치지 않는다.
- 출력 필드: RF05 기존 [rf_pilot_evaluator.py](rf_pilot_evaluator.py) 필수 `trial_id,session_id,placement_id,trial_origin,label,ground_truth_source,quality,rssi_1_dbm,rssi_2_dbm,csi_1_amp_dispersion,csi_2_amp_dispersion`. 장치 MAC, 패킷식별자, 원 raw-I/Q, 원 packet timestamp는 **출력하지 않는다**.
- CSI feature `csi_#_amp_dispersion`는 한 실험창 동안 관측한 **프레임별 평균 subcarrier magnitude의 시간표준편차**다. 이미 정의된 RF05의 피처 이름을 채우는 **명시적 구현 선택**이며 원 논문의 feature 또는 물리 의미를 구현했다고 주장하지 않는다. 고정된 장애물을 시간변화만으로 탐지하기 어렵기 때문에 향후 static occupancy contrast가 반드시 필요하다.
- RSSI 각 링크의 패킷별 dBm 산술평균. 수신 패킷이 2개 미만인 링크가 하나라도 있으면 `quality=missing`으로 표시. 출력 trial 자체는 **버리지 않으며**, RF05 evaluator가 abstain하도록 한다. 단, 형식에 맞더라도 CSI phase, 장치별 AGC 보정, 클록 drift, 파워 소거/가려짐, 선택되지 않은 LTF 신호의 왜곡 등은 현재 검증 범위 밖이다.
- 시험 중 상충 레이블, 중복 reset ID, link별 겹치는 실험창, 없는/잘못된 timestamp, 임의 표현식 삽입 및 비정상 CSI 값은 fail closed. CSV의 `trial_origin=measured_authorized_lab`라는 문자열만으로 **독립 측정 출처의 정당성**을 증명하지 않는다.

## 실제 실행 전 필요한 사항

교사/장비 관리자 승인과 **기관 보유 ESP-CSI 지원 보드의 정확한 SoC·ESP-IDF 버전·실험장소 허가** 확보. 라디오가 출력하는 열/바이트 형식이 공식 예제와 정확히 맞는지 서면 확인. 우리 장비끼리 허가된 비공개 연구용 링크를 쓰고 **타인의 Wi-Fi 프레임 수집, MAC 추적, 외부 도로 송신·신호 제어를 하지 않는다**. 수동 독립 레이블과 장치 위치·세션 레이블을 결과 관측 전에 고정한다. 실제 데이터는 도착하지 않았으므로 아직 수집/성능 평가를 진행하지 않는다.

사용법(장비 데이터가 정식으로 준비된 이후에만):

```bash
python rf10_esp_csi_trial_bridge.py --link-1 own_link_P.csv --link-2 own_link_D.csv --manifest manual_truth_windows.csv --out anonymized_trials.csv --authorized-lab
python rf_crossed_holdout_evaluator.py --help
```

`--authorized-lab` 플래그는 운영자의 선언이지 실제 허가를 대신하지 않는다. 전체 RF05 holdout 규약은 [RF05_CROSSED_HOLDOUT_PREREG](RF05_CROSSED_HOLDOUT_PREREG_20261121.md) 준수.

## 오늘의 검증과 미완료

2026-11-24 기준 로컬 Python3.13: `python -m py_compile rf10_esp_csi_trial_bridge.py test_rf10_esp_csi_trial_bridge.py` 통과 및 `unittest` **3/3** 통과. 수치·원시 RF 측정 결과 아님. git commit은 실제 GitHub main, github-actions bot 사용 금지. 현재 RF 전통의 기술적 최고 단계는 **실제 허가된 CSI 프레임을 수집할 준비**이며 물리 시험은 시작되지 않았다.

**추가 필요:** 원본 공식 CSI 수신기 버전 확인, 측정창 수동/센서 독립 truth 고정, clock reset 처리, 포켓·하류 표지판을 실제로 구분할 만큼 배치된 링크의 selectivity, 기준선 RSSI vs CSI, 정지된 객체 holdout, 위치·시간 교차 holdout, RF 불확실성으로 인한 실질 T2 정책가치의 변화.
