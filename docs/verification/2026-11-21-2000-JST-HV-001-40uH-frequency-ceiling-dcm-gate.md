# HV-001 / Issue #2 — 40 µH DCM frequency ceiling and MAX668 oscillator mismatch
Date: 2026-11-21 20:00 JST. Role: Chat A deep-design. Branch: `codex/reva-integrated-prototype-review`.
**PENDING REVIEW — CONDITIONAL analytical frequency gate; hardware BLOCKED. NO FORMAL CLAIM.**

## Bounded question and evidence
Can the already screened 40 µH / 1:10 transformer, operated in the *explicitly hypothetical isolated fully-reset flyback DCM model*, transfer the target 205 V × 16 mA at the MAX668 draft's nominal 250 kHz? What is the maximum permissible frequency for this model at a stated efficiency? This extends the 2026-11-21 11:55 and 15:55 Chat A reports without claiming that their hypothetical flyback is the actual MAX668 coupled-inductor wiring.

Read live branch SOP, handoff, open-issues, decisions, tech-tree.yaml, existing HV transformer screening, Chat A 08:00/11:55/15:55 reports, and GitHub Issue #2. Reviewed other issue roles to avoid duplicating Chat B's LT8365 investigation. Formal atomic Claim not established; no claim asserted. Exact branch HEAD and complete report tree enumeration were not available through this read path; UNKNOWN. Shared indexes reserved for Work integration.

Primary manufacturer references (as already catalogued in repo):
- ADI MAX668/MAX669: https://www.analog.com/media/en/technical-documentation/data-sheets/MAX668-MAX669.pdf ; existing draft ROSC=200 kΩ yields nominal 250 kHz (TYPICAL design formula, not guaranteed operating frequency).
- Würth 750315839: https://www.we-online.com/components/products/datasheet/750315839.pdf ; 40 µH ±10%, 1:10, representative 50–200 kHz application range, 200 V/12 mA (not 16 mA guarantee).
- Sumida 13324-T087: https://media.digikey.com/pdf/Data%20Sheets/Sumida%20PDFs/13324-T087_Spec.pdf ; 40 µH ±10%, 1:10, no 205 V/16 mA qualification.

## Independent reproducible derivation
**ASSUMED** ideal single-switch isolated DCM flyback with complete demagnetization, linear magnetizing ramp, negligible switching delays and constant eta=0.80. **ASSUMED** Vin=4.75 V, diode drop=1 V, N=10; **TARGET** Pout=3.28 W.

Ipk=Vin D/(Lm f); Pout=eta Vin² D²/(2 Lm f). Thus for fixed Lm and duty, achieving Pout requires
f <= eta Vin² D²/(2 Lm Pout).

The demagnetization condition requires D + Dreset <= 1, with Dreset=N Vin D/(Vout+Vd); therefore D <= (Vout+Vd)/(Vout+Vd+N Vin) = 206/253.5 = 0.812623. Equality is BCM boundary, not DCM with idle margin.

At nominal Lm=40 µH:
- D=0.75 (DCM idle margin about 7.71%): f <= **38.69 kHz**.
- D=0.812623 (optimistic BCM boundary): f <= **45.42 kHz**.
- At f=100 kHz and D=0.75, Pout=**1.269 W** (prior report).
- At f=250 kHz and D=0.75, Pout=**0.508 W**, NOT 3.28 W.

At the optimistic BCM boundary, Lm tolerance changes frequency ceiling inversely:
- Lm=36 µH: f <= 50.47 kHz.
- Lm=40 µH: f <= 45.42 kHz.
- Lm=44 µH: f <= 41.30 kHz.

These ceilings assume eta 80% independent of switching frequency, which is physically not guaranteed. A lower actual efficiency makes the frequency ceiling lower. Even 50 kHz at Lm=40 µH cannot deliver 3.28 W in this specific fully reset model with eta<=80% and Vin=4.75 V. Manufacturer's 50–200 kHz *representative application* is not a universal transformer absolute frequency limit, and changing ROSC does not by itself qualify the converter.

## Independent challenge
This model is **not** a topology-independent power limit. CCM can transfer energy with nonzero valley current; coupled-inductor boost has a different diode current path; alternative control and frequency modes can change constraints. Therefore it would be incorrect to reject Würth 750315839 or MAX668 universally. Further, 250 kHz is the existing nominal oscillator setting, not a measured switching frequency under all conditions; the exact original Zhang/ehbtj circuit winding dots and controller operation are still unverified. The cited 3.2 A Würth Isat is typical, not a guaranteed current ceiling. Input droop, diode recovery, leakage spike, MOSFET losses, core heating, startup and 220 V OVP are not bounded.

## Disposition
**NO-GO (strictly scoped):** claim that a 40 µH, N=10 transformer at nominal 250 kHz, Vin=4.75 V and eta<=80% can deliver 205 V/16 mA by fully-reset isolated flyback DCM energy transfer. Under the assumed DCM model even its optimistic boundary requires f<=45.42 kHz at nominal Lm.
**CONDITIONAL:** formula and parameterized frequency ceiling as an early topology/oscillator consistency gate.
**BLOCKED:** actual MAX668 coupled-inductor topology, switching frequency/mode, real magnetics, MOSFET/rectifier stresses, losses, startup, independent OVP and thermal evidence.
**PENDING REVIEW:** Chat C should independently validate this inverse-frequency result and ensure no DCM proxy is used as a CCM/coupled-boost disqualification. Work must retain D-004/D-005 and avoid part adoption.

Next A: obtain exact original coupled-inductor schematic/dot polarity and two conduction-state node voltages; only then compute genuine controller switch, rectifier and core stresses at the actual oscillator setting. No purchases, PCB manufacture, HV energization, main merge, KiCad or requirements changes.
