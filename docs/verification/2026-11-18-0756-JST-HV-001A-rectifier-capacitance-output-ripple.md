# HV-001A — Rectifier junction capacitance loss and output-capacitor ripple screen (hypothetical tapped boost)

- Timestamp: 2026-11-18 07:56 JST
- Issue: HV-001A / GitHub #2, parent HV-001, Chat A deep-design
- **PENDING REVIEW**; **CONDITIONAL** for ideal algebra, **BLOCKED** for actual topology/component qualification
- **NO FORMAL CLAIM**: atomic claim mechanism not verified
- Branch: `codex/reva-integrated-prototype-review`; starting HEAD **UNKNOWN** (available commit search returns older default-branch commits and cannot certify working branch HEAD). This is a new unique file, not a shared-index edit.

## Startup and bounded task
Read required `docs/ai-workflow.md`, `docs/verification/handoff.md`, `docs/verification/open-issues.md`, `docs/verification/decisions.md`, `docs/tech-tree.yaml`, `docs/tech-tree.md`, and most recent known 2026-11-18 03:55 HV-001A report; checked open GitHub Issues. No atomic claim. The 03:55 report already derives magnetizing current and ideal diode reverse voltage, so this run adds *rectifier capacitive switching sensitivity and output-capacitor RMS/ripple*, without reasserting a verified circuit. A full directory listing/reliable branch HEAD is unavailable via the current connector; a newer concurrent report cannot be excluded.

**Question:** Under the exact ideal series-aiding tapped-inductor boost topology specified in the 03:55 report, how large can rectifier junction-capacitance switching energy become at 222kHz, and what is the output-capacitor AC-current burden? Exit: equations and sensitivity table, conditions under which these estimates fail, evidence gaps.

## Source classifications
- Project TARGET: 205V / 16mA continuous = 3.28W.
- Analog Devices [MAX668/MAX669 Rev3, 2016](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX668-MAX669.pdf): controller oscillator range 222–278kHz at Rosc=200kΩ ±1% over full rated temperature, specified conditions. This is **not** a guaranteed operating frequency of a final circuit with unspecified Rosc.
- Würth [750315839 Rev003.001](https://www.we-online.com/components/products/datasheet/750315839.pdf): 40µH ±10%, 1:10, 50–200kHz **typical application**. It is a flyback transformer, **not** an approved tapped-boost magnetic. Values are used hypothetically.
- Vin=4.75V, n=10, Lp=36µH, f=222kHz, C_HV=1µF, ideal CCM, perfect coupling and lossless rectification are all **ASSUMED**. No selected diode capacitance, C(V), Qrr, recovery waveform, transformer parasitics or measured thermal data exist.

## Ideal waveform and output capacitor current (increment over 03:55)
From prior internally consistent model: D=(205/4.75-1)/(205/4.75+10)=0.793069; I_m,avg=0.850526A; ΔI_m=0.471356A. During ON, output diode current 0 and capacitor supplies Iout. During OFF, diode current i_m/(n+1). Thus ideal diode peak=(0.850526+0.471356/2)/11=0.09875A; valley=(0.850526-0.471356/2)/11=0.05590A; average diode current 16mA. Diode RMS=sqrt((1-D)*(I_m,avg²+ΔI_m²/12))/(n+1)=0.03564A. Capacitor RMS=sqrt(I_diode,rms²-Iout²)=0.03185A, assuming steady DC output and negligible ESR/other AC paths. Capacitor ON-period charge depletion ΔQ=Iout*D/f=57.16nC; at 1µF, ideal capacitive droop ΔV≈57.16mV per cycle, **not** total ripple: ESR, diode pulse recharge, leakage, frequency spread and HV capacitance derating are omitted. Output capacitor RMS/ESR heating is not negligible a priori; requires vendor ESR at relevant frequency and temperature.

## Rectifier capacitive loss sensitivity
Ideal rectifier peak reverse voltage in this hypothetical topology: V_R=Vout+n Vin=252.5V (4.75V). If Vin=5.25V **ASSUMED** high corner, V_R=257.5V; diode rating cannot be selected from 252.5V alone. Leakage overshoot is unknown. For an ideal *linear constant capacitance* Cj charged/discharged once per switching cycle, an illustrative full-energy-dissipation model gives E_event=0.5 Cj V_R² and P_event=0.5 Cj V_R² f. This is **not a proven diode junction heating loss**: charge recovery paths, non-linear C(V), reverse recovery, switching node trajectories, resonant exchange and actual dissipation location matter. The expression is a system-level switched-capacitance energy scale, not a guaranteed thermal loss.

At V_R=252.5V, f=222kHz:

| Cj assumed | Energy/event | P_event scenario | fraction of 1.406W HV-stage loss budget (eta=70% assumed) |
|---:|---:|---:|---:|
| 5pF | 0.159µJ | 0.0354W | 2.5% |
| 10pF | 0.319µJ | 0.0708W | 5.0% |
| 30pF | 0.956µJ | 0.212W | 15.1% |
| 100pF | 3.188µJ | 0.708W | 50.4% |

This loss model is a **screening scenario**, not a component prediction. With nonlinear junction capacitance use energy `Eoss(V)=∫_0^V v*Cj(v) dv`, or the manufacturer's energy/charge data; do not use a small-signal capacitance at one bias as constant over 0–252.5V. At 278kHz, all table powers scale by 278/222=1.2523. For a 30pF constant-C assumption, P≈0.266W. A 5.25V high corner gives voltage-squared factor (257.5/252.5)^2≈1.040, before spikes.

## Nonideal counterexamples and next evidence
1. Reverse recovery can add a large current spike and loss; a high-voltage rectifier must be screened for Qrr/trr, junction capacitance, peak pulse current, VRRM including leakage and thermal resistance, using manufacturer test conditions. A generic 400V rating alone does not qualify it.
2. Capacitance charging energy may be returned elsewhere in the circuit; do not claim P_event is entirely diode junction heat or simply add it to MOSFET losses without a switching-energy accounting.
3. C_HV=1µF nominal is not guaranteed effective capacitance at 205V and temperature. Output capacitor voltage rating, ESR, self-heating, stored energy, bleed/discharge and transient OVP remain independent constraints.
4. 222kHz is above Würth transformer's 50–200kHz typical application; high-frequency core/AC copper loss remains UNKNOWN.
5. Open load, startup, MOSFET stuck on, control reset, independent OVP and 220V HV5524 recommended limit are not resolved by this screen.
6. Exact original Zhang/ehbtj winding polarity and diode connection still unknown; all equations apply **only** to the assumed topology. The 03:55 report's winding currents are not validated for either original build.

## Decision / next task
**CONDITIONAL**: for the assumed tapped-boost CCM waveform, capacitor current and rectifier capacitive-energy equations offer a useful sensitivity screen. **BLOCKED**: no vendor-selected rectifier, measured switching transitions, verified original circuit, magnetic qualification, 205V/16mA continuous thermal proof or independent OVP. **PENDING REVIEW** for Chat C. Existing Issue #2 covers topology verification; no duplicate issue required. Suggested next bounded research: manufacturer-documented 400–600V rectifier options with guaranteed reverse recovery and capacitance/energy versus voltage, then quantify MOSFET/diode switching losses on a verified topology.

No KiCad, shared register, main, manufacturing, purchasing or HV energization changes.
