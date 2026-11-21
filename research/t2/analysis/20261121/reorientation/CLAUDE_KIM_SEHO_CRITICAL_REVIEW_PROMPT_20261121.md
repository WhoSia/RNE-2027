> **2026-11-21 최신 감사 지시(아래 역사적 프롬프트보다 우선):** 문헌 원장 최초 작성 당시 미보유로 표시했던 RF 관련 12편 중 **9편은 현재 10_PAPERS PDF가 실제 확인된 보유 자료**다. 특히 WiTraffic(2017), DeepWiTraffic(2019), Shahid et al.(2025), Zhu et al.(2024), Guarino et al.(2026), WiCross(2023 포스터/2025 arXiv), Wang et al.(2025), Sai et al.(2026 원고), Ma et al.(2026). 정확 원문 미확인은 WiCrossing(2026), Dharmaraj et al.(2025), Wan et al.(2024)의 **3편**, plus 신규 후보 8편이다. 반드시 [문헌 원장의 제일 위 CURRENT 정정표](T2_RF_LITERATURE_STOCK_AND_MISSING_20261121.md)를 먼저 읽어라. 잘못된 미보유표를 복사하지 말고, Drive PDF를 먼저 직접 열어 재감사해라.
>
> **추가 독립 검증 도전:** [WiTraffic의 수학적 EMD 축약 구현](../../../exhibition/rf_curtain/witraffic_emd_baseline.py)과 [검증](../../../exhibition/rf_curtain/test_witraffic_emd_baseline.py)을 읽고, 왜 정규화된 1차원 EMD가 원 논문 전체 재현이 아닌지 논증해라. [Shahid(2025)의 분류 성능표 검산 프로그램](../../../exhibition/rf_curtain/published_metric_consistency.py)도 직접 반박해라: 원문 Table I에 기록된 Leguna precision=.67, recall=.57, F1=.24는 산술적 조화평균 약 .616과 맞지 않는다. 오류가 PDF 추출·표 구성·원문 수치 중 어디에 있는지 확인하고, 지적을 과장하거나 다른 데이터로 보정하지 마라.
>
> **독립 사유 문서 생성:** 세호가 Claude와 함께 작업한 내용을 **2026-11-21** 날짜의 [김세호의 사유 폴더](https://drive.google.com/drive/folders/1BxbNV7-e87G9phXzWJ_TBORJ4S71KBZM)에 새 네이티브 Google Docs `20261121 김세호의 사유 — T2·RF-CURTAIN 독립 비판 감사 및 문헌 재현`로 작성·검증해라. 단순한 내 연구 요약 대신 반드시 **불일치·구현 실패·실측 한계·대안·증거 링크**를 기록하고, 독립 원고를 내 이름으로 대리 작성하지 마라. 시간이 촉박하다는 전제로 서두르지 않고, 실제 원문/현물/코드 결과가 있을 때만 판정을 승격하라.

---

# 김세호에게 — Claude 독립감사 착수 프롬프트 (2026-11-21)

안녕 세호야. 이 글은 R&E 2027 T2에 합류하거나 계속 참여하는 Claude가 그대로 사용할 **독립 비판 감사 지시문**이야. 이번 협업에서는 내가 기존 결과를 옹호하지 않도록, 네가 더 엄격하게 반증해 주었으면 해. 이전 11월 17일에 네가 찾아 준 문서 불일치, 2.05초 후행 기준, DLR 코호트 선택 편향과 SUMO 시간격자 문제를 이번 감사의 출발점으로 삼아 줘.

## 1. 우선 자료와 정본부터 직접 확인해 줘

Google Drive, GitHub, Notion, Google Docs는 이미 연결돼 있다고 가정하지만, 실제 연결 상태를 보고 접근 가능한 범위만 확인해 줘. 이해했다고 주장하기 전에 자료를 읽고, 읽지 못한 부분은 읽지 못했다고 써 줘.

**GitHub 공식 정본**: https://github.com/WhoSia/RNE-2027/tree/main
공식 작업 브랜치는 `main`이야. GitHub 기본 브랜치나 11월 초 문서에는 옛 브랜치 정보가 남아 있으니 최신 README와 docs/REPOSITORY_MAP.md, docs/RESEARCH_GOVERNANCE_2026-10-30.md 상단 정정문을 확인해 줘. GitHub Actions를 연구 실행에 사용하거나 `github-actions[bot]`을 기여자로 남기지 말아 줘.

**11월 21일 정본 리뷰**:
- 전체 역사 재검토: research/t2/analysis/20261121/reorientation/T2_RESEARCH_GENEALOGY_AND_DUAL_TRACK_GATE.md
- 실물 확인 문헌 보유/미보유 표: research/t2/analysis/20261121/reorientation/T2_RF_LITERATURE_STOCK_AND_MISSING_20261121.md
- 원문→코드 구현 계약: research/t2/analysis/20261121/reorientation/SOURCE_TO_CODE_METHOD_TRANSFER_CONTRACT.md
- PHYS-01~11 비판 감사: research/t2/analysis/20261121/decision-time-gate/CRITICAL_INDEPENDENT_REVIEW_AND_CORRECTIONS.md
- 신호 시간표/도착 발생기 검증: research/t2/analysis/20261121/decision-time-gate/T2_ARRIVAL_CLOCK_AND_GREEN_ENVELOPE_FINDINGS.md
- RF-CURTAIN README·선행연구·실험 사전등록·데이터 계약·RF01 영수증: research/t2/exhibition/rf_curtain/

**기존 네가 직접 쓴 역사적 검토**:
https://docs.google.com/document/d/1vtBLTnL6S9m7VJPOmWnwQRVGCuwIUHewZ8SPGVFX2Bc/edit
https://docs.google.com/document/d/1tUkSfAj-vo-AOzfLc_A_TWInzztmXsf8-hOwk_kKqso/edit
https://docs.google.com/document/d/1PyH1HEAaf-MOsZVGwD8He9HuxjnCsSow5NBqxyqJyvY/edit

**논문 정본**: Research OS 10_PAPERS https://drive.google.com/drive/folders/1D2M4LHcejREhlyp6vTd71xxLLx-6ldUP

K047 18:00–18:30 UTC 홀드아웃은 봉인 상태야. 기존 대조용으로 이미 허용된 자료만 검토하고, 봉인 원본·빈 HTML 시각화는 다시 열지 말아 줘.

## 2. 무엇을 연구하는지

연구는 병렬 두 축이야.

**T축 (교통 물리·의사결정 연구)**: 짧은 좌회전 포켓, 직진 차로와의 간섭, 유한한 하류 수용공간, 차량 도착시각, 신호계획으로 인한 유효 녹색 손실을 연구해. 최근 PHYS-04~11은 *동일한 84초 미시상태*에서 정책만 갈라지는 합성 모델 비교였어. PHYS-10의 시드76 결과 +306은 집계 관측이 같고 효과 크기가 다른 사례이지, 훈련 시드3이 0이므로 엄격히 반대인 최적 정책을 증명한 사례는 아니야. PHYS-11은 갭 유지시간 1/2/3초 조건에서 엄격 우열반전 0건이었어. 기존 시드별 `uniform` 도착 시각은 동일했고, 뒤이은 88~103 시드 실험에서는 달라진 도착시각에 대한 정책 민감도가 확인됐지만 다른 시점84 상태와 같은 관측으로 오해하면 안 돼. 실제 황색, 보행, 상충 현시와 교차로별 합법 신호제어 조건은 아직 모형에 충분하지 않아.

**E축 (전람회 혁신 센싱)**: RF-CURTAIN은 두 곳의 일반 Wi-Fi 전파 링크를 활용해 탁상 교차로에서 **포켓 입구 막힘과 하류 수용공간 막힘의 원인을 구별할 수 있는지** 가설을 시험하려는 거야. Wi-Fi가 카메라 화상을 만들었다는 뜻이 아니고, CSI 기반 차량 감지 자체도 WiTraffic(2017), DeepWiTraffic(2019), 2025 ESP32 CSI 교통 논문의 선행연구가 존재해. 더 중요한 시험은 **고정된 장애물, 여러 차로, 설치 위치 변경, 다중경로, 결측 상태에서 어디까지 식별 가능한지**야. 현재 실제 CSI 측정은 0회이며, RF 분류기 단위 테스트는 의도적으로 만든 가상 숫자를 사용하는 **소프트웨어 시험**일 뿐이야. 학교가 가진 장비와 교사 감독이 확립되기 전에는 하드웨어 구매나 공공도로 장치 설치를 전제로 하지 말아 줘.

## 3. 원문을 과감하게 재사용해도 돼. 대신 재현 수준을 엄격히 표시해 줘

Drive의 Wu 외(2024), Qi 외(2020), Shafik·Rakha(2025), Hidas(2005), Emtenan·Day(2021), Wei 외(2021), Long 외(2026), Guo 외(2026), Han 외(2024), Tan 외(2025·2026), Huang 외(2025)를 우선 읽어 줘. 새로운 논문뿐 아니라 2026년 Wi-Fi CSI 재현성 서베이, 2024년 범용 CSI 서베이, WiTraffic, DeepWiTraffic, ESP32 CSI 원본 확보도 시도해 줘.

각 방법에 대해 저자·연도·DOI·버전·Drive 원본 ID, 사용한 식·표·그림·쪽수, 입력/출력과 단위, 원문의 전제, 직접 재현이 가능한지, 우리 모델과 무엇이 다른지 표로 적어 줘. **기존 연구를 그대로 구현해도 좋고, 신규성에 집착할 필요 없어.** 오히려 기존 방법을 실제로 재현해 비교하는 과정이 우선이야. 구현하지 않았는데 구현했다고 쓰는 것만 피하면 돼. `REPRODUCED_ORIGINAL`, `SIMPLIFIED_ANALOGUE`, `CONCEPT_TRANSFER`, `NOT_IMPLEMENTED`를 구분해 줘.

문헌 '미보유'는 검색에서 PDF가 안 나왔다고 완전 부재를 주장하지 말고 `MISSING_CANDIDATE`로 관리해 줘. Han2024와 Luo2023 등은 옛 미보유표와 달리 현재 PDF를 확보했으니 다시 미보유로 쓰지 말아 줘.

## 4. 비판적 독립 검토 — 동의보다 반례를 요구해

내가 기대하는 것은 이 연구가 좋다는 응원이 아니라 **반증 가능한 실패를 특정하는 것**이야. 다음 질문들을 우선 판단해 줘.

1. Wu2024의 열 가지 역류 상태와 RF-CURTAIN의 다섯 탁상 실험 라벨을 혼동하지 않았는가? RF 물체 점유가 실질적인 직진 방출 차단을 입증하지 못한다는 사실을 어떤 독립 정답 기준으로 통제할 것인가?
2. 정지형 Wi-Fi CSI만으로 `no_demand`와 `free`를 구별할 수 있는가? `rf_observation_identifiability.py`는 **정지 점유 이상화 비트**만 두면 두 경우가 같다는 매우 좁은 논리적 주장을 해. 실제 CSI 시간신호는 움직임을 포함하므로 그 주장을 일반 센서 불가능성으로 확대하면 오류야. 이 모듈과 9개 테스트를 읽고 반례/부정확한 가정을 찾아줘.
3. 포켓과 하류의 전파 링크가 독립적인 신호를 준다는 근거가 있는가? 2.4GHz, 1m 구간, 중앙 프레넬 영역 17.7cm를 계산했지만 이것은 RF 교통 검지 정확도를 입증하지 않아. 좁은 탁상 공간에서 다중경로와 안테나 설치 변화에 얼마나 취약한가?
4. 실제 CSI 파일이 전혀 없는 상태에서 만든 인위적 분류 정확도·통과 테스트를 측정 성능처럼 포장하지 않았는가?
5. 예전의 SUMO 황색·시간격자·2.05초 예외와 K047 진입·출구 코호트 오류가 최신 문서에서 제대로 정정됐는가? 네 11월 17일 지적이 사후에 미반영 상태로 남지는 않았는가?
6. WiTraffic·DeepWiTraffic·ESP32 CSI에 이미 있는 기술을 최초 발명처럼 제시하지 않았는가? 기존 장치/알고리즘을 직접 재현하려면 어떤 구체적 하드웨어, 원본 방법, 공개 코드, 허가된 데이터가 필요한가?
7. 어떤 독립 대조실험이면 'Wi-Fi 두 링크가 단순 RSSI보다 원인 구분에 더 유용하다'는 주장을 **기각**할 수 있는가? 고정 물체, 설치 위치가 바뀐 날, 차량 재질, 소음, 결측에 대한 사전등록 필요.
8. 센서 분류 성능이 높더라도 *실제 실행 가능한* 신호 행동 집합에서 현시 결정이 안 바뀌면 정보 가치는 0일 수 있어. 이를 이론적으로 어떤 방식으로 평가해야 하는가?

아예 다른 해결책이 더 타당하면 그 이유와 구체적인 실험을 제안해 줘. 불충분한 증거는 결론을 유보해 줘.

## 5. 실제 실행하고, 의미 있는 커밋을 자주 해줘

먼저 GitHub `main`의 HEAD를 기록해. 코드나 문헌 명세를 바꿀 때마다 독립적인 작은 단위로 리뷰 가능한 커밋을 해 줘. 단순 커밋 숫자 늘리기는 금지하고, 다른 연구자가 동시에 `main`을 수정 중일 수 있으므로 매번 최신 파일 SHA를 확인해 충돌을 피하자. GitHub Actions 사용 금지, `github-actions[bot]` 기여 금지.

가장 먼저 기존 RF 코드 9개 이상 테스트와 가능한 기존 저장소 테스트를 다시 돌려보고 실행 환경을 기록해 줘. 실행하지 못했다면 정직하게 보류해. 가능하다면 논문 하나를 골라 **그 논문의 입력·수식·산출량을 실제로 구현하고 재현하는 작지만 완결된 검증 단위**를 제안·개발해 줘. 해당 논문과 다르게 단순화했다면 다른 점을 반드시 명시해 줘.

## 6. 네 기록 위치 — 오늘 별도 폴더가 준비돼 있어

**김세호의 날짜별 사유 폴더 (2026-11-21)**:
https://drive.google.com/drive/folders/1BxbNV7-e87G9phXzWJ_TBORJ4S71KBZM

이 폴더는 공유 연구일지의 정식 하위 폴더야. 네가 직접 **새 Google Docs 문서**를 만들어 줘.

권장 제목: `20261121 김세호의 사유 — T2·RF-CURTAIN 독립 비판 감사 및 문헌 재현`

파일은 반드시 위 폴더 안에 만들고, 문서 안에 GitHub 커밋 SHA, 검토한 논문 ID·DOI, 실행 명령·환경, 테스트 결과, 반례, 미확인 사실, 수정안, 다음 실험의 사전등록 조건까지 자세히 기록해 줘. 네 11월 17일 연구 기록은 그대로 보존하고 새 문서와 서로 링크만 해 줘. 원본 논문 PDF는 Research OS 10_PAPERS, 새 원시 대용량 데이터와 ZIP은 용도별 Drive 선반에 보존하며 **날짜별 사유 폴더에는 Google Docs만** 두자.

정책·논증상 주요한 반론은 문서에 원문을 남기고 GitHub에도 간결한 감사 결과를 커밋해 줘. 우리 판단과 다르더라도 고치지 말고 근거와 대조해 줘.

## 7. 첫 보고 형식

A. 실제 읽은 정본 및 검증된 HEAD.
B. 확인 사실 / 재현 수치 / 미확인 전제 / 기존 주장과 충돌.
C. 선행논문 보유·미보유 변경표.
D. 네가 직접 찾아낸 **가장 치명적인 반례나 실패 조건 세 가지**.
E. 실제 코드·테스트·커밋·Google Docs URL.
F. 다음 독립 실험과 중단 기준.
끝에 '완료 / 다음 / 미해결 / 내 할 일' 네 줄 요약.

**시간에 쫓겨 실험 수만 늘리지 말고, 내 주장까지 과감히 반박해 줘.** 사실 확인이 안 되는 것은 안 된다고 적고, 새로운 기술을 발명했다는 과장보다 원본 논문을 충실히 이해하고 검증 가능한 장치와 구현을 만드는 데 집중하자.
