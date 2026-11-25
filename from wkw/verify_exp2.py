# -*- coding: utf-8 -*-
"""数值复核：独立方法重提 Δt/幅值，并重算报告中所有派生量"""
import os
import math
import numpy as np
from scipy.signal import find_peaks
from scipy.ndimage import maximum_filter1d

BASE = r"C:\Users\WuKW\Desktop\动态测试技术报告\from wkw\exp2_images\顾宇辽吴凯伟"
OUT = r"C:\Users\WuKW\Desktop\动态测试技术报告\from wkw\verification.txt"
out = open(OUT, "w", encoding="utf-8")


def p(*a):
    print(*a)
    out.write(" ".join(str(x) for x in a) + "\n")


def load(path):
    d = np.genfromtxt(path, delimiter=",", encoding="utf-8",
                      filling_values=np.nan, invalid_raise=False)
    t, v = d[:, 9], d[:, 10]
    ok = ~(np.isnan(t) | np.isnan(v))
    return t[ok], v[ok]


def env_peaks(t, v, t_start=4e-6, min_dist_us=3.0, rel_prom=0.12):
    """包络上直接找峰（独立于自相关/分组的复核方法）"""
    a = np.abs(v)
    dt = t[1] - t[0]
    win = max(int(0.8e-6 / dt), 21)
    env = maximum_filter1d(a, size=win, mode="nearest")
    after = t > t_start
    prom = rel_prom * env[after].max()
    pk, _ = find_peaks(env, prominence=prom,
                       distance=int(min_dist_us * 1e-6 / dt))
    pk = pk[t[pk] > t_start]
    return [(t[i], env[i]) for i in pk]


p("========== 1. Δt 复核（包络峰值法） ==========")
checks = {
    "纯水": None,           # 首回波时间
    "钢-水": 5.05, "铝-水": 4.66, "玻璃-水": 7.58,
    "钢5mhz纵波": 5.06, "钢10mhz纵波": 5.06,
    "玻璃5mhz纵波": 10.57, "玻璃10mhz纵波": None,
    "钢5mhz横波增益10db": 9.29, "铝5mhz横波增益10db": 9.63,
    "玻璃5mhz横波增益30db": 21.99,
}
for name, expect in checks.items():
    t, v = load(os.path.join(BASE, name + ".csv"))
    peaks = env_peaks(t, v)
    tops = peaks[:6]
    desc = " ".join("%.2fμs/%.2fV" % (tp * 1e6, ap) for tp, ap in tops)
    if len(tops) >= 2:
        d = (tops[1][0] - tops[0][0]) * 1e6
        p("%-22s 报告Δt=%-6s 峰值序列: %s | 相邻间隔: %.2f us" %
          (name, expect, desc, d))
    else:
        p("%-22s 报告Δt=%-6s 峰值序列: %s" % (name, expect, desc))

p("")
p("========== 2. 派生量重算 ==========")
m = {"st": 81.940, "al": 29.472, "og": 129.228}
h = {"st": 15.09, "al": 15.07, "og": 14.19}
d_ = {"st": 29.81, "al": 30.09}
a_, b_ = 97.51, 80.21
rho = {"st": 4e3 * m["st"] / (math.pi * d_["st"]**2 * h["st"]),
       "al": 4e3 * m["al"] / (math.pi * d_["al"]**2 * h["al"]),
       "og": 1e3 * m["og"] / (a_ * b_ * h["og"])}
p("密度: st=%.3f al=%.3f og=%.3f  (报告 7.780/2.750/1.164)" %
  (rho["st"], rho["al"], rho["og"]))

dtL = {"st": 5.05, "al": 4.66, "og": 7.58}
dtS = {"st": 9.29, "al": 9.63, "og": 21.99}
CL = {k: 2 * h[k] / dtL[k] * 1e3 for k in dtL}
CS = {k: 2 * h[k] / dtS[k] * 1e3 for k in dtS}
p("C_L 水浸:", {k: round(v) for k, v in CL.items()}, "(报告 5976/6468/3744)")
p("C_S 接触:", {k: round(v) for k, v in CS.items()}, "(报告 3249/3130/1291)")
p("C_L 接触5MHz: st=%.0f og=%.0f  (报告 5964/2685)" %
  (2 * h["st"] / 5.06 * 1e3, 2 * h["og"] / 10.57 * 1e3))

refL = {"st": 5900, "al": 6300, "og": 2730}
refS = {"st": 3230, "al": 3080, "og": 1300}
p("误差L%:", {k: round(abs(CL[k] - refL[k]) / refL[k] * 100, 1) for k in CL},
  "(报告 1.3/2.7/37.1)")
p("误差S%:", {k: round(abs(CS[k] - refS[k]) / refS[k] * 100, 1) for k in CS},
  "(报告 0.6/1.6/0.7)")


def alpha(Pm, Pn, dmm):
    return 20 / (2 * dmm / 10) * math.log10(Pm / Pn)


p("α 水浸: st=%.2f al=%.2f og=%.2f  (报告 2.99/2.02/3.20)" % (
    alpha(0.401, 0.142, h["st"]), alpha(0.655, 0.325, h["al"]),
    alpha(0.208, 0.073, h["og"])))
p("α 玻璃接触5MHz: %.2f  (报告 7.28)" % alpha(2.188, 0.203, h["og"]))

CLuse = {"st": CL["st"], "al": CL["al"], "og": 2 * h["og"] / 10.57 * 1e3}
for k, name in [("st", "钢"), ("al", "铝"), ("og", "玻璃")]:
    r = CS[k] / CLuse[k]
    nu = (1 - 2 * r**2) / (2 - 2 * r**2)
    E = 2 * rho[k] * 1e3 * CS[k]**2 * (1 + nu) / 1e9
    p("%s: ν=%.4f E=%.2f GPa" % (name, nu, E))
p("(报告 ν: 0.290/0.347/0.350; E: 211.9/72.6/5.24)")

# 参考值自洽性检查
E_og_from_ref = 2 * 1164 * 1300**2 * (1 + ((1 - 2 * (1300 / 2730.)**2) / (2 - 2 * (1300 / 2730.)**2))) / 1e9
p("参考波速2730/1300反推E_og = %.2f GPa (报告称约5.2)" % E_og_from_ref)

p("")
p("========== 3. 水中 Δt 与回波一致性 ==========")
t, v = load(os.path.join(BASE, "纯水.csv"))
peaks = env_peaks(t, v, min_dist_us=20)
p("水的回波:", " ".join(["%.2fμs/%.2fV" % (tp * 1e6, ap) for tp, ap in peaks[:4]]))
p("报告 Δt=69.81 μs（首回波到达时间）")

out.close()
