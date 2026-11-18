"""WORK-INT-002 sensitivity checks; no hardware/component qualification.
Run: python hardware/integration/work-int-002-energy-screen.py
All C, trip error, tail energy, startup time, resistor and efficiencies are ASSUMED.
"""
import json, math

v=205.0
limit=220.0
vnormal=1.28*(1+163*1.01/.99)
epsilon=.01
trip=217.
tail=.5*44e-6*3.2**2
den=limit**2-(trip*(1+epsilon))**2
rows=[]
for c in [1e-6,4.7e-6,10e-6]:
    energy=.5*c*v*v
    rows.append(dict(C_effective_assumed_uF=c*1e6,
        stored_mJ=energy*1e3,
        posttrip_headroom_mJ=.5*c*den*1e3,
        linear_ramp_end_cap_W=c*v*v/.5,
        average_full_load_SYS_W=((3.28+energy/.5)/.7+.5)/.85+.5,
        discharge_220_to_60_s_at_Rmax_1Mohm=1e6*c*math.log(220/60)))
# 60V and 1Mohm are illustrations, not selected touch voltage or bleed resistor.
# Real startup constraint uses Cmax; OVP headroom uses Cmin.
c_ovp_lower=2*tail/den
c_start_upper=2*.10*.5/v**2
# Budget .10W HV-output charging headroom over .5s is an ASSUMED integral budget.
baseline=(3.28/.7+.5)/.85+.5
direct=3.28/.7+.5/.85+.5
# Challenge B 05:03: combine its ideal ratio with its lossy primary-current proxy.
vin=3.; duty=.65; d2=.25; eta=.7; iout=.016
ratio=v*d2/(vin*duty)
ipk=2*(v*iout/eta)/(vin*duty)
implied_secondary=d2*ipk/(2*ratio)
result=dict(
    inputs="ASSUMED scenario values except manufacturer cited voltage/table limits; NO MEASUREMENTS",
    normal_static_high_V=vnormal,
    nominal_static_trip_open_interval_V=[vnormal/(1-epsilon),limit/(1+epsilon)],
    one_hypothetical_pulse_mJ=tail*1e3,
    Cmin_strict_lower_for_one_pulse_uF=c_ovp_lower*1e6,
    Cmax_startup_energy_upper_scenario_uF=c_start_upper*1e6,
    SYS_baseline_W=baseline,SYS_direct_70pct_W=direct,SYS_saving_W=baseline-direct,
    B0503_implied_secondary_mA=implied_secondary*1e3,
    B0503_primary_peak_proxy_A=ipk,
    rows=rows)
assert math.isclose(vnormal,214.13494949494952)
assert math.isclose(c_ovp_lower*1e6,1.236066602,rel_tol=1e-8)
assert math.isclose(implied_secondary,iout/eta)
assert math.isclose(baseline,6.600840336134454)
print(json.dumps(result,indent=2,ensure_ascii=False))
