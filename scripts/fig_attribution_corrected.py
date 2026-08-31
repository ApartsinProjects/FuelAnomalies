import json, os, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
ROOT=os.path.join(os.path.dirname(__file__),".."); FIG=os.path.join(ROOT,"figures")
R=json.load(open(os.path.join(ROOT,"data","processed","p17_attribution_fixed.json")))
RED="#7a2020";BLUE="#2c5f8a";GREEN="#0b8a4b";GRAY="#9a9a9a";INK="#1a1a1a"
plt.rcParams.update({"font.family":"serif","font.serif":["Georgia","DejaVu Serif"],"svg.fonttype":"none","axes.titleweight":"bold"})
# ---- Fig: severity sweep + falsification ----
sw=R["driver_severity_sweep"]; xs=[float(k) for k in sw]; ys=[sw[k] for k in sw]
fig,ax=plt.subplots(figsize=(5.8,3.8))
ax.plot(xs,ys,"-o",color=GREEN,lw=2.2,ms=5,label="frozen source-derived attributor")
ax.axhline(R["negated_weights_acc"],ls="--",color=RED,lw=1.4,label="negated weights (falsification)")
ax.axhline(R["fuel_only_measured_acc"],ls=":",color=GRAY,lw=1.4,label="fuel magnitude only (measured)")
ax.plot(0.65,R["frozen_argmax_acc"],"*",color=INK,ms=15)
ax.annotate("realistic operating point\n(d=0.65): %.2f"%R["frozen_argmax_acc"],xy=(0.65,R["frozen_argmax_acc"]),
            xytext=(1.2,0.60),fontsize=9,arrowprops=dict(arrowstyle="->",color=INK,lw=1))
ax.axvline(1.66,color=BLUE,lw=1,ls="--",alpha=0.6); ax.text(1.68,0.50,"fault magnitude\n(bench, 1.66)",fontsize=8,color=BLUE)
ax.set_xlabel("driver aggression severity  (Cohen's d on kinematic score)")
ax.set_ylabel("attribution accuracy"); ax.set_ylim(0.45,1.0)
ax.set_title("Attribution rises with driver severity; falsifiable")
ax.legend(fontsize=8.5,frameon=False,loc="lower right")
for s in ["top","right"]: ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig(f"{FIG}/fig6_attribution_accuracy.svg",bbox_inches="tight"); fig.savefig(f"{FIG}/fig6_attribution_accuracy.png",bbox_inches="tight",dpi=150); plt.close(fig)
# ---- Fig: corrected mixed-cause grid ----
g=R["grid_S"]; H=np.array([[np.nan if x is None else x for x in row] for row in R["grid_acc"]])
fig,ax=plt.subplots(figsize=(4.8,4.2))
im=ax.imshow(H,origin="lower",cmap="RdYlGn",vmin=0.5,vmax=1.0)
ax.set_xticks(range(len(g))); ax.set_xticklabels(g); ax.set_yticks(range(len(g))); ax.set_yticklabels(g)
ax.set_xlabel("fault effect $S_f$"); ax.set_ylabel("driver severity $S_d$"); ax.set_title("Dominant-cause accuracy (corrected)")
for i in range(len(g)):
    for j in range(len(g)):
        if np.isfinite(H[i,j]): ax.text(j,i,f"{H[i,j]:.2f}",ha="center",va="center",fontsize=7)
fig.colorbar(im,ax=ax,shrink=0.8,label="accuracy"); fig.tight_layout()
fig.savefig(f"{FIG}/mixed_cause_grid.svg",bbox_inches="tight"); fig.savefig(f"{FIG}/mixed_cause_grid.png",bbox_inches="tight",dpi=150); plt.close(fig)
print("wrote corrected attribution figures")
