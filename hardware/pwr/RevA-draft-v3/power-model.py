"""Scenario arithmetic, not a validated electrothermal or transient simulator.

The simple_current_pass field means USB demand <= 450 mA and, where relevant,
battery current < 2.56 A (illustrative lower BQ25185 OCP at 27 C). It does not
certify the cell, converter, thermal design, start-up, or high-voltage circuit.
"""

import csv
import math
from pathlib import Path

out = Path(__file__).with_name('power-model.csv')
rows = []

def balance(vbat, usb, p_sys, r_path=0.14, i_usb=0.45):
    if vbat is None:
        vsys = 4.5
        if p_sys > i_usb * vsys:
            return math.nan, 0.0, p_sys / vsys, False
        return vsys, 0.0, p_sys / vsys, True
    if not usb:
        disc = vbat*vbat - 4*r_path*p_sys
        if disc < 0:
            return math.nan, math.nan, math.nan, False
        ibat = (vbat - math.sqrt(disc))/(2*r_path)
        vsys = vbat-r_path*ibat
        return vsys, ibat, 0.0, ibat < 2.56
    if p_sys <= i_usb * 4.5:
        return 4.5, 0.0, p_sys/4.5, True
    # Vsys = Vbat - R*(Psys/Vsys-Iusb), assumes supplement already active.
    b = vbat + r_path*i_usb
    disc = b*b - 4*r_path*p_sys
    if disc < 0:
        return math.nan, math.nan, math.nan, False
    vsys = (b+math.sqrt(disc))/2
    ibat = max(0, p_sys/vsys-i_usb)
    return vsys, ibat, min(i_usb,p_sys/vsys), ibat < 2.56

for label, eh, eb in [('optimistic',0.80,0.90),('working',0.70,0.85),('stress',0.60,0.80)]:
    for hv_ma in (0,4,8,12,16):
        phv=205*hv_ma/1000
        p5=0.5+phv/eh+(0.02 if hv_ma==0 else 0)
        for supply,vbat,usb,other in [
            ('USB only',None,True,0.5),
            ('battery 4.0V',4.0,False,0.5),
            ('battery 3.3V',3.3,False,0.5),
            ('USB+battery 4.0V',4.0,True,0.5),
            ('USB+battery+audio 4.0V',4.0,True,1.3),
            ('battery+audio 3.3V',3.3,False,1.3),
        ]:
            psys=p5/eb+other
            vsys,ibat,iusb,ok=balance(vbat,usb,psys)
            i5=p5/5
            if math.isfinite(vsys):
                duty=max(0,1-eb*vsys/5)
                ripple=vsys*duty/0.7 # 0.7uH, 1MHz, result in A
                il_dc=p5/(eb*vsys)
                il_peak=il_dc+ripple/2
                il_valley=il_dc-ripple/2
            else:
                il_dc=il_peak=il_valley=math.nan
            rows.append({
                'efficiency_case':label,'eta_hv':eh,'eta_boost':eb,
                'hv_mA':hv_ma,'supply':supply,'vbat_V':vbat or '',
                'P_hv_W':round(phv,3),'P_5V_W':round(p5,3),
                'P_SYS_W':round(psys,3),'V_SYS_V':round(vsys,3),
                'I_BAT_A':round(ibat,3),'I_USB_A':round(iusb,3),
                'I_5V_A':round(i5,3),'I_L_DC_A':round(il_dc,3),
                'I_L_PEAK_A':round(il_peak,3),'I_L_VALLEY_A':round(il_valley,3),
                'simple_current_pass':ok,
            })

with out.open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
print(out)
for row in rows:
    if row['hv_mA']==16 and row['efficiency_case'] in ('working','stress'):
        print(row)
