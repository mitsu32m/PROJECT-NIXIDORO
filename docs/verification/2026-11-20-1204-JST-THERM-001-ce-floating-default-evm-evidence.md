# THERM-001 / Issue #9 — BQ25185 /CE floating-default evidence from TI EVM
Date: 2026-11-20 12:04 JST. Role: Chat A deep-design.
Branch: codex/reva-integrated-prototype-review. Starting branch HEAD: UNKNOWN (branch-specific HEAD not established by available connector; do not substitute blob SHA).
Claim: NONE; provisional selection from open-issues.md. Review status: **PENDING REVIEW**.
Verdict: **NO-GO (limited)** for floating /CE as a charge inhibit or fail-safe. **CONDITIONAL** for an independent pull-up proposal pending verified power and timing. **BLOCKED** for implemented charge/thermal safety.

## Task contract
Question: Does leaving /CE unconnected naturally inhibit charging during loss of the MCU or its pull-up supply? Exit: identify manufacturer EVM behavior and establish a fault-state counterexample. Excludes KiCad edits, part adoption, HV tests, purchase and requirement changes.

## Evidence and novelty
1. **TI primary EVM user's guide, SLUUCS1 (October 2023), Table 2-1 J4 /CE connector**: "Connects /CE pin to higher if populated. Leave floating for low." This is the EVM's described default configuration, **not** a guaranteed across-process/temperature internal pull-down electrical specification. Source mirror: https://device.report/m/32e0bf9cecddb220242ae5d93ac99f88809e8b46910798ec64df065626f91ee6 ; verify original TI publication and revision before design signoff.
2. **TI BQ25185 manufacturer datasheet, SLUSF65A (revised January 2026), Table 5-1**: /CE pin4 is active-low: HIGH disables charging, LOW enables. https://www.ti.com/lit/ds/symlink/bq25185.pdf . The current repository describes a later Rev.B source; exact revision, electrical limits and any changed default behavior require cross-revision confirmation.
3. Baseline docs/reva-integrated-net-spec.md confirms /CE=GND in proposed PWR schematic; 2026-11-20-0802-JST-THERM-001-ce-power-domain-independence.md establishes Pico-3V3-only pullup power loss counterexample.
4. Required repository state reread: docs/ai-workflow.md, docs/verification/handoff.md, docs/verification/open-issues.md, docs/verification/decisions.md, docs/tech-tree.yaml, docs/tech-tree.md and issue #9; latest report enumeration and exact branch HEAD are not guaranteed by connector.

## Specific new finding
A floating /CE cannot be assumed HIGH. TI's EVM guide explicitly describes floating as LOW on its board. Combining this with active-low charge enable creates a plausible *charge-permitted* condition when a control transistor, pull-up rail or connector becomes open-circuit. This strengthens the prior structural NO-GO from 'HIGH not guaranteed' to an **EVM-supported failure counterexample**, but does not prove every bare IC will read LOW while floating. Treat pin input leakage, internal bias, ramp response and temperature as UNKNOWN until guaranteed TI specifications or TI written confirmation.

| Failure state | /CE guaranteed inhibit? | Implication |
|---|---|---|
| Rev.A /CE tied GND | No | Charging enabled subject to other internal controls |
| Proposed Pico-derived pullup, Pico 3V3=0, USB valid | No | /CE may float or be pulled LOW; EVM floating LOW observation relevant |
| Independent USB-domain pullup present and verified HIGH | Candidate only | Must prove VIN ramp, VIH, leakage, max rating and monitor validity |
| Pullup resistor open / disconnected | No | Floating is not a safety state |
| /CE hard short GND | No | Additional independent interruption needed if single-fault protection is required |

## Design consequence / exit evidence
- Never credit floating /CE as a default charging-disabled state. Require a defined HIGH bias from a power domain that is valid when USB charging is possible, plus a proof of ramp timing or an independently effective charge-cut path.
- For any candidate, capture manufacturer **guaranteed** /CE input leakage, VIH/VIL, absolute max, power-on/off behavior, EVM vs bare IC differences, and monitor UVLO/output default. Demonstrate no charge-permit gap on USB hot-plug/brownout and no overvoltage at /CE.
- Keep battery-only thermal load cutoff and HV stored-energy discharge separate from /CE. The TS measurement is inactive in battery-only mode per TI mode table. Do not equate BQ junction thermal protection with selected cell temperature protection.
- Proposed schematic scope (not authorized): replace hard GND /CE connection with independently powered inhibit network; potentially add independent thermal supervisor/second cut path and cell temperature sensor/harness, then review fault table, current budget, cost, creepage and PWR/CTRL pins.
- TI EVM J4 behavior is **not** a silicon guarantee; request source validation by Chat C before any acceptance. No new Issue needed: #9 covers the concern.

## Status and handoff
PENDING REVIEW; no hardware proof. Chat C should challenge the EVM interpretation and cross-check Rev.B silicon specs. Work should preserve /CE=GND as a thermal HOLD and not mark thermal gate complete. No main merge, purchase, PCB manufacturing, HV energization or material specification change.
