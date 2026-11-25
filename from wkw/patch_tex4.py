# -*- coding: utf-8 -*-
"""第四轮：用本组实测质量/尺寸/距离替换全部数据并重算所有派生量"""
import io

PATH = r"C:\Users\WuKW\Desktop\动态测试技术报告\from wkw\实验二报告\实验二实验报告.tex"
s = io.open(PATH, encoding="utf-8").read()
count = [0]


def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, "出现 %d 次（预期 %d）：%s" % (c, n, old[:60])
    s = s.replace(old, new)
    count[0] += 1


# ---------- 填写说明 & 共用试件备注 ----------
rep("本部分信号图均已替换为本组实测波形，表中由波形读取的时间差、回波幅值以及由试件尺寸计算的波速、衰减系数、材料常数均已填写。试件为实验室共用试件，质量与尺寸采用同期同实验室测量值，请与本组实验记录核对；探头与盆底距离为现场装调量，仍留空。探伤部分的三维图与损伤示意图暂为参考占位图，待替换。",
    "本部分信号图均为本组实测波形；试件质量、尺寸及探头与盆底距离均为本组现场读数；时间差、回波幅值及各计算结果均已填写。探伤部分的三维图与损伤示意图暂为参考占位图，待替换。")
rep("本组三种试件为实验室共用试件，质量与尺寸采用同期同实验室测量值，请与本组实验记录核对。", "")

# ---------- 密度表 ----------
rep(r"质量 $m_{st}$（g） & 81.940\\", r"质量 $m_{st}$（g） & 81.943\\")
rep(r"直径 $d_{st}$（mm） & 29.81\\", r"直径 $d_{st}$（mm） & 29.8\\")
rep(r"厚度 $h_{st}$（mm） & 15.09\\", r"厚度 $h_{st}$（mm） & 15.05\\")
rep(r"质量 $m_{al}$（g） & 29.472\\", r"质量 $m_{al}$（g） & 29.468\\")
rep(r"直径 $d_{al}$（mm） & 30.09\\", r"直径 $d_{al}$（mm） & 30.0\\")
rep(r"厚度 $h_{al}$（mm） & 15.07\\", r"厚度 $h_{al}$（mm） & 15.02\\")
rep(r"质量 $m_{og}$（g） & 129.228\\", r"质量 $m_{og}$（g） & 131.189\\")
rep(r"长度 $a_{og}$（mm） & 97.51\\", r"长度 $a_{og}$（mm） & 98.9\\")
rep(r"宽度 $b_{og}$（mm） & 80.21\\", r"宽度 $b_{og}$（mm） & 80.4\\")
rep(r"厚度 $h_{og}$（mm） & 14.19\\", r"厚度 $h_{og}$（mm） & 14.1\\")
rep(r"=7.780\ \mathrm{g/cm^3}", r"=7.806\ \mathrm{g/cm^3}")
rep(r"=2.750\ \mathrm{g/cm^3}", r"=2.776\ \mathrm{g/cm^3}")
rep(r"=1.164\ \mathrm{g/cm^3}", r"=1.170\ \mathrm{g/cm^3}")

# ---------- 水中波速 ----------
rep(r"距离 $h$（mm） & \blank[2.4cm]\\", r"距离 $h$（mm） & 50\\")
rep("""  C_{water}=\\frac{2h}{\\Delta t}\\times10^3
  =\\blank[2cm]\\ \\mathrm{m/s}.""",
    """  C_{water}=\\frac{2h}{\\Delta t}\\times10^3
  =1432\\ \\mathrm{m/s}.""")
rep("""  \\delta_{water}=\\frac{|C_{water}-1480|}{1480}\\times100\\%
  =\\blank[2cm].""",
    """  \\delta_{water}=\\frac{|C_{water}-1480|}{1480}\\times100\\%
  =3.2\\%.""")

# ---------- 水浸纵波 ----------
rep(r"=5976\ \mathrm{m/s}", r"=5960\ \mathrm{m/s}")
rep(r"=6468\ \mathrm{m/s}", r"=6446\ \mathrm{m/s}")
rep(r"=3744\ \mathrm{m/s}", r"=3720\ \mathrm{m/s}")
rep(r"\delta_{L,st}&=\frac{|C_{L,st}-5900|}{5900}\times100\%=1.3\%",
    r"\delta_{L,st}&=\frac{|C_{L,st}-5900|}{5900}\times100\%=1.0\%")
rep(r"\delta_{L,al}&=\frac{|C_{L,al}-6300|}{6300}\times100\%=2.7\%",
    r"\delta_{L,al}&=\frac{|C_{L,al}-6300|}{6300}\times100\%=2.3\%")
rep(r"\delta_{L,og}&=\frac{|C_{L,og}-2730|}{2730}\times100\%=37.1\%",
    r"\delta_{L,og}&=\frac{|C_{L,og}-2730|}{2730}\times100\%=36.3\%")

# ---------- 水浸衰减 ----------
rep(r"钢 & 0.401，$m=1$ & 0.142，$n=2$ & 2.99\\", r"钢 & 0.401，$m=1$ & 0.142，$n=2$ & 3.00\\")
rep(r"铝 & 0.655，$m=1$ & 0.325，$n=2$ & 2.02\\", r"铝 & 0.655，$m=1$ & 0.325，$n=2$ & 2.03\\")
rep(r"有机玻璃 & 0.208，$m=1$ & 0.073，$n=2$ & 3.20\\", r"有机玻璃 & 0.208，$m=1$ & 0.073，$n=2$ & 3.23\\")

