---
name: canal-and-drain-hydraulics
description: Hydraulics and design calculation engine for irrigation canals, alluvial channels, lined waterways, stormwater drains, and surface ditches. Includes Manning uniform flow solvers, Lacey regime theory, Kennedy CVR, lined channel optimization, and drainage ditch sizing.
---

# Canal and Drain Hydraulics Engineering Skill

This skill provides verified mathematical formulations, standard design criteria, and ready-to-run Python calculation engines for designing open channels, alluvial irrigation canals, lined waterways, and surface drainage systems.

---

## 1. Core Mathematical Formulations

### 1.1 Uniform Flow (Manning-Strickler)
For any open cross-section under uniform steady flow:
$$Q = \frac{1}{n} A R_h^{2/3} S_0^{1/2}$$
$$V = \frac{1}{n} R_h^{2/3} S_0^{1/2}$$

Where:
- $Q$ = Discharge ($\text{m}^3/\text{s}$ or cumecs)
- $V$ = Mean flow velocity ($\text{m/s}$)
- $n$ = Manning's roughness coefficient
- $A$ = Wetted flow area ($\text{m}^2$)
- $P$ = Wetted perimeter ($\text{m}$)
- $R_h = A / P$ = Hydraulic radius ($\text{m}$)
- $S_0$ = Longitudinal bed slope ($\text{m/m}$)

#### Manning's Roughness Values ($n$)
- Smooth concrete lined canal: $0.013 - 0.015$
- Precast concrete slabs / brick masonry lining: $0.016 - 0.018$
- Unlined earthen alluvial canals (clean bed, uniform): $0.020 - 0.0225$
- Natural earthen channels (irregular, light grass): $0.025 - 0.030$
- Vegetated drainage ditches / unmaintained channels: $0.035 - 0.050$
- Riprap-lined channel ($D_{50} = 200 - 300\text{ mm}$): $0.035 - 0.045$

---

### 1.2 Channel Geometry Formulas

#### Trapezoidal Section (Bed width $B$, Side slope $z\text{ H}:1\text{ V}$, Flow depth $y$)
- Area: $A = (B + z y) y$
- Wetted Perimeter: $P = B + 2 y \sqrt{1 + z^2}$
- Top Width: $T = B + 2 z y$
- Hydraulic Depth: $D_h = A / T$
- Hydraulic Radius: $R_h = A / P = \frac{(B + z y) y}{B + 2 y \sqrt{1 + z^2}}$

#### Best Hydraulic (Most Efficient) Trapezoidal Section
- Semi-hexagon ($z = 1/\sqrt{3} \approx 0.577$, $60^\circ$ side slopes)
- Hydraulic Radius: $R_h = y / 2$
- Bed width: $B = \frac{2}{\sqrt{3}} y \approx 1.155 y$
- Top width: $T = \frac{4}{\sqrt{3}} y \approx 2.309 y$

---

### 1.3 Lacey's Alluvial Regime Theory (Irrigation & Alluvial Canals)
Applicable to stable channels transporting silt in alluvium identical to the silt transported.

1. **Lacey's Silt Factor ($f$)**:
   $$f = 1.76 \sqrt{m_d}$$
   Where $m_d$ = Mean particle diameter in mm ($0.2\text{ mm}$ for fine silt, $0.32\text{ mm}$ for medium silt, $0.4\text{ mm}$ for coarse silt).

2. **Regime Velocity ($V$)**:
   $$V = \left(\frac{Q f^2}{140}\right)^{1/6} \quad (\text{m/s})$$

3. **Required Wetted Flow Area ($A$)**:
   $$A = \frac{Q}{V} \quad (\text{m}^2)$$

4. **Regime Wetted Perimeter ($P$)**:
   $$P = 4.75 \sqrt{Q} \quad (\text{m})$$

5. **Regime Hydraulic Mean Depth / Radius ($R$)**:
   $$R = \frac{5}{2} \left(\frac{V^2}{f}\right) = \frac{A}{P} \quad (\text{m})$$

