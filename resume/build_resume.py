"""Build the one-page, ATS-readable PDF résumé from verified portfolio content."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "Manisha_Pandala_Resume.pdf"


def _font(name: str, path: str, fallback: str) -> str:
    candidate = Path(path)
    if candidate.exists():
        pdfmetrics.registerFont(TTFont(name, str(candidate)))
        return name
    return fallback


BODY_FONT = _font("ResumeSans", "/System/Library/Fonts/Supplemental/Arial.ttf", "Helvetica")
BOLD_FONT = _font("ResumeSansBold", "/System/Library/Fonts/Supplemental/Arial Bold.ttf", "Helvetica-Bold")


def bullet(text: str, style: ParagraphStyle) -> Table:
    table = Table(
        [[Paragraph("•", style), Paragraph(text, style)]],
        colWidths=[0.14 * inch, 6.86 * inch],
    )
    table.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.1)]))
    return table


def build() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=letter,
        rightMargin=0.56 * inch,
        leftMargin=0.56 * inch,
        topMargin=0.42 * inch,
        bottomMargin=0.42 * inch,
        title="Manisha Pandala - Data Science Resume",
        author="Manisha Pandala",
        subject="Data Science and AI/ML Resume",
    )
    styles = getSampleStyleSheet()
    name = ParagraphStyle("Name", parent=styles["Title"], fontName=BOLD_FONT, fontSize=21, leading=23, alignment=TA_CENTER, textColor=colors.HexColor("#102448"), spaceAfter=3)
    contact = ParagraphStyle("Contact", parent=styles["Normal"], fontName=BODY_FONT, fontSize=8.1, leading=10.5, alignment=TA_CENTER, textColor=colors.HexColor("#26364f"), spaceAfter=4)
    section = ParagraphStyle("Section", parent=styles["Heading2"], fontName=BOLD_FONT, fontSize=10, leading=12, textColor=colors.HexColor("#0b6f77"), spaceBefore=6.2, spaceAfter=2.8, borderWidth=0, borderPadding=0)
    body = ParagraphStyle("Body", parent=styles["Normal"], fontName=BODY_FONT, fontSize=8.25, leading=10.35, alignment=TA_LEFT, textColor=colors.HexColor("#151d2b"), spaceAfter=1.3)
    role = ParagraphStyle("Role", parent=body, fontName=BOLD_FONT, fontSize=8.4, leading=10.5, spaceBefore=2.2, spaceAfter=0.8)

    story = [
        Paragraph("MANISHA PANDALA", name),
        Paragraph(
            "Phoenix, AZ | +1 (480) 330-1180 | manishapandala4@gmail.com | "
            '<a href="https://www.linkedin.com/in/manishapandala">linkedin.com/in/manishapandala</a> | '
            '<a href="https://github.com/manishapandala">github.com/manishapandala</a> | '
            '<a href="https://manishapandala.github.io/portfolio/">Portfolio</a>',
            contact,
        ),
        Paragraph("SUMMARY", section),
        Paragraph(
            "M.S. Data Science student at Arizona State University with a B.Tech. in Artificial Intelligence and Machine Learning. Builds reproducible ML and analytics systems across model reliability, forecasting, retrieval, computer vision, data quality, reporting automation, and explainable cybersecurity. Seeking data science and AI/ML internships and early-career roles.",
            body,
        ),
        Paragraph("EDUCATION", section),
        Paragraph("Arizona State University - M.S. Data Science, Analytics and Engineering | GPA: 3.5/4.0 | Expected May 2027 | Tempe, AZ", role),
        Paragraph("Anurag University - B.Tech. Artificial Intelligence and Machine Learning | CGPA: 3.75/4.0 | May 2025 | Hyderabad, India", role),
        Paragraph("EXPERIENCE", section),
        Paragraph("Research Assistant, Data Visualization - Arizona State University | 2025-Present", role),
        bullet("Build research-facing analytics and visual summaries with D3.js, Tableau, and Power BI; translate open-ended faculty questions into structured analysis and actionable next steps.", body),
        bullet("Communicate findings, assumptions, and technical tradeoffs to research stakeholders.", body),
        Paragraph("Data Intern - Open Pixel | May 2024-June 2025", role),
        bullet("Prepared, validated, and analyzed operational data with Python and SQL for recurring reporting.", body),
        bullet("Built repeatable reporting workflows and dashboards with explicit metric definitions and validation checks; collaborated with stakeholders to improve output consistency and usability.", body),
        Paragraph("SELECTED PROJECTS", section),
        Paragraph("Model Reliability Lab | Python, scikit-learn, calibration, drift monitoring", role),
        bullet("Compared calibrated logistic regression with random forest using isolated train, validation, and test partitions; added cost-aware thresholding, cohort checks, permutation importance, and simulated drift.", body),
        bullet("Achieved 0.984 average precision and 0.0445 Brier score on a 114-row held-out partition with eight automated tests.", body),
        Paragraph("Demand Forecasting Backtest | Python, pandas, gradient boosting, time series", role),
        bullet("Built past-only lag/rolling features, chronological splits, three expanding-window folds, a seasonal baseline, and validation-calibrated prediction intervals.", body),
        bullet("Reached 4.25% WAPE versus 8.62% for the generated-data baseline, a 50.7% relative improvement, with eight automated tests.", body),
        Paragraph("CyberGuard Zero Trust Classifier | Python, Flask, explainable rules", role),
        bullet("Developed deterministic event classification, 0-100 risk scoring, traceable reasons, and mappings to selected Zero Trust and NIST control families.", body),
        bullet("Verified parsing, rules, bounded APIs, CLI behavior, and scoring with 45 tests and a deterministic 5,000-event scale check.", body),
        Paragraph("TECHNICAL SKILLS", section),
        Paragraph("<b>Programming and analysis:</b> Python, SQL, R, pandas, NumPy, statistical analysis, feature engineering", body),
        Paragraph("<b>Machine learning:</b> scikit-learn, PyTorch, TensorFlow, classification, anomaly detection, forecasting, calibration, embeddings, NLP, computer vision", body),
        Paragraph("<b>Systems and visualization:</b> Flask, REST APIs, Git/GitHub, Docker, Power BI, Tableau, D3.js, Excel, Jupyter", body),
        Spacer(1, 1),
    ]
    doc.build(story)


if __name__ == "__main__":
    build()
