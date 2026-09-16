import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.load_workbook('D:\\lankford-web-hub\\backend\\ITS831 - AI Risk Management Register - Jeremy Lankford.xlsx')

for name in ['Fault Tree Analysis', 'Monte Carlo Simulation']:
    if name in wb.sheetnames:
        del wb[name]

# Shared Styles
font_family = "Arial"
title_font = Font(name=font_family, size=14, bold=True, color="1F497D")
subtitle_font = Font(name=font_family, size=9, italic=True, color="595959")
th_font = Font(name=font_family, size=10, bold=True, color="FFFFFF")
body_font = Font(name=font_family, size=9, bold=False, color="000000")
body_bold = Font(name=font_family, size=9, bold=True, color="000000")
math_font = Font(name=font_family, size=9, italic=True, color="1F497D")

border_thin = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)
border_header = Border(
    left=Side(style='thin', color='000000'),
    right=Side(style='thin', color='000000'),
    top=Side(style='medium', color='000000'),
    bottom=Side(style='medium', color='000000')
)

fill_navy = PatternFill(start_color='1F497D', end_color='1F497D', fill_type='solid')
fill_blue_sec = PatternFill(start_color='2E75B6', end_color='2E75B6', fill_type='solid')
fill_accent = PatternFill(start_color='D9E1F2', end_color='D9E1F2', fill_type='solid')
fill_gate = PatternFill(start_color='FFF2CC', end_color='FFF2CC', fill_type='solid')
fill_top = PatternFill(start_color='FCE4D6', end_color='FCE4D6', fill_type='solid')

# ----------------- 1. FAULT TREE ANALYSIS -----------------
ws_fta = wb.create_sheet(title='Fault Tree Analysis')
ws_fta.views.sheetView[0].showGridLines = True
ws_fta['A1'] = "Fault Tree Analysis (FTA): OncoVision AI Diagnostic System"
ws_fta['A1'].font = title_font
ws_fta['A2'] = "Systemic Failure Pathway Modeling for Top Event: Undetected Malignancy & Diagnostic Failure"
ws_fta['A2'].font = subtitle_font

fta_headers = ["Node ID", "Event Level", "Gate Type", "Event / Failure Description", "Mapped Risk Ref", "Logic / Formula", "Failure Prob (P)", "Operational Context & Justification"]
for c_idx, h in enumerate(fta_headers, 1):
    c = ws_fta.cell(row=4, column=c_idx, value=h)
    c.font, c.fill, c.border = th_font, fill_navy, border_header
    c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

fta_rows = [
    ("TE-01", "TOP EVENT", "AND Gate", "Undetected Malignancy Reaches Patient / Erroneous Clinical Discharge", "Risk 1 (Primary)", "=G6*G12", None, "Critical diagnostic failure: AI false negative occurs AND clinical verification fails."),
    ("G-01", "Sub-System Gate 1", "OR Gate", "AI Model Diagnostic Detection Failure (CADe/CADx False Negative)", "Risk 1, 2, 4, 7", "=1-(1-G7)*(1-G8)*(1-G9)*(1-G10)", None, "Model fails to generate bounding box overlay or falls below 85% confidence threshold."),
    ("BE-01", "Basic Event", "Primary", "Subtle Lesion Density Below Intrinsic Model Detection Threshold", "Risk 1", "Input Parameter", 0.0450, "Micro-calcifications or subtle tissue densities misclassified as benign background."),
    ("BE-02", "Basic Event", "Secondary", "Data & Covariate Shift / CT-MRI Scanner Calibration Drift", "Risk 4", "Input Parameter", 0.0350, "Slice thickness changes, tube voltage drift, or protocol variance degrade accuracy."),
    ("BE-03", "Basic Event", "Secondary", "Demographic Training Disparity & Subgroup Performance Bias", "Risk 2", "Input Parameter", 0.0400, "Underrepresented demographic subgroups suffer higher error rates."),
    ("BE-04", "Basic Event", "Secondary", "Adversarial Perturbation / Pixel Noise / Header Artifacts", "Risk 7", "Input Parameter", 0.0150, "DICOM metadata corruption or sensor noise alter feature representations."),
    ("G-02", "Sub-System Gate 2", "OR Gate", "Clinical Safety Net / Radiologist Human Oversight Fails", "Risk 5", "=1-(1-G13)*(1-G14)", None, "Human-in-the-loop verification protocol bypassed or compromised."),
    ("BE-05", "Basic Event", "Human Factor", "Automation Bias & Over-Reliance on AI Bounding Boxes", "Risk 5", "Input Parameter", 0.0600, "Clinician assumes absence of AI overlay confirms negative pathology."),
    ("BE-06", "Basic Event", "Human Factor", "Radiologist Cognitive Fatigue / High Caseload Time Pressure", "Operational Support", "Input Parameter", 0.0500, "Heavy clinical shift caseload reduces unassisted visual search diligence."),
    ("G-03", "Institutional Gate", "OR Gate", "Enterprise Security & Governance Compliance Failure", "Risk 3, 6", "=1-(1-G16)*(1-G17)", None, "Breach of legal or regulatory framework during clinical diagnostic operations."),
    ("BE-07", "Basic Event", "Legal / Cyber", "Cloud Inference Transmission Protected Health Information (PHI) Breach", "Risk 3", "Input Parameter", 0.0200, "DICOM de-identification bypass or transmission intercept violates HIPAA."),
    ("BE-08", "Basic Event", "Legal / Regulatory", "Unapproved Model Retraining Deployment Violating FDA SaMD Rules", "Risk 6", "Input Parameter", 0.0100, "Uncontrolled continuous-learning push bypassed Change Control Board governance.")
]

