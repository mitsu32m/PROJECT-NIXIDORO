# Open technical issues — living register

Updated 2026-11-25 JST. Priorities: **P0** blocks safety or physical feasibility; **P1** blocks implementation/manufacturability; **P2** optimizations. Every automated run should select the highest-value unresolved issue and record its own review, with explicit evidence and close criteria.

| ID | Priority | Issue / current evidence | Exit criterion | State |
|---|---|---|---|---|
| HV-001 | P0 | CJ5143 real1:15 characterized at1.2A not continuous;low-SYS reset limits.Würth003.001 drawing/functional insulation partially verified;no qualified pair;#2/#10; [WORK-INT-005](2026-11-24-1003-JST-WORK-INT-005-ovp-timing-and-magnetics-gates.md) | Manufacturer primary electrical spec, feasibility calculation including losses/thermal/startup and evidence path | OPEN |
| HV-002 | P0 | C-027 confirms29us NOM correction;new TPS22918 upstream candidate2us TYP notmax;default-off/max stop still unknown;#6;[WORK-INT-007](2026-11-25-0956-JST-WORK-INT-007-cutoff-energy-and-current-gates.md) | Full FB+OVP tolerances incl. transient & fault-stop latency below 220 V, with acceptable operating window | OPEN |
| HV-003 | P0 | Upstream cutoff does not remove downstream LV capacitor energy;QOD weakens atVIN loss and notHV discharge;real latch/cut/reversefeed/fault paths missing;#6;[WORK-INT-007](2026-11-25-0956-JST-WORK-INT-007-cutoff-energy-and-current-gates.md) | Detailed circuit, single-fault analysis, shutdown under power loss/reset, controlled discharge to defined safe voltage/time, supervised review | OPEN |
| HV-004 | P0 | A1A03/17 Rev2 nominal0.5mA/95VDC vs undated manufacturer0.6mA/90VDC;lot/DC/life unknown;PCN333 A1A-T only obsolete;IN12B unqualified;#4/#7; [WORK-INT-008](2026-11-25-2159-JST-WORK-INT-008-neon-revision-and-lifecycle-gate.md) | Lamp primary specs and bench test plan; approved total worst simultaneous current and rated HV resistors | OPEN |
| PWR-001 | P0 | Low-SYS TPS61023 realL1/Ceff/current/heat/startup unresolved; include same HV Cmax and bleeder loss; #8; [WORK-INT-004](2026-11-23-2201-JST-WORK-INT-004-power-discharge-topology-integration.md) | Worst-case supply, current limit, selected L1 Isat,DCR, C eff, thermal simulation + supervised bench measurements | OPEN |
| PWR-002 | P0 | TI Rev.B supplement verified descriptive only; 115/140mohm at4.5V/400mA not low-cell high-current guarantee; input limit not delivery; #8; [WORK-INT-004](2026-11-23-2201-JST-WORK-INT-004-power-discharge-topology-integration.md) | Quantified component losses, BATFET extrapolation warnings, charger states, thermal test inside planned enclosure | OPEN |
| BAT-001 | P0 | K/R distinct; manufacturer R15A not K rating; real PCM/NTC/holder fit, temp cutoff and contact heat unknown; #7/#9; [WORK-INT-004](2026-11-23-2201-JST-WORK-INT-004-power-discharge-topology-integration.md) | Cell + protection spec, NTC verified attached to cell, discharge/charge/temp limits, connector/test plan | OPEN |
| SYS-001 | P0 | Lamp current remains assumption;A1A revision/DC unresolved;16mA lamp/bus boundary and actualpump lowSYS/charge thermal unknown;#4/#10; [WORK-INT-008](2026-11-25-2159-JST-WORK-INT-008-neon-revision-and-lifecycle-gate.md) | C-003/004 mode/startup arithmetic reviewed only within assumptions; need actual lamp, source, signed BAT, startup and charge/discharge thermal state bounds | OPEN |
| CTRL-001 | P1 | HV5524/OE, RTC, AMP/off-domain leakage unfinished; add reviewed thermal fault/inhibit interface via #9 without MCU-only safety claim | Correct manufacturer pin mapping, power-off-fail-safe interface, low-voltage tests | OPEN |
| NET-001 | P1 | Physical HV and LV connectors and insulation not fixed | Manufacturer-referenced parts, pin1 match and creepage/clearance assessment | OPEN |
| BOM-001 | P1 | A1A-T OBS2014 not allA1A;cached NRND/price not live quote;11/15 BOM historical;exact suffix landed staged quote missing;#7; [WORK-INT-008](2026-11-25-2159-JST-WORK-INT-008-neon-revision-and-lifecycle-gate.md) | Dated, reproducible itemized cost incl. shipping/tax/PCB/rework; initial ≤40k, reserve ≥10k | OPEN |
| SYS-002 | P0 | D-024 includes downstreamLV Ceff/magnetic/latency/alternatefeed in sameHV Cmin/Cmax budget;inputCL limits onlyassumed screens;#6/#8;[WORK-INT-007](2026-11-25-0956-JST-WORK-INT-007-cutoff-energy-and-current-gates.md) | One real Cmin/Cmax, bounded tail energy, startup surplus, discharge time/faults and reviewed margins; #6/#8 | OPEN |
| PROTO-001 | P0 | 11/25 21:59-start HEAD evidence still incomplete;no qualifiedpair/protection/cellassembly/landedBOM;new lamp revision/lifecycle holds;#7; [WORK-INT-008](2026-11-25-2159-JST-WORK-INT-008-neon-revision-and-lifecycle-gate.md) | Exact lamp/cell/magnetics/controller/capacitor/safety candidates, evidence holds, current costs/lead times and staged BOM | OPEN |

