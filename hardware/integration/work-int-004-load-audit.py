#!/usr/bin/env python3
"""WORK-INT-004 reproducible assumed-model audit; no physical qualification."""
import csv
import io
import json
import math
from pathlib import Path

HEADER = ["bleeder_id","usb_input_assumed_a","digits_assumed","neon_max_necessary_only","status","i_bleeder_ma","i_bus_budget_ma","two_digit_power_sys_w","source_class"]
def calculate():
    rows = []
    for bid, ib in [("P1_single330k",205/330000*1000),("P2_dual300k_Rmin285k",2*205/285000*1000)]:
        for ia in (0.450,0.498,0.500):
            budget = 5*ia*.675/205*1000
            for nd in (0,1,2):
                floor = math.floor((budget-3*nd-ib)/.5)
                feasible = floor >= 0
                rows.append([bid,f"{ia:.3f}",nd,min(12,floor) if feasible else "", "NECESSARY_ONLY" if feasible else "INFEASIBLE",f"{ib:.9f}",f"{budget:.9f}",f"{(6+ib)*.205/.675:.9f}","ASSUMED; NO MEASUREMENTS; overhead excluded"])
    logratio = math.log(220/60)
    rnmax = 5/(12e-6*logratio)/1.05
    summary = {
        "r_surv_max_ohm":rnmax*1.05,"r_nom_max_ohm":rnmax,
        "min_over_designs_of_max_dissipation_220_w":2*220**2/(.95*rnmax),
        "one_open_315k_c12uf_t_s":315000*12e-6*logratio,
        "single330k_plus5_c12uf_t_s":346500*12e-6*logratio,
        "dual285k_bleed_205_w":2*205**2/285000,
        "dual285k_bleed_220_w":2*220**2/285000,
        "energy_220_c12uf_j":.5*12e-6*220**2,
        "remaining_energy_60_c12uf_j":.5*12e-6*60**2,
        "lamp16ma_plus_dual_sys_w":(205*.016+2*205**2/285000)/.675,
        "hardware_qualified":False,
    }
    return rows, summary

def render():
    rows, summary = calculate()
    out = io.StringIO(newline="")
    writer = csv.writer(out,lineterminator="\n")
    writer.writerow(HEADER)
    writer.writerows(rows)
    return out.getvalue(), summary

if __name__ == "__main__":
    table, summary = render()
    output = Path(__file__).with_suffix(".csv")
    output.write_text(table,encoding="utf-8")
    print(json.dumps(summary,indent=2))
