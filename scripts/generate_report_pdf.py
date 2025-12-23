from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable, List, Optional


@dataclass(frozen=True)
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
        cur_kind = None
        cur_lines = []

    for raw in lines:
        line = raw.rstrip()
        # IMPORTANT: do NOT rstrip() here; Markdown hard-breaks depend on trailing spaces.
        line = raw

        if line.strip() == "":
            flush()
            blocks.append(Block("blank", []))
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
        Paragraph,
        Spacer,
        ListFlowable,
        ListItem,
        PageBreak,
    )

    styles = getSampleStyleSheet()
    title = ParagraphStyle(
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
