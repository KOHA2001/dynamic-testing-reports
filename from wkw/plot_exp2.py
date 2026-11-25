# -*- coding: utf-8 -*-
"""
实验二 超声波测试实验 —— 波形图批量绘制
样式对齐 exp2_images 参考图（p08~p16）：
  全局图：发射CH1（红）+ 接收CH2（蓝），黑色虚线框标出局部放大区域
  局部图：仅接收CH2（蓝）
csv 结构：左半为输入脉冲（第4、5列 = 时间、幅值），右半为探测信号（第10、11列）
"""
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator
from matplotlib.patches import Rectangle
from matplotlib.font_manager import FontProperties
from scipy.ndimage import maximum_filter1d

# ---------- 全局样式 ----------
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "SimSun"],
    "mathtext.fontset": "stix",
    "axes.unicode_minus": False,
    "axes.linewidth": 2.2,
    "xtick.major.size": 10,
    "ytick.major.size": 10,
    "xtick.major.width": 2.2,
    "ytick.major.width": 2.2,
    "xtick.labelsize": 20,
    "ytick.labelsize": 20,
    "axes.labelsize": 24,
    "legend.fontsize": 22,
})
# 中文标签需要显式字体回退（Times 负责数字/英文，SimSun 负责中文）
FP = FontProperties(family=["Times New Roman", "SimSun"])
FIGSIZE = (10, 8.5)
DPI = 450


def sci_formatter(x, pos=None):
    """x轴科学计数刻度，如 5.0×10^-5；0 显示为 0.0"""
    if x == 0:
        return "0.0"
    e = int(np.floor(np.log10(abs(x))))
    m = x / 10**e
    # 消除浮点误差，如 0.9999999 -> 1.0
    m = round(m, 6)
    return r"$%.1f\times10^{%d}$" % (m, e)


def load_csv(path):
    """返回 (t1, v1, t2, v2)；t1/v1 为左侧输入脉冲，t2/v2 为右侧探测信号"""
    data = np.genfromtxt(path, delimiter=",", encoding="utf-8",
                         filling_values=np.nan, invalid_raise=False)
    if data.ndim == 1:
        data = data[None, :]
    t1, v1 = data[:, 3], data[:, 4]
    t2, v2 = data[:, 9], data[:, 10]
    ok1 = ~(np.isnan(t1) | np.isnan(v1))
    ok2 = ~(np.isnan(t2) | np.isnan(v2))
    return t1[ok1], v1[ok1], t2[ok2], v2[ok2]


def _merge_groups(idx, t, gap_tol):
    """将超过阈值的索引按时间间隔合并为回波组 [(i_start, i_end_exclusive)]"""
    if len(idx) == 0:
        return []
    breaks = np.flatnonzero(np.diff(t[idx]) > gap_tol)
    starts = np.r_[idx[0], idx[breaks + 1]]
    ends = np.r_[idx[breaks], idx[-1]] + 1
    return list(zip(starts, ends))


def detect_echoes(t, v):
    """包络+阈值检测回波组；返回 (全部回波组, 用于局部放大的裁剪组)"""
    a = np.abs(v)
    dt = t[1] - t[0]
    # 包络：约 1.6 us 的滑动最大值，把每个回波包络连成整段
    win = max(int(1.6e-6 / dt), 51)
    env = maximum_filter1d(a, size=win, mode="nearest")
    feedthrough_cut = 3e-6
    after = t > feedthrough_cut
    amax_echo = a[after].max() if after.any() else a.max()
    # 迭代估计噪声：先以粗阈值排除回波，再在安静区取中位数
    thr0 = 0.1 * amax_echo
    quiet = env[(env < thr0) & after]
    noise = np.median(quiet) if len(quiet) else np.median(env[after])
    thr = max(1.4 * noise, 0.02 * amax_echo)
    idx = np.flatnonzero((env > thr) & after)
    if len(idx) == 0:
        return [], []
    # 间隔小于 2.5 us 的并为一组
    groups = _merge_groups(idx, t, gap_tol=2.5e-6)
    zoom_groups = groups
    if len(groups) > 4:
        # 回波组太多（长衰减列或焊缝多回波）：取含最强组的连续 4 组
        peaks = [a[s:e].max() for s, e in groups]
        imax = int(np.argmax(peaks))
        start = max(0, min(imax - 1, len(groups) - 4))
        zoom_groups = groups[start:start + 4]
    return groups, zoom_groups


