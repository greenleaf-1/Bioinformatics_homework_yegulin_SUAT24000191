from __future__ import annotations

import html
import re
import subprocess
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Week4_Homework_Ye_Gulin_SUAT24000191.md"
OUTPUT_DIR = ROOT / "output" / "pdf"
OUTPUT = OUTPUT_DIR / "Week4_Homework_Ye_Gulin_SUAT24000191.pdf"
TMP_DIR = ROOT / "tmp" / "pdfs"

PAGE_W, PAGE_H = A4
LEFT = 18 * mm
RIGHT = 18 * mm
TOP = 18 * mm
BOTTOM = 17 * mm
CONTENT_W = PAGE_W - LEFT - RIGHT

NAVY = colors.HexColor("#17324D")
BLUE = colors.HexColor("#2F6FA3")
TEAL = colors.HexColor("#188977")
LIGHT_BLUE = colors.HexColor("#EAF3FA")
LIGHT_GREY = colors.HexColor("#F3F6F8")
MID_GREY = colors.HexColor("#D5DEE6")
DARK_GREY = colors.HexColor("#4E5D6C")


def register_fonts():
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
    try:
        pdfmetrics.registerFont(
            TTFont(
                "CJK",
                "/System/Library/Fonts/STHeiti Medium.ttc",
                subfontIndex=0,
            )
        )
        cjk = "CJK"
    except Exception:
        cjk = "STSong-Light"
    mono_path = "/System/Library/Fonts/Menlo.ttc"
    try:
        pdfmetrics.registerFont(TTFont("Mono", mono_path, subfontIndex=0))
        mono = "Mono"
    except Exception:
        mono = "Courier"
    return cjk, mono


CJK, MONO = register_fonts()


def normalize_text(text: str) -> str:
    return (
        html.unescape(text)
        .replace("\u2011", "-")
        .replace("\u2013", "-")
        .replace("\u2014", "-")
        .replace("\u2212", "-")
    )


def inline_markup(text: str) -> str:
    text = normalize_text(text)
    tokens: dict[str, str] = {}

    def hold(value: str) -> str:
        key = f"@@TOKEN{len(tokens)}@@"
        tokens[key] = value
        return key

    def code_repl(match):
        value = html.escape(match.group(1))
        return hold(f'<font name="{MONO}" color="#7A3E20">{value}</font>')

    def link_repl(match):
        label = html.escape(normalize_text(match.group(1)))
        url = html.escape(match.group(2), quote=True)
        return hold(f'<link href="{url}" color="#2F6FA3"><u>{label}</u></link>')

    text = re.sub(r"`([^`]+)`", code_repl, text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link_repl, text)
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    for key, value in tokens.items():
        text = text.replace(key, value)
    return text


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="BodyCJK",
        parent=styles["BodyText"],
        fontName=CJK,
        fontSize=9.6,
        leading=15.2,
        textColor=NAVY,
        spaceAfter=6,
        wordWrap="CJK",
        allowWidows=0,
        allowOrphans=0,
    )
)
styles.add(
    ParagraphStyle(
        name="H1CJK",
        parent=styles["Title"],
        fontName=CJK,
        fontSize=23,
        leading=30,
        textColor=NAVY,
        alignment=TA_CENTER,
        spaceAfter=12,
    )
)
styles.add(
    ParagraphStyle(
        name="H2CJK",
        parent=styles["Heading1"],
        fontName=CJK,
        fontSize=17,
        leading=23,
        textColor=NAVY,
        spaceBefore=3,
        spaceAfter=11,
        keepWithNext=True,
    )
)
styles.add(
    ParagraphStyle(
        name="H3CJK",
        parent=styles["Heading2"],
        fontName=CJK,
        fontSize=12.5,
        leading=17,
        textColor=TEAL,
        spaceBefore=9,
        spaceAfter=6,
        keepWithNext=True,
    )
)
styles.add(
    ParagraphStyle(
        name="MetaCJK",
        parent=styles["BodyText"],
        fontName=CJK,
        fontSize=11,
        leading=18,
        textColor=DARK_GREY,
        alignment=TA_CENTER,
        spaceAfter=5,
    )
)
styles.add(
    ParagraphStyle(
        name="QuoteCJK",
        parent=styles["BodyCJK"],
        leftIndent=9 * mm,
        rightIndent=5 * mm,
        borderColor=BLUE,
        borderWidth=1.5,
        borderPadding=(6, 8, 6, 10),
        backColor=LIGHT_BLUE,
        textColor=NAVY,
        spaceBefore=4,
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="BulletCJK",
        parent=styles["BodyCJK"],
        leftIndent=7 * mm,
        firstLineIndent=-3.5 * mm,
        bulletIndent=2 * mm,
        spaceAfter=3,
    )
)
styles.add(
    ParagraphStyle(
        name="TableCJK",
        parent=styles["BodyCJK"],
        fontSize=7.6,
        leading=10.5,
        spaceAfter=0,
    )
)
styles.add(
    ParagraphStyle(
        name="TableHeadCJK",
        parent=styles["TableCJK"],
        textColor=colors.white,
        alignment=TA_LEFT,
    )
)


