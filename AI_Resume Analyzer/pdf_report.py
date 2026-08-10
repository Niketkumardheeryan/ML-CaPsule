from io import BytesIO
from datetime import datetime
import re
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def _format_inline_markdown(text):
    """Convert common Gemini Markdown into safe ReportLab markup."""
    text = escape(str(text))

    # Inline code
    text = re.sub(
        r"`([^`]+)`",
        r"<font name='Courier'>\1</font>",
        text,
    )

    # Markdown links
    text = re.sub(
        r"\[([^\]]+)\]\((https?://[^)]+)\)",
        r"<link href='\2' color='blue'>\1</link>",
        text,
    )

    # Bold + italic
    text = re.sub(
        r"\*\*\*(.+?)\*\*\*",
        r"<b><i>\1</i></b>",
        text,
    )

    text = re.sub(
        r"\*\*(.+?)\*\*",
        r"<b>\1</b>",
        text,
    )

    text = re.sub(
        r"__(.+?)__",
        r"<b>\1</b>",
        text,
    )

    # Italic - avoid treating already converted HTML as Markdown
    text = re.sub(
        r"(?<!\*)\*([^*]+?)\*(?!\*)",
        r"<i>\1</i>",
        text,
    )

    text = re.sub(
        r"(?<!_)_([^_]+?)_(?!_)",
        r"<i>\1</i>",
        text,
    )

    return text


def _add_ai_feedback(story, feedback, styles):
    """
    Convert Gemini Markdown-style output into clean ReportLab elements.

    Supports:
    - # / ## / ### / #### headings
    - numbered lists
    - bullets
    - nested bullets
    - bold / italic text
    - inline code
    - Markdown links
    - horizontal rules
    - normal paragraphs
    """

    if not feedback:
        story.append(
            Paragraph(
                "No AI feedback was generated.",
                styles["BodyCustom"],
            )
        )
        return

    lines = (
        str(feedback)
        .replace("\r\n", "\n")
        .replace("\r", "\n")
        .split("\n")
    )

    paragraph_buffer = []

    def flush_paragraph():
        if not paragraph_buffer:
            return

        text = " ".join(
            line.strip()
            for line in paragraph_buffer
        ).strip()

        paragraph_buffer.clear()

        if text:
            story.append(
                Paragraph(
                    _format_inline_markdown(text),
                    styles["BodyCustom"],
                )
            )

    for raw_line in lines:
        line = raw_line.strip()

        # Blank line
        if not line:
            flush_paragraph()
            continue

        # Markdown horizontal rules
        if re.fullmatch(r"(-{3,}|\*{3,}|_{3,})", line):
            flush_paragraph()
            story.append(Spacer(1, 6))
            continue

        # Markdown headings
        heading_match = re.match(
            r"^(#{1,6})\s+(.+)$",
            line,
        )

        if heading_match:
            flush_paragraph()

            level = len(heading_match.group(1))
            heading_text = _format_inline_markdown(
                heading_match.group(2)
            )

            if level == 1:
                style = styles["AIHeading1"]
            elif level == 2:
                style = styles["AIHeading2"]
            else:
                style = styles["AIHeading3"]

            story.append(
                Paragraph(
                    heading_text,
                    style,
                )
            )
            continue

        # Numbered list
        number_match = re.match(
            r"^(\d+)[.)]\s+(.+)$",
            line,
        )

        if number_match:
            flush_paragraph()

            number = number_match.group(1)
            item = _format_inline_markdown(
                number_match.group(2)
            )

            story.append(
                Paragraph(
                    f"<b>{number}.</b> {item}",
                    styles["NumberedItem"],
                )
            )
            continue

        # Nested bullet.
        # This is checked before normal bullets because Gemini
        # may indent nested Markdown bullets.
        nested_match = re.match(
            r"^\s{2,}[-*+•]\s+(.+)$",
            raw_line,
        )

        if nested_match:
            flush_paragraph()

            item = _format_inline_markdown(
                nested_match.group(1)
            )

            story.append(
                Paragraph(
                    f"- {item}",
                    styles["NestedBullet"],
                )
            )
            continue

        # Normal bullet
        bullet_match = re.match(
            r"^[-*+•]\s+(.+)$",
            line,
        )

        if bullet_match:
            flush_paragraph()

            item = _format_inline_markdown(
                bullet_match.group(1)
            )

            story.append(
                Paragraph(
                    f"- {item}",
                    styles["BulletItem"],
                )
            )
            continue

        # Normal paragraph line
        paragraph_buffer.append(line)

    flush_paragraph()


def _add_page_number(canvas, document):
    """Add footer and page number to every PDF page."""
    canvas.saveState()

    width, _ = A4

    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)

    canvas.drawString(
        42,
        22,
        "AI Resume Analyzer",
    )

    canvas.drawRightString(
        width - 42,
        22,
        f"Page {document.page}",
    )

    canvas.restoreState()


