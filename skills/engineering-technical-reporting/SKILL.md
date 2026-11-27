---
name: engineering-technical-reporting
description: Generates publication-grade engineering inception, feasibility, design, and Planning Commission Proforma 1 (PC-1) technical reports using Typst, automated financial models (EIRR, BCR, NPV), and clean engineering tables. Use when drafting project feasibility studies, tender documentation, or technical appraisal reports.
license: MIT
metadata:
  origin: General-Gemini
tools: Read, Write, Edit, Bash, Grep, Glob
---

# Engineering Technical Reporting & PC-1 Feasibility Skill

Standards, structural outlines, Typst typesetting workflows, and discounted cash-flow financial models for civil and technical engineering reports.

## When to Activate

- Writing technical inception reports, engineering feasibility studies, or design memorandums
- Preparing Planning Commission Proforma 1 (PC-1) project appraisal documentation
- Modeling economic and financial metrics: Benefit-Cost Ratio (BCR), Economic Internal Rate of Return (EIRR), Present Value of Costs (PVC), and Present Value of Benefits (PVB)
- Compiling publication-ready PDF reports via the Typst 0.15+ engine

---

## 1. Technical Report Structure (The Engineering Inception / Feasibility Standard)

Every engineering report generated must follow a crisp, professional sequence:

1. **Executive Summary & Fact Sheet**: Project location, capital cost (CapEx), annual O&M (OpEx), execution timeframe, key engineering metrics, BCR, and EIRR.
2. **Project Background & Problem Statement**: Baseline conditions, deficit analysis, stakeholder demand.
3. **Site & Geophysical Context**: Topography, geology, hydrology, seismicity (PGA zoning), climate data.
4. **Engineering Design Concept**: Design criteria, codes enforced (AASHTO, ACI 318, ASTM, BS EN), layout options, hydraulic/structural calculations.
5. **Bill of Quantities (BOQ) & Cost Estimation**: Itemized civil work quantities, unit rates, contingency allowances.
6. **Implementation Schedule**: Work breakdown structure (WBS), Gantt milestones, procurement packaging.
7. **Economic & Financial Appraisal**: Discounted cash flow (DCF), EIRR, BCR, NPV, sensitivity analysis.
8. **Environmental & Social Impact (ESIA)**: Mitigation measures, regulatory compliance.

---

## 2. PC-1 Discounted Cash-Flow Financial Engine

Automated economic viability evaluator:

```python
import numpy_financial as npf

def evaluate_pc1_project(capital_expenditures: list, annual_om: float, annual_benefits: float, discount_rate: float = 0.12):
    """
    capital_expenditures: list of CapEx for year 0, year 1, etc.
    annual_om: recurring operating cost once operational
    annual_benefits: quantifiable economic benefits per year
    discount_rate: standard discount rate (default 12% per Planning Commission)
    """
    lifecycle_years = 25
    construction_years = len(capital_expenditures)
    
    cash_costs = []
    cash_benefits = []
    net_cash_flows = []
    
    for t in range(lifecycle_years + 1):
        # Costs
        capex = capital_expenditures[t] if t < construction_years else 0.0
        opex = annual_om if t >= construction_years else 0.0
        total_cost = capex + opex
        cash_costs.append(total_cost)
        
        # Benefits
        benefit = annual_benefits if t >= construction_years else 0.0
        cash_benefits.append(benefit)
        
        # Net Flow
        net_cash_flows.append(benefit - total_cost)
        
    # Present Values
    pvc = sum(c / ((1 + discount_rate) ** t) for t, c in enumerate(cash_costs))
    pvb = sum(b / ((1 + discount_rate) ** t) for t, b in enumerate(cash_benefits))
    npv = pvb - pvc
    bcr = pvb / pvc if pvc > 0 else 0.0
    
    # Internal Rate of Return
    try:
        eirr = npf.irr(net_cash_flows)
    except Exception:
        eirr = 0.0
        
    # Sensitivity: +10% Cost, -10% Benefit
    pvc_sens = pvc * 1.10
    pvb_sens = pvb * 0.90
    bcr_sens = pvb_sens / pvc_sens
    
    return {
        'Discount_Rate': f"{discount_rate * 100:.1f}%",
        'PVC_Million': round(pvc / 1e6, 2),
        'PVB_Million': round(pvb / 1e6, 2),
        'NPV_Million': round(npv / 1e6, 2),
        'BCR': round(bcr, 3),
        'EIRR': f"{eirr * 100:.2f}%",
        'Sensitivity_BCR_CostPlus10_BenMinus10': round(bcr_sens, 3),
        'Feasibility_Status': 'Economically Viable' if bcr > 1.0 and eirr >= discount_rate else 'Non-Viable'
    }
```

