# -*- coding: utf-8 -*-
"""把波形图拷入 TeX 项目 exp2_images/，ASCII 命名；并拷贝通用示意图与探伤占位图"""
import os
import shutil

SRC = r"C:\Users\WuKW\Desktop\动态测试技术报告\from wkw\exp2_images"
BASE = os.path.join(SRC, "顾宇辽吴凯伟")
PROJ = r"C:\Users\WuKW\Desktop\动态测试技术报告\from wkw\实验二报告"
IMG = os.path.join(PROJ, "exp2_images")
os.makedirs(IMG, exist_ok=True)

# 材料测量：csv名 -> ASCII前缀
mats = {
    "纯水": "water",
    "钢-水": "steel_water", "铝-水": "alu_water", "玻璃-水": "glass_water",
    "钢5mhz纵波": "steel_5L", "钢10mhz纵波": "steel_10L",
    "玻璃5mhz纵波": "glass_5L", "玻璃10mhz纵波": "glass_10L",
    "钢5mhz横波增益10db": "steel_5S", "铝5mhz横波增益10db": "alu_5S",
    "玻璃5mhz横波增益30db": "glass_5S",
}
n = 0
for cn, en in mats.items():
    for kind, suffix in [("全局", "global"), ("局部", "zoom")]:
        src = os.path.join(BASE, "波形图", "材料测量", "%s_%s.png" % (cn, kind))
        dst = os.path.join(IMG, "%s_%s.png" % (en, suffix))
        shutil.copyfile(src, dst)
        n += 1

# 焊缝探伤：保留目录结构
weld_map = {"探伤斜探头横波1mhz增益30db": "weld_S", "探伤纵波5hz增益10db": "weld_L"}
weld_src = os.path.join(BASE, "波形图", "焊缝探伤")
for cn_dir, en in weld_map.items():
    out_sub = os.path.join(IMG, en)
    os.makedirs(out_sub, exist_ok=True)
    for f in os.listdir(os.path.join(weld_src, cn_dir)):
        if f.endswith(".png"):
            # 17weak_全局.png -> pos17_weak_global.png
            stem = f[:-4].replace(" ", "")
            name, kind = stem.rsplit("_", 1)
            kind_en = {"全局": "global", "局部": "zoom"}[kind]
            import re
            m = re.match(r"(\d+)(.*)", name)
            pos, tag = m.group(1), m.group(2)
            dst = os.path.join(out_sub, "pos%s%s_%s.png" % (
                pos, "_" + tag if tag else "", kind_en))
            shutil.copyfile(os.path.join(weld_src, cn_dir, f), dst)
            n += 1

# 通用示意图（实验指导书图，各组通用）
for f in ["p03_img01.png", "p03_img02.png", "p04_img01.png",
          "p05_img01.png", "p06_img01.png"]:
    shutil.copyfile(os.path.join(SRC, f), os.path.join(IMG, f))
    n += 1

# 探伤三维图/损伤图占位（其他组数据，待本组替换）
for f in ["p17_img01.png", "p17_img02.png", "p17_img03.png", "p17_img04.png"]:
    shutil.copyfile(os.path.join(SRC, f), os.path.join(IMG, f))
    n += 1

print("copied %d files -> %s" % (n, IMG))
