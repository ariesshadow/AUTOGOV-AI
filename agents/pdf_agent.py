"""
pdf_agent.py - AutoGov AI | PDF Generation Engine
Generates clean, pre-filled official application forms with crisp tables,
date formatting, CNIC hyphenation, and professional styling.
"""

import os
import io
import time
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def format_date_clean(date_str):
    """Converts YYYYMMDD or YYYY-MM-DD strings to '23 March 2006' format."""
    if not date_str or date_str == "Not Specified":
        return "Not Specified"
    
    clean_str = date_str.replace("-", "").replace("/", "").strip()
    try:
        if len(clean_str) == 8 and clean_str.isdigit():
            dt = datetime.strptime(clean_str, "%Y%m%d")
            return dt.strftime("%d %B %Y")
    except Exception:
        pass
    return date_str

def format_cnic_clean(cnic_str):
    """Formats 13-digit raw CNIC into XXXXX-XXXXXXX-X format."""
    if not cnic_str or cnic_str == "Not Specified":
        return "Not Specified"
    
    digits = "".join(filter(str.isdigit, cnic_str))
    if len(digits) == 13:
        return f"{digits[:5]}-{digits[5:12]}-{digits[12]}"
    return cnic_str

def make_filename(payload):
    dept = payload.get("service_request", {}).get("department", "GOV").lower()
    cnic = payload.get("user_profile", {}).get("cnic_number", "0000")
    cnic_clean = "".join(filter(str.isdigit, cnic))[-4:] or "0000"
    return f"autogov_{dept}_application_{cnic_clean}.pdf"

