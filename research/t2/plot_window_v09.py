"""Create a reproducible 5-policy figure from window sensitivity JSON.

Requires matplotlib; figure text explicitly identifies simulation status.
Usage: python research/t2/plot_window_v09.py results/window_sensitivity_v09.json output.png
"""
import json,sys
from pathlib import Path
import matplotlib.pyplot as plt

def plot(source,output):
    raw=json.loads(Path(source).read_text())
    rows=raw.get("summary") or raw.get("means")
    fig,ax=plt.subplots(figsize=(9,5.6))
    conditions=[("fifo",1,"FIFO / no bypass"),("window",2,"Window 2"),
        ("window",4,"Window 4"),("window",8,"Window 8"),
        ("bypass",999,"Unbounded lookahead")]
    for policy,window,label in conditions:
        items=[r for r in rows if r["policy"]==policy and r["lookahead"]==window]
        items.sort(key=lambda r:r["bay_m"])
        if len(items)!=4:raise ValueError("incomplete four-pocket scenario")
        ax.plot([r["bay_m"] for r in items],
                [r.get("mean_S",r.get("mean_through")) for r in items],
                marker="o",label=label)
    ax.set(xlabel="Left-turn pocket length (m)",
           ylabel="Through exits per 1800 s (8 paired seeds)",
           title="T2 v0.9: assumption sensitivity (synthetic, uncalibrated)")
    ax.grid(alpha=.2);ax.legend(fontsize=9)
    fig.tight_layout();fig.savefig(output,dpi=200)
    plt.close(fig)
if __name__=="__main__":
    plot(sys.argv[1],sys.argv[2])