def find_zoom_window(t, v, groups, zoom_groups):
    """由回波组确定局部放大窗口"""
    if not zoom_groups:
        i0 = np.searchsorted(t, 3e-6)
        return t[i0], t[-1]
    t_lo, t_hi = t[zoom_groups[0][0]], t[zoom_groups[-1][1] - 1]
    span = t_hi - t_lo
    # 下界不能低于馈通截止时间（4 us），避免把发射尖峰包进局部图
    t_lo = max(4e-6, t_lo - 0.20 * span)
    t_hi = min(t[-1], t_hi + 0.12 * span)
    return t_lo, t_hi


# ---------- 图名 ----------
MATERIAL_TITLES = {
    "纯水": "5 MHz 水浸式测量水中纵波信号",
    "钢-水": "5 MHz 水浸式测量钢试件纵波信号",
    "铝-水": "5 MHz 水浸式测量铝试件纵波信号",
    "玻璃-水": "5 MHz 水浸式测量有机玻璃试件纵波信号",
    "钢5mhz纵波": "5 MHz 接触式测量钢试件纵波信号",
    "钢10mhz纵波": "10 MHz 接触式测量钢试件纵波信号",
    "玻璃5mhz纵波": "5 MHz 接触式测量有机玻璃试件纵波信号",
    "玻璃10mhz纵波": "10 MHz 接触式测量有机玻璃试件纵波信号",
    "钢5mhz横波增益10db": "5 MHz 接触式测量钢试件横波信号（增益 10 dB）",
    "铝5mhz横波增益10db": "5 MHz 接触式测量铝试件横波信号（增益 10 dB）",
    "玻璃5mhz横波增益30db": "5 MHz 接触式测量有机玻璃试件横波信号（增益 30 dB）",
}
WELD_PROBE_TITLES = {
    "探伤斜探头横波1mhz增益30db": "1 MHz 斜探头横波焊缝探伤（增益 30 dB）",
    "探伤纵波5hz增益10db": "5 MHz 纵波直探头焊缝探伤（增益 10 dB）",
}
WELD_TAGS = {"start": "起始信号", "weak": "弱信号", "强": "强信号", "end": "结束信号"}


def weld_title(probe_dir, stem):
    """焊缝文件名 -> 图名，如 17 weak -> 位置 17（弱信号）"""
    import re
    probe = WELD_PROBE_TITLES.get(probe_dir, probe_dir)
    m = re.match(r"(\d+)", stem)
    pos = m.group(1) if m else stem
    tag_cn = ""
    for tag, cn in WELD_TAGS.items():
        if tag in stem.lower() or tag in stem:
            tag_cn = "（%s）" % cn
            break
    return "%s：位置 %s%s" % (probe, pos, tag_cn)


def _decorate(ax, zoom_window=None, title=None):
    ax.set_xlabel("时间（s）", fontproperties=FP)
    ax.set_ylabel("信号强度（V）", fontproperties=FP)
    ax.xaxis.set_major_formatter(FuncFormatter(sci_formatter))
    ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
    for spine in ax.spines.values():
        spine.set_linewidth(2.2)
    ax.tick_params(direction="out")
    if title:
        ax.set_title(title, fontproperties=FP, fontsize=24, pad=12)
    if zoom_window is not None:
        t_lo, t_hi = zoom_window
        # 窗口右界贴近记录末端时稍微内缩，避免虚线框与坐标框重叠
        x_hi = ax.get_xlim()[1]
        if t_hi > 0.97 * x_hi:
            t_hi = 0.96 * x_hi
        y_lo, y_hi = ax.get_ylim()
        rect = Rectangle((t_lo, y_lo), t_hi - t_lo, y_hi - y_lo,
                         fill=False, edgecolor="black", linestyle="--",
                         linewidth=2.0, zorder=5)
        ax.add_patch(rect)


