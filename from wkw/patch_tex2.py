# -*- coding: utf-8 -*-
"""第二轮填充：把能算的量全部算好填入报告"""
import io

DST = r"C:\Users\WuKW\Desktop\动态测试技术报告\from wkw\实验二报告\实验二实验报告.tex"
with io.open(DST, encoding="utf-8") as f:
    s = f.read()

count = [0]


def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, "替换目标出现 %d 次（预期 %d）：%s" % (c, n, old[:60])
    s = s.replace(old, new)
    count[0] += 1


# ---------- 0. 填写说明更新 ----------
rep(r"表中由波形读取的时间差与回波幅值已填写；试件质量、尺寸、探头与盆底距离等现场读数及各计算结果留空，请按实验记录填写。",
    r"表中由波形读取的时间差、回波幅值以及由试件尺寸计算的波速、衰减系数、材料常数均已填写。试件为实验室共用试件，质量与尺寸采用同期同实验室测量值，请与本组实验记录核对；探头与盆底距离为现场装调量，仍留空。")

# ---------- 1. 密度表 + 密度结果 ----------
rep(r"""\multirow{3}{*}{钢} & 质量 $m_{st}$（g） & \blank[2.4cm]\\
 & 直径 $d_{st}$（mm） & \blank[2.4cm]\\
 & 厚度 $h_{st}$（mm） & \blank[2.4cm]\\""",
    r"""\multirow{3}{*}{钢} & 质量 $m_{st}$（g） & 81.940\\
 & 直径 $d_{st}$（mm） & 29.81\\
 & 厚度 $h_{st}$（mm） & 15.09\\""")
rep(r"""\multirow{3}{*}{铝} & 质量 $m_{al}$（g） & \blank[2.4cm]\\
 & 直径 $d_{al}$（mm） & \blank[2.4cm]\\
 & 厚度 $h_{al}$（mm） & \blank[2.4cm]\\""",
    r"""\multirow{3}{*}{铝} & 质量 $m_{al}$（g） & 29.472\\
 & 直径 $d_{al}$（mm） & 30.09\\
 & 厚度 $h_{al}$（mm） & 15.07\\""")
rep(r"""\multirow{4}{*}{有机玻璃} & 质量 $m_{og}$（g） & \blank[2.4cm]\\
 & 长度 $a_{og}$（mm） & \blank[2.4cm]\\
 & 宽度 $b_{og}$（mm） & \blank[2.4cm]\\
 & 厚度 $h_{og}$（mm） & \blank[2.4cm]\\""",
    r"""\multirow{4}{*}{有机玻璃} & 质量 $m_{og}$（g） & 129.228\\
 & 长度 $a_{og}$（mm） & 97.51\\
 & 宽度 $b_{og}$（mm） & 80.21\\
 & 厚度 $h_{og}$（mm） & 14.19\\""")
rep(r"分别测量钢、铝和有机玻璃试件的质量与尺寸，每个量记录一次，按试件形状计算密度。",
    r"分别测量钢、铝和有机玻璃试件的质量与尺寸，每个量记录一次，按试件形状计算密度。本组三种试件为实验室共用试件，质量与尺寸采用同期同实验室测量值，请与本组实验记录核对。")
rep(r"""  \rho_{st}&=\frac{4\times10^3m_{st}}{\pi d_{st}^{\,2}h_{st}}
  =\blank[2cm]\ \mathrm{g/cm^3},\\""",
    r"""  \rho_{st}&=\frac{4\times10^3m_{st}}{\pi d_{st}^{\,2}h_{st}}
  =7.780\ \mathrm{g/cm^3},\\""")
rep(r"""  \rho_{al}&=\frac{4\times10^3m_{al}}{\pi d_{al}^{\,2}h_{al}}
  =\blank[2cm]\ \mathrm{g/cm^3},\\""",
    r"""  \rho_{al}&=\frac{4\times10^3m_{al}}{\pi d_{al}^{\,2}h_{al}}
  =2.750\ \mathrm{g/cm^3},\\""")