6. **Regime Longitudinal Bed Slope ($S$)**:
   $$S = \frac{f^{5/3}}{3340 Q^{1/6}}$$

7. **Regime Scour Depth ($R_{\text{scour}}$)**:
   $$R_{\text{scour}} = 0.473 \left(\frac{Q}{f}\right)^{1/3}$$

---

### 1.4 Kennedy's Critical Velocity Ratio (CVR)
$$V_0 = 0.55 m y^{0.64} \quad (\text{m/s})$$
Where:
- $V_0$ = Critical non-silting, non-scouring velocity ($\text{m/s}$)
- $m$ = Critical Velocity Ratio ($m = V / V_0$). $m = 1.0$ for standard Punjab/Indus alluvium, $m = 1.1 - 1.2$ for coarse sandy silt, $m = 0.8 - 0.9$ for fine silt.
- $y$ = Water depth ($\text{m}$).

---

### 1.5 Surface Stormwater Drains & Ditches (Rational Method Peak Runoff)
$$Q_p = \frac{C \cdot I \cdot A_{\text{catch}}}{360}$$
Where:
- $Q_p$ = Peak discharge ($\text{m}^3/\text{s}$)
- $C$ = Runoff coefficient ($0.15 - 0.25$ pasture/cultivated, $0.40 - 0.60$ semi-urban, $0.70 - 0.90$ paved/asphalt)
- $I$ = Rainfall intensity for time of concentration ($\text{mm/hr}$)
- $A_{\text{catch}}$ = Catchment area in hectares ($\text{ha}$)

---

## 2. Design Standards & Safety Criteria

| Parameter | Unlined Alluvial Canal | Concrete Lined Canal | Roadside Drainage Ditch |
| :--- | :--- | :--- | :--- |
| **Max Permissible Velocity** | $0.60 - 0.90\text{ m/s}$ (non-scour) | $1.80 - 2.50\text{ m/s}$ | $1.20\text{ m/s}$ (grass) / $2.5\text{ m/s}$ (lined) |
| **Min Permissible Velocity** | $0.40 - 0.50\text{ m/s}$ (non-silt) | $0.60\text{ m/s}$ | $0.45\text{ m/s}$ |
| **Side Slope ($z\text{ H}:1\text{ V}$)** | $1.5:1$ (alluvial) to $2:1$ (light soil) | $1.25:1$ to $1.5:1$ | $1.5:1$ to $2:1$ |
| **Freeboard ($FB$)** | $0.50\text{ m}$ ($Q < 5$), $0.75\text{ m}$ ($Q < 20$), $1.0\text{ m}$ ($Q \ge 20$) | $0.30 - 0.60\text{ m}$ | $0.20 - 0.30\text{ m}$ |
| **Bed Width to Depth ($B/y$)** | $2.5 - 6.0$ depending on $Q$ | $1.5 - 3.0$ | $1.0 - 2.0$ |

---

## 3. Production Python Hydraulics Engine

Run this native Python script to size channels, verify Lacey regime parameters, and compute normal depth via Newton-Raphson.