def plot_pair(csv_path, out_global, out_zoom, title):
    t1, v1, t2, v2 = load_csv(csv_path)
    groups, zoom_groups = detect_echoes(t2, v2)
    zoom = find_zoom_window(t2, v2, groups, zoom_groups)

    # 全局图 x 轴裁剪：到最后一个回波组结束 + 余量，砍掉尾部纯噪声段
    if groups:
        t_last = t2[groups[-1][1] - 1]
        x_hi = min(t2[-1], t_last + max(8e-6, 0.10 * t_last))
        x_hi = max(x_hi, zoom[1] + 3e-6)
    else:
        x_hi = max(t1[-1], t2[-1])

    # ---- 全局图 ----
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.plot(t1, v1, color="red", lw=1.0, label="发射CH1")
    ax.plot(t2, v2, color="blue", lw=1.0, label="接收CH2")
    ax.set_xlim(0, x_hi)
    ax.margins(y=0.10)
    ax.legend(loc="upper right", frameon=False, prop=FP)
    _decorate(ax, zoom_window=zoom, title=title + "（全局）")
    fig.savefig(out_global, dpi=DPI, bbox_inches="tight")
    plt.close(fig)

    # ---- 局部放大图 ----
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.plot(t2, v2, color="blue", lw=1.0, label="接收CH2")
    ax.set_xlim(*zoom)
    mask = (t2 >= zoom[0]) & (t2 <= zoom[1])
    ymax = np.abs(v2[mask]).max()
    ax.set_ylim(-1.25 * ymax, 1.25 * ymax)
    ax.legend(loc="upper right", frameon=False, prop=FP)
    _decorate(ax, title=title + "（局部放大）")
    fig.savefig(out_zoom, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    return zoom


def main():
    base = r"C:\Users\WuKW\Desktop\动态测试技术报告\from wkw\exp2_images\顾宇辽吴凯伟"
    out_root = os.path.join(base, "波形图")

    # 1) 非焊缝：全部 csv
    out_dir = os.path.join(out_root, "材料测量")
    os.makedirs(out_dir, exist_ok=True)
    for f in sorted(os.listdir(base)):
        if f.lower().endswith(".csv"):
            src = os.path.join(base, f)
            name = os.path.splitext(f)[0]
            title = MATERIAL_TITLES.get(name, name)
            plot_pair(src,
                      os.path.join(out_dir, name + "_全局.png"),
                      os.path.join(out_dir, name + "_局部.png"),
                      title)
            print("[OK]", f)

    # 2) 焊缝探伤：仅带 start / weak / 强 / end 标记的文件
    tags = ("start", "weak", "强", "end")
    weld_root = os.path.join(base, "焊缝探伤")
    for sub in sorted(os.listdir(weld_root)):
        sub_dir = os.path.join(weld_root, sub)
        if not os.path.isdir(sub_dir):
            continue
        out_sub = os.path.join(out_root, "焊缝探伤", sub)
        os.makedirs(out_sub, exist_ok=True)
        for f in sorted(os.listdir(sub_dir)):
            if not f.lower().endswith(".csv"):
                continue
            stem = os.path.splitext(f)[0].replace(" ", "")
            if any(stem.lower().endswith(t) or t in stem for t in tags):
                plot_pair(os.path.join(sub_dir, f),
                          os.path.join(out_sub, stem + "_全局.png"),
                          os.path.join(out_sub, stem + "_局部.png"),
                          weld_title(sub, stem))
                print("[OK]", sub + "/" + f)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 单文件测试模式：python plot_exp2.py <csv路径>
        src = sys.argv[1]
        name = os.path.splitext(os.path.basename(src))[0]
        out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_out")
        os.makedirs(out_dir, exist_ok=True)
        parent = os.path.basename(os.path.dirname(src))
        if parent in WELD_PROBE_TITLES:
            title = weld_title(parent, name.replace(" ", ""))
        else:
            title = MATERIAL_TITLES.get(name, name)
        zoom = plot_pair(src,
                         os.path.join(out_dir, name + "_全局.png"),
                         os.path.join(out_dir, name + "_局部.png"),
                         title)
        print("zoom window: %.4e ~ %.4e s" % zoom)
    else:
        main()
