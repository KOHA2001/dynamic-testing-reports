# -*- coding: utf-8 -*-
"""在 codex 实验二单次测量版模板上做精准替换，生成本组报告 tex"""
import io
import re

SRC = r"C:\Users\WuKW\Documents\Codex\2026-10-24\bang\outputs\实验二实验报告_单次测量版.tex"
DST = r"C:\Users\WuKW\Desktop\动态测试技术报告\from wkw\实验二报告\实验二实验报告.tex"

with io.open(SRC, encoding="utf-8") as f:
    s = f.read()

count = [0]


def rep(old, new, n=1):
    """替换并断言次数"""
    global s
    c = s.count(old)
    assert c == n, "替换目标出现 %d 次（预期 %d）：%s" % (c, n, old[:60])
    s = s.replace(old, new)
    count[0] += 1


# ---------- 1. 图片替换 ----------
img_map = {
    "p08_img01.png": "water_global.png", "p08_img02.png": "water_zoom.png",
    "p09_img01.png": "steel_water_global.png", "p09_img02.png": "steel_water_zoom.png",
    "p09_img03.png": "alu_water_global.png", "p09_img04.png": "alu_water_zoom.png",
    "p10_img01.png": "glass_water_global.png", "p10_img02.png": "glass_water_zoom.png",
    "p11_img01.png": "steel_5S_global.png", "p11_img02.png": "steel_5S_zoom.png",
    "p12_img01.png": "alu_5S_global.png", "p12_img02.png": "alu_5S_zoom.png",
    "p13_img01.png": "glass_5S_global.png", "p13_img02.png": "glass_5S_zoom.png",
    "p14_img01.png": "steel_5L_global.png", "p14_img02.png": "steel_5L_zoom.png",
    "p14_img03.png": "steel_10L_global.png", "p14_img04.png": "steel_10L_zoom.png",
    "p15_img01.png": "glass_5L_global.png", "p15_img02.png": "glass_5L_zoom.png",
    "p16_img01.png": "glass_10L_global.png", "p16_img02.png": "glass_10L_zoom.png",
}
for old, new in img_map.items():
    rep(old, new)

# ---------- 2. 使用说明改写 ----------
rep(
    r"\noindent\textbf{使用说明：}以下实验结果图均从原报告提取，仅用于保留版式和读图示例。写作时请用同名文件替换为本组图像，并填写本组数据。",
    r"\noindent\textbf{填写说明：}本部分信号图均已替换为本组实测波形，表中由波形读取的时间差与回波幅值已填写；试件质量、尺寸、探头与盆底距离等现场读数及各计算结果留空，请按实验记录填写。探伤部分的三维图与损伤示意图暂为参考占位图，待替换。")

# ---------- 3. 图注 ----------
rep(r"\caption{5 MHz 测量水中纵波波速时信号图（请替换为本组图像）}",
    r"\caption{5 MHz 测量水中纵波波速时信号图}")
rep(r"\caption{5 MHz 接触式纵波直探头测钢板焊缝（请替换为本组图像）}",
    r"\caption{5 MHz 接触式纵波直探头测钢板焊缝（当前为参考占位图，待替换为本组图像）}")
rep(r"\caption{1 MHz 接触式纵波斜探头测钢板焊缝（请替换为本组图像）}",
    r"\caption{1 MHz 接触式斜探头测钢板焊缝（当前为参考占位图，待替换为本组图像）}")

# ---------- 4. 水中波速时间差 ----------
rep(r"$\Delta t$（$\mu$s） & \blank[2.4cm]\\",
    r"$\Delta t$（$\mu$s） & 69.81\\")

# ---------- 5. 水浸纵波时间差表 ----------
old_tab = r"""材料 & $\Delta t_L$（$\mu$s）\\
\midrule
钢 & \blank[2.4cm]\\
铝 & \blank[2.4cm]\\
有机玻璃 & \blank[2.4cm]\\"""
new_tab = r"""材料 & $\Delta t_L$（$\mu$s）\\
\midrule
钢 & 5.05\\
铝 & 4.66\\
有机玻璃 & 7.58\\"""
rep(old_tab, new_tab)