```python
import math

def solve_manning_normal_depth(Q: float, n: float, S0: float, B: float, z: float, tol: float = 1e-6) -> float:
    """
    Solves normal depth (yn) for a trapezoidal open channel using Newton-Raphson iteration.
    Q: Discharge (m3/s)
    n: Manning's roughness
    S0: Bed slope (m/m)
    B: Bottom width (m)
    z: Side slope (z H : 1 V)
    """
    K_target = (Q * n) / math.sqrt(S0)
    y = max(0.1, (K_target / max(1.0, B)) ** 0.6)  # Initial seed
    
    for _ in range(100):
        A = (B + z * y) * y
        P = B + 2.0 * y * math.sqrt(1.0 + z * z)
        T = B + 2.0 * z * y
        
        # Section conveyance factor K(y) = A * R^(2/3) = A^(5/3) / P^(2/3)
        K = (A ** (5.0 / 3.0)) / (P ** (2.0 / 3.0))
        f = K - K_target
        
        if abs(f) < tol:
            return y
            
        # Derivative dK/dy
        dK_dy = (5.0 / 3.0) * (A ** (2.0 / 3.0)) * T / (P ** (2.0 / 3.0)) - \
                (2.0 / 3.0) * (A ** (5.0 / 3.0)) * (2.0 * math.sqrt(1.0 + z * z)) / (P ** (5.0 / 3.0))
        
        y_next = y - f / dK_dy
        if y_next <= 0:
            y_next = y / 2.0
        if abs(y_next - y) < tol:
            return y_next
        y = y_next
        
    return y

def lacey_regime_design(Q: float, m_d: float, side_slope: float = 0.5) -> dict:
    """
    Designs an alluvial canal according to Lacey's Regime Theory.
    Q: Discharge in cumecs (m3/s)
    m_d: Mean silt diameter in mm
    side_slope: z (H:V), standard 0.5 for semi-consolidated alluvium
    """
    f = 1.76 * math.sqrt(m_d)
    V = ((Q * (f ** 2)) / 140.0) ** (1.0 / 6.0)
    A = Q / V
    P = 4.75 * math.sqrt(Q)
    R = (5.0 / 2.0) * ((V ** 2) / f)
    S = (f ** (5.0 / 3.0)) / (3340.0 * (Q ** (1.0 / 6.0)))
    
    # Solve for bottom width B and depth y:
    # A = (B + z*y)*y  => B = A/y - z*y
    # P = B + 2*y*sqrt(1 + z^2) = A/y - z*y + 2*y*sqrt(1 + z^2)
    # y * (2*sqrt(1 + z^2) - z) - P + A/y = 0  => Quadratic in y:
    coeff_c1 = 2.0 * math.sqrt(1.0 + side_slope ** 2) - side_slope
    # coeff_c1 * y^2 - P * y + A = 0
    discriminant = (P ** 2) - 4.0 * coeff_c1 * A
    if discriminant < 0:
        raise ValueError("Lacey geometry constraint violation: P^2 < 4 * c1 * A")
    
    y = (P - math.sqrt(discriminant)) / (2.0 * coeff_c1)
    B = P - 2.0 * y * math.sqrt(1.0 + side_slope ** 2)
    R_scour = 0.473 * ((Q / f) ** (1.0 / 3.0))
    
    return {
        "silt_factor_f": round(f, 3),
        "regime_velocity_V_ms": round(V, 3),
        "flow_area_A_m2": round(A, 2),
        "wetted_perimeter_P_m": round(P, 2),
        "hydraulic_radius_R_m": round(R, 3),
        "regime_bed_slope_S": f"1 in {round(1.0 / S, 0):,.0f} ({S:.6f})",
        "bed_width_B_m": round(B, 2),
        "flow_depth_y_m": round(y, 2),
        "regime_scour_depth_R_m": round(R_scour, 2)
    }

if __name__ == "__main__":
    # Example: Canal for Q = 15 cumecs, medium silt md = 0.3 mm
    res = lacey_regime_design(Q=15.0, m_d=0.3)
    print("=== LACEY ALLUVIAL REGIME DESIGN ===")
    for k, v in res.items():
        print(f"  {k}: {v}")
```

---

## 4. Execution Workflow for Engineering Deliverables

1. **Hydraulic Profile Analysis**:
   - Compute normal depth $y_n$ and critical depth $y_c = (Q^2 / (g B^2))^{1/3}$.
   - Check Froude Number $Fr = V / \sqrt{g D_h}$. Maintain $Fr \le 0.75$ in unlined canals to prevent wave instability.
2. **Channel Freeboard Verification**:
   - $FB = \sqrt{0.5 \cdot y}$ (standard practice, minimum $0.30\text{ m}$).
3. **Cross-Sectional Drawing Production**:
   - Export geometry $(B, y, FB, z, \text{top width } T)$ to DXF via `ezdxf` or CSV coordinates for QGIS 3D terrain profile draping.
