"""Plot two-objective turn-pocket tradeoffs from v1.3 synthetic output."""
from pathlib import Path
import json
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent/"results"

def draw(source=ROOT/"receiver_summary_v13.json",
         target=ROOT/"v13_pareto_tradeoff.png"):
    rows=json.loads(Path(source).read_text())
    fig,ax=plt.subplots(figsize=(9,5.5))
    for headway in (2,4,8):
        group=sorted([r for r in rows if r["turn_share"]==.3 and
            r["receiver_slots"]==2 and r["receiver_headway_s"]==headway and
            r["B_share"]==.5],key=lambda r:r["pocket_m"])
        if len(group)!=4:raise ValueError("missing pocket scenario")
        xs=[r["mean_network_L"] for r in group]
        ys=[r["mean_network_S"] for r in group]
        ax.plot(xs,ys,marker="o",label=f"Receiver headway {headway}s")
        for x,y,r in zip(xs,ys,group):
            ax.annotate(f"{int(r['pocket_m'])}m",(x,y),
                xytext=(4,5),textcoords="offset points",fontsize=8)
    ax.set(xlabel="Left network completions in 720s (8 matched seeds)",
           ylabel="Through network completions in 720s (8 matched seeds)",
           title="T2 v1.3 — pocket tradeoffs depend on downstream supply\nSynthetic, not calibrated")
    ax.grid(alpha=.25);ax.legend()
    fig.tight_layout()
    fig.savefig(target,dpi=190)
    plt.close(fig)
    return target

if __name__=="__main__":
    print(draw())