---

## 3. Typst 0.15+ Publication Template

Compile instantly using `typst compile document.typ output.pdf`:

```typst
#set page(
  paper: "a4",
  margin: (top: 2.5cm, bottom: 2.5cm, left: 3cm, right: 2.5cm),
  header: locate(loc => {
    if loc.page() > 1 [
      #grid(
        columns: (1fr, auto),
        text(9pt, fill: luma(100), font: "Arial")[Civil Infrastructure Feasibility Study],
        text(9pt, fill: luma(100), font: "Arial")[CONFIDENTIAL]
      )
      #line(length: 100%, stroke: 0.5pt + luma(180))
    ]
  }),
  footer: locate(loc => {
    line(length: 100%, stroke: 0.5pt + luma(180))
    grid(
      columns: (1fr, auto),
      text(9pt, fill: luma(100))[Project Technical Inception Report],
      text(9pt, fill: luma(100))[Page #loc.page()]
    )
  })
)

#set text(font: "Liberation Sans", size: 10.5pt, lang: "en")
#set par(justify: true, leading: 0.75em)

// Cover Page Block
#align(center + horizon)[
  #text(22pt, weight: "bold", fill: rgb("#0B3C5D"))[TECHNICAL FEASIBILITY & INCEPTION REPORT] \
  #v(1em)
  #text(14pt, weight: "medium", fill: rgb("#1D2731"))[Municipal Drainage & Stormwater Inundation Mitigation System] \
  #v(2em)
  #rect(width: 80%, fill: rgb("#F0F4F8"), radius: 4pt, inset: 12pt)[
    #align(left)[
      *Executing Agency:* Communication & Works Department \
      *Location:* Regional Basin Zone IV \
      *Date of Submission:* October 2026 \
      *PC-1 Capital Cost:* PKR 1,485.50 Million
    ]
  ]
]
#pagebreak()

// Table of Contents
#outline(indent: auto)
#pagebreak()

= Executive Summary
The proposed infrastructure scheme addresses recurring monsoon inundation affecting a 45-hectare urban catchment. Hydraulic modeling demonstrates that peak discharge reaches $18.4 space "m"^3/"s"$ during a 1-in-25-year 24-hour rainfall event, exceeding existing unlined channel capacity by 240%.

#table(
  columns: (2fr, 1fr, 3fr),
  fill: (col, row) => if row == 0 { rgb("#0B3C5D") } else if calc.odd(row) { rgb("#F7F9FB") } else { none },
  align: (left, center, left),
  stroke: 0.5pt + luma(200),
  [#text(weight: "bold", fill: white)[Key Parameter]], [#text(weight: "bold", fill: white)[Value]], [#text(weight: "bold", fill: white)[Remarks / Basis]],
  [Total Catchment Area], [45.2 ha], [Delineated via ALOS PALSAR 12.5m DEM],
  [Design Rainfall (25-Yr)], [142 mm], [24-Hour Type-II Distribution],
  [Peak Inundation Discharge], [18.42 m³/s], [Computed via EPA-SWMM Dynamic Wave],
  [Capital Expenditure (CapEx)], [PKR 1,485.5 M], [CSR 2026 Scheduled Rates + Taxes],
  [Benefit-Cost Ratio (BCR)], [1.42], [Discounted at 12% over 25-year horizon],
  [Economic IRR (EIRR)], [16.85%], [Exceeds 12% economic hurdle threshold]
)
```

---

## 4. Local Template & Reference Paths

- **Typst Modern Engineering Report**: `C:\tools\engineering-reports\modern-engineering-report\`
- **Reprobe Two-Column Technical Template**: `C:\tools\engineering-reports\reprobe\`
- **Breezy Technical Report**: `C:\tools\engineering-reports\breezy-report\`
- **PC-1 Financial Script**: `C:\Users\Imran\Downloads\General-Gemini\templates\pc1_financial_model.py`