# ---------- 横波 ----------
rep(r"=3249\ \mathrm{m/s}", r"=3240\ \mathrm{m/s}")
rep(r"=3130\ \mathrm{m/s}", r"=3119\ \mathrm{m/s}")
rep(r"=1291\ \mathrm{m/s}", r"=1282\ \mathrm{m/s}")
rep(r"\delta_{S,st}&=\frac{|C_{S,st}-3230|}{3230}\times100\%=0.6\%",
    r"\delta_{S,st}&=\frac{|C_{S,st}-3230|}{3230}\times100\%=0.3\%")
rep(r"\delta_{S,al}&=\frac{|C_{S,al}-3080|}{3080}\times100\%=1.6\%",
    r"\delta_{S,al}&=\frac{|C_{S,al}-3080|}{3080}\times100\%=1.3\%")
rep(r"\delta_{S,og}&=\frac{|C_{S,og}-1300|}{1300}\times100\%=0.7\%",
    r"\delta_{S,og}&=\frac{|C_{S,og}-1300|}{1300}\times100\%=1.4\%")
rep(r"（$2h_{og}/C_{L,og}\approx10.4\,\mu$s）", r"（$2h_{og}/C_{L,og}\approx10.3\,\mu$s）")

# ---------- 材料常数 ----------
rep(r"纵波波速取接触式 5 MHz 测量值 $2685\,\mathrm{m/s}$", r"纵波波速取接触式 5 MHz 测量值 $2668\,\mathrm{m/s}$")
rep(r"E_{st}&=211.9\ \mathrm{GPa}", r"E_{st}&=211.5\ \mathrm{GPa}")
rep(r"E_{al}&=72.6\ \mathrm{GPa}", r"E_{al}&=72.8\ \mathrm{GPa}")
rep(r"E_{og}&=5.24\ \mathrm{GPa}", r"E_{og}&=5.19\ \mathrm{GPa}")
rep(r"\delta_{E,st}&=\frac{|E_{st}-207|}{207}\times100\%=2.4\%",
    r"\delta_{E,st}&=\frac{|E_{st}-207|}{207}\times100\%=2.2\%")
rep(r"\delta_{E,al}&=\frac{|E_{al}-72|}{72}\times100\%=0.8\%",
    r"\delta_{E,al}&=\frac{|E_{al}-72|}{72}\times100\%=1.1\%")
rep(r"\delta_{E,og}&=\frac{|E_{og}-3.16|}{3.16}\times100\%=65.7\%",
    r"\delta_{E,og}&=\frac{|E_{og}-3.16|}{3.16}\times100\%=64.4\%")

# ---------- 频率对比 ----------
rep(r"=5964\ \mathrm{m/s}", r"=5949\ \mathrm{m/s}", n=2)
rep(r"=2685\ \mathrm{m/s}", r"=2668\ \mathrm{m/s}")
rep(r"=2604\ \mathrm{m/s}", r"=2587\ \mathrm{m/s}")
rep(r"5 MHz & 2.188，$m=1$ & 0.203，$n=2$ & 7.28\\", r"5 MHz & 2.188，$m=1$ & 0.203，$n=2$ & 7.32\\")

# ---------- 分析段落中的数字 ----------
rep(r"分别为 $5976\,\mathrm{m/s}$ 和 $6468\,\mathrm{m/s}$，与参考值偏差仅 $1.3\%$ 和 $2.7\%$",
    r"分别为 $5960\,\mathrm{m/s}$ 和 $6446\,\mathrm{m/s}$，与参考值偏差仅 $1.0\%$ 和 $2.3\%$")
rep(r"分别为钢 $2.99\,\mathrm{dB/cm}$、铝 $2.02\,\mathrm{dB/cm}$、有机玻璃 $3.20\,\mathrm{dB/cm}$",
    r"分别为钢 $3.00\,\mathrm{dB/cm}$、铝 $2.03\,\mathrm{dB/cm}$、有机玻璃 $3.23\,\mathrm{dB/cm}$")
rep(r"分别为 $3249\,\mathrm{m/s}$ 和 $3130\,\mathrm{m/s}$",
    r"分别为 $3240\,\mathrm{m/s}$ 和 $3119\,\mathrm{m/s}$")
rep(r"本组测得 $E_{og}=5.24\,\mathrm{GPa}$，与波速反推值一致",
    r"本组测得 $E_{og}=5.19\,\mathrm{GPa}$，与波速反推值一致")
rep(r"钢的弹性模量 $211.9\,\mathrm{GPa}$、泊松比 $0.290$，铝为 $72.6\,\mathrm{GPa}$ 和 $0.347$",
    r"钢的弹性模量 $211.5\,\mathrm{GPa}$、泊松比 $0.290$，铝为 $72.8\,\mathrm{GPa}$ 和 $0.347$")
rep(r"均为 $5964\,\mathrm{m/s}$，与水浸法结果 $5976\,\mathrm{m/s}$ 仅差 $0.2\%$",
    r"均为 $5949\,\mathrm{m/s}$，与水浸法结果 $5960\,\mathrm{m/s}$ 仅差 $0.2\%$")
rep(r"有机玻璃 5 MHz 接触式结果为 $2685\,\mathrm{m/s}$", r"有机玻璃 5 MHz 接触式结果为 $2668\,\mathrm{m/s}$")
rep(r"估算值为 $2604\,\mathrm{m/s}$", r"估算值为 $2587\,\mathrm{m/s}$")
rep(r"衰减系数为 $7.28\,\mathrm{dB/cm}$，明显大于水浸法结果 $3.20\,\mathrm{dB/cm}$",
    r"衰减系数为 $7.32\,\mathrm{dB/cm}$，明显大于水浸法结果 $3.23\,\mathrm{dB/cm}$")

io.open(PATH, "w", encoding="utf-8", newline="\n").write(s)
print("done, %d 处替换" % count[0])
