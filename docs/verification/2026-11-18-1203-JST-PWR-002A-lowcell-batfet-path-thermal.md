# PWR-002A — Low-cell BATFET/external resistance and 5V supply feasibility screen

Date: 2026-11-18 12:03 JST. Chat A deep-design. GitHub Issue #8, parent PWR-002/PWR-001/SYS-001. **PENDING REVIEW**; **NO FORMAL CLAIM**. Result: **CONDITIONAL** analytical model, **BLOCKED** real operating envelope. Starting HEAD SHA: **UNKNOWN** (GitHub connector branch search/fetch does not expose commit HEAD); branch ref explicitly used. Earlier integrated snapshot HEAD 90a2aad... is NOT assumed current. No shared indices edited.

## Task contract and new question
What happens to the integrated HV/logic load at low cell voltage when the cell/protection/connector/wire path has nonzero resistance in addition to BQ25185 BATFET? Exit: solve constant-power current and SYS voltage self-consistently, distinguish cell-side and charger-side dissipation, expose no-solution/undervoltage corners and define measurements. This is NOT a guarantee of the actual BQ BATFET curve, cell model, 5V converter regulation, charging or startup.

Read on working branch: ai-workflow v1.1, handoff (WORK-INT-002), open-issues, decisions, tech-tree.yaml; prior A 07:56 report and WORK-INT-002, plus issue search #1–#8. Work directs A to #8, B to sourcing #7, C to review #2/#4/#6. Therefore this report does not repeat tapped-boost diode-capacitance screening. GitHub issue labels and atomic claim not verified.

