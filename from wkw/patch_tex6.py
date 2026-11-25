# -*- coding: utf-8 -*-
"""第六轮：插入探伤总结图 + 填写封面信息"""
import io
import os
import shutil
from PIL import Image

PROJ = r"C:\Users\WuKW\Desktop\动态测试技术报告\from wkw\实验二报告"
DESK = r"C:\Users\WuKW\Desktop\实验二报告"

# 1. 图片拷入 exp2_images（ASCII 命名 + RGB 扁平化）
for src_name, dst_name in [("探伤 非斜探头.png", "weld_L_summary.png"),
                           ("探伤 斜探头.png", "weld_S_summary.png")]:
    im = Image.open(os.path.join(DESK, src_name)).convert("RGB")
    im.save(os.path.join(PROJ, "exp2_images", dst_name))
    print("saved", dst_name, im.size)

# 2. tex 替换
PATH = os.path.join(PROJ, "实验二实验报告.tex")
s = io.open(PATH, encoding="utf-8").read()
count = [0]


def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, "出现 %d 次（预期 %d）：%s" % (c, n, old[:60])
    s = s.replace(old, new)
    count[0] += 1


# 封面信息
rep(r"姓\qquad 名：\blank[2.5cm] & 学\qquad 号：\blank[3cm]",
    r"姓\qquad 名：吴凯伟 & 学\qquad 号：2601110100")
rep(r"同组成员：\blank[2.5cm] & 实验地点：\blank[3cm]",
    r"同组成员：顾宇辽 & 实验地点：力学楼 203")
rep(r"实验日期：\blank[2.5cm] &",
    r"实验日期：2026 年 10 月 21 日 &")

# 6.1 纵波图位
rep("""\\begin{figure}[H]
  \\centering
  \\framebox[16cm]{\\rule{0pt}{9cm}}
  \\caption{5 MHz 接触式纵波直探头测钢板焊缝（待插入本组图像）}
\\end{figure}""",
    """\\begin{figure}[H]
  \\centering
  \\includegraphics[width=16cm]{weld_L_summary.png}
  \\caption{5 MHz 接触式纵波直探头测钢板焊缝：各位置缺陷反射信号}
\\end{figure}""")

# 6.2 斜探头图位
rep("""\\begin{figure}[H]
  \\centering
  \\framebox[16cm]{\\rule{0pt}{9cm}}
  \\caption{1 MHz 接触式斜探头测钢板焊缝（待插入本组图像）}
\\end{figure}""",
    """\\begin{figure}[H]
  \\centering
  \\includegraphics[width=16cm]{weld_S_summary.png}
  \\caption{1 MHz 接触式斜探头测钢板焊缝：各位置缺陷反射信号}
\\end{figure}""")

# 填写说明
rep("探伤部分结果已按本组记录填写，图位留为 16 cm$\\times$9 cm 整体插图位置，待插入本组图像。",
    "探伤部分结果与图像均已按本组记录填写。")

io.open(PATH, "w", encoding="utf-8", newline="\n").write(s)
print("done, %d 处替换" % count[0])
