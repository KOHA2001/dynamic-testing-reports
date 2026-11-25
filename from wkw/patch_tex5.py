# -*- coding: utf-8 -*-
"""第五轮：探伤部分写入本组结果；并排子图改为 16cm×9cm 整体插图位"""
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


# ---------- 6.1 钢板侧面垂直入射（5 MHz 纵波直探头，增益 10 dB） ----------
rep("记录缺陷反射主要出现的时间区间：\\blank[3cm]。在该区间取反射波形波峰和波谷对应信号强度绝对值中的最大值，作为该位置缺陷大小的度量，并绘制缺陷大小随位置变化的图线。",
    "记录缺陷反射主要出现的时间区间：$4\\times10^{-5}\\sim7\\times10^{-5}\\,\\mathrm{s}$。在该区间取反射波形波峰和波谷对应信号强度绝对值中的最大值，作为该位置缺陷大小的度量，并绘制缺陷大小随位置变化的图线。")

fig61_old = """\\begin{figure}[H]
\\centering
\\begin{minipage}[t]{0.48\\textwidth}
  \\centering
  \\includegraphics[width=\\linewidth]{p17_img01.png}
  （a）信号三维立体图
\\end{minipage}\\hfill
\\begin{minipage}[t]{0.48\\textwidth}
  \\centering
  \\includegraphics[width=\\linewidth]{p17_img02.png}
  （b）损伤示意图
\\end{minipage}
\\caption{5 MHz 接触式纵波直探头测钢板焊缝（当前为参考占位图，待替换为本组图像）}
\\end{figure}"""
fig61_new = """\\begin{figure}[H]
  \\centering
  \\framebox[16cm]{\\rule{0pt}{9cm}}
  \\caption{5 MHz 接触式纵波直探头测钢板焊缝（待插入本组图像）}
\\end{figure}"""
rep(fig61_old, fig61_new)

# ---------- 6.2 钢板表面斜入射（1 MHz 斜探头，增益 30 dB，60°） ----------
rep("本组信号增益为 30 dB，斜探头倾角为\\blank[2cm]。记录缺陷反射主要出现的时间区间：\\blank[3cm]。",
    "本组信号增益为 30 dB，斜探头倾角为 $60^{\\circ}$。记录缺陷反射主要出现的时间区间：$6\\times10^{-5}\\sim8\\times10^{-5}\\,\\mathrm{s}$。")

fig62_old = """\\begin{figure}[H]
\\centering
\\begin{minipage}[t]{0.48\\textwidth}
  \\centering
  \\includegraphics[width=\\linewidth]{p17_img03.png}
  （a）信号三维立体图
\\end{minipage}\\hfill
\\begin{minipage}[t]{0.48\\textwidth}
  \\centering
  \\includegraphics[width=\\linewidth]{p17_img04.png}
  （b）损伤示意图
\\end{minipage}
\\caption{1 MHz 接触式斜探头测钢板焊缝（当前为参考占位图，待替换为本组图像）}
\\end{figure}"""
fig62_new = """\\begin{figure}[H]
  \\centering
  \\framebox[16cm]{\\rule{0pt}{9cm}}
  \\caption{1 MHz 接触式斜探头测钢板焊缝（待插入本组图像）}
\\end{figure}"""
rep(fig62_old, fig62_new)

# ---------- 缺陷位置与长度判断（两处，按顺序） ----------
blank_line = "\\noindent 缺陷位置与长度判断：\\blank[0.72\\textwidth]"
assert s.count(blank_line) == 2
s = s.replace(blank_line,
              "\\noindent 缺陷位置与长度判断：缺陷信号在 4--6 cm、14--18 cm 及 20--25 cm 处出现。", 1)
s = s.replace(blank_line,
              "\\noindent 缺陷位置与长度判断：缺陷在 4--6 cm、14--17 cm 及 20--23 cm 处出现。", 1)
count[0] += 2

# ---------- 填写说明更新 ----------
rep("探伤部分的三维图与损伤示意图暂为参考占位图，待替换。",
    "探伤部分结果已按本组记录填写，图位留为 16 cm$\\times$9 cm 整体插图位置，待插入本组图像。")

io.open(PATH, "w", encoding="utf-8", newline="\n").write(s)
print("done, %d 处替换" % count[0])
