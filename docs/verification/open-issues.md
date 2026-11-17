# Open technical issues — living register

Updated 2026-11-17 JST. Priorities: **P0** blocks safety or physical feasibility; **P1** blocks implementation/manufacturability; **P2** optimizations. Every automated run should select the highest-value unresolved issue and record its own review, with explicit evidence and close criteria.

| ID | Priority | Issue / current evidence | Exit criterion | State |
|---|---|---|---|---|
| HV-001 | P0 | No proven 5 V→205 V /16 mA continuous flyback magnetics+controller combination. One-stage MAX668 boost fails duty check. | Manufacturer primary electrical spec, feasibility calculation including losses/thermal/startup and evidence path | OPEN |
| HV-002 | P0 | 205 V nominal w/MAX668 1% FB gives static high ~214.13 V; HV5524 220 V recommended max | Full FB+OVP tolerances incl. transient & fault-stop latency below 220 V, with acceptable operating window | OPEN |
| HV-003 | P0 | Independent OVP, fault shutdown, discharge circuit not built | Detailed circuit, single-fault analysis, shutdown under power loss/reset, controlled discharge to defined safe voltage/time, supervised review | OPEN |
| HV-004 | P0 | Actual IN-12B & neon current/brightness/limiting resistors not proven | Lamp primary specs and bench test plan; approved total worst simultaneous current and rated HV resistors | OPEN |
| PWR-001 | P0 | TPS61023 low-cell 5 V full load / temperature / startup | Worst-case supply, current limit, selected L1 Isat,DCR, C eff, thermal simulation + supervised bench measurements | OPEN |
| PWR-002 | P0 | BQ25185 thermal and SYS assist, charging under load | Quantified component losses, BATFET extrapolation warnings, charger states, thermal test inside planned enclosure | OPEN |
| BAT-001 | P0 | Protected 21700 actual part/current and 10k B3435 NTC not selected | Cell + protection spec, NTC verified attached to cell, discharge/charge/temp limits, connector/test plan | OPEN |
| SYS-001 | P1 | HV 16 mA + audio + OLED and USB-only cases not assured | End-to-end worst-case power/heat/supply analysis and operating-state gating | OPEN |
| CTRL-001 | P1 | HV5524/OE gate, RTC backup, AMP analog input and off-domain leakage unfinished | Correct manufacturer pin mapping, power-off-fail-safe interface, low-voltage tests | OPEN |
| NET-001 | P1 | Physical HV and LV connectors and insulation not fixed | Manufacturer-referenced parts, pin1 match and creepage/clearance assessment | OPEN |
| BOM-001 | P1 | 50,000 JPY total budget not verified; many major items unpriced | Dated, reproducible itemized cost incl. shipping/tax/PCB/rework; initial ≤40k, reserve ≥10k | OPEN |

## Issue handling

For each dated verification log, update issue `State` to `IN REVIEW`, `BLOCKED`, `RESOLVED (scope)` only with grounded evidence; link dated log in the relevant row. Maintain prior claims when correcting, by describing superseding result. No result is considered `RESOLVED` solely because an ERC check returns zero violations.
