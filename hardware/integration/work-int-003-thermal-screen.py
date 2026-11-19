"""WORK-INT-003: analytical thermal compatibility screen, not hardware approval.
Run: python hardware/integration/work-int-003-thermal-screen.py
BQ table entries: TI SLUSF65B Rev.B p8; TE nominal R/T: probe PDF 01/2022 p3.
Ideal B3435 and all source/path/load scenario values are ASSUMED.
"""
from math import exp, log, sqrt, isclose
import json
def t_at(v, i_uA):
    return 1/(1/298.15+log((v/(i_uA*1e-6))/10000)/3435)-273.15
entry={}
for name,lo,typ,hi in [("cold",.9575,1.0075,1.0575),("hot",.105,.115,.125)]:
    corners=[t_at(v,i) for v in (lo,hi) for i in (36.5,39.5)]
    entry[name]={"ideal_beta_typ_C":t_at(typ,38),
                 "electrical_only_min_C":min(corners),"electrical_only_max_C":max(corners)}
# Manufacturer table is nominal, not a guaranteed R/T tolerance envelope.
te_R={5:22060,10:17950,45:4920,50:4160}
points=[{"T_C":t,"TE_nominal_R_ohm":r,"VTS_at_typ38uA_V":r*38e-6,
         "inside_typ_entry_voltage_window":.115<r*38e-6<1.0075} for t,r in te_R.items()]
required=1.0075/.115
available=te_R[10]/te_R[45]
# Analytical proof for a>b>0, p>0:
# (p*a/(p+a))/(p*b/(p+b)) = (a/b)*(p+b)/(p+a) <= a/b.
# Adding nonnegative series resistance also decreases a ratio >=1.
# Therefore Rs+(Rp||R) cannot expand R10/R45 to the required threshold ratio.
source_v=4.; rt=.24; power=6.60084
ibat=(source_v-sqrt(source_v**2-4*rt*power))/(2*rt)
result={
    "classifications":"BQ specified voltage/current corners; TE nominal table; ideal beta and DC examples ASSUMED; NO MEASUREMENTS",
    "ideal_B3435_entry":entry,"TE_nominal_examples":points,
    "positive_ground_only_series_parallel_screen":{
        "nominal_required_R10_to_R45_ratio":required,
        "TE_nominal_available_ratio":available,
        "can_expand_to_required_ratio":available>=required,
        "scope":"Rs + (Rp || NTC), Rs>=0, Rp>0, fixed bias current. Not all compensation topologies."},
    "reviewed_static_DC_scenario":{"I_BAT_A":ibat,"SYS_V":source_v-rt*ibat,
         "BQ_assumed_path_loss_W":ibat**2*.14,"external_assumed_path_loss_W":ibat**2*.10},
    "warnings":["Entry corners exclude R/T tolerances, lag and wiring; not real cutoffs",
                "5C and 50C examples are outside candidate +10..45C yet inside nominal TS voltage window",
                "No NTC/cell/charger, resistor or thermal cutoff selected"]}
assert isclose(entry["cold"]["ideal_beta_typ_C"],1.735714,abs_tol=1e-5)
assert isclose(entry["hot"]["ideal_beta_typ_C"],59.511638,abs_tol=1e-5)
assert all(p["inside_typ_entry_voltage_window"] for p in points)
assert available<required
assert isclose(ibat,1.85715047,rel_tol=1e-7)
print(json.dumps(result,indent=2))
