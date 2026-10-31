"""Render reproducible v1.4 temporal and sensitivity figures from saved JSON."""
import json
from pathlib import Path
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent/'results'

def temporal():
    data=json.loads((ROOT/'temporal_summary_v14.json').read_text())
    fig,ax=plt.subplots(figsize=(8,5))
    for aoff in (0,30):
        for pocket in (14.,70.):
            items=sorted((r for r in data if r['rate']=='steady'
                and r['turn']=='steady' and r['arrival_offset']==aoff
                and r['pocket_m']==pocket),key=lambda x:x['signal_offset'])
            ax.plot([r['signal_offset'] for r in items],
                [r['mean_total'] for r in items],marker='o',
                label=f'Arrival offset {aoff}s, pocket {int(pocket)}m')
    ax.set(xlabel='Signal phase offset (s)',
           ylabel='Final network exits / 720 s',
           title='T2 v1.4 synthetic temporal coordination, not calibrated')
    ax.grid(alpha=.2);ax.legend(fontsize=8);fig.tight_layout()
    path=ROOT/'temporal_coordination_v14.png';fig.savefig(path,dpi=180);plt.close(fig)
    return path

def sensitivity():
    data=list(reversed(json.loads((ROOT/'sensitivity_rank_v14.json').read_text())))
    fig,ax=plt.subplots(figsize=(8,5))
    ax.barh([r['lever'] for r in data],[r['range_total'] for r in data])
    ax.set(xlabel='Range of average final network exits, 720s',
           title='T2 v1.4 one-at-a-time sensitivity — unstandardized levels')
    ax.grid(axis='x',alpha=.2);fig.tight_layout()
    path=ROOT/'sensitivity_screen_v14.png';fig.savefig(path,dpi=180);plt.close(fig)
    return path

if __name__=='__main__':
    print(temporal(),sensitivity())
