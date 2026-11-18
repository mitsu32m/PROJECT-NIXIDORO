# 2026-11-18 23:xx JST — PWR-002A / Issue #8: HV-enable load-step headroom at a candidate battery corner

**Role:** Chat A / deep-design. **Review:** PENDING REVIEW. **Claim:** provisional; NO FORMAL CLAIM. **Verdict:** CONDITIONAL for the explicitly assumed static algebra; BLOCKED for physical HV startup/continuous operation.

## Task contract and provenance
Repository `mitsu32m/PROJECT-NIXIDORO`, branch `codex/reva-integrated-prototype-review`. Start branch HEAD **UNKNOWN** (connected branch search returned branch name but not commit SHA; file API returned blob SHA, not commit SHA). Read `docs/ai-workflow.md`, `docs/verification/handoff.md`, `docs/verification/open-issues.md`, `docs/verification/decisions.md`, `docs/tech-tree.yaml`, `docs/tech-tree.md`, WORK-INT-002 and previous 20:00 PWR-002A report; reviewed issue #8 and current issue search. No Claim implementation demonstrated. Chat B owns sourcing #7; Chat C reviews; Work integrates shared indexes.

**Question:** For the previous 4.0V / 0.24Ω example, what is the *remaining load-step power budget* before the provisional 3.4V SYS HV-enable gate is violated? Unlike prior reports' resistance bounds, quantify additional load allowance and sensitivity at a fixed assumed battery terminal voltage. Exit: independently check formulas and demonstrate why an OCP pass is insufficient for startup/transients. Excludes component adoption, validated control thresholds, switching ripple, real battery/cell performance, firmware changes and any physical tests.

## Inputs and classification
- **ASSUMED:** fixed battery terminal voltage `Vb`, constant equivalent resistance `R=0.24Ω` including an illustrative `0.14Ω` BATFET extrapolation and `0.10Ω` external path; total constant-power SYS demand `P0=6.60084W`.
- **PROVISIONAL PROJECT POLICY:** `Vgate=3.4V` SYS threshold; not a TI guaranteed minimum, validated UVLO, or specified hysteresis.
- **ILLUSTRATIVE ONLY:** BQ25185 27°C OCP low-side proxy `Icap=2.5666A` from prior reports, not a guaranteed continuous operating current across temperature. TI source: https://www.ti.com/lit/ds/symlink/bq25185.pdf .
- **UNKNOWN:** protected-cell voltage under a real load step, resistance vs current/temperature/age, BATFET actual high-current R, TPS61023 current-limit and dynamic input behavior, SYS capacitance, converter transient efficiency, HV startup timing, real gate threshold and hysteresis.

## Derivation and result
For a battery-only resistive path, `Vsys=Vb-I*R` and `P=I*Vsys`. The lower-current root is `I=(Vb-sqrt(Vb²-4RP))/(2R)` and `Vsys=(Vb+sqrt(Vb²-4RP))/2`. In the considered `Vb<2*Vgate` region, requiring `Vsys>=Vgate` yields a maximum constant-power SYS load `Pgate=Vgate*(Vb-Vgate)/R`. A separate OCP requirement is `I<=Icap`. These are necessary conditions, not converter regulation guarantees.

At `Vb=4.0V, R=0.24Ω`: baseline `I=1.85715A`, `Vsys=3.55428V`; gate margin `154.28mV`. At the gate boundary `Pgate=8.500W`, `Igate=2.500A`. Therefore **only 1.89916W additional *steady* SYS demand** is allowed under this model before the 3.4V gate, even though the 27°C illustrative OCP screen is not yet exceeded. This does **not** mean a 1.9W startup pulse is safe: fast steps can trip UVLO or OCP before the steady equilibrium, and the battery terminal voltage is not actually fixed.

Sensitivity at the baseline `dVsys/dP=-R/sqrt(Vb²-4RP)=-0.07721V/W` (local small-signal *static* derivative, not a transient impedance). A naive 1W step therefore has approximately 77mV initial linearized static effect; use exact quadratic for larger changes.

| Fixed assumed Vb | Pgate at R=0.24Ω | Headroom above P0 |
|---:|---:|---:|
| 3.7V | 4.250W | -2.351W (baseline violates gate) |
| 3.8V | 5.667W | -0.934W (baseline violates gate) |
| 3.9V | 7.083W | +0.483W |
| 4.0V | 8.500W | +1.899W |
| 4.1V | 9.917W | +3.316W |

For this fixed-R scenario the battery terminal voltage must be at least `Vgate+R*P0/Vgate=3.86594V` for the assumed full load to pass the gate. This is **not** a recommended cell cutoff or firmware setting: actual loaded terminal voltage, UVLO hysteresis, ripple, dynamic droop, BATFET characteristics and thermal margins remain unknown. The previous 4.0V steady-state 'pass' must not be promoted to an HV startup approval.

## Independent reproduction
```python
from math import sqrt
P0=6.60084; R=0.24; gate=3.4
for vb in [3.7,3.8,3.9,4.0,4.1]:
    p_gate=gate*(vb-gate)/R
    print(vb, round(p_gate,6), round(p_gate-P0,6))
vb=4.0
disc=vb**2-4*R*P0
i=(vb-sqrt(disc))/(2*R)
vs=vb-R*i
assert abs(vs-3.55428388655)<1e-8
assert abs(gate*(vb-gate)/R-8.5)<1e-10
print('I,Vsys,margin,dVsys_dP',i,vs,vs-gate,-R/sqrt(disc))
```

## Review challenges and next action
1. Replace illustrative `R_BQ` with an evidence-backed high-current path bound or a measured LV-only model under a separately approved test plan; the 140mΩ value is not a guarantee at multiamp load.
2. Resolve actual selected protected 21700 and its voltage/current/temperature constraints with Chat B #7; do not count cell chemistry nominal voltage as loaded terminal voltage.
3. Determine SYS capacitance, TPS61023 startup input surge, regulator UVLO/current-limit and hysteresis from actual part revisions; estimate worst-case time-domain SYS minimum and charge/discharge state transitions, including USB insertion/removal.
4. Check signed battery current and thermal limits under USB supplement; static BAT-only screen is not valid for USB modes.
5. Chat C should verify the branch selection and static load-bound algebra, then Work should decide whether to incorporate this into the SYS/PWR contract. No shared indexes modified to avoid concurrent writes.

**CONDITIONAL:** mathematical necessary steady-state SYS gate/load bound under stated assumptions. **BLOCKED:** validated real 205V/16mA operation, startup, thermal and cell/charger limits. **PENDING REVIEW:** no formal adoption.

No purchase, PCB manufacture, main merge, HV energization, or important requirement change performed.