rep(r"""  \rho_{og}&=\frac{10^3m_{og}}{a_{og}b_{og}h_{og}}
  =\blank[2cm]\ \mathrm{g/cm^3}.""",
    r"""  \rho_{og}&=\frac{10^3m_{og}}{a_{og}b_{og}h_{og}}
  =1.164\ \mathrm{g/cm^3}.""")

# ---------- 2. 水浸纵波波速 ----------
rep(r"""  C_{L,st}&=\frac{2h_{st}}{\Delta t_{L,st}}\times10^3
  =\blank[1.8cm]\ \mathrm{m/s},\\
  C_{L,al}&=\frac{2h_{al}}{\Delta t_{L,al}}\times10^3
  =\blank[1.8cm]\ \mathrm{m/s},\\
  C_{L,og}&=\frac{2h_{og}}{\Delta t_{L,og}}\times10^3
  =\blank[1.8cm]\ \mathrm{m/s}.""",
    r"""  C_{L,st}&=\frac{2h_{st}}{\Delta t_{L,st}}\times10^3
  =5976\ \mathrm{m/s},\\
  C_{L,al}&=\frac{2h_{al}}{\Delta t_{L,al}}\times10^3
  =6468\ \mathrm{m/s},\\
  C_{L,og}&=\frac{2h_{og}}{\Delta t_{L,og}}\times10^3
  =3744\ \mathrm{m/s}.""")
rep(r"""  \delta_{L,st}&=\frac{|C_{L,st}-5900|}{5900}\times100\%=\blank[1.8cm],\\
  \delta_{L,al}&=\frac{|C_{L,al}-6300|}{6300}\times100\%=\blank[1.8cm],\\
  \delta_{L,og}&=\frac{|C_{L,og}-2730|}{2730}\times100\%=\blank[1.8cm].""",
    r"""  \delta_{L,st}&=\frac{|C_{L,st}-5900|}{5900}\times100\%=1.3\%,\\
  \delta_{L,al}&=\frac{|C_{L,al}-6300|}{6300}\times100\%=2.7\%,\\
  \delta_{L,og}&=\frac{|C_{L,og}-2730|}{2730}\times100\%=37.1\%.""")
rep(r"结合信号强度、材料非均匀性和波峰位置的选取分析偏差。",
    r"结合信号强度、材料非均匀性和波峰位置的选取分析偏差。本组钢、铝结果与参考值吻合较好；有机玻璃水浸信号回波成分复杂，除上下表面回波外混有水面与盆底反射杂波，所识别回波间隔对应的波速与参考值偏差较大，仅供参考（有机玻璃纵波波速以接触式测量为准）。")

# ---------- 3. 水浸衰减系数 ----------
rep(r"钢 & 0.401，$m=1$ & 0.142，$n=2$ & \blank[1.3cm]\\",
    r"钢 & 0.401，$m=1$ & 0.142，$n=2$ & 2.99\\")
rep(r"铝 & 0.655，$m=1$ & 0.325，$n=2$ & \blank[1.3cm]\\",
    r"铝 & 0.655，$m=1$ & 0.325，$n=2$ & 2.02\\")
rep(r"有机玻璃 & 0.208，$m=1$ & 0.073，$n=2$ & \blank[1.3cm]\\",
    r"有机玻璃 & 0.208，$m=1$ & 0.073，$n=2$ & 3.20\\")

# ---------- 4. 横波 ----------
rep(r"有机玻璃 & 10.94\\", r"有机玻璃 & 21.99\\")
rep(r"由试件厚度与单次波形中的回波时间差计算横波波速：",
    r"有机玻璃横波信号中除 $22.0\,\mu$s 处的横波回波外，在 $11.1\,\mu$s 处还出现与纵波渡越时间相符的波包（$2h_{og}/C_{L,og}\approx10.4\,\mu$s），判断为横波探头激发时伴随的纵波成分；横波回波仅识别到一个清晰波包，故其 $\Delta t_S$ 取入射波与第一回波的时间差。由试件厚度与单次波形中的回波时间差计算横波波速：")
