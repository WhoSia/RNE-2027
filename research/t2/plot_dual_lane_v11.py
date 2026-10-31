"""Render the physical two-lane sensitivity figure from committed runner JSON.

The plot explicitly labels synthetic values; Matplotlib is the only
non-stdlib dependency and is used only for presentation.
"""
from pathlib import Path
import json
import matplotlib.pyplot as plt

def plot(summary_path,output_path):
    rows=json.loads(Path(summary_path).read_text())
    fig,ax=plt.subplots(figsize=(9,5.6))
    cases=((0.,False,"Only pocket-adjacent through lane"),
        (.5,False,"50/50 fixed lane allocation"),
        (.5,True,"50/50 + restricted lateral movement"),
        (1.,False,"All straight cars in independent lane B"))
    for b,changes,label in cases:
        r=sorted((x for x in rows if x["turn_share"]==.30 and
            x["B_share"]==b and x["lane_change"]==changes),
            key=lambda x:x["pocket_m"])
        if len(r)!=4:raise ValueError("missing bay length cell")
        ax.plot([x["pocket_m"] for x in r],
            [x.get("mean_through_exits",x.get("mean_S")) for x in r],
            marker="o",label=label)
    ax.grid(alpha=.25)
    ax.set(xlabel="Physical turn pocket length (m)",
           ylabel="Through exits in 1800 s (8 matched seeds)",
           title="T2 v1.1 geometric mechanism sensitivity — synthetic, not calibrated")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(output_path,dpi=185)
    plt.close(fig)

if __name__=="__main__":
    import sys
    plot(sys.argv[1],sys.argv[2])
