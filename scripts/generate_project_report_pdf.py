"""
Generate a PDF version of the Notexio CSE323 project report.

Input : docs/Notexio_CSE323_Project_Report.md
Output: docs/Notexio_CSE323_Project_Report.pdf
"""

from __future__ import annotations

import re
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


def _xml_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


_BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
_CODE_RE = re.compile(r"`([^`]+)`")


def _inline_format(md: str) -> str:
    """
    Convert a tiny subset of Markdown to ReportLab Paragraph markup.
    Supports:
      - **bold**
      - `inline code`
    """
    s = _xml_escape(md)
    s = _BOLD_RE.sub(r"<b>\1</b>", s)
    s = _CODE_RE.sub(r'<font face="Courier">\1</font>', s)
    return s


def build_pdf(md_path: Path, pdf_path: Path) -> None:
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        spaceAfter=12,
    )
    h1_style = ParagraphStyle(
        "H1",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        spaceBefore=10,
        spaceAfter=6,
    )
    h2_style = ParagraphStyle(
        "H2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        spaceBefore=8,
        spaceAfter=4,
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=14,
        spaceAfter=4,
    )

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        leftMargin=0.85 * inch,
        rightMargin=0.85 * inch,
        topMargin=0.85 * inch,
        bottomMargin=0.85 * inch,
        title="Notexio — CSE323 Project Report",
        author="Notexio",
    )

    lines = md_path.read_text(encoding="utf-8").splitlines()
    story: list = []

    bullet_buffer: list[str] = []

    def flush_bullets() -> None:
        nonlocal bullet_buffer, story
        if not bullet_buffer:
            return
        items = [
            ListItem(Paragraph(_inline_format(b), body_style), leftIndent=14)
            for b in bullet_buffer
        ]
        story.append(
            ListFlowable(
                items,
                bulletType="bullet",
                leftIndent=18,
                bulletFontName="Helvetica",
                bulletFontSize=10,
            )
        )
        story.append(Spacer(1, 6))
        bullet_buffer = []

    in_code_block = False

    for raw in lines:
        line = raw.rstrip("\n")

        if line.strip().startswith("```"):
            # Skip fenced code blocks entirely (not needed for this report).
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        if not line.strip():
            flush_bullets()
            story.append(Spacer(1, 6))
            continue

        if line.strip() == "---":
            flush_bullets()
            story.append(Spacer(1, 10))
            continue

        if line.startswith("# "):
            flush_bullets()
            story.append(Paragraph(_inline_format(line[2:].strip()), title_style))
            continue

        if line.startswith("## "):
            flush_bullets()
            story.append(Paragraph(_inline_format(line[3:].strip()), h1_style))
            continue

        if line.startswith("### "):
            flush_bullets()
            story.append(Paragraph(_inline_format(line[4:].strip()), h2_style))
            continue

        if line.lstrip().startswith("- "):
            bullet_buffer.append(line.lstrip()[2:].strip())
            continue

        # Normal paragraph (merge soft line breaks into same paragraph)
        flush_bullets()
        story.append(Paragraph(_inline_format(line.strip()), body_style))

    flush_bullets()
    doc.build(story)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    md_path = repo_root / "docs" / "Notexio_CSE323_Project_Report.md"
    pdf_path = repo_root / "docs" / "Notexio_CSE323_Project_Report.pdf"

    if not md_path.exists():
        raise SystemExit(f"Missing input report: {md_path}")

    build_pdf(md_path=md_path, pdf_path=pdf_path)
    print(f"Wrote: {pdf_path}")


if __name__ == "__main__":
    main()

