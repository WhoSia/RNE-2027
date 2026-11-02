"""Run matched-demand scenarios, reproducible CSVs and schematic/plots.
Important: all generated demands are SYNTHETIC and not observed Gyeongnam traffic.
"""
import csv, json, statistics
from pathlib import Path
from network import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT=Path(__file__).parent
SEEDS=(11,29,41,73,97)

def write_csv(path,rows):
    if not rows:return
    with Path(path).open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def run():
    rows=[]; sample={}
    for d in DEMANDS:
        for seed in SEEDS:
            arrivals=make_arrivals(d,seed,arrive_until=320.)
            demand_count=len(arrivals)
            for plan in PLANS:
                detailed=(d.name=='balanced' and seed==41 and plan.name in ('fixed_32','coordinated_32','main_priority_38'))
                result=simulate(plan,arrivals,horizon=580.,dt=DT,save_trajectory=detailed)
                summary={'scenario':d.name,'seed':seed,**result['summary']}
                if summary['generated']!=demand_count:raise AssertionError('matched exogenous demand violated')
                rows.append(summary)
                if detailed:sample[plan.name]=result
    write_csv(ROOT/'policy_runs.csv',rows)
    if sample:
        write_csv(ROOT/'trace_queues.csv', [{ 'policy':k,**row } for k,v in sample.items() for row in v['queues']])
        write_csv(ROOT/'trace_vehicles.csv', [{ 'policy':k,**row } for k,v in sample.items() for row in v['trajectories']])
        write_csv(ROOT/'completed_trips_sample.csv', [{'policy':k,**row} for k,v in sample.items() for row in v['trips']])
    summaries=[]
    for demand in DEMANDS:
        for plan in PLANS:
            sub=[r for r in rows if r['scenario']==demand.name and r['policy']==plan.name]
            summaries.append({'scenario':demand.name,'policy':plan.name,
                'mean_generated':statistics.mean(x['generated'] for x in sub),
                'mean_completed':statistics.mean(x['completed'] for x in sub),
                'mean_remaining_inside':statistics.mean(x['remaining_inside'] for x in sub),
                'mean_pending_boundary':statistics.mean(x['pending_boundary'] for x in sub),
                'mean_vehicle_seconds':statistics.mean(x['system_vehicle_seconds_in_horizon'] for x in sub),
                'min_vehicle_seconds':min(x['system_vehicle_seconds_in_horizon'] for x in sub),
                'max_vehicle_seconds':max(x['system_vehicle_seconds_in_horizon'] for x in sub)})
    write_csv(ROOT/'policy_summary.csv',summaries)
    meta={'model':'T2 v4.9 IDM network, NOT SUMO or field calibrated',
          'time_step_s':DT,'horizon_s':580,'arrival_end_s':320,
          'network_links_m':LENGTHS,'policies':[vars(p) for p in PLANS],
          'demands':[vars(d) for d in DEMANDS], 'seeds':list(SEEDS),
          'runs':len(rows),'tests_required':13,
          'policy_summary':summaries}
    (ROOT/'experiment_manifest.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
    create_charts(summaries,sample)
    return meta


def create_charts(summaries,sample):
    font_path='/usr/share/fonts/truetype/nanum/NanumSquareR.ttf'
    import os
    if not os.path.exists(font_path):
        font_path=next((f.fname for f in font_manager.fontManager.ttflist if 'NanumSquare' in f.name),None)
    if font_path:
        font_manager.fontManager.addfont(font_path)
        f=font_manager.FontProperties(fname=font_path)
        plt.rcParams['font.family']=f.get_name()
    plt.rcParams.update({'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':150,
                         'axes.titlesize':12,'axes.labelsize':10,'legend.frameon':False})
    # Network schematic, conceptual topology rather than a literal geographic location.
    fig,ax=plt.subplots(figsize=(11.3,3.9))
    node_x=(160,340,520)
    for j,x in enumerate(node_x):
        ax.plot([0 if j==0 else node_x[j-1],x],[0,0],lw=14,solid_capstyle='butt',alpha=.28)
        ax.scatter([x],[0],s=800,zorder=10)
        ax.text(x,0,f'J{j+1}',ha='center',va='center',color='white',weight='bold',fontsize=13,zorder=11)
        ax.plot([x,x],[-90,-10],lw=11,solid_capstyle='butt',alpha=.28)
        ax.annotate('',xy=(x,-8),xytext=(x,-50),arrowprops=dict(arrowstyle='->',lw=2))
        ax.text(x,-105,f'측면 S{j+1}',ha='center',fontsize=10)
    ax.annotate('',xy=(145,0),xytext=(65,0),arrowprops=dict(arrowstyle='->',lw=2))
    ax.annotate('',xy=(335,0),xytext=(260,0),arrowprops=dict(arrowstyle='->',lw=2))
    ax.annotate('',xy=(515,0),xytext=(445,0),arrowprops=dict(arrowstyle='->',lw=2))
    for xx,label in ((75,'M0 본선'),(250,'M1 본선'),(435,'M2 본선')):
        ax.text(xx,20,label,fontsize=10,ha='center')
    ax.text(5,38,'상류 진입',fontsize=11)
    ax.text(520,43,'각 J에서 종료하거나\n다음 본선으로 합류',ha='right',fontsize=10)
    ax.set(xlim=(-25,585),ylim=(-133,68));ax.axis('off')
    ax.set_title('3개 신호교차로 × 6개 유한 링크 × 차량별 OD 경로',pad=15)
    fig.tight_layout();fig.savefig(ROOT/'fig01_network.png',bbox_inches='tight');plt.close(fig)

    scenarios=[x.name for x in DEMANDS]
    policies=[x.name for x in PLANS]
    # Metrics: vehicle seconds, lower better, include incomplete vehicles.
    fig,ax=plt.subplots(figsize=(11.3,4.5))
    import numpy as np
    X=np.arange(len(scenarios)); width=.18
    for i,p in enumerate(policies):
        vals=[next(r['mean_vehicle_seconds'] for r in summaries if r['scenario']==s and r['policy']==p)/3600 for s in scenarios]
        ax.bar(X+(i-1.5)*width,vals,width,label=p.replace('_',' '))
    ax.set_xticks(X, ['균형 수요','본선 집중','측면 집중'])
    ax.set_ylabel('시스템 누적 체류량 (차량·시간, 580초 관측)')
    ax.set_title('동일한 OD 유입 목록으로 비교한 신호계획별 시스템 체류량')
    ax.legend(ncol=2,loc='upper left');fig.tight_layout();fig.savefig(ROOT/'fig02_policy_vehicle_hours.png',bbox_inches='tight');plt.close(fig)

    fig,ax=plt.subplots(figsize=(11.3,4.3))
    sample_p=['fixed_32','coordinated_32','main_priority_38']
    for p in sample_p:
        q=sample[p]['queues']; ax.plot([x['t_s'] for x in q],[x['inside']+x['upstream_pending'] for x in q],label=p.replace('_',' '))
    ax.set(xlabel='경과시간 (초)',ylabel='미완료 차량수 (대)',title='균형 수요 · seed=41 — 시간에 따른 미완료 차량수')
    ax.legend();fig.tight_layout();fig.savefig(ROOT/'fig03_occupancy_timeseries.png',bbox_inches='tight');plt.close(fig)

    fig,ax=plt.subplots(figsize=(11.3,4.3))
    for p in sample_p:
        q=sample[p]['queues'];ax.plot([x['t_s'] for x in q], [sum(x[f'queue_{i}'] for i in ('M0','M1','M2','S0','S1','S2')) for x in q],label=p.replace('_',' '))
    ax.set(xlabel='경과시간 (초)',ylabel='정지선 40m 이내 정체 차량수 (대)',title='교차로 접근 대기열의 시간 변화 · seed=41')
    ax.legend();fig.tight_layout();fig.savefig(ROOT/'fig04_stopline_queues.png',bbox_inches='tight');plt.close(fig)

    fig,ax=plt.subplots(figsize=(11.3,4.3))
    # One vehicle ID found in all 3 runs, from M0 to M2.
    target=None
    for trip in sample['fixed_32']['trips']:
        if trip['origin']=='M0' and trip['destination']=='M2':target=trip['id'];break
    if target is not None:
        offsets={'M0':0,'M1':160,'M2':340}
        for p in sample_p:
            t=[x for x in sample[p]['trajectories'] if x['id']==target and x['link'] in offsets]
            ax.plot([x['t_s'] for x in t],[offsets[x['link']]+x['x_m'] for x in t],label=p.replace('_',' '))
        for x,label in ((160,'J1'),(340,'J2'),(520,'J3')):
            ax.axhline(x,linestyle=':',lw=.8)
            ax.text(0,x+4,label,fontsize=9)
        ax.set(xlabel='경과시간 (초)',ylabel='본선 누적 위치 (m)',title=f'동일 OD 차량 #{target}의 시공간 궤적 · seed=41')
        ax.legend();fig.tight_layout();fig.savefig(ROOT/'fig05_vehicle_trajectory.png',bbox_inches='tight')
    plt.close(fig)

if __name__=='__main__':
    summary=run()
    for r in summary['policy_summary']:print(r['scenario'],r['policy'],round(r['mean_completed'],1),round(r['mean_vehicle_seconds']/3600,3))
