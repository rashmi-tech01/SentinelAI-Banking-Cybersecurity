from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os

def generate_report(amount, risk_score, result, status, reasons):

    if not os.path.exists("reports"):
        os.makedirs("reports")

    filename = "reports/Fraud_Report.pdf"

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>SentinelAI Fraud Analysis Report</b>", styles["Title"]))
    story.append(Paragraph(f"<b>Transaction Amount:</b> ₹{amount}", styles["Normal"]))
    story.append(Paragraph(f"<b>Risk Score:</b> {risk_score}%", styles["Normal"]))
    story.append(Paragraph(f"<b>AI Decision:</b> {result}", styles["Normal"]))
    story.append(Paragraph(f"<b>Threat Level:</b> {status}", styles["Normal"]))

    story.append(Paragraph("<br/><b>Reasons:</b>", styles["Heading2"]))

    for reason in reasons:
        story.append(Paragraph(f"• {reason}", styles["Normal"]))

    doc.build(story)

    return filename