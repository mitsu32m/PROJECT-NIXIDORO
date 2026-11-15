"""Screen Rev.A HV architecture power, without qualifying a power stage.

Values of conversion efficiency are assumptions, not guaranteed specifications.
Run with Python 3.10+; output CSV is written beside this script.
"""
import csv
from itertools import product
from pathlib import Path

V5 = 5.0
LOAD_MA = (0, 4, 8, 12, 16)
VHV = (200, 205)
ETA_HV = (0.60, 0.70, 0.80)
ETA_5V = (0.80, 0.85, 0.90)

rows = []
for v_hv, i_ma, eta_hv, eta_5v in product(VHV, LOAD_MA, ETA_HV, ETA_5V):
    p_out = v_hv * i_ma / 1000
    p_hv_in = p_out / eta_hv
    p_hv_loss = p_hv_in - p_out
    p_sys = p_hv_in / eta_5v
    rows.append({
        'V_HV_V': v_hv,
        'I_HV_mA': i_ma,
        'eta_HV_assumed': eta_hv,
        'eta_5V_assumed': eta_5v,
        'P_HV_out_W': round(p_out, 6),
        'P_HV_5V_input_W': round(p_hv_in, 6),
        'I_HV_5V_input_A': round(p_hv_in / V5, 6),
        'P_HV_loss_W': round(p_hv_loss, 6),
        'P_SYS_for_HV_W': round(p_sys, 6),
        'P_5V_boost_loss_W': round(p_sys - p_hv_in, 6),
    })

assert len(rows) == 90
assert round(205 * 0.016 / .7 / 5, 3) == .937
assert round(205 * 0.016 / .7 / .85, 3) == 5.513
assert round((1 - 5 / 205) * 100, 2) == 97.56

out = Path(__file__).with_suffix('.csv')
with out.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
print(f'{len(rows)} assumed scenarios written to {out}')
