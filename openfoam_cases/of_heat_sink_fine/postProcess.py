#!/usr/bin/env python3
import glob, csv

def last_row(pattern):
    files = sorted(glob.glob(pattern))
    if not files:
        return None
    rows = []
    with open(files[-1]) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith(chr(35)):
                continue
            rows.append([float(x) for x in line.split()])
    return rows[-1] if rows else None

inlet_row  = last_row("postProcessing/patchAverage(name=inlet,p)/*/surfaceFieldValue.dat")
outlet_row = last_row("postProcessing/patchAverage(name=outlet,p)/*/surfaceFieldValue.dat")
pt_row     = last_row("postProcessing/peakTemperature/*/volFieldValue.dat")

p_in  = inlet_row[-1]  if inlet_row  else float("nan")
p_out = outlet_row[-1] if outlet_row else float("nan")
dp    = p_in - p_out
Tk    = pt_row[-1] if pt_row else float("nan")
Tc    = Tk - 273.15

print("====================================================")
print(f"  Inlet  p-bar (kinematic)   : {p_in:.6f}")
print(f"  Outlet p-bar (kinematic)   : {p_out:.6f}")
print(f"  Pressure drop  (Pa, rho=1) : {dp:.4f}")
print(f"  Peak temperature      (K)  : {Tk:.3f}")
print(f"  Peak temperature      (C)  : {Tc:.2f}")
print("====================================================")

with open("openfoam_result.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["pressure_drop_Pa", "peak_T_K", "peak_T_C", "h_mid", "h_side", "l_mid", "l_side", "t"])
    w.writerow([f"{dp:.4f}", f"{Tk:.3f}", f"{Tc:.2f}", 0.4, 0.3, 0.75, 1.0, 0.1])
print("  Saved -> openfoam_result.csv")
