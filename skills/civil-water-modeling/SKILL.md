---
name: civil-water-modeling
description: Hydrology and hydraulic modeling for municipal water distribution (EPANET / WNTR), stormwater drainage and retention (EPA-SWMM / PySWMM), 1D/2D river flood modeling (HEC-RAS), and civil earthwork cut-and-fill volume computation. Use when simulating pipe networks, sizing detention basins, modeling flood profiles, or computing earthwork quantities.
license: MIT
metadata:
  origin: General-Gemini
tools: Read, Write, Edit, Bash, Grep, Glob
---

# Civil & Water Resources Engineering Skill

Python-driven automation for EPA-SWMM, EPANET/WNTR, HEC-RAS 2D HDF5 plans, and site earthworks.

## When to Activate

- Designing or verifying stormwater drainage networks, detention ponds, and weir/orifice controls
- Simulating municipal water distribution networks, fire flow scenarios, and pipe burst resilience
- Post-processing HEC-RAS 1D water surface elevations and 2D flood depth/velocity maps
- Calculating cut/fill earthwork volumes between existing ground and proposed design surfaces

---

## 1. Stormwater Drainage Automation (`pyswmm` + `swmmio`)

### A. Run and Monitor SWMM Simulation Step-by-Step
```python
from pyswmm import Simulation, Nodes, Links

with Simulation("model.inp") as sim:
    outfall = Nodes(sim)["J_OUTFALL"]
    pump = Links(sim)["PUMP_1"]
    
    for step in sim:
        # Real-time control logic: throttle pump if outfall depth > 2.5m
        if outfall.depth > 2.5:
            pump.target_setting = 0.5
        else:
            pump.target_setting = 1.0
```

### B. Network Bottleneck Audit via `swmmio`
```python
import swmmio

model = swmmio.Model("model.inp")
# Conduits with max capacity utilization > 90%
conduits = model.conduits()
critical = conduits[conduits['max_flow'] / conduits['capacity'] > 0.9]
print("Critical pipes bottlenecking system:")
print(critical[['InletNode', 'OutletNode', 'capacity', 'max_flow']])
```

---

## 2. Water Distribution & Resilience (`wntr`)

```python
import wntr

# Load EPANET INP
wn = wntr.network.WaterNetworkModel("network.inp")

# Run Hydraulic Simulation
sim = wntr.sim.EpanetSimulator(wn)
results = sim.run_sim()

# Query Low-Pressure Nodes (< 20 psi or < 14 m head)
pressures = results.node['pressure']
min_pressures = pressures.min(axis=0)
low_pressure_nodes = min_pressures[min_pressures < 14.0]
print("Sub-standard pressure nodes under peak demand:")
print(low_pressure_nodes)

# Pipe Fire-Flow Demand Simulation
fire_node = wn.get_node('J-120')
fire_node.demand_timeseries_list[0].base_value += 0.063  # +1000 GPM (0.063 m3/s)
results_fire = sim.run_sim()
```

---

## 3. HEC-RAS 2D Flood Inundation Extraction (`h5py`)

Direct extraction from HEC-RAS 2D `.p##.hdf` plan output files without opening the HEC-RAS GUI:

```python
import h5py
import numpy as np

def extract_hecras_2d_max_depth(hdf_path: str):
    with h5py.File(hdf_path, 'r') as hdf:
        # Navigate to 2D flow area output
        area_name = list(hdf['Results/Unsteady/Output/Output Blocks/Base Output/Unsteady Time Series/2D Flow Areas'].keys())[0]
        base_path = f'Results/Unsteady/Output/Output Blocks/Base Output/Unsteady Time Series/2D Flow Areas/{area_name}'
        
        # Water Surface Elevation timeseries (cells x timesteps)
        wse = hdf[f'{base_path}/Water Surface'][:]
        
        # Cell minimum terrain surface elevation
        cell_elev = hdf[f'Geometry/2D Flow Areas/{area_name}/Cells Minimum Elevation'][:]
        
        # Maximum depth per cell across entire event
        max_wse = np.nanmax(wse, axis=0)
        max_depth = np.maximum(0.0, max_wse - cell_elev)
        
        return {
            'area_name': area_name,
            'max_depth_m': float(np.nanmax(max_depth)),
            'flooded_cells_count': int(np.sum(max_depth > 0.1))
        }
```

---

## 4. Earthwork Cut/Fill Volume Computation

Average End Area formula across survey station cross-sections:

$$V = \sum_{i=1}^{n-1} \frac{A_i + A_{i+1}}{2} \times L_i$$

```python
import pandas as pd

def calculate_earthwork(stations_csv: str):
    """
    CSV Format:
    Station, CutArea_m2, FillArea_m2
    0, 12.5, 0.0
    25, 18.0, 1.2
    50, 10.4, 4.5
    """
    df = pd.read_csv(stations_csv)
    df['Length'] = df['Station'].diff().fillna(0)
    
    cut_vols = []
    fill_vols = []
    
    for i in range(1, len(df)):
        l = df.loc[i, 'Length']
        cut_vol = ((df.loc[i-1, 'CutArea_m2'] + df.loc[i, 'CutArea_m2']) / 2.0) * l
        fill_vol = ((df.loc[i-1, 'FillArea_m2'] + df.loc[i, 'FillArea_m2']) / 2.0) * l
        cut_vols.append(cut_vol)
        fill_vols.append(fill_vol)
        
    total_cut = sum(cut_vols)
    total_fill = sum(fill_vols)
    net_earthwork = total_cut - total_fill  # positive = export, negative = borrow
    
    return {
        'total_cut_m3': round(total_cut, 2),
        'total_fill_m3': round(total_fill, 2),
        'net_balance_m3': round(net_earthwork, 2),
        'balance_status': 'Surplus / Export' if net_earthwork > 0 else 'Deficit / Borrow Required'
    }
```

---

## 5. Local Repositories & Toolchains

- **PySWMM Source & Tests**: `C:\tools\qgis-civil\pyswmm\`
- **EPA WNTR Source & Tests**: `C:\tools\qgis-civil\wntr\`
- **Python Virtualenv**: `C:\Users\Imran\Downloads\General-Gemini\.venv\`
