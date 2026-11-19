# THERM-001 / Issue #9 — adapter-ramp charge-permit race and supply-domain safety contract
Date: 2026-11-20 00:04 JST. Role: Chat A / deep-design. Branch: `codex/reva-integrated-prototype-review`.
Starting branch commit SHA: UNKNOWN (connected fetch_file returns file blob SHA, not branch HEAD; git ls-remote unavailable due DNS). Claim: PROVISIONAL, NO FORMAL CLAIM. Review: PENDING REVIEW.
Verdict: CONDITIONAL (logical timing necessity), BLOCKED (actual hardware safety).

## Bounded contract
Question: Does the proposed adapter-powered pullup + permission-only sink guarantee charge inhibition during USB insertion and monitor brownout? Scope excludes selecting resistor values, modifying /CE schematic, or claiming charger response times. Exit: explicit counterexample, timing inequality, fault-mode verification matrix, and primary evidence needed.
Inputs re-read on target branch: docs/ai-workflow.md, docs/verification/handoff.md, docs/verification/open-issues.md, docs/verification/decisions.md, docs/tech-tree.yaml, docs/tech-tree.md, docs/reva-integrated-net-spec.md, 2026-11-19-2002 THERM-001 report, 2026-11-19-1600 THERM-001 report, GitHub Issues #9/#8/#6/#2. Current branch report discovery via tree API not available in this connector; these are latest known A reports, not an exhaustive newest-report claim. Chat B/C latest unenumerated reports may exist; do not claim no overlap.

## Primary reference and factual baseline
TI BQ25185 datasheet Rev.B (Aug 2026): https://www.ti.com/lit/ds/symlink/bq25185.pdf ; /CE LOW permits charging, HIGH inhibits charging; TS measurement is not active in battery-only (§6.4 p19). Exact VIH/VIL, /CE default bias, charger enable delay and TS qualification timing are UNKNOWN here; no values attributed to TI.
Project source: docs/reva-integrated-net-spec.md and WORK-INT-003 identify /CE=GND on PWR draft; thermal hold D-008/D-015. Candidate circuit in 2026-11-19-2002 report proposes VBUS-present pullup and permission-only open-drain sink, NOT implemented.

## Novel timing counterexample
A passive pullup to adapter VBUS is not automatically a guaranteed inhibit during VBUS ramp. If VBUS is below the valid HIGH threshold while the charger input has already entered a state where charging is possible, /CE can be LOW/undefined. Also if the permit sink remains conducting after monitor power-good falls (output undervoltage behavior not specified), the pullup cannot raise /CE. Thus **static truth tables are insufficient**.

Define times relative to a USB insertion event:
- t_CHG_EARLIEST = earliest time the charger can source charging current under any allowed input/temperature corner;
- t_CE_SAFE = latest time /CE is guaranteed HIGH with margin, including adapter ramp, pullup RC, pin leakage, and monitor output state;
- t_MON_VALID = latest time temperature sensor/monitor and its supply become valid;
- t_PERMIT_ASSERT = earliest time the sink may pull /CE LOW.
For a fail-inhibit argument without relying on internal charger delays, require that **for every instant charging could occur**, /CE is already guaranteed HIGH unless qualified permission is valid. A sufficient (not necessary) start condition is t_CE_SAFE < t_CHG_EARLIEST, with positive timing margin, plus t_PERMIT_ASSERT >= t_MON_VALID and sensor validity confirmed. If t_CHG_EARLIEST is UNKNOWN, this inequality cannot be verified and a passive pullup alone is NOT a proven startup interlock.

On USB removal/brownout, monitor power-good can fall before charger loses charge capability. Require an inhibit response bounded before unsafe charging could persist, or independent physical charging interruption; the exact allowed duration is determined by the selected cell safety specification and charger behavior, not assumed zero.

## Candidate architecture comparison (research only)
A. Adapter-derived pullup + open-drain permission sink: low parts count, but VBUS ramp threshold race, /CE-to-GND short, sink-short and power-domain backfeed remain. Must measure or guarantee internal charge behavior and pin bias.
B. Independent adapter-valid supervisor that inhibits /CE until temperature monitor valid: improves deterministic logic only if supervisor output has specified state across 0V-to-valid rail and the /CE HIGH rail itself exists before charging; cannot fix /CE short.
C. Independent series charge interruption plus /CE: can cover some /CE shorts if the series device defaults open and truly interrupts battery charge current, but topology must preserve permitted battery→SYS discharge, USB supplement, reverse-feed and pack safety. A generic series MOSFET is NOT automatically bidirectional isolation; body diode and source/drain reversal require explicit analysis.
D. Manufacturer-qualified pack temperature charge cutoff: possible independent layer only after exact PCM thermal cutoff/recovery and installation evidence; no claim that a generic protected 21700 contains this function.

## Minimum corner/fault matrix for next component-level study
1. USB rise: 0V, slow ramp, fast ramp, brownout oscillation; cell present/absent; monitor powered/unpowered.
2. MCU reset, 3V3 absent, ADC/TS disconnected, monitor output stuck LOW/HIGH, open-drain short, /CE short to GND, pullup open.
3. USB unplug while battery drives SYS; ensure no monitor I/O backfeed and no unsafe default charge permit on reinsertion.
4. Charge-stop versus battery-only load-stop versus HV stored-energy discharge: distinct controls; /CE does not isolate HV output.
5. For any added series MOSFET, prove both directions and single faults; specify if cell discharge through BQ BATFET is affected.

## Falsifiable component acceptance data needed
TI Rev.B /CE pin VIH(min), VIL(max), input leakage, internal pull and absolute maximum, charger start/stop delay and startup behavior across VBUS ramps; monitor/supervisor guaranteed output for VDD=0 through UVLO; selected cell allowed charge temperature and PCM charge FET behavior; load-stop/hard-off electrical path. Record GUARANTEED vs TYPICAL vs UNKNOWN. With no bounded t_CHG_EARLIEST, static /CE resistor sizing is insufficient for safety qualification.

## Decision and handoff
CONDITIONAL: a necessary power-sequencing/timing contract and concrete counterexample are established; no new numerical component ratings claimed.
BLOCKED: no manufacturer-guaranteed ramp behavior, actual logic thresholds, supervisor, or charge interruption part qualified. PENDING REVIEW for Chat C and Work. New issue not created: existing #9 covers this interface. No shared ledger edits (integrator owns them).
Suggested next task: retrieve BQ25185 Rev.B exact /CE startup electrical table and characterize candidate power-good supervisor datasheets; compare A/B/C by guaranteed defaults, fault coverage, extra GPIO/pins and BOM, then request explicit schematic-change authorization. No purchases, PCB manufacture, HV energization, main merge, or requirements changes.
