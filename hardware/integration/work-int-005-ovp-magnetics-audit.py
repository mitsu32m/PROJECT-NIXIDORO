#!/usr/bin/env python3
"""Work005 assumed-model audit. Not device qualification or test measurements."""
import csv
import io
from pathlib import Path

def render():
    rows = []
    def emit(model, key, value, unit, evidence="ASSUMED"):
        rows.append([model,key,f"{value:.12g}",unit,evidence])
    q = 541.5
    for r in (.01,.001):
        a=.99*(1+(1-r)*q/(1+r))/(1+q)
        b=1.01*(1+(1+r)*q/(1-r))/(1+q)
        lo=214.13495/a
        hi=220/b
        tag=f"OVP_r{r}"
        emit(tag,"nominal_min_strict",lo,"V")
        emit(tag,"nominal_max_strict",hi,"V")
        emit(tag,"window_width",hi-lo,"V")
        emit(tag,"fixed217_trip_min",217*a,"V")
        emit(tag,"fixed217_trip_max",217*b,"V")
        if hi>lo:
            mid=(lo+hi)/2
            emit(tag,"normalized_midpoint",mid,"V")
            emit(tag,"trip_min_midpoint",mid*a,"V")
            emit(tag,"trip_max_midpoint",mid*b,"V")
            emit(tag,"headroom_cmin_1uf",.5e-6*(220**2-(mid*b)**2),"J")
    emit("bias","delta_hv_at_15na",15e-9*5.415e6,"V","ASSUMED: bound not guaranteed at VI=.4V")
    for v in (3,5):
        for f in (100e3,200e3):
            L=15e-6;n=15
            pk=1/f/(L*(1/v+n/205))
            p=.5*L*pk**2*f
            tag=f"CJ_V{v}_f{f:g}"
            emit(tag,"ipk_boundary",pk,"A")
            emit(tag,"p_magnetic",p,"W")
            emit(tag,"p_output_eta75",p*.75,"W")
            emit(tag,"output_margin_eta75",p*.75-3.28,"W")
            emit(tag,"ton",L*pk/v,"s")
            emit(tag,"toff",L*pk*n/205,"s")
    for v in (3,3.6,5):
        L=40e-6;pk=3.2;n=10
        f=1/(L*pk*(1/v+n/205))
        p=.5*L*pk**2*f
        tag=f"WE839_V{v}"
        emit(tag,"f_boundary",f,"Hz")
        emit(tag,"p_magnetic",p,"W")
        emit(tag,"eta_required",3.28/p,"ratio")
        emit(tag,"p_output_eta75",p*.75,"W")
    buf=io.StringIO(newline="")
    w=csv.writer(buf,lineterminator="\n")
    w.writerow(["model","quantity","value","unit","evidence_class"])
    w.writerows(rows)
    return buf.getvalue()

if __name__=="__main__":
    p=Path(__file__).with_suffix(".csv")
    p.write_text(render(),encoding="utf-8")
    print("Generated",p.name,"(all scenarios; no hardware qualification)")
