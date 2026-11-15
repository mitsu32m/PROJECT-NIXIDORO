"""First-order CCM screen of three manufacturer-documented transformers.

This is not a flyback design or a transformer rating calculation. Duty is ideal;
efficiency is assumed; copper resistance is specified at room temperature. No thermal, control,
startup, core, snubber, or certification conclusion can be drawn from the CSV.
"""
import csv
from itertools import product
from pathlib import Path

PARTS = (
    {'part': 'Wuerth 750315839', 'n_sec_pri': 10.0,
     'rpri_max_ohm': 0.085 * 1.10, 'leak_max_h': 0.5e-6,
     'current_reference_a': 3.2, 'current_reference_kind': 'Isat_typ_20pct_L_drop'},
    {'part': 'Sumida 13324-T086', 'n_sec_pri': 5.0,
     'rpri_max_ohm': 0.130, 'leak_max_h': 1.2e-6,
     'current_reference_a': 3.0, 'current_reference_kind': 'rated_DC_15pct_L_drop'},
    {'part': 'Sumida 13324-T087', 'n_sec_pri': 10.0,
     'rpri_max_ohm': 0.130, 'leak_max_h': 1.2e-6,
     'current_reference_a': 3.0, 'current_reference_kind': 'rated_DC_15pct_L_drop'},
)
LT8304_CURRENT_LIMIT_MIN_A = 2.0

rows = []
for part, vin, vout, load_ma, efficiency, frequency_khz, lpri_uh in product(
    PARTS, (4.75, 5.0, 5.25), (200, 205), (12, 16),
    (0.60, 0.70, 0.80), (100, 200), (36, 44)):
    frequency_hz = frequency_khz * 1000
    lpri_h = lpri_uh * 1e-6
    duty = vout / (vout + part['n_sec_pri'] * vin)
    pout = vout * load_ma / 1000
    pin = pout / efficiency
    iin = pin / vin
    ion_avg = iin / duty
    ripple = vin * duty / (lpri_h * frequency_hz)
    ipeak = ion_avg + ripple / 2
    ivalley = ion_avg - ripple / 2
    ipri_rms_sq = duty * (ion_avg**2 + ripple**2 / 12)
    rows.append({
        'candidate': part['part'],
        'Vin_V': vin, 'Vout_V': vout, 'Iout_mA': load_ma,
        'eta_assumed': efficiency, 'f_kHz': frequency_khz,
        'Lpri_uH': lpri_uh, 'D_ideal': round(duty, 6),
        'Pin_assumed_W': round(pin, 6), 'Iin_avg_A': round(iin, 6),
        'Ipri_peak_CCM_A': round(ipeak, 6),
        'Ipri_valley_CCM_A': round(ivalley, 6),
        'MAX668_D87pct_min_spec_margin': round(0.87 - duty, 6),
        'LT8304_2A_limit_margin_A': round(LT8304_CURRENT_LIMIT_MIN_A - ipeak, 6),
        'current_reference_kind': part['current_reference_kind'],
        'current_reference_margin_A': round(part['current_reference_a'] - ipeak, 6),
        'Ppri_copper_room_temp_maxR_W': round(ipri_rms_sq * part['rpri_max_ohm'], 6),
        'P_leak_energy_all_dissipated_upper_W': round(
            0.5 * part['leak_max_h'] * ipeak**2 * frequency_hz, 6),
    })

assert len(rows) == 432
assert all(r['Ipri_valley_CCM_A'] > 0 for r in rows)
assert all(r['current_reference_margin_A'] > 0 for r in rows)
out = Path(__file__).with_suffix('.csv')
with out.open('w', newline='', encoding='utf-8') as stream:
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
for part in PARTS:
    cases = [row for row in rows if row['candidate'] == part['part']]
    worst = max(cases, key=lambda row: row['Ipri_peak_CCM_A'])
    print(f"{part['part']}: {len(cases)} rows; worst modeled peak {worst['Ipri_peak_CCM_A']:.6f} A")
