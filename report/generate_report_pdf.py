"""
Generate the CSE323 Notexio project report as a PDF.

Usage:
  python3 report/generate_report_pdf.py

Output:
  report/Notexio_CSE323_Project_Report.pdf
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Iterable


def _escape_xml(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.drawRightString(doc.pagesize[0] - 36, 20, f"Page {doc.page}")
    canvas.restoreState()


def _p(Paragraph, styles, text: str, style_name: str = "BodyText"):
    return Paragraph(_escape_xml(text), styles[style_name])


def _bullets(ListFlowable, ListItem, Paragraph, styles, items: Iterable[str], level: int = 0):
    left = 18 * (level + 1)
    return ListFlowable(
        [
            ListItem(
                Paragraph(_escape_xml(item), styles["BodyText"]),
                leftIndent=left,
            )
            for item in items
        ],
        bulletType="bullet",
        leftIndent=left,
    )


def build_pdf(out_path: Path) -> None:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        ListFlowable,
        ListItem,
        Paragraph,
        SimpleDocTemplate,
        Spacer,
    )

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            spaceAfter=14,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H1",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            spaceBefore=12,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H2",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            spaceBefore=10,
            spaceAfter=4,
        )
    )
    styles["BodyText"].leading = 14

    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=42,
        bottomMargin=42,
        title="Notexio — CSE323 Project Report",
        author="(fill in your name)",
    )

    story = []

    # Cover
    story.append(_p(Paragraph, styles, "Notexio — CSE323 (Operating Systems Design) Project Report", "ReportTitle"))
    story.append(_p(Paragraph, styles, "Project: Notexio Text Editor (Python + Tkinter)"))
    story.append(_p(Paragraph, styles, "Course: CSE323 — Operating Systems Design"))
    story.append(_p(Paragraph, styles, "Version: 1.0.0"))
    story.append(_p(Paragraph, styles, f"Date: {date.today().isoformat()}"))
    story.append(_p(Paragraph, styles, "Author: <Your Name> | Student ID: <Your ID>"))
    story.append(Spacer(1, 0.35 * inch))

    story.append(_p(Paragraph, styles, "Short introduction (what the project is)", "H1"))
    story.append(
        _p(
            Paragraph,
            styles,
            "Notexio is a lightweight, customizable text editor built with Python and Tkinter. "
            "It was designed as an OS-focused course project to demonstrate practical OS-adjacent concepts "
            "such as file I/O, safe persistence, event-driven GUI programming, and basic OS integration "
            "(printing, filesystem interactions, configuration storage).",
        )
    )
    story.append(Spacer(1, 0.12 * inch))
    story.append(
        _bullets(
            ListFlowable,
            ListItem,
            Paragraph,
            styles,
            [
                "File operations: new/open/save/save as, recent files, unsaved-change prompts.",
                "Editing: undo/redo, find/replace, go-to-line, clipboard operations.",
                "Formatting and view: fonts, colors, zoom, fullscreen, word wrap, line numbers.",
                "Tools: document statistics, reading time, cleanup utilities.",
                "Safety: recovery snapshots and optional auto-save.",
                "OS integration: printing and export as PDF.",
            ],
        )
    )

    story.append(Spacer(1, 0.2 * inch))
    story.append(_p(Paragraph, styles, "GitHub submission links (required)", "H1"))
    story.append(_p(Paragraph, styles, "GitHub repository: <paste your repo link here>"))
    story.append(_p(Paragraph, styles, "GitHub Pages link: <paste your GitHub Pages link here>"))
    story.append(_p(Paragraph, styles, "2–5 minute demo video: <paste your YouTube/Drive link here>"))

    story.append(Spacer(1, 0.2 * inch))
    story.append(_p(Paragraph, styles, "Project structure (high-level)", "H1"))
    story.append(
        _bullets(
            ListFlowable,
            ListItem,
            Paragraph,
            styles,
            [
                "main.py: application entry point, menu bar, shortcut bindings.",
                "src/file_manager.py: open/save/recent files + unsaved-change workflow.",
                "src/safety_features.py: recovery files + optional auto-save.",
                "src/misc_features.py: printing and PDF export, optional drag & drop.",
                "src/ui_components.py: toolbar, status bar, and line numbers UI.",
                "Other modules: editor core, edit operations, formatter, view manager, tools, theme and settings managers.",
            ],
        )
    )

    story.append(Spacer(1, 0.2 * inch))
    story.append(_p(Paragraph, styles, "OS / Systems concepts demonstrated", "H1"))
    story.append(
        _bullets(
            ListFlowable,
            ListItem,
            Paragraph,
            styles,
            [
                "File I/O and persistence: UTF-8 reads/writes, path handling, exceptions, saved vs. dirty state.",
                "Safe shutdown and data-loss prevention: save / don’t save / cancel prompts; recovery-file strategy.",
                "Threads vs. UI event loops: Tkinter is single-threaded; background timing must hand off widget work to the UI thread.",
                "Cross-platform OS integration: platform-specific printing and dependency fallbacks.",
            ],
        )
    )

    story.append(Spacer(1, 0.2 * inch))
    story.append(_p(Paragraph, styles, "Challenges faced (STAR format) — problems and fixes", "H1"))

    def star(title: str, situation: str, task: str, action: list[str], result: list[str], theory: str):
        story.append(_p(Paragraph, styles, title, "H2"))
        story.append(_p(Paragraph, styles, f"<b>Situation:</b> {situation}"))
        story.append(_p(Paragraph, styles, f"<b>Task:</b> {task}"))
        story.append(_p(Paragraph, styles, "<b>Action:</b>"))
        story.append(_bullets(ListFlowable, ListItem, Paragraph, styles, action, level=0))
        story.append(_p(Paragraph, styles, "<b>Result:</b>"))
        story.append(_bullets(ListFlowable, ListItem, Paragraph, styles, result, level=0))
        story.append(_p(Paragraph, styles, f"<b>Theory / notes:</b> {theory}"))
        story.append(Spacer(1, 0.15 * inch))

    star(
        "Challenge 1 — Auto-save crashes due to unsafe Tkinter access (Thread-safety)",
        "Auto-save ran on a background thread and intermittently caused freezes or instability.",
        "Implement reliable periodic recovery without blocking the UI or violating Tkinter thread-safety rules.",
        [
            "Identified root cause: Tkinter widgets are not thread-safe; calling Text.get() from a worker thread is undefined behavior.",
            "Scheduled content snapshot on the UI thread via root.after(...).",
            "Wrote recovery files on a worker thread (disk I/O) and added millisecond timestamps to avoid collisions.",
        ],
        [
            "Auto-save became stable and predictable.",
            "UI stayed responsive while still producing recovery snapshots.",
            "Recovery filename collisions were eliminated.",
        ],
        "Tkinter runs a single-threaded event loop; all widget access must occur on the UI thread. "
        "Using after() safely queues work on that loop; disk writes can be offloaded to a worker thread.",
    )

    star(
        "Challenge 2 — Preventing data loss on exit (Unsaved-change workflow)",
        "Users could lose work if the editor closed without a consistent prompt and save path.",
        "Provide a safe close workflow like real editors (save / don’t save / cancel).",
        [
            "Tracked a dedicated is_modified flag (dirty state).",
            "On new/open/exit, prompted the user and routed the decision to save or cancel.",
            "Updated UI indicators (title/status bar) so users can see unsaved state.",
        ],
        [
            "Accidental data loss was prevented.",
            "Behavior matched user expectations from standard desktop editors.",
        ],
        "Because persistence is explicit (writes happen only on save), the app must gate destructive actions "
        "using a reliable dirty-state model.",
    )

    star(
        "Challenge 3 — “Open Recent” menu opened the wrong file (Closure capture bug)",
        "Dynamic menu generation can accidentally bind all items to the last loop variable value.",
        "Ensure each menu item opens its corresponding file.",
        [
            "Used a lambda default argument: command=lambda fp=filepath: open_file(fp).",
            "Refreshed the menu after open/save to keep the list accurate.",
        ],
        [
            "Each entry opened the correct file consistently.",
        ],
        "Python closures are late-bound; default arguments evaluate immediately and capture the intended value.",
    )

    star(
        "Challenge 4 — PDF export broke on special characters (Markup escaping)",
        "ReportLab Paragraph interprets text as markup; characters like &, <, > can break rendering.",
        "Export arbitrary plain text to PDF reliably.",
        [
            "Escaped markup-sensitive characters before building Paragraph objects.",
            "Split the document into lines and added spacing for readability.",
        ],
        [
            "PDF export worked for normal text and code-like content without errors.",
        ],
        "Escaping prevents the PDF text engine from parsing user content as tags/entities.",
    )

    star(
        "Challenge 5 — Printing is OS-dependent (Windows vs. Linux/macOS)",
        "Printing uses different OS mechanisms and Python integrations on different platforms.",
        "Support printing where possible and fail gracefully otherwise.",
        [
            "On Windows, attempted pywin32-based printing; displayed a clear message when missing.",
            "On Linux/macOS, printed via system commands (lp/lpr) using a temporary file.",
            "Added a print preview window to validate content before printing.",
        ],
        [
            "Cross-platform printing became possible with clear fallbacks.",
            "The app avoided crashes when dependencies were missing.",
        ],
        "Printing is an OS service; robust apps detect platform capabilities and degrade gracefully with user guidance.",
    )

    star(
        "Challenge 6 — Line numbers drifted during scrolling (UI sync)",
        "The line-number gutter could desynchronize from the text while scrolling and editing.",
        "Keep line numbers aligned with the text widget’s scroll position.",
        [
            "Updated line numbers on modifications and synced scroll via yview() fractions.",
            "Repacked widgets on toggle to keep layout stable.",
        ],
        [
            "Line numbers remained aligned during normal editing and scrolling.",
        ],
        "Using yview() as the single source of truth avoids drift caused by multiple scroll inputs (wheel, scrollbar, programmatic).",
    )

    story.append(_p(Paragraph, styles, "Test plan (what I verified)", "H1"))
    story.append(
        _bullets(
            ListFlowable,
            ListItem,
            Paragraph,
            styles,
            [
                "Open/save files and verify correct content persisted.",
                "Modify content and verify the unsaved indicator and prompt-on-exit flow.",
                "Generate and restore recovery files from the recovery/ directory.",
                "Export PDF and open it to verify readability.",
                "Toggle line numbers and scroll to confirm alignment.",
            ],
        )
    )

    story.append(Spacer(1, 0.2 * inch))
    story.append(_p(Paragraph, styles, "Demo video plan (2–5 minutes, required)", "H1"))
    story.append(
        _bullets(
            ListFlowable,
            ListItem,
            Paragraph,
            styles,
            [
                "Show GitHub repo + GitHub Pages page (submission requirement).",
                "Create/edit a file; show modified indicator.",
                "Find/Replace and Go-to-Line quickly.",
                "Recent files menu demonstration.",
                "Zoom + line numbers + theme toggle.",
                "Export as PDF and open the result.",
                "Exit with unsaved changes to show safety prompt.",
            ],
        )
    )

    story.append(Spacer(1, 0.2 * inch))
    story.append(_p(Paragraph, styles, "Conclusion", "H1"))
    story.append(
        _p(
            Paragraph,
            styles,
            "Notexio demonstrates OS design concepts through a real GUI application: safe file I/O, "
            "graceful OS integration, and reliability-focused features like recovery and safe shutdown. "
            "Key lessons were event-driven design, cross-platform behavior, and building safeguards "
            "that mirror professional desktop editors.",
        )
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.build(story, onFirstPage=_footer, onLaterPages=_footer)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    out_path = repo_root / "report" / "Notexio_CSE323_Project_Report.pdf"
    build_pdf(out_path)
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()

