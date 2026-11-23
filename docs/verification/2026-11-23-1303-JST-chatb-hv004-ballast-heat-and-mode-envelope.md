# Chat B — HV-004 / SYS-001 ballast heat and simultaneous-mode envelope
Date: 2026-11-23 13:03 JST
Status: **PENDING REVIEW**; scoped outcome **CONDITIONAL**; hardware qualification **BLOCKED**
Role: Chat B wide research. Formal Claim: **NONE** (no verified atomic Claim mechanism).
Branch: `codex/reva-integrated-prototype-review`
Starting HEAD SHA: **UNKNOWN**. GitHub connector branch search confirms branch name but exposes no HEAD commit SHA; do not substitute file blob SHA or previous report's commit SHA.
Related issues: #7 PROTO-001; #4 SYS-001A; #10 HV-001.

## Bounded task and repository check
Question: How much of the 205V HV output power becomes ballast-resistor heat under a plausible simultaneous display, and how does this change the battery/USB and sealed-enclosure thermal contract?
Exit: transparent arithmetic, evidence classes, explicit mode gates; no resistor adoption.
Read branch ai-workflow, handoff, open-issues, decisions, tech-tree.yaml and tech-tree.md; open GitHub issues and latest known Chat B reports (2026-11-23 05:00 and 09:00). Existing 09:00 report already gave individual 20k/0.18W digit and 290k/0.0725W neon examples; this report adds aggregate heat, mode-dependent scaling and derating/fault gates rather than repeating individual calculations. Shared indexes left to Work.

## Evidence
- SECONDARY supplier tube data: IN-12B typical 145V sustaining and 2.5–3.5mA cathode current: https://www.tube-tester.com/sites/nixie/data/in-12b.htm ; independently https://omnixie.io/in12.html . Not original factory/lot guaranteed.
- SECONDARY commercial assembled IN-12B shield: MikroE reports 3mA per segment, typical start 150V: https://www.mikroe.com/nixie-in-12b ; not a manufacturer guaranteed tube corner.
- PRIMARY San Guang NE-2 manufacturer PDF (AC-only point) https://www.taydaelectronics.com/datasheets/files/1039.PDF 110VAC / 68kΩ / approx 0.7mA; **not** 205V DC.
- ASSUMED neon DC sustaining 60V at 0.5mA, for arithmetic only. A historical NE-2S data compilation suggests 44–74V at 0.3mA, but NE-2S is not a qualified substitute: https://studyres.com/doc/15181948/glow-lamp-specifications .
- TARGET 205V/16mA; no adopted 205V operating current, part/lot, simultaneous truth table, or resistor package.

## Calculation (all values ASSUMED unless marked)
HV supply V=205V; two digits each I_d=3mA at V_d=145V; twelve neon lamps each I_n=0.5mA at V_n=60V. All branches independently ballasted, continuous.
For each branch R=(V_HV-V_lamp)/I; P_res=(V_HV-V_lamp)*I; P_lamp=V_lamp*I; P_HV=V_HV*I.
Digit: R_d=20kΩ; P_Rd=0.180W, P_tube=0.435W, P_HV=0.615W each.
Neon: R_n=290kΩ; P_Rn=0.0725W, P_lamp=0.030W, P_HV=0.1025W each.
**All-on totals:** I_HV=2*3+12*0.5=12.0mA; P_HV=2.460W; P_ballast=2*0.180+12*0.0725=**1.230W**; P_lamps=2*0.435+12*0.030=**1.230W**. Thus half of output power heats ballast resistors under this particular assumed point. This is not an extra 1.23W to add to the 2.46W HV bus output: the bus already includes ballast dissipation. Avoid double-counting.
At 75% assumed HV conversion efficiency, upstream HV conversion loss = P_HV*(1/.75-1)=0.820W. At 90% assumed SYS→5V efficiency, additional converter loss = (2.46/.75)*(1/.9-1)=0.364W. Total **display-chain** heat (lamp+ballast+converters) =3.644W, excluding other loads, and equal to SYS power (energy conservation). Distribution matters for local hotspots and cell heating, not just total.
Resistor nominal power-rating ratio: 0.180W/0.25W=72% (digit), 0.0725W/0.25W=29% (neon). A 0.25W digit resistor is **NOT** qualified: enclosure temperature derating, board thermal resistance, resistor working-voltage and overload ratings, tolerance, tube extinguish/restrike, and supply high corner are unknown. A 0.5W part is a research candidate, not approved.
Potential fault: lamp short drives I≈205V/20k=10.25mA and P≈205²/20k=2.101W in digit resistor (nominal 20k, neglect tolerance); a 0.25W or 0.5W resistor cannot be assumed safe under sustained short. Neon short drives I≈205/290k=0.707mA and P≈0.145W, but other failure/OVP corners matter. Fault behavior requires hardware current limit, rated resistor/fuse strategy, and safe shutdown.
Mode formula: I_HV(N_d,N_n)=N_d*I_d+N_n*I_n+I_aux, P_ballast(N_d,N_n)=N_d*(205-V_d)*I_d+N_n*(205-V_n)*I_n. For 2 digits and 0/6/12 neon at the assumed point: I_HV=6/9/12mA, P_HV=1.230/1.845/2.460W, ballast heat=0.360/0.795/1.230W. This is not a specification for UI simultaneous behavior.
At 75%*90% assumed cascade efficiency, 12mA requires 3.644W SYS; USB 5V*0.5A=2.5W ideal and BQ input limit may be lower; full all-on 12mA USB-only remains impossible. Even 6mA would need 1.822W SYS before control loads and input-path loss; whether USB-only works requires mode-specific real measurement and current-limit corner. Battery supplementation is not equivalent to net charging.

## Design/fault/thermal gates
1. Define UI mode table: clock digits, 12-ring all-on/stepped/PWM, decimal point, startup, transition and fault defaults; verify time-averaged and instantaneous currents separately (PWM does not reduce instantaneous branch current).
2. Obtain selected exact NE-2 DC ignition/sustain/current/lifetime across temperature and IN-12B factory/lot evidence; use measured I-V only after separate human authorization and safe test plan.
3. Resistor worst-case V_HV high/low, tolerances, voltage working limit, power derating at sealed PETG hotspot, failure open/short, series splitting and creepage; 220V recommended HV5524 max is NOT a normal operating target.
4. Allocate enclosure heat separately to lamp, ballast PCB, HV magnetics/MOSFET, SYS converter, BATFET and cell; validate heat transfer and cell temperature under charge and battery-only.
5. Qualify two actual controller+magnetics pairs with stock/lead-time; this report does not qualify any.
6. Work SOP proposal: require a per-mode branch-count + ballast heat + failure-short resistor stress worksheet before adjusting the 16mA target. Do not directly edit ai-workflow.md.

**Decision:** CONDITIONAL arithmetic only; hardware/parts NO RELEASE (BLOCKED). Chat C to check no double-counting, 0.25W derating and fault-case validity. Work to integrate reviewed outcomes. No purchases, PCB manufacture, HV energization, main merge, requirement or schedule changes.
