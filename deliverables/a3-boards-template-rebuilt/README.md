# 五角成戏 · 三张 A3 展板（模板重排版）

![三张展板预览](preview.jpg)

## 下载

- [三张 PNG + 三页 PDF 打包下载](./A3-boards-download.zip)
- [A3 三页 PDF](./A3-exhibition-boards.pdf)
- [01 掌上乾坤](./01-A3.png)
- [02 好戏入日常](./02-A3.png)
- [03 把好戏带回家](./03-A3.png)

## 成品规格

A3 竖版，297 × 420 mm。每张 PNG 为 3508 × 4961 px，输出分辨率 300 dpi；PDF 为三张准确 A3 页面。RGB 色彩，无额外出血。输出像素与原始素材细节不同：图片按其实际尺寸嵌入，具体有效分辨率见 image-resolution-record.json。文字、线条、栏目条及部分装饰在 PDF 中保留矢量，主视觉与样机为位图。

版式依照所给三张参考的主视觉占比、黑黄配色、栏目顺序与多栏结构重新排布，适配 A3 比例；采用所给素材，并补绘主视觉、包装、纹样和挂件。此版为根据模板重排的成品，不是参考图的逐像素复制。模板的跳号和模糊说明文字已重排。文创物件与五角色完整呈现，文化意象照片按横向画框取景。

## 排版源文件

source/layout.py 为可复现的排版脚本；source/input 为本次使用的上传原图，source/assets 为补充视觉、字体子集。部分素材引用同一仓库已有的 deliverables 文件。安装 source/requirements.txt 后，在完整仓库中运行 `python source/layout.py`。PDF 的文字与矢量装饰可在支持 PDF 编辑的软件中进一步调整；这份文件不声明为分层 PSD。
