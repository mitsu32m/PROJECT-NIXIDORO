#!/usr/bin/env python3
"""Assumed energy/current screens for WORK-INT-007. No measurements or hardware approval."""
import csv
import io
from pathlib import Path

def render():
    rows=[]
    def add(model,key,value,unit):
        rows.append([model,key,f"{value:.12g}",unit,"ASSUMED; not hardware qualification"])
    head=.5e-6*(220**2-219.66744265459187**2)
    add("OVP_prior_normalized_example","headroom",head,"J")
    for stop in (3.0,0.0):
        for cu in (10,22,47):
            tag=f"LVcap_{cu}uF_5to{stop:g}V"
            energy=.5*cu*1e-6*(25-stop**2)
            add(tag,"available_energy",energy,"J")
            add(tag,"energy_over_prior_headroom",energy/head,"ratio")
        add(f"ideal_transfer_5to{stop:g}V","CL_if_all_other_tail_zero",2*head/(25-stop**2),"F")
    bleed=2*205**2/285000
    for name,p in (("whole_bus",3.28),("lamp_only_plus_dual_bleed",3.28+bleed)):
        for v in (3,5):
            i=p/(.75*v)
            tag=f"{name}_VIN{v}"
            add(tag,"p_hv",p,"W")
            add(tag,"i_average_proxy",i,"A")
            add(tag,"ripple_budget_to_1p5A",2*(1.5-i),"A_pp")
            add(tag,"eta_floor_at_zero_ripple",p/(1.5*v),"ratio")
    out=io.StringIO(newline="")
    w=csv.writer(out,lineterminator="\n")
    w.writerow(["model","quantity","value","unit","evidence_class"])
    w.writerows(rows)
    return out.getvalue()

if __name__=="__main__":
    p=Path(__file__).with_suffix(".csv")
    p.write_text(render(),encoding="utf-8")
    print("Generated",p.name,"; assumptions only")
