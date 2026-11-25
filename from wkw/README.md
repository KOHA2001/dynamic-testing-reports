# Overleaf 使用说明

1. 在 Overleaf 中选择 **New Project → Upload Project**，上传本压缩包。
2. 项目包含 5 份独立报告。在 **Menu → Main document** 中选择本次要编译的 `.tex` 文件。
3. 根目录的 `latexmkrc` 已设置使用 XeLaTeX。如果没有自动生效，请在 **Menu → Compiler** 中手动选择 **XeLaTeX**。
4. 每份报告通过 `\graphicspath` 引用对应的 `exp1_images` 至 `exp5_images` 文件夹，请保持目录结构不变。
5. 替换结果图时，可覆盖对应图片文件夹中的同名文件。

本地无需再安装 TeX 环境，Overleaf 会在线编译。
