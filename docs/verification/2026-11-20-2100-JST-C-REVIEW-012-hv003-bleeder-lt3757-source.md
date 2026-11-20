# C-REVIEW-012 — Independent batch review: HV-003 bleeder and LT3757/TDK reference
Date: 2026-11-20 21:00 JST. Role: Chat C independent review. Branch: `codex/reva-integrated-prototype-review`.
Starting branch HEAD: **UNKNOWN** — GitHub connector compare confirmed branch is 3 commits ahead of C-REVIEW-011 SHA `36aecf4d81698b9b638219397fa1fdde4746d949`, and listed three files, but did not expose the branch tip SHA. Do not substitute a blob or a repository-global commit for branch HEAD.
Formal Claim: NONE; provisional batch review. No hardware safety approval.

## Evidence and scope
Read six required shared documents: docs/ai-workflow.md, docs/verification/handoff.md, docs/verification/open-issues.md, docs/verification/decisions.md, docs/tech-tree.yaml, docs/tech-tree.md. Compared last C-011 SHA against live branch and retrieved all three newly added reports:
- [Chat A 16:00 HV-003 RC discharge](2026-11-20-1600-JST-HV-003-bleeder-discharge-power-fault-screen.md)
- [Chat B 17:01 LT3757/TDK reference](2026-11-20-1701-JST-chatb-hv001-lt3757-tdk-primary-reference-screen.md)
- [Chat A 20:00 Vishay resistor family and faults](2026-11-20-2000-JST-HV-003-vishay-bleeder-working-voltage-and-fault.md)
Relevant issues: #2 HV topology, #6 OVP and discharge, #7 sourcing, #4 supply modes. GitHub Issues search showed open items; queue/claim state not atomic. Prior reports remain historical and no new parts adopted.

## Independent recomputation
Assume V0=205V, Vsafe=60V (NOT an approved safety threshold), C=1uF, no recharge. `t=RC ln(V0/Vsafe)`, `P=V^2/R`, `E=0.5CV^2`.
- R=100k: t=0.1229s, I205=2.05mA, P205=0.42025W, P220=0.484W.
- R=1M: t=1.2287s, I205=205uA, P205=0.042025W, P220=0.0484W.
- R=10M: t=12.287s, I205=20.5uA, P205=0.0042025W, P220=0.00484W.
- E205=21.0125mJ, E220=24.2mJ; 1M at 220V to 60V = 1.2993s; with Rmax=1.05M, Cmax=1.2uF => 1.637s.
- Two series equal nominal 500k with independent +/-5%: worst single share 1.05/(1.05+0.95)=0.525 => 115.5V at 220V. Nominal per-part P=24.2mW. If one shorts, other 500k takes 220V and 96.8mW. If one opens, discharge path absent.
- Two parallel 2M paths give 1M equivalent nominal. If one opens, R=2M, nominal time doubles; not proof against common-mode faults, HV supply remaining active or shorts.
**ACCEPTED (ideal arithmetic only)** for all these calculations. **CONDITIONAL** for voltage sharing and redundant branch topology under explicit fault assumptions. **BLOCKED** for real resistor MPN/rated continuous operation, approved endpoint/time, effective Cmax, PCB creepage/thermal, power-off cutoff, dielectric absorption and single-fault-safe discharge.

## Manufacturer LT3757 source verification
Directly inspected Analog Devices [LT3757/LT3757A Rev.H PDF](https://www.analog.com/media/en/technical-documentation/data-sheets/lt3757-3757a.pdf), printed page 32 (PDF page index 31), Typical Applications 'High Voltage Flyback Power Supply'. It explicitly identifies LT3757 (not LT3757A), TDK DCT15EFD-U44S003, Si7850DP, GSD2004S dual diode series, 1:10 transformer, 5–12V input, 350V/10mA output, 100kHz and 0.02-ohm sense. **ACCEPTED (manufacturer example identity and conditions)**. Manufacturer controller generic VIN 2.9–40V does NOT qualify the published example for 1S direct input.
3.50W vs 3.28W target = 6.707% nominal power difference. At assumed etaHV 75% or 80%, input at 5V = 0.8747A or 0.820A. At eta5 90% battery/SYS demand 4.859W or 4.556W before other loads. **ACCEPTED (arithmetic under assumed efficiencies)**, **BLOCKED** as actual 205V/16mA stage and order-ready transformer.
**Additional safety-critical issue:** Rev.H electrical table lists FBX overvoltage lockout at 6/7/8% relative to regulated FBX (positive). If simply scaled to nominal 205V, the *nominal-output-proportional* internal FBX OVP range would be approximately 217.3–221.4V before accounting for feedback/reference/divider tolerance or post-trip energy. Thus **internal FBX OVP cannot be claimed to enforce HV5524's 220V recommended maximum**. This is a screening calculation, not a full actual threshold proof. Independent hardware OVP remains mandatory. **CHANGES_REQUESTED** for any proposal using LT3757 internal OVP as independent 220V safety limiter. The Rev.H table also specifies FBX positive regulation 1.569/1.6/1.631V, which further requires full-corner analysis.
Source: Rev.H PDF pp. 3 and 32, https://www.analog.com/media/en/technical-documentation/data-sheets/lt3757-3757a.pdf .
The Vishay CRCW2512 500V/1W *family* assertion was NOT independently verified against an original current Vishay PDF in this run (A used a distributor-hosted manufacturer-authored mirror). **CONDITIONAL / primary-source verification outstanding**; exact resistor codes unavailable.

## Work decision package (important only)
Decision: keep LT3757 + TDK DCT15EFD-U44S003 as a **research alternative**, not a chosen topology; maintain independent OVP and bleeder/discharge as unqualified. A/B claims: concrete 350V/10mA 5–12V reference, and RC/resistor screens. Independently checked: original ADI Rev.H page 32 and p3; calculations above. Unknown: TDK original transformer drawing, Lp/leakage/Isat/DCR/insulation/temperature and Japan availability, 205V feedback/dynamics/efficiency, full worst-case OVP timing and Cmin/Cmax, resistor MPN/derating and discharge fault containment. Alternatives: MAX668 coupled-inductor, other 5V flyback references, direct-SYS design subject to low-cell proof. System effects: 5V rail near 0.82–0.875A HV-only at assumed efficiencies; thermal/USB battery-supplement and safety protection remain bottlenecks. Recommendation: ask Chat A for exact LT3757+TDK 205V/16mA loss/peak/OVP feasibility *as a candidate* and Chat B for TDK controlled drawing/stock and exact Vishay resistor orderable codes. Do not alter 16mA target, PWR draft or approved specs.
Source A/B report paths above, starting comparison base SHA `36aecf4d81698b9b638219397fa1fdde4746d949`; exact new report source commit SHA not established by this connector, verify via GitHub file history before claiming provenance.

## Queue and next review
Three new A/B reports in the examined branch diff, three reviewed here. Important pending count outside this exact diff **UNKNOWN** (full recursive tree and issue-to-report mapping not independently enumerated). Oldest pending globally **UNKNOWN**; historical 2026-11-17 coupled-inductor analysis requires coverage reconciliation. Next: #6 actual Cmin/Cmax and guaranteed OVP tail energy; #2 transformer source/peak-current limits; #9 fail-safe thermal interlock; #7 exact sourcing. No shared index edits, no main merge, purchase, PCB order, HV energization or safety approval.