| THERM-001 | P0 | C-007 ratio proof accepted narrowly; MCU-only pullup/CE float not fail-inhibit; charge/load/HV residual independent paths required; #9; [WORK-INT-004](2026-11-23-2201-JST-WORK-INT-004-power-discharge-topology-integration.md) | Real cell/NTC error/hysteresis/fault budget, MCU-off state, charge and load cut paths, mode/pin/cost impacts; C review before schematic change | OPEN |

## Issue handling

For each dated verification log, update issue `State` to `IN REVIEW`, `BLOCKED`, `RESOLVED (scope)` only with grounded evidence; link dated log in the relevant row. Maintain prior claims when correcting, by describing superseding result. No result is considered `RESOLVED` solely because an ERC check returns zero violations.

## 2026-11-17 — integration triage (WORK-INT-001)

[Integrated review and adoption gates](2026-11-17-work-integration-001.md), baseline 0d83c2d0d551e0893aa1eced613a250ec6a12181. SYS-001 priority elevated P1→P0 for physical feasibility; no issue resolved. Latest Chat A quantitative screen remains PENDING REVIEW; no located new Chat B or Chat C package in examined branch/issues/PRs.

- HV-001A is already [GitHub Issue #2](https://github.com/mitsu32m/PROJECT-NIXIDORO/issues/2); no duplicate or formal claim.
- Prioritize proposed HV-004A lamp-current provenance/current budget alongside topology investigation. 16mA is an assumed load sum, not measured necessity.
- Proposed C-REVIEW-001: review 10:25 Chat A report plus integration; MAX668 full-temperature oscillator range is 222–278kHz at ROSC=200kΩ±1%, not the 0..85°C 225–275kHz table.
- Proposed SYS-001A: integrated mode contract; link PWR-001, PWR-002 and BAT-001. Adoption gates and exact bounded task outputs are in the report. No workflow/claim blocker stops this research.

## 2026-11-18 — current integration (supersedes 11/17 availability snapshot)

[WORK-INT-002](2026-11-18-work-integration-002.md) integrates C-REVIEW-001/002 and references newer A/B as unreviewed. No hardware issue closed. C-REVIEW-003 batch requested: B lamp/direct/DCM/startup and A ideal-tapped series; B 05:03 currents and ratio are not a consistent 16mA operating point. Existing #2/#4/#6 retained; new #7 PROTO-001 (B) and #8 PWR-002A (A). Research continues without formal Claim. Release locks do not prohibit design work.

## 2026-11-19 — current batch integration

[WORK-INT-003](2026-11-19-work-integration-003.md): C-003〜006 integrated; thermal contract is the new highest-impact decision. All physical issues remain OPEN; #9 defines a distinct PWR/CTRL/pack enforcement interface alongside #8 models and #7 parts. Source correction: battery-only TS absence is TI §6.4 functional-mode table p19, not Table 6-2. STM010 PDF body is 20mm; environment/attachment remain unresolved.

Next C batch should address oldest tapped/HV magnetics blockers (#2) rather than repeatedly rechecking generic NTC descriptions. New Work restricted passive-ratio proof is pending C review. User budget deadline 2027-01末; proposed 11/25 evidence, 12/01 design, 12/15 first-order decision checkpoints remain planning proposals.


## 2026-11-23 — Work batch integration / no issue closed

[WORK-INT-004](2026-11-23-2201-JST-WORK-INT-004-power-discharge-topology-integration.md): C-007〜024 scoped review integrated. Formal Claim unavailable/unasserted; historical pending count UNKNOWN. All hardware issues remain OPEN and release gates locked.
Existing Issues #2/#4/#6/#7/#8/#9/#10 cover this batch; no duplicate created. #10 LT8365 DC2838A multiplier explicitly mapped to HV-001 (alternative, not adopted).
Next evidence is actual component/controlled drawing, guaranteed timing/fault path and cost, not another qualitative sensitivity comparison. 11/25 evidence checkpoint remains a proposal. Pending B21:03 requires C review; Work arithmetic acceptance is separate.


## 2026-11-24 — Work OVP / magnetics integration

[WORK-INT-005](2026-11-24-1003-JST-WORK-INT-005-ovp-timing-and-magnetics-gates.md): C-025/026 integrated; B09:03 remains PENDING C REVIEW. C-025 reviewed oldB21:03/Work004 INFEASIBLE arithmetic; older pending-status statements above retain historical date only.
Correct delay polarity to TLV6700 input-rise tPLH29us NOM; no maximum/fail-off proof. Real candidate nodes remain alternative; hardware issues OPEN and release gates locked.
Existing #2/#6/#7 cover new outputs, no duplicate issue. Next: real stop-latch/chain/cap guarantee table, continuous magnetics/controller match and actual landed quote.11/25 evidence checkpoint and<=40k initial/10k reserve remain proposals/unproven.


## 2026-11-25 — C-027 and cutoff-energy integration

[WORK-INT-007](2026-11-25-0956-JST-WORK-INT-007-cutoff-energy-and-current-gates.md): B11/24 09:03 and Work005 timing correction now have C-027 scoped review; older pending statements are historical. A04:01 source/math partially checked by Work, remains pending C. No hardware issue closed or release gate opened.
#6/#7/#10 already cover this batch; no duplicate Issue. Next outputs must be actual circuit/cap-node energy/fault bounds and landed quotes, not repeated sensitivity only.11/25 evidence snapshot is notyet complete; budget notestablished; 12/01/12/15 remain proposed checkpoints.


## 2026-11-25 evening — WORK-INT-008

New lamp source differences and suffix-specific PCN evidence above are PENDING C REVIEW; all issues remain OPEN. Close HV-004 only after applicable manufacturer revision/lot and DC current/life/ballast evidence, not by choosing the more convenient table. No new Issue: existing #4/#7 cover this batch.
