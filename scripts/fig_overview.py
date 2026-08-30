import matplotlib, os
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
ROOT=os.path.join(os.path.dirname(__file__),"..")
RED="#7a2020";BLUE="#2c5f8a";GREEN="#0b8a4b";INK="#1a1a1a"
plt.rcParams.update({"font.family":"sans-serif","font.sans-serif":["Segoe UI","DejaVu Sans"],"svg.fonttype":"none"})
fig,ax=plt.subplots(figsize=(8.2,3.0)); ax.set_xlim(0,100); ax.set_ylim(0,40); ax.axis("off")
def box(x,y,w,h,title,lines,ec,fc):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.4,rounding_size=1.2",lw=1.3,ec=ec,fc=fc))
    ax.text(x+w/2,y+h-3.4,title,ha="center",va="top",fontsize=10,fontweight="bold",color=ec)
    for i,ln in enumerate(lines): ax.text(x+w/2,y+h-7.2-i*3.4,ln,ha="center",va="top",fontsize=8,color=INK)
def arrow(x1,y1,x2,y2):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="-|>",mutation_scale=11,lw=1,color="#555"))
box(1,26,25,12,"Arm 1 — VED fleet",["197 ICE cars, 14,460 trips","GPS + OBD, fuel from MAF"],RED,"#f3eded")
box(1,14,25,10,"Arm 2 — EngineFaultDB",["engine-fault bench","rich / lean / ignition"],BLUE,"#eef2f6")
box(1,2,25,9,"Driving Events",["aggressive/normal labels"],GREEN,"#eef5ee")
box(38,22,26,11,"Kinematic axis",["accel, jerk, harsh events"],RED,"#fff")
box(38,8,26,11,"Combustion axis",["fuel trims / AFR, CO, HC"],BLUE,"#fff")
box(74,13,25,14,"Attribution",["driver vs vehicle","frozen signatures","88.6% (bench)"],GREEN,"#eef5ee")
for y in (30,8): arrow(26,y+2,37.5,26)
arrow(26,19,37.5,14)
arrow(64,27,73.5,22); arrow(64,13,73.5,18)
fig.tight_layout()
fig.savefig(os.path.join(ROOT,"figures","overview.svg"),bbox_inches="tight")
fig.savefig(os.path.join(ROOT,"figures","overview.png"),bbox_inches="tight",dpi=150)
print("wrote overview")
