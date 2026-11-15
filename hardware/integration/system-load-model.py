"""Extend the PWR v3 scenario CSV with explicit CTRL/HV load allocations.

Run in hardware/integration using Python 3.10+. All allocations below are
scenario assumptions unless linked to a manufacturer's specified condition.
"""
import csv
import math
from pathlib import Path

repo = Path(__file__).resolve().parents[2]
source = repo / 'hardware/pwr/RevA-draft-v3/power-model.csv'
out = Path(__file__).with_name('system-load-model.csv')

# These sums deliberately reproduce the existing model, not new measured data.
logic5 = {'HV5524_16MHz_max_W': 0.125,  # 25mA max at 5V, Microchip specified test
          'translator_assumed_W': 0.025,
          'other_5V_assumed_W': 0.350}
system = {'Pico_assumed_W': 0.300,
          'OLED_40mA_typ_W': 3.3 * 0.040,
          'RTC_and_margin_assumed_W': 0.068}
assert math.isclose(sum(logic5.values()), 0.5)
assert math.isclose(sum(system.values()), 0.5)

with source.open(newline='', encoding='utf-8-sig') as f:
    input_rows = list(csv.DictReader(f))
if len(input_rows) != 90:
    raise SystemExit(f'Expected 90 source rows, found {len(input_rows)}')

rows=[]
for i,r in enumerate(input_rows, 1):
    phv=float(r['P_hv_W']); p5=float(r['P_5V_W']); ps=float(r['P_SYS_W'])
    eh=float(r['eta_hv']); eb=float(r['eta_boost'])
    pmaxin=phv/eh
    idle=.02 if int(r['hv_mA'])==0 else 0
    audio=.8 if '+audio' in r['supply'] else 0
    p5_calc=pmaxin+sum(logic5.values())+idle
    ps_calc=p5_calc/eb+sum(system.values())+audio
    if abs(p5_calc-p5)>0.001 or abs(ps_calc-ps)>0.001:
        raise SystemExit(f'Power allocation mismatch in row {i}')
    vb=float(r['vbat_V']) if r['vbat_V'] else math.nan
    ib=float(r['I_BAT_A'])
    rpath_loss=ib*ib*.14 if math.isfinite(ib) and math.isfinite(vb) else math.nan
    rows.append({**r,
        'P_HV_input_assumed_W':round(pmaxin,3),
        'P_HV_stage_loss_assumed_W':round(pmaxin-phv,3),
        'P_HV5524_spec_max_condition_W':.125,
        'P_translator_assumed_W':.025,
        'P_other_5V_assumed_W':.350,
        'P_Pico_assumed_W':.300,
        'P_OLED_typ_condition_W':.132,
        'P_RTC_margin_assumed_W':.068,
        'P_audio_assumed_W':audio,
        'P_boost_total_loss_assumed_W':round(p5_calc*(1/eb-1),3),
        'P_BATFET_extrapolated_W':round(rpath_loss,3),
    })

with out.open('w', newline='', encoding='utf-8-sig') as f:
    w=csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader(); w.writerows(rows)
print(f'{len(rows)} scenario rows validated and written: {out}')