def generate_pdf_form(payload):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    story = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=16,
        leading=20,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1e293b'),
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#475569'),
        fontName='Helvetica'
    )

    section_heading = ParagraphStyle(
        'SecHeading',
        parent=styles['Heading2'],
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#0f172a'),
        fontName='Helvetica-Bold'
    )

    cell_style = ParagraphStyle(
        'CellText',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#334155'),
        fontName='Helvetica'
    )

    cell_bold = ParagraphStyle(
        'CellBold',
        parent=cell_style,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#0f172a')
    )

    # Clean profile data with date and CNIC formatting
    profile = payload.get("user_profile", {})
    full_name = profile.get("full_name") or "Not Specified"
    raw_cnic = profile.get("cnic_number") or "Not Specified"
    cnic = format_cnic_clean(raw_cnic)
    father = profile.get("father_name") or "Not Specified"
    raw_dob = profile.get("dob") or "Not Specified"
    dob = format_date_clean(raw_dob)
    city = profile.get("city") or "Not Specified"
    phone = profile.get("phone") or "Not Specified"
    address = profile.get("address") or "Not Specified"
    email = profile.get("email") or "applicant@example.com"

    # Service & Verification Data
    rag = payload.get("rag_verification", {})
    service_req = payload.get("service_request", {})
    dept_name = service_req.get("department", "GOVERNMENT SERVICE").upper()

    # Smart Fee String formatting
    fee_val = rag.get("official_fee_pkr")
    if dept_name == "FBR" or fee_val == 0:
        fee_str = "PKR 0 (Free of Cost)"
    elif dept_name == "PASSPORT":
        fee_str = "PKR 4,500 (Normal) / PKR 7,500 (Urgent)"
    else:
        fee_str = f"PKR {fee_val:,}" if isinstance(fee_val, (int, float)) and fee_val > 0 else "PKR 750 (Normal) / PKR 1,500 (Urgent)"

    days_val = rag.get("processing_days")
    days_str = f"{days_val} Working Days" if days_val else "15 Working Days (Standard)"

    eligibility_str = "Eligible — Meets standard criteria" if rag.get("eligible") is not False else "Requires manual verification"

    notes_str = rag.get("policy_notes") or "Standard public service application guidelines apply."

    # Department-Specific Checklist Defaults
    dept_defaults = {
        "NADRA": [
            "Original Expired CNIC / Smart Card",
            "Photocopy of Father's or Spouse's CNIC",
            "Proof of Address / Paid Utility Bill"
        ],
        "PASSPORT": [
            "Original CNIC / Smart Card with 1 Photocopy",
            "Existing Original Passport with 1 Photocopy",
            "Bank Fee Payment Challan or Digital Receipt"
        ],
        "FBR": [
            "Valid CNIC / Smart Card Copy",
            "Paid Electricity or Gas Utility Bill Copy",
            "Active Mobile Phone Number registered under applicant's CNIC"
        ]
    }

    raw_docs = rag.get("required_documents") or []
    # Replace generic strings like "Previous Document" or empty arrays
    if not raw_docs or any("previous document" in str(d).lower() for d in raw_docs):
        req_docs = dept_defaults.get(dept_name, dept_defaults["NADRA"])
    else:
        req_docs = raw_docs

    # --- Header Banner ---
    story.append(Paragraph("<b>NATIONAL PUBLIC SERVICE APPLICATION</b>", title_style))
    story.append(Paragraph(f"Department: {dept_name} | Ref Code: AGV-{dept_name}-2026", subtitle_style))
    story.append(Spacer(1, 12))

    # --- Section 1: Applicant Profile ---
    story.append(Paragraph("1. APPLICANT PERSONAL INFORMATION", section_heading))
    story.append(Spacer(1, 4))

    profile_data = [
        [Paragraph("Full Name", cell_bold), Paragraph(full_name, cell_style), Paragraph("CNIC Number", cell_bold), Paragraph(cnic, cell_style)],
        [Paragraph("Father/Husband", cell_bold), Paragraph(father, cell_style), Paragraph("Date of Birth", cell_bold), Paragraph(dob, cell_style)],
        [Paragraph("City", cell_bold), Paragraph(city, cell_style), Paragraph("Contact Phone", cell_bold), Paragraph(phone, cell_style)],
        [Paragraph("Address", cell_bold), Paragraph(address, cell_style), Paragraph("Email", cell_bold), Paragraph(email, cell_style)]
    ]

    t_profile = Table(profile_data, colWidths=[110, 160, 100, 170])
    t_profile.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_profile)
    story.append(Spacer(1, 12))

    # --- Section 2: Policy & Fee Summary ---
    story.append(Paragraph("2. VERIFIED SERVICE & POLICY SUMMARY", section_heading))
    story.append(Spacer(1, 4))

    service_data = [
        [Paragraph("Target Department", cell_bold), Paragraph(dept_name, cell_style)],
        [Paragraph("Eligibility Status", cell_bold), Paragraph(eligibility_str, cell_style)],
        [Paragraph("Official Schedule Fee", cell_bold), Paragraph(fee_str, cell_style)],
        [Paragraph("Estimated Processing Time", cell_bold), Paragraph(days_str, cell_style)]
    ]

    t_service = Table(service_data, colWidths=[160, 380])
    t_service.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f1f5f9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_service)
    story.append(Spacer(1, 12))

    # --- Section 3: Required Checklist ---
    story.append(Paragraph("3. REQUIRED DOCUMENTS CHECKLIST", section_heading))
    story.append(Spacer(1, 4))

    chk_data = [[Paragraph(f"[  ]  {i+1}. {doc}", cell_style)] for i, doc in enumerate(req_docs)]
    t_chk = Table(chk_data, colWidths=[540])
    t_chk.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_chk)
    story.append(Spacer(1, 12))

    # --- Section 4: Policy Notes ---
    story.append(Paragraph("4. OFFICIAL GUIDANCE NOTES", section_heading))
    story.append(Spacer(1, 4))
    story.append(Paragraph(notes_str, cell_style))
    story.append(Spacer(1, 16))

    # --- Section 5: Signature Block ---
    story.append(Paragraph("5. APPLICANT DECLARATION", section_heading))
    story.append(Spacer(1, 4))
    story.append(Paragraph("I hereby declare that all information provided above is authentic and supported by attached identity documents.", cell_style))
    story.append(Spacer(1, 24))

    sig_data = [
        [Paragraph("<b>Applicant Signature:</b> _______________________", cell_style), Paragraph("<b>Date:</b> " + time.strftime("%Y-%m-%d"), cell_style)]
    ]
    t_sig = Table(sig_data, colWidths=[340, 200])
    t_sig.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
    story.append(t_sig)

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()