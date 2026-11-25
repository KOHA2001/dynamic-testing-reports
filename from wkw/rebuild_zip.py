# -*- coding: utf-8 -*-
import re, os, zipfile

DST = r"C:\Users\WuKW\Desktop\实验二报告"
s = open(os.path.join(DST, "实验二实验报告.tex"), encoding="utf-8").read()
refs = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", s)
missing = [r for r in refs if not os.path.exists(os.path.join(DST, "exp2_images", r))]
print("引用图片:", len(refs), "| 缺失:", missing if missing else "无")

zip_path = r"C:\Users\WuKW\Desktop\实验二实验报告_Overleaf.zip"
files = [os.path.join(DST, "实验二实验报告.tex"), os.path.join(DST, "latexmkrc")]
for root, dirs, fs in os.walk(os.path.join(DST, "exp2_images")):
    for f in fs:
        files.append(os.path.join(root, f))
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for f in files:
        z.write(f, os.path.relpath(f, DST))
z = zipfile.ZipFile(zip_path)
names = z.namelist()
print("zip:", len(names), "files, %.1f MB" % (os.path.getsize(zip_path) / 1e6),
      "| 完整性:", "OK" if z.testzip() is None else "BAD")
for f in ["exp2_images/weld_L_summary.png", "exp2_images/weld_S_summary.png"]:
    print(f, "在 zip 里:", f in names)