class HomeworkDoc(BaseDocTemplate):
    def __init__(self, filename):
        super().__init__(
            filename,
            pagesize=A4,
            leftMargin=LEFT,
            rightMargin=RIGHT,
            topMargin=TOP,
            bottomMargin=BOTTOM,
            title="Week 4 Homework - Ye Gulin - SUAT24000191",
            author="Ye Gulin",
            subject="Bioinformatics: From Multi-Omics Data to Discovery",
        )
        frame = Frame(LEFT, BOTTOM, CONTENT_W, PAGE_H - TOP - BOTTOM, id="body")
        self.addPageTemplates(PageTemplate(id="main", frames=[frame], onPage=self.header_footer))

    @staticmethod
    def header_footer(canvas, doc):
        canvas.saveState()
        if doc.page > 1:
            canvas.setStrokeColor(MID_GREY)
            canvas.setLineWidth(0.5)
            canvas.line(LEFT, PAGE_H - 12 * mm, PAGE_W - RIGHT, PAGE_H - 12 * mm)
            canvas.setFont(CJK, 7.5)
            canvas.setFillColor(DARK_GREY)
            canvas.drawString(LEFT, PAGE_H - 9 * mm, "Bioinformatics: From Multi-Omics Data to Discovery")
            canvas.drawRightString(PAGE_W - RIGHT, PAGE_H - 9 * mm, "Week 4 Homework")
        canvas.setFont(CJK, 8)
        canvas.setFillColor(DARK_GREY)
        canvas.drawCentredString(PAGE_W / 2, 8 * mm, f"{doc.page}")
        canvas.restoreState()


def image_flowable(relative: str):
    path = ROOT / relative
    max_w = CONTENT_W
    max_h = 112 * mm
    if path.suffix.lower() == ".svg":
        TMP_DIR.mkdir(parents=True, exist_ok=True)
        raster = TMP_DIR / f"{path.stem}_pdf.png"
        node = "/Users/theaye/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node"
        sharp = "/Users/theaye/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp"
        script = (
            f'const sharp=require("{sharp}");'
            'sharp(process.argv[1],{density:220}).png().toFile(process.argv[2])'
            '.then(()=>process.exit(0)).catch(e=>{console.error(e);process.exit(1)})'
        )
        subprocess.run([node, "-e", script, str(path), str(raster)], check=True)
        path = raster
    item = Image(str(path))
    scale = min(max_w / item.imageWidth, max_h / item.imageHeight)
    item.drawWidth = item.imageWidth * scale
    item.drawHeight = item.imageHeight * scale
    item.hAlign = "CENTER"
    return item


