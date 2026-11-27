import numpy as np
import scipy.optimize as opt
import pandas as pd
import openpyxl
import docx
import matplotlib
import geopandas as gpd
import shapely
import ezdxf
import h5py
import whitebox

def calculate_pc1_financials(costs, benefits, discount_rate=0.12):
    years = np.arange(len(costs))
    net_cashflow = np.array(benefits) - np.array(costs)
    
    # NPV
    discount_factors = 1 / ((1 + discount_rate) ** years)
    pv_costs = np.sum(np.array(costs) * discount_factors)
    pv_benefits = np.sum(np.array(benefits) * discount_factors)
    npv = pv_benefits - pv_costs
    bcr = pv_benefits / pv_costs if pv_costs > 0 else np.nan
    
    # EIRR (solve npv(r) = 0)
    def npv_func(r):
        return np.sum(net_cashflow / ((1 + r) ** years))
    
    try:
        eirr = opt.brentq(npv_func, -0.9, 1.0)
    except Exception:
        eirr = np.nan
        
    return {
        'PV_Costs': pv_costs,
        'PV_Benefits': pv_benefits,
        'NPV': npv,
        'BCR': bcr,
        'EIRR': eirr
    }

# Example PC-1 10-year cashflow (PKR Millions)
costs = [150, 200, 10, 12, 12, 15, 15, 18, 18, 20]
benefits = [0, 20, 60, 80, 85, 90, 95, 100, 105, 110]

results = calculate_pc1_financials(costs, benefits, 0.12)
print("--- PC-1 Feasibility Results ---")
for k, v in results.items():
    if 'EIRR' in k:
        print(f"{k}: {v*100:.2f}%")
    else:
        print(f"{k}: {v:.2f}")

print("\nALL PYTHON MODULES IMPORTED AND VERIFIED SUCCESSFULLY!")
