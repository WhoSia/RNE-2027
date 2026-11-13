"""Source-grounded DLR UT signal head and sampled green observation plots.
Requires matplotlib only for plotting; data analysis otherwise stdlib.
"""
from pathlib import Path
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).parent

def map_figure():
    coords=list(csv.DictReader(open(HERE/'documented_signal_positions.csv',encoding='utf8')))
    stop=list(csv.DictReader(open(HERE/'stopline_candidates.csv',encoding='utf8')))
    fig, ax=plt.subplots(figsize=(8.5,7))
    colors={'north':'#4F79A8','east':'#3F9A82','south':'#C3873B','west':'#885EAA'}
    for d in coords:
        if int(d['head_id'])>9:continue
        x=float(d['utm32_easting_m'])-604763
        y=float(d['utm32_northing_m'])-5792795
        name=d['figure1_approach']
        ax.scatter(x,y,s=35,c=colors[name],zorder=2,alpha=.85)
        ax.annotate(d['head_id'],(x,y),xytext=(4,3),textcoords='offset points',fontsize=9)
    road_approach={'100000':'east','179000':'south','201000':'west','280000':'north'}
    for d in stop:
        road=d['road_id']
        if road not in road_approach:continue
        x,y=float(d['x_ref_m']),float(d['y_ref_m'])
        ax.scatter(x,y,c='black',marker='x',s=100,zorder=4)
        ax.annotate(f'Road {road}',(x,y),xytext=(4,-13),textcoords='offset points',fontsize=9)
    for name,color in colors.items():ax.scatter([],[],c=color,label=f'{name} (vehicle heads)')
    ax.scatter([],[],c='black',marker='x',label='StVO 294 approach-end candidate')
    ax.legend(loc='upper right',fontsize=8,framealpha=.9)
    ax.set(xlabel='local X (m)',ylabel='local Y (m)',title='DLR K047: documented vehicle-signal positions vs static stop-line candidates')
    ax.axis('equal');ax.grid(alpha=.15)
    fig.text(.5,.005,'Positions and signal IDs: DLR-UT v1.3.1 pp.12-13.  No lane/movement mapping or legal crossing claim.',ha='center',fontsize=8)
    fig.tight_layout(rect=[0,0.035,1,1])
    path=HERE/'dlr_figure1_signal_head_stopline_overlay.png';fig.savefig(path,dpi=175,bbox_inches='tight');plt.close(fig)
    return path

def green_figure():
    rows=list(csv.DictReader(open(HERE/'observed_head_phase_samples.csv',encoding='utf8')))
    night={int(r['head_id']):float(r['sampled_green_fraction'])*100 for r in rows if '23:30' in r['window']}
    midday={int(r['head_id']):float(r['sampled_green_fraction'])*100 for r in rows if '12:30' in r['window']}
    fig,ax=plt.subplots(figsize=(9.1,5.1))
    inds=list(range(1,10))
    ax.bar([i-.19 for i in inds],[midday[i] for i in inds],width=.38,label='12:30–12:45 UTC',color='#4F79A8')
    ax.bar([i+.19 for i in inds],[night[i] for i in inds],width=.38,label='23:30–23:45 UTC',color='#C3873B')
    ax.set(xticks=inds,ylim=(0,52),xlabel='Documented motorized traffic signal-head ID',ylabel='Green-coded samples (%)',title='DLR K047: observed 1-Hz green-code fractions, two explored windows')
    ax.grid(axis='y',alpha=.18)
    ax.legend(loc='upper right')
    fig.text(.5,.008,'Sample fractions (codes 5/6), NOT exact green split or actual permitted lane movements. DLR source CSV.',ha='center',fontsize=8)
    fig.tight_layout(rect=[0,0.05,1,1])
    path=HERE/'dlr_observed_vehicle_green_sample_fractions.png';fig.savefig(path,dpi=175,bbox_inches='tight');plt.close(fig)
    return path
if __name__=='__main__':
    print(map_figure());print(green_figure())
