# -*- coding: utf-8 -*-
"""把自制波形图 PNG 从 RGBA 扁平化为 RGB（去掉 alpha 通道），修复 Overleaf/dvipdfmx 无法识别的问题。
参考图 p03~p06、p17 原本就是 RGB 且 Overleaf 能读，不动。"""
import os
from PIL import Image

IMG = r"C:\Users\WuKW\Desktop\动态测试技术报告\from wkw\实验二报告\exp2_images"

keep = {"p03_img01.png", "p03_img02.png", "p04_img01.png", "p05_img01.png",
        "p06_img01.png", "p17_img01.png", "p17_img02.png", "p17_img03.png",
        "p17_img04.png"}

n = 0
for root, dirs, files in os.walk(IMG):
    for f in files:
        if not f.endswith(".png") or f in keep:
            continue
        path = os.path.join(root, f)
        im = Image.open(path)
        if im.mode != "RGB":
            im.convert("RGB").save(path)  # PIL 默认不写有问题的附加块
            n += 1
print("re-encoded:", n)

# 复核：全部图片应为 colortype 2
import struct
bad = []
for root, dirs, files in os.walk(IMG):
    for f in files:
        if not f.endswith(".png"):
            continue
        with open(os.path.join(root, f), "rb") as fp:
            data = fp.read(40)
        w, h, depth, ctype, _, _, _ = struct.unpack(">IIBBBBB", data[16:29])
        if ctype != 2 or depth != 8:
            bad.append((f, ctype, depth))
print("仍非RGB的:", bad if bad else "无")
