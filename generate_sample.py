from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from datetime import datetime
import math

# Luxury Color Palette
NAVY = HexColor('#0B1F3A')
GOLD = HexColor('#C9A646')
IVORY = HexColor('#F8F6F2')

def draw_circular_text(p, text, x, y, radius, start_angle, font_size, font_name, color, reversed=False):
    """Draws text along a circular path."""
    p.saveState()
    p.setFont(font_name, font_size)
    p.setFillColor(color)
    
    char_angle = 360 / (2 * math.pi * radius) * (font_size * 0.8)
    
    for i, char in enumerate(text):
        if reversed:
            angle = start_angle + (i * char_angle)
            rotation = angle + 90
        else:
            angle = start_angle - (i * char_angle)
            rotation = angle - 90
            
        rad = math.radians(angle)
        char_x = x + radius * math.cos(rad)
        char_y = y + radius * math.sin(rad)
        
        p.saveState()
        p.translate(char_x, char_y)
        p.rotate(rotation)
        p.drawCentredString(0, 0, char)
        p.restoreState()
    p.restoreState()

def generate_ultra_premium_sample():
    filename = "sample_certificate.pdf"
    p = canvas.Canvas(filename, pagesize=landscape(A4))
    width, height = landscape(A4)

    # 1. Premium Background Fill (Ivory)
    p.setFillColor(IVORY)
    p.rect(0, 0, width, height, fill=1)

    # 2. Luxury Double Border (Navy + Gold)
    p.setStrokeColor(NAVY)
    p.setLineWidth(4)
    p.rect(1.2*cm, 1.2*cm, width-2.4*cm, height-2.4*cm)
    
    p.setStrokeColor(GOLD)
    p.setLineWidth(1.5)
    p.rect(1.5*cm, 1.5*cm, width-3*cm, height-3*cm)

    # 3. AI & Level Badges (Top Right - FIXED POS)
    p.saveState()
    badge_y = height - 2.5*cm
    p.setFillColor(NAVY)
    p.setStrokeColor(GOLD)
    p.rect(width - 5.5*cm, badge_y, 3.5*cm, 0.6*cm, fill=1)
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 8)
    p.drawCentredString(width - 3.75*cm, badge_y + 0.15*cm, "AI VERIFIED LEARNING")
    
    p.setFillColor(GOLD)
    p.rect(width - 5.5*cm, badge_y - 0.6*cm, 3.5*cm, 0.6*cm, fill=1)
    p.setFillColor(colors.black)
    p.drawCentredString(width - 3.75*cm, badge_y - 0.45*cm, "SKILL LEVEL: PRO")
    p.restoreState()

    # 4. Branding (Subtle at top)
    p.saveState()
    p.setFont("Helvetica-Bold", 28)
    p.setFillAlpha(0.15)
    p.setFillColor(NAVY)
    p.drawCentredString(width / 2.0, height - 3.5*cm, "Python Edition")
    p.restoreState()

    # 5. Main Heading (Centered)
    p.setFillColor(NAVY)
    p.setFont("Times-Bold", 42)
    p.drawCentredString(width / 2.0, height - 6.0*cm, "CERTIFICATE OF ACHIEVEMENT")

    # 6. Subtitle
    p.setFont("Helvetica", 18)
    p.drawCentredString(width / 2.0, height - 8.0*cm, "This certification is proudly presented to")

    # 7. Student Name Section
    p.setStrokeColor(GOLD)
    p.setLineWidth(0.8)
    p.line(width/2 - 10*cm, height - 9.0*cm, width/2 + 10*cm, height - 9.0*cm)
    
    p.setFont("Times-Bold", 48)
    p.setFillColor(GOLD)
    p.drawCentredString(width / 2.0, height - 10.8*cm, "STUDENT NAME")

    p.line(width/2 - 10*cm, height - 11.5*cm, width/2 + 10*cm, height - 11.5*cm)

    # 8. Achievement Statement
    p.setFillColor(NAVY)
    p.setFont("Helvetica", 18)
    p.drawCentredString(width / 2.0, height - 13.0*cm, "For successfully mastering the high-fidelity curriculum of")
    
    p.setFont("Times-Bold", 26)
    p.drawCentredString(width / 2.0, height - 14.5*cm, "Python Fundamentals")

    # 9. Platform Tagline
    p.setFont("Helvetica-Oblique", 14)
    p.drawCentredString(width / 2.0, height - 16*cm, "Python Edition Adaptive Learning Platform")

    # 10. Luxury Gold Seal (Bottom Right - FIXED CONTRAST)
    seal_x, seal_y = width - 5.5*cm, 5.5*cm
    p.setStrokeColor(GOLD)
    p.setLineWidth(2)
    p.circle(seal_x, seal_y, 2.6*cm, stroke=1, fill=0) # Outer
    p.circle(seal_x, seal_y, 2.4*cm, stroke=1, fill=0) # Text Ring
    
    # Inner Fill (Navy Background for contrast)
    p.setFillColor(NAVY)
    p.circle(seal_x, seal_y, 1.8*cm, stroke=1, fill=1) 
    
    # Circular Text (Improved Spacing)
    draw_circular_text(p, "PYTHON EDITION • CERTIFIED", seal_x, seal_y, 2.12*cm, 160, 9, "Times-Bold", GOLD)
    draw_circular_text(p, "AUTHENTIC", seal_x, seal_y, 2.12*cm, -120, 9, "Times-Bold", GOLD, reversed=True)
    
    # Flipped for visibility (Gold on Navy)
    p.setFillColor(WHITE)
    p.setFont("Times-Bold", 12)
    p.drawCentredString(seal_x, seal_y - 0.2*cm, "VERIFIED")

    # 11. QR Verification Code (Bottom Center - REAL TEST)
    real_uuid = "6791d293-87a8-45e7-9132-ed42e322fc30"
    qr_code = qr.QrCodeWidget(f'https://pythonedition.vercel.app/verify/{real_uuid}')
    bounds = qr_code.getBounds()
    qr_width, qr_height = bounds[2] - bounds[0], bounds[3] - bounds[1]
    
    d = Drawing(45, 45, transform=[45./qr_width, 0, 0, 45./qr_height, 0, 0])
    d.add(qr_code)
    
    qr_x, qr_y = width/2 - 22, 3.2*cm
    renderPDF.draw(d, p, qr_x, qr_y)
    p.setFillColor(NAVY)
    p.setFont("Helvetica", 8)
    p.drawCentredString(width/2, qr_y - 0.4*cm, "Scan to Verify Certificate")
    p.drawCentredString(width/2, qr_y - 0.9*cm, f"ID: PY-CERT-{real_uuid[:8].upper()}")

    # 12. Signature Section (Bottom Left)
    p.setStrokeColor(NAVY)
    p.setLineWidth(1.2)
    p.line(3*cm, 5.5*cm, 10*cm, 5.5*cm)
    p.setFont("Courier-BoldOblique", 14)
    p.drawString(3.5*cm, 5.8*cm, "Pythonized AI")
    p.setFont("Helvetica", 10)
    p.drawString(3*cm, 4.9*cm, "PLATFORM DIRECTOR, PYTHON EDITION")

    # 13. Date (Bottom Left below sig)
    p.setFont("Helvetica", 9)
    p.drawString(3*cm, 4.0*cm, f"Issued on: {datetime.now().strftime('%B %d, %Y')}")

    p.showPage()
    p.save()
    print(f"💎 Success: Fixed Ultra-Premium certificate generated as {filename}")

if __name__ == "__main__":
    from reportlab.graphics import renderPDF
    generate_ultra_premium_sample()