for idx, rdata in enumerate(fta_rows):
    r = 5 + idx
    for c_idx in range(1, 9):
        c = ws_fta.cell(row=r, column=c_idx)
        c.border, c.font, c.alignment = border_thin, body_font, Alignment(vertical='center')
    ws_fta.cell(row=r, column=1, value=rdata[0]).alignment = Alignment(horizontal='center')
    ws_fta.cell(row=r, column=2, value=rdata[1]).alignment = Alignment(horizontal='center')
    ws_fta.cell(row=r, column=3, value=rdata[2]).alignment = Alignment(horizontal='center')
    ws_fta.cell(row=r, column=4, value=rdata[3])
    ws_fta.cell(row=r, column=5, value=rdata[4]).alignment = Alignment(horizontal='center')
    ws_fta.cell(row=r, column=6, value=rdata[5])
    p_c = ws_fta.cell(row=r, column=7, value=rdata[6] if rdata[6] is not None else rdata[5])
    p_c.number_format = '0.0000%'
    p_c.alignment = Alignment(horizontal='right')
    ws_fta.cell(row=r, column=8, value=rdata[7])
    if rdata[1] == "TOP EVENT":
        for c in range(1, 9):
            ws_fta.cell(row=r, column=c).fill, ws_fta.cell(row=r, column=c).font = fill_top, body_bold
    elif "Gate" in rdata[1]:
        for c in range(1, 9):
            ws_fta.cell(row=r, column=c).fill, ws_fta.cell(row=r, column=c).font = fill_gate, body_bold

for col, width in {1: 12, 2: 20, 3: 16, 4: 48, 5: 20, 6: 34, 7: 18, 8: 65}.items():
    ws_fta.column_dimensions[get_column_letter(col)].width = width

# -------------- 2. MONTE CARLO SIMULATION --------------
ws_mc = wb.create_sheet(title='Monte Carlo Simulation')
ws_mc.views.sheetView[0].showGridLines = True
ws_mc['A1'] = "Monte Carlo Simulation: OncoVision Enterprise AI Risk Portfolio"
ws_mc['A1'].font = title_font
ws_mc['A2'] = "Stochastic Quantitative Risk Assessment Across 1,000 Operational Diagnostic Trials"
ws_mc['A2'].font = subtitle_font

ws_mc['A4'] = "1. Simulation Parameters & Calibrated Loss Distributions"
ws_mc['A4'].font = Font(name=font_family, size=11, bold=True, color="1F497D")

for c_idx, h in enumerate(["Risk #", "Risk Category", "Risk Event Description", "Register Prob", "Model P(Event)", "Min Impact ($k)", "Likely Impact ($k)", "Max Impact ($k)", "Simulated Loss Engine Formula"], 1):
    c = ws_mc.cell(row=5, column=c_idx, value=h)
    c.font, c.fill, c.border = th_font, fill_navy, border_header
    c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

param_data = [
    (1, "Technical", "Undetected False Negatives & Model Hallucinations", "H", 0.08, 250, 750, 2000),
    (2, "Ethical", "Demographics Performance Bias & Unequal Error Rates", "H", 0.07, 100, 300, 800),
    (3, "Legal", "Loss/Disclosure of Sensitive Patient Health Info (PHI)", "M", 0.04, 200, 600, 1800),
    (4, "Operational", "Data & Covariate Shift / Hardware Calibration Drift", "H", 0.09, 40, 120, 350),
    (5, "Operational", "Automation Bias & Clinician Over-Reliance", "H", 0.08, 50, 150, 400),
    (6, "Legal", "Regulatory Non-Compliance with FDA SaMD Rules", "L", 0.02, 150, 500, 1500),
    (7, "Technical", "Adversarial Perturbation & Image Artifact Sensitivity", "L", 0.03, 30, 80, 250)
]

for idx, p in enumerate(param_data):
    r = 6 + idx
    for c in range(1, 10):
        cell = ws_mc.cell(row=r, column=c)
        cell.border, cell.font, cell.alignment = border_thin, body_font, Alignment(vertical='center')
    ws_mc.cell(row=r, column=1, value=p[0]).alignment = Alignment(horizontal='center')
    ws_mc.cell(row=r, column=2, value=p[1]).alignment = Alignment(horizontal='center')
    ws_mc.cell(row=r, column=3, value=p[2])
    ws_mc.cell(row=r, column=4, value=p[3]).alignment = Alignment(horizontal='center')
    p_c = ws_mc.cell(row=r, column=5, value=p[4])
    p_c.number_format, p_c.alignment = '0.0%', Alignment(horizontal='right')
    for col_i, val in enumerate([p[5], p[6], p[7]], 6):
        c_cell = ws_mc.cell(row=r, column=col_i, value=val)
        c_cell.number_format, c_cell.alignment = '$#,##0"k"', Alignment(horizontal='right')
    ws_mc.cell(row=r, column=9, value=f'=IF(RAND()<{p[4]}, F{r}+RAND()*(H{r}-F{r}), 0)').font = math_font

