from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

def generate_pdf(result, job_id: str):
    file_path = f"reports/{job_id}.pdf"

    os.makedirs("reports", exist_ok=True)

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph(f"<b>{result['company']}</b>", styles['Title']))
    content.append(Spacer(1, 12))

    content.append(Paragraph(f"<b>Signal:</b> {result['signal']}", styles['Normal']))
    content.append(Paragraph(f"<b>Confidence:</b> {result['confidence']}", styles['Normal']))
    content.append(Paragraph(f"<b>Trend:</b> {result.get('trend', 'N/A')}", styles['Normal']))

    content.append(Spacer(1, 12))
    content.append(Paragraph("<b>Thesis</b>", styles['Heading2']))
    content.append(Paragraph(result["thesis"], styles['Normal']))

    content.append(Spacer(1, 12))
    content.append(Paragraph("<b>Insights</b>", styles['Heading2']))
    for i in result["insights"]:
        content.append(Paragraph(f"- {i}", styles['Normal']))

    content.append(Spacer(1, 12))
    content.append(Paragraph("<b>Risks</b>", styles['Heading2']))
    for r in result["risks"]:
        content.append(Paragraph(f"- {r}", styles['Normal']))

    doc.build(content)

    return file_path