---
name: civil-boq-and-cost-estimation
description: Production civil engineering cost estimation and Bill of Quantities (BOQ) preparation skill. Covers Composite Schedule of Rates (CSR/NHA/CESMM4), earthwork mass-haul calculation, stone pitching/riprap, gabions, geotextiles, concrete mix costing, rebar tonnage, and automated Excel/Typst BOQ generation.
---

# Civil BOQ and Cost Estimation Skill

This skill provides standardized item rate analysis, quantity takeoff equations, and automated Python scripts for generating detailed Bills of Quantities (BOQs) and engineer's cost estimates for civil, irrigation, river training, and highway drainage infrastructure projects.

---

## 1. Standard Civil Engineering Measurement Units & Item Coding

Based on Composite Schedule of Rates (CSR), NHA Specifications, and CESMM4 (Civil Engineering Standard Method of Measurement):

| Item Code | Description | Standard Pay Unit | Measurement Rule |
| :--- | :--- | :--- | :--- |
| **EW-01** | Earthwork excavation in open channel / foundation / drain (common soil) | $\text{m}^3$ ($1000\text{ m}^3$ or $\text{m}^3$) | Measured in solid cut volume |
| **EW-02** | Earthwork excavation in saturated / marshy soil / under water | $\text{m}^3$ | Extra over dry excavation |
| **EW-03** | Embankment fill from borrow pit compacted to 95% AASHTO T-180 | $\text{m}^3$ | Measured in compacted embankment volume |
| **EW-04** | Lead haulage of earth / stones beyond free haul ($1\text{ km}$) | $\text{m}^3\cdot\text{km}$ | Volume $\times$ distance |
| **RP-01** | Dry stone boulder pitching ($30 - 80\text{ kg}$) on embankment slopes | $\text{m}^3$ | Net laid volume |
| **RP-02** | Heavy stone boulder launching apron in river training works | $\text{m}^3$ | Dumped net volume |
| **GB-01** | Galvanized wire mesh gabion boxes ($1\text{m} \times 1\text{m} \times 1\text{m}$) filled with stone | $\text{m}^3$ | External crate volume |
| **GT-01** | Non-woven needle-punched polypropylene geotextile ($250\text{ g/m}^2$) | $\text{m}^2$ | Measured flat area (10% lap included) |
| **CC-01** | Plain Cement Concrete (PCC 1:4:8 or 1:3:6) in foundation / bed | $\text{m}^3$ | Net placed concrete |
| **CC-02** | Reinforced Cement Concrete (RCC 1:2:4 / 1:1.5:3) in structural walls/slabs | $\text{m}^3$ | Net placed volume excluding rebar |
| **ST-01** | High yield deformed steel rebar Grade 60 (ASTM A615) cut, bent & tied | Tonne ($\text{t}$) | Theoretical weight + 5% lap/wastage |

---

## 2. Quantity Takeoff Formulations

### 2.1 Earthwork Volume (Average End Area & Prismoidal)
For a channel or embankment length $L$ between chainage station 1 and 2:
- **Average End Area**:
  $$V = \frac{A_1 + A_2}{2} \times L$$
- **Prismoidal Formula** (higher accuracy for transitioning cuts):
  $$V = \frac{L}{6} (A_1 + 4 A_m + A_2)$$
  *(Where $A_m$ is the cross-sectional area at the mid-point).*

### 2.2 Rebar Tonnage Estimation Rules of Thumb
When structural reinforcement details are preliminary:
- Culvert deck slabs / bridge decks: $110 - 130\text{ kg/m}^3$ of concrete.
- Retaining walls / abutments: $90 - 110\text{ kg/m}^3$.
- Canal lining retaining walls / flumes: $80 - 100\text{ kg/m}^3$.
- Footings / raft slabs: $70 - 90\text{ kg/m}^3$.
- **Bar Weight Formula**:
  $$W_{\text{bar}} = \frac{d^2}{162.2} \quad (\text{kg/m, where } d \text{ is bar diameter in mm})$$

### 2.3 Concrete Material Quantities (Nominal Mixes)
Dry volume factor = $1.54$ (accounts for void filling when water is added).
- **PCC 1:4:8 (Sum of parts = 13)**:
  - Cement: $\frac{1}{13} \times 1.54 = 0.118\text{ m}^3 = 3.4\text{ bags/m}^3$ ($50\text{ kg}$ bag = $0.035\text{ m}^3$).
  - Sand: $\frac{4}{13} \times 1.54 = 0.474\text{ m}^3$.
  - Coarse Aggregate: $\frac{8}{13} \times 1.54 = 0.948\text{ m}^3$.
