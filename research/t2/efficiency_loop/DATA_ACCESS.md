# 실측 데이터 접촉 및 결합 계획

| 자료 | 이번 실행에서 확인 | 다음 입력 검사 |
| --- | --- | --- |
| DLR-UT K047 | 열린 블록 7개에서 정지선·대기열·신호 시간축을 재결합. 73개 녹색 구간의 전이 괄호와 분류 불확실성 보존. | 접근로별 신호 헤드, 시야 공백, 하류 수용 공간, 초기 큐를 고정한 뒤 보류된 구간 평가. |
| SinD Tianjin 8_2_1 | 4,843바이트 신호 원본의 SHA-256이 배포 Git LFS 객체와 일치. 궤적 LFS 파일명, 크기 36,940,154바이트와 해시 확인. | 궤적 원본과 지도 원점을 확보해 같은 프레임·교차로에서 정지선 통과를 맞춘다. |
| SinD Changchun 507_009 | 1,721바이트 신호 원본의 SHA-256이 배포본과 일치. 차량 궤적 LFS 크기 129,987,853바이트 확인. | 두 신호그룹이 관리하는 실제 이동류와 프레임 정렬을 확인한다. |
| 서울 C-ITS | 전일 신호·잔여시간, 신호 연결 MAP, 차로 MAP 개별 목록 확인. 신호 목록에서 날짜별 ZIP 이름 확인. | 실제 파일 헤더와 교차로·신호그룹 결합키를 확인. 같은 날짜의 방향별 진입·통과 계수가 확보되면 도착·방출 재생으로 확장. |
| CityArtery | 배포 문서가 신호 시간 기록 3개 시나리오, 궤적, 모의실험 보정 파일을 명시. 공식 배포 버튼의 29.2 MB ZIP 경로와 application/zip 응답을 확인. 실행 환경에서 원시 ZIP 바이트 확보 실패. | 같은 시나리오의 신호·지도·궤적 세 파일과 시계 정렬을 확인. |

## 국내 데이터 문의 초안

제목은 ‘교차로 신호 현시 이력과 방향별 교통량 자료의 결합 가능 여부 문의’로 둔다.

안녕하세요. 학교 연구에서 신호 현시별 대기와 통과를 분석하고 있습니다. 공개된 신호제어기 신호·잔여시간 이력과 신호 연결 MAP을 같은 교차로 기준으로 결합할 수 있는지 확인하고 싶습니다. 교차로 ID와 신호그룹 ID의 대응표, 현시 코드와 시각 기준이 담긴 데이터 사전이 있다면 열람 경로를 알려주실 수 있을까요?

가능하다면 동일 교차로·날짜의 이동류별 검지 또는 통과 건수를 1분 이하로 집계한 자료가 있는지도 궁금합니다. 차량 식별정보는 필요하지 않습니다. 예시 교차로 1곳과 평일의 시간대 2개 정도면 연구 설계를 검증할 수 있습니다. 제공 가능한 시간 해상도와 연구 결과에 집계표를 인용할 때 적용되는 조건도 함께 알려주시면 감사하겠습니다.

## 출처

- SinD 공개 샘플과 구조 [데이터 구조](https://github.com/SOTIF-AVLab/SinD/blob/main/DATASETS.md)
- SinD 실제 신호 [톈진](https://media.githubusercontent.com/media/SOTIF-AVLab/SinD/main/Data/Tianjin/8_2_1/TrafficLight_8_2_1.csv) · [창춘](https://media.githubusercontent.com/media/SOTIF-AVLab/SinD/main/Data/Changchun/changchun_pudong_507_009/Traffic_Lights.csv)
- 서울 C-ITS [신호 이력](https://t-data.seoul.go.kr/dataprovide/trafficdataviewfile.do?data_id=10382) · [신호 연결 MAP](https://t-data.seoul.go.kr/dataprovide/trafficdataviewfile.do?data_id=10146) · [차로 MAP](https://t-data.seoul.go.kr/dataprovide/trafficdataviewfile.do?data_id=10145)
- CityArtery [배포 문서](https://data.mendeley.com/datasets/ftzzmh2cmt/1)