ws_mc['A15'] = "2. Simulation Summary Statistics (N = 1,000 Realizations)"
ws_mc['A15'].font = Font(name=font_family, size=11, bold=True, color="1F497D")

for c_idx, h in enumerate(["Statistical Metric", "Excel Formula", "Simulated Value ($k)", "Strategic Governance Interpretation"], 1):
    c = ws_mc.cell(row=16, column=c_idx, value=h)
    c.font, c.fill, c.border = th_font, fill_navy, border_header
    c.alignment = Alignment(horizontal='center', vertical='center')

stats_defs = [
    ("Expected Portfolio Loss (Mean)", "=AVERAGE(I26:I1025)", "$#,##0", "Expected baseline annualized clinical risk exposure for budget reserves."),
    ("Median Loss (50th Percentile)", "=MEDIAN(I26:I1025)", "$#,##0", "Typical diagnostic review cycle risk realization."),
    ("Standard Deviation (Volatility)", "=STDEV.S(I26:I1025)", "$#,##0", "Dispersion of risk outcomes across fluctuating clinical environments."),
    ("Value-at-Risk (95% VaR)", "=PERCENTILE.INC(I26:I1025, 0.95)", "$#,##0", "Maximum anticipated loss under normal adverse conditions (95% confidence)."),
    ("Value-at-Risk (99% Extreme VaR)", "=PERCENTILE.INC(I26:I1025, 0.99)", "$#,##0", "Tail risk threshold representing catastrophic compound failure."),
    ("Minimum Realized Loss", "=MIN(I26:I1025)", "$#,##0", "Best-case operational cycle with zero triggering incidents."),
    ("Maximum Realized Loss", "=MAX(I26:I1025)", "$#,##0", "Severe worst-case realization across multiple cascading failures.")
]

for idx, st in enumerate(stats_defs):
    r = 17 + idx
    for c in range(1, 5):
        cell = ws_mc.cell(row=r, column=c)
        cell.border, cell.font, cell.alignment = border_thin, body_font, Alignment(vertical='center')
    ws_mc.cell(row=r, column=1, value=st[0]).font = body_bold
    ws_mc.cell(row=r, column=2, value=st[1]).font = math_font
    val_c = ws_mc.cell(row=r, column=3, value=st[1])
    val_c.number_format, val_c.font, val_c.fill = st[2], body_bold, fill_accent
    val_c.alignment = Alignment(horizontal='right')
    ws_mc.cell(row=r, column=4, value=st[3])

ws_mc['A24'] = "3. Stochastic Trial Iteration Table (1,000 Runs)"
ws_mc['A24'].font = Font(name=font_family, size=11, bold=True, color="1F497D")

iter_h = ["Trial #", "Risk 1: False Neg ($k)", "Risk 2: Bias ($k)", "Risk 3: PHI Breach ($k)", "Risk 4: Drift ($k)", "Risk 5: Auto Bias ($k)", "Risk 6: FDA Non-Comp ($k)", "Risk 7: Noise/Artifact ($k)", "Total Exposure ($k)"]
for c_idx, h in enumerate(iter_h, 1):
    c = ws_mc.cell(row=25, column=c_idx, value=h)
    c.font, c.fill, c.border = th_font, fill_blue_sec, border_header
    c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

for trial in range(1, 1001):
    r = 25 + trial
    ws_mc.cell(row=r, column=1, value=trial).alignment = Alignment(horizontal='center')
    ws_mc.cell(row=r, column=1).font, ws_mc.cell(row=r, column=1).border = body_font, border_thin
    for risk_idx in range(1, 8):
        pr = 5 + risk_idx
        c = 1 + risk_idx
        formula = f'=IF(RAND()<$E${pr}, $F${pr}+RAND()*($H${pr}-$F${pr}), 0)'
        cell = ws_mc.cell(row=r, column=c, value=formula)
        cell.number_format, cell.font, cell.border = '$#,##0', body_font, border_thin
        cell.alignment = Alignment(horizontal='right')
    tot = ws_mc.cell(row=r, column=9, value=f'=SUM(B{r}:H{r})')
    tot.number_format, tot.font, tot.border = '$#,##0', body_bold, border_thin
    tot.alignment = Alignment(horizontal='right')

for col, width in {1: 10, 2: 24, 3: 40, 4: 16, 5: 16, 6: 18, 7: 20, 8: 20, 9: 38}.items():
    ws_mc.column_dimensions[get_column_letter(col)].width = width

wb.save('ITS831 - AI Risk Management Register - Jeremy Lankford.xlsx')
print("Complete! Open the file in Excel.")