"""HEC-RAS AI Bridge MCP Server.

Provides contract-bound tools for AI agents to inspect projects, run 1D/2D hydraulic
simulations, parse cross-sections, and extract water surface elevations from HEC-RAS 7.0.
"""

import os
import sys
import glob
from typing import Dict, Any, List, Optional
import h5py
from mcp.server.fastmcp import FastMCP
import ras_commander

mcp = FastMCP("hecras_agent_mcp")

HECRAS_EXE_DIR = r"C:\Program Files (x86)\HEC\HEC-RAS\7.0"


@mcp.tool()
def hecras_version_info() -> Dict[str, Any]:
    """Get the installed HEC-RAS executable paths, version info, and agent automation status."""
    ras_exe = os.path.join(HECRAS_EXE_DIR, "Ras.exe")
    mapper_exe = os.path.join(HECRAS_EXE_DIR, "RasMapper.exe")
    process_exe = os.path.join(HECRAS_EXE_DIR, "RasProcess.exe")
    
    detected_exe = None
    try:
        detected_exe = ras_commander.get_ras_exe("7.0")
    except Exception:
        pass

    return {
        "installed": os.path.exists(ras_exe),
        "version": "7.0",
        "ras_exe": ras_exe if os.path.exists(ras_exe) else None,
        "mapper_exe": mapper_exe if os.path.exists(mapper_exe) else None,
        "process_exe": process_exe if os.path.exists(process_exe) else None,
        "ras_commander_bound": detected_exe is not None,
        "ras_commander_version": getattr(ras_commander, "__version__", "unknown")
    }


@mcp.tool()
def hecras_inspect_project(project_path: str) -> Dict[str, Any]:
    """Inspect a HEC-RAS project (.prj file) to list title, units, plans, geometries, and flow files.
    
    Args:
        project_path: Absolute path to the .prj file.
    """
    if not os.path.exists(project_path):
        return {"error": f"Project file not found: {project_path}"}

    project_dir = os.path.dirname(os.path.abspath(project_path))
    project_base = os.path.splitext(os.path.basename(project_path))[0]

    details: Dict[str, Any] = {
        "project_file": project_path,
        "project_directory": project_dir,
        "project_title": "",
        "units": "English (Default)",
        "current_plan": "",
        "plans": [],
        "geometries": [],
        "steady_flows": [],
        "unsteady_flows": [],
    }

    with open(project_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line_str = line.strip()
            if line_str.startswith("Proj Title="):
                details["project_title"] = line_str.split("=", 1)[1].strip()
            elif line_str.startswith("Current Plan="):
                details["current_plan"] = line_str.split("=", 1)[1].strip()
            elif line_str.startswith("SI Units"):
                details["units"] = "SI (Metric)"
            elif line_str.startswith("English Units"):
                details["units"] = "English (US Customary)"
            elif line_str.startswith("Plan File="):
                details["plans"].append(line_str.split("=", 1)[1].strip())
            elif line_str.startswith("Geom File="):
                details["geometries"].append(line_str.split("=", 1)[1].strip())
            elif line_str.startswith("Flow File="):
                details["steady_flows"].append(line_str.split("=", 1)[1].strip())
            elif line_str.startswith("Unsteady File="):
                details["unsteady_flows"].append(line_str.split("=", 1)[1].strip())

    # Detect any result HDF files
    hdf_files = glob.glob(os.path.join(project_dir, f"{project_base}*.hdf"))
    details["hdf_result_files"] = [os.path.basename(h) for h in hdf_files]

    return details


@mcp.tool()
def hecras_extract_wsel(hdf_path: str, max_cross_sections: int = 50) -> Dict[str, Any]:
    """Extract Water Surface Elevations (WSEL), maximum depths, and velocities from a HEC-RAS plan HDF file (.pXX.hdf).
    
    Args:
        hdf_path: Absolute path to the plan output HDF file (e.g. MyProject.p01.hdf).
        max_cross_sections: Maximum number of cross sections to return (default 50).
    """
    if not os.path.exists(hdf_path):
        return {"error": f"HDF file not found at: {hdf_path}"}

    try:
        results: Dict[str, Any] = {
            "hdf_file": hdf_path,
            "profiles": [],
            "cross_sections_count": 0,
            "data": []
        }

        with h5py.File(hdf_path, "r") as hdf:
            # Check 1D Steady Results
            steady_path = "Results/Steady/Output/Geometry Info/Cross Section Info"
            if steady_path in hdf:
                xs_info = hdf[steady_path][:]
                results["cross_sections_count"] = len(xs_info)

            # Check for Profile Names
            for p_path in [
                "Results/Steady/Output/Profile Names",
                "Results/Unsteady/Output/Profile Names"
            ]:
                if p_path in hdf:
                    results["profiles"] = [p.decode("utf-8") if isinstance(p, bytes) else str(p) for p in hdf[p_path][:]]
                    break

            # 1D Water Surface Elevations
            for wsel_path in [
                "Results/Steady/Output/Output Blocks/Base Output/Steady Profiles/Cross Sections/Water Surface",
                "Results/Unsteady/Output/Output Blocks/Base Output/Unsteady Time Series/Cross Sections/Water Surface"
            ]:
                if wsel_path in hdf:
                    wsel_data = hdf[wsel_path][:]
                    rows = []
                    limit = min(len(wsel_data), max_cross_sections)
                    for i in range(limit):
                        rows.append({
                            "index": i,
                            "wsel_values": [float(val) for val in wsel_data[i][:5]]
                        })
                    results["data"] = rows
                    results["status"] = "Success (1D WSEL Extracted)"
                    return results

            # 2D Flow Areas Summary
            if "Results/Unsteady/Output/Output Blocks/Base Output/Summary Output/2D Flow Areas" in hdf:
                two_d_summary = hdf["Results/Unsteady/Output/Output Blocks/Base Output/Summary Output/2D Flow Areas"]
                results["status"] = "Success (2D Flow Areas Detected)"
                results["two_d_areas"] = list(two_d_summary.keys())
                return results

            results["status"] = "HDF opened, but no standard output blocks found."
            return results

    except Exception as e:
        return {"error": f"Failed reading HDF5 results: {str(e)}"}


@mcp.tool()
def hecras_compute_simulation(project_path: str, plan_suffix: str = "01") -> Dict[str, Any]:
    """Trigger a HEC-RAS 7.0 simulation computation for a specified plan using ras-commander.
    
    Args:
        project_path: Absolute path to the .prj project file.
        plan_suffix: Plan number/suffix (e.g. '01', '02', 'p01').
    """
    if not os.path.exists(project_path):
        return {"error": f"Project file not found: {project_path}"}

    project_dir = os.path.dirname(os.path.abspath(project_path))

    try:
        # Initialize ras project via ras-commander
        ras_proj = ras_commander.init_ras_project(project_dir, ras_version="7.0")
        
        # Clean plan string (e.g. 'p01' -> '01')
        clean_plan = plan_suffix.lower().replace("p", "")
        
        # Compute plan
        result = ras_commander.RasCmdr.compute_plan(
            clean_plan,
            ras_object=ras_proj,
            verify=True
        )

        return {
            "status": "Computed via ras-commander",
            "success": getattr(result, "success", True),
            "plan": clean_plan,
            "project": project_path,
            "result_summary": str(result)
        }
    except Exception as e:
        return {
            "status": "Error",
            "error": f"Computation failed: {str(e)}"
        }


if __name__ == "__main__":
    mcp.run()
