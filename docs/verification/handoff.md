# Handoff — PROJECT-NIXIDORO

Snapshot: **2026-11-17 JST**. This file contains facts checked from project reports and open design decisions. Always re-read GitHub HEAD before working.

## Objective

Rechargeable Pomodoro timer, protected 1S 21700 cell, Raspberry Pi Pico 2 MCU, two IN-12B Nixie digits and twelve NE-2-class neon indicator lamps, OLED, UI and optional audio. HV output **around 200–205 V nominal, up to 16 mA continuous design target** (not proven). Total target JPY 50,000, initial spend target ≤JPY 40,000, JPY 10,000 reserve. No purchasing, fabrication or HV tests authorized.

## Working files and ownership

- Branch `codex/reva-integrated-prototype-review`, integrated schematics at `hardware/pwr/RevA-integrated-draft/`, `hardware/ctrl/RevA-draft/`, `hardware/hv/RevA-draft/`.
- Historical PWR at `hardware/pwr/RevA-draft-v3/`.
- Existing source-of-truth design description: `docs/reva-integrated-net-spec.md`.
- Detailed reviews: `docs/reva-integrated-prototype-review.md`, `docs/hv-architecture-decision.md`, `docs/hv-transformer-screen.md`, `docs/hv-voltage-window.md`, `docs/pwr-reva-power-thermal-review.md`.
- Reproducible calculations: `hardware/hv/hv-option-model.py`, `hardware/hv/hv-voltage-window.py`, `hardware/hv/transformer-screen.py`, `hardware/integration/system-load-model.py`, `hardware/pwr/RevA-draft-v3/power-model.py`. Associated CSV exist in these directories.

## Current architecture — proposed, not approved

- USB-C power input via protection/eFuse into TI BQ25185 (4.2 V cell selection, nominal ~250 mA charging, ~500 mA configured input limit). Battery temperature uses cell-attached 10 kΩ B3435 NTC **proposed**, actual cell and integrated NTC are not selected.
- BQ SYS → external Schottky → Pico 2 VSYS; Pico's 3V3(OUT) → OLED + RV-3028-C7 RTC. Separate TPS63031 is omitted from Rev.A proposal.
- BQ SYS → TPS61023 → 5 V logic/HV input. 5 V rail capacity at low battery and thermal limit is not proven for full HV load.
- Pico GP0–3 → SN74LV4T125 → HV5524. HV5524 BL=LOW, POL=HIGH yields outputs OFF **only under valid logic supply conditions**. Never substitute for HV power isolation.
- HV side MAX668 preliminary controller. **Existing HV schematic cannot generate HV**: transformer, MOSFET, rectifier, feedback, current sense, independent OVP, discharge are incomplete. Use only for a design discussion.
- Pico GP17 → PWR signal J3 pin10 for ADC_SENSE_EN, operating PWR MOS-gated dividers (100 kΩ/47 kΩ, 1 nF). J3 10-pin proposed. Off-state reverse-feed remains unverified.
- Audio amp SYS supply is optional and analog input filtering/Power-off GPIO coupling are unresolved.
- RTC backup hardware/EEPROM settings not complete.

## Most urgent blockers

1. **P0 HV power train**: 5 V →205 V/16 mA with available transformer of verifiable Lp, turns ratio, Isat, leakage, temperature, dielectric ratings and sourcing. The MAX668 one-stage 5 V→205 V boost is invalid due to insufficient maximum duty.
2. **P0 HV voltage safety window**: MAX668 205 V nominal FB worst-case static high ~214.13 V with ±1% feedback resistors, leaving only ~5.87 V below HV5524 recommended 220 V. Independent OVP tolerance plus dynamic overshoot have not been accommodated.
3. **P0 HV hardware safety**: separate OVP, fault-latched shutdown, discharge time, connector insulation and touch prevention absent. No HV energization.
4. **P0 power and thermal**: 205 V×16 mA=3.28 W HV out. With assumed ηHV=70% and η5V=85%, HV input alone requires ~5.51 W from SYS **before other loads**; USB-only 500 mA is insufficient. Low-cell, inductor saturation, IC heat and sealed PETG temperatures lack test results.
5. **P0 cell**: specific protected 21700 chemistry/model, discharge rating, temperature constraints, connector, NTC and enclosure heat are unknown.
6. **P1 manufacturing**: HV resistor voltage/power rating, sockets, connector pin1/locking/cable specification, footprints and all-in price unconfirmed.

