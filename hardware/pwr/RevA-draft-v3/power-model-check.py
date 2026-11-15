"""Reproduce the committed CSV and check every row's published arithmetic.

Run from any directory: python power-model-check.py
Requires Python 3.10+ and no third-party packages.
"""

import csv
import math
import subprocess
import sys
import tempfile
from pathlib import Path

here = Path(__file__).resolve().parent
expected = here / "power-model.csv"
source = here / "power-model.py"

with tempfile.TemporaryDirectory() as td:
    temp = Path(td)
    (temp / source.name).write_bytes(source.read_bytes())
    subprocess.run([sys.executable, str(temp / source.name)], check=True,
                   stdout=subprocess.DEVNULL)
    actual = (temp / expected.name).read_bytes()
    if actual != expected.read_bytes():
        raise SystemExit("FAIL: regenerated CSV differs from committed CSV")

with expected.open(encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))
if len(rows) != 90:
    raise SystemExit(f"FAIL: expected 90 rows, got {len(rows)}")

def near(got, want, name, row_no, tol=0.0015):
    if not math.isclose(float(got), want, rel_tol=0, abs_tol=tol):
        raise SystemExit(f"FAIL: row {row_no} {name}: {got} vs {want:.6f}")

for n, r in enumerate(rows, 2):
    hv = int(r["hv_mA"])
    eh, eb = float(r["eta_hv"]), float(r["eta_boost"])
    phv = 205 * hv / 1000
    p5 = 0.5 + phv / eh + (0.02 if hv == 0 else 0)
    other = 1.3 if "+audio" in r["supply"] else 0.5
    psys = p5 / eb + other
    near(r["P_hv_W"], phv, "P_hv_W", n)
    near(r["P_5V_W"], p5, "P_5V_W", n)
    near(r["P_SYS_W"], psys, "P_SYS_W", n)
    near(r["I_5V_A"], p5 / 5, "I_5V_A", n)
    vsys = float(r["V_SYS_V"])
    ibat = float(r["I_BAT_A"])
    iusb = float(r["I_USB_A"])
    if math.isfinite(vsys):
        near(psys, vsys * (ibat + iusb), "SYS power balance", n, 0.005)
        if r["vbat_V"] and not ("USB" in r["supply"] and ibat == 0):
            vbat = float(r["vbat_V"])
            near(vsys, vbat - 0.14 * ibat, "BATFET path", n, 0.004)
        il = p5 / (eb * vsys)
        duty = max(0, 1 - eb * vsys / 5)
        ripple = vsys * duty / 0.7
        near(r["I_L_DC_A"], il, "I_L_DC_A", n)
        near(r["I_L_PEAK_A"], il + ripple / 2, "I_L_PEAK_A", n)
        near(r["I_L_VALLEY_A"], il - ripple / 2, "I_L_VALLEY_A", n)
    elif r["supply"] != "USB only":
        raise SystemExit(f"FAIL: unexpected nonfinite SYS at row {n}")

def select(case, hv, supply):
    return next(r for r in rows if r["efficiency_case"] == case
                and int(r["hv_mA"]) == hv and r["supply"] == supply)

near(select("working", 16, "battery+audio 3.3V")["I_BAT_A"], 2.51,
     "report working low battery audio", 0, 0.01)
near(select("stress", 16, "battery+audio 3.3V")["I_BAT_A"], 3.05,
     "report stress low battery audio", 0, 0.01)
near(select("working", 16, "USB only")["P_SYS_W"], 6.60,
     "report USB SYS", 0, 0.01)
print(f"PASS: byte-identical regeneration; {len(rows)} rows checked; report anchors checked")
