
import os
import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF

def generate_sample_pdf(output_path):
    # Mock data
    user_name = "STUDENT NAME"
    module_title = "Python Fundamentals"
    issued_at = datetime.datetime.now()
    cert_id = "PY-CERT-001-DEMO-2026"
    user_level = "PRO"

    p = canvas.Canvas(output_path, pagesize=landscape(letter))
    width, height = landscape(letter)

    # Colors
    dark_blue = colors.Color(red=(26/255), green=(43/255), blue=(75/255))
    gold = colors.Color(red=(197/255), green=(160/255), blue=(89/255))
    bg_light = colors.Color(red=(248/255), green=(249/255), blue=(250/255))

    # 1. Background and Borders
    p.setFillColor(bg_light)
    p.rect(0, 0, width, height, fill=1, stroke=0)
    
    # Thick outer border
    p.setStrokeColor(bg_light)
    p.setLineWidth(32)
    p.rect(16, 16, width-32, height-32, fill=0, stroke=1)

    # Inner dark blue border
    p.setStrokeColor(dark_blue)
    p.setLineWidth(2)
    p.rect(40, 40, width-80, height-80, fill=0, stroke=1)

    # Inner gold thin border
    p.setStrokeColor(gold)
    p.setLineWidth(1)
    p.rect(48, 48, width-96, height-96, fill=0, stroke=1)

    # 2. Header
    p.setFillColor(dark_blue)
    p.setFont("Times-Bold", 20)
    p.drawCentredString(width / 2.0, height - 1.2 * inch, "Python Edition")

    # 3. AI Verified Badge (Top Right)
    badge_x = width - 2.2 * inch
    badge_y = height - 1.3 * inch
    p.setFillColor(gold)
    p.rect(badge_x, badge_y, 1.5 * inch, 0.4 * inch, fill=1, stroke=0)
    p.setFillColor(dark_blue)
    p.rect(badge_x + 2, badge_y + 12, 1.5 * inch - 4, 0.2 * inch, fill=1, stroke=1)
    
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 8)
    p.drawCentredString(badge_x + 0.75 * inch, badge_y + 16, "AI VERIFIED LEARNING")
    
    p.setFillColor(dark_blue)
    p.setFont("Helvetica-Bold", 7)
    p.drawCentredString(badge_x + 0.75 * inch, badge_y + 4, f"SKILL LEVEL: {user_level}")

    # 4. Main Heading
    p.setFillColor(dark_blue)
    p.setFont("Times-Bold", 36)
    p.drawCentredString(width / 2.0, height - 2.2 * inch, "CERTIFICATE OF ACHIEVEMENT")

    # 5. Subtext
    p.setFillColor(colors.Color(0.3, 0.3, 0.3))
    p.setFont("Times-Italic", 14)
    p.drawCentredString(width / 2.0, height - 2.8 * inch, "This certification is proudly presented to")

    # 6. Student Name
    p.setFillColor(gold)
    p.setFont("Times-Bold", 42)
    p.drawCentredString(width / 2.0, height - 3.6 * inch, user_name.upper())
    
    # Name underline
    p.setStrokeColor(gold)
    p.setLineWidth(2)
    p.line(width/2.0 - 2.5 * inch, height - 3.8 * inch, width/2.0 + 2.5 * inch, height - 3.8 * inch)

    # 7. Achievement Text
    p.setFillColor(colors.Color(0.3, 0.3, 0.3))
    p.setFont("Times-Roman", 14)
    p.drawCentredString(width / 2.0, height - 4.4 * inch, "For successfully mastering the high-fidelity curriculum of")

    # 8. Module Title
    p.setFillColor(dark_blue)
    p.setFont("Times-Bold", 26)
    p.drawCentredString(width / 2.0, height - 5.0 * inch, module_title)

    # 9. Bottom Section
    
    # Left: Signature
    p.setFillColor(dark_blue)
    p.setFont("Times-Italic", 18)
    p.drawString(1.2 * inch, 1.8 * inch, "Pythonized AI")
    p.setLineWidth(1)
    p.line(1.1 * inch, 1.7 * inch, 2.8 * inch, 1.7 * inch)
    p.setFont("Helvetica-Bold", 8)
    p.drawString(1.1 * inch, 1.55 * inch, "PLATFORM DIRECTOR, PYTHON EDITION")
    p.setFont("Helvetica", 8)
    p.drawString(1.1 * inch, 1.3 * inch, f"Issued on: {issued_at.strftime('%B %d, %Y')}")

    # Center: QR Code
    qr_code = qr.QrCodeWidget(f"https://python-edition.vercel.app/verify/{cert_id}")
    bounds = qr_code.getBounds()
    qr_width = bounds[2] - bounds[0]
    qr_height = bounds[3] - bounds[1]
    d = Drawing(60, 60, transform=[60./qr_width, 0, 0, 60./qr_height, 0, 0])
    d.add(qr_code)
    renderPDF.draw(d, p, width/2.0 - 30, 1.4 * inch)
    
    p.setFillColor(colors.gray)
    p.setFont("Helvetica", 6)
    p.drawCentredString(width/2.0, 1.25 * inch, "Scan to Verify Certificate")
    p.setFont("Courier", 7)
    p.drawCentredString(width/2.0, 1.1 * inch, f"ID: {cert_id}")

    # Right: Seal
    seal_x = width - 2.4 * inch
    seal_y = 1.3 * inch
    center_x = seal_x + 0.6 * inch
    center_y = seal_y + 0.6 * inch
    
    # Outer gold double circle
    p.setStrokeColor(gold)
    p.setLineWidth(2.5)
    p.circle(center_x, center_y, 0.65 * inch, fill=0)
    p.setLineWidth(1)
    p.circle(center_x, center_y, 0.6 * inch, fill=0)
    
    # Inner dark blue circle
    dark_blue_seal = colors.Color(red=(10/255), green=(25/255), blue=(47/255))
    p.setFillColor(dark_blue_seal)
    p.circle(center_x, center_y, 0.45 * inch, fill=1, stroke=0)
    
    # "VERIFIED" text in center
    p.setFillColor(gold)
    p.setFont("Helvetica-Bold", 10)
    p.drawCentredString(center_x, center_y - 3, "VERIFIED")

    # Circular Text: "PYTHON EDITION • CERTIFIED • AUTHENTIC • "
    p.setFont("Helvetica-Bold", 6)
    text_to_draw = "PYTHON EDITION • CERTIFIED • AUTHENTIC • "
    radius = 0.52 * inch
    # We draw each character individually around the circle
    for i, char in enumerate(text_to_draw):
        angle = 90 - (i * (360 / len(text_to_draw)))
        p.saveState()
        p.translate(center_x, center_y)
        p.rotate(angle)
        p.drawCentredString(0, radius, char)
        p.restoreState()

    # Bottom Subtitle
    p.setFillColor(colors.Color(0.4, 0.4, 0.4))
    p.setFont("Times-Italic", 10)
    p.drawCentredString(width / 2.0, 0.8 * inch, "Python Edition Adaptive Learning Platform")

    p.showPage()
    p.save()
    print(f"Sample certificate generated at: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    generate_sample_pdf("sample_certificate.pdf")
