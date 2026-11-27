---
name: river-training-and-flood-protection
description: Complete civil engineering design and calculation engine for river training works, flood protection embankments (levees/bunds), spurs/groynes, guide bunds (Bell's bunds), launching aprons, riprap stone pitching, and Lacey scour depth analysis.
---

# River Training & Flood Protection Works Skill

This skill delivers rigorous engineering calculations, structural sizing rules, and automated Python engines for designing river training structures, flood protection bunds, guide bunds, spurs, and scour protection works in alluvial and mountainous rivers.

---

## 1. Design Principles & Governing Equations

### 1.1 Lacey's Scour Depth Formulation
For alluvial rivers, the regime scour depth $R$ is calculated as:
- Total discharge basis:
  $$R = 0.473 \left(\frac{Q}{f}\right)^{1/3} \quad (\text{m})$$
- Unit discharge (intensity $q = Q/W_{\text{eff}}$) basis:
  $$R = 1.35 \left(\frac{q^2}{f}\right)^{1/3} \quad (\text{m})$$

Where:
- $Q$ = Design peak flood discharge ($\text{m}^3/\text{s}$)
- $q$ = Discharge per unit width ($\text{m}^3/\text{s/m}$)
- $f = 1.76 \sqrt{m_d}$ = Lacey silt factor ($m_d$ in mm)

#### Scour Multiplying Factors ($K_s$) for Maximum Anticipated Scour ($R_{\max} = K_s \cdot R$)
| River Location / Structure Element | Scour Factor ($K_s$) | Design Application |
| :--- | :--- | :--- |
| **Straight reach of river** | $1.25$ | Bank protection, straight revetments |
| **Moderate river bend** | $1.50$ | Outer curvature bank pitching |
| **Severe / acute river bend** | $1.75$ | Highly active meander bends |
| **Upstream transition / guide bund straight** | $1.25 - 1.50$ | Guide bund shank |
| **Guide bund curved head (upstream)** | $2.00 - 2.25$ | Nose of Bell's guide bund |
| **Guide bund curved tail (downstream)** | $1.50 - 1.75$ | Downstream return |
| **Spur / Groyne nose** | $2.00 - 2.25$ | Nose launch apron & armor |
| **Spur shank** | $1.25 - 1.50$ | Shank slope protection |
| **Bridge piers / barrage piers** | $2.00$ | Pier foundation cutoff depth |

---

### 1.2 Launching Apron Sizing & Stone Volume
When river scour undermines the bed at the toe of a pitched slope or spur nose, the horizontal stone apron launches down the slope (assumed at $2\text{ H}:1\text{ V}$) to protect the newly exposed bank.

1. **Scour Depth Below River Bed ($D$)**:
   $$D = R_{\max} - y_{\text{flow}} = K_s R - y_{\text{flow}}$$
   *(Where $y_{\text{flow}}$ is the water depth in the river at High Flood Level).*

2. **Apron Width in Horizontal Plane ($W_{\text{apron}}$)**:
   $$W_{\text{apron}} = 1.5 \cdot D$$

3. **Pitching Thickness on Slope ($t$)**:
   $$t = 0.06 \cdot Q^{1/3} \quad (\text{minimum } 0.60\text{ m to } 1.0\text{ m})$$

4. **Launched Apron Thickness on $2:1$ Slope ($T_{\text{launched}}$)**:
   $$T_{\text{launched}} \approx 1.25 \cdot t$$

5. **Apron Stone Volume per Running Meter of Bank ($V_{\text{apron}}$)**:
   Length along $2:1$ slope = $\sqrt{D^2 + (2D)^2} = \sqrt{5} D \approx 2.236 D$.
   $$V_{\text{apron}} = 2.236 \cdot D \cdot t \quad (\text{m}^3/\text{m})$$
   Horizontal apron placed thickness:
   $$T_{\text{apron}} = \frac{V_{\text{apron}}}{W_{\text{apron}}} = \frac{2.236 \cdot D \cdot t}{1.5 \cdot D} \approx 1.49 \cdot t$$

---

### 1.3 Guide Bunds (Bell's Bunds)
Used to confine meandering river width to the barrage/bridge clear waterway ($L_w$):
- **Waterway Length**: $L_w = 4.75 C_w \sqrt{Q}$ (Indus/Ganges alluvium, $C_w \approx 1.0 - 1.2$).
- **Upstream Bund Length**: $L_{\text{us}} = 1.0 \cdot L_w \text{ to } 1.25 \cdot L_w$.
- **Downstream Bund Length**: $L_{\text{ds}} = 0.20 \cdot L_w \text{ to } 0.25 \cdot L_w$.
- **Curved Upstream Head**:
  - Radius: $R_{\text{head}} = 0.40 \cdot L_w \text{ to } 0.50 \cdot L_w$.
  - Sweep Angle: $120^\circ \text{ to } 140^\circ$.
- **Curved Downstream Tail**:
  - Radius: $R_{\text{tail}} = 0.20 \cdot L_w \text{ to } 0.25 \cdot L_w$.
  - Sweep Angle: $45^\circ \text{ to } 60^\circ$.

---

### 1.4 Spurs (Groynes)
- **Types**:
  - **Repelling (Pointing upstream $60^\circ - 80^\circ$)**: Diverts the main current away from the protected bank. Creates a sediment stilling pool upstream. Recommended for deep river bends.
  - **Deflecting (Perpendicular $90^\circ$)**: Used for small local bank protection.
  - **Attracting (Pointing downstream $100^\circ - 120^\circ$)**: Pulls channel towards bank (special use).
- **Spur Spacing**:
  - Straight reach: $S_{\text{spur}} = 2.0 \text{ to } 2.5 \times L_{\text{spur}}$
  - Convex bank: $S_{\text{spur}} = 2.5 \text{ to } 3.0 \times L_{\text{spur}}$
  - Concave bank (eroding bend): $S_{\text{spur}} = 1.5 \text{ to } 2.0 \times L_{\text{spur}}$
- **Nose Slope**: $1:2$ or $1:3$ with full launching apron around the round nose ($180^\circ$ wrap).

---

### 1.5 Flood Levees / Bunds
- **Top Width**: Minimum $4.0\text{ m}$ (standard inspection path), $6.0\text{ m}$ for two-way vehicle access.
- **Freeboard**: Minimum $1.50\text{ m}$ to $1.80\text{ m}$ above 100-year recurrence High Flood Level (HFL).
- **Side Slopes**:
  - River side: $1:2$ to $1:3$ (stone pitched or turf revetted).
  - Countryside: $1:2$ to $1:2.5$ (with stability berm if embankment height $> 4.0\text{ m}$).
- **Cut-Off / Key Trench**: Depth $1.0\text{ m} - 2.0\text{ m}$ below ground level into impermeable strata; bottom width $2.0\text{ m}$.

---

## 2. Production River Engineering Python Calculator

```python
import math

def calculate_river_training_design(
    Q_peak: float,          # Peak flood discharge in m3/s
    HFL_depth: float,        # Water depth at HFL in m
    m_d: float = 0.35,       # Mean sediment diameter in mm
    river_condition: str = "spur_nose"  # 'straight', 'moderate_bend', 'severe_bend', 'spur_nose'
) -> dict:
    """
    Computes complete Lacey scour depth, slope pitching, and launching apron parameters.
    """
    # 1. Lacey silt factor
    f = 1.76 * math.sqrt(m_d)
    
    # 2. Regime scour depth R
    R = 0.473 * ((Q_peak / f) ** (1.0 / 3.0))
    
    # 3. Scour multiplying factor Ks
    ks_map = {
        "straight": 1.25,
        "moderate_bend": 1.50,
        "severe_bend": 1.75,
        "guide_bund_shank": 1.40,
        "spur_nose": 2.25,
        "guide_bund_head": 2.25
    }
    ks = ks_map.get(river_condition, 2.0)
    R_max = ks * R
    
    # 4. Scour depth below natural bed D
    D = max(0.0, R_max - HFL_depth)
    
    # 5. Slope pitching thickness t
    t = max(0.60, round(0.06 * (Q_peak ** (1.0 / 3.0)), 2))
    
    # 6. Launching apron dimensions
    W_apron = round(1.5 * D, 2)
    # Volume along 2:1 slope = sqrt(5) * D * t
    V_apron_per_m = round(math.sqrt(5.0) * D * t, 2)
    T_apron_placed = round(V_apron_per_m / W_apron if W_apron > 0 else 1.5 * t, 2)
    
    # Minimum stable boulder stone weight (Isbash formula estimate)
    # Approx mean velocity V = (Q * f^2 / 140)^(1/6) * factor
    V_channel = ((Q_peak * (f**2)) / 140.0) ** (1.0 / 6.0)
    V_local = V_channel * (1.3 if "nose" in river_condition else 1.1)
    # Boulder diameter D50 = V^2 / (2 * g * (Ss - 1) * 1.2), Ss = 2.65
    D50_stone = round((V_local ** 2) / (2.0 * 9.81 * (2.65 - 1.0) * 1.2), 3)
    boulder_mass_kg = round((4.0 / 3.0) * math.pi * ((D50_stone / 2.0) ** 3) * 2650.0, 1)
    
    return {
        "design_discharge_m3s": Q_peak,
        "silt_factor_f": round(f, 3),
        "regime_scour_R_m": round(R, 2),
        "condition": river_condition,
        "scour_factor_Ks": ks,
        "max_anticipated_scour_Rmax_m": round(R_max, 2),
        "scour_below_bed_D_m": round(D, 2),
        "slope_pitching_thickness_m": t,
        "launching_apron_width_m": W_apron,
        "launching_apron_thickness_m": T_apron_placed,
        "stone_volume_per_meter_run_m3": V_apron_per_m,
        "required_D50_stone_m": max(0.25, D50_stone),
        "boulder_mass_kg": max(25.0, boulder_mass_kg)
    }

if __name__ == "__main__":
    res = calculate_river_training_design(Q_peak=3500.0, HFL_depth=5.5, m_d=0.35, river_condition="spur_nose")
    print("=== RIVER TRAINING & LAUNCHING APRON DESIGN ===")
    for k, v in res.items():
        print(f"  {k}: {v}")
```

---

## 3. Engineering Report Checklist

When compiling a river training / flood protection design report:
1. **Hydrological Basis**: Document 25-yr, 50-yr, and 100-yr return period flood peaks.
2. **Scour Depth Calculations**: Tabulate $R$, $K_s$, and $R_{\max}$ for each station along bund/spur.
3. **Embankment Cross-Section Drawings**:
   - Crown width, freeboard ($1.8\text{ m}$), side slopes ($1:2$ riverside, $1:2.5$ countryside).
   - Inverted geotextile/crushed stone filter under slope pitching.
   - Horizontal launching apron laying plan showing layout before and after anticipated launch.
4. **Gabion / Riprap Specifications**: Specify minimum boulder specific gravity ($2.65$), wire gauge ($2.7\text{ mm}$ zinc-coated double twisted hexagonal mesh), and non-woven needle-punched geotextile ($250\text{ g/m}^2$).