## Existing quantitative caution

- MAX668 one-stage ideal D=1−5/205≈97.56%, exceeding its specified maximum duty (87/90/93% for given frequency resistance).
- LT8304-1 with its 2 A lower limit and lowest 4.75 V supply requires **idealized** efficiency ≥85.05% for 1:10 and ≥77.05% for 1:5 at 205 V×16 mA, per `docs/hv-transformer-screen.md`. Neither has proved actual efficiency.
- If 200–205 V is mandated as an across-temperature **guaranteed** range, MAX668 FB tolerance alone makes it infeasible under the analyzed feedback topology. Distinguish nominal target from guaranteed range.
- XP Power F05 module and high voltage charge-pump/cascade options studied; none has a documented confirmed fit for 5 V/205 V/16 mA under current budget and thermal constraints.

## Recommended immediate next research task

Identify a *manufacturer-documented* flyback transformer/power-stage combination for 5 V min input, approximately 205 V and at least 16 mA continuous, including efficiency/thermal/safe shutdown evidence. If unavailable, compare reduced-current target (such as 4–8 mA) with actual IN-12B and neon lamp brightness/current requirements. **Do not infer a transformer is suitable just from ratio or distributor listing.**

## Definition of done before release

Independent OVP and hard-off with worst-case tolerances/transients below HV5524 recommended limit; quantified discharge under single fault; actual transformer/FET/diode loss and temperature; PWR 5 V load and 21700 thermal/current constraints; tested ADC/USB reverse feed; confirmed actual component footprints and connectors; measured lamp currents; safe bench protocol with qualified supervisory review; final BOM within budget. No item is considered passed based on ERC only.

## AI collaboration rule

Treat previous AI work as a *claim to audit*, not a guaranteed fact. Include exact references and status in every report; don't silently upgrade preliminary calculations into approved circuit values. Use append-only dated evidence and update issue/decision indexes, and never automatically alter KiCad or authorize high voltage, hardware purchasing, PR merge or PCB fabrication.

## 2026-11-17 — latest Work integration (WORK-INT-001)

Evidence: [integrated review](2026-11-17-work-integration-001.md), baseline 0d83c2d0d551e0893aa1eced613a250ec6a12181. **CONDITIONAL research / BLOCKED final HV selection / PENDING REVIEW.**
No new Chat B research or Chat C judgment package was located in the examined branch tree, Issues #1/#2 comments or PR search. Chat A's latest [10:25 screen](2026-11-17-1025-JST-HV-001-max668-quantitative-screen.md) is unreviewed; do not promote its sizing proxies to selected circuit ratings.

Immediate integration priority is SYS-001 (now P0): establish actual lamp demand (proposed HV-004A) and a mode-specific HV/PWR/CTRL power contract while [Issue #2](https://github.com/mitsu32m/PROJECT-NIXIDORO/issues/2) proceeds on coupled topology. This supplements the earlier transformer-first task, without changing 205V/16mA targets. 16mA comes from assumed 2mA×2 tubes +1mA×12 neons. Even ideal 5V×498mA=2.49W input is below 3.28W HV output; higher-rated USB adapter alone cannot fix BQ's current setting. USB presence may mean battery supplementation, not charging.

At prior assumed efficiencies/allocations, full target needs 6.601W SYS before audio; converter losses are 2.321W, **not** whole-enclosure heat. Lamp/resistor/driver, logic/UI, charger and cell losses also matter. No thermal or safety gate is passed.

Review clarification: full −40..85°C MAX668 table gives 222–278kHz for ROSC=200kΩ±1%; 225–275kHz applies 0..85°C. Keep temperature scope explicit. C-REVIEW-001 is proposed for both latest A report and this integration.

No final topology or BOM values adopted; KiCad unchanged. Batch next Work run on important reviewed power-stage, load, OVP or thermal evidence. Twice/day remains a future ceiling; no schedule or usage quota verified and no automation changed.
