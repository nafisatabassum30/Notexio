"""
Generate a PDF report from docs/report.md using ReportLab.

Output:
  docs/Notexio_CSE323_Report.pdf

Notes:
  - This is a lightweight Markdown-to-PDF renderer (headings, paragraphs, bullets).
  - It intentionally supports only the subset used by docs/report.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable, List, Optional


@dataclass(frozen=True)
class Block:
    kind: str  # "h1" | "h2" | "h3" | "p" | "ul" | "hr" | "blank"
    lines: List[str]


def _escape_xml(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _read_md(path: Path) -> List[str]:
    text = path.read_text(encoding="utf-8")
    # Normalize newlines
    return text.replace("\r\n", "\n").replace("\r", "\n").split("\n")


_INLINE_RE = re.compile(
    r"""
    \[([^\]]+?)\]\((https?://[^)]+?)\)          # [text](url)
    | \*\*([^*]+?)\*\*                         # **bold**
    | `([^`]+?)`                               # `code`
    | (?<!\*)\*(?!\*)([^*]+?)(?<!\*)\*(?!\*)   # *italic* (single asterisks)
    | (?<!_)_(?!_)([^_]+?)(?<!_)_(?!_)         # _italic_ (single underscores)
    """,
    re.VERBOSE,
)


def _md_inline_to_reportlab_markup(text: str) -> str:
    """
    Convert a small subset of Markdown inline syntax to ReportLab Paragraph markup.
    Supports: **bold**, *italic*, _italic_, `code`, [text](url)
    """
    # Preserve <br/> tags inserted by our paragraph joiner.
    segments = text.split("<br/>")
    rendered: List[str] = []

    for seg in segments:
        out: List[str] = []
        last = 0
        for m in _INLINE_RE.finditer(seg):
            out.append(_escape_xml(seg[last : m.start()]))

            link_text, link_url = m.group(1), m.group(2)
            bold = m.group(3)
            code = m.group(4)
            italic_star = m.group(5)
            italic_us = m.group(6)

            if link_text is not None and link_url is not None:
                out.append(
                    f'<link href="{_escape_xml(link_url)}">{_escape_xml(link_text)}</link>'
                )
            elif bold is not None:
                out.append(f"<b>{_escape_xml(bold)}</b>")
            elif code is not None:
                out.append(f'<font face="Courier">{_escape_xml(code)}</font>')
            elif italic_star is not None:
                out.append(f"<i>{_escape_xml(italic_star)}</i>")
            elif italic_us is not None:
                out.append(f"<i>{_escape_xml(italic_us)}</i>")
            else:
                out.append(_escape_xml(m.group(0)))

            last = m.end()

        out.append(_escape_xml(seg[last:]))
        rendered.append("".join(out))

    return "<br/>".join(rendered)


def _to_blocks(lines: Iterable[str]) -> List[Block]:
    blocks: List[Block] = []
    cur_kind: Optional[str] = None
    cur_lines: List[str] = []

    def flush():
        nonlocal cur_kind, cur_lines
        if cur_kind is not None:
            blocks.append(Block(cur_kind, cur_lines))
        cur_kind = None
        cur_lines = []

    for raw in lines:
        line = raw.rstrip()
        # IMPORTANT: do NOT rstrip() here; Markdown hard-breaks depend on trailing spaces.
        line = raw

        if line.strip() == "":
            flush()
            blocks.append(Block("blank", []))
            continue

        if line.strip() == "---":
            flush()
            blocks.append(Block("hr", []))
            continue

        if line.startswith("# "):
            flush()
            blocks.append(Block("h1", [line[2:].strip()]))
            continue

        if line.startswith("## "):
            flush()
            blocks.append(Block("h2", [line[3:].strip()]))
            continue

        if line.startswith("### "):
            flush()
            blocks.append(Block("h3", [line[4:].strip()]))
            continue

        if line.startswith("- "):
        if line.rstrip().startswith("- "):
            if cur_kind not in (None, "ul"):
                flush()
            cur_kind = "ul"
            cur_lines.append(line[2:].strip())
            cur_lines.append(line.rstrip()[2:].strip())
            continue

        # Normal paragraph line (also allows simple hard line breaks)
        if cur_kind not in (None, "p"):
            flush()
        cur_kind = "p"
        cur_lines.append(line)

    flush()
    return blocks


def build_pdf(md_path: Path, pdf_path: Path) -> None:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        ListFlowable,
        ListItem,
        PageBreak,
    )

    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "NotexioTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        spaceAfter=12,
    )
    h2 = ParagraphStyle(
        "NotexioH2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        spaceBefore=10,
        spaceAfter=6,
    )
    h3 = ParagraphStyle(
        "NotexioH3",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        spaceBefore=8,
        spaceAfter=4,
    )
    body = ParagraphStyle(
        "NotexioBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=14,
        spaceAfter=6,
    )
    small = ParagraphStyle(
        "NotexioSmall",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=12,
        spaceAfter=4,
        textColor="#333333",
    )

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 9)
        canvas.setFillGray(0.35)
        canvas.drawRightString(doc.pagesize[0] - 0.75 * inch, 0.6 * inch, f"Page {doc.page}")
        canvas.restoreState()

    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        leftMargin=0.85 * inch,
        rightMargin=0.85 * inch,
        topMargin=0.85 * inch,
        bottomMargin=0.9 * inch,
        title="Notexio — CSE323 Project Report",
        author="Notexio",
    )

    blocks = _to_blocks(_read_md(md_path))
    story = []

    for b in blocks:
        if b.kind == "blank":
            story.append(Spacer(1, 0.12 * inch))
            continue
        if b.kind == "hr":
            story.append(Spacer(1, 0.12 * inch))
            story.append(Paragraph(_escape_xml("—" * 64), small))
            story.append(Spacer(1, 0.12 * inch))
            continue
        if b.kind == "h1":
            story.append(Paragraph(_escape_xml(b.lines[0]), title))
            continue
        if b.kind == "h2":
            story.append(Paragraph(_escape_xml(b.lines[0]), h2))
            continue
        if b.kind == "h3":
            story.append(Paragraph(_escape_xml(b.lines[0]), h3))
            continue
        if b.kind == "p":
            # Markdown "two spaces then newline" line breaks are already in report.md;
            # we convert them into <br/> for Paragraph.
            joined = " ".join([ln.strip() for ln in b.lines]).strip()
            # Preserve explicit Markdown hard-breaks "  " by turning trailing double-space into <br/>
            # (We keep it simple: if a line ends with two spaces, treat it as a break.)
            rebuilt_parts: List[str] = []
            # Preserve Markdown hard-breaks: lines ending with "  " should render as a new line.
            parts: List[str] = []
            for ln in b.lines:
                if ln.endswith("  "):
                    rebuilt_parts.append(ln.rstrip() + "<br/>")
                else:
                    rebuilt_parts.append(ln)
            joined = " ".join([p.strip() for p in rebuilt_parts]).strip()
            story.append(Paragraph(_escape_xml(joined).replace("&lt;br/&gt;", "<br/>"), body))
                hard_break = ln.endswith("  ")
                parts.append(ln.rstrip())
                parts.append("<br/>" if hard_break else " ")
            joined = "".join(parts).strip()

            story.append(Paragraph(_md_inline_to_reportlab_markup(joined), body))
            continue
        if b.kind == "ul":
            items = [
                ListItem(Paragraph(_escape_xml(item), body), leftIndent=12)
                ListItem(Paragraph(_md_inline_to_reportlab_markup(item), body), leftIndent=12)
                for item in b.lines
            ]
            story.append(
                ListFlowable(
                    items,
                    bulletType="bullet",
                    start="bullet",
                    leftIndent=18,
                    bulletFontName="Helvetica",
                    bulletFontSize=9,
                    bulletOffsetY=2,
                )
            )
            story.append(Spacer(1, 0.06 * inch))
            continue

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    md_path = repo_root / "docs" / "report.md"
    pdf_path = repo_root / "docs" / "Notexio_CSE323_Report.pdf"

    if not md_path.exists():
        raise SystemExit(f"Missing input: {md_path}")

    build_pdf(md_path, pdf_path)
    print(f"Generated: {pdf_path}")


if __name__ == "__main__":
    main()
