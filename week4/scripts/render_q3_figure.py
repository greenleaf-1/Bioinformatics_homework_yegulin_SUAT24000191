from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


S = 2
W, H = 1500 * S, 790 * S
HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "figures" / "Q3_integrated_locus.png"
FONT = "/System/Library/Fonts/STHeiti Medium.ttc"


def font(size):
    return ImageFont.truetype(FONT, size * S)


img = Image.new("RGB", (W, H), "#f7f9ff")
d = ImageDraw.Draw(img)


def xy(box):
    return tuple(int(v * S) for v in box)


def centered(text, x, y, fnt, fill):
    left, top, right, bottom = d.textbbox((0, 0), text, font=fnt)
    d.text((x * S - (right - left) / 2, y * S - (bottom - top) / 2), text, font=fnt, fill=fill)


def arrow(x1, y1, x2, y2):
    d.line(xy((x1, y1, x2, y2)), fill="#52627a", width=3 * S)
    d.polygon([((x2 - 9) * S, (y2 - 6) * S), (x2 * S, y2 * S), ((x2 - 9) * S, (y2 + 6) * S)], fill="#52627a")


centered("Gene Y 候选调控区域：多组学证据链与因果检验", 750, 45, font(31), "#152238")
centered("原题仅提供数据类型，未提供任何信号方向或数值；前五步必须先读取真实数据", 750, 82, font(17), "#52627a")

cards = [
    (45, "#3f83b7", "1  Accessibility", "染色质可及性", "ATAC-seq", "读取候选区域峰值"),
    (285, "#7359ad", "2  Chromatin state", "活跃染色质状态", "H3K27ac ChIP/CUT&Tag", "读取 H3K27ac 富集"),
    (525, "#278c79", "3  Methylation", "DNA 甲基化", "CpG methylation", "读取 CpG 甲基化比例"),
    (765, "#c47b2a", "4  3D contact", "三维接触", "Hi-C / Micro-C", "读取启动子接触频率"),
    (1005, "#bd5367", "5  Expression", "Gene Y 表达", "RNA-seq", "与匹配对照比较表达"),
    (1245, "#405670", "6  Perturbation", "原位功能检验", "CRISPRi", "抑制候选区域后"),
]

for i, (x, color, step, label, assay, note) in enumerate(cards):
    d.rounded_rectangle(xy((x, 145, x + 210, 370)), radius=20 * S, fill="white", outline=color, width=2 * S)
    d.rounded_rectangle(xy((x, 145, x + 210, 193)), radius=20 * S, fill=color)
    d.rectangle(xy((x, 173, x + 210, 193)), fill=color)
    centered(step, x + 105, 169, font(17), "white")
    centered(label, x + 105, 225, font(20), "#152238")
    centered(assay, x + 105, 260, font(15), "#38506b")
    centered(note, x + 105, 301, font(15), "#52627a")
    if i < 5:
        centered("结果：题目未提供", x + 105, 330, font(14), "#7b4750")
    else:
        centered("检测 Gene Y 与邻近基因", x + 105, 330, font(14), "#52627a")
    if i < len(cards) - 1:
        arrow(x + 213, 258, x + 237, 258)

d.rounded_rectangle(xy((65, 430, 715, 700)), radius=22 * S, fill="#eef6ff", outline="#75a9d3", width=2 * S)
d.text((95 * S, 452 * S), "证据整合：只能在真实数据支持后建立候选模型", font=font(19), fill="#152238")
left_lines = [
    "• 多层信号一致 → 提高“候选增强子”的可信度",
    "• ATAC/H3K27ac/低甲基化 → 活跃状态相关证据",
    "• 三维接触 + Gene Y 表达 → 靶向关系的相关证据",
    "• 以上均不能单独或合并证明因果",
]
for n, line in enumerate(left_lines):
    d.text((95 * S, (500 + n * 36) * S), line, font=font(16), fill="#35465f")
d.text((95 * S, 652 * S), "当前结论：缺少实际信号，不能判定该区域是否为 Gene Y 增强子", font=font(14), fill="#7b4750")

d.rounded_rectangle(xy((755, 430, 1435, 700)), radius=22 * S, fill="#fff7ef", outline="#d39a54", width=2 * S)
d.text((785 * S, 452 * S), "可证伪设计：同时检验主模型与替代解释", font=font(19), fill="#152238")
right_lines = [
    "CRISPRi：多条独立 sgRNA + non-targeting 对照",
    "读取：Gene Y、候选区域附近其他基因、细胞状态/活力",
    "支持主模型：Gene Y 可重复下降，邻近基因无相同变化",
    "支持替代模型：其他基因改变而 Gene Y 不变",
    "组成混杂：在相同纯化细胞类型或单细胞层面复核",
]
for n, line in enumerate(right_lines):
    d.text((785 * S, (500 + n * 36) * S), line, font=font(16), fill="#35465f")

centered("逻辑箭头表示证据整合顺序，不表示前一步已经发生或自动导致下一步", 750, 752, font(17), "#52627a")

img.save(OUT, dpi=(300, 300), optimize=True)
print(OUT)
