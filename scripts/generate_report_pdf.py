"""
Generate a PDF project report for Notexio from the Markdown source in /docs.

This is intentionally a lightweight Markdown-to-PDF converter tailored to the
report structure used in this repository (headings, paragraphs, bullet lists).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem,
)


def _escape_xml(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


_BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
_CODE_RE = re.compile(r"`([^`]+?)`")


def _format_inline(md: str) -> str:
    """
    Convert a small subset of Markdown inline syntax to ReportLab Paragraph XML.
    Supported:
      - **bold**
      - `code`
    """
    s = _escape_xml(md)

    # code first to avoid bold parsing inside code
    s = _CODE_RE.sub(lambda m: f'<font name="Courier">{_escape_xml(m.group(1))}</font>', s)
    s = _BOLD_RE.sub(lambda m: f"<b>{m.group(1)}</b>", s)
    return s


def _make_doc(out_path: Path):
    return SimpleDocTemplate(
        str(out_path),
        pagesize=letter,
        leftMargin=0.9 * inch,
        rightMargin=0.9 * inch,
        topMargin=0.85 * inch,
        bottomMargin=0.85 * inch,
        title="Notexio — Project Report (CSE323)",
        author="Notexio",
    )


def _build_styles():
    base = getSampleStyleSheet()

    styles = {
        "title": ParagraphStyle(
            "NotexioTitle",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            spaceAfter=14,
        ),
        "h1": ParagraphStyle(
            "NotexioH1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            spaceBefore=10,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "NotexioH2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=16,
            spaceBefore=8,
            spaceAfter=6,
        ),
        "p": ParagraphStyle(
            "NotexioP",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=14,
            spaceAfter=6,
        ),
        "bullet": ParagraphStyle(
            "NotexioBullet",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=14,
            leftIndent=14,
        ),
    }
    return styles


def _add_page_numbers(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    page_num = canvas.getPageNumber()
    canvas.drawRightString(doc.pagesize[0] - 0.9 * inch, 0.6 * inch, f"Page {page_num}")
    canvas.restoreState()


def markdown_to_flowables(md_text: str):
    styles = _build_styles()
    story = []

    lines = md_text.splitlines()
    para_buf: list[str] = []
    bullet_buf: list[str] = []

    def flush_paragraph():
        nonlocal para_buf
        if not para_buf:
            return
        text = " ".join(s.strip() for s in para_buf).strip()
        if text:
            story.append(Paragraph(_format_inline(text), styles["p"]))
        para_buf = []

    def flush_bullets():
        nonlocal bullet_buf
        if not bullet_buf:
            return
        items = [
            ListItem(Paragraph(_format_inline(item), styles["bullet"]))
            for item in bullet_buf
            if item.strip()
        ]
        if items:
            story.append(
                ListFlowable(
                    items,
                    bulletType="bullet",
                    leftIndent=18,
                    bulletFontName="Helvetica",
                    bulletFontSize=9,
                    bulletOffsetY=2,
                )
            )
            story.append(Spacer(1, 6))
        bullet_buf = []

    for raw in lines:
        line = raw.rstrip()

        if line.strip() == "---":
            flush_bullets()
            flush_paragraph()
            story.append(Spacer(1, 10))
            continue

        if line.startswith("# "):
            flush_bullets()
            flush_paragraph()
            story.append(Paragraph(_format_inline(line[2:].strip()), styles["title"]))
            continue

        if line.startswith("## "):
            flush_bullets()
            flush_paragraph()
            story.append(Paragraph(_format_inline(line[3:].strip()), styles["h1"]))
            continue

        if line.startswith("### "):
            flush_bullets()
            flush_paragraph()
            story.append(Paragraph(_format_inline(line[4:].strip()), styles["h2"]))
            continue

        if line.startswith("- "):
            flush_paragraph()
            bullet_buf.append(line[2:].strip())
            continue

        if not line.strip():
            flush_bullets()
            flush_paragraph()
            story.append(Spacer(1, 6))
            continue

        flush_bullets()
        para_buf.append(line)

    flush_bullets()
    flush_paragraph()
    return story


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    default_md = repo_root / "docs" / "Notexio_CSE323_Project_Report.md"
    default_pdf = repo_root / "docs" / "Notexio_CSE323_Project_Report.pdf"

    md_path = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else default_md
    pdf_path = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else default_pdf

    md_text = md_path.read_text(encoding="utf-8")
    story = markdown_to_flowables(md_text)

    doc = _make_doc(pdf_path)
    doc.build(story, onFirstPage=_add_page_numbers, onLaterPages=_add_page_numbers)
    print(f"Wrote: {pdf_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

