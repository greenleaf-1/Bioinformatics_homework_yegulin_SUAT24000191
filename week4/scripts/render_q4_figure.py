from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures" / "Q4_variant_prioritization.png"
W, H = 3000, 1780
BG = "#F7F9FC"
NAVY = "#17324D"
BLUE = "#2F6FA3"
TEAL = "#188977"
GREEN = "#2C8C5A"
AMBER = "#D88A24"
RED = "#B84C4C"
GREY = "#566573"
LIGHT_BLUE = "#EAF3FA"
LIGHT_GREEN = "#E9F6EF"
LIGHT_AMBER = "#FFF4E3"
LIGHT_RED = "#FCECEC"
WHITE = "#FFFFFF"


def font(size, bold=False):
    name = "Arial Bold.ttf" if bold else "Arial.ttf"
    candidates = [
        Path("/Library/Fonts") / name,
        Path("/System/Library/Fonts/Supplemental") / name,
        Path("/usr/share/fonts/truetype/dejavu") / ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


F_TITLE = font(78, True)
F_SUB = font(36)
F_HEAD = font(42, True)
F_BODY = font(32)
F_SMALL = font(28)
F_BOLD = font(32, True)


def rounded(draw, box, fill, outline=None, width=3, radius=28):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def centered(draw, box, text, fnt, fill=NAVY):
    x1, y1, x2, y2 = box
    bb = draw.multiline_textbbox((0, 0), text, font=fnt, spacing=10, align="center")
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    draw.multiline_text(((x1 + x2 - tw) / 2, (y1 + y2 - th) / 2), text, font=fnt, fill=fill, spacing=10, align="center")


def arrow(draw, start, end, color=BLUE, width=10):
    draw.line([start, end], fill=color, width=width)
    ex, ey = end
    draw.polygon([(ex, ey), (ex - 28, ey - 18), (ex - 28, ey + 18)], fill=color)


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
d.text((140, 75), "Q4 Variant Prioritization", font=F_TITLE, fill=NAVY)
d.text((145, 175), "Transparent filters, evidence ranking, false-lead critique, and a functional test", font=F_SUB, fill=GREY)

# Main filter path
d.text((145, 285), "1. Apply the student-defined filters", font=F_HEAD, fill=NAVY)
boxes = [
    (145, 380, 560, 585, WHITE, BLUE, "12 synthetic\nvariants"),
    (680, 380, 1125, 585, LIGHT_BLUE, BLUE, "Technical quality\nFILTER=PASS\nDP >= 20; GQ >= 30"),
    (1245, 380, 1645, 585, LIGHT_BLUE, BLUE, "Rare variation\nAF <= 0.001"),
    (1765, 380, 2215, 585, LIGHT_BLUE, BLUE, "Potential impact\nsplice / stop /\nframeshift / missense"),
    (2335, 380, 2855, 585, LIGHT_GREEN, GREEN, "4 reliable\ncandidates"),
]
for x1, y1, x2, y2, fill, outline, label in boxes:
    rounded(d, (x1, y1, x2, y2), fill, outline)
    centered(d, (x1, y1, x2, y2), label, F_BODY)
for left, right in zip(boxes[:-1], boxes[1:]):
    arrow(d, (left[2] + 15, 482), (right[0] - 18, 482))

# Ranking and selection
d.text((145, 690), "2. Rank retained candidates using consequence and supplied clinical annotation", font=F_HEAD, fill=NAVY)
rounded(d, (145, 780, 1390, 1200), WHITE, "#CCD6E0")
headers = ["Rank", "Variant", "Gene", "Consequence", "Clinical label"]
xs = [185, 340, 680, 855, 1110]
for x, h in zip(xs, headers):
    d.text((x, 825), h, font=F_BOLD, fill=NAVY)
rows = [
    ("1", "chr17:7673803 G>A", "TP53", "splice acceptor", "Pathogenic"),
    ("2", "chr12:25398284 C>A", "KRAS", "missense", "Conflicting"),
    ("3", "chr13:32316461 C>T", "BRCA2", "missense", "VUS"),
    ("4", "chr19:11200200 C>T", "LDLR", "missense", "Likely benign"),
]
for i, row in enumerate(rows):
    y = 905 + i * 68
    if i == 0:
        d.rounded_rectangle((170, y - 8, 1360, y + 50), radius=15, fill=LIGHT_GREEN)
    for x, val in zip(xs, row):
        d.text((x, y), val, font=F_SMALL, fill=NAVY if i == 0 else GREY)

rounded(d, (1515, 780, 2855, 1200), LIGHT_GREEN, GREEN)
d.text((1585, 825), "Selected candidate", font=F_HEAD, fill=GREEN)
d.text((1585, 905), "TP53  chr17:7673803 G>A", font=font(44, True), fill=NAVY)
d.text((1585, 985), "PASS | DP 80 | GQ 99 | AF 0.00001", font=F_BODY, fill=NAVY)
d.text((1585, 1045), "splice_acceptor_variant | synthetic Pathogenic label", font=F_BODY, fill=NAVY)
d.text((1585, 1110), "Priority reflects combined evidence in this table, not patient-specific causality.", font=F_SMALL, fill=GREY)

# Caution and test
rounded(d, (145, 1300, 1450, 1655), LIGHT_RED, RED)
d.text((205, 1345), "Strongest false-lead concern", font=F_HEAD, fill=RED)
d.text((205, 1425), "No phenotype or inheritance model was supplied.\nThe gene–disease match therefore cannot be evaluated.\nThe ClinVar ID is illustrative and the splice effect is predicted.", font=F_BODY, fill=NAVY, spacing=18)

rounded(d, (1565, 1300, 2855, 1655), LIGHT_AMBER, AMBER)
d.text((1625, 1345), "Required experimental test", font=F_HEAD, fill=AMBER)
d.text((1625, 1425), "Confirm DNA call independently  ->  extract RNA  ->\nRT-PCR across flanking exons  ->  sequence cDNA  ->\nlook for exon skipping, intron retention, or cryptic splicing", font=F_BODY, fill=NAVY, spacing=18)

img.save(OUT, dpi=(300, 300))
print(OUT)
