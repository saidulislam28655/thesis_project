# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
"""
Script to check current monitors and identify what's missing
"""
import os

def check_all_monitor_locations():
    """Check all possible monitor locations"""
    
    locations = [
        "outputs/three_fin_flow/monitors",
        "outputs/three_fin_thermal/monitors",
        "outputs/run_mode=eval/three_fin_flow/monitors",
        "outputs/run_mode=eval/three_fin_thermal/monitors",
    ]
    
    print("=" * 70)
    print("COMPLETE MONITOR FILE CHECK")
    print("=" * 70)
    
    for location in locations:
        print(f"\n📁 {location}")
        print("-" * 70)
        
        if os.path.exists(location):
            files = sorted(os.listdir(location))
            print(f"   ✓ Directory exists ({len(files)} items)")
            
            if files:
                for f in files:
                    if f.startswith('.'):
                        continue
                    filepath = os.path.join(location, f)
                    if os.path.isfile(filepath):
                        size = os.path.getsize(filepath)
                        print(f"     - {f} ({size} bytes)")
            else:
                print("     ⚠ Directory is empty")
        else:
            print("   ✗ Directory does not exist")
    
    print("\n" + "=" * 70)
    print("REQUIRED MONITOR FILES FOR DESIGN OPTIMIZATION:")
    print("=" * 70)
    print("""
For each design configuration, you need:
  Flow monitors:
    - back_pressure_<config>.csv
    - front_pressure_<config>.csv  (or inlet_pressure_<config>.csv)
  
  Thermal monitors:
    - peak_temp_<config>.csv

Example config string: _0.4_0.4_1.0_1.0_0.1_0.1
This represents the 6 parametrized dimensions.
""")
    
    print("\n" + "=" * 70)
    print("DIAGNOSIS:")
    print("=" * 70)
    
    # Check what we have
    flow_monitors = "outputs/three_fin_flow/monitors"
    thermal_monitors = "outputs/three_fin_thermal/monitors"
    
    has_flow = os.path.exists(flow_monitors)
    has_thermal = os.path.exists(thermal_monitors)
    
    if not has_flow and not has_thermal:
        print("""
❌ PROBLEM: No monitor files found anywhere

SOLUTION:
1. The models need to have PointwiseMonitor constraints that output:
   - inlet_pressure or front_pressure
   - (back_pressure is calculated from outlet)
   - peak_temp

2. You need to add these monitors to your code:
   See the updated three_fin_flow.py and three_fin_thermal.py below
   
3. Then train both models:
   python three_fin_flow.py
   python three_fin_thermal.py
""")
    elif has_flow and not has_thermal:
        print("""
⚠ PARTIAL: Flow monitors exist but thermal monitors missing

SOLUTION:
1. Check if three_fin_thermal.py has peak temperature monitor
2. Run: python three_fin_thermal.py
3. Check outputs/three_fin_thermal/monitors/ for peak_temp files
""")
        
        # Check flow monitors
        if os.path.exists(flow_monitors):
            files = [f for f in os.listdir(flow_monitors) if f.endswith('.csv')]
            has_back = any('back_pressure' in f for f in files)
            has_front = any('front_pressure' in f or 'inlet_pressure' in f for f in files)
            
            if not has_back:
                print("\n   ⚠ Missing: back_pressure monitors")
            if not has_front:
                print("   ⚠ Missing: front_pressure monitors")
                
            if has_front and not has_back:
                print("\n   💡 You have inlet_pressure. May need outlet_pressure too.")
    else:
        print("✓ Both monitor directories exist - checking contents...")


if __name__ == "__main__":
    check_all_monitor_locations()
