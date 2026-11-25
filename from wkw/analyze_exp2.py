# -*- coding: utf-8 -*-
"""汇总各 csv 的 Δt 与回波幅值，输出实验报告填表用的最终数值"""
import os
import numpy as np
from scipy.signal import find_peaks
from scipy.ndimage import maximum_filter1d

BASE = r"C:\Users\WuKW\Desktop\动态测试技术报告\from wkw\exp2_images\顾宇辽吴凯伟"


def load(path):
    data = np.genfromtxt(path, delimiter=",", encoding="utf-8",
                         filling_values=np.nan, invalid_raise=False)
    t, v = data[:, 9], data[:, 10]
    ok = ~(np.isnan(t) | np.isnan(v))
    return t[ok], v[ok]


def dt_autocorr(t, v, t_start=4e-6, lag_min=2e-6, lag_max=60e-6):
    m = t > t_start
    a = np.abs(v[m]) - np.mean(np.abs(v[m]))
    n = len(a)
    r = np.correlate(a, a, mode="full")[n - 1:]
    r /= r[0]
    dt = t[1] - t[0]
    i_min, i_max = int(lag_min / dt), min(int(lag_max / dt), n - 1)
    pk, _ = find_peaks(r[i_min:i_max], height=0.10, distance=int(1.5e-6 / dt))
    return (pk[0] + i_min) * dt if len(pk) else None


def burst_peaks(t, v, t_start=4e-6, rel=0.08):
    a = np.abs(v)
    dt = t[1] - t[0]
    win = max(int(1.0e-6 / dt), 51)
    env = maximum_filter1d(a, size=win, mode="nearest")
    after = t > t_start
    thr = rel * a[after].max()
    idx = np.flatnonzero((env > thr) & after)
    if len(idx) == 0:
        return []
    brk = np.flatnonzero(np.diff(t[idx]) > 2.5e-6)
    starts = np.r_[idx[0], idx[brk + 1]]
    ends = np.r_[idx[brk], idx[-1]] + 1
    out = []
    for s, e in zip(starts, ends):
        if t[e - 1] - t[s] < 0.3e-6:
            continue
        im = s + int(np.argmax(a[s:e]))
        out.append((t[im], a[im]))
    return out


def window_amp(t, v, t_center, half=1.0e-6):
    m = np.abs(t - t_center) <= half
    return np.abs(v[m]).max() if m.any() else np.nan


print("%-24s %10s %10s %10s %10s" % ("文件", "Δt(us)", "P1(V)", "P2(V)", "备注"))
for name in ["纯水", "钢-水", "铝-水", "玻璃-水",
             "钢5mhz纵波", "钢10mhz纵波", "玻璃5mhz纵波", "玻璃10mhz纵波",
             "钢5mhz横波增益10db", "铝5mhz横波增益10db", "玻璃5mhz横波增益30db"]:
    t, v = load(os.path.join(BASE, name + ".csv"))
    dt_ac = dt_autocorr(t, v)
    bursts = burst_peaks(t, v)
    note = ""
    if name == "纯水":
        # 水：入射波(t≈0)到第一次盆底回波的时间
        dt = bursts[0][0] if bursts else None
        P1 = bursts[0][1] if bursts else np.nan
        P2 = bursts[1][1] if len(bursts) > 1 else np.nan
        note = "Δt=首回波到达时间"
    else:
        if len(bursts) >= 2:
            dt = bursts[1][0] - bursts[0][0]
        else:
            dt = dt_ac
        if bursts:
            t_star = max(bursts, key=lambda b: b[1])[0]  # 最强回波
            P1 = window_amp(t, v, t_star)
            P2 = window_amp(t, v, t_star + dt) if dt else np.nan
        else:
            P1 = P2 = np.nan
        if len(bursts) < 2 and dt_ac is None:
            note = "仅检出一个回波"
        if dt_ac and len(bursts) >= 2 and abs(dt_ac - dt) / dt > 0.3:
            note = "自相关与包络不一致,人工核对"
    print("%-24s %10s %10s %10s  %s" % (
        name,
        "%.2f" % (dt * 1e6) if dt else "N/A",
        "%.3f" % P1 if P1 == P1 else "N/A",
        "%.3f" % P2 if P2 == P2 else "N/A",
        note))
