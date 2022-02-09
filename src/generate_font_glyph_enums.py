import re
import keyword

from fontTools import ttLib

from tools import writeFile, sortObject

font = ttLib.TTFont("./data/font.otf")
acc: dict = {}
# 获取 unicodeid: 字符名对照
for cmap in font["cmap"].tables:
    acc.update(cmap.cmap)

# 以 unicodeid 为键排序
acc = sortObject(acc)
acc_order = {}
# 翻转字典并将键中非法字符转为合法字符
for k, v in acc.items():
    v = re.sub(r"[^\w]", "_", v)
    if keyword.iskeyword(v):
        v = f"_{v}"
    acc_order[v] = k

# 构造输出
pretty_acc = "\n    ".join(f"{k} = {v}" for k, v in acc_order.items())
pretty = f"""from enum import Enum

class FontGlyphs(int, Enum):
    {pretty_acc}
"""
# 输出字符名到 unicodeid 对照表
writeFile("./output/d2_font_glyphs.py", pretty)
