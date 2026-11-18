# 2026-11-19 04:00 JST — PWR-002A / Issue #8: SYS transient capacitor charge deficit

**Role:** Chat A (deep-design). **Claim:** provisional, NO FORMAL CLAIM. **Review:** PENDING REVIEW. **Verdict:** CONDITIONAL (charge-conservation necessary bound); BLOCKED (real TPS61023/BQ25185 startup and hardware qualification).

## Task contract / evidence
Branch: `codex/reva-integrated-prototype-review`. Start HEAD SHA: **UNKNOWN** (GitHub file reads returned blob SHA; no authoritative exact branch commit was obtained). Read the SOP, handoff, open issues, decisions, tech-tree YAML and Mermaid, WORK-INT-002, the previous 2026-11-18-2340 PWR-002A report, and open Issue #8. Claim mechanism not demonstrated; do not claim. Chat B owns part sourcing #7, Chat C review, Work shared-index integration.

**Question:** How much effective SYS capacitance is required to ride through a specified *net* current deficit before the assumed 3.4V HV-enable threshold is crossed, starting at the previous 3.55428V steady-state point? **Exit:** reproducible charge balance and sensitivity table; distinguish a necessary charge bound from verified startup behavior. No component adoption, KiCad changes or tests.

## Model and independently calculated results
All inputs in this section are **ASSUMED**, not TI-guaranteed: previous example V_SYS,0=3.55428V (V_BAT=4.0V, equivalent path R=0.24ohm, P_SYS=6.60084W), V_gate=3.4V, so voltage headroom DeltaV=0.15428V. `I_deficit(t)=I_load(t)-I_source(t)` is the **net** current drawn from the local SYS capacitor after the actual source response, not the HV converter input current and not the battery current.

Charge conservation (neglecting ESR/ESL/leakage) gives `C_eff >= integral(max(I_deficit,0)dt)/DeltaV` for a nonnegative deficit. For a constant deficit `C_eff >= I_deficit*t/DeltaV`. If capacitor ESR is present, `DeltaV_available = 0.15428V - I_step*ESR - L*di/dt` (latter term is an approximate local inductive voltage contribution, topology dependent); negative available headroom means no finite capacitance can fix the instantaneous dip in this simplified model.

| Assumed net current deficit | Duration | Required effective SYS capacitance (ideal minimum) |
|---:|---:|---:|
| 0.10 A | 0.10 ms | 64.8 uF |
| 0.50 A | 0.10 ms | 324.1 uF |
| 0.50 A | 1.00 ms | 3240.9 uF |
| 1.00 A | 1.00 ms | 6481.7 uF |
| 0.50 A | 5.00 ms | 16204.3 uF |

For 0.5A instantaneous capacitor-current step and 50mohm **ASSUMED** ESR, instantaneous ESR drop is 25mV, leaving 129.28mV for charge depletion: 0.5A for 1ms then needs >3867uF effective capacitance even before ESL and derating. At 0.5A and 0.31ohm ESR, the ESR drop alone exceeds 154.28mV, regardless of capacitance. All values are illustrative **necessary** conditions; no actual load step, source response or capacitor is specified.

## Important boundary correction
The prior 1.899W **steady-state** load headroom does not imply any permissible pulse duration or input surge. If the converter requests additional power while SYS voltage falls, its input current can increase; the net capacitor deficit is therefore dynamic and requires time-domain source and converter behavior. Conversely, if BQ/battery source follows the load instantaneously, deficit can be much smaller than the load step. No generic `C=I*t/DeltaV` table should be used to choose a part without a bounded `I_deficit(t)`.

The 3.4V gate itself is only a provisional project screen; a real TPS61023 input UVLO, BQ25185 BATFET path and selected cell/protector may set a different limiting threshold. Effective ceramic capacitance at DC bias/temperature/aging, ESR/ESL, PCB path impedance, comparator/MCU sampling, hysteresis, and brownout recovery remain UNKNOWN.

## Independent reproduction
```python
v0=3.55428
vgate=3.4
dv=v0-vgate
for amp,ms in [(0.1,0.1),(0.5,0.1),(0.5,1),(1,1),(0.5,5)]:
    print(amp,ms,round(amp*(ms/1000)/dv*1e6,1))
print("ESR 50mohm",round(.5*.001/(dv-.5*.05)*1e6,1))
```
These are calculations, **not measured transients**.

## Review / exit blockers
1. Source actual BQ25185 supplement/overcurrent response and TPS61023 startup input-current/current-limit/UVLO timing from manufacturer documents with temperature limits; typical curves cannot be used as guaranteed maxima.
2. Obtain actual protected 21700, protection path and candidate SYS capacitors with DC-bias/temperature/aging Cmin and ESRmax. Chat B #7 sourcing is dependency, not permission to select.
3. Derive or simulate bounded `I_deficit(t)` for BAT-only, USB insertion/removal and USB+BAT supplement; include startup precharge and negative signed IBAT when charging.
4. Check whether HV enable must be sequenced only after 5V settling; no firmware or hardware threshold changed here.
5. Chat C independently challenge the charge bound, then Work integrate if accepted. Shared ledgers deliberately untouched to avoid concurrent writes.

**CONDITIONAL:** ideal charge-conservation calculation. **BLOCKED:** any conclusion that the existing SYS capacitor, BQ path or TPS61023 can support 205V/16mA startup. **PENDING REVIEW:** not an approved design. No purchases, PCB manufacturing, main merge, HV energization or requirements changes.
