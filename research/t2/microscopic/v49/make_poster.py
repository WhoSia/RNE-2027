from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor
import csv
R=Path(__file__).parent
OUT=R/'T2_v49_exhibition_board_A3.pdf'
font='/usr/share/fonts/truetype/nanum/NanumSquareR.ttf'
fontb='/usr/share/fonts/truetype/nanum/NanumSquareB.ttf'
pdfmetrics.registerFont(TTFont('Nanum',font));pdfmetrics.registerFont(TTFont('Nanum-Bold',fontb))
W,H=landscape(A3)
c=canvas.Canvas(str(OUT),pagesize=(W,H))
blue=HexColor('#173b5a'); teal=HexColor('#116e7a'); grey=HexColor('#526172'); pale=HexColor('#edf4f7'); gold=HexColor('#996410')

def text(x,y,s,size=12,color=blue,bold=False):
    c.setFillColor(color);c.setFont('Nanum-Bold' if bold else 'Nanum',size);c.drawString(x,y,s)

def rounded(x,y,w,h,fill,stroke=None,radius=12):
    c.setFillColor(fill);c.setStrokeColor(stroke or fill);c.roundRect(x,y,w,h,radius,fill=1,stroke=bool(stroke))

def image(path,x,y,w,h):
    from PIL import Image
    im=Image.open(path);iw,ih=im.size
    ratio=min(w/iw,h/ih);nw=iw*ratio;nh=ih*ratio
    c.drawImage(ImageReader(im),x+(w-nw)/2,y+(h-nh)/2,nw,nh,mask='auto')

