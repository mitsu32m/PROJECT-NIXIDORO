# Handoff — PROJECT-NIXIDORO

Current snapshot: **2026-11-19 JST**. Examined HEAD: **6ac0d8c966e2f76731997c0c5c45c220cf835bc3**. Always fetch live branch HEAD; this SHA identifies the evidence baseline, not a permanent current head.

## Current decision package

[WORK-INT-003](2026-11-19-work-integration-003.md) integrates C-REVIEW-003/004/005/006. **Comparative research CONDITIONAL; actual battery, sensor, full-HV operating and manufacturing adoption BLOCKED.**

**Highest new concern: thermal enforcement across charge and battery-only operation.** TI BQ25185 Rev.B §6.4 p19 (NOT Table 6-2) has TS Measurement NO in battery-only. Current PWR source/netlist confirms U1 pin4 /CE=GND and U1 pin6 TS/MR=J5 pin3 CELL_NTC. Direct 10k/B3435 plus a protected cell does not automatically enforce cell charge/discharge temperature limits. Candidate Keeppower P2150K official page charge +10..45C is incompatible with an unmodified direct NTC nominal TS window (~1.74/59.51C ideal-beta entry); actual parts/limits still unselected. /CE disables charging, not SYS/HV energy.

New [#9 THERM-001](https://github.com/mitsu32m/PROJECT-NIXIDORO/issues/9): define charge inhibit and separate battery-only monitor/enforcement with real R/T, total error/lag, hysteresis, sensor faults and MCU-off behavior. No schematic change authorized by this document.

## Reviewed scope and correction

- [C-003](2026-11-18-1502-JST-C-REVIEW-003-sys001e-f-dcm-startup.md): mixed B DCM operating point CHANGES_REQUESTED; startup energy algebra accepted only as assumed sensitivity. Supports D-013 joint capacitor assessment.
- [C-004](2026-11-18-2103-JST-C-REVIEW-004-hv004-lamp-sys001-direct-mode.md): mode/direct-SYS algebra and AC source classification reviewed; actual DC lamp/controller/magnetics selection blocked. Corrections in INT-003.
- [C-005](2026-11-19-0302-JST-C-REVIEW-005-pwr002a-proto001bcd-batch.md): A static source/path calculations and B electrical sensor candidates reviewed within assumptions. High-current BATFET R and 27C OCP extrapolations are NOT continuous safe limits.
- [C-006](2026-11-19-0905-JST-C-REVIEW-006-ts-entry-te-probe-primary-check.md): TS ideal math accepted; TE STM010 PDF body 20±1mm/1m, not 15mm. PDF/web environmental conflict and attachment/lag/fault safety unresolved. Correct TI source to §6.4/p19.

TE nominal R/T is not exact ideal B3435. Work's new restricted proof that Rs+(Rp||NTC) cannot widen R10/R45 enough for candidate 10/45C entries is **PENDING C REVIEW**; no universal compensation rejection or part value adopted.

## Unchanged system target and blockers

Around 200–205V/16mA continuous target remains. 500mA-configured USB-only full load is impossible by input/output energy; battery assist may discharge cell. No qualified actual HV topology+magnetics pair, independent OVP/hard-stop/discharge, capacitor Cmin/Cmax, low-cell PWR startup/thermal or cell/NTC assembly is proven. MAX668 ordinary boost alone is rejected; coupled, 5V flyback and direct-SYS alternatives remain candidates. 70us shutdown is TYP, not bounded maximum. MCU BL and firmware stops are not isolation.

Pico2/RTC/OLED/UI remain prior proposals; RTC backup, OE, reverse feed and thermal state interfaces unfinished. Board/enclosure thermal paths, cell-holder/probe geometry and temperature fault response remain open. No hardware node newly verified or release gate unlocked.

## Next role contracts — GitHub handoff, no formal Claim

- **A:** #9 thermal enforcement architecture/interface; #8 real cell/charger/5V quantitative model; continue actual HV #2 and OVP/energy #6. Explain exact proposed circuit-change scope before implementation.
- **B:** #7 complete exact cell/PCM/probe/holder evidence and assembly cost; prioritize actual DC lamp and currently sourceable magnetic/controller pair alongside remaining sensor clarification. No more NTC-only qualitative restatements without new part/drawing/qualification evidence.
- **C:** next important batch #2 oldest A tapped 23:59/03:55/07:56 + B 11/18 13:02 magnetics sourcing; independently challenge #9 Work ratio proof. Do not treat acceptance of equations as hardware qualification.
- **Work:** batch new material judgments, preserve historical rejected branches and bounded review states; no blanket re-review of unchanged reports.

## Prototype and budget preparation

D-014 staged proposal: cell/HV-free PWR/CTRL evaluation planning with simulators first; qualified cell/NTC assembly next; standalone HV/dummy-load safety plan only after its gates; sealed integrated evaluation last. No purchase/test authorization implied.

New hardware/integration/thermal-qualification-holds.csv records partial candidate holds and historical price provenance, NOT an order BOM. Full tax/shipping/PCB/rework-inclusive <=50k total /<=40k initial/>=10k reserve unproven. Protected cell may be ~75mm long; STM010 body20±1mm plus leads/strain relief needs actual CAD; fit/thermal lag unknown.

Deadline 2027-01末. Proposed internal checkpoints remain 11/25 real-part evidence, 12/01 architecture/power/thermal decisions, 12/15 first-order decision package. Escalate long-lead evidence before these dates; dates are not supplier promises or purchase permissions.

Next user decisions once concrete alternatives/costs exist: charger/cell maintenance with extra protection vs combination change; UI simultaneous display and USB net-charge requirements; staged prototype scope and explicit purchase/test authorization. No requirement changed in this run.

## Automation observation 2026-11-19

Lookup found four active project tasks: A6/day, B6/day, C3/9/15/21 JST, weekly separate review. No Work/self-owned task found. environments=null, Work quota/runtime inheritance unavailable; no new task or update. Proven alternative remains A/B/C GitHub accumulation plus manual Work batch integration. Twice/day is a future ceiling, not an enabled Work schedule.

## Historical evidence

Earlier integrations are preserved: [INT-001](2026-11-17-work-integration-001.md), [INT-002](2026-11-18-work-integration-002.md), C-001/002, and their original reports. Previous handoff snapshot is versioned at [examined pre-update SHA](https://github.com/mitsu32m/PROJECT-NIXIDORO/blob/6ac0d8c966e2f76731997c0c5c45c220cf835bc3/docs/verification/handoff.md). Its unavailable-review statements are superseded by the current scoped review list above; no research report deleted.