rep(r"""  C_{S,st}&=\frac{2h_{st}}{\Delta t_{S,st}}\times10^3
  =\blank[1.8cm]\ \mathrm{m/s},\\
  C_{S,al}&=\frac{2h_{al}}{\Delta t_{S,al}}\times10^3
  =\blank[1.8cm]\ \mathrm{m/s},\\
  C_{S,og}&=\frac{2h_{og}}{\Delta t_{S,og}}\times10^3
  =\blank[1.8cm]\ \mathrm{m/s}.""",
    r"""  C_{S,st}&=\frac{2h_{st}}{\Delta t_{S,st}}\times10^3
  =3249\ \mathrm{m/s},\\
  C_{S,al}&=\frac{2h_{al}}{\Delta t_{S,al}}\times10^3
  =3130\ \mathrm{m/s},\\
  C_{S,og}&=\frac{2h_{og}}{\Delta t_{S,og}}\times10^3
  =1291\ \mathrm{m/s}.""")
rep(r"""  \delta_{S,st}&=\frac{|C_{S,st}-3230|}{3230}\times100\%=\blank[1.8cm],\\
  \delta_{S,al}&=\frac{|C_{S,al}-3080|}{3080}\times100\%=\blank[1.8cm],\\
  \delta_{S,og}&=\frac{|C_{S,og}-1300|}{1300}\times100\%=\blank[1.8cm].""",
    r"""  \delta_{S,st}&=\frac{|C_{S,st}-3230|}{3230}\times100\%=0.6\%,\\
  \delta_{S,al}&=\frac{|C_{S,al}-3080|}{3080}\times100\%=1.6\%,\\
  \delta_{S,og}&=\frac{|C_{S,og}-1300|}{1300}\times100\%=0.7\%.""")

# ---------- 5. 材料常数 ----------
rep(r"根据前面测得的 5 MHz 纵波与横波波速，由式\eqref{eq:exp2-E}计算泊松比和弹性模量。",
    r"根据前面测得的 5 MHz 纵波与横波波速，由式\eqref{eq:exp2-E}计算泊松比和弹性模量。其中钢、铝纵波波速取水浸式测量值；有机玻璃水浸信号杂波较多，纵波波速取接触式 5 MHz 测量值 $2685\,\mathrm{m/s}$。")
rep(r"""  \nu_{st}&=\blank[1.5cm], & E_{st}&=\blank[1.5cm]\ \mathrm{GPa},\\
  \nu_{al}&=\blank[1.5cm], & E_{al}&=\blank[1.5cm]\ \mathrm{GPa},\\
  \nu_{og}&=\blank[1.5cm], & E_{og}&=\blank[1.5cm]\ \mathrm{GPa}.""",
    r"""  \nu_{st}&=0.290, & E_{st}&=211.9\ \mathrm{GPa},\\
  \nu_{al}&=0.347, & E_{al}&=72.6\ \mathrm{GPa},\\
  \nu_{og}&=0.350, & E_{og}&=5.24\ \mathrm{GPa}.""")
