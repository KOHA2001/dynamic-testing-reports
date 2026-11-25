# -*- coding: utf-8 -*-
"""从焊缝探伤 csv 生成损伤示意图：缺陷反射区间内 |信号| 最大值 vs 位置
时间区间采用实验记录：纵波 4e-5~7e-5 s，斜探头 6e-5~8e-5 s"""
import os
import re
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import MaxNLocator
from PIL import Image

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "SimSun"],
    "mathtext.fontset": "stix",
    "axes.unicode_minus": False,
    "axes.linewidth": 2.2,
    "xtick.major.size": 10, "ytick.major.size": 10,
    "xtick.major.width": 2.2, "ytick.major.width": 2.2,
    "xtick.labelsize": 20, "ytick.labelsize": 20,
    "axes.labelsize": 24,
})
FP = FontProperties(family=["Times New Roman", "SimSun"])

BASE = r"C:\Users\WuKW\Desktop\动态测试技术报告\from wkw\exp2_images\顾宇辽吴凯伟\焊缝探伤"
OUT = r"C:\Users\WuKW\Desktop\动态测试技术报告\from wkw\实验二报告\exp2_images"

CONFIG = [
    ("探伤纵波5hz增益10db", 40e-6, 70e-6, "weld_L_damage.png"),
    ("探伤斜探头横波1mhz增益30db", 60e-6, 80e-6, "weld_S_damage.png"),
]


def load(path):
    d = np.genfromtxt(path, delimiter=",", encoding="utf-8",
                      filling_values=np.nan, invalid_raise=False)
    t, v = d[:, 9], d[:, 10]
    ok = ~(np.isnan(t) | np.isnan(v))
    return t[ok], v[ok]


for sub, w_lo, w_hi, outname in CONFIG:
    sub_dir = os.path.join(BASE, sub)
    pts = []
    for f in os.listdir(sub_dir):
        if not f.lower().endswith(".csv"):
            continue
        pos = int(re.match(r"(\d+)", f).group(1))
        t, v = load(os.path.join(sub_dir, f))
        m = (t >= w_lo) & (t <= w_hi)
        pts.append((pos, np.abs(v[m]).max()))
    pts.sort()
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]

    fig, ax = plt.subplots(figsize=(9.6, 5.4))  # 16:9
    ax.plot(xs, ys, color="red", lw=1.5)
    ax.set_xlabel("距离（cm）", fontproperties=FP)
    ax.set_ylabel("信号强度（V）", fontproperties=FP)
    ax.set_xlim(0, 30)
    ax.set_ylim(bottom=0)
    ax.xaxis.set_major_locator(MaxNLocator(nbins=6, integer=True))
    for spine in ax.spines.values():
        spine.set_linewidth(2.2)
    ax.tick_params(direction="out")
    out = os.path.join(OUT, outname)
    fig.savefig(out, dpi=400, bbox_inches="tight")
    plt.close(fig)
    # 扁平化为 RGB（Overleaf 兼容）
    Image.open(out).convert("RGB").save(out)
    print(outname, "positions %d~%d, %d pts, max=%.2f V @ %d cm"
          % (xs[0], xs[-1], len(pts), max(ys), xs[ys.index(max(ys))]))