- **PCC 1:3:6 (Sum of parts = 10)**:
  - Cement: $\frac{1}{10} \times 1.54 = 0.154\text{ m}^3 = 4.4\text{ bags/m}^3$.
  - Sand: $\frac{3}{10} \times 1.54 = 0.462\text{ m}^3$.
  - Coarse Aggregate: $\frac{6}{10} \times 1.54 = 0.924\text{ m}^3$.
- **RCC 1:2:4 (Sum of parts = 7)**:
  - Cement: $\frac{1}{7} \times 1.54 = 0.220\text{ m}^3 = 6.3\text{ bags/m}^3$.
  - Sand: $\frac{2}{7} \times 1.54 = 0.440\text{ m}^3$.
  - Coarse Aggregate: $\frac{4}{7} \times 1.54 = 0.880\text{ m}^3$.

---

## 3. Production BOQ Generator Script (Python)

```python
import pandas as pd
import json

class CivilBOQEstimator:
    def __init__(self, project_name: str, currency: str = "PKR"):
        self.project_name = project_name
        self.currency = currency
        self.items = []
        
    def add_item(self, code: str, desc: str, unit: str, quantity: float, unit_rate: float):
        amount = round(quantity * unit_rate, 2)
        self.items.append({
            "Item Code": code,
            "Description": desc,
            "Unit": unit,
            "Quantity": round(quantity, 2),
            f"Rate ({self.currency})": round(unit_rate, 2),
            f"Amount ({self.currency})": amount
        })
        
    def generate_summary(self, overhead_pct: float = 15.0, contingency_pct: float = 5.0) -> dict:
        df = pd.DataFrame(self.items)
        subtotal = df[f"Amount ({self.currency})"].sum()
        overheads = round(subtotal * (overhead_pct / 100.0), 2)
        contingency = round(subtotal * (contingency_pct / 100.0), 2)
        grand_total = round(subtotal + overheads + contingency, 2)
        
        return {
            "df": df,
            "subtotal": subtotal,
            "overhead_profit": overheads,
            "contingency": contingency,
            "grand_total": grand_total
        }

    def export_markdown(self, overhead_pct: float = 15.0, contingency_pct: float = 5.0) -> str:
        summary = self.generate_summary(overhead_pct, contingency_pct)
        df = summary["df"]
        
        md = f"### Bill of Quantities (BOQ): {self.project_name}\n\n"
        md += df.to_markdown(index=False)
        md += "\n\n"
        md += f"- **Direct Subtotal**: `{self.currency} {summary['subtotal']:,.2f}`\n"
        md += f"- **Contractor Overhead & Profit ({overhead_pct}%)**: `{self.currency} {summary['overhead_profit']:,.2f}`\n"
        md += f"- **Contingencies & Physical Variations ({contingency_pct}%)**: `{self.currency} {summary['contingency']:,.2f}`\n"
        md += f"- **Grand Total Engineer's Estimate**: **`{self.currency} {summary['grand_total']:,.2f}`**\n"
        return md

if __name__ == "__main__":
    boq = CivilBOQEstimator(project_name="River Training Spur & Flood Levee Package")
    boq.add_item("EW-01", "Excavation in common riverbed alluvium for launch apron", "m3", 4500.0, 320.0)
    boq.add_item("EW-03", "Embankment formation from borrow pit compacted to 95% AASHTO", "m3", 12500.0, 580.0)
    boq.add_item("RP-01", "Dry stone pitching (30-80 kg boulders) on 1:2 riverside slope", "m3", 1850.0, 3400.0)
    boq.add_item("RP-02", "Heavy quarry boulder launching apron at spur nose", "m3", 3200.0, 3850.0)
    boq.add_item("GT-01", "Non-woven needle-punched polypropylene geotextile (250 g/m2)", "m2", 4200.0, 380.0)
    boq.add_item("CC-01", "Plain Cement Concrete (PCC 1:3:6) in toe wall", "m3", 350.0, 14500.0)
    
    print(boq.export_markdown())
```

---

## 4. Quality Control & Cost Engineering Protocol

1. **Rate Composition Audit**: Always break down CSR rates into three pillars:
   - Materials (ex-factory + transport lead).
   - Labor (skilled mason, bhisti, coolie).
   - Equipment rental & POL (fuel, oil, lubricants).
2. **Lead Distance Verification**: Document borrow pit and quarry GPS coordinates to compute actual haulage distances.
3. **Escalation / Price Adjustment**: For contracts $> 12\text{ months}$, incorporate PEC/FIDIC price adjustment formula for diesel, cement, and Grade 60 rebar.