## Primary manufacturer data and classification
- TI [BQ25185 SLUSF65B Rev.B (Aug 2026)](https://www.ti.com/lit/ds/symlink/bq25185.pdf): BATFET RON 115mΩ TYP/140mΩ MAX at VBAT=4.5V, IBAT=400mA; **NOT guaranteed 140mΩ at 2–3A or high junction temperature**. BAT overcurrent ~3.13A TYP with ±18% accuracy at 27C; lower-side 2.5666A is a *temperature-specific arithmetic screen*, not guaranteed full-temperature trip. 500mA programmed input limit 450/475/498mA min/typ/max under specified conditions. Battery supplementation does not imply positive charge current.
- TI [TPS61023 Rev.B](https://www.ti.com/lit/ds/symlink/tps61023.pdf): 2.7A MIN valley limit at specified VIN=3.6V/VOUT=5V; not a guaranteed 5V output power at low SYS or startup. Startup requires >=1.8V input, which does NOT prove full-load startup at 1.8V.
- Existing project [PWR power-thermal review](../pwr-reva-power-thermal-review.md): etaHV=.70, eta5=.85, 5V logic 0.50W, SYS other 0.50W **ASSUMED**, and 205V/16mA TARGET. Work integration [INT-002](2026-11-18-work-integration-002.md) gives P_SYS=6.60084W at full load, excluding audio. No actual cell model or NTC chosen.

## Reproducible self-consistent DC model
For battery-only discharge: V_SYS=V_BAT-I*(R_BQ+R_EXT), P_SYS=I*V_SYS. Solve low-current branch of R_total I² - V_BAT I + P_SYS=0:

I=(V_BAT-sqrt(V_BAT²-4 R_total P_SYS))/(2R_total). A real root requires V_BAT² >= 4 R_total P_SYS. This is a **necessary algebraic condition** for a constant-power sink; it does not prove regulation, thermal stability or battery chemistry. High-current root is excluded as the undesirable unstable constant-power operating branch. R_BQ=0.14Ω extrapolated **ASSUMED** from 400mA MAX test; R_EXT=0/0.10/0.20Ω are **ASSUMED sensitivity values**, not measurements. V_BAT=4.0/3.6/3.3/3.0V **ASSUMED** at cell terminals, not approved discharge limits.

| VBAT | Rext | I BAT | VSYS | BQ BATFET I²R | external path I²R |
|---:|---:|---:|---:|---:|---:|
| 4.0V | 0Ω | 1.758A | 3.754V | 0.433W | 0W |
| 4.0V | 0.10Ω | 1.857A | 3.554V | 0.483W | 0.345W |
| 3.6V | 0Ω | 1.987A | 3.322V | 0.553W | 0W |
| 3.6V | 0.10Ω | 2.138A | 3.087V | 0.640W | 0.457W |
| 3.3V | 0Ω | 2.207A | 2.991V | 0.682W | 0W |
| 3.3V | 0.10Ω | 2.430A | 2.717V | 0.826W | 0.590W |
| 3.3V | 0.20Ω | 2.819A | 2.342V | 1.113W | 1.589W |
| 3.0V | 0Ω | 2.490A | 2.651V | 0.868W | 0W |
| 3.0V | 0.10Ω | 2.850A | 2.316V | 1.137W | 0.812W |
| 3.0V | 0.20Ω | 4.189A | 1.576V | 2.457W | 3.510W |

The 3.0V/0.20Ω root is near the mathematical maximum-power point and physically implausible as a safe operating regime; current protection, cell polarization, regulator UVLO/efficiency and temperature would likely intervene. 3.3V/0.20Ω and 3.0V/0.10Ω exceed the **27C-only** 2.5666A lower OCP arithmetic. At 3.3V/0.10Ω, I=2.430A is below that arithmetic number by only 0.137A, before startup and load transients. Rext heating occurs in cell, protection PCB, contacts and wiring; it must NOT be added to BQ junction loss.

**Key new insight:** The older model with only 0.14Ω at 3.3V estimates 2.21A. Adding just an assumed 0.10Ω of external series resistance raises BAT current to 2.43A and lowers SYS from 2.99V to 2.72V; the external 0.59W is a major cell/protection/connector heating source that a BQ-only thermal calculation misses. This is an illustrative risk, not a measured cell resistance.

## Thermal and power-stage gates
At TA=45C, TJ<=125C, and TI θJA=68.3C/W *reference-board only*, P_BQ,allowed=(125-45)/68.3=1.171W. The 3.3V/0.10Ω battery-only scenario gives ~0.826W BATFET, leaving ~0.345W hypothetical IC dissipation allowance for other mechanisms. At TA=50C the reference-board allowance is 1.098W, leaving ~0.272W. **These are NOT package guarantees in sealed PETG**; actual copper, layout and junction measurement are required. R_BQ at multiamp/high temperature may exceed the extrapolated value, creating positive feedback.

At 3.3V/0.10Ω VSYS≈2.717V, TPS61023 input inductor RMS, valley-limit, actual L1 Isat/DCR, 5V output capacitance, 5V startup and 5V efficiency at this VIN/load are UNKNOWN. P_SYS=6.60084W presumes 85% 5V efficiency independent of voltage, which is unjustified at this corner; actual efficiency may lower and increase current. If actual 5V fails regulation, the constant-power model ceases to represent real load behavior. Audio and charging transients excluded.

USB-only at configured 500mA remains impossible at 205V×16mA: 5V×498mA=2.49W at source <3.28W HV output even with lossless conversion. USB+BAT supplement must use signed IBAT and measured SYS, not this battery-only quadratic.

## Low-voltage test contract, NOT authorization
Using an isolated current-limited cell simulator and LV-only electronic load, after human test authorization: sweep equivalent cell terminal voltage 4.0→3.0V only within actual cell/protection ratings; introduce known series resistances without dissipating excess heat in a real cell; record signed IBAT, VSYS, 5V, input current, charger state, TPS61023 inductor waveform, BATFET case/board temperature and external resistor/contact temperature at steady state and startup/USB attach/detach. Calibrate current sign (positive=discharge). Stop on loss of 5V regulation, unstable oscillation, current-limit approach, excessive component temperature or abnormal cell/protection behavior; thresholds must be fixed from actual parts before test. Use thermal camera/thermocouples with cell-attached NTC. No HV load required; emulate 5V HV input with an LV electronic load.

## Disposition
**CONDITIONAL** analytical necessary-condition model; **BLOCKED** guaranteed current/thermal/startup due to BQ BATFET RON extrapolation, unknown actual cell/protection R, 5V efficiency/Isat and thermal resistance. **PENDING REVIEW** Chat C. Send to Work as evidence of external-path heating and mode-dependent power contract; no design values adopted. #8 already covers the missing evidence; no duplicate GitHub Issue. No shared indices, KiCad, main, purchasing, fabrication or HV energization changes.

Reproduction: `python hardware/integration/pwr002a-lowcell-path-screen.py` (Python 3.10+). No physical measurements performed.
