# Open technical issues — living register

Updated 2026-11-18 JST. Priorities: **P0** blocks safety or physical feasibility; **P1** blocks implementation/manufacturability; **P2** optimizations. Every automated run should select the highest-value unresolved issue and record its own review, with explicit evidence and close criteria.

| ID | Priority | Issue / current evidence | Exit criterion | State |
|---|---|---|---|---|
| HV-001 | P0 | No qualified 205V/16mA actual stage; #2 hypothetical tapped models are not original-circuit identification; direct-SYS options pending review. [INT-002](2026-11-18-work-integration-002.md) | Manufacturer primary electrical spec, feasibility calculation including losses/thermal/startup and evidence path | OPEN |
| HV-002 | P0 | Static high ~214.13V; reviewed OVP algebra accepted only within assumptions. MAX668 shutdown 70us is TYP, no guaranteed tail bound. [C-002](2026-11-17-2258-JST-C-REVIEW-002-hv002b-ovp-energy-and-shutdown.md), #6 | Full FB+OVP tolerances incl. transient & fault-stop latency below 220 V, with acceptable operating window | OPEN |
| HV-003 | P0 | Independent hard-off/discharge absent; co-design Cmin OVP vs Cmax startup/discharge (SYS-002), #6 | Detailed circuit, single-fault analysis, shutdown under power loss/reset, controlled discharge to defined safe voltage/time, supervised review | OPEN |
| HV-004 | P0 | B lamp provenance/envelope report exists but is unreviewed; archival typical and AC neon data do not qualify exact DC lamps; #7 | Lamp primary specs and bench test plan; approved total worst simultaneous current and rated HV resistors | OPEN |
| PWR-001 | P0 | TPS61023 low-cell 5V/thermal/startup needs actual L1 and effective C; Cmax HV charge energy included; #8 | Worst-case supply, current limit, selected L1 Isat,DCR, C eff, thermal simulation + supervised bench measurements | OPEN |
| PWR-002 | P0 | BQ charge/BAT assist losses and signed IBAT, actual cell/NTC/thermal bounds; #8 | Quantified component losses, BATFET extrapolation warnings, charger states, thermal test inside planned enclosure | OPEN |
| BAT-001 | P0 | Actual protected 21700/NTC still unselected; part sourcing #7, rating/thermal validation #8 | Cell + protection spec, NTC verified attached to cell, discharge/charge/temp limits, connector/test plan | OPEN |
| SYS-001 | P0 | HV 16mA supply/demand mismatch; 500mA-configured USB-only cannot sustain target even ideally; [WORK-INT-001](2026-11-17-work-integration-001.md) | Mode contract: evidenced lamp demand, low-cell/USB/BAT-assist/charging/audio/OLED states, continuous/startup power and thermal bounds | OPEN |
| CTRL-001 | P1 | HV5524/OE gate, RTC backup, AMP analog input and off-domain leakage unfinished | Correct manufacturer pin mapping, power-off-fail-safe interface, low-voltage tests | OPEN |
| NET-001 | P1 | Physical HV and LV connectors and insulation not fixed | Manufacturer-referenced parts, pin1 match and creepage/clearance assessment | OPEN |
| BOM-001 | P1 | 11/15 BOM is historical; current stock/tax/shipping and key parts not qualified; staged prototype sourcing #7 | Dated, reproducible itemized cost incl. shipping/tax/PCB/rework; initial ≤40k, reserve ≥10k | OPEN |
| SYS-002 | P0 | Joint HV capacitor / OVP / startup / discharge contract; [INT-002](2026-11-18-work-integration-002.md), D-013 | One real Cmin/Cmax, bounded tail energy, startup surplus, discharge time/faults and reviewed margins; #6/#8 | OPEN |
| PROTO-001 | P0 | No traceable staged prototype part/sourcing matrix; #7 | Exact lamp/cell/magnetics/controller/capacitor/safety candidates, evidence holds, current costs/lead times and staged BOM | OPEN |

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
