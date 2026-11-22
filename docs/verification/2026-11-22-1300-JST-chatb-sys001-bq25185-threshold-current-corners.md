# Chat B — SYS-001 BQ25185 supplement thresholds and input-current corners
Date: 2026-11-22 13:00 JST
Status: **PENDING REVIEW**; conclusion **CONDITIONAL** for manufacturer threshold transcription; **BLOCKED** for actual 205V/16mA full-load qualification. **NO FORMAL CLAIM**.
Branch: `codex/reva-integrated-prototype-review`; verified starting HEAD: `bc6e0d2f43ccbf76f5ec9ded08c382aaaf1bbf30`.
Issue #4 SYS-001A; related #7/#8/#9. Chat B research; no shared index edits.

## Task contract and nonduplication
Question: What numerical electrical limits bound USB input and BAT supplement onset/exit in the proposed BQ25185 path, beyond the 09:00 descriptive report? Exit: extract TI guaranteed vs typical values and quantify power deficit under minimum programmed input limit and near UVLO, with mode/fault implications.
Read required six canonical files (ai-workflow, handoff, open-issues, decisions, tech-tree YAML and MD), latest C-018, A 11:55 and B 09:00 reports, and open Issues #2/#4/#7/#10. Search metadata lacks dependable Claim state; no atomic Claim attempted or asserted. Shared indexes reserved for Work.

## Primary evidence
TI BQ25185 **SLUSF65B Rev.B (revised Aug 2026)**, official https://www.ti.com/lit/ds/symlink/bq25185.pdf, electrical characteristics pp.6–8 and feature descriptions §6.3.2–6.3.3. Table condition VIN=5V, VBAT=3.6V, -40<TJ<125C unless otherwise noted; typical at 25C.
- Configured **500mA** input-current limit: **MIN 450mA, TYP 475mA, MAX 498mA** (specified electrical-characteristics row; not a promise of 500mA at SYS).
- Supplement onset VBSUP1: **40mV TYP**, condition VSYS < VBAT - VBSUP1, VBAT>VBUVLO. Exit VBSUP2: **20mV TYP**, VSYS>VBAT-VBSUP2. No MIN/MAX published in these rows: threshold tolerances and transient continuity **UNKNOWN**.
- BAT UVLO threshold VBAT falling: **3V TYP**; recovery hysteresis VIN=5V **110/150/190mV MIN/TYP/MAX**, VIN=0 **90/150/210mV**. Do not interpret 3V as guaranteed minimum usable cell voltage.
- BATOCP reverse-current threshold **3.13A TYP** at VBAT=4V; accuracy ±18% specified at 27C and 3.125A, not guaranteed continuous current across all temperatures. Recommended battery discharge up to 3.125A is not thermal/PCM qualification.
- BATFET RON **115mΩ TYP / 140mΩ MAX** only at VBAT=4.5V, IBAT=400mA; extrapolating 140mΩ to low-cell 1–2A is unsupported.
- Charger thermal resistance RthetaJA **68.3 C/W JEDEC**, not sealed PETG board effective thermal resistance. BQ TS monitoring in battery-only absent per Rev.B §6.4 p19; separate thermal stop needed.
- Rev.B page 7 VIN=5V test conditions distinguish device electrical table from all-use operating guarantees.

## Reproducible necessary power bound
PROJECT TARGET (unverified lamp demand): 205V*0.016A=**3.280W**.
For illustrative assumed etaHV=0.75, eta5=0.90, Paux=0: Psys=3.28/(0.75*0.90)=**4.85926W**. This is not a manufacturer efficiency guarantee.
USB ideal input power at nominal 5V:
- 450mA MIN limit: **2.250W** available at IN; deficit **>=2.60926W** at SYS under lossless IN->SYS.
- 475mA TYP limit: **2.375W**; deficit **>=2.48426W**.
- 498mA MAX limit: **2.490W**; deficit **>=2.36926W**.
These are *lower bounds* on deficit for that assumed efficiency pair; real IN->SYS losses and auxiliary loads increase them. For a hypothetical 3.0V BAT, the 450mA case implies ideal battery contribution **>=0.86975A** (2.60926/3.0). This is NOT a permitted continuous low-cell operating point: 3V is UVLO typical, SYS may droop and the battery protector may cut earlier. Even at 3.6V ideal equivalent is >=0.7248A. No current/heat guarantee follows.
In supplement mode battery is **discharging**, not simultaneously net charging at this load/input envelope. USB-only continuous full 3.28W is NO-GO regardless of efficiency because max 2.49W nominal is less than HV output power alone.

## Mode, thermal and fault gates
1. USB-present normal: DPPM first reduces charge current; supplement only if charge reaches zero and SYS droops near BAT. The onset/exit are **typical mV thresholds**, not guaranteed regulated SYS margin.
2. BAT near UVLO: controller may disconnect battery; supplement cannot be treated as a guaranteed uninterruptible path. USB plug/unplug, PCM cutoff and HV inrush require brownout/hard-off/discharge analysis.
3. BATOCP/thermal: 3.13A threshold and 140mΩ@400mA cannot be used to certify >=0.87A continuous at low VBAT, high ambient. Evaluate selected cell, PCM, BATFET loss and PCB+enclosure temperature with real data.
4. USB-only/charging: no 16mA mode at 500mA, and no concurrent positive net charging at this load. A user-approved reduced-load USB mode or battery-assist with explicit energy/temperature constraints is necessary.
5. HV alternatives: MAX668 series-aiding autotransformer, LT3757 flyback, LT8365 charge pump and direct-SYS flyback remain research options; no currently qualified sourceable controller+magnetics pair, OVP or HV stop. No new procurement stock verified.

## Chat C review questions / Work handoff
Check Rev.B p6–7 ILIM, VBSUP1/2, UVLO and OCP table conditions; independently recompute 2.60926W / 0.86975A; challenge use of 'MIN' ILIM as guaranteed input deliverable (it is a current-limit threshold, not an assured source current). Determine whether supplement onset and UVLO corners can be safely combined without guaranteed min/max. Keep SYS-001 and PWR-002 OPEN; no schematic or requirement adoption.
Proposed SOP addition for Work consideration: every mode-budget report must distinguish **programmed current-limit threshold** from guaranteed available adapter power and distinguish threshold TYP from transition guarantees. Do not directly edit ai-workflow.
No purchase, PCB manufacture, HV energization, main merge, important requirement change or automation change.
