---
name: civil-boq-and-cost-estimation
description: Mandatory civil engineering cost estimation and Bill of Quantities (BOQ) preparation engine based on the official Khyber Pakhtunkhwa Market Rate System (KPK MRS) published by Finance Department KP (https://www.finance.gkp.pk/articles/info-desk/market-rate-system). Covers earthwork, concrete, canal lining, river protection & diversion works, gabions, stone pitching, rebar, and district location factors.
---

# Civil BOQ and Cost Estimation Skill (KPK MRS Basis)

> [!IMPORTANT]
> **Mandatory Estimation Rule**: For all engineering estimates, feasibility reports, PC-I documents, and Bills of Quantities (BOQs), **ALWAYS use the latest Market Rate System (MRS)** published by the Finance Department, Government of Khyber Pakhtunkhwa ([finance.gkp.pk/articles/info-desk/market-rate-system](https://www.finance.gkp.pk/articles/info-desk/market-rate-system)) unless the user explicitly specifies otherwise.
> 
> **Current Active Standard**: **KPK MRS-2025 (1st Bi-Annual)**.
> **Local Reference & Index**: `C:\tools\civil-hydraulics\kpk-mrs\kpk_mrs_2025_index.json` (3,036 officially indexed items).

---

## 1. District Location Factors (Cost Multipliers)

Rates in the KPK MRS schedule are base Peshawar rates ($1.00$). When estimating works outside Peshawar, multiply all labour and composite rates by the official **District Location Factor**:

| District / Territory | Location Factor | District / Territory | Location Factor |
| :--- | :--- | :--- | :--- |
| **Peshawar, Mardan, Charsadda, Nowshera, Swabi, Haripur** | **1.00** | **Buner** | **1.09** |
| **Abbottabad, Bannu, D.I. Khan, Kohat, Tank** | **1.03** | **Shangla, Torghar, Upper Dir** | **1.10** |
| **Hangu, Karak, Lakki Marwat** | **1.05** | **Kohistan** | **1.14** |
| **Battagram, Lower Dir, Malakand, Mansehra, Swat** | **1.08** | **Chitral** | **1.15** |
| **Khyber, Mohmand, Orakzai (Merged Areas)** | **1.05** | **Bajaur, Kurram, Waziristan (N & S)** | **1.08** |

$$\text{Project Rate} = \text{Base MRS Rate} \times \text{District Factor}$$

---

## 2. Standard KPK MRS-2025 Master Item Rates (Metric Basis)

### 2.1 Chapter 03: Earthwork (Excavation & Embankment)
| Item Code | Official MRS Description | Unit | Base Labour (PKR) | Base Composite (PKR) |
| :--- | :--- | :--- | :--- | :--- |
| **03-01-a** | Earth excavation undressed: ashes, sand, soft soil or silt clearance | $\text{m}^3$ | 167.52 | 167.52 |
| **03-01-b** | Earth excavation undressed: in ordinary soil | $\text{m}^3$ | 201.03 | 201.03 |
| **03-02-b** | Earth excavation by mechanical means undressed (lead up to $15\text{ m}$) | $\text{m}^3$ | 0.00 | **119.07** |
| **03-03-a** | Excavate unsuitable common material | $\text{m}^3$ | 0.00 | **513.22** |
| **03-03-b** | Excavate unsuitable hard rock material | $\text{m}^3$ | 0.00 | **1,066.19** |
| **03-04-a** | Bed clearance and dressing slopes of drains within $15\text{ m}$ | $\text{m}^3$ | 250.17 | **250.17** |
| **03-05-a** | Borrow pit excavation undressed lead up to $30\text{ m}$ in ordinary soil | $\text{m}^3$ | 0.00 | **470.58** |
| **03-06-a** | Embankment formation from borrow & mechanical compaction to 95% AASHTO | $\text{m}^3$ | 94.98 | **701.99** |

---

### 2.2 Chapter 06: Concrete Works & Reinforcement Steel
| Item Code | Official MRS Description | Unit | Base Labour (PKR) | Base Composite (PKR) |
| :--- | :--- | :--- | :--- | :--- |
| **06-05-i** | Plain Cement Concrete (PCC 1:4:8) in foundation / bed | $\text{m}^3$ | 2,415.03 | **12,340.56** |
| **06-05-h** | Plain Cement Concrete (PCC 1:3:6) in mass concrete / toe walls | $\text{m}^3$ | 2,415.03 | **13,983.72** |
| **06-05-f** | Plain Cement Concrete (PCC 1:2:4) placing, compacting & curing | $\text{m}^3$ | 2,415.03 | **17,035.28** |
| **06-07-a-02** | RCC in structural members (1:1.5:3) in-situ or precast | $\text{m}^3$ | 4,824.69 | **22,220.48** |
| **06-07-a-03** | RCC in structural members (1:2:4) in-situ or precast | $\text{m}^3$ | 4,824.69 | **19,446.34** |
| **06-08-b** | **Supply & fabricate M.S. deformed rebar Grade 60 (ASTM A615)** | **Tonne** | 14,317.65 | **306,713.50** |
| | *(Equivalent per kilogram)* | $\text{kg}$ | 14.32 | **306.71** |

---

### 2.3 Chapter 17: Lining of Canals
| Item Code | Official MRS Description | Unit | Base Labour (PKR) | Base Composite (PKR) |
| :--- | :--- | :--- | :--- | :--- |
| **17-10-a-01** | $4''$ thick PCC lining bed (Ratio 1:2:4) washed graded crushed stone | $\text{m}^2$ | 245.00 | **1,720.50** |
| **17-10-b-01** | $4''$ thick PCC lining on slope (Ratio 1:2:4) washed graded stone | $\text{m}^2$ | 280.00 | **1,850.00** |
| **17-11-c** | Precast parabolic concrete segment $24'' \times 14''$ ($600\text{mm} \times 360\text{mm}$) | $\text{m}$ | 506.33 | **5,105.77** |
| **17-11-d** | Precast parabolic concrete segment $25.5'' \times 18''$ ($640\text{mm} \times 460\text{mm}$) | $\text{m}$ | 622.54 | **6,507.83** |

---

### 2.4 Chapter 19: Protection & Diversion Works (River Training, Spurs & Groynes)
| Item Code | Official MRS Description | Unit | Base Labour (PKR) | Base Composite (PKR) |
| :--- | :--- | :--- | :--- | :--- |
| **19-25** | Providing and laying stone pitching/filling, dry hand packed in pitching & aprons | $\text{m}^3$ | 1,161.50 | **3,080.50** |
| **19-26** | Supplying stone and stone filling in GI wire crates (Gabions) & sewing | $\text{m}^3$ | 1,340.19 | **3,259.19** |
| **19-27** | Providing & laying stone pitching with hammer-dressed stones on surface | $\text{m}^3$ | 1,840.00 | **4,374.00** |
| **19-30-d** | Grouted stone pitching in 1:6 cement-sand mortar on slopes / bed | $\text{m}^3$ | 1,980.00 | **5,450.00** |
| **19-38-f-01** | Stone pitching for top layer only on slope | $\text{m}^3$ | 3,663.19 | **5,965.99** |
| **19-38-g-01** | Laying stone or spall / quarry spawl filling on level apron | $\text{m}^3$ | 513.74 | **2,624.64** |
| **19-45** | Gachi pitching ($1\text{ ft}$ thick) | $\text{m}^2$ | 885.56 | **885.56** |

---

## 3. Real-Time MRS Query CLI & Python Integration

Query any of the 3,036 official KPK MRS items directly via PowerShell/Terminal:

```bash
# Query an exact item code and adjust for Swat district:
python C:\tools\civil-hydraulics\kpk-mrs\mrs_lookup.py --code 19-25 --district Swat

# Search by keywords across all chapters:
python C:\tools\civil-hydraulics\kpk-mrs\mrs_lookup.py --query "gabion" --district Chitral

# Query Grade 60 steel rebar in Abbottabad:
python C:\tools\civil-hydraulics\kpk-mrs\mrs_lookup.py --code 06-08-b --district Abbottabad
```

### Automated BOQ Generator Using Official KPK MRS API

```python
import sys
import os
sys.path.append(r"C:\tools\civil-hydraulics\kpk-mrs")
from mrs_lookup import lookup_mrs

class KPK_MRS_BOQ:
    def __init__(self, project_title: str, district: str = "Peshawar"):
        self.project_title = project_title
        self.district = district
        self.items = []

    def add_mrs_item(self, code: str, quantity: float, custom_desc: str = None):
        res = lookup_mrs(code=code, district=self.district)
        if not res:
            raise ValueError(f"KPK MRS item code {code} not found.")
        it = res[0]
        desc = custom_desc or it["description"]
        unit = it["unit"]
        rate = it["adjusted_composite_rate"]
        amount = round(quantity * rate, 2)
        
        self.items.append({
            "code": it["code"],
            "description": desc,
            "unit": unit,
            "quantity": quantity,
            "rate_pkr": rate,
            "amount_pkr": amount
        })

    def print_boq(self):
        print(f"=== BILL OF QUANTITIES: {self.project_title} ===")
        print(f"Basis: KPK MRS-2025 (1st Bi-Annual) | District: {self.district}\n")
        total = 0.0
        for i, it in enumerate(self.items, 1):
            print(f"{i}. [{it['code']}] {it['description']}")
            print(f"   Qty: {it['quantity']:,.2f} {it['unit']} @ PKR {it['rate_pkr']:,.2f}/{it['unit']} = PKR {it['amount_pkr']:,.2f}")
            total += it["amount_pkr"]
        print("-" * 75)
        print(f"DIRECT COST SUBTOTAL       : PKR {total:,.2f}")
        cont = round(total * 0.05, 2)
        print(f"CONTINGENCY (5%)           : PKR {cont:,.2f}")
        print(f"GRAND TOTAL ESTIMATE       : PKR {total + cont:,.2f}")

if __name__ == "__main__":
    boq = KPK_MRS_BOQ("River Spur & Bank Protection Works", district="Swat")
    boq.add_mrs_item("03-02-b", 5200.0, "Mechanical excavation in river bed for apron")
    boq.add_mrs_item("03-06-a", 14000.0, "Compacted embankment formation (95% AASHTO)")
    boq.add_mrs_item("19-25", 2800.0, "Dry stone boulder pitching in apron and slope")
    boq.add_mrs_item("19-26", 1500.0, "Stone filling in GI wire gabion crates")
    boq.add_mrs_item("06-05-h", 450.0, "PCC 1:3:6 in toe cutoff wall")
    boq.add_mrs_item("06-08-b", 12.5, "Grade 60 steel rebar in regulator and sluices")
    boq.print_boq()
```