def table_flowable(lines: list[str]):
    raw_rows = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        raw_rows.append(cells)
    if len(raw_rows) > 1 and all(re.fullmatch(r":?-{3,}:?", x.replace(" ", "")) for x in raw_rows[1]):
        raw_rows.pop(1)
    cols = len(raw_rows[0])
    if cols == 3:
        widths = [CONTENT_W * 0.22, CONTENT_W * 0.53, CONTENT_W * 0.25]
    elif cols == 4:
        widths = [CONTENT_W * 0.18, CONTENT_W * 0.31, CONTENT_W * 0.31, CONTENT_W * 0.20]
    elif cols == 5:
        widths = [CONTENT_W * 0.10, CONTENT_W * 0.25, CONTENT_W * 0.16, CONTENT_W * 0.25, CONTENT_W * 0.24]
    else:
        widths = [CONTENT_W / cols] * cols
    data = []
    for r, row in enumerate(raw_rows):
        style = styles["TableHeadCJK"] if r == 0 else styles["TableCJK"]
        data.append([Paragraph(inline_markup(cell), style) for cell in row])
    table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT", splitByRow=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.45, MID_GREY),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_GREY]),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def parse_markdown(source: str):
    lines = source.splitlines()
    story = []
    i = 0
    seen_title = False
    question_count = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line:
            i += 1
            continue
        if line == "---":
            story.append(Spacer(1, 4 * mm))
            i += 1
            continue
        image_match = re.fullmatch(r"!\[([^]]*)\]\(([^)]+)\)", line)
        if image_match:
            story.extend([Spacer(1, 3 * mm), image_flowable(image_match.group(2)), Spacer(1, 4 * mm)])
            i += 1
            continue
        if line.startswith("# "):
            if not seen_title:
                story.append(Spacer(1, 35 * mm))
                story.append(Paragraph(inline_markup(line[2:]), styles["H1CJK"]))
                story.append(Spacer(1, 6 * mm))
                seen_title = True
            i += 1
            continue
        if line.startswith("## "):
            question_count += 1
            story.append(PageBreak())
            story.append(Paragraph(inline_markup(line[3:]), styles["H2CJK"]))
            i += 1
            continue
        if line.startswith("### "):
            story.append(Paragraph(inline_markup(line[4:]), styles["H3CJK"]))
            i += 1
            continue
        if line.startswith("**Course:**") or line.startswith("**Student:**") or line.startswith("**Student ID:**"):
            story.append(Paragraph(inline_markup(line), styles["MetaCJK"]))
            if line.startswith("**Student ID:**"):
                story.append(Spacer(1, 8 * mm))
                story.append(Paragraph("Evidence-aware analysis, verification, and reproducible workflows", styles["MetaCJK"]))
                story.append(Spacer(1, 105 * mm))
                story.append(Paragraph("Submitted course artifact", styles["MetaCJK"]))
            i += 1
            continue
        if line.startswith("> "):
            parts = []
            while i < len(lines) and lines[i].startswith("> "):
                parts.append(lines[i][2:])
                i += 1
            story.append(Paragraph(inline_markup(" ".join(parts)), styles["QuoteCJK"]))
            continue
        if line.startswith("| "):
            block = []
            while i < len(lines) and lines[i].startswith("|"):
                block.append(lines[i])
                i += 1
            story.extend([Spacer(1, 2 * mm), table_flowable(block), Spacer(1, 4 * mm)])
            continue
        if line.startswith("- "):
            while i < len(lines) and lines[i].startswith("- "):
                story.append(Paragraph(inline_markup(lines[i][2:]), styles["BulletCJK"], bulletText="•"))
                i += 1
            story.append(Spacer(1, 2 * mm))
            continue

        parts = [line]
        i += 1
        while i < len(lines):
            nxt = lines[i].rstrip()
            if not nxt or nxt.startswith(("#", "|", "> ", "- ", "![")) or nxt == "---":
                break
            parts.append(nxt)
            i += 1
        paragraph = " ".join(parts)
        style = styles["QuoteCJK"] if paragraph.startswith("**The ") or paragraph.startswith("**Variant ") else styles["BodyCJK"]
        story.append(Paragraph(inline_markup(paragraph), style))
    return story


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = HomeworkDoc(str(OUTPUT))
    story = parse_markdown(SOURCE.read_text(encoding="utf-8"))
    doc.build(story)
    print(OUTPUT)


if __name__ == "__main__":
    main()