# ---------- 6. 水浸衰减表 ----------
old_tab = r"""钢 & \blank[1.2cm]，$m=$\blank[0.5cm] & \blank[1.2cm]，$n=$\blank[0.5cm] & \blank[1.3cm]\\
铝 & \blank[1.2cm]，$m=$\blank[0.5cm] & \blank[1.2cm]，$n=$\blank[0.5cm] & \blank[1.3cm]\\
有机玻璃 & \blank[1.2cm]，$m=$\blank[0.5cm] & \blank[1.2cm]，$n=$\blank[0.5cm] & \blank[1.3cm]\\"""
new_tab = r"""钢 & 0.401，$m=1$ & 0.142，$n=2$ & \blank[1.3cm]\\
铝 & 0.655，$m=1$ & 0.325，$n=2$ & \blank[1.3cm]\\
有机玻璃 & 0.208，$m=1$ & 0.073，$n=2$ & \blank[1.3cm]\\"""
rep(old_tab, new_tab)
rep(r"比较三种材料的衰减程度，并分析后续回波信号较弱时波峰读取对结果的影响。",
    r"比较三种材料的衰减程度，并分析后续回波信号较弱时波峰读取对结果的影响。注意本组有机玻璃水浸信号的第二回波幅值已接近噪声水平，其衰减系数仅供参考。")

# ---------- 7. 横波：增益 + 时间差表 ----------
rep(r"本组增益设置为\blank[1.5cm]。波形数据",
    r"本组增益设置为：钢、铝试件 10 dB，有机玻璃试件 30 dB。波形数据")
old_tab = r"""材料 & $\Delta t_S$（$\mu$s）\\
\midrule
钢 & \blank[2.4cm]\\
铝 & \blank[2.4cm]\\
有机玻璃 & \blank[2.4cm]\\"""
new_tab = r"""材料 & $\Delta t_S$（$\mu$s）\\
\midrule
钢 & 9.29\\
铝 & 9.63\\
有机玻璃 & 10.94\\"""
rep(old_tab, new_tab)

# ---------- 8. 不同频率纵波时间差表 ----------
old_tab = r"""钢 & 5 MHz & \blank[2cm]\\
钢 & 10 MHz & \blank[2cm]\\
有机玻璃 & 5 MHz & \blank[2cm]\\
有机玻璃 & 10 MHz & \blank[2cm]\\"""
new_tab = r"""钢 & 5 MHz & 5.06\\
钢 & 10 MHz & 5.06\\
有机玻璃 & 5 MHz & 10.57\\
有机玻璃 & 10 MHz & 仅检出单个回波\\"""
rep(old_tab, new_tab)

# ---------- 9. 不同频率有机玻璃衰减表 ----------
rep(r"5 MHz & \blank[1.2cm]，$m=$\blank[0.5cm] & \blank[1.2cm]，$n=$\blank[0.5cm] & \blank[1.3cm]\\",
    r"5 MHz & 2.188，$m=1$ & 0.203，$n=2$ & \blank[1.3cm]\\")
rep(r"10 MHz & \blank[1.2cm]，$m=$\blank[0.5cm] & \blank[1.2cm]，$n=$\blank[0.5cm] & \blank[1.3cm]\\",
    r"10 MHz & 0.378，$m=1$ & \multicolumn{2}{c}{仅检出单个回波，无法读取}\\")

# ---------- 10. 探伤增益 ----------
rep(r"本组信号增益为\blank[1.5cm]。当扫描路径上存在缺陷时",
    r"本组信号增益为 10 dB。当扫描路径上存在缺陷时")
rep(r"本组信号增益为\blank[2cm]，斜探头倾角为\blank[2cm]。",
    r"本组信号增益为 30 dB，斜探头倾角为\blank[2cm]。")

with io.open(DST, "w", encoding="utf-8", newline="\n") as f:
    f.write(s)
print("done, %d 处替换 -> %s" % (count[0], DST))