# page1
c.setFillColor(HexColor('#f8fafc'));c.rect(0,0,W,H,fill=1,stroke=0)
c.setFillColor(blue);c.rect(0,H-111,W,111,fill=1,stroke=0)
text(35,H-49,'T2  |  교통망을 더 정교하게, 신호 개선은 더 신뢰성 있게',28,HexColor('#ffffff'),True)
text(36,H-78,'경남과학전람회 연구 시안  ·  v4.9  ·  2026-11-02  ·  합성 미시 시뮬레이션  /  실측·SUMO 검증 전',13,HexColor('#c2e7eb'))
# left panel
x0=30;xl=363;right=W-xl-30
rounded(x0,510,320,196,HexColor('#ffffff'),HexColor('#dde8ef'))
text(x0+15,679,'① 실제로 실행되는 3교차로 차량 네트워크',14,blue,True)
image(R/'fig01_network.png',x0+9,525,302,140)
rounded(x0,282,320,215,HexColor('#ffffff'),HexColor('#dde8ef'))
text(x0+15,468,'② 모델링 구성 · 물리 변수',14,blue,True)
for k,line in enumerate([
    '차량별 OD, 이동 경로, 위치, 속도, 정지시간',
    'IDM 차량추종: 가속 / 감속 / 안전간격',
    '3개 활성 신호: 주기 60초, 교차로별 오프셋',
    '주도로·측면도로 녹색시간 및 전환 손실',
    '유한 링크 저장공간 + 하류 수용 제한',
    '외부 진입 대기 + 차량 수 보존 실시간 검사',
    '매칭 수요: 3 수요 × 4 신호안 × 5 시드',
]): text(x0+15,439-k*25,'•  '+line,11,grey)
rounded(x0,68,320,201,HexColor('#eaf2f4'),None)
text(x0+15,243,'③ 관찰된 경향  (합성 모델 내부)',14,blue,True)
text(x0+17,207,'균형 수요',12,blue,True)
text(x0+156,207,'체류량 18.9% 감소',12,teal,True)
text(x0+17,172,'본선 집중',12,blue,True)
text(x0+156,172,'체류량 15.2% 감소',12,teal,True)
text(x0+17,137,'측면 집중',12,blue,True)
text(x0+156,137,'체류량 4.2% 증가',12,gold,True)
text(x0+17,97,'위 수치는 본선 우선 정책 vs 고정시간 기준선',10,grey)
# right panel: bar + queue plots
rounded(xl,354,right,352,HexColor('#ffffff'),HexColor('#dde8ef'))
text(xl+18,679,'④ 동일한 차량 수요로 비교한 정책별 시스템 체류시간',14,blue,True)
image(R/'fig02_policy_vehicle_hours.png',xl+14,369,right-28,291)
rounded(xl,68,right,273,HexColor('#ffffff'),HexColor('#dde8ef'))
text(xl+18,318,'⑤ 신호정책에 따라 달라지는 대기열과 개별 차량 궤적',14,blue,True)
image(R/'fig03_occupancy_timeseries.png',xl+12,83,(right-35)/2,211)
image(R/'fig05_vehicle_trajectory.png',xl+20+(right-35)/2,83,(right-35)/2,211)
text(31,32,'주의: 차량 행동과 교통 수요는 가정값. 실제 경남 도로망의 통행량·차로·신호자료로 보정하거나 검증하지 않았음.',11,HexColor('#9a3a28'),True)
text(W-179,15,'T2 R&E 2027  |  연구 도판 1/2',9,grey)
c.showPage()
# page2
c.setFillColor(HexColor('#f8fafc'));c.rect(0,0,W,H,fill=1,stroke=0)
c.setFillColor(blue);c.rect(0,H-95,W,95,fill=1,stroke=0)
text(35,H-45,'T2  |  실험 프로토콜과 검증 경계',28,HexColor('#ffffff'),True)
text(35,H-72,'전람회 제출 전 검토용 기술 부록 · 합성 결과 / 실제 도로 효과의 추정값이 아님',13,HexColor('#c2e7eb'))
rounded(30,530,550,195,HexColor('#ffffff'),HexColor('#dde8ef'))
text(48,695,'실험 조건',16,blue,True)
for i,line in enumerate([
    '가상 간선: 본선 160 / 180 / 180m, 측면 유입 85m × 3',
    '매 시뮬레이션 시간간격 0.5초 · 관측 580초 · 차량 유입 320초까지',
    '네 정책: 고정시간 / 오프셋 연동 / 본선 우선 / 측면 우선',
    '수요 세 조건: 균형 / 본선 집중 / 측면 집중, 동일 seed의 유입 목록 고정',
    '각 조건 5회 반복, 총 60회. 보정되지 않은 합성 차량 수요만 사용',
]):text(48,660-i*29,'• '+line,12,grey)
rounded(596,530,W-626,195,HexColor('#ffffff'),HexColor('#dde8ef'))
text(614,695,'판정 기준',16,blue,True)
for i,line in enumerate([
    'E(H) = 관측 기간의 미완료 차량 수 × 시간 적분',
    '단위: 차량·초, 완료 여부에 따른 편향을 보완',
    '완료 OD 통행수 / 미완료 / 유입 경계 잔여량 병기',
    '평균 완료 통행시간만 비교하는 해석은 금지',
    '보존: 생성 = 완료 + 내부 차량 + 외부 진입 대기',
]):text(614,660-i*29,'• '+line,12,grey)
rounded(30,173,550,339,HexColor('#ffffff'),HexColor('#dde8ef'))
text(48,485,'6개 정지선 주변 대기열의 시간 변화',15,blue,True)
image(R/'fig04_stopline_queues.png',45,188,522,275)
rounded(596,173,W-626,339,HexColor('#ffffff'),HexColor('#dde8ef'))
text(614,484,'지금까지 통과한 소프트웨어 검증',16,blue,True)
for i,line in enumerate([
    '13개 단위 테스트 통과',
    '모든 시간단계의 차량 수 보존 검사',
    '차량의 링크 내 위치/속도 유효범위 검사',
    '선행차와 후행차의 기하학적 중첩 방지 검사',
    '동일한 seed에서 동일 OD 목록 재현',
    '최소 신호 녹색시간·전환 손실 준수',
    '세 교차로의 활성 신호와 차량 이동 확인',
    '원시 궤적·대기열·완료 차량 CSV 제공',
]):text(614,448-i*34,'• '+line,12,grey)
rounded(30,67,W-60,88,HexColor('#fff6e8'),None)
text(45,132,'아직 주장할 수 없는 것',15,HexColor('#7f490b'),True)
text(45,104,'실제 경남 교차로의 교통 개선율, 현장 보정된 차량추종, 안전성 인증, 미시 SUMO 재현 일치, 최적 제어의 보편적 우월성',11,HexColor('#7f490b'))
text(45,82,'다음: 경남 도로 기하 + 현시 + 방향별 회전교통량 확보 → SUMO 같은 OD 재현 → 다른 날짜 홀드아웃 검증',11,blue,True)
text(31,33,'원시 데이터와 프로그램: 함께 제공되는 T2 v4.9 재현 ZIP / 모든 정책 수치는 합성 모형 내 비교에 한정',10,grey)
text(W-180,16,'T2 R&E 2027  |  기술 부록 2/2',9,grey)
c.save()
print(OUT)