rep(r"""  \delta_{E,st}&=\frac{|E_{st}-207|}{207}\times100\%=\blank[1.2cm], &
  \delta_{\nu,st}&=\frac{|\nu_{st}-0.29|}{0.29}\times100\%=\blank[1.2cm],\\
  \delta_{E,al}&=\frac{|E_{al}-72|}{72}\times100\%=\blank[1.2cm], &
  \delta_{\nu,al}&=\frac{|\nu_{al}-0.33|}{0.33}\times100\%=\blank[1.2cm],\\
  \delta_{E,og}&=\frac{|E_{og}-3.16|}{3.16}\times100\%=\blank[1.2cm], &
  \delta_{\nu,og}&=\frac{|\nu_{og}-0.32|}{0.32}\times100\%=\blank[1.2cm].""",
    r"""  \delta_{E,st}&=\frac{|E_{st}-207|}{207}\times100\%=2.4\%, &
  \delta_{\nu,st}&=\frac{|\nu_{st}-0.29|}{0.29}\times100\%=0.1\%,\\
  \delta_{E,al}&=\frac{|E_{al}-72|}{72}\times100\%=0.8\%, &
  \delta_{\nu,al}&=\frac{|\nu_{al}-0.33|}{0.33}\times100\%=5.2\%,\\
  \delta_{E,og}&=\frac{|E_{og}-3.16|}{3.16}\times100\%=65.7\%, &
  \delta_{\nu,og}&=\frac{|\nu_{og}-0.32|}{0.32}\times100\%=9.3\%.""")
rep(r"分析测得的材料常数与参考值的差异，并考虑材料具体牌号、成分或状态不明确的影响。",
    r"分析测得的材料常数与参考值的差异，并考虑材料具体牌号、成分或状态不明确的影响。钢、铝结果与参考值吻合较好。有机玻璃弹性模量偏差较大，主要因为参考值本身不完全自洽：由参考波速 $C_L=2730$、$C_S=1300\,\mathrm{m/s}$ 反推的弹性模量约为 $5.2\,\mathrm{GPa}$，与参考值 $3.16\,\mathrm{GPa}$ 并不一致；本组测得 $E_{og}=5.24\,\mathrm{GPa}$，与波速反推值一致。")

# ---------- 6. 不同频率纵波 ----------
rep(r"""  C_{L,st}^{5\mathrm{MHz}}&=\frac{2h_{st}}{\Delta t_{L,st}^{5\mathrm{MHz}}}\times10^3
  =\blank[1.5cm]\ \mathrm{m/s},\\
  C_{L,st}^{10\mathrm{MHz}}&=\frac{2h_{st}}{\Delta t_{L,st}^{10\mathrm{MHz}}}\times10^3
  =\blank[1.5cm]\ \mathrm{m/s},\\
  C_{L,og}^{5\mathrm{MHz}}&=\frac{2h_{og}}{\Delta t_{L,og}^{5\mathrm{MHz}}}\times10^3
  =\blank[1.5cm]\ \mathrm{m/s},\\
  C_{L,og}^{10\mathrm{MHz}}&=\frac{2h_{og}}{\Delta t_{L,og}^{10\mathrm{MHz}}}\times10^3
  =\blank[1.5cm]\ \mathrm{m/s}.""",
    r"""  C_{L,st}^{5\mathrm{MHz}}&=\frac{2h_{st}}{\Delta t_{L,st}^{5\mathrm{MHz}}}\times10^3
  =5964\ \mathrm{m/s},\\
  C_{L,st}^{10\mathrm{MHz}}&=\frac{2h_{st}}{\Delta t_{L,st}^{10\mathrm{MHz}}}\times10^3
  =5964\ \mathrm{m/s},\\
  C_{L,og}^{5\mathrm{MHz}}&=\frac{2h_{og}}{\Delta t_{L,og}^{5\mathrm{MHz}}}\times10^3
  =2685\ \mathrm{m/s},\\
  C_{L,og}^{10\mathrm{MHz}}&=\frac{2h_{og}}{\Delta t_{L,og}^{10\mathrm{MHz}}}\times10^3
  =\text{仅检出单个回波，无法计算}.""")
rep(r"5 MHz & 2.188，$m=1$ & 0.203，$n=2$ & \blank[1.3cm]\\",
    r"5 MHz & 2.188，$m=1$ & 0.203，$n=2$ & 7.28\\")

with io.open(DST, "w", encoding="utf-8", newline="\n") as f:
    f.write(s)
print("done, %d 处替换" % count[0])
