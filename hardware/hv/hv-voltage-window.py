"""Reproduce the MAX668 feedback and HV5524 voltage-window screen.

No OVP component is selected here. Static values omit start/stop overshoot,
feedback input current, resistor voltage coefficients and dynamic failures.
"""
import csv
from pathlib import Path

TARGET_NOMINAL_V = 205.0
FB_NOMINAL_V = 1.25
RATIO_NOMINAL = TARGET_NOMINAL_V / FB_NOMINAL_V - 1
HV5524_RECOMMENDED_MAX_V = 220.0

rows = []
for spec, fb_min, fb_max in (
    ('0_to_85C', 1.225, 1.275),
    ('minus40_to_85C', 1.22, 1.28),
):
    for tolerance in (0.0, 0.001, 0.01):
        ratio_min = RATIO_NOMINAL * (1 - tolerance) / (1 + tolerance)
        ratio_max = RATIO_NOMINAL * (1 + tolerance) / (1 - tolerance)
        v_min = fb_min * (1 + ratio_min)
        v_max = fb_max * (1 + ratio_max)
        rows.append({
            'temperature_spec': spec,
            'FB_min_V': fb_min, 'FB_max_V': fb_max,
            'each_resistor_tolerance': tolerance,
            'Rtop_over_Rbottom_nominal': round(RATIO_NOMINAL, 6),
            'Vout_static_min_V': round(v_min, 6),
            'Vout_static_max_V': round(v_max, 6),
            'min_to_200V_margin_V': round(v_min - 200, 6),
            'max_to_205V_margin_V': round(205 - v_max, 6),
            'max_to_220V_OVP_window_V': round(HV5524_RECOMMENDED_MAX_V - v_max, 6),
        })

out = Path(__file__).with_suffix('.csv')
with out.open('w', newline='', encoding='utf-8') as stream:
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)

assert len(rows) == 6
assert all(r['max_to_205V_margin_V'] < 0 for r in rows)
assert all(r['Vout_static_max_V'] - r['Vout_static_min_V'] > 5 for r in rows)
for row in rows:
    print(row['temperature_spec'], row['each_resistor_tolerance'],
          row['Vout_static_min_V'], row['Vout_static_max_V'])