def _safe_score(score):
    """Safely convert the ATS score into a number."""
    try:
        return float(score)
    except (TypeError, ValueError):
        return 0.0


def generate_pdf_report(
    selected_role,
    score,
    found_skills,
    missing_skills,
    entities,
    ai_feedback,
):
    """Generate a clean, structured PDF resume analysis report."""

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=42,
        leftMargin=42,
        topMargin=42,
        bottomMargin=42,
        title="AI Resume Analysis Report",
        author="AI Resume Analyzer",
    )

    base_styles = getSampleStyleSheet()

    styles = {
        # -----------------------------------------------------
        # Main report styles
        # -----------------------------------------------------

        "Title": ParagraphStyle(
            "ReportTitle",
            parent=base_styles["Title"],
            alignment=TA_CENTER,
            fontSize=22,
            leading=27,
            spaceAfter=8,
        ),

        "Subtitle": ParagraphStyle(
            "ReportSubtitle",
            parent=base_styles["BodyText"],
            alignment=TA_CENTER,
            fontSize=9,
            textColor=colors.grey,
            spaceAfter=18,
        ),

        "Section": ParagraphStyle(
            "SectionHeading",
            parent=base_styles["Heading2"],
            fontSize=15,
            leading=19,
            spaceBefore=14,
            spaceAfter=8,
            keepWithNext=True,
        ),

        "BodyCustom": ParagraphStyle(
            "BodyCustom",
            parent=base_styles["BodyText"],
            fontSize=9.5,
            leading=14,
            spaceAfter=6,
        ),

        "Small": ParagraphStyle(
            "Small",
            parent=base_styles["BodyText"],
            fontSize=8.5,
            leading=12,
        ),

        # -----------------------------------------------------
        # AI feedback styles
        # -----------------------------------------------------

        "AIHeading1": ParagraphStyle(
            "AIHeading1",
            parent=base_styles["Heading2"],
            fontSize=14,
            leading=18,
            spaceBefore=12,
            spaceAfter=7,
            keepWithNext=True,
        ),

        "AIHeading2": ParagraphStyle(
            "AIHeading2",
            parent=base_styles["Heading3"],
            fontSize=12,
            leading=16,
            spaceBefore=10,
            spaceAfter=6,
            keepWithNext=True,
        ),

        "AIHeading3": ParagraphStyle(
            "AIHeading3",
            parent=base_styles["Heading4"],
            fontSize=10.5,
            leading=14,
            spaceBefore=7,
            spaceAfter=4,
            keepWithNext=True,
        ),

        "BulletItem": ParagraphStyle(
            "BulletItem",
            parent=base_styles["BodyText"],
            fontSize=9.5,
            leading=14,
            leftIndent=16,
            firstLineIndent=-9,
            spaceAfter=4,
        ),

        "NestedBullet": ParagraphStyle(
            "NestedBullet",
            parent=base_styles["BodyText"],
            fontSize=9.2,
            leading=13,
            leftIndent=30,
            firstLineIndent=-9,
            spaceAfter=3,
        ),

        "NumberedItem": ParagraphStyle(
            "NumberedItem",
            parent=base_styles["BodyText"],
            fontSize=9.5,
            leading=14,
            leftIndent=18,
            firstLineIndent=-18,
            spaceAfter=5,
        ),
    }

    story = []

    # =========================================================
    # 1. REPORT HEADER
    # =========================================================

    story.append(
        Paragraph(
            "AI Resume Analysis Report",
            styles["Title"],
        )
    )

    story.append(
        Paragraph(
            f"Generated on "
            f"{datetime.now().strftime('%d %B %Y, %I:%M %p')}",
            styles["Subtitle"],
        )
    )

    # =========================================================
    # 2. ANALYSIS SUMMARY
    # =========================================================

    story.append(
        Paragraph(
            "Analysis Summary",
            styles["Section"],
        )
    )

    score_number = _safe_score(score)

    summary_data = [
        [
            Paragraph(
                "<b>Target Job Role</b>",
                styles["Small"],
            ),
            Paragraph(
                escape(str(selected_role)),
                styles["Small"],
            ),
        ],
        [
            Paragraph(
                "<b>ATS Score</b>",
                styles["Small"],
            ),
            Paragraph(
                f"<b>{escape(str(score))}%</b>",
                styles["Small"],
            ),
        ],
        [
            Paragraph(
                "<b>Skills Detected</b>",
                styles["Small"],
            ),
            Paragraph(
                str(len(found_skills)),
                styles["Small"],
            ),
        ],
        [
            Paragraph(
                "<b>Missing Skills</b>",
                styles["Small"],
            ),
            Paragraph(
                str(len(missing_skills)),
                styles["Small"],
            ),
        ],
    ]

    summary_table = Table(
        summary_data,
        colWidths=[
            2.15 * inch,
            3.55 * inch,
        ],
        hAlign="LEFT",
    )

    summary_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#F0F0F0"),
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#B8B8B8"),
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    story.append(summary_table)
    story.append(Spacer(1, 12))

    # =========================================================
    # 3. SKILLS DETECTED
    # =========================================================

    story.append(
        Paragraph(
            "Skills Detected",
            styles["Section"],
        )
    )

    if found_skills:
        skill_rows = []

        for skill in found_skills:
            skill_rows.append(
                [
                    Paragraph(
                        "+",
                        styles["Small"],
                    ),
                    Paragraph(
                        escape(str(skill)),
                        styles["Small"],
                    ),
                ]
            )

        skills_table = Table(
            skill_rows,
            colWidths=[
                0.35 * inch,
                5.35 * inch,
            ],
            hAlign="LEFT",
        )

        skills_table.setStyle(
            TableStyle(
                [
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.35,
                        colors.HexColor("#D0D0D0"),
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE",
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                ]
            )
        )

        story.append(skills_table)

    else:
        story.append(
            Paragraph(
                "No matching skills were detected.",
                styles["BodyCustom"],
            )
        )

    # =========================================================
    # 4. MISSING SKILLS
    # =========================================================

    story.append(
        Paragraph(
            "Missing Skills",
            styles["Section"],
        )
    )

    if missing_skills:
        missing_rows = []

        for skill in missing_skills:
            missing_rows.append(
                [
                    Paragraph(
                        "-",
                        styles["Small"],
                    ),
                    Paragraph(
                        escape(str(skill)),
                        styles["Small"],
                    ),
                ]
            )

        missing_table = Table(
            missing_rows,
            colWidths=[
                0.35 * inch,
                5.35 * inch,
            ],
            hAlign="LEFT",
        )

        missing_table.setStyle(
            TableStyle(
                [
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.35,
                        colors.HexColor("#D0D0D0"),
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE",
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                ]
            )
        )

        story.append(missing_table)

    else:
        story.append(
            Paragraph(
                "No missing skills were identified.",
                styles["BodyCustom"],
            )
        )

    # =========================================================
    # 5. EXTRACTED ENTITIES
    # =========================================================

    story.append(
        Paragraph(
            "Extracted Entities",
            styles["Section"],
        )
    )

    if entities:
        entity_data = [
            [
                Paragraph(
                    "<b>Entity</b>",
                    styles["Small"],
                ),
                Paragraph(
                    "<b>Type</b>",
                    styles["Small"],
                ),
            ]
        ]

        for entity, label in entities:
            entity_data.append(
                [
                    Paragraph(
                        escape(str(entity)),
                        styles["Small"],
                    ),
                    Paragraph(
                        escape(str(label)),
                        styles["Small"],
                    ),
                ]
            )

        entity_table = Table(
            entity_data,
            colWidths=[
                3.55 * inch,
                2.15 * inch,
            ],
            repeatRows=1,
            hAlign="LEFT",
        )

        entity_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#E8E8E8"),
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.4,
                        colors.HexColor("#B8B8B8"),
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP",
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                ]
            )
        )

        story.append(entity_table)

    else:
        story.append(
            Paragraph(
                "No entities were detected.",
                styles["BodyCustom"],
            )
        )

    # =========================================================
    # 6. AI RESUME FEEDBACK
    # =========================================================

    story.append(
        Paragraph(
            "AI Resume Feedback",
            styles["Section"],
        )
    )

    _add_ai_feedback(
        story,
        ai_feedback,
        styles,
    )

    # =========================================================
    # 7. ATS SCORE RECOMMENDATION
    # =========================================================

    story.append(
        Paragraph(
            "ATS Score Recommendation",
            styles["Section"],
        )
    )

    if score_number < 50:
        recommendation = (
            "Your resume needs significant improvement. Focus on adding "
            "relevant technical skills, projects, and keywords related "
            "to the selected job role."
        )

    elif score_number < 80:
        recommendation = (
            "Your resume has a reasonable match with the selected job "
            "role. Adding missing skills and improving keyword relevance "
            "could increase the ATS score."
        )

    else:
        recommendation = (
            "Your resume has a strong match with the selected job role "
            "and appears to be well optimized for ATS compatibility."
        )

    recommendation_box = Table(
        [
            [
                Paragraph(
                    _format_inline_markdown(
                        recommendation
                    ),
                    styles["BodyCustom"],
                )
            ]
        ],
        colWidths=[5.7 * inch],
    )

    recommendation_box.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor("#F5F5F5"),
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.6,
                    colors.HexColor("#B8B8B8"),
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
            ]
        )
    )

    story.append(recommendation_box)

    # =========================================================
    # 8. FOOTER
    # =========================================================

    story.append(Spacer(1, 18))

    story.append(
        Paragraph(
            "Generated by AI Resume Analyzer",
            ParagraphStyle(
                "FooterText",
                parent=styles["Small"],
                alignment=TA_CENTER,
                textColor=colors.grey,
            ),
        )
    )

    # Build the PDF
    document.build(
        story,
        onFirstPage=_add_page_number,
        onLaterPages=_add_page_number,
    )

    buffer.seek(0)

    return buffer
