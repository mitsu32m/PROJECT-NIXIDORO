# THERM-001 / Issue #9 — charge inhibit logic defaults and fault containment
Date: 2026-11-19 20:02 JST. Role: Chat A (deep design). Branch: `codex/reva-integrated-prototype-review`.
Starting HEAD: UNKNOWN (contents API provides blob SHA, not commit SHA; commit search did not resolve current branch HEAD). Claim: PROVISIONAL, NO FORMAL CLAIM. Review: PENDING REVIEW.
Verdict: CONDITIONAL for Boolean and passive-network design constraints; BLOCKED for physical charge/load thermal safety.

## Task contract
Question: Can the existing BQ25185 /CE=GND baseline enforce a safe charger-disable state when MCU, comparator or sensor supply fails? Determine a falsifiable fail-safe interface contract and the minimum circuit changes needed, without choosing an unverified device or changing the schematic.
Exit: truth table, static electrical inequalities, fault counterexamples and an exact authorization scope.
Inputs re-read: docs/ai-workflow.md; docs/verification/handoff.md; docs/verification/open-issues.md; docs/verification/decisions.md; docs/tech-tree.yaml and docs/tech-tree.md; WORK-INT-003; previous A THERM-001 sensor loading report; Issue #9 and #8. This work adds charge-enable default logic, not another NTC R/T sensitivity calculation.

## Primary evidence and known net
TI BQ25185 datasheet Rev.B (Aug 2026): https://www.ti.com/lit/ds/symlink/bq25185.pdf . /CE LOW permits charging and HIGH inhibits charging; TS is not measured in battery-only mode (§6.4 p19). This is a charge gate, NOT a battery/SYS or HV energy isolation gate.
Existing Rev.A PWR schematic/netlist as documented in WORK-INT-003: U1 pin4 /CE=GND; U1 pin6 TS/MR=J5 CELL_NTC. No separately controllable charge inhibit path is currently proven. Actual logic VIH/VIL, /CE pin leakage, absolute maximum, pullup domain, startup power sequencing, and internal bias MUST be checked against the exact datasheet before selecting resistor or attaching logic.

## Novel failure-mode counterexamples
1. Present /CE=GND cannot be driven HIGH by firmware or external comparator without changing the net. Therefore no software-only temperature algorithm can claim to inhibit charging on the present hardware.
2. Replacing GND with MCU push-pull GPIO does not by itself fail safe: at reset/brownout the pin may be high impedance, default LOW, or back-powered. An assumed reset HIGH is not evidence.
3. A passive pullup plus a transistor that sinks /CE only on explicit permission can make an *open-circuit* monitor/MCU failure default to charge inhibited, but a transistor drain-source short or a /CE-to-GND wiring short still forces charge enabled. Hence this is not single-fault-complete protection.
4. A powered comparator output without validated undervoltage state can assert permission during supply ramp. An MCU-based gate also cannot replace independently qualified charge temperature enforcement during MCU-off conditions.
5. A shared sensor physically detached but electrically intact defeats both charge and load readers of that same sensor, even with separate circuits. Sensor attachment qualification remains a separate safety requirement.

## Candidate architecture (NOT APPROVED)
Define CHARGE_PERMIT = VALID_SENSOR AND TEMP_WITHIN_CHARGE_WINDOW AND MONITOR_POWER_GOOD AND NOT_FAULT_LATCHED. A normally-off sink device may pull /CE LOW **only** while CHARGE_PERMIT is positively established; otherwise a pullup makes /CE HIGH. The pullup must reference a supply present whenever adapter charging is possible, with a proven safe voltage relative to BQ pin ratings. Do not assume Pico 3V3 is alive when adapter is present. Confirm power-up order and backfeed isolation.

| Adapter | Monitor power | Sensor/fault state | CHARGE_PERMIT | Desired /CE | HV/load |
|---|---|---|---|---|---|
| absent | any | any | 0 | HIGH/inhibit default | independent discharge-temperature policy |
| present | good | valid and within qualified charge range | 1 | LOW/permit conditional | independent load gate |
| present | good | cold/hot/open/short/latched fault | 0 | HIGH/inhibit | independent load gate |
| present | absent/brownout | any | 0 | HIGH/inhibit | independently stop as required |
| present | good | sink transistor short to GND | cannot enforce | LOW (unsafe counterexample) | charge path needs separate protection |

The last row is a failure counterexample, not an allowed operating state. For a single-fault safety case, investigate an independent physical charge-interruption element or a qualified pack protection function with manufacturer-guaranteed temperature thresholds; do not assume a PCM includes temperature cutoff.

## Static logic sizing contract (symbolic; not component values)
For pullup R_PU to a valid V_PU and aggregate worst-case downward leakage I_LEAK, require
V_CE,OFF,min = V_PU,min - I_LEAK,max * R_PU >= V_IH,max + M_H
where M_H>0 is design margin and all quantities are evaluated at actual temperature, adapter and MCU-off corners.
For sink ON with guaranteed maximum sink voltage V_SINK,max, require V_CE,ON,max <= V_IL,max - M_L.
Also ensure sink current I_SINK >= (V_PU,max - V_SINK,max)/R_PU plus any pin bias; check sink capability and power. The actual VIH/VIL and leakage are UNKNOWN in this report, so no numeric resistor is adopted. Input ESD clamp current and absence of monitor supply require explicit proof.

## Change request scope (for Work/human, NOT executed)
- Remove the hard /CE-to-GND connection only after reviewed approval.
- Add adapter-alive default-inhibit pullup, permission-only open-drain sink, and power-good/temperature-fault logic with documented reset and hysteresis.
- Keep BQ TS/MR functions intact and evaluate whether an independent pack-mounted sensor is required; no unreviewed parallel TS loading.
- Add an independently enforceable battery-only load/HV-stop path and retained HV capacitor discharge contract (#6). /CE alone cannot stop the HV converter.
- Require separate fault-injection analysis for /CE short to ground, sink short, sensor detachment, power rail failure, and firmware hang. If single-fault tolerance is demanded, an independent charge interrupt path or qualified PCM is a design prerequisite.

## Classification and next steps
GUARANTEED (manufacturer functional description): /CE LOW enables charging and HIGH inhibits; battery-only TS inactive per cited TI Rev.B. DOCUMENTED (repository): current /CE grounded. ASSUMED: candidate pullup/sink topology, positive margin. UNKNOWN: actual threshold/leakage/supply corners, comparator choice, component price, cell PCM behavior, fault-tolerant physical disconnect, installation thermal lag.
CONDITIONAL: candidate logic defaults for open-circuit and unpowered-monitor faults *if* pullup domain and thresholds are validated.
BLOCKED: actual temperature-window enforcement, single-fault safety, battery-only protection, part adoption, schematic release. PENDING REVIEW for Chat C and Work.
Next evidence: retrieve exact BQ25185 /CE pin electrical specs and selected comparator/power-good output defaults across brownout; produce a component-level truth table and full fault matrix; pair with actual cell PCM specification from Chat B. No purchase, PCB production, HV energization, main merge or requirement change.
