"""
Generate the Notexio (CSE323) project report PDF.

Output:
  docs/Notexio_CSE323_Project_Report.pdf
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Spacer,
    Paragraph,
    PageBreak,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT_PDF = ROOT / "docs" / "Notexio_CSE323_Project_Report.pdf"


def _escape(text: str) -> str:
    """Escape text for ReportLab Paragraph (mini-markup)."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.grey)
    canvas.drawString(0.75 * inch, 0.5 * inch, "Notexio — CSE323 Project Report")
    canvas.drawRightString(8.0 * inch, 0.5 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf() -> Path:
    styles = getSampleStyleSheet()

    title = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=26,
        spaceAfter=14,
    )
    h1 = ParagraphStyle(
        "H1",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        spaceBefore=12,
        spaceAfter=6,
    )
    h2 = ParagraphStyle(
        "H2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        spaceBefore=10,
        spaceAfter=4,
    )
    body = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=14,
    )
    small = ParagraphStyle(
        "Small",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=12,
        textColor=colors.grey,
    )

    OUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUT_PDF),
        pagesize=LETTER,
        leftMargin=0.85 * inch,
        rightMargin=0.85 * inch,
        topMargin=0.85 * inch,
        bottomMargin=0.85 * inch,
        title="Notexio (CSE323) Project Report",
        author="Notexio",
    )

    story = []

    # Cover page
    story.append(Paragraph(_escape("Notexio"), title))
    story.append(Paragraph(_escape("CSE323 — Operating Systems Design"), h1))
    story.append(Paragraph(_escape("Project Report (STAR-format challenges)"), h2))
    story.append(Spacer(1, 0.25 * inch))

    meta_data = [
        ["Project name", "Notexio Text Editor"],
        ["Course", "CSE323 — Operating Systems Design"],
        ["Semester/Section", "[Fill]"],
        ["Student name", "[Fill]"],
        ["Student ID", "[Fill]"],
        ["Instructor", "[Fill]"],
        ["Date", str(date.today())],
    ]
    tbl = Table(meta_data, colWidths=[1.55 * inch, 4.75 * inch])
    tbl.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(tbl)
    story.append(Spacer(1, 0.35 * inch))
    story.append(
        Paragraph(
            _escape(
                "This report follows the course submission requirements: it includes project challenges in STAR format "
                "and provides a GitHub submission checklist (report PDF, GitHub Pages link placeholder, and demo video plan)."
            ),
            small,
        )
    )
    story.append(PageBreak())

    # Sections
    story.append(Paragraph(_escape("1) Abstract"), h1))
    story.append(
        Paragraph(
            _escape(
                "Notexio is a lightweight text editor built with Python and Tkinter. The project was designed as an OS-oriented "
                "application to practice file I/O, data persistence, event-driven GUI programming, and safe recovery mechanisms "
                "in the presence of crashes, forced exits, or unexpected shutdowns. The final system supports open/save, undo/redo, "
                "find/replace, usability features (status bar, line numbers, zoom, themes), and OS-adjacent integrations "
                "(printing via platform tools and exporting to PDF)."
            ),
            body,
        )
    )

    story.append(Paragraph(_escape("2) Project Overview"), h1))
    story.append(Paragraph(_escape("2.1 Goals"), h2))
    story.append(
        Paragraph(
            _escape(
                "• Build a stable, user-friendly editor that behaves like a modern Notepad-style app.<br/>"
                "• Demonstrate OS concepts through real features: file system interaction (open/save), concurrency considerations "
                "(auto-save without blocking UI), process/tool invocation (printing), and fault tolerance (recovery files)."
            ),
            body,
        )
    )
    story.append(Paragraph(_escape("2.2 Key Features Implemented"), h2))
    story.append(
        Paragraph(
            _escape(
                "• File operations: New/Open/Save/Save As, Open Recent, unsaved-change prompts<br/>"
                "• Editing: Undo/Redo, clipboard operations, Find/Replace, Go To Line<br/>"
                "• View: Zoom, word wrap, fullscreen, optional line numbers<br/>"
                "• Tools: statistics, reading time, duplicate-word highlight, remove extra spaces<br/>"
                "• Themes: light/dark/custom<br/>"
                "• Safety: optional auto-save, recovery files, warn on exit<br/>"
                "• Export/print: export as PDF, print preview, printing (platform-dependent)"
            ),
            body,
        )
    )

    story.append(Paragraph(_escape("3) System Design & Architecture"), h1))
    story.append(
        Paragraph(
            _escape(
                "Notexio uses a modular architecture. main.py wires together the components and passes shared references "
                "so modules can coordinate without duplicating state."
            ),
            body,
        )
    )
    story.append(Paragraph(_escape("3.1 Modules (high-signal responsibilities)"), h2))
    story.append(
        Paragraph(
            _escape(
                "• src/editor.py: Tk root + main text widget; modification tracking and title updates<br/>"
                "• src/file_manager.py: open/save, recent files, unsaved-change prompts<br/>"
                "• src/edit_operations.py: find/replace/go-to-line + clipboard + undo/redo<br/>"
                "• src/formatter.py: font and visual formatting controls<br/>"
                "• src/view_manager.py: zoom/word-wrap/fullscreen logic<br/>"
                "• src/tools.py: statistics + cleanup utilities<br/>"
                "• src/theme_manager.py: theme propagation across UI<br/>"
                "• src/safety_features.py: auto-save + recovery snapshots<br/>"
                "• src/misc_features.py: printing and PDF export<br/>"
                "• src/settings_manager.py: JSON persistence (config/settings.json)"
            ),
            body,
        )
    )
    story.append(Paragraph(_escape("3.2 OS concepts reflected"), h2))
    story.append(
        Paragraph(
            _escape(
                "• File I/O + persistence: explicit open/read/write; recent files and preferences persisted in JSON<br/>"
                "• Reliability: recovery files act as journaling-lite for user text<br/>"
                "• Concurrency model: GUI event loop; background timing must not block UI<br/>"
                "• System integration: printing delegates to OS tools/APIs"
            ),
            body,
        )
    )

    story.append(Paragraph(_escape("4) Challenges Faced (STAR format)"), h1))

    def star(title_text: str, situation: str, task: str, action: str, result: str, theory: str | None = None):
        story.append(Paragraph(_escape(title_text), h2))
        story.append(Paragraph(_escape(f"<b>Situation:</b> {situation}"), body))
        story.append(Paragraph(_escape(f"<b>Task:</b> {task}"), body))
        story.append(Paragraph(_escape(f"<b>Action:</b> {action}"), body))
        story.append(Paragraph(_escape(f"<b>Result:</b> {result}"), body))
        if theory:
            story.append(Spacer(1, 0.08 * inch))
            story.append(Paragraph(_escape(f"<i>Theory:</i> {theory}"), body))
        story.append(Spacer(1, 0.15 * inch))

    star(
        "Challenge 1 — Dirty state incorrect after programmatic loads/saves",
        "Tkinter’s Text widget can remain marked as “modified” after code-driven inserts/clears, causing false unsaved-change prompts.",
        "Make the “modified” indicator reflect real user edits only.",
        "Reset Tk’s internal modified flag after open/new/save operations and keep the app-level dirty flag synchronized with title/status.",
        "Opening/saving no longer triggers false prompts; the title shows * only when the user actually edits.",
        "Widgets maintain internal state for change events; applications must explicitly acknowledge when changes are intentional (file load) vs user edits.",
    )

    star(
        "Challenge 2 — Auto-save instability due to thread-unsafe UI access",
        "Auto-save used a background thread for timing, but reading Tkinter widgets from non-UI threads is unsafe and can crash intermittently.",
        "Keep UI responsive while ensuring recovery snapshots are created safely.",
        "Use root.after(...) to schedule snapshot creation on the UI event loop; the worker thread only sleeps and triggers scheduling.",
        "Auto-save remains non-blocking while eliminating thread-safety crashes.",
        "GUI frameworks often require thread confinement: all widget access must occur on the event-loop thread; after() safely queues work there.",
    )

    star(
        "Challenge 3 — Recovery files could grow without bounds",
        "Recovery snapshots are intentionally redundant, but without retention they can fill disk over time.",
        "Keep recovery useful while preventing uncontrolled storage growth.",
        "Implemented a retention policy that keeps only the most recent recovery files (sorted by modification time) and removes older ones.",
        "Recovery remains available for recent work while storage stays bounded.",
        "Bounded logs and log rotation are common OS patterns to prevent resource exhaustion.",
    )

    star(
        "Challenge 4 — PDF export failed on special characters",
        "ReportLab Paragraph accepts markup-like text; unescaped &, <, > can break parsing for normal user content.",
        "Make PDF export robust for code snippets and symbol-heavy text.",
        "Escaped reserved characters before creating Paragraph objects and built a simple paragraph/spacing layout.",
        "PDF export works reliably across typical user text.",
        "When a renderer supports markup, raw user text must be escaped to avoid accidental interpretation.",
    )

    star(
        "Challenge 5 — Printing behavior differed by OS",
        "Windows printing typically uses Win32 APIs, while Linux/macOS often use lp/lpr; dependencies may be missing.",
        "Provide printing with graceful fallbacks and clear feedback.",
        "Used OS detection: pywin32 path on Windows when available; otherwise invoke lp/lpr on Unix-like systems and show guidance if unavailable.",
        "Printing works where supported; users get actionable guidance if tooling/dependencies are missing.",
        "This reflects a common OS abstraction boundary: portable UI logic with OS-specific system services selected at runtime.",
    )

    star(
        "Challenge 6 — Status bar column index mismatched user expectations",
        "Tkinter reports cursor column indices as 0-based, but Notepad-style UIs show 1-based columns.",
        "Match user expectations for professional UX.",
        "Converted internal column values to 1-based for display.",
        "Status bar now shows Ln 1, Col 1 at document start, matching Notepad behavior.",
    )

    story.append(Paragraph(_escape("5) Validation / Test Plan (manual)"), h1))
    story.append(
        Paragraph(
            _escape(
                "• File I/O: open/edit/save/re-open; Save As default extension; recent files update<br/>"
                "• Safety: unsaved-change prompt; recovery restore on startup; auto-save snapshot creation<br/>"
                "• Export/print: export PDF containing < & >; print preview displays content<br/>"
                "• UX: status bar line/column and * indicator; zoom label updates; dark mode theming"
            ),
            body,
        )
    )

    story.append(Paragraph(_escape("6) How to Run"), h1))
    story.append(
        Paragraph(
            _escape("pip install -r requirements.txt<br/>python main.py"),
            body,
        )
    )

    story.append(Paragraph(_escape("7) Submission Package (matches course requirements)"), h1))
    story.append(
        Paragraph(
            _escape(
                "• GitHub folder submission: docs/Notexio_CSE323_Project_Report.pdf (and optional .md source)<br/>"
                "• GitHub page link submission: enable GitHub Pages and paste link here: [Fill after enabling]<br/>"
                "• Submission video demo (2–5 minutes): show open/save, find/replace, theme toggle, export PDF, recovery behavior; paste link: [Fill]<br/>"
                "• Short intro: Notexio is a Notepad-style editor emphasizing OS concepts: persistence, reliability, and system tool integration."
            ),
            body,
        )
    )

    doc.build(story, onFirstPage=_header_footer, onLaterPages=_header_footer)
    return OUT_PDF


if __name__ == "__main__":
    path = build_pdf()
    print(f"Generated: {path}")

