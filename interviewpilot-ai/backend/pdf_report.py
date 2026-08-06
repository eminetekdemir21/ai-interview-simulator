"""Mulakat sonuc raporunu indirilebilir bir PDF'e cevirir.
Turkce karakterler (ı, ş, ğ, ç, ö, ü) icin projeyle birlikte gelen
DejaVu Sans fontunu kullanir, boylece kullanicinin bilgisayarinda
ayri bir font kurulu olmasi gerekmez.
"""
import os
from datetime import datetime
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)

FONTS_DIR = os.path.join(os.path.dirname(__file__), "fonts")
_fonts_registered = False


def _ensure_fonts():
    global _fonts_registered
    if _fonts_registered:
        return
    pdfmetrics.registerFont(TTFont("DejaVuSans", os.path.join(FONTS_DIR, "DejaVuSans.ttf")))
    pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", os.path.join(FONTS_DIR, "DejaVuSans-Bold.ttf")))
    _fonts_registered = True


def _styles():
    _ensure_fonts()
    base = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle("title", parent=base["Title"], fontName="DejaVuSans-Bold", fontSize=20, textColor=colors.HexColor("#6b57a8"), spaceAfter=4),
        "meta": ParagraphStyle("meta", parent=base["Normal"], fontName="DejaVuSans", fontSize=9, textColor=colors.HexColor("#9a8fae"), spaceAfter=14),
        "h2": ParagraphStyle("h2", parent=base["Heading2"], fontName="DejaVuSans-Bold", fontSize=13, textColor=colors.HexColor("#6b57a8"), spaceBefore=14, spaceAfter=6),
        "body": ParagraphStyle("body", parent=base["Normal"], fontName="DejaVuSans", fontSize=10.5, leading=15, textColor=colors.HexColor("#4a3f5a")),
        "bullet": ParagraphStyle("bullet", parent=base["Normal"], fontName="DejaVuSans", fontSize=10.5, leading=15, leftIndent=14, spaceAfter=3, textColor=colors.HexColor("#4a3f5a")),
        "score": ParagraphStyle("score", parent=base["Normal"], fontName="DejaVuSans-Bold", fontSize=28, textColor=colors.HexColor("#6b57a8"), alignment=1),
        "qa_q": ParagraphStyle("qa_q", parent=base["Normal"], fontName="DejaVuSans-Bold", fontSize=10.5, leading=14, textColor=colors.HexColor("#2f4a5c")),
        "qa_a": ParagraphStyle("qa_a", parent=base["Normal"], fontName="DejaVuSans", fontSize=10, leading=14, textColor=colors.HexColor("#4a3f5a"), leftIndent=8),
        "qa_meta": ParagraphStyle("qa_meta", parent=base["Normal"], fontName="DejaVuSans", fontSize=9, leading=13, textColor=colors.HexColor("#6b8f7a"), leftIndent=8),
    }
    return styles


def build_pdf_bytes(record: dict) -> bytes:
    """record: history_store'daki tam kayit (overall_score, strengths,
    weaknesses, summary, history, created_at, job_preview icerir)."""
    styles = _styles()
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm, bottomMargin=18 * mm,
        title="Mulakat Sonuc Raporu",
    )

    story = []
    story.append(Paragraph("AI Interview Simulator", styles["title"]))
    created_raw = record.get("created_at", "")
    try:
        created = datetime.fromisoformat(created_raw).strftime("%d.%m.%Y %H:%M")
    except (ValueError, TypeError):
        created = created_raw or "-"
    job_preview = (record.get("job_preview") or "").replace("\n", " ").strip()[:180]
    story.append(Paragraph(f"Rapor tarihi: {created}  ·  Is ilani: {job_preview or '-'}", styles["meta"]))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e8def7"), spaceAfter=12))

    story.append(Paragraph("Genel Skor", styles["h2"]))
    story.append(Paragraph(f"{record.get('overall_score', '-')}/100", styles["score"]))
    story.append(Spacer(1, 10))

    sub = record.get("sub_scores") or {}
    if sub:
        labels = {"technical": "Teknik Bilgi", "communication": "Iletisim", "confidence": "Ozguven", "system_design": "Sistem Tasarimi"}
        sub_line = "  ·  ".join(f"{labels.get(k, k)}: {v}/100" for k, v in sub.items())
        story.append(Paragraph(sub_line, styles["meta"]))

    story.append(Paragraph("Guclu Yonler", styles["h2"]))
    for s in record.get("strengths", []) or []:
        story.append(Paragraph(f"✓ {s}", styles["bullet"]))

    story.append(Paragraph("Gelistirilmesi Gereken Yonler", styles["h2"]))
    for w in record.get("weaknesses", []) or []:
        story.append(Paragraph(f"✦ {w}", styles["bullet"]))

    story.append(Paragraph("Genel Degerlendirme", styles["h2"]))
    story.append(Paragraph(record.get("summary", "") or "-", styles["body"]))

    qa_history = record.get("history", []) or []
    if qa_history:
        story.append(Paragraph("Soru - Cevap Detaylari", styles["h2"]))
        for i, qa in enumerate(qa_history, 1):
            story.append(Paragraph(f"{i}. {qa.get('question', '')}", styles["qa_q"]))
            if qa.get("answer"):
                story.append(Paragraph(f"Cevap: {qa['answer']}", styles["qa_a"]))
            if qa.get("score") is not None:
                fb = qa.get("feedback") or ""
                story.append(Paragraph(f"Puan: {qa['score']}/100 — {fb}", styles["qa_meta"]))
            story.append(Spacer(1, 8))

    doc.build(story)
    return buf.getvalue()
