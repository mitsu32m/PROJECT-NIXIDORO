# C-REVIEW-017 — MAX668 oscillator / LT8365 current-limit primary-source batch
Date: 2026-11-22 03:00 JST. Role: Chat C independent first-pass review. **NO FORMAL CLAIM; NO HARDWARE SAFETY APPROVAL**.
Repository mitsu32m/PROJECT-NIXIDORO, branch `codex/reva-integrated-prototype-review`.
**Verified starting branch HEAD:** `4c3948c6ed7d23c6cc50678f0dcaf2f131913c7a` (exact GitHub branch endpoint). Recursive tree enumerated at that SHA. Mandatory workflow, handoff, open-issues, decisions, tech-tree YAML and Markdown read. Latest C-REVIEW-016 and two newer A/B reports read. Open GitHub issues searched. Shared indices intentionally unchanged.

## Batch and queue
Two newly discovered PENDING REVIEW reports since C-016:
1. Chat A 2026-11-22 00:00: [MAX668 oscillator floor](https://github.com/mitsu32m/PROJECT-NIXIDORO/blob/4c3948c6ed7d23c6cc50678f0dcaf2f131913c7a/docs/verification/2026-11-22-0000-JST-HV-001-max668-oscillator-floor-dcm-exclusion.md).
2. Chat B 2026-11-22 01:03: [LT8365 limit table](https://github.com/mitsu32m/PROJECT-NIXIDORO/blob/4c3948c6ed7d23c6cc50678f0dcaf2f131913c7a/docs/verification/2026-11-22-0103-JST-chatb-hv001-lt8365-guaranteed-switch-current-table.md).
Both reviewed here (2/2 in new batch); oldest new pending report: 00:00 JST. **Historical unreviewed important count/oldest historical pending UNKNOWN** because complete Issue/comment/report mapping remains unfinished. No formal claim.

## Primary sources independently opened on 2026-11-22
- [ADI MAX668/MAX669 Rev 3, 6/2016](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX668-MAX669.pdf), pp1–3: adjustable 100–500kHz advertised; oscillator ROSC=500kΩ ±1% **85/100/115kHz min/typ/max** at the stated electrical table conditions (VCC=VLDO=5V, 0..85°C); at ROSC=200kΩ ±1%, **225/250/275kHz**. 100kHz is *typical*, not a guaranteed frequency floor. SYNC range 100–500kHz, not an authorization for arbitrary sub-100kHz operation. MAX668 max duty at ROSC=500kΩ is 86/90/94% (table conditions), not the same as energy-reset BCM duty.
- [ADI LT8365 Rev A](https://www.analog.com/media/en/technical-documentation/data-sheets/lt8365.pdf), p3: switch maximum current-limit threshold **1.5/2.0/2.7A min/typ/max**, full-temperature l marker; default electrical test VIN=12V and EN/UVLO=12V unless otherwise noted. p2 SW absolute maximum 150V; p1 nominal application 9–30V to -250V/10mA. p3 switch RDS(on) 700mΩ **typical at 0.5A**, not a guaranteed maximum at high current. E/J/H grade temperature guarantee requires careful Note 3 interpretation; 5V circuit topology and 5V threshold applicability are not independently proven by this table.

## Independent calculation and challenge
### Chat A MAX668 / fully reset *isolated* flyback
ASSUMED: Vin=4.75V, Vout=205V, diode drop=1V, Ns/Np=10, Lm=36/40/44µH, efficiency .8, f variable, fully reset triangular DCM/BCM.
BCM duty: D=206/(206+10*4.75)=0.8126232742.
Ideal Pout=eta*Vin^2*D^2/(2*Lm*f).
At 100kHz, Pout max (36/40/44µH) = 1.656/1.490/1.355W; at 85kHz (lowest specified oscillator table corner at ROSC=500kΩ), even 36µH yields ~1.948W. At eta=1 and 85kHz, 36µH yields ~2.436W, below 3.280W. At nominal Lm=40µH, eta=.8, required f <=45.425kHz; at 36µH f<=50.472kHz. Thus even the *85kHz guaranteed low corner* does not rescue the fixed-frequency fully reset model. At the BCM boundary idle time is zero; genuine DCM power is lower. **ACCEPTED (narrow model arithmetic and oscillator source)**. **CHANGES_REQUESTED**: A report calls 100kHz a published minimum adjustment range; replace with table's 85/100/115kHz and note 100kHz typical. **BLOCKED** any extension to actual MAX668 tapped/coupled boost, CCM or a different winding topology; manufacturer oscillator and Lm tolerance alone do not prove real circuit behavior.

### Chat B LT8365 switch limit
At assumed Vin=5V, Pout=3.28W, L=10µH, f=400kHz, D=.95, eta=.8/.75/.7, ideal single-inductor CCM proxy gives input average 0.8200/0.87467/0.93714A; ripple 1.1875A; peak proxy 1.41375/1.46842/1.53089A. At Vin=4.5V, eta=.75: avg .97185A, ripple 1.06875A, peak 1.50623A. **ACCEPTED (arithmetic only)**. **ACCEPTED (datasheet extraction)** 1.5/2/2.7A threshold at specified VIN=12V test conditions and temperature marker. **CHANGES_REQUESTED** for describing 1.5A as an unconditional guaranteed threshold at VIN=5V: not established from the quoted table alone. Also the proxy is **not** a DC2838A switch peak: flying-cap current paths, input capacitor pulses, topology, L/f tolerances and switch duty are untraced. 2.7A upper limit is a relevant worst-case *current-limit* stress corner, not a measured inductor peak or proof of protection. **BLOCKED** 5V/205V/16mA feasibility, continuous switch thermal, startup, charge-pump diode/cap stresses and HV protection.

### Shared energy/fault check
USB 5V*0.5A=2.50W < HV target 205V*.016A=3.28W before any conversion losses: USB-only full-target mode cannot work. At etaHV=.75, HV-stage input 4.3733W, leaving 1.8733W beyond the 2.5W USB ideal budget before upstream conversion, logic or charging. USB+BAT net current, battery cutoff, PCB thermal and PETG enclosure heating UNKNOWN. Both options require independent OVP/energy tail/Cmin/Cmax/discharge proof, and neither current-limit threshold substitutes for independent HV protection.

## Work decision package — recipient: Work integration lead
**Decision requested:** research sequencing and narrow exclusion only, not architecture or part adoption.
**A claim:** MAX668 100–500kHz excludes a 40µH fully reset isolated DCM route to 3.28W; **independent refinement:** guaranteed low oscillator table corner 85kHz still excludes the stated model, but 100kHz is typical, not hard guaranteed minimum.
**B claim:** LT8365 switch threshold 1.5/2/2.7A; **independent verification:** manufacturer Rev A p3 confirms at VIN=12V header; 5V use and actual charge-pump switch peak not proven.
**Alternatives:** (i) trace original MAX668 coupled/tapped schematic ON/OFF paths, then derive CCM/DCM stress; (ii) trace controlled DC2838A flying-cap circuit and 5V startup/current; (iii) source currently manufactured 5V-capable flyback controller+magnetics with guaranteed electrical/thermal data.
**System effects:** HV 205V/16mA target unchanged; HV5524 220V recommended ceiling, independent OVP, 5V/SYS battery-assist and low-cell startup, 21700/charger heat, prototype BOM qualification remain blocked.
**Recommendation:** Work may accept only narrow isolated-DCM no-go and Rev A limit-table evidence; request A oscillator table wording correction and B 5V/topology-specific proof. Do not adopt LT8365 or reject MAX668 universally. Source report URLs above, primary PDFs above, starting commit `4c3948c6ed7d23c6cc50678f0dcaf2f131913c7a`; saved report commit must be read from the actual GitHub create_file response.

## Next priority and holds
1. P0 #6 independent OVP: real comparator/ref/Cmin/Cmax/tail energy/stop time/fault discharge, worst corners.
2. P0 #2/#10 topology-identical MAX668/LT8365 current paths, manufacturer limits, startup, thermal, sourcing.
3. P0 #9 battery-only and charge-temperature hard interlocks; #8 PWR battery-assist, sealed-cell thermal; #7 BOM; historical queue reconciliation.
**Not done:** no KiCad netlist full audit, manufacturer transformer detailed qualification, actual PCB/thermal measurements, physical tests, purchases, PCB fabrication, main merge, HV energization, important spec changes, scheduler changes or safety approval.
